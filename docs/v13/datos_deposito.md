# V13-B · Datos fuera de git y depósito en Zenodo

Medición del 2026-10-16 sobre el árbol de trabajo de esta sesión (commit 3aa4645).
- La clasificación por fichero la hace src/v13/inventario_datos.py.
- Los ficheros versionados están en [datos_inventario.csv](datos_inventario.csv), con fuente, licencia y motivo. Es determinista: sale igual en cualquier clon.
- La lista completa del disco se obtiene con la opción `--todo <ruta>` del mismo script.

## 1. Cuánto ocupa data/

| Carpeta | En disco | Versionado en git |
|---|---|---|
| data/raw | 11 GB | 1.072 MB |
| data/base | 572 MB | 96,5 MB (sin la base completa hechos.parquet, > 50 MB) |
| data/manual | 67 MB | 0 (ignorado; originales de las descargas manuales del autor) |
| data/sealed | 40 MB (tamaño del directorio; no se lee su contenido) | 0 (ignorado; solo vía src/holdout.py) |
| data/processed | 33 MB | 34,5 MB |
| data/cache | 8,7 MB | 9,1 MB |
| data/CHECKSUMS.sha256 | 12 KB | sí |
| **Total** | **≈ 12 GB** | **1.212 MB** |

## 2. Clases

- **(a) Redistribuible por licencia y versionado.** Entra en el paquete de Zenodo.
- **(b) No redistribuible.** No entra en el paquete. Incluye:
  - licencias no verificadas o no abiertas;
  - microdatos con celdas pequeñas;
  - derivados que contienen series de Notariado, Registradores, AEAT o CGPJ;
  - la base completa (la parte difundible es la capa pública);
  - discrepancias de licencia.
- **(c) Redistribuible pero no versionado.** Originales y microdatos grandes. No entra en el paquete: se regenera con su descarga.

| Clase | Ficheros | MB en disco | Versionados | MB versionados |
|---|---|---|---|---|
| (a) | 756 | 1.199,6 | 756 | 1.199,6 |
| (b) | 3.985 | 770,1 | 14 | 12,7 |
| (c) | 2.082 | 9.926,0 | 0 | 0,0 |

Casi todos los ficheros (b) son páginas HTML temporales de la descarga de la AEAT, que no se versionan. Por carpeta y clase (fuente y licencia: las más frecuentes del grupo; el detalle por fichero está en el CSV):

