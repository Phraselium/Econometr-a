"""V18 · fase 4 · E6 (obra nueva y alquileres cercanos) · datos del piloto de la provincia de València: edificios del Catastro (INSPIRE) con año de
construcción, secciones contiguas y SERPAVI por sección.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Lee data/raw/v11/catastro_inspire/original/BU_46*.zip (microdatos de edificio, una
descarga de 2026-08-21 con licencia de reutilización), asigna cada edificio a la sección INE 2025 que contiene su centro y aplica el sellado de V15 y V16
(secciones de distritos y municipios sellados fuera) y de v6. Nunca se abre data/sealed.
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_datos as D  # noqa: E402

RAIZ = K.RAIZ
ORIG = RAIZ / "data" / "raw" / "v11" / "catastro_inspire" / "original"
CORR = RAIZ / "data" / "raw" / "v11" / "catastro_inspire" / "correspondencia_dgc_ine.csv"
CACHE = RAIZ / "data" / "cache" / "v18_e6_edificios_46.parquet"
RX = {k: re.compile(v) for k, v in {
    "uso": r"<bu-ext2d:currentUse>([^<]+)<", "inm": r"<bu-ext2d:numberOfBuildingUnits>(\d+)<",
    "viv": r"<bu-ext2d:numberOfDwellings>(\d+)<", "anio": r"<bu-core2d:end>(\d{4})-", "estado": r"<bu-core2d:conditionOfConstruction>([^<]+)<",
    "lo": r"<gml:lowerCorner>([\d.]+) ([\d.]+)<", "up": r"<gml:upperCorner>([\d.]+) ([\d.]+)<"}.items()}
SEMILLA = K.SEMILLA


def _edificios_zip(zp: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zp) as z:
        n = next(x for x in z.namelist() if x.endswith(".building.gml"))
        texto = z.read(n).decode("utf-8", "replace")
    filas = []
    for b in texto.split("</bu-ext2d:Building>")[:-1]:
        g = {k: r.search(b) for k, r in RX.items()}
        if not (g["lo"] and g["up"]):
            continue
        filas.append((g["uso"].group(1) if g["uso"] else "", int(g["inm"].group(1)) if g["inm"] else 0, int(g["viv"].group(1)) if g["viv"] else 0,
                      int(g["anio"].group(1)) if g["anio"] else np.nan, g["estado"].group(1) if g["estado"] else "",
                      (float(g["lo"].group(1)) + float(g["up"].group(1))) / 2, (float(g["lo"].group(2)) + float(g["up"].group(2))) / 2))
    return pd.DataFrame(filas, columns=["uso", "inmuebles", "viviendas", "anio", "estado", "x", "y"])


def edificios_46() -> pd.DataFrame:
    """Edificios de los 92 municipios de la provincia de València del Catastro con sección INE asignada por posición (EPSG:25830). Caché en data/cache."""
    if CACHE.exists():
        return pd.read_parquet(CACHE)
    import geopandas as gpd
    corr = pd.read_csv(CORR, dtype=str)
    corr = corr[corr.cod_municipio_seleccion.str.startswith("46")]
    sec = gpd.read_parquet(D.GEO).to_crs(25830)[["cod_seccion", "cod_municipio", "geometry"]]
    partes = []
    for r in corr.itertuples():
        zp = ORIG / f"BU_{r.dgc}.zip"
        if not zp.exists():
            continue
        e = _edificios_zip(zp)
        p = gpd.GeoDataFrame(e, geometry=gpd.points_from_xy(e.x, e.y), crs=25830)
        j = gpd.sjoin(p, sec, how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].drop(columns=["index_right", "geometry"])
        j["dgc"] = r.dgc
        partes.append(j)
    out = pd.concat(partes, ignore_index=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(CACHE)
    return out


def secciones_provincia() -> pd.DataFrame:
    """Secciones INE de la provincia de València no selladas (v6, V15, V16), con centroide en EPSG:25830 y recuento antes y después del filtro."""
    import geopandas as gpd
    g = gpd.read_parquet(D.GEO)
    g = g[g.cod_provincia == "46"][["cod_seccion", "cod_distrito", "cod_municipio", "geometry"]].reset_index(drop=True)
    n0 = len(g)
    g = g[~D.sellado.mascara_v15_v16(g.cod_seccion.astype(str), "seccion").values]
    g = D.holdout.excluir_sellados_v6(g, "cod_seccion", "seccion").reset_index(drop=True)
    gp = g.to_crs(25830)
    g.attrs["n_total"], g.attrs["n_tras_sellado"] = n0, len(g)
    c = gp.geometry.representative_point()
    g["x"], g["y"] = c.x.values, c.y.values
    g["geom25830"] = gp.geometry.values
    return g


def adyacencias(secs: pd.DataFrame, todas: pd.DataFrame | None = None) -> dict[str, set[str]]:
    """Secciones contiguas (comparten frontera o se tocan con un margen de 1 m) dentro de TODAS las secciones de la provincia (incluidas las selladas: la contigüidad
    es geometría, no resultado). Devuelve cod_seccion -> conjunto de contiguas."""
    import geopandas as gpd
    g = gpd.read_parquet(D.GEO)
    g = g[g.cod_provincia == "46"][["cod_seccion", "geometry"]].reset_index(drop=True).to_crs(25830)
    g["geometry"] = g.geometry.buffer(1.0)
    j = gpd.sjoin(g, g, how="inner", predicate="intersects")
    j = j[j.cod_seccion_left != j.cod_seccion_right]
    adj: dict[str, set[str]] = {}
    for a, b in zip(j.cod_seccion_left, j.cod_seccion_right):
        adj.setdefault(a, set()).add(b)
    return adj


def serpavi_prov(cods, tip: str = "VC") -> pd.DataFrame:
    return D.serpavi(cods, tip)
