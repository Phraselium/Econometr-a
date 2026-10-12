"""V7-R5: la congelación existe, sus sha256 coinciden y evaluar_congelado (simulado) devuelve las claves."""
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v7"))
CONG = RAIZ / "output" / "v7" / "R5" / "modelos_congelados.json"


def test_congelacion_sha256():
    assert CONG.exists()
    mj = json.loads(CONG.read_text(encoding="utf-8"))
    assert mj["ficheros_versionados_sha256"]
    for f, s in mj["ficheros_versionados_sha256"].items():
        assert hashlib.sha256((RAIZ / f).read_bytes()).hexdigest() == s
    pf = RAIZ / mj["predicciones"]["fichero"]
    assert hashlib.sha256(pf.read_bytes()).hexdigest() == mj["predicciones"]["sha256"]


def test_evaluar_simulado_claves():
    import r5_prediccion as R5
    res = R5.evaluar_congelado(CONG, datos=None, simular=True)
    for k in ("resumen", "por_ccaa", "dm", "permutacion", "holm"):
        assert k in res
    assert res["por_ccaa"]
