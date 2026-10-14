"""V9-DATOS · INE, Censo anual de población (operación CENSOP), ediciones 2021-2025.

Descarga (jaxiT3, CSV con códigos INE en la etiqueta) y convierte a formato largo con códigos INE como texto:
  1. «Población por sexo y país de nacionalidad (principales países)»: una tabla por provincia (y una nacional), con
     sección censal. Se guarda solo sexo = Total (los totales por sexo están en la tabla 68065):
     censo_seccion_pais.csv.gz: edicion, cod_provincia, cod_municipio, cod_seccion (10 dígitos; vacío en filas de
     municipio o provincia), nivel (provincia/municipio/seccion), pais_nacionalidad, poblacion.
  2. Tabla 68065 «Población por sexo» por municipio: censo_municipio_sexo.csv.gz (edicion, cod_municipio, sexo,
     poblacion).
Cruces SOLO por código INE (el código va al principio de cada etiqueta: «44001 Ababuj», «4400101001 Ababuj sección …»);
no se empareja por nombre. La nacionalidad es la agrupación de «principales países» del INE (22 categorías); no hay
detalle por país completo a nivel de sección. Licencia: aviso legal del INE (reutilización con cita, Ley 37/2007).
Uso: python3 src/v9/fetch_ine_censo_anual.py [--verificar]
"""
from __future__ import annotations

import csv
import gzip
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun  # noqa: E402

def comun_gz(ruta):
    return comun.abrir_gz_texto(ruta)


FUENTE = "ine_censo_anual"
DIR = comun.RAW9 / FUENTE
ORIG = DIR / "original"
URL_T = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{}.csv?nocab=1"
URL_OPS = "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/CENSOP"
NOMBRE_PAIS = "Población por sexo y país de nacionalidad (principales países)"
LIC = "INE: reutilización con cita (aviso legal, Ley 37/2007)"
FICH = {"seccion": DIR / "censo_seccion_pais.csv.gz", "municipio": DIR / "censo_municipio_sexo.csv.gz"}


def codigo(etiqueta: str) -> str:
    m = re.match(r"^\s*(\d+)\s", etiqueta or "")
    return m.group(1) if m else ""


def num(s: str) -> str:
    return (s or "").replace(".", "").replace(",", ".").strip()


TABLA_NACIONAL = 65036   # tabla nacional con todas las secciones (duplica las provinciales y no cabe en memoria): se omite


def tablas_pais() -> list[int]:
    dest = ORIG / "tablas_operacion_censop.json"
    comun.descargar(URL_OPS, dest)
    d = json.loads(dest.read_text(encoding="utf-8"))
    return sorted(x["Id"] for x in d if x["Nombre"].strip() == NOMBRE_PAIS and x["Id"] != TABLA_NACIONAL)


def leer(tid: int):
    dest = ORIG / f"t{tid}.csv.gz"
    if not dest.exists() or comun.FORCE:
        crudo = ORIG / f"t{tid}.csv"
        comun.descargar(URL_T.format(tid), crudo)
        dest.write_bytes(gzip.compress(crudo.read_bytes(), mtime=0))
        crudo.unlink()
    with gzip.open(dest, "rt", encoding="utf-8-sig") as f:
        yield from csv.DictReader(f, delimiter=";")


def construir() -> None:
    ORIG.mkdir(parents=True, exist_ok=True)
    filas = set()
    for tid in tablas_pais():
        for r in leer(tid):
            if r.get("Sexo") != "Total":
                continue
            prov, mun, sec = codigo(r.get("Provincias", "")), codigo(r.get("Municipios", "")), codigo(r.get("Secciones", ""))
            if not prov and not mun:
                continue   # fila nacional de la tabla nacional
            nivel = "seccion" if sec else ("municipio" if mun else "provincia")
            prov = prov or mun[:2]
            filas.add((r["Periodo"], prov.zfill(2), mun.zfill(5) if mun else "", sec.zfill(10) if sec else "", nivel,
                       r["País de nacionalidad"], num(r["Total"])))
    filas = sorted(filas)
    with comun_gz(FICH["seccion"]) as f:
        w = csv.writer(f)
        w.writerow(["edicion", "cod_provincia", "cod_municipio", "cod_seccion", "nivel", "pais_nacionalidad", "poblacion"])
        w.writerows(filas)
    mun = []
    for r in leer(68065):
        c = codigo(r.get("Municipios", ""))
        if c:
            mun.append((r["Periodo"], c.zfill(5), r["Sexo"], num(r["Total"])))
    with comun_gz(FICH["municipio"]) as f:
        w = csv.writer(f)
        w.writerow(["edicion", "cod_municipio", "sexo", "poblacion"])
        w.writerows(sorted(set(mun)))


def verificar() -> int:
    man = DIR / "_manifest.csv"
    if not man.exists():
        return 1
    with open(man, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    ok = [(comun.RAIZ / r["fichero"]).exists() and comun.sha256(comun.RAIZ / r["fichero"]) == r["sha256"] for r in filas]
    return 0 if ok and all(ok) else 1


def main(verificar: bool = False) -> int:
    if verificar:
        return globals()["verificar"]()
    construir()
    comun.registrar(FUENTE, FICH["seccion"], URL_T.format("<tabla por provincia>"), "Censo anual 2021-2025 (CENSOP)", "2021-2025",
                    "sección censal, municipio, provincia", LIC, True,
                    "Principales países de nacionalidad (22 categorías); sexo = Total; códigos INE de la etiqueta")
    comun.registrar(FUENTE, FICH["municipio"], URL_T.format(68065), "Censo anual 2021-2025 (CENSOP), tabla 68065", "2021-2025",
                    "municipio", LIC, True, "Población por sexo")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
