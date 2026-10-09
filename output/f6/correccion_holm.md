ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Corrección por búsqueda sobre la familia de 11 contrastes de interés (diferenciales medios, β=1, diferencia de cuota, tendencias) registrados en output/registro_busqueda_f6.csv.

|                                                    |   p_bruto |    p_Holm |   p_Bonferroni |
|:---------------------------------------------------|----------:|----------:|---------------:|
| cuota_ext_dif_CV_ES                                | 7.452e-32 | 8.197e-31 |      8.197e-31 |
| tendencia_cuota_CV                                 | 4.572e-13 | 4.572e-12 |      5.03e-12  |
| tendencia_cuota_ES                                 | 6.314e-13 | 5.683e-12 |      6.946e-12 |
| beta=1_beta_València_vs_España                     | 4.712e-12 | 3.77e-11  |      5.183e-11 |
| beta=1_beta_València_vs_C. Valenciana              | 4.367e-07 | 3.057e-06 |      4.804e-06 |
| beta=1_beta_València_vs_Provincia                  | 2.861e-05 | 0.0001717 |      0.0003147 |
| beta=1_beta_compraventas_València_vs_España        | 0.01196   | 0.05979   |      0.1315    |
| beta=1_beta_compraventas_València_vs_C. Valenciana | 0.2377    | 0.9506    |      1         |
| dif_media_C. Valenciana                            | 0.3083    | 0.9506    |      1         |
| dif_media_España                                   | 0.3636    | 0.9506    |      1         |
| dif_media_Provincia                                | 0.5412    | 0.9506    |      1         |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
