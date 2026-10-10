"""R1b-2 (BK-040): sensibilidad (Oster, Cinelli-Hazlett) y multiverso para diseños v2 (BI Bartik, BP SDiD H5/H6).

FÓRMULAS (propias; sensemakr no está instalado):
  Oster (2019), R_max = min(1,3·R²_largo, 1), R² intra-FE (sobre la y residualizada de los FE):
      β*(δ) = β_l − δ (β_c − β_l)(R_max − R²_l)/(R²_l − R²_c);   δ* con β*=0:
      δ* = β_l (R²_l − R²_c) / [(β_c − β_l)(R_max − R²_l)]      (|δ*|>1: la omisión necesitaría ser más fuerte que lo observado)
      β*(δ=1) = β_l − (β_c − β_l)(R_max − R²_l)/(R²_l − R²_c).   c=corto (solo FE), l=largo (FE + controles).
  Cinelli-Hazlett (2020), valor de robustez para q=1 (reducir la estimación a 0):
      f = |t|/√gl,   RV = ½(√(f⁴+4f²) − f²).
      RV_α (q=1): f* = f − t_{α/2, gl−1}/√(gl−1);  RV_α = ½(√(f*⁴+4f*²) − f*²) si f*>0, si no 0.
  gl = G−1 (clústeres; conservador) y, como referencia, gl = n−K.
Sin lenguaje causal: son sensibilidades de asociaciones (C4), no identificación.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src/v2"))
import bi_core as bc  # noqa: E402
import bp_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
OUT = RAIZ / "output/v5/R1B"
SEED = 20261010
reg = Registry(OUT / "registro_sens.csv")


def rv(t, gl, alpha=0.05):
    f = abs(t) / np.sqrt(gl)
    r = 0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2)
    fa = f - stats.t.ppf(1 - alpha / 2, gl - 1) / np.sqrt(gl - 1)
    ra = 0.5 * (np.sqrt(fa ** 4 + 4 * fa ** 2) - fa ** 2) if fa > 0 else 0.0
    return float(r), float(ra)


def holm_p(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * p[o]))
    out = np.empty(m)
    out[o] = adj
    return out


def cr1(yt, xt, cl, k_abs):
    """MCO univariante sobre variables ya residualizadas; EE CR1 por clúster."""
    b = (xt @ yt) / (xt @ xt)
    e = yt - b * xt
    G = cl.max() + 1
    s = np.bincount(cl, xt * e, G)
    n = len(yt)
    f = G / (G - 1) * (n - 1) / (n - k_abs - 1)
    se = np.sqrt(f * (s ** 2).sum()) / (xt @ xt)
    return float(b), float(se)


def oster(y_fe, x_fe, y_l, x_l, cl, k_fe, k_l, rmax_f=1.3):
    """y_fe,x_fe: residualizadas de FE; y_l,x_l: residualizadas de FE+controles."""
    sst = (y_fe ** 2).sum()
    bc_, _ = cr1(y_fe, x_fe, cl, k_fe)
    bl_, sel = cr1(y_l, x_l, cl, k_l)
    r2c = 1 - ((y_fe - bc_ * x_fe) ** 2).sum() / sst
    r2l = 1 - ((y_l - bl_ * x_l - 0) ** 2).sum() / sst   # el modelo largo también absorbe los controles: SSR de y_l-b x_l
    # R² del largo respecto de SST_FE: SSR(largo) = SSR de la regresión FWL con controles
    r2l = 1 - ((y_l - bl_ * x_l) ** 2).sum() / sst
    rmax = min(rmax_f * r2l, 1.0)
    den = (bc_ - bl_) * (rmax - r2l)
    delta = float(bl_ * (r2l - r2c) / den) if abs(den) > 1e-15 else float("inf")
    bstar = float(bl_ - (bc_ - bl_) * (rmax - r2l) / (r2l - r2c)) if abs(r2l - r2c) > 1e-12 else float("nan")
    t = bl_ / sel
    G = cl.max() + 1
    gl_n = len(y_l) - k_l - 1
    return dict(b_corto=bc_, b_largo=bl_, se_largo=sel, t=float(t), r2_corto=float(r2c), r2_largo=float(r2l), rmax=float(rmax),
                delta_oster=delta, beta_star_delta1=bstar, RV=rv(t, G - 1)[0], RV_alpha=rv(t, G - 1)[1],
                RV_gl_n=rv(t, gl_n)[0], RV_alpha_gl_n=rv(t, gl_n)[1])


# ------------------------------------------------------------------ BI
def bi():
    d, meta = bc.construir_panel()
    ctrl = ["ln_p02", "extr02", "paro02", "ln_pob02", "costa", "vut20_pm"]
    base = ["x", "z", "z_fwd", "x_stock", "y_alq", "y_pre"]
    out = {}
    m0 = bc.muestra(d, base + ctrl, 2009, 2021)
    m0["y_dif"] = m0.y_alq - m0.y_pre

    def W_of(m):
        t = (m["anio"] - 2015).values[:, None].astype(float)
        C = m[ctrl].values.astype(float)
        C = (C - C.mean(0)) / C.std(0)
        return C * t

    # --- sensibilidad Oster/CH (muestra 2009-2021 de BI: x,z,y_alq,y_pre sin NaN)
    fe = bc.FE(m0)
    W = W_of(m0)
    fel = bc.FE(m0, extra=W)
    cl = fe.cl
    res = {}
    for nom, yv, xv in (("OLS_alq_x", "y_alq", "x"), ("RF_alq_z", "y_alq", "z"), ("RF_dif_z", "y_dif", "z"), ("RF_pre_z", "y_pre", "z")):
        r = oster(fe.r(m0[yv]), fe.r(m0[xv]), fel.r(m0[yv]), fel.r(m0[xv]), cl, fe.k, fel.k)
        # referencia: 2SLS = RF / primera etapa (sin controles de tendencia): RV del RF vale para la 2SLS con el mismo t
        res[nom] = r
        reg.log("R1b-sens", f"BI_{nom}", f"{yv}~{xv}|FE prov+año; largo: +car2002xtend", m0.anio.min(), m0.anio.max(), len(m0), np.nan, np.nan,
                np.nan, coef_interes=r["b_largo"], p_interes=float(2 * stats.t.sf(abs(r["t"]), fe.G - 1)),
                notas=f"delta={r['delta_oster']:.3g}; RV={r['RV']:.3g}; RV_a={r['RV_alpha']:.3g}")
    # 2SLS base (misma muestra) para referencia
    yt, xt, zt = fe.r(m0.y_alq), fe.r(m0.x), fe.r(m0.z)
    r2 = bc.iv(yt, xt, zt, fe)
    res["2SLS_alq_base"] = dict(b=float(r2["b"][0]), se=float(r2["se"][0]), t=float(r2["b"][0] / r2["se"][0]))
    yl, xl, zl = fel.r(m0.y_alq), fel.r(m0.x), fel.r(m0.z)
    r2l = bc.iv(yl, xl, zl, fel)
    res["2SLS_alq_con_controles"] = dict(b=float(r2l["b"][0]), se=float(r2l["se"][0]), t=float(r2l["b"][0] / r2l["se"][0]))
    out["sensibilidad"] = res

    # --- multiverso
    muestras = [(2009, 2021), (2009, 2015), (2012, 2021), (2015, 2021), (2010, 2019)]
    filas = []
    for (a0, a1) in muestras:
        for zv in ("z", "z_fwd"):
            for xv in ("x", "x_stock"):
                for tend in (False, True):
                    for cc in (False, True):
                        for yv in ("y_alq", "y_dif"):
                            m = bc.muestra(d, [xv, zv, "y_alq", "y_pre"] + (ctrl if cc else []), a0, a1)
                            m["y_dif"] = m.y_alq - m.y_pre
                            Wm = W_of(m) if cc else None
                            f_ = bc.FE(m, tend=tend, extra=Wm)
                            yt, xt, zt = f_.r(m[yv]), f_.r(m[xv]), f_.r(m[zv])
                            try:
                                r = bc.iv(yt, xt, zt, f_)
                            except np.linalg.LinAlgError:
                                continue
                            b, se = float(r["b"][0]), float(r["se"][0])
                            p = float(2 * stats.t.sf(abs(b / se), f_.G - 1))
                            filas.append(dict(diseno="BI", resultado=yv, muestra=f"{a0}-{a1}", z=zv, x=xv, tend_prov=tend, controles_car02xt=cc,
                                              n=len(m), G=f_.G, b=b, se=se, p=p))
    mv = pd.DataFrame(filas)
    mv["p_holm"] = holm_p(mv.p.values)
    for (_, r) in mv.iterrows():
        reg.log("R1b-mv", f"BI_mv_{r.resultado}_{r.muestra}_{r.z}_{r.x}_t{int(r.tend_prov)}_c{int(r.controles_car02xt)}", "2SLS", r.muestra[:4], r.muestra[5:], r.n,
                np.nan, np.nan, np.nan, coef_interes=r.b, p_interes=r.p, notas=f"p_holm={r.p_holm:.4g}")
    mv.to_csv(OUT / "tablas/multiverso_BI.csv", index=False)
    out["multiverso"] = resumen_mv(mv, "y_alq")
    out["multiverso_dif"] = resumen_mv(mv, "y_dif")
    return out


def resumen_mv(mv, yv):
    x = mv[mv.resultado == yv]
    base = x[(x.muestra == "2009-2021") & (x.z == "z") & (x.x == "x") & (~x.tend_prov) & (~x.controles_car02xt)].iloc[0]
    s0 = np.sign(base.b)
    return dict(n_spec=len(x), signo_base=int(s0), coef_base=float(base.b), prop_mismo_signo=float((np.sign(x.b) == s0).mean()),
                prop_mismo_signo_sig_nominal=float(((np.sign(x.b) == s0) & (x.p < .05)).mean()),
                prop_mismo_signo_sig_holm=float(((np.sign(x.b) == s0) & (x.p_holm < .05)).mean()),
                rango_b=[float(x.b.min()), float(x.b.max())], mediana_b=float(x.b.median()))


# ------------------------------------------------------------------ BP
TR = ["08", "17", "25", "43"]
SELL = ["11", "16", "45"]


def bp(B=200):
    pan = vc.load("panel_prov_q")
    pan["trimestre"] = pan.trimestre.astype(str)
    pan["cod_prov"] = pan.cod_prov.astype(str)
    niv = np.log(pan.pivot(index="cod_prov", columns="trimestre", values="ipc_alquiler"))
    assert not set(SELL) & set(niv.index)
    qs = [q for q in niv.columns if "2012Q1" <= q <= "2023Q4"]
    qi = {q: i for i, q in enumerate(qs)}
    donantes = [u for u in sorted(niv.index) if u not in TR]
    out = {}

    # --- Oster/CH sobre la versión colapsada (cross-section): ΔY = media post1 − media pre
    def col(pre0, post0="2020Q4", post1="2022Q1", pre1="2020Q3"):
        pre = [q for q in qs if pre0 <= q <= pre1]
        post = [q for q in qs if post0 <= q <= post1]
        return niv[post].mean(axis=1) - niv[pre].mean(axis=1)
    dY = col("2016Q1")
    a = vc.load("panel_prov_a")
    a["cod_prov"] = a.cod_prov.astype(str)
    a15 = a[a.anio == 2015].set_index("cod_prov")
    X = pd.DataFrame({"ln_pob": np.log(a15.pob_total), "extr": 100 * a15.pob_extranj / a15.pob_total,
                      "ln_ptasado": np.log(a15.p_tasado), "paro": 100 * a15.parados / (a15.parados + a15.ocupados)})
    df = pd.concat([dY.rename("dY"), X], axis=1).dropna()
    df["D"] = df.index.isin(TR).astype(float)
    n = len(df)
    y = df.dY.values
    D = df.D.values
    C = ((df[X.columns] - df[X.columns].mean()) / df[X.columns].std()).values
    one = np.ones((n, 1))
    # corto: dY ~ 1 + D ; largo: + C. Oster con proyección sobre la constante
    def resid(v, Z):
        return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]
    yf, Df = resid(y, one), resid(D, one)
    Zl = np.hstack([one, C])
    yl, Dl = resid(y, Zl), resid(D, Zl)
    cl = np.arange(n)
    # EE robusta HC1 (cl=unidad) con k_abs=1 / 1+p
    r = oster(yf, Df, yl, Dl, cl, 1, 1 + C.shape[1])
    # RV con gl = n-K (no hay clústeres): sustituir
    gl = n - (1 + C.shape[1]) - 1
    r["RV"], r["RV_alpha"] = rv(r["t"], gl)
    r["nota"] = "versión colapsada (49 provincias, 4 tratadas): ΔY = media ln IPC alquiler 2020Q4-2022Q1 menos 2016Q1-2020Q3, controles 2015; HC1; gl=n-K. NO es el SDiD"
    out["sens_H5_colapsada"] = r
    reg.log("R1b-sens", "BP_H5_colapsada", "dY~D | +ln_pob,extr,ln_ptasado,paro (2015)", "2016Q1", "2022Q1", n, np.nan, np.nan, np.nan,
            coef_interes=r["b_largo"], p_interes=float(2 * stats.t.sf(abs(r["t"]), gl)), notas=f"delta={r['delta_oster']:.3g}; RV={r['RV']:.3g}")
    # --- H6 (publicado, muestra sellada): solo RV desde tau y se_placebo publicados; sin recalcular
    h6 = json.load(open(RAIZ / "output/v2/BP/h6_sellado.json"))["resultado"]["PRINCIPAL_ln_ipc_alquiler"]["sdid"]
    t6 = h6["tau"] / h6["se_placebo"]
    out["sens_H6_publicado"] = dict(tau=h6["tau"], se_placebo=h6["se_placebo"], t_aprox=float(t6), gl_supuesto=39,
                                    RV=rv(t6, 39)[0], RV_alpha=rv(t6, 39)[1],
                                    nota="aproximación: t=τ/se_placebo con gl=n_donantes-1; Oster no calculable sin los datos sellados (una evaluación, sin re-acceso)")

    # --- multiverso SDiD H5
    rng = np.random.default_rng(SEED)
    vecinas = ["22", "44", "50", "46", "12", "03", "07", "31", "25"]  # contexto: excluir Aragón, C. Valenciana, Baleares, Navarra (limítrofes/costa mediterránea)
    filas = []
    for pre0 in ("2012Q1", "2014Q1", "2016Q1", "2018Q1"):
        for pn, (p0, p1) in {"2020Q4-2022Q1": ("2020Q4", "2022Q1"), "2020Q4-2021Q4": ("2020Q4", "2021Q4"), "2021Q1-2022Q1": ("2021Q1", "2022Q1")}.items():
            for outv in ("nivel", "d4"):
                for dn in ("todos", "sin_limitrofes", "sin_top3_peso"):
                    Y = niv[qs] if outv == "nivel" else (niv - niv.shift(4, axis=1))[qs]
                    don = [u for u in donantes if u not in vecinas] if dn == "sin_limitrofes" else list(donantes)
                    qq = [q for q in qs if q >= pre0 or True]
                    pre = np.array([qi[q] for q in qs if pre0 <= q <= "2020Q3"])
                    post = np.array([qi[q] for q in qs if p0 <= q <= p1])
                    if outv == "d4":
                        pre = pre[pre >= 4]
                    units = TR + don
                    A = Y.loc[units].values
                    if not np.isfinite(A[:, np.r_[pre, post]]).all():
                        continue
                    if dn == "sin_top3_peso":
                        w = bl.sdid(A[4:], A[:4].mean(0), pre, post, n_tr=4)["omega"]
                        keep = np.argsort(w)[:-3]
                        units = TR + [don[i] for i in sorted(keep)]
                        A = Y.loc[units].values
                    tr, co = np.arange(4), np.arange(4, len(units))
                    subs = bl.draws_subsets(len(co), 4, B, seed=SEED)
                    r = bl.run_design(A, tr, co, pre, post, subs)
                    for mth, v in r.items():
                        filas.append(dict(diseno="BP_H5", metodo=mth, pre_ini=pre0, post=pn, resultado=outv, donantes=dn, n_don=len(co),
                                          tau=v["tau"], se_placebo=v["se_placebo"], p=v["p_dos"]))
    mv = pd.DataFrame(filas)
    mv["p_holm"] = holm_p(mv.p.values)
    mv.to_csv(OUT / "tablas/multiverso_BP_H5.csv", index=False)
    for i, r_ in mv.iterrows():
        reg.log("R1b-mv", f"BP_mv_{i}", f"{r_.metodo} {r_.resultado} pre={r_.pre_ini} post={r_.post} don={r_.donantes}", r_.pre_ini, "2022Q1", int(r_.n_don) + 4,
                np.nan, np.nan, np.nan, coef_interes=r_.tau, p_interes=r_.p, notas=f"p_holm={r_.p_holm:.4g}; B={B}")
    res = {}
    for mth, x in mv.groupby("metodo"):
        base = x[(x.pre_ini == "2016Q1") & (x.post == "2020Q4-2022Q1") & (x.resultado == "nivel") & (x.donantes == "todos")].iloc[0]
        s0 = np.sign(base.tau)
        res[mth] = dict(n_spec=len(x), tau_base=float(base.tau), signo_base=int(s0), prop_mismo_signo=float((np.sign(x.tau) == s0).mean()),
                        prop_mismo_signo_sig_nominal=float(((np.sign(x.tau) == s0) & (x.p < .05)).mean()),
                        prop_mismo_signo_sig_holm=float(((np.sign(x.tau) == s0) & (x.p_holm < .05)).mean()),
                        prop_negativo=float((x.tau < 0).mean()), rango_tau=[float(x.tau.min()), float(x.tau.max())])
    out["multiverso_H5"] = res
    out["B_permutaciones_multiverso"] = B
    return out


def main():
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)
    import sys as _s
    smoke = "--smoke" in _s.argv
    r = {"BI": bi()}
    r["BP"] = bp(B=20 if smoke else 200)
    r["BO_H4"] = "no ejecutado (presupuesto del módulo; BK-040 'si cabe')"
    (OUT / "tablas/sens_multiverso.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=float))
    reg.flush()
    print(json.dumps(r, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()
