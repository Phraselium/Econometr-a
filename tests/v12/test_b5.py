"""V12-B5: cuotas de titularidad coherentes y ficha del verificador sin lenguaje causal en el veredicto."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

B5 = Path(__file__).resolve().parents[2] / "output/v12/b5"


def test_cuotas_coherentes():
    if not (B5 / "titularidad_cuotas.csv").exists():
        pytest.skip("ejecutar `make v12`")
    t = pd.read_csv(B5 / "titularidad_cuotas.csv", dtype={"cod_territorio": str})
    v = t[t.viviendas > 0]
    assert ((v.pct_mas100 <= v.pct_mas10 + 1e-9) & (v.pct_mas10 <= v.pct_mas5 + 1e-9)).all()
    assert ((v.pct_PJ + v.pct_PE + v.pct_PF) <= 100 + 1e-6).all()
    n = t[t.nivel == "nacional"].set_index("anio")
    m = t[t.nivel == "municipio"].groupby("anio").viv_mas100.sum()
    assert (m.reindex(n.index) <= n.viv_mas100).all()   # tramos dentro del ámbito: la suma municipal es menor


def test_ficha_v02():
    p = B5 / "fichas_verificador_v12.json"
    if not p.exists():
        pytest.skip("ejecutar `make v12`")
    f = json.loads(p.read_text(encoding="utf-8"))[0]
    assert f["sustituye"] == "V02" and f["capa"] == "C4" and f["veredicto"] == "ANALIZADA, NO CONCLUYENTE"
