"""Regimenes y rupturas: Markov switching con contraste del numero de regimenes por bootstrap parametrico de la LR,
modelo de umbral de Hansen (1996/2000) y Bai-Perron con sup-F cuyos valores criticos se obtienen por bootstrap
(corrigen la busqueda de fechas).

Limites declarados: (i) la LR de Markov switching no tiene distribucion chi2 (parametros no identificados bajo la nula):
por eso el p-valor es bootstrap parametrico, que es una aproximacion (no exacta) y es costoso; (ii) el bootstrap `wild`
de umbral/BP es de regresores fijos con residuos reescalados por N(0,1) (valido con heterocedasticidad, NO con
autocorrelacion de los errores); para errores autocorrelacionados hay dos alternativas, `boot="bloque"` (bloques
circulares con longitud dependiente de los datos, Politis-White/Patton-Politis-White) y `boot="sieve"` (AR(p) de los
residuos con p por BIC e innovaciones remuestreadas). Ambas son aproximaciones: con persistencia muy alta (AR 0,85-0,9)
y n ~ 100 conservan un sesgo de tamano que se mide en output/v8/F3/otros/validacion.md (H5, H6 de la revision F3).
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261010


# =========================================================================== Markov switching
def ms_fit(y, k=2, exog=None, ar=0, switching_variance=True, search_reps=5, seed=SEED):
    """Ajusta MarkovRegression (ar=0) o MarkovAutoregression (ar>0) con k regimenes; varios arranques aleatorios.

    Devuelve dict con loglik, aic, bic, parametros por regimen, matriz de transicion P[i,j]=P(S_t=i|S_{t-1}=j), duraciones
    esperadas y probabilidades suavizadas, mas el objeto `res`.
    """
    from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression
    from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    import statsmodels.tsa.regime_switching.markov_switching as _mss
    y = np.asarray(y, float)
    np.random.seed(seed)
    # statsmodels >= 0.15 busca arranques con check_random_state(None) (generador sin semilla): se fija la semilla
    # durante el ajuste y se restaura despues, para que el resultado sea determinista.
    _chk = _mss.check_random_state
    _mss.check_random_state = lambda rng=None: _chk(seed if rng is None else rng)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if ar > 0:
                mod = MarkovAutoregression(y, k_regimes=k, order=ar, trend="c", switching_variance=switching_variance)
            else:
                mod = MarkovRegression(y, k_regimes=k, trend="c", exog=exog, switching_variance=switching_variance)
            res = mod.fit(search_reps=search_reps, disp=False)
    finally:
        _mss.check_random_state = _chk
    P = np.asarray(res.regime_transition)[:, :, 0] if np.asarray(res.regime_transition).ndim == 3 else np.asarray(res.regime_transition)
    par = dict(zip(mod.param_names, np.asarray(res.params)))
    return {"k": k, "loglik": float(res.llf), "aic": float(res.aic), "bic": float(res.bic), "params": par, "P": P,
            "duraciones": 1.0 / (1.0 - np.diag(P)), "prob_suavizada": np.asarray(res.smoothed_marginal_probabilities),
            "res": res, "n": len(y)}


def _simular_ms(fit, n, rng):
    """Simula una serie del MS ajustado (solo media y varianza conmutantes, sin AR/exog)."""
    k = fit["k"]
    P = fit["P"]
    par = fit["params"]
    mu = np.array([par[f"const[{i}]"] for i in range(k)])
    s2 = np.array([par.get(f"sigma2[{i}]", par.get("sigma2")) for i in range(k)])
    w, v = np.linalg.eig(P)
    pi = np.real(v[:, np.argmin(abs(w - 1))])
    pi = np.abs(pi) / np.abs(pi).sum()
    s = np.empty(n, int)
    s[0] = rng.choice(k, p=pi)
    u = rng.random(n)
    for t in range(1, n):
        s[t] = np.searchsorted(np.cumsum(P[:, s[t - 1]]), u[t])
    s = np.minimum(s, k - 1)
    return mu[s] + np.sqrt(s2[s]) * rng.standard_normal(n)


def ms_contraste_regimenes(y, k0=1, k1=2, B=99, switching_variance=True, search_reps=3, seed=SEED, fit0=None):
    """Contraste H0: k0 regimenes vs H1: k1 por bootstrap parametrico de LR = 2(llf1 - llf0).

    k0=1: la nula es N(mu, s2) (iid). k0>=2: la nula es el MS-k0 ajustado. p = (1+#{LR*>=LR})/(1+B). Cada replica reajusta
    ambos modelos (costoso, sobre todo k1=3).
    """
    y = np.asarray(y, float)
    n = len(y)
    rng = np.random.default_rng(seed)
    f1 = ms_fit(y, k1, switching_variance=switching_variance, search_reps=search_reps, seed=seed)
    if k0 == 1:
        ll0 = float(np.sum(stats.norm.logpdf(y, y.mean(), y.std())))
        fit0 = {"k": 1, "params": {"const[0]": y.mean(), "sigma2": y.var()}, "P": np.ones((1, 1)), "loglik": ll0}
    else:
        fit0 = fit0 or ms_fit(y, k0, switching_variance=switching_variance, search_reps=search_reps, seed=seed)
        ll0 = fit0["loglik"]
    lr = max(2 * (f1["loglik"] - ll0), 0.0)
    cnt = 0
    nok = 0
    for b in range(B):
        if k0 == 1:
            yb = rng.normal(fit0["params"]["const[0]"], np.sqrt(fit0["params"]["sigma2"]), n)
            l0b = float(np.sum(stats.norm.logpdf(yb, yb.mean(), yb.std())))
        else:
            yb = _simular_ms(fit0, n, rng)
            try:
                l0b = ms_fit(yb, k0, switching_variance=switching_variance, search_reps=search_reps, seed=seed + b + 1)["loglik"]
            except Exception:
                continue
        try:
            l1b = ms_fit(yb, k1, switching_variance=switching_variance, search_reps=search_reps, seed=seed + b + 1)["loglik"]
        except Exception:
            continue
        nok += 1
        cnt += max(2 * (l1b - l0b), 0.0) >= lr
    return {"k0": k0, "k1": k1, "LR": lr, "p": (1 + cnt) / (1 + nok), "B_ok": nok, "fit1": f1}


def ms_seleccionar_k(y, kmax=3, B=49, alpha=0.05, search_reps=3, seed=SEED):
    """Secuencia de contrastes bootstrap k vs k+1; devuelve k elegido (primer no rechazo) y la tabla; incluye el k por BIC."""
    filas = []
    k = 1
    elegido = None
    fits = {}
    while k < kmax:
        t = ms_contraste_regimenes(y, k, k + 1, B=B, search_reps=search_reps, seed=seed)
        filas.append({"H0": k, "H1": k + 1, "LR": t["LR"], "p": t["p"]})
        if elegido is None and t["p"] >= alpha:
            elegido = k
            break
        k += 1
    if elegido is None:
        elegido = kmax
    bic = {kk: ms_fit(y, kk, search_reps=search_reps, seed=seed)["bic"] for kk in range(2, kmax + 1)}
    bic[1] = float(-2 * np.sum(stats.norm.logpdf(y, np.mean(y), np.std(y))) + 2 * np.log(len(y)))
    return {"k_secuencial": elegido, "k_bic": min(bic, key=bic.get), "tabla": pd.DataFrame(filas), "bic": bic}


# =========================================================================== remuestreo para errores dependientes
def longitud_bloque_pw(e, max_b=None):
    """Longitud optima de bloque para el bootstrap de bloques circulares (Politis-White 2004 con la correccion de
    Patton-Politis-White 2009): b = (2 G^2 / D_CB)^(1/3) n^(1/3), con D_CB = (4/3) g(0)^2, G = 2 sum lambda(k/M) k R(k),
    g(0) = R(0) + 2 sum lambda(k/M) R(k), lambda = ventana plana (flat-top) y M = 2 m con m = primer retardo tal que las
    kn autocorrelaciones siguientes son todas no significativas (|rho| < 2 sqrt(log10 n / n)). Devuelve entero en [2, max_b]
    (max_b = n//4 por defecto)."""
    e = np.asarray(e, float).ravel()
    n = len(e)
    e = e - e.mean()
    kn = max(5, int(np.ceil(np.sqrt(np.log10(n)))))
    mmax = int(np.ceil(np.sqrt(n))) + kn
    mmax = min(mmax, n - 2)
    R = np.array([e[: n - k] @ e[k:] / n for k in range(mmax + 1)])
    rho = R / R[0]
    thr = 2.0 * np.sqrt(np.log10(n) / n)
    m = max(mmax - kn, 1)
    for mm in range(0, mmax - kn + 1):
        if np.all(np.abs(rho[mm + 1: mm + kn + 1]) < thr):
            m = max(mm, 1)
            break
    M = min(2 * m, mmax)
    k = np.arange(1, M + 1)
    lam = np.where(k / M <= 0.5, 1.0, 2.0 * (1.0 - k / M))
    g0 = R[0] + 2.0 * np.sum(lam * R[1: M + 1])
    G = 2.0 * np.sum(lam * k * R[1: M + 1])
    D = 4.0 / 3.0 * g0 ** 2
    b = (2.0 * G ** 2 / D) ** (1.0 / 3.0) * n ** (1.0 / 3.0) if D > 0 else 2.0
    return int(np.clip(round(b), 2, max_b or max(n // 4, 2)))


def _remuestra_circular(e, b, rng):
    """Bootstrap de bloques moviles CIRCULARES de longitud b (todas las posiciones de inicio, con envolvente)."""
    n = len(e)
    nb = int(np.ceil(n / b))
    st = rng.integers(0, n, nb)
    return e[((st[:, None] + np.arange(b)[None, :]) % n).ravel()[:n]]


def ar_sieve(e, pmax=None):
    """AR(p) de e (centrado) con p elegido por BIC en 0..pmax (pmax = min(8, n//10)). Devuelve (phi, innovaciones centradas)."""
    e = np.asarray(e, float).ravel()
    e = e - e.mean()
    n = len(e)
    pmax = min(8, max(n // 10, 1)) if pmax is None else pmax
    best = (np.inf, np.zeros(0), e.copy())
    for p in range(0, pmax + 1):
        if p == 0:
            phi, u = np.zeros(0), e
        else:
            Z = np.column_stack([e[p - j - 1: n - j - 1] for j in range(p)])
            phi = np.linalg.lstsq(Z, e[p:], rcond=None)[0]
            u = e[p:] - Z @ phi
        bic = len(u) * np.log(u @ u / len(u)) + p * np.log(len(u))
        if bic < best[0]:
            best = (bic, phi, u)
    phi, u = best[1], best[2]
    return phi, u - u.mean()


def simula_sieve(phi, innov, n, rng, quemado=100):
    """Serie AR(phi) de longitud n con innovaciones remuestreadas con reemplazo de `innov`."""
    p = len(phi)
    u = innov[rng.integers(0, len(innov), n + quemado)]
    x = np.zeros(n + quemado)
    for t in range(n + quemado):
        x[t] = u[t] + (sum(phi[j] * x[t - j - 1] for j in range(p) if t - j - 1 >= 0) if p else 0.0)
    return x[quemado:]


def _boot_errores(e, boot, rng, bloque):
    """Un remuestreo de la serie de residuos e (orden temporal) segun `boot`: wild | bloque | sieve."""
    n = len(e)
    if boot == "wild":
        return e * rng.standard_normal(n)
    if boot == "bloque":
        return _remuestra_circular(e, bloque, rng)
    if boot == "sieve":
        phi, u = bloque  # (phi, innovaciones) precalculados
        return simula_sieve(phi, u, n, rng)
    raise ValueError(f"boot desconocido: {boot}")


def _prepara_boot(e_tiempo, boot, bloque):
    """Parametros fijos del remuestreo: longitud de bloque (PW si 'auto'/None) o (phi, innovaciones) del sieve."""
    if boot == "bloque":
        return longitud_bloque_pw(e_tiempo) if bloque in (None, "auto") else int(bloque)
    if boot == "sieve":
        return ar_sieve(e_tiempo)
    return None


# =========================================================================== umbral de Hansen
def _acum(Xs, ys):
    xx = np.einsum("ti,tj->tij", Xs, Xs).cumsum(0)
    xy = (Xs * ys[:, None]).cumsum(0)
    return xx, xy, float(ys @ ys)


def umbral_hansen(y, X, q, trim=0.15, B=499, seed=SEED, nivel=0.95, min_obs=None, boot="wild", bloque="auto"):
    """Modelo de umbral con variable umbral observable `q` y TODOS los coeficientes conmutantes:
    y = X b1 1(q<=g) + X b2 1(q>g) + e. g por minimos cuadrados (rejilla = valores observados dentro del recorte).

    - Contraste de linealidad sup-LR (equivalente al sup-F/sup-Wald homocedastico): bootstrap de regresores fijos de
      Hansen (1996). boot='wild' (por defecto): residuos x N(0,1), robusto a heterocedasticidad pero NO a autocorrelacion.
      boot='bloque': residuos de la nula remuestreados en bloques circulares EN ORDEN TEMPORAL (longitud `bloque`, o
      Politis-White si 'auto'); boot='sieve': AR(p) de los residuos temporales (p por BIC) con innovaciones remuestreadas.
      'bloque' y 'sieve' son para errores autocorrelacionados (p. ej. crecimientos interanuales, MA(3) por construccion) y
      variable umbral persistente: ver la validacion Monte Carlo para su tamano real.
    - IC de g por inversion de LR (Hansen 2000): {g: LR(g) <= c}, c = -2 ln(1 - sqrt(nivel)) (95%: 7,35); asume
      homocedasticidad (con heterocedasticidad es conservador/optimista segun el caso: reservas).
    """
    y = np.asarray(y, float).ravel()
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    q = np.asarray(q, float).ravel()
    n, k = X.shape
    o = np.argsort(q, kind="stable")
    Xs, ys, qs = X[o], y[o], q[o]
    mlo = max(int(np.ceil(trim * n)), (min_obs or k + 1))
    ms = np.arange(mlo, n - mlo + 1)  # m = obs en regimen bajo
    ms = ms[qs[ms - 1] < qs[np.minimum(ms, n - 1)]]  # puntos de corte distintos
    xx, xy, yy = _acum(Xs, ys)
    xx_t, xy_t = xx[-1], xy[-1]
    A1 = xx[ms - 1]
    A2 = xx_t[None] - A1
    I1, I2 = np.linalg.inv(A1), np.linalg.inv(A2)
    # SSR lineal
    b0 = np.linalg.solve(xx_t, xy_t)
    ssr0 = yy - b0 @ xy_t

    def ssr_path(xyc, yyv):
        c1 = xyc[ms - 1]
        c2 = xyc[-1][None] - c1
        b1 = np.einsum("mij,mj->mi", I1, c1)
        b2 = np.einsum("mij,mj->mi", I2, c2)
        return yyv - np.einsum("mi,mi->m", b1, c1) - np.einsum("mi,mi->m", b2, c2)

    ssr = ssr_path(xy, yy)
    j = int(np.argmin(ssr))
    ssr1 = float(ssr[j])
    lr_sup = n * (ssr0 - ssr1) / ssr1
    gamma = float(qs[ms[j] - 1])
    # bootstrap (Hansen 1996): y* = e_hat * N(0,1) con e_hat residuo del modelo LINEAL (nula)
    e0 = ys - Xs @ b0
    rng = np.random.default_rng(seed)
    sup_b = np.empty(B)
    e_t = np.empty(n)
    e_t[o] = e0  # residuos en orden temporal (para bloque/sieve)
    par = _prepara_boot(e_t, boot, bloque)
    for b in range(B):
        yb = e0 * rng.standard_normal(n) if boot == "wild" else _boot_errores(e_t, boot, rng, par)[o]
        xyb = (Xs * yb[:, None]).cumsum(0)
        yyb = float(yb @ yb)
        b0b = np.linalg.solve(xx_t, xyb[-1])
        s0b = yyb - b0b @ xyb[-1]
        s1b = ssr_path(xyb, yyb).min()
        sup_b[b] = n * (s0b - s1b) / s1b
    p = float((1 + np.sum(sup_b >= lr_sup)) / (1 + B))
    lr_path = n * (ssr - ssr1) / ssr1
    c = -2 * np.log(1 - np.sqrt(nivel))
    ok = lr_path <= c
    gam_grid = qs[ms - 1]
    ic = (float(gam_grid[ok].min()), float(gam_grid[ok].max()))
    m_star = ms[j]
    bl = np.linalg.solve(xx[m_star - 1], xy[m_star - 1])
    bh = np.linalg.solve(xx_t - xx[m_star - 1], xy_t - xy[m_star - 1])
    return {"gamma": gamma, "ic_gamma": ic, "c_LR": float(c), "sup_LR": float(lr_sup), "p_linealidad": p,
            "cv95_boot": float(np.quantile(sup_b, 0.95)), "coef_bajo": bl, "coef_alto": bh, "n_bajo": int(m_star),
            "n_alto": int(n - m_star), "n": n, "grid": gam_grid, "lr_path": lr_path, "boot": boot,
            "bloque_usado": par if boot == "bloque" else None}


# =========================================================================== Bai-Perron con sup-F bootstrap
class _BP:
    """Precalcula inversas de X'X por segmento (X fijo) para reutilizar en el bootstrap."""

    def __init__(self, X, h):
        n, k = X.shape
        self.n, self.k, self.h = n, k, h
        c = np.vstack([np.zeros((1, k, k)), np.einsum("ti,tj->tij", X, X).cumsum(0)])
        self.cxx = c
        ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        self.valid = (jj - ii + 1) >= h
        S = c[jj + 1] - c[ii]
        S = np.where(self.valid[:, :, None, None], S, np.eye(k))
        self.inv = np.linalg.inv(S)
        self.ii, self.jj = ii, jj

    def segmentos(self, X, y):
        cxy = np.vstack([np.zeros((1, self.k)), (X * y[:, None]).cumsum(0)])
        cyy = np.r_[0.0, (y * y).cumsum()]
        ii, jj = self.ii, self.jj
        sxy = cxy[jj + 1] - cxy[ii]
        syy = cyy[jj + 1] - cyy[ii]
        ssr = syy - np.einsum("ijk,ijkl,ijl->ij", sxy, self.inv, sxy)
        return np.where(self.valid, ssr, np.inf)

    def dp(self, ssr, M):
        """SSR minimo con m=0..M cortes y fechas. Devuelve (ssr_m[0..M], cortes[m])."""
        n, h = self.n, self.h
        V = [ssr[0, :].copy()]
        arg = [None]
        for s in range(1, M + 1):
            prev = V[-1]
            cost = np.full((n, n), np.inf)
            cost[1:, :] = prev[:-1, None] + ssr[1:, :]
            a = np.argmin(cost, axis=0)
            V.append(cost[a, np.arange(n)])
            arg.append(a)
        res = [float(V[s][n - 1]) for s in range(M + 1)]
        cortes = [()]
        for s in range(1, M + 1):
            j = n - 1
            cs = []
            for t in range(s, 0, -1):
                i = int(arg[t][j])
                cs.append(i)
                j = i - 1
            cortes.append(tuple(sorted(cs)))
        return res, cortes


def bai_perron(y, X=None, max_cortes=3, trim=0.15, B=199, seed=SEED, boot="wild", bloque="auto", ic_k=None):
    """Bai-Perron (cambio estructural puro: todos los coeficientes cambian), minimos cuadrados globales por
    programacion dinamica. sup-F(m) de 0 vs m cortes y UDmax = max_m sup-F(m); p-valores y valores criticos por
    bootstrap de la nula SIN rupturas (corrigen la busqueda de fechas). Seleccion de m por BIC y por UDmax+secuencia.

    boot='wild' (heterocedasticidad, NO autocorrelacion), 'bloque' (bloques circulares de residuos; longitud `bloque` o
    Politis-White si 'auto') o 'sieve' (AR(p) por BIC con innovaciones remuestreadas), ambos para autocorrelacion. 'block'
    se admite como alias de 'bloque'. Con persistencia alta y n ~ 100 el tamano sigue inflado: ver validacion Monte Carlo.
    """
    y = np.asarray(y, float).ravel()
    n = len(y)
    X = np.ones((n, 1)) if X is None else np.asarray(X, float).reshape(n, -1)
    k = X.shape[1]
    h = max(int(np.floor(trim * n)), k + 1)
    bp = _BP(X, h)
    M = int(min(max_cortes, n // h - 1))

    def estad(yv):
        ssr = bp.segmentos(X, yv)
        res, cortes = bp.dp(ssr, M)
        b0 = np.linalg.lstsq(X, yv, rcond=None)[0]
        s0 = float(np.sum((yv - X @ b0) ** 2))
        res[0] = s0
        supf = np.array([((s0 - res[m]) / (m * k)) / (res[m] / (n - (m + 1) * k)) for m in range(1, M + 1)])
        return supf, res, cortes, b0

    supf, res, cortes, b0 = estad(y)
    ud = float(supf.max())
    e0 = y - X @ b0
    rng = np.random.default_rng(seed)
    sb = np.empty((B, M))
    boot = "bloque" if boot == "block" else boot
    par = _prepara_boot(e0, boot, bloque)
    for b in range(B):
        sb[b] = estad(_boot_errores(e0, boot, rng, par))[0]
    p_m = (1 + (sb >= supf[None]).sum(0)) / (1 + B)
    ud_b = sb.max(1)
    p_ud = float((1 + np.sum(ud_b >= ud)) / (1 + B))
    bic = [n * np.log(res[m] / n) + np.log(n) * (m + 1) * k + np.log(n) * m for m in range(M + 1)]
    m_bic = int(np.argmin(bic))
    # numero por UDmax: si rechaza, el m con menor BIC entre >=1; si no, 0
    m_ud = 0 if p_ud >= 0.05 else int(1 + np.argmin(bic[1:]))
    return {"n": n, "k": k, "h": h, "supF": supf, "p_supF": p_m, "UDmax": ud, "p_UDmax": p_ud,
            "cv95_UDmax_boot": float(np.quantile(ud_b, 0.95)), "cv95_supF_boot": np.quantile(sb, 0.95, axis=0),
            "ssr": res, "cortes": cortes, "bic": bic, "m_bic": m_bic, "m_udmax": m_ud, "M": M, "boot": boot,
            "bloque_usado": par if boot == "bloque" else None}


def bai_perron_ruptures(y, n_bkps, min_size=10):
    """Segmentacion de media por programacion dinamica con `ruptures` (contraste cruzado de las fechas del DP propio)."""
    import ruptures as rpt
    algo = rpt.Dynp(model="l2", min_size=min_size, jump=1).fit(np.asarray(y, float).reshape(-1, 1))
    return tuple(int(b) for b in algo.predict(n_bkps=n_bkps)[:-1])
