"""F4 (oferta, P3): déficit acumulado de vivienda 2021-2025, elasticidad de la oferta (DOLS, ECM, IV),
contraste con el Banco de España y panel CCAA (robustez). Determinista (semilla 20261009), sin red.
Lee data/processed (y data/raw/mivau_parque.csv, solo lectura). Escribe output/f4/ y
output/registro_busqueda_f4.csv.
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
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.ardl import UECM, ardl_select_order
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen, select_order

sys.path.insert(0, str(Path(__file__).resolve().parent))
from econ_utils import (ROOT, SEED, Registry, bai_perron, chow, common_sample, df_md,  # noqa: E402
                        diagnostics, dols, holm, load_nacional, ols_hac)

warnings.filterwarnings("ignore")
np.random.seed(SEED)
T0 = time.time()
OUT = ROOT / "output" / "f4"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(ROOT / "output" / "registro_busqueda_f4.csv", reset=True)
Pd = pd.Period
MD = []
BDE_EL = 0.45


def save(df, name, floatfmt=".4g", index=True):
    df.to_csv(OUT / f"{name}.csv", index=index)
    (OUT / f"{name}.md").write_text(df_md(df, floatfmt, index) + "\n")


def tm(df, floatfmt=".4g", index=True):
    return df_md(df, floatfmt, index) + "\n"


def sec(title, text=""):
    MD.append(f"\n## {title}\n\n{text}\n")


W = load_nacional("1995Q1", "2026Q3")
W["trend"] = np.arange(len(W), dtype=float)
Q = ["q2", "q3", "q4"]

# ====================================================================== 1. DÉFICIT
H = W["hogares_epa"] * 1000.0          # miles -> hogares
TER = W["terminadas"]
dq_raw = H.diff()
adj = [Pd("2020Q2", "Q"), Pd("2020Q3", "Q"), Pd("2020Q4", "Q"), Pd("2021Q2", "Q")]
media_adj = float(dq_raw.loc[adj].mean())


def dq_var(mode):
    d = dq_raw.copy()
    if mode == "media":
        d.loc[Pd("2021Q1", "Q")] = media_adj
    elif mode == "cero":
        d.loc[Pd("2021Q1", "Q")] = 0.0
    return d


def ysum(s, y0, y1, q_ini=None):
    s = s[(s.index.year >= y0) & (s.index.year <= y1)]
    return float(s.sum())


def anual(s, years):
    return pd.Series({y: float(s[s.index.year == y].sum()) for y in years})


dq_a = dq_var("media")
dq_a0 = dq_var("cero")
yrs = list(range(2021, 2026))
Q2026 = [Pd("2026Q1", "Q"), Pd("2026Q2", "Q")]
H_fin = float(H.loc[Pd("2025Q4", "Q")])

tab = pd.DataFrame({"delta_hogares": anual(dq_a, yrs), "terminadas": anual(TER, yrs)})
r26 = pd.DataFrame({"delta_hogares": [float(dq_a.loc[Q2026].sum())], "terminadas": [float(TER.loc[Q2026].sum())]},
                   index=["2026T1-T2"])
tab = pd.concat([tab, r26])
tab["deficit_anual"] = tab["delta_hogares"] - tab["terminadas"]
tab["deficit_acum_desde_2021"] = tab["deficit_anual"].cumsum()
tab["delta_hogares_sin_correccion"] = list(anual(dq_raw, yrs).values) + [float(dq_raw.loc[Q2026].sum())]
tab.index = tab.index.astype(str)
save(tab.round(0), "deficit_anual_principal", ",.0f")

# parque MIVAU (anual, 31-dic)
pk = pd.read_csv(ROOT / "data" / "raw" / "mivau_parque.csv")
pk = pk[pk["serie"] == "parque_total_viviendas_nacional"].set_index("periodo")["valor"].astype(float)
dpk = pk.diff()

# ECP

def fila(nombre, periodo, dh, ter, nota):
    d = dh - ter
    return dict(variante=nombre, periodo=periodo, sum_delta_hogares=dh, sum_terminadas=ter, deficit=d,
                pct_hogares_2025T4=100 * d / H_fin, nota=nota)


rows = []
for lab, dq_, nota in [("(a) EPA corregida (PRINCIPAL)", dq_a,
                         f"Δ2021T1 sustituido por la media de Δ 2020T2-T4 y 2021T2 = {media_adj:,.0f} hogares"),
                        ("(a') EPA con Δ2021T1 = 0", dq_a0, "Δ2021T1 = 0"),
                        ("(a'') EPA sin corregir (solo referencia)", dq_raw, "incluye el salto metodológico de 2021T1 (nivel)")]:
    rows.append(fila(lab, "2021T1-2025T4", ysum(dq_, 2021, 2025), ysum(TER, 2021, 2025), nota))
    rows.append(fila(lab, "2021T1-2026T2", ysum(dq_, 2021, 2026), ysum(TER, 2021, 2026), nota + " (extensión)"))
# (b) ECP 60131: STOCK a día 1 del trimestre (fecha 2021-01-01 = 2021T1) -> hogares del periodo = H(t_fin+1) - H(2021T1)
He = W["hogares_ecp"]
rows.append(fila("(b) ECP 60131 (stock a 1 de enero)", "2021T1-2025T4 (H 1-ene-2026 − H 1-ene-2021)",
                 float(He.loc[Pd("2026Q1", "Q")] - He.loc[Pd("2021Q1", "Q")]), ysum(TER, 2021, 2025),
                 "ECP es stock a día 1 del trimestre: no hay trimestre perdido ni imputación"))
rows.append(fila("(b) ECP 60131 (stock a 1 de enero)", "2021T1-2026T2 (H 1-jul-2026 − H 1-ene-2021)",
                 float(He.loc[Pd("2026Q3", "Q")] - He.loc[Pd("2021Q1", "Q")]), ysum(TER, 2021, 2026), "extensión"))
ecp_2025 = float(He.loc[Pd("2026Q1", "Q")] - He.loc[Pd("2025Q1", "Q")])
ecp_m2124 = float((He.loc[Pd("2025Q1", "Q")] - He.loc[Pd("2021Q1", "Q")]) / 4)
# (c) parque
dh_a = anual(dq_a, yrs)
dpk_a = pd.Series({y: float(dpk.loc[y]) for y in yrs})
rows.append(fila("(c) Δparque MIVAU anual − Δhogares EPA corregida", "2021-2025", float(dh_a.sum()), float(dpk_a.sum()),
                 "parque = estimación MIVAU de viviendas totales (incl. secundarias y vacías); sin dato 2026"))
dfv = pd.DataFrame(rows)
save(dfv.round(1), "deficit_variantes", ",.1f", index=False)

# comparación Δparque vs terminadas libres (proxy de protegidas+otros)
cmp_pk = pd.DataFrame({"delta_parque_MIVAU": dpk_a, "terminadas_libres": anual(TER, yrs)})
cmp_pk["parque_menos_terminadas_libres"] = cmp_pk["delta_parque_MIVAU"] - cmp_pk["terminadas_libres"]
cmp_pk["delta_hogares_EPA_corr"] = dh_a
cmp_pk.index = cmp_pk.index.astype(str)
save(cmp_pk.round(0), "parque_vs_terminadas", ",.0f")

# BdE vs nuestro
t25 = tab.loc[2025] if 2025 in tab.index else tab.loc["2025"]
a_ = dfv.iloc[0]
bde = pd.DataFrame([
    ["Déficit acumulado 2021-2025", 750000, a_["deficit"], "BdE IA 2025 p. 157: terminadas − creación neta de hogares (signo cambiado)"],
    ["Creación neta de hogares 2025", 240000, float(t25["delta_hogares"]), "BdE: fuente de hogares no verificada aquí (¿ECP?); nosotros EPA"],
    ["Viviendas terminadas 2025", 92000, float(t25["terminadas"]), "Nosotros: SOLO viviendas libres MIVAU (sin protegidas)"],
    ["Creación neta de hogares 2025 (ECP a 1 de enero)", 240000, ecp_2025, "INFERENCIA: ECP 60131 H(1-ene-2026) − H(1-ene-2025); el BdE no nombra la operación estadística"],
    ["Media anual de hogares 2021-2024 (ECP a 1 de enero)", 245000, ecp_m2124, "INFERENCIA, idem; BdE p. 157: 'promedio anual de 245.000 entre 2021 y 2024'"],
    ["Déficit en % de hogares", 3.7, a_["pct_hogares_2025T4"], "% sobre hogares EPA 2025T4"],
    ["Déficit 2021-2025 (IEF otoño 2025)", 700000, a_["deficit"], "IEF con datos del 1S 2025; periodo y fuente distintos"]],
    columns=["concepto", "BdE", "este_trabajo_principal", "nota"])
bde["diferencia"] = bde["este_trabajo_principal"] - bde["BdE"]
save(bde, "comparacion_bde_deficit", ",.4g", index=False)
ecp_row = dfv.iloc[6]
dec = pd.DataFrame([
    ["Δhogares 2021-2025", a_["sum_delta_hogares"], ecp_row["sum_delta_hogares"], a_["sum_delta_hogares"] - ecp_row["sum_delta_hogares"],
     "fuente de hogares: EPA corregida frente a ECP a 1 de enero (implícita en el BdE: inferencia)"],
    ["Terminadas 2021-2025", a_["sum_terminadas"], ecp_row["sum_delta_hogares"] - 750000, (ecp_row["sum_delta_hogares"] - 750000) - a_["sum_terminadas"],
     "implícito BdE = ΔECP − 750.000; diferencia ≈ viviendas protegidas no incluidas (y redondeo de '750.000')"]],
    columns=["componente", "este_trabajo", "BdE_implicito", "diferencia_BdE_menos_nuestro", "nota"])
dec["contribucion_a_la_diferencia_de_deficit"] = [dec.iloc[0, 3] * -1, dec.iloc[1, 3]]
save(dec, "descomposicion_diferencia_bde", ",.0f", index=False)

# serie larga anual
yl = list(range(2003, 2026))
long = pd.DataFrame({"delta_hogares_EPA_corr": anual(dq_a, yl),
                     "delta_parque_MIVAU": pd.Series({y: float(dpk.get(y, np.nan)) for y in yl}),
                     "terminadas_libres": pd.Series({y: (float(TER[TER.index.year == y].sum()) if y >= 2008 else np.nan) for y in yl})})
long["desequilibrio_hogares_menos_terminadas"] = long["delta_hogares_EPA_corr"] - long["terminadas_libres"]
long["desequilibrio_hogares_menos_dparque"] = long["delta_hogares_EPA_corr"] - long["delta_parque_MIVAU"]
for y0 in (2008, 2014):
    s = long.loc[y0:, "desequilibrio_hogares_menos_terminadas"].cumsum()
    long[f"ESCENARIO_acum_equilibrio_supuesto_en_{y0 - 1}"] = s
long.index.name = "anio"
save(long.round(0), "serie_larga_desequilibrio", ",.0f")
fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(long.index - 0.2, long["desequilibrio_hogares_menos_terminadas"] / 1e3, width=0.4, label="Δhogares − terminadas libres (2008+)")
ax.bar(long.index + 0.2, long["desequilibrio_hogares_menos_dparque"] / 1e3, width=0.4, label="Δhogares − Δparque MIVAU")
ax.axhline(0, color="k", lw=.6)
ax.set_ylabel("miles de viviendas")
ax.set_title("Desequilibrio anual hogares-vivienda (flujo; sin equilibrio inicial supuesto)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "serie_larga_desequilibrio.png", dpi=130)
plt.close(fig)

# ====================================================================== 2. ELASTICIDAD
W["ln_P"] = W["ln_ipv_real"]
W["ln_Pt"] = W["ln_p_tasado"] - W["ln_deflactor"]
for k in range(0, 9):
    W[f"P_l{k}"] = W["ln_P"].shift(k)
    W[f"Pt_l{k}"] = W["ln_Pt"].shift(k)
bad = W["ln_visados"].isna() & (W.index >= Pd("2008Q1", "Q"))      # 2016T2 y 2017T2 (huecos MIVAU)
DEPS = {"visados": "ln_visados", "terminadas": "ln_terminadas", "permisos": "ln_permisos"}
for n_, c in DEPS.items():
    W[f"y_{n_}"] = W[c].where(~bad)       # misma muestra: se excluyen los trimestres sin visados en las tres
GRID = [("visados", k) for k in (0, 2, 4)] + [("terminadas", k) for k in (4, 6, 8)] + [("permisos", k) for k in (0, 2, 4)]
PRINCIPAL = {"visados": 4, "terminadas": 8, "permisos": 4}      # declarado antes de estimar
COSTE, TIPO = "ln_costes_real", "tipo_hip_real"


def run_dols(dep, k, price="P", fijas=None, kk=2, desde=None, y=None):
    xs = [f"{price}_l{k}", COSTE, TIPO]
    fj = (fijas if fijas is not None else Q)
    return dols(W, y or f"y_{dep}", xs, fj, k=kk, desde=desde), xs, fj


# muestra común global (todas las especificaciones DOLS principales y de robustez con precio ipv)
starts, ends = [], []
for dep, k in GRID:
    for tr in (False, True):
        r, _, _ = run_dols(dep, k, fijas=Q + (["trend"] if tr else []))
        idx = r["res"].model.data.row_labels
        starts.append(idx[0]); ends.append(idx[-1])
S_START, S_END = max(starts), min(ends)
SAMP_ALL = None
print("muestra común DOLS:", S_START, S_END)

diag_rows, dols_rows, res_store = [], [], {}


def reg_dols(mid, dep, k, r, xs, fj, notas, price="ipv"):
    res = r["res"]
    # RMSE de predicción a un paso con regresores efectivos, ventana expansiva desde 2018T1 (condicional)
    idx, yv, Xv = list(res.model.data.row_labels), np.asarray(res.model.endog), np.asarray(res.model.exog)
    err = []
    for i, p in enumerate(idx):
        if p >= Pd("2018Q1", "Q") and i > Xv.shape[1] + 6:
            b = np.linalg.lstsq(Xv[:i], yv[:i], rcond=None)[0]
            err.append(yv[i] - Xv[i] @ b)
    rm = float(np.sqrt(np.mean(np.square(err)))) if err else np.nan
    f = f"{dep}: y ~ const + {' + '.join(xs)} + {'+'.join(fj)} + Δ(±{r['_kk']}) de regresores [DOLS]"
    REG.log_res("F4", mid, f, res, interes=xs[0], rmse_oos=rm, notas=notas)
    return rm


MAIN = {}
for price, label in (("P", "ipv"), ("Pt", "tasado")):
    for dep, k in GRID:
        for tr in (False, True):
            if price == "Pt" and tr:
                continue
            fj = Q + (["trend"] if tr else [])
            r, xs, fj = run_dols(dep, k, price=price, fijas=fj, desde=str(S_START))
            r["_kk"] = 2
            mid = f"dols_{dep}_k{k}_{label}{'_trend' if tr else ''}"
            rm = reg_dols(mid, dep, k, r, xs, fj, f"familia=elasticidad; muestra común {S_START}-{S_END}; precio real {label}"
                          + ("; con tendencia" if tr else ""))
            res = r["res"]
            d = diagnostics(res)
            d.update(modelo=mid)
            diag_rows.append(d)
            dols_rows.append(dict(modelo=mid, dep=dep, k=k, precio=label, tendencia=tr, beta=res.params[xs[0]],
                                  EE=res.bse[xs[0]], p=res.pvalues[xs[0]], beta_costes=res.params[xs[1]],
                                  EE_costes=res.bse[xs[1]], beta_tipo=res.params[xs[2]], EE_tipo=res.bse[xs[2]],
                                  n=int(res.nobs), r2_adj=res.rsquared_adj, rmse_1paso=rm))
            res_store[mid] = r
SAMP = res_store["dols_visados_k4_ipv"]["res"].model.data.row_labels
SAMP = pd.PeriodIndex(list(SAMP), freq="Q")
dols_tab = pd.DataFrame(dols_rows)
save(dols_tab, "dols_resultados", ".4g", index=False)

# --- OLS estático (misma muestra), HAC
ols_rows = []
for dep, k in GRID:
    fm = f"y_{dep} ~ P_l{k} + {COSTE} + {TIPO} + q2 + q3 + q4"
    d = W.loc[SAMP]
    res = ols_hac(fm, d)
    REG.log_res("F4", f"ols_{dep}_k{k}_ipv", fm + " [OLS estático HAC4]", res, interes=f"P_l{k}",
                notas=f"familia=elasticidad; misma muestra {SAMP[0]}-{SAMP[-1]}")
    dd = diagnostics(res)
    dd.update(modelo=f"ols_{dep}_k{k}_ipv")
    diag_rows.append(dd)
    ols_rows.append(dict(modelo=f"ols_{dep}_k{k}", dep=dep, k=k, beta=res.params[f"P_l{k}"], EE=res.bse[f"P_l{k}"],
                         p=res.pvalues[f"P_l{k}"], n=int(res.nobs), r2_adj=res.rsquared_adj))
ols_tab = pd.DataFrame(ols_rows)
save(ols_tab, "ols_estatico", ".4g", index=False)

# --- Chow / Bai-Perron / BP sobre la ecuación estática de las principales
chow_rows, bp_rows = [], []
for dep, k in PRINCIPAL.items():
    fm = f"y_{dep} ~ P_l{k} + {COSTE} + {TIPO} + q2 + q3 + q4"
    d = W.loc[SAMP].dropna(subset=[f"y_{dep}"])
    for fe in ("2014Q1", "2020Q1", "2022Q3"):
        c = chow(d, fm, fe)
        c.update(dep=dep, k=k)
        chow_rows.append(c)
    try:
        X = sm.add_constant(d[[f"P_l{k}", COSTE, TIPO]])
        bp = bai_perron(d[f"y_{dep}"], X, max_bkps=3, min_size=12)
        bp_rows.append(dict(dep=dep, k=k, n_bkps=bp["n_bkps"], fechas=";".join(bp["fechas"])))
    except Exception as e:
        bp_rows.append(dict(dep=dep, k=k, n_bkps=np.nan, fechas=str(e)[:50]))
save(pd.DataFrame(chow_rows), "chow", ".4g", index=False)
save(pd.DataFrame(bp_rows), "bai_perron", ".4g", index=False)
save(pd.DataFrame(diag_rows).set_index("modelo"), "diagnosticos", ".4g")

# --- ECM (con el ect del DOLS, misma muestra)
ecm_rows = []
for dep, k in GRID:
    r = res_store[f"dols_{dep}_k{k}_ipv"]
    d = W.loc[SAMP[0] - 1: SAMP[-1]].copy() if False else W.copy()
    d["ect_l1"] = r["ect"].shift(1)
    d["dy"] = d[f"y_{dep}"].diff()
    d["dy_l1"] = d["dy"].shift(1)
    d["dP"] = d[f"P_l{k}"].diff()
    d["dC"] = d[COSTE].diff()
    d["dT"] = d[TIPO].diff()
    fm = "dy ~ ect_l1 + dP + dC + dT + dy_l1 + q2 + q3 + q4"
    de = d.loc[SAMP].dropna(subset=["dy", "ect_l1", "dP", "dC", "dT", "dy_l1"])
    res = ols_hac(fm, de)
    REG.log_res("F4", f"ecm_{dep}_k{k}", fm + f" [ECM; ect del DOLS {dep} k={k}]", res, interes="dP",
                notas="familia=ECM (coef. de interés: elasticidad de corto plazo dP; velocidad = ect_l1)")
    dd = diagnostics(res)
    dd.update(modelo=f"ecm_{dep}_k{k}")
    diag_rows.append(dd)
    ecm_rows.append(dict(modelo=f"ecm_{dep}_k{k}", dep=dep, k=k, ect=res.params["ect_l1"], EE_ect=res.bse["ect_l1"],
                         p_ect=res.pvalues["ect_l1"], dP_corto=res.params["dP"], EE_dP=res.bse["dP"], p_dP=res.pvalues["dP"],
                         n=int(res.nobs), r2_adj=res.rsquared_adj, DW=dd["DW"], BG4_p=dd["BG4_p"]))
ecm_tab = pd.DataFrame(ecm_rows)
save(ecm_tab, "ecm_resultados", ".4g", index=False)
save(pd.DataFrame(diag_rows).set_index("modelo"), "diagnosticos", ".4g")

# --- IV (2SLS con HAC) -----------------------------------------------------
from linearmodels.iv import IV2SLS, IVGMM  # noqa: E402

SHIFT = ["ln_ocupados", "ln_pob_extranj", "ln_renta_hog_real"]


def run_iv(dep, k, forma, idx, tr=False, tag=""):
    m = max(k, 4)
    d = pd.DataFrame(index=W.index)
    if forma == "niveles":
        d["y"] = W[f"y_{dep}"]; d["P"] = W[f"P_l{k}"]; d["C"] = W[COSTE]; d["R"] = W[TIPO]
        for j, s in enumerate(SHIFT):
            d[f"z{j}"] = W[s].shift(m)
        exog = ["C", "R"] + Q
    else:
        d["y"] = W[f"y_{dep}"].diff(4); d["P"] = W[f"P_l{k}"].diff(4); d["C"] = W[COSTE].diff(4); d["R"] = W[TIPO].diff(4)
        for j, s in enumerate(SHIFT):
            d[f"z{j}"] = W[s].shift(m).diff(4)
        exog = ["C", "R"]
    for q in Q:
        d[q] = W[q]
    if tr:
        d["trend"] = W["trend"]; exog = exog + ["trend"]
    d["const"] = 1.0
    d = d.loc[idx].dropna()
    mod = IV2SLS(d["y"], d[["const"] + exog], d[["P"]], d[["z0", "z1", "z2"]])
    res = mod.fit(cov_type="kernel", kernel="bartlett", bandwidth=4)
    fs = res.first_stage.diagnostics
    F = float(fs.loc["P", "f.stat"]); Fp = float(fs.loc["P", "f.pval"])
    try:   # J de Hansen con matriz de pesos HAC (GMM en dos etapas; el coeficiente reportado es el 2SLS)
        gm = IVGMM(d["y"], d[["const"] + exog], d[["P"]], d[["z0", "z1", "z2"]], weight_type="kernel",
                   kernel="bartlett", bandwidth=4).fit(cov_type="kernel", kernel="bartlett", bandwidth=4)
        J, Jp = float(gm.j_stat.stat), float(gm.j_stat.pval)
    except Exception:
        J, Jp = np.nan, np.nan
    b, se, p = float(res.params["P"]), float(res.std_errors["P"]), float(res.pvalues["P"])
    mid = f"iv_{forma}_{dep}_k{k}{tag}"
    REG.log("F4", mid, f"{dep}: y ~ {'+'.join(['const'] + exog)} + [P_l{k} ~ {','.join(s + '_l' + str(m) for s in SHIFT)}] 2SLS-HAC4, forma={forma}",
            d.index[0], d.index[-1], int(res.nobs), np.nan, np.nan, np.nan, np.nan, b, p,
            f"familia=elasticidad IV; F1={F:.1f}; J p={Jp:.3f}")
    ident = (F >= 10) and (Jp > 0.05)
    return dict(modelo=mid, dep=dep, k=k, forma=forma, beta=b, EE=se, p=p, F1=F, F1_p=Fp, J=J, J_p=Jp, n=int(res.nobs),
                ini=str(d.index[0]), fin=str(d.index[-1]), identificada=bool(ident), tendencia=tr)


iv_rows = []
for dep, k in GRID:
    iv_rows.append(run_iv(dep, k, "niveles", SAMP))
    iv_rows.append(run_iv(dep, k, "niveles", SAMP, tr=True, tag="_trend"))
IDX_D4 = SAMP[SAMP >= Pd("2010Q1", "Q")]     # Δ4 de P_l8 exige 12 trimestres desde 2007T1: misma muestra Δ4 para todas
for dep, k in GRID:
    iv_rows.append(run_iv(dep, k, "d4", IDX_D4))
iv_tab = pd.DataFrame(iv_rows)
# la muestra Δ4 es la misma entre dependientes sólo si coincide: se informa n
save(iv_tab, "iv_resultados", ".4g", index=False)

# --- Regresión en Δ4 (OLS-HAC(8), misma muestra que el IV en Δ4): robustez ante la no-cointegración
d4_rows = []
Wd = pd.DataFrame(index=W.index)
Wd["dC"] = W[COSTE].diff(4); Wd["dR"] = W[TIPO].diff(4)
for dep, k in GRID:
    Wd["dy"] = W[f"y_{dep}"].diff(4); Wd["dP"] = W[f"P_l{k}"].diff(4)
    de = Wd.loc[IDX_D4].dropna()
    fm = "dy ~ dP + dC + dR"
    res = ols_hac(fm, de, maxlags=8)
    REG.log_res("F4", f"ols_d4_{dep}_k{k}", f"Δ4 {dep} ~ Δ4 P_l{k} + Δ4 costes_real + Δ4 tipo_real [OLS HAC8]", res, interes="dP",
                notas=f"familia=elasticidad; robustez en Δ4, misma muestra {IDX_D4[0]}-{IDX_D4[-1]}")
    d4_rows.append(dict(modelo=f"ols_d4_{dep}_k{k}", dep=dep, k=k, beta=res.params["dP"], EE_HAC8=res.bse["dP"], p=res.pvalues["dP"],
                        n=int(res.nobs), r2_adj=res.rsquared_adj))
d4_tab = pd.DataFrame(d4_rows)
save(d4_tab, "ols_delta4", ".4g", index=False)

# --- Cointegración (EG + Johansen + ARDL bounds), ecuación de iniciadas y alternativas
Wc = W.copy()
for c in ("ln_visados",):
    Wc[c + "_int"] = Wc[c].interpolate(limit_area="inside")     # SOLO para los contrastes de cointegración (2 huecos)
Qdf = lambda d: d[Q].astype(float)


def coint_system(frame, y, xs, label):
    d = common_sample(frame, [y] + xs)
    out = dict(sistema=label, y=y, X=" + ".join(xs), ini=str(d.index[0]), fin=str(d.index[-1]), N=len(d))
    try:
        t, p, cv = coint(d[y], d[xs], trend="c", method="aeg", maxlag=4, autolag="aic")
        out.update(EG_t=t, EG_p=p, EG_rech=bool(p < .05))
    except Exception:
        out.update(EG_t=np.nan, EG_p=np.nan, EG_rech=False)
    try:
        arr = d[[y] + xs].values
        try:
            kk = int(select_order(arr, maxlags=4, deterministic="co").aic)
        except Exception:
            kk = 1
        j = coint_johansen(arr, det_order=0, k_ar_diff=kk)
        rt = next((r for r in range(len(j.lr1)) if j.lr1[r] < j.cvt[r, 1]), len(j.lr1))
        out.update(J_kardiff=kk, J_traza0=j.lr1[0], J_cv95=j.cvt[0, 1], J_rango_traza=rt, J_rech=bool(rt >= 1))
    except Exception:
        out.update(J_rech=False)
    try:
        ex = d[xs]
        sel = ardl_select_order(d[y], 4, ex, 2, trend="c", fixed=Qdf(d), ic="aic")
        o = sel.model.ardl_order
        order = {c: max(k_, 1) for c, k_ in zip(xs, o[1:])}
        u = UECM(d[y], max(o[0], 1), ex, order, trend="c", fixed=Qdf(d))
        r = u.fit(cov_type="HAC", cov_kwds={"maxlags": 4})
        b = r.bounds_test(case=3)
        up = float(b.critical_values.loc[95.0, "upper"]); lo = float(b.critical_values.loc[95.0, "lower"])
        out.update(ARDL_orden=str(tuple(o)), ARDL_F=float(b.statistic), ARDL_I0_5=lo, ARDL_I1_5=up,
                   ARDL_rech=bool(b.statistic > up), ARDL_inconcluso=bool(lo <= b.statistic <= up))
    except Exception as e:
        out.update(ARDL_rech=False, ARDL_err=str(e)[:60])
    n = int(bool(out.get("EG_rech"))) + int(bool(out.get("J_rech"))) + int(bool(out.get("ARDL_rech")))
    out["n_rechazos"] = n
    out["decision"] = ("cointegración (3/3)" if n == 3 else "cointegración (2/3, discrepancia)" if n == 2
                       else "evidencia mixta (1/3)" if n == 1 else "sin cointegración (0/3)")
    return out


cs = []
for dep, k in [("visados", 0), ("visados", 2), ("visados", 4), ("terminadas", 8), ("permisos", 4)]:
    ycol = "ln_visados_int" if dep == "visados" else DEPS[dep]
    cs.append(coint_system(Wc.loc["2008Q1":"2026Q2"], ycol, [f"P_l{k}", COSTE, TIPO],
                           f"{dep} (k={k}){' [2 huecos interpolados solo aquí]' if dep == 'visados' else ''}"))
    REG.log("F4", f"coint_{dep}_k{k}", f"{ycol} ~ P_l{k}+{COSTE}+{TIPO} [EG/Johansen/ARDL]", cs[-1]["ini"], cs[-1]["fin"],
            cs[-1]["N"], np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, f"cointegración: {cs[-1]['decision']}")
cdf = pd.DataFrame(cs)
save(cdf, "cointegracion", ".4g", index=False)

# --- Quiebre 2014: submuestra 2014T1+ (DOLS ±1, sobre todo por grados de libertad), OLS, IV niveles
post_rows = []
for dep, k in GRID:
    r, xs, fj = run_dols(dep, k, desde="2014Q1", kk=1)
    r["_kk"] = 1
    mid = f"dols_{dep}_k{k}_ipv_2014+"
    reg_dols(mid, dep, k, r, xs, fj, "familia=elasticidad; submuestra 2014Q1+ (DOLS ±1)")
    res = r["res"]
    dd = diagnostics(res); dd.update(modelo=mid); diag_rows.append(dd)
    d = W.loc[res.model.data.row_labels]
    ro = ols_hac(f"y_{dep} ~ P_l{k} + {COSTE} + {TIPO} + q2 + q3 + q4", d)
    REG.log_res("F4", f"ols_{dep}_k{k}_ipv_2014+", f"y_{dep} ~ P_l{k}+{COSTE}+{TIPO}+q [OLS HAC4] 2014Q1+", ro,
                interes=f"P_l{k}", notas="familia=elasticidad; submuestra 2014Q1+")
    iv = run_iv(dep, k, "niveles", d.index, tag="_2014+")
    post_rows.append(dict(dep=dep, k=k, n_dols=int(res.nobs), beta_DOLS=res.params[xs[0]], EE_DOLS=res.bse[xs[0]], p_DOLS=res.pvalues[xs[0]],
                          beta_OLS=ro.params[f"P_l{k}"], EE_OLS=ro.bse[f"P_l{k}"], p_OLS=ro.pvalues[f"P_l{k}"],
                          beta_IV=iv["beta"], EE_IV=iv["EE"], p_IV=iv["p"], F1=iv["F1"], J_p=iv["J_p"], n_IV=iv["n"]))
post_tab = pd.DataFrame(post_rows)
save(post_tab, "submuestra_2014", ".4g", index=False)
save(pd.DataFrame(diag_rows).set_index("modelo"), "diagnosticos", ".4g")

# --- Muestra larga con valor tasado real (permisos, 2003T1+): DOLS ±2
long_rows = []
for k in (0, 2, 4):
    r, xs, fj = run_dols("permisos", k, price="Pt", y="ln_permisos")
    r["_kk"] = 2
    res = r["res"]
    reg_dols(f"dols_permisos_k{k}_tasado_larga", "permisos", k, r, xs, fj,
             f"familia=elasticidad; muestra larga {res.model.data.row_labels[0]}-{res.model.data.row_labels[-1]}; tasado real")
    long_rows.append(dict(dep="permisos", k=k, muestra=f"{res.model.data.row_labels[0]}-{res.model.data.row_labels[-1]}",
                          beta=res.params[xs[0]], EE=res.bse[xs[0]], p=res.pvalues[xs[0]], n=int(res.nobs)))
long_tab = pd.DataFrame(long_rows)
save(long_tab, "muestra_larga_tasado_permisos", ".4g", index=False)

# ====================================================================== 4. PANEL CCAA
from linearmodels.panel import PanelOLS  # noqa: E402

pn = pd.read_csv(ROOT / "data" / "processed" / "panel_ccaa_q.csv")
pn["per"] = pd.PeriodIndex(pn["trimestre"], freq="Q")
full = pd.period_range(pn["per"].min(), pn["per"].max(), freq="Q")
wide_p = pn.pivot(index="per", columns="ccaa", values="d4_ln_ipv").reindex(full)
panel_rows = []
LAGS = (0, 4, 8)
for dep in ("terminadas", "visados"):
    wy = pn.pivot(index="per", columns="ccaa", values=f"d4_ln_{dep}").reindex(full)
    st = {"y": wy.stack()}
    for L in LAGS:
        st[f"p{L}"] = wide_p.shift(L).stack()
    dfp = pd.DataFrame(st).dropna()
    dfp = dfp[dfp.index.get_level_values(0) >= Pd("2008Q1", "Q")]
    dfp.index = pd.MultiIndex.from_arrays([dfp.index.get_level_values(1), dfp.index.get_level_values(0).map(lambda p: p.ordinal)])
    for L in LAGS:
        for te, lab in ((True, "FE CCAA+tiempo"), (False, "FE CCAA")):
            mod = PanelOLS(dfp["y"], dfp[[f"p{L}"]], entity_effects=True, time_effects=te)
            rc = mod.fit(cov_type="clustered", cluster_entity=True)
            rk = mod.fit(cov_type="kernel", kernel="bartlett", bandwidth=4)
            b = float(rc.params[f"p{L}"])
            mid = f"panel_{dep}_L{L}_{'te' if te else 'noTE'}"
            REG.log("F4", mid, f"d4 ln {dep}_ct ~ d4 ln ipv_c,t-{L} [{lab}; cluster CCAA]", dfp.index.get_level_values(1).min(),
                    dfp.index.get_level_values(1).max(), int(rc.nobs), np.nan, np.nan, np.nan, np.nan, b,
                    float(rc.pvalues[f"p{L}"]), "familia=elasticidad panel (robustez); Extremadura sin terminadas")
            ent_ = dfp.index.get_level_values(0).to_numpy(); tim_ = dfp.index.get_level_values(1).to_numpy()
            _, t_w, p_w = wcb_webb(dfp["y"].to_numpy(float), dfp[f"p{L}"].to_numpy(float), ent_, tim_, te)
            panel_rows.append(dict(modelo=mid, dep=dep, lag_trim=L, efectos=lab, beta=b, p_WCB_webb=p_w, EE_cluster=float(rc.std_errors[f"p{L}"]),
                                   p_cluster=float(rc.pvalues[f"p{L}"]), EE_DK=float(rk.std_errors[f"p{L}"]), p_DK=float(rk.pvalues[f"p{L}"]),
                                   n=int(rc.nobs), CCAA=int(dfp.index.get_level_values(0).nunique()), r2_within=float(rc.rsquared_within)))
# Wild cluster bootstrap (Webb 6 puntos, 9.999 réplicas, WCR bajo H0: beta=0), pre-registrado en decisiones.md
def wcb_webb(y, x, ent, tim, te, B=9999, seed=SEED):
    ent_c = pd.factorize(ent)[0]; Gn = ent_c.max() + 1
    D = [np.eye(Gn)[ent_c]]
    if te:
        tc = pd.factorize(tim)[0]; D.append(np.eye(tc.max() + 1)[tc][:, 1:])
    D = np.column_stack(D)
    M = lambda v: v - D @ np.linalg.lstsq(D, v, rcond=None)[0]
    xt, e0 = M(x), M(y)           # e0 = residuo restringido (H0: beta=0) tras absorber efectos
    Sxx = float(xt @ xt)
    order = np.argsort(ent_c, kind="stable"); starts = np.r_[0, np.flatnonzero(np.diff(ent_c[order])) + 1]

    yt0 = M(y)
    b0 = float(xt @ yt0 / Sxx)
    u0 = (yt0 - b0 * xt)
    g0 = np.add.reduceat((xt * u0)[order], starts)
    t0 = b0 / (np.sqrt(float(g0 @ g0)) / Sxx)
    rng = np.random.default_rng(seed)
    vals = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
    S2 = np.add.reduceat((xt * xt)[order], starts)
    tb = np.empty(B)
    ch = 1000
    for a in range(0, B, ch):
        bb = min(ch, B - a)
        w = vals[rng.integers(0, 6, size=(Gn, bb))]
        ys = w[ent_c] * e0[:, None]                         # y* tras absorber efectos (M y* = w e0)
        bs = (xt @ ys) / Sxx
        S1 = np.add.reduceat((xt[:, None] * ys)[order], starts, axis=0)
        sg = S1 - S2[:, None] * bs[None, :]
        tb[a:a + bb] = bs / (np.sqrt((sg ** 2).sum(axis=0)) / Sxx)
    return b0, t0, float((np.abs(tb) >= abs(t0)).mean())


pan_tab = pd.DataFrame(panel_rows)
save(pan_tab, "panel_ccaa", ".4g", index=False)

# ====================================================================== 3. CONTRASTE BdE
cont = []
for _, r in dols_tab[(dols_tab.precio == "ipv") & (~dols_tab.tendencia)].iterrows():
    cont.append(dict(dep=r.dep, estimador="DOLS ±2", k=r.k, muestra=f"{SAMP[0]}-{SAMP[-1]}", beta=r.beta, EE=r.EE, p=r.p, n=r.n, nivel="asociación"))
for _, r in ols_tab.iterrows():
    cont.append(dict(dep=r.dep, estimador="OLS estático", k=r.k, muestra=f"{SAMP[0]}-{SAMP[-1]}", beta=r.beta, EE=r.EE, p=r.p, n=r.n, nivel="asociación"))
for _, r in iv_tab[(iv_tab.forma == "niveles") & (~iv_tab.tendencia) & (~iv_tab.modelo.str.endswith("2014+"))].iterrows():
    cont.append(dict(dep=r.dep, estimador="IV 2SLS niveles", k=r.k, muestra=f"{r.ini}-{r.fin}", beta=r.beta, EE=r.EE, p=r.p, n=r.n,
                     nivel=("IV supera F>=10 y J (identificación solo condicional a una exclusión discutible)" if r.identificada else f"asociación (F1={r.F1:.1f}; J p={r.J_p:.3f})")))
for _, r in iv_tab[iv_tab.forma == "d4"].iterrows():
    cont.append(dict(dep=r.dep, estimador="IV 2SLS Δ4", k=r.k, muestra=f"{r.ini}-{r.fin}", beta=r.beta, EE=r.EE, p=r.p, n=r.n,
                     nivel=("IV supera F>=10 y J (identificación solo condicional a una exclusión discutible)" if r.identificada else f"asociación (F1={r.F1:.1f}; J p={r.J_p:.3f})")))
for _, r in post_tab.iterrows():
    cont.append(dict(dep=r.dep, estimador="DOLS ±1 2014T1+", k=r.k, muestra="2014Q1-", beta=r.beta_DOLS, EE=r.EE_DOLS, p=r.p_DOLS, n=r.n_dols, nivel="asociación"))
    cont.append(dict(dep=r.dep, estimador="IV niveles 2014T1+", k=r.k, muestra="2014Q1-", beta=r.beta_IV, EE=r.EE_IV, p=r.p_IV, n=r.n_IV,
                     nivel=("IV supera F>=10 y J (identificación solo condicional a una exclusión discutible)" if (r.F1 >= 10 and r.J_p > .05) else f"asociación (F1={r.F1:.1f}; J p={r.J_p:.3f})")))
ct = pd.DataFrame(cont)
ct["IC95_inf"] = ct.beta - 1.96 * ct.EE
ct["IC95_sup"] = ct.beta + 1.96 * ct.EE
ct["BdE_0.45"] = BDE_EL
ct["p_H0_beta=0.45"] = 2 * stats.norm.sf(np.abs((ct.beta - BDE_EL) / ct.EE))
ct["dentro_IC_con_0.45"] = (ct.IC95_inf <= BDE_EL) & (BDE_EL <= ct.IC95_sup)
save(ct, "contraste_bde", ".4g", index=False)

# figura: bosque de elasticidades (principales)
fig, ax = plt.subplots(figsize=(8, 6))
sel = ct[(ct.estimador.isin(["DOLS ±2", "OLS estático", "IV 2SLS niveles", "DOLS ±1 2014T1+"])) &
         (ct.k == ct.dep.map(PRINCIPAL))].reset_index(drop=True)
for i, r in sel.iterrows():
    ax.errorbar(r.beta, i, xerr=1.96 * r.EE, fmt="o", color="C0" if r.dep == "visados" else "C1" if r.dep == "terminadas" else "C2")
ax.set_yticks(range(len(sel)))
ax.set_yticklabels([f"{r.dep} k={r.k} {r.estimador}" for _, r in sel.iterrows()], fontsize=7)
ax.axvline(BDE_EL, color="r", ls="--", label="BdE 0,45 (NO VERIFICADA la fuente primaria)")
ax.axvline(0, color="k", lw=.6)
ax.set_xlabel("elasticidad (IC 95 % HAC)")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(OUT / "elasticidades_vs_bde.png", dpi=130)
plt.close(fig)

# ====================================================================== corrección por búsqueda
rg = REG.read()
fam = rg[rg["notas"].astype(str).str.contains("familia=elasticidad")].copy()
fam = fam.dropna(subset=["p_interes"])
N_TOTAL = len(rg)
pv = {r.modelo_id: float(r.p_interes) for r in fam.itertuples()}
hm = holm(pv)
fam["p_bonferroni_N_total"] = np.minimum(1.0, fam["p_interes"] * N_TOTAL)
fam["p_bonferroni_N_familia"] = np.minimum(1.0, fam["p_interes"] * len(fam))
fam["p_holm_familia"] = fam["modelo_id"].map(hm)
fam = fam[["modelo_id", "coef_interes", "p_interes", "p_bonferroni_N_familia", "p_bonferroni_N_total", "p_holm_familia", "n"]]
save(fam, "correccion_busqueda", ".4g", index=False)
print("N modelos registrados:", N_TOTAL, "familia elasticidad:", len(fam))


# ====================================================================== 5. RESUMEN
def g(df, **kw):
    q = df
    for k_, v in kw.items():
        q = q[q[k_] == v]
    return q.iloc[0]


a1 = dfv.iloc[0]; a0 = dfv.iloc[2]; araw = dfv.iloc[4]; ecp = dfv.iloc[6]; ecp2 = dfv.iloc[8]; cpk = dfv.iloc[10]
pr = {d_: g(dols_tab, dep=d_, k=PRINCIPAL[d_], precio="ipv", tendencia=False) for d_ in PRINCIPAL}
pri = {d_: g(iv_tab, dep=d_, k=PRINCIPAL[d_], forma="niveles", tendencia=False) for d_ in PRINCIPAL}
prd = {d_: g(iv_tab, dep=d_, k=PRINCIPAL[d_], forma="d4") for d_ in PRINCIPAL}
pro = {d_: g(ols_tab, dep=d_, k=PRINCIPAL[d_]) for d_ in PRINCIPAL}
pop = {d_: g(post_tab, dep=d_, k=PRINCIPAL[d_]) for d_ in PRINCIPAL}
nfam = len(fam)
fam_s = fam.copy()
n_sig_holm = int((fam_s["p_holm_familia"] < .05).sum())
bonf_n = int((fam_s["p_bonferroni_N_total"] < .05).sum())
ranges = dols_tab[(dols_tab.precio == "ipv")].groupby("dep")["beta"].agg(["min", "max"])
dgx = pd.DataFrame(diag_rows).set_index("modelo")
fallan = {m_: dgx.loc[m_] for m_ in [f"dols_{d_}_k{k_}_ipv" for d_, k_ in PRINCIPAL.items()]}


def fl(r_):
    out = []
    if r_["BG4_p"] < .05: out.append("BG(4)")
    if r_["BP_p"] < .05: out.append("BP")
    if r_["JB_p"] < .05: out.append("JB")
    if r_["RESET_p"] < .05: out.append("RESET")
    if r_["CUSUM_p"] < .05: out.append("CUSUM")
    if r_["DW"] < 1.5 or r_["DW"] > 2.5: out.append(f"DW={r_['DW']:.2f}")
    if r_["VIF_max"] > 10: out.append(f"VIF={r_['VIF_max']:.0f}")
    return ", ".join(out) or "ninguno"


diag_txt = "; ".join(f"{m_.replace('dols_', '').replace('_ipv', '')}: {fl(r_)}" for m_, r_ in fallan.items())
txt = f"""# F4 - Oferta (P3): déficit de vivienda y elasticidad de la oferta

