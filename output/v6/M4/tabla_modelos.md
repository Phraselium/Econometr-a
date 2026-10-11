# M4: modelos en la validacion sellada v6

Fecha: 2026-10-11. Validacion espacial nueva (11 provincias nunca usadas como validacion); temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5; el ultimo anio cae en la ventana sellada de v2. Las conclusiones se apoyan en la parte espacial.

Error en log-puntos x100 (aprox. %). DM-HLN una cola a favor del modelo, perdida cuadratica, celdas (provincia, periodo); Holm dentro de cada tarea y grupo.

## Mejor modelo por tarea (grupo espacial)

| tarea | mercado | medida_precio | nivel | mejor_modelo | rmse_pct_espacial | rmse_persistencia_espacial | p_holm_vs_persistencia | bate_persistencia | lectura |
|---|---|---|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | compra (precio) | valor tasado MIVAU municipal | municipio (anual) | MUN_PRECIO_ANUAL__ecm_v1 | 3.9328 | 0.0633 | 0.0000 | False | El mejor es la linea base ecm_v1: el mejor modelo de M3 (MUN_PRECIO_ANUAL__bosque_bootstrap_bayesiano) no la mejora en mas de un 5 % de RMSE en la parte espacial. |
| PROV_PRECIO_ANUAL | compra (precio) | valor tasado MIVAU | provincia (anual) | PROV_PRECIO_ANUAL__random_forest | 2.4782 | 0.0396 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| PROV_PRECIO_ANUAL_REGISTRADORES | compra (precio) | Registradores (robustez) | provincia (anual) | PROV_PRECIO_ANUAL_REGISTRADORES__ecm_v1 | 4.6759 | 0.0603 | 0.0000 | False | El mejor es la linea base ecm_v1: el mejor modelo de M3 (PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano) no la mejora en mas de un 5 % de RMSE en la parte espacial. |
| PROV_PRECIO_TRIM | compra (precio) | valor tasado MIVAU | provincia (trimestral) | PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano | 1.6140 | 0.0193 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| PROV_VOL_ANUAL | compra (volumen) | nan | provincia (anual) | PROV_VOL_ANUAL__bosque_bootstrap_bayesiano | 13.0447 | 0.1586 | 0.0001 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| PROV_VOL_TRIM | compra (volumen) | nan | provincia (trimestral) | PROV_VOL_TRIM__bosque_bootstrap_bayesiano | 11.3011 | 0.1846 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| alq_distrito | alquiler de stock (SERPAVI) | nan | distrito | alquiler_distrito_gb | 5.6027 | 0.0698 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| alq_municipio | alquiler de stock (SERPAVI) | nan | municipio | alquiler_municipio_rf | 5.0645 | 0.0651 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |
| alq_provincia | alquiler de stock (SERPAVI) | nan | provincia | alquiler_provincia_gb | 1.6066 | 0.0421 | 0.0000 | True | Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm). |

## Sintesis por variable

