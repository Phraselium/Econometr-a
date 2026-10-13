"""BVAR normal-Wishart inversa conjugado tipo Minnesota con hiperparametros por verosimilitud marginal (V8-F3).

Modelo: Y_t = [Y_{t-1}, ..., Y_{t-p}, 1] B + u_t, u_t ~ N(0, Sigma); B es (k, n), k = n*p + 1 (constante la ultima fila).
Prior: Sigma ~ IW(S0, nu0), vec(B)|Sigma ~ N(vec(B0), Sigma x Omega0), con
  S0 = diag(psi), nu0 = n + 2, B0 = delta en el primer retardo propio,
  Var prior del coef. del retardo l de la variable j en la ecuacion i = Sigma_ii * lam^2 / (l^alfa * psi_j)   (alfa = 2)
  (psi_i = varianza residual de un AR(p) univariante; GLP 2015 usan una pre-muestra).
Dummies opcionales (suma de coeficientes, mu; observacion inicial, theta) se incorporan como observaciones ficticias que
actualizan el prior (sigue siendo normal-Wishart inversa). La densidad marginal p(Y | lam, mu, theta) es analitica:
  p(Y) = pi^(-nT/2) Gamma_n(nu1/2)/Gamma_n(nu0/2) |S0|^(nu0/2) |S1|^(-nu1/2) (|Om1|/|Om0|)^(n/2).
Referencia (NO VERIFICADA: sin acceso a Crossref en esta sesion): Giannone, Lenza y Primiceri (2015, REStat); Banbura, Giannone y Reichlin (2010);
Kadiyala y Karlsson (1997).
Convencion de IRF: arrays (..., h, variable, shock). Todo lo aleatorio recibe un Generator explicito (SEED = 20261010 por defecto).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import multigammaln

SEED = 20261010
VAR_CONST = 1e6


def retardos(Y, p, const=True):
    """Devuelve (yy, X): yy = Y[p:], X = [Y_{t-1},...,Y_{t-p}, 1]."""
    Y = np.asarray(Y, float)
    T = Y.shape[0]
    X = np.hstack([Y[p - l - 1:T - l - 1] for l in range(p)])
    if const:
        X = np.hstack([X, np.ones((T - p, 1))])
    return Y[p:], X


def _psi_ar(Y, p):
    """Varianza residual de un AR(p) univariante con constante, por variable."""
    n = Y.shape[1]
    out = np.empty(n)
    for i in range(n):
        y, X = retardos(Y[:, [i]], p)
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        out[i] = float(np.sum(e ** 2)) / (len(y) - X.shape[1])
    return out


def prior_minnesota(n, p, lam, psi, delta=1.0, alfa=2.0, const=True, nu0=None):
    """Prior normal-Wishart inversa (B0, Om0inv, S0, nu0). Om0inv es la matriz de precision (diagonal)."""
    k = n * p + int(const)
    delta = np.broadcast_to(np.asarray(delta, float), (n,))
    B0 = np.zeros((k, n))
    B0[:n, :n] = np.diag(delta)
    om = np.empty(k)
    for l in range(1, p + 1):
        om[(l - 1) * n:l * n] = lam ** 2 / (l ** alfa * psi)
    if const:
        om[-1] = VAR_CONST
    return dict(B0=B0, Oinv=np.diag(1.0 / om), S0=np.diag(psi), nu0=(n + 2.0) if nu0 is None else nu0)


def _actualizar(pr, Y, X):
    """Actualiza un prior NIW con datos (Y, X). Devuelve el nuevo NIW (B, Oinv, S, nu, Om)."""
    Oinv1 = pr["Oinv"] + X.T @ X
    Om1 = np.linalg.inv(Oinv1)
    Om1 = (Om1 + Om1.T) / 2
    B1 = Om1 @ (pr["Oinv"] @ pr["B0"] + X.T @ Y)
    S1 = pr["S0"] + Y.T @ Y + pr["B0"].T @ pr["Oinv"] @ pr["B0"] - B1.T @ Oinv1 @ B1
    S1 = (S1 + S1.T) / 2
    return dict(B0=B1, Oinv=Oinv1, S0=S1, nu0=pr["nu0"] + Y.shape[0], Om=Om1)


def dummies(Y, p, mu=None, theta=None, delta=1.0, const=True):
    """Observaciones ficticias de suma de coeficientes (mu) y observacion inicial (theta). Devuelve (Yd, Xd) o None."""
    n = Y.shape[1]
    y0 = Y[:p].mean(0) * np.broadcast_to(np.asarray(delta, float), (n,))
    Ys, Xs = [], []
    if mu is not None:
        Ys.append(np.diag(y0) / mu)
        Xs.append(np.hstack([np.tile(np.diag(y0), (1, p)) / mu] + ([np.zeros((n, 1))] if const else [])))
    if theta is not None:
        Ys.append((y0 / theta)[None, :])
        Xs.append(np.hstack([np.tile(y0, p)[None, :] / theta] + ([np.array([[1.0 / theta]])] if const else [])))
    if not Ys:
        return None
    return np.vstack(Ys), np.vstack(Xs)


def _prior_completo(Y, p, lam, mu, theta, delta, alfa, const, psi):
    n = Y.shape[1]
    pr = prior_minnesota(n, p, lam, psi, delta, alfa, const)
    d = dummies(Y, p, mu, theta, delta, const)
    if d is not None:
        pr = _actualizar(pr, *d)
    return pr


def logml_prior(pr, yy, X):
    """Log densidad marginal de yy dado X y un prior NIW (B0, Oinv, S0, nu0)."""
    T, n = yy.shape
    post = _actualizar(pr, yy, X)
    ld = lambda M: np.linalg.slogdet(M)[1]
    return (-0.5 * n * T * np.log(np.pi) + multigammaln(post["nu0"] / 2, n) - multigammaln(pr["nu0"] / 2, n)
            + 0.5 * pr["nu0"] * ld(pr["S0"]) - 0.5 * post["nu0"] * ld(post["S0"])
            + 0.5 * n * (-ld(post["Oinv"]) + ld(pr["Oinv"])))


def logml(Y, p, lam, mu=None, theta=None, delta=1.0, alfa=2.0, const=True, psi=None):
    """Log verosimilitud marginal p(Y_{p+1:T} | Y_{1:p}, lam, mu, theta)."""
    Y = np.asarray(Y, float)
    psi = _psi_ar(Y, p) if psi is None else psi
    yy, X = retardos(Y, p, const)
    pr = _prior_completo(Y, p, lam, mu, theta, delta, alfa, const, psi)
    return logml_prior(pr, yy, X)


def estimar(Y, p, lam=None, mu=None, theta=None, soc=False, io=False, delta=1.0, alfa=2.0, const=True,
            lam_lim=(0.005, 20.0), psi=None):
    """Estima el BVAR. Si lam es None se elige maximizando logml (GLP): rejilla en log(lam) + refinado acotado; si soc/io
    son True, mu y theta tambien se maximizan (Nelder-Mead sobre sus logaritmos) partiendo de 1.0 (o del valor dado).
    Devuelve dict con la posterior NIW: B (media), Om, S, nu, hiperparametros y logml."""
    Y = np.asarray(Y, float)
    n = Y.shape[1]
    psi = _psi_ar(Y, p) if psi is None else np.asarray(psi, float)
    yy, X = retardos(Y, p, const)
    mu = (1.0 if mu is None else mu) if soc else None
    theta = (1.0 if theta is None else theta) if io else None
    opt = {}

    def f_lam(ll, m, th):
        return -logml(Y, p, np.exp(ll), m, th, delta, alfa, const, psi)

    if lam is None:
        lo, hi = np.log(lam_lim[0]), np.log(lam_lim[1])
        grid = np.linspace(lo, hi, 25)
        vals = [f_lam(g, mu, theta) for g in grid]
        i = int(np.argmin(vals))
        r = minimize_scalar(lambda x: f_lam(x, mu, theta), bounds=(grid[max(i - 1, 0)], grid[min(i + 1, 24)]), method="bounded",
                            options=dict(xatol=1e-4))
        lam = float(np.exp(r.x))
        if soc or io:
            def f_all(v):
                ll = np.clip(v[0], lo, hi)
                m = np.exp(np.clip(v[1], -6, 6)) if soc else None
                th = np.exp(np.clip(v[-1], -6, 6)) if io else None
                return f_lam(ll, m, th)
            x0 = [np.log(lam)] + ([np.log(mu)] if soc else []) + ([np.log(theta)] if io else [])
            r2 = minimize(f_all, x0, method="Nelder-Mead", options=dict(xatol=1e-3, fatol=1e-4, maxiter=400))
            lam = float(np.exp(np.clip(r2.x[0], lo, hi)))
            if soc:
                mu = float(np.exp(np.clip(r2.x[1], -6, 6)))
            if io:
                theta = float(np.exp(np.clip(r2.x[-1], -6, 6)))
        opt["optimizado"] = True
    pr = _prior_completo(Y, p, lam, mu, theta, delta, alfa, const, psi)
    post = _actualizar(pr, yy, X)
    res = dict(B=post["B0"], Om=post["Om"], S=post["S0"], nu=post["nu0"], lam=lam, mu=mu, theta=theta, p=p, n=n, const=const,
               psi=psi, logml=logml_prior(pr, yy, X), T=yy.shape[0], Y=Y, **opt)
    res["resid"] = yy - X @ post["B0"]
    return res


# ---------------------------------------------------------------- posterior
def muestrear(post, ndraw, rng=None):
    """Muestrea (B, Sigma) de la posterior NIW. B: (D, k, n); Sigma: (D, n, n)."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    n, k = post["n"], post["B"].shape[0]
    nu = post["nu"]
    Sinv_chol = np.linalg.cholesky(np.linalg.inv(post["S"]))
    Lo = np.linalg.cholesky(post["Om"])
    # Wishart por Bartlett: W = L A A' L', Sigma = W^-1
    A = np.zeros((ndraw, n, n))
    for i in range(n):
        A[:, i, i] = np.sqrt(rng.chisquare(nu - i, size=ndraw))
    il = np.tril_indices(n, -1)
    A[:, il[0], il[1]] = rng.standard_normal((ndraw, len(il[0])))
    LA = Sinv_chol[None] @ A
    W = LA @ LA.transpose(0, 2, 1)
    Sig = np.linalg.inv(W)
    Sig = (Sig + Sig.transpose(0, 2, 1)) / 2
    Ls = np.linalg.cholesky(Sig)
    Z = rng.standard_normal((ndraw, k, n))
    B = post["B"][None] + Lo[None] @ Z @ Ls.transpose(0, 2, 1)
    return B, Sig


