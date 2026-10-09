# F3 - Inmigracion y precios (P2): resumen

Todo se reproduce con `python3 src/f3_inmigracion.py` (semilla 20261009, sin red). Tablas CSV/MD en `output/f3/`; registro de busqueda en `output/registro_busqueda_f3.csv`.

## Diseno
- x_ct = (pob_extranj_ct - pob_extranj_c,t-1)/pob_total_c,t-1. Coeficiente = variacion % del precio (Delta ln x 100) por cada 1 punto porcentual de poblacion que llega en el ano (flujo del 1 % de la poblacion).
- Instrumento (Card 2001): z_ct = sum_g s_cg,2002 * (dP_g,t)_{-c} / pob_total_c,t-1, cuotas fijas 2002, flujo nacional del grupo sin la CCAA c (leave-one-out). Grupos (coherentes en el tiempo; Europa = `pob_europa_sin_espana`, no UE28/UE27): europa (sin Espana), africa, america (sud+centro/Caribe+norte), asia, otros (oceania+apatridas). Suman `pob_extranj` (dif. max 0,02 %).
- FE CCAA + FE anio (principal) y + tendencias lineales por CCAA (robustez). EE cluster CCAA (17), p con t(16); wild cluster bootstrap restringido (Webb, 9.999; para 2SLS version WRE de Davidson-MacKinnon); EE Driscoll-Kraay (L=2) como robustez.

## Tabla principal (FE CCAA + FE anio; misma muestra OLS/2SLS)

| resultado        | spec   | est   |   n |    coef |   EE_cluster |   p_cluster |   p_WCB_restr |   EE_DK |   F_1a_etapa |
|:-----------------|:-------|:------|----:|--------:|-------------:|------------:|--------------:|--------:|-------------:|
| IPV (precio)     | FE     | OLS   | 306 | -0.4538 |       0.5027 |    0.38     |      0.3847   | 0.7677  |       nan    |
| IPV (precio)     | FE     | 2SLS  | 306 | -1.615  |       1.078  |    0.1538   |      0.2097   | 0.8157  |        17.87 |
| valor tasado     | FE     | OLS   | 386 |  0.3608 |       0.7163 |    0.6213   |      0.6225   | 0.5335  |       nan    |
| valor tasado     | FE     | 2SLS  | 386 | -0.8753 |       0.9519 |    0.3715   |      0.4885   | 0.7657  |        53.22 |
| alquiler SERPAVI | FE     | OLS   | 198 |  1.217  |       0.3368 |    0.002556 |      0.006601 | 0.4451  |       nan    |
| alquiler SERPAVI | FE     | 2SLS  | 198 |  0.5536 |       0.8126 |    0.5061   |      0.498    | 0.5631  |        10.63 |
| IPC alquiler     | FE     | OLS   | 391 |  0.5341 |       0.1674 |    0.005682 |      0.0044   | 0.05724 |       nan    |
| IPC alquiler     | FE     | 2SLS  | 391 |  0.4366 |       0.2935 |    0.1563   |      0.1194   | 0.211   |        54.36 |

### Robustez (tendencias por CCAA, control ocupados, rezago, sin COVID)