| mercado | variable | signo_esperado | direccion | PIP | F1_ok | F2_ok | F3_ok | criterio_A | criterio_B | clasificacion |
|---|---|---|---|---|---|---|---|---|---|---|
| alquiler de stock (SERPAVI) | ln_pob | 1 | positiva | 1.0000 | False | True | False | False | True | EXPLORATORIA (C4): apoyo en una familia |
| alquiler de stock (SERPAVI) | share_ext_pob | 1 | positiva | 0.2971 | False | False | True | False | True | EXPLORATORIA (C4): apoyo en una familia |
| alquiler de stock (SERPAVI) | ln_pib_pc | 1 | positiva | 0.0972 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| alquiler de stock (SERPAVI) | ln_vut | 1 | negativa | 0.1160 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| alquiler de stock (SERPAVI) | ln_terminadas_libres | -1 | negativa | 0.1688 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| alquiler de stock (SERPAVI) | ln_iniciadas_libres | -1 | negativa | 0.0891 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| alquiler de stock (SERPAVI) | n_mun_tensionados | -1 | sin direccion estable |  | False | False | False | False | True | SIN APOYO suficiente (C4) |
| alquiler de stock (SERPAVI) | n_mun_topes_cat | -1 | positiva | 0.2313 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_pob | 1 | positiva | 0.7633 | False | True | False | False | True | EXPLORATORIA (C4): apoyo en una familia |
| compra (precio, valor tasado MIVAU) | share_ext_pob | 1 | positiva | 0.3083 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_pib_pc | 1 | positiva | 0.8436 | False | True | False | False | True | EXPLORATORIA (C4): apoyo en una familia |
| compra (precio, valor tasado MIVAU) | ln_ocupados_miles | 1 | positiva | 0.1964 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | paro_tasa | -1 | positiva | 0.1314 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_terminadas_libres | -1 | negativa | 0.1163 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_iniciadas_libres | -1 | positiva | 0.1236 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_suelo_pm2_m50k | 1 | positiva | 0.1448 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_vut | 0 | positiva | 0.0954 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (precio, valor tasado MIVAU) | ln_hip_viv_num | 1 | positiva | 0.1217 | False | False | False | False | True | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | ln_pib_pc | 1 | positiva | 0.0926 | False | False | False | False | False | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | ln_ocupados_miles | 1 | negativa | 0.1017 | False | False | False | False | False | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | ln_pob | 1 | negativa | 0.0976 | False | False | False | False | False | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | paro_tasa | -1 | negativa | 0.2237 | False | False | False | False | False | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | ln_terminadas_libres | 0 | negativa | 0.1128 | False | False | False | False | False | SIN APOYO suficiente (C4) |
| compra (volumen, ETDP) | ln_iniciadas_libres | 0 | negativa | 0.9774 | False | False | False | False | False | SIN APOYO suficiente (C4) |

## Tabla de modelos, grupo espacial

