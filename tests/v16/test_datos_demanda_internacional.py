"""Tests mínimos de la normalización V16 demanda_internacional (claves únicas, códigos, unidades, sin terceros)."""
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "data" / "processed" / "v16" / "demanda_internacional.parquet"
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]
H_COLS = list(pd.read_parquet(RAIZ / "data/base/hechos.parquet").columns[:0]) or None

pytestmark = pytest.mark.skipif(not P.exists(), reason="ejecutar src/v16/datos/demanda_internacional.py")


@pytest.fixture(scope="module")
def df():
    return pd.read_parquet(P)


def test_columnas(df):
    esperadas = list(pd.read_parquet(RAIZ / "data/base/hechos.parquet").head(1).columns)
    assert list(df.columns) == esperadas


def test_claves_unicas(df):
    assert not df.duplicated(CLAVE).any()


def test_codigos(df):
    terr = pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")
    nac = df[df.nivel == "nacional"]
    assert set(nac.territorio_codigo) <= set(terr[terr.nivel == "nacional"].territorio_codigo)
    pais = df[df.nivel == "pais"].territorio_codigo
    assert pais.str.fullmatch(r"[A-Z]{2}").all()
    assert set(df[df.nivel == "zona_euro"].territorio_codigo) == {"EA"}
    assert set(df.nivel) <= {"nacional", "pais", "zona_euro", "agregado_ue"}


def test_unidades_y_valores(df):
    assert (df.unidad.str.len() > 0).all()
    assert df.valor.notna().all()


def test_sin_terceros_y_marcas(df):
    assert df.redistribuible.all()
    assert not df.origen.str.contains("_terceros").any()
    assert (df.capa == "C4").all()
    assert not df.posterior_prereg.any()
    assert not df.muestra_sellada_v6.any()
