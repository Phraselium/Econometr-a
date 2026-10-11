"""T1 · Bajas del parque residencial (salidas netas) por provincia y año, 2011-2025. Determinista, sin red.

Tres métodos: (a) identidad de stock Censo 2011 + terminadas - Censo 2021; (b) Catastro (altas de
unidades urbanas residenciales frente a terminadas); (c) licencias de demolición del Ministerio.
Detalle en output/v5_1/T1/metodo.md. Uso: python3 src/v5_1/t1_run.py [--smoke]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in ("src", "src/v3", "src/v4", "src/v5"):
    sys.path.insert(0, str(RAIZ / p))
import b1_run as b1  # noqa: E402
import econ_utils  # noqa: E402
import m1_run as m1  # noqa: E402
import pa_data as pdat  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
LIC = RAW / "v5_1" / "t1"
OUT = RAIZ / "output" / "v5_1" / "T1"
SMOKE = "--smoke" in sys.argv
FOR = ["01", "20", "31", "48"]
MARGEN_PP = 0.05          # margen de coincidencia: ±0,05 pp anuales (≈ ±13.500 viviendas/año = 15 % de 90.000 terminadas)
VENT = 2 / 12 + 9         # 1-nov-2011 a 1-ene-2021 (años)
CCAA_FILE = {1: ["04", "11", "14", "18", "21", "23", "29", "41"], 2: ["22", "44", "50"], 3: ["33"], 4: ["07"],
             5: ["35", "38"], 6: ["39"], 7: ["02", "13", "16", "19", "45"], 8: ["05", "09", "24", "34", "37", "40", "42", "47", "49"],
             9: ["08", "17", "25", "43"], 10: ["03", "12", "46"], 11: ["06", "10"], 12: ["15", "27", "32", "36"],
             13: ["28"], 14: ["30"], 15: ["31"], 16: ["01", "20", "48"], 17: ["26"], 18: ["51"], 19: ["52"]}
FECHAS = {
    "censo2011": "INE Censo 2011 (tabla 3457), referencia 1-nov-2011",
    "censo2021": "INE Censo 2021 (tabla 59525), referencia 1-ene-2021 (la fecha 2021-11-01 del manifiesto es la de publicación)",
    "terminadas": "MIVAU Boletín Online, tablas 3.2 (libres) y 1.6 (protegida), hasta dic-2025",
    "catastro": "Catastro estadísticas urbanas, ejercicios 2012-2025 (1-ene de cada ejercicio)",
    "licencias": "MIVAU Boletín Online, licencias municipales de obra (tablas 6 y 10), serie anual 2000-2024; CCAA hasta 2022",
}


def leer_licencias_anual(f: Path, col: dict[str, int]) -> pd.DataFrame:
    d = pd.read_excel(f, header=None)
    y = pd.to_numeric(d[0], errors="coerce")
    a = d[y.between(1990, 2030) & (d[1].isna() | (pd.to_numeric(d[1], errors='coerce') == y))].copy()
    a["anio"] = y[a.index].astype(int)
    a = a.drop_duplicates("anio").set_index("anio")
    out = pd.DataFrame({k: pd.to_numeric(a[c], errors="coerce") for k, c in col.items()})
    return out.sort_index()


def escribir_entregables(R, comp, desc, pnp, bj, D, base, nacB, nacC, L) -> None:
    pc = lambda x: round(100 * x, 4)  # noqa: E731
    d = {(r.periodo, r.escenario): r for r in D.itertuples()}
    d24c, d24lo, d24hi = d[("2021-2024", "estimada_tasa_central")], d[("2021-2024", "estimada_tasa_min")], d[("2021-2024", "estimada_tasa_max")]
    d25c, d25lo, d25hi = d[("2021-2025", "estimada_tasa_central")], d[("2021-2025", "estimada_tasa_min")], d[("2021-2025", "estimada_tasa_max")]
    s24a, s24b = d[("2021-2024", "supuesto_0,1%")], d[("2021-2024", "supuesto_0,2%")]
    s25a, s25b = d[("2021-2025", "supuesto_0,1%")], d[("2021-2025", "supuesto_0,2%")]
    cen = 100 * R["central_nac"]
    mx = 100 * R["max_nac"]
    f = lambda x: f"{x:,.0f}".replace(",", ".")  # noqa: E731
    H = []

    def h(i, ind, v, lo, hi, u, per, cob, fu, capa, fd):
        H.append({"id": i, "indicador": ind, "valor": v, "min": lo, "max": hi, "unidad": u, "periodo": per, "cobertura": cob,
                  "fuentes": fu, "capa": capa, "fecha_dato": fd})
    h("T1-H1", "Bajas netas implícitas en la identidad Censo 2011 + terminadas - Censo 2021 (negativas)", round(R["sA"] / VENT),
      round(-R["A_libres"] / VENT), round(R["sA"] / VENT), "viviendas/año (negativo = el parque creció más que las terminadas)",
      "1-nov-2011 a 1-ene-2021", "España (52 provincias)", ["INE Censo 2011 t3457", "INE Censo 2021 t59525", "MIVAU 3.2 y 1.6"], "C4",
      "2021-01-01")
    h("T1-H2", "Tasa anual implícita de la identidad de Censos (negativa)", pc(R["tasaA_nac"]), None, None, "% del parque al año",
      "1-nov-2011 a 1-ene-2021", "España", ["INE Censos 2011 y 2021", "MIVAU"], "C4", "2021-01-01")
    h("T1-H3", "Altas netas no explicadas por las terminadas del Ministerio", round(R["G"]), round(R["cat_extra"]), round(R["G"]), "viviendas",
      "1-nov-2011 a 1-ene-2021", "España; la parte catastral solo en territorio común", ["INE Censos", "MIVAU", "Catastro"], "C4", "2021-01-01")
    h("T1-H4", "Tasa anual Catastro-terminadas, territorio común (negativa)", pc(R["tasa_B_nac"]), None, None, "% del parque al año",
      "2012-2020", "España sin País Vasco ni Navarra", ["Catastro urbana", "MIVAU"], "C4", "2021-01-01")
    h("T1-H5", "Tasa anual Catastro-terminadas, territorio común", pc(R["tB1924"]), None, None, "% del parque al año",
      "2019-2024", "España sin País Vasco ni Navarra", ["Catastro urbana", "MIVAU"], "C4", "2025-01-01")
    h("T1-H6", "Viviendas con licencia de demolición (total y parcial) al año", round(R["L_media_1224"]["D_estrecha"]),
      round(R["L_media_1224"]["D_estrecha"]), round(R["L_media_1224"]["D_amplia"]), "viviendas/año", "media 2012-2024", "España",
      ["MIVAU licencias municipales de obra, tablas 6 y 10"], "C4", "2024-12-31")
    h("T1-H7", "Viviendas con licencia de demolición en 2024", R["L2024"]["D_estrecha"], R["L2024"]["D_estrecha"], R["L2024"]["D_amplia"],
      "viviendas", "2024", "España", ["MIVAU licencias, tablas 6 y 10"], "C4", "2024-12-31")
    h("T1-H8", "Tasa anual de bajas (licencias de demolición, media 2015-2024)", round(cen, 4), 0.0, round(mx, 4), "% del parque al año",
      "2015-2024", "España (reparto provincial por parque)", ["MIVAU licencias", "MIVAU parque"], "C4", "2024-12-31")
    h("T1-H9", "Déficit contable 2021-2024 con bajas estimadas (ECP, con protegida)", round(d24c.deficit), round(d24lo.deficit),
      round(d24hi.deficit), "viviendas", "2021-2024", "España", ["M0", "A4", "MIVAU licencias"], "C4", "2024-12-31")
    h("T1-H10", "Déficit contable 2021-2025 con bajas estimadas (ECP, con protegida)", round(d25c.deficit), round(d25lo.deficit),
      round(d25hi.deficit), "viviendas", "2021-2025", "España", ["M0", "A4", "MIVAU licencias"], "C4", "2025-12-31")
    (OUT / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1), encoding="utf-8")

    res = {
        "rama": "T1",
        "pregunta": "¿Cuántas viviendas salen cada año del parque residencial (bajas netas) por provincia, 2011-2025?",
        "capa": "C4 (las identidades de stock dan bajas negativas y no miden bajas; las licencias son fuente única); cota física 0 (C2)",
        "datos": ["INE Censo 2011 (t3457) y Censo 2021 (t59525)", "MIVAU terminadas libres y protegidas, parque",
                  "Catastro urbana municipios 2012-2025", "MIVAU licencias municipales de obra (tablas 6, 10 y CCAA)"],
        "N": {"provincias": R["nprov"], "anios_B": 13, "anios_C_nacional": 14},
        "metodo": "a) identidad de stock con Censos; b) Catastro menos terminadas; c) licencias de demolición del Ministerio; margen de coincidencia ±0,05 pp anuales",
        "estimacion": {"tasa_nacional_pct_anual": {"min": 0.0, "central": round(cen, 4), "max": round(mx, 4), "periodo": "2015-2024", "capa": "C4"},
                       "identidad_censos_pct_anual": pc(R["tasaA_nac"]), "catastro_pct_anual_2012_2020": pc(R["tasa_B_nac"]),
                       "catastro_pct_anual_2019_2024": pc(R["tB1924"]),
                       "licencias_viviendas_anio_2024": R["L2024"],
                       "deficit_2021_2024": {"central": round(d24c.deficit), "rango": [round(d24lo.deficit), round(d24hi.deficit)]},
                       "deficit_2021_2025": {"central": round(d25c.deficit), "rango": [round(d25lo.deficit), round(d25hi.deficit)]}},
        "ic95": None,
        "p_ajustado": {k: v for k, v in R["padj"].items()},
        "nivel_evidencia": "EXPLORATORIO (C4); sin lenguaje causal",
        "diagnosticos": {"coinciden_a_b_dentro_margen": bool(R["dif_ab"] <= MARGEN_PP), "dif_a_b_pp": round(R["dif_ab"], 3),
                         "dif_a_c_pp": round(R["dif_ac"], 3), "dif_b_c_pp": round(R["dif_bc"], 3),
                         "dif_b_c_2019_2024_pp": [round(x, 3) for x in R["dif_bc1924"]],
                         "provincias_con_bajas_negativas_A": R["n_neg_A"], "provincias_con_bajas_negativas_B": f"{R['n_neg_B']} de {R['n_B']}",
                         "ratio_UU_catastro_censo2021": round(R["ratio_uu"], 3), "control_sumas": "output/v5_1/T1/control_sumas.json"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Cálculo contable, no modelo predictivo: no aplica AR(4)/ECM v1. Los p son t de una muestra entre provincias (H0 tasa media = 0) con Holm, solo descriptivos. "
                 "Licencias provinciales no existen en el Boletín: reparto CCAA por parque; CCAA hasta 2022, 2023-2024 con cuota media 2019-2022 y 2025 repetido de 2024 (marcados).",
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")

    fic = [{
        "id": "T1-V1", "tema": "Bajas del parque",
        "enunciado": "En España apenas se derriban viviendas / las bajas del parque son despreciables.",
        "capa": "C4",
        "magnitud": (f"Licencias de demolición del Ministerio: {f(R['L2024']['D_estrecha'])}-{f(R['L2024']['D_amplia'])} viviendas en 2024 y "
                     f"{f(R['L_media_1224']['D_estrecha'])}-{f(R['L_media_1224']['D_amplia'])} de media en 2012-2024, es decir {cen:.3f} % del parque al año "
                     f"(0,02-0,04 %), frente al 0,1-0,2 % supuesto antes. No incluye ruina, cambios de uso, agregaciones ni derribos sin licencia. "
                     f"Las identidades de Censos y Catastro dan bajas negativas ({pc(R['tasaA_nac'])} % y {pc(R['tasa_B_nac'])} % al año en 2011-2020) y no acotan por arriba."),
        "intervalo": f"0-{mx:.3f} % del parque al año (C4)",
        "cota": "C2 solo la cota física inferior (bajas >= 0); sin cota superior medida",
        "literatura": "—",
        "veredicto": "ANALIZADA, NO CONCLUYENTE",
        "regla": "Una sola fuente para el nivel (licencias del Ministerio) y los métodos de stock no miden bajas: capa C4. Lo licenciado es pequeño frente al parque; el total de salidas no está medido.",
        "limites": "Licencia no es derribo ejecutado; faltan ruina, cambio de uso, agregaciones y obras sin licencia; reparto provincial por parque.",
        "evidencia": ["output/v5_1/T1/tablas/comparacion_metodos.csv", "output/v5_1/T1/tablas/licencias_demolicion_nacional.csv",
                      "output/v5_1/T1/tablas/identidad_descomposicion.csv"],
    }]
    (OUT / "fichas_verificador.json").write_text(json.dumps(fic, ensure_ascii=False, indent=1), encoding="utf-8")

    cm_ = comp.copy()
    tabla = "\n".join(f"| {r.metodo} | {r.tasa_anual_pct:.3f} | {f(r.viviendas_anio)} | {r.signo} |" for r in cm_.itertuples())
    dd = "\n".join(f"| {r.concepto.strip()} | {f(r.viviendas)} |" for r in desc.itertuples())
    pn = "\n".join(f"| {r.concepto} | {f(r.censo_2011)} | {f(r.censo_2021)} | {f(r.variacion)} |" for r in pnp.itertuples())
    dtab = "\n".join(f"| {r.periodo} | {r.escenario} | {f(r.bajas)} | {f(r.deficit)} |" for r in D.itertuples())
    md = f"""# T1 · método

