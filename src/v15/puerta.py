"""V15 · Puerta del pre-registro: las fases 4 (estimación) y 5 (síntesis) solo corren si proyecto.json tiene `osf_prereg_v15`
(DOI o URL del registro en OSF) y su fecha (`osf_prereg_v15_fecha`, AAAA-MM-DD) es anterior o igual a la primera estimación.

Uso: python3 src/v15/puerta.py  → código 0 si la puerta está abierta; 1 (con el motivo) si no.
La guarda (d) de .claude/hooks/guardas_bash.py hace la misma comprobación antes de lanzar `make v15_f4*` o `make v15_f5*`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def abierta(p: dict | None = None) -> tuple[bool, str]:
    p = p if p is not None else json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
    v = str(p.get("osf_prereg_v15") or "").strip()
    if not v or v.upper() == "PENDIENTE":
        return False, "falta osf_prereg_v15 en proyecto.json: las fases 4 y 5 esperan al depósito del pre-registro en OSF"
    return True, f"puerta abierta: osf_prereg_v15 = {v} (fecha {p.get('osf_prereg_v15_fecha', 'sin fecha')})"


def main() -> int:
    ok, motivo = abierta()
    print(f"puerta V15: {motivo}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
