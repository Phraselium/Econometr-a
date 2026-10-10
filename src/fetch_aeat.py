"""AEAT: Estadistica de los declarantes del IRPF por municipios (rendimientos del capital inmobiliario).

Estado: NO DESCARGABLE dentro de los terminos de uso del proyecto. Motivo verificado:
  - Las paginas de datos (sede.agenciatributaria.gob.es/AEAT/.../Publicaciones/sites/irpfmunicipios/<año>/)
    muestran la tabla por municipio mediante una consulta dinamica ('Visualizar datos', selectores de
    ambito territorial y tamaño de poblacion) y no enlazan ningun fichero publicado (xls/csv/zip).
  - Descargar esa consulta equivale a scraping de una pagina dinamica, que el proyecto no permite.
  - La estadistica publicada en fichero solo se ha localizado como tabla dinamica; no hay URL de fichero
    verificada. No se inventa ninguna URL ni cifra.
  - Las paginas por partidas (sede.../irpf/<año>/) tampoco enlazan ficheros de datos (solo CSS/HTML).

Este script hace una unica peticion pequeña a la pagina de metodologia 2022 para dejar constancia de la
disponibilidad y termina con codigo 0 (no rompe `make data`). No escribe CSV en data/raw.
Detalle, URLs probadas y alternativas: docs/v2/fuentes_fallidas.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import HEADERS  # noqa: E402

PAGINA_2022 = ("https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/"
               "Estadisticas/Publicaciones/sites/irpfmunicipios/2022/docf763858820a87bad202022caf95a9d485a438a37a.html")


def main() -> int:
    try:
        r = requests.get(PAGINA_2022, headers=HEADERS, timeout=60)
    except requests.RequestException as e:  # noqa: BLE001
        print(f"[aeat] sin conexion con la sede: {e}")
        return 0
    if r.status_code != 200:
        print(f"[aeat] HTTP {r.status_code} en la pagina de metodologia 2022")
        return 0
    enlaces_fichero = [h for h in re.findall(r'href="([^"]+)"', r.text)
                       if re.search(r"\.(xlsx?|csv|zip)(\?|$)", h, re.I)]
    if enlaces_fichero:
        print(f"[aeat] enlaces a ficheros detectados ({len(enlaces_fichero)}): revisar a mano antes de escribir fetch")
    else:
        print("[aeat] sin fichero descargable publicado en la pagina 2022: la tabla municipal es dinamica. "
              "No se descarga (ver docs/v2/fuentes_fallidas.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
