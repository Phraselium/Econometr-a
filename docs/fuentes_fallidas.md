# Fuentes fallidas o incompletas

Registro de descargas que no funcionan, están truncadas o no se han podido verificar.
Los datos de la tabla "no descargado" no se han inventado.

## Banco de España

| Dato | Estado | URLs / búsquedas probadas | Alternativa propuesta |
|---|---|---|---|
| Esfuerzo teórico anual (accesibilidad a la vivienda) | No encontrado | Descarga de los 400 CSV enlazados desde `temas/estadisticas-economicas-generales`, `temas/instituciones-financieras`, `temas/tipos-interes`, `temas/sociedades-no-financieras` y `temas/mercados-financieros`; búsqueda de "esfuerzo" y "accesib" en cabeceras y páginas: sin resultados | Calcular el indicador a partir de la cuota (tipo ECB `ecb_tipo_hipotecario_es.csv` + precio `bde_precio_vivienda_libre.csv`) y de renta de INE/Eurostat (fuera de este script). Revisar la visualización "Indicadores del mercado de la vivienda" de BIEST manualmente. |
| Páginas de estadísticas con índice de indicadores de vivienda | 404 | `https://www.bde.es/webbe/es/estadisticas/indicadores/si1_1.html`, `https://www.bde.es/webbe/es/estadisticas/temas/si_1_5.html` | Usar los CSV de boletín (`compartido/datos/csv/beNNNN.csv`) que sí funcionan. |
| Índice de carpeta `compartido/datos/csv/` | 403 | `https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/` | Enlaces directos a cada CSV (funcionan). |

Series BdE descargadas (ver `src/fetch_bde.py`):
- `be2507.csv`: precio medio m2 de vivienda libre tasada (`DHIVTNOAPLPMMUVT_*`). Trimestral. Las series de vivienda nueva y usada solo tienen datos desde 2013. El origen "Ministerio de Vivienda" del enunciado no aparece en el CSV ni en la página del BdE; queda sin confirmar.
- `be1901.csv`: tipo medio de adquisición de vivienda libre (`D_1T9H0000`). Mensual.

## Banco Central Europeo (data-api)

| Serie | Problema | Alternativa propuesta |
|---|---|---|
| `ICP/M.ES.N.000000.4.ANR` (IAPC España, tasa anual) | La serie termina en 2025-12 (estado `E`, estimada). El BCE indica en la metainformación que deja de publicar el índice actual tras el cambio metodológico de 2026. | Eurostat `prc_hicp_manr` (geo=ES, coicop=CP00), fuera del alcance de este script. |
| `FM/B.U2.EUR.4F.KR.MRR_FR.LEV` (tipo BCE operaciones principales) | Serie de fechas de cambio: 48 observaciones (la última 2026-09-16), no mensual. | Expandir a mensual con el tipo vigente a cierre de mes en la capa de limpieza (data-cleaner). |

## INE (src/fetch_ine.py)

Descargas con fallo de endpoint: ninguna. Las siguientes búsquedas no encontraron la serie pedida (3 intentos o más por búsqueda, sobre `OPERACIONES_DISPONIBLES` y `TABLAS_OPERACION/{id}`):

| Dato pedido | Estado | Búsqueda probada | Alternativa propuesta |
|---|---|---|---|
| Encuesta Continua de Hogares (ECH, anual) | No encontrada | Ninguna operación de INE con nombre "Encuesta Continua de Hogares" en `OPERACIONES_DISPONIBLES`; búsqueda de "Hogares" y "ECH" en las 129 operaciones | 60131 (hogares ECP, trimestral desde 2021) es la fuente disponible. Para renta de hogares, ADRH (op. 353, atlas de renta) o Encuesta de Condiciones de Vida fuera de este script. |
| Renta disponible bruta de los hogares (trimestral) | No encontrada a nivel hogares | `CTNFSI` (op. 246), tablas 62265, 80330, 67203 y 80333: solo aparece renta disponible de la economía total | Se descarga 80333 (renta disponible bruta, total de la economía, CTNFSI, trimestral). No es renta de hogares: usar con cautela. |
| Inmigración total trimestral (suma de todas las nacionalidades) | No publicada como serie única en las tablas de ECP (59011, 59013, 59020, 59012) | Búsqueda de nombres con "Total. Flujo" o "Total Nacional. Total" en las tablas de flujo trimestral | Se descarga 69687 (total anual EMCR). Para el total trimestral hay que sumar las nacionalidades de 59011 en la capa de limpieza y declararlo. |
| Inmigración trimestral por CCAA con total (sin nacionalidad) | No localizada | Tablas de la operación ECP (op. 450) y EMCR (op. 455) | 59013 (CCAA × nacionalidad, trimestral desde 2023T2). Para CCAA anual sin nacionalidad: 69691 (EMCR). |

## MIVAU, Ajuntament de València, IVE/PEGV y Notariado/Registradores (src/fetch_mivau.py, src/fetch_valencia.py)

Última comprobación: 2026-10-09.

### 1. Fuentes no descargables (o solo en visor / PDF)

