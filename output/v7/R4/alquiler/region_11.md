# Region 11, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.044\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.239\,\text{ln\_ocupados}_{t-1} + 0.319\,\text{ln\_pob\_total}_{t-1}]) -0.023\,\text{d\_ln\_ocupados\_L0} +0.409\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.044; semivida = 15.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.239, ln_pob_total = 0.319.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0231 | 0.0154 | -1.50 | 0.138 | 0.510 | [-0.0539, 0.0077] |
| d_ln_pob_total_L0 | 0.4087 | 0.2737 | 1.49 | 0.140 | 0.510 | [-0.1378, 0.9553] |
| d_ln_hip_importe | -0.0004 | 0.0016 | -0.24 | 0.811 | 0.962 | [-0.0036, 0.0028] |

Diagnosticos: BG_p = 0.087; BP_p = 0.265; JB_p = 0.407; RESET_p = 0.268; CUSUM_stat = 0.828; CUSUM_p = 0.500; VIF_max = 1.662; r2_adj = 0.014; phi_mitad1 = -0.107; phi_mitad2 = -0.005; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.002 | -0.001 | -0.000 | -0.021 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.033 | -0.031 | -0.006 | -0.021 | True |
| 2014T1-2019T4 | residuo no explicado | 0.014 | 0.010 | -0.015 | -0.021 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.019 | NA | NA | -0.021 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | -0.021 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.004 | 0.001 | 0.000 | -0.007 | False |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.014 | -0.013 | -0.003 | -0.007 | False |
| 2020T1-2022T2 | residuo no explicado | 0.003 | 0.004 | -0.005 | -0.007 | False |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.002 | NA | NA | -0.007 | False |
| 2020T1-2022T2 | ECM propio: residuo | -0.005 | NA | NA | -0.007 | False |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.005 | -0.001 | -0.000 | 0.003 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.025 | -0.023 | -0.005 | 0.003 | True |
| 2022T3-ultimo | residuo no explicado | 0.032 | 0.027 | 0.008 | 0.003 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | 0.003 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.008 | NA | NA | 0.003 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.004\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.293\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.004; semivida = 156.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.016.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0002 | 1.83 | 0.071 | 0.278 | [-0.0000, 0.0008] |
| d_y_L1 | 0.2934 | 0.1051 | 2.79 | 0.007 | 0.043 | [0.0838, 0.5030] |
| d_ln_hip_importe | -0.0012 | 0.0015 | -0.81 | 0.419 | 0.711 | [-0.0041, 0.0017] |

Diagnosticos: BG_p = 0.970; BP_p = 0.851; JB_p = 0.228; RESET_p = 0.706; CUSUM_stat = 0.739; CUSUM_p = 0.646; VIF_max = 1.000; r2_adj = 0.102; phi_mitad1 = -0.085; phi_mitad2 = -0.079; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.008 | 0.008 | 0.001 | -0.021 | True |
| 2014T1-2019T4 | residuo no explicado | -0.013 | -0.030 | -0.022 | -0.021 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.021 | NA | NA | -0.021 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.001 | NA | NA | -0.021 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.014 | -0.015 | -0.002 | -0.008 | True |
| 2020T1-2022T2 | residuo no explicado | -0.022 | 0.007 | -0.006 | -0.008 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.009 | NA | NA | -0.008 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.001 | NA | NA | -0.008 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.004 | -0.004 | -0.000 | -0.009 | True |
| 2022T3-ultimo | residuo no explicado | -0.014 | -0.005 | -0.009 | -0.009 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.010 | NA | NA | -0.009 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.001 | NA | NA | -0.009 | True |
