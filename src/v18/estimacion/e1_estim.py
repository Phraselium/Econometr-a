"""V18 · fase 4 · E1 · estimación de cada especificación (R1-R4, A1 y la coprincipal P-H3) y sus variantes enumeradas (adenda, anexo A).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. SEED = 20261010. Cada función recibe los paneles de e1_diseno y devuelve un diccionario con
coeficiente, inferencia principal (CR1 con t(G−1) o AR), Webb, Conley, y los diagnósticos propios de la especificación. Nada se elige por su p-valor.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_datos as D  # noqa: E402
import e1_nucleo as N  # noqa: E402

SEMILLA = K.SEMILLA
REF = {"E1-R1": 0.038, "E1-R2": 0.038, "E1-R3": 0.038, "E1-A1": 0.038, "E1-A2": 0.038, "E1-R4": None}
DELTA = {"E1-R1": 0.019, "E1-R2": 0.019, "E1-R3": 0.019, "E1-A1": 0.019, "E1-A2": 0.019, "E1-R4": 0.05}
VENTANA_R = list(range(2018, 2025))
VENTANA_A1 = list(range(2021, 2025))


# ------------------------------------------------------------------------------------------------ muestras
def muestra(P: pd.DataFrame, anios, cols, excl=None, unidad: str = "cod_seccion", cluster: str = "barrio", sin_anios=()) -> pd.DataFrame:
    """Observaciones sección × año de la ventana con todas las columnas requeridas no vacías; u, t y cl codificados 0..n−1 y orden por unidad y año."""
    d = P[P.anio.isin([a for a in anios if a not in sin_anios])].dropna(subset=list(cols)).copy()
    if excl is not None:
        d = d[~d[unidad].isin(set(excl))]
    d = d.sort_values([unidad, "anio"]).reset_index(drop=True)
    d["u"] = pd.factorize(d[unidad])[0]
    d["t"] = pd.factorize(d.anio)[0]
    d["cl"] = pd.factorize(d[cluster])[0]
    return d


def coords_km(d: pd.DataFrame) -> np.ndarray:
    s = d.drop_duplicates("u").sort_values("u")
    return np.column_stack([s.x.values, s.y.values]) / 1000.0


def exposicion_media(d: pd.DataFrame, col: str) -> pd.Series:
    return d.groupby("cod_seccion")[col].mean()


def sin_extremos(d: pd.DataFrame, col: str, q: float = 0.99) -> set:
    e = exposicion_media(d, col)
    return set(e[e > e.quantile(q)].index)


def extra_trend(d: pd.DataFrame, tipo: str) -> np.ndarray | None:
    if tipo == "ninguna":
        return None
    T = N.tendencias(d["barrio"], d["anio"])
    if tipo == "lineal":
        return T
    t2 = (d["anio"].values - d["anio"].mean()) ** 2
    return np.hstack([T, N.dummies(d["barrio"]) * t2[:, None]])


def agregar_barrio(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Panel barrio × año: medias de y y de cada col ponderadas por las viviendas del Censo 2021; u = cl = barrio."""
    a = d.copy()
    for c in ["y", *cols]:
        a[c + "_w"] = a[c] * a.viv
    g = a.groupby(["barrio", "anio"]).agg(viv=("viv", "sum"), x=("x", "mean"), dist_c=("dist_c", "mean"), **{c + "_w": (c + "_w", "sum") for c in ["y", *cols]}).reset_index()
    for c in ["y", *cols]:
        g[c] = g[c + "_w"] / g.viv
    g["w"] = g.viv
    g["cod_seccion"] = g.barrio
    g = g.sort_values(["barrio", "anio"]).reset_index(drop=True)
    g["u"], g["t"], g["cl"] = pd.factorize(g.barrio)[0], pd.factorize(g.anio)[0], pd.factorize(g.barrio)[0]
    return g


def resumen(res: dict, ref: float | None, tamano_mc: float | None, d: pd.DataFrame | None = None, coords=None, inf="CR1 t(G−1) por barrio") -> dict:
    p = res["p_t"]
    out = {"coef": res["coef"], "se": res["se"], "ic95": res["ic_t"], "p_principal": p, "p_i7": K.p_corr(p, tamano_mc), "G": res["G"], "n": res["n"], "inferencia": inf,
           "tamano_mc": tamano_mc, "banda": K.banda_mc(tamano_mc) if tamano_mc is not None else "sin medida"}
    if "p_webb" in res:
        out["p_webb"] = res["p_webb"]
    if ref:
        out["razon_ref"] = res["coef"] / ref
        out["coherente_ref"] = bool(res["coef"] * ref > 0 and 1 / 3 <= abs(res["coef"] / ref) <= 3)
    return out


