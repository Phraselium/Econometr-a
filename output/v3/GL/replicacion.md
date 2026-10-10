# Réplica conceptual de García-López et al. (2020), Barcelona (C4, EXPLORATORIO)

Objetivo: 0,035 (EE 0,009) log-puntos de alquiler por 100 anuncios (WP 2019, Tabla 3, panel A, col. 2). Propio: log mediana SERPAVI €/m2 (vivienda colectiva, stock IRPF) 2021-2024, VUT del INE (media anual de oleadas hasta 2024M11), FE de sección y año, cluster por distrito. Sin sellados v3 (distritos 09 y 10 de Barcelona excluidos) y sin 2026M05. Sin instrumento ni histórico 2012-2016: NO es réplica exacta.

| especificacion                    | nivel    | unidad_coef                                 |     N |   clusters |    coef |     ee |   ic95_lo |   ic95_hi |   p_holm | clasificacion   | criterio                                |
|:----------------------------------|:---------|:--------------------------------------------|------:|-----------:|--------:|-------:|----------:|----------:|---------:|:----------------|:----------------------------------------|
| GL1_bcn_seccion_vut100viv         | seccion  | log-puntos por 100 VUT/100 viviendas (1 pp) |  3260 |          8 | -0.0042 | 0.0015 |   -0.0078 |   -0.0005 |   0.2686 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| GL2_bcn_distrito_vut100viv        | distrito | log-puntos por 1 pp                         |    32 |          8 | -0.0054 | 0.0017 |   -0.0093 |   -0.0014 |   0.1749 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| GL3_bcn_seccion_vut_cien          | seccion  | log-puntos por 100 VUT (homogéneo)          |  3260 |          8 | -0.0421 | 0.0127 |   -0.0722 |   -0.012  |   0.1696 | NO REPLICADO    | signo distinto                          |
| GL4_bcn_distrito_vut_cien         | distrito | log-puntos por 100 VUT (homogéneo)          |    32 |          8 | -0.0008 | 0.0003 |   -0.0015 |   -0.0001 |   0.2631 | NO REPLICADO    | signo distinto                          |
| GL5_bcn_seccion_vut_cien_pond_viv | seccion  | log-puntos por 100 VUT, pond. viviendas     |  3260 |          8 | -0.0405 | 0.0092 |   -0.0622 |   -0.0188 |   0.0463 | NO REPLICADO    | signo distinto                          |
| EXT_Madrid_seccion_vut100viv      | seccion  | log-puntos por 1 pp                         |  7160 |         16 |  0.0032 | 0.0023 |   -0.0016 |    0.008  |   0.7886 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| EXT_Madrid_seccion_vut_cien       | seccion  | log-puntos por 100 VUT                      |  7160 |         16 |  0.0409 | 0.0267 |   -0.016  |    0.0977 |   0.7886 | REPLICADO       | IC95 contiene 0,035 y mismo signo       |
| EXT_València_seccion_vut100viv    | seccion  | log-puntos por 1 pp                         |  1940 |         15 |  0.005  | 0.0023 |    0.0001 |    0.0099 |   0.374  | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| EXT_València_seccion_vut_cien     | seccion  | log-puntos por 100 VUT                      |  1940 |         15 |  0.049  | 0.0293 |   -0.0137 |    0.1117 |   0.7886 | REPLICADO       | IC95 contiene 0,035 y mismo signo       |
| EXT_Sevilla_seccion_vut100viv     | seccion  | log-puntos por 1 pp                         |  1408 |          8 | -0.0027 | 0.0008 |   -0.0044 |   -0.0009 |   0.1387 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| EXT_Sevilla_seccion_vut_cien      | seccion  | log-puntos por 100 VUT                      |  1408 |          8 | -0.0239 | 0.0075 |   -0.0417 |   -0.0061 |   0.1749 | NO REPLICADO    | signo distinto                          |
| EXT_Málaga_seccion_vut100viv      | seccion  | log-puntos por 1 pp                         |   916 |          8 |  0.0017 | 0.0023 |   -0.0038 |    0.0072 |   0.9552 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| EXT_Málaga_seccion_vut_cien       | seccion  | log-puntos por 100 VUT                      |   916 |          8 |  0.0084 | 0.0145 |   -0.0258 |    0.0427 |   0.9552 | REPLICADO       | IC95 contiene 0,035 y mismo signo       |
| EXT_Espana_seccion_vut100viv      | seccion  | log-puntos por 1 pp                         | 70628 |       2888 |  0.0011 | 0.0007 |   -0.0003 |    0.0025 |   0.7886 | NO REPLICABLE   | unidades no homogéneas con el objetivo  |
| EXT_Espana_seccion_vut_cien       | seccion  | log-puntos por 100 VUT                      | 70628 |       2888 |  0.0053 | 0.0035 |   -0.0016 |    0.0121 |   0.7886 | PARCIAL         | mismo signo pero IC95 no contiene 0,035 |

Las filas con unidades «por 1 pp» (VUT por 100 viviendas) no son homogéneas con el objetivo (por 100 anuncios): clasificación NO REPLICABLE por unidades. Las filas «por 100 VUT» sí son homogéneas (VUT INE ≈ anuncios, salvedad de definición).

## Diagnósticos
```
{
 "pretendencia_adelanto_BCN": {
  "coef_lead": 0.000370791197879277,
  "ee": 0.0009436742970765327,
  "p": 0.7060677840533012,
  "nota": "N=3 a\u00f1os; FE; el adelanto de VUT no deber\u00eda predecir el alquiler"
 },
 "placebo_permutacion_BCN": {
  "reps": 500,
  "coef_real": -0.004166504610531088,
  "p_perm": 0.0,
  "sd_placebo": 0.0009169195595062796
 }
}
```

Pérdidas de armonización (unidades): {"seccion_nacional": {"unidades_alq_sin_vut_o_censo": 13, "unidades_no_balanceadas_o_sin_alq": 2766, "unidades_finales": 17657}, "distrito_nacional": {"unidades_alq_sin_vut_o_censo": 4, "unidades_no_balanceadas_o_sin_alq": 454, "unidades_finales": 2975}}

REPLICADO con IC que incluye 0 (Madrid, València, Málaga) es una coincidencia por imprecisión, no confirmación.

Notas: {"distritos_BCN_incluidos": ["01", "02", "03", "04", "05", "06", "07", "08"], "Palma_no_estimable": "menos de 2 distritos no sellados con datos: sin clusters"}

Nivel de evidencia: EXPLORATORIO (C4).