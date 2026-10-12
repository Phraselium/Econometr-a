# Region 16, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.000 +0.005\,(\text{ln\_ipc\_alquiler}_{t-1} - [-6.127\,\text{ln\_ocupados}_{t-1} + 7.205\,\text{ln\_pob\_total}_{t-1}]) +0.006\,\text{d\_ln\_ocupados\_L0} -0.193\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.005; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -6.127, ln_pob_total = 7.205.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0059 | 0.0120 | 0.49 | 0.625 | 0.867 | [-0.0181, 0.0298] |
| d_ln_pob_total_L0 | -0.1927 | 0.4091 | -0.47 | 0.639 | 0.867 | [-1.0097, 0.6242] |
| d_ln_hip_importe | 0.0007 | 0.0017 | 0.44 | 0.664 | 0.868 | [-0.0027, 0.0042] |

Diagnosticos: BG_p = 0.212; BP_p = 0.692; JB_p = 0.647; RESET_p = 0.403; CUSUM_stat = 0.764; CUSUM_p = 0.604; VIF_max = 1.119; r2_adj = 0.191; phi_mitad1 = 0.009; phi_mitad2 = -0.116; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.006 | -0.002 | -0.000 | -0.007 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.008 | 0.007 | 0.002 | -0.007 | True |
| 2014T1-2019T4 | residuo no explicado | -0.009 | -0.012 | -0.008 | -0.007 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.007 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | -0.007 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.002 | -0.001 | -0.000 | 0.003 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.005 | -0.005 | -0.001 | 0.003 | True |
| 2020T1-2022T2 | residuo no explicado | 0.010 | 0.008 | 0.004 | 0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | 0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.009 | NA | NA | 0.003 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.000 | 0.000 | 0.000 | -0.011 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.009 | -0.008 | -0.002 | -0.011 | False |
| 2022T3-ultimo | residuo no explicado | -0.002 | -0.003 | -0.009 | -0.011 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.010 | NA | NA | -0.011 | False |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | -0.011 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.002 -0.028\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.387\,\text{d\_y\_L1} +0.003\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.028; semivida = 24.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.013.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0002 | 0.0002 | 0.76 | 0.448 | 0.711 | [-0.0003, 0.0007] |
| d_y_L1 | 0.3866 | 0.1117 | 3.46 | 0.001 | 0.009 | [0.1637, 0.6094] |
| d_ln_hip_importe | 0.0031 | 0.0018 | 1.76 | 0.082 | 0.299 | [-0.0004, 0.0067] |

Diagnosticos: BG_p = 0.213; BP_p = 0.546; JB_p = 0.345; RESET_p = 0.085; CUSUM_stat = 0.957; CUSUM_p = 0.319; VIF_max = 1.000; r2_adj = 0.282; phi_mitad1 = -0.054; phi_mitad2 = 0.038; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.014 | 0.014 | 0.002 | -0.007 | True |
| 2014T1-2019T4 | residuo no explicado | 0.007 | -0.021 | -0.008 | -0.007 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.011 | NA | NA | -0.007 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.004 | NA | NA | -0.007 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.001 | -0.001 | -0.000 | 0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.000 | 0.003 | 0.002 | 0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.002 | NA | NA | 0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.004 | NA | NA | 0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.003 | 0.003 | 0.000 | -0.026 | True |
| 2022T3-ultimo | residuo no explicado | -0.023 | -0.029 | -0.026 | -0.026 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.014 | NA | NA | -0.026 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.012 | NA | NA | -0.026 | True |
