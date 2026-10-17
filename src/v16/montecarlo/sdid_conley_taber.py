"""Monte Carlo V16 (fase 5) · SDID con inferencia de Conley-Taber (principal) y wild cluster bootstrap de Webb (alternativa), Q1b.

Proceso generador (declarado en docs/v16/validacion_montecarlo/sdid_conley_taber.md ANTES de simular):
  ESTRUCTURA (leída de entrenamiento y de intervenciones.csv, sin valores del resultado): municipios de entrenamiento con SERPAVI completo
  en 2019-2022 y 2024; tratados = municipios con zona tensionada declarada fuera de Cataluña; donantes = municipios de CCAA sin zonas;
  clusters = provincia; años 2019..2024 con 2023 fuera del estimador (pre 2019-2022, post 2024).
  RESULTADO SIMULADO (log SERPAVI €/m²): y_it = mu_i + d_i*t + sum_k g_ik f_kt + eta_{p(i),t} + s_it + e_it
    f_1, f_2 factores comunes AR(1) rho 0,6, sd 0,03; g_i1 ~ N(1; 0,5), g_i2 = campo espacial (alcance 150 km) N(0,1)
    eta: choque provincia-año AR(1) rho 0,5, sd 0,02;  s_it: campo gaussiano espacial exp(-d/100 km), AR(1) rho 0,5, sd 0,02
    e_it: AR(1) rho 0,5, sd marginal 0,05 * exp(0,4 z_i - 0,08) (heterocedasticidad entre municipios)
    d_i ~ N(0; 0,005) tendencia propia. Valores declarados, no estimados con datos reales.
  EFECTO (solo en el año post): nulo = 0; alternativa = -0,0075 (magnitud de referencia de la adenda) con heterogeneidad
  tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i en tratados).
Escenarios: A (estructura real: 2 tratados, 1 provincia) y B (diseño ampliado: patrón de las 8 zonas declaradas 15:2, 20:2, 48:3, 01:1).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_panel as C  # noqa: E402

K = 1
ANIOS = [2019, 2020, 2021, 2022, 2023, 2024]
USA = [0, 1, 2, 3, 5]  # 2023 fuera
TAU_REF = -0.0075
TAU_MDE = -0.071
B_PLACEBO = 99
B_WILD = 999


# ---------------------------------------------------------------- estructura
def construir_estructura(escenario: str) -> dict:
    s = C.estructura_serpavi_municipal()
    z = C.zonas_tensionadas()
    zc = set(z.ccaa)
    rng = C.rng_estructura(K)
    cod = s.cod.to_numpy()
    prov = s.prov.to_numpy()
    donante = ~s.ccaa.isin(zc).to_numpy()
    real = s.cod.isin(set(z.cod)).to_numpy() & (s.ccaa != "09").to_numpy()
    if escenario == "A":
        tr = np.where(real)[0]
    else:  # B: patrón 15:2, 20:2, 48:3, 01:1 con municipios de esas provincias presentes en la muestra
        patron = {"15": 2, "20": 2, "48": 3, "01": 1}
        tr = []
        for p, m in patron.items():
            idx = np.where((prov == p) & ~donante)[0]
            reales = [i for i in idx if real[i]]
            resto = [i for i in idx if not real[i]]
            elegidos = reales[:m] + list(rng.permutation(resto)[: max(0, m - len(reales))])
            tr += [int(i) for i in elegidos]
        tr = np.array(sorted(tr))
    co = np.where(donante)[0]
    coords = C.coords_municipios(cod, rng)
    return {"cod": cod, "prov": prov, "tr": tr, "co": co, "coords": coords, "n": len(cod),
            "L100": C.cholesky_exp(coords, 100.0), "L150": C.cholesky_exp(coords, 150.0)}


# ---------------------------------------------------------------- proceso generador
def simular_y(est: dict, rng: np.random.Generator, tau: float) -> tuple[np.ndarray, float]:
    n, T = est["n"], len(ANIOS)
    prov = est["prov"]
    up, pi = np.unique(prov, return_inverse=True)
    f = C.ar1(rng, 2, T, 0.6, 0.03)
    g1 = rng.normal(1.0, 0.5, n)
    g2 = est["L150"] @ rng.standard_normal(n)
    z = rng.standard_normal(n)
    esc = np.exp(0.4 * z - 0.08)
    y = (rng.normal(0, 1, n)[:, None] + rng.normal(0, 0.005, n)[:, None] * np.arange(T)[None, :]
         + g1[:, None] * f[0][None, :] + g2[:, None] * f[1][None, :])
    y += C.ar1(rng, len(up), T, 0.5, 0.02)[pi]
    sp = C.ar1(rng, n, T, 0.5, 1.0)  # innovaciones espaciales: aplica L a cada columna con dependencia temporal
    sp = est["L100"] @ sp * 0.02
    y += sp
    y += C.ar1(rng, n, T, 0.5, 0.05, escala=esc)
    tau_i = tau * (1 + 0.5 * rng.standard_normal(len(est["tr"])))
    y[est["tr"], T - 1] += tau_i
    att = float(tau_i.mean())
    return y[:, USA], att


# ---------------------------------------------------------------- SDID
def _proj_simplex(v: np.ndarray) -> np.ndarray:
    u = np.sort(v)[::-1]
    css = np.cumsum(u) - 1.0
    k = np.arange(1, len(v) + 1)
    rho = np.nonzero(u - css / k > 0)[0][-1]
    return np.maximum(v - css[rho] / (rho + 1), 0.0)


def _pesos(A: np.ndarray, t: np.ndarray, reg: float, its: int = 40) -> np.ndarray:
    """min_w ||A' w - t||^2 + reg ||w||^2 en el símplex (FISTA). A: (k, m)."""
    k = A.shape[0]
    L = 2 * (np.linalg.eigvalsh(A.T @ A)[-1] + reg)
    w = np.full(k, 1.0 / k)
    v, tk = w.copy(), 1.0
    for _ in range(its):
        grad = 2 * (A @ (A.T @ v - t)) + 2 * reg * v
        wn = _proj_simplex(v - grad / L)
        tn = (1 + np.sqrt(1 + 4 * tk ** 2)) / 2
        v = wn + (tk - 1) / tn * (wn - w)
        w, tk = wn, tn
    return w


