# Notas de inventario de datos (solo lectura)

Fecha de la pasada: 2026-10-12. Sin ejecución de modelos. `data/sealed` no consultado. Fuentes: `data/raw/_manifest.csv` (110 ficheros), `_manifest_series_ine_v2.csv` (18.090 series INE, solo agregados), `docs/diccionario_variables.md`, `docs/v6/diccionario.md`, `docs/fuentes_fallidas.md`, `docs/v*/fuentes_fallidas.md`, `docs/v5/solicitudes.md`, `data/processed/*`, `output/v6/M0/paneles/*`.

Leyenda: T = trimestral, M = mensual, S = semestral, A = anual. "Validado" = lo que consta en el diccionario (sí / plausibilidad / no consta).

## 1. Datasets de data/raw

### 1.1 Nivel raíz (ficheros normalizados `fecha, periodo, serie, valor, unidad, fuente, url, ...`)

| Fichero | Fuente | Descarga (UTC) | Nivel | Frec. | Periodo | Método | Validado | Scripts (src/) |
|---|---|---|---|---|---|---|---|---|
| ine_ipv_80270.csv | INE IPV tabla 80270 | 2026-10-09 | Nac, CCAA | T | 2007Q1–2026Q2 | API | sí | fetch_ine, build_dataset |
| ine_ipv_25171.csv | INE IPV tabla 25171 (base 2015) | 2026-10-09 | Nac, CCAA | T | 2007Q1–2025Q4 | API | sí (robustez) | fetch_ine, ca_run |
| eurostat_hpi.csv / eu_hpi.csv | Eurostat prc_hpi_q | 2026-10-09 / 10-10 | Nac / UE | T | 2005Q4–2026Q2 | API | sí | fetch_eurostat, build_dataset_v2 |
| mivau_valor_tasado_nacional_ccaa_prov.csv | MIVAU Boletín (tabla 35101000) | 2026-10-09 | Nac, CCAA, prov | T | 1995Q1–2026Q2 | XLS | sí | fetch_mivau, build_dataset |
| mivau_valor_tasado_municipios.csv | MIVAU Boletín | 2026-10-09 | Municipio (309 series) | T | 2005–2026T1 | XLS | no consta | fetch_mivau, build_dataset_v2 |
| bde_precio_vivienda_libre.csv | BdE be2507 | 2026-10-09 | Nac | T | 1995Q1–2026Q2 | descarga CSV | sí | fetch_bde, build_dataset |
| vlc_precio_vivienda_libre.csv | Ajuntament de València (CKAN) | 2026-10-09 | Municipio (València) | T | 2021Q2–2022Q1 | API | no consta (fuente primaria sin indicar) | fetch_valencia |
| bis_rpp.csv | BIS | 2026-10-10 | Países | T | 2000–2026T1 | API | no consta | fetch_ue_v2 |
| oecd_house_prices.csv | OCDE | 2026-10-10 | Países | T | 2000–2026-07 | API | no consta | build_dataset_v2 |
| ine_epa_ocupados.csv / _ccaa.csv | INE EPA 65302 / EPA387796 | 2026-10-09 | Nac / CCAA (420 series) | T | 2002–2026T1 | API | sí | fetch_ine, build_dataset |
| ine_epa_hogares.csv | INE EPA 65269 | 2026-10-09 | Nac | T | 2002–2026T1 | API | sí | fetch_ine, k4b_run |
| ine_epa_poblacion_ccaa.csv | INE EPA | 2026-10-09 | CCAA | T | 2002–2026T1 | API | no consta | fetch_ine |
| ine_v2_epa_prov.csv | INE EPA tabla 65345 (ocupados y parados) | 2026-10-10 | Provincia (106 series) | T | 2002–2026T1 | API | no consta | fetch_ine_v2, build_dataset_v2 |
| ine_etdp_compraventas.csv | INE ETDP tabla 6150 | 2026-10-09 | Nac, CCAA (360 series) | M | 2007-01–2026-07 | API | sí | fetch_ine, build_dataset |
| ine_v2_etdp_prov.csv | INE ETDP (régimen y estado) | 2026-10-10 | Provincia (265 series) | M | 2007-01–2026-07 | API | no consta | fetch_ine_v2 |
| ine_ipc_alquiler.csv | INE IPC 290887 | 2026-10-09 | Nac | M | 2002-01–2026-08 | API | sí | fetch_ine, build_dataset |
| ine_v2_ipc_alquiler_prov.csv | INE IPC subgrupo alquiler (tabla 76142) | 2026-10-10 | Provincia (106) | M | 2002-01–2026-08 | API | no consta | fetch_ine_v2 |
| ine_ipva_nacional_ccaa.csv | INE IPVA (59058…) | 2026-10-09 | Nac, CCAA | A | 2011–2024 | API | no consta | fetch_ine |
| ine_ipva_municipal.csv | INE IPVA | 2026-10-09 | Municipio (1.530) | A | 2011–2024 | API | no consta | fetch_ine, extract_serpavi |
| ine_v2_ipva.csv | INE IPVA | 2026-10-10 | Prov. (3.420 series) | A | 2011–2024 | API | no consta | fetch_ine_v2 |
| ine_cnt_pib_oferta_corrientes.csv / _volumen.csv | INE CNT | 2026-10-09 | Nac | T | 1995Q1–2026T1 | API | sí (deflactor) | fetch_ine |
| ine_cnt_demanda_corrientes.csv / _volumen.csv | INE CNT | 2026-10-09 | Nac | T | 1995Q1–2026T1 | API | no consta | fetch_ine |
| ine_cnt_renta_disponible.csv | INE CNT | 2026-10-09 | Nac | T | 1999Q1–2026T1 | API | no consta | fetch_ine |
| ine_v2_cre.csv | INE CRE tabla 80109 (PIB corrientes) | 2026-10-10 | CCAA y provincia (53) | A | 2000–2025 | API | no consta | fetch_ine_v2, build_dataset_v2 |
| ine_ecp_nacional.csv | INE ECP 77023 / 320, 701 | 2026-10-09 | Nac | S (hasta 2020), T (2021+) | 1971–2026-07 | API | sí | fetch_ine, build_dataset |
| ine_ecp_56936.csv / 59585.csv | INE ECP | 2026-10-09 | Nac | T | 2002–2025 / 2025Q2–2026Q3 | API | no consta | fetch_ine |
| ine_ecp_ccaa_paises.csv / _nacionalidad.csv | INE ECP 77023 | 2026-10-09 | CCAA (17) | A / 1 ene | 2002–2025 | API | sí (suma 17 CCAA) | fetch_ine, build_dataset |
| ine_v2_padron_prov_pais.csv / _edad_nac.csv | INE ECP (padrón) | 2026-10-10 | Provincia | A | 2002–2026-01 | API | no consta | fetch_ine_v2, m0_run |
| ine_v2_migraciones_prov.csv | INE EM/EMCR 24420-24421 | 2026-10-10 | Provincia (3.922) | S/A | 2008–2022 | API | no consta | fetch_ine_v2, m2_run |
| ine_migraciones_total_anual.csv | INE EMCR 69687 | 2026-10-09 | Nac | A | 2021–2024 | API | sí (inmig_anual) | fetch_ine |
| ine_migraciones_nacionalidad.csv / _ccaa_nacionalidad.csv | INE EMCR | 2026-10-09 | Nac / CCAA | S | 2023S1–2026S1 | API | no consta | fetch_ine |
| ine_hogares_60131.csv | INE ECP 60131 | 2026-10-09 | Nac | T | 2021Q1–2026Q3 | API | sí (hogares_ecp) | fetch_ine, cb_run |
| ine_v2_hogares_prov.csv | INE ECP hogares | 2026-10-10 | Provincia (265) | T | 2021–2026 | API | no consta | fetch_ine_v2, a4_run |
| ine_v2_hipotecas_prov.csv | INE HPT 76317 (hipotecas constituidas) | 2026-10-10 | Provincia (106) | M | 2003–2026-07 | API | no consta | fetch_ine_v2, ca_run |
| ine_vut_nacional_ccaa_prov.csv | INE Estadística experimental VTE 39364 | 2026-10-09 | Nac, CCAA, prov (268) | M (feb/ago hasta 2024; mayo desde 2024-11) | 2020-08–2026-05 | API | no consta | fetch_mivau, build_dataset |
| ine_v2_vut.csv | INE VTE 39363/39364 | 2026-10-10 | Provincia (8.310 series) | M | 2020-08–2026-05 | API | no consta | fetch_ine_v2, r1a_run |
| ine_vut_valencia_municipio.csv / _provincia.csv | INE VTE | 2026-10-09 | Municipio/prov. València | M | 2020-08–2026-05 | API | no consta | fetch_mivau |
| mivau_visados.csv | MIVAU Boletín 32100500 (PROXY viv. libres iniciadas) | 2026-10-09 | Nac, CCAA | M | 2008-01–2026-06 | XLS | sí (plausibilidad) | fetch_mivau, build_dataset |
| mivau_fin_obra.csv | MIVAU Boletín 32101000 (PROXY viv. libres terminadas) | 2026-10-09 | Nac | M | 2008-01–2026-06 | XLS | sí | fetch_mivau, build_dataset |
| mivau_v2_iniciadas_terminadas_prov.csv | MIVAU Boletín (iniciadas/terminadas) | 2026-10-10 | CCAA (18), prov. | M/A | 1991–2026-06 | XLS | no consta | t1_run, t4_run, build_dataset_v2 |
| mivau_v2_protegida.csv | MIVAU Boletín (protegida) | 2026-10-10 | CCAA (19), prov. | M/A | 1991–2026-06 | XLS | no consta | t1_run, t4_run |
| mivau_v2_suelo.csv | MIVAU Boletín (suelo) | 2026-10-10 | CCAA (18) | T | 2004–2026-04 | XLS | no consta | build_dataset_v2, m3_run |
| mivau_parque.csv | MIVAU Boletín (parque) | 2026-10-09 | Nac, CCAA | A | 2001–2025 | XLS | no consta | t1_run, t3_run |
| mivau_fin_obra / mivau_transacciones_* / mivau_transacciones_municipios.csv | MIVAU Boletín (tx notarios: 34010110, 340101i0, 340101j0/k0) | 2026-10-09 | Nac, CCAA (17), municipio (305) | T | 2004–2026T1 (total), 2007–2026T1 (extranjeros, residencia) | XLS | sí (total, extranjeros) | fetch_mivau, build_dataset |
| eurostat_costes.csv | Eurostat sts_copi_q (índice 2021=100) | 2026-10-09 | Nac | T | 1980–2026T1 | API | sí | fetch_eurostat |
| eurostat_produccion_construccion.csv | Eurostat sts_copr_q | 2026-10-09 | Nac | T | 2005–2026T1 | API | sí | fetch_eurostat, m3_run |
| eurostat_permisos.csv | Eurostat sts_cobp_q | 2026-10-09 | Nac | T | 2000–2026T1 | API | sí | fetch_eurostat |
| eurostat_renta_hogares.csv | Eurostat nasq_10_nf_tr | 2026-10-09 | Nac | T | 1999–2026T1 | API | sí | fetch_eurostat |
| eurostat_empleo_nuts2.csv | Eurostat (empleo NUTS2) | 2026-10-09 | NUTS2 (19) | A | 2008–2025 | API | no consta | fetch_eurostat |
| eurostat_inmigracion_anual.csv | Eurostat migr_imm1ctz | 2026-10-09 | Nac | A | 1998–2024 | API | sí (inmig_anual_eurostat) | fetch_eurostat, m2_run |
| eu_hicp.csv, eu_hicp_rent.csv, eu_income_emp.csv, eu_migr_pop.csv, eu_permits.csv, eu_rates.csv | Eurostat (UE) | 2026-10-10 | Países | A/T/M | 2000–2026 | API | no consta | fetch_ue_v2, ca_run |
| ecb_tipo_hipotecario_es.csv | BCE MIR (nuevas op. vivienda) | 2026-10-09 | Nac | M | 2003-01–2026-08 | API | sí | fetch_ecb, build_dataset |
| ecb_nuevo_credito_vivienda_es.csv / ecb_stock_credito_vivienda_es.csv | BCE MIR / BSI | 2026-10-09 | Nac | M | 2003-01–2026-08 | API | sí | fetch_ecb, build_dataset |
| ecb_euribor1y.csv | BCE Euribor 1 año | 2026-10-09 | Euro área | M | 1994-01–2026-09 | API | sí | fetch_ecb |
| ecb_tipo_oficial.csv | BCE MRR (cambios de tipo) | 2026-10-09 | Euro área | cambios (48) | 1999–2026-09 | API | sí | fetch_ecb |
| ecb_hicp_es.csv | BCE IAPC España | 2026-10-09 | Nac | M | 1996-01–2025-12 | API | no consta (serie termina 2025-12) | fetch_ecb, m0_run |
| bde_tipo_hipotecario_referencia.csv | BdE be1901 | 2026-10-09 | Nac | M | 1973-01–2026-09 | descarga | sí | fetch_bde |
| bde_tipos_hipotecas_nuevas.csv | BdE (tipos hipotecas nuevas) | 2026-10-10 | Nac (6 series) | M | 2003-01–2026-08 | descarga | no consta | fetch_bde_v2 |
| bde_credito_finalidad.csv | BdE (crédito por finalidad) | 2026-10-10 | Nac (14 series) | M | 1992-12–2026-08 | descarga | no consta | fetch_bde_v2, m0_run |
| gva_vut_municipio.csv | Generalitat Valenciana registro turismo (CKAN) | 2026-10-09 | Municipio (495) | M | 2010–2026-10 | API | no consta | fetch_gva, r1a_run |
| gva_padron_extranjeros_municipio.csv | IVE padrón (CKAN, distritos/municipio) | 2026-10-09 | Municipio (543) | A | 2005–2022 | API | no consta | fetch_gva |
| ine_padron_valencia.csv / ine_padron_vlc_nacionalidad.csv | INE padrón València | 2026-10-09 | Municipio (València) | A | 1996–2026-07 / 1998–2022 | API / PC-Axis | no consta | fetch_padron_valencia |
| ine_diccionario_municipios_2026.xlsx | INE diccionario de municipios | — | — | — | 2026 | descarga | — | build_dataset_v2 |
| catastro_urbana_municipios.csv (+ .gz) | Catastro, Datos municipios (Urbano) | 2026-10-10 | Municipio (7.610), prov. | A | 2011-12–2025-12 | descarga | no consta | build_dataset_v2, k4b_run |
| v2_eventos_politica.csv | BOE / boletines (41 eventos) | 2026-10-10 | CCAA, prov., municipio | evento | 2013-06–2026-07 | manual | no consta | build_dataset_v2, build_eventos |
| v2_zonas_tensionadas.csv | BOE/CCAA (318 declaraciones) | 2026-10-10 | Municipio | evento | 2024-03–2026-07 | manual | no consta | build_dataset_v2, build_eventos |
| pdf/notariado_cgn_extranjeros_semestral.csv | Consejo General del Notariado (CIEN, XLSX) | — | Nac (categoría extranjero) | S | 2007S1–2025S2 | PDF/XLSX extraído | sí (validacion) | extract_notariado |
| pdf/notariado_cv_prov_trimestral.csv | Notariado (PDF, CV) | — | Provincia (solo CV) | T | 2018Q1–2025Q4 | PDF extraído | sí | extract_notariado |
| pdf/notariado_cv_municipios_anual.csv | Notariado (PDF, CV) | — | Municipio (solo CV) | A | 2021–2025 | PDF extraído | sí | extract_notariado |
| pdf/notariado_cv_actos_mensual.csv | Notariado (PDF, CV) | — | CV | M | 2019-01–2026-03 | PDF extraído | sí | extract_notariado |
| pdf/registradores_opendata_anual.csv | Colegio de Registradores (OpenData) | — | Nac | A | 2007–2025 | CKAN/PDF | sí (validacion) | extract_registradores |
| pdf/registradores_opendata_compraventas.csv | Registradores (ventanas) | — | nivel no verificado | T | 2007Q1–2026Q1 | CKAN | sí | extract_registradores |
| pdf/registradores_eri_anuario.csv | Registradores, Anuario ERI | — | Nac (% extranjeros) | A | 2016–2025 | PDF extraído | sí | extract_registradores |
| pdf/serpavi_esp_agregado.csv / serpavi_ccaa.csv / serpavi_provincias.csv | MIVAU-SERPAVI (AEAT IRPF), XLSX | — | Nac, CCAA, prov. | A | 2011–2024 | XLSX extraído | sí (validacion) | extract_serpavi |
| pdf/serpavi_municipios_46.csv / serpavi_v2_municipios.csv (+ .gz) | SERPAVI | — | Municipio (46 / 32.402 series) | A | 2011–2024 | XLSX extraído | sí / no consta | extract_serpavi, extract_serpavi_v2 |
| pdf/serpavi_valencia_distritos / secciones.csv | SERPAVI | — | Distrito / sección (València) | A | 2011–2024 | XLSX extraído | sí | extract_serpavi_v2 |
| v2_orig/ (catastro, mivau), gva_orig/ (padrón distritos 2005–2022 zip; VUT histórico 2025; vut_lista_actual) | Originales sin procesar | — | — | — | — | — | — | solo entrada |
| mivau_xls/ (11 XLS: 32100500, 32101000, 33100500, 34010110, 340101d0/i0/j0/k0, 34010210, 35101000, 35103500) | MIVAU Boletín | 2026-10-09 | — | — | — | origen de los CSV anteriores | — | fetch_mivau |
| ine_padron_pcaxis/ (51 ficheros PC-Axis 1998–2019; 00046004/5 y 00046002/3) | INE padrón (PC-Axis) | — | Municipio/València (alcance no verificado) | A | 1998–2019 | PC-Axis | no consta | fetch_padron_valencia |

