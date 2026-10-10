# Diccionario de variables v2 (generado por src/build_dataset_v2.py)

Generado automáticamente. Fuentes en data/raw; ningún dato de PDF/OCR no validado entra en el panel principal.

Convenciones: `<var>_metodo` ∈ {observado, agregado_media, agregado_suma, fin_periodo, escalonado, interpolado_loglineal, anual_asignado, semestral_asignado, derivado}; `<var>_interp` = TRUE solo si interpolado_loglineal (entre dos observaciones). Huecos al final y fuera de rango = NaN.

## Registro de variables

| panel | variable | fuente | archivo raw | tabla | unidad | frecuencia original | agregación | método | notas |
|---|---|---|---|---|---|---|---|---|---|
| prov_q | p_tasado | MIVAU Boletín Online (sedal) valor tasado vivienda libre | mivau_valor_tasado_nacional_ccaa_prov.csv | 35101000 | €/m² | trimestral | ninguna | observado | serie provincial; en uniprovinciales (Balears, Illes, Rioja, La, Madrid, Murcia, Navarra, Asturias, Cantabria, Ceuta, Melilla) se usa la serie de la CCAA (CCAA = provincia) |
| prov_q | p_suelo | MIVAU Boletín Online (sedal) precio medio suelo urbano | mivau_v2_suelo.csv | 36400500 | €/m² | trimestral | ninguna | observado | serie provincial de todos los municipios (no la de municipios >50.000 hab., tabla 36403000); uniprovinciales (Balears, Illes, Rioja, La, Madrid, Murcia, Navarra, Asturias, Cantabria) con serie CCAA |
| prov_q | ipc_alquiler | INE IPC subclase alquiler de vivienda | ine_v2_ipc_alquiler_prov.csv | 76142 | índice (base INE) | mensual | media de 3 meses (NaN si falta alguno) | agregado_media |  |
| prov_q | compraventas_total | INE ETDP compraventas de viviendas | ine_v2_etdp_prov.csv | 6150 | número de compraventas | mensual | suma de 3 meses (NaN si falta alguno) | agregado_suma |  |
| prov_q | compraventas_nueva | INE ETDP compraventas de viviendas | ine_v2_etdp_prov.csv | 6150 | número de compraventas | mensual | suma de 3 meses (NaN si falta alguno) | agregado_suma |  |
| prov_q | compraventas_usada | INE ETDP compraventas de viviendas | ine_v2_etdp_prov.csv | 6150 | número de compraventas | mensual | suma de 3 meses (NaN si falta alguno) | agregado_suma |  |
| prov_q | compraventas_libre | INE ETDP compraventas de viviendas | ine_v2_etdp_prov.csv | 6150 | número de compraventas | mensual | suma de 3 meses (NaN si falta alguno) | agregado_suma |  |
| prov_q | compraventas_protegida | INE ETDP compraventas de viviendas | ine_v2_etdp_prov.csv | 6150 | número de compraventas | mensual | suma de 3 meses (NaN si falta alguno) | agregado_suma |  |
| prov_q | hipotecas_n | INE HPT hipotecas sobre fincas viviendas (base nueva) | ine_v2_hipotecas_prov.csv | 76317 | número | mensual | suma de 3 meses | agregado_suma |  |
| prov_q | hipotecas_importe | INE HPT hipotecas sobre fincas viviendas (base nueva) | ine_v2_hipotecas_prov.csv | 76317 | miles de euros (NO VERIFICADO: inferido de magnitud) | mensual | suma de 3 meses | agregado_suma | unidad no verificada contra metadatos de la API |
| prov_q | ocupados | INE EPA ocupados/parados por provincia | ine_v2_epa_prov.csv | 65345 | miles de personas | trimestral | ninguna | observado |  |
| prov_q | parados | INE EPA ocupados/parados por provincia | ine_v2_epa_prov.csv | 65345 | miles de personas | trimestral | ninguna | observado |  |
| prov_q | iniciadas_libres | MIVAU Boletín Online viviendas libres iniciadas (mensual) | mivau_v2_iniciadas_terminadas_prov.csv | 32100500 | viviendas | mensual | suma de 3 meses | agregado_suma |  |
| prov_q | terminadas_libres | MIVAU Boletín Online viviendas libres terminadas (mensual) | mivau_v2_iniciadas_terminadas_prov.csv | 32101000 | viviendas | mensual | suma de 3 meses | agregado_suma |  |
| prov_q | protegida | MIVAU Boletín Online calificaciones definitivas VPO (mensual) | mivau_v2_protegida.csv | 31205000 | viviendas | mensual | suma de 3 meses | agregado_suma |  |
| prov_q | vut_viviendas | INE Estadística experimental VTE (viviendas turísticas), provincias | ine_v2_vut.csv | 39364 | número de viviendas turísticas | semestral irregular (meses 02/05/08/11 en la serie) | sin agregación: valor del mes observado asignado a su trimestre (Feb→T1, May→T2, Ago→T3, Nov→T4) | observado | sin interpolación; trimestres sin observación = NaN |
| prov_q | pob_total | INE ECP población residente 1 de enero (77023) | ine_v2_padron_prov_edad_nac.csv | 77023 | personas | anual (1 enero) -> trimestral | T1 = 1 de enero; T2-T4 interpolados | observado (T1) / interpolado_loglineal (T2-T4) |  |
| prov_q | pob_extranj | INE ECP población residente 1 de enero (77023) | ine_v2_padron_prov_edad_nac.csv | 77023 | personas | anual (1 enero) -> trimestral | T1 = 1 de enero; T2-T4 interpolados | observado (T1) / interpolado_loglineal (T2-T4) |  |
| prov_q | pob_20_34 | INE ECP población residente 1 de enero (77023) | ine_v2_padron_prov_edad_nac.csv | 77023 | personas | anual (1 enero) -> trimestral | T1 = 1 de enero; T2-T4 interpolados | observado (T1) / interpolado_loglineal (T2-T4) | grupo 20-34 años, total nacionalidades |
| prov_q | inmig_flujo | INE EM inmigración procedente del extranjero, provincia (24420) | ine_v2_migraciones_prov.csv | 24420 | personas (flujo semestral) | semestral (2008S1-2022S1) | semestre asignado al último trimestre del semestre (S1→T2, S2→T4) | semestral_asignado | sin repartir entre trimestres |
| prov_q | zona_tensionada_share | BOE declaraciones de zona tensionada (Ley 12/2023 art. 18) + Catastro uu residenciales por municipio | v2_zonas_tensionadas.csv; catastro_urbana_municipios.csv.gz | — | fracción [0,1] | declaración (escalonada) | peso = unidades urbanas residenciales del municipio (año de stock disponible más cercano) | escalonado | NaN antes de 2024T1 (sin declaraciones en el fichero). Municipios fuera del fichero = 0 desde 2024 (supuesto de cobertura completa del fichero). NaN en provincias sin pesos catastrales (País Vasco y Navarra no aparecen en Catastro estatal). |
| prov_q | zona_tensionada_any | BOE declaraciones de zona tensionada (Ley 12/2023 art. 18) | v2_zonas_tensionadas.csv | — | 0/1 | declaración (escalonada) | 1 si algún municipio de la provincia está declarado (sin ponderar) | escalonado | NaN antes de 2024T1. Incluye País Vasco y Navarra (sin pesos catastrales en zona_tensionada_share). |
| prov_q | ratio_precio_alquiler_idx | derivado | — | — | índice (diferencia de logs) | trimestral | ln p_tasado − ln ipc_alquiler | derivado | índice relativo; no es un nivel de precio/alquiler |
| prov_q | coste_uso_aprox | derivado (Poterba) | nacional_q v1 (tipo_hip, inflacion_deflactor) | — | pp | trimestral | tipo_hip − media móvil 4T de la inflación interanual | derivado | aproximación SIN impuestos, sin depreciación ni prima de riesgo; mismo valor en todas las provincias |
| prov_q | credito_vivienda_nuevo | BdE nuevas operaciones crédito vivienda hogares (DN_1TI2TIE96) | bde_credito_finalidad.csv | be1916 | Millones € | mensual | suma de 3 meses | agregado_suma | nacional (mismo valor en todas las provincias) |
| prov_q | saldo | BdE saldo crédito vivienda hogares (DF_MESNAA22A1U62251Z01E) | bde_credito_finalidad.csv | be1916 | Millones € | mensual | último mes del trimestre | fin_periodo | nacional; unidad 'Millones de euros' según metadatos del fichero |
| prov_q | tipo_hip | v1 nacional_q.csv (ECB/BdE/INE CNT) | data/processed/nacional_q.csv (v1) | — | % / pp | trimestral | según v1 | según v1 (copiado) | nacional; inflacion = inflacion_deflactor (% interanual) |
| prov_q | euribor | v1 nacional_q.csv (ECB/BdE/INE CNT) | data/processed/nacional_q.csv (v1) | — | % / pp | trimestral | según v1 | según v1 (copiado) | nacional; inflacion = inflacion_deflactor (% interanual) |
| prov_q | tipo_hip_real | v1 nacional_q.csv (ECB/BdE/INE CNT) | data/processed/nacional_q.csv (v1) | — | % / pp | trimestral | según v1 | según v1 (copiado) | nacional; inflacion = inflacion_deflactor (% interanual) |
| prov_q | inflacion | v1 nacional_q.csv (ECB/BdE/INE CNT) | data/processed/nacional_q.csv (v1) | — | % / pp | trimestral | según v1 | según v1 (copiado) | nacional; inflacion = inflacion_deflactor (% interanual) |
| prov_q | ln_* / d_ln_* / d4_ln_* | derivado | — | — | log natural | trimestral | ln de niveles > 0; d_ = Δ1 trimestre; d4_ = Δ4 (interanual) | derivado | NaN si nivel ≤ 0 o falta |
| prov_a | serpavi_mediana_vc/vu | MIVAU-SERPAVI (AEAT IRPF) mediana alquiler €/m²/mes, provincia | pdf/serpavi_v2_municipios.csv.gz (nivel PROV) | — | €/m²/mes | anual | observado | observado | 2011-2024 |
| prov_a | serpavi_n_inmuebles_vc/vu | MIVAU-SERPAVI nº de inmuebles (contratos) en alquiler, provincia | pdf/serpavi_v2_municipios.csv.gz (nivel PROV) | — | inmuebles | anual | observado | observado | 2011-2024 |
| prov_a | ipva_indice / ipva_var | INE IPVA índice de precios de vivienda en alquiler, total (59058) | ine_v2_ipva.csv | 59058 | índice / % var. anual | anual | observado | observado | 48 provincias; sin País Vasco ni Navarra |
| prov_a | pib_prov | INE CRE PIB a precios de mercado, precios corrientes, provincia (80109) | ine_v2_cre.csv | 80109 | miles de € (NO VERIFICADO: inferido de FK_Unidad) | anual | observado | observado | 2000-2025 |
| prov_a | pib_pc | derivado: pib_prov × 1000 / pob_total (1 enero del mismo año) | ine_v2_cre.csv + ine_v2_padron_prov_edad_nac.csv | 80109 / 77023 | € por habitante | anual | cociente | derivado | NO existe renta disponible provincial en v2; PIB per cápita es el proxy de renta |
| prov_a | pob_<nac>_<edad> | INE ECP población 1 enero por nacionalidad y edad (77023) | ine_v2_padron_prov_edad_nac.csv | 77023 | personas | anual (1 enero) | observado | observado | nombres: pob_{total,espanola,extranjera}_{todas,0_19,20_34,35_64,65_mas} |
| prov_a | pob_nac_<grupo> | INE ECP población por agrupación de países de nacionalidad (77023) | ine_v2_padron_prov_pais.csv | 77023 | personas | anual (1 enero) | observado | observado | grupos según fichero; algunos con cobertura parcial |
| prov_a | precio_alquiler_ratio_nivel | derivado | — | — | años de alquiler (ratio) | anual | cociente | derivado | p_tasado / (12 × serpavi_mediana_vc); años con ambos datos |
| prov_a | esfuerzo_aprox | derivado | — | — | años de PIB per cápita (proxy) | anual | cociente | derivado | vivienda de 90 m² (supuesto); renta disponible provincial NO existe en v2 |
| prov_a | agregados anuales de trimestrales | derivado | panel_prov_q | — | según variable | anual | media (p_tasado, p_suelo, ipc, EPA, zona) o suma (ETDP, hipotecas, MIVAU); NaN si falta un trimestre | agregado_media / agregado_suma | stock (pob_*): valor 1 enero (T1); vut: agosto (T3); inmig: suma S1+S2 |
| muni_a | serpavi_mediana_vc | SERPAVI municipal (AEAT IRPF) | varios (ver docs) | — | €/m²/mes | anual | según fuente | observado |  |
| muni_a | serpavi_mediana_vu | SERPAVI municipal (AEAT IRPF) | varios (ver docs) | — | €/m²/mes | anual | según fuente | observado |  |
| muni_a | serpavi_n_vc | SERPAVI municipal | varios (ver docs) | — | inmuebles | anual | según fuente | observado |  |
| muni_a | serpavi_n_vu | SERPAVI municipal | varios (ver docs) | — | inmuebles | anual | según fuente | observado |  |
| muni_a | p_tasado | MIVAU valor tasado municipios >25.000 hab. (media de trimestres disponibles) | varios (ver docs) | — | €/m² | anual | según fuente | agregado_media |  |
| muni_a | trans_total | MIVAU transacciones municipales (solo años con 4 trimestres) | varios (ver docs) | — | transacciones | anual | según fuente | agregado_suma |  |
| muni_a | vut_viviendas | INE VTE municipal (mes más cercano a agosto, máx. 3 meses) | varios (ver docs) | — | número | anual | según fuente | observado |  |
| muni_a | uu_residenciales | Catastro (periodo N = stock 31-dic de N-1) | varios (ver docs) | — | unidades urbanas residenciales | anual | según fuente | observado |  |
| muni_a | ipva_indice | INE IPVA municipal (59060) | varios (ver docs) | — | índice | anual | según fuente | observado |  |
| muni_a | ipva_var | INE IPVA municipal (59060) | varios (ver docs) | — | % var. anual | anual | según fuente | observado |  |
| muni_a | zona_tensionada | BOE zonas tensionadas; munis fuera del fichero = 0 desde 2024 | varios (ver docs) | — | fracción de días del año | anual | según fuente | derivado |  |
| muni_a | municipio / cod_muni | INE diccionario municipios 2026 (ine_diccionario_municipios_2026.xlsx) | ine_diccionario_municipios_2026.xlsx | — | código | — | casado por nombre si no hay código | observado | casados por nombre: 8448 únicos + 7 con provincia; no casados: 17; ambiguos: 53 |
| ue_a/q | hpi | Eurostat prc_hpi (índice precios vivienda compra, total) | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | prc_hpi_q / prc_hpi_a | I15 (2015=100) | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | hpi_bis | BIS WS_SPP precios residenciales nominal | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | WS_SPP | índice 2010=100 | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | hpi_oecd | OCDE HPI | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | DF_HOUSE_PRICES | índice / ratio | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | ocde_precio_ingreso | OCDE HPI_YDH | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | DF_HOUSE_PRICES | índice / ratio | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | ocde_precio_alquiler | OCDE HPI_RPI | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | DF_HOUSE_PRICES | índice / ratio | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | ocde_alquiler_idx | OCDE RPI | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | DF_HOUSE_PRICES | índice / ratio | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | alquiler_hicp | Eurostat HICP CP041 alquiler | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | prc_hicp_midx/aind | índice | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | permisos | Eurostat permisos de construcción de viviendas | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | sts_cobp_a / q | THS viviendas (A); índice 2021=100 (Q) | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | inmig_por_1000 | Eurostat migr_imm1ctz / demo_pjan × 1000 | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | migr_imm1ctz, demo_pjan | por 1.000 hab. | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | poblacion | Eurostat demo_pjan población 1 enero, total | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | demo_pjan | personas | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | tipo_hip_mir | BCE MIR tipo hipotecario compra vivienda (solo zona euro) | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | MIR.M.<geo>.B.A2C.AM.R.A.2250.EUR.N | % anual | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | tipo_largo | Eurostat/BCE tipo de interés largo plazo (irt_lt_mcby_a) | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | irt_lt_mcby_a | % anual | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | renta_bruta_disp | Eurostat nasa_10_nf_tr, código B6G (renta disponible bruta hogares, S14_S15) | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | nasa_10_nf_tr | millones € corrientes | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | empleo | Eurostat lfsi_emp_a empleo 15-64 | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | lfsi_emp_a | miles de personas | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| ue_a/q | hicp_general | Eurostat HICP general CP00 (índice medio anual) | eu_*.csv / bis_rpp.csv / oecd_house_prices.csv | prc_hicp_aind | índice | anual / trimestral | según fuente | observado / agregado_media / anual_asignado | UE geo ISO2 Eurostat (EL, UK) |
| eventos | dummy_vigente | BOE (eventos verificados, estado VERIFICADO) | v2_eventos_politica.csv | — | 0/1 | trimestral | vigencia en algún día del trimestre | derivado | 35 eventos verificados de 41; no verificados excluidos |
| nacional_v2 | copia v1 nacional_q | v1 (ver docs/diccionario_variables.md) | data/processed/nacional_q.csv | — | según v1 | trimestral | según v1 | según v1 | todas las columnas de v1 copiadas tal cual |
| nacional_v2 | compraventas_nac / hipotecas_n_nac / hipotecas_importe_nac | INE ETDP (6150) / INE HPT (76317) nacional | ine_v2_etdp_prov.csv / ine_v2_hipotecas_prov.csv | 6150 / 76317 | número / miles € (NO VERIFICADO) | mensual -> trimestral | suma de 3 meses | agregado_suma | serie nacional (no suma de provincias) |
| nacional_v2 | credito_*_bde / saldo_*_bde | BdE be1916/be1906 | bde_credito_finalidad.csv | be1916 | Millones € | mensual | flujo: suma; saldo: fin de trimestre | agregado_suma / fin_periodo |  |
| nacional_v2 | eventos ev_<ID> | derivado de eventos_q | v2_eventos_politica.csv | — | 0/1 | trimestral | vigencia | derivado | solo eventos VERIFICADOS de ámbito nacional |

