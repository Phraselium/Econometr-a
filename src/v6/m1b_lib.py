"""M1b v6: estimadores (efectos fijos, wild cluster bootstrap Webb, Driscoll-Kraay, CCE, grupo medio, Durbin espacial,
DML, 2SLS, sensibilidad Oster y Cinelli-Hazlett, GSADF con tamaño corregido). Sin red. SEED=20261010, un hilo."""
from __future__ import annotations

import math
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
WEBB = np.sqrt(np.array([.5, 1, 1.5]))
WEBB = np.concatenate([-WEBB, WEBB])


# ------------------------------------------------------------------ efectos fijos
def _dm2(M, u, t, iters=100):
    """Quita media de unidad y de tiempo por proyecciones alternas (panel no balanceado). M: n×k."""
    M = M.astype(float).copy()
    nu, nt = u.max() + 1, t.max() + 1
    cu, ct = np.bincount(u, minlength=nu)[:, None], np.bincount(t, minlength=nt)[:, None]
    for _ in range(iters):
        su = np.zeros((nu, M.shape[1]))
        np.add.at(su, u, M)
        M -= (su / cu)[u]
        st = np.zeros((nt, M.shape[1]))
        np.add.at(st, t, M)
        M -= (st / ct)[t]
        if np.abs(su / cu).max() < 1e-12:
            break
    return M


def _trend_out(M, u, tt):
    """Quita, por unidad, constante y tendencia lineal."""
    M = M.astype(float).copy()
    for g in np.unique(u):
        i = u == g
        Z = np.column_stack([np.ones(i.sum()), tt[i] - tt[i].mean()])
        M[i] -= Z @ np.linalg.lstsq(Z, M[i], rcond=None)[0]
    return M


def codif(df, unit, time):
    u = pd.factorize(df[unit])[0]
    t = pd.factorize(df[time], sort=True)[0]
    return u, t


def fit_fe(df, y, xs, unit, time, clus, mode="ute", B=999, seed=SEED, boot=True):
    """MCO con FE. mode: 'ute' = unidad + tiempo; 'utrend' = unidad + tendencia lineal por unidad (sin FE de tiempo).
    Devuelve dict con coef, se (CR1 por clúster), t, p_wcb (restringido, Webb, B réplicas), r2 within, df.
    Se asume df sin NaN en y, xs."""
    d = df.reset_index(drop=True)
    u, t = codif(d, unit, time)
    g = pd.factorize(d[clus])[0]
    G = g.max() + 1
    M = d[[y] + xs].to_numpy(float)
    if mode == "ute":
        Mt = _dm2(M, u, t)
        nfe = u.max() + 1 + t.max()
    else:
        tt = d[time].to_numpy(float)
        Mt = _trend_out(M, u, tt)
        nfe = 2 * (u.max() + 1)
    yt, X = Mt[:, 0], Mt[:, 1:]
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ yt
    e = yt - X @ b
    corr = G / (G - 1) * (n - 1) / max(n - k - nfe, 1)
    S = np.zeros((G, k))
    np.add.at(S, g, X * e[:, None])
    V = corr * XtX_inv @ (S.T @ S) @ XtX_inv
    se = np.sqrt(np.diag(V))
    tst = b / se
    r2 = 1 - (e @ e) / (yt @ yt)
    df_res = max(n - k - nfe, 1)
    s2 = (e @ e) / df_res
    se_ols = np.sqrt(np.diag(XtX_inv) * s2)
    out = dict(xs=xs, coef=b, se=se, t=tst, p_cr1=2 * stats.t.sf(np.abs(tst), G - 1), n=n, G=G, r2_within=r2,
               df_res=df_res, se_ols=se_ols, nfe=nfe, yt=yt, X=X, e=e, g=g)
    if boot:
        rng = np.random.default_rng(seed)
        pw = np.empty(k)
        W = WEBB[rng.integers(0, 6, size=(G, B))][g]          # n×B (pesos por clúster)
        for j in range(k):
            idx = [i for i in range(k) if i != j]
            if idx:
                br = np.linalg.lstsq(X[:, idx], yt, rcond=None)[0]
                fit_r = X[:, idx] @ br
            else:
                fit_r = np.zeros(n)
            ur = yt - fit_r
            Ys = fit_r[:, None] + W * ur[:, None]
            bs = XtX_inv @ (X.T @ Ys)
            Es = Ys - X @ bs
            z = X @ XtX_inv[j]
            Sg = np.zeros((G, B))
            np.add.at(Sg, g, z[:, None] * Es)
            ses = np.sqrt(corr * (Sg ** 2).sum(0))
            ts = bs[j] / ses
            pw[j] = (1 + (np.abs(ts) >= abs(tst[j])).sum()) / (B + 1)
        out["p_wcb"] = pw
    return out


