"""V17 · Lanzador de fases (`make v17_f0` … `make v17_f5`). Cada fase ejecuta, en orden, sus scripts deterministas y sin red.

V17 se ejecuta dentro de V18 (docs/v17/decisiones.md, K0): la fase 4 no se ejecuta y su contenido pasa al Documento de Trabajo de
V18. Todo lo de V17 es a posteriori. Nunca lanza estimaciones de versiones anteriores ni abre muestras selladas.
Uso: python3 src/v17/fase.py f0|f1|f2|f3|f4|f5
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

FASES: dict[str, list[str]] = {
    "f0": ["src/v17/f0_referencias.py"],
    "f1": ["src/v17/f1_inventario.py"],
    "f2": ["src/v17/f2_inferencia_v15_v16_micro.py", "src/v17/f2_inferencia_series_v8_v9_v12.py",
           "src/v17/f2_medidas_referencia.py", "src/v17/f2_lectura_bde.py"],
    "f3": ["src/v17/d3_cuantitativo.py", "src/v17/f3_auditoria.py"],
    "f4": [],
    "f5": ["src/v17/f5_hechos.py"],
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in FASES:
        print("uso: fase.py " + "|".join(FASES))
        return 2
    f = sys.argv[1]
    if f == "f4":
        print("fase f4 de V17: no se ejecuta; su contenido se integra en el Documento de Trabajo de V18 (docs/v17/decisiones.md, K0)")
        return 0
    scripts = [s for s in FASES[f] if (RAIZ / s.split()[0]).exists()]
    if not scripts:
        print(f"fase {f}: sin scripts todavía (docs/v17/estado.md)")
        return 0
    for s in scripts:
        print(f">> {s}")
        r = subprocess.run([sys.executable, str(RAIZ / s.split()[0]), *s.split()[1:]], cwd=RAIZ)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
