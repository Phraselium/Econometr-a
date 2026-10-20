"""V18 · BHJ a nivel de choque: herramienta y Monte Carlo (simulación; sin datos reales)."""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
os.environ["V18_MC_JOBS"] = "1"


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


B = _cargar("t_bhj_inferencia", "src/v18/herr18/bhj_inferencia.py")
MC = _cargar("t_mc_bhj", "src/v18/montecarlo/bhj.py")


def test_alcance_y_semilla():
    assert B.ALCANCE_TERRITORIAL == MC.ALCANCE_TERRITORIAL == "sin lectura de datos"
    assert B.SEED == MC.SEED == 20261010


def test_pesos_hhi_objetivo():
    for K, h in ((10, 0.1), (10, 0.3), (30, 0.2), (20, 0.1)):
        w = B.pesos_con_hhi(K, h)
        assert abs(w.sum() - 1) < 1e-12 and abs(B.hhi(w) - h) < 1e-6 and w.min() > 0


def test_equivariancia_traslacion_beta():
    rng = np.random.default_rng(3)
    x, u, w, s, g = MC.dgp_datos(rng, 20, 0.2, 1.0)
    r0 = B.bhj_choque(u, x, w, s, g, ar=True)
    r1 = B.bhj_choque(u + 0.5 * x, x, w, s, g, ar=True)
    assert abs(r1["beta"] - r0["beta"] - 0.5) < 1e-9 and abs(r1["se"] - r0["se"]) < 1e-9
    if r0["ic_ar"] is not None and r1["ic_ar"] is not None:
        assert abs(r1["ic_ar"][0] - r0["ic_ar"][0] - 0.5) < 5e-3
        assert abs(r1["ic_ar"][1] - r0["ic_ar"][1] - 0.5) < 5e-3


def test_mc_pequeno_escribe_salidas(tmp_path):
    esc = [{"K": 10, "h": 0.2, "pi": 1.0, "principal": True}]
    tab = MC.main(R=40, escenarios=esc, salida=tmp_path)
    assert len(tab) == 3
    assert (tmp_path / "resultado.json").exists() and (tmp_path / "tabla.csv").exists()
    assert "simulación; sin datos reales" in (tmp_path / "informe.md").read_text(encoding="utf-8")
    assert tab.tamano_5pct.between(0, 1).all()
