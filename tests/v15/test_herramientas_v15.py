"""V15-B3/B4 · Verificador de referencias (sin red, con caché), registro de subagentes, puerta y lanzador de fases."""
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v15"))
import puerta as P  # noqa: E402
import registro_subagentes as RS  # noqa: E402
import verificar_referencias as VR  # noqa: E402

FICHAS = """# Prueba

### Saiz (2010). The Geographic Determinants of Housing Supply
- DOI: 10.1162/qjec.2010.125.3.1253 · Revista: QJE
- Estado: NO VERIFICADA

### Saiz (2010). Un título que no se parece en nada
- DOI: 10.1162/qjec.2010.125.3.1253 · Revista: QJE
- Estado: NO VERIFICADA

### Autor (2020). Documento de trabajo sin DOI
- DOI: sin DOI · Revista: serie
- Estado: NO VERIFICADA
"""
CACHE = {"10.1162/qjec.2010.125.3.1253": {"existe": True, "titulo": "The Geographic Determinants of Housing Supply",
                                           "primer_autor": "Saiz", "anio": 2010, "revista": "Quarterly Journal of Economics",
                                           "issn": ["0033-5533"], "consulta": "2026-10-17"},
         "10.9999/no.existe": {"existe": False, "consulta": "2026-10-17"}}


def _preparar(tmp_path, monkeypatch, fichas=FICHAS, scimago=True):
    lit = tmp_path / "literatura"
    lit.mkdir()
    (lit / "p1.md").write_text(fichas, encoding="utf-8")
    (lit / "crossref_cache.json").write_text(json.dumps(CACHE), encoding="utf-8")
    sj = tmp_path / "scimago.csv"
    if scimago:
        sj.write_text("revista,issn,cuartil,categoria,anio_scimago,fecha_consulta\nQuarterly Journal of Economics,0033-5533,Q1,Economics,2024,2026-10-17\n",
                      encoding="utf-8")
    monkeypatch.setattr(VR, "LIT", lit)
    monkeypatch.setattr(VR, "CACHE", lit / "crossref_cache.json")
    monkeypatch.setattr(VR, "SCIMAGO", sj)
    return lit / "p1.md"


def test_verificador_marca_cada_caso(tmp_path, monkeypatch):
    f = _preparar(tmp_path, monkeypatch)
    cuenta, errores = VR.procesar(red=False, escribir=True)
    t = f.read_text(encoding="utf-8")
    assert errores == []
    assert "Estado: VERIFICADA (Crossref; cuartil Q1 Scimago 2024)" in t
    assert "Estado: DISCREPANTE (título)" in t
    assert "Estado: NO VERIFICADA (sin DOI)" in t
    assert cuenta == {"VERIFICADA": 1, "DISCREPANTE": 1, "NO VERIFICADA": 1}


def test_verificador_sin_cuartil(tmp_path, monkeypatch):
    f = _preparar(tmp_path, monkeypatch, scimago=False)
    VR.procesar(red=False, escribir=True)
    assert "VERIFICADA (Crossref; cuartil no verificado)" in f.read_text(encoding="utf-8")


def test_verificador_falla_con_doi_inexistente(tmp_path, monkeypatch):
    _preparar(tmp_path, monkeypatch, fichas="### X (2020). Algo\n- DOI: 10.9999/no.existe\n- Estado: NO VERIFICADA\n")
    _, errores = VR.procesar(red=False, escribir=False)
    assert errores and "inexistente" in errores[0]


def test_registro_subagentes(tmp_path, monkeypatch):
    monkeypatch.setattr(RS, "CSV", tmp_path / "s.csv")
    monkeypatch.setattr(RS, "ESTADO", tmp_path / "estado.md")
    (tmp_path / "estado.md").write_text("# V15 · Estado\n\n## Hecho\n- x\n", encoding="utf-8")
    for tok in (1000, 2500):
        monkeypatch.setattr(sys, "argv", ["x", "--rol", "auditor-datos", "--tarea", "F1", "--tokens", str(tok), "--fecha", "2026-10-17"])
        RS.main()
    t = (tmp_path / "estado.md").read_text(encoding="utf-8")
    assert t.count("## Subagentes y tokens") == 1 and "Total: 3.500 tokens" in t and "## Hecho" in t


def test_puerta():
    assert not P.abierta({})[0] and not P.abierta({"osf_prereg_v15": "PENDIENTE"})[0]
    assert P.abierta({"osf_prereg_v15": "https://doi.org/10.17605/OSF.IO/ABCDE", "osf_prereg_v15_fecha": "2026-11-01"})[0]


def test_fases_4_y_5_cerradas_sin_osf():
    p = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
    if P.abierta(p)[0]:
        return
    for f in ("f4", "f5"):
        r = subprocess.run([sys.executable, str(RAIZ / "src/v15/fase.py"), f], cwd=RAIZ, capture_output=True, text=True)
        assert r.returncode == 1 and "osf_prereg_v15" in r.stdout


def test_lecturas_v6_exige_filtro(tmp_path, monkeypatch):
    import check_v15 as C
    src = tmp_path / "src" / "v99"
    src.mkdir(parents=True)
    (src / "malo.py").write_text('import duckdb\nduckdb.sql("select * from \'data/base/hechos.parquet\'")\n', encoding="utf-8")
    (src / "bueno.py").write_text('q = "select * from \'data/base/hechos.parquet\' where not muestra_sellada_v6"\n', encoding="utf-8")
    (tmp_path / "docs" / "v15").mkdir(parents=True)
    monkeypatch.setattr(C, "RAIZ", tmp_path)
    err = C.lecturas_v6()
    assert len(err) == 1 and "malo.py" in err[0]
