# V15 · Inventario único de variables (fase 1.1)

Generado por `python3 src/v15/f1_inventario.py` desde data/base/hechos.parquet (base V10-V14), data/base/variables.parquet y docs/v15/inventario_anotaciones.csv. La tabla completa está en [inventario_variables.csv](inventario_variables.csv): una fila por variable × nivel × frecuencia. Los ficheros de datos versionados de data/raw y data/manual (con su clase de licencia), en [inventario_ficheros_fuera_base.csv](inventario_ficheros_fuera_base.csv).

- Variables distintas: 340; combinaciones variable × nivel × frecuencia: 467; filas: 14.523.489.
- Con alguna imputación (interpolación, reconstrucción o estimación): 20 combinaciones; con más del 20 % imputado: 20.
- Sin anotación de definición o rupturas: 0 combinaciones (se completan en la auditoría).
- No redistribuibles: 18 variables.
- Ficheros de datos versionados (data/raw y data/manual; docs/v13/datos_inventario.csv): 668 (clase a: 667, b: 1, c: 0).

## Por concepto

| Concepto | Variables | Filas |
|---|---|---|
| demografia | 59 | 5.767.171 |
| parque | 54 | 2.446.355 |
| precio_compra | 44 | 67.238 |
| alquiler | 38 | 1.450.159 |
| financiacion | 34 | 58.867 |
| turismo | 32 | 1.858.980 |
| renta | 21 | 448.993 |
| hogares | 16 | 114.603 |
| empleo | 15 | 2.170.492 |
| oferta | 11 | 127.889 |
| regulacion | 8 | 12.059 |
| otro | 6 | 405 |
| resultado_publicado | 2 | 278 |

## Variables con más del 20 % de filas imputadas (solo en robustez, regla A del plan)

| Variable | Nivel | Frecuencia | % imputado | Métodos |
|---|---|---|---|---|
| inmig_anual | nacional | T | 100.0 | interpolado |
| vut_registro_gva_reconstruido | municipio | M | 100.0 | reconstruido |
| v12_obra_neta | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| v12_hogares_nuevos_estimados | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| v12_ratio_obra_hogares | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| pib_ccaa_q | ccaa | T | 74.66 | interpolacion_loglineal_entre_anclas_T3 / observado_anual_ancla_T3 |
| pob_extranj | nacional | T | 74.19 | observado / interpolado |
| pob_extranj_ccaa_sum | nacional | T | 74.19 | interpolado_loglineal / observado |
| pob_extranj | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| pob_espanola | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| pob_total | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| vut_plazas | provincia | T | 45.83 | interpolado / observado |
| vut_viviendas | nacional | T | 45.83 | interpolado / observado |
| vut_viviendas | ccaa | T | 45.83 | interpolacion_lineal_entre_observaciones / observado |
| vut_viviendas | provincia | T | 45.83 | interpolado / observado |
| vut_plazas | nacional | T | 45.83 | interpolado / observado |
| visados | nacional | T | 41.94 | observado / interpolado |
| terminadas | nacional | T | 41.27 | interpolado / observado |
| pob_total | nacional | T | 41.27 | observado / interpolado |
| pob_extranj_ine | nacional | T | 38.78 | observado / interpolado |

## Rupturas anotadas

