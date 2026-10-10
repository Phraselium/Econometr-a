"""P-A (capa C1): hechos A1-A6. Punto de entrada único; determinista; sin red.

Uso: python3 src/v3/pa_run.py
Salidas: output/v3/PA/{tablas,figuras}, hechos.json, resultado.json, registro.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import econ_utils  # noqa: E402
import pa_a1  # noqa: E402
import pa_a23  # noqa: E402
import pa_a456  # noqa: E402
import pa_data as pdat  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
OUT = pdat.RAIZ / "output" / "v3" / "PA"
TAB, FIG = OUT / "tablas", OUT / "figuras"
HECHOS: list[dict] = []


def hecho(id_, enun, capa, mag, unidad, lo, hi, fuentes, supuestos, limites):
    assert capa in ("C1", "C2", "C4")
    assert capa == "C4" or len(fuentes) >= 2
    HECHOS.append({"id": id_, "enunciado_neutro": enun, "capa": capa, "magnitud": None if pd.isna(mag) else round(float(mag), 3),
                   "unidad": unidad, "intervalo": [round(float(lo), 3), round(float(hi), 3)], "fuentes": fuentes,
                   "supuestos": supuestos, "limites": limites})


def guardar(df: pd.DataFrame, nombre: str) -> None:
    df.to_csv(TAB / f"{nombre}.csv", index=False, float_format="%.4f")


def main() -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")

    # ---------------- A1
    t1, r1 = pa_a1.a1_nacional(reg)
    guardar(t1, "A1_nacional_combinaciones")
    guardar(r1, "A1_nacional_resumen")
    tp, rp = pa_a1.a1_provincial(reg)
    guardar(tp, "A1_provincial_combinaciones")
    guardar(rp, "A1_provincial_resumen")
    F_H = ["INE EPA (hogares, tabla 65269/65944; media trimestral)", "INE Censos 2011 y 2021 y ECP (tabla 60131)"]
    F_N = ["MIVAU certificados de fin de obra (libres) y calificaciones definitivas (protegida)", "MIVAU estimación del parque de viviendas",
           "INE Censos 2011 y 2021 (stock de viviendas)"]
    ESPEC = ["2002-2007", "2008-2013", "2014-2019", "2020-2025", "2014-2025"]
    tab = r1.copy()
    tab["preespecificado"] = tab.periodo.isin(ESPEC)
    tab["signo"] = np.where((tab.min_total < 0) & (tab.max_total > 0), "signo no determinado",
                            np.where(tab.max_total <= 0, "negativo (altas netas superiores)", "positivo"))
    tab["mediana"] = [t1[(t1.periodo == p_) & t1.protegida.isin(["con", "incluida"])].deficit.median() for p_ in tab.periodo]
    tab["criterio"] = np.where(tab.preespecificado, "ventana fijada en la especificación",
                               "ventana añadida tras ver las fuentes disponibles: Censos 2011/2021 y ECP (desde 2021T1) permiten dos fuentes de hogares; "
                               "elegida por disponibilidad de fuentes, no por el resultado; 2021-2025 se añade para comparar con el BdE")
    tab = tab.sort_values("preespecificado", ascending=False, kind="stable")
    guardar(tab, "A1_tabla_unica_periodos")
    for r in tab.itertuples():
        g = t1[(t1.periodo == r.periodo) & t1.protegida.isin(["con", "incluida"])]
        c1 = r.capa == "C1"
        indet = r.signo == "signo no determinado"
        fh = F_H if r.n_fuentes_hogares >= 2 else [F_H[0] + " (única fuente de hogares en este periodo)"]
        fn = [x for x in F_N if (x == F_N[0]) or (x == F_N[1]) or r.periodo in ("2012-2021", "2012-2025")]
        hecho(f"A1_nacional_{r.periodo}",
              f"Balance contable (variación de hogares menos altas netas de vivienda) entre {r.periodo.replace('-', ' y ')}, con vivienda protegida: "
              + (f"el signo no está determinado por las fuentes (rango {r.min_total:,.0f} a {r.max_total:,.0f}). " if indet else
                 f"rango de las combinaciones {r.min_total:,.0f} a {r.max_total:,.0f} ({r.signo}); mediana {r.mediana:,.0f}. ")
              + f"Con bajas del 0,1 %, rango entre fuentes {r.min_entre_fuentes_bajas01:,.0f} a {r.max_entre_fuentes_bajas01:,.0f}. "
              f"Las bajas del 0 % al 0,2 % anual suman hasta {r.efecto_bajas_02_viviendas:,.0f} viviendas."
              + ("" if c1 else " Una sola fuente de hogares: hecho de fuente única (C4)."),
              "C1" if c1 else "C4", np.nan if indet else r.mediana, "viviendas", r.min_total, r.max_total, fh + fn,
              "Hogares = viviendas principales en los censos; bajas = 0, 0,1 y 0,2 % anual del parque MIVAU del año anterior "
              "(solo en la fuente bruta de fin de obra); calificación definitiva de protegida como proxy de terminadas. "
              + ("Ventana fijada en la especificación." if r.preespecificado else
                 "Ventana añadida tras ver las fuentes disponibles (criterio: disponibilidad de Censos y ECP, no el resultado)."),
              "Signo negativo = altas netas superiores a la variación de hogares. Un balance contable no equivale a demanda insatisfecha a cualquier precio. "
              "Independencia parcial entre fuentes: la EPA se calibra con cifras de población del INE y la ECP está anclada al Censo 2021. "
              "Quiebre de la EPA en 2021; el fin de obra del MIVAU cubre menos que la variación del parque y del Censo. "
              "El cambio de signo entre periodos (negativo en 2002-2013, positivo desde 2014) es parte del hecho.")
    # comparación con la cifra del BdE (2021-2025)
    g = t1[(t1.periodo == "2021-2025") & t1.protegida.isin(["con", "incluida"])]
    bde = {"cifra_bde": pa_a1.BDE["cifra"], "ief": pa_a1.BDE["ief"], "min_pa": g.deficit.min(), "max_pa": g.deficit.max(),
           "bde_dentro_del_rango": bool(g.deficit.min() <= pa_a1.BDE["cifra"] <= g.deficit.max()), "nota": pa_a1.BDE["fuente"] + ". Cifra del BdE: DOI no comprobado (NO VERIFICADA en Crossref)"}
    (TAB / "A1_comparacion_BdE.json").write_text(json.dumps(bde, ensure_ascii=False, indent=1, default=float))
    s = rp[rp.periodo == "2022-2025"]
    hecho("A1_provincial_2022-2025",
          f"Déficit contable provincial 2022-2025 (ECP y dos fuentes de altas): suma de provincias {s['min'].sum():,.0f} a {s['max'].sum():,.0f}; "
          f"mayores valores centrales: " + ", ".join(f"{r.provincia} {((r.min + r.max) / 2):,.0f}"
                                                    for r in s.assign(m=(s['min'] + s['max']) / 2).nlargest(5, "m").itertuples()) + ".",
          "C4", ((s["min"] + s["max"]) / 2).sum(), "viviendas", s["min"].sum(), s["max"].sum(),
          ["INE ECP provincial (tabla 60133)", "MIVAU fin de obra provincial", "Catastro unidades urbanas residenciales (sin País Vasco ni Navarra)"],
          "Hogares provinciales de una sola fuente por periodo; bajas 0-0,2 % sobre el stock censal.",
          "Hecho de fuente única en hogares (C4). El Catastro no cubre territorios forales. Los 4 territorios forales usan solo fin de obra.")

    # ---------------- A2
    s2, r2 = pa_a23.a2(reg)
    guardar(s2, "A2_series_tasa")
    guardar(r2, "A2_hogares_implicitos")
    ult = int(r2.anio.iloc[0])
    tes = r2[r2.fuente.str.startswith("Eurostat")].tasa_observada.iloc[0]
    tep = r2[r2.fuente.str.startswith("EPA")].tasa_observada.iloc[0]
    hecho("A2_tasa_convivencia_25_34",
          f"Tasa de personas de 25-34 años que viven con sus progenitores en {ult}: {tes:.1f} % (Eurostat/ECV) y {tep:.1f} % (EPA, hijo/a de la persona de referencia). "
          f"España 2008: {r2[r2.referencia == 'España 2008'].tasa_referencia.iloc[0]:.1f} % (ECV) y {r2[r2.referencia == 'España 2008'].tasa_referencia.iloc[-1]:.1f} % (EPA); UE-27 {ult}: "
          f"{r2[r2.referencia.str.startswith('UE')].tasa_referencia.iloc[0]:.1f} % (ECV).",
          "C1", (tes + tep) / 2, "% de la población 25-34", min(tes, tep), max(tes, tep),
          ["Eurostat ilc_lvps08 (ECV)", "INE EPA tabla 65944 (hijo/a de la persona de referencia)"], "Conceptos distintos entre las dos tasas (convivencia con progenitores frente a hijo/a de la persona de referencia).",
          "Sin desagregación por CCAA (la especificación la pedía; no hay datos nacionales por CCAA en estas tablas); sin error muestral publicado en los ficheros. "
          "Eurostat ilc_lvps08 procede de la ECV (EU-SILC).")
    hecho("A2_hogares_implicitos",
          f"Cota bajo supuestos: hogares implícitos de 25-34 años si la tasa de convivencia fuese la de referencia (diferencia con la tasa de {ult} multiplicada por la población de 25-34 y dividida por el tamaño del hogar joven): "
          f"{r2.hogares_implicitos.min():,.0f} a {r2.hogares_implicitos.max():,.0f}. Con España 2008 como referencia: "
          f"{r2[r2.referencia == 'España 2008'].hogares_implicitos.min():,.0f} a {r2[r2.referencia == 'España 2008'].hogares_implicitos.max():,.0f}; "
          f"con la media UE-27: {r2[r2.referencia.str.startswith('UE')].hogares_implicitos.min():,.0f} a {r2[r2.referencia.str.startswith('UE')].hogares_implicitos.max():,.0f} (solo ECV).",
          "C2", np.nan, "hogares (= viviendas)", r2.hogares_implicitos.min(), r2.hogares_implicitos.max(),
          ["Eurostat ilc_lvps08 (ECV)", "INE EPA tabla 65944 (hijo/a de la persona de referencia)"],
          "Contrafactual: tasa de referencia = España 2008 o UE-27 del último año; personas por hogar joven entre 1,5 y 2,0; una vivienda por hogar. "
          "El rango mezcla la medida (ECV frente a EPA) y los supuestos (referencia y tamaño). No se da valor central.",
          "No es una medida descriptiva: depende de una referencia contrafactual. Sin desagregación por CCAA; sin error muestral publicado.")

    # ---------------- A3
    v3, t3, cob = pa_a23.a3(reg)
    guardar(t3, "A3_vacias_por_tercil")
    guardar(v3.reset_index().rename(columns={"index": "codigo"}), "A3_municipios_base")
    todos = t3[(t3.muestra == "todos con dato") & t3.tercil.isin(["alto", "bajo"]) & t3.presion.str.startswith("Δ")]
    gr = todos[todos.tercil == "alto"].pct_vacias_de_la_muestra
    gb = todos[todos.tercil == "bajo"].pct_vacias_de_la_muestra
    F3 = ["INE Censo 2021, tabla 59531 (vacías y uso esporádico por consumo eléctrico)", "Catastro (unidades urbanas residenciales) − Censo 2021 (principales) − INE VUT",
          "MIVAU valor tasado y SERPAVI (presión)"]
    p0 = "Δ ln valor tasado 2015-2021"
    fx = todos[todos.presion == p0]
    ra = fx[fx.tercil == "alto"].pct_vacias_de_la_muestra
    cm = todos[todos.medida_vacia == "Censo 2021: vacías"]
    rd = cm[cm.tercil == "alto"].pct_vacias_de_la_muestra
    hecho("A3_vacias_tercil_alto_vs_bajo",
          f"Porcentaje de las viviendas vacías (de los municipios con dato) situado en el tercil alto de presión. Rango de medida (tres medidas de vacancia, presión fija = {p0}, 277 municipios): "
          f"{ra.min():.1f} a {ra.max():.1f} %. Rango de definición (vacías del Censo 2021, tres definiciones de presión, 277 a 1.806 municipios): {rd.min():.1f} a {rd.max():.1f} %. "
          f"Tercil bajo, rango total: {gb.min():.1f} a {gb.max():.1f} %.",
          "C1", np.nan, "% de las vacías de la muestra", ra.min(), ra.max(), F3,
          "Terciles por rango dentro de los municipios con dato; presión = Δ ln valor tasado 2015-21 y 2021-25 y Δ ln alquiler SERPAVI 2015-21 (definiciones, no mediciones repetidas); "
          "segunda medida = Catastro 2021 − viviendas principales − VUT (VUT ausente = 0). Intervalo = rango de medida; el rango de definición figura en el enunciado.",
          "Independencia parcial entre las dos medidas de vacancia: ambas usan las viviendas principales del Censo 2021 (la segunda las resta). Muestra con valor tasado: 277 municipios; con SERPAVI: 1.806. "
          "Los municipios de menos de ~375 viviendas se agrupan en «resto» en el INE y quedan fuera. La segunda medida incluye segundas residencias. "
          "El Catastro no cubre País Vasco ni Navarra (la segunda medida excluye esos municipios).")
    may = t3[(t3.muestra == ">50.000 hab.") & t3.tercil.isin(["alto", "bajo"]) & t3.presion.str.startswith("Δ")]
    ga = may[may.tercil == "alto"].pct_vacias_de_la_muestra
    gbj = may[may.tercil == "bajo"].pct_vacias_de_la_muestra
    hecho("A3_vacias_mayores_50000",
          f"En municipios de más de 50.000 habitantes: tercil alto {ga.min():.1f} a {ga.max():.1f} % de las vacías de la muestra; tercil bajo "
          f"{gbj.min():.1f} a {gbj.max():.1f} %.", "C1", ga.median(), "% de las vacías de la muestra", ga.min(), ga.max(), F3,
          "Población = suma de personas de las secciones censales 2021.", "Entre 43 y 48 municipios por tercil.")
    por = todos.dropna(subset=["vacias_por_100_hogares_nuevos_11_21"])
    hecho("A3_vacias_por_100_hogares_nuevos",
          f"Vacías por cada 100 hogares nuevos 2011-2021 en municipios con nombre único en el Censo 2011: tercil alto {por[por.tercil == 'alto'].vacias_por_100_hogares_nuevos_11_21.min():,.0f} "
          f"a {por[por.tercil == 'alto'].vacias_por_100_hogares_nuevos_11_21.max():,.0f}; tercil bajo {por[por.tercil == 'bajo'].vacias_por_100_hogares_nuevos_11_21.min():,.0f} "
          f"a {por[por.tercil == 'bajo'].vacias_por_100_hogares_nuevos_11_21.max():,.0f}.", "C1", por[por.tercil == "alto"].vacias_por_100_hogares_nuevos_11_21.median(),
          "vacías por 100 hogares nuevos", por[por.tercil == "alto"].vacias_por_100_hogares_nuevos_11_21.min(),
          por[por.tercil == "alto"].vacias_por_100_hogares_nuevos_11_21.max(), F3,
          "Hogares nuevos = viviendas principales Censo 2021 − Censo 2011, emparejando por nombre de municipio (solo nombres únicos).",
          "El emparejamiento por nombre es aproximado; el denominador es pequeño en municipios con poco crecimiento. Las vacías del Censo 2011 (declaradas) y 2021 "
          f"(consumo eléctrico) no son comparables: total {cob['vacias_total_nacional_censo2011']:,.0f} frente a {cob['vacias_total_pais']:,.0f}.")

    # ---------------- A4
    o4 = pa_a456.a4(reg)
    for k, df in o4.items():
        guardar(df, k)
    nac = o4["A4_nacional"]
    n23 = nac[nac.anio == pa_a456.ANIO_A4]
    F4n = ["INE ADRH (renta neta media por hogar por sección, ponderada por hogares del Censo 2021)", "Contabilidad nacional (renta disponible de los hogares, Eurostat) / hogares EPA",
           "MIVAU valor tasado", "BCE tipo de interés de nuevos préstamos de vivienda"]
    hecho("A4_precio_renta_nacional_2023",
          f"Precio de una vivienda de 80 m² (valor tasado) en veces la renta anual del hogar, {pa_a456.ANIO_A4}: {n23.precio_renta.min():.2f} a {n23.precio_renta.max():.2f}; "
          f"cuota hipotecaria (80 % del precio, 25 años, tipo {n23.tipo_hipotecario_pct.iloc[0]:.2f} %) de {n23.cuota_mes.iloc[0]:,.0f} €/mes, "
          f"{n23.cuota_pct_renta.min():.1f} a {n23.cuota_pct_renta.max():.1f} % de la renta mensual del hogar.", "C1", n23.precio_renta.median(),
          "veces la renta anual", n23.precio_renta.min(), n23.precio_renta.max(), F4n,
          "80 m²; LTV 80 %; 25 años; tipo medio anual; sin gastos ni impuestos de compra.",
          "Los dos denominadores miden conceptos distintos (renta neta ADRH frente a renta disponible por hogar de la contabilidad nacional); sin cuota por edad (no hay fuente cargada de renta por edad).")
    p4 = o4["A4_provincias"]
    allr = pd.concat([p4.precio_renta_tasado, p4.precio_renta_registradores])
    allc = pd.concat([p4.cuota_pct_renta_tasado, p4.cuota_pct_renta_registradores])
    hecho("A4_precio_renta_provincias_2023",
          f"Precio/renta provincial {pa_a456.ANIO_A4} (80 m²): de {allr.min():.2f} a {allr.max():.2f} veces entre provincias y entre dos fuentes de precio "
          f"(valor tasado y Registradores); cuota hipotecaria de {allc.min():.1f} a {allc.max():.1f} % de la renta mensual del hogar.",
          "C4", allr.median(), "veces la renta anual", allr.min(), allr.max(),
          ["MIVAU valor tasado", "Registradores (precio m², datos abiertos)", "INE ADRH (única fuente de renta provincial)"],
          "Renta provincial = media ponderada por hogares censales de las secciones con dato.", "Renta provincial de fuente única (ADRH): hecho de fuente única en el denominador.")
    a_s = p4.alquiler_pct_renta_serpavi.dropna()
    a_i = p4.alquiler_pct_renta_incasol.dropna()
    hecho("A4_alquiler_renta_provincias_2023",
          f"Alquiler anual (80 m², mediana SERPAVI) en % de la renta del hogar: {a_s.min():.1f} a {a_s.max():.1f} % entre provincias; en las 4 provincias catalanas, "
          f"con las fianzas de Incasòl: {a_i.min():.1f} a {a_i.max():.1f} % (SERPAVI en las mismas: "
          f"{p4[p4.alquiler_pct_renta_incasol.notna()].alquiler_pct_renta_serpavi.min():.1f} a {p4[p4.alquiler_pct_renta_incasol.notna()].alquiler_pct_renta_serpavi.max():.1f} %).",
          "C4", a_s.median(), "% de la renta anual", min(a_s.min(), a_i.min()), max(a_s.max(), a_i.max()),
          ["MIVAU SERPAVI (contratos declarados en el IRPF; stock)", "Incasòl fianzas (flujo, solo Cataluña)", "INE ADRH (única fuente de renta)"],
          "SERPAVI en €/m² por mes × 80; Incasòl = media ponderada de las bandas por contratos, año natural 2023.",
          "SERPAVI es stock de contratos y las fianzas son flujo; renta de fuente única (C4).")

    # ---------------- A5
    t5 = pa_a456.a5(reg)
    guardar(t5, "A5_tenencia_edad")
    def val(f, a, e, c="propietario"):
        x = t5[(t5.fuente.str.startswith(f)) & (t5.anio == a) & (t5.edad == e) & (t5.categoria.str.startswith(c))]
        return x.pct_min.min(), x.pct_max.max()
    j = [val("EFF", 2022, "<35", "propietario"), val("INE ECV", 2022, "De 16 a 29 años"), val("INE ECV", 2022, "De 30 a 44 años")]
    hecho("A5_propiedad_jovenes_2022",
          f"Hogares propietarios de su vivienda principal en 2022: EFF, persona de referencia de menos de 35 años: {j[0][0]:.1f} %; ECV, de 16 a 29 años: {j[1][0]:.1f} %; "
          f"ECV, de 30 a 44 años: {j[2][0]:.1f} %. Rango entre las dos fuentes para el tramo más joven: {min(j[0][0], j[1][0]):.1f} a {max(j[0][1], j[1][1]):.1f} %.",
          "C1", (j[0][0] + j[1][0]) / 2, "% de hogares", min(j[0][0], j[1][0]), max(j[0][1], j[1][1]),
          ["Banco de España, EFF (tablas publicadas, EFF2022)", "INE ECV, tabla 9994"], "Edad de la persona de referencia; los tramos de las fuentes no coinciden (EFF <35; ECV 16-29).",
          "Sin error muestral en los ficheros extraídos (el campo error_max es de validación de la extracción, no muestral).")
    m = [val("EFF", 2022, "65-74"), val("EFF", 2022, "75+"), val("INE ECV", 2022, "65 y más años"), val("Eurostat", 2022, "65+")]
    lo, hi = min(x[0] for x in m), max(x[1] for x in m)
    hecho("A5_propiedad_65_mas_2022",
          f"Hogares propietarios cuya persona de referencia tiene 65 años o más (2022): EFF 65-74 {m[0][0]:.1f} %, EFF 75+ {m[1][0]:.1f} %, ECV {m[2][0]:.1f} %, "
          f"Eurostat (adultos solos de 65+) {m[3][0]:.1f} %.", "C1", float(np.mean([x[0] for x in m])), "% de hogares", lo, hi,
          ["Banco de España, EFF", "INE ECV, tabla 9994", "Eurostat ilc_lvho02"], "Tramos y unidades de los tres no coinciden; Eurostat solo adultos que viven solos.",
          "Eurostat no desagrega por edad de la persona de referencia de otros tipos de hogar.")
    tot = [val("EFF", 2022, "total"), val("INE ECV", 2022, "Total"), val("INE ECV", 2021, "Total"), val("Censo", 2021, "total")]
    lo, hi = min(x[0] for x in tot), max(x[1] for x in tot)
    hecho("A5_propiedad_total",
          f"Hogares propietarios, todas las edades: EFF 2022 {tot[0][0]:.1f} %, ECV 2022 {tot[1][0]:.1f} %, ECV 2021 {tot[2][0]:.1f} %, Censo 2021 {tot[3][0]:.1f} %.",
          "C1", float(np.mean([x[0] for x in tot])), "% de hogares", lo, hi, ["Banco de España, EFF", "INE ECV", "INE Censo 2021"],
          "Censo 2021: viviendas principales en propiedad sobre principales (secciones).", "Fechas de referencia distintas (2021 y 2022).")
    e08, e22 = val("EFF", 2008, "<35"), val("EFF", 2022, "<35")
    c08, c22 = val("INE ECV", 2008, "De 16 a 29 años"), val("INE ECV", 2022, "De 16 a 29 años")
    hecho("A5_cambio_propiedad_jovenes_2008_2022",
          f"Variación 2008-2022 de la proporción de hogares jóvenes propietarios: EFF <35 de {e08[0]:.1f} a {e22[0]:.1f} % ({e22[0] - e08[0]:+.1f} puntos); "
          f"ECV 16-29 de {c08[0]:.1f} a {c22[0]:.1f} % ({c22[0] - c08[0]:+.1f} puntos).", "C1", (e22[0] - e08[0] + c22[0] - c08[0]) / 2, "puntos porcentuales",
          min(e22[0] - e08[0], c22[0] - c08[0]), max(e22[0] - e08[0], c22[0] - c08[0]),
          ["Banco de España, EFF", "INE ECV, tabla 9994"], "Tramos de edad distintos entre fuentes.", "Efecto de composición del tramo de edad no separado.")

    # ---------------- A6
    o6 = pa_a456.a6(reg)
    for k, df in o6.items():
        guardar(df, k)
    rn = o6["A6_ratio_nacional"].set_index("anio")
    ch_idx = 100 * (rn.loc[2024, "ratio_ipv_ipc_base2015"] / rn.loc[2015, "ratio_ipv_ipc_base2015"] - 1)
    ch_niv = 100 * (rn.loc[2024, "ratio_niveles_tasado_serpavi"] / rn.loc[2015, "ratio_niveles_tasado_serpavi"] - 1)
    hecho("A6_ratio_precio_alquiler_2015_2024",
          f"Variación 2015-2024 de la razón precio/alquiler: {ch_idx:+.1f} % con el cociente de índices IPV/IPC de alquiler; {ch_niv:+.1f} % con el cociente de niveles "
          f"valor tasado/(SERPAVI×12) (de {rn.loc[2015, 'ratio_niveles_tasado_serpavi']:.1f} a {rn.loc[2024, 'ratio_niveles_tasado_serpavi']:.1f} años de alquiler). "
          "Las dos medidas difieren en el signo.", "C1", (ch_idx + ch_niv) / 2, "% de variación", min(ch_idx, ch_niv), max(ch_idx, ch_niv),
          ["INE IPV e IPC alquiler (cociente de índices)", "MIVAU valor tasado y SERPAVI (niveles)"],
          "Medias anuales; SERPAVI nacional asignado por año.",
          "El IPC de alquiler mide el stock completo de alquileres; SERPAVI es el stock declarado en el IRPF; ambos amortiguan los cambios de contratos nuevos. "
          "Si dos métodos discrepan se informan los dos.")
    uc = o6["A6_coste_uso"]
    u23 = uc[uc.anio == 2023]
    hecho("A6_coste_uso_poterba_2023",
          f"Coste de uso anual de la vivienda propia en 2023 (Poterba, sin deducción fiscal): {u23.coste_uso_pct.min():.1f} a {u23.coste_uso_pct.max():.1f} % del precio "
          f"(depreciación 1-3 %, impuesto 0,5 %, ganancia esperada = 0, inflación o IPV medio de 4 años); equivale a {u23.coste_uso_sobre_alquiler.min():.2f} a "
          f"{u23.coste_uso_sobre_alquiler.max():.2f} veces el alquiler mensual SERPAVI de 80 m².", "C4", u23.coste_uso_pct.median(), "% del precio por año",
          u23.coste_uso_pct.min(), u23.coste_uso_pct.max(),
          ["BCE tipo de nuevos préstamos de vivienda (v2)", "MIVAU valor tasado y SERPAVI", "INE IPV"],
          "Depreciación 1, 2 y 3 %; impuesto sobre el inmueble 0,5 %; ganancia esperada igual a 0, a la inflación del deflactor o al crecimiento medio del IPV en 4 años.",
          "El rango se debe a los supuestos, no a error de medida; el tipo procede de una sola serie (C4).")

    # ---------------- figuras
    f1, ax = plt.subplots(figsize=(9, 4.5))
    r = r1.reset_index(drop=True)
    x = np.arange(len(r))
    med = [t1[(t1.periodo == p) & t1.protegida.isin(["con", "incluida"])].deficit.median() for p in r.periodo]
    ax.vlines(x, r.min_total / 1e3, r.max_total / 1e3, color="k", lw=6, alpha=.35, label="rango de combinaciones")
    ax.plot(x, np.array(med) / 1e3, "ko", label="mediana")
    ax.scatter([list(r.periodo).index("2021-2025")], [pa_a1.BDE["cifra"] / 1e3], marker="D", color="C3", label="BdE IA 2025 (≈750 mil)")
    ax.axhline(0, color="gray", lw=.6)
    ax.set_xticks(x, r.periodo, rotation=30)
    ax.set_ylabel("miles de viviendas")
    ax.set_title("A1 déficit contable acumulado, nacional (con protegida)")
    ax.legend(fontsize=8)
    f1.tight_layout()
    f1.savefig(FIG / "A1_deficit_nacional.png", dpi=130)
    plt.close(f1)

    f2, ax = plt.subplots(1, 2, figsize=(10, 4))
    for (fu, ed, lab) in (("EFF", "<35", "EFF <35"), ("INE ECV", "De 16 a 29 años", "ECV 16-29"), ("INE ECV", "De 30 a 44 años", "ECV 30-44"),
                          ("EFF", "35-44", "EFF 35-44")):
        d = t5[(t5.fuente.str.startswith(fu)) & (t5.edad == ed) & t5.categoria.str.startswith("propiet")].sort_values("anio")
        ax[0].plot(d.anio, d.pct_min, marker="o" if fu == "EFF" else None, ms=4, label=lab)
    ax[0].set_ylabel("% de hogares propietarios")
    ax[0].set_title("A5 propiedad por edad de la persona de referencia")
    ax[0].legend(fontsize=7)
    d = t3[(t3.muestra == "todos con dato") & t3.tercil.isin(["bajo", "medio", "alto"]) & t3.presion.str.startswith("Δ ln valor tasado 2015")]
    for i, mname in enumerate(d.medida_vacia.unique()):
        dd = d[d.medida_vacia == mname].set_index("tercil").reindex(["bajo", "medio", "alto"])
        ax[1].bar(np.arange(3) + i * .27, dd.pct_vacias_de_la_muestra, width=.27, label=mname[:28])
    ax[1].set_xticks(np.arange(3) + .27, ["bajo", "medio", "alto"])
    ax[1].set_title("A3 % de vacías por tercil de Δ valor tasado 2015-21")
    ax[1].legend(fontsize=7)
    f2.tight_layout()
    f2.savefig(FIG / "A5_A3_tenencia_vacancia.png", dpi=130)
    plt.close(f2)

    f3, ax = plt.subplots(figsize=(8, 4))
    ax.plot(rn.index, rn.ratio_ipv_ipc_base2015, label="IPV / IPC alquiler (2015=100)")
    ax.plot(rn.index, rn.ratio_niveles_base2015, label="valor tasado / SERPAVI (2015=100)")
    ax.set_title("A6 razón precio/alquiler, dos medidas")
    ax.legend()
    f3.tight_layout()
    f3.savefig(FIG / "A6_ratio_precio_alquiler.png", dpi=130)
    plt.close(f3)

    # ---------------- salidas json
    (OUT / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1))
    reg.flush()
    resultado = {
        "rama": "PA", "capa": "C1",
        "pregunta": "Qué magnitudes contables y descriptivas del problema de la vivienda (déficit, demanda latente, vacancia, esfuerzo de acceso, tenencia, precio/alquiler) están medidas con ≥2 fuentes y con qué rango",
        "datos": "MIVAU (fin de obra, parque, protegida, valor tasado, SERPAVI), INE (EPA, ECP, Censos 2011/2021, tabla 59531, ADRH, IPV, IPC), Catastro, Eurostat, BdE (EFF), ECV, Registradores, Incasòl",
        "N": {"hechos": len(HECHOS), "provincias": 52, "municipios_vacancia": int(cob["n_municipios_publicados"])},
        "metodo": "Descriptivo/contable; rango entre combinaciones de fuentes; sin contrastes de hipótesis ni estimación causal",
        "estimacion": {h["id"]: {"magnitud": h["magnitud"], "unidad": h["unidad"]} for h in HECHOS},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO (capa C1 con ≥2 fuentes; los hechos de fuente única van como C4)",
        "diagnosticos": {"cuadre_censo2021_vacias_suma_unidades_igual_total_nacional": bool(abs(pdat.vacias2021().vacias.sum() - cob["vacias_total_pais"]) < 1),
                         "comparacion_BdE": bde, "cobertura_vacancia": cob,
                         "fdr": "No aplica: no hay contrastes de hipótesis (no hay p-valores)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "C1 no predice: sin validación fuera de muestra"},
        "notas": ["La cifra del BdE DO 2432 no es de déficit (trata del alquiler); la comparación usa el Informe Anual 2025 (≈750.000, 2021-2025).",
                  "Interpolaciones: ninguna propia; EPA 2002Q1 como base del periodo 2002-2007 (marcado).",
                  "No encontrado: Censo 2021 por relación con la persona de referencia y tramos 25-34; renta por edad (ECV/EES); error muestral publicado de EPA, ECV y EFF no disponible en los ficheros.",
                  "ECP anclada al Censo 2021 (no independiente de él)."],
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=float))
    print(f"hechos={len(HECHOS)} registro={len(reg.rows)}")


if __name__ == "__main__":
    main()
