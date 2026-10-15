"""V12-F0: `make check` no debe dejar cambios en ficheros versionados. Uso:
  python3 src/v12/git_limpio.py guardar <fichero>   (antes de las comprobaciones)
  python3 src/v12/git_limpio.py comparar <fichero>  (después; código 1 si `git status --porcelain` cambió)
La instantánea se guarda fuera del repositorio (directorio temporal del sistema).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def estado() -> str:
    return subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def main(accion: str, fichero: str) -> int:
    f = Path(fichero)
    if accion == "guardar":
        f.write_text(estado(), encoding="utf-8")
        return 0
    antes, despues = f.read_text(encoding="utf-8"), estado()
    if antes != despues:
        nuevas = sorted(set(despues.splitlines()) - set(antes.splitlines()))
        print("make check ha modificado ficheros del repositorio:\n  " + "\n  ".join(nuevas))
        return 1
    print("make check: sin cambios en git")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
