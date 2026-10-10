"""Panel europeo (v2): Eurostat, OCDE (SDMX) y BIS (SDMX) a data/raw en formato largo.

Salidas (data/raw/):
- eu_hpi.csv           Eurostat prc_hpi_a (anual) y prc_hpi_q (trimestral): TOTAL, índice y tasa anual.
- eu_hicp_rent.csv     Eurostat prc_hicp_aind (anual) y prc_hicp_midx (mensual): CP041 alquiler real.
- eu_hicp.csv          Eurostat prc_hicp_aind CP00 (IAPC general, anual).
- eu_permits.csv       Eurostat sts_cobp_a (anual, BPRM_DW en miles y BPRM_SQM en millones m2) y
                       sts_cobp_q (trimestral, índice BPRM_DW) cuando existe.
- eu_migr_pop.csv      Eurostat migr_imm1ctz (inmigración total) y demo_pjan (población 1 enero).
- eu_rates.csv         BCE MIR (nuevas hipotecas para vivienda, hogares, por país del área euro,
                       clave M.<país>.B.A2C.AM.R.A.2250.EUR.N) y Eurostat irt_lt_mcby_a (tipo largo).
- eu_income_emp.csv    Eurostat nasa_10_nf_tr (renta bruta disponible de hogares, B6G, CP_MEUR) y
                       lfsi_emp_a (empleo 15-64, miles de personas).
- oecd_house_prices.csv OCDE, Analytical house prices indicators (DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES),
                       frecuencias anual y trimestral, todas las medidas publicadas.
- bis_rpp.csv          BIS, WS_SPP (precios residenciales), trimestral, países europeos.

Códigos: Eurostat usa EL (Grecia) y UK (Reino Unido); OCDE y BIS usan GRC/GR y GBR/GB.
La columna 'territorio' conserva el código de cada fuente.

Caché: si el CSV de destino existe no se vuelve a bajar (salvo FORCE=1). Cada endpoint se prueba
antes con una petición pequeña (lastTimePeriod=1 / lastNObservations=1) y se anota la última fecha.
Los fallos se anotan en docs/v2/fallidas/ue_bde.md y no se rellenan con datos inventados.

Ejecutar desde la raíz del repo:  python3 src/fetch_ue_v2.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_eurostat import (  # noqa: E402
    _recortar_vacios, _url, jsonstat_a_largo, parse_periodo,
)
from fetch_ecb import BASE as ECB_BASE, _to_long  # noqa: E402
from utils_fetch import ROOT, cached, get, save  # noqa: E402

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
OECD_BASE = "https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,"
BIS_BASE = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_SPP/1.0/"
FALLIDAS = ROOT / "docs" / "v2" / "fallidas" / "ue_bde.md"

# Eurostat: EU27 (+ agregado), EFTA (NO, CH, IS) y Reino Unido (UK).
EU_GEO = [
    "EU27_2020", "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU",
    "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
    "NO", "CH", "IS", "UK",
]
# OCDE: países europeos miembros (EU27 no OCDE: BG, HR, CY, MT, RO no están).
OECD_AREAS = [
    "AUT", "BEL", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN", "ISL", "IRL", "ITA",
    "LVA", "LTU", "LUX", "NLD", "NOR", "POL", "PRT", "SVK", "SVN", "ESP", "SWE", "CHE", "GBR", "TUR",
]
# BIS: países europeos con WS_SPP (+ XM = área euro).
BIS_AREAS = [
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
    "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "IS", "NO", "CH",
    "GB", "TR", "XM",
]
# Miembros del área euro para el MIR del BCE (clave de país BCE; Grecia = GR). U2 = área euro.
MIR_PAISES = [
    "U2", "AT", "BE", "HR", "CY", "EE", "FI", "FR", "DE", "GR", "IE", "IT", "LV", "LT", "LU",
    "MT", "NL", "PT", "SK", "SI", "ES", "BG",
]
# Unidades BIS (codelist CL_BIS_UNIT) usadas en WS_SPP.
BIS_UNIDAD = {
    "628": "Índice 2010 = 100",
    "771": "Variación interanual, %",
}

DESDE_A = "2000"
DESDE_Q = "2000-Q1"
DESDE_M = "2000-01"


def _registrar_fallo(nombre: str, errores: list[tuple[str, str]]) -> None:
    FALLIDAS.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not FALLIDAS.exists()
    with FALLIDAS.open("a", encoding="utf-8") as f:
        if nuevo:
            f.write("# Fallos de descarga v2: UE (Eurostat, OCDE, BIS, BCE) y Banco de España\n\n")
        f.write(f"## {nombre}\n")
        for url, err in errores:
            f.write(f"- URL probada: {url}\n  - Error: {err}\n")
        f.write("\n")


# ---------------------------------------------------------------- Eurostat

def _eurostat(dataset: str, filtros: dict, desde: str) -> tuple[pd.DataFrame, str, str]:
    """Probe (lastTimePeriod=1) y descarga completa desde 'desde'. Devuelve (df, url, último periodo)."""
    probe = jsonstat_a_largo(get(_url(dataset, filtros, lastTimePeriod=1)))
    ok = probe[probe["valor"].notna()]
    if ok.empty:
        raise ValueError("la petición de prueba no devuelve valores (revisar filtros/códigos)")
    ultimo = str(ok["periodo"].max())
    url = _url(dataset, filtros, sinceTimePeriod=desde)
    df = jsonstat_a_largo(get(url))
    df = _recortar_vacios(df)
    if df["valor"].notna().sum() == 0:
        raise ValueError("la descarga completa no contiene valores")
    df = df.assign(
        dataset=dataset,
        serie=dataset + "|" + df["serie"],
        territorio=df["geo"],
        fuente="Eurostat",
        url=url,
    )
    print(f"[info] Eurostat {dataset}: última publicación {ultimo}; {df['territorio'].nunique()} territorios")
    return df, url, ultimo


def _eurostat_bloque(nombre: str, bloque: list[tuple[str, dict, str]]) -> None:
    """bloque = [(dataset, filtros, desde)]; los fallos parciales se anotan y no detienen el archivo."""
    if cached(nombre):
        return
    partes, errores = [], []
    for dataset, filtros, desde in bloque:
        try:
            df, _, _ = _eurostat(dataset, filtros, desde)
            partes.append(df)
        except Exception as e:  # noqa: BLE001
            errores.append((_url(dataset, filtros, sinceTimePeriod=desde), str(e)))
            print(f"[fallo] {nombre} <- {dataset}: {e}")
    if partes:
        df = pd.concat(partes, ignore_index=True)
        save(df, nombre, "Eurostat")
    if errores:
        _registrar_fallo(f"{nombre} (Eurostat)", errores)


# ---------------------------------------------------------------- BCE (MIR por país)

def _ecb_mir_frame():
    """Hipotecas para vivienda, nuevas operaciones, por país del área euro (BCE MIR).
    Devuelve (df, errores) o None si ningún país responde."""
    partes, errores = [], []
    for cc in MIR_PAISES:
        key = f"MIR/M.{cc}.B.A2C.AM.R.A.2250.EUR.N"
        url = f"{ECB_BASE}/{key}"
        try:
            probe = pd.read_csv(io.StringIO(get(url, params={"format": "csvdata", "lastNObservations": "3"},
                                                 as_json=False)))
            print(f"[probe] BCE {key}: última observación {probe['TIME_PERIOD'].iloc[-1]}")
            text = get(url, params={"format": "csvdata"}, as_json=False)
            partes.append(_to_long(text, f"{url}?format=csvdata").assign(territorio=cc, dataset="MIR"))
        except Exception as e:  # noqa: BLE001
            errores.append((f"{url}?format=csvdata", str(e)))
            print(f"[fallo] BCE MIR {cc}: {e}")
    if not partes:
        return None
    return _recortar_vacios(pd.concat(partes, ignore_index=True)), errores


def _eu_rates(nombre: str) -> None:
    """eu_rates.csv = BCE MIR (por país) + Eurostat irt_lt_mcby_a (tipo largo Maastricht)."""
    if cached(nombre):
        return
    partes, errores = [], []
    for dataset, filtros, desde in BLOQUES["eu_rates.csv"]:
        try:
            partes.append(_eurostat(dataset, filtros, desde)[0])
        except Exception as e:  # noqa: BLE001
            errores.append((_url(dataset, filtros, sinceTimePeriod=desde), str(e)))
            print(f"[fallo] {nombre} <- {dataset}: {e}")
    mir = _ecb_mir_frame()
    if mir is not None:
        partes.append(mir[0])
        errores += mir[1]
    if partes:
        save(pd.concat(partes, ignore_index=True), nombre, "Eurostat/BCE")
    if errores:
        _registrar_fallo(f"{nombre} (Eurostat irt_lt_mcby_a / BCE MIR)", errores)


# ---------------------------------------------------------------- OCDE

def _ocde(nombre: str) -> None:
    if cached(nombre):
        return
    areas = "+".join(OECD_AREAS)
    key = f"{areas}.A+Q...."
    probe_url = f"{OECD_BASE}/{key}?lastNObservations=1&format=csvfilewithlabels"
    try:
        p = pd.read_csv(io.StringIO(get(probe_url, as_json=False)))
        print(f"[probe] OCDE: {len(p)} filas; última observación {p['TIME_PERIOD'].astype(str).max()}")
    except Exception as e:  # noqa: BLE001
        _registrar_fallo("oecd_house_prices.csv (OCDE)", [(probe_url, str(e))])
        print(f"[fallo] OCDE probe: {e}")
        return
    url = f"{OECD_BASE}/{key}?startPeriod=2000&format=csvfilewithlabels"
    try:
        raw = pd.read_csv(io.StringIO(get(url, as_json=False)))
    except Exception as e:  # noqa: BLE001
        _registrar_fallo("oecd_house_prices.csv (OCDE)", [(url, str(e))])
        print(f"[fallo] OCDE descarga: {e}")
        return
    if raw.empty:
        _registrar_fallo("oecd_house_prices.csv (OCDE)", [(url, "respuesta sin observaciones")])
        return
    per = raw["TIME_PERIOD"].astype(str)
    df = pd.DataFrame({
        "fecha": per.map(lambda p: parse_periodo(p).isoformat()),
        "periodo": per,
        "serie": ("OECD|" + raw["MEASURE"].astype(str) + "|" + raw["UNIT_MEASURE"].astype(str)
                  + "|" + raw["ADJUSTMENT"].fillna("").astype(str) + "|" + raw["REF_AREA"].astype(str)
                  + "|" + raw["FREQ"].astype(str)),
        "valor": pd.to_numeric(raw["OBS_VALUE"], errors="coerce"),
        "unidad": raw["Unit of measure"].astype(str),
        "fuente": "OCDE",
        "url": url,
        "territorio": raw["REF_AREA"],
        "territorio_nombre": raw["Reference area"],
        "frecuencia": raw["FREQ"],
        "medida": raw["MEASURE"],
        "medida_nombre": raw["Measure"],
        "ajuste": raw["ADJUSTMENT"].fillna(""),
        "estado_obs": raw["OBS_STATUS"].fillna("") if "OBS_STATUS" in raw else "",
    })
    df = _recortar_vacios(df)
    print(f"[info] OCDE: {df['territorio'].nunique()} áreas, {df['serie'].nunique()} series")
    save(df, nombre, "OCDE")


# ---------------------------------------------------------------- BIS

def _bis(nombre: str) -> None:
    if cached(nombre):
        return
    areas = "+".join(BIS_AREAS)
    key = f"Q.{areas}.."
    probe_url = f"{BIS_BASE}{key}?format=csv&lastNObservations=1"
    try:
        p = pd.read_csv(io.StringIO(get(probe_url, as_json=False)))
        print(f"[probe] BIS: última observación {p['TIME_PERIOD'].astype(str).max()}")
    except Exception as e:  # noqa: BLE001
        _registrar_fallo("bis_rpp.csv (BIS WS_SPP)", [(probe_url, str(e))])
        print(f"[fallo] BIS probe: {e}")
        return
    url = f"{BIS_BASE}{key}?format=csv&startPeriod={DESDE_Q}"
    try:
        raw = pd.read_csv(io.StringIO(get(url, as_json=False)), dtype={"UNIT_MEASURE": str})
    except Exception as e:  # noqa: BLE001
        _registrar_fallo("bis_rpp.csv (BIS WS_SPP)", [(url, str(e))])
        print(f"[fallo] BIS descarga: {e}")
        return
    per = raw["TIME_PERIOD"].astype(str)
    df = pd.DataFrame({
        "fecha": per.map(lambda p: parse_periodo(p).isoformat()),
        "periodo": per,
        "serie": ("BIS|WS_SPP|" + raw["VALUE"].astype(str) + "|" + raw["UNIT_MEASURE"].astype(str)
                  + "|" + raw["REF_AREA"].astype(str) + "|" + raw["FREQ"].astype(str)),
        "valor": pd.to_numeric(raw["OBS_VALUE"], errors="coerce"),
        "unidad": raw["UNIT_MEASURE"].astype(str).map(lambda c: BIS_UNIDAD.get(c, c)),
        "fuente": "BIS",
        "url": url,
        "territorio": raw["REF_AREA"],
        "frecuencia": raw["FREQ"],
        "precio": raw["VALUE"].map({"N": "nominal", "R": "real"}).fillna(raw["VALUE"].astype(str)),
        "estado_obs": raw["OBS_STATUS"].fillna(""),
    })
    df = _recortar_vacios(df)
    print(f"[info] BIS: {df['territorio'].nunique()} áreas, {df['serie'].nunique()} series")
    save(df, nombre, "BIS")


# ---------------------------------------------------------------- definición de salidas

BLOQUES = {
    "eu_hpi.csv": [
        ("prc_hpi_a", {"geo": EU_GEO, "purchase": "TOTAL", "unit": ["I15_A_AVG", "RCH_A_AVG"]}, DESDE_A),
        ("prc_hpi_q", {"geo": EU_GEO, "purchase": "TOTAL", "unit": ["I15_Q", "RCH_A"]}, DESDE_Q),
    ],
    "eu_hicp_rent.csv": [
        ("prc_hicp_aind", {"geo": EU_GEO, "coicop": "CP041", "unit": ["INX_A_AVG", "RCH_A_AVG"]}, DESDE_A),
        ("prc_hicp_midx", {"geo": EU_GEO, "coicop": "CP041", "unit": "I15"}, DESDE_M),
    ],
    "eu_hicp.csv": [
        ("prc_hicp_aind", {"geo": EU_GEO, "coicop": "CP00", "unit": ["INX_A_AVG", "RCH_A_AVG"]}, DESDE_A),
    ],
    "eu_permits.csv": [
        ("sts_cobp_a", {"geo": EU_GEO, "indic_bt": "BPRM_DW", "cpa2_1": "CPA_F41001_X_410014",
                        "unit": "THS"}, DESDE_A),
        ("sts_cobp_a", {"geo": EU_GEO, "indic_bt": "BPRM_SQM", "cpa2_1": "CPA_F41001",
                        "unit": "MIO_M2"}, DESDE_A),
        ("sts_cobp_q", {"geo": EU_GEO, "indic_bt": "BPRM_DW", "cpa2_1": "CPA_F41001_X_410014",
                        "unit": "I21", "s_adj": "SCA"}, DESDE_Q),
    ],
    "eu_migr_pop.csv": [
        ("migr_imm1ctz", {"geo": EU_GEO, "citizen": "TOTAL", "age": "TOTAL", "sex": "T",
                          "agedef": "REACH"}, DESDE_A),
        ("demo_pjan", {"geo": EU_GEO, "age": "TOTAL", "sex": "T"}, DESDE_A),
    ],
    "eu_income_emp.csv": [
        ("nasa_10_nf_tr", {"geo": EU_GEO, "sector": "S14_S15", "na_item": "B6G", "direct": "RECV",
                           "unit": "CP_MEUR"}, DESDE_A),
        ("lfsi_emp_a", {"geo": EU_GEO, "sex": "T", "age": "Y15-64", "unit": "THS_PER",
                        "indic_em": "EMP_LFS"}, DESDE_A),
    ],
    "eu_rates.csv": [
        ("irt_lt_mcby_a", {"geo": EU_GEO, "int_rt": "MCBY"}, DESDE_A),
    ],
}


def main() -> None:
    for nombre, bloque in BLOQUES.items():
        if nombre != "eu_rates.csv":
            _eurostat_bloque(nombre, bloque)
    _eu_rates("eu_rates.csv")
    _ocde("oecd_house_prices.csv")
    _bis("bis_rpp.csv")


if __name__ == "__main__":
    main()
