"""D3 v3: datos para replicar García-López et al. (2020) en Barcelona y medir la caída de anuncios 2025-2026.

Fuentes:
  1. Inside Airbnb (CC BY 4.0). Índice oficial de instantáneas (página get-the-data, datos Gatsby públicos).
     Por cada instantánea española se descarga data/listings.csv.gz en memoria, se agrega por barrio/neighbourhood
     y tipo de habitación y se DESCARTA el listado bruto (no se guarda). Solo se conservan agregados.
  2. Registro de Turisme de Catalunya (HUT), Socrata t2h3-cgys. El dataset publicado solo contiene el estado actual
     (sin fechas de alta/baja): se agrega como fotografía por municipio y, en Barcelona, por código postal.
  3-5. Opendata BCN, Google Trends y atractivos turísticos: no accesibles de forma legítima en esta sesión
     (ver docs/v3/fuentes_fallidas.md). No se descarga nada de ellos aquí.

Salida: data/raw/v3/airbnb_insideairbnb_agregados_v3.csv.gz y data/raw/v3/hut_registro_turismo_cat_v3.csv.gz
Formato largo: fecha, periodo, serie, valor, unidad, fuente, url, territorio, nivel, codigo.
Caché: si el fichero de salida existe no se vuelve a descargar (FORCE=1 para rehacer).
Cuadre: la suma de los barrios/neighbourhoods (incluido SIN_DATO) debe igualar el total de la ciudad en cada instantánea.
"""
from __future__ import annotations

import datetime as dt
import io
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils_fetch as uf  # noqa: E402

IA_PAGEDATA = "https://insideairbnb.com/page-data/get-the-data/page-data.json"
IA_SQ = "https://insideairbnb.com/page-data/sq/d/{h}.json"
IA_NAME = "v3/airbnb_insideairbnb_agregados_v3.csv.gz"
IA_FUENTE = "Inside Airbnb (CC BY 4.0; insideairbnb.com/get-the-data)"
HUT_ID = "t2h3-cgys"
HUT_BASE = f"https://analisi.transparenciacatalunya.cat/resource/{HUT_ID}.json"
HUT_META = f"https://analisi.transparenciacatalunya.cat/api/views/{HUT_ID}.json"
HUT_NAME = "v3/hut_registro_turismo_cat_v3.csv.gz"
HUT_FUENTE = "Registre de Turisme de Catalunya - Establiments d'allotjament turístic (Socrata t2h3-cgys, Dept. Empresa i Treball; licencia Ver términos de uso)"
FALLIDAS = uf.ROOT / "docs" / "v3" / "fuentes_fallidas.md"

ROOM_MAP = {"Entire home/apt": "entera", "Private room": "habitacion"}
SLEEP = 1.5  # cortesía entre peticiones a data.insideairbnb.com


def registrar_fallida(fuente: str, url: str, error: str, alternativa: str) -> None:
    """Añade una fila a docs/v3/fuentes_fallidas.md si no está ya (idempotente)."""
    fecha = dt.date.today().isoformat()
    linea = f"| {fuente} | {url} | {error} | {alternativa} | {fecha} |"
    txt = FALLIDAS.read_text(encoding="utf-8") if FALLIDAS.exists() else ""
    if url in txt and fuente in txt:
        return
    with open(FALLIDAS, "a", encoding="utf-8") as fh:
        if not txt.strip():
            fh.write("# Fuentes fallidas v3\n\n| Fuente | URL | Error | Alternativa | Fecha |\n|---|---|---|---|---|\n")
        fh.write(linea + "\n")
    print(f"[fallida] {fuente}: {error}")


def _get_bytes(url: str, tries: int = 4, timeout: int = 300) -> bytes:
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, headers=uf.HEADERS, timeout=timeout)
            r.raise_for_status()
            if not r.content:
                raise RuntimeError("respuesta vacía")
            return r.content
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"{url}: {last}")


