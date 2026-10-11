# Diccionario de variables v6 (M0)

Fecha de construcción: 2026-10-11. Script: `src/v6/m0_run.py` (sin red). Entradas: `data/raw` y salidas v5/v5_1 versionadas.
Paneles de entrenamiento: `output/v6/M0/paneles/*_train.csv.gz`. Cobertura calculada solo sobre la parte de entrenamiento
(el lado sellado se describe por número de unidades y años en `output/v6/M0/sellado.md`).

Convenciones: `ln_` = logaritmo natural; `d_` = diferencia anual del logaritmo; `_pct` = porcentaje; `share_` = proporción en %.
Unidades: alquiler en €/m²/mes y €/mes; compra en €/m²; contratos nuevos en € de fianza (depósito, **no** renta mensual).
Interpolación: ninguna. Agregación temporal: media de meses o trimestres publicados, o suma (volúmenes), solo si hay el número
mínimo de observaciones indicado; si no, NaN. Ninguna observación imputada, así que no hay columnas `_interp` que marcar.
Extrapolación: ninguna. Las variables estáticas o de corte transversal (costa, isla, distancia, censo 2021) van en
`prov_estatico.csv` y `mun_estatico.csv`, no repetidas en el tiempo.

## 1. Medidas de resultado (principal y robustez)

| Mercado | Nivel | PRINCIPAL | Robustez |
|---|---|---|---|
| Alquiler de stock | provincia | `ln_alq_m2_serpavi_vc` (SERPAVI, mediana VC, €/m²/mes, 2011-2024) | `ln_alq_mes_serpavi_vc` (€/mes); `ln_ipc_alq_idx` (IPC alquiler, índice, 2002-2025) |
| Alquiler de stock | municipio | `ln_alq_m2_serpavi_mun` (SERPAVI municipal, mediana VC) | — |
| Alquiler de stock | distrito / sección | `ln_alq_m2_serpavi_dis` (SERPAVI distrito v3, punto medio p25-p75) | `ln_alq_m2_p25_dis`, `ln_alq_m2_p75_dis` (en el panel, N4) |
| Contratos nuevos | provincia | `ln_fianza_media_gva_eur` (GVA, solo 3 provincias CV) | `ln_n_fianzas_gva`; `pct_fianzas_600_incasol` (Incasòl, 4 provincias CAT); `ln_ipva_nuevo_idx` (IPVA nuevo, 38 provincias) |
| Contratos nuevos | municipio | `ln_fianza_media_gva_mun_eur` (GVA municipal) | `ln_n_fianzas_incasol_mun`, `pct_fianzas_600_incasol_mun` |
| Precio de compra | provincia (anual) | `ln_pm2_tasado` (valor tasado MIVAU, €/m², media de 4 trimestres) | `ln_pm2_registradores` (Registradores, pm2 anual) |
| Precio de compra | provincia (trimestral) | `ln_pm2_tasado` (MIVAU trimestral) | — |
| Precio de compra | municipio | `ln_pm2_tasado_mun` (MIVAU municipal, nombre único) | — |
| Precio de compra | nacional / CCAA | índice triangulado A23 (`idx_triang_*`, nacional) | IPV INE (solo CCAA, `ccaa_ipv_anual_desc.csv`) |
| Volumen de compra | provincia | `ln_cv_etdp` (compraventas INE ETDP, suma anual, 12 meses) | `ln_cv_registradores` (Registradores); `ln_hip_viv_num` (hipotecas nº) |
| Volumen de compra | provincia (trimestral) | `ln_cv_etdp` (suma trimestral, 3 meses) | — |

Medida de precio declarada en `resultado.json` (`medida_precio`): valor tasado MIVAU (provincia y municipio), Registradores,
índice triangulado A23 (nacional), IPV INE (solo CCAA). Notariado: solo Comunitat Valenciana, sin panel M0 (ver sin dato).

## 2. Variables de los paneles de modelización

Nivel: P = provincia, M = municipio, D = distrito. Fuentes en `data/raw` salvo que se indique.

