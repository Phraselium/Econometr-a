"""V7-R4a: modelos explicativos regionales (nucleo). Capa C4, asociacion de largo plazo (sin lenguaje causal).
Informativo, muestra ya vista en v1. Determinista, sin red, SEED=20261010. Usa panel_tools (validado en R2) sin reimplementarlo.
Uso: python3 src/v7/r4a_run.py [--smoke]
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v7"))
import panel_tools as pt  # noqa: E402
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
SEED = pt.SEED
SMOKE = "--smoke" in sys.argv
OUT = ROOT / "output" / "v7" / ("R4_smoke" if SMOKE else "R4")
B_PMG, B_WL, REPS, B_WILD = (19, 19, 50, 99) if SMOKE else (199, 199, 500, 999)
FECHA = "2026-10-10"
ROT = "informativo, muestra ya vista en v1"
CRIT_E2 = -8.83
COVID = ["2020Q2", "2020Q3", "2020Q4"]
EPA_VARS = {"ln_ocupados", "tasa_paro_epa"}
SPECS = {  # (mercado, spec) -> (y, x, control de corto plazo)
    ("alquiler", "A"): ("ln_ipc_alquiler", ["ln_ocupados", "ln_pob_total"], "ln_hip_importe"),
    ("alquiler", "B"): ("ln_ipc_alquiler", ["tasa_paro_epa"], "ln_hip_importe"),
    ("compra", "A"): ("ln_ipv", ["ln_ocupados", "ln_hip_importe", "ln_pob_total"], "ln_compraventas"),
    ("compra", "B"): ("ln_ipv", ["tasa_paro_epa", "ln_hip_importe"], "ln_compraventas"),
}
# hipotesis: id -> (mercado, spec, variable, signo H1)
HIPO = {"H7-A1": ("alquiler", "A", "ln_ocupados", 1), "H7-A2": ("alquiler", "A", "ln_pob_total", 1),
        "H7-A3": ("alquiler", "B", "tasa_paro_epa", -1), "H7-C1": ("compra", "A", "ln_ocupados", 1),
        "H7-C2": ("compra", "A", "ln_hip_importe", 1), "H7-C3": ("compra", "A", "ln_pob_total", 1),
        "H7-C4": ("compra", "B", "tasa_paro_epa", -1)}
FAM = {"alquiler": "F-A", "compra": "F-C"}
UNIDAD = {"tasa_paro_epa": "pp de paro"}
UVARS = ["ln_ipc_alquiler", "ln_ipv", "ln_ocupados", "tasa_paro_epa", "ln_pob_total", "ln_pob_extranj", "ln_hip_importe", "ln_compraventas"]
reg = Registry(OUT / "registro.csv")


# ------------------------------------------------------------------ datos
def load():
    d = pd.read_csv(ROOT / "data/processed/v7/panel_ccaa_q_v7.csv", dtype={"codigo_ine_ccaa": str})
    return d.sort_values(["codigo_ine_ccaa", "trimestre"]).reset_index(drop=True)


def wide(d, var, qs):
    return d.pivot(index="codigo_ine_ccaa", columns="trimestre", values=var)[qs].to_numpy(float)


def adjust_breaks(x, qs, epa):
    """Quita en DIFERENCIAS los pulsos COVID (2020T2-T4) y, en variables EPA, el escalon 2021T1 (pulso en la diferencia); reacumula."""
    out = np.empty_like(x)
    dts = np.array(qs[1:])
    D = np.column_stack([(dts == c).astype(float) for c in COVID] + ([(dts == "2021Q1").astype(float)] if epa else []))
    for i in range(x.shape[0]):
        dx = np.diff(x[i])
        Z = np.column_stack([np.ones(len(dx)), D])
        b = np.linalg.lstsq(Z, dx, rcond=None)[0]
        dx2 = dx - D @ b[1:]
        out[i] = x[i, 0] + np.r_[0.0, np.cumsum(dx2)]
    return out


def build(d, mercado, spec, t0="2007Q1"):
    yv, xv, cv = SPECS[(mercado, spec)]
    cols = [yv] + xv + [cv]
    ok = d.groupby("trimestre")[cols].apply(lambda g: g.notna().all().all())
    qs = [q for q in sorted(d.trimestre.unique()) if ok[q]]
    codes = sorted(d.codigo_ine_ccaa.unique())
    y = adjust_breaks(wide(d, yv, qs), qs, yv in EPA_VARS)
    X = np.stack([adjust_breaks(wide(d, v, qs), qs, v in EPA_VARS) if v != "ln_pob_total" else wide(d, v, qs) for v in xv], 2)
    c = wide(d, cv, qs)
    return dict(y=y, X=X, ctrl=c, qs=qs, codes=codes, yv=yv, xv=xv, cv=cv, per=f"{qs[0]}-{qs[-1]}")


def sub(S, n):  # submuestra smoke
    return dict(S, y=S["y"][:n], X=S["X"][:n], ctrl=S["ctrl"][:n], codes=S["codes"][:n])


# ------------------------------------------------------------------ ADF/KPSS/ZA
def integracion(d, outdir):
    from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews
    rows = []
    qs = sorted(d.trimestre.unique())
    for v in UVARS:
        for cod, g in d.groupby("codigo_ine_ccaa"):
            s = g.set_index("trimestre")[v].reindex(qs).dropna().to_numpy(float)
            r = dict(variable=v, codigo_ine_ccaa=cod, T=len(s), nota="pob anual asignada/interpolada" if "pob" in v else "")
            for lab, z in (("nivel", s), ("dif", np.diff(s))):
                reg_t = ("c", "ct") if lab == "nivel" else ("c",)
                for rg in reg_t:
                    r[f"adf_{rg}_p_{lab}"] = adfuller(z, regression=rg, autolag="BIC")[1]
                    try:
                        r[f"kpss_{rg}_p_{lab}"] = kpss(z, regression=rg, nlags="auto")[1]
                    except Exception:
                        r[f"kpss_{rg}_p_{lab}"] = np.nan
                try:
                    za = zivot_andrews(z, regression="c", autolag="AIC")
                    r[f"za_p_{lab}"], r[f"za_break_{lab}"] = za[1], int(za[4])
                except Exception:
                    r[f"za_p_{lab}"], r[f"za_break_{lab}"] = np.nan, -1
            n_ = r["adf_c_p_nivel"] >= .05 and r["kpss_c_p_nivel"] < .05
            i0 = r["adf_c_p_nivel"] < .05 and r["kpss_c_p_nivel"] >= .05
            dif = r["adf_c_p_dif"] < .05
            r["clasif"] = "I(1)" if (n_ and dif) else ("I(0)" if i0 else "ambiguo")
            rows.append(r)
            reg.log("R4-integracion", f"UR_{v}_{cod}", f"ADF/KPSS/ZA {v}", qs[0], qs[-1], len(s), np.nan, np.nan, np.nan, np.nan, r["adf_c_p_nivel"], r["adf_c_p_dif"], "p ADF nivel/dif; informativo")
    df = pd.DataFrame(rows)
    return df


def panel_ur(S, cvcache):
    """CIPS (apoyo) de y y de cada x, en nivel y diferencias; p simulado (cola izquierda), p=1 y SBC."""
    rows = []
    N = S["y"].shape[0]
    series = {S["yv"]: S["y"]} | {v: S["X"][:, :, j] for j, v in enumerate(S["xv"])}
    for v, z in series.items():
        for lab, zz in (("nivel", z), ("dif", np.diff(z, axis=1))):
            for sbc in (False, True):
                st = pt.cips(zz, p=1, sbc=sbc)
                key = (N, zz.shape[1], sbc)
                if key not in cvcache:
                    cvcache[key] = pt.cips_critical_values(N, zz.shape[1], p=1, reps=REPS, sbc=sbc)["sim"]
                rows.append(dict(variable=v, forma=lab, test="CIPS" + ("_SBC" if sbc else "_p1"), estadistico=st,
                                 p=pt.sim_pvalue(st, cvcache[key]), nota="apoyo; sobrerrechaza con componente I(0) grande (V12); series ajustadas por dummies"))
    return rows


# ------------------------------------------------------------------ bounds y cointegracion
def bounds_cv(k, n, reps, seed=SEED):
    """Valores criticos 5 % del F de PSS (caso III) simulados: cotas I(0) (x iid) e I(1) (x paseo aleatorio); H0: phi=0, bx=0."""
    rng = np.random.default_rng(seed + k)
    out = {}
    for lab, cum in (("I0", False), ("I1", True)):
        fs = []
        for _ in range(reps):
            y = np.cumsum(rng.standard_normal(n + 6))
            X = rng.standard_normal((n + 6, k))
            X = np.cumsum(X, 0) if cum else X
            fs.append(bounds_F(y, X, 1, 1, 1, s=1)[0])
        out[lab] = float(np.quantile(fs, .95))
    return out


def bounds_F(y, X, p, q, extra_start=0, s=None, ctrl=None):
    import statsmodels.api as sm
    s = max(p, q, 1) if s is None else s
    d, L, W = pt._build(y, X, p, q, s, ctrl)
    Z = np.hstack([L, W])
    res = sm.OLS(d, Z).fit()
    k = X.shape[1]
    R = np.zeros((k + 1, Z.shape[1]))
    R[np.arange(k + 1), np.arange(k + 1)] = 1
    f = res.f_test(R)
    return float(f.fvalue), res


def cointegracion(S, p, q, cvb):
    ys, Xs = pt.cs_demean(S["y"], S["X"])
    N, T = ys.shape
    k = Xs.shape[2]
    rows = []
    wl = pt.westerlund(ys, Xs, p=1, B=B_WL)
    for s_ in ("Gt", "Ga", "Pt", "Pa"):
        rows.append(dict(nivel="panel", test="tipo Westerlund " + s_, estadistico=wl[s_], p=wl["p"][s_], decision="",
                         nota="baja potencia con ajuste lento (0,06-0,29): no rechazo no es evidencia de ausencia; datos con demeaning"))
    pe = pt.pedroni(ys, Xs, p=1, reps=REPS)
    for s_ in ("panel_adf", "group_adf"):
        rows.append(dict(nivel="panel", test="Pedroni " + s_, estadistico=pe[s_], p=pe["p"][s_], decision="",
                         nota="p simulado con paseos aleatorios independientes; contraste principal de E1"))
    key = (k, T)
    if key not in cvb:
        cvb[key] = bounds_cv(k, T - max(p, q, 1) - 1, REPS)
    cv = cvb[key]
    for i, cod in enumerate(S["codes"]):
        f, _ = bounds_F(S["y"][i], S["X"][i], p, q)
        dec = "cointegra" if f > cv["I1"] else ("sin cointegracion" if f < cv["I0"] else "inconcluso")
        rows.append(dict(nivel="region", codigo_ine_ccaa=cod, test="ARDL bounds F (PSS 2001, caso III)", estadistico=f, p=np.nan,
                         decision=dec, nota=f"cotas 5 % simuladas I0={cv['I0']:.2f} I1={cv['I1']:.2f} (no tabuladas de PSS)"))
    return rows, wl, pe


# ------------------------------------------------------------------ estimacion
def tinfo(th, se, N, signo=None):
    t = th / se
    p2 = 2 * stats.t.sf(abs(t), N - 1)
    p1 = np.nan if signo is None else (p2 / 2 if np.sign(t) == signo else 1 - p2 / 2)
    h = stats.t.ppf(.975, N - 1) * se
    return t, p2, p1, th - h, th + h


def estimar(S, p, q, boot):
    ys, Xs = pt.cs_demean(S["y"], S["X"])
    N = ys.shape[0]
    mg_ = pt.mg(ys, Xs, p, q)
    pm = pt.pmg(ys, Xs, p, q)
    out = dict(MG_dm=dict(theta=mg_["theta"], se=mg_["se_theta"], phi=mg_["phi"], se_phi=mg_["se_phi"], phi_i=mg_["phi_i"], mg=mg_))
    if boot:
        bb = pt.pmg_bootstrap(S["y"], S["X"], p, q, B=B_PMG, demean=True)
        se_pm = bb["se_theta"]
    else:
        se_pm = pm["se_theta"]
    out["PMG_dm"] = dict(theta=pm["theta"], se=se_pm, phi=pm["phi"], se_phi=pm["se_phi"], boot=boot, conv=pm["converged"], pm=pm)
    df = pt.dfe(ys, Xs, p, q)
    out["DFE"] = dict(theta=df["theta"], se=df["se_theta"], phi=df["phi"], se_phi=df["se_phi"])
    out["haus"] = pt.hausman_mg_pmg(mg_, pm)
    return out


def dfe_inferencia(S, p, q):
    """Coeficientes ECM de DFE (phi y x_{t-1}) con wild cluster Webb y Driscoll-Kraay (datos con demeaning)."""
    ys, Xs = pt.cs_demean(S["y"], S["X"])
    N = ys.shape[0]
    k = Xs.shape[2]
    s = pt._start(p, q)
    ds, Zs = [], []
    for i in range(N):
        d, L, W = pt._build(ys[i], Xs[i], p, q, s)
        ds.append(d)
        Zs.append(np.hstack([L, W[:, 1:]]))
    n = len(ds[0])
    D, Z, cl = np.concatenate(ds), np.vstack(Zs), np.repeat(np.arange(N), n)
    dk = pt.driscoll_kraay(D, Z, N, n)
    rows = []
    for j, nm in enumerate(["phi"] + [f"b_{v}" for v in S["xv"]]):
        w = pt.wild_cluster_boot(D, Z, cl, j=j, B=B_WILD)
        pdk = 2 * stats.t.sf(abs(dk["t"][j]), n - 1)
        rows.append(dict(coef_ecm=nm, coef=w["coef"], t_cluster=w["t"], p_wild_webb=w["p_boot"], ee_dk=dk["se"][j], t_dk=dk["t"][j], p_dk=pdk,
                         nota="coeficiente del ECM (no theta); wild cluster restringido, Webb, B=%d" % B_WILD))
    return rows


def region_ecm(S, i, ys, Xs, p, q):
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import acorr_breusch_godfrey, breaks_cusumolsresid, het_breuschpagan, linear_reset
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    k = Xs.shape[2]
    c = S["ctrl"] - S["ctrl"].mean(0, keepdims=True)
    cx = np.r_[np.nan, np.diff(c[i])][:, None]
    s = pt._start(p, q)
    d, L, W = pt._build(ys[i], Xs[i], p, q, s, cx)
    Z = np.hstack([L, W])
    names = ["phi"] + [f"b_{v}" for v in S["xv"]] + ["const"]
    for j in range(q):
        names += [f"d_{v}_L{j}" for v in S["xv"]]
    names += [f"d_y_L{j}" for j in range(1, p)] + ["d_" + S["cv"]]
    res = sm.OLS(d, Z).fit()
    bhat, se = res.params, res.bse
    th, Vt = pt._theta_delta(bhat, res.cov_params(), k)
    r = dict(codigo_ine_ccaa=S["codes"][i], n=len(d))
    ph = bhat[0]
    r.update(phi=ph, ee_phi=se[0], semivida_trim=(np.log(.5) / np.log(1 + ph) if -1 < ph < 0 else np.nan))
    for j, v in enumerate(S["xv"]):
        r[f"theta_{v}"] = th[j]
        r[f"ee_theta_{v}"] = np.sqrt(Vt[j, j])
    bg = acorr_breusch_godfrey(res, nlags=4)
    bp = het_breuschpagan(res.resid, Z)
    jb = stats.jarque_bera(res.resid)
    try:
        rs = linear_reset(res, power=2, use_f=True)
        rs_p = float(rs.pvalue)
    except Exception:
        rs_p = np.nan
    cu = breaks_cusumolsresid(res.resid, ddof=Z.shape[1])
    xl = np.column_stack([np.ones(Xs.shape[1]), S["X"][i]])
    vif = [variance_inflation_factor(xl, j + 1) for j in range(k)] if k > 1 else [1.0]
    h = len(d) // 2
    halves = []
    for sl in (slice(0, h), slice(h, None)):
        rh = sm.OLS(d[sl], Z[sl]).fit()
        halves.append((rh.params[0], pt._theta_delta(rh.params, rh.cov_params(), k)[0]))
    diag = dict(codigo_ine_ccaa=S["codes"][i], BG_p=bg[1], BP_p=bp[1], JB_p=jb[1], RESET_p=rs_p, CUSUM_stat=cu[0], CUSUM_p=cu[1],
                CUSUM_rechaza5=bool(cu[1] < .05), VIF_max=max(vif), r2_adj=res.rsquared_adj, phi_mitad1=halves[0][0], phi_mitad2=halves[1][0],
                cambio_signo_phi=bool(np.sign(halves[0][0]) != np.sign(halves[1][0])))
    for j, v in enumerate(S["xv"]):
        diag[f"VIF_{v}"] = vif[j]
        diag[f"theta_{v}_m1"], diag[f"theta_{v}_m2"] = halves[0][1][j], halves[1][1][j]
    corto = [dict(codigo_ine_ccaa=S["codes"][i], coef=nm, estimacion=bhat[j], ee=se[j], t=bhat[j] / se[j], p=res.pvalues[j])
             for j, nm in enumerate(names) if nm.startswith("d_") or nm == "phi"]
    return r, diag, corto, dict(names=names, b=bhat, se=se, theta=th, res=res)


def bai_perron(yb, Xb, qs, mmax=3, trim=.15):
    T = len(yb)
    h = max(int(trim * T), Xb.shape[1] + 3)
    Zf = np.column_stack([np.ones(T), Xb])

    def ssr(a, b):
        z, v = Zf[a:b], yb[a:b]
        bb = np.linalg.lstsq(z, v, rcond=None)[0]
        return float(((v - z @ bb) ** 2).sum())

    S = {(a, b): ssr(a, b) for a in range(T) for b in range(a + h, T + 1)}
    best = {0: (S[(0, T)], [])}
    kk = Zf.shape[1]
    dp = {(0, b): (S[(0, b)], []) for b in range(h, T + 1)}
    for m in range(1, mmax + 1):
        nd = {}
        for b in range(h * (m + 1), T + 1):
            cand = [(dp[(m - 1, a)][0] + S[(a, b)], dp[(m - 1, a)][1] + [a]) for a in range(h * m, b - h + 1) if (m - 1, a) in dp]
            if cand:
                nd[(m, b)] = min(cand, key=lambda z: z[0])
        dp.update(nd)
        if (m, T) in dp:
            best[m] = dp[(m, T)]
    bic = {m: T * np.log(v[0] / T) + ((m + 1) * kk + m) * np.log(T) for m, v in best.items()}
    mb = min(bic, key=bic.get)
    return dict(m_bic=mb, fechas=[qs[a] for a in best[mb][1]], bic={m: float(v) for m, v in bic.items()},
                fechas_m1=[qs[a] for a in best[1][1]] if 1 in best else [])


# ------------------------------------------------------------------ niveles
def niveles(d):
    s = pd.read_csv(ROOT / "data/raw/pdf/serpavi_ccaa.csv", dtype={"codigo": str})
    s = s[(s.periodo == 2024) & (s.tipologia == "VC") & (s.variable == "alquiler_mes") & (s.estadistico == "mediana")]
    alq = s.set_index("codigo")["valor"].to_dict()
    cmp_ = d[d.trimestre.str.startswith("2025")].groupby("codigo_ine_ccaa")["p_tasado"].mean().to_dict()
    return alq, cmp_


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for m in ("alquiler", "compra"):
        (OUT / m).mkdir(exist_ok=True)
    d = load()
    alq, cmp_ = niveles(d)
    ur = integracion(d, OUT)
    cvcache, cvb = {}, {}
    lp_all, hip_rows, e2_rows, res_json = [], [], [], {}
    region_tables = {m: dict(corto=[], diag=[], coint=[], dfe=[], ur=[], eq=[], bp=[], reg_phi=[]) for m in ("alquiler", "compra")}
    est_main = {}
    for (m, sp), _v in SPECS.items():
        S = build(d, m, sp)
        if SMOKE:
            S = sub(S, 6)
        N, T = S["y"].shape
        ys, Xs = pt.cs_demean(S["y"], S["X"])
        p, q = pt.select_lags_sbc(ys, Xs)
        T_ = region_tables[m]
        for r in ur.to_dict("records"):
            pass
        T_["ur"] += [dict(spec=sp) | r for r in panel_ur(S, cvcache)]
        rows, wl, pe = cointegracion(S, p, q, cvb)
        T_["coint"] += [dict(spec=sp, rezago=f"({p},{q})", N=N, T=T, periodo=S["per"]) | r for r in rows]
        for r in rows:
            if r["nivel"] == "panel":
                reg.log("R4-cointegracion", f"{m}_{sp}_{r['test']}", r["test"], S["qs"][0], S["qs"][-1], N * T, np.nan, np.nan, np.nan, np.nan, r["estadistico"], r["p"], ROT)
        lagsets = [("SBC", p, q, True), ("(1,1)", 1, 1, False), ("(2,2)", 2, 2, False)]
        ests = {}
        for lab, pp, qq, boot in lagsets:
            ests[lab] = estimar(S, pp, qq, boot)
        cs = pt.cs_dl(S["y"], S["X"], pT=4)
        est_main[(m, sp)] = (ests["SBC"], cs, S, (p, q))
        for lab, pp, qq, boot in lagsets:
            E = ests[lab]
            lab_full = f"{lab}=({pp},{qq})" if lab == "SBC" else lab
            for est in ("MG_dm", "PMG_dm", "DFE"):
                for j, v in enumerate(S["xv"]):
                    th, se = E[est]["theta"][j], E[est]["se"][j]
                    hs = [h for h, z in HIPO.items() if z[:3] == (m, sp, v)]
                    sg = HIPO[hs[0]][3] if hs else None
                    t, p2, p1, lo, hi = tinfo(th, se, N, sg)
                    nota = f"{ROT}; asociacion de largo plazo"
                    if est == "PMG_dm":
                        nota += "; IC aproximado (cobertura simulada ~0,88)" + ("; EE bootstrap B=%d (puede inflarse por replicas extremas: PMG inestable con ajuste lento)" % B_PMG if boot else "; EE informacion (sin bootstrap)")
                    if est == "DFE":
                        nota += "; robustez; EE agrupados por unidad"
                    lp_all.append(dict(mercado=m, spec=sp, rezago=lab_full, estimador=est, variable=v, hipotesis=hs[0] if hs else "", coef=th, ee=se, t=t,
                                       p_bilateral=p2, p_H1=p1, ic95_lo=lo, ic95_hi=hi, N=N, T=T, periodo=S["per"], nota=nota))
                    reg.log("R4-largo-plazo", f"{m}_{sp}_{lab_full}_{est}_{v}", f"{S['yv']} ~ {'+'.join(S['xv'])} | ARDL{(pp, qq)} {est}", S["qs"][0], S["qs"][-1], N * T,
                            np.nan, np.nan, np.nan, np.nan, th, p2, nota)
        for j, v in enumerate(S["xv"]):
            hs = [h for h, z in HIPO.items() if z[:3] == (m, sp, v)]
            sg = HIPO[hs[0]][3] if hs else None
            th, se = cs["theta"][j], cs["se_theta"][j]
            t, p2, p1, lo, hi = tinfo(th, se, N, sg)
            lp_all.append(dict(mercado=m, spec=sp, rezago="pT=4", estimador="CS-DL", variable=v, hipotesis=hs[0] if hs else "", coef=th, ee=se, t=t, p_bilateral=p2,
                               p_H1=p1, ic95_lo=lo, ic95_hi=hi, N=N, T=T, periodo=S["per"], nota=f"{ROT}; asociacion; sin demeaning (medias transversales y 4 retardos)"))
            reg.log("R4-largo-plazo", f"{m}_{sp}_CS-DL_{v}", f"{S['yv']} CS-DL pT=4", S["qs"][0], S["qs"][-1], N * T, np.nan, np.nan, np.nan, np.nan, th, p2, ROT)
        E = ests["SBC"]
        # Hausman, E2
        tphi = E["MG_dm"]["phi"] / E["MG_dm"]["se_phi"]
        jk = pt.jackknife_phi(pt.mg, ys, Xs, p=p, q=q)
        e2_rows.append(dict(mercado=m, spec=sp, rezago=f"({p},{q})", phi_MG=E["MG_dm"]["phi"], ee=E["MG_dm"]["se_phi"], t_MG=tphi, vc5=CRIT_E2,
                            rechaza=bool(tphi < CRIT_E2), phi_jackknife_mitades=jk, hausman_H=E["haus"]["H"], hausman_p=E["haus"]["p"], hausman_pd=E["haus"]["pd"],
                            wl_Gt_p=wl["p"]["Gt"], wl_Pt_p=wl["p"]["Pt"], pedroni_panel_p=pe["p"]["panel_adf"], pedroni_group_p=pe["p"]["group_adf"],
                            nota="H7-E2: t de MG vs -8,83 (sesgo de phi en muestra finita declarado); Hausman con varianza del MG, potencia ~0,61: sin afirmar homogeneidad"))
        reg.log("R4-E2", f"{m}_{sp}_phi", "t_MG(phi) vs -8,83", S["qs"][0], S["qs"][-1], N * T, np.nan, np.nan, np.nan, np.nan, E["MG_dm"]["phi"], np.nan, ROT)
        # DFE inferencia
        T_["dfe"] += [dict(spec=sp, rezago=f"({p},{q})") | r for r in dfe_inferencia(S, p, q)]
        # colinealidad
        T_.setdefault("col", []).append((sp, S))
        # por region
        for i in range(N):
            r, dg, co, ex = region_ecm(S, i, ys, Xs, p, q)
            T_["reg_phi"].append(dict(spec=sp, rezago=f"({p},{q})") | r)
            T_["diag"].append(dict(spec=sp) | dg)
            T_["corto"] += [dict(spec=sp) | c_ for c_ in co]
            T_["eq"].append((sp, i, ex, S, p, q))
            reg.log("R4-region", f"{m}_{sp}_{S['codes'][i]}", f"ECM {S['yv']} region {S['codes'][i]} ARDL{(p, q)}", S["qs"][0], S["qs"][-1], r["n"], ex["res"].rsquared_adj,
                    ex["res"].aic, ex["res"].bic, np.nan, r["phi"], ex["res"].pvalues[0], ROT)
        agg_y = S["y"].mean(0)
        agg_X = S["X"].mean(0)
        T_["bp"].append(dict(spec=sp, periodo=S["per"]) | {k_: str(v_) for k_, v_ in bai_perron(agg_y, agg_X, S["qs"]).items()})
    # ------------- Holm, triangulacion
    lp = pd.DataFrame(lp_all)
    lp["p_holm"] = np.nan
    for m in ("alquiler", "compra"):
        for est in ("MG_dm", "PMG_dm", "CS-DL", "DFE"):
            msk = (lp.mercado == m) & (lp.estimador == est) & lp.hipotesis.ne("") & (lp.rezago.str.startswith("SBC") | (lp.rezago == "pT=4"))
            if msk.sum():
                lp.loc[msk, "p_holm"] = multipletests(lp.loc[msk, "p_H1"].to_numpy(), method="holm")[1]
    hip = []
    for h, (m, sp, v, sg) in HIPO.items():
        g = lp[(lp.hipotesis == h) & (lp.rezago.str.startswith("SBC") | (lp.rezago == "pT=4"))].set_index("estimador")
        mgr, pmr, csr = g.loc["MG_dm"], g.loc["PMG_dm"], g.loc["CS-DL"]
        sig = mgr.p_holm < .05
        same = np.sign(mgr.coef) == np.sign(pmr.coef) == np.sign(csr.coef)
        ver = ("CONFIRMADA (asociacion C4)" if sig and same else ("NO CONCLUYENTE (signos discrepantes)" if sig else "NO CONFIRMADA (p de Holm de MG_dm >= 0,05)"))
        vals = [mgr.coef, pmr.coef, csr.coef]
        hip.append(dict(id=h, mercado=m, familia=FAM[m], spec=sp, variable=v, signo_H1=sg, MG_dm=mgr.coef, PMG_dm=pmr.coef, CS_DL=csr.coef, rango_min=min(vals), rango_max=max(vals),
                        p_H1_MG=mgr.p_H1, p_holm_MG=mgr.p_holm, p_holm_PMG=pmr.p_holm, p_holm_CSDL=csr.p_holm, signos_coinciden=bool(same), veredicto=ver, periodo=mgr.periodo,
                        nota=f"{ROT}; rango entre los tres estimadores; no causal"))
    hip = pd.DataFrame(hip)
    e2 = pd.DataFrame(e2_rows)
    # F-E: Holm sobre p de cointegracion (spec A) por mercado
    fe = []
    for m in ("alquiler", "compra"):
        cc = pd.DataFrame(region_tables[m]["coint"])
        pa = cc[(cc.spec == "A") & (cc.nivel == "panel")].copy()
        pa["p_holm"] = multipletests(pa.p.to_numpy(), method="holm")[1]
        pa["mercado"] = m
        fe.append(pa)
    fe = pd.concat(fe)
    # ------------- magnitudes
    mag = []
    for _, r in lp[lp.rezago.str.startswith("SBC") | (lp.rezago == "pT=4")].iterrows():
        pct = r.coef * 100.0
        niv = np.mean([alq[c] for c in alq if c in set(d.codigo_ine_ccaa)]) if r.mercado == "alquiler" else np.mean([cmp_[c] for c in cmp_])
        mag.append(dict(mercado=r.mercado, spec=r.spec, estimador=r.estimador, variable=r.variable, pct_y_por_unidad=pct, unidad="por +1 % de x" if r.variable != "tasa_paro_epa" else "por +1 pp de paro",
                        nivel_medio_regional=niv, eur_por_unidad=niv * pct / 100.0,
                        unidad_eur="EUR/mes (SERPAVI VC mediana 2024)" if r.mercado == "alquiler" else "EUR/m2 (valor tasado medio 2025; supuesto: % del IPV aplicado al valor tasado)"))
    mag = pd.DataFrame(mag)
    lp = lp.merge(mag[["mercado", "spec", "estimador", "variable", "pct_y_por_unidad", "eur_por_unidad"]], how="left", on=["mercado", "spec", "estimador", "variable"])
    # ------------- escritura por mercado
    summaries = {}
    for m in ("alquiler", "compra"):
        D = OUT / m
        Tm = region_tables[m]
        ur_m = ur[ur.variable.isin(["ln_ipc_alquiler" if m == "alquiler" else "ln_ipv"] + [v for k_, z in SPECS.items() if k_[0] == m for v in z[1]])]
        ur_m.to_csv(D / "integracion.csv", index=False)
        pd.DataFrame(Tm["ur"]).to_csv(D / "integracion_panel_CIPS.csv", index=False)
        pd.DataFrame(Tm["coint"]).to_csv(D / "cointegracion.csv", index=False)
        lp[lp.mercado == m].to_csv(D / "largo_plazo.csv", index=False)
        hip[hip.mercado == m].to_csv(D / "hipotesis.csv", index=False)
        e2[e2.mercado == m].to_csv(D / "hipotesis_E.csv", index=False)
        mag[mag.mercado == m].to_csv(D / "magnitudes.csv", index=False)
        pd.DataFrame(Tm["dfe"]).to_csv(D / "dfe_inferencia.csv", index=False)
        pd.DataFrame(Tm["bp"]).to_csv(D / "bai_perron.csv", index=False)
        cor = pd.DataFrame(Tm["corto"])
        ph = pd.DataFrame(Tm["reg_phi"])
        # F-H: BH por (mercado, spec)
        cor["q_bh"] = np.nan
        for sp in cor.spec.unique():
            mk = cor.spec == sp
            cor.loc[mk, "q_bh"] = multipletests(cor.loc[mk, "p"].to_numpy(), method="fdr_bh")[1]
        cor["rechaza_bh10"] = cor.q_bh < .10
        cor["familia"] = "F-H (exploratoria, BH q=0,10); t convencional: aproximado para phi (distribucion no estandar)"
        cor.to_csv(D / "corto_plazo_region.csv", index=False)
        ph.to_csv(D / "velocidad_ajuste_region.csv", index=False)
        pd.DataFrame(Tm["diag"]).to_csv(D / "diagnosticos_region.csv", index=False)
        # colinealidad
        colrows = []
        for sp, S in Tm["col"]:
            names = S["xv"]
            Xd = pt.cs_demean(S["y"], S["X"])[1]
            pool = Xd.reshape(-1, Xd.shape[2])
            C = np.corrcoef(pool.T)
            for a in range(len(names)):
                for b_ in range(a + 1, len(names)):
                    colrows.append(dict(mercado=m, spec=sp, v1=names[a], v2=names[b_], corr_demeaned=C[a, b_]))
            Ci = np.linalg.inv(C) if len(names) > 1 else np.eye(1)
            for a, nm in enumerate(names):
                colrows.append(dict(mercado=m, spec=sp, v1=nm, v2="VIF_poblacional_demeaned", corr_demeaned=Ci[a, a]))
        pd.DataFrame(colrows).to_csv(D / "colinealidad.csv", index=False)
        write_eq(D / "ecuaciones.md", m, Tm["eq"], est_main, hip, ph)
        summaries[m] = (cor, ph, pd.DataFrame(Tm["diag"]))
    # colinealidad pob/extranjeros/ocupados (niveles, panel entero, demeaning)
    qs = [q for q in sorted(d.trimestre.unique()) if d[d.trimestre == q][["ln_ocupados", "ln_pob_total", "ln_pob_extranj"]].notna().all().all()]
    Z3 = np.stack([wide(d, v, qs) for v in ("ln_ocupados", "ln_pob_total", "ln_pob_extranj")], 2)
    Zd = Z3 - Z3.mean(0, keepdims=True)
    C3 = np.corrcoef(Zd.reshape(-1, 3).T)
    pd.DataFrame(C3, index=["ln_ocupados", "ln_pob_total", "ln_pob_extranj"], columns=["ln_ocupados", "ln_pob_total", "ln_pob_extranj"]).assign(
        VIF=np.diag(np.linalg.inv(C3))).to_csv(OUT / "colinealidad_ocup_pob_extranj.csv")
    hip.to_csv(OUT / "hipotesis_confirmatorias.csv", index=False)
    fe.to_csv(OUT / "familia_FE_cointegracion.csv", index=False)
    write_resumen(summaries, hip, e2, fe, lp, ur, est_main)
    write_json(hip, e2, lp, ur, summaries, est_main, fe)
    reg.flush()


# ------------------------------------------------------------------ salidas
def write_eq(path, m, eqs, est_main, hip, ph):
    L = [f"# Ecuaciones, mercado {m} ({ROT}; asociacion de largo plazo, no causal)\n"]
    for sp in ("A", "B"):
        E, cs, S, (p, q) = est_main[(m, sp)]
        th = E["MG_dm"]["theta"]
        yv, xv = S["yv"], S["xv"]
        tex = lambda s: s.replace("_", r"\_")  # noqa: E731
        lhs = " + ".join(f"{th[j]:+.3f}\\,\\text{{{tex(v)}}}_{{it}}" for j, v in enumerate(xv))
        L += [f"## Especificacion {sp}: largo plazo comun (MG con demeaning transversal, ARDL({p},{q}), {S['per']})\n",
              f"$$\\text{{{tex(yv)}}}_{{it}} - \\bar{{\\text{{{tex(yv)}}}}}_t = \\alpha_i + {lhs} + u_{{it}}$$",
              "(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)\n",
              f"### ECM por region, spec {sp}\n",
              f"$$\\Delta \\text{{{tex(yv)}}}_{{it}} = c_i + \\varphi_i\\Big(\\text{{{tex(yv)}}}_{{i,t-1}} - \\sum_k \\theta_{{ik}}\\,x_{{k,i,t-1}}\\Big) + \\sum_{{j=0}}^{{{q - 1}}}\\gamma_{{ij}}'\\,\\Delta x_{{i,t-j}} + \\sum_{{j=1}}^{{{p - 1}}}\\lambda_{{ij}}\\Delta y_{{i,t-j}} + \\delta_i\\,\\Delta \\text{{{tex(S['cv'])}}}_{{it}} + \\varepsilon_{{it}}$$\n"]
        for s_, i, ex, S_, pp, qq in eqs:
            if s_ != sp:
                continue
            nm, b, se = ex["names"], ex["b"], ex["se"]
            th_i = ex["theta"]
            lr = " + ".join(f"{th_i[j]:.3f}\\,\\text{{{tex(v)}}}_{{t-1}}" for j, v in enumerate(xv))
            sr = " ".join(f"{b[j]:+.3f}\\,\\text{{{tex(n_)}}}" for j, n_ in enumerate(nm) if n_.startswith("d_"))
            L.append(f"- Region {S['codes'][i]}: $\\Delta y_t = {b[nm.index('const')]:+.3f} {b[0]:+.3f}\\,(y_{{t-1}} - [{lr}]) {sr}$ (EE de $\\varphi$: {se[0]:.3f})")
        L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def fmt(x, n=3):
    return "NA" if pd.isna(x) else f"{x:.{n}f}"


def write_resumen(summ, hip, e2, fe, lp, ur, est_main):
    for m in ("alquiler", "compra"):
        cor, ph, dg = summ[m]
        L = [f"# Resumen R4a, {m} ({ROT}; capa C4; asociacion de largo plazo, sin lenguaje causal)\n",
             "## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)\n",
             "| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |", "|---|---|---|---|---|---|---|---|"]
        for _, r in hip[hip.mercado == m].iterrows():
            L.append(f"| {r['id']} | {r.variable} (spec {r.spec}) | {fmt(r.MG_dm)} | {fmt(r.PMG_dm)} | {fmt(r.CS_DL)} | [{fmt(r.rango_min)}, {fmt(r.rango_max)}] | {fmt(r.p_holm_MG, 4)} | {r.veredicto} |")
        L += ["", "## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman\n", "| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |", "|---|---|---|---|---|---|---|---|"]
        for _, r in e2[e2.mercado == m].iterrows():
            L.append(f"| {r.spec} | {fmt(r.phi_MG)} | {fmt(r.t_MG, 2)} | {r.rechaza} | {fmt(r.hausman_p)} | {fmt(r.pedroni_panel_p)} | {fmt(r.pedroni_group_p)} | {fmt(r.wl_Gt_p)} |")
        for sp in ("A", "B"):
            x = ph[ph.spec == sp]
            L.append(f"\nHeterogeneidad de phi_i, spec {sp}: media {fmt(x.phi.mean())}, mediana {fmt(x.phi.median())}, DE {fmt(x.phi.std())}, min {fmt(x.phi.min())}, max {fmt(x.phi.max())}; "
                     f"phi_i<0 en {int((x.phi < 0).sum())}/{len(x)}; semivida mediana {fmt(x.semivida_trim.median(), 1)} trimestres; BH q<0,10 en phi_i: "
                     f"{int(cor[(cor.spec == sp) & (cor.coef == 'phi')].rechaza_bh10.sum())}/{len(x)} (t convencional, aproximado).")
            dd = dg[dg.spec == sp]
            L.append(f"Diagnosticos spec {sp}: BG p<0,05 en {int((dd.BG_p < .05).sum())}, BP en {int((dd.BP_p < .05).sum())}, JB en {int((dd.JB_p < .05).sum())}, RESET en {int((dd.RESET_p < .05).sum())}, "
                     f"CUSUM rechaza en {int(dd.CUSUM_rechaza5.sum())} de {len(dd)}; cambio de signo de phi entre mitades en {int(dd.cambio_signo_phi.sum())}.")
        vs = ["ln_ipc_alquiler" if m == "alquiler" else "ln_ipv"] + sorted({v for k_, z in SPECS.items() if k_[0] == m for v in z[1]})
        L += ["", "## Orden de integracion por CCAA (ADF c + KPSS c; I(1) si ADF no rechaza en nivel, KPSS rechaza y ADF rechaza en diferencias)\n"]
        for v in vs:
            c_ = ur[ur.variable == v].clasif.value_counts().to_dict()
            L.append(f"- {v}: {c_} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)")
        L += ["", "Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.",
              "Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %)."]
        (OUT / m / "resumen.md").write_text("\n".join(L), encoding="utf-8")


def write_json(hip, e2, lp, ur, summ, est_main, fe):
    facts = []
    for _, r in hip.iterrows():
        pr = "valor tasado (magnitud) / IPV INE CCAA (dependiente)" if r.mercado == "compra" else "IPC alquiler INE (stock)"
        facts.append(dict(id=f"V7-R4-{r['id']}", indicador=f"Coef. largo plazo {r.variable} ({r.mercado}, spec {r.spec}), MG_dm; veredicto: {r.veredicto}", valor=r.MG_dm, min=r.rango_min, max=r.rango_max,
                          unidad="d ln y por d ln x" if r.variable != "tasa_paro_epa" else "d ln y por pp de paro", periodo=r.periodo, cobertura="17 CCAA", fuentes="INE (IPV, IPC, EPA, padron, hipotecas); panel_ccaa_q_v7",
                          capa="C4", fecha_dato=FECHA, medida_precio=pr if r.mercado == "compra" else "no aplica (alquiler: IPC alquiler, stock)", sentido_min_max="rango entre MG_dm, PMG_dm y CS-DL"))
    for _, r in e2.iterrows():
        facts.append(dict(id=f"V7-R4-PHI-{r.mercado.upper()}-{r.spec}", indicador=f"Velocidad de ajuste media phi (MG_dm), {r.mercado} spec {r.spec}", valor=r.phi_MG, min=r.phi_MG - 1.96 * r.ee,
                          max=r.phi_MG + 1.96 * r.ee, unidad="por trimestre", periodo=est_main[(r.mercado, r.spec)][2]["per"], cobertura="17 CCAA", fuentes="INE; panel_ccaa_q_v7", capa="C4", fecha_dato=FECHA,
                          medida_precio="IPV INE CCAA" if r.mercado == "compra" else "no aplica (IPC alquiler)", sentido_min_max="IC95 normal"))
    (OUT / "hechos.json").write_text(json.dumps(facts, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    conf = hip[hip.veredicto.str.startswith("CONFIRMADA")]["id"].tolist()
    res = dict(rama="V7-R4a", pregunta="Asociacion de largo plazo entre precios (alquiler IPC; compra IPV) y ocupacion, poblacion, paro e hipotecas en 17 CCAA", capa="C4",
               datos="data/processed/v7/panel_ccaa_q_v7.csv (2007T1-2026T2; spec A con poblacion hasta 2025T1)", N=17,
               metodo="ECM de panel: MG con demeaning transversal (principal), PMG_dm (bootstrap B=199), CS-DL (pT=4), DFE; Holm por familia; triangulacion V12",
               estimacion={r["id"]: dict(MG_dm=r.MG_dm, PMG_dm=r.PMG_dm, CS_DL=r.CS_DL, veredicto=r.veredicto) for _, r in hip.iterrows()},
               ic95={r["id"]: [float(lp[(lp.hipotesis == r["id"]) & (lp.estimador == "MG_dm") & lp.rezago.str.startswith("SBC")].ic95_lo.iloc[0]),
                              float(lp[(lp.hipotesis == r["id"]) & (lp.estimador == "MG_dm") & lp.rezago.str.startswith("SBC")].ic95_hi.iloc[0])] for _, r in hip.iterrows()},
               p_ajustado={r["id"]: r.p_holm_MG for _, r in hip.iterrows()}, nivel_evidencia="EXPLORATORIO (C4): asociacion de largo plazo; confirmadas bajo regla de triangulacion: " + (", ".join(conf) or "ninguna"),
               diagnosticos="ver diagnosticos_region.csv, cointegracion.csv, integracion.csv, bai_perron.csv, hipotesis_E.csv",
               fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None), medida_precio="compra: IPV INE (CCAA) como dependiente; magnitudes en EUR/m2 con valor tasado; alquiler: IPC alquiler (stock), EUR/mes SERPAVI",
               notas=f"{ROT}. Sin evaluacion fuera de muestra en R4a (corresponde a R5). Dummies de quiebre aplicadas como pulsos en diferencias (ver desviaciones). Controles de corto plazo solo en ECM por region.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