| resultado        | spec                  | est   |   n |     coef |   EE_cluster |   p_cluster |   p_WCB_restr |   EE_DK |   F_1a_etapa |
|:-----------------|:----------------------|:------|----:|---------:|-------------:|------------:|--------------:|--------:|-------------:|
| IPV (precio)     | FE+tend               | OLS   | 306 | -1.001   |       0.6331 |   0.1334    |      0.1365   | 0.6102  |      nan     |
| IPV (precio)     | FE+tend               | 2SLS  | 306 | -2.59    |       1.249  |   0.05462   |      0.07221  | 0.6087  |       21.78  |
| IPV (precio)     | FE+ctrl d_ln_ocupados | OLS   | 306 | -0.447   |       0.5174 |   0.4004    |      0.4118   | 0.7762  |      nan     |
| IPV (precio)     | FE+ctrl d_ln_ocupados | 2SLS  | 306 | -1.723   |       1.052  |   0.121     |      0.1887   | 0.8274  |       19.72  |
| IPV (precio)     | FE, x_t y x_t-1       | OLS   | 306 |  1.183   |       0.4755 |   0.02426   |    nan        | 0.9404  |      nan     |
| IPV (precio)     | FE, x_t y x_t-1       | OLS   | 306 | -2.157   |       0.8923 |   0.02797   |    nan        | 0.6991  |      nan     |
| IPV (precio)     | FE, x_t y x_t-1       | 2SLS  | 306 |  1.804   |       1.003  |   0.09085   |    nan        | 0.9788  |        8.902 |
| IPV (precio)     | FE, x_t y x_t-1       | 2SLS  | 306 | -3.459   |       1.342  |   0.02029   |    nan        | 1.199   |       12.01  |
| IPV (precio)     | FE sin 2020-2021      | OLS   | 272 | -0.4838  |       0.5305 |   0.3753    |      0.3652   | 0.8496  |      nan     |
| IPV (precio)     | FE sin 2020-2021      | 2SLS  | 272 | -1.773   |       1.111  |   0.1302    |      0.1804   | 0.8177  |       16.93  |
| valor tasado     | FE+tend               | OLS   | 386 |  1.034   |       0.5353 |   0.07132   |      0.08221  | 0.6376  |      nan     |
| valor tasado     | FE+tend               | 2SLS  | 386 |  0.2221  |       0.9258 |   0.8134    |      0.8065   | 0.9799  |       39.05  |
| valor tasado     | FE+ctrl d_ln_ocupados | OLS   | 386 |  0.2716  |       0.6823 |   0.6959    |      0.7049   | 0.5348  |      nan     |
| valor tasado     | FE+ctrl d_ln_ocupados | 2SLS  | 386 | -0.733   |       0.8969 |   0.4258    |      0.5328   | 0.7544  |       61.03  |
| valor tasado     | FE, x_t y x_t-1       | OLS   | 369 |  1.628   |       0.6223 |   0.01873   |    nan        | 1.032   |      nan     |
| valor tasado     | FE, x_t y x_t-1       | OLS   | 369 | -1.491   |       0.7889 |   0.07711   |    nan        | 0.7456  |      nan     |
| valor tasado     | FE, x_t y x_t-1       | 2SLS  | 369 |  3.518   |       0.8494 |   0.0007661 |    nan        | 2.068   |       29.97  |
| valor tasado     | FE, x_t y x_t-1       | 2SLS  | 369 | -4.347   |       1.107  |   0.001199  |    nan        | 1.557   |       26.03  |
| valor tasado     | FE sin 2020-2021      | OLS   | 352 |  0.4012  |       0.7422 |   0.5963    |      0.6083   | 0.5474  |      nan     |
| valor tasado     | FE sin 2020-2021      | 2SLS  | 352 | -0.8564  |       0.9838 |   0.3969    |      0.5048   | 0.7822  |       51.96  |
| alquiler SERPAVI | FE+tend               | OLS   | 198 |  0.9046  |       0.3384 |   0.01737   |      0.0197   | 0.5752  |      nan     |
| alquiler SERPAVI | FE+tend               | 2SLS  | 198 | -0.6967  |       0.5588 |   0.2316    |      0.2559   | 1.169   |       14.02  |
| alquiler SERPAVI | FE+ctrl d_ln_ocupados | OLS   | 198 |  1.208   |       0.3347 |   0.002577  |      0.006501 | 0.4473  |      nan     |
| alquiler SERPAVI | FE+ctrl d_ln_ocupados | 2SLS  | 198 |  0.593   |       0.7734 |   0.4552    |      0.434    | 0.5775  |       10.74  |
| alquiler SERPAVI | FE, x_t y x_t-1       | OLS   | 198 |  1.563   |       0.3597 |   0.0005768 |    nan        | 0.5459  |      nan     |
| alquiler SERPAVI | FE, x_t y x_t-1       | OLS   | 198 | -0.4874  |       0.3445 |   0.1776    |    nan        | 0.4409  |      nan     |
| alquiler SERPAVI | FE, x_t y x_t-1       | 2SLS  | 198 |  1.596   |       0.7431 |   0.04849   |    nan        | 0.885   |       11.64  |
| alquiler SERPAVI | FE, x_t y x_t-1       | 2SLS  | 198 | -1.221   |       0.3652 |   0.00444   |    nan        | 0.662   |        7.197 |
| alquiler SERPAVI | FE sin 2020-2021      | OLS   | 168 |  1.358   |       0.351  |   0.001513  |      0.005101 | 0.5022  |      nan     |
| alquiler SERPAVI | FE sin 2020-2021      | 2SLS  | 168 |  0.8142  |       0.7929 |   0.3208    |      0.2721   | 0.7076  |        8.854 |
| IPC alquiler     | FE+tend               | OLS   | 391 |  0.6431  |       0.1781 |   0.002345  |      0.0027   | 0.0731  |      nan     |
| IPC alquiler     | FE+tend               | 2SLS  | 391 |  0.6832  |       0.3022 |   0.03805   |      0.0128   | 0.1527  |       39.63  |
| IPC alquiler     | FE+ctrl d_ln_ocupados | OLS   | 391 |  0.533   |       0.1691 |   0.006172  |      0.006201 | 0.05942 |      nan     |
| IPC alquiler     | FE+ctrl d_ln_ocupados | 2SLS  | 391 |  0.4392  |       0.2868 |   0.1452    |      0.1137   | 0.2074  |       62.01  |
| IPC alquiler     | FE, x_t y x_t-1       | OLS   | 374 |  0.6087  |       0.1636 |   0.001859  |    nan        | 0.1067  |      nan     |
| IPC alquiler     | FE, x_t y x_t-1       | OLS   | 374 | -0.08968 |       0.1259 |   0.4864    |    nan        | 0.1361  |      nan     |
| IPC alquiler     | FE, x_t y x_t-1       | 2SLS  | 374 |  0.9532  |       0.3854 |   0.02499   |    nan        | 0.3854  |       28.52  |
| IPC alquiler     | FE, x_t y x_t-1       | 2SLS  | 374 | -0.5387  |       0.3096 |   0.1011    |    nan        | 0.2794  |       26.89  |
| IPC alquiler     | FE sin 2020-2021      | OLS   | 357 |  0.5334  |       0.172  |   0.006861  |      0.005601 | 0.05834 |      nan     |
| IPC alquiler     | FE sin 2020-2021      | 2SLS  | 357 |  0.4174  |       0.2934 |   0.1741    |      0.1476   | 0.2068  |       53.17  |

