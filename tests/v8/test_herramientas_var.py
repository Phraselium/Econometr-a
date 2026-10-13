"""V8-F3 (familia VAR): tests rapidos de bvar, signos y tvp con datos simulados y versiones reducidas."""
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v8"))
from herramientas import bvar, signos, tvp  # noqa: E402

VARS = ["y", "pi", "cred", "tipo"]
SHOCKS = ["oferta", "demanda", "credito", "monetario"]
A0 = np.array([[1.0, 0.8, 0.5, -0.6], [-0.5, 0.6, 0.3, -0.4], [0.2, 0.4, 1.0, -0.5], [0.1, 0.5, 0.2, 0.8]])


def _datos(T=80, n=4, seed=11, imp=None):
    rg = np.random.default_rng(seed)
    imp = np.eye(n) if imp is None else imp
    A1, A2 = 0.5 * np.eye(n), -0.1 * np.eye(n)
    Y = np.zeros((T + 50, n))
    for t in range(2, T + 50):
        Y[t] = A1 @ Y[t - 1] + A2 @ Y[t - 2] + imp @ rg.standard_normal(n)
    return Y[50:]


def _restr(ceros):
    r = signos.Restricciones(VARS, SHOCKS)
    r.signo("y", "oferta", 1).signo("pi", "oferta", -1)
    r.signo("y", "demanda", 1).signo("pi", "demanda", 1).signo("tipo", "demanda", 1)
    r.signo("cred", "credito", 1).signo("y", "credito", 1).signo("pi", "credito", 1)
    r.signo("tipo", "monetario", 1).signo("pi", "monetario", -1).signo("cred", "monetario", -1)
    if ceros:
        r.cero("y", "monetario", 0).cero("tipo", "oferta", 0)
    else:
        r.signo("y", "monetario", -1)
    return r


def test_bvar_formas_semilla_y_logml():
    Y = _datos(70, 4)
    post = bvar.estimar(Y, 2)
    assert post["B"].shape == (9, 4) and 0.005 <= post["lam"] <= 20
    assert abs(post["logml"] - bvar.logml(Y, 2, post["lam"])) < 1e-9
    # el optimo no es peor que sus vecinos
    assert post["logml"] >= bvar.logml(Y, 2, post["lam"] * 1.5) - 1e-6 and post["logml"] >= bvar.logml(Y, 2, post["lam"] / 1.5) - 1e-6
    B1, S1 = bvar.muestrear(post, 20, np.random.default_rng(1))
    B2, S2 = bvar.muestrear(post, 20, np.random.default_rng(1))
    assert B1.shape == (20, 9, 4) and S1.shape == (20, 4, 4)
    assert np.array_equal(B1, B2) and np.array_equal(S1, S2)
    I, b = bvar.irf(post, 8, 50, np.random.default_rng(2))
    assert I.shape == (50, 9, 4, 4) and np.all(b["lo90"] <= b["lo68"] + 1e-12) and np.all(b["hi68"] <= b["hi90"] + 1e-12)
    assert np.allclose(I[:, 0], np.linalg.cholesky(bvar.muestrear(post, 50, np.random.default_rng(2))[1]), atol=1e-10)
    assert bvar.prediccion(post, 5, 30, np.random.default_rng(3)).shape == (30, 5, 4)


def test_bvar_dummies_y_cadena_predictiva():
    from scipy import stats
    Y = _datos(40, 3, 5)
    post = bvar.estimar(Y, 2, soc=True, io=True)
    assert post["mu"] > 0 and post["theta"] > 0
    pr = bvar._prior_completo(Y, 2, 0.3, 0.8, 1.5, 1.0, 2.0, True, bvar._psi_ar(Y, 2))
    yy, X = bvar.retardos(Y, 2)
    cur, tot = pr, 0.0
    for t in range(len(yy)):
        x = X[t:t + 1]
        po = bvar._actualizar(cur, yy[t:t + 1], x)
        dfp = cur["nu0"] - 3 + 1
        sc = cur["S0"] / dfp * (1 + (x @ np.linalg.inv(cur["Oinv"]) @ x.T)[0, 0])
        tot += stats.multivariate_t.logpdf(yy[t], (x @ cur["B0"])[0], sc, df=dfp)
        cur = dict(B0=po["B0"], Oinv=po["Oinv"], S0=po["S0"], nu0=po["nu0"])
    assert abs(tot - bvar.logml_prior(pr, yy, X)) < 1e-8


def _identificar(ceros, seed=7, n_obj=15):
    Y = _datos(80, 4, 21, A0 if not ceros else _a0_ceros())
    rg = np.random.default_rng(seed)
    post = bvar.estimar(Y, 2)
    B, S = bvar.muestrear(post, 150, rg)
    r = _restr(ceros)
    return Y, r, signos.identificar(B, S, 4, 2, r, H=20, n_objetivo=n_obj, rng=rg)


def _a0_ceros():
    a = A0.copy()
    a[0, 3] = 0.0
    a[3, 0] = 0.0
    return a


