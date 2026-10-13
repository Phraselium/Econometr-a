"""Tests rapidos de M5 (IV1 JK, IV2 migratorio, IV3 Bartik): helpers sobre datos sinteticos y salidas ya escritas."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
_spec = importlib.util.spec_from_file_location("m5_lpiv", RAIZ / "src" / "v8" / "m5_lpiv.py")
m5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m5)
OUT = RAIZ / "output" / "v8" / "M5"


def test_bh_y_ar_ext():
    p = m5.bh({"a": 0.01, "b": 0.04, "c": 0.5})
    assert p["a"] <= p["b"] <= p["c"] and p["a"] == pytest.approx(0.03)
    assert m5.ar_ext(-5000.0, 5000.0, False, 0.0, 1.0) == (-np.inf, np.inf)
    assert m5.ar_ext(-1.0, 2.0, True, 0.5, 1.0) == (-1.0, 2.0)


def test_evalua_c3_exige_los_cuatro():
    ok = m5.evalua_c3(15.0, 0.5, 2.0, True, [0.3, 0.4], 0.01)
    assert ok["cumple_c3"] and ok["c3_laxo"]
    assert not m5.evalua_c3(5.0, 0.5, 2.0, True, [0.3], 0.01)["cumple_c3"]       # F < 10
    assert not m5.evalua_c3(15.0, -0.5, 2.0, True, [0.3], 0.01)["cumple_c3"]     # AR incluye 0
    assert not m5.evalua_c3(15.0, 0.5, 2.0, True, [0.01], 0.01)["cumple_c3"]     # pretendencia significativa
    assert not m5.evalua_c3(15.0, 0.5, 2.0, True, [0.3], 0.5)["cumple_c3"]       # placebo
    assert m5.evalua_c3(5.0, 0.5, 2.0, True, [0.3], 0.01)["c3_laxo"]


def test_bartik_leave_one_out_sintetico():
    filas = []
    rng = np.random.default_rng(1)
    for g in m5.NUTS_TODOS + ["ES"]:
        for s in m5.SECTORES + ["TOTAL"]:
            for a in (2008, 2009, 2010):
                filas.append((g, s, a, 100.0 + rng.normal() + (a - 2008) * 3 if s != "TOTAL" else 1000.0))
    sec = pd.DataFrame(filas, columns=["geo", "nace_r2", "anio", "valor"])
    B, Bs, cuotas, tot = m5.construye_bartik(sec)
    assert B.shape[0] == 17 and np.allclose(cuotas.sum(axis=1), 1.0)
    assert np.isnan(B[2008]).all() and np.isfinite(B[2009]).all()
    # leave-one-out: cambiar el empleo de una region en un sector no altera su propio Bartik
    sec2 = sec.copy()
    sec2.loc[(sec2.geo == "ES30") & (sec2.nace_r2 == "F") & (sec2.anio == 2010), "valor"] *= 3
    B2, *_ = m5.construye_bartik(sec2)
    assert B2.loc["ES30", 2010] == pytest.approx(B.loc["ES30", 2010]) or abs(B2.loc["ES30", 2010] - B.loc["ES30", 2010]) < 1e-9
    assert abs(B2.loc["ES11", 2010] - B.loc["ES11", 2010]) > 1e-6


def test_panel_iv_coincide_con_ajuste_directo_y_lp_panel():
    from herramientas import lp as LP
    rng = np.random.default_rng(3)
    N, T = 12, 14
    ent = np.repeat(np.arange(N), T)
    t = np.tile(np.arange(T), N)
    z = rng.normal(size=N * T)
    x = 0.9 * z + rng.normal(size=N * T)
    y = 0.5 * x + rng.normal(size=N * T)
    d = pd.DataFrame({"ent": ent, "t": t, "y": y, "x": x, "z": z})
    r = m5.panel_iv(d, "y", 1, 2, grid_n=801)
    assert r["F_robusto"] > 10 and r["beta"] == pytest.approx(0.5, abs=0.5)
    # reducida en b0 = 0 igual que lp_panel (misma especificacion con rezago 1 y efectos de tiempo)
    ref = LP.lp_panel(d.rename(columns={"z": "zz"}).assign(z=d["z"]), "y", "z", "ent", "t", H=1, rezagos=1, efectos_tiempo=True)
    assert r["pi_y"] == pytest.approx(ref.loc[ref.h == 1, "beta"].iloc[0], rel=1e-6, abs=1e-6)
    # varianza cuadratica en b0: contraste con un ajuste directo en b0 = 0,5
    dd = m5._diseno(d, "y", 1)
    dd["w"] = dd["dep"] - 0.5 * dd["x"]
    b, se, _ = m5._ajusta(dd, "w", ["z", "yl", "xl", "zl"], 2)
    assert b == pytest.approx(r["pi_y"] - 0.5 * r["pi_x"], rel=1e-6, abs=1e-8)
    # el beta verdadero (0,5) cae en el conjunto AR 95
    assert r["ar_lo95"] <= 0.5 * 2 and r["ar_hi95"] >= 0.0


def test_iv2_construccion_sintetica():
    anios = list(range(2002, 2008))
    filas = []
    for g in ["DE", "FR"]:
        for c in ["TOTAL", "MA", "RO"]:
            for a in anios:
                filas.append((g, c, a, 1000.0 + 100 * (a - 2002) + (50 if c == "RO" else 0)))
    imm = pd.DataFrame(filas, columns=["geo", "citizen", "anio", "valor"])
    pop = pd.DataFrame({"citizen": ["MA", "RO", "ES", "EUR"], "valor": [30000.0, 10000.0, 1e6, 1e6]})
    Z, tab, dest = m5.construye_iv2(imm, pop, pd.Series(dtype=float), anio1=2007)
    assert dest == ["DE", "FR"] and set(tab["origen"]) == {"MA", "RO"}
    assert tab["cuota_2002"].sum() == pytest.approx(1.0)
    assert np.isnan(Z.loc[2002]) and Z.loc[2005] > 0


@pytest.mark.skipif(not (OUT / "resultado.json").exists(), reason="requiere ejecutar m5_lpiv.py")
def test_salidas_contrato():
    coef = pd.read_csv(OUT / "coeficientes.csv")
    assert {"f1_etapa", "ar_lo", "ar_hi", "modelo_id", "capa"} <= set(coef.columns)
    assert list(coef.columns)[:9] == ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio"]
    assert set(coef["capa"]) <= {"C1", "C2", "C3", "C3s", "C4"}
    atr = pd.read_csv(OUT / "atribucion.csv")
    assert list(atr.columns) == m5.COLS_ATR and set(atr["metodo"]) == {"lpiv"}
    assert set(atr["factor"]) <= {"credito_tipos", "demografia", "empleo_renta"}
    hip = pd.read_csv(OUT / "hipotesis_m5.csv")
    assert list(hip["id"]) == ["H8-5", "H8-6", "H8-7"]
    # Holm sobre la familia de tres
    esperado = m5.holm(dict(zip(hip["id"], hip["ar_p"].fillna(1.0))))
    assert np.allclose(hip["p_holm"], [esperado[i] for i in hip["id"]])
    # sin C3 no hay lectura causal
    for _, h in hip.iterrows():
        if not h["cumple_c3"]:
            assert str(h["capa"]).startswith("C4") and "causal" not in str(h["lectura"]).replace("sin lectura causal", "")
    res = json.loads((OUT / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in res
    reg = pd.read_csv(OUT / "registro.csv")
    assert len(reg) >= len(coef) - 12 and (OUT / "resumen.md").exists()
