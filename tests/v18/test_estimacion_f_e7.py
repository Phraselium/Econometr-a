"""V18 · fase 4 · F1-F4 y E7 (src/v18/estimacion/f_nucleo.py, f_datos.py, f_conjunto.py y e7_tipos.py).

Los tests de núcleo usan datos simulados con SEED 20261010; los de datos comprueban el filtro de sellado y los topes; los de salida (si existen) comprueban las
cifras V18 de output/v18/estimacion/{f_conjunto,e7} con las mismas reglas que check_v18 (id V18-, capa C4, clase válida, sin lenguaje causal).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "estimacion"))
sys.path.insert(0, str(RAIZ / "src"))
import f_nucleo as N  # noqa: E402

SEED = 20261010
CLASES = {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
CAUSAL = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)


# ---------------------------------------------------------------------------------------------- núcleo
def _coint_series(rng, T=200, alpha=-0.2, beta=0.8):
    x = np.cumsum(rng.normal(size=T))
    y = np.zeros(T)
    for t in range(1, T):
        y[t] = y[t - 1] + alpha * (y[t - 1] - beta * x[t - 1]) + rng.normal() * 0.5
    return y, x


def test_uecm_recupera_velocidad_y_largo_plazo():
    rng = np.random.default_rng(SEED)
    y, x = _coint_series(rng, 600)
    r = N.uecm(y, x, p=1)
    assert -0.32 < r["alpha"] < -0.10
    assert abs(r["beta_lp"][0] - 0.8) < 0.15
    assert r["t"] < -3 and r["F"] > 5


def test_contraste_de_limites_rechaza_con_cointegracion_y_no_bajo_la_nula():
    rng = np.random.default_rng(SEED)
    y, x = _coint_series(rng, 200)
    c = N.contraste_limites(y, x, p=1, B=300, seed=SEED, B_val=200)
    assert c["p"] < 0.05
    y0 = np.cumsum(rng.normal(size=200))
    x0 = np.cumsum(rng.normal(size=200))
    c0 = N.contraste_limites(y0, x0, p=1, B=300, seed=SEED, B_val=200)
    assert c0["p"] > 0.01
    assert 0.0 <= c0["tamano_conjunto_5pct"] <= 0.12


def test_uecm_con_mascara_omite_filas():
    rng = np.random.default_rng(SEED)
    y, x = _coint_series(rng, 120)
    m = np.ones(120, bool)
    m[40:60] = False
    assert N.uecm(y, x, 1, m)["n"] == N.uecm(y, x, 1)["n"] - 20


def test_dols_propio_coincide_con_econ_utils():
    from econ_utils import dols
    rng = np.random.default_rng(SEED)
    x = np.cumsum(rng.normal(size=(150, 2)), axis=0)
    y = x @ np.array([0.5, -0.2]) + rng.normal(size=150)
    df = pd.DataFrame({"y": y, "a": x[:, 0], "b": x[:, 1]}, index=pd.period_range("1990Q1", periods=150, freq="Q"))
    ref = dols(df, "y", ["a", "b"], k=1, maxlags=4)
    mio = N.dols_ts(y, x, k=1, maxlags=4)
    assert np.allclose(ref["beta"].to_numpy(), mio["beta"], atol=1e-10)
    assert np.allclose(ref["res"].bse[["a", "b"]].to_numpy(), mio["se"], atol=1e-8)


def _panel(rng, n=24, t=20, k=2, coint=True):
    X = np.cumsum(rng.normal(size=(n, t, k)), axis=1)
    if coint:
        Y = X @ np.array([0.6, -0.3]) + rng.normal(size=(n, t)) * 0.3
    else:
        Y = np.cumsum(rng.normal(size=(n, t)), axis=1)
    return Y, X


def test_pmg_y_dols_de_panel_recuperan_el_largo_plazo():
    rng = np.random.default_rng(SEED)
    Y, X = _panel(rng)
    p = N.pmg(Y, X)
    assert np.allclose(p["theta"], [0.6, -0.3], atol=0.12)
    assert p["phi_medio"] < -0.5
    d = N.panel_dols(Y, X)
    assert np.allclose(d["beta"], [0.6, -0.3], atol=0.12)
    assert np.all(d["se_dk"] > 0) and np.all(d["se_cluster"] > 0)


def test_contraste_de_panel_distingue_cointegracion():
    rng = np.random.default_rng(SEED)
    Y, X = _panel(rng, coint=True)
    assert N.coint_panel_bootstrap(Y, X, 199, SEED)["p"] < 0.05
    Y0, X0 = _panel(rng, coint=False)
    assert N.coint_panel_bootstrap(Y0, X0, 199, SEED)["p"] > 0.02


def test_csardl_grupo_medio_recupera_el_largo_plazo():
    rng = np.random.default_rng(SEED)
    X = np.cumsum(rng.normal(size=(20, 40, 1)), axis=1)
    Y = X[:, :, 0] * 0.5 + rng.normal(size=(20, 40)) * 0.2
    r = N.csardl_mg(Y, X, estatico=True)
    assert abs(r["theta_mg"][0] - 0.5) < 0.1


def test_iv_panel_fe_recupera_beta_con_instrumento_valido():
    rng = np.random.default_rng(SEED)
    n, t = 30, 12
    z = rng.normal(size=(n, t))
    u = rng.normal(size=(n, t))
    x = 0.8 * z + 0.5 * u + rng.normal(size=(n, t)) * 0.3
    y = 0.7 * x + u + rng.normal(size=(n, 1))
    r = N.iv_panel_fe(y, x, None, z[:, :, None])
    assert abs(r["beta"] - 0.7) < 0.15
    assert r["F_primera_etapa"] > 10 and r["gl"] == n - 1


def test_mde_mc_es_positivo_y_proporcional_a_la_desviacion():
    def sim(s):
        def f(rng):
            b = rng.normal() * s
            return b, s
        return f
    a, b = N.mde_mc(sim(1.0), 400, SEED), N.mde_mc(sim(2.0), 400, SEED)
    assert 2.0 < a["mde"] < 3.5
    assert abs(b["mde"] / a["mde"] - 2) < 0.05


def test_fuera_de_muestra_bloques_con_embargo_no_filtra_el_entrenamiento():
    for tr, te in N.bloques_embargo(100, 5, 4):
        assert len(set(tr) & set(te)) == 0
        assert not any(abs(a - b) <= 4 for a in te[[0, -1]] for b in tr[(tr >= te[0] - 4) & (tr <= te[-1] + 4)])


def test_dm_cw_gw_y_mcs_sobre_modelos_conocidos():
    rng = np.random.default_rng(SEED)
    n = 300
    e_mal = rng.normal(size=n) * 2
    e_bien = rng.normal(size=n)
    m = N.mcs({"mal": e_mal ** 2, "bien": e_bien ** 2}, B=199, alfa=0.10, seed=SEED)
    assert m["en_mcs"] == ["bien"]
    gw = N.giacomini_white(e_bien, e_mal)
    assert gw["p"] < 0.05
    cw = N.clark_west(e_bien, e_mal, np.zeros(n), np.zeros(n))
    assert "CW" in cw


def test_holm_y_by_de_las_variantes():
    from f_conjunto import by_adjust
    q = by_adjust([0.001, 0.02, 0.5])
    assert q[0] <= q[1] <= q[2] and all(0 <= v <= 1 for v in q)
    assert q[0] >= 0.001


# ---------------------------------------------------------------------------------------------- E7: LP-IV propio frente a la herramienta
def test_lp_iv_con_controles_vacios_coincide_con_la_herramienta():
    import e7_tipos as E
    from src.v18.herramientas import lp_iv as L
    rng = np.random.default_rng(SEED)
    T = 120
    z = rng.normal(size=T)
    x = 0.5 * z + rng.normal(size=T)
    y = np.cumsum(rng.normal(size=T)) + 0.3 * np.cumsum(x)
    a = L.lp_iv(y, x, z, 8, 0, 4)
    b = E.lp_iv_ctrl(y, x, z, [], 8, 4, 0)
    assert abs(a["beta"] - b["beta"]) < 1e-9 and a["n"] == b["n"]
    assert np.allclose(a["Om"], b["Om"])


def test_mde_lp_es_infinito_con_primera_etapa_nula_y_finito_con_fuerte():
    import e7_tipos as E
    rng = np.random.default_rng(SEED)
    zt = rng.normal(size=100)
    debil = E.mde_lp(zt, 0.0, 1.0, 5.0, 8, 300)
    fuerte = E.mde_lp(zt, 2.0, 1.0, 5.0, 8, 300)
    assert not np.isfinite(debil["mde"])
    assert np.isfinite(fuerte["mde"]) and fuerte["mde"] < 5


def test_clasificacion_e7_respeta_el_gate_y_la_regla_de_la_f():
    import e7_tipos as E
    sp = {"estimable": False, "mde": {"mde": float("inf")}, "umbral": 2.0, "res": {"F": 3.0, "ar": ("recta", np.nan, np.nan)}}
    assert E.clasificar_lp(sp, None, None, None)[0] == "NO ESTIMABLE"
    sp["estimable"] = True
    assert E.clasificar_lp(sp, None, 0.5, None)[0] == "ASOCIACIÓN"            # F < 5 con AR no acotado: fallo decisivo
    sp["res"] = {"F": 7.0, "ar": ("acotado", -3.0, -0.5)}
    assert E.clasificar_lp(sp, None, 0.01, 1.0)[0] == "SUGESTIVO"             # F < 10: tope SUGESTIVO (R-9)
    sp["res"] = {"F": 20.0, "ar": ("acotado", -3.0, -0.5)}
    assert E.clasificar_lp(sp, None, 0.01, 1.0)[0] == "IDENTIFICADO"


def test_etiqueta_i6_razon_entre_un_tercio_y_tres():
    import e7_tipos as E
    assert E.etiqueta_i6(-2.5, -2.0).startswith("coherente")
    assert E.etiqueta_i6(+2.0, -2.0).startswith("no coherente")
    assert E.etiqueta_i6(-9.0, -2.0).startswith("no coherente")


# ---------------------------------------------------------------------------------------------- datos y sellado
@pytest.fixture(scope="module")
def datos():
    import f_datos as D
    return D


def test_codigo_provincia_y_cantabria_uniprovincial(datos):
    assert datos.codigo_provincia("Coruña (A)") == "15"
    assert datos.codigo_provincia("Palmas (Las)") == "35"
    assert datos.codigo_provincia("Araba/Alava") == "01"
    assert datos.codigo_provincia("Valencia/València") == "46"
    assert datos.codigo_provincia("Cantabria") == "39"


def test_series_nacionales_respetan_los_topes(datos):
    n = datos.nacional_t()
    assert str(n.index[-1]) <= "2026Q2" and str(n.index[0]) >= "1999Q1"
    a = datos.nacional_a()
    assert a.index.max() <= 2025 and a.index.min() >= 2001


def test_panel_provincial_sin_unidades_selladas_ni_periodos_posteriores(datos):
    import holdout
    P = datos.panel_prov()
    assert P.anio.max() <= 2025
    sellada = set(holdout.provincias_selladas_v6())
    assert not (set(P.prov) & sellada)
    assert P.loc[P.vt.notna(), "anio"].max() <= 2024               # valor tasado anual: tope 2024
    C = datos.panel_ccaa_oferta()
    assert C.anio.max() <= 2024 and C.ccaa.nunique() == 9
    assert not (set(C.ccaa) & set(holdout.ccaa_selladas_v6()))


def test_choques_trimestrales_hasta_2025t3_y_ficheros_identicos():
    import e7_tipos as E
    q = E.choques_trimestrales()
    assert str(q.index[-1]) == "2025Q3" and str(q.index[0]) == "1999Q1"
    j = pd.read_csv(E.JK)
    m = j[(j.year == 2001) & (j.month.isin([1, 2, 3]))].MP_median.sum()
    assert abs(q.loc[pd.Period("2001Q1", "Q"), "z_med"] - m) < 1e-12
    assert hashlib.sha256(E.JK.read_bytes()).hexdigest() == hashlib.sha256(E.JK_RAW.read_bytes()).hexdigest()


def test_exposicion_hipotecaria_entre_cero_y_uno_y_sin_provincias_selladas():
    import e7_tipos as E
    import holdout
    e = E.exposicion_hipoteca(2007, 2019)
    assert len(e) >= 30 and e.min() > 0 and e.max() < 1.5
    assert not (set(e.index) & set(holdout.provincias_selladas_v6()))


# ---------------------------------------------------------------------------------------------- salidas
SALIDAS = [RAIZ / "output" / "v18" / "estimacion" / d for d in ("f_conjunto", "e7")]


@pytest.mark.parametrize("carpeta", SALIDAS)
def test_cifras_v18_de_las_salidas(carpeta):
    h = carpeta / "hechos.json"
    if not h.exists():
        pytest.skip("la salida aún no se ha generado")
    hechos = json.loads(h.read_text(encoding="utf-8"))
    assert hechos
    pref = "V18-F" if carpeta.name == "f_conjunto" else "V18-E7"
    claves = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "clasificacion_v18", "nota"}
    for x in hechos:
        assert claves <= set(x), x["id"]
        assert x["id"].startswith(pref)
        assert x["capa"] == "C4" and x["clasificacion_v18"] in CLASES
        assert x["fuentes"]
        assert not CAUSAL.search(f"{x['indicador']} {x['nota']}"), x["id"]
        assert "plan-replicacion-v18" in x["nota"]
    r = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    assert r["nivel_evidencia"] == "EXPLORATORIO" and r["capa"] == "C4" and "clasificacion_v18" in r
    assert "plan-replicacion-v18" in (carpeta / "informe.md").read_text(encoding="utf-8")


def test_f_sin_cointegracion_no_publica_largo_plazo_ni_sobrevaloracion():
    carpeta = SALIDAS[0]
    if not (carpeta / "tabla.csv").exists():
        pytest.skip("la salida aún no se ha generado")
    t = pd.read_csv(carpeta / "tabla.csv")
    sin = t[(t.estado == "principal") & (t.coint_rechaza_5pct == False)]            # noqa: E712
    assert (sin.publica_largo_plazo == False).all()                                  # noqa: E712
    r = json.loads((carpeta / "resultado.json").read_text(encoding="utf-8"))
    if r["diagnosticos"]["especificaciones_con_cointegracion_rechazada"] == 0:
        assert t.loc[t.id == "F1-A3", "clasificacion_v18"].iloc[0] == "NO ESTIMABLE"
        assert (t.loc[t.id.str.startswith("F4-"), "clasificacion_v18"] == "NO ESTIMABLE").all()


def test_f_y_e7_sin_nada_en_clase_identificado_si_el_gate_falla():
    for c in SALIDAS:
        if not (c / "tabla.csv").exists():
            pytest.skip("la salida aún no se ha generado")
    f = pd.read_csv(SALIDAS[0] / "tabla.csv")
    assert not (f.clasificacion_v18 == "IDENTIFICADO").any()                          # F: tope ASOCIACIÓN
    e = pd.read_csv(SALIDAS[1] / "tabla.csv")
    gate = e[e.estimable == False]                                                    # noqa: E712
    assert not gate.clasificacion_v18.isin(["IDENTIFICADO", "SUGESTIVO", "NO CONCLUYENTE"]).any()