Generado por `src/f4_oferta.py` (semilla {SEED}). Todo es **asociación** salvo lo indicado en 'Nivel de evidencia'.

## Respuesta corta a P3

1. **Déficit 2021-2025 (flujo acumulado de Δhogares − terminadas, sin equilibrio inicial supuesto).** Principal (EPA corregida):
   **{a1.deficit:,.0f} viviendas** ({a1.pct_hogares_2025T4:.1f} % de los hogares EPA 2025T4); con Δ2021T1=0: {a0.deficit:,.0f};
   con ECP 60131 (2021T2-2025T4, periodo consistente): {ecp.deficit:,.0f}; ECP anualizada: {ecp2.deficit:,.0f}; con Δparque MIVAU: {cpk.deficit:,.0f}.
   Extensión a 2026T2 (principal): {dfv.iloc[1].deficit:,.0f}. BdE: ~750.000 (IA 2025) y 700.000 (IEF otoño 2025). Las diferencias NO se ajustan (ver abajo).
2. **Elasticidad de la oferta** (iniciadas libres MIVAU, precio real retardado, DOLS ±2, HAC4, muestra común {SAMP[0]}-{SAMP[-1]}, N={pr['visados'].n}):
   iniciadas k=4: **{pr['visados'].beta:.2f}** (EE {pr['visados'].EE:.2f}); terminadas k=8: {pr['terminadas'].beta:.2f} ({pr['terminadas'].EE:.2f});
   permisos k=4: {pr['permisos'].beta:.2f} ({pr['permisos'].EE:.2f}). Rango de las 9 especificaciones DOLS (ipv, sin tendencia): iniciadas {ranges.loc['visados','min']:.2f}-{ranges.loc['visados','max']:.2f},
   terminadas {ranges.loc['terminadas','min']:.2f}-{ranges.loc['terminadas','max']:.2f}, permisos {ranges.loc['permisos','min']:.2f}-{ranges.loc['permisos','max']:.2f}.
   Son varias veces el 0,45 del BdE, pero **no son comparables en concepto** (ver contraste) y reflejan sobre todo la co-movimiento ciclo 2008-2025 de precios y construcción.