Bajas del parque residencial (salidas netas), 2011-2025, en viviendas y % del parque. Cifras con fecha: {FECHAS['censo2011']}; {FECHAS['censo2021']}; {FECHAS['terminadas']}; {FECHAS['catastro']}; {FECHAS['licencias']}.

## (a) Identidad de stock con los Censos
Bajas = Parque_Censo2011 + Terminadas(1-nov-2011 a 31-dic-2020) - Parque_Censo2021. Tasa anual = Bajas / (ventana x Parque_2011), ventana = 9,17 años.

- Fecha de referencia: el Censo 2021 se refiere a 1-ene-2021 (el manifiesto del repositorio anota 2021-11-01, que es la fecha de publicación de la descarga). Lo corrobora que el parque MIVAU a 31-dic-2020 (26.623.708) coincide con V_TOTAL del Censo 2021. El Censo 2011 se refiere a 1-nov-2011. Ventana de terminadas: nov-dic 2011 (libres mensuales; protegida a prorrata 2/12 del año, supuesto) más 2012-2020.
- Corrección respecto a B1: B1 sumaba terminadas 2012-2021 (un año de más, {f(desc.viviendas.iloc[7])} viviendas netas de la ventana correcta). Con la ventana de B1 las bajas implícitas son {f(R['A_b1'])}; con la correcta, {f(R['sA'])}. B1 no cambia de signo (siguen negativas).
- Definiciones: ambos Censos cuentan viviendas familiares (total = principales + no principales). Según el encargo, el Censo 2011 se obtuvo con encuesta y muestra y el 2021 con registros y Catastro (no verificado en el repositorio); esa diferencia de cobertura no se puede medir con datos del repositorio y es la causa principal admitida del residuo (se cuantifica por diferencia, no por medición). Descomposición del principal/no principal:

