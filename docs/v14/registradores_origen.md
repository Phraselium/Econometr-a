# V14.3 · Origen de las cifras y tablas de Registradores: datos abiertos (ODbL) o Anuario ERI

Generado por `python3 src/v14/registradores_origen.py`. Lista completa: [registradores_origen.csv](registradores_origen.csv) (tipo, id o fichero, dependencia, origen, fichero, evidencia, regla). Licencias por fichero: [licencias_tablas.csv](licencias_tablas.csv).

- **ODbL**: conjunto abierto «Compraventas de inmuebles, uso residencial, por provincia», bajo la Open Database License 1.0. Con terceros_1_0.registradores_odbl = «agregados» sus cifras se publican con el aviso de la ODbL y la serie no se redistribuye.
- **ERI**: Anuario de la Estadística Registral Inmobiliaria (derechos reservados). Con terceros_1_0.registradores_eri = «excluir» sus cifras (y las «ambos») se retiran de publicacion/, web/ y consulta/; siguen en cifras_clave sin cambios.

## Cifras

| Dependencia | ODbL | ERI | ambos |
|---|---|---|---|
| directa | 51 | 1 | 4 |
| indirecta (el modelo usa la serie) | 35 | 0 | 0 |
| técnica (panel con terceros; el modelo no usa la serie) | 151 | 0 | 0 |

Cifras con origen ERI o ambos (las que usan la serie y se retiran con registradores_eri = «excluir»):

| id | origen | dependencia | fichero | regla |
|---|---|---|---|---|
| A23-P5 | ERI | directa | output/v5/A23/hechos.json | 2: fuentes o enunciado |
| CA-CT-ratio-triang-2022 | ambos | directa | output/v5/CA/hechos.json | 1: compraventas del CSV de datos abiertos e hipotecas tecleadas del Anuario ERI (REGISTRADORES_HIP, src/v5/ca_run.py) |
| CA-CT-ratio-triang-2023 | ambos | directa | output/v5/CA/hechos.json | 1: compraventas del CSV de datos abiertos e hipotecas tecleadas del Anuario ERI (REGISTRADORES_HIP, src/v5/ca_run.py) |
| CA-CT-ratio-triang-2024 | ambos | directa | output/v5/CA/hechos.json | 1: compraventas del CSV de datos abiertos e hipotecas tecleadas del Anuario ERI (REGISTRADORES_HIP, src/v5/ca_run.py) |
| CA-CT-ratio-triang-2025 | ambos | directa | output/v5/CA/hechos.json | 1: compraventas del CSV de datos abiertos e hipotecas tecleadas del Anuario ERI (REGISTRADORES_HIP, src/v5/ca_run.py) |

Cifras con origen ODbL que usan la serie (se publican con el aviso):

