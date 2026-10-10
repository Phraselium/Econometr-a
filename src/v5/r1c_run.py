"""R1c: (1) quien posee las viviendas (tabla y figura); (2) BK-009 capacidad del sector construccion.
Determinista, sin red. Lee data/raw y output/v4/M4. Escribe en output/v5/R1C/.
"""
import json
import sys
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, holm  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v5" / "R1C"
(OUT / "figuras").mkdir(parents=True, exist_ok=True)
reg = Registry(OUT / "registro.csv")
hechos = []


def hecho(id_, ind, v, mn, mx, unidad, periodo, cob, fuentes, capa, fecha):
    hechos.append(dict(id=id_, indicador=ind, valor=v, min=mn, max=mx, unidad=unidad, periodo=periodo,
                       cobertura=cob, fuentes=fuentes, capa=capa, fecha_dato=fecha))


# ---------------------------------------------------------------- TAREA 1
eff = pd.read_csv(RAW / "v3" / "eff_tenencia_edad_v3.csv")
eff = eff[eff.serie.str.contains("DO 2413")].copy()
eff["medida"] = eff.serie.str.extract(r"eff_(pct_hogares_\w+?)\|")[0]
eff["edad"] = eff.serie.str.extract(r"edad=([^|]+)\|")[0]
eff = eff[(eff.periodo == 2022) & eff.medida.notna()]
EFF = {(r.medida, r.edad): r.valor for r in eff.itertuples()}
ecv = pd.read_csv(RAW / "v3" / "ine_ecv_tenencia_edad_v3.csv")
ecv = ecv[ecv.serie.str.contains("sexo=Ambos sexos")].copy()
ecv["reg"] = ecv.serie.str.split("|").str[1]
ecv["edad"] = ecv.serie.str.extract(r"edad_persona_referencia=([^|]+)\|")[0]
ECV = {(r.reg, r.edad, r.periodo): r.valor for r in ecv.itertuples()}
cen = pd.read_csv(OUT.parents[1] / "v4" / "M4" / "tablas" / "tenencia_censo2021.csv")
cen_n = cen[cen.nivel == "nacional"].iloc[0]
etdp = pd.read_csv(OUT.parents[1] / "v4" / "M4" / "tablas" / "flujo_compraventas_comprador_pj_etdp.csv")
et = etdp[etdp.anyo == etdp.anyo.max()].iloc[0]

SD = "sin dato"
filas = []


def fila(ambito, cat, sub, medida, valor, unidad, ano, fuentes, capa, nota=""):
    filas.append(dict(ambito=ambito, categoria=cat, subcategoria=sub, medida=medida,
                      valor=valor if valor is not None else SD, unidad=unidad, ano=ano,
                      fuentes=fuentes, capa=capa, nota=nota))


TR = ["<35", "35-44", "45-54", "55-64", "65-74", "75+"]
F_EFF = "BdE EFF 2022 (DO 2413)"
for t in TR:
    fila("Parque total", "Persona fisica", f"titular/cabeza de familia {t}",
         "hogares con vivienda principal en propiedad", EFF[("pct_hogares_vivienda_principal", t)],
         "% de hogares del tramo", 2022, F_EFF, "C4",
         "EFF 2022 y ECV 2022 no coinciden por tramo (ECV 65+: 89,4 %; EFF 65-74: 83,0 %, 75+: 84,0 %; "
         "diferencia 5,4-6,4 pp); tramos no homologables bajo 65; ambos se reportan")
    fila("Parque total", "Persona fisica", f"titular/cabeza de familia {t}",
         "hogares con otras propiedades inmobiliarias", EFF[("pct_hogares_otras_propiedades", t)],
         "% de hogares del tramo", 2022, F_EFF, "C4", "fuente unica; incluye cualquier inmueble, no solo vivienda")
for t in ["De 16 a 29 años", "De 30 a 44 años", "De 45 a 64 años", "65 y más años"]:
    fila("Parque total", "Persona fisica", f"persona de referencia {t}",
         "hogares con vivienda principal en propiedad (segunda fuente)", ECV[("Propiedad", t, 2022)],
         "% de hogares del tramo", 2022, "INE ECV tabla 9994", "C4", "tramos distintos de EFF; ver nota anterior")
