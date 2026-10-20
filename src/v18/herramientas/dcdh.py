"""V18 · de Chaisemartin y D'Haultfœuille (DID_M con dosis continua y escalonada, horizonte ℓ) con inferencia por bootstrap de Webb y
por aleatorización del calendario entre clusters. Sin lectura de datos: reciben arrays.

Estimador (DID_ℓ): para cada periodo t (1..T−1−ℓ),
  cambiantes  = unidades con ΔD_t ≠ 0 y SIN otro cambio en (t, t+ℓ];
  controles   = unidades SIN cambio en [t, t+ℓ];
  β̂_ℓ = Σ_{cambiantes} sign(ΔD_t) (Y_{t+ℓ} − Y_{t−1} − m_t) / Σ_{cambiantes} |ΔD_t|, m_t = media de Y_{t+ℓ} − Y_{t−1} de los controles.
Con ℓ = 0 es el DID_M continuo de V16. Todo está escrito con una dimensión de lote (permutaciones) para que el contraste por
aleatorización recalcule el estimador y su EE de agrupación en cada permutación.

Lo que corrige frente a V16 (dcdh_aleatorizacion, NO APTO por tamaño 0,0775 con 11 clusters heterocedásticos): el estadístico del
contraste de aleatorización es ESTUDENTIZADO (β̂ / EE de agrupación recalculado en cada permutación) y no el coeficiente a secas:
con clusters de tamaño y varianza desiguales, el coeficiente no es intercambiable entre calendarios y la razón sí lo es,
aproximadamente.
"""
from __future__ import annotations

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"
SEMILLA = 20261010

_WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def onehot(cluster: np.ndarray) -> np.ndarray:
    cl = np.unique(cluster)
    return (cluster[:, None] == cl[None, :]).astype(float)


def _celdas(D: np.ndarray, ell: int):
    T = D.shape[-1]
    dD = D[..., 1:] - D[..., :-1]
    c = dD != 0
    cum = np.concatenate([np.zeros(c.shape[:-1] + (1,), int), np.cumsum(c, axis=-1)], axis=-1)   # cum[j] = cambios en índices < j
    Tc = T - 1 - ell
    k = np.arange(Tc)
    w1 = cum[..., k + ell + 1] - cum[..., k + 1]      # cambios en (t, t+ℓ]
    w0 = cum[..., k + ell + 1] - cum[..., k]          # cambios en [t, t+ℓ]
    chg = c[..., :Tc] & (w1 == 0)
    ctrl = w0 == 0
    return dD[..., :Tc], chg, ctrl


def estimar(Y: np.ndarray, D: np.ndarray, ell: int = 0, beta0=None) -> dict:
    """DID_ℓ y función de influencia por unidad. Y y D con forma (..., n, T) (se difunden). beta0: valor con el que se calcula la
    influencia (None: la estimación; 0: nulo impuesto). Devuelve dict con beta, IF (..., n), den y las máscaras."""
    dD, chg, ctrl = _celdas(D, ell)
    T = Y.shape[-1]
    dY = Y[..., 1 + ell:] - Y[..., :T - 1 - ell]
    n0 = ctrl.sum(-2)                                         # (..., Tc)
    valido = n0 > 0
    m = np.where(valido, (dY * ctrl).sum(-2) / np.maximum(n0, 1), 0.0)
    chg = chg & valido[..., None, :]
    s = np.sign(dD)
    a = np.abs(dD)
    num = (chg * s * (dY - m[..., None, :])).sum((-2, -1))
    den = (chg * a).sum((-2, -1))
    beta = np.where(den > 0, num / np.maximum(den, 1e-300), np.nan)
    b0 = beta if beta0 is None else np.broadcast_to(np.asarray(beta0, float), np.shape(beta))
    St = (chg * s).sum(-2)                                    # (..., Tc)
    res = dY - m[..., None, :]
    termino_c = (chg * (s * res - np.asarray(b0)[..., None, None] * a)).sum(-1)
    termino_k = (ctrl * valido[..., None, :] * (St / np.maximum(n0, 1))[..., None, :] * res).sum(-1)
    IF = (termino_c - termino_k) / np.maximum(den, 1e-300)[..., None]
    return {"beta": beta, "IF": IF, "den": den, "chg": chg, "a": a}