## Cobertura y huecos por panel

### panel_prov_q

Filas: 5096; unidades (cod_prov): 52; claves duplicadas: 0

| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |
|---|---|---|---|---|---|
| p_tasado | 2002Q1 | 2026Q2 | 52 | 0 | 33 |
| p_suelo | 2004Q1 | 2026Q2 | 50 | 0 | 614 |
| ipc_alquiler | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| compraventas_total | 2007Q1 | 2026Q2 | 52 | 0 | 1040 |
| compraventas_nueva | 2007Q1 | 2026Q2 | 52 | 0 | 1040 |
| compraventas_usada | 2007Q1 | 2026Q2 | 52 | 0 | 1040 |
| compraventas_libre | 2007Q1 | 2026Q2 | 52 | 0 | 1040 |
| compraventas_protegida | 2007Q1 | 2026Q2 | 52 | 0 | 1040 |
| hipotecas_n | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| hipotecas_importe | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| ocupados | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| parados | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| iniciadas_libres | 2008Q1 | 2026Q2 | 50 | 0 | 1497 |
| terminadas_libres | 2008Q1 | 2026Q2 | 50 | 0 | 1396 |
| protegida | 2008Q1 | 2026Q2 | 50 | 0 | 1396 |
| vut_viviendas | 2020Q3 | 2026Q2 | 52 | 0 | 4420 |
| pob_total | 2002Q1 | 2026Q1 | 52 | 3744 | 52 |
| pob_extranj | 2002Q1 | 2026Q1 | 52 | 3744 | 52 |
| pob_20_34 | 2002Q1 | 2026Q1 | 52 | 3744 | 52 |
| inmig_flujo | 2008Q2 | 2022Q2 | 52 | 0 | 3588 |
| zona_tensionada_share | 2024Q1 | 2026Q2 | 48 | 0 | 4616 |
| zona_tensionada_any | 2024Q1 | 2026Q2 | 52 | 0 | 4576 |
| tipo_hip | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| euribor | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| tipo_hip_real | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| inflacion | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| coste_uso_aprox | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| credito_vivienda_nuevo | 2003Q1 | 2026Q2 | 52 | 0 | 208 |
| saldo | 2002Q1 | 2026Q2 | 52 | 0 | 0 |
| ratio_precio_alquiler_idx | 2002Q1 | 2026Q2 | 52 | 0 | 33 |

