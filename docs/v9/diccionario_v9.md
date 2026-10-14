# Diccionario de datos V9 (data/raw/v9)

Fecha: 2026-10-14. Solo datos descargados y validados; ninguna variable se ha usado todavía en un modelo.

- **Capa prevista.** Es la capa máxima a la que podría llegar un resultado construido con la variable, según el diseño de docs/v9_prep/plan_v9.md. No la asigna el dato en sí.
- **Códigos territoriales.** Texto con ceros a la izquierda: municipio, 5 dígitos INE; sección, 10 dígitos (municipio y distrito-sección); provincia, 2 dígitos.
- **Licencias.** En data/raw/v9/<fuente>/_manifest.csv.

## EMAL Euskadi: `emal/emal_largo.csv` (CC BY 4.0, Gobierno Vasco)

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| periodo | trimestre (aaaaTn), año o `vigente_<fecha>[_estadístico]` | Fecha de inicio del contrato; `vigente_*` = stock de contratos vigentes a esa fecha (media, mediana, P25 y P75 cuando la tabla los da) | — |
| nivel | texto | territorio, municipio (>20.000 hab.), agrupacion (estratos de tamaño), zona (distrito/barrio de las capitales (código de la fuente; véase correspondencia_zonas_distrito.csv) | — |
| codigo_ine | 5 dígitos | Municipio INE cuando la fila es municipal | — |
| tipo_contrato | nuevo / vigente | Contratos iniciados en el periodo frente a stock vigente | — |
| variable | n_fianzas, renta_mensual_eur, renta_eur_m2_construido | Número de fianzas depositadas; renta mensual media (€/mes); renta por m² construido (€/m²/mes) | C1 si se triangula con SERPAVI; C3 en DiD de zonas tensionadas |
| valor | según variable | Valor publicado | — |
| posterior_prereg | booleano | Fila de 2026T3 o posterior (no se usa) | — |

- **Hojas no convertidas.** Las hojas A1-A2.4 (desglose del stock vigente por tipo de contrato a 31-12-2025) siguen solo en el XLSX original.
- **Cuadre.** Euskadi = Álava + Gipuzkoa + Bizkaia en T2.1 para los diez años (test).

## INE, Censo anual de población

`ine_censo_anual/censo_seccion_pais.csv.gz` y `censo_municipio_sexo.csv.gz` (INE, reutilización con cita):

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| edicion | año | Población a 1 de enero (2021-2025) | — |
| cod_provincia, cod_municipio, cod_seccion | códigos INE | Sección censal de 10 dígitos en las filas de nivel `seccion` | — |
| nivel | provincia / municipio / seccion | — | — |
| pais_nacionalidad | 22 categorías INE | Total, España, Francia, Reino Unido, Rumanía, Ucrania, Marruecos, Colombia, Venezuela, China…, «Otros países de …», Apátridas | C1 (recuento oficial); insumo de shift-share (C3 posible) |
| poblacion | personas | Población censada | C1 |
| sexo (solo municipio) | Total / Hombres / Mujeres | — | C1 |

Cuadres (tests):
- la suma de las provincias es igual al total nacional publicado (tabla 68065), 2021-2025;
- las secciones suman su municipio en los 40.660 pares municipio-edición;
- no hay claves duplicadas.

## INE, IPVA por antigüedad del contrato y por distrito: `ine_ipva/*.csv`

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| Antigüedad del contrato | nuevos / existentes / total | Contratos con un año o menos de vigencia frente al resto (tablas 59004 y 59005) | C1 con SERPAVI y fianzas |
| Distritos | código del INE | Distritos de las capitales de provincia (tabla 59061) | C1 |
| Tipo de dato | índice (2015 = 100), variación anual, euros/m² | Según la tabla | — |
| periodo, valor | año, valor | 2015-2024 | — |

## Registro de viviendas turísticas de la GVA: `gva_vut/` (CC BY 4.0)

| Fichero o variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| cortes/vut_*.csv.gz | registro | Cortes del registro: histórico (2025-01-26), último periodo (2025-01-26) y actual (2026-10-14). Incluyen signatura, municipio, código postal, dirección, referencia catastral, plazas, superficie y fecha de alta | C1 (registro oficial) |
| gva_vut_panel_municipio.csv: ine5, tipo, fecha, stock | viviendas | Stock por municipio: `corte` (fecha del corte) o `mensual_reconstruido` (altas y bajas fechadas; véase gva_vut/LEEME.md) | C1 en corte; C4 el reconstruido (supuesto de fechado) |
| gva_vut_panel_cp.csv | viviendas | Igual, por código postal (`-----` = sin código postal) | C4 |

- El código `03000` agrupa registros sin municipio asignado. Su stock es nulo en los cortes recientes.
- El corte de 2026 no trae bajas: las posteriores a enero de 2025 no se pueden fechar.

## Inside Airbnb: `insideairbnb/` (CC BY 4.0, no oficial)

| Fichero o variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| insideairbnb_seccion.csv.gz | anuncios | Por ciudad, edición y sección censal: anuncios por tipo (vivienda entera, habitación privada, compartida, hotel), con licencia, disponibilidad media a 365 días y reseñas en 12 meses | C4 (solo robustez frente al INE VUT y al registro de la GVA) |
| insideairbnb_barrio.csv.gz | anuncios | Lo mismo por barrio de Inside Airbnb (no es código INE) | C4 |
| calendar_resumen_*, reviews_resumen_* | noches, reseñas | Por anuncio y mes. El precio no viene en estas ediciones | C4 |
| listings_*.csv.gz | anuncio | Ficheros completos (no versionados: contienen datos de anfitriones) | — |

Ediciones: València 2026-09-20, Barcelona y Madrid 2026-09-17, Málaga 2026-09-28 y Mallorca 2026-09-19. Las históricas no son públicas.

## Eurostat, alojamiento vía plataformas: `eurostat_plataformas/tour_ce_*.csv.gz` (CC BY 4.0)

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| dataset | — | tour_ce_oan3 (NUTS 3 anual), tour_ce_omn12 (NUTS 1-2 mensual), tour_ce_omr (país mensual), tour_ce_oam, tour_ce_oasc | — |
| geo, periodo | código NUTS, periodo | 2018-2025/2026 | — |
| indicador | código Eurostat | noches pasadas (NGT_SP), estancias (STY) y duración media (LSTY), por residencia y mes; NUTS 3 solo noches (NGT_SP) | C1 (estadística oficial con datos de 4 plataformas; ruptura en 2025) |
| valor, bandera | número | — | — |

## BCE, tipos y volúmenes hipotecarios: `bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz`

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| pais | ISO-2 | 21 países de la zona euro | — |
| fijacion_codigo | F, I, O, P, K, AM, A_volumen | Tipo variable o fijación ≤1 año (F); 1-5 años (I); 5-10 años (O); >10 años (P); >1 año (K); coste total de financiación (AM). A_volumen = volumen de nuevas operaciones, solo total | Exposición al tipo variable por país: insumo de diseño en panel (C3 posible con shocks del BCE) |
| periodo | mes | 2003-01 a 2026-08 | — |
| valor | % anual (tipos) o millones de euros (volumen) | Nuevas operaciones de préstamos a hogares para vivienda | C1 |

## Incasòl, fianzas de Cataluña: `incasol/incasol_qww9-bvhh_actual.csv.gz`

No versionado: «términos de uso»; se obtiene con `make datos_terceros` o `make datos_v9`.

| Variable | Unidad | Definición | Capa prevista |
|---|---|---|---|
| codi_territorial | 5 dígitos INE | Municipio | — |
| any, periode, periodo_iso | año, trimestre | 2007-2026T1 | — |
| habitatges | contratos | Contratos nuevos (fianzas) por tramo de precio | C1 con SERPAVI; C3 en DiD de zonas tensionadas |
| renda | €/mes | Renta media | C1 |
| tram_preus | texto | Tramo de renta | — |
| posterior_prereg | booleano | 2026T3 o posterior (no se usa) | — |

## Fianzas GVA: `gva_fianzas/`

- La versión actual (2020-2026) es **idéntica** byte a byte a la copia del proyecto (data/raw/v5).
- Solo se versiona comparacion_v5.csv; los CSV, no, porque ya están en data/raw/v5.

## Microdatos INE (EPA 2018T1-2026T2; ECV 2018-2025): `ine_microdatos/`

ZIP originales del INE con su diseño de registro. No versionados por tamaño.
- **EPA:** individuos, con edad, relación con la persona de referencia, actividad y nacionalidad. Sirve para la emancipación, en el diseño del Bono Alquiler Joven (C3 posible por discontinuidad de edad).
- **ECV:** hogares, con régimen de tenencia y alquiler pagado. Sirve para la carga de vivienda.
