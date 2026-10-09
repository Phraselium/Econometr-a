"""F5 (panel CCAA, P4): FE bidireccional, tendencias, CCE (Pesaran 2006), CD, CIPS, poolability,
heterogeneidad. Determinista (semilla 20261009), sin red. Lee solo data/processed.
Escribe en output/f5/ y output/registro_busqueda_f5.csv.
"""
import sys
import time
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera

sys.path.insert(0, str(Path(__file__).resolve().parent))
from econ_utils import ROOT, SEED, Registry, df_md, holm  # noqa: E402

warnings.filterwarnings("ignore")
T0 = time.time()
OUT = ROOT / "output" / "f5"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(ROOT / "output" / "registro_busqueda_f5.csv", reset=True)
RNG = np.random.default_rng(SEED)
NBOOT = 9999
MD = []
BETA2_P = {}      # p-valores de beta2 por modelo (para Holm/Bonferroni)

XN = ["d_ln_ocup", "d_share_extr", "d_ln_pob_esp", "term_l1"]
LAB = {"d_ln_ocup": "b1 dln ocupados", "d_share_extr": "b2 d(extr/total, pp)",
       "d_ln_pob_esp": "b3 dln pob espanola", "term_l1": "b4 terminadas/1000 hab (t-1)"}
REGIONES = {"Comunitat Valenciana": "C. Valenciana", "Comunidad de Madrid": "Madrid", "Cataluña": "Cataluna",
            "Illes Balears": "Baleares", "Canarias": "Canarias", "Andalucía": "Andalucia"}


def save(df, name, fmt=".4g", index=True):
    df.to_csv(OUT / f"{name}.csv", index=index)
    (OUT / f"{name}.md").write_text(df_md(df, fmt, index) + "\n")


def sec(t, txt=""):
    MD.append(f"\n## {t}\n\n{txt}\n")


def tm(df, fmt=".4g", index=True):
    return df_md(df, fmt, index) + "\n"


# ================================================================ datos
def prep_annual():
    a = pd.read_csv(ROOT / "data/processed/panel_ccaa_a.csv").sort_values(["ccaa", "anio"]).reset_index(drop=True)
    g = a.groupby("ccaa")
    a["share_extr"] = 100 * a.pob_extranj / a.pob_total
    a["d_share_extr"] = g.share_extr.diff()
    a["d_ln_ocup"] = a.d_ln_ocupados
    a["d_ln_pob_esp"] = a.d_ln_pob_espanola
    a["term_pc"] = 1000 * a.terminadas / a.pob_total
    a["term_l1"] = a.groupby("ccaa").term_pc.shift(1)
    a["share_mid"] = (a.share_extr + a.groupby("ccaa").share_extr.shift(-1)) / 2   # cuota a mitad de anio t
    a["d_share_mid"] = a.groupby("ccaa").share_mid.diff()
    a["d_share_flow_t"] = a.groupby("ccaa").d_share_extr.shift(-1)                  # flujo durante el anio t
    a["y"] = a.d_ln_ipv
    a["y_pt"] = a.d_ln_p_tasado
    return a


A = prep_annual()
MAIN = A[(A.anio >= 2009) & (A.anio <= 2025)].dropna(subset=["y"] + XN).copy()
CCAAS = sorted(MAIN.ccaa.unique())
assert MAIN.groupby("ccaa").size().nunique() == 1, "panel principal no balanceado"
N_MAIN, T_MAIN = len(CCAAS), MAIN.anio.nunique()


# ================================================================ núcleo numérico FE
def arr(df, ycol, xcols, ccaas=None):
    ccaas = ccaas or sorted(df.ccaa.unique())
    d = df.set_index(["ccaa", "anio"]).sort_index()
    yrs = sorted(df.anio.unique())
    Y = np.stack([d.loc[c, ycol].reindex(yrs).values for c in ccaas])
    X = np.stack([np.stack([d.loc[c, x].reindex(yrs).values for x in xcols], -1) for c in ccaas])
    return Y, X


def dd(Z):
    """doble demeaning sobre ejes (0, 1) de un array (N,T,...)"""
    return Z - Z.mean(0, keepdims=True) - Z.mean(1, keepdims=True) + Z.mean((0, 1), keepdims=True)


def crve_t(Xd, yd, j):
    """beta, EE y t cluster (por unidad) para datos ya demeaned: Xd (N,T,k), yd (N,T)."""
    N = Xd.shape[0]
    XtX = np.einsum("ntk,ntl->kl", Xd, Xd)
    b = np.linalg.solve(XtX, np.einsum("ntk,nt->k", Xd, yd))
    e = yd - Xd @ b
    s = np.einsum("ntk,nt->nk", Xd, e)
    Ai = np.linalg.inv(XtX)
    V = Ai @ (s.T @ s) @ Ai * N / (N - 1)
    return b, np.sqrt(np.diag(V)), b[j] / np.sqrt(V[j, j])


WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(.5), np.sqrt(.5), 1, np.sqrt(1.5)])


def wild_boot(Y, X, j, B=NBOOT, batch=1000):
    """Wild cluster bootstrap restringido (Webb) para H0: beta_j = 0; panel balanceado, FE bidireccionales."""
    N, T, k = X.shape
    Xd, yd = dd(X), dd(Y)
    _, _, t0 = crve_t(Xd, yd, j)
    keep = [i for i in range(k) if i != j]
    Xr = Xd[:, :, keep]
    br = np.linalg.solve(np.einsum("ntk,ntl->kl", Xr, Xr), np.einsum("ntk,nt->k", Xr, yd))
    fit = Xr @ br
    u = yd - fit
    XtXi = np.linalg.inv(np.einsum("ntk,ntl->kl", Xd, Xd))
    aj = XtXi[j]
    cnt, tot = 0, 0
    while tot < B:
        m = min(batch, B - tot)
        w = RNG.choice(WEBB, size=(m, N))
        ys = fit[None] + w[:, :, None] * u[None]
        ys = ys - ys.mean(1, keepdims=True) - ys.mean(2, keepdims=True) + ys.mean((1, 2), keepdims=True)
        bs = np.einsum("kl,ntl,mnt->mk", XtXi, Xd, ys)
        e = ys - np.einsum("ntk,mk->mnt", Xd, bs)
        s = np.einsum("ntk,mnt->mnk", Xd, e)
        sj = s @ aj
        vj = (sj ** 2).sum(1) * N / (N - 1)
        ts = bs[:, j] / np.sqrt(vj)
        cnt += (np.abs(ts) >= abs(t0) - 1e-12).sum()
        tot += m
    return (cnt + 1) / (B + 1)


# ================================================================ FE linearmodels
def fe_fit(df, ycol, xcols, trends=False, cov="clustered", bw=None):
    d = df.set_index(["ccaa", "anio"]).sort_index()
    X = d[xcols].copy()
    if trends:
        ccs = sorted(df.ccaa.unique())
        yrs = d.index.get_level_values("anio").values
        tt = yrs - yrs.mean()
        for c in ccs[1:]:
            X[f"tr_{c[:8]}"] = tt * (d.index.get_level_values("ccaa") == c)
    mod = PanelOLS(d[ycol], X, entity_effects=True, time_effects=True, drop_absorbed=True)
    if cov == "clustered":
        return mod.fit(cov_type="clustered", cluster_entity=True)
    if cov == "kernel":
        return mod.fit(cov_type="kernel", kernel="bartlett", bandwidth=bw)
    return mod.fit()


