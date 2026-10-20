"""V18 · wild cluster bootstrap con pesos de Webb para TWFE (panel balanceado), con H0 impuesta (WCR).

Sin lectura de datos: recibe arrays (G clusters x T periodos). El bootstrap usa el teorema de Frisch-Waugh:
con H0: beta = beta0 impuesta, los residuos restringidos son la desviación a efectos fijos de y - beta0 D, y
D-tilde (D sin efectos de unidad y de tiempo) no cambia entre réplicas, de modo que cada réplica es una
desmedia a dos vías vectorizada. Estadístico: t con varianza CR1 por cluster (unidad). p simétrico.
"""
from __future__ import annotations

import numpy as np

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def desmedia2(A):
    """Desmedia a dos vías sobre los dos últimos ejes (G, T): A - media_t - media_g + media."""
    return A - A.mean(axis=-1, keepdims=True) - A.mean(axis=-2, keepdims=True) + A.mean(axis=(-2, -1), keepdims=True)


def twfe_crve(y, D):
    """TWFE por MCO con CR1 por unidad. Devuelve (beta, se, Dt, e) con CR1 = G/(G-1) (N-1)/(N-K), K = 1 + (T-1)."""
    G, T = y.shape
    Dt = desmedia2(D)
    yt = desmedia2(y)
    sdd = float((Dt ** 2).sum())
    beta = float((Dt * yt).sum() / sdd)
    e = yt - beta * Dt
    sc = (Dt * e).sum(axis=1)
    N, K = G * T, T
    c = G / (G - 1) * (N - 1) / (N - K)
    se = float(np.sqrt(c * np.sum(sc ** 2)) / sdd)
    return beta, se, Dt, e


def wcr_webb(y, D, beta0, B, rng, tamano_lote=2500):
    """p-valor del WCR de Webb para H0: beta = beta0. Devuelve (p, t, beta_hat, se)."""
    G, T = y.shape
    beta, se, Dt, _ = twfe_crve(y, D)
    t = (beta - beta0) / se
    er = desmedia2(y - beta0 * D)             # residuos restringidos (H0 impuesta)
    sdd = float((Dt ** 2).sum())
    N, K = G * T, T
    c = G / (G - 1) * (N - 1) / (N - K)
    cuenta = 0
    hechas = 0
    while hechas < B:
        b = min(tamano_lote, B - hechas)
        w = WEBB[rng.integers(0, 6, size=(b, G))]
        ys = desmedia2(w[:, :, None] * er[None, :, :])      # (b, G, T)
        bs = (Dt[None] * ys).sum(axis=(1, 2)) / sdd
        es = ys - bs[:, None, None] * Dt[None]
        sc = (Dt[None] * es).sum(axis=2)
        ses = np.sqrt(c * (sc ** 2).sum(axis=1)) / sdd
        cuenta += int(np.sum(np.abs(bs / ses) >= abs(t) - 1e-12))
        hechas += b
    return cuenta / B, t, beta, se
