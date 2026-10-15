# V11-DATOS · Auditoría de exhaustividad (2026-10-15)

Cada fuente pedida en la tarea V11-DATOS y las que quedaron abiertas en auditorías anteriores (docs/v9/auditoria_exhaustividad.md),
con su estado.

**Leyenda.**
- **✔**: incorporada.
- **✔ parcial**: incorporada con un recorte documentado.
- **= sin edición nueva**: ya estaba y no hay edición posterior (verificado).
- **✘**: no conseguida, con su causa.

**Fallos.** El detalle está en docs/v11/fuentes_fallidas.md; las peticiones, en docs/v11/solicitudes.md.

| # | Fuente | Estado | Inicio real | Nivel | Detalle |
|---|---|---|---|---|---|
| 1 | EVR, microdatos (OD municipio-municipio, nacionalidad, sexo, edad) | ✔ | 1988 | municipio ≥10.000 hab. (resto = PP999) | resuelve el ✘ de V9 («EVR 1988-2007»); OD anual no versionado (make datos_v11); bajas al extranjero solo desde 2002 (no registradas antes) |
| 2 | EMCR, microdatos | ✔ | 2021 | municipio ≥10.000 hab. | validada contra la tabla 69696 |
| 2 | EMCR, tablas municipales publicadas (8) | ✔ | 2021 | todos los municipios; área submunicipal | — |
| 2 | EM municipal antes de 2021 | ✘ (no existe) | — | — | la EM es provincial (v9); municipal = EVR |
| 3 | MNP nacimientos y defunciones por municipio de residencia | ✔ | 1980 | municipio ≥10.000 hab. | nacionalidad desde 1996 (nac.) y 1999 (def.); 1975-1979 no incorporado (otro diseño) |
| 4 | ECP por nacionalidad, trimestral | ✔ | 2002T1 | provincia | 56947, 82104, 60129, 79278 |
| 4 | ECP por municipio | ✘ (no existe) | — | — | municipal anual: padrón (v9, 2003-2022) y censo anual (v9, 2021-2025) |
| 4 | Hogares por nacionalidad de la persona de referencia | ✔ parcial | 2021 | municipio (muestra 10 %) | ECP no lo publica; Censo 2021 microdatos (NORDEN = 01 como aproximación) |
| 5 | OPI, certificados y tarjetas en vigor | ✘ | — | — | 403 (servidor); Eurostat migr_resvalid nacional como respaldo |
| 6 | Protección temporal (Ucrania) por provincia y mes | ✘ / ✔ nacional | 2022-03 | España | Interior inaccesible; Eurostat migr_asytpsm/fm |
| 6 | Protección internacional por provincia y nacionalidad | ✘ / ✔ nacional | 2008-01 | España | Eurostat migr_asyappctzm, migr_asydcfstq |
| 6 | Arraigo y regularizaciones por provincia | ✘ | — | — | 403 (servidor); solicitud 5(c) |
| 7 | Eventos normativos migratorios (BOE) | ✔ | 1985 (consolidadas) | España | 85 normas y 171 modificaciones de las normas núcleo |
| 8 | Censo 2021: tenencia, tamaño y tipo de hogar, superficie, principales y no principales | ✔ | 2021 | municipio (capitales y > 50.000 hab.), provincia, tamaño de municipio | 37 tablas tpx |
| 8 | Censo 2021 por sección | ✔ parcial | 2021 | sección | indicadores ya en v3; no hay tablas de tenencia u hogares por sección |
| 8 | Censo 2021 cruzado por nacionalidad | ✔ parcial | 2021 | municipio (muestra) | microdatos de personas, recuentos sin elevar |
| 9 | Microdatos ECV y EPA: auditoría de variables | ✔ | 2018 | — | docs/v11/auditoria_microdatos_ecv_epa.md |
| 10 | ECEPOV 2021 | ✔ | 2021 | microdatos (municipio solo > 50.000 hab.) | no versionados; inventario de variables |
| 11 | Catastro INSPIRE edificios (València, área metropolitana, Alicante, Castellón) | ✔ | stock 2026 | sección y barrio | 51 municipios; parcelas y direcciones no agregadas (los edificios llevan uso, inmuebles, viviendas, superficie y año) |
| 12 | Catastro, valores de referencia por municipio | ✘ | — | — | no hay fichero descargable; solicitud 2 |
| 12 | Catastro, estadísticas municipales | = sin edición nueva | 2012 | municipio | URBANA2026 ya en la base |
| 13 | MIVAU iniciadas y terminadas, protegida, suelo (incl. municipios > 50.000), transacciones y valor tasado municipales | = sin edición nueva | 1991 | provincia / municipio | al día hasta 2026-06 |
| 13 | MIVAU visados y licencias por municipio | ✘ (no existe) | — | — | visados solo por provincia |
| 14 | Ajuntament de València: equipamientos, vulnerabilidad por barrio, superficie por barrio, manzanas con población, VPP, precio, renta | ✔ | según conjunto | barrio, manzana, punto | CKAN, CC BY 4.0 |
| 14 | Ajuntament: licencias urbanísticas y de cambio de uso; padrón por barrio × edad × nacionalidad | ✘ (no publicado) | — | — | solicitudes 6 y 7 |
| 15 | Afiliación a la Seguridad Social por municipio | ✔ | 2011-12 (diciembres); mensual desde 2022-01 | municipio | resuelve el ✘ de V9; celdas «<5» contadas |
| 15 | Afiliación: réplicas GVA, Idescat, Eustat, Comunidad de Madrid | no necesario | — | — | la fuente primaria municipal ya está |
| 16 | Registro VUT de la GVA con fechas | = sin edición nueva | 2010 (altas) | registro | el recurso «2025-11-12» es una re-subida del corte de 2025-01-26 |
| 16 | GVA cortes antiguos (web.archive.org) | ✘ | — | — | red |
| 16 | Euskadi (REATE) | ✔ | inscripciones 2016-08 | registro, municipio | solo vigentes (sin bajas) |
| 16 | Barcelona, cortes antiguos | ✘ | — | — | reto anti-bots |
| 17 | INE VUT noviembre de 2026 | no publicado aún | — | — | la tarea se ejecuta el 2026-10-15; último dato 2026-05 (ya en la base) |
| 17 | Turismo con teléfonos móviles por municipio | ✔ parcial | 2019 | municipio (Comunitat Valenciana y capitales) | límite de volumen de la API |
| 18 | GTFS EMT València | ✔ | vigente | líneas y paradas | zip CKAN |
| 18 | GTFS Metrovalencia | ✘ | — | — | red |
| 18 | Matrícula y residencias UV y UPV | ✘ | — | — | red |
| 19 | CGPJ lanzamientos por partido judicial y tipo | = sin edición nueva | 2013 | partido judicial | último: 1T 2026 (ya en v5) |
| 20 | BdE crédito a construcción y promoción; crédito a hogares para vivienda | = sin edición nueva | 1992 | España | al día (2026-06 trimestral; 2026-08 mensual) |
| V9 | Censo 2001 por provincia | ✘ (sin cambios) | — | — | solo sistema interactivo |
| V9 | BCE volúmenes por fijación y país | ✘ (sin cambios) | — | — | solo U2 |
| V9 | IDESCAT hoteles y rural por municipio | ✘ (sin cambios) | — | — | sin años municipales |

**Ausencias.** Ninguna queda sin justificar. Las ausencias que dependen de terceros tienen solicitud redactada. Las que dependen de la red del entorno tienen anotado el host.
