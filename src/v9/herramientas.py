"""V9 · herramientas econométricas propias (sin dependencias nuevas), validadas por Monte Carlo en
tests/v9/test_herramientas.py antes de usarse (regla V7).

DiD escalonado (panel equilibrado; Y: matriz unidades × periodos; g: índice de columna del primer periodo tratado,
np.inf si nunca tratada; tratamiento absorbente):
  cs()       Callaway y Sant'Anna (2021) sin covariables: ATT(g,t) con base universal g-1 y controles «nunca» o «aún no»
             tratados; agregados (ATT global ponderado por tamaño de cohorte, estudio de eventos ATT(e)) con funciones
             de influencia por unidad y bootstrap multiplicador de Rademacher a nivel de unidad (= bootstrap salvaje por
             conglomerados de unidad).
  bjs()      imputación de Borusyak, Jaravel y Spiess (2024): efectos fijos de unidad y periodo estimados solo con
             observaciones no tratadas; ATT = media de Y - Ŷ(0) en las tratadas; IC por bootstrap de unidades.
  dcdh()     de Chaisemartin y D'Haultfœuille, DID_l con controles aún no tratados (equivale a CS «aún no tratados» con
             base g-1 para tratamientos absorbentes); se expone por separado para la tabla.
  honest_rm() Rambachan y Roth (2023), magnitudes relativas, versión simplificada: sesgo posterior acotado por
             M̄ × máx |Δ| entre coeficientes previos consecutivos; IC = [θ̂ - cota - z·se, θ̂ + cota + z·se].
Regresión con dosis continua (D2): twfe_cluster() con efectos fijos bidireccionales (panel equilibrado), errores por
conglomerados y p de bootstrap salvaje (Rademacher, no restringido, bootstrap-t).
IV y shift-share (D4): iv_just() 2SLS con un instrumento, F efectiva (Montiel Olea-Pflueger; con un instrumento es la
F robusta de la primera etapa), IC de Anderson-Rubin por inversión, errores AKM (Adão, Kolesár y Morales 2019) y
pesos de Rotemberg (Goldsmith-Pinkham, Sorkin y Swift 2020) con crecimientos nacionales (aproximación sin leave-one-out).
Espacial (D3): conley() errores HAC espaciales con núcleo uniforme.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

SEED = 20261010


# =========================================================================================== DiD escalonado
def _medias(Y, idx):
    return Y[idx].mean(0) if len(idx) else np.full(Y.shape[1], np.nan)


def cs(Y: np.ndarray, g: np.ndarray, control: str = "nunca", e_min: int = -8, e_max: int = 8, B: int = 999,
       seed: int = SEED, w: np.ndarray | None = None) -> dict:
    """ATT(g,t) = [Ȳ_g(t) - Ȳ_g(g-1)] - [Ȳ_C(t) - Ȳ_C(g-1)], C = nunca tratadas (o aún no tratadas en t y en g-1).
    Devuelve ATT global (t ≥ g), ATT(e) para e ∈ [e_min, e_max] (e = t - g; e = -1 es la base) y sus IF."""
    n, T = Y.shape
    w = np.ones(n) if w is None else np.asarray(w, float) / np.mean(w)
    grupos = sorted(int(x) for x in np.unique(g[np.isfinite(g)]) if 1 <= x < T)
    att, peso, IF = {}, {}, {}
    for gg in grupos:
        tr = np.where(g == gg)[0]
        for t in range(T):
            if t == gg - 1:
                continue
            if control == "nunca":
                c = np.where(~np.isfinite(g))[0]
            else:
                c = np.where(((~np.isfinite(g)) | (g > max(t, gg - 1))) & (g != gg))[0]
            if len(c) == 0 or len(tr) == 0:
                continue
            dt = Y[tr, t] - Y[tr, gg - 1]
            dc = Y[c, t] - Y[c, gg - 1]
            wt, wc = w[tr], w[c]
            mt, mc = np.average(dt, weights=wt), np.average(dc, weights=wc)
            a = mt - mc
            inf = np.zeros(n)
            inf[tr] = wt * (dt - mt) / wt.sum() * n
            inf[c] -= wc * (dc - mc) / wc.sum() * n
            att[(gg, t)], peso[(gg, t)], IF[(gg, t)] = a, wt.sum(), inf
    def agrega(claves):
        if not claves:
            return np.nan, np.zeros(n)
        w = np.array([peso[k] for k in claves], float)
        w = w / w.sum()
        est = float(sum(wi * att[k] for wi, k in zip(w, claves)))
        inf = sum(wi * IF[k] for wi, k in zip(w, claves))
        return est, inf
    global_claves = [k for k in att if k[1] >= k[0]]
    est_g, if_g = agrega(global_claves)
    es = {}
    for e in range(e_min, e_max + 1):
        if e == -1:
            continue
        ks = [k for k in att if k[1] - k[0] == e]
        if ks:
            es[e] = agrega(ks)
    rng = np.random.default_rng(seed)
    V = rng.choice([-1.0, 1.0], size=(B, n))
    def boot(inf):
        return V @ inf / n
    bg = boot(if_g)
    se_g = float(bg.std(ddof=1))
    es_tab = {e: (v[0], float(boot(v[1]).std(ddof=1))) for e, v in es.items()}
    # p del bootstrap: proporción de |t*| ≥ |t| con t* centrado
    p_g = float(np.mean(np.abs(bg) >= abs(est_g))) if se_g > 0 else np.nan
    # matriz de covarianzas del estudio de eventos (para pretendencias y Honest DiD)
    eks = sorted(es)
    M = np.column_stack([boot(es[e][1]) for e in eks]) if eks else np.zeros((B, 0))
    return {"att": est_g, "se": se_g, "p_boot": p_g, "p_normal": float(2 * stats.norm.sf(abs(est_g / se_g))) if se_g > 0 else np.nan,
            "es": es_tab, "es_orden": eks, "es_vcov": np.cov(M, rowvar=False) if M.shape[1] > 1 else M.var(ddof=1, axis=0),
            "n_tratadas": int(np.isfinite(g).sum()), "n_controles": int((~np.isfinite(g)).sum()), "att_gt": att}


def pretendencias(res: dict, e_lo: int = -8, e_hi: int = -2) -> tuple[float, float, int]:
    """Wald conjunto de ATT(e) = 0 para e ∈ [e_lo, e_hi]; devuelve (estadístico, p, gl)."""
    idx = [i for i, e in enumerate(res["es_orden"]) if e_lo <= e <= e_hi]
    if not idx:
        return np.nan, np.nan, 0
    b = np.array([res["es"][res["es_orden"][i]][0] for i in idx])
    V = np.atleast_2d(res["es_vcov"])[np.ix_(idx, idx)]
    w = float(b @ np.linalg.pinv(V) @ b)
    return w, float(stats.chi2.sf(w, len(idx))), len(idx)


def honest_rm(res: dict, Mbar: float, alfa: float = 0.05) -> tuple[float, float]:
    """IC del ATT medio posterior (media simple de ATT(e), e ≥ 0) bajo magnitudes relativas M̄ (simplificado)."""
    pre = sorted(e for e in res["es_orden"] if e < -1)
    post = [e for e in res["es_orden"] if e >= 0]
    if not post:
        return np.nan, np.nan
    b_pre = [res["es"][e][0] for e in pre] + [0.0]          # incluye la base e = -1 (0)
    max_d = float(np.max(np.abs(np.diff(b_pre)))) if len(b_pre) > 1 else 0.0
    idx = [res["es_orden"].index(e) for e in post]
    V = np.atleast_2d(res["es_vcov"])[np.ix_(idx, idx)]
    w = np.ones(len(idx)) / len(idx)
    theta = float(np.mean([res["es"][e][0] for e in post]))
    se = float(np.sqrt(w @ V @ w))
    # el sesgo en el periodo posterior k crece como mucho M̄·max_d por periodo (acumulado): cota media
    cota = Mbar * max_d * float(np.mean(np.arange(1, len(post) + 1)))
    z = stats.norm.ppf(1 - alfa / 2)
    return theta - cota - z * se, theta + cota + z * se


def honest_ruptura(res: dict, rejilla=np.arange(0, 3.01, 0.05)) -> float:
    """Menor M̄ con el que el IC contiene el 0 (M̄ de ruptura)."""
    for m in rejilla:
        lo, hi = honest_rm(res, m)
        if lo <= 0 <= hi:
            return float(m)
    return float(rejilla[-1])


# =========================================================================================== Honest DiD (Rambachan y Roth)
def _eta_lp(Y: np.ndarray, X: np.ndarray, sig: np.ndarray) -> float:
    """η = min_{η, τ̃} η  s.a.  Y − X τ̃ ≤ η σ  (programa lineal; X puede tener 0 columnas)."""
    from scipy.optimize import linprog
    k = X.shape[1]
    c = np.zeros(k + 1)
    c[0] = 1.0
    A_ub = np.column_stack([-sig, -X]) if k else -sig[:, None]
    r = linprog(c, A_ub=A_ub, b_ub=-Y, bounds=[(None, None)] * (k + 1), method="highs")
    return float(r.x[0]) if r.status == 0 else np.inf


def _piezas_rm(n_pre: int, n_post: int, Mbar: float) -> list[np.ndarray]:
    """Δ^RM(M̄) = ∪_{s, signo} {δ: |δ_{t+1}−δ_t| ≤ M̄·signo·(δ_{s+1}−δ_s) ∀ t ≥ −1}, con δ_{−1} = 0 (la condición de signo
    queda implícita; con M̄ = 0 todas las piezas coinciden: tendencias paralelas exactas tras el tratamiento).
    δ = (δ_pre [e = −n_pre..−2], δ_post [e = 0..n_post−1]). Devuelve las matrices A de cada pieza (A δ ≤ 0)."""
    n = n_pre + n_post
    def dif_pre(r):            # δ_{r+1} − δ_r para r = 0..n_pre−1 (el último es δ_{−1} − δ_{−2} = −δ_{−2})
        v = np.zeros(n)
        if r + 1 < n_pre:
            v[r + 1] += 1
        v[r] -= 1
        return v
    def dif_post(t):           # δ_{t} − δ_{t−1} para t = 0..n_post−1 (t = 0: δ_0 − δ_{−1} = δ_0)
        v = np.zeros(n)
        v[n_pre + t] += 1
        if t > 0:
            v[n_pre + t - 1] -= 1
        return v
    piezas = []
    for s in range(n_pre):
        for signo in (1.0, -1.0):
            D = signo * dif_pre(s)
            filas = []   # signo·D ≥ 0 ya está implícito en |d_t| ≤ M̄·signo·D (y con M̄ = 0 no aplica): no se añade como fila
            for t in range(n_post):
                filas += [dif_post(t) - Mbar * D, -dif_post(t) - Mbar * D]
            piezas.append(np.array(filas))
    return piezas


def _arp_condicional(Y: np.ndarray, X: np.ndarray, sig: np.ndarray, SY: np.ndarray, alfa: float) -> bool:
    """Contraste condicional de Andrews, Roth y Pakes (2023) de H0: E[Y] − X τ̃ ≤ 0 para algún τ̃.
    η̂ = máx γ'Y s.a. γ ≥ 0, X'γ = 0, σ'γ = 1 (dual del programa de η); condicionando en el vértice óptimo γ*, η̂ sigue una
    normal N(0, γ*'Σγ*) truncada en [v_lo, v_up] (cotas por programación lineal fraccional, transformación de
    Charnes-Cooper). Devuelve True si rechaza al nivel α."""
    from scipy.optimize import linprog
    from scipy.stats import norm
    m, k = len(Y), X.shape[1]
    A_eq = np.vstack([X.T, sig[None, :]]) if k else sig[None, :]
    b_eq = np.r_[np.zeros(k), 1.0]
    r = linprog(-Y, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * m, method="highs")
    if r.status != 0:
        return False
    g = r.x
    eta = float(g @ Y)
    s2 = float(g @ SY @ g)
    if s2 <= 0:
        return eta > 0
    c = SY @ g / s2
    S = Y - c * eta
    # v_lo: máx γ'S/(1−γ'c) con γ'c < 1  → u = tγ, t = 1/(1−γ'c): máx u'S s.a. u ≥ 0, X'u = 0, σ'u = t, t − c'u = 1
    A1 = np.vstack([np.c_[X.T, np.zeros(k)] if k else np.zeros((0, m + 1)), np.r_[sig, -1.0][None, :], np.r_[-c, 1.0][None, :]])
    b1 = np.r_[np.zeros(k), 0.0, 1.0]
    r1 = linprog(-np.r_[S, 0.0], A_eq=A1, b_eq=b1, bounds=[(0, None)] * (m + 1), method="highs")
    v_lo = -r1.fun if r1.status == 0 else -np.inf
    if r1.status == 3:
        v_lo = np.inf
    # v_up: mín γ'S/(1−γ'c) con γ'c > 1  → u = tγ, t = 1/(γ'c−1): mín −u'S s.a. u ≥ 0, X'u = 0, σ'u = t, c'u − t = 1
    A2 = np.vstack([np.c_[X.T, np.zeros(k)] if k else np.zeros((0, m + 1)), np.r_[sig, -1.0][None, :], np.r_[c, -1.0][None, :]])
    r2 = linprog(-np.r_[S, 0.0], A_eq=A2, b_eq=b1, bounds=[(0, None)] * (m + 1), method="highs")
    v_up = float(r2.fun) if r2.status == 0 else np.inf   # el programa minimiza −u'S, que es justo la cota superior
    sd = np.sqrt(s2)
    lo, hi = max(v_lo, -1e9) / sd, min(v_up, 1e9) / sd
    lo = min(lo, eta / sd)
    hi = max(hi, eta / sd)
    den = norm.cdf(hi) - norm.cdf(lo)
    if den <= 1e-300:
        return eta / sd > norm.ppf(1 - alfa)
    pval = (norm.cdf(hi) - norm.cdf(eta / sd)) / den
    return pval < alfa


def honest_rr(res: dict, Mbar: float, alfa: float = 0.05, n_sim: int = 0, rejilla: np.ndarray | None = None,
              seed: int = SEED) -> tuple[float, float]:
    """IC de Rambachan y Roth (2023) para el ATT medio posterior (media de ATT(e), e ≥ 0) bajo magnitudes relativas M̄.
    Δ^RM se descompone en piezas poliédricas (una por diferencia previa y signo); en cada pieza se invierte el contraste
    condicional de Andrews, Roth y Pakes (2023); el IC es la unión sobre piezas. Usa ATT(e) y su covarianza.
    (n_sim y seed se conservan por compatibilidad; el contraste condicional no simula.)"""
    pre = sorted(e for e in res["es_orden"] if e < -1)
    post = sorted(e for e in res["es_orden"] if e >= 0)
    orden = pre + post
    idx = [res["es_orden"].index(e) for e in orden]
    b = np.array([res["es"][e][0] for e in orden])
    S = np.atleast_2d(res["es_vcov"])[np.ix_(idx, idx)]
    n_pre, n_post = len(pre), len(post)
    l = np.ones(n_post) / n_post
    theta = float(l @ b[n_pre:])
    se = float(np.sqrt(l @ S[n_pre:, n_pre:] @ l))
    if rejilla is None:
        rejilla = np.linspace(theta - 15 * se - 3 * abs(theta), theta + 15 * se + 3 * abs(theta), 301)
    Bm = np.linalg.svd(l[None, :])[2][1:].T if n_post > 1 else np.zeros((1, 0))
    aceptados = np.zeros(len(rejilla), bool)
    for A in _piezas_rm(n_pre, n_post, Mbar):
        SY = A @ S @ A.T
        sig = np.sqrt(np.clip(np.diag(SY), 1e-14, None))
        Ap = A[:, n_pre:]
        X = Ap @ Bm
        AB = A @ b
        for k, th in enumerate(rejilla):
            if aceptados[k]:
                continue
            aceptados[k] = not _arp_condicional(AB - Ap @ (th * np.ones(n_post)), X, sig, SY, alfa)
    if not aceptados.any():
        return np.nan, np.nan
    return float(rejilla[aceptados].min()), float(rejilla[aceptados].max())


def honest_rr_ruptura(res: dict, rejilla_M=np.arange(0, 2.01, 0.1), **kw) -> float:
    """Menor M̄ (rejilla de 0,1) con el que el IC de RR contiene el 0."""
    for m in rejilla_M:
        lo, hi = honest_rr(res, float(m), **kw)
        if not np.isfinite(lo) or lo <= 0 <= hi:
            return float(m)
    return float(rejilla_M[-1])


def _fe_no_tratadas(Y: np.ndarray, D: np.ndarray, it: int = 200) -> tuple[np.ndarray, np.ndarray]:
    """a_i + b_t ajustados por mínimos cuadrados sobre las celdas con D = 0 (proyecciones alternas)."""
    m = (D == 0) & np.isfinite(Y)
    a = np.zeros(Y.shape[0])
    b = np.zeros(Y.shape[1])
    Yz = np.where(m, Y, 0.0)
    cnt_i = m.sum(1).clip(1)
    cnt_t = m.sum(0).clip(1)
    for _ in range(it):
        a_new = ((Yz - b[None, :]) * m).sum(1) / cnt_i
        b_new = ((Yz - a_new[:, None]) * m).sum(0) / cnt_t
        if np.max(np.abs(a_new - a)) < 1e-10 and np.max(np.abs(b_new - b)) < 1e-10:
            a, b = a_new, b_new
            break
        a, b = a_new, b_new
    return a, b


def bjs(Y: np.ndarray, g: np.ndarray, B: int = 499, seed: int = SEED, e_max: int = 8) -> dict:
    n, T = Y.shape
    tt = np.arange(T)[None, :]
    D = (tt >= g[:, None]).astype(float)
    def estima(Yb, gb):
        Db = (tt >= gb[:, None]).astype(float)
        a, b = _fe_no_tratadas(Yb, Db)
        tau = Yb - a[:, None] - b[None, :]
        trat = Db == 1
        es = {}
        e_mat = tt - gb[:, None]
        for e in range(0, e_max + 1):
            m = trat & (e_mat == e)
            if m.any():
                es[e] = float(tau[m].mean())
        return float(tau[trat].mean()), es
    att, es = estima(Y, g)
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        if not np.isfinite(g[i]).any() or np.isfinite(g[i]).all():
            continue
        bs.append(estima(Y[i], g[i])[0])
    se = float(np.std(bs, ddof=1))
    return {"att": att, "se": se, "p_normal": float(2 * stats.norm.sf(abs(att / se))) if se > 0 else np.nan,
            "ic95": (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))), "es": es, "n_obs_tratadas": int(D.sum())}


def dcdh(Y: np.ndarray, g: np.ndarray, B: int = 999, seed: int = SEED) -> dict:
    """DID_l (l ≥ 0) con controles aún no tratados; con tratamiento binario absorbente coincide con CS «aún no tratados»."""
    r = cs(Y, g, control="aun_no", e_min=0, e_max=8, B=B, seed=seed)
    return {"att": r["att"], "se": r["se"], "p_normal": r["p_normal"], "es": r["es"]}


# =========================================================================================== regresión TWFE con dosis
def dm2(X: np.ndarray) -> np.ndarray:
    """Doble centrado (unidad y periodo) de una matriz unidades × periodos (panel equilibrado)."""
    return X - X.mean(1, keepdims=True) - X.mean(0, keepdims=True) + X.mean()


def twfe_cluster(Y: np.ndarray, Xs: list[np.ndarray], B: int = 999, seed: int = SEED) -> dict:
    """y_it = a_i + b_t + Σ_k β_k x_k,it + e; Xs: lista de matrices unidades × periodos. Conglomerado = unidad."""
    n, T = Y.shape
    y = dm2(Y).ravel()
    X = np.column_stack([dm2(x).ravel() for x in Xs])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    cl = np.repeat(np.arange(n), T)
    S = np.zeros((X.shape[1], X.shape[1]))
    scores = np.zeros((n, X.shape[1]))
    np.add.at(scores, cl, X * u[:, None])
    S = scores.T @ scores
    k = X.shape[1] + n + T - 1
    c = n / (n - 1) * (n * T - 1) / (n * T - k)
    V = c * XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(V))
    rng = np.random.default_rng(seed)
    tb = np.zeros((B, X.shape[1]))
    for b in range(B):
        w = rng.choice([-1.0, 1.0], n)[cl]
        yb = X @ beta + u * w
        bb = XtX_inv @ X.T @ yb
        ub = yb - X @ bb
        sc = np.zeros((n, X.shape[1]))
        np.add.at(sc, cl, X * ub[:, None])
        Vb = c * XtX_inv @ (sc.T @ sc) @ XtX_inv
        tb[b] = (bb - beta) / np.sqrt(np.diag(Vb))
    t = beta / se
    p_boot = np.array([np.mean(np.abs(tb[:, j]) >= abs(t[j])) for j in range(len(beta))])
    return {"beta": beta, "se": se, "V": V, "p_normal": 2 * stats.norm.sf(np.abs(t)), "p_boot": p_boot, "n": n, "T": T}


def wald(beta: np.ndarray, V: np.ndarray, idx: list[int]) -> tuple[float, float]:
    b = beta[idx]
    w = float(b @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ b)
    return w, float(stats.chi2.sf(w, len(idx)))


# =========================================================================================== IV y shift-share
def _ols(y, X):
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ y
    return b, y - X @ b, XtX_inv


def _hc1(X, u, XtX_inv):
    n, k = X.shape
    S = (X * u[:, None]).T @ (X * u[:, None])
    return n / (n - k) * XtX_inv @ S @ XtX_inv


def iv_just(y: np.ndarray, x: np.ndarray, z: np.ndarray, W: np.ndarray | None = None, w: np.ndarray | None = None) -> dict:
    """2SLS con una endógena x, un instrumento z y controles W (con constante). w: pesos opcionales."""
    n = len(y)
    W = np.ones((n, 1)) if W is None else np.column_stack([np.ones(n), W])
    if w is not None:
        s = np.sqrt(w / w.mean())
        y, x, z, W = y * s, x * s, z * s, W * s[:, None]
    # parcialar controles
    def res(v):
        return v - W @ np.linalg.lstsq(W, v, rcond=None)[0]
    yt, xt, zt = res(y), res(x), res(z)
    pi = float(zt @ xt / (zt @ zt))
    rf = float(zt @ yt / (zt @ zt))
    beta = rf / pi
    u = yt - beta * xt
    v = xt - pi * zt
    e_rf = yt - rf * zt
    k = W.shape[1] + 1
    se_iv = float(np.sqrt(n / (n - k) * np.sum(zt ** 2 * u ** 2)) / abs(zt @ xt))
    se_pi = float(np.sqrt(n / (n - k) * np.sum(zt ** 2 * v ** 2)) / (zt @ zt))
    se_rf = float(np.sqrt(n / (n - k) * np.sum(zt ** 2 * e_rf ** 2)) / (zt @ zt))
    F_eff = (pi / se_pi) ** 2 if se_pi > 0 else np.inf
    return {"beta": beta, "se": se_iv, "p": float(2 * stats.norm.sf(abs(beta / se_iv))), "pi": pi, "se_pi": se_pi,
            "rf": rf, "se_rf": se_rf, "p_rf": float(2 * stats.norm.sf(abs(rf / se_rf))), "F_eff": F_eff, "n": n,
            "_parciales": (yt, xt, zt, k)}


def anderson_rubin(res: dict, rejilla: np.ndarray, alfa: float = 0.05) -> tuple[float, float, bool]:
    """IC de AR por inversión (robusto a heterocedasticidad); devuelve (lo, hi, acotado)."""
    yt, xt, zt, k = res["_parciales"]
    n = len(yt)
    acept = []
    for b0 in rejilla:
        e = yt - b0 * xt
        g = float(zt @ e / (zt @ zt))
        u = e - g * zt
        se = np.sqrt(n / (n - k) * np.sum(zt ** 2 * u ** 2)) / (zt @ zt)
        acept.append(abs(g / se) <= stats.norm.ppf(1 - alfa / 2))
    acept = np.array(acept)
    if not acept.any():
        return np.nan, np.nan, True
    lo, hi = rejilla[acept].min(), rejilla[acept].max()
    return float(lo), float(hi), bool(not acept[0] and not acept[-1])


def akm_se(res: dict, shares: np.ndarray, shocks: np.ndarray, W: np.ndarray | None = None, coef: str = "rf") -> float:
    """Error estándar AKM (Adão, Kolesár y Morales 2019) del coeficiente de forma reducida o de 2SLS.
    shares: n × C (cuotas de exposición), shocks: C. Var = Σ_c g_c² (Σ_i s̃_ic ε̂_i)² / (Σ_i z̃_i x̃_i)²."""
    yt, xt, zt, k = res["_parciales"]
    n = len(yt)
    if shares.shape[1] < 2:          # con un solo shock el error AKM no está definido
        return np.nan
    Wm = np.ones((n, 1)) if W is None else np.column_stack([np.ones(n), W])
    st = shares - Wm @ np.linalg.lstsq(Wm, shares, rcond=None)[0]
    if coef == "rf":
        e = yt - res["rf"] * zt
        den = zt @ zt
    else:
        e = yt - res["beta"] * xt
        den = zt @ xt
    R = (st * e[:, None]).sum(0)
    return float(np.sqrt(np.sum(shocks ** 2 * R ** 2)) / abs(den))


def rotemberg(y: np.ndarray, x: np.ndarray, shares: np.ndarray, shocks: np.ndarray, W: np.ndarray | None = None) -> np.ndarray:
    """Pesos de Rotemberg α_c = g_c s_c'x̃ / Σ_c g_c s_c'x̃ (GPSS 2020) con crecimientos nacionales comunes."""
    n = len(y)
    Wm = np.ones((n, 1)) if W is None else np.column_stack([np.ones(n), W])
    xt = x - Wm @ np.linalg.lstsq(Wm, x, rcond=None)[0]
    num = shocks * (shares.T @ xt)
    return num / num.sum()


# =========================================================================================== espacial
def conley(y: np.ndarray, X: np.ndarray, coords: np.ndarray, corte_m: float) -> dict:
    """MCO con errores de Conley (núcleo uniforme, distancia euclídea en metros). X incluye la constante."""
    b, u, XtX_inv = _ols(y, X)
    d = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1))
    K = (d <= corte_m).astype(float)
    Xu = X * u[:, None]
    S = Xu.T @ K @ Xu
    V = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(V))
    V_hc = _hc1(X, u, XtX_inv)
    return {"beta": b, "se": se, "p": 2 * stats.norm.sf(np.abs(b / se)), "se_hc1": np.sqrt(np.diag(V_hc)), "n": len(y)}


# =========================================================================================== ajustes múltiples
def holm(p: list[float]) -> np.ndarray:
    p = np.asarray(p, float)
    m = len(p)
    orden = np.argsort(p)
    adj = np.empty(m)
    acum = 0.0
    for r, i in enumerate(orden):
        acum = max(acum, (m - r) * p[i])
        adj[i] = min(1.0, acum)
    return adj


def bh(p: list[float]) -> np.ndarray:
    p = np.asarray(p, float)
    m = len(p)
    orden = np.argsort(p)[::-1]
    adj = np.empty(m)
    prev = 1.0
    for r, i in enumerate(orden):
        rank = m - r
        prev = min(prev, p[i] * m / rank)
        adj[i] = prev
    return adj
