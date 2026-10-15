"""V9 · validación Monte Carlo de src/v9/herramientas.py antes de usarlas (regla V7). SEED fija; tolerancias amplias."""
from pathlib import Path

import numpy as np
from statsmodels.stats.multitest import multipletests

import importlib.util  # noqa: E402

# carga por ruta con nombre propio: src/v7 y src/v8 también tienen un módulo «herramientas» en la misma sesión de pytest
_spec = importlib.util.spec_from_file_location("herramientas_v9", Path(__file__).resolve().parents[2] / "src" / "v9" / "herramientas.py")
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)


def _panel(rng, n=240, T=14, cohortes=((7, 0.3), (9, 0.3)), efecto=lambda e: 0.05 + 0.01 * e, rho=0.0):
    g = np.full(n, np.inf)
    u = rng.random(n)
    acum = 0
    for gg, s in cohortes:
        g[(u >= acum) & (u < acum + s)] = gg
        acum += s
    a = rng.normal(0, 1, n)[:, None]
    b = np.cumsum(rng.normal(0, 0.05, T))[None, :]
    eps = rng.normal(0, 0.1, (n, T))
    for t in range(1, T):
        eps[:, t] += rho * eps[:, t - 1]
    e = np.arange(T)[None, :] - g[:, None]
    tau = np.where(e >= 0, efecto(np.clip(e, 0, None)), 0.0)
    return a + b + tau + eps, g, tau


def _verdad(g, tau, T):
    cel = []
    for gg in np.unique(g[np.isfinite(g)]):
        idx = g == gg
        for t in range(int(gg), T):
            cel.append((idx.sum(), tau[idx, t].mean()))
    w = np.array([c[0] for c in cel], float)
    return float(np.sum(w * np.array([c[1] for c in cel])) / w.sum())


def test_cs_bjs_insesgados_y_cobertura():
    rng = np.random.default_rng(H.SEED)
    sesgo_cs, sesgo_bjs, cubre = [], [], []
    for _ in range(60):
        Y, g, tau = _panel(rng)
        v = _verdad(g, tau, Y.shape[1])
        r = H.cs(Y, g, B=199)
        sesgo_cs.append(r["att"] - v)
        cubre.append(abs(r["att"] - v) <= 1.96 * r["se"])
        sesgo_bjs.append(H.bjs(Y, g, B=29)["att"] - float(tau[tau != 0].mean()))
    assert abs(np.mean(sesgo_cs)) < 0.005
    assert abs(np.mean(sesgo_bjs)) < 0.005
    assert 0.85 <= np.mean(cubre) <= 1.0


def test_pretendencias_y_honest():
    rng = np.random.default_rng(H.SEED + 1)
    rech = []
    for _ in range(60):
        Y, g, _ = _panel(rng)
        rech.append(H.pretendencias(H.cs(Y, g, B=199), -6, -2)[1] < 0.05)
    assert np.mean(rech) <= 0.15          # tamaño razonable sin violación
    Y, g, _ = _panel(rng, efecto=lambda e: 0.2 + 0 * e)
    r = H.cs(Y, g, B=199)
    lo, hi = H.honest_rm(r, 0.0)
    assert lo > 0                          # efecto grande, sin violación: excluye el 0
    assert H.honest_ruptura(r) > 0


def test_dcdh_igual_cs_aun_no():
    rng = np.random.default_rng(H.SEED + 2)
    Y, g, _ = _panel(rng)
    assert abs(H.dcdh(Y, g, B=99)["att"] - H.cs(Y, g, control="aun_no", B=99)["att"]) < 1e-12


def test_twfe_cluster_cobertura():
    rng = np.random.default_rng(H.SEED + 3)
    cub, size = [], []
    for _ in range(80):
        n, T = 200, 12
        x = rng.normal(0, 1, n)
        post = (np.arange(T) >= 6).astype(float)
        D = np.outer(x, post)
        Y = rng.normal(0, 1, (n, 1)) + rng.normal(0, 0.1, (1, T)) + 0.02 * D + rng.normal(0, 0.1, (n, T))
        r = H.twfe_cluster(Y, [D], B=99)
        cub.append(abs(r["beta"][0] - 0.02) <= 1.96 * r["se"][0])
        Y0 = Y - 0.02 * D
        size.append(H.twfe_cluster(Y0, [D], B=99)["p_boot"][0] < 0.05)
    assert 0.85 <= np.mean(cub) <= 1.0
    assert np.mean(size) <= 0.12


