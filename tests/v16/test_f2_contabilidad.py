"""Tests de V16-F2.2 contabilidad: identidad exacta, determinismo (SEED 20261010) y ausencia de provincias v6 en el panel."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v16"))
import f2_contabilidad_hogares as H  # noqa: E402
import f2_contabilidad_precio as P  # noqa: E402

OUT = RAIZ / "output/v16/f2_contabilidad"
SELLADAS = {"07", "22", "26", "28", "30", "31", "33", "35", "38", "44", "50"}
COMP = ["poblacion", "composicion_nacionalidad", "estructura_edad", "jefatura_residuo"]


def test_identidad_sintetica_exacta():
    rng = np.random.default_rng(20261010)
    P0, P1 = rng.uniform(1e3, 1e5, (2, 16)), rng.uniform(1e3, 1e5, (2, 16))
    h = rng.uniform(0.0, 0.6, (2, 16))
    r = H.descomponer(P0, P1, h, 5.0e5, 5.4e5)
    assert abs(sum(r[c] for c in COMP) - (5.4e5 - 5.0e5)) < 1e-6
    assert abs(r["error_identidad"]) < 1e-6
    for c in COMP[:3]:
        assert r[f"{c}_min"] <= r[c] <= r[f"{c}_max"]
    assert abs(r["nac_ES"] + r["nac_EXT"] - (r["poblacion"] + r["composicion_nacionalidad"] + r["estructura_edad"])) < 1e-6


def test_sin_cambio_demografico_todo_es_jefatura():
    P0 = np.full((2, 4), 1000.0)
    r = H.descomponer(P0, P0.copy(), np.full((2, 4), 0.4), 3200.0, 3300.0)
    assert r["poblacion"] == pytest.approx(0) and r["estructura_edad"] == pytest.approx(0) and r["jefatura_residuo"] == pytest.approx(100)


@pytest.mark.parametrize("f", ["hogares_ecp_2021_2025.csv", "hogares_ecp_2021_2026.csv", "hogares_ecp_anual_nacional.csv", "hogares_epa_2002_2021_nacional.csv",
                               "hogares_epa_2021_2025_2026_nacional.csv"])
def test_identidad_en_tablas(f):
    p = OUT / f
    if not p.exists():
        pytest.skip("ejecutar src/v16/f2_contabilidad.py")
    d = pd.read_csv(p)
    suma = d[COMP[0]] + d[COMP[1]] + d[COMP[2]] + d[COMP[3]]
    assert (suma - d.cambio_observado).abs().max() < 1e-3
    assert d.error_identidad.abs().max() < 1e-3


def test_hogares_sin_ccaa_ni_provincias_selladas():
    p = OUT / "hogares_ecp_2021_2025.csv"
    if not p.exists():
        pytest.skip("ejecutar src/v16/f2_contabilidad.py")
    d = pd.read_csv(p, dtype={"codigo": str})
    assert not set(d[d.nivel == "provincia"].codigo) & SELLADAS
    t = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    m = t[t.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa
    ccaa_selladas = set(m[list(SELLADAS)])
    assert not set(d[d.nivel == "ccaa"].codigo) & ccaa_selladas


def test_ninguna_provincia_v6_en_el_panel():
    lp = P.cargar_log_precio()
    assert not set(lp.columns) & SELLADAS
    assert lp.shape[1] >= 33
    prov = OUT / "precio_cuota_comun_provincia.csv"
    if prov.exists():
        assert not set(pd.read_csv(prov, dtype={"provincia": str}).provincia) & SELLADAS
    niv = OUT / "precio_contabilidad_nivel_provincia.csv"
    if niv.exists():
        d = pd.read_csv(niv, dtype={"provincia": str})
        assert not set(d.provincia) & SELLADAS
        assert d.error_identidad.abs().max() < 1e-8


def test_contabilidad_nivel_exacta():
    rng = np.random.default_rng(20261010)
    X = rng.normal(0.01, 0.03, (26, 7))
    d = P.contabilidad_nivel(X, list("abcdefg"), "t")
    assert d.error_identidad.abs().max() < 1e-10
    assert np.allclose(d.cambio_ln_x100, 100 * X.sum(0))


def test_determinismo_pca_y_bootstrap():
    rng = np.random.default_rng(20261010)
    X = rng.normal(size=(28, 12)) + rng.normal(size=(28, 1))
    a, b = P.pca_periodo(X), P.pca_periodo(X)
    assert a["cuota1"] == b["cuota1"] and np.array_equal(a["r2"], b["r2"])
    b1 = P.cuota_bootstrap(X, 50, np.random.default_rng(20261010))
    b2 = P.cuota_bootstrap(X, 50, np.random.default_rng(20261010))
    assert np.array_equal(b1, b2)
    n1 = P.cuota_nula(20, 10, 30, np.random.default_rng(20261010))
    assert np.array_equal(n1, P.cuota_nula(20, 10, 30, np.random.default_rng(20261010)))


def test_determinismo_hogares_nacional():
    a = H.bloque_ecp(2021, 2025, smoke=True).iloc[0]
    b = H.bloque_ecp(2021, 2025, smoke=True).iloc[0]
    assert a.poblacion == b.poblacion and a.estructura_edad == b.estructura_edad


def test_hechos_y_resultado():
    p = OUT / "hechos.json"
    if not p.exists():
        pytest.skip("ejecutar src/v16/f2_contabilidad.py")
    hs = json.loads(p.read_text(encoding="utf-8"))
    assert 0 < len(hs) <= 30
    claves = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"}
    informe = (OUT / "informe.md").read_text(encoding="utf-8")
    for h in hs:
        assert set(h) == claves and h["id"].startswith("V16-CON-") and h["capa"] == "C4"
        assert h["ficha"].startswith("output/v16/f2_contabilidad/informe.md#")
        assert f'id="{h["ficha"].split("#")[1]}"' in informe
    r = json.loads((OUT / "resultado.json").read_text(encoding="utf-8"))
    for k in ("rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"):
        assert k in r
    assert r["capa"] == "C4" and r["diagnosticos"]["error_identidad_max_hogares"] < 1e-3
    low = informe.lower()
    for prohibido in ("componente", "atribución contable", "se asocia"):
        assert prohibido not in low
