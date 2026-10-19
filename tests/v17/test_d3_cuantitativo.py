"""Tests de V17 D3 (apoyo cuantitativo): las sumas contables cuadran y los hechos cumplen el esquema. A posteriori."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/v17/d3"


@pytest.fixture(scope="module", autouse=True)
def generar():
    subprocess.run([sys.executable, str(ROOT / "src/v17/d3_cuantitativo.py")], check=True, cwd=ROOT)


def test_poblacion_igual_sv_mas_residuo():
    d = pd.read_csv(OUT / "demografia_descomposicion_anual.csv")
    assert np.allclose(d.d_pob, d.sv + d.residuo_mig_ajustes, atol=1)
    assert np.allclose(d.d_pob, d.d_pob_nac_esp + d.d_pob_nac_ext, atol=1)
    assert (d.anio.min(), d.anio.max()) == (2015, 2025)


def test_residuo_igual_saldo_exterior_mas_ajuste():
    d = pd.read_csv(OUT / "demografia_descomposicion_anual.csv").dropna(subset=["saldo_exterior_oficial"])
    assert np.allclose(d.residuo_mig_ajustes, d.saldo_exterior_oficial + d.ajuste_estadistico, atol=1)


def test_nacidos_cuadran_con_poblacion():
    d = pd.read_csv(OUT / "demografia_descomposicion_anual.csv").query("anio < 2025")
    assert np.allclose(d.d_pob, d.d_nacidos_espana + d.d_nacidos_extranjero, rtol=0, atol=2_000)  # ECP: provincias y nacional redondean


def test_saldo_vegetativo_2024_coincide_con_ine():
    d = pd.read_csv(OUT / "demografia_descomposicion_anual.csv").set_index("anio")
    assert d.loc[2024, "sv"] == -116056  # nota MNP 2024 del INE (definitivo)
    assert d.loc[2024, "nacimientos"] - d.loc[2024, "defunciones"] == d.loc[2024, "sv"]
    assert d.loc[2024, "saldo_exterior_oficial"] == 626268  # EMCR 2024


def test_hogares_componentes_suman_cambio():
    h = pd.read_csv(OUT / "hogares_motores_2014_2026.csv")
    s = h.poblacion + h.composicion_nacionalidad + h.estructura_edad + h.jefatura_residuo
    assert np.allclose(s, h.cambio_observado, atol=1)
    assert np.allclose(h.suma_componentes, h.cambio_observado)
    ecp = h[h.fuente.str.startswith("ECP")]
    assert ecp.cambio_observado.sum() == 1222836  # 1-1-2021 a 1-1-2026, V16


def test_varianza_cuotas_suman_uno():
    v = pd.read_csv(OUT / "varianza_comun_local.csv")
    assert np.allclose(v.cuota_comun_anio + v.cuota_provincia_fija + v.cuota_local_provincia_x_anio, 1, atol=1e-5)
    assert ((v.ic95_lo <= v.cuota_comun_anio + 1e-9) | (v.ic95_lo <= v.ic95_hi)).all()
    assert (v.azar_media < v.cuota_comun_anio.max()).all()


def test_concentracion_acumulada_termina_en_100():
    c = pd.read_csv(OUT / "deficit_provincial_concentracion.csv", dtype={"cod_prov": str}).dropna(subset=["acum_pct"])
    assert abs(c.acum_pct.max() - 100) < 1e-3
    assert abs(c.cuota_pct.sum() - 100) < 1e-3
    assert c.acum_pct.is_monotonic_increasing
    assert not c.cod_prov.isin(pd.read_csv(OUT / "deficit_provincial_concentracion.csv", dtype={"cod_prov": str}).query("sellada_v6").cod_prov).any()


def test_provincias_selladas_en_blanco():
    c = pd.read_csv(OUT / "deficit_provincial_concentracion.csv", dtype={"cod_prov": str})
    assert c.loc[c.sellada_v6, ["deficit_bajas0", "N10_central"]].isna().all().all()
    assert c.sellada_v6.sum() == 11


def test_escenarios_aritmetica():
    e = pd.read_csv(OUT / "escenarios_produccion_5_10_anios.csv")
    nec = e.deficit_inicial / e.horizonte_anios + e.hogares_nuevos_anuales_INE + e.reposicion_anual_v5_1
    assert np.allclose(nec, e.produccion_anual_necesaria, atol=1)
    assert np.allclose(e.produccion_anual_necesaria / e.produccion_actual_2024_2025, e.ratio_necesaria_actual, atol=0.01)
    assert abs(e.hogares_nuevos_anuales_INE.iloc[0] - (21943397 - 19759349) / 15) < 1
    assert (e[e.horizonte_anios == 5].produccion_anual_necesaria.values > e[e.horizonte_anios == 10].produccion_anual_necesaria.values).all()


def test_tenencia_suma_100():
    t = pd.read_csv(OUT / "tenencia_por_origen_censo2021.csv")
    s = t.groupby(["grupo", "categoria"]).pct.sum()
    assert np.allclose(s, 100, atol=1e-2)


def test_hechos_esquema():
    hs = json.load(open(OUT / "hechos.json"))
    claves = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "lectura_v17", "fecha_dato", "ficha", "nota"}
    ids = [h["id"] for h in hs]
    assert len(ids) == len(set(ids)) and len(ids) >= 30
    for h in hs:
        assert set(h) == claves
        assert h["id"].startswith("V17-D3-") and h["capa"] == "C4" and h["lectura_v17"] in ("OF", "hecho", "cota", "asociación")
        assert "a posteriori" in h["nota"]
        if h["min"] is not None and h["max"] is not None and h["valor"] is not None and not h["unidad"].startswith("índice"):
            pass
    assert (OUT / "informe.md").read_text(encoding="utf-8").startswith("Análisis a posteriori (V17).")
