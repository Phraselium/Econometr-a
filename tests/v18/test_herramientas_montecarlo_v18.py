"""V18 · Infraestructura del Monte Carlo (bandas, semillas, determinismo) y humo de cada conductor con R minúsculo, sin escribir en output/."""
import importlib
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.montecarlo import _comun as C  # noqa: E402


def test_bandas_del_encargo_y_de_la_adenda_112():
    assert C.banda_encargo(0.05, [0.95, 0.94], 2000)["apto"]
    assert C.banda_encargo(0.08, 0.92, 2000)["apto"] and C.banda_encargo(0.03, 0.97, 2000)["apto"]
    assert not C.banda_encargo(0.0775, 0.90, 2000)["apto"]
    assert not C.banda_encargo(0.02, 0.95, 2000)["apto"]
    b = C.banda_encargo(0.09, 0.95, 2000)
    assert not b["apto"] and "liberal" in b["fallos"][0]
    assert C.banda_encargo(0.05, 0.95, 1000)["R_menor_2000"]
    assert C.banda_112(0.05, 0.95, 2000) == "apta"
    assert C.banda_112(0.07, 0.95, 2000) == "con valor crítico corregido"
    assert C.banda_112(0.20, 0.80, 2000) == "no fiable" and C.banda_112(0.0, 1.0, 2000) == "no fiable"
    assert C.banda_112(0.05, 0.95, 1500) == "con valor crítico corregido"


def test_flujos_son_deterministas_y_la_paralelizacion_no_cambia_el_resultado():
    a = [r.random() for r in C.flujos(1, 2, 5)]
    b = [r.random() for r in C.flujos(1, 2, 5)]
    assert a == b and len(set(a)) == 5
    from src.v18.montecarlo import lp_iv as M
    m1 = C.ejecutar(M.rep, (0.4, 0.95, False), 12, 99, 1, 1)
    m2 = C.ejecutar(M.rep, (0.4, 0.95, False), 12, 99, 1, 2)
    assert np.allclose(m1, m2, equal_nan=True)


def _humo(nombre, tmp_path, **kw):
    m = importlib.import_module("src.v18.montecarlo." + nombre)
    assert m.ALCANCE_TERRITORIAL == "sin lectura de datos"
    m.main(4, 1, salida=tmp_path, **kw)
    carpeta = tmp_path / nombre
    r = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in r
    assert (carpeta / "tabla.csv").read_text(encoding="utf-8").count("\n") >= 2
    assert "Veredicto" in (carpeta / "informe.md").read_text(encoding="utf-8")
    return r


def test_humo_conductores_de_series_y_metaanalisis(tmp_path):
    for n in ("lp_iv", "meta_bayes"):
        r = _humo(n, tmp_path)
        assert r["diagnosticos"]["veredicto"]


def test_humo_conductores_de_paneles(tmp_path):
    _humo("cs_webb", tmp_path, escenarios=["cat_anual"])
    _humo("sa_webb", tmp_path, escenarios=["cat_anual"])
    _humo("honest_did", tmp_path, escenarios=["cat_M_M0_PTexacta"])
    _humo("sdid_conley_taber", tmp_path, escenarios=["tratados_05"])


def test_humo_conductores_de_aleatorizacion_y_svar(tmp_path):
    for n in ("dcdh_aleatorizacion", "aleatorizacion", "svar_proxy"):
        _humo(n, tmp_path)


def test_ningun_modulo_nuevo_lee_datos():
    import re
    for p in list((RAIZ / "src" / "v18" / "montecarlo").glob("*.py")) + list((RAIZ / "src" / "v18" / "herr18").glob("*.py")):
        t = p.read_text(encoding="utf-8").replace("read_csv(SALIDA", "")   # releer su propia tabla simulada no es leer datos
        if p.name == "__init__.py":
            continue
        assert re.search(r'^ALCANCE_TERRITORIAL\s*=\s*"sin lectura de datos"', t, re.M), p.name
        assert not re.search(r"read_csv|read_parquet|data/sealed|open\(", t), p.name
