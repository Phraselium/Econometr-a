"""V9 F5 · rellena docs/v9/plantillas/*.md -> output/v9/ con output/v5/cifras_clave.csv (marcadores {{id}}, {{id:campo}},
{{id:cita}}), reutilizando el renderizador de V8 (src/v8/render_v8.py, que a su vez importa src/v5/render.py).
Un marcador sin resolver es un error (código de salida 1). Uso: python3 src/v9/render_v9.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import render_v8  # noqa: E402

PLANT = RAIZ / "docs" / "v9" / "plantillas"
OUT = RAIZ / "output" / "v9"


def main() -> int:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    errores = 0
    for p in sorted(PLANT.glob("*.md")):
        txt, falta = render_v8.render(p, ck)
        (OUT / p.name).write_text(txt, encoding="utf-8")
        if falta:
            errores += len(falta)
            print(f"{p.relative_to(RAIZ)}: marcadores sin cifra: {sorted(set(falta))}")
    print(f"render_v9: {errores} marcadores sin resolver")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
