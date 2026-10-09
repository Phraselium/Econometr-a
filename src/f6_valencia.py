"""F6 (Valencia): comparativo de precios/transacciones (N>=40, inferencia HAC) y descriptivo (N<40).

Lee solo data/processed (valencia.csv, panel_ccaa_a.csv, nacional_q.csv). Determinista, sin red.
Salidas: output/f6/*.csv|.md|.png, output/registro_busqueda_f6.csv. Uso de econ_utils sin modificarlo.
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import econ_utils as eu  # noqa: E402

warnings.filterwarnings("ignore")
np.random.seed(eu.SEED)
ROOT = eu.ROOT
OUT = ROOT / "output" / "f6"
OUT.mkdir(parents=True, exist_ok=True)
REG = eu.Registry(ROOT / "output" / "registro_busqueda_f6.csv", reset=True)
FASE = "F6"
VAL, PROV, CV, ES = "València (municipio)", "Provincia de València", "Comunitat Valenciana", "España"
TXT_DESC = "DESCRIPTIVO: N < 40 observaciones; no se hace inferencia estadística."
TXT_EST = "ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación."
FUENTE = "Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado)."


def save(df, name, nota, index=True, fl=".4g"):
    df.to_csv(OUT / f"{name}.csv", index=index, encoding="utf-8")
    (OUT / f"{name}.md").write_text(f"{nota}\n\n{eu.df_md(df, fl, index=index)}\n\n{FUENTE}\n", encoding="utf-8")


def fig_save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=130)
    plt.close(fig)


# ------------------------------------------------------------------ datos
raw = pd.read_csv(ROOT / "data" / "processed" / "valencia.csv", dtype={"periodo": str})
pa = pd.read_csv(ROOT / "data" / "processed" / "panel_ccaa_a.csv")
nq = pd.read_csv(ROOT / "data" / "processed" / "nacional_q.csv")


def serie(var, terr):
    s = raw[(raw.variable == var) & (raw.territorio == terr)].set_index("periodo")["valor"]
    if "Q" in str(s.index[0]):
        s.index = pd.PeriodIndex(s.index, freq="Q")
    else:
        s.index = s.index.astype(int)
    return s.sort_index()


# ------------------------------------------------------------------ tabla de N
rows = []
for (v, t), g in raw[~raw.territorio.str.contains("distrito")].groupby(["variable", "territorio"]):
    n = int(g["valor"].count())
    rows.append(dict(variable=v, territorio=t, frecuencia=g["frecuencia"].iloc[0][:28], n=n,
                     inicio=g.dropna(subset=["valor"]).periodo.min(), fin=g.dropna(subset=["valor"]).periodo.max(),
                     rol=g["rol"].iloc[0], validado=g["validado"].iloc[0],
                     uso="elegible (N>=40)" if n >= 40 else "descriptivo (N<40)"))
tabN = pd.DataFrame(rows)
USADAS = {("p_tasado", VAL), ("p_tasado", PROV), ("p_tasado", CV), ("p_tasado", ES), ("trans_total", VAL), ("trans_total", CV),
          ("trans_total", ES), ("trans_extranjeros", CV), ("trans_extranjeros", ES), ("ipv", CV), ("ipv", ES)}
tabN["usada_en_estimacion"] = ["sí" if (v_, t_) in USADAS else "no" for v_, t_ in zip(tabN.variable, tabN.territorio)]
save(tabN, "tabla_N_series", "Nº de observaciones por serie en valencia.csv. El umbral N>=40 decide estimación vs descriptivo "
     "(decisiones.md, F6). 'elegible' = N>=40; 'usada_en_estimacion' = entra de verdad en una regresión de este script. "
     "vut_stock_gva (N=60) es elegible pero solo se describe (registro administrativo con quiebres regulatorios).", index=False)

# ================================================================== 1. COMPARATIVO (N>=40)
P = pd.DataFrame({"València": serie("p_tasado", VAL), "Provincia": serie("p_tasado", PROV),
                  "C. Valenciana": serie("p_tasado", CV), "España": serie("p_tasado", ES)})
P = eu.common_sample(P, P.columns).loc["2005Q1":"2026Q2"]
NP = len(P)
base = P.loc["2015Q1":"2015Q4"].mean()
IDX = P / base * 100
save(IDX.round(2).assign(trimestre=IDX.index.astype(str)).set_index("trimestre"), "indices_p_tasado_base2015",
     f"{TXT_EST} Valor tasado (€/m²) índice 2015=100 (media de 2015). Muestra común 2005Q1-2026Q2, N={NP}.", fl=".2f")

fig, ax = plt.subplots(figsize=(9, 4.8))
for c in IDX:
    ax.plot(IDX.index.to_timestamp(), IDX[c], label=c, lw=2.2 if c == "València" else 1.3)
ax.axhline(100, color="grey", lw=.6)
ax.set_xlabel("Trimestre"); ax.set_ylabel("Índice, 2015 = 100")
ax.set_title("Valor tasado de la vivienda libre: València vs provincia, C. Valenciana y España")
ax.legend(); ax.text(0, -0.2, FUENTE + " Valor tasado MIVAU, €/m².", transform=ax.transAxes, fontsize=7)
fig_save(fig, "fig_indices_p_tasado")

# crecimiento acumulado
tr = [("2008-2013 (caída)", "2007Q4", "2013Q4"), ("2014-2019", "2013Q4", "2019Q4"), ("2020-2026Q2", "2019Q4", "2026Q2")]
cum = pd.DataFrame({n: (P.loc[b] / P.loc[a] - 1) * 100 for n, a, b in tr}).T
cum["dif_València_vs_España_pp"] = cum["València"] - cum["España"]
save(cum, "crecimiento_acumulado_p_tasado",
     f"{TXT_EST} Variación acumulada (%) del valor tasado entre el último trimestre previo y el final de cada tramo "
     f"(2007Q4-2013Q4, 2013Q4-2019Q4, 2019Q4-2026Q2). Es descripción de niveles, sin contraste.", fl=".1f")

# Δ4 ln
D4 = np.log(P).diff(4).dropna() * 100  # puntos log %
D4.columns = ["dV", "dProv", "dCV", "dES"]
N4 = len(D4)
reg_rows, holm_p = [], {}


def oos_rmse(df, y, x=None, start="2018Q1"):
    """RMSE de predicción a un paso (expanding) desde `start`; con x usa x_t observado (condicional)."""
    errs = []
    for t in df.index[df.index >= pd.Period(start, "Q")]:
        tr_ = df.loc[:t].iloc[:-1]
        if x is None:
            errs.append(df.loc[t, y] - tr_[y].mean())
        else:
            b = np.polyfit(tr_[x], tr_[y], 1)
            errs.append(df.loc[t, y] - (b[1] + b[0] * df.loc[t, x]))
    return float(np.sqrt(np.mean(np.square(errs))))


comps = {"Provincia": "dProv", "C. Valenciana": "dCV", "España": "dES"}
diffrows = []
for nm, c in comps.items():
    d = D4.assign(dif=D4["dV"] - D4[c])
    r = eu.ols_hac("dif ~ 1", d, 4)
    ci = r.conf_int().loc["Intercept"]
    mid = f"dif_media_{nm}"
    holm_p[mid] = float(r.pvalues["Intercept"])
    REG.log(FASE, mid, f"d4ln_pt_València - d4ln_pt_{nm} ~ 1", d.index[0], d.index[-1], int(r.nobs), r.rsquared_adj, r.aic, r.bic,
            oos_rmse(d, "dif"), r.params["Intercept"], r.pvalues["Intercept"],
            "media del diferencial (pp log); HAC4; comparación en muestra común")
    diffrows.append(dict(comparador=nm, N=int(r.nobs), media_pp=r.params["Intercept"], EE_HAC=r.bse["Intercept"],
                         IC95_inf=ci[0], IC95_sup=ci[1], p=r.pvalues["Intercept"]))
    # subperiodos: descriptivo
DIF = pd.DataFrame(diffrows)
save(DIF, "diferencial_crecimiento_media", f"{TXT_EST} Diferencial de crecimiento interanual Δ4 ln p_tasado (València menos comparador), "
     f"puntos porcentuales (100·Δ4 ln). Media con IC95 % HAC(4). N={N4} trimestres (2006Q1-2026Q2; solapamiento MA(3) por Δ4). "
     "Es una asociación/diferencia descriptiva de ritmos, sin interpretación causal.", index=False)

# diferencial por subperíodo (descriptivo)
sub = []
for n, a, b in [("2008Q1-2013Q4", "2008Q1", "2013Q4"), ("2014Q1-2019Q4", "2014Q1", "2019Q4"), ("2020Q1-2026Q2", "2020Q1", "2026Q2")]:
    z = D4.loc[a:b]
    sub.append(dict(tramo=n, N=len(z), **{f"dif_media_vs_{k}": (z["dV"] - z[c]).mean() for k, c in comps.items()}))
save(pd.DataFrame(sub), "diferencial_por_tramo", f"{TXT_DESC} Medias del diferencial Δ4 ln (pp) por tramo (N de cada fila); "
     "sin IC ni p-valores porque N<40 por tramo.", index=False)

fig, ax = plt.subplots(figsize=(9, 4.5))
for nm, c in comps.items():
    ax.plot(D4.index.to_timestamp(), D4["dV"] - D4[c], label=f"València − {nm}")
ax.axhline(0, color="k", lw=.7)
ax.set_xlabel("Trimestre"); ax.set_ylabel("Diferencial del crecimiento interanual (pp, 100·Δ4 ln)")
ax.set_title("Diferencial de crecimiento interanual del valor tasado de València")
ax.legend(); ax.text(0, -0.2, FUENTE, transform=ax.transAxes, fontsize=7)
fig_save(fig, "fig_diferencial_d4")

# betas
betarows, diagrows, chowrows, bprows = [], [], [], []


def beta_model(df, y, x, label, maxlags=4, extra=""):
    f = f"{y} ~ {x}"
    r = eu.ols_hac(f, df, maxlags)
    b = r.params[x]; ee = r.bse[x]
    p1 = float(r.t_test(f"{x} = 1").pvalue)
    ci = r.conf_int().loc[x]
    mid = f"{label}_hac{maxlags}"
    if maxlags == 4:
        holm_p[f"beta=1_{label}"] = p1
    REG.log(FASE, mid, f, df.index[0], df.index[-1], int(r.nobs), r.rsquared_adj, r.aic, r.bic, oos_rmse(df, y, x), b, p1,
            f"coef=beta; p_interes = H0 beta=1 (HAC{maxlags}); rmse_oos CONDICIONAL al x contemporáneo (no es pronóstico); {extra}")
    betarows.append(dict(modelo=label, maxlags=maxlags, N=int(r.nobs), beta=b, EE_HAC=ee, IC95_inf=ci[0], IC95_sup=ci[1],
                         p_beta0=r.pvalues[x], p_beta_igual_1=p1, R2_aj=r.rsquared_adj, const=r.params["Intercept"]))
    return r, f


for nm, c in comps.items():
    for ml in (4, 6):
        r, f = beta_model(D4, "dV", c, f"beta_València_vs_{nm}", ml)
        if ml == 4:
            dg = eu.diagnostics(r); dg["modelo"] = f"beta_València_vs_{nm}"; diagrows.append(dg)
            for fch in ("2014Q1", "2020Q1", "2022Q3"):
                ch = eu.chow(D4, f, fch); ch["modelo"] = f"beta_València_vs_{nm}"; chowrows.append(ch)
            bp = eu.bai_perron(D4["dV"], pd.DataFrame({"const": 1.0, c: D4[c]}, index=D4.index))
            bprows.append(dict(modelo=f"beta_València_vs_{nm}", n_quiebres=bp["n_bkps"], fechas=";".join(bp["fechas"])))
BET = pd.DataFrame(betarows)
save(BET, "beta_valencia_vs_comparadores", f"{TXT_EST} Regresión Δ4 ln p_tasado València (100·) sobre Δ4 ln del comparador, "
     f"N={N4}. EE HAC Newey-West con maxlags=4 (principal) y 6 (robustez; Δ4 induce MA(3)). p_beta_igual_1 contrasta H0: β=1. "
     "Asociación contemporánea, no efecto causal.", index=False)
save(pd.DataFrame(diagrows).set_index("modelo"), "diagnosticos_beta", f"{TXT_EST} Diagnósticos de los modelos beta (MCO clásico): DW, BG(4), BP, JB, RESET, CUSUM, VIF.")
save(pd.DataFrame(chowrows), "chow_beta", f"{TXT_EST} Chow en fechas candidatas (2014Q1, 2020Q1, 2022Q3).", index=False)
save(pd.DataFrame(bprows), "bai_perron_beta", f"{TXT_EST} Bai-Perron (ruptures, máx. 3 quiebres, tramo mínimo 12) sobre el modelo beta; nº por BIC.", index=False)


# ---- cambio 1: beta y diferencial de nivel por subperíodos (interacciones en la muestra completa)
TRAMOS = ["2006Q1-2013Q4", "2014Q1-2019Q4", "2020Q1-2026Q2"]


def tramo_models(df, y, x, label, maxlags=8, en_holm=True):
    d = df.copy()
    tr = np.where(d.index < pd.Period("2014Q1", "Q"), 0, np.where(d.index < pd.Period("2020Q1", "Q"), 1, 2))
    for k in range(3):
        d[f"a{k}"] = (tr == k) * 1.0
        d[f"b{k}"] = (tr == k) * d[x]
    f1 = f"{y} ~ 0 + a0 + a1 + a2 + b0 + b1 + b2"
    r = eu.ols_hac(f1, d, maxlags)
    wp = float(np.squeeze(r.wald_test("b0 = b1, b1 = b2", use_f=False).pvalue))
    d["difnivel"] = d[y] - d[x]
    f2 = "difnivel ~ 0 + a0 + a1 + a2"
    r2 = eu.ols_hac(f2, d, maxlags)
    rows_b, rows_d = [], []
    for k in range(3):
        rows_b.append(dict(modelo=label, tramo=TRAMOS[k], N_tramo=int((tr == k).sum()), beta=r.params[f"b{k}"], EE_HAC=r.bse[f"b{k}"],
                           p_beta_igual_1=float(r.t_test(f"b{k} = 1").pvalue), const=r.params[f"a{k}"], EE_const=r.bse[f"a{k}"]))
        rows_d.append(dict(modelo=label, tramo=TRAMOS[k], N_tramo=int((tr == k).sum()), dif_media_pp=r2.params[f"a{k}"], EE_HAC=r2.bse[f"a{k}"],
                           p_dif_igual_0=r2.pvalues[f"a{k}"]))
    pd2 = float(r2.pvalues["a2"])
    REG.log(FASE, f"tramos_beta_{label}", f1, d.index[0], d.index[-1], int(r.nobs), r.rsquared_adj, r.aic, r.bic, np.nan, r.params["b2"], wp,
            f"interacciones por tramo, HAC{maxlags}; p_interes = Wald H0 beta igual en los 3 tramos; N por tramo <40 (inferencia sobre N total)")
    REG.log(FASE, f"tramos_difnivel_{label}", f2, d.index[0], d.index[-1], int(r2.nobs), r2.rsquared_adj, r2.aic, r2.bic, np.nan, r2.params["a2"], pd2,
            f"diferencial medio (y-x) por tramo, HAC{maxlags}; p_interes = H0 dif 2020-26 = 0")
    if en_holm:
        holm_p[f"wald_betas_iguales_{label}"] = wp
        holm_p[f"dif_nivel_2020-26_{label}"] = pd2
    return pd.DataFrame(rows_b), pd.DataFrame(rows_d), wp


def wald_break(df, y, x, fecha, label, maxlags=8):
    d = df.copy()
    d["post"] = (d.index >= pd.Period(fecha, "Q")) * 1.0
    r = eu.ols_hac(f"{y} ~ {x}*post", d, maxlags)
    p = float(np.squeeze(r.wald_test(f"post = 0, {x}:post = 0", use_f=False).pvalue))
    return dict(modelo=label, fecha=fecha, n=int(r.nobs), dif_beta_post=r.params[f"{x}:post"], EE_dif_beta=r.bse[f"{x}:post"],
                dif_const_post=r.params["post"], EE_dif_const=r.bse["post"], p_Wald_HAC8=p)


TB, TD_, WALL, WB = [], [], {}, []
for nm, c in comps.items():
    tb, td, wp = tramo_models(D4, "dV", c, f"València_vs_{nm}")
    TB.append(tb); TD_.append(td); WALL[nm] = wp
    for fch in ("2014Q1", "2020Q1", "2022Q3"):
        WB.append(wald_break(D4, "dV", c, fch, f"València_vs_{nm}"))
TB, TD_ = pd.concat(TB), pd.concat(TD_)
save(TB, "beta_por_tramos", f"{TXT_EST} Modelo de interacciones en la muestra completa (N={N4}): Δ4 ln p_tasado València sobre Δ4 ln comparador con pendiente e "
     "intercepto propios por tramo; EE HAC(8) (Δ4 induce MA(3) y la persistencia es mayor). Cada tramo tiene N<40 (24-32 trimestres): su cifra es descriptiva dentro de un "
     "modelo con N total >= 40. 'const' es el intercepto del tramo (pp/año). Asociación, no causa. ADVERTENCIA parte-todo: València forma parte de provincia, CV y España, "
     "lo que induce un componente mecánico de co-movimiento (sobre todo frente a la provincia).", index=False)
save(TD_, "diferencial_nivel_por_tramos", f"{TXT_EST} Diferencial medio de crecimiento interanual (València menos comparador, pp, 100·Δ4 ln) con constante por tramo, N={N4}, HAC(8). "
     "El diferencial medio de toda la muestra (diferencial_crecimiento_media) promedia tramos de signo contrario y no resume bien. N por tramo <40.", index=False)
WBd = pd.DataFrame(WB)
save(WBd, "quiebres_wald_hac", f"{TXT_EST} Contraste de quiebre en fechas candidatas: Wald HAC(8) conjunto de (intercepto, pendiente) post-fecha, N={N4}. Sustituye al Chow F clásico "
     "(que supone errores no autocorrelacionados y sobrerrechaza); el Chow se conserva como complemento en chow_beta.", index=False)

# robustez: beta en Δ1 (sin solapamiento) con dummies trimestrales
D1 = np.log(P).diff().dropna() * 100
D1.columns = ["dV", "dProv", "dCV", "dES"]
for q in (2, 3, 4):
    D1[f"q{q}"] = (D1.index.quarter == q) * 1.0
d1rows = []
for nm, c in comps.items():
    f_ = f"dV ~ {c} + q2 + q3 + q4"
    r = eu.ols_hac(f_, D1, 4)
    p1 = float(r.t_test(f"{c} = 1").pvalue)
    REG.log(FASE, f"beta_d1_{nm}", f_, D1.index[0], D1.index[-1], int(r.nobs), r.rsquared_adj, r.aic, r.bic, np.nan, r.params[c], p1,
            "robustez Δ1 sin solapamiento, dummies trimestrales, HAC4; p_interes = H0 beta=1; fuera de la familia Holm")
    d1rows.append(dict(comparador=nm, N=int(r.nobs), beta=r.params[c], EE_HAC4=r.bse[c], p_beta_igual_1=p1))
D1T = pd.DataFrame(d1rows)
save(D1T, "beta_delta1_robustez", f"{TXT_EST} Robustez sin solapamiento: Δ1 ln p_tasado València sobre Δ1 ln del comparador con dummies trimestrales, HAC(4).", index=False)

# ---- cambio 2: contraste con el IPV del INE (CV vs España)
IP = pd.DataFrame({"ipv_CV": serie("ipv", CV), "ipv_ES": serie("ipv", ES), "pt_CV": P["C. Valenciana"], "pt_ES": P["España"], "pt_V": P["València"],
                   "pt_Prov": P["Provincia"]})
IP = eu.common_sample(IP, IP.columns).loc["2007Q1":"2026Q2"]
sens = []
for med in ["pt_V", "pt_Prov", "pt_CV", "pt_ES", "ipv_CV", "ipv_ES"]:
    s_ = IP[med]
    ya = s_.groupby(s_.index.year).mean()
    sens.append(dict(medida=med, **{"2019Q4->2026Q2_%": (s_["2026Q2"] / s_["2019Q4"] - 1) * 100, "2020Q1->2026Q2_%": (s_["2026Q2"] / s_["2020Q1"] - 1) * 100,
                                    "media2019->media2025_%": (ya[2025] / ya[2019] - 1) * 100}))
SENS = pd.DataFrame(sens).set_index("medida")
save(SENS, "ipv_vs_tasado_acumulado", f"{TXT_EST} Variación acumulada (%) del valor tasado (pt_*) y del IPV del INE (ipv_*) con tres bases (2019Q4, 2020Q1, medias anuales 2019->2025). "
     f"Muestra común 2007Q1-2026Q2 (N={len(IP)}). Para València solo existe valor tasado: NO hay contraste independiente para el municipio. El exceso CV-España es sobre todo del valor tasado "
     "(composición de lo tasado, mezcla nueva/usada); con el IPV la diferencia casi desaparece.", fl=".1f")
ID4 = np.log(IP[["ipv_CV", "ipv_ES", "pt_CV", "pt_ES"]]).diff(4).dropna() * 100
ipvrows, ipvt = [], []
for med, (y_, x_) in {"IPV": ("ipv_CV", "ipv_ES"), "valor_tasado": ("pt_CV", "pt_ES")}.items():
    dd_ = ID4[[y_, x_]].copy(); dd_.columns = ["dV", "dES"]
    tb, td, wp = tramo_models(dd_, "dV", "dES", f"CV_vs_España_{med}", en_holm=False)
    tb["medida"] = med; td["medida"] = med
    ipvrows.append(tb); ipvt.append(td)
IPB, IPD = pd.concat(ipvrows), pd.concat(ipvt)
save(IPB, "ipv_vs_tasado_beta_cv_es", f"{TXT_EST} Beta de Δ4 ln CV sobre Δ4 ln España por tramos, con IPV y con valor tasado, MISMA muestra (Δ4 desde 2008Q1, N={len(ID4)}), HAC(8). "
     "Primer tramo parcial (2008Q1-2013Q4). Fuera de la familia Holm (contraste de medida).", index=False)
save(IPD, "ipv_vs_tasado_difnivel_cv_es", f"{TXT_EST} Diferencial medio CV-España por tramo (pp, 100·Δ4 ln) con IPV y con valor tasado, misma muestra, HAC(8).", index=False)

# compraventas MIVAU
T = pd.DataFrame({"tot_V": serie("trans_total", VAL), "tot_CV": serie("trans_total", CV), "tot_ES": serie("trans_total", ES),
                  "ext_CV": serie("trans_extranjeros", CV), "ext_ES": serie("trans_extranjeros", ES)})
T = eu.common_sample(T, T.columns)   # 2007Q1-2026Q1
NT = len(T)
T["cuota_CV"] = T.ext_CV / T.tot_CV * 100
T["cuota_ES"] = T.ext_ES / T.tot_ES * 100
T["peso_V_en_CV"] = T.tot_V / T.tot_CV * 100
T["cuota_dif_CV_ES"] = T.cuota_CV - T.cuota_ES
rc = eu.ols_hac("cuota_dif_CV_ES ~ 1", T, 8)
rc4 = eu.ols_hac("cuota_dif_CV_ES ~ 1", T, 4); rc12 = eu.ols_hac("cuota_dif_CV_ES ~ 1", T, 12)
REG.log(FASE, "cuota_ext_dif_CV_ES", "cuota_ext_CV - cuota_ext_ES ~ 1", T.index[0], T.index[-1], int(rc.nobs), rc.rsquared_adj,
        rc.aic, rc.bic, oos_rmse(T, "cuota_dif_CV_ES"), rc.params["Intercept"], rc.pvalues["Intercept"],
        "pp; HAC8 (HAC4 y HAC12 en cuota_extranjeros_inferencia); la diferencia es muy persistente (acf1~0,9): p numérico poco fiable")
holm_p["cuota_ext_dif_CV_ES"] = float(rc.pvalues["Intercept"])
NPOS = int((T.cuota_dif_CV_ES > 0).sum()); DMIN = float(T.cuota_dif_CV_ES.min())
# tendencia lineal: series I(1) -> se reportan SIN p-valor y fuera de Holm
T["t"] = np.arange(NT) / 4.0
rt = {}
for k in ("cuota_CV", "cuota_ES"):
    r = eu.ols_hac(f"{k} ~ t", T, 4); rt[k] = r
    REG.log(FASE, f"tendencia_{k}", f"{k} ~ t(años)", T.index[0], T.index[-1], int(r.nobs), r.rsquared_adj, r.aic, r.bic,
            oos_rmse(T, k, "t"), r.params["t"], np.nan, "pp/año; DESCRIPTIVA: serie I(1), t de tendencia espurio; sin p-valor; fuera de Holm")
# beta compraventas
TD = np.log(T[["tot_V", "tot_CV", "tot_ES"]]).diff(4).dropna() * 100
TD.columns = ["tV", "tCV", "tES"]
TD["tRest"] = np.log(T.tot_CV - T.tot_V).diff(4).dropna() * 100
for c, nm in (("tCV", "C. Valenciana"), ("tES", "España"), ("tRest", "CV sin València (parte-todo)")):
    beta_model(TD, "tV", c, f"beta_compraventas_València_vs_{nm}", 4, "Δ4 ln trans_total; MIVAU")
BET2 = pd.DataFrame(betarows)
save(BET2, "beta_todos", f"{TXT_EST} Todos los modelos beta (precios y compraventas), HAC.", index=False)
anual = T[["tot_V", "tot_CV", "tot_ES", "ext_CV", "ext_ES"]].groupby(T.index.year).sum()
cnt = T.groupby(T.index.year).size()
anual = anual[cnt == 4]
anual["cuota_ext_CV_%"] = anual.ext_CV / anual.tot_CV * 100
anual["cuota_ext_ES_%"] = anual.ext_ES / anual.tot_ES * 100
anual["peso_València_en_CV_%"] = anual.tot_V / anual.tot_CV * 100
anual.index.name = "anio"
save(anual, "compraventas_cuota_extranjeros", f"{TXT_EST} Compraventas MIVAU (trans_total, trans_extranjeros), sumas de años completos; "
     f"muestra común trimestral 2007Q1-2026Q1 (N={NT}). La serie MIVAU NO tiene trans_extranjeros para el municipio de València: "
     "la cuota de extranjeros solo existe para la C. Valenciana y España (València municipio: solo Notariado, ver descriptivo).", fl=".2f")
save(pd.DataFrame({"concepto": ["media cuota CV - ES (pp)", "EE HAC4", "EE HAC8", "EE HAC12", "p (HAC8; poco fiable)", "trimestres con CV > ES", "N", "mínimo diferencia (pp)",
                                "pendiente lineal cuota CV (pp/año; sin p-valor)", "pendiente lineal cuota ES (pp/año; sin p-valor)"],
                   "valor": [rc.params["Intercept"], rc4.bse["Intercept"], rc.bse["Intercept"], rc12.bse["Intercept"], rc.pvalues["Intercept"], NPOS, NT, DMIN,
                             rt["cuota_CV"].params["t"], rt["cuota_ES"].params["t"]]}),
     "cuota_extranjeros_inferencia", f"{TXT_EST} N={NT}. Hecho descriptivo: la cuota de la CV supera a la de España en {NPOS}/{NT} trimestres. La diferencia es persistente (acf1~0,9) y el EE crece con los retardos HAC; "
     "las pendientes lineales se reportan SIN p-valor porque las cuotas son I(1) (t de tendencia espurio). AVISO: trans_extranjeros tiene un salto de cobertura entre 2008 y 2009 (decisiones.md, F3).",
     index=False)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
ax[0].plot(T.index.to_timestamp(), T.cuota_CV, label="C. Valenciana"); ax[0].plot(T.index.to_timestamp(), T.cuota_ES, label="España")
ax[0].set_xlabel("Trimestre"); ax[0].set_ylabel("% compraventas con comprador extranjero"); ax[0].set_title("Cuota de extranjeros (MIVAU)"); ax[0].legend()
ax[1].plot(T.index.to_timestamp(), T.peso_V_en_CV); ax[1].set_xlabel("Trimestre"); ax[1].set_ylabel("% de compraventas de la C. Valenciana")
ax[1].set_title("Peso de València municipio en compraventas CV")
fig.text(0.01, 0.005, FUENTE + " Compraventas MIVAU (Registradores/Notariado).", fontsize=7)
fig_save(fig, "fig_cuota_extranjeros_compraventas")

# ================================================================== 2. DESCRIPTIVO (N<40)
# padrón
pad = pd.DataFrame({k: serie(v, VAL) for k, v in {"pob_total_dpop": "pob_total", "espanoles": "pob_espanola", "extranjeros": "pob_extranjera",
                    "africa": "pob_vlc_africa", "america": "pob_vlc_america", "asia": "pob_vlc_asia", "europa": "pob_vlc_europa",
                    "alemania(en Europa)": "pob_vlc_alemania", "reino_unido(en Europa)": "pob_vlc_reino_unido"}.items()})
pad["total_esp+ext"] = pad.espanoles + pad.extranjeros
pad["pct_extranjeros"] = pad.extranjeros / pad["total_esp+ext"] * 100
pad["otros_no_clasif(ext-continentes)"] = pad.extranjeros - pad[["africa", "america", "asia", "europa"]].sum(axis=1)
pad.index.name = "anio"
Npad = int(pad.extranjeros.count())
save(pad, "padron_valencia_nacionalidad", f"{TXT_DESC} Padrón de València ciudad a 1 de enero. Nacionalidad 1998-2022 (N={Npad}); población "
     f"total DPOP 1996-2025 (N={int(pad.pob_total_dpop.count())}, la columna total_esp+ext solo 1998-2022). Continentes: América, Europa, África, Asia; "
     "Alemania y Reino Unido son subconjuntos de Europa; Oceanía/apátridas caen en 'otros'. Las nacionalidades pueden cambiar por nacionalizaciones.",
     fl=".1f")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
ax[0].plot(pad.index, pad.pct_extranjeros, marker="o", ms=3); ax[0].set_xlabel("Año (1 de enero)"); ax[0].set_ylabel("% población extranjera sobre total")
ax[0].set_title("València: % de población extranjera (padrón)")
for c in ["africa", "america", "asia", "europa"]:
    ax[1].plot(pad.index, pad[c] / 1000, label=c.capitalize())
ax[1].set_xlabel("Año (1 de enero)"); ax[1].set_ylabel("Miles de personas"); ax[1].set_title("Extranjeros por continente"); ax[1].legend()
fig.text(0.01, 0.005, FUENTE + " Padrón INE.", fontsize=7)
fig_save(fig, "fig_padron_valencia")

# alquiler
alq = pd.DataFrame({"serpavi_val_mediana": serie("serpavi_vc_mediana", VAL), "serpavi_val_dist_ponderada": serie("serpavi_vc_dist_agg", VAL),
                    "ipva_val": serie("ipva", VAL)})
cvr = pa[pa.ccaa == CV].set_index("anio")
alq["serpavi_cv_mediana"] = cvr["serpavi_vc_mediana"]
nqa = nq.assign(anio=nq.trimestre.str[:4].astype(int)).groupby("anio")["serpavi_esp_constante"].mean()
alq["serpavi_esp_constante"] = nqa
alq = alq.loc[2011:2024]
pt_anual = P.groupby(P.index.year).mean()
alq["p_tasado_val"] = pt_anual["València"]; alq["p_tasado_cv"] = pt_anual["C. Valenciana"]; alq["p_tasado_esp"] = pt_anual["España"]
alq["rent_bruta_val_%"] = 12 * alq.serpavi_val_mediana / alq.p_tasado_val * 100
alq["rent_bruta_cv_%"] = 12 * alq.serpavi_cv_mediana / alq.p_tasado_cv * 100
alq["rent_bruta_esp_%"] = 12 * alq.serpavi_esp_constante / alq.p_tasado_esp * 100
alq["crec_alq_val_%"] = alq.serpavi_val_mediana.pct_change() * 100
alq["crec_p_val_%"] = alq.p_tasado_val.pct_change() * 100
alq.index.name = "anio"
save(alq, "alquiler_serpavi_vs_precio", f"{TXT_DESC} N=14 años (2011-2024). Mediana SERPAVI del alquiler (€/m²/mes, stock de contratos declarados en IRPF) "
     "frente al valor tasado medio anual (€/m², MIVAU). ADVERTENCIA: rentabilidad bruta aproximada = 12·alquiler/precio; mezcla fuentes (AEAT vs tasaciones), "
     "conceptos (mediana de contratos vigentes vs media de valor tasado) y no descuenta vacíos ni costes; solo ilustra la evolución. serpavi_esp_constante: "
     "agregado propio de composición constante (robustez). Matices: SERPAVI es el stock de contratos vigentes (va por detrás de la renta de mercado, la infravalora en fases alcistas); "
     "la superficie de SERPAVI y la de la tasación pueden no coincidir (no verificado); lo informativo es la trayectoria (pico y caída), no los extremos.", fl=".2f")
base_a = alq.loc[2015]
idx_a = pd.DataFrame({"Alquiler València": alq.serpavi_val_mediana / base_a.serpavi_val_mediana * 100,
                      "Alquiler C. Valenciana": alq.serpavi_cv_mediana / base_a.serpavi_cv_mediana * 100,
                      "Valor tasado València": alq.p_tasado_val / base_a.p_tasado_val * 100,
                      "Valor tasado España": alq.p_tasado_esp / base_a.p_tasado_esp * 100})
save(idx_a, "alquiler_precio_indices_2015", f"{TXT_DESC} N=14. Índices 2015=100 (alquiler SERPAVI y valor tasado anual medio).", fl=".1f")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
for c in idx_a:
    ax[0].plot(idx_a.index, idx_a[c], label=c)
ax[0].set_xlabel("Año"); ax[0].set_ylabel("Índice, 2015 = 100"); ax[0].set_title("Alquiler (SERPAVI) y precio (tasado)"); ax[0].legend(fontsize=7)
ax[1].plot(alq.index, alq["rent_bruta_val_%"], label="València"); ax[1].plot(alq.index, alq["rent_bruta_cv_%"], label="C. Valenciana")
ax[1].plot(alq.index, alq["rent_bruta_esp_%"], label="España (aprox.)", ls="--")
ax[1].set_xlabel("Año"); ax[1].set_ylabel("12·alquiler/precio (%)"); ax[1].set_title("Rentabilidad bruta aproximada (mezcla fuentes)"); ax[1].legend(fontsize=7)
fig.text(0.01, 0.005, FUENTE, fontsize=7)
fig_save(fig, "fig_alquiler_precio")

# VUT
vs = {k: serie("vut_stock_gva", t) for k, t in {"València": VAL, "Provincia": PROV, "C. Valenciana": CV}.items()}
vut = pd.DataFrame({k: s[s.index.quarter == 4].groupby(lambda p: p.year).last() for k, s in vs.items()})
pcv = pa[pa.ccaa == CV].set_index("anio")["pob_total"]
pv = serie("pob_total", VAL)
vut["pob_València"] = pv; vut["pob_CV"] = pcv
vut["VUT_por_1000hab_València"] = vut["València"] / vut.pob_València * 1000
vut["VUT_por_1000hab_CV"] = vut["C. Valenciana"] / vut.pob_CV * 1000
vut["peso_València_en_CV_%"] = vut["València"] / vut["C. Valenciana"] * 100
vut = vut.loc[2010:2024]
vut.index.name = "anio"
save(vut, "vut_gva_stock", f"{TXT_DESC} Viviendas de uso turístico REGISTRADAS (GVA, stock reconstruido a diciembre) 2010-2024, N={len(vut)} años (60 trimestres en la "
     "serie original, pero con quiebres regulatorios 2016-2019 y 2021 y registros dados de baja: no se trata como mercado ni se usa en inferencia). No encadenar con la lista vigente de 2026. "
     "Población al 1 de enero del mismo año (DPOP València; CV de panel_ccaa_a).", fl=".1f")
ine = pd.DataFrame({"viv_tur_València": serie("vut_viviendas_turisticas", VAL), "viv_tur_Provincia": serie("vut_viviendas_turisticas", PROV),
                    "plazas_València": serie("vut_plazas", VAL), "plazas_Provincia": serie("vut_plazas", PROV),
                    "pct_sobre_total_València": serie("vut_pct_sobre_total", VAL), "pct_sobre_total_Provincia": serie("vut_pct_sobre_total", PROV)})
ine["peso_València_en_Provincia_%"] = ine.viv_tur_València / ine.viv_tur_Provincia * 100
ine.index = ine.index.astype(str)
save(ine, "vut_ine_municipio_provincia", f"{TXT_DESC} VUT INE experimental, N={len(ine)} cortes semestrales de calendario irregular (feb/ago -> T1/T3 hasta 2024-08; "
     "may/nov desde 2024-11; además 2024Q4). Estas cifras NO son comparables en niveles con el registro GVA (ratio INE/GVA inestable, 0,57-0,71 en la CV).", fl=".2f")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
ax[0].plot(vut.index, vut["VUT_por_1000hab_València"], label="València"); ax[0].plot(vut.index, vut["VUT_por_1000hab_CV"], label="C. Valenciana")
ax[0].set_xlabel("Año (diciembre)"); ax[0].set_ylabel("VUT registradas por 1.000 habitantes"); ax[0].set_title("VUT GVA por 1.000 hab."); ax[0].legend()
ax[1].plot(range(len(ine)), ine.viv_tur_València, marker="o", label="València municipio"); ax[1].plot(range(len(ine)), ine.viv_tur_Provincia, marker="o", label="Provincia")
ax[1].set_xticks(range(len(ine))); ax[1].set_xticklabels(ine.index, rotation=60, fontsize=7)
ax[1].set_xlabel("Corte semestral (calendario irregular)"); ax[1].set_ylabel("Viviendas turísticas (INE)"); ax[1].set_title("VUT INE experimental"); ax[1].legend()
fig.text(0.01, 0.005, FUENTE, fontsize=7)
fig_save(fig, "fig_vut")

# Notariado
nv = serie("notariado_viv_extranj", VAL)
ne = serie("notariado_viv_ext_prov", PROV); ns = serie("notariado_viv_esp_prov", PROV)
nprov = pd.DataFrame({"viv_ext": ne, "viv_esp": ns})
nprov["pct_ext"] = nprov.viv_ext / (nprov.viv_ext + nprov.viv_esp) * 100
nprov["cuantia_media_ext"] = serie("notariado_cuantia_ext_prov", PROV)
nprov["cuantia_media_esp"] = serie("notariado_cuantia_esp_prov", PROV)
nprov.index = nprov.index.astype(str)
save(nprov, "notariado_provincia_trimestral", f"{TXT_DESC} Notariado, provincia de València, 2018T1-2025T4, N={len(nprov)} trimestres (<40). Robustez. "
     "Cuenta viviendas con al menos un comprador extranjero (el 4T2025 con remisión IUI del 99,9 %). No mezclar niveles con MIVAU (ratio 1,06-1,20).", fl=".1f")
na = nprov.copy(); na["anio"] = [int(i[:4]) for i in na.index]
ya = na.groupby("anio")[["viv_ext", "viv_esp"]].sum()
ya["pct_ext"] = ya.viv_ext / (ya.viv_ext + ya.viv_esp) * 100
ya["Valencia_municipio_total_general_ext"] = nv
ya["municipio/provincia_ext_%"] = ya.Valencia_municipio_total_general_ext / ya.viv_ext * 100
save(ya, "notariado_municipio_vs_provincia", f"{TXT_DESC} Notariado, compras de extranjeros: València municipio 'Total general' (edición 4T de cada año, N={int(nv.count())} años, 2021-2025) "
     "frente a la suma anual de la provincia (N=8 años). Solo robustez: el municipal solo existe como 'Total general' y la comparación de conceptos "
     "(acumulado hasta 4T de la edición vs suma de trimestres) no está validada.", fl=".1f")
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.plot(range(len(nprov)), nprov.pct_ext, marker="o", ms=3)
ax.set_xticks(range(0, len(nprov), 4)); ax.set_xticklabels(nprov.index[::4], rotation=45)
ax.set_xlabel("Trimestre"); ax.set_ylabel("% viviendas vendidas con comprador extranjero"); ax.set_title("Notariado, provincia de València")
ax.text(0, -0.3, FUENTE, transform=ax.transAxes, fontsize=7)
fig_save(fig, "fig_notariado_provincia")

# correlaciones (solo descripción)
A = pd.DataFrame({"pct_extranj_padron": pad.pct_extranjeros, "ln_extranj": np.log(pad.extranjeros), "ln_pob_total": np.log(pad.pob_total_dpop)})
A["ln_p_tasado_val"] = np.log(pt_anual["València"])
A["ln_alquiler_val"] = np.log(alq.serpavi_val_mediana)
A["ln_vut_val"] = np.log(vut["València"])
dA = A.drop(columns=["pct_extranj_padron"]).diff()
dA.columns = ["d" + c for c in dA.columns]
dA["d_pct_extranj"] = A.pct_extranj_padron.diff()
pairs = [("ln_extranj", "ln_p_tasado_val"), ("ln_alquiler_val", "ln_p_tasado_val"), ("ln_vut_val", "ln_p_tasado_val"), ("ln_vut_val", "ln_alquiler_val"),
         ("ln_extranj", "ln_alquiler_val")]
cr = []
for x, y in pairs:
    z = A[[x, y]].dropna()
    zd = dA[["d" + x, "d" + y]].dropna()
    cr.append(dict(x=x, y=y, N_niveles=len(z), corr_niveles=z.corr().iloc[0, 1], N_difs=len(zd), corr_difs=zd.corr().iloc[0, 1]))
save(pd.DataFrame(cr), "correlaciones_anuales", f"{TXT_DESC} Correlaciones de Pearson entre series anuales de València, SIN p-valores: con N de 8-23 años y series "
     "con tendencia, las correlaciones en niveles son espurias en gran medida (tendencia común); las de primeras diferencias de ln son más informativas, pero siguen siendo "
     "descriptivas. No implican causalidad.", index=False)

# SERPAVI por distrito (descriptivo; el raw no trae nombres: se usa el código 4625NNN)
dd = raw[raw.variable == "serpavi_dist_vc_mediana"].copy()
dd["distrito"] = dd.territorio.str.extract(r"(\d{7})")[0]
W = dd.pivot(index="periodo", columns="distrito", values="valor")
W.index = W.index.astype(int)
nc = raw[raw.variable == "serpavi_dist_vc_n_contratos"].copy()
nc["distrito"] = nc.territorio.str.extract(r"(\d{7})")[0]
NC = nc.pivot(index="periodo", columns="distrito", values="valor"); NC.index = NC.index.astype(int)
rk = pd.DataFrame({"mediana_VC_2024": W.loc[2024], "mediana_VC_2015": W.loc[2015], "n_contratos_2024": NC.loc[2024]})
rk["crec_2015_2024_%"] = (rk.mediana_VC_2024 / rk.mediana_VC_2015 - 1) * 100
rk["ranking_2024"] = rk.mediana_VC_2024.rank(ascending=False, method="min")
rk["ranking_crecimiento"] = rk["crec_2015_2024_%"].rank(ascending=False, method="min")
rk = rk.sort_values("ranking_2024"); rk.index.name = "distrito_cod"
save(rk, "serpavi_distritos_ranking", f"{TXT_DESC} SERPAVI alquiler (mediana VC, €/m²/mes) por distrito de València, N=14 años (2011-2024), 19 distritos. "
     "El origen no trae nombres de distrito: se identifican por código 4625NNN. Distritos con pocos contratos (mín. 10 viviendas) son ruidosos.", fl=".2f")
cvd = pd.DataFrame({"media": W.mean(axis=1), "sd": W.std(axis=1), "n_distritos": W.count(axis=1)})
cvd["coef_variacion"] = cvd.sd / cvd.media
cvd["max/min"] = W.max(axis=1) / W.min(axis=1)
cvd.index.name = "anio"
save(cvd, "serpavi_distritos_dispersion", f"{TXT_DESC} Dispersión entre distritos por año (media simple de medianas, desviación típica, coeficiente de variación). N=14 años.", fl=".3f")
fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
o = rk.sort_values("mediana_VC_2024")
ax[0].barh(o.index, o.mediana_VC_2024); ax[0].set_xlabel("Mediana alquiler VC 2024 (€/m²/mes)"); ax[0].set_ylabel("Distrito (código 4625NNN)")
ax[0].set_title("Ranking por distrito, 2024"); ax[0].tick_params(axis="y", labelsize=6)
ax[1].plot(cvd.index, cvd.coef_variacion, marker="o"); ax[1].set_xlabel("Año"); ax[1].set_ylabel("Coeficiente de variación entre distritos")
ax[1].set_title("Dispersión del alquiler entre distritos")
fig.text(0.01, 0.005, FUENTE + " SERPAVI por distrito (descriptivo, N=14).", fontsize=7)
fig_save(fig, "fig_serpavi_distritos")

# ================================================================== registro y resumen
Hl = eu.holm(holm_p)
hol = pd.DataFrame({"p_bruto": pd.Series(holm_p), "p_Holm": pd.Series(Hl)}).sort_values("p_bruto")
hol["p_Bonferroni"] = (hol.p_bruto * len(hol)).clip(upper=1)
save(hol, "correccion_holm", f"{TXT_EST} Corrección por búsqueda sobre la familia de {len(hol)} contrastes de interés (diferenciales medios, β=1, "
     "diferencia de cuota, Wald de igualdad de betas, diferencial de nivel 2020-26; las tendencias lineales de las cuotas (I(1)) quedan fuera) registrados en output/registro_busqueda_f6.csv.", fl=".4g")
reg = REG.read()
NREG = len(reg)

f = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
b = BET.set_index(["modelo", "maxlags"])
dgt = pd.DataFrame(diagrows).set_index("modelo")
fallos = []
for m, r in dgt.iterrows():
    for k in ("BG4_p", "BP_p", "JB_p", "RESET_p", "CUSUM_p"):
        if r[k] < 0.05:
            fallos.append(f"{m}:{k}={r[k]:.3f}")
chw = pd.DataFrame(chowrows)
chfail = [f"{r.modelo}@{r.fecha}(p={r.p_Wald_HAC8:.3f})" for r in WBd.itertuples() if r.p_Wald_HAC8 < 0.05]
tbs = TB.set_index(["modelo", "tramo"]); tds = TD_.set_index(["modelo", "tramo"])
def tr_txt(nm):
    m_ = f"València_vs_{nm}"
    return "; ".join(f"{t_[:4]}-{t_[7:11]}: β={f(tbs.loc[(m_,t_),'beta'])} (EE {f(tbs.loc[(m_,t_),'EE_HAC'])})" for t_ in TRAMOS)
def td_txt(nm):
    m_ = f"València_vs_{nm}"
    return "; ".join(f"{t_[:4]}-{t_[7:11]}: {f(tds.loc[(m_,t_),'dif_media_pp'],1)} (EE {f(tds.loc[(m_,t_),'EE_HAC'],1)})" for t_ in TRAMOS)
ipvs = SENS.round(1)
ipb = IPB.set_index(["medida", "tramo"]); ipd = IPD.set_index(["medida", "tramo"])
rb = alq["rent_bruta_val_%"]
nmax = nprov.pct_ext.max(); nmax_q = nprov.pct_ext.idxmax()
dif_txt = "; ".join(f"vs {r.comparador}: {f(r.media_pp)} pp (IC95 % {f(r.IC95_inf)} a {f(r.IC95_sup)}; EE HAC {f(r.EE_HAC)}; p={f(r.p,3)})" for r in DIF.itertuples())
bt_txt = "; ".join(f"vs {nm}: β={f(b.loc[(f'beta_València_vs_{nm}',4),'beta'])} (EE HAC {f(b.loc[(f'beta_València_vs_{nm}',4),'EE_HAC'])}; p(β=1)={f(b.loc[(f'beta_València_vs_{nm}',4),'p_beta_igual_1'],3)})" for nm in comps)
cu = cum.round(1)
md = f"""# Resumen F6: València (precios, alquiler, población extranjera, VUT)