A23-P10, A23-P2, A23-P4, A23-P6, A23-P8, A23-P9, B3-H-B3-6-b-control, B3-H-B3-6-p-control, B3-mv-H-B3-1, B3-mv-H-B3-2, B3-mv-H-B3-6, B3-shap-orden, B3-shap-spearman, B4-b3-shapley-demografica, B4-b3-shapley-financiacion_tipos, B4-b3-shapley-oferta_suelo, B4-b3-shapley-renta_empleo, B4-b3-shapley-residuo, B4-b3-shapley-turismo_no_residentes, E-B3-H-B3-1-ic, E-B3-H-B3-1-p3, E-B3-H-B3-1-pri, E-B3-H-B3-2-ic, E-B3-H-B3-2-p3, E-B3-H-B3-2-pri, E-B3-H-B3-6-ic, E-B3-H-B3-6-p3, E-B3-H-B3-6-p8, E-B3-H-B3-6-pri, E-B3-N, E-B3-R2reg, E-B3-kendall, E-B3-rmse, K1-BASE-PROV_PRECIO_ANUAL_REGISTRADORES, K1-RATIO-PROV_PRECIO_ANUAL_REGISTRADORES, K1-RMSE-PROV_PRECIO_ANUAL_REGISTRADORES, K3-RATIO-2015, K3-RATIO-2023, V6-M4-PERS-PROV_PRECIO_ANUAL_REGISTRADORES, V6-M4-RMSE-MUN_PRECIO_ANUAL, V6-M4-RMSE-PROV_PRECIO_ANUAL, V6-M4-RMSE-PROV_PRECIO_ANUAL_REGISTRADORES, V6-M4-RMSE-PROV_PRECIO_TRIM, V6-M4-RMSE-PROV_VOL_ANUAL, V6-M4-RMSE-PROV_VOL_TRIM, V8-M8-cv-p03-P5-acum-alt, V8-M8-cv-p12-P5-acum-alt, V8-M8-cv-p46-P5-acum-alt, m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_ADL, m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_AR, m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_mejor_ML, K2-CUOTA-ALQ-NUCLEO-EXT, K2-CUOTA-ALQ-NUCLEO-SIN, K2-CUOTA-ALQ-SINPOB-EXT, K2-CUOTA-ALQ-SINPOB-SIN, K2-CUOTA-COMPRA-EXT, K2-CUOTA-COMPRA-SIN, K2-CUOTA-COMPRA-SINPOB-EXT, K2-CUOTA-COMPRA-SINPOB-SIN, m2_pip_alq_ln_iniciadas_libres, m2_pip_alq_ln_pib_pc, m2_pip_alq_ln_pob, m2_pip_alq_ln_terminadas_libres, m2_pip_alq_ln_vut, m2_pip_alq_n_mun_topes_cat, m2_pip_alq_share_ext_pob, m2_pip_cp_ln_hip_viv_num, m2_pip_cp_ln_iniciadas_libres, m2_pip_cp_ln_ocupados_miles, m2_pip_cp_ln_pib_pc, m2_pip_cp_ln_pob, m2_pip_cp_ln_suelo_pm2_m50k, m2_pip_cp_ln_terminadas_libres, m2_pip_cp_ln_vut, m2_pip_cp_paro_tasa, m2_pip_cp_share_ext_pob, m2_pip_cv_ln_hip_viv_num, m2_pip_cv_ln_iniciadas_libres, m2_pip_cv_ln_ocupados_miles, m2_pip_cv_ln_pib_pc, m2_pip_cv_ln_pob, m2_pip_cv_ln_suelo_pm2_m50k, m2_pip_cv_ln_terminadas_libres, m2_pip_cv_ln_vut, m2_pip_cv_paro_tasa, m2_pip_cv_share_ext_pob

## Tablas y ficheros

