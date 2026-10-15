# Inventario previo a V11-DATOS (2026-10-15)

Generado a partir de data/raw/_manifest.csv (proyecto v1-v8), data/raw/v9/_manifest.csv (V9) y los ficheros de data/raw/v3, v4, v5, v8 y v10. Sirve para no duplicar: una fuente que ya está solo se actualiza si hay edición nueva.

## migración y población

| fichero | fuente | periodo |
|---|---|---|
| data/raw/eu_migr_pop.csv | Eurostat | 2000-01-01 – 2025-01-01 |
| data/raw/eurostat_inmigracion_anual.csv | Eurostat | 1998-01-01 – 2024-01-01 |
| data/raw/eurostat_renta_hogares.csv | Eurostat | 1999-01-01 – 2026-04-01 |
| data/raw/gva_padron_extranjeros_municipio.csv | IVE - Padron municipal continuo: explotacion estadistica por distritos y secciones (datos abiertos CKAN) | 2005-01-01 – 2022-01-01 |
| data/raw/ine_ecp_56936.csv | INE | 2002-01-01 – 2025-01-01 |
| data/raw/ine_ecp_59585.csv | INE | 2025-04-01 – 2026-07-01 |
| data/raw/ine_ecp_ccaa_nacionalidad.csv | INE | 2002-01-01 – 2025-01-01 |
| data/raw/ine_ecp_ccaa_paises.csv | INE | 2002-01-01 – 2025-01-01 |
| data/raw/ine_ecp_nacional.csv | INE | 1971-01-01 – 2026-07-01 |
| data/raw/ine_epa_hogares.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_epa_poblacion_ccaa.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_hogares_60131.csv | INE | 2021-01-01 – 2026-07-01 |
| data/raw/ine_migraciones_ccaa_nacionalidad.csv | INE | 2023-04-01 – 2026-07-01 |
| data/raw/ine_migraciones_nacionalidad.csv | INE | 2023-04-01 – 2026-07-01 |
| data/raw/ine_migraciones_total_anual.csv | INE | 2021-01-01 – 2024-01-01 |
| data/raw/ine_padron_valencia.csv | INE | 1996-01-01 – 2026-07-01 |
| data/raw/ine_padron_vlc_nacionalidad.csv | INE Padrón continuo | 1998-01-01 – 2022-01-01 |
| data/raw/ine_v2_hogares_prov.csv | INE ECP - Hogares de personas residentes en viviendas familiares por tamaño, trimestral (tabla 60133) | 2021-01-01 – 2026-07-01 |
| data/raw/ine_v2_migraciones_prov.csv | INE EM/EMCR - Flujo de inmigración procedente del extranjero por provincia, semestre (tablas 24420, 24421) | 2008-01-01 – 2022-01-01 |
| data/raw/ine_v2_padron_prov_edad_nac.csv | INE ECP - Población residente por fecha, sexo, grupo de edad y nacionalidad (tabla 77023; 1 de enero) | 2002-01-01 – 2026-01-01 |
| data/raw/ine_v2_padron_prov_pais.csv | INE ECP - Población residente por provincia y agrupación de países de nacionalidad, 1 de enero (tabla 77023) | 2002-01-01 – 2026-01-01 |
| data/raw/mivau_transacciones_extranjeros.csv | MIVAU - Boletin Online Fomento (sedal) | 2007-01-01 – 2026-04-01 |
| data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v3/ine_v3_censo2021_seccion_edad.csv | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v9/ine_censo_anual/censo_municipio_sexo.csv.gz | ine_censo_anual | 2021-2025 |
| data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz | ine_censo_anual | 2021-2025 |
| data/raw/v9/ine_censos/censo_t3457.csv.gz | ine_censos | 2011 (1 de noviembre) |
| data/raw/v9/ine_migraciones/ine_em_24323.csv.gz | ine_migraciones | 2008–2021 |
| data/raw/v9/ine_migraciones/ine_em_24326.csv.gz | ine_migraciones | 2008–2021 |
| data/raw/v9/ine_migraciones/ine_em_24379.csv.gz | ine_migraciones | 2008–2021 |
| data/raw/v9/ine_migraciones/ine_em_24385.csv.gz | ine_migraciones | 2008–2021 |
| data/raw/v9/ine_migraciones/ine_emcr_69693.csv.gz | ine_migraciones | 2021–2024 |
| data/raw/v9/ine_migraciones/ine_emcr_69708.csv.gz | ine_migraciones | 2021–2024 |
| data/raw/v9/ine_migraciones/ine_emcr_69733.csv.gz | ine_migraciones | 2021–2024 |
| data/raw/v9/ine_migraciones/ine_emcr_69764.csv.gz | ine_migraciones | 2021–2024 |
| data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz | ine_padron_nacionalidad | 2003-2022 (1 de enero) |
| data/raw/v9/ine_padron_nacionalidad/padron_pais_nacimiento_2003_2022.csv.gz | ine_padron_nacionalidad | 2003-2022 (1 de enero) |
| data/raw/v9/ine_padron_nacionalidad/tablas.csv | ine_padron_nacionalidad | nan |
| data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_censo2021_seccion_edad.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz | (sin manifiesto global) | ver fichero |
| data/raw/v5/ine_b1_t36726_proy_poblacion_prov.csv | (sin manifiesto global) | ver fichero |
| data/raw/v5/ine_b1_t54562_proy_hogares.csv | (sin manifiesto global) | ver fichero |
| data/raw/v5/ine_b1_t67235_mortalidad_prov.csv | (sin manifiesto global) | ver fichero |
| data/raw/v5/ine_b1_t69764_saldos_prov.csv | (sin manifiesto global) | ver fichero |
| data/raw/v8/eurostat_migr_pop1ctz_es.csv | (sin manifiesto global) | ver fichero |

