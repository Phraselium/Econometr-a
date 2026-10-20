---
description: V18 · Fase 0 · Punto de partida
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 0 · Punto de partida: Comprueba V17 (referencias, datos y auditoría). Inventaria qué datos de la base sirven para cada estudio de la sección E y cuáles faltan (output/v18/f0/). Lo que requiera al autor va a docs/v18/tareas_autor.md al principio y el trabajo sigue.
3. Ejecuta solo esta fase (`make v18_f0`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
