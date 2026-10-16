"""V14: control de heredocs sin comillas (incidencia D3 de V13)."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v14 import check_v14 as C  # noqa: E402


def test_repositorio_sin_heredocs_sin_comillas():
    assert C.heredocs_sin_comillas() == []


def test_detecta_heredoc_sin_comillas(tmp_path):
    malo, bueno = tmp_path / "malo.sh", tmp_path / "bueno.sh"
    delim = "E" + "OF"   # concatenado: el propio control rechazaría el literal en este fichero
    malo.write_text(f"cat > x.md <<{delim}\n`make all`\n{delim}\n", encoding="utf-8")
    bueno.write_text(f"cat > x.md <<'{delim}'\n`make all`\n{delim}\nx=$((1 << 2))\n", encoding="utf-8")
    assert len(C.heredocs_sin_comillas([str(malo)])) == 1
    assert C.heredocs_sin_comillas([str(bueno)]) == []


def test_hash_sellado_aviso_en_desarrollo_error_en_arbol():
    pendiente = {"hash_sellado": {"valor": "PENDIENTE", "comando": "x"}}
    assert C.hash_sellado(pendiente)[0] == [] and len(C.hash_sellado(pendiente)[1]) == 1
    assert len(C.hash_sellado({**pendiente, "arbol_publico": True})[0]) == 1
    assert C.hash_sellado({"hash_sellado": {"valor": "a" * 64}, "arbol_publico": True}) == ([], [])
    assert len(C.hash_sellado({"hash_sellado": {"valor": "no-es-un-hash"}})[0]) == 1


def test_readme_del_arbol_lleva_el_recuento_de_la_ejecucion():
    """V14.1: la primera sección del README del árbol público publica pasados y omitidos de docs/v14/tests_arbol.json."""
    import json
    from src.v14 import tests_arbol as TA
    j = RAIZ / "docs" / "v14" / "tests_arbol.json"
    if not j.exists():   # antes de la primera ejecución en el árbol (bootstrap de V14.1)
        return
    r = json.loads(j.read_text(encoding="utf-8"))
    inicio = TA.readme_inicio(r)
    assert f"Pasan {r['pasados']} tests" in inicio and f"se omiten {r['omitidos']} tests" in inicio
    assert len(inicio.split()) < 120
    if json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8")).get("arbol_publico"):
        assert inicio.strip() in (RAIZ / "README.md").read_text(encoding="utf-8")