## vivienda y hogares (condiciones)

| fichero | fuente | periodo |
|---|---|---|
| data/raw/ine_epa_hogares.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_epa_ocupados.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_epa_ocupados_ccaa.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_epa_poblacion_ccaa.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_v2_epa_prov.csv | INE EPA - Ocupados y parados por provincia, trimestral (tabla 65345) | 2002-01-01 – 2026-04-01 |
| data/raw/v3/eff_tenencia_edad_v3.csv | BdE EFF | 2002-12-31 – 2022-12-31 |
| data/raw/v3/eurostat_emancipacion_tenencia_v3.csv | Eurostat ilc_lvps08 / ilc_lvho02 | 2004-01-01 – 2025-01-01 |
| data/raw/v3/ine_ecv_tenencia_edad_v3.csv | INE ECV | 2004-01-01 – 2025-01-01 |
| data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v3/ine_v3_censo2021_seccion_edad.csv | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz | INE Censo de Población y Viviendas 2021 (provisional) | 2021-11-01 – 2021-11-01 |
| data/raw/v9/ine_censo_anual/censo_municipio_sexo.csv.gz | ine_censo_anual | 2021-2025 |
| data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz | ine_censo_anual | 2021-2025 |
| data/raw/v9/ine_censos/censo_t3457.csv.gz | ine_censos | 2011 (1 de noviembre) |
| data/raw/v9/ine_microdatos/ecv/datos_2018.zip | ine_microdatos | 2018 |
| data/raw/v9/ine_microdatos/ecv/datos_2019.zip | ine_microdatos | 2019 |
| data/raw/v9/ine_microdatos/ecv/datos_2020.zip | ine_microdatos | 2020 |
| data/raw/v9/ine_microdatos/ecv/datos_2021.zip | ine_microdatos | 2021 |
| data/raw/v9/ine_microdatos/ecv/datos_2022.zip | ine_microdatos | 2022 |
| data/raw/v9/ine_microdatos/ecv/datos_2023.zip | ine_microdatos | 2023 |
| data/raw/v9/ine_microdatos/ecv/datos_2024.zip | ine_microdatos | 2024 |
| data/raw/v9/ine_microdatos/ecv/datos_2025.zip | ine_microdatos | 2025 |
| data/raw/v9/ine_microdatos/epa/datos_1t18.zip | ine_microdatos | 1t18 |
| data/raw/v9/ine_microdatos/epa/datos_1t19.zip | ine_microdatos | 1t19 |
| data/raw/v9/ine_microdatos/epa/datos_1t20.zip | ine_microdatos | 1t20 |
| data/raw/v9/ine_microdatos/epa/datos_1t21.zip | ine_microdatos | 1t21 |
| data/raw/v9/ine_microdatos/epa/datos_1t22.zip | ine_microdatos | 1t22 |
| data/raw/v9/ine_microdatos/epa/datos_1t23.zip | ine_microdatos | 1t23 |
| data/raw/v9/ine_microdatos/epa/datos_1t24.zip | ine_microdatos | 1t24 |
| data/raw/v9/ine_microdatos/epa/datos_1t25.zip | ine_microdatos | 1t25 |
| data/raw/v9/ine_microdatos/epa/datos_1t26.zip | ine_microdatos | 1t26 |
| data/raw/v9/ine_microdatos/epa/datos_2t18.zip | ine_microdatos | 2t18 |
| data/raw/v9/ine_microdatos/epa/datos_2t19.zip | ine_microdatos | 2t19 |
| data/raw/v9/ine_microdatos/epa/datos_2t20.zip | ine_microdatos | 2t20 |
| data/raw/v9/ine_microdatos/epa/datos_2t21.zip | ine_microdatos | 2t21 |
| data/raw/v9/ine_microdatos/epa/datos_2t22.zip | ine_microdatos | 2t22 |
| data/raw/v9/ine_microdatos/epa/datos_2t23.zip | ine_microdatos | 2t23 |
| data/raw/v9/ine_microdatos/epa/datos_2t24.zip | ine_microdatos | 2t24 |
| data/raw/v9/ine_microdatos/epa/datos_2t25.zip | ine_microdatos | 2t25 |
| data/raw/v9/ine_microdatos/epa/datos_2t26.zip | ine_microdatos | 2t26 |
| data/raw/v9/ine_microdatos/epa/datos_3t18.zip | ine_microdatos | 3t18 |
| data/raw/v9/ine_microdatos/epa/datos_3t19.zip | ine_microdatos | 3t19 |
| data/raw/v9/ine_microdatos/epa/datos_3t20.zip | ine_microdatos | 3t20 |
| data/raw/v9/ine_microdatos/epa/datos_3t21.zip | ine_microdatos | 3t21 |
| data/raw/v9/ine_microdatos/epa/datos_3t22.zip | ine_microdatos | 3t22 |
| data/raw/v9/ine_microdatos/epa/datos_3t23.zip | ine_microdatos | 3t23 |
| data/raw/v9/ine_microdatos/epa/datos_3t24.zip | ine_microdatos | 3t24 |
| data/raw/v9/ine_microdatos/epa/datos_3t25.zip | ine_microdatos | 3t25 |
| data/raw/v9/ine_microdatos/epa/datos_4t18.zip | ine_microdatos | 4t18 |
| data/raw/v9/ine_microdatos/epa/datos_4t19.zip | ine_microdatos | 4t19 |
| data/raw/v9/ine_microdatos/epa/datos_4t20.zip | ine_microdatos | 4t20 |
| data/raw/v9/ine_microdatos/epa/datos_4t21.zip | ine_microdatos | 4t21 |
| data/raw/v9/ine_microdatos/epa/datos_4t22.zip | ine_microdatos | 4t22 |
| data/raw/v9/ine_microdatos/epa/datos_4t23.zip | ine_microdatos | 4t23 |
| data/raw/v9/ine_microdatos/epa/datos_4t24.zip | ine_microdatos | 4t24 |
| data/raw/v9/ine_microdatos/epa/datos_4t25.zip | ine_microdatos | 4t25 |
| data/raw/v9/ine_microdatos/epa/dr_EPA_2021.xlsx | ine_microdatos | dr_EPA_2021 |
| data/raw/v9/ine_microdatos/epa/dr_EPA_2026.xlsx | ine_microdatos | dr_EPA_2026 |
| data/raw/v3/eff_tenencia_edad_v3.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/eurostat_emancipacion_tenencia_v3.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_ecv_tenencia_edad_v3.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_censo2021_seccion_edad.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz | (sin manifiesto global) | ver fichero |
| data/raw/v5/cb_ine_t9997_ecv_tenencia_ccaa.json | (sin manifiesto global) | ver fichero |

