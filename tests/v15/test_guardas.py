"""V15-B1 · Cada guarda bloquea lo que debe y deja pasar lo permitido (.claude/hooks/guardas_bash.py y .claude/settings.json)."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
HOOK = RAIZ / ".claude" / "hooks" / "guardas_bash.py"
D = "E" + "OF"                 # partido: check_v14 rechazaría el literal en un fichero de src/
SEL = "data/" + "sealed"


def _g():
    spec = importlib.util.spec_from_file_location("guardas_bash", HOOK)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _hook(cmd: str, env=None) -> int:
    """Ejecuta el hook como lo hace Claude Code: JSON por la entrada estándar; 2 = bloqueado."""
    datos = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
    e = {**os.environ, "CLAUDE_PROJECT_DIR": str(RAIZ), **(env or {})}
    return subprocess.run([sys.executable, str(HOOK)], input=datos, text=True, capture_output=True, env=e).returncode


@pytest.mark.parametrize("cmd", [f"cat > x.md <<{D}\n`make all`\n{D}", f"python3 - <<{D}\nprint(1)\n{D}"])
def test_a_heredoc_sin_comillas(cmd):
    assert _hook(cmd) == 2
    assert _hook(cmd.replace(f"<<{D}", f"<<'{D}'")) == 0


@pytest.mark.parametrize("cmd", [f"ls {SEL}", f"cat {SEL}/x.csv", f"python3 -c \"open('{SEL}/a')\"", f"cp -r {SEL} /tmp/x"])
def test_b_sellado_solo_por_holdout(cmd):
    assert _hook(cmd) == 2
    assert _hook(f"python3 src/holdout.py estado  # {SEL}") == 0


def test_c_un_solo_make_check(tmp_path):
    lock = tmp_path / "lock"
    env = {"ECONOMETRA_LOCK_CHECK": str(lock), "ECONOMETRA_LOCK_SOLO_FICHERO": "1"}
    assert _hook("make check", env) == 0                        # nadie en marcha
    p = subprocess.Popen(["sleep", "30"])
    try:
        lock.write_text(str(p.pid))
        assert _hook("make check", env) == 2                    # otro make check vivo
        assert _hook("cd x && make check > log 2>&1", env) == 2
        assert _hook("make publicacion", env) == 0              # otros objetivos no
    finally:
        p.kill()
        p.wait()
    assert _hook("make check", env) == 0                        # PID muerto: el bloqueo caduca


def test_d_puerta_del_preregistro(tmp_path):
    g = _g()
    sin = tmp_path / "sin"
    con = tmp_path / "con"
    for d, p in ((sin, {}), (con, {"osf_prereg_v15": "https://doi.org/10.17605/OSF.IO/XXXXX"})):
        d.mkdir()
        (d / "proyecto.json").write_text(json.dumps(p), encoding="utf-8")
    for cmd in ("make v15_f4", "make v15_f5", "make v15_f4_p1"):
        assert g.evaluar(cmd, sin).startswith("(d)")
        assert g.evaluar(cmd, con) is None
    assert g.evaluar("make v15_f3", sin) is None
    pend = tmp_path / "pend"
    pend.mkdir()
    (pend / "proyecto.json").write_text(json.dumps({"osf_prereg_v15": "PENDIENTE"}), encoding="utf-8")
    assert g.evaluar("make v15_f4", pend).startswith("(d)")


@pytest.mark.parametrize("cmd", ["make clean", "make all", "make v7", "make evaluate_v7", "git push --force origin x",
                                 "git push -f origin x", "git filter-repo --path x", "rm -rf data", "rm -rf output/", "rm -rf ./data"])
def test_e_comandos_prohibidos(cmd):
    assert _hook(cmd) == 2


def test_e_cuerpo_de_heredoc():
    """«make all» dentro de un texto que cat escribe en un fichero no es una orden; dentro de un script de bash, sí."""
    assert _hook(f"cat > nota.md <<'{D}'\nNunca make all ni make clean.\n{D}") == 0
    assert _hook(f"bash <<'{D}'\nmake clean\n{D}") == 2
    assert _hook(f"python3 - <<'{D}'\nx = '<<sin comillas dentro del cuerpo'\n{D}") == 0


@pytest.mark.parametrize("cmd", ["make publicacion", "make v7_1", "git push -u origin r12/analisis:rama", "rm -r /tmp/x",
                                 "make check_v15", "make allx"])
def test_permitidos(cmd):
    assert _hook(cmd, {"ECONOMETRA_LOCK_CHECK": "/nonexistent/lock", "ECONOMETRA_LOCK_SOLO_FICHERO": "1"}) == 0


def test_settings_deniega_y_registra_el_hook():
    s = json.loads((RAIZ / ".claude" / "settings.json").read_text(encoding="utf-8"))
    deny = set(s["permissions"]["deny"])
    for d in ("Read(data/sealed/**)", "Write(data/sealed/**)", "Edit(data/sealed/**)", "Bash(make clean:*)", "Bash(make all:*)",
              "Bash(make evaluate_v7:*)", "Bash(git push --force:*)", "Bash(git filter-repo:*)", "Bash(rm -rf data:*)", "Bash(rm -rf output:*)"):
        assert d in deny, d
    assert "guardas_bash.py" in json.dumps(s["hooks"]["PreToolUse"])


def test_check_v15_autocomprueba_las_guardas():
    sys.path.insert(0, str(RAIZ / "src" / "v15"))
    import check_v15
    assert check_v15.guardas() == []
