"""Rama BO (oferta y suelo) - utilidades: MCO con efectos fijos (FWL), EE cluster, wild cluster
bootstrap restringido (Webb), 2SLS con EE cluster, F de primera etapa y J de Hansen, y
construcción de variables. Sin red; datos solo vía v2_common.load (el import de este módulo no
carga nada). Se fuerza 1 hilo BLAS antes de importar numpy (determinismo)."""
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
OUT = ROOT / "output" / "v2" / "BO"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


# ------------------------------------------------------------------ efectos fijos (FWL)
def _fe_proj(d, fe, cluster):
    mats, lev_cl = [], 0
    for i, f in enumerate(fe):
        dm = pd.get_dummies(d[f].astype(str), drop_first=(i > 0)).to_numpy(float)
        mats.append(dm)
        if f == cluster:
            lev_cl = dm.shape[1]
    D = np.hstack(mats)
    Qm, R, _ = sla.qr(D, mode="economic", pivoting=True)
    rank = int((np.abs(np.diag(R)) > 1e-8 * abs(R[0, 0])).sum())
    return Qm[:, :rank], rank, lev_cl


def fe_ols(df, y, xs, fe=("cod_prov", "anio"), cluster="cod_prov", boot_vars=(), B=0, seed=SEED):
    """MCO con FE, EE cluster CR1, p y IC con t(G-1). Wild cluster bootstrap restringido (WCR, Webb)
    para cada variable de boot_vars: devuelve p bilateral y p unilaterales (t*>=t, t*<=t)."""
    xs = list(xs)
    d = df.dropna(subset=[y] + xs + list(fe) + [cluster]).copy()
    d = d.sort_values([cluster] + [f for f in fe if f != cluster], kind="stable").reset_index(drop=True)
    n = len(d)
    Q, rank, lev_cl = _fe_proj(d, fe, cluster)
    X = d[xs].to_numpy(float)
    yv = d[y].to_numpy(float)
    Xt = X - Q @ (Q.T @ X)
    yt = yv - Q @ (Q.T @ yv)
    Ainv = np.linalg.inv(Xt.T @ Xt)
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
    res = dict(names=xs, beta=beta, se=se, t=t, p=p, lo=beta - tq * se, hi=beta + tq * se, V=V, n=n, G=G,
               r2_within=float(1 - (e @ e) / (yt @ yt)), df=dfree, K=K,
               muestra=(str(d[fe[-1]].min()), str(d[fe[-1]].max())), boot={}, data=d)
    if B and boot_vars:
        for jv in boot_vars:
            j = xs.index(jv)
            res["boot"][jv] = _wcr(Xt, yt, Ainv, Q, cl, starts, c, j, float(t[j]), B, seed + j)
    return res


def _wcr(Xt, yt, Ainv, Q, cl, starts, c, j, t_obs, B, seed, bs=500):
    n, k = Xt.shape
    G = int(cl.max()) + 1
    keep = [i for i in range(k) if i != j]
    fit_r = Xt[:, keep] @ np.linalg.lstsq(Xt[:, keep], yt, rcond=None)[0] if keep else np.zeros(n)
    u = yt - fit_r
    z = Xt @ Ainv[j, :]
    rng = np.random.default_rng(seed)
    ts, hecho = [], 0
    while hecho < B:
        b = min(bs, B - hecho)
        W = WEBB[rng.integers(0, 6, size=(G, b))]
        U = u[:, None] * W[cl]
        Y = fit_r[:, None] + U - Q @ (Q.T @ U)
        bj = z @ Y
        E = Y - Xt @ (Ainv @ (Xt.T @ Y))
        sc = np.add.reduceat(z[:, None] * E, starts, axis=0)
        ts.append(bj / np.sqrt(c * (sc ** 2).sum(axis=0)))
        hecho += b
    ts = np.concatenate(ts)
    return dict(p2=float(np.mean(np.abs(ts) >= abs(t_obs))), p_ge=float(np.mean(ts >= t_obs)),
                p_le=float(np.mean(ts <= t_obs)), B=int(B))


def p_unilateral(res, var, signo):
    """p unilateral de H1: beta*signo > 0. Bootstrap si existe; si no, t(G-1)."""
    i = res["names"].index(var)
    if var in res["boot"]:
        return res["boot"][var]["p_ge"] if signo > 0 else res["boot"][var]["p_le"]
    t = res["t"][i]
    return float(stats.t.sf(t, res["df"]) if signo > 0 else stats.t.cdf(t, res["df"]))


