"""V15-F1.3 · Potencia por pregunta candidata → output/v15/potencia/. Determinista (SEED=20261010); sin red; solo lee la base.

Ningún efecto se estima aquí. Para cada pregunta candidata del plan (P1-P10) se toma el panel de resultado que usaría el diseño y se
mide el efecto mínimo detectable al 80 % (contraste bilateral al 5 %) por aleatorización placebo:
- el «tratamiento» se genera al azar, independiente del resultado (DiD: unidades y fechas al azar con el número de tratadas y el
  calendario reales; exposición continua: proceso AR(1) con un componente común por grupo territorial, para imitar la correlación
  espacial de las exposiciones de tipo shift-share);
- se estima el coeficiente placebo con efectos fijos de unidad y periodo (proyecciones alternadas: vale para paneles desequilibrados);
- MDE80 = 2,8 × desviación típica de los coeficientes placebo (≈ (z0,975 + z0,80) × error típico);
- se anota también la tasa de rechazo al 5 % con errores agrupados por grupo territorial: si se aleja del 5 %, la inferencia con esos
  clusters no es fiable (pocos clusters).
En los diseños de regulación (P6) se usan SOLO periodos anteriores a la regulación (adopción placebo con el mismo número de periodos
posteriores que tendrá el diseño): así no se mira ningún resultado posterior al tratamiento real.
P2 (cointegración) no tiene MDE en este sentido: su potencia se valida por Monte Carlo tras la puerta (agente montecarlo).
P8 usa los errores típicos ya publicados de output/v12/b6 (ECV); P9, simulación del contraste DM frente al AR(4).
Los umbrales de referencia (columna «referencia») salen de estimaciones previas del repositorio cuando existen; si no, se deja para la
fase 2 (literatura) y el veredicto es provisional.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "output" / "v15" / "potencia"
SEED = 20261010
REPS = 500
HECHOS = RAIZ / "data/base/hechos.parquet"
FILTRO = "NOT coalesce(muestra_sellada_v6, false)"


def q(sql: str) -> pd.DataFrame:
    con = duckdb.connect()
    con.execute("SET threads TO 4")
    return con.execute(sql.replace("{H}", f"read_parquet('{HECHOS}')").replace("{F}", FILTRO)).df()


def panel(variable: str, nivel: str, frecuencia: str, desag: str = "", donde: str = "TRUE", min_t: int = 0) -> pd.DataFrame:
    d = q(f"""SELECT territorio_codigo AS u, periodo AS t, valor FROM {{H}}
              WHERE {{F}} AND variable='{variable}' AND nivel='{nivel}' AND frecuencia='{frecuencia}'
                AND coalesce(desagregacion,'')='{desag}' AND valor > 0 AND {donde}""")
    d["y"] = np.log(d.valor)
    if min_t:
        n = d.groupby("u").t.transform("count")
        d = d[n >= min_t]
    return d.reset_index(drop=True)


class FE2:
    """Proyección sobre efectos fijos de unidad y periodo por proyecciones alternadas (panel desequilibrado)."""

    def __init__(self, u: pd.Series, t: pd.Series, it: int = 40):
        self.iu, self.u = pd.factorize(u)
        self.itt, self.t = pd.factorize(t)
        self.nu = np.bincount(self.iu)
        self.nt = np.bincount(self.itt)
        self.it = it

    def __call__(self, v: np.ndarray) -> np.ndarray:
        v = np.asarray(v, float).copy()
        for _ in range(self.it):
            v -= (np.bincount(self.iu, v) / self.nu)[self.iu]
            v -= (np.bincount(self.itt, v) / self.nt)[self.itt]
        return v


def _coef(yr: np.ndarray, xr: np.ndarray, g: np.ndarray) -> tuple[float, float]:
    b = (xr @ yr) / (xr @ xr)
    e = yr - b * xr
    s = np.bincount(g, xr * e)
    G = len(s)
    se = np.sqrt(G / max(G - 1, 1) * (s @ s)) / (xr @ xr)
    return b, se


def placebo_did(p: pd.DataFrame, n_trat: int, adopciones: list[str], grupo: pd.Series, rng) -> dict:
    fe = FE2(p.u, p.t)
    yr = fe(p.y.values)
    g = pd.factorize(grupo)[0]
    unidades = fe.u
    orden = {t: k for k, t in enumerate(sorted(fe.t))}
    tk = p.t.map(orden).values
    bs, rech = [], 0
    for _ in range(REPS):
        trat = rng.choice(len(unidades), size=min(n_trat, len(unidades) - 1), replace=False)
        adop = np.full(len(unidades), 10**6)
        adop[trat] = [orden[a] for a in rng.choice(adopciones, size=len(trat))]
        d = (tk >= adop[fe.iu]).astype(float)
        b, se = _coef(yr, fe(d), g)
        bs.append(b)
        rech += abs(b / se) > 1.96
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": rech / REPS}


def placebo_continuo(p: pd.DataFrame, grupo: pd.Series, rng, rho: float = 0.8, comun: float = 0.5) -> dict:
    fe = FE2(p.u, p.t)
    yr = fe(p.y.values)
    g = pd.factorize(grupo)[0]
    gu = pd.Series(g).groupby(fe.iu).first().reindex(range(len(fe.u))).values
    orden = {t: k for k, t in enumerate(sorted(fe.t))}
    tk = p.t.map(orden).values
    T, N, G = len(orden), len(fe.u), g.max() + 1
    bs, rech = [], 0
    for _ in range(REPS):
        eg = rng.standard_normal((G, T))
        eu = rng.standard_normal((N, T))
        sh = np.sqrt(comun) * eg[gu] + np.sqrt(1 - comun) * eu
        x = np.empty_like(sh)
        x[:, 0] = sh[:, 0]
        for k in range(1, T):   # AR(1) con varianza estacionaria 1
            x[:, k] = rho * x[:, k - 1] + np.sqrt(1 - rho**2) * sh[:, k]
        xv = x[fe.iu, tk]
        xr = fe(xv)
        b, se = _coef(yr, xr / xv.std(), g)
        bs.append(b)
        rech += abs(b / se) > 1.96
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": rech / REPS}


def placebo_seccion(dy: pd.Series, grupo: pd.Series, rng, comun: float = 0.5) -> dict:
    """Corte transversal (diferencia larga del log) sobre una covariable placebo con componente común por grupo."""
    y = dy.values - dy.values.mean()
    g = pd.factorize(grupo)[0]
    G = g.max() + 1
    bs, rech = [], 0
    for _ in range(REPS):
        x = np.sqrt(comun) * rng.standard_normal(G)[g] + np.sqrt(1 - comun) * rng.standard_normal(len(y))
        x = (x - x.mean()) / x.std()
        b, se = _coef(y, x, g)
        bs.append(b)
        rech += abs(b / se) > 1.96
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": rech / REPS}


def placebo_lp(y: pd.Series, h: int, rng, lags: int = 4) -> dict:
    """Proyección local de y_{t+h} − y_{t−1} sobre un choque placebo iid N(0,1) con 4 retardos de Δy (serie trimestral)."""
    v = y.values
    dy = np.diff(v, prepend=np.nan)
    filas = range(lags + 1, len(v) - h)
    Y = np.array([v[t + h] - v[t - 1] for t in filas])
    L = np.array([[dy[t - k] for k in range(1, lags + 1)] for t in filas])
    bs = []
    for _ in range(REPS):
        s = rng.standard_normal(len(v))[list(filas)]
        X = np.column_stack([np.ones(len(Y)), s, L])
        bs.append(np.linalg.lstsq(X, Y, rcond=None)[0][1])
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": np.nan, "T": len(Y)}


def ar4_errores(y: pd.Series, inicio: int) -> np.ndarray:
    dy = np.diff(y.values)
    e = []
    for t in range(inicio, len(dy)):
        Y = dy[4:t]
        X = np.column_stack([np.ones(len(Y))] + [dy[4 - k:t - k] for k in range(1, 5)])
        b = np.linalg.lstsq(X, Y, rcond=None)[0]
        e.append(dy[t] - np.r_[1, dy[t - 1:t - 5:-1]] @ b)
    return np.array(e)


def mde_dm(e: np.ndarray, rng, rho: float) -> float:
    """Menor reducción relativa del ECM de un competidor que el DM (HLN, h=1, unilateral 5 %) detecta con potencia 0,8."""
    from scipy import stats
    n = len(e)
    for r in np.arange(0.02, 0.81, 0.02):
        rech = 0
        for _ in range(300):
            k = rng.integers(0, n - 4, size=n // 4 + 1)
            eb = np.concatenate([e[i:i + 4] for i in k])[:n]
            z = rng.standard_normal(n) * eb.std()
            c = np.sqrt((1 - r) * np.mean(eb**2) / np.mean((rho * eb + np.sqrt(1 - rho**2) * z) ** 2))
            e2 = c * (rho * eb + np.sqrt(1 - rho**2) * z)
            d = eb**2 - e2**2
            dm = d.mean() / (d.std(ddof=1) / np.sqrt(n)) * np.sqrt((n - 1) / n)
            rech += dm > stats.t.ppf(0.95, n - 1)
        if rech / 300 >= 0.8:
            return float(r)
    return float("nan")


def incasol_trimestral() -> pd.DataFrame:
    d = q("""SELECT r.territorio_codigo AS u, r.periodo AS t, sum(r.valor*c.valor)/sum(c.valor) AS valor
             FROM {H} r JOIN {H} c USING (territorio_codigo, periodo, desagregacion, frecuencia, nivel)
             WHERE r.variable='incasol_renta_media' AND c.variable='incasol_contratos' AND r.frecuencia='T' AND r.nivel='municipio'
               AND NOT coalesce(r.muestra_sellada_v6,false) AND r.valor>0 AND c.valor>0
             GROUP BY 1,2""")
    d["y"] = np.log(d.valor)
    return d


def main() -> int:
    rng = np.random.default_rng(SEED)
    SAL.mkdir(parents=True, exist_ok=True)
    F = []

    def fila(preg, diseno, datos, nivel, p_or_n, clusters, T, res, unidad, referencia, nota, tratadas=""):
        mde = 2.8 * res["sd_placebo"]
        F.append({"pregunta": preg, "diseno": diseno, "datos": datos, "nivel": nivel, "n_unidades": p_or_n, "clusters": clusters,
                  "T": T, "tratadas": tratadas, "sd_placebo": round(res["sd_placebo"], 5), "mde80": round(mde, 4), "unidad_mde": unidad,
                  "tamano_5pct_cluster": res.get("tamano_5pct"), "referencia": referencia, "nota": nota})

    zt = q("""SELECT territorio_codigo AS u, min(periodo) AS adop FROM {H} WHERE variable='zt_vigente' AND valor=1 GROUP BY 1""")
    cat = zt[zt.u.str[:2].isin(["08", "17", "25", "43"])]

    # P6 · zonas tensionadas en Cataluña: Incasòl trimestral (contratos nuevos), solo antes de 2024T1; adopción placebo con 9 trimestres posteriores
    inc = incasol_trimestral()
    inc = inc[inc.t < "2024T1"]
    inc = inc[inc.groupby("u").t.transform("count") >= 16]
    n_trat = int(cat.u.isin(inc.u).sum())
    res = placebo_did(inc, n_trat, ["2021T4"], inc.u.str[:2], rng)
    fila("P6", "DiD placebo (adopción 2021T4, 9 trimestres posteriores), EF municipio y trimestre", "incasol renta media ponderada por contratos",
         "municipio (Cataluña)", inc.u.nunique(), "4 provincias / municipios", inc.t.nunique(), res, "log puntos",
         "0,059 (V9-D1b, −5,9 %, contratos nuevos)", "Solo periodos anteriores a la ZT. Con 4 provincias, los errores agrupados por provincia no sirven: agrupar por municipio.", n_trat)
    res = placebo_did(inc, n_trat, ["2021T4"], inc.u, rng)
    fila("P6", "Igual, errores agrupados por municipio", "incasol", "municipio (Cataluña)", inc.u.nunique(), inc.u.nunique(), inc.t.nunique(), res,
         "log puntos", "0,059 (V9-D1b)", "", n_trat)
    # P6 · SERPAVI anual nacional: la base acaba en 2024 → 1 año posterior
    sp = panel("serpavi_alquiler_m2_mediana", "municipio", "A", "tipologia=VC", "periodo < '2024'", min_t=8)
    n_trat = int(zt.u.isin(sp.u).sum())
    res = placebo_did(sp, n_trat, ["2023"], sp.u.str[:2], rng)
    fila("P6", "DiD placebo (1 año posterior: SERPAVI acaba en 2024)", "serpavi €/m² mediana, colectiva", "municipio (España)", sp.u.nunique(),
         "50 provincias", sp.t.nunique(), res, "log puntos", "0,059 (V9-D1b)", "Mide stock de contratos declarados, no contratos nuevos: diluye el efecto.", n_trat)

    # P4 · inmigración: (a) municipal 2021-2024 (padrón por nacionalidad solo desde 2021); (b) València por sección 2011-2024, grupo distrito
    spm = panel("serpavi_alquiler_m2_mediana", "municipio", "A", "tipologia=VC", min_t=0)
    a = spm[spm.t >= "2021"]
    a = a[a.groupby("u").t.transform("count") == 4]
    res = placebo_continuo(a, a.u.str[:2], rng)
    fila("P4", "Exposición continua placebo (shift-share), EF municipio y año", "serpavi €/m² VC", "municipio", a.u.nunique(), "50 provincias",
         4, res, "log puntos por 1 DT de exposición", "pendiente fase 2", "T = 4: la exposición por nacionalidad municipal solo existe 2021-2025.")
    b = spm[spm.t <= "2022"]   # padrón municipal por nacionalidad 2003-2022 (auditoría de demografía): solape con SERPAVI 2011-2022
    b = b[b.groupby("u").t.transform("count") >= 8]
    res = placebo_continuo(b, b.u.str[:2], rng)
    fila("P4", "Exposición continua placebo (shift-share con padrón 2003-2022), EF municipio y año", "serpavi €/m² VC", "municipio", b.u.nunique(),
         "50 provincias", b.t.nunique(), res, "log puntos por 1 DT de exposición", "pendiente fase 2",
         "Padrón por nacionalidad (28 países) 2003-2022 para toda España; SERPAVI desde 2011.")
    vs = panel("serpavi_alquiler_m2_mediana", "seccion", "A", "tipologia=VC", "territorio_codigo LIKE '46250%'", min_t=10)
    res = placebo_continuo(vs, vs.u.str[5:7], rng)
    fila("P4", "Exposición continua placebo por barrio (shift-share), EF sección y año", "serpavi €/m² VC", "sección (València)", vs.u.nunique(),
         f"{vs.u.str[5:7].nunique()} distritos", vs.t.nunique(), res, "log puntos por 1 DT", "pendiente fase 2",
         "Clusters efectivos = distritos (19) o barrios (87); el shift-share tiene además tantos clusters como orígenes (AKM).")

    # P5 · pisos turísticos: Barcelona por sección (grupo distrito) y Comunitat Valenciana por municipio
    bs = panel("serpavi_alquiler_m2_mediana", "seccion", "A", "tipologia=VC", "territorio_codigo LIKE '08019%'", min_t=10)
    res = placebo_continuo(bs, bs.u.str[5:7], rng)
    fila("P5", "Exposición continua placebo (densidad HUT), EF sección y año", "serpavi €/m² VC", "sección (Barcelona)", bs.u.nunique(),
         f"{bs.u.str[5:7].nunique()} distritos", bs.t.nunique(), res, "log puntos por 1 DT", "pendiente fase 2",
         "La exposición HUT es por barrio (73): agrupar por barrio; con 10 distritos, la tasa de rechazo indica si sirve.")
    cv = spm[spm.u.str[:2].isin(["03", "12", "46"]) & (spm.t >= "2015")]
    cv = cv[cv.groupby("u").t.transform("count") >= 8]
    res = placebo_continuo(cv, cv.u, rng)
    fila("P5", "Exposición continua placebo (registro GVA reconstruido), EF municipio y año", "serpavi €/m² VC", "municipio (C. Valenciana)",
         cv.u.nunique(), cv.u.nunique(), cv.t.nunique(), res, "log puntos por 1 DT", "pendiente fase 2",
         "El registro reconstruido es un supuesto de fechado (C4): solo robustez, nunca exposición principal.")

    # P7 · presión demográfica frente a obra nueva: municipal 2021-2024 (igual panel que P4a)
    res = placebo_continuo(a, a.u.str[:2], rng, rho=0.5)
    fila("P7", "Exposición continua placebo (hogares − obra), EF municipio y año", "serpavi €/m² VC", "municipio", a.u.nunique(), "50 provincias", 4,
         res, "log puntos por 1 DT", "pendiente fase 2", "T = 4; la población municipal anual por censo solo existe 2021-2025.")

    # P10 · espacial: corte municipal de la diferencia larga 2015-2024
    w = spm.pivot_table(index="u", columns="t", values="y")
    if "2015" in w and "2024" in w:
        dl = (w["2024"] - w["2015"]).dropna()
        res = placebo_seccion(dl, dl.index.str[:2], rng)
        fila("P10", "Corte transversal placebo con componente provincial (Conley ≈ agrupado provincial)", "serpavi €/m² VC, Δlog 2015-2024",
             "municipio", len(dl), "50 provincias", 1, res, "log puntos por 1 DT", "pendiente fase 2",
             "Los efectos indirectos (SAR/SDM) dependen de W: su potencia se valida por Monte Carlo tras la puerta.")

    # P1 · oferta: corte provincial (valor tasado, Δlog 2013-2024) frente a un índice de restricciones placebo
    vt = panel("valor_tasado", "provincia", "A", "")
    w = vt.pivot_table(index="u", columns="t", values="y")
    dl = (w["2024"] - w["2013"]).dropna()
    res = placebo_seccion(dl, pd.Series(dl.index, index=dl.index), rng, comun=0.0)
    fila("P1", "Corte transversal placebo (índice de restricciones físicas)", "valor tasado, Δlog 2013-2024", "provincia", len(dl), len(dl), 1,
         res, "log puntos por 1 DT", "pendiente fase 2",
         "Las restricciones físicas (pendiente, agua, suelo protegido) no están en el repositorio; a escala municipal no hay precio de compra en la base.")

    # P3 · tipos: proyección local nacional (valor tasado 1995-2026 e IPV 2007-2026), h = 4 y 8
    for var, nombre in (("p_tasado", "valor tasado"), ("ipv", "IPV")):
        s = q(f"SELECT periodo, valor FROM {{H}} WHERE {{F}} AND variable='{var}' AND nivel='nacional' AND frecuencia='T' ORDER BY periodo")
        y = np.log(s.set_index("periodo").valor)
        for h in (4, 8):
            res = placebo_lp(y, h, rng)
            fila("P3", f"Proyección local placebo, h = {h}", f"{nombre} nacional, log", "nacional", 1, "1 (serie temporal)", res["T"], res,
                 "log puntos por 1 DT de sorpresa", "pendiente fase 2",
                 "Sin exposición provincial a hipoteca variable en el repositorio: el diseño queda en serie temporal (o 21 países del BCE).")

    # P9 · predicción: DM frente al AR(4) en Δlog valor tasado nacional, errores recursivos desde 2008
    s = q("SELECT periodo, valor FROM {H} WHERE {F} AND variable='p_tasado' AND nivel='nacional' AND frecuencia='T' ORDER BY periodo")
    y = np.log(s.set_index("periodo").valor)
    e = ar4_errores(y, inicio=int(np.where(y.index == "2008T1")[0][0]))
    for rho in (0.9, 0.7):
        r = mde_dm(e, rng, rho)
        F.append({"pregunta": "P9", "diseno": f"DM (HLN, h=1) frente a AR(4), correlación de errores {rho}", "datos": "valor tasado nacional, Δlog",
                  "nivel": "nacional", "n_unidades": 1, "clusters": "", "T": len(e), "tratadas": "", "sd_placebo": np.nan, "mde80": r,
                  "unidad_mde": "reducción relativa del ECM", "tamano_5pct_cluster": np.nan, "referencia": "ningún modelo bate al AR(4) (v1, K1, V8)",
                  "nota": "Con la muestra sellada de V15 (datos posteriores al depósito), T será mucho menor: la potencia real será más baja."})

    # P8 · distribución: brecha de sobrecarga entre origen español y extranjero, cambio 2018→2025, con los errores publicados de V12-B6
    ecv = pd.read_csv(RAIZ / "output/v12/b6/ecv_anual_origen.csv")
    for ind in ("sobrecarga_30", "esfuerzo_alquiler_30", "propiedad"):
        e_ = ecv[(ecv.grupo == "origen") & ecv.categoria.isin(["española", "fuera de la UE"]) & (ecv.indicador == ind)
                 & ecv.anio.isin([2018, 2025]) & ecv.publicable]
        if len(e_) < 4:
            continue
        se = (e_.ic95_sup - e_.ic95_inf) / (2 * 1.96)
        sd = float(np.sqrt((se**2).sum()))
        F.append({"pregunta": "P8", "diseno": "Cambio de la brecha entre orígenes, 2018-2025 (diferencia de diferencias de proporciones)",
                  "datos": f"ECV microdatos, {ind}", "nivel": "nacional (personas)", "n_unidades": int(e_.n_muestral.sum()), "clusters": "",
                  "T": 2, "tratadas": "", "sd_placebo": round(sd / 100, 5), "mde80": round(2.8 * sd, 2), "unidad_mde": "puntos porcentuales",
                  "tamano_5pct_cluster": np.nan, "referencia": "pendiente fase 2",
                  "nota": f"Celdas: {', '.join(sorted(e_.categoria.unique()))}. Errores de diseño publicados en output/v12/b6."})

    t = pd.DataFrame(F)
    t["tamano_5pct_cluster"] = pd.to_numeric(t.tamano_5pct_cluster).round(3)
    t.to_csv(SAL / "potencia.csv", index=False)
    (SAL / "resultado.json").write_text(json.dumps({
        "rama": "v15-f1-potencia", "pregunta": "Efecto mínimo detectable al 80 % por pregunta candidata (P1-P10)", "capa": "C4",
        "datos": "data/base/hechos.parquet (sin la muestra sellada de v6); output/v12/b6/ecv_anual_origen.csv", "N": int(len(t)),
        "metodo": f"aleatorización placebo, {REPS} réplicas, SEED={SEED}; MDE80 = 2,8 × DT placebo; DM por simulación con bloques de 4",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"tamano_5pct_cluster": "tasa de rechazo placebo con errores agrupados (debería ser ≈ 0,05)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Ningún efecto estimado: tratamientos y exposiciones placebo independientes del resultado; P6 solo con periodos previos a la regulación."},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(t[["pregunta", "nivel", "n_unidades", "T", "mde80", "unidad_mde", "tamano_5pct_cluster"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
