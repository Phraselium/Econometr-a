ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Corrección por búsqueda sobre la familia de 16 contrastes de interés (diferenciales medios, β=1, diferencia de cuota, Wald de igualdad de betas, diferencial de nivel 2020-26; las tendencias lineales de las cuotas (I(1)) quedan fuera) registrados en output/registro_busqueda_f6.csv.

|                                                                   |   p_bruto |    p_Holm |   p_Bonferroni |
|:------------------------------------------------------------------|----------:|----------:|---------------:|
| cuota_ext_dif_CV_ES                                               | 3.942e-20 | 6.307e-19 |      6.307e-19 |
| beta=1_beta_València_vs_España                                    | 4.712e-12 | 7.068e-11 |      7.539e-11 |
| dif_nivel_2020-26_València_vs_C. Valenciana                       | 2.586e-10 | 3.621e-09 |      4.138e-09 |
| dif_nivel_2020-26_València_vs_España                              | 8.636e-09 | 1.123e-07 |      1.382e-07 |
| dif_nivel_2020-26_València_vs_Provincia                           | 7.538e-08 | 9.045e-07 |      1.206e-06 |
| beta=1_beta_València_vs_C. Valenciana                             | 4.367e-07 | 4.804e-06 |      6.987e-06 |
| wald_betas_iguales_València_vs_Provincia                          | 2.909e-06 | 2.909e-05 |      4.654e-05 |
| beta=1_beta_València_vs_Provincia                                 | 2.861e-05 | 0.0002575 |      0.0004578 |
| wald_betas_iguales_València_vs_C. Valenciana                      | 3.983e-05 | 0.0003186 |      0.0006373 |
| wald_betas_iguales_València_vs_España                             | 0.001722  | 0.01206   |      0.02756   |
| beta=1_beta_compraventas_València_vs_España                       | 0.01196   | 0.07174   |      0.1913    |
| beta=1_beta_compraventas_València_vs_C. Valenciana                | 0.2377    | 1         |      1         |
| dif_media_C. Valenciana                                           | 0.3083    | 1         |      1         |
| dif_media_España                                                  | 0.3636    | 1         |      1         |
| beta=1_beta_compraventas_València_vs_CV sin València (parte-todo) | 0.5057    | 1         |      1         |
| dif_media_Provincia                                               | 0.5412    | 1         |      1         |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
