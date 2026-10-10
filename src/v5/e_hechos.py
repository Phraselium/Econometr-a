"""E (v5): cifras adicionales que piden los entregables, LEÍDAS de las salidas de los módulos (nada tecleado).

Cada redactor añade funciones `_xxx() -> list[dict]` y las registra en FUENTES. Escribe output/v5/E/hechos.json.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v5" / "E"


def h(i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha) -> dict:
    return dict(id=i, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per, cobertura=cob, fuentes=fue, capa=capa, fecha_dato=fecha)


FUENTES: list = []


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    filas = [x for f in FUENTES for x in f()]
    (OUT / "hechos.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    main()
