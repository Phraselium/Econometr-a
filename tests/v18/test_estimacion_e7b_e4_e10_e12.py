"""V18 · fase 4 · E7-R3/A1 (BVAR), E4, E10, E11 y E12 (src/v18/estimacion/{e7_bvar_lib,e7_bvar,e4_e10_e12}.py y src/v18/montecarlo/bvar.py).

Los tests de núcleo usan datos simulados con SEED 20261010; los de salida (si existen) comprueban las cifras V18 de output/v18/estimacion/{e7_bvar,e4,e10,e11,e12}
con las mismas reglas que check_v18 (id V18-, capa C4, clase válida, sin lenguaje causal), la unicidad de los ids frente a E7 y la coherencia con el veredicto del Monte Carlo.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "estimacion"))
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ))
import e4_e10_e12 as E  # noqa: E402
import e7_bvar_lib as B  # noqa: E402

SEED = 20261010
CLASES = {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
CAUSAL = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)
OUT = RAIZ / "output" / "v18" / "estimacion"
MODULOS = ["e7_bvar", "e4", "e10", "e11", "e12"]


# ---------------------------------------------------------------------------------------------- BVAR
def _var_sim(rng, T=400, n=3):
    A = np.array([[0.5, 0.0, 0.0], [0.3, 0.4, 0.0], [0.0, 0.2, 0.3]])
    P = np.array([[1.0, 0, 0], [0.3, 1.0, 0], [0.2, 0.1, 1.0]])
    Y = np.zeros((T + 50, n))
    u = rng.standard_normal((T + 50, n)) @ P.T
    for t in range(1, T + 50):
        Y[t] = A @ Y[t - 1] + u[t]
    return Y[50:], A, P


def test_ficticias_dimensiones_y_posterior():
    rng = np.random.default_rng(SEED)
    Y, _, _ = _var_sim(rng, 120)
    post = B.ajustar(Y, (np.arange(120) % 4) + 1, 2, 0.2, 0.5, np.ones(3))
    assert post["B"].shape == (2 * 3 + 1 + 3, 3) and post["S"].shape == (3, 3)
    assert post["nu"] > 3 and post["filas"] == 118
    Bd, Sg = B.sacar(post, 50, rng)
    assert Bd.shape == (50, 10, 3) and np.all(np.linalg.eigvalsh(Sg).min(axis=1) > 0)


def test_irf_normalizada_impacto_uno_y_recupera_la_verdadera_con_prior_difuso():
    rng = np.random.default_rng(SEED)
    Y, A, P = _var_sim(rng, 800)
    post = B.ajustar(Y, None, 1, 50.0, 0.0, np.ones(3))
    Bd, Sg = B.sacar(post, 400, rng)
    R = B.irf(Bd, Sg, 3, 1, 6, 1)
    assert np.allclose(R[:, 0, 1], 1.0)                          # impacto del choque en su propia variable = 1
    ver = np.linalg.matrix_power(A, 4) @ P[:, 1] / P[1, 1]
    med = np.median(R[:, 4, :], axis=0)
    assert np.all(np.abs(med - ver) < 0.12)


def test_prior_estrecho_encoge_hacia_el_paseo_aleatorio():
    rng = np.random.default_rng(SEED)
    Y, _, _ = _var_sim(rng, 60)
    Y = Y + np.array([5.0, 5.0, 5.0])
    flojo = B.ajustar(Y, None, 1, 50.0, 0.0, np.ones(3))["B"][:3, :]
    firme = B.ajustar(Y, None, 1, 0.05, 0.0, np.ones(3))["B"][:3, :]
    assert np.abs(firme - np.eye(3)).sum() < np.abs(flojo - np.eye(3)).sum()


def test_omitir_y_huecos_reducen_filas():
    rng = np.random.default_rng(SEED)
    Y, _, _ = _var_sim(rng, 80)
    Y[30, 1] = np.nan
    om = np.zeros(80, bool)
    om[50:60] = True
    p0 = B.ajustar(Y, None, 2, 0.2, 0.5, np.ones(3))
    p1 = B.ajustar(Y, None, 2, 0.2, 0.5, np.ones(3), omitir=om)
    assert p0["filas"] == 78 - 3 and p1["filas"] == p0["filas"] - 10


def test_raiz_maxima_de_un_var_estable():
    rng = np.random.default_rng(SEED)
    Y, _, _ = _var_sim(rng, 500)
    post = B.ajustar(Y, None, 1, 50.0, 0.0, np.ones(3))
    Bd, _ = B.sacar(post, 20, rng)
    assert np.all(B.raiz_maxima(Bd, 3, 1) < 1.0)


# ---------------------------------------------------------------------------------------------- inferencia de E10 y E12
def _panel(rng, n=30, T=15, beta=0.0, pi=1.0):
    z = rng.standard_normal((n, T))
    v = rng.standard_normal((n, T))
    u = 0.5 * v + rng.standard_normal((n, T))
    x = pi * z + v
    y = beta * x + u
    return y, x, z


def test_iv_cluster_recupera_beta_y_el_ar_contiene_la_verdad():
    rng = np.random.default_rng(SEED)
    y, x, z = _panel(rng, 40, 15, beta=2.0, pi=1.0)
    n, T = y.shape
    W = np.hstack([np.kron(np.eye(n), np.ones((T, 1))), np.kron(np.ones((n, 1)), np.eye(T)[:, 1:])])
    r = E.iv_cluster(y.reshape(-1), x.reshape(-1), z.reshape(-1), W, np.repeat(np.arange(n), T), n)
    assert abs(r["beta"] - 2.0) < 0.35 and r["F_efectivo"] > 10
    assert r["ar"][0] == "intervalo" and r["ar"][1] < 2.0 < r["ar"][2]


def test_webb_bajo_el_nulo_no_rechaza_demasiado_y_con_efecto_si_rechaza():
    rng = np.random.default_rng(SEED)
    rech = 0
    for k in range(40):
        y, x, z = _panel(np.random.default_rng(SEED + k), 30, 10, beta=0.0)
        n, T = y.shape
        W = np.hstack([np.kron(np.eye(n), np.ones((T, 1))), np.kron(np.ones((n, 1)), np.eye(T)[:, 1:])])
        cl = np.repeat(np.arange(n), T)
        rech += E.wcr_forma_reducida(y.reshape(-1), z.reshape(-1), W, cl, n, 199, rng)["p_webb"] < 0.05
    assert rech <= 6                                              # tamaño ≈ 5 % con 40 réplicas (cota holgada)
    y, x, z = _panel(np.random.default_rng(SEED), 30, 10, beta=1.0)
    n, T = y.shape
    W = np.hstack([np.kron(np.eye(n), np.ones((T, 1))), np.kron(np.ones((n, 1)), np.eye(T)[:, 1:])])
    p = E.wcr_forma_reducida(y.reshape(-1), z.reshape(-1), W, np.repeat(np.arange(n), T), n, 499, rng)["p_webb"]
    assert p < 0.02


def test_mde_crece_con_el_ruido_y_es_reproducible():
    rng = np.random.default_rng(SEED)
    n, T = 30, 12
    z = rng.standard_normal(n * T)
    cl = np.repeat(np.arange(n), T)
    y1 = rng.standard_normal(n * T)
    m1 = E.mde_forma_reducida(z, y1, cl, n, 300)["mde_gamma"]
    m2 = E.mde_forma_reducida(z, 3 * y1, cl, n, 300)["mde_gamma"]
    assert m2 > 2.5 * m1 and m1 == E.mde_forma_reducida(z, y1, cl, n, 300)["mde_gamma"]


def test_moran_detecta_dependencia_espacial():
    rng = np.random.default_rng(SEED)
    c = rng.uniform(0, 100, (300, 2))
    suave = np.sin(c[:, 0] / 15) + 0.2 * rng.standard_normal(300)
    ruido = rng.standard_normal(300)
    assert E.moran(suave, c, 8, 199)["I"] > 0.4
    assert abs(E.moran(ruido, c, 8, 199)["I"]) < 0.15


def test_conley_con_corte_pequeno_se_parece_a_hc():
    rng = np.random.default_rng(SEED)
    c = rng.uniform(0, 1000, (400, 2))
    x = rng.standard_normal(400)
    y = 0.3 * x + rng.standard_normal(400)
    r = E.conley_fwl(x - x.mean(), y - y.mean(), c, 0.01)
    e = (y - y.mean()) - (x @ y / (x @ x)) * (x - x.mean())
    hc0 = np.sqrt(((x - x.mean()) ** 2 * e ** 2).sum()) / ((x - x.mean()) @ (x - x.mean()))
    assert abs(r["se_conley"] - hc0) / hc0 < 0.05


# ---------------------------------------------------------------------------------------------- reglas de acceso
def test_sin_acceso_a_datos_sellados_ni_evaluate():
    for f in ("e7_bvar_lib.py", "e7_bvar.py", "e4_e10_e12.py"):
        s = (RAIZ / "src" / "v18" / "estimacion" / f).read_text(encoding="utf-8")
        assert not re.search(r"evaluate_\w+\s*\(", s) and not re.search(r"sellar_\w+\s*\(", s)
        assert "open(" not in s or "data/sealed" not in s
        assert not re.search(r"read_\w+\([^)]*sealed", s)
    s = (RAIZ / "src" / "v18" / "estimacion" / "e4_e10_e12.py").read_text(encoding="utf-8")
    assert "sellado.filtrar" in s or "D.sellado.filtrar" in s


def test_montecarlo_bvar_declara_criterio_y_semilla():
    s = (RAIZ / "src" / "v18" / "montecarlo" / "bvar.py").read_text(encoding="utf-8")
    assert "ALCANCE_TERRITORIAL = \"sin lectura de datos\"" in s and "BANDA68, BANDA90 = (0.63, 0.73), (0.87, 0.93)" in s
    assert "read_parquet" not in s and "hechos.parquet" not in s


# ---------------------------------------------------------------------------------------------- salidas
def _hechos(m):
    p = OUT / m / "hechos.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


@pytest.mark.parametrize("m", MODULOS)
def test_salida_hechos_reglas_de_check_v18(m):
    h = _hechos(m)
    if h is None:
        pytest.skip(f"sin salida de {m}")
    assert h, f"{m}: hechos vacíos"
    ids = [x["id"] for x in h]
    assert len(ids) == len(set(ids))
    for x in h:
        assert x["id"].startswith(f"V18-{m.upper().replace('_BVAR', '')}-") and x["capa"] == "C4" and x["clasificacion_v18"] in CLASES
        assert x["fuentes"] and not CAUSAL.search(f"{x['indicador']} {x['nota']}")
        assert "análisis V18; capa C4; pre-registro interno plan-replicacion-v18" in x["nota"]


@pytest.mark.parametrize("m", MODULOS)
def test_salida_ficheros_y_resultado_json(m):
    d = OUT / m
    if not (d / "resultado.json").exists():
        pytest.skip(f"sin salida de {m}")
    for f in ("resultado.json", "tabla.csv", "informe.md", "hechos.json", "registro.csv"):
        assert (d / f).exists(), f"{m}/{f}"
    r = json.loads((d / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas", "clasificacion_v18"):
        assert k in r, f"{m}: falta {k}"
    assert r["capa"] == "C4" and r["nivel_evidencia"] == "EXPLORATORIO" and r["clasificacion_v18"] in CLASES
    assert "análisis V18; capa C4; pre-registro interno plan-replicacion-v18" in (d / "informe.md").read_text(encoding="utf-8")


def test_ids_de_e7_bvar_distintos_de_los_de_e7():
    a, b = _hechos("e7_bvar"), _hechos("e7")
    if a is None or b is None:
        pytest.skip("sin salidas")
    assert not ({x["id"] for x in a} & {x["id"] for x in b})
    assert {"V18-E7-R3", "V18-E7-A1"} <= {x["id"] for x in a}


def test_e7_bvar_coherente_con_el_veredicto_del_montecarlo():
    mc = RAIZ / "output" / "v18" / "montecarlo" / "bvar" / "resultado.json"
    rj = OUT / "e7_bvar" / "resultado.json"
    if not mc.exists() or not rj.exists():
        pytest.skip("sin salidas")
    v = json.loads(mc.read_text(encoding="utf-8"))["diagnosticos"]["veredicto"]
    r = json.loads(rj.read_text(encoding="utf-8"))
    assert r["solo_informativa"] == (v == "NO APTO") and r["diagnosticos"]["mc_bandas"]["veredicto"] == v
    assert r["clasificacion_v18"] == "ASOCIACIÓN" and set(r["clasificacion_v18_por_especificacion"].values()) == {"ASOCIACIÓN"}
    # R >= 1.000 réplicas (encargo) y semilla
    j = json.loads(mc.read_text(encoding="utf-8"))
    assert j["diagnosticos"]["R"] >= 1000 and j["semilla"] == SEED


def test_e4_e11_no_estimables_y_con_tarea_del_autor():
    for m in ("e4", "e11"):
        p = OUT / m / "tabla.csv"
        if not p.exists():
            pytest.skip("sin salidas")
        import pandas as pd
        t = pd.read_csv(p)
        assert (t.loc[t.id.str.endswith(("-X1", "-X2")), "estimable"] == False).all()  # noqa: E712
        assert t.tarea_autor.notna().all()
    s = (RAIZ / "docs" / "v18" / "tareas_autor.md").read_text(encoding="utf-8")
    assert "V18 · fase 4" in s and s.index("V18 · fase 4") < s.index("V18 · fase 3")


def test_e10_e12_son_asociacion_o_sugestivo_como_maximo():
    for m, tope in (("e10", {"ASOCIACIÓN", "NO ESTIMABLE"}), ("e12", {"SUGESTIVO", "NO CONCLUYENTE", "ASOCIACIÓN", "NO ESTIMABLE"})):
        h = _hechos(m)
        if h is None:
            pytest.skip("sin salidas")
        assert {x["clasificacion_v18"] for x in h} <= tope
    h = _hechos("e12")
    assert all("protegida" in x["nota"].lower() for x in h if x["id"].startswith(("V18-E12-A1", "V18-E12-A2")))