| concepto | Censo 2011 | Censo 2021 | variación |
|---|---|---|---|
{pn}

- Terminadas: MIVAU libres (3.2) + protegidas (calificaciones definitivas, 1.6). Solo libres: bajas implícitas {f(R['A_libres'])}.

| concepto | viviendas |
|---|---|
{dd}

Lectura: bajas negativas. El parque de los Censos creció {f(R['G'])} viviendas más de lo que explican las terminadas del Ministerio. Como mucho {f(R['cat_extra'])} (territorio común) se corresponden con altas catastrales sin terminadas (regularizaciones y viviendas aflorando); el resto ({f(R['G_com'] - R['cat_extra'])} en territorio común y {f(R['G_for'])} en las cuatro provincias forales) es cobertura censal, vivienda no registrada que aflora, rehabilitaciones que recuperan viviendas, cambios de uso a vivienda o terminadas no certificadas, sin separar. Provincias con bajas implícitas negativas: {R['n_neg_A']} de {R['nprov']}.

## (b) Catastro
Bajas(y) = Terminadas MIVAU(y) - [UU(1-ene-y+1) - UU(1-ene-y)], UU = unidades urbanas residenciales de los municipios presentes en todos los ejercicios 2012-2025, territorio común. UU / viviendas del Censo 2021 = {R['ratio_uu']:.3f}: no son la misma unidad, la comparación es de variaciones. Resultados anuales en tablas/bajas_nacional_B.csv y por provincia en tablas/catastro_bajas_provincia_anio.csv. Negativas en 2012-2017 (regularizaciones y actualización catastral, como en M0) y cercanas a 0 en 2018-2024, donde coincide con las terminadas por construcción de M0 (la coincidencia MIVAU-Catastro es el criterio de M0): no es una confirmación independiente de una baja pequeña. Provincias con bajas 2012-2020 negativas: {R['n_neg_B']} de {R['n_B']}.

## (c) Licencias de obra del Ministerio
Boletín Online, licencias municipales de obra: tabla 10 (viviendas a demoler en demolición total + viviendas suprimidas en demolición parcial) = definición estrecha; tabla 6 columna (3) (viviendas, obras de demolición total) = definición amplia. Coinciden hasta 2018; desde 2019 la amplia es mayor ({f(R['L2024']['D_amplia'])} frente a {f(R['L2024']['D_estrecha'])} en 2024) sin explicación en la fuente. Nivel provincial: no existe; hay CCAA hasta 2022, y se reparte por el parque provincial MIVAU (reparto, no medida). 2023-2024: cuota CCAA media 2019-2022; 2025: no publicado, se repite 2024 (marcado). Ceuta y Melilla: sin dato, tasa media del resto. La suma provincial es igual al total nacional (control_sumas.json). Una licencia no es un derribo ejecutado y no incluye ruina, cambios de uso ni agregaciones.

## Comparación (margen ±0,05 pp anuales, declarado antes de ver los resultados: equivale a unas 13.500 viviendas/año, el 15 % de 90.000 terminadas, la tolerancia de M0)

| método | tasa anual (%) | viviendas/año | signo |
|---|---|---|---|
{tabla}

