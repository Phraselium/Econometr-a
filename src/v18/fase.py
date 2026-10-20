"""V18 · Lanzador de fases (`make v18_f0` … `make v18_f6`). Cada fase ejecuta, en orden, sus scripts deterministas y sin red.

Las fases 3 (comprobación del plan etiquetado), 4, 5 y 6 exigen la puerta del plan de replicación (src/v18/etiqueta.py); la guarda (g) del
hook lo comprueba también antes de lanzar make. Nunca lanza estimaciones de versiones anteriores ni abre muestras selladas.
Uso: python3 src/v18/fase.py f0|f1|f2|f3|f4|f5|f6
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import etiqueta  # noqa: E402

# Los scripts se añaden a su fase a medida que existen (docs/v18/estado.md).
FASES: dict[str, list[str]] = {
    "f0": ["src/v18/f0_inventario.py"],
    "f1": ["src/v18/f1_bibliografia.py"],
    "f2": ["src/v18/f2_reproduccion.py"],
    "f3": ["src/v18/f3_plan.py"],
    "f4": [],
    "f5": [],
    "f6": [],
}
CON_PUERTA = {"f3", "f4", "f5", "f6"}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in FASES:
        print("uso: fase.py " + "|".join(FASES))
        return 2
    f = sys.argv[1]
    if f in CON_PUERTA:
        ok, motivo = etiqueta.puerta()
        if not ok:
            print(f"fase {f} de V18 bloqueada: {motivo} (plan V18, B1)")
            return 1
    scripts = [s for s in FASES[f] if (RAIZ / s).exists()]
    if not scripts:
        print(f"fase {f}: sin scripts todavía (docs/v18/estado.md)")
        return 0
    for s in scripts:
        print(f">> {s}")
        r = subprocess.run([sys.executable, str(RAIZ / s)], cwd=RAIZ)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
