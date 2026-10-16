"""V14 · `make datos` (árbol público): trae data/ desde el paquete del depósito de Zenodo y verifica cada sha256.

- El paquete es el que genera `make paquete_zenodo` (src/v13/paquete_zenodo.py): un directorio o un .zip
  `vivienda-espana-evidencia-<versión>` con CHECKSUMS.sha256 en su raíz.
- Origen, por orden:
  1. el paquete ya presente dentro del repositorio, en `_descarga/` (directorio o .zip; ignorado por git);
  2. la URL `zenodo_url_paquete` de proyecto.json, que se descarga a `_descarga/`.
  Mientras el DOI o la URL sean «PENDIENTE» y no haya paquete en `_descarga/`, falla con un mensaje claro.
- Solo se copian los ficheros de data/ del paquete. Cada uno se verifica contra CHECKSUMS.sha256 del paquete.
- Nunca se sobrescribe un fichero versionado: si ya existe y es distinto, falla.
- Nada se lee fuera del repositorio. Los datos no redistribuibles no están en el paquete: `make datos_terceros` y
  docs/v11/descargas_manuales.md.
Uso: python3 src/v14/datos.py [--solo-verificar]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
NOMBRE = f"vivienda-espana-evidencia-{P['version_publica']}"
DESCARGA = RAIZ / "_descarga"


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def localizar() -> Path:
    """Devuelve el directorio del paquete dentro de _descarga/ (descomprimiendo o descargando si hace falta)."""
    d = DESCARGA / NOMBRE
    if (d / "CHECKSUMS.sha256").exists():
        return d
    z = DESCARGA / f"{NOMBRE}.zip"
    if not z.exists():
        url, doi = P.get("zenodo_url_paquete", "PENDIENTE"), P.get("doi", "PENDIENTE")
        if "PENDIENTE" in (str(url).upper(), str(doi).upper()):
            raise SystemExit(
                "make datos: el depósito de Zenodo aún no está publicado (proyecto.json: doi y zenodo_url_paquete = PENDIENTE).\n"
                f"  Mientras tanto, copie el paquete de `make paquete_zenodo` en {DESCARGA.relative_to(RAIZ)}/{NOMBRE}/ "
                f"(o el zip en {DESCARGA.relative_to(RAIZ)}/{NOMBRE}.zip) y repita.")
        DESCARGA.mkdir(exist_ok=True)
        print(f"make datos: descargando {url} (DOI {doi})")
        with urllib.request.urlopen(url, timeout=600) as r, z.open("wb") as fh:   # noqa: S310 (URL de proyecto.json)
            shutil.copyfileobj(r, fh)
    with zipfile.ZipFile(z) as zf:
        for m in zf.infolist():
            destino = (DESCARGA / m.filename).resolve()
            if not str(destino).startswith(str(DESCARGA.resolve())):
                raise SystemExit(f"make datos: ruta fuera de _descarga/ en el zip: {m.filename}")
        zf.extractall(DESCARGA)
    if not (d / "CHECKSUMS.sha256").exists():
        raise SystemExit(f"make datos: el zip no contiene {NOMBRE}/CHECKSUMS.sha256")
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo-verificar", action="store_true", help="solo comprueba los sha256 de data/ en el repositorio")
    a = ap.parse_args()
    paquete = localizar()
    sumas = {}
    for ln in (paquete / "CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines():
        h, f = ln.split("  ", 1)
        if f.startswith("data/"):
            sumas[f] = h
    copiados = iguales = 0
    malos = []
    for f, h in sorted(sumas.items()):
        origen, destino = paquete / f, RAIZ / f
        if _sha(origen) != h:
            malos.append(f"paquete corrupto: {f}")
            continue
        if destino.exists():
            if _sha(destino) == h:
                iguales += 1
            else:
                malos.append(f"distinto del paquete (no se sobrescribe): {f}")
            continue
        if a.solo_verificar:
            malos.append(f"falta: {f}")
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen, destino)
        copiados += 1
    print(f"make datos: {copiados} copiados, {iguales} ya presentes e iguales, {len(malos)} problemas (de {len(sumas)} ficheros de data/)")
    for m in malos[:20]:
        print("  -", m)
    print("Datos no redistribuibles (no están en el paquete): `make datos_terceros` y docs/v11/descargas_manuales.md.")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