# ---------------------------------------------------------------- Inside Airbnb
def indice_espana() -> pd.DataFrame:
    """Lista de instantáneas españolas publicadas en el índice oficial de Inside Airbnb."""
    pagina = uf.get(IA_PAGEDATA, as_json=True)
    hashes = pagina.get("staticQueryHashes", [])
    datasets = None
    for h in hashes:
        sq = uf.get(IA_SQ.format(h=h), as_json=True)
        if "data" in sq and "allData" in sq["data"]:
            datasets = sq["data"]["allData"]["datasets"]
            break
    if datasets is None:
        raise RuntimeError("No se encontró el índice de instantáneas (allData) en get-the-data")
    df = pd.DataFrame([d for d in datasets if d.get("country") == "Spain"])
    df["fecha_captura"] = pd.to_datetime(df["publishDate"]).dt.date
    return df.sort_values(["city", "publishDate"]).reset_index(drop=True)


def agregar_instantanea(city: str, publish: str, root: str, fecha: dt.date) -> tuple[list[dict], dict]:
    """Descarga listings.csv.gz en memoria, agrega y descarta el bruto. Devuelve filas y cifras de cuadre."""
    url = f"{root}{publish}/data/listings.csv.gz"
    content = _get_bytes(url)
    cab = pd.read_csv(io.BytesIO(content), compression="gzip", nrows=0).columns
    usar = [c for c in ["id", "room_type", "neighbourhood_cleansed", "neighbourhood",
                        "neighbourhood_group_cleansed", "last_review"] if c in cab]
    if "room_type" not in usar:
        raise RuntimeError(f"{url}: sin columna room_type")
    lst = pd.read_csv(io.BytesIO(content), compression="gzip", usecols=usar, low_memory=False)
    del content  # listado bruto descartado
    barrio_col = "neighbourhood_cleansed" if "neighbourhood_cleansed" in lst.columns else None
    if barrio_col is None:
        lst["_b"] = lst.get("neighbourhood", pd.Series(index=lst.index, dtype=object))
        barrio_col = "_b"
    lst["barrio"] = lst[barrio_col].fillna("SIN_DATO").astype(str).str.strip()
    lst["barrio"] = lst["barrio"].replace("", "SIN_DATO")
    lst["tipo"] = lst["room_type"].map(ROOM_MAP).fillna("otros")
    lr = pd.to_datetime(lst["last_review"], errors="coerce") if "last_review" in lst.columns else pd.Series(pd.NaT, index=lst.index)
    corte = pd.Timestamp(fecha) - pd.Timedelta(days=365)
    lst["resena12"] = (lr >= corte).astype(int)
    lst["_uno"] = 1

    por_b = lst.groupby("barrio").agg(
        total=("_uno", "sum"), resena12=("resena12", "sum")).reset_index()
    por_t = lst.pivot_table(index="barrio", columns="tipo", values="_uno", aggfunc="sum", fill_value=0).reset_index()
    tab = por_b.merge(por_t, on="barrio", how="left").fillna(0)
    for c in ["entera", "habitacion", "otros"]:
        if c not in tab.columns:
            tab[c] = 0

    ciudad = {"total": int(lst.shape[0]), "resena12": int(lst["resena12"].sum()),
              "entera": int((lst["tipo"] == "entera").sum()),
              "habitacion": int((lst["tipo"] == "habitacion").sum()),
              "otros": int((lst["tipo"] == "otros").sum())}
    filas = []
    slug = city.lower()
    series = {"total": "IA_anuncios_activos_total", "entera": "IA_anuncios_activos_entera",
              "habitacion": "IA_anuncios_activos_habitacion", "otros": "IA_anuncios_activos_otros_tipos",
              "resena12": "IA_anuncios_con_resena_12m"}
    base = dict(fecha=fecha.isoformat(), periodo=fecha.isoformat(), fuente=IA_FUENTE, url=url)
    for _, r in tab.iterrows():
        nivel = "NEIGHBOURHOOD"
        for k, s in series.items():
            filas.append({**base, "serie": f"{s}__{slug}", "valor": float(r[k]),
                          "unidad": "anuncios", "territorio": r["barrio"], "nivel": nivel,
                          "codigo": r["barrio"]})
    for k, s in series.items():
        filas.append({**base, "serie": f"{s}__{slug}", "valor": float(ciudad[k]), "unidad": "anuncios",
                      "territorio": city, "nivel": "CIUDAD", "codigo": slug})
    # Cuadre: suma de barrios == total de ciudad (no se rellena ni se redistribuye nada)
    suma = {k: float(tab[k].sum()) for k in series}
    cuadre = {k: suma[k] == ciudad[k] for k in series}
    cuadre_tipos = (ciudad["entera"] + ciudad["habitacion"] + ciudad["otros"]) == ciudad["total"]
    info = {"ciudad": city, "fecha": fecha.isoformat(), "n_barrios": int(tab.shape[0]),
            "total": ciudad["total"], "cuadre_barrios": all(cuadre.values()),
            "cuadre_tipos": cuadre_tipos, "columnas": ",".join(usar)}
    return filas, info