| Variable | Panel | Definición y transformación | Frecuencia original | Fuente | Fecha del dato | Capa | Cobertura train (unidades / años) |
|---|---|---|---|---|---|---|---|
| ln_pm2_tasado | prov_compra_anual, prov_trim_compra | valor tasado libre, €/m², ln | trimestral → anual (4 trim.) / trimestral | MIVAU sedal (`mivau_valor_tasado_nacional_ccaa_prov`) | 2025 (anual), 2026T1 | C4 | 38 / 2015-2024 (anual); 38 / 2015-2025 (trim.) |
| ln_pm2_registradores | prov_compra_anual | pm2 compraventas vivienda, ln | anual (T4 suma móvil) | Registradores OpenData (`pdf/registradores_opendata_anual`) | 2025 | C4 | 41 / 2015-2024 |
| ln_cv_etdp | prov_compra_anual, prov_trim_compra | compraventas viviendas (total), ln, suma de 12 (anual) o 3 (trim.) meses | mensual | INE ETDP tabla 6150 (`ine_v2_etdp_prov`) | 2026-06 (último trimestre completo) | C1 si se cruza con Registradores (ver A23) | 41 / 2015-2024 |
| ln_cv_registradores | prov_compra_anual | compraventas viviendas nº, ln | anual | Registradores | 2025 | C4 | 41 |
| share_nueva_etdp | prov_compra_anual | nueva / total compraventas, % | mensual → anual | INE ETDP | 2025 | C4 | 41 |
| ln_hip_viv_num | prov_compra_anual, prov_trim_compra | hipotecas sobre viviendas, nº, ln (suma 12/3 meses) | mensual | INE HPT tabla 76317 | 2025 | C4 | 41 |
| share_contado_proxy | prov_compra_anual | 100·(1 − hipotecas nº / compraventas ETDP), **proxy** (las hipotecas incluyen operaciones no ligadas a compra) | anual | INE HPT + ETDP | 2025 | C4 (proxy) | 41 (399 obs) |
| share_compra_ext_res_pct | prov_compra_anual | compras de extranjeros residentes (tx) / compraventas ETDP, % | trimestral → anual (4 trim.) | MIVAU transacciones extranjeros | 2025 | C4 | 38 |
| no_res_share_R1A_pct | prov_compra_anual | % no residentes (R1A) | **solo 2015, 2016 y 2025 en la fuente R1A** | output/v5/R1A | 2016 | C4 | 38 (76 obs, 2015-2016) |
| ln_pob | prov_compra_anual | población total 1 enero, ln | anual | INE padrón (`ine_v2_padron_prov_pais`) | 2025-01-01 | C1 (INE) | 41 |
| share_ext_pob | prov_compra_anual | población extranjera / total, % | anual | INE padrón | 2025 | C1 | 41 |
| share_20_34 | prov_compra_anual | población 20-34 / población 20+ (ambos sexos) — **no es jóvenes en casa de los padres** | anual | INE padrón edad (`ine_v2_padron_prov_edad_nac`) | 2025 | C4 | 41 |
| jefatura_proxy_pct | prov_compra_anual | hogares (ECP 60133) / población 20+, %, **proxy** de tasa de jefatura | trimestral → anual (4 trim.) | INE ECP (`ine_v2_hogares_prov`) | 2024 (2021 en adelante) | C4 (proxy) | 41 (164 obs, 2021-2024) |
| paro_tasa | prov_compra_anual | parados / (ocupados + parados), % | trimestral → anual (4 trim.) | INE EPA (`ine_v2_epa_prov`) | 2025 | C1 | 41 |
| ln_ocupados_miles | prov_compra_anual | ocupados (miles), ln | trimestral → anual | INE EPA | 2025 | C1 | 41 |
| ln_pib_pc | prov_compra_anual | PIB a precios corrientes (€) / población, ln — **proxy de renta**; renta disponible provincial sin dato | anual | INE CRE tabla 80109 (`ine_v2_cre`) | 2024 | C4 (proxy) | 41 |
| ln_vut | prov_compra_anual, prov_alquiler_anual | viviendas turísticas (INE VTE, experimental), ln | 1-2 meses publicados/año → media | INE VTE 39364 | 2025 (2020-2025) | C4 (estadística experimental) | 41 (205 obs, 2020-2024) |
| ln_terminadas_libres | prov_compra_anual | viviendas libres terminadas, ln (suma 12 meses) | mensual → anual | MIVAU iniciadas/terminadas (sedal) | 2025 | C1 | 38 |
| ln_iniciadas_libres | prov_compra_anual | viviendas libres iniciadas, ln | anual | MIVAU | 2025 | C1 | 38 |
| bajas_tasa_C_amplia_pct | prov_compra_anual | bajas del parque, método C amplia, % del parque (T1) | anual | output/v5_1/T1 (C4 en T1) | 2025 | C4 | 41 |
| ln_suelo_pm2_m50k | prov_compra_anual | suelo €/m² (MIVAU, provincia, trimestral → anual con ≥4 trim.) | trimestral | MIVAU suelo (`mivau_v2_suelo`) | 2025 | C4 | 25 (147 obs) |
| ln_llegada_total_ext / ln_llegada_esp_ext / ln_llegada_ext_ext | prov_compra_anual | inmigración desde el extranjero (flujo bruto, no neto), total, españoles y extranjeros | semestral → suma anual | INE migraciones (`ine_v2_migraciones_prov`) | 2021 (último año en la fuente provincial) | C4 | 41 (287 obs, 2015-2021) |
| ln_alq_m2_serpavi_vc | prov_alquiler_anual | mediana alquiler €/m²/mes, VC | anual | MIVAU-SERPAVI (`pdf/serpavi_provincias`) | 2024 | C1 (SERPAVI) | 39 (344 obs, 2015-2023) |
| ln_alq_mes_serpavi_vc | prov_alquiler_anual | mediana alquiler €/mes, VC | anual | SERPAVI | 2024 | C1 | 39 |
| ln_n_contratos_serpavi_vc | prov_alquiler_anual | contratos declarados, nº, ln | anual | SERPAVI | 2024 | C1 | 39 |
| ln_ipc_alq_idx | prov_alquiler_anual, prov_trim_compra | IPC subclase alquiler de vivienda, índice (media mensual) | mensual → anual / trim. | INE IPC tabla 76142 | 2025 | C1 | 41 (369) / 38 trim. |
| d_ln_ipc_alq | prov_alquiler_anual | Δ ln del índice IPC alquiler (anual) | anual | derivada | 2025 | C1 | 41 (328) |
| ln_ratio_precio_alquiler | prov_alquiler_anual | ln(€/m² tasado) − ln(€/m²/mes SERPAVI) − ln 12 | anual | derivada | 2024 | C4 | 36 (317) |
| rentabilidad_bruta_pct | prov_alquiler_anual | 100·12·alquiler SERPAVI / precio tasado, % (rentabilidad bruta, sin gastos ni IBI) | anual | derivada | 2024 | C4 | 36 (317) |
| n_mun_tensionados / n_mun_topes_cat | prov_alquiler_anual | nº municipios con zona tensionada vigente / con tope en Cataluña (por año) | evento (BOE/CCAA) | `v3/zonas_tensionadas_v3`, `v3/cataluna_contencion_rentas_v3` | 2025 | C1 (BOE) | 39 (344) |
| ln_fianza_media_gva_eur | prov_contratos_nuevos_anual | media de importe de fianza (€, depósito), ln | contrato → media anual | GVA fianzas (`v5/gva_fianzas_20xx`) | 2024 | C4 (única fuente en CV) | 3 prov. (15 obs, 2020-2024) |
| ln_n_fianzas_gva | prov_contratos_nuevos_anual | fianzas registradas, nº, ln | anual | GVA | 2024 | C4 | 3 prov. |
| ln_n_fianzas_incasol / pct_fianzas_600_incasol | prov_contratos_nuevos_anual | Incasòl: nº contratos (banda total) y % en banda >600 €/mes | anual | Incasòl (`v3/incasol_fianzas_municipio_v3`) | 2024 | C4 | 4 prov. (40 / 16 obs) |
| ln_ipva_nuevo_idx | prov_contratos_nuevos_anual | IPVA nuevo contrato, índice provincial | anual | INE IPVA (`ine_v2_ipva`, «Nuevo contrato») | 2024 | C4 | 38 (152 obs, 2021-2024) |
| ln_pm2_tasado_mun | mun_compra_anual / mun_alquiler_anual / mun_contratos_anual | valor tasado municipal, €/m², ln (municipios >25.000 con nombre único) | trimestral → anual (4 trim.) | MIVAU valor tasado municipios | 2025 | C4 | 200 mun. (1.909 obs, 2015-2024) |
| ln_alq_m2_serpavi_mun | mun_compra_anual / mun_alquiler_anual / mun_contratos_anual | mediana alquiler €/m²/mes VC, municipal | anual | SERPAVI municipal (`pdf/serpavi_v2_municipios`) | 2024 | C1 | 2.021 mun. (16.633 obs) |
| ln_n_fianzas_gva_mun / ln_fianza_media_gva_mun_eur | mun_compra_anual / mun_alquiler_anual / mun_contratos_anual | fianzas GVA municipal (nº y media €) | anual | GVA | 2024 | C4 | 281 / 272 mun. |
| ln_n_fianzas_incasol_mun / pct_fianzas_600_incasol_mun | mun_compra_anual / mun_alquiler_anual / mun_contratos_anual | Incasòl municipal | anual | Incasòl | 2024 | C4 | 943 / 623 mun. |
| tensionada_mun / tope_cat_mun | mun_compra_anual / mun_alquiler_anual / mun_contratos_anual | indicador 0/1 vigente en el año | evento | BOE / CCAA | 2025 | C1 | 2.470 mun. (todas las filas) |
| ln_alq_m2_serpavi_dis | dis_alquiler_anual | punto medio p25-p75 €/m²/mes VC, distrito (v3; **no hay mediana**) | anual | SERPAVI distritos v3 (`v3/serpavi_distritos_nacional_v3`) | 2023 (sellado 2024) | C4 | 2.501 dist. (27.578 obs, 2011-2023) |
| ln_vut_plazas_dis | dis_alquiler_anual | plazas VUT por distrito, ln, media de meses publicados | 1-2 meses/año | INE VUT sección v3 (`v3/ine_v3_vut_seccion`) | 2023 | C4 (experimental) | 4.950 dist. (13.523 obs, 2021-2023) |