def coef_matrices(B, n, p):
    """A_l (D, p, n, n) con A_l[i, j] = efecto de y_j(t-l) sobre y_i(t), y constante (D, n)."""
    B = np.asarray(B)
    A = np.stack([B[:, l * n:(l + 1) * n, :].transpose(0, 2, 1) for l in range(p)], axis=1)
    return A, B[:, n * p, :] if B.shape[1] > n * p else np.zeros((B.shape[0], n))


def ma_coefs(B, n, p, H):
    """Coeficientes MA (D, H+1, n, n): Phi_0 = I, Phi_h = sum_l A_l Phi_{h-l}."""
    B = np.asarray(B)
    if B.ndim == 2:
        B = B[None]
    A, _ = coef_matrices(B, n, p)
    D = B.shape[0]
    Phi = np.zeros((D, H + 1, n, n))
    Phi[:, 0] = np.eye(n)
    for h in range(1, H + 1):
        for l in range(1, min(h, p) + 1):
            Phi[:, h] += A[:, l - 1] @ Phi[:, h - l]
    return Phi


def irf_cholesky(B, Sigma, n, p, H):
    """IRF ortogonalizadas (Cholesky inferior, orden de las columnas de Y). (D, H+1, variable, shock)."""
    Phi = ma_coefs(B, n, p, H)
    P = np.linalg.cholesky(Sigma if Sigma.ndim == 3 else Sigma[None])
    return Phi @ P[:, None]


