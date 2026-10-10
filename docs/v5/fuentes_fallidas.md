# Fuentes fallidas v5

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba, error.


## R1c (2026-10-10)
- Catastro: titulares por naturaleza (persona fisica o juridica) y titularidad publica: sin fichero abierto (comprobado en v4: URBANA solo trae unidades, valor y superficie). Sin dato; solicitud S1 (docs/v4/solicitudes.md).
- Censo 2021, regimen de tenencia por edad de la persona de referencia: sin tabla en Tempus (operaciones CENSOP 463 y CENSOPV 8, probado 2026-10-10); solicitud S7. Se usan EFF 2022 y ECV 2022-2025 (INE 9994) como fuentes por edad.
- Notariado: compradores persona juridica: el repositorio solo trae extranjeros y actos; sin dato.
- INE ICC (indice de costes de construccion): no existe como operacion en Tempus (busqueda en OPERACIONES_DISPONIBLES, 2026-10-10); se usan Eurostat sts_copi_q (en repositorio) e INE ETCL tablas 6030. Afiliacion a la Seguridad Social, seccion F, por provincia: no localizada en fuente abierta accesible. Tabla EPA 66088 (ocupados por sector y CCAA) solo trae 2005-2007 (base antigua); se usa 65354 (provincia, 2007T4-2026T1).
- BK-034 (corregido): la tabla INE 59531 (Censo 2021, consumo electrico, DATOS_TABLA?nult=1) SI publica vacias y uso esporadico por entidad municipal: 3.185 entidades (510 marcadas con asterisco agrupan municipios pequenos) que suman el total nacional. No hay desglose por seccion censal. Fuente unica (C4).

## R1A (BK-014 · alquiler de temporada y por habitaciones) (2026-10-10; véase también A23: fianzas GVA sin duración del contrato)

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

## R1b (donut, sensibilidad v2, GSADF; 2026-10-10)

| Fuente | Endpoint probado | Edición | Fecha de la prueba | Resultado |
|---|---|---|---|---|
| Atlas de Áreas Urbanas (MIVAU) | https://www.mivau.gob.es (raíz) | — | 2026-10-10 | 403 desde el proxy; no está en el repositorio. Sustituto declarado: áreas = capital provincial (o municipio de mayor parque de viviendas, Censo 2021) y radio de 15-60 km sobre centroides de secciones INE 2021 (data/raw/v5/municipio_centroides_utm30.csv, generado por src/v5/r1b_fetch.py desde el zip local) |
| BO H4 (sensibilidad Oster/CH) | — | — | 2026-10-10 | No ejecutado por presupuesto del módulo (BK-040 «si cabe») |

## A4 (coste de construcción oficial, 2026-10-10)

| Fuente | Endpoint probado | Edición | Fecha de la prueba | Resultado |
|---|---|---|---|---|
| (a) MBC, RD 1020/1993 (BOE-A-1993-19265) | https://www.boe.es/buscar/act.php?id=BOE-A-1993-19265 | consolidada 2025-12 | 2026-10-10 | DESCARGADA a data/raw/v5/a4_mbc_rd1020_1993.csv (src/v5/a4_fetch.py). Solo MBC1-MBC7 de 1993 (28.800-46.800 pta/m2) y coeficientes máximos (1,20-1,36). MBC vigentes por ponencia municipal y valores de referencia (Orden HFP/1104/2021 solo fija el factor de minoración): sin tabla agregada accesible; sede del Catastro devuelve formulario por inmueble. SIN DATO por provincia |
| (b) Módulos/precios máximos VPO (RD 42/2022 BOE-A-2022-802; RD 326/2026 BOE-A-2026-8872; RD 106/2018 BOE-A-2018-3358) | texto consolidado BOE | 2018, 2022, 2026 | 2026-10-10 | Sin módulo de coste: el precio máximo lo fija cada CCAA. Subvenciones por m2 útil (hasta 1.000 EUR/m2 en el RD 326/2026, art. del programa de vivienda asequible) no son coste. Comunidad de Madrid y Generalitat de Cataluña: URL probadas 404; Junta de Andalucía: portal sin tabla de módulos. SIN DATO |
| (c) PEM por m2 en licencias/visados (MIVAU Boletín Online, CSCAE) | https://apps.fomento.gob.es/BoletinOnline2/?nivel=2&orden=3x000000 (30-37); https://www.mivau.gob.es/vivienda/estadisticas-observatorio; https://www.cscae.com/index.php/es/estadisticas | — | 2026-10-10 | Boletín: las tablas de edificación son de unidades (iniciadas, terminadas, protegidas), sin presupuesto de ejecución material; MIVAU 403; CSCAE 404. SIN DATO |
| INE ETCL / Eurostat sts_copi_q | data/raw/eurostat_costes.csv; data/raw/v5/ine_r1c_t6030.csv | 1980Q1-2026Q2 | 2026-10-10 | Solo evolución (índice 2021=100): se usa para actualizar el MBC de 1993; no da nivel |
| Catastro (catastro.hacienda.gob.es/esp/valores_referencia.asp) | idem | — | 2026-10-10 | Túnel 502 |