def stats_fe(r):
    n = int(r.nobs)
    rss = float((r.resids ** 2).sum())
    kk = n - r.df_resid
    r2a = 1 - (1 - r.rsquared) * (n - 1) / r.df_resid
    return n, r2a, n * np.log(rss / n) + 2 * kk, n * np.log(rss / n) + np.log(n) * kk


def log_fe(mid, formula, r, interest, ini, fin, note=""):
    n, r2a, aic, bic = stats_fe(r)
    ci, pi = (r.params.get(interest, np.nan), r.pvalues.get(interest, np.nan)) if interest else (np.nan, np.nan)
    REG.log("F5", mid, formula, ini, fin, n, r2a, aic, bic, np.nan, ci, pi,
            note + " | rmse_oos no aplica (efectos de anio no predecibles fuera de muestra); R2aj = R2 within ajustado")
    if interest == "d_share_extr":
        BETA2_P[mid] = pi


# ================================================================ CCE
def cce(Y, X):
    """CCE-MG y CCE-P (Pesaran 2006). Y (N,T), X (N,T,k)."""
    N, T, k = X.shape
    yb, xb = Y.mean(0), X.mean(0)
    Zc = np.column_stack([np.ones(T), yb, xb])
    dfres = T - (k + Zc.shape[1])
    bi, se_i, res_mg, Mi, XMX, XMy = [], [], [], [], [], []
    M = np.eye(T) - Zc @ np.linalg.pinv(Zc)
    for i in range(N):
        Wm = np.column_stack([X[i], Zc])
        coef, *_ = np.linalg.lstsq(Wm, Y[i], rcond=None)
        e = Y[i] - Wm @ coef
        C = (e @ e / dfres) * np.linalg.pinv(Wm.T @ Wm)
        bi.append(coef[:k])
        se_i.append(np.sqrt(np.diag(C))[:k])
        res_mg.append(e)
        XMX.append(X[i].T @ M @ X[i] / T)
        XMy.append(X[i].T @ M @ Y[i] / T)
    bi = np.array(bi)
    b_mg = bi.mean(0)
    V_mg = (bi - b_mg).T @ (bi - b_mg) / (N * (N - 1))
    Psi = np.mean(XMX, 0)
    b_p = np.linalg.solve(Psi, np.mean(XMy, 0))
    R = sum(XMX[i] @ np.outer(bi[i] - b_mg, bi[i] - b_mg) @ XMX[i] for i in range(N)) / (N - 1)
    Pi = np.linalg.inv(Psi)
    V_p = Pi @ R @ Pi / N
    res_p = np.array([M @ (Y[i] - X[i] @ b_p) for i in range(N)])
    return dict(b_mg=b_mg, se_mg=np.sqrt(np.diag(V_mg)), b_p=b_p, se_p=np.sqrt(np.diag(V_p)), bi=bi,
                se_i=np.array(se_i), res_mg=np.array(res_mg), res_p=res_p, dfres=dfres)


def cce_table(c, names):
    rows = []
    for lab, b, s in (("CCE-MG", c["b_mg"], c["se_mg"]), ("CCE-P", c["b_p"], c["se_p"])):
        for j, n in enumerate(names):
            t = b[j] / s[j]
            rows.append((lab, n, b[j], s[j], t, 2 * stats.norm.sf(abs(t))))
    return pd.DataFrame(rows, columns=["estimador", "var", "coef", "EE", "z", "p"])


# ================================================================ CD de Pesaran
def cd_test(E):
    """E: DataFrame T x N. CD = sqrt(2/(N(N-1))) sum_{i<j} sqrt(T_ij) rho_ij."""
    N = E.shape[1]
    s, rhos = 0.0, []
    for a in range(N):
        for b in range(a + 1, N):
            m = E.iloc[:, [a, b]].dropna()
            if len(m) < 3:
                continue
            rho = np.corrcoef(m.iloc[:, 0], m.iloc[:, 1])[0, 1]
            s += np.sqrt(len(m)) * rho
            rhos.append(rho)
    cd = np.sqrt(2.0 / (N * (N - 1))) * s
    return dict(CD=cd, p=2 * stats.norm.sf(abs(cd)), rho_medio=np.mean(rhos), abs_rho_medio=np.mean(np.abs(rhos)))


def resid_wide(r):
    return r.resids.unstack(level=0)


# ================================================================ CIPS
def cadf_t(y, p):
    N, T = y.shape
    yb = y.mean(0)
    dy = np.diff(y, axis=1)
    dyb = np.diff(yb)
    ts = []
    rows = np.arange(p + 1, T)
    for i in range(N):
        cols = [np.ones(len(rows)), y[i, rows - 1], yb[rows - 1], dyb[rows - 1]]
        for j in range(1, p + 1):
            cols += [dy[i, rows - 1 - j], dyb[rows - 1 - j]]
        W = np.column_stack(cols)
        yy = dy[i, rows - 1]
        coef, *_ = np.linalg.lstsq(W, yy, rcond=None)
        e = yy - W @ coef
        s2 = e @ e / (len(yy) - W.shape[1])
        ts.append(coef[1] / np.sqrt(s2 * np.linalg.inv(W.T @ W)[1, 1]))
    return np.array(ts)


def cips(y, p):
    return np.clip(cadf_t(y, p), -6.19, 2.61).mean()


_SIM = {}


def cips_sim(N, T, p, R=1000):
    key = (N, T, p)
    if key not in _SIM:
        rng = np.random.default_rng(SEED + 7 * N + T + 100 * p)
        out = []
        for _ in range(R):
            f = rng.standard_normal(T)
            lam = rng.uniform(0, 1, N)
            e = lam[:, None] * f[None] + rng.standard_normal((N, T))
            out.append(cips(np.cumsum(e, 1), p))
        _SIM[key] = np.sort(out)
    return _SIM[key]


# ================================================================ 1. Principal
sec("0. Datos y muestra",
    f"Panel anual `panel_ccaa_a`: dependiente d_ln_ipv (IPV media anual, base 2025). Muestra principal "
    f"{N_MAIN} CCAA x {T_MAIN} anios (2009-2025; N={len(MAIN)}, balanceado; `terminadas` de Extremadura ya incorporada en data/processed). "
    f"**Timing de b2**: la poblacion es el stock a 1 de enero del anio t, de modo que d_share_t = cuota(1-1-t) - cuota(1-1-(t-1)) mide la "
    f"entrada neta ocurrida durante el anio t-1, mientras el IPV es la media del anio t (b2 principal = flujo retardado un anio). "
    f"Alternativas registradas (seccion 1g): cuota a mitad de anio t (media de 1-1-t y 1-1-t+1) y flujo del anio t (cuota(1-1-t+1) - cuota(1-1-t)); "
    f"ambas necesitan la cuota de 1-1-2026, por lo que se comparan en 2009-2024. b2 se mide en puntos porcentuales de cuota "
    f"(pob_extranj/pob_total); el coeficiente es Delta ln IPV por pp (x100 = %/pp). `term_l1` = terminadas por 1.000 hab. de t-1.")

