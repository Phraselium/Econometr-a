"""V18 · E8 · fiscalidad de la compra (ITP por comunidades): orquestación (estimabilidad → estimación → pruebas → clasificación → Holm → salidas).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan_replicacion.md §1.8 + adenda R-18, 1.3, 1.6, 1.7, 1.12, anexos A-C).
Orden de la adenda 1.3: mínimos de datos y MDE ANTES de mirar ningún coeficiente; lo que no los supera queda «NO ESTIMABLE por variación» y no se estima.
Reglas de codificación de fechas de la adenda (R-18) en e8_datos.py. Aleatorización del calendario entre comunidades como inferencia principal
(dcdh_aleatorizacion: APTO, tamaño 0,0455); Webb con 7-8 comunidades NO APTO (solo se rotula). Determinista (SEED 20261010), sin red.

Uso: python3 src/v18/estimacion/e8_itp.py
Salidas: output/v18/estimacion/e8/{estimabilidad.csv, calendario.csv, registry.csv, tabla.csv, resultado.json, hechos.json, informe.md}
Lecturas: solo con sellado.filtrar + holdout.excluir_sellados_v6 (a través de _e2e8_comun, e8_datos y e8_diseno). Nunca data/sealed.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e8_datos as D8  # noqa: E402
import e8_diseno as DS  # noqa: E402
import e8_estim as E  # noqa: E402
from herramientas import dcdh as DC  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
OUT = DS.OUT
B_P, B_IC, B_VAR = 9999, 1999, 4999
ELL_R1 = 4

SPECS = {   # id: (rol, familia, repite_visto, resultado, fórmula)
    "E8-R1": ("principal", "E8", "sí (Q6-p)", "log valor tasado provincial trimestral", "dCDH con dosis continua (ℓ = 4 trimestres): Δtipo general del ITP en puntos"),
    "E8-R2": ("principal", "E8", "sí (Q6-v)", "log compraventas de vivienda usada provinciales mensuales", "dCDH con dosis continua (ℓ = 12 meses)"),
    "E8-A1": ("principal", "E8", "no", "recaudación del ITP por comunidad", "primera etapa fiscal"),
    "E8-A2": ("principal", "E8", "no", "log compraventas municipales (municipios grandes)", "dCDH con dosis continua (ℓ = 4 trimestres)"),
    "E8-X1": ("NO ESTIMABLE", "fuera", "-", "bunching en los umbrales de los tipos reducidos", "-"),
    "E8-X2": ("NO ESTIMABLE", "fuera", "-", "tipos reducidos para jóvenes y familias", "-"),
    "E8-P-Q6p": ("coprincipal", "E8", "sí", "log valor tasado provincial anual", "V16-Q6-p: Wald-DID anual 2011-2024, fechas por año de efecto"),
    "E8-P-Q6v": ("coprincipal", "E8", "sí", "log compraventas provinciales anuales", "V16-Q6-v: Wald-DID anual 2011-2024"),
}
NO_EST_DATOS = {
    "E8-X1": "no hay compraventas por tramo de precio (Notariado o AEAT modelo 600; tareas_autor, punto 7)",
    "E8-X2": "faltan el calendario de tipos reducidos (leyes autonómicas) y las compraventas por tramo (tareas_autor, punto 7)",
}
VARIANTES = {
    "E8-R1": [("v1", "M", "fechas del 1 de enero"), ("v2", "M", "fechas −3 meses"), ("v3", "M", "fechas +3 meses"), ("v4", "V", "sin 2012-2013 (cambiantes fuera de esos años)"),
              ("v5", "E", "subidas por separado (Sun-Abraham)"), ("v6", "E", "bajadas por separado (Sun-Abraham)"), ("v7", "M", "IPV por comunidad"),
              ("v8", "U", "sin Barcelona"), ("v9", "C", "sin recaudación previa")],
    "E8-R2": [("v1", "M", "fechas del 1 de enero"), ("v2", "M", "fechas −3 meses"), ("v3", "M", "fechas +3 meses"), ("v4", "V", "sin 2012-2013"),
              ("v5", "E", "subidas por separado"), ("v6", "E", "bajadas por separado"), ("v7", "U", "sin Barcelona"), ("v8", "C", "sin recaudación previa")],
    "E8-A1": [("v1", "V", "sin 2012-2013"), ("v2", "M", "fechas del 1 de enero")],
    "E8-A2": [("v1", "V", "sin 2012-2013"), ("v2", "U", "sin Barcelona")],
}
FUENTES = ["intervenciones.csv de V16 (tipos del ITP: Ministerio de Hacienda, «Tributación Autonómica. Medidas» 2010-2026, fuente secundaria)",
           "MIVAU, valor tasado de vivienda libre por provincia (base: valor_tasado)", "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"]


def comprobar_sin_selladas(codigos, nivel: str = "provincia") -> None:
    """Postcondición: ningún código del panel pertenece a los bloques sellados de v6 (holdout.excluir_sellados_v6 no quita nada)."""
    cods = pd.DataFrame({"cod": [str(c) for c in codigos]})
    assert len(K.holdout.excluir_sellados_v6(cods, "cod", nivel)) == len(cods), "unidades selladas en el panel"


def pf(x, n=4):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def fila_base(id_, rol, fam, rep, res, estado, nota="") -> dict:
    return {"id": id_, "rol": rol, "familia": fam, "repite_visto": rep, "resultado": res, "estado": estado, "n_provincias": None, "n_comunidades": None, "n_obs": None,
            "coef": None, "se": None, "p_t": None, "p_aleat": None, "p_i7": None, "ic95_lo": None, "ic95_hi": None, "tipo_ic": "", "p_webb_no_fiable": None,
            "q_by": None, "p_holm": None, "clase": "", "nota": nota}


def idx_mask(periodos: list[str], excluir: tuple[str, str]) -> np.ndarray:
    """Máscara de periodos del cambio (índice del periodo del cambio menos 1 = posición en dD): True fuera de la ventana excluida."""
    return np.array([not (excluir[0] <= p[:4] <= excluir[1]) for p in periodos[1:]])


def preparar(prov: dict, ev: pd.DataFrame, provs_excluir: tuple = ()) -> dict:
    keep = np.array([c not in provs_excluir for c in prov["cod"]])
    ccaa = prov["ccaa"][keep]
    cc = sorted(set(ccaa))
    cl = np.array([cc.index(x) for x in ccaa])
    Dc, _ = D8.calendarios(ev, prov["cols"], "T", cc)
    return {"Y": prov["Y"][keep], "cl": cl, "Dc": Dc, "cols": prov["cols"], "cc": cc, "cod": prov["cod"][keep]}


def estimar_variante(p: dict, ell: int, mask=None, B: int = B_VAR) -> dict:
    r = E.principal(p["Y"], p["Dc"], p["cl"], ell, B, B, mask=mask, ic=False)
    return r


def wald_anual_panel(provs: dict) -> dict:
    """Panel anual de la coprincipal de V16 (Q6-p): log valor tasado provincial 2010-2024 y tipos por año de efecto (calendario de 2011-2024 con t − 1)."""
    s = K.leer_hechos("valor_tasado", "provincia", "A")
    anios = [str(a) for a in range(2010, 2025)]
    w = s[s.territorio_codigo.isin(provs)].pivot_table(index="territorio_codigo", columns="periodo", values="valor", aggfunc="first").reindex(columns=anios)
    w = w.dropna(how="all")
    cc = sorted(set(provs[c] for c in w.index))
    cl = np.array([cc.index(provs[c]) for c in w.index])
    t = D8.tipos_generales()
    t["a"] = t.fecha.dt.year
    Dc = np.full((len(cc), len(anios)), np.nan)
    for i, c in enumerate(cc):
        g = t[t.cod_ine == c]
        for j, a in enumerate(anios):
            prev = g[g.a <= int(a)]
            Dc[i, j] = float(prev.tipo.iloc[-1]) if len(prev) else np.nan
    return {"Y": np.log(w.values), "cl": cl, "Dc": Dc, "cols": anios, "cod": np.array(w.index), "cc": cc}


def wald_anual(Y: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Wald-DID de V16 (anual, dosis continua): por año t, cambiantes = ΔD ≠ 0 sin cambio al año siguiente; controles = ΔD = 0 sin cambio al año siguiente; la suma de
    (ΔY − media ΔY de controles) entre la suma de ΔD. Admite lote (..., n, T). Solo diferencias entre años consecutivos con dato."""
    dy = Y[..., 1:] - Y[..., :-1]
    dd = np.where(np.isfinite(dy), D[..., 1:] - D[..., :-1], np.nan)      # solo diferencias entre años consecutivos con dato (corrección K16)
    ddf = np.concatenate([dd[..., 1:], np.full(dd.shape[:-1] + (1,), np.nan)], axis=-1)
    ok = np.isfinite(dy) & np.isfinite(dd)
    sw = ok & (dd != 0) & (np.nan_to_num(ddf, nan=0.0) == 0)
    ct = ok & (dd == 0) & (np.nan_to_num(ddf, nan=0.0) == 0)
    n0 = ct.sum(-2)
    m = np.where(n0 > 0, (np.where(ct, dy, 0.0)).sum(-2) / np.maximum(n0, 1), 0.0)
    valido = (n0 > 0) & (sw.sum(-2) > 0)
    num = (np.where(sw & valido[..., None, :], dy - m[..., None, :], 0.0)).sum((-2, -1))
    den = (np.where(sw & valido[..., None, :], dd, 0.0)).sum((-2, -1))
    return np.where(den != 0, num / np.where(den != 0, den, 1.0), np.nan)


