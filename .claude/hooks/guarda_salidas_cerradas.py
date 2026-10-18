#!/usr/bin/env python3
"""V16 · Guarda PreToolUse: los SUBAGENTES no escriben en las salidas de versiones cerradas (incidente de B-3: un agente de auditoría
vació output/v9/d4/registry.csv al ejecutar un script de V9).

Cerrado = output/<versión> salvo las versiones en curso (ABIERTAS), los ficheros sueltos de output/, data/base, publicacion/ y metodologia/.
Solo se aplica cuando la llamada viene de un subagente (el JSON del hook trae agent_id o agent_type); el orquestador escribe ahí solo con
orden expresa del autor, y check_v16 («salidas cerradas») comprueba antes de cada commit que toda modificación sin commit en esas rutas esté
autorizada en docs/v16/escrituras_autorizadas.csv.
Bloquea (código 2, motivo en stderr):
  - Write/Edit/NotebookEdit con file_path en una ruta cerrada;
  - Bash que ejecuta un script de una versión cerrada (python src/vN/... o src/*.py raíz, que escriben en sus salidas), o que redirige
    (>, >>, tee) a una ruta cerrada. Para auditar, se copia el script a /tmp y se ejecuta allí con salidas en /tmp.
Uso como función: `evaluar(datos_hook) -> motivo | None` (tests/v16/test_guarda_salidas.py).
"""
from __future__ import annotations

import json
import re
import sys

ABIERTAS = {"v15", "v16"}
_VERS = r"v\d+(?:_\d+)?"
RAICES_CERRADAS = ("data/base/", "publicacion/", "metodologia/")


RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[2])


def ruta_cerrada(ruta: str) -> bool:
    r = ruta.strip().strip("'\"")
    r = r[len(RAIZ) + 1:] if r.startswith(RAIZ + "/") else re.sub(r"^\./", "", r)
    if r.startswith(RAICES_CERRADAS):
        return True
    m = re.match(rf"output/({_VERS})(/|$)", r)
    if m:
        return m.group(1) not in ABIERTAS
    return r.startswith("output/") and "/" not in r[len("output/"):]   # ficheros sueltos de output/ (v1)


def _script_cerrado(cmd: str) -> str | None:
    for m in re.finditer(r"\bpython3?\s+(?:-\S+\s+)*([\w./-]+\.py)", cmd):
        s = re.sub(r"^\./", "", m.group(1))
        mv = re.match(rf"src/({_VERS})/", s)
        if mv and mv.group(1) not in ABIERTAS:
            return s
        if re.match(r"src/[^/]+\.py$", s):
            return s
    return None


def evaluar(d: dict) -> str | None:
    if not (d.get("agent_id") or d.get("agent_type")):
        return None   # orquestador: lo controla check_v16 («salidas cerradas»)
    herr, ti = d.get("tool_name", ""), d.get("tool_input") or {}
    if herr in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
        ruta = ti.get("file_path") or ti.get("notebook_path") or ""
        if ruta_cerrada(ruta):
            return f"subagente: escritura en una ruta cerrada ({ruta}); copia a /tmp y trabaja allí"
        return None
    if herr == "Bash":
        cmd = ti.get("command", "")
        s = _script_cerrado(cmd)
        if s:
            return f"subagente: ejecutar {s} escribe en salidas de una versión cerrada; cópialo a /tmp y ejecútalo allí con salidas en /tmp"
        for m in re.finditer(r"(?:>>?|\btee\s+(?:-a\s+)?)\s*([\w./-]+)", cmd):
            if ruta_cerrada(m.group(1)):
                return f"subagente: redirección a una ruta cerrada ({m.group(1)})"
    return None


def main() -> int:
    try:
        d = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    motivo = evaluar(d)
    if motivo:
        print(f"Guarda de salidas cerradas: {motivo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
