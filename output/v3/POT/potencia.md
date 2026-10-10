# Potencia de P-C (EMD vs EER)

EMD = max(EMD analítico con t(G-1), EMD calibrado por wild cluster bootstrap Rademacher), potencia 0,80 y alfa 0,05 bilateral, EE clúster de datos reales tras efectos fijos (500 réplicas, SEED=20261010). Veredicto «estimable» solo si EMD <= EER y G >= 20; con G < 20 es «no concluyente (G<20)». Sellado v3 (distritos, municipios con >=50 % de distritos sellados y 2026M05) excluido antes de calcular. NO se publican coeficientes (versión anterior de este fichero publicó coeficientes de P-C1 y P-C3 por error; retirados por la revisión de la oleada 1, O1). Capa: C4 (potencia, no estimación de efectos).

| diseno   | especificacion                                                              |     N |   clusters |       ee |    emd_t |   emd_wcb |      emd |   eer |   potencia_wcb_en_emd |   F_1a_etapa | veredicto                               |
|:---------|:----------------------------------------------------------------------------|------:|-----------:|---------:|---------:|----------:|---------:|------:|----------------------:|-------------:|:----------------------------------------|
| P-C1     | OLS FE sección+año, nacional                                                | 70628 |       2888 |   0.0007 |   0.002  |    0.0018 |   0.002  |  0.01 |                 0.8   |     nan      | estimable                               |
| P-C1     | OLS FE, 6 ciudades grandes (pool)                                           | 14768 |         56 |   0.0022 |   0.0063 |    0.0055 |   0.0063 |  0.01 |                 0.8   |     nan      | estimable                               |
| P-C1     | OLS FE, Barcelona                                                           |  3260 |          8 |   0.0015 |   0.005  |    0.0071 |   0.0071 |  0.01 |                 0.8   |     nan      | no concluyente (G<20)                   |
| P-C1     | OLS FE, Madrid                                                              |  7160 |         16 |   0.0023 |   0.0068 |    0.0041 |   0.0068 |  0.01 |                 0.8   |     nan      | no concluyente (G<20)                   |
| P-C1     | OLS FE, València                                                            |  1940 |         15 |   0.0023 |   0.0069 |    0.0085 |   0.0085 |  0.01 |                 0.8   |     nan      | no concluyente (G<20)                   |
| P-C1     | OLS FE, Sevilla                                                             |  1408 |          8 |   0.0008 |   0.0025 |    0.0044 |   0.0044 |  0.01 |                 0.804 |     nan      | no concluyente (G<20)                   |
| P-C1     | OLS FE, Málaga                                                              |   916 |          8 |   0.0023 |   0.0076 |    0.0049 |   0.0076 |  0.01 |                 0.806 |     nan      | no concluyente (G<20)                   |
| P-C1     | shift-share LOO municipio, nacional                                         | 68092 |       2254 |   0.0443 |   0.1241 |    0.0767 |   0.1241 |  0.01 |                 0.8   |       0.2526 | no detectable con los datos disponibles |
| P-C1     | shift-share LOO municipio, 6 ciudades                                       | 14768 |         56 |   0.0029 |   0.0082 |    0.0075 |   0.0082 |  0.01 |                 0.8   |      23.7234 | estimable                               |
| P-C1     | shift-share LOO provincia, nacional                                         | 70628 |       2888 |   0.0085 |   0.0237 |    0.0217 |   0.0237 |  0.01 |                 0.8   |       5.3186 | no detectable con los datos disponibles |
| P-C1     | shift-share LOO provincia, 6 ciudades                                       | 14768 |         56 |   0.0032 |   0.0092 |    0.0089 |   0.0092 |  0.01 |                 0.8   |      29.3511 | estimable                               |
| P-C2     | caída de anuncios 2025-2026 -> alquiler fino                                |     0 |          0 | inf      | inf      |  inf      | inf      |  0.1  |               nan     |     nan      | no detectable con los datos disponibles |
| P-C3     | topes Ley 11/2020, ventana 2020T4-2022T1 (2016-2022) -> alquiler            |  2548 |        364 |   0.0068 |   0.019  |    0.0203 |   0.0203 |  0.03 |                 0.8   |     nan      | estimable                               |
| P-C3     | topes Ley 11/2020, ventana 2020T4-2022T1 (2016-2022) -> contratos           |  2548 |        364 |   0.0237 |   0.0666 |    0.0662 |   0.0666 |  0.1  |                 0.8   |     nan      | estimable                               |
| P-C3     | topes Ley 11/2020, ventana sensibilidad fin 2021T3 (2016-2022) -> alquiler  |  2548 |        364 |   0.0084 |   0.0237 |    0.0254 |   0.0254 |  0.03 |                 0.8   |     nan      | estimable                               |
| P-C3     | topes Ley 11/2020, ventana sensibilidad fin 2021T3 (2016-2022) -> contratos |  2548 |        364 |   0.0291 |   0.0816 |    0.0826 |   0.0826 |  0.1  |                 0.8   |     nan      | estimable                               |
| P-C3     | zonas tensionadas (2016-2025) -> alquiler                                   |  3510 |        351 |   0.0093 |   0.0261 |    0.0266 |   0.0266 |  0.03 |                 0.8   |     nan      | estimable                               |
| P-C3     | zonas tensionadas (2016-2025) -> contratos                                  |  3510 |        351 |   0.0319 |   0.0895 |    0.0834 |   0.0895 |  0.1  |                 0.8   |     nan      | estimable                               |
| P-C4     | d_ln_ocupados x ln p_suelo                                                  |  1134 |         50 |   0.0549 |   0.1571 |    0.1581 |   0.1581 |  0.1  |                 0.8   |     nan      | no detectable con los datos disponibles |
| P-C4     | d_ln_pob_total x ln p_suelo                                                 |  1134 |         50 |   0.239  |   0.6832 |    0.7645 |   0.7645 |  0.1  |                 0.8   |     nan      | no detectable con los datos disponibles |

