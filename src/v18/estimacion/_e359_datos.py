"""V18 · fase 4 · capa de datos compartida de E3, E5 y E9: lecturas con sellado de V18 y construcción de los bloques del shift-share.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010. Cada serie pasa por _e359_comun.filtrar
(sellado.filtrar + holdout.excluir_sellados_v6()). Los periodos y las unidades selladas no llegan a ninguna estimación.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import _e359_comun as K

RAW = K.RAW
EURO = K.EURO

# ------------------------------------------------------------------------------------------------ grupos de origen (adenda AD-E3, lista fija)
# La lista fija de 16 grupos del Censo de 1991 no puede construirse con el Censo de 2001 que sirve Eurostat (cens_01rsctz): solo distingue
# 14 países de la UE-15, la AELC, Europa Central y del Este, la ex-URSS europea, el resto de Europa, el norte de África, el resto de África,
# América del Norte, el resto de América, Asia, Oceanía y otros (docs/v18/desviaciones.md, D-E359-3). Los 16 grupos se funden en 8 antes de estimar.
GRUPOS = ["G1_UE15", "G2_AELC", "G3_Europa_resto", "G4_Africa_norte", "G5_Africa_resto", "G6_America_latina_Caribe", "G7_Asia", "G8_resto_mundo"]
EU15 = {"AT", "BE", "DE", "DK", "EL", "FI", "FR", "IE", "IT", "LU", "NL", "PT", "SE", "UK"}
EFTA = {"CH", "NO", "IS", "LI"}
EUR_RESTO = {"AD", "AL", "BA", "BG", "BY", "CY", "CZ", "EE", "HR", "HU", "LT", "LV", "MC", "MD", "ME", "MK", "MT", "PL", "RO", "RS", "RU", "SI", "SK", "SM",
             "UA", "VA", "XK", "FO", "GI", "GG", "JE", "IM", "EX_YU", "EX_SU", "RS_ME", "CZ_SK"}
AFRICA_N = {"MA", "DZ", "TN", "LY", "EG", "EH"}
AFRICA_RESTO = {"AO", "BF", "BI", "BJ", "BW", "CD", "CF", "CG", "CI", "CM", "CV", "DJ", "ER", "ET", "GA", "GH", "GM", "GN", "GQ", "GW", "KE", "KM", "LR", "LS",
                "MG", "ML", "MR", "MU", "MW", "MZ", "NA", "NE", "NG", "RW", "SC", "SD", "SL", "SN", "SO", "ST", "SZ", "TD", "TG", "TZ", "UG", "ZA", "ZM", "ZW",
                "SS", "SH", "YT", "RE"}
AMERICA_LATINA = {"AG", "AI", "AN", "AR", "AW", "BB", "BO", "BQ", "BR", "BS", "BZ", "CL", "CO", "CR", "CU", "CW", "DM", "DO", "EC", "FK", "GD", "GT", "GY", "HN",
                  "HT", "JM", "KN", "KY", "LC", "MS", "MX", "NI", "PA", "PE", "PY", "SR", "SV", "SX", "TC", "TT", "UY", "VC", "VE", "VG", "BL", "MF", "GF", "GP",
                  "MQ", "VI", "PR", "CRB"}
ASIA = {"AE", "AF", "AM", "AZ", "BD", "BH", "BN", "BT", "CN", "GE", "HK", "ID", "IL", "IN", "IQ", "IR", "JO", "JP", "KG", "KH", "KP", "KR", "KW", "KZ", "LA", "LB",
        "LK", "MM", "MN", "MO", "MV", "MY", "NP", "OM", "PH", "PK", "PS", "QA", "SA", "SG", "SY", "TH", "TJ", "TL", "TM", "TR", "TW", "UZ", "VN", "YE"}
CODIGOS = [EU15, EFTA, EUR_RESTO, AFRICA_N, AFRICA_RESTO, AMERICA_LATINA, ASIA]


def flujos_por_grupo() -> pd.DataFrame:
    """Entradas desde el extranjero por grupo de nacionalidad (columnas = GRUPOS, índice = año), Eurostat migr_imm1ctz (datos del INE). El grupo 8
    es el resto hasta el total de extranjeros y apátridas (FOR_STLS): Norteamérica, Oceanía, apátridas y códigos sin asignar. 2003 no tiene
    detalle por nacionalidad en la fuente y queda vacío (no se interpola en la principal). Sellado: ine_migraciones_nacionalidad|nacional|A."""
    d = pd.read_csv(RAW / "eurostat_inmigracion_anual.csv", keep_default_na=False)
    d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
    d["periodo"] = d["periodo"].astype(str)
    d["territorio_codigo"] = "00"
    d = K.filtrar(d, "territorio_codigo", "nacional", "periodo", "ine_migraciones_nacionalidad", "A")
    w = d.pivot_table(index="citizen", columns="periodo", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    out = {}
    for g, cods in zip(GRUPOS[:7], CODIGOS):
        out[g] = w.reindex(sorted(cods & set(w.index))).sum(axis=0, min_count=1)
    out = pd.DataFrame(out)
    tot = w.loc["FOR_STLS"]
    out[GRUPOS[7]] = (tot - out.sum(axis=1, min_count=7)).clip(lower=0)
    out.loc[~tot.notna(), :] = np.nan
    out["total_extranjeros"] = tot
    return out.sort_index()


def censo2001_grupos() -> pd.DataFrame:
    """Censo de 2001 (Eurostat cens_01rsctz): extranjeros por grupo y provincia (índice = código INE de provincia, columnas = GRUPOS) y totales.
    Las 52 provincias (también las selladas) se usan SOLO para el denominador nacional de cada grupo (la nación no está sellada); el filtro de
    sellado se aplica al devolver las provincias de entrenamiento. Devuelve (shares_loc, stock, pob_total_censo) con stock de las 52."""
    c = pd.read_csv(EURO / "cens_01rsctz_ES_nuts3.csv.gz", keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce")
    c = c[c["geo"].isin(K.NUTS3_A_PROV)].copy()
    c["cod"] = c["geo"].map(K.NUTS3_A_PROV)
    w = c.pivot_table(index="cod", columns="citizen", values="valor", aggfunc="first").fillna(0.0)
    g = pd.DataFrame({
        GRUPOS[0]: w["EU_FOR"], GRUPOS[1]: w["EFTA"], GRUPOS[2]: w["EUR_C_E"] + w["EX_SU_EUR"] + w["EUR_OTH"], GRUPOS[3]: w["AFR_N"],
        GRUPOS[4]: w["AFR_OTH"], GRUPOS[5]: w["AME_OTH"], GRUPOS[6]: w["ASI"], GRUPOS[7]: w["AME_N"] + w["OCE"] + w["OTH"]})
    ext = w["TOTAL"] - w["NAT"]
    g["total_extranjeros"] = ext
    g["pob_total"] = w["TOTAL"]
    return g


def shares_localizacion(stock: pd.DataFrame, provincias: list[str]) -> pd.DataFrame:
    """s_pc = stock_pc,2001 / stock_c,nacional,2001 (la distribución de cada grupo entre provincias; suma 1 sobre las 52). Solo las provincias
    pedidas (entrenamiento) en el índice."""
    S = stock[GRUPOS].div(stock[GRUPOS].sum(axis=0), axis=1)
    sal = S.loc[[p for p in provincias if p in S.index]]
    # el filtro de sellado se aplica por el manifiesto (periodo de la fuente = 2001)
    tmp = sal.reset_index().rename(columns={"cod": "cod"})
    tmp["periodo"] = "2001"
    tmp = K.filtrar(tmp, "cod", "provincia", "periodo", "eurostat_censo2001_nacionalidad", "A")
    return tmp.set_index("cod").drop(columns="periodo")


def empleo_a10() -> pd.DataFrame:
    """Empleo (miles de personas) por provincia y rama NACE Rev. 2, Eurostat nama_10r_3empers (índice MultiIndex (cod, rama), columnas = años).
    Se devuelve también el nacional ('ES', suma de las 52 provincias de la fuente) para el crecimiento sectorial sin la propia provincia."""
    e = pd.read_csv(EURO / "nama_10r_3empers_ES_nuts3.csv.gz", keep_default_na=False)
    e["valor"] = pd.to_numeric(e["valor"], errors="coerce")
    e = e[e["geo"].isin(K.NUTS3_A_PROV)].copy()
    e["cod"] = e["geo"].map(K.NUTS3_A_PROV)
    w = e.pivot_table(index=["cod", "nace_r2"], columns="time", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    return w


def empleo_nacional() -> pd.DataFrame:
    """Empleo nacional por rama (fila «ES» de nama_10r_3empers; incluye las provincias selladas: la nación no está sellada). Índice = rama, columnas = años (≤ 2024)."""
    e = pd.read_csv(EURO / "nama_10r_3empers_ES_nuts3.csv.gz", keep_default_na=False)
    e["valor"] = pd.to_numeric(e["valor"], errors="coerce")
    e = e[e["geo"] == "ES"].copy()
    e["cod"] = "00"
    e["periodo"] = e["time"].astype(str)
    e = K.filtrar(e[["cod", "nace_r2", "periodo", "valor"]], "cod", "nacional", "periodo", "eurostat_empleo_nuts3_a10", "A")
    w = e.pivot_table(index="nace_r2", columns="periodo", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    return w


def empleo_entrenamiento(provincias: list[str]) -> pd.DataFrame:
    w = empleo_a10()
    tmp = w.reset_index()
    largo = tmp.melt(id_vars=["cod", "nace_r2"], var_name="periodo", value_name="valor")
    largo["periodo"] = largo["periodo"].astype(str)
    largo = largo[largo["cod"].isin(provincias)]
    largo = K.filtrar(largo, "cod", "provincia", "periodo", "eurostat_empleo_nuts3_a10", "A")
    p = largo.pivot_table(index=["cod", "nace_r2"], columns="periodo", values="valor", aggfunc="first")
    p.columns = [int(c) for c in p.columns]
    return p


def poblacion_edad(provincias: list[str]) -> pd.DataFrame:
    """Eurostat demo_r_pjanaggr3 (1 de enero): MultiIndex (cod, edad) con edad en TOTAL, Y15-64, Y_GE65, Y_LT15; columnas = años (≤ 2024)."""
    p = pd.read_csv(EURO / "demo_r_pjanaggr3_ES_nuts3.csv.gz", keep_default_na=False)
    p["valor"] = pd.to_numeric(p["valor"], errors="coerce")
    p = p[p["geo"].isin(K.NUTS3_A_PROV)].copy()
    p["cod"] = p["geo"].map(K.NUTS3_A_PROV)
    p = p[p["cod"].isin(provincias)]
    p["periodo"] = p["time"].astype(str)
    p = K.filtrar(p, "cod", "provincia", "periodo", "eurostat_poblacion_nuts3", "A")
    w = p.pivot_table(index=["cod", "age"], columns="periodo", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    return w


# ------------------------------------------------------------------------------------------------ MIVAU (raw, con las claves de sellado de la base)
def _cod_mivau(nombre: str) -> str | None:
    return K.NOMBRE_A_PROV.get(nombre)


def valor_tasado_anual(provincias: list[str]) -> pd.DataFrame:
    """Valor tasado de la vivienda libre (€/m²), media anual de los cuatro trimestres (años completos; adenda 1.4 b), por provincia de
    entrenamiento. Origen: MIVAU (data/raw/mivau_valor_tasado_nacional_ccaa_prov.csv, desde 1995T1); Cantabria entra por su serie autonómica
    (comunidad uniprovincial). Sellado: valor_tasado|provincia|T (2026T2) y valor_tasado|provincia|A (2024)."""
    d = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    a = d[d["nivel"] == "provincia"].copy()
    a["cod"] = a["territorio"].map(_cod_mivau)
    b = d[(d["nivel"] == "ccaa") & (d["territorio"] == "Cantabria")].copy()
    b["cod"] = "39"
    d = pd.concat([a, b])
    d = d[d["cod"].notna() & d["cod"].isin(provincias)][["cod", "periodo", "valor"]]
    d = K.filtrar(d, "cod", "provincia", "periodo", "valor_tasado", "T")
    d["año"] = d["periodo"].str[:4].astype(int)
    g = d.groupby(["cod", "año"])["valor"].agg(["mean", "count"]).reset_index()
    g = g[g["count"] == 4]
    g["periodo"] = g["año"].astype(str)
    g = K.filtrar(g.rename(columns={"mean": "valor"})[["cod", "periodo", "valor"]], "cod", "provincia", "periodo", "valor_tasado", "A")
    w = g.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    return w


def _anual_mivau(variable_base: str, variable_sellado: str, provincias: list[str]) -> pd.DataFrame:
    d = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    d = d[d["serie"].str.startswith(variable_base + "_anual_")]
    a = d[d["nivel"] == "provincia"].copy()
    a["cod"] = a["territorio"].map(_cod_mivau)
    b = d[(d["nivel"] == "ccaa") & (d["territorio"].str.startswith("Cantabria"))].copy()
    b["cod"] = "39"
    d = pd.concat([a, b])
    d = d[d["cod"].notna() & d["cod"].isin(provincias)].copy()
    d["periodo"] = d["periodo"].astype(str)
    d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
    d = K.filtrar(d[["cod", "periodo", "valor"]], "cod", "provincia", "periodo", variable_sellado, "A")
    w = d.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="first")
    w.columns = [int(c) for c in w.columns]
    return w


def iniciadas_anual(provincias: list[str]) -> pd.DataFrame:
    """Viviendas libres iniciadas por año (MIVAU, desde 1991). Sellado: iniciadas_anual_tabla|provincia|A (2024)."""
    return _anual_mivau("viv_libres_iniciadas", "iniciadas_anual_tabla", provincias)


def terminadas_anual(provincias: list[str]) -> pd.DataFrame:
    return _anual_mivau("viv_libres_terminadas", "terminadas_anual_tabla", provincias)


# ------------------------------------------------------------------------------------------------ base del proyecto
def pob_prov(variable: str, provincias: list[str] | None = None) -> pd.DataFrame:
    """pob_total o pob_extranj por provincia (1 de enero; años 2002-2024), con el sellado de V18; solo las provincias de entrenamiento."""
    d = K.leer_hechos(variable, "provincia", "A")
    w = K.ancho(d)
    return w.loc[[p for p in (provincias or K.PROVINCIAS_ENTRENAMIENTO) if p in w.index]]


def deflactor_anual() -> pd.Series:
    """Deflactor (2020 = 100): media anual de los cuatro trimestres (años completos; clave T 2026T2 y clave A 2025, adenda 1.4 b)."""
    d = K.leer_hechos("deflactor", "nacional", "T")
    d["año"] = d["periodo"].str[:4].astype(int)
    g = d.groupby("año")["valor"].agg(["mean", "count"])
    g = g[g["count"] == 4]["mean"]
    tmp = pd.DataFrame({"cod": "00", "periodo": [str(a) for a in g.index], "valor": g.values})
    tmp = K.filtrar(tmp, "cod", "nacional", "periodo", "deflactor", "A")
    return pd.Series(tmp["valor"].values, index=[int(a) for a in tmp["periodo"]])


def serpavi_prov(tipologia: str = "tipologia=VC") -> pd.DataFrame:
    d = K.leer_hechos("serpavi_alquiler_m2_mediana", "provincia", "A", desag=tipologia)
    w = K.ancho(d)
    return w.loc[[p for p in K.PROVINCIAS_ENTRENAMIENTO if p in w.index]]


def ipva_prov() -> pd.DataFrame:
    d = K.leer_hechos("ipva_indice", "provincia", "A")
    w = K.ancho(d)
    return w.loc[[p for p in K.PROVINCIAS_ENTRENAMIENTO if p in w.index]]


def ipc_alquiler_prov() -> pd.DataFrame:
    d = K.leer_hechos("ipc_alquiler_indice", "provincia", "A")
    w = K.ancho(d)
    return w.loc[[p for p in K.PROVINCIAS_ENTRENAMIENTO if p in w.index]]


def ipv_ccaa_a() -> pd.DataFrame:
    d = K.leer_hechos("ipv", "ccaa", "A")
    return K.ancho(d)


__all__ = ["GRUPOS", "re"]
