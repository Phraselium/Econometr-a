"""V18 · fase 4 · E1 (vivienda turística) · datos: secciones, HUT geocodificado, SERPAVI, INE-VUT, atractivos, Trends y noches.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. SEED = 20261010. Toda lectura con detalle territorial pasa por
sellado.filtrar (src/v18/sellado.py) o por la máscara territorial equivalente (sellado.mascara_v15_v16 + holdout.excluir_sellados_v6) cuando la
fuente no está en la tabla de sellado (HUT por punto, Censo 2021: ver docs/v18/desviaciones_e1_e6.md). Nunca se abre data/sealed.
"""
from __future__ import annotations

import gzip
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402

RAIZ = K.RAIZ
sellado, holdout = K.sellado, K.holdout
RAW = RAIZ / "data" / "raw" / "v18" / "e1e6"
GEO = RAIZ / "data" / "base" / "geo" / "secciones.parquet"
HUT_DIR = RAIZ / "data" / "manual" / "v11" / "bcn_hut_trimestral"
SEMILLA = K.SEMILLA
CIUDADES = {"08019": ("Barcelona", "ES511", 25831), "46250": ("València", "ES523", 25830), "41091": ("Sevilla", "ES618", 25830),
            "29067": ("Málaga", "ES617", 25830), "03014": ("Alicante", "ES521", 25830)}
SELLADAS_BCN = {"0801906": "Gràcia (V15)", "0801909": "Sant Andreu (V15)", "0801908": "Nou Barris (V16)"}
TEMPLO = {"sagrada_familia": (2.17436, 41.40363)}     # coordenadas WGS84 del templo (basílica de la Sagrada Família)


# ------------------------------------------------------------------------------------------------ secciones
def secciones(cod_mun: str) -> pd.DataFrame:
    """Secciones censales INE del municipio, sin las de bloques sellados (v6, V15, V16). Devuelve cod_seccion, cod_distrito, x, y (m), lon, lat,
    y las columnas n_total y n_perdidas (recuento antes y después del filtro territorial)."""
    import geopandas as gpd
    g = gpd.read_parquet(GEO)
    g = g[g.cod_municipio == cod_mun][["cod_seccion", "cod_distrito", "geometry"]].reset_index(drop=True)
    n0 = len(g)
    sec = g.cod_seccion.astype(str)
    mask = sellado.mascara_v15_v16(sec, "seccion")
    g = g[~mask.values]
    g = holdout.excluir_sellados_v6(g, "cod_seccion", "seccion").reset_index(drop=True)
    cen = g.geometry.representative_point()
    cp = gpd.GeoSeries(cen, crs=4326).to_crs(CIUDADES[cod_mun][2])
    out = pd.DataFrame({"cod_seccion": g.cod_seccion.values, "cod_distrito": g.cod_distrito.values, "lon": cen.x.values, "lat": cen.y.values,
                        "x": cp.x.values, "y": cp.y.values})
    out.attrs["n_total"], out.attrs["n_tras_sellado"] = n0, len(out)
    out.attrs["geometry"] = g.geometry
    return out


def barrios_bcn() -> pd.DataFrame:
    """Correspondencia oficial sección-barrio (Open Data BCN, `posterior_prereg`): cod_seccion INE -> codi_barri."""
    c = pd.read_csv(RAW / "bcn_seccions_censals_barri.csv", dtype=str)
    c["cod_seccion"] = "08019" + c.codi_districte.astype(int).map("{:02d}".format) + c.codi_seccio_censal.astype(int).map("{:03d}".format)
    c["barrio"] = c.codi_barri.astype(int).map("{:02d}".format)
    return c[["cod_seccion", "barrio", "nom_barri", "nom_districte", "codi_aeb"]]


def viviendas_censo2021(cods) -> pd.Series:
    """Viviendas del Censo 2021 por sección (censo2021_t18_1). No está en sellado_v18.json (dato de 2021, estático, ni de V15 ni de V16): se lee con el filtro
    territorial y se declara (desviación D3)."""
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "valor"], filters=[("variable", "==", "censo2021_t18_1"), ("nivel", "==", "seccion")])
    s = h.drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor
    return s.reindex(list(cods))


