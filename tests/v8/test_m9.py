"""Tests rapidos de M9 (salidas ya escritas + piezas sinteticas)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src"))
import m9_ml as m  # noqa: E402

OUT = RAIZ / "output" / "v8" / "M9"


def test_folds_embargo():
    q = [f"{a}Q{k}" for a in range(2009, 2027) for k in range(1, 5)]
    for tr, te in m.folds_tiempo(q):
        assert max(tr) < min(te)
        i = {t: j for j, t in enumerate(q)}
        assert i[min(te)] - i[max(tr)] > 4


def test_ar_y_gam_sinteticos():
    rng = np.random.default_rng(1)
    n = 300
    d = pd.DataFrame({"x1": rng.normal(size=n), "x2": rng.normal(size=n), "ccaa": 0})
    d["y1"] = rng.normal(size=n)
    d["y"] = np.sin(d["x1"]) + 0.5 * d["y1"] + 0.1 * rng.normal(size=n)
    tr, te = d.iloc[:200], d.iloc[200:]
    p = m.pred_gam(tr, te, ["x1", "x2"], ["y1"], 1.0)
    assert np.corrcoef(p, te["y"])[0, 1] > 0.9
    pa = m.pred_ar(tr, te, ["y1"], False)
    assert len(pa) == len(te)


def test_monotonia_vector():
    assert m.monot_vec(["tipo_hip_real", "visados", "ocupados"], True) == [-1, 0, 1]
    assert m.monot_vec(["tipo_hip_real"], False) == [0]


def test_salidas():
    r = json.loads((OUT / "resultado.json").read_text())
    assert r["capa"] == "C4" and set(r["fuera_muestra"]) >= {"compra/ccaa_panel", "alquiler/nacional"}
    a = pd.read_csv(OUT / "atribucion.csv")
    assert list(a.columns) == m.COLS_ATR and set(a["capa"]) == {"C4"}
    assert a["notas"].str.contains("contraste, no causal").all()
    assert "shap" in set(a["metodo"])
    k = pd.read_csv(OUT / "ranking_shap.csv")
    assert {"mercado", "periodo", "factor", "rango_mediano", "prob_primero"} <= set(k.columns)
    assert k["prob_primero"].between(0, 1).all()
    reg = pd.read_csv(OUT / "registro.csv")
    assert len(reg) > 30
    est = pd.read_csv(OUT / "estabilidad_ranking.csv")
    assert (est["B"] >= 30).all()