t_eff, t_ecv, t_cen = EFF[("pct_hogares_vivienda_principal", "total")], ECV[("Propiedad", "Total", 2022)], \
    cen_n.pct_propiedad
rng = (min(t_eff, t_ecv, t_cen), max(t_eff, t_ecv, t_cen))
c_tot = "C1" if rng[1] - rng[0] <= 5 else "C4"
fila("Parque total", "Persona fisica", "todas las edades", "hogares con vivienda principal en propiedad",
     round(float(np.mean([t_eff, t_ecv, t_cen])), 1), "% de hogares", "2021-2022",
     "BdE EFF 2022; INE ECV 2022; INE Censo 2021 (59523)", c_tot,
     f"EFF {t_eff} %, ECV {t_ecv} %, Censo {t_cen:.1f} % (viviendas principales); rango {rng[0]:.1f}-{rng[1]:.1f} pp. "
     "v4 rotulaba el Censo como C4 por fuente unica; con EFF y ECV hay tres fuentes en 5 pp")
fila("Parque total", "Persona fisica", "todas las edades", "viviendas principales en propiedad",
     int(cen_n.propiedad), "viviendas", 2021, "INE Censo 2021 (59523)", "C4",
     "fuente unica en numero de viviendas; sin desglose por edad")
fila("Parque total", "Persona fisica", "por edad (Censo 2021)", "regimen de tenencia por edad", None, "-", 2021,
     "INE Censo 2021", "-", "sin tabla publicada en Tempus (M2); solicitud S7 en docs/v4/solicitudes.md")
fila("Parque total", "Persona juridica o empresa", "stock", "viviendas con titular persona juridica", None,
     "viviendas", "-", "Catastro", "-", "Catastro no publica titulares por naturaleza; solicitud S1 (Catastro)")
fila("Parque total", "Sector publico", "stock", "viviendas de titularidad publica", None, "viviendas", "-",
     "Catastro / Ministerio", "-", "sin fuente abierta localizada; solicitud S1 (Catastro)")
fila("Mercado: compraventas", "Persona fisica", "comprador", "compraventas con comprador persona fisica",
     round(100 - et.pct_comprador_pj, 1), "% de compraventas", int(et.anyo),
     "INE ETDP tabla 50272", "C4", "fuente unica (INE); Notariado y Registradores sin dato de tipo de comprador")
fila("Mercado: compraventas", "Persona juridica o empresa", "comprador", "compraventas con comprador persona juridica",
     et.pct_comprador_pj, "% de compraventas", int(et.anyo), "INE ETDP tabla 50272", "C4",
     "fuente unica; Notariado: sin dato de compradores persona juridica en el repositorio")
fila("Mercado: compraventas", "Persona juridica o empresa", "vendedor", "compraventas con vendedor persona juridica",
     round(et.pct_vendedor_pj, 1), "% de compraventas", int(et.anyo), "INE ETDP tabla 50272", "C4", "fuente unica")
fila("Mercado: compraventas", "Persona fisica", "comprador por edad", "compraventas por tramo de edad del comprador",
     None, "-", "-", "INE ETDP", "-", "ETDP no desglosa por edad; sin solicitud especifica")
fila("Mercado: compraventas", "Sector publico", "comprador/vendedor", "compraventas con sector publico", None,
     "-", "-", "INE ETDP", "-", "ETDP agrega personas juridicas; sin desglose publico")
ECV_TR = ["De 16 a 29 años", "De 30 a 44 años", "De 45 a 64 años", "65 y más años"]
tot_alq = ECV[("Alquiler a precio de mercado", "Total", 2025)] + ECV[("Alquiler inferior al precio de mercado", "Total", 2025)]
fila("Mercado: alquiler", "Persona fisica", "inquilinos, todas las edades", "hogares en alquiler (demanda)",
     round(tot_alq, 1), "% de hogares", 2025, "INE ECV tabla 9994", "C4", "lado inquilino, no arrendador; fuente unica en 2025")
