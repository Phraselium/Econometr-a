"""V11-DATOS: utilidades comunes (descarga con caché y reintentos, registro en el manifiesto, gzip determinista).
Reutiliza src/v9/comun.py cambiando la raíz a data/raw/v11. Cada fuente: src/v11/fetch_<fuente>.py con
`main(verificar: bool = False) -> int`; datos en data/raw/v11/<fuente>/ y manifiesto data/raw/v11/<fuente>/_manifest.csv;
src/v11/datos_v11.py consolida data/raw/v11/_manifest.csv (`make datos_v11`).
"""
from __future__ import annotations

import csv
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import (CABECERAS, COLS_MANIFIESTO, GZ_PANDAS, INICIO_POSTERIOR, abrir_gz_texto,  # noqa: E402,F401
                          contar_filas, descargar, marcar_posterior_prereg, sha256)

RAIZ = Path(__file__).resolve().parents[2]
RAW11 = RAIZ / "data" / "raw" / "v11"


def registrar(fuente: str, ruta: Path, url: str, edicion: str, periodo: str, nivel_territorial: str, licencia: str,
              redistribuible: bool, notas: str = "") -> dict:
    ruta = Path(ruta)
    man = RAW11 / fuente / "_manifest.csv"
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


def verificar_manifiesto(fuente: str, omitir_no_redistribuibles: bool = True) -> int:
    """0 si todos los ficheros del manifiesto existen con su sha256 (los no redistribuibles ausentes se omiten:
    los trae make datos_terceros o make datos_v11)."""
    man = RAW11 / fuente / "_manifest.csv"
    if not man.exists():
        print(f"falta {man.relative_to(RAIZ)}")
        return 1
    with open(man, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta = RAIZ / fila["fichero"]
            if not ruta.exists() and omitir_no_redistribuibles and (fila["redistribuible"] == "no" or "no versionado" in fila["notas"]):
                continue
            if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                print("FALLO", fila["fichero"])
                return 1
    print(f"OK {fuente}")
    return 0