### panel_prov_a

Filas: 1248; unidades (cod_prov): 52; claves duplicadas: 0

| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |
|---|---|---|---|---|---|
| p_tasado | 2002 | 2025 | 52 | 0 | 14 |
| p_suelo | 2004 | 2025 | 50 | 0 | 164 |
| ipc_alquiler | 2002 | 2025 | 52 | 0 | 0 |
| ocupados | 2002 | 2025 | 52 | 0 | 0 |
| parados | 2002 | 2025 | 52 | 0 | 0 |
| zona_tensionada_share | 2024 | 2025 | 48 | 0 | 1152 |
| compraventas_total | 2007 | 2025 | 52 | 0 | 260 |
| compraventas_nueva | 2007 | 2025 | 52 | 0 | 260 |
| compraventas_usada | 2007 | 2025 | 52 | 0 | 260 |
| compraventas_libre | 2007 | 2025 | 52 | 0 | 260 |
| compraventas_protegida | 2007 | 2025 | 52 | 0 | 260 |
| hipotecas_n | 2003 | 2025 | 52 | 0 | 52 |
| hipotecas_importe | 2003 | 2025 | 52 | 0 | 52 |
| iniciadas_libres | 2008 | 2025 | 50 | 0 | 448 |
| terminadas_libres | 2008 | 2025 | 50 | 0 | 348 |
| protegida | 2008 | 2025 | 50 | 0 | 348 |
| pob_total | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranj | 2002 | 2025 | 52 | 0 | 0 |
| pob_20_34 | 2002 | 2025 | 52 | 0 | 0 |
| vut_viviendas | 2020 | 2024 | 52 | 0 | 988 |
| inmig_flujo | 2008 | 2021 | 52 | 0 | 520 |
| serpavi_mediana_vc | 2011 | 2024 | 52 | 0 | 567 |
| serpavi_n_inmuebles_vc | 2011 | 2024 | 52 | 0 | 567 |
| serpavi_mediana_vu | 2011 | 2024 | 52 | 0 | 567 |
| serpavi_n_inmuebles_vu | 2011 | 2024 | 52 | 0 | 567 |
| ipva_indice | 2011 | 2024 | 48 | 0 | 576 |
| ipva_var | 2012 | 2024 | 48 | 0 | 624 |
| pib_prov | 2002 | 2025 | 52 | 0 | 43 |
| pib_pc | 2002 | 2025 | 52 | 0 | 43 |
| pob_espanola_0_19 | 2002 | 2025 | 52 | 0 | 0 |
| pob_espanola_20_34 | 2002 | 2025 | 52 | 0 | 0 |
| pob_espanola_35_64 | 2002 | 2025 | 52 | 0 | 0 |
| pob_espanola_65_mas | 2002 | 2025 | 52 | 0 | 0 |
| pob_espanola_todas | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranjera_0_19 | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranjera_20_34 | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranjera_35_64 | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranjera_65_mas | 2002 | 2025 | 52 | 0 | 0 |
| pob_extranjera_todas | 2002 | 2025 | 52 | 0 | 0 |
| pob_total_0_19 | 2002 | 2025 | 52 | 0 | 0 |
| pob_total_20_34 | 2002 | 2025 | 52 | 0 | 0 |
| pob_total_35_64 | 2002 | 2025 | 52 | 0 | 0 |
| pob_total_65_mas | 2002 | 2025 | 52 | 0 | 0 |
| pob_total_todas | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_apatridas | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_africa | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_america_del_norte | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_asia | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_centro_america_y_caribe | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_oceania | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_de_sudamerica | 2002 | 2025 | 52 | 0 | 0 |
| pob_nac_pais_de_europa_menos_ue27_2020 | 2021 | 2025 | 52 | 0 | 988 |
| pob_nac_pais_de_europa_menos_ue28 | 2002 | 2020 | 52 | 0 | 260 |
| pob_nac_pais_de_la_ue27_2020_sin_espana | 2021 | 2025 | 52 | 0 | 988 |
| pob_nac_pais_de_la_ue28_sin_espana | 2002 | 2020 | 52 | 0 | 260 |
| precio_alquiler_ratio_nivel | 2011 | 2024 | 52 | 0 | 577 |
| esfuerzo_aprox | 2002 | 2025 | 52 | 0 | 57 |

