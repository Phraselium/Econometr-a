"""V8-F5: tests rapidos (regla §9 sobre datos sinteticos y coherencia de las salidas ya escritas)."""
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
_spec = importlib.util.spec_from_file_location("f5_atribucion", RAIZ / "src" / "v8" / "f5_atribucion.py")
f5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(f5)
SAL = RAIZ / "output" / "v8" / "F5"


@pytest.fixture(scope="module")
def R():
    return pd.read_csv(SAL / "regla_s9.csv")


def test_regla_cubre_diez_celdas(R):
    assert len(R) == 10 and set(R["mercado"]) == {"compra", "alquiler"} and set(R["periodo"]) == set(f5.PERS)
    assert not R.duplicated(["mercado", "ambito", "periodo"]).any()


def test_designacion_exige_las_tres_condiciones_y_no_r7(R):
    d = R[R["resultado"] != "no designado"]
    assert d["cond1"].all() and d["cond2"].all() and d["cond3"].all() and not d["R7_impreciso"].any()
    assert d["resultado"].isin(f5.FACTORES7).all()
    imp = R[R["R7_impreciso"]]
    assert set(zip(imp["mercado"], imp["periodo"])) == f5.IMPRECISOS
    assert (imp["resultado"] == "no designado").all()


def test_sin_designacion_hay_motivo(R):
    nd = R[R["resultado"] == "no designado"]
    assert nd["motivo"].fillna("").str.len().gt(10).all()


def test_abstencion_no_cuenta_como_voto(R):
    # un factor con menos de 3 votos reales no puede cumplir la condicion 1
    assert ((R["n_votos"] >= 3) == R["cond1"]).all()


def test_votos_lpiv_solo_si_aporta_y_supera():
    E = f5.entradas()
    sv = f5.cand_svar(E, "compra", "P2")
    f, motivo = f5.voto_lpiv(E, "compra", "P2", -1.0, sv)
    assert f is None and "no supera" in motivo       # c·sign negativa: no supera a svar_hd
    f, motivo = f5.voto_lpiv(E, "alquiler", "P3", -1.0, f5.cand_svar(E, "alquiler", "P3"))
    assert f is None and "F < 10" in motivo


def test_svar_vota_por_prob_mayor_y_marca_discrepancia():
    E = f5.entradas()
    s = f5.cand_svar(E, "compra", "P5")
    assert s["voto"] == s["tabla"].sort_values("prob_mayor").iloc[-1]["factor"]
    assert s["factor_media"] != s["voto"] and "discrepan" in s["nota"]


def test_cond2_orientado_y_fallidas_en_denominador():
    E = f5.entradas()
    c = f5.cond2(E, "compra", "P1", "empleo_renta")
    assert c["pct_familia_fall"] <= c["pct_familia"] + 1e-12
    assert c["ok"] == (c["pct_familia"] >= 0.8 and c["pct_variable"] >= 0.8)
    assert f5.cond2(E, "alquiler", "P4", "demanda_vivienda")["ok"] is False


def test_cuota_no_atribuida_suma_de_medias():
    E = f5.entradas()
    q = f5.cuota_no_atribuida(E, "compra", "P5", 18.420287, 7.157)
    g = E["m2"][(E["m2"]["mercado"] == "compra") & (E["m2"]["periodo"] == "P5") & E["m2"]["factor"].isin(["determinista", "no_identificados"])]
    assert q["pp"] == pytest.approx(g["media"].sum()) and q["cuota"] == pytest.approx(q["pp"] / 18.420287)


def test_ranking_orden_y_bandas_en_signo_de_dy():
    K = pd.read_csv(SAL / "ranking.csv")
    g = K[(K["mercado"] == "compra") & (K["periodo"] == "P2")].dropna(subset=["rank_svar_media"]).sort_values("rank_svar_media")
    assert g["media_c_signo_pp"].is_monotonic_decreasing
    assert (g["b68_lo"] <= g["b68_hi"]).all()
    assert g["prob_mayor"].sum() == pytest.approx(1.0, abs=1e-6)


def test_combinada_unicidad_y_no_compiten():
    C = pd.read_csv(SAL / "atribucion_combinada.csv")
    assert not C.duplicated(["mercado", "ambito", "periodo", "factor", "metodo", "variante"]).any()
    assert (C.loc[C["factor"].isin(f5.NO_COMPITEN), "compite"] == "no").all()
    assert (C.loc[C["metodo"] == "svar_hd", "capa"] == "C3s").all() and set(C.loc[C["metodo"] != "svar_hd", "capa"]) <= {"C4"}


def test_regional_sin_designacion():
    G = pd.read_csv(SAL / "regional_ranking.csv")
    assert G["designacion"].str.startswith("no designado").all()
    assert set(G["ambito"]) >= {"cv_prov:03", "cv_prov:12", "cv_prov:46", "valencia_ciudad", "ccaa:01", "ccaa:17"}


def test_fuera_muestra_comun_misma_muestra():
    T = pd.read_csv(SAL / "fuera_muestra_comun.csv")
    for m, g in T[T["evaluable"] == "si"].groupby("mercado"):
        assert g["n_test"].nunique() == 1 and g["n_trimestres"].iloc[0] == 40
        assert {"ar4", "ecm_v1", "bvar_m2", "ar_fc"} <= set(g["modelo"])
    P = pd.read_csv(SAL / "fuera_muestra_comun_predicciones.csv")
    assert P["trimestre"].min() == "2016Q2" and P["trimestre"].max() == "2026Q1"


def test_resultado_json_y_registro():
    r = json.loads((SAL / "resultado.json").read_text())
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in r
    reg = pd.read_csv(SAL / "registro.csv")
    assert (reg["fase"] == "F5").all() and len(reg) >= 10 + 8


def test_neutralidad_y_sin_lenguaje_causal_en_fichas():
    t = (SAL / "fichas.md").read_text().lower()
    for pal in ("causa ", "provoca", "culpa", "partido"):
        assert pal not in t


def test_determinismo_rapido(tmp_path):
    f5.main(["--rapido", "--salida", str(tmp_path / "a")])
    f5.main(["--rapido", "--salida", str(tmp_path / "b")])
    for n in ("regla_s9.csv", "ranking.csv", "atribucion_combinada.csv", "fuera_muestra_comun.csv"):
        assert (tmp_path / "a" / n).read_bytes() == (tmp_path / "b" / n).read_bytes()
