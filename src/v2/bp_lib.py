"""Rama BP: biblioteca de estimadores de efecto de política con un grupo tratado agregado.

* sdid        : Synthetic DiD (Arkhangelsky, Athey, Hirshberg, Imbens y Wager, 2021, AER). Implementación
                propia fiel al algoritmo 1: pesos de unidad ω (con intercepto y regularización
                ζ_ω² T_pre ||ω||², ζ_ω = (N_tr T_post)^{1/4} σ̂), pesos de tiempo λ (con intercepto y
                ζ_λ = 1e-6 σ̂), σ̂ = DE de las primeras diferencias de los controles en el pre-periodo.
                El problema es un QP sobre el símplex que se resuelve con SLSQP (la referencia usa
                Frank-Wolfe: misma solución salvo tolerancia). τ = diff-in-diff ponderado.
* sc          : control sintético de Abadie-Diamond-Hainmueller (2010): ω en el símplex que minimiza el
                error cuadrático del pre-periodo, sin intercepto, sin regularización, sin λ.
                τ = brecha media del post-periodo.
* did         : DiD con pesos uniformes (equivale a los efectos fijos de unidad y tiempo con adopción
                simultánea en un panel balanceado).
* permutaciones: se reasigna el estatus de tratada a subconjuntos aleatorios de N_tr donantes (semilla
                fija) y se re-estima TODO (también ω y λ); p = (1 + #{|τ_b| >= |τ|}) / (B + 1).
Todo es determinista (SEED = 20261010) y sin red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SEED = 20261010
NO_CONV = [0]   # nº de QP que SLSQP no declaró convergidos (diagnóstico)


# ------------------------------------------------------------------ QP sobre el símplex
def simplex_qp(A, b, pen, x0=None):
    """min ||A x - b||² + pen ||x||²  s.a. x >= 0, sum x = 1 (A: m×n)."""
    A = np.asarray(A, float)
    b = np.asarray(b, float)
    n = A.shape[1]
    if n == 1:
        return np.ones(1)
    H = A.T @ A + (pen + 1e-12 * max(np.trace(A.T @ A) / n, 1e-30)) * np.eye(n)
    g = A.T @ b
    sc = max(np.trace(H) / n, 1e-30)
    H, g = H / sc, g / sc
    x0 = np.full(n, 1.0 / n) if x0 is None else x0
    r = minimize(lambda x: 0.5 * x @ H @ x - g @ x, x0, jac=lambda x: H @ x - g, method="SLSQP",
                 bounds=[(0, 1)] * n, constraints=[{"type": "eq", "fun": lambda x: x.sum() - 1,
                                                    "jac": lambda x: np.ones(n)}],
                 options={"ftol": 1e-13, "maxiter": 500})
    if not r.success:
        NO_CONV[0] += 1
    x = np.clip(r.x, 0, None)
    return x / x.sum()


def _noise(Yco, pre):
    """DE de las primeras diferencias (solo trimestres consecutivos) de los controles en el pre-periodo."""
    pre = np.asarray(sorted(pre))
    ok = np.where(np.diff(pre) == 1)[0]
    if len(ok) == 0:
        return float(np.std(Yco[:, pre]) or 1.0)
    d = Yco[:, pre[ok + 1]] - Yco[:, pre[ok]]
    return float(np.std(d, ddof=1))


# ------------------------------------------------------------------ estimadores
def sdid(Yco, ytr, pre, post, zeta_scale=1.0, n_tr=1):
    """Synthetic DiD. Yco: N0×T (controles), ytr: T (media del grupo tratado), pre/post: posiciones."""
    pre, post = np.asarray(pre), np.asarray(post)
    N0, Tpre = Yco.shape[0], len(pre)
    sig = _noise(Yco, pre)
    z_om = zeta_scale * (n_tr * len(post)) ** 0.25 * sig
    z_la = 1e-6 * sig
    A = Yco[:, pre].T
    Ac = A - A.mean(axis=0, keepdims=True)
    bc = ytr[pre] - ytr[pre].mean()
    om = simplex_qp(Ac, bc, z_om ** 2 * Tpre)
    A2 = Yco[:, pre]
    A2c = A2 - A2.mean(axis=0, keepdims=True)
    b2 = Yco[:, post].mean(axis=1)
    b2c = b2 - b2.mean()
    la = simplex_qp(A2c, b2c, z_la ** 2 * N0)
    gap = ytr - om @ Yco
    tau = gap[post].mean() - la @ gap[pre]
    return dict(tau=float(tau), omega=om, lam=la, gap=gap, sigma=sig, zeta_omega=z_om)


def sc(Yco, ytr, pre, post):
    """Control sintético clásico (sin intercepto): τ = brecha media en el post-periodo."""
    pre, post = np.asarray(pre), np.asarray(post)
    om = simplex_qp(Yco[:, pre].T, ytr[pre], 0.0)
    gap = ytr - om @ Yco
    return dict(tau=float(gap[post].mean()), omega=om, gap=gap)


def did(Yco, ytr, pre, post):
    pre, post = np.asarray(pre), np.asarray(post)
    om = np.full(Yco.shape[0], 1.0 / Yco.shape[0])
    gap = ytr - om @ Yco
    return dict(tau=float(gap[post].mean() - gap[pre].mean()), omega=om, gap=gap)


def jackknife_se(Y, tr_idx, co_idx, om, la, pre, post, w_tr=None):
    """Jackknife (Alg. 3 del paper) con pesos fijos renormalizados sobre unidades (tratadas y controles)."""
    pre, post = np.asarray(pre), np.asarray(post)
    w_tr = np.full(len(tr_idx), 1.0 / len(tr_idx)) if w_tr is None else np.asarray(w_tr)
    units = [("t", i) for i in range(len(tr_idx))] + [("c", j) for j in range(len(co_idx))]
    taus = []
    for kind, i in units:
        wt, oc = w_tr.copy(), om.copy()
        if kind == "t":
            if len(tr_idx) == 1:
                continue
            wt[i] = 0
        else:
            oc[i] = 0
        wt, oc = wt / wt.sum(), oc / oc.sum()
        gap = wt @ Y[tr_idx] - oc @ Y[co_idx]
        taus.append(gap[post].mean() - la @ gap[pre])
    taus = np.array(taus)
    n = len(taus)
    return float(np.sqrt((n - 1) / n * np.sum((taus - taus.mean()) ** 2))) if n > 1 else np.nan


# ------------------------------------------------------------------ permutaciones
def draws_subsets(n_donors, k, B, seed=SEED):
    """B subconjuntos distintos de k donantes (índices ordenados), deterministas."""
    rng = np.random.default_rng(seed)
    seen, out = set(), []
    tot_max = 1
    for i in range(k):
        tot_max = tot_max * (n_donors - i) // (i + 1)
    B = min(B, tot_max)
    while len(out) < B:
        s = tuple(sorted(rng.choice(n_donors, k, replace=False).tolist()))
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def p_perm(tau, taus_b, lado="dos"):
    taus_b = np.asarray(taus_b, float)
    taus_b = taus_b[np.isfinite(taus_b)]
    if lado == "dos":
        return float((1 + np.sum(np.abs(taus_b) >= abs(tau) - 1e-15)) / (len(taus_b) + 1))
    return float((1 + np.sum(taus_b <= tau + 1e-15)) / (len(taus_b) + 1))   # una cola: efecto <= observado


def run_design(Y, tr_idx, co_idx, pre, post, subsets, w_tr=None, metodos=("sdid", "sc", "did")):
    """Estima τ (real) y su distribución de permutación por método. Y: unidades×T."""
    tr_idx, co_idx = np.asarray(tr_idx), np.asarray(co_idx)
    k = len(tr_idx)
    w_tr = np.full(k, 1.0 / k) if w_tr is None else np.asarray(w_tr, float) / np.sum(w_tr)

    def one(tr, co):
        ytr, Yco = w_tr @ Y[tr], Y[co]
        r = {}
        if "sdid" in metodos:
            r["sdid"] = sdid(Yco, ytr, pre, post, n_tr=len(tr))
        if "sc" in metodos:
            r["sc"] = sc(Yco, ytr, pre, post)
        if "did" in metodos:
            r["did"] = did(Yco, ytr, pre, post)
        return r
    real = one(tr_idx, co_idx)
    dist = {m: [] for m in real}
    for s in subsets:
        s = np.asarray(s)
        co_b = co_idx[s]
        rest = np.setdiff1d(np.arange(len(co_idx)), s)
        r = one(co_b, co_idx[rest])
        for m in r:
            dist[m].append(r[m]["tau"])
    out = {}
    for m, r in real.items():
        d = np.array(dist[m])
        se = float(np.std(d, ddof=1)) if len(d) > 1 else np.nan
        out[m] = dict(tau=r["tau"], se_placebo=se, ic95=[r["tau"] - 1.96 * se, r["tau"] + 1.96 * se],
                      p_dos=p_perm(r["tau"], d, "dos"), p_una=p_perm(r["tau"], d, "una"),
                      B=int(len(d)), dist=d, omega=r["omega"], gap=r["gap"],
                      lam=r.get("lam"), sigma=r.get("sigma"))
    return out


# ------------------------------------------------------------------ event study / pretendencias
def _slope(e):
    t = np.arange(len(e), dtype=float)
    t -= t.mean()
    return float((t @ (e - e.mean())) / (t @ t) * 4.0)   # pendiente por año (4 trimestres)


def evento_design(Y, tr_idx, co_idx, pre, post, subsets, w_tr=None):
    """Event study por trimestre (brecha tratada - sintético, centrada en la media del pre-periodo).

    Dos ponderaciones: 'sdid' (ω de SDiD ajustado en el pre-periodo; ajuste DENTRO de muestra) y 'did'
    (ω uniforme; diagnóstico no ajustado). Devuelve, por método: e (T), banda 2,5-97,5 % de permutación
    puntual (T), estadístico RMS del pre-periodo y pendiente por año con sus p de permutación
    (RMS: una cola superior; pendiente: bilateral). Toda la distribución nula re-estima ω."""
    tr_idx, co_idx = np.asarray(tr_idx), np.asarray(co_idx)
    pre, post = np.asarray(pre), np.asarray(post)
    k = len(tr_idx)
    w_tr = np.full(k, 1.0 / k) if w_tr is None else np.asarray(w_tr, float) / np.sum(w_tr)

    def one(tr, co):
        ytr, Yco = w_tr @ Y[tr], Y[co]
        g_s = sdid(Yco, ytr, pre, post, n_tr=len(tr))["gap"]
        g_d = ytr - Yco.mean(axis=0)
        return {"sdid": g_s - g_s[pre].mean(), "did": g_d - g_d[pre].mean()}
    real = one(tr_idx, co_idx)
    nul = {m: [] for m in real}
    for s in subsets:
        s = np.asarray(s)
        rest = np.setdiff1d(np.arange(len(co_idx)), s)
        r = one(co_idx[s], co_idx[rest])
        for m in r:
            nul[m].append(r[m])
    out = {}
    for m in real:
        N = np.array(nul[m])
        e = real[m]
        rms = float(np.sqrt(np.mean(e[pre] ** 2)))
        sl = _slope(e[pre])
        rms_b = np.sqrt(np.mean(N[:, pre] ** 2, axis=1))
        sl_b = np.array([_slope(x[pre]) for x in N])
        out[m] = dict(e=e, lo=np.percentile(N, 2.5, axis=0), hi=np.percentile(N, 97.5, axis=0),
                      rms_pre=rms, slope_pre_anual=sl,
                      p_rms=float((1 + np.sum(rms_b >= rms - 1e-15)) / (len(rms_b) + 1)),
                      p_slope=float((1 + np.sum(np.abs(sl_b) >= abs(sl) - 1e-15)) / (len(sl_b) + 1)),
                      B=int(len(N)))
    return out
