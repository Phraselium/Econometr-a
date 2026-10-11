"""M1a v6: utilidades econométricas (FE absorbidos, EE por clúster, wild bootstrap, Driscoll-Kraay, Conley,
CCE, MG, SDM por 2SLS, DML con cross-fitting, Oster, Cinelli-Hazlett). Determinista, un hilo, sin red."""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy import stats
from scipy.sparse import csr_matrix, identity
from scipy.spatial import cKDTree

SEED = 20261010


# ---------------------------------------------------------------- absorción de efectos fijos
def absorb(Z, u, t, trend=False, tol=1e-9, maxit=300):
    """Residualiza columnas de Z (n,k) sobre FE de unidad (u: enteros), FE de año (t: enteros) y, si trend,
    tendencia lineal propia de cada unidad. Proyecciones alternas."""
    Z = np.array(Z, float, copy=True)
    if Z.ndim == 1:
        Z = Z[:, None]
    nu, nt = u.max() + 1, t.max() + 1
    cu = np.bincount(u, minlength=nu).astype(float)
    ct = np.bincount(t, minlength=nt).astype(float)
    tc = t.astype(float)
    tm = np.bincount(u, weights=tc, minlength=nu) / cu
    td = tc - tm[u]
    stt = np.bincount(u, weights=td * td, minlength=nu)
    stt[stt == 0] = np.inf
    for _ in range(maxit):
        prev = Z.copy()
        for j in range(Z.shape[1]):
            z = Z[:, j]
            z = z - (np.bincount(u, weights=z, minlength=nu) / cu)[u]
            if trend:
                b = np.bincount(u, weights=td * z, minlength=nu) / stt
                z = z - b[u] * td
            z = z - (np.bincount(t, weights=z, minlength=nt) / ct)[t]
            Z[:, j] = z
        if np.max(np.abs(Z - prev)) < tol:
            break
    return Z


def ols(y, X):
    Minv = np.linalg.pinv(X.T @ X)
    b = Minv @ (X.T @ y)
    return b, y - X @ b, Minv


def cr1(X, e, Minv, cl, k_abs):
    """EE CR1 por clúster (cl: enteros 0..G-1)."""
    G = cl.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, cl, X * e[:, None])
    n, k = X.shape
    c = G / (G - 1) * (n - 1) / max(n - k - k_abs, 1)
    return c * Minv @ (S.T @ S) @ Minv, G


def wild_p(y, X, Minv, cl, j, B, rng, kind="webb", k_abs=0):
    """p del wild cluster bootstrap con H0 impuesta (WCR) para el coeficiente j, sobre datos ya absorbidos.
    Usa estadísticos suficientes por clúster (A_g = X_g'X_g, S_g = X_g'u_r)."""
    n, k = X.shape
    G = cl.max() + 1
    b, e, _ = ols(y, X)
    V, _ = cr1(X, e, Minv, cl, k_abs)
    t0 = b[j] / np.sqrt(V[j, j])
    _, ur, _ = ols(y, np.delete(X, j, axis=1))
    A = np.zeros((G, k, k))
    S = np.zeros((G, k))
    for g in range(G):
        m = cl == g
        A[g] = X[m].T @ X[m]
        S[g] = X[m].T @ ur[m]
    if kind == "webb":
        vals = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])
        W = rng.choice(vals, size=(B, G))
    else:
        W = rng.choice([-1.0, 1.0], size=(B, G))
    dev = (W @ S) @ Minv
    sg = W[:, :, None] * S[None] - np.einsum("gkl,bl->bgk", A, dev)
    Vs = np.einsum("kl,bgl->bgk", Minv, sg)
    vj = (Vs[:, :, j] ** 2).sum(1) * (G / (G - 1) * (n - 1) / max(n - k - k_abs, 1))
    ts = dev[:, j] / np.sqrt(vj)
    return float((1 + np.sum(np.abs(ts) >= abs(t0) - 1e-12)) / (B + 1)), float(t0)


def dk_cov(X, e, Minv, t, L=2):
    T = t.max() + 1
    H = np.zeros((T, X.shape[1]))
    np.add.at(H, t, X * e[:, None])
    Om = H.T @ H
    for lag in range(1, L + 1):
        G = H[lag:].T @ H[:-lag]
        Om += (1 - lag / (L + 1)) * (G + G.T)
    return Minv @ Om @ Minv


