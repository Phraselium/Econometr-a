"""V18 · Fase 3 · Comprobación del pre-registro interno (plan de replicación + adenda) frente a la etiqueta.

Comprueba que docs/v18/plan_replicacion.md y docs/v18/plan_replicacion_adenda.md no han cambiado desde el commit de la etiqueta
plan-replicacion-v18 (src/v18/etiqueta.py) y que docs/v18/sellado_v18.json, si existe, se creó después de ella. No lee datos.
Uso: python3 src/v18/f3_plan.py (make v18_f3; la guarda (g) exige la etiqueta)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import etiqueta  # noqa: E402

PREREG = ["docs/v18/plan_replicacion.md", "docs/v18/plan_replicacion_adenda.md"]
SELLADO = "docs/v18/sellado_v18.json"


def main() -> int:
    ok, motivo = etiqueta.puerta()
    if not ok:
        print(f"f3_plan V18: puerta cerrada ({motivo})")
        return 1
    c = etiqueta.commit_etiqueta()
    err = []
    for f in PREREG:
        r = subprocess.run(["git", "diff", "--quiet", c, "--", f], cwd=RAIZ)
        if r.returncode:
            err.append(f"{f} ha cambiado desde {etiqueta.ETIQUETA} ({c[:7]}): un cambio va en una adenda nueva, fechada")
    if (RAIZ / SELLADO).exists():
        r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", SELLADO], cwd=RAIZ, capture_output=True, text=True)
        primero = (r.stdout.split() or [None])[-1]
        if primero and not etiqueta.es_posterior(primero):
            err.append(f"{SELLADO} entró en git antes de la etiqueta")
    for e in err:
        print(f"  - {e}")
    print(f"f3_plan V18: {motivo}; pre-registro {'intacto' if not err else 'con cambios'}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
