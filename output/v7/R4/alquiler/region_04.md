# Region 04, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.033 -0.087\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.009\,\text{ln\_ocupados}_{t-1} + 0.812\,\text{ln\_pob\_total}_{t-1}]) +0.002\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.087; semivida = 7.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.009, ln_pob_total = 0.812.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0015 | 0.0033 | 0.46 | 0.646 | 0.867 | [-0.0050, 0.0081] |
| d_ln_pob_total_L0 | 0.2979 | 0.3344 | 0.89 | 0.376 | 0.768 | [-0.3700, 0.9657] |
| d_ln_hip_importe | 0.0002 | 0.0016 | 0.13 | 0.896 | 0.972 | [-0.0031, 0.0035] |

Diagnosticos: BG_p = 0.025; BP_p = 0.000; JB_p = 0.972; RESET_p = 0.182; CUSUM_stat = 0.505; CUSUM_p = 0.961; VIF_max = 1.688; r2_adj = 0.021; phi_mitad1 = -0.107; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.008 | 0.002 | 0.000 | 0.044 | False |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.046 | 0.043 | 0.009 | 0.044 | False |
| 2014T1-2019T4 | residuo no explicado | -0.010 | -0.002 | 0.034 | 0.044 | False |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.036 | NA | NA | 0.044 | False |
| 2014T1-2019T4 | ECM propio: residuo | 0.008 | NA | NA | 0.044 | False |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.003 | 0.001 | 0.000 | 0.013 | False |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.010 | 0.010 | 0.002 | 0.013 | False |
| 2020T1-2022T2 | residuo no explicado | -0.000 | 0.002 | 0.010 | 0.013 | False |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.011 | NA | NA | 0.013 | False |
| 2020T1-2022T2 | ECM propio: residuo | 0.002 | NA | NA | 0.013 | False |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.010 | -0.003 | -0.000 | 0.013 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.020 | 0.018 | 0.004 | 0.013 | False |
| 2022T3-ultimo | residuo no explicado | 0.004 | -0.002 | 0.010 | 0.013 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.017 | NA | NA | 0.013 | False |
| 2022T3-ultimo | ECM propio: residuo | -0.004 | NA | NA | 0.013 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.011\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.006\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.040\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.011; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.006.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0000 | 0.0001 | -0.57 | 0.567 | 0.731 | [-0.0002, 0.0001] |
| d_y_L1 | 0.0401 | 0.1220 | 0.33 | 0.743 | 0.842 | [-0.2033, 0.2835] |
| d_ln_hip_importe | 0.0006 | 0.0016 | 0.39 | 0.697 | 0.808 | [-0.0025, 0.0038] |

Diagnosticos: BG_p = 0.024; BP_p = 0.795; JB_p = 0.148; RESET_p = 0.409; CUSUM_stat = 0.513; CUSUM_p = 0.955; VIF_max = 1.000; r2_adj = -0.010; phi_mitad1 = 0.040; phi_mitad2 = -0.015; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.008 | -0.008 | -0.001 | 0.044 | True |
| 2014T1-2019T4 | residuo no explicado | 0.036 | 0.051 | 0.045 | 0.044 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.033 | NA | NA | 0.044 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.010 | NA | NA | 0.044 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.006 | 0.006 | 0.001 | 0.013 | True |
| 2020T1-2022T2 | residuo no explicado | 0.019 | 0.007 | 0.012 | 0.013 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.013 | NA | NA | 0.013 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.000 | NA | NA | 0.013 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.002 | -0.002 | -0.000 | 0.025 | True |
| 2022T3-ultimo | residuo no explicado | 0.023 | 0.026 | 0.025 | 0.025 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.027 | NA | NA | 0.025 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.002 | NA | NA | 0.025 | True |
