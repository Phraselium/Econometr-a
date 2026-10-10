"""C3: motor de estimación DiD (numpy). Un solo momento de tratamiento (2020Q4), Callaway-Sant'Anna sin covariables con
controles nunca tratados, TWFE, DID_M y utilidades de inferencia. Cluster = municipio (unidad)."""
import numpy as np
from scipy import stats

SEED = 20261010
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
Z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)


def _cov(M):
    return np.atleast_2d(np.cov(M.T, ddof=1)) if len(M) > 1 else np.zeros((M.shape[1], M.shape[1]))


def did_vec(Dm, tr):
    """Estimaciones DiD por columna de Dm (n x K de cambios frente a la base) y su covarianza (grupos independientes)."""
    T, C = Dm[tr], Dm[~tr]
    est = T.mean(0) - C.mean(0)
    V = _cov(T) / len(T) + _cov(C) / len(C)
    return est, V


def cs(Y, tr, base, post):
    """Y: n x T (columnas = periodos). ATT medio en las columnas `post` frente al periodo base (columna `base`)."""
    D = Y - Y[:, [base]]
    est, V = did_vec(D[:, post], tr)
    w = np.ones(len(post)) / len(post)
    th = float(w @ est)
    se = float(np.sqrt(w @ V @ w))
    n = len(tr)
    p = float(2 * stats.t.sf(abs(th / se), n - 2)) if se > 0 else np.nan
    return dict(b=th, se=se, p=p, ic=(th - stats.t.ppf(.975, n - 2) * se, th + stats.t.ppf(.975, n - 2) * se),
                nT=int(tr.sum()), nC=int((~tr).sum()))


def delta_cs(Y, base, post):
    return (Y[:, post].mean(1) - Y[:, base])


def event_study(Y, tr, base):
    D = Y - Y[:, [base]]
    est, V = did_vec(D, tr)
    return est, np.sqrt(np.diag(V)), V


def wald_pre(est, V, cols):
    e, Vs = est[cols], V[np.ix_(cols, cols)]
    W = float(e @ np.linalg.pinv(Vs) @ e)
    k = len(cols)
    return dict(W=W, k=k, p=float(stats.chi2.sf(W, k)))


def twfe(Y, tr, t0):
    """TWFE con D = tratado x (columna >= t0); panel equilibrado, FE de unidad y de periodo, cluster por unidad."""
    n, T = Y.shape
    D = np.outer(tr.astype(float), (np.arange(T) >= t0).astype(float))

    def dm(M):
        return M - M.mean(1, keepdims=True) - M.mean(0, keepdims=True) + M.mean()
    Dt, Yt = dm(D), dm(Y)
    den = (Dt ** 2).sum()
    b = float((Dt * Yt).sum() / den)
    e = Yt - b * Dt
    s = (Dt * e).sum(1)
    se = float(np.sqrt((s ** 2).sum() * n / (n - 1)) / den)
    p = float(2 * stats.t.sf(abs(b / se), n - 1))
    h = stats.t.ppf(.975, n - 1) * se
    return dict(b=b, se=se, p=p, ic=(b - h, b + h), nT=int(tr.sum()), nC=int((~tr).sum()))


def twfe_frac(Y, tr, Dfrac):
    """TWFE con intensidad de tratamiento por columna (p. ej. fracción del año con tope vigente)."""
    n, T = Y.shape
    D = np.outer(tr.astype(float), np.asarray(Dfrac, float))

    def dm(M):
        return M - M.mean(1, keepdims=True) - M.mean(0, keepdims=True) + M.mean()
    Dt, Yt = dm(D), dm(Y)
    den = (Dt ** 2).sum()
    b = float((Dt * Yt).sum() / den)
    e = Yt - b * Dt
    s = (Dt * e).sum(1)
    se = float(np.sqrt((s ** 2).sum() * n / (n - 1)) / den)
    h = stats.t.ppf(.975, n - 1) * se
    return dict(b=b, se=se, p=float(2 * stats.t.sf(abs(b / se), n - 1)), ic=(b - h, b + h),
                nT=int(tr.sum()), nC=int((~tr).sum()))


