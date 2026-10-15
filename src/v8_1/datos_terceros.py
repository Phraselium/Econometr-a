"""V8.1 bloque C: datos de terceros retirados del índice de git (`make datos_terceros`).

Los ficheros listados como «no claramente permitida / no consta» en docs/v8_1/inventario_licencias.csv ya no se
versionan (están en .gitignore). Este script:
  1. con red (y sin --solo-verificar): ejecuta los fetch_* existentes que producen los ficheros que faltan o
     difieren, escribiendo en data/raw (nunca sobrescribe lo que ya coincide con el checksum);
  2. con o sin red: verifica el sha256 de cada fichero contra data/CHECKSUMS.sha256.
Sin red solo verifica. Los .gz regenerados llevan otra marca de tiempo en la cabecera: se comparan por contenido
con docs/v8_1/contenido_gz.sha256. Código de salida 0 si todo coincide; 1 si algo falta o difiere (los renders PNG manuales,
sin script de descarga, solo avisan). Uso: python3 src/v8_1/datos_terceros.py [--solo-verificar] [--raiz RUTA]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
JK_CMD = ("import sys; sys.path[:0]=['src','src/v8']; import fetch_v8 as f; "
          "print(f.guardar(f.serie_jk(), 'jk_shocks_ecb_mensual.csv'))")

# Orden: el cruce de registradores con el notariado exige ejecutar antes extract_notariado.
SCRIPTS = [
    ("src/extract_notariado.py", [PY, "src/extract_notariado.py"]),
    ("src/extract_registradores.py", [PY, "src/extract_registradores.py"]),
    ("src/v5/cb_fetch.py", [PY, "src/v5/cb_fetch.py"]),
    ("src/v5/a5_fetch.py", [PY, "src/v5/a5_fetch.py"]),
    ("src/v3/fetch_madrid_alquiler_cp_v3.py", [PY, "src/v3/fetch_madrid_alquiler_cp_v3.py"]),
    ("src/v3/fetch_d3_v3.py", [PY, "src/v3/fetch_d3_v3.py"]),
    ("src/v8/fetch_v8.py", [PY, "-c", JK_CMD]),
    ("src/v9/fetch_incasol.py", [PY, "src/v9/fetch_incasol.py"]),   # V9-DATOS
    ("src/v9/fetch_cat_turisme.py", [PY, "src/v9/fetch_cat_turisme.py"]),   # V9 COMPLETO
]
MANUALES = ("_p1.png", "_zoomA.png", "_zoomB.png",   # renders de validación hechos a mano con pdftoppm sobre el PDF original
            "v4/medidas_programas.csv")   # V8.1: transcripción manual de medidas de programas, aplazada a la fase de propuestas


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def hay_red() -> bool:
    try:
        urllib.request.urlopen("https://servicios.ine.es/", timeout=6)
        return True
    except Exception:  # noqa: BLE001
        return False


def cargar(raiz: Path):
    """Devuelve [(fichero, sha_esperado, script)] de los retirados, con sha de data/CHECKSUMS.sha256."""
    ck = {}
    for ln in (raiz / "data/CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines():
        if "  " in ln:
            h, f = ln.split("  ", 1)
            ck[f.strip()] = h.strip()
    out = []
    with (raiz / "docs/v8_1/inventario_licencias.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["estado"].startswith("no claramente"):
                out.append((r["fichero"], ck.get(r["fichero"], ""), r["script_descarga"].split(";")[0]))
    return out


def cargar_contenido_gz(raiz: Path) -> dict:
    p = raiz / "docs/v8_1/contenido_gz.sha256"
    if not p.exists():
        return {}
    return {l.split("  ", 1)[1].strip(): l.split("  ", 1)[0] for l in p.read_text(encoding="utf-8").splitlines() if "  " in l}


def estado(raiz: Path, fichero: str, esperado: str) -> str:
    p = raiz / fichero
    if not p.exists():
        return "AUSENTE"
    if not esperado:
        return "SIN_CHECKSUM"
    if sha(p) == esperado:
        return "OK"
    if fichero.endswith(".gz") and fichero in cargar_contenido_gz(raiz):
        # la cabecera gzip lleva marca de tiempo: se compara el contenido descomprimido
        if hashlib.sha256(gzip.decompress(p.read_bytes())).hexdigest() == cargar_contenido_gz(raiz)[fichero]:
            return "OK (contenido; cabecera gzip distinta)"
    return "DISTINTO"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-verificar", action="store_true")
    ap.add_argument("--raiz", default=str(ROOT))
    a = ap.parse_args()
    raiz = Path(a.raiz)
    items = cargar(raiz)
    pend = {s for f, h, s in items if estado(raiz, f, h) in ("AUSENTE", "DISTINTO") and s and not f.endswith(MANUALES)}
    if pend and not a.solo_verificar:
        if hay_red():
            for nombre, cmd in SCRIPTS:
                if nombre in pend:
                    print(f"[datos_terceros] descargando con {nombre}")
                    subprocess.run(cmd, cwd=raiz, check=False)
        else:
            print("[datos_terceros] sin red: solo se verifica")
    malos, avisos, n_ok = [], [], 0
    for f, h, s in items:
        e = estado(raiz, f, h)
        if e.startswith("OK"):
            n_ok += 1
        elif f.endswith(MANUALES) and e == "AUSENTE":
            avisos.append((f, "transcripción manual aplazada a la fase de propuestas (copia local del autor)" if f.endswith("medidas_programas.csv") else "render manual (pdftoppm del original)"))
        else:
            malos.append((f, e))
    print(f"[datos_terceros] {n_ok}/{len(items)} ficheros coinciden con data/CHECKSUMS.sha256")
    for f, m in avisos:
        print(f"  AVISO {f}: {m}")
    for f, e in malos:
        print(f"  {e}: {f}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
