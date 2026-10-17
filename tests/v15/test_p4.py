"""V15-B · H4: comprobaciones rápidas de la salida (entrenamiento, C4, pendiente de evaluación sellada)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "output" / "v15" / "p4"


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
        assert x["ficha"].startswith("output/v15/p4/informe.md#")
        assert "{#" + x["ficha"].split("#")[1] + "}" in (R / "informe.md").read_text(encoding="utf-8")


def test_sin_inferencia_por_herramienta_no_apta():
    r = json.loads((R / "resultado.json").read_text(encoding="utf-8"))
    assert r["ic95"] is None and all(p["p"] is None for p in r["p_valores_para_BY"])
    assert len(r["p_valores_para_BY"]) == 65


def test_instrumento_forma():
    import numpy as np
    from src.v15.p4_inmigracion import ANIOS, instrumento
    A = np.abs(np.random.default_rng(1).normal(10, 2, (6, 3, len(ANIOS)))) + 1
    z, zk, sh = instrumento(A, {"a": 0, "b": 1, "Total": 2}, ["a", "b"], 2003)
    assert z.shape == (6, len(ANIOS)) and np.isnan(z).sum() == 0
