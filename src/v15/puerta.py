"""V15 · Puerta del pre-registro (V16: pre-registro interno, sin sello de tiempo externo).

Las fases de estimación de V15 y la apertura de su muestra sellada solo corren si la etiqueta `prereg-v15` existe en el
remoto y apunta al commit 542b4fd (src/v16/etiquetas.py). Ya no se usa OSF (docs/v16/plan.md, regla A y fase 0).

Uso: python3 src/v15/puerta.py  → código 0 si la puerta está abierta; 1 (con el motivo) si no.
La guarda (d) de .claude/hooks/guardas_bash.py hace la misma comprobación antes de lanzar `make v15_f4*` o `make v15_f5*`.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16"))
import etiquetas  # noqa: E402


def abierta(p: dict | None = None) -> tuple[bool, str]:
    """`p` (proyecto.json) se acepta por compatibilidad y no se usa: la puerta es la etiqueta publicada en el remoto."""
    return etiquetas.prereg_v15_publicada(RAIZ)


def main() -> int:
    ok, motivo = abierta()
    print(f"puerta V15: {motivo}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
