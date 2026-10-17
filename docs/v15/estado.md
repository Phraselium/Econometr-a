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
- **Fase 1 completa.** Siete auditorías, incluidas turismo (BCN por barrio solo desde 2023T1; el INE VUT empieza en 2021) y renta (AEAT 2013-2015 no utilizable).
- **Fase 3.**
  - Pre-registro (docs/v15/preregistro_v15.md) con: H1 y H2 (zonas tensionadas), H4 (inmigración), H3 (asociación de turismo), H5 (predicción), E1-E4, y P1, P3 y P8 descartadas.
  - Validación sellada ejecutada antes de estimar (src/v15/f3_sellado.py; docs/v15/sellado_v15.json; decisiones G6).
  - revisor-preregistro: APTO CON CAMBIOS, 18 hallazgos. Adenda vinculante: docs/v15/preregistro_v15_adenda.md (Holm m = 3, preperiodo 2022T2-2023T4, CS y SDID, evaluación sellada como condición de C3, multiverso ≤ 408).
  - `make check` en solitario: 440 pasados; solo el aviso del hash; check_v15 sin errores; git sin cambios.
  - Etiqueta local prereg-v15 y texto para OSF en tareas_autor.md.

## Siguiente
- **PARADA en la puerta.** Las fases 4 y 5 esperan a que el autor deposite en OSF y ponga `osf_prereg_v15` en proyecto.json.
- Al reanudar:
  - comprobar que la fecha del depósito es anterior a cualquier estimación;
  - montecarlo valida las herramientas;
  - recálculo de potencias del punto 9 de la adenda;
  - modelizadores por pregunta.

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
| 2026-10-17 | auditor-datos | F1.2 renta y microdatos (AEAT 2013-2015) | 203.774 | src/v15/auditoria/renta_microdatos.py; output/v15/auditoria/renta_microdatos/ |
| 2026-10-17 | auditor-datos | F1.2 turismo | 290.251 | src/v15/auditoria/turismo.py; output/v15/auditoria/turismo/ |
| 2026-10-17 | revisor-preregistro | F3.4 revisión del pre-registro (APTO CON CAMBIOS. 18 hallazgos) | 82.220 | docs/v15/preregistro_v15_adenda.md |

Total: 2.696.099 tokens · auditor-datos: 1.458.372; inventariador: 287.158; lector-literatura: 868.349; revisor-preregistro: 82.220

<!-- fin subagentes -->
