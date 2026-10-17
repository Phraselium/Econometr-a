"""V15 fase 4.1 · Tests mínimos del Monte Carlo: determinismo con la semilla (R pequeño) y veredicto con los umbrales de la adenda."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src" / "v15" / "montecarlo"))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

HERRAMIENTAS = ["sdid_placebo_h1h2", "honest_did", "control_sintetico", "akm_municipal", "dfm_bvar_mcs", "westerlund_csardl", "sar_sdm", "wild_webb_v15"]


def test_veredicto_umbrales():
    assert C.veredicto(0.05, 0.95, 2000)["apto"]
    assert C.veredicto(0.04, 0.92, 2000)["apto"] and C.veredicto(0.06, 0.97, 2000)["apto"]
    assert not C.veredicto(0.0, 0.95, 2000)["apto"]                 # conservador extremo
    assert not C.veredicto(0.073, 0.95, 5000)["apto"]               # el 7,3 % de V9 no pasa
    assert not C.veredicto(0.0399, 0.95, 2000)["apto"] and not C.veredicto(0.0601, 0.95, 2000)["apto"]
    assert not C.veredicto(0.05, 0.9199, 2000)["apto"] and not C.veredicto(0.05, 0.9701, 2000)["apto"]
    assert not C.veredicto(0.05, 0.95, 1999)["apto"]                # R < 2.000
    assert C.veredicto(0.05, None, 2000)["apto"]                    # prueba sin IC
    assert C.veredicto(0.10, None, 2000, banda_tam=(0.08, 0.12))["apto"]


def test_flujos_deterministas():
    a = [g.standard_normal(3) for g in C.flujos(1, 4, 7)]
    b = [g.standard_normal(3) for g in C.flujos(1, 4, 7)]
    assert all(np.array_equal(x, y) for x, y in zip(a, b))
    assert not np.array_equal(C.flujos(1, 1, 7)[0].standard_normal(3), C.flujos(2, 1, 7)[0].standard_normal(3))
    assert C.SEED == 20261010


def test_sdid_y_webb_deterministas():
    from src.v15.montecarlo import _comun_panel_v15 as Pn
    import sdid_placebo_h1h2 as S
    est = Pn.estructura_h1()
    P = Pn.armar(est, "74")
    assert len(P["tr"]) == 124 and len(P["co"]) == 74
    r1 = S.una_rep(P, C.rng(1, 1), "S1_H1_74donantes", 0.0, 0.05, 5)
    r2 = S.una_rep(P, C.rng(1, 1), "S1_H1_74donantes", 0.0, 0.05, 5)
    assert np.allclose(r1, r2, equal_nan=True)
    # el placebo literal no es computable con 74 donantes y 124 tratados
    Y, _ = Pn.simular_h1(P, C.rng(1, 2), 0.0, 0.05)
    assert np.isnan(Pn.placebo_se(Y, P["tr"], P["co"], C.rng(1, 3), 5)[0])
    # SDID recupera un efecto grande
    Y, att = Pn.simular_h1(P, C.rng(1, 4), -0.5, 0.01)
    assert abs(Pn.sdid(Y, P["tr"], P["co"])[0] - att) < 0.08


def test_honest_did_determinista():
    import honest_did as H
    P, _ = H.panel_h1()
    res1, att1, _ = H.evento(P, C.rng(2, 1), 0.0, 0.004)
    res2, att2, _ = H.evento(P, C.rng(2, 1), 0.0, 0.004)
    assert att1 == att2 and np.allclose(res1["es_vcov"], res2["es_vcov"])
    assert H.rechaza(res1, 1.0, 0.0) == H.rechaza(res2, 1.0, 0.0)
    # un efecto enorme y sin tendencia se rechaza incluso con M̄ = 1
    res3, _, _ = H.evento(P, C.rng(2, 2), -0.5, 0.0)
    assert H.rechaza(res3, 1.0, 0.0)


def test_control_sintetico_determinista():
    import control_sintetico as CS
    P = CS.estructura()
    a = CS.una(P, C.rng(3, 1), 0.0, 7, True)
    b = CS.una(P, C.rng(3, 1), 0.0, 7, True)
    assert np.allclose(a, b) and len(a) == 10


def test_akm_inversion_coherente():
    import akm_municipal as A
    S, orig = A.estructura()
    D = A.Dis(S, orig, orig)
    o1 = A.trozo(C.rng(4, 1), 5, D, 0.39)
    o2 = A.trozo(C.rng(4, 1), 5, D, 0.39)
    assert np.array_equal(o1, o2, equal_nan=True)
    # AKM0 rechaza b0 si y solo si b0 queda fuera del IC invertido (cuando es acotado)
    g = C.rng(4, 2)
    gk, z, x, eps = A.lote(g, 4, D, 0.39)
    y = 0.01 * x + eps
    b, se, sc, SA, SB, Ak, Bk, F = A.estima(D, gk, z, x, y)
    lo, hi, ac = A.akm0_ic(SA, SB, Ak, Bk)
    for i in range(4):
        if ac[i] and np.isfinite(lo[i]):
            dentro = lo[i] <= 0.01 <= hi[i]
            assert dentro == (not A.akm0_rechaza(SA, SB, Ak, Bk, 0.01)[i])


def test_dfm_mcs_determinista():
    import dfm_bvar_mcs as Dm
    assert Dm.mcs_rep(C.rng(5, 1)) == Dm.mcs_rep(C.rng(5, 1))
    y, X, V = Dm.generar(C.rng(5, 2), 0.5)
    assert y.shape == (Dm.N_TOT,) and X.shape == (Dm.N_TOT, Dm.M_IND) and V.shape == (Dm.N_TOT, 6)
    e = Dm.errores(y, X, V)
    assert e.shape == (Dm.P_OOS, 6) and np.isfinite(e).all()      # 73 errores fuera de muestra
    # sin igualdad de precisión (un modelo muy peor) el MCS lo excluye
    g = C.rng(5, 3)
    L = (g.standard_normal((73, 6))) ** 2
    L[:, 0] *= 30
    assert Dm.mcs(L, (0.1,), g)[0.1] < 6


def test_westerlund_cips_csardl():
    import westerlund_csardl as W
    y, x, beta, speed = W.panel(C.rng(6, 1), True)
    assert y.shape == (W.N, W.T) and -0.07 < speed < -0.01
    s1, s2 = W.west_stats(y, x), W.west_stats(y, x)
    assert np.array_equal(s1, s2) and s1.shape == (4,)
    # con cointegración fuerte el estadístico es más negativo que bajo el nulo
    y0, x0, _, _ = W.panel(C.rng(6, 1), False)
    assert W.west_stats(y, x)[0] < W.west_stats(y0, x0)[0]
    assert np.array_equal(W.west_boot(y, x, C.rng(6, 2), 3), W.west_boot(y, x, C.rng(6, 2), 3))
    assert W.rep_cs(C.rng(6, 3), 5) == W.rep_cs(C.rng(6, 3), 5)


def test_sar_efectos_y_ajuste():
    import sar_sdm as S
    n = 300
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[i, (i - 1) % n] = 1.0
    W = A / A.sum(1, keepdims=True)
    lam = S.autovalores(W, np.sqrt(A.sum(1)))
    assert abs(lam.max() - 1) < 1e-9
    g = C.rng(7, 1)
    X = np.column_stack([np.ones(n), g.standard_normal(n), g.standard_normal(n)])
    M = S.Malla(W, X, "SAR", lam)
    rho = 0.4
    y = np.linalg.solve(np.eye(n) - rho * W, X @ S.BETA + g.standard_normal(n))
    a = S.ajusta(M, y)
    assert abs(a["par"] - rho) < 0.2
    vd, vi = S.verdad_efectos(M, rho)
    assert abs((vd + vi) - S.BETA[1] / (1 - rho)) < 1e-9 and vd >= S.BETA[1] - 1e-12


def test_webb_cierre_algebraico():
    import wild_webb_v15 as WW
    g = C.rng(8, 1)
    n, T = 30, 8
    D = np.zeros((n, T)); D[:12, 4:] = 1
    Y = g.standard_normal((n, T))
    cl = np.arange(n)
    dt, yt = WW.dm2(D), WW.dm2(Y)
    beta, e, sdd, se = WW.twfe_estadisticos(dt, yt, cl, n)
    V = C.webb(g, (n, 4))
    ts = WW.boot_t(dt, yt, cl, n, V, sdd, True, n)
    for b in range(4):
        bs, es, _, ses = WW.twfe_estadisticos(dt, WW.dm2(yt * V[cl, b][:, None]), cl, n)
        assert abs(ts[b] - bs / ses) < 1e-9


def test_resultados_coherentes_con_umbrales():
    """Si ya existen las salidas, el veredicto de cada resultado.json debe poder reproducirse con los umbrales de la adenda."""
    for h in HERRAMIENTAS:
        f = RAIZ / "output" / "v15" / "montecarlo" / h / "resultado.json"
        if not f.exists():
            continue
        r = json.loads(f.read_text(encoding="utf-8"))
        assert r["rama"] == "v15/montecarlo" and "diagnosticos" in r and "estimacion" in r
        assert (f.parent / "tabla.csv").exists()
        assert r["diagnosticos"].get("semilla", C.SEED) == C.SEED
        tab = pd.read_csv(f.parent / "tabla.csv")
        if h == "akm_municipal":
            for _, x in tab.iterrows():
                v = C.veredicto(float(x.tamano_5pct), float(x.cobertura_95), int(x.R))
                assert r["diagnosticos"]["por_inferencia"][x.escenario][x.inferencia]["apto"] == v["apto"]
        if h == "westerlund_csardl":
            for _, x in tab.iterrows():
                cob = None if pd.isna(x.cobertura_95) else float(x.cobertura_95)
                v = C.veredicto(float(x.tamano_5pct), cob, int(x.R_nulo))
                assert r["diagnosticos"]["detalle"][x.herramienta]["apto"] == v["apto"]
