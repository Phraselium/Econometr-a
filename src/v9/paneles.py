"""V9 COMPLETO · paneles de los diseños D1-D7 (solo construcción de datos; ninguna estimación).

Todo cruce territorial es por código INE. Las funciones leen data/raw (solo lectura) y devuelven DataFrames:
  incasol()            municipio × trimestre (Cataluña): contratos nuevos y renta media ponderada (2007T1-2026T1)
  tratamientos_cat()   municipio → fechas de la Ley 11/2020 y de las zonas tensionadas (BOE)
  emal()               municipio × trimestre (Euskadi, >20.000 hab.): fianzas nuevas y renta media
  tratamientos_pv()    municipio → fecha de efecto de la zona tensionada (BOE)
  hut_cat()            municipio × año: HUT y plazas (IDESCAT) y población (padrón)
  fianzas_gva_cp()     código postal × año: fianzas y fianza media (GVA)
  vut_gva_cp()         código postal: stock VUT en los cortes 2025-01-26 y 2026-10-14
  viviendas_cp()       código postal: viviendas (censo 2021 por sección × reparto sección-CP del callejero)
  padron_nac()         municipio o provincia × año × nacionalidad (2003-2022)
  valor_tasado_prov()  provincia × año: valor tasado medio (media de trimestres)
  ipc_alquiler_prov()  provincia × año: IPC de alquiler (media de meses)
  europa()             país × trimestre/mes: HPI, IPCA alquiler, cuota a tipo variable y shocks JK
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
RAW9 = RAW / "v9"
SEED = 20261010
# Euro área con shocks del BCE: países con cuota de tipo variable desde 2003-2007 (exposición previa)
ZONA_EURO = ["AT", "BE", "CY", "DE", "EE", "ES", "FI", "FR", "GR", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PT", "SI", "SK"]


def trimestre(fecha: str) -> str:
    t = pd.Timestamp(fecha)
    return f"{t.year}T{t.quarter}"


def tindex(per: pd.Series) -> pd.Series:
    """'2020T3' → índice entero de trimestres (año*4 + t-1)."""
    return per.str[:4].astype(int) * 4 + per.str[-1].astype(int) - 1


# ------------------------------------------------------------------------------------------------ D1 / D2 Cataluña
def _agrega_incasol(d: pd.DataFrame, cod: str, per: str, n: str, r: str) -> pd.DataFrame:
    d = d.copy()
    d["n"] = pd.to_numeric(d[n], errors="coerce")
    d["r"] = pd.to_numeric(d[r].astype(str).str.replace(",", "."), errors="coerce") if r else np.nan
    d["nr"] = np.where(d.r.notna(), d.n, 0.0)
    d["rn"] = d.r.fillna(0) * d.nr
    g = d.groupby([d[cod].str.zfill(5).rename("cod"), d[per].rename("periodo")]).agg(
        contratos=("n", "sum"), n_con_renta=("nr", "sum"), suma=("rn", "sum")).reset_index()
    g["renta_media"] = g.suma / g.n_con_renta.where(g.n_con_renta > 0)
    return g.drop(columns="suma")


def incasol(frecuencia: str = "T") -> pd.DataFrame:
    """Fianzas Incasòl por municipio (fichero V9). Frecuencia «T»: trimestral 2019T1-2026T1. «A»: anual 2007-2025 (los
    municipios solo tienen datos anuales antes de 2019; coincide con el fichero de v3). Cada municipio y periodo está en
    un solo tramo de precio (el tramo clasifica al municipio): contratos y renta media son los de esa fila."""
    i = pd.read_csv(RAW9 / "incasol/incasol_qww9-bvhh_actual.csv.gz", dtype=str)
    i = i[i.ambit_territorial.str.lower().str.startswith("municipi") & (i.posterior_prereg.str.lower() != "true")]
    if frecuencia == "T":
        q = i[i.periodo_iso.str.fullmatch(r"\d{4}T[1-4]")]
        g = _agrega_incasol(q, "codi_territorial", "periodo_iso", "habitatges", "renda")
        g["t"] = tindex(g.periodo)
        return g
    a9 = i[i.periodo_iso.str.fullmatch(r"\d{4}_gener-desembre")].assign(anio=lambda x: x.periodo_iso.str[:4])
    g = _agrega_incasol(a9, "codi_territorial", "anio", "habitatges", "renda")
    g["anio"] = g.periodo.astype(int)
    return g


def tratamientos_cat() -> pd.DataFrame:
    c = pd.read_csv(RAW / "v3/cataluna_contencion_rentas_v3.csv", dtype=str)
    ley = c[c.regimen == "ley11_2020"].cod_ine.str.zfill(5).unique()
    z = pd.read_csv(RAW9 / "regulacion/zonas_tensionadas_v9.csv", dtype=str)
    z = z[z.ccaa == "Cataluña"]
    out = pd.DataFrame({"cod": sorted(set(ley) | set(z.cod_ine_municipio.str.zfill(5)))})
    out["ley11"] = out.cod.isin(ley)
    zt = z.assign(cod=z.cod_ine_municipio.str.zfill(5)).groupby("cod").fecha_efecto.min()
    out["zt_fecha"] = out.cod.map(zt)
    # primer trimestre tratado: el trimestre que contiene la fecha de efecto si empieza antes de su mitad; si no, el siguiente
    def primer_t(f):
        if pd.isna(f):
            return np.nan
        d = pd.Timestamp(f)
        q0 = d.year * 4 + d.quarter - 1
        inicio = pd.Timestamp(year=d.year, month=3 * (d.quarter - 1) + 1, day=1)
        return q0 if (d - inicio).days < 45 else q0 + 1
    out["zt_t0"] = out.zt_fecha.map(primer_t)
    return out


def emal() -> pd.DataFrame:
    e = pd.read_csv(RAW9 / "emal/emal_largo.csv", dtype=str)
    e = e[e.codigo_ine.notna() & e.periodo.str.fullmatch(r"\d{4}T[1-4]") & (e.tipo_contrato == "nuevo")
          & (e.grupo == "Municipios de más de 20.000")]
    e = e[e.variable.isin(["n_fianzas", "renta_mensual_eur"])]
    e["valor"] = pd.to_numeric(e.valor, errors="coerce")
    w = e.pivot_table(index=["codigo_ine", "periodo"], columns="variable", values="valor", aggfunc="first").reset_index()
    w = w.rename(columns={"codigo_ine": "cod", "n_fianzas": "contratos", "renta_mensual_eur": "renta_media"})
    w["t"] = tindex(w.periodo)
    return w


def tratamientos_pv() -> pd.DataFrame:
    z = pd.read_csv(RAW9 / "regulacion/zonas_tensionadas_v9.csv", dtype=str)
    z = z[z.ccaa == "País Vasco"]
    d = z.assign(cod=z.cod_ine_municipio.str.zfill(5)).groupby("cod").fecha_efecto.min().reset_index()
    d["zt_t0"] = d.fecha_efecto.map(lambda f: pd.Timestamp(f).year * 4 + pd.Timestamp(f).quarter - 1
                                   + (0 if (pd.Timestamp(f) - pd.Timestamp(year=pd.Timestamp(f).year, month=3 * (pd.Timestamp(f).quarter - 1) + 1, day=1)).days < 45 else 1))
    return d


def padron_nac(nivel: str = "municipio", tipo: str = "nacionalidad") -> pd.DataFrame:
    d = pd.read_csv(RAW9 / f"ine_padron_nacionalidad/padron_{tipo}_2003_2022.csv.gz",
                    dtype={"anio": int, "cod_provincia": str, "cod_municipio": str, tipo: str, "poblacion": float})
    d = d[d.cod_municipio.notna()]
    if nivel == "provincia":
        d = d.groupby(["anio", "cod_provincia", tipo], as_index=False).poblacion.sum()
    return d


def hut_cat() -> pd.DataFrame:
    t = pd.read_csv(RAW9 / "cat_turisme/idescat_allotjaments_municipi.csv.gz", dtype={"cod_ine": str})
    t = t[t.tipo == "habitatges_us_turistic"].pivot_table(index=["cod_ine", "anio"], columns="medida", values="valor",
                                                          aggfunc="first").reset_index()
    t.columns = ["cod", "anio", "hut", "hut_plazas"]
    p = padron_nac("municipio")
    p = p[p.nacionalidad == "Total"][["anio", "cod_municipio", "poblacion"]].rename(columns={"cod_municipio": "cod"})
    return t.merge(p, on=["cod", "anio"], how="left")


# ------------------------------------------------------------------------------------------------ D3 Comunitat Valenciana
def fianzas_gva_cp() -> pd.DataFrame:
    partes = []
    for f in sorted((RAW / "v5").glob("gva_fianzas_20*.csv")):
        d = pd.read_csv(f, sep=";", dtype=str)
        d["importe"] = pd.to_numeric(d.importe_fianza.str.replace(",", "."), errors="coerce")
        d = d[d.cp.str.fullmatch(r"\d{5}", na=False) & d.importe.between(50, 20000)]
        d["cod_mun"] = d.cod_provincia.str.zfill(2) + d.cod_municipio.str.zfill(3)
        g = d.groupby(["anyo_datos", "cp"]).agg(fianzas=("importe", "size"), fianza_media=("importe", "mean"),
                                                fianza_mediana=("importe", "median"), cod_mun=("cod_mun", lambda s: s.mode().iat[0]))
        partes.append(g.reset_index())
    out = pd.concat(partes, ignore_index=True).rename(columns={"anyo_datos": "anio"})
    out["anio"] = out.anio.astype(int)
    return out


def vut_gva_cp() -> pd.DataFrame:
    v = pd.read_csv(RAW9 / "gva_vut/gva_vut_panel_cp.csv", dtype=str)
    v = v[(v.tipo == "corte") & v.cp.str.fullmatch(r"\d{5}", na=False)]
    w = v.pivot_table(index="cp", columns="fecha", values="stock", aggfunc=lambda s: pd.to_numeric(s).sum()).reset_index()
    w.columns.name = None
    return w.rename(columns={"2025-01-26": "vut_2025", "2026-10-14": "vut_2026"}).fillna({"vut_2025": 0, "vut_2026": 0})


def viviendas_cp() -> pd.DataFrame:
    """Viviendas (t18_1) y hogares (t21_1) del censo 2021 por sección, repartidos entre códigos postales según los
    portales del callejero de 2025 (tabla sección × CP); coordenadas del CP = centroides de sección ponderados."""
    c = pd.read_csv(RAW9 / "ine_callejero/seccion_cp_2025.csv.gz", dtype={"seccion": str, "cp": str, "cod_municipio": str})
    c["peso"] = c.portales_aprox / c.groupby("seccion").portales_aprox.transform("sum")
    s = pd.read_csv(RAW / "v3/ine_v3_censo2021_seccion_indicadores.csv.gz", dtype=str, usecols=["serie", "valor", "codigo"])
    s = s[s.serie.isin(["t18_1", "t21_1"])].pivot_table(index="codigo", columns="serie", values="valor",
                                                       aggfunc=lambda x: pd.to_numeric(x).sum()).reset_index()
    s.columns = ["seccion", "viviendas", "hogares"]
    m = c.merge(s, on="seccion", how="left")
    import geopandas as gpd
    g = gpd.read_parquet(RAIZ / "data/base/geo/secciones.parquet").to_crs(3035)   # metros (ETRS89-LAEA)
    cen = g.geometry.centroid
    m = m.merge(pd.DataFrame({"seccion": g.cod_seccion, "lon": cen.x, "lat": cen.y}), on="seccion", how="left")
    m["viv_w"] = m.viviendas * m.peso
    m["hog_w"] = m.hogares * m.peso
    agg = {"viviendas": ("viv_w", "sum"), "hogares": ("hog_w", "sum"), "cod_municipio": ("cod_municipio", lambda x: x.mode().iat[0])}
    if "lon" in m:
        m["lon_w"], m["lat_w"] = m.lon * m.viv_w, m.lat * m.viv_w
        agg |= {"lon_w": ("lon_w", "sum"), "lat_w": ("lat_w", "sum")}
    out = m.groupby("cp").agg(**agg).reset_index()
    if "lon_w" in out:
        out["lon"], out["lat"] = out.lon_w / out.viviendas, out.lat_w / out.viviendas
        out = out.drop(columns=["lon_w", "lat_w"])
    return out


# ------------------------------------------------------------------------------------------------ D4 provincias
def valor_tasado_prov() -> pd.DataFrame:
    v = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv", dtype=str)
    v = v[v.nivel == "provincia"]
    v["anio"] = v.periodo.str[:4].astype(int)
    v["valor"] = pd.to_numeric(v.valor, errors="coerce")
    return v


def ipc_alquiler_prov() -> pd.DataFrame:
    v = pd.read_csv(RAW / "ine_v2_ipc_alquiler_prov.csv", dtype=str)
    v = v[v.nivel == "provincia"]
    v["anio"] = v.periodo.str[:4].astype(int)
    v["valor"] = pd.to_numeric(v.valor, errors="coerce")
    return v


# ------------------------------------------------------------------------------------------------ D5 zona euro
def europa() -> dict[str, pd.DataFrame]:
    jk = pd.read_csv(RAW / "v8/jk_shocks_ecb_mensual.csv", dtype=str)
    jk["valor"] = pd.to_numeric(jk.valor, errors="coerce")
    jk = jk.pivot_table(index="periodo", columns="serie", values="valor").reset_index()
    rai = pd.read_csv(RAW9 / "bce_rai/bce_rai_svlhphh.csv.gz", dtype=str)
    rai["valor"] = pd.to_numeric(rai.valor, errors="coerce")
    hicp = pd.read_csv(RAW9 / "eurostat_alquiler/prc_hicp_minr_cp041_mensual.csv.gz", dtype=str)
    hicp = hicp[hicp.posterior_prereg.str.lower() != "true"]
    hicp["valor"] = pd.to_numeric(hicp.indice_2015, errors="coerce")
    hpi = pd.read_csv(RAW / "v8/eurostat_prc_hpi_q_multi.csv", dtype=str)
    return {"jk": jk, "rai": rai, "hicp": hicp, "hpi": hpi}


def es_codigo(s: str) -> bool:
    return bool(re.fullmatch(r"\d{5}", s or ""))
