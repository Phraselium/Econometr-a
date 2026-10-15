"""V9-DATOS-COMPLETO (bloque 6): BCE, Risk Assessment Indicators (dataflow RAI), serie SVLHPHH: proporción de nuevos
préstamos a hogares para vivienda a tipo variable o con fijación inicial ≤1 año, por país de la zona euro (mensual).

Es la medida de exposición de D5: los volúmenes de MIR por periodo de fijación solo se publican para el agregado U2
(comprobado 2026-10-15; docs/v9/decisiones_datos.md, D9). Licencia BCE: reutilización con cita.
Salida: data/raw/v9/bce_rai/bce_rai_svlhphh.csv.gz (pais, periodo, valor, estado_obs, clave, titulo).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAIZ, RAW9, abrir_gz_texto, descargar, registrar, sha256  # noqa: E402

FUENTE = "bce_rai"
DIR = RAW9 / FUENTE
SALIDA = DIR / "bce_rai_svlhphh.csv.gz"
URL = "https://data-api.ecb.europa.eu/service/data/RAI/M..SVLHPHH..MIR.Z?format=csvdata"
LICENCIA = "BCE: reutilización con cita (ECB Data Portal)"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        with open(DIR / "_manifest.csv", encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                if sha256(RAIZ / fila["fichero"]) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK bce_rai"); return 0
    bruto = descargar(URL, DIR / "original" / "rai_svlhphh.csv", timeout=600)
    filas = []
    with open(bruto, encoding="utf-8") as f:
        for x in csv.DictReader(f):
            filas.append([x["REF_AREA"], x["TIME_PERIOD"], x["OBS_VALUE"], x["OBS_STATUS"], x["KEY"], x["TITLE"].strip()])
    filas.sort()
    with abrir_gz_texto(SALIDA) as g:
        w = csv.writer(g)
        w.writerow(["pais", "periodo", "valor", "estado_obs", "clave", "titulo"])
        w.writerows(filas)
    per = sorted({r[1] for r in filas})
    paises = sorted({r[0] for r in filas})
    registrar(FUENTE, SALIDA, URL, edicion="ECB Data Portal (RAI, API SDMX)", periodo=f"{per[0]}–{per[-1]}",
              nivel_territorial="país (zona euro)", licencia=LICENCIA, redistribuible=True,
              notas=f"filas={len(filas)}; países={','.join(paises)}")
    print(len(filas), paises, per[0], per[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
