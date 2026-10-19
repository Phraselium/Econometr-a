"""Tests de src/v17/f3_demanda_precios.py (V17, fase 3, análisis a posteriori)."""
import csv
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "src/v17/f3_demanda_precios.py"
SALIDA = ROOT / "output/v17/auditoria/demanda_precios_hechos.json"
TABLA = ROOT / "output/v17/auditoria/demanda_precios.csv"
FILAS = ["turisticos", "inmigracion", "tipos", "burbuja", "alquiler", "precio"]
VEREDICTOS = {"se sostiene", "se sostiene con matices", "engañosa", "incorrecta", "no se puede saber"}


@pytest.fixture(scope="module")
def hechos():
    if not SALIDA.exists():
        pytest.skip("salida no generada")
    return {h["id"]: h for h in json.loads(SALIDA.read_text(encoding="utf-8"))}


def test_formato(hechos):
    assert len(hechos) >= 30
    for i, h in hechos.items():
        assert i.startswith("V17-AUD-DP-")
        assert h["capa"] == "C4"
        assert h["nota"].startswith("a posteriori")
        assert h["lectura_v17"] in ("OF", "hecho", "cota", "asociación", "juicio experto", "juicio experto (calibración)")
        assert h["fuentes"]
        if h["min"] is not None and h["max"] is not None and h["unidad"].startswith("%"):
            assert h["min"] <= h["max"] + 1e-9, i


def test_cota_turistica_reproduce_publicada(hechos):
    # B4-v3-vut-cantidad = 2,746 (2,423-2,746) en output/v5/cifras_clave.csv
    h = hechos["V17-AUD-DP-TUR-NAC-AUMENTO-2020-2024"]
    assert abs(h["valor"] - 2.746) < 0.001 and abs(h["min"] - 2.423) < 0.001


def test_stock_turistico_reproduce_bde(hechos):
    # Cuadro A.3 de BdE DO 2432: 11,8 % (viviendas turísticas feb. 2024 / alquiler del Censo 2021)
    assert abs(hechos["V17-AUD-DP-TUR-NAC-STOCK-2024M02"]["valor"] - 11.8) < 0.05
    assert hechos["V17-AUD-DP-TUR-NAC-STOCK-2024M08"]["valor"] > 4 * hechos["V17-AUD-DP-TUR-NAC-AUMENTO-2020-2024"]["valor"]


def test_percentiles_ordenados(hechos):
    p50, p90 = hechos["V17-AUD-DP-TUR-SEC-P50"]["valor"], hechos["V17-AUD-DP-TUR-SEC-P90"]["valor"]
    p99 = hechos["V17-AUD-DP-TUR-SEC-P99"]["valor"]
    assert p50 < p90 < p99


def test_precio_reproduce_publicado(hechos):
    # IPV real 2019-2025 publicado: 18,7 %; IPV deflactado por renta por hogar debe quedar por debajo
    h = hechos["V17-AUD-DP-PRE-IPV-REAL-RENTA"]
    assert 0 < h["valor"] < 18.7


def test_fichas_y_tabla():
    for f in FILAS:
        t = (ROOT / f"output/v17/auditoria/filas/{f}.md").read_text(encoding="utf-8")
        assert t.startswith("Análisis a posteriori (V17).")
        for s in ("Texto auditado", "Veredicto", "Texto corregido", "Parada"):
            assert s in t, (f, s)
    assert (ROOT / "output/v17/auditoria/preguntas/D3-1.md").read_text(encoding="utf-8").startswith("Análisis a posteriori (V17).")
    filas = list(csv.DictReader(TABLA.open(encoding="utf-8")))
    assert [r["id_fila"] for r in filas] == FILAS
    for r in filas:
        assert r["veredicto"] in VEREDICTOS
        assert set(r) == {"id_fila", "texto_antes", "veredicto", "texto_despues", "confianza", "por_que", "pruebas", "referencias", "parada"}


def test_script_sin_red_ni_sellado():
    src = SCRIPT.read_text(encoding="utf-8").split('"""', 2)[2]   # sin la cadena de documentación
    for prohibido in ("requests", "urllib", "data/sealed", "evaluate_", "http://", "https://"):
        assert prohibido not in src
    assert "SEED = 20261010" in src
    assert "not muestra_sellada_v6" in src


def test_determinista():
    antes = SALIDA.read_bytes() if SALIDA.exists() else None
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    primero = SALIDA.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    assert SALIDA.read_bytes() == primero
    if antes is not None:
        assert antes == primero
