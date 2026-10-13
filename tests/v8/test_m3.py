"""Tests rapidos de M3 (salidas ya escritas + LP periodo sintetico)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src"))
import m3_periodos_var as m  # noqa: E402

OUT = RAIZ / "output" / "v8" / "M3"


def test_lp_periodo_sintetico():
    rng = np.random.default_rng(1)
    idx = [f"{a}Q{q}" for a in range(1995, 2027) for q in range(1, 5)]
    S = pd.DataFrame(rng.normal(size=(len(idx), 3)), index=idx, columns=["p", "i", "n"])
    S["covid"] = 0.0
    S["epa2021"] = 0.0
    # pendiente 1 en P1 y 0 en el resto: y_{t+1} = 1*x_t en P1
    D = m.dummies_periodo(S.index)
    S["p"] = (D["P1"] * S["n"]).shift(1).fillna(0) + 0.05 * rng.normal(size=len(idx))
    r = m.lp_periodo(S, ["p", "i", "n"], "n", "p", 1)
    assert r["per"] == m.PERS
    assert abs(r["beta"][0] - 1) < 0.2 and np.all(np.abs(r["beta"][1:]) < 0.5)


def test_bh_monotono():
    p = np.array([0.001, 0.02, 0.5, np.nan])
    a = m.bh(p)
    assert np.isnan(a[3]) and a[0] <= a[1] <= a[2] <= 1


def test_salidas():
    cp = pd.read_csv(OUT / "coef_periodo.csv")
    assert {"variable_origen", "variable_destino", "periodo", "mediana", "b68_lo", "b68_hi", "b90_lo", "b90_hi"} <= set(cp.columns)
    assert set(cp["periodo"]) == set(m.PERS)
    assert (cp["b90_lo"] <= cp["b68_lo"]).all() and (cp["b68_hi"] <= cp["b90_hi"]).all()
    co = pd.read_csv(OUT / "coeficientes.csv")
    assert set(co["familia_modelo"]) == {"lp_periodo", "var_regimenes"} and set(co["capa"]) == {"C4"}
    di = pd.read_csv(OUT / "diferencias_periodos.csv")
    assert di["p_ajustado"].between(0, 1).all() and (di["p_ajustado"] >= di["p"] - 1e-12).all()
    assert len(pd.read_csv(OUT / "registro.csv")) > 0
    assert "P4" in (OUT / "resumen.md").read_text()


def test_ids_registro_y_ficticia():
    co = pd.read_csv(OUT / "coeficientes.csv")
    reg = pd.read_csv(OUT / "registro.csv")
    assert set(co["modelo_id"]) <= set(reg["modelo_id"])        # J17: mismos ids
    assert (OUT / "tiempos.json").exists() and "tiempo" not in (OUT / "resultado.json").read_text()
    S = m.cargar()
    assert S["epa2021"].sum() == 1 and S.loc["2021Q1", "epa2021"] == 1
    for f in ("coeficientes", "coef_periodo", "coef_periodo_h", "diferencias_periodos"):
        d = pd.read_csv(OUT / f"{f}.csv")
        assert d["p"].notna().sum() == d["p_ajustado"].notna().sum()
