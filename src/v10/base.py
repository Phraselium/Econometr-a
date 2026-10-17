"""V10-B1 · `make base`: base de datos única del proyecto (sin red; SEED no aplica: no hay nada aleatorio).

Entradas (solo lectura): data/processed (paneles v1, v7 y v8; València), data/raw/v9 (descargas V9 con manifiesto),
data/raw/v10/geo (geometrías), publicacion/cifras_clave.csv y los diccionarios de variables de docs/.

Salidas:
  data/base/hechos.parquet              tabla larga completa (todas las filas; incluye las no redistribuibles)
  data/base/publica/hechos.parquet      solo filas redistribuibles (la que usa la web)
  data/base/territorios.parquet         dimensión territorial con jerarquía (código INE como clave)
  data/base/variables.parquet           dimensión de variables (definición, unidad, capa, fuente, licencia)
  data/base/cifras_clave.parquet        copia tipada de publicacion/cifras_clave.csv (test de identidad)
  data/base/regulacion_zonas.parquet    zonas tensionadas (v9) con fechas y alcance
  data/base/vivienda.duckdb             todo lo anterior como tablas DuckDB (no versionado: se regenera)
  data/base/geo/*.parquet y data/base/geo/web/*.geojson   (src/v10/geo.py)
  docs/v10/diccionario_base.md          diccionario único generado

Reglas:
- clave única: (territorio_codigo, nivel, periodo, frecuencia, variable, desagregacion);
- si la misma clave aparece en varios paneles, se queda la versión más reciente (v8 > v7 > v1) y se cuentan las
  discrepancias (docs/v10/diccionario_base.md);
- `posterior_prereg` = periodo que empieza el 2026-07-01 o después (evaluate_v7/evaluate_v8): esas filas se marcan y
  no entran en ningún cálculo del atlas;
- `muestra_sellada_v6` marca las provincias del sellado transversal de v6 y, desde V15, sus municipios, distritos y
  secciones (solo se leen a través de src/holdout.py; los módulos de V10-V14 que las usaron están en
  docs/v15/contaminacion_v6.md; data/sealed no se lee);
- solo descriptivo: no se estima nada.
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v11 import base_v11  # noqa: E402
from src.v11.base_v11 import META_V11  # noqa: E402
from src.v12 import base_v12  # noqa: E402

META_V11 = {**META_V11, **base_v12.META_V12}   # V12: variables v12_* (src/v12/base_v12.py)
PROC = RAIZ / "data" / "processed"
RAW = RAIZ / "data" / "raw"
RAW9 = RAW / "v9"
RAW11 = RAW / "v11"
BASE = RAIZ / "data" / "base"
PUB = BASE / "publica"
DOCS = RAIZ / "docs" / "v10"

COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente",
        "edicion", "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg",
        "muestra_sellada_v6"]
CLAVE = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion"]

CCAA = {"01": "Andalucía", "02": "Aragón", "03": "Asturias, Principado de", "04": "Balears, Illes", "05": "Canarias",
        "06": "Cantabria", "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña",
        "10": "Comunitat Valenciana", "11": "Extremadura", "12": "Galicia", "13": "Madrid, Comunidad de",
        "14": "Murcia, Región de", "15": "Navarra, Comunidad Foral de", "16": "País Vasco", "17": "Rioja, La",
        "18": "Ceuta", "19": "Melilla"}

# Columnas que no son variables de nivel propias del territorio del panel (comunes nacionales, dummies de modelo,
# exposiciones fijas, banderas de sellado)
EXCLUIR_PREF = ("ln_", "d_ln_", "d4_ln_", "d_", "nac_", "jk_", "hpi_ea", "bis_", "quiebre_", "exp_", "prov_sellada",
                "anio_embargo", "P_")
EXCLUIR = {"covid", "epa2021", "etcl2008", "P1", "P2", "P3", "P4", "P5", "periodo_h8", "ley12_2023_nac",
           "tope_actualiz_rentas_nac", "registro_unico_arrend_nac", "fianzas_parcial", "cod_ccaa", "codigo_ine_ccaa",
           "ccaa", "cod_prov", "anio", "trimestre", "fecha", "deflactor_pib", "ipc_general", "hicp_yoy", "q1", "q2", "q3", "q4"}
# Fuentes sin licencia abierta clara (docs/v8_1/inventario_licencias.csv, datos_retirados.md, v9 manifiestos)
NO_REDISTRIBUIBLE = re.compile(r"^(registr|notariado|jk_|incasol_|airdna|idealista|fotocasa|cgn_)", re.I)
# Por defecto NO se redistribuye: una variable entra en la capa pública solo si su fuente es de un organismo con
# licencia abierta o reutilización con cita (lista explícita) o si figura en FUENTES_DOCUMENTADAS (revisión V10, R6).
FUENTE_PERMITIDA = re.compile(r"\bINE\b|ine_|Eurostat|eurostat|\bBCE\b|\bECB\b|ecb_|Banco de España|\bBdE\b|bde_|MIVAU|mivau|"
                              r"Ministerio de Vivienda|SERPAVI|serpavi|\bGVA\b|gva_|Generalitat Valenciana|Gobierno Vasco|EMAL|"
                              r"Ajuntament|Catastro|catastro|\bBOE\b|Resultado publicado|elaboración propia|Inside Airbnb|\bBIS\b|OCDE")
FUENTES_DOCUMENTADAS = {   # variables de paneles sin fila de diccionario: fuente comprobada en el script del panel
    "costes": "Eurostat, sts_copi_q (coste de construcción residencial)", "hpi_eurostat": "Eurostat, prc_hpi_q",
    "prod_constr": "Eurostat, sts_copr (producción de la construcción)", "renta_hog": "INE, Contabilidad Nacional Trimestral",
    "permisos": "MIVAU, visados de dirección de obra", "iniciadas": "MIVAU, viviendas libres iniciadas",
    "iniciadas_anual_tabla": "MIVAU, viviendas libres iniciadas (tabla anual)", "terminadas_anual_tabla": "MIVAU, viviendas libres terminadas (tabla anual)",
    "ipc_alquiler_indice": "INE, IPC de alquiler por provincia", "ipva": "INE, IPVA municipal (59060)",
    "ocupados_epa": "INE, EPA por provincia", "pob_extranjera": "INE, Padrón continuo", "pob_extranjera_gva": "GVA (IVE), Padrón municipal",
    "vut_pct_sobre_total": "INE, viviendas turísticas (experimental)", "vut_plazas_por_vivienda": "INE, viviendas turísticas (experimental)",
    "vut_viviendas_turisticas": "INE, viviendas turísticas (experimental)", "vut_stock_gva": "GVA, registro de turismo (CC BY 4.0)",
    "serpavi_vc_dist_agg": "MIVAU, SERPAVI por distritos",
    "compraventas_sa": "INE, ETDP (desestacionalización propia STL)", "ocupados_sa": "INE, EPA (desestacionalización propia STL)",
    "dif_hip_euribor_bce": "BCE, MIR y Euríbor (diferencia propia)", "dif_hip_euribor_bde": "BdE, tipo hipotecario y Euríbor (diferencia propia)",
    "inflacion_deflactor": "INE, CNT (deflactor; cálculo propio)", "inflacion_ipc_yoy": "INE, IPC (cálculo propio)",
    "tipo_hip_real": "BdE e INE IPC (tipo real; cálculo propio)", "tipo_hip_real_bce": "BCE e INE IPC (tipo real; cálculo propio)",
    "tipo_hip_real_bde": "BdE e INE IPC (tipo real; cálculo propio)", "renta_hog_real": "INE, CNT (renta real; cálculo propio)",
    "pib_ccaa_q": "INE, Contabilidad Regional (trimestralización propia)", "pob_europa_sin_espana": "INE, Estadística Continua de Población (77019)",
    "tope_rentas_ccaa_alt_v3": "BOE, Ley catalana 11/2020 (evento)", "tope_rentas_ccaa_frac": "BOE, Ley catalana 11/2020 (evento)",
    "vut_regulacion_ccaa": "BOE, normas autonómicas de viviendas de uso turístico (evento)",
    "zt_declarada": "BOE, resoluciones de zonas tensionadas (evento)", "zt_n_municipios": "BOE, resoluciones de zonas tensionadas (evento)", **{f"serpavi_dist_{t}_{e}": "MIVAU, SERPAVI por distritos"
                                                              for t in ("vc", "vu") for e in ("mediana", "n_contratos", "p25", "p75")},
    **{f"pob_{g}": "INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019)" for g in
       ("africa", "apatridas", "asia", "centroamerica_caribe", "europa_no_ue27", "europa_no_ue28", "norteamerica", "oceania",
        "sudamerica", "ue27_sin_espana", "ue28_sin_espana")},
    **{f"pob_vlc_{g}": "INE, Padrón continuo (València por nacionalidad)" for g in ("africa", "alemania", "america", "asia", "europa", "reino_unido")},
}
FUENTE_NO_REDISTRIBUIBLE = re.compile(r"registradores|notariado|jaroci|incas[oò]l|airdna|idealista|fotocasa", re.I)


# ----------------------------------------------------------------------------------------------- utilidades
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def periodo_y_frecuencia(p: str) -> tuple[str, str]:
    p = str(p).strip()
    if m := re.fullmatch(r"(\d{4})[QT]([1-4])", p):
        return f"{m.group(1)}T{m.group(2)}", "T"
    if m := re.fullmatch(r"(\d{4})-Q([1-4])", p):
        return f"{m.group(1)}T{m.group(2)}", "T"
    if re.fullmatch(r"\d{4}", p):
        return p, "A"
    if m := re.fullmatch(r"(\d{4})-?M?(\d{2})", p):
        return f"{m.group(1)}-{m.group(2)}", "M"
    if m := re.fullmatch(r"(\d{4})S([12])", p):
        return f"{m.group(1)}S{m.group(2)}", "S"
    if m := re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", p):
        return p, "D"
    return p, "?"


def _inicio_fin(periodo: str, frec: str) -> tuple[str, str]:
    t = None
    if frec == "A":
        t = pd.Period(periodo, freq="Y")
    elif frec == "T":
        t = pd.Period(periodo.replace("T", "Q"), freq="Q")
    elif frec == "M":
        t = pd.Period(periodo, freq="M")
    elif frec == "S":
        a, h = periodo.split("S")
        ini = pd.Timestamp(f"{a}-{'01' if h == '1' else '07'}-01")
        return ini.strftime("%Y-%m-%d"), (ini + pd.offsets.MonthEnd(6)).strftime("%Y-%m-%d")
    elif frec == "D":
        return periodo, periodo
    if t is None:
        return "", ""
    return t.start_time.strftime("%Y-%m-%d"), t.end_time.strftime("%Y-%m-%d")


# ----------------------------------------------------------------------------------------------- diccionarios
def leer_tablas_md(ruta: Path) -> list[dict]:
    filas, cab = [], None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if not linea.startswith("|"):
            cab = None
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if cab is None:
            cab = [norm(c) for c in celdas]
            continue
        if set("".join(celdas)) <= set("-: "):
            continue
        if len(celdas) == len(cab):
            filas.append(dict(zip(cab, celdas)))
    return filas


def metadatos_variables() -> dict[str, dict]:
    """Definición, unidad, fuente y capa por variable desde los diccionarios del proyecto (v8 > v7 > v6 > v1)."""
    meta: dict[str, dict] = {}
    for rel in ("docs/diccionario_variables.md", "docs/v6/diccionario.md", "docs/v7/diccionario.md", "docs/v8/diccionario.md"):
        for f in leer_tablas_md(RAIZ / rel):
            var = f.get("variable", "").strip("`* ")
            if not var or var.startswith("-") or " " in var:
                continue
            capa_txt = f.get("capa", "")
            capa = re.search(r"C[1-4]s?", capa_txt).group(0) if re.search(r"C[1-4]s?", capa_txt) else ""
            nuevo = {"definicion": f.get("definicion") or f.get("definicion_y_transformacion") or "",
                     "unidad": f.get("unidad", ""),
                     "fuente": f.get("fuente") or f.get("fuente_data_raw") or f.get("fuente_fichero_y_serie") or "",
                     "capa": capa, "dic": rel}
            previo = meta.get(var, {})
            meta[var] = {k: (nuevo[k] if nuevo[k] and nuevo[k] != "—" else previo.get(k, "")) for k in nuevo}
            meta[var]["dic_capa"] = rel if capa else previo.get("dic_capa", "")
    return meta


def estado_licencias() -> dict[str, str]:
    inv = pd.read_csv(RAIZ / "docs/v8_1/inventario_licencias.csv", dtype=str)
    return {Path(f).name.lower(): e for f, e in zip(inv.fichero, inv.estado)}


# ----------------------------------------------------------------------------------------------- territorios
def territorios() -> pd.DataFrame:
    m = pd.read_excel(RAW / "ine_diccionario_municipios_2026.xlsx", dtype=str, header=1)
    filas = [{"territorio_codigo": "00", "nivel": "nacional", "nombre": "España", "padre_codigo": "", "padre_nivel": "",
              "cod_ccaa": "", "cod_provincia": "", "fuente": "INE"}]
    filas += [{"territorio_codigo": c, "nivel": "ccaa", "nombre": n, "padre_codigo": "00", "padre_nivel": "nacional",
               "cod_ccaa": c, "cod_provincia": "", "fuente": "INE (códigos de CCAA)"} for c, n in CCAA.items()]
    prov_ccaa = m.drop_duplicates("CPRO").set_index("CPRO").CODAUTO
    nombres_prov = provincias_nombres()
    filas += [{"territorio_codigo": p, "nivel": "provincia", "nombre": nombres_prov.get(p, p), "padre_codigo": c,
               "padre_nivel": "ccaa", "cod_ccaa": c, "cod_provincia": p, "fuente": "INE"} for p, c in prov_ccaa.items()]
    filas += [{"territorio_codigo": r.CPRO + r.CMUN, "nivel": "municipio", "nombre": r.NOMBRE, "padre_codigo": r.CPRO,
               "padre_nivel": "provincia", "cod_ccaa": r.CODAUTO, "cod_provincia": r.CPRO,
               "fuente": "INE, relación de municipios 2026"} for r in m.itertuples()]
    t = pd.DataFrame(filas)
    geo = BASE / "geo"
    if (geo / "secciones.parquet").exists():
        import geopandas as gpd
        s = gpd.read_parquet(geo / "secciones.parquet").drop(columns="geometry")
        dist = s.drop_duplicates("cod_distrito")
        extra = [pd.DataFrame({"territorio_codigo": dist.cod_distrito, "nivel": "distrito",
                               "nombre": dist.cod_municipio.map(t[t.nivel == "municipio"].set_index("territorio_codigo").nombre) + " distrito " + dist.cod_distrito.str[-2:],
                               "padre_codigo": dist.cod_municipio, "padre_nivel": "municipio", "cod_ccaa": dist.cod_ccaa,
                               "cod_provincia": dist.cod_provincia, "fuente": "INE, seccionado 2025"}),
                 pd.DataFrame({"territorio_codigo": s.cod_seccion, "nivel": "seccion", "nombre": "sección " + s.cod_seccion,
                               "padre_codigo": s.cod_distrito, "padre_nivel": "distrito", "cod_ccaa": s.cod_ccaa,
                               "cod_provincia": s.cod_provincia, "fuente": "INE, seccionado 2025"})]
        if (geo / "barrios_valencia.parquet").exists():
            b = gpd.read_parquet(geo / "barrios_valencia.parquet").drop(columns="geometry")
            extra.append(pd.DataFrame({"territorio_codigo": b.cod_barrio, "nivel": "barrio", "nombre": b.nombre,
                                       "padre_codigo": b.cod_distrito, "padre_nivel": "distrito", "cod_ccaa": "10",
                                       "cod_provincia": "46", "fuente": "Ajuntament de València (CC BY 4.0)"}))
        t = pd.concat([t, *extra], ignore_index=True)
    return t.drop_duplicates(["territorio_codigo", "nivel"]).reset_index(drop=True)


def provincias_nombres() -> dict[str, str]:
    d = pd.read_csv(RAW9 / "ine_ipva/ipva_provincia_antiguedad.csv", dtype=str)
    lab = d["Provincias"].dropna().unique()
    out = {x[:2]: x[3:] for x in lab if re.match(r"^\d{2} ", x)}
    out.setdefault("01", "Araba/Álava")
    out.setdefault("20", "Gipuzkoa")
    out.setdefault("31", "Navarra")
    out.setdefault("48", "Bizkaia")
    return out


# ----------------------------------------------------------------------------------------------- cargadores
def ancho_a_largo(ruta: Path, terr: str | None, nivel: str, per_col: str, origen: str) -> pd.DataFrame:
    d = pd.read_csv(ruta, dtype={terr: str} if terr else None, low_memory=False)
    vals = [c for c in d.columns if c not in EXCLUIR and not c.startswith(EXCLUIR_PREF)
            and not c.endswith(("_metodo", "_interp")) and pd.api.types.is_numeric_dtype(d[c])
            and not pd.api.types.is_bool_dtype(d[c])]
    codigo = d[terr].astype(str).str.zfill(2 if nivel in ("ccaa", "provincia") else 5) if terr else pd.Series("00", index=d.index)
    partes = []
    for v in vals:
        x = pd.DataFrame({"territorio_codigo": codigo, "periodo_raw": d[per_col].astype(str), "variable": v,
                          "valor": d[v]})
        if f"{v}_metodo" in d:
            x["metodo_dato"] = d[f"{v}_metodo"].astype("string")
        elif f"{v}_interp" in d:
            x["metodo_dato"] = d[f"{v}_interp"].map({True: "interpolado", False: "observado"}).astype("string")
        else:
            x["metodo_dato"] = pd.NA
        partes.append(x.dropna(subset=["valor"]))
    out = pd.concat(partes, ignore_index=True)
    out["nivel"], out["origen"], out["desagregacion"] = nivel, origen, ""
    return out


def procesados() -> pd.DataFrame:
    p = PROC
    fuentes = [  # (fichero, columna de territorio, nivel, columna de periodo, prioridad)
        ("nacional_q.csv", None, "nacional", "trimestre", 1), ("nacional_a.csv", None, "nacional", "anio", 1),
        ("panel_ccaa_q.csv", "codigo_ine_ccaa", "ccaa", "trimestre", 1), ("panel_ccaa_a.csv", "codigo_ine_ccaa", "ccaa", "anio", 1),
        ("v7/panel_ccaa_q_v7.csv", "codigo_ine_ccaa", "ccaa", "trimestre", 2),
        ("v7/panel_prov_q_v7.csv", "cod_prov", "provincia", "trimestre", 2),
        ("v7/panel_prov_a_v7.csv", "cod_prov", "provincia", "anio", 2),
        ("v8/nacional_q_v8.csv", None, "nacional", "trimestre", 3),
        ("v8/panel_ccaa_q_v8.csv", "codigo_ine_ccaa", "ccaa", "trimestre", 3),
        ("v8/cv_prov_q_v8.csv", "cod_prov", "provincia", "trimestre", 3),
        ("v8/cv_prov_a_v8.csv", "cod_prov", "provincia", "anio", 3)]
    partes = []
    for f, terr, nivel, per, prio in fuentes:
        x = ancho_a_largo(p / f, terr, nivel, per, f"data/processed/{f}")
        x["prioridad"] = prio
        partes.append(x)
    # València (formato largo propio)
    v = pd.read_csv(p / "valencia.csv", dtype=str)
    mapa = {"España": ("00", "nacional"), "Comunitat Valenciana": ("10", "ccaa"), "Provincia de València": ("46", "provincia"),
            "València (municipio)": ("46250", "municipio")}
    cod = v.territorio.map(lambda t: mapa.get(t, (t.split()[-1], "distrito") if "distrito" in t else (None, None)))
    v["territorio_codigo"], v["nivel"] = cod.str[0], cod.str[1]
    v = v.dropna(subset=["territorio_codigo"])
    partes.append(pd.DataFrame({"territorio_codigo": v.territorio_codigo, "periodo_raw": v.periodo, "variable": v.variable,
                                "valor": pd.to_numeric(v.valor, errors="coerce"), "metodo_dato": v.metodo,
                                "nivel": v.nivel, "origen": "data/processed/valencia.csv", "desagregacion": "",
                                "prioridad": 1}).dropna(subset=["valor"]))
    w = pd.read_csv(p / "v8/valencia_ciudad_v8.csv", dtype=str)
    partes.append(pd.DataFrame({"territorio_codigo": w.codigo_ine, "periodo_raw": w.periodo, "variable": w.variable,
                                "valor": pd.to_numeric(w.valor, errors="coerce"), "metodo_dato": w.metodo,
                                "nivel": w.nivel.replace({"municipio": "municipio"}), "origen": "data/processed/v8/valencia_ciudad_v8.csv",
                                "desagregacion": "", "prioridad": 3}).dropna(subset=["valor"]))
    return partes


def v9() -> pd.DataFrame:
    partes = []

    def add(df, origen, prio=4):
        df = df.copy()
        df["origen"], df["prioridad"] = origen, prio
        for c in ("metodo_dato", "desagregacion"):
            if c not in df:
                df[c] = "" if c == "desagregacion" else pd.NA
        partes.append(df)

    # Censo anual por sección y país de nacionalidad
    c = pd.read_csv(RAW9 / "ine_censo_anual/censo_seccion_pais.csv.gz", dtype=str)
    cod = np.where(c.nivel == "seccion", c.cod_seccion, np.where(c.nivel == "municipio", c.cod_municipio, c.cod_provincia))
    add(pd.DataFrame({"territorio_codigo": cod, "nivel": c.nivel, "periodo_raw": c.edicion, "variable": "pob_censo_anual",
                      "desagregacion": "nacionalidad=" + c.pais_nacionalidad, "valor": pd.to_numeric(c.poblacion),
                      "metodo_dato": "observado"}), "data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz")
    # IPVA por antigüedad del contrato (CCAA y provincia) y por distritos de capitales
    for f, col, nivel in (("ipva_ccaa_antiguedad", "Comunidades y Ciudades Autónomas", "ccaa"),
                          ("ipva_provincia_antiguedad", "Provincias", "provincia")):
        d = pd.read_csv(RAW9 / f"ine_ipva/{f}.csv", dtype=str)
        terr = d[col].fillna("00 Total").str.split(" ").str[0]
        niv = np.where(d[col].isna(), "nacional", nivel)
        var = np.where(d["Tipo de dato"] == "Índice", "ipva_indice", "ipva_var_anual")
        add(pd.DataFrame({"territorio_codigo": terr, "nivel": niv, "periodo_raw": d.periodo, "variable": var,
                          "desagregacion": "contrato=" + d["Antigüedad del contrato de arrendamiento"],
                          "valor": pd.to_numeric(d.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
            f"data/raw/v9/ine_ipva/{f}.csv")
    d = pd.read_csv(RAW9 / "ine_ipva/ipva_distrito_capitales.csv", dtype=str).dropna(subset=["Distritos"])
    add(pd.DataFrame({"territorio_codigo": d.Distritos.str.split(" ").str[0], "nivel": "distrito", "periodo_raw": d.periodo,
                      "variable": np.where(d["Tipo de dato"] == "Índice", "ipva_indice", "ipva_var_anual"),
                      "desagregacion": "contrato=Total", "valor": pd.to_numeric(d.valor, errors="coerce"),
                      "metodo_dato": "observado"}).dropna(subset=["valor"]), "data/raw/v9/ine_ipva/ipva_distrito_capitales.csv")
    # Registro de viviendas turísticas de la GVA (cortes = C1; mensual reconstruido = C4)
    g = pd.read_csv(RAW9 / "gva_vut/gva_vut_panel_municipio.csv", dtype=str)
    g = g[g.ine5 != "03000"]
    add(pd.DataFrame({"territorio_codigo": g.ine5, "nivel": "municipio",
                      "periodo_raw": np.where(g.tipo == "corte", g.fecha, g.fecha),
                      "variable": np.where(g.tipo == "corte", "vut_registro_gva", "vut_registro_gva_reconstruido"),
                      "valor": pd.to_numeric(g.stock), "metodo_dato": np.where(g.tipo == "corte", "observado", "reconstruido")}),
        "data/raw/v9/gva_vut/gva_vut_panel_municipio.csv")
    # EMAL Euskadi: filas municipales trimestrales
    e = pd.read_csv(RAW9 / "emal/emal_largo.csv", dtype=str)
    e = e[e.codigo_ine.notna() & e.periodo.str.fullmatch(r"\d{4}T[1-4]")]
    add(pd.DataFrame({"territorio_codigo": e.codigo_ine, "nivel": "municipio", "periodo_raw": e.periodo,
                      "variable": "emal_" + e.variable,
                      "desagregacion": "libro=" + e.libro + "|ambito=" + e.nombre.fillna("") + "|hoja=" + e.hoja + "|grupo=" + e.grupo.fillna("") + "|contrato=" + e.tipo_contrato.fillna(""),
                      "valor": pd.to_numeric(e.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/emal/emal_largo.csv")
    # Inside Airbnb por sección (C4, no oficial)
    a = pd.read_csv(RAW9 / "insideairbnb/insideairbnb_seccion.csv.gz", dtype=str)
    num = [x for x in a.columns if x not in ("ciudad", "edicion", "cod_seccion") and pd.to_numeric(a[x], errors="coerce").notna().all()]
    for x in num:
        add(pd.DataFrame({"territorio_codigo": a.cod_seccion, "nivel": "seccion", "periodo_raw": a.edicion.str[:7],
                          "variable": "iab_" + x, "valor": pd.to_numeric(a[x]), "metodo_dato": "agregado (join espacial)"}),
            "data/raw/v9/insideairbnb/insideairbnb_seccion.csv.gz")
    # BCE: tipos y volúmenes por país (nivel país, código ISO-2)
    b = pd.read_csv(RAW9 / "bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz", dtype=str)
    add(pd.DataFrame({"territorio_codigo": b.pais, "nivel": "pais", "periodo_raw": b.periodo,
                      "variable": np.where(b.fijacion_codigo == "A_volumen", "bce_hip_volumen_nuevas", "bce_hip_tipo_nuevas"),
                      "desagregacion": np.where(b.fijacion_codigo == "A_volumen", "", "fijacion=" + b.fijacion_codigo),
                      "valor": pd.to_numeric(b.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz")
    # Eurostat: noches en alojamientos reservados por plataformas (NUTS 3, anual)
    u = pd.read_csv(RAW9 / "eurostat_plataformas/tour_ce_oan3.csv.gz", dtype=str)
    u = u[u.geo.str.startswith("ES")]
    add(pd.DataFrame({"territorio_codigo": u.geo, "nivel": "nuts3", "periodo_raw": u.periodo,
                      "variable": "eurostat_plataformas_noches", "desagregacion": "indicador=" + u.indicador,
                      "valor": pd.to_numeric(u.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/eurostat_plataformas/tour_ce_oan3.csv.gz")
    # --- V9 COMPLETO (F1): fuentes nuevas ---------------------------------------------------------------------
    # IDESCAT: viviendas de uso turístico y apartamentos turísticos por municipio (stock a 31-dic)
    t = pd.read_csv(RAW9 / "cat_turisme/idescat_allotjaments_municipi.csv.gz", dtype=str)
    corto = {"habitatges_us_turistic": "hut", "apartaments_turistics": "apartamentos"}
    t = t[t.tipo.isin(corto)]
    add(pd.DataFrame({"territorio_codigo": t.cod_ine, "nivel": "municipio", "periodo_raw": t.anio,
                      "variable": "idescat_" + t.tipo.map(corto) + "_" + t.medida.str.lower().map({"establiments": "n", "places": "plazas"}),
                      "valor": pd.to_numeric(t.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/cat_turisme/idescat_allotjaments_municipi.csv.gz")
    # Padrón continuo por nacionalidad: total provincial = suma de municipios (el fichero municipal queda en data/raw/v9)
    pn = pd.read_csv(RAW9 / "ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz", dtype=str)
    pn = pn[pn.cod_municipio.notna()]
    pn = pn.assign(poblacion=pd.to_numeric(pn.poblacion)).groupby(["cod_provincia", "anio", "nacionalidad"], as_index=False).poblacion.sum()
    add(pd.DataFrame({"territorio_codigo": pn.cod_provincia, "nivel": "provincia", "periodo_raw": pn.anio,
                      "variable": "padron_pob_nacionalidad", "desagregacion": "nacionalidad=" + pn.nacionalidad,
                      "valor": pn.poblacion, "metodo_dato": "suma de municipios"}),
        "data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz")
    # Migraciones (EM 2008-2021 y EMCR 2021-2024): saldos y flujos por provincia
    for f, var, col_nac in (("ine_em_24385", "em_saldo_interprovincial", "Nacionalidad"),
                            ("ine_em_24323", "em_inmigracion_extranjero", "Nacionalidad"),
                            ("ine_em_24326", "em_emigracion_extranjero", "Nacionalidad")):
        m = pd.read_csv(RAW9 / f"ine_migraciones/{f}.csv.gz", dtype=str)
        m = m[m.Provincias.str.match(r"^\d{2} ")]
        add(pd.DataFrame({"territorio_codigo": m.Provincias.str[:2], "nivel": "provincia", "periodo_raw": m.Periodo,
                          "variable": var, "desagregacion": "nacionalidad=" + m[col_nac],
                          "valor": pd.to_numeric(m.Total.str.replace(".", "", regex=False), errors="coerce"),
                          "metodo_dato": "observado"}).dropna(subset=["valor"]), f"data/raw/v9/ine_migraciones/{f}.csv.gz")
    m = pd.read_csv(RAW9 / "ine_migraciones/ine_emcr_69764.csv.gz", dtype=str)
    m = m[m.Provincias.fillna("").str.match(r"^\d{2} ")]
    add(pd.DataFrame({"territorio_codigo": m.Provincias.str[:2], "nivel": "provincia", "periodo_raw": m.Periodo,
                      "variable": "emcr_saldo", "desagregacion": "tipo=" + m["Tipo de saldo"] + "|nacionalidad=" + m.Nacionalidad,
                      "valor": pd.to_numeric(m.Total.str.replace(".", "", regex=False), errors="coerce"),
                      "metodo_dato": "observado"}).dropna(subset=["valor"]), "data/raw/v9/ine_migraciones/ine_emcr_69764.csv.gz")
    # SEPE: paro registrado y contratos por municipio, media anual de los meses publicados (cálculo propio)
    for var in ("paro_registrado", "contratos"):
        s = pd.read_csv(RAW9 / f"sepe_municipios/{var}_municipio_mensual.csv.gz", dtype={"mes": str, "cod_municipio": str})
        s = s[~s.posterior_prereg.astype(str).str.lower().eq("true")]
        s["anio"] = s.mes.str[:4]
        g = s.groupby(["cod_municipio", "anio"])[var].agg(["mean", "count"]).reset_index()
        g = g[g["count"] == 12]
        add(pd.DataFrame({"territorio_codigo": g.cod_municipio, "nivel": "municipio", "periodo_raw": g.anio,
                          "variable": f"sepe_{var}_media_anual", "valor": g["mean"], "metodo_dato": "media de 12 meses (cálculo propio)"}),
            f"data/raw/v9/sepe_municipios/{var}_municipio_mensual.csv.gz")
    # BCE RAI: cuota de nuevos préstamos de vivienda a tipo variable o fijación ≤1 año; Eurostat IPCA alquileres
    r = pd.read_csv(RAW9 / "bce_rai/bce_rai_svlhphh.csv.gz", dtype=str)
    add(pd.DataFrame({"territorio_codigo": r.pais, "nivel": "pais", "periodo_raw": r.periodo, "variable": "bce_cuota_tipo_variable",
                      "valor": pd.to_numeric(r.valor, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/bce_rai/bce_rai_svlhphh.csv.gz")
    h = pd.read_csv(RAW9 / "eurostat_alquiler/prc_hicp_minr_cp041_mensual.csv.gz", dtype=str)
    h = h[h.pais.str.fullmatch(r"[A-Z]{2}")]
    add(pd.DataFrame({"territorio_codigo": h.pais, "nivel": "pais", "periodo_raw": h.periodo, "variable": "hicp_alquiler_indice",
                      "valor": pd.to_numeric(h.indice_2015, errors="coerce"), "metodo_dato": "observado"}).dropna(subset=["valor"]),
        "data/raw/v9/eurostat_alquiler/prc_hicp_minr_cp041_mensual.csv.gz")
    # Censo 2011: viviendas por tipo y provincia (vivienda principal = hogar)
    c11 = pd.read_csv(RAW9 / "ine_censos/censo_t3457.csv.gz", sep=";", dtype=str)
    col = c11.columns[0]
    # CCAA y provincias comparten códigos de 2 dígitos: la tabla lista cada CCAA (01..19, en orden) seguida de sus
    # provincias; una etiqueta es CCAA si su código es el siguiente de la secuencia 01..19
    es_prov, sig = {}, 1
    for e in c11[col].drop_duplicates():
        if e[:2].isdigit() and int(e[:2]) == sig:
            es_prov[e], sig = False, sig + 1
        else:
            es_prov[e] = e[:2].isdigit()
    c11 = c11[c11[col].map(es_prov)]
    add(pd.DataFrame({"territorio_codigo": c11[col].str[:2], "nivel": "provincia", "periodo_raw": c11.Periodo,
                      "variable": "censo2011_viviendas", "desagregacion": "tipo=" + c11["Tipo de vivienda"],
                      "valor": pd.to_numeric(c11.Total.str.replace(".", "", regex=False), errors="coerce"),
                      "metodo_dato": "observado"}).dropna(subset=["valor"]), "data/raw/v9/ine_censos/censo_t3457.csv.gz")
    # Incasòl (no redistribuible; solo si está en disco)
    inc = RAW9 / "incasol/incasol_qww9-bvhh_actual.csv.gz"
    if inc.exists():
        i = pd.read_csv(inc, dtype=str)
        i = i[i.ambit_territorial.str.lower().str.startswith("municipi")]
        i["periodo_iso"] = i.periodo_iso.str.replace("_gener-desembre", "", regex=False)
        i = i[i.periodo_iso.str.fullmatch(r"\d{4}(T[1-4])?")]   # se descartan los acumulados parciales del año
        for var, col in (("incasol_contratos", "habitatges"), ("incasol_renta_media", "renda")):
            add(pd.DataFrame({"territorio_codigo": i.codi_territorial.str.zfill(5), "nivel": "municipio",
                              "periodo_raw": i.periodo_iso, "variable": var, "desagregacion": "tramo=" + i.tram_preus.fillna("Total"),
                              "valor": pd.to_numeric(i[col].str.replace(",", "."), errors="coerce"), "metodo_dato": "observado"}
                             ).dropna(subset=["valor"]), "data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz")
    return partes


def raw_proyecto() -> pd.DataFrame:
    """Fuentes con código INE que ya estaban en data/raw (v2-v3) y que el atlas necesita por sección o municipio."""
    partes = []

    def add(df, origen, prio=2):
        df = df.copy()
        df["origen"], df["prioridad"] = origen, prio
        for c in ("metodo_dato", "desagregacion"):
            if c not in df:
                df[c] = "" if c == "desagregacion" else "observado"
        partes.append(df.dropna(subset=["valor"]))

    # SERPAVI municipal y provincial (AEAT-IRPF, stock de contratos)
    s = pd.read_csv(RAW / "pdf/serpavi_v2_municipios.csv.gz", dtype=str)
    niv = s.nivel.map({"MUN": "municipio", "PROV": "provincia"})
    add(pd.DataFrame({"territorio_codigo": s.codigo, "nivel": niv, "periodo_raw": s.periodo,
                      "variable": "serpavi_" + s.variable + "_" + s.estadistico, "desagregacion": "tipologia=" + s.tipologia,
                      "valor": pd.to_numeric(s.valor, errors="coerce")}), "data/raw/pdf/serpavi_v2_municipios.csv.gz")
    # SERPAVI por sección y distrito (solo medianas y recuentos)
    medidas = {"ALQM2_LV_M": "serpavi_alquiler_m2_mediana", "ALQTBID12_M": "serpavi_alquiler_mes_mediana",
               "BI_ALVHEPCO_T": "serpavi_n_contratos_recuento"}
    for f, nivel in (("v3/serpavi_secciones_nacional_v3.csv.gz", "seccion"), ("v3/serpavi_distritos_nacional_v3.csv.gz", "distrito")):
        d = pd.read_csv(RAW / f, dtype=str, usecols=["periodo", "serie", "valor", "codigo"])
        sufijo = d.serie.str.split("_", n=3).str[3]
        tip = sufijo.str[-2:]
        med = sufijo.str[:-3].map(medidas)
        d = d[med.notna()]
        add(pd.DataFrame({"territorio_codigo": d.codigo, "nivel": nivel, "periodo_raw": d.periodo, "variable": med[med.notna()],
                          "desagregacion": "tipologia=" + tip[med.notna()], "valor": pd.to_numeric(d.valor, errors="coerce")}),
            f"data/raw/{f}")
    # INE, viviendas turísticas por sección y distrito (estadística experimental)
    v = pd.read_csv(RAW / "v3/ine_v3_vut_seccion.csv.gz", dtype=str, usecols=["periodo", "valor", "nivel", "codigo", "medida"])
    add(pd.DataFrame({"territorio_codigo": v.codigo, "nivel": v.nivel, "periodo_raw": v.periodo,
                      "variable": "ine_vut_" + v.medida, "valor": pd.to_numeric(v.valor, errors="coerce")}),
        "data/raw/v3/ine_v3_vut_seccion.csv.gz")
    # INE, Atlas de distribución de renta de los hogares (ADRH) por sección
    g = pd.read_csv(RAW / "v3/ine_v3_gis_seccion.csv.gz", dtype=str)
    ind = {"Renta neta media por persona": "adrh_renta_neta_persona", "Renta neta media por hogar": "adrh_renta_neta_hogar",
           "Índice de Gini": "adrh_gini"}
    g = g[g.servicio.str.contains("Renta") & g.indicador.isin(ind)]
    g["anio"] = g.anio.astype(float).astype(int).astype(str)
    g = g.drop_duplicates(["codigo", "anio", "indicador"])
    add(pd.DataFrame({"territorio_codigo": g.codigo, "nivel": "seccion", "periodo_raw": g.anio, "variable": g.indicador.map(ind),
                      "valor": pd.to_numeric(g.valor, errors="coerce")}), "data/raw/v3/ine_v3_gis_seccion.csv.gz")
    # INE, Censo de Población y Viviendas 2021: indicadores por sección
    c = pd.read_csv(RAW / "v3/ine_v3_censo2021_seccion_indicadores.csv.gz", dtype=str, usecols=["serie", "valor", "codigo"])
    add(pd.DataFrame({"territorio_codigo": c.codigo, "nivel": "seccion", "periodo_raw": "2021",
                      "variable": "censo2021_" + c.serie, "valor": pd.to_numeric(c.valor, errors="coerce")}),
        "data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz")
    # Catastro: unidades urbanas por municipio
    k = pd.read_csv(RAW / "catastro_urbana_municipios.csv.gz", dtype=str)
    add(pd.DataFrame({"territorio_codigo": k.codigo, "nivel": "municipio", "periodo_raw": k.periodo,
                      "variable": "catastro_" + k.unidad, "valor": pd.to_numeric(k.valor, errors="coerce")}),
        "data/raw/catastro_urbana_municipios.csv.gz")
    return partes


def resultados_publicados() -> tuple[list[pd.DataFrame], pd.DataFrame]:
    """Resultados ya publicados (V5 y V8) que las figuras regeneran desde la base: déficit provincial 2021-2025 (A4,
    C4), factor común de precios (M1, C4) y atribución combinada (F5; capa propia de cada fila, con bandas)."""
    partes = []
    a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str})
    for est in ("min", "mediana", "max"):
        partes.append(pd.DataFrame({"territorio_codigo": a4.cod_prov, "nivel": "provincia", "periodo_raw": "2025",
                                    "variable": "v5_deficit_2021_2025", "desagregacion": f"estadistico={est}",
                                    "valor": a4[f"deficit_2021_2025_{est}"], "metodo_dato": "resultado publicado (V5 A4)",
                                    "origen": "output/v5/A4/clasificacion_provincias.csv", "prioridad": 5}))
    f = pd.read_csv(RAIZ / "output/v8/M1/factor_comun.csv")
    partes.append(pd.DataFrame({"territorio_codigo": "00", "nivel": "nacional", "periodo_raw": f.trimestre,
                                "variable": "v8_factor_comun_precios", "desagregacion": "", "valor": f.factor_pca,
                                "metodo_dato": "resultado publicado (V8 M1, primer componente principal)",
                                "origen": "output/v8/M1/factor_comun.csv", "prioridad": 5}))
    atr = pd.read_csv(RAIZ / "output/v8/F5/atribucion_combinada.csv")
    atr.insert(0, "origen", "output/v8/F5/atribucion_combinada.csv")
    return partes, atr


def efectos_v9_tabla() -> pd.DataFrame:
    """V9 (F5): tabla de efectos y asociaciones de los diseños D1-D5 con su capa (output/v9/f3/tabla_capas.csv) y el script
    que la produce. Solo estimaciones agregadas (Incasòl, Registre y los shocks JK no se publican en bruto)."""
    ruta = RAIZ / "output/v9/f3/tabla_capas.csv"
    if not ruta.exists():
        return pd.DataFrame()
    t = pd.read_csv(ruta)
    scripts = {"D1a": "src/v9/d1_zonas.py", "D1b": "src/v9/d1_zonas.py", "D1c": "src/v9/d1_zonas.py", "D2": "src/v9/d2_turisticos.py",
               "D3": "src/v9/d3_valencia.py", "D4": "src/v9/d4_inmigracion.py", "D5": "src/v9/d5_tipos.py"}
    t["script"] = t.diseno.map(scripts)
    cols = ["diseno", "hipotesis", "resultado", "metodo", "beta", "se", "ic95_lo", "ic95_hi", "p", "p_holm", "p_bh", "N",
            "confirmatoria", "capa", "motivo_capa", "script"]
    return t[cols].assign(origen="output/v9/f3/tabla_capas.csv")


def monitor_series() -> list[pd.DataFrame]:
    """Series del monitor (src/v10/monitor.py): último tramo de series abiertas, variable `monitor_<id>`."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("monitor", Path(__file__).with_name("monitor.py"))
    mon = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mon)
    partes = []
    for ident in mon.SERIES:
        ruta = RAW / "v10" / "monitor" / f"{ident}.csv"
        if not ruta.exists():
            continue
        d = pd.read_csv(ruta, dtype={"periodo": str})
        terr, nivel = ("10", "ccaa") if ident == "fianzas_gva" else ("00", "nacional")
        partes.append(pd.DataFrame({"territorio_codigo": terr, "nivel": nivel, "periodo_raw": d.periodo,
                                    "variable": f"monitor_{ident}", "desagregacion": "", "valor": d.valor,
                                    "metodo_dato": "observado (monitor)", "origen": f"data/raw/v10/monitor/{ident}.csv",
                                    "prioridad": 6}))
        _, _, _, unidad, capa, fuente = mon.SERIES[ident]
        META_V9[f"monitor_{ident}"] = (unidad, fuente, capa, "reutilización con cita del organismo", True)
    return partes


