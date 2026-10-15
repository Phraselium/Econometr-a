# Diccionario de la base única (V10)

Generado por `src/v10/base.py` (`make base`); no editar a mano.

## Tablas

| tabla | contenido |
|---|---|
| hechos | tabla larga: una fila por territorio, periodo, variable y desagregación |
| territorios | dimensión territorial con jerarquía (padre_codigo, padre_nivel) |
| variables | definición, unidad, capa, fuente, licencia y cobertura de cada variable |
| cifras_clave | copia tipada de publicacion/cifras_clave.csv |
| regulacion_zonas | declaraciones de zona tensionada (data/raw/v9/regulacion) |
| hechos_publica (vista) | filas redistribuibles; es lo único que se publica en data/base/publica y en la web |

## Columnas de `hechos`

| columna | definición |
|---|---|
| territorio_codigo | código INE (nacional 00; CCAA 2; provincia 2; municipio 5; distrito 7; barrio de València 9 = municipio + distrito + barrio; sección 10). Excepciones: `pais` (ISO-2) y `nuts3` (Eurostat) |
| nivel | nacional, ccaa, provincia, municipio, distrito, barrio, seccion, pais, nuts3 |
| periodo | AAAA (anual), AAAATn (trimestral), AAAA-MM (mensual), AAAASn (semestral), AAAA-MM-DD (corte) |
| frecuencia | A, T, M, S, D |
| variable | nombre de la variable (tabla `variables`) |
| desagregacion | dimensión adicional `clave=valor` (nacionalidad, antigüedad del contrato, fijación…); vacía si no hay |
| valor | valor numérico |
| unidad, fuente, capa, licencia, redistribuible | de la tabla `variables` |
| edicion | edición o fecha de descarga del fichero de origen |
| fecha_dato | último día del periodo al que se refiere el dato |
| metodo_dato | observado, interpolado, agregado, reconstruido… (banderas `_metodo` de los paneles) |
| origen | fichero de data/processed o data/raw/v9 del que sale la fila |
| posterior_prereg | True si el periodo empieza el 2026-07-01 o después (evaluate_v7/evaluate_v8): se muestra, pero no entra en cálculos |
| muestra_sellada_v6 | True en las provincias del sellado transversal de v6 (informativo) |

## Resumen

- filas_publica: 14028906
- territorios: 56579
- filas_posterior_prereg: 301342
- variables_publicas: 297
- filas públicas por nivel: barrio 2408, ccaa 47980, distrito 587783, municipio 5159904, nacional 8833, nuts3 1440, pais 53350, provincia 294751, seccion 7872457

Las discrepancias entre paneles son claves presentes en varios ficheros procesados con valores distintos; se conserva el panel más reciente (v8 > v7 > v1), que es el que usan las publicaciones vigentes.

## Variables

