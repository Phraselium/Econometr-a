"""Rama BV (compra): H2 (confirmatoria), periodos, arbitraje alquiler-compra, nacional, fuera de muestra.
Uso: python src/v2/bv_main.py [--smoke]   (smoke: 10 provincias, 2010-2019, B=199 -> output/v2/BV/smoke/)"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bv_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402

warnings.filterwarnings("ignore")
SMOKE = "--smoke" in sys.argv
OUT = bl.OUT / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)
B = 199 if SMOKE else 9999
reg = bl.Registry(OUT / "registro.csv")
signos = []   # tabla de signos


def csv(df, name):
    df.to_csv(OUT / name, index=False, float_format="%.8g")


pan0, nac0 = vc.load("panel_prov_q"), vc.load("nacional_q_v2")
pan = bl.preparar_panel(pan0, nac0)
pan = pan.replace([np.inf, -np.inf], np.nan)
if SMOKE:
    provs = sorted(pan["cod_prov"].unique())[:10]
    pan = pan[pan["cod_prov"].isin(provs) & pan["trimestre"].between("2010Q1", "2019Q4")].copy()
nprov = pan["cod_prov"].nunique()
print("panel", pan.shape, "provincias", nprov, flush=True)

# ============================================================ 1. H2
Y = "d4_ln_p_real"
X0 = ["d4_ln_hipotecas_importe", "cu_x_expo", "d4_ln_ocupados"]
ESPERADO = {"d4_ln_hipotecas_importe": "+", "hip_l4": "+", "cu_x_expo": "-", "d4_ln_ocupados": "+"}


def corre_h2(id_, df, y, xs, nota, boot=False):
    m = bl.FE(df, y, xs)
    t = m.tabla()
    t["p_wcb"] = np.nan
    if boot:
        for j in range(len(xs)):
            t.loc[j, "p_wcb"] = m.wild_cluster_boot(j, B=B)
    t.insert(0, "spec", id_)
    t["N"], t["G"] = m.N, m.G
    sub = m.d["trimestre"]
    for _, r in t.iterrows():
        reg.log("H2", id_, f"{y} ~ {' + '.join(xs)} | FE prov + trim | cluster prov", sub.min(), sub.max(), m.N,
                np.nan, np.nan, np.nan, coef_interes=r["coef"], p_interes=r["p"],
                notas=f"var={r['var']} p_wcb={r['p_wcb']} {nota} B={B if boot else 0}")
    return t, m


res_h2 = []
t0, m0 = corre_h2("H2_principal", pan, Y, X0, "especificación pre-registrada; Δ4 ln p_tasado real (deflactor nacional ln_deflactor de nacional_q_v2)", True)
res_h2.append(t0)
t1, _ = corre_h2("H2_credito_l4", pan, Y, ["hip_l4", "cu_x_expo", "d4_ln_ocupados"], "crédito retardado 4 trimestres (simultaneidad)", True)
res_h2.append(t1)
pan["d4_ln_p_nom"] = pan["d4_ln_p_tasado"]
res_h2.append(corre_h2("H2_nominal_equivalente_por_FE_trim", pan, "d4_ln_p_nom", X0, "NO es robustez: el deflactor es nacional y lo absorbe el FE de trimestre (equivalente numérico)")[0])
res_h2.append(corre_h2("H2_ambos_cred", pan, Y, ["d4_ln_hipotecas_importe", "hip_l4", "cu_x_expo", "d4_ln_ocupados"], "robustez: crédito t y t-4")[0])
res_h2.append(corre_h2("H2_sin_credito", pan, Y, ["cu_x_expo", "d4_ln_ocupados"], "robustez: sin crédito")[0])
if not SMOKE:
    res_h2.append(corre_h2("H2_sub_hasta2013", pan[pan.trimestre <= "2013Q4"], Y, X0, "submuestra 2004Q1-2013Q4")[0])
    res_h2.append(corre_h2("H2_sub_desde2014", pan[pan.trimestre >= "2014Q1"], Y, X0, "submuestra 2014Q1-2024Q2")[0])
    res_h2.append(corre_h2("H2_sin_covid", pan[~pan.trimestre.between("2020Q1", "2021Q4")], Y, X0, "sin 2020-2021")[0])
    res_h2.append(corre_h2("H2_sin_madrid_bcn", pan[~pan.cod_prov.isin(["08", "28"])], Y, X0, "sin Madrid ni Barcelona")[0])
else:
    res_h2.append(corre_h2("H2_sub_hasta2014", pan[pan.trimestre <= "2014Q4"], Y, X0, "smoke submuestra")[0])
h2 = pd.concat(res_h2, ignore_index=True)
csv(h2, "h2_resultados.csv")

# Holm / BH sobre los dos contrastes de H2 (crédito, interacción) con p del wild cluster bootstrap
fam = {r["var"]: r["p_wcb"] for _, r in t0.iterrows() if r["var"] in ("d4_ln_hipotecas_importe", "cu_x_expo")}
holm_h2, bh_h2 = bl.holm(fam), bl.bh(fam)
fam_l4 = {r["var"]: r["p_wcb"] for _, r in t1.iterrows() if r["var"] in ("hip_l4", "cu_x_expo")}
holm_l4 = bl.holm(fam_l4)
adj = pd.DataFrame([{"coef": k, "p_wcb": fam[k], "p_holm_m2": holm_h2[k], "p_bh_m2": bh_h2[k],
                     "p_bonf_x7_conservador": min(1, fam[k] * 7)} for k in fam])
csv(adj, "h2_p_ajustados.csv")
for _, r in t0.iterrows():
    signos.append(dict(analisis="H2 principal (confirmatoria, sin sellado)", variable=r["var"],
                       esperado=ESPERADO[r["var"]], estimado="+" if r["coef"] > 0 else "-",
                       coincide=(ESPERADO[r["var"]] == ("+" if r["coef"] > 0 else "-")), p=r["p_wcb"], coef=r["coef"]))
for _, r in t1.iterrows():
    signos.append(dict(analisis="H2 crédito retardado 4T", variable=r["var"], esperado=ESPERADO[r["var"]],
                       estimado="+" if r["coef"] > 0 else "-",
                       coincide=(ESPERADO[r["var"]] == ("+" if r["coef"] > 0 else "-")), p=r["p_wcb"], coef=r["coef"]))
print(t0.round(4).to_string(), flush=True)
print(t1.round(4).to_string(), flush=True)

# ============================================================ 2. Periodos (EXPLORATORIO)
pan["per"] = pan["trimestre"].map(bl.periodo_de)
pp = pan[pan["per"].notna()].copy()
pp["cu"] = pp["coste_uso_aprox"]
FAM = {"credito_tipos": ["d4_ln_hipotecas_importe"], "coste_de_uso": ["cu_x_expo"],
       "empleo_renta": ["d4_ln_ocupados"], "demografia": ["d4_ln_pob_20_34", "d4_ln_pob_extranj"],
       "oferta": ["d4_ln_terminadas_libres"]}
VARS_B = [v for f in FAM.values() for v in f]
ppB = pp.dropna(subset=VARS_B + [Y]).copy()
if SMOKE:                       # sin periodos completos: solo se ejercita el código con los periodos disponibles
    pass
perlist = [p for p in bl.PERIODOS if (ppB["per"] == p).sum() > 30]
cols, names = [], []
for p in perlist:
    for v in VARS_B:
        c = f"{v}__{p}"
        ppB[c] = np.where(ppB["per"] == p, ppB[v], 0.0)
        cols.append(c)
mB = bl.FE(ppB, Y, cols, fe_time=False, extra_fe="per")
tB = mB.tabla()
tB[["variable", "periodo"]] = tB["var"].str.split("__", expand=True)
tB["N"] = mB.N
csv(tB, "periodos_coeficientes_modeloB.csv")
for _, r in tB.iterrows():
    reg.log("P_periodos", "B_" + r["var"], f"{Y} ~ vars x periodo | FE prov + intercepto de periodo | cluster prov",
            "", "", mB.N, np.nan, np.nan, np.nan, coef_interes=r["coef"], p_interes=r["p"], notas="EXPLORATORIO")
xbar_all = ppB[VARS_B].mean()
contrib = []
from scipy import stats as _st  # noqa: E402
tcrit = _st.t.ppf(0.975, mB.G - 1)
for p in perlist:
    sub = ppB[ppB["per"] == p]
    dx = sub[VARS_B].mean() - xbar_all
    # coste de uso: efecto diferencial de una provincia con exposición +1 DE (expo=1): beta_p x (cu_p - cu_total);
    # el nivel nacional de cu queda absorbido por el intercepto de periodo (no identificado aparte)
    dx["cu_x_expo"] = sub["cu"].mean() - ppB["cu"].mean()
    tot_est, tot_c = 0.0, np.zeros(len(cols))
    for fam_name, vs in FAM.items():
        c = np.zeros(len(cols))
        for v in vs:
            c[cols.index(f"{v}__{p}")] = dx[v]
        est = float(c @ mB.beta)
        se = float(np.sqrt(c @ mB.cov @ c))
        contrib.append(dict(periodo=p, familia=fam_name, contribucion_pp=100 * est, ic95_inf=100 * (est - tcrit * se),
                            ic95_sup=100 * (est + tcrit * se), se=100 * se))
        tot_c += c
    est = float(tot_c @ mB.beta)
    se = float(np.sqrt(tot_c @ mB.cov @ tot_c))
    obs = sub[Y].mean() - ppB[Y].mean()
    contrib.append(dict(periodo=p, familia="TOTAL_explicado", contribucion_pp=100 * est, ic95_inf=100 * (est - tcrit * se),
                        ic95_sup=100 * (est + tcrit * se), se=100 * se))
    contrib.append(dict(periodo=p, familia="OBSERVADO_desv_media", contribucion_pp=100 * obs, ic95_inf=np.nan, ic95_sup=np.nan, se=np.nan))
    contrib.append(dict(periodo=p, familia="RESTO_(FE,interceptos,no_explicado)", contribucion_pp=100 * (obs - est), ic95_inf=np.nan, ic95_sup=np.nan, se=np.nan))
contrib = pd.DataFrame(contrib)
csv(contrib, "periodos_contribuciones.csv")
for _, r in contrib.iterrows():
    reg.log("P_periodos", f"contrib_{r['periodo']}_{r['familia']}", "beta_p x (xbar_p - xbar_total)", "", "", mB.N, np.nan, np.nan, np.nan,
            coef_interes=r["contribucion_pp"], notas="EXPLORATORIO; pp de Δ4 ln precio real")

# modelo A por periodo (spec H2 con FE de trimestre, coeficientes por periodo)
ppA = pp.dropna(subset=X0 + [Y]).copy()
colsA = []
for p in perlist:
    for v in X0:
        c = f"{v}__{p}"
        ppA[c] = np.where(ppA["per"] == p, ppA[v], 0.0)
        colsA.append(c)
mA = bl.FE(ppA, Y, colsA)
tA = mA.tabla()
tA[["variable", "periodo"]] = tA["var"].str.split("__", expand=True)
csv(tA, "periodos_coeficientes_H2_FEtrim.csv")
pvals_p = {r["var"]: r["p"] for _, r in tA.iterrows()}
hp, bp = bl.holm(pvals_p), bl.bh(pvals_p)
tA["p_holm"] = tA["var"].map(hp)
tA["p_bh"] = tA["var"].map(bp)
csv(tA, "periodos_coeficientes_H2_FEtrim.csv")
for _, r in tA.iterrows():
    reg.log("P_periodos", "A_" + r["var"], f"{Y} ~ X0 x periodo | FE prov+trim | cluster prov", "", "", mA.N, np.nan, np.nan, np.nan,
            coef_interes=r["coef"], p_interes=r["p"], notas=f"EXPLORATORIO p_holm={r['p_holm']:.4g} p_bh={r['p_bh']:.4g}")
    e = ESPERADO[r["variable"]]
    signos.append(dict(analisis=f"Periodo {r['periodo']} (expl.)", variable=r["variable"], esperado=e,
                       estimado="+" if r["coef"] > 0 else "-", coincide=(e == ("+" if r["coef"] > 0 else "-")),
                       p=r["p"], coef=r["coef"]))

# ============================================================ 3. Arbitraje alquiler-compra (EXPLORATORIO)
a = pan.copy()
a["q"] = a["trimestre"].str[:4].astype(int) * 4 + a["trimestre"].str[-1].astype(int)
a["dev_ratio"] = a["ratio_precio_alquiler_idx"] - a.groupby("cod_prov")["ratio_precio_alquiler_idx"].transform("mean")
a = a.sort_values(["cod_prov", "q"])
a["dev_exp"] = a["ratio_precio_alquiler_idx"] - a.groupby("cod_prov")["ratio_precio_alquiler_idx"].transform(
    lambda s: s.expanding(min_periods=20).mean().shift(1))
lp_rows = []
base = a[["cod_prov", "q", "ln_p_tasado", "ln_ipc_alquiler"]]
for h in range(1, 9):
    fut = base.copy()
    fut["q"] = fut["q"] - h
    m = a.merge(fut.rename(columns={"ln_p_tasado": "lp_f", "ln_ipc_alquiler": "lr_f"}), on=["cod_prov", "q"], how="left")
    m["y_precio"] = m["lp_f"] - m["ln_p_tasado"]
    m["y_alq"] = m["lr_f"] - m["ln_ipc_alquiler"]
    for disp, dv in (("media_total", "dev_ratio"), ("media_expansiva", "dev_exp")):
        for yn in ("y_precio", "y_alq"):
            f = bl.FE(m, yn, [dv, "d4_ln_p_tasado", "d4_ln_ipc_alquiler"])
            r = f.tabla().iloc[0]
            lp_rows.append(dict(h=h, desv=disp, outcome=yn, coef=r["coef"], se=r["se"], p=r["p"], ic95_inf=r["ic95_inf"],
                                ic95_sup=r["ic95_sup"], N=f.N))
            reg.log("ARB_LP", f"LP_{disp}_{yn}_h{h}", f"{yn}(t+{h}) ~ {dv} + d4 ln p + d4 ln alq | FE prov+trim | cluster prov",
                    "", "", f.N, np.nan, np.nan, np.nan, coef_interes=r["coef"], p_interes=r["p"], notas="EXPLORATORIO")
lp = pd.DataFrame(lp_rows)
lp["p_holm_m16"] = np.nan
lp["p_bh_m16"] = np.nan
for dsv in ("media_total", "media_expansiva"):
    sel = lp[lp.desv == dsv]
    keys = {i: p_ for i, p_ in zip(sel.index, sel.p)}
    hh, bb = bl.holm(keys), bl.bh(keys)
    for i in sel.index:
        lp.loc[i, "p_holm_m16"], lp.loc[i, "p_bh_m16"] = hh[i], bb[i]
csv(lp, "arbitraje_lp.csv")
for yn, esp in (("y_precio", "-"), ("y_alq", "+")):
    s = lp[(lp.desv == "media_expansiva") & (lp.outcome == yn)]
    signos.append(dict(analisis="Arbitraje LP (expl.) h=1..8", variable=f"dev_ratio->{yn}", esperado=esp,
                       estimado=f"{(s.coef > 0).sum()}+/{(s.coef < 0).sum()}-", coincide=bool(((s.coef < 0) if esp == "-" else (s.coef > 0)).all()),
                       p=float(s.p.min()), coef=float(s.coef.mean())))
print(lp[lp.desv == "media_expansiva"].round(4).to_string(), flush=True)

# ============================================================ 4-5. Fuera de muestra
DESDE, MINTR = ("2014Q1", 8) if SMOKE else ("2012Q1", 8)
nac = nac0.copy()
nac["trimestre"] = nac["trimestre"].astype(str)


def comun(dfs):
    idx = None
    for d in dfs:
        k = d.dropna(subset=["y_real", "y_pred"]).drop_duplicates(["unidad", "periodo"]).set_index(["unidad", "periodo"]).index
        idx = k if idx is None else idx.intersection(k)
    out = []
    for d in dfs:
        e = d.set_index(["unidad", "periodo"])
        out.append(e.loc[idx].reset_index().assign(h=d["h"].iloc[0], modelo=d["modelo"].iloc[0]))
    return out


def oos(nombre, fase, base_fn, ecm_fn, run_fn, cfgs, desc, extra_cols=None):
    pres = bl.vc.Presupuesto(reg, fase, len(cfgs), desc)
    ar4, ecm = base_fn(), ecm_fn()
    modelos = {c: run_fn(c) for c in cfgs}
    allp = comun([ar4, ecm] + list(modelos.values()))
    ar4c, ecmc, mods = allp[0], allp[1], dict(zip(cfgs, allp[2:]))
    rows = []
    for c in cfgs:
        ev = vc.evaluar(mods[c], {vc.BASE: ar4c, vc.ECM: ecmc}, 4).iloc[0].to_dict()
        ev.update(cfg=c)
        rows.append(ev)
        pres.usar(f"{fase}_{c}", {"cfg": c}, formula=desc, muestra_ini=DESDE, muestra_fin="2024Q2", n=int(ev["n"]), rmse_oos=ev["rmse"],
                  notas=f"DM vs AR4={ev['dm_vs_AR4']:.3f} p={ev['p_vs_AR4']:.3f}; vs ECM={ev['dm_vs_ECM_v1']:.3f} p={ev['p_vs_ECM_v1']:.3f}")
    t = pd.DataFrame(rows)
    pv = {}
    for _, r in t.iterrows():
        pv[f"{r.cfg}|AR4"], pv[f"{r.cfg}|ECM"] = r["p_vs_AR4"], r["p_vs_ECM_v1"]
    pv = {k: (1.0 if np.isnan(v) else v) for k, v in pv.items()}
    hm, bhh = bl.holm(pv), bl.bh(pv)
    t["p_holm_vs_AR4"] = [hm[f"{c}|AR4"] for c in t.cfg]
    t["p_holm_vs_ECM"] = [hm[f"{c}|ECM"] for c in t.cfg]
    t["p_bh_vs_AR4"] = [bhh[f"{c}|AR4"] for c in t.cfg]
    t["p_bh_vs_ECM"] = [bhh[f"{c}|ECM"] for c in t.cfg]
    t["mejora_vs_AR4"] = t["rmse"] < t["rmse_AR4"]
    t["mejora_vs_ECM"] = t["rmse"] < t["rmse_ECM_v1"]
    csv(t, nombre)
    return t, ar4c, ecmc


tp, _, _ = oos("oos_panel.csv", "OOS_panel",
               lambda: vc.panel_ar4(pan, "p_tasado", "cod_prov", 4, real=True, nac=nac, desde=DESDE, min_train=MINTR),
               lambda: vc.panel_ecm_v1(pan, "p_tasado", "cod_prov", 4, real=True, nac=nac, desde=DESDE, min_train=MINTR),
               lambda c: bl.run_panel_model(pan, nac, c, desde=DESDE, min_train=MINTR),
               ["C1", "C2", "C3", "C4", "C5", "C6"],
               "panel h=4 var_precio=p_tasado real; C1 AR4+Δ4hip; C2 +Δ4ocup; C3 +cu+cu×expo; C4 sin AR; C5 crédito t-4; C6 AR4+coste uso")
print(tp.round(4).to_string(), flush=True)
nac_ok = nac[nac["trimestre"] <= vc.Q_TRAIN_FIN].copy()
tn, _, _ = oos("oos_nacional.csv", "OOS_nac",
               lambda: vc.ar4_nacional(nac_ok, "p_tasado", 4, real=True, desde=DESDE, min_train=MINTR),
               lambda: vc.ecm_v1_nacional(nac_ok, 4, var="p_tasado", real=True, desde=DESDE, min_train=MINTR),
               lambda c: bl.run_nac_model(nac_ok, c, desde=DESDE, min_train=MINTR),
               ["N1", "N2", "N3", "N4"],
               "nacional h=4 p_tasado real; N1 AR4+Δcrédito; N2 +Δhipotecas+Δcu; N3 crédito por finalidad (vivienda, consumo, otros)+Δcu; N4 parsimonioso")
print(tn.round(4).to_string(), flush=True)

# nacional en muestra (HAC 4), EXPLORATORIO
nn = nac_ok.copy()
nn["d4_p_real"] = nn["d4_ln_p_tasado"] - nn["d4_ln_deflactor"]
nn["d4_ln_hipn"] = np.log(nn["hipotecas_importe_nac"]).diff(4)
nn["d4_cu"] = nn["coste_uso_aprox"].diff(4)
nac_is = []
for id_, xs in (("NAC_IS1", ["d4_ln_credito_nuevo", "d4_cu", "d4_ln_ocupados"]), ("NAC_IS2", ["d4_ln_hipn", "d4_cu", "d4_ln_ocupados"])):
    z = nn.dropna(subset=["d4_p_real"] + xs)
    r = bl.hac_ols(z["d4_p_real"].values, z[xs].values)
    for k, v in enumerate(xs):
        nac_is.append(dict(spec=id_, var=v, coef=r.params[k + 1], se=r.bse[k + 1], p=r.pvalues[k + 1], N=int(r.nobs)))
        reg.log("NAC_IS", id_, f"d4 ln p real ~ {' + '.join(xs)} | HAC(4)", z.trimestre.min(), z.trimestre.max(), int(r.nobs), r.rsquared_adj,
                np.nan, np.nan, coef_interes=r.params[k + 1], p_interes=r.pvalues[k + 1], notas=f"var={v} EXPLORATORIO")
csv(pd.DataFrame(nac_is), "nacional_en_muestra.csv")

# ============================================================ 7. cierre
st = pd.DataFrame(signos)
csv(st, "tabla_signos.csv")
best = tp[tp.cfg == "C3"].iloc[0]   # modelo de H2 (variables del pre-registro), fijado SIN selección por RMSE
best_rmse = tp.sort_values("rmse").iloc[0]["cfg"]
(OUT / "config_h2_sellado.json").write_text(json.dumps({"cfg": "C3", "criterio": "pre-registro: AR(4) de panel + variables de H2; no se elige por RMSE (C1 era el de menor RMSE en entrenamiento: %s)" % best_rmse}))
reg.flush()

if not SMOKE:
    dsig = lambda v: t0.set_index("var").loc[v]  # noqa: E731
    cred, inter, ocu = dsig("d4_ln_hipotecas_importe"), dsig("cu_x_expo"), dsig("d4_ln_ocupados")
    signos_ok = cred["coef"] > 0 and inter["coef"] < 0
    holm_ok = max(holm_h2.values()) < 0.05
    subs = h2[h2.spec.isin(["H2_sub_hasta2013", "H2_sub_desde2014", "H2_sin_covid"])]
    sub_ok = bool(all((subs[(subs["var"] == "d4_ln_hipotecas_importe")]["coef"] > 0)) and all(subs[subs["var"] == "cu_x_expo"]["coef"] < 0))
    oos_ok = bool(best["mejora_vs_AR4"] and best["p_holm_vs_AR4"] < 0.10)
    nivel = "ASOCIACIÓN ROBUSTA" if (signos_ok and holm_ok and sub_ok and oos_ok) else "EXPLORATORIO"
    crit = dict(signos_ok=bool(signos_ok), holm_ok=bool(holm_ok), submuestras_ok=sub_ok, oos_ok=oos_ok)
    ic = {r["var"]: [r["ic95_inf"], r["ic95_sup"]] for _, r in t0.iterrows()}
    est = {r["var"]: r["coef"] for _, r in t0.iterrows()}
    pa = {k: holm_h2[k] for k in holm_h2}
    pa["d4_ln_ocupados"] = None
    vc.resultado_json(
        OUT / "resultado.json", rama="BV",
        pregunta="H2 (confirmatoria): ¿se asocia el crecimiento del precio real de compra provincial con el crédito hipotecario nuevo (+) y con el coste de uso (−, vía interacción con la exposición hipotecaria 2005-2007)? Más: periodos, arbitraje alquiler-compra, nacional y fuera de muestra.",
        datos="panel_prov_q y nacional_q_v2 (holdout.load_train), 49 provincias, 2004Q1-2024Q2; precio real = Δ4 ln p_tasado − Δ4 ln deflactor nacional (nacional_q_v2); sin muestra sellada",
        N={"H2_principal": int(t0["N"].iloc[0]), "provincias": int(t0["G"].iloc[0])},
        metodo="MCO con FE de provincia y trimestre, EE cluster provincia + wild cluster bootstrap (Webb, 9.999, WCR); Holm/BH intra-H2 (m=2) sobre crédito e interacción; el Holm de la familia de 7 confirmatorias se aplica en la síntesis BS; DM-HLN fuera de muestra (bloques h=4, embargo 4, primer test 2012Q1)",
        estimacion=est, ic95=ic, p_ajustado={"holm_m2_wcb": pa, "holm_m2_credito_l4": holm_l4},
        nivel_evidencia=nivel,
        diagnosticos={"criterios_nivel": crit, "p_wcb": fam, "p_wcb_cota": "los p=0 del bootstrap son p <= 1/(B+1) = 1e-4 (B=9.999)", "nota_simultaneidad": "el crédito es comovimiento con el precio (v1); la variante con crédito retardado 4T se reporta; asociación, no causalidad",
                      "nota_identificacion": "el nivel nacional del coste de uso queda absorbido por el FE de trimestre; solo se identifica la interacción con la exposición 2005-2007"},
        fuera_muestra={"modelo": f"BV_{best['cfg']} (panel, h=4; modelo de H2 fijado para el sellado)", "rmse": float(best["rmse"]), "dm_vs_ar4": float(best["dm_vs_AR4"]),
                       "rmse_ar4": float(best["rmse_AR4"]), "rmse_ecm_v1": float(best["rmse_ECM_v1"]), "dm_vs_ecm_v1": float(best["dm_vs_ECM_v1"]),
                       "p_holm_vs_ar4": float(best["p_holm_vs_AR4"]), "n": int(best["n"])},
        notas="Máximo posible sin muestra sellada: ASOCIACIÓN ROBUSTA; la confirmación requiere holdout.evaluate('H2') (evaluar_H2 en bv_h2_sellado.py, NO ejecutada). No residentes: sin datos provinciales (limitación). Periodos, arbitraje y nacional: EXPLORATORIO.")
    print("NIVEL", nivel, crit, flush=True)
print("OK", flush=True)
