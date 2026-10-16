# V13-A · Coherencia de las puertas de entrada

Inventario del 2026-10-16, sobre el commit a58b426 (antes de V13). Busca menciones a «versión de referencia», «vigente», «versión de consulta», «**Versión:**» y números de versión en las puertas de entrada: README.md, LEEME_PRIMERO.md, CLAUDE.md, llms.txt, consulta/, publicacion/, metodologia/, reproducir/, web/, historico/INDICE.md, CITATION.cff y .zenodo.json.

Lo mismo lo hace ahora, en cada `make check`, src/v13/check_v13.py.

## 1. Qué declaraba cada puerta

| Puerta | Qué decía (antes de V13) | Discrepancia |
|---|---|---|
| CLAUDE.md (cabecera) | «V8.1 … v8 referencia (v7.2 anterior); trabajo en docs/v8_1» | describe V8.1; no recoge V9-V12 |
| README.md | «**Versión:** v8.1 … v8 es la versión de referencia de modelización»; «## Versión vigente: v8»; cita «(versión 7.2)» | tres versiones distintas en la misma página |
| LEEME_PRIMERO.md | «Versión de referencia: **v8** (publicada como v8.1)»; déficit «v7.1 con las correcciones de v7.2» | v8 frente a v8.1 del README |
| CITATION.cff | `version: "8.1"`, `date-released: "2026-10-14"`, título «(v8.1)» | sin V9-V12 |
| .zenodo.json | `"version": "8.1"`, título «(v8.1)» | igual |
| llms.txt | «Versión de consulta 8.1» | igual |
| consulta/LEEME_ASISTENTE.md | «Versión de consulta: **8.1**»; V8 referencia de modelización; v7.1-v7.2 referencia del déficit | sin V9 ni V12 |
| consulta/version.json, hallazgos.json | `"version": "8.1"` | igual |
| README_REPLICACION.md → reproducir/instrucciones.md | título «(v1-v7.1)»; «**Versión:** 7.2, versión de referencia (v7.1 con correcciones)»; «### Versión de referencia v7.1» | 7.2 y 7.1 frente a 8.1 |
| reproducir/evaluacion_2027.md | «en la versión de referencia (v7.1)» | 7.1 |
| metodologia/guia_revisor.md | título «(versión de referencia v7.2)»; «**Versión:** v7.1, versión de referencia» | 7.2 y 7.1 en el mismo documento |
| publicacion/una_pagina.md | título «(versión de referencia v8)»; «Qué añade la versión de referencia v7.2»; «… v8» | 8 y 7.2 |
| publicacion/lo_que_sabemos.md | título «(versión de referencia v8)»; apartados «versión de referencia v7.2» y «v8» | 8 y 7.2 |
| publicacion/que_cambio.md | título «(versión de referencia v8)»; «Solo es citable la versión de referencia: hoy, la v7.1» | 8 frente a 7.1 en el mismo párrafo inicial |
| publicacion/policy_brief.md | título «(policy brief, versión de referencia v7.2)» | 7.2 |
| publicacion/informe_tecnico.md | título «(versión de referencia v7.2)»; «**Versión:** `5.0`» | 7.2 y 5.0 |
| publicacion/working_paper.md | «versión de referencia `7.2`, 12 de octubre de 2026» | 7.2 |
| publicacion/ponencia (diapositivas, guion) | «versión de referencia v7.2»; «Versión de referencia v7.1» | 7.2 y 7.1 |
| historico/INDICE.md | «La versión de referencia es la **v7.1**» | 7.1 |
| web/ (plantillas) | «Versión {{ version.version }}» leído de consulta/version.json | 8.1 (heredado de consulta) |

En total, la búsqueda automática encontró **35** declaraciones discrepantes en publicacion/, metodologia/, reproducir/, consulta/ y llms.txt, más las de las puertas escritas a mano: README, CLAUDE.md, CITATION.cff y .zenodo.json. La lista completa la reproduce `python3 -c "from src.v13 import check_v13 as c; print(c.version_unica())"` sobre el commit a58b426.

## 2. Corrección

Esquema: versión pública **1.0** (16-10-2026). v1-V12 pasan a versiones internas (tabla en CHANGELOG.md). Para cada tema vale una versión interna:

| Tema | Versión interna vigente |
|---|---|
| Déficit y necesidad de vivienda, simulaciones de instrumentos y atlas regional | v7.1 con las correcciones de v7.2 |
| Por qué ha subido | V8 (redacción y tablas de v8.1) |
| Qué causa qué | V9 |
| Atlas descriptivo, base y web | V10 (base ampliada en V11 y V12) |
| Demografía, hogares, titularidad y oferta | V12 (datos de V11) |

Cómo se corrigió cada puerta:
- **Puertas generadas** (publicacion/, metodologia/, reproducir/, consulta/, llms.txt, web): se corrigieron solo sus fuentes.
  - Las plantillas de docs/v5/plantillas leen la versión con `{{proyecto.version_publica}}`.
  - docs/v7_1/guia_revisor.md y docs/v7_1/evaluacion_2027.md se corrigieron a mano.
  - src/consulta/generar.py y src/v10/web.py leen proyecto.json.
  - Después se regeneraron con `make publicacion`, `make consulta` y `make web`.
