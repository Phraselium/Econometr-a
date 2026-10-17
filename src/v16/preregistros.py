"""V16 · Registro de los pre-registros internos (docs/preregistros.md y docs/preregistros_ficheros.csv).

Todo sale de git, no de documentos anteriores:
- fecha del commit en UTC: `git show -s --format=%cd` con TZ=UTC;
- sha256 de cada fichero del pre-registro tal como está en ese commit: `git show <commit>:<ruta>`;
- si el fichero de hoy sigue igual y, si no, qué commits lo cambiaron después.
La fecha de publicación de cada etiqueta en el remoto se toma de docs/v16/etiquetas_prereg.csv (`fecha_publicacion_utc`, la del
etiquetador de la etiqueta anotada publicada desde el ordenador del autor), porque un clon no tiene por qué traer los objetos
de las etiquetas.
`check()` (lo usa check_v16) recalcula los hashes desde git y exige que coincidan con el CSV, y que los ficheros de los
pre-registros vigentes (V15 y V16) sigan iguales que en su commit.
Uso: python3 src/v16/preregistros.py [--escribir]
"""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ETIQUETAS = RAIZ / "docs" / "v16" / "etiquetas_prereg.csv"
MD = RAIZ / "docs" / "preregistros.md"
CSV = RAIZ / "docs" / "preregistros_ficheros.csv"
VIGENTES = {"prereg-v15", "prereg-v16"}
FICHEROS = {
    "prereg-v2": ["docs/v2/hipotesis.md", "data/processed/v2/train/_sellado.json"],
    "prereg-v3": ["docs/v3/hipotesis.md"],
    "prereg-v5": ["docs/v5/prereg_B3.md"],
    "prereg-v6": ["docs/v6/hipotesis.md", "output/v6/M0/sellado_info.json"],
    "prereg-v7": ["docs/v7/hipotesis.md"],
    "prereg-v8": ["docs/v8/hipotesis.md"],
    "prereg-v9": ["docs/v9/hipotesis.md"],
    "prereg-v9-a1": ["docs/v9/hipotesis_addendum_a1.md"],
    "prereg-v9-a1b": ["docs/v9/hipotesis_addendum_a1.md"],
    "prereg-v15": ["docs/v15/preregistro_v15.md", "docs/v15/preregistro_v15_adenda.md", "docs/v15/sellado_v15.json"],
    "prereg-v16": ["docs/v16/preregistro_v16.md", "docs/v16/preregistro_v16_adenda.md", "docs/v16/sellado_v16.json"],
}
COLS = ["etiqueta", "commit", "fichero", "sha256_en_commit", "igual_hoy", "commits_posteriores"]


def _git(*a: str, binario: bool = False):
    r = subprocess.run(["git", *a], cwd=RAIZ, capture_output=True, text=not binario, env={**os.environ, "TZ": "UTC"})
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr if not binario else r.stderr.decode()}")
    return r.stdout


def etiquetas() -> list[dict]:
    with ETIQUETAS.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fecha_commit_utc(commit: str) -> str:
    return _git("show", "-s", "--date=format-local:%Y-%m-%dT%H:%M:%SZ", "--format=%cd", commit).strip()


def filas() -> list[dict]:
    out = []
    for e in etiquetas():
        c = e["commit"]
        for f in FICHEROS[e["etiqueta"]]:
            h = hashlib.sha256(_git("show", f"{c}:{f}", binario=True)).hexdigest()
            p = RAIZ / f
            hoy = p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == h
            post = "" if hoy else "; ".join(_git("log", "--format=%h %cs %s", f"{c}..HEAD", "--", f).strip().splitlines())
            out.append({"etiqueta": e["etiqueta"], "commit": c, "fichero": f, "sha256_en_commit": h, "igual_hoy": "sí" if hoy else "no",
                        "commits_posteriores": post[:300]})
    return out


