"""V18 · Conley en sección y municipio con geometría sintética (simulación; sin datos reales)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


C = _cargar("t_conley", "src/v18/herr18/conley.py")
MC = _cargar("t_mc_conley", "src/v18/montecarlo/conley.py")


def test_alcance():
    assert C.ALCANCE_TERRITORIAL == MC.ALCANCE_TERRITORIAL == "sin lectura de datos"


def test_geometria_determinista_y_densidad():
    c1, g1, ciu = C.geometria_secciones(np.random.default_rng(1))
    c2, g2, _ = C.geometria_secciones(np.random.default_rng(1))
    assert np.array_equal(c1, c2) and np.array_equal(g1, g2)
    assert len(c1) == 4000 and ciu.sum() == 800 and np.all(np.diff(g1) >= 0)
    assert len(C.geometria_municipios(np.random.default_rng(1))) == 311
    ax, ay = C.CIUDAD
    assert abs(800 / (ax * ay) - 10.6) < 0.2          # densidad de secciones de Barcelona


def test_nucleo_y_wendland():
    c = np.random.default_rng(0).uniform(0, 5, (300, 2))
    K = C.nucleo_bartlett(c, 2.0)
    assert np.allclose(np.diag(K), 1) and np.allclose(K, K.T)
    W = C.wendland(C.distancias(c), 3.0)
    assert np.linalg.eigvalsh(W).min() > -1e-8          # definida positiva en 2D


def test_conley_corte_minimo_es_hc():
    rng = np.random.default_rng(2)
    c = rng.uniform(0, 50, (200, 2))
    x, y = rng.standard_normal(200), rng.standard_normal(200)
    b, se, ok = C.conley_ols(y, x, c, 1e-6)
    xt, yt = x - x.mean(), y - y.mean()
    s = xt * (yt - b * xt)
    assert ok and abs(se - np.sqrt((s ** 2).sum()) / (xt @ xt)) < 1e-12


def test_mc_pequeno(tmp_path):
    tab = MC.main(R=20, salida=tmp_path, niveles=("municipio",), cortes=(2.0,))
    assert len(tab) == 6 and (tmp_path / "resultado.json").exists()
    assert "simulación; sin datos reales" in (tmp_path / "informe.md").read_text(encoding="utf-8")
