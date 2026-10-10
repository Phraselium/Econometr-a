"""Rama BA (alquiler) - utilidades: MCO con efectos fijos, EE cluster, wild cluster bootstrap (Webb),
variables derivadas y predictores fuera de muestra. Sin red; datos solo vía v2_common.load.

Nota de determinismo: se fuerza 1 hilo BLAS antes de importar numpy.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.linalg as sla
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import econ_utils as eu  # noqa: E402
import v2_common as vc  # noqa: E402

SEED = vc.SEED
OUT = ROOT / "output" / "v2" / "BA"

# Periodos pre-registrados (docs/v2/hipotesis.md), restringidos a la muestra de H1 (2008Q1-2024Q2)
PERIODOS = {"P1": ("2008Q1", "2013Q4"), "P2": ("2014Q1", "2019Q4"),
            "P3": ("2020Q1", "2021Q4"), "P4": ("2022Q1", "2024Q2")}
PERIODOS_A = {"P1": (2008, 2013), "P2": (2014, 2019), "P3": (2020, 2021), "P4": (2022, 2024)}
H1_X = ["d4_ln_pob_20_34", "d4_ln_pob_extranj", "d4_ln_ocupados"]
H1_Y = "d4_ln_ipc_alquiler"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def periodo_de(q: str) -> str | None:
    for k, (a, b) in PERIODOS.items():
        if a <= q <= b:
            return k
    return None


# ------------------------------------------------------------------ MCO con efectos fijos
def fe_ols(df, y, xs, fe=("cod_prov", "trimestre"), cluster="cod_prov", boot_vars=(), B=0, seed=SEED):
    """MCO con efectos fijos por proyección (FWL), EE cluster CR1 y p/IC con t(G-1).
    boot_vars/B: wild cluster bootstrap restringido (WCR, pesos de Webb de 6 puntos) para cada variable.
    La corrección de muestras pequeñas es G/(G-1)*(N-1)/(N-K), K = k_x + rango de los FE no anidados
    en el cluster."""
    xs = list(xs)
    d = df.dropna(subset=[y] + xs + list(fe) + [cluster]).copy()
    d = d.sort_values(cluster, kind="stable").reset_index(drop=True)
    n = len(d)
    mats, lev_cl = [], 0
    for i, f in enumerate(fe):
        dm = pd.get_dummies(d[f].astype(str), drop_first=(i > 0)).to_numpy(float)
        mats.append(dm)
        if f == cluster:
            lev_cl = dm.shape[1]
    D = np.hstack(mats)
    Qm, R, piv = sla.qr(D, mode="economic", pivoting=True)
    rank = int((np.abs(np.diag(R)) > 1e-8 * abs(R[0, 0])).sum())
    Q = Qm[:, :rank]
    X = d[xs].to_numpy(float)
    yv = d[y].to_numpy(float)
    Xt = X - Q @ (Q.T @ X)
    yt = yv - Q @ (Q.T @ yv)
    A = Xt.T @ Xt
    Ainv = np.linalg.inv(A)
    beta = Ainv @ (Xt.T @ yt)
    e = yt - Xt @ beta
    cl, ucl = pd.factorize(d[cluster])
    G = len(ucl)
    starts = np.r_[0, np.flatnonzero(np.diff(cl)) + 1]
    S = np.add.reduceat(Xt * e[:, None], starts, axis=0)
    K = len(xs) + rank - lev_cl
    c = G / (G - 1) * (n - 1) / (n - K)
    V = c * Ainv @ (S.T @ S) @ Ainv
    se = np.sqrt(np.diag(V))
    t = beta / se
    dfree = G - 1
    p = 2 * stats.t.sf(np.abs(t), dfree)
    tq = stats.t.ppf(0.975, dfree)
    res = dict(names=xs, beta=beta, se=se, t=t, p=p, lo=beta - tq * se, hi=beta + tq * se, V=V,
               n=n, G=G, r2_within=float(1 - (e @ e) / (yt @ yt)), df=dfree, K=K,
               muestra=(str(d[fe[-1]].min()), str(d[fe[-1]].max())), p_boot={}, X=d[xs], data=d)
    if B and boot_vars:
        for jv in boot_vars:
            res["p_boot"][jv] = _wcr(Xt, yt, Ainv, Q, cl, starts, G, c, xs.index(jv), float(t[xs.index(jv)]),
                                     B, seed + xs.index(jv))
    return res


def _wcr(Xt, yt, Ainv, Q, cl, starts, G, c, j, t_obs, B, seed, bs=500):
    n, k = Xt.shape
    keep = [i for i in range(k) if i != j]
    if keep:
        br = np.linalg.lstsq(Xt[:, keep], yt, rcond=None)[0]
        fit_r = Xt[:, keep] @ br
    else:
        fit_r = np.zeros(n)
    u = yt - fit_r
    z = Xt @ Ainv[j, :]
    rng = np.random.default_rng(seed)
    tstar, hecho = [], 0
    while hecho < B:
        b = min(bs, B - hecho)
        W = WEBB[rng.integers(0, 6, size=(G, b))]
        U = u[:, None] * W[cl]
        MU = U - Q @ (Q.T @ U)
        Y = fit_r[:, None] + MU
        bj = z @ Y
        E = Y - Xt @ (Ainv @ (Xt.T @ Y))
        sc = np.add.reduceat(z[:, None] * E, starts, axis=0)
        tstar.append(bj / np.sqrt(c * (sc ** 2).sum(axis=0)))
        hecho += b
    tstar = np.concatenate(tstar)
    return float(np.mean(np.abs(tstar) >= abs(t_obs)))


def tabla_res(res, spec_id, extra=None):
    """DataFrame (una fila por coeficiente) de un fe_ols."""
    rows = []
    for i, nm in enumerate(res["names"]):
        r = dict(spec=spec_id, var=nm, coef=res["beta"][i], se=res["se"][i], t=res["t"][i], p=res["p"][i],
                 ic95_lo=res["lo"][i], ic95_hi=res["hi"][i], p_boot=res["p_boot"].get(nm, np.nan),
                 n=res["n"], G=res["G"], r2_within=res["r2_within"])
        if extra:
            r.update(extra)
        rows.append(r)
    return pd.DataFrame(rows)


class Log:
    """Envoltorio del Registry de econ_utils: TODA especificación se anota aquí."""

    def __init__(self, ruta):
        self.reg = eu.Registry(ruta)

    def spec(self, fase, mid, formula, res, interes=None, notas=""):
        i = res["names"].index(interes) if interes in res["names"] else None
        self.reg.log(fase, mid, formula, res["muestra"][0], res["muestra"][1], res["n"], np.nan, np.nan,
                     np.nan, np.nan, res["beta"][i] if i is not None else np.nan,
                     (res["p_boot"].get(interes, res["p"][i]) if i is not None else np.nan),
                     notas + f" | G={res['G']}")

    def flush(self):
        self.reg.flush()


def bh(pvals: dict) -> dict:
    """Benjamini-Hochberg (q-valores)."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    q, prev = {}, 1.0
    for i in range(m - 1, -1, -1):
        k, p = items[i]
        prev = min(prev, p * m / (i + 1))
        q[k] = prev
    return q


