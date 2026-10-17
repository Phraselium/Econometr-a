"""Tests mínimos de la normalización V16 alquiler_turismo (claves únicas, códigos INE, unidades, sin terceros, marcas)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "data" / "processed" / "v16" / "alquiler_turismo.parquet"
PT = RAIZ / "data" / "processed" / "v16" / "alquiler_turismo_terceros.parquet"
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]

pytestmark = pytest.mark.skipif(not P.exists(), reason="ejecutar src/v16/datos/alquiler_turismo.py")


@pytest.fixture(scope="module")
def df():
    return pd.read_parquet(P)


@pytest.fixture(scope="module")
def terr():
    return pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")


def test_columnas(df):
    esperadas = list(pd.read_parquet(RAIZ / "data/base/hechos.parquet").head(1).columns)
    assert list(df.columns) == esperadas


def test_claves_unicas(df):
    assert not df.duplicated(CLAVE).any()


def test_codigos_ine_validos_por_nivel(df, terr):
    assert set(df.nivel) <= {"nacional", "ccaa", "provincia", "municipio", "seccion"}
    for nivel, g in df.groupby("nivel"):
        validos = set(terr[terr.nivel == nivel].territorio_codigo)
        assert set(g.territorio_codigo) <= validos, nivel


def test_unidades_y_valores(df):
    assert (df.unidad.str.len() > 0).all()
    assert df.valor.notna().all()
    assert (df.groupby("variable").unidad.nunique() >= 1).all()


def test_sin_terceros_y_marcas(df):
    assert df.redistribuible.all()
    assert not df.origen.str.contains("_terceros").any()
    assert (df.capa == "C4").all()
    assert not df.posterior_prereg.any()


def test_muestra_sellada_regla(df):
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout
    sel = set(holdout.provincias_selladas_v6())
    sub = df.nivel.isin(["provincia", "municipio", "distrito", "seccion"])
    esperado = sub & df.territorio_codigo.str[:2].isin(sel)
    assert (df.muestra_sellada_v6 == esperado).all()


def test_inside_airbnb_agregado_sin_anuncios_individuales(df):
    ia = df[df.variable.str.startswith("ia_")]
    assert len(ia) > 0 or not (RAIZ / "data/raw/v16/alquiler_turismo/original/insideairbnb").exists()
    assert set(ia.nivel) <= {"municipio", "seccion"}
    assert not any(c in ia.columns for c in ("host_id", "id", "latitude", "longitude"))
    med = ia[ia.variable.str.endswith("_mediana") | ia.variable.str.contains("mediana")]
    n = ia[ia.variable == "ia_precio_noche_n_numero"].set_index(CLAVE[:3] + ["desagregacion"]).valor
    pm = ia[ia.variable == "ia_precio_noche_mediana"].set_index(CLAVE[:3] + ["desagregacion"]).valor
    assert (n.reindex(pm.index) >= 5).all()
    assert len(med) >= 0


def test_terceros_aparte():
    if not PT.exists():
        pytest.skip("sin parquet de terceros en este clon")
    t = pd.read_parquet(PT)
    assert not t.redistribuible.any()
    assert not t.duplicated(CLAVE).any()
    assert t.origen.str.contains("_terceros").all()
    terr = pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")
    assert set(t.territorio_codigo) <= set(terr[terr.nivel == "municipio"].territorio_codigo)
    assert (t.unidad.str.len() > 0).all()
    # solo recuentos: ningún campo personal en las columnas de texto
    assert not t.desagregacion.str.contains("@").any()