def test_signos_cumple_y_descomposicion_historica_identidad():
    Y, r, res = _identificar(False)
    assert len(res["Q"]) == 15 and res["irf"].shape == (15, 21, 4, 4)
    mz, fs = signos.comprobar(res, r)
    assert fs == 1.0
    assert np.allclose(res["peso"], 1 / 15)  # sin ceros no hay pesos de importancia
    Q = res["Q"]
    assert np.allclose(Q @ Q.transpose(0, 2, 1), np.eye(4), atol=1e-10)
    hd = signos.descomposicion_historica(res, Y)
    assert hd["contrib"].shape == (15, 78, 4, 4) and hd["error"] < 1e-8
    fv = signos.fevd(res["irf"])
    assert fv.shape == (15, 4, 4, 4) and np.allclose(fv.sum(-1), 1.0)
    rs = signos.resumen(res)
    assert rs["irf"]["med"].shape == (21, 4, 4) and np.all(rs["irf"]["lo68"] <= rs["irf"]["hi68"])
    # tramos: la suma de todos los tramos que cubren la muestra = suma total
    fechas = np.arange(78)
    tr = signos.sumar_tramos(hd["contrib"], fechas, [(0, 29), (30, 77)])
    assert tr.shape == (15, 2, 4, 4) and np.allclose(tr.sum(1), hd["contrib"].sum(1))
    hb = signos.historica_bandas(hd, res["peso"], fechas, [(0, 29), (30, 77)])
    assert hb["med"].shape == (2, 4, 4)


def test_ceros_exactos_y_pesos():
    Y, r, res = _identificar(True)
    mz, fs = signos.comprobar(res, r)
    assert mz < 1e-10 and fs == 1.0
    assert abs(res["peso"].sum() - 1) < 1e-12 and res["ess"] > 1
    assert np.all(np.abs(res["irf"][:, 0, 0, 3]) < 1e-10) and np.all(np.abs(res["irf"][:, 0, 3, 0]) < 1e-10)
    hd = signos.descomposicion_historica(res, Y)
    assert hd["error"] < 1e-8


def test_signos_reproducible_con_semilla():
    _, _, r1 = _identificar(True, seed=3, n_obj=5)
    _, _, r2 = _identificar(True, seed=3, n_obj=5)
    _, _, r3 = _identificar(True, seed=4, n_obj=5)
    assert np.array_equal(r1["irf"], r2["irf"]) and np.array_equal(r1["peso"], r2["peso"])
    assert not np.array_equal(r1["irf"], r3["irf"])


def test_orden_de_ceros_inadmisible():
    r = signos.Restricciones(VARS, SHOCKS)
    for i in range(3):
        r.cero(i, "oferta", 0)
        r.cero(i, "demanda", 0)
    try:
        r.orden_shocks()
        raise AssertionError("debia fallar")
    except ValueError:
        pass


def test_tvp_formas_y_semilla():
    Y = _datos(70, 3, 9)
    kw = dict(p=2, tau=25, n_iter=40, burn=20, thin=2)
    a = tvp.estimar(Y, rng=np.random.default_rng(1), **kw)
    b = tvp.estimar(Y, rng=np.random.default_rng(1), **kw)
    T = 70 - 2 - 25
    assert a["beta"].shape == (10, T, 21) and a["h"].shape == (10, T, 3) and a["a"].shape == (10, T, 3)
    assert np.array_equal(a["beta"], b["beta"])
    assert tvp.trayectoria(a, 0, 0, 1).shape == (10, T) and np.all(tvp.volatilidad(a) > 0)
    assert tvp.irf_en(a, T - 1, 6).shape == (10, 7, 3, 3)
    assert np.all(np.isfinite(a["beta"]))


# ------------------------------------------------------------ correcciones de la revision F3 (H2, H4, H9, H10)
def _exog(T, idx):
    X = np.zeros((T, len(idx)))
    for k, ii in enumerate(idx):
        X[ii, k] = 1.0
    return X


def test_exog_retardos_estimar_y_prediccion():
    Y = _datos(70, 4, 31)
    X = _exog(70, [[20, 21, 22], [40]])
    Y = Y + X @ np.array([[2.0, 0, -1.5, 0], [0, 1.0, 0, 0.0]])
    yy, XX = bvar.retardos(Y, 2, True, X)
    assert XX.shape == (68, 4 * 2 + 2 + 1) and np.array_equal(XX[:, -1], np.ones(68)) and np.array_equal(XX[:, 8:10], X[2:])
    post = bvar.estimar(Y, 2, exog=X)
    assert post["B"].shape == (11, 4) and post["m"] == 2
    # la ficticia recupera el efecto (prior laxo) y la constante sigue en la ultima fila
    assert abs(post["B"][8, 0] - 2.0) < 1.0 and abs(post["B"][9, 1] - 1.0) < 1.5
    assert abs(post["logml"] - bvar.logml(Y, 2, post["lam"], exog=X)) < 1e-9
    A, c = bvar.coef_matrices(post["B"][None], 4, 2, 2)
    assert np.allclose(c[0], post["B"][10]) and bvar.coef_exog(post["B"][None], 4, 2, 2).shape == (1, 2, 4)
    pr = bvar.prediccion(post, 4, 20, np.random.default_rng(3), exog_futuro=np.zeros((4, 2)))
    assert pr.shape == (20, 4, 4)
    # con dummies SOC/IO el prior sigue siendo conjugado y la ml finita
    assert np.isfinite(bvar.estimar(Y, 2, soc=True, io=True, exog=X)["logml"])


