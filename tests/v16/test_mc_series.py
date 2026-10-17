"""Pruebas mínimas del grupo «series» de la validación Monte Carlo V16 (R pequeño, sin escribir en el repositorio)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402
from src.v16.montecarlo import bh_jerarquico as bh  # noqa: E402
from src.v16.montecarlo import bayes_jerarquico as bj  # noqa: E402
from src.v16.montecarlo import cips_bootstrap as cp  # noqa: E402
from src.v16.montecarlo import csardl as cs  # noqa: E402
from src.v16.montecarlo import dm_hln as dm  # noqa: E402
from src.v16.montecarlo import gsadf_factor as gs  # noqa: E402
from src.v16.montecarlo import tost as ts  # noqa: E402


def test_veredicto_umbrales_adenda():
    assert C.SEED == 20261010
    assert C.veredicto(0.05, 2000, 0.95)["veredicto"] == "APTO"
    assert C.veredicto(0.0, 2000)["veredicto"] == "NO APTO"        # tamaño 0,0 es fallo
    assert C.veredicto(0.07, 2000)["veredicto"] == "NO APTO"
    assert C.veredicto(0.05, 500)["veredicto"] == "NO APTO"        # R < 2.000
    assert C.veredicto(0.05, 2000, 0.90)["veredicto"] == "NO APTO"  # cobertura fuera de [0,92; 0,97]


def test_determinismo_cips():
    assert cp.una(3, "nulo", 9, 9) == cp.una(3, "nulo", 9, 9)


def test_determinismo_csardl():
    assert cs.una(3, 5, 9, 0.8) == cs.una(3, 5, 9, 0.8)


def test_determinismo_gsadf():
    assert gs.una(3, "salto", False, 5, 1.5) == gs.una(3, "salto", False, 5, 1.5)


def test_determinismo_dm():
    assert dm.una(3, 0.0) == dm.una(3, 0.0)


def test_determinismo_bh_y_estructura():
    est = bh.estructura_rejilla()
    assert len(est[0]) == 83 and len(set(est[0])) == 5
    assert bh.evaluar(est, .4, .2, "positivos", "celdas_20", 30, 1) == bh.evaluar(est, .4, .2, "positivos", "celdas_20", 30, 1)
    assert len(bh.estructura_disenos(18)[0]) == 18 and len(bh.estructura_disenos(21)[0]) == 21


def test_bh_jerarquico_global_nulo_sin_rechazos_con_p_altos():
    fam = np.array(["a"] * 5 + ["b"] * 5)
    assert not bh.jerarquico(np.full(10, 0.5), fam, "bh").any()
    assert bh.jerarquico(np.full(10, 1e-8), fam, "bh").all()


def test_determinismo_bayes():
    mp, sm = np.repeat(np.arange(2), 3), np.repeat(np.arange(6), 2)
    bj.ITER, bj.BURN = 40, 10
    assert bj.una(3, "no_nulo", 1.0, mp, sm) == bj.una(3, "no_nulo", 1.0, mp, sm)


def test_tost_tamano_borde_cerca_del_nominal():
    rng = C.rng(99)
    assert abs(ts.tost_rechaza(rng, 20000, 5.0, None, 1.0).mean() - 0.05) < 0.01
    assert ts.tost_rechaza(rng, 20000, 0.5, None, 1.0).mean() < 0.005