### 1.2 Subcarpetas de versiones

| Carpeta | Contenido principal | Fuente | Periodo | Scripts |
|---|---|---|---|---|
| v3/ (23) | airbnb_insideairbnb_agregados (2025-12–2026-09, anuncios activos); hut_registro_turismo_cat (Catalunya, snapshot 2026-10); incasol_fianzas_municipio (138.315 filas, 2007–2026-01, por banda); eff_tenencia_edad (BdE EFF, 2002–2022); ine_ecv_tenencia_edad (2004–2025); eurostat_emancipacion (2004–2025); ine_v3_censo2021 (municipio y sección, 2021); ine_v3_vut_municipio_pct (2020-08–2026-05); ine_v3_vut_seccion (145.101 filas, 2021-02–2026-05); ine_v3_gis_seccion (ADRH/censo, 2019–2025); serpavi_distritos/secciones_nacional (2011–2024); madrid_alquiler_cp (2023–2024, origen no verificado); zonas_tensionadas_v3 (BOE/CCAA); eventos_v3 (8 eventos); cataluna_contencion_rentas_v3 (2020-09–2024-10) | Mixta: INE, BdE, Eurostat, Incasòl (Socrata), HUT Catalunya, Inside Airbnb, BOE | — | k4b_run, l1_verifica, m0_run, r1a_run, fetch_*_v3 |
| v4/ (6) | catastro_solares_municipios (114.065 filas, 2012–2026, municipio); ine_v4_t50256, t50272, t59523, t59529 (INE Tempus); medidas_programas | Catastro, INE | 2006–2026 | m3_fetch, m3_run, l1_verifica |
| v5/ (57) | Tablas CA (ca_*: BdE be0418, ECB, Eurostat demo/ilc), cb_* (AEAT IRPF 2019–2024 y IRPFviv 2024; CGPJ lanzamientos 2013–2025 y series TSJ 1T2026; INE ECV t9997; t59953), cc_* (BOE legislación 1992–2026; Eurostat ilc_lvho07b/c, lvho28), gva_fianzas_2020–2022, a4_mbc_rd1020 y d3_referencias | Mixta | Variable | ca_run, cb_run, cc_run, d3 |
| v5_1/ (2) | ine_t2_t6154.csv (ETDP 6154, transmisiones por título); t1/ | INE | — | T1/T2 |
| v3_orig/ (10) | Originales (C2021 indicadores, censo API, Eurostat json, ine_t39366, ine_t59525, madrid_alquiler_cp_1934258, vut_seccion, GIS) | — | — | — |
| vlc_fuente/ (1) | precio_vivienda-cas.csv (fuente de vlc_precio_vivienda_libre) | Ajuntament València | 2021–2022 | fetch_valencia |