def driscoll_kraay(df, y, xs, unit, time, bw=2):
    from linearmodels.panel import PanelOLS
    d = df.set_index([unit, time])
    m = PanelOLS(d[y], d[xs], entity_effects=True, time_effects=True, drop_absorbed=True)
    r = m.fit(cov_type="kernel", kernel="bartlett", bandwidth=bw)
    return pd.DataFrame({"coef": r.params, "se": r.std_errors, "p": r.pvalues})


def oster_delta(yt, X, j, r2_long, rmax_mult=1.3):
    """delta (aprox. de Oster 2019 con R2 within): relación de selección en no observables que anularía el coef."""
    xj = X[:, j]
    bs = (xj @ yt) / (xj @ xj)
    r2_short = 1 - ((yt - bs * xj) ** 2).sum() / (yt @ yt)
    bl = np.linalg.lstsq(X, yt, rcond=None)[0][j]
    rmax = min(rmax_mult * r2_long, 1.0)
    den = (bs - bl) * (rmax - r2_long)
    return dict(beta_corto=float(bs), beta_largo=float(bl), r2_corto=float(r2_short), rmax=float(rmax),
                delta=float(bl * (r2_long - r2_short) / den) if abs(den) > 1e-12 else float("nan"))


def cinelli_hazlett(t, dfres, alpha=0.05):
    f = abs(t) / math.sqrt(dfres)
    rv = 0.5 * (math.sqrt(f ** 4 + 4 * f ** 2) - f ** 2)
    fa = f - stats.t.ppf(1 - alpha / 2, dfres - 1) / math.sqrt(dfres - 1)
    rva = 0.5 * (math.sqrt(fa ** 4 + 4 * fa ** 2) - fa ** 2) if fa > 0 else 0.0
    return dict(RV_q1=rv, RV_q1_alpha05=rva)


# ------------------------------------------------------------------ CCE y grupo medio
def mg(df, y, xs, unit, extra_cs=(), trend=False):
    """Grupo medio (Pesaran-Smith). Si extra_cs no vacío: CCEMG (medias de sección cruzada de y y xs por periodo
    añadidas con carga heterogénea). df debe traer la columna 'tt' (periodo ordenado)."""
    cs = None
    if extra_cs:
        cs = df.groupby("tt")[[y] + xs].mean().add_suffix("_bar")
    betas = []
    for _, h in df.groupby(unit):
        h = h.sort_values("tt")
        Z = [np.ones(len(h))]
        if trend:
            Z.append(h.tt.to_numpy(float))
        Z += [h[x].to_numpy() for x in xs]
        if cs is not None:
            c = cs.loc[h.tt]
            Z += [c[col].to_numpy() for col in c.columns]
        Z = np.column_stack(Z)
        if len(h) <= Z.shape[1] + 1:
            continue
        bb = np.linalg.lstsq(Z, h[y].to_numpy(), rcond=None)[0]
        betas.append(bb[1 + int(trend): 1 + int(trend) + len(xs)])
    B_ = np.array(betas)
    m_, s_ = B_.mean(0), B_.std(0, ddof=1) / np.sqrt(len(B_))
    return dict(coef=m_, se=s_, p=2 * stats.t.sf(np.abs(m_ / s_), len(B_) - 1), N_unidades=len(B_))


