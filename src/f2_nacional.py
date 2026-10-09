"""F2 (nacional): raíces unitarias, réplica, cointegración, DOLS, búsqueda de corto plazo con
corrección (Bonferroni + bootstrap de la selección), OOS, diagnósticos y quiebres.
Determinista (semilla 20261009), sin red. Escribe en output/f2/ y output/registro_busqueda_f2.csv.
"""
import itertools
import sys
import time
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.recursive_ls import RecursiveLS  # noqa: F401
from statsmodels.stats.diagnostic import recursive_olsresiduals
from statsmodels.tsa.ardl import UECM, ardl_select_order
from statsmodels.tsa.stattools import adfuller, coint, kpss, zivot_andrews
from statsmodels.tsa.vector_ar.vecm import coint_johansen, select_order

sys.path.insert(0, str(Path(__file__).resolve().parent))
from econ_utils import (DUMMIES_Q, ROOT, SEED, Registry, bai_perron, chow, common_sample,  # noqa: E402
                        df_md, diagnostics, dm_test, dols, holm, load_nacional, ols_hac, tabla,
                        tabla_md)

warnings.filterwarnings("ignore")
T0 = time.time()
OUT = ROOT / "output" / "f2"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(ROOT / "output" / "registro_busqueda_f2.csv", reset=True)
Fw = load_nacional("1995Q1", "2026Q3")
S0, S1 = "2008Q1", "2026Q2"
BASE = ["ln_ocupados", "tipo_hip", "ln_permisos_l4", "ln_costes"]
P = pd.Period
MD = []  # líneas del resumen


def save(df, name, floatfmt=".4g", index=True):
    df.to_csv(OUT / f"{name}.csv", index=index)
    (OUT / f"{name}.md").write_text(df_md(df, floatfmt, index) + "\n")


def sec(title, text=""):
    MD.append(f"\n## {title}\n\n{text}\n")


def tm(df, floatfmt=".4g", index=True):
    return df_md(df, floatfmt, index) + "\n"


def fmt(c, s):
    return f"{c:.4f} ({s:.4f})"


# =============================================================== 1. raíces unitarias
UR_SERIES = ["ln_ipv", "ln_ipv_real", "ln_p_tasado", "ln_p_bde", "ln_ocupados", "tipo_hip", "tipo_hip_real",
             "ln_permisos", "ln_costes", "ln_renta_hog_real", "ln_pob_extranj", "ln_pob_total",
             "ln_hogares_epa", "ln_credito_nuevo"]
Fw["ln_ipv_real"] = Fw["ln_ipv"] - Fw["ln_deflactor"]


def ur_tests(x, nivel):
    r = {}
    try:
        a = adfuller(x, maxlag=8, regression="c", autolag="AIC")
        r.update(adf_c=a[0], adf_c_p=a[1], adf_c_lag=a[2])
    except Exception:
        pass
    if nivel:
        try:
            a = adfuller(x, maxlag=8, regression="ct", autolag="AIC")
            r.update(adf_ct=a[0], adf_ct_p=a[1])
        except Exception:
            pass
    try:
        r["kpss_c_p"] = kpss(x, regression="c", nlags="auto")[1]
        if nivel:
            r["kpss_ct_p"] = kpss(x, regression="ct", nlags="auto")[1]
    except Exception:
        pass
    try:
        z = zivot_andrews(x, maxlag=4, regression="ct" if nivel else "c", autolag="AIC")
        r.update(za=z[0], za_p=z[1], za_quiebre=str(x.index[z[4]]))
    except Exception:
        pass
    return r


def concl(lv, df_):
    g = lambda d, k: d.get(k, np.nan)
    unit = g(lv, "adf_c_p") > .05 and g(lv, "adf_ct_p") > .05
    kr = g(lv, "kpss_c_p") < .05 or g(lv, "kpss_ct_p") < .05
    dw = g(df_, "adf_c_p") < .05 or g(df_, "kpss_c_p") >= .05
    if not unit and not kr:
        return "I(0)"
    if unit and kr and dw:
        return "I(1)"
    return "ambigua"


rows, crow = [], []
for s in UR_SERIES:
    for lab, a, b in [("2008Q1-2026Q2", S0, S1), ("larga", None, None)]:
        x = Fw[s].loc[a:b].dropna() if a else Fw[s].dropna()
        if lab == "larga" and s in ("ln_ipv", "ln_ipv_real"):
            pass
        lv, dd = ur_tests(x, True), ur_tests(x.diff().dropna(), False)
        c = concl(lv, dd)
        ini, fin = str(x.index[0]), str(x.index[-1])
        rows.append(dict(serie=s, muestra=lab, rango=f"{ini}-{fin}", N_niv=len(x), orden="nivel", **lv))
        rows.append(dict(serie=s, muestra=lab, rango=f"{ini}-{fin}", N_niv=len(x) - 1, orden="dif", **dd))
        crow.append(dict(serie=s, muestra=lab, rango=f"{ini}-{fin}", N=len(x), conclusion=c,
                         adf_c_p=lv.get("adf_c_p"), adf_ct_p=lv.get("adf_ct_p"),
                         kpss_c_p=lv.get("kpss_c_p"), kpss_ct_p=lv.get("kpss_ct_p"),
                         adf_dif_p=dd.get("adf_c_p"), kpss_dif_p=dd.get("kpss_c_p"),
                         za_p=lv.get("za_p"), za_quiebre=lv.get("za_quiebre")))
ur_full = pd.DataFrame(rows)
ur_c = pd.DataFrame(crow)
save(ur_full, "raices_unitarias_detalle", index=False)
save(ur_c, "raices_unitarias", ".3f", index=False)
ur_wide = ur_c.pivot(index="serie", columns="muestra", values="conclusion")
sec("1. Raíces unitarias",
    "ADF (AIC, maxlag 8; constante y constante+tendencia en niveles), KPSS (nivel y tendencia), "
    "Zivot-Andrews (maxlag 4). Regla: I(0) si ADF rechaza y KPSS no; I(1) si ADF no rechaza (c y ct), "
    "KPSS rechaza y la primera diferencia es estacionaria; resto 'ambigua'. Se ofrecen la muestra "
    "2008Q1-2026Q2 y la muestra LARGA (todo lo disponible por serie; ln_p_tasado y ln_p_bde desde 1995).\n\n"
    + tm(ur_c.drop(columns=["adf_dif_p", "kpss_dif_p"]), ".3f", False))

# =============================================================== datos de trabajo (ect)
Q = DUMMIES_Q


def build_ect(frame, end, xs=BASE, fijas=Q, y="ln_ipv"):
    """DOLS con datos hasta `end` (inclusive). Devuelve dict de dols (ect sobre fechas <= end)."""
    sub = frame.loc[:end]
    return dols(sub, y, xs, fijas, k=2, maxlags=4, desde=S0)


# =============================================================== 2. réplica
lr_cols = ["ln_ipv"] + BASE
dlr = common_sample(Fw.loc[S0:"2025Q4"], lr_cols)
lr_rep = ols_hac("ln_ipv ~ " + " + ".join(BASE), dlr)
REG.log_res("F2", "rep_LR", "ln_ipv ~ " + " + ".join(BASE), lr_rep, "ln_costes", notas="réplica EG estático 2008Q1-2025Q4")
ect_rep = Fw["ln_ipv"] - lr_rep.predict(Fw)
Fw["ect_rep_l1"] = ect_rep.shift(1)
ecm_terms = "d_ln_ocupados + d_tipo_hip + d_ln_permisos_l4 + d_ln_ipv_l1 + d_ln_pob_extranj + ect_rep_l1"
ecm_cols = ["d_ln_ipv", "d_ln_ocupados", "d_tipo_hip", "d_ln_permisos_l4", "d_ln_ipv_l1", "d_ln_pob_extranj",
            "ect_rep_l1"]
decm = common_sample(Fw.loc[S0:"2025Q4"], ecm_cols)
ecm_sin = ols_hac("d_ln_ipv ~ " + ecm_terms, decm)
ecm_con = ols_hac("d_ln_ipv ~ " + ecm_terms + " + q2 + q3 + q4", decm)
REG.log_res("F2", "rep_ECM_sin", "d_ln_ipv ~ " + ecm_terms, ecm_sin, "ect_rep_l1", notas="réplica sin dummies")
REG.log_res("F2", "rep_ECM_con", "d_ln_ipv ~ " + ecm_terms + " + q2+q3+q4", ecm_con, "ect_rep_l1", notas="réplica con dummies")
ref_lr = {"Intercept": -6.59, "ln_ocupados": 0.878, "tipo_hip": -0.042, "ln_permisos_l4": 0.156, "ln_costes": 0.465}
ref_ecm = {"d_ln_ocupados": 0.686, "d_tipo_hip": -0.0147, "d_ln_permisos_l4": 0.025, "d_ln_ipv_l1": 0.254,
           "d_ln_pob_extranj": 0.321, "ect_rep_l1": -0.1265}
t1 = pd.DataFrame({"punto_partida": pd.Series(ref_lr), "replica": lr_rep.params, "EE_HAC": lr_rep.bse,
                   "p": lr_rep.pvalues}).loc[list(ref_lr)]
t2 = pd.DataFrame({"punto_partida": pd.Series(ref_ecm), "sin_dum": ecm_sin.params, "EE_sin": ecm_sin.bse,
                   "p_sin": ecm_sin.pvalues, "con_dum": ecm_con.params, "EE_con": ecm_con.bse,
                   "p_con": ecm_con.pvalues}).loc[list(ref_ecm)]
t2.loc["R2_aj"] = [0.60, ecm_sin.rsquared_adj, np.nan, np.nan, ecm_con.rsquared_adj, np.nan, np.nan]
t2.loc["N"] = [72, ecm_sin.nobs, np.nan, np.nan, ecm_con.nobs, np.nan, np.nan]
t1.loc["R2_aj (LR)"] = [np.nan, lr_rep.rsquared_adj, np.nan, np.nan]
t1.loc["N (LR)"] = [72, lr_rep.nobs, np.nan, np.nan]
save(t1, "replica_LR")
save(t2, "replica_ECM")
sec("2. Réplica del punto de partida (2008Q1-2025Q4)",
    f"N exacto: LR {int(lr_rep.nobs)} ({dlr.index[0]}-{dlr.index[-1]}); ECM {int(ecm_sin.nobs)} "
    f"({decm.index[0]}-{decm.index[-1]}). EE HAC(4). El ect de la réplica es el residuo del LR estático "
    "calculado también para 2007Q4 (los niveles existen), de ahí N=72 en el ECM. El punto de partida no "
    "reporta constante del ECM (aquí sí se estima).\n\n**LR estático**\n\n" + tm(t1, ".4g") +
    "\n**ECM dos etapas**\n\n" + tm(t2, ".4g") +
    "\nLas pendientes del LR reproducen el punto de partida casi exactamente (0,878 / −0,042 / 0,156 / 0,465); "
    "solo cambia la constante (consistente con el rebase del IPV a base 2025 y de otros índices). En el ECM los "
    "coeficientes de ocupados, tipo, permisos y ect son próximos; la mayor diferencia es d_ln_pob_extranj "
    "(0,16 frente a 0,321 y no significativo), compatible con la revisión/interpolación de la población extranjera (ECP). "
    "Es una conjetura: no se dispone de la base del punto de partida para verificarlo. Con dummies el R² aj sube.\n")
