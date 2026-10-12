# Region 05, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.005 -0.140\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.039\,\text{ln\_ocupados}_{t-1} + 0.157\,\text{ln\_pob\_total}_{t-1}]) +0.007\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.140; semivida = 4.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.039, ln_pob_total = 0.157.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0069 | 0.0064 | 1.08 | 0.282 | 0.706 | [-0.0058, 0.0196] |
| d_ln_pob_total_L0 | 0.2978 | 0.3545 | 0.84 | 0.404 | 0.792 | [-0.4101, 1.0058] |
| d_ln_hip_importe | -0.0000 | 0.0012 | -0.03 | 0.980 | 0.980 | [-0.0024, 0.0023] |

Diagnosticos: BG_p = 0.188; BP_p = 0.546; JB_p = 0.543; RESET_p = 0.118; CUSUM_stat = 0.591; CUSUM_p = 0.876; VIF_max = 2.083; r2_adj = 0.270; phi_mitad1 = -0.280; phi_mitad2 = -0.238; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.009 | 0.003 | 0.000 | 0.008 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.024 | 0.023 | 0.005 | 0.008 | True |
| 2014T1-2019T4 | residuo no explicado | -0.026 | -0.018 | 0.003 | 0.008 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.003 | NA | NA | 0.008 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.004 | NA | NA | 0.008 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.011 | 0.003 | 0.000 | 0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.003 | 0.003 | 0.001 | 0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.012 | -0.005 | 0.001 | 0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.004 | NA | NA | 0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | 0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.006 | 0.002 | 0.000 | 0.006 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.004 | 0.004 | 0.001 | 0.006 | True |
| 2022T3-ultimo | residuo no explicado | -0.004 | 0.000 | 0.005 | 0.006 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.006 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.001 | NA | NA | 0.006 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.000 -0.105\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.001\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.140\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.105; semivida = 6.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.001.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0003 | 0.0001 | -2.28 | 0.026 | 0.120 | [-0.0005, -0.0000] |
| d_y_L1 | 0.1395 | 0.1180 | 1.18 | 0.241 | 0.534 | [-0.0958, 0.3748] |
| d_ln_hip_importe | -0.0007 | 0.0014 | -0.53 | 0.598 | 0.731 | [-0.0034, 0.0020] |

Diagnosticos: BG_p = 0.011; BP_p = 0.099; JB_p = 0.014; RESET_p = 0.655; CUSUM_stat = 1.217; CUSUM_p = 0.104; VIF_max = 1.000; r2_adj = 0.058; phi_mitad1 = -0.245; phi_mitad2 = -0.309; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.014 | -0.014 | -0.001 | 0.008 | True |
| 2014T1-2019T4 | residuo no explicado | -0.006 | 0.022 | 0.009 | 0.008 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.003 | NA | NA | 0.008 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.011 | NA | NA | 0.008 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.021 | -0.021 | -0.002 | 0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.019 | 0.023 | 0.004 | 0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.001 | NA | NA | 0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.001 | NA | NA | 0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.015 | -0.016 | -0.002 | 0.002 | True |
| 2022T3-ultimo | residuo no explicado | -0.014 | 0.017 | 0.003 | 0.002 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.001 | NA | NA | 0.002 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.001 | NA | NA | 0.002 | True |
