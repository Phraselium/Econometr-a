"""V18 · Proyección local con instrumento (LP-IV) con un regresor endógeno y un instrumento: 2SLS con errores de Newey-West (ancho h + 1) o
de Eicker-Huber-White tras aumentar con rezagos (Montiel Olea y Plagborg-Møller, 2021), y conjuntos de confianza de Anderson-Rubin
(robustos a instrumento débil) con la misma varianza. Sin lectura de datos: reciben arrays.

Todo se escribe con el teorema de Frisch-Waugh: tras residualizar y_{t+h} − y_{t−1}, Δi_t y z_t sobre los controles, el 2SLS es a / b con
a = Σ z̃ ỹ y b = Σ z̃ x̃. Con un solo instrumento, el estadístico de AR en β0 es (a − β0 b)² / (n V(β0)), V(β0) = Ω_aa − 2 β0 Ω_ab + β0² Ω_bb, y la
pertenencia de β0 al conjunto es una desigualdad cuadrática en β0 (forma cerrada, conjunto posiblemente no acotado).
"""
from __future__ import annotations

import numpy as np
from scipy import stats

ALCANCE_TERRITORIAL = "sin lectura de datos"
CHI2_95 = float(stats.chi2.ppf(0.95, 1))


def lrv(S: np.ndarray, L: int) -> np.ndarray:
    """Varianza de largo plazo de Bartlett (Newey-West) con L rezagos (L = 0: Eicker-Huber-White) de las filas de S (n, k), centradas."""
    S = S - S.mean(0, keepdims=True)
    n = len(S)
    V = S.T @ S / n
    for j in range(1, L + 1):
        G = S[j:].T @ S[:-j] / n
        V += (1 - j / (L + 1)) * (G + G.T)
    return V


def matriz_lp(y: np.ndarray, x: np.ndarray, z: np.ndarray, h: int, p: int = 4):
    """y_{t+h} − y_{t−1}, x_t, z_t y controles (constante, p rezagos de y en niveles y p rezagos de x) para t = p, ..., T − h − 1 (cero-índice)."""
    T = len(y)
    t = np.arange(p, T - h)
    dep = y[t + h] - y[t - 1]
    W = [np.ones(len(t))] + [y[t - l] for l in range(1, p + 1)] + [x[t - l] for l in range(1, p + 1)]
    return dep, x[t], z[t], np.column_stack(W)


def _res(v: np.ndarray, W: np.ndarray) -> np.ndarray:
    return v - W @ np.linalg.lstsq(W, v, rcond=None)[0]


def lp_iv(y: np.ndarray, x: np.ndarray, z: np.ndarray, h: int, L: int, p: int = 4) -> dict:
    """LP-IV a horizonte h con varianza de largo plazo de L rezagos (L = h + 1: Newey-West del plan; L = 0: EHW con aumento por rezagos)."""
    dep, xx, zz, W = matriz_lp(y, x, z, h, p)
    n, k = W.shape
    yt, xt, zt = _res(dep, W), _res(xx, W), _res(z[p:len(y) - h], W)
    a, b = float(zt @ yt), float(zt @ xt)
    s = zt[:, None] * np.column_stack([yt, xt])
    fac = n / max(n - k - 1, 1)
    Om = lrv(s, L) * fac
    return {"a": a, "b": b, "Om": Om, "n": n, "beta": a / b if abs(b) > 1e-300 else np.nan, "zz": float(zt @ zt)}


def var_g(r: dict, b0: float) -> float:
    Om = r["Om"]
    return float(Om[0, 0] - 2 * b0 * Om[0, 1] + b0 ** 2 * Om[1, 1])


def p_t(r: dict, b0: float) -> float:
    """p-valor del contraste t de 2SLS de β = β0 con la varianza robusta evaluada en β̂ (normal)."""
    if not np.isfinite(r["beta"]):
        return np.nan
    v = var_g(r, r["beta"]) * r["n"] / r["b"] ** 2
    return float(2 * stats.norm.sf(abs(r["beta"] - b0) / np.sqrt(max(v, 1e-300))))


def ar_stat(r: dict, b0: float) -> float:
    return float((r["a"] - b0 * r["b"]) ** 2 / (r["n"] * max(var_g(r, b0), 1e-300)))


def p_ar(r: dict, b0: float) -> float:
    return float(stats.chi2.sf(ar_stat(r, b0), 1))


def f_robusto(r: dict) -> float:
    """F robusta de primera etapa (un instrumento): (b / n)² / Var(b/n) con Var = Ω_bb / n."""
    return float((r["b"] ** 2) / (r["n"] * max(r["Om"][1, 1], 1e-300)))


def conjunto_ar(r: dict) -> tuple[str, float, float]:
    """Conjunto AR al 95 %: ('acotado', lo, hi), ('no_acotado', r1, r2) con el conjunto fuera de (r1, r2), ('recta', nan, nan) o ('vacio', nan, nan)."""
    a, b, n, Om = r["a"], r["b"], r["n"], r["Om"]
    c = CHI2_95 * n
    A2 = b * b - c * Om[1, 1]
    B1 = -2 * (a * b - c * Om[0, 1])
    C0 = a * a - c * Om[0, 0]
    if abs(A2) < 1e-300:
        return ("recta", np.nan, np.nan)
    disc = B1 * B1 - 4 * A2 * C0
    if disc < 0:
        return ("recta", np.nan, np.nan) if A2 < 0 else ("vacio", np.nan, np.nan)
    r1, r2 = sorted([(-B1 - np.sqrt(disc)) / (2 * A2), (-B1 + np.sqrt(disc)) / (2 * A2)])
    return ("acotado", r1, r2) if A2 > 0 else ("no_acotado", r1, r2)