# ------------------------------------------------------------------------------------------------ R1
def r1(P: pd.DataFrame, v: str | None = None, webb_B: int = 0, rng=None, conley: bool = False) -> dict:
    """V18-E1-R1: ln SERPAVI_st = β·HUT_st + α_s + γ_t + δ_b·t, 2018-2024, cluster por barrio. v ∈ {None, 'v1'..'v10'} (anexo A)."""
    opc = {"anios": VENTANA_R, "hut": "hut", "y": "y", "trend": "lineal", "w": None, "excl_top": False, "dist_ano": False, "unidad": "seccion", "adrh": False, "sin": ()}
    mod = {"v1": {"trend": "ninguna"}, "v2": {"trend": "cuad"}, "v3": {"sin": (2020, 2021)}, "v5": {"hut": "hut_exp"}, "v6": {"excl_top": True}, "v7": {"w": "w"},
           "v8": {"dist_ano": True}, "v9": {"unidad": "barrio"}, "v10": {"adrh": True, "anios": list(range(2019, 2024))}}
    opc.update(mod.get(v, {}))
    cols = ["y", opc["hut"]] + (["ladrh"] if opc["adrh"] else [])
    d = muestra(P, opc["anios"], cols, sin_anios=opc["sin"])
    if opc["excl_top"]:
        d = muestra(P, opc["anios"], cols, excl=sin_extremos(d, opc["hut"]), sin_anios=opc["sin"])
    if opc["unidad"] == "barrio":
        d = agregar_barrio(d, [opc["hut"]])
    ex = extra_trend(d, opc["trend"])
    if opc["dist_ano"]:
        e2 = N.interaccion_anio(d.dist_c.values, d.anio.values)
        ex = e2 if ex is None else np.hstack([ex, e2])
    if opc["adrh"]:
        e3 = d[["ladrh"]].values
        ex = e3 if ex is None else np.hstack([ex, e3])
    res = N.ajustar(d, "y", opc["hut"], extra=ex, w=opc["w"], webb_B=webb_B, rng=rng)
    out = {"_d": d, "_res": res, "n_unidades": int(d.u.nunique()), "ventana": f"{d.anio.min()}-{d.anio.max()}"}
    out.update(resumen(res, REF["E1-R1"], 0.045))
    if conley and opc["unidad"] == "seccion":
        ck = coords_km(d)
        M = res["modelo"]
        out["conley"] = {c: M.conley(ck, c) for c in (1.0, 2.0)}
        out["conley_p"] = {c: float(2 * stats.t.sf(abs(res["coef"] / s), res["G"] - 1)) for c, s in out["conley"].items()}
    return out


def r1_diagnosticos(P: pd.DataFrame, r: dict, rng) -> dict:
    """Pruebas B4 de R1: placebo de adelanto (HUT en t+1), sin extremos (exposición y resultado), medida del resultado (€/mes, VU), Moran de los residuos."""
    d = r["_d"]
    out = {}
    dd = d.sort_values(["cod_seccion", "anio"]).copy()
    dd["hut_lead"] = dd.groupby("cod_seccion").hut.shift(-1)
    # el adelanto en 2024 es HUT de 2025 (ventana de estimación hasta 2024): se pierde ese año
    dl = dd.dropna(subset=["hut_lead"]).copy()
    dl["u"], dl["t"] = pd.factorize(dl.cod_seccion)[0], pd.factorize(dl.anio)[0]
    ex = np.hstack([N.tendencias(dl.barrio, dl.anio), dl[["hut"]].values])
    pl = N.ajustar(dl, "y", "hut_lead", extra=ex)
    out["placebo_adelanto"] = {"coef": pl["coef"], "se": pl["se"], "p": pl["p_t"], "n": pl["n"], "mismo_signo": bool(pl["coef"] * r["coef"] > 0)}
    # medida alternativa del resultado: €/mes (VC) y vivienda unifamiliar (VU)
    for nombre, col in (("y_mes", "y_mes"), ("y_vu", "y_vu")):
        s = P.dropna(subset=[col, "hut"]) if False else None
        dm = muestra(P, VENTANA_R, [col, "hut"])
        rr = N.ajustar(dm.rename(columns={col: "yy"}), "yy", "hut", extra=extra_trend(dm, "lineal"))
        out[f"medida_{nombre}"] = {"coef": rr["coef"], "ic95": rr["ic_t"], "p": rr["p_t"], "n": rr["n"], "mismo_signo": bool(rr["coef"] * r["coef"] > 0)}
    # sin atípicos: 1 % superior de exposición y 1 % extremo de la variación del resultado (Δ ln y 2018-2024)
    d0 = muestra(P, VENTANA_R, ["y", "hut"])
    var = d0.groupby("cod_seccion").y.agg(lambda s: s.iloc[-1] - s.iloc[0]).abs()
    ex_out = sin_extremos(d0, "hut") | set(var[var > var.quantile(0.99)].index)
    da = muestra(P, VENTANA_R, ["y", "hut"], excl=ex_out)
    ra = N.ajustar(da, "y", "hut", extra=extra_trend(da, "lineal"))
    out["sin_atipicos"] = {"coef": ra["coef"], "ic95": ra["ic_t"], "p": ra["p_t"], "n": ra["n"], "n_excluidas": len(ex_out), "mismo_signo": bool(ra["coef"] * r["coef"] > 0)}
    # Moran de los residuos medios por sección (vecinos por distancia)
    M = r["_res"]["modelo"]
    out["moran"] = K.moran_i(K.residuo_medio_por_unidad(M), coords_km(d), k=5, B=999)
    return out


