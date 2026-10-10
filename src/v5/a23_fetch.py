"""A23 · Descarga (con red, fuera de make) de fianzas de alquiler autonómicas.

Descarga a data/raw/v5/: GVA (Registro de fianzas de alquiler 2020-2026, CKAN dadesobertes.gva.es).
Prueba y registra Madrid, Euskadi y Baleares (resultado en docs/v5/fuentes_fallidas.md).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "data" / "raw" / "v5"
DEST.mkdir(parents=True, exist_ok=True)


def curl(url: str) -> bytes:
    r = subprocess.run(["curl", "-sS", "-L", "-m", "90", url], capture_output=True)
    return r.stdout


def gva() -> None:
    for anio in range(2020, 2027):
        try:
            meta = json.loads(curl(f"https://dadesobertes.gva.es/api/3/action/package_show?id=viv-reg-fia-{anio}"))
            csv = [x for x in meta["result"]["resources"] if x["format"] == "CSV"][0]["url"]
            raw = curl(csv)
        except Exception as e:  # noqa: BLE001
            print(anio, "ERROR", e)
            continue
        (DEST / f"gva_fianzas_{anio}.csv").write_bytes(raw)
        print(anio, len(raw), hashlib.sha256(raw).hexdigest()[:12], meta["result"].get("metadata_modified"))


def pruebas() -> None:
    for u in ["https://datos.comunidad.madrid/api/3/action/package_search?q=fianzas",
              "https://datos.comunidad.madrid/api/3/action/package_search?q=arrendamientos",
              "https://opendata.euskadi.eus/api-contents?q=fianzas",
              "https://catalegdades.caib.cat/api/3/action/package_search?q=lloguer"]:
        print(u, curl(u)[:120])


if __name__ == "__main__":
    gva()
    if "--pruebas" in sys.argv:
        pruebas()
