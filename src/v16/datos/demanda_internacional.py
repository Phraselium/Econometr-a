"""V16-F1 · Normalización de la familia demanda_internacional al formato largo de data/base/hechos.parquet.

Determinista (SEED=20261010, sin aleatoriedad) y sin red. Lee solo data/raw/v16/demanda_internacional/ y data/base/publica/territorios.parquet.
Salidas:
- data/processed/v16/demanda_internacional.parquet (solo redistribuible = sí);
- data/processed/v16/demanda_internacional_terceros.parquet (EA-MPD, redistribuible = False; solo si el libro existe en disco; NO se versiona);
- data/processed/v16/demanda_internacional_resultado.json y docs/v16/fuentes/demanda_internacional_variables.csv.
capa = C4 (dato bruto; la capa se decide en la fase 2). posterior_prereg = False (el corte de V16 no está fijado).
"""
from __future__ import annotations

import csv
import gzip
import json
import sys
from pathlib import Path

import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
ENT = RAIZ / "data" / "raw" / "v16" / "demanda_internacional"
SAL = RAIZ / "data" / "processed" / "v16"
DICC = RAIZ / "docs" / "v16" / "fuentes" / "demanda_internacional_variables.csv"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg", "muestra_sellada_v6"]

# Tabla de correspondencia versionada ISO-3 (OCDE) -> ISO-2 (clave de país del proyecto). Solo coincidencias únicas.
ISO3_ISO2 = {"AUS": "AU", "AUT": "AT", "BEL": "BE", "CAN": "CA", "CHE": "CH", "CHL": "CL", "COL": "CO", "CRI": "CR", "CZE": "CZ",
             "DEU": "DE", "DNK": "DK", "ESP": "ES", "EST": "EE", "FIN": "FI", "FRA": "FR", "GBR": "GB", "GRC": "GR", "HUN": "HU",
             "IRL": "IE", "ISL": "IS", "ISR": "IL", "ITA": "IT", "JPN": "JP", "KOR": "KR", "LTU": "LT", "LUX": "LU", "LVA": "LV",
             "MEX": "MX", "NLD": "NL", "NOR": "NO", "NZL": "NZ", "POL": "PL", "PRT": "PT", "SVK": "SK", "SVN": "SI", "SWE": "SE",
             "TUR": "TR", "USA": "US"}
# Eurostat usa EL y UK; el resto de países coincide con ISO-2. Agregados: EA -> zona_euro; el resto -> nivel «agregado_ue».
EUROSTAT_PAIS = {"EL": "GR", "UK": "GB"}
EUROSTAT_AGREGADOS = {"EA18", "EA19", "EA20", "EA21", "EU", "EU27_2007", "EU27_2020", "EU28"}