# columna ect común
rep_diag = {}

# =============================================================== 3. cointegración
Qdf = lambda d: d[Q].astype(float)


def coint_system(frame, y, xs, label):
    d = common_sample(frame, [y] + xs)
    out = dict(sistema=label, y=y, X=" + ".join(xs), ini=str(d.index[0]), fin=str(d.index[-1]), N=len(d))
    # Engle-Granger
    try:
        t, p, cv = coint(d[y], d[xs], trend="c", method="aeg", maxlag=4, autolag="aic")
        out.update(EG_t=t, EG_p=p, EG_rech=p < .05)
    except Exception as e:
        out.update(EG_t=np.nan, EG_p=np.nan, EG_rech=False)
    # Johansen
    try:
        arr = d[[y] + xs].values
        try:
            k = int(select_order(arr, maxlags=4, deterministic="co").aic)
        except Exception:
            k = 1
        j = coint_johansen(arr, det_order=0, k_ar_diff=k)
        rt = next((r for r in range(len(j.lr1)) if j.lr1[r] < j.cvt[r, 1]), len(j.lr1))
        rm = next((r for r in range(len(j.lr2)) if j.lr2[r] < j.cvm[r, 1]), len(j.lr2))
        out.update(J_kardiff=k, J_traza0=j.lr1[0], J_cv95=j.cvt[0, 1], J_rango_traza=rt, J_rango_maxeig=rm,
                   J_rech=rt >= 1)
    except Exception:
        out.update(J_rech=False)
    # ARDL bounds (caso 3), dummies trimestrales fijas EN el contraste (F de Wald propio sobre niveles
    # retardados; bounds_test de statsmodels descarta `fixed`), k = nº de regresores x (sin la dependiente)
    try:
        from statsmodels.tsa.ardl import pss_critical_values as pss
        ex = d[xs]
        sel = ardl_select_order(d[y], 4, ex, 2, trend="c", fixed=Qdf(d), ic="aic")
        dl = sel.model.dl_lags
        order = {c: max(max(dl[c]), 1) if c in dl and len(dl[c]) else 1 for c in xs}  # por NOMBRE
        plag = max(max(sel.model.ar_lags), 1)
        u = UECM(d[y], plag, ex, order, trend="c", fixed=Qdf(d))
        r = u.fit()
        names = list(r.params.index)
        lv = [names.index(f"{y}.L1")] + [names.index(f"{x}.L1") for x in xs]
        R = np.zeros((len(lv), len(names)))
        for i_, j_ in enumerate(lv):
            R[i_, j_] = 1
        cov = r.cov_params().values
        coef = R @ r.params.values
        F = float(coef @ np.linalg.inv(R @ cov @ R.T) @ coef / len(lv))
        kx = len(xs)
        lo, up = pss.crit_vals[(kx, 3, False)][1], pss.crit_vals[(kx, 3, True)][1]
        tY = float(r.tvalues[f"{y}.L1"])
        out.update(ARDL_p=plag, ARDL_ordenes_x=str(order), ARDL_N=int(r.nobs), ARDL_k=kx, ARDL_F=F, ARDL_I0_5=lo,
                   ARDL_I1_5=up, ARDL_t_yL1=tY, ARDL_rech=F > up,
                   ARDL_zona="rechaza (F>I1)" if F > up else "no concluyente" if F > lo else "no rechaza (F<I0)")
        out["_uecm"] = u.fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    except Exception as e:
        out.update(ARDL_rech=False, ARDL_err=str(e)[:60])
    n_rech = int(bool(out.get("EG_rech"))) + int(bool(out.get("J_rech"))) + int(bool(out.get("ARDL_rech")))
    out["n_rechazos"] = n_rech
    out["decision"] = ("cointegración (3/3)" if n_rech == 3 else "cointegración (2/3, discrepancia)"
                       if n_rech == 2 else "evidencia mixta (1/3)" if n_rech == 1 else "sin cointegración (0/3)")
    return out


EXT = {"base": [], "+pob_extranj": ["ln_pob_extranj"], "+renta": ["ln_renta_hog_real"],
       "+pob_total": ["ln_pob_total"]}
systems = []
Fm = Fw.loc[S0:S1]
Fl = Fw.loc["2003Q1":S1]
for ylab, y, frame, xb in [
        ("ln_ipv 2008Q1-2026Q2 (principal)", "ln_ipv", Fm, BASE),
        ("ln_ipv_real (tipo real, costes reales)", "ln_ipv_real", Fm,
         ["ln_ocupados", "tipo_hip_real", "ln_permisos_l4", "ln_costes_real"]),
        ("ln_p_tasado 2003Q1-2026Q2", "ln_p_tasado", Fl, BASE),
        ("ln_p_bde 2003Q1-2026Q2", "ln_p_bde", Fl, BASE)]:
    for el, ex_ in EXT.items():
        systems.append(coint_system(frame, y, xb + ex_, f"{ylab} / {el}"))
uecm_base = systems[0].get("_uecm")
cdf = pd.DataFrame([{k: v for k, v in s.items() if not k.startswith("_")} for s in systems])
save(cdf, "cointegracion", ".4g", index=False)
sec("3. Cointegración (se reportan SIEMPRE los tres contrastes)",
    "EG (statsmodels.coint, MacKinnon, AIC), Johansen (det_order=0, k_ar_diff por AIC del VAR/VECM ≤4, traza al 5 %; "
    "no admite dummies estacionales), ARDL bounds (caso 3; ardl_select_order AIC maxlag 4/orden ≤2 con dummies trimestrales fijas; órdenes asignados por NOMBRE "
    "de variable y regresores excluidos forzados a orden 1; F de Wald propio sobre y.L1 y x.L1 en el UECM CON dummies "
    "(bounds_test de statsmodels las descarta) y valores críticos PSS caso III con k = nº de regresores x, sin la dependiente). Decisión: ≥2 de 3 (docs/decisiones.md).\n\n"
    + tm(cdf[["sistema", "N", "EG_p", "J_kardiff", "J_traza0", "J_cv95", "J_rango_traza", "J_rango_maxeig",
              "ARDL_p", "ARDL_ordenes_x", "ARDL_N", "ARDL_k", "ARDL_F", "ARDL_I0_5", "ARDL_I1_5", "ARDL_t_yL1", "ARDL_zona", "n_rechazos", "decision"]], ".3g", False))

# =============================================================== 4. largo plazo preferido
dol = {}
dol["DOLS base (+q)"] = dols(Fw.loc[:S1], "ln_ipv", BASE, Q, k=2, desde=S0)
dol["DOLS base + epa21 + tipo22"] = dols(Fw.loc[:S1], "ln_ipv", BASE, Q + ["epa21", "tipo22"], k=2, desde=S0)
dol["DOLS +pob_extranj"] = dols(Fw.loc[:S1], "ln_ipv", BASE + ["ln_pob_extranj"], Q, k=2, desde=S0)
dol["DOLS +renta"] = dols(Fw.loc[:S1], "ln_ipv", BASE + ["ln_renta_hog_real"], Q, k=2, desde=S0)
lr_rows = []
for k, v in dol.items():
    res = v["res"]
    for x in v["beta"].index:
        lr_rows.append(dict(metodo=k, N=v["n"], var=x, coef=res.params[x], EE_HAC=res.bse[x], p=res.pvalues[x]))
    lr_rows.append(dict(metodo=k, N=v["n"], var="const", coef=res.params["const"], EE_HAC=res.bse["const"],
                        p=res.pvalues["const"]))
    REG.log("F2", "lr_" + k.replace(" ", "_"), "DOLS±2: ln_ipv ~ " + "+".join(v["beta"].index), res.model.data.row_labels[0],
            res.model.data.row_labels[-1], v["n"], res.rsquared_adj, res.aic, res.bic,
            coef_interes=res.params["ln_ocupados"], p_interes=res.pvalues["ln_ocupados"], notas="largo plazo")
dc = common_sample(Fw.loc[S0:S1], ["ln_ipv"] + BASE)
eg_s = ols_hac("ln_ipv ~ " + " + ".join(BASE), dc)
eg_q = ols_hac("ln_ipv ~ " + " + ".join(BASE) + " + q2+q3+q4", dc)
for lab, res in [("EG estático (const)", eg_s), ("EG estático (+q)", eg_q)]:
    for x in ["Intercept"] + BASE:
        lr_rows.append(dict(metodo=lab, N=int(res.nobs), var="const" if x == "Intercept" else x, coef=res.params[x],
                            EE_HAC=res.bse[x], p=res.pvalues[x]))
    REG.log_res("F2", "lr_" + lab.replace(" ", "_"), "ln_ipv ~ " + "+".join(BASE), res, "ln_ocupados", notas="largo plazo estático")
if uecm_base is not None:
    pr = uecm_base.params
    cv = uecm_base.cov_params()
    a = "ln_ipv.L1"
    for x in BASE:
        nm = f"{x}.L1"
        if nm in pr.index:
            b = -pr[nm] / pr[a]
            g = pd.Series(0.0, index=pr.index)
            g[nm] = -1 / pr[a]
            g[a] = pr[nm] / pr[a] ** 2
            se = float(np.sqrt(g.values @ cv.loc[pr.index, pr.index].values @ g.values))
            from scipy import stats as _st
            lr_rows.append(dict(metodo="UECM implícito (delta, HAC)", N=int(uecm_base.nobs), var=x, coef=b,
                                EE_HAC=se, p=2 * _st.norm.sf(abs(b / se))))
lr_tab = pd.DataFrame(lr_rows)
save(lr_tab, "largo_plazo", ".4g", index=False)
beta_pref = dol["DOLS base (+q)"]
lr_w = lr_tab.assign(c=lambda d: d.apply(lambda r: f"{r.coef:.3f} ({r.EE_HAC:.3f})", axis=1)).pivot(
    index="var", columns="metodo", values="c")
exp_sign = {"ln_ocupados": "+", "tipo_hip": "-", "ln_permisos_l4": "-", "ln_costes": "+", "ln_pob_extranj": "+",
            "ln_renta_hog_real": "+"}
lr_w["signo_esperado"] = pd.Series(exp_sign)
sec("4. Largo plazo", "DOLS ±2 con HAC(4) (estimador preferido, vector base con dummies trimestrales en la relación). "
    "Celdas: coef (EE HAC). Signos esperados de docs/literatura.md.\n\n" + tm(lr_w, index=True))