Descriptivas, sin sellado (no son paneles de modelización; si se usan en M1/M2 deben sellarse en el tiempo antes):
`nacional_trim_desc.csv` (tipo hipotecario ECB, crédito vivienda BdE stock y nuevas operaciones, crédito a promotores
(BdE via v5/CA), HICP y tasa de inflación interanual, coste de construcción Eurostat, valor tasado nacional, IPC alquiler
nacional, IPV INE nacional, paro nacional, compraventas y hipotecas sumadas por provincias, 2005-2025);
`nacional_anual_a23_desc.csv` (índice triangulado A23 con banda min/max, y medias por fuente 2015-2025);
`ccaa_ipv_anual_desc.csv` (IPV INE CCAA, media anual, 2015-2025);
`ccaa_seguridad_juridica_transversal_desc.csv` (CB, corte transversal sin año: usurpaciones, verbales posesorios, % alquiler censo).
Estáticas: `prov_estatico.csv` (costa, isla, costa_sol de R1A; distancia mediana al municipio de mayor población; % no
principal Censo 2021); `mun_estatico.csv` (distancia al municipio de mayor población de su provincia, km, centroides v5).
La distancia es un **proxy** del centro, no la capital; el efecto donut se estima en M1/M2.

## 3. Sin dato o sin cobertura suficiente (no incluido en paneles)

