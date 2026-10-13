#!/usr/bin/env python3
"""V8-F4 M4: relaciones de largo plazo del precio real de compra (desde 1997T3) y del alquiler real (desde 2002T1).

Cointegracion con DOLS (Stock-Watson, econ_utils.dols), FMOLS (Phillips-Hansen, implementacion propia con deterministas,
contrastada con arch en los tests) y ARDL-bounds (Pesaran-Shin-Smith, statsmodels UECM). Rupturas: sin ellas y con escalones de nivel en los
periodos pre-registrados (P2..P5) + COVID (+ EPA 2021 en hogares) y Gregory-Hansen (cambio de nivel, fecha desconocida) con valores criticos
simulados bajo la nula. Velocidad de ajuste y semivida; diagnosticos; fuera de muestra en bloques con embargo frente a AR(4) en la MISMA
muestra; contribuciones de largo plazo por periodo (metodo `contabilidad_lp`, bandas por bootstrap por bloques) y contabilidad
hogares-viviendas (`contabilidad`). Capa C4 (asociacion): sin lenguaje causal.
Uso: python3 src/v8/m4_largo_plazo.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402
from scipy import stats  # noqa: E402
from statsmodels.stats.outliers_influence import variance_inflation_factor  # noqa: E402
from statsmodels.tsa.stattools import adfuller, coint  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, diagnostics, dm_test, dols  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
DATOS = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
SCRIPT = "src/v8/m4_largo_plazo.py"
PERIODOS = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"),
            "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", "2026Q2")}
K_DOLS = 1
HAC = 4
BLOQUE = 8

# variable -> (descripcion, familia)
FAMILIA = {"renta": "empleo_renta", "tipo": "credito_tipos", "credito": "credito_tipos", "pob": "demografia", "hogares": "demografia", "oferta": "oferta"}
DESC = {"renta": "ln PIB volumen", "tipo": "tipo hipotecario real BdE (pp)", "credito": "ln saldo credito vivienda real", "pob": "ln poblacion total (interpolada)",
        "hogares": "ln hogares EPA (ruptura EPA 2021)", "oferta": "ln terminadas acumuladas desde 1995 (libres; 1995-2007 anual/4)"}
SPECS = {
    "compra": {"C1": ["renta", "tipo"], "C2": ["renta", "tipo", "pob"], "C3": ["renta", "tipo", "pob", "credito"],
               "C4": ["renta", "tipo", "pob", "credito", "oferta"]},
    "alquiler": {"A1": ["renta", "tipo"], "A2": ["renta", "tipo", "hogares"], "A2b": ["renta", "tipo", "pob"],
                 "A3": ["renta", "tipo", "hogares", "credito"], "A4": ["renta", "tipo", "hogares", "credito", "oferta"]},
}
COMPLETA = {"compra": "C4", "alquiler": "A4"}   # fijada a priori como especificacion de cabecera (no por su p)
Y_COL = {"compra": "ln_p_tasado_real", "alquiler": "ln_ipc_alquiler_real"}
MEDIDA = {"compra": "valor tasado MIVAU, real (IPC general)", "alquiler": "IPC alquiler, real (IPC general)"}
INICIO = {"compra": "1997Q3", "alquiler": "2002Q1"}


# ------------------------------------------------------------------ utilidades
def md_tabla(df: pd.DataFrame, fmt: str = "{:.3f}") -> str:
    cols = [str(c) for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(("" if (isinstance(v, float) and v != v) else fmt.format(v) if isinstance(v, (float, np.floating)) else str(v)) for v in r.values) + " |")
    return "\n".join(out)


def preparar(d: pd.DataFrame) -> pd.DataFrame:
    G = pd.DataFrame(index=d.index)
    G["y_compra"] = d["ln_p_tasado_real"]
    G["y_alquiler"] = d["ln_ipc_alquiler_real"]
    G["renta"] = d["ln_pib_vol_idx"]
    G["tipo"] = d["tipo_hip_real_bde"]
    G["pob"] = d["ln_pob_total"]
    G["hogares"] = d["ln_hogares_epa"]
    G["credito"] = d["ln_credito_stock_bde_real"]
    G["oferta"] = np.log(d["terminadas"].cumsum())
    for P in ("P2", "P3", "P4", "P5"):
        G["s_" + P] = (d.index >= PERIODOS[P][0]).astype(float)
    G["covid"] = d["covid"].astype(float)
    G["epa2021"] = d["epa2021"].astype(float)
    return G


def fijas_de(xs, rupturas):
    f = ["epa2021"] if "hogares" in xs else []
    if rupturas:
        # con hogares, COVID (2020T2-T4) = s_P4 - epa2021 exactamente: se omite para evitar colinealidad perfecta
        f = ["s_P2", "s_P3", "s_P4", "s_P5"] + ([] if "hogares" in xs else ["covid"]) + f
    return f


def ventana(G, mk):
    """Posiciones (i0, i1) del primer trimestre de INICIO y del ultimo con dato del precio."""
    idx = list(G.index)
    ult = G["y_" + mk].last_valid_index()
    return idx.index(INICIO[mk]), idx.index(ult)


def vif_max(X):
    if X.shape[1] < 2:
        return np.nan
    Z = np.column_stack([np.ones(len(X)), X])
    return float(max(variance_inflation_factor(Z, i + 1) for i in range(X.shape[1])))


def diag_de(y, W):
    """Diagnosticos econ_utils sobre un OLS auxiliar (y ~ W)."""
    res = sm.OLS(y, W).fit()
    dg = diagnostics(res)
    return {"bg_p": dg.get("BG4_p"), "bp_p": dg.get("BP_p"), "jb_p": dg.get("JB_p"), "reset_p": dg.get("RESET_p"),
            "cusum_estable": bool(dg.get("CUSUM_p", np.nan) > 0.05) if dg.get("CUSUM_p", np.nan) == dg.get("CUSUM_p", np.nan) else np.nan}


def semivida(lam):
    return float(np.log(0.5) / np.log(1 + lam)) if (lam == lam and -1 < lam < 0) else np.nan


# ------------------------------------------------------------------ FMOLS (Phillips-Hansen) con deterministas
def fmols(y, Z, X, bw=None):
    """y = Z g + X b + u; X I(1). Devuelve (theta [Z, X], cov, residuos, bw). Kernel Bartlett.
    Correccion: y+ = y - Oue Oee^-1 e; sesgo: T [0; D+ue]. Se pierde la 1a observacion (e = Dx demeaned)."""
    y, Z, X = np.asarray(y, float), np.asarray(Z, float), np.asarray(X, float)
    W = np.column_stack([Z, X])
    u = y - W @ np.linalg.lstsq(W, y, rcond=None)[0]
    e = np.diff(X, axis=0)
    e = e - e.mean(0)
    u1, W1, y1 = u[1:], W[1:], y[1:]
    T = len(u1)
    m = X.shape[1]
    xi = np.column_stack([u1, e])
    b = int(4 * (T / 100) ** (2 / 9)) if bw is None else bw

    def gam(j):
        return xi[: T - j].T @ xi[j:] / T   # sum_t xi_t xi_{t+j}'
    Om = gam(0).copy()
    De = gam(0).copy()
    for j in range(1, b + 1):
        w = 1 - j / (b + 1)
        Gj = gam(j)
        Om += w * (Gj + Gj.T)
        De += w * Gj
    Oue, Oee = Om[0, 1:], Om[1:, 1:]
    Oinv = np.linalg.inv(Oee)
    Ouu_e = Om[0, 0] - Oue @ Oinv @ Oue
    yplus = y1 - e @ (Oinv @ Oue)
    Dplus = De[0, 1:] - Oue @ Oinv @ De[1:, 1:]
    A = np.r_[np.zeros(Z.shape[1]), Dplus]
    WtW = W1.T @ W1
    Dg = 1.0 / np.sqrt(np.diag(WtW))
    WtWi = (Dg[:, None] * np.linalg.inv(Dg[:, None] * WtW * Dg[None, :]) * Dg[None, :])   # inversa con columnas escaladas (mejor condicion)
    theta = WtWi @ (W1.T @ yplus - T * A)
    cov = Ouu_e * WtWi
    resid = y1 - W1 @ theta
    return theta, cov, resid, b, m


# ------------------------------------------------------------------ Gregory-Hansen (cambio de nivel, fecha desconocida)
def _adf_t(u, L):
    du = np.diff(u)
    n = len(du)
    rows = np.arange(L, n)
    cols = [u[rows]] + [du[rows - i] for i in range(1, L + 1)]
    Zm = np.column_stack(cols)
    yv = du[rows]
    beta, *_ = np.linalg.lstsq(Zm, yv, rcond=None)
    r = yv - Zm @ beta
    s2 = r @ r / (len(yv) - Zm.shape[1])
    cov = s2 * np.linalg.inv(Zm.T @ Zm)
    return beta[0] / np.sqrt(cov[0, 0])


def gh_stat(y, X, L=4, trim=0.15):
    T = len(y)
    best, tau_b = np.inf, None
    for tau in range(int(np.floor(trim * T)), int(np.ceil((1 - trim) * T))):
        D = (np.arange(T) >= tau).astype(float)
        Zm = np.column_stack([np.ones(T), D, X])
        u = y - Zm @ np.linalg.lstsq(Zm, y, rcond=None)[0]
        t = _adf_t(u, L)
        if t < best:
            best, tau_b = t, tau
    return best, tau_b


def gh_sim(T, m, nsim, seed, L=4):
    """Distribucion nula de GH (y y X paseos aleatorios independientes, innovaciones N(0,1))."""
    rng = np.random.default_rng(seed)
    out = np.empty(nsim)
    for s in range(nsim):
        W = np.cumsum(rng.standard_normal((T, m + 1)), axis=0)
        out[s] = gh_stat(W[:, 0], W[:, 1:], L)[0]
    return out


# ------------------------------------------------------------------ estimacion de un modelo
def estima(G, mk, xs, rupturas, i0, i1, nsim_gh=0, ardl=True):
    """DOLS, FMOLS y ARDL en la ventana comun. Devuelve dict de resultados por metodo."""
    yc = "y_" + mk
    idx = list(G.index)
    fj = fijas_de(xs, rupturas)
    W0, W1 = i0 + 2, i1 - K_DOLS            # ventana efectiva [W0, W1]
    desde = idx[W0]
    sub = G.iloc[: W1 + 1 + K_DOLS]           # historia previa para diferencias
    out = {"xs": xs, "fijas": fj, "ventana": (idx[W0], idx[W1])}
    # ---- DOLS
    dd = dols(sub.loc[:, [yc] + xs + fj], yc, xs, fijas=fj, k=K_DOLS, maxlags=HAC, desde=desde)
    res = dd["res"]
    nom = xs + fj
    ci = res.conf_int()
    out["dols"] = {"b": res.params[nom].values, "se": res.bse[nom].values, "p": res.pvalues[nom].values, "ci": ci.loc[nom].values,
                   "n": int(res.nobs), "r2": res.rsquared, "r2a": res.rsquared_adj, "aic": res.aic, "bic": res.bic, "ect": dd["ect"],
                   "const": dd["const"], "res": res}
    # ---- FMOLS en la ventana W0..W1
    S = G.iloc[W0: W1 + 1]
    Zd = np.column_stack([np.ones(len(S))] + [S[f].values for f in fj])
    th, cov, resid, b, m = fmols(S[yc].values, Zd, S[xs].values)
    nz = 1 + len(fj)
    se = np.sqrt(np.diag(cov))
    dfp = len(resid)
    pv = 2 * stats.norm.sf(np.abs(th / se))
    sel = list(range(nz, nz + len(xs))) + list(range(1, nz))
    out["fmols"] = {"b": th[sel], "se": se[sel], "p": pv[sel], "ci": np.column_stack([th[sel] - 1.96 * se[sel], th[sel] + 1.96 * se[sel]]),
                    "n": dfp, "bw": b, "resid": resid, "const": th[0],
                    "W": np.column_stack([Zd[1:], S[xs].values[1:]]), "theta": th}
    ssr = float(resid @ resid)
    yy = S[yc].values[1:]
    tss = float(((yy - yy.mean()) ** 2).sum())
    k_ = len(th)
    out["fmols"].update({"r2": 1 - ssr / tss, "r2a": 1 - (ssr / (dfp - k_)) / (tss / (dfp - 1)),
                         "aic": dfp * np.log(ssr / dfp) + 2 * k_, "bic": dfp * np.log(ssr / dfp) + k_ * np.log(dfp)})
    # ECT FMOLS sobre toda la muestra
    ect_f = G[yc] - th[0] - sum(G[f] * th[1 + j] for j, f in enumerate(fj)) - sum(G[x] * th[nz + j] for j, x in enumerate(xs))
    out["fmols"]["ect"] = ect_f
    # ---- ARDL / UECM (p=2, q=1 contemporaneo en dx) con fijas
    if ardl:
        out["ardl"] = ardl_uecm(G, yc, xs, fj, W0, W1)
    # ---- cointegracion Engle-Granger (MacKinnon) y Gregory-Hansen
    try:
        eg = coint(S[yc].values, S[xs].values, trend="c", maxlag=4, autolag="bic")
        out["eg_p"] = float(eg[1])
    except Exception:
        out["eg_p"] = np.nan
    if nsim_gh:
        stat, tau = gh_stat(S[yc].values, S[xs].values)
        out["gh"] = {"stat": stat, "fecha": idx[W0 + tau], "T": len(S), "m": len(xs)}
    return out


def ardl_uecm(G, yc, xs, fj, W0, W1):
    idx = list(G.index)
    Sx = G.iloc[W0 - 2: W1 + 1]
    y = Sx[yc]
    dy = y.diff()
    dX = Sx[xs].diff()
    D = pd.concat([pd.Series(1.0, index=Sx.index, name="const"), y.shift(1).rename("y_L1"), Sx[xs].shift(1).add_suffix("_L1"),
                   dy.shift(1).rename("dy_L1"), dX.add_suffix("_d0"), Sx[fj]], axis=1)
    Z = pd.concat([dy.rename("dy"), D], axis=1).iloc[2:].dropna()
    fit = sm.OLS(Z["dy"], Z.drop(columns="dy")).fit()
    names = list(Z.columns[1:])
    thy = fit.params["y_L1"]
    cov = fit.cov_params()
    res = {"lam": float(thy), "n": int(fit.nobs), "r2": fit.rsquared, "r2a": fit.rsquared_adj, "aic": fit.aic, "bic": fit.bic, "fit": fit,
           "Z": Z.drop(columns="dy"), "dy": Z["dy"]}
    b, se = [], []
    for v in xs + fj:
        key = (v + "_L1") if v in xs else v
        g = -fit.params[key] / thy
        grad = np.zeros(len(names))
        grad[names.index(key)] = -1 / thy
        grad[names.index("y_L1")] = fit.params[key] / thy ** 2
        b.append(g)
        se.append(float(np.sqrt(grad @ cov.values @ grad)))
    b, se = np.array(b), np.array(se)
    res.update({"b": b, "se": se, "p": 2 * stats.norm.sf(np.abs(b / se)), "ci": np.column_stack([b - 1.96 * se, b + 1.96 * se])})
    # bounds test (caso 3: constante libre, sin tendencia). F propio (los `fixed` de UECM.bounds_test no se incorporan al F: verificado);
    # valores criticos asintoticos de statsmodels (Pesaran-Shin-Smith / Kripfganz-Schneider) para k = len(xs) regresores I(1)
    R = np.zeros((1 + len(xs), len(names)))
    for k_, nme in enumerate(["y_L1"] + [x + "_L1" for x in xs]):
        R[k_, names.index(nme)] = 1
    F = float(fit.f_test(R).fvalue)
    try:
        from statsmodels.tsa.ardl import UECM
        m = UECM(Sx[yc], 2, Sx[xs], 1, trend="c")
        cvt = m.fit().bounds_test(case=3).critical_values
        pct = np.array(cvt.index, float)
        cu, cl = cvt["upper"].values, cvt["lower"].values
        if F >= cu[-1]:
            p_sup, nota = 0.001, "<0,001"
        elif F < cu[0]:
            p_sup, nota = 0.10, ">=0,10"
        else:
            p_sup = float(np.exp(np.interp(F, cu, np.log(1 - pct / 100)))), 
            p_sup, nota = p_sup[0], "interpolado"
        dec = "rechaza no-cointegracion (F > cota superior 5%)" if F > cvt.loc[95.0, "upper"] else ("no rechaza (F < cota inferior 5%)" if F < cvt.loc[95.0, "lower"] else "inconcluso (entre cotas 5%)")
        res.update({"F": F, "p_inf": np.nan, "p_sup": p_sup, "p_nota": nota, "decision": dec, "cv95": (float(cvt.loc[95.0, "lower"]), float(cvt.loc[95.0, "upper"]))})
    except Exception as e:  # noqa: BLE001
        res.update({"F": F, "p_inf": np.nan, "p_sup": np.nan, "p_nota": "", "decision": "", "cv95": (np.nan, np.nan), "error": type(e).__name__})
    return res


def ecm_lambda(G, yc, ect, xs):
    """Velocidad de ajuste: dy_t = c + lam ECT_{t-1} + dy_{t-1} + dy_{t-2} + dX_{t-1} (HAC)."""
    dy = G[yc].diff()
    Z = pd.concat([dy.rename("dy"), ect.shift(1).rename("ect"), dy.shift(1).rename("dy1"), dy.shift(2).rename("dy2"),
                   G[xs].diff().shift(1).add_suffix("_d1")], axis=1).dropna()
    r = sm.OLS(Z["dy"], sm.add_constant(Z.drop(columns="dy"))).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})
    return float(r.params["ect"]), float(r.pvalues["ect"])


# ------------------------------------------------------------------ fuera de muestra
def fuera_de_muestra(G, mk, xs, rupturas, K=5, embargo=4, comunes=()):
    yc = "y_" + mk
    fj = fijas_de(xs, rupturas)
    base = G[[yc] + xs + fj].copy()
    dy = base[yc].diff() * 100
    cols = {"dy": dy}
    for j in range(1, 5):
        cols[f"dy{j}"] = dy.shift(j)
    for x in xs:
        cols[f"{x}_d1"] = base[x].diff().shift(1) * 100
    Z = pd.concat([base, pd.DataFrame(cols)], axis=1)
    Z = pd.concat([Z, G[list(comunes)].add_prefix('_c_'), G[list(comunes)].diff().shift(1).add_prefix('_cd_')], axis=1) if comunes else Z
    Z = Z.loc[INICIO[mk]:].dropna()
    n = len(Z)
    cort = np.linspace(0, n, K + 1).astype(int)
    lagc = [f"dy{j}" for j in range(1, 5)] + [f"{x}_d1" for x in xs]
    err = {"AR4": np.full(n, np.nan), "SR (dy, dX rezagados)": np.full(n, np.nan), "ECM (SR + ECT)": np.full(n, np.nan)}
    yv = Z["dy"].values
    L = np.column_stack([np.ones(n)] + [Z[f"dy{j}"].values for j in range(1, 5)])
    SR = np.column_stack([np.ones(n), Z[lagc].values])
    LV = np.column_stack([np.ones(n), Z[xs].values] + ([Z[fj].values] if fj else []))
    for i in range(K):
        a, b = cort[i], cort[i + 1]
        te = np.arange(a, b)
        tr = np.array([t for t in range(n) if t < a - embargo or t >= b + embargo])
        for nom, M in (("AR4", L), ("SR (dy, dX rezagados)", SR)):
            be = np.linalg.lstsq(M[tr], yv[tr], rcond=None)[0]
            err[nom][te] = yv[te] - M[te] @ be
        yl = Z[yc].values
        bl = np.linalg.lstsq(LV[tr], yl[tr], rcond=None)[0]
        ect = yl - LV @ bl
        # ECT en t-1 (dentro de Z contiguo; el primer elemento del bloque usa el ultimo del bloque previo, que es dato observado)
        ect1 = np.r_[np.nan, ect[:-1]]
        M = np.column_stack([SR, ect1])
        ok = ~np.isnan(ect1)
        trk = np.array([t for t in tr if ok[t]])
        be = np.linalg.lstsq(M[trk], yv[trk], rcond=None)[0]
        tek = np.array([t for t in te if ok[t]])
        err["ECM (SR + ECT)"][tek] = yv[tek] - M[tek] @ be
    m = ~np.isnan(err["ECM (SR + ECT)"])
    out = {"n": int(m.sum()), "muestra": f"{Z.index[0]}..{Z.index[-1]}", "bloques": K, "embargo": embargo, "rmse": {}, "dm_vs_ar4": {}}
    for k in err:
        out["rmse"][k] = float(np.sqrt(np.mean(err[k][m] ** 2)))
    for k in ("SR (dy, dX rezagados)", "ECM (SR + ECT)"):
        r = dm_test(err[k][m], err["AR4"][m], h=1)
        out["dm_vs_ar4"][k] = {"DM_HLN": r["DM"], "p": r["p"], "mean_d": r["mean_d"]}
    return out


# ------------------------------------------------------------------ contribuciones de largo plazo
def periodo_cortes(idx_sample):
    out = {}
    for P, (a, b) in PERIODOS.items():
        pos = [i for i, q in enumerate(idx_sample) if a <= q <= b]
        if pos:
            out[P] = (pos[0], pos[-1])
    return out


def delta_periodo(serie: pd.Series, P):
    """Variacion acumulada en el periodo: valor del ultimo trimestre menos el del trimestre anterior al primero; si la serie
    empieza dentro del periodo (periodo parcial), desde su primer dato."""
    a, b = PERIODOS[P]
    s = serie.dropna()
    idx = list(s.index)
    ini = [i for i, q in enumerate(idx) if q >= a]
    fin = [i for i, q in enumerate(idx) if q <= b]
    if not ini or not fin or idx[ini[0]] > b:
        return np.nan
    i0, i1 = ini[0], fin[-1]
    if i1 < i0:
        return np.nan
    base = max(i0 - 1, 0)
    return float(s.iloc[i1] - s.iloc[base])


def serie_ajustada(G, v):
    s = G[v].copy()
    if v == "hogares":   # el salto de la EPA 2021T1 no es variacion real: se sustituye su diferencia por la media de las vecinas
        dxs = s.diff()
        j = list(s.index).index("2021Q1")
        dxs.iloc[j] = np.nanmean([dxs.iloc[j - 1], dxs.iloc[j + 1]])
        s = s.loc[s.first_valid_index()] + dxs.fillna(0).cumsum()
        s[G[v].isna()] = np.nan
    return s


def contribuciones(G, mk, xs, rupturas, est, metodo, B, rng):
    """beta x variacion acumulada por periodo; bandas: bootstrap por bloques (DOLS: re-estimacion OLS de la regresion; FMOLS: normal con su covarianza)."""
    yc = "y_" + mk
    fj = fijas_de(xs, rupturas)
    r = est[metodo]
    v0 = est["ventana"][0]
    dY = {P: delta_periodo(G[yc].loc[v0:], P) * 100 for P in PERIODOS}
    dX = {(v, P): delta_periodo(serie_ajustada(G, v).loc[v0:], P) * 100 for v in xs for P in PERIODOS}
    dF = {(v, P): delta_periodo(G[v].loc[v0:], P) * 100 for v in fj for P in PERIODOS}
    nb = len(xs) + len(fj)
    if metodo == "dols":
        res = r["res"]
        X = res.model.exog
        y = res.model.endog
        names = list(res.model.exog_names)
        pos = [names.index(v) for v in xs + fj]
        n = len(y)
        nbk = int(np.ceil(n / BLOQUE))
        bs = np.empty((B, nb))
        for i in range(B):
            st = rng.integers(0, n, nbk)
            ii = ((st[:, None] + np.arange(BLOQUE)[None, :]) % n).ravel()[:n]
            try:
                bb = np.linalg.lstsq(X[ii], y[ii], rcond=None)[0]
                bs[i] = bb[pos]
            except np.linalg.LinAlgError:
                bs[i] = np.nan
        bhat = r["b"]
        metodo_banda = "bootstrap por bloques (circular, bloque 8) de las filas de la regresion DOLS"
    else:
        cov = None
        th = r["theta"]
        # covarianza ordenada [x, fijas] a partir de los se (diagonal) aproximada: normal independiente
        bs = rng.normal(r["b"], r["se"], size=(B, nb))
        bhat = r["b"]
        metodo_banda = "normal con la covarianza FMOLS (diagonal; no es bootstrap)"
    filas = []
    for P in PERIODOS:
        if np.isnan(dY[P]):
            continue
        contrib = {}
        draws = {}
        fact_names = {}
        for j, v in enumerate(xs):
            f = FAMILIA[v]
            dx = dX[(v, P)]
            if dx != dx:
                continue
            contrib[f] = contrib.get(f, 0.0) + bhat[j] * dx
            draws[f] = draws.get(f, 0.0) + bs[:, j] * dx
        dfix = 0.0
        dfd = 0.0
        for j, v in enumerate(fj):
            dd = dF[(v, P)]
            if dd == dd:
                dfix += bhat[len(xs) + j] * dd
                dfd = dfd + bs[:, len(xs) + j] * dd
        suma = sum(contrib.values()) + dfix
        contrib["residuo"] = dY[P] - sum(v for k, v in contrib.items())
        draws["residuo"] = dY[P] - sum(draws[k] for k in list(draws))
        for f, c in contrib.items():
            dr = draws[f]
            q = np.nanquantile(dr, [0.05, 0.16, 0.84, 0.95])
            filas.append({"metodo": "contabilidad_lp", "mercado": mk, "ambito": "nacional", "periodo": P, "factor": f, "contribucion_pp": c,
                          "pct_total": 100 * c / dY[P] if abs(dY[P]) > 1e-9 else np.nan, "b68_lo": q[1], "b68_hi": q[2], "b90_lo": q[0], "b90_hi": q[3],
                          "capa": "C4", "notas": f"{metodo.upper()}; spec {'/'.join(xs)}; {'con' if rupturas else 'sin'} escalones; variacion observada del periodo {dY[P]:.2f} pp log x100; "
                                                 f"escalones de ruptura incluidos en residuo ({dfix:.2f}); bandas: {metodo_banda}; ASOCIACION de largo plazo, no causal"})
    return filas


# ------------------------------------------------------------------ contabilidad hogares-viviendas
def contabilidad_hogares(G, d, B, rng):
    h = serie_ajustada(G, "hogares")                 # ln hogares (miles), sin salto EPA 2021
    H = np.exp(h)
    dH = H.diff()                                    # miles de hogares por trimestre
    term = d["terminadas"] / 1000.0                  # miles de viviendas libres terminadas
    brecha_q = dH - term
    gap_pct = 100 * brecha_q / H.shift(1)           # % del stock de hogares
    gap4 = gap_pct.rolling(4).sum()
    G = G.loc["2002Q1":]
    p = G["y_compra"].diff() * 100
    a = G["y_alquiler"].diff() * 100
    filas, res_f = [], []
    out = []
    for P, (i, f) in PERIODOS.items():
        sl = (d.index >= i) & (d.index <= f)
        s = pd.DataFrame({"dH": dH[sl], "term": term[sl], "br": brecha_q[sl], "gp": gap_pct[sl]}).dropna()
        if len(s) < 4:
            out.append({"periodo": P, "n_trim": len(s), "nota": "sin cobertura de hogares (EPA desde 2002T1)"})
            continue
        dpp = delta_periodo(G["y_compra"], P)
        dpa = delta_periodo(G["y_alquiler"], P)
        out.append({"periodo": P, "n_trim": len(s), "hogares_nuevos_miles": s.dH.sum(), "viviendas_libres_terminadas_miles": s.term.sum(),
                    "brecha_miles": s.br.sum(), "brecha_pct_hogares": s.gp.sum(), "dln_precio_compra_x100": dpp * 100 if dpp == dpp else np.nan,
                    "dln_alquiler_x100": dpa * 100 if dpa == dpa else np.nan,
                    "nota": "viviendas LIBRES terminadas (faltan protegidas); hogares EPA con salto 2021T1 neutralizado; no se restan viviendas liberadas (v5.1)"})
    tab = pd.DataFrame(out)
    # asociacion: dy_q = b * gap4_{t-1} + e (sin constante: cada trimestre responde al desequilibrio anual acumulado), HAC
    ass = []
    for mk, ser in (("compra", p), ("alquiler", a)):
        D = pd.DataFrame({"dy": ser, "g": gap4.shift(1)}).dropna()
        D = D.loc["2003Q1":]
        for P in list(PERIODOS) + ["completo"]:
            Dp = D if P == "completo" else D[(D.index >= PERIODOS[P][0]) & (D.index <= PERIODOS[P][1])]
            if len(Dp) < 8:
                ass.append({"mercado": mk, "periodo": P, "n": len(Dp), "b": np.nan, "ee": np.nan, "p": np.nan, "contrib_pp": np.nan, "b68_lo": np.nan, "b68_hi": np.nan,
                            "b90_lo": np.nan, "b90_hi": np.nan, "nota": "n < 8"})
                continue
            r = sm.OLS(Dp["dy"], Dp[["g"]]).fit(cov_type="HAC", cov_kwds={"maxlags": HAC})
            bb = float(r.params["g"])
            n = len(Dp)
            nbk = int(np.ceil(n / BLOQUE))
            dr = np.empty(B)
            Xv, yv = Dp["g"].values, Dp["dy"].values
            for k in range(B):
                st = rng.integers(0, n, nbk)
                ii = ((st[:, None] + np.arange(BLOQUE)[None, :]) % n).ravel()[:n]
                den = Xv[ii] @ Xv[ii]
                dr[k] = (Xv[ii] @ yv[ii]) / den * Xv.sum() if den > 0 else np.nan
            q = np.nanquantile(dr, [0.05, 0.16, 0.84, 0.95])
            ass.append({"mercado": mk, "periodo": P, "n": n, "b": bb, "ee": float(r.bse["g"]), "p": float(r.pvalues["g"]), "contrib_pp": bb * Xv.sum(),
                        "b68_lo": q[1], "b68_hi": q[2], "b90_lo": q[0], "b90_hi": q[3],
                        "nota": "dy_q = b gap4_{t-1}; contrib = b * suma de gap4 rezagado en el periodo" + ("; n<12: inferencia HAC no fiable" if n < 12 else "")})
    asc = pd.DataFrame(ass)
    for r in asc[asc.periodo != "completo"].itertuples():
        if r.b == r.b:
            filas.append({"metodo": "contabilidad", "mercado": r.mercado, "ambito": "nacional", "periodo": r.periodo, "factor": "demografia",
                          "contribucion_pp": r.contrib_pp, "pct_total": np.nan, "b68_lo": r.b68_lo, "b68_hi": r.b68_hi, "b90_lo": r.b90_lo, "b90_hi": r.b90_hi,
                          "capa": "C4", "notas": f"brecha hogares nuevos - viviendas libres terminadas (demografia menos oferta, no separables); asociacion b={r.b:.3f} (p={r.p:.2f}, n={r.n}); "
                                                  "bandas: bootstrap por bloques; no causal"})
    return tab, asc, filas


# ------------------------------------------------------------------ principal
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M4"))
    a = ap.parse_args(argv)
    t0 = time.time()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    NSIM, B = (30, 99) if a.rapido else (500, 999)
    d = pd.read_csv(DATOS).set_index("trimestre")
    G = preparar(d)
    REG = Registry(out / "registro.csv")
    rng = np.random.default_rng(SEED)
    filas, coint_f, oos_f, attr, raices, discrep = [], [], [], [], [], []
    ests = {}
    # ---- raices unitarias
    for v in ["y_compra", "y_alquiler", "renta", "tipo", "pob", "hogares", "credito", "oferta"]:
        s = G[v].dropna()
        for orden, x in (("nivel", s), ("dif1", s.diff().dropna())):
            try:
                st = adfuller(x.values, regression="c", autolag="BIC")
                raices.append({"variable": v, "orden": orden, "n": len(x), "adf_stat": st[0], "p": st[1], "rezagos": st[2], "nota": "ADF con constante, BIC"})
            except Exception:
                pass
    pd.DataFrame(raices).to_csv(out / "raices_unitarias.csv", index=False)
    for mk, specs in SPECS.items():
        i0, i1 = ventana(G, mk)
        gh_cache = {}
        for sn, xs in specs.items():
            for rup in (False, True):
                tag = "con_rupturas" if rup else "sin_rupturas"
                ests[(mk, sn, tag)] = estima(G, mk, xs, rup, i0, i1, nsim_gh=NSIM if not rup else 0, ardl=True)
            est0 = ests[(mk, sn, "sin_rupturas")]
            ini, fin = est0["ventana"]
            g = est0["gh"]
            key = (g["T"], g["m"])
            if key not in gh_cache:
                gh_cache[key] = gh_sim(g["T"], g["m"], NSIM, SEED + g["m"])
            sim = gh_cache[key]
            gh_p = float((1 + np.sum(sim <= g["stat"])) / (1 + len(sim)))
            cv = np.quantile(sim, [0.01, 0.05, 0.10])
            coint_f.append({"mercado": mk, "spec": sn, "variables": "+".join(xs), "ventana": f"{ini}..{fin}", "n": len(G.loc[ini:fin]),
                            "EG_p_mackinnon": est0["eg_p"], "GH_stat": g["stat"], "GH_fecha": g["fecha"], "GH_p_sim": gh_p, "GH_cv1": cv[0], "GH_cv5": cv[1], "GH_cv10": cv[2],
                            "ARDL_F_sin_rupturas": est0["ardl"]["F"], "ARDL_p_sup_sin": est0["ardl"]["p_sup"], "ARDL_decision_5pct_sin": est0["ardl"]["decision"], "ARDL_cv95_sup": est0["ardl"]["cv95"][1], "ARDL_t_yL1_sin": float(est0["ardl"]["fit"].tvalues["y_L1"]),
                            "ARDL_F_con_rupturas": ests[(mk, sn, "con_rupturas")]["ardl"]["F"], "ARDL_p_sup_con": ests[(mk, sn, "con_rupturas")]["ardl"]["p_sup"], "ARDL_decision_5pct_con": ests[(mk, sn, "con_rupturas")]["ardl"]["decision"],
                            "nota": "ARDL: F propio con VC asintoticos de statsmodels (con escalones, aproximados); casos degenerados posibles: revisar t de y_L1 (debe ser negativo y significativo); p aproximado por interpolacion de la tabla de VC (acotado a [0,001; 0,10]); GH: cambio de nivel, retardos ADF fijos 4, VC simulados bajo la nula (paseos independientes, nsim=%d); EG: sin rupturas" % len(sim)})
            for rup in (False, True):
                tag = "con_rupturas" if rup else "sin_rupturas"
                est = ests[(mk, sn, tag)]
                ini, fin = est["ventana"]
                nom = xs + est["fijas"]
                for met in ("dols", "fmols", "ardl"):
                    r = est[met]
                    nm = len(nom)
                    if met == "dols":
                        lam, plam = ecm_lambda(G, "y_" + mk, r["ect"], xs)
                        dg = diag_de(r["res"].model.endog, r["res"].model.exog)
                        coint_p = est["eg_p"]
                    elif met == "fmols":
                        lam, plam = ecm_lambda(G, "y_" + mk, r["ect"], xs)
                        dg = diag_de(r["resid"], r["W"])
                        coint_p = est["eg_p"]
                    else:
                        lam, plam = r["lam"], float(r["fit"].pvalues["y_L1"])
                        dg = diag_de(r["dy"].values, r["Z"].values)
                        coint_p = r["p_sup"]
                    vif = vif_max(G.loc[ini:fin, xs].values)
                    mid = f"M4_{mk}_{sn}_{tag}_{met}"
                    rm = r.get("n", np.nan)
                    for j, v in enumerate(nom):
                        fam = FAMILIA.get(v, "residuo")
                        sd_y = G.loc[ini:fin, "y_" + mk].std()
                        sd_x = G.loc[ini:fin, v].std()
                        filas.append({
                            "modelo_id": mid, "modulo": "M4", "familia_modelo": {"dols": "dols", "fmols": "fmols", "ardl": "ardl_bounds_uecm"}[met], "mercado": mk,
                            "ambito": "nacional", "periodo": "completo", "dependiente": Y_COL[mk], "transformacion": "ln niveles; tipo en pp",
                            "medida_precio": MEDIDA[mk], "variable": v if v in xs else f"ruptura:{v}", "beta": r["b"][j], "ee": r["se"][j],
                            "tipo_ee": {"dols": f"HAC-NW({HAC})", "fmols": "FMOLS Omega_u.e (Bartlett)", "ardl": "delta (OLS clasico)"}[met],
                            "t": r["b"][j] / r["se"][j], "p": r["p"][j], "ic95_lo": r["ci"][j, 0], "ic95_hi": r["ci"][j, 1],
                            "beta_std": r["b"][j] * sd_x / sd_y if sd_y > 0 else np.nan, "elasticidad": r["b"][j] if (v in xs and v != "tipo") else np.nan,
                            "n": rm, "r2": r["r2"], "r2_adj": r["r2a"], "aic": r["aic"], "bic": r["bic"], "vel_ajuste": lam, "semivida": semivida(lam),
                            "coint_p": coint_p, "bg_p": dg["bg_p"], "bp_p": dg["bp_p"], "jb_p": dg["jb_p"], "reset_p": dg["reset_p"],
                            "cusum_estable": dg["cusum_estable"], "vif_max": vif, "capa": "C4", "script": SCRIPT, "familia_factor": fam,
                            "ventana": f"{ini}..{fin}", "spec": sn, "rupturas": tag, "metodo_lp": met})
                    REG.log("M4", mid, f"{Y_COL[mk]} ~ {'+'.join(nom)} [{met}]", ini, fin, rm, r["r2a"], r["aic"], r["bic"], np.nan, r["b"][0], r["p"][0],
                            f"lam={lam:.3f}; coint_p={coint_p:.3f}" if coint_p == coint_p else f"lam={lam:.3f}")
            # --- discrepancia DOLS vs FMOLS (por especificacion y variante)
            for tag in ("sin_rupturas", "con_rupturas"):
                e = ests[(mk, sn, tag)]
                for j, v in enumerate(e["xs"]):
                    bd, bf, sd, sf = e["dols"]["b"][j], e["fmols"]["b"][j], e["dols"]["se"][j], e["fmols"]["se"][j]
                    z = (bd - bf) / np.sqrt(sd ** 2 + sf ** 2)
                    discrep.append({"mercado": mk, "spec": sn, "rupturas": tag, "variable": v, "beta_dols": bd, "beta_fmols": bf, "beta_ardl": e["ardl"]["b"][j],
                                    "signo_difiere_dols_fmols": bool(np.sign(bd) != np.sign(bf)), "z_diferencia": z, "discrepan": bool(np.sign(bd) != np.sign(bf) or abs(z) > 1.96),
                                    "nota": "si discrepan se reportan ambos (no se elige)"})
    # ---- fuera de muestra (todas las especificaciones, sin y con rupturas)
    for mk, specs in SPECS.items():
        for sn, xs in specs.items():
            for rup in (False,):   # con escalones no es identificable por bloques (un escalon cae entero en un bloque): se omite, ver notas
                o = fuera_de_muestra(G, mk, xs, rup, comunes=SPECS[mk][COMPLETA[mk]])
                oos_f.append({"mercado": mk, "spec": sn, "rupturas": "con_rupturas" if rup else "sin_rupturas", "n": o["n"], "muestra": o["muestra"],
                              **{f"rmse_{k}": v for k, v in o["rmse"].items()},
                              **{f"dm_p_{k}": v["p"] for k, v in o["dm_vs_ar4"].items()}, **{f"dm_{k}": v["DM_HLN"] for k, v in o["dm_vs_ar4"].items()}})
                REG.log("M4_oos", f"M4_oos_{mk}_{sn}_{'rup' if rup else 'sin'}", "ECM (SR+ECT) vs AR4", o["muestra"].split("..")[0], o["muestra"].split("..")[1], o["n"],
                        np.nan, np.nan, np.nan, o["rmse"]["ECM (SR + ECT)"], np.nan, o["dm_vs_ar4"]["ECM (SR + ECT)"]["p"],
                        f"AR4 rmse={o['rmse']['AR4']:.3f}; bloques=5 embargo=4")
    oos = pd.DataFrame(oos_f)
    oos.to_csv(out / "fuera_muestra.csv", index=False)
    # ---- contribuciones (cabecera de cada mercado; DOLS y FMOLS; sin y con escalones)
    for mk, sn in COMPLETA.items():
        xs = SPECS[mk][sn]
        for tag, rup in (("sin_rupturas", False), ("con_rupturas", True)):
            e = ests[(mk, sn, tag)]
            for met in ("dols", "fmols"):
                attr += contribuciones(G, mk, xs, rup, e, met, B, rng)
    tab_h, ass_h, filas_h = contabilidad_hogares(G, d, B, rng)
    tab_h.to_csv(out / "contabilidad_hogares_viviendas.csv", index=False)
    ass_h.to_csv(out / "contabilidad_hogares_asociacion.csv", index=False)
    attr += filas_h
    at = pd.DataFrame(attr)
    at = at[["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "notas"]]
    at.to_csv(out / "atribucion.csv", index=False)
    # ---- coeficientes
    coef = pd.DataFrame(filas)
    from scipy.stats import false_discovery_control
    lr = coef["variable"].str.startswith("ruptura:") == False  # noqa: E712
    coef["p_ajustado"] = np.nan
    coef.loc[lr, "p_ajustado"] = false_discovery_control(coef.loc[lr, "p"].fillna(1).values, method="bh")
    coef["metodo_ajuste"] = np.where(lr, "BH", "")
    ORD = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio", "variable", "beta", "ee", "tipo_ee",
           "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad", "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida",
           "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo",
           "pct_sig_bh", "cumple_regla_m0", "cumple_multiverso", "destacado", "motivo_destacado", "script"]
    EXTRA = ["familia_factor", "ventana", "spec", "rupturas", "metodo_lp"]
    for c in ORD:
        if c not in coef:
            coef[c] = np.nan
    coef[ORD + EXTRA].to_csv(out / "coeficientes.csv", index=False)
    cdf = pd.DataFrame(coint_f)
    cdf.to_csv(out / "cointegracion.csv", index=False)
    pd.DataFrame(discrep).to_csv(out / "discrepancias_dols_fmols.csv", index=False)
    REG.flush()

    # ---- resultado.json
    cab = {}
    for mk, sn in COMPLETA.items():
        o = oos[(oos.mercado == mk) & (oos.spec == sn) & (oos.rupturas == "sin_rupturas")].iloc[0]
        cab[mk] = {"spec": sn, "n": int(o.n), "muestra": o.muestra, "rmse": {"AR4": o["rmse_AR4"], "SR": o["rmse_SR (dy, dX rezagados)"], "ECM": o["rmse_ECM (SR + ECT)"]},
                   "dm_vs_ar4": {"SR": {"DM_HLN": o["dm_SR (dy, dX rezagados)"], "p": o["dm_p_SR (dy, dX rezagados)"]}, "ECM": {"DM_HLN": o["dm_ECM (SR + ECT)"], "p": o["dm_p_ECM (SR + ECT)"]}}}
    est_c = {}
    for mk, sn in COMPLETA.items():
        for tag in ("sin_rupturas", "con_rupturas"):
            c_ = coef[(coef.mercado == mk) & (coef.spec == sn) & (coef.rupturas == tag) & (~coef.variable.str.startswith("ruptura:"))]
            est_c[f"{mk}|{sn}|{tag}"] = c_[["metodo_lp", "variable", "beta", "ic95_lo", "ic95_hi", "p_ajustado", "vel_ajuste", "semivida", "coint_p"]].round(4).to_dict("records")
    ndisc = int(pd.DataFrame(discrep).discrepan.sum())
    res = {
        "rama": "v8/M4", "pregunta": "¿Existe una relación de largo plazo (cointegración) del precio real de compra (desde 1997T3) y del alquiler real (desde 2002T1) con renta, tipo hipotecario real, población u hogares, crédito y oferta?",
        "capa": "C4", "datos": "data/processed/v8/nacional_q_v8.csv", "N": {mk: int(len(G.loc[ests[(mk, COMPLETA[mk], 'sin_rupturas')]['ventana'][0]: ests[(mk, COMPLETA[mk], 'sin_rupturas')]['ventana'][1]])) for mk in SPECS},
        "metodo": "DOLS (k=1), FMOLS (Bartlett) y ARDL-bounds (UECM p=2,q=1, caso 3); rupturas: sin / escalones P2-P5 + COVID (+EPA2021) y Gregory-Hansen (VC simulados); BH q=0,10",
        "estimacion": est_c, "ic95": "ver coeficientes.csv", "p_ajustado": "BH q=0,10 sobre coeficientes de largo plazo (sin escalones)",
        "nivel_evidencia": "EXPLORATORIO / ASOCIACION de largo plazo (C4). Sin lenguaje causal.",
        "diagnosticos": {"cointegracion": cdf[["mercado", "spec", "EG_p_mackinnon", "GH_stat", "GH_fecha", "GH_p_sim", "ARDL_F_sin_rupturas", "ARDL_p_sup_sin"]].round(4).to_dict("records"),
                         "n_discrepancias_dols_fmols": ndisc, "nota": "Con raíces cercanas a la unidad y T≈100, los contrastes tienen poca potencia; un no rechazo no prueba ausencia de cointegración. 'tipo' puede ser I(0)/I(1) ambiguo: ver raices_unitarias.csv."},
        "fuera_muestra": {"modelo": "ECM de largo plazo (beta OLS estatico por pliegue + corrección de error) frente a AR(4) sobre dy trimestral x100, bloques con embargo (5 bloques, embargo 4)",
                          "rmse": {mk: cab[mk]["rmse"] for mk in cab}, "dm_vs_ar4": {mk: cab[mk]["dm_vs_ar4"] for mk in cab},
                          "detalle": {mk: {"spec": cab[mk]["spec"], "n": cab[mk]["n"], "muestra": cab[mk]["muestra"]} for mk in cab},
                          "ecm_v1": "no evaluable en la misma muestra (el ECM v1 usa IPV desde 2007 y permisos); este ECM es el comparador de largo plazo de V8"},
        "notas": "Especificación de cabecera fijada a priori: compra C4 y alquiler A4 (sin rupturas). Oferta = ln de terminadas acumuladas desde 1995 (proxy de stock; libres; 1995-2007 anual/4, marcada). Población interpolada (marcada). "
                 "Contribuciones de largo plazo en atribucion.csv (contabilidad_lp) y brecha hogares-viviendas (contabilidad): C4, asociación. Bandas FMOLS: normal diagonal (no bootstrap).",
        "segundos": round(time.time() - t0, 1), "rapido": bool(a.rapido),
    }
    (out / "resultado.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))
    # ---- resumen
    cc = cdf[["mercado", "spec", "EG_p_mackinnon", "GH_p_sim", "GH_fecha", "ARDL_F_sin_rupturas", "ARDL_p_sup_sin"]]
    cl = coef[(coef.spec.isin(list(COMPLETA.values()))) & (coef.rupturas == "sin_rupturas") & (~coef.variable.str.startswith("ruptura:"))][["mercado", "metodo_lp", "variable", "beta", "ic95_lo", "ic95_hi", "p_ajustado", "vel_ajuste", "semivida"]]
    md = [f"# M4 largo plazo (C4, asociación; {'RÁPIDO' if a.rapido else 'completo'})", "",
          "## Cointegración por especificación", "", md_tabla(cc), "",
          "## Coeficientes de largo plazo de la especificación de cabecera (sin rupturas)", "", md_tabla(cl), "",
          f"Discrepancias DOLS/FMOLS (signo o |z|>1,96): {ndisc} de {len(discrep)}; se reportan ambos (discrepancias_dols_fmols.csv).", "",
          "## Fuera de muestra (RMSE de dy x100; bloques con embargo; misma muestra)", "", "```", json.dumps({mk: cab[mk]["rmse"] for mk in cab}, indent=1), "```",
          "", "Límites: asociación de largo plazo (no causal); potencia baja de los contrastes de cointegración; FMOLS con bandas normales; oferta y población son proxies marcadas; ECM v1 no replicable en la misma muestra."]
    (out / "resumen.md").write_text("\n".join(md))
    print(f"M4 ok en {time.time() - t0:.0f}s")
    return res


if __name__ == "__main__":
    main()