for t in ECV_TR:
    a = ECV[("Alquiler a precio de mercado", t, 2025)] + ECV[("Alquiler inferior al precio de mercado", t, 2025)]
    fila("Mercado: alquiler", "Persona fisica", f"inquilino {t}", "hogares en alquiler (demanda)", round(a, 1),
         "% de hogares del tramo", 2025, "INE ECV tabla 9994", "C4",
         "lado inquilino, no arrendador; fuente unica en 2025")
fila("Mercado: alquiler", "Persona fisica", "arrendador", "viviendas alquiladas por arrendador persona fisica",
     None, "-", "-", "AEAT / registros de fianzas", "-", "solicitudes S3 (AEAT) y S4 (fianzas)")
fila("Mercado: alquiler", "Persona juridica o empresa", "arrendador", "viviendas alquiladas por persona juridica",
     None, "-", "-", "AEAT / registros de fianzas", "-", "solicitudes S3 (AEAT) y S4 (fianzas)")
fila("Mercado: alquiler", "Sector publico", "arrendador", "viviendas en alquiler de titularidad publica", None,
     "-", "-", "Ministerio de Vivienda", "-", "sin fuente abierta localizada")
tab = pd.DataFrame(filas)
tab.to_csv(OUT / "tabla_propiedad.csv", index=False)
reg.log("T1", "tenencia_total_3fuentes", "EFF2022|ECV2022|Censo2021", 2021, 2022, 3, np.nan, np.nan, np.nan,
        coef_interes=rng[1] - rng[0], notas=f"rango pp; capa {c_tot}")
reg.log("T1", "tenencia_65mas_EFF_vs_ECV", "ECV65+ - EFF65-74/75+", 2022, 2022, 2, np.nan, np.nan, np.nan,
        coef_interes=ECV[("Propiedad", "65 y más años", 2022)] - EFF[("pct_hogares_vivienda_principal", "65-74")],
        notas="discrepancia pp; ambos se reportan; C4")

hecho("R1C-001", "Hogares con vivienda principal en propiedad", round(float(np.mean([t_eff, t_ecv, t_cen])), 1),
      round(rng[0], 1), round(rng[1], 1), "% de hogares", "2021-2022", "Espana", "BdE EFF; INE ECV; INE Censo 2021",
      c_tot, "2022")
hecho("R1C-002", "Hogares con otras propiedades (cualquier inmueble), tramo 65-74", EFF[("pct_hogares_otras_propiedades", "65-74")],
      EFF[("pct_hogares_otras_propiedades", "65-74")], EFF[("pct_hogares_otras_propiedades", "65-74")],
      "% de hogares del tramo", "2022", "Espana", "BdE EFF 2022", "C4", "2022")
hecho("R1C-003", "Hogares con otras propiedades (cualquier inmueble), tramo <35", EFF[("pct_hogares_otras_propiedades", "<35")],
      EFF[("pct_hogares_otras_propiedades", "<35")], EFF[("pct_hogares_otras_propiedades", "<35")],
      "% de hogares del tramo", "2022", "Espana", "BdE EFF 2022", "C4", "2022")
hecho("R1C-004", "Compraventas con comprador persona juridica", et.pct_comprador_pj, et.pct_comprador_pj,
      et.pct_comprador_pj, "% de compraventas", str(int(et.anyo)), "Espana", "INE ETDP 50272", "C4", f"{int(et.anyo)}-12")

# Figuras
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
x = np.arange(len(TR))
ax[0].bar(x - 0.2, [EFF[("pct_hogares_vivienda_principal", t)] for t in TR], 0.4, label="Vivienda principal en propiedad (EFF)")
ax[0].bar(x + 0.2, [EFF[("pct_hogares_otras_propiedades", t)] for t in TR], 0.4, label="Otras propiedades (EFF)")
ax[0].set_xticks(x, TR)
ax[0].set_xlabel("Edad del cabeza de familia")
ax[0].set_ylabel("% de hogares del tramo, 2022")
ax[0].set_title("Parque total: personas fisicas por edad (C4 por tramo)")
ax[0].legend(fontsize=8)
ax[0].text(0.02, 0.02, "Personas juridicas y sector publico: sin dato", transform=ax[0].transAxes, fontsize=8)
ys = etdp.sort_values("anyo")
ax[1].plot(ys.anyo, ys.pct_comprador_pj, label="Comprador persona juridica")
ax[1].plot(ys.anyo, ys.pct_vendedor_pj, label="Vendedor persona juridica")
ax[1].set_ylabel("% de compraventas de vivienda")
ax[1].set_title("Mercado: compraventas con persona juridica (ETDP, C4)")
ax[1].legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "figuras" / "propiedad_edad_y_pj.png", dpi=130, metadata={"Software": None})
plt.close(fig)

