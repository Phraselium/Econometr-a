"""V18 · E2 · topes al alquiler: orquestación (estimabilidad → estimación → pruebas → clasificación → Holm → salidas).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan_replicacion.md §1.2 + adenda §1.1-1.12, anexos A-C).
Orden fijado por la adenda 1.3: la estimabilidad (mínimos de datos y MDE) se calcula y se registra ANTES de mirar ningún coeficiente; lo que no
la supera queda «NO ESTIMABLE por variación» y no se estima. Determinista (SEED 20261010), sin red.

Uso: python3 src/v18/estimacion/e2_topes.py
Salidas: output/v18/estimacion/e2/{estimabilidad.csv, registry.csv, tabla.csv, estudio_eventos_r1.csv, resultado.json, hechos.json, informe.md}
Lecturas: solo con sellado.filtrar + holdout.excluir_sellados_v6 (a través de _e2e8_comun, e2_datos y e2_diseno). Nunca data/sealed.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_diseno as DS  # noqa: E402
import e2_estim as E  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
OUT = DS.OUT
B_P, B_IC, B_VAR, B_ALEAT = DS.B_P, DS.B_IC, DS.B_VAR, 9999
FUENTES = "Incasòl (fianzas, municipio-trimestre); cataluna_contencion_rentas_v3.csv de v3 (Ley 11/2020, BOE-A-2020-11363)"
ANIOS_V8 = ["2014", "2015", "2016", "2017", "2018", "2019", "2021"]
ANIOS_V9 = ["2016", "2017", "2018", "2019", "2021"]
ANIOS_PF = ["2014", "2015", "2016", "2017", "2018", "2019"]
ANIOS_IRPF = ["2016", "2017", "2018", "2019", "2021"]

# id: (rol, familia, repite_visto, resultado, fórmula, ini, fin)
F_R1 = "ln renta_mt = β·Reg_m·Post_t + θ·Reg_m·1[t=2020T3] + α_m + γ_t + ε (Post = 2020T4-2022T1; base 2019T4)"
SPECS = {
    "E2-R1": ("principal", "E2", "sí (V9-D1b)", "log renta media de contratos nuevos", F_R1, "2019T1", "2022T1"),
    "E2-R1c": ("principal", "E2", "sí (V9-D1b)", "log contratos por 1.000 habitantes", F_R1.replace("renta_mt", "(contratos/pob)_mt"), "2019T1", "2022T1"),
    "E2-A1": ("principal (provisional)", "E2", "sí (H1, H2)", "log renta media de contratos nuevos", "CS, cohortes 2024T2 y 2024T4, nunca tratados", "2022T1", "2026T1"),
    "E2-A2": ("principal", "E2", "sí (V9-D1c)", "log renta mensual EMAL", "SDID/CS País Vasco", "2016T1", "2025T4"),
    "E2-A3": ("principal", "E2", "sí (Q1c)", "log compraventas por 1.000 habitantes", "TWFE anual 2016-2022", "2016", "2022"),
    "E2-A4": ("principal", "E2", "no", "log renta media de contratos nuevos", "TWFE cerca (< 10 km) frente a lejos (> 25 km)", "2019T1", "2022T1"),
    "E2-P-D1b": ("coprincipal", "E2", "sí", "log renta media de contratos nuevos", "V9-D1b: CS nunca tratados, 2019T1-2022T1", "2019T1", "2022T1"),
    "E2-P-D1b-c": ("coprincipal", "E2", "sí", "log contratos nuevos", "V9-D1b (contratos): CS nunca tratados", "2019T1", "2022T1"),
    "E2-P-H1": ("coprincipal", "E2", "sí", "log renta media de contratos nuevos", "V15-H1: SDID, cohortes 2024", "2022T2", "2026T1"),
    "E2-P-H2": ("coprincipal", "E2", "sí", "log(1 + contratos)", "V15-H2: SDID, cohortes 2024", "2022T2", "2026T1"),
    "E2-P-D1c": ("coprincipal", "E2", "sí", "log renta EMAL", "V9-D1c: CS aún no tratados, EMAL", "2016T1", "2025T4"),
    "E2-P-Q1c": ("coprincipal", "E2", "sí", "log compraventas provinciales", "V16-Q1c: CS provincial, zonas de 2024", "2019T1", "2026T2"),
    "E2-R2": ("NO ESTIMABLE (adenda R-2)", "fuera", "-", "PPML por tramo", "-", "", ""),
    "E2-R2s": ("NO ESTIMABLE (adenda R-2)", "fuera", "-", "proporción por tramo", "-", "", ""),
    "E2-R2-X1": ("NO ESTIMABLE (adenda R-2)", "fuera", "-", "precio en exceso", "-", "", ""),
    "E2-A5": ("NO ESTIMABLE", "fuera", "-", "alquiler de temporada", "-", "", ""),
}
NO_EST_DATOS = {
    "E2-R2": "el campo de tramo de Incasòl clasifica al municipio y no reparte sus contratos (docstring de incasol en src/v9/paneles.py; adenda R-2); hacen falta microdatos de contratos con renta, renta anterior y superficie (tareas_autor, punto 4)",
    "E2-R2s": "ídem E2-R2",
    "E2-R2-X1": "ídem E2-R2: precio de referencia, renta anterior y superficie por contrato (tareas_autor, punto 4)",
    "E2-A5": "faltan las fianzas por tipo de contrato o el Registro Único (tareas_autor, punto 4)",
}
VARIANTES = {   # id padre: [(sufijo, dimensión, descripción)]
    "E2-R1": [("v1", "V", "sin 2020T1-2020T3"), ("v2", "U", "con Barcelona ciudad"), ("v3", "C", "controles por covariables (vecino más cercano)"),
              ("v4", "C", "controles a más de 10 km"), ("v5", "C", "sin covariables"), ("v6", "C", "densidad HUT 2019 × posterior"),
              ("v7", "E", "anticipación desde 2019T2"), ("v8", "V", "anual 2014-2021 con Honest DiD"), ("v9", "M", "SERPAVI municipal anual 2016-2021"),
              ("v10", "P", "ponderada por contratos de 2019"), ("v11", "U", "sin el 1 % de municipios con más contratos")],
    "E2-R1c": [("v1", "M", "contratos por hogar inquilino"), ("v2", "E", "PPML"), ("v3", "V", "sin 2020T1-2020T3"), ("v4", "U", "con Barcelona")],
    "E2-A1": [("v1", "E", "efectos fijos de dos vías"), ("v2", "E", "emparejamiento por puntuación de propensión"), ("v3", "E", "SDID"),
              ("v4", "U", "sin Barcelona"), ("v5", "V", "2023T1-2026T1")],
    "E2-A2": [("v1", "M", "€/m²"), ("v2", "U", "sin Bilbao")],
    "E2-A3": [("v1", "M", "valor tasado"), ("v2", "U", "sin Barcelona"), ("v3", "V", "trimestral 2019-2022")],
    "E2-A4": [("v1", "C", "vecinos directos"), ("v2", "C", "10-25 km frente a > 25 km")],
}
HOLGURA = [("E2-R1-h1", "E2-R1", "paro registrado con 2020 interpolado linealmente (el de 2020 no está en la base): solo robustez, holgura de la adenda 1.8")]


def comprobar_sin_selladas(codigos, nivel: str = "municipio") -> None:
    """Postcondición: ningún código del panel pertenece a los bloques selladas de v6 (holdout.excluir_sellados_v6 no quita nada)."""
    cods = pd.DataFrame({"cod": [str(c) for c in codigos]})
    assert len(K.holdout.excluir_sellados_v6(cods, "cod", nivel)) == len(cods), "unidades selladas en el panel"


def pf(x, n=4):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def fila_base(id_, rol, fam, rep, res, estado, nota="") -> dict:
    return {"id": id_, "rol": rol, "familia": fam, "repite_visto": rep, "resultado": res, "estado": estado, "n_tratados": None, "n_controles": None,
            "n_obs": None, "G": None, "coef": None, "se_cr1": None, "p_cr1": None, "ic95_lo": None, "ic95_hi": None, "tipo_ic": "", "p_webb": None,
            "p_i7": None, "p_aleat": None, "p_aleat_conglom": None, "p_webb_conglom": None, "se_conley10": None, "p_dk_no_fiable": None, "q_by": None,
            "p_holm": None, "clase": "", "nota": nota}


def rellena(f: dict, r: dict, q: dict | None = None, principal: bool = False) -> dict:
    f.update({"n_obs": r.get("n_obs"), "G": r.get("G"), "coef": r["coef"], "se_cr1": r.get("se"), "p_cr1": r.get("p_cr1"), "p_webb": r.get("p_webb"),
              "p_i7": r.get("p_webb_i7")})
    if principal and np.isfinite(r.get("ic_webb", (np.nan,))[0]):
        f.update({"ic95_lo": r["ic_webb"][0], "ic95_hi": r["ic_webb"][1], "tipo_ic": "inversión del Webb (WCR-t, nulo impuesto)"})
    elif r.get("ic_cr1") is not None:
        f.update({"ic95_lo": r["ic_cr1"][0], "ic95_hi": r["ic_cr1"][1], "tipo_ic": "CR1 por municipio, t(G−1)"})
    if q is not None:
        f["n_tratados"], f["n_controles"] = q["n_tr"], q["n_co"]
    return f


def variante_trim(d, ident, suf, resultado, base_ic, rng_seed):
    """Estimación de una variante trimestral: devuelve (fila-resultado, panel). Inferencia: CR1 y Webb (B_VAR), sin IC de Webb."""
    kw = {"v1": dict(drop=(4, 5, 6), ant=()), "v2": dict(con_barcelona=True), "v3": dict(matching=True), "v4": dict(grupo="10km"),
          "v6": dict(covar="hut"), "v7": dict(ant=tuple(range(1, 7))), "v10": dict(pesos="contratos2019"), "v11": dict(sin_p99=True),
          "h1": dict(covar="paro")}
    if ident == "E2-R1c":
        kw = {"v3": dict(drop=(4, 5, 6), ant=()), "v4": dict(con_barcelona=True)}
    m, q = E.spec_trim(d, resultado, **kw[suf])
    r = E.inferir(m, B_VAR, B_IC, ic=False, semilla=rng_seed)
    return r, q


def main() -> int:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    d = DS.cargar()
    est, pan = DS.estimabilidad(d)
    for p_ in pan.values():
        comprobar_sin_selladas(p_["cod"])
    est.to_csv(OUT / "estimabilidad.csv", index=False, float_format="%.6f")
    estim = est.set_index("id")
    reg = K.Registry(OUT / "registry.csv")
    # ---------------------------------------------------------------- Registry: toda especificación, antes de leer ningún coeficiente
    for ident, (rol, fam, rep, res, form, ini, fin) in SPECS.items():
        e = estim.loc[ident] if ident in estim.index else None
        n = int(e.n_tratados + e.n_controles) if e is not None and pd.notna(e.n_tratados) else 0
        reg.log("v18-E2-prereg", ident, form, ini, fin, n, np.nan, np.nan, np.nan, notas=f"{rol}; registrada antes de estimar (estimabilidad calculada sin coeficientes)")
    for ident, vs in VARIANTES.items():
        for suf, dim, desc in vs:
            reg.log("v18-E2-prereg", f"{ident}-{suf}", f"variante [{dim}] {desc}", "", "", 0, np.nan, np.nan, np.nan, notas="variante enumerada (adenda anexo A)")
    for hid, padre, desc in HOLGURA:
        reg.log("v18-E2-prereg", hid, desc, "", "", 0, np.nan, np.nan, np.nan, notas="holgura (adenda 1.8); motivo en desviaciones")
    reg.flush()
    print("estimabilidad registrada:", {k: bool(v) for k, v in estim.estimable.items()}, flush=True)

    filas, diag, es_tab = [], {}, None
    # ---------------------------------------------------------------- no estimables por datos (adenda R-2)
    for ident, motivo in NO_EST_DATOS.items():
        rol, fam, rep, res, *_ = SPECS[ident]
        filas.append(fila_base(ident, rol, fam, rep, res, "NO ESTIMABLE", motivo) | {"clase": "NO ESTIMABLE"})
    # ---------------------------------------------------------------- especificaciones principales que no superan la estimabilidad
    for ident in ("E2-A1", "E2-A2", "E2-A3", "E2-A4"):
        rol, fam, rep, res, *_ = SPECS[ident]
        e = estim.loc[ident]
        filas.append(fila_base(ident, rol, "fuera" if not e.estimable else fam, rep, res, ("NO ESTIMABLE (mínimo de datos)" if not e.minimo_ok else "NO ESTIMABLE por variación (MDE)"),
                               e.motivo_no_estimable) | {"clase": "NO ESTIMABLE", "n_tratados": int(e.n_tratados), "n_controles": int(e.n_controles)})
        for suf, dim, desc in VARIANTES[ident]:
            filas.append(fila_base(f"{ident}-{suf}", "variante", "fuera", rep, res, "NO ESTIMABLE (hereda la principal)", f"[{dim}] {desc}; {e.motivo_no_estimable}") | {"clase": "NO ESTIMABLE"})
    herencia = {"E2-P-H1": "E2-A1", "E2-P-H2": "E2-A1", "E2-P-D1c": "E2-A2", "E2-P-Q1c": "E2-A3"}
    for ident, padre in herencia.items():
        rol, fam, rep, res, *_ = SPECS[ident]
        filas.append(fila_base(ident, rol, "fuera", rep, res, "NO ESTIMABLE (hereda la principal)", f"se estima al lado de {padre}, que no supera la estimabilidad: {estim.loc[padre].motivo_no_estimable}") | {"clase": "no se clasifica"})

    estimables = [i for i in ("E2-R1", "E2-R1c") if estim.loc[i].estimable]
    fam_p = {}                                           # p de Holm de la familia E2
    cuerpo = {}
    # ================================================================ E2-R1 y E2-R1c
    for ident, resultado, serie_anual, pop_ in (("E2-R1", "renta", "rA", False), ("E2-R1c", "contratos", "cA", True)):
        if ident not in estimables:
            continue
        rol, fam, rep, res, form, ini, fin = SPECS[ident]
        ref = DS.ESPEC[ident]
        m, q = E.spec_trim(d, resultado)
        r = E.inferir(m, B_P, B_IC, ic=True)
        f = rellena(fila_base(ident, rol, fam, rep, res, "estimada"), r, q, principal=True)
        # inferencias alternativas
        cl = E.conglomerados(q, d)
        m_c = E.twfe_panel(q["Y"], q["tr"], E.POST_COLS, (E.ANT_COL,), cluster=cl)
        f["p_webb_conglom"] = m_c.webb_p(0.0, B_VAR, np.random.default_rng(K.SEMILLA))
        pre = [0, 1, 2, 3, 4, 5]
        al = E.aleatorizar(q["Y"], q["tr"], pre, E.POST_COLS, B_ALEAT)
        al_c = E.aleatorizar(q["Y"], q["tr"], pre, E.POST_COLS, B_ALEAT, estrato=cl)
        f["p_aleat"], f["p_aleat_conglom"] = al["p"], al_c["p"]
        f["se_conley10"] = m.conley(E.coords(q, d), 10.0)
        dk = E.dk_trimestral(r, q["Y"], q["tr"].astype(float), E.ANT_COL)
        moran = K.moran_i(K.residuo_medio_por_unidad(m), E.coords(q, d))
        f["p_dk_no_fiable"] = dk["p"]
        # estudio de eventos, pretendencias y potencia de Roth
        ev = E.evento_trimestral(q["Y"], q["tr"].astype(float))
        # placebo de fecha (anual 2014-2019, adopción falsa en 2017)
        pa = E.panel_anual(d, serie_anual, ANIOS_PF, [], por_mil_hab=pop_)
        mpf = E.twfe_anual(pa, falso_desde="2017")
        placebo_fecha = {"coef": mpf.beta, "p": mpf.p_t, "mismo_signo": bool(np.sign(mpf.beta) == np.sign(r["coef"])), "n_tr": pa["n_tr"], "n_co": pa["n_co"]}
        # placebo de resultado: población de 65 o más sin dato; sustituto informativo: renta disponible del IRPF (anual, no es del plan)
        pi = E.panel_anual(d, "irpf", ANIOS_IRPF, ["2021"])
        sust = None
        if pi["n_tr"] >= 10 and pi["n_co"] >= 10:
            mi = E.twfe_anual(pi)
            sust = {"coef": mi.beta, "p": mi.p_t, "n_tr": pi["n_tr"], "n_co": pi["n_co"]}
        else:
            sust = {"n_tr": pi["n_tr"], "n_co": pi["n_co"], "nota": "la renta IRPF municipal del repositorio solo cubre la C. Valenciana: sin municipios catalanes, no realizable"}
        # reversión tras la STC 37/2022 (2022T2-2023T4)
        per20 = K.trimestres("2019T1", "2023T4")
        p20 = DS.panel_r1(d, resultado, per=per20)
        N20, T20 = p20["Y"].shape
        rev = np.zeros(T20)
        rev[13:] = 1
        trf = p20["tr"].astype(float)
        postv = np.zeros(T20)
        postv[E.POST_COLS] = 1
        antv = np.zeros(T20)
        antv[E.ANT_COL] = 1
        m_post = E.twfe_panel(p20["Y"], p20["tr"], E.POST_COLS, (E.ANT_COL,), extras=[trf[:, None] * rev[None, :]])
        unit = np.repeat(np.arange(N20), T20)
        time_ = np.tile(np.arange(T20), N20)
        m_rev = K.Modelo(p20["Y"].ravel(), (trf[:, None] * rev[None, :]).ravel(), unit, time_,
                         extra=np.column_stack([(trf[:, None] * postv[None, :]).ravel(), (trf[:, None] * antv[None, :]).ravel()]), cluster=unit)
        reversion = {"coef_post": m_post.beta, "coef_reversion": m_rev.beta, "se_reversion": m_rev.se, "p_reversion": m_rev.p_t, "n_tr": p20["n_tr"],
                     "n_co": p20["n_co"],
                     "persiste": bool(np.sign(m_rev.beta) == np.sign(m_post.beta) and m_rev.p_t < 0.05 and abs(m_rev.beta) >= 0.5 * abs(m_post.beta))}
        # Honest DiD
        hon = E.honest_trimestral(q["Y"], q["tr"])
        diag[ident] = {"evento": ev, "placebo_fecha": placebo_fecha, "placebo_resultado_sustituto": sust, "reversion": reversion, "honest": hon,
                       "aleat": al, "aleat_conglom": al_c, "dk": dk, "moran": moran, "m": m, "q": q, "r": r, "f": f}
        es_tab = ev["tabla"].assign(spec=ident) if es_tab is None else pd.concat([es_tab, ev["tabla"].assign(spec=ident)])
        filas.append(f)
        fam_p[ident] = f["p_i7"]
        # ---------------- variantes
        vs = VARIANTES[ident]
        for suf, dim, desc in vs:
            idv = f"{ident}-{suf}"
            fv = fila_base(idv, "variante", fam, rep, res, "estimada", f"[{dim}] {desc}")
            if ident == "E2-R1c" and suf == "v1":
                fv.update({"estado": "NO ESTIMABLE", "clase": "NO ESTIMABLE",
                           "nota": f"[{dim}] {desc}: los hogares en alquiler del Censo 2021 por municipio no tienen entrada en docs/v18/sellado_v18.json (añadir a src/v18/f3_sellado.py); "
                                   "sin ese contraste no se puede descartar el desvío a la temporada o a no depositar la fianza (adenda, AD-E2 medida)"})
                filas.append(fv)
                continue
            if ident == "E2-R1" and suf == "v5":
                fv.update({"estado": "coincide con la principal", "nota": f"[{dim}] {desc}: la principal ya va sin covariables (el paro registrado de 2020 no está en la base: "
                                                                          "interpolarlo solo es robustez, holgura E2-R1-h1)", "coef": f["coef"], "p_webb": f["p_webb"], "p_cr1": f["p_cr1"],
                           "ic95_lo": f["ic95_lo"], "ic95_hi": f["ic95_hi"]})
                filas.append(fv)
                continue
            if ident == "E2-R1" and suf in ("v8", "v9"):
                pv = E.panel_anual(d, "rA" if suf == "v8" else "serpavi", ANIOS_V8 if suf == "v8" else ANIOS_V9, ["2021"])
                mv = E.twfe_anual(pv)
                rv = E.inferir(mv, B_VAR, B_IC, ic=False)
                fv = rellena(fv, rv, pv)
                if suf == "v8":
                    ha = E.honest_anual(pv, ["2014", "2015", "2016", "2017", "2018"], "2019", ["2021"])
                    diag[ident]["honest_anual_v8"] = ha
            elif ident == "E2-R1c" and suf == "v2":
                pv = DS.panel_r1(d, resultado)
                rv = E.ppml(d, pv)
                fv = rellena(fv, rv | {"p_webb": None, "p_webb_i7": None}, pv)
            else:
                rv, pv = variante_trim(d, ident, suf, resultado, False, K.SEMILLA)
                fv = rellena(fv, rv, pv)
            filas.append(fv)
        if ident == "E2-R1":
            for hid, padre, desc in HOLGURA:
                rv, pv = variante_trim(d, ident, "h1", resultado, False, K.SEMILLA)
                fv = rellena(fila_base(hid, "holgura", fam, rep, res, "estimada", desc), rv, pv)
                filas.append(fv)
    # ================================================================ coprincipales P (V9-D1b, CS nunca tratados)
    for ident, resultado in (("E2-P-D1b", "renta"), ("E2-P-D1b-c", "contratos")):
        if "E2-R1" not in estimables:
            continue
        rol, fam, rep, res, *_ = SPECS[ident]
        pp = E.panel_d1b(d, resultado)
        r = E.cs_p(pp, B_P, B_IC)
        f = fila_base(ident, rol, fam, rep, res, "estimada")
        f.update({"n_tratados": pp["n_tr"], "n_controles": pp["n_co"], "n_obs": r["n_obs"], "G": r["G"], "coef": r["coef"], "se_cr1": r["se"], "p_webb": r["p_webb"],
                  "p_i7": r["p_webb_i7"], "ic95_lo": r["ic_webb"][0], "ic95_hi": r["ic_webb"][1], "tipo_ic": "inversión del Webb CS (WCR-t, nulo impuesto)", "clase": "no se clasifica"})
        v9 = pd.read_csv(K.RAIZ / "output" / "v9" / "d1" / "tabla_d1.csv")
        v9 = v9[(v9.diseno == "D1b") & (v9.especificacion == "CS nunca tratados (principal)") &
                (v9.resultado == ("log renta media de contratos nuevos" if resultado == "renta" else "log contratos nuevos"))].iloc[0]
        f["nota"] = (f"cifra publicada V9-D1b: {v9.beta:.4f} (IC95 {v9.ic95_lo:.4f}; {v9.ic95_hi:.4f}; {int(v9.tratadas)} tratadas y {int(v9.controles)} controles); "
                     "la P se estima en la muestra V18 (sin unidades selladas de V15 y V16)")
        filas.append(f)
        fam_p[ident] = f["p_i7"]
        diag[ident] = {"v9": v9.to_dict(), "r": r, "panel": {"n_tr": pp["n_tr"], "n_co": pp["n_co"]}}

    # ================================================================ Holm (familia E2: especificaciones estimables) y BY por identificador
    holm = K.holm_familia({k: v for k, v in fam_p.items() if v is not None and np.isfinite(v)})
    tab = pd.DataFrame(filas)
    for k, v in holm.items():
        tab.loc[tab.id == k, "p_holm"] = v
    for ident in ("E2-R1", "E2-R1c"):
        if ident not in estimables:
            continue
        vv = tab[(tab.rol == "variante") & tab.id.str.startswith(ident + "-") & tab.p_webb.notna() & (tab.estado == "estimada")]
        if len(vv):
            q_by = multipletests(vv.p_webb.values, alpha=0.10, method="fdr_by")[1]
            tab.loc[vv.index, "q_by"] = q_by

    # ================================================================ clasificación
    clasif = {}
    for ident in estimables:
        di = diag[ident]
        r, f = di["r"], di["f"]
        ref = DS.ESPEC[ident]
        ph = float(tab.loc[tab.id == ident, "p_holm"].iloc[0])
        vv = tab[(tab.rol == "variante") & tab.id.str.startswith(ident + "-") & (tab.estado == "estimada")]
        signo = np.sign(r["coef"])
        mismo = (np.sign(vv.coef) == signo)
        b4 = vv[vv.id.isin([f"{ident}-v2", f"{ident}-v4", f"{ident}-v9", f"{ident}-v11"])]
        ic0 = (r["ic_cr1"][0], r["ic_cr1"][1])
        solape = bool(((vv.ic95_lo <= ic0[1]) & (vv.ic95_hi >= ic0[0])).all())
        robustez = {"frac_mismo_signo": float(mismo.mean()) if len(vv) else None, "n_variantes": int(len(vv)),
                    "cambio_signo": bool((np.sign(b4.coef) != signo).any()) if len(b4) else False, "solape_ic": solape}
        topes = []
        if ident == "E2-R1":
            topes.append("tope SUGESTIVO por corrección de un fallo conocido de V9-D1b: grupo de control y ventana (adenda 1.6; Honest M̄ de ruptura 0,5)")
            if di["reversion"]["persiste"]:
                topes.append("reversión: la diferencia persiste en 2022T2-2023T4 (adenda, AD-E2-R1)")
            r1c = diag.get("E2-R1c")
            if r1c is not None:
                rc = r1c["r"]
                if rc["coef"] <= -0.05 and rc["p_cr1"] < 0.05:
                    topes.append("contratos por 1.000 habitantes caen ≥ 5 % con significación al 5 %: no se descarta el desvío a la temporada o a no depositar la fianza (AD-E2)")
        ev = di["evento"]
        umbral_sesgo = 0.5 * ref["ref"] if ref["ref"] else ref["delta"]
        info = {"estimable": True, "coprincipal": False, "p_holm": ph, "coef": r["coef"], "pretend_p": ev["p_pretend"],
                "roth_ok": bool(ev["sesgo_post"] < umbral_sesgo), "placebo_fecha": di["placebo_fecha"], "placebo_resultado": "no disponible", "robustez": robustez,
                "inferencia_banda": K.banda_mc(E.TAM_WEBB_MUN), "topes": topes,
                "tost": K.tost(r["coef"], r["se"], ref["delta"], di["m"].G - 1)}
        c = K.clasificar(info)
        clasif[ident] = {"info": info, "clase": c}
        tab.loc[tab.id == ident, "clase"] = c["clase"]
    for ident in ("E2-P-D1b", "E2-P-D1b-c"):
        if ident in diag:
            tab.loc[tab.id == ident, "clase"] = "no se clasifica"
    tab.to_csv(OUT / "tabla.csv", index=False, float_format="%.6f")
    if es_tab is not None:
        es_tab.to_csv(OUT / "estudio_eventos.csv", index=False, float_format="%.6f")
    reg_post(reg, tab)
    from e2_salidas import escribir
    escribir(OUT, d, est, tab, diag, clasif, time.time() - t0)
    print(f"E2 hecho en {time.time() - t0:.0f} s", flush=True)
    return 0


def reg_post(reg, tab: pd.DataFrame) -> None:
    for r in tab.itertuples():
        if r.estado.startswith("estimada") or r.estado.startswith("coincide"):
            reg.log("v18-E2-estimada", r.id, r.resultado, "", "", int(r.n_obs) if r.n_obs == r.n_obs and r.n_obs is not None else 0, np.nan, np.nan, np.nan,
                    coef_interes=r.coef if r.coef is not None else np.nan, p_interes=r.p_webb if r.p_webb is not None else np.nan, notas=f"{r.rol}; clase {r.clase}")
        else:
            reg.log("v18-E2-no-estimada", r.id, r.resultado, "", "", 0, np.nan, np.nan, np.nan, notas=r.estado)
    reg.flush()


if __name__ == "__main__":
    sys.exit(main())
