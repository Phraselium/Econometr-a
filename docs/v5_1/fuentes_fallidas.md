# Fuentes fallidas v5.1

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba y error.


## T2 (viviendas liberadas por envejecimiento) — prueba 2026-10-11
| Fuente | Endpoint / prueba | Resultado | Uso alternativo |
|---|---|---|---|
| Censo 2021: hogares unipersonales y de pareja por edad del sustentador | WS-Tempus `TABLAS_OPERACION/8` y `/463`, `/70` (Censo, Proyeccion de Hogares): sin tabla de hogares por edad de la persona de referencia | SIN DATO | Tasa de jefatura 65+ de v4/M2 (como B1) |
| Censo 2021 / IMSERSO: poblacion en establecimientos colectivos por edad | Mismo listado: sin tabla; IMSERSO no consultado (sin enlace verificado) | SIN DATO | Supuestos C4 (4-8 % de 75+ en residencia), NO VERIFICADOS |
| Seguimiento de la vivienda heredada (venta/alquiler posterior) | INE ETDP 6154 solo cuenta transmisiones por titulo | NO EXISTE | Rango con X de vacias y secundarias del Censo 2021 |

## T1 · bajas del parque (probado 2026-10-11)
| Fuente | Endpoint | Edición | Fecha | Resultado |
|---|---|---|---|---|
| Licencias de obra, nivel provincial | https://apps.fomento.gob.es/BoletinOnline/?nivel=2&orden=10000000 (bloque 1: tablas 1-10 nacionales y 1002NN10/20/30 por CCAA) | Boletín Online, modificaciones dic-2025 | 2026-10-11 | No hay desglose provincial; solo nacional y CCAA. Reparto provincial por parque (no es medida) |
| Licencias de obra, CCAA | .../sedal/1002NN30.XLS (NN=01..19) | modificadas 2023 | 2026-10-11 | Serie hasta 2022 (Ceuta y Melilla hasta 2019, sin demolición). 2023-2024 con cuota media 2019-2022 y 2025 sin dato |
| Licencias de obra, 2025 | .../sedal/10010600.XLS y 10011000.XLS | dic-2025 | 2026-10-11 | Último año anual: 2024 |
| Ruina, cambios de uso, agregaciones | no localizado endpoint | — | 2026-10-11 | SIN DATO; INE ECE, censo de edificios ruinosos y registros autonómicos no probados |

## T6 · BK-014 alquiler de temporada y por habitaciones; BK-017 MESVAL (probado 2026-10-11)
| Fuente | Endpoint / fichero probado | Edición | Fecha de la prueba | Resultado |
|---|---|---|---|---|
| (a) INE, viviendas turísticas (estadística experimental) | https://www.ine.es/jaxiT3/Tabla.htm?t=39363 (HTTP 200) y tabla 39364 (ya en data/raw/ine_v2_vut.csv) | Tabla 39363 vigente | 2026-10-11 | Plazas y viviendas turísticas por municipio; sin duración de contrato ni alquiler de temporada. Sin serie oficial utilizable |
| (b) Registro Único de Arrendamientos (Ministerio de Vivienda) | https://www.mivau.gob.es/vivienda/registro-unico-de-arrendamientos (HTTP 403 con curl y con WebFetch); búsqueda web sin página estadística oficial localizada | RD 1312/2024, vigente desde 2025-01-02 | 2026-10-11 | BLOQUEADO (403). No se localizó tabla agregada de contratos de temporada o corta duración. Solicitud S6 |
| (c) Incasòl (Cataluña), fianzas de lloguer | https://analisi.transparenciacatalunya.cat/api/views/qww9-bvhh.json (Preu mitjà del lloguer per municipi) y hepw-33ik (àmbits supramunicipals) | Actualizado 2026-07-30 | 2026-10-11 | Columnas: ámbito, código, nombre, año, periodo, habitatges, renda, tram_preus. Sin duración del contrato. Idescat (paae) responde 301 y no se siguió |
| (c) GVA (C. Valenciana), fianzas | https://dadesobertes.gva.es/api/3/action/package_show?id=viv-reg-fia-2026 (CSV del recurso b7253c3d-...) | 2020-2026; última modificación 2026-10-10 | 2026-10-11 | Cabecera: anyo_datos; cod_provincia; provincia; cod_municipio; municipio; cp; importe_fianza; devuelta. Sin duración. Confirma A23 |
| (c) Euskadi, EMAL (Gobierno Vasco) | https://www.euskadi.eus/ficha-metodologica-de-la-estadistica-del-mercado-de-alquiler-ema/y22-bilaar/es/ | Ficha con última modificación 2024-07-04; periodicidad contradictoria (anual o semestral) | 2026-10-11 | Fianzas de vivienda habitual, de temporada y de locales en un mismo agregado, sin categoría separada; sin duración; difusión «bajo petición»; sin formato ni licencia de descarga. Inutilizable como serie de temporada |
| (c) Madrid (Agencia de Vivienda Social), Baleares (IBAVI) | https://datos.madrid.es/egob/catalogo/?q=alquiler+temporada (HTTP 404); búsqueda web sin resultados de fianzas con duración | — | 2026-10-11 | NO LOCALIZADO. Sin endpoint verificado |
| (d) Ayuntamiento de Barcelona, datos abiertos | https://opendata-ajuntament.barcelona.cat/data/api/3/action/package_search?q=lloguer (y temporada, habitatges turistics) | — | 2026-10-11 | Sin datasets de alquiler de temporada ni por habitaciones (4, 1 y 1 resultados no relacionados). Otro endpoint (opendata.barcelona.cat) responde 400 |
| (d) València, datos abiertos | https://dadesobertes.gva.es/api/3/action/package_search?q=alquiler (8 resultados) | — | 2026-10-11 | Solo fianzas y viviendas del patrimonio público adjudicadas; sin temporada ni habitaciones |
| MESVAL (BK-017) | Sin descarga: usa datos privados de un portal inmobiliario (Fotocasa), según docs/v5/backlog.md BK-017 y docs/v3/estado.md:7 | — | 2026-10-11 | No replicable con fuentes abiertas. Sin prueba de red |

Estado T6: NO ANALIZADA: FALTAN DATOS. Ninguna serie oficial con duración del contrato o modalidad por habitaciones es utilizable. Solicitudes que lo resolverían: S4 (registros autonómicos de fianzas con duración, tipo de arrendador y tramos de tamaño) y S6 (Registro Único de Arrendamientos: agregados de corta duración y de temporada por municipio). Ver docs/v5/solicitudes.md.