def zonas_trimestrales() -> tuple[pd.DataFrame, pd.DataFrame]:
    z = pd.read_csv(RAW9 / "regulacion/zonas_tensionadas_v9.csv", dtype=str)
    filas = []
    for t in pd.period_range("2024Q1", "2026Q3", freq="Q"):
        fin = t.end_time.strftime("%Y-%m-%d")
        vig = z[(z.fecha_efecto <= fin) & (z.fecha_fin_prevista > fin)]
        for cod in sorted(set(vig.cod_ine_municipio)):
            filas.append({"territorio_codigo": cod, "nivel": "municipio", "periodo_raw": f"{t.year}T{t.quarter}",
                          "variable": "zt_vigente", "valor": 1.0, "metodo_dato": "evento (resolución BOE)",
                          "desagregacion": "", "origen": "data/raw/v9/regulacion/zonas_tensionadas_v9.csv", "prioridad": 4})
    return pd.DataFrame(filas), z


# ----------------------------------------------------------------------------------------------- metadatos de filas
META_V9 = {  # variable -> (unidad, fuente, capa, licencia, redistribuible)
    "pob_censo_anual": ("personas", "INE, Censo anual de población (tablas por provincia)", "C4", "INE: reutilización con cita (Ley 37/2007)", True),
    "ipva_indice": ("índice 2015=100", "INE, Índice de Precios de Vivienda en Alquiler (59004, 59005, 59061)", "C4", "INE: reutilización con cita", True),
    "ipva_var_anual": ("%", "INE, IPVA", "C4", "INE: reutilización con cita", True),
    "vut_registro_gva": ("viviendas", "GVA, Registro de Turismo de la Comunitat Valenciana (cortes)", "C4", "CC BY 4.0", True),
    "vut_registro_gva_reconstruido": ("viviendas", "GVA, registro (altas y bajas fechadas; reconstrucción propia)", "C4", "CC BY 4.0", True),
    "emal_n_fianzas": ("contratos", "Gobierno Vasco, EMAL (fianzas)", "C4", "CC BY 4.0", True),
    "emal_renta_mensual_eur": ("€/mes", "Gobierno Vasco, EMAL", "C4", "CC BY 4.0", True),
    "emal_renta_eur_m2_construido": ("€/m²/mes", "Gobierno Vasco, EMAL", "C4", "CC BY 4.0", True),
    "bce_hip_tipo_nuevas": ("% anual", "BCE, MIR (nuevas operaciones de vivienda)", "C4", "BCE: reutilización con cita", True),
    "bce_hip_volumen_nuevas": ("millones de euros", "BCE, MIR", "C4", "BCE: reutilización con cita", True),
    "eurostat_plataformas_noches": ("noches", "Eurostat, tour_ce_oan3 (plataformas colaborativas)", "C4", "CC BY 4.0 (Eurostat)", True),
    "incasol_contratos": ("contratos", "Incasòl, fianzas (Socrata qww9-bvhh)", "C4", "Términos de uso (no CC BY)", False),
    "incasol_renta_media": ("€/mes", "Incasòl, fianzas", "C4", "Términos de uso (no CC BY)", False),
    "ine_vut_vivienda_turistica": ("viviendas", "INE, Medición del número de viviendas turísticas (experimental)", "C4", "INE: reutilización con cita", True),
    "ine_vut_plazas": ("plazas", "INE, viviendas turísticas (experimental)", "C4", "INE: reutilización con cita", True),
    "ine_vut_porcentaje_vivienda_turistica": ("% de viviendas", "INE, viviendas turísticas (experimental)", "C4", "INE: reutilización con cita", True),
    "adrh_renta_neta_persona": ("€/año", "INE, Atlas de distribución de renta de los hogares (ADRH)", "C4", "INE: reutilización con cita", True),
    "adrh_renta_neta_hogar": ("€/año", "INE, ADRH", "C4", "INE: reutilización con cita", True),
    "adrh_gini": ("índice", "INE, ADRH", "C4", "INE: reutilización con cita", True),
    "catastro_unidades_urbanas_residenciales": ("inmuebles", "Dirección General del Catastro, estadísticas catastrales (urbana)", "C4", "Catastro: reutilización con cita", True),
    "catastro_unidades_urbanas_total": ("inmuebles", "Dirección General del Catastro, estadísticas catastrales (urbana)", "C4", "Catastro: reutilización con cita", True),
    "v5_deficit_2021_2025": ("viviendas", "Resultado publicado V5 (A4): déficit 2021-2025 por provincia (rango de variantes)", "C4", "elaboración propia (CC BY 4.0)", True),
    "v8_factor_comun_precios": ("unidades del componente (estandarizado)", "Resultado publicado V8 (M1): factor común de las fuentes de precio", "C4", "elaboración propia (CC BY 4.0)", True),
    "idescat_hut_n": ("viviendas", "IDESCAT, Estadística de establecimientos turísticos (turall): HUT", "C4", "IDESCAT: reutilización con cita", True),
    "idescat_hut_plazas": ("plazas", "IDESCAT, turall: HUT", "C4", "IDESCAT: reutilización con cita", True),
    "idescat_apartamentos_n": ("establecimientos", "IDESCAT, turall: apartamentos turísticos", "C4", "IDESCAT: reutilización con cita", True),
    "idescat_apartamentos_plazas": ("plazas", "IDESCAT, turall: apartamentos turísticos", "C4", "IDESCAT: reutilización con cita", True),
    "padron_pob_nacionalidad": ("personas", "INE, Padrón continuo por nacionalidad (tablas jaxiT3 por provincia; suma de municipios)", "C4", "INE: reutilización con cita", True),
    "em_saldo_interprovincial": ("personas", "INE, Estadística de Migraciones (24385)", "C4", "INE: reutilización con cita", True),
    "em_inmigracion_extranjero": ("personas", "INE, Estadística de Migraciones (24323)", "C4", "INE: reutilización con cita", True),
    "em_emigracion_extranjero": ("personas", "INE, Estadística de Migraciones (24326)", "C4", "INE: reutilización con cita", True),
    "emcr_saldo": ("personas", "INE, Estadística de Migraciones y Cambios de Residencia (69764)", "C4", "INE: reutilización con cita", True),
    "sepe_paro_registrado_media_anual": ("personas", "SEPE, paro registrado por municipio (media anual propia)", "C4", "SEPE: reutilización con cita", True),
    "sepe_contratos_media_anual": ("contratos al mes", "SEPE, contratos registrados por municipio (media anual propia)", "C4", "SEPE: reutilización con cita", True),
    "bce_cuota_tipo_variable": ("% de nuevos préstamos", "BCE, RAI (SVLHPHH): nuevos préstamos de vivienda a tipo variable o fijación ≤1 año", "C4", "BCE: reutilización con cita", True),
    "hicp_alquiler_indice": ("índice 2015=100", "Eurostat, prc_hicp_minr (CP041, alquileres efectivos)", "C4", "Eurostat: reutilización con cita", True),
    "censo2011_viviendas": ("viviendas", "INE, Censo de Población y Viviendas 2011 (3457)", "C4", "INE: reutilización con cita", True),
    "zt_vigente": ("0/1", "BOE, resoluciones de la Secretaría de Estado de Vivienda (zonas tensionadas)", "C4", "BOE: reutilización con cita", True),
}