## Primera etapa (2SLS FE, instrumento unico z)

| resultado        |   n |   F_cluster |     pi |   EE_pi |   R2_parcial |   RF_coef |   RF_p_cluster |
|:-----------------|----:|------------:|-------:|--------:|-------------:|----------:|---------------:|
| IPV (precio)     | 306 |       17.87 | 0.5647 |  0.1336 |       0.3107 |   -0.9119 |         0.1902 |
| valor tasado     | 386 |       53.22 | 0.7649 |  0.1048 |       0.4841 |   -0.6695 |         0.3502 |
| alquiler SERPAVI | 198 |       10.63 | 0.5966 |  0.183  |       0.3323 |    0.3302 |         0.5129 |
| IPC alquiler     | 391 |       54.36 | 0.7621 |  0.1034 |       0.4784 |    0.3327 |         0.1873 |

F = Wald cluster-robusto (con un instrumento y un regresor endogeno equivale a Kleibergen-Paap rk F). No se implemento el F efectivo de Montiel Olea-Pflueger.

## Pesos de Rotemberg (Delta ln valor tasado) y 2SLS con cada grupo como instrumento unico

| grupo   |    alpha |   beta_g |   EE_g |    p_g |   sh_nacional_grupo_2002 |   corr_cuota_ln_p_tasado_0207 |   corr_cuota_tasa_ocup_2002 |   corr_cuota_ln_pob_total_2002 |   corr_cuota_sh_extranj_2002 |   corr_cuota_crec_p_tasado_0307 | alpha_neg   |
|:--------|---------:|---------:|-------:|-------:|-------------------------:|------------------------------:|----------------------------:|-------------------------------:|-----------------------------:|--------------------------------:|:------------|
| europa  | 0.428    |   -2.45  |  0.983 | 0.0239 |                  0.341   |                         0.277 |                       0.269 |                          0.76  |                        0.462 |                           0.321 | False       |
| africa  | 0.145    |    0.114 |  1.09  | 0.918  |                  0.206   |                         0.353 |                       0.32  |                          0.699 |                        0.374 |                           0.385 | False       |
| america | 0.392    |    0.513 |  1.24  | 0.684  |                  0.405   |                         0.532 |                       0.47  |                          0.634 |                        0.51  |                           0.241 | False       |
| asia    | 0.0358   |   -1.28  |  1.26  | 0.328  |                  0.0467  |                         0.503 |                       0.443 |                          0.673 |                        0.444 |                           0.192 | False       |
| otros   | 6.91e-05 |   33.6   | 38.3   | 0.394  |                  0.00109 |                         0.458 |                       0.277 |                          0.809 |                        0.392 |                           0.323 | False       |

