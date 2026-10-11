# K1: modelos de v6 frente a lineas base exigentes (validacion sellada v6)

Fecha: 2026-10-11. Segunda mirada a la misma muestra sellada para NUEVOS comparadores (las predicciones de los modelos de v6 no cambian). Error en log-puntos x100 (aprox. %). La base exigente es la de menor RMSE espacial entre persistencia, AR por unidad, ECM v1, M1 econ y las tres nuevas en su variante factible. DM-HLN y permutacion de una cola (a favor del modelo), Holm por tarea y grupo; 11 provincias selladas: poca potencia.

## Resultado por tarea (grupo espacial)

| tarea | medida_precio | mejor_modelo | base_exigente | rmse_pct_modelo | rmse_pct_base | ratio | p_dm_hln_holm | p_dm_hln_per_holm | p_perm_holm | clase_rotulo |
|---|---|---|---|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | valor tasado MIVAU municipal | MUN_PRECIO_ANUAL__bosque_bootstrap_bayesiano | ecm_v1 | 4.1270 | 3.9328 | 1.0494 | 0.8959 | 0.8630 | 0.7549 | no distinguible |
| PROV_PRECIO_ANUAL | valor tasado MIVAU | PROV_PRECIO_ANUAL__random_forest | ecm_v1 | 2.4782 | 2.8178 | 0.8795 | 0.0025 | 0.1308 | 0.0005 | predice mejor que la base mas exigente (fragil: DM por periodo no significativo) |
| PROV_PRECIO_ANUAL_REGISTRADORES | Registradores (robustez) | PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano | ecm_v1 | 4.6995 | 4.6759 | 1.0050 | 0.5710 | 0.5549 | 0.5435 | no distinguible |
| PROV_PRECIO_TRIM | valor tasado MIVAU | PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano | ar_factor_fac | 1.6140 | 1.8174 | 0.8881 | 0.0000 | 0.0000 | 0.0005 | predice mejor que la base mas exigente |
| PROV_VOL_ANUAL |  | PROV_VOL_ANUAL__bosque_bootstrap_bayesiano | ecm_v1 | 13.0447 | 13.6984 | 0.9523 | 0.1190 | 0.3303 | 0.1665 | no distinguible |
| PROV_VOL_TRIM |  | PROV_VOL_TRIM__bosque_bootstrap_bayesiano | ar_factor_fac | 11.3011 | 16.7389 | 0.6751 | 0.0000 | 0.0452 | 0.0005 | predice mejor que la base mas exigente |
| alq_distrito |  | alquiler_distrito_gb | ecm_v1 | 5.6027 | 6.1217 | 0.9152 | 0.0000 | 0.0284 | 0.0059 | predice mejor que la base mas exigente |
| alq_municipio |  | alquiler_municipio_gb | ar_factor_fac | 5.0543 | 5.4319 | 0.9305 | 0.0000 | 0.0289 | 0.0015 | predice mejor que la base mas exigente |
| alq_provincia |  | alquiler_provincia_gb | ar_factor_fac | 1.6066 | 2.2031 | 0.7292 | 0.0000 | 0.0262 | 0.0015 | predice mejor que la base mas exigente |

Sensibilidad (revision R-06): Holm sobre las 9 tareas del grupo espacial.

| tarea | p_dm_hln_holm_9tareas | p_perm_holm_9tareas | clase_holm_9tareas |
|---|---|---|---|
| MUN_PRECIO_ANUAL | 1.0000 | 1.0000 | no distinguible |
| PROV_PRECIO_ANUAL | 0.0102 | 0.0044 | predice mejor que la base mas exigente |
| PROV_PRECIO_ANUAL_REGISTRADORES | 1.0000 | 1.0000 | no distinguible |
| PROV_PRECIO_TRIM | 0.0000 | 0.0044 | predice mejor que la base mas exigente |
| PROV_VOL_ANUAL | 0.3570 | 0.4995 | no distinguible |
| PROV_VOL_TRIM | 0.0000 | 0.0044 | predice mejor que la base mas exigente |
| alq_distrito | 0.0000 | 0.0234 | predice mejor que la base mas exigente |
| alq_municipio | 0.0002 | 0.0088 | predice mejor que la base mas exigente |
| alq_provincia | 0.0002 | 0.0088 | predice mejor que la base mas exigente |

## Otros grupos (mejor modelo espacial contra su base exigente espacial)

