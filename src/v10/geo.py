"""V10-B1 · geometrías de la base (parte de `make base`; sin red).

Entradas: data/raw/v10/geo/seccionado_2025.zip (INE, secciones censales a 1-1-2025, ETRS89 UTM 30N) y las capas del
Ajuntament de València (barrios, distritos; CC BY 4.0), descargadas por src/v10/fetch_geo.py.

Salidas (data/base/geo/):
  secciones.parquet, municipios.parquet, provincias.parquet, ccaa.parquet   GeoParquet (EPSG:4326), simplificadas a
      ~10 m (secciones y municipios) o ~200 m (provincias y CCAA); los niveles superiores se obtienen disolviendo
      las secciones por código INE (sin cruce por nombre)
  barrios_valencia.parquet   barrios de València con código 46250+distrito(2)+barrio(2)
  correspondencia_seccion_barrio_valencia.csv   peso por área de cada sección INE en cada barrio (y error)
  web/*.geojson   versiones muy simplificadas para la web (España CCAA y provincias; municipios de la Comunitat
      Valenciana; secciones y barrios de València)
Canarias se mantiene en su posición real (la web la recoloca en un recuadro).
"""
from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ENT = RAIZ / "data" / "raw" / "v10" / "geo"
SAL = RAIZ / "data" / "base" / "geo"
UTM = 25830
FUENTES = {
    "secciones": "INE, Cartografía digitalizada de secciones censales a 1-1-2025 (seccionado_2025.zip); reutilización con cita",
    "barrios": "Ajuntament de València, geoportal (capa 224 barrios, 225 distritos); CC BY 4.0",
}


def leer_secciones() -> gpd.GeoDataFrame:
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(ENT / "seccionado_2025.zip") as z:
        for n in z.namelist():
            if n.split(".")[-1].lower() in ("shp", "shx", "dbf", "prj", "cpg"):
                (Path(tmp) / Path(n).name).write_bytes(z.read(n))
        shp = next(Path(tmp).glob("*.shp"))
        g = gpd.read_file(shp)
    g = g.to_crs(UTM)
    g["cod_seccion"] = g.CUSEC.astype(str).str.zfill(10)
    g["cod_municipio"] = g.CUMUN.astype(str).str.zfill(5)
    g["cod_distrito"] = g.cod_municipio + g.CDIS.astype(str).str.zfill(2)
    g["cod_provincia"] = g.CPRO.astype(str).str.zfill(2)
    g["cod_ccaa"] = g.CCA.astype(str).str.zfill(2)
    g["nombre_municipio"] = g.NMUN
    return g[["cod_seccion", "cod_distrito", "cod_municipio", "cod_provincia", "cod_ccaa", "nombre_municipio", "geometry"]]


def disolver(g: gpd.GeoDataFrame, clave: str, extra: list[str]) -> gpd.GeoDataFrame:
    d = g.dissolve(by=clave, aggfunc="first")[extra + ["geometry"]].reset_index()
    d["geometry"] = d.geometry.buffer(0)
    return d


def simplificar(g: gpd.GeoDataFrame, tol: float) -> gpd.GeoDataFrame:
    g = g.copy()
    g["geometry"] = g.geometry.simplify(tol, preserve_topology=True)
    return g.to_crs(4326)


def guardar_geojson(g: gpd.GeoDataFrame, ruta: Path, decimales: int = 4) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    js = json.loads(g.to_json(drop_id=True))
    def red(c):
        return [red(x) for x in c] if isinstance(c, list) and c and isinstance(c[0], list) else [round(v, decimales) for v in c]
    for f in js["features"]:
        f["geometry"]["coordinates"] = red(f["geometry"]["coordinates"])
    ruta.write_text(json.dumps(js, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def barrios_valencia() -> gpd.GeoDataFrame:
    b = gpd.read_file(ENT / "vlc_barrios.geojson").to_crs(UTM)
    b["cod_distrito"] = "46250" + b.coddistrit.astype(int).astype(str).str.zfill(2)
    b["cod_barrio"] = b.cod_distrito + b.codbarrio.astype(int).astype(str).str.zfill(2)
    b = b.dissolve(by="cod_barrio", aggfunc="first").reset_index()
    return b[["cod_barrio", "cod_distrito", "nombre", "geometry"]]


def main() -> dict:
    SAL.mkdir(parents=True, exist_ok=True)
    s = leer_secciones()
    mun = disolver(s, "cod_municipio", ["cod_provincia", "cod_ccaa", "nombre_municipio"])
    prov = disolver(s, "cod_provincia", ["cod_ccaa"])
    ccaa = disolver(s, "cod_ccaa", [])
    for nombre, g, tol in (("secciones", s, 10), ("municipios", mun, 10), ("provincias", prov, 200), ("ccaa", ccaa, 200)):
        out = simplificar(g, tol)
        out["fuente"] = FUENTES["secciones"]
        out.to_parquet(SAL / f"{nombre}.parquet", compression="zstd")
    b = barrios_valencia()
    bo = b.to_crs(4326)
    bo["fuente"] = FUENTES["barrios"]
    bo.to_parquet(SAL / "barrios_valencia.parquet", compression="zstd")
    # correspondencia sección INE -> barrio por área (València)
    sv = s[s.cod_municipio == "46250"][["cod_seccion", "geometry"]]
    inter = gpd.overlay(sv, b[["cod_barrio", "geometry"]], how="intersection", keep_geom_type=True)
    inter["area"] = inter.area
    inter = inter[inter.area > 1]
    inter["peso_area"] = inter.area / inter.groupby("cod_seccion").area.transform("sum")
    corr = inter[["cod_seccion", "cod_barrio", "peso_area"]].sort_values(["cod_seccion", "peso_area"], ascending=[True, False])
    corr["peso_area"] = corr.peso_area.round(6)
    corr["seccion_en_un_barrio"] = corr.groupby("cod_seccion").peso_area.transform("max") >= 0.95
    corr.to_csv(SAL / "correspondencia_seccion_barrio_valencia.csv", index=False)
    # web
    w = SAL / "web"
    guardar_geojson(simplificar(ccaa, 1500).assign(nombre=ccaa.cod_ccaa), w / "ccaa.geojson", 3)
    guardar_geojson(simplificar(prov, 1500), w / "provincias.geojson", 3)
    cv = mun[mun.cod_ccaa == "10"]
    guardar_geojson(simplificar(cv, 120), w / "municipios_cv.geojson", 4)
    guardar_geojson(simplificar(s[s.cod_municipio == "46250"].drop(columns="nombre_municipio"), 8), w / "secciones_valencia.geojson", 5)
    guardar_geojson(simplificar(b, 8), w / "barrios_valencia.geojson", 5)
    n_sec = corr.cod_seccion.nunique()
    resumen = {"secciones": len(s), "municipios": len(mun), "provincias": len(prov), "ccaa": len(ccaa),
               "barrios_valencia": len(b), "secciones_valencia": n_sec,
               "secciones_valencia_en_un_barrio_95pct": int(corr.drop_duplicates("cod_seccion").seccion_en_un_barrio.sum())}
    pd.Series(resumen).to_json(SAL / "resumen_geo.json", force_ascii=False, indent=1)
    return resumen


if __name__ == "__main__":
    print(main())
