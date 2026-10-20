---
description: V18 · Fase 5 · Magnitudes preferidas y contabilidad de la subida
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 5 · Magnitudes preferidas y contabilidad de la subida: Magnitud preferida por factor (B5, metaanálisis bayesiano de efectos aleatorios o media ponderada por precisión); contabilidad de la subida por periodo y territorio con Monte Carlo sobre las magnitudes y fila «no explicado»; comparación con el SVAR de V8 y con el Banco de España.
3. Ejecuta solo esta fase (`make v18_f5`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