r_cl = fe_fit(MAIN, "y", XN)
r_dk = fe_fit(MAIN, "y", XN, cov="kernel", bw=2)
r_dk3 = fe_fit(MAIN, "y", XN, cov="kernel", bw=3)
Yn, Xn = arr(MAIN, "y", XN, CCAAS)
b_np = crve_t(dd(Xn), dd(Yn), 1)[0]
assert np.allclose(b_np, r_cl.params[XN].values, atol=1e-8), "FE numpy != linearmodels"
ini, fin = int(MAIN.anio.min()), int(MAIN.anio.max())
fm = "d_ln_ipv ~ " + " + ".join(XN) + " | CCAA + anio"
log_fe("A_FE_cl", fm + " [cluster CCAA]", r_cl, "d_share_extr", ini, fin, "principal")
log_fe("A_FE_dk", fm + " [Driscoll-Kraay bw=2]", r_dk, "d_share_extr", ini, fin, "robustez EE")
log_fe("A_FE_dk3", fm + " [Driscoll-Kraay bw=3]", r_dk3, "d_share_extr", ini, fin, "robustez EE")
pw = {j: wild_boot(Yn, Xn, j) for j in range(4)}
BETA2_P["A_FE_wild"] = pw[1]
REG.log("F5", "A_FE_wild", fm + " [wild cluster bootstrap Webb 9999, H0 b2=0]", ini, fin, len(MAIN), np.nan, np.nan, np.nan,
        np.nan, r_cl.params["d_share_extr"], pw[1], "mismo modelo que A_FE_cl; solo cambia la inferencia")
rows = [(LAB[n], r_cl.params[n], r_cl.std_errors[n], r_cl.pvalues[n], r_dk.std_errors[n], r_dk.pvalues[n],
         r_dk3.std_errors[n], r_dk3.pvalues[n], pw[j]) for j, n in enumerate(XN)]
tab_fe = pd.DataFrame(rows, columns=["variable", "coef", "EE_cluster", "p_cluster", "EE_DK_bw2", "p_DK_bw2",
                                     "EE_DK_bw3", "p_DK_bw3", "p_wild_Webb"]).set_index("variable")
save(tab_fe, "tabla_fe_principal")
sec("1a. FE bidireccional (CCAA + anio), muestra principal",
    f"N={len(MAIN)}, {N_MAIN} CCAA, T={T_MAIN}. EE cluster por CCAA (17 clusters), Driscoll-Kraay (Bartlett; con T=17 ancho 2-3, "
    f"poco fiable) y p-valor del wild cluster bootstrap restringido (Webb, {NBOOT} replicas, semilla {SEED}) para H0: coef=0.\n\n"
    + tm(tab_fe))

r_tr = fe_fit(MAIN, "y", XN, trends=True)
r_tr_dk = fe_fit(MAIN, "y", XN, trends=True, cov="kernel", bw=2)
log_fe("A_FE_trend", fm + " + tendencia lineal por CCAA [cluster]", r_tr, "d_share_extr", ini, fin, "robustez")
tab_tr = pd.DataFrame({"coef": r_tr.params[XN], "EE_cluster": r_tr.std_errors[XN], "p_cluster": r_tr.pvalues[XN],
                       "EE_DK_bw2": r_tr_dk.std_errors[XN], "p_DK_bw2": r_tr_dk.pvalues[XN]})
tab_tr.index = [LAB[i] for i in XN]
save(tab_tr, "tabla_fe_tendencias")
sec("1b. FE + tendencias lineales por CCAA (en diferencias = deriva de crecimiento propia por CCAA)", tm(tab_tr))

cc = cce(Yn, Xn)
tab_cce = cce_table(cc, XN)
tab_cce["var"] = tab_cce["var"].map(LAB)
save(tab_cce, "tabla_cce", index=False)
nobs = N_MAIN * T_MAIN
for est, key, res in (("MG", "CCE-MG", cc["res_mg"]), ("P", "CCE-P", cc["res_p"])):
    row = tab_cce[(tab_cce.estimador == key) & (tab_cce["var"] == LAB["d_share_extr"])].iloc[0]
    kk = N_MAIN * (4 + 6) if est == "MG" else 4 + N_MAIN * 6
    rss = (res ** 2).sum()
    REG.log("F5", f"A_CCE_{est}", f"d_ln_ipv ~ X + const + promedios transversales (y, X) [{key}, EE no parametricos]", ini, fin,
            nobs, np.nan, nobs * np.log(rss / nobs) + 2 * kk, nobs * np.log(rss / nobs) + np.log(nobs) * kk, np.nan,
            row.coef, row.p, "Pesaran 2006 | rmse_oos no aplica")
    BETA2_P[f"A_CCE_{est}"] = row.p
sec("1c. CCE-MG y CCE-pooled (Pesaran 2006)",
    f"Cada regresion se aumenta con constante y promedios transversales de y y de las 4 X (6 auxiliares por CCAA; {cc['dfres']} gl "
    "por unidad en MG: muy justo). EE no parametricos (varianza empirica de los b_i). Sin efectos de anio (los promedios los sustituyen).\n\n"
    + tm(tab_cce, index=False))

comp = pd.DataFrame({
    "FE cluster": r_cl.params[XN].values, "EE": r_cl.std_errors[XN].values,
    "FE+tend": r_tr.params[XN].values, "EE tend": r_tr.std_errors[XN].values,
    "CCE-MG": cc["b_mg"], "EE MG": cc["se_mg"], "CCE-P": cc["b_p"], "EE P": cc["se_p"]}, index=[LAB[i] for i in XN])
save(comp, "tabla_comparacion_estimadores")
sec(f"1d. Comparacion de estimadores (misma muestra: {N_MAIN} CCAA x 2009-2025)", tm(comp))

# ---- timing de b2 (misma muestra 2009-2024 para las tres alineaciones)
M24 = MAIN[MAIN.anio <= 2024].dropna(subset=["d_share_mid", "d_share_flow_t"]).copy()
trows = []
for tid, col, desc in (("T_flow_tm1", "d_share_extr", "flujo del anio t-1 (principal)"),
                       ("T_mid", "d_share_mid", "cuota a mitad de anio t"),
                       ("T_flow_t", "d_share_flow_t", "flujo del anio t (contemporaneo)")):
    xs = [col if x == "d_share_extr" else x for x in XN]
    rt = fe_fit(M24, "y", xs)
    Y_, X_ = arr(M24, "y", xs, CCAAS)
    pwt = wild_boot(Y_, X_, 1)
    mid = tid
    n_, r2a_, aic_, bic_ = stats_fe(rt)
    REG.log("F5", mid, "d_ln_ipv ~ " + " + ".join(xs) + " | CCAA + anio [2009-2024] [cluster; p = wild Webb]", 2009, 2024, n_, r2a_, aic_,
            bic_, np.nan, rt.params[col], pwt, "timing de b2 | rmse_oos no aplica")
    BETA2_P[mid] = pwt
    trows.append((desc, rt.params[col], rt.std_errors[col], rt.pvalues[col], pwt, 100 * rt.params[col], int(rt.nobs)))
