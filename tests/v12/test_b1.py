"""V12-B1: coherencia de la contabilidad demográfica (identidad, sumas territoriales, celdas pequeñas)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

B1 = Path(__file__).resolve().parents[2] / "output/v12/b1"
COMP = ["vegetativo", "saldo_exterior", "saldo_interior", "residuo"]


def _csv(nombre: str) -> pd.DataFrame:
    r = B1 / nombre
    if not r.exists():
        pytest.skip(f"{nombre} no existe (ejecutar `make v12`)")
    return pd.read_csv(r, dtype={"cod_territorio": str, "cod_barrio": str, "cod_seccion": str})


def test_identidad_cierra():
    for n in ("nacional", "ccaa", "provincia"):
        a = _csv(f"contabilidad_anual_{n}.csv")
        assert (a.crecimiento - a[COMP].sum(axis=1)).abs().max() < 1e-6 * a.poblacion_inicio.max()


def test_provincias_suman_nacional():
    p, n = _csv("contabilidad_anual_provincia.csv"), _csv("contabilidad_anual_nacional.csv")
    s = p.groupby(["anio", "nac"])[["crecimiento", "vegetativo", "saldo_exterior"]].sum()
    t = n.set_index(["anio", "nac"])[["crecimiento", "vegetativo", "saldo_exterior"]]
    assert (s - t.reindex(s.index)).abs().max().max() < 1
    assert n.saldo_interior.abs().max() == 0


def test_valencia_celdas_pequenas_y_comparables():
    lb = _csv("valencia_barrio_nacionalidad.csv")
    paises = lb[~lb.nacionalidad.isin(["Total", "España", "EXT"])]
    assert not (paises.poblacion < 10).any()
    v = _csv("valencia_barrio_variacion_2021_2025.csv")
    assert v.loc[~v.comparable, "var_Total_2021_2025"].isna().all()
