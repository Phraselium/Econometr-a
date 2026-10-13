"""V8-F4 M7: tests rapidos (motor contra la herramienta de F3 con datos sinteticos; modo --rapido sobre datos reales)."""
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
sys.path.insert(0, str(RAIZ / "src"))
import m67_comun as C  # noqa: E402
from herramientas import multiverso as mvt  # noqa: E402

_spec = importlib.util.spec_from_file_location("m7_multiverso", RAIZ / "src" / "v8" / "m7_multiverso.py")
m7 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m7)

COLS_RESUMEN = ["mercado", "periodo", "factor", "variable", "n_multiverso", "pct_mismo_signo", "signo_mayoritario", "pct_sig_bh", "beta_std_mediana", "p05", "p95",
                "cumple_multiverso"]


@pytest.fixture(scope="module")
def corridas(tmp_path_factory):
    base = tmp_path_factory.mktemp("m7")
    rutas = []
    for k in (1, 2):
        r = base / f"c{k}"
        m7.main(["--rapido", "--salida", str(r)])
        rutas.append(r)
    return rutas


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sintetico():
    rng = np.random.default_rng(5)
    idx = [f"{2000 + i // 4}Q{i % 4 + 1}" for i in range(80)]
    x, g = rng.normal(size=80), rng.normal(size=80)
    dep = pd.Series(0.6 * x + 0.3 * g + rng.normal(size=80), index=idx)
    X = pd.DataFrame({"x": x, "g": g}, index=idx)
    d = pd.DataFrame({"covid": 0, "epa2021": 0}, index=idx)
    return {"dep": dep, "X": X, "win": idx, "ctrl": {"otra": "g"}, "focal": {"fam": [("x", False)]}}, d


def test_motor_igual_a_herramienta_hac():
    c, d = sintetico()
    r = m7.ajustar(c, d, "fam", "x", ["otra"], 0, 0, "HAC4")
    df = pd.DataFrame({"dep": c["dep"], "x": c["X"]["x"], "g": c["X"]["g"]})
    specs, _, _ = mvt.correr_multiverso(df, {"dep": ["dep"], "x": ["x"], "controles": [["g"]], "hac": [4]})
    assert abs(r["beta"] - specs["beta"].iloc[0]) < 1e-10 and abs(r["p"] - specs["p"].iloc[0]) < 1e-10 and r["n"] == specs["n"].iloc[0]


def test_ewc_y_retardo_y_fallida():
    c, d = sintetico()
    r0 = m7.ajustar(c, d, "fam", "x", [], 0, 0, "EWC")
    r4 = m7.ajustar(c, d, "fam", "x", [], 4, 0, "EWC")
    assert r4["n"] == r0["n"] - 4 and 0 < r0["p"] < 0.01
    assert abs(r0["beta_std"] - np.corrcoef(c["dep"], c["X"]["x"])[0, 1]) < 1e-10      # sin controles, beta tipificado = correlacion
    c["win"] = c["win"][:6]
    f = m7.ajustar(c, d, "fam", "x", [], 0, 0, "EWC")
    assert f[0] == "FALLIDA"
    assert m7.ajustar(sintetico()[0], d, "fam", "x", [], 0, 1, "EWC")[0] == "OMITIDA"      # ficticias que no varian


def test_regla_cumple_multiverso():
    filas = []
    for i in range(10):
        filas.append(dict(mercado="compra", periodo="P3", factor="oferta", variable="v", interpolada=False, errores="HAC4",
                          beta_std=0.5 if i < 9 else -0.1, p_bh=0.01 if i < 4 else 0.5))
    r = m7._resumir(pd.DataFrame(filas), "compra", "P3", "oferta", "v")
    assert r["pct_mismo_signo"] == 0.9 and r["pct_sig_bh"] == 0.4 and r["cumple_multiverso"] is False
    filas[4]["p_bh"] = 0.01
    r = m7._resumir(pd.DataFrame(filas), "compra", "P3", "oferta", "v")
    assert r["pct_sig_bh"] == 0.5 and r["cumple_multiverso"] is True
    assert r["signo_mayoritario"] == "positivo"