# ------------------------------------------------------------------ variables derivadas
def preparar_prov_q(d: pd.DataFrame) -> pd.DataFrame:
    """Añade periodo pre-registrado y regresores adicionales (panel completo, antes de recortar).
    x_oferta_l4: retardo de 4 trimestres de Δ4 ln(terminadas libres 4T por 1.000 hab.).
    x_cu: Δ4 de coste_uso_aprox (pp; nacional). Ambos son EXPLORATORIOS."""
    d = d.sort_values(["cod_prov", "trimestre"]).reset_index(drop=True).copy()
    g = d.groupby("cod_prov", sort=False)
    d["periodo"] = d["trimestre"].map(periodo_de)
    roll = g["terminadas_libres"].transform(lambda s: s.rolling(4).sum())
    pc = roll / d["pob_total"] * 1000
    lnpc = np.log(pc.where(pc > 0))
    d["d4_ln_term_pc"] = lnpc - lnpc.groupby(d["cod_prov"]).shift(4)
    d["x_oferta_l4"] = d.groupby("cod_prov", sort=False)["d4_ln_term_pc"].shift(4)
    d["x_cu"] = d["coste_uso_aprox"] - d.groupby("cod_prov", sort=False)["coste_uso_aprox"].shift(4)
    d["anio"] = d["anio"].astype(int)
    d["ccaa"] = d["cod_ccaa"].astype(str)
    return d


