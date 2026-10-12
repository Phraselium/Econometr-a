# Auditoría del repositorio para su publicación (v6, módulo G)

Fecha: 11 de octubre de 2026. Alcance: árbol de trabajo de la rama de la sesión (y, para credenciales, todo el historial git). Sin commit: los cambios quedan en el árbol para que el orquestador los revise.

## Resumen
| # | Comprobación | Resultado | Acción |
|---|---|---|---|
| 1 | Ficheros >50 MB | CUMPLE | Ninguna |
| 2 | Rutas locales absolutas | CUMPLE tras corregir 6 documentos; 1 excepción interna anotada | Corregido |
| 3 | Credenciales, tokens y claves | CUMPLE | Ninguna |
| 4 | Datos personales | CUMPLE | Decisiones del autor anotadas |
| 5 | Ficheros huérfanos en src/ | 2 scripts de modelo añadidos al Makefile; 3 de datos pendientes | Parcial |
| 6 | Scripts de modelo en el Makefile | CUMPLE tras el punto 5 | Corregido |
| 7 | Coherencia CITATION, LICENSE, .zenodo.json, licencias_datos | CUMPLE tras pasar a 5.1 | Corregido |
| 8 | CHANGELOG y ERRATA al día | CUMPLE | Entrada «v6 (en curso)» añadida |
| 9 | archive/ | 5 ficheros trasladados; 2 se quedan | Hecho |
| 10 | `make -n all` | Todos los ficheros referenciados existen | Ninguna |
| 11 | `make check` | Véase el final | — |

## 1. Ficheros de más de 50 MB
`find . -size +50M -not -path './.git/*'` encuentra 13 ficheros. Los 13 están ignorados (`git check-ignore`), ninguno está versionado y todos tienen su línea en data/CHECKSUMS.sha256; `sha256sum -c data/CHECKSUMS.sha256` da OK en las 14 líneas. Ningún fichero versionado supera 50 MB. No hay LFS (.gitattributes no existe) ni hace falta.

| Fichero | MB |
|---|---|
| data/raw/pdf/serpavi_v2_municipios.csv | 96 |
| data/raw/v3_orig/gis/ (7 JSON del Atlas de renta) | 51-72 |
| data/raw/pdf/originales/serpavi_bd_2011-2024.xlsx | 68 |
| data/raw/gva_vut_municipio.csv | 64 |
| data/raw/v3/cartografia/Cartografia_secc.zip | 62 |
| data/raw/catastro_urbana_municipios.csv | 57 |
| data/raw/gva_orig/vut_historico_2025.csv | 51 |