### panel_muni_a

Filas: 83496; unidades (cod_muni): 3479; claves duplicadas: 0

| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |
|---|---|---|---|---|---|
| serpavi_mediana_vc | 2011 | 2024 | 2616 | 0 | 54780 |
| serpavi_mediana_vu | 2011 | 2024 | 3184 | 0 | 50444 |
| serpavi_n_vc | 2011 | 2024 | 3479 | 0 | 37781 |
| serpavi_n_vu | 2011 | 2024 | 3477 | 0 | 37791 |
| p_tasado | 2005 | 2025 | 299 | 0 | 77554 |
| trans_total | 2004 | 2025 | 301 | 0 | 76874 |
| vut_viviendas | 2020 | 2025 | 3445 | 0 | 62850 |
| uu_residenciales | 2012 | 2025 | 3224 | 0 | 38379 |
| ipva_indice | 2011 | 2024 | 703 | 0 | 73850 |
| ipva_var | 2012 | 2024 | 703 | 0 | 74538 |
| zona_tensionada | 2024 | 2025 | 3479 | 0 | 76538 |

### panel_ue_a

Filas: 744; unidades (geo): 31; claves duplicadas: 0

| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |
|---|---|---|---|---|---|
| hpi | 2005 | 2025 | 29 | 0 | 179 |
| hpi_bis | 2002 | 2025 | 31 | 0 | 45 |
| hpi_oecd | 2002 | 2025 | 26 | 0 | 158 |
| ocde_precio_ingreso | 2002 | 2025 | 26 | 0 | 164 |
| ocde_precio_alquiler | 2002 | 2025 | 26 | 0 | 158 |
| ocde_alquiler_idx | 2002 | 2025 | 26 | 0 | 120 |
| alquiler_hicp | 2002 | 2025 | 31 | 0 | 9 |
| permisos | 2005 | 2025 | 29 | 0 | 141 |
| inmig_por_1000 | 2002 | 2024 | 31 | 0 | 63 |
| poblacion | 2002 | 2025 | 31 | 0 | 5 |
| tipo_hip_mir | 2003 | 2025 | 19 | 0 | 367 |
| tipo_largo | 2002 | 2025 | 28 | 0 | 98 |
| renta_bruta_disp | 2002 | 2025 | 30 | 0 | 48 |
| empleo | 2003 | 2025 | 30 | 0 | 225 |
| hicp_general | 2002 | 2025 | 31 | 0 | 9 |

