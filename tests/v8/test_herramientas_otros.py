"""Tests rapidos (<60 s) de src/v8/herramientas (grupo B: no VAR). Solo datos SIMULADOS, SEED=20261010."""
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
from src.v8.herramientas import dfm, dominancia, lp, multiverso, permutacion, regimenes, shap_grupos  # noqa: E402

SEED = 20261010


def g(k=0):
    return np.random.default_rng([SEED, k])


def test_umbral_detecta_y_no_detecta():
    r = g(1)
    n = 150
    x, q = r.normal(size=n), r.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    y1 = 1 + np.where(q > 0, 1.5, 0.2) * x + r.normal(size=n) * .6
    o = regimenes.umbral_hansen(y1, X, q, B=199)
    assert o["p_linealidad"] < 0.05 and abs(o["gamma"]) < 0.4
    assert o["ic_gamma"][0] <= o["gamma"] <= o["ic_gamma"][1]
    y0 = 1 + .5 * x + r.normal(size=n)
    assert regimenes.umbral_hansen(y0, X, q, B=199)["p_linealidad"] > 0.05


def test_bai_perron_fechas_y_ruptures():
    r = g(2)
    y = np.r_[r.normal(0, 1, 60), r.normal(1.5, 1, 60)]
    o = regimenes.bai_perron(y, max_cortes=2, B=99)
    assert o["p_UDmax"] < 0.05 and abs(o["cortes"][1][0] - 60) <= 3
    assert abs(regimenes.bai_perron_ruptures(y, 1)[0] - o["cortes"][1][0]) <= 1
    assert regimenes.bai_perron(r.normal(size=120), B=99, max_cortes=2)["p_UDmax"] > 0.05


def test_markov_switching_fit_y_contraste():
    r = g(3)
    y = regimenes.__dict__["np"].r_[r.normal(0, 1, 100), r.normal(3, 1.5, 100)]
    f = regimenes.ms_fit(y, 2, search_reps=3)
    assert abs(sorted([f["params"]["const[0]"], f["params"]["const[1]"]])[1] - 3) < 1
    t = regimenes.ms_contraste_regimenes(y, 1, 2, B=9, search_reps=2)
    assert t["p"] <= 0.2 and t["LR"] > 10


def test_dfm_bai_ng_y_ml():
    r = g(4)
    T, N = 120, 40
    F = r.normal(size=(T, 2))
    X = F @ r.normal(size=(2, N)) + r.normal(size=(T, N))
    assert dfm.bai_ng(X, 6)["k_ic2"] == 2
    p = dfm.pca_factores(X, 2)
    assert p["factores"].shape == (T, 2) and 0.2 < p["var_explicada_total"] < 1
    ev = dfm.evolucion_ventanas(X, 2, ventana=40, paso=20)
    assert len(ev) == 5
    o = dfm.dfm_ml(X[:, :6], 1, maxiter=30)
    assert o["cargas"].shape == (6, 1) and o["r2"].shape == (6, 1)


def test_lp_y_lp_iv():
    r = g(5)
    n = 300
    z, v = r.normal(size=n), r.normal(size=n)
    u = .7 * v + .7 * r.normal(size=n)
    x = z + v
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = .5 * y[t - 1] + x[t] + u[t]
    o = lp.lp_iv(y, x, z, H=2, rezagos=1, grid_n=801)
    assert abs(o.beta[0] - 1) < .3 and o.F_robusto[0] > 50
    assert o.ar_lo[0] <= 1 <= o.ar_hi[0] and o.ar_acotado[0]
    d = lp.lp(y, x - u * 0, H=2, rezagos=1)
    assert list(d.columns[:5]) == ["h", "beta", "se", "lo", "hi"] and len(d) == 3
    # AR con instrumento debil: no acotado o amplio
    zd = .02 * z + r.normal(size=n)
    xd = .02 * z + v
    od = lp.lp_iv(y, xd, zd, H=0, rezagos=1, grid_n=801)
    assert od.F_robusto[0] < 10 and (not od.ar_acotado[0] or od.ar_hi[0] - od.ar_lo[0] > 5)


def test_lp_panel():
    r = g(6)
    N, T = 12, 40
    rows = []
    for i in range(N):
        a = r.normal()
        x = r.normal(size=T)
        y = np.zeros(T)
        for t in range(1, T):
            y[t] = a + .5 * y[t - 1] + .8 * x[t] + r.normal() * .5
        rows += [{"i": i, "t": t, "y": y[t], "x": x[t]} for t in range(T)]
    o = lp.lp_panel(pd.DataFrame(rows), "y", "x", "i", "t", H=2)
    assert abs(o.beta[0] - .8) < .2 and len(o) == 3


