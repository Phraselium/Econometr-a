"""V18 · F efectivo (MOP) y Anderson-Rubin (simulación; sin datos reales)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


H = _cargar("t_iv_debil", "src/v18/herramientas/iv_debil.py")
MC = _cargar("t_mc_iv", "src/v18/montecarlo/iv_debil.py")


def _datos(p=1, pi=(0.3,), seed=2):
    y, X, Z, cl = MC.dgp(np.random.default_rng(seed), p, pi)
    return H.preparar(y + 0.4 * X[:, 0], X, Z, cl)


def test_alcance():
    assert H.ALCANCE_TERRITORIAL == MC.ALCANCE_TERRITORIAL == "sin lectura de datos"


def test_iv_exacto_k1():
    y, X, Z, cl, G = _datos()
    b, _ = H.dos_sls(y, X, Z, cl, G)
    assert abs(b[0] - (Z[:, 0] @ y) / (Z[:, 0] @ X[:, 0])) < 1e-10


def test_f_efectivo_k1_es_f_robusto():
    y, X, Z, cl, G = _datos()
    F = H.f_efectivo(X, Z, cl, G)[0]
    z, x = Z[:, 0], X[:, 0]
    pi = (z @ x) / (z @ z)
    sc = np.bincount(cl, weights=z * (x - pi * z), minlength=G)
    assert abs(F - pi ** 2 * (z @ z) ** 2 / (np.sum(sc ** 2) * G / (G - 1))) < 1e-8


def test_ic_ar_exacto_en_extremos():
    y, X, Z, cl, G = _datos(pi=(0.8,))
    A, C = H.sumas_ar(y, X, Z, cl, G)
    tipo, lo, hi = H.ar_ic_1(A, C, G)
    crit = stats.chi2.ppf(0.95, 1)
    assert tipo == "intervalo"
    for b in (lo, hi):
        assert abs(H.ar_estadistico(A, C, np.array([b]), G)[0] - crit) < 1e-6
    assert H.ar_estadistico(A, C, np.array([(lo + hi) / 2]), G)[0] < crit


def test_ar_dos_endogenas_equivariante_y_subvector():
    y, X, Z, cl, G = _datos(p=2, pi=(0.5, 0.5))
    A, C = H.sumas_ar(y, X, Z, cl, G)
    A2, C2 = H.sumas_ar(y - X @ np.array([0.4, 0.2]), X, Z, cl, G)
    assert abs(H.ar_p(A, C, np.array([0.4, 0.2]), G) - H.ar_p(A2, C2, np.zeros(2), G)) < 1e-10
    pc = H.ar_p(A, C, np.array([0.4, 0.4]), G)
    ps = H.ar_subvector_p(A, C, G, 0.4)
    assert ps >= pc - 1e-9      # la proyección nunca rechaza más que el conjunto


def test_mc_pequeno(tmp_path):
    esc = [{"nombre": "p=1, pi=0.2", "p": 1, "pi": (0.2,)}, {"nombre": "p=2 test", "p": 2, "pi": (0.5, 0.5)}]
    tab = MC.main(R=40, salida=tmp_path, esc=esc)
    assert (tmp_path / "resultado.json").exists() and len(tab) > 6
    assert "simulación; sin datos reales" in (tmp_path / "informe.md").read_text(encoding="utf-8")
