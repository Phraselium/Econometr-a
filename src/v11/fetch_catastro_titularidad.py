"""V11-DATOS, segunda pasada (Catastro): estadística de TITULARIDAD por municipio (padrón del IBI urbano), sede del
Catastro, «Estadísticas → Titularidad» (página dinámica; los CSV siguen el patrón
https://www.catastro.hacienda.gob.es/documentos/estadisticas/propietarios/<año>/<fichero>.csv, leído del JavaScript de
la página renderizada con Chromium sin interfaz):
- P_SPI_mun_U: sujetos pasivos e inmuebles urbanos por municipio, tramo de nº de inmuebles del titular
  (1, ≤5, ≤10, ≤25, ≤100, >100) y tipo de persona (PF física, PJ jurídica, PE entidad, PD otros);
- P_SPI_mun_V: idem, inmuebles de uso residencial (viviendas);
- P_SPI_mun_V_TPF: viviendas por tramo y tipo detallado de titular (física nacional o extranjera, sociedades,
  entidades, administraciones públicas…).
Cruce por CODINE (código INE del municipio). Licencia Catastro: reutilización libre con cita. Se prueban todos los años
2006-2026; los años sin fichero quedan anotados. Responde en parte a la solicitud 2 (titularidad agregada).
Valores de referencia: la sede no publica estadística descargable (solo metodología y consulta individual).
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "catastro_titularidad"
DIR = RAW11 / FUENTE
URL = "https://www.catastro.hacienda.gob.es/documentos/estadisticas/propietarios/{a}/{f}.csv"
LIC = "Catastro (DGC): reutilización libre con reconocimiento de la fuente"
FICHEROS = {"P_SPI_mun_U": "inmuebles urbanos", "P_SPI_mun_V": "inmuebles de uso residencial",
            "P_SPI_mun_V_TPF": "viviendas por tipo detallado de titular",
            # V12: mismos indicadores por ámbito nacional, autonómico y provincial. Los tramos se cuentan DENTRO de cada
            # ámbito (comprobado: suma municipal de viviendas de PJ con >100 = 139.295 frente a 290.427 en el total
            # nacional de 2025), así que la concentración municipal es una cota inferior de la nacional.
            "P_SPI_total_V": "total nacional, uso residencial", "P_SPI_aut_V": "comunidades autónomas, uso residencial",
            "P_SPI_prov_V": "provincias, uso residencial", "P_SPI_total_V_TPF": "total nacional, tipo detallado de titular",
            "P_SPI_prov_V_TPF": "provincias, tipo detallado de titular"}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for f, desc in FICHEROS.items():
        partes, faltan = [], []
        for a in range(2006, 2027):
            r = requests.get(URL.format(a=a, f=f), headers=CABECERAS, timeout=120)
            txt = r.content.decode("latin-1")
            if r.status_code != 200 or not txt.startswith("AREF"):
                faltan.append(a)
                continue
            d = pd.read_csv(io.StringIO(txt), sep=";", dtype=str, keep_default_na=False)
            d.insert(0, "anio_fichero", a)
            partes.append(d)
        if not partes:
            print("sin datos", f)
            continue
        D = pd.concat(partes, ignore_index=True)
        if "CODINE" in D:
            D["CODINE"] = D.CODINE.str.zfill(5)
        out = DIR / f"{f.lower()}.csv.gz"
        D.to_csv(out, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, out, URL.format(a="<año>", f=f), edicion="Catastro, estadística de titularidad (padrón IBI urbano)",
                  periodo=f"{D.anio_fichero.min()}-{D.anio_fichero.max()}", nivel_territorial="municipio (CODINE = código INE)",
                  licencia=LIC, redistribuible=True, notas=f"{desc}; años sin fichero: {faltan}; filas={len(D)}")
        print(f, len(D), D.anio_fichero.min(), D.anio_fichero.max(), "faltan", faltan)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
