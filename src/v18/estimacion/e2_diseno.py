"""V18 · E2 · topes al alquiler · diseño: paneles, mínimos de datos y MDE de cada especificación principal o coprincipal (adenda 1.3).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan_replicacion.md §1.2 + adenda §1.3, §1.6, §1.7, §1.11, §1.12, anexos A-C).
Orden (adenda 1.3): (1) mínimos de datos y MDE de cada especificación principal o coprincipal ANTES de mirar ningún coeficiente
(output/v18/estimacion/e2/estimabilidad.csv, y el Registry con la marca «registrada antes de estimar»); (2) estimación solo de lo estimable;
(3) pruebas B4; (4) clasificación; (5) Holm por familia; (6) Registry. Determinista (SEED 20261010), sin red.
Lecturas de datos: solo por _e2e8_comun.leer_hechos / filtrar (sellado.filtrar + holdout.excluir_sellados_v6). Nunca data/sealed.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_datos as D  # noqa: E402
from herramientas.did import CallawaySantAnna  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEED = K.SEMILLA
OUT = K.RAIZ / "output" / "v18" / "estimacion" / "e2"
B_P, B_IC, B_VAR, R_MDE = 9999, 1999, 1999, 2000

# referencia única y δ (anexo B); umbral de estimabilidad: |referencia| o 2δ si no hay referencia (adenda 1.3)
ESPEC = {
    "E2-R1": {"ref": 0.045, "delta": 0.022, "umbral": 0.045, "fuente_ref": "Jofre-Monseny et al. (2023), tabla 2, col. 3: −0,045 (0,006)"},
    "E2-R1c": {"ref": None, "delta": 0.05, "umbral": 0.10, "fuente_ref": "sin referencia en la misma unidad (la de JMS, −0,003, es ≈ 0): 2δ"},
    "E2-A1": {"ref": 0.0298, "delta": 0.015, "umbral": 0.0298, "fuente_ref": "Pérez García (2026): −0,0298 (0,0113)"},
    "E2-A2": {"ref": 0.0298, "delta": 0.015, "umbral": 0.0298, "fuente_ref": "Pérez García (2026)"},
    "E2-A3": {"ref": None, "delta": 0.05, "umbral": 0.10, "fuente_ref": "sin referencia: 2δ"},
    "E2-A4": {"ref": 0.027, "delta": 0.0135, "umbral": 0.027, "fuente_ref": "Jofre-Monseny et al. (2023), vecinos directos, p. 18: −0,027"},
}


def desmedia2(A):
    return A - A.mean(axis=-1, keepdims=True) - A.mean(axis=-2, keepdims=True) + A.mean(axis=(-2, -1), keepdims=True)


# --------------------------------------------------------------------------------------------- paneles
def cargar() -> dict:
    t0 = time.time()
    d = {"ley": D.regulados_ley11()}
    d["rT"], d["cT"] = D.serie_t("incasol_renta_media"), D.serie_t("incasol_contratos")
    d["rA"] = D.anual(K.leer_hechos("incasol_renta_media", "municipio", "A"))
    d["cA"] = D.anual(K.leer_hechos("incasol_contratos", "municipio", "A"))
    d["paro"] = D.anual(K.leer_hechos("sepe_paro_registrado_media_anual", "municipio", "A"))
    d["paro_trim"] = D.paro_trimestral()        # media trimestral del fichero mensual del SEPE (adenda R-1; K9)
    d["hut"] = D.anual(K.leer_hechos("idescat_hut_n", "municipio", "A"))
    sp = K.leer_hechos("serpavi_alquiler_m2_mediana", "municipio", "A")
    d["serpavi"] = D.anual(sp[sp.desagregacion == "tipologia=VC"])
    d["irpf"] = D.anual(K.leer_hechos("aeat_irpf_renta_disponible_media", "municipio", "A"))
    d["pop"] = D.poblacion()
    d["zt"] = K.leer_hechos("zt_vigente", "municipio", "T")
    d["geo"] = D.geografia()
    d["segundos_carga"] = round(time.time() - t0, 1)
    return d


def paro_interp(paro: pd.DataFrame) -> pd.DataFrame:
    """Paro registrado anual con 2020 INTERPOLADO linealmente entre 2019 y 2021. OBSOLETO desde K9 (el fichero mensual del SEPE sí trae 2020 y la
    principal usa el paro trimestral); se conserva solo para 2019, que no se interpola."""
    p = paro.copy()
    p["2020"] = (p["2019"] + p["2021"]) / 2
    return p


def crecimiento_2014_2019(rA: pd.DataFrame) -> pd.Series:
    return (rA["2019"] / rA["2014"]) ** (1 / 5) - 1


def ln_pop_trimestral(pop: pd.DataFrame, cods, periodos) -> np.ndarray:
    ultimo = max(pop.columns)   # el padrón con sellado llega a 2022: en la prueba de reversión (2023) se mantiene la población de 2022
    return np.column_stack([np.log(pop.reindex(cods)[min(p[:4], ultimo)].values) for p in periodos])


def panel_r1(d: dict, resultado: str = "renta", con_barcelona: bool = False, grupo_control: str = "jms", con_paro: bool = False, per: list | None = None) -> dict:
    """Panel trimestral 2019T1-2022T1 (equilibrado: ≥ 1 contrato y renta en cada trimestre). Tratados: Ley 11/2020 (sin Barcelona ciudad salvo
    con_barcelona). Controles: «jms» = no regulados con crecimiento anual de la renta 2014-2019 > 4,15 %; «10km» = no regulados a más de 10 km de un
    regulado con ≥ 5 contratos por trimestre (variante v4)."""
    per = per or D.PER13
    cT, rT, ley = d["cT"], d["rT"], d["ley"]
    ok_c = (cT[per] >= 1).all(axis=1)
    if resultado == "renta":
        ok = ok_c & rT[per].notna().all(axis=1) & (rT[per] > 0).all(axis=1)
    else:
        ok = ok_c & d["pop"].reindex(cT.index)[["2019", "2020", "2021", "2022"]].notna().all(axis=1)
    if con_paro:
        ok = ok & d["paro_trim"].reindex(ok.index)[per].notna().all(axis=1)
    cods = ok[ok].index
    gr = crecimiento_2014_2019(d["rA"])
    quitar = set() if con_barcelona else {D.BARCELONA}
    tr = [c for c in cods if c in ley and c not in quitar]
    if grupo_control == "jms":
        co = [c for c in cods if c not in ley and c != D.BARCELONA and gr.get(c, np.nan) > 0.0415]
    elif grupo_control == "todos":
        co = [c for c in cods if c not in ley and c != D.BARCELONA]
    else:
        geo = d["geo"]
        reg_xy = geo["xy"][[geo["idx"][c] for c in ley if c in geo["idx"]]]
        co = []
        for c in cods:
            if c in ley or c == D.BARCELONA or c not in geo["idx"]:
                continue
            dd = D.dist_min(geo["xy"][[geo["idx"][c]]], reg_xy)[0]
            if dd > 10 and (cT.loc[c, per] >= 5).all():
                co.append(c)
    sel = tr + co
    if resultado == "renta":
        Y = np.log(rT.loc[sel, per].values)
    else:
        Y = np.log(cT.loc[sel, per].values) - ln_pop_trimestral(d["pop"], sel, per) + np.log(1000)
    return {"cod": np.array(sel), "Y": Y, "tr": np.array([c in set(tr) for c in sel]), "cols": per, "n_tr": len(tr), "n_co": len(co)}


# --------------------------------------------------------------------------------------------- MDE
def placebos_twfe(Y: np.ndarray, n_tr: int, post_cols: list[int], R: int, rng: np.random.Generator) -> np.ndarray:
    """β̂ de TWFE (sin covariables) bajo R reasignaciones aleatorias de los n_tr tratados (variación real: número y calendario)."""
    N, T = Y.shape
    yt = desmedia2(Y)
    pm = np.zeros(T)
    pm[post_cols] = 1.0
    out = []
    for b0 in range(0, R, 250):
        b = min(250, R - b0)
        lab = np.zeros((b, N))
        for r in range(b):
            lab[r, rng.choice(N, n_tr, replace=False)] = 1.0
        Dm = lab[:, :, None] * pm[None, None, :]
        Dt = desmedia2(Dm)
        out.append((Dt * yt[None]).sum((1, 2)) / (Dt ** 2).sum((1, 2)))
    return np.concatenate(out)


def fila_estimabilidad(id_, n_tr, n_co, T, minimo, mde, motivo_extra="") -> dict:
    e = ESPEC[id_]
    ok_min = minimo["ok"]
    ok_mde = mde is not None and mde["mde80"] <= e["umbral"]
    estimable = bool(ok_min and ok_mde)
    motivo = []
    if not ok_min:
        motivo.append(minimo["texto"])
    if mde is not None and not ok_mde:
        motivo.append(f"MDE80 = {mde['mde80']:.4f} > umbral {e['umbral']:.4f}")
    if motivo_extra:
        motivo.append(motivo_extra)
    return {"id": id_, "n_tratados": n_tr, "n_controles": n_co, "T": T, "minimo_datos": minimo["texto"], "minimo_ok": ok_min,
            "mde80": None if mde is None else mde["mde80"], "sd_placebo": None if mde is None else mde["sd_placebo"],
            "umbral": e["umbral"], "referencia": e["fuente_ref"], "estimable": estimable,
            "motivo_no_estimable": "; ".join(motivo) if not estimable else ""}


def cohortes_zt(d: dict) -> pd.Series:
    """Primer trimestre con zona tensionada vigente por municipio (hecho normativo, zt_vigente de la base)."""
    z = d["zt"]
    z = z[z.valor == 1]
    return z.groupby("territorio_codigo").periodo.min()


def panel_a1(d: dict, ini: str = "2022T1", fin: str = "2026T1", sin_barcelona: bool = False) -> dict:
    """Panel trimestral de Cataluña 2022T1-2026T1 (equilibrado: renta y ≥ 1 contrato cada trimestre); cohortes 2024T1 (efecto desde 2024T2) y 2024T4."""
    per = K.trimestres(ini, fin)
    ok = (d["cT"][per] >= 1).all(axis=1) & d["rT"][per].notna().all(axis=1) & (d["rT"][per] > 0).all(axis=1)
    cods = [c for c in ok[ok].index if c[:2] in D.CAT and not (sin_barcelona and c == D.BARCELONA)]
    z = cohortes_zt(d)
    g = np.full(len(cods), -1)
    for i, c in enumerate(cods):
        if c in z.index and z[c] in ("2024T1", "2024T4"):
            g[i] = per.index("2024T2") if z[c] == "2024T1" else per.index("2024T4")
        elif c in z.index:
            g[i] = -2        # cohorte distinta (fuera del diseño): se excluye
    keep = g != -2
    cods = [c for c, k in zip(cods, keep) if k]
    g = g[keep]
    Y = np.log(d["rT"].loc[cods, per].values)
    return {"cod": np.array(cods), "Y": Y, "g": g, "cols": per, "n_tr": int((g >= 0).sum()), "n_co": int((g < 0).sum())}


def placebos_cs(Y: np.ndarray, g: np.ndarray, R: int, rng: np.random.Generator) -> np.ndarray:
    T = Y.shape[1]
    cl = np.arange(len(g))
    out = []
    for _ in range(R):
        gp = rng.permutation(g)
        out.append(CallawaySantAnna(gp, cl, T).estimar(Y))
    return np.array(out)


def a2_conteo(d: dict) -> dict:
    """E2-A2: municipios de País Vasco con zona tensionada y renta EMAL no sellados; trimestres posteriores por cohorte (ventana hasta 2025T4)."""
    e = K.leer_hechos("emal_renta_mensual_eur", "municipio", "T")
    emal = set(e.territorio_codigo)
    z = d["zt"][d["zt"].valor == 1].groupby("territorio_codigo").periodo.min()
    vasco = z[z.index.str[:2].isin(["01", "20", "48"])]
    tr = vasco[vasco.index.isin(emal)]
    post = {c: max(0, K.indice_t("2025T4") - K.indice_t(p) + 1) for c, p in tr.items()}
    por_cohorte = pd.Series(post).groupby(tr).max() if len(tr) else pd.Series(dtype=float)
    return {"n_emal_no_sellados": len(emal), "n_tratados": len(tr), "post_por_cohorte": {k: int(v) for k, v in por_cohorte.items()},
            "texto": f"{len(tr)} municipios tratados con EMAL no sellados (mínimo 10) y trimestres posteriores por cohorte {dict(por_cohorte)} (mínimo 3)",
            "ok": len(tr) >= 10 and (len(por_cohorte) > 0 and bool((por_cohorte >= 3).all()))}


def panel_a3(d: dict) -> dict:
    """Compraventas municipales por 1.000 habitantes, anual 2016-2022 (años con los cuatro trimestres), municipios catalanes de MIVAU."""
    t = D.mivau_municipal("mivau_transacciones_municipios.csv", "trans_total")
    t = t[t.territorio_codigo.str[:2].isin(D.CAT)].copy()
    t["anio"] = t.periodo.str[:4]
    cuenta = t.groupby(["territorio_codigo", "anio"]).valor.agg(["sum", "count"]).reset_index()
    cuenta = cuenta[(cuenta["count"] == 4) & cuenta.anio.between("2016", "2022")]
    w = cuenta.pivot(index="territorio_codigo", columns="anio", values="sum").reindex(columns=[str(y) for y in range(2016, 2023)])
    w = w.dropna()
    w = w[(w > 0).all(axis=1)]
    pop = d["pop"].reindex(w.index)[[str(y) for y in range(2016, 2023)]]
    w, pop = w[pop.notna().all(axis=1)], pop[pop.notna().all(axis=1)]
    Y = np.log(w.values) - np.log(pop.values) + np.log(1000)
    tr = np.array([c in d["ley"] for c in w.index])
    return {"cod": np.array(w.index), "Y": Y, "tr": tr, "cols": [str(y) for y in range(2016, 2023)], "n_tr": int(tr.sum()), "n_co": int((~tr).sum())}


def panel_a4(d: dict, variante: str = "base") -> dict:
    """Desbordamiento: no regulados a < 10 km de un regulado («cerca») frente a > 25 km («lejos»). v1: vecinos directos (frontera común) frente
    a > 25 km; v2: 10-25 km frente a > 25 km. Mismo panel trimestral 2019T1-2022T1 equilibrado."""
    per = D.PER13
    ok = (d["cT"][per] >= 1).all(axis=1) & d["rT"][per].notna().all(axis=1) & (d["rT"][per] > 0).all(axis=1)
    geo, ley = d["geo"], d["ley"]
    reg_xy = geo["xy"][[geo["idx"][c] for c in ley if c in geo["idx"]]]
    cods, cerca = [], []
    for c in ok[ok].index:
        if c in ley or c not in geo["idx"]:
            continue
        dd = D.dist_min(geo["xy"][[geo["idx"][c]]], reg_xy)[0]
        if variante == "base":
            tr, co = dd < 10, dd > 25
        elif variante == "v1":
            tr, co = bool(geo["vecinos"][c] & ley), dd > 25
        else:
            tr, co = 10 <= dd <= 25, dd > 25
        if tr or co:
            cods.append(c)
            cerca.append(bool(tr))
    Y = np.log(d["rT"].loc[cods, per].values)
    cerca = np.array(cerca)
    return {"cod": np.array(cods), "Y": Y, "tr": cerca, "cols": per, "n_tr": int(cerca.sum()), "n_co": int((~cerca).sum())}


def estimabilidad(d: dict) -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    filas, paneles = [], {}
    # R1 y R1c: ≥ 30 tratados y ≥ 30 controles, panel equilibrado con ≥ 1 contrato por trimestre
    for id_, res in (("E2-R1", "renta"), ("E2-R1c", "contratos")):
        p = panel_r1(d, res)
        paneles[id_] = p
        mn = {"ok": p["n_tr"] >= 30 and p["n_co"] >= 30, "texto": f"{p['n_tr']} tratados y {p['n_co']} controles (mínimo 30 y 30)"}
        mde = K.mde_desde_placebos(placebos_twfe(p["Y"], p["n_tr"], list(range(7, 13)), R_MDE, rng)) if mn["ok"] else None
        filas.append(fila_estimabilidad(id_, p["n_tr"], p["n_co"], 13, mn, mde,
                                        "σ y dependencia: ya vistas (reasignación placebo sobre el propio panel de entrenamiento; no se usa el coeficiente)"))
    # A1: CS con cohortes de 2024
    p = panel_a1(d)
    paneles["E2-A1"] = p
    mn = {"ok": p["n_tr"] >= 10 and p["n_co"] >= 10, "texto": f"{p['n_tr']} tratados y {p['n_co']} nunca tratados (CS exige controles propios)"}
    mde = K.mde_desde_placebos(placebos_cs(p["Y"], p["g"], R_MDE, rng)) if mn["ok"] else None
    filas.append(fila_estimabilidad("E2-A1", p["n_tr"], p["n_co"], len(p["cols"]), mn, mde))
    # A2: EMAL
    c2 = a2_conteo(d)
    filas.append(fila_estimabilidad("E2-A2", c2["n_tratados"], c2["n_emal_no_sellados"] - c2["n_tratados"], 40, c2, None))
    # A3
    p = panel_a3(d)
    paneles["E2-A3"] = p
    mn = {"ok": p["n_tr"] >= 10 and p["n_co"] >= 10, "texto": f"{p['n_tr']} tratados y {p['n_co']} controles en la serie municipal de MIVAU"}
    mde = K.mde_desde_placebos(placebos_twfe(p["Y"], p["n_tr"], [5, 6], R_MDE, rng)) if mn["ok"] else None
    filas.append(fila_estimabilidad("E2-A3", p["n_tr"], p["n_co"], 7, mn, mde))
    # A4
    p = panel_a4(d)
    paneles["E2-A4"] = p
    mn = {"ok": p["n_tr"] >= 10 and p["n_co"] >= 10, "texto": f"{p['n_tr']} cerca (< 10 km) y {p['n_co']} lejos (> 25 km)"}
    mde = K.mde_desde_placebos(placebos_twfe(p["Y"], p["n_tr"], list(range(7, 13)), R_MDE, rng)) if mn["ok"] else None
    filas.append(fila_estimabilidad("E2-A4", p["n_tr"], p["n_co"], 13, mn, mde))
    return pd.DataFrame(filas), paneles


