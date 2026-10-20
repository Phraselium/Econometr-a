---
description: V18 · Fase 1 · Bibliografía
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 1 · Bibliografía: Hasta 3 subagentes bibliotecario en paralelo: descarga legítima y ficha de todas las referencias de la sección E y de las de docs/v15/literatura.md y docs/v16/literatura con versión abierta; búsqueda sistemática por factor con criterios escritos antes de buscar (docs/v18/bib/criterios.md); tabla resumen por factor con la unidad del efecto; verificación de DOI con src/v15/verificar_referencias.py.
3. Ejecuta solo esta fase (`make v18_f1`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