### panel_ue_q

Filas: 3038; unidades (geo): 31; claves duplicadas: 0

| variable | primer dato | último dato | nº unidades con dato | nº interpolaciones | nº NaN |
|---|---|---|---|---|---|
| hpi | 2005Q1 | 2026Q2 | 29 | 0 | 717 |
| hpi_bis | 2002Q1 | 2026Q2 | 31 | 0 | 198 |
| hpi_oecd | 2002Q1 | 2026Q2 | 26 | 0 | 644 |
| ocde_precio_ingreso | 2002Q1 | 2026Q2 | 26 | 0 | 670 |
| ocde_precio_alquiler | 2002Q1 | 2026Q2 | 26 | 0 | 656 |
| ocde_alquiler_idx | 2002Q1 | 2026Q2 | 26 | 0 | 502 |
| alquiler_hicp | 2002Q1 | 2025Q4 | 31 | 0 | 95 |
| permisos | 2002Q1 | 2026Q2 | 28 | 0 | 299 |
| inmig_por_1000 | 2002Q1 | 2024Q4 | 31 | 0 | 314 |
| poblacion | 2002Q1 | 2025Q4 | 31 | 0 | 82 |
| tipo_hip_mir | 2003Q1 | 2026Q2 | 20 | 0 | 1490 |
| tipo_largo | 2002Q1 | 2025Q4 | 28 | 0 | 454 |
| renta_bruta_disp | 2002Q1 | 2025Q4 | 30 | 0 | 254 |
| empleo | 2003Q1 | 2025Q4 | 30 | 0 | 962 |
| hicp_general | 2002Q1 | 2025Q4 | 31 | 0 | 98 |

