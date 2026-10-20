"""V18 · fase 4 · E7-R3 y E7-A1: BVAR recursivo con prior de Minnesota (conjugada normal-Wishart inversa por observaciones ficticias).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md 1.7, R3 y A1; adenda R-27).
Sin datos: solo funciones (las usan src/v18/estimacion/e7_bvar.py y el Monte Carlo src/v18/montecarlo/bvar.py).

Modelo: y_t = c + A_1 y_{t-1} + ... + A_p y_{t-p} + d_t' s + u_t, u_t ~ N(0, Σ), con d_t las tres ficticias estacionales centradas.
Prior de Minnesota (Bańbura, Giannone y Reichlin, 2010; Sims y Zha, 1998) como observaciones ficticias:
  - estrechez general λ (propia y cruzada con el mismo λ, decaimiento por rezago l^2), media del primer rezago propio γ_i;
  - suma de coeficientes (Doan, Litterman y Sims, 1984) con peso μ = 1/τ (τ = 10 λ; μ = 0 la desactiva), sobre la media inicial en logaritmos;
  - a priori impropio sobre (B, Σ) |Σ|^{-(n+1)/2}, de modo que el posterior con las observaciones ficticias es normal-Wishart inversa:
    Σ | datos ~ IW(S, T* − k); vec(B) | Σ ~ N(vec(B̃), Σ ⊗ (X*'X*)^{-1}), con T* = T + T_ficticias.
Identificación recursiva: Cholesky de Σ en el orden de las columnas; la respuesta se normaliza por el impacto del propio choque en su variable (+1 unidad
en la variable del choque en el momento del impacto), de modo que «por +100 pb» es +1 pp si la variable del choque está en puntos porcentuales.
"""
from __future__ import annotations

import numpy as np

SEED = 20261010
ALCANCE = "sin lectura de datos"


def rezagos_y_resp(Y: np.ndarray, p: int, estacional: np.ndarray | None):
    """Y (T, n) con NaN posibles. Devuelve (y_t (T-p, n), X (T-p, k), índice t de cada fila). X = [rezagos 1..p, constante, estacionales]."""
    T, n = Y.shape
    t = np.arange(p, T)
    cols = [Y[t - l] for l in range(1, p + 1)]
    cols.append(np.ones((len(t), 1)))
    if estacional is not None:
        cols.append(estacional[t])
    return Y[t], np.hstack(cols), t


def ficticias_estacionales(trimestres: np.ndarray) -> np.ndarray:
    """Tres ficticias estacionales centradas (Q2, Q3, Q4 menos 1/4) a partir del número de trimestre (1..4) de cada fila."""
    q = np.asarray(trimestres)
    return np.column_stack([(q == k).astype(float) - 0.25 for k in (2, 3, 4)])


def sigma_ar1(Y: np.ndarray) -> np.ndarray:
    """Desviación típica del residuo de un AR(1) con constante de cada serie (escala del prior de Minnesota), con los NaN omitidos."""
    out = np.empty(Y.shape[1])
    for i in range(Y.shape[1]):
        y = Y[:, i]
        ok = np.isfinite(y[1:]) & np.isfinite(y[:-1])
        x, z = y[:-1][ok], y[1:][ok]
        Z = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(Z, z, rcond=None)[0]
        out[i] = np.std(z - Z @ b, ddof=2)
    return out


def ficticias(n: int, p: int, k_extra: int, sig: np.ndarray, ybar: np.ndarray, gamma: np.ndarray, lam: float, mu: float):
    """Observaciones ficticias (Yd, Xd) de Minnesota y de suma de coeficientes; k = n p + 1 + k_extra regresores."""
    k = n * p + 1 + k_extra
    Yd, Xd = [], []
    # Minnesota: coeficientes de rezago l de la variable j en la ecuación i ~ N(γ_i 1{l=1, i=j}, (λ σ_i/(l σ_j))^2)
    for l in range(1, p + 1):
        y = np.zeros((n, n))
        x = np.zeros((n, k))
        if l == 1:
            y = np.diag(gamma * sig) / lam
        x[:, (l - 1) * n:l * n] = np.diag(sig) * l / lam
        Yd.append(y)
        Xd.append(x)
    # cov. de los residuos: prior diag(σ^2)
    Yd.append(np.diag(sig))
    Xd.append(np.zeros((n, k)))
    # constante y estacionales: prior casi plano
    Yd.append(np.zeros((1, n)))
    x = np.zeros((1, k))
    x[0, n * p] = 1e-6
    Xd.append(x)
    if k_extra:
        for j in range(k_extra):
            x = np.zeros((1, k))
            x[0, n * p + 1 + j] = 1e-6
            Yd.append(np.zeros((1, n)))
            Xd.append(x)
    if mu > 0:
        Ysc = np.diag(gamma * ybar * mu)
        Xsc = np.zeros((n, k))
        for l in range(1, p + 1):
            Xsc[:, (l - 1) * n:l * n] = np.diag(ybar * mu)
        Yd.append(Ysc)
        Xd.append(Xsc)
    return np.vstack(Yd), np.vstack(Xd)


