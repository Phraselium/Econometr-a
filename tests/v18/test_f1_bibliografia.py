"""V18 · Fase 1 · El catálogo se reconstruye sin red desde las fichas y la caché, y reconoce DOI con paréntesis."""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import f1_bibliografia as f1  # noqa: E402


def test_doi_con_parentesis():
    m = f1.DOI.search("- Clave: x · DOI: 10.1016/S0047-2727(01)00085-8 (edición publicada) · Revista")
    assert m.group(1) == "10.1016/S0047-2727(01)00085-8"


def test_sin_red_y_determinista():
    cat = RAIZ / "output" / "v18" / "f1" / "catalogo.csv"
    antes = cat.read_bytes()
    r = subprocess.run([sys.executable, str(RAIZ / "src" / "v18" / "f1_bibliografia.py")], cwd=RAIZ, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
    assert cat.read_bytes() == antes
