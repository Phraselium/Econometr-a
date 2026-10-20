"""V18 · fase 4 · núcleo numérico de los modelos de conjunto F1-F4 (y utilidades comunes con E7).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lectura de datos: recibe arrays. SEED = 20261010.

Herramientas:
- UECM / contraste de límites de Pesaran-Shin-Smith con valores críticos por Monte Carlo (remuestreo por bloques de las diferencias bajo la
  nula de no cointegración), con su tamaño y potencia medidos en réplicas independientes;
- DOLS de panel con efectos fijos y errores de Driscoll-Kraay (src/v18/herramientas/driscoll_kraay.py), PMG (Pesaran-Shin-Smith) y CS-ARDL/CCE-MG;
- contraste de cointegración de panel tipo Westerlund (Gτ: media de las t de la velocidad de ajuste por unidad) con bootstrap conjunto en el tiempo;
- fuera de muestra: bloques con embargo, Diebold-Mariano (HLN), Clark-West, Giacomini-White y conjunto de confianza de modelos (MCS);
- diferencia mínima detectable (MDE) por Monte Carlo y clasificación I1-I8.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import dm_test, holm  # noqa: E402,F401
from src.v18.herramientas import driscoll_kraay as DK  # noqa: E402

SEED = 20261010
Z80 = float(stats.norm.ppf(0.8))


# ---------------------------------------------------------------------------------------------- MCO y UECM
def mco(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    n, k = X.shape
    s2 = float(e @ e / max(n - k, 1))
    V = s2 * np.linalg.pinv(X.T @ X)
    return b, e, V, s2


def uecm(y, X, p: int = 2, mask=None) -> dict:
    """UECM de Pesaran-Shin-Smith, caso III (constante libre): Δy_t = c + α y_{t-1} + λ'x_{t-1} + Σ_{l<p} ψ_l Δy_{t-l} + ω'Δx_t + e.
    Devuelve α, t(α), F de H0: α = 0 y λ = 0, y el largo plazo β = −λ/α con error típico por el método delta."""
    y = np.asarray(y, float)
    X = np.asarray(X, float).reshape(len(y), -1)
    T, k = X.shape
    dy, dX = np.diff(y), np.diff(X, axis=0)
    t = np.arange(p, T)
    if mask is not None:                       # filas t que se omiten de la estimación (los rezagos usan los niveles reales)
        t = t[np.asarray(mask, bool)[t]]
    cols = [np.ones(len(t)), y[t - 1]] + [X[t - 1, j] for j in range(k)] + [dy[t - 1 - l] for l in range(1, p)] + [dX[t - 1, j] for j in range(k)]
    W = np.column_stack(cols)
    b, e, V, s2 = mco(dy[t - 1], W)
    a, lam = b[1], b[2:2 + k]
    R = np.zeros((k + 1, W.shape[1]))
    R[np.arange(k + 1), 1 + np.arange(k + 1)] = 1.0
    Rb = R @ b
    F = float(Rb @ np.linalg.solve(R @ V @ R.T, Rb) / (k + 1))
    beta = -lam / a if abs(a) > 1e-12 else np.full(k, np.nan)
    se_beta = np.full(k, np.nan)
    if abs(a) > 1e-12:
        for j in range(k):
            g = np.zeros(W.shape[1])
            g[1] = lam[j] / a ** 2
            g[2 + j] = -1.0 / a
            se_beta[j] = float(np.sqrt(max(g @ V @ g, 0.0)))
    ll = -0.5 * len(t) * (np.log(2 * np.pi * e @ e / len(t)) + 1)
    return {"alpha": float(a), "t": float(a / np.sqrt(V[1, 1])), "F": F, "beta_lp": beta, "se_beta_lp": se_beta, "n": len(t),
            "se_alpha": float(np.sqrt(V[1, 1])), "aic": float(-2 * ll + 2 * W.shape[1]), "resid": e, "coef": b, "W": W}


def _bloques(T: int, L: int, rng) -> np.ndarray:
    n = int(np.ceil(T / L))
    ini = rng.integers(0, T, size=n)
    return np.concatenate([(s + np.arange(L)) % T for s in ini])[:T]


def bounds_mc(y, X, p: int, B: int, seed: int, L: int = 4, mask=None):
    """Distribución de (F, t) del UECM bajo la nula de no cointegración: niveles I(1) construidos acumulando las diferencias
    remuestreadas por bloques (L = 4) de (Δy, ΔX) centradas, con la misma longitud que la muestra."""
    Z = np.column_stack([np.asarray(y, float), np.asarray(X, float).reshape(len(y), -1)])
    D = np.diff(Z, axis=0)
    D = D - D.mean(0)
    rng = np.random.default_rng(seed)
    Fs, ts = np.empty(B), np.empty(B)
    for b in range(B):
        idx = _bloques(len(D), L, rng)
        Zb = np.vstack([np.zeros(Z.shape[1]), np.cumsum(D[idx], axis=0)])
        r = uecm(Zb[:, 0], Zb[:, 1:], p, mask)
        Fs[b], ts[b] = r["F"], r["t"]
    return Fs, ts


def contraste_limites(y, X, p: int = 2, B: int = 2000, seed: int = SEED, B_val: int = 1000, mask=None) -> dict:
    """Contraste de límites con valores críticos simulados, tamaño medido en réplicas independientes y potencia frente a α = −0,10."""
    r = uecm(y, X, p, mask)
    Fs, ts = bounds_mc(y, X, p, B, seed, mask=mask)
    cF, ct = float(np.quantile(Fs, 0.95)), float(np.quantile(ts, 0.05))
    pF = float((1 + np.sum(Fs >= r["F"])) / (B + 1))
    pt = float((1 + np.sum(ts <= r["t"])) / (B + 1))
    F2, t2 = bounds_mc(y, X, p, B_val, seed + 1, mask=mask)
    tam = float(np.mean((F2 > cF) & (t2 < ct)))
    # potencia: y_t = y_{t-1} + α (y_{t-1} − β x_{t-1}) + e con x paseo aleatorio y errores remuestreados de los datos
    Z = np.column_stack([np.asarray(y, float), np.asarray(X, float).reshape(len(y), -1)])
    D = np.diff(Z, axis=0)
    D = D - D.mean(0)
    rng = np.random.default_rng(seed + 2)
    T = len(y)
    rech, R = 0, 400
    for _ in range(R):
        idx = _bloques(len(D), 4, rng)
        d = D[idx]
        xs = np.vstack([np.zeros(Z.shape[1] - 1), np.cumsum(d[:, 1:], axis=0)])
        ys = np.zeros(T)
        for s in range(1, T):
            ys[s] = ys[s - 1] - 0.10 * (ys[s - 1] - xs[s - 1].sum()) + d[s - 1, 0]
        rr = uecm(ys, xs, p, mask)
        rech += int(rr["F"] > cF and rr["t"] < ct)
    return {"alpha": r["alpha"], "t": r["t"], "F": r["F"], "cv_F95": cF, "cv_t05": ct, "p_F": pF, "p_t": pt, "p": max(pF, pt),
            "tamano_conjunto_5pct": tam, "potencia_alpha_-0,10": rech / R, "B": B, "B_validacion": B_val, "R_potencia": R,
            "beta_lp": r["beta_lp"].tolist(), "se_beta_lp": r["se_beta_lp"].tolist(), "n": r["n"], "se_alpha": r["se_alpha"]}


# ---------------------------------------------------------------------------------------------- paneles
def lead_lag(X, j: int):
    """Δx desplazado: Δx_{t+j} para t = 2..T-2 (índices de nivel), de forma que todos los desplazamientos de −1 a 1 existan. X (N, T, k)."""
    dX = np.diff(X, axis=1)                  # dX[:, s] = x_{s+1} - x_s
    T = X.shape[1]
    t = np.arange(2, T - 1)
    return dX[:, t + j - 1, :]


def panel_dols(Y, X, m: int | None = None, tiempo: bool = False) -> dict:
    """DOLS con efectos fijos (±1 adelanto y retardo de Δx) y Driscoll-Kraay; Y (N, T), X (N, T, k). El largo plazo son los k primeros coeficientes."""
    N, T, k = X.shape
    t = np.arange(2, T - 1)
    reg = [X[:, t, :]] + [lead_lag(X, j) for j in (-1, 0, 1)]
    Xa = np.concatenate(reg, axis=2)
    r = DK.fe_dk(Y[:, t], Xa, m=m, tiempo=tiempo)
    b = r["beta"][:k]
    se = {n: np.sqrt(np.diag(r[n])[:k]) for n in ("V_dk", "V_cluster", "V_hc1")}
    return {"beta": b, "se_dk": se["V_dk"], "se_cluster": se["V_cluster"], "se_hc1": se["V_hc1"], "m": r["m"], "T_efectivo": len(t), "N": N,
            "t_idx": t}


def residuo_equilibrio(Y, X, beta):
    """Desviación respecto al equilibrio estático con efectos fijos: y_it − α_i − β'x_it (α_i media de y − β'x por unidad)."""
    z = Y - np.einsum("itk,k->it", X, beta)
    return z - z.mean(axis=1, keepdims=True)


def pmg(Y, X, iters: int = 200, tol: float = 1e-9) -> dict:
    """PMG de Pesaran, Shin y Smith (1999) con ECM(1; 0): Δy_it = c_i + φ_i (y_{i,t-1} − θ'x_{i,t-1}) + ψ_i'Δx_it + e_it. θ común (ML concentrada
    por el algoritmo de iteración sobre θ), φ_i y ψ_i por unidad. Devuelve θ, su error típico asintótico, φ medio (grupo medio) y la semivida."""
    N, T, k = X.shape
    dy = np.diff(Y, axis=1)
    ylag = Y[:, :-1]
    xlag = X[:, :-1, :]
    dx = np.diff(X, axis=1)
    One = np.ones((T - 1, 1))
    Ms = []
    for i in range(N):
        W = np.column_stack([One, dx[i]])
        Ms.append(np.eye(T - 1) - W @ np.linalg.pinv(W))
    # arranque: largo plazo estático con efectos fijos
    z = Y - Y.mean(1, keepdims=True)
    xc = X - X.mean(1, keepdims=True)
    theta = np.linalg.lstsq(xc.reshape(-1, k), z.reshape(-1), rcond=None)[0]
    for _ in range(iters):
        phi, s2, psi = np.empty(N), np.empty(N), np.empty((N, k))
        for i in range(N):
            ec = ylag[i] - xlag[i] @ theta
            Zi = np.column_stack([One, dx[i], ec])
            b, e, _, s = mco(dy[i], Zi)
            phi[i], s2[i], psi[i] = b[-1], max(s, 1e-12), b[1:1 + k]
        A = np.zeros((k, k))
        c = np.zeros(k)
        for i in range(N):
            Xt = Ms[i] @ xlag[i]
            at = Ms[i] @ (dy[i] - phi[i] * ylag[i])
            A += phi[i] ** 2 / s2[i] * (Xt.T @ Xt)
            c += phi[i] / s2[i] * (Xt.T @ at)
        new = -np.linalg.solve(A, c)
        if np.max(np.abs(new - theta)) < tol:
            theta = new
            break
        theta = new
    se = np.sqrt(np.diag(np.linalg.inv(A)))
    pm = float(np.mean(phi))
    se_phi = float(np.std(phi, ddof=1) / np.sqrt(N))
    return {"theta": theta, "se_theta": se, "phi": phi, "psi": psi, "psi_medio": psi.mean(0), "se_psi_medio": psi.std(0, ddof=1) / np.sqrt(N),
            "phi_medio": pm, "se_phi_medio": se_phi,
            "semivida": float(np.log(0.5) / np.log(1 + pm)) if -1 < pm < 0 else float("nan"), "N": N, "T": T}


def pmg_bootstrap(Y, X, B: int, seed: int) -> dict:
    """Bootstrap por bloques de provincia (remuestreo de unidades con reposición) de θ y de φ medio."""
    rng = np.random.default_rng(seed)
    N = Y.shape[0]
    th, ph, ps = [], [], []
    for _ in range(B):
        idx = rng.integers(0, N, size=N)
        try:
            r = pmg(Y[idx], X[idx])
            th.append(r["theta"])
            ph.append(r["phi_medio"])
            ps.append(r["psi_medio"])
        except np.linalg.LinAlgError:
            continue
    th, ps = np.array(th), np.array(ps)
    return {"ic95_psi": [np.quantile(ps, 0.025, axis=0), np.quantile(ps, 0.975, axis=0)], "se_theta": th.std(0, ddof=1), "ic95_theta": [np.quantile(th, 0.025, axis=0), np.quantile(th, 0.975, axis=0)],
            "se_phi": float(np.std(ph, ddof=1)), "ic95_phi": [float(np.quantile(ph, 0.025)), float(np.quantile(ph, 0.975))], "B": len(th)}


def gtau_panel(Y, X) -> float:
    """Gτ tipo Westerlund: media entre unidades de la t de α en Δy = c + α y_{t-1} + λ'x_{t-1} + ψ'Δx_t + e, por unidad (UECM(1; 0))."""
    N, T, k = X.shape
    dy = np.diff(Y, axis=1)
    dx = np.diff(X, axis=1)
    W = np.concatenate([np.ones((N, T - 1, 1)), Y[:, :-1, None], X[:, :-1, :], dx], axis=2)
    G = np.einsum("itp,itq->ipq", W, W)
    Wy = np.einsum("itp,it->ip", W, dy)
    b = np.linalg.solve(G + 1e-12 * np.eye(W.shape[2]), Wy[..., None])[..., 0]
    e = dy - np.einsum("itp,ip->it", W, b)
    dof = T - 1 - W.shape[2]
    s2 = (e ** 2).sum(1) / dof
    Ginv = np.linalg.inv(G + 1e-12 * np.eye(W.shape[2]))
    se = np.sqrt(s2 * Ginv[:, 1, 1])
    return float(np.mean(b[:, 1] / se))


def coint_panel_bootstrap(Y, X, B: int, seed: int) -> dict:
    """p-valor (cola izquierda) de Gτ con bootstrap de signos conjunto en el tiempo: las diferencias (Δy, Δx) de todas las unidades, centradas por unidad, se multiplican
    por un signo ±1 común a todas las unidades y variables en cada periodo (conserva la covarianza transversal y la heterocedasticidad temporal); niveles por acumulación
    (nula de no cointegración). Se eligió frente al remuestreo por bloques porque con T = 14-23 el remuestreo duplica periodos, infla las t de la nula y vuelve el
    contraste conservador (tamaño 0,00 en la validación de la primera versión), mientras que el de signos da tamaño 0,03-0,05 (desviaciones, punto 10)."""
    N_, T, k = X.shape
    Z = np.concatenate([Y[:, :, None], X], axis=2)
    D = np.diff(Z, axis=1)
    D = D - D.mean(1, keepdims=True)
    g0 = gtau_panel(Y, X)
    rng = np.random.default_rng(seed)
    gs = np.empty(B)
    for b in range(B):
        sg = rng.choice([-1.0, 1.0], size=T - 1)
        Zb = np.concatenate([np.zeros((N_, 1, k + 1)), np.cumsum(D * sg[None, :, None], axis=1)], axis=1)
        gs[b] = gtau_panel(Zb[:, :, 0], Zb[:, :, 1:])
    return {"gtau": g0, "p": float((1 + np.sum(gs <= g0)) / (B + 1)), "cv_5pct": float(np.quantile(gs, 0.05)), "B": B}


def validar_coint_panel(N: int, T: int, k: int, R: int, B: int, seed: int) -> dict:
    """Tamaño y potencia del contraste anterior en un proceso generador con la estructura del diseño (N, T, k): factor común AR(1) (ρ = 0,5)
    con cargas N(1; 0,5²), ruido idiosincrásico y deriva 0,2; nula: y_it y x_it paseos aleatorios con deriva; alternativa: ajuste α_i ~ U(−0,5; −0,2) hacia β x_it."""
    rng = np.random.default_rng(seed)
    rej0 = rej1 = 0
    for r in range(R):
        f = np.zeros(T + 20)
        for s in range(1, T + 20):
            f[s] = 0.5 * f[s - 1] + rng.normal()
        gam = rng.normal(1, 0.5, size=(N, k + 1))
        inn = 0.5 * gam[:, None, :] * f[None, 20:, None] + rng.normal(size=(N, T, k + 1)) + 0.2
        x = np.cumsum(inn[:, :, 1:], axis=1)
        y0 = np.cumsum(inn[:, :, 0], axis=1)
        alpha = rng.uniform(-0.5, -0.2, size=N)
        y1 = np.zeros((N, T))
        for s in range(1, T):
            y1[:, s] = y1[:, s - 1] + alpha * (y1[:, s - 1] - 0.8 * x[:, s - 1, :].sum(1)) + inn[:, s, 0]
        for Yk, flag in ((y0, 0), (y1, 1)):
            p = coint_panel_bootstrap(Yk, x, B, int(rng.integers(1, 2 ** 31 - 1)))["p"]
            if flag == 0:
                rej0 += int(p < 0.05)
            else:
                rej1 += int(p < 0.05)
    return {"tamano_5pct": rej0 / R, "potencia": rej1 / R, "R": R, "B": B, "N": N, "T": T, "k": k}


def csardl_mg(Y, X, estatico: bool = False) -> dict:
    """CS-ARDL(1,0) (o CCE-MG estático) de grupo medio: y_it = c_i + φ_i y_{i,t-1} + β_i'x_it + δ_i'(ȳ_t, x̄_t) + e. Largo plazo θ_i = β_i/(1 − φ_i)
    (estático: β_i). Error típico = desviación entre unidades / √N. Herramienta NO APTA en V15/V16: solo descriptiva."""
    N, T, k = X.shape
    yb = Y.mean(0)
    xb = X.mean(0)
    ths, phis = [], []
    for i in range(N):
        if estatico:
            W = np.column_stack([np.ones(T), X[i], yb, xb])
            b = mco(Y[i], W)[0]
            ths.append(b[1:1 + k])
        else:
            t = np.arange(1, T)
            W = np.column_stack([np.ones(len(t)), Y[i, t - 1], X[i, t], yb[t], xb[t]])
            b = mco(Y[i, t], W)[0]
            phi = b[1]
            phis.append(phi)
            ths.append(b[2:2 + k] / (1 - phi))
    ths = np.array(ths)
    med = np.median(ths, axis=0)
    # media recortada (5 %) por la inestabilidad del cociente
    rec = stats.trim_mean(ths, 0.05, axis=0)
    return {"theta_mg": ths.mean(0), "theta_mediana": med, "theta_recortada": rec, "se_mg": ths.std(0, ddof=1) / np.sqrt(N),
            "phi_medio": float(np.mean(phis)) if phis else float("nan"), "N": N}


# ---------------------------------------------------------------------------------------------- fuera de muestra
def bloques_embargo(n: int, K: int, embargo: int):
    """K bloques contiguos de prueba; el entrenamiento excluye el bloque y `embargo` periodos a cada lado (CLAUDE.md)."""
    lims = np.linspace(0, n, K + 1).astype(int)
    for a, b in zip(lims[:-1], lims[1:]):
        test = np.arange(a, b)
        train = np.setdiff1d(np.arange(n), np.arange(max(a - embargo, 0), min(b + embargo, n)))
        yield train, test


def pred_bloques(dy, Wsets: dict, K: int = 5, embargo: int = 4):
    """Predicción a un paso de Δy_t con cada modelo (matriz de regresores en Wsets[nombre], fila t alineada con dy[t]) en bloques con embargo.
    Devuelve errores por modelo sobre la MISMA muestra de prueba (todas las filas completas en todos los modelos)."""
    ok = np.ones(len(dy), bool)
    for W in Wsets.values():
        ok &= np.all(np.isfinite(W), axis=1)
    ok &= np.isfinite(dy)
    idx = np.where(ok)[0]
    err = {k_: [] for k_ in Wsets}
    pred = {k_: [] for k_ in Wsets}
    tt = []
    for tr, te in bloques_embargo(len(idx), K, embargo):
        for nom, W in Wsets.items():
            Wc = W[idx]
            b = np.linalg.lstsq(Wc[tr], dy[idx][tr], rcond=None)[0]
            p = Wc[te] @ b
            pred[nom].append(p)
            err[nom].append(dy[idx][te] - p)
        tt.append(idx[te])
    return {k_: np.concatenate(v) for k_, v in err.items()}, {k_: np.concatenate(v) for k_, v in pred.items()}, np.concatenate(tt)


def clark_west(e1, e2, p1, p2):
    """Clark-West para modelos anidados: 1 = pequeño (AR), 2 = grande. f_t = e1² − (e2² − (p1 − p2)²); t de la media (normal, una cola)."""
    f = e1 ** 2 - (e2 ** 2 - (p1 - p2) ** 2)
    t = f.mean() / (f.std(ddof=1) / np.sqrt(len(f)))
    return {"CW": float(t), "p_una_cola": float(stats.norm.sf(t)), "n": len(f)}


def giacomini_white(e1, e2, h: int = 1):
    """Giacomini-White condicional con instrumentos (1, d_{t-1}): n·R² de la regresión de d_t·h_{t-1} sobre 1 → Wald χ²(2)."""
    d = e1 ** 2 - e2 ** 2
    Hh = np.column_stack([np.ones(len(d) - 1), d[:-1]])
    Z = Hh * d[1:, None]
    zb = Z.mean(0)
    S = np.cov(Z.T, bias=True)
    W = len(Z) * float(zb @ np.linalg.solve(S + 1e-15 * np.eye(2), zb))
    return {"GW": W, "p": float(stats.chi2.sf(W, 2)), "n": len(Z)}


def mcs(perdidas: dict, B: int = 999, alfa: float = 0.10, L: int = 4, seed: int = SEED) -> dict:
    """Conjunto de confianza de modelos (Hansen, Lunde y Nason, 2011) con el estadístico T_max y bootstrap de bloques; pérdidas por modelo (n,)."""
    nombres = list(perdidas)
    Lm = np.column_stack([perdidas[n] for n in nombres])
    n = len(Lm)
    rng = np.random.default_rng(seed)
    idx_b = [_bloques(n, L, rng) for _ in range(B)]
    vivos = list(range(len(nombres)))
    pvals = {}
    pmax = 0.0
    while len(vivos) > 1:
        sub = Lm[:, vivos]
        mi = sub.mean(0)
        di = mi - mi.mean()                                          # proporcional a d_i. de Hansen-Lunde-Nason
        bs = np.array([sub[ix].mean(0) for ix in idx_b])             # (B, m)
        bdi = bs - bs.mean(1, keepdims=True)
        se = bdi.std(0, ddof=1) + 1e-18
        t_i = di / se
        tmax = t_i.max()
        tb = ((bdi - di[None, :]) / se[None, :]).max(1)
        p = float(np.mean(tb >= tmax))
        peor = int(np.argmax(t_i))
        pmax = max(pmax, p)
        pvals[nombres[vivos[peor]]] = pmax
        vivos.pop(peor)
    pvals[nombres[vivos[0]]] = 1.0
    return {"p_mcs": pvals, "en_mcs": [n_ for n_, p in pvals.items() if p >= alfa], "alfa": alfa, "B": B}


# ---------------------------------------------------------------------------------------------- MDE
def mde_mc(sim, R: int = 2000, seed: int = SEED) -> dict:
    """MDE al 80 % de potencia (5 % bilateral) por Monte Carlo: sim(rng) -> (b_hat, se_hat) bajo la nula con la variación real y el σ declarado.
    MDE = (c_{0,975} + z_{0,8}) · sd(b_hat), con c el cuantil 97,5 % de |t| simulado (no se asume la normalidad)."""
    rng = np.random.default_rng(seed)
    bs, ts = np.empty(R), np.empty(R)
    for r in range(R):
        b, se = sim(rng)
        bs[r], ts[r] = b, b / se
    c = float(np.quantile(np.abs(ts), 0.95))
    return {"mde": float((c + Z80) * bs.std(ddof=1)), "c_t_95": c, "sd_b": float(bs.std(ddof=1)), "R": R, "seed": seed}


# ---------------------------------------------------------------------------------------------- clasificación
def clase_v18(estimable: bool, diseno_valido: bool, fallo_decisivo: bool, i7: bool, prueba_debil: bool, i8: bool | None = None) -> str:
    """Reglas de la adenda 1.2 (sin I8 la clase es provisional)."""
    if not estimable:
        return "NO ESTIMABLE"
    if not diseno_valido or fallo_decisivo:
        return "ASOCIACIÓN"
    if i7 and not prueba_debil:
        return "IDENTIFICADO"
    return "SUGESTIVO" if (i7 or prueba_debil) else "NO CONCLUYENTE"


# ---------------------------------------------------------------------------------------------- MC2E de panel con efectos fijos
def iv_panel_fe(y, endog, exog, inst):
    """2SLS con efectos fijos de unidad. y (N, T); endog (N, T) (un regresor endógeno); exog (N, T, ke) (puede ser vacío); inst (N, T, m) excluidos.
    Varianza agrupada por unidad (CR1) y F de primera etapa agrupado (H0: instrumentos excluidos = 0). Devuelve beta de la endógena, se, t, g.l. = G − 1."""
    n, t = y.shape
    dm = lambda a: a - a.mean(axis=1, keepdims=True)           # noqa: E731
    yt, xt = dm(y), dm(endog)
    Et = dm(exog.reshape(n, t, -1)) if exog is not None and exog.size else np.zeros((n, t, 0))
    It = dm(inst)
    Z = np.concatenate([Et, It], axis=2).reshape(n * t, -1)
    Xr = np.concatenate([xt[:, :, None], Et], axis=2).reshape(n * t, -1)
    yv = yt.reshape(-1)
    Pz = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    Xh = Pz @ Xr
    b = np.linalg.solve(Xh.T @ Xr, Xh.T @ yv)
    e = yv - Xr @ b
    G = n
    A = np.linalg.inv(Xh.T @ Xh)
    sc = np.stack([Xh[i * t:(i + 1) * t].T @ e[i * t:(i + 1) * t] for i in range(n)])
    V = A @ (G / (G - 1) * sc.T @ sc) @ A
    # primera etapa agrupada: x ~ exog + inst
    W = Z
    pi = np.linalg.pinv(W.T @ W) @ W.T @ xt.reshape(-1)
    u = xt.reshape(-1) - W @ pi
    Ainv = np.linalg.pinv(W.T @ W)
    scf = np.stack([W[i * t:(i + 1) * t].T @ u[i * t:(i + 1) * t] for i in range(n)])
    Vf = Ainv @ (G / (G - 1) * scf.T @ scf) @ Ainv
    ke = Et.shape[2]
    m = It.shape[2]
    pr = pi[ke:ke + m]
    Fe = float(pr @ np.linalg.solve(Vf[ke:ke + m, ke:ke + m] + 1e-15 * np.eye(m), pr) / m)
    se = float(np.sqrt(V[0, 0]))
    return {"beta": float(b[0]), "se": se, "t": float(b[0] / se), "gl": G - 1, "p": float(2 * stats.t.sf(abs(b[0] / se), G - 1)), "F_primera_etapa": Fe,
            "n_obs": n * t}


def dols_ts(y, X, k: int = 1, mask=None, maxlags: int = 4):
    """DOLS de Stock-Watson para series: y sobre constante, X en niveles y ±k adelantos/retardos de ΔX; errores de Newey-West (Bartlett, maxlags).
    mask: filas t (índice de nivel) que se omiten. Devuelve beta (k_x), se, n."""
    y = np.asarray(y, float)
    X = np.asarray(X, float).reshape(len(y), -1)
    T, kx = X.shape
    dX = np.vstack([np.full((1, kx), np.nan), np.diff(X, axis=0)])
    t = np.arange(k + 1, T - k)
    if mask is not None:
        t = t[np.asarray(mask, bool)[t]]
    cols = [np.ones(len(t)), *[X[t, j] for j in range(kx)]]
    for l in range(-k, k + 1):
        cols += [dX[t - l, j] for j in range(kx)]
    W = np.column_stack(cols)
    b, e, _, _ = mco(y[t], W)
    A = np.linalg.pinv(W.T @ W)
    s = W * e[:, None]
    S = s.T @ s
    for j in range(1, maxlags + 1):
        G = s[j:].T @ s[:-j]
        S += (1 - j / (maxlags + 1)) * (G + G.T)
    V = A @ S @ A
    return {"beta": b[1:1 + kx], "se": np.sqrt(np.diag(V))[1:1 + kx], "n": len(t), "const": float(b[0])}
