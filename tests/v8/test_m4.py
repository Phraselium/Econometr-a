"""V8-F4 M4: tests rapidos (modo --rapido; datos sinteticos para FMOLS, Gregory-Hansen y el cierre de las contribuciones)."""
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
_spec = importlib.util.spec_from_file_location("m4_largo_plazo", RAIZ / "src" / "v8" / "m4_largo_plazo.py")
m4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m4)

COLS_ATR = ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "notas", "variante", "principal", "vota_s9"]
FACTORES = {"demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo", "residuo"}


@pytest.fixture(scope="module")
def corrida(tmp_path_factory):
    r = tmp_path_factory.mktemp("m4")
    m4.main(["--rapido", "--salida", str(r)])
    return r


def test_contrato(corrida):
    c = pd.read_csv(corrida / "coeficientes.csv")
    for col in ("vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "capa", "p_ajustado", "metodo_ajuste"):
        assert col in c.columns
    assert set(c.capa) == {"C4"} and set(c.modulo) == {"M4"}
    assert {"dols", "fmols", "ardl"} == set(c.metodo_lp)
    lr = c[~c.variable.str.startswith("ruptura:")]
    assert (lr.p_ajustado >= lr.p - 1e-12).all()
    ok = c[c.vel_ajuste.notna() & c.semivida.notna()]
    assert (ok.vel_ajuste < 0).all() and (ok.vel_ajuste > -1).all() and (ok.semivida > 0).all()
    assert c.p_ajustado.notna().all() and (c.metodo_ajuste == "BH").all()
    a = pd.read_csv(corrida / "atribucion.csv")
    assert list(a.columns) == COLS_ATR
    assert set(a.vota_s9) == {"no"} and not a.duplicated(["metodo", "mercado", "ambito", "periodo", "factor", "variante"]).any()
    assert a[a.metodo == "contabilidad_lp"].notas.str.contains("SIN COINTEGRACION DEMOSTRADA").all() and set(a.metodo) == {"contabilidad_lp", "contabilidad"} and set(a.factor) <= FACTORES
    assert (a.b90_lo <= a.b68_lo + 1e-9).all() and (a.b68_hi <= a.b90_hi + 1e-9).all()
    j = json.loads((corrida / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in j
    assert j["capa"] == "C4" and set(j["fuera_muestra"]) >= {"modelo", "rmse", "dm_vs_ar4"}
    assert (corrida / "registro.csv").exists() and (corrida / "resumen.md").exists()
    assert "n_discrepancias_dols_fmols" in j["diagnosticos"]


def test_cierre_contribuciones(corrida):
    """Suma de factores (incluido el residuo) = variacion observada del periodo."""
    a = pd.read_csv(corrida / "atribucion.csv")
    a = a[a.metodo == "contabilidad_lp"]
    d = pd.read_csv(m4.DATOS).set_index("trimestre")
    G = m4.preparar(d)
    for (mk, per, nota), g in a.groupby(["mercado", "periodo", "notas"]):
        i0 = list(G.index)[list(G.index).index(m4.INICIO[mk]) + 2]      # inicio de la ventana efectiva (INICIO + 2 trimestres)
        dy = m4.delta_periodo(G["y_" + mk].loc[i0:], per) * 100
        assert abs(g.contribucion_pp.sum() - dy) < 1e-6


def test_misma_muestra_fuera_de_muestra(corrida):
    o = pd.read_csv(corrida / "fuera_muestra.csv")
    for mk, g in o.groupby("mercado"):
        assert g.n.nunique() == 1 and g.muestra.nunique() == 1       # misma muestra en todas las especificaciones de un mercado
    assert (o["rmse_AR4"] > 0).all()


def test_fmols_recupera_beta_sintetico_y_coincide_con_arch():
    rng = np.random.default_rng(3)
    T = 300
    x = np.cumsum(rng.standard_normal((T, 2)), axis=0)
    ex = np.diff(x, axis=0, prepend=0)
    u = 0.5 * ex[:, 0] + rng.standard_normal(T) * 0.3    # error endogeno
    y = 1.0 + 0.7 * x[:, 0] - 0.4 * x[:, 1] + u
    th, cov, res, b, m = m4.fmols(y, np.ones((T, 1)), x)
    assert abs(th[1] - 0.7) < 0.05 and abs(th[2] + 0.4) < 0.05
    from arch.unitroot.cointegration import FullyModifiedOLS
    ar = FullyModifiedOLS(pd.Series(y), pd.DataFrame(x), trend="c").fit(kernel="bartlett", bandwidth=b, force_int=True)
    assert np.allclose(np.asarray(ar.params)[:2], th[1:], atol=0.03)


def test_gregory_hansen_nula_y_cointegrada():
    rng = np.random.default_rng(4)
    T = 100
    sim = m4.gh_sim(T, 1, 40, 11)
    x = np.cumsum(rng.standard_normal(T))
    y_c = 0.5 * x + rng.standard_normal(T) * 0.3         # cointegrada
    y_n = np.cumsum(rng.standard_normal(T))             # no cointegrada
    sc = m4.gh_stat(y_c, x[:, None])[0]
    sn = m4.gh_stat(y_n, x[:, None])[0]
    assert sc < np.quantile(sim, 0.05) and sc < sn


def test_semivida_y_vif():
    assert abs(m4.semivida(-0.5) - 1.0) < 1e-12 and np.isnan(m4.semivida(0.1))
    x = np.random.default_rng(0).standard_normal((50, 2))
    assert m4.vif_max(x) < 2


def test_ardl_decision_exige_t(corrida):
    c = pd.read_csv(corrida / "cointegracion.csv")
    ok = c.ARDL_rechaza_sin
    # rechaza solo si t < cota I(1) (J10); con t >= cota nunca rechaza
    assert (c.loc[ok, "ARDL_t_yL1_sin"] < c.loc[ok, "ARDL_t_cota_I1_5"]).all()
    assert (~ok[c.ARDL_t_yL1_sin >= c.ARDL_t_cota_I1_5]).all()
    assert (c.loc[c.ARDL_decision_5pct_sin.str.startswith("rechaza"), "ARDL_rechaza_sin"]).all()


def test_voto_contabilidad(corrida):
    v = pd.read_csv(corrida / "voto_contabilidad.csv")
    for col in ("mercado", "periodo", "ventana_R0", "brecha", "brecha_pct_stock_hogares", "signo_dY", "vota_demografia"):
        assert col in v.columns
    vv = v[v.vota_demografia == "si"]
    assert (vv.brecha_pct_stock_hogares.abs() >= 0.5).all() and (vv.signo_brecha == vv.signo_dY).all()
    assert (v.loc[v.vota_demografia == "no", "n_trim"] >= 0).all()
    assert not (corrida / "resultado.json").read_text().count("segundos") and (corrida / "tiempos.json").exists()
