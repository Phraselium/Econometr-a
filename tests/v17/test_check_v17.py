"""V17 · check_v17: las cifras V17 son C4 con lectura propia y todo lleva el rótulo «a posteriori»."""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v17"))
import check_v17  # noqa: E402


def test_repositorio_pasa():
    assert check_v17.a_posteriori() == []
    assert check_v17.cifras() == []
    assert check_v17.sin_promocion() == []


def test_cifra_promovida_falla(tmp_path, monkeypatch):
    d = tmp_path / "output" / "v17" / "x"
    d.mkdir(parents=True)
    (d / "hechos.json").write_text(json.dumps([{"id": "V17-X", "fuentes": ["INE"], "capa": "C1", "lectura_v17": "OF"}]))
    monkeypatch.setattr(check_v17, "OUT", tmp_path / "output" / "v17")
    monkeypatch.setattr(check_v17, "RAIZ", tmp_path)
    e = check_v17.cifras()
    assert any("capa" in x for x in e)
    assert check_v17.a_posteriori()   # sin rótulo


def test_cifra_correcta_pasa(tmp_path, monkeypatch):
    d = tmp_path / "output" / "v17" / "x"
    d.mkdir(parents=True)
    (d / "hechos.json").write_text(json.dumps([{"id": "V17-X", "fuentes": ["INE"], "capa": "C4", "lectura_v17": "OF",
                                                "tipo_rango": "sin rango", "cobertura": "España", "nota": "a posteriori"}]))
    monkeypatch.setattr(check_v17, "OUT", tmp_path / "output" / "v17")
    monkeypatch.setattr(check_v17, "RAIZ", tmp_path)
    assert check_v17.cifras() == [] and check_v17.a_posteriori() == []


def test_tipo_rango_y_cobertura_obligatorios(tmp_path, monkeypatch):
    d = tmp_path / "output" / "v17" / "x"
    d.mkdir(parents=True)
    (d / "hechos.json").write_text(json.dumps([{"id": "V17-X", "fuentes": ["INE"], "capa": "C4", "lectura_v17": "OF",
                                                "cobertura": "véase la ficha", "nota": "a posteriori"}]))
    monkeypatch.setattr(check_v17, "OUT", tmp_path / "output" / "v17")
    monkeypatch.setattr(check_v17, "RAIZ", tmp_path)
    e = check_v17.cifras()
    assert any("tipo_rango" in x for x in e) and any("cobertura" in x for x in e)