## Notas por fila

- P-C1 / OLS FE sección+año, nacional: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=0.574
- P-C1 / OLS FE, 6 ciudades grandes (pool): log-puntos de alquiler por 1 pp VUT/viviendas. cluster distritosd residual VUT tras FE=0.693
- P-C1 / OLS FE, Barcelona: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=0.445
- P-C1 / OLS FE, Madrid: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=0.318
- P-C1 / OLS FE, València: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=0.485
- P-C1 / OLS FE, Sevilla: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=0.782
- P-C1 / OLS FE, Málaga: log-puntos de alquiler por 1 pp VUT/viviendas. sd residual VUT tras FE=2.053
- P-C1 / shift-share LOO municipio, nacional: log-puntos por 1 pp VUT (2SLS). sd z tras FE=2.024
- P-C1 / shift-share LOO municipio, 6 ciudades: log-puntos por 1 pp VUT (2SLS). sd z tras FE=0.845
- P-C1 / shift-share LOO provincia, nacional: log-puntos por 1 pp VUT (2SLS). sd z tras FE=0.590
- P-C1 / shift-share LOO provincia, 6 ciudades: log-puntos por 1 pp VUT (2SLS). sd z tras FE=0.438
- P-C2 / caída de anuncios 2025-2026 -> alquiler fino: log-puntos de alquiler por 1 de caída log de anuncios. Resultado de alquiler a escala fina posterior a 2025: NO. {"serpavi_distrito_max_anio": 2024, "incasol_max_anio_nivel_municipal": 2026, "madrid_cp_periodos": ["2023", "2024"], "insideairbnb_rango": ["2025-12-14", "2026-09-28"]}. Incasòl llega a 2026 pero solo a escala municipal y las capturas Inside Airbnb empiezan en 2025-12 (sin periodo previo).
- P-C3 / topes Ley 11/2020, ventana 2020T4-2022T1 (2016-2022) -> alquiler: log-puntos (EMD sobre el coef de D). tratados = 61 municipios de la Ley 11/2020 (lista oficial); tratados=49, controles=315; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / topes Ley 11/2020, ventana 2020T4-2022T1 (2016-2022) -> contratos: log-puntos (EMD sobre el coef de D). tratados = 61 municipios de la Ley 11/2020 (lista oficial); tratados=49, controles=315; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / topes Ley 11/2020, ventana sensibilidad fin 2021T3 (2016-2022) -> alquiler: log-puntos (EMD sobre el coef de D). tratados = 61 municipios de la Ley 11/2020 (lista oficial); tratados=49, controles=315; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / topes Ley 11/2020, ventana sensibilidad fin 2021T3 (2016-2022) -> contratos: log-puntos (EMD sobre el coef de D). tratados = 61 municipios de la Ley 11/2020 (lista oficial); tratados=49, controles=315; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / zonas tensionadas (2016-2025) -> alquiler: log-puntos (EMD sobre el coef de D). tratamiento = fracción del año con zona declarada (códigos corregidos); tratados=222, controles=129; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / zonas tensionadas (2016-2025) -> contratos: log-puntos (EMD sobre el coef de D). tratamiento = fracción del año con zona declarada (códigos corregidos); tratados=222, controles=129; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C4 / d_ln_ocupados x ln p_suelo: diferencia de elasticidad p75-p25 de ln(p_suelo). IQR ln p_suelo=0.66; p_suelo = media provincial (invariante)
- P-C4 / d_ln_pob_total x ln p_suelo: diferencia de elasticidad p75-p25 de ln(p_suelo). IQR ln p_suelo=0.66; p_suelo = media provincial (invariante)

Pérdidas de armonización P-C1 (secciones): {"unidades_alq_sin_vut_o_censo": 13, "unidades_no_balanceadas_o_sin_alq": 2766, "unidades_finales": 17657}

Advertencia P-C1: SERPAVI es stock IRPF y amortigua el alquiler; si el efecto sobre el stock es una fracción k del efecto sobre contratos nuevos, el EMD relevante es EMD/k (peor). VUT INE cubre ~89-90 % (error de medida, sesgo a 0).