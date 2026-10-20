"""V18 · fase 4 · E1 · construcción de los paneles de sección × año (Barcelona y las otras cuatro ciudades no selladas).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin resultados: solo datos y variables derivadas (exposición, instrumento, distancia al centro).
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e1_datos as D  # noqa: E402

ANIOS = list(range(2011, 2025))
GRANDES_ATRACTIVOS = ("sagrada", "güell", "guell", "batll")      # E1-R2-v3: Sagrada Família, Park Güell y Casa Batlló
NOMBRE_CLAVE = {"08019": ["barcelona"], "46250": ["valencia"], "41091": ["sevilla"], "29067": ["malaga"], "03014": ["alicante", "alacant"]}
EXCLUIR_AYTO = ("distrit", "districte", "junta", "oficina", "tenencia", "tinencia", "registro", "registre", "juzgado", "pedania", "casa consist")


def _norm(s) -> str:
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def centro_ayuntamiento(cod: str, osm: pd.DataFrame, secs_completas: "pd.DataFrame") -> dict:
    """Sede del ayuntamiento (amenity=townhall de OSM): la de nombre del municipio sin «distrito/junta/oficina…»; con varias, el medoide. Devuelve lon, lat y la sección que la contiene."""
    t = osm[(osm.cod_municipio == cod) & (osm.clase == "townhall")].copy()
    t["n"] = t.nombre.map(_norm)
    c = t[t.n.map(lambda s: any(k in s for k in NOMBRE_CLAVE[cod]) and not any(e in s for e in EXCLUIR_AYTO))]
    fuente = "OSM amenity=townhall (nombre del municipio)"
    if len(c) == 0:
        return {"lon": np.nan, "lat": np.nan, "fuente": "sin sede en OSM"}
    if len(c) > 1:
        xy = np.column_stack(D.proyectar(c.lon.values, c.lat.values, D.CIUDADES[cod][2]))
        dm = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1)).sum(1)
        c = c.iloc[[int(np.argmin(dm))]]
        fuente += f"; {len(t)} candidatos, medoide"
    r = c.iloc[0]
    return {"lon": float(r.lon), "lat": float(r.lat), "nombre": r.nombre, "fuente": fuente}


def _centroide_seccion_que_contiene(lon, lat, cod: str):
    import geopandas as gpd
    g = gpd.read_parquet(D.GEO)
    g = g[g.cod_municipio == cod][["cod_seccion", "geometry"]]
    p = gpd.GeoDataFrame(geometry=gpd.points_from_xy([lon], [lat]), crs=4326)
    j = gpd.sjoin(p, g, how="left", predicate="within")
    if j.cod_seccion.isna().all():
        return None, None
    cs = j.cod_seccion.iloc[0]
    geom = g[g.cod_seccion == cs].geometry.iloc[0]
    c = geom.representative_point()
    return cs, (c.x, c.y)


def prox_atractivos(x, y, cod: str, osm: pd.DataFrame, k: int = 3, excluir_grandes: bool = False) -> np.ndarray:
    a = osm[(osm.cod_municipio == cod) & (osm.clase == "attraction")].copy()
    if excluir_grandes:
        a = a[~a.nombre.fillna("").map(_norm).map(lambda s: any(g in s for g in GRANDES_ATRACTIVOS))]
    ax, ay = D.proyectar(a.lon.values, a.lat.values, D.CIUDADES[cod][2])
    d = D.dist_min_k(x, y, ax, ay, k)
    return -np.log(np.maximum(d, 0.05)), len(a)


def prox_equip(x, y, cod: str, osm: pd.DataFrame, clase: str, k: int = 3) -> np.ndarray:
    a = osm[(osm.cod_municipio == cod) & (osm.clase == clase)]
    ax, ay = D.proyectar(a.lon.values, a.lat.values, D.CIUDADES[cod][2])
    return -np.log(np.maximum(D.dist_min_k(x, y, ax, ay, min(k, len(a))), 0.05))


def seccion_base(cod: str, osm: pd.DataFrame) -> pd.DataFrame:
    """Una fila por sección no sellada del municipio: geografía, distancia al centro, proximidades (atractivos y placebos) y viviendas del Censo 2021."""
    sec = D.secciones(cod)
    viv = D.viviendas_censo2021(sec.cod_seccion)
    sec["viv"] = viv.values
    c = centro_ayuntamiento(cod, osm, sec)
    cs, cxy = (None, None)
    if np.isfinite(c["lon"]):
        cs, cxy = _centroide_seccion_que_contiene(c["lon"], c["lat"], cod)
    if cxy is None:
        a = osm[(osm.cod_municipio == cod) & (osm.clase == "attraction")]
        lon0, lat0 = a.lon.median(), a.lat.median()
        c = {"lon": float(lon0), "lat": float(lat0), "fuente": "mediana de los atractivos (sin sede de ayuntamiento localizable)"}
        cxy = (lon0, lat0)
        cs = None
    cx, cy = D.proyectar([cxy[0]], [cxy[1]], D.CIUDADES[cod][2])
    sec["dist_c"] = np.sqrt((sec.x - cx[0]) ** 2 + (sec.y - cy[0]) ** 2) / 1000.0
    sec["prox3"], n_att = prox_atractivos(sec.x.values, sec.y.values, cod, osm, 3)
    sec["prox5"], _ = prox_atractivos(sec.x.values, sec.y.values, cod, osm, 5)
    sec["prox3_sin"], _ = prox_atractivos(sec.x.values, sec.y.values, cod, osm, 3, excluir_grandes=True)
    sec["prox_hosp"] = prox_equip(sec.x.values, sec.y.values, cod, osm, "hospital")
    sec["prox_univ"] = prox_equip(sec.x.values, sec.y.values, cod, osm, "university")
    sec["cod_mun"] = cod
    sec.attrs["centro"] = {**c, "seccion_centro": cs}
    sec.attrs["n_atractivos"] = n_att
    return sec


def panel_largo(cod: str, osm: pd.DataFrame, trends: pd.Series, anios: list[int] = ANIOS) -> pd.DataFrame:
    """Panel sección × año 2011-2024: ln SERPAVI (VC, VU, €/mes), HUT por 100 viviendas (Barcelona 2018-2024), INE-VUT (porcentaje, plazas), noches de la NUTS3 y Trends."""
    sec = seccion_base(cod, osm)
    sp = D.serpavi(sec.cod_seccion, "VC")
    spu = D.serpavi(sec.cod_seccion, "VU")
    spm = D.serpavi(sec.cod_seccion, "VC", "serpavi_alquiler_mes_mediana")
    base = sec.assign(key=1).merge(pd.DataFrame({"anio": anios, "key": 1}), on="key").drop(columns="key")
    base = base.merge(sp.rename(columns={"valor": "ym2"}), on=["cod_seccion", "anio"], how="left")
    base = base.merge(spu.rename(columns={"valor": "ym2_vu"}), on=["cod_seccion", "anio"], how="left")
    base = base.merge(spm.rename(columns={"valor": "ymes"}), on=["cod_seccion", "anio"], how="left")
    base["y"], base["y_vu"], base["y_mes"] = np.log(base.ym2), np.log(base.ym2_vu), np.log(base.ymes)
    pct = D.ine_vut(sec.cod_seccion, "ine_vut_porcentaje_vivienda_turistica").rename(columns={"valor": "vut_pct"})
    npl = D.ine_vut(sec.cod_seccion, "ine_vut_plazas").rename(columns={"valor": "vut_plazas"})
    base = base.merge(pct, on=["cod_seccion", "anio"], how="left").merge(npl, on=["cod_seccion", "anio"], how="left")
    base["vut_plazas100"] = 100.0 * base.vut_plazas / base.viv
    nch = D.noches(D.CIUDADES[cod][1]) / 1e6
    base["noches"] = base.anio.map(nch)
    base["trends"] = base.anio.map(trends)
    base["u"] = pd.factorize(base.cod_seccion)[0]
    base["t"] = base.anio - min(anios)
    base["w"] = base.viv
    return base.attrs.update(sec.attrs) or base


def añadir_hut(base: pd.DataFrame, cod: str = "08019") -> tuple[pd.DataFrame, dict]:
    """Añade HUT por 100 viviendas del Censo 2021 (valor anual = corte de 4T de 2018 a 2024; dosis de 2018T2) y el barrio oficial."""
    sec = base.drop_duplicates("cod_seccion")[["cod_seccion", "cod_distrito", "lon", "lat", "x", "y", "viv"]].reset_index(drop=True)
    sec.attrs["geometry"] = base.attrs["geometry"]
    W, aud = D.hut_por_seccion(sec)
    out = base.copy()
    for a in range(2018, 2025):
        h = 100.0 * W[f"{a}T4"] / sec.set_index("cod_seccion").viv
        out[f"hut{a}"] = out.cod_seccion.map(h)
    out["hut"] = np.nan
    for a in range(2018, 2025):
        m = out.anio == a
        out.loc[m, "hut"] = out.loc[m, f"hut{a}"]
    out["dosis0"] = out.cod_seccion.map(100.0 * W["2018T2"] / sec.set_index("cod_seccion").viv)
    out["n_hut_2018T2"] = out.cod_seccion.map(W["2018T2"])
    b = D.barrios_bcn()
    out = out.merge(b, on="cod_seccion", how="left")
    out["cl"] = pd.factorize(out.barrio)[0]
    return out, aud
