"""V12, revisión final: las celdas suprimidas no se pueden recuperar."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

O = Path(__file__).resolve().parents[2] / "output/v12"


def _csv(rel: str) -> pd.DataFrame:
    if not (O / rel).exists():
        pytest.skip("ejecutar `make v12`")
    return pd.read_csv(O / rel, dtype={"cod_barrio": str, "cod_seccion": str, "cod_territorio": str})


def test_error_relativo_en_blanco_si_suprimida():
    for rel in ("b3/hogares_nacionalidad_censo2021.csv", "b6/ecv_anual_origen.csv", "b6/ecv_cruces_origen.csv"):
        t = _csv(rel)
        assert t.loc[~t.publicable, "error_relativo"].isna().all(), rel


def test_supresion_complementaria_valencia():
    for rel, k in (("b1/valencia_barrio_nacionalidad.csv", "cod_barrio"),):
        t = _csv(rel)
        p = t[~t.nacionalidad.isin(["Total", "España", "EXT"])]
        n = p.groupby([k, "anio"]).suprimido.sum()
        assert not (n == 1).any()


def test_jefatura_publicada_sin_celdas_pequenas():
    t = pd.read_csv(O / "b3/jefatura_municipio.csv.gz")
    assert (t.loc[t.publicable, "referencias_muestra"] >= 10).all()
    assert t.loc[~t.publicable, "jefatura"].isna().all()


def test_saldos_edad_suprimidos():
    t = pd.read_csv(O / "b2/saldos_interiores_edad_nac_municipio.csv.gz")
    v = t[~t.suprimido]
    assert (v.altas_interiores >= 10).all() and (v.bajas_interiores >= 10).all()
