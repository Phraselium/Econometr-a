# Fuentes fallidas o no disponibles (V9-DATOS, 2026-10-14)

| Fuente | URL o endpoint | Motivo | Qué se hizo en su lugar |
|---|---|---|---|
| Afiliación a la Seguridad Social por municipio | https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/EST10/EST305/c43ad8ea-fe79-4329-ac8e-e5758f3c4d7a («Información desagregada a nivel Municipal») | La página construye los enlaces a los ficheros con JavaScript; ni curl ni un navegador sin interfaz con un tiempo límite razonable obtuvieron los enlaces. Las páginas EST306/EST307 solo tienen datos nacionales y provinciales por CNAE. | Nada. Alternativas para v9: las series municipales de los institutos autonómicos (IDESCAT, Eustat y el Portal Estadístico de la GVA) o la descarga manual del fichero mensual por el autor. |
| Padrón de València por barrio y nacionalidad 2023-2026 | https://opendata.vlci.valencia.es (CKAN; búsqueda «padron»: 0 conjuntos) y https://www.valencia.es/val/estadistica/per-territori | No hay conjunto de padrón por barrio en el portal de datos abiertos; la Oficina d'Estadística no publica ficheros descargables de 2023-2026 localizables por script. | El Censo anual del INE por sección censal y país de nacionalidad (2021-2025) cubre València ciudad por sección (agregable a barrio con la correspondencia sección-barrio del Ajuntament). |
| Inside Airbnb, ediciones históricas | https://insideairbnb.com/get-the-data/ | Solo es pública la última edición de cada ciudad (septiembre de 2026). Las anteriores se piden por formulario (una prueba con València 2025-09-20 dio 403). | Se descargó la edición pública de las cinco ciudades. Para el shock COVID de Cataluña hacen falta las ediciones 2019-2021: hay que pedirlas a Inside Airbnb. |
| Aena, pasajeros mensuales por aeropuerto | https://www.aena.es/es/estadisticas/informes-mensuales.html | Las páginas de estadísticas cargan los informes con JavaScript; no hay enlaces de descarga directa estables. | Nada (fuente opcional). Alternativa: FRONTUR por CCAA (INE), ya en data/raw/v8. |
| INE, viviendas turísticas, edición de noviembre de 2026 | https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/VTE | Aún no publicada: la última edición es la de mayo de 2026, actualizada el 2026-06-24. | Nada: el proyecto ya tiene la edición de mayo de 2026 (data/raw/v3 e ine_vut_*). |

## V9-DATOS-COMPLETO

| Fuente | URL o endpoint | Motivo | Qué se hizo en su lugar |
|---|---|---|---|
| Convalidación o derogación del Decreto ley catalán 1/2025 (contención de rentas) | https://portaljuridic.gencat.cat/eli/es-ct/dl/2025/01/28/1 (HTML, XML y Turtle); conjunto n6hn-rmy7 de analisi.transparenciacatalunya.cat; sumarios del BOE 2025-01 a 2026-10 | El BOE no lo ha publicado (sí el DOGC núm. 9339). El conjunto de normativa del DOGC no incluye las resoluciones del Parlament, y la ficha del Portal Jurídic no trae referencias posteriores. 3 intentos (2026-10-14). | Se registra con la publicación verificada y el estado NO VERIFICADO (eventos_regulacion_v9.csv y regimen_alcance_v9.csv). Segunda pasada en el bloque 9: buscador del Parlament o DOGC por fecha. |
| Wayback Machine (cortes antiguos de registros públicos) | https://web.archive.org/cdx/search/cdx | «Blocked by egress policy»: la política de red del entorno no permite el host. | Pendiente: el autor puede añadir web.archive.org a los dominios permitidos del entorno. |

## V9 COMPLETO, F1 (2026-10-15)

| Fuente | URL o endpoint | Motivo | Qué se hizo en su lugar |
|---|---|---|---|
| BCE MIR, volúmenes de nuevas operaciones por periodo de fijación y país | `MIR/M.<país>.B.A2C.<F,I,O,P>.B.A.2250.EUR.N` | 404 para todos los países: solo existen para el agregado U2 (consulta con comodín, 3 intentos) | Cuota de nuevos préstamos a tipo variable o fijación ≤1 año por país (RAI, SVLHPHH; src/v9/fetch_bce_rai.py) |
| Censo 2001, viviendas principales por provincia | ine.es/censo (sistema interactivo); tempus CENSOPV solo tiene tablas de 2011 | Sin tabla descargable por script (3 intentos) | D7 empieza en 2011 a escala provincial; 2001-2011 solo como contexto nacional |
| EVR (Estadística de Variaciones Residenciales) 1988-2007 por provincia | tempus OPERACIONES_DISPONIBLES (no figura); jaxiT3 | No está en la API ni en jaxiT3 | Flujos EM desde 2008 y EMCR desde 2021; antes de 2008, el componente interno se aproxima con el cambio de la población española del padrón (marcado) |
| Barcelona, cortes trimestrales de HUT (2018T2-2026T3) | opendata-ajuntament.barcelona.cat/…/download | Prueba anti-bot («/challenge») para los zip (3 intentos, con y sin redirecciones) | Registro vigente por la API CKAN datastore, con el año del número de expediente (src/v9/fetch_bcn_hut.py) |
| IDESCAT, hoteles, campings y turismo rural por municipio | turall n=6033, 6034, 6037 con geo=mun | La tabla no ofrece años a escala municipal | Solo HUT y apartamentos turísticos (los que usa D2) |
| Afiliación por municipio (IDESCAT `afi`) | idescat.cat/pub/?id=afi&n=… | Las tablas no exponen descarga SSV municipal estable (2 intentos) | Paro registrado y contratos del SEPE por municipio desde 2006 (src/v9/fetch_sepe_municipios.py) |
| Cortes antiguos del registro VUT de la GVA | web.archive.org | Bloqueado por la política de red (sin cambio desde V9-DATOS) | Panel mensual reconstruido de altas y bajas fechadas (ya en el proyecto) |
| INE viviendas turísticas, edición de noviembre de 2026 | tempus VTE | Aún no publicada (referencia noviembre; se publica en febrero) | Edición de mayo de 2026 |
