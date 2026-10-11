# Estado v6.1

## Hecho
- Preparación: rama `r6.1/main` desde 08d7629; creado docs/v6_1/; CLAUDE.md apunta a v6.1.

## Siguiente
- K1, K4a y K4b en paralelo.

## Tokens de subagentes (presupuesto 1,4 M; corte al 80 %: 1,12 M)
| Módulo | Tokens |
|---|---|

## En curso
- K1 (ml-engineer), K4a (sonnet) y K4b (sonnet), lanzados en paralelo.
- Para K4b se preparó docs/v6_1/k4b_especificacion.md: las 15 cifras sin referencias al código original.
- K1 terminado: unos 90.000 tokens; integrado en make (V6_1_ORDEN). cifras_clave ahora también lee output/v6_1/*/hechos.json.
- K4a está en curso. Este commit es intermedio e incluye correcciones parciales de K4a (fianzas Incasòl): ver docs/v6_1/auditoria_K4a.md cuando termine.
