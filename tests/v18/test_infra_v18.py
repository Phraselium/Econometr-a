"""V18 · Infraestructura: puerta del plan de replicación, guarda (g) del hook y controles de check_v18."""
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import check_v18  # noqa: E402
import etiqueta  # noqa: E402

spec = importlib.util.spec_from_file_location("guardas_bash", RAIZ / ".claude" / "hooks" / "guardas_bash.py")
guardas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guardas)


def _simula(tmp_path, monkeypatch, commit, en_remoto):
    f = tmp_path / "etiqueta.json"
    f.write_text(json.dumps({"commit": commit, "en_remoto": en_remoto}), encoding="utf-8")
    monkeypatch.setenv("ECONOMETRA_ETIQUETA_V18", str(f))


def test_puerta(tmp_path, monkeypatch):
    _simula(tmp_path, monkeypatch, None, False)
    assert not etiqueta.puerta()[0]
    _simula(tmp_path, monkeypatch, "abc1234", False)
    assert not etiqueta.puerta()[0]
    _simula(tmp_path, monkeypatch, "abc1234", True)
    assert etiqueta.puerta()[0]


def test_guarda_g(tmp_path, monkeypatch):
    _simula(tmp_path, monkeypatch, None, False)
    for c in ("make v18_f3", "make v18_f4", "make -s v18_f6", "make v18"):
        assert guardas.evaluar(c, RAIZ).startswith("(g)"), c
    for c in ("make v18_f0", "make v18_f1", "make v18_f2", "make check_v18"):
        assert guardas.evaluar(c, RAIZ) is None, c
    _simula(tmp_path, monkeypatch, "abc1234", True)
    assert guardas.evaluar("make v18_f4", RAIZ) is None


def test_lenguaje_causal(tmp_path, monkeypatch):
    out = tmp_path / "output" / "v18" / "x"
    out.mkdir(parents=True)
    h = [{"id": "V18-A", "fuentes": ["f"], "capa": "C4", "clasificacion_v18": "ASOCIACIÓN", "indicador": "La subida se debe a X"},
         {"id": "V18-B", "fuentes": ["f"], "capa": "C4", "clasificacion_v18": "IDENTIFICADO", "indicador": "X causa una subida"},
         {"id": "W-C", "capa": "C9", "clasificacion_v18": "OTRA"}]
    (out / "hechos.json").write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(check_v18, "OUT", tmp_path / "output" / "v18")
    monkeypatch.setattr(check_v18, "RAIZ", tmp_path)
    assert [e for e in check_v18.causal()] and all("V18-A" in e for e in check_v18.causal())
    e = check_v18.cifras()
    assert any("prefijo" in x for x in e) and any("sin fuente" in x for x in e) and any("clasificacion_v18" in x for x in e)


def test_citas_largas(tmp_path, monkeypatch):
    bib = tmp_path / "docs" / "v18" / "bib"
    bib.mkdir(parents=True)
    (bib / "f.md").write_text("Cita corta «una dos tres» y larga «" + " ".join(["p"] * 16) + "».", encoding="utf-8")
    monkeypatch.setattr(check_v18, "RAIZ", tmp_path)
    e = [x for x in check_v18.derechos() if "cita" in x]
    assert len(e) == 1 and "16 palabras" in e[0]


def test_repositorio_pasa():
    assert check_v18.main() == 0
