"""Pruebas rápidas de Q4 (grupo B)."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v16" / "q4"


def test_resultado_q4_solo_puntual():
    r = json.loads((OUT / "resultado.json").read_text(encoding="utf-8"))
    assert r["capa"] == "C4" and r["pendiente_sellada"] is True
    assert r["ic95"] is None and r["p_ajustado"] is None
    assert all(x["p"] is None for x in r["p_valores_para_BY"])
    assert r["estimacion"]["Q4a"]["ic95"] is None and r["estimacion"]["Q4b"]["p"] is None
    assert r["estimacion"]["Q4a"]["multiverso"]["n"] == 8 and r["estimacion"]["Q4b"]["multiverso"]["n"] == 8


def test_hechos_y_registro_q4():
    h = json.loads((OUT / "hechos.json").read_text(encoding="utf-8"))
    assert 0 < len(h) <= 10 and all(x["id"].startswith("V16-Q4") and x["capa"] == "C4" for x in h)
    lineas = (OUT / "registro.csv").read_text(encoding="utf-8").splitlines()
    assert sum("PRINCIPAL" in l for l in lineas) == 2
    assert (OUT / "informe.md").exists()