(Mismo ejercicio para IPV, SERPAVI e IPC alquiler en `rotemberg_*.csv`.) Suma alpha_g * beta_g = 2SLS (comprobacion numerica incluida en el codigo).

## Pretendencias

| resultado    | test                                                    |   n |     coef |      EE |        p |   p_Holm_cuotas |
|:-------------|:--------------------------------------------------------|----:|---------:|--------:|---------:|----------------:|
| p_tasado     | seccion cruzada: media dln 2003-07 ~ zbar(2008-25), HC3 |  17 | -1.404   | 3.586   | 0.6953   |      nan        |
| p_tasado     | panel 2003-07 con FE anio, cluster CCAA                 |  85 | -1.404   | 3.331   | 0.6733   |      nan        |
| p_tasado     | cuota 2002 grupo europa (una a una), HC3                |  17 |  0.08713 | 0.05357 | 0.1039   |        0.5193   |
| p_tasado     | cuota 2002 grupo africa (una a una), HC3                |  17 |  0.08895 | 0.1142  | 0.4362   |        0.8725   |
| p_tasado     | cuota 2002 grupo america (una a una), HC3               |  17 |  0.05488 | 0.09425 | 0.5604   |        0.8725   |
| p_tasado     | cuota 2002 grupo asia (una a una), HC3                  |  17 |  0.03851 | 0.02747 | 0.1609   |        0.6436   |
| p_tasado     | cuota 2002 grupo otros (una a una), HC3                 |  17 |  0.09396 | 0.07212 | 0.1926   |        0.6436   |
| ipc_alquiler | seccion cruzada: media dln 2003-07 ~ zbar(2008-25), HC3 |  17 |  1.537   | 1.161   | 0.1854   |      nan        |
| ipc_alquiler | panel 2003-07 con FE anio, cluster CCAA                 |  85 |  1.537   | 1.067   | 0.1498   |      nan        |
| ipc_alquiler | cuota 2002 grupo europa (una a una), HC3                |  17 |  0.03616 | 0.02397 | 0.1314   |        0.2628   |
| ipc_alquiler | cuota 2002 grupo africa (una a una), HC3                |  17 |  0.04477 | 0.03104 | 0.1492   |        0.2628   |
| ipc_alquiler | cuota 2002 grupo america (una a una), HC3               |  17 |  0.04364 | 0.01546 | 0.004759 |        0.01428  |
| ipc_alquiler | cuota 2002 grupo asia (una a una), HC3                  |  17 |  0.03543 | 0.01197 | 0.003071 |        0.01228  |
| ipc_alquiler | cuota 2002 grupo otros (una a una), HC3                 |  17 |  0.05078 | 0.01557 | 0.001112 |        0.005559 |

## Sobreidentificacion (J de Hansen con 5 instrumentos por grupo) y AKM simplificado

| resultado        |   n |   F_conjunta_5IV |   J_Hansen |   J_df |    J_p |   coef_2SLS_5IV |   coef_2SLS_z_unico |   EE_AKM_simplificado_G5 |   p_AKM_t4 |
|:-----------------|----:|-----------------:|-----------:|-------:|-------:|----------------:|--------------------:|-------------------------:|-----------:|
| IPV (precio)     | 306 |            7.439 |      3.985 |      4 | 0.4081 |         -1.15   |             -1.615  |                   0.9136 |     0.1519 |
| valor tasado     | 386 |           29.29  |      6.711 |      4 | 0.152  |          0.5467 |             -0.8753 |                   0.982  |     0.4231 |
| alquiler SERPAVI | 198 |            6.404 |      7.545 |      4 | 0.1097 |          0.8987 |              0.5536 |                   0.413  |     0.2512 |
| IPC alquiler     | 391 |           28.61  |      5.526 |      4 | 0.2375 |          0.7166 |              0.4366 |                   0.3737 |     0.3076 |

