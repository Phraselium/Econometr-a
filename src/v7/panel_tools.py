"""Herramientas de panel validadas (V7-R2). Capa C4 (metodologico, solo datos simulados en su validacion).

Convenciones: y es (N, T); X es (N, T, k); panel balanceado. ARDL(p, q): p retardos de y y retardos 0..q de x,
en forma ECM: dy_t = phi*(y_{t-1} - theta'x_{t-1}) + sum_{j<p} lam_j dy_{t-j} + sum_{j<q} d_j' dx_{t-j} + c.
(q=1 equivale a dx contemporaneo). Todo lo aleatorio usa SEED = 20261010 por defecto.
Referencias (NO VERIFICADAS en esta sesion, sin acceso a Crossref): Pesaran-Smith 1995; Pesaran-Shin-Smith 1999;
Chudik-Pesaran 2015; Pesaran 2007; Westerlund 2007; Pedroni 1999/2004; Webb 2014; Driscoll-Kraay 1998.
"""
from __future__ import annotations

import numpy as np
from scipy import stats
from scipy.optimize import minimize

SEED = 20261010
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])


def _ols(d, Z):
    """MCO: devuelve coef, residuos, (Z'Z)^-1."""
    ZtZi = np.linalg.pinv(Z.T @ Z)
    b = ZtZi @ (Z.T @ d)
    return b, d - Z @ b, ZtZi


def _build(y, X, p, q, s, extra=None):
    """Diseno ECM de una unidad. y (T,), X (T,k). Devuelve d, L=[ylag, Xlag], W=[const, dX.., dy.., extra]."""
    T, k = X.shape
    dy, dX = np.diff(y), np.diff(X, axis=0)
    t = np.arange(s, T)
    d = dy[t - 1]
    L = np.column_stack([y[t - 1], X[t - 1]])
    W = [np.ones((len(t), 1))]
    for j in range(q):
        W.append(dX[t - 1 - j])
    for j in range(1, p):
        W.append(dy[t - 1 - j][:, None])
    if extra is not None:
        W.append(extra[t])
    return d, L, np.hstack(W)


def _start(p, q, extra_lags=0):
    return max(p, q, 1, extra_lags)


def _cs_extra(y, X, pT):
    """Aumento CS: z_{t-1} (niveles de medias transversales) y dz_{t-j}, j=0..pT-1."""
    Z = np.column_stack([y.mean(0)] + [X[:, :, j].mean(0) for j in range(X.shape[2])])  # (T,1+k)
    T = Z.shape[0]
    cols = [np.vstack([np.full((1, Z.shape[1]), np.nan), Z[:-1]])]
    dZ = np.vstack([np.full((1, Z.shape[1]), np.nan), np.diff(Z, axis=0)])
    for j in range(pT):
        cols.append(np.vstack([np.full((j, Z.shape[1]), np.nan), dZ[:T - j]]))
    return np.hstack(cols)


def _theta_delta(b, V, k):
    """theta = -b_x/phi con metodo delta. b=[phi, bx(k)], V cov. Devuelve theta, cov_theta."""
    phi, bx = b[0], b[1:1 + k]
    th = -bx / phi
    G = np.zeros((k, 1 + k))
    G[:, 0] = bx / phi ** 2
    G[:, 1:] = -np.eye(k) / phi
    return th, G @ V[:1 + k, :1 + k] @ G.T


def _units(y, X, p, q, cs, pT):
    N, T = y.shape
    s = _start(p, q, pT if cs else 0)
    ex = _cs_extra(y, X, pT) if cs else None
    return [_build(y[i], X[i], p, q, s, ex) for i in range(N)]


