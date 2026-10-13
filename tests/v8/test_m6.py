"""V8-F4 M6: tests rapidos (datos sinteticos y modo --rapido sobre datos reales de solo lectura; escribe en un directorio temporal)."""
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
from herramientas import lp  # noqa: E402

_spec = importlib.util.spec_from_file_location("m6_colinealidad", RAIZ / "src" / "v8" / "m6_colinealidad.py")
m6 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m6)

FACTORES = {"demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo"}
COLS_COEF = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio", "variable"]


@pytest.fixture(scope="module")
def corridas(tmp_path_factory):
    base = tmp_path_factory.mktemp("m6")
    rutas = []
    for k in (1, 2):
        r = base / f"c{k}"
        m6.main(["--rapido", "--salida", str(r)])
        rutas.append(r)
    return rutas


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def test_ewc_identico_a_lp():
    rng = np.random.default_rng(1)
    n = 80
    x = rng.normal(size=n)
    y = 0.5 * x + rng.normal(size=n)
    A = np.column_stack([np.ones(n), x])
    e1 = C.ewc_ols(y, A)
    M = pd.DataFrame({"dep": y, "x": x})
    e2 = lp._ols_ewc(M, 0.95)
    assert abs(e1["beta"][1] - e2["beta"]) < 1e-10 and abs(e1["se"][1] - e2["se"]) < 1e-10


def test_bma_recupera_senal():
    rng = np.random.default_rng(2)
    n, p = 120, 5
    X = pd.DataFrame(rng.normal(size=(n, p)), columns=list("abcde"))
    y = 1.0 * X["a"].values - 0.8 * X["c"].values + rng.normal(size=n)
    filas, w, pip, pm = m6.bma_celda(y, X, kmax=5)
    assert len(filas) == 2 ** p and abs(w.sum() - 1) < 1e-12
    assert pip[0] > 0.99 and pip[2] > 0.99 and pip[[1, 3, 4]].max() < 0.5
    assert pm[0] > 0 > pm[2]


def test_dominancia_suma_r2_y_johnson():
    from herramientas import dominancia
    rng = np.random.default_rng(3)
    X = rng.normal(size=(100, 4))
    X[:, 1] += 0.8 * X[:, 0]
    y = X @ np.array([1, 0.5, 0, 0.3]) + rng.normal(size=100)
    s = dominancia.shapley_r2(pd.DataFrame(X, columns=list("abcd")), y)
    assert abs(s["phi"].sum() - s.attrs["r2"]) < 1e-10
    j = dominancia.johnson_rw(X, y)
    assert abs(j["peso"].sum() - s.attrs["r2"]) < 1e-6


def test_preparar_tasas_y_familias():
    d = C.cargar()
    dep, X, ip, niv = C.preparar(d, "compra", "tasado", "ipc", "interanual")
    manual = 100 * (np.log(d["p_tasado"]) - np.log(d["ipc_general"])).diff(4)
    assert np.allclose(dep.dropna().values, manual.dropna().values[-len(dep.dropna()):], atol=1e-6)
    win = C.ventana(d.index, "P5")
    sel, exc = C.elegir_principales(dep, X, ip, win)
    assert set(sel) | set(exc) == set(C.FAM_ORDEN)
    # la poblacion semestral (interpolada) no entra en tasa trimestral
    dq, Xq, ipq, _ = C.preparar(d, "compra", "tasado", "ipc", "trimestral")
    assert C.es_interpolada(Xq["pob_total"], ipq["pob_total"], C.ventana(d.index, "P2"))
    assert "turismo" in C.elegir_principales(dep, X, ip, C.ventana(d.index, "P1"))[1]


def test_gl_minimos_p4():
    d = C.cargar()
    dep, X, ip, _ = C.preparar(d, "alquiler", "ipc_alquiler", "ipc", "interanual")
    win = C.ventana(d.index, "P4")
    sel, _ = C.elegir_principales(dep, X, ip, win)
    sel2, D, mot = C.limitar_por_gl(dep, X, sel, win)
    assert len(D) - (len(sel2) + 1) >= C.GL_MIN
    assert len(sel2) < len(sel) and list(sel2) == C.FAM_ORDEN[:len(sel2)]
    assert mot


