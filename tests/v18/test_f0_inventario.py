"""V18 · Fase 0: el inventario es determinista, no lee datos y cubre E1-E12 y F1-F3."""
import csv
import importlib.util
import io
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("f0_inventario", RAIZ / "src" / "v18" / "f0_inventario.py")
f0 = importlib.util.module_from_spec(spec)
sys.modules["f0_inventario"] = f0   # dataclasses necesita el módulo registrado
spec.loader.exec_module(f0)

ESPERADOS = [f"E{i}" for i in range(1, 13)] + ["F1", "F2", "F3"]


def test_declara_alcance_sin_lectura():
    texto = (RAIZ / "src" / "v18" / "f0_inventario.py").read_text(encoding="utf-8")
    assert 'ALCANCE_TERRITORIAL = "sin lectura de datos"' in texto
    assert "read_parquet" not in texto and "read_csv(" not in texto


def test_determinista(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    f0.main(a)
    f0.main(b)
    for nombre in ("inventario.csv", "informe.md"):
        assert (a / nombre).read_bytes() == (b / nombre).read_bytes()


def test_todos_los_estudios_y_columnas(tmp_path):
    f0.main(tmp_path)
    filas = list(csv.DictReader(io.StringIO((tmp_path / "inventario.csv").read_text(encoding="utf-8"))))
    assert list(filas[0]) == f0.COLUMNAS
    assert sorted({f["estudio"] for f in filas}, key=ESPERADOS.index) == ESPERADOS
    for e in ESPERADOS:
        usos = {f["uso"] for f in filas if f["estudio"] == e}
        assert "réplica" in usos, e
    assert {f["estado"] for f in filas} <= set(f0.ESTADOS)
    assert {f["requiere_autor"] for f in filas} <= {"sí", "no", ""}
    informe = (tmp_path / "informe.md").read_text(encoding="utf-8")
    for e in ESPERADOS:
        assert f"## {e} · " in informe, e
    assert informe.count("**Veredicto preliminar: ") == len(ESPERADOS)


def test_sellado_v6_barcelona_no_madrid_si():
    sel = f0.sellado()
    assert "08" not in sel["provincias"] and "28" in sel["provincias"]
    assert len(sel["ccaa"]) == 8 and "13" in sel["ccaa"] and "09" not in sel["ccaa"]