# ------------------------------------------------------------------------------------------------ R2 (IV) y A1 (IV)
def _z(d: pd.DataFrame, prox: str, cuando: str) -> np.ndarray:
    zs = (d[prox] - d[prox].mean()) / d[prox].std(ddof=0)
    return (zs * d[cuando]).values


def r2(P: pd.DataFrame, v: str | None = None) -> dict:
    """V18-E1-R2: IV de la HUT por proximidad a atractivos × Trends (variante v1: noches de Eurostat), con distancia al centro × año. Ventana 2018-2024."""
    opc = {"anios": VENTANA_R, "prox": "prox3", "cuando": "trends", "x": "hut", "dist_ano": True, "w": None, "sin": ()}
    mod = {"v1": {"cuando": "noches"}, "v2": {"sin": (2020, 2021)}, "v3": {"prox": "prox3_sin"}, "v4": {"prox": "prox5"}, "v5": {"x": "vut_pct", "anios": [2022, 2023, 2024]},
           "v6": {"dist_ano": False}, "v8": {"w": "w"}}
    opc.update(mod.get(v, {}))
    d = muestra(P, opc["anios"], ["y", opc["x"], opc["prox"], opc["cuando"], "dist_c"], sin_anios=opc["sin"])
    d["z"] = _z(d, opc["prox"], opc["cuando"])
    ex = N.interaccion_anio(d.dist_c.values, d.anio.values) if opc["dist_ano"] else None
    res = N.iv_ajustar(d, "y", opc["x"], "z", extra=ex, w=opc["w"])
    out = {"_d": d, "_res": res, "n_unidades": int(d.u.nunique()), "ventana": f"{d.anio.min()}-{d.anio.max()}", "coef": res["beta"], "se": res["se"], "ic95_2sls": res["ic_t"],
           "p_2sls": res["p_t"], "p_principal": res["p_ar"], "ic_ar": res["ar_ic"], "F": res["F_efectivo"], "G": res["G"], "n": res["n"], "p_i7": res["p_ar"], "tamano_mc": 0.0485,
           "banda": "apta (AR, p = 1: iv_debil)", "inferencia": "Anderson-Rubin por barrio (IC exacto) con F efectivo de MOP; 2SLS con t(G−1) al lado",
           "razon_ref": res["beta"] / REF["E1-R2"], "pi": res["pi"], "rf": res["rf"], "p_rf": res["p_rf"], "_x": opc["x"], "_cluster": "barrio"}
    t, lo, hi = res["ar_ic"]
    out["ic95"] = (lo, hi) if t == "intervalo" else (np.nan, np.nan)
    out["coherente_ref"] = bool(res["beta"] * REF["E1-R2"] > 0 and 1 / 3 <= abs(out["razon_ref"]) <= 3)
    return out


