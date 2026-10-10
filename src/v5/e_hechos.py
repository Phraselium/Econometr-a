"""E (v5): cifras adicionales que piden los entregables, LEÍDAS de las salidas de los módulos (nada tecleado).

Cada redactor escribe su propio módulo `src/v5/e_hechos_<redactor>.py` con una función `filas() -> list[dict]`
(usando `h(...)` de aquí). Este script los carga todos en orden alfabético y escribe output/v5/E/hechos.json.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v5" / "E"


def h(i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha) -> dict:
    return dict(id=i, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per, cobertura=cob, fuentes=fue, capa=capa, fecha_dato=fecha)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    filas = []
    for p in sorted((RAIZ / "src" / "v5").glob("e_hechos_*.py")):
        spec = importlib.util.spec_from_file_location(p.stem, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        filas += m.filas()
    (OUT / "hechos.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()
