"""Tests rapidos de src/v7/panel_tools.py con Monte Carlo reducido (N=17, T=78; solo datos simulados)."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v7"))
import panel_tools as pt  # noqa: E402
import r2_montecarlo as mc  # noqa: E402

R = 12


def _panel(r, scen="A_coint_sin_factor"):
    c, f, h = mc.SCEN[scen]
    return mc.simulate(np.random.default_rng([pt.SEED, r, 99]), c, f, h)


def test_mg_pmg_recuperan_theta():
    est = {"MG": [], "PMG": []}
    for r in range(R):
        y, X, *_ = _panel(r)
        est["MG"].append(pt.mg(y, X)["theta"])
        est["PMG"].append(pt.pmg(y, X)["theta"])
    for m, v in est.items():
        assert np.allclose(np.mean(v, 0), mc.TH, atol=0.08), (m, np.mean(v, 0))


def test_dfe_cs_ejecutan():
    y, X, *_ = _panel(0)
    assert np.allclose(pt.dfe(y, X)["theta"], mc.TH, atol=0.3)
    cs = pt.cs_ardl(y, X)
    assert cs["theta"].shape == (2,) and np.all(np.isfinite(cs["se_theta"]))


def test_hausman_no_rechaza_en_exceso():
    rej = 0
    for r in range(R):
        y, X, *_ = _panel(r)
        rej += pt.hausman_mg_pmg(pt.mg(y, X), pt.pmg(y, X))["p"] < 0.05
    assert rej / R <= 0.35


def test_westerlund_rechaza_con_cointegracion_y_no_sin_ella():
    y, X, *_ = _panel(1)
    w = pt.westerlund(y, X, 1, B=49)
    assert w["p"]["Gt"] < 0.05 and w["p"]["Pt"] < 0.05
    y0, X0, *_ = _panel(1, "C_sin_coint_sin_factor")
    assert pt.westerlund(y0, X0, 1, B=49)["p"]["Gt"] > 0.05


def test_cips_no_rechaza_raiz_unitaria_y_si_estacionaria():
    sim = pt.cips_critical_values(mc.N, mc.T, 1, reps=200)["sim"]
    rej = 0
    for r in range(R):
        y, X, ys, *_ = _panel(r, "C_sin_coint_sin_factor")
        rej += pt.sim_pvalue(pt.cips(y), sim) < 0.05
    assert rej / R <= 0.30
    _, _, ys, *_ = _panel(0)
    assert pt.sim_pvalue(pt.cips(ys), sim) < 0.05


def test_pedroni():
    sim = pt.pedroni_null(mc.N, mc.T, 2, 1, reps=100)
    y, X, *_ = _panel(2)
    assert pt.pedroni(y, X, 1, sim=sim)["p"]["group_adf"] < 0.05


def test_pocos_clusters():
    rng = np.random.default_rng(pt.SEED)
    G, n = 17, 20
    cl = np.repeat(np.arange(G), n)
    x = rng.standard_normal(G * n) + rng.standard_normal(G)[cl]
    y = 0.0 * x + rng.standard_normal(G)[cl] + rng.standard_normal(G * n)
    w = pt.wild_cluster_boot(y, x[:, None], cl, 0, B=199)
    assert 0 <= w["p_boot"] <= 1
    y2 = 1.0 * x + rng.standard_normal(G * n)
    assert pt.wild_cluster_boot(y2, x[:, None], cl, 0, B=199)["p_boot"] < 0.05
    dk = pt.driscoll_kraay(rng.standard_normal(17 * 40), rng.standard_normal((17 * 40, 1)), 17, 40)
    assert np.isfinite(dk["se"]).all()


def test_pmg_bootstrap_cs_dl_demean():
    y, X, *_ = _panel(3)
    b = pt.pmg_bootstrap(y, X, B=9)
    assert b["se_theta"].shape == (2,) and np.all(b["se_theta"] > 0)
    assert np.all(np.isfinite(pt.cs_dl(y, X)["theta"]))
    yd, Xd = pt.cs_demean(y, X)
    assert abs(yd.mean(0)).max() < 1e-9
    assert np.allclose(pt.pmg(y, X)["theta"], mc.TH, atol=0.15)
