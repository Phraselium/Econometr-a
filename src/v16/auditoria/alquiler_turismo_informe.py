"""Texto del informe de la auditoría alquiler_turismo; las cifras salen del diccionario de diagnósticos D."""


def pc(x, n=0):
    return f"{100 * x:.{n}f} %"


def informe(D):
    s = D["1a_saltos_municipio"]["ia_anuncios_total_numero"]
    v = D["1a_var_area_consecutiva"]
    act = D["1a_cuota_activos_sobre_total_por_area"]
    reg = D["1b_ia_vs_vut_niveles_2026-09"]
    cv = D["1c_ia_vs_vte"]
    e1 = reg["Euskadi_REATE__IA_entera__umbral1"]
    c1 = reg["Cataluna_HUT__IA_entera__umbral1"]
    a1 = reg["Andalucia_OpenRTA__IA_entera__umbral1"]
    t1 = cv["IA_entera_2026-06__VTE_viviendas_2026-05__umbral1"]
    t20 = cv["IA_entera_2026-06__VTE_viviendas_2026-05__umbral20"]
    ta = cv["IA_activos_2026-06__VTE_viviendas_2026-05__umbral1"]
    tv = cv["variacion_log_IA_entera_2025-12_2026-06_vs_VTE_2025-11_2026-05"]
    ciu = D["1b_ciudades_IA_registro_VTE"]
    m = D["1d_precio_moneda"]
    pr = D["1d_precio_mediana_ciudades"]
    gh = D["2_gva_historico"]
    gc = D["2_gva_cortes"]["total"]
    ra = D["2_openrta_codigos_registro_repetidos"]
    u = D["3_unidades_y_rangos"]
    at = D["3_atipicos_yoy_log_z>5"]
    vz = D["3_vte_variacion_entre_cortes_municipal"]["2025-05->2025-11"]
    ev = D["3_eoap_pernoctaciones_vs_vte"]
    oe = D["3_oat_vs_eoap_pernoctaciones"]["nacional"]
    ip = D["3_ipap_coherencia_tasa"]
    z = D["4_peso_zonas_descartadas"]
    z39 = z["tabla2039_pernoctaciones_12m_2025-09_2026-08"]
    z22 = z["tabla2022_plazas_apartamentos_2026-08"]
    z48 = z["tabla48432_OAT_zonas"]
    sol = D["3_solapes_crudo_mismo_COD_fecha"]
    return f"""# Auditoría de datos V16, familia alquiler_turismo (fase 1, C4 descriptivo)

SEED=20261010. Script: `src/v16/auditoria/alquiler_turismo.py`. Entrada: `data/processed/v16/alquiler_turismo.parquet` con `muestra_sellada_v6 == False`. Solo descriptivo. Los recuentos de OpenRTA (terceros) se usan solo como agregados propios.

## 0. Alcance tras el filtro de la muestra sellada
- Madrid, Mallorca, Menorca, Canarias e ISTAC quedan sin filas: no se audita el corte de formato de Madrid VUT ni los duplicados de sus cortes (solo consta lo declarado en la ficha). Inside Airbnb: Barcelona, Girona, Euskadi, Málaga, Sevilla y València.
- Incidencia de marcado: {D["2_filtrado"]["filas_ccaa_de_regiones_selladas_con_marca_False_excluidas"]:,} filas de nivel `ccaa` de regiones enteramente selladas (Aragón, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra, La Rioja) llevan `False`. Se han excluido de todos los cálculos y conviene revisar la marca en la fase de datos.

## 1. Inside Airbnb
- Saltos entre instantáneas consecutivas (municipios con 20 o más anuncios en ambas): {s["n_saltos_>25%"]} de {s["pares_municipio_ronda_>=20_en_ambas"]} pares superan el 25 % y {s["n_saltos_>50%"]} el 50 % (3 de Girona, 1 de Euskadi y València, todos entre 2026-03 y 2026-06). En València el total pasa de 7.697 (2025-12) a 4.927 (2026-03) y a 7.848 (2026-06): {pc(v["Valencia"]["2025-12->2026-03"])} y +{pc(v["Valencia"]["2026-03->2026-06"])}, con precio ausente en esa foto; la instantánea de 2026-03 de València parece parcial. Entre 2026-03 y 2026-06 el total sube también en Girona (+{pc(v["Girona"]["2026-03->2026-06"])}), Euskadi (+{pc(v["Euskadi"]["2026-03->2026-06"])}), Málaga (+{pc(v["Malaga"]["2026-03->2026-06"])}) y Sevilla (+{pc(v["Sevilla"]["2026-03->2026-06"])}), tras caídas de 6-8 % en diciembre-marzo en Euskadi, Málaga y Sevilla: patrón común, compatible con estacionalidad o con la captura. Barcelona baja en tres trimestres seguidos ({pc(v["Barcelona"]["2025-12->2026-03"],1)}, {pc(v["Barcelona"]["2026-03->2026-06"],1)}, {pc(v["Barcelona"]["2026-06->2026-09"],1)}).
- Cobertura: entran 4-7 y salen 2-3 municipios por trimestre, con 1-2 anuncios cada uno (puntos del borde del área). Secciones: {D["1a_secciones"]["secciones_variacion_>50%_(>=20_anuncios_en_ambas)"]} de {D["1a_secciones"]["secciones_pares_evaluables"]} pares con variación superior al 50 %.
- Activos: la cuota de activos sobre el total cae en 2026-09 a {pc(act["Sevilla"]["2026-09"])} (Sevilla), {pc(act["Malaga"]["2026-09"])} (Málaga), {pc(act["Valencia"]["2026-09"])} (València), {pc(act["Barcelona"]["2026-09"])} (Barcelona), frente a 90-99 % antes; activos y vivienda entera no son comparables entre 2026-06 y 2026-09.
- Contra registros VUT (2026-09, vivienda entera): Euskadi (REATE, n={e1["n"]}) Pearson {e1["corr_pearson"]}, Spearman {e1["corr_spearman"]}, razón agregada {e1["ratio_agregado"]}; Cataluña (HUT, n={c1["n"]}) Pearson {c1["corr_pearson"]}, Spearman {c1["corr_spearman"]}, razón agregada {c1["ratio_agregado"]} (mediana {c1["ratio_mediana"]}); Andalucía (OpenRTA completa más habitaciones, n={a1["n"]}, solo Málaga y Sevilla y sus bordes) razón agregada {a1["ratio_agregado"]}; València (GVA, n=1) {ciu["46250"]["IA_entera_2026-09"]:,.0f} frente a {ciu["46250"]["registro_VUT"]:,.0f}. Variaciones: Euskadi (altas REATE 2026 sin bajas, n=37) correlación {D["1b_ia_vs_vut_variaciones"]["Euskadi_REATE_altas_2026_sin_bajas"]["corr_variaciones_abs"]}; no hay serie de bajas alineada en València ni en Cataluña.
- Contra VTE del INE ({cv["municipios_comunes_IA_VTE"]} municipios comunes; IA 2026-06 frente a VTE 2026-05): vivienda entera n={t1["n"]}, Pearson {t1["corr_pearson"]}, Spearman {t1["corr_spearman"]}, razón media {t1["ratio_medio"]}, razón agregada {t1["ratio_agregado"]}; con 20 o más anuncios n={t20["n"]}, Pearson {t20["corr_pearson"]}, razón media {t20["ratio_medio"]}. Con anuncios activos la razón agregada es {ta["ratio_agregado"]}. Las variaciones (IA 2025-12 a 2026-06 frente a VTE 2025-11 a 2026-05, n={tv["n"]}) no se corresponden: correlación {tv["corr"]}, {tv["signo_opuesto_n"]} municipios con signo opuesto.
- Precio: el símbolo «$» es un rótulo del fichero. En {m["snapshots_leidos"]} instantáneas, {m["moneda_quote"].get("EUR", 0):,} cotizaciones declaran `currency = EUR` (ninguna otra moneda), {m["precio_con_$"]:,} precios llevan «$» y ninguno «€», y el precio coincide con la cotización por noche en el 100 % de los casos ({m["precio_igual_a_cotizacion_noche"][0]:,} de {m["precio_igual_a_cotizacion_noche"][1]:,}). Medianas municipales: sin valores fuera de 10-1500 ni atípicos entre municipios con 20 o más precios, pero las medianas de ciudad oscilan (Sevilla {pr["Sevilla"]["2026-03"]} / {pr["Sevilla"]["2026-06"]} / {pr["Sevilla"]["2026-09"]}; Donostia {pr["Donostia"]["2026-03"]} / {pr["Donostia"]["2026-06"]} / {pr["Donostia"]["2026-09"]}), coherente con una cotización de estancia futura que varía de una foto a otra.

## 2. Registros VUT
- GVA: el total de los cortes pasa de {gc["2025-01-26"]:,.0f} (2025-01-26) a {gc["2026-10-14"]:,.0f} (2026-10-14); sin duplicados de signatura en ninguno. Las signaturas de 2025 y de 2026 no comparten formato (0 coincidencias), de modo que las bajas posteriores a enero de 2025 no se pueden obtener por diferencia. En el histórico: {gh["baja_anterior_a_alta"]} bajas anteriores a su alta, {gh["estado_BAJA_sin_fecha_baja"]} registros en BAJA sin fecha, {gh["altas_antes_2015"]:,} altas anteriores a 2015 (migración del registro).
- Euskadi REATE: 1 número de registro repetido en 4.738. OpenRTA: {ra["repeticiones_extra"]} repeticiones de {ra["distintos"]:,} códigos (cota superior; esquema mixto); el acumulado de altas es monótono en todas las series; reconstrucción con sesgo de supervivencia.

## 3. INE
- Solapes: {sol["solapes_entre_tablas"]:,} claves (COD, fecha) repetidas entre tablas, con {sol["discrepancias_de_valor"]} discrepancias de valor; el parquet no tiene duplicados de clave.
- Rangos: los {u["porcentaje_fuera_0_100"][1]:,} valores en % están en [0, 100]; plazas por vivienda de VTE calculadas y publicadas coinciden en todos los casos; {u["VTE_plazas_por_vivienda_>20"]} observaciones superan 20 plazas por vivienda (percentil 99: {u["VTE_plazas_por_vivienda_p1_p50_p99"][2]}).
- Atípicos (|z robusto| > 5 de la tasa interanual logarítmica, {at["series_mensuales_evaluadas"]:,} series): {at["n_atipicos"]:,} marcas, {at["n_en_ventana_covid_2020-03_2022-06"]:,} en 2020-03 a 2022-06; fuera de esa ventana {at["n_fuera_covid"]:,} en {at["series_distintas_fuera_covid"]} series (EOH {at["por_operacion_fuera_covid"]["eoh"]}, EOAP {at["por_operacion_fuera_covid"]["eoap"]}, EOT {at["por_operacion_fuera_covid"]["eot"]}, OAT {at["por_operacion_fuera_covid"]["oat"]}); casos extremos: pernoctaciones hoteleras de Cantabria en 2012-01 (log interanual -2,53) y plazas hoteleras de Melilla en 2004.
- Rupturas: la serie antigua de EOAP y «total categorías» solo comparten el agregado nacional (29 pares) y difieren en media entre 91 % y 259 % según variable: no se puede empalmar; EOH no tiene territorios comunes. Bajo el mismo nombre `ine_eot_pernoctaciones_total` conviven dos series (COD EOT732 y EOT1145, p. ej. 5,7 y 1,2 millones en junio de 2026): no deben sumarse ni compararse sin asignar la operación. VTE: entre 2025-05 y 2025-11 el total municipal cae {vz["var_total_pct"]} % y {vz["n_pasan_a_0_o_ausentes"]} municipios pasan a 0 o desaparecen (89-147 en otros cortes); los cortes alternan febrero y agosto, por lo que parte de la variación es estacional. IPAP: tras reindexar el mes ausente (2020-05), tasa calculada y publicada difieren {ip["dif_abs_media_pp"]} pp de media (máximo {ip["dif_abs_max_pp"]} pp).
- EOAP frente a VTE (provincias, n=17): pernoctaciones de 12 meses frente a plazas VTE, Pearson {ev["provincia_2025-11"]["EOAP_pernoct12m_vs_VTE_plazas"]["corr_pearson"]} (2025-11) y {ev["provincia_2026-05"]["EOAP_pernoct12m_vs_VTE_plazas"]["corr_pearson"]} (2026-05); la variación interanual correlaciona {ev["provincia_2025-11"]["variacion_log_12m_EOAP_pernoct_vs_VTE_plazas"]["corr"]} y {ev["provincia_2026-05"]["variacion_log_12m_EOAP_pernoct_vs_VTE_plazas"]["corr"]}, con signo opuesto en {ev["provincia_2025-11"]["variacion_log_12m_EOAP_pernoct_vs_VTE_plazas"]["signo_opuesto_n"]} y {ev["provincia_2026-05"]["variacion_log_12m_EOAP_pernoct_vs_VTE_plazas"]["signo_opuesto_n"]} provincias. En municipios (n=14-16) Pearson 0,2-0,3. OAT frente a EOAP (nacional): razón de pernoctaciones de {oe["razon_por_anio"]["2018"]} (2018) a {oe["razon_por_anio"]["2025"]} (2025), correlación interanual {oe["corr_yoy_log"]}.

## 4. Series sin código INE descartadas (870)
- Distribución: tabla 2013 (336), 2022 (264), 2039 (192), 48432 (78). Sin las zonas de regiones selladas: las zonas de la tabla 48432 (OAT) suman {z48["suma_zonas_por_anio"]["2025"]/1e6:.1f} millones de pernoctaciones en 2025 frente a {z48["OAT_nacional_anual"]["2025"]/1e6:.1f} del total nacional ({pc(z48["suma_zonas_por_anio"]["2025"]/z48["OAT_nacional_anual"]["2025"])}); las de la tabla 2039 suman {z39["suma_zonas_sin_versiones_solapadas"]/1e6:.1f}-{z39["suma_zonas_bruta"]/1e6:.1f} millones en 12 meses, {pc(z39["cuota_sin_solapes_sobre_EOH"])}-{pc(z39["cuota_bruta_sobre_EOH"])} de las pernoctaciones hoteleras nacionales (la tabla no declara operación); plazas de apartamentos en zonas (tabla 2022): {z22["suma_zonas_sin_solapes"]:,.0f}-{z22["suma_zonas"]:,.0f} frente a {z22["suma_provincias_EOAP_no_selladas"]:,.0f} en las provincias de EOAP (versiones solapadas de una misma zona pueden duplicar). Además, 136 series VTE de municipio con nombre repetido y 91 sin coincidencia quedan fuera.
"""