def verdad(beta_i: np.ndarray, D: np.ndarray, ell: int = 0) -> float:
    """Media de β_i ponderada por |ΔD| en las celdas cambiantes (la que estima DID_ℓ en un modelo de nivel y_it = β_i D_it):
    es el propio estimador aplicado al resultado sin ruido β_i D_it, donde los controles tienen ΔY = 0."""
    return float(estimar(beta_i[:, None] * D, D, ell)["beta"])


def ee_cluster(IF: np.ndarray, M: np.ndarray) -> np.ndarray:
    psi = IF @ M
    return np.sqrt((psi ** 2).sum(-1))


def p_webb(Y: np.ndarray, D: np.ndarray, theta0: float, ell: int, M: np.ndarray, rng: np.random.Generator, B: int = 999) -> float:
    """Bootstrap-t con pesos de Webb por cluster sobre la influencia con el nulo impuesto (β0 = θ0)."""
    r = estimar(Y, D, ell)
    if not np.isfinite(r["beta"]):
        return np.nan
    se = float(ee_cluster(r["IF"], M))
    t_obs = (r["beta"] - theta0) / max(se, 1e-300)
    psi0 = r["IF"] if theta0 is None else estimar(Y, D, ell, beta0=theta0)["IF"] @ M
    if psi0.ndim == 2:
        psi0 = psi0[0]
    G = M.shape[1]
    V = _WEBB[rng.integers(0, 6, size=(G, B))]
    num = (V * psi0[:, None]).sum(0)
    den = np.sqrt(((V * psi0[:, None]) ** 2).sum(0))
    t_b = num / np.maximum(den, 1e-300)
    return float((1 + np.sum(np.abs(t_b) >= abs(t_obs))) / (B + 1))


def permutaciones(rng: np.random.Generator, G: int, B: int) -> np.ndarray:
    """B permutaciones distintas de los G calendarios (la identidad se añade fuera)."""
    return np.array([rng.permutation(G) for _ in range(B)])


def p_aleatorizacion(Y: np.ndarray, Dc: np.ndarray, cl_idx: np.ndarray, theta0: float, ell: int, perms: np.ndarray,
                     estudentizado: bool = True) -> float:
    """Contraste de aleatorización (Fisher) de β = θ0 con efecto constante: se reasignan los calendarios de dosis completos entre
    los G clusters (cl_idx: cluster 0..G−1 de cada unidad; Dc: (G, T) dosis por cluster). Estadístico: |β̂/EE| (estudentizado)
    o |β̂|. Devuelve el p-valor con la identidad incluida."""
    M = onehot(cl_idx)
    D_obs = Dc[cl_idx]
    Yt = Y - theta0 * D_obs
    r0 = estimar(Yt, D_obs, ell)
    if not np.isfinite(r0["beta"]):
        return np.nan
    t0 = abs(r0["beta"] / max(float(ee_cluster(r0["IF"], M)), 1e-300)) if estudentizado else abs(r0["beta"])
    Dp = Dc[perms][:, cl_idx, :]                                  # (B, n, T)
    rp = estimar(Yt[None, :, :], Dp, ell)
    b = rp["beta"]
    if estudentizado:
        se = ee_cluster(rp["IF"], M)
        stat = np.abs(b) / np.maximum(se, 1e-300)
    else:
        stat = np.abs(b)
    stat = np.where(np.isfinite(stat), stat, 0.0)
    return float((1 + np.sum(stat >= t0 - 1e-12)) / (len(stat) + 1))
