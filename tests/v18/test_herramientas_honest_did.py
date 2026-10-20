"""V18 · Honest DiD (magnitudes relativas) sobre el contraste condicional de V9 (src/v18/herr18/honest_did.py)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herr18 import honest_did as H  # noqa: E402


def test_covarianza_agrupada_rango_y_simetria():
    rng = np.random.default_rng(1)
    n, T = 60, 9
    Y = rng.normal(0, 1, (n, T))
    tr = np.arange(n) < 20
    cl = np.arange(n) % 6                      # 6 clusters
    b, V, info = H.evento_agrupado(Y, tr, cl, 4, [0, 1, 2, 3], [5, 6, 7, 8])
    assert b.shape == (8,) and V.shape == (8, 8)
    assert np.allclose(V, V.T) and info["G"] == 6 and info["rango_V"] <= 5     # rango <= G − 1
    b2, V2, info2 = H.evento_agrupado(Y, tr, np.arange(n), 4, [0, 1, 2, 3], [5, 6, 7, 8])
    assert info2["rango_V"] == 8


def test_m0_rechaza_lejos_y_no_rechaza_la_verdad():
    n_pre, n_post = 4, 5
    V = np.eye(n_pre + n_post) * 0.01 ** 2
    tau = 0.10
    b = np.r_[np.zeros(n_pre), tau * np.ones(n_post)]          # sin sesgo: el efecto es 0,10 en todos los posteriores
    assert H.contrasta(b, V, n_pre, n_post, 0.0, 0.0)           # θ0 = 0 está lejos
    assert not H.contrasta(b, V, n_pre, n_post, 0.0, tau)       # θ0 = verdad: no rechaza


def test_m_mayor_ensancha_el_conjunto():
    n_pre, n_post = 4, 4
    V = np.eye(n_pre + n_post) * 0.005 ** 2
    b = np.r_[[-0.03, -0.02, -0.01, 0.0], [0.05, 0.06, 0.07, 0.08]]      # tendencia previa de 0,01 por periodo
    lo0, hi0 = H.ic(b, V, n_pre, n_post, 0.0)
    lo1, hi1 = H.ic(b, V, n_pre, n_post, 1.0)
    assert (hi1 - lo1) > (hi0 - lo0) > 0
    assert lo1 < lo0 < hi0 < hi1 + 1e-9