def a1(P: pd.DataFrame, v: str | None = None, ciudades=("46250", "41091", "29067", "03014")) -> dict:
    """V18-E1-A1: ln SERPAVI_st sobre el % de viviendas turísticas (INE-VUT, media anual) con efectos de sección y de municipio × año, distancia al centro × año;
    instrumento: proximidad a atractivos × noches de la NUTS3 (Eurostat). 2021-2024, cluster por distrito censal."""
    opc = {"anios": VENTANA_A1, "x": "vut_pct", "y": "y", "dist_ano": True, "w": None, "excl_top": False, "ciudades": list(ciudades), "sin": ()}
    mod = {"v1": {"anios": [2022, 2023, 2024]}, "v2": {"ciudades": list(ciudades) + ["08019"]}, "v4": {"w": "w"}, "v5": {"x": "vut_plazas100"}, "v10": {"excl_top": True}, "v11": {"dist_ano": False}}
    if v in ("v6", "v7", "v8", "v9"):
        mod[v] = {"ciudades": [{"v6": "46250", "v7": "41091", "v8": "29067", "v9": "03014"}[v]]}
    opc.update(mod.get(v, {}))
    Q = P[P.cod_mun.isin(opc["ciudades"])]
    d = muestra(Q, opc["anios"], ["y", opc["x"], "prox3", "noches", "dist_c"], cluster="cod_distrito")
    if opc["excl_top"]:
        d = muestra(Q, opc["anios"], ["y", opc["x"], "prox3", "noches", "dist_c"], excl=sin_extremos(d, opc["x"]), cluster="cod_distrito")
    d["z"] = _z(d, "prox3", "noches")
    cy = N.dummies(d.cod_mun.astype(str) + "_" + d.anio.astype(str))
    ex = cy if not opc["dist_ano"] else np.hstack([cy, N.interaccion_anio(d.dist_c.values, d.anio.values)])
    res = N.iv_ajustar(d, "y", opc["x"], "z", extra=ex, w=opc["w"])
    out = {"_d": d, "_res": res, "n_unidades": int(d.u.nunique()), "ventana": f"{d.anio.min()}-{d.anio.max()}", "coef": res["beta"], "se": res["se"], "ic95_2sls": res["ic_t"],
           "p_2sls": res["p_t"], "p_principal": res["p_ar"], "ic_ar": res["ar_ic"], "F": res["F_efectivo"], "G": res["G"], "n": res["n"], "p_i7": res["p_ar"], "tamano_mc": 0.0485,
           "banda": "apta (AR, p = 1: iv_debil)", "inferencia": "Anderson-Rubin por distrito censal (IC exacto) con F efectivo de MOP; 2SLS con t(G−1) al lado",
           "razon_ref": res["beta"] / REF["E1-A1"], "pi": res["pi"], "rf": res["rf"], "p_rf": res["p_rf"], "ciudades": opc["ciudades"], "_x": opc["x"], "_cluster": "cod_distrito"}
    t, lo, hi = res["ar_ic"]
    out["ic95"] = (lo, hi) if t == "intervalo" else (np.nan, np.nan)
    out["coherente_ref"] = bool(res["beta"] * REF["E1-A1"] > 0 and 1 / 3 <= abs(out["razon_ref"]) <= 3)
    return out


def iv_placebos(P: pd.DataFrame, r: dict, cuando: str, extra_fun, cluster: str, prox_real: str = "prox3") -> dict:
    """Placebos del instrumento: proximidad a hospitales y universidades × el mismo «cuándo»; forma reducida (ln y sobre z, con los mismos efectos y controles), en unidades
    de una desviación típica de la proximidad, comparada con la forma reducida del instrumento real."""
    d = r["_d"]
    ex = extra_fun(d)
    out = {}
    for nombre, col in (("real", prox_real), ("hospitales", "prox_hosp"), ("universidades", "prox_univ")):
        d2 = d.copy()
        d2["zz"] = _z(d2, col, cuando)
        rr = N.iv_ajustar(d2, "y", r["_x"], "zz", extra=ex)
        out[nombre] = {"rf": rr["rf"], "se_rf": rr["se_rf"], "p_rf": rr["p_rf"], "F": rr["F_efectivo"], "pi": rr["pi"]}
    base = out["real"]["rf"]
    for nombre in ("hospitales", "universidades"):
        o = out[nombre]
        o["mismo_signo"] = bool(o["rf"] * base > 0)
        o["mitad_del_efecto"] = bool(abs(o["rf"]) >= 0.5 * abs(base))
        o["decisivo"] = bool(o["p_rf"] < 0.05 and o["mismo_signo"] and o["mitad_del_efecto"])
        o["debil"] = bool(0.05 <= o["p_rf"] <= 0.10)
    return out


def primera_etapa_subperiodos(P: pd.DataFrame, r: dict, ex_fun) -> dict:
    """Primera etapa por subperiodo (adenda R-14): 2018-2019, 2020-2021 y 2022-2024."""
    d = r["_d"]
    out = {}
    for nombre, anios in (("2018-2019", [2018, 2019]), ("2020-2021", [2020, 2021]), ("2022-2024", [2022, 2023, 2024])):
        s = d[d.anio.isin(anios)].copy()
        s["u"], s["t"] = pd.factorize(s.cod_seccion)[0], pd.factorize(s.anio)[0]
        s["cl"] = pd.factorize(s[r["_cluster"]])[0]
        try:
            rr = N.iv_ajustar(s, "y", r["_x"], "z", extra=ex_fun(s))
            out[nombre] = {"pi": rr["pi"], "F": rr["F_efectivo"], "n": rr["n"]}
        except Exception as e:  # noqa: BLE001
            out[nombre] = {"pi": np.nan, "F": np.nan, "n": 0, "error": str(e)[:80]}
    pis = [v["pi"] for v in out.values() if np.isfinite(v["pi"])]
    out["cambia_signo"] = bool(len(pis) > 1 and (min(pis) < 0 < max(pis)))
    return out


