# V11-DATOS · Auditoría de exhaustividad (2026-10-15; actualizada tras la segunda pasada)

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
| 5 | OPI, certificados y tarjetas en vigor | ✘ servidor / ✔ parcial | 2013 (Madrid; 1995 por edad y tipo) | provincia 28 | 403 por IP incluso con navegador; réplica CC BY de la Comunidad de Madrid incorporada; sustituto de stock: ECP, censo anual y padrón (cobertura.md) |
| 6 | Protección temporal (Ucrania) por provincia y mes | ✘ / ✔ nacional | 2022-03 | España | Interior inaccesible; Eurostat migr_asytpsm/fm |
| 6 | Protección internacional por provincia y nacionalidad | ✘ / ✔ nacional | 2008-01 | España | Eurostat migr_asyappctzm, migr_asydcfstq |
| 6 | Arraigo y regularizaciones por provincia | ✘ | — | — | 403 (servidor); solicitud 5(c) |
| 7 | Eventos normativos migratorios (BOE) | ✔ | 1985 (consolidadas) | España | 85 normas y 171 modificaciones de las normas núcleo |
| 8 | Censo 2021: tenencia, tamaño y tipo de hogar, superficie, principales y no principales | ✔ | 2021 | municipio (capitales y > 50.000 hab.), provincia, tamaño de municipio | 37 tablas tpx |
| 8 | Censo 2021 por sección | ✔ parcial | 2021 | sección | indicadores ya en v3; no hay tablas de tenencia u hogares por sección |
| 8 | Censo 2021 cruzado por nacionalidad | ✔ parcial | 2021 | municipio (muestra) | microdatos de personas, recuentos sin elevar |
| 9 | Microdatos ECV y EPA: auditoría de variables | ✔ | 2018 | — | docs/v11/auditoria_microdatos_ecv_epa.md |
| 10 | ECEPOV 2021 | ✔ | 2021 | microdatos (municipio solo > 50.000 hab.) | no versionados; inventario de variables |
| 11 | Catastro INSPIRE edificios (València, área metropolitana, Alicante, Castellón) | ✔ | stock 2026 | sección y barrio | 94 municipios (ámbito oficial PATEVAL ∪ radio 20 km ∪ capitales); parcelas y direcciones no agregadas (los edificios llevan uso, inmuebles, viviendas, superficie y año) |
| 12 | Catastro, valores de referencia por municipio | ✘ (no publicado) | — | — | la página renderizada no los ofrece; solicitud 2 |
| 12 | Catastro, titularidad (titulares e inmuebles residenciales por tramo y tipo de persona) | ✔ | 2024 | municipio | CSV 2024-2026; 2006-2023 solo en PC-Axis provincial (no descargado) |
| 12 | Catastro, estadísticas municipales | = sin edición nueva | 2012 | municipio | URBANA2026 ya en la base |
| 13 | MIVAU iniciadas y terminadas, protegida, suelo (incl. municipios > 50.000), transacciones y valor tasado municipales | = sin edición nueva | 1991 | provincia / municipio | al día hasta 2026-06 |
| 13 | MIVAU visados y licencias por municipio | ✘ (no existe) | — | — | visados solo por provincia |
| 14 | Ajuntament de València: equipamientos, vulnerabilidad por barrio, superficie por barrio, manzanas con población, VPP, precio, renta | ✔ | según conjunto | barrio, manzana, punto | CKAN, CC BY 4.0 |
| 14 | Ajuntament: licencias urbanísticas y de cambio de uso; padrón por barrio × edad × nacionalidad | ✘ (no publicado) | — | — | solicitudes 6 y 7 |
| 15 | Afiliación a la Seguridad Social por municipio | ✔ | 2011-12 (diciembres 2011-2020, 2021-10, 2021-12); mensual 2022-01 a 2026-09 | municipio | se prueban todos los meses desde 2009-01: antes de 2022 solo existen esos cortes; celdas «<5» contadas; 2026-07 en adelante = posterior_prereg |
| 15 | Afiliación de extranjeros por provincia | ✔ | 2022-01 (fotos anuales) | provincia | Seguridad Social, ficheros anuales; total 2025-12 = 3.045.174 (cuadra) |
| 15 | Afiliados por municipio de residencia y nacionalidad (BDO GVA) | ✘ entorno | — | — | bdo.gva.es bloqueado por el proxy |
| — | Ámbito oficial del área metropolitana (PATEVAL, GVA) | ✔ | 2026 | 90 municipios | sustituye a la definición operativa |
| 15 | Afiliación: réplicas GVA, Idescat, Eustat, Comunidad de Madrid | no necesario | — | — | la fuente primaria municipal ya está |
| 16 | Registro VUT de la GVA con fechas | = sin edición nueva | 2010 (altas) | registro | el recurso «2025-11-12» es una re-subida del corte de 2025-01-26 |
| 16 | GVA cortes antiguos (web.archive.org) | ✘ entorno | — | — | web.archive.org bloqueado por el proxy de la sesión en las dos pasadas |
| 16 | Euskadi (REATE) | ✔ | inscripciones 2016-08 | registro, municipio | solo vigentes (sin bajas) |
| 16 | Barcelona, cortes antiguos | ✘ servidor | — | — | hCaptcha en las descargas; los cortes trimestrales no están en el datastore CKAN |
| 17 | INE VUT noviembre de 2026 | no publicado aún | — | — | la tarea se ejecuta el 2026-10-15; último dato 2026-05 (ya en la base) |
| 17 | Turismo con teléfonos móviles por municipio | ✔ parcial | 2019 | municipio (Comunitat Valenciana y capitales) | límite de volumen de la API |
| 18 | GTFS EMT València | ✔ | vigente | líneas y paradas | zip CKAN |
| 18 | GTFS Metrovalencia | ✘ entorno | — | — | fgv.es y metrovalencia.es bloqueados por el proxy; no está en los CKAN de GVA ni de València |
| 18 | Matrícula UV | ✔ parcial (no redistribuible) | curso 2024/25 | universidad | tablas del SAP; cursos anteriores solo en PDF |
| 18 | Matrícula UPV; residencias; SIIU | ✘ entorno / no publicado | — | — | datos.upv.es y estadisticas.universidades.gob.es bloqueados por el proxy; upv.es sin ficheros |
| 19 | CGPJ lanzamientos por partido judicial y tipo | = sin edición nueva | 2013 | partido judicial | último: 1T 2026 (ya en v5) |
| 20 | BdE crédito a construcción y promoción; crédito a hogares para vivienda | = sin edición nueva | 1992 | España | al día (2026-06 trimestral; 2026-08 mensual) |
| V9 | Censo 2001 por provincia | ✘ (sin cambios) | — | — | solo sistema interactivo |
| V9 | BCE volúmenes por fijación y país | ✘ (sin cambios) | — | — | solo U2 |
| V9 | IDESCAT hoteles y rural por municipio | ✘ (sin cambios) | — | — | sin años municipales |