def test_dh_identidad_con_exogenas():
    Y = _datos(80, 4, 21, A0)
    X = _exog(80, [[30, 31, 32], [50]])
    Y = Y + X @ np.array([[3.0, 0, -2.0, 0], [0, 0, 1.0, 0.0]])
    rg = np.random.default_rng(5)
    post = bvar.estimar(Y, 2, exog=X)
    B, S = bvar.muestrear(post, 100, rg)
    r = _restr(False)
    res = signos.identificar(B, S, 4, 2, r, H=10, n_objetivo=10, rng=rg)
    hd = signos.descomposicion_historica(res, Y, exog=X)
    assert hd["error"] < 1e-8 and hd["contrib"].shape[1] == 78
    assert np.max(np.abs(hd["det_exog"])) > 0.1          # las exogenas entran en la parte determinista
    # sin exogenas, det_exog es 0 y la identidad sigue valiendo
    post0 = bvar.estimar(Y, 2)
    B0, S0 = bvar.muestrear(post0, 100, rg)
    res0 = signos.identificar(B0, S0, 4, 2, r, H=10, n_objetivo=10, rng=rg)
    hd0 = signos.descomposicion_historica(res0, Y)
    assert hd0["error"] < 1e-8 and np.all(hd0["det_exog"] == 0)


def test_delta_vector_y_por_defecto_cero():
    pr = bvar.prior_minnesota(3, 2, 0.5, np.ones(3), delta=np.array([0.0, 0.5, 1.0]))
    assert np.allclose(np.diag(pr["B0"][:3]), [0.0, 0.5, 1.0])
    assert np.all(bvar.prior_minnesota(3, 2, 0.5, np.ones(3))["B0"] == 0.0)
    Y = _datos(60, 3, 7)
    a, b = bvar.estimar(Y, 2, lam=0.3), bvar.estimar(Y, 2, lam=0.3, delta=np.array([0.0, 0.0, 0.0]))
    assert np.allclose(a["B"], b["B"]) and abs(a["logml"] - b["logml"]) < 1e-12
    c = bvar.estimar(Y, 2, lam=0.3, delta=np.array([0.0, 0.0, 1.0]))
    assert not np.allclose(a["B"], c["B"]) and np.isfinite(c["logml"])


def test_signos_rotaciones_fijas_por_theta():
    Y = _datos(80, 4, 21, A0)
    rg = np.random.default_rng(9)
    post = bvar.estimar(Y, 2)
    B, S = bvar.muestrear(post, 12, rg)
    r = _restr(False)
    res = signos.identificar(B, S, 4, 2, r, H=4, rotaciones=300, rng=rg)
    assert res["rot_total"] == 12 * 300 and res["n_sorteos_usados"] == 12       # nunca reintenta hasta aceptar
    assert 0.0 <= res["frac_theta_acept"] <= 1.0
    # una sola rotacion por theta (sin reintentar): como mucho una aceptada por theta
    r1 = signos.identificar(B, S, 4, 2, r, H=4, rotaciones=1, rng=np.random.default_rng(1))
    assert r1["rot_total"] == 12 and len(r1["Q"]) <= 12
    # con rotaciones suficientes un mismo theta puede aportar varias aceptadas
    res2 = signos.identificar(B[:1], S[:1], 4, 2, r, H=4, rotaciones=20000, rng=np.random.default_rng(2))
    assert len(res2["Q"]) > 1 and len(set(res2["idx"].tolist())) == 1


def test_var_regimenes_tramos_con_huecos():
    Y = _datos(90, 3, 4)
    res = tvp.var_regimenes(Y, 2, tramos=[(0, 20), (22, 50), (55, 88)])
    assert [r["T"] for r in res["regimenes"]] == [20, 28, 33] and res["segs"] == [(0, 20), (22, 50), (55, 88)]
    # contiguo con tramos == con cortes
    a = tvp.var_regimenes(Y, 2, tramos=[(0, 40), (40, 88)], lam=0.4)
    b = tvp.var_regimenes(Y, 2, [40], lam=0.4)
    assert np.allclose(a["regimenes"][1]["B"], b["regimenes"][1]["B"])
    d = tvp.diferencia_regimenes(res, 0, 2, 0, 0, 1, 50, np.random.default_rng(1))
    assert d.shape == (50,)
    try:
        tvp.var_regimenes(Y, 2, tramos=[(0, 30), (20, 50)])
        raise AssertionError("debia fallar")
    except AssertionError as e:
        assert "solapados" in str(e)
