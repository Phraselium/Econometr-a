"""V16 fase 2 · pruebas de esfuerzo de acceso: implementación frente a Eurostat, determinismo e identidades contables."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v16"))
sys.path.insert(0, str(ROOT / "src"))

from f2_esfuerzo_datos import cargar  # noqa: E402
from f2_esfuerzo_nucleo import SEED, bootstrap_anio, descomponer, directa, preparar  # noqa: E402

EUROSTAT = ROOT / "data" / "processed" / "v16" / "demanda_internacional.parquet"
pytestmark = pytest.mark.skipif(not (ROOT / "data" / "raw" / "v9" / "ine_microdatos" / "ecv").exists(),
                                reason="microdatos ECV no disponibles")


@pytest.fixture(scope="module")
def datos():
    return preparar(cargar(anios=range(2015, 2025)))


def test_sobreesfuerzo_espana_coincide_con_eurostat(datos):
    eu = pd.read_parquet(EUROSTAT)
    eu = eu[(eu.variable == "eurostat_sobrecarga_coste_vivienda_pct") & (eu.territorio_codigo == "ES")
            & (eu.desagregacion == "edad=TOTAL;sexo=T;pobreza=TOTAL")]
    eu = eu.assign(anio=eu.periodo.astype(int)).set_index("anio").valor
    difs = {}
    for y in range(2015, 2025):
        g = datos[datos.anio == y].reset_index(drop=True)
        res, _ = bootstrap_anio(g, 0, SEED)
        difs[y] = res[("Total", "Espana", "sobre40")][0] - float(eu[y])
    assert all(abs(v) <= 0.5 for v in difs.values()), difs


def test_bootstrap_determinista_con_semilla(datos):
    g = datos[datos.anio == 2015].reset_index(drop=True)
    r1, n1 = bootstrap_anio(g, 30, SEED)
    r2, n2 = bootstrap_anio(g, 30, SEED)
    r3, _ = bootstrap_anio(g, 30, SEED + 1)
    k = ("Total", "Espana", "sobre40")
    assert n1 == n2
    assert np.array_equal(r1[k], r2[k], equal_nan=True)
    assert np.array_equal(r1[("Tenencia", "alquiler_mercado", "esfuerzo_medio")],
                          r2[("Tenencia", "alquiler_mercado", "esfuerzo_medio")], equal_nan=True)
    assert not np.array_equal(r1[k][1:], r3[k][1:])
    assert np.isfinite(r1[k]).all()


def test_identidades_contables(datos):
    def m(y):
        x = datos[(datos.anio == y) & (datos.ten == "alquiler_mercado") & datos.edad_sust.notna()]
        return x.reset_index(drop=True)
    a, b = m(2015), m(2024)
    o = descomponer(a, b)
    assert o["OB2|atribuido"] + o["OB2|no_atribuido"] == pytest.approx(o["media|total"], abs=1e-9)
    assert o["OB3|dotaciones"] + o["OB3|coeficientes"] + o["OB3|interaccion"] == pytest.approx(o["media|total"], abs=1e-9)
    assert o["DFL|media|composicion"] + o["DFL|media|estructura"] == pytest.approx(o["DFL|media|total"], abs=1e-9)
    d = directa(a, b)
    assert d["gasto"] + d["renta"] + d["interaccion"] == pytest.approx(d["dR"], abs=1e-9)
    assert d["dlnG"] - d["dlnY"] == pytest.approx(d["dlnR"], abs=1e-9)


def test_supresion_de_celdas_pequenas():
    from f2_esfuerzo_nucleo import resumen_celda
    v = np.r_[5.0, np.random.default_rng(1).normal(5, 0.1, 100)]
    assert resumen_celda(v, 49)["estado"] == "suprimida"
    assert resumen_celda(v, 50)["estado"] == "publicable"
    w = np.r_[1.0, np.random.default_rng(1).normal(1, 0.5, 100)]
    assert resumen_celda(w, 500)["estado"] == "suprimida"   # CV > 30 %
