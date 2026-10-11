"""K4a: paneles de entrenamiento M0 (claves únicas, rangos, sellado, unidades). Lee salidas versionadas; sin red."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
PAN = RAIZ / "output" / "v6" / "M0" / "paneles"
sys.path.insert(0, str(RAIZ / "src"))

CLAVES = {"prov_alquiler_anual_train": ["cod", "anio"], "prov_compra_anual_train": ["cod", "anio"],
          "prov_contratos_nuevos_anual_train": ["cod", "anio"], "prov_trim_compra_train": ["cod", "t"],
          "mun_alquiler_anual_train": ["cod_mun", "anio"], "mun_compra_anual_train": ["cod_mun", "anio"],
          "mun_contratos_anual_train": ["cod_mun", "anio"], "dis_alquiler_anual_train": ["distrito", "anio"]}


def leer(n):
    return pd.read_csv(PAN / f"{n}.csv.gz")


@pytest.mark.parametrize("nombre", sorted(CLAVES))
def test_clave_unica(nombre):
    d = leer(nombre)
    assert not d.duplicated(CLAVES[nombre]).any()


@pytest.mark.parametrize("nombre", sorted(CLAVES))
def test_sin_unidades_selladas_ni_ultimo_anio(nombre):
    import holdout
    d = leer(nombre)
    sel = set(holdout.provincias_selladas_v6())
    col = "cod" if "cod" in d else "cod_prov"
    prov = d[col].astype(int).astype(str).str.zfill(2)
    assert not prov.isin(sel).any(), "provincia sellada en el panel de entrenamiento"
    if "mun" in nombre or "dis" in nombre:
        assert not d.iloc[:, 0].astype(str).str.zfill(5 if "mun" in nombre else 7).str[:2].isin(sel).any()
    ult = {"prov_compra_anual_train": 2025, "prov_trim_compra_train": 2025, "mun_compra_anual_train": 2025}.get(nombre, 2024)
    assert d.anio.max() < ult


def test_porcentajes_en_0_100():
    """K4a-02: pct_fianzas_600_incasol llegaba a 606 % (sumaba contratos y euros/mes)."""
    for n, c in (("prov_contratos_nuevos_anual_train", "pct_fianzas_600_incasol"), ("mun_contratos_anual_train", "pct_fianzas_600_incasol_mun")):
        x = leer(n)[c].dropna()
        assert len(x) > 0 and x.between(0, 100).all(), (n, x.max())
    c = leer("prov_compra_anual_train")
    for v in ("share_nueva_etdp", "share_contado_proxy", "share_compra_ext_res_pct", "no_res_share_R1A_pct", "share_ext_pob", "share_20_34", "paro_tasa"):
        x = c[v].dropna()
        assert x.between(0, 100).all(), v


def test_incasol_cuenta_solo_el_ano_completo():
    """K4a-02: Barcelona (08) 2021-2023 = 128.381 / 116.158 / 100.395 contratos (año completo); antes ~3,3 veces más."""
    d = leer("prov_contratos_nuevos_anual_train").set_index(["cod", "anio"]).ln_n_fianzas_incasol
    for a, n in ((2021, 128381), (2022, 116158), (2023, 100395)):
        assert abs(np.exp(d.loc[(8, a)]) / n - 1) < 1e-4   # los ln del panel van a 6 cifras


def test_precios_y_escalas_plausibles():
    c = leer("prov_compra_anual_train")
    assert np.exp(c.ln_pm2_tasado).between(300, 6000).all()          # €/m²
    a = leer("prov_alquiler_anual_train").dropna(subset=["ln_alq_m2_serpavi_vc"])
    assert np.exp(a.ln_alq_m2_serpavi_vc).between(2, 25).all()       # €/m²/mes
    assert np.exp(a.ln_alq_mes_serpavi_vc).between(150, 1500).all()  # €/mes


def test_ceuta_melilla_y_41_provincias_en_entrenamiento():
    c = leer("prov_compra_anual_train")
    assert c.cod.nunique() == 41 and {51, 52} <= set(c.cod)


def test_panel_provincial_sin_huecos_anuales():
    """Los retardos de M1/M3 con shift(1) por unidad exigen años consecutivos: sin huecos en los paneles provinciales."""
    for n in ("prov_alquiler_anual_train", "prov_compra_anual_train", "prov_contratos_nuevos_anual_train"):
        d = leer(n)
        g = d.groupby("cod").anio.agg(["min", "max", "nunique"])
        assert ((g["max"] - g["min"] + 1) == g["nunique"]).all(), n
