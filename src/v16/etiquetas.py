"""V16 · Etiquetas de pre-registro en el remoto (pre-registro interno, sin sello de tiempo externo).

`remota(nombre)` devuelve el commit al que apunta la etiqueta en el remoto `origin` (resuelve las etiquetas anotadas con
`^{}`), o None si no existe o no se puede consultar. Para tests y para trabajar sin red, la variable de entorno
ECONOMETRA_ETIQUETAS_REMOTAS puede apuntar a un JSON {etiqueta: commit} que sustituye a la consulta.

Etiquetas que fijan los pre-registros:
- prereg-v15 → commit 542b4fd (docs/v15/preregistro_v15.md y sus dos adendas).
- prereg-v16 → se fija al cerrar la fase 4 de V16.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PREREG_V15 = ("prereg-v15", "542b4fd")
PREREG_V16 = "prereg-v16"


def remota(nombre: str, raiz: Path = RAIZ, timeout: int = 25) -> str | None:
    f = os.environ.get("ECONOMETRA_ETIQUETAS_REMOTAS")
    if f:
        try:
            return json.loads(Path(f).read_text(encoding="utf-8")).get(nombre)
        except (OSError, ValueError):
            return None
    try:
        r = subprocess.run(["git", "ls-remote", "--tags", "origin", f"refs/tags/{nombre}", f"refs/tags/{nombre}^{{}}"],
                           cwd=raiz, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    filas = dict(reversed(linea.split("\t")) for linea in r.stdout.strip().splitlines() if "\t" in linea)
    return filas.get(f"refs/tags/{nombre}^{{}}") or filas.get(f"refs/tags/{nombre}")


def prereg_v15_publicada(raiz: Path = RAIZ) -> tuple[bool, str]:
    nombre, commit = PREREG_V15
    sha = remota(nombre, raiz)
    if not sha:
        return False, f"la etiqueta {nombre} no existe en el remoto (pre-registro interno sin publicar)"
    if not sha.startswith(commit):
        return False, f"la etiqueta {nombre} del remoto apunta a {sha[:7]}, no a {commit}"
    return True, f"{nombre} publicada en el remoto ({commit}); pre-registro interno sin sello de tiempo externo"


def prereg_v16_publicada(raiz: Path = RAIZ) -> tuple[bool, str]:
    sha = remota(PREREG_V16, raiz)
    if not sha:
        return False, f"la etiqueta {PREREG_V16} no existe en el remoto: las fases 5-7 de V16 esperan"
    return True, f"{PREREG_V16} publicada en el remoto ({sha[:7]}); pre-registro interno sin sello de tiempo externo"
