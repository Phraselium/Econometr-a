"""Tests mínimos del grupo «panel» del Monte Carlo V16: determinismo con la semilla (R pequeño) y veredicto con los umbrales de la adenda."""
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16" / "montecarlo"))
pytest.importorskip("joblib")
ENTR = RAIZ / "data" / "processed" / "v16" / "entrenamiento" / "base_alquiler.parquet"
pytestmark = pytest.mark.skipif(not ENTR.exists(), reason="faltan los datos procesados de V16 (solo estructura)")

import _comun_panel as C  # noqa: E402


def test_semilla_fija_y_flujos_reproducibles():
    assert C.SEMILLA == 20261010
    a = [r.standard_normal(3) for r in C.flujos(7, 4)]
    b = [r.standard_normal(3) for r in C.flujos(7, 4)]
    assert all(np.array_equal(x, y) for x, y in zip(a, b))
    assert not np.array_equal(C.flujos(7, 1)[0].standard_normal(3), C.flujos(8, 1)[0].standard_normal(3))


@pytest.mark.parametrize("tam,cob,R,apto", [
    (0.050, 0.95, 2000, True), (0.040, 0.92, 2000, True), (0.060, 0.97, 2000, True),
    (0.0, 0.95, 2000, False),      # conservador extremo
    (0.0775, 0.9225, 2000, False),  # tamaño fuera de [0,04; 0,06]
    (0.050, 0.90, 2000, False),    # cobertura fuera
    (0.050, 0.95, 1999, False),    # R insuficiente
    (0.039, 0.95, 2000, False), (0.061, 0.95, 2000, False), (0.050, 0.971, 2000, False),
])
def test_veredicto_umbrales_adenda(tam, cob, R, apto):
    v = C.veredicto(tam, cob, R)
    assert v["apto"] is apto
    assert (not apto) == bool(v["fallos"])


def test_webb_seis_puntos():
    v = C.webb(np.random.default_rng(1), 5000)
    assert len(np.unique(v)) == 6
    assert abs(v.mean()) < 0.05 and abs((v ** 2).mean() - 1) < 0.05


def test_cs_webb_determinista():
    import cs_webb as M
    est = M.construir_estructura()
    assert est["n"] == 41
    a = M.una_rep(est, C.flujos(2, 1)[0], 0.05)
    b = M.una_rep(est, C.flujos(2, 1)[0], 0.05)
    assert a == b


def test_dcdh_determinista_y_linealidad():
    import dcdh_aleatorizacion as M
    est = M.construir_estructura()
    M.B_PERM = 120
    a = M.una_rep(est, C.flujos(3, 1)[0], -0.07)
    b = M.una_rep(est, C.flujos(3, 1)[0], -0.07)
    assert a == b
    # el estimador es lineal en el tratamiento: Y + c D desplaza beta en c
    rng = np.random.default_rng(5)
    dY = rng.standard_normal((est["n"], M.T - 1))
    b0 = M.beta_dcdh(dY, est["D"])
    b1 = M.beta_dcdh(dY + 0.3 * np.diff(est["D"], axis=1), est["D"])
    assert b1 - b0 == pytest.approx(0.3, abs=1e-9)


def test_rejilla_determinista():
    import rejilla_twfe as M
    est = M.construir_estructura("provincia")
    a = M.una_rep(est, C.flujos(4, 1)[0], 0.04)
    b = M.una_rep(est, C.flujos(4, 1)[0], 0.04)
    assert a == b


def test_sdid_determinista():
    import sdid_conley_taber as M
    M.B_PLACEBO = 30
    M.B_WILD = 99
    est = M.construir_estructura("A")
    a = M.una_rep(est, C.flujos(1, 1)[0], -0.0075, True)
    b = M.una_rep(est, C.flujos(1, 1)[0], -0.0075, True)
    assert a == b
    # SDID es equivariante al desplazamiento del tratamiento: añadir c a los tratados en el año post mueve tau en c
    Y, _ = M.simular_y(est, C.flujos(1, 1)[0], 0.0)
    t0 = M.sdid(Y, est["tr"], est["co"])[0]
    Y2 = Y.copy()
    Y2[est["tr"], -1] += 0.1
    assert M.sdid(Y2, est["tr"], est["co"])[0] - t0 == pytest.approx(0.1, abs=1e-9)
