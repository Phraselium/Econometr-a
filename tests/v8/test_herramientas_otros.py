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
    assert o["p"] < .05 and o["modo"] == "enumeracion_completa"
    assert permutacion.n_conjuntos(100, 2, 15) == 71
    o3 = permutacion.permutacion_cortes(permutacion.stat_dif_coef(y, X, 1), n, (33, 66), 10, n_perm=2000)
    assert o3["modo"] == "monte_carlo" and o3["n_perm"] == 2000 and 0 < o3["p"] <= 1


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


# ----------------------------------------------------------------------------- correcciones F3 (H5-H7, H13, H17, H18)
def test_bloque_pw_y_sieve():
    r = g(11)
    n = 200
    e_iid = r.normal(size=n)
    u = np.zeros(n)
    for t in range(1, n):
        u[t] = .85 * u[t - 1] + r.normal()
    assert 2 <= regimenes.longitud_bloque_pw(e_iid) <= regimenes.longitud_bloque_pw(u) <= n // 4
    phi, inn = regimenes.ar_sieve(u)
    assert len(phi) >= 1 and abs(phi[0] - .85) < .15 and abs(inn.mean()) < 1e-10
    z = regimenes.simula_sieve(phi, inn, 300, np.random.default_rng(SEED))
    assert abs(np.corrcoef(z[1:], z[:-1])[0, 1] - .85) < .2


def test_bai_perron_y_umbral_con_bootstrap_dependiente():
    r = g(12)
    n = 100
    y = np.r_[r.normal(0, 1, 50), r.normal(2.5, 1, 50)]
    for boot in ("bloque", "sieve"):
        o = regimenes.bai_perron(y, max_cortes=2, B=49, boot=boot)
        assert o["p_UDmax"] < .1 and o["boot"] == boot
    assert regimenes.bai_perron(y, max_cortes=2, B=19, boot="block")["boot"] == "bloque"  # alias
    x, q = r.normal(size=n), r.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    yu = 1 + np.where(q > 0, 1.5, .1) * x + r.normal(size=n) * .6
    for boot in ("bloque", "sieve"):
        o = regimenes.umbral_hansen(yu, X, q, B=99, boot=boot)
        assert o["p_linealidad"] < .1 and abs(o["gamma"]) < .6
    # mismas semillas -> mismo resultado (determinismo)
    a = regimenes.umbral_hansen(yu, X, q, B=49, boot="sieve", seed=5)["p_linealidad"]
    assert a == regimenes.umbral_hansen(yu, X, q, B=49, boot="sieve", seed=5)["p_linealidad"]


def _dgp_iv(seed, n=200, beta=1.0, contaminada=False):
    r = g(seed)
    N = n + 50
    z, v = r.normal(size=N), r.normal(size=N)
    u = .7 * v + .7 * r.normal(size=N)
    if contaminada:
        z = z + .8 * np.r_[0.0, u[:-1]]
    x = z + v
    y = np.zeros(N)
    for t in range(1, N):
        y[t] = .5 * y[t - 1] + beta * x[t] + u[t]
    return y[50:], x[50:], z[50:]


def test_lp_horizontes_negativos_y_agregado():
    y, x, z = _dgp_iv(20)
    o = lp.lp(y, x - 0.0, H=2, H_min=-3, rezagos=2)
    assert list(o.h) == [-3, -2, -1, 0, 1, 2]
    pre = o[o.h < 0]
    assert (pre.beta.abs() / pre.se).max() < 3.5  # sin pretendencia en el DGP (instrumento exogeno; OLS tiene sesgo solo en h>=0)
    oa = lp.lp(y, x, H=2, H_min=-3, rezagos=2, acumulado=True)
    assert -1 not in list(oa.h)  # h=-1 acumulado es identicamente 0
    iv = lp.lp_iv(y, x, z, H=1, H_min=-2, grid_n=401)
    assert list(iv.h) == [-2, -1, 0, 1] and (iv.ar_p_dos.iloc[:2] > .01).all()
    ag = lp.lp_agregado(y, x, hs=(4, 8))
    ivag = lp.lp_iv_agregado(y, x, z, hs=(4, 8), grid_n=401)
    assert ag.h.iloc[0] == "4-8" and ivag.ar_lo.iloc[0] <= np.mean([.5 ** h for h in range(4, 9)]) <= ivag.ar_hi.iloc[0] + .3
    # EWC y ancho de banda mayor devuelven IC mas anchos que NW(h+1) o comparables, nunca mas estrechos que el 70 %
    a = lp.lp(y, x, H=4, hac="h+1").se.values
    assert (lp.lp(y, x, H=4, hac="2h+2").se.values > .7 * a).all() and (lp.lp(y, x, H=4, ewc=True).se.values > .5 * a).all()


def test_ar_p_unilateral_y_consistencia():
    y, x, z = _dgp_iv(21, beta=-1.0)
    dos = lp.ar_p(y, x, z, 0, b0=0.0, lado="dos")
    menor = lp.ar_p(y, x, z, 0, b0=0.0, lado="menor")
    mayor = lp.ar_p(y, x, z, 0, b0=0.0, lado="mayor")
    assert menor < 1e-4 and mayor > .99 and abs(menor + mayor - 1) < 1e-9 and dos < 1e-3  # efecto -1: rechaza H0 contra beta<0
    # coherencia con el conjunto AR: b0 dentro del intervalo => p_dos > 0,05; fuera => < 0,05
    row = lp.lp_iv(y, x, z, H=0, grid_n=801).iloc[0]
    assert lp.ar_p(y, x, z, 0, b0=(row.ar_lo + row.ar_hi) / 2) > .05 and lp.ar_p(y, x, z, 0, b0=row.ar_hi + 1.0) < .05
    assert abs(row.ar_p_dos - dos) < 1e-12 and abs(row.ar_p_menor - menor) < 1e-12
    # agregado: misma funcion con `agregado`
    pa = lp.ar_p(y, x, z, 0, b0=0.0, lado="menor", agregado=(4, 8))
    assert 0 <= pa <= 1


