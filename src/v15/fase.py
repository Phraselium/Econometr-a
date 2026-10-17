"""V15 · Lanzador de fases (`make v15_f0` … `make v15_f5`). Cada fase ejecuta, en orden, sus scripts deterministas y sin red.

Los scripts se añaden a FASES cuando existen; una fase sin scripts todavía lo dice y termina con código 0. Las fases 4 y 5
pasan antes por src/v15/puerta.py (Makefile). Nunca lanza estimaciones de versiones anteriores ni toca data/sealed.
Uso: python3 src/v15/fase.py f0|f1|f2|f3|f4|f5
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FASES: dict[str, list[str]] = {
    "f0": ["src/v15/f0_punto_partida.py"],
    "f1": ["src/v15/f1_inventario.py", "src/v15/f1_calidad.py", "src/v15/f1_potencia.py"],
    "f2": ["src/v15/verificar_referencias.py"],
    "f3": ["src/v15/f3_preregistro.py"],
    "f4": [],
    "f5": [],
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in FASES:
        print("uso: fase.py f0|f1|f2|f3|f4|f5")
        return 2
    f = sys.argv[1]
    if f in ("f4", "f5"):
        r = subprocess.run([sys.executable, str(RAIZ / "src/v15/puerta.py")], cwd=RAIZ)
        if r.returncode:
            return r.returncode
    scripts = [s for s in FASES[f] if (RAIZ / s).exists()]
    if not scripts:
        print(f"fase {f}: sin scripts todavía (docs/v15/estado.md)")
        return 0
    for s in scripts:
        print(f">> {s}")
        r = subprocess.run([sys.executable, str(RAIZ / s)], cwd=RAIZ)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