def ccep(df, y, xs, unit):
    """CCE agrupado (CCEP): quita por unidad la proyección sobre [1, ȳ_t, x̄_t] y estima pendiente común.
    se: sandwich por unidad."""
    cs = df.groupby("tt")[[y] + xs].mean()
    Xs, Ys, U = [], [], []
    for gi, h in df.groupby(unit):
        c = cs.loc[h.tt].to_numpy()
        Z = np.column_stack([np.ones(len(h)), c])
        if len(h) <= Z.shape[1] + 1:
            continue
        P = np.eye(len(h)) - Z @ np.linalg.pinv(Z)
        Ys.append(P @ h[y].to_numpy())
        Xs.append(P @ h[xs].to_numpy())
        U += [gi] * len(h)
    X, Yv = np.vstack(Xs), np.concatenate(Ys)
    A = np.linalg.inv(X.T @ X)
    b = A @ X.T @ Yv
    e = Yv - X @ b
    U = np.array(U)
    S = np.array([X[U == g_].T @ e[U == g_] for g_ in np.unique(U)])
    V = A @ (S.T @ S) @ A * len(S) / (len(S) - 1)
    se = np.sqrt(np.diag(V))
    return dict(coef=b, se=se, p=2 * stats.t.sf(np.abs(b / se), len(S) - 1), N_unidades=len(S), n=len(Yv))


# ------------------------------------------------------------------ Durbin espacial
def matriz_w(coords, k=4):
    """W de k vecinos más próximos (distancia entre centroides), normalizada por filas. coords: n×2 (m)."""
    D = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(D, np.inf)
    W = np.zeros_like(D)
    for i in range(len(D)):
        W[i, np.argsort(D[i])[:k]] = 1.0
    return W / W.sum(1, keepdims=True)


def sdm_fe(Y, Xs, W, nsim=2000, seed=SEED):
    """Durbin espacial con FE de unidad y tiempo (panel balanceado). Y: N×T, Xs: lista de arrays N×T.
    ML concentrada en rho. Efectos directos/indirectos con IC por simulación normal (Hessiano numérico)."""
    from scipy.optimize import minimize_scalar
    N, T = Y.shape
    k = len(Xs)

    def dm(A):
        return A - A.mean(1, keepdims=True) - A.mean(0, keepdims=True) + A.mean()
    y = dm(Y).ravel(order="F")
    Wy = dm(W @ Y).ravel(order="F")
    cols = [dm(x).ravel(order="F") for x in Xs] + [dm(W @ x).ravel(order="F") for x in Xs]
    Z = np.column_stack(cols)
    lam = np.linalg.eigvals(W).real

    def resid(r):
        return y - r * Wy

    def ll(r, gam):
        e = resid(r) - Z @ gam
        return -N * T / 2 * np.log(e @ e / (N * T)) + T * np.log(1 - r * lam).sum()

    def conc(r):
        e = resid(r)
        gam = np.linalg.lstsq(Z, e, rcond=None)[0]
        return -ll(r, gam)
    res = minimize_scalar(conc, bounds=(-0.95, 0.95), method="bounded")
    rho = res.x
    gam = np.linalg.lstsq(Z, resid(rho), rcond=None)[0]
    th = np.concatenate([[rho], gam])
    f = lambda p: ll(p[0], p[1:])  # noqa: E731
    npar = len(th)
    H = np.zeros((npar, npar))
    h = 1e-4 * np.maximum(1, np.abs(th))
    for i in range(npar):
        for j in range(i, npar):
            ei, ej = np.zeros(npar), np.zeros(npar)
            ei[i], ej[j] = h[i], h[j]
            H[i, j] = H[j, i] = (f(th + ei + ej) - f(th + ei - ej) - f(th - ei + ej) + f(th - ei - ej)) / (4 * h[i] * h[j])
    cov = np.linalg.inv(-H)
    rng = np.random.default_rng(seed)
    draws = rng.multivariate_normal(th, cov, size=nsim)
    draws[:, 0] = np.clip(draws[:, 0], -0.97, 0.97)
    I = np.eye(N)
    dire, indi = np.empty((nsim, k)), np.empty((nsim, k))
    for s in range(nsim):
        r = draws[s, 0]
        Sinv = np.linalg.inv(I - r * W)
        for j in range(k):
            S = Sinv @ (draws[s, 1 + j] * I + draws[s, 1 + k + j] * W)
            dire[s, j] = np.trace(S) / N
            indi[s, j] = S.sum() / N - dire[s, j]
    Sinv = np.linalg.inv(I - rho * W)
    pt = {"dir": [], "ind": []}
    for j in range(k):
        S = Sinv @ (gam[j] * I + gam[k + j] * W)
        pt["dir"].append(np.trace(S) / N)
        pt["ind"].append(S.sum() / N - np.trace(S) / N)

    def ci(a):
        return np.percentile(a, [2.5, 97.5], axis=0)

    def pv(a, p0):
        return np.minimum(1, 2 * np.minimum((a <= 0).mean(0), (a >= 0).mean(0)))
    return dict(rho=rho, rho_se=float(np.sqrt(cov[0, 0])), gam=gam, N=N, T=T, loglik=float(-res.fun),
                direct=np.array(pt["dir"]), indirect=np.array(pt["ind"]), dir_ci=ci(dire), ind_ci=ci(indi),
                dir_p=pv(dire, None), ind_p=pv(indi, None))