Cómputo del `_manifest_series_ine_v2.csv` (18.090 series, por tabla/fuente, solo agregados): INE VTE 39364 y 39363 (8.310), INE EM/EMCR 24420-24421 (3.922), INE IPVA 59058/59005/59059/59060/59061 (3.420), ECP 77023 población por edad y nacionalidad (795), ECP 77023 población por provincia y país (742), ECP hogares 60133 (265), ETDP 6150 (265), EPA 65345 (106), HPT 76317 (106), IPC alquiler 76142 (106), CRE 80109 (53).

## 2. Paneles procesados

Notas generales: `panel_ccaa_q` y `nacional_q` cubren 1995–2026; el `*_metodo` distingue observado / agregado / interpolado_loglineal / anual_asignado / desestacionalizado_stl; sólo `pob_*` tiene interpolación real (la bandera `_interp` vale 1 sólo para `pob_*`; `compraventas_interp`, `visados_interp`, `terminadas_interp`, `ipc_alquiler_interp` valen 0 en 2007+).

| Fichero | Dimensiones | Periodo | Columnas (resumen) | % NaN relevantes |
|---|---|---|---|---|
| data/processed/nacional_q.csv | 127 × 195 (T) | 1995Q1–2026Q3 | ipv, ipv_nueva/usada, ipv15, p_tasado, p_bde, hpi_eurostat, ocupados(_sa), renta_hog(_real), deflactor, ipc_alquiler(_yoy), credito_nuevo/stock, permisos, costes, prod_constr, visados, terminadas, compraventas(_sa), trans_total/extranjeros, pob_total/extranj, hogares_epa/ecp, tipo_hip, euribor, tipo_bce, tipo_hip_real, inflacion_deflactor, inmig_anual, registradores_*, notariado_cgn_extranj, serpavi | ipv 39; hpi_eurostat 35; visados 43; terminadas 42; compraventas 39; prod_constr 32; credito 26; ocupados 23; renta_hog 13; resto ≤1 |
| data/processed/nacional_a.csv | 28 × 44 (A) | 1998–2025 | ipv, ocupados, pob_extranj, hogares_epa, terminadas, visados, inmig_anual_eurostat, inmig_anual, quiebres 2021, ln_/d_ln_ | inmig_anual 86; visados 43; terminadas 36; ipv 32 |
| data/processed/panel_ccaa_q.csv | 2.142 × 78 (17 CCAA × 126 T) | 1995Q1–2026Q2 | ipv(_nueva/_usada), p_tasado, ocupados, compraventas, trans_total/extranjeros, visados, terminadas, ipc_alquiler, pob_total/extranj/espanola (+_metodo, _interp), epa_pob_total, ln_/d_/d4_ | ipv 38; compraventas 38; trans_extranjeros 38; visados 43; terminadas 41; pob_* 26 (sobre el total); ocupados 22 |
| data/processed/panel_ccaa_a.csv | 408 × 104 (17 × 24) | 2002–2025 | pob_* por origen (total, extranj., española, continentes, UE), ipv, p_tasado, ocupados, compraventas, trans, visados, terminadas, ipc_alquiler, serpavi_vc_mediana, notariado_cgn_extranj, registradores_extranj_pct, *_metodo, *_interp | ipv 21; visados 33; terminadas 25; serpavi 47; registradores_extranj_pct 58 |
| data/processed/panel_ccaa_nacionalidad.csv | 5.610 × 9 (T, CCAA × nacionalidad) | 2002Q1–2026Q3 | inmig_flujo, pob_stock, tipo_registro, serie_ine | inmig_flujo 87; pob_stock 13 |
| data/processed/valencia.csv | 3.610 × 10 (formato largo: territorio, variable, valor, origen, rol, validado, metodo, interp) | 1995Q1–2026Q2 | 23 territorios | sin NaN |
| data/processed/validacion_gva.csv | 12 × 8 (controles) | — | bloque, check, error_max | error_max 42% (esperado) |
| data/processed/v2/train/nacional_q_v2.csv | 118 × 239 (T) | 1995Q1–2024Q2 | versión v2 de nacional_q | ipv 41; visados 46; terminadas 44 |
| data/processed/v2/train/panel_prov_q.csv | 4.410 × 182 (49 cód. prov. × T) | 2002Q1–2024Q2 | p_tasado(_suelo), ipc_alquiler, compraventas_*, hipotecas, iniciadas, terminadas, pob, paro, etc. (+_metodo/_interp) | p_tasado 1; p_suelo 13; compraventas 22 |
| data/processed/v2/train/panel_prov_a.csv | 1.078 × 182 (49 cód. × A) | 2002–2023 | p_tasado, p_suelo, ipc_alquiler, ocupados, parados, compraventas_*, hipotecas_*, iniciadas/terminadas_libres, protegida, pob_*, vut_* | zona_tensionada_share 100; iniciadas 39; terminadas 30; protegida 30; compraventas 23; p_suelo 14 |
| data/processed/v2/train/panel_muni_a.csv | 71.720 × 38 (3.258 municipios × A) | 2002–2023 | serpavi_mediana_vc/vu, serpavi_n_*, p_tasado, trans_total, vut_viviendas, uu_residenciales, ipva_*, zona_tensionada, metodo_*, ln_* | zona_tensionada 100; ipva 88–89; p_tasado 93; trans 92; serpavi_vc 65 |
| data/processed/v2/train/panel_ue_a.csv | 682 × 77 (31 países × A) | 2002–2023 | hpi (BIS, OCDE), precio/ingreso, precio/alquiler, alquiler HICP, permisos, inmig_por_1000 | hpi 25; hpi_oecd 22; precio_ingreso 22 |
| data/processed/v2/train/panel_ue_q.csv, eventos_q.csv, nacional_q_v2 | — | — | eventos_q: 3.150 filas (trimestre × evento, 2002Q1–2024Q2, dummy_vigente) | codigos_ine_* 57 (ámbito nacional) |
| data/processed/v3/sellado_v3.json | Metadatos de partición v3 (fracción 0,2; semilla 20261010; última oleada 2026M05) | — | — | — |

