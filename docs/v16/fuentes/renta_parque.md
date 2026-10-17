# V16 · Fuentes de la familia renta_parque (fase 1)

Adquisidor: adquisidor-datos (V16, fase 1). Fecha de verificación: 2026-10-17.
Manifiesto: `data/raw/v16/renta_parque/_manifest.csv`. Scripts reproducibles: `data/raw/v16/renta_parque/_scripts/` (ejecutar con `python3 -I`).
Redistribuible: «sí» (cita obligatoria, reutilización permitida); «no» o «dudoso» van a `_terceros/` (no versionado).
Ficheros de más de 50 MB o de volumen agregado: `_grandes/` (ignorado en git); su sha256 está en el manifiesto.

## Estado por fuente

| # | Fuente | Estado | Ruta | Cobertura |
|---|---|---|---|---|
| 1 | INE ADRH (renta media/mediana, fuentes, Gini, P80/P20, umbrales, demografía) | parcial: 432 de 540 tablas; 108 bloqueadas por el API (fuente fallida) | `_grandes/adrh/` | municipio, 2015-2023; sección solo en servergis (2019-2023) |
| 2 | INE Censo 2021 (viviendas principales, no principales, vacías) | ya en el repositorio | `data/raw/v11/ine_censo2021/`, `data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz`, `data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv` | municipio (tablas 59515-59551), sección (indicadores, edición provisional) |
| 3 | INE viviendas vacías por consumo eléctrico | ya en el repositorio (Censo 2021); serie anual 2020-… no localizada | `data/raw/v11/ine_censo2021/censo2021_tpx59531.csv` | total nacional, CCAA, provincia y municipio; sin sección |
| 4 | INE EPF (microdatos gasto y hogar) | parcial: 2006 y módulo de bienestar descargados; 2007-2025 no localizados | `epf/` | 2006 (nacional) |
| 5 | INE ECV (microdatos) | completada: transversal 2004-2025 y longitudinal parcial | `ecv/` (+ `data/raw/v9/ine_microdatos/ecv/` para 2018-2025) | ver ficha ECV |
| 6 | Catastro estadísticas municipales (urbana) | 2026 descargada; resto ya en repositorio; descarga masiva alfanumérica → requiere al autor | `catastro/URBANA2026.xls` | municipio, 2011-2026 |
| 7 | Banco de España EFF | requiere al autor (solicitud BELab) | — | 2002-2022 (edición 2022 en BELab) |

## Ficha 1 · INE ADRH (Atlas de Distribución de Renta de los Hogares)

- **Endpoint verificado:** `https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/ADRH` (lista, 540 tablas) y `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<Id>?nult=20` (datos). La llamada sin `nult` devuelve cuerpo vacío; con `nult=20` responde en unos 9 s por tabla.
- **Edición:** las tablas de la API tienen fecha de última modificación 2025-10-21 (campo `Ultima_Modificacion` de la lista). La serie llega hasta 2023 en la respuesta; no se ha encontrado 2024 en la API.
- **Tablas:** nueve familias por código de territorio. Renta media y mediana, fuentes de ingresos, porcentaje bajo umbrales fijos y relativos (por sexo, edad y nacionalidad), Gini y P80/P20, indicadores demográficos. Códigos: `DIST-SECC-MUN` (529 tablas, por provincia), `NAC-CCAA-PROV` (10), `1976_DIST-SECC-MUN` (1).
- **Cobertura real (control en `_grandes/adrh/resumen_control.json`, script `resumen_adrh.py`):** 432 tablas, 6.766.362 series, 58,6 millones de puntos anuales. Años 2015-2023 con unos 6,3-6,7 millones de puntos por año. Los puntos con `Secreto: true` o sin valor suman 37,4 millones (64 %). La proporción tan alta de secretos hace que el uso de estas cifras a nivel municipal pequeño sea limitado; no se imputa nada.
- **Nivel territorial:** las series de las tablas `DIST-SECC-MUN` tienen nombre de municipio (p. ej., «Abengibre. Dato base. Renta neta media por persona», 3.090 series en la tabla 30656). No aparecen distrito ni sección en el nombre de la serie. El nivel sección queda en el servergis ya existente (`data/raw/v3/ine_v3_gis_seccion.csv.gz`, 2019-2023). Para la sección censal 2015-2018 no hay fuente en este lote.
- **Descarga:** 540 tablas listadas; 432 descargadas. Las 108 restantes devuelven `{"status": "No puede mostrarse por restricciones de volumen"}`, también con `nult=1` (ver fuentes fallidas). Esas respuestas de error se eliminaron del directorio de datos y del manifiesto. Lista en `_grandes/adrh/bloqueadas_volumen.txt`.
- **Licencia:** INE, reutilización con cita (Ley 37/2007); aviso legal https://www.ine.es/aviso_legal. Redistribuible: sí, con cita.
- **Sha256:** en el manifiesto, una fila por tabla.
- **Notas:** el ADRH ya existía en el repositorio en forma parcial (`data/raw/v3/ine_v3_gis_seccion.csv.gz`, servidor ArcGIS, 2019-2023 por sección). Se descarga la API oficial porque cubre la serie desde 2015 a nivel municipal, con 432 tablas útiles. La comparación con el servergis queda para el ingeniero de datos (normalización). Los valores secretos (`Secreto: true`) y los nulos se conservan sin imputar. Nada se ha interpolado.