def hansen_j(d: pd.DataFrame, prox: str, cuandos: list[str], x: str, extra, cluster: str = "cl") -> dict:
    """Contraste de sobreidentificación de Hansen (varianza agrupada) con las dos medidas del «cuándo» a la vez: instrumentos prox × Trends y prox × noches."""
    from herramientas import iv_debil as IV
    M = K.Modelo(d["y"].values, d[x].values, d.u.values, d.t.values, extra=extra, cluster=d[cluster].values)
    Zs = []
    for c in cuandos:
        z = _z(d, prox, c)
        Zs.append(M._m(M.sw * z[M.orden]))
    Z = np.column_stack(Zs)
    cl = np.unique(M.cl_ord, return_inverse=True)[1]
    G = int(cl.max()) + 1
    if np.linalg.matrix_rank(Z, tol=1e-8 * np.abs(Z).max()) < Z.shape[1]:
        return {"calculable": False, "motivo": "instrumentos colineales tras parcializar"}
    X = M.dtil[:, None]
    beta, _ = IV.dos_sls(M.ytil, X, Z, cl, G)
    e = M.ytil - X @ beta
    S = np.zeros((G, Z.shape[1]))
    np.add.at(S, cl, Z * e[:, None])
    g = S.sum(0)
    W = S.T @ S * G / (G - 1)
    J = float(g @ np.linalg.solve(W + 1e-12 * np.eye(len(g)), g))
    gl = Z.shape[1] - 1
    return {"calculable": True, "J": J, "gl": gl, "p": float(stats.chi2.sf(J, gl))}


def pretendencia_instrumento(P: pd.DataFrame, ciudades: list[str] | None, a0: int, a1_: int, cluster: str, controles=("dist_c",), prox: str = "prox3") -> dict:
    """El instrumento (proximidad, desviaciones típicas) no predice la variación del resultado previa: Δ ln SERPAVI a0 → a1_ por sección, con efectos de ciudad y la distancia al
    centro; EE agrupados por cluster (CR1 con t(G−1))."""
    Q = P if ciudades is None else P[P.cod_mun.isin(ciudades)]
    w = Q.pivot_table(index="cod_seccion", columns="anio", values="y", aggfunc="first")
    base = Q.drop_duplicates("cod_seccion").set_index("cod_seccion")
    s = pd.DataFrame({"dy": w[a1_] - w[a0]}).join(base[[prox, cluster, "cod_mun", *controles]]).dropna()
    out = {"n": int(len(s)), "G": int(s[cluster].nunique())}
    if len(s) < 30 or out["G"] < 3:
        return {**out, "p": np.nan, "coef": np.nan, "motivo": "datos insuficientes en el periodo previo"}
    zs = (s[prox] - s[prox].mean()) / s[prox].std(ddof=0)
    X = np.column_stack([zs.values, *[s[c].values for c in controles], N.dummies(s.cod_mun)])
    r = _ols_cluster(s.dy.values, X, s[cluster].values)
    return {**out, "coef": r["b"][0], "se": r["se"][0], "p": r["p"][0]}


def _ols_cluster(y, X, cl) -> dict:
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    c = pd.factorize(pd.Series(cl).astype(str))[0]
    G = c.max() + 1
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, c, X * e[:, None])
    n, k = X.shape
    k = np.linalg.matrix_rank(X)
    V = G / (G - 1) * (n - 1) / max(n - k, 1) * XtXi @ (S.T @ S) @ XtXi
    se = np.sqrt(np.diag(V))
    return {"b": b, "se": se, "p": 2 * stats.t.sf(np.abs(b / se), G - 1)}


# ------------------------------------------------------------------------------------------------ R3 (estudio de eventos de dosis)
ANIOS_R3 = list(range(2011, 2020))