ttab = pd.DataFrame(trows, columns=["alineacion de la cuota", "b2", "EE_cluster", "p_cluster", "p_wild_Webb", "b2 en %/pp", "N"])
save(ttab, "timing_b2", index=False)
sec("1g. Timing de b2 (FE bidireccional, 2009-2024, misma muestra)",
    "La cuota es un stock a 1 de enero; las tres alineaciones se comparan en la misma muestra. El flujo contemporaneo es el mas expuesto "
    "a causalidad inversa (precio -> llegadas en el mismo anio).\n\n" + tm(ttab, index=False))

# ---- diagnósticos del FE
Xd_all = dd(Xn).reshape(-1, 4)
vif = pd.Series([variance_inflation_factor(Xd_all, i) for i in range(4)], index=[LAB[i] for i in XN], name="VIF (X demeaned)")
res_fe = r_cl.resids.values
ee = resid_wide(r_cl)
ar1 = np.mean([np.corrcoef(ee[c].values[1:], ee[c].values[:-1])[0, 1] for c in ee.columns])
jb = jarque_bera(res_fe)
bp = het_breuschpagan(res_fe, np.column_stack([np.ones(len(res_fe)), Xd_all]))
diag = pd.DataFrame({"estadistico": [durbin_watson(res_fe), ar1, jb[0], bp[0]], "p": [np.nan, np.nan, jb[1], bp[1]]},
                    index=["Durbin-Watson (apilado)", "AR(1) medio residuos FE", "Jarque-Bera", "Breusch-Pagan (sobre X demeaned)"])
save(diag, "diagnosticos_fe")
save(vif.to_frame(), "vif")

# poolability
Xdm, ydm = dd(Xn), dd(Yn)
b_pool = np.linalg.solve(np.einsum("ntk,ntl->kl", Xdm, Xdm), np.einsum("ntk,nt->k", Xdm, ydm))
rss_r = ((ydm - Xdm @ b_pool) ** 2).sum()
N, T, k = Xn.shape
Yt, Xt = Yn - Yn.mean(1, keepdims=True), Xn - Xn.mean(1, keepdims=True)
Dt = np.eye(T)[:, 1:]
Dt = Dt - Dt.mean(0)
blocks = []
for i in range(N):
    blk = np.zeros((T, N * k))
    blk[:, i * k:(i + 1) * k] = Xt[i]
    blocks.append(np.hstack([blk, Dt]))
Wfull = np.vstack(blocks)
cf, *_ = np.linalg.lstsq(Wfull, Yt.reshape(-1), rcond=None)
rss_u = ((Yt.reshape(-1) - Wfull @ cf) ** 2).sum()
df1, df2 = (N - 1) * k, N * T - N - (T - 1) - N * k
Fp = ((rss_r - rss_u) / df1) / (rss_u / df2)
pF = stats.f.sf(Fp, df1, df2)
# wild cluster bootstrap (Webb) restringido del F de poolability: H0 = pendientes comunes
Pu = Wfull @ np.linalg.pinv(Wfull)
fit_r = Xdm @ b_pool
u_r = ydm - fit_r
XtXi_p = np.linalg.inv(np.einsum("ntk,ntl->kl", Xdm, Xdm))
cntp, totp = 0, 0
while totp < NBOOT:
    m = min(1000, NBOOT - totp)
    w = RNG.choice(WEBB, size=(m, N))
    ys = fit_r[None] + w[:, :, None] * u_r[None]
    ys = ys - ys.mean(1, keepdims=True) - ys.mean(2, keepdims=True) + ys.mean((1, 2), keepdims=True)
    bs_ = np.einsum("kl,ntl,mnt->mk", XtXi_p, Xdm, ys)
    rr_ = ((ys - np.einsum("ntk,mk->mnt", Xdm, bs_)) ** 2).sum((1, 2))
    yf = ys.reshape(m, -1)
    ru_ = ((yf - yf @ Pu.T) ** 2).sum(1)
    cntp += ((((rr_ - ru_) / df1) / (ru_ / df2)) >= Fp).sum()
    totp += m
pF_wild = (cntp + 1) / (NBOOT + 1)
pool = pd.DataFrame({"F": [Fp], "gl1": [df1], "gl2": [df2], "p_clasico": [pF], "p_wild_Webb": [pF_wild]},
                    index=["H0: pendientes iguales entre CCAA"])
save(pool, "poolability")
sec("1e. Diagnosticos del FE principal", tm(diag) + "\n" + tm(vif.to_frame()) +
    "\nPoolability (F de igualdad de pendientes; efectos de CCAA y anio comunes):\n\n" + tm(pool) +
    "\nNota: el p clasico supone errores iid y esta sobredimensionado (heterocedasticidad, AR(1) residual ~0.3-0.4); la referencia es el p wild. "
    f"Con N*k={N*k} pendientes y T={T} la potencia es minima. Limite de aleatorizacion: con {N} unidades, un contraste de una region por "
    f"permutacion/placebo no puede dar p < 1/{N} = {1/N:.3f}.")

# ---- CD
r_noyr = PanelOLS(MAIN.set_index(["ccaa", "anio"])["y"], MAIN.set_index(["ccaa", "anio"])[XN], entity_effects=True).fit()
cd_rows = {"FE bidireccional (residuos)": cd_test(ee),
           "CCE-MG (residuos)": cd_test(pd.DataFrame(cc["res_mg"].T, columns=CCAAS)),
           "CCE-P (residuos)": cd_test(pd.DataFrame(cc["res_p"].T, columns=CCAAS)),
           "FE solo CCAA, sin anio (residuos)": cd_test(resid_wide(r_noyr)),
           "d_ln_ipv (variable)": cd_test(pd.DataFrame(Yn.T, columns=CCAAS))}
cdt = pd.DataFrame(cd_rows).T
save(cdt, "cd_pesaran")
sec("3a. Dependencia transversal: CD de Pesaran (2004/2015) - NO CONCLUYENTE sobre residuos de FE y CCE",
    "CD = sqrt(2/(N(N-1))) sum sqrt(T_ij) rho_ij. **Advertencia**: sobre residuos de FE bidireccional y de CCE el CD no sigue una N(0,1) "
    "(problema de parametros incidentales; Juodis y Reese 2022, verificada en docs/literatura.md): la correlacion media de residuos de un FE "
    f"con efectos de anio es mecanicamente ~ -1/(N-1) = {-1/(N_MAIN-1):.3f}, de modo que un CD negativo 'significativo' o un CCE-MG que 'pasa' el "
    "test no son interpretables y NO se usan como diagnostico. Solo el CD de la variable d_ln_ipv (sin ajustar) es informativo: dependencia "
    f"transversal fuerte (factor nacional). Para T={T_MAIN} el |rho| medio esperado bajo independencia es ~ sqrt(2/(pi T)) = "
    f"{np.sqrt(2/(np.pi*T_MAIN)):.2f}; el observado en residuos (0.3) es mayor, indicio (no prueba) de dependencia heterogenea remanente. "
    "No se implementa el CD ponderado de Juodis-Reese.\n\n" + tm(cdt))