def preparar_prov_a(d: pd.DataFrame, q: pd.DataFrame) -> pd.DataFrame:
    d = d.sort_values(["cod_prov", "anio"]).reset_index(drop=True).copy()
    d["anio"] = d["anio"].astype(int)
    d["cod_prov"] = d["cod_prov"].astype(str)
    pc = d["terminadas_libres"] / d["pob_total"] * 1000
    d["ln_term_pc"] = np.log(pc.where(pc > 0))
    d["d_ln_term_pc"] = d.groupby("cod_prov", sort=False)["ln_term_pc"].diff()
    d["x_oferta_l1"] = d.groupby("cod_prov", sort=False)["d_ln_term_pc"].shift(1)
    qn = q.groupby("trimestre").agg(anio=("anio", "first"), cu=("coste_uso_aprox", "mean"))
    cu = qn.groupby("anio")["cu"].agg(["mean", "count"])
    cu = cu["mean"].where(cu["count"] == 4)          # solo años con 4 trimestres
    d["x_cu"] = d["anio"].map(cu) - d["anio"].sub(1).map(cu)
    d["periodo"] = d["anio"].map(lambda a: next((k for k, (x, y) in PERIODOS_A.items() if x <= a <= y), None))
    return d


# ------------------------------------------------------------------ fuera de muestra
CONFIGS = {
    "A_solo_H1": dict(ar=False, oferta=False, cu=False),
    "B_AR4_mas_H1": dict(ar=True, oferta=False, cu=False),      # PRIMARIO (declarado antes de ver resultados)
    "C_AR4_H1_oferta": dict(ar=True, oferta=True, cu=False),
    "D_AR4_H1_oferta_cu": dict(ar=True, oferta=True, cu=True),
}
PRIMARIO = "B_AR4_mas_H1"


def _step_ln(long, v):
    """ln de la serie de población en escalera: último valor OBSERVADO (1 enero) conocido en t.
    Evita la fuga de la interpolación intra-anual (que usa el 1 de enero siguiente)."""
    obs = long[v].where(long[v + "_metodo"] == "observado")
    step = obs.groupby(long["unidad"]).ffill(limit=3)
    return np.log(step.where(step > 0))


def make_feat(cfg):
    def f(long):
        g = vc._g
        cols = []
        if cfg["ar"]:
            for k in range(4):
                long[f"dY_l{k}"] = g(long, long["dY"], k) if k else long["dY"]
                cols.append(f"dY_l{k}")
        for v in ("pob_20_34", "pob_extranj"):
            ls = _step_ln(long, v)
            long["xb_" + v] = ls - g(long, ls, 4)
            cols.append("xb_" + v)
        long["xb_ocup"] = long["ln_ocupados"] - g(long, long["ln_ocupados"], 4)
        cols.append("xb_ocup")
        if cfg["oferta"]:
            roll = long.groupby("unidad")["terminadas_libres"].transform(lambda s: s.rolling(4).sum())
            ptot = np.exp(_step_ln(long, "pob_total"))
            pc = roll / ptot * 1000
            lp = np.log(pc.where(pc > 0))
            long["xb_oferta"] = lp - g(long, lp, 4)
            cols.append("xb_oferta")
        if cfg["cu"]:
            long["xb_cu"] = long["coste_uso_aprox"] - g(long, long["coste_uso_aprox"], 4)
            cols.append("xb_cu")
        return cols
    return f


def predecir_modelo(df, nombre, cfg, splits=None, desde=None, min_train=36):
    """Predicción directa a h=4 del alquiler provincial (nominal) con el modelo `cfg`, mismo
    marco que panel_ar4 (FE de unidad + dummies del trimestre objetivo, ventana expansiva)."""
    return vc._run(df, "cod_prov", 4, splits, desde, min_train, 4, 4, vc._lvl_fn("ipc_alquiler", False, None),
                   make_feat(cfg), nombre)


def muestra_comun(frames: dict) -> dict:
    """Recorta todos los DataFrame de predicciones a la intersección exacta de (unidad, periodo)."""
    idx = None
    for f in frames.values():
        k = f.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(
            ["unidad", "periodo"]).index
        idx = k if idx is None else idx.intersection(k)
    out = {}
    for nm, f in frames.items():
        m = f.drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"]).loc[idx].reset_index()
        out[nm] = m
    return out
