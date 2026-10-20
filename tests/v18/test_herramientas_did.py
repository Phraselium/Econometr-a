"""V18 · Callaway-Sant'Anna y Sun-Abraham con wild cluster bootstrap de Webb (src/v18/herramientas/did.py)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herramientas.did import CallawaySantAnna, SunAbraham  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402


def _panel_exacto(coh, T, rng):
    n = len(coh)
    a = rng.normal(0, 1, n)[:, None]
    g = rng.normal(0, 1, T)[None, :]
    efecto = np.zeros((n, T))
    for gg in set(coh[coh >= 0].tolist()):
        m = coh == gg
        het = rng.normal(0.05, 0.02, m.sum())
        efecto[m, gg:] = het[:, None] * (1 - np.exp(-(np.arange(T - gg) + 1) / 2))[None, :]
    return a + g + efecto, efecto


def test_sin_ruido_recupera_el_agregado_verdadero():
    rng = np.random.default_rng(1)
    coh = np.array([5] * 10 + [8] * 6 + [-1] * 24)
    cl = np.arange(len(coh))
    Y, e = _panel_exacto(coh, 12, rng)
    cs, sa = CallawaySantAnna(coh, cl, 12), SunAbraham(coh, cl, 12)
    assert abs(cs.estimar(Y) - cs.verdad(e)) < 1e-10
    assert abs(sa.estimar(Y) - sa.verdad(e)) < 1e-10


def test_una_cohorte_cs_y_sa_coinciden_en_la_estimacion_puntual():
    rng = np.random.default_rng(2)
    coh = np.array([6] * 12 + [-1] * 30)
    cl = np.arange(len(coh))
    Y = rng.normal(0, 1, (len(coh), 10)) + rng.normal(0, 1, (len(coh), 1))
    cs, sa = CallawaySantAnna(coh, cl, 10), SunAbraham(coh, cl, 10)
    assert abs(cs.estimar(Y) - sa.estimar(Y)) < 1e-9


def test_pvalor_en_rango_y_rechaza_un_efecto_grande():
    rng = np.random.default_rng(3)
    coh = np.array([6] * 20 + [-1] * 40)
    cl = np.arange(len(coh))
    Y = rng.normal(0, 0.1, (len(coh), 10)) + rng.normal(0, 1, (len(coh), 1))
    Y[:20, 6:] += 1.0
    for est in (CallawaySantAnna(coh, cl, 10), SunAbraham(coh, cl, 10)):
        p, att, se = est.p_valor(Y, 0.0, rng, 199)
        assert 0 < p <= 1 and p < 0.05
        assert abs(att - 1.0) < 0.2 and se > 0
        p_v, _, _ = est.p_valor(Y, att, rng, 199)     # contrastar la propia estimación: no rechaza
        assert p_v > 0.5


def test_tamano_cercano_al_nominal_con_clusters_independientes():
    rng = np.random.default_rng(4)
    coh = np.array([5] * 25 + [-1] * 50)
    cl = np.arange(len(coh))
    cs = CallawaySantAnna(coh, cl, 9)
    rej = 0
    R = 300
    for _ in range(R):
        Y = rng.normal(0, 1, (len(coh), 9)) * 0.3 + rng.normal(0, 1, (len(coh), 1))
        rej += cs.p_valor(Y, 0.0, rng, 199)[0] <= 0.05
    assert 0.02 <= rej / R <= 0.10


def test_diseno_declarado_dimensiones():
    d = D.diseno("cat_trim_M")
    assert (d.cohorte >= 0).sum() == 100 and (d.cohorte < 0).sum() == 200 and d.T == 13
    d = D.diseno("zt2024_2cohortes")
    assert sorted(set(d.cohorte[d.cohorte >= 0].tolist())) == [9, 13] and d.T == 17
    d = D.diseno("itp_8ccaa")
    assert len(d.cohorte) == 36 and len(np.unique(d.cl_fino)) == 8 and (d.cohorte < 0).sum() == 10
    Y, e = D.simular(d, np.random.default_rng(5), 0.05)
    assert Y.shape == (36, 24) and e.shape == (36, 24) and (e[d.cohorte < 0] == 0).all()