# ---- CIPS
cips_rows = []
sub = A[A.ccaa.isin(CCAAS) & (A.anio >= 2008) & (A.anio <= 2025)]
for nm, col in [("ln IPV", "ln_ipv"), ("ln ocupados", "ln_ocupados"), ("cuota extranjera (pp)", "share_extr"),
                ("ln pob espanola", "ln_pob_espanola"), ("terminadas/1000 hab", "term_pc")]:
    Yl, _ = arr(sub, col, [col], CCAAS)
    for tr, yy in (("nivel", Yl), ("1a diferencia", np.diff(Yl, axis=1))):
        for p in (0, 1):
            st = cips(yy, p)
            sim = cips_sim(*yy.shape, p)
            cips_rows.append((nm, tr, p, yy.shape[0], yy.shape[1], st, np.quantile(sim, .05), (sim <= st).mean()))
cipsd = pd.DataFrame(cips_rows, columns=["serie", "transformacion", "retardos", "N", "T", "CIPS*", "vc5%_sim", "p_sim"])
save(cipsd, "cips")
sec("3b. Raiz unitaria de panel CIPS (Pesaran 2007), con constante, truncado",
    "Implementacion propia (CADF con promedios transversales, 0/1 retardos). Valores criticos y p-valores por simulacion "
    "(1.000 replicas, N y T de cada serie, un factor comun + ruido normal; semilla fija), no de las tablas del articulo. "
    "H0: raiz unitaria en todas las unidades. Con T=17-18 es orientativo.\n\n" + tm(cipsd))

# ---- robustez de muestras
X3 = XN[:3]
r16_3 = fe_fit(MAIN, "y", X3)
log_fe("R_sin_term", "d_ln_ipv ~ " + " + ".join(X3) + f" | CCAA + anio [{N_MAIN} CCAA, 2009-2025]", r16_3, "d_share_extr", ini, fin,
       "robustez (muestra principal sin terminadas)")
rpt = fe_fit(MAIN.dropna(subset=["y_pt"]), "y_pt", XN)
log_fe("R_ptasado_main", "d_ln_p_tasado ~ " + " + ".join(XN) + " | CCAA + anio [2009-2025]", rpt, "d_share_extr", ini, fin,
       "robustez: dependiente valor tasado")
SL = A[(A.anio >= 2003) & (A.anio <= 2025)].dropna(subset=["y_pt", "d_ln_ocup", "d_share_extr", "d_ln_pob_esp"])
rl = fe_fit(SL, "y_pt", X3)
log_fe("R_ptasado_2003", "d_ln_p_tasado ~ " + " + ".join(X3) + " | CCAA + anio [17 CCAA, 2003-2025, Navarra incompleta]", rl,
       "d_share_extr", 2003, 2025, "robustez larga (sin terminadas; no balanceado)")
rl_dk = fe_fit(SL, "y_pt", X3, cov="kernel", bw=3)
rows = []
for nm, rr_ in (("IPV, 2009-2025, sin term.", r16_3),
                ("Valor tasado, 2009-2025", rpt), ("Valor tasado 2003-2025, 17 CCAA, sin term.", rl)):
    for n in XN:
        if n in rr_.params.index:
            rows.append((nm, LAB[n], rr_.params[n], rr_.std_errors[n], rr_.pvalues[n], int(rr_.nobs)))
rob = pd.DataFrame(rows, columns=["muestra/dependiente", "variable", "coef", "EE_cluster", "p", "N"])
save(rob, "robustez_muestras_anual", index=False)
sec("1f. Robustez de muestra y variable dependiente (FE bidireccional, EE cluster)", tm(rob, index=False) +
    f"\nValor tasado 2003-2025: b2 con Driscoll-Kraay bw=3: {rl_dk.params['d_share_extr']:.4f} (EE {rl_dk.std_errors['d_share_extr']:.4f}).")

# ================================================================ 2. Trimestral
Q = pd.read_csv(ROOT / "data/processed/panel_ccaa_q.csv")
Q["per"] = pd.PeriodIndex(Q.trimestre, freq="Q")
Q = Q.sort_values(["ccaa", "per"]).reset_index(drop=True)
Q["share_extr"] = 100 * Q.pob_extranj / Q.pob_total
Q["d4_share_extr"] = Q.groupby("ccaa").share_extr.diff(4)
Q["term_pc"] = 1000 * Q.terminadas / Q.pob_total
Q["term_pc_l1"] = Q.groupby("ccaa").term_pc.shift(1)
Q["d4_ln_term_l1"] = Q.groupby("ccaa").d4_ln_terminadas.shift(1)
Q["t_idx"] = Q.per.apply(lambda p: p.year * 4 + p.quarter - 1)
q_models = {
    "Q1_sin_pob": ["d4_ln_ocupados", "d4_ln_compraventas", "d4_ln_term_l1"],
    "Q2_con_pob_d4": ["d4_ln_ocupados", "d4_ln_compraventas", "d4_ln_term_l1", "d4_share_extr", "d4_ln_pob_espanola"],
    "Q3_term_por_hab": ["d4_ln_ocupados", "d4_ln_compraventas", "term_pc_l1", "d4_share_extr", "d4_ln_pob_espanola"],
}
allq = sorted(set(sum(q_models.values(), [])))
QS = Q.dropna(subset=["d4_ln_ipv"] + allq)
QS = QS[QS.per <= pd.Period("2025Q1", "Q")]
qi, qf = str(QS.per.min()), str(QS.per.max())


def qfit(cols, cov, bw=None):
    d = QS.set_index(["ccaa", "t_idx"]).sort_index()
    mod = PanelOLS(d["d4_ln_ipv"], d[cols], entity_effects=True, time_effects=True)
    if cov == "cl":
        return mod.fit(cov_type="clustered", cluster_entity=True)
    return mod.fit(cov_type="kernel", kernel="bartlett", bandwidth=bw)


qrows = []
for mid, cols in q_models.items():
    rc, rd4, rd8 = qfit(cols, "cl"), qfit(cols, "dk", 4), qfit(cols, "dk", 8)
    n, r2a, aic, bic = stats_fe(rc)
    REG.log("F5", mid, "d4_ln_ipv ~ " + " + ".join(cols) + " | CCAA + trimestre [trimestral, cluster]", qi, qf, n, r2a, aic, bic,
            np.nan, np.nan, np.nan, "robustez trimestral; poblacion interpolada hasta 2025Q1 | rmse_oos no aplica")
    if "d4_share_extr" in cols:
        BETA2_P["Q_" + mid] = max(rc.pvalues["d4_share_extr"], rd4.pvalues["d4_share_extr"])   # el mayor entre cluster y DK(bw4)
    for c in cols:
        qrows.append((mid, c, rc.params[c], rc.std_errors[c], rc.pvalues[c], rd4.std_errors[c], rd4.pvalues[c],
                      rd8.std_errors[c], rd8.pvalues[c], n))
