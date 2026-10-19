---
description: V17 · Fase 0 · Referencias del Banco de España y del INE
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 0 · Referencias del Banco de España y del INE: Localiza y lee lo publicado por el Banco de España, el BCE y el INE (plan, fase 0); docs/v17/referencias_bde.md con la tabla de comparación y docs/v17/correcciones.md (D4). Subagentes lector-literatura (hasta 3 en paralelo).
3. Ejecuta solo esta fase (`make v17_f0`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
