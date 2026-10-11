"""K2 (v6.1): utilidades de estimacion. EF por proyecciones alternas, MCO/2SLS con errores agrupados, BMA aproximado con BIC.

Sin red, sin aleatoriedad, un solo hilo. Todo C4 (asociacion).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import itertools

import numpy as np
import pandas as pd
from scipy import stats


def _codes(s):
    return pd.factorize(pd.Series(s))[0]


def demean(V, unit, anio, fe, it=1000, tol=1e-10):
    """Residualiza columnas de V (n x k) sobre los EF pedidos.

    fe: 'pooled' (constante), 'unidad', 'anio', 'dobles' (unidad + anio), 'dobles_tend' (+ tendencia por unidad).
    Devuelve (V residualizada, grados de libertad absorbidos).
    """
    V = np.asarray(V, float).copy()
    if V.ndim == 1:
        V = V[:, None]
    n = len(V)
    u, a = _codes(unit), _codes(anio)
    nu, na = u.max() + 1, a.max() + 1
    if fe == "pooled":
        return V - V.mean(axis=0), 1
    groups = []
    if fe in ("unidad", "dobles", "dobles_tend"):
        groups.append((u, nu))
    if fe in ("anio", "dobles", "dobles_tend"):
        groups.append((a, na))
    t = np.asarray(anio, float)
    tc = t - (np.bincount(u, weights=t) / np.bincount(u))[u] if fe == "dobles_tend" else None
    den = np.bincount(u, weights=tc ** 2) if tc is not None else None
    for j in range(V.shape[1]):
        v = V[:, j]
        for _ in range(it):
            v0 = v.copy()
            for g, ng in groups:
                v = v - (np.bincount(g, weights=v, minlength=ng) / np.bincount(g, minlength=ng))[g]
            if tc is not None:
                sl = np.bincount(u, weights=tc * v) / np.where(den == 0, np.nan, den)
                v = v - tc * np.nan_to_num(sl)[u]
            if np.abs(v - v0).max() < tol:
                break
        V[:, j] = v
    kfe = {"unidad": nu, "anio": na, "dobles": nu + na - 1, "dobles_tend": 2 * nu + na - 1}[fe]
    return V, kfe


def _cluster_cov(Xh, X, e, cl, kfe):
    cls = _codes(cl)
    G = cls.max() + 1
    n, k = X.shape
    sc = np.zeros((G, Xh.shape[1]))
    np.add.at(sc, cls, Xh * e[:, None])
    f = G / max(G - 1, 1) * (n - 1) / max(n - kfe - k, 1)
    return f * (sc.T @ sc), G


def fit(m, y, xs, ctrl=(), fe="dobles", z=None, unit="cod", anio="anio", cl="cod", extra=None):
    """MCO o 2SLS (si z) con EF y errores agrupados CR1, t(G-1). xs[0] es la variable de interes.

    extra: DataFrame con controles adicionales (ya alineado a m). Devuelve dict con coef, se, p, ic95, N, G, F1 y
    la tabla completa de coeficientes (dict nombre -> (b, se, p))."""
    cols = list(xs) + list(ctrl)
    ex_names = list(extra.columns) if extra is not None else []
    need = [y, unit, anio, cl] + cols + ([z] if z else [])
    mm = m.dropna(subset=need).reset_index(drop=True)
    ex = extra.loc[m.dropna(subset=need).index].reset_index(drop=True) if extra is not None else None
    X = mm[cols].to_numpy(float)
    if ex is not None:
        X = np.hstack([X, ex.to_numpy(float)])
    names = cols + ex_names
    Y = mm[y].to_numpy(float)
    A = [Y] + [X[:, j] for j in range(X.shape[1])]
    Zc = []
    if z:
        Zc = [mm[z].to_numpy(float)]
    allv = np.column_stack(A + Zc)
    R, kfe = demean(allv, mm[unit], mm[anio], fe)
    yt, Xt = R[:, 0], R[:, 1:1 + X.shape[1]]
    # columnas de controles degeneradas tras residualizar (rango): se descartan
    keep = [0] + [j for j in range(1, Xt.shape[1]) if Xt[:, j].std() > 1e-9]
    Xt = Xt[:, keep]
    kn = [names[j] for j in keep]
    if kn[0] != names[0]:
        return None
    n = len(yt)
    F1 = np.nan
    if z:
        zt = R[:, -1]
        Zt = np.column_stack([zt, Xt[:, 1:]])
        Pz = Zt @ np.linalg.pinv(Zt.T @ Zt) @ Zt.T
        Xh = Pz @ Xt
        b = np.linalg.pinv(Xh.T @ Xt) @ (Xh.T @ yt)
        e = yt - Xt @ b
        A_ = np.linalg.pinv(Xh.T @ Xt)
        S, G = _cluster_cov(Xh, Xt, e, mm[cl], kfe)
        V = A_ @ S @ A_.T
        # F de primera etapa (cluster) del instrumento excluido
        pi = np.linalg.pinv(Zt.T @ Zt) @ Zt.T @ Xt[:, 0]
        u1 = Xt[:, 0] - Zt @ pi
        S1, _ = _cluster_cov(Zt, Zt, u1, mm[cl], kfe)
        Ai = np.linalg.pinv(Zt.T @ Zt)
        V1 = Ai @ S1 @ Ai.T
        F1 = float(pi[0] ** 2 / V1[0, 0])
    else:
        XtX = np.linalg.pinv(Xt.T @ Xt)
        b = XtX @ Xt.T @ yt
        e = yt - Xt @ b
        S, G = _cluster_cov(Xt, Xt, e, mm[cl], kfe)
        V = XtX @ S @ XtX
    se = np.sqrt(np.clip(np.diag(V), 1e-300, None))
    dfree = max(G - 1, 1)
    p = 2 * stats.t.sf(np.abs(b / se), dfree)
    tc = stats.t.ppf(0.975, dfree)
    return dict(coef=float(b[0]), se=float(se[0]), p=float(p[0]), lo=float(b[0] - tc * se[0]),
                hi=float(b[0] + tc * se[0]), N=int(n), G=int(G), F1=F1,
                tabla={k: (float(b[i]), float(se[i]), float(p[i])) for i, k in enumerate(kn)}, Xt=Xt, kn=kn, yt=yt)


def vif_within(m, cols, fe="dobles", unit="cod", anio="anio"):
    """VIF de cada columna con EF absorbidos (regresion de cada columna sobre las demas, residualizadas)."""
    mm = m.dropna(subset=list(cols) + [unit, anio])
    R, _ = demean(mm[list(cols)].to_numpy(float), mm[unit], mm[anio], fe)
    out = {}
    for j, c in enumerate(cols):
        o = [i for i in range(len(cols)) if i != j]
        if not o:
            out[c] = 1.0
            continue
        b = np.linalg.lstsq(R[:, o], R[:, j], rcond=None)[0]
        r2 = 1 - ((R[:, j] - R[:, o] @ b) ** 2).sum() / (R[:, j] ** 2).sum()
        out[c] = float(1 / (1 - r2))
    return out, len(mm)


def corr_tipos(m, a, b, unit="cod", anio="anio"):
    """Correlacion de a y b: conjunta (pooled), entre unidades (medias) y dentro (EF dobles)."""
    mm = m.dropna(subset=[a, b, unit, anio])
    pooled = float(np.corrcoef(mm[a], mm[b])[0, 1])
    g = mm.groupby(unit)[[a, b]].mean()
    entre = float(np.corrcoef(g[a], g[b])[0, 1])
    R, _ = demean(mm[[a, b]].to_numpy(float), mm[unit], mm[anio], "dobles")
    dentro = float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])
    return dict(pooled=pooled, entre=entre, dentro=dentro, N=len(mm))


def bma_bic(m, y, xs, fe="dobles", unit="cod", anio="anio", forzadas=()):
    """BMA aproximado con BIC (pesos exp(-BIC/2), prior uniforme sobre modelos) sobre datos residualizados por EF.

    Devuelve PIP y media posterior del coeficiente de cada variable (en unidades de y por unidad de x)."""
    cols = list(xs)
    mm = m.dropna(subset=[y, unit, anio] + cols)
    R, kfe = demean(mm[[y] + cols].to_numpy(float), mm[unit], mm[anio], fe)
    yt, X = R[:, 0], R[:, 1:]
    n, K = X.shape
    G = X.T @ X
    c = X.T @ yt
    yy = float(yt @ yt)
    fz = [cols.index(f) for f in forzadas]
    libres = [j for j in range(K) if j not in fz]
    bics, betas, incl = [], [], []
    for r in range(len(libres) + 1):
        for sub in itertools.combinations(libres, r):
            idx = list(fz) + list(sub)
            if idx:
                bb = np.linalg.solve(G[np.ix_(idx, idx)] + 1e-10 * np.eye(len(idx)), c[idx])
                rss = yy - float(c[idx] @ bb)
            else:
                bb, rss = np.array([]), yy
            k = len(idx) + kfe
            bics.append(n * np.log(max(rss, 1e-12) / n) + k * np.log(n))
            full = np.zeros(K)
            full[idx] = bb
            betas.append(full)
            inc = np.zeros(K, bool)
            inc[idx] = True
            incl.append(inc)
    bics = np.array(bics)
    w = np.exp(-(bics - bics.min()) / 2)
    w /= w.sum()
    B = np.array(betas)
    I = np.array(incl)
    pip = (w[:, None] * I).sum(axis=0)
    mean = (w[:, None] * B).sum(axis=0)
    return {c_: dict(pip=float(pip[i]), media=float(mean[i])) for i, c_ in enumerate(cols)}, n, 2 ** len(libres)


def holm_dict(p):
    items = sorted(p.items(), key=lambda kv: kv[1])
    mm, out, run = len(items), {}, 0.0
    for i, (k, v) in enumerate(items):
        run = max(run, min(1.0, (mm - i) * v))
        out[k] = run
    return out


def bh_dict(p):
    items = sorted(p.items(), key=lambda kv: kv[1])
    mm = len(items)
    out, prev = {}, 1.0
    for i in range(mm - 1, -1, -1):
        k, v = items[i]
        prev = min(prev, v * mm / (i + 1))
        out[k] = prev
    return out
