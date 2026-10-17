"""INE · ECV · microdatos que faltan en el repositorio (completa la serie).

Ya en el repositorio (no se descargan): transversal 2018-2025 (data/raw/v9/ine_microdatos/ecv/).
Esta descarga añade:
  a) transversal 2004-2012 (ecv_b2004/ecvb04_<año>.zip)                -> ecv/transversal_2004_2012/
  b) longitudinal base 2004, periodos 2004-2007 ... 2009-2012 (ecv_b2004/periodo_<f>-<l>.zip)
  c) longitudinal base 2013, periodos 2008-2011 ... 2016-2019 (ecv_b2013/periodo_<f>-<l>.zip)
NO se descargan (volumen agregado ~510 MB; decisión pendiente del autor, ver ficha):
  longitudinal base 2013 periodos 2017-2020 ... 2022-2025.
Las URL y el patrón de nombres proceden de mvazcar/ECV (config.py), verificados por cabecera HTTP.
Ejecutar: python3 -I descarga_ecv_resto.py
"""
import datetime as dt
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

BASE = "https://www.ine.es/ftp/microdatos/ecv"
LICENCIA = ("INE: microdatos anonimizados, descarga libre y reutilización con cita (aviso legal del INE,"
            " https://www.ine.es/aviso_legal)")

CATALOGO = []
for y in range(2004, 2013):
    CATALOGO.append((f"ecv_b2004/ecvb04_{y}.zip", f"ecv/transversal_2004_2012/ecvb04_{y}.zip",
                     f"ECV transversal base 2004, año {y}", str(y)))
for f, l in [(2004, 2007), (2004, 2006), (2004, 2005), (2005, 2008), (2006, 2009),
             (2007, 2010), (2008, 2011), (2009, 2012)]:
    CATALOGO.append((f"ecv_b2004/periodo_{f}-{l}.zip", f"ecv/longitudinal/b2004_periodo_{f}-{l}.zip",
                     f"ECV longitudinal base 2004, periodo {f}-{l}", f"{f}-{l}"))
for f in range(2008, 2020):
    if f + 3 > 2019:
        break
    CATALOGO.append((f"ecv_b2013/periodo_{f}-{f + 3}.zip", f"ecv/longitudinal/b2013_periodo_{f}-{f + 3}.zip",
                     f"ECV longitudinal base 2013, periodo {f}-{f + 3}", f"{f}-{f + 3}"))


def main():
    hoy = dt.date.today().isoformat()
    filas = []
    for ruta_url, ruta_local, desc, periodo in CATALOGO:
        url = f"{BASE}/{ruta_url}"
        destino = os.path.join(au.FAMILIA_DIR, ruta_local)
        estado, nbytes = au.descargar(url, destino)
        with zipfile.ZipFile(destino) as z:  # solo listado; no se extrae nada
            nficheros = len(z.namelist())
            zbad = z.testzip()
        filas.append({
            "fuente": "INE ECV (microdatos)",
            "fichero": os.path.relpath(destino, au.RAIZ),
            "url": url,
            "fecha_descarga": hoy,
            "edicion": f"{desc}; ruta {ruta_url}",
            "periodo": periodo,
            "nivel_territorial": "individuos y hogares (nacional; sin desagregación territorial fina)",
            "n_filas": "",
            "sha256": au.sha256(destino),
            "licencia": LICENCIA,
            "redistribuible": "sí",
            "notas": (f"ZIP original, {nficheros} ficheros internos; integridad zip:"
                      f" {'OK' if zbad is None else 'ERROR ' + zbad}; descarga {estado}; {nbytes} bytes"),
        })
        print(ruta_url, estado, nbytes, nficheros, zbad, flush=True)
    au.upsert(filas)


if __name__ == "__main__":
    main()
