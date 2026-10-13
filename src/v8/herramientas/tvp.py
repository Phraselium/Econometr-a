"""TVP-VAR con volatilidad estocastica (Primiceri 2005; orden de bloques corregido segun Del Negro y Primiceri 2015). V8-F3. Capa C4.

y_t = X_t beta_t + A_t^-1 Sigma_t eps_t,  eps_t ~ N(0, I);  beta_t = beta_{t-1} + v_t (Q);  a_t = a_{t-1} + z_t (S, bloques por ecuacion);
log sigma_it = log sigma_i,t-1 + w_it (W diagonal). X_t = I_n x [y_{t-1}', ..., y_{t-p}', 1]; beta ordenado ecuacion por ecuacion.
Gibbs: (1) beta^T (Carter-Kohn), (2) Q, (3) a^T (CK por ecuacion), (4) S, (5) indicadores de mezcla de 7 componentes de Kim-Shephard-Chib
(1998) y DESPUES h^T (CK), (6) W. Orden (5) segun Del Negro-Primiceri (2015): primero los indicadores dados h, luego h dados los indicadores.
Prior: muestra de entrenamiento (primeras tau filas efectivas, no entran en la estimacion): beta0 ~ N(OLS, 4 V), a0 ~ N(a_OLS, 10|a_OLS|),
h0 ~ N(log sigma_OLS, 10); Q ~ IW(kQ^2 tau V, tau), S_i ~ IW(kS^2 (1+i) V_Ai, 1+i), W_i ~ IG(.): kQ=0.01, kS=0.1, kW=0.01 (Primiceri).
No se imponen restricciones de estabilidad a las sendas de beta. Referencias NO VERIFICADAS: Primiceri (2005, REStud); Del Negro y Primiceri (2015, REStud);
Carter y Kohn (1994); Kim, Shephard y Chib (1998). Estado: ver validacion.md.
"""
from __future__ import annotations

import numpy as np
from numba import njit
from scipy.stats import invwishart

from . import bvar

SEED = 20261010
KSC_Q = np.array([0.00730, 0.10556, 0.00002, 0.04395, 0.34001, 0.24566, 0.25750])
KSC_M = np.array([-10.12999, -3.97281, -8.56686, 2.77786, 0.61942, 1.79518, -1.08819]) - 1.2704
KSC_V = np.array([5.79596, 2.61369, 5.17950, 0.16735, 0.64009, 0.34023, 1.26261])


@njit(cache=True)
def _ck(y, Z, R, Qm, b0, P0, eps):
    """Carter-Kohn con observaciones vectoriales de errores independientes (filtrado univariante secuencial).
    y (T,m), Z (T,m,d), R (T,m) varianzas, estado paseo aleatorio con varianza Qm (d,d); estado inicial N(b0,P0) en t=0 (sin Qm).
    eps (T,d) normales estandar. Devuelve la trayectoria muestreada (T,d)."""
    T, m = y.shape
    d = b0.shape[0]
    bf = np.zeros((T, d))
    Pf = np.zeros((T, d, d))
    b = b0.copy()
    P = P0.copy()
    for t in range(T):
        if t > 0:
            P = P + Qm
        for i in range(m):
            z = Z[t, i]
            Pz = P @ z
            f = z @ Pz + R[t, i]
            k = Pz / f
            b = b + k * (y[t, i] - z @ b)
            P = P - np.outer(k, Pz)
            P = (P + P.T) / 2
        bf[t] = b
        Pf[t] = P
    out = np.zeros((T, d))
    L = np.linalg.cholesky(Pf[T - 1] + 1e-12 * np.eye(d))
    out[T - 1] = bf[T - 1] + L @ eps[T - 1]
    for t in range(T - 2, -1, -1):
        Pp = Pf[t] + Qm
        J = Pf[t] @ np.linalg.inv(Pp)
        mu = bf[t] + J @ (out[t + 1] - bf[t])
        V = Pf[t] - J @ Pf[t]
        V = (V + V.T) / 2
        L = np.linalg.cholesky(V + 1e-12 * np.eye(d))
        out[t] = mu + L @ eps[t]
    return out


