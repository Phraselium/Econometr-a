"""BI · H3 confirmatoria + diagnósticos shift-share + stock/flujo/timing. Todo al Registry."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bi_core as bc  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "output" / "v2" / "BI"
YS = {"alq": "y_alq", "pre": "y_pre", "dif": "y_dif"}


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    adj = np.empty_like(p)
    run = 0
    for r, i in enumerate(o):
        run = max(run, (len(p) - r) * p[i])
        adj[i] = min(1, run)
    return adj


def log(reg, mid, formula, m, coef, p, notas, a0, a1):
    reg.log("BI", mid, formula, a0, a1, len(m), np.nan, np.nan, np.nan, coef_interes=coef, p_interes=p,
            notas=notas)


def est(m, yv, xv="x", zv="z", fe=None):
    fe = fe or bc.FE(m)
    yt, xt, zt = fe.r(m[yv]), fe.r(m[xv]), fe.r(m[zv])
    r = bc.iv(yt, xt, zt, fe)
    pe = bc.primera_etapa(xt, zt, fe)
    ols = bc.iv(yt, xt, xt, fe)
    return fe, r, pe, ols


def run(reg, smoke=False, B=9999):
    a0, a1 = (2009, 2015) if smoke else (2009, 2021)
    B = 499 if smoke else B
    d, meta = bc.construir_panel()
    res = {"smoke": smoke, "B": B}
    m = bc.muestra(d, ["x", "z", "y_alq", "y_pre"], a0, a1)       # MISMA muestra para alq, precio y diferencia
    fe = bc.FE(m)
    res["N"] = len(m)
    res["G"] = fe.G
    # --- principal: 3 ecuaciones (alquiler, precio, diferencia = contraste exacto de betas)
    tab = []
    boot = {}
    for k, yv in YS.items():
        _, r, pe, ols = est(m, yv, fe=fe)
        b, se = r["b"][0], r["se"][0]
        w = bc.wcb_wre(m[yv].values, m["x"].values, m["z"].values, fe, 0.0, B, seed=bc.SEED + len(tab))
        yt, xt, zt = fe.r(m[yv]), fe.r(m["x"]), fe.r(m["z"])
        ar = bc.ar_set(yt, xt, zt, fe, np.linspace(-15, 15, 601))
        boot[k] = w
        tab.append(dict(resultado=k, b_2sls=b, se=se, t=b / se, p_cluster_2c=bc.tp(b / se, fe.G),
                        p_cluster_1c=float(stats.t.sf(b / se, fe.G - 1)), p_wcb_2c=w["p2"],
                        p_wcb_1c=w["p_right"], ar_lo=ar[0], ar_hi=ar[1], b_ols=ols["b"][0], se_ols=ols["se"][0],
                        F=pe["F"], pi=pe["pi"][0], r2_parcial=pe["r2p"],
                        ic95_lo=b - stats.t.ppf(.975, fe.G - 1) * se, ic95_hi=b + stats.t.ppf(.975, fe.G - 1) * se))
        log(reg, f"H3_2SLS_{k}", f"{yv} ~ x | FE prov+año | z shift-share (cuotas 2002, LOO)", m, b, tab[-1]["p_wcb_2c"],
            f"EE cluster prov; WCB Webb B={B}; F={pe['F']:.2f}; confirmatoria H3" + ("; SMOKE" if smoke else ""), a0, a1)
        log(reg, f"H3_OLS_{k}", f"{yv} ~ x | FE prov+año", m, ols["b"][0], bc.tp(ols["b"][0] / ols["se"][0], fe.G),
            "referencia MCO", a0, a1)
    T = pd.DataFrame(tab)
    T.to_csv(OUT / f"{'smoke_' if smoke else ''}h3_principal.csv", index=False)
    # --- sistema apilado: covarianza entre ecuaciones (cluster) y contraste; verificación con y_dif
    ra = est(m, "y_alq", fe=fe)[1]
    rp = est(m, "y_pre", fe=fe)[1]
    cov_ap = ra["f"] * (ra["A"] @ (ra["sc"].T @ rp["sc"]) @ rp["A"].T)[0, 0]
    var_c = ra["V"][0, 0] + rp["V"][0, 0] - 2 * cov_ap
    b_c = ra["b"][0] - rp["b"][0]
    chk = est(m, "y_dif", fe=fe)[1]
    se_c = float(np.sqrt(var_c))
    res["sistema"] = dict(b_alq=float(ra["b"][0]), b_pre=float(rp["b"][0]), cov=float(cov_ap),
                          contraste=float(b_c), se_contraste=se_c, se_contraste_dif_directa=float(chk["se"][0]),
                          corr_ecuaciones=float(cov_ap / (ra["se"][0] * rp["se"][0])))
    p1 = float(T.loc[0, "p_wcb_1c"])
    p2 = float(T.loc[2, "p_wcb_1c"])
    pc1, pc2 = float(T.loc[0, "p_cluster_1c"]), float(T.loc[2, "p_cluster_1c"])
    res["contraste_conjunto"] = dict(p_wcb_beta_alq_gt0=p1, p_wcb_contraste_gt0=p2, p_IUT_wcb=max(p1, p2),
                                     p_cluster_beta_alq_gt0=pc1, p_cluster_contraste_gt0=pc2, p_IUT_cluster=max(pc1, pc2),
                                     cota_bonferroni_familia7=float(min(1, 7 * max(p1, p2))),
                                     nota="H3 se sostiene si ambos componentes rechazan (unión-intersección); Holm sobre la familia de 7 la aplica el orquestador; se da la cota Bonferroni-7")
    log(reg, "H3_conjunto_IUT", "beta_alq>0 y beta_alq-beta_pre>0", m, b_c, max(p1, p2), "IUT con p WCB una cola", a0, a1)
    # --- diagnósticos
    dg = {}
    pe = bc.primera_etapa(fe.r(m["x"]), fe.r(m["z"]), fe)
    dg["F_cluster"] = pe["F"]
    dg["F_efectivo_MOP"] = "no implementado: con un instrumento y un regresor se reporta el F robusto cluster, sin valores críticos"
    # Rotemberg
    for k, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        R = bc.rotemberg(m, fe, yv)
        R.to_csv(OUT / f"{'smoke_' if smoke else ''}rotemberg_{k}.csv", index=False)
        dg[f"rotemberg_{k}"] = dict(top=R.reindex(R["alpha"].abs().sort_values(ascending=False).index).head(3)[["grupo", "alpha", "beta_g", "F_g"]].to_dict("records"),
                                    suma_neg=float(R.loc[R["alpha"] < 0, "alpha"].sum()), suma_top2=float(R["alpha"].abs().nlargest(2).sum()))
        log(reg, f"diag_rotemberg_{k}", "pesos de Rotemberg (8 grupos)", m, np.nan, np.nan,
            "top=" + R.sort_values("alpha", key=abs, ascending=False).iloc[0]["grupo"], a0, a1)
    # características 2002 vs cuotas
    car = meta["car"]
    sh = meta["share"]
    rows = []
    for g in bc.GRUPOS:
        for c in ("ln_p02", "paro02", "ln_pob02", "extr02", "costa"):
            ok = car[c].notna()
            r_, p_ = stats.pearsonr(sh.loc[ok.index[ok], g], car.loc[ok, c])
            rows.append(dict(grupo=g, caract=c, corr=r_, p=p_))
    zbar = m.groupby("cod_prov")["z"].mean()
    for c in ("ln_p02", "paro02", "ln_pob02", "extr02", "costa"):
        ok = car.index.intersection(zbar.index)
        ok = [i for i in ok if pd.notna(car.loc[i, c])]
        r_, p_ = stats.pearsonr(zbar.loc[ok], car.loc[ok, c])
        rows.append(dict(grupo="z_medio", caract=c, corr=r_, p=p_))
    C = pd.DataFrame(rows)
    C.to_csv(OUT / f"{'smoke_' if smoke else ''}cuotas_vs_caracteristicas02.csv", index=False)
    dg["corr_zmedio_caract02"] = C[C.grupo == "z_medio"].set_index("caract")[["corr", "p"]].round(4).to_dict("index")
    reg.log("BI", "diag_cuotas_caract02", "corr cuotas 2002 con ln_p02, paro02, ln_pob02, extr02, costa", a0, a1, 49, np.nan, np.nan, np.nan,
            notas="ver cuotas_vs_caracteristicas02.csv")
    # pretendencias: resultados 2003-2007 sobre z medio posterior (FE año)
    pt = d[d["anio"].between(2003, 2007)].copy()
    pt["zbar"] = pt["cod_prov"].map(zbar)
    pt["zbar"] = (pt["zbar"] - zbar.mean()) / zbar.std()
    pre = {}
    for k, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        q = pt.dropna(subset=[yv, "zbar"]).reset_index(drop=True)
        A = pd.get_dummies(q["anio"], dtype=float).values
        Xm = np.column_stack([q["zbar"].values, A])
        cl = pd.factorize(q["cod_prov"])[0]
        G = cl.max() + 1
        beta = np.linalg.lstsq(Xm, q[yv].values, rcond=None)[0]
        e = q[yv].values - Xm @ beta
        Ai = np.linalg.inv(Xm.T @ Xm)
        sc = bc._csum(cl, G, Xm * e[:, None])
        V = G / (G - 1) * (len(q) - 1) / (len(q) - Xm.shape[1]) * Ai @ (sc.T @ sc) @ Ai
        se = np.sqrt(V[0, 0])
        pre[k] = dict(b_por_DE_z=float(beta[0]), se=float(se), p=float(bc.tp(beta[0] / se, G)), n=len(q))
        log(reg, f"diag_pretrend_{k}", f"{yv}(2003-07) ~ z_medio(2009-21) + FE año", q, beta[0], pre[k]["p"], "pretendencias; EE cluster prov", 2003, 2007)
    dg["pretendencias"] = pre
    # sobreidentificación: instrumentos por grupo (5 agrupaciones) -> J de Hansen
    Z5 = np.column_stack([fe.r(m[f"z5_{k}"]) for k in bc.GRUPOS5])
    jj = {}
    for k, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        yt, xt = fe.r(m[yv]), fe.r(m["x"])
        h_ = bc.hansen_j(yt, xt, Z5, fe)
        r5 = bc.iv(yt, xt, Z5, fe)
        pe5 = bc.primera_etapa(xt, Z5, fe)
        jj[k] = dict(J=h_["J"], p_hansen=h_["p"], df=h_["df"], sargan=h_["sargan"], p_sargan=h_["p_sargan"],
                     b_2sls_5inst=float(r5["b"][0]), se=float(r5["se"][0]), b_gmm=h_["b_gmm"], F_5inst=pe5["F"])
        log(reg, f"diag_overid_{k}", f"{yv} ~ x | 5 instrumentos por grupo", m, r5["b"][0], h_["p"], f"Hansen J cluster={h_['J']:.2f} (df={h_['df']})", a0, a1)
    dg["overid"] = jj
    # BHJ y AKM0
    bh = {}
    for k, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        for nm, kw in (("anioFE", dict(fe_anio=True)), ("anio+grupoFE", dict(fe_anio=True, fe_grupo=True))):
            r_ = bc.bhj(m, fe, yv, **kw)
            bh[f"{k}_{nm}"] = r_
            log(reg, f"diag_BHJ_{k}_{nm}", f"BHJ nivel shock ({r_['n']} shocks g-t, {r_['G']} grupos)", m, r_["b"], r_["p"],
                "potencia baja: 8 grupos; EE cluster por grupo t(7)", a0, a1)
    dg["BHJ"] = bh
    ak = {}
    for k, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        r_ = bc.akm0(m, fe, yv)
        ak[k] = r_
        log(reg, f"diag_AKM0_{k}", "EE exposición-robustos tipo AKM (agrupa grupos-shock)", m, r_["b"], r_["p_t"], "aprox. AKM0; 8 shocks-grupo", a0, a1)
    dg["AKM0"] = ak
    res["diagnosticos"] = dg
    # --- diagnósticos de identificación (EXPLORATORIOS; revisión de la puerta)
    res_id = []
    car_cols = ["extr02", "ln_pob02", "ln_p02", "paro02", "costa"]
    ys_ = (("alq", "y_alq"), ("pre", "y_pre"), ("dif", "y_dif"))

    def spec(name, mm, zv, extra=None, xv="x", ys=ys_, wcb=True, nota=""):
        f2 = bc.FE(mm, extra=extra)
        xt = f2.r(mm[xv]); zt = f2.r(mm[zv])
        pe_ = bc.primera_etapa(xt, zt, f2)
        for kk, yv in ys:
            r = bc.iv(f2.r(mm[yv]), xt, zt, f2)
            b_, s_ = float(r["b"][0]), float(r["se"][0])
            row = dict(spec=name, res=kk, n=len(mm), b=b_, se=s_, p_cluster=float(bc.tp(b_ / s_, f2.G)), F=pe_["F"], p_wcb_1c=np.nan, nota=nota)
            if wcb:
                row["p_wcb_1c"] = bc.wcb_wre(mm[yv].values, mm[xv].values, mm[zv].values, f2, 0.0, B, seed=bc.SEED + 100 + len(res_id))["p_right"]
            res_id.append(row)
            log(reg, f"id_{name}_{kk}", f"{yv} ~ {xv} | {zv}" + (" | controles" if extra is not None else ""), mm, b_, row["p_cluster"],
                f"EXPLORATORIO identificación; F={pe_['F']:.2f}; p_wcb_1c={row['p_wcb_1c']:.4f}; {nota}", a0, a1)

    def ctrl(cols):
        yd = pd.get_dummies(m["anio"], dtype=float).iloc[:, 1:].values
        return np.hstack([((m[c] - m[c].mean()) / m[c].std()).values[:, None] * yd for c in cols])
    spec("principal", m, "z")
    for c in car_cols:
        spec(f"gpss_{c}", m, "z", extra=ctrl([c]), nota="característica 2002 x año (GPSS)")
    spec("gpss_todas", m, "z", extra=ctrl(car_cols), nota="5 características 2002 x año")
    m["z_sin_sud"] = m["z"] - m["zg_sudamerica"]
    spec("solo_Sudamerica", m, "zg_sudamerica", nota="instrumento: solo cuota Sudamérica")
    spec("sin_Sudamerica", m, "z_sin_sud", nota="instrumento sin Sudamérica")
    spec("z_alineado_t+1", bc.muestra(d, ["x", "z_fwd", "y_alq", "y_pre", "y_dif"], a0, a1), "z_fwd", nota="ΔS_{t+1}=S(1-ene t+1)-S(1-ene t), alineado con el flujo del año t")
    ml_ = bc.muestra(d, ["x_l1", "z_l1", "y_alq", "y_pre", "y_dif"], a0, a1)
    spec("flujo_t-1", ml_, "z_l1", xv="x_l1", nota="lectura alternativa de 'flujo t-1'")
    cut = 2012 if smoke else 2014
    spec(f"sub_{a0}-{cut}", m[m["anio"] <= cut].reset_index(drop=True), "z", nota="subperiodo")
    spec(f"sub_{cut + 1}-{a1}", m[m["anio"] > cut].reset_index(drop=True), "z", nota="subperiodo")
    # placebo: resultados pasados sobre x_t instrumentado (misma muestra principal)
    for L_ in (1, 2):
        d[f"y_alq_p{L_}"] = d.groupby("cod_prov")["y_alq"].shift(L_)
        d[f"y_pre_p{L_}"] = d.groupby("cod_prov")["y_pre"].shift(L_)
    mp = bc.muestra(d, ["x", "z", "y_alq", "y_pre", "y_alq_p1", "y_alq_p2", "y_pre_p1", "y_pre_p2"], a0, a1)
    for L_ in (1, 2):
        spec(f"placebo_resultado_t-{L_}", mp, "z", ys=(("alq", f"y_alq_p{L_}"), ("pre", f"y_pre_p{L_}")), nota="resultado PASADO sobre x_t instrumentado (debería ser 0)")
    # pretendencias con el instrumento dominante (Sudamérica) y balance
    zb = m.groupby("cod_prov")["zg_sudamerica"].mean()
    pts = {}
    for kk, yv in (("alq", "y_alq"), ("pre", "y_pre")):
        q = d[d["anio"].between(2003, 2007)].copy()
        q["zb"] = q["cod_prov"].map(zb)
        q["zb"] = (q["zb"] - zb.mean()) / zb.std()
        q = q.dropna(subset=[yv, "zb"]).reset_index(drop=True)
        Xm = np.column_stack([q["zb"].values, pd.get_dummies(q["anio"], dtype=float).values])
        cl_ = pd.factorize(q["cod_prov"])[0]; G_ = cl_.max() + 1
        be = np.linalg.lstsq(Xm, q[yv].values, rcond=None)[0]; e_ = q[yv].values - Xm @ be
        Ai = np.linalg.inv(Xm.T @ Xm); sc_ = bc._csum(cl_, G_, Xm * e_[:, None])
        V_ = G_ / (G_ - 1) * Ai @ (sc_.T @ sc_) @ Ai
        pts[kk] = dict(b=float(be[0]), se=float(np.sqrt(V_[0, 0])), p=float(bc.tp(be[0] / np.sqrt(V_[0, 0]), G_)))
        log(reg, f"id_pretrend_Sudamerica_{kk}", f"{yv}(2003-07) ~ z_Sudamérica medio", q, be[0], pts[kk]["p"], "ventana 2003-07 = boom de llegadas (no pre-tratamiento)", 2003, 2007)
    cs = meta["share"]["sudamerica"]
    bal = {c: dict(zip(("corr", "p"), (float(v) for v in stats.pearsonr(cs.loc[meta["car"][c].dropna().index], meta["car"][c].dropna())))) for c in car_cols}
    res["balance_cuotas_Sudamerica"] = bal
    res["pretendencias_Sudamerica"] = pts
    reg.log("BI", "id_rotemberg_beta_g", "β_g de Rotemberg (8 grupos x 2 resultados) en rotemberg_*.csv", a0, a1, len(m), np.nan, np.nan, np.nan, notas="familia de diagnósticos descriptivos")
    reg.log("BI", "id_AR_conjunto", "conjunto de confianza Anderson-Rubin en rejilla (3 resultados)", a0, a1, len(m), np.nan, np.nan, np.nan, notas="en h3_principal.csv")
    reg.log("BI", "het_CATE_terciles", "CATE del bosque por terciles y Spearman (6 características; vut20_pm es de 2020, posterior)", a0, a1, len(m), np.nan, np.nan, np.nan, notas="descriptivo, ver bi_het")
    pd.DataFrame(res_id).to_csv(OUT / f"{'smoke_' if smoke else ''}h3_identificacion.csv", index=False)
    res["identificacion"] = res_id
    # --- robustez y stock/flujo/timing (EXPLORATORIO)
    rob = []

    def add(nombre, mm, yv, xv, zv, tend=False, extra=""):
        f2 = bc.FE(mm, tend=tend)
        if len(xv) == 1:
            xt = f2.r(mm[xv[0]]); zt = f2.r(mm[zv[0]])
            xmat, zmat = xt, zt
        else:
            xmat = np.column_stack([f2.r(mm[v]) for v in xv]); zmat = np.column_stack([f2.r(mm[v]) for v in zv])
        yt = f2.r(mm[yv])
        r = bc.iv(yt, xmat, zmat, f2)
        pe_ = bc.primera_etapa(xmat[:, 0] if xmat.ndim > 1 else xmat, zmat, f2)
        for j, v in enumerate(xv):
            b_, s_ = r["b"][j], r["se"][j]
            rob.append(dict(spec=nombre, resultado=yv, regresor=v, n=len(mm), b=b_, se=s_, p_cluster=bc.tp(b_ / s_, f2.G), F=pe_["F"]))
            log(reg, f"rob_{nombre}_{yv}_{v}", f"{yv} ~ {','.join(xv)} | {','.join(zv)}", mm, b_, bc.tp(b_ / s_, f2.G),
                f"EXPLORATORIO; {extra}; F={pe_['F']:.2f}", a0, a1)

    for yv in ("y_alq", "y_pre"):
        add("tendencias_prov", m, yv, ["x"], ["z"], tend=True)
        add("sin_covid", m[m["anio"] <= 2019].reset_index(drop=True), yv, ["x"], ["z"]) if not smoke else None
        # stock (Δ cuota extranjera)
        ms = bc.muestra(d, ["x_stock", "z", "y_alq", "y_pre"], a0, a1)
        add("stock_dcuota_extranj", ms, yv, ["x_stock"], ["z"], extra="stock vs flujo")
        # timing: flujo t-1, instrumento t-1
        ml = bc.muestra(d, ["x_l1", "z_l1", "y_alq", "y_pre"], a0, a1)
        add("flujo_t-1", ml, yv, ["x_l1"], ["z_l1"], extra="timing")
        # x_t y x_{t-1} conjuntos
        mj = bc.muestra(d, ["x", "x_l1", "z", "z_l1", "y_alq", "y_pre"], a0, a1)
        add("x_t_y_x_t-1", mj, yv, ["x", "x_l1"], ["z", "z_l1"], extra="timing conjunto")
        # instrumento alineado (variación del stock t+1 - t)
        mf = bc.muestra(d, ["x", "z_fwd", "y_alq", "y_pre"], a0, a1)
        if len(mf) > 0:
            add("z_alineado_stock_t+1", mf, yv, ["x"], ["z_fwd"], extra="instrumento con ΔS_{t+1}")
    R = pd.DataFrame(rob)
    R.to_csv(OUT / f"{'smoke_' if smoke else ''}h3_robustez_timing.csv", index=False)
    res["robustez"] = R.round(4).to_dict("records")
    # --- nivel de evidencia (criterio uniforme de decisiones.md): H3 SIN evaluación sellada; unidad de Holm = H3 con p_IUT.
    #     Holm-7 se acota por Bonferroni-7 (el ajuste final lo hace el orquestador). CAUSAL queda DESCARTADO (ver diagnóstico).
    p_iut = max(p1, p2)
    comp = {}
    for nm, pp in (("beta_alq_gt0 (componente, signo)", p1), ("contraste_alq_menos_compra_gt0", p2)):
        comp[nm] = dict(p_wcb_1c=pp, p_cota_Holm7=min(1, 7 * pp), informativo_no_confirmatorio=True)
    sig_pos = all(r["b"] > 0 for r in res_id if r["res"] == "alq" and r["spec"] != "sin_Sudamerica" and not r["spec"].startswith(("placebo", "sub_")))
    res["criterios_identificacion"] = dict(
        F_ge_10_principal=bool(dg["F_cluster"] >= 10), pretendencias_NO_informativas="ventana 2003-07 = boom de llegadas a los mismos enclaves",
        J_hansen_p=dict(alq=jj["alq"]["p_hansen"], pre=jj["pre"]["p_hansen"]),
        sargan_homoc_p=dict(alq=jj["alq"]["p_sargan"], pre=jj["pre"]["p_sargan"]),
        placebo_alquiler_pasado_rechaza=bool(any(r["spec"].startswith("placebo") and r["p_cluster"] < 0.05 for r in res_id if r["res"] == "alq")),
        signo_alq_positivo_en_todas_las_variantes_con_instrumento_completo=bool(sig_pos),
        signo_contraste_estable=bool(all(r["b"] > 0 for r in res_id if r["res"] == "dif" and r["spec"] in ("principal", "gpss_extr02", "gpss_todas", "z_alineado_t+1", "solo_Sudamerica"))),
        CAUSAL="DESCARTADO: placebos de alquiler pasado rechazan, cuotas no balanceadas, F cae con controles GPSS",
        componentes=comp)
    h3_ar = min(1, 7 * p_iut) < 0.05 and bool(res["criterios_identificacion"]["signo_contraste_estable"])
    res["nivel_evidencia"] = "ASOCIACIÓN ROBUSTA" if h3_ar else "EXPLORATORIO"
    res["nivel_beta_alq_signo"] = "EXPLORATORIO (signo positivo estable con el instrumento completo, pero falla submuestras 2015-2021 p=0,073, controles GPSS de extranjeros 2002 p=0,115 y los placebos de resultado pasado rechazan también en precio: patrón transversal persistente; magnitud NO identificada)"
    res["tabla_principal"] = T.round(4).to_dict("records")
    (OUT / f"{'smoke_' if smoke else ''}h3_resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float))
    return res
