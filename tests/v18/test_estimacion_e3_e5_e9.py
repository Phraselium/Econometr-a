"""V18 · fase 4 · pruebas de E3 (inmigración), E5 (oferta) y E9 (no residentes): herramientas comunes, sellado, orden MDE-antes-de-estimar y contrato de las salidas.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. SEED 20261010. Las pruebas que leen datos usan solo lo versionado; las de salidas se omiten si el módulo
todavía no se ha ejecutado.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "estimacion"))
import _e359_comun as K  # noqa: E402

CLASES = {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
CAUSAL = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)
OUT = RAIZ / "output" / "v18" / "estimacion"
SRC = RAIZ / "src" / "v18" / "estimacion"


def _panel(G=39, T=7, seed=1, pi=0.6, beta=0.3):
    rng = np.random.default_rng(seed)
    prov = np.repeat(np.arange(G), T)
    yr = np.tile(np.arange(T), G)
    reg = prov % 5
    C = np.column_stack([(reg == r) * (yr == t) for r in range(5) for t in range(T)]).astype(float)
    w = rng.uniform(1, 3, G)[prov]
    z = rng.standard_normal(len(prov))
    v = rng.standard_normal(G)[prov] * 0.5 + rng.standard_normal(len(prov))
    x = pi * z + v
    y = beta * x + 0.7 * v + rng.standard_normal(len(prov))
    return y, x, z, prov, C, w, yr


def test_grupos_equivale_a_proyeccion_densa():
    rng = np.random.default_rng(3)
    G, T = 39, 7
    prov = np.repeat(np.arange(G), T)
    yr = np.tile(np.arange(T), G)
    w = rng.uniform(1, 3, G)[prov]
    z = rng.standard_normal(len(prov))
    x = 0.5 * z + rng.standard_normal(len(prov))
    y = 0.3 * x + rng.standard_normal(len(prov))
    py = np.array([f"{p // 3}_{t}" for p, t in zip(prov, yr)])
    cl = prov // 3
    D = (py[:, None] == np.unique(py)[None]).astype(float)
    a = K.DisenoIV(y, x, z, cl, C=D, w=w, B=199)
    b = K.DisenoIV(y, x, z, cl, w=w, B=199, grupos=py)
    assert abs(a.iv()["beta"] - b.iv()["beta"]) < 1e-9
    assert abs(a.webb_ar_p(0.1) - b.webb_ar_p(0.1)) < 1e-12
    assert a.k == b.k


def test_grupos_con_orden_de_aparicion_no_monotono():
    """Regresión del fallo de reduceat con etiquetas de grupo no monótonas respecto al conglomerado."""
    rng = np.random.default_rng(5)
    n = 600
    cl = rng.integers(0, 12, n)
    gr = np.array([f"{c}_{t}" for c, t in zip(cl, rng.integers(0, 4, n))])
    gr = gr[rng.permutation(n)] if False else gr
    z = rng.standard_normal(n)
    x = 0.6 * z + rng.standard_normal(n)
    y = 0.2 * x + rng.standard_normal(n)
    D = (gr[:, None] == np.unique(gr)[None]).astype(float)
    a = K.DisenoIV(y, x, z, cl, C=D, B=50)
    b = K.DisenoIV(y, x, z, cl, B=50, grupos=gr)
    assert abs(a.iv()["beta"] - b.iv()["beta"]) < 1e-9


def test_inferencia_por_provincia_cobertura_razonable():
    """Tamaño al 5 % de t(G-1), AR exacto y Webb-AR cerca del nominal con 39 clusters y efectos región-año (200 réplicas: banda ancha)."""
    rt, ra, rw = [], [], []
    for s in range(200):
        y, x, z, prov, C, w, _ = _panel(seed=100 + s)
        d = K.DisenoIV(y, x, z, prov, C=C, w=w, B=199, semilla=s + 1)
        r = d.iv()
        rt.append(abs((r["beta"] - 0.3) / r["se"]) > 2.0244)
        ar = d.ar_exacto()
        ra.append(not (ar["lo"] <= 0.3 <= ar["hi"]) if ar["tipo"] == "intervalo" else False)
        rw.append(d.webb_ar_p(0.3) < 0.05)
    for tasa in (np.mean(rt), np.mean(ra), np.mean(rw)):
        assert 0.01 <= tasa <= 0.11


def test_webb_ar_determinista_e_inversion_contiene_el_2sls():
    y, x, z, prov, C, w, _ = _panel(seed=9)
    a = K.DisenoIV(y, x, z, prov, C=C, w=w, B=499)
    b = K.DisenoIV(y, x, z, prov, C=C, w=w, B=499)
    assert a.webb_ar_p(0.0) == b.webb_ar_p(0.0)
    ic = a.ic_webb_ar(0.05)
    assert ic["lo"] <= a.iv()["beta"] <= ic["hi"]


def test_mde_escala_con_sigma_y_es_determinista():
    y, x, z, prov, C, w, yr = _panel(seed=4)
    d = K.DisenoIV(y, x, z, prov, C=C, w=w, B=1)
    a = K.mde_iv(d, yr[d.orden], 1.0, 0.3, R=400)
    b = K.mde_iv(d, yr[d.orden], 1.0, 0.3, R=400)
    c2 = K.mde_iv(d, yr[d.orden], 2.0, 0.3, R=400)
    assert a["mde80"] == b["mde80"]
    assert 1.6 < c2["mde80"] / a["mde80"] < 2.4
    assert 0.0 <= a["tamano_nulo"] <= 0.12


def test_by_holm_inv_hhi():
    q = K.by_qvalores({"a": 0.001, "b": 0.02, "c": 0.5})
    assert q["a"] <= q["b"] <= q["c"] <= 1.0
    assert K.by_qvalores({}) == {}
    assert abs(K.inv_hhi([1, 1, 1, 1]) - 4.0) < 1e-12
    assert K.inv_hhi([10, 1e-9]) < 1.01
    h = K.holm({"x": 0.01, "y": 0.04})
    assert h["x"] == pytest.approx(0.02) and h["y"] == pytest.approx(0.04)


def test_clasificar_reglas_de_la_adenda():
    base = dict(estimable=True, p_holm=0.01, F_eff=30.0, ar_acotado=True, pretend_p=0.5, roth_ok=True, placebo_fecha_p=0.5, placebo_resultado_p=0.5,
                robustez={"cambio_signo": False, "frac_mismo_signo": 1.0, "solape_ic": True}, rotemberg_ok=True, jrs_ok=True, balance_ok=True, tost={"equivalente": False})
    assert K.clasificar(base)["clase"] == "IDENTIFICADO"
    assert K.clasificar(dict(base, topes=["tope"]))["clase"] == "SUGESTIVO"
    assert K.clasificar(dict(base, F_eff=7.0))["clase"] == "SUGESTIVO"
    assert K.clasificar(dict(base, F_eff=3.0, ar_acotado=False))["clase"] == "ASOCIACIÓN"
    assert K.clasificar(dict(base, pretend_p=0.005))["clase"] == "ASOCIACIÓN"
    assert K.clasificar(dict(base, p_holm=0.5))["clase"] == "NO CONCLUYENTE (sin potencia)"
    assert K.clasificar(dict(base, p_holm=0.5, tost={"equivalente": True}))["clase"] == "IDENTIFICADO (efecto nulo acotado)"
    assert K.clasificar(dict(base, tope_max="SUGESTIVO"))["clase"] == "SUGESTIVO"
    assert K.clasificar({"estimable": False, "motivo_no_estimable": "x"})["clase"] == "NO ESTIMABLE"
    assert K.clasificar({"coprincipal": True})["clase"] == "no se clasifica"


def test_hecho_rechaza_lenguaje_causal_y_clase_corta():
    with pytest.raises(ValueError):
        K.hecho("V18-E3-x", "efecto causal", 1.0, 0, 2, "u", "2002", "c", ["f"], "SUGESTIVO", "n")
    h = K.hecho("V18-E3-x", "asociación", float("nan"), None, None, "u", "2002", "c", ["f"], "NO CONCLUYENTE (sin potencia)", "nota")
    assert h["clasificacion_v18"] == "NO CONCLUYENTE" and h["capa"] == "C4" and h["valor"] is None


def test_manifiesto_ampliado_no_toca_el_fichero_y_filtra_selladas():
    import sellado
    base = sellado.cargar()
    man = K.manifiesto()
    nuevas = set(man["topes"]) - set(base["topes"])
    assert {"eurostat_censo2001_nacionalidad|provincia|A", "eurostat_empleo_nuts3_a10|provincia|A", "eurostat_poblacion_nuts3|provincia|A"} <= nuevas
    assert not (set(base["topes"]) & nuevas)
    assert len(K.PROVINCIAS_ENTRENAMIENTO) == 39
    assert not (set(K.PROVINCIAS_ENTRENAMIENTO) & K.SELLADAS_V6)
    assert set(K.MACRO) == set(K.PROVINCIAS_ENTRENAMIENTO)


def test_paneles_e3_y_e5_no_contienen_provincias_selladas():
    import e3_panel as EP
    d = EP.DatosE3()
    pan = d.panel(dict(ventana=(2002, 2008), x="pp_ext", y="dprecio", peso="pob1998", controles=dict(construccion=True, costa=True), shares="censo2001"))
    assert not (set(pan.prov) & K.SELLADAS_V6)
    assert 2003 not in set(pan.año) and pan.año.max() <= 2008
    assert set(d.vt.index).isdisjoint(K.SELLADAS_V6)


def test_mde_se_calcula_antes_de_estimar_en_el_codigo():
    """Orden del pre-registro (adenda 1.3): en main(), la comprobación previa precede a la estimación."""
    for f in ("e3_inmigracion.py", "e5_oferta.py"):
        t = (SRC / f).read_text(encoding="utf-8")
        i, j = t.index("precomprobar("), t.index("estimar(dat, s, completo")
        assert t.index("precomprobar(dat, s)") < j, f
        assert i < j


def test_codigo_no_abre_muestras_selladas_ni_evaluate():
    for f in ("_e359_comun.py", "_e359_datos.py", "e359_adquisicion.py", "e3_inmigracion.py", "e3_panel.py", "e3_municipal.py", "e3_extra.py", "e3_salidas.py", "e3_texto.py",
              "e5_oferta.py", "e5_salidas.py", "e9_no_residentes.py"):
        t = (SRC / f).read_text(encoding="utf-8")
        assert not re.search(r"evaluate_v\d+\(|sellar_v\d+\(|holdout\.abrir|read_parquet\([^)]*sealed", t), f
        assert "SEED" in t or "SEMILLA" in t or f.startswith("_")


@pytest.mark.parametrize("estudio", ["e3", "e5", "e9"])
def test_contrato_de_las_salidas(estudio):
    d = OUT / estudio
    if not (d / "resultado.json").exists():
        pytest.skip(f"{estudio} sin ejecutar")
    r = json.loads((d / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas", "clasificacion_v18"):
        assert k in r, k
    assert r["capa"] == "C4" and r["nivel_evidencia"] == "EXPLORATORIO"
    assert set(r["fuera_muestra"]) >= {"modelo", "rmse", "dm_vs_ar4"}
    assert r["clasificacion_v18"] in CLASES | {"pendiente"} or r["clasificacion_v18"] is None
    H = json.loads((d / "hechos.json").read_text(encoding="utf-8"))
    assert H
    for h in H:
        assert h["id"].startswith(f"V18-{estudio.upper()}-")
        assert h["capa"] == "C4" and h["clasificacion_v18"] in CLASES and (h.get("fuentes") or h.get("fuente"))
        for k in ("indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "nota"):
            assert k in h
        assert not CAUSAL.search(f"{h['indicador']} {h['nota']}")
    inf = (d / "informe.md").read_text(encoding="utf-8")
    assert "análisis V18; capa C4; pre-registro interno plan-replicacion-v18" in inf
    assert (d / "tabla.csv").exists() and (d / "registro.csv").exists()


def test_e9_es_no_estimable_por_choques_efectivos():
    f = OUT / "e9" / "resultado.json"
    if not f.exists():
        pytest.skip("e9 sin ejecutar")
    r = json.loads(f.read_text(encoding="utf-8"))
    v = r["diagnosticos"]["inv_hhi"]["origenes_con_serie_de_riesgo|sin pesos"]["inv_hhi"]
    assert v < r["diagnosticos"]["umbral"] == 10
    for sid in ("E9-R1", "E9-R2", "E9-A1", "E9-A2", "E9-X1", "E9-X2"):
        assert r["especificaciones"][sid]["clasificacion_v18"] == "NO ESTIMABLE"
    assert r["estimacion"] is None


def test_e3_publica_mde_y_solo_estima_lo_estimable():
    f = OUT / "e3" / "resultado.json"
    if not f.exists():
        pytest.skip("e3 sin ejecutar")
    r = json.loads(f.read_text(encoding="utf-8"))
    mde = r["diagnosticos"]["mde"]
    for sid, m in mde.items():
        esp = r["especificaciones"][sid]
        if m["estimable"]:
            assert esp["clasificacion_v18"] != "NO ESTIMABLE"
        else:
            assert esp["clasificacion_v18"] == "NO ESTIMABLE" and "estimacion" not in esp
    assert r["diagnosticos"]["estado_I8"].startswith("pendiente")
    fam = r["diagnosticos"]["familia_holm"]
    assert fam["m"] == len(fam["p_ajustados"]) and all(0 <= p <= 1 for p in fam["p_ajustados"].values())
