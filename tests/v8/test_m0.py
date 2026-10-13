"""V8-F4 M0: tests rapidos (modo --rapido en un directorio temporal; sinteticos para la permutacion)."""
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
_spec = importlib.util.spec_from_file_location("m0_periodos", RAIZ / "src" / "v8" / "m0_periodos.py")
m0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m0)

COLS_COEF = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio", "variable", "beta", "ee",
             "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad", "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste",
             "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso",
             "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0", "cumple_multiverso", "destacado", "motivo_destacado", "script"]


@pytest.fixture(scope="module")
def corrida(tmp_path_factory):
    r = tmp_path_factory.mktemp("m0")
    m0.main(["--rapido", "--salida", str(r)])
    return r


def test_contrato(corrida):
    c = pd.read_csv(corrida / "coeficientes.csv")
    assert list(c.columns[: len(COLS_COEF)]) == COLS_COEF
    assert set(c.capa) == {"C4"} and set(c.modulo) == {"M0"} and set(c.ambito) == {"nacional"}
    assert set(c.metodo_ajuste) == {"BH"} and (c.p_ajustado >= c.p - 1e-12).all()
    assert set(c.periodo) <= {"P1", "P2", "P3", "P4", "P5"}
    r = pd.read_csv(corrida / "regla_m0.csv")
    assert {"mercado", "periodo", "variable", "signo_principal", "n_confirmaciones", "p_perm", "signo_alternativa", "cumple"} <= set(r.columns)
    assert set(r.cumple) <= {"si", "no", "no_evaluable"}
    # el alquiler nunca cumple (SERPAVI anual: no evaluable) y el P1 de compra tampoco (IPV desde 2007)
    assert (r[r.mercado == "alquiler"].cumple == "no_evaluable").all()
    assert (r[(r.mercado == "compra") & (r.periodo == "P1")].cumple == "no_evaluable").all()
    # cumple => se verifican las condiciones de la regla
    ok = r[r.cumple == "si"]
    assert ((ok.n_confirmaciones >= 1) & (ok.p_perm < 0.05) & (ok.alt_mismo_signo == "si") & (ok.signo_principal != 0)).all()
    d = pd.read_csv(corrida / "periodos_detectados.csv")
    assert {"metodo", "particion", "serie", "detectado", "corte_o_regimen", "ic", "p"} <= set(d.columns)
    assert {"completa", "train_1995_2013", "test_2014_ult"} <= set(d.particion)
    j = json.loads((corrida / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in j
    assert j["capa"] == "C4" and set(j["fuera_muestra"]) >= {"modelo", "rmse", "dm_vs_ar4"}
    assert (corrida / "registro.csv").exists() and (corrida / "resumen.md").exists()
    reg = pd.read_csv(corrida / "registro.csv")
    assert len(reg) >= len(c)   # toda especificacion probada esta en el Registry


def test_determinista(corrida, tmp_path):
    m0.main(["--rapido", "--salida", str(tmp_path)])
    for f in ("coeficientes.csv", "regla_m0.csv", "periodos_detectados.csv"):
        a, b = pd.read_csv(corrida / f), pd.read_csv(tmp_path / f)
        pd.testing.assert_frame_equal(a, b)


def test_muestras_y_periodos():
    d = m0.cargar()
    F = m0.marco(d)
    E = m0.ecuacion(F, "y_compra", list(m0.BASE), list(m0.PERIODOS))
    idx = list(E["S"].index)
    assert not E["S"].isna().any().any()
    for P, (a, b) in E["tr"].items():
        assert idx[a] >= m0.PERIODOS[P][0] and idx[b - 1] <= m0.PERIODOS[P][1]   # los huecos 2008T1-T2 y 2020T1 no pertenecen a ningun tramo
    assert "2008Q1" not in [idx[i] for a, b in E["tr"].values() for i in range(a, b)]


def test_permutacion_sintetica_detecta_cambio_de_pendiente():
    rng = np.random.default_rng(1)
    n = 90
    x = rng.standard_normal(n)
    y = np.where((np.arange(n) >= 30) & (np.arange(n) < 60), -4.0, 4.0) * x + rng.standard_normal(n) * 0.5
    X = np.column_stack([np.ones(n), x])
    E = {"y": pd.Series(y), "X": pd.DataFrame(X), "xs": ["x"], "tr": {"A": (0, 30), "B": (30, 60), "C": (60, 90)}}
    p, modo, st = m0.p_perm_periodo(E, "x", "B", 500, 20261010)
    assert p < 0.05                       # B (pendiente -4) frente a A/C (pendiente +4): las fechas importan
    y0 = rng.standard_normal(n)
    E["y"] = pd.Series(y0)
    p0, _, _ = m0.p_perm_periodo(E, "x", "A", 300, 20261010)
    assert p0 > 0.05                      # sin efecto: no rechaza


def test_senales_signos_y_confirmacion():
    rng = np.random.default_rng(2)
    n = 80
    x = rng.standard_normal(n)
    y = np.where(np.arange(n) < 40, 1.0, -1.0) * x + 0.3 * rng.standard_normal(n)
    idx = [f"{2000 + i // 4}Q{i % 4 + 1}" for i in range(n)]
    S = pd.DataFrame({"y": y, "x": x}, index=idx)
    X = pd.DataFrame({"const": 1.0, "x": x})
    E = {"S": S, "X": X, "y": pd.Series(y), "xs": ["x"], "tr": {"P1": (0, 20), "P2": (20, 40), "P3": (40, 80)}}
    et = pd.Series(np.where(np.arange(n) < 40, 0.0, 1.0), index=idx)
    s = m0.signos_en_regimen(E, et, "P1")
    assert s == {"x": 1}
    assert m0.signos_en_regimen(E, et, "P3") == {"x": -1}