def test_rejilla_completa_dentro_del_tope():
    d = C.cargar()
    celdas = m7.construir_celdas(d, C.MEDIDAS, ["ipc", "pib"], ["interanual", "trimestral"], list(C.PERIODOS))
    desc = m7.descriptores(celdas, (0, 1, 4), ("HAC4", "EWC"), d)
    assert 5000 < len(desc) <= m7.MAX_SPECS
    assert {k[0] for k in celdas} == {"compra", "alquiler"} and {k[1] for k in celdas} == {"tasado", "ipv", "ipc_alquiler"}


def test_contrato_resumen(corridas):
    r = corridas[0]
    res = pd.read_csv(r / "resumen_multiverso.csv")
    assert list(res.columns[:12]) == COLS_RESUMEN
    tod = res[res["variable"] == "TODAS"]
    assert len(tod) > 0 and set(tod["mercado"]) == {"compra", "alquiler"}
    assert not tod.duplicated(["mercado", "periodo", "factor"]).any()          # clave de cruce unica para M2/M5
    pv = res[res["variable"] != "TODAS"]
    assert (pv["cumple_multiverso"] == ((pv["pct_mismo_signo"] >= 0.8) & (pv["pct_sig_bh"] >= 0.5))).all()
    # R3: la familia cumple solo si cumplen la familia (orientada) y su variable principal
    assert (tod["cumple_multiverso"] == tod["cumple_R3"]).all()
    assert (tod["cumple_multiverso"].astype(bool) <= tod["cumple_multiverso_familia"].astype(bool)).all()
    assert (res["n_rejilla"] >= res["n_multiverso"]).all() and (res["pct_mismo_signo_rejilla"] <= res["pct_mismo_signo"] + 1e-12).all()
    assert "tiempo" not in (r / "resultado.json").read_text() and (r / "tiempos.json").exists()
    assert (res["p05"] <= res["beta_std_mediana"] + 1e-12).all() and (res["beta_std_mediana"] <= res["p95"] + 1e-12).all()
    # n de la fila TODAS = suma de las filas por variable
    s = res[res["variable"] != "TODAS"].groupby(["mercado", "periodo", "factor"])["n_multiverso"].sum()
    assert (tod.set_index(["mercado", "periodo", "factor"])["n_multiverso"] == s).all()


def test_bh_y_registry_completo(corridas):
    r = corridas[0]
    sp = pd.read_csv(r / "especificaciones.csv")
    fa = pd.read_csv(r / "fallidas.csv")
    reg = pd.read_csv(r / "registro.csv")
    assert len(reg) == len(sp) + len(fa) <= m7.MAX_SPECS            # TODAS las especificaciones, incluidas las fallidas, en el Registry
    assert reg["fase"].eq("M7").all() and reg["modelo_id"].is_unique
    g = sp[(sp["mercado"] == "compra") & (sp["periodo"] == "P3")]
    assert np.allclose(g["p_bh"].values, C.bh(g["p"].values, 0.10))
    assert (sp["p_bh"] >= sp["p"] - 1e-12).all()


def test_resultado_y_determinismo(corridas):
    j = json.loads((corridas[0] / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in j
    assert j["capa"] == "C4" and "sin lenguaje causal" in j["nivel_evidencia"]
    assert j["N"]["tope"] == 50000 and j["N"]["truncado"] is False
    for f in ["resumen_multiverso.csv", "especificaciones.csv", "registro.csv"]:
        assert sha(corridas[0] / f) == sha(corridas[1] / f), f


def test_orientacion_tipos():
    filas = [dict(mercado="compra", periodo="P5", factor="credito_tipos", variable=v, interpolada=False, errores="HAC4",
                  beta_std=b, p_bh=0.01) for v, b in (("tipo_hip_real", 0.4), ("tipo_hip_real", 0.5), ("credito_stock_real", -0.3), ("credito_stock_real", -0.2))]
    r = m7._resumir(pd.DataFrame(filas), "compra", "P5", "credito_tipos", "TODAS", 6)
    assert r["pct_mismo_signo"] == 1.0 and r["signo_mayoritario"] == "negativo"     # tipos x-1: los 4 coeficientes apuntan en la misma direccion
    assert abs(r["pct_mismo_signo_rejilla"] - 4 / 6) < 1e-12 and r["cumple_multiverso_rejilla"] is False


def test_ficticia_epa_impulso():
    d = C.cargar()
    assert d["epa2021"].sum() == 4 and d["epa2021_q"].sum() == 1 and d.loc["2021Q1", "epa2021_q"] == 1 and d.loc["2022Q1", "epa2021"] == 0