def posterior(y: np.ndarray, X: np.ndarray, Yd: np.ndarray, Xd: np.ndarray) -> dict:
    Ys, Xs = np.vstack([y, Yd]), np.vstack([X, Xd])
    XtX = Xs.T @ Xs
    B = np.linalg.solve(XtX, Xs.T @ Ys)
    E = Ys - Xs @ B
    S = E.T @ E
    return {"B": B, "S": (S + S.T) / 2, "XtXinv": np.linalg.inv(XtX), "nu": Xs.shape[0] - Xs.shape[1], "n": y.shape[1], "k": X.shape[1], "Tn": len(y)}


def sacar(post: dict, D: int, rng: np.random.Generator):
    """D extracciones (B, Σ) del posterior normal-Wishart inversa. B (D, k, n), Σ (D, n, n)."""
    n, k, nu = post["n"], post["k"], post["nu"]
    Sinv = np.linalg.inv(post["S"])
    L = np.linalg.cholesky(Sinv)
    A = np.zeros((D, n, n))
    ch = np.sqrt(rng.chisquare(nu - np.arange(n), size=(D, n)))
    A[:, np.arange(n), np.arange(n)] = ch
    low = np.tril_indices(n, -1)
    A[:, low[0], low[1]] = rng.standard_normal((D, len(low[0])))
    LA = L[None] @ A
    W = LA @ LA.transpose(0, 2, 1)                       # Wishart(ν, S^{-1})
    Sig = np.linalg.inv(W)
    Sig = (Sig + Sig.transpose(0, 2, 1)) / 2
    CS = np.linalg.cholesky(Sig)
    CX = np.linalg.cholesky(post["XtXinv"])
    Z = rng.standard_normal((D, k, n))
    Bd = post["B"][None] + CX[None] @ Z @ CS.transpose(0, 2, 1)
    return Bd, Sig


def irf(Bd: np.ndarray, Sig: np.ndarray, n: int, p: int, hmax: int, j: int, normalizar: bool = True) -> np.ndarray:
    """Respuestas (D, hmax+1, n) de cada variable a un choque recursivo (Cholesky, orden de las columnas) en la variable j.
    Con normalizar, el impacto del choque en la variable j es +1."""
    D = Bd.shape[0]
    A = [Bd[:, l * n:(l + 1) * n, :].transpose(0, 2, 1) for l in range(p)]      # A_l (D, n, n): y_t = Σ A_l y_{t-l}
    P = np.linalg.cholesky(Sig)
    imp = P[:, :, j]
    if normalizar:
        imp = imp / P[:, j, j][:, None]
    Psi = [np.broadcast_to(np.eye(n), (D, n, n)).copy()]
    for s in range(1, hmax + 1):
        acc = np.zeros((D, n, n))
        for l in range(1, min(s, p) + 1):
            acc += A[l - 1] @ Psi[s - l]
        Psi.append(acc)
    return np.stack([(Ps @ imp[:, :, None])[:, :, 0] for Ps in Psi], axis=1)


def raiz_maxima(Bd: np.ndarray, n: int, p: int) -> np.ndarray:
    """Mayor módulo de las raíces de la matriz companion de cada extracción."""
    D = Bd.shape[0]
    C = np.zeros((D, n * p, n * p))
    for l in range(p):
        C[:, :n, l * n:(l + 1) * n] = Bd[:, l * n:(l + 1) * n, :].transpose(0, 2, 1)
    if p > 1:
        C[:, n:, :-n] = np.eye(n * (p - 1))[None]
    return np.abs(np.linalg.eigvals(C)).max(1)


def ajustar(Y: np.ndarray, trimestre: np.ndarray | None, p: int, lam: float, mu: float, gamma: np.ndarray,
            omitir: np.ndarray | None = None, unidad: np.ndarray | None = None) -> dict:
    """Ajusta el BVAR a Y (T, n; NaN permitidos: las filas con algún NaN en la variable dependiente o en sus rezagos se omiten).
    `omitir` (T,) bool: observaciones cuya fila de regresión se omite (los rezagos usan los valores reales). `unidad` (n,): divisor de la media inicial en la
    ficticia de suma de coeficientes (100 para las series en 100 log: la convención de Bańbura et al. es en logaritmos). Devuelve el posterior y el recuento de filas."""
    n = Y.shape[1]
    est = ficticias_estacionales(trimestre) if trimestre is not None else None
    y, X, t = rezagos_y_resp(Y, p, est)
    ok = np.isfinite(y).all(1) & np.isfinite(X).all(1)
    if omitir is not None:
        ok &= ~omitir[t]
    sig = sigma_ar1(Y)
    ybar = np.nanmean(Y[: max(p, 4)], axis=0)          # media de las primeras observaciones (Bańbura et al., 2010)
    if unidad is not None:
        ybar = ybar / unidad
    Yd, Xd = ficticias(n, p, 0 if est is None else est.shape[1], sig, ybar, gamma, lam, mu)
    post = posterior(y[ok], X[ok], Yd, Xd)
    post["filas"] = int(ok.sum())
    post["t_filas"] = t[ok]
    return post
