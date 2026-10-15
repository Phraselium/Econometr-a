"""V12-B7: coherencia de las tablas de turismo."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

B7 = Path(__file__).resolve().parents[2] / "output/v12/b7"


def test_porcentajes_y_holm():
    if not (B7 / "cv_asociaciones.csv").exists():
        pytest.skip("ejecutar `make v12`")
    s = pd.read_csv(B7 / "serie_vut_cv_valencia.csv")
    assert s.pct_vut.between(0, 100).all()
    a = pd.read_csv(B7 / "cv_asociaciones.csv")
    assert (a.p_holm >= a.p).all() and a.spearman.between(-1, 1).all()
    d = pd.read_csv(B7 / "valencia_distritos.csv", dtype={"cod_distrito": str})
    assert len(d) == 19 and d.cod_distrito.str.startswith("46250").all()