qtab = pd.DataFrame(qrows, columns=["modelo", "variable", "coef", "EE_cluster", "p_cluster", "EE_DK_bw4", "p_DK_bw4",
                                    "EE_DK_bw8", "p_DK_bw8", "N"])
save(qtab, "tabla_trimestral", index=False)
for mid in ("Q2_con_pob_d4", "Q3_term_por_hab"):
    s_ = qtab[(qtab.modelo == mid) & (qtab.variable == "d4_share_extr")].iloc[0]
cdq = cd_test(resid_wide(qfit(q_models["Q1_sin_pob"], "cl")))
sec("2. Panel trimestral (robustez): Delta4 ln IPV",
    f"Muestra comun a los tres modelos: {QS.ccaa.nunique()} CCAA, {qi}-{qf} (N={len(QS)}), FE CCAA + FE trimestre. "
    "Delta4 solapa 4 trimestres (MA(3)): EE Driscoll-Kraay con ancho 4 y 8 ademas de cluster por CCAA. "
    "**Advertencia**: la poblacion es anual (1 de enero) interpolada log-linealmente y acaba en 2025Q1; solo entra en Delta4 (Q2, Q3) "
    "y recorta la muestra a 2025Q1. Q1 usa d4 ln terminadas retardada 1 trimestre (sin poblacion); Q3 usa terminadas por 1.000 hab. "
    "(nivel, t-1, poblacion interpolada). Las d4 de poblacion interpolada son casi deterministas por tramos: no son variacion "
    "trimestral informativa.\n\n" + tm(qtab, index=False) +
    f"\nCD de Pesaran (residuos Q1): {cdq['CD']:.2f} (p={cdq['p']:.3g}); |rho| medio {cdq['abs_rho_medio']:.2f}.")

# ================================================================ 4. Heterogeneidad
het_rows = []


def het_fit(labs, mid):
    df = MAIN.copy()
    names = list(XN)
    inter = []
    for lab in labs:
        d_ = df.ccaa.map(lambda c: 1.0 if REGIONES.get(c) == lab else 0.0)
        for v in (0, 1):
            nm = f"{XN[v].replace('d_ln_', 'dln_').replace('d_share_extr', 'dshare')}_x_{lab}"
            df[nm] = d_ * df[XN[v]]
            names.append(nm)
            inter.append(nm)
    r = fe_fit(df, "y", names)
    Yh, Xi = arr(df, "y", names, CCAAS)
    assert np.allclose(r.params[names].values, crve_t(dd(Xi), dd(Yh), 0)[0], atol=1e-7)
    log_fe(mid, "d_ln_ipv ~ X + (b1,b2) x " + "+".join(labs) + " | CCAA + anio", r, "d_share_extr", ini, fin, "heterogeneidad")
    out = []
    for nm in inter:
        pwb = wild_boot(Yh, Xi, names.index(nm))
        out.append((mid, "+".join(labs), nm, r.params[nm], r.std_errors[nm], r.pvalues[nm], pwb))
    return out, Xi, Yh, names


for lab in REGIONES.values():
    het_rows += het_fit([lab], f"H_{lab}")[0]
o, Xij, Yh, names_j = het_fit(list(REGIONES.values()), "H_conjunto")
het_rows += o
het = pd.DataFrame(het_rows, columns=["modelo", "grupo", "interaccion", "coef", "EE_cluster", "p_cluster", "p_wild_Webb"])
het["p_wild_Holm"] = np.nan
for m in (het.modelo == "H_conjunto", het.modelo != "H_conjunto"):
    for i, v in holm(het.loc[m, "p_wild_Webb"].to_dict()).items():
        het.loc[i, "p_wild_Holm"] = v
save(het, "heterogeneidad_interacciones", index=False)

# F conjunto (12 interacciones) con wild bootstrap
Xd_i, yd_i = dd(Xij), dd(Yh)
XtXi = np.linalg.inv(np.einsum("ntk,ntl->kl", Xd_i, Xd_i))
bj = XtXi @ np.einsum("ntk,nt->k", Xd_i, yd_i)
rss_u2 = ((yd_i - Xd_i @ bj) ** 2).sum()
Xb_r = Xd_i[:, :, :4]
Xri = np.linalg.inv(np.einsum("ntk,ntl->kl", Xb_r, Xb_r))
br_ = Xri @ np.einsum("ntk,nt->k", Xb_r, yd_i)
fitr = Xb_r @ br_
ur = yd_i - fitr
nr = Xij.shape[2] - 4
dfu = N_MAIN * T_MAIN - N_MAIN - T_MAIN + 1 - Xij.shape[2]
Fh = (((ur ** 2).sum() - rss_u2) / nr) / (rss_u2 / dfu)
pFh = stats.f.sf(Fh, nr, dfu)
cntF, tot = 0, 0
while tot < NBOOT:
    m = min(1000, NBOOT - tot)
    w = RNG.choice(WEBB, size=(m, N_MAIN))
    ys = fitr[None] + w[:, :, None] * ur[None]
    ys = ys - ys.mean(1, keepdims=True) - ys.mean(2, keepdims=True) + ys.mean((1, 2), keepdims=True)
    bu = np.einsum("kl,ntl,mnt->mk", XtXi, Xd_i, ys)
    eu = ((ys - np.einsum("ntk,mk->mnt", Xd_i, bu)) ** 2).sum((1, 2))
    brs = np.einsum("kl,ntl,mnt->mk", Xri, Xb_r, ys)
    er = ((ys - np.einsum("ntk,mk->mnt", Xb_r, brs)) ** 2).sum((1, 2))
    cntF += (((er - eu) / nr) / (eu / dfu) >= Fh).sum()
    tot += m
pFw = (cntF + 1) / (NBOOT + 1)
for kk_ in [k_ for k_ in BETA2_P if k_.startswith("H_")]:
    del BETA2_P[kk_]   # no son b2 de la misma hipotesis (b2 del grupo de referencia / F conjunto)
sec("4a. Heterogeneidad: interacciones de b1 (ocupados) y b2 (cuota extranjera) con dummies regionales",
    "Cada fila es el diferencial respecto al resto de CCAA (efectos de anio y CCAA incluidos). Modelos individuales (una dummy) "
    "y conjunto (6 dummies; referencia = resto de CCAA). EE cluster y p-valor wild cluster bootstrap restringido (Webb). "
    "Holm dentro de cada familia (12 interacciones). **Aviso**: cada dummy regional marca UN solo cluster; el EE cluster (CRVE) es "
    "poco fiable (p_cluster muy bajos con p_wild altos), y el wild bootstrap con un solo cluster tratado tampoco es valido (MacKinnon y Webb 2018): "
    "los p_wild agrupados en 0.3-0.5 reflejan esa degeneracion y NO evidencia de homogeneidad. Referencia: p_wild_Webb, con cautela.\n\n" + tm(het, index=False) +
    f"\nTest conjunto de las 12 interacciones = 0 (F de sumas de cuadrados, no robusto): F={Fh:.2f}, p={pF if False else pFh:.3g}; "
    f"p del F por wild bootstrap = {pFw:.3g}.")