## Notas de limitación

- Renta disponible provincial NO existe en los datos v2: el proxy de esfuerzo usa PIB per cápita.
- IPVA provincial sin País Vasco ni Navarra (no publicado por la fuente).
- Unidades de hipotecas_importe y pib_prov inferidas de FK_Unidad/magnitud: no verificadas contra metadatos.
- zona_tensionada: NaN antes de 2024; municipios fuera del fichero BOE = 0 desde 2024 (supuesto).
- Casamiento de municipios por nombre (VUT INE, IPVA municipal, valor tasado y transacciones MIVAU) con ine_diccionario_municipios_2026.xlsx: 8448 casados por nombre único, 7 con ayuda de provincia, 15 nombres sin casar, 53 ambiguos (no casados), 46 nombres «Resto de provincia» excluidos (agregados, no municipios).
- Nombres sin casar (muestra): ['Calonge', "Castell-Platja d'Aro", 'Cerdedo', 'Cesuras', 'Cotobade', 'Mahón', 'Maó-Mahón', 'Oza dos Ríos', 'Palma de Mallorca', 'San Cristóbal Laguna', 'Sant Carles de la Ràpita', 'Santa Coloma Gramanet', 'Santa Cruz deTenerife', 'Santa Eulalia del Río', 'Vitoria']
- Ambiguos (muestra): ['Cieza (nan): 2 candidatos', 'Mieres (nan): 2 candidatos', 'Serrada (): 2 candidatos', 'Carpio (): 2 candidatos', 'Campillo, El (): 2 candidatos', 'Torrent (): 2 candidatos', 'Piles (): 2 candidatos', 'Oliva (): 2 candidatos', 'Marines (): 2 candidatos', 'Molinos (): 2 candidatos', 'Fonfría (): 2 candidatos', 'Molar, El (): 2 candidatos', 'Tejado (): 2 candidatos', 'Rebollar (): 2 candidatos', 'Herrera (): 2 candidatos', 'Sotillo (): 2 candidatos', 'Villaescusa (): 2 candidatos', 'Pesquera (): 2 candidatos', 'Frontera (): 2 candidatos', 'Sancti-Spíritus (): 2 candidatos']
- coste_uso_aprox: aproximación sin impuestos, depreciación ni prima de riesgo (método derivado).
- ratio_precio_alquiler_idx es una diferencia de logaritmos (índice), no un nivel.
