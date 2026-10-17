"""Panel de H1/H2 (Incasòl, Cataluña) y variante IPVA: estructura real (códigos, cohortes, centroides), SDID y bootstrap salvaje de Webb.

Ningún valor de resultado real: el resultado se simula con los procesos declarados en docs/v15/validacion_montecarlo/*.md.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.v15.montecarlo import _comun_v15 as C

T_PRE, T_POST = 7, 9            # 2022T2-2023T4 y 2024T1-2026T1 (adenda 1, punto 1)
PESOS_PRE = list(range(5))      # pesos SDID en 2022T2-2023T2; 2023T3-2023T4 reservados (adenda 1, punto 6)
POST = list(range(T_PRE, T_PRE + T_POST))
N_TR_H1, N_CO_H1, N_CO_10KM = 124, 74, 13   # 234*128/241 = 124 (cohorte 2024T1); 74 nunca tratados; 13 a >=10 km (adenda)


# ----------------------------------------------------------------------------- estructura
def estructura_h1(k: int = 1) -> dict:
    """124 tratados de la cohorte 2024T1 y 74 donantes nunca tratados (muestras al azar de los códigos reales); 13 donantes lejanos
    = los 13 de los 74 con mayor distancia mínima a un municipio tratado (cualquier cohorte)."""
    e = C.estructura_cataluna()
    g = C.rng(k, 0)
    tr = sorted(g.choice(e["coh1"], N_TR_H1, replace=False))
    co = sorted(g.choice(e["nunca"], N_CO_H1, replace=False))
    ce = C.centroides()
    ct = ce.loc[e["todos_trat"], ["lat", "lon"]].to_numpy()
    cc = ce.loc[co, ["lat", "lon"]].to_numpy()
    dmin = C.dist_km(cc, ct).min(1)
    lejos = np.argsort(-dmin)[:N_CO_10KM]
    return {"tr": tr, "co": co, "co_lejos": [co[i] for i in sorted(lejos)], "dmin_km": dmin, "dmin_lejos_min": float(np.sort(dmin)[::-1][:N_CO_10KM].min()),
            "n_donantes_mas_10km_entre_74": int((dmin >= 10).sum()), "coords": ce}


def armar(est: dict, donantes: str) -> dict:
    cods = est["tr"] + (est["co"] if donantes == "74" else est["co_lejos"])
    n_tr = len(est["tr"])
    xy = est["coords"].loc[cods, ["lat", "lon"]].to_numpy()
    return {"cods": cods, "tr": np.arange(n_tr), "co": np.arange(n_tr, len(cods)), "n": len(cods), "xy": xy,
            "L25": C.cholesky_exp(xy, 25.0), "L60": C.cholesky_exp(xy, 60.0), "cl": np.arange(len(cods))}


# ----------------------------------------------------------------------------- proceso generador (H1/H2)
def simular_h1(P: dict, g: np.random.Generator, tau: float, sd_e: float, T: int = T_PRE + T_POST, rho_e: float = 0.5,
               tendencia: float = 0.002, hetero: float = 0.5, g_trat: float = 0.0, pt_exacta: bool = False) -> tuple[np.ndarray, float]:
    """y_it = mu_i + d_i t + g1_i f1_t + g2_i f2_t + s_it + e_it + efecto. g_trat: sesgo de composición (cargas del factor mayores en tratados).
    pt_exacta: sin tendencias propias ni cargas heterogéneas de los factores (las tendencias paralelas se cumplen exactamente: solo efectos
    de tiempo comunes, campo espacial y AR(1) idiosincrásicos)."""
    n = P["n"]
    if pt_exacta:
        tendencia = 0.0
    f = C.ar1(g, 2, T, 0.6, 0.03)
    g1 = g.normal(1.0, 0.5, n)
    g1[P["tr"]] += g_trat
    g2 = P["L60"] @ g.standard_normal(n)
    if pt_exacta:
        g1, g2 = np.ones(n), np.zeros(n)
    z = g.standard_normal(n)
    y = (g.normal(0, 1, n)[:, None] + g.normal(0, tendencia, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += P["L25"] @ C.ar1(g, n, T, 0.5, 0.02)
    y += C.ar1(g, n, T, rho_e, sd_e, escala=np.exp(hetero * z - hetero ** 2 / 2))
    tau_i = tau * (1 + 0.5 * g.standard_normal(len(P["tr"])))
    y[np.ix_(P["tr"], POST)] += tau_i[:, None]
    return y, float(tau_i.mean())


# ----------------------------------------------------------------------------- SDID
def _proj_simplex(v: np.ndarray) -> np.ndarray:
    u = np.sort(v)[::-1]
    css = np.cumsum(u) - 1.0
    k = np.arange(1, len(v) + 1)
    rho = np.nonzero(u - css / k > 0)[0][-1]
    return np.maximum(v - css[rho] / (rho + 1), 0.0)


def _pesos(A: np.ndarray, t: np.ndarray, reg: float, its: int = 40) -> np.ndarray:
    """min_w ||A' w - t||^2 + reg ||w||^2 en el símplex (FISTA); A (k, m)."""
    G = A @ A.T
    b = A @ t
    k = A.shape[0]
    L = 2 * (np.linalg.eigvalsh(G)[-1] + reg)
    w = np.full(k, 1.0 / k)
    v, tk = w.copy(), 1.0
    for _ in range(its):
        wn = _proj_simplex(v - (2 * (G @ v - b) + 2 * reg * v) / L)
        tn = (1 + np.sqrt(1 + 4 * tk ** 2)) / 2
        v = wn + (tk - 1) / tn * (wn - w)
        w, tk = wn, tn
    return w


