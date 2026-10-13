"""Tests rapidos de M1 (factor comun): funciones sobre datos sinteticos y contrato de las salidas ya escritas."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import m1_factor_comun as m1  # noqa: E402

OUT = RAIZ / "output" / "v8" / "M1"


def sintetico(T=60, N=17, peso=1.0, seed=1):
    r = np.random.default_rng(seed)
    f = r.normal(size=T)
    return peso * f[:, None] + r.normal(size=(T, N)), f


def test_cuota_sube_con_factor():
    X1, _ = sintetico(peso=2.0)
    X0, _ = sintetico(peso=0.0)
    assert m1.cuota_pca(X1) > 0.5 > m1.cuota_pca(X0) - 0.2
    assert m1.cuota_pca(X1) > m1.cuota_pca(X0)


def test_bloques_y_p():
    rng = np.random.default_rng(0)
    ix = m1.idx_bloques(30, 4, rng)
    assert len(ix) == 30 and ix.min() >= 0 and ix.max() < 30
    assert m1.p_unilat_mayor(np.ones(99), 0.0) == 1 / 100


def test_correlacion_bootstrap_detecta_factor():
    X, f = sintetico(T=80, peso=1.5)
    r0, bs = m1.corr_boot(X, f + 0.3 * np.random.default_rng(2).normal(size=80), 4, 99, np.random.default_rng(3))
    assert r0 > 0.8 and m1.p_unilat_mayor(bs, 0.0) < 0.05


def test_salidas_contrato():
    if not (OUT / "resultado.json").exists():
        return
    r = json.loads((OUT / "resultado.json").read_text())
    for k in ["rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"]:
        assert k in r
    h = pd.read_csv(OUT / "hipotesis_m1.csv")
    assert list(h["id"]) == ["H8-8", "H8-9"] and (h["p_holm"] >= h["p"] - 1e-12).all() and (h["capa"] == "C4").all()
    a = pd.read_csv(OUT / "atribucion.csv")
    assert list(a.columns) == m1.COLS_ATR
    assert set(a["metodo"]) == {"factor_comun"} and "factor_europeo" in set(a["factor"])
    assert (a["b90_lo"] <= a["b68_lo"] + 1e-9).all() or a["b90_lo"].isna().any()
    c = pd.read_csv(OUT / "coeficientes.csv")
    assert list(c.columns) == m1.COLS_COEF
    assert len(pd.read_csv(OUT / "registro.csv")) > 20
