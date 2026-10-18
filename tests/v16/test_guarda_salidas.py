"""V16 · Guarda de salidas cerradas (incidente de B-3: un subagente vació output/v9/d4/registry.csv)."""
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("guarda_salidas", RAIZ / ".claude" / "hooks" / "guarda_salidas_cerradas.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)


def _sub(herr, ti):
    return {"agent_id": "a1", "agent_type": "general-purpose", "tool_name": herr, "tool_input": ti}


def test_rutas_cerradas():
    assert G.ruta_cerrada("output/v9/d4/registry.csv")
    assert G.ruta_cerrada("./output/v8/M5/atribucion.csv")
    assert G.ruta_cerrada("data/base/v8_atribucion.parquet")
    assert G.ruta_cerrada("publicacion/tablas_v8.xlsx")
    assert G.ruta_cerrada("output/informe.md")
    assert not G.ruta_cerrada("output/v16/q3/resultado.json")
    assert not G.ruta_cerrada("output/v15/p4/informe.md")
    assert not G.ruta_cerrada("/tmp/x/registry.csv")


def test_subagente_bloqueado():
    assert G.evaluar(_sub("Write", {"file_path": f"{RAIZ}/output/v9/d4/registry.csv"}))
    assert G.evaluar(_sub("Edit", {"file_path": "data/base/v8_atribucion.parquet"}))
    assert G.evaluar(_sub("Bash", {"command": "python3 src/v9/d4_inmigracion.py"}))
    assert G.evaluar(_sub("Bash", {"command": f"cd {RAIZ} && python src/f3_inmigracion.py"}))
    assert G.evaluar(_sub("Bash", {"command": "echo x > output/v8/M5/resumen.md"}))


def test_subagente_permitido():
    assert G.evaluar(_sub("Write", {"file_path": "output/v16/replica/q6p/resultado.json"})) is None
    assert G.evaluar(_sub("Bash", {"command": "python3 /tmp/copia/d4_inmigracion.py --salida /tmp/out"})) is None
    assert G.evaluar(_sub("Bash", {"command": "python3 src/v16/q6_itp.py"})) is None
    assert G.evaluar(_sub("Read", {"file_path": "output/v9/d4/registry.csv"})) is None


def test_orquestador_no_bloqueado():
    d = {"tool_name": "Bash", "tool_input": {"command": "python3 src/v8/m5_lpiv.py"}}
    assert G.evaluar(d) is None
