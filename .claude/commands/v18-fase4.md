---
description: V18 · Fase 4 · Estimación
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 4 · Estimación: Solo con la etiqueta plan-replicacion-v18 (la guarda del hook lo exige). Hasta 3 modelizador en worktrees; montecarlo para cada herramienta nueva. Por estudio: réplica, ampliación, pruebas B4, inferencia B2, clasificación B3, replicador-ciego y abogado-del-diablo (B6). Modelos de conjunto F1-F4. Unidades selladas excluidas (holdout.excluir_sellados_v6).
3. Ejecuta solo esta fase (`make v18_f4`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