amb = ["Parque total", "Mercado: compraventas", "Mercado: alquiler"]
cats = ["Persona fisica", "Persona juridica o empresa", "Sector publico"]
col = {"C1": "#9fd3a5", "C4": "#f2d98a", "-": "#d9d9d9"}
fig, ax = plt.subplots(figsize=(13, 4.8))
for i, c in enumerate(cats):
    for j, a in enumerate(amb):
        s = tab[(tab.ambito == a) & (tab.categoria == c)]
        con = s[s.valor != SD]
        capa = "C1" if (con.capa == "C1").any() else ("C4" if len(con) else "-")
        if len(con):
            r = con[con.capa == "C1"].iloc[0] if capa == "C1" else con.iloc[0]
            txt = f"{r.medida[:60]}\n{r.valor} {r.unidad} ({r.ano})\n{capa}"
        else:
            txt = "sin dato"
        ax.add_patch(plt.Rectangle((j, 2 - i), 1, 1, fc=col[capa], ec="k"))
        ax.text(j + 0.5, 2.5 - i, txt, ha="center", va="center", fontsize=7.5)
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.set_xticks([0.5, 1.5, 2.5], amb)
ax.set_yticks([2.5, 1.5, 0.5], cats)
ax.set_title("Quien posee las viviendas: cobertura por celda y capa (verde C1, amarillo C4, gris sin dato)")
fig.tight_layout()
fig.savefig(OUT / "figuras" / "propiedad_matriz_capas.png", dpi=130, metadata={"Software": None})
plt.close(fig)

# ---------------------------------------------------------------- TAREA 2
def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    for ch in "(),.":
        s = s.replace(ch, " ")
    return " ".join(s.split())


epa = pd.read_csv(RAW / "v5" / "ine_r1c_t65354.csv")
epa = epa[epa.nombre.str.contains("Construcci", regex=False)].copy()
epa["f"] = pd.to_datetime(epa.fecha, unit="ms") + pd.Timedelta(hours=12)
epa["anyo"] = epa.f.dt.year
epa["terr"] = epa.nombre.str.extract(r"^(.*?)\. Ocupados")[0]
epa = epa[epa.f <= "2025-12-31"]
cnt = epa.groupby(["terr", "anyo"]).valor.agg(["mean", "count"]).reset_index()
cnt = cnt[cnt["count"] == 4]  # solo anos completos
ini = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
ini = ini[ini.serie.str.contains("iniciadas_anual")].copy()
ini["anyo"] = ini.fecha.str[:4].astype(int)
mp = ini[ini.nivel == "provincia"][["territorio", "ccaa"]].drop_duplicates()
mp = {norm(a): b for a, b in zip(mp.territorio, mp.ccaa)}
mp.update({norm(k): v for k, v in {
    "Coruña, A": "Galicia", "Palmas, Las": "Canarias", "Araba/Álava": "País Vasco", "Asturias": "Asturias (Principado de )",
    "Balears, Illes": "Balears (Illes)", "Cantabria": "Cantabria", "Madrid": "Madrid (Comunidad de)",
    "Murcia": "Murcia (Región de)", "Navarra": "Navarra (Comunidad Foral de)", "Rioja, La": "Rioja (La)",
    "Ceuta": "Ceuta", "Melilla": "Melilla"}.items()})
cnt["ccaa"] = cnt.terr.map(lambda t: mp.get(norm(t)))
sin_map = sorted(cnt[cnt.ccaa.isna() & (cnt.terr != "Total Nacional")].terr.unique())
nac = cnt[cnt.terr == "Total Nacional"].set_index("anyo")["mean"]
cc = cnt[cnt.ccaa.notna()].groupby(["ccaa", "anyo"])["mean"].sum().reset_index()
iv = ini[ini.nivel.isin(["ccaa", "ciudad_autonoma"])][["territorio", "anyo", "valor"]]
iv = iv.rename(columns={"territorio": "ccaa", "valor": "iniciadas"})
j = cc.merge(iv, on=["ccaa", "anyo"])
j["ocupados_miles"] = j["mean"]
j["ratio_ocupados_por_vivienda_iniciada"] = j.ocupados_miles * 1000 / j.iniciadas
j[["ccaa", "anyo", "ocupados_miles", "iniciadas", "ratio_ocupados_por_vivienda_iniciada"]].to_csv(
    OUT / "empleo_vs_iniciadas_ccaa.csv", index=False)