Nota: `panel_prov_a` tiene 49 códigos de provincia distintos (no 52); no se ha verificado cuáles faltan. Los metadatos de partición train/sellado se leen sólo como metadatos (no se ha abierto `data/sealed`).

### 2.1 Paneles de entrenamiento output/v6/M0/paneles/*_train.csv.gz (M0)

| Fichero | Dimensiones | Periodo | Columnas | % NaN |
|---|---|---|---|---|
| nacional_trim_desc.csv / nacional_anual_a23_desc.csv | nacional, desc. | — | — | — (no leídos en esta pasada) |
| ccaa_ipv_anual_desc.csv, ccaa_seguridad_juridica_transversal_desc.csv | CCAA, desc. | — | — | — (no leídos) |
| prov_compra_anual_train.csv.gz | 410 × 27 (41 prov. × 10 A) | 2015–2024 | ln_pm2_tasado, ln_pm2_registradores, ln_cv_etdp, ln_cv_registradores, share_nueva_etdp, ln_hip_viv_num, share_contado_proxy, share_compra_ext_res_pct, no_res_share_R1A_pct, ln_pob, share_ext_pob, share_20_34, jefatura_proxy_pct, paro_tasa, ln_ocupados_miles, ln_pib_pc, ln_vut, ln_terminadas_libres, ln_iniciadas_libres, bajas_tasa_C_amplia_pct, ln_suelo_pm2_m50k, ln_llegada_total_ext | no_res_share_R1A 81; jefatura_proxy 60; ln_suelo 64; ln_vut 50; ln_llegada_total_ext 30 |
| prov_alquiler_anual_train.csv.gz | 369 × 13 (41 × 9) | 2015–2023 | ln_alq_m2_serpavi_vc, ln_alq_mes_serpavi_vc, ln_n_contratos_serpavi_vc, ln_ipc_alq_idx, d_ln_ipc_alq, ln_ratio_precio_alquiler, rentabilidad_bruta_pct, ln_vut, n_mun_tensionados, n_mun_topes_cat | ln_vut 56; d_ln_ipc 11; resto ≈7 |
| prov_contratos_nuevos_anual_train.csv.gz | 369 × 8 | 2015–2023 | ln_fianza_media_gva_eur, ln_n_fianzas_gva, pct_fianzas_600_incasol, ln_n_fianzas_incasol, ln_ipva_nuevo_idx | 69–97 |
| prov_trim_compra_train.csv.gz | 1.640 × 12 (41 × 4 T × 10 A) | 2015–2024 | ln_pm2_tasado, ln_cv_etdp, ln_ipc_alq_idx, ln_hip_viv_num (+ niveles) | ninguna |
| mun_compra_anual_train.csv.gz | 20.530 × 4 | 2015–2024 | ln_pm2_tasado_mun | 91 |
| mun_alquiler_anual_train.csv.gz | 18.181 × 6 | 2015–2023 | ln_alq_m2_serpavi_mun, tensionada_mun, tope_cat_mun | 19 |
| mun_contratos_anual_train.csv.gz | 18.181 × 7 | 2015–2023 | ln_fianza_media_gva_mun, ln_n_fianzas_gva/incasol, pct_fianzas_600_incasol | 58–95 |
| dis_alquiler_anual_train.csv.gz | 40.673 × 7 (distrito, 41 prov.) | 2011–2023 | ln_alq_m2_serpavi_dis, p25/p75, ln_vut_plazas_dis | serpavi 32; vut 67 |
| prov_estatico.csv, mun_estatico.csv, potencia.csv, cobertura_train.json, hechos.json | estáticos / metadatos | — | — | — |

