"""B4 · Contribuciones por familia a la subida de precio y alquiler (triangulación, sin reestimar).

Uso: python3 src/v5/b4_run.py
Lee solo salidas ya versionadas de v2, v3 y v5 (B3, A23, R1A, R1B). Determinista, sin red, SEED=20261010.
Nada aquí es C3: las celdas son contribuciones CONTABLES o cotas, no efectos.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
OUT = ROOT / "output" / "v5" / "B4"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")

FAM = ["demografica", "renta_empleo", "financiacion_tipos", "oferta_suelo", "turismo_no_residentes", "inversion", "residuo"]
COMUNES = ["demografica", "renta_empleo", "financiacion_tipos", "oferta_suelo"]  # con dato en v2 y B3
COLS = ["2015-2019", "2019-2025", "2015-2025"]
MERC = ["compra", "alquiler_stock", "alquiler_nuevos"]
entradas = []  # una por (mercado, columna, familia, metodo)


def add(mercado, col, fam, metodo, periodo_origen, lo, hi, unidad, capa, tipo, nota, ic=None, central=None,
        fecha="", desplazada=False):
    entradas.append(dict(mercado=mercado, columna=col, familia=fam, metodo=metodo, periodo_origen=periodo_origen,
                         rango_lo=lo, rango_hi=hi, central=central, ic_lo=None if ic is None else ic[0],
                         ic_hi=None if ic is None else ic[1], unidad=unidad, capa=capa, tipo=tipo,
                         ventana_desplazada=desplazada, fecha_dato=fecha, nota=nota))
    REG.log("B4", f"{mercado}|{col}|{fam}|{metodo}", "triangulacion_sin_reestimacion", periodo_origen, "", 0,
            np.nan, np.nan, np.nan, coef_interes=central if central is not None else np.nan, notas=tipo)


# ---------------------------------------------------------------- v2 BD (temporal, M1/M2)
bd = pd.read_csv(ROOT / "output/v2/BD/contribuciones_todas.csv")
PER2 = {"2015-2019": "P2", "2019-2025": "P3-P4 (desde 2020)", "2015-2025": "P2-P4 (desde 2014)"}
VENT2 = {"2015-2019": "2014Q1-2019Q4", "2019-2025": "2020Q1-2024Q1", "2015-2025": "2014Q1-2024Q1"}
COMP2 = {"demografica": ["demografia"], "renta_empleo": ["empleo_renta"], "financiacion_tipos": ["credito_tipos_cu"],
         "oferta_suelo": ["oferta"], "residuo": ["comun_efectos_tiempo", "residuo"]}
OBS = {}
for merc, mb in (("alquiler_stock", "alquiler"), ("compra", "compra")):
    for col in COLS:
        sub = bd[(bd.mercado == mb) & (bd.periodo == PER2[col])]
        OBS[(merc, col)] = sub[sub.componente == "observado"].groupby("modelo").contrib_pp.first().mean()
        for fam, comps in COMP2.items():
            v, lo, hi = {}, [], []
            for m in ("M1", "M2"):
                s = sub[(sub.modelo == m) & sub.componente.isin(comps)]
                v[m] = s.contrib_pp.sum()
                if fam != "residuo":
                    lo.append(s.ic95_inf.iloc[0])
                    hi.append(s.ic95_sup.iloc[0])
            vals = list(v.values())
            ic = None if fam == "residuo" else (min(lo), max(hi))
            sig = (ic is not None) and (ic[0] > 0 or ic[1] < 0)
            nota = ("M1 y M2 puntuales: " + ", ".join(f"{k} {x:.2f}" for k, x in v.items()) + " pp. "
                    + ("IC95 (envolvente de M1 y M2) excluye 0. " if sig else "IC95 incluye 0. ")
                    + ("Residuo = común (efectos de tiempo+FE: tipos nacionales, regulación, expectativas) + residuo. "
                       if fam == "residuo" else "")
                    + ("Variable REAL (deflactada por IPC nacional): no comparable en nivel con precio nominal. "
                       if merc == "compra" else "Alquiler = IPC alquiler nominal (proxy de stock). "))
            add(merc, col, fam, "v2_BD_temporal", VENT2[col], min(vals), max(vals), "pp de Δln acumulado", "C4",
                "contribucion_contable", nota, ic=ic, central=float(np.mean(vals)), fecha="2024Q1",
                desplazada=True)
# turismo v2 (ventana corta VUT 2021Q3-2024Q1), solo alquiler
tur = pd.read_csv(ROOT / "output/v2/BD/turismo_ventana_2021Q3_2024Q1.csv")
st = tur[(tur.periodo == "P3-P4 (desde 2020)") & (tur.componente == "turismo")].set_index("modelo")
vals = st.contrib_pp.tolist()
add("alquiler_stock", "2019-2025", "turismo_no_residentes", "v2_BD_temporal", "2021Q3-2024Q1", min(vals), max(vals),
    "pp de Δln acumulado", "C4", "contribucion_contable",
    f"Solo VUT (no residentes sin serie temporal). Observado en la ventana: {tur[(tur.periodo=='P3-P4 (desde 2020)')&(tur.componente=='observado')].contrib_pp.iloc[0]:.2f} pp. IC95 incluye 0.",
    ic=(st.ic95_inf.min(), st.ic95_sup.max()), central=float(np.mean(vals)), fecha="2024Q1", desplazada=True)

# ---------------------------------------------------------------- v2 BV (compra real, orden y signo)
bv = pd.read_csv(ROOT / "output/v2/BV/periodos_contribuciones.csv")
MAPBV = {"demografica": ["demografia"], "renta_empleo": ["empleo_renta"],
         "financiacion_tipos": ["credito_tipos", "coste_de_uso"], "oferta_suelo": ["oferta"]}
for col, pers in (("2015-2019", ["P2_recuperacion"]), ("2019-2025", ["P3_covid", "P4_tipos"])):
    for fam, comps in MAPBV.items():
        s = bv[bv.periodo.isin(pers) & bv.familia.isin(comps)]
        v = float(s.contribucion_pp.sum())
        add("compra", col, fam, "v2_BV_modeloB", "+".join(pers), v, v, "pp de Δ4 real vs media (otra escala)", "C4",
            "contribucion_contable", "Solo orden y signo: unidad distinta a BD (desviación respecto a la media muestral; "
            "suma de periodos). Tipos = crédito + coste de uso.", central=v, fecha="2024Q2", desplazada=True)

# ---------------------------------------------------------------- B3 transversal
sh = pd.read_csv(ROOT / "output/v5/B3/tablas/shapley_R2.csv").set_index("familia")
cs = lambda f: (sh.loc[f, "cuota_tasado_pct"], sh.loc[f, "cuota_reg_pct"])  # noqa: E731
GRP = {"demografica": ["F2"], "renta_empleo": ["F1", "F5"], "financiacion_tipos": ["F7"], "oferta_suelo": ["F4"]}
for fam, fs in GRP.items():
    a = sum(cs(f)[0] for f in fs)
    b = sum(cs(f)[1] for f in fs)
    add("compra", "2015-2025", fam, "B3_transversal_Shapley", "2015-2025 (50 provincias)", min(a, b), max(a, b),
        "% del R2 entre provincias", "C4", "reparto_varianza_transversal",
        f"Familias {'+'.join(fs)}. Cuota de R2 (tasado {a:.1f} %, Registradores {b:.1f} %), no pp de la subida. "
        "El orden de Shapley no coincide entre las dos fuentes de Y1."
        + (" F4 se mide en 2021-2025 con precios: parte puede ser mecánica." if fam == "oferta_suelo" else ""),
        central=(a + b) / 2, fecha="2025T4", desplazada=False)
a = cs("F3")[0] + cs("F8")[0]
b = cs("F3")[1] + cs("F8")[1]
add("compra", "2015-2025", "turismo_no_residentes", "B3_transversal_Shapley", "2015-2025 (50 provincias)",
    min(cs("F3") + (cs("F3")[0] + cs("F8")[0], cs("F3")[1] + cs("F8")[1])),
    max(a, b), "% del R2 entre provincias", "C4", "reparto_varianza_transversal",
    "Rango: solo F3 (VUT por 1.000 viviendas, 2021) hasta F3+F8 (costa e isla, proxy geográfico). F3 no se distingue de 0 en el coeficiente.",
    central=(a + b) / 2, fecha="2025T4")
res_lo = 100 * (1 - 0.9115066991822581)
res_hi = 100 * (1 - 0.8208410390832163)
f6 = cs("F6")
add("compra", "2015-2025", "residuo", "B3_transversal_Shapley", "2015-2025 (50 provincias)", res_lo + min(f6), res_hi + max(f6),
    "% del R2 entre provincias", "C4", "reparto_varianza_transversal",
    f"1-R2 ({res_lo:.1f}-{res_hi:.1f} %) más F6 (precio inicial, convergencia; puede ser error de medida): {min(f6):.1f}-{max(f6):.1f} %.",
    central=None, fecha="2025T4")
# B3 coeficientes (señal) por Y y periodo
co = pd.read_csv(ROOT / "output/v5/B3/tablas/coeficientes_principal.csv")
FAMCOEF = {"demografica": ["F2_dlnpob", "F2_dext_pp"], "renta_empleo": ["F1_bartik", "F5_lnpibpc0", "F5_dlnpibpc"],
           "financiacion_tipos": ["F7_hip_1000hab"], "oferta_suelo": ["F4_brecha"], "turismo_no_residentes": ["F3_vut_1000viv"]}
MAPB3 = {("Y1", "P2"): ("compra", "2019-2025", "2021-2025"), ("Y2", "P1"): ("alquiler_stock", "2015-2025", "2015-2021"),
         ("Y2", "P2"): ("alquiler_stock", "2019-2025", "2021-2024")}
for (y, p), (merc, col, per) in MAPB3.items():
    for fam, cl in FAMCOEF.items():
        s = co[(co.Y == y) & (co.periodo == p) & co.coef.isin(cl)]
        sig = s[s.p_perm < 0.05]
        b = s.beta_std.abs().max() if len(sig) == 0 else sig.beta_std.abs().max()
        lo, hi = s.beta_std.min(), s.beta_std.max()
        add(merc, col, fam, "B3_transversal_coef", per, float(lo), float(hi), "beta estandarizado (DT de Y)", "C4",
            "asociacion_transversal",
            ("Significativo (p de aleatorización < 0,05 sin ajustar) en: " + ", ".join(sig.coef) + ". " if len(sig)
             else "Ningún coeficiente con p de aleatorización < 0,05 sin ajustar. ")
            + "Y2 = SERPAVI stock (AEAT), 46-47 provincias. Sin ajuste de multiplicidad aquí.",
            central=float(sig.beta_std.abs().max()) if len(sig) else 0.0, fecha="2025T4" if y == "Y1" else "2024",
            desplazada=True)

# ---------------------------------------------------------------- v3 cotas PB y R1A
pb = {x["id"]: x for x in json.load(open(ROOT / "output/v3/PB/cotas.json"))}
t = pb["B1-nac-cantidad"]
add("alquiler_stock", "2019-2025", "turismo_no_residentes", "v3_PB_cota", "2020M08-2024M08", t["sensibilidad_min"],
    t["sensibilidad_max"], "% del stock de alquiler (máximo)", "C2", "cota_superior",
    "Supuesto: cada vivienda turística nueva es una de alquiler menos (1:1), 81.771 viviendas como máximo; stock Censo 2021 constante. Cota de CANTIDAD (C2).",
    central=t["cota_superior"], fecha="2024-08", desplazada=True)
t = pb["B1-nac-precio-central"]
add("alquiler_stock", "2019-2025", "turismo_no_residentes", "v3_PB_cota_precio", "2020M08-2024M08", t["sensibilidad_min"],
    t["sensibilidad_max"], "% de alquiler (Δln) como máximo", "C4", "cota_condicional",
    "Condicional a |ε_d| de 1,0 (1,0-0,33 da 2,7-8,3 %): elasticidad sin estimación verificada para España, por eso C4.",
    central=t["cota_superior"], fecha="2024-08", desplazada=True)
for per, col in (("2014-2019", "2015-2019"), ("2020-2025", "2019-2025"), ("2014-2025", "2015-2025")):
    cu, vi = pb[f"B2-nac-cuota-{per}"], pb[f"B2-nac-viviendas-{per}"]
    pc, pa = pb[f"B2-nac-precio-compra-{per}"], pb[f"B2-nac-precio-alquiler-{per}"]
    add("compra", col, "demografica", "v3_PB_cota_inmigracion", per, 0.0, pc["cota_superior"], "% de precio (Δln) como máximo",
        "C4", "cota_condicional",
        f"Cuota máx. de la creación de hogares: {cu['cota_superior']:.1f} % (C2; 100 % = no informativa); {vi['cota_superior']:,.0f} viviendas. "
        "Precio: condicional a |ε_d|=0,33 (mínimo de la rejilla), 1 persona/hogar.", central=None, fecha="2025", desplazada=False)
    add("alquiler_stock", col, "demografica", "v3_PB_cota_inmigracion", per, 0.0, pa["cota_superior"], "% de alquiler (Δln) como máximo",
        "C4", "cota_condicional",
        "Condicional a |ε_d|=0,33; supera el alquiler observado en 2020-2025 y 2014-2025: no informativa.", fecha="2025")
b4 = pd.read_csv(ROOT / "output/v3/PB/tablas/b4_periodos.csv").set_index("periodo")
for per in ("2014-2021", "2021-2025"):
    r = b4.loc[per]
    add("compra", "2015-2025", "financiacion_tipos", "v3_PB_cota_tipos", per, float(r.dln_inv_uc_min_pct),
        float(r.dln_inv_uc_max_pct), "% de Δln(1/coste de uso) como máximo", "C4", "cota_condicional",
        f"Observado en el periodo: Δln precio tasado {r.dlnP_tasado_pct:.1f} %. "
        + ("Signo contrario: los tipos suben y el precio también." if bool(r.signo_contrario) else "Mismo signo que el precio.")
        + " Dependencia del suelo de coste de uso; componente en alquiler fijada en 0 por supuesto.", fecha="2025", desplazada=True)
r1a = json.load(open(ROOT / "output/v5/R1A/resultado.json"))
e = r1a["estimacion"]
ic = r1a["ic95"]
add("compra", "2015-2025", "turismo_no_residentes", "R1A_no_residentes", "2015-2025 (43 prov.)", e["BK002_E2_con_controles_dlnP_por_pp_nr"],
    e["BK002_E1_bivariada_dlnP_por_pp_nr"], "Δln precio por pp de peso no residente (asociación)", "C4", "asociacion_transversal",
    "Bivariada 0,0096 [0,0046; 0,0147]; con controles 0,0002 [-0,0055; 0,0059]. Peso (MIVAU/Notariado) de fuente efectiva única. No es una contribución en pp.",
    ic=tuple(ic["BK002_E2"]), fecha="2026T2")
entradas_df = pd.DataFrame(entradas)

# ---------------------------------------------------------------- huecos declarados
HUECOS = []
for merc in MERC:
    for col in COLS:
        for fam in FAM:
            if not ((entradas_df.mercado == merc) & (entradas_df.columna == col) & (entradas_df.familia == fam)).any():
                HUECOS.append(dict(mercado=merc, columna=col, familia=fam))
entradas_df.to_csv(OUT / "tabla_contribuciones_larga.csv", index=False, float_format="%.4f")
pd.DataFrame(HUECOS).to_csv(OUT / "huecos.csv", index=False)

# ---------------------------------------------------------------- estabilidad: rangos de las 4 familias comunes
def rank_vec(df, metric):
    v = df.groupby("familia")[metric].first().reindex(COMUNES)
    return v.abs().rank(ascending=False, method="average") if v.notna().all() else None


def metricas(m):
    return "central"


estab = []
grupos = entradas_df[entradas_df.familia.isin(COMUNES) & entradas_df.central.notna()
                     & ~entradas_df.metodo.isin(["v3_PB_cota_inmigracion"])]
rk = {}
for (merc, col, met), g in grupos.groupby(["mercado", "columna", "metodo"]):
    r = rank_vec(g, "central")
    if r is not None:
        rk[(merc, col, met)] = r
# v2: M1 y M2 por separado (estabilidad interna)
for merc in ("compra", "alquiler_stock"):
    for col in COLS:
        sub = bd[(bd.mercado == ("alquiler" if merc == "alquiler_stock" else "compra")) & (bd.periodo == PER2[col])]
        cm = {"demografica": "demografia", "renta_empleo": "empleo_renta", "financiacion_tipos": "credito_tipos_cu", "oferta_suelo": "oferta"}
        r = {m: pd.Series({f: abs(sub[(sub.modelo == m) & (sub.componente == c)].contrib_pp.iloc[0]) for f, c in cm.items()}).rank(ascending=False)
             for m in ("M1", "M2")}
        tau = float(pd.Series(r["M1"]).corr(pd.Series(r["M2"]), method="kendall"))
        estab.append(dict(tipo="M1_vs_M2", mercado=merc, a=f"v2 {col}", b="", tau=tau, n_fam=4,
                          orden_a=" > ".join(r["M1"].sort_values().index), orden_b=" > ".join(r["M2"].sort_values().index)))
for (k1, r1), (k2, r2) in combinations(rk.items(), 2):
    if k1[0] != k2[0]:
        continue
    if k1[1] == k2[1] and k1[2] != k2[2]:
        tipo = "entre_metodos_mismo_periodo"
    elif k1[2] == k2[2] and k1[1] != k2[1]:
        tipo = "mismo_metodo_entre_periodos"
    else:
        tipo = "metodos_y_periodos_distintos"
    tau = float(r1.corr(r2, method="kendall"))
    estab.append(dict(tipo=tipo, mercado=k1[0], a=f"{k1[2]} {k1[1]}", b=f"{k2[2]} {k2[1]}", tau=tau, n_fam=4,
                      orden_a=" > ".join(r1.sort_values().index), orden_b=" > ".join(r2.sort_values().index)))
est = pd.DataFrame(estab)
est.to_csv(OUT / "estabilidad.csv", index=False, float_format="%.3f")
UMBRAL = 0.67  # tau >= 0,67 con 4 familias: como mucho una pareja invertida
inest = bool((est.tau.dropna() < UMBRAL).any()) if len(est) else True
frac = float((est.tau.dropna() >= UMBRAL).mean()) if len(est) else 0.0
ESTABLE = (not inest)
veredicto_est = "contribuciones estables" if ESTABLE else "contribuciones no estables"

# ---------------------------------------------------------------- tabla ancha (texto)
def celda(merc, col, fam):
    g = entradas_df[(entradas_df.mercado == merc) & (entradas_df.columna == col) & (entradas_df.familia == fam)]
    if g.empty:
        return "sin dato"
    return " | ".join(f"[{r.metodo}, {r.capa}] {r.rango_lo:.2f} a {r.rango_hi:.2f} {r.unidad}"
                      for r in g.itertuples())

ancho = pd.DataFrame({f"{m} {c}": [celda(m, c, f) for f in FAM] for m in MERC for c in COLS}, index=FAM)
ancho.index.name = "familia"
ancho.to_csv(OUT / "tabla_contribuciones.csv")

# observados de referencia
obs_ref = {f"{m}|{c}": float(v) for (m, c), v in OBS.items()}

# ---------------------------------------------------------------- figura determinista
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, merc, tit in ((axs[0], "compra", "Compra (v2: real; B3: % R2)"), (axs[1], "alquiler_stock", "Alquiler stock (v2: IPC nominal, pp)")):
    d = entradas_df[(entradas_df.mercado == merc) & entradas_df.metodo.isin(["v2_BD_temporal"]) & entradas_df.familia.isin(COMUNES + ["residuo"])]
    y = 0
    labs = []
    for col, colr in zip(COLS, ["#4c72b0", "#dd8452", "#55a868"]):
        for fam in COMUNES + ["residuo"]:
            r = d[(d.columna == col) & (d.familia == fam)]
            if r.empty:
                continue
            r = r.iloc[0]
            ax.plot([r.rango_lo, r.rango_hi], [y, y], color=colr, lw=5)
            if pd.notna(r.ic_lo):
                ax.plot([r.ic_lo, r.ic_hi], [y, y], color="k", lw=0.8)
            labs.append((y, f"{col} {fam}"))
            y += 1
        y += 1
    ax.axvline(0, color="grey", lw=0.6)
    ax.set_yticks([a for a, _ in labs])
    ax.set_yticklabels([b for _, b in labs], fontsize=6)
    ax.invert_yaxis()
    ax.set_xlabel("pp de Δln acumulado: barra = rango M1-M2; línea = IC95 envolvente")
    ax.set_title(tit + "\nv2 BD, contribución contable (C4), no efecto", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "fig_contribuciones.png", dpi=110, metadata={"Software": None})
plt.close(fig)

# ---------------------------------------------------------------- hechos.json
hechos = []


def hecho(i, ind, v, lo, hi, u, per, cob, fu, capa, fecha):
    hechos.append(dict(id=i, indicador=ind, valor=None if v is None else round(float(v), 3),
                       min=None if lo is None else round(float(lo), 3), max=None if hi is None else round(float(hi), 3),
                       unidad=u, periodo=per, cobertura=cob, fuentes=fu, capa=capa, fecha_dato=fecha))


def rg(merc, col, fam, met):
    g = entradas_df[(entradas_df.mercado == merc) & (entradas_df.columna == col) & (entradas_df.familia == fam) & (entradas_df.metodo == met)]
    return g.iloc[0] if len(g) else None


for merc, nm in (("alquiler_stock", "alquiler (IPC, stock)"), ("compra", "compra (valor tasado real)")):
    for col in COLS:
        for fam in COMUNES + ["residuo"]:
            r = rg(merc, col, fam, "v2_BD_temporal")
            hecho(f"B4-v2-{merc}-{col}-{fam}", f"Contribución contable de {fam} a {nm} (v2, M1-M2)", r.central, r.rango_lo, r.rango_hi,
                  "pp de Δln acumulado", f"{col} (v2: {r.periodo_origen})", "49 provincias", "v2 BD (panel provincial, FE)", "C4", "2024Q1")
for fam in COMUNES + ["turismo_no_residentes", "residuo"]:
    r = rg("compra", "2015-2025", fam, "B3_transversal_Shapley")
    hecho(f"B4-b3-shapley-{fam}", f"Cuota de R2 entre provincias de {fam} (precio)", r.central, r.rango_lo, r.rango_hi,
          "% del R2", "2015-2025", "50 provincias", "B3 (MIVAU y Registradores)", "C4", "2025T4")
_vut = json.loads((ROOT / "output" / "v3" / "PB" / "cotas.json").read_text())[0]   # cota C2 de cantidad de v3 (no tecleada)
hecho("B4-v3-vut-cantidad", "Máximo de stock de alquiler desplazado por viviendas turísticas", round(_vut["cota_superior"], 3),
      round(_vut["sensibilidad_min"], 3), round(_vut["sensibilidad_max"], 3),
      "% del stock de alquiler", "2020M08-2024M08", "España", "v3 PB (INE VUT, Censo 2021)", "C2", "2024-08")
hecho("B4-estabilidad-tau-min", "Tau de Kendall mínima del orden de familias entre métodos/periodos", float(est.tau.min()),
      float(est.tau.min()), float(est.tau.max()), "tau (4 familias)", "2015-2025", "comparaciones: %d" % len(est),
      "B4 estabilidad.csv", "C4", "2026-10-10")
json.dump(hechos, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- fichas
def fr(x):
    return f"{x:.2f}"

ev_com = ["output/v5/B4/tabla_contribuciones_larga.csv", "output/v5/B4/estabilidad.csv"]
fichas = [
    dict(id="B4-V1", tema="Inmigración", enunciado="La subida se debe sobre todo a la inmigración.", capa="C4",
         magnitud="Cota C2 de cantidad: la población extranjera supone como máximo el 45,2 % de la creación de hogares en 2014-2019 (174.410 viviendas) y no informa en 2020-2025 (100 %). Precio: condicional a |ε_d|=0,33, ≤2,1 % (2014-2019) y ≤19,0 % (2020-2025) (C4). v2: la componente demográfica de la descomposición contable es de -3,0 a -4,1 pp al alquiler en 2014-2019 y signo opuesto según modelo en compra 2020-2024 (M1 +1,2; M2 -5,3 pp reales). B3: demografía segunda por cuota de R2 (21-26 %), con p de Holm 0,41 para F2.",
         intervalo="Cuota de R2 entre provincias 21-26 %; contribución v2 sin signo estable", cota="C2 solo la cantidad; magnitud sobre precio C4",
         literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
         regla="La traducción a precio solo es C4 (ε sin estimación verificada, fuente única de población); sin C3 no se puede afirmar ni negar el papel principal.",
         limites="La asociación transversal y la contribución temporal discrepan en signo y orden; sin identificación causal.", evidencia=ev_com),
    dict(id="B4-V2", tema="Turismo", enunciado="La subida se debe a los pisos turísticos.", capa="C4",
         magnitud="Cota C2: como máximo el 2,4-2,7 % del stock de alquiler (hasta 81.771 viviendas), 2020M08-2024M08, suponiendo sustitución 1:1. En precio de alquiler, condicional a |ε_d| (1,0-0,33): ≤2,7-8,3 % frente a un alquiler de stock que sube 10,9-22,9 % en 2015-2024 (IPC, IPVA). v2 (2021T3-2024T1, solo M1): +0,02 pp [-0,06; 0,09] de 2,26 pp. B3: VUT sin coeficiente distinguible de 0 en precio. Concentración local: hasta 8,9 % del stock en Málaga capital (cota C2).",
         intervalo="Cantidad 2,4-2,7 % del stock (C2); precio ≤2,7-8,3 % (C4, condicional)", cota="C2 de cantidad; C4 de precio",
         literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
         regla="La cota de cantidad (C2) limita el desplazamiento nacional, pero la traducción a precio depende de una elasticidad no verificada (C4): no se llega a un veredicto sobre «se debe». El alcance es nacional; en ciudades concretas la cota es mayor.",
         limites="VUT del INE es estadística experimental; sin series de alquiler turístico/de temporada (BK-014 sin analizar); no residentes: con controles la asociación no se distingue de cero (R1A, C4).",
         evidencia=ev_com),
    dict(id="B4-V3", tema="Oferta", enunciado="La subida se debe a la falta de oferta.", capa="C4",
         magnitud="B3: la brecha de oferta (F4) es la familia con mayor cuota de R2 entre provincias (23-29 %), pero se mide en 2021-2025 con precios y puede ser en parte mecánica. v2: la componente contable de la oferta contemporánea (terminadas) es de -0,02 a 0,10 pp, con IC que incluye 0. Las clases de A4 son C4 (regla B5).",
         intervalo="B3 23-29 % del R2; v2 -0,02 a 0,10 pp", cota="C4 (no hay cota de oferta con supuestos explícitos en esta tabla)",
         literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
         regla="Los dos métodos discrepan (orden primero en B3, nulo en v2) y ninguno es C3; se reportan ambos.",
         limites="Medición distinta en cada método (stock de déficit frente a flujo de terminadas); sin respuesta de la oferta identificada.", evidencia=ev_com),
    dict(id="B4-V4", tema="Financiación", enunciado="La subida se debe a los tipos de interés bajos.", capa="C4",
         magnitud="v3 PB: la caída del coste de uso es compatible como máximo con +23,5 a +78,0 % (Δln 1/uc) en 2014-2021 frente a +12,7 % de precio tasado; en 2021-2025 los tipos suben y el precio también (+25,0 %): signo contrario. v2: financiación y tipos +1,9 a +2,3 pp en compra real (M1) y ≈0 (M2): discrepan. En alquiler, la componente de los tipos se fija en 0 por supuesto. B3: hipotecas por 1.000 habitantes sin asociación distinguible (8,9-13,6 % del R2).",
         intervalo="v2 compra -0,00 a 2,27 pp según modelo; cota v3 23-78 % (C4)", cota="C4",
         literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
         regla="Los métodos discrepan y la componente común de los tipos nacionales queda en el componente común de v2 (tiempo), no atribuible por provincia; sin C3 no se concluye.",
         limites="Los tipos nacionales no varían entre provincias: v2 y B3 no los identifican; la cota v3 es condicional a supuestos de coste de uso.", evidencia=ev_com),
]
json.dump(fichas, open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- resultado.json
res = dict(
    rama="B4",
    pregunta="¿Cuánto de la variación del precio de compra y del alquiler (stock y contratos nuevos) se asocia con cada familia (demografía, renta y empleo, financiación, oferta, turismo y no residentes, inversión, residuo) y es estable el orden entre métodos y periodos?",
    capa="C4 (C2 solo en las cotas de cantidad de v3 PB)",
    datos="output/v5/B3 (Shapley y coeficientes provinciales), output/v2/BD y BV (descomposición temporal), output/v3/PB (cotas), output/v5/A23 (observados), output/v5/R1A y R1B. Sin datos nuevos ni reestimación.",
    N=dict(entradas=int(len(entradas_df)), huecos=int(len(HUECOS)), comparaciones_estabilidad=int(len(est))),
    metodo="Triangulación de salidas existentes: v2 (pp de Δln, FE, M1/M2), B3 (cuota de R2 y beta estandarizado, transversal), v3 (cotas). Unidades no sumables entre métodos; rango por celda = mín-máx entre variantes de un método. Estabilidad = tau de Kendall del orden de las 4 familias comunes.",
    estimacion=dict(observados_v2_pp=obs_ref, estabilidad=dict(veredicto=veredicto_est, tau_min=float(est.tau.min()), tau_max=float(est.tau.max()),
                                                           frac_tau_ge_067=frac, umbral=UMBRAL),
                    alquiler_nuevos="sin descomposición por familia en ninguna fuente: solo conciliación contable de A23 (IPVA 2021-2024: existentes 7,06, nuevos 3,54, composición -0,38 de 10,23 pts)",
                    inversion="sin dato: grandes tenedores en espera de solicitud de transparencia (v3 PB B3)"),
    ic95=None, p_ajustado=None,
    nivel_evidencia="EXPLORATORIO / DESCRIPTIVO: contribuciones contables y cotas, no efectos. Nada es C3.",
    diagnosticos=dict(estabilidad=veredicto_est, ventanas="Ventanas de v2 desplazadas (2014Q1-2024Q1; P4 hasta 2024Q1) frente a 2015-2025; compra v2 es REAL, A23 es nominal.",
                      multiplicidad="No se contrasta ninguna hipótesis nueva; los p de B3 conservan su ajuste original."),
    fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
    notas=["No aplica validación fuera de muestra: no se estima nada; AR(4)/ECM v1 y DM no procede.",
           "Contribución contable no es efecto: v2 asigna coef×variación media; B3 reparte R2 entre provincias; v3 da máximos bajo supuestos.",
           "Cuando B3 y v2 discrepan se reportan ambos (ver tabla larga).", "Capa de cada celda = la menor de sus componentes."],
)
json.dump(res, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)
REG.flush()
print(veredicto_est, round(est.tau.min(), 2), round(frac, 2), len(entradas_df), len(HUECOS))
print(est[["tipo", "mercado", "a", "b", "tau"]].to_string())
