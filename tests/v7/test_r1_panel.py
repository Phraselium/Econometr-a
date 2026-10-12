"""V7 R1: comprobaciones rápidas de los paneles regionales (leen data/processed/v7)."""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parents[2] / "data" / "processed" / "v7"
TXT = {"codigo_ine_ccaa": str, "cod_prov": str, "cod_ccaa": str}


def _leer(n):
    return pd.read_csv(D / n, dtype=TXT)


def test_ccaa_unico_17_y_codigos():
    p = _leer("panel_ccaa_q_v7.csv")
    assert not p.duplicated(["codigo_ine_ccaa", "trimestre"]).any()
    assert p["codigo_ine_ccaa"].nunique() == 17
    assert p["codigo_ine_ccaa"].str.fullmatch(r"\d{2}").all()
    assert p["trimestre"].min() == "2007Q1" and p["trimestre"].max() == "2026Q2"


def test_prov_unico_52_y_codigos():
    for n, k in [("panel_prov_a_v7.csv", "anio"), ("panel_prov_q_v7.csv", "trimestre")]:
        a = _leer(n)
        assert not a.duplicated(["cod_prov", k]).any()
        assert a["cod_prov"].nunique() == 52
        assert a["cod_prov"].str.fullmatch(r"\d{2}").all()
    a = _leer("panel_prov_a_v7.csv")
    assert a["anio"].min() == 2002 and a["anio"].max() == 2024


def test_hipotecas_provincias_suman_ccaa():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "v7"))
    from r1_panel import PROV_A_CCAA

    pq = _leer("panel_prov_q_v7.csv")
    p = _leer("panel_ccaa_q_v7.csv")
    for t in ("2012Q3", "2019Q4"):
        x = pq[pq["trimestre"] == t].copy()
        x["cod_ccaa"] = x["cod_prov"].map(PROV_A_CCAA)
        s = x[x["cod_ccaa"].isin(p["codigo_ine_ccaa"].unique())].groupby("cod_ccaa")["hip_n"].sum()
        c = p[p["trimestre"] == t].set_index("codigo_ine_ccaa")["hip_n"]
        assert (s.reindex(c.index) - c).abs().max() < 1e-6