- a vs b: diferencia {R['dif_ab']:.3f} pp (fuera del margen, ambas negativas). a vs c: {R['dif_ac']:.3f} pp. b vs c 2012-2020: {R['dif_bc']:.3f} pp. b vs c 2019-2024: {R['dif_bc1924'][0]:.3f} y {R['dif_bc1924'][1]:.3f} pp (dentro del margen, pero b es neta de altas catastrales y coincide con las terminadas por construcción de M0).
- Resultado: los métodos no coinciden en 2011-2020. Rango C4: 0 a {mx:.3f} % del parque al año (0 es la cota física; el máximo es el máximo anual 2011-2024 de la definición amplia). Causa de la discrepancia: a y b miden altas netas no certificadas, no bajas; solo c es positiva y es fuente única.
- Capa: ningún método supera C4 como nivel de bajas. C1 requiere dos fuentes independientes con componentes C1 y aquí solo licencias miden bajas; C2 requeriría cota superior, que las identidades no dan (las altas no certificadas son un sumando desconocido, de modo que b es una cota inferior de las bajas si esas altas son >= 0).
- Contraste de tasas medias provinciales (H0: media = 0, t de una muestra, Holm): {', '.join(f'{k}: p_aj={v:.2g}' for k, v in R['padj'].items())}. Descriptivo; las bajas de a y b son significativamente negativas, lo que confirma que no miden bajas.

## Sustitución del supuesto de bajas en el déficit
Déficit contable = delta de hogares (ECP) - terminadas (libres + protegida) + bajas, con bajas = tasa provincial x parque MIVAU a 1 de enero de cada año (tablas/bajas_provincia.csv: tasa_min = 0, central = media de las dos definiciones de licencia 2015-2024, max = máximo anual de la definición amplia 2011-2024). Base sin bajas: A4 / M0.

| periodo | escenario | bajas acumuladas | déficit |
|---|---|---|---|
{dtab}

Con las bajas licenciadas el déficit 2021-2024 queda en {f(d24c.deficit)} (rango {f(d24lo.deficit)}-{f(d24hi.deficit)}) y el 2021-2025 en {f(d25c.deficit)} ({f(d25lo.deficit)}-{f(d25hi.deficit)}), frente a {f(s24a.deficit)}-{f(s24b.deficit)} y {f(s25a.deficit)}-{f(s25b.deficit)} con el supuesto de 0,1-0,2 %. La capa pasa de C2 a C4 (la parte de bajas es de fuente única). El extremo del supuesto antiguo no queda respaldado por ningún método, pero tampoco refutado: ruina, cambios de uso y agregaciones no están medidos.

