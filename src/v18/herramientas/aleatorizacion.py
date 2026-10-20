"""V18 · Inferencia por aleatorización (permutaciones) para diferencias en diferencias (E2) y para dosis continua con calendarios por CCAA (E8).

Contraste de Fisher de «efecto constante θ0» (se resta θ0 a los resultados de las tratadas en los periodos posteriores) con estadístico
estudentizado (|razón t|) o no (|coeficiente|), recalculado en cada permutación. Sin lectura de datos: reciben arrays.

E2 (municipios): la asignación se permuta (a) entre todos los municipios (la del plan: «1.000 asignaciones del tratamiento entre municipios
catalanes») o (b) DENTRO de cada comarca, conservando el número de tratados por comarca (aleatorización condicionada al estrato, que es el
contraste correcto si los choques de comarca se reparten entre tratados y controles).
E8 (CCAA): se permutan los calendarios de dosis entre las CCAA; estadístico: coeficiente de MCO de dos vías sobre la dosis con EE agrupado por CCAA.
"""
from __future__ import annotations

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"


# ------------------------------------------------------------------------------------------------ E2: diferencias en diferencias
def delta_unidad(Y: np.ndarray, g: int) -> np.ndarray:
    """Cambio medio por unidad: media de los periodos >= g menos media de los anteriores."""
    return Y[:, g:].mean(1) - Y[:, :g].mean(1)


def did_welch(d: np.ndarray, lab: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """ATT = media(d | lab) − media(d | ~lab) y su EE de agrupación por unidad (Welch). lab: (..., n) bool."""
    lab = lab.astype(float)
    n1 = lab.sum(-1)
    n0 = lab.shape[-1] - n1
    m1 = (lab * d).sum(-1) / n1
    m0 = ((1 - lab) * d).sum(-1) / n0
    v1 = (lab * (d - m1[..., None]) ** 2).sum(-1) / np.maximum(n1 - 1, 1) / n1
    v0 = ((1 - lab) * (d - m0[..., None]) ** 2).sum(-1) / np.maximum(n0 - 1, 1) / n0
    return m1 - m0, np.sqrt(v1 + v0)


def etiquetas_individual(rng: np.random.Generator, lab: np.ndarray, B: int) -> np.ndarray:
    n = len(lab)
    orden = np.argsort(rng.random((B, n)), axis=1)
    return lab[orden]


def etiquetas_estrato(rng: np.random.Generator, lab: np.ndarray, estrato: np.ndarray, B: int) -> np.ndarray:
    """Permuta las etiquetas dentro de cada estrato (conserva el número de tratados por estrato)."""
    n = len(lab)
    ord0 = np.argsort(estrato, kind="stable")
    lab_ord = lab[ord0]                                       # etiquetas ordenadas por estrato
    clave = estrato[None, :] + rng.random((B, n)) * 0.5       # estrato (entero) + ruido < 1
    orden = np.argsort(clave, axis=1)                         # unidades ordenadas por estrato y al azar dentro
    nuevo = np.empty((B, n), bool)
    np.put_along_axis(nuevo, orden, np.broadcast_to(lab_ord, (B, n)), axis=1)
    return nuevo


def p_did(d: np.ndarray, lab: np.ndarray, theta0: float, perms: np.ndarray, estud: bool = True) -> float:
    """p-valor de aleatorización de θ = θ0. d: cambio por unidad; lab: etiqueta observada; perms: (B, n) etiquetas permutadas."""
    dt = d - theta0 * lab
    a0, s0 = did_welch(dt, lab)
    t0 = abs(a0 / max(s0, 1e-300)) if estud else abs(a0)
    a, s = did_welch(dt[None, :], perms)
    st = np.abs(a / np.maximum(s, 1e-300)) if estud else np.abs(a)
    return float((1 + np.sum(st >= t0 - 1e-12)) / (len(st) + 1))


# ------------------------------------------------------------------------------------------------ E8: dosis continua
def desmedia2(Z: np.ndarray) -> np.ndarray:
    return Z - Z.mean(-1, keepdims=True) - Z.mean(-2, keepdims=True) + Z.mean((-2, -1), keepdims=True)


def twfe_dosis(Y: np.ndarray, D: np.ndarray, M: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Coeficiente de MCO de dos vías de Y sobre la dosis D y EE agrupado (clusters = columnas de M). D puede tener un lote (B, n, T)."""
    Dt = desmedia2(D)
    yt = desmedia2(Y)
    den = (Dt ** 2).sum((-2, -1))
    b = (Dt * yt).sum((-2, -1)) / np.maximum(den, 1e-300)
    u = yt - b[..., None, None] * Dt
    psi = (Dt * u).sum(-1) @ M
    se = np.sqrt((psi ** 2).sum(-1)) / np.maximum(den, 1e-300)
    return b, se


def p_calendarios(Y: np.ndarray, Dc: np.ndarray, cl_idx: np.ndarray, theta0: float, perms: np.ndarray, estud: bool = True) -> float:
    """p-valor de aleatorización de β = θ0 (efecto constante) permutando los calendarios de dosis entre CCAA. perms: (B, G)."""
    G = Dc.shape[0]
    M = (cl_idx[:, None] == np.arange(G)[None, :]).astype(float)
    Dobs = Dc[cl_idx]
    Yt = Y - theta0 * Dobs
    b0, s0 = twfe_dosis(Yt, Dobs, M)
    t0 = abs(b0 / max(float(s0), 1e-300)) if estud else abs(float(b0))
    Dp = Dc[perms][:, cl_idx, :]
    b, s = twfe_dosis(Yt[None], Dp, M)
    st = np.abs(b / np.maximum(s, 1e-300)) if estud else np.abs(b)
    st = np.where(np.isfinite(st), st, 0.0)
    return float((1 + np.sum(st >= t0 - 1e-12)) / (len(st) + 1))
