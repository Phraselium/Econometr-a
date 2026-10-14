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

- filas: 5267501
- filas_publica: 5211508
- variables: 187
- territorios: 55664
- discrepancias_entre_paneles: 203
- filas_posterior_prereg: 35734
- filas por nivel: ccaa 48471, distrito 11544, municipio 1001005, nacional 7648, nuts3 1440, pais 34354, provincia 70239, seccion 4092800

Las discrepancias entre paneles son claves presentes en varios ficheros procesados con valores distintos; se conserva el panel más reciente (v8 > v7 > v1), que es el que usan las publicaciones vigentes.

## Variables

| variable | definición | unidad | capa | fuente | redistribuible | niveles | periodo |
|---|---|---|---|---|---|---|---|
| `bce_hip_tipo_nuevas` | BCE, MIR (nuevas operaciones de vivienda) | % anual | C1 | BCE, MIR (nuevas operaciones de vivienda) | sí | pais | 2003-01–2026-08 |
| `bce_hip_volumen_nuevas` | BCE, MIR | millones de euros | C1 | BCE, MIR | sí | pais | 2003-01–2026-08 |
| `bls_criterios_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, criterios de concesión (oferta), índice de difusión | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ST.S.DINX) | sí | nacional | 2003T1–2026T2 |
| `bls_criterios_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, criterios de concesión (oferta), porcentaje neto (endurecimiento menos relajación) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ST.S.FNET) | sí | nacional | 2003T1–2026T2 |
| `bls_demanda_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, demanda de préstamos, índice de difusión | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ZZ.D.DINX) | sí | nacional | 2003T1–2026T2 |
| `bls_demanda_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, demanda de préstamos, porcentaje neto | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.ZZ.D.FNET) | sí | nacional | 2003T1–2026T2 |
| `bls_rechazo_dif` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, solicitudes rechazadas, índice de difusión (desde 2015T2) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.RA.D.DINX) | sí | nacional | 2015T2–2026T2 |
| `bls_rechazo_neto` | Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, solicitudes rechazadas, porcentaje neto (desde 2015T2) | puntos | C4 | v8/ecb_bls_es_vivienda.csv (Q.ES.ALL.Z.H.H.B3.RA.D.FNET) | sí | nacional | 2015T2–2026T2 |
| `compraventas` | Compraventas de viviendas ETDP, total (anual = suma) | número | C4 | INE ETDP 6150, desglose total | sí | ccaa,nacional,provincia | 2007–2026T2 |
| `compraventas_ine` | Compraventas de vivienda, total nacional (ETDP, INE), suma trimestral | número | C4 | ine_etdp_compraventas.csv (ETDP1826) | sí | nacional | 2007T1–2026T2 |
| `compraventas_sa` |  | número (SA) | C4 | Derivada (STL) | sí | nacional | 2007T1–2026T2 |
| `costes` |  | índice 2021=100 | C4 | ver diccionario del panel de origen | sí | nacional | 1995T1–2026T2 |
| `costes_constr` | Índice de costes de construcción de edificios residenciales, España (Eurostat sts_copi_q, 2021=100, sin ajustar) | índice 2021=100 | C4 | eurostat_costes.csv | sí | nacional | 1995T1–2026T2 |
| `credito_construccion` | Saldo de crédito de entidades de crédito a construcción (promotores y constructoras), fin de trimestre | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv (D_MEE61010) | sí | nacional | 1995T1–2026T2 |
| `credito_inmobiliario` | Saldo de crédito de entidades de crédito a actividades inmobiliarias (promotores y constructoras), fin de trimestre | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv (D_MEE61013) | sí | nacional | 1995T1–2026T2 |
| `credito_nuevo` | Nuevo crédito a la vivienda (volumen de nuevas operaciones), España, suma trimestral | millones de euros | C4 | ecb_nuevo_credito_vivienda_es.csv | sí | nacional | 2003T1–2026T2 |
| `credito_promotor` | Crédito a construcción + actividades inmobiliarias (proxy de crédito a promotores) | millones de euros | C4 | v5/ca_bde_be0418_credito_actividad.csv | sí | nacional | 1995T1–2026T2 |
| `credito_stock` |  | M€ (stock) | C4 | BCE BSI, stock crédito vivienda | sí | nacional | 2003T1–2026T2 |
| `credito_stock_bde` | Saldo de crédito a la vivienda de hogares, entidades de crédito (BdE be1916), fin de trimestre (primer dato 1997T3) | millones de euros | C1 | bde_credito_finalidad.csv (DF_MESNAA22A1U62251Z01E) | sí | nacional | 1997T3–2026T2 |
| `credito_stock_ecb` | Saldo vivo de crédito a la vivienda, IFM España (BCE BSI), fin de trimestre | millones de euros | C1 | ecb_stock_credito_vivienda_es.csv | sí | nacional | 2003T1–2026T2 |
| `deflactor` |  | índice 2020=100 | C4 | Derivada: INE CNT (SA) | sí | nacional | 1995T1–2026T2 |
| `dif_hip_euribor_bce` | Diferencial tipo hipotecario BCE - Euríbor 1 año | puntos porcentuales | C4 | derivada | sí | nacional | 2003T1–2026T2 |
| `dif_hip_euribor_bde` | Diferencial tipo hipotecario BdE - Euríbor 1 año | puntos porcentuales | C4 | derivada | sí | nacional | 1995T1–2026T2 |
| `emal_n_fianzas` | Gobierno Vasco, EMAL (fianzas) | contratos | C4 | Gobierno Vasco, EMAL (fianzas) | sí | municipio | 2016T1–2025T4 |
| `emal_renta_eur_m2_construido` | Gobierno Vasco, EMAL | €/m²/mes | C4 | Gobierno Vasco, EMAL | sí | municipio | 2016T1–2025T4 |
| `emal_renta_mensual_eur` | Gobierno Vasco, EMAL | €/mes | C4 | Gobierno Vasco, EMAL | sí | municipio | 2016T1–2025T4 |
| `epa_pob_total` |  | miles (todas las edades) | C4 | INE EPA, tabla 65285 | sí | ccaa | 2007T1–2026T2 |
| `euribor` |  | % anual | C4 | BCE, Euribor 1 año | sí | nacional | 1995T1–2026T3 |
| `euribor_1y` | Euríbor a 1 año, media trimestral | % anual | C4 | ecb_euribor1y.csv | sí | nacional | 1995T1–2026T2 |
| `euribor_3m` | Euríbor a 3 meses, media trimestral | % anual | C4 | v8/ecb_tipos_euribor3m_depo.csv | sí | nacional | 1995T1–2026T2 |
| `eurostat_plataformas_noches` | Eurostat, tour_ce_oan3 (plataformas colaborativas) | noches | C1 | Eurostat, tour_ce_oan3 (plataformas colaborativas) | sí | nuts3 | 2018–2025 |
| `fianzas_importe_media` | Importe medio de la fianza | euros | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `fianzas_importe_mediana` | Importe mediano de la fianza (proxy de una mensualidad de alquiler) | euros | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `fianzas_n` | Fianzas de arrendamiento depositadas en la GVA (número de contratos), por provincia y año | número | C4 | v5/gva_fianzas_AAAA.csv | sí | municipio,provincia | 2020–2026 |
| `hip_importe` | Importe de hipotecas sobre viviendas | miles de euros | C4 | INE Hipotecas, hipotecas_viviendas_importe | sí | ccaa,provincia | 2003–2026T2 |
| `hip_n` | Hipotecas constituidas sobre viviendas, número | número | C4 | INE Hipotecas, serie HPT por provincia, hipotecas_viviendas_numero | sí | ccaa,provincia | 2003–2026T2 |
| `hogares_ecp` | Hogares en viviendas familiares (ECP, proyección/estimación INE), total nacional | miles de hogares | C1 | ine_hogares_60131.csv (ECP355533) | sí | nacional | 2021T1–2026T2 |
| `hogares_epa` | Hogares (EPA), total nacional | miles de hogares | C1 | ine_epa_hogares.csv (EPA430446) | sí | nacional | 2002T1–2026T2 |
| `hpi_es_eurostat` | Índice de precios de la vivienda Eurostat (total, 2015=100), ES | índice 2015=100 | C1 | v8/eurostat_prc_hpi_q_multi.csv | sí | nacional | 2005T4–2026T2 |
| `hpi_eurostat` |  | índice 2015=100 | C4 | ver diccionario del panel de origen | sí | nacional | 2005T4–2026T2 |
| `iab_disponibilidad_365_media` |  | días | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_anuncios` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_con_licencia` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_entire_home` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_hotel_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_private_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_n_shared_room` |  | anuncios | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `iab_resenas_ultimos_12m` |  | reseñas | C4 | Inside Airbnb (no oficial) | sí | seccion | 2026-09–2026-09 |
| `incasol_contratos` | Incasòl, fianzas (Socrata qww9-bvhh) | contratos | C1 | Incasòl, fianzas (Socrata qww9-bvhh) | no | municipio | 2007–2026T1 |
| `incasol_renta_media` | Incasòl, fianzas | €/mes | C1 | Incasòl, fianzas | no | municipio | 2007–2026T1 |
| `inflacion_deflactor` |  | % interanual | C4 | Derivada | sí | nacional | 1996T1–2026T2 |
| `inflacion_ipc_yoy` | Inflación interanual = 100 x (ln IPC_t - ln IPC_t-4) | % (puntos log) | C4 | derivada de ipc_general | sí | nacional | 1996T1–2026T2 |
| `iniciadas` |  | viviendas | C4 | ver diccionario del panel de origen | sí | provincia | 2008–2026T2 |
| `iniciadas_anual_tabla` |  | viviendas | C4 | ver diccionario del panel de origen | sí | provincia | 2002–2024 |
| `inmig_anual` | Inmigración anual desde el extranjero, total (Eurostat migr_imm1ctz), valor anual asignado a cada trimestre del año | personas/año | C4 | eurostat_inmigracion_anual.csv (A/TOTAL/REACH/TOTAL/NR/T/ES) | sí | nacional | 1998T1–2024T4 |
| `inmig_anual_eurostat` |  | personas (flujo anual) | C4 | Eurostat migr_imm1ctz (inmigración anual, ciudadanía TOTAL) | sí | nacional | 1998–2024T4 |
| `ipc_alquiler` | IPC, alquiler de vivienda, nacional (índice; media trimestral de los 3 índices mensuales) | índice (base INE) | C4 | ine_ipc_alquiler.csv (IPC290887) | sí | ccaa,nacional | 2002T1–2026T2 |
| `ipc_alquiler_indice` |  | índice 2021=100 | C4 | ver diccionario del panel de origen | sí | provincia | 2002–2026T2 |
| `ipc_alquiler_yoy` |  | % interanual | C4 | INE IPC, subclase alquiler de vivienda | sí | nacional,provincia | 2002–2026T2 |
| `ipv` | Índice de precios de vivienda INE, general, nacional (base 2015=100) | índice | C1 | ine_ipv_80270.csv (IPV1209) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipv15` |  | índice | C4 | INE IPV, tabla 25171 (base 2015, robustez) | sí | nacional | 2007T1–2025T4 |
| `ipv_nueva` | IPV INE, vivienda nueva, nacional | índice | C4 | ine_ipv_80270.csv (IPV1613) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipv_usada` | IPV INE, vivienda segunda mano, nacional | índice | C4 | ine_ipv_80270.csv (IPV1618) | sí | ccaa,nacional | 2007T1–2026T2 |
| `ipva` |  | índice | C4 | ver diccionario del panel de origen | sí | municipio | 2011–2024 |
| `ipva_indice` | Índice de precios de vivienda en alquiler (IPVA, base SERPAVI), total; 48 provincias, desde 2011; stock | índice 2015=100 | C1 | INE, Índice de Precios de Vivienda en Alquiler (59004, 59005, 59061) | sí | ccaa,distrito,nacional,provincia | 2011–2024 |
| `ipva_var_anual` | INE, IPVA | % | C1 | INE, IPVA | sí | ccaa,distrito,nacional,provincia | 2012–2024 |
| `notariado_cgn_extranj` |  | operaciones | C4 | Consejo General del Notariado (CIEN) | no | ccaa,nacional | 2007–2025T4 |
| `notariado_cuantia_esp_prov` |  | € | C4 | ver diccionario del panel de origen | no | provincia | 2018T1–2025T4 |
| `notariado_cuantia_ext_prov` |  | € | C4 | ver diccionario del panel de origen | no | provincia | 2018T1–2025T4 |
| `notariado_cuantia_media_esp` | Notariado CV, cuantia_media_esp (provincia) | euros | C4 | pdf/notariado_cv_prov_trimestral.csv | no | provincia | 2018T1–2025T4 |
| `notariado_cuantia_media_ext` | Notariado CV, cuantia_media_ext (provincia) | euros | C4 | pdf/notariado_cv_prov_trimestral.csv | no | provincia | 2018T1–2025T4 |
| `notariado_op_sem` | Operaciones de compraventa de vivienda libre ante notario, total, semestral (T2, T4) | número | C4 | pdf/notariado_cgn_extranjeros_semestral.csv (op_viv_libre) | no | nacional | 2007T2–2025T4 |
| `notariado_pm2_sem` | Precio medio m2 de las compraventas de vivienda libre ante notario, total, dato semestral asignado al último trimestre del semestre (T2, T4) | euros/m2 | C4 | pdf/notariado_cgn_extranjeros_semestral.csv (precio_m2, Total general) | no | nacional | 2007T2–2025T4 |
| `notariado_viv_esp_prov` |  | viviendas | C4 | ver diccionario del panel de origen | no | provincia | 2018T1–2025T4 |
| `notariado_viv_ext_prov` |  | viviendas | C4 | ver diccionario del panel de origen | no | provincia | 2018T1–2025T4 |
| `notariado_viv_extranj` |  | viviendas | C4 | ver diccionario del panel de origen | no | municipio | 2021–2025 |
| `notariado_viv_vendidas_esp` | Notariado CV, viv_vendidas_esp (provincia) | viviendas | C4 | pdf/notariado_cv_prov_trimestral.csv | no | provincia | 2018T1–2025T4 |
| `notariado_viv_vendidas_ext` | Notariado CV, viv_vendidas_ext (provincia) | viviendas | C4 | pdf/notariado_cv_prov_trimestral.csv | no | provincia | 2018T1–2025T4 |
| `ocupados` | Ocupados EPA, total nacional (media del trimestre) | miles de personas | C4 | ine_epa_ocupados.csv (EPA387796) | sí | ccaa,nacional | 2002T1–2026T2 |
| `ocupados_epa` |  | miles de personas | C4 | ver diccionario del panel de origen | sí | provincia | 2002–2026T2 |
| `ocupados_epa_prov` | Ocupados EPA, suma de provincias (contraste con ocupados CCAA) | miles de personas | C1 | INE EPA 65345 EPA_ocupados | sí | ccaa | 2007T1–2026T2 |
| `ocupados_sa` |  | miles (SA) | C4 | Derivada (STL) | sí | nacional | 2002T1–2026T2 |
| `p_bde` | Precio medio m2 viviendas libres tasadas, total nacional (BdE; trimestre = mes de cierre) | euros/m2 | C1 | bde_precio_vivienda_libre.csv (DHIVTNOAPLPMMUVT_RLI.T) | sí | nacional | 1995T1–2026T2 |
| `p_bde_nueva` | Precio medio m2 tasado, viviendas hasta 5 años (BdE) | euros/m2 | C4 | bde_precio_vivienda_libre.csv (VVN) | sí | nacional | 2013T1–2026T2 |
| `p_bde_usada` | Precio medio m2 tasado, viviendas de más de 5 años (BdE) | euros/m2 | C4 | bde_precio_vivienda_libre.csv (VVU) | sí | nacional | 2013T1–2026T2 |
| `p_tasado` | Valor tasado medio de la vivienda libre, total nacional (medida principal de precio de compra) | euros/m2 | C1 | mivau_valor_tasado_nacional_ccaa_prov.csv (serie valor_tasado_libre_nacional) | sí | ccaa,municipio,nacional,provincia | 1995T1–2026T2 |
| `parados_epa` | Parados EPA, suma de provincias de la CCAA | miles de personas | C4 | INE EPA tabla 65345, medida EPA_parados | sí | ccaa,provincia | 2002–2026T2 |
| `permisos` |  | viviendas (visados) | C4 | ver diccionario del panel de origen | sí | nacional | 2000T1–2026T2 |
| `pib_ccaa_anual` | PIB a precios corrientes, suma de provincias (CRE 80109); control; el valor anual se repite en los 4 trimestres sin interpolar | miles de euros | C4 | INE CRE 80109 PIB_precios_corrientes | sí | ccaa | 2007T1–2025T4 |
| `pib_ccaa_q` | PIB trimestralizado: ancla en T3, log-lineal entre anclas, sin extrapolar (huecos tras el último ancla); solo robustez | miles de euros | C4 | idem | sí | ccaa | 2007T1–2025T3 |
| `pib_miles_eur` | PIB a precios corrientes (CRE 80109) | miles de euros | C4 | INE CRE 80109 | sí | provincia | 2002–2024 |
| `pib_nom` | PIB a precios de mercado, precios corrientes, ajustado de estacionalidad y calendario (INE) | millones de euros | C4 | ine_cnt_demanda_corrientes.csv (CNTR6597) | sí | nacional | 1995T1–2026T2 |
| `pib_vol_idx` | PIB, índice de volumen encadenado, ajustado de estacionalidad y calendario (INE) | índice | C4 | ine_cnt_demanda_volumen.csv (CNTR6652) | sí | nacional | 1995T1–2026T2 |
| `pob_africa` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_apatridas` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_asia` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_censo_anual` | INE, Censo anual de población (tablas por provincia) | personas | C1 | INE, Censo anual de población (tablas por provincia) | sí | municipio,provincia,seccion | 2021–2025 |
| `pob_centroamerica_caribe` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_espanola` |  | personas (stock 1 ene) | C4 | INE 77019 (ECP) | sí | ccaa,municipio | 1998–2025T1 |
| `pob_europa_no_ue27` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2021–2025 |
| `pob_europa_no_ue28` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2020 |
| `pob_europa_sin_espana` |  | personas (stock 1 ene) | C4 | Derivada de 77019 (ver nota) | sí | ccaa | 2002–2025 |
| `pob_extranj` | Población extranjera = total - nacionales, a 1 de enero (Eurostat migr_pop1ctz), interpolada linealmente a trimestral | personas | C1 | v8/eurostat_migr_pop1ctz_es.csv (códigos TOTAL y NAT) | sí | ccaa,nacional,provincia | 2002–2025T1 |
| `pob_extranj_ccaa_sum` |  | personas (stock) | C4 | Derivada: suma de 17 CCAA de INE 77019 | sí | nacional | 2002T1–2025T1 |
| `pob_extranj_ine` | Población residente de nacionalidad extranjera (ECP/INE) | personas | C1 | ine_ecp_nacional.csv (ECP701) | sí | nacional | 2002T1–2026T2 |
| `pob_extranjera` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_extranjera_gva` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 2005–2022 |
| `pob_norteamerica` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_oceania` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_sudamerica` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2025 |
| `pob_total` | Población residente total (ECP/INE) | personas | C4 | ine_ecp_nacional.csv (ECP320) | sí | ccaa,municipio,nacional,provincia | 1995T1–2026T2 |
| `pob_ue27_sin_espana` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2021–2025 |
| `pob_ue28_sin_espana` |  | personas | C4 | ver diccionario del panel de origen | sí | ccaa | 2002–2020 |
| `pob_vlc_africa` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_vlc_alemania` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_vlc_america` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_vlc_asia` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_vlc_europa` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `pob_vlc_reino_unido` |  | personas | C4 | ver diccionario del panel de origen | sí | municipio | 1998–2022 |
| `prod_constr` |  | índice 2021=100 | C4 | ver diccionario del panel de origen | sí | nacional | 2005T1–2026T2 |
| `rdb` | Renta disponible bruta del total de la economía, ajustada de estacionalidad (INE); NO es renta de los hogares | millones de euros | C4 | ine_cnt_renta_disponible.csv (CTNFSI11113) | sí | nacional | 1999T1–2026T2 |
| `registr_num_4tm` | Compraventas de vivienda inscritas, suma móvil de 4 trimestres (Registradores) (provincia) | número | C4 | pdf/registradores_opendata_compraventas.csv | no | nacional,provincia | 2007T1–2026T2 |
| `registr_pm2_4tm` | Precio medio m2 de las compraventas de vivienda inscritas, media móvil de 4 trimestres (Registradores) (provincia) | euros/m2 | C4 | pdf/registradores_opendata_compraventas.csv | no | nacional,provincia | 2007T1–2026T2 |
| `registradores_compraventas_anual` |  | viviendas (año natural) | C4 | Colegio de Registradores, OpenData (compraventas viviendas, nacional) | sí | nacional | 2007T4–2025T4 |
| `registradores_extranj_pct` |  | % | C4 | Colegio de Registradores, Anuario ERI | sí | ccaa,nacional | 2016–2025T4 |
| `renta_hog` |  | millones de euros | C4 | ver diccionario del panel de origen | sí | nacional | 1999T1–2026T2 |
| `renta_hog_real` |  | M€ a precios de 2020 | C4 | Derivada | sí | nacional | 1999T1–2026T2 |
| `salario` | Coste salarial total por trabajador y mes, industria, construcción y servicios (ETCL, INE); 2000T1-2007T4 tabla 6067 y 2008T1+ tabla 79662 | euros/mes | C4 | v8/ine_etcl_6067_nacional.csv (ETCL5741) + v8/ine_etcl_79662_ccaa.csv (Total Nacional) | sí | nacional | 2000T1–2026T2 |
| `salario_ccaa` | Coste salarial total por trabajador y mes, industria, construcción y servicios, por CCAA (ETCL tabla 79662) | euros/mes | C4 | v8/ine_etcl_79662_ccaa.csv | sí | ccaa | 2008T1–2026T2 |
| `serpavi_dist_vc_mediana` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_n_contratos` |  | viviendas (contratos) | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_p25` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vc_p75` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_mediana` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_n_contratos` |  | viviendas (contratos) | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_p25` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_dist_vu_p75` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | distrito | 2011–2024 |
| `serpavi_esp_constante` |  | €/m²/mes (alquiler, VC) | C4 | MIVAU-SERPAVI (XLSX) → agregado propio | sí | nacional | 2011T4–2024T4 |
| `serpavi_vc_alq_m2_mediana` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 mediana | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_alq_m2_p25` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 p25 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_alq_m2_p75` | SERPAVI provincia, VC (vivienda colectiva), alquiler_m2 p75 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vc_dist_agg` |  | €/m²/mes | C4 | ver diccionario del panel de origen | sí | municipio | 2011–2024 |
| `serpavi_vc_mediana` |  | €/m²/mes | C4 | MIVAU-SERPAVI (XLSX) | sí | ccaa,municipio | 2011–2024 |
| `serpavi_vc_n_contratos` | SERPAVI provincia, VC (vivienda colectiva), n_contratos recuento | contratos | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_mediana` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 mediana | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_p25` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 p25 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_alq_m2_p75` | SERPAVI provincia, VU (vivienda unifamiliar), alquiler_m2 p75 | euros/m2/mes | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `serpavi_vu_n_contratos` | SERPAVI provincia, VU (vivienda unifamiliar), n_contratos recuento | contratos | C4 | pdf/serpavi_provincias.csv | sí | provincia | 2011–2024 |
| `tasa_paro_epa` | Tasa de paro nacional EPA = parados/(parados+ocupados)×100 (código INE 00) | % | C4 | ine_v2_epa_prov.csv (EPA_parados, EPA_ocupados) | sí | ccaa,nacional | 2002T1–2026T2 |
| `terminadas` | Viviendas libres terminadas, nacional, flujo trimestral (MIVAU tabla 3.2) | viviendas | C4 | mivau_fin_obra.csv (mensual 2008+) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025) | sí | ccaa,nacional,provincia | 1995T1–2026T2 |
| `terminadas_anual_tabla` |  | viviendas | C4 | ver diccionario del panel de origen | sí | provincia | 2002–2024 |
| `tipo_bce` |  | % anual | C4 | BCE, tipo MRR (operaciones principales) | sí | nacional | 1999T1–2026T2 |
| `tipo_dfr` | Tipo de la facilidad de depósito del BCE, media trimestral ponderada por días | % anual | C4 | v8/ecb_tipos_euribor3m_depo.csv | sí | nacional | 1999T1–2026T2 |
| `tipo_hip` |  | % anual | C4 | BCE MIR, nuevas operaciones vivienda | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_bce` | Tipo de interés (TAE) de nuevas operaciones de crédito para adquisición de vivienda, España (BCE MIR), media trimestral | % anual | C1 | ecb_tipo_hipotecario_es.csv | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_bde` | Tipo medio de adquisición de vivienda libre, más de 3 años, conjunto de entidades (BdE), media trimestral | % anual | C1 | bde_tipo_hipotecario_referencia.csv (D_1T9H0000) | sí | nacional | 1995T1–2026T2 |
| `tipo_hip_nuevas_tae` | TAE de nuevas operaciones de crédito a la vivienda, hogares (BdE), media trimestral | % anual | C1 | bde_tipos_hipotecas_nuevas.csv (DN_1TI2T0082) | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real` |  | pp | C4 | Derivada | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real_bce` | Tipo hipotecario BCE (TAE nuevas operaciones) menos inflación interanual | puntos porcentuales | C4 | derivada de tipo_hip_bce e ipc_general | sí | nacional | 2003T1–2026T2 |
| `tipo_hip_real_bde` | Tipo hipotecario BdE menos inflación interanual del IPC | puntos porcentuales | C4 | derivada de tipo_hip_bde e ipc_general | sí | nacional | 1996T1–2026T2 |
| `tipo_mro` | Tipo de las operaciones principales de financiación (MRO) del BCE, media trimestral ponderada por días | % anual | C4 | ecb_tipo_oficial.csv | sí | nacional | 1999T1–2026T2 |
| `tope_rentas_ccaa` | Tope de rentas autonómico vigente al cierre del trimestre (E09: Ley catalana 11/2020, 2020-09-22 a 2022-04-08, anulación parcial STC 37/2022) | 0/1 | C4 | v2_eventos_politica.csv, E09 (BOE) | sí | ccaa | 2007T1–2026T2 |
| `tope_rentas_ccaa_alt_v3` | Tope vigente con la ventana de la ley según cataluna_contencion_rentas_v3 (hasta 2021-09-21); se reporta junto a E09 porque las ventanas difieren | 0/1 | C4 | v3/cataluna_contencion_rentas_v3.csv | sí | ccaa | 2007T1–2026T2 |
| `tope_rentas_ccaa_frac` | Fracción de días del trimestre con tope vigente (E09) | proporción | C4 | idem | sí | ccaa | 2007T1–2026T2 |
| `trans_extranjeros` |  | transacciones | C4 | MIVAU 340101i0 (de panel_ccaa_q) | sí | ccaa,nacional | 2007T1–2026T2 |
| `trans_total` |  | transacciones | C4 | MIVAU 34010110 (de panel_ccaa_q) | sí | ccaa,municipio,nacional | 2004T1–2026T1 |
| `turistas` | Turistas internacionales llegados a España, total (FRONTUR, dato base mensual), suma trimestral | personas | C4 | v8/ine_frontur_10823_ccaa.csv (FREG286, Total Nacional); el fichero ine_frontur_10822_pais.csv solo trae desglose por pa | sí | nacional | 2015T4–2026T2 |
| `turistas_ccaa` | Turistas internacionales por CCAA de destino (FRONTUR, dato base mensual), suma trimestral | personas | C4 | v8/ine_frontur_10823_ccaa.csv | sí | ccaa | 2015T4–2026T2 |
| `tx_extranj` | Transacciones de vivienda adquiridas por extranjeros residentes, total nacional (MIVAU, tabla 1.6.5) | número | C4 | mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_nacional) | sí | nacional | 2007T1–2026T2 |
| `tx_extranj_ccaa` | Transacciones de vivienda adquiridas por extranjeros residentes por CCAA (MIVAU 1.6.5), total | número | C4 | mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_ccaa_*) | sí | ccaa | 2007T1–2026T2 |
| `tx_total` | Transacciones inmobiliarias de vivienda, total nacional (MIVAU) | número | C4 | mivau_transacciones_total.csv | sí | nacional | 2004T1–2026T1 |
| `valor_tasado` | Valor tasado medio vivienda libre provincial (MIVAU) desde 1995T1; coincide con v7 en el solape | euros/m2 | C4 | mivau_valor_tasado_nacional_ccaa_prov.csv | sí | provincia | 1995T1–2026T2 |
| `valor_tasado_ccaa` | Valor tasado medio de vivienda libre por CCAA, desde 1995T1 | euros/m2 | C4 | mivau_valor_tasado_nacional_ccaa_prov.csv (nivel ccaa) | sí | ccaa | 1995T1–2026T2 |
| `visados` | Viviendas libres iniciadas (visados de dirección de obra), nacional, flujo trimestral (MIVAU tabla 3.1) | viviendas | C4 | mivau_visados.csv (mensual 2008+, suma de 3 meses) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025) | sí | ccaa,nacional | 1995T1–2026T2 |
| `vut_pct_sobre_total` |  | % | C4 | ver diccionario del panel de origen | sí | municipio,provincia | 2020T3–2026T2 |
| `vut_plazas` | Plazas turísticas por provincia (INE experimental) | plazas | C4 | ine_vut_nacional_ccaa_prov.csv | sí | municipio,nacional,provincia | 2020T3–2026T2 |
| `vut_plazas_por_vivienda` |  | plazas/vivienda | C4 | ver diccionario del panel de origen | sí | municipio,provincia | 2020T3–2026T2 |
| `vut_registro_gva` | GVA, Registro de Turismo de la Comunitat Valenciana (cortes) | viviendas | C1 | GVA, Registro de Turismo de la Comunitat Valenciana (cortes) | sí | municipio | 2025-01-26–2026-10-14 |
| `vut_registro_gva_reconstruido` | GVA, registro (altas y bajas fechadas; reconstrucción propia) | viviendas | C4 | GVA, registro (altas y bajas fechadas; reconstrucción propia) | sí | municipio | 2015-01–2025-01 |
| `vut_regulacion_ccaa` | Norma autonómica de viviendas de uso turístico vigente (E23 Cataluña 2023-11-09, E24 C. Valenciana 2024-08-08, E25 Baleares 2025-04-16, E26 Canarias 2025-12-13) | 0/1 | C4 | v2_eventos_politica.csv | sí | ccaa | 2007T1–2026T2 |
| `vut_stock_gva` |  | viviendas (stock) | C4 | ver diccionario del panel de origen | sí | ccaa,municipio,provincia | 2010T1–2024T4 |
| `vut_viviendas` | Viviendas de uso turístico por provincia (INE experimental) | viviendas | C4 | ine_vut_nacional_ccaa_prov.csv | sí | ccaa,nacional,provincia | 2020–2026T2 |
| `vut_viviendas_turisticas` |  | viviendas | C4 | ver diccionario del panel de origen | sí | municipio,provincia | 2020T3–2026T2 |
| `zt_cuota_municipios` | Municipios en zona tensionada / municipios de la CCAA (diccionario INE 2026) | proporción | C4 | idem + ine_diccionario_municipios_2026.xlsx | sí | ccaa | 2007T1–2026T2 |
| `zt_declarada` | Al menos un municipio en zona tensionada vigente (Ley 12/2023, art. 18) | 0/1 | C4 | idem | sí | ccaa | 2007T1–2026T2 |
| `zt_n_municipios` | Municipios en zona tensionada vigente al cierre del trimestre (alcance parcial cuenta como municipio) | número | C4 | Resoluciones de zonas tensionadas, v3/zonas_tensionadas_v3.csv (fecha_efecto, fecha_fin_prevista) | sí | ccaa | 2007T1–2026T2 |
| `zt_vigente` | BOE, resoluciones de la Secretaría de Estado de Vivienda (zonas tensionadas) | 0/1 | C1 | BOE, resoluciones de la Secretaría de Estado de Vivienda (zonas tensionadas) | sí | municipio | 2024T1–2026T3 |
