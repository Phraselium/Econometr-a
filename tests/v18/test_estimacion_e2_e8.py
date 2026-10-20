"""V18 · fase 4 · E2 (topes al alquiler) y E8 (ITP): determinismo, que el sellado (sellado.filtrar) se aplica, reglas de codificación de fechas de la adenda,
estimador dCDH con máscara, adelantos, clasificación I1-I8 y salidas (hechos sin lenguaje causal, capa C4, EXPLORATORIO).

Los tests no abren data/sealed ni estiman con datos reales: usan paneles sintéticos y el manifiesto de sellado (solo metadatos).
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "estimacion"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import _e2e8_comun as K  # noqa: E402
import e8_datos as D8  # noqa: E402
import e8_estim as E8  # noqa: E402
import sellado  # noqa: E402
from herramientas import dcdh as DC  # noqa: E402

SALIDAS = RAIZ / "output" / "v18" / "estimacion"


# ------------------------------------------------------------------------------------------------ sellado
def test_filtrar_aplica_sellado_temporal_y_territorial():
    man = sellado.cargar()
    sellado_mun = sorted(man["unidades_excluidas"]["municipio"]["v15"]["unidades"])[0]
    df = pd.DataFrame({"territorio_codigo": [sellado_mun, "08019", "08019", "08019"], "periodo": ["2020T1", "2020T1", "2026T1", "2027T1"], "valor": [1.0, 2.0, 3.0, 4.0]})
    out = K.filtrar(df, "territorio_codigo", "municipio", "periodo", "incasol_renta_media", "T")
    assert sellado_mun not in set(out.territorio_codigo)          # unidad sellada de V15
    assert "2027T1" not in set(out.periodo)                        # posterior al tope de la variable (2026T1)
    assert set(out.periodo) == {"2020T1", "2026T1"}


def test_filtrar_rechaza_variable_sin_clave():
    df = pd.DataFrame({"territorio_codigo": ["08019"], "periodo": ["2020"], "valor": [1.0]})
    with pytest.raises(KeyError):
        K.filtrar(df, "territorio_codigo", "municipio", "periodo", "variable_inventada", "A")


def test_filtrar_excluye_provincias_selladas_v6():
    df = pd.DataFrame({"territorio_codigo": ["28", "08"], "periodo": ["2020T1", "2020T1"], "valor": [1.0, 1.0]})       # 28 = Madrid (v6)
    out = K.filtrar(df, "territorio_codigo", "provincia", "periodo", "valor_tasado", "T")
    assert list(out.territorio_codigo) == ["08"]


def test_toda_lectura_de_datos_pasa_por_filtrar():
    for nombre in ("e2_datos.py", "e2_diseno.py", "e2_estim.py", "e8_datos.py", "e8_diseno.py", "e8_estim.py", "e2_topes.py", "e8_itp.py"):
        txt = (RAIZ / "src" / "v18" / "estimacion" / nombre).read_text(encoding="utf-8")
        for m in re.finditer(r"pd\.read_(csv|parquet|excel)\(", txt):
            linea = txt[: m.start()].count("\n") + 1
            contexto = "\n".join(txt.splitlines()[max(0, linea - 12): linea + 12])
            assert ("K.filtrar(" in contexto or "K.leer_hechos(" in contexto or "hecho normativo" in contexto or "diccionario" in contexto or "tipos_generales" in contexto
                    or "geopandas" in contexto or "intervenciones" in contexto or "cataluna_contencion" in contexto or "tabla_d1" in contexto), f"{nombre}:{linea} lee datos sin filtrar"
    txt = (RAIZ / "src" / "v18" / "estimacion" / "_e2e8_comun.py").read_text(encoding="utf-8")
    assert "sellado.filtrar(" in txt and "holdout.excluir_sellados_v6(" in txt
    assert "data/sealed" not in txt.replace("nunca se abre data/sealed", "")


def test_sin_acceso_a_muestra_sellada_ni_evaluate():
    for p in (RAIZ / "src" / "v18" / "estimacion").glob("e[28]_*.py"):
        t = p.read_text(encoding="utf-8")
        assert "evaluate_" not in t.replace("ningún `evaluate_*`", "").replace("evaluate_*", "")
        assert "sellar_v" not in t


# ------------------------------------------------------------------------------------------------ determinismo y regresión
def _panel(seed=1, N=60, T=10, tr=20, post=6, efecto=-0.05):
    rng = np.random.default_rng(seed)
    Y = rng.normal(size=(N, 1)) + rng.normal(size=(1, T)) + rng.normal(size=(N, T)) * 0.2
    lab = np.arange(N) < tr
    Y = Y + efecto * (lab[:, None] & (np.arange(T) >= post)[None, :])
    unit, time = np.repeat(np.arange(N), T), np.tile(np.arange(T), N)
    d = (lab[:, None] & (np.arange(T) >= post)[None, :]).ravel().astype(float)
    return Y, lab, unit, time, d


def test_modelo_coincide_con_statsmodels_y_es_determinista():
    import statsmodels.formula.api as smf
    Y, lab, unit, time, d = _panel()
    m = K.Modelo(Y.ravel(), d, unit, time)
    df = pd.DataFrame({"y": Y.ravel(), "d": d, "u": unit, "t": time})
    r = smf.ols("y ~ d + C(u) + C(t)", df).fit(cov_type="cluster", cov_kwds={"groups": df.u})
    assert m.beta == pytest.approx(r.params["d"], rel=1e-8)
    assert m.se == pytest.approx(r.bse["d"], rel=1e-8)
    p1 = m.webb_p(0.0, 999, np.random.default_rng(K.SEMILLA))
    p2 = K.Modelo(Y.ravel(), d, unit, time).webb_p(0.0, 999, np.random.default_rng(K.SEMILLA))
    assert p1 == p2
    assert K.SEMILLA == 20261010


def test_webb_detecta_efecto_y_no_rechaza_nulo():
    Y, lab, unit, time, d = _panel(efecto=-0.3)
    assert K.Modelo(Y.ravel(), d, unit, time).webb_p(0.0, 999, np.random.default_rng(1)) < 0.05
    Y0, lab, unit, time, d = _panel(seed=7, efecto=0.0)
    assert K.Modelo(Y0.ravel(), d, unit, time).webb_p(0.0, 999, np.random.default_rng(1)) > 0.05


def test_mde_determinista_y_proporcional_a_la_desviacion():
    rng = np.random.default_rng(3)
    x = rng.normal(size=2000) * 0.01
    a, b = K.mde_desde_placebos(x), K.mde_desde_placebos(x)
    assert a == b
    assert 2.4 * 0.01 < a["mde80"] < 3.2 * 0.01
    assert K.mde_desde_placebos(2 * x)["mde80"] == pytest.approx(2 * a["mde80"], rel=0.02)


def test_p_corr_y_bandas():
    assert K.p_corr(0.03, 0.05) == 0.03
    assert K.p_corr(0.03, 0.071) == pytest.approx(0.03 * 0.071 / 0.05)
    assert K.p_corr(0.9, 0.1) == 0.9 * 2 or K.p_corr(0.9, 0.1) == 1.0
    assert K.banda_mc(0.0455) == "apta" and K.banda_mc(0.071) == "con valor crítico corregido" and K.banda_mc(0.178) == "no fiable"


# ------------------------------------------------------------------------------------------------ E8: codificación de fechas y estimador
def test_codificacion_mes_y_trimestre():
    assert D8.mes_codificado(pd.Timestamp("2013-08-06")) == "2013-08"          # día ≤ 15: el mes de entrada
    assert D8.mes_codificado(pd.Timestamp("2021-04-28")) == "2021-05"          # día > 15: el mes siguiente
    assert D8.trimestre_codificado(pd.Timestamp("2021-04-28")) == "2021T2"
    assert D8.trimestre_codificado(pd.Timestamp("2013-03-31")) == "2013T2"      # 31-mar: abril, segundo trimestre


def test_calendario_fusion_menos_de_12_meses_y_reproducible():
    e1, e2 = D8.eventos("exacta"), D8.eventos("exacta")
    pd.testing.assert_frame_equal(e1, e2)
    v = e1[e1.cod_ine == "10"]
    assert (v.dosis == 3.0).any()                       # Comunitat Valenciana: +1 y +2 en 2013 se fusionan con la dosis acumulada en la primera fecha
    assert v[v.dosis == 3.0].fecha.iloc[0] == pd.Timestamp("2013-01-01")
    assert (D8.eventos("enero").fecha.dt.month == 1).all() and (D8.eventos("enero").fecha.dt.day == 1).all()
    mas, menos = D8.eventos("mas3"), D8.eventos("menos3")
    assert (mas.fecha > menos.fecha).all()


def test_dcdh_con_mascara_reproduce_la_herramienta_y_las_leads_detectan_tendencia():
    rng = np.random.default_rng(5)
    n, T = 12, 40
    cl = np.repeat(np.arange(4), 3)
    Dc = np.zeros((4, T))
    Dc[0, 10:], Dc[1, 20:], Dc[2, 15:], Dc[3, 30:] = 1, 2, -1, 1
    Y = rng.normal(size=(n, T)).cumsum(1) * 0.1 + 0.5 * Dc[cl]
    for ell in (0, 2, 4):
        a, b = DC.estimar(Y, Dc[cl], ell), E8.estimar_m(Y, Dc[cl], ell)
        assert float(a["beta"]) == pytest.approx(float(b["beta"]))
        assert np.allclose(a["IF"], b["IF"])
    m = np.ones(T - 1, bool)
    m[8:12] = False
    assert E8.estimar_m(Y, Dc[cl], 2, m)["beta"] != E8.estimar_m(Y, Dc[cl], 2)["beta"]
    Y2 = 0.5 * Dc[cl] + rng.normal(size=(n, T)) * 0.001
    assert float(E8.estimar_m(Y2, Dc[cl], 2)["beta"]) == pytest.approx(0.5, abs=0.02)
    assert abs(float(E8.lead_gap(Y2, Dc[cl], 4))) < 0.01
    tendencia = 0.1 * np.arange(T)[None, :] * np.where(np.isin(cl, [0, 1]), 1.0, 0.0)[:, None]
    assert abs(float(E8.lead_gap(Y2 + tendencia, Dc[cl], 4))) > 0.05            # una tendencia previa del grupo que cambia aparece en el adelanto


def test_aleatorizacion_calendarios_determinista():
    rng = np.random.default_rng(9)
    n, T = 16, 30
    cl = np.repeat(np.arange(4), 4)
    Dc = np.zeros((4, T))
    Dc[0, 8:], Dc[1, 14:], Dc[2, 20:] = 1, 1, 2
    Y = rng.normal(size=(n, T)) * 0.1 + 0.4 * Dc[cl]
    p1 = E8.p_aleat(Y, Dc, cl, 0.0, 2, DC.permutaciones(np.random.default_rng(K.SEMILLA), 4, 500))
    p2 = E8.p_aleat(Y, Dc, cl, 0.0, 2, DC.permutaciones(np.random.default_rng(K.SEMILLA), 4, 500))
    assert p1 == p2 and 0 < p1 <= 1


def test_moran_detecta_autocorrelacion_espacial_y_es_determinista():
    rng = np.random.default_rng(2)
    xy = rng.uniform(0, 100, size=(60, 2))
    liso = xy[:, 0] / 100.0 + rng.normal(size=60) * 0.05            # valores que varían suavemente en el espacio
    ruido = rng.normal(size=60)
    a, b = K.moran_i(liso, xy), K.moran_i(liso, xy)
    assert a == b and a["I"] > 0.5 and a["p_unilateral"] < 0.01
    assert abs(K.moran_i(ruido, xy)["I"]) < 0.3
    assert K.trimestres("2019T4", "2020T2") == ["2019T4", "2020T1", "2020T2"]


# ------------------------------------------------------------------------------------------------ clasificación
def _info(**kw):
    base = {"estimable": True, "coprincipal": False, "p_holm": 0.01, "coef": -0.04, "pretend_p": 0.5, "roth_ok": True, "placebo_fecha": {"coef": 0.001, "p": 0.8, "mismo_signo": False},
            "placebo_resultado": "ok", "robustez": {"frac_mismo_signo": 1.0, "cambio_signo": False, "solape_ic": True}, "inferencia_banda": "apta", "topes": [],
            "tost": {"equivalente": False}}
    base.update(kw)
    return base


def test_clasificar_identificado_sugestivo_y_ascociacion():
    assert K.clasificar(_info())["clase"] == "IDENTIFICADO"
    assert K.clasificar(_info(topes=["tope"]))["clase"] == "SUGESTIVO"
    assert K.clasificar(_info(roth_ok=False))["clase"] == "SUGESTIVO"
    assert K.clasificar(_info(pretend_p=0.005))["clase"] == "ASOCIACIÓN"
    assert K.clasificar(_info(robustez={"frac_mismo_signo": 1.0, "cambio_signo": True, "solape_ic": True}))["clase"] == "ASOCIACIÓN"
    assert K.clasificar(_info(placebo_fecha={"coef": -0.03, "p": 0.01, "mismo_signo": True}))["clase"] == "ASOCIACIÓN"
    assert K.clasificar(_info(inferencia_banda="no fiable"))["clase"] == "ASOCIACIÓN"


def test_k7_no_significativo_sin_i1_i5_es_asociacion_solo_con_la_opcion():
    """K7 (B6): no existe «SUGESTIVO sin significación»; con la opción, un no significativo que no supera I1-I5 es ASOCIACIÓN."""
    debil = _info(p_holm=0.5, roth_ok=False)
    assert K.clasificar(debil)["clase"] == "SUGESTIVO"                                  # lectura anterior (E1 y E6 no usan la opción)
    assert K.clasificar(debil | {"nulo_sin_sugestivo": True})["clase"] == "ASOCIACIÓN"
    assert K.clasificar(_info(p_holm=0.5) | {"nulo_sin_sugestivo": True})["clase"] == "NO CONCLUYENTE (sin potencia)"
    assert K.clasificar(_info(p_holm=0.07, roth_ok=False) | {"nulo_sin_sugestivo": True})["clase"] == "SUGESTIVO"     # significación entre 0,05 y 0,10
    cambio = K.clasificar(_info(robustez={"frac_mismo_signo": 0.9, "cambio_signo": True, "solape_ic": True}, texto_cambio_signo="el signo cambia sin 2012-2013 (B4)"))
    assert cambio["clase"] == "ASOCIACIÓN" and cambio["razones"] == ["el signo cambia sin 2012-2013 (B4)"]


def test_salidas_k7_e2r1c_y_e8r1_son_asociacion():
    for estudio, clave in (("e2", "E2-R1c"), ("e8", "E8-R1")):
        f = SALIDAS / estudio / "resultado.json"
        if not f.exists():
            pytest.skip("sin salidas")
        assert json.loads(f.read_text(encoding="utf-8"))["clasificaciones"][clave] == "ASOCIACIÓN"
    assert json.loads((SALIDAS / "e2" / "resultado.json").read_text(encoding="utf-8"))["clasificaciones"]["E2-R1"] == "SUGESTIVO"


def test_robustez_b6_de_e2_formato():
    f = SALIDAS / "e2" / "robustez_b6.csv"
    if not f.exists():
        pytest.skip("sin salidas")
    r = pd.read_csv(f)
    assert {"id", "prueba", "coef", "p_webb", "q_bh"} <= set(r.columns)
    assert set(r.prueba) == {"a", "b", "c", "d", "e"} and "E2-R1c-v1" in set(r.id)
    h = json.loads((SALIDAS / "e2" / "hechos.json").read_text(encoding="utf-8"))
    b6 = [x for x in h if x["id"].startswith("V18-E2-B6-")]
    assert len(b6) >= 4 and all(x["capa"] == "C4" for x in b6)
    assert "## Robustez B6 (a posteriori)" in (SALIDAS / "e2" / "informe.md").read_text(encoding="utf-8")


def test_clasificar_nulos_no_concluyente_y_no_estimable():
    assert K.clasificar(_info(p_holm=0.5))["clase"] == "NO CONCLUYENTE (sin potencia)"
    assert K.clasificar(_info(p_holm=0.5, tost={"equivalente": True}))["clase"] == "IDENTIFICADO (efecto nulo acotado)"
    assert K.clasificar(_info(p_holm=0.5, tost={"equivalente": True}, topes=["t"]))["clase"] == "SUGESTIVO (efecto nulo acotado)"
    assert K.clasificar(_info(p_holm=0.07))["clase"] == "SUGESTIVO"
    assert K.clasificar({"estimable": False, "motivo_no_estimable": "MDE"})["clase"] == "NO ESTIMABLE"
    assert K.clasificar(_info(coprincipal=True))["clase"] == "no se clasifica"
    assert K.clase_corta("IDENTIFICADO (efecto nulo acotado)") == "IDENTIFICADO"
    assert K.clase_corta("NO CONCLUYENTE (sin potencia)") == "NO CONCLUYENTE"


def test_tost_y_roth():
    assert K.tost(0.001, 0.005, 0.05, 100)["equivalente"] is True
    assert K.tost(0.04, 0.02, 0.05, 100)["equivalente"] is False
    V = np.eye(4) * 0.01 ** 2
    d = K.roth_pendiente(V, np.array([-4.0, -3.0, -2.0, -1.0]))
    assert 0 < d < 0.01


# ------------------------------------------------------------------------------------------------ hechos y salidas
def test_hecho_rechaza_lenguaje_causal():
    K.hecho("V18-E2-TEST", "indicador", 1.0, 0.0, 2.0, "log", "2020", "cob", ["f"], "SUGESTIVO", "asociación estimada")
    for malo in ("efecto causal", "debido a", "provoca", "gracias a", "causa", "impacto causal", "se debe a"):
        with pytest.raises(ValueError):
            K.hecho("V18-E2-TEST", "indicador", 1.0, 0.0, 2.0, "log", "2020", "cob", ["f"], "SUGESTIVO", f"nota {malo} nota")


@pytest.mark.parametrize("estudio", ["e2", "e8"])
def test_salidas_formato(estudio):
    carpeta = SALIDAS / estudio
    if not (carpeta / "resultado.json").exists():
        pytest.skip("las salidas se generan con src/v18/estimacion/*.py")
    r = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas", "clasificacion_v18"):
        assert k in r
    assert r["nivel_evidencia"] == "EXPLORATORIO" and r["capa"] == "C4"
    assert r["clasificacion_v18"] in {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
    assert set(r["fuera_muestra"]) >= {"modelo", "rmse", "dm_vs_ar4"}
    hechos = json.loads((carpeta / "hechos.json").read_text(encoding="utf-8"))
    pat = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)
    for h in hechos:
        assert h["id"].startswith(f"V18-{estudio.upper()}-")
        assert h["capa"] == "C4" and h["clasificacion_v18"] in {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
        assert not pat.search(f"{h['indicador']} {h['nota']}")
        assert set(h) >= {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "clasificacion_v18", "nota"}
    informe = (carpeta / "informe.md").read_text(encoding="utf-8")
    assert "análisis v18; capa c4; pre-registro interno plan-replicacion-v18" in informe.lower()
    assert not pat.search(informe)


def test_estimabilidad_antes_de_estimar_en_el_registry():
    for estudio in ("e2", "e8"):
        f = SALIDAS / estudio / "registry.csv"
        if not f.exists():
            pytest.skip("sin salidas")
        reg = pd.read_csv(f)
        pre = reg[reg.fase.str.contains("prereg")]
        est = reg[reg.fase.str.contains("estimada|no-estimada")]
        assert len(pre) > 0 and reg.index[reg.fase.str.contains("prereg")].max() < reg.index[reg.fase.str.contains("estimada|no-estimada")].min()
        assert pre.coef_interes.isna().all()                       # ningún coeficiente al registrar
        assert len(est) > 0
