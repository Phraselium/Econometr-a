"""INE · ECV (Encuesta de Condiciones de Vida) · microdatos transversales 2013-2017 que faltan en el repositorio.

Ya existían en el repositorio (no se descargan de nuevo): ECV 2018-2025 en data/raw/v9/ine_microdatos/ecv/.
Origen: https://www.ine.es/ftp/microdatos/ecv/ecv_b2013/datos_<año>.zip (cabecera HTTP verificada 2026-10-17).
Salida: data/raw/v16/renta_parque/ecv/datos_<año>.zip (todos < 50 MB). Caché salvo FORCE=1.
Ejecutar: python3 -I descarga_ecv.py
"""
import datetime as dt
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

ANIOS = [2013, 2014, 2015, 2016, 2017]
LICENCIA = ("INE: microdatos anonimizados, descarga libre y reutilización con cita (aviso legal del INE,"
            " https://www.ine.es/aviso_legal)")


def main():
    hoy = dt.date.today().isoformat()
    filas = []
    for y in ANIOS:
        url = f"https://www.ine.es/ftp/microdatos/ecv/ecv_b2013/datos_{y}.zip"
        destino = os.path.join(au.FAMILIA_DIR, "ecv", f"datos_{y}.zip")
        estado, nbytes = au.descargar(url, destino)
        with zipfile.ZipFile(destino) as z:  # solo listado; no se extrae nada
            nficheros = len(z.namelist())
            zbad = z.testzip()
        filas.append({
            "fuente": "INE ECV (microdatos transversales)",
            "fichero": os.path.relpath(destino, au.RAIZ),
            "url": url,
            "fecha_descarga": hoy,
            "edicion": f"ECV ecv_b2013, año {y}; cabecera Last-Modified verificada en 2026-10-17",
            "periodo": str(y),
            "nivel_territorial": "individuos y hogares (nacional; sin desagregación territorial fina)",
            "n_filas": "",
            "sha256": au.sha256(destino),
            "licencia": LICENCIA,
            "redistribuible": "sí",
            "notas": (f"ZIP original, {nficheros} ficheros internos; integridad zip:"
                      f" {'OK' if zbad is None else 'ERROR ' + zbad}; descarga {estado}; {nbytes} bytes"),
        })
        print(y, estado, nbytes, nficheros, zbad)
    au.upsert(filas)


if __name__ == "__main__":
    main()
