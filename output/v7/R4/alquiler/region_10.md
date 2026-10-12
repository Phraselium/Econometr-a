# Region 10, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.138 -0.147\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.072\,\text{ln\_ocupados}_{t-1} + 0.979\,\text{ln\_pob\_total}_{t-1}]) -0.012\,\text{d\_ln\_ocupados\_L0} +0.601\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.147; semivida = 4.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.072, ln_pob_total = 0.979.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0120 | 0.0154 | -0.78 | 0.438 | 0.823 | [-0.0428, 0.0187] |
| d_ln_pob_total_L0 | 0.6007 | 0.3513 | 1.71 | 0.092 | 0.396 | [-0.1009, 1.3024] |
| d_ln_hip_importe | -0.0019 | 0.0025 | -0.76 | 0.452 | 0.823 | [-0.0070, 0.0031] |

Diagnosticos: BG_p = 0.000; BP_p = 0.019; JB_p = 0.721; RESET_p = 0.205; CUSUM_stat = 0.742; CUSUM_p = 0.640; VIF_max = 1.715; r2_adj = 0.239; phi_mitad1 = -0.334; phi_mitad2 = -0.116; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | 0.006 | False |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.005 | 0.005 | 0.001 | 0.006 | False |
| 2014T1-2019T4 | residuo no explicado | -0.002 | 0.000 | 0.005 | 0.006 | False |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.009 | NA | NA | 0.006 | False |
| 2014T1-2019T4 | ECM propio: residuo | -0.003 | NA | NA | 0.006 | False |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | 0.010 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.013 | 0.012 | 0.002 | 0.010 | True |
| 2020T1-2022T2 | residuo no explicado | -0.005 | -0.003 | 0.007 | 0.010 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.003 | NA | NA | 0.010 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.007 | NA | NA | 0.010 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | 0.021 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.027 | 0.025 | 0.005 | 0.021 | False |
| 2022T3-ultimo | residuo no explicado | -0.008 | -0.005 | 0.016 | 0.021 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.025 | NA | NA | 0.021 | False |
| 2022T3-ultimo | ECM propio: residuo | -0.003 | NA | NA | 0.021 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.019\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.407\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.019; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.014.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0002 | -0.52 | 0.602 | 0.731 | [-0.0006, 0.0003] |
| d_y_L1 | 0.4068 | 0.1162 | 3.50 | 0.001 | 0.009 | [0.1752, 0.6385] |
| d_ln_hip_importe | -0.0018 | 0.0024 | -0.74 | 0.460 | 0.711 | [-0.0066, 0.0030] |

Diagnosticos: BG_p = 0.009; BP_p = 0.325; JB_p = 0.510; RESET_p = 0.509; CUSUM_stat = 0.570; CUSUM_p = 0.902; VIF_max = 1.000; r2_adj = 0.345; phi_mitad1 = -0.060; phi_mitad2 = 0.022; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.008 | -0.009 | -0.001 | 0.006 | True |
| 2014T1-2019T4 | residuo no explicado | -0.002 | 0.015 | 0.007 | 0.006 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.006 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | 0.006 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.002 | -0.003 | -0.000 | 0.010 | True |
| 2020T1-2022T2 | residuo no explicado | 0.008 | 0.013 | 0.011 | 0.010 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.014 | NA | NA | 0.010 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | 0.010 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.002 | 0.002 | 0.000 | 0.038 | True |
| 2022T3-ultimo | residuo no explicado | 0.039 | 0.036 | 0.037 | 0.038 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.033 | NA | NA | 0.038 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.005 | NA | NA | 0.038 | True |
