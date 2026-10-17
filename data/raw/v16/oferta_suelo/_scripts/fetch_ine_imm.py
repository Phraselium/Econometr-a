#!/usr/bin/env python3
"""V16 · oferta_suelo · INE IMM (índices de precios de materiales y mano de obra en construcción).

Descarga las tablas originales de la API de INE (servicios.ine.es/wstempus, uso libre con cita).
Caché: si el fichero existe no se vuelve a bajar salvo FORCE=1.
Escribe JSON original sin transformar y añade sus sha256 al manifiesto de la familia.
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

RAIZ = "/home/user/Econometr-a/data/raw/v16/oferta_suelo"
DESTINO = os.path.join(RAIZ, "ine_imm")
UA = "Econometria-V16-adquisidor (proyecto academico; contacto: autor del repositorio)"
TABLAS = {
    "8381": "Índices de precios de materiales generales (base diciembre 2011)",
    "8382": "Índices de precios de materiales específicos (base diciembre 2011)",
    "8377": "Índice nacional de la mano de obra en construcción (base julio 1980)",
}
FORCE = os.environ.get("FORCE") == "1"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def bajar(tabla):
    url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/%s" % tabla
    ruta = os.path.join(DESTINO, "imm_%s.json" % tabla)
    if os.path.exists(ruta) and not FORCE:
        print("cache", ruta)
        return url, ruta, None
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        cuerpo = r.read()
    with open(ruta, "wb") as f:
        f.write(cuerpo)
    time.sleep(1.0)  # límite de frecuencia educado
    return url, ruta, datetime.now(timezone.utc).strftime("%Y-%m-%d")


def ultima_fecha(ruta):
    with open(ruta, encoding="utf-8") as f:
        d = json.load(f)
    fechas = []
    for serie in d:
        for p in serie.get("Data", []):
            fechas.append((p["Anyo"], p["FK_Periodo"], p["Valor"]))
    fechas.sort()
    n = sum(len(s.get("Data", [])) for s in d)
    return n, fechas[0] if fechas else None, fechas[-1] if fechas else None


def main():
    os.makedirs(DESTINO, exist_ok=True)
    filas = []
    for t, desc in TABLAS.items():
        url, ruta, fecha = bajar(t)
        n, primera, ultima = ultima_fecha(ruta)
        filas.append((t, desc, url, ruta, fecha or "cache", n, primera, ultima, sha256(ruta)))
    for f in filas:
        print("|".join(str(x) for x in f))
    return 0


if __name__ == "__main__":
    sys.exit(main())