# =============================================================== 5. búsqueda
ect_full = beta_pref["ect"]
Fw["ect_l1"] = ect_full.shift(1)
GROUPS = {
    "ocupados": [None, "d_ln_ocupados", "d_ln_ocupados_l1"],
    "tipo": [None, "d_tipo_hip", "d_tipo_hip_l1"],
    "permisos": [None, "d_ln_permisos_l4"],
    "costes": [None, "d_ln_costes"],
    "renta": [None, "d_ln_renta_hog_real"],
    "pob": [None, "d_ln_pob_extranj", "d_ln_pob_extranj4", "d_ln_pob_total"],
    "ipv": [None, "d_ln_ipv_l1", "d_ln_ipv_l4"],
    "credito": [None, "d_ln_credito_nuevo"],
}
CAND = [c for g in GROUPS.values() for c in g if c]
COLS = ["const"] + Q + ["ect_l1"] + CAND
need = ["d_ln_ipv", "ect_l1"] + CAND + Q
C = common_sample(Fw.loc[S0:S1], need)
N = len(C)
y = C["d_ln_ipv"].values
M = np.column_stack([np.ones(N)] + [C[c].values for c in COLS[1:]])
cidx = {c: i for i, c in enumerate(COLS)}
MODELS = list(itertools.product(*GROUPS.values()))
MODELS = [tuple(t for t in m if t) for m in MODELS]
fix_ix = [0, 1, 2, 3, 4]
mix = [fix_ix + [cidx[t] for t in m] for m in MODELS]
NM = len(MODELS)
corr_pob = pd.DataFrame({"corr_niveles(ln_pob_extranj, ln_pob_total)": [Fw.loc[S0:S1, ["ln_pob_extranj", "ln_pob_total"]].corr().iloc[0, 1]],
                         "corr_dif(d_ln_pob_extranj, d_ln_pob_total)": [C[["d_ln_pob_extranj", "d_ln_pob_total"]].corr().iloc[0, 1]],
                         "corr_dif(d_ln_pob_extranj4, d_ln_pob_total)": [C[["d_ln_pob_extranj4", "d_ln_pob_total"]].corr().iloc[0, 1]]})
save(corr_pob, "corr_pob", ".3f", index=False)

# -- OOS: ect re-estimado con datos hasta t-1 en cada origen
orig = [p for p in C.index if p >= P("2018Q1", "Q")]
E = {}
for T in orig:
    e = build_ect(Fw, str(T - 1))["ect"]
    E[T] = e.reindex(Fw.index).shift(1).reindex(C.index).values
tr_idx = {T: np.where(C.index < T)[0] for T in orig}
te_idx = {T: int(np.where(C.index == T)[0][0]) for T in orig}
err = np.full((NM, len(orig)), np.nan)
bench = {k: np.full(len(orig), np.nan) for k in ["AR4+q", "media historica", "paseo con deriva (20T)"]}
Xar = np.column_stack([np.ones(N)] + [C[c].values for c in Q] + [C[f"d_ln_ipv_l{k}"].values for k in range(1, 5)])
for j, T in enumerate(orig):
    Mo = M.copy()
    Mo[:, 4] = E[T]
    tr, te = tr_idx[T], te_idx[T]
    Xt = Mo[tr]
    G, g = Xt.T @ Xt, Xt.T @ y[tr]
    for i, ix in enumerate(mix):
        b = np.linalg.solve(G[np.ix_(ix, ix)], g[ix])
        err[i, j] = y[te] - Mo[te, ix] @ b
    b = np.linalg.lstsq(Xar[tr], y[tr], rcond=None)[0]
    bench["AR4+q"][j] = y[te] - Xar[te] @ b
    bench["media historica"][j] = y[te] - y[tr].mean()
    bench["paseo con deriva (20T)"][j] = y[te] - y[tr][-20:].mean()
rmse_oos = np.sqrt(np.nanmean(err ** 2, axis=1))

# -- estimación con HAC de cada modelo
srows, crows = [], []
for i, m in enumerate(MODELS):
    cols = ["ect_l1"] + Q + list(m)
    Xd = sm.add_constant(C[cols])
    r = sm.OLS(C["d_ln_ipv"], Xd).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    r0 = sm.OLS(C["d_ln_ipv"], Xd).fit()
    mid = f"busq_{i + 1:04d}"
    srows.append(dict(id=mid, terminos=" + ".join(m) if m else "(vacío)", k=len(cols) + 1, N=int(r.nobs),
                      r2_adj=r0.rsquared_adj, aic=r0.aic, bic=r0.bic, rmse_oos=rmse_oos[i],
                      ect=r.params["ect_l1"], ect_p=r.pvalues["ect_l1"]))
    for c in ["ect_l1"] + list(m):
        crows.append(dict(id=mid, term=c, coef=r.params[c], se=r.bse[c], p=r.pvalues[c]))
    REG.log("F2", mid, "d_ln_ipv ~ ect_l1 + q2+q3+q4" + "".join(" + " + t for t in m), C.index[0], C.index[-1],
            int(r.nobs), r0.rsquared_adj, r0.aic, r0.bic, rmse_oos[i], r.params["ect_l1"], r.pvalues["ect_l1"],
            "búsqueda corto plazo; coef de interés = ect(t-1)")
S = pd.DataFrame(srows)
CF = pd.DataFrame(crows)
S.to_csv(OUT / "busqueda_modelos.csv", index=False)
CF.to_csv(OUT / "busqueda_coefs.csv", index=False)
# comprobación del cálculo rápido
G0, g0 = M.T @ M, M.T @ y
iw = int(S.r2_adj.idxmax())
ix = mix[iw]
b0 = np.linalg.solve(G0[np.ix_(ix, ix)], g0[ix])
rss = float(((y - M[:, ix] @ b0) ** 2).sum())
r2a_fast = 1 - (rss / (N - len(ix))) / (((y - y.mean()) ** 2).sum() / (N - 1))
assert abs(r2a_fast - S.r2_adj.max()) < 1e-8
i_r2, i_aic, i_bic, i_rm = int(S.r2_adj.idxmax()), int(S.aic.idxmin()), int(S.bic.idxmin()), int(S.rmse_oos.idxmin())
i_empty = int(S.index[S.terminos == "(vacío)"][0])
PREF = i_r2

# -- Bonferroni / EBA
pref_id = S.id[PREF]
terms_all = ["ect_l1"] + CAND
eba = []
for t in terms_all:
    sub = CF[CF.term == t]
    K = len(sub)
    sig = (sub.p < .05).mean()
    pr = CF[(CF.id == pref_id) & (CF.term == t)]
    in_pref = len(pr) > 0
    eba.append(dict(termino=t, K_modelos=K, frac_signif_5pct=sig, signo_pos=(sub.coef > 0).mean(),
                    coef_min=sub.coef.min(), coef_max=sub.coef.max(),
                    Leamer_inf=(sub.coef - 2 * sub.se).min(), Leamer_sup=(sub.coef + 2 * sub.se).max(),
                    en_preferido=in_pref, coef_pref=pr.coef.iloc[0] if in_pref else np.nan,
                    EE_pref=pr.se.iloc[0] if in_pref else np.nan, p_pref=pr.p.iloc[0] if in_pref else np.nan))
EBA = pd.DataFrame(eba)
EBA["p_bonf_K"] = np.minimum(1, EBA.p_pref * EBA.K_modelos)
# Holm con K propio: ordenado por p ascendente entre los términos del preferido
ip = EBA[EBA.en_preferido].sort_values("p_pref")
run, hol = 0.0, {}
for rnk, (ii, r) in enumerate(ip.iterrows()):
    run = max(run, min(1.0, r.p_pref * max(r.K_modelos - rnk, 1)))
    hol[ii] = run
EBA["p_holm_K"] = pd.Series(hol)
EBA["robusto_EBA(Leamer no cruza 0)"] = (EBA.Leamer_inf > 0) | (EBA.Leamer_sup < 0)
save(EBA, "busqueda_eba", ".4g", index=False)

# -- bootstrap de la selección (bloques móviles 8, B=999) sobre R2 ajustado
rng = np.random.default_rng(SEED)
B, BL = 999, 8
nblk = int(np.ceil(N / BL))
win_cnt = np.zeros(NM)
term_cnt = {t: 0 for t in terms_all}
term_coef = {t: [] for t in terms_all}
for bsi in range(B):
    st = rng.integers(0, N - BL + 1, nblk)
    idx = np.concatenate([np.arange(s, s + BL) for s in st])[:N]
    Mb, yb = M[idx], y[idx]
    Gb, gb = Mb.T @ Mb, Mb.T @ yb
    tss = ((yb - yb.mean()) ** 2).sum()
    yy = yb @ yb
    best, bi, bb = -np.inf, -1, None
    for i, ix in enumerate(mix):
        try:
            b = np.linalg.solve(Gb[np.ix_(ix, ix)], gb[ix])
        except np.linalg.LinAlgError:
            continue
        rs = yy - b @ gb[ix]
        r2a = 1 - (rs / (N - len(ix))) / (tss / (N - 1))
        if r2a > best:
            best, bi, bb = r2a, i, b
    win_cnt[bi] += 1
    names = [COLS[j] for j in mix[bi]]
    for nme, cf in zip(names, bb):
        if nme in term_cnt:
            term_cnt[nme] += 1
            term_coef[nme].append(cf)
brow = []
for t in terms_all:
    a = np.array(term_coef[t])
    brow.append(dict(termino=t, frec_en_ganador=term_cnt[t] / B,
                     coef_post_med=np.median(a) if len(a) else np.nan,
                     IC95_inf=np.percentile(a, 2.5) if len(a) > 20 else np.nan,
                     IC95_sup=np.percentile(a, 97.5) if len(a) > 20 else np.nan,
                     n_rep_condicional=len(a)))
BOOT = pd.DataFrame(brow)
save(BOOT, "busqueda_bootstrap", ".4g", index=False)
freq_pref = win_cnt[PREF] / B
top = np.argsort(-win_cnt)[:5]
BOOTWIN = pd.DataFrame({"modelo": [S.id[i] for i in top], "terminos": [S.terminos[i] for i in top],
                        "frec_ganador": win_cnt[top] / B})
save(BOOTWIN, "busqueda_bootstrap_ganadores", ".4g", index=False)