| tarea | modelo_id | rol | n | rmse_pct | cobertura95 | sd_rmse_entre_periodos | ratio_rmse_vs_persistencia | p_holm_vs_persistencia | p_holm_vs_ar_unidad | p_holm_vs_ecm_v1 |
|---|---|---|---|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__ar_unidad | base | 678 | 6.3256 | 1.0000 | 0.0164 | 1.0000 |  |  | 1.0000 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__bosque_bootstrap_bayesiano | modelo | 678 | 4.1270 | 0.9779 | 0.0078 | 0.6524 | 0.0000 | 0.0000 | 1.0000 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__ecm_v1 | base | 678 | 3.9328 | 1.0000 | 0.0071 | 0.6217 | 0.0000 | 0.0000 |  |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__m1_econ | base | 678 | 6.3256 | 1.0000 | 0.0164 | 1.0000 |  |  | 1.0000 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__persistencia | base | 678 | 6.3256 | 0.9307 | 0.0164 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__ar_unidad | base | 99 | 6.0321 | 0.9798 | 0.0132 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano | modelo | 99 | 4.6995 | 0.8990 | 0.0085 | 0.7791 | 0.0000 | 0.0000 | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__ecm_v1 | base | 99 | 4.6759 | 1.0000 | 0.0078 | 0.7752 | 0.0000 | 0.0000 |  |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__m1_econ | base | 99 | 6.0321 | 0.9798 | 0.0132 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__persistencia | base | 99 | 6.0321 | 0.8889 | 0.0132 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__ar_unidad | base | 95 | 3.9638 | 0.9368 | 0.0156 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__ecm_v1 | base | 95 | 2.8178 | 0.9895 | 0.0105 | 0.7109 | 0.0000 | 0.0000 |  |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__m1_econ | base | 95 | 3.9638 | 0.9368 | 0.0156 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__persistencia | base | 95 | 3.9638 | 0.8632 | 0.0156 | 1.0000 |  |  | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__random_forest | modelo | 95 | 2.4782 | 0.9684 | 0.0047 | 0.6252 | 0.0000 | 0.0000 | 0.0102 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__ar_unidad | base | 380 | 1.9310 | 1.0000 | 0.0042 | 1.0000 |  |  |  |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano | modelo | 380 | 1.6140 | 0.9921 | 0.0034 | 0.8358 | 0.0000 | 0.0000 | 0.0000 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__ecm_v1 | base | 380 | 1.9310 | 1.0000 | 0.0042 | 1.0000 |  |  |  |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__m1_econ | base | 380 | 1.9310 | 1.0000 | 0.0042 | 1.0000 |  |  |  |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__persistencia | base | 380 | 1.9310 | 0.9789 | 0.0042 | 1.0000 |  |  |  |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__ar_unidad | base | 99 | 15.8610 | 1.0000 | 0.0534 | 1.0000 |  |  | 1.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__bosque_bootstrap_bayesiano | modelo | 99 | 13.0447 | 1.0000 | 0.0423 | 0.8224 | 0.0001 | 0.0001 | 0.4760 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__ecm_v1 | base | 99 | 13.6984 | 1.0000 | 0.0578 | 0.8637 | 0.0054 | 0.0054 |  |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__m1_econ | base | 99 | 15.8610 | 1.0000 | 0.0534 | 1.0000 |  |  | 1.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__persistencia | base | 99 | 15.8610 | 1.0000 | 0.0534 | 1.0000 |  |  | 1.0000 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__ar_unidad | base | 380 | 18.4571 | 0.9974 | 0.1001 | 1.0000 |  |  |  |
| PROV_VOL_TRIM | PROV_VOL_TRIM__bosque_bootstrap_bayesiano | modelo | 380 | 11.3011 | 0.9974 | 0.0273 | 0.6123 | 0.0000 | 0.0000 | 0.0000 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__ecm_v1 | base | 380 | 18.4571 | 0.9974 | 0.1001 | 1.0000 |  |  |  |
| PROV_VOL_TRIM | PROV_VOL_TRIM__m1_econ | base | 380 | 18.4571 | 1.0000 | 0.1001 | 1.0000 |  |  |  |
| PROV_VOL_TRIM | PROV_VOL_TRIM__persistencia | base | 380 | 18.4571 | 0.9632 | 0.1001 | 1.0000 |  |  |  |
| alq_distrito | alq_distrito__ar_unidad | base | 7256 | 6.9801 | 0.9829 | 0.0138 | 1.0000 |  |  | 1.0000 |
| alq_distrito | alq_distrito__ecm_v1 | base | 7256 | 6.1217 | 0.9048 | 0.0145 | 0.8770 | 0.0000 | 0.0000 |  |
| alq_distrito | alq_distrito__m1_econ | base | 7256 | 6.9801 | 0.9702 | 0.0138 | 1.0000 |  |  | 1.0000 |
| alq_distrito | alq_distrito__persistencia | base | 7256 | 6.9801 | 0.9294 | 0.0138 | 1.0000 |  |  | 1.0000 |
| alq_distrito | alquiler_distrito_gb | modelo | 7256 | 5.6027 | 0.9187 | 0.0109 | 0.8027 | 0.0000 | 0.0000 | 0.0000 |
| alq_distrito | alquiler_distrito_gnn | modelo | 7256 | 5.9327 | 0.9052 | 0.0110 | 0.8499 | 0.0000 | 0.0000 | 0.3648 |
| alq_distrito | alquiler_distrito_mixto | modelo | 7256 | 6.9303 | 0.8954 | 0.0108 | 0.9929 | 0.6111 | 0.6111 | 1.0000 |
| alq_distrito | alquiler_distrito_mlp | modelo | 7256 | 5.9537 | 0.9052 | 0.0095 | 0.8530 | 0.0000 | 0.0000 | 0.5246 |
| alq_distrito | alquiler_distrito_rf | modelo | 7256 | 5.7476 | 0.9136 | 0.0116 | 0.8234 | 0.0000 | 0.0000 | 0.0000 |
| alq_municipio | alq_municipio__ar_unidad | base | 3815 | 6.5064 | 0.9727 | 0.0114 | 1.0000 |  |  | 1.0000 |
| alq_municipio | alq_municipio__ecm_v1 | base | 3815 | 6.1890 | 0.9106 | 0.0097 | 0.9512 | 0.0011 | 0.0011 |  |
| alq_municipio | alq_municipio__m1_econ | base | 3815 | 6.5064 | 0.9761 | 0.0114 | 1.0000 |  |  | 1.0000 |
| alq_municipio | alq_municipio__persistencia | base | 3815 | 6.5064 | 0.9421 | 0.0114 | 1.0000 |  |  | 1.0000 |
| alq_municipio | alquiler_municipio_gb | modelo | 3815 | 5.0543 | 0.9376 | 0.0078 | 0.7768 | 0.0000 | 0.0000 | 0.0000 |
| alq_municipio | alquiler_municipio_mixto | modelo | 3815 | 6.1976 | 0.9135 | 0.0093 | 0.9525 | 0.0010 | 0.0010 | 1.0000 |
| alq_municipio | alquiler_municipio_rf | modelo | 3815 | 5.0645 | 0.9389 | 0.0074 | 0.7784 | 0.0000 | 0.0000 | 0.0000 |
| alq_provincia | alq_provincia__ar_unidad | base | 82 | 4.2098 | 0.8537 | 0.0186 | 1.0000 |  |  | 1.0000 |
| alq_provincia | alq_provincia__ecm_v1 | base | 82 | 3.3504 | 0.5000 | 0.0123 | 0.7959 | 0.0000 | 0.0000 |  |
| alq_provincia | alq_provincia__m1_econ | base | 82 | 4.2098 | 0.9634 | 0.0186 | 1.0000 |  |  | 1.0000 |
| alq_provincia | alq_provincia__persistencia | base | 82 | 4.2098 | 0.9390 | 0.0186 | 1.0000 |  |  | 1.0000 |
| alq_provincia | alquiler_provincia_gb | modelo | 82 | 1.6066 | 0.8902 | 0.0082 | 0.3816 | 0.0000 | 0.0000 | 0.0000 |
| alq_provincia | alquiler_provincia_mixto | modelo | 82 | 3.3659 | 0.6098 | 0.0118 | 0.7995 | 0.0001 | 0.0001 | 1.0000 |
| alq_provincia | alquiler_provincia_rf | modelo | 82 | 1.6321 | 0.8659 | 0.0095 | 0.3877 | 0.0000 | 0.0000 | 0.0000 |

