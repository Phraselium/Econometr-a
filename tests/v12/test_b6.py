"""V12-B6: supresión de celdas pequeñas y brechas estandarizadas con intervalo."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

B6 = Path(__file__).resolve().parents[2] / "output/v12/b6"


def test_supresion():
    if not (B6 / "ecv_anual_origen.csv").exists():
        pytest.skip("ejecutar `make v12`")
    for f in ("ecv_anual_origen.csv", "ecv_cruces_origen.csv", "censo2021_condiciones_origen.csv"):
        t = pd.read_csv(B6 / f)
        assert t.loc[~t.publicable, "valor"].isna().all(), f
    a = pd.read_csv(B6 / "ecv_anual_origen.csv")
    pub = a[a.publicable]
    assert (pub.n_muestral >= 50).all() and (pub.casos >= 10).all() and (pub.error_relativo <= 0.30).all()


def test_brecha_con_intervalo():
    b = pd.read_csv(B6 / "ecv_brecha_misma_edad_renta.csv")
    assert (b.ic95_inf <= b.diferencia_estandarizada).all() and (b.diferencia_estandarizada <= b.ic95_sup).all()