| Fuente (objetivo) | URL probada | Resultado | Alternativa propuesta |
|---|---|---|---|
| SERPAVI, precio del alquiler por municipio (obj. 4) | https://serpavi.mivau.gob.es (visor) · metodología: https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/2026-03-18_Metodologia_SERPAVI.pdf | El visor es una aplicación SPA que consume una API no documentada; `/api/Core` y `/api/Municipios` devuelven 404 y no se han localizado ficheros de descarga. La metodología (PDF) sí responde 200. | Exportar desde el visor si ofrece descarga, o pedir la serie a MIVAU. Como sustituto verificado en INE, la operación 481 "IRAV, Índice de Referencia de Arrendamientos de Vivienda" (API INE `OPERACIONES_DISPONIBLES`); no descargada. |
| Ajuntament de València, padrón de población extranjera por nacionalidad y distrito (obj. 7) | https://valencia.opendatasoft.com (404 en la raíz y en la API v2.1) · catálogo CKAN https://opendata.vlci.valencia.es (funciona, 279 datasets) · informes anuales: https://www.valencia.es/estadistica/Padron/2024/Pob_estrangera_2024_Cast.pdf (200, PDF de 4 MB) | El portal Opendatasoft no responde. El CKAN no tiene un dataset de padrón por nacionalidad (búsquedas `padron`, `nacionalidad`, `extranjer`, `poblacion`). Los datos por distrito solo aparecen en PDF anuales. | Extraer las tablas por distrito de los PDF anuales (2001-2024; el padrón es a 1 de enero) con un parser de PDF y revisión manual. |
| Institut Valencià d'Estadística (IVE) y Portal Estadístic PEGV (obj. 8) | https://www.ive.es · https://pegv.gva.es · https://www.gva.es · https://ive.gva.es | Bloqueo en el proxy de salida: `ws_closed_mid_exchange` (corte de túnel tras 8-13 s) en www.ive.es, pegv.gva.es y www.gva.es, y `502` a CONNECT en ive.gva.es (estado del proxy, `recentRelayFailures`). Es un problema de red, no del endpoint. | Reintentar desde otra red o más tarde. No se ha intentado rodear el bloqueo. Sin datos de la CV de esta fuente por ahora. |
| Colegio de Registradores, Estadística Registral Inmobiliaria: compras por extranjeros (obj. 9) | https://www.registradores.org/documents/33383/148210/ERI+Anuario+2025.pdf (200, PDF) · https://www.registradores.org/en/actualidad/notas-de-prensa/-/asset_publisher/VkEXepWEVFi3/content/estadistica-registral-inmobiliaria-1er-trimestre-de-2025 (200) · https://www.registradores.org/estadistica (404) | Las estadísticas se publican como notas de prensa y PDF (anuario, trimestral). No hay fichero de serie. | Extraer tablas del anuario PDF (compras por extranjeros, nacionalidad, CCAA) con revisión manual. |
| Notariado, Centro de Información Estadística (obj. 9) | https://www.notariado.org/portal/estadisticas (404) · https://www.notariado.org/portal/estadistica-notarial (404) · https://www.notariado.org (200) · documento de biblioteca: https://www.notariado.org/liferay/c/document_library/get_file?uuid=3d4f2b73-8fae-43a2-a132-60571cbd87f7&groupId=2289837 (200, PDF) · https://www.cienotariado.org (corte de conexión) | Las series se publican como anexos PDF/XLSX dentro de los informes semestrales. La URL del XLSX de series no se ha verificado. | Descargar el "Anexo tablas: series estadísticas" del informe 2S 2025 desde la nota de prensa de compraventas por extranjeros (XLSX si está disponible) y convertirlo a CSV. |

### 2. Fuentes parciales o sustitutas (documentar en el análisis)

- **Visados de dirección de obra (CSCAE) y certificados de fin de obra (obj. 2).** No están en el MIVAU. Se usan las series mensuales "viviendas libres iniciadas" (tabla 32100500, `mivau_visados.csv`) y "viviendas libres terminadas" (tabla 32101000, `mivau_fin_obra.csv`), del Boletín de Fomento. Son proxies: no son visados ni certificados de fin de obra, y su definición exacta no consta en el fichero.
- **Transacciones por municipio (obj. 5).** `mivau_transacciones_municipios.csv` solo contiene los municipios que aparecen en la lista >25.000 hab. de la tabla 35103500 (305 de 306 emparejados por nombre; Vila-real/Villarreal no aparece en la tabla de transacciones). El Boletín publica todos los municipios (tabla 34010210, ~240 MB en CSV); el fichero completo se puede regenerar desde `data/raw/mivau_xls/34010210.XLS`.
- **Valor tasado, vivienda libre antigüedad (35101500, 35102000).** Disponibles en el Boletín, no incorporadas en esta descarga.
- **Precio de la vivienda libre del Ajuntament de València (`vlc_precio_vivienda_libre.csv`).** Cobertura solo 2021T2-2022T2 en el recurso CKAN. La fuente primaria no aparece en el recurso. Sirve solo como contraste.
- **Idealista / Fotocasa.** PRIVADA: no descargar. Solo para robustez (ver `CLAUDE.md`).

### 3. Notas de acceso

- Los XLS de `apps.fomento.gob.es/BoletinOnline2/sedal/` responden con User-Agent del proyecto. Algunas páginas HTML del MIVAU (`www.mivau.gob.es`) devuelven 403 a clientes sin navegador; el script no raspa HTML, solo descarga XLS e INE API.
- Algunos ficheros `.XLS` del Boletín son en realidad xlsx; `utils_fetch.read_excel_any` detecta el formato por cabecera.
