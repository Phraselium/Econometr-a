# V14 · Árbol limpio de la versión 1.0 (repositorio vivienda-espana-evidencia)

`make arbol_publico DEST=../vivienda-espana-evidencia` (src/v14/arbol_publico.py) copia el árbol y crea un repositorio git nuevo con un único commit, «Versión 1.0».
- La procedencia queda escrita en el README: repositorio de desarrollo, commit de origen (hash) y DOI pendiente.
- La lista de lo excluido y lo redactado, fichero a fichero, va en el propio árbol: docs/v14/excluidos_arbol.csv.
- Econometr-a queda archivado como historia de desarrollo; su historia no se reescribe.

## Qué entra

Entra todo lo versionado en Econometr-a, salvo las exclusiones de la tabla siguiente.

| Entra | Por qué |
|---|---|
| src/, tests/, Makefile, requirements.lock, requirements-web.txt, ruff.toml, .github/ | Código, pruebas y despliegue de la web. Sin ellos no se reproduce nada |
| proyecto.json, CITATION.cff, .zenodo.json, LICENSE | Versión, URL, DOI y licencias, con una fuente única |
| README.md, LEEME_PRIMERO.md, README_REPLICACION.md, CHANGELOG.md, ERRATA.md, DECLARACION_IA.md, CLAUDE.md, llms.txt | Puertas de entrada y registro de cambios y erratas |
| publicacion/, metodologia/, reproducir/, consulta/ | Lo publicado. `make publicacion` y `make consulta` lo regeneran y los tests lo comparan |
| figuras/, web/ (fuentes), paper/ | Figuras con ficha, web estática y manuscrito |
| docs/ completo (3,6 MB) | Los scripts y tests leen plantillas, pre-registros, decisiones, manifiestos e inventarios de docs/. Separar lo «imprescindible» rompería `make all` y los tests |
| output/ (89 MB) | Salidas versionadas: `make publicacion` copia de ahí y los tests las comparan. Incluye las evaluaciones selladas ya hechas (`make all` no reabre el sellado). Las 16 tablas con columnas de Notariado, Registradores o AEAT van **redactadas**, sin esas columnas |
| data/CHECKSUMS.sha256 y los manifiestos data/raw/**/_manifest*.csv | URL, edición, fecha, licencia y sha256 de cada fichero de datos. Con ellos `make datos` y `make datos_terceros` verifican lo que descargan |
| revision_externa/ | Paquete para la revisión externa (bloque 3) |
| historico/INDICE.md (nuevo) | Sustituye a historico/: enlaza al repositorio de desarrollo y al commit de origen |

## Qué no entra y por qué

| No entra | Ficheros | Por qué | Cómo se obtiene |
|---|---|---|---|
| data/ (salvo manifiestos y checksums) | 719 | No se versionan datos en el repositorio público: la historia de git no se puede retirar y Zenodo es el archivo con DOI | `make datos`: descarga el paquete de Zenodo (DOI y URL en proyecto.json) o usa el paquete copiado en `_descarga/`, y verifica cada sha256 |
| data/raw de terceros no redistribuibles (Notariado, Registradores, CGPJ, Interior, Incasòl, Registre de Turisme, Comunidad de Madrid, Jarociński-Karadi, AEAT) | dentro de los 719 | Licencia no verificada o no abierta (docs/v8_1/datos_retirados.md; D4) | `make datos_terceros` (con red) y docs/v11/descargas_manuales.md |
| data/sealed | — | Muestra sellada: solo vía src/holdout.py; nunca se publica | `make clean` la reconstruye (solo por orden del autor) |
| Derivados con series de Notariado o Registradores (data/processed/nacional_q, panel_ccaa_a, v2/train/nacional_q_v2, v8/nacional_q_v8, v8/cv_prov_q_v8) | dentro de los 719 | Contienen series de esas fuentes (D5) | `make datos_terceros` y reconstrucción de paneles |
| Columnas de Notariado, Registradores o AEAT de 16 tablas de output/ (también .csv.gz desde V14.1) | 16 tablas redactadas | Ídem (D5, D4). Se quita la columna y no la tabla, para que no se rompa ningún enlace publicado | `make all` tras `make datos_terceros` |
| historico/ | 76 | Documentos de versiones superadas; ningún script los necesita | Repositorio de desarrollo archivado, en el commit de origen (historico/INDICE.md) |
| .claude/ | 19 | Configuración de los agentes de trabajo de la sesión de desarrollo | — |

No queda ninguna serie de Notariado ni de Registradores: ni por cabeceras ni por valores de muestra (decisiones.md, E3).

## Datos en el repositorio nuevo: `make datos`
- Se leen de proyecto.json `doi` y `zenodo_url_paquete`. Mientras sean «PENDIENTE» y no haya paquete en `_descarga/`, falla con un mensaje claro.
- Solo copia ficheros de data/ y verifica su sha256 contra CHECKSUMS.sha256 del paquete.
- Nunca sobrescribe un fichero versionado.
- No lee nada fuera del repositorio.