UNIDADES = {  # variables cuyo diccionario de origen no da unidad (comprobado en el diccionario y en el fichero raw)
    "costes": "índice 2021=100", "hpi_eurostat": "índice 2015=100", "iniciadas": "viviendas",
    "iniciadas_anual_tabla": "viviendas", "terminadas_anual_tabla": "viviendas", "ipc_alquiler_indice": "índice 2021=100",
    "ocupados_epa": "miles de personas", "permisos": "viviendas (visados)", "prod_constr": "índice 2021=100",
    "renta_hog": "millones de euros", "iab_disponibilidad_365_media": "días", "iab_resenas_ultimos_12m": "reseñas",
}


def periodos(raw: list[str]) -> pd.DataFrame:
    filas = []
    for r in raw:
        per, frec = periodo_y_frecuencia(r)
        ini, fin = _inicio_fin(per, frec)
        if not fin:
            raise ValueError(f"periodo no reconocido: {r}")
        filas.append({"periodo_raw": r, "periodo": per, "frecuencia": frec, "ini": ini, "fin": fin})
    return pd.DataFrame(filas)


def tabla_variables(vars_: list[str], meta: dict, lic: dict) -> pd.DataFrame:
    tabla = {}
    for v in vars_:
        if v.startswith("serpavi_") and not meta.get(v, {}).get("unidad"):
            tabla[v] = ("€/m²/mes" if "m2" in v else ("€/mes" if "mes" in v else "contratos"),
                        "MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados)", "C4",
                        "MIVAU: reutilización con cita", True)
        elif v.startswith("censo2021_"):
            tabla[v] = ("viviendas u hogares" if re.match(r"censo2021_t(1|18|19|20|21|22)_", v) else "%",
                        "INE, Censo de Población y Viviendas 2021 (indicadores por sección)", "C4", "INE: reutilización con cita", True)
        elif v.startswith("iab_"):
            tabla[v] = ("anuncios" if "anuncios" in v or v.startswith("iab_n") else "", "Inside Airbnb (no oficial)", "C4", "CC BY 4.0", True)
        elif v in META_V9:
            tabla[v] = META_V9[v]
        elif v in META_V11:
            tabla[v] = META_V11[v]
        else:
            m = meta.get(v, {})
            fuente = m.get("fuente", "") if m.get("fuente") and m.get("fuente") not in ("idem", "Derivada", "derivada") else (FUENTES_DOCUMENTADAS.get(v) or m.get("fuente", ""))
            capa = m.get("capa") or "C4"
            redis = (not NO_REDISTRIBUIBLE.search(v) and not FUENTE_NO_REDISTRIBUIBLE.search(fuente)
                     and bool(FUENTE_PERMITIDA.search(fuente) or v in FUENTES_DOCUMENTADAS))
            for f in re.findall(r"[\w./-]+\.(?:csv|xlsx?|json|px)", fuente, re.I):
                if lic.get(Path(f).name.lower(), "permitida") != "permitida":
                    redis = False
            licencia = "según organismo (docs/v8_1/inventario_licencias.csv)" if redis else "sin licencia abierta clara (no se redistribuye)"
            tabla[v] = (m.get("unidad", ""), fuente or "ver diccionario del panel de origen", capa, licencia, redis)
    t = pd.DataFrame.from_dict(tabla, orient="index", columns=["unidad", "fuente", "capa", "licencia", "redistribuible"])
    vacia = t.unidad.fillna("") == ""
    t.loc[vacia, "unidad"] = [UNIDADES.get(v, "personas" if v.startswith("pob_") else "") for v in t.index[vacia]]
    # C1 vale solo en el nivel territorial que documenta el diccionario que la asigna (revisión V10, R3): V8 → nacional,
    # V7 → CCAA; cualquier otro nivel (o C1 sin diccionario que la documente) baja a C4 en la consulta de montaje.
    t["nivel_c1"] = [{"docs/v8/diccionario.md": "nacional", "docs/v7/diccionario.md": "ccaa"}.get(meta.get(v, {}).get("dic_capa", ""), "")
                     if t.at[v, "capa"] == "C1" else "" for v in t.index]
    t["definicion"] = [meta.get(v, {}).get("definicion", "") or (META_V9[v][1] if v in META_V9 else META_V11[v][1] if v in META_V11 else "")
                       for v in t.index]
    return t.rename_axis("variable").reset_index()


