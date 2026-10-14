"""V10-B4 · `make web`: sitio estático (GitHub Pages, sin servidor) en web/_site desde la base, el atlas y las figuras.

- Plantillas Jinja2 en web/plantillas; CSS y JS en web/src; Observable Plot, D3 y Leaflet vendorizados en web/vendor
  (sin red al construir ni peticiones a terceros al navegar; los mapas no usan teselas externas).
- Solo datos redistribuibles: todo sale de data/base/publica y de output/v10 (agregados propios).
- Las filas `posterior_prereg` no se muestran en el panel de indicadores ni en los mapas; el monitor las enseña como
  dato nuevo, marcado, sin interpretación ni comparación con predicciones.
- Español y valenciano en la navegación y en los textos clave; inglés en metodología y resumen.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path

import duckdb
import geopandas as gpd
import markdown
import pandas as pd
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader, select_autoescape

RAIZ = Path(__file__).resolve().parents[2]
WEB = RAIZ / "web"
SITE = WEB / "_site"
PUB = RAIZ / "data" / "base" / "publica"
GEO = RAIZ / "data" / "base" / "geo"
ATLAS = RAIZ / "output" / "v10" / "atlas"
REPO = "https://github.com/Phraselium/vivienda-espana-evidencia"
URL_PREVISTA = "https://phraselium.github.io/vivienda-espana-evidencia/"

PAGINAS = [
    {"url": "index.html", "es": "Inicio", "va": "Inici"},
    {"url": "indicadores.html", "es": "Indicadores", "va": "Indicadors"},
    {"url": "mapas.html", "es": "Mapas", "va": "Mapes"},
    {"url": "fichas.html", "es": "Fichas territoriales", "va": "Fitxes territorials"},
    {"url": "quien.html", "es": "Quién lo sufre", "va": "Qui ho patix"},
    {"url": "verificador.html", "es": "Verificador", "va": "Verificador"},
    {"url": "monitor.html", "es": "Monitor", "va": "Monitor"},
    {"url": "metodologia.html", "es": "Metodología y datos", "va": "Metodologia i dades"},
    {"url": "historial.html", "es": "Historial", "va": "Historial"},
]

# Indicadores del panel (nivel, variable, desagregación, etiqueta)
INDICADORES = [
    ("nacional", "p_tasado", "", "Valor tasado de la vivienda libre"),
    ("nacional", "ipv", "", "Índice de precios de vivienda (INE)"),
    ("nacional", "ipc_alquiler", "", "IPC de alquiler de vivienda"),
    ("nacional", "tipo_hip_bde", "", "Tipo de interés de las hipotecas sobre vivienda"),
    ("nacional", "euribor_1y", "", "Euríbor a un año"),
    ("nacional", "compraventas_ine", "", "Compraventas de vivienda (INE)"),
    ("nacional", "terminadas", "", "Viviendas terminadas"),
    ("nacional", "hogares_epa", "", "Hogares (EPA)"),
    ("nacional", "pob_extranj_ine", "", "Población extranjera"),
    ("ccaa", "p_tasado", "", "Valor tasado de la vivienda libre"),
    ("ccaa", "ipv", "", "Índice de precios de vivienda (INE)"),
    ("ccaa", "ipc_alquiler", "", "IPC de alquiler de vivienda"),
    ("ccaa", "compraventas", "", "Compraventas de vivienda"),
    ("ccaa", "terminadas", "", "Viviendas terminadas"),
    ("ccaa", "tasa_paro_epa", "", "Tasa de paro (EPA)"),
    ("ccaa", "pob_extranj", "", "Población extranjera"),
    ("ccaa", "vut_viviendas", "", "Viviendas turísticas (INE)"),
    ("ccaa", "ipva_indice", "contrato=Nuevo contrato", "IPVA, contratos nuevos"),
    ("ccaa", "ipva_indice", "contrato=Contrato existente", "IPVA, contratos existentes"),
    ("provincia", "valor_tasado", "", "Valor tasado de la vivienda libre"),
    ("provincia", "compraventas", "", "Compraventas de vivienda"),
    ("provincia", "ipc_alquiler_indice", "", "IPC de alquiler"),
    ("provincia", "hip_n", "", "Hipotecas sobre vivienda (número)"),
    ("provincia", "iniciadas", "", "Viviendas iniciadas"),
    ("provincia", "serpavi_alquiler_m2_mediana", "tipologia=VC", "Alquiler mediano €/m² (SERPAVI, colectiva)"),
    ("provincia", "ipva_indice", "contrato=Nuevo contrato", "IPVA, contratos nuevos"),
    ("provincia", "pob_censo_anual", "nacionalidad=Total", "Población (censo anual)"),
]

# Capas de mapa: fichero de atlas, clave, geometría y columnas mostrables (columna, etiqueta, unidad, capa, divergente)
MAPAS = {
    "provincias": {
        "titulo": "España por provincia", "geo": "provincias.parquet", "clave_geo": "cod_provincia",
        "tabla": "d_espana_provincias.csv", "clave": "cod_provincia", "simplificar": 0.02,
        "fuente": "MIVAU (valor tasado, SERPAVI); INE (censo anual, ADRH, ETDP, viviendas turísticas); V5-A4 (déficit)",
        "fecha": "2023-2025 según indicador",
        "cols": [("alquiler_anual_80m2_pct_renta_persona", "Alquiler 80 m² / renta por persona", "%", "C4", False),
                 ("precio_80m2_en_anios_renta_persona", "Precio 80 m² en años de renta por persona", "años", "C4", False),
                 ("var_alquiler_2015_2024_pct", "Variación del alquiler 2015-2024", "%", "C4", False),
                 ("var_valor_tasado_2015_2024_pct", "Variación del valor tasado 2015-2024", "%", "C4", False),
                 ("pct_extranj_2025", "Población extranjera 2025", "%", "C1", False),
                 ("var_pob_2021_2025_pct", "Variación de la población 2021-2025", "%", "C1", True),
                 ("deficit_2021_2025_mediana", "Déficit de vivienda 2021-2025 (mediana)", "viviendas", "C4", True)]},
    "cv_municipios": {
        "titulo": "Comunitat Valenciana por municipio", "geo": "municipios.parquet", "clave_geo": "cod_municipio",
        "filtro": ("cod_ccaa", "10"), "tabla": "d_cv_municipios.csv", "clave": "cod_municipio", "simplificar": 0.001,
        "fuente": "INE (censo anual, viviendas turísticas); MIVAU SERPAVI; GVA registro de turismo; Catastro",
        "fecha": "2019-2026 según indicador",
        "cols": [("var_alquiler_2019_2024_pct", "Variación del alquiler 2019-2024", "%", "C4", False),
                 ("alquiler_m2_2024", "Alquiler mediano 2024", "€/m²/mes", "C4", False),
                 ("vut_ine_por_100_inmuebles", "Viviendas turísticas (INE) por 100 inmuebles residenciales", "por 100", "C4", False),
                 ("pct_extranj_2025", "Población extranjera 2025", "%", "C1", False),
                 ("var_pob_2021_2025_pct", "Variación de la población 2021-2025", "%", "C1", True)]},
    "valencia_barrios": {
        "titulo": "València por barrio", "geo": "barrios_valencia.parquet", "clave_geo": "cod_barrio",
        "tabla": "c_valencia_barrio.csv", "clave": "cod_barrio", "simplificar": 0.0001,
        "fuente": "INE (censo anual, ADRH, viviendas turísticas, Censo 2021); MIVAU SERPAVI; Ajuntament de València (CC BY 4.0)",
        "fecha": "2019-2026 según indicador",
        "cols": [("indice_presion_descriptivo", "Índice descriptivo de presión residencial", "z medio", "C4", True),
                 ("alquiler_m2_2024", "Alquiler mediano 2024", "€/m²/mes", "C4", False),
                 ("var_alquiler_2019_2024_pct", "Variación del alquiler 2019-2024", "%", "C4", False),
                 ("vut_por_100_viv", "Viviendas turísticas por 100 viviendas (2026-05)", "por 100", "C4", False),
                 ("pct_extranj_2025", "Población extranjera 2025", "%", "C1", False),
                 ("var_pct_extranj_pp", "Cambio del % de extranjeros 2021-2025", "puntos", "C1", True),
                 ("renta_persona_2023", "Renta neta por persona 2023", "€", "C4", False)]},
    "valencia_secciones": {
        "titulo": "València por sección censal", "geo": "secciones.parquet", "clave_geo": "cod_seccion",
        "filtro": ("cod_municipio", "46250"), "tabla": "c_valencia_seccion.csv", "clave": "cod_seccion", "simplificar": 0.0001,
        "fuente": "INE (censo anual, ADRH, viviendas turísticas, Censo 2021); MIVAU SERPAVI", "fecha": "2019-2026 según indicador",
        "cols": [("vut_por_100_viv", "Viviendas turísticas por 100 viviendas (2026-05)", "por 100", "C4", False),
                 ("alquiler_m2_2024", "Alquiler mediano 2024", "€/m²/mes", "C4", False),
                 ("pct_extranj_2025", "Población extranjera 2025", "%", "C1", False),
                 ("renta_persona_2023", "Renta neta por persona 2023", "€", "C4", False),
                 ("pct_viv_no_principales_2021", "Viviendas no principales (Censo 2021)", "%", "C4", False)]},
}


def md(texto: str, base_pub: str = "publicacion/") -> str:
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)

    def enlace(m):
        dest = m.group(2)
        if re.match(r"^(https?:|#|mailto:)", dest):
            return m.group(0)
        return f"{m.group(1)}{REPO}/blob/main/{base_pub}{dest}{m.group(3)}"
    texto = re.sub(r"(\]\()([^)\s]+)(\))", enlace, texto)
    html = markdown.markdown(texto, extensions=["tables", "sane_lists"])
    return re.sub(r"\[(C1|C2|C3s|C3|C4)\]", r'<span class="capa \1">\1</span>', html)


def consulta(sql: str) -> pd.DataFrame:
    con = duckdb.connect()
    con.execute(f"CREATE VIEW h AS SELECT * FROM read_parquet('{PUB / 'hechos.parquet'}')")
    con.execute(f"CREATE VIEW t AS SELECT * FROM read_parquet('{PUB / 'territorios.parquet'}')")
    d = con.execute(sql).df()
    con.close()
    return d


def escribir_json(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False), encoding="utf-8")


def limpio(v):
    if v is None or (isinstance(v, float) and (pd.isna(v))):
        return None
    if isinstance(v, float):
        return round(v, 4)
    return v


# ------------------------------------------------------------------------------------------------ datos de la web
def datos_indicadores() -> list[dict]:
    nombres = consulta("SELECT territorio_codigo, nivel, nombre FROM t").set_index(["nivel", "territorio_codigo"]).nombre.to_dict()
    catalogo = []
    for nivel, var, des, etiqueta in INDICADORES:
        d = consulta(f"""SELECT territorio_codigo, periodo, frecuencia, valor, unidad, fuente, capa, fecha_dato FROM h
                         WHERE nivel = '{nivel}' AND variable = '{var}' AND desagregacion = '{des}' AND NOT posterior_prereg
                         ORDER BY territorio_codigo, periodo""")
        if d.empty:
            continue
        frec = "T" if (d.frecuencia == "T").any() else d.frecuencia.mode().iloc[0]
        d = d[d.frecuencia == frec]
        ident = f"{nivel}__{var}__{re.sub(r'[^a-z0-9]+', '_', des.lower()).strip('_')}".rstrip("_")
        meta = {"id": ident, "nivel": nivel, "variable": var, "desagregacion": des, "etiqueta": etiqueta,
                "unidad": d.unidad.iloc[0],
                "fuente": d.fuente.iloc[0] if nivel == "nacional" else re.sub(r"\s*\(serie [^)]*nacional[^)]*\)", "", d.fuente.iloc[0]), "capa": d.capa.iloc[0], "frecuencia": frec,
                "fecha_dato": d.fecha_dato.max()}
        filas = [[c, nombres.get((nivel, c), c), p, limpio(float(v))] for c, p, v in zip(d.territorio_codigo, d.periodo, d.valor)]
        escribir_json(SITE / "datos" / "indicadores" / f"{ident}.json", {"meta": meta, "filas": filas})
        catalogo.append(meta)
    escribir_json(SITE / "datos" / "indicadores" / "catalogo.json", catalogo)
    return catalogo


def datos_mapas() -> dict:
    meta = {}
    for clave, m in MAPAS.items():
        g = gpd.read_parquet(GEO / m["geo"])
        if "filtro" in m:
            g = g[g[m["filtro"][0]] == m["filtro"][1]]
        t = pd.read_csv(ATLAS / m["tabla"], dtype={m["clave"]: str})
        cols = [c[0] for c in m["cols"]]
        nombre = "nombre" if "nombre" in t else None
        sel = t[[m["clave"]] + cols + ([nombre] if nombre else [])]
        g = g[[m["clave_geo"], "geometry"]].merge(sel, left_on=m["clave_geo"], right_on=m["clave"], how="left")
        if "nombre" not in g or g["nombre"].isna().all():
            g["nombre"] = g[m["clave_geo"]]
        g["nombre"] = g["nombre"].fillna(g[m["clave_geo"]]).astype(str)
        g["geometry"] = g.geometry.simplify(m["simplificar"], preserve_topology=True)
        g = g[["nombre", m["clave_geo"]] + cols + ["geometry"]].rename(columns={m["clave_geo"]: "codigo"})
        for c in cols:
            g[c] = g[c].round(3)
        js = json.loads(g.to_json(drop_id=True, na="null"))

        def red(c):
            return [red(x) for x in c] if isinstance(c, list) and c and isinstance(c[0], list) else [round(v, 5) for v in c]
        for f in js["features"]:
            f["geometry"]["coordinates"] = red(f["geometry"]["coordinates"])
        escribir_json(SITE / "datos" / "mapas" / f"{clave}.geojson", js)
        meta[clave] = {"titulo": m["titulo"], "fuente": m["fuente"], "fecha": m["fecha"],
                       "cols": [{"col": c, "etiqueta": e, "unidad": u, "capa": k, "divergente": dv} for c, e, u, k, dv in m["cols"]]}
    escribir_json(SITE / "datos" / "mapas" / "catalogo.json", meta)
    return meta


def datos_quien() -> None:
    e = pd.read_csv(ATLAS / "a_quien_ecv.csv")
    cols = ["anio", "grupo", "categoria", "indicador", "valor", "ic95_inf", "ic95_sup", "n_muestral", "muestra_pequena", "capa"]
    escribir_json(SITE / "datos" / "quien_ecv.json", [{k: limpio(v) for k, v in r.items()} for r in e[cols].to_dict("records")])
    p = pd.read_csv(ATLAS / "a_quien_epa.csv")
    cols = ["anio", "tramo_edad", "grupo", "categoria", "valor", "ic95_inf", "ic95_sup", "n_muestral", "capa", "nota"]
    escribir_json(SITE / "datos" / "quien_epa.json", [{k: limpio(v) for k, v in r.items()} for r in p[cols].to_dict("records")])


def fichas_verificador() -> list[dict]:
    out = []
    for f in sorted((RAIZ / "output/v5/verificador/fichas").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        out.append({**d, "version": "v5", "veredicto": d.get("veredicto", "")})
    for rel, ver in (("publicacion/verificador/fichas_v7_1.json", "v7.1"), ("publicacion/verificador/fichas_v8.json", "v8")):
        for d in json.loads((RAIZ / rel).read_text(encoding="utf-8")):
            out.append({**d, "version": ver})
    if (RAIZ / "output/v5/verificador/resumen.csv").exists():
        res = pd.read_csv(RAIZ / "output/v5/verificador/resumen.csv", dtype=str).set_index("id").veredicto.to_dict()
        for d in out:
            if not d.get("veredicto") and d["id"] in res:
                d["veredicto"] = res[d["id"]]
    return out


# ------------------------------------------------------------------------------------------------ fichas territoriales
def fichas_territoriales(env) -> list[dict]:
    prov = pd.read_csv(ATLAS / "d_espana_provincias.csv", dtype={"cod_provincia": str})
    cvm = pd.read_csv(ATLAS / "d_cv_municipios.csv", dtype={"cod_municipio": str})
    bar = pd.read_csv(ATLAS / "c_valencia_barrio.csv", dtype={"cod_barrio": str})
    ipva = pd.read_csv(ATLAS / "b_ipva_nuevo_existente.csv", dtype={"territorio_codigo": str})
    ult = ipva.periodo.max()
    pob_mun = consulta("""SELECT territorio_codigo, valor FROM h WHERE variable = 'pob_censo_anual' AND nivel = 'municipio'
                          AND periodo = '2025' AND desagregacion = 'nacionalidad=Total'""").set_index("territorio_codigo").valor
    alq_mun = consulta("""SELECT territorio_codigo, periodo, valor FROM h WHERE variable = 'serpavi_alquiler_m2_mediana'
                          AND nivel = 'municipio' AND desagregacion = 'tipologia=VC' AND periodo IN ('2019', '2024')""")
    alq_mun = alq_mun.pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    nom = consulta("SELECT territorio_codigo, nivel, nombre FROM t").set_index(["nivel", "territorio_codigo"]).nombre.to_dict()
    lista = []

    def fila(etq, v, u, capa, fuente, fecha, dec=1):
        return {"etiqueta": etq, "valor": "—" if v is None or pd.isna(v) else f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "unidad": u, "capa": capa, "fuente": fuente, "fecha": fecha}

    def ip(cod, nivel):
        x = ipva[(ipva.nivel == nivel) & (ipva.territorio_codigo == cod) & (ipva.periodo == ult)]
        return x.iloc[0] if len(x) else None

    for c, n in [(c, n) for (nv, c), n in nom.items() if nv == "ccaa"]:
        x = ip(c, "ccaa")
        filas = [fila("IPVA, contratos nuevos (2015=100)", x.nuevo if x is not None else None, "índice", "C4", "INE IPVA", ult),
                 fila("IPVA, contratos existentes (2015=100)", x.existente if x is not None else None, "índice", "C4", "INE IPVA", ult),
                 fila("Brecha nuevos − existentes", x.brecha_nuevo_menos_existente if x is not None else None, "puntos", "C4", "INE IPVA", ult)]
        hijos = prov[prov.cod_provincia.isin([k for (nv, k), _ in nom.items() if nv == "provincia" and k in set(prov.cod_provincia)])]
        lista.append({"tipo": "Comunidad autónoma", "codigo": c, "nombre": n, "url": f"fichas/ccaa_{c}.html", "filas": filas,
                      "indicador_serie": f"ccaa__p_tasado", "hijos": []})
        del hijos
    for r in prov.itertuples():
        x = ip(r.cod_provincia, "provincia")
        filas = [fila("Población 2025", r.pob_2025, "personas", "C1", "INE censo anual", "2025-01-01", 0),
                 fila("Población extranjera 2025", r.pct_extranj_2025, "%", "C1", "INE censo anual", "2025-01-01"),
                 fila("Valor tasado 2024", r.valor_tasado_2024, "€/m²", "C4", "MIVAU", "2024"),
                 fila("Alquiler mediano 2024 (SERPAVI)", r.alquiler_m2_2024, "€/m²/mes", "C4", "MIVAU SERPAVI", "2024", 2),
                 fila("Alquiler de 80 m² / renta por persona", r.alquiler_anual_80m2_pct_renta_persona, "%", "C4", "SERPAVI; INE ADRH", "2023-2024"),
                 fila("Déficit 2021-2025 (mediana)", r.deficit_2021_2025_mediana, "viviendas", "C4", "V5 (A4)", "2021-2025", 0),
                 fila("Brecha IPVA nuevos − existentes", x.brecha_nuevo_menos_existente if x is not None else None, "puntos", "C4", "INE IPVA", ult)]
        lista.append({"tipo": "Provincia", "codigo": r.cod_provincia, "nombre": r.nombre, "url": f"fichas/provincia_{r.cod_provincia}.html",
                      "filas": filas, "indicador_serie": "provincia__valor_tasado"})
    grandes = pob_mun[pob_mun >= 50000].index
    cvm_i = cvm.set_index("cod_municipio")
    for c in sorted(grandes):
        filas = [fila("Población 2025", pob_mun.get(c), "personas", "C1", "INE censo anual", "2025-01-01", 0),
                 fila("Alquiler mediano 2019 (SERPAVI)", alq_mun.at[c, "2019"] if c in alq_mun.index and "2019" in alq_mun else None, "€/m²/mes", "C4", "MIVAU SERPAVI", "2019", 2),
                 fila("Alquiler mediano 2024 (SERPAVI)", alq_mun.at[c, "2024"] if c in alq_mun.index and "2024" in alq_mun else None, "€/m²/mes", "C4", "MIVAU SERPAVI", "2024", 2)]
        if c in cvm_i.index:
            r = cvm_i.loc[c]
            filas += [fila("Población extranjera 2025", r.pct_extranj_2025, "%", "C1", "INE censo anual", "2025-01-01"),
                      fila("Viviendas turísticas (INE) por 100 inmuebles", r.vut_ine_por_100_inmuebles, "por 100", "C4", "INE; Catastro", "2026-05")]
        lista.append({"tipo": "Municipio (≥50.000 hab.)", "codigo": c, "nombre": nom.get(("municipio", c), c),
                      "url": f"fichas/municipio_{c}.html", "filas": filas})
    for r in bar.itertuples():
        filas = [fila("Población 2025", r.pob_2025, "personas (reparto por área)", "C4", "INE censo anual", "2025-01-01", 0),
                 fila("Población extranjera 2025", r.pct_extranj_2025, "%", "C4", "INE censo anual", "2025-01-01"),
                 fila("Alquiler mediano 2024", r.alquiler_m2_2024, "€/m²/mes", "C4", "MIVAU SERPAVI", "2024", 2),
                 fila("Variación del alquiler 2019-2024", r.var_alquiler_2019_2024_pct, "%", "C4", "MIVAU SERPAVI", "2019-2024"),
                 fila("Viviendas turísticas por 100 viviendas", r.vut_por_100_viv, "por 100", "C4", "INE (experimental); Censo 2021", "2026-05", 2),
                 fila("Renta neta por persona 2023", r.renta_persona_2023, "€", "C4", "INE ADRH", "2023", 0),
                 fila("Índice descriptivo de presión residencial", r.indice_presion_descriptivo, "z medio", "C4", "elaboración propia", "2019-2026", 2)]
        lista.append({"tipo": "Barrio de València", "codigo": r.cod_barrio, "nombre": str(r.nombre).title(),
                      "url": f"fichas/barrio_{r.cod_barrio}.html", "filas": filas})
    plantilla = env.get_template("ficha.html")
    for f in lista:
        (SITE / f["url"]).parent.mkdir(parents=True, exist_ok=True)
        (SITE / f["url"]).write_text(plantilla.render(**ctx("Ficha: " + f["nombre"], "fichas.html", "../"), ficha=f), encoding="utf-8")
    return lista


# ------------------------------------------------------------------------------------------------ plantillas de páginas
PLANTILLAS = {
"index.html": """{% extends "base.html" %}{% block contenido %}
<h1>Vivienda en España: lo que sabemos</h1>
<p class="lema">Una base de evidencia abierta: datos oficiales, cotas y modelos con su capa de evidencia. Cada cifra indica su fuente, su fecha y su capa.</p>
<p class="lema" lang="ca-valencia">Una base d'evidència oberta sobre l'habitatge: dades oficials, cotes i models amb la seua capa d'evidència. Cada xifra indica la font, la data i la capa.</p>
<div class="panel">{{ una_pagina|safe }}</div>
<h2>Atlas: quién sufre la subida y dónde <span lang="ca-valencia" class="meta">· Qui patix la pujada i on</span></h2>
<div class="panel">{{ atlas|safe }}</div>
<h2>Figuras</h2>
<div class="tarjetas">{% for f in figuras %}<figure class="tarjeta"><img src="figuras/{{ f.id }}.svg" alt="{{ f.texto_alternativo }}" loading="lazy">
<figcaption>{{ f.titulo }} <span class="capa {{ f.capa.split(' ')[0] }}">{{ f.capa.split(' ')[0] }}</span><br>{{ f.fuente }} · {{ f.fecha_dato }}</figcaption></figure>{% endfor %}</div>
{% endblock %}""",
"indicadores.html": """{% extends "base.html" %}{% block contenido %}
<h1>Indicadores <span class="meta" lang="ca-valencia">· Indicadors</span></h1>
<p class="lema">Elige nivel, indicador y territorios. Los datos desde 2026T3 (posteriores al pre-registro de V7 y V8) no se muestran aquí; los datos nuevos están en el <a href="monitor.html">monitor</a>.</p>
<div class="panel"><div class="controles">
<label>Nivel<select id="nivel"><option value="nacional">España</option><option value="ccaa" selected>Comunidades autónomas</option><option value="provincia">Provincias</option></select></label>
<label>Indicador<select id="indicador"></select></label>
<label>Territorios (Ctrl/Cmd para varios)<select id="territorios" multiple size="6"></select></label>
<label>Desde<input id="desde" type="number" value="2015" min="1995" max="2026"></label>
</div><div id="meta"></div><div id="grafico"></div>
<details><summary>Tabla de datos</summary><div id="tabla"></div></details><div id="descarga"></div></div>
{% endblock %}{% block guion %}<script>
(async () => {
  const cat = await V.json("datos/indicadores/catalogo.json");
  const selN = document.getElementById("nivel"), selI = document.getElementById("indicador"), selT = document.getElementById("territorios");
  let datos = null;
  const rellenaI = () => { selI.innerHTML = ""; cat.filter(c => c.nivel === selN.value).forEach(c => selI.append(V.el("option", { value: c.id, text: c.etiqueta }))); };
  const carga = async () => {
    datos = await V.json(`datos/indicadores/${selI.value}.json`);
    const terrs = [...new Map(datos.filas.map(f => [f[0], f[1]])).entries()];
    selT.innerHTML = "";
    terrs.forEach(([c, n], i) => selT.append(V.el("option", Object.assign({ value: c, text: n }, i < 4 ? { selected: "" } : {}))));
    dibuja();
  };
  const dibuja = () => {
    const sel = new Set([...selT.selectedOptions].map(o => o.value)), desde = String(document.getElementById("desde").value);
    const filas = datos.filas.filter(f => sel.has(f[0]) && f[2] >= desde).map(f => ({ codigo: f[0], nombre: f[1], periodo: f[2], valor: f[3] }));
    const m = datos.meta;
    document.getElementById("meta").replaceChildren(V.el("h2", { text: m.etiqueta }), V.meta(m));
    document.getElementById("grafico").replaceChildren(V.lineas(filas, { titulo: m.etiqueta, unidad: m.unidad }));
    document.getElementById("tabla").replaceChildren(V.tabla(filas, ["nombre", "codigo", "periodo", "valor"], ["Territorio", "Código INE", "Periodo", "Valor"]));
    document.getElementById("descarga").replaceChildren(V.descarga(V.csv(filas, ["codigo", "nombre", "periodo", "valor"]), `${m.id}.csv`));
  };
  selN.addEventListener("change", async () => { rellenaI(); await carga(); });
  selI.addEventListener("change", carga); selT.addEventListener("change", dibuja); document.getElementById("desde").addEventListener("change", dibuja);
  rellenaI(); await carga();
})();
</script>{% endblock %}""",
"mapas.html": """{% extends "base.html" %}{% block contenido %}
<h1>Mapas <span class="meta" lang="ca-valencia">· Mapes</span></h1>
<p class="lema">España por provincia, Comunitat Valenciana por municipio y València por barrio y sección. Mapas sin teselas externas; la tabla de debajo contiene los mismos datos que el mapa.</p>
<div class="panel"><div class="controles">
<label>Mapa<select id="capaMapa"></select></label><label>Indicador<select id="col"></select></label></div>
<div id="metaMapa"></div><div id="mapa" class="mapa" role="region" aria-label="Mapa coroplético; los datos equivalentes están en la tabla siguiente"></div>
<details open><summary>Tabla equivalente al mapa</summary><div id="tablaMapa"></div></details><div id="descargaMapa"></div></div>
{% endblock %}{% block guion %}<script>
(async () => {
  const cat = await V.json("datos/mapas/catalogo.json");
  const sC = document.getElementById("capaMapa"), sI = document.getElementById("col"), div = document.getElementById("mapa");
  let geo = null, mapa = null;
  Object.entries(cat).forEach(([k, m]) => sC.append(V.el("option", { value: k, text: m.titulo })));
  const rellena = () => { sI.innerHTML = ""; cat[sC.value].cols.forEach(c => sI.append(V.el("option", { value: c.col, text: c.etiqueta }))); };
  const dibuja = () => {
    const m = cat[sC.value], c = m.cols.find(x => x.col === sI.value);
    document.getElementById("metaMapa").replaceChildren(V.el("h2", { text: `${m.titulo}: ${c.etiqueta}` }), V.meta({ capa: c.capa, fuente: m.fuente, fecha_dato: m.fecha, unidad: c.unidad }));
    if (mapa) mapa.remove();
    mapa = V.mapa(div, geo, c.col, { etiqueta: c.unidad, decimales: 1, divergente: c.divergente });
    const filas = geo.features.map(f => ({ codigo: f.properties.codigo, nombre: f.properties.nombre, valor: f.properties[c.col] })).sort((a, b) => (b.valor ?? -1e18) - (a.valor ?? -1e18));
    document.getElementById("tablaMapa").replaceChildren(V.tabla(filas, ["nombre", "codigo", "valor"], ["Territorio", "Código", `${c.etiqueta} (${c.unidad})`]));
    document.getElementById("descargaMapa").replaceChildren(V.descarga(V.csv(filas, ["codigo", "nombre", "valor"]), `${sC.value}_${c.col}.csv`));
  };
  const carga = async () => { geo = await V.json(`datos/mapas/${sC.value}.geojson`); rellena(); dibuja(); };
  sC.addEventListener("change", carga); sI.addEventListener("change", dibuja);
  await carga();
})();
</script>{% endblock %}""",
"fichas.html": """{% extends "base.html" %}{% block contenido %}
<h1>Fichas territoriales <span class="meta" lang="ca-valencia">· Fitxes territorials</span></h1>
<p class="lema">Una ficha por comunidad autónoma, provincia, municipio de 50.000 habitantes o más y barrio de València. Generadas automáticamente desde la base.</p>
<label>Buscar <input id="buscar" type="search" placeholder="nombre o código INE"></label>
{% for tipo, grupo in fichas|groupby("tipo") %}<h2>{{ tipo }} ({{ grupo|length }})</h2><ul class="lista-fichas">
{% for f in grupo %}<li data-texto="{{ (f.nombre ~ ' ' ~ f.codigo)|lower }}"><a href="{{ f.url }}">{{ f.nombre }}</a> <span class="meta">{{ f.codigo }}</span></li>{% endfor %}</ul>{% endfor %}
{% endblock %}{% block guion %}<script>
document.getElementById("buscar").addEventListener("input", e => { const q = e.target.value.toLowerCase();
  document.querySelectorAll(".lista-fichas li").forEach(li => { li.hidden = q && !li.dataset.texto.includes(q); }); });