| Variable pedida | Motivo |
|---|---|
| Llegada NETA por origen (provincial) | Sin emigración provincial en data/raw; solo flujo bruto (ver arriba). |
| Jóvenes en casa de los padres (provincial) | Sin fuente provincial; solo EFF/ECV (nacional o CCAA). Se usa `share_20_34` como proxy de demanda, no como esa variable. |
| Renta disponible provincial | Sin fuente en data/raw; `ln_pib_pc` como proxy. |
| Coste de construcción provincial o municipal | Eurostat solo nacional (`eurostat_costes`); en `nacional_trim_desc.csv`. |
| Tipo hipotecario provincial | Solo nacional (ECB, BdE). |
| Crédito hipotecario y a promotores provincial | Solo nacional y CCAA (BdE). |
| Notariado (precio y volumen) | Solo Comunitat Valenciana (`pdf/notariado_cv_prov_trimestral`, 2018-2025); sin panel M0 para no sesgar la muestra a 3 provincias. |
| VUT municipal (INE VTE, municipio) | Columna vacía tras el cruce (`ln_vut_viviendas_mun`): se elimina del train; revisar codificación. |
| Precio por provincia (uniprovinciales) | RESUELTO (B3): las CCAA uniprovinciales (07, 26, 28, 30, 31, 33, 39) y Ceuta/Melilla (51, 52) toman la serie CCAA; marcado «CCAA = provincia (uniprovincial)», no es interpolación. Navarra tiene dos rótulos: se usa el de serie más completa. |
| Municipios con valor tasado | 277 municipios emparejados por nombre único (de ~700 en A4); el resto, sin código fiable. |
| Seguridad jurídica provincial | Solo CCAA (CB); en `ccaa_seguridad_juridica_transversal_desc.csv`. |
| Costa, islas, distancia | Estáticas; fuera del panel (ver arriba). |
| IPV INE provincial | Solo CCAA y nacional (`ine_ipv_80270`). |
| Coste de uso completo | Sin IBI ni depreciación en data/raw; el componente disponible es el tipo hipotecario real (tipo ECB − inflación interanual), en `nacional_trim_desc.csv`. |