# ------------------------------------------------------------------ DML (PLR con FE y validación cruzada por provincia)
def dml_plr(df, y, d, controls, unit, time, clus, seed=SEED, nfold=5):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GroupKFold
    dd = df.dropna(subset=[y, d] + controls).reset_index(drop=True)
    u, t = codif(dd, unit, time)
    M = _dm2(dd[[y, d] + controls].to_numpy(float), u, t)
    yt, dt, Xc = M[:, 0], M[:, 1], M[:, 2:]
    ry, rd = np.zeros(len(dd)), np.zeros(len(dd))
    # permutación determinista de provincias para los pliegues
    gcod = pd.factorize(dd[unit])[0]
    perm = np.random.default_rng(seed).permutation(gcod.max() + 1)
    for tr, te in GroupKFold(n_splits=nfold).split(Xc, groups=perm[gcod]):
        for tgt, res_ in ((yt, ry), (dt, rd)):
            m = RandomForestRegressor(n_estimators=200, min_samples_leaf=5, max_features=0.5, n_jobs=1, random_state=seed)
            m.fit(Xc[tr], tgt[tr])
            res_[te] = tgt[te] - m.predict(Xc[te])
    th = (rd @ ry) / (rd @ rd)
    psi = (ry - th * rd) * rd
    g = pd.factorize(dd[clus])[0]
    G = g.max() + 1
    sg = np.bincount(g, weights=psi)
    se = np.sqrt(G / (G - 1) * (sg ** 2).sum()) / (rd @ rd)
    return dict(theta=float(th), se=float(se), p=float(2 * stats.t.sf(abs(th / se), G - 1)), n=len(dd), G=int(G),
                r2_y=float(1 - (ry ** 2).sum() / (yt ** 2).sum()), r2_d=float(1 - (rd ** 2).sum() / (dt ** 2).sum()))


# ------------------------------------------------------------------ 2SLS
def iv2sls(y, X, Z, cl, B=0):
    """2SLS: y, X (endógenas + exógenas), Z (instrumentos + exógenas). SE por clúster CR1. Devuelve coef, se, F primera etapa."""
    PZ = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    Xh = PZ @ X
    A = np.linalg.inv(Xh.T @ X)
    b = A @ Xh.T @ y
    e = y - X @ b
    g = pd.factorize(cl)[0]
    G = g.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, g, Xh * e[:, None])
    n, k = X.shape
    V = A @ (S.T @ S) @ A.T * G / (G - 1) * (n - 1) / max(n - k, 1)
    return b, np.sqrt(np.diag(V))


