"""V18 · dCDH con dosis continua (DID_ℓ) e inferencia por aleatorización (src/v18/herramientas/dcdh.py y aleatorizacion.py)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herramientas import aleatorizacion as A  # noqa: E402
from src.v18.herramientas import dcdh as H  # noqa: E402
from src.v18.montecarlo import _dgp_itp as P  # noqa: E402


def _caso(seed=1, ell=0):
    rng = np.random.default_rng(seed)
    y, Dc, bi, cl = P.simular(rng, "desigual", -0.03)
    return rng, y, Dc, bi, cl


def test_calendario_declarado():
    Dc = P.calendario(np.random.default_rng(3))
    assert Dc.shape == (8, 24)
    assert (Dc[1] == 7).all() and (Dc[2] == 7).all()              # CCAA sin cambio
    assert (np.diff(Dc, axis=1) != 0).any()
    assert len(P.cl_idx("desigual")) == 36 and np.bincount(P.cl_idx("desigual")).tolist() == [8, 1, 9, 5, 4, 3, 2, 4]


def test_sin_ruido_dcdh_recupera_el_efecto_de_nivel():
    rng = np.random.default_rng(2)
    Dc = P.calendario(rng)
    cl = P.cl_idx("desigual")
    D = Dc[cl]
    a = rng.normal(0, 1, (36, 1))
    g = rng.normal(0, 1, (1, 24))
    for ell in (0, 4):
        Y = a + g - 0.05 * D
        r = H.estimar(Y, D, ell)
        assert abs(r["beta"] + 0.05) < 1e-10
    bi = rng.normal(-0.03, 0.01, 36)
    Y = a + g + bi[:, None] * D
    assert abs(H.estimar(Y, D, 0)["beta"] - H.verdad(bi, D, 0)) < 1e-10


def test_pvalores_de_aleatorizacion_en_rango_y_rechazan_efecto_grande():
    rng, y, Dc, bi, cl = _caso(4)
    perms = H.permutaciones(rng, 8, 199)
    assert perms.shape == (199, 8)
    for est in (True, False):
        p = H.p_aleatorizacion(y, Dc, cl, 0.0, 0, perms, est)
        assert 0 < p <= 1
    y2 = y - 0.5 * Dc[cl]
    assert H.p_aleatorizacion(y2, Dc, cl, 0.0, 0, perms, True) < 0.05


def test_webb_y_ee_de_agrupacion():
    rng, y, Dc, bi, cl = _caso(5)
    M = H.onehot(cl)
    r = H.estimar(y, Dc[cl], 0)
    assert H.ee_cluster(r["IF"], M) > 0
    p = H.p_webb(y, Dc[cl], 0.0, 0, M, rng, 199)
    assert 0 < p <= 1


def test_aleatorizacion_e2_etiquetas_conservan_conteos():
    rng = np.random.default_rng(6)
    lab = np.array([True] * 6 + [False] * 14)
    estrato = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3])
    P1 = A.etiquetas_individual(rng, lab, 50)
    assert (P1.sum(1) == 6).all()
    P2 = A.etiquetas_estrato(rng, lab, estrato, 50)
    for e in np.unique(estrato):
        assert (P2[:, estrato == e].sum(1) == lab[estrato == e].sum()).all()


def test_aleatorizacion_did_sin_ruido_y_con_efecto():
    rng = np.random.default_rng(7)
    n = 60
    lab = np.arange(n) < 15
    d = rng.normal(0, 0.2, n) + 0.5 * lab
    perms = A.etiquetas_individual(rng, lab, 499)
    assert A.p_did(d, lab, 0.0, perms, True) < 0.01
    assert A.p_did(d, lab, 0.5, perms, True) > 0.1


def test_twfe_dosis_recupera_beta_y_p_calendarios():
    rng, y, Dc, bi, cl = _caso(8)
    M = (cl[:, None] == np.arange(8)[None, :]).astype(float)
    a = rng.normal(0, 1, (36, 1))
    g = rng.normal(0, 1, (1, 24))
    b, se = A.twfe_dosis(a + g - 0.04 * Dc[cl], Dc[cl], M)
    assert abs(b + 0.04) < 1e-10
    perms = H.permutaciones(rng, 8, 99)
    p = A.p_calendarios(y, Dc, cl, 0.0, perms, True)
    assert 0 < p <= 1
