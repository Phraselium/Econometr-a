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
  data/raw/catastro_urbana_municipios.csv.gz   (gzip determinista, mtime=0; el .csv sin comprimir ~60 MB no se versiona)
         series catastro_uu_res_<INE5> y catastro_uu_tot_<INE5>
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
import datetime as dt  # noqa: E402
import fcntl  # noqa: E402

from utils_fetch import HEADERS, MANIFEST, RAW, FORCE, download, read_excel_any  # noqa: E402

warnings.filterwarnings("ignore")

BASE = "https://www.catastro.hacienda.gob.es/documentos/estadisticas"
XLS_DIR = RAW / "v2_orig" / "catastro"
FUENTE = "Catastro - Estadisticas catastrales, Datos municipios (Urbano)"
EJERCICIOS = range(2012, 2027)
OLE_MAGIC = b"\xd0\xcf\x11\xe0"


def verificar(url: str) -> int:
    """Peticion pequeña (bytes 0-15): comprueba HTTP 206 y cabecera OLE2; devuelve el tamaño total."""
    r = requests.get(url, headers={**HEADERS, "Range": "bytes=0-15"}, timeout=60)
    if r.status_code not in (200, 206) or not r.content.startswith(OLE_MAGIC):
        raise RuntimeError(f"endpoint {url}: HTTP {r.status_code}, cabecera {r.content[:4]!r}")
    cr = r.headers.get("Content-Range", "")
    return int(cr.split("/")[-1]) if "/" in cr else len(r.content)


def _col(cab, *cands):
    """Primera columna de la lista de candidatos que exista en la cabecera (None si ninguna)."""
    return next((c for c in cands if c in cab), None)


def leer(path: Path, ejercicio: int) -> pd.DataFrame:
    """Parser tolerante: la cabecera cambia entre ejercicios (2012: C_INE sin nombres; 2019+: COD_INE_*)."""
    sh = list(read_excel_any(path).values())[0]
    hr = next(r for r in range(min(20, sh.shape[0])) if "UU_RES" in [str(v).strip() for v in sh.iloc[r]])
    cab = [str(v).strip() for v in sh.iloc[hr]]
    c_muni = _col(cab, "COD_INE_MUNI", "C_INE")
    c_uures, c_tot = _col(cab, "UU_RES"), _col(cab, "UURBANAS")
    if c_muni is None or c_tot is None:
        raise ValueError(f"URBANA{ejercicio}: faltan columnas de codigo o UURBANAS ({cab[:12]})")
    c_nmun = _col(cab, "NOM_MUNI", "MUNICIPIO", "NOM_COMUNI", "NOM_COMUNI")
    c_nprov = _col(cab, "NOM_PROV", "PROVINCIA")
    c_nccaa = _col(cab, "NOM_CCAA")
    d = sh.iloc[hr + 1:].copy()
    d.columns = cab
    code = d[c_muni].map(lambda v: str(int(float(v))).zfill(5) if str(v).strip() not in ("", "nan") else "")
    ok = code.str.fullmatch(r"\d{5}")
    print(f"  [codigos] URBANA{ejercicio}: {int(ok.sum())} municipios validos, {int((~ok).sum())} filas sin codigo INE de 5 digitos (descartadas)")
    d = d[ok].copy()
    code = code[ok]
    url = f"{BASE}/URBANA{ejercicio}.xls"
    txt = lambda c: d[c].astype(str).str.strip().values if c else [""] * len(d)  # noqa: E731
    base = pd.DataFrame({
        "fecha": f"{ejercicio - 1}-12-31", "periodo": str(ejercicio), "fuente": FUENTE, "url": url,
        "territorio": txt(c_nmun), "nivel": "municipio", "codigo": code.values,
        "provincia_codigo": code.str[:2].values, "provincia": txt(c_nprov),
        "ccaa_codigo": "", "ccaa": txt(c_nccaa), "ejercicio": ejercicio,
    })
    partes = []
    for col, serie_pref, unidad in [(c_uures, "catastro_uu_res", "unidades_urbanas_residenciales"),
                                    (c_tot, "catastro_uu_tot", "unidades_urbanas_total")]:
        if col is None:
            continue
        p = base.copy()
        p["serie"] = f"{serie_pref}_" + code.values
        p["valor"] = pd.to_numeric(d[col], errors="coerce").values  # vacios = NaN, sin relleno
        p["unidad"] = unidad
        partes.append(p)
    return pd.concat(partes, ignore_index=True)


OUT = RAW / "catastro_urbana_municipios.csv.gz"


def registrar(df: pd.DataFrame) -> None:
    """Fila en _manifest.csv con el mismo formato que utils_fetch.save (archivo relativo a data/raw)."""
    row = pd.DataFrame([{
        "archivo": OUT.name, "fuente": FUENTE, "n_series": df["serie"].nunique(),
        "primera_fecha": str(df["fecha"].min()), "ultima_fecha": str(df["fecha"].max()),
        "n_obs": len(df), "n_nan": int(df["valor"].isna().sum()),
        "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }])
    with open(RAW / ".manifest.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if MANIFEST.exists():
            man = pd.read_csv(MANIFEST)
            man = pd.concat([man[man["archivo"] != OUT.name], row], ignore_index=True)
        else:
            man = row
        man.sort_values("archivo").to_csv(MANIFEST, index=False)


def main() -> None:
    if OUT.exists() and not FORCE:
        print(f"[cache] {OUT.name}")
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
    out = out.drop(columns=["ejercicio"]).sort_values(["serie", "fecha"]).reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, compression={"method": "gzip", "mtime": 0})
    registrar(out)
    print(f"[ok] {OUT.name}: {len(out)} obs, {out.serie.nunique()} series, "
          f"{out.fecha.min()} -> {out.fecha.max()}, NaN={int(out.valor.isna().sum())}")


if __name__ == "__main__":
    main()
