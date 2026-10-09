"""F3 - Inmigracion y precios (P2). Determinista, sin red. Semilla 20261009.

Salidas: output/f3/*.csv|md|png, output/registro_busqueda_f3.csv (reescrito en cada ejecucion).
1) Nacional (asociacion): proyecciones locales, flujo anual, separabilidad empleo-inmigracion.
2-5) Panel CCAA anual: IV shift-share (Card 2001), diagnosticos GPSS/AKM-simplificado, canal comprador,
     desagregacion por nacionalidad.
Motor 2SLS propio (FWL con efectos fijos proyectados), EE cluster CRV1, Driscoll-Kraay, wild cluster
bootstrap restringido (Webb, 9.999) para el coeficiente de x, J de Hansen robusto a cluster.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ_utils as eu  # noqa: E402

warnings.filterwarnings("ignore")
SEED = eu.SEED
ROOT = eu.ROOT
OUT = ROOT / "output" / "f3"
OUT.mkdir(parents=True, exist_ok=True)
REG = eu.Registry(ROOT / "output" / "registro_busqueda_f3.csv", reset=True)
B_BOOT = 9999
RES = {}          # resultados para el resumen
NSPEC = [0]


def save(df, name, index=True, fmt=".4g"):
    df.to_csv(OUT / f"{name}.csv", index=index)
    (OUT / f"{name}.md").write_text(eu.df_md(df, fmt, index=index) + "\n", encoding="utf-8")


def reglog(mid, formula, ini, fin, n, r2, aic, bic, coef, p, notas=""):
    NSPEC[0] += 1
    REG.log("F3", mid, formula, ini, fin, int(n), r2, aic, bic, np.nan, coef, p, notas)


# =====================================================================================
# 1. NACIONAL
# =====================================================================================
def nacional():
    q = eu.load_nacional(desde="2000Q1", hasta="2026Q4")
    q["x_ext"] = q["d4_ln_pob_extranj"]
    q["x_tot"] = q["d4_ln_pob_total"]
    q["x_flow"] = (q["pob_extranj"] - q["pob_extranj"].shift(4)) / q["pob_total"].shift(4)
    for k in range(1, 5):
        q[f"d_ln_ocu_l{k}"] = q["d_ln_ocupados"].shift(k)
        q[f"d_tipo_l{k}"] = q["d_tipo_hip"].shift(k)
        q[f"d_ln_alq_l{k}"] = q["d_ln_ipc_alquiler"].shift(k)
    H = list(range(0, 9))
    out_rows, diag_rows = [], []
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), sharex=True)
    for ax, (dep, lab, own) in zip(axs, [("ln_ipv", "IPV (precio)", "d_ln_ipv_l"),
                                          ("ln_ipc_alquiler", "IPC alquiler", "d_ln_alq_l")]):
        ctrl = [f"{own}{k}" for k in range(1, 5)] + [f"d_ln_ocu_l{k}" for k in range(1, 5)] + \
               [f"d_tipo_l{k}" for k in range(1, 5)] + ["q2", "q3", "q4"]
        for h in H:
            q[f"y_{dep}_{h}"] = q[dep].shift(-h) - q[dep].shift(1)
        for xv in ["x_ext", "x_tot", "x_flow"]:
            cols = [f"y_{dep}_{h}" for h in H] + [xv] + ctrl
            S = eu.common_sample(q, cols)          # muestra comun = la del h=8
            rows = []
            for h in H:
                f = f"y_{dep}_{h} ~ {xv} + " + " + ".join(ctrl)
                r = eu.ols_hac(f, S, maxlags=h + 4)
                b, se = r.params[xv], r.bse[xv]
                rows.append(dict(h=h, coef=b, EE_HAC=se, p=r.pvalues[xv], lo=b - 1.96 * se, hi=b + 1.96 * se,
                                 n=int(r.nobs), muestra=f"{S.index[0]}-{S.index[-1]}"))
                reglog(f"NAC_LP_{dep}_{xv}_h{h}", f, S.index[0], S.index[-1], r.nobs, r.rsquared_adj,
                       r.aic, r.bic, b, r.pvalues[xv], f"HAC({h + 4}); muestra comun h=0..8")
                if xv == "x_ext" and h in (0, 4, 8):
                    d = eu.diagnostics(r)
                    d.update(modelo=f"{dep}_h{h}")
                    for fch in ["2014Q1", "2020Q1", "2022Q3"]:
                        c = eu.chow(S, f, fch)
                        d[f"Chow_{fch}_p"] = c["p"]
                    try:
                        yy = pd.Series(r.model.endog, index=S.index)
                        bp = eu.bai_perron(yy, pd.DataFrame(r.model.exog, index=S.index), 2, 12)
                        d["BaiPerron"] = f"{bp['n_bkps']}:{','.join(bp['fechas'])}"
                    except Exception as e:
                        d["BaiPerron"] = f"err {e}"
                    diag_rows.append(d)
            t = pd.DataFrame(rows)
            t.insert(0, "x", xv)
            t.insert(0, "dep", dep)
            out_rows.append(t)
            if xv in ("x_ext", "x_flow"):
                sc = 1.0 if xv == "x_flow" else 1.0
                ax.plot(t.h, t.coef * sc, marker="o", label={"x_ext": "Delta4 ln pob. extranjera",
                                                           "x_flow": "Delta4 extranj./pob. total (-4)"}[xv])
                ax.fill_between(t.h, t.lo * sc, t.hi * sc, alpha=0.15)
        ax.axhline(0, color="k", lw=0.6)
        ax.set_title(f"{lab}: ln y(t+h) - ln y(t-1) sobre x_t")
        ax.set_xlabel("h (trimestres)")
        ax.set_ylabel("coef. (ln por unidad de x)")
        ax.legend(fontsize=7)
    fig.suptitle("Asociacion dinamica (proyecciones locales), IC95% HAC(h+4); sin identificacion", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "irf_nacional.png", dpi=130)
    plt.close(fig)
    lp = pd.concat(out_rows)
    save(lp, "nacional_lp", index=False)
    save(pd.DataFrame(diag_rows).set_index("modelo"), "nacional_lp_diagnosticos")
    RES["lp"] = lp

    # (b) flujo anual
    na = pd.read_csv(ROOT / "data/processed/nacional_a.csv").set_index("anio")
    pa = pd.read_csv(ROOT / "data/processed/panel_ccaa_a.csv")
    pop = pa.groupby("anio")["pob_total"].sum()
    na["pob_total_l1"] = pop.shift(1).reindex(na.index)
    na["tasa"] = na["inmig_anual_eurostat"] / na["pob_total_l1"]
    na["tasa_l1"] = na["tasa"].shift(1)
    na["d_ln_pob_extranj_l1"] = na["d_ln_pob_extranj"].shift(1)
    na["emcr"] = na["quiebre_emcr_2021"].astype(float)
    cols = ["d_ln_ipv", "tasa", "tasa_l1", "d_ln_pob_extranj", "d_ln_pob_extranj_l1", "emcr"]
    S = eu.common_sample(na, cols)
    specs = {"A1_flujo_t": ("d_ln_ipv ~ tasa + emcr", "tasa"),
             "A2_flujo_t_l1": ("d_ln_ipv ~ tasa + tasa_l1 + emcr", "tasa"),
             "A3_stock_t": ("d_ln_ipv ~ d_ln_pob_extranj + emcr", "d_ln_pob_extranj"),
             "A4_stock_t_l1": ("d_ln_ipv ~ d_ln_pob_extranj + d_ln_pob_extranj_l1 + emcr", "d_ln_pob_extranj")}
    rows = []
    for k, (f, v) in specs.items():
        r = eu.ols_hac(f, S, maxlags=4)
        for nm in r.params.index[1:]:
            rows.append(dict(modelo=k, var=nm, coef=r.params[nm], EE_HAC4=r.bse[nm], p=r.pvalues[nm],
                             n=int(r.nobs), R2aj=r.rsquared_adj))
        reglog(f"NAC_ANUAL_{k}", f, S.index[0], S.index[-1], r.nobs, r.rsquared_adj, r.aic, r.bic,
               r.params[v], r.pvalues[v], "anual N pequeno; HAC(4) con N~16 poco fiable")
        d = eu.diagnostics(r)
        d["modelo"] = k
        diag_rows.append(d)
    t = pd.DataFrame(rows)
    save(t, "nacional_anual", index=False)
    RES["anual"] = t
    RES["anual_n"] = len(S)
    RES["anual_rng"] = f"{S.index[0]}-{S.index[-1]}"

    # (c) separabilidad empleo-inmigracion
    Z = eu.common_sample(q, ["d4_ln_ocupados", "d4_ln_pob_extranj"])
    rows = []
    for nm, sub in {"muestra completa": Z, "2008Q1-2019Q4": Z.loc["2008Q1":"2019Q4"],
                    "2013Q1-2026Q2": Z.loc["2013Q1":"2026Q2"]}.items():
        c = sub["d4_ln_ocupados"].corr(sub["d4_ln_pob_extranj"])
        rows.append(dict(muestra=nm, n=len(sub), corr=c, VIF_par=1 / (1 - c ** 2)))
    X3 = eu.common_sample(q, ["d4_ln_ocupados", "d4_ln_pob_extranj", "d_tipo_hip"])
    Xm = sm.add_constant(X3[["d4_ln_ocupados", "d4_ln_pob_extranj", "d_tipo_hip"]])
    from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
    rows.append(dict(muestra="VIF (ocupados, extranj., d_tipo) completa", n=len(X3), corr=np.nan,
                     VIF_par=max(vif(Xm.values, i) for i in (1, 2))))
    save(pd.DataFrame(rows), "nacional_separabilidad", index=False)
    RES["sep"] = pd.DataFrame(rows)


# =====================================================================================
# 2. MOTOR PANEL
# =====================================================================================
GRUPOS = {"europa": ["pob_europa_sin_espana"], "africa": ["pob_africa"],
          "america": ["pob_sudamerica", "pob_centroamerica_caribe", "pob_norteamerica"],
          "asia": ["pob_asia"], "otros": ["pob_oceania", "pob_apatridas"]}
GN = list(GRUPOS)


def build_panel():
    P = pd.read_csv(ROOT / "data/processed/panel_ccaa_a.csv").sort_values(["ccaa", "anio"]).reset_index(drop=True)
    gb = P.groupby("ccaa")
    for g, cols in GRUPOS.items():
        P[f"P_{g}"] = P[cols].sum(axis=1)
    P["pop_l1"] = gb["pob_total"].shift(1)
    P["dext"] = gb["pob_extranj"].diff()
    P["x"] = P["dext"] / P["pop_l1"]
    for g in GN:
        P[f"dP_{g}"] = P.groupby("ccaa")[f"P_{g}"].diff()
        P[f"x_{g}"] = P[f"dP_{g}"] / P["pop_l1"]
    nat = P.groupby("anio")[[f"dP_{g}" for g in GN]].sum(min_count=17)
    P0 = P[P.anio == 2002].set_index("ccaa")
    for g in GN:
        s = P0[f"P_{g}"] / P0[f"P_{g}"].sum()
        P[f"s_{g}"] = P["ccaa"].map(s)
        loo = P["anio"].map(nat[f"dP_{g}"]) - P[f"dP_{g}"]
        P[f"z_{g}"] = P[f"s_{g}"] * loo / P["pop_l1"]
    P["z"] = P[[f"z_{g}" for g in GN]].sum(axis=1, min_count=5)
    P.loc[P.anio == 2002, ["z", "x"]] = np.nan
    P["x_l1"] = P.groupby("ccaa")["x"].shift(1)
    P["z_l1"] = P.groupby("ccaa")["z"].shift(1)
    P["cl"] = P["ccaa"].astype("category").cat.codes
    return P


def resid(A, U):
    return A - U @ (U.T @ A)


def basis(D):
    U, s, _ = np.linalg.svd(D, full_matrices=False)
    return U[:, : int((s > s.max() * 1e-9).sum())]


def design(s, trends=False, ctrl=()):
    cc = pd.get_dummies(s["ccaa"]).astype(float)
    yy = pd.get_dummies(s["anio"]).astype(float).iloc[:, 1:]
    parts = [cc.values, yy.values]
    if trends:
        t = (s["anio"] - s["anio"].mean()).values[:, None]
        parts.append(cc.values * t)
    for c in ctrl:
        parts.append(s[[c]].values.astype(float))
    return basis(np.hstack(parts))


def cluster_scores(M, cl, G):
    return np.vstack([np.bincount(cl, weights=M[:, j], minlength=G) for j in range(M.shape[1])]).T


def wald_F(pi, V, q):
    try:
        return float(pi @ np.linalg.pinv(V) @ pi / q)
    except Exception:
        return np.nan


def fit_iv(s, y, xs, zs, trends=False, ctrl=(), boot=False, ols_only=False, seed_off=0, do_J=False):
    """2SLS (o OLS si ols_only) con FE proyectados (FWL). s: DataFrame muestra ya recortada."""
    s = s.reset_index(drop=True)
    U = design(s, trends, ctrl)
    yt = resid(s[[y]].values.astype(float), U)[:, 0]
    X = resid(s[xs].values.astype(float), U)
    Z = X if ols_only else resid(s[zs].values.astype(float), U)
    cl = s["cl"].values
    cl = pd.factorize(cl)[0]
    G = cl.max() + 1
    n, k, q = len(yt), X.shape[1], Z.shape[1]
    K = U.shape[1] + k
    c = G / (G - 1) * (n - 1) / (n - K)
    ZZi = np.linalg.pinv(Z.T @ Z)
    Xh = Z @ ZZi @ Z.T @ X
    A = np.linalg.pinv(Xh.T @ Xh)
    beta = A @ Xh.T @ yt
    u = yt - X @ beta
    Sc = cluster_scores(Xh * u[:, None], cl, G)
    V = c * A @ (Sc.T @ Sc) @ A
    se = np.sqrt(np.diag(V))
    # Driscoll-Kraay
    yrs = pd.factorize(s["anio"].values, sort=True)[0]
    Hh = cluster_scores(Xh * u[:, None], yrs, yrs.max() + 1)
    S = Hh.T @ Hh
    L = 2
    for l in range(1, L + 1):
        Gm = Hh[l:].T @ Hh[:-l]
        S += (1 - l / (L + 1)) * (Gm + Gm.T)
    se_dk = np.sqrt(np.diag(A @ S @ A))
    p = 2 * stats.t.sf(np.abs(beta / se), G - 1)
    out = dict(n=n, G=G, K=K, beta=beta, se=se, p=p, se_dk=se_dk, ols_only=ols_only,
               r2_within=1 - (u @ u) / (yt @ yt), rss=float(u @ u))
    # primera etapa y forma reducida
    if not ols_only:
        fs = []
        for j in range(k):
            Pi = ZZi @ Z.T @ X[:, j]
            e = X[:, j] - Z @ Pi
            Sj = cluster_scores(Z * e[:, None], cl, G)
            Vp = c * ZZi @ (Sj.T @ Sj) @ ZZi
            F = wald_F(Pi, Vp, q)
            r2p = 1 - (e @ e) / (X[:, j] @ X[:, j])
            fs.append(dict(F=F, pi=Pi, se_pi=np.sqrt(np.diag(Vp)), r2_parcial=r2p))
        out["fs"] = fs
        Pr = ZZi @ Z.T @ yt
        er = yt - Z @ Pr
        Sr = cluster_scores(Z * er[:, None], cl, G)
        Vr = c * ZZi @ (Sr.T @ Sr) @ ZZi
        out["rf"] = dict(coef=Pr, se=np.sqrt(np.diag(Vr)),
                         p=2 * stats.t.sf(np.abs(Pr / np.sqrt(np.diag(Vr))), G - 1))
    if do_J and (not ols_only) and q > k:
        out["J"] = hansen_J(yt, X, Z, cl, G, n)
    if boot and k == 1:
        out["wcb_p"], out["wcb_t"] = wre_boot(yt, X[:, 0], Z[:, 0], U, cl, G, c, B_BOOT,
                                              np.random.default_rng(SEED + seed_off), ols_only)
    out["yt"], out["Xt"], out["Zt"], out["U"], out["cl_i"], out["u"] = yt, X, Z, U, cl, u
    return out


def hansen_J(yt, X, Z, cl, G, n):
    ZZi = np.linalg.pinv(Z.T @ Z)
    b = np.linalg.pinv(X.T @ Z @ ZZi @ Z.T @ X) @ (X.T @ Z @ ZZi @ Z.T @ yt)
    u = yt - X @ b
    for _ in range(2):
        gS = cluster_scores(Z * u[:, None], cl, G)
        Sh = gS.T @ gS / n
        W = np.linalg.pinv(Sh)
        b = np.linalg.pinv(X.T @ Z @ W @ Z.T @ X) @ (X.T @ Z @ W @ Z.T @ yt)
        u = yt - X @ b
    gS = cluster_scores(Z * u[:, None], cl, G)
    Sh = gS.T @ gS / n
    gbar = Z.T @ u / n
    J = float(n * gbar @ np.linalg.pinv(Sh) @ gbar)
    dfj = Z.shape[1] - X.shape[1]
    return dict(J=J, df=dfj, p=float(stats.chi2.sf(J, dfj)), beta=b.tolist())


def wre_boot(yt, xt, zt, U, cl, G, c, B, rng, ols):
    n = len(yt)
    zx = zt @ xt
    beta = (zt @ yt) / zx
    u = yt - beta * xt
    s = np.bincount(cl, weights=zt * u, minlength=G)
    t0 = beta / (np.sqrt(c * (s @ s)) / abs(zx))
    if not ols:
        pi = (zt @ xt) / (zt @ zt)
        v = xt - pi * zt
    webb = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])
    C = np.zeros((n, G))
    C[np.arange(n), cl] = 1.0
    tb, done = [], 0
    while done < B:
        b = min(1000, B - done)
        W = webb[rng.integers(0, 6, size=(b, G))][:, cl].T
        Ys = resid(yt[:, None] * W, U)
        if ols:
            Xs = np.repeat(xt[:, None], b, axis=1)
        else:
            Xs = pi * zt[:, None] + resid(v[:, None] * W, U)
        zxb = zt @ Xs
        bb = (zt @ Ys) / zxb
        ub = Ys - bb * Xs
        Sb = C.T @ (zt[:, None] * ub)
        seb = np.sqrt(c * (Sb ** 2).sum(axis=0)) / np.abs(zxb)
        tb.append(bb / seb)
        done += b
    tb = np.concatenate(tb)
    return float((np.abs(tb) >= abs(t0)).mean()), float(t0)


def sample_for(P, y, start, extra=()):
    cols = [y, "x", "z", "cl"] + list(extra)
    s = P[(P.anio >= start)].dropna(subset=cols)
    return s


def summarize(tag, res, which=0):
    r = dict(modelo=tag, n=res["n"], G=res["G"], coef=res["beta"][which], EE_cluster=res["se"][which],
             p_cluster=res["p"][which], EE_DK=res["se_dk"][which])
    if "fs" in res:
        r["F_1a_etapa"] = res["fs"][which]["F"]
        r["pi"] = res["fs"][which]["pi"][0] if len(res["fs"][which]["pi"]) == 1 else np.nan
        r["EE_pi"] = res["fs"][which]["se_pi"][0] if len(res["fs"][which]["pi"]) == 1 else np.nan
        r["RF_coef"] = res["rf"]["coef"][0] if len(res["rf"]["coef"]) == 1 else np.nan
        r["RF_p"] = res["rf"]["p"][0] if len(res["rf"]["p"]) == 1 else np.nan
    if "wcb_p" in res:
        r["p_WCB_restr"] = res["wcb_p"]
    if "J" in res:
        r["J"] = res["J"]["J"]
        r["J_df"] = res["J"]["df"]
        r["J_p"] = res["J"]["p"]
    return r


def log_panel(mid, formula, s, res, interes_idx=0, notas=""):
    p_i = res.get("wcb_p", res["p"][interes_idx])
    n = res["n"]
    rss = res["rss"]
    aic = n * np.log(rss / n) + 2 * res["K"] if res["ols_only"] else np.nan
    bic = n * np.log(rss / n) + res["K"] * np.log(n) if res["ols_only"] else np.nan
    r2a = 1 - (1 - res["r2_within"]) * (n - 1) / (n - res["K"])
    reglog(mid, formula, s["anio"].min(), s["anio"].max(), n, r2a, aic, bic, res["beta"][interes_idx],
           p_i, notas + (" | p=wild bootstrap restringido" if "wcb_p" in res else " | p=cluster t(G-1)"))


OUTCOMES = {"ipv": ("d_ln_ipv", 2008, "IPV (precio)"), "p_tasado": ("d_ln_p_tasado", 2003, "valor tasado"),
            "serpavi": ("d_ln_serpavi_vc_mediana", 2012, "alquiler SERPAVI"),
            "ipc_alq": ("d_ln_ipc_alquiler", 2003, "IPC alquiler")}


def principal(P):
    rows, diag, fs_rows = [], [], []
    cache = {}
    off = 0
    for key, (y, start, lab) in OUTCOMES.items():
        s = sample_for(P, y, start)
        for tr in (False, True):
            tg = "FE" if not tr else "FE+tend"
            for est in ("OLS", "2SLS"):
                off += 1
                res = fit_iv(s, y, ["x"], ["z"], trends=tr, ols_only=(est == "OLS"), boot=True,
                             seed_off=off, do_J=False)
                cache[(key, tg, est)] = res
                r = summarize(f"{key}|{tg}|{est}", res)
                r.update(resultado=lab, spec=tg, est=est, muestra=f"{s.anio.min()}-{s.anio.max()}")
                rows.append(r)
                log_panel(f"PAN_{key}_{tg}_{est}", f"{y} ~ x | FE ccaa + FE anio" + (" + tend ccaa" if tr else ""),
                          s, res, notas=f"{est} cluster17; x=dExtr/pop(-1); z=shift-share Card LOO")
        # control de ocupados (mal control potencial)
        s2 = sample_for(P, y, start, extra=["d_ln_ocupados"])
        # misma muestra que principal salvo faltantes: reportar n
        for est in ("OLS", "2SLS"):
            off += 1
            res = fit_iv(s2, y, ["x"], ["z"], ctrl=["d_ln_ocupados"], ols_only=(est == "OLS"), boot=True, seed_off=off)
            r = summarize(f"{key}|FE+ocupados|{est}", res)
            r.update(resultado=lab, spec="FE+ctrl d_ln_ocupados", est=est, muestra=f"{s2.anio.min()}-{s2.anio.max()}")
            rows.append(r)
            log_panel(f"PAN_{key}_FEocu_{est}", f"{y} ~ x + d_ln_ocupados | FE ccaa + anio", s2, res,
                      notas="robustez: posible mal control")
        # x y x rezagada
        s3 = sample_for(P, y, start, extra=["x_l1", "z_l1"])
        for est in ("OLS", "2SLS"):
            res = fit_iv(s3, y, ["x", "x_l1"], ["z", "z_l1"], ols_only=(est == "OLS"))
            for j, nm in enumerate(["x", "x_l1"]):
                r = summarize(f"{key}|FE+rezago|{est}|{nm}", res, which=j)
                r.update(resultado=lab, spec=f"FE, x_t y x_t-1 [{nm}]", est=est, muestra=f"{s3.anio.min()}-{s3.anio.max()}")
                rows.append(r)
            log_panel(f"PAN_{key}_FElag_{est}", f"{y} ~ x + x_l1 | FE ccaa + anio", s3, res,
                      notas="robustez dinamica; coef de x_t")
        # sin 2020-2021 (COVID)
        s4 = s[~s.anio.isin([2020, 2021])]
        for est in ("OLS", "2SLS"):
            off += 1
            res = fit_iv(s4, y, ["x"], ["z"], ols_only=(est == "OLS"), boot=True, seed_off=off)
            r = summarize(f"{key}|FE sin 2020-21|{est}", res)
            r.update(resultado=lab, spec="FE sin 2020-2021", est=est, muestra=f"{s4.anio.min()}-{s4.anio.max()}")
            rows.append(r)
            log_panel(f"PAN_{key}_FEsinCOVID_{est}", f"{y} ~ x | FE, sin 2020-21", s4, res)
        # diagnosticos del OLS principal
        r0 = cache[(key, "FE", "OLS")]
        yt, xt = r0["yt"], r0["Xt"][:, 0]
        m = sm.OLS(yt, sm.add_constant(xt)).fit()
        d = eu.diagnostics(m)
        d["modelo"] = f"{key}|FE|OLS (residuos FWL)"
        u = r0["u"]
        sdf = s.reset_index(drop=True)
        lag = pd.Series(u).groupby(sdf["ccaa"]).shift(1)
        mk = lag.notna().values
        d["AR1_resid_intra_ccaa"] = float(np.corrcoef(u[mk], lag.values[mk])[0, 1])
        diag.append(d)
        for est_ in ("2SLS",):
            rs = cache[(key, "FE", est_)]
            fs_rows.append(dict(resultado=lab, n=rs["n"], F_cluster=rs["fs"][0]["F"], pi=rs["fs"][0]["pi"][0],
                                EE_pi=rs["fs"][0]["se_pi"][0], R2_parcial=rs["fs"][0]["r2_parcial"],
                                RF_coef=rs["rf"]["coef"][0], RF_p_cluster=rs["rf"]["p"][0]))
    # submuestra auge 2003-07 (valor tasado): comparabilidad con Gonzalez-Ortega
    s07 = sample_for(P, "d_ln_p_tasado", 2003)
    s07 = s07[s07.anio <= 2007]
    r07 = fit_iv(s07, "d_ln_p_tasado", ["x"], ["z"])
    RES["sub0307"] = dict(coef=r07["beta"][0], se=r07["se"][0], F=r07["fs"][0]["F"])
    log_panel("PAN_p_tasado_2003_07", "d_ln_p_tasado ~ x | FE, 2003-2007", s07, r07, notas="submuestra auge; comparabilidad")
    # jackknife por CCAA (valor tasado, 2SLS FE)
    y, start, lab = OUTCOMES["p_tasado"][0], OUTCOMES["p_tasado"][1], "valor tasado"
    s = sample_for(P, y, start)
    jk = []
    for c in sorted(s.ccaa.unique()):
        sc = s[s.ccaa != c]
        res = fit_iv(sc, y, ["x"], ["z"])
        jk.append(dict(excluida=c, n=res["n"], coef=res["beta"][0], EE=res["se"][0], p=res["p"][0],
                       F=res["fs"][0]["F"]))
        log_panel(f"PAN_p_tasado_sin_{c}", f"{y} ~ x | FE, sin {c}", sc, res, notas="jackknife CCAA 2SLS")
    save(pd.DataFrame(jk), "panel_jackknife_ccaa_p_tasado", index=False)
    RES["jk"] = pd.DataFrame(jk)
    T = pd.DataFrame(rows)
    save(T, "panel_principal", index=False)
    save(pd.DataFrame(diag).set_index("modelo"), "panel_diagnosticos_ols")
    save(pd.DataFrame(fs_rows), "panel_primera_etapa", index=False)
    RES["princ"], RES["cache"], RES["fs"] = T, cache, pd.DataFrame(fs_rows)
    return cache


# =====================================================================================
# 3. DIAGNOSTICOS SHIFT-SHARE
# =====================================================================================
def rotemberg(P, key):
    y, start, lab = OUTCOMES[key]
    s = sample_for(P, y, start).reset_index(drop=True)
    U = design(s)
    yt = resid(s[[y]].values.astype(float), U)[:, 0]
    xt = resid(s[["x"]].values.astype(float), U)[:, 0]
    zg = {g: resid(s[[f"z_{g}"]].values.astype(float), U)[:, 0] for g in GN}
    zt = sum(zg.values())
    cl = pd.factorize(s["cl"].values)[0]
    G = cl.max() + 1
    n = len(yt)
    c = G / (G - 1) * (n - 1) / (n - U.shape[1] - 1)
    den = zt @ xt
    # caracteristicas 2002 por CCAA
    P0 = P[P.anio == 2002].set_index("ccaa")
    pre = P[P.anio.between(2002, 2007)].groupby("ccaa")["p_tasado"].apply(lambda v: np.log(v).mean())
    pg = P[P.anio.between(2003, 2007)].groupby("ccaa")["d_ln_p_tasado"].mean()
    chars = pd.DataFrame({"ln_p_tasado_0207": pre, "tasa_ocup_2002": P0.ocupados / P0.pob_total,
                          "ln_pob_total_2002": np.log(P0.pob_total), "sh_extranj_2002": P0.pob_extranj / P0.pob_total,
                          "crec_p_tasado_0307": pg})
    rows = []
    for g in GN:
        a = (zg[g] @ xt) / den
        bg = (zg[g] @ yt) / (zg[g] @ xt)
        u = yt - bg * xt
        sc = np.bincount(cl, weights=zg[g] * u, minlength=G)
        seg = np.sqrt(c * (sc @ sc)) / abs(zg[g] @ xt)
        sh = P0[f"P_{g}"] / P0[f"P_{g}"].sum()
        r = dict(grupo=g, alpha=a, beta_g=bg, EE_g=seg, p_g=2 * stats.t.sf(abs(bg / seg), G - 1),
                 sh_nacional_grupo_2002=P0[f"P_{g}"].sum() / P0["pob_extranj"].sum())
        for ch in chars:
            r[f"corr_cuota_{ch}"] = float(np.corrcoef(sh.reindex(chars.index), chars[ch])[0, 1])
        rows.append(r)
    t = pd.DataFrame(rows)
    t["alpha_neg"] = t.alpha < 0
    beta_tot = (zt @ yt) / den
    assert abs((t.alpha * t.beta_g).sum() - beta_tot) < 1e-8 and abs(t.alpha.sum() - 1) < 1e-8
    save(t, f"rotemberg_{key}", index=False)
    RES[f"rot_{key}"] = t
    # figura
    if key == "p_tasado":
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.bar(t.grupo, t.alpha, color=["C3" if v < 0 else "C0" for v in t.alpha])
        ax.axhline(0, color="k", lw=0.6)
        ax.set_title("Pesos de Rotemberg (alpha_g), Delta ln valor tasado")
        fig.tight_layout()
        fig.savefig(OUT / "rotemberg_alpha.png", dpi=130)
        plt.close(fig)
    return t


def pretendencias(P):
    zbar = P[P.anio >= 2008].groupby("ccaa")["z"].mean()
    rows = []
    for nm, col in [("p_tasado", "d_ln_p_tasado"), ("ipc_alquiler", "d_ln_ipc_alquiler")]:
        pre = P[P.anio.between(2003, 2007)]
        cs = pre.groupby("ccaa")[col].mean().to_frame("y")
        cs["zbar"] = zbar
        r = smf.ols("y ~ zbar", cs).fit(cov_type="HC3")
        rows.append(dict(resultado=nm, test="seccion cruzada (primeros anos de la muestra, NO pre salvo IPV): media dln 2003-07 ~ zbar(2008-25), HC3", n=len(cs),
                         coef=r.params["zbar"], EE=r.bse["zbar"], p=r.pvalues["zbar"]))
        reglog(f"PRE_{nm}_cs", f"mean {col} 2003-07 ~ zbar", 2003, 2007, len(cs), r.rsquared_adj, r.aic, r.bic,
               r.params["zbar"], r.pvalues["zbar"], "pretendencias, HC3, N=17")
        pp = pre.dropna(subset=[col]).copy()
        pp["zbar"] = pp["ccaa"].map(zbar)
        r2 = smf.ols(f"{col} ~ zbar + C(anio)", pp).fit(cov_type="cluster", cov_kwds={"groups": pp["ccaa"].astype("category").cat.codes})
        rows.append(dict(resultado=nm, test="panel 2003-07 (primeros anos de la muestra) con FE anio, cluster CCAA; coincide con la seccion cruzada", n=len(pp),
                         coef=r2.params["zbar"], EE=r2.bse["zbar"], p=r2.pvalues["zbar"]))
        reglog(f"PRE_{nm}_panel", f"{col} ~ zbar + FE anio (2003-07)", 2003, 2007, len(pp), r2.rsquared_adj, r2.aic,
               r2.bic, r2.params["zbar"], r2.pvalues["zbar"], "pretendencias, cluster")
        # con cuotas por grupo, una a una
        ps = {}
        for g in GN:
            cs[f"s_{g}"] = P[P.anio == 2002].set_index("ccaa")[f"s_{g}"]
            r3 = smf.ols(f"y ~ s_{g}", cs).fit(cov_type="HC3")
            ps[g] = r3.pvalues[f"s_{g}"]
            rows.append(dict(resultado=nm, test=f"cuota 2002 grupo {g} (una a una), HC3", n=len(cs),
                             coef=r3.params[f"s_{g}"], EE=r3.bse[f"s_{g}"], p=r3.pvalues[f"s_{g}"]))
            reglog(f"PRE_{nm}_cuota_{g}", f"mean {col} 2003-07 ~ s_{g}", 2003, 2007, len(cs), r3.rsquared_adj,
                   r3.aic, r3.bic, r3.params[f"s_{g}"], r3.pvalues[f"s_{g}"], "pretendencias por cuota")
        h = eu.holm(ps)
        for rr in rows[-len(GN):]:
            rr["p_Holm_cuotas"] = h[rr["test"].split("grupo ")[1].split(" ")[0]]
    t = pd.DataFrame(rows)
    save(t, "pretendencias", index=False)
    RES["pre"] = t
    return t


def sobreid_akm(P):
    rows = []
    for key, (y, start, lab) in OUTCOMES.items():
        s = sample_for(P, y, start)
        zs = [f"z_{g}" for g in GN]
        res = fit_iv(s, y, ["x"], zs, do_J=True)
        J = res["J"]
        fsr = res["fs"][0]
        # AKM simplificado: scores agregados por grupo de shock (G=5)
        U = res["U"]
        yt, xt = res["yt"], res["Xt"][:, 0]
        zgs = [resid(s.reset_index(drop=True)[[f"z_{g}"]].values.astype(float), U)[:, 0] for g in GN]
        zt = sum(zgs)
        bz = (zt @ yt) / (zt @ xt)
        u = yt - bz * xt
        Sg = np.array([zg @ u for zg in zgs])
        se_akm = np.sqrt(len(GN) / (len(GN) - 1) * (Sg @ Sg)) / abs(zt @ xt)
        p_akm = 2 * stats.t.sf(abs(bz / se_akm), len(GN) - 1)
        rows.append(dict(resultado=lab, n=res["n"], F_conjunta_5IV=fsr["F"], J_Hansen=J["J"], J_df=J["df"],
                         J_p=J["p"], coef_2SLS_5IV=J["beta"][0], coef_2SLS_z_unico=bz,
                         EE_AKM_simplificado_G5=se_akm, p_AKM_t4=p_akm))
        reglog(f"OVERID_{key}", f"{y} ~ x | z_g (5 grupos) FE", s["anio"].min(), s["anio"].max(), res["n"],
               np.nan, np.nan, np.nan, J["beta"][0], J["p"], "p=J Hansen cluster (poca potencia con 17 clusters)")
        reglog(f"AKM_{key}", f"{y} ~ x | z FE, EE cluster por grupo de shock", s["anio"].min(), s["anio"].max(),
               res["n"], np.nan, np.nan, np.nan, bz, p_akm, "AKM simplificado (G=5 grupos), indicativo")
    t = pd.DataFrame(rows)
    save(t, "sobreid_J_akm", index=False)
    RES["jak"] = t
    # 2SLS con cada grupo como instrumento unico (valor tasado) - en rotemberg beta_g (just-ID)


# =====================================================================================
# 4-5. COMPRADOR Y NACIONALIDAD
# =====================================================================================
def comprador(P):
    rows = []
    off = 1000
    for key, y, lab in [("trans_extr", "d_ln_trans_extranjeros", "compras de extranjeros"),
                        ("trans_total", "d_ln_trans_total", "compras totales (comparacion)")]:
        s = sample_for(P, y, 2008)
        for tr in (False, True):
            for est in ("OLS", "2SLS"):
                off += 1
                res = fit_iv(s, y, ["x"], ["z"], trends=tr, ols_only=(est == "OLS"), boot=True, seed_off=off)
                r = summarize(f"{key}|{'FE+tend' if tr else 'FE'}|{est}", res)
                r.update(resultado=lab, spec="FE+tend" if tr else "FE", est=est, muestra=f"{s.anio.min()}-{s.anio.max()}")
                rows.append(r)
                log_panel(f"COMP_{key}_{'T' if tr else 'FE'}_{est}", f"{y} ~ x | FE" + (" + tend" if tr else ""), s, res,
                          notas="canal comprador")
    t = pd.DataFrame(rows)
    save(t, "comprador", index=False)
    RES["comp"] = t


def nacionalidad(P):
    G4 = ["europa", "africa", "america", "asia"]
    rows, fsr = [], []
    for key in ("p_tasado", "ipv"):
        y, start, lab = OUTCOMES[key]
        s = P[P.anio >= start].dropna(subset=[y] + [f"x_{g}" for g in G4] + [f"z_{g}" for g in G4]).reset_index(drop=True)
        o = fit_iv(s, y, [f"x_{g}" for g in G4], [f"z_{g}" for g in G4], ols_only=True)
        v = fit_iv(s, y, [f"x_{g}" for g in G4], [f"z_{g}" for g in G4])
        for j, g in enumerate(G4):
            for est, res in (("OLS", o), ("2SLS", v)):
                rows.append(dict(resultado=lab, grupo=g, est=est, n=res["n"], coef=res["beta"][j], EE=res["se"][j],
                                 p=res["p"][j], F_propio=(res["fs"][j]["F"] if est == "2SLS" else np.nan)))
            fsr.append(dict(resultado=lab, grupo=g, F_cluster_4IV=v["fs"][j]["F"],
                            pi_propio=v["fs"][j]["pi"][j], EE_pi_propio=v["fs"][j]["se_pi"][j]))
            # OLS individual
            oi = fit_iv(s, y, [f"x_{g}"], [f"z_{g}"], ols_only=True)
            rows.append(dict(resultado=lab, grupo=g, est="OLS (grupo solo)", n=oi["n"], coef=oi["beta"][0],
                             EE=oi["se"][0], p=oi["p"][0], F_propio=np.nan))
        reglog(f"NAT_{key}_OLS", f"{y} ~ x_europa+x_africa+x_america+x_asia | FE", s.anio.min(), s.anio.max(), o["n"],
               np.nan, np.nan, np.nan, o["beta"][0], o["p"][0], "OLS por grupo; coef = europa")
        reglog(f"NAT_{key}_2SLS", f"{y} ~ x_g (4) | z_g (4), FE", s.anio.min(), s.anio.max(), v["n"],
               np.nan, np.nan, np.nan, v["beta"][0], v["p"][0], "2SLS por grupo; coef = europa")
    save(pd.DataFrame(rows), "nacionalidad", index=False)
    save(pd.DataFrame(fsr), "nacionalidad_primera_etapa", index=False)
    RES["nat"], RES["natfs"] = pd.DataFrame(rows), pd.DataFrame(fsr)


# =====================================================================================
# MAIN + RESUMEN
# =====================================================================================
def fmt(v, d=3):
    return "n/d" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{d}f}"


def resumen(P):
    T = RES["princ"]
    reg = REG.read()
    reg_p = reg.dropna(subset=["p_interes"])
    holm_all = eu.holm(dict(zip(reg_p.modelo_id, reg_p.p_interes)))
    reg_p = reg_p.assign(p_holm=reg_p.modelo_id.map(holm_all), p_bonf=np.minimum(1, reg_p.p_interes * len(reg_p)))
    reg_p[["modelo_id", "coef_interes", "p_interes", "p_holm", "p_bonf"]].to_csv(OUT / "correccion_busqueda.csv", index=False)
    main = T[(T.spec == "FE") & (T.est == "2SLS")].set_index("resultado")
    main_ols = T[(T.spec == "FE") & (T.est == "OLS")].set_index("resultado")
    jak = RES["jak"].set_index("resultado")
    pre = RES["pre"]

    def pre_p(key):
        nm = "ipc_alquiler" if key in ("serpavi", "ipc_alq") else "p_tasado"
        sub = pre[(pre.resultado == nm) & (pre.test.str.startswith("seccion") | pre.test.str.startswith("panel"))]
        sc = pre[(pre.resultado == nm) & pre.test.str.startswith("cuota")]
        return float(min(sub.p.min(), sc.p_Holm_cuotas.min()))
    ev = []
    for key, (y, st, lab) in OUTCOMES.items():
        m = main.loc[lab]
        F, pw, Jp = m["F_1a_etapa"], m["p_WCB_restr"], jak.loc[lab, "J_p"]
        pp = pre_p(key)
        c1, c2, c3, c4 = F >= 10, pp > 0.05, Jp > 0.05, pw < 0.05
        causal = c1 and c2 and c3 and c4
        ev.append(dict(resultado=lab, F_ge10=c1, pretend_no_signif=c2, J_no_rechaza=c3, sobrevive_WCB=c4,
                       p_pretend_min=pp, nivel="causal" if causal else "asociacion"))
    E = pd.DataFrame(ev)
    save(E, "nivel_evidencia", index=False)
    cols = ["resultado", "spec", "est", "n", "coef", "EE_cluster", "p_cluster", "p_WCB_restr", "EE_DK", "F_1a_etapa"]
    L = []
    L.append("# F3 - Inmigracion y precios (P2): resumen\n")
    L.append("Todo se reproduce con `python3 src/f3_inmigracion.py` (semilla 20261009, sin red). Tablas CSV/MD en "
             "`output/f3/`; registro de busqueda en `output/registro_busqueda_f3.csv`.\n")
    L.append("## Diseno\n- x_ct = (pob_extranj_ct - pob_extranj_c,t-1)/pob_total_c,t-1. Coeficiente = variacion % del precio "
             "(Delta ln x 100) por cada 1 punto porcentual de poblacion de flujo neto (1 % de la poblacion total del ano anterior). Calendario: los stocks son a 1 de enero, asi que x del ano t es el cambio neto del stock durante el ano t-1 (no 'en el ano t'), adelantado ~medio ano frente a la media anual de precios.\n"
             "- Instrumento (Card 2001): z_ct = sum_g s_cg,2002 * (dP_g,t)_{-c} / pob_total_c,t-1, cuotas fijas 2002, "
             "flujo nacional del grupo sin la CCAA c (leave-one-out). Grupos (coherentes en el tiempo; Europa = "
             "`pob_europa_sin_espana`, no UE28/UE27): europa (sin Espana), africa, america (sud+centro/Caribe+norte), "
             "asia, otros (oceania+apatridas). Suman `pob_extranj` (dif. max 0,02 %).\n"
             "- FE CCAA + FE anio (principal) y + tendencias lineales por CCAA (robustez). EE cluster CCAA (17), "
             "p con t(16); wild cluster bootstrap restringido (Webb, 9.999; para 2SLS version WRE de Davidson-MacKinnon); "
             "EE Driscoll-Kraay (L=2) como robustez.\n")
    L.append("## Tabla principal (FE CCAA + FE anio; misma muestra OLS/2SLS)\n")
    L.append(eu.df_md(T[(T.spec == "FE")][cols], ".4g", index=False))
    L.append("\n### Robustez (tendencias por CCAA, control ocupados, rezago, sin COVID)\n")
    L.append(eu.df_md(T[(T.spec != "FE")][cols], ".4g", index=False))
    L.append("\n## Primera etapa (2SLS FE, instrumento unico z)\n")
    L.append(eu.df_md(RES["fs"], ".4g", index=False))
    L.append("\nF = Wald cluster-robusto (con un instrumento y un regresor endogeno equivale a Kleibergen-Paap rk F). "
             "Con un instrumento y un regresor endogeno, el F efectivo de Montiel Olea-Pflueger coincide con este F robusto (la comparacion con sus valores criticos depende de la varianza usada, no calculados aqui). La forma reducida (RF_p_cluster) equivale a la prueba Anderson-Rubin y es robusta a instrumentos debiles: no rechaza en ningun resultado. EE y F usan correccion de muestra pequena con K que cuenta los FE de CCAA anidados en el cluster (algo mas conservadora, ~6 % en EE y ~16 % en F frente a linearmodels).\n")
    L.append("## Pesos de Rotemberg (Delta ln valor tasado) y 2SLS con cada grupo como instrumento unico\n")
    L.append(eu.df_md(RES["rot_p_tasado"], ".3g", index=False))
    L.append("\n(Mismo ejercicio para IPV, SERPAVI e IPC alquiler en `rotemberg_*.csv`.) Suma alpha_g * beta_g = 2SLS "
             "(comprobacion numerica incluida en el codigo).\n")
    L.append("## Pretendencias\n")
    L.append(eu.df_md(pre, ".4g", index=False))
    L.append("\n## Sobreidentificacion (J de Hansen con 5 instrumentos por grupo) y AKM simplificado\n")
    L.append(eu.df_md(RES["jak"], ".4g", index=False))
    L.append("\nAdvertencia: con 17 clusters y 5 instrumentos el J (matriz de pesos con 17 vectores de momentos) tiene "
             "muy poca potencia y tiende a no rechazar; ademas los instrumentos por grupo estan fuertemente correlacionados. "
             "El AKM implementado es una version SIMPLIFICADA (scores agregados por grupo de shock, G=5 clusters, t(4)); "
             "no es el AKM completo (sin shocks anidados ni correccion por dependencia temporal de los shocks). "
             "Con 5 grupos el enfoque BHJ (2022, identificacion por shocks cuasi-aleatorios) no es viable: se necesitan "
             "muchos shocks independientes; los shocks de grupo son 5 series temporales muy persistentes.\n")
    L.append("## Canal comprador (compras de extranjeros)\n")
    L.append(eu.df_md(RES["comp"][cols], ".4g", index=False))
    L.append("\n## Desagregacion por nacionalidad (Europa sin Espana, Africa, America, Asia; 'otros' omitido)\n")
    L.append(eu.df_md(RES["nat"], ".4g", index=False))
    L.append("\n")
    L.append(eu.df_md(RES["natfs"], ".4g", index=False))
    L.append("\nSi la F de primera etapa propia es < 10 el 2SLS por grupo no se interpreta; se lee solo el OLS como asociacion.\n")
    L.append("## Nacional (asociacion, sin identificacion)\n")
    lp = RES["lp"]
    for dep in ("ln_ipv", "ln_ipc_alquiler"):
        sub = lp[(lp.dep == dep) & (lp.x == "x_ext")][["h", "coef", "EE_HAC", "p", "n"]]
        L.append(f"### Proyecciones locales {dep} sobre d4_ln_pob_extranj (muestra comun {lp[(lp.dep == dep)].muestra.iloc[0]})\n")
        L.append(eu.df_md(sub, ".4g", index=False))
        L.append("\n")
    L.append("Figura: `irf_nacional.png`. Variantes con d4_ln_pob_total y con el flujo Delta4/pob. total en `nacional_lp.csv`. "
             "La poblacion es semestral interpolada antes de 2021 y el IPV/EPA no estan desestacionalizados (dummies q2-q4).\n")
    L.append("### Flujo anual (N pequeno)\n")
    L.append(f"Muestra {RES['anual_rng']}, N = {RES['anual_n']}: inferencia HAC(4) con N tan pequeno es poco fiable; "
             "solo orientativo.\n")
    L.append(eu.df_md(RES["anual"], ".4g", index=False))
    L.append("\n### Separabilidad empleo-inmigracion\n")
    L.append(eu.df_md(RES["sep"], ".3g", index=False))
    L.append("\n## Conclusion P2 y nivel de evidencia\n")
    L.append("Regla: 'causal' solo si F>=10 Y pretendencias no significativas Y J no rechaza Y sobrevive al wild bootstrap; "
             "si no, 'asociacion'. (Pretendencias: minimo de los p de la seccion cruzada y el panel con zbar 2008-25 y de los p de Holm de las cuotas 2002 una a una; para IPV y "
             "valor tasado se usa la pretendencia del valor tasado; para alquiler, la del IPC alquiler.)\n")
    L.append(eu.df_md(E, ".4g", index=False))
    for lab_ in main.index:
        m, o = main.loc[lab_], main_ols.loc[lab_]
        L.append(f"\n- {lab_}: OLS {fmt(o.coef)} (EE {fmt(o.EE_cluster)}), 2SLS {fmt(m.coef)} (EE {fmt(m.EE_cluster)}; "
                 f"p cluster {fmt(m.p_cluster)}, p WCB {fmt(m.p_WCB_restr)}; F {fmt(m.F_1a_etapa, 1)}) "
                 f"= variacion % del precio por flujo del 1 % de la poblacion total.")
    ic = []
    for lab_ in main.index:
        m = main.loc[lab_]
        tc = stats.t.ppf(0.975, 16)
        ic.append(dict(resultado=lab_, coef_2SLS=m.coef, IC95_lo=m.coef - tc * m.EE_cluster, IC95_hi=m.coef + tc * m.EE_cluster))
    ICd = pd.DataFrame(ic)
    save(ICd, "ic95_2sls_principal", index=False)
    jk = RES["jk"].set_index("excluida")
    bal = jk.loc[[i_ for i_ in jk.index if "Balears" in i_], "coef"]
    ipv = ICd[ICd.resultado == "IPV (precio)"].iloc[0]
    sub = RES["sub0307"]
    L.append("\n### Intervalos de confianza 95 % del 2SLS (t(16), cluster)\n")
    L.append(eu.df_md(ICd, ".3g", index=False))
    L.append("\n\nComparabilidad (docs/literatura.md): Saiz (2007, EE. UU.): entrada = 1 % de la poblacion -> alquileres y "
             "valores ~ +1 %. Sa (2015, RU, version de trabajo IZA DP 5893): -1,6 % por 1 % de poblacion. Gonzalez y Ortega "
             "(2013, Espana 1998-2008): flujo medio del 17 % de la poblacion en edad de trabajar -> precios ~ +52 % "
             "(cociente simple ~ 3 puntos % por punto de flujo; derivado aqui, denominador distinto). "
             f"El IC95 % del 2SLS del IPV es [{ipv.IC95_lo:.2f}; {ipv.IC95_hi:.2f}]: EXCLUYE +1 (Saiz) y ~3 (Gonzalez-Ortega); "
             "es compatible con el signo negativo de Sa (2015). Para el valor tasado y el SERPAVI los IC si incluyen +1 y "
             "valores negativos. La discrepancia se explica por diseno y periodo, no se presenta como error de calculo: "
             "(i) la muestra del IPV es 2008+ (crisis y recuperacion), no el auge 1998-2008 de Gonzalez-Ortega; (ii) la "
             "estimacion es en diferencias anuales con flujo neto del padron (resta nacionalizaciones); (iii) el peso de "
             "Rotemberg recae en la cuota europea de 2002 (Europa alpha 0,31 en IPV, 0,43 en valor tasado; beta_g de Europa "
             "negativo y significativo), muy ligada a costa e islas con demanda de residentes y turistica; el jackknife sin "
             f"Baleares da {', '.join(f'{v:.2f}' for v in bal)} para el valor tasado (frente a {main.loc['valor tasado'].coef:.2f}). "
             f"En el auge 2003-07 el 2SLS del valor tasado es {sub['coef']:.2f} (EE {sub['se']:.2f}, F {sub['F']:.1f}; instrumento debil, "
             "especificacion registrada como PAN_p_tasado_2003_07). En nacional, la comparacion en la misma unidad es la "
             "variante x_flow (Delta4 extranjeros / pob. total) de `nacional_lp.csv`; el coeficiente anual nacional de "
             "flujo (~10) es covariacion ciclica auge-crisis con N=17, no un efecto. En alquiler (IPC) las estimaciones son "
             "positivas (~0,4-0,5) pero fragiles (ver Problemas abiertos).\n")
    L.append(f"\n## Busqueda de especificaciones\nEspecificaciones registradas en F3: **{len(reg)}** "
             f"({len(reg_p)} con p de interes). Correccion de Holm/Bonferroni sobre TODAS ellas en `correccion_busqueda.csv`. "
             "Para las 4 estimaciones 2SLS principales (FE) el p-valor del wild bootstrap y el ajustado:\n")
    mm = []
    for key in OUTCOMES:
        mid = f"PAN_{key}_FE_2SLS"
        r = reg_p[reg_p.modelo_id == mid]
        if len(r):
            mm.append(dict(modelo=mid, coef=r.coef_interes.iloc[0], p=r.p_interes.iloc[0], p_holm=r.p_holm.iloc[0],
                           p_bonferroni=r.p_bonf.iloc[0]))
    L.append(eu.df_md(pd.DataFrame(mm), ".4g", index=False))
    L.append("\nLa mayoria de filas son robusteces/diagnosticos no independientes; la correccion sobre todas es muy conservadora. "
             "RMSE fuera de muestra no aplica en F3 (columna vacia).\n")
    L.append("## Problemas abiertos\n"
             "- Canal comprador: el coeficiente sobre compras de extranjeros es NEGATIVO y muy grande (OLS -19, 2SLS -42). "
             "`trans_extranjeros` = compradores extranjeros RESIDENTES (MIVAU 340101i0), con salto 2008->2009 en la serie. "
             "Pero sin 2008-09 (2010+) sigue en -24,7 (EE 6,4) y en compras totales en -16,5 (EE 5,2): no es solo un artefacto "
             "de la serie. Es una senal de posible VIOLACION DE LA EXCLUSION (z correlacionado con el ciclo inmobiliario "
             "local; la inmigracion no puede explicar un desplome de transacciones de esa magnitud) y refuerza leer todo P2 "
             "como asociacion. (Cifras sin 2008-09 de la revision independiente, docs/revision_f3.md; no son salida de este script.)\n"
             "- IPV: sin efecto distinguible de cero en OLS; el 2SLS es negativo y su IC95 % excluye +1. En compraventas "
             "(IPV, valor tasado) no hay ni asociacion significativa: formulacion correcta = 'sin evidencia de efecto "
             "positivo'. Alquiler IPC: asociacion positiva en OLS (0,53; WCB p = 0,004) que NO sobrevive a Holm sobre las "
             "149 especificaciones (Holm 0,59); 2SLS 0,44 no significativo (WCB p = 0,12); el IPC alquiler no estaba en el "
             "diseno prefijado (se anade despues, ver docs/decisiones.md); el resultado lo mueve America, cuya cuota 2002 "
             "tiene pretendencia significativa.\n"
             "- Pretendencias: la ventana 2003-07 esta DENTRO de la muestra de estimacion del valor tasado y del IPC alquiler "
             "(2003+), asi que es 'correlacion en los primeros anos de la muestra', no una prueba pre; solo es pre para el IPV (2008+). "
             "La seccion cruzada y el panel con FE de anio dan el mismo coeficiente (no son pruebas independientes). La "
             "pretendencia 1996-2001 (anterior al ano base) NO se puede computar aqui: `data/processed` no contiene precios por "
             "CCAA antes de 2002 (el valor tasado por CCAA desde 1995 solo esta en data/raw/mivau_valor_tasado_nacional_ccaa_prov.csv, "
             "y la regla es leer solo de processed). La revision independiente con raw obtuvo 9,46 (EE HC3 6,26; p = 0,13) sobre zbar "
             "y p entre 0,43 y 0,996 sobre las cuotas una a una: no rechaza pero es imprecisa. Pendiente de incorporar a processed.\n"
             "- 17 clusters: inferencia cluster y J de Hansen poco fiables; el wild bootstrap lo mitiga solo en parte.\n"
             "- Exclusion del instrumento: la historia de asentamiento (cuotas 2002) puede correlacionarse con demanda local "
             "(burbuja inmobiliaria 2002-07, turismo/retirados en la costa) y los flujos de grupo se mueven por el ciclo "
             "nacional comun; los FE de anio absorben lo comun, no lo heterogeneo. Ver pretendencias y Rotemberg.\n"
             "- Solo 5 grupos (de hecho 4 relevantes): imposible aplicar BHJ; AKM solo simplificado.\n"
             "- x_ct mide variacion del stock padronal (incluye nacionalizaciones, cambios de padron y regularizaciones); "
             "no es flujo migratorio bruto. Las nacionalizaciones mueven personas de 'extranjero' a 'espanol'.\n"
             "- IPV por CCAA solo desde 2007 (resultados 2008+), SERPAVI 2011-2024 con huecos (Navarra, Pais Vasco: "
             "N desequilibrado), valor tasado de Navarra falta 2015-18.\n"
             "- El efecto sobre el precio en la diferencia anual (con x adelantada ~medio ano) no recoge ajustes de oferta a medio plazo; el rezago de x se "
             "incluye solo como robustez.\n"
             "- Sin variable de paro por CCAA: las correlaciones de cuotas usan tasa de ocupados/poblacion 2002.\n"
             "- Referencias metodologicas citadas (Webb; Davidson-MacKinnon WRE; Driscoll-Kraay; Montiel Olea-Pflueger; Sanderson-Windmeijer; Kleibergen-Paap; Hansen) NO estan en docs/literatura.md: NO VERIFICADAS.\n"
             "- Panel nacionalidad: 2SLS con 4 endogenas y 4 instrumentos muy correlacionados, F condicional "
             "(Sanderson-Windmeijer) no implementado; se muestra F conjunta.\n")
    (OUT / "resumen_f3.md").write_text("\n".join(L), encoding="utf-8")


def main():
    nacional()
    P = build_panel()
    P.to_csv(OUT / "panel_construido_x_z.csv", index=False)
    principal(P)
    for k in OUTCOMES:
        rotemberg(P, k)
    pretendencias(P)
    sobreid_akm(P)
    comprador(P)
    nacionalidad(P)
    # figura primera etapa (valor tasado)
    r = RES["cache"][("p_tasado", "FE", "2SLS")]
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.scatter(r["Zt"][:, 0], r["Xt"][:, 0], s=8)
    ax.set_xlabel("z residualizado (FE)")
    ax.set_ylabel("x residualizado (FE)")
    ax.set_title(f"Primera etapa (valor tasado): F cluster = {r['fs'][0]['F']:.1f}")
    fig.tight_layout()
    fig.savefig(OUT / "primera_etapa.png", dpi=130)
    plt.close(fig)
    resumen(P)
    print(f"F3 ok. Especificaciones registradas: {NSPEC[0]}")


if __name__ == "__main__":
    main()
