# Fuentes fallidas v5

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba, error.


## R1c (2026-10-10)
- Catastro: titulares por naturaleza (persona fisica o juridica) y titularidad publica: sin fichero abierto (comprobado en v4: URBANA solo trae unidades, valor y superficie). Sin dato; solicitud S1 (docs/v4/solicitudes.md).
- Censo 2021, regimen de tenencia por edad de la persona de referencia: sin tabla en Tempus (operaciones CENSOP 463 y CENSOPV 8, probado 2026-10-10); solicitud S7. Se usan EFF 2022 y ECV 2022-2025 (INE 9994) como fuentes por edad.
- Notariado: compradores persona juridica: el repositorio solo trae extranjeros y actos; sin dato.
- INE ICC (indice de costes de construccion): no existe como operacion en Tempus (busqueda en OPERACIONES_DISPONIBLES, 2026-10-10); se usan Eurostat sts_copi_q (en repositorio) e INE ETCL tablas 6030. Afiliacion a la Seguridad Social, seccion F, por provincia: no localizada en fuente abierta accesible. Tabla EPA 66088 (ocupados por sector y CCAA) solo trae 2005-2007 (base antigua); se usa 65354 (provincia, 2007T4-2026T1).
- BK-034 (corregido): la tabla INE 59531 (Censo 2021, consumo electrico, DATOS_TABLA?nult=1) SI publica vacias y uso esporadico por entidad municipal: 3.185 entidades (510 marcadas con asterisco agrupan municipios pequenos) que suman el total nacional. No hay desglose por seccion censal. Fuente unica (C4).

## R1A (BK-014 · alquiler de temporada y por habitaciones)

| Fuente | Endpoint / fichero probado | Edición | Fecha de la prueba | Resultado |
|---|---|---|---|---|
| INE estadística experimental de alojamiento (VUT) | data/raw/ine_v2_vut.csv (tablas 39363/39364) | 2020-08 a 2026-05 | 2026-10-10 | Viviendas y plazas turísticas; sin duración de contrato ni alquiler de temporada |
| SERPAVI (IRPF) | data/raw/pdf/serpavi_*, data/raw/v3/serpavi_*_v3.csv.gz | 2011-2024 | 2026-10-10 | Alquiler declarado en IRPF; sin duración ni modalidad habitación/temporada |
| Fianzas autonómicas (Incasòl) | data/raw/v3/incasol_fianzas_municipio_v3.csv.gz | 2007-2026 | 2026-10-10 | Columnas: contratos y renta por banda; sin duración del contrato |
| Inside Airbnb | data/raw/v3/airbnb_insideairbnb_agregados_v3.csv.gz | 2025-12 a 2026-09 | 2026-10-10 | Solo anuncios activos por tipo (entera, habitación, otros) en 9 ámbitos; sin minimum_nights agregado; fuente única, C4 |

Solo se revisó lo versionado en el repositorio; no se hizo prueba de red en esta pasada. Estado: NO ANALIZADA: FALTAN DATOS (sin fuente oficial con duración del contrato ni modalidad por habitaciones para medir el desvío a temporada).

## A23 (precio y alquiler, 2026-10-10)

| Fuente | Endpoint probado | Edición | Fecha de la prueba | Resultado |
|---|---|---|---|---|
| GVA registro de fianzas de alquiler 2020-2026 | https://dadesobertes.gva.es/api/3/action/package_search?q=fianzas (conjuntos viv-reg-fia-2020 a 2026) | 2020-2026 (2026 parcial) | 2026-10-10 | DESCARGADA en data/raw/v5/gva_fianzas_AAAA.csv (script src/v5/a23_fetch.py). Un registro por fianza: importe, municipio, CP, devuelta; sin mes ni duración. Primer intento del día: túnel cerrado; reintento correcto |
| Madrid, fianzas (Agencia de Vivienda Social / datos.comunidad.madrid.es) | .../package_search?q=fianzas | — | 2026-10-10 | 0 resultados. Existen alquiler medio por CP (1934258, ya en v3) e IPVA por antigüedad de contrato (1934428, derivado del INE IPVA, ya en el repositorio) |
| Euskadi, fianzas (Etxebizitza / opendata.euskadi.eus) | https://opendata.euskadi.eus/api-contents?q=fianzas; /catalogo/...; api.euskadi.eus/vivienda | — | 2026-10-10 | 404 / 403: sin conjunto de fianzas abierto localizado |
| Baleares, fianzas (catalegdades.caib.cat / caib.es) | .../api/3/action/package_search?q=lloguer | — | 2026-10-10 | 404: sin API CKAN; sin dato de fianzas localizado |
| datos.gob.es (catálogo nacional) | apidata/catalog/dataset?_q=fianzas; catalogo.datos.gob.es | — | 2026-10-10 | Bloqueado (Incapsula) / túnel 502 |
| Portales (Idealista, Fotocasa) | No consultados | — | 2026-10-10 | Sin cifra incluida: no hay descarga verificable de informes públicos en esta sesión. Si se añaden, solo C4 con procedencia |
| Tope legal de actualización (RDL 6/2022, RDL 8/2023) y fianza = 1 mensualidad (LAU art. 36) | texto legal no consultado | — | 2026-10-10 | NO VERIFICADO; se declara como supuesto en a23_run.py |
