"""K4c: ninguna cifra huérfana ni contradictoria nueva en los entregables principales output/v5/*.md. Sin red."""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src" / "v6_1"))
import k4c_cifras as k  # noqa: E402

# Lista cerrada de excepciones documentadas (fichero, cifra). 242.400: constante de corrección de la EPA fijada en v1 (informe v1, §5.1),
# declarada como tal en la nota K4b de la plantilla; no es un resultado de esta versión (docs/v6_1/auditoria_K4cd.md, K4c-01). Las excepciones de método están en k4c_cifras.EXCEPCIONES.
EXCEPCIONES_TEST: set[tuple[str, str]] = {("output/v5/informe_tecnico.md", "242.400")}


def test_sin_huerfanas_en_entregables_principales():
    df = k.escanear()
    principal = df[df.fichero.str.fullmatch(r"output/v5/[^/]+\.md")]
    malas = principal[principal.clase.isin(["HUERFANA", "CONTRADICTORIA"])]
    nuevas = [(r.fichero, r.cifra, r.linea) for r in malas.itertuples() if (r.fichero, r.cifra) not in EXCEPCIONES_TEST]
    assert not nuevas, f"cifras fuera de cifras_clave.csv: {nuevas[:10]}"


def test_tablas_literatura_cerradas():
    """v6.1: toda fila de tabla de docs/literatura.md termina en «|» (bs_tablas de v2 la parsea por columnas)."""
    from pathlib import Path
    raiz = Path(__file__).resolve().parents[1]
    malas = [i + 1 for i, ln in enumerate((raiz / "docs" / "literatura.md").read_text().splitlines())
             if ln.rstrip().startswith("|") and not ln.rstrip().endswith("|")]
    assert not malas, f"filas de tabla sin cerrar en docs/literatura.md: {malas[:10]}"
