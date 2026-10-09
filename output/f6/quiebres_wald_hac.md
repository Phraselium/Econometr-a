ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Contraste de quiebre en fechas candidatas: Wald HAC(8) conjunto de (intercepto, pendiente) post-fecha, N=82. Sustituye al Chow F clásico (que supone errores no autocorrelacionados y sobrerrechaza); el Chow se conserva como complemento en chow_beta.

| modelo                    | fecha   |   n |   dif_beta_post |   EE_dif_beta |   dif_const_post |   EE_dif_const |   p_Wald_HAC8 |
|:--------------------------|:--------|----:|----------------:|--------------:|-----------------:|---------------:|--------------:|
| València_vs_Provincia     | 2014Q1  |  82 |         0.07054 |        0.2346 |           1.239  |          1.628 |     0.4807    |
| València_vs_Provincia     | 2020Q1  |  82 |        -0.4286  |        0.1852 |           3.709  |          1.365 |     0.003993  |
| València_vs_Provincia     | 2022Q3  |  82 |        -0.5972  |        0.2274 |           5.244  |          2.277 |     0.02263   |
| València_vs_C. Valenciana | 2014Q1  |  82 |        -0.1631  |        0.2625 |           0.2912 |          1.933 |     0.8094    |
| València_vs_C. Valenciana | 2020Q1  |  82 |        -0.6298  |        0.1896 |           3.645  |          1.375 |     1.356e-05 |
| València_vs_C. Valenciana | 2022Q3  |  82 |        -0.7319  |        0.2301 |           4.839  |          2.127 |     0.004997  |
| València_vs_España        | 2014Q1  |  82 |         0.03987 |        0.3025 |           1.053  |          2.129 |     0.7928    |
| València_vs_España        | 2020Q1  |  82 |        -0.5278  |        0.1806 |           5.053  |          1.37  |     7.416e-07 |
| València_vs_España        | 2022Q3  |  82 |        -0.7022  |        0.267  |           6.083  |          2.444 |     0.01528   |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
