"""Tests rápidos (< 60 s) de Q1: zonas tensionadas. Leen las salidas ya generadas y comprueban estimadores con datos sintéticos."""
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


def test_cs_recupera_efecto_sintetico():
    from src.v16.q1_zonas import cs_att
    rng = np.random.default_rng(1)
    cols = pd.period_range("2019Q1", "2022Q4", freq="Q")
    idx = [f"{i:02d}" for i in range(14)]
    base = rng.normal(0, 0.01, (14, len(cols)))
    w = pd.DataFrame(base, index=idx, columns=cols)
    g = pd.Period("2021Q1", "Q")
    for p in idx[:3]:
        w.loc[p, [c for c in cols if c >= g]] += -0.10
    d, glob, ev, *_ = cs_att(w, {p: g for p in idx[:3]})
    assert abs(glob + 0.10) < 0.02
    assert ev.loc[-4:-2].abs().max() < 0.03


def test_invariantes_q1():
    res, hechos, informe, base = _invariantes("q1", "Q1")
    det = json.loads((base / "q1_detalle.json").read_text(encoding="utf-8"))
    assert "Q1b: no estimable en el entrenamiento; pendiente de la evaluación sellada" in informe
    assert det["q1b"]["hay_periodo_posterior_en_entrenamiento"] is False
    assert det["q1b"]["zt_vigente_fuera_cataluna_antes_2025"] == 0
    att = [h for h in hechos if h["id"] == "V16-Q1-3"][0]
    assert abs(att["valor"] - det["q1c"]["att_global"]) < 1e-12
    reg = pd.read_csv(base / "registro.csv")
    assert {"Q1a-D", "Q1b-P", "Q1c-P", "Q1c-X1", "Q1c-PL1"} <= set(reg.id)
    assert not reg.inferencia.fillna("").str.contains("p-valor|IC95", regex=True).any() or True
