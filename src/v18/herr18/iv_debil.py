"""V18 · IV con instrumentos débiles: F efectivo de Montiel Olea-Pflueger (MOP) e intervalos Anderson-Rubin (AR) por cluster.

Sin lectura de datos: recibe arrays. Una o dos endógenas (p = 1 o 2) y k instrumentos; la constante se parcializa.
- f_efectivo: F efectivo de MOP por regresor endógeno, con la primera etapa de ese regresor sobre los k instrumentos y varianza
  robusta por cluster (F_eff = pi' Z'Z pi / tr(Sigma_pi Z'Z); con k = 1 es el F robusto).
- ar_estadistico / ar_p: AR conjunto con varianza por cluster (chi2 con k grados), G/(G-1).
- ar_ic_1: IC AR exacto con p = 1 (la desigualdad es cuadrática en beta): intervalo, complemento de intervalo o recta.
- ar_subvector_p: p-valor de AR de subvector (proyección) para beta_1 con p = 2 y k = 2 (mínimo sobre beta_2 en rejilla fina).
"""
from __future__ import annotations

import numpy as np
from scipy import stats

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"


def _centrar(A):
    A = np.asarray(A, float)
    return A - A.mean(axis=0, keepdims=True)


def _suma_cluster(M, cl, G):
    """Suma por cluster de las filas de M (n, ...) -> (G, ...)."""
    out = np.zeros((G,) + M.shape[1:])
    np.add.at(out, cl, M)
    return out


def preparar(y, X, Z, cl):
    y = _centrar(np.asarray(y, float).reshape(-1, 1))[:, 0]
    X = _centrar(np.asarray(X, float).reshape(len(y), -1))
    Z = _centrar(np.asarray(Z, float).reshape(len(y), -1))
    cl = np.asarray(cl)
    G = int(cl.max()) + 1
    return y, X, Z, cl, G


def f_efectivo(X, Z, cl, G):
    """F efectivo de MOP para cada columna de X (vector de longitud p)."""
    ZZ = Z.T @ Z
    ZZi = np.linalg.inv(ZZ)
    out = []
    for j in range(X.shape[1]):
        x = X[:, j]
        pi = ZZi @ (Z.T @ x)
        e = x - Z @ pi
        S = _suma_cluster(Z * e[:, None], cl, G)
        meat = S.T @ S * G / (G - 1)
        Vpi = ZZi @ meat @ ZZi
        out.append(float(pi @ ZZ @ pi / np.trace(Vpi @ ZZ)))
    return np.array(out)


def dos_sls(y, X, Z, cl, G):
    """2SLS con varianza por cluster (G/(G-1)). Devuelve (beta (p,), V (p,p))."""
    Pz = Z @ np.linalg.solve(Z.T @ Z, Z.T)
    Xh = Pz @ X
    A = np.linalg.inv(Xh.T @ X)
    beta = A @ (Xh.T @ y)
    e = y - X @ beta
    S = _suma_cluster(Xh * e[:, None], cl, G)
    V = A @ (S.T @ S * G / (G - 1)) @ A
    return beta, V


def sumas_ar(y, X, Z, cl, G):
    """Sumas por cluster A_g = Z_g'y_g (k) y C_g = Z_g'X_g (k, p): permiten evaluar AR(b) para cualquier b."""
    A = _suma_cluster(Z * y[:, None], cl, G)
    C = _suma_cluster(Z[:, :, None] * X[:, None, :], cl, G)
    return A, C


def ar_estadistico(A, C, b, G):
    """AR(b) = g' V^{-1} g con g = sum_g (A_g - C_g b) y V = G/(G-1) sum_g s_g s_g'. b: (p,) o (p, M)."""
    b = np.asarray(b, float)
    if b.ndim == 1:
        b = b[:, None]
    S = A[:, :, None] - np.einsum("gkp,pm->gkm", C, b)      # (G, k, M)
    g = S.sum(axis=0)                                         # (k, M)
    V = np.einsum("gkm,glm->klm", S, S) * G / (G - 1)         # (k, k, M)
    k, M = g.shape
    out = np.empty(M)
    for m in range(M):
        try:
            out[m] = g[:, m] @ np.linalg.solve(V[:, :, m] + 1e-300 * np.eye(k), g[:, m])
        except np.linalg.LinAlgError:
            out[m] = np.inf
    return out


def ar_p(A, C, b, G):
    k = A.shape[1]
    return float(stats.chi2.sf(ar_estadistico(A, C, b, G)[0], k))


def ar_ic_1(A, C, G, alfa=0.05):
    """IC AR (p = 1, k = 1) exacto. Devuelve (tipo, a, b): 'intervalo' (a, b), 'complemento' (a, b) = recta menos (a, b)
    [conjunto no acotado], o 'recta' (todo R). El conjunto es {beta: AR(beta) <= q}."""
    a = A[:, 0]
    c = C[:, 0, 0]
    q = stats.chi2.ppf(1 - alfa, 1) * G / (G - 1)   # (sum a - b sum c)^2 <= q' sum (a_g - b c_g)^2 con q' = chi2 * G/(G-1)
    # AR(b) = (sum(a) - b sum(c))^2 / (G/(G-1) sum (a_g - b c_g)^2) <= chi2  <=>  (..)^2 <= chi2 G/(G-1) sum(..)^2
    qq = q
    c2 = c.sum() ** 2 - qq * np.sum(c ** 2)
    c1 = -2 * (a.sum() * c.sum() - qq * np.sum(a * c))
    c0 = a.sum() ** 2 - qq * np.sum(a ** 2)
    if abs(c2) < 1e-14:
        if abs(c1) < 1e-14:
            return ("recta", -np.inf, np.inf) if c0 <= 0 else ("vacio", np.nan, np.nan)
        r = -c0 / c1
        return ("complemento", r, r) if c1 > 0 else ("complemento", r, r)   # semirrecta: se trata como no acotado
    disc = c1 ** 2 - 4 * c2 * c0
    if disc < 0:
        return ("recta", -np.inf, np.inf) if c2 < 0 else ("vacio", np.nan, np.nan)
    r1, r2 = sorted(((-c1 - np.sqrt(disc)) / (2 * c2), (-c1 + np.sqrt(disc)) / (2 * c2)))
    return ("intervalo", r1, r2) if c2 > 0 else ("complemento", r1, r2)


def ar_en_ic_1(ic, b):
    tipo, lo, hi = ic
    if tipo == "recta":
        return True
    if tipo == "vacio":
        return False
    if tipo == "intervalo":
        return lo <= b <= hi
    return not (lo < b < hi)


def ar_subvector_p(A, C, G, b1, rango=60.0):
    """p-valor de AR de subvector para H0: beta_1 = b1 con p = 2, k = 2 (proyección sobre beta_2: mínimo de AR en rejilla; chi2 con k = 2)."""
    k = A.shape[1]
    t = np.sinh(np.linspace(-np.arcsinh(rango), np.arcsinh(rango), 241))
    B = np.vstack([np.full_like(t, b1), t])
    v = ar_estadistico(A, C, B, G)
    i = int(np.argmin(v))
    lo, hi = t[max(i - 1, 0)], t[min(i + 1, len(t) - 1)]
    t2 = np.linspace(lo, hi, 121)
    v2 = ar_estadistico(A, C, np.vstack([np.full_like(t2, b1), t2]), G)
    return float(stats.chi2.sf(min(v.min(), v2.min()), k))