Los paneles M0 tienen 41 provincias, no 52: el panel de compra y alquiler se limita a las provincias con cobertura en fianzas/SERPAVI.

## 3. Matriz de cobertura (variable × nivel × frecuencia)

Celdas: frecuencia (T/M/S/A) y periodo disponible. "—" = no existe en data/raw ni en processed. "PROXY" = proxy declarado.

| Variable | Nacional | CCAA | Provincia | Municipio | Distrito / Sección |
|---|---|---|---|---|---|
| Precio IPV (INE) | T 2007Q1–2026Q2 | T 2007Q1–2026Q2 (17) | — | — | — |
| Valor tasado MIVAU (p_tasado) | T 1995Q1–2026Q2 | T 1995Q1–2026Q2 | A 2002–2023 (panel_prov_a) | T 2005–2026T1 (309 series) | — |
| Precio BdE (p_bde) | T 1995Q1–2026Q2 | — | — | — | — |
| Notariado (CGN) | S 2007S1–2025S2 (extranj.) | — (CV: M 2019–2026-03) | CV: T 2018–2025T4 | CV: A 2021–2025 | — |
| Registradores (compraventas, anual) | A 2007–2025 | — | — | — | — |
| Registradores (ventanas trimestrales) | T 2007Q1–2026Q1 (nivel no verificado) | — | — | — | — |
| Registradores (ERI, % extranjeros) | A 2016–2025 | — | — | — | — |
| IPC alquiler | M 2002-01–2026-08; T 2002Q1–2026Q2 | T 2002Q1–2026Q2 (17) | M 2002–2026-08 (ine_v2) | — | — |
| SERPAVI (alquiler, €/m²) | A 2011–2024 | A 2011–2024 | A 2011–2024 | A 2011–2024 (32.402 series; 46 mun. en CSV aparte) | Distritos A 2011–2024 (València y nacional); secciones A 2011–2024 (nacional, 398k filas) |
| IPVA (índice alquiler INE) | A 2011–2024 | A 2011–2024 | A 2011–2024 | A 2011–2024 (1.530) | — |
| Fianzas de alquiler | — | CAT (Incasòl, 2007–2026-01); CV (GVA, 2020–2026); MAD, EUS, BAL no disponible | CV/CAT derivado A 2015–2023 | CV/CAT A 2007–2026 (Incasòl por banda) | — |
| Empleo (ocupados) | T 2002Q1–2026Q1 (EPA); desest. (_sa) | T 2002Q1–2026Q1 (17) | T 2002Q1–2026Q1 (106, ine_v2_epa) | — | — |
| Paro (parados) | nac: derivable de EPA (no verificado en el raw); T | CCAA: no verificado | A 2002–2023 (panel_prov_a, parados) | — | — |
| Renta de hogares | T 1999Q1–2026Q1 (Eurostat); INE renta disponible T 1999Q1–2026Q1 | — | — | — | — |
| PIB | T 1995Q1–2026Q1 (INE CNT corr./vol.) | A 2000–2025 (ine_v2_cre, 17 CCAA) | A 2000–2025 (ine_v2_cre, 53 cód.) | — | — |
| Población | T 2002–2025 (ECP, 2021+ trimestral; 1 ene/jul antes); A 1971–2026 | T 2002–2025 (ECP 77023, 1 ene; interp. T2–T4); EPA T 2002–2026T1 | A 2002–2026-01 (ine_v2_padron_prov_pais) | Valencia A 1996–2026 (ine_padron_valencia) | — |
| Llegada neta / inmigración | A 2021–2024 (EMCR 69687); A 1998–2024 (Eurostat); S 2023S1–2026S1 (nacionalidad) | S 2023S1–2026S1 (ccaa × nacionalidad) | A 2008–2022 (ine_v2_migraciones, 3.922 series) | — | — |
| Extranjeros (stock) | T 2002–2025 (ECP701, interp. desde 2021) | T 2002–2025 (ECP701 por CCAA, 17) | A 2002–2026-01 (padrón por país) | A 2005–2022 (GVA, 543 mun.); València A 1998–2022 | — |
| Hogares | T 2002Q1–2026Q1 (EPA; serie principal); T 2021Q1–2026Q3 (ECP 60131, solo nacional, sin retropolación) | — (no trimestral CCAA) | T/A 2021–2026 (ine_v2_hogares_prov) | — | — |
| Tipo hipotecario | M 2003-01–2026-08 (BCE MIR); M 1973–2026-09 (BdE); T mediana (agregado) | — | — | — | — |
| Nuevas hipotecas / crédito | M 2003-01–2026-08 (crédito nuevo y stock BCE); M 1992-12–2026-08 (BdE finalidad, 14 series); M 2003–2026-08 (BdE tipos) | — | M 2003–2026-07 (ine_v2_hipotecas, constituidas) | — | — |
| Compraventas (total) | M 2007-01–2026-07 (ETDP); T agregado | M 2007-01–2026-07 (17 CCAA, ETDP 6150) | M 2007–2026-07 (ine_v2_etdp, 265 series) | — (Notariado/MIVAU municipal, no ETDP) | — |
| Compraventas extranjeros | T 2007Q1–2026Q1 (MIVAU tx extranjeros); Notariado S 2007–2025 | T 2007Q1–2026Q2 (17) | — | — | — |
| Compraventas al contado | — (no hay serie nativa; proxy `share_contado_proxy` en panel prov. anual, NaN 3%) | — | proxy A 2015–2024 | — | — |
| Terminadas (PROXY libres) | M 2008-01–2026-06 (fin_obra); T 2008Q1–2026Q2 | T 2008Q1–2026Q2 (17) | M/A 1991–2026-06 (iniciadas_terminadas_prov) | — | — |
| Iniciadas (PROXY, visados) | M 2008-01–2026-06 (visados); T 2008Q1–2026Q2 | T 2008Q1–2026Q2 (17) | M/A 1991–2026-06 (iniciadas_terminadas_prov) | — | — |
| Licencias de obra (tabla MIVAU) | — (fallido; sin serie nacional reciente) | Endpoint identificado (1002NN30, hasta 2022); no descargado | — (endpoint provincial, sin dato) | — | — |
| Costes de construcción | T 1980Q1–2026Q1 (Eurostat sts_copi_q, 2021=100); sin ICC INE | — | — | — | — |
| VUT (viviendas turísticas) | M 2020-08–2026-05 (INE experimental) | M 2020-08–2026-05 (17) | M 2020-08–2026-05 (ine_v2_vut, 8.310 series); GVA registro M 2010–2026-10 | Municipio: INE 2020-08–2026-05 (8.207 filas); GVA 2010–2026 (495 mun.); HUT Catalunya snapshot 2026-10 | Sección: INE 2021-02–2026-05 (145k filas); distrito València VUT plazas (SERPAVI-dis) |
| Eventos regulatorios | v2_eventos_politica (41, 2013–2026-07, ámbito nac./CCAA/prov.) | Id. (CCAA en v2_eventos) | Codigos INE provincia (12 códigos en eventos) | v2_zonas_tensionadas (318 declaraciones, 2024-03–2026-07; municipio) | — |
| Catastro | A 2011-12–2025-12 (agregado) | A 2011–2025 (por CCAA, derivable) | A 2011–2025 (derivable, catastro_urbana) | A 2011–2025 (7.610 cód.); solares A 2012–2026 (v4) | — |