- **Puertas a mano** (README, LEEME_PRIMERO, CLAUDE.md, README_REPLICACION, historico/INDICE): se reescribieron sus cabeceras.
- **CITATION.cff y .zenodo.json**: se generan desde proyecto.json (`make metadatos`).
- **Versiones por tema**: dentro de los entregables, «versión de referencia vX» pasa a «versión interna vX». La expresión «versión pública / de referencia / vigente / de consulta N» queda reservada a la 1.0.

## 3. URL del repositorio

La URL configurada es https://github.com/Phraselium/vivienda-espana-evidencia (proyecto.json, campo `repositorio`). La web está en https://phraselium.github.io/vivienda-espana-evidencia/ (campo `web`). El nombre actual del remoto es Phraselium/Econometr-a; el renombrado lo hace el autor (docs/v13/tareas_autor.md, punto 1).

**Discrepancia con el recuento del encargo.** El encargo habla de 17 apariciones. La búsqueda encuentra **19** URL `https://github.com/Phraselium/…` en los ficheros versionados, sin contar data/ ni historico/. Hay además 2 enlaces de texto sin protocolo y 8 URL de la web. Todas usan ya el nombre nuevo; ninguna usa Phraselium/Econometr-a. Lo que faltaba era un sitio único del que leerlas.

| # | Fichero | Apariciones | Tipo | Corrección |
|---|---|---|---|---|
| 1-2 | CITATION.cff | 2 (repository-code, url) | metadato | generado desde proyecto.json |
| 3 | README.md | 1 | puerta a mano | conservada; la comprueba check_v13 |
| 4 | LEEME_PRIMERO.md | 1 | puerta a mano | conservada; la comprueba check_v13 |
| 5 | README_REPLICACION.md | 1 (git clone) | puerta a mano | conservada; la comprueba check_v13 |
| 6 | reproducir/instrucciones.md | 1 | copia de README_REPLICACION | `make publicacion` |
| 7 | consulta/LEEME_ASISTENTE.md | 1 | generado | src/consulta/generar.py lee proyecto.json |
| 8 | consulta/version.json | 1 | generado | ídem |
| 9 | llms.txt | 1 | generado | ídem |
| 10 | src/consulta/generar.py | 2 (constante y texto de llms) | fuente | `REPOSITORIO = PROYECTO["repositorio"]` |
| 11-12 | src/v10/web.py | 2 (constante y enlace al pre-registro V9) | fuente | `REPO` desde proyecto.json; el enlace usa `{{ repo }}` |
| 13 | docs/v5/plantillas/articulo_colegio.md | 1 (+1 texto) | plantilla | `{{proyecto.repositorio}}` |
| 14 | docs/v5/plantillas/ponencia/diapositivas.md | 1 | plantilla | `{{proyecto.repositorio}}` |
| 15 | output/v5/articulo_colegio.md | 1 (+1 texto) | render | `src/v5/render.py` |
| 16 | output/v5/ponencia/diapositivas.md | 1 | render | ídem |
| 17 | publicacion/articulo_colegio.md | 1 (+1 texto) | copia | `make publicacion` |
| 18 | publicacion/ponencia/diapositivas.md | 1 | copia | ídem |
| — | web: README.md, consulta/version.json, web/README.md, docs/v10/decisiones.md, docs/v10/tareas_autor.md, output/v10/web_resumen.csv, src/consulta/generar.py, src/v10/web.py | 8 (phraselium.github.io) | varias | las de código leen proyecto.json; el resto, comprobadas por check_v13 |

Menciones del nombre antiguo que no son URL y se conservan, porque describen la historia o son rutas locales:
- README.md, «antes Phraselium/Econometr-a»;
- docs/v8_1/publicacion_github.sh, variable NOMBRE_ANTIGUO, necesaria para renombrar;
- src/v8/f6_tablas.py, metadato del Excel V8 (cambiarlo alteraría un binario congelado);
- docs/v5/instrucciones_subagentes.md, nombre del directorio de trabajo.

## 4. Control en `make check`

src/v13/check_v13.py falla si:
1. una puerta de entrada declara una versión pública, de referencia, vigente o de consulta distinta de proyecto.json;
2. una puerta principal no declara la versión pública;
3. el campo `version` de CITATION.cff, .zenodo.json o consulta/*.json no coincide;
4. aparece una URL github.com/Phraselium/… o phraselium.github.io/… distinta de la configurada en cualquier fichero de texto versionado;
5. CITATION.cff o .zenodo.json no son los que genera `make metadatos`;
6. cambia, desaparece o se añade una cifra de cifras_clave sin ERRATA. Las huellas están en docs/v13/cifras_base_v12.csv, con el mismo criterio que check_v9.