def p_wald_aleat(p: dict, B: int, semilla: int = K.SEMILLA) -> dict:
    Y, cl, Dc = p["Y"], p["cl"], p["Dc"]
    b0 = float(wald_anual(Y, Dc[cl]))
    perms = DC.permutaciones(np.random.default_rng(semilla), Dc.shape[0], B)
    bp = np.concatenate([wald_anual(Y[None], Dc[perms[i:i + 400]][:, cl, :]) for i in range(0, B, 400)])
    bp = bp[np.isfinite(bp)]
    pv = float((1 + np.sum(np.abs(bp) >= abs(b0) - 1e-12)) / (len(bp) + 1))
    return {"coef": b0, "p_aleat": pv, "sd_placebo": float(bp.std(ddof=1)), "n_obs": int(np.isfinite(Y).sum()), "n_perm": int(len(bp))}


def main() -> int:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    est, pan = DS.estimabilidad()
    for k_, v_ in pan.items():
        comprobar_sin_selladas(v_["panel"]["cod"], "municipio" if k_ == "E8-A2" else "provincia")
    est.to_csv(OUT / "estimabilidad.csv", index=False, float_format="%.6f")
    estim = est.set_index("id")
    ev = D8.eventos("exacta")
    cal = ev.assign(fecha_codificada_mes=ev.fecha.map(D8.mes_codificado), fecha_codificada_trimestre=ev.fecha.map(D8.trimestre_codificado),
                    calidad_fecha=np.where(ev.aprox, "aproximada (1 de enero)", "de la memoria de Hacienda, sin contraste con el BOE"))
    cal.to_csv(OUT / "calendario.csv", index=False)
    reg = K.Registry(OUT / "registry.csv")
    for ident, (rol, fam, rep, res, form) in SPECS.items():
        e = estim.loc[ident] if ident in estim.index else None
        n = int(e.n_unidades) if e is not None and pd.notna(e.n_unidades) else 0
        reg.log("v18-E8-prereg", ident, form, "2007", "2026", n, np.nan, np.nan, np.nan, notas=f"{rol}; registrada antes de estimar (estimabilidad calculada sin coeficientes)")
    for ident, vs in VARIANTES.items():
        for suf, dim, desc in vs:
            reg.log("v18-E8-prereg", f"{ident}-{suf}", f"variante [{dim}] {desc}", "", "", 0, np.nan, np.nan, np.nan, notas="variante enumerada (adenda anexo A)")
    reg.flush()
    print("estimabilidad registrada:", {k: bool(v) for k, v in estim.estimable.items()}, flush=True)

    filas, diag = [], {}
    for ident, motivo in NO_EST_DATOS.items():
        rol, fam, rep, res, *_ = SPECS[ident]
        filas.append(fila_base(ident, rol, fam, rep, res, "NO ESTIMABLE", motivo) | {"clase": "NO ESTIMABLE"})
    for ident in ("E8-R2", "E8-A1", "E8-A2"):
        rol, fam, rep, res, *_ = SPECS[ident]
        e = estim.loc[ident]
        estado = "NO ESTIMABLE (mínimo de datos)" if not e.minimo_ok else "NO ESTIMABLE por variación (MDE)"
        filas.append(fila_base(ident, rol, "fuera", rep, res, estado, e.motivo_no_estimable) | {"clase": "NO ESTIMABLE", "n_provincias": int(e.n_unidades), "n_comunidades": int(e.n_comunidades)})
        for suf, dim, desc in VARIANTES[ident]:
            filas.append(fila_base(f"{ident}-{suf}", "variante", "fuera", rep, res, "NO ESTIMABLE (hereda la principal)", f"[{dim}] {desc}; {e.motivo_no_estimable}") | {"clase": "NO ESTIMABLE"})
    filas.append(fila_base("E8-P-Q6v", *SPECS["E8-P-Q6v"][:4], "NO ESTIMABLE (hereda la principal)", f"se estima al lado de E8-R2, que no supera la estimabilidad: {estim.loc['E8-R2'].motivo_no_estimable}")
                 | {"clase": "no se clasifica", "familia": "fuera"})

    fam_p, cuerpo = {}, {}
    if estim.loc["E8-R1"].estimable:
        rol, fam, rep, res, form = SPECS["E8-R1"]
        v = pan["E8-R1"]["panel"]
        p = preparar(v, ev)
        r = E.principal(p["Y"], p["Dc"], p["cl"], ELL_R1, B_P, B_IC)
        ref = DS.ESPEC["E8-R1"]
        r["tost"] = K.tost(r["coef"], r["se"], ref["delta"], r["G"] - 1)
        f = fila_base("E8-R1", rol, fam, rep, res, "estimada", "fechas de la memoria de Hacienda (sin contraste con el BOE); sin control de recaudación previa (no descargada)")
        f.update({"n_provincias": len(p["cod"]), "n_comunidades": len(p["cc"]), "n_obs": r["n_obs"], "coef": r["coef"], "se": r["se"], "p_t": r["p_t"], "p_aleat": r["p_aleat"],
                  "p_i7": r["p_aleat_i7"], "ic95_lo": r["ic_aleat"][0], "ic95_hi": r["ic_aleat"][1], "tipo_ic": "inversión de la aleatorización de calendarios (ℓ = 4)"})
        f["p_webb_no_fiable"] = E.webb_no_fiable(p["Y"], p["Dc"], p["cl"], ELL_R1, B_VAR)
        dk = E.twfe_dk(p["Y"], p["Dc"], p["cl"])
        # I de Moran de los residuos medios por provincia del TWFE de la dosis (diagnóstico espacial del pre-registro)
        nP, TP = p["Y"].shape
        mT = K.Modelo(p["Y"].ravel(), p["Dc"][p["cl"]].ravel(), np.repeat(np.arange(nP), TP), np.tile(np.arange(TP), nP), cluster=np.repeat(p["cl"], TP))
        moran = K.moran_i(K.residuo_medio_por_unidad(mT), D8.centroides_provincias(p["cod"]))
        # adelantos (−8 a −2 trimestres) y pendiente detectable
        ad = E.adelantos(p["Y"], p["Dc"], p["cl"], list(range(2, 9)), B_VAR)
        pend = E.pendiente_detectable(ad["perm"], ad["ks"], 8, ELL_R1)
        # placebo de fecha: adelanto de 8 trimestres (dos años antes)
        i8 = ad["ks"].index(8)
        placebo_fecha = {"coef": ad["g"][i8], "p": ad["p_k"][8], "mismo_signo": bool(np.sign(ad["g"][i8]) == np.sign(r["coef"]))}
        # placebo de resultado: log de la población provincial (anual), ℓ = 1 año
        pp = D8.panel_poblacion({c: D8.provincias_e8()[c] for c in p["cod"]})
        ccp = sorted(set(pp["ccaa"]))
        clp = np.array([ccp.index(x) for x in pp["ccaa"]])
        Dct, _ = D8.calendarios(ev, p["cols"], "T", ccp)
        Dca = E.anual_desde_trimestral(Dct, p["cols"], pp["cols"])
        rp = E.principal(pp["Y"], Dca, clp, 1, B_VAR, B_VAR, ic=False)
        placebo_res = {"coef": rp["coef"], "p": rp["p_aleat"], "n_prov": len(pp["cod"])}
        diag["E8-R1"] = {"r": r, "dk": dk, "moran": moran, "adelantos": ad, "pendiente": pend, "placebo_fecha": placebo_fecha, "placebo_resultado": placebo_res, "p": p, "f": f}
        filas.append(f)
        fam_p["E8-R1"] = f["p_i7"]
        # ---------------------------------------------------------- variantes
        for suf, dim, desc in VARIANTES["E8-R1"]:
            idv = f"E8-R1-{suf}"
            fv = fila_base(idv, "variante", fam, rep, res, "estimada", f"[{dim}] {desc}")
            if suf in ("v1", "v2", "v3"):
                modo = {"v1": "enero", "v2": "menos3", "v3": "mas3"}[suf]
                ev_v = D8.eventos(modo)
                Dcv, _ = D8.calendarios(ev_v, p["cols"], "T", p["cc"])
                rv = estimar_variante({**p, "Dc": Dcv}, ELL_R1)
            elif suf == "v4":
                rv = estimar_variante(p, ELL_R1, mask=idx_mask(p["cols"], ("2012", "2013")))
            elif suf == "v5":
                fv.update({"estado": "NO ESTIMABLE", "clase": "NO ESTIMABLE",
                           "nota": f"[{dim}] {desc}: todas las comunidades del panel suben el tipo en algún momento, así que Sun-Abraham no tiene comunidades nunca tratadas"})
                filas.append(fv)
                continue
            elif suf == "v6":
                sa = E.sun_abraham_bajadas(p["Y"], p["Dc"], p["cl"], 999)
                if not sa["estimable"]:
                    fv.update({"estado": "NO ESTIMABLE", "clase": "NO ESTIMABLE", "nota": f"[{dim}] {desc}: sin comunidades tratadas o sin controles"})
                else:
                    fv.update({"coef": sa["coef"], "se": sa["se"], "p_t": sa["p_webb"], "n_provincias": len(p["cod"]),
                               "nota": f"[{dim}] {desc}: {sa['n_tr']} comunidades con bajadas y {sa['n_co']} sin ellas; p de Webb sin banda propia de Monte Carlo (puntual)"})
                filas.append(fv)
                continue
            elif suf == "v7":
                ipv = K.leer_hechos("ipv", "ccaa", "T")
                wi = K.ancho(ipv[ipv.territorio_codigo.isin(p["cc"])], p["cols"]).dropna()
                if len(wi) < len(p["cc"]):
                    fv.update({"estado": "NO ESTIMABLE", "clase": "NO ESTIMABLE", "nota": f"[{dim}] {desc}: IPV disponible para {len(wi)} de {len(p['cc'])} comunidades"})
                    filas.append(fv)
                    continue
                wi = wi.reindex(p["cc"])
                pv = {**p, "Y": np.log(wi.values), "cl": np.arange(len(p["cc"]))}
                rv = estimar_variante(pv, ELL_R1)
            elif suf == "v8":
                pv = preparar(v, ev, provs_excluir=("08",))
                rv = estimar_variante(pv, ELL_R1)
            else:   # v9
                fv.update({"estado": "coincide con la principal", "coef": r["coef"], "p_aleat": r["p_aleat"], "p_t": r["p_t"], "se": r["se"],
                           "nota": f"[{dim}] {desc}: la principal ya va sin control de recaudación (la fuente no está descargada)"})
                filas.append(fv)
                continue
            fv.update({"n_provincias": rv["n_obs"] // len(p["cols"]) if suf != "v7" else len(p["cc"]), "n_obs": rv["n_obs"], "coef": rv["coef"], "se": rv["se"], "p_t": rv["p_t"], "p_aleat": rv["p_aleat"],
                       "p_i7": rv["p_aleat_i7"], "ic95_lo": rv["ic_t"][0], "ic95_hi": rv["ic_t"][1], "tipo_ic": "t con G − 1 gl (comunidad)"})
            filas.append(fv)
    # ------------------------------------------------------------------ coprincipal P-Q6p (V16, muestra V18)
    if estim.loc["E8-R1"].estimable:
        rol, fam, rep, res, form = SPECS["E8-P-Q6p"]
        pa = wald_anual_panel(D8.provincias_e8())
        rq = p_wald_aleat(pa, B_P)
        f = fila_base("E8-P-Q6p", rol, fam, rep, res, "estimada", "")
        f.update({"n_provincias": len(pa["cod"]), "n_comunidades": len(pa["cc"]), "n_obs": rq["n_obs"], "coef": rq["coef"], "p_aleat": rq["p_aleat"], "p_i7": K.p_corr(rq["p_aleat"], 0.0415),
                  "clase": "no se clasifica"})
        f["nota"] = ("cifra publicada V16-Q6-p: −0,0020 por pp (puntual, sin inferencia: dCDH con aleatorización NO APTO en V16); en la muestra V18 se reproduce el estimador anual y se añade "
                     "la aleatorización de calendarios (estadístico: coeficiente)")
        filas.append(f)
        fam_p["E8-P-Q6p"] = f["p_i7"]
        diag["E8-P-Q6p"] = {"r": rq, "n_prov": len(pa["cod"])}
    tab = pd.DataFrame(filas)
    holm = K.holm_familia({k: v for k, v in fam_p.items() if v is not None and np.isfinite(v)})
    for k, v in holm.items():
        tab.loc[tab.id == k, "p_holm"] = v
    vv = tab[(tab.rol == "variante") & tab.id.str.startswith("E8-R1-") & tab.p_aleat.notna() & (tab.estado == "estimada")]
    if len(vv):
        tab.loc[vv.index, "q_by"] = multipletests(vv.p_aleat.values, alpha=0.10, method="fdr_by")[1]

    # ------------------------------------------------------------------ clasificación de E8-R1
    clasif = {}
    if "E8-R1" in diag:
        di = diag["E8-R1"]
        r = di["r"]
        ref = DS.ESPEC["E8-R1"]
        vv = tab[(tab.rol == "variante") & tab.id.str.startswith("E8-R1-") & (tab.estado == "estimada")]
        signo = np.sign(r["coef"])
        b4 = vv[vv.id.isin(["E8-R1-v7", "E8-R1-v8"])]
        v4 = tab[tab.id == "E8-R1-v4"]
        sin_1213_cambia = bool(len(v4) and np.sign(v4.coef.iloc[0]) != signo)
        # K7 (B6, ronda 1): el signo sin 2012-2013 es una prueba B4 (plan 0.5 y línea 737) y un cambio de signo en B4 es fallo decisivo (plan, línea 124);
        # el tope de la adenda R-18 es un techo y no anula esa regla.
        robustez = {"frac_mismo_signo": float((np.sign(vv.coef) == signo).mean()) if len(vv) else None, "n_variantes": int(len(vv)),
                    "cambio_signo": bool((np.sign(b4.coef) != signo).any()) if len(b4) else False, "solape_ic": None}
        robustez["cambio_signo"] = bool(robustez["cambio_signo"] or sin_1213_cambia)
        topes = ["fechas de entrada en vigor de la memoria de Hacienda, sin contraste con el BOE ni con el diario autonómico: SUGESTIVO como máximo (plan, 1.8 f)",
                 "sin control de recaudación previa (fuente no descargada): tope SUGESTIVO (adenda R-18)",
                 "tope SUGESTIVO por corrección de un fallo conocido de Q6 (fechas; adenda 1.6)"]
        info = {"estimable": True, "coprincipal": False, "p_holm": float(tab.loc[tab.id == "E8-R1", "p_holm"].iloc[0]), "coef": r["coef"], "pretend_p": di["adelantos"]["p_conjunto"],
                "roth_ok": bool(di["pendiente"]["sesgo_post"] < 0.5 * ref["ref"]), "placebo_fecha": di["placebo_fecha"],
                "placebo_resultado": "falla" if di["placebo_resultado"]["p"] <= 0.10 else "ok", "robustez": robustez, "inferencia_banda": K.banda_mc(E.TAM_ALEAT), "topes": topes,
                "tost": K.tost(r["coef"], r["se"], ref["delta"], r["G"] - 1), "nulo_sin_sugestivo": True,
                "texto_cambio_signo": "el signo cambia sin 2012-2013 (prueba B4 del plan, línea 737): cambio de signo en B4 = fallo decisivo (plan, línea 124; K7)"}
        clasif["E8-R1"] = {"info": info, "clase": K.clasificar(info)}
        tab.loc[tab.id == "E8-R1", "clase"] = clasif["E8-R1"]["clase"]["clase"]
    tab.to_csv(OUT / "tabla.csv", index=False, float_format="%.6f")
    for r_ in tab.itertuples():
        if r_.estado.startswith(("estimada", "coincide")):
            reg.log("v18-E8-estimada", r_.id, r_.resultado, "", "", int(r_.n_obs) if r_.n_obs == r_.n_obs and r_.n_obs is not None else 0, np.nan, np.nan, np.nan,
                    coef_interes=r_.coef if r_.coef is not None else np.nan, p_interes=r_.p_aleat if r_.p_aleat is not None else np.nan, notas=f"{r_.rol}; clase {r_.clase}")
        else:
            reg.log("v18-E8-no-estimada", r_.id, r_.resultado, "", "", 0, np.nan, np.nan, np.nan, notas=r_.estado)
    reg.flush()
    from e8_salidas import escribir
    escribir(OUT, est, tab, diag, clasif, cal, time.time() - t0)
    print(f"E8 hecho en {time.time() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
