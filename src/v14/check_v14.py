"""Comprobaciones de puerta V14 (entran en `make check`). Sin red; no escribe nada.

1. Heredocs entrecomillados: ningún heredoc de shell con el delimitador sin comillas (p. ej. EOF a pelo) en src/, el Makefile ni los guiones .sh
   versionados. Con comillas (`<<'EOF'`) el shell no expande `$(...)` ni comillas invertidas del texto; sin ellas, una orden
   escrita entre comillas invertidas en un texto se ejecuta (incidencia D3 de V13: `make clean` y `make all`).
2. Huella de la muestra sellada (V14.1): proyecto.json `hash_sellado.valor` debe ser un sha256 (64 caracteres hexadecimales).
   Mientras sea «PENDIENTE» es un AVISO en el repositorio de desarrollo y un ERROR en el árbol público
   (proyecto.json con `arbol_publico: true`, que escribe `make arbol_publico`).
"""
from __future__ import annotations

import json
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


def hash_sellado(proyecto: dict | None = None) -> tuple[list[str], list[str]]:
    """(errores, avisos) sobre proyecto.json hash_sellado."""
    p = proyecto if proyecto is not None else json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
    h = p.get("hash_sellado") or {}
    v = str(h.get("valor", "")).strip()
    if re.fullmatch(r"[0-9a-f]{64}", v):
        return [], []
    msg = (f"proyecto.json hash_sellado = «{v or 'falta'}»: el autor debe calcularlo con "
           f"`{h.get('comando', 'find data/sealed -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum')}`")
    if v and v.upper() != "PENDIENTE":
        return [f"{msg} (no es un sha256 válido)"], []
    return ([msg], []) if p.get("arbol_publico") else ([], [msg])


def main() -> int:
    e = heredocs_sin_comillas()
    print(f"check_v14 · heredocs sin comillas: {len(e)} errores")
    for x in e[:20]:
        print("  -", x)
    eh, ah = hash_sellado()
    print(f"check_v14 · huella de la muestra sellada: {len(eh)} errores")
    for x in eh:
        print("  -", x)
    for x in ah:
        print("  AVISO:", x)
    e += eh
    print(f"check_v14: {len(e)} errores")
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main())
