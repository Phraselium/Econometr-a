"""Tests rapidos de M8 (regional): funciones sobre datos sinteticos y contrato de las salidas ya escritas."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import m1_factor_comun as m1  # noqa: E402
import m8_regional as m8  # noqa: E402

OUT = RAIZ / "output" / "v8" / "M8"


def test_within_recupera_gamma():
    r = np.random.default_rng(0)
    E, T = 10, 40
    x = r.normal(size=(E, T))
    y = 2.0 * x + r.normal(size=(E, 1)) * 5 + 0.05 * r.normal(size=(E, T))
    g = m8.within_ols(y, [x])
    assert abs(g[0] - 2.0) < 0.05
    C, tot = m8.contribs_panel(y, [x])
    assert C.shape == (E, 1) and tot.shape == (E,)


def test_ols_hac_basico():
    r = np.random.default_rng(1)
    x = r.normal(size=200)
    y = 1 + 3 * x + 0.1 * r.normal(size=200)
    be, ee, r2, _, n = m8.ols_hac(y, np.column_stack([np.ones(200), x]), 4)
    assert abs(be[1] - 3) < 0.05 and r2 > 0.99 and n == 200 and (ee > 0).all()


def test_codigos_ine_cruce():
    p = m1.cargar()
    assert sorted(p["codigo_ine_ccaa"].unique()) == list(range(1, 18))


def test_salidas_contrato():
    if not (OUT / "resultado.json").exists():
        return
    r = json.loads((OUT / "resultado.json").read_text())
    for k in ["rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"]:
        assert k in r
    a = pd.read_csv(OUT / "atribucion.csv")
    assert list(a.columns) == m1.COLS_ATR
    assert set(a["metodo"]) <= {"regional_panel", "regional_ccaa_ols", "contabilidad"}
    amb = set(a["ambito"])
    assert {"cv_prov:03", "cv_prov:12", "cv_prov:46", "valencia_ciudad"} <= amb and sum(x.startswith("ccaa:") for x in amb) == 17
    assert (a["capa"] == "C4").all()
    c = pd.read_csv(OUT / "coeficientes.csv")
    assert list(c.columns) == m1.COLS_COEF
    d = pd.read_csv(OUT / "descriptivo_cv.csv")
    assert set(d["capa"]) <= {"C1", "C4"} and (d.loc[d["capa"] == "C1", "concordantes"]).all()
    assert len(pd.read_csv(OUT / "registro.csv")) > 100