def conley_cov(X, e, Minv, t, loc, xy, cutoff_km=50.0, L=2):
    """Conley-HAC simplificado: scores agregados por localización (municipio) y año; núcleo de Bartlett en distancia
    (mismo año) más Bartlett en el tiempo dentro de cada localización."""
    k = X.shape[1]
    T = t.max() + 1
    nl = loc.max() + 1
    H = np.zeros((nl, T, k))
    np.add.at(H, (loc, t), X * e[:, None])
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1)) / 1000.0
    K = np.clip(1 - d / cutoff_km, 0, None)
    Om = np.zeros((k, k))
    for s in range(T):
        Hs = H[:, s, :]
        Om += Hs.T @ K @ Hs
    for lag in range(1, L + 1):
        for s in range(lag, T):
            G = H[:, s, :].T @ H[:, s - lag, :]
            Om += (1 - lag / (L + 1)) * (G + G.T)
    return Minv @ Om @ Minv


# ---------------------------------------------------------------- sensibilidad (fórmulas de src/v5/r1b_sens.py)
def cinelli_hazlett(t, gl, alpha=0.05):
    f = abs(t) / np.sqrt(gl)
    r = 0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2)
    fa = f - stats.t.ppf(1 - alpha / 2, gl - 1) / np.sqrt(gl - 1)
    ra = 0.5 * (np.sqrt(fa ** 4 + 4 * fa ** 2) - fa ** 2) if fa > 0 else 0.0
    return float(r), float(ra)


def oster(bc, bl, r2c, r2l, rmax_mult=1.3):
    rmax = min(1.0, rmax_mult * r2l)
    if abs(bc - bl) < 1e-12 or r2l - r2c <= 1e-12 or rmax - r2l <= 1e-12:
        return np.nan, np.nan
    d = bl * (r2l - r2c) / ((bc - bl) * (rmax - r2l))
    b1 = bl - (bc - bl) * (rmax - r2l) / (r2l - r2c)
    return float(d), float(b1)


# ---------------------------------------------------------------- CCE y MG
def _avgs(y, X, t, with_y=True):
    nt = t.max() + 1
    cnt = np.bincount(t, minlength=nt).astype(float)
    Z = np.column_stack(([y] if with_y else []) + [X[:, j] for j in range(X.shape[1])])
    return np.column_stack([np.bincount(t, weights=Z[:, j], minlength=nt) / cnt for j in range(Z.shape[1])])[t]


def cce_p(y, X, u, t, cl):
    """CCEP de Pesaran (2006): cada unidad proyecta y y X fuera de [1, ybar_t, xbar_t]; luego MCO agrupado."""
    avg = _avgs(y, X, t)
    Yt, Xt, keep = np.zeros(len(y)), np.zeros_like(X), np.zeros(len(y), bool)
    for i in np.unique(u):
        m = np.where(u == i)[0]
        H = np.column_stack((np.ones(len(m)), avg[m]))
        if len(m) < H.shape[1] + 2:
            continue
        P = np.eye(len(m)) - H @ np.linalg.pinv(H)
        Yt[m], Xt[m], keep[m] = P @ y[m], P @ X[m], True
    b, e, Minv = ols(Yt[keep], Xt[keep])
    clk = np.unique(cl[keep], return_inverse=True)[1]
    nu = int(np.unique(u[keep]).size)
    V, G = cr1(Xt[keep], e, Minv, clk, k_abs=nu * (avg.shape[1] + 1))
    return b, V, G, int(keep.sum()), nu


def mean_group(y, X, u, t, cce=False, min_extra=2):
    avg = _avgs(y, X, t) if cce else None
    B = []
    for i in np.unique(u):
        m = np.where(u == i)[0]
        cols = [np.ones(len(m)), *[X[m, j] for j in range(X.shape[1])]]
        if cce:
            cols += [avg[m, j] for j in range(avg.shape[1])]
        H = np.column_stack(cols)
        if len(m) < H.shape[1] + min_extra:
            continue
        B.append(np.linalg.lstsq(H, y[m], rcond=None)[0][1:1 + X.shape[1]])
    B = np.array(B)
    n = len(B)
    return B.mean(0), B.std(0, ddof=1) / np.sqrt(n), n, B.std(0, ddof=1)


