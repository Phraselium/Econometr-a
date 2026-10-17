"""V16 · El control BY con denominador fijo coincide con statsmodels y no rechaza pruebas sin p."""
import numpy as np
from statsmodels.stats.multitest import multipletests

from src.v16.f6_fdr import by


def test_by_coincide_con_statsmodels():
    p = {"a": 1e-8, "b": 0.004, "c": 0.03}
    m = 21
    r = by(p, m)
    ref = multipletests(np.array(list(p.values()) + [1.0] * (m - len(p))), alpha=0.10, method="fdr_by")[1][:3]
    assert np.allclose([r[k]["q_BY"] for k in p], ref)
    assert r["a"]["rechaza"] and not r["b"]["rechaza"]
