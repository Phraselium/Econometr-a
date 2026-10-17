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

- **Fase 1.**
  - Inventario: 340 variables y 467 combinaciones, todas anotadas (79 familias del inventariador y 6 del orquestador).
  - Auditorías de calidad, una por grupo en output/v15/auditoria/: precios de compra, alquiler, oferta y parque, demografía y hogares, financiación y macro. Faltan turismo y renta.
  - Potencia por pregunta: output/v15/potencia/informe.md.
  - Tres fallos de metadatos de la base 1.0 que no cambian ninguna cifra de cifras_clave (decisiones G4; tarea del autor).
- **Fase 2.**
  - Seis revisiones: P2, P3, P4, P5, P6 y P9.
  - 100 fichas: 88 VERIFICADA y 12 NO VERIFICADA. Cuartiles no verificados, porque Scimago bloquea la descarga (tarea del autor).
  - Síntesis en docs/v15/literatura.md.
- **Fase 3 (preparación).** sellar_v15 y evaluate_v15 en src/holdout.py, con tests. Todavía no se ha sellado nada.

## Siguiente
- Recoger las auditorías de turismo y renta.
- Fase 3: selección de preguntas, preregistro_v15.md, sellado, revisor-preregistro, adenda, etiqueta prereg-v15 y texto OSF. PARADA en la puerta.

<!-- las secciones siguientes las mantiene src/v15/registro_subagentes.py -->

## Subagentes y tokens

Generada por src/v15/registro_subagentes.py (fuente: docs/v15/subagentes.csv). Tokens aproximados según el informe de cada subagente.

| Fecha | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|
| 2026-10-17 | auditor-datos | F1.2 precios de compra | 103.963 | src/v15/auditoria/precios_compra.py; output/v15/auditoria/precios_compra/ |
| 2026-10-17 | inventariador | F1.1 anotaciones del inventario (79 familias) | 287.158 | docs/v15/inventario_anotaciones.csv |
| 2026-10-17 | auditor-datos | F1.2 alquiler | 179.787 | src/v15/auditoria/alquiler.py; output/v15/auditoria/alquiler/ |
| 2026-10-17 | auditor-datos | F1.2 oferta y parque | 193.197 | src/v15/auditoria/oferta_parque.py; output/v15/auditoria/oferta_parque/ |
| 2026-10-17 | lector-literatura | F2 P4 inmigración | 85.881 | docs/v15/literatura/P4_inmigracion.md |
| 2026-10-17 | auditor-datos | F1.2 demografía y hogares (incl. reparto alternativo B1) | 244.726 | src/v15/auditoria/demografia_hogares.py; output/v15/auditoria/demografia_hogares/ |
| 2026-10-17 | lector-literatura | F2 P5 pisos turísticos | 145.840 | docs/v15/literatura/P5_pisos_turisticos.md |
| 2026-10-17 | lector-literatura | F2 P6 topes y zonas tensionadas | 198.830 | docs/v15/literatura/P6_topes_alquiler.md |
| 2026-10-17 | lector-literatura | F2 P9 predicción | 86.141 | docs/v15/literatura/P9_prediccion.md |
| 2026-10-17 | lector-literatura | F2 P3 tipos de interés | 182.064 | docs/v15/literatura/P3_tipos_interes.md |
| 2026-10-17 | auditor-datos | F1.2 financiación y macro | 242.674 | src/v15/auditoria/financiacion_macro.py; output/v15/auditoria/financiacion_macro/ |
| 2026-10-17 | lector-literatura | F2 P2 fundamentales | 169.593 | docs/v15/literatura/P2_fundamentales.md |

Total: 2.119.854 tokens · auditor-datos: 964.347; inventariador: 287.158; lector-literatura: 868.349

<!-- fin subagentes -->
