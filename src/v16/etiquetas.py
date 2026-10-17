"""V16 · Etiquetas de pre-registro en el remoto (pre-registro interno, sin sello de tiempo externo).

`remota(nombre)` devuelve el commit al que apunta la etiqueta en el remoto `origin` (resuelve las etiquetas anotadas con
`^{}`), o None si no existe o no se puede consultar. Para tests y para trabajar sin red, la variable de entorno
ECONOMETRA_ETIQUETAS_REMOTAS puede apuntar a un JSON {etiqueta: commit} que sustituye a la consulta.

La puerta de cada pre-registro exige DOS cosas (decisiones K10):
1. la etiqueta publicada en el remoto y apuntando a su commit;
2. el criterio provisional que ya regía antes de publicarla: el commit está en la rama remota de desarrollo y los ficheros del
   pre-registro no han cambiado desde ese commit (`criterio_provisional`). Para tests, ECONOMETRA_CRITERIO_PROVISIONAL puede
   apuntar a un JSON {versión: motivo} que fuerza el fallo de esa versión.

Etiquetas que fijan los pre-registros (docs/preregistros.md):
- prereg-v15 → 542b4fd (docs/v15/preregistro_v15.md, su adenda y sellado_v15.json);
- prereg-v16 → a8304ec (docs/v16/preregistro_v16.md, su adenda y sellado_v16.json).
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RAMA_REMOTA = "origin/claude/housing-price-spain-econometric-95dhj3"
PREREG = {
    "v15": ("prereg-v15", "542b4fd", ["docs/v15/preregistro_v15.md", "docs/v15/preregistro_v15_adenda.md", "docs/v15/sellado_v15.json"]),
    "v16": ("prereg-v16", "a8304ec", ["docs/v16/preregistro_v16.md", "docs/v16/preregistro_v16_adenda.md", "docs/v16/sellado_v16.json"]),
}
PREREG_V15 = PREREG["v15"][:2]
PREREG_V16 = PREREG["v16"][0]


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


def criterio_provisional(version: str, raiz: Path = RAIZ) -> tuple[bool, str]:
    """El commit del pre-registro está en la rama remota (referencia local de seguimiento) y sus ficheros no han cambiado."""
    f = os.environ.get("ECONOMETRA_CRITERIO_PROVISIONAL")
    if f:
        try:
            forzado = json.loads(Path(f).read_text(encoding="utf-8")).get(version)
        except (OSError, ValueError):
            forzado = "configuración de prueba ilegible"
        return (False, forzado) if forzado else (True, "criterio provisional (simulado) cumplido")
    _, commit, ficheros = PREREG[version]
    try:
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", commit, RAMA_REMOTA], cwd=raiz, capture_output=True, timeout=25)
        if anc.returncode != 0:
            return False, f"el commit {commit} no está en {RAMA_REMOTA}"
        dif = subprocess.run(["git", "diff", "--quiet", commit, "HEAD", "--", *ficheros], cwd=raiz, capture_output=True, timeout=25)
        if dif.returncode != 0:
            return False, f"los ficheros del pre-registro {version} han cambiado desde {commit}"
    except (OSError, subprocess.TimeoutExpired):
        return False, "no se pudo comprobar el criterio provisional"
    return True, f"{commit} en la rama remota y pre-registro {version} sin cambios"


def _publicada(version: str, raiz: Path) -> tuple[bool, str]:
    nombre, commit, _ = PREREG[version]
    sha = remota(nombre, raiz)
    if not sha:
        return False, f"la etiqueta {nombre} no existe en el remoto (pre-registro interno sin publicar)"
    if not sha.startswith(commit):
        return False, f"la etiqueta {nombre} del remoto apunta a {sha[:7]}, no a {commit}"
    ok, motivo = criterio_provisional(version, raiz)
    if not ok:
        return False, f"{nombre} publicada, pero falla el criterio provisional: {motivo}"
    return True, f"{nombre} publicada en el remoto ({commit}) y {motivo}; pre-registro interno sin sello de tiempo externo"


def prereg_v15_publicada(raiz: Path = RAIZ) -> tuple[bool, str]:
    return _publicada("v15", raiz)


def prereg_v16_publicada(raiz: Path = RAIZ) -> tuple[bool, str]:
    ok, motivo = _publicada("v16", raiz)
    return ok, motivo if ok else f"{motivo}: las fases 5-7 de V16 esperan"
