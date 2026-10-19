---
description: V17 · Fase 4 · Documento estilo Banco de España (NO SE EJECUTA)
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 4 · Documento estilo Banco de España (NO SE EJECUTA): No se ejecuta: su contenido se integra en el Documento de Trabajo de la fase 6 de V18 (docs/v17/decisiones.md, K0).
3. Ejecuta solo esta fase (`make v17_f4`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
