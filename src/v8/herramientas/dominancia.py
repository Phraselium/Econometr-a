"""Dominancia general (LMG/Shapley del R2), pesos de Johnson, colinealidad de Belsley y ortogonalizacion secuencial.

Solo estadistica descriptiva de la descomposicion del R2: NO es atribucion causal.
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd

SEED = 20261010


def _prep(X, y):
    X = np.asarray(X, float)
    y = np.asarray(y, float).ravel()
    return X, y


def _r2_cache(X, y, players):
    """R2 de todos los subconjuntos de jugadores (cada jugador = lista de columnas). Devuelve dict frozenset->R2."""
    Xc = X - X.mean(0)
    yc = y - y.mean()
    C = Xc.T @ Xc
    c = Xc.T @ yc
    syy = float(yc @ yc)
    p = len(players)
    out = {frozenset(): 0.0}
    for r in range(1, p + 1):
        for S in itertools.combinations(range(p), r):
            cols = [j for s in S for j in players[s]]
            Css = C[np.ix_(cols, cols)]
            cs = c[cols]
            try:
                b = np.linalg.solve(Css, cs)
            except np.linalg.LinAlgError:
                b = np.linalg.lstsq(Css, cs, rcond=None)[0]
            out[frozenset(S)] = float(cs @ b) / syy
    return out


def _shapley_from_cache(cache, p):
    w = [math.factorial(k) * math.factorial(p - k - 1) / math.factorial(p) for k in range(p)]
    phi = np.zeros(p)
    for j in range(p):
        others = [i for i in range(p) if i != j]
        for r in range(p):
            for S in itertools.combinations(others, r):
                s = frozenset(S)
                phi[j] += w[r] * (cache[s | {j}] - cache[s])
    return phi


def shapley_r2(X, y, nombres=None, grupos=None, max_jugadores=10, B=0, bloque=1, seed=SEED, alpha=0.05):
    """LMG / Shapley del R2 exacto. `grupos`: dict nombre->lista de nombres/indices de columnas (jugador = grupo).

    B>0: IC percentil por bootstrap de filas (o de bloques moviles si bloque>1). Devuelve DataFrame con
    phi (aporte al R2), share (phi/R2), lo/hi. La suma de phi = R2 del modelo completo.
    """
    if isinstance(X, pd.DataFrame):
        nombres = list(X.columns) if nombres is None else nombres
        X = X.values
    X, y = _prep(X, y)
    k = X.shape[1]
    nombres = list(nombres) if nombres is not None else [f"x{i}" for i in range(k)]
    if grupos is None:
        players = [[j] for j in range(k)]
        pn = nombres
    else:
        pn = list(grupos)
        players = [[nombres.index(c) if isinstance(c, str) else int(c) for c in grupos[g]] for g in pn]
    p = len(players)
    if p > max_jugadores:
        raise ValueError(f"{p} jugadores > max {max_jugadores}: agrupa variables en familias (calculo exacto 2^p)")
    cache = _r2_cache(X, y, players)
    phi = _shapley_from_cache(cache, p)
    r2 = cache[frozenset(range(p))]
    out = pd.DataFrame({"phi": phi, "share": phi / r2}, index=pn)
    if B > 0:
        rng = np.random.default_rng(seed)
        n = len(y)
        draws = np.empty((B, p))
        for b in range(B):
            idx = _boot_idx(n, bloque, rng)
            cb = _r2_cache(X[idx], y[idx], players)
            draws[b] = _shapley_from_cache(cb, p)
        out["lo"] = np.quantile(draws, alpha / 2, axis=0)
        out["hi"] = np.quantile(draws, 1 - alpha / 2, axis=0)
        out["share_lo"] = np.quantile(draws / draws.sum(1, keepdims=True), alpha / 2, axis=0)
        out["share_hi"] = np.quantile(draws / draws.sum(1, keepdims=True), 1 - alpha / 2, axis=0)
    out.attrs["r2"] = r2
    return out


def _boot_idx(n, bloque, rng):
    if bloque <= 1:
        return rng.integers(0, n, n)
    nb = int(np.ceil(n / bloque))
    st = rng.integers(0, n - bloque + 1, nb)
    return (st[:, None] + np.arange(bloque)[None, :]).ravel()[:n]


def johnson_rw(X, y, nombres=None):
    """Pesos relativos de Johnson (2000). Suman R2. Aproximan la importancia sobre predictores ortogonales."""
    if isinstance(X, pd.DataFrame):
        nombres = list(X.columns) if nombres is None else nombres
        X = X.values
    X, y = _prep(X, y)
    Z = (X - X.mean(0)) / X.std(0, ddof=0)
    yz = (y - y.mean()) / y.std()
    U, d, Vt = np.linalg.svd(Z, full_matrices=False)
    Q = U @ Vt  # mejor aproximacion ortonormal (escalada)
    Lam = Vt.T @ np.diag(d) @ Vt / np.sqrt(len(y))
    Q = Q * np.sqrt(len(y))
    beta = Q.T @ yz / len(y)
    raw = (Lam ** 2) @ (beta ** 2)
    nombres = nombres or [f"x{i}" for i in range(X.shape[1])]
    return pd.DataFrame({"peso": raw, "share": raw / raw.sum()}, index=nombres)


def colinealidad(X, nombres=None, constante=True, umbral_ci=30.0, umbral_prop=0.5):
    """VIF, indices de condicion y proporciones de descomposicion de varianza de Belsley-Kuh-Welsch."""
    if isinstance(X, pd.DataFrame):
        nombres = list(X.columns) if nombres is None else nombres
        X = X.values
    X = np.asarray(X, float)
    k = X.shape[1]
    nombres = list(nombres) if nombres is not None else [f"x{i}" for i in range(k)]
    R = np.corrcoef(X, rowvar=False).reshape(k, k)
    vif = np.diag(np.linalg.inv(R)) if k > 1 else np.ones(1)
    A = np.column_stack([np.ones(len(X)), X]) if constante else X
    A = A / np.sqrt((A ** 2).sum(0))
    U, d, Vt = np.linalg.svd(A, full_matrices=False)
    ci = d.max() / d
    phi = (Vt.T ** 2) / d ** 2  # phi[j, k]
    prop = phi / phi.sum(1, keepdims=True)  # prop[j,k] = pi_kj
    cols = (["const"] if constante else []) + nombres
    tab = pd.DataFrame(prop.T, columns=cols)
    tab.insert(0, "indice_condicion", ci)
    flag = [(i, [c for c in cols if tab.loc[i, c] > umbral_prop]) for i in range(len(ci)) if ci[i] > umbral_ci]
    flag = [(i, v) for i, v in flag if len(v) >= 2]
    return {"vif": pd.Series(vif, index=nombres), "belsley": tab, "ci_max": float(ci.max()),
            "dependencias": [(float(ci[i]), v) for i, v in flag]}


def gram_schmidt(X, orden):
    """Ortonormaliza las columnas de X (ya centradas) siguiendo `orden` (Gram-Schmidt clasico). Devuelve Q (columnas en ese orden)."""
    X = np.asarray(X, float)
    Q = []
    for j in orden:
        v = X[:, j].copy()
        for q in Q:
            v -= (q @ X[:, j]) * q
        nv = np.linalg.norm(v)
        Q.append(v / nv if nv > 1e-12 else np.zeros_like(v))
    return np.column_stack(Q)


def r2_incremental_orden(X, y, orden):
    """R2 incremental de cada variable segun `orden` por Gram-Schmidt: (q_j'yc)^2 / yc'yc."""
    X = np.asarray(X, float)
    Xc = X - X.mean(0)
    yc = np.asarray(y, float) - np.mean(y)
    Q = gram_schmidt(Xc, orden)
    return (Q.T @ yc) ** 2 / float(yc @ yc)


def ortogonalizacion_secuencial(X, y, nombres=None, max_vars=7):
    """R2 incremental de cada variable en TODOS los ordenes (p! <= 5040 con p=7).

    Devuelve dict: por_posicion (variable x posicion: media del R2 incremental), minimo/maximo sobre ordenes,
    primero (R2 marginal cuando entra primera), ultimo (cuando entra ultima), media (= LMG).
    """
    if isinstance(X, pd.DataFrame):
        nombres = list(X.columns) if nombres is None else nombres
        X = X.values
    X, y = _prep(X, y)
    k = X.shape[1]
    if k > max_vars:
        raise ValueError(f"p={k}>{max_vars}: p! ordenes inviable; agrupa en familias")
    nombres = list(nombres) if nombres is not None else [f"x{i}" for i in range(k)]
    pos = np.zeros((k, k))
    cnt = np.zeros((k, k))
    allv = [[] for _ in range(k)]
    for perm in itertools.permutations(range(k)):
        inc = r2_incremental_orden(X, y, perm)
        for m, j in enumerate(perm):
            pos[j, m] += inc[m]
            cnt[j, m] += 1
            allv[j].append(inc[m])
    por_pos = pd.DataFrame(pos / cnt, index=nombres, columns=[f"pos{m + 1}" for m in range(k)])
    res = pd.DataFrame({"media": [np.mean(a) for a in allv], "minimo": [np.min(a) for a in allv],
                        "maximo": [np.max(a) for a in allv], "primero": por_pos.iloc[:, 0].values,
                        "ultimo": por_pos.iloc[:, -1].values}, index=nombres)
    return {"por_posicion": por_pos, "resumen": res}