Observación de cobertura: la mayoría de las variables de vivienda son de nivel nacional o CCAA; provincial es sólo para INE (EPA, ETDP, IPC, IPVA, hipotecas, padrón, PIB CRE, VUT), SERPAVI y Catastro; municipal sólo para valor tasado, SERPAVI, IPVA, VUT, Catastro, GVA (CV) y fianzas (CAT y CV). Notariado y Registradores no tienen cobertura territorial completa (Notariado sólo CV a nivel municipal y provincial).

## 4. Panel trimestral CCAA desde 2007 y panel anual provincial

### 4.1 Trimestral por CCAA (panel_ccaa_q, 17 CCAA × 2007Q1–2026Q2, 78 cols)

Completas (NaN 0% desde 2007Q1, observadas o agregadas):
- ipv, ipv_nueva, ipv_usada (INE IPV, 2007Q1–2026Q2)
- trans_extranjeros (MIVAU, 2007Q1–2026Q2)
- compraventas (ETDP suma 3 meses; NaN 0%, sin interpolación)
- ipc_alquiler (INE IPC; NaN 0% desde 2002Q1)
- ocupados (EPA; NaN 0% desde 2002Q1, cambio base 2021 documentado)
- epa_pob_total (EPA, NaN 0%)

Con huecos menores (NaN 1–8%):
- p_tasado (1%, MIVAU 1995Q1–2026Q2)
- trans_total (2%, 2004Q1–2026Q1; no cubre 2026Q2)
- terminadas (5%, 68 filas NaN; proxy MIVAU)
- visados (8%, 102 filas NaN; proxy MIVAU, no visados CSCAE)

