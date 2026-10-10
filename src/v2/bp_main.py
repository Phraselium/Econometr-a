"""Rama BP (política de vivienda): H5 (confirmatoria, tope de rentas catalán), preparación de H6,
exploratorio descriptivo (RDL 7/2019, Ley 12/2023) y diagnóstico de ajuste frente al AR(4).

Uso: python src/v2/bp_main.py [--smoke]   (smoke: 10 donantes, B=50 -> output/v2/BP/smoke/)
Datos SOLO vía v2_common.load (holdout.load_train). NO llama a holdout.evaluate.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bp_h6_sellado as h6  # noqa: E402
import bp_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402
from econ_utils import Registry, holm  # noqa: E402

warnings.filterwarnings("ignore")
SMOKE = "--smoke" in sys.argv
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v2" / "BP" / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)
B = 50 if SMOKE else 1000
SEED = vc.SEED
reg = Registry(OUT / "registro.csv")

TRATADAS = ["08", "17", "25", "43"]
SELLADAS = ["11", "16", "45"]
Q = [f"{y}Q{q}" for y in range(2016, 2024) for q in range(1, 5)]
QI = {q: i for i, q in enumerate(Q)}
PRE = np.arange(QI["2016Q1"], QI["2020Q3"] + 1)          # 19 trimestres
POST1 = np.arange(QI["2020Q4"], QI["2022Q1"] + 1)        # 6 trimestres: tope vigente (pre-registro)
POST2 = np.arange(QI["2022Q2"], QI["2023Q4"] + 1)        # 7 trimestres: tras la anulación (STC 37/2022)
PRE_E = np.arange(QI["2016Q1"], QI["2018Q3"] + 1)        # placebo en el tiempo: pre 2016Q1-2018Q3
POST_F = np.arange(QI["2018Q4"], QI["2020Q3"] + 1)       # fecha falsa 2018Q4, post falso hasta 2020Q3


def csv(df, name):
    df.to_csv(OUT / name, index=False, float_format="%.8g")


def log(modelo, formula, ini, fin, n, coef, p, notas=""):
    reg.log("H5" if modelo.startswith("H5") else "BP", modelo, formula, ini, fin, n, np.nan, np.nan, np.nan,
            coef_interes=coef, p_interes=p, notas=notas)


# ------------------------------------------------------------------ datos
pan = vc.load("panel_prov_q")
pan["trimestre"] = pan["trimestre"].astype(str)
pan["cod_prov"] = pan["cod_prov"].astype(str)
assert pan["trimestre"].max() <= vc.Q_TRAIN_FIN
niv = np.log(pan.pivot(index="cod_prov", columns="trimestre", values="ipc_alquiler"))
d4 = niv - niv.shift(4, axis=1)
unidades = sorted(niv.index)
assert not set(SELLADAS) & set(unidades)
donantes = [u for u in unidades if u not in TRATADAS]
if SMOKE:
    donantes = sorted(np.random.default_rng(SEED).choice(donantes, 10, replace=False).tolist())
assert len(donantes) == (10 if SMOKE else 45), len(donantes)
units = TRATADAS + donantes
tr_idx, co_idx = np.arange(4), np.arange(4, len(units))
Y = {"ln_ipc_alquiler": niv.loc[units, Q].values, "d4_ln_ipc_alquiler": d4.loc[units, Q].values}
assert np.isfinite(Y["ln_ipc_alquiler"]).all() and np.isfinite(Y["d4_ln_ipc_alquiler"]).all()
subsets = bl.draws_subsets(len(co_idx), 4, B)
subsets1 = bl.draws_subsets(len(co_idx), 1, len(co_idx))      # cada donante como tratado (exacto)
print(f"donantes={len(donantes)} B={len(subsets)} SMOKE={SMOKE}")

# ------------------------------------------------------------------ H5: efectos principales y robustez
filas, pesos, gaps = [], [], {}
VENT = {"post1_2020Q4_2022Q1": POST1, "post2_2022Q2_2023Q4": POST2}
res_main = {}
for out_name, y in Y.items():
    for vn, post in VENT.items():
        r = bl.run_design(y, tr_idx, co_idx, PRE, post, subsets)
        res_main[(out_name, vn)] = r
        for m, v in r.items():
            filas.append(dict(resultado=out_name, ventana=vn, metodo=m, tau=v["tau"], se_placebo=v["se_placebo"],
                              ic95_inf=v["ic95"][0], ic95_sup=v["ic95"][1], p_perm_dos=v["p_dos"],
                              p_perm_una=v["p_una"], B=v["B"], n_tratadas=4, n_donantes=len(co_idx),
                              T_pre=len(PRE), T_post=len(post)))
            log(f"H5_{m}_{out_name}_{vn}", f"{out_name} ~ {m}(tratada x post)", Q[PRE[0]], Q[post[-1]],
                len(units) * (len(PRE) + len(post)), v["tau"], v["p_dos"],
                f"EXPLORATORIO/CONFIRMATORIA; se_placebo={v['se_placebo']:.5g}; B={v['B']}")
        s = r["sdid"]
        # jackknife (secundario, pesos fijos)
        jk = bl.jackknife_se(y, tr_idx, co_idx, s["omega"], s["lam"], PRE, post)
        filas[-3].update(se_jackknife=jk)
        for u, w in zip(donantes, s["omega"]):
            pesos.append(dict(resultado=out_name, ventana=vn, donante=u, omega=w))
        gaps[(out_name, vn)] = s
tab = pd.DataFrame(filas)

# DiD con efectos fijos de provincia y trimestre, EE cluster por provincia (robustez)
import statsmodels.api as sm  # noqa: E402

for out_name, y in Y.items():
    for vn, post in VENT.items():
        cols = list(PRE) + list(post)
        rows = [(units[i], Q[t], y[i, t], float(i in tr_idx and t in post)) for i in range(len(units)) for t in cols]
        d = pd.DataFrame(rows, columns=["u", "q", "y", "D"])
        X = pd.concat([d[["D"]], pd.get_dummies(d["u"], drop_first=True, dtype=float),
                       pd.get_dummies(d["q"], drop_first=True, dtype=float)], axis=1)
        X = sm.add_constant(X)
        m = sm.OLS(d["y"], X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["u"])[0]}, use_t=True)
        b, se = float(m.params["D"]), float(m.bse["D"])
        tau_did = float(tab[(tab.resultado == out_name) & (tab.ventana == vn) & (tab.metodo == "did")].tau.iloc[0])
        assert abs(b - tau_did) < 1e-9, (b, tau_did)
        filas.append(dict(resultado=out_name, ventana=vn, metodo="did_FE_cluster", tau=b, se_placebo=se,
                          ic95_inf=b - 2.01 * se, ic95_sup=b + 2.01 * se, p_perm_dos=float(m.pvalues["D"]),
                          p_perm_una=np.nan, B=0, n_tratadas=4, n_donantes=len(co_idx), T_pre=len(PRE),
                          T_post=len(post)))
        log(f"H5_did_FE_cluster_{out_name}_{vn}", f"{out_name} ~ D + FE prov + FE trim (cluster prov)",
            Q[PRE[0]], Q[post[-1]], len(d), b, float(m.pvalues["D"]),
            "p analítico t(G-1) con solo 4 tratadas: poco fiable; usar p de permutación")
tab = pd.DataFrame(filas)

# FDR interno (m=6 por ventana: 3 métodos x 2 resultados), Holm y Benjamini-Hochberg


def bh(p):
    k = list(p)
    v = np.array([p[x] for x in k])
    o = np.argsort(v)
    m = len(v)
    adj = np.empty(m)
    run = 1.0
    for r in range(m - 1, -1, -1):
        run = min(run, v[o[r]] * m / (r + 1))
        adj[o[r]] = run
    return dict(zip(k, adj))


tab["p_holm_m6"] = np.nan
tab["p_bh_m6"] = np.nan
for vn in VENT:
    sel = tab[(tab.ventana == vn) & tab.metodo.isin(["sdid", "sc", "did"])]
    ps = {i: r.p_perm_dos for i, r in sel.iterrows()}
    for i, a in holm(ps).items():
        tab.loc[i, "p_holm_m6"] = a
    for i, a in bh(ps).items():
        tab.loc[i, "p_bh_m6"] = a
csv(tab, "h5_efectos.csv")
csv(pd.DataFrame(pesos), "h5_pesos_donantes.csv")

# ------------------------------------------------------------------ pretendencias: event study
ev_rows, ev_stats = [], []
for out_name, y in Y.items():
    ev = bl.evento_design(y, tr_idx, co_idx, PRE, POST1, subsets)
    for m, v in ev.items():
        for t in range(len(Q)):
            ev_rows.append(dict(resultado=out_name, metodo=m, periodo=Q[t],
                                fase="pre" if t in PRE else ("tope" if t in POST1 else "post_anulacion"),
                                e=v["e"][t], banda_inf=v["lo"][t], banda_sup=v["hi"][t]))
        ev_stats.append(dict(resultado=out_name, metodo=m, rms_pre=v["rms_pre"],
                             pendiente_pre_anual=v["slope_pre_anual"], p_rms=v["p_rms"], p_pendiente=v["p_slope"],
                             B=v["B"], nota=("ajuste dentro de muestra" if m == "sdid" else "pesos uniformes, sin ajuste")))
        log(f"H5_pretendencias_{m}_{out_name}", "event study 2016Q1-2020Q3 (brecha centrada en media pre)",
            Q[PRE[0]], Q[PRE[-1]], len(PRE), v["slope_pre_anual"], v["p_slope"],
            f"p_rms={v['p_rms']:.4f}; permutación B={v['B']}")
csv(pd.DataFrame(ev_rows), "h5_event_study.csv")
csv(pd.DataFrame(ev_stats), "h5_pretendencias.csv")

# ------------------------------------------------------------------ placebo en el tiempo (fecha falsa 2018Q4)
pt = []
for out_name, y in Y.items():
    r = bl.run_design(y, tr_idx, co_idx, PRE_E, POST_F, subsets)
    for m, v in r.items():
        pt.append(dict(resultado=out_name, metodo=m, tau=v["tau"], se_placebo=v["se_placebo"],
                       p_perm_dos=v["p_dos"], B=v["B"], pre="2016Q1-2018Q3", post_falso="2018Q4-2020Q3"))
        log(f"H5_placebo_tiempo_{m}_{out_name}", f"{out_name}: fecha falsa 2018Q4", Q[PRE_E[0]], Q[POST_F[-1]],
            len(units) * (len(PRE_E) + len(POST_F)), v["tau"], v["p_dos"], "placebo en el tiempo (debe ser nulo)")
csv(pd.DataFrame(pt), "h5_placebo_tiempo.csv")

# ------------------------------------------------------------------ placebo en el espacio: cada donante como tratado
esp, dist_rows = [], []
for out_name, y in Y.items():
    for vn, post in VENT.items():
        # (a) cada tratada sola frente a los donantes; permutación exacta con cada donante como único tratado
        for i, u in enumerate(TRATADAS):
            r = bl.run_design(y, [i], co_idx, PRE, post, subsets1, metodos=("sdid",))["sdid"]
            esp.append(dict(resultado=out_name, ventana=vn, unidad=u, tau=r["tau"], p_perm_dos=r["p_dos"],
                            p_perm_una=r["p_una"], n_placebos=r["B"]))
            log(f"H5_prov_{u}_{out_name}_{vn}", f"{out_name}: SDiD, tratada {u} sola", Q[PRE[0]], Q[post[-1]],
                len(units) * (len(PRE) + len(post)), r["tau"], r["p_dos"], "exploratorio; permutación exacta (45 donantes)")
        # (b) distribución del agregado (4 donantes aleatorios) para la figura/inspección
        s = res_main[(out_name, vn)]["sdid"]
        for b_, t_ in enumerate(s["dist"]):
            dist_rows.append(dict(resultado=out_name, ventana=vn, b=b_, tau_placebo=t_))
csv(pd.DataFrame(esp), "h5_por_provincia_placebo_espacio.csv")
csv(pd.DataFrame(dist_rows), "h5_placebos_espacio_distribucion.csv")

# ------------------------------------------------------------------ ajuste previo vs AR(4) de panel (diagnóstico)
y = Y["ln_ipc_alquiler"]
fitE = bl.sdid(y[co_idx], y[tr_idx].mean(0), PRE_E, POST_F, n_tr=4)
gapE = fitE["gap"]
e_syn = (gapE - np.r_[[np.nan] * 4, gapE[:-4]])[POST_F]               # Δ4 de la brecha, objetivos 2018Q4-2020Q3
per_all = sorted(pan["trimestre"].unique())
posL = per_all.index("2018Q3")
orig = [per_all.index(q) for q in ("2017Q4", "2018Q1", "2018Q2", "2018Q3", "2018Q4", "2019Q1", "2019Q2", "2019Q3")]
pa = pan[pan.cod_prov.isin(units)]
ar = vc.panel_ar4(pa, "ipc_alquiler", "cod_prov", 4, splits=[(np.arange(0, posL + 1), np.array(orig))])
art = ar[ar.unidad.isin(TRATADAS)].groupby("periodo_obj")[["y_real", "y_pred"]].mean()
e_ar = (art["y_real"] - art["y_pred"]).values
assert len(e_ar) == len(e_syn) == 8, (len(e_ar), len(e_syn))
dm = vc.dm_hln(e_ar, e_syn, 4)
fit_pre = bl.sdid(y[co_idx], y[tr_idx].mean(0), PRE, POST1, n_tr=4)
sc_pre = bl.sc(y[co_idx], y[tr_idx].mean(0), PRE, POST1)
g_s, g_c = fit_pre["gap"][PRE], sc_pre["gap"][PRE]
d4g = lambda g: (g - np.r_[[np.nan] * 4, g[:-4]])[PRE[4:]]    # noqa: E731
ajuste = pd.DataFrame([
    dict(diagnostico="pseudo-OOS (pesos <=2018Q3, objetivos 2018Q4-2020Q3), Δ4 ln IPC alquiler, media de las 4 tratadas",
         rmse_sintetico_sdid=float(np.sqrt(np.mean(e_syn ** 2))), rmse_AR4_panel=float(np.sqrt(np.mean(e_ar ** 2))),
         dm_hln_AR4_menos_sint=dm["DM"], p=dm["p"], n=8,
         nota="el sintético usa donantes contemporáneos (nowcast); el AR(4) solo información pasada: no es un duelo de predicción"),
    dict(diagnostico="en muestra 2016Q1-2020Q3: RMSE de la brecha de nivel (centrada) SDiD",
         rmse_sintetico_sdid=float(np.sqrt(np.mean((g_s - g_s.mean()) ** 2))), rmse_AR4_panel=np.nan,
         dm_hln_AR4_menos_sint=np.nan, p=np.nan, n=len(PRE), nota="ajuste de ω dentro de muestra"),
    dict(diagnostico="en muestra 2016Q1-2020Q3: RMSE de la brecha de nivel SC (Abadie)",
         rmse_sintetico_sdid=float(np.sqrt(np.mean(g_c ** 2))), rmse_AR4_panel=np.nan,
         dm_hln_AR4_menos_sint=np.nan, p=np.nan, n=len(PRE), nota="ajuste de ω dentro de muestra"),
    dict(diagnostico="en muestra 2017Q1-2020Q3: RMSE de la brecha Δ4 SDiD",
         rmse_sintetico_sdid=float(np.sqrt(np.mean(d4g(fit_pre["gap"]) ** 2))), rmse_AR4_panel=np.nan,
         dm_hln_AR4_menos_sint=np.nan, p=np.nan, n=len(PRE) - 4, nota="ajuste de ω dentro de muestra")])
csv(ajuste, "h5_ajuste_vs_ar4.csv")
log("H5_diag_ajuste_vs_AR4", "RMSE sintético vs AR(4) de panel", Q[PRE_E[0]], Q[POST_F[-1]], 8,
    float(np.sqrt(np.mean(e_syn ** 2))), dm["p"], f"rmse_AR4={np.sqrt(np.mean(e_ar ** 2)):.5g}; diagnóstico")

# ------------------------------------------------------------------ figuras
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

evdf = pd.DataFrame(ev_rows)
fig, axs = plt.subplots(1, 2, figsize=(12, 4), sharey=False)
for ax, out_name in zip(axs, Y):
    for m, c in (("sdid", "C0"), ("did", "C3")):
        s = evdf[(evdf.resultado == out_name) & (evdf.metodo == m)]
        ax.plot(range(len(s)), s.e, color=c, label=m)
        ax.fill_between(range(len(s)), s.banda_inf, s.banda_sup, color=c, alpha=0.12)
    ax.axvline(QI["2020Q4"] - 0.5, color="k", ls="--")
    ax.axvline(QI["2022Q2"] - 0.5, color="gray", ls=":")
    ax.axhline(0, color="k", lw=0.5)
    ax.set_xticks(range(0, len(Q), 4))
    ax.set_xticklabels(Q[::4], rotation=45)
    ax.set_title(out_name)
    ax.legend()
fig.suptitle("H5: brecha tratadas - sintético (banda 95% de permutación puntual); EXPLORATORIO/diagnóstico")
fig.tight_layout()
fig.savefig(OUT / "h5_event_study.png", dpi=110, metadata={"Software": None})
plt.close(fig)

# ------------------------------------------------------------------ exploratorio descriptivo nacional
nac = vc.load("nacional_q_v2")
nac["trimestre"] = nac["trimestre"].astype(str)
n = nac[nac.trimestre.between("2016Q1", vc.Q_TRAIN_FIN)].set_index("trimestre")
d4n = (n["ln_ipc_alquiler"] - n["ln_ipc_alquiler"].shift(4)).dropna()
med_prov = d4.loc[unidades].median(axis=0)
desc = pd.DataFrame({"d4_ln_ipc_alquiler_nacional": d4n, "mediana_provincial_d4": med_prov})
desc = desc.loc["2017Q1":]
csv(desc.reset_index().rename(columns={"index": "trimestre"}), "exploratorio_descriptivo_nacional.csv")


def ventana(a, b):
    return float(desc.loc[a:b, "d4_ln_ipc_alquiler_nacional"].mean())


expl = pd.DataFrame([
    dict(evento="RDL 7/2019 (vigor 2019-03-06)", pre="2017Q1-2018Q4", media_pre=ventana("2017Q1", "2018Q4"),
         post="2019Q2-2020Q1", media_post=ventana("2019Q2", "2020Q1"), nivel="DESCRIPTIVO",
         nota="nacional, sin grupo de control, sin inferencia; COVID a partir de 2020Q1"),
    dict(evento="Ley 12/2023 (vigor 2023-05-26), índice de referencia y topes a la actualización (3 % en 2024: DF 6)",
         pre="2021Q3-2022Q4", media_pre=ventana("2021Q3", "2022Q4"), post="2023Q3-2024Q2",
         media_post=ventana("2023Q3", "2024Q2"), nivel="DESCRIPTIVO",
         nota="nacional, sin control; coincide con alza de tipos/inflación (P4) y con el tope de actualización del RDL 6/2022; "
              "no se atribuye a la ley")])
csv(expl, "exploratorio_descriptivo_eventos.csv")
for _, r in expl.iterrows():
    log("EXPL_" + r.evento[:12].replace(" ", "_"), "media Δ4 ln IPC alquiler nacional, post - pre", r.pre, r.post, 0,
        r.media_post - r.media_pre, np.nan, "DESCRIPTIVO; sin inferencia")

# ------------------------------------------------------------------ preparación H6 (solo entrenamiento)
prep = h6.preparar_entrenamiento(pan, B=B, smoke=SMOKE)
(OUT / "h6_preparacion.json").write_text(json.dumps(prep, indent=2, ensure_ascii=False, default=float))
log("H6_preparacion", "ajuste de pesos con datos <=2023Q4 (sin efecto: la ventana de efecto es sellada)", "2016Q1",
    "2023Q4", prep["n_donantes"], np.nan, np.nan, "solo preparación; no se evalúa ningún efecto")

# ------------------------------------------------------------------ resultado.json
e = lambda o, v, m: tab[(tab.resultado == o) & (tab.ventana == v) & (tab.metodo == m)].iloc[0]   # noqa: E731
p1 = e("ln_ipc_alquiler", "post1_2020Q4_2022Q1", "sdid")
p2 = e("ln_ipc_alquiler", "post2_2022Q2_2023Q4", "sdid")
evs = pd.DataFrame(ev_stats)
ev_l = evs[(evs.resultado == "ln_ipc_alquiler") & (evs.metodo == "sdid")].iloc[0]
ev_d = evs[(evs.resultado == "ln_ipc_alquiler") & (evs.metodo == "did")].iloc[0]
pl = pd.DataFrame(pt)
pl_l = pl[(pl.resultado == "ln_ipc_alquiler") & (pl.metodo == "sdid")].iloc[0]
pretrend_ok = bool(ev_l.p_rms > 0.05 and ev_l.p_pendiente > 0.05)
placebo_ok = bool(pl_l.p_perm_dos > 0.05)
main_ok = bool(p1.tau < 0 and p1.p_perm_dos < 0.05)
# Escala: CAUSAL exige además Holm-7 y submuestras (BS); aquí, con tests superados, solo "candidata".
nivel_texto = ("candidata a CAUSAL (pendiente de Holm-7 y submuestras en BS)" if (main_ok and pretrend_ok and placebo_ok)
               else "EXPLORATORIO")
nivel = "EXPLORATORIO"        # nivel válido de la escala hasta que BS aplique Holm-7
diag = dict(pretendencias_sdid_p_rms=float(ev_l.p_rms), pretendencias_sdid_p_pendiente=float(ev_l.p_pendiente),
            pretendencias_did_uniforme_p_rms=float(ev_d.p_rms), pretendencias_did_uniforme_p_pendiente=float(ev_d.p_pendiente),
            placebo_tiempo_2018Q4_tau=float(pl_l.tau), placebo_tiempo_2018Q4_p=float(pl_l.p_perm_dos),
            p_permutacion_dos_colas_post1=float(p1.p_perm_dos), p_permutacion_una_cola_post1=float(p1.p_perm_una),
            pretendencias_ok=pretrend_ok, placebo_tiempo_ok=placebo_ok, efecto_negativo_y_p_menor_005=main_ok,
            tau_post2_anulacion=float(p2.tau), p_permutacion_post2=float(p2.p_perm_dos),
            sc_tau_post1=float(e("ln_ipc_alquiler", "post1_2020Q4_2022Q1", "sc").tau),
            did_tau_post1=float(e("ln_ipc_alquiler", "post1_2020Q4_2022Q1", "did").tau),
            tau_d4_sdid_post1=float(e("d4_ln_ipc_alquiler", "post1_2020Q4_2022Q1", "sdid").tau),
            p_d4_sdid_post1=float(e("d4_ln_ipc_alquiler", "post1_2020Q4_2022Q1", "sdid").p_perm_dos),
            jackknife_se_post1=float(p1.get("se_jackknife", np.nan)), B=B,
            qp_no_convergidos=int(bl.NO_CONV[0]), h6="preparación solo; evaluar_H6 NO ejecutada (muestra sellada intacta)")
vc.resultado_json(
    OUT / "resultado.json", rama="BP",
    pregunta="H5: ¿redujo el tope de rentas catalán (Ley 11/2020, vigente 2020Q4-2022Q1) el IPC de alquiler provincial?",
    datos="panel_prov_q (entrenamiento), ipc_alquiler provincial (agregado_media, sin interpolación); 4 tratadas (08,17,25,43) "
          "y 45 donantes no catalanas no selladas; 2016Q1-2023Q4",
    N={"tratadas": 4, "donantes": len(co_idx), "trimestres": len(Q)},
    metodo="Synthetic DiD (implementación propia, Arkhangelsky et al. 2021); EE y p por permutación espacial (4 donantes "
           "aleatorios como placebo-tratadas, B=%d); robustez SC, DiD, DiD-FE cluster" % B,
    estimacion={"efecto_medio_ln_2020Q4_2022Q1": float(p1.tau), "efecto_medio_ln_2022Q2_2023Q4": float(p2.tau)},
    ic95={"efecto_2020Q4_2022Q1": [float(p1.ic95_inf), float(p1.ic95_sup)],
          "efecto_2022Q2_2023Q4": [float(p2.ic95_inf), float(p2.ic95_sup)]},
    p_ajustado={"p_perm_dos_post1": float(p1.p_perm_dos), "holm_m6_post1": float(p1.p_holm_m6),
                "bh_m6_post1": float(p1.p_bh_m6), "holm_7_confirmatorias": "pendiente (BS)"},
    nivel_evidencia=nivel, diagnosticos=diag,
    fuera_muestra={"modelo": "no aplica a estimadores de efecto de política; diagnóstico pseudo-OOS del sintético",
                   "rmse": float(ajuste.rmse_sintetico_sdid.iloc[0]), "dm_vs_ar4": float(dm["DM"])},
    notas="Tratamiento a nivel provincial diluido (el tope solo regía en municipios de alta demanda y en contratos nuevos); "
          "el IPC mide rentas de todo el parque (stock). Sin lenguaje causal salvo que se cumplan los criterios de CAUSAL. "
          f"Nivel asignado por regla: {nivel_texto}. MDE (80 %, bilateral) H5 ≈ 0,56 % y H6 ≈ 1,7 % en ln. El IPC de alquiler mide todos los "
          "contratos vigentes mientras el tope afecta sobre todo a contratos nuevos (Jofre-Monseny, Martínez-Mazza y Segú 2023, RSUE 101, "
          "103916): un nulo no prueba ausencia de efecto. Inferencia placebo: supone unidades intercambiables; jackknife poco fiable con "
          "4 tratadas. SC sin penalización: depende de los hilos BLAS (OMP_NUM_THREADS=1).")
print("nivel:", nivel, "| tau1=%.4f p=%.3f | tau2=%.4f p=%.3f" % (p1.tau, p1.p_perm_dos, p2.tau, p2.p_perm_dos))