def cuantiles(x, qs, axis=0, pesos=None):
    """Cuantiles (ponderados si pesos) a lo largo de axis. Devuelve array con eje nuevo al principio (len(qs), ...)."""
    x = np.asarray(x)
    if pesos is None:
        return np.quantile(x, qs, axis=axis)
    x = np.moveaxis(x, axis, 0)
    o = np.argsort(x, axis=0)
    xs = np.take_along_axis(x, o, 0)
    w = np.asarray(pesos, float)[o]
    cw = (np.cumsum(w, axis=0) - 0.5 * w) / w.sum(0, keepdims=True)
    out = np.empty((len(qs),) + x.shape[1:])
    flat_c = cw.reshape(cw.shape[0], -1)
    flat_x = xs.reshape(xs.shape[0], -1)
    for c in range(flat_x.shape[1]):
        out.reshape(len(qs), -1)[:, c] = np.interp(qs, flat_c[:, c], flat_x[:, c])
    return out


def bandas(x, axis=0, pesos=None):
    """Mediana y bandas creibles 68 % y 90 %: dict(med, lo68, hi68, lo90, hi90)."""
    q = cuantiles(x, [0.05, 0.16, 0.5, 0.84, 0.95], axis, pesos)
    return dict(lo90=q[0], lo68=q[1], med=q[2], hi68=q[3], hi90=q[4])


