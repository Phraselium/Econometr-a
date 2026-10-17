"""V15 fase 4.1 · H5: combinación de 4 modelos (DFM, BVAR Minnesota de 6 variables, LASSO, ARDL) frente al AR(4) con DM-HLN unilateral,
Giacomini-White y Clark-West, y MCS al 10 %.

Proceso generador declarado en docs/v15/validacion_montecarlo/dfm_bvar_mcs.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/dfm_bvar_mcs.py [--R 2000] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats
from sklearn.linear_model import LassoLarsIC

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

HERR, K = "dfm_bvar_mcs", 5
N_TOT, P_OOS, M_IND = 94, 73, 20          # 2003T1-2026T2 = 94 trimestres; 73 errores fuera de muestra
PHI = np.array([0.3, 0.25, 0.2, 0.1])
LAM_BVAR = 0.2

DGP = """# dfm_bvar_mcs · H5: combinación DFM + BVAR + LASSO + ARDL frente al AR(4); DM-HLN, GW, CW y MCS

Herramienta de V15 (preregistro_v15.md H5 y sección 6; adenda 1 puntos 8 y 16). Código: `src/v15/montecarlo/dfm_bvar_mcs.py`; semilla `SeedSequence([20261010, 5, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de H5):** 94 trimestres (2003T1-2026T2), ventana expansiva desde el trimestre 22, de modo que hay **73 errores fuera de muestra** a horizonte 1; 20 indicadores «mensuales agregados al trimestre».
- **Factores y dependencia:** 2 factores comunes F_t = 0,7 F_{t−1} + u_t (u ~ N(0, I)). Indicadores x_jt = λ_j'F_t + 0,7 η_jt con cargas λ ~ N(0,1) sorteadas por réplica.
- **Variables del BVAR (6):** objetivo g_t (Δlog valor tasado), compraventas c_t = 0,6 F1_t + 0,8 ε, hipotecas h_t = 0,5 F2_t + 0,8 ε, ocupados o_t AR(1) ρ = 0,5, tipo AR(1) ρ = 0,9 e inflación AR(1) ρ = 0,8.
- **Objetivo:** g_t = 0,1 + Σ_{l=1..4} φ_l g_{t−l} + δ (0,7 F1_{t−1} + 0,7 F2_{t−1}) + ε_t, ε ~ N(0,1), φ = (0,3; 0,25; 0,2; 0,1) (AR(4) con memoria larga: los cuatro rezagos importan, de modo que los modelos más parsimoniosos de la combinación pierden precisión si no hay señal; con φ de memoria corta la combinación ya mejora al AR(4) sin señal, porque el AR(4) con 21 observaciones iniciales está mal estimado, y no existe un δ ≥ 0 de igual precisión); δ controla la señal de los indicadores.
- **Modelos (re-estimados en cada origen con la ventana expansiva):**
  - AR(4) (línea base).
  - DFM: 2 componentes principales de los 20 indicadores estandarizados + g_t, regresión directa a h = 1.
  - BVAR de Minnesota de 6 variables con 2 rezagos, media a priori 0, tightness λ = 0,2, decaimiento 1/l², escala de varianzas por AR(1) univariantes; media posterior de la ecuación de g (la verosimilitud marginal de Giannone-Lenza-Primiceri de la adenda se sustituye por λ fijo: coste; se declara).
  - LASSO: g_t y 20 indicadores, λ por BIC (LassoLarsIC; la validación temporal con embargo de la adenda se sustituye por BIC por coste).
  - ARDL: rezagos de g (1-4) y de c y h (1-4), orden por BIC.
  - Combinación = media simple de los 4 pronósticos.
- **Escenarios de señal:** δ = 0 (AR(4) es el proceso verdadero: nulo de Clark-West); δ* = el valor que iguala en media el ECM de la combinación y del AR(4) con n = 94 (nulo de igual precisión finita de Diebold-Mariano; calibrado con 300 réplicas por punto de una rejilla, semillas comunes; δ* hace cero la media de la diferencia de pérdidas); δ_20 = el que reduce un 20 % la razón entre los ECM medios (potencia; el pre-registro cita MDE del 18-30 %).
- **Pruebas** (combinación frente a AR(4), pérdida cuadrática, h = 1): DM-HLN unilateral (varianza de largo plazo = γ0 porque h = 1; t de Student con P − 1 gl); Giacomini-White condicional con instrumentos (1, d_{t−1}), χ²(2) (su hipótesis nula es condicional: bajo δ* solo es la igualdad incondicional, se reporta como diagnóstico); Clark-West unilateral normal.
- **MCS (Hansen-Lunde-Nason), tamaño:** proceso de pérdidas con 6 modelos (los 5 del pre-registro + AR(4)) con igualdad de precisión por construcción: errores e_mt = s_t √ρ-correlación 0,8 con t de 8 grados de libertad y volatilidad común log-AR(1) (ρ = 0,7, sd 0,3); pérdida cuadrática; P = 73. Estadístico T_max, bootstrap de bloques móviles (longitud 4, 999 réplicas), regla de eliminación e_max; tamaño = prob. de que el MCS excluya algún modelo.
- **R = 2.000** réplicas bajo cada nulo. **Criterio:** tamaño del DM-HLN, de CW (bajo δ = 0) en [0,04; 0,06]; para el MCS al 10 % la banda es [0,08; 0,12] (análoga, declarada aquí) y al 5 % [0,04; 0,06]. No hay IC: no hay cobertura. El pre-registro no nombra alternativa distinta de GW y CW; si DM-HLN no pasa y CW pasa, «alternativa APTA (CW)»; si ninguna pasa, «NO APTO → contraste solo descriptivo».
"""


# ------------------------------------------------------------------------------------------ proceso generador
def generar(g, delta):
    n = N_TOT + 50
    F = np.zeros((n, 2))
    u = g.standard_normal((n, 2))
    for t in range(1, n):
        F[t] = 0.7 * F[t - 1] + u[t]
    Lam = g.standard_normal((2, M_IND))
    X = F @ Lam + 0.7 * g.standard_normal((n, M_IND))
    c = 0.6 * F[:, 0] + 0.8 * g.standard_normal(n)
    h = 0.5 * F[:, 1] + 0.8 * g.standard_normal(n)

    def ar(rho):
        z, e = np.zeros(n), g.standard_normal(n)
        for t in range(1, n):
            z[t] = rho * z[t - 1] + e[t]
        return z
    o, tipo, pi = ar(0.5), ar(0.9), ar(0.8)
    y = np.zeros(n)
    e = g.standard_normal(n)
    for t in range(4, n):
        y[t] = 0.1 + PHI @ y[t - 4:t][::-1] + delta * 0.7 * (F[t - 1, 0] + F[t - 1, 1]) + e[t]
    s = slice(50, None)
    return y[s], X[s], np.column_stack([y[s], c[s], h[s], o[s], tipo[s], pi[s]])


# ------------------------------------------------------------------------------------------ modelos (pronóstico a h = 1 desde el origen t)
def _ols(Z, y):
    return np.linalg.lstsq(Z, y, rcond=None)[0]


def f_ar(y, t):
    n = t + 1
    Z = np.column_stack([np.ones(n - 4)] + [y[4 - l:n - l] for l in range(1, 5)])
    b = _ols(Z, y[4:n])
    z = np.r_[1.0, y[n - 1], y[n - 2], y[n - 3], y[n - 4]]
    return z @ b


def f_dfm(y, X, t):
    Xs = X[:t + 1]
    mu, sd = Xs.mean(0), Xs.std(0) + 1e-9
    U, S, Vt = np.linalg.svd((Xs - mu) / sd, full_matrices=False)
    Fh = (Xs - mu) / sd @ Vt[:2].T
    Z = np.column_stack([np.ones(t), y[:t], Fh[:t]])
    b = _ols(Z, y[1:t + 1])
    return np.r_[1.0, y[t], Fh[t]] @ b


def f_bvar(V, t, p=2):
    n = t + 1
    k = V.shape[1]
    sig2 = np.empty(k)
    for j in range(k):
        v = V[:n, j]
        b = (v[1:] - v[1:].mean()) @ (v[:-1] - v[:-1].mean()) / ((v[:-1] - v[:-1].mean()) ** 2).sum()
        sig2[j] = np.var(v[1:] - b * v[:-1], ddof=1) + 1e-9
    Z = np.column_stack([np.ones(n - p)] + [V[p - l:n - l, j] for l in range(1, p + 1) for j in range(k)])
    pen = np.r_[1e-6, [sig2[j] * l ** 2 / LAM_BVAR ** 2 for l in range(1, p + 1) for j in range(k)]]
    A = Z.T @ Z + np.diag(pen)
    b = np.linalg.solve(A, Z.T @ V[p:n, 0])
    z = np.r_[1.0, [V[n - l, j] for l in range(1, p + 1) for j in range(k)]]
    return z @ b


def f_lasso(y, X, t):
    Z = np.column_stack([y[:t], X[:t]])
    mu, sd = Z.mean(0), Z.std(0) + 1e-9
    yy = y[1:t + 1]
    r = yy - np.polyval(np.polyfit(y[:t], yy, 1), y[:t])
    m = LassoLarsIC(criterion="bic", noise_variance=float(r.var(ddof=2))).fit((Z - mu) / sd, yy)
    z = np.r_[y[t], X[t]]
    return m.predict(((z - mu) / sd)[None, :])[0]


def f_ardl(y, c, h, t):
    best, fc = np.inf, None
    n = t + 1
    for py in (1, 2, 3, 4):
        for px in (1, 2, 3, 4):
            m = max(py, px)
            if n - m < py + 2 * px + 6:
                continue
            Z = np.column_stack([np.ones(n - m)] + [y[m - l:n - l] for l in range(1, py + 1)]
                                + [c[m - l:n - l] for l in range(1, px + 1)] + [h[m - l:n - l] for l in range(1, px + 1)])
            b = _ols(Z, y[m:n])
            r = y[m:n] - Z @ b
            bic = len(r) * np.log((r @ r) / len(r)) + Z.shape[1] * np.log(len(r))
            if bic < best:
                z = np.r_[1.0, [y[n - l] for l in range(1, py + 1)], [c[n - l] for l in range(1, px + 1)], [h[n - l] for l in range(1, px + 1)]]
                best, fc = bic, z @ b
    return fc


def errores(y, X, V):
    t0 = N_TOT - P_OOS - 1          # primer origen: 21 obs → 22º trimestre pronosticado
    e = np.empty((P_OOS, 6))
    for i in range(P_OOS):
        t = t0 + i
        fs = [f_ar(y, t), f_dfm(y, X, t), f_bvar(V, t), f_lasso(y, X, t), f_ardl(y, V[:, 1], V[:, 2], t)]
        fc = np.mean(fs[1:], axis=0)
        real = y[t + 1]
        e[i] = [real - fs[0], real - fc, real - fs[1], real - fs[2], real - fs[3], real - fs[4]]
    fAR = None
    return e


# ------------------------------------------------------------------------------------------ pruebas
def pruebas(e_ar, e_c):
    P = len(e_ar)
    d = e_ar ** 2 - e_c ** 2
    dm = d.mean() / np.sqrt(d.var(ddof=0) / P)
    hln = dm * np.sqrt((P - 1) / P)
    p_hln = 1 - stats.t.cdf(hln, P - 1)
    Hh = np.column_stack([np.ones(P - 1), d[:-1]])
    Zt = Hh * d[1:, None]
    zb = Zt.mean(0)
    S = Zt.T @ Zt / (P - 1)
    gw = (P - 1) * zb @ np.linalg.solve(S, zb)
    p_gw = 1 - stats.chi2.cdf(gw, 2)
    f_ar_, f_c_ = None, None
    return p_hln, p_gw, d.mean()


def pruebas_cw(e_ar, e_c):
    # fAR − fC = e_c − e_ar (pronóstico menos real); ajuste de CW: e_ar² − (e_c² − (f_ar − f_c)²)
    P = len(e_ar)
    adj = e_ar ** 2 - (e_c ** 2 - (e_c - e_ar) ** 2)
    t = adj.mean() / np.sqrt(adj.var(ddof=1) / P)
    return 1 - stats.norm.cdf(t)


def una(g, delta):
    y, X, V = generar(g, delta)
    e = errores(y, X, V)
    p_hln, p_gw, dbar = pruebas(e[:, 0], e[:, 1])
    p_cw = pruebas_cw(e[:, 0], e[:, 1])
    return [p_hln, p_gw, p_cw, dbar, (e[:, 1] ** 2).mean() / (e[:, 0] ** 2).mean(), (e[:, 0] ** 2).mean()]


def bloque(gens, delta):
    return [una(g, delta) for g in gens]


def correr(R, delta, etapa, jobs):
    gens = C.flujos(K, R, etapa)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(c, delta) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, f in enumerate(b):
            res[i + j * 40] = f
    return np.array(res, float)


def calibra(jobs, Rg=300):
    """Rejilla de δ con Rg réplicas y semillas comunes. δ* = cruce de cero de la media de d = pérdida(AR4) − pérdida(combinación) (igualdad de
    ECM esperado, el nulo de Diebold-Mariano); δ_20 = cruce de 0,8 de la razón de ECM medios (media de pérdidas de la combinación / del AR(4))."""
    grid = [0.0, 0.15, 0.3, 0.45, 0.6, 0.8, 1.0, 1.3]
    dbar, rat = [], []
    for d in grid:
        M = correr(Rg, d, 99, jobs)
        dbar.append(float(M[:, 3].mean()))
        rat.append(float(1 - M[:, 3].mean() / M[:, 5].mean()))
    return _interp(grid, -np.array(dbar), 0.0), _interp(grid, np.array(rat), 0.8), {"dbar_media": dict(zip(grid, dbar)), "razon_ECM_medios": dict(zip(grid, rat))}


def _interp(grid, r, obj):
    # r decrece con δ (a partir de un máximo); busca el primer cruce descendente de obj
    for i in range(1, len(grid)):
        if (r[i - 1] - obj) * (r[i] - obj) <= 0 and r[i - 1] != r[i]:
            return float(grid[i - 1] + (obj - r[i - 1]) * (grid[i] - grid[i - 1]) / (r[i] - r[i - 1]))
    return float(grid[-1] if r[-1] > obj else grid[0])


# ------------------------------------------------------------------------------------------ MCS (T_max, bootstrap de bloques)
def mcs(L, alphas, g, B=999, bl=4):
    P, m = L.shape
    nb = int(np.ceil(P / bl))
    st = g.integers(0, P - bl + 1, (B, nb))
    idx = (st[:, :, None] + np.arange(bl)[None, None, :]).reshape(B, -1)[:, :P]
    Lb = L[idx].mean(1)                 # (B, m)
    Lbar = L.mean(0)
    sal = {a: set(range(m)) for a in alphas}
    act = list(range(m))
    elim = {a: False for a in alphas}
    # un único recorrido de eliminaciones; el conjunto al nivel a es lo que queda cuando p >= a
    conjunto = list(range(m))
    pvals = []
    while len(conjunto) > 1:
        S = np.array(conjunto)
        d = Lbar[S][:, None] - Lbar[S][None, :]
        db = Lb[:, S][:, :, None] - Lb[:, S][:, None, :]
        v = ((db - d[None]) ** 2).mean(0) + np.eye(len(S))
        t = d / np.sqrt(v)
        tmax = np.max(t)
        tb = ((db - d[None]) / np.sqrt(v)[None]).reshape(B, -1).max(1)
        p = float(np.mean(tb >= tmax))
        pvals.append((tuple(conjunto), p))
        i = int(np.argmax(t.max(1)))
        conjunto = [c for k, c in enumerate(conjunto) if k != i]
    # p-valor de cada modelo = máx acumulado de p
    out = {}
    for a in alphas:
        # el MCS al nivel a: el primer conjunto cuyo p >= a
        mc = None
        for cj, p in pvals:
            if p >= a:
                mc = cj
                break
        out[a] = len(mc) if mc is not None else 1
    return out


def mcs_rep(g, m=6, P=P_OOS):
    ls = np.zeros(P)
    ls[0] = g.normal(0, 0.3)
    for t in range(1, P):
        ls[t] = 0.7 * ls[t - 1] + 0.3 * np.sqrt(1 - 0.49) * g.standard_normal()
    vol = np.exp(ls)
    cov = 0.8 * np.ones((m, m)) + 0.2 * np.eye(m)
    z = g.standard_normal((P, m)) @ np.linalg.cholesky(cov).T
    z = z / np.sqrt(g.chisquare(8, (P, 1)) / 8) * np.sqrt(6 / 8)          # t(8) con varianza 1
    L = (vol[:, None] * z) ** 2
    return mcs(L, (0.10, 0.05), g)


def bloque_mcs(gens):
    return [mcs_rep(g) for g in gens]


def correr_mcs(R, etapa, jobs):
    gens = C.flujos(K, R, etapa)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque_mcs)(c) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, f in enumerate(b):
            res[i + j * 40] = f
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=1000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    t0 = time.time()
    dstar, d20, rejilla = calibra(a.jobs)
    print("calibración", dstar, d20, rejilla, round(time.time() - t0), flush=True)
    esc = {"nulo_AR4_verdadero (delta=0)": 0.0, "nulo_igual_ECM (delta*)": dstar, "alt_ECM_-20% (delta_20)": d20}
    filas = []
    for i, (nm, d) in enumerate(esc.items()):
        R = a.R if i < 2 else a.R_alt
        M = correr(R, d, 10 + i, a.jobs)
        filas.append({"escenario": nm, "delta": d, "R": R, "ratio_ECM_medio": float(M[:, 4].mean()), "dif_perdida_media": float(M[:, 3].mean()), "rechazo_DM_HLN": float((M[:, 0] <= 0.05).mean()),
                      "rechazo_GW_cond": float((M[:, 1] <= 0.05).mean()), "rechazo_CW": float((M[:, 2] <= 0.05).mean()),
                      "rechazo_DM_HLN_10pct": float((M[:, 0] <= 0.10).mean())})
        print(filas[-1], round(time.time() - t0), flush=True)
    tab = pd.DataFrame(filas)
    sm = correr_mcs(a.R, 20, a.jobs)
    n10 = np.array([s[0.10] for s in sm]); n05 = np.array([s[0.05] for s in sm])
    mcs_t = {"tamano_mcs_10pct": float((n10 < 6).mean()), "tamano_mcs_5pct": float((n05 < 6).mean()), "R": a.R, "tam_medio_conjunto_10": float(n10.mean())}
    print(mcs_t, round(time.time() - t0), flush=True)
    t_hln = float(tab.loc[1, "rechazo_DM_HLN"]); t_cw = float(tab.loc[0, "rechazo_CW"])
    v_hln = C.veredicto(t_hln, None, a.R)
    v_cw = C.veredicto(t_cw, None, a.R)
    v_gw = C.veredicto(float(tab.loc[1, "rechazo_GW_cond"]), None, a.R)
    v_m10 = C.veredicto(mcs_t["tamano_mcs_10pct"], None, a.R, banda_tam=(0.08, 0.12))
    v_m05 = C.veredicto(mcs_t["tamano_mcs_5pct"], None, a.R)
    if v_hln["apto"]:
        glob_dm = "APTO (DM-HLN)"
    elif v_cw["apto"]:
        glob_dm = "alternativa APTA (Clark-West)"
    else:
        glob_dm = "NO APTO → contraste solo descriptivo"
    glob_mcs = "APTO (MCS)" if v_m10["apto"] else "NO APTO → MCS solo descriptivo"
    r = C.base_resultado("H5 (combinación DFM+BVAR+LASSO+ARDL frente a AR(4); MCS)", {"T": N_TOT, "errores_OOS": P_OOS, "modelos": 4}, "DM-HLN unilateral, GW, CW; MCS T_max")
    r["estimacion"] = {"tamano_DM_HLN": t_hln, "tamano_CW_delta0": t_cw, "tamano_GW": float(tab.loc[1, "rechazo_GW_cond"]), "potencia_DM_HLN_ECM_-20": float(tab.loc[2, "rechazo_DM_HLN"]),
                       "potencia_CW_ECM_-20": float(tab.loc[2, "rechazo_CW"]), **mcs_t, "cobertura": "no aplica (pruebas)"}
    r["ic95"] = C.ic_binomial(t_hln, a.R)
    r["diagnosticos"] = {"veredicto_DM": glob_dm, "veredicto_MCS": glob_mcs, "v_HLN": v_hln, "v_CW": v_cw, "v_GW": v_gw, "v_MCS10": v_m10, "v_MCS05": v_m05,
                         "delta_estrella": dstar, "delta_20": d20, "rejilla_ratio_ECM": rejilla, "R": a.R, "semilla": C.SEED}
    r["fuera_muestra"] = {"modelo": "combinación simulada", "rmse": None, "dm_vs_ar4": f"tamaño HLN {t_hln:.3f}"}
    r["notas"] = ["BVAR con λ fijo y LASSO por BIC (sustitutos declarados de GLP y de la validación temporal con embargo).",
                  "La banda del MCS al 10 % ([0,08; 0,12]) es análoga a la del 5 % y está declarada en este documento."]
    md = (f"## Resultados (R = {a.R} bajo cada nulo; semilla {C.SEED}, k = {K})\n\nCalibración: δ* = {dstar:.3f}; δ_20 = {d20:.3f}. Rejilla (diferencia media de pérdidas y razón de ECM medios con 300 réplicas): {rejilla}\n\n"
          + C.md_tabla(tab) + f"\n**MCS (pérdidas con igualdad de precisión, 6 modelos, P = 73):** {mcs_t}\n\n**Veredicto DM/CW: {glob_dm}.** **Veredicto MCS: {glob_mcs}.**\n\n"
          f"- DM-HLN: {v_hln['veredicto']} {'; '.join(v_hln['fallos'])}\n- CW (δ = 0): {v_cw['veredicto']} {'; '.join(v_cw['fallos'])}\n- GW: {v_gw['veredicto']} {'; '.join(v_gw['fallos'])}\n"
          f"- MCS 10 %: {v_m10['veredicto']} {'; '.join(v_m10['fallos'])}\n- MCS 5 %: {v_m05['veredicto']} {'; '.join(v_m05['fallos'])}\n")
    C.cerrar(HERR, r, tab, md)
    print(glob_dm, glob_mcs)


if __name__ == "__main__":
    main()
