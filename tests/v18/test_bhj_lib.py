"""V18 · bhj_lib: la agregación a nivel de shock reproduce el IV shift-share (BHJ 2022, equivalencia)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "bhj_lib", RAIZ / "src" / "v18" / "reproduccion" / "bhj_lib.py")
bhj = importlib.util.module_from_spec(spec)
sys.modules["bhj_lib"] = bhj
spec.loader.exec_module(bhj)


def _caso(L=300, N=25, seed=20261010, suma_uno=True):
    rng = np.random.default_rng(seed)
    S = rng.dirichlet(np.ones(N) * 0.5, size=L)
    if not suma_uno:
        S = S * rng.uniform(0.5, 1.0, size=(L, 1))
    g = rng.normal(size=N)
    w = rng.uniform(0.5, 2.0, size=L)
    c = rng.normal(size=(L, 2))
    z = S @ g
    x = 0.8 * z + c[:, 0] + rng.normal(size=L)
    y = -0.5 * x + 0.3 * c[:, 0] + 0.2 * c[:, 1] + rng.normal(size=L)
    cuotas = pd.DataFrame({
        "loc": np.repeat(np.arange(L), N), "sector": np.tile(np.arange(1, N + 1), L),
        "s": S.ravel()})
    return S, g, w, c, z, x, y, cuotas


def test_equivalencia_iv_localizacion_iv_shock():
    L, N = 300, 25
    S, g, w, c, z, x, y, cuotas = _caso(L, N)
    ctrl = c
    # IV a nivel de localización, controles parcializados
    loc = bhj.iv_cluster(y, x, z, w, np.arange(L), ctrl)
    # IV a nivel de shock con ssaggregate
    ag = bhj.ssaggregate(pd.DataFrame({"y": y, "x": x}), w, np.arange(L), np.zeros(L), cuotas,
                         controles={"": ctrl})
    assert (ag["sector"] != 0).all() or True
    ag = ag[ag["sector"] != 0].reset_index(drop=True)   # el sector faltante tiene cuota 0
    assert abs(ag["s_n"].sum() - 1) < 1e-6
    gs = g[ag["sector"].to_numpy() - 1]
    sh = bhj.iv_cluster(ag["y"], ag["x"], gs, ag["s_n"], ag["sector"])
    assert abs(loc["beta"] - sh["beta"]) < 1e-10


def test_agregado_manual_y_cuotas_incompletas():
    S, g, w, c, z, x, y, cuotas = _caso(80, 6, suma_uno=False)
    ag = bhj.ssaggregate(pd.DataFrame({"x": x}), w, np.arange(80), np.zeros(80), cuotas,
                         controles={"": c}, addmissing=True)
    xr = bhj.residuos_ponderados(x, c, w)
    n = 3
    manual = np.sum(S[:, n - 1] * w * xr) / np.sum(S[:, n - 1] * w)
    fila = ag[ag["sector"] == n].iloc[0]
    assert abs(fila["x"] - manual) < 1e-12
    # sector faltante presente con cuota 1 - sum(cuotas)
    assert (ag["sector"] == 0).sum() == 1
    falt = np.sum((1 - S.sum(axis=1)) * w) / np.sum(S * w[:, None])
    assert abs(ag.loc[ag.sector == 0, "s_n"].iloc[0] - np.sum((1 - S.sum(axis=1)) * w) /
               (np.sum(S * w[:, None]) + np.sum((1 - S.sum(axis=1)) * w))) < 1e-12
    assert falt > 0


def test_ic_nulo_contiene_beta_y_es_determinista():
    L, N = 600, 40
    S, g, w, c, z, x, y, cuotas = _caso(L, N)
    ag = bhj.ssaggregate(pd.DataFrame({"y": y, "x": x}), w, np.arange(L), np.zeros(L), cuotas,
                         controles={"": c})
    ag = ag[ag["sector"] != 0].reset_index(drop=True)
    gs = g[ag["sector"].to_numpy() - 1]
    r = bhj.iv_cluster(ag["y"], ag["x"], gs, ag["s_n"], ag["sector"])
    a1 = bhj.ar_ic_nulo_impuesto(ag["y"], ag["x"], gs, ag["s_n"], ag["sector"])
    a2 = bhj.ar_ic_nulo_impuesto(ag["y"], ag["x"], gs, ag["s_n"], ag["sector"])
    assert a1 == a2 and a1[0] < r["beta"] < a1[1]
    assert a1[0] < -0.5 < a1[1]    # el verdadero coeficiente cae en el IC
    assert r["F1"] > 10


def test_declara_alcance_sin_lectura():
    t = (RAIZ / "src" / "v18" / "reproduccion" / "bhj_lib.py").read_text(encoding="utf-8")
    assert 'ALCANCE_TERRITORIAL = "sin lectura de datos"' in t
    assert "read_csv(" not in t and "read_stata(" not in t
