"""V9-DATOS-COMPLETO (bloque 3, D7): viviendas principales (= hogares) por provincia en los censos.

- Censo 2011: tabla 3457 (viviendas por tipo, CCAA y provincia).
- Censo 2021: ya en el proyecto (data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv, por municipio).
- Censo 2001: solo en el sistema interactivo de INEbase (ine.es/censo), sin tabla descargable por script
  (3 intentos, 2026-10-15; docs/v9/fuentes_fallidas.md). D7 empieza en 2011 a escala provincial.
Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAIZ, RAW9, abrir_gz_texto, descargar, registrar, sha256  # noqa: E402

FUENTE = "ine_censos"
DIR = RAW9 / FUENTE
URL = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1"
TABLAS = {3457: "censo 2011: viviendas por tipo, CCAA y provincia"}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        with open(DIR / "_manifest.csv", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                if sha256(RAIZ / fila["fichero"]) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK ine_censos"); return 0
    for t, desc in TABLAS.items():
        bruto = descargar(URL.format(t=t), DIR / "original" / f"t{t}.csv")
        ruta = DIR / f"censo_t{t}.csv.gz"
        with open(bruto, encoding="utf-8-sig") as f, abrir_gz_texto(ruta) as g:
            g.write(f.read())
        registrar(FUENTE, ruta, URL.format(t=t), edicion=f"INE, Censo 2011, tabla {t}", periodo="2011 (1 de noviembre)",
                  nivel_territorial="CCAA y provincia (código en la etiqueta)", licencia="INE: reutilización con cita",
                  redistribuible=True, notas=desc)
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
