"""V8-F4 M2: tests rapidos del SVAR (modo --rapido, datos reales de solo lectura; escribe en un directorio temporal)."""
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
_spec = importlib.util.spec_from_file_location("m2_svar", RAIZ / "src" / "v8" / "m2_svar.py")
m2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m2)

FICHEROS = ["irf.csv", "fevd.csv", "hd_periodos.csv", "atribucion.csv", "hipotesis_m2.csv", "predicciones_congeladas.csv"]
FACTORES = {"demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo", "residuo", "demanda_vivienda"}


@pytest.fixture(scope="module")
def corridas(tmp_path_factory):
    base = tmp_path_factory.mktemp("m2")
    rutas = []
    for k in (1, 2):
        r = base / f"c{k}"
        m2.main(["--rapido", "--salida", str(r)])
        rutas.append(r)
    return rutas


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def test_identidad_dh_datos_reales(corridas):
    j = json.loads((corridas[0] / "resultado.json").read_text())
    for nom, d in j["diagnosticos"]["estimaciones"].items():
        assert d["n_aceptadas"] >= 5, nom
        assert d["hd_error_max"] < 1e-8, (nom, d["hd_error_max"])      # y = det + sum(contrib) en cada trimestre
        assert d["cierre_hd_max"] < 1e-6, (nom, d["cierre_hd_max"])    # suma de factores por periodo = variacion observada
    assert j["diagnosticos"]["estimaciones"]["V3"]["max_abs_cero"] < 1e-9   # ceros exactos


def test_columnas_contrato(corridas):
    r = corridas[0]
    irf = pd.read_csv(r / "irf.csv")
    assert list(irf.columns) == ["variante", "shock", "variable", "h", "mediana", "b68_lo", "b68_hi", "b90_lo", "b90_hi"]
    assert sorted(irf.h.unique()) == list(range(21))
    fe = pd.read_csv(r / "fevd.csv")
    assert list(fe.columns) == ["variante", "variable", "h", "shock", "mediana", "b68_lo", "b68_hi"]
    assert sorted(fe.h.unique()) == [4, 8, 12, 20]
    sumas = fe[fe.variante == "V3"].groupby(["variable", "h"])["mediana"].sum()
    assert sumas.between(0.8, 1.2).all()
    hd = pd.read_csv(r / "hd_periodos.csv")
    assert list(hd.columns[:11]) == ["variante", "mercado", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "prob_pos"]
    assert set(hd.mercado) == {"compra", "alquiler"} and {"P2", "P3", "P4", "P5"} <= set(hd.periodo)
    assert "P1" in set(hd[hd.variante == "larga"].periodo)
    at = pd.read_csv(r / "atribucion.csv")
    assert list(at.columns) == ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "notas"]
    assert set(at.metodo) == {"svar_hd"} and set(at.factor) <= FACTORES and set(at.ambito) == {"nacional"}
    hp = pd.read_csv(r / "hipotesis_m2.csv")
    assert list(hp.id) == ["H8-1", "H8-2", "H8-3", "H8-4"] and (hp.p_holm >= hp.p_unilateral - 1e-12).all()
    assert (r / "registro.csv").exists() and (r / "resumen.md").exists()
    j = json.loads((r / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in j
    assert set(j["fuera_muestra"]) >= {"modelo", "rmse", "dm_vs_ar4"}


def test_variables_y_muestra():
    d = m2.cargar()
    S = m2.series_base(d)
    pd.testing.assert_series_equal(S["p"].dropna(), 100 * d["d_ln_p_tasado_real"].reindex(S["p"].dropna().index), check_names=False, atol=1e-5, rtol=0)
    sp = m2.construir("V3", d)
    assert sp["Y"].index[0] == "2004Q2" and sp["Y"].index[-1] == "2026Q1" and list(sp["Y"].columns) == m2.VARS7
    assert m2.construir("larga", d)["Y"].index[0] == "1995Q2"


def test_congelacion(corridas):
    r = corridas[0]
    meta = json.loads((r / "congelacion.json").read_text())
    assert meta["sha256"] == sha(r / "predicciones_congeladas.csv")
    pc = pd.read_csv(r / "predicciones_congeladas.csv")
    assert set(pc.variable) == {"p", "r"} and (pc[pc.evaluable].h_desde_2026T2.between(1, 4)).all()


def test_determinismo(corridas):
    a, b = corridas
    for f in FICHEROS + ["resumen.md", "registro.csv"]:
        assert sha(a / f) == sha(b / f), f