## 4. Principales limitaciones de cobertura

- Los paneles de compra y alquiler (52 provincias) tienen 38-41 provincias en entrenamiento según la fuente; el sellado
  de v6 quita 11 provincias (ver `sellado.md`).
- SERPAVI: 48 provincias con dato VC en 2011-2020 y 52 en 2024; la cobertura de años en train depende del sellado.
- Los distritos SERPAVI (v3) solo cubren algunos municipios grandes (2.501 distritos con dato en train).
- La validación sellada v6 es nueva, pero las provincias y los distritos se usaron de forma descriptiva en v4-v5
  (decisiones.md). Se dirá en todos los resultados.

## 5. Cambios de la revisión (docs/v6/revision_M0.md)

- B1: el trimestral usa el mismo corte que el anual de compra (2025T1 en adelante sellado).
- B2: los paneles municipales se separan por medida (compra 2025, alquiler 2024, contratos 2024); el corte es el mismo en todos los niveles.
- B3: uniprovinciales resueltos desde la serie CCAA; todas las provincias selladas tienen precio.
- N1: etiqueta de provincia fija desde `territorio` (ETDP); gzip con `mtime=0`; md5 idénticos en dos ejecuciones.
- N2: `sellado_info.json` guarda el sha256 de cada `data/sealed/v6_*.csv`, sin leer su contenido. Integrar `m0_run.py` en `make all` y el check del sha256 en `check_v6.py` queda pendiente (Makefile y check_v6 no están en las rutas de M0).
- N3: agregados nacionales que suman desenlaces provinciales excluidos de modelos (ver hipotesis.md §3). IPV CCAA también como tasa (`ipv_tasa_anual_pct`).
- N4: p25 y p75 del distrito en el panel.
- N6: la caché de sellado se verifica también con distritos sellados en v3 (rama None).
- N8: potencia con sd within, K = regresores preregistrados + 1, clústeres reales (8-11 CCAA).
- Municipal: `mun_compra_anual` incluye todos los municipios con valor tasado por nombre único; el resto de municipios de SERPAVI o fianzas no tienen precio.