## oferta y parque

| fichero | fuente | periodo |
|---|---|---|
| data/raw/catastro_urbana_municipios.csv | Catastro - Estadisticas catastrales, Datos municipios (Urbano) | 2011-12-31 – 2025-12-31 |
| data/raw/catastro_urbana_municipios.csv.gz | Catastro - Estadisticas catastrales, Datos municipios (Urbano) | 2011-12-31 – 2025-12-31 |
| data/raw/mivau_fin_obra.csv | MIVAU - Boletin Online Fomento (sedal) | 2008-01-01 – 2026-06-01 |
| data/raw/mivau_parque.csv | MIVAU - Boletin Online Fomento (sedal) | 2001-12-31 – 2025-12-31 |
| data/raw/mivau_v2_iniciadas_terminadas_prov.csv | MIVAU - Boletin Online Fomento/Transportes (sedal) | 1991-01-01 – 2026-06-01 |
| data/raw/mivau_v2_protegida.csv | MIVAU - Boletin Online Fomento/Transportes (sedal) | 1991-01-01 – 2026-06-01 |
| data/raw/mivau_v2_suelo.csv | MIVAU - Boletin Online Fomento/Transportes (sedal) | 2004-01-01 – 2026-04-01 |
| data/raw/mivau_visados.csv | MIVAU - Boletin Online Fomento (sedal) | 2008-01-01 – 2026-06-01 |
| data/raw/v4/catastro_solares_municipios.csv.gz | Catastro - Estadisticas catastrales municipales (URBANA2012-2026.xls); extracto | 2012-01-01 – 2026-01-01 |
| data/raw/v4/catastro_solares_municipios.csv.gz | (sin manifiesto global) | ver fichero |