def irf(post, H=20, ndraw=500, rng=None, solo_estables=False):
    """IRF Cholesky con bandas desde la posterior. Devuelve (draws, bandas)."""
    B, Sig = muestrear(post, ndraw, rng)
    if solo_estables:
        ok = np.array([_estable(b, post["n"], post["p"]) for b in B])
        B, Sig = B[ok], Sig[ok]
    I = irf_cholesky(B, Sig, post["n"], post["p"], H)
    return I, bandas(I)


def _estable(B, n, p):
    top = np.hstack([B[l * n:(l + 1) * n, :].T for l in range(p)])
    comp = np.vstack([top, np.hstack([np.eye(n * (p - 1)), np.zeros((n * (p - 1), n))])]) if p > 1 else top
    return np.max(np.abs(np.linalg.eigvals(comp))) < 1


def prediccion(post, h=8, ndraw=500, rng=None, Y=None):
    """Densidad predictiva (D, h, n): incertidumbre de parametros e innovaciones, condicionada a las ultimas p observaciones."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    n, p = post["n"], post["p"]
    Y = post["Y"] if Y is None else np.asarray(Y, float)
    B, Sig = muestrear(post, ndraw, rng)
    L = np.linalg.cholesky(Sig)
    hist = np.repeat(Y[-p:][None], ndraw, axis=0)  # (D, p, n), orden cronologico
    out = np.empty((ndraw, h, n))
    for s in range(h):
        x = np.concatenate([hist[:, -1 - l, :] for l in range(p)] + ([np.ones((ndraw, 1))] if post["const"] else []), axis=1)
        mean = np.einsum("dk,dkn->dn", x, B)
        y = mean + np.einsum("dij,dj->di", L, rng.standard_normal((ndraw, n)))
        out[:, s] = y
        hist = np.concatenate([hist[:, 1:], y[:, None]], axis=1)
    return out