Advertencia: con 17 clusters y 5 instrumentos el J (matriz de pesos con 17 vectores de momentos) tiene muy poca potencia y tiende a no rechazar; ademas los instrumentos por grupo estan fuertemente correlacionados. El AKM implementado es una version SIMPLIFICADA (scores agregados por grupo de shock, G=5 clusters, t(4)); no es el AKM completo (sin shocks anidados ni correccion por dependencia temporal de los shocks). Con 5 grupos el enfoque BHJ (2022, identificacion por shocks cuasi-aleatorios) no es viable: se necesitan muchos shocks independientes; los shocks de grupo son 5 series temporales muy persistentes.

## Canal comprador (compras de extranjeros)

| resultado                     | spec    | est   |   n |    coef |   EE_cluster |   p_cluster |   p_WCB_restr |   EE_DK |   F_1a_etapa |
|:------------------------------|:--------|:------|----:|--------:|-------------:|------------:|--------------:|--------:|-------------:|
| compras de extranjeros        | FE      | OLS   | 306 | -19.23  |        6.95  |    0.01376  |        0.0244 |   6.638 |       nan    |
| compras de extranjeros        | FE      | 2SLS  | 306 | -42.08  |       11.39  |    0.001969 |        0.0013 |  17.16  |        17.87 |
| compras de extranjeros        | FE+tend | OLS   | 306 | -21.35  |        8.544 |    0.02375  |        0.0355 |   8.253 |       nan    |
| compras de extranjeros        | FE+tend | 2SLS  | 306 | -43.56  |       12.85  |    0.003735 |        0.0018 |  18.32  |        21.78 |
| compras totales (comparacion) | FE      | OLS   | 304 |  -7.587 |        2.734 |    0.01353  |        0.0185 |   1.287 |       nan    |
| compras totales (comparacion) | FE      | 2SLS  | 304 | -17.67  |        5.069 |    0.003052 |        0.0024 |   3.453 |        17.85 |
| compras totales (comparacion) | FE+tend | OLS   | 304 |  -7.768 |        3.473 |    0.03993  |        0.0473 |   1.623 |       nan    |
| compras totales (comparacion) | FE+tend | 2SLS  | 304 | -17.3   |        5.451 |    0.005887 |        0.0031 |   3.449 |        21.08 |

## Desagregacion por nacionalidad (Europa sin Espana, Africa, America, Asia; 'otros' omitido)

| resultado    | grupo   | est              |   n |       coef |     EE |       p |   F_propio |
|:-------------|:--------|:-----------------|----:|-----------:|-------:|--------:|-----------:|
| valor tasado | europa  | OLS              | 386 |  -0.7835   |  1.321 | 0.5613  |    nan     |
| valor tasado | europa  | 2SLS             | 386 |  -8.204    |  3.879 | 0.05051 |     10.57  |
| valor tasado | europa  | OLS (grupo solo) | 386 |  -0.09906  |  1.231 | 0.9369  |    nan     |
| valor tasado | africa  | OLS              | 386 |  -0.6857   |  2.991 | 0.8216  |    nan     |
| valor tasado | africa  | 2SLS             | 386 |   8.573    |  6.126 | 0.1808  |    116.6   |
| valor tasado | africa  | OLS (grupo solo) | 386 |   0.4869   |  2.44  | 0.8443  |    nan     |
| valor tasado | america | OLS              | 386 |   2.032    |  1.547 | 0.2074  |    nan     |
| valor tasado | america | 2SLS             | 386 |   2.55     |  2.599 | 0.3412  |     15.92  |
| valor tasado | america | OLS (grupo solo) | 386 |   1.533    |  1.51  | 0.3253  |    nan     |
| valor tasado | asia    | OLS              | 386 |  -0.005378 |  8.947 | 0.9995  |    nan     |
| valor tasado | asia    | 2SLS             | 386 |  -6.21     | 19.54  | 0.7548  |     28.93  |
| valor tasado | asia    | OLS (grupo solo) | 386 |   2.011    |  5.067 | 0.6967  |    nan     |
| IPV (precio) | europa  | OLS              | 306 |   0.392    |  2.073 | 0.8524  |    nan     |
| IPV (precio) | europa  | 2SLS             | 306 |  -8.579    |  3.98  | 0.04667 |      4.796 |
| IPV (precio) | europa  | OLS (grupo solo) | 306 |  -0.1916   |  1.645 | 0.9087  |    nan     |
| IPV (precio) | africa  | OLS              | 306 |  -0.6616   |  3.882 | 0.8668  |    nan     |
| IPV (precio) | africa  | 2SLS             | 306 |   6.571    |  5.744 | 0.2695  |     13.29  |
| IPV (precio) | africa  | OLS (grupo solo) | 306 |  -2.235    |  3.139 | 0.4868  |    nan     |
| IPV (precio) | america | OLS              | 306 |  -0.02828  |  1.266 | 0.9825  |    nan     |
| IPV (precio) | america | 2SLS             | 306 |   0.9231   |  2.112 | 0.668   |      3.475 |
| IPV (precio) | america | OLS (grupo solo) | 306 |  -0.6348   |  0.833 | 0.4571  |    nan     |
| IPV (precio) | asia    | OLS              | 306 |  -8.928    |  4.147 | 0.04694 |    nan     |
| IPV (precio) | asia    | 2SLS             | 306 | -19.1      | 27.66  | 0.4997  |      6.175 |
| IPV (precio) | asia    | OLS (grupo solo) | 306 |  -9.375    |  3.745 | 0.02351 |    nan     |