3. **Evidencia sobre 0,45:** nuestro rango no lo valida ni lo refuta como elasticidad de la inversión residencial; con 2014T1+ la elasticidad de iniciadas es {pop['visados'].beta_DOLS:.2f} (DOLS ±1, EE {pop['visados'].EE_DOLS:.2f}), todavía alejada de 0,45.

## 1. Déficit acumulado 2021-2025

Definición (decisiones.md, F4): déficit = Σ(Δhogares − terminadas), en viviendas; positivo = faltan viviendas. `hogares_epa` está en miles y se multiplica por 1.000.
**Corrección del cambio de 2021 (documentada):** la EPA cambia de definición de hogar y de factores de elevación en 2021T1 (`quiebre_epa_2021`); el Δ de 2021T1 de la serie es {dq_raw.loc[Pd('2021Q1','Q')]:,.0f} hogares (salto de nivel, no creación de hogares).
Principal: Δ2021T1 := media de Δ en 2020T2, 2020T3, 2020T4 y 2021T2 = {media_adj:,.0f}. Variante (a'): Δ2021T1 = 0. La serie sin corregir se da solo como referencia (a'').

### Tabla por año (principal)

{tm(tab.round(0), ",.0f")}
### Variantes

{tm(dfv.round(1).drop(columns=['nota']), ",.1f", index=False)}
- (b) ECP 60131 existe desde 2021T1: el primer Δ es 2021T2, así que 2021 solo tiene 3 trimestres. Se da el periodo consistente (2021T2-2025T4, con terminadas de los mismos trimestres) y una versión 'anualizada' que imputa Δ2021T1 con la media de los Δ ECP de 2021T2-T4: la imputación es nuestra, no un dato.
- (c) Δparque MIVAU anual (31-dic) − Δhogares EPA corregida; el parque incluye secundarias y vacías, y su Δ supera a las terminadas libres en 10.000-16.000 viviendas/año (tabla `parque_vs_terminadas`), consistente con protegidas y otros ajustes (no cuantificado: no hay protegidas en raw).
- (d) **Protegidas:** `data/raw/mivau_*` solo contiene tablas de vivienda LIBRE (iniciadas 32100500, terminadas 32101000); no hay protegidas, así que no se han podido añadir. Las terminadas totales serían mayores y el déficit principal una cota superior en esa magnitud.

### Contraste con el Banco de España (sin ajustar)

{tm(bde.round(2), ",.4g", index=False)}
Diferencias, documentadas y no ajustadas:
- **Concepto de terminadas:** MIVAU libres ({t25.terminadas:,.0f} en 2025) frente a 92.000 del BdE (la fuente del BdE no se ha verificado aquí; posiblemente incluye protegidas u otra fuente).
- **Fuente de hogares:** EPA corregida frente a la que use el BdE (creación neta 2025: {t25.delta_hogares:,.0f} frente a 240.000). Con ECP el déficit baja a {ecp.deficit:,.0f} para 2021T2-2025T4, más cerca de 750.000, pero con un trimestre menos.
- **Periodo:** el IEF (700.000) usa datos del primer semestre de 2025; 2021T1 no es comparable entre fuentes.
- La corrección de 2021 pesa {a1.deficit - araw.deficit:,.0f} viviendas: sin ella el déficit sería {araw.deficit:,.0f} (por debajo de 750.000); no se usa como principal porque incorpora un salto metodológico, y no se ajusta hacia el BdE.
- Un 'déficit en niveles' requiere un equilibrio inicial; aquí solo se da el flujo acumulado desde 2021.

### Serie larga (contexto)

`serie_larga_desequilibrio.csv/png`: desequilibrio anual Δhogares − terminadas (2008+) y Δhogares − Δparque (2003+). Los acumulados desde 2008 y desde 2014 son **escenarios con equilibrio supuesto en el año anterior (2007 / 2013)**, no estimaciones; ver columnas `ESCENARIO_*`.

## 2. Elasticidad de la oferta

Muestra común {SAMP[0]}-{SAMP[-1]} (N={pr['visados'].n}; la impone el retardo máximo del precio, 8 trimestres, y ±2 adelantos/retardos; se excluyen 2016T2 y 2017T2 sin iniciadas en las tres variables dependientes). Precio real = ln IPV − ln deflactor; costes reales = ln costes − ln deflactor; tipo hipotecario real; dummies trimestrales. Principales declaradas antes de estimar: k=4 (iniciadas, permisos), k=8 (terminadas).

### DOLS (tabla completa en `dols_resultados.csv`)

{tm(dols_tab[(dols_tab.precio=='ipv')][['dep','k','tendencia','beta','EE','p','beta_costes','beta_tipo','n','r2_adj','rmse_1paso']], ".3g", index=False)}
Robustez con valor tasado real: ver `dols_resultados.csv` (precio='tasado'); coeficientes mayores (iniciadas {g(dols_tab, dep='visados', k=4, precio='tasado').beta:.2f}). Muestra larga de permisos (2003T4+, tasado real): {long_tab.beta.min():.2f}-{long_tab.beta.max():.2f}.
`rmse_1paso` = error de predicción a un paso con regresores efectivos (ventana expansiva desde 2018T1): es condicional, no fuera de muestra genuino.

### ECM

{tm(ecm_tab[['dep','k','ect','EE_ect','p_ect','dP_corto','EE_dP','p_dP','n','r2_adj','DW']], ".3g", index=False)}
La velocidad de ajuste (ect) es negativa en todas; para iniciadas con k=4 no es significativa (p={g(ecm_tab, dep='visados', k=4).p_ect:.2f}).

### IV (2SLS, HAC 4) - desplazadores de demanda

Instrumentos: ln ocupados, ln pob_extranj, ln renta real del hogar, retardados max(k,4) trimestres; 3 instrumentos para 1 endógena. F de primera etapa robusta; J de Hansen con pesos HAC.
{tm(iv_tab[['dep','k','forma','beta','EE','p','F1','J_p','n','tendencia']], ".3g", index=False)}
Lectura: en niveles, la F es alta (≥28), pero las tres variables están tendenciales (probable regresión espuria de primera etapa) y con tendencia el J rechaza en iniciadas. En Δ4, la elasticidad de iniciadas cae a {prd['visados'].beta:.2f} (EE {prd['visados'].EE:.2f}, no significativa) con F1={prd['visados'].F1:.1f}-{iv_tab[(iv_tab.forma=='d4')&(iv_tab.dep=='visados')].F1.max():.1f}.
**Exclusión (argumentación):** ocupados, población extranjera y renta desplazan la demanda de vivienda, pero también afectan directamente a la construcción (empleo y mano de obra del sector, crédito, costes). Por eso, aunque F≥10 y J no rechace, la identificación es **solo condicional a una exclusión discutible** y los instrumentos son de la misma familia (J con poca potencia). No se afirma causalidad.

### Cointegración de la ecuación de iniciadas (los tres contrastes)

{tm(cdf[['sistema','N','EG_t','EG_p','J_traza0','J_cv95','J_rango_traza','ARDL_F','ARDL_I0_5','ARDL_I1_5','n_rechazos','decision']], ".3g", index=False)}
Regla de decisiones.md: se exige ≥2 de 3. Iniciadas k=0: 3/3; k=2: 2/3; **k=4 (principal): 1/3, evidencia mixta** (ARDL en zona inconclusa). Terminadas k=8: evidencia mixta; permisos k=4: sin cointegración. Por tanto la relación de largo plazo de DOLS **no está respaldada de forma robusta** para la especificación principal. Johansen sin dummies estacionales; para iniciadas se interpolaron 2 huecos solo en estos contrastes.

### Diagnósticos (modelos principales, DOLS)

{diag_txt}. Tabla completa en `diagnosticos.csv`. Chow/Bai-Perron (ecuación estática, `chow.csv`, `bai_perron.csv`): rechazo de estabilidad en 2014T1 en las tres (p<0,01) y Bai-Perron fecha quiebres en 2013T1 y 2014T1 (permisos) y 2018-2022; el quiebre de 2008 (colapso) queda en el arranque de la muestra, y la submuestra 2014T1+ se presenta aparte.

## 3. Contraste con el BdE (0,45)

Referencia: BdE, Informe Anual 2025, p. 156: "España presentaría una elasticidad de la oferta a largo plazo aproximadamente de 0,45 ..." (cota superior de la respuesta actual), basada en Caldera y Johansson (2013) y Cavalleri, Cournède y Özsöğüt (2019): **ambas NO VERIFICADAS** (no comprobadas de forma independiente).

| Principal | OLS estático | DOLS ±2 | IV niveles (F1; J p) | IV Δ4 | DOLS ±1 2014T1+ |
|---|---|---|---|---|---|
""" + "\n".join(
    f"| {d_} k={PRINCIPAL[d_]} | {pro[d_].beta:.2f} ({pro[d_].EE:.2f}) | {pr[d_].beta:.2f} ({pr[d_].EE:.2f}) | {pri[d_].beta:.2f} ({pri[d_].EE:.2f}; {pri[d_].F1:.0f}; {pri[d_].J_p:.2f}) | {prd[d_].beta:.2f} ({prd[d_].EE:.2f}) | {pop[d_].beta_DOLS:.2f} ({pop[d_].EE_DOLS:.2f}) |"
    for d_ in PRINCIPAL) + f"""

(EE HAC entre paréntesis.) Tabla completa con IC95 y p de H0: β=0,45 en `contraste_bde.csv`; figura `elasticidades_vs_bde.png`.
Por qué no son directamente comparables: (i) el BdE habla de la elasticidad de la **inversión residencial** (stock/flujo agregado) a precios reales de **largo plazo** entre países; la nuestra es la de **viviendas libres iniciadas** (un flujo muy volátil, cero en ciclos bajos) al precio real retardado; (ii) las iniciadas de 2008-2013 se desploman y recuperan junto con el precio, lo que mecánicamente da elasticidades altas en logs; (iii) los permisos son un índice (2021=100) y las terminadas un flujo con retardo de obra; (iv) los regresores (precio real, costes reales, tipo real) no coinciden con la especificación de los trabajos citados (no verificados). **Quiebre 2008/2014:** estimar desde 2014T1 reduce la elasticidad de terminadas ({pop['terminadas'].beta_DOLS:.2f}) y aumenta la de iniciadas/permisos en OLS/IV; los resultados son sensibles a la submuestra.

### Corrección por búsqueda

Se registraron **{N_TOTAL} modelos** en `output/registro_busqueda_f4.csv` ({nfam} en la familia 'elasticidad' del precio retardado). Con H0: β=0 sobre esos {nfam} coeficientes, {n_sig_holm} siguen significativos tras Holm y {bonf_n} tras Bonferroni con N total={N_TOTAL}. Esta corrección controla la búsqueda pero no la sensibilidad de signo/magnitud: el coeficiente va de {fam.coef_interes.min():.2f} a {fam.coef_interes.max():.2f} (incluidos los del panel con efectos de tiempo, que son negativos o nulos). Tabla: `correccion_busqueda.csv`. No se calculó Romano-Wolf.

## 4. Panel CCAA (robustez)

Δ4 ln (terminadas / iniciadas) por CCAA sobre Δ4 ln IPV CCAA retardado (0, 4, 8 trimestres); EE cluster por CCAA y Driscoll-Kraay (bandwidth 4); Extremadura sin terminadas (16 CCAA).
{tm(pan_tab[['dep','lag_trim','efectos','beta','EE_cluster','p_cluster','EE_DK','p_DK','n','CCAA']], ".3g", index=False)}
Con efectos de tiempo (que absorben el ciclo nacional) la asociación desaparece o cambia de signo (salvo contemporánea); con solo FE de CCAA es positiva y significativa. **La asociación positiva del agregado nacional procede del ciclo común, no de diferencias entre CCAA.** (Con 16-17 clusters no se hizo wild bootstrap; ver problemas abiertos.)

## Nivel de evidencia

- OLS/DOLS/ECM: **asociación** de largo plazo (cointegración mixta para la especificación principal) - no es una elasticidad estructural de oferta.
- IV: se informa F1 y J; en niveles todos pasan F≥10 y la mayoría J, pero la exclusión es discutible y la primera etapa en niveles es probablemente espuria por tendencias; en Δ4 el IV de iniciadas no es significativo. **No se afirma elasticidad identificada.**
- Déficit: aritmética contable con supuestos explícitos; sensible a la fuente de hogares (rango {min(ecp.deficit, a0.deficit, cpk.deficit, a1.deficit):,.0f}-{max(ecp.deficit, a0.deficit, cpk.deficit, a1.deficit):,.0f} en las variantes con corrección).

## Problemas abiertos

1. Sin viviendas protegidas en raw: las terminadas totales y el déficit no son directamente comparables con el BdE.
2. Fuente de hogares/terminadas del BdE no verificada; no se puede explicar la diferencia de ~{a1.deficit - 750000:,.0f} con certeza.
3. Caldera-Johansson (2013) y Cavalleri et al. (2019): NO VERIFICADAS; la cifra 0,45 solo está respaldada por la cita literal del IA 2025.
4. Elasticidades de niveles muy altas y sensibles al periodo (colapso 2008-2013): interpretar con cautela; falta una especificación con stock de vivienda/suelo y restricciones regulatorias.
5. Sin wild cluster bootstrap en el panel (solo cluster y DK); instrumentos de la misma familia.
6. Johansen sin dummies estacionales; 2 huecos de iniciadas interpolados solo en los contrastes de cointegración.
7. Parque MIVAU: estimación derivada, parcialmente mecánica con las terminadas; sin dato de 2026.
"""
(OUT / "resumen_f4.md").write_text(txt)
print("OK", round(time.time() - T0, 1), "s")