ini_n = ini[ini.nivel == "nacional"].set_index("anyo").valor
nat = pd.DataFrame({"ocupados_miles": nac, "iniciadas": ini_n}).dropna()
nat["ratio"] = nat.ocupados_miles * 1000 / nat.iniciadas
nat.to_csv(OUT / "empleo_vs_iniciadas_nacional.csv")
print("ratio nacional\n", nat.round(2).to_string())
print("provincias sin mapa:", sin_map)
for y in nat.index:
    reg.log("T2", f"ratio_nac_{y}", "ocupados_construccion/viviendas_libres_iniciadas", y, y, 1, np.nan, np.nan, np.nan,
            coef_interes=nat.loc[y, "ratio"])

# correlacion de variaciones 2013-2025 entre CCAA (descriptivo)
y0, y1 = 2013, 2025
a = j[j.anyo == y0].set_index("ccaa")
b = j[j.anyo == y1].set_index("ccaa")
com = a.index.intersection(b.index)
d_emp = np.log(b.loc[com, "ocupados_miles"] / a.loc[com, "ocupados_miles"])
d_ini = np.log(b.loc[com, "iniciadas"] / a.loc[com, "iniciadas"])
rho, p1 = stats.spearmanr(d_emp, d_ini)
d_rat = np.log(b.loc[com, "ratio_ocupados_por_vivienda_iniciada"] / a.loc[com, "ratio_ocupados_por_vivienda_iniciada"])
# ratio 2025 vs 2008
a8 = j[j.anyo == 2008].set_index("ccaa")
com8 = a8.index.intersection(b.index)
pres = {"spearman_dlog_empleo_vs_dlog_iniciadas_2013_2025": p1}
pa = holm(pres)
reg.log("T2", "spearman_emp_ini", "rho(dlog empleo, dlog iniciadas) CCAA 2013-2025", y0, y1, len(com), np.nan, np.nan,
        np.nan, coef_interes=rho, p_interes=p1, notas=f"Holm p={pa['spearman_dlog_empleo_vs_dlog_iniciadas_2013_2025']:.4f}; descriptivo")

# costes frente a precio (trimestral, muestra comun 2008T1-2025T4)
def trim(f):
    return pd.PeriodIndex(pd.to_datetime(f), freq="Q")


co = pd.read_csv(RAW / "eurostat_costes.csv")
co = pd.Series(co.valor.values, index=trim(co.fecha))
hp = pd.read_csv(RAW / "eurostat_hpi.csv")
hp = hp[(hp.purchase == "TOTAL") & (hp.unit == "I15_Q")]
hp = pd.Series(hp.valor.values, index=trim(hp.fecha))
bd = pd.read_csv(RAW / "bde_precio_vivienda_libre.csv")
bd = bd[bd.serie == "DHIVTNOAPLPMMUVT_RLI.T"]
bd = pd.Series(bd.valor.values, index=pd.PeriodIndex([f"{int(f[:4])}Q{(int(f[5:7]) - 1) // 3 + 1}" for f in bd.fecha], freq="Q"))
et6 = pd.read_csv(RAW / "v5" / "ine_r1c_t6030.csv")
et6 = et6[et6.serie == "ETCL34"].copy()
et6["f"] = pd.to_datetime(et6.fecha, unit="ms") + pd.Timedelta(hours=12)
etc = pd.Series(et6.valor.values, index=trim(et6.f))
sem = pd.concat({"coste_materiales_eurostat": co, "coste_laboral_constr_ine": etc, "precio_hpi_eurostat": hp,
                 "precio_tasacion_bde": bd}, axis=1).loc["2008Q1":"2025Q4"].dropna()
