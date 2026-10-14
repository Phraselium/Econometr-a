"""V9-DATOS: utilidades comunes de descarga, registro y validación (sin estimaciones).

Cada fuente tiene su script src/v9/fetch_<fuente>.py con una función `main(verificar: bool = False) -> int` y escribe en
data/raw/v9/<fuente>/. Este módulo ofrece:
  - descargar(url, destino): descarga binaria con caché y reintentos (no vuelve a bajar si existe, salvo FORCE=1);
  - registrar(...): añade o actualiza la fila del fichero en data/raw/v9/<fuente>/_manifest.csv (fuente, url, fecha de
    descarga, edición, periodo, nivel territorial, filas, sha256, licencia, redistribuible);
  - marcar_posterior_prereg(df, col_fecha): añade la columna booleana `posterior_prereg` (True desde 2026T3) a las series
    de precios y alquileres que usan evaluate_v7 y evaluate_v8; esas filas no se usan en ningún cálculo;
  - sha256(ruta).
El manifiesto global data/raw/v9/_manifest.csv lo consolida src/v9/datos_v9.py.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import os
import time
from pathlib import Path

import requests

RAIZ = Path(__file__).resolve().parents[2]
RAW9 = RAIZ / "data" / "raw" / "v9"
FORCE = os.environ.get("FORCE") == "1"
CABECERAS = {"User-Agent": "vivienda-espana-evidencia/9 (investigacion academica independiente)"}
COLS_MANIFIESTO = ["fuente", "fichero", "url", "fecha_descarga", "edicion", "periodo", "nivel_territorial", "n_filas",
                   "sha256", "licencia", "redistribuible", "notas"]
INICIO_POSTERIOR = dt.date(2026, 7, 1)   # 2026T3: posterior al pre-registro de V7/V8 (evaluate_v7/evaluate_v8)


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(url: str, destino: Path, timeout: int = 300, intentos: int = 4, **kw) -> Path:
    destino = Path(destino)
    if destino.exists() and destino.stat().st_size > 0 and not FORCE:
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    ultimo = None
    for i in range(intentos):
        try:
            r = requests.get(url, headers=CABECERAS, timeout=timeout, stream=True, **kw)
            r.raise_for_status()
            tmp = destino.with_suffix(destino.suffix + ".part")
            with open(tmp, "wb") as f:
                for trozo in r.iter_content(1 << 20):
                    f.write(trozo)
            if tmp.stat().st_size == 0:
                raise RuntimeError("respuesta vacía")
            tmp.replace(destino)
            return destino
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"no se pudo descargar {url}: {ultimo}")


def contar_filas(ruta: Path) -> int | str:
    s = str(ruta)
    try:
        if s.endswith(".csv"):
            with open(ruta, encoding="utf-8", errors="replace") as f:
                return max(sum(1 for _ in f) - 1, 0)
        if s.endswith(".csv.gz"):
            import gzip
            with gzip.open(ruta, "rt", encoding="utf-8", errors="replace") as f:
                return max(sum(1 for _ in f) - 1, 0)
    except Exception:  # noqa: BLE001
        pass
    return ""


def registrar(fuente: str, ruta: Path, url: str, edicion: str, periodo: str, nivel_territorial: str, licencia: str,
              redistribuible: bool, notas: str = "") -> dict:
    ruta = Path(ruta)
    man = RAW9 / fuente / "_manifest.csv"
    filas = []
    if man.exists():
        with open(man, encoding="utf-8") as f:
            filas = [r for r in csv.DictReader(f) if r["fichero"] != str(ruta.relative_to(RAIZ))]
    fila = {"fuente": fuente, "fichero": str(ruta.relative_to(RAIZ)), "url": url,
            "fecha_descarga": dt.datetime.fromtimestamp(ruta.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%d"),
            "edicion": edicion, "periodo": periodo, "nivel_territorial": nivel_territorial, "n_filas": contar_filas(ruta),
            "sha256": sha256(ruta), "licencia": licencia, "redistribuible": "sí" if redistribuible else "no", "notas": notas}
    filas.append(fila)
    filas.sort(key=lambda r: r["fichero"])
    man.parent.mkdir(parents=True, exist_ok=True)
    with open(man, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS_MANIFIESTO)
        w.writeheader()
        w.writerows(filas)
    return fila


def marcar_posterior_prereg(df, col_fecha: str):
    """Añade `posterior_prereg` (True si la fecha es 2026-07-01 o posterior). No se mira el valor de esas filas."""
    import pandas as pd
    f = pd.to_datetime(df[col_fecha].astype(str).str.replace(r"^(\d{4})[TQ]([1-4])$", lambda m: f"{m.group(1)}-{3 * int(m.group(2)) - 2:02d}-01", regex=True),
                       errors="coerce")
    df["posterior_prereg"] = f >= pd.Timestamp(INICIO_POSTERIOR)
    return df


def abrir_gz_texto(ruta: Path):
    """gzip de texto determinista (mtime = 0): dos ejecuciones dan el mismo sha256."""
    import gzip
    import io
    return io.TextIOWrapper(gzip.GzipFile(filename="", mode="wb", fileobj=open(ruta, "wb"), mtime=0), encoding="utf-8", newline="")


GZ_PANDAS = {"method": "gzip", "mtime": 0}