| resultado    | grupo   |   F_cluster_4IV |   pi_propio |   EE_pi_propio |
|:-------------|:--------|----------------:|------------:|---------------:|
| valor tasado | europa  |          10.57  |      0.461  |         0.1299 |
| valor tasado | africa  |         116.6   |      1.108  |         0.1145 |
| valor tasado | america |          15.92  |      0.6208 |         0.1923 |
| valor tasado | asia    |          28.93  |      0.7248 |         0.1985 |
| IPV (precio) | europa  |           4.796 |      0.3565 |         0.1211 |
| IPV (precio) | africa  |          13.29  |      0.9068 |         0.2111 |
| IPV (precio) | america |           3.475 |      0.5732 |         0.2112 |
| IPV (precio) | asia    |           6.175 |      0.5623 |         0.2236 |

Si la F de primera etapa propia es < 10 el 2SLS por grupo no se interpreta; se lee solo el OLS como asociacion.

## Nacional (asociacion, sin identificacion)

### Proyecciones locales ln_ipv sobre d4_ln_pob_extranj (muestra comun 2008Q2-2024Q2)

|   h |     coef |   EE_HAC |      p |   n |
|----:|---------:|---------:|-------:|----:|
|   0 | -0.04119 |  0.04818 | 0.3926 |  65 |
|   1 | -0.06989 |  0.08732 | 0.4235 |  65 |
|   2 | -0.1015  |  0.1464  | 0.4882 |  65 |
|   3 | -0.09407 |  0.2317  | 0.6847 |  65 |
|   4 | -0.1214  |  0.3204  | 0.7049 |  65 |
|   5 | -0.09315 |  0.4143  | 0.8221 |  65 |
|   6 | -0.06688 |  0.4952  | 0.8926 |  65 |
|   7 | -0.0583  |  0.5625  | 0.9174 |  65 |
|   8 | -0.06734 |  0.6242  | 0.9141 |  65 |


### Proyecciones locales ln_ipc_alquiler sobre d4_ln_pob_extranj (muestra comun 2004Q2-2024Q2)

|   h |     coef |   EE_HAC |         p |   n |
|----:|---------:|---------:|----------:|----:|
|   0 | 0.006072 | 0.004173 | 0.1456    |  81 |
|   1 | 0.01116  | 0.008789 | 0.2043    |  81 |
|   2 | 0.0161   | 0.0125   | 0.1976    |  81 |
|   3 | 0.02884  | 0.01821  | 0.1132    |  81 |
|   4 | 0.05265  | 0.02575  | 0.04087   |  81 |
|   5 | 0.07927  | 0.03382  | 0.01909   |  81 |
|   6 | 0.1082   | 0.04145  | 0.009019  |  81 |
|   7 | 0.1441   | 0.04848  | 0.002967  |  81 |
|   8 | 0.1883   | 0.05522  | 0.0006508 |  81 |


