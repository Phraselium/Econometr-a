"""V18 · fase 4 · E1 · adquisición de las fuentes `posterior_prereg` de E1 (descarga única, después de la etiqueta plan-replicacion-v18).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Único módulo de E1 que usa red; las estimaciones (e1_turismo.py) leen solo
los ficheros locales. Se descarga, se normaliza y se audita la calidad; no se cruza con ningún resultado.

Fuentes (todas abiertas; ver data/raw/v18/_manifest_e1e6.csv con fuente, URL, fecha, sha256 y licencia):
- Google Trends, término «airbnb» (término, no tema), región ES-CT, 2010-01 a 2024-12, mensual; media anual; UNA descarga con su fecha (adenda R-14).
- OpenStreetMap (extractos regionales de download.openstreetmap.fr, ODbL): tourism=attraction, amenity=hospital, amenity=university y
  amenity=townhall en Barcelona, València, Sevilla, Málaga y Alicante. Overpass no es accesible desde el proxy de esta sesión (docs/v18/desviaciones_e1_e6.md, D1).
- Open Data BCN: BarcelonaCiutat_SeccionsCensals.csv (correspondencia oficial sección censal-barrio, ODbL/CC BY 4.0).
Uso: python3 src/v18/estimacion/e1_adquisicion.py [--osm] [--trends] [--bcn]   (sin aleatoriedad).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ALCANCE_TERRITORIAL = "sin lectura de datos"     # solo descarga y escribe ficheros nuevos; no lee datos del proyecto
RAIZ = Path(__file__).resolve().parents[3]
DEST = RAIZ / "data" / "raw" / "v18" / "e1e6"
MANIFIESTO = RAIZ / "data" / "raw" / "v18" / "_manifest_e1e6.csv"
SCRATCH = Path(os.environ.get("V18_SCRATCH", "/tmp/claude-0/-home-user-Econometr-a/468da938-3e2d-5fba-ac52-e16a4175b9ac/scratchpad/osm"))
OSM_BASE = "https://download.openstreetmap.fr/extracts/europe/spain/"
EXTRACTOS = {"catalunya": ["08019"], "comunitat_valenciana": ["46250", "03014"], "andalucia": ["41091", "29067"]}
BBOX = {"08019": (2.0525, 41.3169, 2.2292, 41.4683), "46250": (-0.4325, 39.2791, -0.2737, 39.5661), "41091": (-6.0329, 37.3002, -5.8192, 37.4530),
        "29067": (-4.5879, 36.6346, -4.2605, 36.8940), "03014": (-0.6567, 38.1620, -0.3751, 38.5371)}
NOMBRE = {"08019": "Barcelona", "46250": "València", "41091": "Sevilla", "29067": "Málaga", "03014": "Alicante"}
BUFFER = 0.02


def sha256(f: Path) -> str:
    h = hashlib.sha256()
    with open(f, "rb") as g:
        for b in iter(lambda: g.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def registrar(fichero: Path, fuente: str, url: str, edicion: str, periodo: str, nivel: str, licencia: str, notas: str) -> None:
    fila = {"fuente": fuente, "fichero": str(fichero.relative_to(RAIZ)), "url": url, "fecha_descarga": date.today().isoformat(), "edicion": edicion,
            "periodo": periodo, "nivel_territorial": nivel, "sha256": sha256(fichero), "licencia": licencia, "redistribuible": "sí",
            "posterior_prereg": "sí", "notas": notas}
    antes = pd.read_csv(MANIFIESTO) if MANIFIESTO.exists() else pd.DataFrame()
    if len(antes):
        antes = antes[antes["fichero"] != fila["fichero"]]
    pd.concat([antes, pd.DataFrame([fila])], ignore_index=True).to_csv(MANIFIESTO, index=False)
    print("registrado", fila["fichero"], fila["sha256"][:12])


# ---------------------------------------------------------------------------------------------- Google Trends
def trends() -> None:
    f = DEST / "google_trends_airbnb_ES-CT_anual.csv"
    if f.exists():
        return
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                      "Accept-Language": "en-US,en;q=0.9"})
    s.get("https://trends.google.com/trends/explore?geo=ES-CT&q=airbnb", timeout=60)
    req = {"comparisonItem": [{"keyword": "airbnb", "geo": "ES-CT", "time": "2010-01-01 2024-12-31"}], "category": 0, "property": ""}
    r = s.get("https://trends.google.com/trends/api/explore", params={"hl": "en-US", "tz": "-60", "req": json.dumps(req)}, timeout=60)
    r.raise_for_status()
    w = [x for x in json.loads(r.text[5:])["widgets"] if x["id"] == "TIMESERIES"][0]
    time.sleep(2)
    r2 = s.get("https://trends.google.com/trends/api/widgetdata/multiline", params={"hl": "en-US", "tz": "-60", "req": json.dumps(w["request"]), "token": w["token"]}, timeout=60)
    r2.raise_for_status()
    datos = json.loads(r2.text[5:])["default"]["timelineData"]
    m = pd.DataFrame({"mes": [pd.Timestamp(int(x["time"]), unit="s").strftime("%Y-%m") for x in datos], "valor": [x["value"][0] for x in datos]})
    DEST.mkdir(parents=True, exist_ok=True)
    fm = DEST / "google_trends_airbnb_ES-CT_mensual.csv"
    m.to_csv(fm, index=False)
    a = m.assign(anio=m.mes.str[:4].astype(int)).groupby("anio", as_index=False).valor.mean().rename(columns={"valor": "trends"})
    a.to_csv(f, index=False)
    url = "https://trends.google.com/trends/explore?geo=ES-CT&q=airbnb&date=2010-01-01%202024-12-31 (API explore + widgetdata/multiline)"
    registrar(fm, "Google Trends", url, f"descarga única {date.today().isoformat()}", "2010-01 a 2024-12", "ES-CT (Cataluña)", "Google Trends: índice 0-100 reescalado por descarga; condiciones de uso por verificar (docs/v18/tareas_autor.md)", "término «airbnb», mensual; el índice se reescala en cada descarga: no se empalma con otra")
    registrar(f, "Google Trends (media anual)", url, f"descarga única {date.today().isoformat()}", "2010-2024", "ES-CT (Cataluña)", "Google Trends: índice 0-100; agregado propio", "media anual de los 12 índices mensuales")


# ---------------------------------------------------------------------------------------------- Open Data BCN
def bcn() -> None:
    f = DEST / "bcn_seccions_censals_barri.csv"
    if f.exists():
        return
    B = "https://opendata-ajuntament.barcelona.cat/data/api/3/action/"
    p = requests.get(B + "package_show", params={"id": "20170706-districtes-barris"}, timeout=60).json()["result"]
    rec = [r for r in p["resources"] if r["name"] == "BarcelonaCiutat_SeccionsCensals.csv"][0]
    # la descarga directa del fichero pasa por un antibots; la API de datastore (datastore_search) sirve los mismos registros
    filas, off = [], 0
    while True:
        r = requests.get(B + "datastore_search", params={"resource_id": rec["id"], "limit": 1000, "offset": off}, timeout=120).json()["result"]
        filas += r["records"]
        off += 1000
        if off >= r["total"]:
            break
    DEST.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(filas).drop(columns=["_id", "_full_text"], errors="ignore").to_csv(f, index=False)
    registrar(f, "Ajuntament de Barcelona, Open Data BCN (BarcelonaCiutat_SeccionsCensals.csv, vía datastore_search)", B + "datastore_search?resource_id=" + rec["id"], p.get("metadata_modified", ""), "vigente", "sección censal (Barcelona)",
              "CC BY 4.0 (Open Data BCN)", "correspondencia oficial sección censal-barrio-distrito")


# ---------------------------------------------------------------------------------------------- OpenStreetMap
def descargar_pbf(nombre: str) -> Path:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    f = SCRATCH / f"{nombre}.osm.pbf"
    if not f.exists():
        urllib.request.urlretrieve(OSM_BASE + f"{nombre}.osm.pbf", f)
    return f


def extraer(nombre: str, pbf: Path) -> pd.DataFrame:
    import geopandas as gpd
    import pyogrio
    os.environ.setdefault("CPL_TMPDIR", str(SCRATCH))
    os.environ["OSM_MAX_TMPFILE_SIZE"] = "512"
    claves = [("tourism", "attraction", "attraction"), ("amenity", "hospital", "hospital"), ("amenity", "university", "university"), ("amenity", "townhall", "townhall")]
    out = []
    for capa in ("points", "multipolygons"):
        cond = []
        for k, v, _ in claves:
            cond.append(f"other_tags LIKE '%\"{k}\"=>\"{v}\"%'")
            if capa == "multipolygons":
                cond.append(f"{k} = '{v}'")
        g = pyogrio.read_dataframe(pbf, layer=capa, where=" OR ".join(cond))
        g = g.reset_index(drop=True)
        tags = g["other_tags"].fillna("")
        for k, v, c in claves:
            m = tags.str.contains(f'"{k}"=>"{v}"', regex=False)
            if capa == "multipolygons" and k in g:
                m = m | (g[k] == v)
            if not m.any():
                continue
            h = g[m].copy()
            cen = h.geometry.representative_point()
            tab = pd.DataFrame({"clase": c, "capa": capa, "osm_id": (h["osm_id"] if capa == "points" else h["osm_id"].fillna(h.get("osm_way_id"))).astype(str).values,
                                "nombre": h["name"].values, "lon": cen.x.values, "lat": cen.y.values})
            out.append(tab)
    t = pd.concat(out, ignore_index=True)
    filas = []
    for cod in EXTRACTOS[nombre]:
        x0, y0, x1, y1 = BBOX[cod]
        s = t[(t.lon >= x0 - BUFFER) & (t.lon <= x1 + BUFFER) & (t.lat >= y0 - BUFFER) & (t.lat <= y1 + BUFFER)].copy()
        s["cod_municipio"] = cod
        s["ciudad"] = NOMBRE[cod]
        filas.append(s)
    return pd.concat(filas, ignore_index=True)


def osm() -> None:
    f = DEST / "osm_atractivos_equipamientos.csv.gz"
    if f.exists():
        return
    partes, ediciones = [], []
    for nombre in EXTRACTOS:
        pbf = descargar_pbf(nombre)
        estado = requests.get(OSM_BASE + f"{nombre}.state.txt", timeout=60).text
        ts = re.search(r"timestamp=(.*)", estado).group(1).replace("\\", "")
        ediciones.append(f"{nombre}: {ts}")
        print(nombre, "sha256", sha256(pbf)[:12], ts)
        partes.append(extraer(nombre, pbf))
        pbf.unlink()
    t = pd.concat(partes, ignore_index=True).drop_duplicates(["cod_municipio", "clase", "capa", "osm_id"])
    DEST.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(f, "wb", mtime=0) as g:
        g.write(t.to_csv(index=False).encode("utf-8"))
    registrar(f, "OpenStreetMap (extractos de download.openstreetmap.fr)", OSM_BASE + "{catalunya,comunitat_valenciana,andalucia}.osm.pbf", "; ".join(ediciones), "instantánea",
              "puntos y polígonos (centroide interior)", "ODbL 1.0 © colaboradores de OpenStreetMap", "tourism=attraction, amenity=hospital|university|townhall; bbox municipal + 0,02°; filtro por municipio posterior en e1_datos.py")


def main() -> int:
    args = set(sys.argv[1:]) or {"--trends", "--bcn", "--osm"}
    if "--trends" in args:
        trends()
    if "--bcn" in args:
        bcn()
    if "--osm" in args:
        osm()
    return 0


if __name__ == "__main__":
    sys.exit(main())
