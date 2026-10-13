"""check_v8: la puerta V8 pasa y sus reglas detectan las infracciones que deben detectar."""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
sys.path.insert(0, str(RAIZ / "src"))
import check_v8 as C  # noqa: E402


def test_puerta_v8_sin_errores():
    r = subprocess.run([sys.executable, str(RAIZ / "src" / "v8" / "check_v8.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]


def test_detecta_cifra_libre_y_admite_umbrales():
    assert re.search(r"\d", C._libres("El precio subió un 12,3 % en P5."))
    assert not re.search(r"\d", C._libres("Banda del 68 % y umbral del 80 % en P5 (C3s); AR(4); log ×100."))


def test_detecta_causal_desde_shap():
    linea = "SHAP muestra que el turismo provoca la subida."
    assert C.CAUSAL.search(linea) and C.INTERP.search(linea) and not C.NEG.search(linea)
    assert C.NEG.search("SHAP no permite una lectura causal.")


def test_cifras_previas_intactas():
    assert C.cifras_previas() == []