Figura: `irf_nacional.png`. Variantes con d4_ln_pob_total y con el flujo Delta4/pob. total en `nacional_lp.csv`. La poblacion es semestral interpolada antes de 2021 y el IPV/EPA no estan desestacionalizados (dummies q2-q4).

### Flujo anual (N pequeno)

Muestra 2008-2024, N = 17: inferencia HAC(4) con N tan pequeno es poco fiable; solo orientativo.

| modelo        | var                 |     coef |   EE_HAC4 |         p |   n |   R2aj |
|:--------------|:--------------------|---------:|----------:|----------:|----:|-------:|
| A1_flujo_t    | tasa                | 10.65    |   2.972   | 0.0003397 |  17 | 0.3807 |
| A1_flujo_t    | emcr                | -0.0915  |   0.04055 | 0.02404   |  17 | 0.3807 |
| A2_flujo_t_l1 | tasa                | 18.08    |   5.401   | 0.000817  |  17 | 0.4658 |
| A2_flujo_t_l1 | tasa_l1             | -6.216   |   2.528   | 0.01395   |  17 | 0.4658 |
| A2_flujo_t_l1 | emcr                | -0.1417  |   0.05054 | 0.005053  |  17 | 0.4658 |
| A3_stock_t    | d_ln_pob_extranj    |  0.4311  |   0.2365  | 0.06837   |  17 | 0.182  |
| A3_stock_t    | emcr                |  0.04945 |   0.02894 | 0.08747   |  17 | 0.182  |
| A4_stock_t_l1 | d_ln_pob_extranj    |  1.204   |   0.3719  | 0.001202  |  17 | 0.3384 |
| A4_stock_t_l1 | d_ln_pob_extranj_l1 | -0.8499  |   0.3322  | 0.01052   |  17 | 0.3384 |
| A4_stock_t_l1 | emcr                |  0.04898 |   0.01535 | 0.001413  |  17 | 0.3384 |

### Separabilidad empleo-inmigracion

| muestra                                   |   n |    corr |   VIF_par |
|:------------------------------------------|----:|--------:|----------:|
| muestra completa                          |  94 |   0.441 |      1.24 |
| 2008Q1-2019Q4                             |  48 |   0.064 |      1    |
| 2013Q1-2026Q2                             |  54 |   0.174 |      1.03 |
| VIF (ocupados, extranj., d_tipo) completa |  93 | nan     |      1.42 |

## Conclusion P2 y nivel de evidencia

Regla: 'causal' solo si F>=10 Y pretendencias no significativas Y J no rechaza Y sobrevive al wild bootstrap; si no, 'asociacion'. (Pretendencias: minimo de los p de la seccion cruzada y el panel con zbar 2008-25 y de los p de Holm de las cuotas 2002 una a una; para IPV y valor tasado se usa la pretendencia del valor tasado; para alquiler, la del IPC alquiler.)

| resultado        | F_ge10   | pretend_no_signif   | J_no_rechaza   | sobrevive_WCB   |   p_pretend_min | nivel      |
|:-----------------|:---------|:--------------------|:---------------|:----------------|----------------:|:-----------|
| IPV (precio)     | True     | True                | True           | False           |        0.5193   | asociacion |
| valor tasado     | True     | True                | True           | False           |        0.5193   | asociacion |
| alquiler SERPAVI | True     | False               | True           | False           |        0.005559 | asociacion |
| IPC alquiler     | True     | False               | True           | False           |        0.005559 | asociacion |

- IPV (precio): OLS -0.454 (EE 0.503), 2SLS -1.615 (EE 1.078; p cluster 0.154, p WCB 0.210; F 17.9) = variacion % del precio por flujo del 1 % de la poblacion total.

- valor tasado: OLS 0.361 (EE 0.716), 2SLS -0.875 (EE 0.952; p cluster 0.371, p WCB 0.489; F 53.2) = variacion % del precio por flujo del 1 % de la poblacion total.

- alquiler SERPAVI: OLS 1.217 (EE 0.337), 2SLS 0.554 (EE 0.813; p cluster 0.506, p WCB 0.498; F 10.6) = variacion % del precio por flujo del 1 % de la poblacion total.

- IPC alquiler: OLS 0.534 (EE 0.167), 2SLS 0.437 (EE 0.293; p cluster 0.156, p WCB 0.119; F 54.4) = variacion % del precio por flujo del 1 % de la poblacion total.


