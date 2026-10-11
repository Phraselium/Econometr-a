# Mapa del repositorio

Qué hay en cada carpeta y qué es **VIGENTE** (lo que se cita y se mantiene) frente a **HISTÓRICO** (versiones cerradas; se conserva para la trazabilidad y porque los scripts vigentes leen parte de sus salidas). Actualizado: 11 de octubre de 2026 (auditoría v6).

## Raíz
| Fichero | Contenido |
|---|---|
| README.md | Presentación del proyecto (una página) |
| README_REPLICACION.md | Paquete de replicación: software, orden de los programas, fuentes y correspondencia salida-script |
| Makefile | `make all` (data → clean → models → report), `make check`, `make verificador` |
| CHANGELOG.md, ERRATA.md | Cambios por versión y fe de erratas |
| LICENSE, CITATION.cff, .zenodo.json | Licencias (MIT y CC BY 4.0) y metadatos de cita |
| requirements.lock | Versiones fijadas de Python |
| CLAUDE.md | Instrucciones de trabajo para los agentes |

## src/ (código)
| Ruta | Versión | Estado | Contenido |
|---|---|---|---|
| src/fetch_*.py, src/extract_*.py | v1-v2 | VIGENTE (`make data`) | Descargas con caché en data/raw |
| src/build_dataset*.py, src/holdout.py | v1-v2 | VIGENTE (`make clean`) | Paneles y muestras selladas (único acceso a data/sealed) |
| src/econ_utils.py, src/v2_common.py, src/utils_fetch.py | — | VIGENTE | Utilidades compartidas (Registry de especificaciones) |
| src/f2_*.py … src/f6_*.py, src/report.py | v1 | HISTÓRICO (se ejecuta en `make all`) | Modelos e informe v1 |
| src/v2/ | v2 | HISTÓRICO (se ejecuta) | Ramas BA, BV, BI, BO, BP, BM, BD, BS |
| src/v3/ | v3 | HISTÓRICO (se ejecuta); `check_texto.py` y `verificador.py` VIGENTES | PA, PB, POT, GL, C1, C3, PD; control de texto |
| src/v4/ | v4 | HISTÓRICO (se ejecuta) | M0-M7 y verificador v4 |
| src/v5/ | v5 | VIGENTE | Módulos R, A, B, C, D, E; `cifras_clave.py`, `render.py`, `verificador.py`, `check_v5.py` |
| src/v5_1/ | v5.1 | VIGENTE | T1-T4 (bajas, liberadas por envejecimiento, rangos, dirección); se ejecutan dentro de `V5_ORDEN` |
| src/v6/ | v6 | EN CURSO | `check_v6.py` |

## data/
| Ruta | Contenido |
|---|---|
| data/raw/ | Descargas versionadas (solo lectura); inventario en data/raw/_manifest.csv; subcarpetas v3, v4, v5, v5_1 por versión |
| data/raw/*_orig/, originales >50 MB | No versionados (.gitignore); checksum en data/CHECKSUMS.sha256 |
| data/processed/ | Paneles construidos por `make clean` (v1, v2, v3) |
| data/sealed/ | Muestras selladas; no versionadas; acceso solo por src/holdout.py |

## output/
| Ruta | Estado | Contenido |
|---|---|---|
| output/v5/ | **VIGENTE** | Entregables (informe_tecnico, working_paper, policy_brief, lo_que_sabemos, una_pagina, articulo_colegio, articulos/, ponencia/, linkedin/), generados por `render.py` desde docs/v5/plantillas |
| output/v5/cifras_clave.csv | **VIGENTE** | Tabla única de cifras: toda cifra de los entregables sale de aquí |
| output/v5/verificador/ | **VIGENTE** | Verificador de afirmaciones v5 (incluye fichas de v5.1) |
| output/v5/{R1*, A*, B*, C*, D*, E} | VIGENTE | Salidas de los módulos v5 (resultado.json, tablas, figuras) |
| output/v5_1/T1-T4, T6 | **VIGENTE** | Salidas de v5.1 |
| output/v6/ | EN CURSO | v6 |
| output/v4/ | HISTÓRICO | M0-M7 (los leen scripts de v5), verificador v4, informe_tecnico.md y lo_que_sabemos.md (citados por las plantillas v5) |
| output/v3/ | HISTÓRICO | PA, PB, POT, GL, C1, C3, PD, verificador v3 (los leen scripts de v4 y v5) |
| output/v2/ | HISTÓRICO | Ramas v2 e informe_v2.md |
| output/informe.md, output/f2-f6, output/tablas, output/registro_busqueda*.csv | HISTÓRICO | v1 |

## docs/
| Ruta | Estado | Contenido |
|---|---|---|
| docs/v5/plantillas/ | **VIGENTE** | Plantillas de los entregables v5 (se rellenan desde cifras_clave) |
| docs/v5/ | VIGENTE | Decisiones, backlog, pre-registro B3, licencias de datos, revisión humana (15 cifras), solicitudes, tareas del autor |
| docs/v5_1/ | VIGENTE | Plan, estado, decisiones y revisión de v5.1 |
| docs/v6/ | EN CURSO | Plan, estado, decisiones, auditoría y tareas del autor de v6 |
| docs/v2/, docs/v3/, docs/v4/ | HISTÓRICO | Planes, decisiones, revisiones, fuentes fallidas e hipótesis de cada versión |
| docs/*.md (raíz de docs), docs/fallidas/ | HISTÓRICO | v1: decisiones, revisiones F1-F7, literatura, fuentes fallidas |
| docs/MAPA.md | VIGENTE | Este fichero |

## archive/
Salidas superadas que ningún script, regla del Makefile, test ni plantilla lee o escribe: síntesis de v3 (articulo, informe_politica, lo_que_sabemos) y de v4 (working_paper, policy_brief). Registro de movimientos en archive/README.md.

## tests/
Tests de pytest (`make check`): utilidades v2, evaluaciones selladas en modo de ensayo y control de texto.
