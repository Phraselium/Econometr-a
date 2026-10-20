"""V18 · errores estándar de Driscoll-Kraay (1998) para paneles con efectos fijos de unidad (y opcionalmente de año).

Sin lectura de datos: recibe arrays (N unidades x T periodos). Estimador de efectos fijos intra-grupo; momentos
h_t = sum_i x_it e_it (por periodo) con núcleo de Bartlett de ancho m (Newey-West) y matriz sandwich (X'X)^-1 S (X'X)^-1.
Sin ajuste de muestra pequeña salvo el inferencial: se usa t con T-1 grados (como xtscc de Stata).
"""
from __future__ import annotations

import numpy as np

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"


def ancho_por_defecto(T: int) -> int:
    """m = floor(4 (T/100)^(2/9)), el predeterminado de xtscc."""
    return int(np.floor(4 * (T / 100.0) ** (2.0 / 9.0)))


def _intra(A, tiempo=False):
    """Desmedia intra-unidad sobre el eje T (último eje de A: (N, T, ...)); con tiempo=True, también por periodo."""
    A = A - A.mean(axis=1, keepdims=True)
    if tiempo:
        A = A - A.mean(axis=0, keepdims=True)
    return A


def fe_dk(y, X, m=None, tiempo=False):
    """y (N, T), X (N, T, p). Devuelve dict(beta, V_dk, V_cluster, V_hc1, m, T) del estimador FE.

    V_cluster: agrupado por unidad (CR1, G/(G-1)); V_hc1: heterocedástico sin agrupar (referencia).
    """
    N, T = y.shape
    X = X.reshape(N, T, -1)
    p = X.shape[2]
    yt = _intra(y, tiempo)
    Xt = _intra(X, tiempo)
    Sxx = np.einsum("itp,itq->pq", Xt, Xt)
    Si = np.linalg.inv(Sxx)
    beta = Si @ np.einsum("itp,it->p", Xt, yt)
    e = yt - Xt @ beta
    h = np.einsum("itp,it->tp", Xt, e)        # (T, p)
    if m is None:
        m = ancho_por_defecto(T)
    m = min(m, T - 1)
    S = h.T @ h
    for lag in range(1, m + 1):
        w = 1.0 - lag / (m + 1.0)
        G = h[lag:].T @ h[:-lag]
        S = S + w * (G + G.T)
    V_dk = Si @ S @ Si
    sc = np.einsum("itp,it->ip", Xt, e)       # (N, p)
    V_cl = Si @ (N / (N - 1.0) * sc.T @ sc) @ Si
    Sh = np.einsum("itp,itq,it->pq", Xt, Xt, e ** 2)
    V_h = Si @ (N * T / (N * T - 1.0) * Sh) @ Si
    return {"beta": beta, "V_dk": V_dk, "V_cluster": V_cl, "V_hc1": V_h, "m": m, "T": T}
