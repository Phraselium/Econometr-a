"""INE · Encuesta de Presupuestos Familiares (EPF) · microdatos y documentación localizados.

Localización: página de operación INE (Base 2006, cid=1254736176806), sección «Microdatos (ficheros)».
Verificado por cabecera HTTP el 2026-10-17:
  - epf2006/datos_epf2006.zip (microdatos EPF 2006, 24,8 MB)
  - epf2006/disreg_epf.zip (diseño de registro)
  - epf2006/Corresp_COICOP_2018_ECOICOP.xlsx (equivalencias de clasificación)
  - epf_bienestar/datos_epf_bienestar.zip y disreg_epf_bienestar.zip (módulo de bienestar)
NO localizado: microdatos EPF 2007-2015 y 2016-2025. Los patrones probados (epf<año>/datos_epf<año>.zip,
epf<año>/datos_epf.zip) dan 404. Ver docs/v16/fuentes/renta_parque.md.
Ejecutar: python3 -I descarga_epf.py
"""
import datetime as dt
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

BASE = "https://www.ine.es/ftp/microdatos"
LICENCIA = ("INE: microdatos y documentación; reutilización con cita de la fuente (Ley 37/2007);"
            " aviso legal https://www.ine.es/aviso_legal. La página de la operación indica CC BY-SA 4.0"
            " en el pie pero enlaza CC BY 4.0 (discrepancia no resuelta)")

ITEMS = [
    ("epf2006/datos_epf2006.zip", "epf/epf2006/datos_epf2006.zip", "EPF base 2006, microdatos año 2006", "2006"),
    ("epf2006/disreg_epf.zip", "epf/epf2006/disreg_epf.zip", "EPF base 2006, diseño de registro", "2006"),
    ("epf2006/Corresp_COICOP_2018_ECOICOP.xlsx", "epf/epf2006/Corresp_COICOP_2018_ECOICOP.xlsx",
     "EPF, equivalencia ECOICOP / COICOP 2018", "2006-2025"),
    ("epf_bienestar/datos_epf_bienestar.zip", "epf/bienestar/datos_epf_bienestar.zip",
     "EPF módulo de bienestar, microdatos", "según módulo"),
    ("epf_bienestar/disreg_epf_bienestar.zip", "epf/bienestar/disreg_epf_bienestar.zip",
     "EPF módulo de bienestar, diseño de registro", "según módulo"),
]


def main():
    hoy = dt.date.today().isoformat()
    filas = []
    for ruta_url, ruta_local, desc, periodo in ITEMS:
        url = f"{BASE}/{ruta_url}"
        destino = os.path.join(au.FAMILIA_DIR, ruta_local)
        estado, nbytes = au.descargar(url, destino)
        nota_zip = ""
        if destino.endswith(".zip"):
            with zipfile.ZipFile(destino) as z:  # solo listado
                nota_zip = f"{len(z.namelist())} ficheros internos; integridad zip: {'OK' if z.testzip() is None else 'ERROR'}; "
        filas.append({
            "fuente": "INE EPF (microdatos y documentación)",
            "fichero": os.path.relpath(destino, au.RAIZ),
            "url": url,
            "fecha_descarga": hoy,
            "edicion": f"{desc}; ruta {ruta_url}",
            "periodo": periodo,
            "nivel_territorial": "hogar y miembros (nacional; sin desagregación territorial en el fichero)",
            "n_filas": "",
            "sha256": au.sha256(destino),
            "licencia": LICENCIA,
            "redistribuible": "sí",
            "notas": f"{nota_zip}descarga {estado}; {nbytes} bytes",
        })
        print(ruta_url, estado, nbytes, flush=True)
    au.upsert(filas)


if __name__ == "__main__":
    main()
