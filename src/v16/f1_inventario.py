"""V16-F1 · Inventario y control del registro de licencias de las fuentes nuevas (docs/v16/decisiones.md K5).

Lee los manifiestos data/raw/v16/<familia>/_manifest.csv (esquema de data/raw/v11/_manifest.csv) y comprueba:
- columnas exactas y licencia no vacía;
- redistribuible ∈ {sí, no, dudoso};
- que los ficheros de terceros (redistribuible no o dudoso) estén en _terceros/ y no versionados;
- que los ficheros versionados existan y su sha256 coincida.
Los originales de _grandes/ y _terceros/ pueden faltar en otro clon: se anotan como «solo en disco».
Escribe docs/v16/inventario_fuentes.csv (`--escribir`); sin argumentos solo valida (lo usa check_v16). Sin red; determinista.
"""
from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
V16 = RAIZ / "data" / "raw" / "v16"
SAL = RAIZ / "docs" / "v16" / "inventario_fuentes.csv"
COLUMNAS = ["fuente", "fichero", "url", "fecha_descarga", "edicion", "periodo", "nivel_territorial", "n_filas", "sha256",
            "licencia", "redistribuible", "notas"]
REDIS = {"sí", "no", "dudoso"}


def _sha(f: Path) -> str:
    h = hashlib.sha256()
    with f.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _versionados() -> set[str]:
    r = subprocess.run(["git", "ls-files", "-z", "--", "data/raw/v16"], cwd=RAIZ, capture_output=True, text=True, check=True)
    return {f for f in r.stdout.split("\0") if f}


def revisar(comprobar_sha: bool = True) -> tuple[list[dict], list[str]]:
    filas, errores = [], []
    vers = _versionados()
    for m in sorted(V16.glob("*/_manifest.csv")):
        familia = m.parent.name
        with m.open(encoding="utf-8", newline="") as fh:
            rd = csv.DictReader(fh)
            if rd.fieldnames != COLUMNAS:
                errores.append(f"{m.relative_to(RAIZ)}: columnas {rd.fieldnames} != {COLUMNAS}")
                continue
            for r in rd:
                rel = r["fichero"].strip()
                donde = f"{m.relative_to(RAIZ)}: {rel}"
                red = r["redistribuible"].strip().lower()
                if not r["licencia"].strip():
                    errores.append(f"{donde}: licencia vacía")
                if red not in REDIS:
                    errores.append(f"{donde}: redistribuible «{r['redistribuible']}» no es sí/no/dudoso")
                if not rel:
                    estado = "sin fichero (fuente anotada)"
                else:
                    f = RAIZ / rel
                    tercero = "/_terceros/" in rel
                    grande = "/_grandes/" in rel
                    if red in ("no", "dudoso") and not tercero:
                        errores.append(f"{donde}: fuente {red} fuera de _terceros/")
                    if rel in vers and (tercero or grande):
                        errores.append(f"{donde}: fichero de _terceros/ o _grandes/ versionado")
                    if rel in vers:
                        estado = "versionado"
                        if comprobar_sha and r["sha256"].strip():
                            if not f.exists():
                                errores.append(f"{donde}: versionado pero no existe")
                            elif _sha(f) != r["sha256"].strip():
                                errores.append(f"{donde}: sha256 no coincide")
                    elif f.exists():
                        estado = "solo en disco"
                    else:
                        estado = "ausente en este clon"
                filas.append({"familia": familia, **{k: r[k] for k in ("fuente", "fichero", "edicion", "periodo", "nivel_territorial",
                                                                         "licencia", "redistribuible", "sha256")},
                              "estado": estado})
    return filas, errores


def main() -> int:
    escribir = "--escribir" in sys.argv
    filas, errores = revisar()
    for e in errores:
        print("ERROR", e)
    if escribir:
        SAL.parent.mkdir(parents=True, exist_ok=True)
        with SAL.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["familia", "fuente", "fichero", "edicion", "periodo", "nivel_territorial", "licencia",
                                                "redistribuible", "sha256", "estado"], lineterminator="\n")
            w.writeheader()
            for f in sorted(filas, key=lambda x: (x["familia"], x["fuente"], x["fichero"])):
                # determinista: el estado sale de la ruta, no del clon ni del índice de git
                rel = f["fichero"]
                f = dict(f, estado="sin fichero" if not rel else
                         "no versionado" if ("/_terceros/" in rel or "/_grandes/" in rel) else "versionado")
                w.writerow(f)
    print(f"f1_inventario: {len(filas)} filas, {len(errores)} errores")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