Interpoladas o asignadas (no observadas trimestralmente):
- pob_total, pob_extranj, pob_espanola (6% NaN; 2002Q1–2025Q1): 918 filas con `interpolado_loglineal` (bandera `_interp`=1), 323 filas `anual_asignado`; el último dato es 2025Q1, no llega a 2026.
- compraventas_interp, visados_interp, terminadas_interp, ipc_alquiler_interp: bandera presente pero valor 0 en 2007+; son agregados, no interpolaciones.
- Las columnas `*_metodo` distinguen la transformación; sólo pob_* usa interpolación.

No existen trimestrales por CCAA en el panel (sólo nacional o anual/semestral):
- PIB por CCAA (sólo anual, ine_v2_cre)
- Renta de hogares por CCAA (no hay serie Eurostat/INE trimestral por CCAA)
- Hogares por CCAA (ECP 60131 sólo nacional; ine_v2_hogares_prov es provincial)
- Hipotecas/crédito por CCAA trimestral (sólo provincial mensual en ine_v2_hipotecas, o nacional BCE/BdE)
- Tipo hipotecario por CCAA (sólo nacional)
- Costes de construcción por CCAA (sólo nacional, Eurostat)
- Licencias de obra (no descargadas; intento fallido)
- Notariado y Registradores por CCAA trimestrales (Notariado CV mensual sólo para CV)
- Parados por CCAA (no consta en el panel)
- SERPAVI y IPVA por CCAA (sólo anual)