sem = sem[~sem.index.duplicated()]
base = sem.loc["2008Q1"]
idx = sem / base * 100
idx.index = idx.index.astype(str)
idx.to_csv(OUT / "costes_vs_precio_indice_2008T1.csv")
crec = {}
for per in [("2008Q1", "2013Q4"), ("2014Q1", "2025Q4"), ("2008Q1", "2025Q4")]:
    g = (sem.loc[per[1]] / sem.loc[per[0]] - 1) * 100
    crec[f"{per[0]}-{per[1]}"] = g.round(1).to_dict()
    for k, v in g.items():
        reg.log("T2", f"crec_{k}_{per[0]}_{per[1]}", "variacion % indice", per[0], per[1], len(sem.loc[per[0]:per[1]]),
                np.nan, np.nan, np.nan, coef_interes=v)
print(crec)
print("N muestra comun costes", len(sem), sem.index.min(), sem.index.max())

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].plot(nat.index, nat.ratio)
ax[0].set_title("Ocupados en construccion por vivienda libre iniciada (nacional)")
ax[0].set_ylabel("personas por vivienda iniciada")
ax[0].text(0.02, 0.9, "C4: numerador incluye obra no residencial; denominador solo vivienda libre", transform=ax[0].transAxes, fontsize=7)
for c in idx.columns:
    ax[1].plot(range(len(idx)), idx[c], label=c)
ax[1].set_xticks(range(0, len(idx), 16), list(idx.index[::16]), rotation=45)
ax[1].set_title("Indices de coste y precio (2008T1 = 100)")
ax[1].legend(fontsize=7)
fig.tight_layout()
fig.savefig(OUT / "figuras" / "construccion_capacidad.png", dpi=130, metadata={"Software": None})
plt.close(fig)

r08, r13, r25 = nat.loc[2008, "ratio"], nat.loc[2013, "ratio"], nat.loc[2025, "ratio"]
FU2 = "INE EPA 65354 (ocupados, construccion); MIVAU Boletin (viviendas libres iniciadas)"
hecho("R1C-010", "Ocupados en construccion por vivienda libre iniciada, nacional 2008", round(r08, 2), round(r08, 2),
      round(r08, 2), "personas por vivienda", "2008", "Espana", FU2, "C4", "2025-12")
hecho("R1C-011", "Ocupados en construccion por vivienda libre iniciada, nacional 2013", round(r13, 2), round(r13, 2),
      round(r13, 2), "personas por vivienda", "2013", "Espana", FU2, "C4", "2025-12")
hecho("R1C-012", "Ocupados en construccion por vivienda libre iniciada, nacional 2025", round(r25, 2), round(r25, 2),
      round(r25, 2), "personas por vivienda", "2025", "Espana", FU2, "C4", "2025-12")
g = crec["2014Q1-2025Q4"]
hecho("R1C-013", "Variacion 2014T1-2025T4 del coste de construccion (Eurostat) menos precio (tasacion BdE)",
      round(g["coste_materiales_eurostat"] - g["precio_tasacion_bde"], 1),
      round(min(g["coste_materiales_eurostat"], g["coste_laboral_constr_ine"]) - max(g["precio_hpi_eurostat"], g["precio_tasacion_bde"]), 1),
      round(max(g["coste_materiales_eurostat"], g["coste_laboral_constr_ine"]) - min(g["precio_hpi_eurostat"], g["precio_tasacion_bde"]), 1),
      "puntos porcentuales", "2014T1-2025T4", "Espana",
      "Eurostat sts_copi_q; INE ETCL 6030; Eurostat prc_hpi_q; BdE tasacion", "C4", "2025-12")


# ---------------------------------------------------------------- TAREA 3 (BK-034)
cv = pd.read_csv(RAW / "v5" / "ine_r1c_t59531.csv")
cv["terr"] = cv.nombre.str.rsplit(", ", n=1).str[0]
cv["var"] = cv.nombre.str.rsplit(", ", n=1).str[1]
cv = cv[cv.terr.str[:5].str.isdigit()]
cw = cv[cv["var"].isin(["Viviendas totales", "Viviendas vacías", "Viviendas de uso esporádico"])].pivot_table(
    index="terr", columns="var", values="valor", aggfunc="sum")