BDE_VARS = {  # serie -> (variable, descripcion, unidad)
    "DN_1TI2T0002": ("bde_tedr_vivienda_total_be1904", "TEDR nuevas operaciones crédito vivienda, tipo medio ponderado (be1904)", "porcentaje anual (TEDR)"),
    "DN_1TI2T0003": ("bde_tedr_vivienda_fij_hasta_1a", "TEDR vivienda, periodo inicial de fijación hasta 1 año", "porcentaje anual (TEDR)"),
    "DN_1TI2T0004": ("bde_tedr_vivienda_fij_1a_5a", "TEDR vivienda, fijación inicial de más de 1 año y hasta 5", "porcentaje anual (TEDR)"),
    "DN_1TI2T0005": ("bde_tedr_vivienda_fij_5a_10a", "TEDR vivienda, fijación inicial de más de 5 años y hasta 10", "porcentaje anual (TEDR)"),
    "DN_1TI2T0006": ("bde_tedr_vivienda_fij_mas_10a", "TEDR vivienda, fijación inicial de más de 10 años", "porcentaje anual (TEDR)"),
    "DN_1TI2T0135": ("bde_tedr_vivienda_total_be1903", "TEDR vivienda, total (be1903)", "porcentaje anual (TEDR)"),
    "DN_1TI2T0136": ("bde_tedr_vivienda_renegociados", "TEDR vivienda, operaciones renegociadas", "porcentaje anual (TEDR)"),
    "DN_1TI2T0137": ("bde_tedr_vivienda_excl_renegociaciones", "TEDR vivienda, excluidas renegociaciones", "porcentaje anual (TEDR)"),
    "DN_1TI2TIE42": ("bde_importe_vivienda_total_be1912", "Importe estimado nuevas operaciones vivienda, total (be1912)", "millones de euros"),
    "DN_1TI2TIE43": ("bde_importe_vivienda_fij_hasta_1a", "Importe estimado vivienda, fijación inicial hasta 1 año", "millones de euros"),
    "DN_1TI2TIE44": ("bde_importe_vivienda_fij_1a_5a", "Importe estimado vivienda, fijación inicial de más de 1 año y hasta 5", "millones de euros"),
    "DN_1TI2TIE45": ("bde_importe_vivienda_fij_5a_10a", "Importe estimado vivienda, fijación inicial de más de 5 años y hasta 10", "millones de euros"),
    "DN_1TI2TIE46": ("bde_importe_vivienda_fij_mas_10a", "Importe estimado vivienda, fijación inicial de más de 10 años", "millones de euros"),
    "DN_1TI2TIE96": ("bde_importe_vivienda_total_be1911", "Importe estimado vivienda, total (be1911)", "millones de euros"),
    "DN_1TI2TIE97": ("bde_importe_vivienda_renegociados", "Importe estimado vivienda, renegociados", "millones de euros"),
    "DN_1TI2TIE98": ("bde_importe_vivienda_excl_renegociaciones", "Importe estimado vivienda, excluidas renegociaciones", "millones de euros"),
}
JK_UNIDAD = "unidad no declarada en el fichero JK (choque estandarizado de política monetaria)"
OECD_UNIDAD = {"IX": "índice 2015=100", "PT_AVG_L_TERM": "porcentaje respecto a la media de largo plazo"}
OECD_DESC = {"HPI": "precio nominal de la vivienda", "HPI_RPI": "ratio precio/alquiler", "HPI_RPI_AVG": "ratio precio/alquiler vs media largo plazo",
             "HPI_YDH": "ratio precio/renta disponible por hogar", "HPI_YDH_AVG": "ratio precio/renta vs media largo plazo",
             "RHP": "precio real de la vivienda", "RPI": "índice de alquileres"}


