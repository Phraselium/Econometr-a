"""V9-DATOS · INE, Índice de Precios de Vivienda en Alquiler (IPVA), edición 2024 (publicada en 2026).

Tablas (jaxiT3, CSV con códigos INE en la etiqueta), en formato largo con códigos como texto:
  59004 nacional y CCAA por antigüedad del contrato (nuevos y existentes);
  59005 provincias por antigüedad del contrato;
  59061 distritos de los municipios capitales de provincia.
El IPVA municipal (59060) y por tipo de edificación ya están en el proyecto (data/raw/ine_ipva_municipal.csv). Es una serie
anual: no hay filas posteriores al pre-registro. Licencia: INE, reutilización con cita.
Uso: python3 src/v9/fetch_ine_ipva.py [--verificar]
"""
from __future__ import annotations

import csv
import gzip
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun  # noqa: E402

FUENTE = "ine_ipva"
DIR = comun.RAW9 / FUENTE
URL_T = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{}.csv?nocab=1"
TABLAS = {59004: "ccaa_antiguedad", 59005: "provincia_antiguedad", 59061: "distrito_capitales"}
LIC = "INE: reutilización con cita (aviso legal, Ley 37/2007)"


def codigo(etiqueta: str) -> str:
    m = re.match(r"^\s*(\d+)\s", etiqueta or "")
    return m.group(1) if m else ""


def convertir(tid: int, nombre: str) -> Path:
    crudo = DIR / "original" / f"t{tid}.csv"
    comun.descargar(URL_T.format(tid), crudo)
    with open(crudo, encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f, delimiter=";"))
    cols = [c for c in filas[0] if c not in ("Periodo", "Total")]
    dest = DIR / f"ipva_{nombre}.csv"
    with open(dest, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tabla"] + [f"{c}_codigo" for c in cols] + cols + ["periodo", "valor"])
        for r in filas:
            w.writerow([tid] + [codigo(r[c]) for c in cols] + [r[c] for c in cols] + [r["Periodo"], r["Total"].replace(".", "").replace(",", ".")])
    return dest


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
    for tid, nombre in TABLAS.items():
        dest = convertir(tid, nombre)
        comun.registrar(FUENTE, dest, URL_T.format(tid), "IPVA 2024 (publicado 2026-05)", "2015-2024", nombre.split("_")[0], LIC, True,
                        f"Tabla INE {tid}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