def test_iv_y_ar():
    rng = np.random.default_rng(H.SEED + 4)
    ests, cubre_ar = [], []
    for _ in range(150):
        n = 300
        z = rng.normal(0, 1, n)
        v = rng.normal(0, 1, n)
        x = 0.8 * z + v
        y = 1.0 * x + 0.8 * v + rng.normal(0, 1, n)       # endogeneidad
        r = H.iv_just(y, x, z)
        ests.append(r["beta"])
        lo, hi, _ = H.anderson_rubin(r, np.linspace(0, 2, 201))
        cubre_ar.append(lo <= 1.0 <= hi)
        assert r["F_eff"] > 20
    assert abs(np.mean(ests) - 1.0) < 0.05
    assert np.mean(cubre_ar) >= 0.88


def test_akm_cobertura():
    """Shocks aleatorios a nivel de «país» con cuotas comunes: AKM debe cubrir mejor que HC1 ingenuo."""
    rng = np.random.default_rng(H.SEED + 5)
    n, C = 200, 15
    S = rng.dirichlet(np.ones(C) * 0.3, n)
    cub = []
    for _ in range(150):
        g = rng.normal(0, 1, C)
        nu = rng.normal(0, 1, C)                # perturbación a nivel de país (correlaciona residuos)
        z = S @ g
        y = 0.5 * z + S @ nu + rng.normal(0, 0.2, n)
        r = H.iv_just(y, z, z)
        se = H.akm_se(r, S, g, coef="rf")
        cub.append(abs(r["rf"] - 0.5) <= 1.96 * se)
    assert np.mean(cub) >= 0.85


def test_conley_corte_cero_es_hc0():
    rng = np.random.default_rng(H.SEED + 6)
    n = 100
    X = np.column_stack([np.ones(n), rng.normal(0, 1, n)])
    y = X @ np.array([1, 2]) + rng.normal(0, 1, n)
    coords = rng.uniform(0, 1e5, (n, 2))
    r = H.conley(y, X, coords, 0.0)
    assert np.allclose(r["se"] * np.sqrt(n / (n - 2)), r["se_hc1"])


def test_holm_bh():
    p = [0.01, 0.04, 0.03, 0.2]
    assert np.allclose(H.holm(p), multipletests(p, method="holm")[1])
    assert np.allclose(H.bh(p), multipletests(p, method="fdr_bh")[1])


def test_honest_rr_propiedades():
    """IC de RR: contiene θ̂; se ensancha con M̄; sin tendencia previa y efecto grande excluye el 0 con M̄ = 1."""
    pre, post = [-4, -3, -2], [0, 1, 2]
    orden = pre + post
    S = 0.01 ** 2 * np.eye(len(orden))
    b = np.array([0.001, -0.001, 0.0, 0.10, 0.10, 0.10])
    res = {"es_orden": orden, "es": {e: (b[i], 0.01) for i, e in enumerate(orden)}, "es_vcov": S}
    lo0, hi0 = H.honest_rr(res, 0.0, n_sim=200)
    lo1, hi1 = H.honest_rr(res, 1.0, n_sim=200)
    assert lo0 <= 0.10 <= hi0
    assert hi1 - lo1 >= hi0 - lo0 - 1e-9
    assert lo1 > 0
    b2 = np.array([0.03, -0.03, 0.0, 0.01, 0.01, 0.01])        # tendencia previa grande, efecto pequeño
    res2 = {"es_orden": orden, "es": {e: (b2[i], 0.01) for i, e in enumerate(orden)}, "es_vcov": S}
    lo, hi = H.honest_rr(res2, 1.0, n_sim=200)
    assert lo <= 0 <= hi
