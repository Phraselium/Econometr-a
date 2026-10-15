# V11-DATOS · Fuentes fallidas

Regla: máximo 3 intentos y 30 minutos por fuente; segunda pasada al final de la tarea (2026-10-15, tarde).

Tipos de fallo:
- **Servidor**: el organismo rechaza la conexión automatizada (403, WAF, Cloudflare, reto anti-bots).
- **Red**: el proxy del entorno rechaza el host («connect_rejected»: no está en la lista de dominios permitidos) o
  corta el túnel. Se resuelve ampliando el acceso de red del entorno (configuración del entorno → Network access →
  añadir el dominio).

| Fuente (punto) | Endpoint | Edición buscada | Fecha | Intentos | Error | Tipo | Segunda pasada | Alternativa |
|---|---|---|---|---|---|---|---|---|
| OPI: residentes con certificado o tarjeta en vigor (5) | inclusion.gob.es/web/opi/estadisticas/catalogo/extranjeros_con_certificado; /documents/d/opi/… | nota 30-6-2025 / 2-12-2025 | 2026-10-15 | 3 + 2 | HTTP 403 «Acceso denegado» (también vía WebFetch); datos.gob.es 403 (Incapsula) | servidor | 403 | Eurostat migr_resvalid (nacional); solicitud 5(d) |
| Interior, protección internacional y temporal por provincia (6) | interior.gob.es (Oficina de Asilo y Refugio); proteccion-asilo.interior.gob.es | avances mensuales 2026 | 2026-10-15 | 3 + 1 | reto Cloudflare; subdominio sin conexión | servidor / red | igual | Eurostat migr_asy* (nacional); solicitud 5(a,b) |
| Arraigo y regularizaciones por provincia (6) | inclusion.gob.es (OPI, flujo de autorizaciones) | — | 2026-10-15 | (mismo host que OPI) | 403 | servidor | 403 | solicitud 5(c) |
| Catastro, valores de referencia por municipio (12) | catastro.hacienda.gob.es/esp/estadisticas*.html; /documentos/estadisticas/ | 2022-2026 | 2026-10-15 | 3 | página generada con JavaScript sin enlaces; rutas directas = página genérica; búsqueda web sin fichero | no publicado como fichero | — | solicitud 2 |
| MIVAU: visados y licencias municipales por municipio (13) | apps.fomento.gob.es/BoletinOnline2 | — | 2026-10-15 | 1 (índice completo) | no existen en el boletín (visados solo por provincia; licencias no publicadas) | no publicado | — | provincia (ya en la base) |
| Ajuntament de València: licencias urbanísticas y padrón por barrio × nacionalidad (14) | opendata.vlci.valencia.es (CKAN) | — | 2026-10-15 | 2 búsquedas | no publicados en el portal | no publicado | — | solicitudes 6 y 7; IVE por sección (v9) |
| GVA VUT, cortes antiguos en web.archive.org (16) | web.archive.org | 2015-2024 | 2026-10-15 | 3 + 1 | túnel cerrado / «connection reset» en el proxy | red | igual | histórico GVA con altas y bajas (v9) |
| Barcelona HUT, cortes trimestrales 2018T2-2026T3 (16) | opendata-ajuntament.barcelona.cat/…/resource/<id>/download | 33 cortes | 2026-10-15 | 2 + 1 | 302 → /challenge (reto anti-bots) | servidor | igual (la API CKAN responde; las descargas no) | registro vigente por año de expediente (v9) |
| Metrovalencia GTFS (18) | fgv.es, metrovalencia.es | vigente | 2026-10-15 | 3 | sin conexión (000) | red | — | GTFS EMT (descargado); NAP de Transportes requiere registro |
| Universidades: matrícula y residencias UV y UPV (18) | estadisticas.universidades.gob.es (SIIU), educacion.gob.es/educabase, datos.upv.es, uv.es | cursos 2015-2026 | 2026-10-15 | 3 + 1 | sin conexión o connect_rejected (SIIU, EDUCAbase, datos.upv.es); 404 en páginas de cifras UV/UPV | red | igual | — |
| INE turismo con móviles, tablas completas (17) | jaxiT3 52048/53464 (csv, px, xlsx) | — | 2026-10-15 | 4 formatos | HTTP 500 (tabla demasiado grande); API: «restricciones de volumen» | servidor | resuelto por municipio (CV y capitales) | — |

Hosts rechazados por la política de red (para ampliar el acceso si se quiere completar): estadisticas.universidades.gob.es,
www.educacion.gob.es, datos.upv.es, proteccion-asilo.interior.gob.es, www.fgv.es, www.metrovalencia.es, web.archive.org.
