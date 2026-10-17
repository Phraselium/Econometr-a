"""Utilidades de registro para la familia demanda_internacional (V16, fase 1).

Escribe/actualiza data/raw/v16/demanda_internacional/_manifest.csv con las columnas
EXACTAS del protocolo de adquisición. Las filas se identifican por la columna
«fichero» (ruta relativa al repositorio); una nueva descarga sustituye la fila previa.
"""
import csv
import hashlib
import os
import urllib.request
from datetime import datetime, timezone

RAIZ = "/home/user/Econometr-a"
FAMILIA_DIR = os.path.join(RAIZ, "data/raw/v16/demanda_internacional")
MANIFEST = os.path.join(FAMILIA_DIR, "_manifest.csv")
COLUMNAS = ["fuente", "fichero", "url", "fecha_descarga", "edicion", "periodo",
            "nivel_territorial", "n_filas", "sha256", "licencia", "redistribuible", "notas"]
AGENTE = "adquisidor-datos-v16 (investigacion academica; contacto: romerolopezborja@gmail.com)"


def ahora_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_fichero(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def descargar(url, destino, timeout=120):
    """Descarga un fichero con cabecera de agente identificable. No reintenta en bucle."""
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(peticion, timeout=timeout) as r, open(destino, "wb") as f:
        f.write(r.read())
    return destino


def relativa(ruta):
    return os.path.relpath(ruta, RAIZ)


def registrar(fila):
    """Inserta o sustituye la fila (clave: fichero) en el manifiesto."""
    filas = []
    if os.path.exists(MANIFEST):
        with open(MANIFEST, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    filas = [x for x in filas if x["fichero"] != fila["fichero"]]
    filas.append({c: fila.get(c, "") for c in COLUMNAS})
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)