## Comprobación en el árbol generado (V14.1, 2026-10-16)
**Árbol final:** generado con `make arbol_publico` desde el commit de origen exacto `6d86b2a1f71d084af1d54b734ac09001a446de22` (6d86b2a). En el repositorio nuevo hay un único commit, c4ac604 «Versión 1.0». La prueba se hizo sin red y con el paquete de `make paquete_zenodo` copiado a mano en `_descarga/`.
- **`make datos`:** 705 ficheros copiados, 50 ya presentes (los manifiestos) y 0 problemas.
- **`make check`:**
  - pytest: **318 tests pasados y 59 omitidos** por faltar datos de terceros. Coinciden con docs/v14/tests_arbol.json, que es lo que publica el README; tests/conftest.py lo comprueba.
  - ruff, check_texto, check_v5, v6, v8, v9 y v13: sin errores. check_v14: sin heredocs sin comillas.
  - **Un único error, por diseño:** `hash_sellado` sigue PENDIENTE. En el árbol público es obligatorio y lo calcula el autor (tareas_autor.md, paso 0 bis). Con el hash escrito, `make check` pasa entero.
  - Git queda sin cambios tras el check (comprobado con `git status` y src/v12/git_limpio.py).
- **`make publicacion`:** sin cambios.
- **Recuento:** `pytest tests --junitxml` en un árbol de arranque (generado desde 56d7192 con `--sin-recuento`) escribió docs/v14/tests_arbol.json con src/v14/tests_arbol.py: 318 pasados, 59 omitidos, 0 fallos, 0 errores. El árbol final da los mismos números.
- **Limitación** documentada en reproducir/instrucciones.md («Árbol público»): sin `make datos_terceros`, los tests que leen datos de terceros se marcan como omitidos, con su motivo, y solo si fallan por la falta de uno de esos ficheros (tests/conftest.py).

## Tamaño
- Repositorio git (pack, lo que descarga un clon y cuenta GitHub): **46,14 MiB** en el árbol final (origen 6d86b2a). Cumple el objetivo de menos de 100 MB.
- Árbol de trabajo sin datos: 125,2 MB en 3.000 ficheros. El 71 % es output/ (89 MB). Las salidas de texto se comprimen bien en git.
- Con `make datos`, data/ añade unos 1.200 MB en el disco local; no entran en git.

Los 20 ficheros mayores:

| # | Fichero | MB |
|---|---|---|
| 1 | output/v8/M7/registro.csv | 11,8 |
| 2 | output/v8/M7/especificaciones.csv | 7,0 |
| 3 | data/raw/_manifest_series_ine_v2.csv | 4,1 |
| 4 | output/v12/b5/titularidad_cuotas.csv | 2,5 |
| 5 | output/v7/R2/montecarlo_r3_replicas.csv.gz | 2,0 |
| 6 | output/v6/M3A/predicciones_cv_ml.csv.gz | 2,0 |
| 7 | figuras/web/F19_mapa_cv_obra_hogares.svg | 1,7 |
| 8 | figuras/web/F07_mapa_cv_alquiler.svg | 1,7 |
| 9 | output/v6/M2/registro_bh.csv | 1,5 |
| 10 | output/v6/M2/registro.csv | 1,4 |
| 11 | output/v10/atlas/a_quien_ecv.csv | 1,3 |
| 12 | output/v12/b1/contabilidad_anual_municipio.csv.gz | 1,3 |
| 13 | output/registro_busqueda_f2.csv | 1,1 |
| 14 | output/registro_busqueda.csv | 1,1 |
| 15 | output/v3/C1/centroides.csv | 1,1 |
| 16 | output/v6_1/K4C/cifras_entregables.csv | 1,1 |
| 17 | consulta/hallazgos.json | 1,0 |
| 18 | output/f2/real_busqueda_coefs.csv | 0,9 |
| 19 | output/v12/b1/contabilidad_periodos_municipio.csv.gz | 0,9 |
| 20 | output/f2/busqueda_coefs.csv | 0,8 |

## Datos personales y rutas locales
- `arbol_publico` rechaza el árbol si encuentra cualquiera de estos patrones: rutas locales (directorios temporales de la sesión, del usuario o de root), enlaces de sesión, correos (salvo noreply@anthropic.com) o tokens (ghp_, github_pat_, sk-, AKIA, xox*).
- Se encontró y se corrigió en origen una ruta local de la sesión en src/v10/fetch_geo.py: ahora es una variable de entorno opcional.
- El commit «Versión 1.0» lleva la identidad de git configurada en la máquina que lo genera. El autor puede reescribirla antes de subir con `git commit --amend --reset-author` (tareas_autor.md, punto 2).
