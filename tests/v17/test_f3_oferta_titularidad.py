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
        assert h["tipo_rango"] in ("rango", "referencias", "sin rango")
        assert (h["tipo_rango"] == "sin rango") == (h["min"] is None or h["max"] is None)
        assert h["cobertura"] and "véase" not in h["cobertura"].lower()


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


def test_ronda1(hechos):
    assert hechos["V17-AUD-OT-CAT-GT-PROV-FRENTE-SUMA-MUN-2026"]["valor"] > 1          # tramo por NIF dentro de cada ámbito
    assert abs(hechos["V17-AUD-OT-PUB-UE-MEDIA-SIMPLE"]["valor"] - 7.99) < 0.01           # media simple de la OCDE
    c = hechos["V17-AUD-OT-COTA-GT-ALQUILER-PRIVADOS"]
    assert c["min"] <= c["max"] <= hechos["V17-AUD-OT-COTA-GT-ALQUILER-CON-PUBLICA"]["max"]
    s = hechos["V17-AUD-OT-SUELO-BARCELONA-RATIO"]
    assert s["min"] < s["valor"] < s["max"] < 1


def test_script_sin_red_ni_sellado():
    src = SCRIPT.read_text(encoding="utf-8")
    src = src.split('"""', 2)[2]           # sin la cadena de documentación
    for prohibido in ("requests", "urllib", "data/sealed", "evaluate_", "http://", "https://"):
        assert prohibido not in src
    assert "SEED = 20261010" in src
    assert "excluir_sellados_v6(" in src


def test_determinista(tmp_path):
    antes = SALIDA.read_bytes() if SALIDA.exists() else None
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    primero = SALIDA.read_bytes()
    subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, cwd=ROOT)
    assert SALIDA.read_bytes() == primero
    if antes is not None:
        assert antes == primero


def test_empleo_y_guarda(hechos):
    for n in ("5A", "10A"):
        e = hechos[f"V17-AUD-OT-EMPLEO-INCREMENTO-RANGO-{n}"]
        assert 0 < e["min"] < e["valor"] < e["max"] and e["lectura_v17"] == "juicio experto"
    assert hechos["V17-AUD-OT-EMPLEO-INCREMENTO-RANGO-10A"]["max"] < hechos["V17-AUD-OT-EMPLEO-INCREMENTO-RANGO-5A"]["max"]
    assert "9 CCAA" in hechos["V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71"]["cobertura"]
    assert "V17-AUD-OT-CAT-GT-TOTAL-FRENTE-SUMA-PROV-2026" not in hechos
