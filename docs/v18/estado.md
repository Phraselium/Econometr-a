# V18 · Estado

V18: bibliografía, replicación de estudios y estimación del impacto de cada factor (docs/v18/plan.md). V17 cerrada dentro de V18 (fases 0-3 y 5; docs/v17/resumen.md).

## Hecho
- 2026-10-20 · **Infraestructura C.**
  - Subagentes nuevos: bibliotecario y replicador-estudio (.claude/agents/).
  - Comandos /v18-fase0 … /v18-fase6 y /v18-estado; objetivos make v18_f0 … v18_f6, v18 y check_v18 (dentro de make check).
  - Puerta del plan de replicación (src/v18/etiqueta.py): etiqueta local plan-replicacion-v18 con su commit en la rama remota. La guarda (g) del hook rechaza las fases 3 a 6 y make v18 sin ella; src/v18/fase.py lo comprueba también.
  - check_v18: cifras V18 con id, fuente, capa y clasificación; sin lenguaje causal por debajo de IDENTIFICADO; ninguna estimación anterior a la etiqueta; ningún PDF versionado, citas de 15 palabras como máximo y sha256 de cada PDF.
  - data/bib/ fuera de git salvo data/bib/CHECKSUMS.sha256; registro de subagentes con tope de 6 millones por fase.

- 2026-10-20 · **Fase 0 cerrada.** V17 completa (check_v17 sin errores). Inventario de 103 variables (output/v18/f0/): E1, E2, E3, E5, E6 (piloto en València), E7, E8, E9 y F1-F3 replicables en parte; E4, E10, E11 y E12 NO ESTIMABLES con los datos actuales. Paneles provinciales con 39 provincias (11 selladas fuera). 14 tareas del autor al principio de docs/v18/tareas_autor.md.

## Siguiente
- Fase 1: bibliografía (grupos A y B en marcha; C después).

## Subagentes y tokens

Generada por src/v18/registro_subagentes.py (fuente: docs/v18/subagentes.csv). Tokens aproximados según el informe de cada subagente. Tope por fase: 6.000.000 (parada G).

| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|---|
| 2026-10-20 | F0 | general-purpose | inventario de datos por estudio (E1-E12, F1-F3) y tareas del autor | 259.633 | src/v18/f0_inventario.py; output/v18/f0/; docs/v18/tareas_autor.md |
| 2026-10-20 | F1 | bibliotecario | grupo B: inmigración, oferta y suelo, obra nueva, vivienda pública (47 fichas) | 470.079 | docs/v18/bib/{inmigracion,oferta_suelo,obra_nueva,vivienda_publica}/ |
| 2026-10-20 | F1 | bibliotecario | grupo A: turismo, topes, grandes tenedores, vacías (51 fichas) | 550.339 | docs/v18/bib/{turismo,topes,grandes_tenedores,vacias}/ |

| Fase | Tokens de subagentes |
|---|---|
| F0 | 259.633 |
| F1 | 1.020.418 |

Total V18: 1.280.051 tokens

<!-- fin subagentes -->