## Ficha 2 · INE Censo 2021 (ya en el repositorio)

- Tablas tpx 59515-59551 en `data/raw/v11/ine_censo2021/` (nacional, CCAA, provincia, municipio, distrito, tipo de vivienda principal o no, tenencia, tamaño de hogar, año de construcción).
- Indicadores por sección (edición provisional de noviembre de 2021; `data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz`, con `t20_1` viviendas por sección).
- **Pendiente de comprobar:** la edición definitiva de los resultados por sección no se ha verificado. Las cifras de sección son provisionales según la cabecera de la fuente.
- Licencia: INE, reutilización con cita. Redistribuible: sí.

## Ficha 3 · INE viviendas vacías por consumo eléctrico

- Tabla `59531` (Censo 2021), «Viviendas por intensidad de uso a partir del consumo eléctrico»: 3.828.307 viviendas vacías y 2.517.628 de uso esporádico a nivel nacional. Es la misma definición de la estadística experimental (ausencia de contrato o consumo inferior al de una vivienda media ocupada 15 días al año). Ya en `data/raw/v11/ine_censo2021/censo2021_tpx59531.csv`, 58.626 filas, con desglose por municipio.
- **No localizada:** una serie anual de la estadística experimental 2020-… con desglose por sección o municipio distinto del censo. Una búsqueda no la confirmó. Queda pendiente de verificación en el portal del INE; no se ha intentado descargarla por scraping.
- Licencia: como el censo, reutilización con cita. Redistribuible: sí.

## Ficha 4 · INE EPF (Encuesta de Presupuestos Familiares)

- **Localizado y descargado:** `https://www.ine.es/ftp/microdatos/epf2006/datos_epf2006.zip` (microdatos 2006, 24,8 MB), `.../epf2006/disreg_epf.zip` (diseño de registro), `.../epf2006/Corresp_COICOP_2018_ECOICOP.xlsx` (equivalencias de clasificación), `https://www.ine.es/ftp/microdatos/epf_bienestar/datos_epf_bienestar.zip` y `.../disreg_epf_bienestar.zip` (módulo de bienestar).
- **No localizado:** microdatos EPF 2007-2015 (COICOP) y 2016-2025 (ECOICOP, 2024-2025 COICOP 2018). La página de la operación INE (`cid=1254736176806`) indica selector de año, pero los enlaces directos no aparecen en el HTML. Patrones probados sin éxito: `ftp/microdatos/epf<año>/datos_epf<año>.zip`, `epf<año>/datos_epf.zip`, `epf_<año>/`, `epfc/`, `epf_continua/`. Ver la ficha de fuentes fallidas.
- **Licencia:** INE, reutilización con cita de la fuente primaria. El pie de la página de la operación menciona CC BY-SA 4.0, pero el enlace apunta a CC BY 4.0. Se marca redistribuible «sí» conforme a la regla de los microdatos del INE, con la discrepancia anotada.
- **Ruta:** `data/raw/v16/renta_parque/epf/`.

