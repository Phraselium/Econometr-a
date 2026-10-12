# Region 14, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.011 -0.041\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.012\,\text{ln\_ocupados}_{t-1} + -1.146\,\text{ln\_pob\_total}_{t-1}]) -0.004\,\text{d\_ln\_ocupados\_L0} +0.373\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.041; semivida = 16.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.012, ln_pob_total = -1.146.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0036 | 0.0259 | -0.14 | 0.889 | 0.972 | [-0.0553, 0.0480] |
| d_ln_pob_total_L0 | 0.3727 | 0.9553 | 0.39 | 0.698 | 0.890 | [-1.5352, 2.2805] |
| d_ln_hip_importe | 0.0036 | 0.0036 | 1.01 | 0.318 | 0.706 | [-0.0036, 0.0109] |

Diagnosticos: BG_p = 0.046; BP_p = 0.011; JB_p = 0.000; RESET_p = 0.640; CUSUM_stat = 0.669; CUSUM_p = 0.762; VIF_max = 1.396; r2_adj = -0.021; phi_mitad1 = 0.134; phi_mitad2 = -0.458; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.003 | 0.001 | 0.000 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.019 | 0.018 | 0.004 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | -0.039 | -0.036 | -0.021 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.024 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.006 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.001 | 0.000 | 0.000 | -0.009 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.012 | 0.012 | 0.002 | -0.009 | True |
| 2020T1-2022T2 | residuo no explicado | -0.022 | -0.021 | -0.011 | -0.009 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.012 | NA | NA | -0.009 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.003 | NA | NA | -0.009 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.019 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.007 | 0.007 | 0.001 | -0.019 | True |
| 2022T3-ultimo | residuo no explicado | -0.025 | -0.025 | -0.020 | -0.019 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.013 | NA | NA | -0.019 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.006 | NA | NA | -0.019 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.006\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.073\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.294\,\text{d\_y\_L1} +0.006\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.006; semivida = 121.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.073.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0003 | -0.30 | 0.763 | 0.846 | [-0.0007, 0.0005] |
| d_y_L1 | 0.2942 | 0.1071 | 2.75 | 0.008 | 0.043 | [0.0806, 0.5079] |
| d_ln_hip_importe | 0.0065 | 0.0033 | 1.99 | 0.051 | 0.217 | [-0.0000, 0.0129] |

Diagnosticos: BG_p = 0.740; BP_p = 0.534; JB_p = 0.005; RESET_p = 0.520; CUSUM_stat = 0.603; CUSUM_p = 0.861; VIF_max = 1.000; r2_adj = 0.136; phi_mitad1 = -0.009; phi_mitad2 = -0.051; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.006 | -0.006 | -0.001 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | -0.023 | -0.011 | -0.017 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.019 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.004 | -0.004 | -0.000 | -0.008 | True |
| 2020T1-2022T2 | residuo no explicado | -0.012 | -0.004 | -0.008 | -0.008 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.008 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | -0.008 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.003 | 0.003 | 0.000 | -0.016 | True |
| 2022T3-ultimo | residuo no explicado | -0.012 | -0.019 | -0.016 | -0.016 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.015 | NA | NA | -0.016 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | -0.016 | True |
