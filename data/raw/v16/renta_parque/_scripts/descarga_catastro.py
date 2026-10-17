"""Dirección General del Catastro · estadísticas catastrales municipales (urbana), edición 2026.

Solo se descarga la edición que el repositorio no tiene: URBANA2026.xls (referencia 2026-01-01).
Ya en el repositorio: data/raw/catastro_urbana_municipios.csv(.gz) (2011-2025) y
data/raw/v4/catastro_solares_municipios.csv.gz (extracto 2012-2026 de URBANA2012-2026.xls, 7.610 municipios).
Verificado por cabecera HTTP el 2026-10-17: URBANA2026.xls (4.072.191 bytes).
Descarga masiva alfanumérica (registro con certificado): NO intentada; ver docs/v16/fuentes/renta_parque.md.
Ejecutar: python3 -I descarga_catastro.py
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

URL = "https://www.catastro.hacienda.gob.es/documentos/estadisticas/URBANA2026.xls"
DESTINO = os.path.join(au.FAMILIA_DIR, "catastro", "URBANA2026.xls")
LICENCIA = ("Catastro (DGC): reutilización libre con reconocimiento de la fuente (inventario V15,"
            " docs/v5/licencias_datos.md); aviso legal https://www.sedecatastro.gob.es/")


def main():
    hoy = dt.date.today().isoformat()
    estado, nbytes = au.descargar(URL, DESTINO)
    with open(DESTINO, "rb") as f:
        cabecera = f.read(8)
    formato_ok = cabecera[:4] == b"\xd0\xcf\x11\xe0"  # OLE2 (xls)
    au.upsert([{
        "fuente": "Catastro · estadísticas catastrales municipales (urbana)",
        "fichero": os.path.relpath(DESTINO, au.RAIZ),
        "url": URL,
        "fecha_descarga": hoy,
        "edicion": "URBANA2026 (fecha de referencia 2026-01-01)",
        "periodo": "2026-01-01",
        "nivel_territorial": "municipio (urbano)",
        "n_filas": "",
        "sha256": au.sha256(DESTINO),
        "licencia": LICENCIA,
        "redistribuible": "sí",
        "notas": (f"Libro Excel original; cabecera OLE2 {'OK' if formato_ok else 'NO RECONOCIDA'};"
                  f" descarga {estado}; {nbytes} bytes; el repositorio tenía 2026 solo en el extracto"
                  " de variables de solar (v4) y 2011-2025 en catastro_urbana_municipios.csv"),
    }])
    print(estado, nbytes, formato_ok)


if __name__ == "__main__":
    main()
