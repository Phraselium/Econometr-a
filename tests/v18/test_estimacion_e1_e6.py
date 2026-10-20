"""V18 · fase 4 · E1 (vivienda turística) y E6 (obra nueva): que el sellado se aplica, que el MDE y el IV se comportan, que las pilas de E6 asignan bien tratadas y controles y que las
salidas cumplen el formato (capa C4, EXPLORATORIO, clasificacion_v18, sin lenguaje causal).

Los tests no abren data/sealed ni estiman con datos reales: usan paneles sintéticos y los manifiestos de sellado (solo metadatos). Las comprobaciones de salidas se omiten si todavía no se han generado.
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
import e1_estim as E1  # noqa: E402
import e1_nucleo as N  # noqa: E402
import e6_diseno as G6  # noqa: E402
import e6_estim as E6  # noqa: E402

DIR = RAIZ / "src" / "v18" / "estimacion"
SALIDAS = RAIZ / "output" / "v18" / "estimacion"
MODULOS = ("e1_adquisicion.py", "e1_datos.py", "e1_diseno.py", "e1_estim.py", "e1_mde.py", "e1_nucleo.py", "e1_resultados.py", "e1_salidas.py", "e1_turismo.py",
           "e6_datos.py", "e6_diseno.py", "e6_estim.py", "e6_obra_nueva.py", "e6_salidas.py")
CAUSAL = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)


# ------------------------------------------------------------------------------------------------ sellado y prohibiciones
def test_toda_lectura_de_datos_territoriales_pasa_por_el_filtro_de_sellado():
    permitido = ("K.filtrar(", "sellado.mascara_v15_v16", "excluir_sellados_v6", "desviación D3", "viviendas_censo2021", "diccionario", "correspondencia", "geometría", "geopandas")
    for nombre in ("e1_datos.py", "e1_diseno.py", "e1_estim.py", "e6_datos.py", "e6_diseno.py"):
        txt = (DIR / nombre).read_text(encoding="utf-8")
        for m in re.finditer(r"(pd|gpd)\.read_(csv|parquet|excel)\(", txt):
            linea = txt[: m.start()].count("\n") + 1
            contexto = "\n".join(txt.splitlines()[max(0, linea - 14): linea + 14])
            assert any(p in contexto for p in permitido), f"{nombre}:{linea} lee datos sin filtrar"


def test_sin_acceso_a_muestra_sellada_ni_evaluate():
    for nombre in MODULOS:
        t = (DIR / nombre).read_text(encoding="utf-8")
        assert "evaluate_" not in t.replace("ningún `evaluate_*`", "").replace("evaluate_*", "")
        assert "sellar_v" not in t
        assert "data/sealed" not in re.sub(r"(?i)nunca (se abre )?data/sealed", "", t)


def test_semilla_unica_y_sin_heredoc_sin_comillas():
    assert K.SEMILLA == 20261010 and N.SEMILLA == 20261010 and E1.SEMILLA == 20261010
    for nombre in MODULOS:
        t = (DIR / nombre).read_text(encoding="utf-8")
        assert "<<EOF" not in t and "<< EOF" not in t


# ------------------------------------------------------------------------------------------------ núcleo econométrico
def _panel_iv(seed=1, n=300, T=6, beta=0.5, fuerza=1.0, cl_n=30):
    rng = np.random.default_rng(seed)
    z_s = rng.normal(size=n)
    cu = rng.integers(0, cl_n, size=n)
    filas = []
    for s in range(n):
        for t in range(T):
            z = z_s[s] * (t + 1)
            x = fuerza * 0.5 * z + rng.normal() + 0.3 * (t) + 0.5 * z_s[s]
            conf = rng.normal() * 0.5
            y = beta * x + 0.4 * conf + rng.normal() * 0.3 + 0.2 * s % 3
            filas.append({"u": s, "t": t, "cl": cu[s], "x": x + conf, "z": z, "y": y + 0.0})
    return pd.DataFrame(filas)


def test_iv_ajustar_con_instrumento_fuerte_recupera_el_efecto_y_ar_lo_contiene():
    d = _panel_iv(beta=0.5)
    r = N.iv_ajustar(d, "y", "x", "z")
    assert r["F_efectivo"] > 10
    assert abs(r["beta"] - 0.5) < 0.25
    tipo, lo, hi = r["ar_ic"]
    assert tipo == "intervalo" and lo < 0.5 < hi


def test_iv_con_instrumento_nulo_no_alcanza_potencia_y_el_mde_no_esta_definido():
    d = _panel_iv(fuerza=0.0, seed=3)
    d["z"] = np.random.default_rng(9).normal(size=len(d))           # instrumento sin relación con x
    r = N.iv_ajustar(d, "y", "x", "z")
    assert r["F_efectivo"] < 10
    R = np.random.default_rng(2).normal(size=(d.u.nunique(), 6)) * 0.3
    pool = N.PoolResiduos(R, d.drop_duplicates("u").sort_values("u").cl.values)
    m = N.mde_iv_ar(r, pool, d.u.values, d.t.values, T=6, R=300)
    assert (not np.isfinite(m["mde80"])) or m["mde80"] > 3.0       # con primera etapa nula: sin potencia o MDE enorme


def test_mde_ols_determinista_y_escala_con_la_sigma():
    rng = np.random.default_rng(4)
    n, T, G = 120, 6, 24
    unit = np.repeat(np.arange(n), T)
    time = np.tile(np.arange(T), n)
    cl = np.arange(n) % G
    dos = rng.normal(size=n)
    d = dos[unit] * (time >= 3)
    M = K.Modelo(np.zeros(n * T), d, unit, time, cluster=cl[unit])

    def mde(sig):
        R = rng.normal(size=(n, T)) * sig
        pool = N.PoolResiduos(R, cl)
        return N.mde_ols(M, pool, unit, time, T=T, R=300)

    a1, a2 = mde(0.1), mde(0.1)
    assert np.isfinite(a1["mde80"]) and a1["mde80"] > 0
    assert mde(0.2)["mde80"] > 1.6 * a1["mde80"]
    pool = N.PoolResiduos(np.random.default_rng(5).normal(size=(n, T)) * 0.1, cl)
    assert N.mde_ols(M, pool, unit, time, T=T, R=200)["mde80"] == N.mde_ols(M, pool, unit, time, T=T, R=200)["mde80"]      # determinista (SEED fijo)
    assert a1["tamano_nominal"] < 0.15 and a2 is not None


def test_pool_de_residuos_conserva_dimensiones_y_es_reproducible():
    R = np.arange(40, dtype=float).reshape(10, 4)
    cl = np.array([0, 0, 1, 1, 2, 2, 3, 3, 4, 4])
    pool = N.PoolResiduos(R, cl)
    a = pool.sortear(np.random.default_rng(1), 9)
    b = pool.sortear(np.random.default_rng(1), 9)
    assert a.shape == (10, 9) and (a == b).all()
    assert set(np.unique(a)) <= set(R.ravel())                      # solo valores observados del periodo previo


def test_evento_dosis_detecta_tendencia_previa_y_no_la_inventa():
    rng = np.random.default_rng(6)
    n, anios = 400, list(range(2011, 2020))
    dosis = rng.normal(size=n)
    cl = np.arange(n) % 40

    def panel(pend):
        filas = []
        for s in range(n):
            for a in anios:
                filas.append({"u": s, "t": a - 2011, "cl": cl[s], "anio": a, "D": dosis[s], "y": pend * dosis[s] * (a - 2013) + rng.normal() * 0.1 + 0.05 * s % 2})
        return pd.DataFrame(filas)

    sin = N.pretendencias(N.evento_dosis(panel(0.0), "y", "D", anios, 2013), 2013)
    con = N.pretendencias(N.evento_dosis(panel(0.05), "y", "D", anios, 2013), 2013)
    assert con["p"] < 0.01 < sin["p"] or con["p"] < sin["p"] / 10
    assert sin["pendiente_detectable"] > 0
    ev = N.evento_dosis(panel(0.0), "y", "D", anios, 2013)
    assert N.media_posterior(ev, 2013)["se"] > 0


def test_absorber_map_coincide_con_modelo_de_efectos_fijos():
    rng = np.random.default_rng(8)
    n, T = 80, 5
    u = np.repeat(np.arange(n), T)
    t = np.tile(np.arange(T), n)
    x = rng.normal(size=n * T) + 0.5 * u % 3
    y = 0.3 * x + rng.normal(size=n * T) + u * 0.01
    yt, xt = E1.absorber([y, x], [u, t])
    beta = float(xt @ yt / (xt @ xt))
    assert beta == pytest.approx(K.Modelo(y, x, u, t).beta, rel=1e-6)


def test_p_corr_y_bandas_de_monte_carlo():
    assert K.p_corr(0.03, 0.05) == 0.03
    assert K.p_corr(0.03, 0.0785) == pytest.approx(0.03 * 0.0785 / 0.05)
    assert K.banda_mc(0.045) == "apta" and K.banda_mc(0.0785) == "con valor crítico corregido" and K.banda_mc(0.17) == "no fiable"


# ------------------------------------------------------------------------------------------------ E6: pilas
def _base_sintetica():
    cods = [f"46901{i:05d}" for i in range(1, 8)]               # s1..s7 en cadena
    adj = {c: set() for c in cods}
    for a, b in zip(cods[:-1], cods[1:]):
        adj[a].add(b)
        adj[b].add(a)
    edif = pd.DataFrame({"cod_seccion": [cods[1], cods[5]], "viviendas": [30, 30], "anio": [2016, 2023], "x": [0.0, 0.0], "y": [0.0, 0.0]})
    anios = list(range(2011, 2025))
    sp = pd.DataFrame(10.0 + np.arange(len(anios))[None, :] * 0.1 + np.arange(len(cods))[:, None] * 0.01, index=cods, columns=anios)
    cen = pd.DataFrame({"x": np.arange(len(cods)) * 500.0, "y": 0.0}, index=cods)
    return {"ok": set(cods), "adj": adj, "edif": edif, "sp": {"VC": sp, "VU": sp}, "centroides": cen, "secs": None}, cods


def test_pilas_de_e6_asignan_tratadas_y_controles_con_la_regla_de_la_adenda():
    B, c = _base_sintetica()
    r = G6.construir(B, cohortes=[2016])
    d = r["datos"]
    tr = set(d[d.tr == 1].cod_seccion)
    co = set(d[d.tr == 0].cod_seccion)
    assert tr == {c[0], c[2]}                                       # contiguas al edificio de 2016 (s2), sin la propia (s2)
    assert co == {c[4], c[6]}                                       # contiguas al edificio de 2023 (s6): terminado en T+6 o después
    assert c[1] not in tr | co and c[5] not in tr | co              # la sección del edificio no se mide (adenda AD-E6-R1)
    assert d.k.min() == -5 and d.k.max() == 3                       # ventana T−4..T+4; k = 0 es T+1
    assert (d[d.anio == 2017].k == 0).all()


def test_pilas_de_e6_excluyen_unidades_con_vecina_sellada_y_controles_tempranos():
    B, c = _base_sintetica()
    B2 = {**B, "ok": set(c) - {c[3]}}                              # s4 sellada: s3 y s5 quedan sin exposición observable
    B2["edif"] = B["edif"][B["edif"].cod_seccion.isin(B2["ok"])]
    r = G6.construir(B2, cohortes=[2016])
    assert c[2] not in set(r["datos"].cod_seccion)                  # vecina sellada
    B3 = {**B, "edif": pd.DataFrame({"cod_seccion": [c[1], c[5]], "viviendas": [30, 30], "anio": [2016, 2020], "x": [0.0, 0.0], "y": [0.0, 0.0]})}
    r3 = G6.construir(B3, cohortes=[2016])
    assert (r3["datos"].tr == 0).sum() == 0 if len(r3["datos"]) else True   # 2020 < 2016 + 6: no es control
    B4 = {**B, "edif": pd.DataFrame({"cod_seccion": [c[1]], "viviendas": [15], "anio": [2016], "x": [0.0], "y": [0.0]})}
    assert len(G6.construir(B4, cohortes=[2016])["datos"]) == 0     # por debajo del umbral de 20 viviendas


def test_estimador_de_e6_recupera_un_efecto_sintetico_y_las_pretendencias_no_rechazan():
    rng = np.random.default_rng(11)
    filas = []
    for E in (2015, 2016):
        for j in range(60):
            tr = j < 25
            bs = f"b{E}_{j // 2}"
            for a in range(E - 4, E + 5):
                k = a - (E + 1)
                y = 0.02 * (a - E) + 0.1 * (j % 7) + rng.normal() * 0.05 - (0.12 if (tr and 0 <= k <= 3) else 0.0)
                filas.append({"pila": E, "cod_seccion": f"s{E}_{j}", "anio": a, "y": y, "tr": int(tr), "k": k, "bsec": bs, "mun": "46250"})
    d = pd.DataFrame(filas)
    d["unit_pila"] = d.pila.astype(str) + "_" + d.cod_seccion
    d["anio_pila"] = d.pila.astype(str) + "_" + d.anio.astype(str)
    d["mun_anio_pila"] = d.pila.astype(str) + "_" + d.mun + "_" + d.anio.astype(str)
    secs = pd.DataFrame({"cod_seccion": d.cod_seccion.unique(), "x": 0.0, "y": 0.0})
    dd = E6.preparar(d, secs)
    r = E6.estimar(dd)
    assert abs(r["coef"] - (-0.12)) < 0.04 and r["p_t"] < 0.01
    ev = E6.evento(dd)
    assert ev["pretend"]["p"] > 0.05
    assert E6.placebo_fecha(dd)["p"] > 0.05


# ------------------------------------------------------------------------------------------------ salidas
@pytest.mark.parametrize("estudio", ["e1", "e6"])
def test_salidas_cumplen_el_formato_c4_exploratorio_y_sin_lenguaje_causal(estudio):
    ruta = SALIDAS / estudio / "hechos.json"
    if not ruta.exists():
        pytest.skip("salidas todavía no generadas")
    hechos = json.loads(ruta.read_text(encoding="utf-8"))
    assert hechos
    for h in hechos:
        assert h["id"].startswith(f"V18-{estudio.upper()}-")
        assert h["capa"] == "C4"
        assert h["clasificacion_v18"] in {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
        assert h["fuentes"]
        assert not CAUSAL.search(f"{h['indicador']} {h['nota']}")
    res = json.loads((SALIDAS / estudio / "resultado.json").read_text(encoding="utf-8"))
    for clave in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas", "clasificacion_v18"):
        assert clave in res
    assert res["capa"] == "C4" and res["nivel_evidencia"] == "EXPLORATORIO"
    inf = (SALIDAS / estudio / "informe.md").read_text(encoding="utf-8")
    assert "análisis v18; capa c4; pre-registro interno plan-replicacion-v18" in inf.lower()
    assert not CAUSAL.search(inf)
    for f in ("tabla.csv", "registro.csv", "mde.csv"):
        assert (SALIDAS / estudio / f).exists()


def test_e1_r4_principal_es_el_anillo_y_la_clase_exige_el_tost_con_ic90_de_webb():
    g = pd.DataFrame({"cod_seccion": ["a", "b", "c", "d"], "dist_sf": [0.2, 0.7, 1.4, 0.49], "sellada": [False, False, False, True]})
    c = E1.r4_conteos(g)
    assert (c["radio_total"], c["anillo_total"], c["radio_no_sellado"]) == (2, 1, 1)          # el control principal es solo el anillo de 500-1.000 m
    assert E1.DELTA["E1-R4"] == 0.05
    ruta = SALIDAS / "e1" / "resultado.json"
    if not ruta.exists():
        pytest.skip("salidas todavía no generadas")
    res = json.loads(ruta.read_text(encoding="utf-8"))
    t = res["diagnosticos"]["E1-R4"]["tost_delta_0_05"]
    lo, hi = t["ic90_webb"]
    assert t["equivalente"] == (lo > -0.05 and hi < 0.05)
    clase = res["clasificaciones"]["E1-R4"]
    assert ("nulo acotado" in clase) == t["equivalente"]
    if not t["equivalente"]:
        assert clase.startswith(("NO CONCLUYENTE", "SUGESTIVO", "ASOCIACIÓN")) and "nulo acotado" not in clase
    tabla = pd.read_csv(SALIDAS / "e1" / "tabla.csv").set_index("id")
    assert "E1-R4-v1" in tabla.index and "resto de Barcelona" in tabla.loc["E1-R4-v1", "resultado"]


def test_e1_r4_k8_bis_principal_sin_adelantos_y_variante_con_adelantos():
    ruta = SALIDAS / "e1" / "resultado.json"
    if not ruta.exists():
        pytest.skip("salidas todavía no generadas")
    res = json.loads(ruta.read_text(encoding="utf-8"))
    d = res["diagnosticos"]["E1-R4"]
    v3 = d["variante_con_adelantos_E1-R4-v3"]
    lo, hi = v3["ic90_webb"]
    assert v3["equivalente"] == (lo > -0.05 and hi < 0.05)
    assert ("nulo acotado" in res["clasificaciones"]["E1-R4-v3"]) == v3["equivalente"]
    t = d["tost_delta_0_05"]
    if not t["equivalente"]:
        assert res["clasificaciones"]["E1-R4"].startswith("NO CONCLUYENTE")
    tabla = pd.read_csv(SALIDAS / "e1" / "tabla.csv").set_index("id")
    assert "estudio de eventos con adelantos" in tabla.loc["E1-R4-v3", "resultado"]
    assert "sin los adelantos" in tabla.loc["E1-R4", "resultado"]
    assert tabla.loc["E1-R4-v3", "coef"] == pytest.approx(v3["coef"])
