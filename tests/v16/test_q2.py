"""Tests rápidos (< 60 s) de Q2: vivienda turística. Leen las salidas ya generadas y comprueban estimadores con datos sintéticos."""
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


def test_twfe_recupera_beta():
    from src.v16.q_comun import twfe
    rng = np.random.default_rng(2)
    n, T = 30, 6
    u = np.repeat(np.arange(n), T)
    t = np.tile(np.arange(T), n)
    z = np.repeat(rng.normal(size=n), T)
    post = (t >= 3).astype(float)
    y = 0.5 * np.repeat(rng.normal(size=n), T) + 0.2 * t + 0.05 * z * post + rng.normal(0, 0.001, n * T)
    df = pd.DataFrame({"u": u, "t": t, "y": y, "x": z * post})
    r = twfe(df, "y", "x", "u", "t")
    assert abs(r["beta"] - 0.05) < 0.005


def test_sensibilidad_formulas():
    from src.v16.q_comun import cinelli_hazlett_rv, oster_delta
    assert cinelli_hazlett_rv(0.0) == 0.0
    assert 0 < cinelli_hazlett_rv(0.2) < 1
    assert oster_delta(1.0, 0.1, 0.5, 0.3)["delta"] > 0


def test_invariantes_q2():
    res, hechos, informe, base = _invariantes("q2", "Q2")
    det = json.loads((base / "q2_detalle.json").read_text(encoding="utf-8"))
    assert abs([h for h in hechos if h["id"] == "V16-Q2-1"][0]["valor"] - det["q2a"]["beta_por_DT"]) < 1e-12
    reg = pd.read_csv(base / "registro.csv")
    assert "Q2b" in set(reg.pregunta) and reg[reg.pregunta == "Q2b"].rol.str.contains("robustez").all()
    assert "NO APTO" in informe and "Sin p-valor ni IC" in informe
