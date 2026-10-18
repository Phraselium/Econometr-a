"""V15-A · regresión de panel con efectos fijos de dos vías (iteración de desmedias), error agrupado y error de Conley (núcleo de Bartlett).

El Conley sigue la fórmula validada en src/v16/montecarlo/conley_seccion.py (APTO solo en su escenario principal: corte transversal,
efectos fijos de municipio). Aquí se extiende al panel T = 4 sumando las puntuaciones por sección en el tiempo; no está validado como tal (DV15-A, A5).
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
from scipy.spatial import cKDTree


def demean_2fe(a: np.ndarray, g1: np.ndarray, g2: np.ndarray, it: int = 200, tol: float = 1e-10) -> np.ndarray:
    """Quita dos efectos fijos (códigos enteros g1, g2) por proyecciones alternas. a: (n,) o (n,k)."""
    a = np.array(a, dtype=float, copy=True)
    if a.ndim == 1:
        a = a[:, None]
    n1, n2 = g1.max() + 1, g2.max() + 1
    c1, c2 = np.bincount(g1, minlength=n1).astype(float), np.bincount(g2, minlength=n2).astype(float)
    for _ in range(it):
        prev = a.copy()
        for g, c, m in ((g1, c1, n1), (g2, c2, n2)):
            s = np.zeros((m, a.shape[1]))
            np.add.at(s, g, a)
            a -= (s / c[:, None])[g]
        if np.max(np.abs(a - prev)) < tol:
            break
    return a


def matriz_conley(xyz: np.ndarray, corte_km: float = 2.0) -> sp.csr_matrix:
    tree = cKDTree(xyz)
    D = tree.sparse_distance_matrix(tree, corte_km, output_type="coo_matrix")
    n = len(xyz)
    idx = np.arange(n)
    m = D.row != D.col  # la diagonal ya viene en D (distancia 0): se toma una sola vez (corrección K16)
    ii = np.concatenate([D.row[m], idx])
    jj = np.concatenate([D.col[m], idx])
    dd = np.concatenate([D.data[m], np.zeros(n)])
    return sp.csr_matrix((np.maximum(0.0, 1 - dd / corte_km), (ii, jj)), shape=(n, n))


def ols_fe(y, X, fe_sec, fe_grp, cl_mun, sec_of_obs=None, K=None, nombres=None):
    """MCO con dos efectos fijos. Devuelve coeficientes, EE agrupados por municipio y EE de Conley (si K).

    sec_of_obs: índice (0..S-1) de la sección de cada observación (para sumar puntuaciones por sección); K: matriz (S, S) de Conley.
    """
    X = np.atleast_2d(X.T).T if X.ndim == 1 else X
    Z = demean_2fe(np.column_stack([y, X]), fe_sec, fe_grp)
    yt, Xt = Z[:, 0], Z[:, 1:]
    XtX = Xt.T @ Xt
    inv = np.linalg.inv(XtX)
    b = inv @ (Xt.T @ yt)
    e = yt - Xt @ b
    s_obs = Xt * e[:, None]
    # agrupado por municipio
    G = cl_mun.max() + 1
    cs = np.zeros((G, X.shape[1]))
    np.add.at(cs, cl_mun, s_obs)
    Vg = inv @ (cs.T @ cs) * G / (G - 1) @ inv
    out = {"b": b, "se_mun": np.sqrt(np.diag(Vg)), "n": len(y), "ssr": float(e @ e), "tss": float(((y - y.mean()) ** 2).sum()), "resid": e,
           "n_fe": int(fe_sec.max() + 1 + fe_grp.max() + 1), "n_clusters": int(G)}
    if K is not None:
        S = K.shape[0]
        ss = np.zeros((S, X.shape[1]))
        np.add.at(ss, sec_of_obs, s_obs)
        M = ss.T @ (K @ ss)
        Vc = inv @ M @ inv
        d = np.diag(Vc)
        out["se_conley"] = np.where(d > 0, np.sqrt(np.maximum(d, 0)), np.nan)
        out["conley_var_no_positiva"] = bool(np.any(d <= 0))
    return out


def moran_I(res_sec: np.ndarray, xyz: np.ndarray, corte_km: float = 2.0) -> float:
    """I de Moran del vector res_sec con pesos de distancia inversa truncada a corte_km, filas normalizadas (solo el estadístico)."""
    tree = cKDTree(xyz)
    D = tree.sparse_distance_matrix(tree, corte_km, output_type="coo_matrix")
    m = D.row != D.col
    w = 1.0 / np.maximum(D.data[m], 0.05)
    W = sp.csr_matrix((w, (D.row[m], D.col[m])), shape=(len(res_sec), len(res_sec)))
    rs = np.asarray(W.sum(axis=1)).ravel()
    con = rs > 0
    W = sp.diags(np.where(con, 1 / np.where(con, rs, 1), 0)) @ W
    z = res_sec - res_sec.mean()
    return float(len(z) / W.sum() * (z @ (W @ z)) / (z @ z))
