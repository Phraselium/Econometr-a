"""Descarga series del BCE (data-api) a data/raw en formato largo.

Idempotente: si el CSV de destino ya existe no se vuelve a bajar (salvo FORCE=1).
Cada serie: probe rápido (lastNObservations=3) y después histórico completo.
Ejecutar desde la raíz del repo:  python3 src/fetch_ecb.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import cached, get, save  # noqa: E402

BASE = "https://data-api.ecb.europa.eu/service/data"
FUENTE = "BCE"

# (archivo, flujo/clave, descripción corta)
SERIES = [
    ("ecb_tipo_hipotecario_es.csv", "MIR/M.ES.B.A2C.AM.R.A.2250.EUR.N",
     "Tipo medio nuevas operaciones préstamo vivienda hogares ES (AAR, %)"),
    ("ecb_euribor1y.csv", "FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA",
     "Euríbor 1 año, media mensual (%)"),
    ("ecb_nuevo_credito_vivienda_es.csv", "MIR/M.ES.B.A2C.A.B.A.2250.EUR.N",
     "Volumen nuevas operaciones préstamo vivienda hogares ES (EUR millones)"),
    ("ecb_stock_credito_vivienda_es.csv", "BSI/M.ES.N.A.A22.A.1.U2.2250.Z01.E",
     "Stock préstamos vivienda hogares ES (EUR millones, fin de periodo)"),
    ("ecb_tipo_oficial.csv", "FM/B.U2.EUR.4F.KR.MRR_FR.LEV",
     "Tipo BCE operaciones principales de financiación (%, fechas de cambio)"),
    ("ecb_hicp_es.csv", "ICP/M.ES.N.000000.4.ANR",
     "IAPC España, tasa anual (%) - serie discontinuada por el BCE tras 2025-12"),
]

UNIT_MAP = {"PCPA": "% anual", "PCCH": "% variación anual"}


def _unidad(unit: str, mult: str) -> str:
    if unit == "EUR" and str(mult) == "6":
        return "EUR millones"
    if unit == "EUR" and str(mult) == "3":
        return "EUR miles"
    return UNIT_MAP.get(unit, unit)


def _to_long(text: str, url: str) -> pd.DataFrame:
    raw = pd.read_csv(io.StringIO(text))
    tp = raw["TIME_PERIOD"].astype(str)
    # Series mensuales: 'YYYY-MM' -> 'YYYY-MM-01'. Series de fechas de cambio: 'YYYY-MM-DD' se conserva.
    fecha = tp.where(tp.str.len() == 10, tp + "-01")
    unit = raw["UNIT"].iloc[0]
    mult = str(raw["UNIT_MULT"].iloc[0])
    out = pd.DataFrame({
        "fecha": fecha,
        "periodo": tp.str[:7],
        "serie": raw["KEY"],
        "valor": pd.to_numeric(raw["OBS_VALUE"], errors="coerce"),
        "unidad": _unidad(unit, mult),
        "fuente": FUENTE,
        "url": url,
        "unit_ecb": unit,
        "unit_mult_ecb": mult,
        "freq": raw["FREQ"].iloc[0],
        "titulo": raw["TITLE_COMPL"].iloc[0] if "TITLE_COMPL" in raw.columns else "",
    })
    return out


def fetch(name: str, key: str, desc: str) -> None:
    if cached(name):
        return
    url = f"{BASE}/{key}"
    # Probe rápido: comprueba endpoint y última observación antes del histórico completo.
    probe = get(url, params={"format": "csvdata", "lastNObservations": "3"}, as_json=False)
    p = pd.read_csv(io.StringIO(probe))
    print(f"[probe] {key}: última observación {p['TIME_PERIOD'].iloc[-1]} ({desc})")
    text = get(url, params={"format": "csvdata"}, as_json=False)
    df = _to_long(text, f"{url}?format=csvdata")
    save(df, name, FUENTE)


if __name__ == "__main__":
    for archivo, clave, desc in SERIES:
        fetch(archivo, clave, desc)
