"""Tests de src/v17/f3_oferta_titularidad.py (V17, fase 3, análisis a posteriori)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "src/v17/f3_oferta_titularidad.py"
SALIDA = ROOT / "output/v17/auditoria/oferta_titularidad_hechos.json"


@pytest.fixture(scope="module")
def hechos():
    if not SALIDA.exists():
        pytest.skip("salida no generada")
    return {h["id"]: h for h in json.loads(SALIDA.read_text(encoding="utf-8"))}


def test_formato(hechos):
    assert len(hechos) >= 20
    for i, h in hechos.items():
        assert i.startswith("V17-AUD-OT-")
        assert h["capa"] == "C4"
        assert h["nota"].startswith("a posteriori")
        assert h["lectura_v17"] in ("OF", "hecho", "cota", "asociación", "juicio experto")
        assert h["fuentes"]


def test_catastro_reproduce_fuente(hechos):
    h = hechos["V17-AUD-OT-CAT-GT-PARQUE-2026"]
    assert 4.1 < h["valor"] < 4.2          # 4,16 % en 2026
    assert abs(h["min"] - 4.30) < 0.01     # 4,30 % en 2025 (docs/v17/fuentes/titularidad.md)


def test_cota_alquiler_ordenada(hechos):
    h = hechos["V17-AUD-OT-COTA-GT-ALQUILER-NACIONAL"]
    assert h["min"] < h["max"]
    assert abs(h["min"] - 2.16) < 1e-6 and abs(h["max"] - 12.16) < 1e-6


def test_vacancia_decrece_con_tamano(hechos):
    t = [hechos[f"V17-AUD-OT-VAC-TASA-T{k}"]["valor"] for k in range(1, 5)]
    assert t == sorted(t, reverse=True)


def test_script_sin_red_ni_sellado():
    src = SCRIPT.read_text(encoding="utf-8")
    src = src.split('"""', 2)[2]           # sin la cadena de documentación
    for prohibido in ("requests", "urllib", "data/sealed", "evaluate_", "http://", "https://"):
        assert prohibido not in src
    assert "SEED = 20261010" in src
    assert "muestra_sellada_v6" in src


def test_determinista(tmp_path):
    antes = SALIDA.read_bytes() if SALIDA.exists() else None
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    primero = SALIDA.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    assert SALIDA.read_bytes() == primero
    if antes is not None:
        assert antes == primero
