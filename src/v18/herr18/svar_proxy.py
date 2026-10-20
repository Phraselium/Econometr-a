"""V18 · SVAR con instrumento externo (proxy-SVAR) con conjuntos de confianza de Anderson-Rubin robustos a proxy débil (Montiel Olea, Stock y
Watson, 2021) por el método delta, y bootstrap de bloques como comparación. Sin lectura de datos: reciben arrays.

Modelo: VAR(p) en forma reducida Y_t = c + Σ A_l Y_{t−l} + u_t y proxy z_t con E[z_t u_t] = m (proporcional a la columna de impacto del choque
objetivo). Respuesta normalizada del variable j a horizonte h a un choque que mueve la variable `ref` una unidad en el impacto:
θ_{h,j} = Ψ_h[j, :] m / m[ref], con Ψ_h = Σ_{l=1..min(h,p)} A_l Ψ_{h−l} (Ψ_0 = I).
Contraste AR de θ = θ0: g(θ0) = Ψ_h[j, :] m̂ − θ0 m̂[ref], con varianza por el método delta sobre las influencias conjuntas de (A, m); g es lineal
en θ0 y su varianza cuadrática: se reutiliza la forma cerrada de lp_iv (Fieller).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herr18 import lp_iv as L  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"


def var_ols(Y: np.ndarray, p: int):
    """Devuelve (A (n, 1 + n p) con la constante primero, U (T−p, n), X (T−p, 1 + n p))."""
    T, n = Y.shape
    X = np.column_stack([np.ones(T - p)] + [Y[p - l:T - l] for l in range(1, p + 1)])
    B = np.linalg.lstsq(X, Y[p:], rcond=None)[0].T
    return B, Y[p:] - X @ B.T, X


def psi(Als: np.ndarray, h: int) -> np.ndarray:
    """Ψ_h para un lote de matrices de coeficientes Als (..., p, n, n): devuelve (..., n, n)."""
    p = Als.shape[-3]
    n = Als.shape[-1]
    P = [np.broadcast_to(np.eye(n), Als.shape[:-3] + (n, n)).copy()]
    for k in range(1, h + 1):
        s = np.zeros_like(P[0])
        for l in range(1, min(k, p) + 1):
            s = s + Als[..., l - 1, :, :] @ P[k - l]
        P.append(s)
    return P[h]


def _lags(B: np.ndarray, p: int) -> np.ndarray:
    n = B.shape[0]
    return np.stack([B[:, 1 + l * n:1 + (l + 1) * n] for l in range(p)])


def proxy_svar(Y: np.ndarray, z: np.ndarray, p: int, h: int, j: int, ref: int = 0, L_hac: int = 4) -> dict:
    """Estima θ_{h,j} y arma el objeto r (formato de lp_iv) para el contraste AR y el t por método delta."""
    T, n = Y.shape
    B, U, X = var_ols(Y, p)
    Te = len(U)
    zz = z[p:] - z[p:].mean()
    m = (zz[:, None] * U).mean(0)
    Als = _lags(B, p)
    a_val = float(psi(Als, h)[j, :] @ m)
    b_val = float(m[ref])
    # gradiente numérico de Ψ_h[j,:] m respecto de los coeficientes de rezago (lote de perturbaciones centradas)
    flat = Als.reshape(-1)
    K = len(flat)
    eps = 1e-5
    E = np.eye(K) * eps
    mas = (flat[None, :] + E).reshape(K, p, n, n)
    menos = (flat[None, :] - E).reshape(K, p, n, n)
    grad = (psi(mas, h)[:, j, :] @ m - psi(menos, h)[:, j, :] @ m) / (2 * eps)       # (K,)
    # influencias: A por MCO, m por el momento
    Q_inv = np.linalg.inv(X.T @ X / Te)
    XQ = X @ Q_inv                                                                    # (Te, k)
    k = X.shape[1]
    # IF de A (n, k): u_t ⊗ Q^-1 x_t ; solo los coeficientes de rezago (columnas 1..)
    IFA = (U[:, :, None] * XQ[:, None, :])[:, :, 1:]                                 # (Te, n, n p)
    IFA = IFA.reshape(Te, n, p, n).transpose(0, 2, 1, 3).reshape(Te, K)               # orden (l, fila, col) como Als.reshape(-1)
    IFm = zz[:, None] * U - m[None, :]
    alpha = IFA @ grad + IFm @ psi(Als, h)[j, :]
    beta = IFm[:, ref]
    s = np.column_stack([alpha, beta])
    Om = L.lrv(s, L_hac)
    r = {"a": a_val * Te, "b": b_val * Te, "Om": Om, "n": Te, "beta": a_val / b_val if abs(b_val) > 1e-300 else np.nan, "m": m, "Als": Als}
    return r


def theta_verdadero(Als: np.ndarray, b_imp: np.ndarray, h: int, j: int, ref: int = 0) -> float:
    return float(psi(Als, h)[j, :] @ b_imp / b_imp[ref])
