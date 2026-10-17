"""Tests rápidos (< 60 s) de Q7a: diferencia en discontinuidades por edad. Leen las salidas ya generadas y comprueban estimadores con datos sintéticos."""
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


def test_diff_in_disc_sintetico():
    from src.v16.q7_bono import did_disc
    rng = np.random.default_rng(3)
    filas = []
    for anio in (2019, 2020, 2023, 2024):
        for edad in range(28, 43):
            for _ in range(60):
                T = edad <= 35
                post = anio >= 2023
                y = 0.05 * (edad - 35.5) + 0.08 * T - 0.12 * T * post + rng.normal(0, 0.05)
                filas.append({"anio": anio, "edad_sust": edad, "y": y, "DB090": 1.0})
    r = did_disc(pd.DataFrame(filas), "y", 5)
    assert abs(r["diferencia_en_discontinuidades"] + 0.12) < 0.02
    assert abs(r["salto_antes"] - 0.08) < 0.02


def test_invariantes_q7():
    res, hechos, informe, base = _invariantes("q7", "Q7")
    det = json.loads((base / "q7_detalle.json").read_text(encoding="utf-8"))
    assert det["plan_2018_2021"]["existia_programa_para_menores_de_35"] is True
    assert "Sí tenía un programa para menores de 35 años" in informe
    assert "Kolesár-Rothe" in informe
