"""T1 · descarga (con red, fuera de make) de licencias de obra del Ministerio (Boletín Online, bloque 1).

Tablas: 10010600 (viviendas según tipo de obra, nacional), 10011000 (obras de demolición, nacional)
y 1002NN30 (viviendas según tipo de obra por comunidad autónoma, NN=01..19). Se guardan en
data/raw/v5_1/t1/ (solo ficheros nuevos). Uso: python3 src/v5_1/t1_fetch.py
"""
from __future__ import annotations

from pathlib import Path

import requests

OUT = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5_1" / "t1"
BASE = "https://apps.fomento.gob.es/BoletinOnline/sedal/"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    codigos = ["10010600", "10011000"] + [f"1002{n:02d}30" for n in range(1, 20)]
    for c in codigos:
        r = requests.get(f"{BASE}{c}.XLS", timeout=60)
        print(c, r.status_code, len(r.content))
        if r.status_code == 200:
            (OUT / f"{c}.XLS").write_bytes(r.content)


if __name__ == "__main__":
    main()
