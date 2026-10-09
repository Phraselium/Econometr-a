"""Ajuntament de València: precio de la vivienda libre (catálogo CKAN opendata.vlci.valencia.es).

El padrón por nacionalidad y distrito no está en el catálogo abierto (ver docs/fuentes_fallidas.md).
Salida: data/raw/vlc_precio_vivienda_libre.csv (€/m2 trimestral; València, CV y España).
El CSV original se guarda sin editar en data/raw/vlc_fuente/.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

from utils_fetch import RAW, cached, download, save

URL = ("https://opendata.vlci.valencia.es/dataset/86123d64-c767-4ab0-8e2b-446904b89fdc/"
       "resource/df2b8eeb-5e14-4627-9044-b502ea174445/download/precio_vivienda-cas.csv")
DEST = RAW / "vlc_fuente" / "precio_vivienda-cas.csv"
FUENTE = "Ajuntament de València - Opendata (CKAN); fuente primaria no indicada en el recurso"
TRIMESTRES = ["1er Trimestre", "2º Trimestre", "3er Trimestre", "4º Trimestre"]


def _slug(s: str) -> str:
    rep = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n", "à": "a", "è": "e", "ò": "o", "ç": "c"}
    s = s.lower()
    for a, b in rep.items():
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _valor(x) -> float:
    s = str(x).replace(" ", "").replace("\xa0", "").strip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return np.nan  # '---' o vacío: trimestre no disponible
    return float(s)


def main() -> None:
    if cached("vlc_precio_vivienda_libre.csv"):
        return
    download(URL, DEST)
    raw = pd.read_csv(DEST, sep=";", encoding="utf-8-sig", dtype=str)
    raw.columns = [c.strip() for c in raw.columns]
    filas = []
    for _, r in raw.iterrows():
        tipo, ciudad, anyo = r["Tipo"].strip(), r["Ciudad/Otro"].strip(), int(r["Año"])
        for q, col in enumerate(TRIMESTRES, start=1):
            v = _valor(r[col])
            if np.isnan(v):
                continue
            filas.append({
                "fecha": f"{anyo}-{3 * q - 2:02d}-01", "periodo": f"{anyo}T{q}",
                "serie": f"vlc_precio_libre_{_slug(tipo)}_{_slug(ciudad)}", "valor": v,
                "unidad": "euros/m2", "fuente": FUENTE, "url": URL,
                "tipo": tipo, "territorio": ciudad,
            })
    df = pd.DataFrame(filas)
    if df.duplicated(["serie", "fecha"]).any():
        raise ValueError("duplicados serie/fecha en precio vivienda libre")
    save(df, "vlc_precio_vivienda_libre.csv", FUENTE)


if __name__ == "__main__":
    main()