def _pesos_gram(X: np.ndarray, y: np.ndarray, reg: float, its: int = 200) -> np.ndarray:
    """min_l ||X' l - y||^2 + reg ||l||^2 en el símplex, con X (T0, n): itera sobre el gramiano T0 x T0."""
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


def sdid(Y: np.ndarray, tr: np.ndarray, co: np.ndarray) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    """Y (n, 5): pre = 4 primeras columnas, post = última. Devuelve tau, omega (sobre co), lambda y puntuaciones s_i."""
    T0 = Y.shape[1] - 1
    pre, post = Y[:, :T0], Y[:, T0]
    Yc = pre[co]
    dif = np.diff(Yc, axis=1)
    sig = dif.std()
    zeta2 = np.sqrt(len(tr) * 1.0) * sig ** 2
    Ac = Yc - Yc.mean(axis=1, keepdims=True)
    tc = pre[tr].mean(axis=0)
    tc = tc - tc.mean()
    om = _pesos(Ac, tc, zeta2 * T0)
    # lambda: regresión de post sobre pre entre donantes (con constante: se centra por columnas)
    Xl = (Yc - Yc.mean(axis=0, keepdims=True)).T  # (T0, n_co)
    yl = post[co] - post[co].mean()
    lam = _pesos_gram(Xl, yl, (1e-6 * sig) ** 2 * len(co))
    s = post - pre @ lam
    tau = s[tr].mean() - om @ s[co]
    return float(tau), om, lam, s


def ct_placebo(est: dict, Y: np.ndarray, rng: np.random.Generator, B: int) -> np.ndarray:
    """Conley-Taber: reasigna el patrón de tratados (mismo reparto por provincia) a provincias donantes y reestima."""
    prov, co = est["prov"], est["co"]
    tr = est["tr"]
    patron = sorted(pd.Series(prov[tr]).value_counts().tolist(), reverse=True)
    prov_co = pd.Series(prov[co])
    idx_prov = {p: co[np.where(prov[co] == p)[0]] for p in prov_co.unique()}
    out = np.full(B, np.nan)
    for b in range(B):
        usados, elegidos = set(), []
        ok = True
        for m in patron:
            cand = [p for p, ix in idx_prov.items() if len(ix) >= m and p not in usados]
            if not cand:
                ok = False
                break
            p = cand[rng.integers(len(cand))]
            usados.add(p)
            elegidos += list(rng.choice(idx_prov[p], m, replace=False))
        if not ok:
            continue
        elegidos = np.array(elegidos)
        m = np.zeros(est['n'], bool)
        m[co] = True
        m[elegidos] = False
        out[b] = sdid(Y, elegidos, np.where(m)[0])[0]
    return out


