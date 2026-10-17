"""Tests rápidos (< 60 s) de Q8: compras de no residentes. Leen las salidas ya generadas y comprueban estimadores con datos sintéticos."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
CLAVES_HECHO = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"}


def _cargar(q):
    base = RAIZ / "output" / "v16" / q
    if not (base / "resultado.json").exists():
        pytest.skip(f"ejecutar src/v16/q_salidas.py ({q})")
    return (json.loads((base / "resultado.json").read_text(encoding="utf-8")), json.loads((base / "hechos.json").read_text(encoding="utf-8")),
            (base / "informe.md").read_text(encoding="utf-8"), base)


def _invariantes(q, Q):
    res, hechos, informe, base = _cargar(q)
    assert res["capa"] == "C4" and res["pendiente_sellada"] is True and res["ic95"] is None
    assert res["p_valores"] == [] and res["nivel_evidencia"] == "DESCRIPTIVO"
    assert 1 <= len(hechos) <= 10
    for h in hechos:
        assert CLAVES_HECHO <= set(h) and h["id"].startswith(f"V16-{Q}-") and h["capa"] == "C4"
        ruta, ancla = h["ficha"].split("#")
        assert ruta == f"output/v16/{q}/informe.md" and f'id="{ancla}"' in informe
    assert (base / "registro.csv").exists()
    for clave in ("rama", "pregunta", "datos", "N", "metodo", "estimacion", "diagnosticos", "fuera_muestra", "notas"):
        assert clave in res
    assert not any(w in informe.lower() for w in (" causa ", "causal es", "provoca", "reduce el alquiler", "aumenta el alquiler"))
    return res, hechos, informe, base


def test_invariantes_q8():
    res, hechos, informe, base = _invariantes("q8", "Q8")
    det = json.loads((base / "q8_detalle.json").read_text(encoding="utf-8"))
    c = det["cambio"]
    assert abs(c["cuota_no_res_antes"] - 100 * c["compras_no_res_antes"] / c["compras_total_antes"]) < 1e-9
    assert abs(c["cuota_no_res_despues"] - 100 * c["compras_no_res_despues"] / c["compras_total_despues"]) < 1e-9


def test_agregado_sin_ccaa_selladas():
    from src.v16.q8_no_residentes import CCAA, SELLADAS_PROV
    prohibidas = {"Aragón", "Asturias (Principado de)", "Balears (Illes)", "Canarias", "Madrid (Comunidad de)", "Murcia (Región de)", "Navarra (Comunidad Foral de)", "Rioja (La)"}
    assert not prohibidas & set(CCAA)
    assert {"Zaragoza", "Huesca", "Teruel"} <= set(SELLADAS_PROV)