# CCE individual
tc = stats.t.ppf(0.975, cc["dfres"])
ind = [(c, LAB[n], cc["bi"][i, j], cc["se_i"][i, j], cc["bi"][i, j] - tc * cc["se_i"][i, j], cc["bi"][i, j] + tc * cc["se_i"][i, j])
       for i, c in enumerate(CCAAS) for j, n in enumerate(XN)]
indd = pd.DataFrame(ind, columns=["ccaa", "variable", "coef", "EE", "IC95_inf", "IC95_sup"])
save(indd, "cce_por_ccaa", index=False)
fig, axs = plt.subplots(1, 4, figsize=(18, 6), sharey=True)
for j, (ax, n) in enumerate(zip(axs, XN)):
    s = indd[indd.variable == LAB[n]].reset_index(drop=True)
    for i, row in s.iterrows():
        col = "tab:red" if row.ccaa == "Comunitat Valenciana" else "tab:blue"
        ax.errorbar(row.coef, i, xerr=[[row.coef - row.IC95_inf], [row.IC95_sup - row.coef]], fmt="o", color=col, capsize=2)
    ax.axvline(0, color="grey", lw=.8)
    ax.axvline(cc["b_mg"][j], color="k", ls="--", lw=.8)
    ax.set_title(LAB[n], fontsize=9)
    ax.set_yticks(range(len(s)))
    ax.set_yticklabels(s.ccaa, fontsize=8)
fig.suptitle("Coeficientes CCE por CCAA (IC95% t con 7 gl; linea discontinua = CCE-MG). T=17 por unidad: muy imprecisos", fontsize=10)
plt.tight_layout()
plt.savefig(OUT / "cce_por_ccaa.png", dpi=130)
plt.close()
iv = CCAAS.index("Comunitat Valenciana")
piv = indd.pivot(index="ccaa", columns="variable", values="coef")
sec("4b. Coeficientes CCE individuales por CCAA",
    "**Advertencia**: cada unidad tiene T=17 y 10 parametros (7 gl); IC anchos; el CCE individual solo es consistente para T grande. "
    "Aqui los coeficientes; EE e IC95% en `cce_por_ccaa.csv` y `cce_por_ccaa.png`.\n\n" + tm(piv) +
    f"\nDispersion de b2 individual: sd={np.std(cc['bi'][:, 1], ddof=1):.3f} (EE MG={cc['se_mg'][1]:.3f}). "
    f"Valencia: b1={cc['bi'][iv, 0]:.3f} (EE {cc['se_i'][iv, 0]:.3f}), b2={cc['bi'][iv, 1]:.3f} (EE {cc['se_i'][iv, 1]:.3f}).")

# Valencia vs España
nq = pd.read_csv(ROOT / "data/processed/nacional_q.csv").set_index("trimestre")
vq = Q[Q.ccaa == "Comunitat Valenciana"].set_index("trimestre")
vrows = []
for a_, b_ in (("2014Q1", "2026Q2"), ("2021Q1", "2026Q2")):
    for ser in ("ipv", "p_tasado"):
        gv = 100 * (vq.loc[b_, ser] / vq.loc[a_, ser] - 1)
        gn = 100 * (nq.loc[b_, ser] / nq.loc[a_, ser] - 1)
        vrows.append((f"{a_}-{b_}", ser, gv, gn, gv - gn))
vtab = pd.DataFrame(vrows, columns=["periodo", "serie", "crec_acum_CV_%", "crec_acum_Espana_%", "dif_pp"])
save(vtab, "valencia_vs_espana", index=False)
sec("4c. C. Valenciana frente a Espana: crecimiento acumulado",
    "Del trimestre inicial a 2026Q2 (IPV base 2025 y valor tasado MIVAU; Espana = `nacional_q`).\n\n" + tm(vtab, index=False))

# ================================================================ Búsqueda
nreg = len(REG.read())
pv = {k: v for k, v in BETA2_P.items() if np.isfinite(v)}
hp = holm(pv)
srch = pd.DataFrame({"p_sin_corregir": pv, "p_Holm": hp, "p_Bonferroni": {k: min(1, v * len(pv)) for k, v in pv.items()}})
save(srch, "correccion_busqueda_beta2")
sec("5. Registro de busqueda y correccion para b2 (cuota extranjera)",
    f"Especificaciones registradas en `output/registro_busqueda_f5.csv`: **{nreg}**. Familia de {len(pv)} p-valores de b2 "
    "(distintas inferencias, tendencias, CCE, muestras, alineaciones temporales y b2 trimestrales; excluidas las interacciones de heterogeneidad, que son otra hipotesis) corregida por Holm y Bonferroni. "
    "Muy correlacionadas entre si, asi que ambas correcciones son conservadoras.\n\n" + tm(srch))