Todo lo que sigue es **asociación** o descripción; no hay identificación causal en esta fase. Reproducible con `python3 src/f6_valencia.py`.

## A. Estimación (N >= 40 trimestres; HAC Newey-West, maxlags=4 salvo indicación)

Muestra común precios: 2005Q1-2026Q2 (N={NP} niveles; N={N4} en Δ4). Compraventas: 2007Q1-2026Q1 (N={NT}).

- **Índices 2015=100 y crecimiento acumulado (%) del valor tasado** (`crecimiento_acumulado_p_tasado.md`):
  2008-2013: València {cu.loc['2008-2013 (caída)','València']}, provincia {cu.loc['2008-2013 (caída)','Provincia']}, CV {cu.loc['2008-2013 (caída)','C. Valenciana']}, España {cu.loc['2008-2013 (caída)','España']};
  2014-2019: València {cu.loc['2014-2019','València']}, provincia {cu.loc['2014-2019','Provincia']}, CV {cu.loc['2014-2019','C. Valenciana']}, España {cu.loc['2014-2019','España']};
  2020-2026Q2: València {cu.loc['2020-2026Q2','València']}, provincia {cu.loc['2020-2026Q2','Provincia']}, CV {cu.loc['2020-2026Q2','C. Valenciana']}, España {cu.loc['2020-2026Q2','España']}.
