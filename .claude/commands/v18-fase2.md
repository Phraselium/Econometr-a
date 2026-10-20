---
description: V18 · Fase 2 · Reproducción de los estudios originales
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 2 · Reproducción de los estudios originales: Hasta 3 subagentes replicador-estudio: para cada estudio con paquete de replicación, reproduce su resultado principal con sus datos y compáralo con lo publicado. Sin paquete, anótalo. Resultado: docs/v18/reproduccion.md.
3. Ejecuta solo esta fase (`make v18_f2`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
