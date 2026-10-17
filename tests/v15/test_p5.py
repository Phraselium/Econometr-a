"""V15-A · H3 y E4: regresión con dos efectos fijos, Conley y forma de las salidas."""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v15"))
sys.path.insert(0, str(RAIZ / "src"))
import pa_panel as PN  # noqa: E402


def test_ols_fe_recupera_beta_y_conley_positivo():
    rng = np.random.default_rng(20261010)
    S, T = 400, 4
    sec = np.repeat(np.arange(S), T)
    anio = np.tile(np.arange(T), S)
    mun = sec // 8
    xyz = np.column_stack([rng.uniform(0, 30, S), rng.uniform(0, 30, S), np.zeros(S)])
    x = rng.normal(size=S * T) + rng.normal(size=S)[sec]
    y = 0.05 * x + rng.normal(size=S)[sec] + rng.normal(size=(mun.max() + 1) * T)[mun * T + anio] + rng.normal(0, 0.5, S * T)
    grp = mun * T + anio
    K = PN.matriz_conley(xyz, 2.0)
    r = PN.ols_fe(y, x[:, None], sec, grp, mun, sec, K)
    assert abs(r["b"][0] - 0.05) < 4 * r["se_mun"][0]
    assert r["se_conley"][0] > 0 and not r["conley_var_no_positiva"]


def test_demean_2fe_ortogonal():
    rng = np.random.default_rng(1)
    g1, g2 = rng.integers(0, 20, 500), rng.integers(0, 5, 500)
    a = PN.demean_2fe(rng.normal(size=500), g1, g2)[:, 0]
    assert abs(a.mean()) < 1e-9
    assert np.max(np.abs(np.bincount(g2, a) / np.maximum(np.bincount(g2), 1))) < 1e-6


def test_salidas_forma():
    for carp in ("p5", "p5cv"):
        ruta = RAIZ / "output" / "v15" / carp / "resultado.json"
        if not ruta.exists():
            continue
        r = json.loads(ruta.read_text(encoding="utf-8"))
        assert r["capa"] == "C4" and r["pendiente_sellada"] is True and "p_valores_para_BY" in r
        h = json.loads((ruta.parent / "hechos.json").read_text(encoding="utf-8"))
        assert len(h) <= 10 and all(x["id"].startswith("V15-") for x in h)
