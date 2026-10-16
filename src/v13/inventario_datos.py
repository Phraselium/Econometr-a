"""V13-B1 · Inventario de data/ para el depósito: tamaño por carpeta y clase de cada fichero, con licencia y fuente.

Clases:
- (a) redistribuible por licencia y versionado: entra en el paquete de Zenodo (`make paquete_zenodo`);
- (b) no redistribuible (licencia no verificada o no abierta, microdatos con celdas pequeñas, derivados que contienen series de
  Notariado o Registradores): no entra en el paquete; se obtiene con `make datos_terceros` o por descarga manual;
- (c) redistribuible pero no versionado (originales y microdatos grandes): no entra; se regenera con su descarga.
data/sealed no se recorre (solo vía src/holdout.py): se anota su existencia, sin leer ni medir su contenido.

Fuentes de la licencia, por orden: docs/v8_1/inventario_licencias.csv (ficheros de v1-v8), manifiestos de data/raw/v9, v10 y
v11 (columnas licencia y redistribuible) y, si no hay, la tabla por organismo de docs/v5/licencias_datos.md (por prefijo).
Escribe docs/v13/datos_inventario.csv solo con los ficheros versionados (determinista: igual en cualquier clon) y, con
`--todo RUTA`, la lista completa de lo que hay en disco (para el resumen de docs/v13/datos_deposito.md). Sin red.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
SALIDA = RAIZ / "docs" / "v13" / "datos_inventario.csv"

# derivados versionados que contienen series de fuentes no redistribuibles (cabeceras con notariado/registradores/AEAT/CGPJ)
NO_REDIS_COL = re.compile(r"notar|registrad|cgn_|cgpj|aeat", re.I)
# licencia por prefijo del fichero (docs/v5/licencias_datos.md), para los ficheros sin inventario ni manifiesto
PREFIJOS = [
    (r"^(ine|_manifest_series_ine)", "INE", "INE: reutilización con cita (Ley 37/2007)", True),
    (r"^(mivau|serpavi|suelo)", "MIVAU", "MIVAU: reutilización con cita (Ley 37/2007)", True),
    (r"^catastro", "Dirección General del Catastro", "Catastro: reutilización con reconocimiento", True),
    (r"^bde", "Banco de España", "BdE: reproducción con cita", True),
    (r"^(eu_|eurostat)", "Eurostat", "CC BY 4.0 (Decisión 2011/833/UE)", True),
    (r"^(ecb|bce)", "BCE", "BCE: reutilización con cita", True),
    (r"^bis", "BIS", "BIS: reutilización con cita", True),
    (r"^(oecd|ocde)", "OCDE", "CC BY 4.0", True),
    (r"^gva", "Generalitat Valenciana", "CC BY 4.0", True),
    (r"^(vlc|valencia)", "Ajuntament de València", "CC BY 4.0", True),
    (r"^(notari)", "Consejo General del Notariado", "no verificada", False),
    (r"^(registr)", "Colegio de Registradores", "no verificada", False),
]


def _git_ls(ruta: str) -> set[str]:
    r = subprocess.run(["git", "ls-files", "-z", "--", ruta], cwd=RAIZ, capture_output=True, text=True, check=True)
    return {f for f in r.stdout.split("\0") if f}


def _licencias() -> tuple[dict[str, tuple[str, str, bool]], dict[str, tuple[str, str, bool]]]:
    """{fichero: (fuente, licencia, redistribuible)} de los inventarios y manifiestos versionados."""
    out: dict[str, tuple[str, str, bool]] = {}
    carpetas: dict[str, tuple[str, str, bool]] = {}   # carpeta de la fuente -> licencia (para los ficheros sin fila propia)
    with (RAIZ / "docs/v8_1/inventario_licencias.csv").open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[r["fichero"]] = (r["organismo"], r["motivo"] if r["estado"] != "permitida" else "permitida (docs/v5/licencias_datos.md)",
                                 r["estado"] == "permitida")
    for m in sorted((DATA / "raw").glob("v*/_manifest.csv")) + sorted((DATA / "raw").glob("v*/*/_manifest.csv")):
        with m.open(encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                f = r.get("fichero") or ""
                if f and "licencia" in r:
                    red = str(r.get("redistribuible", "")).strip().lower() in ("sí", "si", "true", "1", "yes")
                    out.setdefault(f, (r.get("fuente", ""), r.get("licencia", ""), red))
                    carpetas.setdefault(m.parent.relative_to(RAIZ).as_posix(), (r.get("fuente", ""), r.get("licencia", ""), red))
    return out, carpetas


CARPETAS_SIN_MANIFIESTO = [   # originales no versionados de v2-v10 sin manifiesto propio (ver el script que los descarga)
    ("data/raw/v3_orig/", "INE (ADRH, censo anual, VUT por sección)", "INE: reutilización con cita (Ley 37/2007)", True),
    ("data/raw/v3/cartografia/", "INE (seccionado censal)", "INE: reutilización con cita (Ley 37/2007)", True),
    ("data/raw/v10/geo/", "INE (seccionado 2025) y Ajuntament de València (geoportal)", "INE (Ley 37/2007) y CC BY 4.0", True),
    ("data/raw/v2_orig/catastro/", "Dirección General del Catastro (URBANA)", "Catastro: reutilización con reconocimiento", True),
    ("data/raw/gva_orig/", "Generalitat Valenciana (registro VUT)", "CC BY 4.0", True),
    ("data/raw/v10/monitor/", "INE, MIVAU, Eurostat, BdE y GVA (series del monitor, src/v10/monitor.py)", "la de cada organismo (todas con reutilización con cita)", True),
]


def _por_prefijo(nombre: str) -> tuple[str, str, bool] | None:
    for pat, org, lic, red in PREFIJOS:
        if re.search(pat, nombre, re.I):
            return org, lic, red
    return None


def _cabecera_no_redis(p: Path) -> bool:
    if p.suffix != ".csv":
        return False
    try:
        with p.open(encoding="utf-8", errors="ignore") as fh:
            return bool(NO_REDIS_COL.search(fh.readline()))
    except OSError:
        return False


def clasificar() -> list[dict]:
    versionados = _git_ls("data")
    lic, lic_carpeta = _licencias()
    filas = []
    for p in sorted(DATA.rglob("*")):
        rel = p.relative_to(RAIZ).as_posix()
        if rel.startswith("data/sealed") or not p.is_file():
            continue
        v = rel in versionados
        partes = rel.split("/")
        carpeta = "/".join(partes[:3]) if len(partes) > 3 else "/".join(partes[:2])
        dueno = next((c for c in sorted(lic_carpeta, key=len, reverse=True) if rel.startswith(c + "/")), None)
        fuente, licencia, red = lic.get(rel) or (lic_carpeta[dueno] if dueno else None) or next(((f, li, rd) for c, f, li, rd in CARPETAS_SIN_MANIFIESTO if rel.startswith(c)), None) \
            or _por_prefijo(p.name) or ("", "", None)
        motivo = ""
        if p.name in ("_manifest.csv", "CHECKSUMS.sha256", "validacion.csv", "_manifest_series_ine_v2.csv") or p.name.endswith(".lock"):
            fuente, licencia, red = "elaboración propia (metadatos)", "CC BY 4.0", True
            clase = "a" if v else "c"
        elif re.search(r"aeat|agencia tributaria", f"{rel} {fuente} {licencia}", re.I):
            clase = "b"
            motivo = ("discrepancia de licencia: el manifiesto V11 dice «redistribuible: sí» (Ley 37/2007) y docs/v5/licencias_datos.md "
                      "y V8.1 dicen «no verificada en detalle»; se excluye hasta que el autor la confirme")
        elif rel.startswith("data/manual/"):
            fuente, licencia = fuente or "descarga manual del autor", licencia or "según la fuente (docs/v11/descargas_manuales.md)"
            clase, motivo = "b", "original de una descarga manual; su versión normalizada está en data/raw/v11/manual"
        elif rel.startswith("data/cache/"):
            clase, motivo, fuente, licencia = "b", "caché interna con celdas pequeñas (data/cache/v12/LEEME.md)", "INE (microdatos EVR/EMCR)", "INE; no difundible por secreto estadístico"
        elif rel.startswith("data/processed/") and v and _cabecera_no_redis(p):
            clase, motivo = "b", "derivado que contiene series de Notariado, Registradores, AEAT o CGPJ"
            fuente, licencia = "elaboración propia (incluye series de terceros)", "mixta: la de su fuente más restrictiva"
        elif rel.startswith(("data/processed/", "data/base/")):
            fuente = fuente or "elaboración propia (derivado de data/raw)"
            licencia = licencia or "CC BY 4.0 (elaboración propia) + licencia de sus fuentes"
            red = True if red is None else red
            if rel.startswith("data/base/") and not rel.startswith(("data/base/publica/", "data/base/geo/")):
                clase, motivo = ("b", "base completa (incluye variables no redistribuibles); su versión difundible es data/base/publica")
            else:
                clase = "a" if v else "c"
        elif red is False:
            clase, motivo = "b", "licencia no verificada o no abierta"
        elif red is None:
            clase, motivo = ("a" if v else "c"), "licencia no inventariada: se asume la del organismo (revisar)"
            fuente, licencia = fuente or "sin inventario", licencia or "no inventariada"
        else:
            clase = "a" if v else "c"
        if clase == "c" and not motivo:
            motivo = "no versionado (tamaño u original): se regenera con su descarga"
        filas.append({"fichero": rel, "carpeta": carpeta, "bytes": p.stat().st_size, "versionado": v, "clase": clase,
                      "fuente": fuente, "licencia": licencia, "motivo": motivo})
    return filas


def _escribir(ruta: Path, filas: list[dict]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--todo", help="escribe aquí también la lista completa de ficheros en disco")
    a = ap.parse_args()
    filas = clasificar()
    _escribir(SALIDA, [f for f in filas if f["versionado"]])
    if a.todo:
        _escribir(Path(a.todo), filas)
    n = {c: sum(f["clase"] == c for f in filas) for c in "abc"}
    print(f"inventario_datos: {len(filas)} ficheros; a={n['a']} b={n['b']} c={n['c']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