def tabla_res(res, spec_id, extra=None):
    rows = []
    for i, nm in enumerate(res["names"]):
        b = res["boot"].get(nm, {})
        r = dict(spec=spec_id, var=nm, coef=res["beta"][i], se=res["se"][i], t=res["t"][i], p=res["p"][i],
                 ic95_lo=res["lo"][i], ic95_hi=res["hi"][i], p_boot=b.get("p2", np.nan),
                 p_boot_ge=b.get("p_ge", np.nan), p_boot_le=b.get("p_le", np.nan),
                 n=res["n"], G=res["G"], r2_within=res["r2_within"])
        if extra:
            r.update(extra)
        rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 2SLS con EE cluster
def fe_2sls(df, y, endog, exog, inst, fe=("cod_prov", "anio"), cluster="cod_prov"):
    """2SLS con FE (FWL). EE cluster CR1 (sándwich con X-hat), F de primera etapa (Wald cluster
    conjunto de los instrumentos excluidos, por regresor endógeno) y J de Hansen (2 pasos, cluster).
    Con FE de provincia y año; los instrumentos excluidos son `inst`."""
    endog, exog, inst = list(endog), list(exog), list(inst)
    xs = endog + exog
    d = df.dropna(subset=[y] + xs + inst + list(fe) + [cluster]).copy()
    d = d.sort_values([cluster] + [f for f in fe if f != cluster], kind="stable").reset_index(drop=True)
    n = len(d)
    Q, rank, lev_cl = _fe_proj(d, fe, cluster)

    def res_(cols):
        M = d[cols].to_numpy(float)
        return M - Q @ (Q.T @ M)
    Xt, Zx, yt = res_(xs), res_(inst + exog), res_(y if isinstance(y, list) else [y])[:, 0]
    cl, ucl = pd.factorize(d[cluster])
    G = len(ucl)
    starts = np.r_[0, np.flatnonzero(np.diff(cl)) + 1]
    K = len(xs) + rank - lev_cl
    c = G / (G - 1) * (n - 1) / (n - K)
    ZZinv = np.linalg.pinv(Zx.T @ Zx)
    Xh = Zx @ (ZZinv @ (Zx.T @ Xt))
    A = np.linalg.inv(Xh.T @ Xh)
    beta = A @ (Xh.T @ yt)
    e = yt - Xt @ beta
    S = np.add.reduceat(Xh * e[:, None], starts, axis=0)
    V = c * A @ (S.T @ S) @ A
    se = np.sqrt(np.diag(V))
    t = beta / se
    dfree = G - 1
    p = 2 * stats.t.sf(np.abs(t), dfree)
    tq = stats.t.ppf(0.975, dfree)
    # F de primera etapa por endógeno (Wald cluster sobre los instrumentos excluidos)
    Fs = {}
    ki = len(inst)
    for k, nm in enumerate(endog):
        a = Zx.T @ Zx
        pi = np.linalg.solve(a, Zx.T @ Xt[:, k])
        u = Xt[:, k] - Zx @ pi
        Sg = np.add.reduceat(Zx * u[:, None], starts, axis=0)
        Vp = np.linalg.inv(a) @ (Sg.T @ Sg) @ np.linalg.inv(a) * (G / (G - 1))
        w = pi[:ki] @ np.linalg.solve(Vp[:ki, :ki], pi[:ki])
        Fs[nm] = float(w / ki)
    # J de Hansen (2 pasos) con momentos Z_x'e (instrumentos excluidos + exógenos)
    nover = ki - len(endog)
    J = dict(J=np.nan, df=nover, p=np.nan)
    if nover > 0:
        Sg = np.add.reduceat(Zx * e[:, None], starts, axis=0)
        W = np.linalg.pinv(Sg.T @ Sg)
        ZX = Zx.T @ Xt
        b2 = np.linalg.solve(ZX.T @ W @ ZX, ZX.T @ W @ (Zx.T @ yt))
        e2 = yt - Xt @ b2
        Sg2 = np.add.reduceat(Zx * e2[:, None], starts, axis=0)
        W2 = np.linalg.pinv(Sg2.T @ Sg2)
        g = Zx.T @ e2
        Jv = float(g @ W2 @ g)
        J = dict(J=Jv, df=nover, p=float(stats.chi2.sf(Jv, nover)))
    return dict(names=xs, beta=beta, se=se, t=t, p=p, lo=beta - tq * se, hi=beta + tq * se, n=n, G=G, df=dfree,
                F=Fs, J=J, muestra=(str(d[fe[-1]].min()), str(d[fe[-1]].max())), boot={})