def r3(P: pd.DataFrame, v: str | None = None, webb_B: int = 0, rng=None) -> dict:
    """V18-E1-R3: ln SERPAVI_st = Σ_k β_k·D_s·1[t = k] + α_s + γ_t, D = densidad HUT de 2018T2 (por 100 viviendas), k = 2011-2019, base 2013 (v1: 2012).
    Resumen: media de β_k posteriores a 2013 (2014-2019), estimada como un solo coeficiente D × 1[t ≥ 2014] con los adelantos como controles."""
    opc = {"base": 2013, "dosis": "dosis0", "dist_ano": False, "unidad": "seccion", "excl_top": False}
    mod = {"v1": {"base": 2012}, "v2": {"dosis": "dosis_bin"}, "v3": {"dist_ano": True}, "v4": {"unidad": "barrio"}, "v5": {"excl_top": True}}
    opc.update(mod.get(v, {}))
    d = muestra(P, ANIOS_R3, ["y", "dosis0"])
    if opc["excl_top"]:
        d = muestra(P, ANIOS_R3, ["y", "dosis0"], excl=set(d.drop_duplicates("cod_seccion").pipe(lambda s: s[s.dosis0 > s.dosis0.quantile(0.99)]).cod_seccion))
    d["dosis_bin"] = (d.dosis0 > d.drop_duplicates("cod_seccion").dosis0.quantile(0.90)).astype(float)
    if opc["unidad"] == "barrio":
        d = agregar_barrio(d, ["dosis0"])
    if "dosis_bin" not in d:
        d["dosis_bin"] = (d.dosis0 > d.drop_duplicates("cod_seccion").dosis0.quantile(0.90)).astype(float)
    dos = opc["dosis"]
    sd = d.drop_duplicates("cod_seccion")[dos].std(ddof=0)
    d["D"] = d[dos] / sd                                           # dosis estandarizada (por desviación típica entre secciones)
    base = opc["base"]
    d["post"] = (d.anio >= 2014).astype(float)
    pre_k = [k for k in ANIOS_R3 if k < 2014 and k != base]
    lead = np.column_stack([(d.anio.values == k) * d.D.values for k in pre_k]) if pre_k else None
    if base == 2012:        # base 2012: los años 2011 y 2013 son «adelantos» (2013 es previo a la dosis posterior)
        pre_k = [2011, 2013]
        lead = np.column_stack([(d.anio.values == k) * d.D.values for k in pre_k])
    d["Dpost"] = d.D * (d.anio >= 2014).astype(float)
    ex = lead
    if opc["dist_ano"] and "dist_c" in d:
        e2 = N.interaccion_anio(d.dist_c.values, d.anio.values)
        ex = e2 if ex is None else np.hstack([ex, e2])
    res = N.ajustar(d, "y", "Dpost", extra=ex, webb_B=webb_B, rng=rng)
    out = {"_d": d, "_res": res, "n_unidades": int(d.u.nunique()), "ventana": f"{d.anio.min()}-{d.anio.max()}", "_sd_dosis": float(sd)}
    # por pp de densidad HUT: coeficiente por desviación típica / desviación típica (solo la dosis continua)
    out.update(resumen(res, None, 0.045))
    out["coef_por_pp"] = res["coef"] / sd if dos == "dosis0" else np.nan
    out["ic95_por_pp"] = tuple(np.array(res["ic_t"]) / sd) if dos == "dosis0" else (np.nan, np.nan)
    out["razon_ref"] = out["coef_por_pp"] / REF["E1-R3"] if dos == "dosis0" else np.nan
    out["coherente_ref"] = bool(dos == "dosis0" and res["coef"] * REF["E1-R3"] > 0 and 1 / 3 <= abs(out["razon_ref"]) <= 3)
    return out


def r3_evento(P: pd.DataFrame) -> dict:
    """Estudio de eventos completo de R3 (base 2013): β_k de dosis × año, pretendencias, potencia de Roth y Honest DiD."""
    d = muestra(P, ANIOS_R3, ["y", "dosis0"])
    sd = d.drop_duplicates("cod_seccion").dosis0.std(ddof=0)
    d["D"] = d.dosis0 / sd
    ev = N.evento_dosis(d, "y", "D", ANIOS_R3, 2013)
    pre = N.pretendencias(ev, 2013)
    hon = N.honest_dosis(ev, 2013)
    # placebo de fecha: base falsa en 2011; ventana 2011-2013; adopción falsa en 2012
    dp = muestra(P, [2011, 2012, 2013], ["y", "dosis0"])
    dp["D"] = dp.dosis0 / sd
    dp["Dpost"] = dp.D * (dp.anio >= 2012).astype(float)
    pf = N.ajustar(dp, "y", "Dpost")
    # tendencia por distancia al centro 2011-2013 (diagnóstico de la adenda R-15)
    td = pretendencia_dist(P)
    return {"ev": ev, "pretend": pre, "honest": hon, "placebo_fecha": {"coef": pf["coef"], "p": pf["p_t"], "mismo_signo": None, "n": pf["n"]}, "tendencia_distancia": td, "sd_dosis": float(sd)}


