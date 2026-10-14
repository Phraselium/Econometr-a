"""V9-DATOS: Inside Airbnb (València, Barcelona, Madrid, Málaga, Mallorca).

Descarga las ediciones públicas actuales (listings.csv.gz; calendar y reviews solo se resumen y se borran) y, para
València y Barcelona, neighbourhoods.geojson. Agrega los anuncios a sección censal INE (CUSEC, 10 dígitos) mediante
join espacial con la cartografía INE de secciones censales, y a barrio (nombre de Inside Airbnb; NO es código INE).

Salida: data/raw/v9/insideairbnb/. Sin estimaciones. Uso:
    python3 src/v9/fetch_insideairbnb.py              # descarga y agrega
    python3 src/v9/fetch_insideairbnb.py --verificar  # sin red: comprueba ficheros y sha256 del manifiesto
Variable IAB_TMP: directorio de trabajo temporal para ficheros intermedios (calendar, reviews, zip INE).
"""
from __future__ import annotations

import csv
import hashlib
import os
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

import pandas as pd  # noqa: E402

from src.v9.comun import RAW9, descargar, registrar, sha256  # noqa: E402

FUENTE = "insideairbnb"
BASE = "https://data.insideairbnb.com"
OUT = RAW9 / FUENTE
TMP = Path(os.environ.get("IAB_TMP", Path(tempfile.gettempdir()) / "iab_v9"))
LICENCIA = "CC BY 4.0 (declarada en insideairbnb.com/get-the-data; no oficial)"
INE_URL = "https://www.ine.es/prodyser/cartografia/seccionado_2025.zip"
# ruta de edición (sin BASE) y código de provincia INE
CIUDADES = {
    "valencia": ("spain/vc/valencia/2026-09-20", "46"),
    "barcelona": ("spain/catalonia/barcelona/2026-09-17", "08"),
    "madrid": ("spain/comunidad-de-madrid/madrid/2026-09-17", "28"),
    "malaga": ("spain/andaluc%C3%ADa/malaga/2026-09-28", "29"),
    "mallorca": ("spain/islas-baleares/mallorca/2026-09-19", "07"),
}
BARRIOS = {"valencia", "barcelona"}