## 2. Rutas locales absolutas
Búsqueda de `/home/`, `/tmp/`, `/root/`, `/Users/` y `C:\` en todos los ficheros versionados salvo data/raw. Sin coincidencias en src/, tests/, output/, Makefile ni en los documentos de la raíz.

Corregidas (texto sustituido por una ruta relativa o una descripción):
- docs/v2/revision_BA.md, revision_BP.md, revision_BV.md: `/home/user/wt-*` → `../wt-*`; «Clon local de /home/user/Econometr-a» → «Clon local del repositorio».
- docs/v5/instrucciones_subagentes.md y docs/v5_1/instrucciones_subagentes.md: «Proyecto: /home/user/Econometr-a» → «Proyecto: raíz del repositorio (Econometr-a)».
- docs/fallidas/ive.md: `/root/.ccr/README.md` → «el README del proxy de la sesión».

Excepción anotada (documento interno en uso): docs/v6/instrucciones_subagentes.md conserva `/home/user/Econometr-a` porque es la instrucción vigente para los subagentes de v6. Propuesta: sustituirla al cerrar v6. Los prompts de los agentes pueden citar el scratchpad de la sesión (`/tmp/claude-0/...`); no aparece en ningún fichero versionado.

## 3. Credenciales
Árbol de trabajo: grep de `api_key`, `token=`, `password`, `secret_`, `client_secret`, `access_token`, `Authorization:`, `ghp_`, `github_pat_`, `sk-`, `AKIA`. Solo hay falsos positivos («Secretaría de Estado», «secreto estadístico»). Historial completo (`git log --all -p`, sin data/): ninguna coincidencia de `ghp_`, `github_pat_`, `sk-`, `AKIA`, `xox[bp]-` ni cabeceras de clave privada. Pendiente del autor: pasar un escáner dedicado antes de abrir el repositorio (docs/v6/tareas_autor.md §7).

## 4. Datos personales
- Correo del autor: no aparece en ningún fichero versionado. Decidir si se añade como contacto en CITATION.cff o README.md (tareas del autor §2).
- Correos de terceros: ninguno (grep de patrones de correo en todo el árbol salvo data/raw y requirements.lock).
- Teléfonos o DNI: ninguno (las coincidencias numéricas son fórmulas de output/registro_busqueda.csv).
- Nombres de terceros: no hay nombres de cargos ni de personas en docs/ ni en output/ fuera de las referencias bibliográficas; `check_texto.py` controla los entregables. Los programas electorales versionados (data/raw/v5/programas) son documentos oficiales publicados; su redistribución está pendiente de confirmar (docs/v5/licencias_datos.md).
- Autoría de los commits: los 332 commits figuran con el correo noreply@anthropic.com. Decisión del autor (tareas del autor §7).

## 5 y 6. Ficheros huérfanos y scripts de modelo
Método: scripts de src/ que no aparecen en `make -n all` ni en `make check` y que ningún otro script importa o carga (import, `spec_from_file_location`, glob de `e_hechos_*.py`, lista de módulos en `r1b_run.py`). Se excluyen `fetch_*`, `*_fetch.py` y `extract_*`.

| Script | Tipo | Situación | Acción |
|---|---|---|---|
| src/v5/b3_potencia.py | Modelo (potencia previa del pre-registro de B3); escribe output/v5/B3/tablas/potencia_emd.csv, que lee e_hechos_e2.py | Fuera del Makefile | **Añadido a `V5_ORDEN` antes de b3_run.** Ejecutado aislado: reproduce los ficheros versionados byte a byte (git status limpio) |
| src/v5/a5_validacion.py | Modelo (validación de precisión del diccionario A5); escribe validacion_precision.json, que lee a5_hechos.py | Fuera del Makefile | **Añadido a `V5_ORDEN` entre a5_run y a5_hechos.** Misma prueba: sin cambios en output |
| src/build_eventos.py | Datos (descarga del BOE; escribe data/raw/v2_eventos_politica.csv y v2_zonas_tensionadas.csv) | Fuera de `make data`; salidas versionadas | Pendiente: renombrar a `fetch_*` o documentar en README_REPLICACION §2 |
| src/v3/build_zonas_eventos_v3.py | Datos (copia y fechas BOE para data/raw/v3) | Igual | Pendiente, misma propuesta |
| src/v3/pa_fetch_aux.py | Descarga INE (data/raw/v3/pa_aux) | Igual; el nombre no sigue el patrón `*_fetch.py` | Pendiente, misma propuesta |

No se renombraron los tres scripts de datos porque `make data` ejecuta todo `src/fetch_*.py` y el cambio alteraría esa etapa (con red y FORCE). README_REPLICACION.md §2 recoge ahora a5_validacion, b3_potencia y los cuatro scripts de v5.1.

## 7. Coherencia de licencias y cita
- LICENSE: MIT (código) y CC BY 4.0 (textos, tablas y figuras); datos de terceros remiten a docs/v5/licencias_datos.md. Coincide con CITATION.cff (`MIT`, `CC-BY-4.0`), con la nota de .zenodo.json y con README.md y README_REPLICACION.md.
- .zenodo.json declara solo `"license": "MIT"` porque Zenodo admite una licencia por depósito; la licencia de los textos va en `notes`. Se deja así.
- Versión: CITATION.cff, .zenodo.json y README_REPLICACION.md decían 5.0; pasan a 5.1 (fecha 2026-10-11, la de la entrada v5.1 de CHANGELOG). DOI: pendiente en todos.
- licencias_datos.md: sin cambios; mantiene como pendientes Notariado, Registradores, CGPJ, AEAT y la copia de los programas.

## 8. CHANGELOG y ERRATA
CHANGELOG tenía la entrada v5.1; se añade «v6 (en curso)» con esta auditoría. ERRATA incluye la corrección de la ventana censal de B1 hecha en T1 de v5.1; no hay erratas nuevas.

## 9. archive/
Criterio: grep de la ruta y del nombre en src/, tests/, Makefile y docs/v5/plantillas sin coincidencias. Trasladados con `git mv`: output/v3/{articulo, informe_politica, lo_que_sabemos}.md y output/v4/{policy_brief, working_paper}.md. **No** se trasladan output/v4/informe_tecnico.md ni output/v4/lo_que_sabemos.md, porque las plantillas de v5 los citan por ruta. Quedan output/v3/README.md y output/v4/README.md con enlaces; el registro está en archive/README.md. README_REPLICACION.md (§4 y §5) apunta a las rutas nuevas. Los documentos de planificación de v3 y v4 (docs/v3/plan.md, docs/v4/plan.md, revisiones) conservan las rutas originales como registro histórico.

Efecto en `make check`: check_texto.py ya no escanea los cinco ficheros trasladados.

## 10 y 11. Comprobaciones finales
- `make -n all`: los 80 scripts referenciados existen (incluidos `src/v5/../v5_1/t*_run.py`).
- `make check`: pasa (ruff sin avisos; pytest 36 tests superados; check_texto, check_v5 y check_v6 con 0 errores).