def fetch_airbnb() -> Path:
    if uf.cached(IA_NAME):
        return uf.RAW / IA_NAME
    idx = indice_espana()
    print(f"[ia] {len(idx)} instantáneas españolas en el índice; ciudades: {sorted(idx['city'].unique())}")
    todas, infos = [], []
    for _, r in idx.iterrows():
        try:
            filas, info = agregar_instantanea(r["city"], r["publishDate"], r["dataRoot"], r["fecha_captura"])
            todas += filas
            infos.append(info)
            print(f"[ia] {info['ciudad']} {info['fecha']}: {info['n_barrios']} barrios, total {info['total']}, "
                  f"cuadre_barrios={info['cuadre_barrios']}, cuadre_tipos={info['cuadre_tipos']}")
        except Exception as e:  # noqa: BLE001
            registrar_fallida(f"Inside Airbnb {r['city']} {r['publishDate']}",
                              f"{r['dataRoot']}{r['publishDate']}/data/listings.csv.gz", str(e)[:200],
                              "reintentar con FORCE=1; si persiste, excluir la instantánea y anotarlo")
        time.sleep(SLEEP)
    if not todas:
        raise RuntimeError("Ninguna instantánea de Inside Airbnb se pudo agregar")
    df = pd.DataFrame(todas)
    df["valor"] = df["valor"].astype(float)
    (uf.RAW / "v3").mkdir(parents=True, exist_ok=True)
    uf.save(df, IA_NAME, IA_FUENTE)
    return uf.RAW / IA_NAME


# ---------------------------------------------------------------- Registro de Turismo (HUT)
def _soql(params: dict) -> list[dict]:
    return uf.get(HUT_BASE, params=params, as_json=True)


