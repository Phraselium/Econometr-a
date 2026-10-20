"""V18 · Driscoll-Kraay (simulación; sin datos reales)."""
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


D = _cargar("t_driscoll_kraay", "src/v18/herr18/driscoll_kraay.py")
MC = _cargar("t_mc_dk", "src/v18/montecarlo/driscoll_kraay.py")


def _datos(T=14, seed=4):
    x, e = MC.dgp(np.random.default_rng(seed), T, 0.5)
    return 0.3 * x + e, x


def test_alcance():
    assert D.ALCANCE_TERRITORIAL == MC.ALCANCE_TERRITORIAL == "sin lectura de datos"


def test_ancho_por_defecto():
    assert D.ancho_por_defecto(14) == 2 and D.ancho_por_defecto(30) == 3


def test_beta_igual_a_mco_con_dummies():
    y, x = _datos(T=8)
    N, T = y.shape
    cols = [x.ravel()] + [np.repeat(np.arange(N) == i, T).astype(float) for i in range(N)]
    coef = np.linalg.lstsq(np.column_stack(cols), y.ravel(), rcond=None)[0]
    assert abs(coef[0] - D.fe_dk(y, x[:, :, None], 1)["beta"][0]) < 1e-9


def test_dk_con_m0_es_suma_de_momentos_por_periodo():
    y, x = _datos()
    r = D.fe_dk(y, x[:, :, None], 0)
    xt = x - x.mean(1, keepdims=True)
    yt = y - y.mean(1, keepdims=True)
    b = (xt * yt).sum() / (xt ** 2).sum()
    h = (xt * (yt - b * xt)).sum(0)
    assert abs(r["V_dk"][0, 0] - (h ** 2).sum() / (xt ** 2).sum() ** 2) < 1e-12


def test_mc_pequeno(tmp_path):
    esc = [{"T": 14, "rho_f": 0.5, "tiempo": False, "principal": True}]
    tab = MC.main(R=40, salida=tmp_path, esc=esc)
    assert len(tab) == 4 and (tmp_path / "resultado.json").exists()
    assert "simulación; sin datos reales" in (tmp_path / "informe.md").read_text(encoding="utf-8")
