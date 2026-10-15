"""V12-F0: el guardia de `make check` detecta un fichero versionado modificado."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v12"))
import git_limpio  # noqa: E402


def test_guardia_detecta_cambios(tmp_path, monkeypatch):
    f = tmp_path / "antes.txt"
    assert git_limpio.main("guardar", str(f)) == 0
    assert git_limpio.main("comparar", str(f)) == 0
    monkeypatch.setattr(git_limpio, "estado", lambda: f.read_text(encoding="utf-8") + " M fichero_inventado.csv\n")
    assert git_limpio.main("comparar", str(f)) == 1


def test_web_no_escribe_resumen_versionado():
    web = (RAIZ / "tests/v10/test_web.py").read_text(encoding="utf-8")
    assert "web.RESUMEN" in web and "tmp_path_factory" in web
    assert subprocess.run(["git", "ls-files", "output/v10/web_resumen.csv"], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