- **Sensibilidad a la base (variación acumulada %, `ipv_vs_tasado_acumulado.md`)**: 2019Q4->2026Q2 València {f(ipvs.loc['pt_V','2019Q4->2026Q2_%'],1)}, CV {f(ipvs.loc['pt_CV','2019Q4->2026Q2_%'],1)}, España {f(ipvs.loc['pt_ES','2019Q4->2026Q2_%'],1)} (valor tasado); con base 2020Q1 València {f(ipvs.loc['pt_V','2020Q1->2026Q2_%'],1)}; medias anuales 2019->2025 València {f(ipvs.loc['pt_V','media2019->media2025_%'],1)}, España {f(ipvs.loc['pt_ES','media2019->media2025_%'],1)}. El orden se mantiene.
- **Contraste con el IPV del INE (CV frente a España)**: 2019Q4->2026Q2 el IPV da CV {f(ipvs.loc['ipv_CV','2019Q4->2026Q2_%'],1)} % frente a España {f(ipvs.loc['ipv_ES','2019Q4->2026Q2_%'],1)} % (diferencia {f(ipvs.loc['ipv_CV','2019Q4->2026Q2_%']-ipvs.loc['ipv_ES','2019Q4->2026Q2_%'],1)} pp), mientras que con valor tasado es {f(ipvs.loc['pt_CV','2019Q4->2026Q2_%'],1)} % frente a {f(ipvs.loc['pt_ES','2019Q4->2026Q2_%'],1)} % ({f(ipvs.loc['pt_CV','2019Q4->2026Q2_%']-ipvs.loc['pt_ES','2019Q4->2026Q2_%'],1)} pp). El exceso CV-España es sobre todo del valor tasado (composición de lo tasado). Diferencial medio CV-España 2020-26 (Δ4, pp): IPV {f(ipd.loc[('IPV',TRAMOS[2]),'dif_media_pp'],1)} (EE {f(ipd.loc[('IPV',TRAMOS[2]),'EE_HAC'],1)}) frente a valor tasado {f(ipd.loc[('valor_tasado',TRAMOS[2]),'dif_media_pp'],1)} (EE {f(ipd.loc[('valor_tasado',TRAMOS[2]),'EE_HAC'],1)}). **Para el municipio de València no hay un contraste independiente** (solo valor tasado), así que el +100 % puede reflejar en parte composición de tasaciones.
- **Beta de Δ4 ln p_tasado València (muestra completa, HAC4)**: {bt_txt}. Esta beta es un **promedio inestable** (CUSUM, Wald de quiebre, Bai-Perron). Robusta a Δ1 sin solapamiento (`beta_delta1_robustez.md`): {'; '.join(f"{r.comparador} β={f(r.beta)} (EE {f(r.EE_HAC4)})" for r in D1T.itertuples())}.
- **Beta por tramos (interacciones, N={N4}, HAC8; `beta_por_tramos.md`; cada tramo N<40, descriptivo dentro del modelo)**: vs España {tr_txt('España')}; vs CV {tr_txt('C. Valenciana')}; vs provincia {tr_txt('Provincia')}. Wald de igualdad de betas entre tramos: España p={f(WALL['España'],3)}, CV p={f(WALL['C. Valenciana'],3)}, provincia p={f(WALL['Provincia'],3)}.
- **Diferencial medio de crecimiento por tramo (pp/año, `diferencial_nivel_por_tramos.md`, HAC8)**: vs España {td_txt('España')}; vs CV {td_txt('C. Valenciana')}. El diferencial medio de toda la muestra ({dif_txt}) **promedia tramos de signo contrario y no resume bien**; no se presenta como resultado.
- **Conclusión de precios**: la beta de la muestra completa (>1) no es un parámetro estable. Desde 2020 el mayor crecimiento de València respecto a la CV y España se asocia con un **diferencial de nivel** (constante positiva del tramo) más que con una mayor sensibilidad (amplificación) al ciclo: ver las betas del último tramo. Es una asociación y, al ser València parte de provincia, CV y España, hay un componente mecánico parte-todo.
- **Compraventas MIVAU**: cuota de extranjeros CV (media {f(T.cuota_CV.mean(),1)} %) frente a España ({f(T.cuota_ES.mean(),1)} %). Hecho descriptivo: la cuota CV supera a la de España en **{NPOS}/{NT} trimestres** (mínimo {f(DMIN)} pp; diferencia media {f(rc.params['Intercept'])} pp, EE HAC4 {f(rc4.bse['Intercept'])}, HAC8 {f(rc.bse['Intercept'])}, HAC12 {f(rc12.bse['Intercept'])}; la diferencia es muy persistente y el p-valor numérico no es fiable). Pendientes lineales descriptivas (series I(1), sin p-valor): CV {f(rt['cuota_CV'].params['t'])} y España {f(rt['cuota_ES'].params['t'])} pp/año. Aviso: salto de cobertura de `trans_extranjeros` entre 2008 y 2009. La serie MIVAU de extranjeros **no existe a nivel de municipio**.
- **Diagnósticos que fallan (p<0,05)** en los modelos beta (Δ4): {', '.join(fallos) if fallos else 'ninguno'}. Quiebres con Wald HAC(8) significativos (sustituye al Chow clásico, que sobrerrechaza con residuos autocorrelacionados; `quiebres_wald_hac.md`): {', '.join(chfail) if chfail else 'ninguno'}. Bai-Perron (BIC, sin corregir autocorrelación, tiende a sobreestimar el nº de quiebres): {'; '.join(f"{r['modelo']}: {r['n_quiebres']} ({r['fechas']})" for r in bprows)}.
- **Búsqueda**: {NREG} modelos registrados en `output/registro_busqueda_f6.csv`; corrección Holm/Bonferroni sobre {len(hol)} contrastes en `correccion_holm.md`. Con Holm, contrastes con p_Holm<0,05: {', '.join(hol[hol.p_Holm<0.05].index) or 'ninguno'}.