def _pesos_t(X: np.ndarray, y: np.ndarray, reg: float, its: int = 100) -> np.ndarray:
    G = X @ X.T
    b = X @ y
    k = G.shape[0]
    L = 2 * (np.linalg.eigvalsh(G)[-1] + reg)
    w = np.full(k, 1.0 / k)
    v, tk = w.copy(), 1.0
    for _ in range(its):
        wn = _proj_simplex(v - (2 * (G @ v - b) + 2 * reg * v) / L)
        tn = (1 + np.sqrt(1 + 4 * tk ** 2)) / 2
        v = wn + (tk - 1) / tn * (wn - w)
        w, tk = wn, tn
    return w


def sdid(Y: np.ndarray, tr: np.ndarray, co: np.ndarray, pre=PESOS_PRE, post=POST):
    """SDID (Arkhangelsky et al.): pesos de unidad omega (sobre co) y de tiempo lambda; devuelve tau, omega, lambda y puntuaciones s_i."""
    Ypre = Y[:, pre]
    ypost = Y[:, post].mean(1)
    Yc = Ypre[co]
    sig = np.diff(Yc, axis=1).std()
    zeta2 = np.sqrt(len(tr) * len(post)) * sig ** 2
    Ac = Yc - Yc.mean(axis=1, keepdims=True)
    tc = Ypre[tr].mean(axis=0)
    tc = tc - tc.mean()
    om = _pesos(Ac, tc, zeta2 * len(pre))
    Xl = (Yc - Yc.mean(axis=0, keepdims=True)).T
    yl = ypost[co] - ypost[co].mean()
    lam = _pesos_t(Xl, yl, (1e-6 * sig) ** 2 * len(co))
    s = ypost - Ypre @ lam
    return float(s[tr].mean() - om @ s[co]), om, lam, s


def placebo_se(Y: np.ndarray, tr: np.ndarray, co: np.ndarray, g: np.random.Generator, B: int, m: int | None = None):
    """Bootstrap de placebo (Arkhangelsky et al., alg. 4): reasigna m donantes (m = N_tr si hay holgura) como tratados y reestima.
    Devuelve (SE, m, tau_placebo). Si m < N_tr el SE no es el del algoritmo literal."""
    n_tr = len(tr)
    if m is None:
        m = n_tr
    if len(co) - m < 5:
        return np.nan, m, np.array([])
    out = np.empty(B)
    for b in range(B):
        p = g.permutation(co)
        out[b] = sdid(Y, p[:m], p[m:])[0]
    return float(out.std(ddof=1)), m, out


def wild_webb(a_tr: np.ndarray, tau: float, om: np.ndarray, s: np.ndarray, tr: np.ndarray, co: np.ndarray, cl: np.ndarray,
              g: np.random.Generator, B: int):
    """Wild cluster bootstrap-t de Webb sobre tau = sum_i a_i s_i (pesos SDID fijos), clusters cl, nulo impuesto.
    Devuelve (p, lo, hi, se)."""
    n = len(s)
    a = np.zeros(n)
    a[tr] = 1.0 / len(tr)
    a[co] = -om
    uc, pi = np.unique(cl, return_inverse=True)
    G = len(uc)
    r_un = s.copy()
    r_un[tr] -= s[tr].mean()
    r_un[co] -= om @ s[co]

    def se_de(r):
        c = np.zeros((G,) + r.shape[1:])
        np.add.at(c, pi, a[:, None] * r if r.ndim == 2 else a * r)
        return np.sqrt((c ** 2).sum(axis=0))

    se = se_de(r_un)
    t_obs = tau / se if se > 0 else np.nan
    r0 = s - om @ s[co]
    v = C.webb(g, (G, B))
    rstar = r0[:, None] * v[pi]
    taustar = (a[:, None] * rstar).sum(axis=0)
    sestar = se_de(rstar)
    tstar = taustar / np.maximum(sestar, 1e-15)
    p = float(np.mean(np.abs(tstar) >= abs(t_obs)))
    c = float(np.quantile(np.abs(tstar), 0.95))
    return p, tau - c * se, tau + c * se, float(se)
