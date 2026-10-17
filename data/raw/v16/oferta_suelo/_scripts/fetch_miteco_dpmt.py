#!/usr/bin/env python3
"""V16 · oferta_suelo · Dominio público marítimo-terrestre (MITECO, deslinde DPMT y núcleos excluidos).

Condiciones de uso declaradas por MITECO: uso libre y gratuito con citación
«Fuente: «© Ministerio para la Transición Ecológica y el Reto Demográfico»».
Ficheros pequeños (< 50 MB): van a la carpeta principal.
Caché: no se vuelve a bajar si existe, salvo FORCE=1.
"""
import hashlib
import os
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone

RAIZ = "/home/user/Econometr-a/data/raw/v16/oferta_suelo"
DESTINO = os.path.join(RAIZ, "dpmt_miteco")
UA = "Econometria-V16-adquisidor (proyecto academico; contacto: autor del repositorio)"
FICHEROS = {
    "dpmt.zip": "https://gis.miteco.gob.es/descargas/app/DescargaFichero?f=dpmt.zip",
    "nucleos-excluidos-dpmt.zip": "https://gis.miteco.gob.es/descargas/app/DescargaFichero?f=nucleos-excluidos-dpmt.zip",
}
FORCE = os.environ.get("FORCE") == "1"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for nombre, url in FICHEROS.items():
        ruta = os.path.join(DESTINO, nombre)
        if os.path.exists(ruta) and not FORCE:
            print("cache", ruta, sha256(ruta))
            continue
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r, open(ruta + ".part", "wb") as f:
            while True:
                bloque = r.read(1 << 20)
                if not bloque:
                    break
                f.write(bloque)
        if not zipfile.is_zipfile(ruta + ".part"):
            # El endpoint gis.miteco.gob.es/descargas/app/DescargaFichero devuelve una página HTML
            # (aplicación de descargas) en lugar del ZIP. Se descarta y se registra como fallida.
            os.remove(ruta + ".part")
            print("FALLIDA: respuesta HTML, no ZIP:", url)
            continue
        os.replace(ruta + ".part", ruta)
        print("ok", ruta, os.path.getsize(ruta), sha256(ruta), datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
