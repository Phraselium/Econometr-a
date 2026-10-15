"""V9-DATOS-COMPLETO (bloque 6, D5): IPCA de alquileres efectivos de vivienda (COICOP 2018 CP041) por país, mensual,
índice 2015 = 100 (Eurostat prc_hicp_minr, sustituto de prc_hicp_midx desde 2026). Desde el primer mes disponible.
Los precios de la vivienda por país (prc_hpi_q) ya están en data/raw/v8/eurostat_prc_hpi_q_multi.csv.
Licencia Eurostat: reutilización con cita (Decisión 2011/833/UE). Marca posterior_prereg desde 2026-07.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAIZ, RAW9, abrir_gz_texto, descargar, registrar, sha256  # noqa: E402

FUENTE = "eurostat_alquiler"
DIR = RAW9 / FUENTE
URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/prc_hicp_minr/M.I15.CP041.?format=SDMX-CSV"
SALIDA = DIR / "prc_hicp_minr_cp041_mensual.csv.gz"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                if not (RAIZ / fila["fichero"]).exists() or sha256(RAIZ / fila["fichero"]) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK eurostat_alquiler"); return 0
    bruto = descargar(URL, DIR / "original" / "prc_hicp_minr_cp041.csv", timeout=600)
    filas = []
    with open(bruto, encoding="utf-8") as f:
        for x in csv.DictReader(f):
            if x["OBS_VALUE"]:
                filas.append([x["geo"], x["TIME_PERIOD"], x["OBS_VALUE"], x["OBS_FLAG"], x["TIME_PERIOD"] >= "2026-07"])
    filas.sort()
    with abrir_gz_texto(SALIDA) as g:
        w = csv.writer(g)
        w.writerow(["pais", "periodo", "indice_2015", "flag", "posterior_prereg"])
        w.writerows(filas)
    per = sorted({r[1] for r in filas})
    registrar(FUENTE, SALIDA, URL, edicion="Eurostat prc_hicp_minr (consulta 2026-10-15)", periodo=f"{per[0]}–{per[-1]}",
              nivel_territorial="país", licencia="Eurostat: reutilización con cita", redistribuible=True,
              notas=f"filas={len(filas)}; países={len({r[0] for r in filas})}")
    print(len(filas), per[0], per[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