def mg(y, X, p=2, q=1, cs=False, pT=None):
    """Mean Group (Pesaran-Smith 1995) en ECM; con cs=True es CS-ARDL/CCE-ECM (Chudik-Pesaran 2015) con
    pT=floor(T^{1/3}) retardos de las medias transversales. Largo plazo = media de theta_i; EE no parametrico."""
    N, T = y.shape
    k = X.shape[2]
    pT = int(np.floor(T ** (1 / 3))) if pT is None else pT
    th, ph, sph = [], [], []
    for d, L, W in _units(y, X, p, q, cs, pT):
        Z = np.hstack([L, W])
        b, e, ZtZi = _ols(d, Z)
        V = ZtZi * (e @ e) / (len(d) - Z.shape[1])
        t_i, _ = _theta_delta(b, V, k)
        th.append(t_i)
        ph.append(b[0])
        sph.append(np.sqrt(V[0, 0]))
    th, ph = np.array(th), np.array(ph)
    # EE no parametrico; para theta se usa la varianza muestral de theta_i (robusta a theta_i extremos via MG simple)
    se = th.std(0, ddof=1) / np.sqrt(N)
    return dict(theta=th.mean(0), se_theta=se, V_theta=np.atleast_2d(np.cov(th.T)) / N, theta_i=th,
                phi=ph.mean(), se_phi=ph.std(ddof=1) / np.sqrt(N), phi_i=ph, se_phi_i=np.array(sph))


def cs_demean(y, X):
    """Demeaning transversal: resta en cada t la media entre unidades de y y de x (alternativa a CS-ARDL/CS-DL)."""
    return y - y.mean(0, keepdims=True), X - X.mean(0, keepdims=True)


def cs_ardl(y, X, p=2, q=1, pT=None):
    """CS-ARDL / CCE-ECM (Chudik-Pesaran 2015), largo plazo MG. Atajo de mg(cs=True)."""
    return mg(y, X, p, q, cs=True, pT=pT)


def pmg(y, X, p=2, q=1, theta0=None, se="info"):
    """PMG (Pesaran-Shin-Smith 1999) por maxima verosimilitud concentrada en theta (BFGS; equivalente a la
    retrosustitucion de PSS). EE de theta: se='info' (defecto; informacion) o 'sandwich' (Huber-White de las puntuaciones por unidad;
    en el MC cubre peor que 'info'; para inferencia usar pmg_bootstrap) (informacion
    [sum phi_i^2/sig_i^2 X~_i'X~_i]^-1); ambas matrices se devuelven (V_info, V_sandwich).
    phi_i y EE por unidad condicionales en theta-hat."""
    N, T = y.shape
    k = X.shape[2]
    parts = []
    for d, L, W in _units(y, X, p, q, False, 0):
        Mw = np.eye(len(d)) - W @ np.linalg.pinv(W)
        parts.append((Mw @ d, Mw @ L[:, 0], Mw @ L[:, 1:], len(d), W.shape[1]))

    DT, YL, XL = (np.array([a[i] for a in parts]) for i in range(3))  # (N,n), (N,n), (N,n,k)
    n_ = parts[0][3]
    dtdt = (DT * DT).sum(1)

    def prof(th):  # verosimilitud concentrada vectorizada
        xi = YL - XL @ th
        rss = dtdt - (xi * DT).sum(1) ** 2 / (xi * xi).sum(1)
        return float(n_ * np.log(np.maximum(rss, 1e-12) / n_).sum())

    start = mg(y, X, p, q)["theta"] if theta0 is None else np.asarray(theta0, float)
    start = np.clip(start, -10, 10)
    r = minimize(prof, start, method="BFGS", options=dict(gtol=1e-8))
    th = r.x
    ph, sph, info = [], [], np.zeros((k, k))
    scores = []
    for dt, yl, Xl, n, _w in parts:
        def li(t, dt=dt, yl=yl, Xl=Xl, n=n):
            xi_ = yl - Xl @ t
            return -0.5 * n * np.log(max(dt @ dt - (xi_ @ dt) ** 2 / (xi_ @ xi_), 1e-12) / n)
        h = 1e-5
        scores.append(np.array([(li(th + h * np.eye(k)[j]) - li(th - h * np.eye(k)[j])) / (2 * h) for j in range(k)]))
    for dt, yl, Xl, n, nw in parts:
        xi = yl - Xl @ th
        f = (xi @ dt) / (xi @ xi)
        rss = dt @ dt - f * (xi @ dt)
        s2 = rss / n
        ph.append(f)
        sph.append(np.sqrt(rss / (n - nw - 1) / (xi @ xi)))
        info += f ** 2 / s2 * (Xl.T @ Xl)
    Vi = np.linalg.pinv(info)
    Sc = np.array(scores)
    Vsw = Vi @ (Sc.T @ Sc) @ Vi * N / (N - 1)  # sandwich Huber-White por unidad sobre la verosimilitud concentrada
    V = Vsw if se == "sandwich" else Vi
    ph = np.array(ph)
    return dict(theta=th, se_theta=np.sqrt(np.diag(V)), V_theta=V, V_info=Vi, V_sandwich=Vsw, phi=ph.mean(), se_phi=ph.std(ddof=1) / np.sqrt(N),
                phi_i=ph, se_phi_i=np.array(sph), converged=bool(r.success), loglik_prof=-r.fun / 2)