## A5 (2026-10-10, programas oficiales)
| Fuente | URL | Error | Alternativa | Fecha |
|---|---|---|---|---|
| Programa 2023, D01 (web oficial) | web oficial de la formación de D01 (URL en inventario.csv) | HTTP 200 con HTML de 212 bytes: script anti-bot (Incapsula); no se evade | Solo copia de medio (v4): «no oficial: excluido» | 2026-10-10 |
| Programa 2023, D02 (completo) | https://www.pp.es/programa-electoral y 3 rutas /storage/2023/07/... y /sites/default/files/documentos/... | HTTP 404 | Resumen oficial de 5 pp. (D03, cota); el completo solo en copia de medio: excluido | 2026-10-10 |
| Programa 2023, D04 | https://www.voxespana.es/ , /programa y rutas de PDF probadas | HTTP 403 (bloqueo) / 404 | Solo copia de medio (v4): excluido; sus proposiciones de ley (D20, D21) si entran | 2026-10-10 |
| Programa 2023, D13 | https://www.junts.cat y busqueda web | Sin PDF del programa de 2023 (solo manifiestos de otras convocatorias) | Proposicion de ley oficial D26 (congreso.es) | 2026-10-10 |
| Programa 2023, D14 | https://www.coalicioncanaria.org y busqueda web | Sin programa general 2023 (solo programas locales/insulares) | Ninguna | 2026-10-10 |
| Programa 2023, D15 | https://www.podemos.info | HTTP 403 | Ninguna; no se probo otra via | 2026-10-10 |
| Programa 2023, D16 | https://compromis.net | Sin conexion (codigo 000) | Ninguna | 2026-10-10 |
| Proposiciones de ley XV leg. de formaciones sin PL de vivienda localizada | congreso.es/webpublica/opendata/iniciativas/ProposicionesDeLey (CSV 2026-10-10) | Sin iniciativa de vivienda localizada por palabra clave en OBJETO para BNG, UPN, CC | Ninguna | 2026-10-10 |

## B1 (necesidad de vivienda 2026-2035)
Prueba del 2026-10-10 contra la API Tempus del INE (https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/{op}):
- Censo 2021 (operaciones 463 CENSOP y 8 CENSOPV; edición 2021): sin tablas de hogares con varios núcleos, hacinamiento, superficie por persona ni hogares por edad del jefe. Componentes A3, A4, A5 y tasa de jefatura 75+ de L: SIN DATO (Censo 2021 solo aporta por sección hogares por tamaño, `t22_*`).
- ECV (operación 155, edición 2025): tabla 10001 (problemas en la vivienda) solo por CCAA y sin hacinamiento; no se usa para provincias.
- Traslados a residencias (EPA/Censo/literatura) y licencias de derribo del Ministerio: no se localizó endpoint; no probados fuera del repositorio. Componente de residencias de L y método de demoliciones de R: SIN DATO.
- Proyección de Hogares (operación 70, tabla 54562, mod. 2026-06-17) incluye provincias: sin fallo.
- Vacancia disponible en venta y alquiler por provincia: sin endpoint; V usa solo el alquiler del Censo 2021.
- Referencia Rosen y Smith (1983, AER) sobre vacancia natural: no hallada en Crossref (consulta 2026-10-10): NO VERIFICADA.

## B3 (2026-10-10)
| Fuente | Endpoint | Resultado |
|---|---|---|
| ADRH renta por hogar provincial 2015 | servicios.ine.es/wstempus/js/ES/DATOS_TABLA/30656 (y 31097, 30824) | Solo municipios/secciones; descarga completa «No puede mostrarse por restricciones de volumen». Sin agregado provincial 2015. Se usa PIB pc de la CRE |

## CA (2026-10-10, comparación europea, crédito a promotores, contado frente a hipoteca)
| Fuente | Endpoint | Resultado | Alternativa |
|---|---|---|---|
| BdE, nuevas operaciones de crédito por finalidad (construcción, inmobiliarias) | Boletín Estadístico cap. 4, be04xx/be19xx (csv) probados be0401-be0430, be1901-be1920 | Los cuadros 4.12, 4.13, 4.18 dan solo saldos por finalidad; las nuevas operaciones por actividad no figuran en el Boletín (be1913 es SNF sin desglose por actividad) | Saldo (be0418, mensual, desde 1992-12) como serie de crédito; no es flujo |
| BCE BLS (EPB) España, criterios de vivienda anteriores a 2022 | data-api.ecb.europa.eu/service/data/BLS/Q.ES.ALL.CP.H.H.B3.ST.S.FNET | Disponible solo desde 2022-Q2 (18 trimestres); empresas desde 2003-Q1 | Se usa empresas (CP.E.Z) para 2005-2025; vivienda solo descriptiva reciente |
| BCE data-api, claves BLS con comodines (Q.ES, Q.ES.ALL.ALL...) | idem | HTTP 400 con página de bloqueo; solo funcionan claves completas o detail=serieskeysonly en BLS/all | Claves completas de 10 dimensiones |
| Notariado, porcentaje de compraventas con préstamo hipotecario | notariado.org/liferay/web/cien/estadisticas-al-completo (getFiltrosWeb: 404/HTML); penotariado.com (exige cuenta, ver docs/fallidas/notariado.md) | Sin serie accesible de compraventas ni de financiadas | Ninguna: tercera fuente de C3 sin dato |
| Registradores, % de compras con hipoteca | opendata.registradores.org (solo compraventas); ERI Anuarios 2023-2025 (PDF local) | No publica el porcentaje; sí el número de hipotecas sobre vivienda (2022-2025, texto del capítulo 17) | Razón hipotecas/compraventas 2022-2025 |
| Eurostat, nivel de precio de la vivienda comparable (€/m²) | datasets pedidos (prc_hpi_a es índice 2015=100) | No existe un nivel en los datasets solicitados; no se probaron otros | Sobrecarga y alquiler como aproximaciones de asequibilidad |