## empleo

| fichero | fuente | periodo |
|---|---|---|
| data/raw/eurostat_empleo_nuts2.csv | Eurostat | 2008-01-01 – 2025-01-01 |
| data/raw/ine_epa_ocupados.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/ine_epa_ocupados_ccaa.csv | INE | 2002-01-01 – 2026-04-01 |
| data/raw/v9/sepe_municipios/contratos_municipio_mensual.csv.gz | sepe_municipios | 200601-202608 |
| data/raw/v9/sepe_municipios/paro_registrado_municipio_mensual.csv.gz | sepe_municipios | 200601-202608 |

## turismo

| fichero | fuente | periodo |
|---|---|---|
| data/raw/gva_vut_municipio.csv | Generalitat Valenciana - Registre de Turisme CV (datos abiertos CKAN) | 2010-01-01 – 2026-10-09 |
| data/raw/ine_v2_vut.csv | INE VTE - Viviendas turísticas, plazas: provincias (39364) y municipios (39363), mensual | 2020-08-01 – 2026-05-01 |
| data/raw/ine_vut_nacional_ccaa_prov.csv | INE - Estadistica experimental viviendas turisticas | 2020-08-01 – 2026-05-01 |
| data/raw/ine_vut_valencia_municipio.csv | INE - Estadistica experimental viviendas turisticas | 2020-08-01 – 2026-05-01 |
| data/raw/ine_vut_valencia_provincia.csv | INE - Estadistica experimental viviendas turisticas | 2020-08-01 – 2026-05-01 |
| data/raw/v3/airbnb_insideairbnb_agregados_v3.csv.gz | Inside Airbnb (CC BY 4.0; insideairbnb.com/get-the-data) | 2025-12-14 – 2026-09-28 |
| data/raw/v3/hut_registro_turismo_cat_v3.csv.gz | Registre de Turisme de Catalunya - Establiments d'allotjament turístic (Socrata t2h3-cgys, Dept. Empresa i Treball; licencia Ver términos de uso) | 2026-10-05 – 2026-10-05 |
| data/raw/v3/ine_v3_vut_municipio_pct.csv | INE Medición del número de viviendas turísticas (estadística experimental) | 2020-08-01 – 2026-05-01 |
| data/raw/v3/ine_v3_vut_seccion.csv.gz | INE (servergis ArcGIS) | 2021-02-01 – 2026-05-01 |
| data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz | bcn_hut | licencias vigentes; año de expediente |
| data/raw/v9/cat_turisme/idescat_allotjaments_municipi.csv.gz | cat_turisme | 2015-2025 |
| data/raw/v9/cat_turisme/ieet_municipi.csv.gz | cat_turisme | 17S1-25S1 |
| data/raw/v9/cat_turisme/registre_turisme_agregat_municipi.csv.gz | cat_turisme | corte 2026-10 |
| data/raw/v9/eurostat_plataformas/tour_ce_oam.csv.gz | eurostat_plataformas | 2018–2025 |
| data/raw/v9/eurostat_plataformas/tour_ce_oan3.csv.gz | eurostat_plataformas | 2018–2025 |
| data/raw/v9/eurostat_plataformas/tour_ce_oasc.csv.gz | eurostat_plataformas | 2018–2025 |
| data/raw/v9/eurostat_plataformas/tour_ce_omn12.csv.gz | eurostat_plataformas | 2018–2026 |
| data/raw/v9/eurostat_plataformas/tour_ce_omr.csv.gz | eurostat_plataformas | 2018–2026 |
| data/raw/v9/gva_vut/cortes/vut_actual_2026-10-14.csv.gz | gva_vut | 2026-10-14 |
| data/raw/v9/gva_vut/cortes/vut_historico_2025-01-26.csv.gz | gva_vut | 2025-01-26 |
| data/raw/v9/gva_vut/cortes/vut_ultimo_periodo_2025-01-26.csv.gz | gva_vut | 2025-01-26 |
| data/raw/v9/gva_vut/gva_vut_panel_cp.csv | gva_vut | 2015-01/2026-10 |
| data/raw/v9/gva_vut/gva_vut_panel_municipio.csv | gva_vut | 2015-01/2026-10 |
| data/raw/v9/insideairbnb/calendar_resumen_barcelona_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/calendar_resumen_madrid_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/calendar_resumen_malaga_2026-09-28.csv.gz | insideairbnb | 2026-09-28 |
| data/raw/v9/insideairbnb/calendar_resumen_mallorca_2026-09-19.csv.gz | insideairbnb | 2026-09-19 |
| data/raw/v9/insideairbnb/calendar_resumen_valencia_2026-09-20.csv.gz | insideairbnb | 2026-09-20 |
| data/raw/v9/insideairbnb/insideairbnb_barrio.csv.gz | insideairbnb | 2026-09 |
| data/raw/v9/insideairbnb/insideairbnb_seccion.csv.gz | insideairbnb | 2025-09 a 2026-09 |
| data/raw/v9/insideairbnb/listings_barcelona_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/listings_madrid_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/listings_malaga_2026-09-28.csv.gz | insideairbnb | 2026-09-28 |
| data/raw/v9/insideairbnb/listings_mallorca_2026-09-19.csv.gz | insideairbnb | 2026-09-19 |
| data/raw/v9/insideairbnb/listings_valencia_2026-09-20.csv.gz | insideairbnb | 2026-09-20 |
| data/raw/v9/insideairbnb/neighbourhoods_barcelona_2026-09-17.geojson | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/neighbourhoods_valencia_2026-09-20.geojson | insideairbnb | 2026-09-20 |
| data/raw/v9/insideairbnb/reviews_resumen_barcelona_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/reviews_resumen_madrid_2026-09-17.csv.gz | insideairbnb | 2026-09-17 |
| data/raw/v9/insideairbnb/reviews_resumen_malaga_2026-09-28.csv.gz | insideairbnb | 2026-09-28 |
| data/raw/v9/insideairbnb/reviews_resumen_mallorca_2026-09-19.csv.gz | insideairbnb | 2026-09-19 |
| data/raw/v9/insideairbnb/reviews_resumen_valencia_2026-09-20.csv.gz | insideairbnb | 2026-09-20 |
| data/raw/v9/insideairbnb/validacion_insideairbnb.csv | insideairbnb | 2026-09 |
| data/raw/v3/airbnb_insideairbnb_agregados_v3.csv.gz | (sin manifiesto global) | ver fichero |
| data/raw/v3/hut_registro_turismo_cat_v3.csv.gz | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_vut_municipio_pct.csv | (sin manifiesto global) | ver fichero |
| data/raw/v3/ine_v3_vut_seccion.csv.gz | (sin manifiesto global) | ver fichero |
| data/raw/v8/ine_frontur_10822_pais.csv | (sin manifiesto global) | ver fichero |
| data/raw/v8/ine_frontur_10823_ccaa.csv | (sin manifiesto global) | ver fichero |