def _resumen_calendar(ruta: Path) -> pd.DataFrame:
    """Por listing y mes: noches registradas, noches disponibles y precio medio (sobre noches con precio)."""
    acum = []
    cabecera = pd.read_csv(ruta, nrows=0, compression="gzip").columns.tolist()
    con_precio = "price" in cabecera  # algunas ediciones públicas no traen precio en calendar
    cols = ["listing_id", "date", "available"] + (["price"] if con_precio else [])
    for ch in pd.read_csv(ruta, usecols=cols, dtype={c: str for c in cols}, chunksize=1_000_000):
        ch["mes"] = ch["date"].str[:7]
        ch["disp"] = (ch["available"] == "t").astype(int)
        if con_precio:
            ch["precio"] = pd.to_numeric(ch["price"].str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        else:
            ch["precio"] = float("nan")
        acum.append(ch.groupby(["listing_id", "mes"]).agg(
            noches_registradas=("disp", "size"), noches_disponibles=("disp", "sum"),
            precio_suma=("precio", "sum"), precio_n=("precio", "count")).reset_index())
    t = pd.concat(acum).groupby(["listing_id", "mes"]).sum().reset_index()
    t["precio_medio"] = (t["precio_suma"] / t["precio_n"]).round(2)
    return t.drop(columns=["precio_suma"])


def _resumen_reviews(ruta: Path) -> pd.DataFrame:
    """Por listing y mes: nº de reseñas."""
    acum = []
    for ch in pd.read_csv(ruta, usecols=["listing_id", "date"], dtype={"listing_id": str, "date": str},
                          chunksize=1_000_000):
        acum.append(ch.assign(mes=ch["date"].str[:7]).groupby(["listing_id", "mes"]).size()
                    .rename("n_resenas").reset_index())
    return pd.concat(acum).groupby(["listing_id", "mes"])["n_resenas"].sum().reset_index()


def _secciones(provincias: list[str]) -> "gpd.GeoDataFrame":  # noqa: F821
    import geopandas as gpd
    TMP.mkdir(parents=True, exist_ok=True)
    zip_ine = descargar(INE_URL, TMP / "seccionado_2025.zip")
    with zipfile.ZipFile(zip_ine) as zf:
        shps = [n for n in zf.namelist() if n.lower().endswith(".shp") and "secc" in n.lower()]
    if not shps:
        raise RuntimeError("no hay shapefile de secciones en el ZIP del INE")
    gdf = gpd.read_file(f"zip://{zip_ine}!{shps[0]}")
    gdf["CUSEC"] = gdf["CUSEC"].astype(str).str.zfill(10)
    gdf = gdf[gdf["CUSEC"].str[:2].isin(provincias)].copy()
    if gdf.crs is None:
        gdf = gdf.set_crs(4258)
    return gdf[["CUSEC", "geometry"]].to_crs(4326)


def _agregar(puntos, poligonos, clave: str) -> pd.DataFrame:
    """Join espacial (within; si cae en borde se toma la primera coincidencia) y agregación por clave."""
    import geopandas as gpd
    j = gpd.sjoin(puntos, poligonos, how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")]
    j["con_licencia"] = j["license"].notna() & (j["license"].astype(str).str.strip() != "")
    for tipo, col in [("Entire home/apt", "n_entire_home"), ("Private room", "n_private_room"),
                      ("Shared room", "n_shared_room"), ("Hotel room", "n_hotel_room")]:
        j[col] = j["room_type"].eq(tipo).astype(int)
    j["resenas_ltm"] = pd.to_numeric(j["number_of_reviews_ltm"], errors="coerce").fillna(0)
    g = j.groupby(clave, dropna=True).agg(
        n_anuncios=("id", "size"), n_entire_home=("n_entire_home", "sum"),
        n_private_room=("n_private_room", "sum"), n_shared_room=("n_shared_room", "sum"),
        n_hotel_room=("n_hotel_room", "sum"), n_con_licencia=("con_licencia", "sum"),
        disponibilidad_365_media=("availability_365", "mean"), resenas_ultimos_12m=("resenas_ltm", "sum"),
    ).reset_index()
    g["disponibilidad_365_media"] = g["disponibilidad_365_media"].round(1)
    return g, int(j[clave].notna().sum()), int(j[clave].isna().sum())


def main(verificar: bool = False) -> int:
    if verificar:
        return _verificar()
    import geopandas as gpd
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    provincias = [p for _, p in CIUDADES.values()]
    secc = _secciones(provincias)
    seccion_filas, barrio_filas, validacion = [], [], []
    for ciudad, (ruta_ed, prov) in CIUDADES.items():
        base = f"{BASE}/{ruta_ed}"
        fecha = ruta_ed.split("/")[-1]
        url_list = f"{base}/data/listings.csv.gz"
        ruta_list = OUT / f"listings_{ciudad}_{fecha}.csv.gz"
        descargar(url_list, ruta_list)
        registrar(FUENTE, ruta_list, url_list, fecha, fecha, "anuncio (lat/lon)", LICENCIA, True,
                  "ficheros >50 MB se excluyen de git (ver .gitignore del proyecto)")
        df = pd.read_csv(ruta_list, compression="gzip", dtype={"id": str, "host_id": str}, low_memory=False)
        # proxy de recuento: visualisations/listings.csv (mismo universo que la página de la ciudad)
        url_vis = f"{base}/visualisations/listings.csv"
        n_vis = sum(1 for _ in open(descargar(url_vis, TMP / f"{ciudad}_{fecha}_vis_listings.csv"), encoding="utf-8",
                                    errors="replace")) - 1
        for url, dest, nivel, nota in [(f"{base}/data/calendar.csv.gz", TMP / f"{ciudad}_{fecha}_calendar.csv.gz",
                                        "listing x mes", "resumen; crudo no guardado (tamaño)"),
                                       (f"{base}/data/reviews.csv.gz", TMP / f"{ciudad}_{fecha}_reviews.csv.gz",
                                        "listing x mes", "resumen; crudo no guardado (tamaño)")]:
            descargar(url, dest)
            res = _resumen_calendar(dest) if "calendar" in dest.name else _resumen_reviews(dest)
            nombre = "calendar_resumen" if "calendar" in dest.name else "reviews_resumen"
            salida = OUT / f"{nombre}_{ciudad}_{fecha}.csv.gz"
            res.to_csv(salida, index=False, compression="gzip")
            registrar(FUENTE, salida, url, fecha, fecha, nivel, LICENCIA, True, nota)
            dest.unlink()
        puntos = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]), crs=4326)
        g_sec, n_dentro, n_fuera = _agregar(puntos, secc, "CUSEC")
        g_sec.insert(0, "edicion", fecha)
        g_sec.insert(0, "ciudad", ciudad)
        seccion_filas.append(g_sec.rename(columns={"CUSEC": "cod_seccion"}))
        if ciudad in BARRIOS:
            url_geo = f"{base}/visualisations/neighbourhoods.geojson"
            ruta_geo = OUT / f"neighbourhoods_{ciudad}_{fecha}.geojson"
            descargar(url_geo, ruta_geo)
            registrar(FUENTE, ruta_geo, url_geo, fecha, fecha, "barrio (Inside Airbnb; no es código INE)", LICENCIA,
                      True)
            barrios = gpd.read_file(ruta_geo)[["neighbourhood", "geometry"]].to_crs(4326)
            g_b, _, _ = _agregar(puntos, barrios, "neighbourhood")
            g_b.insert(0, "edicion", fecha)
            g_b.insert(0, "ciudad", ciudad)
            barrio_filas.append(g_b.rename(columns={"neighbourhood": "barrio_iab"}))
        validacion.append({"ciudad": ciudad, "edicion": fecha, "filas_listings": len(df),
                           "filas_visualisations_listings": n_vis, "dentro_seccion": n_dentro,
                           "fuera_seccion": n_fuera, "sin_coordenadas": int(df["latitude"].isna().sum())})
        print(validacion[-1], flush=True)
    seccion = pd.concat(seccion_filas, ignore_index=True)
    ruta_sec = OUT / "insideairbnb_seccion.csv.gz"
    seccion.to_csv(ruta_sec, index=False, compression="gzip")
    registrar(FUENTE, ruta_sec, INE_URL + " (secciones) + " + BASE, "2026", "2025-09 a 2026-09", "sección INE (CUSEC)",
              LICENCIA, True, f"join espacial con seccionado_2025.zip del INE (sha256 zip "
              f"{sha256(TMP / 'seccionado_2025.zip')}); solo provincias {', '.join(provincias)}")
    ruta_b = OUT / "insideairbnb_barrio.csv.gz"
    pd.concat(barrio_filas, ignore_index=True).to_csv(ruta_b, index=False, compression="gzip")
    registrar(FUENTE, ruta_b, BASE, "2026", "2026-09", "barrio Inside Airbnb (no INE)", LICENCIA, True,
              "solo València y Barcelona")
    ruta_v = OUT / "validacion_insideairbnb.csv"
    pd.DataFrame(validacion).to_csv(ruta_v, index=False)
    registrar(FUENTE, ruta_v, BASE, "2026", "2026-09", "control", LICENCIA, True, "recuentos de control")
    return 0


def _verificar() -> int:
    man = OUT / "_manifest.csv"
    if not man.exists():
        print("falta _manifest.csv")
        return 1
    errores = 0
    with open(man, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta = RAIZ / fila["fichero"]
            if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                print("FALLO", fila["fichero"])
                errores += 1
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
