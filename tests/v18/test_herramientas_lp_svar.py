"""V18 · LP-IV (2SLS y Anderson-Rubin) y SVAR con proxy (src/v18/herramientas/lp_iv.py y svar_proxy.py)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herramientas import lp_iv as L  # noqa: E402
from src.v18.herramientas import svar_proxy as S  # noqa: E402
from src.v18.montecarlo import lp_iv as MLP  # noqa: E402
from src.v18.montecarlo import svar_proxy as MSV  # noqa: E402


def test_lrv_de_ruido_blanco_es_la_varianza():
    rng = np.random.default_rng(1)
    s = rng.normal(0, 2, (20000, 1))
    assert abs(L.lrv(s, 0)[0, 0] - 4) < 0.2
    assert abs(L.lrv(s, 5)[0, 0] - 4) < 0.4


def test_trayectoria_verdadera_a_h0_es_kappa():
    tr = MLP.trayectoria_verdadera(0.5, 0.95, -0.5, 0.1)
    assert abs(tr[0] - (-0.5)) < 1e-12
    assert abs(tr[1] - ((1.2 * (-0.5 * 0.5) + (-0.5) * 0.2 + 0.1 * 0.5) / 0.5)) < 1e-9


def test_lp_iv_instrumento_fuerte_recupera_beta_y_el_conjunto_ar_lo_contiene():
    # muestra larga para comprobar consistencia (T grande)
    MLP.T = 4000
    try:
        y, di, z = MLP.simular(np.random.default_rng(3), 1.0, 0.95, -0.5, 0.1)
    finally:
        MLP.T = 108
    h = 4
    r = L.lp_iv(y, di, z, h, L=h + 1, p=4)
    ver = MLP.trayectoria_verdadera(1.0, 0.95, -0.5, 0.1)[h]
    assert abs(r["beta"] - ver) < 0.15
    tipo, lo, hi = L.conjunto_ar(r)
    assert tipo == "acotado" and lo - 0.1 < ver < hi + 0.1 and (hi - lo) < 0.5
    assert L.p_ar(r, ver) > 0.001 and L.p_ar(r, ver + 1.0) < 0.05
    assert L.f_robusto(r) > 10


def test_conjunto_ar_con_instrumento_irrelevante_no_es_acotado():
    rng = np.random.default_rng(4)
    y, di, z = MLP.simular(rng, 0.0, 0.9, 0.0, 0.0)
    r = L.lp_iv(y, di, z, 4, L=5, p=4)
    tipo, _, _ = L.conjunto_ar(r)
    assert tipo in ("recta", "no_acotado", "vacio")
    assert L.p_ar(r, 0.0) > 0.0


def test_psi_con_p1_es_potencia_de_la_matriz():
    A = np.array([[[0.5, 0.1], [0.0, 0.3]]])
    for h in range(5):
        assert np.allclose(S.psi(A, h), np.linalg.matrix_power(A[0], h))


def test_proxy_svar_recupera_la_respuesta_con_muestra_larga():
    MSV.T = 5000
    try:
        Y, z = MSV.simular(np.random.default_rng(5), 63.0, 0.9, False)
    finally:
        MSV.T = 108
        MSV._phi.cache_clear()
    A, B0 = MSV._estructura(0.9, False)
    ver = S.theta_verdadero(A, B0[:, 0], 4, MSV.J_PRECIO, MSV.REF)
    r = S.proxy_svar(Y, z, 2, 4, MSV.J_PRECIO, MSV.REF)
    assert abs(r["beta"] - ver) < 0.1
    tipo, lo, hi = L.conjunto_ar(r)
    assert tipo == "acotado" and lo - 0.1 <= ver <= hi + 0.1
