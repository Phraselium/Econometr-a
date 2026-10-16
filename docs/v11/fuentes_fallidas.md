# V11-DATOS · Fuentes fallidas

Regla: máximo 3 intentos y 30 minutos por fuente. Dos pasadas el 2026-10-15:
- **primera pasada**: tarea V11-DATOS;
- **segunda pasada**: «acceso de red completo», 15:15-16:30 UTC.

## A. Bloqueo del ENTORNO (proxy de salida de la sesión)
Comprobación de la segunda pasada: 3 intentos por host con curl, separados 15 s. Resultado en los tres: código 000. El registro del proxy dice «tunnel closed (code 1006) … 39 B received»: el proxy de la sesión cierra el túnel. No es el servidor (uv.es y upv.es responden 200 en el mismo bucle). La ampliación de red pedida no se ha aplicado a este contenedor; probablemente hará falta una sesión nueva.

| Host | Qué se necesitaba | Estado tras la 2.ª pasada | Alternativa usada |
|---|---|---|---|
| web.archive.org | cortes antiguos del registro VUT de la GVA y de Barcelona (punto 2) | bloqueado (000) | ninguna: no hay otra copia histórica pública; GVA tiene el histórico con altas y bajas hasta 2025-01 (v9) |
| datos.upv.es | matrícula UPV | bloqueado | ninguna (upv.es no publica ficheros de cifras) |
| estadisticas.universidades.gob.es (SIIU) | matrícula y residencias por universidad | bloqueado | UV: tablas del SAP (curso 2024/25, no redistribuibles) |
| www.fgv.es, www.metrovalencia.es | GTFS de Metrovalencia | bloqueados | ninguna (no está en el CKAN de la GVA ni en el de València) |
| bdo.gva.es | Base de Datos Oficial de la GVA: afiliados por municipio de residencia y nacionalidad (trimestral) | bloqueado (túnel cerrado) | afiliación por municipio de la Seguridad Social (sin nacionalidad) y afiliación de extranjeros por provincia |
| proteccion-asilo.interior.gob.es | protección internacional | bloqueado | Eurostat (nacional) |

## B. Bloqueo del SERVIDOR (el organismo rechaza el acceso automatizado)
| Fuente | Endpoint | Intentos (1.ª + 2.ª pasada) | Respuesta | Alternativa conseguida |
|---|---|---|---|---|
| OPI, residentes con certificado o tarjeta en vigor | inclusion.gob.es (catálogo, /documents/d/opi/…) | 3 + 3 (curl, WebFetch, Chromium sin interfaz) | 403 «Acceso denegado» por IP, también con navegador real | réplica de la Comunidad de Madrid (CC BY, provincia 28, 2013-2025 por país; desde 1995 por edad y tipo); Eurostat migr_resvalid (nacional); sustituto de stock ECP, censo y padrón (cobertura.md) |
| Interior, protección internacional y temporal por provincia | interior.gob.es | 3 + 1 (Chromium sin interfaz) | reto de Cloudflare («Just a moment…») no superado; no se intenta eludir | Eurostat migr_asy* (nacional) |
| Arraigo y regularizaciones | inclusion.gob.es | igual que la OPI | 403 | solicitud 5(c) |
| Barcelona, cortes trimestrales HUT 2018T2-2026T3 | opendata-ajuntament.barcelona.cat/…/download | 2 + 1; datastore CKAN comprobado | hCaptcha (BunkerWeb). Solo el recurso vigente está en el datastore; los 33 zips trimestrales no (`datastore_active = False`) | registro vigente por año de expediente (v9); no se elude el captcha |
| datos.gob.es (réplicas) | apidata | varias | Incapsula limita tras 1-2 peticiones; con espera responde | catálogo leído: réplicas de Madrid (incorporada) e ICANE (Cantabria, otra estadística: permisos de trabajo) |
| INE turismo con móviles (tablas completas) | jaxiT3 52048/53464 | 4 formatos | 500; API: «restricciones de volumen» (≤ ~36 meses por municipio) | descarga por municipio y tramo de 3 años (Comunitat Valenciana y capitales) |

## C. No publicado (no es un fallo de acceso)
- **Catastro, valores de referencia por municipio.** La página de estadísticas, renderizada con Chromium, no tiene ningún fichero de valores de referencia (sí ocupación, año de construcción y titularidad). Solicitud 2.
  - **Recuperado en esta pasada:** la estadística de TITULARIDAD por municipio, 2024-2026, en CSV. Los años 2006-2023 solo están en PC-Axis por provincia, en el servidor jaxi del Catastro (no descargados).
- **MIVAU:** visados y licencias por municipio.
- **Ajuntament de València:** licencias urbanísticas y padrón por barrio × nacionalidad. Solicitudes 6 y 7.
- **UPV:** matrícula en ficheros descargables (solo noticias).
- **INE VUT noviembre de 2026:** todavía no publicado (fecha de la tarea: 2026-10-15).

## D. Incidencias de proceso
- **Afiliación municipal de la Seguridad Social.** El fichero de 2025-05 trae el último dígito del código de municipio desplazado al nombre, y el de 2025-07 llama «COD CNAE09» a la columna. Se corrigen en el script, que ahora guarda caché por mes. La primera ejecución se perdió al fallar en 2025-07, y se relanzó.
- **Turismo con móviles.** La primera ejecución pidió 200 periodos y fallaron las 591 peticiones (límite de volumen). Se relanzó por tramos.

## E. Tercera pasada (2026-10-16)
- **OPI por la API de datos.gob.es** («Extranjeros con certificado de registro o tarjeta de residencia en vigor» y «Personas ucranianas con documentación de residencia o estancia en vigor»): un intento, 403 de Incapsula. No se insiste.
  - Los ficheros subidos por el autor (`OPI_datos_completos.zip`, `OPI_Descarga_Completa.zip`) contienen la página de bloqueo, no datos.
  - `datos-wayback.zip` contiene conjuntos de la GVA ajenos al registro turístico; no se incorpora. El primer zip subido estaba vacío.
- **Padrón de València 2014:** no existe con ningún nombre (`Padron2014.pdf`, `...Cast.pdf`, `...Val.pdf`). No publicado.
- **Altas y bajas del padrón de València desde 2017:** no existe en `AltasBajas/<A>/` ni en `<A>/`. No publicado.
- **Padrón y población extranjera de València 2025-2026 en castellano:** fuentes sin mapa Unicode; se usa la versión en valenciano y OCR en las páginas afectadas.