## Tabla de modelos, grupo temporal

| tarea | modelo_id | rol | n | rmse_pct | cobertura95 | sd_rmse_entre_periodos | ratio_rmse_vs_persistencia | p_holm_vs_persistencia | p_holm_vs_ar_unidad | p_holm_vs_ecm_v1 |
|---|---|---|---|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__ar_unidad | base | 200 | 7.5350 | 0.9800 |  | 0.6268 | 0.0000 |  | 1.0000 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__bosque_bootstrap_bayesiano | modelo | 200 | 7.5707 | 0.7600 |  | 0.6297 | 0.0000 | 1.0000 | 1.0000 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__ecm_v1 | base | 200 | 7.4222 | 0.9950 |  | 0.6174 | 0.0000 | 1.0000 |  |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__m1_econ | base | 200 | 6.7231 | 0.9900 |  | 0.5592 | 0.0000 | 1.0000 | 0.1071 |
| MUN_PRECIO_ANUAL | MUN_PRECIO_ANUAL__persistencia | base | 200 | 12.0222 | 0.4800 |  | 1.0000 |  | 1.0000 | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__ar_unidad | base | 41 | 16.0214 | 0.9024 |  | 1.7669 | 1.0000 |  | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano | modelo | 41 | 6.4115 | 0.8537 |  | 0.7071 | 0.0000 | 1.0000 | 1.0000 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__ecm_v1 | base | 41 | 6.3865 | 0.9756 |  | 0.7043 | 0.0000 | 1.0000 |  |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__m1_econ | base | 41 | 5.9562 | 1.0000 |  | 0.6569 | 0.0000 | 1.0000 | 0.7089 |
| PROV_PRECIO_ANUAL_REGISTRADORES | PROV_PRECIO_ANUAL_REGISTRADORES__persistencia | base | 41 | 9.0676 | 0.5610 |  | 1.0000 |  | 1.0000 | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__ar_unidad | base | 41 | 5.5018 | 0.8293 |  | 0.6091 | 0.0000 |  | 0.0133 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__ecm_v1 | base | 41 | 7.0317 | 0.6829 |  | 0.7784 | 0.0000 | 1.0000 |  |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__m1_econ | base | 41 | 5.2296 | 0.9512 |  | 0.5789 | 0.0000 | 1.0000 | 0.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__persistencia | base | 41 | 9.0334 | 0.1463 |  | 1.0000 |  | 1.0000 | 1.0000 |
| PROV_PRECIO_ANUAL | PROV_PRECIO_ANUAL__random_forest | modelo | 41 | 6.0203 | 0.4146 |  | 0.6664 | 0.0000 | 1.0000 | 0.0000 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__ar_unidad | base | 164 | 3.3119 | 0.9634 | 0.0033 | 1.1264 | 1.0000 |  | 1.0000 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano | modelo | 164 | 2.2685 | 0.9451 | 0.0015 | 0.7715 | 0.0000 | 0.0000 | 0.0491 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__ecm_v1 | base | 164 | 2.3718 | 1.0000 | 0.0015 | 0.8067 | 0.0000 | 0.0001 |  |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__m1_econ | base | 164 | 2.6384 | 1.0000 | 0.0026 | 0.8973 | 0.0000 | 0.0036 | 1.0000 |
| PROV_PRECIO_TRIM | PROV_PRECIO_TRIM__persistencia | base | 164 | 2.9403 | 0.7683 | 0.0026 | 1.0000 |  | 0.1567 | 1.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__ar_unidad | base | 41 | 18.6822 | 1.0000 |  | 1.2113 | 1.0000 |  | 1.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__bosque_bootstrap_bayesiano | modelo | 41 | 8.5769 | 1.0000 |  | 0.5561 | 0.0000 | 0.0000 | 0.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__ecm_v1 | base | 41 | 13.0036 | 1.0000 |  | 0.8431 | 0.0000 | 0.0026 |  |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__m1_econ | base | 41 | 19.0347 | 1.0000 |  | 1.2341 | 1.0000 | 1.0000 | 1.0000 |
| PROV_VOL_ANUAL | PROV_VOL_ANUAL__persistencia | base | 41 | 15.4236 | 1.0000 |  | 1.0000 |  | 0.0699 | 1.0000 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__ar_unidad | base | 164 | 16.4446 | 1.0000 | 0.0161 | 1.4563 | 1.0000 |  | 1.0000 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__bosque_bootstrap_bayesiano | modelo | 164 | 12.0039 | 1.0000 | 0.0199 | 1.0630 | 1.0000 | 0.0031 | 1.0000 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__ecm_v1 | base | 164 | 11.9936 | 1.0000 | 0.0123 | 1.0621 | 1.0000 | 0.0021 |  |
| PROV_VOL_TRIM | PROV_VOL_TRIM__m1_econ | base | 164 | 11.5673 | 1.0000 | 0.0062 | 1.0243 | 1.0000 | 0.0008 | 0.2847 |
| PROV_VOL_TRIM | PROV_VOL_TRIM__persistencia | base | 164 | 11.2924 | 0.9939 | 0.0093 | 1.0000 |  | 0.0001 | 1.0000 |
| alq_distrito | alq_distrito__ar_unidad | base | 2437 | 8.8133 | 0.9618 |  | 1.1288 | 1.0000 |  | 1.0000 |
| alq_distrito | alq_distrito__ecm_v1 | base | 2437 | 5.6438 | 0.9282 |  | 0.7228 | 0.0000 | 0.0000 |  |
| alq_distrito | alq_distrito__m1_econ | base | 2437 | 7.9843 | 0.9581 |  | 1.0226 | 1.0000 | 0.0015 | 1.0000 |
| alq_distrito | alq_distrito__persistencia | base | 2437 | 7.8077 | 0.9208 |  | 1.0000 |  | 0.0005 | 1.0000 |
| alq_distrito | alquiler_distrito_gb | modelo | 2437 | 5.4233 | 0.9245 |  | 0.6946 | 0.0000 | 0.0000 | 0.0007 |
| alq_distrito | alquiler_distrito_gnn | modelo | 2437 | 5.4431 | 0.9265 |  | 0.6971 | 0.0000 | 0.0000 | 0.3575 |
| alq_distrito | alquiler_distrito_mixto | modelo | 2437 | 5.6203 | 0.9307 |  | 0.7198 | 0.0000 | 0.0000 | 1.0000 |
| alq_distrito | alquiler_distrito_mlp | modelo | 2437 | 5.3936 | 0.9265 |  | 0.6908 | 0.0000 | 0.0000 | 0.0349 |
| alq_distrito | alquiler_distrito_rf | modelo | 2437 | 5.4684 | 0.9261 |  | 0.7004 | 0.0000 | 0.0000 | 0.0043 |
| alq_municipio | alq_municipio__ar_unidad | base | 1821 | 1627.3509 | 0.9286 |  | 205.5860 | 1.0000 |  | 1.0000 |
| alq_municipio | alq_municipio__ecm_v1 | base | 1821 | 5.9030 | 0.9165 |  | 0.7457 | 0.0000 | 1.0000 |  |
| alq_municipio | alq_municipio__m1_econ | base | 1821 | 7.5724 | 0.9528 |  | 0.9566 | 1.0000 | 1.0000 | 1.0000 |
| alq_municipio | alq_municipio__persistencia | base | 1821 | 7.9157 | 0.9132 |  | 1.0000 |  | 1.0000 | 1.0000 |
| alq_municipio | alquiler_municipio_gb | modelo | 1821 | 5.8241 | 0.9121 |  | 0.7358 | 0.0000 | 1.0000 | 0.3298 |
| alq_municipio | alquiler_municipio_mixto | modelo | 1821 | 5.8960 | 0.9237 |  | 0.7448 | 0.0000 | 1.0000 | 1.0000 |
| alq_municipio | alquiler_municipio_rf | modelo | 1821 | 5.6850 | 0.9187 |  | 0.7182 | 0.0000 | 1.0000 | 0.0082 |
| alq_provincia | alq_provincia__ar_unidad | base | 39 | 1.0149 | 1.0000 |  | 0.1931 | 0.0000 |  | 0.0123 |
| alq_provincia | alq_provincia__ecm_v1 | base | 39 | 1.9952 | 0.7179 |  | 0.3795 | 0.0000 | 1.0000 |  |
| alq_provincia | alq_provincia__m1_econ | base | 39 | 2.6541 | 1.0000 |  | 0.5049 | 0.0000 | 1.0000 | 1.0000 |
| alq_provincia | alq_provincia__persistencia | base | 39 | 5.2568 | 0.9744 |  | 1.0000 |  | 1.0000 | 1.0000 |
| alq_provincia | alquiler_provincia_gb | modelo | 39 | 1.6060 | 0.9231 |  | 0.3055 | 0.0000 | 1.0000 | 0.4251 |
| alq_provincia | alquiler_provincia_mixto | modelo | 39 | 1.8951 | 0.7949 |  | 0.3605 | 0.0000 | 1.0000 | 0.4016 |
| alq_provincia | alquiler_provincia_rf | modelo | 39 | 1.3851 | 0.8718 |  | 0.2635 | 0.0000 | 1.0000 | 0.0661 |