def _A_from_a(a, n):
    """a (T, n(n-1)/2) -> A_t (T,n,n) triangular inferior con unos en la diagonal."""
    T = a.shape[0]
    A = np.tile(np.eye(n), (T, 1, 1))
    il = np.tril_indices(n, -1)
    A[:, il[0], il[1]] = a
    return A


def _iw(rng, nu, S):
    S = np.atleast_2d(S)
    return np.atleast_2d(invwishart.rvs(df=nu, scale=S, random_state=rng))


def _entrenar(yy, X, tau, n, k):
    y0, X0 = yy[:tau], X[:tau]
    XtXi = np.linalg.inv(X0.T @ X0)
    Bo = XtXi @ X0.T @ y0
    e = y0 - X0 @ Bo
    Sg = e.T @ e / (tau - k)
    beta0 = Bo.T.reshape(-1)  # ecuacion por ecuacion
    Vb = np.kron(Sg, XtXi)
    L = np.linalg.cholesky(Sg)
    Ainv = L / np.diag(L)[None, :]
    Ao = np.linalg.inv(Ainv)
    a0 = Ao[np.tril_indices(n, -1)]
    return beta0, Vb, a0, np.log(np.diag(L)), Sg


def estimar(Y, p=2, tau=30, n_iter=3000, burn=1000, thin=5, rng=None, kQ=0.01, kS=0.1, kW=0.01, verbose=False):
    """Estima el TVP-VAR-SV. Y (T,n). Las primeras tau filas efectivas (tras p retardos) solo entrenan el prior.
    Devuelve dict con beta (D,Te,d), h (D,Te,n) (log sigma), a (D,Te,n(n-1)/2), Q medio, fechas efectivas (indices de Y), etc."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    Y = np.asarray(Y, float)
    n = Y.shape[1]
    yy, X = bvar.retardos(Y, p, True)
    k = n * p + 1
    d = n * k
    na = n * (n - 1) // 2
    beta0, Vb, a0, h0, Sg = _entrenar(yy, X, tau, n, k)
    ye, Xe = yy[tau:], X[tau:]
    T = ye.shape[0]
    # prior
    b_mean, b_var = beta0, 4 * Vb
    a_mean, a_var = a0, np.diag(10 * np.abs(a0) + 1e-3)
    Q0 = kQ ** 2 * tau * Vb
    nuQ = float(tau)
    # bloques de S: ecuacion i (i=1..n-1) tiene i elementos
    blocks = []
    r = 0
    for i in range(1, n):
        blocks.append(np.arange(r, r + i))
        r += i
    S0 = [kS ** 2 * (1 + len(bl)) * np.diag(a_var)[bl] * np.eye(len(bl)) for bl in blocks]
    nuS = [1.0 + len(bl) for bl in blocks]
    nuW, sW = 2.0, kW ** 2 * 2.0
    # inicial
    beta = np.tile(beta0, (T, 1))
    a = np.tile(a0, (T, 1))
    h = np.tile(h0, (T, 1))
    Q = Q0 / nuQ * 1.0 + 0 * Q0
    Q = Q0 / (nuQ - d - 1) if nuQ > d + 1 else Q0 / nuQ
    S = [S0[i] / max(nuS[i] - len(blocks[i]) - 1, 1.0) for i in range(len(blocks))]
    W = np.full(n, sW / (nuW + 1))
    # regresores X_t = I_n x x_t : construir bloque por bloque
    Zb = np.zeros((T, n, d))
    for i in range(n):
        Zb[:, i, i * k:(i + 1) * k] = Xe
    keep = []
    for it in range(n_iter):
        A = _A_from_a(a, n)
        sig = np.exp(h)
        # (1) beta^T: A_t y_t = A_t X_t beta_t + Sigma_t eta
        ys = np.einsum("tij,tj->ti", A, ye)
        Zs = np.einsum("tij,tjk->tik", A, Zb)
        beta = _ck(ys, Zs, sig ** 2, Q, b_mean, b_var, rng.standard_normal((T, d)))
        # (2) Q
        db = np.diff(beta, axis=0)
        Q = _iw(rng, nuQ + T - 1, Q0 + db.T @ db)
        # (3) a^T por ecuacion
        eps_ = ye - np.einsum("tij,tj->ti", Zb, beta)
        for i in range(1, n):
            bl = blocks[i - 1]
            Zi = -eps_[:, :i][:, None, :]  # (T,1,i)
            ai = _ck(eps_[:, i:i + 1], Zi, (sig[:, i] ** 2)[:, None], S[i - 1], a_mean[bl], a_var[np.ix_(bl, bl)], rng.standard_normal((T, i)))
            a[:, bl] = ai
        # (4) S
        for i in range(1, n):
            bl = blocks[i - 1]
            da = np.diff(a[:, bl], axis=0)
            S[i - 1] = _iw(rng, nuS[i - 1] + T - 1, S0[i - 1] + da.T @ da)
        # (5) volatilidades: indicadores de mezcla y luego h (KSC; orden DNP 2015)
        A = _A_from_a(a, n)
        ystar = np.einsum("tij,tj->ti", A, eps_)
        zl = np.log(ystar ** 2 + 1e-3)
        for i in range(n):
            lik = KSC_Q[None, :] * np.exp(-0.5 * (zl[:, i:i + 1] - 2 * h[:, i:i + 1] - KSC_M[None, :]) ** 2 / KSC_V[None, :]) / np.sqrt(KSC_V)[None, :]
            lik = lik + 1e-300
            cum = np.cumsum(lik / lik.sum(1, keepdims=True), axis=1)
            s = (rng.random(T)[:, None] > cum).sum(1).clip(0, 6)
            obs = (zl[:, i] - KSC_M[s])[:, None]
            Zh = np.full((T, 1, 1), 2.0)
            h[:, i] = _ck(obs, Zh, KSC_V[s][:, None], np.array([[W[i]]]), np.array([h0[i]]), np.array([[10.0]]), rng.standard_normal((T, 1)))[:, 0]
        # (6) W
        for i in range(n):
            dh = np.diff(h[:, i])
            W[i] = 1.0 / rng.gamma((nuW + T - 1) / 2, 2.0 / (sW + dh @ dh))
        if it >= burn and (it - burn) % thin == 0:
            keep.append((beta.copy(), h.copy(), a.copy()))
        if verbose and it % 200 == 0:
            print(it, flush=True)
    return dict(beta=np.array([x[0] for x in keep]), h=np.array([x[1] for x in keep]), a=np.array([x[2] for x in keep]),
                n=n, p=p, k=k, d=d, tau=tau, T=T, indice_obs=np.arange(p + tau, p + tau + T), Q=Q, W=W)


def trayectoria(res, ecuacion, variable, retardo=1):
    """Sorteos (D, T) de la senda del coeficiente de y_variable(t-retardo) en la ecuacion dada (variable=n -> constante)."""
    n = res["n"]
    pos = ecuacion * res["k"] + (res["n"] * res["p"] if variable == n else (retardo - 1) * n + variable)
    return res["beta"][:, :, pos]


def volatilidad(res):
    """Sorteos de la desviacion tipica estructural sigma_it (D, T, n)."""
    return np.exp(res["h"])


def irf_en(res, t, H=12):
    """IRF Cholesky (D, H+1, variable, shock) con los parametros del periodo efectivo t (A_t^-1 Sigma_t como matriz de impacto)."""
    n, p, k = res["n"], res["p"], res["k"]
    D = res["beta"].shape[0]
    B = res["beta"][:, t, :].reshape(D, n, k).transpose(0, 2, 1)
    Phi = bvar.ma_coefs(B, n, p, H)
    imp = np.empty((D, n, n))
    for dd in range(D):
        A = _A_from_a(res["a"][dd, t][None], n)[0]
        imp[dd] = np.linalg.inv(A) * np.exp(res["h"][dd, t])[None, :]
    return Phi @ imp[:, None]


# ------------------------------------------------------------ alternativa: VAR por regimenes (prior comun)
def var_regimenes(Y, p, cortes=None, lam=None, delta=0.0, lam_lim=(0.005, 20.0), tramos=None):
    """VAR bayesiano con coeficientes distintos por tramo y PRIOR COMUN (Minnesota con el mismo lambda; psi de la muestra completa).
    Tramos sobre las observaciones efectivas yy = Y[p:] (indices base 0):
      * cortes: indices donde empieza cada nuevo regimen, p. ej. [60] -> dos regimenes contiguos que cubren toda la muestra; o
      * tramos: lista de (ini, fin) SEMIABIERTOS, no necesariamente contiguos: las observaciones fuera de todo tramo (huecos de
        transicion) no entran en la estimacion como variable dependiente (siguen siendo retardos de las observaciones posteriores).
    delta: media a priori del primer retardo propio (escalar o vector; por defecto 0).
    El fechado de las rupturas se SUPONE conocido (no se estima). lambda se elige maximizando la suma de las densidades marginales
    de los tramos (GLP). Devuelve dict con 'regimenes': lista de posteriores NIW compatibles con bvar.muestrear."""
    from scipy.optimize import minimize_scalar
    Y = np.asarray(Y, float)
    n = Y.shape[1]
    yy, X = bvar.retardos(Y, p, True)
    if tramos is None:
        assert cortes is not None, "indicar cortes o tramos"
        lim = [0, *cortes, yy.shape[0]]
        segs = [(lim[i], lim[i + 1]) for i in range(len(lim) - 1)]
    else:
        segs = [(int(a), int(b)) for a, b in tramos]
        assert all(0 <= a < b <= yy.shape[0] for a, b in segs), "tramos fuera de la muestra efectiva"
        assert all(segs[i][1] <= segs[i + 1][0] for i in range(len(segs) - 1)), "tramos solapados o desordenados"
    psi = bvar._psi_ar(Y, p)

    def total(ll):
        pr = bvar.prior_minnesota(n, p, np.exp(ll), psi, delta)
        return sum(bvar.logml_prior(pr, yy[a:b], X[a:b]) for a, b in segs)
    if lam is None:
        grid = np.linspace(np.log(lam_lim[0]), np.log(lam_lim[1]), 25)
        v = [-total(g) for g in grid]
        i = int(np.argmin(v))
        r = minimize_scalar(lambda x: -total(x), bounds=(grid[max(i - 1, 0)], grid[min(i + 1, 24)]), method="bounded")
        lam = float(np.exp(r.x))
    pr = bvar.prior_minnesota(n, p, lam, psi, delta)
    regs = []
    for a, b in segs:
        po = bvar._actualizar(pr, yy[a:b], X[a:b])
        regs.append(dict(B=po["B0"], Om=po["Om"], S=po["S0"], nu=po["nu0"], n=n, p=p, const=True, lam=lam, T=b - a, Y=Y))
    prior = dict(B=pr["B0"], Om=np.linalg.inv(pr["Oinv"]), S=pr["S0"], nu=pr["nu0"], n=n, p=p, const=True)
    return dict(regimenes=regs, lam=lam, segs=segs, n=n, p=p, k=n * p + 1, prior=prior)


def diferencia_regimenes(res, i, j, ecuacion, variable, retardo=1, ndraw=500, rng=None):
    """Sorteos de (coef. regimen j) - (coef. regimen i) del retardo `retardo` de y_variable en la ecuacion dada."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    n = res["n"]
    pos = (retardo - 1) * n + variable
    Bi, _ = bvar.muestrear(res["regimenes"][i], ndraw, rng)
    Bj, _ = bvar.muestrear(res["regimenes"][j], ndraw, rng)
    return Bj[:, pos, ecuacion] - Bi[:, pos, ecuacion]