def pretendencia_dist(P: pd.DataFrame) -> dict:
    """Tendencia por distancia al centro de 2011-2013: Δ ln y (2011 → 2013) sobre la distancia al centro (sección), cluster por barrio."""
    w = P.pivot_table(index="cod_seccion", columns="anio", values="y", aggfunc="first")
    b = P.drop_duplicates("cod_seccion").set_index("cod_seccion")
    s = pd.DataFrame({"dy": w[2013] - w[2011]}).join(b[["dist_c", "barrio"]]).dropna()
    r = _ols_cluster(s.dy.values, np.column_stack([np.ones(len(s)), s.dist_c.values]), s.barrio.values)
    return {"coef": float(r["b"][1]), "p": float(r["p"][1]), "n": int(len(s))}


# ------------------------------------------------------------------------------------------------ R4 (Sagrada Família)
def sf_geometria() -> dict:
    """Secciones de Barcelona (todas, con y sin sellado) por distancia del centroide al templo; recuentos para la regla del 75 % (adenda 1.5)."""
    import geopandas as gpd
    g = gpd.read_parquet(D.GEO)
    g = g[g.cod_municipio == "08019"][["cod_seccion", "cod_distrito", "geometry"]].reset_index(drop=True)
    c = g.geometry.to_crs(25831).centroid          # centroide geométrico en ETRS89 / UTM 31N (K8: la réplica ciega usa el centroide, no un punto interior)
    x, y = c.x.values, c.y.values
    tx, ty = D.proyectar([D.TEMPLO["sagrada_familia"][0]], [D.TEMPLO["sagrada_familia"][1]], 25831)
    g["dist_sf"] = np.sqrt((x - tx[0]) ** 2 + (y - ty[0]) ** 2) / 1000.0
    g["sellada"] = g.cod_distrito.isin(set(D.SELLADAS_BCN))
    return g.drop(columns="geometry")


def r4_conteos(g: pd.DataFrame, r_in: float = 0.5, r_out: float = 1.0) -> dict:
    dentro = g[g.dist_sf < r_in]
    anillo = g[(g.dist_sf >= r_in) & (g.dist_sf < r_out)]
    return {"radio_total": len(dentro), "radio_no_sellado": int((~dentro.sellada).sum()), "anillo_total": len(anillo), "anillo_no_sellado": int((~anillo.sellada).sum()),
            "cuota_radio": float((~dentro.sellada).mean()) if len(dentro) else np.nan, "cuota_anillo": float((~anillo.sellada).mean()) if len(anillo) else np.nan}


def r4(P: pd.DataFrame, g: pd.DataFrame, v: str | None = None, webb_B: int = 0, rng=None) -> dict:
    """V18-E1-R4 (K8 bis): diferencias en diferencias de las secciones a < 500 m del templo frente al anillo de 500-1.000 m SIN los adelantos de 2011-2012 como regresores (los adelantos
    son el diagnóstico de pretendencias, r4_eventos); v1: resto de Barcelona; v2: 300 m y 300-800 m; v3: estudio de eventos con los adelantos como regresores. Tratamiento desde
    2014, base 2013, preperiodo 2011-2012, años 2011-2019, efectos de sección y de año, cluster por barrio."""
    r_in, r_out, resto = {"v1": (0.5, 1.0, True), "v2": (0.3, 0.8, False)}.get(v, (0.5, 1.0, False))
    gg = g.set_index("cod_seccion")
    d = muestra(P, ANIOS_R3, ["y"])
    dist = d.cod_seccion.map(gg.dist_sf)
    d["tr"] = (dist < r_in).astype(float)
    d["en_anillo"] = ((dist >= r_in) & (dist < r_out)).astype(float)
    d = d[(d.tr == 1) | (d.en_anillo == 1) | resto].copy()
    d = d.sort_values(["cod_seccion", "anio"]).reset_index(drop=True)
    d["u"], d["t"], d["cl"] = pd.factorize(d.cod_seccion)[0], pd.factorize(d.anio)[0], pd.factorize(d.barrio)[0]
    d["Dpost"] = d.tr * (d.anio >= 2014).astype(float)
    lead = np.column_stack([(d.anio.values == k) * d.tr.values for k in (2011, 2012)]) if v == "v3" else None
    res = N.ajustar(d, "y", "Dpost", extra=lead, webb_B=webb_B, rng=rng)
    out = {"_d": d, "_res": res, "n_tratadas": int(d[d.tr == 1].u.nunique()), "n_control": int(d[d.tr == 0].u.nunique()), "n_unidades": int(d.u.nunique()), "ventana": "2011-2019",
           "G_tratados": int(d[d.tr == 1].cl.nunique())}
    out.update(resumen(res, None, 0.0595 if res["G"] <= 8 else 0.045))
    if webb_B:
        out["p_i7"] = K.p_corr(res.get("p_webb", out["p_principal"]), 0.0595 if res["G"] <= 8 else 0.0465)
    return out


