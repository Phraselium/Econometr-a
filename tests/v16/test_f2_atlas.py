"""V16 fase 2.3 · atlas multiescala: sin unidades selladas, supresión aplicada, tamaño < 50 MB y determinismo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v16"))

import f2_atlas  # noqa: E402
import f2_atlas_datos as D  # noqa: E402
import holdout  # noqa: E402

SAL = ROOT / "output" / "v16" / "f2_atlas"
ATLAS = SAL / "atlas.parquet"
COLS = ["territorio_codigo", "nivel", "periodo", "indicador", "valor", "ic_inf", "ic_sup", "calidad", "suprimida", "fuente"]
pytestmark = pytest.mark.skipif(not ATLAS.exists(), reason="atlas.parquet no generado (python3 src/v16/f2_atlas.py)")


@pytest.fixture(scope="module")
def atlas() -> pd.DataFrame:
    return pd.read_parquet(ATLAS)


def test_columnas_y_capa(atlas):
    assert set(COLS) <= set(atlas.columns)
    r = json.loads((SAL / "resultado.json").read_text(encoding="utf-8"))
    assert r["capa"] == "C4" and r["nivel_evidencia"] == "DESCRIPTIVO"
    assert r["diagnosticos"]["unidades_selladas_en_salida"] == 0


def test_ninguna_unidad_sellada_v16(atlas):
    for nivel in ("provincia", "municipio", "distrito", "seccion", "partido_judicial"):
        c = atlas.loc[atlas.nivel == nivel, "territorio_codigo"].drop_duplicates()
        if len(c):
            assert not holdout.unidad_sellada_v16(c, nivel).any(), nivel


def test_ccaa_k8_no_aparecen_por_debajo_de_ccaa(atlas):
    k8 = {"07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"}  # provincias selladas v6 (bloques de CCAA)
    fino = atlas[atlas.nivel.isin(["provincia", "municipio", "distrito", "seccion"])]
    assert not fino.territorio_codigo.str[:2].isin(k8).any()
    pj = atlas[atlas.nivel == "partido_judicial"].territorio_codigo
    assert not pj.str[3:5].isin(k8).any()


def test_supresion_aplicada(atlas):
    ok = atlas[~atlas.suprimida]
    assert not (ok.n_base < D.N_MIN).any()
    assert not (ok.cv > D.CV_MAX).any()
    sup = atlas[atlas.suprimida]
    assert len(sup) > 0
    assert sup.valor.isna().all() and sup.ic_inf.isna().all() and sup.ic_sup.isna().all()
    assert sup.calidad.str.contains("suprimida|sustituto").all()


def test_sustitutos_adrh_no_se_muestran_como_municipales(atlas):
    s = atlas[atlas.calidad.str.contains("sustituto de provincia/comarca", regex=False)]
    assert len(s) > 0 and s.suprimida.all() and s.valor.isna().all()


def test_intervalos_coherentes(atlas):
    c = atlas.dropna(subset=["ic_inf", "ic_sup", "valor"])
    assert len(c) > 0
    assert (c.ic_inf <= c.valor + 1e-6).all() and (c.valor <= c.ic_sup + 1e-6).all()


def test_tamano_menor_de_50_mb():
    assert ATLAS.stat().st_size < 50 * 1024 * 1024


def test_hechos_forma_y_limite():
    h = json.loads((SAL / "hechos.json").read_text(encoding="utf-8"))
    assert 0 < len(h) <= 25
    claves = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"}
    for x in h:
        assert claves <= set(x) and x["id"].startswith("V16-ATL-") and x["capa"] == "C4"
        assert x["ficha"].startswith("output/v16/f2_atlas/atlas.md#")


def test_atlas_md_en_cuatro_paginas():
    t = (SAL / "atlas.md").read_text(encoding="utf-8")
    assert len(t.splitlines()) <= 4 * 60 + 30
    assert "validación sellada" in t and "no es la tasa de sobreesfuerzo" in t.replace("**No es la tasa de sobreesfuerzo de la ECV**", "no es la tasa de sobreesfuerzo")


def test_determinismo_smoke():
    a = f2_atlas.construir(smoke=True)
    b = f2_atlas.construir(smoke=True)
    pd.testing.assert_frame_equal(a, b)
    assert not a.duplicated(["territorio_codigo", "nivel", "periodo", "indicador"]).any()