def manifiesto() -> dict:
    m = {}
    with open(ENT / "_manifest.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            m[r["fichero"]] = r
    return m


def fin_periodo(p: pd.Series, freq: str) -> pd.Series:
    if freq == "M":
        return (pd.PeriodIndex(p, freq="M").to_timestamp(how="end")).strftime("%Y-%m-%d")
    if freq == "T":
        return (pd.PeriodIndex(p.str.replace("T", "Q"), freq="Q").to_timestamp(how="end")).strftime("%Y-%m-%d")
    if freq == "A":
        return p.str[:4] + "-12-31"
    return p


def construir(df: pd.DataFrame, rel: str, man: dict, redistribuible: bool | None = None) -> pd.DataFrame:
    r = man[rel]
    df = df.copy()
    df["fuente"] = r["fuente"]
    df["edicion"] = r["edicion"] + " (descarga " + r["fecha_descarga"] + ")"
    df["licencia"] = r["licencia"]
    df["redistribuible"] = (r["redistribuible"].strip().lower() == "sí") if redistribuible is None else redistribuible
    df["origen"] = rel
    df["capa"] = "C4"
    df["posterior_prereg"] = False
    if "metodo_dato" not in df:
        df["metodo_dato"] = "observado"
    if "desagregacion" not in df:
        df["desagregacion"] = ""
    return df


def sellada(df: pd.DataFrame) -> pd.Series:
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout  # solo devuelve la lista de códigos; no abre nada sellado
    prov = set(map(str, holdout.provincias_selladas_v6()))
    prov = {p.zfill(2) for p in prov}
    return df.nivel.isin(["provincia", "municipio", "distrito", "seccion"]) & df.territorio_codigo.str[:2].isin(prov)


def jk(man: dict) -> list[pd.DataFrame]:
    out = []
    rel = "data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_d.csv"
    d = pd.read_csv(RAIZ / rel)
    d = d.melt(id_vars="date", var_name="c", value_name="valor").dropna(subset=["valor"])
    d["valor"] = d.valor.astype(float) + 0.0  # -0 -> 0
    d["variable"] = "bce_jk_" + d.c.str.lower() + "_d"
    d["periodo"] = d.date
    d["frecuencia"] = "D"
    d["fecha_dato"] = d.date
    d["unidad"] = JK_UNIDAD
    d.loc[d.c == "STOXX50", "unidad"] = "variación del STOXX50 en la ventana de la reunión (unidad no declarada en el fichero JK)"
    d["territorio_codigo"], d["nivel"] = "EA", "zona_euro"
    out.append(construir(d, rel, man))
    rel = "data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_m.csv"
    m = pd.read_csv(RAIZ / rel)
    m["periodo"] = m.year.astype(str) + "-" + m.month.astype(str).str.zfill(2)
    m = m.drop(columns=["year", "month"]).melt(id_vars="periodo", var_name="c", value_name="valor").dropna(subset=["valor"])
    m["valor"] = m.valor.astype(float) + 0.0
    m["variable"] = "bce_jk_" + m.c.str.lower().str.replace("_hf", "") + "_m"
    m["frecuencia"] = "M"
    m["fecha_dato"] = fin_periodo(m.periodo, "M")
    m["unidad"] = JK_UNIDAD
    m.loc[m.c == "STOXX50_hf", "unidad"] = "variación del STOXX50 en las ventanas del mes (unidad no declarada en el fichero JK)"
    m["territorio_codigo"], m["nivel"] = "EA", "zona_euro"
    m["metodo_dato"] = "observado (agregado mensual de los autores; cero si no hay reunión)"
    out.append(construir(m, rel, man))
    return out


def bde(man: dict) -> pd.DataFrame:
    rel = "data/raw/v16/demanda_internacional/bde_fijacion/bde_nuevas_fijacion_vivienda.csv"
    d = pd.read_csv(RAIZ / rel).dropna(subset=["valor"])
    d = d[d.serie.isin(BDE_VARS)].copy()
    d["variable"] = d.serie.map(lambda s: BDE_VARS[s][0])
    d["unidad"] = d.serie.map(lambda s: BDE_VARS[s][2])
    d["frecuencia"] = "M"
    d["fecha_dato"] = fin_periodo(d.periodo, "M")
    d["territorio_codigo"], d["nivel"] = "00", "nacional"
    return construir(d[["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "valor", "unidad", "fecha_dato"]], rel, man)


def ine(man: dict) -> pd.DataFrame:
    rel = "data/raw/v16/demanda_internacional/ine_etdp_titular/ine_etdp_titular_largo.csv"
    d = pd.read_csv(RAIZ / rel, dtype={"periodo": str}).dropna(subset=["valor"])
    partes = d.descripcion.str.extract(r"Total Nacional\. (Persona \w+)\. (Persona \w+)\.")
    # supuesto declarado: el orden del título del INE es «transmitente. titular»
    cond = lambda s: s.str.replace("Persona jurídica", "juridica").str.replace("Persona física", "fisica")
    d["desagregacion"] = "transmitente=" + cond(partes[0]) + ";titular=" + cond(partes[1])
    anual = d.periodo.str.endswith("anual")
    d["periodo"] = d.periodo.str.replace("-anual", "", regex=False)
    d["frecuencia"] = anual.map({True: "A", False: "M"})
    d["fecha_dato"] = d.periodo.str[:4] + "-12-31"
    mm = d.frecuencia == "M"
    d.loc[mm, "fecha_dato"] = list(fin_periodo(d.loc[mm, "periodo"], "M"))
    d["variable"] = "ine_etdp_compraventas_vivienda_pct"
    d["unidad"] = "porcentaje de compraventas de vivienda"
    d["territorio_codigo"], d["nivel"] = "00", "nacional"
    return construir(d[["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fecha_dato"]], rel, man)


def oecd(man: dict) -> pd.DataFrame:
    rel = "data/raw/v16/demanda_internacional/comparacion_internacional/oecd_house_prices_todos.csv.gz"
    d = pd.read_csv(RAIZ / rel, usecols=["REF_AREA", "MEASURE", "UNIT_MEASURE", "TIME_PERIOD", "OBS_VALUE", "ADJUSTMENT", "OBS_STATUS"])
    d = d.dropna(subset=["OBS_VALUE"])
    sin = sorted(set(d.REF_AREA) - set(ISO3_ISO2))
    if sin:
        print("OCDE: áreas sin correspondencia ISO-2 (descartadas):", sin)
    d = d[d.REF_AREA.isin(ISO3_ISO2)].copy()
    d["territorio_codigo"], d["nivel"] = d.REF_AREA.map(ISO3_ISO2), "pais"
    d["periodo"] = d.TIME_PERIOD.str.replace("-Q", "T")
    d["frecuencia"] = "T"
    d["fecha_dato"] = fin_periodo(d.periodo, "T")
    d["variable"] = "oecd_" + d.MEASURE.str.lower()
    d["unidad"] = d.UNIT_MEASURE.map(OECD_UNIDAD)
    d["valor"] = d.OBS_VALUE.astype(float)
    return construir(d[["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "valor", "unidad", "fecha_dato"]], rel, man)


def eurostat(man: dict) -> pd.DataFrame:
    rel = "data/raw/v16/demanda_internacional/eurostat_ilc/ilc_lvho07a_todos_desgloses.csv.gz"
    d = pd.read_csv(RAIZ / rel, dtype=str)
    d = d.dropna(subset=["OBS_VALUE"]).copy()
    d["valor"] = d.OBS_VALUE.astype(float)
    g = d.geo
    d["territorio_codigo"] = g.map(lambda x: EUROSTAT_PAIS.get(x, x))
    d["nivel"] = g.map(lambda x: "zona_euro" if x == "EA" else "agregado_ue" if x in EUROSTAT_AGREGADOS else "pais")
    d["periodo"] = d.TIME_PERIOD
    d["frecuencia"] = "A"
    d["fecha_dato"] = fin_periodo(d.periodo, "A")
    d["variable"] = "eurostat_sobrecarga_coste_vivienda_pct"
    d["unidad"] = "porcentaje de la población del desglose"
    d["desagregacion"] = "edad=" + d.age + ";sexo=" + d.sex + ";pobreza=" + d.rskpovth
    d["metodo_dato"] = d.OBS_FLAG.map(lambda f: "observado" if pd.isna(f) else f"observado;marca_eurostat={f}")
    return construir(d[["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fecha_dato",
                        "metodo_dato"]], rel, man)


def eampd(man: dict) -> pd.DataFrame | None:
    rel = "data/raw/v16/demanda_internacional/_terceros/bce_sorpresas/Dataset_EA-MPD.xlsx"
    f = RAIZ / rel
    if not f.exists():
        return None
    try:
        x = pd.ExcelFile(f)
    except Exception as e:  # sin openpyxl o libro dañado: no falla
        print("EA-MPD no legible:", e)
        return None
    ventanas = {"Press Release Window": "press_release", "Press Conference Window": "press_conference",
                "Monetary Event Window": "monetary_event"}
    partes = []
    for hoja, v in ventanas.items():
        d = x.parse(hoja)
        fecha = d.date.map(lambda z: pd.to_datetime(z, dayfirst=True) if isinstance(z, str) else pd.Timestamp(z))
        d = d.drop(columns="date")
        d.index = fecha.dt.strftime("%Y-%m-%d")
        d = d.rename_axis("periodo").reset_index().melt(id_vars="periodo", var_name="c", value_name="valor").dropna(subset=["valor"])
        d["valor"] = d.valor.astype(float)
        d["desagregacion"] = "ventana=" + v
        partes.append(d)
    d = pd.concat(partes, ignore_index=True)
    d["variable"] = "bce_eampd_" + d.c.str.lower()
    d["frecuencia"], d["fecha_dato"] = "D", d.periodo
    d["unidad"] = d.c.map(lambda c: "variación porcentual (puntos porcentuales)" if c in ("STOXX50", "SX7E", "EURUSD", "EURGBP", "EURJPY")
                          else "puntos básicos")
    d["territorio_codigo"], d["nivel"] = "EA", "zona_euro"
    d = d.drop(columns="c")
    return construir(d, rel, man, redistribuible=False)


def diccionario(h: pd.DataFrame, t: pd.DataFrame | None) -> pd.DataFrame:
    desc = {v[0]: v[1] for v in BDE_VARS.values()}
    desc.update({"ine_etdp_compraventas_vivienda_pct": "ETDP INE: % de compraventas de vivienda por condición de transmitente y titular (desagregación)",
                 "eurostat_sobrecarga_coste_vivienda_pct": "Eurostat ilc_lvho07a: tasa de sobrecarga del coste de la vivienda (>40 % de la renta)"})
    jkd = {"pc1": "factor de sorpresa (OIS 1M-1Y)", "stoxx50": "reacción del STOXX50", "mp_pm": "choque de política monetaria (restricciones de signo simples)",
           "cbi_pm": "información del banco central (restricciones de signo simples)", "mp_median": "choque de política monetaria (rotación mediana)",
           "cbi_median": "información del banco central (rotación mediana)"}
    for k, v in jkd.items():
        desc["bce_jk_" + k + "_d"] = "Jarociński-Karadi, por reunión del Consejo de Gobierno: " + v
        desc["bce_jk_" + k + "_m"] = "Jarociński-Karadi, agregado mensual: " + v
    for k, v in OECD_DESC.items():
        desc["oecd_" + k.lower()] = "OCDE Analytical house prices: " + v
    rupt = {"bde": "clasificación por periodo inicial de fijación (no fijo/variable); series con huecos (celdas «_») descartadas",
            "oecd": "ajuste S (desestacionalizado) en todas las series; base 2015=100",
            "eurostat": "marcas de calidad (b ruptura de serie, u poco fiable, e estimado, p provisional) en metodo_dato; agregados EA18-EA21/EU* con nivel agregado_ue",
            "ine": "orden transmitente/titular supuesto según el título de la tabla; mensual (50256) y anual (50272) con frecuencia distinta",
            "bce_jk": "sin unidad declarada en el CSV; muestra hasta 2025-10-30",
            "bce_ea": "cambio de ventanas horarias en julio 2022; terceros, no versionado"}
    filas = []
    for df in [h] + ([t] if t is not None else []):
        for (v, f, n), g in df.groupby(["variable", "frecuencia", "nivel"]):
            clave = next((k for k in rupt if v.startswith(k)), "")
            if v.startswith("bce_eampd"):
                clave = "bce_ea"
            filas.append({"variable": v, "descripcion": desc.get(v, v), "unidad": g.unidad.iloc[0], "nivel": n, "frecuencia": f,
                          "periodo_min": g.periodo.min(), "periodo_max": g.periodo.max(), "fuente": g.fuente.iloc[0],
                          "rupturas": rupt.get(clave, "")})
    return pd.DataFrame(filas)


def main() -> int:
    man = manifiesto()
    partes = jk(man) + [bde(man), ine(man), oecd(man), eurostat(man)]
    h = pd.concat(partes, ignore_index=True)
    h["muestra_sellada_v6"] = sellada(h)
    h = h[COLS].sort_values(["variable", "nivel", "territorio_codigo", "desagregacion", "periodo"], kind="mergesort").reset_index(drop=True)
    SAL.mkdir(parents=True, exist_ok=True)
    h.to_parquet(SAL / "demanda_internacional.parquet", index=False)
    t = eampd(man)
    ruta_t = SAL / "demanda_internacional_terceros.parquet"
    if t is not None:
        t["muestra_sellada_v6"] = sellada(t)
        t = t[COLS].sort_values(["variable", "desagregacion", "periodo"], kind="mergesort").reset_index(drop=True)
        t.to_parquet(ruta_t, index=False)
    elif ruta_t.exists():
        ruta_t.unlink()
    diccionario(h, t).to_csv(DICC, index=False)
    res = {"rama": "v16-f1-datos-demanda_internacional",
           "pregunta": "Normalización al formato largo: choques BCE (JK; EA-MPD en terceros), BdE nuevas operaciones por periodo de fijación, "
                       "INE ETDP por titular, OCDE precios analíticos, Eurostat sobrecarga de vivienda",
           "capa": "C4", "N": int(len(h)), "metodo": "normalización",
           "notas": f"N_terceros={0 if t is None else len(t)} (no versionado, redistribuible=False). posterior_prereg=False porque el corte de V16 no "
                    "está fijado. Sin datos de provincia o inferior: muestra_sellada_v6 = False en todas las filas. Descartes: celdas vacías del BdE, "
                    "Eurostat y EA-MPD; zip JK de terceros no procesado."}
    (SAL / "demanda_internacional_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"filas versionadas={len(h)} terceros={0 if t is None else len(t)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