def r4_eventos(d: pd.DataFrame) -> dict:
    ev = N.evento_dosis(d.assign(D=d.tr), "y", "D", ANIOS_R3, 2013)
    pre = N.pretendencias(ev, 2013)
    hon = N.honest_dosis(ev, 2013)
    dp = d[d.anio.isin([2011, 2012, 2013])].copy()
    dp["u"], dp["t"] = pd.factorize(dp.cod_seccion)[0], pd.factorize(dp.anio)[0]
    dp["Dpost"] = dp.tr * (dp.anio >= 2012).astype(float)
    pf = N.ajustar(dp, "y", "Dpost")
    return {"ev": ev, "pretend": pre, "honest": hon, "placebo_fecha": {"coef": pf["coef"], "p": pf["p_t"], "n": pf["n"]}}


# ------------------------------------------------------------------------------------------------ coprincipal P-H3 (V15), muestra V18
def absorber(vs: list[np.ndarray], grupos: list[np.ndarray], tol: float = 1e-11, maxit: int = 2000) -> list[np.ndarray]:
    """Mínimos cuadrados alternos (MAP): resta de cada vector las medias de cada grupo hasta convergencia."""
    out = [np.asarray(v, float).copy() for v in vs]
    cnt = [np.bincount(g) for g in grupos]
    for _ in range(maxit):
        mov = 0.0
        for v in out:
            for g, c in zip(grupos, cnt):
                m = np.bincount(g, weights=v) / c
                v -= m[g]
                mov = max(mov, float(np.abs(m).max()))
        if mov < tol:
            break
    return out


def ph3(sitio_municipio=None) -> dict:
    """E1-P-H3: la especificación de H3 de V15 (log SERPAVI VC sobre el % de viviendas turísticas INE estandarizado por la DT intra-sección, efectos fijos de sección y de
    municipio × año, 2021-2024, cluster por municipio) en la muestra V18 (sin unidades selladas de v6, V15 y V16)."""
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "periodo", "valor", "desagregacion", "edicion", "muestra_sellada_v6"],
                        filters=[("variable", "==", "serpavi_alquiler_m2_mediana"), ("nivel", "==", "seccion"), ("frecuencia", "==", "A"), ("periodo", "in", ["2021", "2022", "2023", "2024"])])
    h = K.filtrar(h, "territorio_codigo", "seccion", "periodo", "serpavi_alquiler_m2_mediana", "A")
    h = h[(h.desagregacion == "tipologia=VC") & (h.valor > 0)]
    y = pd.DataFrame({"cod_seccion": h.territorio_codigo.values, "anio": h.periodo.astype(int).values, "y": np.log(h.valor.values)})
    cods = y.cod_seccion.unique().tolist()
    p = D.ine_vut(cods, "ine_vut_porcentaje_vivienda_turistica").rename(columns={"valor": "pct"})
    d = y.merge(p, on=["cod_seccion", "anio"], how="inner")
    pres = d.groupby("cod_seccion").anio.agg(lambda a: {2021, 2024} <= set(a))
    d = d[d.cod_seccion.isin(pres[pres].index)].copy()
    d["mun"] = d.cod_seccion.str[:5]
    sd = float((d.pct - d.groupby("cod_seccion").pct.transform("mean")).std(ddof=1))
    d["x"] = d.pct / sd
    u = pd.factorize(d.cod_seccion)[0]
    my = pd.factorize(d.mun + "_" + d.anio.astype(str))[0]
    yt, xt = absorber([d.y.values, d.x.values], [u, my])
    dd = float(xt @ xt)
    beta = float(xt @ yt / dd)
    e = yt - beta * xt
    cl = pd.factorize(d.mun)[0]
    G = int(cl.max()) + 1
    s = np.bincount(cl, weights=xt * e)
    se = float(np.sqrt(G / (G - 1) * (s ** 2).sum()) / dd)
    t = beta / se
    p_t = float(2 * stats.t.sf(abs(t), G - 1))
    q = stats.t.ppf(0.975, G - 1)
    return {"coef": beta, "se": se, "ic95": (beta - q * se, beta + q * se), "p_principal": p_t, "G": G, "n": len(d), "n_secciones": int(d.cod_seccion.nunique()), "sd_intra": sd,
            "tamano_mc": None, "inferencia": "CR1 t(G−1) por municipio (la de V15; rechazo placebo 0,052 en su Monte Carlo)", "ventana": "2021-2024", "p_i7": p_t}