def fetch_hut() -> Path:
    if uf.cached(HUT_NAME):
        return uf.RAW / HUT_NAME
    meta = uf.get(HUT_META, as_json=True)
    f_ver = dt.datetime.fromtimestamp(int(meta["rowsUpdatedAt"]), dt.timezone.utc).date()
    url = f"https://analisi.transparenciacatalunya.cat/d/{HUT_ID}"
    base = dict(fecha=f_ver.isoformat(), periodo=f_ver.isoformat(), fuente=HUT_FUENTE, url=url)
    filas = []

    # Por municipio y tipo (incluye todos los tipos de establecimiento; HUT = "Habitatges d'ús turístic")
    grupos = _soql({"$select": "codi_municipi_idescat,municipi,tipus_establiment,estat,"
                               "count(*) as n,sum(total_places) as plazas",
                    "$group": "codi_municipi_idescat,municipi,tipus_establiment,estat",
                    "$limit": 50000})
    tot_n = _soql({"$select": "tipus_establiment,estat,count(*) as n,sum(total_places) as plazas", "$group": "tipus_establiment,estat",
                   "$limit": 50000})
    for g in grupos:
        ine5 = str(g.get("codi_municipi_idescat") or "")[:5] or "SIN_DATO"
        tipo = re.sub(r"\W+", "_", g.get("tipus_establiment", "SIN_DATO")).strip("_")
        est = re.sub(r"\W+", "_", g.get("estat", "SIN_DATO")).strip("_")
        for sufijo, unidad, col in [("establecimientos", "establecimientos", "n"), ("plazas", "plazas", "plazas")]:
            filas.append({**base, "serie": f"HUT_{sufijo}_{tipo}_{est}", "valor": float(g.get(col) or 0),
                          "unidad": unidad, "territorio": g.get("municipi", "SIN_DATO"), "nivel": "MUNICIPIO",
                          "codigo": ine5})

    # Cuadre: suma de municipios == total autonómico por tipo y estado
    suma_mun: dict[tuple, float] = {}
    for g in grupos:
        k = (g.get("tipus_establiment"), g.get("estat"))
        suma_mun[k] = suma_mun.get(k, 0) + float(g.get("n") or 0)
    cuadre = all(abs(suma_mun.get((t.get("tipus_establiment"), t.get("estat")), 0) - float(t.get("n") or 0)) < 1e-9
                 for t in tot_n)

    # Barcelona municipio por código postal (no hay barrio en el dataset)
    cp = _soql({"$select": "codi_postal,count(*) as n,sum(total_places) as plazas",
                "$where": "municipi='Barcelona' AND tipus_establiment='Habitatges d''ús turístic'",
                "$group": "codi_postal", "$limit": 50000})
    for g in cp:
        cpc = str(g.get("codi_postal") or "SIN_DATO")
        filas.append({**base, "serie": "HUT_establecimientos_Habitatges_us_turistic_Barcelona_CP",
                      "valor": float(g.get("n") or 0), "unidad": "establecimientos",
                      "territorio": "Barcelona", "nivel": "CODIGO_POSTAL", "codigo": cpc})
        filas.append({**base, "serie": "HUT_plazas_Habitatges_us_turistic_Barcelona_CP",
                      "valor": float(g.get("plazas") or 0), "unidad": "plazas",
                      "territorio": "Barcelona", "nivel": "CODIGO_POSTAL", "codigo": cpc})
    bcn_hut = sum(float(g.get("n") or 0) for g in cp)
    bcn_mun = sum(float(g.get("n") or 0) for g in grupos
                  if g.get("municipi") == "Barcelona" and g.get("tipus_establiment") == "Habitatges d'ús turístic")
    print(f"[hut] fecha {f_ver}, municipios agrupados {len(grupos)}, cuadre_total={cuadre}, "
          f"cuadre_BCN_CP={abs(bcn_hut - bcn_mun) < 1e-9}")
    registrar_fallida("Registre de Turisme de Catalunya (HUT) con fechas de alta y baja",
                      f"https://analisi.transparenciacatalunya.cat/d/{HUT_ID}",
                      "dataset sin columnas de fecha de alta/baja; solo estado actual (todas 'Alta')",
                      "fotografía única; para flujos pedir histórico al Registre (solicitud de transparencia) "
                      "o usar Incasòl/Registre de fiances")
    df = pd.DataFrame(filas)
    uf.save(df, HUT_NAME, HUT_FUENTE)
    return uf.RAW / HUT_NAME


def main() -> None:
    (uf.RAW / "v3").mkdir(parents=True, exist_ok=True)
    print(fetch_airbnb())
    print(fetch_hut())
    registrar_fallida("Opendata BCN (precio venta por barrio, superficie/población, atractivos)",
                      "https://opendata-ajuntament.barcelona.cat/",
                      "desafío anti-bot (302 a /challenge) en todas las rutas; API CKAN sin respuesta",
                      "precio: notariado/registradores ya en data/raw; atractivos: OSM (ODbL) pendiente de decisión")
    registrar_fallida("Google Trends «airbnb» (España y Barcelona)",
                      "https://trends.google.com/trends/api/explore",
                      "sin API pública; el endpoint explore responde 400 sin token de widget; pytrends es scraping no autorizado",
                      "exportación CSV manual desde trends.google.com por el responsable, colocada en data/raw/v3/")


if __name__ == "__main__":
    main()
