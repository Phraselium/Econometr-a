---
description: V17 · Fase 2 · Inferencia convencional y mejor estimación
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 2 · Inferencia convencional y mejor estimación: B2-B5 sobre lo estimado (output/v17/lectura_bde/): inferencia convencional con la distorsión medida por Monte Carlo (no se publica si el tamaño real supera el 15 %), corrección por familia de pregunta, mejor estimación por canal con la escala del Banco de España, medidas de referencia.
3. Ejecuta solo esta fase (`make v17_f2`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
