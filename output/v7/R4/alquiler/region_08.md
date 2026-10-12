# Region 08, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.011 -0.132\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.071\,\text{ln\_ocupados}_{t-1} + 0.828\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.346\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.132; semivida = 4.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.071, ln_pob_total = 0.828.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0008 | 0.0159 | -0.05 | 0.959 | 0.980 | [-0.0326, 0.0310] |
| d_ln_pob_total_L0 | 0.3458 | 0.1846 | 1.87 | 0.066 | 0.396 | [-0.0228, 0.7145] |
| d_ln_hip_importe | 0.0001 | 0.0013 | 0.09 | 0.932 | 0.980 | [-0.0025, 0.0027] |

Diagnosticos: BG_p = 0.191; BP_p = 0.052; JB_p = 0.231; RESET_p = 0.715; CUSUM_stat = 0.564; CUSUM_p = 0.908; VIF_max = 1.009; r2_adj = 0.110; phi_mitad1 = -0.413; phi_mitad2 = -0.340; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.000 | 0.000 | 0.000 | -0.016 | False |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.021 | -0.020 | -0.004 | -0.016 | False |
| 2014T1-2019T4 | residuo no explicado | 0.005 | 0.004 | -0.012 | -0.016 | False |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.022 | NA | NA | -0.016 | False |
| 2014T1-2019T4 | ECM propio: residuo | 0.006 | NA | NA | -0.016 | False |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.007 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.003 | 0.003 | 0.001 | -0.007 | True |
| 2020T1-2022T2 | residuo no explicado | -0.009 | -0.010 | -0.008 | -0.007 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.007 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.007 | NA | NA | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | 0.006 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.004 | 0.004 | 0.001 | 0.006 | False |
| 2022T3-ultimo | residuo no explicado | 0.003 | 0.003 | 0.006 | 0.006 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.004 | NA | NA | 0.006 | False |
| 2022T3-ultimo | ECM propio: residuo | 0.002 | NA | NA | 0.006 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.021\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.004\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.154\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.021; semivida = 33.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0002 | 0.0002 | -0.84 | 0.403 | 0.708 | [-0.0006, 0.0003] |
| d_y_L1 | 0.1538 | 0.1215 | 1.27 | 0.210 | 0.509 | [-0.0885, 0.3960] |
| d_ln_hip_importe | -0.0007 | 0.0014 | -0.53 | 0.600 | 0.731 | [-0.0036, 0.0021] |

Diagnosticos: BG_p = 0.339; BP_p = 0.008; JB_p = 0.259; RESET_p = 0.119; CUSUM_stat = 0.731; CUSUM_p = 0.660; VIF_max = 1.000; r2_adj = -0.018; phi_mitad1 = -0.117; phi_mitad2 = -0.070; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.006 | -0.006 | -0.001 | -0.016 | True |
| 2014T1-2019T4 | residuo no explicado | -0.022 | -0.010 | -0.015 | -0.016 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.008 | NA | NA | -0.016 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.008 | NA | NA | -0.016 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.006 | 0.006 | 0.001 | -0.007 | True |
| 2020T1-2022T2 | residuo no explicado | -0.001 | -0.013 | -0.008 | -0.007 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.007 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.007 | NA | NA | -0.007 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.001 | -0.001 | -0.000 | 0.008 | True |
| 2022T3-ultimo | residuo no explicado | 0.007 | 0.008 | 0.008 | 0.008 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.000 | NA | NA | 0.008 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.007 | NA | NA | 0.008 | True |