def pmg_bootstrap(y, X, p=2, q=1, B=199, seed=SEED, demean=False):
    """Bootstrap por unidades (pairs cluster: se remuestrean las N unidades con reposicion) del PMG.
    Con demean=True las unidades se remuestrean sobre los datos BRUTOS y el demeaning se re-aplica en cada
    remuestra. Devuelve EE y matriz de covarianza de theta."""
    rng = np.random.default_rng(seed)
    N = y.shape[0]
    th0 = pmg(*(cs_demean(y, X) if demean else (y, X)), p, q)["theta"]
    ths = []
    for _ in range(B):
        i = rng.integers(0, N, N)
        yy, XX = (cs_demean(y[i], X[i]) if demean else (y[i], X[i]))  # demeaning re-aplicado en cada remuestra
        ths.append(pmg(yy, XX, p, q, theta0=th0)["theta"])
    V = np.atleast_2d(np.cov(np.array(ths).T))
    return dict(se_theta=np.sqrt(np.diag(V)), V_theta=V)


def cs_dl(y, X, pT=None):
    """CS-DL (Chudik-Mohaddes-Pesaran-Raissi 2016): y_it = a_i + theta_i'x_it + sum_{j=0}^{pT} g_ij'dx_{i,t-j}
    + medias transversales (y, x) y sus pT retardos + e. Largo plazo = MG de theta_i (sin cociente phi)."""
    N, T, k = X.shape
    pT = int(np.floor(T ** (1 / 3))) if pT is None else pT
    Z = np.column_stack([y.mean(0)] + [X[:, :, j].mean(0) for j in range(k)])
    t = np.arange(pT + 1, T)
    th = []
    ex = np.hstack([Z[t - j] for j in range(pT + 1)])
    for i in range(N):
        dX = np.diff(X[i], axis=0)
        cols = [np.ones((len(t), 1)), X[i][t]] + [dX[t - 1 - j] for j in range(pT + 1)]
        Zm = np.hstack(cols + [ex])
        b, _, _ = _ols(y[i][t], Zm)
        th.append(b[1:1 + k])
    th = np.array(th)
    return dict(theta=th.mean(0), se_theta=th.std(0, ddof=1) / np.sqrt(N), V_theta=np.atleast_2d(np.cov(th.T)) / N,
                theta_i=th, phi=np.nan)


def jackknife_phi(fn, y, X, **kw):
    """Corrector de sesgo de muestra finita de phi: 2*phi_total - media(phi en mitades temporales)."""
    T = y.shape[1]
    h = T // 2
    ph = fn(y, X, **kw)["phi"]
    a, b = fn(y[:, :h], X[:, :h], **kw)["phi"], fn(y[:, T - h:], X[:, T - h:], **kw)["phi"]
    return 2 * ph - 0.5 * (a + b)


