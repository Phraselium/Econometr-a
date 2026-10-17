"""Pruebas rápidas de Q6 (grupo B): Wald-DID de dCDH con efecto conocido y forma de los resultados."""
import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16"))
sys.path.insert(0, str(RAIZ / "src"))
import q6_itp as Q  # noqa: E402

OUT = RAIZ / "output" / "v16" / "q6"


def _panel(efecto):
    filas = []
    for u, c in [("a", 1), ("b", 1), ("c", 2), ("d", 2), ("e", 3), ("f", 3)]:
        for t in range(2011, 2021):
            filas.append((u, c, t))
    d = pd.DataFrame(filas, columns=["u", "c", "t"])
    d["dd"] = 0.0
    d.loc[(d.c == 1) & (d.t == 2015), "dd"] = 2.0
    d.loc[(d.c == 2) & (d.t == 2018), "dd"] = -1.0
    d["dd_f"] = d.groupby("u").dd.shift(-1)
    d["dy"] = 0.01 + efecto * d.dd
    return d


def test_wald_did_recupera_el_efecto():
    for e in (-0.07, 0.03):
        w = Q.wald_did(_panel(e))
        assert abs(w["beta"] - e) < 1e-12 and w["n_provincias_switchers"] == 4


def test_anticipacion_excluye_estables_que_cambian_al_año_siguiente():
    d = _panel(-0.05)
    d.loc[(d.c == 3) & (d.t == 2016), "dd"] = 1.0  # las estables de 2015 con cambio en 2016 no son control en 2015
    d["dd_f"] = d.groupby("u").dd.shift(-1)
    d["dy"] = 0.01 - 0.05 * d.dd
    w = Q.wald_did(d)
    assert abs(w["beta"] + 0.05) < 1e-12


def test_calendario_itp():
    T = Q.tipos(0)
    assert set(T.c.unique()) == set(Q.CCAA_OK)
    T["dd"] = T.groupby("c").d.diff()
    assert int(((T.dd.fillna(0) != 0) & (T.t >= 2011)).sum()) == 14


def test_resultado_q6_solo_puntual():
    r = json.loads((OUT / "resultado.json").read_text(encoding="utf-8"))
    assert r["capa"] == "C4" and r["pendiente_sellada"] is True and r["ic95"] is None and r["p_ajustado"] is None
    assert all(x["p"] is None for x in r["p_valores_para_BY"])
    assert r["estimacion"]["Q6-v"]["multiverso"]["n"] == 8
    h = json.loads((OUT / "hechos.json").read_text(encoding="utf-8"))
    assert 0 < len(h) <= 10 and all(x["id"].startswith("V16-Q6") for x in h)
    assert "honest_did" in r["diagnosticos"]["Q6-v"]
