---
description: V18 · Fase 3 · Plan de replicación y etiqueta
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 3 · Plan de replicación y etiqueta: docs/v18/plan_replicacion.md (B1) con un apartado por estudio y por ampliación; revisor-preregistro y abogado-del-diablo; adenda; etiqueta local plan-replicacion-v18 y push de la rama (si el proxy no deja subir la etiqueta, la orden va a tareas_autor.md).
3. Ejecuta solo esta fase (`make v18_f3`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
