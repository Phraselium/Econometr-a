"""V18 · Metaanálisis bayesiano por cuadratura (src/v18/herr18/meta_bayes.py): contra integración bruta y propiedades."""
import sys
from pathlib import Path

import numpy as np
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herr18 import meta_bayes as H  # noqa: E402


def _bruto(y, se, s0, s_tau, mu_grid=np.linspace(-4, 4, 1601), tau_grid=np.linspace(1e-4, 4, 1601)):
    """Posterior por rejilla 2D de (μ, τ) con prior semi-normal de τ; devuelve mediana e intervalo de μ y de τ."""
    MU, TAU = np.meshgrid(mu_grid, tau_grid, indexing="ij")
    ll = np.zeros_like(MU)
    for yk, sk in zip(y, se):
        ll += stats.norm.logpdf(yk, MU, np.sqrt(sk ** 2 + TAU ** 2))
    lp = ll + stats.norm.logpdf(MU, 0, s0) + stats.halfnorm.logpdf(TAU, scale=s_tau)
    w = np.exp(lp - lp.max())
    w /= w.sum()
    pm = w.sum(1)
    pt = w.sum(0)
    q = lambda p, g, a: g[np.searchsorted(np.cumsum(p), a)]
    return [q(pm, mu_grid, a) for a in (0.025, 0.5, 0.975)], [q(pt, tau_grid, a) for a in (0.025, 0.5, 0.975)]


def test_posterior_coincide_con_la_integracion_bruta():
    y = np.array([[-0.3, 0.1, -0.5, 0.2]])
    se = np.array([[0.2, 0.15, 0.3, 0.25]])
    r = H.posterior(y, se, 1.0, 1.0, "seminormal")
    mu, tau = _bruto(y[0], se[0], 1.0, 0.5)
    assert np.allclose([r["mu_lo"][0], r["mu_med"][0], r["mu_hi"][0]], mu, atol=0.02)
    assert np.allclose([r["tau_lo"][0], r["tau_med"][0], r["tau_hi"][0]], tau, atol=0.03)


def test_variantes_de_prior_ordenan_la_contraccion():
    y = np.array([[0.9, 1.1, 0.8]])
    se = np.array([[0.3, 0.3, 0.3]])
    med = {c: H.posterior(y, se, 1.0, c)["mu_med"][0] for c in (0.5, 1.0, 2.0)}
    assert med[0.5] < med[1.0] < med[2.0] < y.mean()           # prior más estrecho: más cerca de 0
    r = H.posterior(y, se, 1.0, 1.0, "semicauchy")
    assert r["mu_lo"][0] < r["mu_med"][0] < r["mu_hi"][0]


def test_efecto_fijo_es_la_media_ponderada():
    y = np.array([[1.0, 3.0]])
    se = np.array([[1.0, 2.0]])
    e = H.efecto_fijo(y, se)
    w = np.array([1.0, 0.25])
    assert abs(e["mu_med"][0] - (w * y[0]).sum() / w.sum()) < 1e-12
    assert abs((e["mu_hi"][0] - e["mu_lo"][0]) - 2 * 1.959964 / np.sqrt(w.sum())) < 1e-6


def test_calibracion_con_verdad_sorteada_del_prior():
    rng = np.random.default_rng(7)
    R, K = 600, 5
    mu = rng.normal(0, 1, R)
    tau = np.abs(rng.normal(0, 0.5, R))
    se = np.exp(rng.uniform(np.log(0.05), np.log(0.4), (R, K)))
    y = mu[:, None] + tau[:, None] * rng.standard_normal((R, K)) + se * rng.standard_normal((R, K))
    r = H.posterior(y, se, 1.0, 1.0, "seminormal")
    cov_mu = np.mean((r["mu_lo"] <= mu) & (mu <= r["mu_hi"]))
    cov_tau = np.mean((r["tau_lo"] <= tau) & (tau <= r["tau_hi"]))
    assert 0.92 <= cov_mu <= 0.99 and 0.92 <= cov_tau <= 0.99