def welch_t(d, tr):
    T, C = d[tr], d[~tr]
    th = T.mean() - C.mean()
    se = np.sqrt(T.var(ddof=1) / len(T) + C.var(ddof=1) / len(C))
    return th, se


def wcb_webb(d, tr, reps=999, seed=SEED):
    """Wild cluster bootstrap (Webb) sobre el corte transversal Δ_i = a + b·tratado_i (clusters = unidades),
    imponiendo b = 0. p bilateral de la t de Welch."""
    th, se = welch_t(d, tr)
    t0 = th / se
    rng = np.random.default_rng(seed)
    e0 = d - d.mean()
    W = rng.choice(WEBB, size=(len(d), reps))
    Ds = d.mean() + W * e0[:, None]
    T, C = Ds[tr], Ds[~tr]
    ths = T.mean(0) - C.mean(0)
    ses = np.sqrt(T.var(0, ddof=1) / len(T) + C.var(0, ddof=1) / len(C))
    return float((1 + (np.abs(ths / ses) >= abs(t0)).sum()) / (reps + 1))


def ri_perm(d, tr, reps=999, seed=SEED):
    """Inferencia por aleatorización: permuta la etiqueta de tratamiento entre los clusters (unidades)."""
    th = d[tr].mean() - d[~tr].mean()
    rng = np.random.default_rng(seed)
    n, nt = len(d), int(tr.sum())
    cnt = 0
    for _ in range(reps):
        idx = rng.permutation(n)[:nt]
        m = np.zeros(n, bool)
        m[idx] = True
        cnt += abs(d[m].mean() - d[~m].mean()) >= abs(th) - 1e-15
    return float((1 + cnt) / (reps + 1))


def rr_bounds(Y, tr, base, pre, post, reps=999, seed=SEED, Mbar=1.0):
    """Cotas tipo Rambachan-Roth sin paquete (no está instalado): bootstrap por unidad dentro de grupo.
    RM: |δ_{j+1}-δ_j| <= Mbar x max |Δδ| de las pretendencias (con δ_base = 0); cota media post = Mbar·maxΔ·mean(j).
    SD (M=0): extrapola la tendencia lineal de los coeficientes previos (recta por la base) a los periodos post.
    IC robusto = percentiles 2,5 / 97,5 de (θ* ∓ cota*) en las réplicas."""
    rng = np.random.default_rng(seed)
    iT, iC = np.where(tr)[0], np.where(~tr)[0]
    jj = np.array(post) - base
    xp = np.array(pre) - base
    pre_all = list(pre) + [base]
    out_rm_lo, out_rm_hi, out_sd = [], [], []

    def una(idx_t, idx_c):
        Yb = np.vstack([Y[idx_t], Y[idx_c]])
        trb = np.r_[np.ones(len(idx_t), bool), np.zeros(len(idx_c), bool)]
        D = Yb - Yb[:, [base]]
        est = D[trb].mean(0) - D[~trb].mean(0)
        th = est[post].mean()
        seq = est[pre_all]
        maxd = np.abs(np.diff(seq)).max()
        B = Mbar * maxd * jj.mean()
        slope = (xp * est[pre]).sum() / (xp ** 2).sum()
        return th, B, slope * jj.mean()
    th0, B0, lin0 = una(iT, iC)
    for _ in range(reps):
        th, B, lin = una(rng.choice(iT, len(iT)), rng.choice(iC, len(iC)))
        out_rm_lo.append(th - B)
        out_rm_hi.append(th + B)
        out_sd.append(th - lin)
    return dict(theta=float(th0), cota_RM=float(B0), ic_RM=(float(np.quantile(out_rm_lo, .025)), float(np.quantile(out_rm_hi, .975))),
                ic_SD0=(float(np.quantile(out_sd, .025)), float(np.quantile(out_sd, .975))),
                theta_SD0=float(th0 - lin0))


def ols_t(X, y):
    """MCO clásico: coeficientes, t, R² y gl."""
    n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = (e @ e) / (n - k)
    V = s2 * np.linalg.pinv(X.T @ X)
    r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
    return b, b / np.sqrt(np.diag(V)), float(r2), n - k