def dfe(y, X, p=2, q=1):
    """DFE: ECM con efectos fijos de unidad y todos los coeficientes comunes; EE agrupados por unidad."""
    N, T = y.shape
    k = X.shape[2]
    ds, Zs = [], []
    for d, L, W in _units(y, X, p, q, False, 0):
        Z = np.hstack([L, W[:, 1:]])
        ds.append(d - d.mean())
        Zs.append(Z - Z.mean(0))
    D, Z = np.concatenate(ds), np.vstack(Zs)
    b, e, ZtZi = _ols(D, Z)
    n = len(ds[0])
    meat = sum(Zs[i].T @ (e[i * n:(i + 1) * n, None] * np.ones((1, 1))) @ (e[i * n:(i + 1) * n, None].T @ Zs[i])
               for i in range(N))
    V = ZtZi @ meat @ ZtZi * N / (N - 1)
    th, Vt = _theta_delta(b, V, k)
    return dict(theta=th, se_theta=np.sqrt(np.diag(Vt)), V_theta=Vt, phi=b[0], se_phi=np.sqrt(V[0, 0]))


def hausman_mg_pmg(mgres, pmgres, vpmg="info", var_diff="mg"):
    """Variantes: var_diff='mg' (defecto) usa solo la varianza no parametrica de MG (conservador; unica variante con
    tamano en [0,02; 0,10] en el MC); var_diff='difference' usa V_MG - V_PMG con vpmg in {'info','sandwich'}."""
    pm = dict(pmgres)
    pm["V_theta"] = pmgres["V_info" if vpmg == "info" else "V_sandwich"]
    if var_diff == "mg":
        pm["V_theta"] = np.zeros_like(pm["V_theta"])
    return _hausman(mgres, pm)


def _hausman(mgres, pmgres):
    """Hausman sobre theta: H=(th_MG-th_PMG)'[V_MG-V_PMG]^-1(..) ~ chi2(k) bajo H0 (PMG eficiente).
    Si V_MG-V_PMG no es definida positiva se usa la pseudo-inversa y se marca pd=False."""
    dth = mgres["theta"] - pmgres["theta"]
    Vd = np.atleast_2d(mgres["V_theta"]) - np.atleast_2d(pmgres["V_theta"])
    pd = bool(np.all(np.linalg.eigvalsh((Vd + Vd.T) / 2) > 0))
    H = float(dth @ np.linalg.pinv(Vd) @ dth)
    H = max(H, 0.0)
    return dict(H=H, p=float(stats.chi2.sf(H, len(dth))), pd=pd)


# ------------------------------------------------------------------ CIPS
K1, K2 = 6.19, 2.61  # truncacion de Pesaran (2007), caso con constante: NO VERIFICADOS


def cips(y, p=1, trend=False, trunc=False, sbc=False, pmax=4):
    """CIPS (Pesaran 2007). trend: constante y tendencia; trunc: CIPS* (t_i truncado a [-K1, K2]);
    sbc: retardos de cada CADF por SBC (0..pmax). Rechaza (raiz unitaria) con valores BAJOS."""
    N, T = y.shape
    yb = y.mean(0)
    dyb = np.diff(yb)
    ts = []
    for i in range(N):
        dy = np.diff(y[i])
        best = None
        for pp in (range(pmax + 1) if sbc else [p]):
            t = np.arange(pmax + 1 if sbc else pp + 1, T)
            cols = [np.ones(len(t))] + ([t.astype(float)] if trend else [])
            k0 = len(cols)
            cols += [y[i][t - 1], yb[t - 1], dyb[t - 1]]
            for j in range(1, pp + 1):
                cols += [dy[t - 1 - j], dyb[t - 1 - j]]
            Z = np.column_stack(cols)
            d = dy[t - 1]
            b, e, ZtZi = _ols(d, Z)
            n = len(d)
            tst = b[k0] / np.sqrt(ZtZi[k0, k0] * (e @ e) / (n - Z.shape[1]))
            crit = n * np.log(e @ e / n) + Z.shape[1] * np.log(n)
            if best is None or crit < best[0]:
                best = (crit, tst)
        ts.append(best[1])
    ts = np.array(ts)
    if trunc:
        ts = np.clip(ts, -K1, K2)
    return float(ts.mean())