## Fuera de alcance / no probado
Censo 2011 de edificios en estado ruinoso, Estadística de Construcción de Edificios del INE y registros autonómicos de derribos: no probados en esta tarea.
"""
    (OUT / "metodo.md").write_text(md, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    _, nombres = m1.provincias_ecp()
    cods = sorted(nombres)
    if SMOKE:
        cods = ["46", "28", "52", "31"]
    # -------------------------------------------------- stocks
    c11 = pdat.censo2011_provincias()
    cm = pdat.censo2021_municipios().copy()
    cm["cod_prov"] = cm.index.str[:2]
    c21 = cm.groupby("cod_prov")[["V_TOTAL", "V_PRINCIPAL", "V_NOPRINCIPAL"]].sum()
    n11 = pdat.censo2011_nacional()
    base = pd.DataFrame({"cod_prov": cods, "provincia": [nombres[c] for c in cods]}).set_index("cod_prov")
    base["viv_2011"] = [c11.loc[pdat.clave(nombres[c]), "Total viviendas"] for c in cods]
    base["princ_2011"] = [c11.loc[pdat.clave(nombres[c]), "Vivienda principal"] for c in cods]
    base["viv_2021"] = c21.V_TOTAL.reindex(base.index)
    base["princ_2021"] = c21.V_PRINCIPAL.reindex(base.index)
    # parque MIVAU provincial (stock a 31-dic; el de 2020 coincide con el Censo 2021)
    mp = pd.read_csv(RAW / "mivau_parque.csv")
    park = b1.serie_prov(mp.assign(serie=mp.serie.str.replace("parque_total_viviendas", "parque")), "parque", nombres,
                         {c: m1.UNIPROV_PROT.get(c) for c in cods})
    park = park.reindex(cods)
    park.columns = park.columns.astype(int)
    # Asturias: el nombre del parque lleva un espacio; Ceuta y Melilla vienen agrupadas (se reparten por el Censo 2021)
    pall = mp[mp.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])].pivot_table(index="territorio", columns="periodo", values="valor", aggfunc="first")
    pall.columns = pall.columns.astype(int)
    for c, nm in (("33", "Asturias (Principado de )"), ("33", "Asturias (Principado de)")):
        if c in cods and park.loc[c].isna().all() and nm in pall.index:
            park.loc[c] = pall.loc[nm]
    cym = [t for t in pall.index if "Ceuta" in t]
    if cym and "51" in cods and "52" in cods and park.loc["51"].isna().all():
        sh51 = c21.V_TOTAL["51"] / (c21.V_TOTAL["51"] + c21.V_TOTAL["52"])
        park.loc["51"] = pall.loc[cym[0]] * sh51
        park.loc["52"] = pall.loc[cym[0]] * (1 - sh51)
    # -------------------------------------------------- terminadas (MIVAU)
    mi = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    pr = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    ex_l = {c: m1.UNIPROV.get(c) for c in cods}
    ex_p = {c: m1.UNIPROV_PROT.get(c) for c in cods}
    lib = b1.serie_prov(mi, "viv_libres_terminadas_anual", nombres, ex_l).reindex(cods)
    pro = b1.serie_prov(pr, "prot_definitiva_anual", nombres, ex_p).reindex(cods).fillna(0.0)
    # libres mensuales (nov-dic 2011)
    mm = mi[mi.serie.str.contains("viv_libres_terminadas_mensual") & mi.nivel.isin(["provincia", "ccaa", "ciudad_autonoma"])]
    mm = mm[mm.periodo.isin(["2011-11", "2011-12"])].pivot_table(index="territorio", columns="periodo", values="valor", aggfunc="first")
    claves = {m1.norm(x): x for x in mm.index}
    nd11 = {}
    for c in cods:
        t = ex_l.get(c) or claves.get(m1.norm(nombres[c])) or claves.get(m1.norm(nombres[c].split("/")[0]))
        nd11[c] = float(mm.loc[t].sum()) if t in mm.index else np.nan
    nd11 = pd.Series(nd11)
    base["nov_dic_2011_libres"] = nd11
    base["prot_2011_prorrata"] = pro[2011] * 2 / 12
    ys = list(range(2012, 2021))
    base["term_libres_W"] = nd11 + lib[ys].sum(axis=1)
    base["term_prot_W"] = base.prot_2011_prorrata + pro[ys].sum(axis=1)
    base["term_W"] = base.term_libres_W + base.term_prot_W
    base["term_2021"] = lib[2021] + pro[2021]
    # -------------------------------------------------- (a) identidad de stock
    base["delta_censo"] = base.viv_2021 - base.viv_2011
    base["bajas_A"] = base.viv_2011 + base.term_W - base.viv_2021
    base["tasa_A"] = base.bajas_A / (VENT * base.viv_2011)
    # variante B1 (ventana 2012-2021 completa, tomando 2021 como 1-nov-2021): para comparar con output/v5/B1
    base["bajas_A_b1"] = base.viv_2011 + base.term_W - base.nov_dic_2011_libres - base.prot_2011_prorrata + base.term_2021 - base.viv_2021
    base["bajas_A_libres"] = base.viv_2011 + base.term_libres_W - base.viv_2021
    base["tasa_A_libres"] = base.bajas_A_libres / (VENT * base.viv_2011)
    # -------------------------------------------------- (b) Catastro
    cat = m1.catastro_stock()
    cat = cat.dropna()                       # municipios presentes en todos los ejercicios 2012-2025
    cat.columns = cat.columns.astype(int)
    catp = cat.groupby(cat.index.str[:2]).sum()
    catp = catp.reindex(cods)
    for c in FOR:
        if c in catp.index:
            catp.loc[c] = np.nan
    filasB = []
    for c in cods:
        if c in FOR or catp.loc[c].isna().all():
            continue
        for y in range(2012, 2025):
            t = lib.loc[c, y] + pro.loc[c, y]
            dU = catp.loc[c, y + 1] - catp.loc[c, y]
            filasB.append({"cod_prov": c, "anio": y, "terminadas": t, "delta_UU": dU, "bajas_B": t - dU, "UU_ini": catp.loc[c, y]})
    B = pd.DataFrame(filasB)
    B["tasa_B"] = B.bajas_B / B.UU_ini
    B["provincia"] = B.cod_prov.map(nombres)
    bw = B[B.anio.between(2012, 2020)].groupby("cod_prov")[["terminadas", "delta_UU", "bajas_B"]].sum()
    base["bajas_B_1220"] = bw.bajas_B
    base["tasa_B"] = B.groupby("cod_prov").apply(lambda g: g.bajas_B.sum() / g.UU_ini.sum(), include_groups=False)
    # -------------------------------------------------- (c) licencias
    nac6 = leer_licencias_anual(LIC / "10010600.XLS", {"nueva_viv": 2, "rehab_viv": 7, "demol_viv_t6": 8})
    nac10 = leer_licencias_anual(LIC / "10011000.XLS", {"edif_demol_total": 2, "viv_demol_total": 6, "viv_suprimidas_parcial": 9})
    L = nac6.join(nac10)
    L["D_estrecha"] = L.viv_demol_total + L.viv_suprimidas_parcial     # tabla 10
    L["D_amplia"] = L.demol_viv_t6                                       # tabla 6 (3)
    L["D_min"] = L[["D_estrecha", "D_amplia"]].min(axis=1)
    L["D_max"] = L[["D_estrecha", "D_amplia"]].max(axis=1)
    pn = pd.read_csv(RAW / "mivau_parque.csv")
    pn = pn[pn.nivel == "nacional"].set_index("periodo").valor
    pn.index = pn.index.astype(int)
    L["parque_ini"] = [pn.get(y - 1, np.nan) for y in L.index]
    L["tasa_D_estrecha"] = L.D_estrecha / L.parque_ini
    L["tasa_D_amplia"] = L.D_amplia / L.parque_ini
    L.to_csv(OUT / "tablas" / "licencias_demolicion_nacional.csv", index_label="anio")
    # CCAA -> reparto provincial
    ccaa = {}
    for k in CCAA_FILE:
        f = LIC / f"1002{k:02d}30.XLS"
        ccaa[k] = leer_licencias_anual(f, {"d": 8}).d
    CC = pd.DataFrame(ccaa)
    CC.to_csv(OUT / "tablas" / "licencias_demolicion_ccaa.csv", index_label="anio")
    anios = list(range(2011, 2026))
    share = {}
    for y in anios:
        if y in CC.index and CC.loc[y].notna().sum() >= 17 and CC.loc[y].sum() > 0:
            s = CC.loc[y].fillna(0.0)
            imput = False
        else:
            ref = CC.loc[2019:2022]
            ref = ref.fillna(0.0)
            s = ref.sum()
            imput = True
        for k in (18, 19):                  # Ceuta y Melilla sin dato de licencias: tasa media del resto
            if s[k] == 0 or pd.isna(s[k]):
                pk = {c: park.loc[c, y - 1] for c in CCAA_FILE[k] if c in cods and (y - 1) in park.columns}
                resto = [c for kk, pl in CCAA_FILE.items() if kk not in (18, 19) for c in pl if c in cods]
                if pk and resto:
                    s[k] = s.drop([18, 19]).sum() * pk[CCAA_FILE[k][0]] / park.loc[resto, y - 1].sum()
        share[y] = (s / s.sum(), imput)
    # tasa: reparto del total nacional entre CCAA según cuota; dentro de CCAA, proporcional al parque provincial
    filasC = []
    for y in anios:
        yy = min(y, int(L.index.max()))               # 2025: sin dato; se repite 2024 (marcado)
        shr, imp = share[y]
        for k, plist in CCAA_FILE.items():
            pl = [c for c in plist if c in cods]
            if not pl:
                continue
            park_ini = park.loc[pl, y - 1] if (y - 1) in park.columns else park.loc[pl, park.columns.max()]
            for c in pl:
                w = park_ini[c] / park_ini.sum()
                for lab, col in (("estrecha", "D_estrecha"), ("amplia", "D_amplia")):
                    filasC.append({"cod_prov": c, "anio": y, "def": lab, "bajas_C": L.loc[yy, col] * shr[k] * w,
                                   "parque_ini": park.loc[c, y - 1] if (y - 1) in park.columns else np.nan,
                                   "imputado_cuota": imp, "repetido_2024": y > L.index.max()})
    C = pd.DataFrame(filasC)
    C["tasa_C"] = C.bajas_C / C.parque_ini
    C["provincia"] = C.cod_prov.map(nombres)
    Cw = C.pivot_table(index=["cod_prov", "anio"], columns="def", values=["bajas_C", "tasa_C"]).reset_index()
    Cw.columns = ["_".join([x for x in c if x]) for c in Cw.columns]
    # -------------------------------------------------- tablas anuales (provincia x año)
    anual = Cw.merge(B[["cod_prov", "anio", "terminadas", "delta_UU", "bajas_B", "tasa_B"]], on=["cod_prov", "anio"], how="left")
    anual["provincia"] = anual.cod_prov.map(nombres)
    anual["bajas_A_media_anual"] = anual.cod_prov.map(base.bajas_A / VENT).where(anual.anio.between(2012, 2020))
    anual["tasa_A_media_anual"] = anual.cod_prov.map(base.tasa_A).where(anual.anio.between(2012, 2020))
    anual.to_csv(OUT / "tablas" / "bajas_provincia_anio.csv", index=False)
    # -------------------------------------------------- niveles y tasas nacionales
    sA, sB = base.bajas_A.sum(), B[B.anio.between(2012, 2020)].bajas_B.sum()
    tasaA_nac = sA / (VENT * base.viv_2011.sum())
    comun = [c for c in cods if c not in FOR]
    nacB = B.groupby("anio").agg(bajas=("bajas_B", "sum"), UU=("UU_ini", "sum"), term=("terminadas", "sum"), dU=("delta_UU", "sum"))
    nacB["tasa"] = nacB.bajas / nacB.UU
    nacC = C.groupby(["anio", "def"]).agg(bajas=("bajas_C", "sum"), parque=("parque_ini", "sum")).reset_index()
    nacC["tasa"] = nacC.bajas / nacC.parque
    nacC.to_csv(OUT / "tablas" / "bajas_nacional_C.csv", index=False)
    nacB.to_csv(OUT / "tablas" / "bajas_nacional_B.csv", index_label="anio")
    # -------------------------------------------------- descomposición de la identidad (nacional, viviendas)
    G = -sA
    tcom = base.loc[comun]
    UU12, UU21 = catp.loc[comun, 2012].sum(), catp.loc[comun, 2021].sum()
    dUU_1220 = UU21 - UU12
    term_com_1220 = float(sum((lib.loc[comun, y] + pro.loc[comun, y]).sum() for y in ys))
    cat_extra = dUU_1220 - term_com_1220
    G_com = float((tcom.viv_2021 - tcom.viv_2011 - tcom.term_W).sum())
    G_for = float((base.loc[[c for c in FOR if c in cods], "viv_2021"] - base.loc[[c for c in FOR if c in cods], "viv_2011"]
                   - base.loc[[c for c in FOR if c in cods], "term_W"]).sum())
    desc = pd.DataFrame([
        ["Δ parque Censo 2011 a Censo 2021 (viviendas familiares)", float(base.delta_censo.sum()), "INE 3457, 59525"],
        ["Terminadas MIVAU 1-nov-2011 a 31-dic-2020 (libres + protegidas, nov-dic 2011 y protegida 2011 a prorrata 2/12)",
         float(base.term_W.sum()), "MIVAU 3.2 y 1.6"],
        ["Diferencia = altas netas no explicadas por terminadas (= -bajas de la identidad)", G, "cálculo"],
        ["  de ellas, territorio común", G_com, "cálculo"],
        ["  de ellas, 4 provincias forales", G_for, "cálculo"],
        ["  territorio común: Δ unidades urbanas residenciales Catastro 1-ene-2012 a 1-ene-2021 menos terminadas 2012-2020", cat_extra,
         "Catastro, MIVAU"],
        ["  territorio común: residuo no explicado por el Catastro (cobertura censal 2011/2021, vivienda aflorada, otras)",
         G_com - cat_extra, "cálculo"],
        ["Sensibilidad ventana: sumar terminadas 2021 completo y quitar nov-dic 2011 (lectura B1: 2012-2021)",
         float(base.term_2021.sum() - base.nov_dic_2011_libres.sum() - base.prot_2011_prorrata.sum()), "cálculo"],
    ], columns=["concepto", "viviendas", "fuente"])
    desc.to_csv(OUT / "tablas" / "identidad_descomposicion.csv", index=False)
    pnp = pd.DataFrame({
        "concepto": ["viviendas principales", "no principales (secundarias + vacías + otras)", "total"],
        "censo_2011": [n11["principal"], n11["total"] - n11["principal"], n11["total"]],
        "censo_2021": [float(base.princ_2021.sum()), float(base.viv_2021.sum() - base.princ_2021.sum()), float(base.viv_2021.sum())]})
    pnp["variacion"] = pnp.censo_2021 - pnp.censo_2011
    pnp.to_csv(OUT / "tablas" / "censos_principal_no_principal.csv", index=False)
    # ratio UU Catastro / viviendas censo 2021 (territorio común)
    ratio_uu = float(catp.loc[comun, 2021].sum() / tcom.viv_2021.sum())
    # -------------------------------------------------- comparación y capas
    tasa_B_nac = float(nacB.loc[2012:2020, "bajas"].sum() / nacB.loc[2012:2020, "UU"].sum())
    tasa_A_com = float(tcom.bajas_A.sum() / (VENT * tcom.viv_2011.sum()))
    tC = nacC[nacC.anio.between(2012, 2020)].groupby("def").apply(lambda g: g.bajas.sum() / g.parque.sum(), include_groups=False)
    bC = nacC[nacC.anio.between(2012, 2020)].groupby("def").bajas.sum() / 9.0
    comp = pd.DataFrame([
        ["a) identidad Censo, nacional 2011-2020", 100 * tasaA_nac, sA / VENT, "negativa"],
        ["a) identidad Censo, territorio común", 100 * tasa_A_com, float(tcom.bajas_A.sum() / VENT), "negativa"],
        ["b) Catastro, territorio común 2012-2020", 100 * tasa_B_nac, sB / 9, "negativa"],
        ["c) licencias, demolición estrecha (tabla 10) 2012-2020", 100 * float(tC["estrecha"]), float(bC["estrecha"]), "positiva"],
        ["c) licencias, demolición amplia (tabla 6) 2012-2020", 100 * float(tC["amplia"]), float(bC["amplia"]), "positiva"],
    ], columns=["metodo", "tasa_anual_pct", "viviendas_anio", "signo"])
    b1924 = nacB.loc[2019:2024]
    c1924 = nacC[nacC.anio.between(2019, 2024)].groupby("def").apply(lambda g: g.bajas.sum() / g.parque.sum(), include_groups=False)
    tB1924 = float(b1924.bajas.sum() / b1924.UU.sum())
    comp.loc[len(comp)] = ["b) Catastro, territorio común 2019-2024 (núcleo C1 de terminadas, M0)", 100 * tB1924,
                           float(b1924.bajas.sum() / 6), "≈0 (neta)"]
    comp.loc[len(comp)] = ["c) licencias demolición estrecha 2019-2024", 100 * float(c1924["estrecha"]),
                           float(nacC[(nacC.anio.between(2019, 2024)) & (nacC["def"] == "estrecha")].bajas.sum() / 6), "positiva"]
    comp.loc[len(comp)] = ["c) licencias demolición amplia 2019-2024", 100 * float(c1924["amplia"]),
                           float(nacC[(nacC.anio.between(2019, 2024)) & (nacC["def"] == "amplia")].bajas.sum() / 6), "positiva"]
    dif_bc1924 = [abs(comp.tasa_anual_pct[5] - comp.tasa_anual_pct[6]), abs(comp.tasa_anual_pct[5] - comp.tasa_anual_pct[7])]
    dif_ab = abs(comp.tasa_anual_pct[1] - comp.tasa_anual_pct[2])
    dif_ac = abs(comp.tasa_anual_pct[1] - comp.tasa_anual_pct[3])
    dif_bc = abs(comp.tasa_anual_pct[2] - comp.tasa_anual_pct[3])
    comp["margen_declarado_pp"] = MARGEN_PP
    comp.to_csv(OUT / "tablas" / "comparacion_metodos.csv", index=False)
    # tests y FDR (H0: tasa media provincial = 0)
    from scipy import stats
    pvals = {}
    for nm, ser in (("A", base.tasa_A.dropna()), ("B", base.tasa_B.dropna()),
                    ("C_estrecha", C[(C["def"] == "estrecha") & C.anio.between(2012, 2020)].groupby("cod_prov").tasa_C.mean()),
                    ("C_amplia", C[(C["def"] == "amplia") & C.anio.between(2012, 2020)].groupby("cod_prov").tasa_C.mean())):
        if len(ser) > 2:
            ser = ser.dropna()
            tt = stats.ttest_1samp(ser, 0.0)
            pvals[nm] = float(tt.pvalue)
            reg.log("T1", f"test_{nm}", f"media provincial tasa {nm} = 0", 2011, 2020, len(ser), np.nan, np.nan, np.nan,
                    coef_interes=float(ser.mean()), p_interes=float(tt.pvalue), notas="t de una muestra entre provincias")
    padj = econ_utils.holm(pvals)
    # registro de especificaciones
    for nm, v in (("A_total_ventana_nov11_ene21", tasaA_nac), ("A_comun", tasa_A_com), ("B_catastro_1220", tasa_B_nac),
                  ("C_estrecha", float(tC["estrecha"])), ("C_amplia", float(tC["amplia"]))):
        reg.log("T1", f"tasa_{nm}", "tasa anual de bajas / parque", 2011, 2020, int(len(cods)), np.nan, np.nan, np.nan, coef_interes=v,
                notas="tasa nacional")
    reg.log("T1", "A_variante_b1_ventana", "Censo11 + term(2012-2021) - Censo21", 2012, 2021, len(cods), np.nan, np.nan, np.nan,
            coef_interes=float(base.bajas_A_b1.sum() / (10 * base.viv_2011.sum())), notas="lectura B1 (2021 como fecha 1-nov-2021)")
    reg.log("T1", "A_solo_libres", "Censo11 + libres - Censo21", 2011, 2020, len(cods), np.nan, np.nan, np.nan,
            coef_interes=float(base.bajas_A_libres.sum() / (VENT * base.viv_2011.sum())), notas="sin protegida")
    # -------------------------------------------------- tasas provinciales para T3/T4 y déficit
    # central: media de las dos definiciones de licencia (2015-2024); max: máximo anual 2011-2024 de la def. amplia
    Cr = C[C.anio.between(2015, 2024)]
    pm = Cr.pivot_table(index="cod_prov", columns="def", values="tasa_C", aggfunc="mean")
    mx = C[(C["def"] == "amplia") & C.anio.between(2011, 2024)].groupby("cod_prov").tasa_C.max()
    bj = pd.DataFrame({"cod_prov": cods, "provincia": [nombres[c] for c in cods]}).set_index("cod_prov")
    bj["tasa_min"] = 0.0
    bj["tasa_central"] = (pm["estrecha"] + pm["amplia"]) / 2
    bj["tasa_max"] = mx
    bj["tasa_licencia_estrecha"] = pm["estrecha"]
    bj["tasa_licencia_amplia"] = pm["amplia"]
    bj["metodo"] = "min=0 (identidades a y b negativas; bajas>=0); central y max: licencias de demolición MIVAU repartidas por parque (c)"
    bj["capa"] = "C4"
    bj = bj.reset_index()
    for c in ("tasa_min", "tasa_central", "tasa_max", "tasa_licencia_estrecha", "tasa_licencia_amplia"):
        bj[c] = bj[c].round(7)
    bj[["cod_prov", "provincia", "tasa_min", "tasa_central", "tasa_max", "metodo", "capa", "tasa_licencia_estrecha",
        "tasa_licencia_amplia"]].to_csv(OUT / "tablas" / "bajas_provincia.csv", index=False)
    # -------------------------------------------------- déficit con bajas estimadas
    a4 = pd.read_csv(RAIZ / "output" / "v5" / "A4" / "tablas" / "A4_deficit_provincial_ECP_MIVAU.csv", dtype={"cod_prov": str})
    pk = park.copy()
    filasD = []
    for per, yrs in (("2021-2024", range(2021, 2025)), ("2021-2025", range(2021, 2026))):
        a = a4[a4.periodo == per].set_index("cod_prov").reindex(cods)
        for esc in ("tasa_min", "tasa_central", "tasa_max"):
            baj = pd.Series(0.0, index=cods)
            for y in yrs:
                col = y - 1 if (y - 1) in pk.columns else pk.columns.max()
                baj = baj + bj.set_index("cod_prov")[esc] * pk[col]
            for sup, r in (("estimada_" + esc, None), ("supuesto_0,1%", 0.001), ("supuesto_0,2%", 0.002)):
                if r is not None and esc != "tasa_central":
                    continue
                if r is not None:
                    baj2 = pd.Series(0.0, index=cods)
                    for y in yrs:
                        col = y - 1 if (y - 1) in pk.columns else pk.columns.max()
                        baj2 = baj2 + r * pk[col]
                else:
                    baj2 = baj
                filasD.append({"periodo": per, "escenario": sup, "deficit_sin_bajas": float(a.deficit_bajas0.sum()),
                               "bajas": float(baj2.sum()), "deficit": float(a.deficit_bajas0.sum() + baj2.sum()),
                               "n_prov": int(a.deficit_bajas0.notna().sum())})
    D = pd.DataFrame(filasD)
    D.to_csv(OUT / "tablas" / "deficit_con_bajas_estimadas.csv", index=False)
    base_out = base.reset_index()
    base_out.to_csv(OUT / "tablas" / "identidad_censos_provincia.csv", index=False)
    B.to_csv(OUT / "tablas" / "catastro_bajas_provincia_anio.csv", index=False)
    # -------------------------------------------------- control de sumas
    cs = []

    def chk(nm, parts, tot, tol=1e-6):
        cs.append({"tabla": nm, "suma_provincial": float(parts), "nacional": float(tot), "tolerancia_rel": tol,
                   "ok": bool(abs(parts - tot) <= tol * max(1.0, abs(tot)))})
    chk("viv_2011_censo", base.viv_2011.sum(), n11["total"], 5e-3)
    chk("viv_2021_censo", base.viv_2021.sum(), c21.V_TOTAL.sum())
    if not SMOKE:
        chk("terminadas_W_libres_2012_2020", lib[ys].sum().sum(),
            mi[(mi.nivel == "nacional") & mi.serie.str.contains("viv_libres_terminadas_anual")
               & pd.to_numeric(mi.periodo, errors="coerce").between(2012, 2020)].valor.sum(), 1e-3)
        for y in (2014, 2020, 2024):
            chk(f"licencias_demolicion_{y}_amplia", C[(C.anio == y) & (C["def"] == "amplia")].bajas_C.sum(), L.loc[y, "D_amplia"])
            chk(f"licencias_demolicion_{y}_estrecha", C[(C.anio == y) & (C["def"] == "estrecha")].bajas_C.sum(), L.loc[y, "D_estrecha"])
        chk("bajas_A_suma_provincial", base.bajas_A.sum(), sA)
        chk("bajas_B_1220_suma_provincial", base.bajas_B_1220.sum(), sB)
        chk("deficit_2021_2024_sin_bajas", D[D.periodo == "2021-2024"].deficit_sin_bajas.iloc[0], 562692.0, 1e-3)
    (OUT / "control_sumas.json").write_text(json.dumps(cs, ensure_ascii=False, indent=1), encoding="utf-8")
    # -------------------------------------------------- figura determinista
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(nacB.index, 100 * nacB.tasa, marker="o", label="b) Catastro (territorio común)")
    for lab, st in (("estrecha", "--"), ("amplia", "-")):
        s = nacC[nacC["def"] == lab]
        s = s[s.anio <= 2024]
        ax.plot(s.anio, 100 * s.tasa, st, marker="s", label=f"c) licencias de demolición ({lab})")
    ax.hlines(100 * tasaA_nac, 2012, 2020, color="k", linestyles=":", label="a) identidad Censos (media 2011-2020)")
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_ylabel("% del parque al año")
    ax.set_title("Tasa anual de bajas del parque residencial por método")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "T1_tasas_por_metodo.png", dpi=120, metadata={"Software": None})
    plt.close(fig)
    # -------------------------------------------------- salida resumen para hechos/resultado
    npos = {m: int((base[c].dropna() > 0).sum()) for m, c in (("A", "bajas_A"), ("B", "bajas_B_1220"))}
    resumen = {
        "tasaA_nac": tasaA_nac, "sA": sA, "tasa_A_com": tasa_A_com, "tasa_B_nac": tasa_B_nac, "sB": sB,
        "tC": tC.to_dict(), "bC": bC.to_dict(), "dif_bc1924": dif_bc1924, "tB1924": tB1924, "c1924": c1924.to_dict(), "dif_ab": dif_ab, "dif_ac": dif_ac, "dif_bc": dif_bc, "ratio_uu": ratio_uu,
        "npos": npos, "n_neg_A": int((base.bajas_A < 0).sum()), "n_neg_B": int((base.bajas_B_1220.dropna() < 0).sum()),
        "n_B": int(base.bajas_B_1220.notna().sum()), "pvals": pvals, "padj": padj, "G_com": G_com, "G_for": G_for,
        "cat_extra": cat_extra, "G": G, "term_W": float(base.term_W.sum()), "delta_censo": float(base.delta_censo.sum()),
        "A_b1": float(base.bajas_A_b1.sum()), "A_libres": float(base.bajas_A_libres.sum()),
        "L2024": L.loc[2024, ["D_estrecha", "D_amplia"]].to_dict(), "L_media_1224": L.loc[2012:2024, ["D_estrecha", "D_amplia"]].mean().to_dict(),
        "tasa_L2024": [float(L.loc[2024, "tasa_D_estrecha"]), float(L.loc[2024, "tasa_D_amplia"])],
        "tasa_L_max_0024": float(L.tasa_D_amplia.max()), "central_nac": float((bj.tasa_central * park[2020].reindex(bj.cod_prov).values).sum() / park[2020].sum()),
        "max_nac": float((bj.tasa_max * park[2020].reindex(bj.cod_prov).values).sum() / park[2020].sum()),
        "deficit": D.to_dict("records"), "nprov": len(cods), "smoke": SMOKE,
        "ccaa_vs_nac": {int(y): float(CC.loc[y].sum() / L.loc[y, "D_amplia"]) for y in (2012, 2016, 2020, 2022) if y in CC.index},
    }
    (OUT / ("resumen_smoke.json" if SMOKE else "resumen_interno.json")).write_text(json.dumps(resumen, ensure_ascii=False, indent=1, default=float))

    if not SMOKE:
        escribir_entregables(resumen, comp, desc, pnp, bj, D, base, nacB, nacC, L)
    reg.flush()
    print(json.dumps(resumen, ensure_ascii=False, indent=1, default=float)[:6000])
    print(comp.to_string())
    print(desc.to_string())
    print(pnp.to_string())


if __name__ == "__main__":
    main()
