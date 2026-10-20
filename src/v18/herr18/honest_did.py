"""V18 · Honest DiD de Rambachan y Roth (2023), magnitudes relativas Δ^RM(M̄), con contraste condicional de Andrews, Roth y Pakes.

Sin lectura de datos: recibe coeficientes de estudio de eventos y su covarianza. Reutiliza las piezas poliédricas y el contraste
condicional de src/v9/herramientas.py (validados contra la rejilla en V15) y añade lo que V15 mostró que faltaba:
  * la covarianza del estudio de eventos se estima AGRUPADA al nivel del tratamiento (o del cluster elegido), no por unidad ignorando
    la correlación dentro del cluster (V15: tamaño 0,144 con la covarianza estimada y 0,052 con la verdadera: el fallo era la covarianza);
  * opción de corrección de grados de libertad de la covarianza (factor de Hotelling n_gl / (n_gl − k + 1)) cuando k coeficientes se
    estiman con n_gl grados de libertad de cluster, porque la covarianza muestral de dimensión k con pocos clusters sesga a la baja los
    contrastes conjuntos.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v9 import herramientas as H9  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"


def evento_agrupado(Y: np.ndarray, tratado: np.ndarray, cluster: np.ndarray, ref: int, pre: list[int], post: list[int],
                    corr_G: bool = True) -> tuple[np.ndarray, np.ndarray, dict]:
    """Coeficientes b_t = media_trat(Y_t − Y_ref) − media_ctrl(Y_t − Y_ref), t en pre + post, y su covarianza agrupada por cluster.
    Devuelve (b, V, info)."""
    cols = list(pre) + list(post)
    d = Y[:, cols] - Y[:, [ref]]
    tr, co = tratado, ~tratado
    n1, n0 = tr.sum(), co.sum()
    m1, m0 = d[tr].mean(0), d[co].mean(0)
    b = m1 - m0
    u = np.where(tr[:, None], (d - m1) / n1, -(d - m0) / n0)
    cl = np.unique(cluster)
    S = np.zeros((len(cl), len(cols)))
    idx = np.searchsorted(cl, cluster)
    np.add.at(S, idx, u)
    V = S.T @ S
    G = len(cl)
    if corr_G and G > 1:
        V = V * G / (G - 1)
    return b, V, {"G": G, "k": len(cols), "rango_V": int(np.linalg.matrix_rank(V))}


def contrasta(b: np.ndarray, V: np.ndarray, n_pre: int, n_post: int, Mbar: float, theta0: float, alfa: float = 0.05, l: np.ndarray | None = None) -> bool:
    """True si RECHAZA H0: θ = θ0 (θ = l'τ, por defecto la media de los coeficientes posteriores) con Δ^RM(M̄): rechaza solo si lo
    rechazan todas las piezas (unión de piezas poliédricas)."""
    l = np.ones(n_post) / n_post if l is None else l
    Bm = np.linalg.svd(l[None, :])[2][1:].T
    for A in H9._piezas_rm(n_pre, n_post, Mbar):
        SY = A @ V @ A.T
        sig = np.sqrt(np.clip(np.diag(SY), 1e-14, None))
        Ap = A[:, n_pre:]
        y = A @ b - Ap @ (theta0 * np.ones(n_post))
        # Se contrasta E[y] − X τ̃ ≤ 0 con X = Ap Bm (grados de libertad del parámetro nuisance), igual que V9/V15
        if not H9._arp_condicional(y, Ap @ Bm, sig, SY, alfa):
            return False
    return True


def ic(b: np.ndarray, V: np.ndarray, n_pre: int, n_post: int, Mbar: float, alfa: float = 0.05, rejilla: np.ndarray | None = None) -> tuple[float, float]:
    """IC por inversión del contraste sobre una rejilla (extremos refinados por bisección)."""
    l = np.ones(n_post) / n_post
    th = float(l @ b[n_pre:])
    se = float(np.sqrt(l @ V[n_pre:, n_pre:] @ l))
    if rejilla is None:
        rejilla = np.linspace(th - 12 * se - 0.01, th + 12 * se + 0.01, 241)
    ok = np.array([not contrasta(b, V, n_pre, n_post, Mbar, t, alfa) for t in rejilla])
    if not ok.any():
        return np.nan, np.nan
    i, j = int(np.argmax(ok)), int(len(ok) - 1 - np.argmax(ok[::-1]))

    def bis(dentro, fuera):
        for _ in range(10):
            m = (dentro + fuera) / 2
            dentro, fuera = (m, fuera) if not contrasta(b, V, n_pre, n_post, Mbar, m, alfa) else (dentro, m)
        return dentro
    lo = bis(rejilla[i], rejilla[i - 1]) if i > 0 else float(rejilla[0])
    hi = bis(rejilla[j], rejilla[j + 1]) if j < len(rejilla) - 1 else float(rejilla[-1])
    return float(lo), float(hi)