def test_contrato_salidas(corridas):
    r = corridas[0]
    for f in ["coeficientes.csv", "atribucion.csv", "colinealidad.csv", "belsley.csv", "pesos_johnson.csv", "ortogonalizacion.csv", "indice_compuesto.csv",
              "granger.csv", "lp_agregado.csv", "bma.csv", "penalizados.csv", "fuera_muestra.csv", "muestras.csv", "registro.csv", "resultado.json", "resumen.md", "voto_dominancia.csv", "tiempos.json"]:
        assert (r / f).exists(), f
    assert "tiempo" not in (r / "resultado.json").read_text() and "tiempo" not in (r / "resumen.md").read_text()
    co = pd.read_csv(r / "coeficientes.csv")
    assert list(co.columns[:10]) == COLS_COEF and co["capa"].eq("C4").all() and co["tipo_ee"].eq("EWC").all()
    assert co["vif_max"].notna().all() and co["modulo"].eq("M6").all()
    at = pd.read_csv(r / "atribucion.csv")
    assert list(at.columns) == ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "notas",
                               "cuota_lmg", "r2", "delta_y_pp", "signo_parcial", "contrib_parcial_pp", "orientacion", "variante", "principal"]
    assert not at.duplicated(["metodo", "mercado", "ambito", "periodo", "factor", "variante"]).any()
    assert set(at["metodo"]) <= {"dominancia", "dominancia_trimestral"} and set(at["factor"]) <= FACTORES | {"residuo"} and at["capa"].eq("C4").all()
    ok = at[at["pct_total"].notna()]
    for _, g in ok.groupby(["metodo", "mercado", "periodo"]):
        assert abs(g["pct_total"].sum() - 100) < 1e-6
        assert (g["b90_lo"] <= g["b90_hi"] + 1e-12).all() and (g["b68_lo"] <= g["b68_hi"] + 1e-12).all()
        var = float(g["notas"].iloc[0].split("variacion acumulada (")[1].split(" pp")[0])
        assert abs(g["contribucion_pp"].sum() - var) < 0.06   # la variacion se imprime con 1 decimal
    # J5: contribucion = cuota LMG x R2 x variacion; fila residuo = (1 - R2) x variacion; signo_parcial = signo de contrib_parcial_pp
    fa = ok[ok["factor"] != "residuo"]
    assert np.allclose(fa["contribucion_pp"], fa["cuota_lmg"] * fa["r2"] * fa["delta_y_pp"])
    rs = ok[ok["factor"] == "residuo"]
    assert len(rs) and np.allclose(rs["contribucion_pp"], (1 - rs["r2"]) * rs["delta_y_pp"])
    assert (np.sign(fa["contrib_parcial_pp"]) == fa["signo_parcial"]).all()
    vo = pd.read_csv(r / "voto_dominancia.csv")
    assert {"mercado", "periodo", "factor_votado"} <= set(vo.columns)
    for _, v in vo[vo["factor_votado"] != "abstiene"].iterrows():
        g = fa[(fa["metodo"] == "dominancia") & (fa["mercado"] == v["mercado"]) & (fa["periodo"] == v["periodo"])]
        elegible = g[g["signo_parcial"] == np.sign(g["delta_y_pp"])]
        assert v["factor_votado"] == elegible.sort_values("cuota_lmg", ascending=False)["factor"].iloc[0]
    # las bandas del bootstrap por bloques rodean la estimacion puntual en la mayoria de los casos
    dentro = ((ok["contribucion_pp"] >= ok["b90_lo"] - 1e-9) & (ok["contribucion_pp"] <= ok["b90_hi"] + 1e-9)).mean()
    assert dentro > 0.8


def test_ortogonalizacion_todos_los_ordenes(corridas):
    o = pd.read_csv(corridas[0] / "ortogonalizacion.csv")
    import math
    assert (o["n_ordenes"] == o.groupby(["mercado", "transformacion", "periodo"])["factor"].transform("count").map(math.factorial)).all()
    assert (o["r2_inc_min"] <= o["r2_inc_media"] + 1e-12).all() and (o["r2_inc_media"] <= o["r2_inc_max"] + 1e-12).all()
    # la media sobre todos los ordenes es el LMG: coincide con la cuota de dominancia
    j = pd.read_csv(corridas[0] / "pesos_johnson.csv")
    m = o.merge(j, on=["mercado", "transformacion", "periodo", "factor"])
    assert np.allclose(m["r2_inc_media"] / m["r2_total"], m["cuota_dominancia"], atol=1e-6)


def test_resultado_y_lenguaje(corridas):
    j = json.loads((corridas[0] / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in j
    assert j["capa"] == "C4" and "EXPLORATORIO" in j["nivel_evidencia"] and "NO" in j["nivel_evidencia"].upper()
    fm = pd.read_csv(corridas[0] / "fuera_muestra.csv")
    assert {"ar4", "ecm_v1", "ridge", "enet", "ols_factores"} <= set(fm["modelo"])
    assert fm["n_oos"].nunique() == 1          # misma muestra de evaluacion para todos los modelos
    g = pd.read_csv(corridas[0] / "granger.csv")
    assert g["nota"].str.contains("NO causal|n insuficiente").all()


def test_registry_y_determinismo(corridas):
    reg = pd.read_csv(corridas[0] / "registro.csv")
    assert list(reg.columns) == ["fase", "modelo_id", "formula", "muestra_ini", "muestra_fin", "n", "r2_adj", "aic", "bic", "rmse_oos", "coef_interes", "p_interes", "notas"]
    assert reg["fase"].eq("M6").all() and len(reg) > 50
    for f in ["atribucion.csv", "coeficientes.csv", "bma.csv", "granger.csv", "lp_agregado.csv", "penalizados.csv", "fuera_muestra.csv"]:
        assert sha(corridas[0] / f) == sha(corridas[1] / f), f
