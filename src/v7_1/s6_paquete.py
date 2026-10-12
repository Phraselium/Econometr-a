"""V7.1-S6 · Renderiza docs/v7_1/release_notes.md desde su plantilla (las cifras salen de cifras_clave). Sin red, determinista."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import render as R  # noqa: E402


def main() -> int:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    txt, falta = R.render(RAIZ / "docs" / "v7_1" / "plantillas" / "release_notes.md", ck)
    if falta:
        print(f"s6_paquete: marcadores sin cifra: {sorted(set(falta))}")
        return 1
    (RAIZ / "docs" / "v7_1" / "release_notes.md").write_text(txt, encoding="utf-8")
    print("s6_paquete: docs/v7_1/release_notes.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
