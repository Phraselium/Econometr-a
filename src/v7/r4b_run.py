"""V7-R4b: modelo jerarquico (F-H), proyecciones locales (F-L), regulacion (F-R) y provincia anual (F-P).

Capa C4. Informativo, muestra ya vista en v1. Determinista, sin red, SEED=20261010. Sin lectura de data/sealed.
Asociaciones, nunca efectos causales. Uso: python3 src/v7/r4b_run.py [--smoke] [--only h,l,r,p]
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v7"))
from econ_utils import Registry  # noqa: E402
from panel_tools import _ols, _within, wild_cluster_boot  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = ROOT / "output" / "v7" / "R4b"
SMOKE = "--smoke" in sys.argv
ONLY = (sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else ["h", "l", "r", "p"])
if SMOKE:
    OUT = ROOT / "output" / "v7" / "R4b_smoke"
(OUT / "figuras").mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")
ROT = "informativo, muestra ya vista en v1"
FECHA = "2026-10-10"
HECHOS: list = []
RES: dict = {}


def bh(p):
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = ~np.isnan(p)
    pv = p[ok]
    o = np.argsort(pv)
    m = len(pv)
    q = pv[o] * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    r = np.empty(m)
    r[o] = np.minimum(q, 1)
    out[ok] = r
    return out


def load_ccaa():
    d = pd.read_csv(ROOT / "data/processed/v7/panel_ccaa_q_v7.csv", dtype={"codigo_ine_ccaa": str})
    return d.sort_values(["codigo_ine_ccaa", "trimestre"]).reset_index(drop=True)


# ------------------------------------------------------------------ 1. jerarquico
def arr(d, col):
    return d.pivot(index="codigo_ine_ccaa", columns="trimestre", values=col).values


def hier_design(d, mercado, spec):
    """Devuelve dict de arrays apilados para el ECM de un mercado/especificacion, muestra comun completa."""
    ycol = "ln_ipc_alquiler" if mercado == "alquiler" else "ln_ipv"
    if mercado == "alquiler":
        xs = ["ln_ocupados", "ln_pob_total"] if spec == "A" else ["tasa_paro_epa"]
        sr = "d_ln_hip_importe"
    else:
        xs = ["ln_ocupados", "ln_hip_importe", "ln_pob_total"] if spec == "A" else ["tasa_paro_epa", "ln_hip_importe"]
        sr = "d_ln_compraventas"
    return ycol, xs, sr


def common_sample(d):
    cols = ["ln_ipc_alquiler", "ln_ipv", "ln_ocupados", "ln_pob_total", "tasa_paro_epa", "ln_hip_importe",
            "d_ln_hip_importe", "d_ln_compraventas"]
    ok = d.groupby("trimestre")[cols].apply(lambda g: g.notna().all().all() and len(g) == 17)
    ok = ok[ok].index
    t = sorted(ok)
    t = t[1:]  # primera obs sin retardo de diferencias
    return d[d.trimestre.isin(t)].copy(), t


def build_ecm(d, ycol, xs, sr):
    """Arrays del ECM: dy, ylag, Xlag (demeaning transversal y por CCAA), dX corto plazo, dylag, dummies."""
    ids = sorted(d.codigo_ine_ccaa.unique())
    Y = arr(d, ycol)
    X = np.stack([arr(d, c) for c in xs], -1)
    S = arr(d, sr)
    N, T = Y.shape
    # demeaning transversal (V10) y por unidad sobre todo el periodo
    Yd = Y - Y.mean(0)
    Xd = X - X.mean(0)
    Yd = Yd - Yd.mean(1, keepdims=True)
    Xd = Xd - Xd.mean(1, keepdims=True)
    dy = Y[:, 1:] - Y[:, :-1]
    ts = np.arange(2, T)
    rows = dict(dy=dy[:, ts - 1], ylag=Yd[:, ts - 1], Xlag=Xd[:, ts - 1, :], dX=S[:, ts], dylag=dy[:, ts - 2])
    tr = np.array(sorted(d.trimestre.unique()))[ts]
    rows["covid"] = np.tile(np.isin(tr, ["2020Q2", "2020Q3", "2020Q4"]).astype(float), (N, 1))
    rows["epa21"] = np.tile((tr == "2021Q1").astype(float), (N, 1))
    g = np.repeat(np.arange(N), len(ts))
    flat = {k: (v.reshape(N * len(ts), -1) if v.ndim == 3 else v.reshape(-1)) for k, v in rows.items()}
    flat["g"] = g
    flat["ids"] = ids
    flat["tr"] = tr
    return flat


def ols_individual(F):
    N = len(F["ids"])
    out = []
    for i in range(N):
        m = F["g"] == i
        Z = np.column_stack([np.ones(m.sum()), F["ylag"][m], F["Xlag"][m], F["dX"][m], F["dylag"][m],
                             F["covid"][m], F["epa21"][m]])
        b, e, ZtZi = _ols(F["dy"][m], Z)
        k = Z.shape[1]
        s2 = e @ e / (m.sum() - k)
        se = np.sqrt(np.diag(ZtZi) * s2)
        ix = 2 + F["Xlag"].shape[1]
        out.append(dict(phi=b[1], phi_se=se[1], delta=b[ix], delta_se=se[ix]))
    return pd.DataFrame(out)


def fit_pymc(F, tag):
    import arviz as az
    import pymc as pm
    N = len(F["ids"])
    k = F["Xlag"].shape[1]
    sdx = F["Xlag"].std(0)
    th0 = np.linalg.lstsq(F["Xlag"] / sdx, F["ylag"], rcond=None)[0]
    Xs = F["Xlag"] / sdx
    draws, tune = (100, 100) if SMOKE else (700, 1000)
    with pm.Model():
        phib = pm.Normal("phi_bar", -0.05, 0.05)
        sphi = pm.HalfNormal("sd_phi", 0.1)
        zp = pm.Normal("z_phi", 0, 1, shape=N)
        phi = pm.Deterministic("phi_i", phib + sphi * zp)
        db = pm.Normal("delta_bar", 0, 0.3)
        sd_ = pm.HalfNormal("sd_delta", 0.2)
        zd = pm.Normal("z_delta", 0, 1, shape=N)
        dl = pm.Deterministic("delta_i", db + sd_ * zd)
        ab = pm.Normal("alpha_bar", 0, 0.01)
        sa = pm.HalfNormal("sd_alpha", 0.01)
        za = pm.Normal("z_alpha", 0, 1, shape=N)
        al = ab + sa * za
        theta_s = pm.Normal("theta_s", 0, 0.15, shape=k)
        theta = pm.Deterministic("theta", theta_s / sdx)
        lam = pm.Normal("lam", 0, 0.5)
        c1 = pm.Normal("c_covid", 0, 0.05)
        c2 = pm.Normal("c_epa21", 0, 0.05)
        sig = pm.HalfNormal("sigma_i", 0.02, shape=N)
        g = F["g"]
        ect = F["ylag"] - pm.math.dot(Xs, theta_s)
        mu = al[g] + phi[g] * ect + dl[g] * F["dX"] + lam * F["dylag"] + c1 * F["covid"] + c2 * F["epa21"]
        pm.Normal("obs", mu, sig[g], observed=F["dy"])
        idata = pm.sample(draws=draws, tune=tune, chains=4, cores=1, random_seed=SEED, target_accept=0.95,
                          progressbar=False, initvals={"theta_s": th0})
    import time
    print("pymc", tag, time.strftime("%X"), flush=True)
    vars_ = ["phi_bar", "sd_phi", "delta_bar", "sd_delta", "theta", "lam", "sd_alpha"]
    summ = az.summary(idata, var_names=vars_, ci_prob=0.95)
    summ_i = az.summary(idata, var_names=["phi_i", "delta_i"], ci_prob=0.95)
    for s_ in (summ, summ_i):
        s_.rename(columns={"eti95_lb": "hdi_2.5%", "eti95_ub": "hdi_97.5%"}, inplace=True)
    div = int(idata.sample_stats["diverging"].sum())
    return summ, summ_i, div


def mixedlm(F):
    import statsmodels.formula.api as smf
    k = F["Xlag"].shape[1]
    df = pd.DataFrame({"dy": F["dy"], "ylag": F["ylag"], "dX": F["dX"], "dylag": F["dylag"], "covid": F["covid"],
                       "epa21": F["epa21"], "g": F["g"]})
    for j in range(k):
        df[f"x{j}"] = F["Xlag"][:, j]
    f = "dy ~ ylag + dX + dylag + covid + epa21 + " + " + ".join(f"x{j}" for j in range(k))
    try:
        m = smf.mixedlm(f, df, groups=df["g"], re_formula="~ ylag + dX").fit(method="lbfgs", reml=True)
        re = pd.DataFrame(m.random_effects).T
        phi_i = m.fe_params["ylag"] + re["ylag"].values
        dl_i = m.fe_params["dX"] + re["dX"].values
        return dict(phi_bar=m.fe_params["ylag"], phi_se=m.bse_fe["ylag"], delta_bar=m.fe_params["dX"],
                    delta_se=m.bse_fe["dX"], sd_phi=float(np.sqrt(m.cov_re.loc["ylag", "ylag"])),
                    sd_delta=float(np.sqrt(m.cov_re.loc["dX", "dX"])), conv=bool(m.converged),
                    phi_i=phi_i, delta_i=dl_i, n=int(m.nobs), ll=float(m.llf))
    except Exception as ex:  # pragma: no cover
        return dict(error=str(ex)[:120])


def run_h():
    d, tgrid = common_sample(load_ccaa())
    ini, fin = tgrid[0], tgrid[-1]
    ccaa_names = d.drop_duplicates("codigo_ine_ccaa").set_index("codigo_ine_ccaa").ccaa.to_dict()
    for mercado in ["alquiler", "compra"]:
        frames = []
        for spec in ["A", "B"]:
            ycol, xs, sr = hier_design(d, mercado, spec)
            F = build_ecm(d, ycol, xs, sr)
            ind = ols_individual(F)
            summ, summ_i, div = fit_pymc(F, f"{mercado}_{spec}")
            ml = mixedlm(F)
            N = len(F["ids"])
            pb = summ.loc["phi_bar", "mean"]
            db = summ.loc["delta_bar", "mean"]
            fm = f"d {ycol} = a_i + phi_i*(y - theta'x)_(t-1) + d_i*d{sr} + lam*dy_(t-1) + dummies; x={xs}"
            n = len(F["dy"])
            phis = summ_i.loc[[f"phi_i[{i}]" for i in range(N)]]
            dels = summ_i.loc[[f"delta_i[{i}]" for i in range(N)]]
            rhat = float(max(summ["r_hat"].max(), summ_i["r_hat"].max()))
            ess = float(min(summ["ess_bulk"].min(), summ_i["ess_bulk"].min()))
            for i in range(N):
                shr_p = (ind.phi[i] - phis["mean"].iloc[i]) / (ind.phi[i] - pb) if abs(ind.phi[i] - pb) > 1e-9 else np.nan
                shr_d = (ind.delta[i] - dels["mean"].iloc[i]) / (ind.delta[i] - db) if abs(ind.delta[i] - db) > 1e-9 else np.nan
                frames.append(dict(mercado=mercado, spec=spec, codigo_ine_ccaa=F["ids"][i], ccaa=ccaa_names[F["ids"][i]],
                                   phi_ols=ind.phi[i], phi_ols_se=ind.phi_se[i], phi_jerarquico=phis["mean"].iloc[i],
                                   phi_ic95_lo=phis["hdi_2.5%"].iloc[i], phi_ic95_hi=phis["hdi_97.5%"].iloc[i],
                                   phi_encogimiento=shr_p, phi_mixedlm=(ml["phi_i"][i] if "phi_i" in ml else np.nan),
                                   delta_ols=ind.delta[i], delta_jerarquico=dels["mean"].iloc[i],
                                   delta_ic95_lo=dels["hdi_2.5%"].iloc[i], delta_ic95_hi=dels["hdi_97.5%"].iloc[i],
                                   delta_encogimiento=shr_d, delta_mixedlm=(ml["delta_i"][i] if "delta_i" in ml else np.nan),
                                   rotulo=ROT))
            REG.log("F-H", f"H_{mercado}_{spec}_pymc", fm, ini, fin, n, np.nan, np.nan, np.nan, np.nan, pb, np.nan,
                    f"phi_bar IC95 [{summ.loc['phi_bar','hdi_2.5%']:.3f},{summ.loc['phi_bar','hdi_97.5%']:.3f}]; "
                    f"sd_phi={summ.loc['sd_phi','mean']:.3f}; rhat_max={rhat:.3f}; ess_min={ess:.0f}; div={div}; NUTS 4 cad; {ROT}")
            if "error" not in ml:
                REG.log("F-H", f"H_{mercado}_{spec}_mixedlm", fm, ini, fin, ml["n"], np.nan, np.nan, np.nan, np.nan,
                        ml["phi_bar"], 2 * stats.norm.sf(abs(ml["phi_bar"] / ml["phi_se"])),
                        f"MixedLM REML; sd_phi={ml['sd_phi']:.3f}; converge={ml['conv']}; forma ECM sin restringir")
            shrk = np.nanmean(np.abs([f["phi_encogimiento"] for f in frames[-N:]]))
            RES[f"H_{mercado}_{spec}"] = dict(
                phi_bar=float(pb), phi_ic=[float(summ.loc["phi_bar", "hdi_2.5%"]), float(summ.loc["phi_bar", "hdi_97.5%"])],
                sd_phi=float(summ.loc["sd_phi", "mean"]), delta_bar=float(db), sd_delta=float(summ.loc["sd_delta", "mean"]),
                theta=[float(x) for x in summ.filter(like="theta", axis=0)["mean"]], xs=xs, rhat_max=rhat, ess_min=ess,
                divergencias=div, mixedlm_phi_bar=ml.get("phi_bar"), mixedlm_sd_phi=ml.get("sd_phi"),
                mixedlm_conv=ml.get("conv"), encogimiento_phi_medio=float(shrk), n=n, ols_phi_media=float(ind.phi.mean()),
                ols_phi_sd=float(ind.phi.std()), muestra=[ini, fin])
            HECHOS.append(dict(id=f"V7-R4b-H-{mercado}-{spec}-phibar", indicador=f"Velocidad de ajuste media del ECM jerarquico, {mercado}, spec {spec}",
                               valor=float(pb), min=float(summ.loc["phi_bar", "hdi_2.5%"]), max=float(summ.loc["phi_bar", "hdi_97.5%"]),
                               unidad="coef. trimestral", periodo=f"{ini}-{fin}", cobertura="17 CCAA", fuentes=["INE IPC/IPV, EPA, Hipotecas"],
                               capa="C4", fecha_dato=FECHA))
        pd.DataFrame(frames).to_csv(OUT / f"jerarquico_{mercado}.csv", index=False)


# ------------------------------------------------------------------ 2. proyecciones locales
def twoway(a):
    return a - a.mean(1, keepdims=True) - a.mean(0, keepdims=True) + a.mean()


def dk_balanced(y, X, N, T, maxlag):
    from panel_tools import driscoll_kraay
    r = driscoll_kraay(y, X, N, T, maxlag=maxlag)
    return r["coef"], r["se"]


def ar_resid(s, p=2):
    s = np.asarray(s, float)
    Z = np.column_stack([np.ones(len(s) - p)] + [s[p - j - 1:len(s) - j - 1] for j in range(p)])
    b, e, _ = _ols(s[p:], Z)
    out = np.full(len(s), np.nan)
    out[p:] = e
    return out / np.nanstd(e)


def run_l():
    d = load_ccaa()
    nat = d.groupby("trimestre").agg(tipo=("nac_tipo_hip", "first"), cred=("nac_credito_nuevo", "first")).sort_index()
    sh = {"tipo_hip": ar_resid(np.diff(nat.tipo.values, prepend=np.nan)[1:]),
          "credito_nuevo": ar_resid(np.diff(np.log(nat.cred.values)))}
    # alinear: indice 0 corresponde a trimestre 1 (diferencias); desplazar
    sh = {k: np.concatenate([[np.nan], v]) for k, v in sh.items()}
    z = d.groupby("codigo_ine_ccaa").exp_hip_importe_pib_1519.first()
    z = ((z - z.mean()) / z.std()).values
    ids = sorted(d.codigo_ine_ccaa.unique())
    H = range(0, 9)
    for mercado, ycol in [("alquiler", "ln_ipc_alquiler"), ("compra", "ln_ipv")]:
        Y = arr(d, ycol)
        N, T = Y.shape
        rows = []
        for sname, s in sh.items():
            t0 = 5  # necesito shock_{t-2} valido (s[0] nan, s[1..]), dy_{t-2}
            for h in H:
                ts = np.arange(t0, T - h)
                dep = Y[:, ts + h] - Y[:, ts - 1]
                cols = [z[:, None] * s[ts - j][None, :] for j in range(3)]
                cols += [Y[:, ts - 1 - j] - Y[:, ts - 2 - j] for j in range(2)]
                Dp = twoway(dep)
                Xs = np.stack([twoway(c) for c in cols], -1)
                Th = len(ts)
                yv, Xv = Dp.reshape(-1), Xs.reshape(-1, Xs.shape[-1])
                cl = np.repeat(np.arange(N), Th)
                b, se = dk_balanced(yv, Xv, N, Th, maxlag=max(4, h + 1))
                wb = wild_cluster_boot(yv, Xv, cl, j=0, B=199 if SMOKE else 999, seed=SEED)
                p_dk = 2 * stats.norm.sf(abs(b[0] / se[0]))
                rows.append(dict(mercado=mercado, shock=sname, h=h, coef=b[0], se_dk=se[0], ic95_lo=b[0] - 1.96 * se[0],
                                 ic95_hi=b[0] + 1.96 * se[0], p_dk=p_dk, p_wild_webb=wb["p_boot"], n=len(yv),
                                 muestra=f"{nat.index[ts[0]]}-{nat.index[ts[-1]]}+h", rotulo=ROT))
        df = pd.DataFrame(rows)
        df["q_bh_wild"] = np.nan
        for sname in sh:
            m = df.shock == sname
            df.loc[m, "q_bh_wild"] = bh(df.loc[m, "p_wild_webb"].values)
            df.loc[m, "q_bh_dk"] = bh(df.loc[m, "p_dk"].values)
        # familia estricta: horizontes x mercado para cada shock (9 contrastes por mercado/shock)
        df.to_csv(OUT / f"lp_{mercado}.csv", index=False)
        for _, r in df.iterrows():
            REG.log("F-L", f"LP_{mercado}_{r.shock}_h{r.h}", f"y_(t+h)-y_(t-1) ~ z_i*shock_t(+2 rezagos) + 2 dy + FE CCAA + FE t (h={r.h})",
                    "", "", r.n, np.nan, np.nan, np.nan, np.nan, r.coef, r.p_wild_webb,
                    f"se_dk={r.se_dk:.4g}; p_dk={r.p_dk:.3f}; q_bh_wild={r.q_bh_wild:.3f}; {ROT}")
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
        for a, sname in zip(ax, sh):
            g = df[df.shock == sname]
            a.plot(g.h, g.coef * 100, "k-o", ms=3)
            a.fill_between(g.h, g.ic95_lo * 100, g.ic95_hi * 100, color="grey", alpha=.3)
            a.axhline(0, color="r", lw=.7)
            a.set_title(f"{mercado}: {sname} x exposicion (IRF diferencial)")
            a.set_xlabel("horizonte (trimestres)")
            a.set_ylabel("puntos % acumulados por 1 DT de exposicion")
        fig.suptitle(f"IC95 Driscoll-Kraay; asociacion, {ROT}", fontsize=8)
        fig.tight_layout()
        fig.savefig(OUT / "figuras" / f"irf_diferencial_{mercado}.png", dpi=110)
        plt.close(fig)
        k = df[(df.shock == "tipo_hip")]
        RES[f"L_{mercado}"] = dict(coef_h0_8=[float(x) for x in k.coef], p_wild=[float(x) for x in k.p_wild_webb],
                                   q_bh=[float(x) for x in k.q_bh_wild], n_sig_bh10=int((k.q_bh_wild < .10).sum()),
                                   n_sig_bh10_credito=int((df[df.shock == "credito_nuevo"].q_bh_wild < .10).sum()))
        g = k.loc[k.coef.abs().idxmax()]
        HECHOS.append(dict(id=f"V7-R4b-L-{mercado}-tipo-pico", indicador=f"Mayor efecto diferencial |coef| de shock tipo hipotecario x exposicion, {mercado} (h={int(g.h)})",
                           valor=float(g.coef * 100), min=float(g.ic95_lo * 100), max=float(g.ic95_hi * 100), unidad="puntos % por DT de exposicion",
                           periodo="2008-2026", cobertura="17 CCAA", fuentes=["INE", "BdE/BCE"], capa="C4", fecha_dato=FECHA))


# ------------------------------------------------------------------ 3. regulacion
def run_r():
    d = load_ccaa()
    Y = arr(d, "ln_ipc_alquiler")
    N, T = Y.shape
    dy = Y[:, 1:] - Y[:, :-1]
    HIP = arr(d, "d_ln_hip_importe")[:, 1:]
    regs = ["zt_declarada", "zt_cuota_municipios", "tope_rentas_ccaa", "tope_rentas_ccaa_alt_v3", "tope_rentas_ccaa_frac"]
    rows = []
    for rg in regs:
        R = arr(d, rg)[:, 1:]
        for variante in ["contemporaneo", "con_adelanto4"]:
            ts = np.arange(5, dy.shape[1] - (4 if variante == "con_adelanto4" else 0))
            dep = dy[:, ts]
            cols = [R[:, ts], dy[:, ts - 1], HIP[:, ts]]
            if variante == "con_adelanto4":
                cols.append(R[:, ts + 4])
            Xs = np.stack([twoway(c) for c in cols], -1)
            if Xs[..., 0].std() < 1e-9:
                continue
            Th = len(ts)
            yv, Xv = twoway(dep).reshape(-1), Xs.reshape(-1, Xs.shape[-1])
            cl = np.repeat(np.arange(N), Th)
            b, se = dk_balanced(yv, Xv, N, Th, 4)
            ntrat = int((arr(d, rg).max(1) > 0).sum())
            for j, nm in [(0, rg)] + ([(3, rg + "_adelanto4_placebo")] if variante == "con_adelanto4" else []):
                wb = wild_cluster_boot(yv, Xv, cl, j=j, B=199 if SMOKE else 999, seed=SEED)
                rows.append(dict(regulador=rg, variante=variante, termino=nm, coef=b[j], se_dk=se[j],
                                 p_dk=2 * stats.norm.sf(abs(b[j] / se[j])), p_wild_webb=wb["p_boot"], ccaa_tratadas=ntrat,
                                 n=len(yv), nota="pocas CCAA tratadas: p wild poco fiable" if ntrat < 6 else "", rotulo=ROT))
    df = pd.DataFrame(rows)
    df["q_bh"] = bh(df.p_wild_webb.values)
    df.to_csv(OUT / "regulacion.csv", index=False)
    for _, r in df.iterrows():
        REG.log("F-R", f"R_{r.regulador}_{r.variante}_{r.termino}", "d ln IPC alquiler ~ regulador + dy_(t-1) + d ln hip + FE CCAA + FE t",
                "2008Q2", "2026Q2", r.n, np.nan, np.nan, np.nan, np.nan, r.coef, r.p_wild_webb,
                f"se_dk={r.se_dk:.4g}; q_bh={r.q_bh:.3f}; tratadas={r.ccaa_tratadas}; exploratorio")
    main = df[df.termino == df.regulador]
    RES["R"] = dict(n_tests=int(len(df)), n_sig_bh10=int((df.q_bh < .10).sum()),
                    coefs={f"{r.regulador}|{r.variante}": [float(r.coef), float(r.p_wild_webb), float(r.q_bh)] for _, r in main.iterrows()},
                    placebo_adelanto_sig=int(((df.termino.str.contains("placebo")) & (df.q_bh < .10)).sum()))


# ------------------------------------------------------------------ 4. provincia
def dk_unbal(yw, Xw, tt, m=2):
    b, e, XtXi = _ols(yw, Xw)
    u = np.unique(tt)
    h = np.array([(Xw[tt == t] * e[tt == t][:, None]).sum(0) for t in u])
    S = h.T @ h
    for lag in range(1, m + 1):
        G = h[lag:].T @ h[:-lag]
        S += (1 - lag / (m + 1)) * (G + G.T)
    V = XtXi @ S @ XtXi
    return b, np.sqrt(np.diag(V))


def run_p():
    p = pd.read_csv(ROOT / "data/processed/v7/panel_prov_a_v7.csv", dtype={"cod_prov": str})
    p = p.sort_values(["cod_prov", "anio"]).reset_index(drop=True)
    p["d_ln_ipc_alquiler"] = p.groupby("cod_prov").ipc_alquiler_indice.transform(lambda s: np.log(s).diff())
    core = ["d_ln_pob_total", "d_ln_ocupados_epa", "d_ln_hip_importe"]
    full = core + ["d_ln_compraventas", "d_ln_iniciadas"]
    deps = {"valor_tasado": "d_ln_valor_tasado", "ipc_alquiler": "d_ln_ipc_alquiler"}
    fe_rows, cce_rows, val_rows = [], [], []
    for dn, dc in deps.items():
        for sname, xs in [("core", core), ("full", full)]:
            s = p.dropna(subset=[dc] + xs).copy()
            k = len(xs)
            cnt = s.groupby("cod_prov").size()
            s = s[s.cod_prov.isin(cnt[cnt >= k + 4].index)]
            n = len(s)
            nprov = s.cod_prov.nunique()
            ini, fin = int(s.anio.min()), int(s.anio.max())
            tt = s.anio.values
            cl = pd.factorize(s.cod_prov)[0]
            # FE: provincia (within) + dummies de anio
            yd = pd.get_dummies(s.anio, drop_first=True).values.astype(float)
            Xf = np.column_stack([s[xs].values, yd])
            yw, Xw = _within(s[dc].values, cl), _within(Xf, cl)
            b, se = dk_unbal(yw, Xw, tt)
            for j, x in enumerate(xs):
                wb = wild_cluster_boot(s[dc].values, Xf, cl, j=j, B=199 if SMOKE else 499, seed=SEED)
                fe_rows.append(dict(dependiente=dn, spec=sname, regresor=x, coef=b[j], se_dk=se[j],
                                    p_dk=2 * stats.norm.sf(abs(b[j] / se[j])), p_wild_webb=wb["p_boot"], n=n, provincias=nprov,
                                    periodo=f"{ini}-{fin}"))
            if cnt.min() < 2 * k + 6:  # CCE inviable: obs por provincia < parametros (1+k+1+k) + margen
                continue
            # CCE: medias transversales de y y X (muestra completa del caso), cargas por provincia
            avg = s.groupby("anio")[[dc] + xs].transform("mean").values
            yres, Xres, bi, ids_ok = [], [], [], []
            for c in sorted(s.cod_prov.unique()):
                m = (s.cod_prov == c).values
                Zc = np.column_stack([np.ones(m.sum()), avg[m]])
                yi, Xi = s.loc[m, dc].values, s.loc[m, xs].values
                P = np.linalg.pinv(Zc)
                ry, rX = yi - Zc @ (P @ yi), Xi - Zc @ (P @ Xi)
                yres.append(ry)
                Xres.append(rX)
                Wi = np.column_stack([np.ones(m.sum()), Xi, avg[m]])
                if m.sum() >= Wi.shape[1] + 3:
                    bb, _, _ = _ols(yi, Wi)
                    bi.append(bb[1:1 + k])
                    ids_ok.append(c)
                    if c in ("03", "12", "46"):
                        val_rows.append(dict(cod_prov=c, dependiente=dn, spec=sname, **{x: bb[1 + j] for j, x in enumerate(xs)}, n_obs=int(m.sum())))
            yr, Xr = np.concatenate(yres), np.vstack(Xres)
            bc, sec = dk_unbal(yr, Xr, tt)
            bi = np.array(bi)
            mg = bi.mean(0)
            mg_se = bi.std(0, ddof=1) / np.sqrt(len(bi))
            for j, x in enumerate(xs):
                wb = wild_cluster_boot(yr, Xr, cl, j=j, B=199 if SMOKE else 499, seed=SEED)
                cce_rows.append(dict(dependiente=dn, spec=sname, regresor=x, estimador="CCEP", coef=bc[j], se_dk=sec[j],
                                     p_dk=2 * stats.norm.sf(abs(bc[j] / sec[j])), p_wild_webb=wb["p_boot"], n=n, provincias=nprov,
                                     periodo=f"{ini}-{fin}"))
                cce_rows.append(dict(dependiente=dn, spec=sname, regresor=x, estimador="CCE-MG", coef=mg[j], se_dk=mg_se[j],
                                     p_dk=2 * stats.norm.sf(abs(mg[j] / mg_se[j])), p_wild_webb=np.nan, n=n, provincias=len(bi),
                                     periodo=f"{ini}-{fin}"))
    fe, cce = pd.DataFrame(fe_rows), pd.DataFrame(cce_rows)
    fe["q_bh"] = bh(fe.p_wild_webb.values)
    cce["q_bh"] = bh(np.where(cce.estimador == "CCEP", cce.p_wild_webb, cce.p_dk))
    for df, nm in [(fe, "provincia_fe"), (cce, "provincia_cce")]:
        df["rotulo"] = "complemento anual; incluye provincias selladas en v2/v6 (solo exploratorio)"
        df.to_csv(OUT / f"{nm}.csv", index=False)
    pd.DataFrame(val_rows).to_csv(OUT / "provincia_valencia.csv", index=False)
    for df, nm in [(fe, "FE"), (cce, "CCE")]:
        for _, r in df.iterrows():
            REG.log("F-P", f"P_{nm}_{r.dependiente}_{r.spec}_{r.regresor}_{getattr(r, 'estimador', 'FE')}",
                    f"{r.dependiente} ~ {r.regresor} + flujos + {nm}", r.periodo[:4], r.periodo[-4:], r.n, np.nan, np.nan, np.nan, np.nan,
                    r.coef, r.p_wild_webb if not np.isnan(r.p_wild_webb) else r.p_dk, f"q_bh={r.q_bh:.3f}; prov={r.provincias}")
    RES["P"] = dict(fe_sig_bh10=int((fe.q_bh < .10).sum()), cce_sig_bh10=int((cce.q_bh < .10).sum()), n_fe=len(fe), n_cce=len(cce),
                    fe_core={f"{r.dependiente}|{r.regresor}": [float(r.coef), float(r.p_wild_webb), float(r.q_bh)] for _, r in fe[fe.spec == "core"].iterrows()},
                    cce_core={f"{r.dependiente}|{r.regresor}|{r.estimador}": [float(r.coef), float(r.q_bh)] for _, r in cce[cce.spec == "core"].iterrows()})


def main():
    np.random.seed(SEED)
    for k, f in [("h", run_h), ("l", run_l), ("r", run_r), ("p", run_p)]:
        if k in ONLY:
            f()
    REG.flush()
    (OUT / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1))
    (OUT / "resumen_numerico.json").write_text(json.dumps(RES, ensure_ascii=False, indent=1, default=float))
    res = dict(rama="R4b", pregunta="Heterogeneidad regional (jerarquico), proyecciones locales por exposicion hipotecaria, regulacion y provincia anual",
               capa="C4", datos="panel_ccaa_q_v7 (17 CCAA, 2007Q1-2026Q2), panel_prov_a_v7 (52 prov, 2002-2024); " + ROT,
               N="17 CCAA x ~75 T; 52 provincias x <=23 anios", metodo="ECM jerarquico pymc NUTS + MixedLM; LP de panel con EF, Driscoll-Kraay y wild Webb; FE/CCE",
               estimacion=RES, ic95="ver csv por modelo", p_ajustado="BH por familia (q=0,10), ver csv", nivel_evidencia="EXPLORATORIO",
               diagnosticos="R-hat/ESS/divergencias en resumen_numerico.json", fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
               notas="Asociaciones, sin lenguaje causal. Sin validacion fuera de muestra en este encargo. " + ROT + " Veredicto: ANALIZADA, NO CONCLUYENTE. Ver resumen.md.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()