</script>{% endblock %}""",
"ficha.html": """{% extends "base.html" %}{% block contenido %}
<p class="meta"><a href="../fichas.html">← Fichas territoriales</a></p>
<h1>{{ ficha.nombre }} <span class="meta">{{ ficha.tipo }} · código INE {{ ficha.codigo }}</span></h1>
<table><thead><tr><th scope="col">Indicador</th><th scope="col" class="num">Valor</th><th scope="col">Unidad</th><th scope="col">Capa</th><th scope="col">Fuente</th><th scope="col">Dato</th></tr></thead><tbody>
{% for r in ficha.filas %}<tr><td>{{ r.etiqueta }}</td><td class="num">{{ r.valor }}</td><td>{{ r.unidad }}</td><td><span class="capa {{ r.capa }}">{{ r.capa }}</span></td><td>{{ r.fuente }}</td><td>{{ r.fecha }}</td></tr>{% endfor %}
</tbody></table>
<p class="meta">Descriptivo. Las afirmaciones sobre causas se evalúan en el <a href="../verificador.html">verificador</a>.</p>
{% endblock %}""",
"quien.html": """{% extends "base.html" %}{% block contenido %}
<h1>Quién sufre la subida <span class="meta" lang="ca-valencia">· Qui patix la pujada</span></h1>
<p class="lema">Microdatos de la Encuesta de Condiciones de Vida (2018-2025) y de la EPA (2018-2026T2). Intervalos al 95 % (linealización; los ficheros públicos no traen estratos, así que los intervalos son algo estrechos).</p>
<div class="panel"><div class="controles">
<label>Indicador<select id="ind">{% for k, v in indicadores_ecv.items() %}<option value="{{ k }}">{{ v }}</option>{% endfor %}</select></label>
<label>Grupo<select id="grupo"><option value="tenencia">Tenencia</option><option value="decil_renta">Decil de renta</option><option value="edad">Edad</option>
<option value="nacionalidad">Nacionalidad</option><option value="tipo_hogar">Tipo de hogar</option><option value="ccaa">CCAA</option><option value="total">Total</option></select></label>
<label>Año<select id="anio"></select></label></div>
<div id="metaQ"></div><div id="graficoQ"></div><details><summary>Tabla</summary><div id="tablaQ"></div></details><div id="descQ"></div></div>
{% for f in figuras %}<figure><img src="figuras/{{ f.id }}.svg" alt="{{ f.texto_alternativo }}"><figcaption>{{ f.titulo }}. {{ f.fuente }}. Capa {{ f.capa }}. {{ f.nota }}</figcaption></figure>{% endfor %}
{% endblock %}{% block guion %}<script>
(async () => {
  const d = await V.json("datos/quien_ecv.json");
  const ccaa = {{ nombres_ccaa|tojson }};
  const sA = document.getElementById("anio");
  [...new Set(d.map(r => r.anio))].sort().reverse().forEach(a => sA.append(V.el("option", { value: a, text: a })));
  const dibuja = () => {
    const ind = document.getElementById("ind").value, g = document.getElementById("grupo").value, a = +sA.value;
    const filas = d.filter(r => r.indicador === ind && r.grupo === g && r.anio === a)
      .map(r => ({ ...r, etiqueta: g === "ccaa" ? (ccaa[r.categoria] || r.categoria) : String(r.categoria) }));
    const capas = [...new Set(filas.map(r => r.capa))].join(", ");
    document.getElementById("metaQ").replaceChildren(V.meta({ capa: capas || "C4", fuente: "INE, ECV (microdatos), cálculo propio", fecha_dato: `ECV ${a} (renta del año anterior)`, unidad: ind.includes("mediana") ? "% de la renta (mediana)" : "% de personas" }));
    const fig = Plot.plot({ marginLeft: 190, width: 760, height: 40 + 26 * filas.length, x: { label: "%", grid: true },
      marks: [Plot.ruleY(filas, { y: "etiqueta", x1: "ic95_inf", x2: "ic95_sup", stroke: "#888" }),
              Plot.dot(filas, { y: "etiqueta", x: "valor", fill: "#0072B2", r: 4, tip: true }), Plot.ruleX([0])] });
    fig.setAttribute("role", "img"); fig.setAttribute("aria-label", "Puntos con intervalos por grupo; datos en la tabla");
    document.getElementById("graficoQ").replaceChildren(fig);
    document.getElementById("tablaQ").replaceChildren(V.tabla(filas, ["etiqueta", "valor", "ic95_inf", "ic95_sup", "n_muestral", "capa"], ["Grupo", "Valor", "IC 95 % inf.", "IC 95 % sup.", "n", "Capa"], { n_muestral: 0 }));
    document.getElementById("descQ").replaceChildren(V.descarga(V.csv(filas, ["anio", "grupo", "categoria", "indicador", "valor", "ic95_inf", "ic95_sup", "n_muestral", "capa"]), `ecv_${ind}_${g}_${a}.csv`));
  };
  ["ind", "grupo", "anio"].forEach(id => document.getElementById(id).addEventListener("change", dibuja));
  dibuja();
})();
</script>{% endblock %}""",
"verificador.html": """{% extends "base.html" %}{% block contenido %}
<h1>Verificador <span class="meta" lang="ca-valencia">· Verificador</span></h1>
<p class="lema">Afirmaciones frecuentes evaluadas con datos. El veredicto se refiere a la afirmación, nunca a quién la hace. Capa de la evidencia en cada ficha.</p>
<label>Buscar <input id="buscarV" type="search" placeholder="tema o palabra"></label>
<div class="tarjetas">{% for f in fichas %}<article class="tarjeta ficha-v" data-texto="{{ (f.tema ~ ' ' ~ f.enunciado)|lower }}" id="{{ f.id }}">
<p class="meta">{{ f.id }} · {{ f.version }} · {{ f.tema }}</p><h3>{{ f.enunciado }}</h3>
<p class="veredicto">{{ f.veredicto }} <span class="capa {{ f.capa }}">{{ f.capa }}</span></p>
<details><summary>Magnitud y límites</summary><p>{{ f.magnitud }}</p>{% if f.intervalo %}<p><strong>Intervalo:</strong> {{ f.intervalo }}</p>{% endif %}
{% if f.limites %}<p><strong>Límites:</strong> {{ f.limites }}</p>{% endif %}</details></article>{% endfor %}</div>
{% endblock %}{% block guion %}<script>
document.getElementById("buscarV").addEventListener("input", e => { const q = e.target.value.toLowerCase();
  document.querySelectorAll(".ficha-v").forEach(a => { a.hidden = q && !a.dataset.texto.includes(q); }); });
