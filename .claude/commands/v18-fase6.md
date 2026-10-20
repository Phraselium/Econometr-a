---
description: V18 · Fase 6 · Documento de Trabajo e integración
---
1. Lee CLAUDE.md, docs/v18/plan.md, docs/v18/estado.md, docs/v18/decisiones.md y docs/v18/tareas_autor.md. Respeta las reglas A, el estándar B y las paradas G.
2. Fase 6 · Documento de Trabajo e integración: publicacion/documento_v18/ con make (formato Documento de Trabajo del Banco de España, incluidas las secciones de V17: demografía, general o local, factibilidad, discurso y medidas auditadas); arbitro-final; verificador-cifras; tablas_v18.xlsx; check_v18; make publicacion, make web y make check limpios.
3. Ejecuta solo esta fase (`make v18_f6`). Registra cada subagente con `python3 src/v18/registro_subagentes.py` (tope 6 millones de tokens por fase; si se supera, para y explícalo).
4. Actualiza docs/v18/estado.md (hecho / siguiente / tokens) y docs/v18/decisiones.md; lo que dependa del autor, a docs/v18/tareas_autor.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
