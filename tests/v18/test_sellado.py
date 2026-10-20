"""V18 · Sellado (adenda 1.4 y 1.5): reglas (a)-(g) de src/v18/f3_sellado.py y filtro de src/v18/sellado.py, con casos sintéticos.

Ningún test lee datos ni la muestra sellada: los manifiestos y los metadatos de la base son diccionarios inventados.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import f3_sellado as f3  # noqa: E402
import sellado  # noqa: E402

CORTE = "2026-10-17"


def _reglas(k15=None, k16=None, conj15=None, conj16=None, base=None):
    m15 = {"fecha_corte": CORTE, "ultimo_periodo_visto": k15 or {}, "preguntas": {"p": {"variables": conj15 or []}}}
    m16 = {"fecha_corte": CORTE, "ultimo_periodo_visto": k16 or {}, "conjuntos": {"c": {"variables": conj16 or []}}}
    return f3.Reglas(m15, m16, base or {}, "0" * 40, "2026-10-20", "f" * 64)


# ---------------------------------------------------------------------------------------------- periodos
def test_periodos():
    assert f3.fin("2024") == dt.date(2024, 12, 31)
    assert f3.fin("2024T2") == dt.date(2024, 6, 30)
    assert f3.fin("2024-02") == dt.date(2024, 2, 29)
    assert f3.ultimo_hasta(dt.date(2026, 6, 30), "A") == "2025"
    assert f3.ultimo_hasta(dt.date(2024, 12, 31), "A") == "2024"
    assert f3.ultimo_hasta(dt.date(2025, 10, 31), "T") == "2025T3"
    assert f3.ultimo_hasta(dt.date(2025, 10, 30), "M") == "2025-09"
    assert f3.ultimo_hasta(dt.date(2024, 12, 31), "M") == "2024-12"
    assert f3.periodo_en(dt.date(2026, 4, 1), "T") == "2026T2"
    assert f3.menor("2024", "2026T2") == "2024"


# ---------------------------------------------------------------------------------------------- reglas (a)-(g)
def test_regla_a_manda_la_menor():
    r = _reglas(k15={"x|provincia|T": "2026T1"}, k16={"x|provincia|T": "2026T2"}, conj16=["x"])
    t = r.calcular(f3.V("x", "provincia", "T", ["E0"]))
    assert (t["tope"], t["regla"], t["edicion_maxima"]) == ("2026T1", "(a)", CORTE)


def test_regla_b_media_anual():
    k = {"vt|provincia|A": "2024", "vt|provincia|T": "2026T2"}
    t = _reglas(k16=k, conj16=["vt"]).calcular(f3.V("vt", "provincia", "A", ["E0"], de="T"))
    assert t["tope"] == "2024" and t["regla"].startswith("(b)")          # ejemplo de la adenda: valor tasado provincial
    t = _reglas(k16={"vut|seccion|M": "2026-05"}, conj16=["vut"]).calcular(f3.V("vut", "seccion", "A", ["E0"], de="M"))
    assert t["tope"] == "2025"                                            # sin clave anual: años completos bajo la mensual


def test_regla_c_otra_frecuencia():
    k = {"cv|provincia|A": "2024", "cv|provincia|T": "2026T2"}
    t = _reglas(k16=k, conj16=["cv"]).calcular(f3.V("cv", "provincia", "M", ["E0"]))
    assert (t["tope"], t["regla"]) == ("2024-12", "(c)")                  # ejemplo de la adenda: compraventas mensuales
    t = _reglas(k16={"jk|zona_euro|M": "2025-10"}, conj16=["jk"]).calcular(f3.V("jk", "zona_euro", "T", ["E0"], de="M"))
    assert t["tope"] == "2025T3"                                          # suma trimestral de la sorpresa mensual


def test_regla_d_sellada_entera():
    r = _reglas(k16={"n|municipio|A": "2024"}, conj16=["n"])
    t = r.calcular(f3.V("n", "seccion", "A", ["E0"], anexo="2024"))
    assert t["sellada_entera"] and t["tope"] is None and t["regla"] == "(d)" and not t["coincide_anexo_c"]


def test_regla_e_fuera_de_conjuntos():
    base = {("hut", "municipio", "T"): ("2018T2", "2026T3"), ("defl", "nacional", "T"): ("1995T1", "2026T2")}
    r = _reglas(base=base)
    t = r.calcular(f3.V("hut", "municipio", "T", ["E0"]))
    assert (t["tope"], t["regla"], t["edicion_maxima"]) == ("2026T3", "(e)", "2026-10-20")   # (g): edición hasta la etiqueta
    t = r.calcular(f3.V("defl", "nacional", "A", ["E0"], de="T"))
    assert t["tope"] == "2025" and t["regla"] == "(b) con (e)"
    t = r.calcular(f3.V("censo", "provincia", "A", ["E0"], meta={"tipo": "fijo", "periodo": "2011", "frec": "A"}))
    assert t["tope"] == "2011"
    with pytest.raises(RuntimeError):
        r.calcular(f3.V("nada", "provincia", "A", ["E0"]))


def test_regla_f_sustituto():
    r = _reglas(k16={"padron|provincia|A": "2022"}, conj16=["padron"])
    t = r.calcular(f3.V("ecp", "provincia", "D", ["E0"], hereda="padron"))
    assert t["tope"] == "2022-12-31" and t["regla"] == "(f) (c)"
    t = r.calcular(f3.V("padron_raw", "provincia", "A", ["E0"], hereda="padron"))
    assert t["tope"] == "2022" and t["regla"] == "(f) (a)"


def test_anexo_c_nunca_mas_permisivo():
    base = {("tt", "municipio", "T"): ("2004T1", "2026T1")}
    t = _reglas(base=base).calcular(f3.V("tt", "municipio", "T", ["E0"], anexo="2024T4"))
    assert t["tope"] == "2024T4" and "Anexo C" in t["regla"] and not t["coincide_anexo_c"]
    t = _reglas(k16={"s|provincia|A": "2024"}, conj16=["s"]).calcular(f3.V("s", "provincia", "A", ["E0"], anexo="2025"))
    assert t["tope"] == "2024" and not t["coincide_anexo_c"]


# ---------------------------------------------------------------------------------------------- filtro de la fase 4
MAN = {
    "topes": {
        "v|municipio|A": {"tope": "2022", "sellada_entera": False, "edicion_maxima": CORTE},
        "v|seccion|A": {"tope": "2024", "sellada_entera": False, "edicion_maxima": CORTE},
        "v|provincia|T": {"tope": "2026T2", "sellada_entera": False, "edicion_maxima": CORTE},
        "v|nacional|T": {"tope": "2026T2", "sellada_entera": False, "edicion_maxima": CORTE},
        "v|ccaa|A": {"tope": "2024", "sellada_entera": False, "edicion_maxima": CORTE},
        "v|barrio|T": {"tope": "2026T3", "sellada_entera": False, "edicion_maxima": "2026-10-20"},
        "w|seccion|A": {"tope": None, "sellada_entera": True, "regla": "(d)"},
        "p|provincia|A": {"tope": None, "sellada_entera": False, "fuente_clave": "posterior a la etiqueta"},
    },
    "unidades_excluidas": {
        "provincia": {"v6": {"unidades": ["07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"]}},
        "municipio": {"v15": {"unidades": ["46001"]}, "v16": {"unidades": ["03002"]}},
        "distrito": {"v15": {"unidades": ["0801906"]}, "v16": {"unidades": ["0801908"]}},
        "fuga_declarada": {"municipios_con_distritos_sellados": ["08019"]},
    },
}


def test_tope_y_errores():
    assert sellado.tope("v", "municipio", "A", MAN) == "2022"
    with pytest.raises(KeyError):
        sellado.tope("no_esta", "municipio", "A", MAN)
    with pytest.raises(PermissionError):
        sellado.tope("w", "seccion", "A", MAN)
    with pytest.raises(PermissionError):
        sellado.tope("p", "provincia", "A", MAN)
    assert sellado.municipios_con_distritos_sellados(MAN) == {"08019"}


def test_filtrar_municipio():
    df = pd.DataFrame({"cod": ["28079", "46001", "03002", "08019", "08019", "08019", "8019"],
                       "periodo": ["2020", "2020", "2020", "2021", "2022", "2023", 2020],
                       "edicion": ["2026-10-01"] * 6 + ["2026-10-18"]})
    out = sellado.filtrar(df, "cod", "municipio", "periodo", "v", "A", MAN)
    assert out.cod.tolist() == ["08019", "08019"] and out.periodo.tolist() == ["2021", "2022"]   # v6, V15, V16, tope y edición


def test_filtrar_seccion_y_marca_v6():
    df = pd.DataFrame({"cod": ["0801906001", "0801908002", "0801901001", "2807901001", "0801902001"],
                       "periodo": ["2024", "2024", "2024", "2024", "2025"], "muestra_sellada_v6": [False, False, False, False, False]})
    out = sellado.filtrar(df, "cod", "seccion", "periodo", "v", "A", MAN)
    assert out.cod.tolist() == ["0801901001"]
    df["muestra_sellada_v6"] = [False, False, True, False, False]
    assert sellado.filtrar(df, "cod", "seccion", "periodo", "v", "A", MAN).empty


def test_filtrar_provincia_nacional_y_formatos():
    df = pd.DataFrame({"cod": ["28", "46", "46"], "periodo": ["2026T2", "2026T2", "2026T3"]})
    assert sellado.filtrar(df, "cod", "provincia", "periodo", "v", "T", MAN).cod.tolist() == ["46"]
    nac = pd.DataFrame({"cod": ["ES", "ES"], "periodo": ["2026T2", "2026T3"]})
    assert sellado.filtrar(nac, "cod", "nacional", "periodo", "v", "T", MAN).periodo.tolist() == ["2026T2"]
    anual = pd.DataFrame({"cod": ["46"], "periodo": ["2024"]})
    with pytest.raises(ValueError):
        sellado.filtrar(anual, "cod", "provincia", "periodo", "v", "T", MAN)    # periodos anuales con frecuencia trimestral
    with pytest.raises(KeyError):
        sellado.filtrar(df, "cod", "provincia", "periodo", "v", "M", MAN)
    with pytest.raises(ValueError):
        sellado.filtrar(pd.DataFrame({"cod": ["1"], "periodo": ["2024T1"]}), "cod", "barrio", "periodo", "v", "T", MAN)


@pytest.mark.skipif(not (RAIZ / "data" / "base" / "publica" / "territorios.parquet").exists(), reason="sin territorios.parquet")
def test_filtrar_ccaa():
    df = pd.DataFrame({"cod": ["13", "09", "10"], "periodo": ["2024", "2024", "2025"]})
    assert sellado.filtrar(df, "cod", "ccaa", "periodo", "v", "A", MAN).cod.tolist() == ["09"]   # Madrid (13) sellada en v6


# ---------------------------------------------------------------------------------------------- manifiesto real (si existe)
@pytest.mark.skipif(not sellado.MANIFIESTO.exists(), reason="sin docs/v18/sellado_v18.json")
def test_manifiesto_v18_ejemplos_de_la_adenda():
    m = json.loads(sellado.MANIFIESTO.read_text(encoding="utf-8"))
    assert sellado.tope("valor_tasado", "provincia", "A") == "2024"
    assert sellado.tope("valor_tasado", "provincia", "T") == "2026T2"
    assert sellado.tope("compraventas", "provincia", "M") == "2024-12"
    assert sellado.tope("incasol_renta_media", "municipio", "T") == "2026T1"
    assert sellado.tope("padron_pob_nacionalidad", "provincia", "A") == "2022"
    assert sellado.tope("ecp_pob_nacionalidad", "provincia", "D") == "2022-12-31"
    assert sellado.tope("bce_jk_mp_median_m", "zona_euro", "T") == "2025T3"
    with pytest.raises(PermissionError):
        sellado.tope("serpavi_n_contratos_recuento", "seccion", "A")
    c = m["unidades_excluidas"]["comprobacion_adenda_1_5"]
    assert c["distritos_coinciden"] and c["municipios_coinciden"]
    assert m["etiqueta"]["nombre"] == "plan-replicacion-v18"


@pytest.mark.skipif(not sellado.MANIFIESTO.exists(), reason="sin docs/v18/sellado_v18.json")
def test_claves_añadidas_tras_la_etiqueta_b6():
    """B6-1: claves añadidas después de la etiqueta con las mismas reglas; el resto del manifiesto no cambia de significado."""
    m = json.loads(sellado.MANIFIESTO.read_text(encoding="utf-8"))
    assert sellado.tope("c21md_hogares_muestra", "municipio", "D") == "2021-01-01"      # (e): Censo 2021, corte único
    assert m["topes"]["c21md_hogares_muestra|municipio|D"]["regla"] == "(e)"
    assert sellado.tope("mivau_obra_libre_terminadas", "provincia", "A") == "2024"       # (f) con (a): sustituto de terminadas|provincia|A
    assert m["topes"]["mivau_obra_libre_terminadas|provincia|A"]["regla"] == "(f) (a)"
    assert "c21md_hogares_muestra|municipio|D" in m["especificaciones"]["E2-R1c"]["variables"]
    assert "mivau_obra_libre_terminadas|provincia|A" in m["especificaciones"]["E12-A1"]["variables"]
    assert m["resumen"]["n_variables"] == len(m["topes"]) == 102
