---
description: V17 · Fase 5 · Integración
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 5 · Integración: check_v17 en make check; make publicacion, make web y make check limpios; commit y push.
3. Ejecuta solo esta fase (`make v17_f5`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
