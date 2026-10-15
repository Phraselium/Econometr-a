"""V11-DATOS (bloque 1, punto 4): INE, Estadística Continua de Población (ECP), población por PROVINCIA y nacionalidad,
TRIMESTRAL (la base anterior solo tenía el 1 de enero: data/raw/ine_v2_padron_prov_*, tabla 77023).

Tablas (jaxiT3, se guarda sexo = Total):
- 56947: población residente por fecha, provincia, grupo quinquenal de edad y nacionalidad (agrupación de países),
  trimestral 2002T1-2025T1 (serie cerrada al cambiar de base);
- 82104: idem, nacionalidad española/extranjera, 2025T2- (serie vigente; filas desde 2026T3 = posterior_prereg);
- 60129: población en viviendas familiares por provincia, nacionalidad (española/extranjera) y edad, 2021T1-;
- 79278: población por provincia, nacionalidad (española/extranjera) y país de nacimiento (España/extranjero), 2002-.
Hogares por nacionalidad de la persona de referencia: la ECP NO los publica (solo hogares por tamaño, ya en
data/raw/ine_v2_hogares_prov.csv); la fuente es el Censo 2021 (bloque 2) y la EPA/ECV (microdatos, punto 9).
Municipio por nacionalidad: la ECP no baja de provincia; el nivel municipal anual está en el padrón (v9,
2003-2022) y el censo anual (v9, 2021-2025).
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, INICIO_POSTERIOR, RAW11, abrir_gz_texto, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_ecp"
DIR = RAW11 / FUENTE
URL_T = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1"
LIC = "INE: reutilización con cita (Ley 37/2007)"
TABLAS = {56947: "provincia × edad quinquenal × nacionalidad (agrupación de países), trimestral, base anterior",
          82104: "provincia × edad quinquenal × nacionalidad (española/extranjera), trimestral, serie vigente",
          60129: "población en viviendas familiares por provincia × nacionalidad × edad, trimestral",
          79278: "provincia × nacionalidad × país de nacimiento (España/extranjero)"}
MESES = {"enero": 1, "abril": 4, "julio": 7, "octubre": 10}


def fecha(p: str) -> str:
    m = re.match(r"1 de (\w+) de (\d{4})", p)
    return f"{m.group(2)}-{MESES[m.group(1)]:02d}-01" if m else p


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for t, desc in TABLAS.items():
        r = None
        for _ in range(3):
            try:
                r = requests.get(URL_T.format(t=t), headers=CABECERAS, timeout=1200)
                r.raise_for_status()
                break
            except Exception:  # noqa: BLE001
                r = None
        if r is None:
            print("FALLO tabla", t)
            continue
        lector = csv.reader(io.StringIO(r.content.decode("utf-8-sig", "replace")), delimiter=";")
        cab = next(lector)
        i_s, i_p = cab.index("Sexo"), cab.index("Periodo")
        filas = []
        for f in lector:
            if len(f) == len(cab) and f[i_s] == "Total":
                f = f[:i_s] + f[i_s + 1:]
                filas.append(f)
        cab2 = [c for c in cab if c != "Sexo"] + ["fecha", "posterior_prereg"]
        i_p2 = cab2.index("Periodo")
        filas = [f + [fecha(f[i_p2]), str(fecha(f[i_p2]) >= str(INICIO_POSTERIOR))] for f in filas]
        ruta = DIR / f"ecp_t{t}.csv.gz"
        filas.sort(key=lambda f: (f[-2], f[:i_p2]))
        with abrir_gz_texto(ruta) as g:
            w = csv.writer(g)
            w.writerow(cab2)
            w.writerows(filas)
        fechas = sorted({f[-2] for f in filas})
        npost = sum(f[-1] == "True" for f in filas)
        registrar(FUENTE, ruta, URL_T.format(t=t), edicion=f"INE ECP, tabla {t} (jaxiT3)", periodo=f"{fechas[0]}–{fechas[-1]}",
                  nivel_territorial="provincia (código en la etiqueta)", licencia=LIC, redistribuible=True,
                  notas=f"{desc}; sexo = total; filas={len(filas)}; posterior_prereg={npost}")
        print("tabla", t, len(filas), fechas[0], fechas[-1], "post", npost)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
