"""V17 f2 · grupo v15_v16_micro: reproducción del punto y regla del 15 % (análisis a posteriori).

Lee output/v17/lectura_bde/v15_v16_micro/ (generado por src/v17/f2_inferencia_v15_v16_micro.py) y comprueba las reglas del encargo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v17"))
import f2_inferencia_v15_v16_micro as F  # noqa: E402

SAL = ROOT / "output" / "v17" / "lectura_bde" / "v15_v16_micro"


@pytest.fixture(scope="module")
def df():
    ruta = SAL / "inferencia.csv"
    if not ruta.exists():
        pytest.skip("ejecuta antes src/v17/f2_inferencia_v15_v16_micro.py")
    return pd.read_csv(ruta)


def test_regla_15_unidad():
    assert F.clasifica(0.1500001) == "no_fiable"
    assert F.clasifica(0.15) == "si"
    assert F.clasifica(0.0963) == "si"
    assert F.clasifica(0.0047) == "si"
    assert F.clasifica(float("nan")) == "sin_medir"
    assert "rechaza un 9,6 % de las veces bajo la nula" in F.frase("si", 0.03, 0.0963, "x")
    assert "NO publicada" in F.frase("no_fiable", 0.03, 0.2, "x")


def test_holm_bh():
    p = np.array([0.01, 0.04, 0.03, 0.2])
    h, b = F.holm(p), F.bh(p)
    assert np.all(h >= p) and np.all(b >= p) and np.all(b <= h + 1e-12)
    assert abs(h[0] - 0.04) < 1e-12 and abs(b[0] - 0.04) < 1e-12


def test_columnas_y_rotulo(df):
    assert list(df.columns) == F.COLS
    r = json.loads((SAL / "resultado.json").read_text(encoding="utf-8"))
    assert r["nota"] == "a posteriori"
    assert (SAL / "informe.md").read_text(encoding="utf-8").startswith("Análisis a posteriori (V17).")


def test_cubre_los_resultados_del_grupo(df):
    ids = set(df.id_resultado)
    for esperado in ("H1-CS", "H1-SDID", "H2-PPML", "H2-CS", "H2-SDID", "H3", "H4-AKM0", "Q1c-global", "Q2a", "Q2c", "Q3-b", "Q3-c1-AKM0", "Q3-c2-AKM0", "Q4a", "Q4b", "Q6-v", "Q6-p", "Q7", "Q8"):
        assert esperado in ids, esperado


def test_punto_reproducido(df):
    # tolerancia 1e-6 relativa; Q8 publica la razón de sumas y se reproduce con ella
    rel = (df.estimacion_reproducida - df.estimacion_publicada).abs() / df.estimacion_publicada.abs()
    malas = df[rel > 1e-6]
    assert malas.empty, malas[["id_resultado", "estimacion_publicada", "estimacion_reproducida"]].to_string()


def test_regla_del_15_por_ciento(df):
    for r in df.itertuples():
        if np.isfinite(r.tamano_real) and r.tamano_real > 0.15:
            assert r.publicable == "no_fiable", r.id_resultado
        if r.publicable == "no_fiable":
            assert not np.isfinite(r.tamano_real) or r.tamano_real > 0.15
            # solo estimación puntual: ni p, ni IC, ni EE, ni ajustes
            for c in ("se_conv", "p_conv", "ic95_lo", "ic95_hi", "p_holm_pregunta", "p_bh_pregunta"):
                assert pd.isna(getattr(r, c)), (r.id_resultado, c)
            assert "NO publicada" in r.frase
        elif r.publicable == "si":
            assert 0 <= r.tamano_real <= 0.15
            assert np.isfinite(r.p_conv) and "rechaza un" in r.frase and "bajo la nula" in r.frase
        else:
            assert r.publicable == "sin_medir" and "sin medir" in r.frase


def test_ajustes_dentro_de_pregunta(df):
    pub = df[df.publicable != "no_fiable"].dropna(subset=["p_holm_pregunta"])
    assert (pub.p_holm_pregunta >= pub.p_conv - 1e-12).all()
    assert (pub.p_bh_pregunta >= pub.p_conv - 1e-12).all() and (pub.p_bh_pregunta <= pub.p_holm_pregunta + 1e-12).all()
    # las alternativas del mismo punto no entran en Holm/BH
    alt = df[df.id_resultado.str.endswith(("-AKM", "-PROV", "-Webb"))]
    assert alt.p_holm_pregunta.isna().all()


def test_todo_es_capa_c4_sin_cambio(df):
    assert (df.capa_proyecto == "C4").all()
    assert not df.frase.str.contains("causal|causa ", case=False, regex=True).any()