def test_placebo_permutacion_iv():
    y, x, z = _dgp_iv(22, n=150)
    o = lp.placebo_permutacion_iv(y, x, z, h=0, n_perm=199)
    assert o["p_perm"] < .02 and o["beta_perm_q025"] < 0 < o["beta_perm_q975"]
    y0, x0, z0 = _dgp_iv(23, n=150, beta=0.0)
    assert lp.placebo_permutacion_iv(y0, x0, z0, h=0, n_perm=199)["p_perm"] > .05
    o2 = lp.placebo_permutacion_iv(y, x, z, agregado=(4, 8), n_perm=99, modo="desplazamiento")
    assert 0 < o2["p_perm"] <= 1 and o2["modo"] == "desplazamiento"
    # determinista
    assert lp.placebo_permutacion_iv(y, x, z, h=2, n_perm=49)["p_perm"] == lp.placebo_permutacion_iv(y, x, z, h=2, n_perm=49)["p_perm"]


def test_permutacion_tramos_no_contiguos():
    r = g(13)
    n = 126
    tr = ((0, 28), (32, 58), (58, 80), (80, 106), (108, 126))
    assert permutacion.cortes_a_tramos((60,), 100) == ((0, 60), (60, 100))
    assert permutacion.n_conjuntos_tramos(n, tr, 8) == __import__("math").comb(sum(b - a for a, b in tr) - 40 + 4, 4)
    x = r.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    b = np.full(n, .3)
    b[58:106] = 1.5
    y = 1 + b * x + r.normal(size=n) * .6
    for fab in (permutacion.stat_Q_tramos, permutacion.stat_maxt_tramos):
        o = permutacion.permutacion_tramos(fab(y, X, 1), n, tr, 8, n_perm=299)
        assert o["modo"] == "monte_carlo" and o["n_perm"] == 299 and o["p"] <= 0.2
    # los conjuntos aleatorios respetan huecos y longitud minima
    vistos = []
    permutacion.permutacion_tramos(lambda t: vistos.append(t) or 0.0, n, tr, 8, n_perm=50)
    for t in vistos[1:]:
        assert len(t) == 5 and all(b_ - a_ >= 8 for a_, b_ in t) and t[0][0] == 0
        assert [t[i + 1][0] - t[i][1] for i in range(4)] == [4, 0, 0, 2] and t[-1][1] == 126 - 2 + 2 - 0
    # H0 pequeno: enumeracion completa
    o = permutacion.permutacion_tramos(permutacion.stat_Q_tramos(y, X, 1), 40, ((0, 15), (17, 40)), 10, n_perm=5000)
    assert o["modo"] == "enumeracion_completa"
    # el texto ya no afirma exactitud
    assert "exacto" not in permutacion.__doc__.split("VALIDEZ")[0]
    try:
        permutacion.permutacion_tramos(lambda t: 0.0, n, tr, 25)
        raise AssertionError("debia fallar: tramo observado mas corto que min_len")
    except ValueError:
        pass


def test_multiverso_tope_y_fallidas(tmp_path):
    from econ_utils import Registry
    import inspect
    assert inspect.signature(multiverso.correr_multiverso).parameters["max_specs"].default == 50_000
    r = g(14)
    n = 60
    df = pd.DataFrame(r.normal(size=(n, 3)), columns=["y", "x", "c1"], index=pd.period_range("1990Q1", periods=n, freq="Q"))
    rg = Registry(tmp_path / "reg.csv")
    op = {"dep": ["y"], "x": ["x"], "controles": [[], ["c1"]], "muestra": [None, ("1990Q1", "1991Q4")], "hac": [2]}
    specs, trunc, nrej = multiverso.correr_multiverso(df, op, registry=rg)
    fal = specs.attrs["fallidas"]
    assert nrej == 4 and len(specs) == 2 and len(fal) == 2 and not trunc
    assert fal.motivo.str.contains("muestra insuficiente").all()
    reg = rg.frame()
    assert len(reg) == 4 and reg.notas.str.startswith("FALLIDA").sum() == 2


def test_f3_out_redirige_salida(tmp_path, monkeypatch):
    import importlib
    monkeypatch.setenv("F3_OUT", str(tmp_path / "salida"))
    m = importlib.import_module("src.v8.f3_montecarlo_otros")
    m = importlib.reload(m)
    assert m.OUT == tmp_path / "salida"


def test_etiquetas_derivadas_por_reglas():
    import importlib
    m = importlib.import_module("src.v8.f3_montecarlo_otros")
    m.FILAS.clear()
    m.reg("h", "c1", "e", "m", 0.05, "tamano", 10)
    m.reg("h", "c1", "e", "m2", 0.70, "potencia", 10)
    m.reg("h", "c2", "e", "m", 0.12, "tamano", 10)
    m.reg("h", "c3", "e", "m", 0.40, "tamano", 10)
    m.reg("h", "c4", "e", "m", 0.40, "tamano", 10, rol="referencia")
    df = pd.DataFrame(m.FILAS)
    m.FILAS.clear()
    E = m.etiquetas(df).set_index("config")
    assert E.loc["c1", "validez"] == "apta" and E.loc["c1", "potencia"] == "con reservas"
    assert E.loc["c2", "validez"] == "con reservas" and E.loc["c3", "validez"] == "no apta" and "c4" not in E.index
    assert "0,400" in E.loc["c3", "incumple"]