| tarea | ratio_temporal | clase_temporal | ratio_conjunta | clase_conjunta | ratio_total | clase_total |
|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | 1.0200 | no distinguible | 1.1364 | no distinguible | 1.0562 | peor |
| PROV_PRECIO_ANUAL | 0.8562 | predice mejor que la base mas exigente | 0.8219 | predice mejor que la base mas exigente | 0.8539 | predice mejor que la base mas exigente |
| PROV_PRECIO_ANUAL_REGISTRADORES | 1.0039 | no distinguible | 0.9043 | no distinguible | 0.9876 | no distinguible |
| PROV_PRECIO_TRIM | 1.0480 | peor | 0.9122 | predice mejor que la base mas exigente | 0.9472 | no distinguible |
| PROV_VOL_ANUAL | 0.6596 | predice mejor que la base mas exigente | 0.5710 | predice mejor que la base mas exigente | 0.8723 | predice mejor que la base mas exigente |
| PROV_VOL_TRIM | 1.2329 | peor | 1.3057 | peor | 0.7821 | no distinguible |
| alq_distrito | 0.9609 | predice mejor que la base mas exigente | 0.9285 | no distinguible | 0.9257 | predice mejor que la base mas exigente |
| alq_municipio | 0.8916 | predice mejor que la base mas exigente | 1.0200 | no distinguible | 0.9209 | predice mejor que la base mas exigente |
| alq_provincia | 0.8780 | no distinguible | 0.7899 | no distinguible | 0.7699 | predice mejor que la base mas exigente |

## Variante oraculo (factor del periodo objetivo, no conocible al predecir; solo informativa)

| tarea | base_oraculo | rmse_pct_base_oraculo | rmse_pct_modelo | ratio_vs_oraculo |
|---|---|---|---|---|
| MUN_PRECIO_ANUAL | twfe_ora | 3.8259 | 4.1270 | 1.0787 |
| PROV_PRECIO_ANUAL | ult_crec_nac_ora | 2.5749 | 2.4782 | 0.9624 |
| PROV_PRECIO_ANUAL_REGISTRADORES | twfe_ora | 4.8788 | 4.6995 | 0.9632 |
| PROV_PRECIO_TRIM | twfe_ora | 1.6231 | 1.6140 | 0.9944 |
| PROV_VOL_ANUAL | ult_crec_nac_ora | 7.5673 | 13.0447 | 1.7238 |
| PROV_VOL_TRIM | ar_factor_ora | 10.8911 | 11.3011 | 1.0376 |
| alq_distrito | twfe_ora | 5.8226 | 5.6027 | 0.9622 |
| alq_municipio | twfe_ora | 5.0853 | 5.0543 | 0.9939 |
| alq_provincia | ult_crec_nac_ora | 1.0446 | 1.6066 | 1.5379 |

## Referencias v6 (mejor M3 bate segun v6)

| tarea | rmse_pct_persistencia | rmse_pct_ar_unidad | rmse_pct_ecm_v1 | v6_m3_bate_persistencia | v6_m3_bate_ar | v6_m3_bate_ecm | n_modelos_m3_mejor_que_base | n_modelos_m3 |
|---|---|---|---|---|---|---|---|---|
| MUN_PRECIO_ANUAL | 6.3256 | 6.3256 | 3.9328 | True | True | False | 0 | 1 |
| PROV_PRECIO_ANUAL | 3.9638 | 3.9638 | 2.8178 | True | True | True | 1 | 1 |
| PROV_PRECIO_ANUAL_REGISTRADORES | 6.0321 | 6.0321 | 4.6759 | True | True | False | 0 | 1 |
| PROV_PRECIO_TRIM | 1.9310 | 1.9310 | 1.9310 | True | True | True | 1 | 1 |
| PROV_VOL_ANUAL | 15.8610 | 15.8610 | 13.6984 | True | True | False | 0 | 1 |
| PROV_VOL_TRIM | 18.4571 | 18.4571 | 18.4571 | True | True | True | 1 | 1 |
| alq_distrito | 6.9801 | 6.9801 | 6.1217 | True | True | True | 2 | 5 |
| alq_municipio | 6.5064 | 6.5064 | 6.1890 | True | True | True | 2 | 3 |
| alq_provincia | 4.2098 | 4.2098 | 3.3504 | True | True | True | 2 | 3 |