# ------------------------------------------------------------------ GSADF con tamaño corregido (misma implementación que v5/R1B)
def _prefijos(y):
    dy = np.diff(y)
    m = np.column_stack([np.ones_like(y[1:-1]), y[1:-1], dy[:-1], dy[1:]])
    p = np.zeros((len(m) + 1, 4, 4))
    p[1:] = np.cumsum(m[:, :, None] * m[:, None, :], axis=0)
    return p, len(m)


def bsadf_path(y, w0, ab):
    p, n = _prefijos(y)
    a, b = ab
    s = p[b + 1] - p[a]
    xtx, xty = s[:, :3, :3], s[:, :3, 3]
    inv = np.linalg.inv(xtx + 1e-12 * np.eye(3))
    beta = np.einsum("nij,nj->ni", inv, xty)
    ssr = s[:, 3, 3] - np.einsum("ni,ni->n", beta, xty)
    s2 = np.maximum(ssr, 1e-300) / ((b - a + 1) - 3)
    t = beta[:, 1] / np.sqrt(s2 * inv[:, 1, 1])
    m = np.full((n, n), -np.inf)
    m[b, a] = t
    return m.max(axis=1)


def ar_fit(dy, pmax=4):
    best = None
    for p in range(0, pmax + 1):
        yy = dy[p:]
        X = np.column_stack([np.ones(len(yy))] + [dy[p - j - 1: len(dy) - j - 1] for j in range(p)])
        b = np.linalg.lstsq(X, yy, rcond=None)[0]
        e = yy - X @ b
        bic = len(yy) * math.log((e ** 2).mean()) + (p + 1) * math.log(len(yy))
        if best is None or bic < best[0]:
            best = (bic, p, b, e)
    _, p, b, e = best
    return b[0], b[1:], e - e.mean(), p


def sim_nula(y0, dy_ini, c, phi, e_pool, T, rng):
    p = len(phi)
    dy = np.empty(T - 1)
    dy[:p] = dy_ini[:p]
    ee = rng.choice(e_pool, size=T - 1)
    for t in range(p, T - 1):
        dy[t] = c + (phi @ dy[t - p:t][::-1] if p else 0.0) + ee[t]
    return np.concatenate([[y0], y0 + np.cumsum(dy)])


def gsadf_corr(y, nboot, seed):
    T = len(y)
    r0 = 0.01 + 1.8 / math.sqrt(T)
    w0 = max(int(math.floor(r0 * T)), 8)
    n = T - 2
    ab = np.triu_indices(n, k=w0 - 1)
    bs = bsadf_path(y, w0, ab)
    gs = float(bs[w0 - 1:].max())
    dy = np.diff(y)
    c, phi, e, p = ar_fit(dy)
    rng = np.random.default_rng(seed)
    paths = np.empty((nboot, n))
    for i in range(nboot):
        paths[i] = bsadf_path(sim_nula(y[0], dy, c, phi, e, T, rng), w0, ab)
    bmax = paths[:, w0 - 1:].max(axis=1)
    cv_path = np.quantile(paths, 0.95, axis=0)
    sobre = np.zeros(n, bool)
    sobre[w0 - 1:] = bs[w0 - 1:] > cv_path[w0 - 1:]
    L = math.ceil(math.log(T))
    eps, i = [], 0
    while i < n:
        if sobre[i]:
            j = i
            while j + 1 < n and sobre[j + 1]:
                j += 1
            if j - i + 1 >= L:
                eps.append((i + 2, j + 2))
            i = j + 1
        else:
            i += 1
    return dict(T=T, w0=w0, gsadf=gs, cv95=float(np.quantile(bmax, .95)), p=float((1 + (bmax >= gs).sum()) / (nboot + 1)),
                ar_p=int(p), eps=eps)


def bh(p):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    adj = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(adj, 1.0)
    return out
