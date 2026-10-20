# V18 · Estado

V18: bibliografía, replicación de estudios y estimación del impacto de cada factor (docs/v18/plan.md). V17 cerrada dentro de V18 (fases 0-3 y 5; docs/v17/resumen.md).

## Hecho
- 2026-10-20 · **Infraestructura C.**
  - Subagentes nuevos: bibliotecario y replicador-estudio (.claude/agents/).
  - Comandos /v18-fase0 … /v18-fase6 y /v18-estado; objetivos make v18_f0 … v18_f6, v18 y check_v18 (dentro de make check).
  - Puerta del plan de replicación (src/v18/etiqueta.py): etiqueta local plan-replicacion-v18 con su commit en la rama remota. La guarda (g) del hook rechaza las fases 3 a 6 y make v18 sin ella; src/v18/fase.py lo comprueba también.
  - check_v18: cifras V18 con id, fuente, capa y clasificación; sin lenguaje causal por debajo de IDENTIFICADO; ninguna estimación anterior a la etiqueta; ningún PDF versionado, citas de 15 palabras como máximo y sha256 de cada PDF.
  - data/bib/ fuera de git salvo data/bib/CHECKSUMS.sha256; registro de subagentes con tope de 6 millones por fase.

## Siguiente
- Fase 0: comprobar V17 e inventariar datos por estudio (E1-E12 y F1-F4); tareas del autor al principio de tareas_autor.md.

## Subagentes y tokens

Sin subagentes todavía.

<!-- fin subagentes -->
