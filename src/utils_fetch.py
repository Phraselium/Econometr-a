"""Utilidades comunes de descarga con caché para data/raw.

Formato largo estándar: fecha, periodo, serie, valor, unidad, fuente, url.
Si el CSV de destino existe, no se vuelve a descargar salvo FORCE=1.
"""
from __future__ import annotations

import datetime as dt
import os
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "_manifest.csv"
COLS = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url"]
FORCE = os.environ.get("FORCE") == "1"
HEADERS = {"User-Agent": "econometria-vivienda-tfm/1.0 (investigacion academica)"}


def download(url: str, dest: Path, timeout: int = 180) -> Path:
    """Descarga binaria sin editar, con caché (no se baja si dest ya existe y no hay FORCE=1)."""
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0 and not FORCE:
        print(f"[cache] {dest.relative_to(ROOT)}")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for i in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            if not r.content:
                raise RuntimeError("respuesta vacía")
            dest.write_bytes(r.content)
            print(f"[dl] {dest.name} ({len(r.content)} bytes)")
            return dest
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"Fallo al descargar {url}: {last}")


def read_excel_any(path: Path) -> dict:
    """Lee todas las hojas (header=None). Detecta xlsx/xls por cabecera aunque la extensión sea .XLS."""
    import pandas as pd

    with open(path, "rb") as fh:
        magic = fh.read(4)
    engine = "openpyxl" if magic == b"PK\x03\x04" else "xlrd"
    return pd.read_excel(path, sheet_name=None, header=None, engine=engine)


def cached(name: str) -> bool:
    """True si data/raw/<name> existe y no se fuerza la descarga."""
    p = RAW / name
    if p.exists() and not FORCE:
        print(f"[cache] {name}")
        return True
    return False


def get(url: str, params: dict | None = None, tries: int = 4, timeout: int = 90, as_json: bool = True):
    """GET con reintentos y backoff exponencial (2, 4, 8 s)."""
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            return r.json() if as_json else r.text
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"Fallo al descargar {url} {params}: {last}")


def save(df: pd.DataFrame, name: str, fuente: str) -> Path:
    """Guarda un CSV largo en data/raw y actualiza el manifiesto."""
    missing = [c for c in COLS if c not in df.columns]
    if missing:
        raise ValueError(f"{name}: faltan columnas {missing}")
    RAW.mkdir(parents=True, exist_ok=True)
    df = df[COLS + [c for c in df.columns if c not in COLS]].sort_values(["serie", "fecha"])
    path = RAW / name
    df.to_csv(path, index=False)
    row = pd.DataFrame([{
        "archivo": name, "fuente": fuente,
        "n_series": df["serie"].nunique(),
        "primera_fecha": str(df["fecha"].min()), "ultima_fecha": str(df["fecha"].max()),
        "n_obs": len(df), "n_nan": int(df["valor"].isna().sum()),
        "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }])
    if MANIFEST.exists():
        man = pd.read_csv(MANIFEST)
        man = pd.concat([man[man["archivo"] != name], row], ignore_index=True)
    else:
        man = row
    man.sort_values("archivo").to_csv(MANIFEST, index=False)
    print(f"[ok] {name}: {len(df)} obs, {df['serie'].nunique()} series, {row.primera_fecha[0]} → {row.ultima_fecha[0]}")
    return path
