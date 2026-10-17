"""V16 fase 6, grupo C · auxiliares de series para Q9: GSADF/BSADF con bootstrap salvaje, CIPS, MG, PMG y CS-ARDL. Sin efectos al importar.

GSADF (Phillips-Shi-Yu 2015), constante y sin rezagos, ventana mínima floor(T(0,01 + 1,8/sqrt(T))); bootstrap salvaje de Harvey et al. (2016):
Δy* = Δy·w, w ~ N(0,1), raíz unitaria impuesta, y*_0 = y_0 (el mismo de la fase 5: src/v16/montecarlo/gsadf_factor.py).
CS-ARDL (Chudik-Pesaran 2015) y MG/PMG (Pesaran-Shin-Smith 1999): estimación puntual; la inferencia de la herramienta es NO APTA.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

SEED = 20261010


def r0_psy(T: int) -> int:
    return int(np.floor(T * (0.01 + 1.8 / np.sqrt(T))))


def bsadf_seq(y: np.ndarray, r0: int | None = None) -> np.ndarray:
    """Secuencia BSADF(e) = sup_s ADF(s,e) para cada final e (en índice de Δy, e = r0..n). Devuelve array de longitud n+1 con NaN antes de r0."""
    T = len(y)
    r0 = r0_psy(T) if r0 is None else r0
    dy = np.diff(y)
    x = y[:-1]
    n = len(dy)
    cs = lambda v: np.concatenate([[0.0], np.cumsum(v)])
    Sx, Sxx, Sd, Sdd, Sxd = cs(x), cs(x * x), cs(dy), cs(dy * dy), cs(x * dy)
    out = np.full(n + 1, np.nan)
    for e in range(r0, n + 1):
        s = np.arange(0, e - r0 + 1)
        m = (e - s).astype(float)
        sx, sxx, sd, sdd, sxd = Sx[e] - Sx[s], Sxx[e] - Sxx[s], Sd[e] - Sd[s], Sdd[e] - Sdd[s], Sxd[e] - Sxd[s]
        sxx_c = sxx - sx ** 2 / m
        sxd_c = sxd - sx * sd / m
        b = sxd_c / sxx_c
        ssr = (sdd - sd ** 2 / m) - b * sxd_c
        out[e] = np.max(b / np.sqrt(np.maximum(ssr, 1e-300) / (m - 2) / sxx_c))
    return out


def gsadf_boot(y: np.ndarray, B: int = 499, seed: int = SEED, k: int = 0) -> dict:
    """GSADF con bootstrap salvaje: estadístico, vc 95 %, p bootstrap, BSADF y vc puntual (fechas de exuberancia)."""
    rng = np.random.default_rng([seed, 9, k])
    seq = bsadf_seq(y)
    stat = float(np.nanmax(seq))
    dy = np.diff(y)
    mx = np.empty(B)
    sq = np.empty((B, len(seq)))
    for b in range(B):
        yb = np.concatenate([[y[0]], y[0] + np.cumsum(dy * rng.standard_normal(len(dy)))])
        s = bsadf_seq(yb)
        sq[b] = s
        mx[b] = np.nanmax(s)
    cv = float(np.quantile(mx, 0.95))
    cv_pt = np.nanquantile(sq, 0.95, axis=0)
    # índice de y: BSADF(e) usa y hasta la posición e (Δy_e = y_e − y_{e−1}), es decir, y[e]
    exu = np.where(seq > cv_pt)[0]
    return {"stat": stat, "cv95": cv, "p_bootstrap": float((1 + (mx >= stat).sum()) / (B + 1)), "B": B, "seq": seq, "cv_puntual": cv_pt, "indices_exuberancia": exu.tolist()}


# ------------------------------------------------------------------------------------------- paneles (T x N)
def _lagmat(v: np.ndarray, p: int, desde: int) -> np.ndarray:
    """columnas v_t, v_{t-1}, ..., v_{t-p} para t = desde..T-1."""
    T = len(v)
    return np.column_stack([v[desde - l:T - l] for l in range(p + 1)])


def ardl_unit(y: np.ndarray, x: np.ndarray, p: int, z: np.ndarray | None = None, csa: np.ndarray | None = None) -> float:
    """ARDL(p,p) de una unidad con medias transversales opcionales (csa: T x 2 = ȳ, x̄) y regresor común opcional z (T,). Devuelve θ de largo plazo."""
    T = len(y)
    d = p
    Y = y[d:]
    cols = [np.ones(T - d)]
    Ly = _lagmat(y, p, d)[:, 1:]
    Lx = _lagmat(x, p, d)
    cols += [Ly, Lx]
    if z is not None:
        cols.append(_lagmat(z, p, d))
    if csa is not None:
        for j in range(csa.shape[1]):
            cols.append(_lagmat(csa[:, j], p, d))
    A = np.column_stack(cols)
    b, *_ = np.linalg.lstsq(A, Y, rcond=None)
    phi = b[1:1 + p].sum()
    beta = b[1 + p:2 + 2 * p].sum()
    den = 1 - phi
    return float(beta / den) if abs(den) > 1e-6 else np.nan


def mg_cs(Y: np.ndarray, X: np.ndarray, p: int, estimador: str, Z: np.ndarray | None = None) -> dict:
    """MG (sin medias transversales) o CS-ARDL (con ȳ, x̄ contemporáneas y p rezagos). Y, X: T x N. Z: regresor común (T,) opcional (solo MG)."""
    T, N = Y.shape
    csa = np.column_stack([Y.mean(1), X.mean(1)]) if estimador == "CS-ARDL" else None
    th = np.array([ardl_unit(Y[:, i], X[:, i], p, z=Z, csa=csa) for i in range(N)])
    ok = np.isfinite(th)
    return {"theta_media": float(np.mean(th[ok])), "theta_mediana": float(np.median(th[ok])), "theta_p25": float(np.quantile(th[ok], .25)),
            "theta_p75": float(np.quantile(th[ok], .75)), "n_unidades": int(ok.sum()), "n_no_estimables": int((~ok).sum()), "theta_i": th.tolist()}


def pmg(Y: np.ndarray, X: np.ndarray, p: int, Z: np.ndarray | None = None) -> dict:
    """PMG por verosimilitud concentrada: θ común (y − θx [− θ_z z]) y el resto por unidad. Modelo ECM con p−1 rezagos de Δ."""
    T, N = Y.shape
    nl = max(p - 1, 0)
    d = nl + 1
    k = 1 if Z is None else 2
    LR = [X] + ([np.repeat(Z[:, None], N, 1)] if Z is not None else [])

    def ssr(theta):
        tot = 0.0
        phis = []
        for i in range(N):
            ect = (Y[:, i] - sum(th * L[:, i] for th, L in zip(theta, LR)))[d - 1:T - 1]
            dY = np.diff(Y[:, i])
            dep = dY[d - 1:]
            cols = [np.ones(len(dep)), ect]
            for l in range(1, nl + 1):
                cols.append(dY[d - 1 - l:len(dY) - l])
            for L in LR:
                dL = np.diff(L[:, i])
                for l in range(0, nl + 1):
                    cols.append(dL[d - 1 - l:len(dL) - l])
            A = np.column_stack(cols)
            b, *_ = np.linalg.lstsq(A, dep, rcond=None)
            e = dep - A @ b
            tot += len(dep) * np.log(e @ e / len(dep))
            phis.append(b[1])
        return tot, np.array(phis)

    best = None
    for t0 in (0.5, 1.0, 1.5):
        r = minimize(lambda th: ssr(th)[0], x0=np.array([t0] + [0.0] * (k - 1)), method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-7, "maxiter": 400})
        if best is None or r.fun < best.fun:
            best = r
    phis = ssr(best.x)[1]
    return {"theta": float(best.x[0]), "theta_vector": best.x.tolist(), "phi_media": float(phis.mean()), "phi_mediana": float(np.median(phis)),
            "frac_phi_negativo": float((phis < 0).mean()), "convergio": bool(best.success), "n_unidades": N}


def cips(Y: np.ndarray, lags: int = 1) -> dict:
    """Estadístico CIPS (media de t-CADF) con constante y `lags` rezagos de Δy y de Δȳ. Descriptivo: sin valor crítico (bootstrap NO APTO)."""
    T, N = Y.shape
    yb = Y.mean(1)
    dyb = np.diff(yb)
    ts = []
    d = lags + 1
    for i in range(N):
        y = Y[:, i]
        dy = np.diff(y)
        dep = dy[d - 1:]
        cols = [np.ones(len(dep)), y[d - 1:T - 1], yb[d - 1:T - 1], dyb[d - 1:]]
        for l in range(1, lags + 1):
            cols += [dy[d - 1 - l:len(dy) - l], dyb[d - 1 - l:len(dyb) - l]]
        A = np.column_stack(cols)
        b, *_ = np.linalg.lstsq(A, dep, rcond=None)
        e = dep - A @ b
        s2 = e @ e / (len(dep) - A.shape[1])
        V = s2 * np.linalg.inv(A.T @ A)
        ts.append(b[1] / np.sqrt(V[1, 1]))
    return {"CIPS": float(np.mean(ts)), "t_CADF_mediana": float(np.median(ts)), "N": N, "T": T, "rezagos": lags}