cw.columns = ["esporadicas", "totales", "vacias"]
cw["pct_vacias"] = 100 * cw.vacias / cw.totales
cw["pct_esporadicas"] = 100 * cw.esporadicas / cw.totales
cw["agrupado_asterisco"] = cw.index.str.contains("*", regex=False)
cw.reset_index().to_csv(OUT / "vacias_esporadicas_municipio_censo2021.csv", index=False)
n_ent, n_ast = len(cw), int(cw.agrupado_asterisco.sum())
q = cw.pct_vacias.quantile([0.1, 0.5, 0.9]).round(1).tolist()
reg.log("T3", "vacias_municipio_59531", "INE 59531 vacias/totales por entidad municipal", 2021, 2021, n_ent,
        np.nan, np.nan, np.nan, coef_interes=float(cw.vacias.sum() / cw.totales.sum() * 100),
        notas=f"{n_ast} entidades agrupadas (asterisco); cubre {int(cw.totales.sum())} viviendas")
hecho("R1C-020", "Entidades municipales con vacias y uso esporadico publicadas por el INE (Censo 2021, consumo electrico)",
      n_ent, n_ent, n_ent, "entidades", "2021-11", "Espana (8.131 municipios en 3.185 entidades)",
      "INE Censo 2021 tabla 59531", "C4", "2026-10-10")
hecho("R1C-021", "Mediana municipal del % de viviendas vacias (p10-p90 en min-max)", q[1], q[0], q[2],
      "% de viviendas", "2021-11", "Espana, entidades municipales", "INE Censo 2021 tabla 59531", "C4", "2021-11")

reg.flush()
res = dict(
    rama="R1C", pregunta="Quien posee las viviendas (por edad, persona juridica, sector publico; parque y mercado) y "
    "capacidad del sector construccion (BK-009)", capa="C4",
    datos="BdE EFF 2022; INE ECV 9994; INE Censo 2021 (59523); INE ETDP 50272; INE EPA 65354; MIVAU iniciadas; "
          "Eurostat costes e HPI; INE ETCL 6030; BdE tasacion",
    N=int(len(tab)), metodo="tabulacion descriptiva con capa por celda; ratio empleo/iniciadas y correlacion de Spearman entre CCAA",
    estimacion={"tenencia_total_pct": round(float(np.mean([t_eff, t_ecv, t_cen])), 1),
                "ratio_ocupados_por_vivienda_iniciada": {"2008": round(r08, 2), "2013": round(r13, 2), "2025": round(r25, 2)},
                "crecimiento_pct_2014T1_2025T4": g, "crecimiento_pct_2008T1_2013T4": crec["2008Q1-2013Q4"],
                "spearman_dlog_emp_ini_2013_2025": {"rho": round(float(rho), 3), "n_ccaa": int(len(com))}},
    ic95=None, p_ajustado={"spearman_holm": round(pa["spearman_dlog_empleo_vs_dlog_iniciadas_2013_2025"], 4)},
    nivel_evidencia="DESCRIPTIVO / EXPLORATORIO (tenencia total C1; resto C4)",
    diagnosticos={"celdas_sin_dato": int((tab.valor == SD).sum()), "provincias_sin_mapa_ccaa": sin_map,
                  "muestra_comun_costes": f"{sem.index.min()}-{sem.index.max()} n={len(sem)}"},
    fuera_muestra={"modelo": None, "rmse": None, "dm_vs_ar4": None},
    notas=f"BK-034: INE 59531 publica vacias y esporadicas en {n_ent} entidades municipales ({n_ast} agrupan municipios pequenos); sin seccion; fuente unica C4. Veredicto como maximo ANALIZADA, NO CONCLUYENTE. Sin dato: personas juridicas en el parque, sector publico, "
          "Censo por edad, arrendador por tipo (solicitudes S1, S3, S4, S7). Iniciadas = solo vivienda libre. "
          "Empleo: EPA ocupados por provincia agregados a CCAA; sin afiliacion SS por provincia (no localizada). "
          "INE no publica un ICC propio: se usan Eurostat sts_copi_q (coste de materiales y mano de obra) e INE ETCL. "
          "Analisis de capacidad no contrasta cuello de botella causal.")
(OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
(OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))
