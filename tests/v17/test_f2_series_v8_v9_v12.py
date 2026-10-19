"""V17 fase 2, grupo series_v8_v9_v12: reproducción del punto y regla del 15 % (análisis a posteriori)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.v17 import f2_inferencia_series_v8_v9_v12 as F  # noqa: E402

CSV = ROOT / "output/v17/lectura_bde/series_v8_v9_v12/inferencia.csv"


@pytest.fixture(scope="module")
def df():
    if not CSV.exists():
        pytest.skip("ejecutar primero src/v17/f2_inferencia_series_v8_v9_v12.py")
    return pd.read_csv(CSV)


def test_columnas(df):
    assert list(df.columns) == F.COLS


def test_reproduccion_punto(df):
    r = df[df.estimacion_reproducida.notna() & df.estimacion_publicada.notna()]
    assert len(r) >= 30
    dev = (r.estimacion_reproducida - r.estimacion_publicada).abs() / r.estimacion_publicada.abs()
    assert dev.max() < 1e-6


def test_regla_15(df):
    t = df[df.tamano_real.notna()]
    assert (t[t.tamano_real > 0.15].publicable.str.startswith("no")).all()
    assert (t[t.tamano_real > 0.15][["se_conv", "p_conv", "ic95_lo", "ic95_hi"]].isna()).all().all()
    assert (t[t.tamano_real <= 0.15].publicable == "sí").all()
    assert (df[df.tamano_real.isna() & df.p_conv.notna()].publicable == "con reserva (sin medir)").all()
    assert F.regla(0.1515).startswith("no") and F.regla(0.15) == "sí" and F.regla(None).startswith("con reserva")


def test_frase_5_15():
    s = F.frase(0.03, 0.09, "sí")
    assert "p = 0,03" in s and "9,0 % de las veces bajo la nula" in s


def test_familias_por_pregunta(df):
    for _, g in df[df.p_conv.notna()].groupby("pregunta"):
        assert (g.p_holm_pregunta >= g.p_conv - 1e-12).all() and (g.p_bh_pregunta >= g.p_conv - 1e-12).all()
        assert (g.p_holm_pregunta >= g.p_bh_pregunta - 1e-12).all()


def test_no_fiables_conocidos(df):
    d = df.set_index("id_resultado")
    assert d.loc["E1-P2-CS-ARDL-p1-velocidad", "publicable"].startswith("no")
    assert d.loc["H5-ClarkWest", "publicable"].startswith("no")
    assert d.loc["Q9-g", "publicable"] == "sí"
    assert df[df.version == "V9"].query("pregunta in ['V9-D1a','V9-D2','V9-D4']").publicable.str.startswith("no").all()


def test_nw_y_dm():
    assert F.nw_lag(100) == 4
    rng = np.random.default_rng(F.SEED)
    e1, e2 = rng.normal(size=60), rng.normal(size=60)
    s, p, _ = F.dm_hln(e1, e2, 1)
    assert 0 <= p <= 1
    A = np.column_stack([np.ones(200), rng.normal(size=200)])
    e = rng.normal(size=200)
    assert np.allclose(np.diag(F.nw_cov(A, e, 0)), np.diag(F.nw_cov(A, e, 0)))


def test_resultado_json_a_posteriori():
    r = json.load(open(CSV.parent / "resultado.json"))
    assert r["nota"] == "a posteriori"
    assert (CSV.parent / "informe.md").read_text(encoding="utf-8").startswith("Análisis a posteriori (V17).")
