"""V16-B1 · Guardas: (d) prereg-v15 en el remoto en 542b4fd, (f) prereg-v16 en el remoto para las fases 5-7, las de V15 siguen
vigentes, y check_v16 detecta estimaciones anteriores a su etiqueta. Sin red: el remoto se simula con
ECONOMETRA_ETIQUETAS_REMOTAS."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
V15 = "make " + "v15_f"
V16 = "make " + "v16"
SHA15 = "542b4fdf398970c817af7abfcd20c92dda299c69"


def _g():
    spec = importlib.util.spec_from_file_location("guardas_bash", RAIZ / ".claude/hooks/guardas_bash.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


@pytest.fixture
def remoto(tmp_path, monkeypatch):
    def fijar(etiquetas: dict):
        f = tmp_path / "remoto.json"
        f.write_text(json.dumps(etiquetas), encoding="utf-8")
        monkeypatch.setenv("ECONOMETRA_ETIQUETAS_REMOTAS", str(f))
    return fijar


@pytest.mark.parametrize("cmd", [f"{V15}4", f"{V15}5", f"{V15}4_p6", f"cd x && {V15}5"])
def test_d_sin_etiqueta_v15_bloquea(remoto, cmd):
    remoto({})
    assert _g().evaluar(cmd, RAIZ).startswith("(d)")


def test_d_etiqueta_v15_en_otro_commit_bloquea(remoto):
    remoto({"prereg-v15": "deadbeef" * 5})
    assert _g().evaluar(f"{V15}4", RAIZ).startswith("(d)")


def test_d_etiqueta_v15_correcta_deja_pasar(remoto):
    remoto({"prereg-v15": SHA15})
    assert _g().evaluar(f"{V15}4", RAIZ) is None


@pytest.mark.parametrize("cmd", [f"{V16}_f5", f"{V16}_f6", f"{V16}_f7", f"{V16}_f6_q1", V16, f"{V16} ; ls"])
def test_f_sin_etiqueta_v16_bloquea(remoto, cmd):
    remoto({"prereg-v15": SHA15})
    assert _g().evaluar(cmd, RAIZ).startswith("(f)")


@pytest.mark.parametrize("cmd", [f"{V16}_f0", f"{V16}_f1", f"{V16}_f4", "make check_v16"])
def test_f_fases_previas_libres(remoto, cmd):
    remoto({})
    assert _g().evaluar(cmd, RAIZ) is None


def test_f_con_etiqueta_v16_deja_pasar(remoto):
    remoto({"prereg-v16": "abc1234"})
    assert _g().evaluar(f"{V16}_f5", RAIZ) is None


def test_sin_red_la_puerta_queda_cerrada(monkeypatch):
    monkeypatch.delenv("ECONOMETRA_ETIQUETAS_REMOTAS", raising=False)
    sys.path.insert(0, str(RAIZ / "src" / "v16"))
    import etiquetas
    monkeypatch.setattr(etiquetas.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(OSError("sin red")))
    assert etiquetas.remota("prereg-v16") is None
    assert not etiquetas.prereg_v16_publicada()[0]


@pytest.mark.parametrize("cmd", ["make clean", "make all", "make v7", "make evaluate_v7", "git push --force origin x", "rm -rf data"])
def test_guardas_v15_siguen_vigentes(cmd):
    assert _g().evaluar(cmd, RAIZ).startswith("(e)")


def test_estimacion_antes_de_su_etiqueta(tmp_path, monkeypatch):
    """check_v16 detecta un commit de estimación anterior a la etiqueta y acepta uno posterior."""
    sys.path.insert(0, str(RAIZ / "src" / "v16"))
    import check_v16 as C

    def git(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, capture_output=True, text=True, check=True)
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (tmp_path / "src" / "v16").mkdir(parents=True)
    (tmp_path / "src" / "v16" / "q1_zonas.py").write_text("x = 1\n")
    git("add", "-A")
    git("commit", "-qm", "estimación antes de la etiqueta")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "pre.md").write_text("pre\n")
    git("add", "-A")
    git("commit", "-qm", "pre-registro")
    git("tag", "prereg-v16")
    monkeypatch.setattr(C, "RAIZ", tmp_path)
    err = C.estimaciones_tras_etiqueta()
    assert len(err) == 1 and "anterior a prereg-v16" in err[0]
    git("tag", "-d", "prereg-v16")
    git("tag", "prereg-v16", "HEAD~1")
    assert C.estimaciones_tras_etiqueta() == []


def test_sin_etiqueta_no_puede_haber_estimaciones(tmp_path, monkeypatch):
    sys.path.insert(0, str(RAIZ / "src" / "v16"))
    import check_v16 as C
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "output" / "v16" / "q2_turismo").mkdir(parents=True)
    (tmp_path / "output" / "v16" / "q2_turismo" / "resultado.json").write_text("{}")
    for a in (["config", "user.email", "t@t"], ["config", "user.name", "t"], ["add", "-A"], ["commit", "-qm", "x"]):
        subprocess.run(["git", *a], cwd=tmp_path, check=True)
    monkeypatch.setattr(C, "RAIZ", tmp_path)
    assert C.estimaciones_tras_etiqueta() == ["1 commits con estimaciones sin la etiqueta prereg-v16"]
