"""V15-B · E1: comprobaciones rápidas de la salida (entrenamiento, C4, pendiente de evaluación sellada)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "output" / "v15" / "p2"


def test_resultado_forma_y_capa():
    r = json.loads((R / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in r
    assert r["capa"] == "C4" and r["pendiente_sellada"] is True and r["p_ajustado"] is None
    assert "p_valores_para_BY" in r and len(r["p_valores_para_BY"]) >= 1


def test_hechos_y_ficha():
    h = json.loads((R / "hechos.json").read_text(encoding="utf-8"))
    assert 1 <= len(h) <= 10
    for x in h:
        assert x["id"].startswith("V15-") and x["capa"] == "C4"
        assert x["ficha"].startswith("output/v15/p2/informe.md#")
        assert "{#" + x["ficha"].split("#")[1] + "}" in (R / "informe.md").read_text(encoding="utf-8")