## Ficha 5 · INE ECV (Encuesta de Condiciones de Vida)

- **Ya en el repositorio:** transversal 2018-2025 (`data/raw/v9/ine_microdatos/ecv/`, ZIP originales).
- **Descargado ahora:**
  - transversal 2013-2017 (`ecv_b2013/datos_<año>.zip`, en `ecv/`);
  - transversal 2004-2012 (`ecv_b2004/ecvb04_<año>.zip`, en `ecv/transversal_2004_2012/`);
  - longitudinal base 2004 (`ecv_b2004/periodo_<f>-<l>.zip`, 8 periodos, 2004-2012) y base 2013 (`ecv_b2013/periodo_<f>-<l>.zip`, periodos 2008-2011 a 2016-2019, 9 periodos), en `ecv/longitudinal/`.
- **No descargado (decisión pendiente del autor):** longitudinal base 2013 periodos 2017-2020 a 2022-2025. El volumen agregado es de unos 510 MB (los periodos 2019-2022 a 2022-2025 superan 75 MB cada uno). Se propone descargarlos en `_grandes/` si el autor lo aprueba.
- **Verificación:** todos los ZIP se listan con `zipfile` y su integridad se comprueba con `testzip()` (sin extraer). El resultado se anota en la columna `notas`.
- **Patrón de URL:** `https://www.ine.es/ftp/microdatos/ecv/...`, según el repositorio de referencia `mvazcar/ECV` (`config.py`), verificado por cabecera HTTP.
- **Licencia:** INE, microdatos anonimizados, reutilización con cita. Redistribuible: sí.

## Ficha 6 · Catastro (estadísticas catastrales municipales)

