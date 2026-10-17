"""Pruebas mínimas del grupo «iv_espacial» de la fase 5 de V16: determinismo con la semilla (R pequeño) y umbrales de la adenda en el veredicto."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v16" / "montecarlo"))

import _comun_iv_espacial as C  # noqa: E402


def test_semilla_y_umbrales():
    assert C.SEED == 20261010
    assert (C.TAM_MIN, C.TAM_MAX, C.COB_MIN, C.COB_MAX, C.R_MIN) == (0.04, 0.06, 0.92, 0.97, 2000)


def test_veredicto_umbrales_adenda():
    assert C.veredicto(0.05, 2000, 0.95)["veredicto"] == "APTO"
    assert C.veredicto(0.0, 5000, 0.97)["veredicto"] == "NO APTO"            # tamaño 0,0 = conservador extremo
    assert C.veredicto(0.07, 5000, 0.95)["veredicto"] == "NO APTO"
    assert C.veredicto(0.05, 5000, 0.98)["veredicto"] == "NO APTO"
    assert C.veredicto(0.05, 1000, 0.95)["veredicto"] == "NO APTO"           # R < 2.000
    assert C.veredicto(0.0400, 2000, 0.92)["veredicto"] == "APTO"
    assert C.veredicto(0.0600, 2000, 0.97)["veredicto"] == "APTO"


def test_shiftshare_determinista():
    import shiftshare_akm as s
    S, provs, orig = s.cuotas()
    assert S.shape == (41, 28) and len(provs) == 41 and len(orig) == 28
    a = C.paralelo(s.f_rep, 31, 40, n_jobs=1, n_trozos=4, S=S)
    b = C.paralelo(s.f_rep, 31, 40, n_jobs=1, n_trozos=4, S=S)
    assert a.shape == b.shape and np.array_equal(a, b, equal_nan=True)


def test_akm0_intervalo_consistente_con_prueba():
    import shiftshare_akm as s
    S, _, _ = s.cuotas()
    (b0, sc0, sa0, SA0, SB0, Ak0, Bk0, sxx0), (b1, sc1, sa1, SA1, SB1, Ak1, Bk1, sxx1) = s.lote(C.rng(1, 1), 50, S)
    lo, hi, acot = s.akm0_ic(SA1, SB1, Ak1, Bk1)
    for i in np.where(acot & ~np.isnan(lo))[0][:10]:
        medio = (lo[i] + hi[i]) / 2
        assert not s.akm0_rechaza(SA1[i:i + 1], SB1[i:i + 1], Ak1[i:i + 1], Bk1[i:i + 1], medio)[0]
        assert s.akm0_rechaza(SA1[i:i + 1], SB1[i:i + 1], Ak1[i:i + 1], Bk1[i:i + 1], hi[i] + 1.0)[0]


def test_lp_determinista_y_cv():
    import lp_newey_west_b as lp
    cv = {0.2: 2.0, 1.0: 3.0}
    a = C.paralelo(lp.f_rep, 34, 16, n_jobs=1, n_trozos=2, rho=0.95, theta_alt=-0.006 / 0.95 ** 4, cv=cv)
    b = C.paralelo(lp.f_rep, 34, 16, n_jobs=1, n_trozos=2, rho=0.95, theta_alt=-0.006 / 0.95 ** 4, cv=cv)
    assert np.array_equal(a, b)
    assert 1.96 < lp.cv_fijo_b(0.2, n=200, ndraw=10000) < 3.0


def test_did_y_blp_deterministas():
    import did_intensidad_webb as d
    e = d.estructura()
    assert e["G"] == 41 and e["Nm"] > 300
    a = C.paralelo(d.f_rep, 33, 4, n_jobs=1, n_trozos=2, e=e, B=19, modo="P")
    b = C.paralelo(d.f_rep, 33, 4, n_jobs=1, n_trozos=2, e=e, B=19, modo="P")
    assert np.array_equal(a, b)
    import blp_gates as g
    eg = g.estructura()
    assert eg["N"] > 1000 and eg["G"] >= 30
    a = C.paralelo(g.f_rep, 35, 2, n_jobs=1, n_trozos=2, e=eg, S=3)
    b = C.paralelo(g.f_rep, 35, 2, n_jobs=1, n_trozos=2, e=eg, S=3)
    assert np.array_equal(a, b, equal_nan=True)


def test_conley_determinista_y_sin_selladas():
    import conley_seccion as c
    est = c.estructura()
    assert 5000 < est["n"] < 20000
    K, W = c.matrices(est, 1.0)
    a = C.paralelo(c.f_rep, 32, 4, n_jobs=1, n_trozos=2, est=est, K=K, W=W)
    b = C.paralelo(c.f_rep, 32, 4, n_jobs=1, n_trozos=2, est=est, K=K, W=W)
    assert np.array_equal(a, b)