## B. Descriptivo (N insuficiente, N < 40; **sin inferencia**)

- **Padrón** (1998-2022, N={Npad}; DPOP 1996-2025): extranjeros {f(pad.pct_extranjeros.dropna().iloc[0],1)} % en 1998, máximo {f(pad.pct_extranjeros.max(),1)} % en {int(pad.pct_extranjeros.idxmax())}, {f(pad.pct_extranjeros.dropna().iloc[-1],1)} % en 2022 (`padron_valencia_nacionalidad.md`).
- **Alquiler SERPAVI València** (2011-2024, N=14): mediana {f(alq.serpavi_val_mediana.iloc[0])} a {f(alq.serpavi_val_mediana.iloc[-1])} €/m²/mes; índice 2015=100 a 2024: València {f(idx_a['Alquiler València'].iloc[-1],0)}, CV {f(idx_a['Alquiler C. Valenciana'].iloc[-1],0)}, valor tasado València {f(idx_a['Valor tasado València'].iloc[-1],0)}. Rentabilidad bruta aproximada València: {f(rb.iloc[0],1)} % (2011), **pico {f(rb.max(),1)} % en {int(rb.idxmax())}**, {f(rb.loc[2020],1)} % (2020) y {f(rb.iloc[-1],1)} % (2024): caída desde 2020 porque el valor tasado sube más que la renta SERPAVI. Advertencias: mezcla fuentes y conceptos; SERPAVI es stock de contratos vigentes (retrasa la renta de mercado); la superficie de SERPAVI y la de la tasación pueden no coincidir (no verificado).
- **VUT GVA** (registradas, 2010-2024, N=15 años): València {int(vut['València'].iloc[0])} a {int(vut['València'].iloc[-1])}; por 1.000 hab. {f(vut['VUT_por_1000hab_València'].iloc[-1],1)} frente a {f(vut['VUT_por_1000hab_CV'].iloc[-1],1)} en la CV (2024). VUT INE: N=13 cortes irregulares, no comparable en niveles con GVA.
- **SERPAVI por distrito** (19 distritos, N=14 años): mayor mediana 2024 {rk.index[0]} ({f(rk.mediana_VC_2024.iloc[0])} €/m²), menor {rk.index[-1]} ({f(rk.mediana_VC_2024.iloc[-1])}); crecimiento 2015-2024 entre {f(rk['crec_2015_2024_%'].min(),0)} % y {f(rk['crec_2015_2024_%'].max(),0)} %; coeficiente de variación {f(cvd.coef_variacion.iloc[0],3)} (2011) a {f(cvd.coef_variacion.iloc[-1],3)} (2024) (`serpavi_distritos_*.md`; por código).
- **Notariado (robustez)**: municipio 'Total general' 2021-2025 (N=5); provincia trimestral 2018-2025 (N=32), % con comprador extranjero {f(nprov.pct_ext.iloc[0],1)} % (2018T1), máximo {f(nmax,1)} % ({nmax_q}), {f(nprov.pct_ext.iloc[-1],1)} % (2025T4).
- **Correlaciones anuales** (`correlaciones_anuales.md`): solo descripción, sin p-valores.

