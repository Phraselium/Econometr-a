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
