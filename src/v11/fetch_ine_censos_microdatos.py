"""V12-B3 (fetcher en src/v11 para que lo ejecute `make datos_v11`): tasas de jefatura por edad y nacionalidad de los microdatos de los Censos 2011 y 2021 (INE).

- 2011: Microdatos_personas_nacional.zip (muestra con factor de elevación; ine.es/ftp/microdatos/censopv/cen11/,
  155 MB, no versionado) y su diseño de registro «Personas detallado_WEB.xls».
- 2021: CensoPersonas_2021.zip, ya descargado por src/v11/fetch_ine_censo2021.py (muestra del 10 % de los hogares, sin
  factor).
Persona de referencia COMÚN a los dos censos: la persona de MAYOR edad del hogar (empate: menor NORDEN). El orden de
las personas no significa lo mismo en los dos ficheros (en 2021 NORDEN = 01 es siempre la de más edad; en 2011 no), así
que «primera persona» no sería comparable. Se cuenta un hogar por persona de referencia.
Salida (versionada): data/raw/v11/ine_censos_microdatos/jefatura_{2011,2021}.csv.gz con, por provincia × municipio (o
tamaño de municipio: 991-994) × grupo quinquenal de edad × nacionalidad (ES/EXT): personas y personas de referencia,
elevadas (2011) o muestrales (2021), y los recuentos muestrales. Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_censos_microdatos"
DIR = RAW11 / FUENTE
URL11 = "https://www.ine.es/ftp/microdatos/censopv/cen11/Microdatos_personas_nacional.zip"
URL11_DR = "https://www.ine.es/ftp/microdatos/censopv/cen11/Personas%20detallado_WEB.xls"
ZIP21 = RAW11 / "ine_censo2021/original/CensoPersonas_2021.zip"
LIC = "INE: reutilización con cita (Ley 37/2007)"
# posiciones (1-indexadas) del diseño «Personas detallado_WEB.xls» (2011) y dr_CensoPersonas_2021.xlsx (2021)
P11 = {"CPRO": (1, 2), "CMUN": (3, 3), "IDHUECO": (6, 10), "NORDEN": (16, 4), "FACTOR": (20, 14), "EDAD": (40, 3), "NACI": (44, 3)}
C21 = ["CPRO", "CMUN", "NVIV", "NORDEN", "VAREDAD", "PNACIO", "TAM_HOG"]
CORTES = [-1, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 200]
EDADES = ["0-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69",
          "70-74", "75-79", "80-84", "85+"]


def referencia(hogar: pd.Series, edad: pd.Series, orden: pd.Series) -> pd.Series:
    t = pd.DataFrame({"h": hogar.values, "e": edad.values, "o": orden.values}, index=hogar.index)
    t = t.sort_values(["h", "e", "o"], ascending=[True, False, True])
    return (~t.h.duplicated()).reindex(hogar.index)


def agregar(d: pd.DataFrame, peso: pd.Series, ref: pd.Series) -> pd.DataFrame:
    d = d.assign(peso=peso.values, ref=ref.astype(int).values)
    d["refp"] = d.ref * d.peso
    d["grupo_edad"] = pd.cut(d.edad, CORTES, labels=EDADES).astype(str)
    return (d.groupby(["cpro", "cmun", "grupo_edad", "nac"])
            .agg(personas=("peso", "sum"), personas_muestra=("peso", "size"), referencias=("refp", "sum"), referencias_muestra=("ref", "sum"))
            .reset_index())


def censo2011() -> Path:
    zp = descargar(URL11, DIR / "original" / "Microdatos_personas_nacional.zip", timeout=3600)
    descargar(URL11_DR, DIR / "original" / "Personas_detallado_WEB.xls", timeout=300)
    with zipfile.ZipFile(zp) as z, z.open(next(n for n in z.namelist() if n.lower().endswith(".txt"))) as f:
        d = pd.read_fwf(io.TextIOWrapper(f, encoding="latin-1"), colspecs=[(i - 1, i - 1 + n) for i, n in P11.values()],
                        names=list(P11), dtype=str, header=None, keep_default_na=False)
    d["edad"] = pd.to_numeric(d.EDAD)
    d["nac"] = np.where(d.NACI.str.strip() == "108", "ES", "EXT")
    d["cpro"], d["cmun"] = d.CPRO, d.CMUN
    g = agregar(d, pd.to_numeric(d.FACTOR), referencia(d.IDHUECO, d.edad, pd.to_numeric(d.NORDEN)))
    r = DIR / "jefatura_2011.csv.gz"
    g.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, URL11, edicion="Censo 2011, microdatos de personas (muestra con factor de elevación)", periodo="2011-11-01",
              nivel_territorial="provincia × municipio > 20.000 hab. (991-994: tamaños de municipio)", licencia=LIC, redistribuible=True,
              notas=f"persona de referencia = mayor edad del hogar; hogares elevados={g.referencias.sum():.0f}")
    return r


def censo2021() -> Path:
    with zipfile.ZipFile(ZIP21) as z, z.open(next(n for n in z.namelist() if n.lower().endswith(".tab"))) as f:
        d = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep="\t", dtype=str, keep_default_na=False, usecols=lambda c: c in C21)
    d = d[d.TAM_HOG.str.strip() != "9"].copy()   # 9 = no aplicable (no reside en vivienda familiar)
    d["edad"] = pd.to_numeric(d.VAREDAD)
    d["nac"] = np.where(d.PNACIO.str.strip() == "108", "ES", "EXT")
    d["cpro"], d["cmun"] = d.CPRO, d.CMUN
    ref = referencia(d.CPRO + d.CMUN + d.NVIV, d.edad, pd.to_numeric(d.NORDEN))
    g = agregar(d, pd.Series(1.0, index=d.index), ref)
    r = DIR / "jefatura_2021.csv.gz"
    g.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, "https://www.ine.es/ftp/microdatos/censopv/cen21/CensoPersonas_2021.zip",
              edicion="Censo 2021, microdatos de personas (muestra 10 % de hogares, sin factor)", periodo="2021-01-01",
              nivel_territorial="provincia × municipio ≥ 10.000 hab. (991-993: tamaños de municipio)", licencia=LIC, redistribuible=True,
              notas=f"persona de referencia = mayor edad del hogar; hogares de la muestra={int(g.referencias_muestra.sum())}")
    return r


def main(verificar: bool = False) -> int:
    if verificar:
        return verificar_manifiesto(FUENTE)
    DIR.mkdir(parents=True, exist_ok=True)
    for f in (censo2011, censo2021):
        print(f.__name__, f())
    o = DIR / "original" / "Microdatos_personas_nacional.zip"
    registrar(FUENTE, o, URL11, edicion="Censo 2011, microdatos", periodo="2011-11-01", nivel_territorial="microdatos", licencia=LIC,
              redistribuible=True, notas="no versionado (tamaño): se regenera con make datos_v11")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
