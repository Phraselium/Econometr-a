"""V10-B2 · `make atlas`: atlas descriptivo (b-e) desde la base única (data/base/publica) y tablas oficiales del proyecto.

Solo descriptivo: ninguna tabla interpreta causas. Cada fila lleva capa, fuente y fecha del dato. Las filas con
`posterior_prereg` no entran en ningún cálculo (se excluyen al leer la base).

b) entrar frente a quedarse: IPVA de contratos nuevos frente a existentes (CCAA y provincia, 2015-2024) y dispersión
   entre distritos de las capitales; fianzas de la GVA por código postal (2020-2025).
c) València por sección y barrio: población y extranjeros (censo anual 2021-2025), renta (ADRH 2020-2023), viviendas
   turísticas (INE, 2021-2026M05), alquiler (SERPAVI 2019-2024), hogares y viviendas (Censo 2021); agregación a barrio
   con la correspondencia por área; índice sintético descriptivo de presión residencial.
d) Comunitat Valenciana por municipio y España por provincia.
e) València frente a ciudades comparables (Málaga, Sevilla, Bilbao, Zaragoza, Palma y Alicante).
Salidas: output/v10/atlas/*.csv y output/v10/atlas/resumen.json (lo lee publicacion/atlas_descriptivo.md).
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PUB = RAIZ / "data" / "base" / "publica"
OUT = RAIZ / "output" / "v10" / "atlas"
VLC = "46250"
CIUDADES = {"46250": "València", "29067": "Málaga", "41091": "Sevilla", "48020": "Bilbao", "50297": "Zaragoza",
            "07040": "Palma", "03014": "Alicante/Alacant"}


def q(sql: str) -> pd.DataFrame:
    con = duckdb.connect()
    con.execute(f"CREATE VIEW h AS SELECT * FROM read_parquet('{PUB / 'hechos.parquet'}') WHERE NOT posterior_prereg")
    con.execute(f"CREATE VIEW t AS SELECT * FROM read_parquet('{PUB / 'territorios.parquet'}')")
    d = con.execute(sql).df()
    con.close()
    return d


def serie(variable: str, nivel: str, desag: str = "", filtro: str = "") -> pd.DataFrame:
    return q(f"""SELECT territorio_codigo, periodo, valor, fecha_dato, capa, fuente FROM h
                 WHERE variable = '{variable}' AND nivel = '{nivel}' AND desagregacion = '{desag}' {filtro}""")


def ancho(variable: str, nivel: str, desag: str = "", filtro: str = "") -> pd.DataFrame:
    d = serie(variable, nivel, desag, filtro)
    return d.pivot_table(index="territorio_codigo", columns="periodo", values="valor")


def nombres() -> pd.Series:
    t = q("SELECT territorio_codigo, nivel, nombre FROM t")
    return t.set_index(["nivel", "territorio_codigo"]).nombre


# ------------------------------------------------------------------------------------------------ b) entrar frente a quedarse
def b_ipva() -> pd.DataFrame:
    filas = []
    nom = nombres()
    for nivel in ("nacional", "ccaa", "provincia"):
        d = q(f"""SELECT territorio_codigo, periodo, desagregacion, valor FROM h WHERE variable = 'ipva_indice'
                  AND nivel = '{nivel}' AND desagregacion IN ('contrato=Nuevo contrato', 'contrato=Contrato existente', 'contrato=Total')""")
        w = d.pivot_table(index=["territorio_codigo", "periodo"], columns="desagregacion", values="valor").reset_index()
        w.columns = ["territorio_codigo", "periodo", "existente", "nuevo", "total"]
        w["brecha_nuevo_menos_existente"] = w.nuevo - w.existente
        w["nivel"] = nivel
        w["nombre"] = [nom.get((nivel, c), c) for c in w.territorio_codigo]
        filas.append(w)
    t = pd.concat(filas, ignore_index=True)
    t["unidad"] = "índice 2015=100 (la brecha, en puntos de índice)"
    t["fuente"] = "INE, Índice de Precios de Vivienda en Alquiler (tablas 59004 y 59005)"
    t["capa"] = "C4"
    t["fecha_dato"] = t.periodo + "-12-31"
    t["nota"] = ("Índices encadenados de renta por contrato: miden la evolución desde 2015, no el nivel. Brecha > 0: la renta "
                 "de los contratos nuevos ha crecido más que la de los existentes desde 2015")
    return t


def b_distritos_capitales() -> pd.DataFrame:
    d = serie("ipva_indice", "distrito", "contrato=Total")
    d["municipio"] = d.territorio_codigo.str[:5]
    g = d.groupby(["municipio", "periodo"]).valor.agg(["min", "max", "median", "count"]).reset_index()
    g["rango_entre_distritos"] = g["max"] - g["min"]
    nom = nombres()
    g["nombre"] = [nom.get(("municipio", c), c) for c in g.municipio]
    g["unidad"] = "índice 2015=100"
    g["fuente"] = "INE, IPVA por distritos de las capitales (tabla 59061)"
    g["capa"] = "C4"
    g["fecha_dato"] = g.periodo + "-12-31"
    return g.rename(columns={"min": "indice_min", "max": "indice_max", "median": "indice_mediana", "count": "n_distritos"})


def b_fianzas_cp() -> pd.DataFrame:
    """Fianzas depositadas en la GVA por código postal: número y fianza mediana (≈ una mensualidad en vivienda)."""
    partes = []
    for f in sorted((RAIZ / "data/raw/v5").glob("gva_fianzas_20*.csv")):
        d = pd.read_csv(f, sep=";", dtype=str)
        d["importe"] = pd.to_numeric(d.importe_fianza.str.replace(",", "."), errors="coerce")
        partes.append(d[["anyo_datos", "cod_provincia", "cod_municipio", "cp", "importe"]])
    d = pd.concat(partes, ignore_index=True)
    d = d[d.anyo_datos.astype(int) <= 2025]   # 2026 incompleto y posterior al pre-registro en su segundo semestre
    d["ine5"] = d.cod_provincia.str.zfill(2) + d.cod_municipio.str.zfill(3)
    g = d.groupby(["anyo_datos", "ine5", "cp"]).importe.agg(n_fianzas="size", fianza_mediana="median").reset_index()
    g = g[g.n_fianzas >= 20]   # celdas con menos de 20 fianzas se suprimen
    g["unidad"] = "fianzas; € (mediana)"
    g["fuente"] = "Generalitat Valenciana, fianzas de arrendamiento (datos abiertos, CC BY 4.0)"
    g["capa"] = "C4"
    g["fecha_dato"] = g.anyo_datos + "-12-31"
    g["nota"] = "Código postal (no es código INE; no se cruza con otras fuentes). Celdas con menos de 20 fianzas suprimidas"
    return g


# ------------------------------------------------------------------------------------------------ c) València por sección y barrio
def c_valencia() -> tuple[pd.DataFrame, pd.DataFrame]:
    fil = f"AND territorio_codigo LIKE '{VLC}%'"
    pob = ancho("pob_censo_anual", "seccion", "nacionalidad=Total", fil)
    esp = ancho("pob_censo_anual", "seccion", "nacionalidad=España", fil)
    s = pd.DataFrame(index=pob.index)
    s["pob_2021"], s["pob_2025"] = pob.get("2021"), pob.get("2025")
    s["extranj_2021"] = pob.get("2021") - esp.get("2021")
    s["extranj_2025"] = pob.get("2025") - esp.get("2025")
    s["pct_extranj_2021"] = 100 * s.extranj_2021 / s.pob_2021
    s["pct_extranj_2025"] = 100 * s.extranj_2025 / s.pob_2025
    renta = ancho("adrh_renta_neta_persona", "seccion", "", fil)
    s["renta_persona_2020"], s["renta_persona_2023"] = renta.get("2020"), renta.get("2023")
    vut = ancho("ine_vut_vivienda_turistica", "seccion", "", fil)
    pct = ancho("ine_vut_porcentaje_vivienda_turistica", "seccion", "", fil)
    s["vut_2021_08"], s["vut_2026_05"] = vut.get("2021-08"), vut.get("2026-05")
    s["pct_vut_2026_05"] = pct.get("2026-05")
    alq = ancho("serpavi_alquiler_m2_mediana", "seccion", "tipologia=VC", fil)
    s["alquiler_m2_2019"], s["alquiler_m2_2024"] = alq.get("2019"), alq.get("2024")
    c21 = q(f"""SELECT territorio_codigo, variable, valor FROM h WHERE nivel = 'seccion' AND periodo = '2021'
                AND variable IN ('censo2021_t18_1', 'censo2021_t19_1', 'censo2021_t19_2', 'censo2021_t20_2', 'censo2021_t21_1',
                                 'censo2021_t22_1') {fil}""").pivot_table(index="territorio_codigo", columns="variable", values="valor")
    s["viviendas_2021"] = c21.get("censo2021_t18_1")
    s["viv_no_principales_2021"] = c21.get("censo2021_t19_2")
    s["viv_alquiler_2021"] = c21.get("censo2021_t20_2")
    s["viv_principales_2021"] = c21.get("censo2021_t19_1")
    s["hogares_2021"] = c21.get("censo2021_t21_1")
    s["hogares_1p_2021"] = c21.get("censo2021_t22_1")
    s = s.reset_index().rename(columns={"territorio_codigo": "cod_seccion"})
    # agregación a barrio por área (recuentos repartidos con el peso; tasas recalculadas; medianas: media ponderada)
    corr = pd.read_csv(RAIZ / "data/base/geo/correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str, "cod_barrio": str})
    m = s.merge(corr, on="cod_seccion")
    cuentas = ["pob_2021", "pob_2025", "extranj_2021", "extranj_2025", "vut_2021_08", "vut_2026_05", "viviendas_2021",
               "viv_no_principales_2021", "viv_alquiler_2021", "viv_principales_2021", "hogares_2021", "hogares_1p_2021"]
    for c in cuentas:
        m[c] = m[c] * m.peso_area
    b = m.groupby("cod_barrio")[cuentas].sum(min_count=1)
    for c, peso in (("renta_persona_2020", "pob_2021"), ("renta_persona_2023", "pob_2025"),
                    ("alquiler_m2_2019", "viv_alquiler_2021"), ("alquiler_m2_2024", "viv_alquiler_2021")):
        w = m[peso]
        ok = m[c].notna() & w.notna()
        b[c] = (m[c] * w).where(ok).groupby(m.cod_barrio).sum() / w.where(ok).groupby(m.cod_barrio).sum()
    b = b.reset_index()
    for d in (s, b):
        d["var_pob_2021_2025_pct"] = 100 * (d.pob_2025 / d.pob_2021 - 1)
        d["pct_extranj_2021"] = 100 * d.extranj_2021 / d.pob_2021
        d["pct_extranj_2025"] = 100 * d.extranj_2025 / d.pob_2025
        d["var_pct_extranj_pp"] = d.pct_extranj_2025 - d.pct_extranj_2021
        d["vut_por_100_viv"] = 100 * d.vut_2026_05 / d.viviendas_2021
        d["var_alquiler_2019_2024_pct"] = 100 * (d.alquiler_m2_2024 / d.alquiler_m2_2019 - 1)
        d["var_renta_2020_2023_pct"] = 100 * (d.renta_persona_2023 / d.renta_persona_2020 - 1)
        d["pct_viv_no_principales_2021"] = 100 * d.viv_no_principales_2021 / d.viviendas_2021
        d["pct_hogares_1p_2021"] = 100 * d.hogares_1p_2021 / d.hogares_2021
        # índice sintético descriptivo: media de puntuaciones z (sin pesos ni interpretación causal)
        comp = ["alquiler_m2_2024", "var_alquiler_2019_2024_pct", "vut_por_100_viv", "var_pct_extranj_pp"]
        z = (d[comp] - d[comp].mean()) / d[comp].std(ddof=0)
        d["indice_presion_descriptivo"] = z.mean(axis=1, skipna=False)
        d["n_componentes_indice"] = z.notna().sum(axis=1)
    nb = q("SELECT territorio_codigo cod_barrio, nombre FROM t WHERE nivel = 'barrio'")
    b = b.merge(nb, on="cod_barrio", how="left")
    for d, nivel in ((s, "seccion"), (b, "barrio")):
        d["nivel"] = nivel
        d["capa"] = "C4"
        d["fuente"] = ("INE (Censo anual 2021-2025; ADRH; viviendas turísticas, experimental; Censo 2021); MIVAU SERPAVI; "
                       "Ajuntament de València (barrios, CC BY 4.0)")
        d["fecha_dato"] = "2026-05-31 (VUT); 2025-01-01 (población); 2024 (alquiler); 2023 (renta); 2021-11-01 (censo)"
    return s, b


# ------------------------------------------------------------------------------------------------ d) CV por municipio y España por provincia
def d_cv_municipios() -> pd.DataFrame:
    fil = "AND substr(territorio_codigo, 1, 2) IN ('03', '12', '46')"
    pob = ancho("pob_censo_anual", "municipio", "nacionalidad=Total", fil)
    esp = ancho("pob_censo_anual", "municipio", "nacionalidad=España", fil)
    d = pd.DataFrame(index=pob.index)
    d["pob_2021"], d["pob_2025"] = pob.get("2021"), pob.get("2025")
    d["var_pob_2021_2025_pct"] = 100 * (d.pob_2025 / d.pob_2021 - 1)
    d["pct_extranj_2025"] = 100 * (1 - esp.get("2025") / pob.get("2025"))
    d["var_pct_extranj_pp"] = d.pct_extranj_2025 - 100 * (1 - esp.get("2021") / pob.get("2021"))
    alq = ancho("serpavi_alquiler_m2_mediana", "municipio", "tipologia=VC", fil)
    d["alquiler_m2_2019"], d["alquiler_m2_2024"] = alq.get("2019"), alq.get("2024")
    d["var_alquiler_2019_2024_pct"] = 100 * (d.alquiler_m2_2024 / d.alquiler_m2_2019 - 1)
    vut = ancho("vut_registro_gva", "municipio", "", fil)
    cortes = sorted(vut.columns)
    d["vut_registro_gva_ultimo_corte"] = vut[cortes[-1]] if cortes else np.nan
    d["corte_registro_gva"] = cortes[-1] if cortes else ""
    ine = ancho("ine_vut_vivienda_turistica", "municipio", "", fil)
    d["vut_ine_2026_05"] = ine.get("2026-05")
    viv = ancho("catastro_unidades_urbanas_residenciales", "municipio", "", fil)
    ult = max(viv.columns) if len(viv.columns) else None
    d["inmuebles_residenciales_catastro"] = viv[ult] if ult else np.nan
    d["vut_ine_por_100_inmuebles"] = 100 * d.vut_ine_2026_05 / d.inmuebles_residenciales_catastro
    a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_municipios.csv", dtype={"cod_mun": str})
    a4 = a4.set_index("cod_mun")[["precio_eur_m2", "precio_fuente", "deficit_2021_2025"]]
    d = d.join(a4, how="left").reset_index().rename(columns={"index": "cod_municipio", "territorio_codigo": "cod_municipio"})
    nom = nombres()
    d["nombre"] = [nom.get(("municipio", c), c) for c in d.cod_municipio]
    d["capa"] = "C4"
    d["fuente"] = ("INE censo anual; MIVAU SERPAVI; GVA registro de turismo (CC BY 4.0); INE viviendas turísticas; Catastro; "
                   "output/v5/A4 (precio y déficit publicados, C4)")
    d["fecha_dato"] = "2025-01-01 (población); 2024 (alquiler); corte del registro GVA; 2026-05 (INE VUT)"
    d["nota"] = ("Compraventas municipales: el MIVAU las publica solo con el nombre del municipio, sin código INE (no se "
                 "cruzan por nombre). Precio y déficit: los publicados en V5 (A4)")
    return d


def d_provincias() -> pd.DataFrame:
    def ult(var, nivel="provincia", desag=""):
        w = ancho(var, nivel, desag)
        return w
    p = pd.DataFrame(index=[f"{i:02d}" for i in range(1, 53)])
    vt = ult("valor_tasado")
    p["valor_tasado_2024"] = vt.get("2024") if "2024" in vt else np.nan
    p["valor_tasado_2015"] = vt.get("2015") if "2015" in vt else np.nan
    # CCAA uniprovinciales: el panel provincial no trae su valor tasado; se usa el de la CCAA (mismo territorio),
    # media de los cuatro trimestres (como el dato anual provincial del panel)
    uni = {"33": "03", "07": "04", "26": "17", "28": "13", "30": "14", "31": "15", "39": "06", "51": "18", "52": "19"}
    vq = q("""SELECT territorio_codigo, substr(periodo, 1, 4) anio, avg(valor) v, count(*) n FROM h
              WHERE variable = 'p_tasado' AND nivel = 'ccaa' AND frecuencia = 'T' GROUP BY 1, 2 HAVING count(*) = 4""")
    vq = vq.set_index(["territorio_codigo", "anio"]).v
    p["valor_tasado_origen"] = np.where(p.valor_tasado_2024.notna(), "provincia (panel v7)", "")
    for prov, cc in uni.items():
        if pd.isna(p.at[prov, "valor_tasado_2024"]):
            p.at[prov, "valor_tasado_2024"] = vq.get((cc, "2024"), np.nan)
            p.at[prov, "valor_tasado_2015"] = vq.get((cc, "2015"), np.nan)
            p.at[prov, "valor_tasado_origen"] = "CCAA uniprovincial (p_tasado trimestral, media anual)"
    p["var_valor_tasado_2015_2024_pct"] = 100 * (p.valor_tasado_2024 / p.valor_tasado_2015 - 1)
    alq = ult("serpavi_alquiler_m2_mediana", desag="tipologia=VC")
    p["alquiler_m2_2024"], p["alquiler_m2_2015"] = alq.get("2024"), alq.get("2015")
    p["var_alquiler_2015_2024_pct"] = 100 * (p.alquiler_m2_2024 / p.alquiler_m2_2015 - 1)
    pob = ult("pob_censo_anual", desag="nacionalidad=Total")
    esp = ult("pob_censo_anual", desag="nacionalidad=España")
    p["pob_2025"] = pob.get("2025")
    p["var_pob_2021_2025_pct"] = 100 * (pob.get("2025") / pob.get("2021") - 1)
    p["pct_extranj_2025"] = 100 * (1 - esp.get("2025") / pob.get("2025"))
    cv = ult("compraventas")
    p["compraventas_2024"] = cv.get("2024")
    it = ult("iniciadas")
    p["iniciadas_2024"] = it.get("2024")
    vut = ult("vut_viviendas")
    p["vut_2024"] = vut.get("2024")
    # renta: media de la renta por persona de las secciones ponderada por población (ADRH 2023, censo 2023)
    r = q("""SELECT substr(a.territorio_codigo, 1, 2) prov, sum(a.valor * b.valor) / sum(b.valor) renta
             FROM h a JOIN h b ON a.territorio_codigo = b.territorio_codigo AND b.variable = 'pob_censo_anual'
             AND b.desagregacion = 'nacionalidad=Total' AND b.periodo = '2023' AND b.nivel = 'seccion'
             WHERE a.variable = 'adrh_renta_neta_persona' AND a.nivel = 'seccion' AND a.periodo = '2023' GROUP BY 1""")
    p["renta_neta_persona_2023"] = r.set_index("prov").renta
    p["precio_80m2_en_anios_renta_persona"] = p.valor_tasado_2024 * 80 / p.renta_neta_persona_2023
    p["alquiler_anual_80m2_pct_renta_persona"] = 100 * p.alquiler_m2_2024 * 80 * 12 / p.renta_neta_persona_2023
    a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    p["deficit_2021_2025_mediana"] = a4.deficit_2021_2025_mediana
    p["deficit_2021_2025_min"] = a4.deficit_2021_2025_min
    p["deficit_2021_2025_max"] = a4.deficit_2021_2025_max
    nom = nombres()
    p = p.rename_axis("cod_provincia").reset_index()
    p["nombre"] = [nom.get(("provincia", c), c) for c in p.cod_provincia]
    p["capa"] = "C4"
    p["fuente"] = ("MIVAU (valor tasado, SERPAVI); INE (censo anual, ETDP, ADRH, viviendas turísticas); MIVAU iniciadas; "
                   "output/v5/A4 (déficit publicado, C4)")
    p["fecha_dato"] = "2024 (precio, alquiler, compraventas); 2025-01-01 (población); 2023 (renta)"
    p["nota"] = ("Esfuerzo aproximado con una vivienda tipo de 80 m² y la renta neta media por persona (no por hogar): "
                 "indicador comparativo entre provincias, no carga de un hogar concreto")
    return p


# ------------------------------------------------------------------------------------------------ e) ciudades comparables
def e_ciudades() -> pd.DataFrame:
    filas = []
    cods = "', '".join(CIUDADES)
    defs = [("serpavi_alquiler_m2_mediana", "tipologia=VC", "alquiler_m2_mediana", "€/m²/mes", "MIVAU SERPAVI"),
            ("pob_censo_anual", "nacionalidad=Total", "poblacion", "personas", "INE censo anual"),
            ("ine_vut_vivienda_turistica", "", "viviendas_turisticas", "viviendas", "INE viviendas turísticas (experimental)"),
            ("ine_vut_porcentaje_vivienda_turistica", "", "pct_viviendas_turisticas", "% de viviendas", "INE viviendas turísticas")]
    for var, des, nombre, unidad, fuente in defs:
        d = q(f"""SELECT territorio_codigo, periodo, valor FROM h WHERE variable = '{var}' AND nivel = 'municipio'
                  AND desagregacion = '{des}' AND territorio_codigo IN ('{cods}')""")
        d["indicador"], d["unidad"], d["fuente"] = nombre, unidad, fuente
        filas.append(d)
    pob = q(f"""SELECT territorio_codigo, periodo, desagregacion, valor FROM h WHERE variable = 'pob_censo_anual'
               AND nivel = 'municipio' AND territorio_codigo IN ('{cods}') AND desagregacion IN ('nacionalidad=Total', 'nacionalidad=España')""")
    w = pob.pivot_table(index=["territorio_codigo", "periodo"], columns="desagregacion", values="valor").reset_index()
    w["valor"] = 100 * (1 - w["nacionalidad=España"] / w["nacionalidad=Total"])
    w["indicador"], w["unidad"], w["fuente"] = "pct_extranjeros", "%", "INE censo anual"
    filas.append(w[["territorio_codigo", "periodo", "valor", "indicador", "unidad", "fuente"]])
    r = q(f"""SELECT substr(a.territorio_codigo, 1, 5) territorio_codigo, a.periodo, sum(a.valor * b.valor) / sum(b.valor) valor
             FROM h a JOIN h b ON a.territorio_codigo = b.territorio_codigo AND b.variable = 'pob_censo_anual'
             AND b.desagregacion = 'nacionalidad=Total' AND b.periodo = '2023' AND b.nivel = 'seccion'
             WHERE a.variable = 'adrh_renta_neta_persona' AND a.nivel = 'seccion' AND substr(a.territorio_codigo, 1, 5) IN ('{cods}')
             GROUP BY 1, 2""")
    r["indicador"], r["unidad"], r["fuente"] = "renta_neta_persona", "€/año", "INE ADRH (media de secciones ponderada por población 2023)"
    filas.append(r)
    e = pd.concat(filas, ignore_index=True)
    e["ciudad"] = e.territorio_codigo.map(CIUDADES)
    e["periodo"] = e.periodo.astype(str)
    e["fecha_dato"] = [f"{x}-12-31" if len(x) == 4 else x for x in e.periodo]
    e["capa"] = "C4"
    e["nota"] = np.where((e.ciudad == "Bilbao") & (e.indicador == "alquiler_m2_mediana"),
                         "SERPAVI cubre los territorios forales solo desde 2024", "Comparación descriptiva; sin inferencia causal")
    return e.sort_values(["indicador", "ciudad", "periodo"])


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    tablas = {"b_ipva_nuevo_existente.csv": b_ipva(), "b_ipva_distritos_capitales.csv": b_distritos_capitales(),
              "b_fianzas_gva_cp.csv": b_fianzas_cp()}
    s, b = c_valencia()
    tablas["c_valencia_seccion.csv"], tablas["c_valencia_barrio.csv"] = s, b
    tablas["d_cv_municipios.csv"], tablas["d_espana_provincias.csv"] = d_cv_municipios(), d_provincias()
    tablas["e_ciudades_comparables.csv"] = e_ciudades()
    for nombre, t in tablas.items():
        t.to_csv(OUT / nombre, index=False, float_format="%.4f")
        res[nombre] = len(t)
    (OUT / "resumen.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    print(main())