def test_dominancia():
    r = g(7)
    n = 400
    S = np.eye(4)
    S[0, 1] = S[1, 0] = .85
    X = r.multivariate_normal(np.zeros(4), S, n)
    y = X @ [1, .5, .3, 0.] + r.normal(size=n)
    o = dominancia.shapley_r2(X, y, B=20)
    assert abs(o.phi.sum() - o.attrs["r2"]) < 1e-10
    j = dominancia.johnson_rw(X, y)
    assert abs(j.peso.sum() - o.attrs["r2"]) < 0.02
    c = dominancia.colinealidad(X)
    assert c["vif"].iloc[0] > 3 and c["ci_max"] > 1
    s = dominancia.ortogonalizacion_secuencial(X, y)
    assert np.allclose(s["resumen"]["media"].values, o.phi.values, atol=1e-8)
    inc = dominancia.r2_incremental_orden(X, y, [2, 0, 1, 3])
    assert abs(inc.sum() - o.attrs["r2"]) < 1e-10
    g2 = dominancia.shapley_r2(X, y, grupos={"A": [0, 1], "B": [2, 3]})
    assert abs(g2.phi.sum() - o.attrs["r2"]) < 1e-10
    try:
        dominancia.shapley_r2(r.normal(size=(50, 11)), r.normal(size=50))
        raise AssertionError("debia fallar con 11 jugadores")
    except ValueError:
        pass


def test_permutacion_fechas():
    r = g(8)
    n = 200
    x = r.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    y = 1 + np.where(np.arange(n) >= 100, 2.0, .2) * x + r.normal(size=n)
    o = permutacion.permutacion_cortes(permutacion.stat_t_dif_coef(y, X, 1), n, (100,), 20, n_perm=2000)
    assert o["p"] < .05 and o["modo"] == "enumeracion_exacta"
    assert permutacion.n_conjuntos(100, 2, 15) == 71
    o3 = permutacion.permutacion_cortes(permutacion.stat_dif_coef(y, X, 1), n, (33, 66), 10, n_perm=2000)
    assert o3["modo"] == "monte_carlo_exacto" and o3["n_perm"] == 2000 and 0 < o3["p"] <= 1


def test_shap_grupos():
    r = g(9)
    n = 300
    X = pd.DataFrame(r.normal(size=(n, 6)), columns=list("abcdef"))
    y = 2 * X.a + 1.5 * X.b + np.sin(2 * X.c) + .7 * X.d * X.e + r.normal(size=n) * .5
    gr = {"F1": ["a", "b"], "F2": ["c"], "F3": ["d", "e"], "F4": ["f"]}
    m = shap_grupos.modelo_lgbm().fit(X.values, y)
    imp = shap_grupos.shap_grupos(m, X, gr)[0]
    assert list(imp.index)[:2] == ["F1", "F2"] and imp.index[-1] == "F4"
    pg = shap_grupos.perm_agrupada(m, X, y, gr, n_rep=3)
    assert pg.index[0] == "F1"
    ale = shap_grupos.ale_1d(m.predict, X, "c")
    assert abs(np.average(ale.ale)) < 0.5 and np.corrcoef(ale.ale, np.sin(2 * ale.x))[0, 1] > .8
    assert len(shap_grupos.pdp_1d(m.predict, X, "c")) > 5
    assert shap_grupos.sustituto(m, X)["fidelidad_r2"] > .5
    assert shap_grupos.interacciones_shap(m, X, gr, max_n=60).shape == (4, 4)
    e = shap_grupos.estabilidad_ranking(X, y, gr, B=4, n_pliegues=2)
    assert e["ranking"][0] == "F1" and 0 <= e["pct_ranking_completo_bootstrap"] <= 1


def test_multiverso_registra_todas(tmp_path):
    from econ_utils import Registry
    r = g(10)
    n = 120
    df = pd.DataFrame(r.normal(size=(n, 5)), columns=["y", "x", "c1", "c2", "c3"], index=pd.period_range("1990Q1", periods=n, freq="Q"))
    df["y"] = .5 * df.x + df.c1 + df.y
    rg = Registry(tmp_path / "reg.csv")
    op = {"dep": ["y"], "x": ["x"], "controles": [[], ["c1"], ["c1", "c2"], ["c1", "c2", "c3"]], "muestra": [None, ("1990Q1", "2010Q4")], "hac": [2, 4]}
    specs, trunc, nrej = multiverso.correr_multiverso(df, op, registry=rg, max_specs=100)
    assert nrej == 16 and len(specs) == 16 and not trunc and len(rg.frame()) == 16
    res = multiverso.resumen_multiverso(specs)
    assert res.pct_mismo_signo.iloc[0] == 1.0 and 0.2 < res.mediana.iloc[0] < 0.8
    specs2, trunc2, _ = multiverso.correr_multiverso(df, op, registry=rg, max_specs=5)
    assert trunc2 and len(specs2) == 5 and len(rg.frame()) == 21