def check() -> list[str]:
    """Errores: hash del CSV distinto del recalculado desde git; fichero de un pre-registro vigente cambiado; fecha distinta de git."""
    err = []
    if not CSV.exists():
        return ["falta docs/preregistros_ficheros.csv (python3 src/v16/preregistros.py --escribir)"]
    with CSV.open(encoding="utf-8", newline="") as fh:
        guardado = {(r["etiqueta"], r["fichero"]): r for r in csv.DictReader(fh)}
    for r in filas():
        g = guardado.get((r["etiqueta"], r["fichero"]))
        if g is None:
            err.append(f"{r['etiqueta']} {r['fichero']}: falta en el registro")
        elif g["sha256_en_commit"] != r["sha256_en_commit"]:
            err.append(f"{r['etiqueta']} {r['fichero']}: sha256 registrado distinto del de git en {r['commit'][:7]}")
        if r["etiqueta"] in VIGENTES and r["igual_hoy"] != "sí":
            err.append(f"{r['etiqueta']} {r['fichero']}: el pre-registro vigente ha cambiado desde {r['commit'][:7]}")
    for e in etiquetas():
        if e.get("fecha_commit_utc") != fecha_commit_utc(e["commit"]):
            err.append(f"{e['etiqueta']}: fecha_commit_utc {e.get('fecha_commit_utc')} distinta de git")
    return err


def escribir() -> None:
    fs = filas()
    with CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(fs)
    L = ["# Pre-registros internos (etiquetas git)", "",
         "Generado por `python3 src/v16/preregistros.py --escribir` a partir de git. Cada pre-registro es **interno**: lo fija un commit "
         "de la rama de desarrollo y una etiqueta anotada publicada en el remoto, **sin sello de tiempo externo** (no es un pre-registro "
         "depositado). La fecha del commit y los sha256 salen de git; la de publicación, de la etiqueta anotada (docs/v16/etiquetas_prereg.csv). "
         "`make check` (check_v16) comprueba que los hashes coinciden con git y que los pre-registros vigentes (V15 y V16) no han cambiado.", "",
         "Forma de citarlo en los textos: «pre-registro interno, fijado en el commit X y publicado como etiqueta el <fecha>, sin sello de "
         "tiempo externo».", "",
         "| Etiqueta | Commit | Fecha del commit (UTC) | Publicada como etiqueta (UTC) | Ficheros (sha256 en el commit) | ¿Igual hoy? |",
         "|---|---|---|---|---|---|"]
    for e in etiquetas():
        mine = [f for f in fs if f["etiqueta"] == e["etiqueta"]]
        fich = "<br>".join(f"`{f['fichero']}` `{f['sha256_en_commit'][:16]}…`" for f in mine)
        igual = "<br>".join(f["igual_hoy"] for f in mine)
        L.append(f"| {e['etiqueta']} | {e['commit'][:7]} | {e['fecha_commit_utc']} | {e['fecha_publicacion_utc']} | {fich} | {igual} |")
    cambios = [f for f in fs if f["igual_hoy"] == "no"]
    L += ["", "## Ficheros cambiados después de su commit de pre-registro", "",
          "Ninguno pertenece a un pre-registro vigente. Los sha256 completos y los commits posteriores están en "
          "[preregistros_ficheros.csv](preregistros_ficheros.csv).", ""]
    for f in cambios:
        L.append(f"- **{f['etiqueta']}** · `{f['fichero']}`: {f['commits_posteriores'] or 'sin commits posteriores en esta rama'}")
    L += ["", "**Sin efecto en resultados publicados** (detalle por versión en docs/preregistros_desviaciones.md, publicado en "
          "metodologia/desviaciones_preregistros.md):", "",
          "- **v2.** El cambio (fd2559a) es anterior a todas las evaluaciones selladas de v2. Lleva el sellado a lo que ya decía el "
          "pre-registro (entrenamiento hasta 2024Q2): una fila 2026Q3 sin variables de resultado sale del entrenamiento. Queda fuera de la "
          "ventana evaluada, 2024Q3-2026Q2, y no entra en ninguna métrica. H6 (R1B-S-BP-H6-RV) usa un panel que no cambió.",
          "- **v6.** El cambio (42cf68b) es posterior a todas las evaluaciones selladas de v6. Solo rehace las huellas de dos paneles de "
          "contratos nuevos tras la corrección K4a-02 (ERRATA). Ninguna evaluación abrió esos paneles.",
          "- **v9.** Solo añade el hash del commit pre-registrado.",
          "- **v9-a1.** Lo sustituye prereg-v9-a1b.", "",
          "Ninguno cambia una hipótesis ni una cifra de la versión 1.0, así que no procede entrada en ERRATA.", ""]
    MD.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    if "--escribir" in sys.argv:
        escribir()
    errores = check()
    for x in errores:
        print("ERROR", x)
    print(f"preregistros: {len(etiquetas())} etiquetas, {len(errores)} errores")
    sys.exit(1 if errores else 0)