### 4.2 Anual provincial (panel_prov_a, 49 códigos, 2002–2023)

Hay 49 códigos de provincia distintos en el fichero, no 52. Completas o casi (NaN ≤5%): p_tasado (1%), hipotecas_n e importe (5%), ipc_alquiler, ocupados, parados, pob_total, pob_extranj.

Con huecos relevantes:
- p_suelo (14%), compraventas_* (23%), terminadas_libres (30%), protegida (30%), iniciadas_libres (39%).
- zona_tensionada_share (100%, sin datos en el panel; ver v2_zonas_tensionadas a nivel municipal).

Interpolaciones: `panel_prov_q` (2002Q1–2024Q2) lleva banderas `_metodo` e `_interp` por variable; `panel_prov_a` no tiene banderas de interpolación en su versión anual.

Presentes además en panel_prov_a (verificado por columnas): parados, hipotecas_n/importe, vut_viviendas, serpavi_* (mediana y nº inmuebles vc/vu), ipva_indice/var, pib_prov, pib_pc, y sus versiones ln_ / d_ln_. Verificado: panel_prov_a no tiene columnas `_interp` ni `_metodo` salvo `vut_viviendas_metodo`.

Ausentes en provincial anual del panel: Notariado (sólo CV en su PDF), Registradores (sólo nacional o agregado CCAA), renta de hogares (no hay), costes de construcción (sólo nacional), licencias de obra (no existen).

Paneles de 41 provincias (output/v6/M0, 2015–2024/2023): cobertura más corta; el panel de compra incluye pm2 tasado, cv ETDP, hipotecas y tasa de paro; el de alquiler incluye SERPAVI 2015–2023.

## 5. Fuentes fallidas y solicitudes pendientes (compacto)

Fallidas (sin fichero o sin acceso verificado):
- MIVAU licencias de obra, nacional o provincial (Boletín, endpoint sin tabla) y CCAA (serie hasta 2022, no descargada).
- MIVAU SIU (suelo urbanizable, capacidad residencial por municipio): connect_rejected.
- MIVAU ruina, cambios de uso, agregaciones: sin endpoint.
- MIVAU Registro Único de Arrendamientos: 403 (sin datos).
- Catastro titulares persona física/jurídica por municipio o provincia: consulta dinámica (jaxi); sin fichero abierto.
- AEAT IRPF por municipio (capital inmobiliario): consulta dinámica; error TLS en agenciatributaria.es.
- INE: ECH (no existe), renta disponible de hogares trimestral (no existe a nivel hogares), inmigración total trimestral (no publicada), inmigración trimestral por CCAA sin nacionalidad (no localizada); Tabla 69691 (EMCR por CCAA) pendiente.
- INE ICC (índice de costes de construcción): no existe en Tempus.
- INE ECV y EPA tenencia por edad de la persona de referencia; Censo 2021 por edad de la persona de referencia y por sección (CENSOP 463, CENSOPV 8, 404 de la API del censo).
- INE ADRH por sección (redirige), tabla de variaciones del seccionado (no localizada).
- INE VUT por sección en algunas tablas (ver v3 fuentes_fallidas).
- BdE: esfuerzo teórico anual (no encontrado), índices de vivienda 404, carpeta csv 403, EFF microdatos (solicitud), EFF 2014/2017 artículo (404).
- BCE: IAPC España termina 2025-12 (estado E); tipo BCE MRR de fechas de cambio (48 obs.).
- Valencia/GVA: fianzas GVA con bloqueo de proxy (ws_closed) en v3; fianzas CV disponibles en v5 (2020–2026).
- Madrid, Euskadi, Baleares: fianzas sin dato (0 resultados o 404); Barcelona opendata: anti-bot; Google Trends: sin API.
- Portales inmobiliarios (Idealista, Fotocasa, MESVAL): no consultados o privados.
- Registro de Turismo Catalunya con fechas de alta/baja: dataset sin columnas necesarias.
- Inside Airbnb: instantáneas anteriores a 2025-12 no descargadas.
- Notariado: compradores persona jurídica (sin dato); fuera de CV sin cobertura territorial.
- Registradores: compras por personas jurídicas (sin serie).
- Programa electoral y proposiciones de ley (v4 M5a): fuera de alcance, pendientes.

Pendientes de solicitud formal (docs/v5/solicitudes.md, sin respuesta registrada; tarea del autor):
- S1 Catastro: inmuebles residenciales por municipio y naturaleza del titular.
- S2 SIU (MITMA): suelo urbanizable 2016–2025 por municipio.
- S3 AEAT: IRPF capital inmobiliario por municipio.
- S4 Registros autonómicos de fianzas (CAT, CV, Madrid, Euskadi, Baleares).
- S5 Licencias de obra (PEM por m²).
- S6 Registro Único de Arrendamientos (contratos de corta duración).
- S7 INE: tabulación a medida de Censos 2011 y 2021 (hogares, hacinamiento, vacías).
- S8 Ayuntamientos grandes ciudades: plazo medio de licencias.
- S9 Portales inmobiliarios e Inside Airbnb histórico 2012–2016.
- S10 CGPJ y Ministerio del Interior: duración de juicios de desahucio.