def sensibilidad(d, tr, cov):
    """Oster (δ con R_max = min(1,3 R², 1) -> 1,3 x R² del modelo largo, tope 1) y Cinelli-Hazlett (RV_q=1) en Δ_i ~ tratado (+ covariables).
    cov: dict nombre -> vector. Devuelve δ, RV y el mayor R² parcial entre covariables observadas."""
    n = len(d)
    X0 = np.column_stack([np.ones(n), tr.astype(float)])
    names = list(cov)
    Xc = np.column_stack([X0] + [(cov[k] - cov[k].mean()) / (cov[k].std() + 1e-12) for k in names])
    b0, t0, r0, _ = ols_t(X0, d)
    b1, t1, r1, df1 = ols_t(Xc, d)
    rmax = min(1.3 * r1, 1.0)
    den = (b0[1] - b1[1]) * (rmax - r1)
    delta = np.inf if abs(den) < 1e-15 else float(b1[1] * (r1 - r0) / den)
    f = abs(t1[1]) / np.sqrt(df1)
    rv = float(0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2))
    pr = {k: float(t1[2 + i] ** 2 / (t1[2 + i] ** 2 + df1)) for i, k in enumerate(names)}
    return dict(oster_delta=delta, oster_abs=abs(delta), beta_corto=float(b0[1]), beta_largo=float(b1[1]), R2_corto=r0,
                R2_largo=r1, Rmax=rmax, RV_q1=rv, r2_parcial=pr, r2_parcial_max=max(pr.values()) if pr else 0.0,
                t_largo=float(t1[1]))


# ---- potencia (copia de src/v3/pot_run.py: EMD analítico t(G-1) y wild cluster bootstrap Rademacher)
def _sums(zt, xt, et, cl):
    import pandas as pd
    f, G = pd.factorize(cl)[0], len(set(cl))
    return np.bincount(f, zt * et, G), np.bincount(f, zt * xt, G), G


def estima(zt, xt, yt, cl):
    Sze, Szx, G = _sums(zt, xt, yt, cl)
    b = Sze.sum() / Szx.sum()
    r = Sze - b * Szx
    return b, float(np.sqrt((r ** 2).sum() / Szx.sum() ** 2 * G / (G - 1))), G


def emd_wcb(zt, xt, yt, cl, reps=500):
    Sze0, Szx, G = _sums(zt, xt, yt, cl)
    D = Szx.sum()
    b0 = Sze0.sum() / D
    Sze1 = _sums(zt, xt, yt - b0 * xt, cl)[0]
    rng = np.random.default_rng(SEED)
    W = rng.choice([-1.0, 1.0], size=(G, reps))

    def tab(Sze, delta):
        b = delta + (W.T @ Sze) / D
        r = W * Sze[:, None] + (delta - b)[None, :] * Szx[:, None]
        V = (r ** 2).sum(0) / D ** 2 * G / (G - 1)
        return np.abs(b / np.sqrt(V))
    crit = float(np.quantile(tab(Sze0, 0.0), 0.95))

    def pw(d):
        return float((tab(Sze1, d) > crit).mean())
    hi = Z * estima(zt, xt, yt, cl)[1]
    for _ in range(14):
        if pw(hi) >= 0.8:
            break
        hi *= 2
    else:
        return np.inf
    lo = 0.0
    for _ in range(18):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if pw(mid) < 0.8 else (lo, mid)
    return hi


def emd_cs(d, tr, reps=500):
    """EMD de una DiD de corte transversal Δ_i ~ tratado: max(analítico t(G-1), wild cluster bootstrap)."""
    zt = tr.astype(float) - tr.mean()
    yt = d - d.mean()
    cl = np.arange(len(d))
    b, se, G = estima(zt, zt, yt, cl)
    tg = stats.t.ppf(0.975, G - 1) + stats.t.ppf(0.80, G - 1)
    emd_t = tg * se
    emd_b = emd_wcb(zt, zt, yt, cl, reps)
    return dict(ee=se, emd_t=float(emd_t), emd_wcb=float(emd_b), emd=float(max(emd_t, emd_b)), G=int(G))