**Ausencias.** Ninguna queda sin justificar. Las ausencias que dependen de terceros tienen solicitud redactada. Las que dependen de la red del entorno tienen anotado el host.

## Histórico (continuación V11)
| Fuente | Estado | Inicio–fin real | Nivel | Detalle |
|---|---|---|---|---|
| Catastro, titulares por municipio (JAXI) | ✔ | 2012–2023 | municipio (régimen común, ~7.600) | 2006-2011 no publicados; definición distinta de los CSV 2024-2026 (no se encadenan) |
| Catastro, titularidad por tramos y tipo de persona | ✔ | 2024–2026 | municipio | CSV de la sede |
| Catastro, viviendas por año de construcción y reforma | ✔ | 2019 | municipio | solo publicado para 2019; 2020 únicamente superficie y uso; desde 2022 solo piscinas |
| Obra nueva por municipio y año | ✔ (construida) | INSPIRE: 1900–2026; neta: 2013–2026 | municipio | dos medidas: stock superviviente por año de construcción (94 municipios) y Δ unidades urbanas residenciales (todos) |
| AEAT, IRPF por municipios | ✔ parcial | 2013–2024 | municipio > 1.000 hab., Comunitat Valenciana (331) | informe HTML por municipio; València figura desde 2016; sin nº de declarantes con rentas inmobiliarias; código postal no descargado |
| INE IPVA municipio y distrito | ✔ | 2011–2024 | municipio > 10.000 hab. (720), distritos de capitales (379) | código INE de los metadatos; por tamaño de vivienda; sin antigüedad de contrato |
| Censo anual: país de nacimiento y hogares por municipio | ✘ (no publicado) | — | — | padrón por país de nacimiento 2003-2022 (v9) |

## Tercera pasada (2026-10-16)
| Fuente | Estado | Inicio–fin real | Nivel | Detalle |
|---|---|---|---|---|
| Ajuntament de València, padrón (PDF) | ✔ | 2001–2026 (sin 2014) | barrio, distrito | sexo, edad (3 grupos), continente; validado con INE y censo anual |
| Ajuntament de València, población extranjera (PDF) | ✔ parcial | 2001–2026 | distrito, ciudad | continente por barrio y distrito; países principales 2005-2018 |
| Ajuntament de València, altas y bajas (PDF) | ✔ | 1998–2016 | distrito | sin informe desde 2017 |
| OPI vía datos.gob.es | ✘ | — | — | 403 Incapsula (un intento); los ficheros subidos son páginas de bloqueo |
| Barcelona HUT trimestral (manual) | ✔ | 2018T2–2026T3 | municipio; barrio desde 2023T1 | expedientes únicos |
| GVA BDO afiliación por nacionalidad (manual) | ✔ | 2012T1–2026T3 | municipio | ratio 0,961 frente a la SS en la provincia 46 |
