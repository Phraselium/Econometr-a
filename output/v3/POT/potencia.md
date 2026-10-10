# Potencia de P-C (EMD vs EER)

EMD = (z_0,975 + z_0,80) x EE clúster = 2,8016 x EE; EE de datos reales tras efectos fijos; potencia verificada por bootstrap de clústeres con residuos reales (500 réplicas, SEED=20261010) añadiendo un efecto igual al EMD (columna potencia_sim_en_emd, objetivo ≈ 0,80). Sellado v3 (distritos y 2026M05) excluido antes de calcular. Capa: C4 (potencia, no estimación de efectos).

| diseno   | especificacion                               |     N |   clusters |      emd |   eer |   potencia_sim_en_emd |   F_1a_etapa | veredicto                               |
|:---------|:---------------------------------------------|------:|-----------:|---------:|------:|----------------------:|-------------:|:----------------------------------------|
| P-C1     | OLS FE sección+año, nacional                 | 70628 |       2888 |   0.002  |  0.01 |                 0.968 |     nan      | estimable                               |
| P-C1     | OLS FE, 6 ciudades grandes (pool)            | 14768 |         56 |   0.0062 |  0.01 |                 0.988 |     nan      | estimable                               |
| P-C1     | OLS FE, Barcelona                            |  3260 |          8 |   0.0043 |  0.01 |                 0.736 |     nan      | estimable                               |
| P-C1     | OLS FE, Madrid                               |  7160 |         16 |   0.0063 |  0.01 |                 1     |     nan      | estimable                               |
| P-C1     | OLS FE, València                             |  1940 |         15 |   0.0064 |  0.01 |                 0.646 |     nan      | estimable                               |
| P-C1     | OLS FE, Sevilla                              |  1408 |          8 |   0.0021 |  0.01 |                 0.532 |     nan      | estimable                               |
| P-C1     | OLS FE, Málaga                               |   916 |          8 |   0.0065 |  0.01 |                 0.7   |     nan      | estimable                               |
| P-C1     | shift-share LOO municipio, nacional          | 68092 |       2254 |   0.124  |  0.01 |                 0.686 |       0.2526 | no detectable con los datos disponibles |
| P-C1     | shift-share LOO municipio, 6 ciudades        | 14768 |         56 |   0.008  |  0.01 |                 0.906 |      23.7234 | estimable                               |
| P-C1     | shift-share LOO provincia, nacional          | 70628 |       2888 |   0.0237 |  0.01 |                 0.778 |       5.3186 | no detectable con los datos disponibles |
| P-C1     | shift-share LOO provincia, 6 ciudades        | 14768 |         56 |   0.009  |  0.01 |                 0.884 |      29.3511 | estimable                               |
| P-C2     | caída de anuncios 2025-2026 -> alquiler fino |     0 |          0 | inf      |  0.1  |               nan     |     nan      | no detectable con los datos disponibles |
| P-C3     | topes Ley 11/2020 (2016-2022) -> alquiler    |  3171 |        453 |   0.0178 |  0.03 |                 0.822 |     nan      | estimable                               |
| P-C3     | topes Ley 11/2020 (2016-2022) -> contratos   |  3171 |        453 |   0.054  |  0.1  |                 0.786 |     nan      | estimable                               |
| P-C3     | zonas tensionadas (2016-2025) -> alquiler    |  4380 |        438 |   0.0229 |  0.03 |                 0.816 |     nan      | estimable                               |
| P-C3     | zonas tensionadas (2016-2025) -> contratos   |  4380 |        438 |   0.0789 |  0.1  |                 0.804 |     nan      | estimable                               |
| P-C4     | d_ln_ocupados x ln p_suelo                   |  1134 |         50 |   0.1539 |  0.1  |                 0.806 |     nan      | no detectable con los datos disponibles |
| P-C4     | d_ln_pob_total x ln p_suelo                  |  1134 |         50 |   0.6695 |  0.1  |                 0.758 |     nan      | no detectable con los datos disponibles |

