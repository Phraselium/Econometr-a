"""V11-DATOS (bloque 1, punto 2): INE, Estadística de Migraciones y Cambios de Residencia (EMCR), desde 2021.

1. Microdatos anuales 2021-2024 (https://www.ine.es/ftp/microdatos/emcr/datos_<año>.zip; diseño dr_emcr_Desde2021.xlsx):
   cada registro es una migración (TIPO_MIGR: IE inmigración exterior, EE emigración exterior, MI interior) con municipio
   de procedencia y de destino (blanqueado si < 10.000 hab. → PP999), país de nacionalidad, de nacimiento y de
   procedencia o destino, sexo y edad. Se agregan igual que la EVR (fetch_ine_evr.py):
   - od_municipios_<año>.parquet (interior; no versionado);
   - saldos_internos_municipio.csv.gz (altas, bajas y saldo interior por municipio × año × nacionalidad ES/EXT × edad);
   - flujos_exterior_municipio.csv.gz (inmigración y emigración exterior por municipio × año × país de nacionalidad).
2. Tablas municipales (jaxiT3): 69696 y 69711 (exterior por municipio y sexo), 69743-69746 (intermunicipales por
   municipio y nacionalidad o país de nacimiento), 69767 (saldos por municipio y tipo), 75690 (área submunicipal).
Antes de 2021, la EM (2008-2021) solo tiene tablas provinciales (ya en data/raw/v9/ine_migraciones); el nivel municipal
anterior a 2021 lo da la EVR (fetch_ine_evr.py). Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, abrir_gz_texto, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_emcr"
DIR = RAW11 / FUENTE
URL = "https://www.ine.es/ftp/microdatos/emcr/datos_{a}.zip"
URL_T = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1"
ANIOS = range(2021, 2025)
TABLAS = {69696: "inmigración exterior por municipio y sexo", 69711: "emigración exterior por municipio y sexo",
          69743: "inmigraciones intermunicipales por municipio de destino y nacionalidad",
          69744: "inmigraciones intermunicipales por municipio de destino y país de nacimiento",
          69745: "emigraciones intermunicipales por municipio de procedencia y nacionalidad",
          69746: "emigraciones intermunicipales por municipio de procedencia y país de nacimiento",
          69767: "saldos por municipio y tipo de saldo", 75690: "migraciones por área submunicipal y país de nacimiento"}
LIC = "INE: reutilización con cita (Ley 37/2007)"
ESPANA = "108"
EDAD = [-1, 15, 34, 64, 200]
EDAD_LAB = ["0-15", "16-34", "35-64", "65+"]
ANCHO = {"ANYO": (10, 14), "TIPO_MIGR": (16, 18), "SEXO": (18, 19), "EDAD": (28, 31), "PAIS_NACIO": (35, 38),
         "PAIS_PROC_DEST": (38, 41), "PROVDEST": (41, 43), "MUNIDEST": (43, 46), "PROVPROC": (47, 49), "MUNIPROC": (49, 52)}


def cod(prov: pd.Series, mun: pd.Series) -> np.ndarray:
    p = prov.astype(str).str.strip().str.zfill(2)
    m = mun.astype(str).str.strip()
    return np.where(p == "00", "", np.where(m == "", p + "999", p + m.str.zfill(3)))


def leer(zp: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zp) as z:
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if csvs:
            with z.open(csvs[0]) as f:
                d = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep="\t", dtype=str, keep_default_na=False,
                                usecols=list(ANCHO))
        else:
            nombre = next(n for n in z.namelist() if n.lower().endswith(".txt") and "leeme" not in n.lower())
            with z.open(nombre) as f:
                d = pd.read_fwf(io.TextIOWrapper(f, encoding="latin-1"), colspecs=list(ANCHO.values()), names=list(ANCHO),
                                dtype=str, header=None, keep_default_na=False)
    d["tipo"] = d.TIPO_MIGR.str.strip()
    d["destino"] = cod(d.PROVDEST, d.MUNIDEST)
    d["origen"] = cod(d.PROVPROC, d.MUNIPROC)
    d["nac"] = np.where(d.PAIS_NACIO.str.strip() == ESPANA, "ES", "EXT")
    d["edad_g"] = pd.cut(pd.to_numeric(d.EDAD, errors="coerce"), EDAD, labels=EDAD_LAB).astype(str)
    d["sexo"] = d.SEXO.str.strip().map({"1": "H", "6": "M"}).fillna("?")
    return d


def tablas() -> list[Path]:
    rutas = []
    for t, desc in TABLAS.items():
        r = None
        for _ in range(3):
            try:
                r = requests.get(URL_T.format(t=t), headers=CABECERAS, timeout=900)
                r.raise_for_status()
                break
            except Exception:  # noqa: BLE001
                r = None
        if r is None:
            print("FALLO tabla", t)
            continue
        lector = csv.reader(io.StringIO(r.content.decode("utf-8-sig", "replace")), delimiter=";")
        cab = next(lector)
        i_sexo = cab.index("Sexo") if "Sexo" in cab else None
        filas = [f for f in lector if len(f) == len(cab) and (i_sexo is None or f[i_sexo] in ("Total", "Ambos sexos"))]
        ruta = DIR / f"emcr_t{t}.csv.gz"
        with abrir_gz_texto(ruta) as g:
            w = csv.writer(g)
            w.writerow(cab)
            w.writerows(filas)
        per = sorted({f[cab.index("Periodo")] for f in filas})
        registrar(FUENTE, ruta, URL_T.format(t=t), edicion=f"INE EMCR, tabla {t} (jaxiT3)", periodo=f"{per[0]}–{per[-1]}",
                  nivel_territorial="municipio (código en la etiqueta)" if t != 75690 else "área submunicipal",
                  licencia=LIC, redistribuible=True, notas=f"{desc}; sexo = total; filas={len(filas)}")
        rutas.append(ruta)
        print("tabla", t, len(filas), per[0], per[-1])
    return rutas


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    tablas()
    saldos, exter = [], []
    for a in ANIOS:
        try:
            zp = descargar(URL.format(a=a), DIR / "original" / f"datos_{a}.zip", timeout=1800)
        except RuntimeError as e:
            print("FALLO", a, e)
            continue
        d = leer(zp)
        mi = d[d.tipo == "MI"]
        od = mi.groupby(["origen", "destino", "nac", "sexo", "edad_g"]).size().rename("n").reset_index()
        od.insert(0, "anio", a)
        od.to_parquet(DIR / f"od_municipios_{a}.parquet", index=False, compression="zstd")
        alt = mi.groupby(["destino", "nac", "edad_g"]).size().rename("altas")
        baj = mi.groupby(["origen", "nac", "edad_g"]).size().rename("bajas")
        alt.index.names = baj.index.names = ["cod_municipio", "nac", "edad_g"]
        s = pd.concat([alt, baj], axis=1).fillna(0).astype(int).reset_index()
        s["saldo"] = s.altas - s.bajas
        s.insert(0, "anio", a)
        saldos.append(s)
        ie = d[d.tipo == "IE"].groupby(["destino", "PAIS_NACIO"]).size().rename("inmigracion_exterior")
        ee = d[d.tipo == "EE"].groupby(["origen", "PAIS_NACIO"]).size().rename("emigracion_exterior")
        ie.index.names = ee.index.names = ["cod_municipio", "pais_nacionalidad"]
        e = pd.concat([ie, ee], axis=1).fillna(0).astype(int).reset_index()
        e.insert(0, "anio", a)
        exter.append(e)
        print(a, len(d), d.tipo.value_counts().to_dict())
    if not saldos:
        return 1
    S = pd.concat(saldos, ignore_index=True).sort_values(["anio", "cod_municipio", "nac", "edad_g"])
    E = pd.concat(exter, ignore_index=True).sort_values(["anio", "cod_municipio", "pais_nacionalidad"])
    r1, r2 = DIR / "saldos_internos_municipio.csv.gz", DIR / "flujos_exterior_municipio.csv.gz"
    S.to_csv(r1, index=False, compression=GZ_PANDAS)
    E.to_csv(r2, index=False, compression=GZ_PANDAS)
    per = f"{S.anio.min()}-{S.anio.max()}"
    for r, nota in ((r1, "migraciones interiores (MI): altas, bajas y saldo; nac ES/EXT; edad en 4 grupos"),
                    (r2, "inmigración (IE) y emigración (EE) exterior por país de nacionalidad (108 = España)")):
        registrar(FUENTE, r, URL.format(a="<año>"), edicion="EMCR microdatos 2021-2024 (ftp INE)", periodo=per,
                  nivel_territorial="municipio ≥10.000 hab. (PP999 = resto de provincia)", licencia=LIC, redistribuible=True, notas=nota)
    for a in ANIOS:
        p = DIR / f"od_municipios_{a}.parquet"
        if p.exists():
            registrar(FUENTE, p, URL.format(a=a), edicion=f"EMCR {a} (agregado propio)", periodo=str(a),
                      nivel_territorial="municipio × municipio", licencia=LIC, redistribuible=True,
                      notas="no versionado (tamaño): se regenera con make datos_v11")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
