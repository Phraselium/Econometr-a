"""V13-A · CITATION.cff y .zenodo.json se generan desde proyecto.json (versión pública, fecha, repositorio). Nunca a mano.

`make metadatos` (también dentro de `make publicacion`). src/v13/check_v13.py comprueba que lo versionado coincide con lo
que se genera ahora. Determinista y sin red.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(RAIZ))
from src.v14 import terceros_1_0 as T10  # noqa: E402   (V14.3: aviso de la ODbL)

RESUMEN = ("Base de evidencia independiente y reproducible sobre la vivienda en España por provincias, con un módulo para València. "
           "Cubre el déficit y la necesidad de vivienda 2026-2035, las diferencias territoriales, los precios y el alquiler triangulados, "
           "la comparación europea, una matriz de instrumentos de política y un verificador de afirmaciones. Incluye una atribución por "
           "factores y periodos de la subida del precio de compra y del alquiler (V8), diseños de identificación pre-registrados (V9), "
           "una base de datos única con atlas descriptivo y web (V10) y una contabilidad demográfica, de hogares, titularidad y oferta (V12). "
           "Cada resultado se clasifica en capas de evidencia (C1, C2, C3, C3s y C4).")
KEYWORDS = ["vivienda", "España", "precios de la vivienda", "alquiler", "déficit de vivienda", "econometría", "reproducibilidad"]


def citation() -> str:
    kw = ", ".join(KEYWORDS)
    return f"""cff-version: 1.2.0
message: "Si usa este trabajo, cítelo así."
title: "{P['titulo']} ({P['version_publica']})"
type: software
authors:
  - family-names: Romero
    given-names: Borja
    affiliation: "Economista independiente"
version: "{P['version_publica']}"
date-released: "{P['fecha_version']}"
repository-code: "{P['repositorio']}"
url: "{P['repositorio']}"
license:
  - MIT
  - CC-BY-4.0
  - ODbL-1.0
keywords: [{kw}]
abstract: "{RESUMEN}"
"""


def zenodo() -> str:
    d = {
        "title": f"{P['titulo']} ({P['version_publica']})",
        "upload_type": "software",
        "description": RESUMEN + " Los datos de terceros sin redistribución clara no se incluyen: `make datos_terceros` los descarga y "
                                 "verifica (docs/v8_1/datos_retirados.md; docs/v13/datos_deposito.md); después, `make all` reproduce sin red. "
                                 f"La versión pública {P['version_publica']} reúne las versiones internas v1-V12 (CHANGELOG.md).",
        "creators": [{"name": "Romero, Borja", "affiliation": "Economista independiente"}],
        "version": P["version_publica"],
        "publication_date": P["fecha_version"],
        "language": "spa",
        "license": "MIT",
        "keywords": KEYWORDS,
        "related_identifiers": [{"identifier": P["repositorio"], "relation": "isSupplementTo", "scheme": "url"}],
        "notes": "Código bajo MIT; textos, tablas y figuras propios bajo CC BY 4.0 (fichero LICENSE). Los datos de terceros conservan sus "
                 "licencias: véase docs/v5/licencias_datos.md y docs/v13/datos_deposito.md. Las tablas, bases y cifras construidas con los "
                 "datos abiertos del Colegio de Registradores se publican bajo la Open Database License (ODbL) 1.0 "
                 "(https://opendatacommons.org/licenses/odbl/1-0/; lista de ficheros en docs/v14/licencias_tablas.csv). " + T10.AVISO_ODBL,
    }
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def generar() -> dict[str, str]:
    return {"CITATION.cff": citation(), ".zenodo.json": zenodo()}


def main() -> int:
    for rel, txt in generar().items():
        (RAIZ / rel).write_text(txt, encoding="utf-8")
    print("metadatos: CITATION.cff y .zenodo.json desde proyecto.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