def cips_critical_values(N, T, p=1, reps=1000, seed=SEED, **kw):
    """Valores criticos simulados (cuantiles 1, 5, 10 %) y muestra nula completa de CIPS."""
    sim = sim_null(lambda y: cips(y, p, **kw), N, T, reps, seed)
    return dict(cv={q: float(np.quantile(sim, q)) for q in (.01, .05, .10)}, sim=sim)


def sim_null(fn, N, T, reps=1000, seed=SEED, k=0):
    """Distribucion nula simulada de fn(y[,X]) con paseos aleatorios independientes (sin dependencia transversal)."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(reps):
        y = np.cumsum(rng.standard_normal((N, T)), 1)
        if k:
            X = np.cumsum(rng.standard_normal((N, T, k)), 1)
            out.append(fn(y, X))
        else:
            out.append(fn(y))
    return np.array(out)


def sim_pvalue(stat, sim):
    """p de cola izquierda con correccion (1+#{sim<=stat})/(reps+1)."""
    sim = np.asarray(sim)
    return float((1 + np.sum(sim <= stat)) / (len(sim) + 1))


# ------------------------------------------------------------------ Westerlund
def _wl_stats(y, X, p):
    N, T = y.shape
    dy_all = np.diff(y, axis=1)
    ga = gt = 0.0
    num = den = 0.0
    a1s = []
    s2 = []
    for i in range(N):
        d, L, W = _build(y[i], X[i], p + 1, 1, max(p + 1, 1))
        Z = np.hstack([L, W])
        b, e, ZtZi = _ols(d, Z)
        n, m = Z.shape
        sig2 = e @ e / (n - m)
        a = b[0]
        a1 = 1 - b[L.shape[1] + 1 + X.shape[2]:].sum()  # alpha_i(1) = 1 - sum lambda
        gt += a / np.sqrt(ZtZi[0, 0] * sig2)
        ga += n * a / a1
        a1s.append(a1)
        # parcializar todo salvo y_{t-1}
        R = Z[:, 1:]
        Mr = np.eye(n) - R @ np.linalg.pinv(R)
        yt, dt = Mr @ L[:, 0], Mr @ d
        num += (yt @ dt) / sig2
        den += (yt @ yt) / sig2
        s2.append(sig2)
    alpha = num / den
    Tn = n
    return np.array([gt / N, ga / N, alpha / np.sqrt(1 / den), Tn * alpha / np.mean(a1s)])


def westerlund(y, X, p=1, B=199, block=None, seed=SEED):
    """Test tipo Westerlund (2007; variante, no el estadistico original): Gt, Ga, Pt, Pa (rechazo de H0 sin cointegracion con valores BAJOS). p por bootstrap
    por bloques circulares de las DIFERENCIAS (mismos bloques temporales en todas las unidades: conserva la
    dependencia transversal y la dinamica corta; H0 impuesta porque y*, x* son I(1) sin ECM).
    Variante: pooled ponderado por 1/sigma_i^2, parcializando tambien x_{t-1}; sin leads de dx."""
    N, T = y.shape
    k = X.shape[2]
    block = block or 2 * int(np.floor(T ** (1 / 3)))
    obs = _wl_stats(y, X, p)
    rng = np.random.default_rng(seed)
    D = np.concatenate([np.diff(y, axis=1)[:, :, None], np.diff(X, axis=1)], 2)  # (N,T-1,1+k)
    n = D.shape[1]
    nb = int(np.ceil(n / block))
    sims = np.empty((B, 4))
    for b in range(B):
        st = rng.integers(0, n, nb)
        idx = ((st[:, None] + np.arange(block)[None, :]) % n).ravel()[:n]
        Ds = D[:, idx, :]
        lev = np.concatenate([np.zeros((N, 1, 1 + k)), np.cumsum(Ds, 1)], 1)
        sims[b] = _wl_stats(lev[:, :, 0], lev[:, :, 1:], p)
    pv = (1 + (sims <= obs).sum(0)) / (B + 1)
    return dict(zip(["Gt", "Ga", "Pt", "Pa"], obs.tolist())) | dict(p=dict(zip(["Gt", "Ga", "Pt", "Pa"], pv.tolist())))


# ------------------------------------------------------------------ Pedroni
def _pedroni_stats(y, X, p):
    N, T = y.shape
    ts, num, den, s2s = [], 0.0, 0.0, []
    for i in range(N):
        Z = np.column_stack([np.ones(T), X[i]])
        _, e, _ = _ols(y[i], Z)
        de = np.diff(e)
        t = np.arange(p + 1, T)
        cols = [e[t - 1]] + [de[t - 1 - j] for j in range(1, p + 1)]
        Zc = np.column_stack(cols)
        d = de[t - 1]
        b, u, ZtZi = _ols(d, Zc)
        s2 = u @ u / (len(d) - Zc.shape[1])
        ts.append(b[0] / np.sqrt(ZtZi[0, 0] * s2))
        if p:
            R = Zc[:, 1:]
            Mr = np.eye(len(d)) - R @ np.linalg.pinv(R)
            et, dt = Mr @ Zc[:, 0], Mr @ d
        else:
            et, dt = Zc[:, 0], d
        num += et @ dt
        den += et @ et
        s2s.append(s2)
    panel = (num / den) / np.sqrt(np.mean(s2s) / den)
    return np.array([panel, np.sum(ts) / np.sqrt(N)])


def pedroni(y, X, p=1, sim=None, reps=500, seed=SEED):
    """Pedroni: panel-ADF (t agrupado) y group-ADF, sobre residuos de y_i = a_i + b_i'x_i + e_i.
    Las medias/varianzas tabuladas de Pedroni (1999/2004) NO se usan (NO VERIFICADAS): p simulado con paseos
    aleatorios independientes del mismo (N,T,k). `sim` (reps,2) permite reutilizar la simulacion."""
    N, T = y.shape
    obs = _pedroni_stats(y, X, p)
    if sim is None:
        sim = pedroni_null(N, T, X.shape[2], p, reps, seed)
    return dict(panel_adf=float(obs[0]), group_adf=float(obs[1]),
                p=dict(panel_adf=sim_pvalue(obs[0], sim[:, 0]), group_adf=sim_pvalue(obs[1], sim[:, 1])))


def pedroni_null(N, T, k, p=1, reps=500, seed=SEED):
    return sim_null(lambda y, X: _pedroni_stats(y, X, p), N, T, reps, seed, k=k)


# ------------------------------------------------------------------ pocos clusters
def _within(a, cl):
    a = np.asarray(a, float)
    out = a.copy()
    for c in np.unique(cl):
        m = cl == c
        out[m] -= a[m].mean(0)
    return out


def cluster_fe_t(y, X, cl, j):
    """Coef. y la t agrupada de la columna j en MCO con efectos fijos de cluster."""
    Xw, yw = _within(X, cl), _within(y, cl)
    b, e, XtXi = _ols(yw, Xw)
    meat = sum(np.outer(Xw[cl == c].T @ e[cl == c], Xw[cl == c].T @ e[cl == c]) for c in np.unique(cl))
    G = len(np.unique(cl))
    V = XtXi @ meat @ XtXi * G / (G - 1)
    return b[j], b[j] / np.sqrt(V[j, j])


def wild_cluster_boot(y, X, cl, j=0, B=999, seed=SEED, null=0.0):
    """Wild cluster bootstrap-t restringido con pesos de Webb (6 puntos) para H0: beta_j = null, FE de cluster.
    Devuelve coef, t, p bootstrap (simetrico). Adecuado con pocos clusters (p. ej. 17 CCAA)."""
    y, X, cl = np.asarray(y, float), np.asarray(X, float), np.asarray(cl)
    b0, t0 = cluster_fe_t(y, X, cl, j)
    keep = [c for c in range(X.shape[1]) if c != j]
    yr = y - X[:, j] * null
    if keep:
        Xr = _within(X[:, keep], cl)
        br, er, _ = _ols(_within(yr, cl), Xr)
        fit = (X[:, keep] - 0) @ br
        u = _within(yr, cl) - Xr @ br
    else:
        fit, u = np.zeros(len(y)), _within(yr, cl)
    rng = np.random.default_rng(seed)
    ids = np.unique(cl)
    pos = np.searchsorted(ids, cl)
    ts = np.empty(B)
    for bidx in range(B):
        w = rng.choice(WEBB, len(ids))[pos]
        ys = fit + X[:, j] * null + u * w
        ts[bidx] = cluster_fe_t(ys, X, cl, j)[1]
    return dict(coef=float(b0), t=float(t0), p_boot=float(np.mean(np.abs(ts) >= abs(t0 - 0))), B=B)


def driscoll_kraay(y, X, N, T, maxlag=None):
    """Driscoll-Kraay (1998) para MCO con FE de unidad; datos apilados por unidad (N*T filas, orden i-mayor).
    Devuelve coef, EE, t. Ventana Bartlett con m = floor(4 (T/100)^{2/9}) si no se indica."""
    cl = np.repeat(np.arange(N), T)
    Xw, yw = _within(X, cl), _within(y, cl)
    b, e, XtXi = _ols(yw, Xw)
    h = (Xw * e[:, None]).reshape(N, T, -1).sum(0)  # (T,k)
    m = int(np.floor(4 * (T / 100) ** (2 / 9))) if maxlag is None else maxlag
    S = h.T @ h
    for l in range(1, m + 1):
        G = h[l:].T @ h[:-l]
        S += (1 - l / (m + 1)) * (G + G.T)
    V = XtXi @ S @ XtXi
    se = np.sqrt(np.diag(V))
    return dict(coef=b, se=se, t=b / se)


def mg_dm_jackknife(y, X, p=2, q=1):
    """MG con demeaning transversal y EE por jackknife de unidades (dejar una unidad fuera y RE-aplicar el demeaning)."""
    N = y.shape[0]
    full = mg(*cs_demean(y, X), p, q)["theta"]
    lo = np.array([mg(*cs_demean(np.delete(y, i, 0), np.delete(X, i, 0)), p, q)["theta"] for i in range(N)])
    V = (N - 1) / N * ((lo - lo.mean(0)).T @ (lo - lo.mean(0)))
    return dict(theta=full, se_theta=np.sqrt(np.diag(np.atleast_2d(V))))


def jackknife_theta(fn, y, X, **kw):
    """Jackknife de mitades temporales sobre theta: 2*theta_total - media(theta en mitades)."""
    T = y.shape[1]
    h = T // 2
    a, b = fn(y[:, :h], X[:, :h], **kw)["theta"], fn(y[:, T - h:], X[:, T - h:], **kw)["theta"]
    return 2 * fn(y, X, **kw)["theta"] - 0.5 * (a + b)


def select_lags_sbc(y, X, pmax=4, qmax=4):
    """Seleccion de (p, q) por SBC sumado entre unidades, muestra comun (s = max(pmax, qmax)); p>=1, q>=1."""
    s = max(pmax, qmax)
    best = (np.inf, None)
    for p in range(1, pmax + 1):
        for q in range(1, qmax + 1):
            tot = 0.0
            for i in range(y.shape[0]):
                d, L, W = _build(y[i], X[i], p, q, s)
                Z = np.hstack([L, W])
                _, e, _ = _ols(d, Z)
                n = len(d)
                tot += n * np.log(e @ e / n) + Z.shape[1] * np.log(n)
            if tot < best[0]:
                best = (tot, (p, q))
    return best[1]
