"""V18 · wild cluster bootstrap de Webb en TWFE (simulación; sin datos reales)."""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
os.environ["V18_MC_JOBS"] = "1"


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


W = _cargar("t_webb_twfe", "src/v18/herr18/webb_twfe.py")
MC = _cargar("t_mc_webb", "src/v18/montecarlo/webb_twfe.py")


def _panel(seed=1, G=6, T=8):
    rng = np.random.default_rng(seed)
    e, D = MC.dgp(rng, G, T, 3)
    return 0.4 * D + e, D


def test_alcance():
    assert W.ALCANCE_TERRITORIAL == MC.ALCANCE_TERRITORIAL == "sin lectura de datos"


def test_desmedia_margenes_nulos():
    A = np.random.default_rng(0).standard_normal((5, 7))
    d = W.desmedia2(A)
    assert np.allclose(d.mean(0), 0) and np.allclose(d.mean(1), 0)


def test_beta_igual_a_mco_con_dummies():
    y, D = _panel()
    G, T = y.shape
    X = [D.ravel()]
    for g in range(G):
        X.append(np.repeat(np.arange(G) == g, T).astype(float))
    for t in range(1, T):
        X.append(np.tile(np.arange(T) == t, G).astype(float))
    coef = np.linalg.lstsq(np.column_stack(X), y.ravel(), rcond=None)[0]
    assert abs(coef[0] - W.twfe_crve(y, D)[0]) < 1e-9


def test_weights_webb_momentos():
    assert abs(W.WEBB.mean()) < 1e-12 and abs((W.WEBB ** 2).mean() - 1) < 1e-12


def test_p_valor_determinista_y_valido():
    y, D = _panel()
    p1 = W.wcr_webb(y, D, 0.4, 999, np.random.default_rng(5))[0]
    p2 = W.wcr_webb(y, D, 0.4, 999, np.random.default_rng(5))[0]
    assert p1 == p2 and 0 < p1 <= 1


def test_equivariancia_p():
    y, D = _panel()
    a = W.wcr_webb(y, D, 0.4, 499, np.random.default_rng(7))[0]
    b = W.wcr_webb(y + 0.3 * D, D, 0.7, 499, np.random.default_rng(7))[0]
    assert abs(a - b) < 1e-12


def test_mc_pequeno(tmp_path):
    esc = [{"G": 8, "T": 14, "n_trat": 4, "B": 49, "principal": True}]
    tab = MC.main(R=40, B=49, salida=tmp_path, esc=esc)
    assert len(tab) == 3 and (tmp_path / "resultado.json").exists()
    assert "simulación; sin datos reales" in (tmp_path / "informe.md").read_text(encoding="utf-8")