# ================================================================ resumen
g = lambda n, c: r_cl.params[n] if c == "b" else r_cl.std_errors[n]
cdr = lambda k: f"{cdt.loc[k, 'abs_rho_medio']:.2f}"
srch_min = srch.drop(index=[i for i in srch.index if i.startswith("A_FE_dk")], errors="ignore")
tl = ttab.set_index("alineacion de la cuota")
cip = cipsd.set_index(["serie", "transformacion", "retardos"])
head = [
    "# F5: panel de CCAA (P4) - resumen\n",
    f"Generado por `src/f5_panel.py` (semilla {SEED}).\n",
    "## Respuesta a P4\n",
    "**Pregunta**: ¿difieren entre CCAA (y en la C. Valenciana) las asociaciones del precio de la vivienda con empleo y poblacion extranjera?\n",
    "- **Respuesta**: *no se detecta heterogeneidad* de pendientes entre CCAA. Esto es ausencia de evidencia, **no evidencia de homogeneidad**: "
    f"con N={N_MAIN} y T={T_MAIN} la potencia es minima (el p minimo de un contraste por aleatorizacion de una region es 1/{N_MAIN}={1/N_MAIN:.3f}; "
    "el CCE individual tiene 7 gl por CCAA).",
    "- Nivel de evidencia: **asociacion condicional y fragil** (panel observacional con FE de CCAA y anio / CCE). Sin identificacion causal en "
    "esta fase; para la lectura causal remite al IV de F3 (no se repite aqui).",
    f"- C. Valenciana: ninguna interaccion distinguible del resto (p wild de b1 y b2 en tabla 4a). La unica diferencia solida es **descriptiva** y depende de la "
    "medida de precio (tabla 4c): 2014Q1-2026Q2 el IPV de la CV crece menos que el de Espana pero su valor tasado mas; desde 2021Q1 crece mas con ambas.",
    f"- FE bidireccional ({N_MAIN} CCAA, 2009-2025): b1 (elasticidad al empleo) = {g('d_ln_ocup','b'):.3f} (EE cluster {g('d_ln_ocup','s'):.3f}, "
    f"p wild={pw[0]:.3f}); b2 = {g('d_share_extr','b'):.4f} (EE {g('d_share_extr','s'):.4f}; {100*g('d_share_extr','b'):.2f} %/pp; "
    f"p cluster={r_cl.pvalues['d_share_extr']:.3f}, DK bw2={r_dk.pvalues['d_share_extr']:.3f}, wild={pw[1]:.3f}). R2 within ajustado = "
    f"{stats_fe(r_cl)[1]:.3f}: los regresores explican poco de las desviaciones regionales respecto del ciclo comun.",
    f"- **b2 depende del timing** (2009-2024, misma muestra): flujo t-1 {tl.iloc[0]['b2 en %/pp']:.2f} %/pp (p wild {tl.iloc[0]['p_wild_Webb']:.3f}); "
    f"cuota a mitad de anio {tl.iloc[1]['b2 en %/pp']:.2f} %/pp (p wild {tl.iloc[1]['p_wild_Webb']:.3f}); "
    f"flujo contemporaneo {tl.iloc[2]['b2 en %/pp']:.2f} %/pp (p wild {tl.iloc[2]['p_wild_Webb']:.3f}). "
    f"Tras la correccion por busqueda (Holm sobre {len(pv)} p-valores de b2, incluidos los trimestrales con el mayor de p cluster y DK) el menor p ajustado es {min(hp.values()):.3f}: "
    f"{'ninguna alineacion es significativa' if min(hp.values()) > 0.05 else 'alguna especificacion sigue siendo significativa'} tras la correccion; b2 queda **entre {ttab['b2 en %/pp'].min():.1f} y {ttab['b2 en %/pp'].max():.1f} %/pp segun la alineacion**. "
    "No se afirma b2 = 0.",
    f"- CCE-MG: b1={cc['b_mg'][0]:.3f} ({cc['se_mg'][0]:.3f}), b2={cc['b_mg'][1]:.3f} ({cc['se_mg'][1]:.3f}); "
    f"CCE-P: b1={cc['b_p'][0]:.3f} ({cc['se_p'][0]:.3f}), b2={cc['b_p'][1]:.3f} ({cc['se_p'][1]:.3f}).",
    f"- Poolability: F={Fp:.2f}, p clasico={pF:.2g} (sobredimensionado), **p wild Webb={pF_wild:.3f}**; F conjunto de las 12 interacciones regionales: "
    f"p clasico={pFh:.2g}, p wild={pFw:.3f}.",
    f"- Dependencia transversal: el CD sobre residuos de FE y CCE **no es interpretable** (Juodis y Reese 2022; seccion 3a) y no se usa como diagnostico.\n",
    "## Discusion de signos y magnitudes\n",
    f"- **b2 frente a la literatura** (docs/literatura.md): Saiz (2007) encuentra ~+1 % en alquileres y valores por una entrada igual al 1 % de la poblacion, "
    "y Gonzalez y Ortega (2013) efectos positivos de la inmigracion sobre el precio en Espana. Un b2 ~ 0 (flujo t-1) discrepa; el flujo contemporaneo "
    "(~+1,9 %/pp) y la cuota a mitad de anio se acercan al orden de magnitud, pero con causalidad inversa posible. F3 (FE/2SLS, ver output/f3) da "
    "estimaciones tampoco distinguibles de 0; la comparacion directa exige expresar F5 en %/pp (hecho arriba).",
    f"- **b4 (terminadas por 1.000 hab., t-1) > 0** ({g('term_l1','b'):.4f}, EE {g('term_l1','s'):.4f}, p wild {pw[3]:.3f}) frente al signo negativo "
    "esperado de la oferta (Saiz 2010; Hilber y Vermeulen 2016; tabla de signos de literatura.md). No debe leerse como efecto de oferta: es compatible con "
    "simultaneidad/inercia (se termina mas donde los precios ya subian) y con dinamica omitida (AR(1) residual ~0,3); en CCE el signo se invierte y deja de "
    "ser significativo. Se deja como discrepancia abierta.",
    f"- **b1 y F2**: b1 es una elasticidad de corto plazo ({g('d_ln_ocup','b'):.2f} %/1 % de empleo), no comparable con la elasticidad de largo plazo de F2 (DOLS, 1,95 con EE HAC 0,48, evidencia mixta/inestable segun F2): "
    "F5 usa desviaciones regionales anuales respecto del ciclo comun (los efectos de anio absorben lo nacional) y probable atenuacion por el error muestral "
    "de la EPA regional en diferencias. Con valor tasado como dependiente b1 es mayor (tabla 1f), asi que b1 ~ 0 no es robusto a la medida de precio.",
    f"- **CIPS** (tabla 3b): no rechaza raiz unitaria en la primera diferencia de la cuota extranjera (CIPS* {cip.loc[('cuota extranjera (pp)','1a diferencia',0),'CIPS*']:.2f}, "
    f"p sim {cip.loc[('cuota extranjera (pp)','1a diferencia',0),'p_sim']:.2f}) ni de ln poblacion espanola (p sim "
    f"{cip.loc[('ln pob espanola','1a diferencia',0),'p_sim']:.2f}). Puede ser falta de potencia con T=17, o persistencia migratoria; si d_share fuese casi "
    "I(1), la regresion de un y I(0) estaria desequilibrada y b2, b3 tenderian a 0 con inferencia no estandar. Es una limitacion de b2 y b3.\n",
]
tail = ("\n## Problemas abiertos\n\n"
        "- Timing de b2 (stock a 1 de enero frente a IPV de media anual) decide el resultado; sin instrumento no se distingue entre efecto y causalidad inversa (F3).\n"
        "- T=17, N=17: pocos clusters (wild bootstrap como referencia); Driscoll-Kraay y CCE por unidad con pocos grados de libertad; CIPS y poolability con "
        "potencia dudosa; wild bootstrap invalido con un solo cluster tratado (interacciones regionales).\n"
        "- CD sobre residuos de FE/CCE no interpretable; no se implementa el CD ponderado de Juodis-Reese (CDw).\n"
        "- b4 > 0 sin explicacion estructural; falta probar dinamica (y retardada) en una fase posterior.\n"
        "- Nota (1) de Extremadura en MIVAU 32101000 sin resolver (revision F5).\n"
        "- Poblacion trimestral interpolada y hasta 2025Q1.\n"
        "- Valor tasado y `p_bde` son la misma serie (decisiones.md): robusteces no independientes.\n"
        "- rmse_oos no se calcula en el registro: los efectos de anio no son predecibles fuera de muestra.\n")
(OUT / "resumen_f5.md").write_text("\n".join(head) + "".join(MD) + tail)
print("F5 OK:", nreg, "modelos registrados;", f"{time.time() - T0:.0f}s")
