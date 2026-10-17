"""V15-A · H1/H2: recuento de la adenda, recuperación de un efecto conocido (CS, SDID, PPML) y forma de las salidas."""
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v15"))
sys.path.insert(0, str(RAIZ / "src"))
import pa_did as D  # noqa: E402


def test_recuento_adenda():
    P = D.construir_panel()
    c = P["coh"]
    assert len(c) == 308
    assert (c != "nunca").sum() == 234 and (c == "nunca").sum() == 74
    assert (c == D.G1).sum() == 127 and (c == D.G4).sum() == 107


def _sintetico(tau=-0.08, seed=20261010):
    rng = np.random.default_rng(seed)
    n, T = 300, len(D.QUARTERS)
    coh = np.array(["nunca"] * 100 + [D.G1] * 100 + [D.G4] * 100, dtype=object)
    Y = rng.normal(0, 0.02, (n, T)) + rng.normal(0, 0.2, (n, 1)) + np.linspace(0, 0.1, T)
    q = {p: i for i, p in enumerate(D.QUARTERS)}
    for u in range(n):
        if coh[u] == D.G1:
            Y[u, q["2024T2"]:] += tau
        if coh[u] == D.G4:
            Y[u, q["2024T4"]:] += tau
    return Y, coh


def test_cs_sdid_recuperan_efecto():
    Y, coh = _sintetico()
    cs = D.cs_agregar(D.cs_celdas(Y, coh, D.QUARTERS, "2026T1"))
    sd = D.sdid_cohortes(Y, coh, D.QUARTERS, "2026T1")["att"]
    assert abs(cs - (-0.08)) < 0.01 and abs(sd - (-0.08)) < 0.02


def test_ppml_recupera_efecto():
    rng = np.random.default_rng(20261010)
    Y, coh = _sintetico(tau=np.log(0.9))
    N = np.exp(Y + 2) * rng.uniform(0.95, 1.05, Y.shape)
    r = D.ppml(N, coh, D.QUARTERS, "2026T1")
    assert abs(r["att_pct"] - (-10.0)) < 2.0 and r["convergio"]


def test_salidas_forma():
    ruta = RAIZ / "output" / "v15" / "p6" / "resultado.json"
    if not ruta.exists():
        return
    r = json.loads(ruta.read_text(encoding="utf-8"))
    for h in ("H1", "H2"):
        assert r[h]["capa"] == "C4" and r[h]["pendiente_sellada"] is True
        assert r[h]["p_ajustado"] is None and r[h]["ic95"] is None
        assert r[h]["p_valores_para_BY"][0]["p"] is None
    hechos = json.loads((RAIZ / "output" / "v15" / "p6" / "hechos.json").read_text(encoding="utf-8"))
    assert len(hechos) <= 20 and all(x["id"].startswith("V15-H") for x in hechos)
