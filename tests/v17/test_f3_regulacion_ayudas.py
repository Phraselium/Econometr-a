"""Análisis a posteriori (V17). Tests de src/v17/f3_regulacion_ayudas.py (auditoría, grupo regulacion_ayudas).

No escribe en el repositorio: hechos y registro se redirigen a un directorio temporal. El script tarda unos 25 s; se
ejecuta dos veces (determinismo).
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("f3_ra", ROOT / "src" / "v17" / "f3_regulacion_ayudas.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
LECTURAS = {"OF", "hecho", "cota", "asociación", "juicio experto", "no fiable", "no se puede saber", "sin cambio"}


def _correr(d: Path):
    M.OUT = d / "regulacion_ayudas_hechos.json"
    M.REGISTRO = d / "regulacion_ayudas_registro.csv"
    r = M.main()
    return r, json.loads(M.OUT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def corrida(tmp_path_factory):
    return _correr(tmp_path_factory.mktemp("ra1"))


def test_determinista(corrida, tmp_path):
    _, b = _correr(tmp_path)
    assert corrida[1] == b


def test_formato_hechos(corrida):
    _, h = corrida
    ids = [f["id"] for f in h]
    assert len(ids) == len(set(ids))
    for f in h:
        assert f["id"].startswith("V17-AUD-RA-")
        assert f["capa"] == "C4"
        assert f["lectura_v17"] in LECTURAS
        assert f["nota"].startswith("a posteriori")
        assert f["fuentes"]
        if f["min"] is not None and f["max"] is not None:
            assert f["min"] <= f["max"]


def test_valores_clave(corrida):
    r, h = corrida
    d = {f["id"]: f for f in h}
    assert abs(d["V17-AUD-RA-TOP-CONTRATOS-DIF"]["valor"] - 0.103) < 1e-9
    # id citado en ERRATA.md (P1): mediana 46 %, rango 3,6-78 %
    t = d["V17-AUD-RA-AYU-TRASLACION-MEDIANA"]
    assert (t["valor"], t["min"], t["max"]) == (46.0, 3.6, 78.0)
    assert abs(d["V17-AUD-RA-AYU-RETIENE-MEDIANA"]["valor"] - 54.0) < 1e-9
    assert "V17-AUD-RA-TOP-COMPOSICION" not in d          # retirado en la ronda 1
    # tabla de θ: todas las filas de traslación de L5 (sin la renta regulada ni las de precio de compra) y 3 añadidas
    tab = r["ayudas"]["tabla"]
    assert int(tab.principal.sum()) == 8
    assert (tab.theta > 1).sum() == 3                      # Fack (2005) DDD: 1,42, 1,02 y 1,45
    # duración del bono: la ganancia en el contrato es negativa si θ > 24/60
    assert d["V17-AUD-RA-AYU-BONO-DURACION"]["valor"] < 0
    # denominador turístico: stock sobre alquiler + turísticas, del orden del 10 % del Banco de España
    assert 9 < d["V17-AUD-RA-TUR-CUOTA-STOCK"]["valor"] < 13
    # descomposición de la Ley 11/2020 con el Incasòl: 60 de cantidad y 24 de renta
    inc = r["topes_inc"]["tabla"]
    assert len(inc) == 84
    assert (inc[inc.forma == "log_renta"].b < 0).all()


def test_cifras_publicadas_sin_cambio(corrida):
    p = corrida[0]["publicadas"]
    assert p["V9-D1b-renta-att"] == "-5.851"
    assert p["V9-D1b-contratos-att"] == "-1.317"
    assert p["B4-v3-vut-cantidad"] == "2.746"


def test_sin_red_ni_evaluacion():
    src = (ROOT / "src" / "v17" / "f3_regulacion_ayudas.py").read_text(encoding="utf-8")
    for prohibido in ("import requests", "import urllib", "http://", "https://", "holdout", "evaluate_("):
        assert prohibido not in src
    assert "muestra_sellada_v6" in src                     # filtra la muestra cerrada al leer la base