</script>{% endblock %}""",
"monitor.html": """{% extends "base.html" %}{% block contenido %}
<h1>Monitor <span class="meta" lang="ca-valencia">· Monitor</span></h1>
<p class="lema">Últimos datos publicados y su variación. Sin interpretación causal. Los datos desde 2026T3 son posteriores al pre-registro: se muestran como dato, sin compararlos con ninguna predicción hasta que se ejecuten las evaluaciones previstas (evaluate_v7 y evaluate_v8).</p>
{% if monitor %}<p class="meta">Actualizado: {{ monitor.fecha }} · {{ monitor.n }} series.</p>
<table><thead><tr><th scope="col">Serie</th><th scope="col">Territorio</th><th scope="col">Último periodo</th><th scope="col" class="num">Valor</th><th scope="col" class="num">Variación</th><th scope="col">Unidad</th><th scope="col">Capa</th><th scope="col">Fuente</th><th scope="col">Posterior al pre-registro</th></tr></thead><tbody>
{% for r in monitor.filas %}<tr><td>{{ r.etiqueta }}</td><td>{{ r.territorio }}</td><td>{{ r.periodo }}</td><td class="num">{{ r.valor }}</td><td class="num">{{ r.variacion }}</td><td>{{ r.unidad }}</td><td><span class="capa {{ r.capa }}">{{ r.capa }}</span></td><td>{{ r.fuente }}</td><td>{{ "sí" if r.posterior_prereg else "no" }}</td></tr>{% endfor %}
</tbody></table>{% else %}<p class="aviso">El monitor todavía no se ha ejecutado.</p>{% endif %}
{% endblock %}""",
"metodologia.html": """{% extends "base.html" %}{% block contenido %}
<h1>Metodología y datos <span class="meta" lang="ca-valencia">· Metodologia i dades</span></h1>
<h2 id="descargas">Descargas (capa pública)</h2>
<ul>{% for d in descargas %}<li><a href="{{ d.url }}">{{ d.nombre }}</a> <span class="meta">{{ d.desc }}</span></li>{% endfor %}</ul>
<p>Solo datos redistribuibles. Las fuentes sin licencia abierta clara (Notariado, Registradores, Incasòl, shocks JK) no se publican: aparecen solo como agregados ya publicados, con su nota.</p>
<h2 id="capas">Capas de evidencia</h2><div>{{ capas|safe }}</div>
<h2 id="diccionario">Diccionario de la base</h2><details><summary>Ver diccionario</summary>{{ diccionario|safe }}</details>
<h2 id="licencias">Licencias</h2><p>Variables no redistribuibles (excluidas de la capa pública): {{ no_redis|join(", ") }}.</p>
<h2 id="citar">Cómo citar</h2><pre>{{ citacion }}</pre><p>DOI: {{ version.doi }} (pendiente hasta el depósito en Zenodo).</p>
<h2 id="ia">Uso de IA</h2><div>{{ ia|safe }}</div>
<h2 id="errata">ERRATA</h2><div>{{ errata|safe }}</div>
<h2 id="english" lang="en">Methodology summary (English)</h2>
<div lang="en">
<p>This site presents the project's single evidence database. It combines official Spanish and European statistics: INE, the Ministry of Housing, the Bank of Spain, Eurostat, the ECB, the Valencian Government and Valencia City Council. Every figure states its source, data date and evidence layer.</p>
<ul>
<li><strong>C1:</strong> facts confirmed by at least two sources.</li>
<li><strong>C2:</strong> bounds with explicit assumptions.</li>
<li><strong>C3/C3s:</strong> effects from designs that pass falsification tests, or from explicit sign restrictions.</li>
<li><strong>C4:</strong> exploratory or single-source results.</li>
</ul>
<p>The atlas is descriptive and makes no causal claims. Territorial joins use INE codes only. Data from 2026Q3 onwards are shown in the monitor but are not compared with the frozen forecasts until the pre-registered evaluations are run. Only redistributable data are published.</p>
</div>
{% endblock %}""",
"historial.html": """{% extends "base.html" %}{% block contenido %}
<h1>Historial de versiones <span class="meta" lang="ca-valencia">· Historial de versions</span></h1>
<div>{{ historial|safe }}</div>
{% endblock %}""",
}


def ctx(titulo: str, actual: str, raiz: str = "") -> dict:
    version = json.loads((RAIZ / "consulta" / "version.json").read_text(encoding="utf-8"))
    return {"titulo": titulo, "actual": actual, "raiz": raiz, "paginas": PAGINAS, "version": version,
            "leaflet": actual == "mapas.html"}


def construir() -> dict:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    shutil.copytree(WEB / "vendor", SITE / "vendor")
    for f in (WEB / "src").iterdir():
        shutil.copy(f, SITE / f.name)
    (SITE / "figuras").mkdir()
    for f in (RAIZ / "figuras" / "web").glob("*.svg"):
        shutil.copy(f, SITE / "figuras" / f.name)
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    env = Environment(loader=ChoiceLoader([FileSystemLoader(WEB / "plantillas"), DictLoader(PLANTILLAS)]),
                      autoescape=select_autoescape(["html"]))
    catalogo = datos_indicadores()
    mapas = datos_mapas()
    datos_quien()
    figuras = json.loads((RAIZ / "figuras" / "fichas.json").read_text(encoding="utf-8"))
    una = (RAIZ / "publicacion" / "una_pagina.md").read_text(encoding="utf-8")
    atlas_md = (RAIZ / "publicacion" / "atlas_descriptivo.md").read_text(encoding="utf-8")
    hall = atlas_md.split("## Hallazgos", 1)[1].split("## Tablas", 1)[0] if "## Hallazgos" in atlas_md else atlas_md
    paginas = {"index.html": {"una_pagina": md(una.split("\n", 2)[-1] if una.startswith("<!--") else una), "atlas": md(hall),
                              "figuras": figuras}}
    nombres_ccaa = consulta("SELECT territorio_codigo, nombre FROM t WHERE nivel = 'ccaa'").set_index("territorio_codigo").nombre.to_dict()
    paginas["quien.html"] = {"figuras": [f for f in figuras if f["id"].startswith(("F01", "F02", "F14"))],
                             "nombres_ccaa": nombres_ccaa,
                             "indicadores_ecv": {"sobrecarga_40": "Sobrecarga del gasto en vivienda > 40 % de la renta",
                                                 "sobrecarga_30": "Sobrecarga > 30 %",
                                                 "esfuerzo_alquiler_mediana": "Esfuerzo de alquiler (mediana, alquiler de mercado)",
                                                 "esfuerzo_alquiler_40": "Alquiler > 40 % de la renta (alquiler de mercado)",
                                                 "esfuerzo_hipoteca_mediana": "Esfuerzo de hipoteca (mediana, cuota completa)",
                                                 "hacinamiento": "Hacinamiento (definición de Eurostat)",
                                                 "tenencia_3": "Viven en alquiler de mercado", "tenencia_2": "Propiedad con hipoteca"}}
    paginas["verificador.html"] = {"fichas": fichas_verificador()}
    mon = RAIZ / "output" / "v10" / "monitor" / "monitor.json"
    paginas["monitor.html"] = {"monitor": json.loads(mon.read_text(encoding="utf-8")) if mon.exists() else None}
    # descargas
    (SITE / "descargas").mkdir()
    descargas = []
    for f in sorted(PUB.glob("*.parquet")):
        shutil.copy(f, SITE / "descargas" / f.name)
        descargas.append({"url": f"descargas/{f.name}", "nombre": f.name, "desc": f"Parquet ({f.stat().st_size / 1e6:.1f} MB)"})
    for f in ("variables", "territorios", "cifras_clave"):
        pd.read_parquet(PUB / f"{f}.parquet").to_csv(SITE / "descargas" / f"{f}.csv", index=False)
        descargas.append({"url": f"descargas/{f}.csv", "nombre": f"{f}.csv", "desc": "CSV"})
    for f in sorted(ATLAS.glob("*.csv")):
        shutil.copy(f, SITE / "descargas" / f"atlas_{f.name}")
        descargas.append({"url": f"descargas/atlas_{f.name}", "nombre": f"atlas_{f.name}", "desc": "tabla del atlas (CSV)"})
    v = pd.read_parquet(RAIZ / "data/base/variables.parquet") if (RAIZ / "data/base/variables.parquet").exists() else pd.DataFrame()
    no_redis = sorted(v[~v.redistribuible].variable) if len(v) else []
    paginas["metodologia.html"] = {
        "descargas": descargas, "no_redis": no_redis,
        "diccionario": md((RAIZ / "docs/v10/diccionario_base.md").read_text(encoding="utf-8"), "docs/v10/"),
        "capas": md((RAIZ / "metodologia/capas.md").read_text(encoding="utf-8"), "metodologia/"),
        "citacion": (RAIZ / "CITATION.cff").read_text(encoding="utf-8"),
        "ia": md((RAIZ / "DECLARACION_IA.md").read_text(encoding="utf-8"), ""),
        "errata": md((RAIZ / "ERRATA.md").read_text(encoding="utf-8"), "")}
    paginas["historial.html"] = {"historial": md((RAIZ / "CHANGELOG.md").read_text(encoding="utf-8"), "")}
    fichas = fichas_territoriales(env)
    paginas["fichas.html"] = {"fichas": fichas}
    paginas.setdefault("indicadores.html", {})
    paginas.setdefault("mapas.html", {})
    titulos = {p["url"]: p["es"] for p in PAGINAS}
    for nombre, extra in paginas.items():
        html = env.get_template(nombre).render(**ctx(titulos[nombre], nombre), **extra)
        (SITE / nombre).write_text(html, encoding="utf-8")
    with open(SITE / "sitemap.txt", "w", encoding="utf-8") as fh:
        for p in sorted(SITE.rglob("*.html")):
            fh.write(URL_PREVISTA + p.relative_to(SITE).as_posix() + "\n")
    tam = sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file())
    res = {"paginas": len(list(SITE.rglob("*.html"))), "indicadores": len(catalogo), "mapas": len(mapas),
           "fichas_territoriales": len(fichas), "tamano_mb": round(tam / 1e6, 1), "url_prevista": URL_PREVISTA}
    with open(RAIZ / "output" / "v10" / "web_resumen.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["clave", "valor"])
        w.writerows(res.items())
    return res


if __name__ == "__main__":
    print(construir())
