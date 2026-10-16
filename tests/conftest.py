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


def _comprobar_recuento_arbol(session) -> None:
    """V14.1: en el árbol público, una ejecución completa de `pytest tests` debe dar los pasados y omitidos de
    docs/v14/tests_arbol.json (los que publica el README)."""
    import json as _json
    try:
        proyecto = _json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
        esperado = _json.loads((RAIZ / "docs/v14/tests_arbol.json").read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return
    cfg = session.config
    completa = [str(x).rstrip("/") for x in cfg.args] == ["tests"] and not cfg.option.keyword and not cfg.option.markexpr
    if not proyecto.get("arbol_publico") or not completa or session.testsfailed:
        return
    tr = cfg.pluginmanager.get_plugin("terminalreporter")
    real = {"pasados": len(tr.stats.get("passed", [])), "omitidos": len(tr.stats.get("skipped", []))}
    if real != {k: esperado[k] for k in real}:
        print(f"\nRecuento de tests distinto del publicado en el README: ejecución {real}, docs/v14/tests_arbol.json "
              f"{ {k: esperado[k] for k in real} }")
        session.exitstatus = 1


def pytest_sessionfinish(session, exitstatus):
    _comprobar_recuento_arbol(session)
    antes = getattr(session.config, "_git_antes", None)
    if antes is None:
        return
    despues = _estado()
    if despues != antes:
        nuevas = sorted(set(despues.splitlines()) - set(antes.splitlines()))
        print("\nLos tests han modificado ficheros del repositorio:\n  " + "\n  ".join(nuevas))
        session.exitstatus = 1


# V14 (árbol público): sin los datos de terceros (Notariado, Registradores; `make datos_terceros` y la reconstrucción de
# los paneles), los tests que los leen no pueden ejecutarse. Solo se marcan como omitidos los que fallan con
# FileNotFoundError sobre uno de esos ficheros (src/v14/terceros.py, REQUIEREN_TERCEROS); cualquier otro fallo sigue siendo
# un fallo. En el repositorio de desarrollo, con los datos presentes, no se omite nada. Limitación documentada en
# reproducir/instrucciones.md («Árbol público»).
import sys as _sys  # noqa: E402

import pytest  # noqa: E402

_sys.path.insert(0, str(RAIZ))
try:
    from src.v14.terceros import REQUIEREN_TERCEROS as _TERCEROS
except Exception:  # noqa: BLE001
    _TERCEROS = ()


def _falta_terceros(texto: str) -> str | None:
    if "No such file or directory" not in texto:
        return None
    for f in _TERCEROS:
        if f in texto and not (RAIZ / f).exists():
            return f
    return None


def _texto(rep, call=None) -> str:
    partes = [str(getattr(rep, "longreprtext", "") or "")]
    partes += [c for _, c in getattr(rep, "sections", [])]
    exc = getattr(getattr(call, "excinfo", None), "value", None)
    if exc is not None and exc.__class__.__name__ == "CalledProcessError":
        partes += [str(getattr(exc, a) or "") for a in ("stderr", "output")]
        # sin salida capturada: el script lanzado lee por nombre un fichero de terceros que falta
        for arg in (exc.cmd if isinstance(exc.cmd, (list, tuple)) else [exc.cmd]):
            q = Path(str(arg))
            q = q if q.is_absolute() else RAIZ / q
            if q.suffix == ".py" and q.exists():
                fuente = q.read_text(encoding="utf-8", errors="ignore")
                partes += [f"No such file or directory: {f}" for f in _TERCEROS if Path(f).name in fuente and not (RAIZ / f).exists()]
    return "\n".join(partes)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    rep = out.get_result()
    if rep.failed:
        f = _falta_terceros(_texto(rep, call))
        if f:
            rep.outcome = "skipped"
            rep.longrepr = (str(item.path), item.location[1] or 0, f"requiere datos de terceros no redistribuibles: {f} (make datos_terceros)")


@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    out = yield
    rep = out.get_result()
    if rep.failed:
        f = _falta_terceros(_texto(rep))
        if f:
            rep.outcome = "skipped"
            rep.longrepr = (str(collector.path), 0, f"requiere datos de terceros no redistribuibles: {f} (make datos_terceros)")