| Fichero | Origen | Árbol / paquete | Columnas o claves |
|---|---|---|---|
| data/base/cifras_clave.parquet | ambos | árbol: no entra; paquete: no entra | H-B3-6 con el precio inicial de Registradores; Hipotecas por 100 compraventas: INE 65.3 frente a Registradores 65.8; Hip |
| data/base/publica/cifras_clave.parquet | ambos | árbol: no entra; paquete: revisado: registro de cifras: enunciados que nombran la fuente; sin series | H-B3-6 con el precio inicial de Registradores; Hipotecas por 100 compraventas: INE 65.3 frente a Registradores 65.8; Hip |
| data/base/variables.parquet | ambos | árbol: no entra; paquete: no entra | registr_num_4tm; registr_pm2_4tm; registradores_compraventas_anual; registradores_extranj_pct |
| data/processed/nacional_q.csv | ambos | árbol: no entra; paquete: no entra | d4_ln_registradores_compraventas_anual; d_ln_registradores_compraventas_anual; d_registradores_extranj_pct; ln_registrad |
| data/processed/panel_ccaa_a.csv | ambos | árbol: no entra; paquete: no entra | d_registradores_extranj_pct; registradores_extranj_pct |
| data/processed/v2/train/nacional_q_v2.csv | ambos | árbol: no entra; paquete: no entra | d4_ln_registradores_compraventas_anual; d_ln_registradores_compraventas_anual; d_registradores_extranj_pct; ln_registrad |
| data/processed/v8/cv_prov_q_v8.csv | ODbL | árbol: no entra; paquete: no entra | registr_num_4tm; registr_pm2_4tm |
| data/processed/v8/nacional_q_v8.csv | ODbL | árbol: no entra; paquete: no entra | d4_ln_registr_pm2_4tm; d4_ln_registr_pm2_4tm_real; d_ln_registr_pm2_4tm; d_ln_registr_pm2_4tm_real; ln_registr_pm2_4tm;  |
| output/f3/panel_construido_x_z.csv | ERI | árbol: redactado; paquete: redactado | d_registradores_extranj_pct; registradores_extranj_pct |
| output/v3/PA/tablas/A4_provincias.csv | ODbL | árbol: redactado; paquete: redactado | cuota_mes_registradores; cuota_pct_renta_registradores; precio_m2_registradores; precio_registradores_80m2; precio_renta |
| output/v4/M4/hechos.json | ERI | árbol: revisado: cifras nacionales publicadas por la fuente, citadas (un valor por año), y cálculos propios; paquete: revisado: cifras nacionales publicadas por la fuente, citadas (un valor por año), y cálculos propios | extranjeros_nacional.registradores_pct_publicado |
| output/v4/M4/resultado.json | ambos | árbol: revisado: ídem, y diagnósticos propios (correlación, diferencia media, cobertura); paquete: revisado: ídem, y diagnósticos propios (correlación, diferencia media, cobertura) | diagnosticos.cobertura_registradores_ccaa_min; diagnosticos.corr_prov_mivau_registradores_2023_25; diagnosticos.dif_medi |
| output/v4/M4/tablas/extranjeros_evolucion_nacional.csv | ERI | árbol: redactado; paquete: redactado | registradores_cobertura_ccaa; registradores_pct_ext_derivado_ccaa; registradores_pct_ext_publicado |
| output/v4/M4/tablas/extranjeros_provincias_2023_2025.csv | ERI | árbol: redactado; paquete: redactado | registradores_ext_n_2023_25; registradores_pct_ext_ponderado_2023_25 |
| output/v4/M7/hechos.json | ODbL | árbol: revisado: variaciones acumuladas y anuales calculadas: resultado propio; paquete: revisado: variaciones acumuladas y anuales calculadas: resultado propio | precio_2015_2025.ann.Registradores; precio_2015_2025.cum.Registradores; precio_2021_2025.ann.Registradores; precio_2021_ |
| output/v4/M7/tablas/precio_nacional_idx2015.csv | ODbL | árbol: redactado; paquete: redactado | Registradores |
| output/v4/M7/tablas/variacion_precio.csv | ODbL | árbol: redactado; paquete: redactado | var_Registradores_pct |
| output/v5/A23/calculos.json | ODbL | árbol: revisado: variaciones y factores calculados: resultado propio; paquete: revisado: variaciones y factores calculados: resultado propio | precio.cum_publicado.Registradores; precio.factor.cargas.Registradores; precio.mix_provincial_registradores |
| output/v5/A23/resultado.json | ODbL | árbol: revisado: ídem; paquete: revisado: ídem | N.provincias_registradores; estimacion.precio.registradores_pesos_provincia_pct; estimacion.precio.variacion_superficie_ |
| output/v5/A23/tablas/idx_precio_publicado_2015.csv | ODbL | árbol: redactado; paquete: redactado | Registradores |
| output/v5/A23/tablas/precio_m2_nivel.csv | ODbL | árbol: redactado; paquete: redactado | pm2_registradores_pesos_CCAA2015; pm2_registradores_publicado |
| output/v5/A23/tablas/tamano_implicito_registradores.csv | ODbL | árbol: redactado; paquete: redactado | nombre del fichero; columna pm2 (serie de registradores; escaneo por valores); c |
| output/v5/B3/_smoke/tablas/shapley_R2.csv | ODbL | árbol: revisado: ídem (ejecución de prueba); paquete: revisado: ídem (ejecución de prueba) | registradores |
| output/v5/B3/resultado.json | ODbL | árbol: revisado: R² de Shapley: resultado propio; paquete: revisado: R² de Shapley: resultado propio | diagnosticos.shapley.R2_registradores |
| output/v5/B3/tablas/resumen_interno.json | ODbL | árbol: revisado: contraste de hipótesis: resultado propio; paquete: revisado: contraste de hipótesis: resultado propio | hip.H-B3-6.control_error_medida_F6_precio_registradores |
| output/v5/B3/tablas/shapley_R2.csv | ODbL | árbol: revisado: cuota de R² (REVISADAS_SIN_SERIES); paquete: revisado: cuota de R² (REVISADAS_SIN_SERIES) | registradores |
| output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv | ambos | árbol: redactado; paquete: redactado | reg_compraventas_viv; reg_hipotecas_viv |
| output/v6/M0/cobertura_train.json | ODbL | árbol: revisado: recuento de cobertura (n, unidades, años); sin valores; paquete: revisado: recuento de cobertura (n, unidades, años); sin valores | prov_compra_anual.ln_cv_registradores; prov_compra_anual.ln_pm2_registradores |
| output/v6/M0/paneles/nacional_anual_a23_desc.csv | ODbL | árbol: redactado; paquete: redactado | pm2_registradores_pesos_CCAA2015; pm2_registradores_publicado |
| output/v6/M0/paneles/prov_compra_anual_train.csv.gz | ODbL | árbol: redactado; paquete: redactado | ln_cv_registradores; ln_pm2_registradores |
| output/v6/M1B/tablas/b1_provincias_ultimo_anio.csv | ODbL | árbol: redactado; paquete: redactado | ratio_anios_registradores |
| output/v6/M1B/tablas/b1_ratio_coste_uso_provincia_anio.csv | ODbL | árbol: redactado; paquete: redactado | ln_pm2_registradores; ratio_anios_registradores |
| output/v6/M1B/tablas/ratio_d.csv | ODbL | árbol: redactado; paquete: redactado | ln_pm2_registradores; ratio_anios_registradores |
| output/v6/M1B/tablas/ratio_ult.csv | ODbL | árbol: redactado; paquete: redactado | ln_pm2_registradores; ratio_anios_registradores |
| output/v6/M3B/resultado.json | ODbL | árbol: revisado: métricas de predicción y SHAP de un modelo con el precio de Registradores: resultado propio; paquete: revisado: métricas de predicción y SHAP de un modelo con el precio de Registradores: resultado propio | N.PROV_PRECIO_ANUAL_REGISTRADORES; diagnosticos.PROV_PRECIO_ANUAL_REGISTRADORES; estimacion.PROV_PRECIO_ANUAL_REGISTRADO |
| output/v6/M3B/tablas/interpretacion_resumen.json | ODbL | árbol: revisado: ídem; paquete: revisado: ídem | PROV_PRECIO_ANUAL_REGISTRADORES |
| output/v6/M3B/tablas/resumen_por_setting.json | ODbL | árbol: revisado: ídem; paquete: revisado: ídem | PROV_PRECIO_ANUAL_REGISTRADORES |
| output/v6_1/K4B/calculos.json | ODbL | árbol: revisado: ídem; paquete: revisado: ídem | A23-P2.registradores |
| output/v8/F1/resultado.json | ODbL | árbol: revisado: correlación de tasas: resultado propio; paquete: revisado: correlación de tasas: resultado propio | diagnosticos.coincidencias.registr_pm2_4tm/p_bde |
| revision_externa/hoja_revision.xlsx | ODbL | árbol: revisado: enunciados publicados que nombran la fuente; sin series; paquete: revisado: enunciados publicados que nombran la fuente; sin series | hoja fuentes: cabecera Registradores; hoja revision: cabecera MIVAU valor tasado |
| output/v6/M3B/figuras/interpretacion_PROV_PRECIO_ANUAL_REGISTRADORES.png | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/modelos/PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano.joblib | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/ale_PROV_PRECIO_ANUAL_REGISTRADORES_ln_suelo_pm2_m50k_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/ale_PROV_PRECIO_ANUAL_REGISTRADORES_ln_terminadas_libres_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/ale_PROV_PRECIO_ANUAL_REGISTRADORES_ln_vut_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/pdp_PROV_PRECIO_ANUAL_REGISTRADORES_ln_suelo_pm2_m50k_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/pdp_PROV_PRECIO_ANUAL_REGISTRADORES_ln_terminadas_libres_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/pdp_PROV_PRECIO_ANUAL_REGISTRADORES_ln_vut_l1.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/permutacion_agrupada_PROV_PRECIO_ANUAL_REGISTRADORES.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/shap_por_provincia_PROV_PRECIO_ANUAL_REGISTRADORES.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M3B/tablas/vif_PROV_PRECIO_ANUAL_REGISTRADORES.csv | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M4/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ar_unidad.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M4/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M4/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ecm_v1.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M4/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__m1_econ.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6/M4/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__persistencia.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ar_factor_fac.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ar_factor_ora.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__twfe_fac.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__twfe_ora.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ult_crec_nac_fac.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v6_1/K1/sellado_PROV_PRECIO_ANUAL_REGISTRADORES__ult_crec_nac_ora.json | ODbL | árbol y paquete: sí (resultado propio) | modelo con ln_pm2_registradores (datos abiertos) |
| output/v5/A23/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v5/B3/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v5/B4/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v5/E/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6/M2/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6/M3B/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6/M4/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6_1/K1/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6_1/K2/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v6_1/K3/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |
| output/v8/F6/hechos.json | ODbL | árbol y paquete: sí (origen de cifras ODbL) | fichero de origen de cifras con origen ODbL |

## Licencia ODbL en el árbol y el paquete (65 ficheros)

Cada fichero de [licencias_tablas.csv](licencias_tablas.csv) que contiene variables o cifras construidas desde los datos abiertos se publica, en esa parte, bajo la ODbL 1.0 (4.4, «share alike»), con este aviso (4.2 y 4.3):

> Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/.

