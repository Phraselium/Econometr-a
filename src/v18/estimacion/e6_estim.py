"""V18 · fase 4 · E6-R1 · estimación sobre las pilas de e6_diseno: coeficiente medio de k = 0..3, estudio de eventos, placebo de fecha, Honest DiD, MDE y pruebas B4.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. SEED = 20261010.
Ecuación: ln SERPAVI_ja = Σ_{k=-4..-1} γ_k·Tr_j·1[k] + β·Tr_j·1[0 <= k <= 3] + α_(j,pila) + δ_(año,pila) + θ_(municipio,año,pila) + ε; referencia k = −5;
EE agrupados por sección del edificio (CR1 con t(G−1)); Webb si G < 40.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_nucleo as N  # noqa: E402

SEMILLA = K.SEMILLA
REF_R1 = -0.062
DELTA_R1 = 0.031
LEADS = [-4, -3, -2, -1]
POST = [0, 1, 2, 3]


def preparar(d: pd.DataFrame, secs: pd.DataFrame) -> pd.DataFrame:
    """Codifica unidad×pila, año×pila y cluster (sección del edificio), añade adelantos, post, coordenadas (km) y el municipio×año×pila."""
    d = d.sort_values(["unit_pila", "anio"]).reset_index(drop=True).copy()
    d["u"] = pd.factorize(d.unit_pila)[0]
    d["t"] = pd.factorize(d.anio_pila)[0]
    d["cl"] = pd.factorize(d.bsec)[0]
    d["Dpost"] = d.tr * d.k.between(POST[0], POST[-1]).astype(float)
    for l in LEADS:
        d[f"lead{l}"] = d.tr * (d.k == l).astype(float)
    xy = secs.set_index("cod_seccion")[["x", "y"]]
    d["x"] = d.cod_seccion.map(xy.x)
    d["y_c"] = d.cod_seccion.map(xy.y)
    return d


def extras(d: pd.DataFrame, con_gmt: bool = True) -> np.ndarray:
    L = d[[f"lead{l}" for l in LEADS]].values
    return np.hstack([L, N.dummies(d.mun_anio_pila)]) if con_gmt else L


def coords_km(d: pd.DataFrame) -> np.ndarray:
    s = d.drop_duplicates("u").sort_values("u")
    return np.column_stack([s.x.values, s.y_c.values]) / 1000.0


def estimar(d: pd.DataFrame, webb_B: int = 0, rng=None, conley: bool = False, con_gmt: bool = True) -> dict:
    res = N.ajustar(d, "y", "Dpost", extra=extras(d, con_gmt), webb_B=webb_B, rng=rng)
    G = res["G"]
    out = {"coef": res["coef"], "se": res["se"], "ic95": res["ic_t"], "p_t": res["p_t"], "p_webb": res.get("p_webb", np.nan), "G": G, "n": res["n"],
           "n_tratadas": int(d[d.tr == 1].cod_seccion.nunique()), "n_controles": int(d[d.tr == 0].cod_seccion.nunique()), "n_unidades_pila": int(d.u.nunique()),
           "G_tratados": int(d[d.tr == 1].cl.nunique()), "_res": res}
    out["razon_ref"] = res["coef"] / REF_R1
    out["coherente_ref"] = bool(res["coef"] * REF_R1 > 0 and 1 / 3 <= abs(out["razon_ref"]) <= 3)
    if conley:
        M = res["modelo"]
        ck = coords_km(d)
        out["conley_se"] = {c: M.conley(ck, c) for c in (1.0, 2.0)}
        out["conley_p"] = {c: float(2 * stats.t.sf(abs(res["coef"] / s), G - 1)) for c, s in out["conley_se"].items()}
    return out


def evento(d: pd.DataFrame) -> dict:
    """Estudio de eventos k = −4..3 (referencia k = −5): coeficientes, pretendencias (contraste conjunto de los adelantos), potencia de Roth y Honest DiD re-referenciado a k = −1."""
    ks = LEADS + POST
    D_ = np.column_stack([d.tr.values * (d.k.values == k) for k in ks])
    ex = N.dummies(d.mun_anio_pila)
    r = K.evento_multi(d.y.values, D_, d.u.values, d.t.values, extra=ex, cluster=d.cl.values)
    ev = {"anios": ks, "b": r["b"], "V": r["V"], "G": r["G"], "k": r["k"]}
    pre_idx = np.array([k < 0 for k in ks])
    b, V = r["b"], r["V"]
    W, p = K.wald_conjunto(b[pre_idx], V[np.ix_(pre_idx, pre_idx)], r["G"])
    ell = np.array([k + 5 for k in ks if k < 0], float)          # pendiente lineal desde la referencia k = −5
    delta = K.roth_pendiente(V[np.ix_(pre_idx, pre_idx)], ell)
    sesgo = float(np.mean([delta * (k + 5) for k in POST]))
    # Honest DiD con referencia k = −1: b' = b − b_{−1} para k ≠ −1; k = −5 entra con b = 0 → b'_{−5} = −b_{−1}
    ks_full = [-5] + ks
    b_full = np.concatenate([[0.0], b])
    V_full = np.zeros((len(ks_full), len(ks_full)))
    V_full[1:, 1:] = V
    i_ref = ks_full.index(-1)
    A = np.eye(len(ks_full)) - np.outer(np.ones(len(ks_full)), np.eye(len(ks_full))[i_ref])
    keep = [i for i in range(len(ks_full)) if i != i_ref]
    bp = (A @ b_full)[keep]
    Vp = (A @ V_full @ A.T)[np.ix_(keep, keep)]
    ks_new = [ks_full[i] for i in keep]
    ev2 = {"anios": ks_new, "b": bp, "V": Vp, "G": r["G"], "k": len(keep)}
    hon = N.honest_dosis(ev2, -1)
    return {"ev": ev, "pretend": {"p": p, "wald": W, "pendiente_detectable": delta, "sesgo_post": sesgo, "n_pre": int(pre_idx.sum()), "n_post": len(POST)}, "honest": hon}


def placebo_fecha(d: pd.DataFrame) -> dict:
    """Evento falso 3 años antes: solo años de la ventana con k <= −1 (periodo previo), adopción falsa en k >= −3 (E' = E − 3)."""
    s = d[d.k <= -1].copy()
    s["Dfalso"] = s.tr * (s.k >= -3).astype(float)
    s = s.sort_values(["unit_pila", "anio"]).reset_index(drop=True)
    s["u"], s["t"], s["cl"] = pd.factorize(s.unit_pila)[0], pd.factorize(s.anio_pila)[0], pd.factorize(s.bsec)[0]
    r = N.ajustar(s, "y", "Dfalso", extra=N.dummies(s.mun_anio_pila))
    return {"coef": r["coef"], "se": r["se"], "p": r["p_t"], "n": r["n"], "G": r["G"]}


def mde(d: pd.DataFrame, secs: pd.DataFrame, sp_vc: pd.DataFrame, R: int = 2000) -> dict:
    """MDE80 de β (media de k = 0..3) con CR1 t(G−1): el ruido se remuestrea de los residuos de 2011-2014 (antes de cualquier cohorte; ln SERPAVI tras efectos de sección y de
    municipio × año) por cluster, con la variación real del tratamiento y de las pilas."""
    M = K.Modelo(np.zeros(len(d)), d.Dpost.values, d.u.values, d.t.values, extra=extras(d), cluster=d.cl.values)
    unidades = sorted(d.cod_seccion.unique())
    pos = {j: i for i, j in enumerate(unidades)}
    # residuos del periodo previo (2011-2014) de las secciones del diseño
    Y = np.log(sp_vc.reindex(index=unidades, columns=[2011, 2012, 2013, 2014]).values.astype(float))
    dfp = pd.DataFrame({"cod_seccion": np.repeat(unidades, 4), "anio": np.tile([2011, 2012, 2013, 2014], len(unidades)), "y": Y.ravel()})
    dfp["mun"] = dfp.cod_seccion.str[:5]
    dfp = dfp.dropna(subset=["y"])
    dfp["mun_anio"] = dfp.mun + "_" + dfp.anio.astype(str)
    R_, unid_p = N.residuos_previos_fe(dfp, "y", "cod_seccion", "anio", [2011, 2012, 2013, 2014], lambda z: N.dummies(z["mun_anio"]))
    Rdf = pd.DataFrame(R_, index=unid_p).reindex(unidades).fillna(0.0)
    cl_unidad = d.drop_duplicates("cod_seccion").set_index("cod_seccion").bsec.reindex(unidades).astype(str).values
    pool = N.PoolResiduos(Rdf.values, cl_unidad)
    uo = d.cod_seccion.map(pos).values.astype(int)
    to = (d.anio.values - d.pila.values + 4).astype(int)        # posición 0..8 dentro de la ventana de la pila
    m = N.mde_ols(M, pool, uo, to, T=9, R=R)
    m["G"] = M.G
    return m


def sin_atipicos(d: pd.DataFrame) -> pd.DataFrame:
    var = d.groupby("unit_pila").y.agg(lambda s: s.iloc[-1] - s.iloc[0]).abs()
    malos = set(var[var > var.quantile(0.99)].index)
    return d[~d.unit_pila.isin(malos)].copy()