# ---------------------------------------------------------------- SDM por 2SLS
def sdm_2sls(y, X, u, t, cl, xy_u, k=5, trend=False, B=999, seed=SEED):
    """SDM por 2SLS sobre datos con FE absorbidos: y = rho Wy + X b + WX th + FE. Instrumentos W2X, W3X.
    W: k vecinos más cercanos por año entre las unidades presentes, estandarizada por filas. Impactos directo,
    indirecto y total por serie de potencias de W (muestra completa de unidades) e IC por simulación normal con la
    covarianza por clúster."""
    n, kx = X.shape
    Wy = np.zeros(n)
    WX, W2X, W3X = (np.zeros((n, kx)) for _ in range(3))
    for yr in np.unique(t):
        rows = np.where(t == yr)[0]
        if len(rows) <= k + 1:
            continue
        nb = cKDTree(xy_u[u[rows]]).query(xy_u[u[rows]], k=k + 1)[1][:, 1:]
        Wy[rows] = y[rows][nb].mean(1)
        for j in range(kx):
            WX[rows, j] = X[rows, j][nb].mean(1)
            W2X[rows, j] = WX[rows, j][nb].mean(1)
            W3X[rows, j] = W2X[rows, j][nb].mean(1)
    Wy_, WX_, W2X_, W3X_ = (absorb(a, u, t, trend) for a in (Wy, WX, W2X, W3X))
    R = np.column_stack((Wy_, X, WX_))
    Zi = np.column_stack((X, WX_, W2X_, W3X_))
    Rh = Zi @ (np.linalg.pinv(Zi.T @ Zi) @ (Zi.T @ R))
    b = np.linalg.lstsq(Rh, y, rcond=None)[0]
    e = y - R @ b
    V, G = cr1(Rh, e, np.linalg.pinv(Rh.T @ Rh), cl, k_abs=0)
    rho, beta, theta = b[0], b[1:1 + kx], b[1 + kx:]
    uu = np.unique(u)
    nu = len(uu)
    nb = cKDTree(xy_u[uu]).query(xy_u[uu], k=min(k, nu - 1) + 1)[1][:, 1:]
    Wf = csr_matrix((np.full(nb.size, 1.0 / nb.shape[1]), (np.repeat(np.arange(nu), nb.shape[1]), nb.ravel())),
                    shape=(nu, nu))
    P = 12
    trk, cur = [1.0], identity(nu, format="csr")
    for _ in range(P):
        cur = cur @ Wf
        trk.append(float(cur.diagonal().sum()) / nu)
    trk = np.array(trk)

    def impacts(rh, be, th):
        pw = rh ** np.arange(P + 1)
        dr = be * float((pw * trk).sum()) + th * float((pw[:-1] * trk[1:]).sum())
        tot = (be + th) / (1 - rh)
        return dr, tot - dr, tot
    d0, i0, t0 = impacts(rho, beta, theta)
    dr = np.random.default_rng(seed).multivariate_normal(b, V, size=B)
    dr = dr[np.abs(dr[:, 0]) < 0.98]
    sims = np.array([impacts(r[0], r[1:1 + kx], r[1 + kx:]) for r in dr])
    return {"rho": rho, "rho_se": float(np.sqrt(V[0, 0])), "beta": beta, "theta": theta, "dir": d0, "ind": i0,
            "tot": t0, "dir_se": sims[:, 0].std(0), "ind_se": sims[:, 1].std(0), "tot_se": sims[:, 2].std(0),
            "n": n, "G": G}


# ---------------------------------------------------------------- DML (PLR con cross-fitting agrupado)
def dml_plr(y, d, W, cl, seed=SEED, nfold=5, trees=150):
    """DML parcialmente lineal: y y d ya sin FE; nuisance = bosque aleatorio; folds por clúster (CCAA)."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import GroupKFold
    ry, rd = np.zeros(len(y)), np.zeros(len(y))
    for tr_, te_ in GroupKFold(n_splits=min(nfold, len(np.unique(cl)))).split(W, groups=cl):
        for tgt, out in ((y, ry), (d, rd)):
            rf = RandomForestRegressor(n_estimators=trees, min_samples_leaf=5, max_features=0.5, random_state=seed,
                                       n_jobs=1)
            rf.fit(W[tr_], tgt[tr_])
            out[te_] = tgt[te_] - rf.predict(W[te_])
    th = float((rd @ ry) / (rd @ rd))
    G = cl.max() + 1
    S = np.bincount(cl, weights=rd * (ry - th * rd), minlength=G)
    return th, float(np.sqrt(G / (G - 1) * (S ** 2).sum()) / (rd @ rd)), G


def dm_hln(e1, e2, h=1):
    d = np.asarray(e1, float) ** 2 - np.asarray(e2, float) ** 2
    n = len(d)
    dc = d - d.mean()
    lrv = dc @ dc / n
    for lag in range(1, h):
        lrv += 2 * (1 - lag / h) * (dc[lag:] @ dc[:-lag]) / n
    dm = d.mean() / np.sqrt(lrv / n) * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    return float(dm), float(2 * stats.t.sf(abs(dm), n - 1)), n


def holm_adj(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    out = np.empty(m)
    out[o] = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * p[o]))
    return out


def bh_adj(p):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    out = np.empty(m)
    out[o] = np.minimum(np.minimum.accumulate((p[o] * m / (np.arange(m) + 1))[::-1])[::-1], 1)
    return out