## crédito y lanzamientos

| fichero | fuente | periodo |
|---|---|---|
| data/raw/bde_credito_finalidad.csv | BdE | 1992-12-01 – 2026-08-01 |
| data/raw/bde_precio_vivienda_libre.csv | BdE | 1995-03-01 – 2026-06-01 |
| data/raw/bde_tipo_hipotecario_referencia.csv | BdE | 1973-01-01 – 2026-09-01 |
| data/raw/bde_tipos_hipotecas_nuevas.csv | BdE | 2003-01-01 – 2026-08-01 |
| data/raw/ecb_nuevo_credito_vivienda_es.csv | BCE | 2003-01-01 – 2026-08-01 |
| data/raw/ecb_stock_credito_vivienda_es.csv | BCE | 2003-01-01 – 2026-08-01 |
| data/raw/ecb_tipo_hipotecario_es.csv | BCE | 2003-01-01 – 2026-08-01 |
| data/raw/ine_v2_hipotecas_prov.csv | INE HPT - Hipotecas constituidas sobre el total de fincas, viviendas (tabla 76317, base nueva) | 2003-01-01 – 2026-07-01 |
| data/raw/v9/actualizaciones/bde_be0418.csv | actualizaciones | 1992-12–2026-06 |
| data/raw/v9/actualizaciones/bde_be0819.csv | actualizaciones | 1992-12–2026-06 |
| data/raw/v9/actualizaciones/bde_be1911.csv | actualizaciones | 2003-01–2026-08 |
| data/raw/v9/actualizaciones/bde_be1916.csv | actualizaciones | 2003-01–2026-08 |
| data/raw/v9/bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz | bce_hipotecas | 2003-01–2026-08 |
| data/raw/v5/ca_bde_be0418_credito_actividad.csv | (sin manifiesto global) | ver fichero |
| data/raw/v5/cb_cgpj_lanzamientos_pj_2013_2025.xlsx | (sin manifiesto global) | ver fichero |
| data/raw/v5/cb_cgpj_series_tsj_1T2026.xlsx | (sin manifiesto global) | ver fichero |

## Huecos ya documentados

- docs/v9/cobertura.md y docs/v9/auditoria_exhaustividad.md: EVR antes de 2008, censo 2001, afiliación municipal, cortes antiguos VUT GVA (Wayback bloqueado), cortes trimestrales BCN (anti-bot), padrón por barrio de València 2023-2026, INE VUT nov-2026 (no publicado).
