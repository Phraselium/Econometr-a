"""V12-F0: la sesión de tests falla si deja cambios en ficheros versionados (git status distinto al empezar y al
terminar). Las salidas de los tests van a directorios temporales."""
from __future__ import annotations

import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _estado() -> str:
    try:
        return subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    except Exception:  # noqa: BLE001  (sin git: no se comprueba)
        return ""


def pytest_sessionstart(session):
    session.config._git_antes = _estado()


def pytest_sessionfinish(session, exitstatus):
    antes = getattr(session.config, "_git_antes", None)
    if antes is None:
        return
    despues = _estado()
    if despues != antes:
        nuevas = sorted(set(despues.splitlines()) - set(antes.splitlines()))
        print("\nLos tests han modificado ficheros del repositorio:\n  " + "\n  ".join(nuevas))
        session.exitstatus = 1