## Notas por fila

- P-C1 / OLS FE sección+año, nacional: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=0.574; coef=0.0011
- P-C1 / OLS FE, 6 ciudades grandes (pool): log-puntos de alquiler por 1 pp VUT/viviendas. cluster distrito; sd residual VUT tras FE=0.693; coef=0.0040
- P-C1 / OLS FE, Barcelona: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=0.445; coef=-0.0042
- P-C1 / OLS FE, Madrid: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=0.318; coef=0.0032
- P-C1 / OLS FE, València: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=0.485; coef=0.0050
- P-C1 / OLS FE, Sevilla: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=0.782; coef=-0.0027
- P-C1 / OLS FE, Málaga: log-puntos de alquiler por 1 pp VUT/viviendas. ; sd residual VUT tras FE=2.053; coef=0.0017
- P-C1 / shift-share LOO municipio, nacional: log-puntos por 1 pp VUT (2SLS). coef 2SLS=0.0223; sd z tras FE=2.024
- P-C1 / shift-share LOO municipio, 6 ciudades: log-puntos por 1 pp VUT (2SLS). coef 2SLS=0.0069; sd z tras FE=0.845
- P-C1 / shift-share LOO provincia, nacional: log-puntos por 1 pp VUT (2SLS). coef 2SLS=0.0180; sd z tras FE=0.590
- P-C1 / shift-share LOO provincia, 6 ciudades: log-puntos por 1 pp VUT (2SLS). coef 2SLS=0.0076; sd z tras FE=0.438
- P-C2 / caída de anuncios 2025-2026 -> alquiler fino: log-puntos de alquiler por 1 de caída log de anuncios. Resultado de alquiler a escala fina posterior a 2025: NO. {"serpavi_distrito_max_anio": 2024, "incasol_max_anio_nivel_municipal": 2026, "madrid_cp_periodos": ["2023", "2024"], "insideairbnb_rango": ["2025-12-14", "2026-09-28"]}. Incasòl llega a 2026 pero solo a escala municipal y las capturas Inside Airbnb empiezan en 2025-12 (sin periodo previo).
- P-C3 / topes Ley 11/2020 (2016-2022) -> alquiler: log-puntos (efecto = coef de D). PROXY de tratados (58 mayores zonificados); la lista 2020 no está en data/; tratados=58, controles=395; coef=-0.0218; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / topes Ley 11/2020 (2016-2022) -> contratos: log-puntos (efecto = coef de D). PROXY de tratados (58 mayores zonificados); la lista 2020 no está en data/; tratados=58, controles=395; coef=0.0019; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / zonas tensionadas (2016-2025) -> alquiler: log-puntos (efecto = coef de D). tratamiento = fracción del año con zona declarada; tratados=268, controles=170; coef=-0.0468; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C3 / zonas tensionadas (2016-2025) -> contratos: log-puntos (efecto = coef de D). tratamiento = fracción del año con zona declarada; tratados=268, controles=170; coef=-0.2027; renta = media ponderada de medias de banda (bandas cambian entre años)
- P-C4 / d_ln_ocupados x ln p_suelo: diferencia de elasticidad p75-p25 de ln(p_suelo). coef interacción=0.1598; IQR ln p_suelo=0.66; p_suelo = media provincial (invariante)
- P-C4 / d_ln_pob_total x ln p_suelo: diferencia de elasticidad p75-p25 de ln(p_suelo). coef interacción=-0.9369; IQR ln p_suelo=0.66; p_suelo = media provincial (invariante)

Pérdidas de armonización P-C1 (secciones): {"unidades_alq_sin_vut_o_censo": 13, "unidades_no_balanceadas_o_sin_alq": 2766, "unidades_finales": 17657}

Advertencia P-C1: SERPAVI es stock IRPF y amortigua el alquiler; si el efecto sobre el stock es una fracción k del efecto sobre contratos nuevos, el EMD relevante es EMD/k (peor). VUT INE cubre ~89-90 % (error de medida, sesgo a 0).