def wild_webb(est: dict, Y: np.ndarray, tau: float, om: np.ndarray, lam: np.ndarray, s: np.ndarray, rng, B: int) -> tuple[float, float, float]:
    """Wild cluster bootstrap-t de Webb por provincia sobre tau = sum_i a_i s_i (pesos SDID fijos). Devuelve (p, ic_lo, ic_hi)."""
    tr, co, prov = est["tr"], est["co"], est["prov"]
    n = est["n"]
    a = np.zeros(n)
    a[tr] = 1.0 / len(tr)
    a[co] = -om
    up, pi = np.unique(prov, return_inverse=True)
    G = len(up)
    m_co = om @ s[co]
    m_tr = s[tr].mean()

    def se_de(r):  # r: residuos por unidad (n,) o (n,B)
        c = np.zeros((G,) + r.shape[1:])
        np.add.at(c, pi, a[:, None] * r if r.ndim == 2 else a * r)
        return np.sqrt((c ** 2).sum(axis=0)), c

    r_un = s.copy()
    r_un[tr] -= m_tr
    r_un[co] -= m_co
    se, _ = se_de(r_un)
    t_obs = tau / se if se > 0 else np.nan
    r0 = s - m_co  # nulo impuesto: misma media para todos
    v = C.webb(rng, (G, B))
    rstar = r0[:, None] * v[pi]
    taustar = (a[:, None] * rstar).sum(axis=0)
    sestar, _ = se_de(rstar)
    tstar = taustar / np.maximum(sestar, 1e-15)
    p = float(np.mean(np.abs(tstar) >= abs(t_obs)))
    c = float(np.quantile(np.abs(tstar), 0.95))
    return p, tau - c * se, tau + c * se


# ---------------------------------------------------------------- réplica
def una_rep(est: dict, rng: np.random.Generator, tau: float, alt: bool) -> list[float]:
    Y, att = simular_y(est, rng, tau)
    t, om, lam, s = sdid(Y, est["tr"], est["co"])
    pl = ct_placebo(est, Y, rng, B_PLACEBO)
    a = np.sort(np.abs(pl[np.isfinite(pl)]))
    if len(a) < 20:
        res = [att, t, np.nan, np.nan, np.nan]
    else:
        c = a[int(np.ceil(0.95 * len(a))) - 1]
        res = [att, t, t - c, t + c, float(abs(t) > c)]
    if alt:
        p, lo, hi = wild_webb(est, Y, t, om, lam, s, rng, B_WILD)
        res += [lo, hi, float(p <= 0.05)]
    return res


def _bloque(est, rngs, tau, alt):
    return [una_rep(est, r, tau, alt) for r in rngs]


def correr(est: dict, R: int, tau: float, k_sub: int, alt: bool, n_jobs: int = 4) -> np.ndarray:
    rngs = C.flujos(K * 100 + k_sub, R)
    trozos = [rngs[i::n_jobs * 4] for i in range(n_jobs * 4)]
    sal = Parallel(n_jobs=n_jobs)(delayed(_bloque)(est, tr, tau, alt) for tr in trozos)
    # reordenar a orden original
    res = [None] * R
    for i, blq in enumerate(sal):
        for j, fila in enumerate(blq):
            res[i + j * n_jobs * 4] = fila
    return np.array(res, float)


def evaluar(est: dict, R_nulo: int, R_alt: int, R_mde: int, alt: bool, n_jobs: int) -> dict:
    sal = {}
    for nom, R, tau, ks in (("nulo", R_nulo, 0.0, 1), ("ref", R_alt, TAU_REF, 2), ("mde", R_mde, TAU_MDE, 3)):
        t0 = time.time()
        M = correr(est, R, tau, ks, alt, n_jobs)
        d = {"seg": time.time() - t0}
        d["ct"] = C.resumen_escenario(M[:, 1], M[:, 2], M[:, 3], M[:, 4], M[:, 0])
        if alt:
            d["webb"] = C.resumen_escenario(M[:, 1], M[:, 5], M[:, 6], M[:, 7], M[:, 0])
        sal[nom] = d
    return sal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=2000)
    ap.add_argument("--R_mde", type=int, default=500)
    ap.add_argument("--alt", action="store_true", help="calcular también la alternativa Webb")
    ap.add_argument("--escenarios", default="A,B")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--salida", default=str(C.RAIZ / "output" / "v16" / "montecarlo" / "sdid_conley_taber"))
    a = ap.parse_args()
    res = {}
    filas = []
    for esc in a.escenarios.split(","):
        est = construir_estructura(esc)
        info = {"n_tratados": int(len(est["tr"])), "n_donantes": int(len(est["co"])),
                "provincias_tratadas": sorted(set(est["prov"][est["tr"]])), "provincias_donantes": int(len(set(est["prov"][est["co"]])))}
        r = evaluar(est, a.R, a.R_alt, a.R_mde, a.alt, a.jobs)
        res[esc] = {"estructura": info, "resultados": r}
        for nom, d in r.items():
            for inf in ("ct", "webb"):
                if inf in d:
                    filas.append({"escenario": esc, "inferencia": inf, "efecto": nom, **info, **d[inf], "segundos": d["seg"]})
    tabla = pd.DataFrame(filas)
    C.guardar(Path(a.salida), {"escenarios": res}, tabla)
    print(tabla.drop(columns=["provincias_tratadas"]).to_string())


if __name__ == "__main__":
    main()
