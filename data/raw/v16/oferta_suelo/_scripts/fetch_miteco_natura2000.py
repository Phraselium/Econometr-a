#!/usr/bin/env python3
"""V16 · oferta_suelo · Red Natura 2000 (MITECO, Banco de Datos de la Naturaleza), edición 2025.

Licencia no verificada en la página (solo enlace a aviso legal): redistribuible = dudoso.
Por eso el fichero va a _terceros/_grandes (no versionado) con sha256 en el manifiesto.
Caché: no se vuelve a bajar si existe, salvo FORCE=1.
"""
import hashlib
import os
import sys
import urllib.request
from datetime import datetime, timezone

RAIZ = "/home/user/Econometr-a/data/raw/v16/oferta_suelo"
DESTINO = os.path.join(RAIZ, "_terceros", "_grandes")
UA = "Econometria-V16-adquisidor (proyecto academico; contacto: autor del repositorio)"
BASE = "https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/servicios/banco-datos-naturaleza/3-rn2000/"
FICHEROS = ["n2000_2025_shp.zip"]
FORCE = os.environ.get("FORCE") == "1"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for nombre in FICHEROS:
        ruta = os.path.join(DESTINO, nombre)
        if os.path.exists(ruta) and not FORCE:
            print("cache", ruta, sha256(ruta))
            continue
        req = urllib.request.Request(BASE + nombre, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r, open(ruta + ".part", "wb") as f:
            while True:
                bloque = r.read(1 << 20)
                if not bloque:
                    break
                f.write(bloque)
        os.replace(ruta + ".part", ruta)
        print("ok", ruta, os.path.getsize(ruta), sha256(ruta), datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
