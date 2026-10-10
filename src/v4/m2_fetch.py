"""M2: búsqueda (con red, NO forma parte de m2_run) de tablas del INE con hogares por edad de la persona de referencia.

Resultado (2026-10-10): TABLAS_OPERACION de CENSOP (463) y CENSOPV (8) no contienen tablas de hogares por edad de la
persona de referencia (ni 'hogar', ni 'persona de referencia'); no se descargó nada a data/raw/v4/.
"""
from __future__ import annotations

import json
import sys
import urllib.request


def main() -> None:
    for op in ("CENSOP", "CENSOPV"):
        url = f"https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/{op}"
        t = json.load(urllib.request.urlopen(url, timeout=60))  # noqa: S310
        hit = [x for x in t if any(k in x["Nombre"].lower() for k in ("hogar", "persona de referencia"))]
        print(op, len(t), "coincidencias:", [(x["Id"], x["Nombre"][:80]) for x in hit])


if __name__ == "__main__":
    sys.exit(main())
