"""Tests mínimos de la normalización V16 tension_social (claves únicas, códigos INE, unidades, sin terceros en el parquet versionado)."""
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "data" / "processed" / "v16" / "tension_social.parquet"
PT = RAIZ / "data" / "processed" / "v16" / "tension_social_terceros.parquet"
PC = RAIZ / "data" / "processed" / "v16" / "tension_social_partidos_municipios_terceros.parquet"
CLAVE = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]

pytestmark = pytest.mark.skipif(not P.exists(), reason="ejecutar src/v16/datos/tension_social.py")


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
    assert set(df.nivel) <= {"nacional", "provincia", "municipio", "seccion"}
    for nivel in ["nacional", "provincia", "municipio", "seccion"]:
        usados = set(df.loc[df.nivel == nivel, "territorio_codigo"])
        validos = set(terr.loc[terr.nivel == nivel, "territorio_codigo"])
        assert usados <= validos, nivel
    assert df.loc[df.nivel == "municipio", "territorio_codigo"].str.fullmatch(r"\d{5}").all()
    assert df.loc[df.nivel == "seccion", "territorio_codigo"].str.fullmatch(r"\d{10}").all()


def test_unidades_y_valores(df):
    assert (df.unidad.str.len() > 0).all()
    assert df.valor.notna().all()


def test_sin_terceros_y_marcas(df):
    assert df.redistribuible.all()
    assert not df.origen.str.contains("_terceros").any()
    assert not df.variable.str.startswith("cgpj_").any()
    assert (df.capa == "C4").all()
    assert not df.posterior_prereg.any()


def test_muestra_sellada(df):
    import sys
    sys.path.insert(0, str(RAIZ / "src"))
    import holdout
    prov = {str(p).zfill(2) for p in holdout.provincias_selladas_v6()}
    esperado = df.nivel.isin(["provincia", "municipio", "seccion"]) & df.territorio_codigo.str[:2].isin(prov)
    assert (df.muestra_sellada_v6 == esperado).all()


@pytest.mark.skipif(not PT.exists(), reason="terceros no generado")
def test_terceros():
    t = pd.read_parquet(PT)
    terr = pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")
    assert not t.duplicated(CLAVE).any()
    assert not t.redistribuible.any()
    assert (t.unidad.str.len() > 0).all()
    prov = t[t.nivel == "provincia"].territorio_codigo
    assert set(prov) <= set(terr[terr.nivel == "provincia"].territorio_codigo)
    pj = t[t.nivel == "partido_judicial"].territorio_codigo
    assert pj.str.fullmatch(r"PJ-\d{2}-\d{1,3}").all()
    assert set(pj.str[3:5]) <= set(terr[terr.nivel == "provincia"].territorio_codigo)


@pytest.mark.skipif(not PC.exists(), reason="terceros no generado")
def test_correspondencia_partidos():
    c = pd.read_parquet(PC)
    terr = pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet")
    m = c[c.cod_municipio_ine.notna()]
    assert m.cod_municipio_ine.is_unique
    assert set(m.cod_municipio_ine) <= set(terr[terr.nivel == "municipio"].territorio_codigo)
