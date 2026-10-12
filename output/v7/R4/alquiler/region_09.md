# Region 09, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.105 +0.009\,(\text{ln\_ipc\_alquiler}_{t-1} - [3.603\,\text{ln\_ocupados}_{t-1} + 4.596\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} -0.533\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.009; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 3.603, ln_pob_total = 4.596.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0158 | 0.0234 | -0.67 | 0.503 | 0.856 | [-0.0626, 0.0310] |
| d_ln_pob_total_L0 | -0.5327 | 0.2709 | -1.97 | 0.054 | 0.396 | [-1.0738, 0.0084] |
| d_ln_hip_importe | -0.0005 | 0.0015 | -0.32 | 0.754 | 0.937 | [-0.0034, 0.0025] |

Diagnosticos: BG_p = 0.019; BP_p = 0.039; JB_p = 0.000; RESET_p = 0.890; CUSUM_stat = 0.700; CUSUM_p = 0.711; VIF_max = 1.680; r2_adj = 0.378; phi_mitad1 = 0.008; phi_mitad2 = 0.103; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.001 | 0.000 | 0.000 | 0.024 | False |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.023 | 0.022 | 0.005 | 0.024 | False |
| 2014T1-2019T4 | residuo no explicado | -0.001 | 0.002 | 0.019 | 0.024 | False |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.025 | NA | NA | 0.024 | False |
| 2014T1-2019T4 | ECM propio: residuo | -0.001 | NA | NA | 0.024 | False |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.000 | -0.000 | -0.000 | -0.000 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.006 | 0.006 | 0.001 | -0.000 | True |
| 2020T1-2022T2 | residuo no explicado | -0.006 | -0.006 | -0.001 | -0.000 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | -0.000 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.000 | NA | NA | -0.000 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | -0.012 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.014 | 0.014 | 0.003 | -0.012 | True |
| 2022T3-ultimo | residuo no explicado | -0.029 | -0.026 | -0.015 | -0.012 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.012 | NA | NA | -0.012 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.000 | NA | NA | -0.012 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.012\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.052\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.529\,\text{d\_y\_L1} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.012; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.052.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0003 | 0.79 | 0.432 | 0.711 | [-0.0004, 0.0009] |
| d_y_L1 | 0.5294 | 0.0920 | 5.75 | 0.000 | 0.000 | [0.3458, 0.7129] |
| d_ln_hip_importe | -0.0004 | 0.0014 | -0.27 | 0.791 | 0.858 | [-0.0032, 0.0024] |

Diagnosticos: BG_p = 0.825; BP_p = 0.035; JB_p = 0.142; RESET_p = 0.541; CUSUM_stat = 0.867; CUSUM_p = 0.440; VIF_max = 1.000; r2_adj = 0.432; phi_mitad1 = 0.029; phi_mitad2 = 0.064; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.002 | -0.002 | -0.000 | 0.024 | True |
| 2014T1-2019T4 | residuo no explicado | 0.022 | 0.026 | 0.024 | 0.024 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.018 | NA | NA | 0.024 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.006 | NA | NA | 0.024 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.002 | -0.003 | -0.000 | -0.001 | True |
| 2020T1-2022T2 | residuo no explicado | -0.003 | 0.002 | -0.000 | -0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.003 | NA | NA | -0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.002 | NA | NA | -0.001 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.004 | 0.004 | 0.000 | -0.021 | True |
| 2022T3-ultimo | residuo no explicado | -0.017 | -0.024 | -0.021 | -0.021 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.012 | NA | NA | -0.021 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.009 | NA | NA | -0.021 | True |