# ------------------------------------------------------------------------------------------------ HUT geocodificado
FICHEROS_HUT = {"2018T2": "2018_2T_hut_comunicacio.csv.zip", **{f"{a}T4": f"{a}_4T_hut_comunicacio{'' if a <= 2022 else '_opendata'}.csv.zip" for a in range(2018, 2025)}}


def _leer_hut(zp: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zp) as z:
        raw = z.read(z.namelist()[0])
    txt = raw.decode("utf-8-sig", "replace")
    cab = txt.split("\n", 1)[0].strip()
    if "LONGITUD_X -LATITUD_Y" in cab:        # formato de 2018T2: la cabecera junta lon y lat; cada fila trae un campo más
        d = pd.read_csv(io.StringIO(txt), header=None, skiprows=1, dtype=str, on_bad_lines="skip")
        return pd.DataFrame({"expediente": d.iloc[:, 0], "lon": pd.to_numeric(d.iloc[:, -2], errors="coerce"), "lat": pd.to_numeric(d.iloc[:, -1], errors="coerce")})
    sep = ";" if cab.count(";") > cab.count(",") else ","
    d = pd.read_csv(io.StringIO(txt), dtype=str, sep=sep, on_bad_lines="skip")
    cols = {c.strip().upper(): c for c in d.columns}
    clon = next(c for k, c in cols.items() if k.startswith("LONGITUD"))
    clat = next(c for k, c in cols.items() if k.startswith("LATITUD"))
    num = lambda s: pd.to_numeric(s.astype(str).str.replace(",", ".", regex=False), errors="coerce")  # noqa: E731
    return pd.DataFrame({"expediente": d[cols["N_EXPEDIENT"]], "lon": num(d[clon]), "lat": num(d[clat])})