### Tabla de N por serie
Ver `tabla_N_series.md` (todas las series de `valencia.csv`).

{eu.df_md(tabN[['variable','territorio','n','inicio','fin','uso','usada_en_estimacion']], index=False)}

## Problemas abiertos
- Distritos SERPAVI: el origen no trae nombres, solo código 4625NNN; mediana por distrito ruidosa (mín. 10 viviendas).
- Trans_extranjeros no existe para València municipio en MIVAU.
- El valor tasado municipal es de tasaciones (composición cambiante de inmuebles tasados); el padrón por nacionalidad acaba en 2022 (no hay 2023-2025 por municipio).
- Δ4 solapa: EE HAC(4) en la beta completa, HAC(8) en tramos y quiebres; el EE del diferencial medio crece con los retardos.
- Contradicción documental pendiente: `fuentes_fallidas.md` dice que la nacionalidad 2023-2025 no está publicada a nivel municipal, mientras `docs/fallidas/ine_ccaa.md` anota que la tabla 79544 es municipal desde 2021 (no se ha resuelto aquí).
- `rmse_oos` del registro en las betas es condicional al x contemporáneo (no es pronóstico).
- La VUT GVA es un registro con quiebres regulatorios; la serie 2026 no se encadena.

## Qué NO se puede afirmar
- Que las viviendas turísticas o la inmigración/compradores extranjeros **causen** variaciones del precio o del alquiler en València: solo hay N<40 anual, sin instrumento ni variación cruzada municipal.
- Que la rentabilidad bruta aproximada sea la rentabilidad real de un inversor (mezcla fuentes).
- Que las correlaciones anuales sean relaciones estables; que los niveles INE y GVA de VUT sean comparables.
- Que la cuota de extranjeros de la CV (MIVAU) sea la de València ciudad, ni que el Notariado municipal sea comparable en niveles con MIVAU.
"""
(OUT / "resumen_f6.md").write_text(md, encoding="utf-8")
print(f"F6 OK: {NREG} modelos registrados; salidas en {OUT}")
