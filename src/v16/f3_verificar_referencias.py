"""V16-F3 · Verificador de referencias de docs/v16/literatura: el mismo de V15 (src/v15/verificar_referencias.py), con su propia caché
versionada (docs/v16/literatura/crossref_cache.json) y la tabla de cuartiles de Scimago de V15 (descarga del autor).

Sin red por defecto (lo que corre `make v16_f3`): falla si una ficha trae un DOI sin caché. Con `--red` consulta Crossref, DataCite o doi.org
y amplía la caché. Reescribe la línea «Estado:» de cada ficha: VERIFICADA, DISCREPANTE o NO VERIFICADA.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("v15_verificar_referencias", RAIZ / "src" / "v15" / "verificar_referencias.py")
VR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VR)
VR.LIT = RAIZ / "docs" / "v16" / "literatura"
VR.CACHE = VR.LIT / "crossref_cache.json"


def main() -> int:
    red = "--red" in sys.argv
    cuenta, errores = VR.procesar(red=red, escribir=True, solo="L*.md")
    for e in errores:
        print("ERROR", e)
    print("f3_verificar_referencias:", ", ".join(f"{k}: {v}" for k, v in sorted(cuenta.items())))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