# ------------------------------------------------------------------ registro
class Log:
    """Envoltorio del Registry de econ_utils: TODA especificación se anota aquí."""

    def __init__(self, ruta):
        self.reg = eu.Registry(ruta)
        self.n = 0

    def spec(self, fase, mid, formula, res, interes=None, notas=""):
        i = res["names"].index(interes) if interes in res["names"] else None
        pint = np.nan
        if i is not None:
            pint = res["boot"][interes]["p2"] if interes in res["boot"] else res["p"][i]
        self.reg.log(fase, mid, formula, res["muestra"][0], res["muestra"][1], res["n"], np.nan, np.nan, np.nan,
                     np.nan, res["beta"][i] if i is not None else np.nan, pint, notas + f" | G={res['G']}")
        self.n += 1

    def libre(self, fase, mid, formula, ini, fin, n, coef=np.nan, p=np.nan, rmse_oos=np.nan, notas=""):
        self.reg.log(fase, mid, formula, ini, fin, n, np.nan, np.nan, np.nan, rmse_oos, coef, p, notas)
        self.n += 1

    def flush(self):
        self.reg.flush()


def bh(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    q, prev = {}, 1.0
    for i in range(m - 1, -1, -1):
        k, p = items[i]
        prev = min(prev, p * m / (i + 1))
        q[k] = prev
    return q


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, prev = {}, 0.0
    for i, (k, p) in enumerate(items):
        prev = max(prev, min(1.0, (m - i) * p))
        out[k] = prev
    return out


# ------------------------------------------------------------------ variables H4
def preparar_h4(pa: pd.DataFrame, nq: pd.DataFrame, suelo_ini=2005, suelo_fin=2007,
                ini_col="iniciadas_libres_anual") -> pd.DataFrame:
    """Panel anual provincial con las variables de H4.
    d_ln_ini        = Δ ln iniciadas_libres_t (tabla anual MIVAU 32200500, 2002-2025; ini_col)
    d_ln_pr_l1      = Δ ln precio real_{t-1}; precio real = p_tasado / deflactor (media anual de nacional_q_v2)
    suelo_c         = ln(media p_suelo 2005-2007) - media de las provincias de entrenamiento (fijo)
    inter           = d_ln_pr_l1 * suelo_c
    Desplazadores de demanda (robustez IV): Δ ln ocupados_{t-1}, Δ ln pob_20_34_{t-1}."""
    d = pa.sort_values(["cod_prov", "anio"]).reset_index(drop=True).copy()
    d["anio"] = d["anio"].astype(int)
    d["cod_prov"] = d["cod_prov"].astype(str)
    n = nq.copy()
    n["anio"] = n["trimestre"].astype(str).str[:4].astype(int)
    g = n.groupby("anio")["deflactor"].agg(["mean", "count"])
    defl = g["mean"].where(g["count"] == 4)
    d["defl"] = d["anio"].map(defl)
    gp = d.groupby("cod_prov", sort=False)
    d["ln_pr"] = np.log(d["p_tasado"] / d["defl"])
    d["ln_pn"] = np.log(d["p_tasado"])
    d["ln_ini"] = np.log(d[ini_col].where(d[ini_col] > 0))
    for v in ("ln_pr", "ln_pn", "ln_ini"):
        d["d_" + v] = d.groupby("cod_prov", sort=False)[v].diff()
    d["d_ln_ocup"] = d.groupby("cod_prov", sort=False)["ocupados"].transform(lambda s: np.log(s).diff())
    d["d_ln_pob2034"] = d.groupby("cod_prov", sort=False)["pob_20_34"].transform(lambda s: np.log(s).diff())
    for v, nuevo in (("d_ln_pr", "d_ln_pr_l1"), ("d_ln_pr", "d_ln_pr_l2"), ("d_ln_pn", "d_ln_pn_l1"),
                     ("d_ln_ocup", "d_ln_ocup_l1"), ("d_ln_pob2034", "d_ln_pob2034_l1")):
        k = 2 if nuevo.endswith("l2") else 1
        d[nuevo] = d.groupby("cod_prov", sort=False)[v].shift(k)
    s = d[d["anio"].between(suelo_ini, suelo_fin)].groupby("cod_prov")["p_suelo"].agg(["mean", "count"])
    s = s[s["count"] == (suelo_fin - suelo_ini + 1)]["mean"]
    ls = np.log(s)
    ls_c = ls - ls.mean()                    # media de las provincias de entrenamiento con dato
    d["suelo_bar"] = d["cod_prov"].map(s)
    d["suelo_c"] = d["cod_prov"].map(ls_c)
    d["inter"] = d["d_ln_pr_l1"] * d["suelo_c"]
    d["inter_n"] = d["d_ln_pn_l1"] * d["suelo_c"]
    d["inter_l2"] = d["d_ln_pr_l2"] * d["suelo_c"]
    for z in ("d_ln_ocup_l1", "d_ln_pob2034_l1"):
        d[z + "_x"] = d[z] * d["suelo_c"]
    d.attrs["media_ln_suelo"] = float(ls.mean())
    d.attrs["n_prov_suelo"] = int(len(ls))
    return d
