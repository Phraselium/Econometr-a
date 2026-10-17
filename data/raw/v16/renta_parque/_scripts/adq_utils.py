"""Utilidades de adquisición para la familia renta_parque (V16, fase 1).

Caché: si el fichero de destino existe no se vuelve a descargar salvo FORCE=1.
Manifiesto: data/raw/v16/renta_parque/_manifest.csv con columnas exactas.
Ejecutar siempre con python3 -I.
"""
import csv
import gzip
import hashlib
import os
import time
import urllib.request

RAIZ = "/home/user/Econometr-a"
FAMILIA_DIR = os.path.join(RAIZ, "data/raw/v16/renta_parque")
MANIFIESTO = os.path.join(FAMILIA_DIR, "_manifest.csv")
COLUMNAS = [
    "fuente", "fichero", "url", "fecha_descarga", "edicion", "periodo",
    "nivel_territorial", "n_filas", "sha256", "licencia", "redistribuible", "notas",
]
UA = "Mozilla/5.0 (investigacion academica; contacto: autor del proyecto Vivienda Espana)"
FORCE = os.environ.get("FORCE") == "1"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(url, destino, reintentos=4, pausa=2.0, timeout=300):
    """Descarga url a destino (gzip si termina en .gz). Devuelve (estado, bytes)."""
    if os.path.exists(destino) and not FORCE:
        return "cache", os.path.getsize(destino)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    ultimo_error = None
    for intento in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                cuerpo = r.read()
            if not cuerpo:
                raise ValueError("respuesta vacía")
            tmp = destino + ".tmp"
            if destino.endswith(".gz"):
                with gzip.open(tmp, "wb") as f:
                    f.write(cuerpo)
            else:
                with open(tmp, "wb") as f:
                    f.write(cuerpo)
            os.replace(tmp, destino)
            return "descargado", len(cuerpo)
        except Exception as e:  # noqa: BLE001 - registrar y reintentar
            ultimo_error = e
            time.sleep(pausa * (intento + 1))
    raise RuntimeError(f"fallo tras {reintentos} intentos: {url}: {ultimo_error}")


def leer_manifiesto():
    if not os.path.exists(MANIFIESTO):
        return {}
    with open(MANIFIESTO, newline="", encoding="utf-8") as f:
        return {fila["fichero"]: fila for fila in csv.DictReader(f)}


def escribir_manifiesto(filas):
    """filas: dict fichero -> dict con COLUMNAS. Escribe ordenado por fichero."""
    os.makedirs(FAMILIA_DIR, exist_ok=True)
    tmp = MANIFIESTO + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS, extrasaction="ignore")
        w.writeheader()
        for k in sorted(filas):
            w.writerow(filas[k])
    os.replace(tmp, MANIFIESTO)


def upsert(filas_nuevas):
    """Actualiza el manifiesto con filas nuevas (clave = fichero)."""
    actual = leer_manifiesto()
    for fila in filas_nuevas:
        actual[fila["fichero"]] = fila
    escribir_manifiesto(actual)
