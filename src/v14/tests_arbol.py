"""V14.1 · Recuento de tests del árbol público, leído de una ejecución real, y primera sección de su README.

- `python3 src/v14/tests_arbol.py --junit <informe.xml> --commit <hash>`: lee el informe JUnit de `pytest tests` ejecutado
  en el árbol público (con `make datos` y sin `make datos_terceros`) y escribe docs/v14/tests_arbol.json (pasados,
  omitidos, fallos, errores, commit del árbol y fecha).
- `readme_inicio()`: rellena docs/v14/plantillas/readme_arbol.md con ese recuento. La usa `make arbol_publico`.
- tests/conftest.py comprueba, al final de cada ejecución completa en el árbol público, que los pasados y omitidos
  coinciden con docs/v14/tests_arbol.json; tests/v14 comprueba que el README lleva esos números.
Sin red.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
JSON = RAIZ / "docs" / "v14" / "tests_arbol.json"
PLANTILLA = RAIZ / "docs" / "v14" / "plantillas" / "readme_arbol.md"


def leer_junit(ruta: Path) -> dict:
    raiz = ET.parse(ruta).getroot()
    suites = [raiz] if raiz.tag == "testsuite" else list(raiz.iter("testsuite"))
    tot = {k: sum(int(s.get(k, 0)) for s in suites) for k in ("tests", "failures", "errors", "skipped")}
    return {"pasados": tot["tests"] - tot["failures"] - tot["errors"] - tot["skipped"], "omitidos": tot["skipped"],
            "fallos": tot["failures"], "errores": tot["errors"]}


def recuento() -> dict:
    return json.loads(JSON.read_text(encoding="utf-8"))


def readme_inicio(r: dict | None = None) -> str:
    r = r or recuento()
    txt = PLANTILLA.read_text(encoding="utf-8")
    for k in ("pasados", "omitidos"):
        txt = txt.replace("{{" + k + "}}", str(r[k]))
    if "{{" in txt:
        raise SystemExit("tests_arbol: marcador sin resolver en docs/v14/plantillas/readme_arbol.md")
    return txt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--junit", required=True)
    ap.add_argument("--commit", required=True, help="commit de origen del árbol en el que se ejecutaron los tests")
    a = ap.parse_args()
    r = leer_junit(Path(a.junit))
    r.update({"commit_arbol": a.commit, "fecha": dt.date.today().isoformat(),
              "_nota": "Ejecución de `pytest tests` en el árbol público con `make datos` y sin `make datos_terceros` (src/v14/tests_arbol.py)."})
    JSON.write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("tests_arbol:", {k: r[k] for k in ("pasados", "omitidos", "fallos", "errores")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