| Carpeta | Clase | Ficheros | MB | Versionados | Fuente principal | Licencia |
|---|---|---|---|---|---|---|
| data/CHECKSUMS.sha256 | (a) | 1 | 0,0 | 1 | elaboración propia (metadatos) | CC BY 4.0 |
| data/base | (a) | 19 | 95,7 | 19 | elaboración propia (capa pública y geometrías) | CC BY 4.0 (elaboración propia) + licencia de sus fuentes |
| data/base | (b) | 8 | 504,0 | 6 | elaboración propia (base completa) | incluye variables no redistribuibles |
| data/cache | (b) | 2 | 9,1 | 2 | INE (microdatos EVR/EMCR) | INE; no difundible por secreto estadístico |
| data/manual | (b) | 35 | 70,1 | 0 | descargas manuales del autor | Ajuntament de Barcelona: CC BY 4.0; Generalitat Valenciana: CC BY 4.0 |
| data/processed | (a) | 19 | 33,1 | 19 | elaboración propia (derivado de data/raw) | CC BY 4.0 + licencia de sus fuentes |
| data/processed | (b) | 5 | 1,4 | 5 | elaboración propia (incluye series de terceros) | mixta: la de su fuente más restrictiva |
| data/raw (raíz) | (a) | 87 | 372,2 | 87 | INE; Eurostat; MIVAU | permitida (docs/v5/licencias_datos.md); CC BY 4.0 |
| data/raw (raíz) | (c) | 3 | 126,5 | 0 | Catastro; Generalitat Valenciana | Catastro: reutilización con reconocimiento; CC BY 4.0 |
| data/raw/gva_orig | (a) | 18 | 24,3 | 18 | Generalitat Valenciana | permitida |
| data/raw/gva_orig | (c) | 3 | 96,8 | 0 | Generalitat Valenciana (registro VUT) | CC BY 4.0 |
| data/raw/ine_padron_pcaxis | (a) | 45 | 84,0 | 45 | INE | permitida |
| data/raw/mivau_xls | (a) | 11 | 14,9 | 11 | MIVAU | permitida |
| data/raw/pdf | (a) | 8 | 42,6 | 8 | MIVAU (SERPAVI) | permitida |
| data/raw/pdf | (b) | 51 | 75,5 | 0 | Notariado; Registradores | condiciones de reutilización no verificadas |
| data/raw/pdf | (c) | 2 | 171,2 | 0 | MIVAU | MIVAU: reutilización con cita (Ley 37/2007) |
| data/raw/v10 | (a) | 15 | 1,2 | 15 | INE, MIVAU, Eurostat, BdE y GVA (monitor) | reutilización con cita de cada organismo |
| data/raw/v10 | (c) | 1 | 60,3 | 0 | INE (seccionado 2025) | INE (Ley 37/2007) |
| data/raw/v11 | (a) | 137 | 87,0 | 137 | INE (censo 2021, EMCR…); Ajuntament de València | INE: reutilización con cita; CC BY 4.0 |
| data/raw/v11 | (b) | 3.854 | 94,4 | 1 | AEAT (IRPF por municipios); Universitat de València; Euskadi | discrepancia (AEAT); sin licencia abierta declarada |
| data/raw/v11 | (c) | 1.850 | 7.311,4 | 0 | INE (móviles, microdatos de censos); Catastro | INE; Catastro |
| data/raw/v2_orig | (a) | 16 | 22,0 | 16 | MIVAU; Catastro | permitida |
| data/raw/v2_orig | (c) | 9 | 36,4 | 0 | Catastro (URBANA) | Catastro: reutilización con reconocimiento |
| data/raw/v3 | (a) | 55 | 195,8 | 55 | Banco de España; INE; BOE | permitida |
| data/raw/v3 | (b) | 2 | 0,1 | 0 | Registre de Turisme; Comunidad de Madrid | licencia no verificada |
| data/raw/v3 | (c) | 1 | 64,4 | 0 | INE (seccionado censal) | INE (Ley 37/2007) |
| data/raw/v3_orig | (a) | 7 | 33,0 | 7 | INE; Eurostat | permitida |
| data/raw/v3_orig | (b) | 1 | 0,0 | 0 | Comunidad de Madrid | licencia no verificada |
| data/raw/v3_orig | (c) | 41 | 778,1 | 0 | INE (ADRH, censo anual, VUT por sección) | INE (Ley 37/2007) |
| data/raw/v4 | (a) | 5 | 3,9 | 5 | INE; Catastro | permitida |
| data/raw/v4 | (b) | 1 | 0,0 | 0 | transcripción del autor (programas electorales) | aplazado a la fase de propuestas (V8.1) |
| data/raw/v5 | (a) | 58 | 55,2 | 58 | Congreso; BOE; INE | permitida |
| data/raw/v5 | (b) | 20 | 10,1 | 0 | AEAT; CGPJ; Interior; programas electorales | reutilización no verificada en detalle |
| data/raw/v5_1 | (a) | 22 | 5,1 | 22 | MIVAU; INE | permitida |
| data/raw/v8 | (a) | 41 | 19,2 | 41 | Eurostat; INE | permitida; CC BY 4.0 |
| data/raw/v8 | (b) | 1 | 0,6 | 0 | Jarociński y Karadi (GitHub) | sin licencia verificada |
| data/raw/v9 | (a) | 191 | 110,6 | 191 | BOE (regulación); Inside Airbnb; INE | BOE: reutilización con cita; CC BY 4.0 |
| data/raw/v9 | (b) | 5 | 4,9 | 0 | Incasòl; Generalitat de Catalunya (Socrata) | «See Terms of Use» (no CC BY) |
| data/raw/v9 | (c) | 171 | 1.281,0 | 0 | INE (censo anual, microdatos); BCE | INE: reutilización con cita |
| data/raw/vlc_fuente | (a) | 1 | 0,0 | 1 | Ajuntament de València | permitida |

## 3. Hallazgos que el autor debe decidir