win = pd.DataFrame({"criterio": ["R2 ajustado (principal)", "AIC", "BIC", "RMSE OOS", "vacío (ect+dummies)"],
                    "id": [S.id[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "terminos": [S.terminos[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "N": [S.N[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "R2_aj": [S.r2_adj[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "AIC": [S.aic[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "BIC": [S.bic[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)],
                    "RMSE_OOS": [S.rmse_oos[i] for i in (i_r2, i_aic, i_bic, i_rm, i_empty)]})
save(win, "busqueda_ganadores", ".5g", index=False)

# -- OOS y DM
def rm(e):
    return float(np.sqrt(np.mean(np.asarray(e) ** 2)))


oos_models = {"Preferido (R2aj)": err[i_r2], "Ganador BIC": err[i_bic], "Ganador AIC": err[i_aic],
              "Mejor RMSE OOS": err[i_rm], "Vacío (ect+q)": err[i_empty]}
orows = []
for nme, e in list(oos_models.items()):
    r = {"modelo": nme, "RMSE": rm(e), "n_oos": len(e)}
    for bn, be in bench.items():
        d = dm_test(e, be, 1)
        r[f"DM vs {bn}"] = d["DM"]
        r[f"p vs {bn}"] = d["p"]
    orows.append(r)
for bn, be in bench.items():
    orows.append({"modelo": "[ref] " + bn, "RMSE": rm(be), "n_oos": len(be)})
OOS = pd.DataFrame(orows)
save(OOS, "oos_dm", ".4g", index=False)

# =============================================================== registro de la búsqueda en resumen
Ntot_search = NM
sec("5. Búsqueda de corto plazo (conjunto CERRADO, declarado antes de resultados)",
    "**Siempre**: ect(t−1) del DOLS preferido (vector base con dummies trimestrales) + q2,q3,q4. **Candidatos** "
    "(cada variable con a lo sumo uno de sus retardos): d_ln_ocupados {0,1}; d_tipo_hip {0,1}; "
    "d_ln_permisos {t−4}; d_ln_costes {0}; d_ln_renta_hog_real {0}; inmigración {ninguna, d_ln_pob_extranj, "
    "d4_ln_pob_extranj/4, d_ln_pob_total} (alternativas excluyentes: nunca stock extranjero y población total a la vez); "
    "d_ln_ipv {1, 4}; d_ln_credito_nuevo {0}. Total de modelos enumerados: **" + str(Ntot_search) +
    f"** (más los modelos de réplica/LR/robustez/precio real del registro; el total final está en la cabecera). "
    f"Muestra común: {C.index[0]}-{C.index[-1]}, **N={N}** (límite: d_ln_ipv(t−4)). "
    "Criterio principal: R² ajustado (como el punto de partida), corregido por la búsqueda (Bonferroni con K = "
    "modelos que contienen el término y bootstrap de la selección). También se reportan AIC y BIC. "
    "Asociaciones, no causalidad.\n\n**Ganadores (misma muestra)**\n\n" + tm(win, ".5g", False) +
    "\n**Correlación stock extranjeros vs población total**\n\n" + tm(corr_pob, ".3f", False) +
    "\n**EBA y Bonferroni/Holm (K = nº de modelos con el término)**\n\n" + tm(EBA.drop(columns=["en_preferido"]), ".3g", False) +
    f"\n**Bootstrap de la selección** (bloques móviles de 8, B=999, semilla {SEED}; se re-ejecuta TODA la búsqueda "
    "en cada réplica por R² aj; el ect se mantiene fijo, es regresor generado: limitación). El modelo preferido "
    f"original vuelve a ser ganador en {freq_pref:.1%} de las réplicas.\n\n" + tm(BOOT, ".3g", False) +
    "\nModelos más frecuentes como ganadores:\n\n" + tm(BOOTWIN, ".3g", False))

sec("5b. Fuera de muestra",
    f"Ventana expansiva, 1 paso, {orig[0]}-{orig[-1]} ({len(orig)} predicciones). En cada origen el LARGO PLAZO "
    "(DOLS y ect) se re-estima solo con datos hasta t−1 (los adelantos obligan a terminar la muestra del DOLS en t−3); "
    "los regresores contemporáneos del ECM se toman observados (predicción condicional). Referencias: AR(4)+dummies, "
    "media histórica expansiva de d_ln_ipv y paseo con deriva (deriva = media de los últimos 20 trimestres; con deriva "
    "estimada en ventana expansiva coincidiría con la media histórica). DM: HAC(h−1=0) con corrección HLN; DM<0 favorece al modelo.\n\n"
    "**Salvedades.** (i) La especificación preferida (y los ganadores AIC/BIC) se eligió con la muestra COMPLETA, "
    "incluidos 2018-2026: la selección no es en tiempo real y el OOS es pseudo-OOS (favorece al modelo). "
    "(ii) La fila «Mejor RMSE OOS» se elige con los propios errores fuera de muestra: es un óptimo ex post, no evidencia "
    "predictiva. (iii) Crédito y empleo contemporáneos entran observados (predicción condicional sobre regresores simultáneos). "
    "(iv) Resultado: el preferido NO mejora al AR(4)+dummies ni al paseo con deriva (DM no significativos); solo bate a la media histórica.\n\n"
    + tm(OOS, ".4g", False))

# =============================================================== 6. diagnósticos
terms_pref = [t for t in S.terminos[PREF].split(" + ") if t != "(vacío)"]
form_pref = "d_ln_ipv ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in terms_pref)
res_pref = ols_hac(form_pref, C)
res_pref_tab = tabla(res_pref)
save(res_pref_tab, "ecm_preferido", ".4g")
diag = {}
diag["Réplica ECM sin q"] = diagnostics(ecm_sin)
diag["Réplica ECM con q"] = diagnostics(ecm_con)
diag["Réplica LR estático"] = diagnostics(lr_rep)
diag["Preferido (R2aj)"] = diagnostics(res_pref)
for lab, i in [("Ganador BIC", i_bic), ("Ganador AIC", i_aic)]:
    tt = [t for t in S.terminos[i].split(" + ") if t != "(vacío)"]
    diag[lab] = diagnostics(ols_hac("d_ln_ipv ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in tt), C))
diag["DOLS base (LR)"] = diagnostics(beta_pref["res"])

# BG: añadir retardos de d_ln_ipv
aug_rows, cur_terms = [], list(terms_pref)
bg0 = diag["Preferido (R2aj)"]["BG4_p"]
aug_rows.append(dict(paso="preferido", terminos_extra="", BG4_p=bg0, DW=diag["Preferido (R2aj)"]["DW"]))
res_aug = res_pref
form_aug = form_pref
if bg0 < .05:
    for k in range(1, 5):
        nm = f"d_ln_ipv_l{k}"
        if nm in cur_terms or (k in (1, 4) and any(t.startswith("d_ln_ipv_l") for t in cur_terms) and False):
            continue
        cur_terms.append(nm)
        f_ = "d_ln_ipv ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in cur_terms)
        r_ = ols_hac(f_, C)
        d_ = diagnostics(r_)
        aug_rows.append(dict(paso=f"+{nm}", terminos_extra=nm, BG4_p=d_["BG4_p"], DW=d_["DW"]))
        res_aug, form_aug = r_, f_
        REG.log_res("F2", f"aug_BG_{k}", f_, r_, "ect_l1", notas="añade retardos de d_ln_ipv por BG")
        if d_["BG4_p"] >= .05:
            break
    diag["Preferido + retardos (BG)"] = diagnostics(res_aug)
AUG = pd.DataFrame(aug_rows)
save(AUG, "bg_aumentado", ".4g", index=False)
res_aug_tab = tabla(res_aug)
save(res_aug_tab, "ecm_aumentado", ".4g")

# Chow
ch = pd.DataFrame([chow(C, form_pref, f) for f in ["2014Q1", "2020Q1", "2022Q3"]])
save(ch, "chow", ".4g", index=False)

# Bai-Perron (ECM y LR) sobre datos con dummies trimestrales partialled out
def partial(dfq, cols, ycol):
    Zq = sm.add_constant(dfq[Q])
    out = {}
    for c in [ycol] + cols:
        out[c] = sm.OLS(dfq[c], Zq).fit().resid
    return pd.DataFrame(out)


bp_rows = []
Pp = partial(C, ["ect_l1"] + terms_pref, "d_ln_ipv")
bp_ecm = bai_perron(Pp["d_ln_ipv"], sm.add_constant(Pp.drop(columns="d_ln_ipv")), 3, 12)
bp_rows.append(dict(ecuacion="ECM preferido", N=len(Pp), n_quiebres=bp_ecm["n_bkps"], fechas=", ".join(bp_ecm["fechas"]),
                    bic=str({k: round(v, 1) for k, v in bp_ecm["bic"].items()})))
Dl = common_sample(Fw.loc[S0:S1], ["ln_ipv"] + BASE)
Pl = partial(Dl, BASE, "ln_ipv")
bp_lr = bai_perron(Pl["ln_ipv"], sm.add_constant(Pl.drop(columns="ln_ipv")), 3, 12)
bp_rows.append(dict(ecuacion="LR (niveles, DOLS base sin retardos)", N=len(Pl), n_quiebres=bp_lr["n_bkps"],
                    fechas=", ".join(bp_lr["fechas"]), bic=str({k: round(v, 1) for k, v in bp_lr["bic"].items()})))
BP = pd.DataFrame(bp_rows)
save(BP, "bai_perron", ".4g", index=False)

# CUSUM y estabilidad recursiva del ect
ols_pref = sm.OLS(res_pref.model.endog, res_pref.model.exog).fit()
try:
    rc = recursive_olsresiduals(ols_pref)
    cus, ci = np.asarray(rc[5]), np.asarray(rc[6])
    fechas = C.index[len(C) - len(cus):].to_timestamp()
    ci = ci[:, -len(cus):] if ci.shape[1] >= len(cus) else ci
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(fechas, cus, label="CUSUM")
    ci = ci if ci.shape[0] == 2 else ci.T
    ci = np.column_stack([ci, ci[:, -1:]]) if ci.shape[1] < len(cus) else ci
    ax.plot(fechas, ci[0], "r--", lw=1)
    ax.plot(fechas, ci[1], "r--", lw=1, label="banda 5 %")
    ax.axhline(0, color="k", lw=.5)
    ax.set_title("CUSUM de residuos recursivos - ECM preferido")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "cusum.png", dpi=130)
    plt.close(fig)
except Exception as e:
    print("CUSUM fig error", e)
Xp = res_pref.model.exog
yp = res_pref.model.endog
j_ect = list(res_pref.model.exog_names).index("ect_l1")
rec = []
for t in range(Xp.shape[1] + 10, len(yp) + 1):
    r = sm.OLS(yp[:t], Xp[:t]).fit()
    rec.append(dict(hasta=str(C.index[t - 1]), n=t, coef_ect=r.params[j_ect], se=r.bse[j_ect]))
REC = pd.DataFrame(rec)
save(REC, "ect_recursivo", ".4g", index=False)
fig, ax = plt.subplots(figsize=(8, 4))
xs_ = pd.PeriodIndex(REC.hasta, freq="Q").to_timestamp()
ax.plot(xs_, REC.coef_ect)
ax.fill_between(xs_, REC.coef_ect - 2 * REC.se, REC.coef_ect + 2 * REC.se, alpha=.25)
ax.axhline(0, color="k", lw=.5)
ax.set_title("Coeficiente del ect(t-1): estimación recursiva (±2 EE MCO)")
fig.tight_layout()
fig.savefig(OUT / "ect_recursivo.png", dpi=130)
plt.close(fig)

# Robustez: escalones, dummies EPA / tipos 2022, pre-COVID
rob = {}
Cx = C.copy()
bp_all = sorted(set(bp_ecm["fechas"]) | set(bp_lr["fechas"]))
for f in bp_all:
    Cx[f"esc_{f}"] = (C.index >= P(f, "Q")).astype(float)
steps = [f"esc_{f}" for f in bp_all]
rob_forms = {
    "Preferido": form_pref,
    "+ epa21 + tipo22 (escalones)": form_pref + " + epa21 + tipo22",
}
if steps:
    rob_forms["+ escalones Bai-Perron (ECM y LR)"] = form_pref + "".join(" + " + s for s in steps)
rrows = []
for lab, f in rob_forms.items():
    r = ols_hac(f, Cx)
    d_ = diagnostics(r)
    rrows.append(dict(modelo=lab, N=int(r.nobs), ect=fmt(r.params["ect_l1"], r.bse["ect_l1"]), p_ect=r.pvalues["ect_l1"],
                      R2_aj=r.rsquared_adj, BG4_p=d_["BG4_p"], BP_p=d_["BP_p"], JB_p=d_["JB_p"], RESET_p=d_["RESET_p"],
                      extras="; ".join(f"{k}={fmt(r.params[k], r.bse[k])}" for k in r.params.index if k in ["epa21", "tipo22"] + steps)))
    REG.log_res("F2", "rob_" + lab.split()[0] + str(len(rrows)), f, r, "ect_l1", notas="robustez quiebres")
# pre-COVID: DOLS y ect re-estimados con datos <=2019Q4
dpc = build_ect(Fw, "2019Q4")
Fpc = Fw.loc[:"2019Q4"].copy()
Fpc["ect_l1"] = dpc["ect"].shift(1)
Cpc = common_sample(Fpc.loc[S0:"2019Q4"], need)
f_pc = form_pref
r_pc = ols_hac(f_pc, Cpc)
d_pc = diagnostics(r_pc)
rrows.append(dict(modelo="Pre-COVID (hasta 2019Q4; ect re-estimado)", N=int(r_pc.nobs),
                  ect=fmt(r_pc.params["ect_l1"], r_pc.bse["ect_l1"]), p_ect=r_pc.pvalues["ect_l1"], R2_aj=r_pc.rsquared_adj,
                  BG4_p=d_pc["BG4_p"], BP_p=d_pc["BP_p"], JB_p=d_pc["JB_p"], RESET_p=d_pc["RESET_p"],
                  extras="LR pre-COVID: " + "; ".join(f"{k}={dpc['beta'][k]:.3f}" for k in BASE)))
REG.log_res("F2", "rob_preCOVID", f_pc, r_pc, "ect_l1", notas="muestra termina 2019Q4 (excluye shock COVID)")
ROB = pd.DataFrame(rrows)
save(ROB, "robustez_quiebres", ".4g", index=False)
pcf = pd.DataFrame({"coef": r_pc.params, "EE_HAC": r_pc.bse, "p": r_pc.pvalues})
save(pcf, "ecm_precovid", ".4g")
diag["Preferido pre-COVID"] = diagnostics(r_pc)
DG = pd.DataFrame(diag).T
save(DG, "diagnosticos", ".3g")

# =============================================================== extras de la puerta F2 (iteración 1)
# (a) DOLS por subperíodos (k=1 por escasez de grados de libertad) y EG estático por subperíodos
sub_rows = []
for lab, a_, b_ in [("2008Q1-2025Q4", "2008Q1", "2025Q4"), ("2008Q1-2019Q4 (pre-COVID)", "2008Q1", "2019Q4"),
                    ("2012Q1-2025Q4 (tras quiebre BP 2012Q1)", "2012Q1", "2025Q4"),
                    ("2014Q1-2025Q4", "2014Q1", "2025Q4")]:
    dd_ = dols(Fw.loc[:b_], "ln_ipv", BASE, Q, k=1, desde=a_)
    es_ = ols_hac("ln_ipv ~ " + " + ".join(BASE) + " + q2+q3+q4", common_sample(Fw.loc[a_:b_], ["ln_ipv"] + BASE))
    for x in BASE:
        sub_rows.append(dict(subperiodo=lab, var=x, DOLS_k1=fmt(dd_["beta"][x], dd_["res"].bse[x]), N_DOLS=dd_["n"],
                             EG_q=fmt(es_.params[x], es_.bse[x]), N_EG=int(es_.nobs)))
SUB = pd.DataFrame(sub_rows)
save(SUB, "dols_subperiodos", ".4g", index=False)

# (b) crédito: comovimiento/simultaneidad (fuera de la K de búsqueda)
Cr = C.copy()
Cr["d_ln_credito_nuevo_l1"] = Fw["d_ln_credito_nuevo"].shift(1).reindex(C.index)
cr_rows = []
for lab, i in [("Preferido R2aj", PREF), ("Ganador BIC/AIC", i_bic)]:
    tt = [t for t in S.terminos[i].split(" + ") if t != "(vacío)"]
    variants = {"base (crédito t)": tt,
                "crédito en t−1": [("d_ln_credito_nuevo_l1" if t == "d_ln_credito_nuevo" else t) for t in tt],
                "sin crédito": [t for t in tt if t != "d_ln_credito_nuevo"]}
    for vl, tv in variants.items():
        f_ = "d_ln_ipv ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in tv)
        r_ = ols_hac(f_, Cr)
        d_ = diagnostics(r_)
        REG.log_res("F2", f"rob_cred_{lab.split()[0]}_{vl.split()[0]}_{vl[-3:].strip()}", f_, r_, "ect_l1",
                    notas="robustez simultaneidad del crédito (fuera de la K de búsqueda)")
        row = dict(modelo=lab, variante=vl, N=int(r_.nobs), R2_aj=r_.rsquared_adj, BG4_p=d_["BG4_p"])
        for t in ["ect_l1", "d_ln_ocupados", "d_ln_ipv_l1", "d_ln_credito_nuevo", "d_ln_credito_nuevo_l1", "d_ln_costes",
                  "d_ln_renta_hog_real"]:
            if t in r_.params.index:
                row[t] = f"{fmt(r_.params[t], r_.bse[t])} p={r_.pvalues[t]:.3f}"
        cr_rows.append(row)
CR = pd.DataFrame(cr_rows).fillna("")
save(CR, "robustez_credito", ".4g", index=False)

# (c) estabilidad del ECM preferido por muestra: completa, desde 2014Q1, pre-COVID
C14 = C.loc["2014Q1":]
r14 = ols_hac(form_pref, C14)
REG.log_res("F2", "rob_2014+", form_pref, r14, "ect_l1", notas="ECM preferido 2014Q1-2026Q2 (ect de la muestra completa)")
st_rows = []
for lab, r_ in [("2008Q2-2026Q2 (completa)", res_pref), ("2014Q1-2026Q2", r14), ("2008Q2-2019Q4 (pre-COVID, ect reest.)", r_pc)]:
    st_rows.append(dict(muestra=lab, N=int(r_.nobs), R2_aj=r_.rsquared_adj,
                        **{t: f"{fmt(r_.params[t], r_.bse[t])}" for t in ["ect_l1"] + terms_pref}))
STB = pd.DataFrame(st_rows)
save(STB, "estabilidad_muestras", ".4g", index=False)

# (d) tabla de signos frente a literatura
lrt = lr_tab.copy()
eb = EBA.set_index("termino")


def lrv(met, var):
    r = lrt[(lrt.metodo == met) & (lrt["var"] == var)]
    return (r.coef.iloc[0], r.EE_HAC.iloc[0], r.p.iloc[0]) if len(r) else (np.nan,) * 3


def sgn(v):
    return "+" if v > 0 else "-"


ocup_lr = lrt[(lrt["var"] == "ln_ocupados") & (~lrt.metodo.str.startswith("UECM"))]
sg = []
for var, esp, etiqueta in [("ln_ocupados", "+", "Empleo (LP)"), ("tipo_hip", "-", "Tipo hipotecario (LP)"),
                           ("ln_permisos_l4", "-", "Permisos t−4 (LP)"), ("ln_costes", "+", "Costes construcción (LP)")]:
    d1, d2, d3 = lrv("DOLS base (+q)", var), lrv("EG estático (+q)", var), lrv("UECM implícito (delta, HAC)", var)
    vals = [d1[0], d2[0], d3[0]]
    disc = "" if all(sgn(v) == esp for v in vals if v == v) else "DISCREPANCIA de signo en algún estimador"
    if var == "ln_ocupados":
        disc = (f"signo OK; magnitud NO robusta: rango {ocup_lr.coef.min():.2f}-{ocup_lr.coef.max():.2f} según estimador/vector; "
                "literatura.md no da magnitud de referencia")
    sg.append(dict(variable=etiqueta, esperado=esp, DOLS=fmt(d1[0], d1[1]), EG_q=fmt(d2[0], d2[1]),
                   UECM=fmt(d3[0], d3[1]) if d3[0] == d3[0] else "n.d.", discrepancia=disc))
for var, esp, etiqueta, met in [("ln_renta_hog_real", "+", "Renta real (LP)", "DOLS +renta"),
                                ("ln_pob_extranj", "+", "Pob. extranjera (LP)", "DOLS +pob_extranj")]:
    d1 = lrv(met, var)
    sg.append(dict(variable=etiqueta, esperado=esp, DOLS=fmt(d1[0], d1[1]), EG_q="", UECM="",
                   discrepancia="" if sgn(d1[0]) == esp else "DISCREPANCIA de signo"))
SGL = pd.DataFrame(sg)
cp = []
for t, esp, etiqueta in [("d_ln_ocupados", "+", "Empleo (CP)"), ("d_tipo_hip", "-", "Tipo (CP)"),
                         ("d_ln_permisos_l4", "-", "Permisos t−4 (CP)"), ("d_ln_costes", "+", "Costes (CP)"),
                         ("d_ln_renta_hog_real", "+", "Renta (CP)"), ("d_ln_credito_nuevo", "+", "Crédito (CP, comovimiento)"),
                         ("d_ln_pob_extranj", "+", "Pob. extranjera (CP)"), ("ect_l1", "-", "ect (entre −1 y 0)")]:
    e = eb.loc[t]
    inpref = bool(e.en_preferido)
    pos = e.signo_pos
    maj = "+" if pos >= .5 else "-"
    c_ = f"{e.coef_pref:.4f} (p={e.p_pref:.3f})" if inpref else "no incluido"
    disc = ""
    if inpref and sgn(e.coef_pref) != esp:
        disc = "DISCREPANCIA de signo en el preferido"
    elif not inpref and maj != esp:
        disc = "DISCREPANCIA: signo mayoritario en la búsqueda contrario"
    cp.append(dict(variable=etiqueta, esperado=esp, preferido=c_, pct_modelos_signo_pos=f"{pos:.0%}",
                   frac_signif=f"{e.frac_signif_5pct:.0%}", discrepancia=disc))
SGC = pd.DataFrame(cp)
save(SGL, "signos_LP", ".4g", index=False)
save(SGC, "signos_CP", ".4g", index=False)

# =============================================================== resumen
pref_tab = res_pref_tab.copy()
pref_tab["p_Bonf(K)"] = [eb.p_bonf_K.get(i, np.nan) for i in pref_tab.index]
pref_tab["K"] = [eb.K_modelos.get(i, np.nan) for i in pref_tab.index]
sec("6. Diagnósticos", "Contrastes sobre MCO clásico (los EE de los coeficientes son HAC). DW, BG(4) p, BP p, JB p, "
    "RESET p (potencias 2-3), CUSUM p, VIF máx (sin dummies q).\n\n" + tm(DG, ".3g") +
    "\n**Breusch-Godfrey: añadir retardos de d_ln_ipv (preferido)**\n\n" + tm(AUG, ".4g", False) +
    "\n(La versión pre-COVID sí rechaza BG(4), p=%.3f; no se ha aplicado el aumento de retardos allí.)\n" % d_pc["BG4_p"])

chow_txt = "; ".join(f"{r.fecha}: F={r.F:.2f}, p={r.p:.3f}" for r in ch.itertuples())
sec("6b. Quiebres y estabilidad (P5: 2008, 2014, 2020, 2022)",
    "**Chow (ECM preferido)**\n\n" + tm(ch, ".4g", False) + "\n**Bai-Perron (min 12, máx 3, BIC; dummies q eliminadas por partialling)**\n\n"
    + tm(BP, ".4g", False) +
    "\n**Estabilidad del ECM preferido por muestras**\n\n" + tm(STB, ".4g", False) +
    "\n**Robustez: escalones y pre-COVID**\n\n" + tm(ROB, ".4g", False) +
    "\n**DOLS / EG por subperíodos** (DOLS ±1 por grados de libertad)\n\n" + tm(SUB, ".4g", False) +
    "\nFiguras: output/f2/cusum.png (CUSUM, p=%.3f) y output/f2/ect_recursivo.png (ect recursivo).\n\n" % diag["Preferido (R2aj)"]["CUSUM_p"] +
    "**Lectura por fecha (asociaciones, no causalidad):**\n"
    "- **2008:** la muestra del IPV empieza en 2007Q1 y la del modelo en 2008Q1/Q2, de modo que el quiebre de la crisis financiera no es contrastable con un Chow dentro de la muestra; no hay conclusión.\n"
    f"- **2014Q1:** el Chow rechaza la estabilidad del ECM preferido ({ch.iloc[0].F:.2f}, p={ch.iloc[0].p:.3f}); Bai-Perron por BIC no encuentra quiebres en el ECM (el BIC es conservador). "
    "La estimación desde 2014Q1 (tabla de estabilidad) permite ver cuánto cambian ect y coeficientes. Es evidencia de inestabilidad moderada, con tramo previo de solo 23 observaciones.\n"
    f"- **2020Q1:** Chow p={ch.iloc[1].p:.3f} (no rechaza). Sin embargo, el LR cambia mucho al excluir 2020-2026 (pre-COVID: costes y permisos cambian de signo) y Bai-Perron en niveles fecha un quiebre en 2020Q2.\n"
    f"- **2022Q3 (subida de tipos):** Chow p={ch.iloc[2].p:.3f} (no rechaza, 16 obs. en el segundo tramo: baja potencia); el escalón tipo22 en el ECM no es significativo (ver robustez).\n"
    "- **Estabilidad global:** CUSUM no rechaza en el ECM; el LR (niveles) no es estable (Bai-Perron: 2012Q1, 2020Q2, 2023Q2; CUSUM del DOLS p=%.3f; DW=0,71). El coeficiente del ect cae a −0,05 en pre-COVID.\n\n" % diag["DOLS base (LR)"]["CUSUM_p"] +
    "Los escalones se usan solo como robustez (en una ecuación en diferencias un escalón es un cambio de deriva; "
    "`epa21`=0,0078 en el ECM debe leerse como «cambio de deriva desde 2021», no como corrección del salto de la EPA; un impulso en 2021Q1 no cambia nada según la revisión).\n")
sec("6c. Crédito nuevo: comovimiento y simultaneidad (robustez, fuera de la K de búsqueda)",
    "El volumen de crédito nuevo es operaciones × importe medio, y el importe depende del precio: la asociación contemporánea "
    "con el IPV es un comovimiento/simultaneidad, no un determinante predeterminado. Se reestima el preferido y el ganador "
    "AIC/BIC con crédito en t−1 y sin crédito (misma muestra N=73).\n\n" + tm(CR, ".4g", False) +
    "\nLas otras variables cambian como muestra la tabla (compárese ect, ocupados y d_ln_ipv_l1 entre variantes).\n")
sec("6d. Signos y magnitudes frente a docs/literatura.md",
    "**Largo plazo**\n\n" + tm(SGL, ".4g", False) + "\n**Corto plazo (preferido y búsqueda)**\n\n" + tm(SGC, ".4g", False) +
    "\nLa elasticidad del precio al empleo no tiene magnitud de referencia en literatura.md. Los signos contrarios de "
    "permisos (+) y de costes/renta en el CP son compatibles con causalidad inversa o colinealidad y no se interpretan como efecto de oferta.\n")

# =============================================================== 8. ECUACIÓN EN PRECIO REAL (condición de la re-revisión)
# Vector real = el MISMO que dio 3/3 en el test de cointegración: y = ln_ipv_real (= ln_ipv − ln_deflactor);
# X = ln_ocupados, tipo_hip_real (= tipo_hip − inflación del deflactor), ln_permisos_l4, ln_costes_real (= ln_costes − ln_deflactor).
BASE_R = ["ln_ocupados", "tipo_hip_real", "ln_permisos_l4", "ln_costes_real"]
FwR = Fw.copy()
for k_ in range(1, 5):
    FwR[f"d_ln_ipv_real_l{k_}"] = FwR["d_ln_ipv_real"].shift(k_)
dolR = dols(FwR.loc[:S1], "ln_ipv_real", BASE_R, Q, k=2, desde=S0)
ciR = dolR["res"].conf_int()
FwR["ect_l1"] = dolR["ect"].shift(1)
REG.log("F2", "real_DOLS", "DOLS±2: ln_ipv_real ~ " + "+".join(BASE_R), dolR["res"].model.data.row_labels[0],
        dolR["res"].model.data.row_labels[-1], dolR["n"], dolR["res"].rsquared_adj, dolR["res"].aic, dolR["res"].bic,
        coef_interes=dolR["res"].params["ln_ocupados"], p_interes=dolR["res"].pvalues["ln_ocupados"], notas="LR precio real")
GR = {k_: list(v) for k_, v in GROUPS.items()}
GR["ipv"] = [None, "d_ln_ipv_real_l1", "d_ln_ipv_real_l4"]
CAND_R = [c for g in GR.values() for c in g if c]
COLS_R = ["const"] + Q + ["ect_l1"] + CAND_R
needR = ["d_ln_ipv_real", "ect_l1"] + CAND_R + Q
CR_ = common_sample(FwR.loc[S0:S1], needR)
NR = len(CR_)
yR = CR_["d_ln_ipv_real"].values
MR = np.column_stack([np.ones(NR)] + [CR_[c].values for c in COLS_R[1:]])
cixR = {c: i for i, c in enumerate(COLS_R)}
MODR = [tuple(t for t in m if t) for m in itertools.product(*GR.values())]
mixR = [[0, 1, 2, 3, 4] + [cixR[t] for t in m] for m in MODR]
NMR = len(MODR)
origR = [p_ for p_ in CR_.index if p_ >= P("2018Q1", "Q")]
ER = {T: build_ect(FwR, str(T - 1), BASE_R, Q, "ln_ipv_real")["ect"].reindex(FwR.index).shift(1).reindex(CR_.index).values
      for T in origR}
errR = np.full((NMR, len(origR)), np.nan)
benchR = {k_: np.full(len(origR), np.nan) for k_ in ["AR4+q", "media historica", "paseo con deriva (20T)"]}
XarR = np.column_stack([np.ones(NR)] + [CR_[c].values for c in Q] + [CR_[f"d_ln_ipv_real_l{k_}"].values for k_ in range(1, 5)])
for j, T in enumerate(origR):
    Mo = MR.copy()
    Mo[:, 4] = ER[T]
    tr = np.where(CR_.index < T)[0]
    te = int(np.where(CR_.index == T)[0][0])
    G, g = Mo[tr].T @ Mo[tr], Mo[tr].T @ yR[tr]
    for i, ix in enumerate(mixR):
        errR[i, j] = yR[te] - Mo[te, ix] @ np.linalg.solve(G[np.ix_(ix, ix)], g[ix])
    b = np.linalg.lstsq(XarR[tr], yR[tr], rcond=None)[0]
    benchR["AR4+q"][j] = yR[te] - XarR[te] @ b
    benchR["media historica"][j] = yR[te] - yR[tr].mean()
    benchR["paseo con deriva (20T)"][j] = yR[te] - yR[tr][-20:].mean()
rmseR = np.sqrt(np.nanmean(errR ** 2, axis=1))
srR, cfR = [], []
for i, m in enumerate(MODR):
    cols = ["ect_l1"] + Q + list(m)
    Xd = sm.add_constant(CR_[cols])
    r = sm.OLS(CR_["d_ln_ipv_real"], Xd).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    r0 = sm.OLS(CR_["d_ln_ipv_real"], Xd).fit()
    mid = f"real_busq_{i + 1:04d}"
    srR.append(dict(id=mid, terminos=" + ".join(m) if m else "(vacío)", N=int(r.nobs), r2_adj=r0.rsquared_adj, aic=r0.aic,
                    bic=r0.bic, rmse_oos=rmseR[i], ect=r.params["ect_l1"], ect_p=r.pvalues["ect_l1"]))
    for c in ["ect_l1"] + list(m):
        cfR.append(dict(id=mid, term=c, coef=r.params[c], se=r.bse[c], p=r.pvalues[c]))
    REG.log("F2", mid, "d_ln_ipv_real ~ ect_l1 + q2+q3+q4" + "".join(" + " + t for t in m), CR_.index[0], CR_.index[-1],
            int(r.nobs), r0.rsquared_adj, r0.aic, r0.bic, rmseR[i], r.params["ect_l1"], r.pvalues["ect_l1"],
            "búsqueda CP precio real; coef de interés = ect(t-1)")
SR, CFR = pd.DataFrame(srR), pd.DataFrame(cfR)
SR.to_csv(OUT / "real_busqueda_modelos.csv", index=False)
CFR.to_csv(OUT / "real_busqueda_coefs.csv", index=False)
jr2, jaic, jbic, jrm = int(SR.r2_adj.idxmax()), int(SR.aic.idxmin()), int(SR.bic.idxmin()), int(SR.rmse_oos.idxmin())
jemp = int(SR.index[SR.terminos == "(vacío)"][0])
PR = jr2
ebaR = []
termsR = ["ect_l1"] + CAND_R
for t in termsR:
    sub = CFR[CFR.term == t]
    pr_ = CFR[(CFR.id == SR.id[PR]) & (CFR.term == t)]
    ip_ = len(pr_) > 0
    ebaR.append(dict(termino=t, K_modelos=len(sub), frac_signif_5pct=(sub.p < .05).mean(), signo_pos=(sub.coef > 0).mean(),
                     coef_min=sub.coef.min(), coef_max=sub.coef.max(), Leamer_inf=(sub.coef - 2 * sub.se).min(),
                     Leamer_sup=(sub.coef + 2 * sub.se).max(), en_preferido=ip_,
                     coef_pref=pr_.coef.iloc[0] if ip_ else np.nan, EE_pref=pr_.se.iloc[0] if ip_ else np.nan,
                     p_pref=pr_.p.iloc[0] if ip_ else np.nan))
EBAR = pd.DataFrame(ebaR)
EBAR["p_bonf_K"] = np.minimum(1, EBAR.p_pref * EBAR.K_modelos)
save(EBAR, "real_busqueda_eba", ".4g", index=False)
# bootstrap de la selección
rngR = np.random.default_rng(SEED)
winR = np.zeros(NMR)
tcR = {t: 0 for t in termsR}
tcoR = {t: [] for t in termsR}
for _ in range(999):
    st = rngR.integers(0, NR - 8 + 1, int(np.ceil(NR / 8)))
    idx = np.concatenate([np.arange(s_, s_ + 8) for s_ in st])[:NR]
    Mb, yb = MR[idx], yR[idx]
    Gb, gb = Mb.T @ Mb, Mb.T @ yb
    tss, yy = ((yb - yb.mean()) ** 2).sum(), yb @ yb
    best, bi, bb = -np.inf, -1, None
    for i, ix in enumerate(mixR):
        try:
            b = np.linalg.solve(Gb[np.ix_(ix, ix)], gb[ix])
        except np.linalg.LinAlgError:
            continue
        r2a = 1 - ((yy - b @ gb[ix]) / (NR - len(ix))) / (tss / (NR - 1))
        if r2a > best:
            best, bi, bb = r2a, i, b
    winR[bi] += 1
    for nme, cf in zip([COLS_R[j] for j in mixR[bi]], bb):
        if nme in tcR:
            tcR[nme] += 1
            tcoR[nme].append(cf)
BOOTR = pd.DataFrame([dict(termino=t, frec_en_ganador=tcR[t] / 999, coef_post_med=np.median(tcoR[t]) if tcoR[t] else np.nan,
                           IC95_inf=np.percentile(tcoR[t], 2.5) if len(tcoR[t]) > 20 else np.nan,
                           IC95_sup=np.percentile(tcoR[t], 97.5) if len(tcoR[t]) > 20 else np.nan) for t in termsR])
save(BOOTR, "real_busqueda_bootstrap", ".4g", index=False)
freqR = winR[PR] / 999
winTR = pd.DataFrame({"criterio": ["R2 ajustado (principal)", "AIC", "BIC", "RMSE OOS (ex post)", "vacío"],
                      "id": [SR.id[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "terminos": [SR.terminos[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "N": [SR.N[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "R2_aj": [SR.r2_adj[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "AIC": [SR.aic[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "BIC": [SR.bic[i] for i in (jr2, jaic, jbic, jrm, jemp)],
                      "RMSE_OOS": [SR.rmse_oos[i] for i in (jr2, jaic, jbic, jrm, jemp)]})
save(winTR, "real_busqueda_ganadores", ".5g", index=False)
orR = []
for nme, i in [("Preferido (R2aj)", jr2), ("Ganador BIC", jbic), ("Ganador AIC", jaic), ("Mejor RMSE OOS (ex post)", jrm),
               ("Vacío (ect+q)", jemp)]:
    r = {"modelo": nme, "RMSE": rm(errR[i]), "n_oos": errR.shape[1]}
    for bn, be in benchR.items():
        dd_ = dm_test(errR[i], be, 1)
        r[f"DM vs {bn}"], r[f"p vs {bn}"] = dd_["DM"], dd_["p"]
    orR.append(r)
for bn, be in benchR.items():
    orR.append({"modelo": "[ref] " + bn, "RMSE": rm(be), "n_oos": len(be)})
OOSR = pd.DataFrame(orR)
save(OOSR, "real_oos_dm", ".4g", index=False)
# diagnósticos, quiebres, robustez
tR = [t for t in SR.terminos[PR].split(" + ") if t != "(vacío)"]
fR = "d_ln_ipv_real ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in tR)
resR = ols_hac(fR, CR_)
REG.log_res("F2", "real_preferido_refit", fR, resR, "ect_l1", notas="refit del preferido real (no cuenta como modelo nuevo)")
diagR = {"Preferido real (R2aj)": diagnostics(resR)}
for lab, i in [("Ganador BIC real", jbic), ("Ganador AIC real", jaic)]:
    tt = [t for t in SR.terminos[i].split(" + ") if t != "(vacío)"]
    diagR[lab] = diagnostics(ols_hac("d_ln_ipv_real ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in tt), CR_))
diagR["DOLS real (LR)"] = diagnostics(dolR["res"])
augR, curR, resA = [dict(paso="preferido", BG4_p=diagR["Preferido real (R2aj)"]["BG4_p"])], list(tR), resR
if augR[0]["BG4_p"] < .05:
    for k_ in range(1, 5):
        nm = f"d_ln_ipv_real_l{k_}"
        if nm in curR:
            continue
        curR.append(nm)
        f_ = "d_ln_ipv_real ~ ect_l1 + q2 + q3 + q4" + "".join(" + " + t for t in curR)
        resA = ols_hac(f_, CR_)
        augR.append(dict(paso="+" + nm, BG4_p=diagnostics(resA)["BG4_p"]))
        REG.log_res("F2", f"real_aug_BG_{k_}", f_, resA, "ect_l1", notas="añade retardos por BG")
        if augR[-1]["BG4_p"] >= .05:
            break
chR = pd.DataFrame([chow(CR_, fR, f_) for f_ in ["2014Q1", "2020Q1", "2022Q3"]])
save(chR, "real_chow", ".4g", index=False)
PpR = partial(CR_, ["ect_l1"] + tR, "d_ln_ipv_real")
bpR = bai_perron(PpR["d_ln_ipv_real"], sm.add_constant(PpR.drop(columns="d_ln_ipv_real")), 3, 12)
DlR = common_sample(FwR.loc[S0:S1], ["ln_ipv_real"] + BASE_R)
PlR = partial(DlR, BASE_R, "ln_ipv_real")
bpRl = bai_perron(PlR["ln_ipv_real"], sm.add_constant(PlR.drop(columns="ln_ipv_real")), 3, 12)
BPR = pd.DataFrame([dict(ecuacion="ECM real preferido", N=len(PpR), n_quiebres=bpR["n_bkps"], fechas=", ".join(bpR["fechas"])),
                    dict(ecuacion="LR real (niveles)", N=len(PlR), n_quiebres=bpRl["n_bkps"], fechas=", ".join(bpRl["fechas"]))])
save(BPR, "real_bai_perron", ".4g", index=False)
rbR = []
CxR = CR_.copy()
bpa = sorted(set(bpR["fechas"]) | set(bpRl["fechas"]))
for f_ in bpa:
    CxR[f"esc_{f_}"] = (CR_.index >= P(f_, "Q")).astype(float)
forms = {"Preferido real": (fR, CxR), "+ epa21 (quiebre_epa_2021) + tipo22 (escalón 2022Q3)": (fR + " + epa21 + tipo22", CxR),
         "2014Q1-2026Q2": (fR, CxR.loc["2014Q1":])}
if bpa:
    forms["+ escalones Bai-Perron"] = (fR + "".join(f" + esc_{f_}" for f_ in bpa), CxR)
for lab, (f_, d_) in forms.items():
    r_ = ols_hac(f_, d_)
    dg_ = diagnostics(r_)
    REG.log_res("F2", "real_rob_" + str(len(rbR) + 1), f_, r_, "ect_l1", notas="robustez real: " + lab)
    ex_ = "; ".join(f"{k}={fmt(r_.params[k], r_.bse[k])}" for k in r_.params.index if k in ["epa21", "tipo22"] or k.startswith("esc_"))
    rbR.append(dict(modelo=lab, N=int(r_.nobs), ect=fmt(r_.params["ect_l1"], r_.bse["ect_l1"]), p_ect=r_.pvalues["ect_l1"],
                    R2_aj=r_.rsquared_adj, BG4_p=dg_["BG4_p"], BP_p=dg_["BP_p"], JB_p=dg_["JB_p"], RESET_p=dg_["RESET_p"], extras=ex_))
dpcR = build_ect(FwR, "2019Q4", BASE_R, Q, "ln_ipv_real")
Fpc2 = FwR.loc[:"2019Q4"].copy()
Fpc2["ect_l1"] = dpcR["ect"].shift(1)
Cpc2 = common_sample(Fpc2.loc[S0:"2019Q4"], needR)
rpcR = ols_hac(fR, Cpc2)
dgp = diagnostics(rpcR)
REG.log_res("F2", "real_rob_preCOVID", fR, rpcR, "ect_l1", notas="real, muestra hasta 2019Q4 (ect re-estimado)")
rbR.append(dict(modelo="Pre-COVID (≤2019Q4; ect re-estimado)", N=int(rpcR.nobs), ect=fmt(rpcR.params["ect_l1"], rpcR.bse["ect_l1"]),
                p_ect=rpcR.pvalues["ect_l1"], R2_aj=rpcR.rsquared_adj, BG4_p=dgp["BG4_p"], BP_p=dgp["BP_p"], JB_p=dgp["JB_p"],
                RESET_p=dgp["RESET_p"], extras="LR pre-COVID: " + "; ".join(f"{k}={dpcR['beta'][k]:.3f}" for k in BASE_R)))
ROBR = pd.DataFrame(rbR)
save(ROBR, "real_robustez", ".4g", index=False)
DGR = pd.DataFrame(diagR).T
save(DGR, "real_diagnosticos", ".3g")
# tabla final
rowsF = []
rs = dolR["res"]
for x in ["const"] + BASE_R:
    rowsF.append(dict(bloque="LR (DOLS ±2, HAC)", termino=x, coef=rs.params[x], EE_HAC=rs.bse[x], IC95_inf=ciR.loc[x, 0],
                      IC95_sup=ciR.loc[x, 1], p=rs.pvalues[x], p_bonf_K=np.nan, K=np.nan, N=dolR["n"]))
cip = resR.conf_int()
ebR = EBAR.set_index("termino")
for x in ["Intercept", "ect_l1", "q2", "q3", "q4"] + tR:
    rowsF.append(dict(bloque="CP (ECM, preferido R2aj)", termino=x, coef=resR.params[x], EE_HAC=resR.bse[x], IC95_inf=cip.loc[x, 0],
                      IC95_sup=cip.loc[x, 1], p=resR.pvalues[x], p_bonf_K=ebR.p_bonf_K.get(x, np.nan),
                      K=ebR.K_modelos.get(x, np.nan), N=int(resR.nobs)))
ECR = pd.DataFrame(rowsF)
save(ECR, "ecuacion_real", ".4g", index=False)
# comparación nominal-real
cmp = pd.DataFrame({
    "nominal": [fmt(dol['DOLS base (+q)']['beta'][a], dol['DOLS base (+q)']['res'].bse[a]) for a in BASE] + [
        fmt(res_pref.params["ect_l1"], res_pref.bse["ect_l1"]), res_pref.rsquared_adj, int(res_pref.nobs), S.terminos[PREF],
        freq_pref, diag["Preferido (R2aj)"]["BG4_p"], diag["Preferido (R2aj)"]["RESET_p"], ch.iloc[0].p, cdf.iloc[0].decision],
    "real": [fmt(rs.params[a], rs.bse[a]) for a in BASE_R] + [
        fmt(resR.params["ect_l1"], resR.bse["ect_l1"]), resR.rsquared_adj, int(resR.nobs), SR.terminos[PR], freqR,
        diagR["Preferido real (R2aj)"]["BG4_p"], diagR["Preferido real (R2aj)"]["RESET_p"], chR.iloc[0].p, real.decision]},
    index=["LR ocupados", "LR tipo (nominal / real)", "LR permisos t−4", "LR costes (nominal / reales)", "ect(t−1)", "R2_aj CP", "N CP",
           "términos CP", "frec. bootstrap del preferido", "BG(4) p", "RESET p", "Chow 2014Q1 p", "cointegración (≥2/3)"])
save(cmp.astype(str), "comparacion_nominal_real", index=True)
sec("8. Ecuación en PRECIO REAL (única con cointegración 3/3)",
    "**Definición.** y = ln_ipv_real = ln_ipv − ln_deflactor (deflactor del PIB). Vector exactamente igual al del test 3/3: "
    "ln_ocupados, tipo_hip_real (= tipo_hip − inflación del deflactor), ln_permisos_l4 y ln_costes_real (= ln_costes − ln_deflactor): "
    "SÍ, los costes van en términos reales. DOLS ±2 con dummies trimestrales, HAC(4). CP: d(ln_ipv_real) con ect(t−1) del DOLS real, "
    f"el MISMO conjunto cerrado de candidatos (el retardo de la dependiente es d_ln_ipv_real_l1/l4; el resto de candidatos son los mismos "
    f"d_ ya definidos), {NMR} modelos, muestra común {CR_.index[0]}-{CR_.index[-1]}, N={NR}. Selección por R² aj con Bonferroni "
    f"(K = modelos con el término) y bootstrap de bloques (B=999, bloque 8, semilla {SEED}; ect fijo). Asociaciones, no causalidad.\n\n"
    "**Ecuación real final (coef, EE HAC, IC 95 %, p, p Bonferroni)**\n\n" + tm(ECR, ".4g", False) +
    f"\nEl preferido real gana en {freqR:.1%} de las réplicas bootstrap. **Ganadores (misma muestra)**\n\n" + tm(winTR, ".5g", False) +
    "\n**EBA / Bonferroni**\n\n" + tm(EBAR.drop(columns=["en_preferido"]), ".3g", False) + "\n**Bootstrap de la selección**\n\n" + tm(BOOTR, ".3g", False) +
    "\n**OOS** (ventana expansiva desde 2018Q1; LR re-estimado hasta t−1; selección con muestra completa → pseudo-OOS)\n\n" + tm(OOSR, ".4g", False) +
    "\n**Diagnósticos** (BG-aumentado: " + "; ".join(f"{a['paso']} p={a['BG4_p']:.3f}" for a in augR) + ")\n\n" + tm(DGR, ".3g") +
    "\n**Chow**\n\n" + tm(chR, ".4g", False) + "\n**Bai-Perron**\n\n" + tm(BPR, ".4g", False) +
    "\n**Robustez (dummies epa21/tipo22, escalones, 2014+, pre-COVID)**\n\n" + tm(ROBR, ".4g", False) +
    "\n**Comparación nominal vs real**\n\n" + tm(cmp.astype(str), ".4g") +
    "\nEl precio real y el nominal difieren por el deflactor (tendencia común de precios generales); la relación de nivel es "
    "estadísticamente más sostenible en términos reales (3/3 frente a 1/3), pero comparte la inestabilidad de los quiebres.\n")

# estado de cointegración
nom, real = cdf.iloc[0], cdf[cdf.sistema.str.startswith("ln_ipv_real")].iloc[0]
txt_coint = (f"**Estado de la relación de largo plazo.** Vector nominal principal: EG p={nom.EG_p:.3f}, Johansen traza (r≥1: {bool(nom.J_rech)}), "
             f"ARDL bounds F={nom.ARDL_F:.2f} (I0/I1 5 % = {nom.ARDL_I0_5:.2f}/{nom.ARDL_I1_5:.2f}, k={int(nom.ARDL_k)}; {nom.ARDL_zona}) → "
             f"{int(nom.n_rechazos)}/3: **{nom.decision}**. Vector en precio real: EG p={real.EG_p:.3f}, ARDL F={real.ARDL_F:.2f} "
             f"(I1 5 % = {real.ARDL_I1_5:.2f}) → {int(real.n_rechazos)}/3: **{real.decision}**. "
             "La significatividad del coeficiente del ect (t≈−3,1) NO contrasta cointegración: bajo la nula de no cointegración su "
             "distribución no es normal ni t, y los valores críticos son más negativos que −1,96 (contrastes de tipo Banerjee-Dolado-Mestre, "
             "referencia propuesta por el revisor, aún sin añadir a la literatura verificada). El ECM se presenta por tanto como un modelo condicional con "
             "término de desequilibrio respecto a una relación de nivel NO confirmada, e inestable (Bai-Perron en niveles: 3 quiebres; "
             "pre-COVID: costes y permisos cambian de signo). Se interpreta como reversión parcial hacia una tendencia común inestable.")

dcoef = beta_pref["res"]
top = BOOT.set_index("termino").frec_en_ganador
res_txt = [f"# Resumen F2 (nacional)\n\nLenguaje: asociaciones, sin identificación causal. Semilla {SEED}. "
           f"Filas del registro de la fase: {len(REG.read())} (de ellas {NM} de la búsqueda de corto plazo).\n",
           "## P1. Ecuación final\n\n" + txt_coint + "\n\n**Largo plazo (DOLS ±2, HAC(4), "
           f"N={beta_pref['n']}; estado: evidencia mixta/inestable, no usar como estimación puntual fiable):** ln_ipv = {beta_pref['const']:.3f} " +
           " ".join(f"{'+' if beta_pref['beta'][x] >= 0 else '-'} {abs(beta_pref['beta'][x]):.3f}[{dcoef.bse[x]:.3f}]·{x}" for x in BASE) +
           " (EE HAC entre corchetes; dummies trimestrales incluidas).\n\n**Corto plazo (preferido por R² ajustado, "
           f"N={int(res_pref.nobs)}; ecuación condicional, selección inestable):**\n\n" + tm(pref_tab, ".4g") +
           f"\nLa especificación concreta no está identificada (gana en {freq_pref:.1%} de las réplicas bootstrap). Términos sostenibles como "
           f"asociación: empleo (en t o t−1: {top['d_ln_ocupados'] + top['d_ln_ocupados_l1']:.0%} de las réplicas), persistencia de Δprecio "
           f"({top['d_ln_ipv_l1'] + top['d_ln_ipv_l4']:.0%}) y crédito contemporáneo ({top['d_ln_credito_nuevo']:.0%}), este último solo como comovimiento "
           "(ver 6c). El ect está forzado en todos los modelos, así que su frecuencia no es informativa.\n"] + MD
prob = []
d_ = diag["Preferido (R2aj)"]
for k_ in ["BG4_p", "BP_p", "JB_p", "RESET_p", "CUSUM_p"]:
    if d_[k_] < .05:
        prob.append(f"El ECM preferido rechaza {k_} (p={d_[k_]:.3f}).")
    if diag["Réplica ECM con q"][k_] < .05:
        prob.append(f"La réplica ECM (con q) rechaza {k_} (p={diag['Réplica ECM con q'][k_]:.3g}).")
if d_["VIF_max"] > 10:
    prob.append(f"VIF máximo {d_['VIF_max']:.1f} (>10) en el preferido.")
prob.append(f"Cointegración nominal: {nom.decision} (EG/Johansen/ARDL: {bool(nom.EG_rech)}/{bool(nom.J_rech)}/{bool(nom.ARDL_rech)}); "
            f"precio real: {real.decision}. La regla ≥2/3 se aplica tal cual; no se cambia la especificación principal ex post.")
prob += [
    "El p-valor del ect no es un contraste de cointegración (ver P1).",
    "LR inestable: Bai-Perron en niveles (2012Q1, 2020Q2, 2023Q2), cambios de signo pre-COVID; Chow 2014Q1 rechaza en el ECM (p=%.3f)." % ch.iloc[0].p,
    "Crédito contemporáneo simultáneo con el precio (6c).",
    "ln_p_tasado y ln_p_bde son idénticas en nacional_q (diferencia máx. 0): los dos sistemas de robustez no son independientes.",
    "Johansen rechaza rangos altos (2-4) en sistemas de 5-6 variables I(1) con N≈74: probable sobre-rechazo; no puede ser el único apoyo.",
    "Bonferroni con K=nº de modelos que contienen el término es una cota muy conservadora (los modelos están anidados, no son hipótesis independientes) y no aplica al ect forzado; se da prioridad al bootstrap de la selección.",
    "OOS: el preferido no mejora al AR(4)+dummies ni al paseo con deriva; selección con muestra completa (pseudo-OOS).",
    "El ect del ECM es un regresor generado; no se corrige su incertidumbre; en el bootstrap se mantiene fijo.",
    "Johansen sin dummies estacionales (limitación de coint_johansen); ARDL sí las incluye.",
    "Población extranjera y población total interpoladas log-lineal antes de 2021 (MA mecánica en Δ1); d4/4 como contraste.",
    "IPV no desestacionalizado; las dummies absorben solo estacionalidad determinista.",
]
res_txt.append("\n## 7. Problemas abiertos\n\n" + "\n".join("- " + p for p in prob) + "\n")
(OUT / "resumen_f2.md").write_text("\n".join(res_txt))
print(f"F2 OK en {time.time() - T0:.0f}s; N_modelos={NM}; registro={len(REG.read())} filas; N búsqueda={N}")
print("Preferido R2aj:", S.terminos[PREF], "| BIC:", S.terminos[i_bic], "| AIC:", S.terminos[i_aic])
print(cdf[["sistema", "EG_p", "J_rech", "ARDL_F", "ARDL_I1_5", "ARDL_zona", "n_rechazos", "decision"]].to_string())
