"""Catastro: unidades urbanas por municipio (uso residencial), anual 2012-2026.

Fuente: Dirección General del Catastro, 'Estadísticas catastrales > Datos municipios > Urbano'
  https://www.catastro.hacienda.gob.es/es-ES/estadisticas_7.html
  Fichero publicado y de descarga directa: /documentos/estadisticas/URBANA{ejercicio}.xls (OLE2, ~3-4 MB).
  Un registro por municipio. Columnas usadas: COD_INE_MUNI, NOM_MUNI, COD_INE_PROV, NOM_PROV,
  COD_INE_CCAA, NOM_CCAA, UURBANAS (unidades urbanas totales), UU_RES (unidades urbanas residenciales).
  Fuente oficial: "Padrón correspondiente al ejercicio seleccionado (datos a 31 de diciembre del año anterior)".

Titularidad (personas físicas / jurídicas por municipio): NO extraido. La pagina 'Titularidad'
(estadisticas_3_1.html) ofrece solo un visor JAXI (tabla.do) con consulta dinámica por dimensiones; no hay
fichero publicado descargable. Ver docs/v2/fuentes_fallidas.md. Por eso no se genera catastro_titulares.csv.

Salidas:
  data/raw/catastro_urbana_municipios.csv   series catastro_uu_res_<INE5> y catastro_uu_tot_<INE5>
  data/raw/v2_orig/catastro/URBANA{ejercicio}.xls  originales sin editar (~50 MB; gitignore)
Fecha = 31-dic del ejercicio anterior (fecha de referencia de los datos); periodo = ejercicio.
Cache: si el CSV existe no se vuelve a descargar (FORCE=1 rehace).
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import HEADERS, RAW, cached, download, read_excel_any, save  # noqa: E402

warnings.filterwarnings("ignore")

BASE = "https://www.catastro.hacienda.gob.es/documentos/estadisticas"
XLS_DIR = RAW / "v2_orig" / "catastro"
FUENTE = "Catastro - Estadisticas catastrales, Datos municipios (Urbano)"
EJERCICIOS = range(2012, 2027)
OLE_MAGIC = b"\xd0\xcf\x11\xe0"
NEEDED = ["COD_INE_MUNI", "NOM_MUNI", "COD_INE_PROV", "NOM_PROV", "COD_INE_CCAA", "NOM_CCAA", "UURBANAS", "UU_RES"]


def verificar(url: str) -> int:
    """Peticion pequeña (bytes 0-15): comprueba HTTP 206 y cabecera OLE2; devuelve el tamaño total."""
    r = requests.get(url, headers={**HEADERS, "Range": "bytes=0-15"}, timeout=60)
    if r.status_code not in (200, 206) or not r.content.startswith(OLE_MAGIC):
        raise RuntimeError(f"endpoint {url}: HTTP {r.status_code}, cabecera {r.content[:4]!r}")
    cr = r.headers.get("Content-Range", "")
    return int(cr.split("/")[-1]) if "/" in cr else len(r.content)


def leer(path: Path, ejercicio: int) -> pd.DataFrame:
    hojas = read_excel_any(path)
    sh = list(hojas.values())[0]
    hr = next(r for r in range(min(20, sh.shape[0])) if "COD_INE_MUNI" in [str(v).strip() for v in sh.iloc[r]])
    cab = [str(v).strip() for v in sh.iloc[hr]]
    falt = [c for c in NEEDED if c not in cab]
    if falt:
        raise ValueError(f"URBANA{ejercicio}: faltan columnas {falt}")
    d = sh.iloc[hr + 1:].copy()
    d.columns = cab
    d = d[d["COD_INE_MUNI"].notna()]
    d["muni"] = d["COD_INE_MUNI"].map(lambda v: str(int(float(v))).zfill(5) if str(v).strip() not in ("", "nan") else None)
    d = d[d["muni"].notna()]
    d["prov"] = d["COD_INE_PROV"].map(lambda v: str(int(float(v))).zfill(2))
    d["ccaa"] = d["COD_INE_CCAA"].map(lambda v: str(int(float(v))).zfill(2))
    d["UU_RES"] = pd.to_numeric(d["UU_RES"], errors="coerce")
    d["UURBANAS"] = pd.to_numeric(d["UURBANAS"], errors="coerce")
    url = f"{BASE}/URBANA{ejercicio}.xls"
    base = pd.DataFrame({
        "fecha": f"{ejercicio - 1}-12-31", "periodo": str(ejercicio), "fuente": FUENTE, "url": url,
        "territorio": d["NOM_MUNI"].astype(str).str.strip().values, "nivel": "municipio",
        "codigo": d["muni"].values, "provincia_codigo": d["prov"].values,
        "provincia": d["NOM_PROV"].astype(str).str.strip().values, "ccaa_codigo": d["ccaa"].values,
        "ccaa": d["NOM_CCAA"].astype(str).str.strip().values, "ejercicio": ejercicio,
    })
    partes = []
    for var, serie_pref, unidad in [("UU_RES", "catastro_uu_res", "unidades_urbanas_residenciales"),
                                    ("UURBANAS", "catastro_uu_tot", "unidades_urbanas_total")]:
        p = base.copy()
        p["serie"] = f"{serie_pref}_" + d["muni"].values
        p["valor"] = d[var].values  # NaN se conserva tal cual (sin relleno)
        p["unidad"] = unidad
        partes.append(p)
    return pd.concat(partes, ignore_index=True)


def main() -> None:
    if cached("catastro_urbana_municipios.csv"):
        return
    partes = []
    for y in EJERCICIOS:
        url = f"{BASE}/URBANA{y}.xls"
        tam = verificar(url)
        dest = XLS_DIR / f"URBANA{y}.xls"
        download(url, dest, timeout=300)
        df = leer(dest, y)
        n_mun = df.loc[df.serie.str.startswith("catastro_uu_res"), "codigo"].nunique()
        print(f"  [parse] URBANA{y}: {n_mun} municipios (fichero {tam} bytes)")
        partes.append(df)
    out = pd.concat(partes, ignore_index=True)
    # Sin rellenar: valores vacios se conservan como NaN
    out = out.drop(columns=["ejercicio"]) if False else out
    save(out[["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo",
              "provincia_codigo", "provincia", "ccaa_codigo", "ccaa", "ejercicio"]],
         "catastro_urbana_municipios.csv", FUENTE)


if __name__ == "__main__":
    main()
