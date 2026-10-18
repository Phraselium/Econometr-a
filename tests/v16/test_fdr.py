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


def test_q_de_q9g_citable_es_el_vigente():
    """La cifra citable V16-FDR-Q9-g-q es el q que da hoy el control BY sobre los p vigentes (decisión K18), no un valor anterior."""
    import json
    from pathlib import Path

    from src.v16.f6_fdr import M, by, recoger
    raiz = Path(__file__).resolve().parents[2]
    h = {x["id"]: x for x in json.loads((raiz / "output/v16/fdr/hechos.json").read_text(encoding="utf-8"))}
    q = by(recoger()["con_p"]["diseños"], M["diseños"])["Q9-g"]["q_BY"]
    assert abs(h["V16-FDR-Q9-g-q"]["valor"] - q) < 1e-12
    for f in raiz.glob("output/v16/*/hechos.json"):
        assert "0.153" not in f.read_text(encoding="utf-8"), f  # el q previo a K16 no puede quedar como cifra citable