def edicion_origen() -> dict:
    out = {}
    for m in [*RAW9.glob("*/_manifest.csv"), *RAW11.glob("*/_manifest.csv")]:
        with open(m, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r["fichero"]] = f"{r['edicion']} (descarga {r['fecha_descarga']})"
    for f in PROC.rglob("*.csv"):
        out[str(f.relative_to(RAIZ))] = "panel procesado del proyecto (data/processed, construcción v1-v8; descargas hasta 2026-10-10)"
    out["data/raw/v9/regulacion/zonas_tensionadas_v9.csv"] = "BOE hasta 2026-10-14"
    out["output/v5/A4/clasificacion_provincias.csv"] = "V5 (publicado; cifras_clave A4)"
    out["output/v8/M1/factor_comun.csv"] = "V8 (congelado; M1)"
    for f in (RAW / "v10" / "monitor").glob("*.csv"):
        out[str(f.relative_to(RAIZ))] = "monitor V10 (fecha de descarga en output/v10/monitor/monitor.json)"
    return out


def sellado_v6() -> set[str]:
    d = pd.read_csv(PROC / "v7/panel_prov_a_v7.csv", dtype={"cod_prov": str})
    return set(d.loc[d.prov_sellada_v6 == True, "cod_prov"].str.zfill(2))  # noqa: E712