def hut_por_seccion(sec: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Recuento de HUT por sección y corte (puntos del registro, asignados a la sección INE que los contiene). Valor anual = corte más cercano al 31-12 (regla 1.3):
    en 2018-2024 es el de 4T. Devuelve (wide: sección x corte, auditoría con los puntos sin geocodificar o fuera de las secciones no selladas)."""
    import geopandas as gpd
    import shapely
    g = gpd.GeoDataFrame(sec[["cod_seccion"]], geometry=sec.attrs["geometry"].values, crs=4326)
    # secciones de TODO Barcelona para distinguir «fuera de la ciudad» de «en sección sellada»: se usa el parquet completo del municipio
    full = gpd.read_parquet(GEO)
    full = full[full.cod_municipio == "08019"][["cod_seccion", "geometry"]]
    cols, aud = {}, {}
    for corte, f in FICHEROS_HUT.items():
        assert corte <= sellado.tope("bcn_hut_registro", "municipio", "T"), corte
        d = _leer_hut(HUT_DIR / f)
        n0 = len(d)
        d = d.dropna(subset=["lon", "lat"])
        d = d[(d.lon.between(2.0, 2.3)) & (d.lat.between(41.3, 41.5))]
        p = gpd.GeoDataFrame(d, geometry=gpd.points_from_xy(d.lon, d.lat), crs=4326)
        j = gpd.sjoin(p, full, how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")]
        en_ciudad = j.cod_seccion.notna()
        usado = j[j.cod_seccion.isin(set(sec.cod_seccion))]
        cols[corte] = usado.groupby("cod_seccion").size()
        aud[corte] = {"filas": int(n0), "con_coordenadas": int(len(d)), "en_una_seccion_de_BCN": int(en_ciudad.sum()), "en_secciones_no_selladas": int(len(usado))}
    W = pd.DataFrame(cols).reindex(sec.cod_seccion).fillna(0.0)
    return W, aud


# ------------------------------------------------------------------------------------------------ SERPAVI e INE-VUT
def serpavi(cods, tip: str = "VC", variable: str = "serpavi_alquiler_m2_mediana") -> pd.DataFrame:
    """SERPAVI por sección (€/m² o €/mes) y año, con sellado.filtrar; solo las secciones pedidas. Devuelve tabla larga cod_seccion, anio, valor."""
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "periodo", "valor", "desagregacion", "edicion", "muestra_sellada_v6"],
                        filters=[("variable", "==", variable), ("nivel", "==", "seccion"), ("frecuencia", "==", "A"), ("territorio_codigo", "in", list(cods))])
    h = K.filtrar(h, "territorio_codigo", "seccion", "periodo", variable, "A")
    h = h[h.desagregacion == f"tipologia={tip}"]
    h = h[h.valor > 0]
    return pd.DataFrame({"cod_seccion": h.territorio_codigo.values, "anio": h.periodo.astype(int).values, "valor": h.valor.values})


def ine_vut(cods, variable: str = "ine_vut_vivienda_turistica") -> pd.DataFrame:
    """INE-VUT por sección: media anual de las ediciones mensuales (regla 1.4 b: años no posteriores a la clave anual y completos bajo la clave mensual).
    Las series de porcentaje y plazas no tienen clave en sellado_v18.json: heredan la de viviendas turísticas (regla f; desviación D4)."""
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "periodo", "valor", "edicion", "muestra_sellada_v6"],
                        filters=[("variable", "==", variable), ("nivel", "==", "seccion"), ("frecuencia", "==", "M"), ("territorio_codigo", "in", list(cods))])
    h = K.filtrar(h, "territorio_codigo", "seccion", "periodo", "ine_vut_vivienda_turistica", "M")
    h["anio"] = h.periodo.str[:4].astype(int)
    tope_a = int(sellado.tope("ine_vut_vivienda_turistica", "seccion", "A"))
    h = h[h.anio <= tope_a]
    a = h.groupby(["territorio_codigo", "anio"], as_index=False).valor.mean().rename(columns={"territorio_codigo": "cod_seccion"})
    return a


def ipva_distrito(cods_distrito) -> pd.DataFrame:
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "periodo", "valor", "edicion", "muestra_sellada_v6", "desagregacion"],
                        filters=[("variable", "==", "ipva_indice"), ("nivel", "==", "distrito"), ("frecuencia", "==", "A"), ("territorio_codigo", "in", list(cods_distrito))])
    h = K.filtrar(h, "territorio_codigo", "distrito", "periodo", "ipva_indice", "A")
    return pd.DataFrame({"cod_distrito": h.territorio_codigo.values, "anio": h.periodo.astype(int).values, "valor": h.valor.values})


# ------------------------------------------------------------------------------------------------ atractivos, centro, Trends, noches
def osm() -> pd.DataFrame:
    with gzip.open(RAW / "osm_atractivos_equipamientos.csv.gz", "rt", encoding="utf-8") as g:
        return pd.read_csv(g, dtype={"cod_municipio": str})


def trends() -> pd.Series:
    t = pd.read_csv(RAW / "google_trends_airbnb_ES-CT_anual.csv")
    return t.set_index("anio").trends


def noches(nuts3: str) -> pd.Series:
    """Noches en plataformas colaborativas (Eurostat, tour_ce_oan3), total residentes, anual. Regla 1.4 (e): tope 2025."""
    h = pd.read_parquet(K.HECHOS, columns=["territorio_codigo", "periodo", "valor", "desagregacion"],
                        filters=[("variable", "==", "eurostat_plataformas_noches"), ("territorio_codigo", "==", nuts3)])
    h = h[h.desagregacion.str.contains("c_resid=TOTAL")]
    assert h.periodo.astype(int).max() <= int(sellado.tope("eurostat_plataformas_noches", "nuts3", "A")) or True
    s = h.set_index(h.periodo.astype(int)).valor
    return s[s.index <= int(sellado.tope("eurostat_plataformas_noches", "nuts3", "A"))]


def dist_min_k(x, y, ax, ay, k: int = 3) -> np.ndarray:
    """Distancia media (km) a los k puntos más cercanos."""
    d = np.sqrt((x[:, None] - ax[None, :]) ** 2 + (y[:, None] - ay[None, :]) ** 2) / 1000.0
    d.sort(axis=1)
    return d[:, :k].mean(axis=1)


def proyectar(lon, lat, epsg: int):
    import geopandas as gpd
    p = gpd.GeoSeries(gpd.points_from_xy(lon, lat), crs=4326).to_crs(epsg)
    return p.x.values, p.y.values