- **Ya en el repositorio:** `data/raw/catastro_urbana_municipios.csv(.gz)` (2011-2025, 228.130 filas) y `data/raw/v4/catastro_solares_municipios.csv.gz` (extracto de variables de solar, 2012-2026, 7.610 municipios). Las variables de construcción por año vienen de INSPIRE en `data/raw/v11/catastro_inspire/`.
- **Descargado ahora:** `https://www.catastro.hacienda.gob.es/documentos/estadisticas/URBANA2026.xls` (libro Excel, edición 2026, referencia 2026-01-01, 4.072.191 bytes). Cabecera OLE2 verificada.
- **Requiere al autor:** la descarga masiva alfanumérica de los datos no protegidos del Catastro exige registro con certificado electrónico. No se ha intentado. Paso exacto pendiente de confirmar en la sede: identificarse en la Sede Electrónica del Catastro (https://www.sedecatastro.gob.es/) con certificado electrónico, buscar la opción de descarga masiva de datos alfanuméricos y solicitar el acceso. Los ficheros se guardarían en `data/raw/v16/renta_parque/catastro/masivo/`. Ni el formulario ni las condiciones se han comprobado en esta sesión.
- **Licencia:** reutilización libre con reconocimiento de la fuente (inventario V15, `docs/v5/licencias_datos.md`). Redistribuible: sí.

## Ficha 7 · Banco de España EFF (Encuesta Financiera de las Familias)

- **Requiere al autor.** No se ha intentado descarga alguna.
- **Procedimiento:** los microdatos de la EFF (edición 2022 para uso científico) se ofrecen a través del laboratorio BELab del Banco de España, con acceso remoto. Según la información pública, el investigador envía su currículum vitae y un formulario de solicitud. Pasos: (1) consultar la sección «Bases de datos y otros recursos» y la de BELab en https://www.bde.es/wbe/es/areas-actuacion/analisis-e-investigacion/recursos/ ; (2) descargar el formulario vigente; (3) enviar el formulario y el currículum a la dirección indicada en esa página. El formulario y la dirección exacta no se han podido verificar en esta sesión.
- **Repositorio:** `data/raw/v3/eff_tenencia_edad_v3.csv` (tabla agregada derivada, ya existente) no sustituye a los microdatos.

## Fuentes fallidas

- **ADRH, 108 tablas bloqueadas por volumen.** Endpoint `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<Id>?nult=<n>`, con n = 1, 5, 10, 15 y 20. Respuesta: `{"status" : "No puede mostrarse por restricciones de volumen"}`. Edición de la lista: última modificación 2025-10-21. Fecha de verificación: 2026-10-17. Ids en `_grandes/adrh/bloqueadas_volumen.txt`. Alternativa: el servergis existente para 2019-2023 por sección (`data/raw/v3/ine_v3_gis_seccion.csv.gz`), o pedir al INE la tabla completa por otro canal.
- **EPF 2007-2025:** `https://www.ine.es/ftp/microdatos/epf<año>/datos_epf<año>.zip`, `.../epf<año>/datos_epf.zip`, `.../epf_<año>/`, `.../epfc/`, `.../epf_continua/` devuelven 404. Edición: página de operación base 2006 (`cid=1254736176806`) con selector de año. Alternativa: pedir los ficheros al INE o usar el ZIP 2006 descargado.
- **Vacías por consumo eléctrico, serie anual 2020-…:** no localizada. Alternativa: tabla 59531 del Censo 2021 (ya en el repositorio).
- **Catastro, descarga masiva alfanumérica:** no intentada; requiere certificado (ficha 6).
- **EFF (Banco de España):** no intentada; requiere solicitud a BELab (ficha 7).
- **ECV longitudinal 2017-2025:** no descargada por volumen (~510 MB); decisión del autor pendiente (ficha 5).

## Decisiones tomadas por el adquisidor

- No se ha vuelto a descargar lo que ya estaba en el repositorio (Censo 2021, catastro 2011-2025, ECV 2018-2025, ADRH parcial de servergis).
- La API del ADRH se descargó completa (540 tablas) porque el repositorio solo tenía 2019-2023 por sección desde ArcGIS.
- Los datos crudos no se transforman. La normalización a formato largo es tarea del ingeniero de datos.


## Normalización

Script `src/v16/datos/renta_parque.py` (determinista, sin red, SEED=20261010). Salidas: `data/processed/v16/renta_parque.parquet` (versionado, 2.433.670 filas, 6,3 MB: ADRH variables principales a municipio, distrito y sección más nacional, CCAA y provincia, y Catastro urbano municipal 2026), `data/processed/v16/renta_parque_adrh_completo.parquet` (NO versionado, 37,2 MB, 21.160.414 filas: todo el ADRH normalizado; contiene el versionado salvo la parte ya presente en la base), diccionario `docs/v16/fuentes/renta_parque_variables.csv` (33 variables), tabla de correspondencia nombre -> código INE `docs/v16/fuentes/renta_parque_correspondencia.csv` y estadísticas `data/processed/v16/renta_parque_estadisticas.json`. Test: `tests/v16/test_datos_renta_parque.py` (7 pruebas). capa = C4; `posterior_prereg` = False en todas las filas (el corte de V16 no está fijado); `muestra_sellada_v6` = True en provincia, municipio, distrito y sección de las provincias de `holdout.provincias_selladas_v6()` (600.822 filas del versionado). ECV y EPF no se normalizan aquí: son microdatos que usa directamente el módulo de fase 2.

### Corrección de la ficha 1
Las series de las tablas `DIST-SECC-MUN` SÍ traen distrito y sección en el nombre («Albacete sección 01001», «Albacete distrito 05»; sección = distrito de 2 dígitos + sección de 3). La ficha decía lo contrario. El ADRH de la API cubre así sección 2015-2023 (la base pública solo tenía 2019-2023 del servergis). Las 8 tablas `NAC-CCAA-PROV` descargadas traen nacional, CCAA y provincia.

### Decisiones
- **Formato.** Una fila por serie, año, territorio. Variables `ine_adrh_*` (unidad en la columna `unidad`). Los umbrales (tablas de pobreza) van en tres variables (`ine_adrh_pob_bajo_umbral_fijo_pct`, `ine_adrh_pob_bajo_umbral_rel_pct`, `ine_adrh_pob_sobre_umbral_rel_pct`) y el umbral, el sexo, la edad y la nacionalidad en `desagregacion` (`umbral_eur=5000|sexo=Total|edad=...|nac=...`). Fuentes de renta: una variable por fuente. `fecha_dato` = 31-dic del año de renta. `edicion` = tabla de origen y fecha de modificación (2025-10-21).
- **Unidades.** Se fijan por variable, no por `FK_Unidad` de la API, que es incoherente (renta bruta media por persona viene con la unidad 101, de porcentaje; la cifra es euros: 15.182 en Almansa 2023).
- **Cruce por código INE.** El ADRH solo trae nombres. Municipio: coincidencia exacta con `territorios.parquet` dentro de la provincia inferida de cada tabla (provincia donde caen >= 80 % de los nombres de coincidencia nacional única; las 424 tablas `DIST-SECC-MUN` resultaron de una sola provincia); si no, coincidencia normalizada (tildes, mayúsculas, puntuación); si no, 11 alias explícitos en `ALIAS` del script (cambios de nombre o de grafía, elegidos a mano: Castelló de la Plana, Sant Vicent del Raspeig, Bisbal de Falset -> de Montsant, Atez -> Atetz, Noáin -> Valle de Elorz, etc.; **a revisar por el autor**). Solo coincidencias únicas. Distrito = municipio + 2 dígitos; sección = municipio + 5 dígitos, comprobados contra `territorios.parquet`. CCAA y provincia (tablas NAC): por nombre; los nombres de CCAA uniprovinciales que coinciden con su provincia (Illes Balears, Cantabria, La Rioja, Ceuta, Melilla) se asignan por orden de aparición (primero CCAA, después provincia: así vienen en las 8 tablas) y se publican con su valor propio en cada nivel.
- **Duplicados.** 6 series con el mismo COD en dos tablas: se conserva la primera. Clave única comprobada en el parquet versionado.
- **No duplicado con la base.** `data/base/publica/variables.parquet` ya trae `adrh_renta_neta_persona`, `adrh_renta_neta_hogar` y `adrh_gini` a nivel SECCIÓN 2019-2023 (servergis ArcGIS). Esas 531.812 filas (API, mismas variables, mismo nivel y años) no van al parquet versionado; sí al completo. Sección 2015-2018 de esas tres variables, y todo lo demás, es nuevo. No se ha comparado valor a valor la API con el servergis (queda para la fase 2; no se leyeron filas selladas de la base). No hay municipio, distrito ni otras variables del ADRH en la base.
- **Qué va al versionado.** Renta neta media por persona y por hogar, renta mediana por unidad de consumo, Gini, P80/P20 y población (`desagregacion` vacía), en todos los niveles. El resto (renta bruta, media por UC, mediana por hogar, fuentes de renta, demografía, umbrales) solo en el completo.
- **Catastro URBANA2026.xls.** 7.610 municipios, todos con código INE válido, corte 2026-01-01, periodo 2026. Variables `catastro_urbano_*`: unidades urbanas, valor catastral (total, construcción, suelo), superficie de suelo, parcelas, año de última revisión y, por uso (`desagregacion` = `uso=...`), unidades y valor catastral. Los valores vacíos (43.276: valor catastral de un uso con pocas unidades, presumiblemente secreto estadístico; no verificado) se omiten. La unidad de `SUPERF_URB` (m2) se asume por el nombre del campo: no verificada.

### Valores secretos, nulos y marcados
- Puntos sin guardar: **37.363.757 con `Secreto: true`** (6,1 M en municipio, 7,5 M en distrito, 23,6 M en sección) y **56.225 nulos**; 21.160.414 puntos válidos (de 58.602.409 de la API; la diferencia son los 37,4 M secretos, los nulos y los descartes por código).
- No todo valor con `Secreto: false` es una observación directa. La API lo anota en `Notas` y se declara en `metodo_dato`: `cota_superior_por_secreto_estadistico` (87.700 puntos del completo) y `cota_inferior_por_secreto_estadistico` (27.947): el valor es la cota, no el dato; `valor_sustituto_media_provincia_pob_menor_100` (32.436) y `valor_sustituto_media_comarca_agraria_pob_menor_100` (31.360): en municipios de menos de 100 habitantes el valor es la media de los municipios pequeños de la provincia o de la comarca agraria, no el del propio municipio; `valor_sustituto_media_distrito` (36, secciones); `valor_subarea_estrategia_territorial_navarra` (422). Para análisis municipal hay que excluir o tratar aparte las filas cuyo `metodo_dato` no sea `observado`.

### Rupturas
- **Seccionado.** Las secciones de cada año usan el seccionado de ese año; el cruce se hace con el seccionado 2025 de `territorios.parquet`. 2.839 series de sección y distrito (códigos que ya no existen en 2025) se descartan; la cobertura de sección cambia entre años (p. ej. Gini: 33.342 secciones en 2015, 34.178 en 2018). No se empalman secciones.
- **Municipios.** Fusiones y cambios de nombre: ver alias y descartes. El número de municipios con dato no es constante: puntos municipales de las seis variables principales, 39.722 en 2015, 39.171 en 2019, 43.925 en 2020 y 44.443 en 2023 (salto en 2020, probablemente por menos secreto o más municipios publicados; sin verificar).
- **Base de la renta.** El ADRH usa fuentes administrativas (AEAT y haciendas forales en Navarra y País Vasco; dato de memoria de la metodología INE, no verificado en esta sesión). Un cambio de base o de definición entre 2015 y 2023 dentro de la API no está documentado en los datos descargados; no se ha verificado en la metodología del INE y queda pendiente. Gini y P80/P20 a nivel nacional solo desde 2021.
- **Catastro.** No incluye Navarra ni el País Vasco (haciendas forales; sin las provincias 01, 20, 31 y 48). Un solo corte (2026).

### Descartes
- Municipios del ADRH sin código INE único (18 nombres, 4.107 series; lista en la tabla de correspondencia con estado `sin_coincidencia`): Darrical, Cesuras y Oza dos Ríos (fusionados en Oza-Cesuras), Cerdedo y Cotobade (Cerdedo-Cotobade), Candín, Goñi, Alfarp y los nombres de islas de las tablas NAC (Fuerteventura, Gomera, Gran Canaria, Hierro, Ibiza y Formentera, Lanzarote, Mallorca, Menorca, La Palma, Tenerife: no tienen nivel INE).
- 2.839 series con sección o distrito cuyo código no existe en el seccionado 2025.
- Cero descartes por formato de nombre en la versión final (el parser admite espacios dobles, tabuladores, «Distrito» en mayúscula y «X. distrito 01.»). El fichero de listado de tablas (540 títulos, en `_grandes/adrh/`, no es dato) no se lee.

### Bloques ADRH no descargados (108 de 540; restricción de volumen de la API)
Los 96 asignables por provincia son tablas de porcentaje bajo o sobre umbrales («fijo» = umbrales en euros, «rel» = umbrales relativos a la mediana; por sexo, sexo+nacionalidad o sexo+tramos de edad). En las 52 provincias están completas las familias renta, Gini y P80/P20, fuentes de ingreso y demografía de las tablas `DIST-SECC-MUN`. La provincia se infiere de las tablas descargadas (cada provincia tiene 10 familias); los otros 12 ids no se pueden asignar con certeza (30824-30832 entre Albacete y Alicante, 37677, 37728, 37742, 48439, 48550, 53692 y 53693; estos dos últimos, por su posición, serían de las tablas NAC-CCAA-PROV, de las que se descargaron 8 de 10). Faltan, por provincia:

| Provincia | Tablas que faltan | Familias que faltan |
|---|---|---|
| 01 | 2 | fijo/sexo+nac, rel/sexo+edad |
| 02 | 1 | fijo/sexo+nac |
| 04 | 1 | fijo/sexo+edad |
| 06 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 08 | 3 | fijo/sexo+edad, rel/sexo+nac, rel/sexo+edad |
| 10 | 2 | fijo/sexo, fijo/sexo+edad |
| 11 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 12 | 2 | fijo/sexo+nac, rel/sexo+edad |
| 13 | 3 | fijo/sexo, fijo/sexo+nac, rel/sexo+edad |
| 14 | 3 | fijo/sexo+nac, fijo/sexo+edad, rel/sexo+edad |
| 15 | 2 | fijo/sexo+edad, rel/sexo+edad |
| 16 | 3 | fijo/sexo, fijo/sexo+edad, rel/sexo+edad |
| 17 | 3 | fijo/sexo+nac, rel/sexo+nac, rel/sexo+edad |
| 18 | 2 | fijo/sexo+nac, rel/sexo+edad |
| 19 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 20 | 4 | fijo/sexo+nac, fijo/sexo+edad, rel/sexo, rel/sexo+nac |
| 21 | 1 | fijo/sexo |
| 22 | 4 | fijo/sexo, fijo/sexo+nac, fijo/sexo+edad, rel/sexo+edad |
| 23 | 2 | fijo/sexo, fijo/sexo+edad |
| 24 | 2 | fijo/sexo, fijo/sexo+nac |
| 25 | 1 | fijo/sexo+edad |
| 26 | 3 | fijo/sexo, fijo/sexo+edad, rel/sexo+nac |
| 27 | 2 | fijo/sexo, fijo/sexo+edad |
| 28 | 3 | fijo/sexo+edad, rel/sexo+nac, rel/sexo+edad |
| 30 | 2 | fijo/sexo+edad, rel/sexo+nac |
| 31 | 2 | fijo/sexo+edad, rel/sexo+edad |
| 32 | 1 | fijo/sexo+edad |
| 33 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 34 | 2 | fijo/sexo, fijo/sexo+nac |
| 35 | 3 | fijo/sexo+nac, fijo/sexo+edad, rel/sexo+nac |
| 36 | 2 | fijo/sexo+nac, rel/sexo+nac |
| 37 | 3 | fijo/sexo+nac, fijo/sexo+edad, rel/sexo |
| 38 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 40 | 1 | fijo/sexo+nac |
| 41 | 1 | fijo/sexo+nac |
| 42 | 1 | fijo/sexo+edad |
| 43 | 1 | fijo/sexo+nac |
| 44 | 2 | fijo/sexo+nac, fijo/sexo+edad |
| 45 | 2 | fijo/sexo, fijo/sexo+nac |
| 46 | 5 | fijo/sexo, fijo/sexo+nac, fijo/sexo+edad, rel/sexo+nac, rel/sexo+edad |
| 47 | 2 | fijo/sexo+nac, rel/sexo+nac |
| 49 | 1 | fijo/sexo+edad |
| 50 | 4 | fijo/sexo, fijo/sexo+nac, fijo/sexo+edad, rel/sexo+nac |
| 51 | 2 | fijo/sexo+nac, fijo/sexo+edad |

Ids de las 108 tablas bloqueadas: 30660, 30824, 30825, 30826, 30827, 30828, 30829, 30830, 30831, 30832, 30845, 30855, 30857, 30863, 30864, 30881, 30882, 30899, 30902, 30903, 30937, 30938, 30947, 30948, 30966, 30968, 30973, 30975, 30977, 30983, 30984, 30986, 30992, 30995, 31000, 31001, 31004, 31020, 31022, 31023, 31029, 31031, 31037, 31038, 31045, 31054, 31055, 31056, 31058, 31063, 31064, 31072, 31074, 31082, 31090, 31091, 31100, 31103, 31104, 31118, 31122, 31127, 31130, 31136, 31144, 31146, 31154, 31155, 31158, 31164, 31167, 31171, 31172, 31176, 31181, 31182, 31183, 31190, 31191, 31200, 31209, 31217, 31227, 31235, 31236, 31243, 31245, 31252, 31253, 31254, 31256, 31257, 31263, 31266, 31271, 31279, 31280, 31281, 31284, 31289, 31290, 37677, 37728, 37742, 48439, 48550, 53692, 53693. Fuente fallida registrada arriba (endpoint, edición y fecha).
