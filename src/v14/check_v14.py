"""Comprobaciones de puerta V14 (entran en `make check`). Sin red; no escribe nada.

1. Heredocs entrecomillados: ningún heredoc de shell con el delimitador sin comillas (p. ej. EOF a pelo) en src/, el Makefile ni los guiones .sh
   versionados. Con comillas (`<<'EOF'`) el shell no expande `$(...)` ni comillas invertidas del texto; sin ellas, una orden
   escrita entre comillas invertidas en un texto se ejecuta (incidencia D3 de V13: `make clean` y `make all`).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
# `<<` o `<<-` seguido de un delimitador SIN comillas (mayúsculas, como EOF o PY). `x << 2` (desplazamiento) no coincide.
HEREDOC = re.compile(r"<<-?[ \t]*(?P<d>[A-Z][A-Z0-9_]*)\b")
RUTAS = ("src", "Makefile", "*.sh", "docs/*.sh", ".github")


def _versionados() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z", "--", *RUTAS], cwd=RAIZ, capture_output=True, text=True, check=True)
    return [f for f in r.stdout.split("\0") if f and (RAIZ / f).is_file()]


def heredocs_sin_comillas(ficheros: list[str] | None = None) -> list[str]:
    err = []
    for f in ficheros if ficheros is not None else _versionados():
        if not f.endswith((".py", ".sh", ".yml", ".yaml", "Makefile", ".mk")):
            continue
        for n, ln in enumerate((RAIZ / f).read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if "check_v14: permitido" in ln:
                continue
            for m in HEREDOC.finditer(ln):
                err.append(f"{f}:{n}: heredoc sin comillas «{m.group(0)}» (usar <<'{m.group('d')}')")
    return err


def main() -> int:
    e = heredocs_sin_comillas()
    print(f"check_v14 · heredocs sin comillas: {len(e)} errores")
    for x in e[:20]:
        print("  -", x)
    print(f"check_v14: {len(e)} errores")
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main())