# ----------------------------------------------------------------------------------------------- construcción
def construir() -> dict:
    """Ensamblado en DuckDB (en disco) para no cargar ~11 M filas con texto en pandas."""
    import duckdb
    BASE.mkdir(parents=True, exist_ok=True)
    PUB.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    meta, lic = metadatos_variables(), estado_licencias()
    zt, zonas = zonas_trimestrales()
    db = BASE / "vivienda.duckdb"
    for f in (db, BASE / "vivienda.duckdb.wal"):
        if f.exists():
            f.unlink()
    con = duckdb.connect(str(db))
    con.execute("SET preserve_insertion_order=false")
    con.execute("""CREATE TABLE bruto (territorio_codigo VARCHAR, nivel VARCHAR, periodo_raw VARCHAR, variable VARCHAR,
                   desagregacion VARCHAR, valor DOUBLE, metodo_dato VARCHAR, origen VARCHAR, prioridad INTEGER)""")
    cols = ["territorio_codigo", "nivel", "periodo_raw", "variable", "desagregacion", "valor", "metodo_dato", "origen", "prioridad"]

    def insertar(partes):
        for x in partes:
            x = x.copy()
            for c in ("desagregacion", "metodo_dato"):
                if c not in x:
                    x[c] = None
            x = x[cols]
            for c in cols:
                if c not in ("valor", "prioridad"):
                    x[c] = x[c].astype(object).where(x[c].notna(), None).astype(str).where(x[c].notna(), None)
            x["valor"] = pd.to_numeric(x.valor, errors="coerce")
            x = x[x.valor.notna() & np.isfinite(x.valor)]
            con.register("parte", x)
            con.execute("INSERT INTO bruto SELECT * FROM parte")
            con.unregister("parte")
    insertar(procesados())
    insertar(raw_proyecto())
    insertar(v9())
    insertar(base_v11.partes())   # V11-DATOS: migración, MNP, ECP, Catastro, afiliación, turismo (src/v11/base_v11.py)
    insertar(base_v12.partes())   # V12: contabilidad demográfica, hogares, presión, titularidad (src/v12/base_v12.py)
    insertar([zt])
    res_partes, atribucion = resultados_publicados()
    insertar(res_partes)
    insertar(monitor_series())
    con.execute("UPDATE bruto SET desagregacion = coalesce(desagregacion, ''), "
                "metodo_dato = CASE WHEN metodo_dato IS NULL OR metodo_dato IN ('', 'nan', '<NA>') THEN 'observado' ELSE metodo_dato END")
    # periodos y metadatos de variables (tablas pequeñas)
    pf = periodos([r[0] for r in con.execute("SELECT DISTINCT periodo_raw FROM bruto").fetchall()])
    con.register("pf", pf)
    vt_meta = tabla_variables([r[0] for r in con.execute("SELECT DISTINCT variable FROM bruto").fetchall()], meta, lic)
    con.register("vmeta", vt_meta)
    ed = pd.DataFrame(list(edicion_origen().items()), columns=["origen", "edicion"])
    con.register("ed", ed)
    sell = pd.DataFrame({"territorio_codigo": sorted(sellado_v6())})
    con.register("sell", sell)
    con.execute("""CREATE TABLE b2 AS SELECT b.territorio_codigo, b.nivel, pf.periodo, pf.frecuencia, b.variable,
                   b.desagregacion, b.valor, b.metodo_dato, b.origen, b.prioridad, pf.ini, pf.fin
                   FROM bruto b JOIN pf USING (periodo_raw)""")
    con.execute("DROP TABLE bruto")
    clave = ", ".join(CLAVE)
    # una misma fuente no puede traer dos filas con la misma clave: la elección sería arbitraria (no determinista)
    dup_origen = con.execute(f"""SELECT origen, count(*) n FROM (SELECT origen, {clave} FROM b2 GROUP BY origen, {clave}
        HAVING count(*) > 1 AND max(valor) <> min(valor)) GROUP BY origen""").fetchall()
    if dup_origen:
        raise ValueError(f"claves duplicadas con valores distintos dentro de una misma fuente: {dup_origen}")
    discrepancias = con.execute(f"""SELECT count(*) FROM (SELECT {clave} FROM b2 GROUP BY {clave}
        HAVING count(*) > 1 AND (max(valor) - min(valor)) / greatest(max(abs(valor)), 1e-12) > 1e-6)""").fetchone()[0]
    # un panel por serie (el de mayor prioridad) y una fila por clave
    con.execute(f"""CREATE TABLE hechos AS
        WITH s AS (SELECT *, max(prioridad) OVER (PARTITION BY variable, nivel, territorio_codigo, desagregacion) AS pmax FROM b2),
             u AS (SELECT *, row_number() OVER (PARTITION BY {clave} ORDER BY prioridad DESC, origen) AS rn FROM s WHERE prioridad = pmax)
        SELECT u.territorio_codigo, u.nivel, u.periodo, u.frecuencia, u.variable, u.desagregacion, u.valor,
               vm.unidad, vm.fuente, coalesce(ed.edicion, 'proyecto') AS edicion, u.fin AS fecha_dato, CASE WHEN vm.capa = 'C1' AND u.nivel <> vm.nivel_c1 THEN 'C4' ELSE vm.capa END AS capa, vm.licencia,
               vm.redistribuible, u.metodo_dato, u.origen, u.fin >= '2026-07-01' AS posterior_prereg,
               (u.nivel IN ('provincia', 'municipio', 'distrito', 'seccion')   -- V15: también filas sub-provinciales (docs/v15/contaminacion_v6.md)
                AND substr(u.territorio_codigo, 1, 2) IN (SELECT territorio_codigo FROM sell)) AS muestra_sellada_v6
        FROM u JOIN vmeta vm USING (variable) LEFT JOIN ed USING (origen) WHERE rn = 1
        ORDER BY {clave}""")
    con.execute("DROP TABLE b2")
    # territorios (con secciones y distritos históricos presentes en los datos)
    terr = territorios()
    terr["vigente_2025"] = True
    faltan = con.execute("SELECT DISTINCT territorio_codigo, nivel FROM hechos WHERE nivel IN ('seccion', 'distrito')").df()
    faltan = faltan.merge(terr[["territorio_codigo", "nivel"]], how="left", indicator=True)
    faltan = faltan[faltan._merge == "left_only"].drop(columns="_merge")
    ccaa_mun = terr[terr.nivel == "municipio"].set_index("territorio_codigo").cod_ccaa
    if len(faltan):
        hist = pd.DataFrame({"territorio_codigo": faltan.territorio_codigo, "nivel": faltan.nivel,
                             "nombre": faltan.nivel + " " + faltan.territorio_codigo + " (no vigente en 2025)",
                             "padre_codigo": [c[:7] if n == "seccion" else c[:5] for c, n in zip(faltan.territorio_codigo, faltan.nivel)],
                             "padre_nivel": ["distrito" if n == "seccion" else "municipio" for n in faltan.nivel],
                             "cod_ccaa": faltan.territorio_codigo.str[:5].map(ccaa_mun),
                             "cod_provincia": faltan.territorio_codigo.str[:2], "fuente": "INE (código histórico)",
                             "vigente_2025": False})
        terr = pd.concat([terr, hist], ignore_index=True)
        pares = set(zip(terr.territorio_codigo, terr.nivel))
        dpad = sorted({c[:7] for c, n in zip(hist.territorio_codigo, hist.nivel) if n == "seccion" and (c[:7], "distrito") not in pares})
        if dpad:
            terr = pd.concat([terr, pd.DataFrame({"territorio_codigo": dpad, "nivel": "distrito",
                              "nombre": [f"distrito {d} (no vigente en 2025)" for d in dpad], "padre_codigo": [d[:5] for d in dpad],
                              "padre_nivel": "municipio", "cod_ccaa": [ccaa_mun.get(d[:5], "") for d in dpad],
                              "cod_provincia": [d[:2] for d in dpad], "fuente": "INE (código histórico)",
                              "vigente_2025": False})], ignore_index=True)
    # municipios históricos (fusionados o suprimidos antes de la relación de 2026) presentes en los datos o como padres
    munis = set(con.execute("SELECT DISTINCT territorio_codigo FROM hechos WHERE nivel = 'municipio'").df().territorio_codigo)
    munis |= set(terr.loc[terr.padre_nivel == "municipio", "padre_codigo"])
    viejos = sorted(m for m in munis - set(terr.loc[terr.nivel == "municipio", "territorio_codigo"]) if re.fullmatch(r"\d{5}", m))
    if viejos:
        ccaa_prov = terr[terr.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa
        terr = pd.concat([terr, pd.DataFrame({"territorio_codigo": viejos, "nivel": "municipio",
                          "nombre": [f"municipio {m} (no vigente en 2026)" for m in viejos], "padre_codigo": [m[:2] for m in viejos],
                          "padre_nivel": "provincia", "cod_ccaa": [ccaa_prov.get(m[:2], "") for m in viejos],
                          "cod_provincia": [m[:2] for m in viejos], "fuente": "INE (código histórico)", "vigente_2025": False})],
                         ignore_index=True)
    terr["cod_ccaa"] = terr.cod_ccaa.fillna("")
    orden = {"nacional": 0, "ccaa": 1, "provincia": 2, "municipio": 3, "distrito": 4, "barrio": 5, "seccion": 6}
    terr = terr.sort_values(["nivel", "territorio_codigo"], key=lambda c: c.map(orden) if c.name == "nivel" else c).reset_index(drop=True)
    # variables
    vt = con.execute("""SELECT variable, any_value(unidad) unidad, any_value(fuente) fuente, string_agg(DISTINCT capa, '/' ORDER BY capa) capa,
        any_value(licencia) licencia, bool_and(redistribuible) redistribuible, string_agg(DISTINCT nivel, ',' ORDER BY nivel) niveles,
        min(periodo) primer_periodo, max(periodo) ultimo_periodo, count(*) n_filas FROM hechos GROUP BY variable ORDER BY variable""").df()
    vt = vt.merge(vt_meta[["variable", "definicion"]], on="variable", how="left")
    cifras = pd.read_csv(RAIZ / "publicacion/cifras_clave.csv", dtype=str, keep_default_na=False)
    efectos_v9 = efectos_v9_tabla()
    # escritura
    con.execute("SET preserve_insertion_order=true")   # escritura determinista (mismo orden de filas y de grupos)
    con.execute(f"COPY (SELECT * FROM hechos ORDER BY {clave}) TO '{BASE / 'hechos.parquet'}' (FORMAT parquet, COMPRESSION zstd)")
    con.execute(f"COPY (SELECT * FROM hechos WHERE redistribuible ORDER BY {clave}) TO '{PUB / 'hechos.parquet'}' (FORMAT parquet, COMPRESSION zstd)")
    opts = {"index": False, "compression": "zstd"}
    for nombre, df, pub in (("territorios", terr, terr), ("variables", vt, vt[vt.redistribuible]),
                            ("cifras_clave", cifras, cifras), ("regulacion_zonas", zonas, zonas),
                            ("v8_atribucion", atribucion, atribucion), ("v9_efectos", efectos_v9, efectos_v9)):
        df.to_parquet(BASE / f"{nombre}.parquet", **opts)
        pub.to_parquet(PUB / f"{nombre}.parquet", **opts)
        con.register("tmp", df)
        con.execute(f"CREATE TABLE {nombre} AS SELECT * FROM tmp")
        con.unregister("tmp")
    con.execute("CREATE VIEW hechos_publica AS SELECT * FROM hechos WHERE redistribuible")
    n, npub, npost = con.execute("SELECT count(*), sum(redistribuible::INT), sum(posterior_prereg::INT) FROM hechos").fetchone()
    niv = con.execute("SELECT nivel, count(*) FROM hechos WHERE redistribuible GROUP BY nivel ORDER BY nivel").fetchall()
    con.execute("CHECKPOINT")
    con.close()
    resumen = {"filas": int(n), "filas_publica": int(npub), "variables": len(vt), "territorios": len(terr),
               "discrepancias_entre_paneles": int(discrepancias), "filas_posterior_prereg": int(npost)}
    # el diccionario versionado solo describe la capa pública: no depende de qué datos de terceros estén en disco
    escribir_diccionario(vt[vt.redistribuible], dict(niv),
                         {k: v for k, v in resumen.items() if k not in ("filas", "variables", "discrepancias_entre_paneles")}
                         | {"variables_publicas": int(vt.redistribuible.sum())})
    return resumen


def escribir_diccionario(vt: pd.DataFrame, niv: dict, resumen: dict) -> None:
    lin = ["# Diccionario de la base única (V10)", "",
           "Generado por `src/v10/base.py` (`make base`); no editar a mano.", "",
           "## Tablas", "",
           "| tabla | contenido |", "|---|---|",
           "| hechos | tabla larga: una fila por territorio, periodo, variable y desagregación |",
           "| territorios | dimensión territorial con jerarquía (padre_codigo, padre_nivel) |",
           "| variables | definición, unidad, capa, fuente, licencia y cobertura de cada variable |",
           "| cifras_clave | copia tipada de publicacion/cifras_clave.csv |",
           "| regulacion_zonas | declaraciones de zona tensionada (data/raw/v9/regulacion) |",
           "| hechos_publica (vista) | filas redistribuibles; es lo único que se publica en data/base/publica y en la web |", "",
           "## Columnas de `hechos`", "",
           "| columna | definición |", "|---|---|",
           "| territorio_codigo | código INE (nacional 00; CCAA 2; provincia 2; municipio 5; distrito 7; barrio de València 9 = municipio + distrito + barrio; sección 10). Excepciones: `pais` (ISO-2) y `nuts3` (Eurostat) |",
           "| nivel | nacional, ccaa, provincia, municipio, distrito, barrio, seccion, pais, nuts3 |",
           "| periodo | AAAA (anual), AAAATn (trimestral), AAAA-MM (mensual), AAAASn (semestral), AAAA-MM-DD (corte) |",
           "| frecuencia | A, T, M, S, D |",
           "| variable | nombre de la variable (tabla `variables`) |",
           "| desagregacion | dimensión adicional `clave=valor` (nacionalidad, antigüedad del contrato, fijación…); vacía si no hay |",
           "| valor | valor numérico |",
           "| unidad, fuente, capa, licencia, redistribuible | de la tabla `variables` |",
           "| edicion | edición o fecha de descarga del fichero de origen |",
           "| fecha_dato | último día del periodo al que se refiere el dato |",
           "| metodo_dato | observado, interpolado, agregado, reconstruido… (banderas `_metodo` de los paneles) |",
           "| origen | fichero de data/processed o data/raw/v9 del que sale la fila |",
           "| posterior_prereg | True si el periodo empieza el 2026-07-01 o después (evaluate_v7/evaluate_v8): se muestra, pero no entra en cálculos |",
           "| muestra_sellada_v6 | True en las provincias del sellado transversal de v6 y en sus municipios, distritos y secciones (V15; solo a través de src/holdout.py) |", "",
           "## Resumen", "",
           *[f"- {k}: {v}" for k, v in resumen.items()],
           "- filas públicas por nivel: " + ", ".join(f"{k} {v}" for k, v in niv.items()), "",
           "Las discrepancias entre paneles son claves presentes en varios ficheros procesados con valores distintos; se "
           "conserva el panel más reciente (v8 > v7 > v1), que es el que usan las publicaciones vigentes.", "",
           "## Variables", "",
           "| variable | definición | unidad | capa | fuente | redistribuible | niveles | periodo |", "|---|---|---|---|---|---|---|---|"]
    for r in vt.itertuples():
        d = str(r.definicion).replace("|", "/")[:160]
        f = str(r.fuente).replace("|", "/")[:120]
        lin.append(f"| `{r.variable}` | {d} | {r.unidad} | {r.capa} | {f} | {'sí' if r.redistribuible else 'no'} | "
                   f"{r.niveles} | {r.primer_periodo}–{r.ultimo_periodo} |")
    sys.path.insert(0, str(RAIZ))
    from src.v14 import registradores_origen as RO   # V14.3: licencia por tabla (ODbL de los datos abiertos de Registradores)
    (DOCS / "diccionario_base.md").write_text("\n".join(lin) + "\n\n" + RO.seccion_diccionario(), encoding="utf-8")


if __name__ == "__main__":
    import json
    print(json.dumps(construir(), ensure_ascii=False, indent=1))
    sys.exit(0)