Comparabilidad (docs/literatura.md): Saiz (2007, EE. UU.): entrada = 1 % de la poblacion -> alquileres y valores ~ +1 %. Sa (2015, RU, version de trabajo IZA DP 5893): -1,6 % por 1 % de poblacion. Gonzalez y Ortega (2013, Espana 1998-2008): flujo medio del 17 % de la poblacion en edad de trabajar -> precios ~ +52 % (cociente simple ~ 3 puntos % por punto de flujo; derivado aqui, denominador distinto: poblacion en edad de trabajar, no comparable 1 a 1). Nuestras elasticidades (variacion % del precio por 1 % de la poblacion total que llega en el ano) son de corto plazo (anual, contemporaneas) y con intervalos que incluyen tanto +1 como valores negativos en precio; en alquiler (IPC) las estimaciones son positivas y del orden de 0,4-0,7.


## Busqueda de especificaciones
Especificaciones registradas en F3: **149** (149 con p de interes). Correccion de Holm/Bonferroni sobre TODAS ellas en `correccion_busqueda.csv`. Para las 4 estimaciones 2SLS principales (FE) el p-valor del wild bootstrap y el ajustado:

| modelo               |    coef |      p |   p_holm |   p_bonferroni |
|:---------------------|--------:|-------:|---------:|---------------:|
| PAN_ipv_FE_2SLS      | -1.615  | 0.2097 |        1 |              1 |
| PAN_p_tasado_FE_2SLS | -0.8753 | 0.4885 |        1 |              1 |
| PAN_serpavi_FE_2SLS  |  0.5536 | 0.498  |        1 |              1 |
| PAN_ipc_alq_FE_2SLS  |  0.4366 | 0.1194 |        1 |              1 |

La mayoria de filas son robusteces/diagnosticos no independientes; la correccion sobre todas es muy conservadora. RMSE fuera de muestra no aplica en F3 (columna vacia).

## Problemas abiertos
- Canal comprador: el coeficiente sobre compras de extranjeros es NEGATIVO y muy grande (OLS y 2SLS, tambien en compras totales); implausible como efecto causal. Probable artefacto de la cobertura/serie de `trans_extranjeros` (2007 como nivel de partida y caida posterior) y de la correlacion entre ciclo local y variacion de poblacion; leer solo como asociacion y revisar la serie antes de usar.
- El IPV por CCAA no da efecto distinguible de cero ni en OLS ni en 2SLS; el unico resultado robusto es la asociacion positiva con el IPC de alquiler (OLS y 2SLS similares), pero las pretendencias por cuotas del IPC alquiler 2003-07 son significativas (America, Asia, otros), lo que impide leerlo como causal.
- 17 clusters: inferencia cluster y J de Hansen poco fiables; el wild bootstrap lo mitiga solo en parte.
- Exclusion del instrumento: la historia de asentamiento (cuotas 2002) puede correlacionarse con demanda local (burbuja inmobiliaria 2002-07, turismo/retirados en la costa) y los flujos de grupo se mueven por el ciclo nacional comun; los FE de anio absorben lo comun, no lo heterogeneo. Ver pretendencias y Rotemberg.
- Solo 5 grupos (de hecho 4 relevantes): imposible aplicar BHJ; AKM solo simplificado.
- x_ct mide variacion del stock padronal (incluye nacionalizaciones, cambios de padron y regularizaciones); no es flujo migratorio bruto. Las nacionalizaciones mueven personas de 'extranjero' a 'espanol'.
- IPV por CCAA solo desde 2007 (resultados 2008+), SERPAVI 2011-2024 con huecos (Navarra, Pais Vasco: N desequilibrado), valor tasado de Navarra falta 2015-18.
- El efecto sobre el precio en un ano contemporaneo no recoge ajustes de oferta a medio plazo; el rezago de x se incluye solo como robustez.
- Sin variable de paro por CCAA: las correlaciones de cuotas usan tasa de ocupados/poblacion 2002.
- No se implemento F efectivo de Montiel Olea-Pflueger.
- Panel nacionalidad: 2SLS con 4 endogenas y 4 instrumentos muy correlacionados, F condicional (Sanderson-Windmeijer) no implementado; se muestra F conjunta.
