# V15 · Estado

Plan: docs/v15/plan.md (íntegro). Versión pública vigente: 1.0. V15 solo añade cifras V15-* y se publicará como 1.1.

## Hecho
- **Plan** guardado íntegro en docs/v15/plan.md (0e4ca8a) y aviso en CLAUDE.md.
- **B1 · Guardas.**
  - .claude/settings.json: permissions.deny para leer, editar y escribir la muestra sellada; make clean, make all, make v7, make evaluate_v7, git push --force, git filter-repo, rm -rf data y rm -rf output.
  - .claude/hooks/guardas_bash.py, hook PreToolUse de Bash, que rechaza:
    - (a) heredocs sin comillas;
    - (b) cualquier mención de la muestra sellada salvo src/holdout.py;
    - (c) un segundo make check (bloqueo /tmp/econometra_make_check.lock que escribe el Makefile, o un proceso `make check` vivo);
    - (d) make v15_f4* y v15_f5* sin osf_prereg_v15;
    - (e) los mismos comandos prohibidos que deny.
  - tests/v15/test_guardas.py: 27 casos. Además, intentos reales que fallaron como debían: `make clean` (hook), listar la muestra sellada (hook) y leerla con Read (permissions.deny).
- **B2 · Subagentes** en .claude/agents/: inventariador (haiku), auditor-datos, lector-literatura, montecarlo y modelizador (sonnet), y revisor-preregistro y arbitro-final (opus, sin Write ni Bash). Cada uno lleva su tope de tokens.
- **B3 · Herramientas.**
  - src/v15/verificar_referencias.py: Crossref con caché versionada para funcionar sin red, cuartil desde docs/v15/scimago_cuartiles.csv, estados VERIFICADA / NO VERIFICADA / DISCREPANTE y fallo ante un DOI inexistente.
  - src/v15/registro_subagentes.py.
  - src/v15/puerta.py y src/v15/fase.py.
  - Tests en tests/v15/test_herramientas_v15.py.
- **B4 · Comandos y make.**
  - .claude/commands/v15-fase0 … v15-fase5 y v15-estado.
  - Makefile: v15_f0 … v15_f5, v15, check_v15, y check_v15 dentro de make check.

- **B5 · Comprobación.**
  - Tests de las guardas en verde (33 tests en tests/v15).
  - `make check` en solitario: 436 pasados; solo el aviso del hash pendiente; check_v15 sin errores; git sin cambios.
  - Commit «V15 infraestructura» (eb61254).

- **Fase 0.**
  - V14.4 aplicada (5557c25): las cuatro fuentes de terceros en «agregados» y las 16 cifras reincorporadas a los textos; cifras_clave sin cambios.
  - docs/v15/punto_partida.md (unas 1.300 palabras): preguntas sin respuesta con su causa, 7 resultados frágiles y 7 debilidades.
  - Entre las debilidades, siete cifras C1 que no cumplen la definición de C1. Queda para el autor (tareas_autor.md) y no se corrige.

## Siguiente
- Fase 1: inventario (inventariador), calidad (auditor-datos por grupos) y potencia por pregunta candidata.

<!-- las secciones siguientes las mantiene src/v15/registro_subagentes.py -->

## Subagentes y tokens

Generada por src/v15/registro_subagentes.py (fuente: docs/v15/subagentes.csv). Tokens aproximados según el informe de cada subagente.

| Fecha | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|
| 2026-10-17 | auditor-datos | F1.2 precios de compra | 103.963 | src/v15/auditoria/precios_compra.py; output/v15/auditoria/precios_compra/ |
| 2026-10-17 | inventariador | F1.1 anotaciones del inventario (79 familias) | 287.158 | docs/v15/inventario_anotaciones.csv |

Total: 391.121 tokens · auditor-datos: 103.963; inventariador: 287.158

<!-- fin subagentes -->