| variable | definición | unidad | capa | fuente | redistribuible | niveles | periodo |
|---|---|---|---|---|---|---|---|
| `adrh_gini` | INE, ADRH | índice | C4 | INE, ADRH | sí | seccion | 2019–2023 |
| `adrh_renta_neta_hogar` | INE, ADRH | €/año | C4 | INE, ADRH | sí | seccion | 2019–2023 |
| `adrh_renta_neta_persona` | INE, Atlas de distribución de renta de los hogares (ADRH) | €/año | C4 | INE, Atlas de distribución de renta de los hogares (ADRH) | sí | seccion | 2019–2023 |
| `aeat_irpf_declaraciones` | AEAT, estadística de declarantes del IRPF por municipios | declaraciones | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `aeat_irpf_renta_bruta_media` | AEAT, estadística de declarantes del IRPF por municipios | € | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `aeat_irpf_renta_disponible_media` | AEAT, estadística de declarantes del IRPF por municipios | € | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `aeat_irpf_rentas_inmuebles_importe` | AEAT, estadística de declarantes del IRPF por municipios | € | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `aeat_irpf_rentas_inmuebles_media` | AEAT, estadística de declarantes del IRPF por municipios | € | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `aeat_irpf_rentas_trabajo_importe` | AEAT, estadística de declarantes del IRPF por municipios | € | C4 | AEAT, estadística de declarantes del IRPF por municipios | sí | municipio | 2016–2024 |
| `asilo_solicitantes` | Eurostat, migr_asyappctzm (solicitantes de protección internacional, total de solicitudes) | personas | C4 | Eurostat, migr_asyappctzm (solicitantes de protección internacional, total de solicitudes) | sí | nacional | 2008-01–2026-07 |
| `bce_cuota_tipo_variable` | BCE, RAI (SVLHPHH): nuevos préstamos de vivienda a tipo variable o fijación ≤1 año | % de nuevos préstamos | C4 | BCE, RAI (SVLHPHH): nuevos préstamos de vivienda a tipo variable o fijación ≤1 año | sí | pais | 2003-01–2026-08 |
| `bce_hip_tipo_nuevas` | BCE, MIR (nuevas operaciones de vivienda) | % anual | C4 | BCE, MIR (nuevas operaciones de vivienda) | sí | pais | 2003-01–2026-08 |
| `bce_hip_volumen_nuevas` | BCE, MIR | millones de euros | C4 | BCE, MIR | sí | pais | 2003-01–2026-08 |
| `bls_criterios_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, criterios de concesión (oferta), índice de difusión | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ST.S.DINX) | sí | nacional | 2003T1–2026T2 |
| `bls_criterios_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, criterios de concesión (oferta), porcentaje neto (endurecimiento menos relajación) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ST.S.FNET) | sí | nacional | 2003T1–2026T2 |
| `bls_demanda_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, demanda de préstamos, índice de difusión | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ZZ.D.DINX) | sí | nacional | 2003T1–2026T2 |
| `bls_demanda_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, demanda de préstamos, porcentaje neto | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ZZ.D.FNET) | sí | nacional | 2003T1–2026T2 |
| `bls_rechazo_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, solicitudes rechazadas, índice de difusión (desde 2015T2) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.RA.D.DINX) | sí | nacional | 2015T2–2026T2 |
| `bls_rechazo_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, solicitudes rechazadas, porcentaje neto (desde 2015T2) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.RA.D.FNET) | sí | nacional | 2015T2–2026T2 |
| `c21md_hogares_muestra` | INE, Censo 2021, microdatos de personas (recuento muestral) | hogares (muestra 10 %) | C4 | INE, Censo 2021, microdatos de personas (recuento muestral) | sí | municipio | 2021-01-01–2021-01-01 |
| `catastro_inspire_edificios` | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | edificios | C4 | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | sí | barrio,seccion | 2026-08-21–2026-08-21 |
| `catastro_inspire_inmuebles` | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | inmuebles | C4 | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | sí | barrio,seccion | 2026-08-21–2026-08-21 |
| `catastro_inspire_superficie_construida_m2` | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | m² | C4 | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | sí | barrio,seccion | 2026-08-21–2026-08-21 |
| `catastro_inspire_viviendas` | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | viviendas | C4 | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | sí | barrio,seccion | 2026-08-21–2026-08-21 |
| `catastro_inspire_viviendas_por_antiguedad` | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | viviendas | C4 | Catastro, INSPIRE Buildings (agregado espacial propio a sección INE) | sí | barrio,seccion | 2026-08-21–2026-08-21 |
| `catastro_tit_titulares` | Catastro, estadística de titularidad (padrón IBI urbano, uso residencial) | titulares (sujetos pasivos) | C4 | Catastro, estadística de titularidad (padrón IBI urbano, uso residencial) | sí | municipio | 2024–2026 |
| `catastro_tit_viviendas` | Catastro, estadística de titularidad (padrón IBI urbano, uso residencial) | inmuebles residenciales | C4 | Catastro, estadística de titularidad (padrón IBI urbano, uso residencial) | sí | municipio | 2024–2026 |
| `catastro_titulares_jaxi` | Catastro, titulares por municipio y clase (visor JAXI; 2012-2023) | titulares | C4 | Catastro, titulares por municipio y clase (visor JAXI; 2012-2023) | sí | municipio | 2012–2023 |
| `catastro_unidades_urbanas_residenciales` | Dirección General del Catastro, estadísticas catastrales (urbana) | inmuebles | C4 | Dirección General del Catastro, estadísticas catastrales (urbana) | sí | municipio | 2012–2026 |
| `catastro_unidades_urbanas_total` | Dirección General del Catastro, estadísticas catastrales (urbana) | inmuebles | C4 | Dirección General del Catastro, estadísticas catastrales (urbana) | sí | municipio | 2012–2026 |
| `catastro_viviendas_por_anio_construccion` | Catastro, otras estadísticas (2019): viviendas por año de construcción | viviendas | C4 | Catastro, otras estadísticas (2019): viviendas por año de construcción | sí | municipio | 2019–2019 |
| `catastro_viviendas_por_anio_reforma` | Catastro, otras estadísticas (2019): viviendas por año de reforma | viviendas | C4 | Catastro, otras estadísticas (2019): viviendas por año de reforma | sí | municipio | 2019–2019 |
| `censo2011_viviendas` | INE, Censo de Población y Viviendas 2011 (3457) | viviendas | C4 | INE, Censo de Población y Viviendas 2011 (3457) | sí | provincia | 2011–2011 |
| `censo2021_t10_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t11_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t12_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t13_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t14_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t15_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t16_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t17_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t17_2` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t17_3` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t17_4` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t17_5` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t18_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t19_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t19_2` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t1_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t20_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t20_2` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t20_3` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t21_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t22_1` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t22_2` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t22_3` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t22_4` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t22_5` |  | viviendas u hogares | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t2_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t2_2` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t3_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t4_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t4_2` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t4_3` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t5_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t6_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t7_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t8_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `censo2021_t9_1` |  | % | C4 | INE, Censo de Población y Viviendas 2021 (indicadores por sección) | sí | seccion | 2021–2021 |
| `compraventas` | Compraventas de viviendas ETDP, total (anual = suma) | número | C4 | INE ETDP 6150, desglose total | sí | ccaa,nacional,provincia | 2007–2026T2 |
| `compraventas_ine` | Compraventas de vivienda, total nacional (ETDP, INE), suma trimestral | número | C4 | ine_etdp_compraventas.csv (ETDP1826) | sí | nacional | 2007T1–2026T2 |
| `compraventas_sa` |  | número (SA) | C4 | Derivada (STL) | sí | nacional | 2007T1–2026T2 |
| `costes` |  | índice 2021=100 | C4 | Eurostat, sts_copi_q (coste de construcción residencial) | sí | nacional | 1995T1–2026T2 |
| `costes_constr` | Índice de costes de construcción de edificios residenciales, España (Eurostat sts_copi_q, 2021=100, sin ajustar) | índice 2021=100 | C4 | eurostat_costes.csv | sí | nacional | 1995T1–2026T2 |
| `credito_construccion` | Saldo de crédito de entidades de crédito a construcción (promotores y constructoras), fin de trimestre | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv (D_MEE61010) | sí | nacional | 1995T1–2026T2 |
| `credito_inmobiliario` | Saldo de crédito de entidades de crédito a actividades inmobiliarias (promotores y constructoras), fin de trimestre | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv (D_MEE61013) | sí | nacional | 1995T1–2026T2 |
| `credito_nuevo` | Nuevo crédito a la vivienda (volumen de nuevas operaciones), España, suma trimestral | millones de euros | C4 | ecb_nuevo_credito_vivienda_es.csv | sí | nacional | 2003T1–2026T2 |
| `credito_promotor` | Crédito a construcción + actividades inmobiliarias (proxy de crédito a promotores) | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv | sí | nacional | 1995T1–2026T2 |
| `credito_stock` |  | M€ (stock) | C4 | BCE BSI, stock crédito vivienda | sí | nacional | 2003T1–2026T2 |
| `credito_stock_bde` | Saldo de crédito a la vivienda de hogares, entidades de crédito (BdE be1916), fin de trimestre (primer dato 1997T3) | millones de euros | C1 | bde_credito_finalidad.csv (DF_MESNAA22A1U62251Z01E) | sí | nacional | 1997T3–2026T2 |
| `credito_stock_ecb` | Saldo vivo de crédito a la vivienda, IFM España (BCE BSI), fin de trimestre | millones de euros | C1 | ecb_stock_credito_vivienda_es.csv | sí | nacional | 2003T1–2026T2 |
| `deflactor` |  | índice 2020=100 | C4 | Derivada: INE CNT (SA) | sí | nacional | 1995T1–2026T2 |
| `dif_hip_euribor_bce` | Diferencial tipo hipotecario BCE - Euríbor 1 año | puntos porcentuales | C4 | BCE, MIR y Euríbor (diferencia propia) | sí | nacional | 2003T1–2026T2 |
| `dif_hip_euribor_bde` | Diferencial tipo hipotecario BdE - Euríbor 1 año | puntos porcentuales | C4 | BdE, tipo hipotecario y Euríbor (diferencia propia) | sí | nacional | 1995T1–2026T2 |
| `ecp_pob_nacionalidad` | INE, Estadística Continua de Población (56947, 82104; trimestral) | personas | C4 | INE, Estadística Continua de Población (56947, 82104; trimestral) | sí | provincia | 2002-01-01–2026-07-01 |
| `ecp_pob_viv_familiares_nacionalidad` | INE, ECP (60129; población en viviendas familiares) | personas | C4 | INE, ECP (60129; población en viviendas familiares) | sí | provincia | 2021-01-01–2026-07-01 |
| `em_emigracion_extranjero` | INE, Estadística de Migraciones (24326) | personas | C4 | INE, Estadística de Migraciones (24326) | sí | provincia | 2008–2021 |
| `em_inmigracion_extranjero` | INE, Estadística de Migraciones (24323) | personas | C4 | INE, Estadística de Migraciones (24323) | sí | provincia | 2008–2021 |
| `em_saldo_interprovincial` | INE, Estadística de Migraciones (24385) | personas | C4 | INE, Estadística de Migraciones (24385) | sí | provincia | 2008–2021 |
| `emal_n_fianzas` | Gobierno Vasco, EMAL (fianzas) | contratos | C4 | Gobierno Vasco, EMAL (fianzas) | sí | municipio | 2016T1–2025T4 |
| `emal_renta_eur_m2_construido` | Gobierno Vasco, EMAL | €/m²/mes | C4 | Gobierno Vasco, EMAL | sí | municipio | 2016T1–2025T4 |
| `emal_renta_mensual_eur` | Gobierno Vasco, EMAL | €/mes | C4 | Gobierno Vasco, EMAL | sí | municipio | 2016T1–2025T4 |
| `emcr_md_altas_interno` | INE, EMCR (microdatos 2021-2024; agregado propio) | personas | C4 | INE, EMCR (microdatos 2021-2024; agregado propio) | sí | municipio | 2021–2024 |
| `emcr_md_bajas_interno` | INE, EMCR (microdatos 2021-2024; agregado propio) | personas | C4 | INE, EMCR (microdatos 2021-2024; agregado propio) | sí | municipio | 2021–2024 |
| `emcr_md_emigracion_exterior` | INE, EMCR (microdatos; migraciones exteriores) | personas | C4 | INE, EMCR (microdatos; migraciones exteriores) | sí | municipio | 2021–2024 |
| `emcr_md_inmigracion_exterior` | INE, EMCR (microdatos; migraciones exteriores) | personas | C4 | INE, EMCR (microdatos; migraciones exteriores) | sí | municipio | 2021–2024 |
| `emcr_md_saldo_interno` | INE, EMCR (microdatos 2021-2024; agregado propio) | personas | C4 | INE, EMCR (microdatos 2021-2024; agregado propio) | sí | municipio | 2021–2024 |
| `emcr_saldo` | INE, Estadística de Migraciones y Cambios de Residencia (69764) | personas | C4 | INE, Estadística de Migraciones y Cambios de Residencia (69764) | sí | provincia | 2021–2024 |
| `emcr_saldo_municipal` | INE, EMCR, tabla 69767 (saldos por municipio) | personas | C4 | INE, EMCR, tabla 69767 (saldos por municipio) | sí | municipio | 2021–2024 |
| `epa_pob_total` |  | miles (todas las edades) | C4 | INE EPA, tabla 65285 | sí | ccaa | 2007T1–2026T2 |
| `euribor` |  | % anual | C4 | BCE, Euribor 1 año | sí | nacional | 1995T1–2026T3 |
| `euribor_1y` | Euríbor a 1 año, media trimestral | % anual | C4 | ecb_euribor1y.csv | sí | nacional | 1995T1–2026T2 |
| `euribor_3m` | Euríbor a 3 meses, media trimestral | % anual | C4 | v8/ecb_tipos_euribor3m_depo.csv | sí | nacional | 1995T1–2026T2 |
| `eurostat_plataformas_noches` | Eurostat, tour_ce_oan3 (plataformas colaborativas) | noches | C4 | Eurostat, tour_ce_oan3 (plataformas colaborativas) | sí | nuts3 | 2018–2025 |
| `evr_altas_interno` | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | personas | C4 | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | sí | municipio | 1988–2021 |
| `evr_bajas_interno` | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | personas | C4 | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | sí | municipio | 1988–2021 |
| `evr_emigracion_exterior` | INE, EVR (microdatos; altas desde y bajas al extranjero) | personas | C4 | INE, EVR (microdatos; altas desde y bajas al extranjero) | sí | municipio | 1988–2021 |
| `evr_inmigracion_exterior` | INE, EVR (microdatos; altas desde y bajas al extranjero) | personas | C4 | INE, EVR (microdatos; altas desde y bajas al extranjero) | sí | municipio | 1988–2021 |
| `evr_saldo_interno` | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | personas | C4 | INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio) | sí | municipio | 1988–2021 |
| `fianzas_importe_media` | Importe medio de la fianza | euros | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `fianzas_importe_mediana` | Importe mediano de la fianza (proxy de una mensualidad de alquiler) | euros | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `fianzas_n` | Fianzas de arrendamiento depositadas en la GVA (número de contratos), por provincia y año | número | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `hicp_alquiler_indice` | Eurostat, prc_hicp_minr (CP041, alquileres efectivos) | índice 2015=100 | C4 | Eurostat, prc_hicp_minr (CP041, alquileres efectivos) | sí | pais | 1996-01–2026-08 |
| `hip_importe` | Importe de hipotecas sobre viviendas | miles de euros | C4 | INE Hipotecas, hipotecas_viviendas_importe | sí | ccaa,provincia | 2003–2026T2 |
| `hip_n` | Hipotecas constituidas sobre viviendas, número | número | C4 | INE Hipotecas, serie HPT por provincia, hipotecas_viviendas_numero | sí | ccaa,provincia | 2003–2026T2 |
| `hogares_ecp` | Hogares en viviendas familiares (ECP, proyección/estimación INE), total nacional | miles de hogares | C1 | ine_hogares_60131.csv (ECP355533) | sí | nacional | 2021T1–2026T2 |
| `hogares_epa` | Hogares (EPA), total nacional | miles de hogares | C1 | ine_epa_hogares.csv (EPA430446) | sí | nacional | 2002T1–2026T2 |
| `hpi_es_eurostat` | Índice de precios de la vivienda Eurostat (total, 2015=100), ES | índice 2015=100 | C1 | v8/eurostat_prc_hpi_q_multi.csv | sí | nacional | 2005T4–2026T2 |
| `hpi_eurostat` |  | índice 2015=100 | C4 | Eurostat, prc_hpi_q | sí | nacional | 2005T4–2026T2 |
| `iab_disponibilidad_365_media` |  | días | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_anuncios` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_con_licencia` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_entire_home` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_hotel_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_private_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_shared_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_resenas_ultimos_12m` |  | reseñas | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `idescat_apartamentos_n` | IDESCAT, turall: apartamentos turísticos | establecimientos | C4 | IDESCAT, turall: apartamentos turísticos | sí | municipio | 2015–2025 |
| `idescat_apartamentos_plazas` | IDESCAT, turall: apartamentos turísticos | plazas | C4 | IDESCAT, turall: apartamentos turísticos | sí | municipio | 2015–2025 |
| `idescat_hut_n` | IDESCAT, Estadística de establecimientos turísticos (turall): HUT | viviendas | C4 | IDESCAT, Estadística de establecimientos turísticos (turall): HUT | sí | municipio | 2015–2025 |
| `idescat_hut_plazas` | IDESCAT, turall: HUT | plazas | C4 | IDESCAT, turall: HUT | sí | municipio | 2015–2025 |
| `ine_tmov_interno_turistas` | INE, turismo interno medido con teléfonos móviles (53464; experimental) | turistas | C4 | INE, turismo interno medido con teléfonos móviles (53464; experimental) | sí | municipio | 2019-07–2026-08 |
| `ine_tmov_receptor_turistas` | INE, turismo receptor medido con teléfonos móviles (52048; experimental) | turistas | C4 | INE, turismo receptor medido con teléfonos móviles (52048; experimental) | sí | municipio | 2019-07–2025-12 |
| `ine_vut_plazas` | INE, viviendas turísticas (experimental) | plazas | C4 | INE, viviendas turísticas (experimental) | sí | distrito,seccion | 2021-02–2026-05 |
| `ine_vut_porcentaje_vivienda_turistica` | INE, viviendas turísticas (experimental) | % de viviendas | C4 | INE, viviendas turísticas (experimental) | sí | distrito,seccion | 2021-02–2026-05 |
| `ine_vut_vivienda_turistica` | INE, Medición del número de viviendas turísticas (experimental) | viviendas | C4 | INE, Medición del número de viviendas turísticas (experimental) | sí | distrito,seccion | 2021-02–2026-05 |
| `inflacion_deflactor` |  | % interanual | C4 | INE, CNT (deflactor; cálculo propio) | sí | nacional | 1996T1–2026T2 |
| `inflacion_ipc_yoy` | Inflación interanual = 100 x (ln IPC_t - ln IPC_t-4) | % (puntos log) | C4 | derivada de ipc_general | sí | nacional | 1996T1–2026T2 |
| `iniciadas` |  | viviendas | C4 | MIVAU, viviendas libres iniciadas | sí | provincia | 2008–2026T2 |
| `iniciadas_anual_tabla` |  | viviendas | C4 | MIVAU, viviendas libres iniciadas (tabla anual) | sí | provincia | 2002–2024 |
| `inmig_anual` | Inmigración anual desde el extranjero, total (Eurostat migr_imm1ctz), valor anual asignado a cada trimestre del año | personas/año | C4 | eurostat_inmigracion_anual.csv (A/TOTAL/REACH/TOTAL/NR/T/ES) | sí | nacional | 1998T1–2024T4 |
| `inmig_anual_eurostat` |  | personas (flujo anual) | C4 | Eurostat migr_imm1ctz (inmigración anual, ciudadanía TOTAL) | sí | nacional | 1998–2024T4 |
| `ipc_alquiler` | IPC, alquiler de vivienda, nacional (índice; media trimestral de los 3 índices mensuales) | índice (base INE) | C4 | ine_ipc_alquiler.csv (IPC290887) | sí | ccaa,nacional | 2002T1–2026T2 |
| `ipc_alquiler_indice` |  | índice 2021=100 | C4 | INE, IPC de alquiler por provincia | sí | provincia | 2002–2026T2 |
| `ipc_alquiler_yoy` |  | % interanual | C4 | INE IPC, subclase alquiler de vivienda | sí | nacional,provincia | 2002–2026T2 |
| `ipv` | Índice de precios de vivienda INE, general, nacional (base 2015=100) | índice | C1/C4 | ine_ipv_80270.csv (IPV1209) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipv15` |  | índice | C4 | INE IPV, tabla 25171 (base 2015, robustez) | sí | nacional | 2007T1–2025T4 |
| `ipv_nueva` | IPV INE, vivienda nueva, nacional | índice | C4 | ine_ipv_80270.csv (IPV1613) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipv_usada` | IPV INE, vivienda segunda mano, nacional | índice | C4 | ine_ipv_80270.csv (IPV1618) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipva` |  | índice | C4 | INE, IPVA municipal (59060) | sí | municipio | 2011–2024 |
| `ipva_indice` | Índice de precios de vivienda en alquiler (IPVA, base SERPAVI), total; 48 provincias, desde 2011; stock | índice 2015=100 | C4 | INE, Índice de Precios de Vivienda en Alquiler (59004, 59005, 59061) | sí | ccaa,distrito,nacional,provincia | 2011–2024 |
| `ipva_tam_indice` | INE, IPVA por municipio y distrito (59060, 59061) por tamaño de la vivienda | índice 2015=100 | C4 | INE, IPVA por municipio y distrito (59060, 59061) por tamaño de la vivienda | sí | distrito,municipio | 2011–2024 |
| `ipva_tam_var_anual` | INE, IPVA por municipio y distrito (59060, 59061) | % | C4 | INE, IPVA por municipio y distrito (59060, 59061) | sí | distrito,municipio | 2012–2024 |
| `ipva_var_anual` | INE, IPVA | % | C4 | INE, IPVA | sí | ccaa,distrito,nacional,provincia | 2012–2024 |
| `mnp_defunciones` | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | personas | C4 | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | sí | municipio | 1980–2024 |
| `mnp_nacimientos` | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | personas | C4 | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | sí | municipio | 1980–2024 |
| `mnp_saldo_vegetativo` | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | personas | C4 | INE, Movimiento Natural de la Población (microdatos; municipio de residencia) | sí | municipio | 1980–2024 |
| `monitor_compraventas_libre` | INE, ETDP (ETDP1823) | operaciones | C4 | INE, ETDP (ETDP1823) | sí | nacional | 2023-08–2026-07 |
| `monitor_compraventas_protegida` | INE, ETDP (ETDP1822) | operaciones | C4 | INE, ETDP (ETDP1822) | sí | nacional | 2023-08–2026-07 |
| `monitor_fianzas_gva` | Generalitat Valenciana, datos abiertos (CC BY 4.0) | fianzas | C4 | Generalitat Valenciana, datos abiertos (CC BY 4.0) | sí | ccaa | 2025–2026 |
| `monitor_hipotecas_viviendas` | INE, hipotecas (HPT34618) | hipotecas | C4 | INE, hipotecas (HPT34618) | sí | nacional | 2023-08–2026-07 |
| `monitor_hpi_eurostat` | Eurostat, prc_hpi_q | índice 2015=100 | C4 | Eurostat, prc_hpi_q | sí | nacional | 2005T4–2026T2 |
| `monitor_ipc_alquiler` | INE, IPC (IPC290887) | índice | C4 | INE, IPC (IPC290887) | sí | nacional | 2023-10–2026-09 |
| `monitor_ipv_general` | INE, IPV (serie IPV1209) | índice | C4 | INE, IPV (serie IPV1209) | sí | nacional | 2017T3–2026T2 |
| `monitor_plataformas_noches` | Eurostat, tour_ce_omr | noches | C4 | Eurostat, tour_ce_omr | sí | nacional | 2018–2025 |
| `monitor_poblacion` | INE, ECP (ECP320) | personas | C4 | INE, ECP (ECP320) | sí | nacional | 2014T3–2026T3 |
| `monitor_tipo_hip_tae` | BCE, MIR | % anual | C4 | BCE, MIR | sí | nacional | 2022-01–2026-08 |
| `monitor_tipo_hip_variable` | BCE, MIR | % anual | C4 | BCE, MIR | sí | nacional | 2022-01–2026-08 |
| `monitor_vut_viviendas` | INE, VUT (VTE71) | viviendas | C4 | INE, VUT (VTE71) | sí | nacional | 2020-08–2026-05 |
| `obra_nueva_neta_catastro` | Catastro, estadística URBANA: diferencia anual (cálculo propio) | unidades urbanas residenciales | C4 | Catastro, estadística URBANA: diferencia anual (cálculo propio) | sí | municipio | 2013–2026 |
| `obra_nueva_viviendas_inspire` | Catastro INSPIRE: viviendas por año de construcción (stock superviviente; agregado propio) | viviendas | C4 | Catastro INSPIRE: viviendas por año de construcción (stock superviviente; agregado propio) | sí | municipio | 1900–2026 |
| `ocupados` | Ocupados EPA, total nacional (media del trimestre) | miles de personas | C4 | ine_epa_ocupados.csv (EPA387796) | sí | ccaa,nacional | 2002T1–2026T2 |
| `ocupados_epa` |  | miles de personas | C4 | INE, EPA por provincia | sí | provincia | 2002–2026T2 |
| `ocupados_epa_prov` | Ocupados EPA, suma de provincias (contraste con ocupados CCAA) | miles de personas | C1 | INE EPA 65345 EPA_ocupados | sí | ccaa | 2007T1–2026T2 |
| `ocupados_sa` |  | miles (SA) | C4 | Derivada (STL) | sí | nacional | 2002T1–2026T2 |
| `opi_residentes_documentados` | OPI (Ministerio de Inclusión), extranjeros con certificado de registro o tarjeta en vigor; réplica de la Comunidad de Madrid | personas | C4 | OPI (Ministerio de Inclusión), extranjeros con certificado de registro o tarjeta en vigor; réplica de la Comunidad de Ma | sí | provincia | 2013–2025 |
| `p_bde` | Precio medio m2 viviendas libres tasadas, total nacional (BdE; trimestre = mes de cierre) | euros/m2 | C1 | bde_precio_vivienda_libre.csv (DHIVTNOAPLPMMUVT_RLI.T) | sí | nacional | 1995T1–2026T2 |
| `p_bde_nueva` | Precio medio m2 tasado, viviendas hasta 5 años (BdE) | euros/m2 | C4 | bde_precio_vivienda_libre.csv (VVN) | sí | nacional | 2013T1–2026T2 |
| `p_bde_usada` | Precio medio m2 tasado, viviendas de más de 5 años (BdE) | euros/m2 | C4 | bde_precio_vivienda_libre.csv (VVU) | sí | nacional | 2013T1–2026T2 |
| `p_tasado` | Valor tasado medio de la vivienda libre, total nacional (medida principal de precio de compra) | euros/m2 | C1/C4 | mivau_valor_tasado_nacional_ccaa_prov.csv (serie valor_tasado_libre_nacional) | sí | ccaa,municipio,nacional,provincia | 1995T1–2026T2 |
| `padron_pob_nacionalidad` | INE, Padrón continuo por nacionalidad (tablas jaxiT3 por provincia; suma de municipios) | personas | C4 | INE, Padrón continuo por nacionalidad (tablas jaxiT3 por provincia; suma de municipios) | sí | provincia | 2003–2022 |
| `parados_epa` | Parados EPA, suma de provincias de la CCAA | miles de personas | C4 | INE EPA tabla 65345, medida EPA_parados | sí | ccaa,provincia | 2002–2026T2 |
| `permisos` |  | viviendas (visados) | C4 | MIVAU, visados de dirección de obra | sí | nacional | 2000T1–2026T2 |
| `pib_ccaa_anual` | PIB a precios corrientes, suma de provincias (CRE 80109); control; el valor anual se repite en los 4 trimestres sin interpolar | miles de euros | C4 | INE CRE 80109 PIB_precios_corrientes | sí | ccaa | 2007T1–2025T4 |
| `pib_ccaa_q` | PIB trimestralizado: ancla en T3, log-lineal entre anclas, sin extrapolar (huecos tras el último ancla); solo robustez | miles de euros | C4 | INE, Contabilidad Regional (trimestralización propia) | sí | ccaa | 2007T1–2025T3 |
| `pib_miles_eur` | PIB a precios corrientes (CRE 80109) | miles de euros | C4 | INE CRE 80109 | sí | provincia | 2002–2024 |
| `pib_nom` | PIB a precios de mercado, precios corrientes, ajustado de estacionalidad y calendario (INE) | millones de euros | C4 | ine_cnt_demanda_corrientes.csv (CNTR6597) | sí | nacional | 1995T1–2026T2 |
| `pib_vol_idx` | PIB, índice de volumen encadenado, ajustado de estacionalidad y calendario (INE) | índice | C4 | ine_cnt_demanda_volumen.csv (CNTR6652) | sí | nacional | 1995T1–2026T2 |
| `pob_africa` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_apatridas` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_asia` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_censo_anual` | INE, Censo anual de población (tablas por provincia) | personas | C4 | INE, Censo anual de población (tablas por provincia) | sí | municipio,provincia,seccion | 2021–2025 |
| `pob_centroamerica_caribe` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_espanola` |  | personas (stock 1 ene) | C4 | INE 77019 (ECP) | sí | ccaa,municipio | 1998–2025T1 |
| `pob_europa_no_ue27` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2021–2025 |
| `pob_europa_no_ue28` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2020 |
| `pob_europa_sin_espana` |  | personas (stock 1 ene) | C4 | Derivada de 77019 (ver nota) | sí | ccaa | 2002–2025 |
| `pob_extranj` | Población extranjera = total - nacionales, a 1 de enero (Eurostat migr_pop1ctz), interpolada linealmente a trimestral | personas | C1/C4 | v8/eurostat_migr_pop1ctz_es.csv (códigos TOTAL y NAT) | sí | ccaa,nacional,provincia | 2002–2025T1 |
| `pob_extranj_ccaa_sum` |  | personas (stock) | C4 | Derivada: suma de 17 CCAA de INE 77019 | sí | nacional | 2002T1–2025T1 |
| `pob_extranj_ine` | Población residente de nacionalidad extranjera (ECP/INE) | personas | C1 | ine_ecp_nacional.csv (ECP701) | sí | nacional | 2002T1–2026T2 |
| `pob_extranjera` |  | personas | C4 | INE, Padrón continuo | sí | municipio | 1998–2022 |
| `pob_extranjera_gva` |  | personas | C4 | GVA (IVE), Padrón municipal | sí | municipio | 2005–2022 |
| `pob_norteamerica` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_oceania` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_sudamerica` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2025 |
| `pob_total` | Población residente total (ECP/INE) | personas | C4 | ine_ecp_nacional.csv (ECP320) | sí | ccaa,municipio,nacional,provincia | 1995T1–2026T2 |
| `pob_ue27_sin_espana` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2021–2025 |
| `pob_ue28_sin_espana` |  | personas | C4 | INE, Estadística Continua de Población por CCAA y grupo de nacionalidad (77019) | sí | ccaa | 2002–2020 |
| `pob_vlc_africa` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `pob_vlc_alemania` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `pob_vlc_america` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `pob_vlc_asia` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `pob_vlc_europa` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `pob_vlc_reino_unido` |  | personas | C4 | INE, Padrón continuo (València por nacionalidad) | sí | municipio | 1998–2022 |
| `prod_constr` |  | índice 2021=100 | C4 | Eurostat, sts_copr (producción de la construcción) | sí | nacional | 2005T1–2026T2 |
| `proteccion_temporal_beneficiarios` | Eurostat, migr_asytpsm (beneficiarios a fin de mes) | personas | C4 | Eurostat, migr_asytpsm (beneficiarios a fin de mes) | sí | nacional | 2022-03–2026-08 |
| `proteccion_temporal_concesiones` | Eurostat, migr_asytpfm (concesiones mensuales) | personas | C4 | Eurostat, migr_asytpfm (concesiones mensuales) | sí | nacional | 2022-03–2026-08 |
| `rdb` | Renta disponible bruta del total de la economía, ajustada de estacionalidad (INE); NO es renta de los hogares | millones de euros | C4 | ine_cnt_renta_disponible.csv (CTNFSI11113) | sí | nacional | 1999T1–2026T2 |
| `reate_habitaciones_uso_turistico` | Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0) | habitaciones | C4 | Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0) | sí | municipio | 2026-10-15–2026-10-15 |
| `reate_viviendas_uso_turistico` | Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0) | viviendas | C4 | Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0) | sí | municipio | 2026-10-15–2026-10-15 |
| `renta_hog` |  | millones de euros | C4 | INE, Contabilidad Nacional Trimestral | sí | nacional | 1999T1–2026T2 |
| `renta_hog_real` |  | M€ a precios de 2020 | C4 | INE, CNT (renta real; cálculo propio) | sí | nacional | 1999T1–2026T2 |
| `salario` | Coste salarial total por trabajador y mes, industria, construcción y servicios (ETCL, INE); 2000T1-2007T4 tabla 6067 y 2008T1+ tabla 79662 | euros/mes | C4 | v8/ine_etcl_6067_nacional.csv (ETCL5741) + v8/ine_etcl_79662_ccaa.csv (Total Nacional) | sí | nacional | 2000T1–2026T2 |
| `salario_ccaa` | Coste salarial total por trabajador y mes, industria, construcción y servicios, por CCAA (ETCL tabla 79662) | euros/mes | C4 | v8/ine_etcl_79662_ccaa.csv | sí | ccaa | 2008T1–2026T2 |
| `sepe_contratos_media_anual` | SEPE, contratos registrados por municipio (media anual propia) | contratos al mes | C4 | SEPE, contratos registrados por municipio (media anual propia) | sí | municipio | 2006–2025 |
| `sepe_paro_registrado_media_anual` | SEPE, paro registrado por municipio (media anual propia) | personas | C4 | SEPE, paro registrado por municipio (media anual propia) | sí | municipio | 2006–2025 |
| `serpavi_alquiler_m2_mediana` |  | €/m²/mes | C4 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados) | sí | distrito,municipio,provincia,seccion | 2011–2024 |
| `serpavi_alquiler_m2_p25` |  | €/m²/mes | C4 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados) | sí | municipio,provincia | 2011–2024 |
| `serpavi_alquiler_m2_p75` |  | €/m²/mes | C4 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados) | sí | municipio,provincia | 2011–2024 |
| `serpavi_alquiler_mes_mediana` |  | €/mes | C4 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados) | sí | distrito,seccion | 2011–2024 |
| `serpavi_dist_vc_mediana` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_n_contratos` |  | viviendas (contratos) | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_p25` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_p75` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_mediana` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_n_contratos` |  | viviendas (contratos) | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_p25` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_p75` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | distrito | 2011–2024 |
| `serpavi_esp_constante` |  | €/m²/mes (alquiler, VC) | C4 | MIVAU-SERPAVI (XLSX) → agregado propio | sí | nacional | 2011T4–2024T4 |
| `serpavi_n_contratos_recuento` |  | contratos | C4 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados) | sí | municipio,provincia | 2011–2024 |
| `serpavi_vc_alq_m2_mediana` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 mediana | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_alq_m2_p25` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 p25 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_alq_m2_p75` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 p75 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_dist_agg` |  | €/m²/mes | C4 | MIVAU, SERPAVI por distritos | sí | municipio | 2011–2024 |
| `serpavi_vc_mediana` |  | €/m²/mes | C4 | MIVAU-SERPAVI (XLSX) | sí | ccaa,municipio | 2011–2024 |
| `serpavi_vc_n_contratos` | SERPAVI provincia, VC (vivienda colectiva), n_contratos recuento | contratos | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_mediana` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 mediana | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_p25` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 p25 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_p75` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 p75 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_n_contratos` | SERPAVI provincia, VU (vivienda unifamiliar), n_contratos recuento | contratos | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `ss_afiliados_celdas_menor5` | Seguridad Social, afiliados por municipio (nº de celdas «<5») | celdas | C4 | Seguridad Social, afiliados por municipio (nº de celdas «<5») | sí | municipio | 2011-12–2026-09 |
| `ss_afiliados_construccion_cota_inferior` | Seguridad Social, afiliados por municipio, CNAE construccion | afiliados | C4 | Seguridad Social, afiliados por municipio, CNAE construccion | sí | municipio | 2011-12–2026-09 |
| `ss_afiliados_cota_inferior` | Seguridad Social, afiliados por municipio (MUNCNAE; suma de celdas ≥5) | afiliados | C4 | Seguridad Social, afiliados por municipio (MUNCNAE; suma de celdas ≥5) | sí | municipio | 2011-12–2026-09 |
| `ss_afiliados_extranjeros` | Seguridad Social, afiliados extranjeros por provincia (último día del periodo) | afiliados | C4 | Seguridad Social, afiliados extranjeros por provincia (último día del periodo) | sí | provincia | 2022-01–2026-09 |
| `ss_afiliados_hosteleria_cota_inferior` | Seguridad Social, afiliados por municipio, CNAE hosteleria | afiliados | C4 | Seguridad Social, afiliados por municipio, CNAE hosteleria | sí | municipio | 2011-12–2026-09 |
| `ss_afiliados_inmobiliarias_cota_inferior` | Seguridad Social, afiliados por municipio, CNAE inmobiliarias | afiliados | C4 | Seguridad Social, afiliados por municipio, CNAE inmobiliarias | sí | municipio | 2012-12–2026-09 |
| `tasa_paro_epa` | Tasa de paro nacional EPA = parados/(parados+ocupados)×100 (código INE 00) | % | C4 | ine_v2_epa_prov.csv (EPA_parados, EPA_ocupados) | sí | ccaa,nacional | 2002T1–2026T2 |
| `terminadas` | Viviendas libres terminadas, nacional, flujo trimestral (MIVAU tabla 3.2) | viviendas | C4 | mivau_fin_obra.csv (mensual 2008+) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025) | sí | ccaa,nacional,provincia | 1995T1–2026T2 |
| `terminadas_anual_tabla` |  | viviendas | C4 | MIVAU, viviendas libres terminadas (tabla anual) | sí | provincia | 2002–2024 |
| `tipo_bce` |  | % anual | C4 | BCE, tipo MRR (operaciones principales) | sí | nacional | 1999T1–2026T2 |
| `tipo_dfr` | Tipo de la facilidad de depósito del BCE, media trimestral ponderada por días | % anual | C4 | v8/ecb_tipos_euribor3m_depo.csv | sí | nacional | 1999T1–2026T2 |
| `tipo_hip` |  | % anual | C4 | BCE MIR, nuevas operaciones vivienda | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_bce` | Tipo de interés (TAE) de nuevas operaciones de crédito para adquisición de vivienda, España (BCE MIR), media trimestral | % anual | C1 | ecb_tipo_hipotecario_es.csv | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_bde` | Tipo medio de adquisición de vivienda libre, más de 3 años, conjunto de entidades (BdE), media trimestral | % anual | C1 | bde_tipo_hipotecario_referencia.csv (D_1T9H0000) | sí | nacional | 1995T1–2026T2 |
| `tipo_hip_nuevas_tae` | TAE de nuevas operaciones de crédito a la vivienda, hogares (BdE), media trimestral | % anual | C1 | bde_tipos_hipotecas_nuevas.csv (DN_1TI2T0082) | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real` |  | pp | C4 | BdE e INE IPC (tipo real; cálculo propio) | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real_bce` | Tipo hipotecario BCE (TAE nuevas operaciones) menos inflación interanual | puntos porcentuales | C4 | derivada de tipo_hip_bce e ipc_general | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real_bde` | Tipo hipotecario BdE menos inflación interanual del IPC | puntos porcentuales | C4 | derivada de tipo_hip_bde e ipc_general | sí | nacional | 1996T1–2026T2 |
| `tipo_mro` | Tipo de las operaciones principales de financiación (MRO) del BCE, media trimestral ponderada por días | % anual | C4 | ecb_tipo_oficial.csv | sí | nacional | 1999T1–2026T2 |
| `tope_rentas_ccaa` | Tope de rentas autonómico vigente al cierre del trimestre (E09: Ley catalana 11/2020, 2020-09-22 a 2022-04-08, anulación parcial STC 37/2022) | 0/1 | C4 | v2_eventos_politica.csv, E09 (BOE) | sí | ccaa | 2007T1–2026T2 |
| `tope_rentas_ccaa_alt_v3` | Tope vigente con la ventana de la ley según cataluna_contencion_rentas_v3 (hasta 2021-09-21); se reporta junto a E09 porque las ventanas difieren | 0/1 | C4 | v3/cataluna_contencion_rentas_v3.csv | sí | ccaa | 2007T1–2026T2 |
| `tope_rentas_ccaa_frac` | Fracción de días del trimestre con tope vigente (E09) | proporción | C4 | BOE, Ley catalana 11/2020 (evento) | sí | ccaa | 2007T1–2026T2 |
| `trans_extranjeros` |  | transacciones | C4 | MIVAU 340101i0 (de panel_ccaa_q) | sí | ccaa,nacional | 2007T1–2026T2 |
| `trans_total` |  | transacciones | C4 | MIVAU 34010110 (de panel_ccaa_q) | sí | ccaa,municipio,nacional | 2004T1–2026T1 |
| `turistas` | Turistas internacionales llegados a España, total (FRONTUR, dato base mensual), suma trimestral | personas | C4 | v8/ine_frontur_10823_ccaa.csv (FREG286, Total Nacional); el fichero ine_frontur_10822_pais.csv solo trae desglose por pa | sí | nacional | 2015T4–2026T2 |
| `turistas_ccaa` | Turistas internacionales por CCAA de destino (FRONTUR, dato base mensual), suma trimestral | personas | C4 | v8/ine_frontur_10823_ccaa.csv | sí | ccaa | 2015T4–2026T2 |
| `tx_extranj` | Transacciones de vivienda adquiridas por extranjeros residentes, total nacional (MIVAU, tabla 1.6.5) | número | C4 | mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_nacional) | sí | nacional | 2007T1–2026T2 |
| `tx_extranj_ccaa` | Transacciones de vivienda adquiridas por extranjeros residentes por CCAA (MIVAU 1.6.5), total | número | C4 | mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_ccaa_*) | sí | ccaa | 2007T1–2026T2 |
| `tx_total` | Transacciones inmobiliarias de vivienda, total nacional (MIVAU) | número | C4 | mivau_transacciones_total.csv | sí | nacional | 2004T1–2026T1 |
| `v5_deficit_2021_2025` | Resultado publicado V5 (A4): déficit 2021-2025 por provincia (rango de variantes) | viviendas | C4 | Resultado publicado V5 (A4): déficit 2021-2025 por provincia (rango de variantes) | sí | provincia | 2025–2025 |
| `v8_factor_comun_precios` | Resultado publicado V8 (M1): factor común de las fuentes de precio | unidades del componente (estandarizado) | C4 | Resultado publicado V8 (M1): factor común de las fuentes de precio | sí | nacional | 1996T1–2026T2 |
| `valor_tasado` | Valor tasado medio vivienda libre provincial (MIVAU) desde 1995T1; coincide con v7 en el solape | euros/m2 | C4 | mivau_valor_tasado_nacional_ccaa_prov.csv | sí | provincia | 1995T1–2026T2 |
| `valor_tasado_ccaa` | Valor tasado medio de vivienda libre por CCAA, desde 1995T1 | euros/m2 | C4 | mivau_valor_tasado_nacional_ccaa_prov.csv (nivel ccaa) | sí | ccaa | 1995T1–2026T2 |
| `visados` | Viviendas libres iniciadas (visados de dirección de obra), nacional, flujo trimestral (MIVAU tabla 3.1) | viviendas | C4 | mivau_visados.csv (mensual 2008+, suma de 3 meses) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025) | sí | ccaa,nacional | 1995T1–2026T2 |
| `vut_pct_sobre_total` |  | % | C4 | INE, viviendas turísticas (experimental) | sí | municipio,provincia | 2020T3–2026T2 |
| `vut_plazas` | Plazas turísticas por provincia (INE experimental) | plazas | C4 | ine_vut_nacional_ccaa_prov.csv | sí | municipio,nacional,provincia | 2020T3–2026T2 |
| `vut_plazas_por_vivienda` |  | plazas/vivienda | C4 | INE, viviendas turísticas (experimental) | sí | municipio,provincia | 2020T3–2026T2 |
| `vut_registro_gva` | GVA, Registro de Turismo de la Comunitat Valenciana (cortes) | viviendas | C4 | GVA, Registro de Turismo de la Comunitat Valenciana (cortes) | sí | municipio | 2025-01-26–2026-10-14 |
| `vut_registro_gva_reconstruido` | GVA, registro (altas y bajas fechadas; reconstrucción propia) | viviendas | C4 | GVA, registro (altas y bajas fechadas; reconstrucción propia) | sí | municipio | 2015-01–2025-01 |
| `vut_regulacion_ccaa` | Norma autonómica de viviendas de uso turístico vigente (E23 Cataluña 2023-11-09, E24 C. Valenciana 2024-08-08, E25 Baleares 2025-04-16, E26 Canarias 2025-12-13) | 0/1 | C4 | v2_eventos_politica.csv | sí | ccaa | 2007T1–2026T2 |
| `vut_stock_gva` |  | viviendas (stock) | C4 | GVA, registro de turismo (CC BY 4.0) | sí | ccaa,municipio,provincia | 2010T1–2024T4 |
| `vut_viviendas` | Viviendas de uso turístico por provincia (INE experimental) | viviendas | C4 | ine_vut_nacional_ccaa_prov.csv | sí | ccaa,nacional,provincia | 2020–2026T2 |
| `vut_viviendas_turisticas` |  | viviendas | C4 | INE, viviendas turísticas (experimental) | sí | municipio,provincia | 2020T3–2026T2 |
| `zt_cuota_municipios` | Municipios en zona tensionada / municipios de la CCAA (diccionario INE 2026) | proporción | C4 | idem + ine_diccionario_municipios_2026.xlsx | sí | ccaa | 2007T1–2026T2 |
| `zt_declarada` | Al menos un municipio en zona tensionada vigente (Ley 12/2023, art. 18) | 0/1 | C4 | BOE, resoluciones de zonas tensionadas (evento) | sí | ccaa | 2007T1–2026T2 |
| `zt_n_municipios` | Municipios en zona tensionada vigente al cierre del trimestre (alcance parcial cuenta como municipio) | número | C4 | Resoluciones de zonas tensionadas, v3/zonas_tensionadas_v3.csv (fecha_efecto, fecha_fin_prevista) | sí | ccaa | 2007T1–2026T2 |
| `zt_vigente` | BOE, resoluciones de la Secretaría de Estado de Vivienda (zonas tensionadas) | 0/1 | C4 | BOE, resoluciones de la Secretaría de Estado de Vivienda (zonas tensionadas) | sí | municipio | 2024T1–2026T3 |
