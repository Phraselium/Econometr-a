"""Tests de F6: congelacion de predicciones y evaluate_v8 (ensayo)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CONG = RAIZ / "output" / "v8" / "congelacion"
ACC = RAIZ / "docs" / "v8" / "evaluate_v8_accesos.md"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def test_sha_coincide_con_notas_release():
    cj = json.loads((CONG / "congelacion.json").read_text(encoding="utf-8"))
    anot = [ln for ln in (RAIZ / "docs/v8/notas_release.md").read_text(encoding="utf-8").splitlines() if ln.startswith("sha256_predicciones_v8:")]
    assert anot and anot[0].split(":", 1)[1].split()[0] == cj["sha256_conjunto"]
    for f, s in cj["sha256_ficheros"].items():
        assert _sha(RAIZ / f) == s, f
    man = json.loads((CONG / "manifiesto.json").read_text(encoding="utf-8"))
    assert man["referencias"]["output/v8/M2/predicciones_congeladas.csv"] == _sha(RAIZ / "output/v8/M2/predicciones_congeladas.csv")
    assert "fecha_verificable: PENDIENTE" in (RAIZ / "docs/v8/notas_release.md").read_text(encoding="utf-8")


def test_ninguna_fecha_objetivo_pasada_es_evaluable():
    P = pd.read_csv(CONG / "predicciones_congeladas.csv")
    assert set(P["h"]) == {1, 2, 3, 4} and set(P["fecha_objetivo"]) == {"2026Q3", "2026Q4", "2027Q1", "2027Q2"}
    assert set(P["modelo"]) == {"ar4", "ar_fc", "ecm_v1"} and set(P["mercado"]) == {"compra", "alquiler"}
    for r in P.itertuples():
        assert bool(r.evaluable) == (r.fecha_objetivo > "2026Q2")
    M2 = pd.read_csv(RAIZ / "output/v8/M2/predicciones_congeladas.csv")
    assert not M2[M2["fecha_objetivo"] <= "2026Q2"]["evaluable"].astype(bool).any()


def test_simular_no_escribe_accesos():
    antes = ACC.read_bytes()
    r = subprocess.run([sys.executable, "-I", str(RAIZ / "src/v8/evaluate_v8.py"), "--simular"], cwd=RAIZ, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    assert ACC.read_bytes() == antes
    assert "Sin aperturas registradas." in ACC.read_text(encoding="utf-8")
    assert (CONG / "ensayo_evaluate.md").exists()
