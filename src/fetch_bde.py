"""Descarga series del Banco de España (CSV de boletín estadístico) a data/raw.

Los CSV del BdE son anchos: fila 0 = código de serie, filas 1-5 = metadatos
(número secuencial, alias, descripción, unidades, frecuencia) y luego una fila por
periodo con etiquetas tipo 'MAR 1995' y '_' para huecos. Aquí se transforman a formato largo.

Idempotente: si el CSV de destino ya existe no se vuelve a bajar (salvo FORCE=1).
Ejecutar desde la raíz del repo:  python3 src/fetch_bde.py
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import cached, get, save  # noqa: E402

BASE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv"
FUENTE = "BdE"

# (archivo de salida, tabla CSV del BdE, [(código de serie, descripción corta)])
SOURCES = [
    ("bde_precio_vivienda_libre.csv", "be2507.csv", [
        ("DHIVTNOAPLPMMUVT_RLI.T", "Precio medio m2 viviendas libres tasadas. Total nacional"),
        ("DHIVTNOAPLPMMUVT_VVN_RLI.T", "Precio medio m2 viviendas libres tasadas. Hasta 5 años"),
        ("DHIVTNOAPLPMMUVT_VVU_RLI.T", "Precio medio m2 viviendas libres tasadas. Más de 5 años"),
    ]),
    ("bde_tipo_hipotecario_referencia.csv", "be1901.csv", [
        ("D_1T9H0000", "Tipo medio adquisición vivienda libre, más de 3 años, conjunto EC España"),
    ]),
]

MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
         "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}
META_ROWS = ("CÓDIGO DE LA SERIE", "NÚMERO SECUENCIAL", "ALIAS DE LA SERIE",
             "DESCRIPCIÓN DE LA SERIE", "DESCRIPCIÓN DE LAS UNIDADES", "FRECUENCIA")


def _parse_wide(text: str, url: str, wanted: list[tuple[str, str]]) -> pd.DataFrame:
    raw = pd.read_csv(io.StringIO(text), header=None, dtype=str, keep_default_na=False)
    labels = raw[0].str.strip()
    meta = {lab: raw[labels == lab].iloc[0] for lab in META_ROWS if (labels == lab).any()}
    codes = meta["CÓDIGO DE LA SERIE"]
    unidades = meta["DESCRIPCIÓN DE LAS UNIDADES"]
    frec = meta["FRECUENCIA"]
    data = raw[labels.str.match(r"^[A-ZÁÉÍÓÚ]{3} \d{4}$")]

    frames = []
    for code, desc in wanted:
        col = [c for c in raw.columns if c != 0 and codes[c] == code]
        if not col:
            raise ValueError(f"Serie {code} no encontrada en {url}")
        c = col[0]
        sub = data[[0, c]].copy()
        sub.columns = ["etiqueta", "valor_raw"]
        partes = sub["etiqueta"].str.split(" ", n=1, expand=True)
        periodo = partes[1] + "-" + partes[0].map(lambda m: f"{MESES[m]:02d}")
        if frec[c].strip().upper() == "TRIMESTRAL":
            # En series trimestrales el BdE rellena todos los meses con '_'; solo cierres de trimestre.
            keep = periodo.str[-2:].isin(["03", "06", "09", "12"])
            sub, periodo = sub[keep], periodo[keep]
        valor = sub["valor_raw"].str.strip().replace({"_": None, "": None})
        frames.append(pd.DataFrame({
            "fecha": periodo + "-01",
            "periodo": periodo,
            "serie": code,
            "valor": pd.to_numeric(valor.str.replace(",", ".", regex=False), errors="coerce"),
            "unidad": unidades[c],
            "fuente": FUENTE,
            "url": url,
            "frecuencia_bde": frec[c],
            "titulo": desc,
        }))
    return pd.concat(frames, ignore_index=True)


def fetch(out_name: str, table: str, wanted: list[tuple[str, str]]) -> None:
    if cached(out_name):
        return
    url = f"{BASE}/{table}"
    text = get(url, as_json=False)
    if "CÓDIGO DE LA SERIE" not in text and "CODIGO DE LA SERIE" not in text:
        raise RuntimeError(f"{url}: formato inesperado (no contiene 'CÓDIGO DE LA SERIE')")
    df = _parse_wide(text, url, wanted)
    save(df, out_name, FUENTE)


if __name__ == "__main__":
    for out_name, table, wanted in SOURCES:
        fetch(out_name, table, wanted)