1. **AEAT, IRPF por municipios (V11): las dos fuentes de licencia discrepan.**
   - El manifiesto de data/raw/v11/aeat_irpf_municipios dice «redistribuible: sí» (Ley 37/2007).
   - docs/v5/licencias_datos.md y la retirada de V8.1 dicen «reutilización no verificada en detalle».
   - Como discrepan, se reportan las dos. El fichero se clasifica como (b).
   - Las 7 variables `aeat_irpf_*` de la capa pública se quitan del paquete (lista `EXCLUIR_PUBLICA` de src/v13/paquete_zenodo.py).
   - La base versionada no se toca. Es la decisión D4 de [decisiones.md](decisiones.md).
2. **Series de Notariado y Registradores en derivados versionados.**
   - Afecta a 5 paneles de data/processed: nacional_q, panel_ccaa_a, v2/train/nacional_q_v2, v8/nacional_q_v8 y v8/cv_prov_q_v8.
   - Afecta también a 20 tablas de output/.
   - Contienen series publicadas por esas fuentes, cuya reutilización no está verificada. V8.1 retiró los ficheros brutos, pero estos derivados siguen en git.
   - El paquete los excluye; `make all` los regenera después de `make datos_terceros`. Es la decisión D5.
3. **Muestra sellada.** data/sealed ni se incluye ni se recorre. La reconstruye `make clean` (src/holdout.py build). Las evaluaciones selladas ya hechas viajan en output/.

## 4. `make paquete_zenodo`

Genera `_deposito/vivienda-espana-evidencia-<versión>/`, un directorio ignorado por git. Con `python3 src/v13/paquete_zenodo.py --zip` genera también el zip. No borra nada del repositorio ni de su historia.

Contenido:
- **Código y documentación:** todo lo versionado fuera de data/ y output/, salvo .claude/ (código, tests, Makefile, docs, publicacion, metodologia, reproducir, consulta, figuras, web, paper, historico y metadatos).
- **Salidas:** output/ versionado, salvo las tablas con series de Notariado, Registradores o AEAT.
- **Datos:** data/ de clase (a), con data/base/publica y data/base/geo. hechos.parquet va sin las variables `aeat_*`.
- **Ficheros de control:**
  - `CHECKSUMS.sha256`: sha256 de cada fichero;
  - `LEEME_DEPOSITO.md`: qué contiene, qué no y cómo obtenerlo;
  - `EXCLUIDOS.csv`: cada fichero versionado excluido, con su motivo.

Ensayo del 2026-10-16: 3.760 ficheros incluidos, 34 versionados excluidos, 7 variables AEAT quitadas de la capa pública y 1.322 MB. La verificación de CHECKSUMS.sha256 con sha256sum fue correcta.

Cómo se obtiene lo excluido:
- **(b) de terceros:** `make datos_terceros` descarga y verifica, contra data/CHECKSUMS.sha256, los ficheros retirados en V8.1 (docs/v8_1/datos_retirados.md). Las descargas manuales del autor se describen en docs/v11/descargas_manuales.md.
- **(c):** con red, `make datos_v9`, `make datos_v11`, el script src/v10/fetch_geo.py y `make data`. Todos verifican contra sus manifiestos.
- **Derivados con series de terceros:** `make all` después de `make datos_terceros`.

## 5. `make datos_terceros` ya no reescribe ficheros versionados

Era la tarea 2 de docs/v12/tareas_autor.md. Los scripts de descarga reescribían tres ficheros versionados con la fecha de descarga y las filas de v4:
- data/raw/_manifest.csv;
- data/raw/v9/incasol/_manifest.csv;
- docs/v5/programas/inventario.csv.

Solución en src/v8_1/datos_terceros.py (`proteger_versionados`):
1. guarda esos ficheros antes de descargar;
2. copia la versión de la descarga en data/raw/_descargas_terceros/, que es un directorio ignorado;
3. restaura la versión versionada.

Prueba real (2026-10-16):
- se retiraron del disco tres ficheros: notariado_validacion.csv, programas/upn.pdf e incasol_qww9-bvhh_actual.csv.gz;
- `make datos_terceros` los descargó con red;
- incasol/_manifest.csv e inventario.csv quedaron intactos en git, y sus versiones nuevas, en el registro;
- 79/79 ficheros coinciden con data/CHECKSUMS.sha256 y git queda sin cambios.

El test está en tests/v13/test_v13.py.
