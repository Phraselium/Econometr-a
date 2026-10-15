"""V12-B2: flujos OD y concordancia MIVAU."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

B2 = Path(__file__).resolve().parents[2] / "output/v12/b2"


def _csv(n: str) -> pd.DataFrame:
    if not (B2 / n).exists():
        pytest.skip(f"{n} no existe (ejecutar `make v12`)")
    return pd.read_csv(B2 / n, dtype={"cod_municipio": str}, keep_default_na=False)


def test_saldos_cuadran():
    w = _csv("flujos_area_anual.csv")
    assert (w.saldo_capital_con_corona == w.corona_a_capital - w.capital_a_corona).all()
    assert (w[["capital_a_corona", "corona_a_capital"]] >= 0).all().all()


def test_concordancia_unica():
    k = _csv("concordancia_mivau_municipios.csv")
    con = k[k.cod_municipio != ""]
    assert con.cod_municipio.str.fullmatch(r"\d{5}").all()
    assert (k.loc[k.cod_municipio != "", "candidatos"].astype(int) == 1).all()


def test_asociaciones_con_holm():
    a = _csv("asociacion_saldos_precios.csv")
    assert len(a) and "p_holm" in a and (a.p_holm.astype(float) >= a.p.astype(float)).all()
