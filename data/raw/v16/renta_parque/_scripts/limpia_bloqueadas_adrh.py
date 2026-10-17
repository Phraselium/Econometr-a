"""Limpieza ADRH: la API devuelve {"status": "No puede mostrarse por restricciones de volumen"} para
108 tablas (incluso con nult=1). Esos ficheros de 62-113 bytes no son datos: se eliminan y sus filas
salen del manifiesto. Las tablas quedan registradas como fuente fallida en docs/v16/fuentes/renta_parque.md.
La lista de tablas bloqueadas se toma de los ficheros que son respuestas de error (tamaño < 1000 bytes
y contenido JSON tipo objeto), sin leer el resto de la carpeta.
Ejecutar: python3 -I limpia_bloqueadas_adrh.py
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

CARPETA = os.path.join(au.FAMILIA_DIR, "_grandes", "adrh")


def es_error(ruta):
    with gzip.open(ruta, "rb") as f:
        return isinstance(json.loads(f.read().decode("utf-8")), dict)


def main():
    bloqueadas = []
    for f in sorted(os.listdir(CARPETA)):
        if not f.endswith(".json.gz") or f == "tablas_adrh.json.gz":
            continue
        ruta = os.path.join(CARPETA, f)
        if os.path.getsize(ruta) < 1000 and es_error(ruta):
            bloqueadas.append(f[: -len(".json.gz")])
            os.remove(ruta)
    rutas = {os.path.join("data/raw/v16/renta_parque/_grandes/adrh", f"{t}.json.gz") for t in bloqueadas}
    manifiesto = au.leer_manifiesto()
    for r in rutas:
        manifiesto.pop(r, None)
    au.escribir_manifiesto(manifiesto)
    with open(os.path.join(CARPETA, "bloqueadas_volumen.txt"), "w", encoding="utf-8") as f:
        f.write(" ".join(bloqueadas) + "\n")
    print("eliminadas (respuesta de error):", len(bloqueadas))


if __name__ == "__main__":
    main()
