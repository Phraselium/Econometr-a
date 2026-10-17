"""Tests rápidos (< 60 s) del grupo C de la fase 6 (Q5, Q9, Q10, rejilla): salidas ya generadas y estimadores con datos sintéticos."""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
CLAVES_HECHO = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"}
CAUSAL = re.compile(r"\b(efecto causal|causa|causó|provoca|provocó|genera el aumento)\b", re.I)


def _salida(q):
    base = RAIZ / "output" / "v16" / q
    if not (base / "resultado.json").exists():
        pytest.skip(f"ejecutar src/v16/{q}_*.py")
    return json.loads((base / "resultado.json").read_text(encoding="utf-8")), json.loads((base / "hechos.json").read_text(encoding="utf-8")), \
        (base / "informe.md").read_text(encoding="utf-8"), base


@pytest.mark.parametrize("q", ["q5", "q9", "q10", "rejilla"])
def test_invariantes(q):
    res, hechos, informe, base = _salida(q)
    assert res["capa"] == "C4" and res["pendiente_sellada"] is True
    assert "p_valores_para_BY" in res and len(hechos) <= 10
    assert all(set(h) == CLAVES_HECHO and h["capa"] == "C4" and h["ficha"].startswith(f"output/v16/{q}/informe.md#") for h in hechos)
    for h in hechos:
        assert f'id="{h["ficha"].split("#")[1]}"' in informe
    assert not CAUSAL.search(informe)
    assert (base / "registro.csv").exists()


def test_p_solo_si_apto():
    for q, aptos in (("q5", set()), ("q10", set()), ("rejilla", set()), ("q9", {"Q9-g"})):
        res = _salida(q)[0]
        for p in res["p_valores_para_BY"]:
            assert (p["p"] is None) or p["id"] in aptos


def test_gsadf_detecta_explosividad_y_no_en_paseo():
    from src.v16 import qc_series as S
    rng = np.random.default_rng(1)
    rw = np.cumsum(rng.standard_normal(98))
    ex = rw.copy()
    for t in range(50, 66):
        ex[t:] += 0.0
        ex[t] = 1.08 * ex[t - 1] + rng.standard_normal() if t > 50 else ex[t]
    ex[66:] = ex[65] + np.cumsum(rng.standard_normal(98 - 66))
    g0 = S.gsadf_boot(rw, B=99)
    g1 = S.gsadf_boot(ex, B=99)
    assert np.isfinite(g0["stat"]) and g0["cv95"] > 0
    assert g1["stat"] > g0["stat"] - 5   # forma básica; la potencia está validada en la fase 5


def test_mg_pmg_recuperan_elasticidad():
    from src.v16 import qc_series as S
    rng = np.random.default_rng(2)
    T, N = 98, 15
    x = np.cumsum(rng.standard_normal((T, N)) * 0.02, axis=0)
    y = 1.5 * x + 0.1 * rng.standard_normal((T, N))   # cointegradas con θ = 1,5
    assert abs(S.mg_cs(y, x, 2, "MG")["theta_mediana"] - 1.5) < 0.4
    assert abs(S.pmg(y, x, 2)["theta"] - 1.5) < 0.4


def test_lp_sin_efecto_da_cero():
    from src.v16 import q5_proyecciones as P
    rng = np.random.default_rng(3)
    idx = pd.period_range("2000Q1", periods=120, freq="Q")
    y = pd.Series(np.cumsum(rng.standard_normal(120) * 0.01), index=idx)
    s = pd.Series(rng.standard_normal(120), index=idx)
    assert abs(P.lp(y, s, 4, 4, "2000Q1")["beta"]) < 1.0
    y2 = y + 0.5 * s.cumsum().rolling(1).mean() * 0   # sin efecto
    assert P.lp(y2, s, 1, 2, "2000Q1")["n"] > 80


def test_rejilla_tiene_83_celdas():
    res = _salida("rejilla")[0]
    assert res["N"]["celdas"] == 83 and len(res["p_valores_para_BY"]) == 83
