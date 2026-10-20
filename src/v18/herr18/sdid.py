"""V18 · Diferencias en diferencias sintéticas (SDID, Arkhangelsky et al. 2021) con inferencia de Conley-Taber (2011) por placebos
para pocos tratados. Sin lectura de datos: reciben arrays.

Pesos de unidad ω (símplex, con intercepto implícito por centrado en el tiempo y regularización ζ² T_pre ||ω||²,
ζ = (N_tr T_post)^(1/4) σ̂) y de tiempo λ (símplex, regularización mínima) resueltos por gradiente proyectado acelerado (FISTA). Los
placebos se resuelven en LOTE: cada placebo toma n_tr controles al azar como «tratados» y el resto como donantes; el estimador es el mismo.

Aproximación declarada: los pesos de tiempo λ se calculan una vez con todos los controles y se mantienen fijos en los placebos (en el
artículo se reestiman); los ω sí se reestiman en cada placebo con los donantes restantes.
"""
from __future__ import annotations

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"


def proyecta_simplex(V: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Proyección euclídea de cada fila de V sobre el símplex (restringida a las posiciones con mask True)."""
    V = np.array(V, float)
    if mask is not None:
        V = np.where(mask, V, -1e9)
    B, N = V.shape
    U = -np.sort(-V, axis=1)
    css = np.cumsum(U, axis=1) - 1.0
    k = np.arange(1, N + 1)
    cond = (U - css / k) > 0
    rho = np.maximum(cond.sum(1), 1)
    theta = css[np.arange(B), rho - 1] / rho
    W = np.maximum(V - theta[:, None], 0.0)
    W[W < 1e-13] = 0.0
    if mask is not None:
        W = np.where(mask, W, 0.0)
    return W


def _fista(grad, L: float, W0: np.ndarray, mask: np.ndarray | None, it: int) -> np.ndarray:
    W, Z, t = W0.copy(), W0.copy(), 1.0
    for _ in range(it):
        Wn = proyecta_simplex(Z - grad(Z) / L, mask)
        tn = (1 + np.sqrt(1 + 4 * t * t)) / 2
        Z = Wn + ((t - 1) / tn) * (Wn - W)
        Z[np.abs(Z) < 1e-13] = 0.0          # evita números subnormales (ralentizan el producto matricial 10 a 100 veces)
        W, t = Wn, tn
    return W


def pesos_tiempo(Ypre_co: np.ndarray, ypost_co: np.ndarray, it: int = 60) -> np.ndarray:
    """λ ∈ símplex: Ypre_co (N_co, T_pre), ypost_co (N_co,) media posterior de cada control. Regularización mínima (1e-6 σ)."""
    B = Ypre_co - Ypre_co.mean(0, keepdims=True)
    b = ypost_co - ypost_co.mean()
    Tpre = B.shape[1]
    sig = float(np.std(np.diff(Ypre_co, axis=1))) + 1e-12
    reg = (1e-6 * sig) ** 2 * B.shape[0]
    BtB, Btb = B.T @ B, B.T @ b
    L = 2 * (np.linalg.eigvalsh(BtB)[-1] + reg) + 1e-12
    lam = _fista(lambda Z: 2 * (Z @ BtB - Btb[None, :]) + 2 * reg * Z, L, np.full((1, Tpre), 1.0 / Tpre), None, it)
    return lam[0]


def zeta(Ypre_co: np.ndarray, n_tr: int, T_post: int) -> float:
    return float((n_tr * T_post) ** 0.25 * np.std(np.diff(Ypre_co, axis=1)))


def pesos_unidad_lote(Ypre_co: np.ndarray, grupos: np.ndarray, zeta_: float, it: int = 60) -> np.ndarray:
    """Pesos ω por fila de `grupos` (B, N_co) bool: el grupo de cada fila es el «tratado» (media de sus columnas) y los donantes son
    los controles fuera del grupo. Devuelve Ω (B, N_co) en el símplex de los donantes."""
    A = Ypre_co.T - Ypre_co.T.mean(0, keepdims=True)         # (T_pre, N) centrado en el tiempo por unidad
    Tpre, N = A.shape
    G = grupos.astype(float)
    a = (G / G.sum(1, keepdims=True)) @ A.T                  # (B, T_pre)
    Aa = a @ A                                               # (B, N)
    reg = zeta_ ** 2 * Tpre
    L = 2 * (np.linalg.norm(A, 2) ** 2 + reg) + 1e-12
    donantes = ~grupos
    W0 = donantes / donantes.sum(1, keepdims=True)
    return _fista(lambda Z: 2 * ((Z @ A.T) @ A - Aa) + 2 * reg * Z, L, W0, donantes, it)   # (Z A') A: T_pre << N


def sdid(Ypre_tr: np.ndarray, Ypost_tr: np.ndarray, Ypre_co: np.ndarray, Ypost_co: np.ndarray) -> dict:
    """Estimador SDID. Ypre_*: (N, T_pre); Ypost_*: (N, T_post). Devuelve tau, pesos, y los Δ_j de los controles."""
    n_tr, n_co = Ypre_tr.shape[0], Ypre_co.shape[0]
    lam = pesos_tiempo(Ypre_co, Ypost_co.mean(1))
    z = zeta(Ypre_co, n_tr, Ypost_tr.shape[1])
    # El «grupo» tratado se pasa como una fila de objetivo propia: se añade al lote como una fila especial
    A = Ypre_co.T - Ypre_co.T.mean(0, keepdims=True)
    a = Ypre_tr.mean(0) - Ypre_tr.mean(0).mean()
    Aa = (a @ A)[None, :]
    reg = z ** 2 * A.shape[0]
    L = 2 * (np.linalg.norm(A, 2) ** 2 + reg) + 1e-12
    om = _fista(lambda Z: 2 * ((Z @ A.T) @ A - Aa) + 2 * reg * Z, L, np.full((1, n_co), 1.0 / n_co), None, 80)[0]
    delta_co = Ypost_co.mean(1) - Ypre_co @ lam
    delta_tr = Ypost_tr.mean(1) - Ypre_tr @ lam
    tau = float(delta_tr.mean() - om @ delta_co)
    return {"tau": tau, "omega": om, "lambda": lam, "delta_co": delta_co, "zeta": z, "delta_tr_medio": float(delta_tr.mean())}


def placebos(Ypre_co: np.ndarray, Ypost_co: np.ndarray, lam: np.ndarray, z: float, n_tr: int, rng: np.random.Generator, B: int = 199,
             it: int = 60) -> dict:
    """Distribución de placebos: B grupos al azar de n_tr controles, estimador SDID (ω reestimados) y DiD simple."""
    n_co = Ypre_co.shape[0]
    grupos = np.zeros((B, n_co), bool)
    for b in range(B):
        grupos[b, rng.choice(n_co, size=n_tr, replace=False)] = True
    delta = Ypost_co.mean(1) - Ypre_co @ lam
    Om = pesos_unidad_lote(Ypre_co, grupos, z, it)
    G = grupos / n_tr
    c_sdid = G @ delta - Om @ delta
    don = ~grupos
    c_did = G @ delta - (don @ delta) / don.sum(1)
    return {"sdid": c_sdid, "did": c_did}


def p_placebo(tau: float, c: np.ndarray, theta0: float) -> float:
    """p-valor de Conley-Taber con estadístico simétrico: P(|c| >= |τ̂ − θ0|) con la identidad incluida."""
    return float((1 + np.sum(np.abs(c) >= abs(tau - theta0))) / (len(c) + 1))


def p_normal_placebo(tau: float, c: np.ndarray, theta0: float) -> float:
    from scipy.stats import norm
    se = float(np.std(c, ddof=1))
    return float(2 * norm.sf(abs(tau - theta0) / max(se, 1e-300)))
