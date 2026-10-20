"""V18 · Metaanálisis bayesiano de efectos aleatorios por cuadratura determinista (sin MCMC): y_k ~ N(θ_k, se_k²), θ_k ~ N(μ, τ²).

Prior de μ: N(0, (c·s)²) con c = 1 (principal), 2 y 1/2 (las tres variantes de la adenda 1.9); prior de τ: semi-normal(0, (s/2)²)
(plan, sección 3) o semi-Cauchy(0, s/2) (sensibilidad). μ se marginaliza analíticamente; τ se integra en una rejilla fija (400 puntos,
espaciado cuadrático hasta 8 s). Devuelve medianas e intervalos de credibilidad equicolas al 95 % de μ y de τ, y el intervalo
de predicción de un estudio nuevo no se calcula aquí (no es objeto de la validación pedida: cobertura de μ y de τ).
Con menos de 3 estudios (plan, sección 3) se usa la media ponderada por la inversa de la varianza (efecto fijo) con su IC95 sin τ.
Sin lectura de datos: reciben arrays; todo se hace en lote sobre réplicas.
"""
from __future__ import annotations

import numpy as np
from scipy.special import ndtr

ALCANCE_TERRITORIAL = "sin lectura de datos"
J = 400
XG = 240


def rejilla_tau(s: float = 1.0):
    u = (np.arange(J) + 0.5) / J
    tau = 8.0 * s * u ** 2
    dt = 16.0 * s * u / J
    return tau, dt


def densidad_prior_tau(tau: np.ndarray, s: float, tipo: str) -> np.ndarray:
    sc = s / 2.0
    if tipo == "seminormal":
        return np.sqrt(2 / np.pi) / sc * np.exp(-0.5 * (tau / sc) ** 2)
    if tipo == "semicauchy":
        return 2.0 / (np.pi * sc * (1 + (tau / sc) ** 2))
    raise ValueError(tipo)


def posterior(Y: np.ndarray, SE: np.ndarray, s: float = 1.0, mult: float = 1.0, tipo_tau: str = "seminormal") -> dict:
    """Y, SE: (R, K). Devuelve dict con mu_lo, mu_med, mu_hi, tau_lo, tau_med, tau_hi (R,)."""
    R, K = Y.shape
    tau, dt = rejilla_tau(s)
    s0 = mult * s
    w = 1.0 / (SE[:, :, None] ** 2 + tau[None, None, :] ** 2)            # (R, K, J)
    S1 = w.sum(1)
    Sy = (w * Y[:, :, None]).sum(1)
    Syy = (w * Y[:, :, None] ** 2).sum(1)
    P = S1 + 1.0 / s0 ** 2
    logL = 0.5 * np.log(w).sum(1) - 0.5 * np.log(P) - 0.5 * (Syy - Sy ** 2 / P)
    logw = logL + np.log(densidad_prior_tau(tau, s, tipo_tau) * dt)[None, :]
    logw -= logw.max(1, keepdims=True)
    om = np.exp(logw)
    om /= om.sum(1, keepdims=True)                                       # (R, J)
    m = Sy / P
    sd = 1.0 / np.sqrt(P)
    # cuantiles de μ: mezcla de normales
    lo = (m - 9 * sd).min(1)
    hi = (m + 9 * sd).max(1)
    xs = lo[:, None] + (hi - lo)[:, None] * np.linspace(0, 1, XG)[None, :]   # (R, XG)
    F = np.empty((R, XG))
    paso = max(1, 2_000_000 // (XG * J))
    for a in range(0, R, paso):
        b = min(R, a + paso)
        z = (xs[a:b, :, None] - m[a:b, None, :]) / sd[a:b, None, :]
        F[a:b] = (ndtr(z) * om[a:b, None, :]).sum(2)
    mu = {q: _inv(xs, F, q) for q in (0.025, 0.5, 0.975)}
    cum = np.cumsum(om, axis=1)
    tt = np.broadcast_to(tau, (R, J))
    ta = {q: _inv(tt, cum, q) for q in (0.025, 0.5, 0.975)}
    return {"mu_lo": mu[0.025], "mu_med": mu[0.5], "mu_hi": mu[0.975], "tau_lo": ta[0.025], "tau_med": ta[0.5], "tau_hi": ta[0.975]}


def _inv(x: np.ndarray, F: np.ndarray, q: float) -> np.ndarray:
    """Cuantil q por interpolación lineal de una cdf discreta F (R, n) sobre x (R, n)."""
    idx = np.minimum((F >= q).argmax(1), F.shape[1] - 1)
    i0 = np.maximum(idx - 1, 0)
    r = np.arange(len(F))
    f0, f1 = F[r, i0], F[r, idx]
    x0, x1 = x[r, i0], x[r, idx]
    den = np.where(f1 > f0, f1 - f0, 1.0)
    frac = np.clip((q - f0) / den, 0, 1)
    return x0 + frac * (x1 - x0)


def efecto_fijo(Y: np.ndarray, SE: np.ndarray) -> dict:
    """Media ponderada por la inversa de la varianza (efecto fijo) con IC95 normal."""
    w = 1.0 / SE ** 2
    m = (w * Y).sum(1) / w.sum(1)
    se = 1.0 / np.sqrt(w.sum(1))
    return {"mu_lo": m - 1.959964 * se, "mu_med": m, "mu_hi": m + 1.959964 * se}
