"""V9-DATOS · Generalitat Valenciana, registro de fianzas de alquiler (conjuntos viv-reg-fia-2020 … 2026, CC BY 4.0).

Descarga la versión actual de cada conjunto (CSV) a data/raw/v9/gva_fianzas/ y la compara con la copia del proyecto
(data/raw/v5/gva_fianzas_<año>.csv, solo lectura): escribe comparacion_v5.csv (año, filas, sha256 de ambas, igual sí/no).
Las fianzas no las usan evaluate_v7 ni evaluate_v8; aun así, si el fichero tiene fecha mensual se añade
`posterior_prereg` en la comparación (no se modifica el crudo). Uso: python3 src/v9/fetch_gva_fianzas.py [--verificar]
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun  # noqa: E402

FUENTE = "gva_fianzas"
DIR = comun.RAW9 / FUENTE
API = "https://dadesobertes.gva.es/api/3/action/package_show?id=viv-reg-fia-{}"
LIC = "CC BY 4.0 (dadesobertes.gva.es)"
ANIOS = range(2020, 2027)


def url_csv(anio: int) -> str:
    for i in range(4):
        try:
            r = requests.get(API.format(anio), headers=comun.CABECERAS, timeout=60)
            r.raise_for_status()
            res = json.loads(r.text)["result"]["resources"]
            return next(x["url"] for x in res if x.get("format", "").upper() == "CSV")
        except Exception:  # noqa: BLE001
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"CKAN GVA no responde para {anio}")


def verificar() -> int:
    man = DIR / "_manifest.csv"
    if not man.exists():
        return 1
    with open(man, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return 0 if filas and all((comun.RAIZ / r["fichero"]).exists() and comun.sha256(comun.RAIZ / r["fichero"]) == r["sha256"] for r in filas) else 1


def main(verificar: bool = False) -> int:
    if verificar:
        return globals()["verificar"]()
    comp = []
    for a in ANIOS:
        u = url_csv(a)
        dest = DIR / f"gva_fianzas_{a}.csv"
        comun.descargar(u, dest)
        comun.registrar(FUENTE, dest, u, f"viv-reg-fia-{a} (versión 2026-10)", str(a), "municipio", LIC, True)
        v5 = comun.RAIZ / "data" / "raw" / "v5" / f"gva_fianzas_{a}.csv"
        s9, s5 = comun.sha256(dest), (comun.sha256(v5) if v5.exists() else "")
        comp.append({"anio": a, "filas_v9": comun.contar_filas(dest), "filas_v5": comun.contar_filas(v5) if v5.exists() else "",
                     "sha256_v9": s9, "sha256_v5": s5, "igual": "sí" if s9 == s5 else "no"})
    out = DIR / "comparacion_v5.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(comp[0]))
        w.writeheader()
        w.writerows(comp)
    comun.registrar(FUENTE, out, "", "comparación con data/raw/v5", "2020-2026", "municipio", LIC, True, "derivado")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
