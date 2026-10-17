"""Tests mínimos de la normalización V16 renta_parque (claves únicas, códigos INE, unidades, sin terceros ni microdatos)."""
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "data" / "processed" / "v16" / "renta_parque.parquet"
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "fecha_dato", "capa", "licencia", "redistribuible", "metodo_dato", "origen", "posterior_prereg", "muestra_sellada_v6"]
LARGO = {"nacional": 2, "ccaa": 2, "provincia": 2, "municipio": 5, "distrito": 7, "seccion": 10}

pytestmark = pytest.mark.skipif(not P.exists(), reason="ejecutar src/v16/datos/renta_parque.py")


@pytest.fixture(scope="module")
def df():
    return pd.read_parquet(P)


@pytest.fixture(scope="module")
def terr():
    return pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")


def test_columnas(df):
    assert list(df.columns) == COLS


def test_claves_unicas(df):
    assert not df.duplicated(CLAVE).any()


def test_codigos_ine(df, terr):
    assert set(df.nivel) <= set(LARGO)
    for nivel in df.nivel.unique():
        usados = set(df.loc[df.nivel == nivel, "territorio_codigo"])
        validos = set(terr.loc[terr.nivel == nivel, "territorio_codigo"])
        assert usados <= validos, nivel
        assert df.loc[df.nivel == nivel, "territorio_codigo"].str.len().eq(LARGO[nivel]).all(), nivel


def test_unidades_y_valores(df):
    assert df.unidad.notna().all() and (df.unidad.str.len() > 0).all()
    assert df.valor.notna().all()
    assert df.groupby("variable").unidad.nunique().max() == 1


def test_sin_terceros_ni_microdatos(df):
    assert df.redistribuible.all()
    assert (df.capa == "C4").all()
    assert not df.posterior_prereg.any()
    assert not df.origen.str.contains("_terceros|/ecv/|/epf/", regex=True).any()


def test_marca_muestra_sellada(df):
    import sys
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout
    esperado = df.nivel.isin(["provincia", "municipio", "distrito", "seccion"]) & df.territorio_codigo.str[:2].isin(holdout.provincias_selladas_v6())
    assert (df.muestra_sellada_v6 == esperado).all()


def test_peso(df):
    assert P.stat().st_size < 50 * 1024 * 1024
