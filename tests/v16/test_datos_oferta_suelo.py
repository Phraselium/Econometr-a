"""Tests mínimos de la normalización V16 oferta_suelo (claves únicas, códigos INE, unidades, sin terceros en el parquet versionado)."""
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "data" / "processed" / "v16" / "oferta_suelo.parquet"
PT = RAIZ / "data" / "processed" / "v16" / "oferta_suelo_terceros.parquet"
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]

pytestmark = pytest.mark.skipif(not P.exists(), reason="ejecutar src/v16/datos/oferta_suelo.py")


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


def test_codigos_ine(df, terr):
    assert set(df.nivel) == {"nacional"}
    assert set(df.territorio_codigo) <= set(terr.loc[terr.nivel == "nacional", "territorio_codigo"])


def test_unidades_y_valores(df):
    assert (df.unidad.str.len() > 0).all()
    assert df.valor.notna().all() and (df.valor > 0).all()


def test_sin_terceros_y_marcas(df):
    assert df.redistribuible.all()
    assert not df.origen.str.contains("_terceros|_grandes").any()
    assert not df.variable.str.startswith("miteco_").any()
    assert (df.capa == "C4").all()
    assert not df.posterior_prereg.any()
    assert not df.muestra_sellada_v6.any()


@pytest.mark.skipif(not PT.exists(), reason="terceros no generado")
def test_terceros(terr):
    t = pd.read_parquet(PT)
    assert not t.duplicated(CLAVE).any()
    assert not t.redistribuible.any()
    assert (t.unidad.str.len() > 0).all()
    assert set(t.territorio_codigo) <= set(terr.loc[terr.nivel == "municipio", "territorio_codigo"])
    assert t.territorio_codigo.str.fullmatch(r"\d{5}").all()
    p = t[t.variable == "miteco_rn2000_porcentaje_superficie_municipal"].valor
    assert p.between(0, 100).all()
    import sys
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout
    prov = {str(x).zfill(2) for x in holdout.provincias_selladas_v6()}
    assert (t.muestra_sellada_v6 == t.territorio_codigo.str[:2].isin(prov)).all()
