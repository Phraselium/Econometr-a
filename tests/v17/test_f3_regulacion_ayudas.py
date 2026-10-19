"""Análisis a posteriori (V17). Tests de src/v17/f3_regulacion_ayudas.py (auditoría, grupo regulacion_ayudas).

No escribe en el repositorio: se redirige la salida a un directorio temporal.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("f3_ra", ROOT / "src" / "v17" / "f3_regulacion_ayudas.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def _correr(tmp_path):
    M.OUT = tmp_path / "regulacion_ayudas_hechos.json"
    r = M.main()
    return r, json.loads(M.OUT.read_text(encoding="utf-8"))


def test_determinista(tmp_path):
    _, a = _correr(tmp_path)
    _, b = _correr(tmp_path)
    assert a == b


def test_formato_hechos(tmp_path):
    _, h = _correr(tmp_path)
    assert h
    for f in h:
        assert f["id"].startswith("V17-AUD-")
        assert f["capa"] == "C4"
        assert f["lectura_v17"] in {"OF", "hecho", "cota", "asociación", "juicio experto", "no fiable",
                                    "no se puede saber", "sin cambio"}
        assert f["nota"].startswith("a posteriori")
        assert f["fuentes"]


def test_valores_clave(tmp_path):
    r, h = _correr(tmp_path)
    d = {f["id"]: f for f in h}
    # Jofre-Monseny et al. (0,001; 0,021) frente a Monràs y García-Montalvo (-0,102; 0,034)
    assert abs(d["V17-AUD-RA-TOP-CONTRATOS-DIF"]["valor"] - 0.103) < 1e-9
    assert abs(r["topes"]["z"] - 0.103 / (0.021 ** 2 + 0.034 ** 2) ** 0.5) < 1e-9
    assert abs(d["V17-AUD-RA-TOP-COMPOSICION"]["valor"] - 100 * 0.019 / 0.049) < 1e-3
    # retención del beneficiario: mediana de 7 estudios = 1 - 0,46
    assert len(r["ayudas"]["thetas"]) == 7
    assert abs(d["V17-AUD-RA-AYU-RETIENE-MEDIANA"]["valor"] - 54.0) < 1e-9
    b = d["V17-AUD-RA-AYU-BONO-RETIENE"]
    assert b["min"] <= b["valor"] <= b["max"]
    t = d["V17-AUD-RA-TUR-BCN-TRASLACION"]
    assert t["min"] <= t["valor"] <= t["max"]


def test_cifras_publicadas_sin_cambio(tmp_path):
    r, _ = _correr(tmp_path)
    p = r["publicadas"]
    assert p["V9-D1b-renta-att"] == "-5.851"
    assert p["V9-D1b-contratos-att"] == "-1.317"
    assert p["B4-v3-vut-cantidad"] == "2.746"


def test_sin_red_ni_sellado():
    src = (ROOT / "src" / "v17" / "f3_regulacion_ayudas.py").read_text(encoding="utf-8")
    for prohibido in ("import requests", "import urllib", "http://", "https://", "holdout", "evaluate_("):
        assert prohibido not in src
    assert '"data"' not in src   # no construye rutas bajo data/ (ni raw, ni base, ni la muestra cerrada)
