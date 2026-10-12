# Mapa del repositorio

Qué hay en cada carpeta y qué es **VIGENTE** (lo que se cita y se mantiene) frente a **HISTÓRICO** (versiones cerradas; se conserva para la trazabilidad y porque los scripts vigentes leen parte de sus salidas). Actualizado: 12 de octubre de 2026 (v7.1, versión de referencia). Para leer, empiece por [LEEME_PRIMERO.md](../LEEME_PRIMERO.md).

## Estructura para el lector (v7.1)
| Carpeta | Estado | Contenido |
|---|---|---|
| [publicacion/](../publicacion/MANIFIESTO.md) | **VIGENTE**, generado | Entregables vigentes, atlas regional, verificador y cifras_clave.csv. Lo genera `make publicacion` (src/v7_1/publicacion.py) desde output/; nunca se edita a mano |
| [metodologia/](../metodologia/MANIFIESTO.md) | **VIGENTE**, generado | Anexo metodológico, guía del revisor, capas, historial de conclusiones, validación Monte Carlo, pre-registro V7, dosis y coste |
| [reproducir/](../reproducir/MANIFIESTO.md) | **VIGENTE**, generado | Instrucciones, entorno, tiempos, ensayo y protocolo de evaluate_v7 |
| [historico/](../historico/INDICE.md) | HISTÓRICO | Documentos de versiones cerradas que ningún script lee (movidos con `git mv`) e índice por versión |

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
| src/v6/ | v6 | HISTÓRICO (se ejecuta en `make all`); `check_v6.py` VIGENTE | M0-M4 de v6 |
| src/v6_1/, src/v6_2/, src/v6_3/ | v6.1-v6.3 | HISTÓRICO (se ejecutan en `make all`) | K1-K6, L1-L5, VER |
| src/v7/ | v7.0 | VIGENTE (`make v7`) | Atlas regional R1-R7, herramientas de panel, evaluate_v7 |
| src/v7_1/ | v7.1 | VIGENTE (`make v7_1`, `make publicacion`) | Dosis y coste (S1), cifras de difusión (S3), ensayo de evaluate_v7 (S4), generador de publicacion/ (S5) |

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
| output/v5/ | **VIGENTE** (fuente de publicacion/) | Entregables (informe_tecnico, working_paper, policy_brief, lo_que_sabemos, una_pagina, articulo_colegio, articulos/, ponencia/, linkedin/), generados por `render.py` desde docs/v5/plantillas |
| output/v5/cifras_clave.csv | **VIGENTE** | Tabla única de cifras: toda cifra de los entregables sale de aquí |
| output/v5/verificador/ | **VIGENTE** | Verificador de afirmaciones v5 (incluye fichas de v5.1) |
| output/v5/{R1*, A*, B*, C*, D*, E} | VIGENTE | Salidas de los módulos v5 (resultado.json, tablas, figuras) |
| output/v5_1/T1-T4, T6 | **VIGENTE** | Salidas de v5.1 |
| output/v6/ | HISTÓRICO (lo regenera `make all`) | v6 |
| output/v6_1/, output/v6_2/, output/v6_3/ | HISTÓRICO (lo regenera `make all`); el anexo de v6.2 sigue vigente en metodologia/ | K1-K6, L1-L5, VER |
| output/v7/ | VIGENTE (`make v7`) | Atlas regional V7: paneles, Monte Carlo, modelos, predicción congelada, propuestas |
| output/v7_1/ | VIGENTE (`make v7_1`) | Dosis y coste, atlas v7.1, verificador v7.1, cifras de difusión, ensayo de evaluate_v7 |
| output/v4/ | HISTÓRICO | M0-M7 (los leen scripts de v5), verificador v4, informe_tecnico.md y lo_que_sabemos.md (citados por las plantillas v5) |
| output/v3/ | HISTÓRICO | PA, PB, POT, GL, C1, C3, PD, verificador v3 (los leen scripts de v4 y v5) |
| output/v2/ | HISTÓRICO | Ramas v2 e informe_v2.md |
| output/informe.md, output/f2-f6, output/tablas, output/registro_busqueda*.csv | HISTÓRICO | v1 |

## docs/
| Ruta | Estado | Contenido |
|---|---|---|
| docs/v5/plantillas/ | **VIGENTE** | Plantillas de los entregables v5 (se rellenan desde cifras_clave) |
| docs/v5/ | VIGENTE | Decisiones, backlog, pre-registro B3, licencias de datos, revisión humana (15 cifras), solicitudes, tareas del autor |
| docs/v5_1/ | HISTÓRICO | Decisiones y revisión de v5.1 (plan y estado en historico/docs/v5_1/) |
| docs/v6/, docs/v6_1/, docs/v6_2/ | HISTÓRICO | Pre-registros, diccionarios, decisiones, historial de conclusiones, backlog, guía del revisor de v6.2 y cifras publicables (lo que leen scripts y tests). Planes, estados, auditorías y arbitrajes en historico/docs/ |
| docs/v2/, docs/v3/, docs/v4/ | HISTÓRICO | Decisiones, fuentes fallidas e hipótesis que leen los scripts; planes y revisiones en historico/docs/ |
| docs/v7/ | VIGENTE | Pre-registro V7, decisiones, validación de herramientas, notas de la release, registro de accesos de evaluate_v7 |
| docs/v7_1/ | VIGENTE | Plan, estado, decisiones, guía del revisor, capas, tiempos, protocolo de evaluación 2027, release notes y tareas del autor |
| docs/*.md (raíz de docs), docs/fallidas/ | HISTÓRICO | v1: decisiones, revisiones F1-F7, literatura, fuentes fallidas |
| docs/MAPA.md | VIGENTE | Este fichero |

## historico/
Documentos y salidas superadas que ningún script, regla del Makefile, test ni plantilla lee o escribe, movidos con `git mv` y sin modificar. Incluyen las síntesis de v3 y v4 (antes en archive/) y los planes, estados, revisiones, auditorías y arbitrajes de v1-v6.2 (trasladados en v7.1). Índice por versión en [historico/INDICE.md](../historico/INDICE.md).

## tests/
Tests de pytest (`make check`): utilidades v2, evaluaciones selladas en modo de ensayo y control de texto.