| Familia | Rupturas | Documento |
|---|---|---|
| adrh_gini | Tabla de relaciones del seccionado 2021–2023 no localizada; ADRH 2019–2023 por sección en el manifiesto. | docs/v10/diccionario_base.md l.49-51; data/raw/_manifest.csv l.99; docs/v3/fuentes_fallidas.md l.25 |
| aeat_irpf_declaraciones | Unidades dudosas 2013–2015. Periodo 2016–2024 en la base frente a 2013–2024 en el manifiesto. Licencia en conflicto (AEAT «reutilización con cita» frente a «no verificada»): clase b. | docs/v10/diccionario_base.md l.52-58; data/raw/v11/_manifest.csv l.2; docs/v13/datos_deposito.md l.61,85-89; docs/v15/punto_partida.md l.46 |
| asilo_solicitantes | Protección temporal desde 2022-03; Interior (protección internacional) inaccesible; no distingue provincias. | docs/v10/diccionario_base.md l.59,267-268; docs/v11/cobertura.md l.97,115-119 |
| bce_cuota_tipo_variable | no consta. | docs/v10/diccionario_base.md l.59-62; docs/v9/diccionario_v9.md l.82-89 |
| bcn_hut_registro | Conflicto: base da serie 2018T2–2026T3; manifiesto sin serie temporal (solo año de expediente). Cortes trimestrales con anti-bot. | docs/v10/diccionario_base.md l.63; data/raw/v9/_manifest.csv l.9; docs/v11/inventario.md l.229 |
| bls_criterios_dif | Rechazo solo desde 2015T2; resto no consta. | docs/v10/diccionario_base.md l.64-69 |
| c21md_hogares_muestra | Muestra 10 %. Celdas pequeñas: no redistribuibles (clase b). | docs/v10/diccionario_base.md l.70; docs/v11/cobertura.md l.47-59; docs/v13/datos_deposito.md l.24-28 |
| catastro_inspire_edificios | Asignación a sección INE 2025. Tabla de relaciones del seccionado 2021–2023 no localizada (armonización bloqueada). | docs/v10/diccionario_base.md l.71-75; data/raw/v11/_manifest.csv l.5-7; docs/v3/fuentes_fallidas.md l.25 |
| catastro_tit_titulares | No encadenar JAXI con sujetos pasivos desde 2024 (base l.76-78). Conflicto: base da JAXI 2012–2023; manifiesto del fichero da 2006–2023. | docs/v10/diccionario_base.md l.76-78,344-348; data/raw/v11/_manifest.csv l.104-112 |
| catastro_viviendas_por_anio_construccion | Solo 2019; sin serie. | docs/v10/diccionario_base.md l.81-82; data/raw/v11/_manifest.csv l.103 |
| censo2011_viviendas | Comparabilidad con el Censo 2021: no consta. | docs/v10/diccionario_base.md l.83; docs/v11/inventario.md l.36 |
| censo2021_t10_1 | Seccionado 2021; relaciones 2021–2023 no localizadas. Versión provisional en v3 (manifiesto). | docs/v10/diccionario_base.md l.84-119; docs/v3/fuentes_fallidas.md l.25; data/raw/_manifest.csv l.96-98 |
| compraventas | Monitor desde 2023-08 (base l.209-210). Sin otra ruptura documentada. | docs/v10/diccionario_base.md l.120-122,209-210; docs/diccionario_variables.md l.119-120 |
| costes | Cobertura inicial de costes: 1980T1 (diccionario_variables l.115) frente a 1995T1 (base l.123): conflicto menor. | docs/diccionario_variables.md l.115-116; docs/v10/diccionario_base.md l.123-124,266 |
| credito_construccion | no consta. Origen en data/raw/v5 sin manifiesto global. | docs/v10/diccionario_base.md l.125-128; docs/v11/inventario.md l.223 |
| credito_stock | credito_stock_bde: primer dato 1997T3; resto no consta. | docs/v10/diccionario_base.md l.129-131; docs/diccionario_variables.md l.113 |
| deflactor | No consta cambio de base de la CNT. pib_ccaa_anual repite el anual en cuatro trimestres; pib_ccaa_q solo robustez; deflactor aproximado. | docs/v10/diccionario_base.md l.235-239,269,272-273; docs/diccionario_variables.md l.103,146; docs/limitaciones.md l.12 |
| ecp_pob_nacionalidad | ECP trimestral desde 2021; antes semestral. | data/base/variables.parquet (anotación del orquestador) |
| ecp_pob_viv_familiares_nacionalidad | Suma de 17 CCAA frente a nacional: −2,09 % a +1,30 % (diccionario_variables l.141). Padrón termina en 2022; ECP desde 2021 trimestral. | docs/v10/diccionario_base.md l.135-136,232,249-252; docs/diccionario_variables.md l.124,133,141; data/raw/v9/_manifest.csv l.96 |
| em_emigracion_extranjero | Series EM terminan en 2021; la EMCR toma el relevo en 2021 (quiebre de fuente documentado para la inmigración anual). | docs/v10/diccionario_base.md l.137-139; docs/v11/inventario.md l.37-40; data/raw/_manifest.csv l.64 |
| emal_n_fianzas | Datos 2016–2025T4. Hojas A1–A2.4 solo en XLSX original. Sin ruptura documentada. | docs/v9/diccionario_v9.md l.9-22; docs/v10/diccionario_base.md l.140-142; data/raw/v9/_manifest.csv l.13-16 |
| emcr_md_altas_interno | Inicio 2021: quiebre de fuente en inmigración (diccionario_variables l.156); solo cuatro años (l.155). | docs/v10/diccionario_base.md l.143-149; docs/diccionario_variables.md l.155-156; data/raw/_manifest.csv l.52-53 |
| epa_pob_total | Cambio de base EPA 2021T1: no consta para esta tabla. | docs/v10/diccionario_base.md l.150; docs/diccionario_variables.md l.204 |
| euribor | tipo_bce escalonado, sin interpolar (escalón vigente). | docs/v10/diccionario_base.md l.151-153,311-312,320; docs/diccionario_variables.md l.107 |
| eurostat_plataformas_noches | Ruptura en 2025 (fuente oficial con datos de 4 plataformas). | docs/v10/diccionario_base.md l.154,216; docs/v9/diccionario_v9.md l.73-79 |
| evr_altas_interno | EVR antes de 2008 con huecos; bajas al extranjero desde 2002; quiebre de fuente 2021 (paso a EMCR). | docs/v10/diccionario_base.md l.155-159; docs/v11/cobertura.md l.10-16; docs/v11/inventario.md l.229 |
| fianzas_importe_media | Sin ruptura documentada. El tramo 2020–2026 es idéntico byte a byte al de data/raw/v5. Contrato nuevo o vigente: no consta. | docs/v10/diccionario_base.md l.160-162,211; docs/v9/diccionario_v9.md l.104-106; data/raw/v9/_manifest.csv l.23-30 |
| gva_bdo_afiliados | Diciembres 2011–2021 y mensual desde 2022 (municipal). Afiliación de extranjeros solo provincial. | docs/v10/diccionario_base.md l.163,302-307; docs/v11/cobertura.md l.37-38,97-98 |
| hicp_alquiler_indice | Cambio metodológico IPC base 2021 resuelto por INE (fecha no consta). Clasificación ECOICOP v2 en la tabla provincial, sin detalle. HICP: no consta. | docs/v10/diccionario_base.md l.164,194-196,214; docs/v8/diccionario.md l.69; docs/v6_2/cifras_publicables.md l.13; data/raw/_manifest.csv l.62 |
| hip_importe | Tabla 76317 descrita como «base nueva» en el manifiesto; fecha del cambio de base: no consta. | docs/v10/diccionario_base.md l.165-166,212; data/raw/_manifest.csv l.60 |
| hogares_ecp | No empalmada con la EPA (la EPA es 0,38–1,01 % mayor en el solape). La ECP no publica hogares por nacionalidad. | docs/diccionario_variables.md l.126,138; docs/v10/diccionario_base.md l.167; docs/v11/cobertura.md l.58-64 |
| hogares_epa | EPA 2021T1: nueva definición de hogar (presupuesto compartido, Reg. UE 2019/1700) y factores de elevación del Censo 2021; −1,1 % en 2021T1. | docs/diccionario_variables.md l.125,138-139; docs/v10/diccionario_base.md l.168 |
| iab_disponibilidad_365_media | Solo ediciones de 2026-09; las históricas no son públicas. | docs/v10/diccionario_base.md l.171-178; docs/v9/diccionario_v9.md l.62-71 |
| idescat_apartamentos_n | Registre sin fechas de alta; IEET sin código de municipio (requiere tabla nombre→INE); licencia de Catalunya «See Terms of Use». Sin otra ruptura documentada. | docs/v10/diccionario_base.md l.179-182,270-271; data/raw/v9/_manifest.csv l.10-12; data/raw/v11/_manifest.csv l.119-122 |
| incasol_contratos | Licencia «See Terms of Use»: no redistribuible (clase b). | docs/v9/diccionario_v9.md l.91-102; data/raw/v9/_manifest.csv l.36 |
| ine_tmov_interno_turistas | Teléfonos móviles: estadística experimental. FRONTUR: no consta. | docs/v10/diccionario_base.md l.183-184,326-327 |
| ine_vut_plazas | Estadística experimental; edición de noviembre de 2026 no publicada. | docs/v10/diccionario_base.md l.185-187,358-366; docs/v11/inventario.md l.229 |
| inflacion_deflactor | Ruptura IPC base 2021 documentada solo para la subclase alquiler; para el IPC general, no consta. | docs/v10/diccionario_base.md l.188-189; docs/v8/diccionario.md l.69 |
| iniciadas | Permisos = Eurostat sts_cobp_q, índice 2021=100 (SCA); el conflicto con «visados MIVAU» era un error de metadatos de la base, corregido en V15 (ERRATA). Visados sin datos abril–junio de 2016 y 2017. | docs/v10/diccionario_base.md l.190-191,234,353; docs/diccionario_variables.md l.114,117,149 |
| inmig_anual | Quiebre de fuente 2021: paso a EMCR (2019 = 750.480; 2020 = 467.918; 2021 = 887.960). | docs/v10/diccionario_base.md l.192-193; docs/diccionario_variables.md l.127-128,156 |
| ipv | Base 2015=100 (base 2010 l.197). Conflicto: decisiones.md l.14 cita «INE IPV base 2025»; v8 l.62 dice que 25171 es base 2007 reescalada, y diccionario_variables l.96 que es base 2015. Sin resolver. | docs/v10/diccionario_base.md l.197-200; docs/diccionario_variables.md l.93-96; docs/v8/diccionario.md l.62; docs/decisiones.md l.14; docs/v4/decisiones.md l.86 |
| monitor_ipv_general | Las mismas que la serie de origen. | data/base/variables.parquet (anotación del orquestador) |
| monitor_poblacion | ECP semestral hasta 2020 y trimestral desde 2021; interpolación 1995–2020 (diccionario_variables l.123, 151). | docs/v10/diccionario_base.md l.217,257; docs/diccionario_variables.md l.123,151 |
| notariado_cgn_extranj | Difiere 9,4 % del MIVAU (concepto distinto). Licencia no verificada: derivado en clase (b). | docs/diccionario_variables.md l.131; docs/v13/datos_deposito.md l.56,91-95 |
| notariado_cuantia_esp_prov | Semestral; concepto distinto del MIVAU (diferencia de 9,4 % en extranjeros). Comparte fuente notarial con el IPV del INE: no es fuente independiente del IPV. | docs/diccionario_variables.md l.131; data/base/variables.parquet (anotación del orquestador) |
| obra_nueva_neta_catastro | Etiqueta de año corregida en V15 (antes un año tarde; ERRATA). Regularización catastral 2013-2017. INSPIRE: 94 municipios (cobertura). | docs/v10/diccionario_base.md l.221-222; docs/v11/cobertura.md l.128-129 |
| ocupados | EPA 2021T1: cambio de base de factores de elevación; efecto declarado por el INE «no relevante», no medido. Tasa y parados con el mismo cambio. | docs/diccionario_variables.md l.100,140; docs/v10/diccionario_base.md l.223-226,233,308; docs/v8/diccionario.md l.307 |
| opi_residentes_documentados | Concepto administrativo (documentación), no residencia: no comparable con padrón ni ECP. | data/base/variables.parquet (anotación del orquestador) |
| p_bde | Serie BdE general declarada igual a p_tasado en limitaciones (l.11), pero listada como serie separada en la base (l.228): conflicto. Nueva y usada desde 2013T1; sin ruptura documentada. | docs/v10/diccionario_base.md l.228-230; docs/limitaciones.md l.11; docs/diccionario_variables.md l.98 |
| p_tasado | Sin cambio de base documentado. Nacional desde 1995T1; municipal desde 2005 (manifiesto). Limitaciones dice p_bde = p_tasado en la base (no verificado). | docs/diccionario_variables.md l.97; docs/v10/diccionario_base.md l.231,351-352; docs/v15/punto_partida.md l.40; docs/limitaciones.md l.11; data/raw/_manifest.csv l.80-81 |
| pob_africa | Europa no UE: UE28 (2002–2020) y UE27 (2021–2025) con periodos disjuntos; enlace no consta. | docs/v10/diccionario_base.md l.240-248,258-259; data/raw/_manifest.csv l.65-66 |
| pob_censo_anual | Cuadre: suma de provincias = nacional. Sin otra ruptura documentada. | docs/v9/diccionario_v9.md l.24-40; docs/v10/diccionario_base.md l.243 |
| pob_vlc_africa | Padrón 2014 no publicado; 2011 por sexo excluido; altas y bajas desde 2017 sin informe; padrón por nacionalidad hasta 2022. | docs/v11/cobertura.md l.137-152; docs/v10/diccionario_base.md l.260-265,355-357; docs/limitaciones.md l.13 |
| registr_num_4tm | Medias móviles de 4 trimestres: no se pueden leer como dato trimestral; inscripción posterior a la escritura (desfase). | docs/v14/decisiones.md E9; data/base/variables.parquet (anotación del orquestador) |
| registradores_compraventas_anual | Solo dato anual en T4; no se reconstruye trimestral (diccionario_variables l.142). Datos ODbL 1.0; Anuario ERI no redistribuible. | docs/diccionario_variables.md l.129-130,142; docs/v10/diccionario_base.md l.378 |
| salario | 2008T1: cambio de base y de clasificación (CNAE-93 a CNAE-2009) y de tabla. | docs/v10/diccionario_base.md l.274-275; docs/v8/diccionario.md l.152 |
| serpavi_alquiler_m2_mediana | Sin cambio de base documentado. Contraste con IPVA no independiente (ambos AEAT-IRPF). esp_constante excluye Navarra y País Vasco. | docs/v10/diccionario_base.md l.278-302; docs/revision_f1_fuentes.md l.29; docs/diccionario_variables.md l.132,144 |
| terminadas | Mensual desde 2008 y anual 1991–2025 en provincias. Vivienda protegida ausente (limitaciones l.30). | docs/v10/diccionario_base.md l.309-310; docs/diccionario_variables.md l.118; docs/limitaciones.md l.30 |
| tipo_hip | BdE desde 1995T1; BCE desde 2003T1; resto no consta. | docs/v10/diccionario_base.md l.313-316; docs/diccionario_variables.md l.105 |
| tope_rentas_ccaa | zt_vigente 2024T1–2026T3; primera resolución 2024-03-16. Tope: ventana 2020-09-22 a 2022-04-08; STC 37/2022; variante v3 hasta 2021-09-21. | docs/v10/diccionario_base.md l.321-323,367-370; data/raw/_manifest.csv l.87 |
| trans_total | no consta. Total hasta 2026T1. | docs/diccionario_variables.md l.121; docs/v10/diccionario_base.md l.325,330; data/raw/_manifest.csv l.74,75 |
| v12_hogares_2011_2021_crecimiento | Comparabilidad 2011–2021 y muestra de hogares: no consta. | docs/v10/diccionario_base.md l.331-343 |
| v5_deficit_2021_2025 | Ligados a la edición de la 1.0. | data/base/variables.parquet (anotación del orquestador) |
| vlc_altas_bajas | Sin informe desde 2017; altas y bajas por nacionalidad solo en tablas crudas. | docs/v10/diccionario_base.md l.354; docs/v11/cobertura.md l.144-148 |
| vut_registro_gva | Corte de 2026 sin bajas: altas y bajas posteriores a enero de 2025 no se pueden fechar. El reconstruido es un supuesto de fechado. | docs/v9/diccionario_v9.md l.54-60; docs/v10/diccionario_base.md l.361-364 |
