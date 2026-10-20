"""V18 · SDID con placebos de Conley-Taber (src/v18/herramientas/sdid.py)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herramientas import sdid as S  # noqa: E402


def test_proyeccion_al_simplex():
    rng = np.random.default_rng(1)
    V = rng.normal(0, 2, (7, 12))
    W = S.proyecta_simplex(V)
    assert np.allclose(W.sum(1), 1) and (W >= 0).all()
    mask = rng.random((7, 12)) < 0.6
    mask[:, 0] = True
    Wm = S.proyecta_simplex(V, mask)
    assert np.allclose(Wm.sum(1), 1) and (Wm[~mask] == 0).all() and (Wm >= 0).all()
    # un punto ya en el símplex es fijo
    p = np.array([[0.2, 0.3, 0.5]])
    assert np.allclose(S.proyecta_simplex(p), p)


def _panel(rng, n_tr, n_co, T, g, tau):
    f = rng.normal(0, 1, (2, T))
    lam = rng.normal(0, 1, (n_tr + n_co, 2))
    Y = lam @ f + rng.normal(0, 1, (n_tr + n_co, 1)) + rng.normal(0, 0.05, (n_tr + n_co, T))
    Y[:n_tr, g:] += tau
    return Y


def test_sdid_recupera_el_efecto_con_poco_ruido():
    rng = np.random.default_rng(2)
    n_tr, n_co, T, g = 3, 80, 20, 14
    Y = _panel(rng, n_tr, n_co, T, g, 0.8)
    r = S.sdid(Y[:n_tr, :g], Y[:n_tr, g:], Y[n_tr:, :g], Y[n_tr:, g:])
    assert abs(r["tau"] - 0.8) < 0.35
    assert abs(r["omega"].sum() - 1) < 1e-9 and (r["omega"] >= -1e-12).all()
    assert abs(r["lambda"].sum() - 1) < 1e-9


def test_placebos_forma_y_pvalores():
    rng = np.random.default_rng(3)
    n_tr, n_co, T, g = 4, 60, 16, 10
    Y = _panel(rng, n_tr, n_co, T, g, 0.0)
    r = S.sdid(Y[:n_tr, :g], Y[:n_tr, g:], Y[n_tr:, :g], Y[n_tr:, g:])
    pl = S.placebos(Y[n_tr:, :g], Y[n_tr:, g:], r["lambda"], r["zeta"], n_tr, rng, 99)
    assert pl["sdid"].shape == (99,) and pl["did"].shape == (99,)
    p = S.p_placebo(r["tau"], pl["sdid"], 0.0)
    assert 0 < p <= 1
    assert S.p_placebo(5.0, pl["sdid"], 0.0) == 1 / 100            # efecto enorme: solo la identidad
    assert 0 < S.p_normal_placebo(r["tau"], pl["sdid"], 0.0) <= 1
