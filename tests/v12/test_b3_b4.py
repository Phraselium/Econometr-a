"""V12-B3/B4: descomposición de hogares, celdas pequeñas y presión obra/hogares."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

O = Path(__file__).resolve().parents[2] / "output/v12"


def _csv(rel: str) -> pd.DataFrame:
    if not (O / rel).exists():
        pytest.skip(f"{rel} no existe (ejecutar `make v12`)")
    return pd.read_csv(O / rel, dtype={"cod_territorio": str, "cod_municipio": str, "cpro": str, "ccaa": str})


def test_descomposicion_cierra_en_los_dos_ordenes():
    for n in ("nacional", "provincia", "municipio"):
        d = _csv(f"b3/descomposicion_2011_2021_{n}.csv")
        for o in ("A", "B"):
            s = d[f"poblacion_{o}"] + d[f"estructura_{o}"] + d[f"jefatura_{o}"]
            assert ((s - d.crecimiento).abs() < 1e-6 * d.hogares_2021.abs().max()).all(), (n, o)


def test_hogares_2011_igual_censo_publicado():
    d = _csv("b3/descomposicion_2011_2021_nacional.csv")
    assert abs(d.hogares_2011.iloc[0] - 18083692) < 1   # INE, Censo 2011: hogares


def test_celdas_pequenas_suprimidas():
    h = _csv("b3/hogares_nacionalidad_censo2021.csv")
    pub = h[h.publicable]
    assert (pub.hogares_ext_muestra >= 10).all() and (pub.error_relativo <= 0.30).all()
    assert h.loc[~h.publicable, "cuota_ext_pct"].isna().all()


def test_presion_categorias():
    p = _csv("b4/presion_hogares_obra_municipio.csv")
    assert set(p.categoria) <= {"obra ≥ hogares", "obra 50-100 %", "obra < 50 %", "hogares no crecen"}
    c = _csv("b4/concordancia_mivau_protegida_provincias.csv")
    assert c.loc[c.cpro.notna(), "cpro"].str.fullmatch(r"\d{2}").all() and c.cpro.dropna().is_unique
