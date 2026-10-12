# Region 13, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.023 +0.053\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.953\,\text{ln\_ocupados}_{t-1} + -0.696\,\text{ln\_pob\_total}_{t-1}]) -0.008\,\text{d\_ln\_ocupados\_L0} +0.780\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.053; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.953, ln_pob_total = -0.696.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0077 | 0.0153 | -0.51 | 0.614 | 0.867 | [-0.0382, 0.0228] |
| d_ln_pob_total_L0 | 0.7799 | 0.3192 | 2.44 | 0.017 | 0.274 | [0.1424, 1.4174] |
| d_ln_hip_importe | 0.0011 | 0.0020 | 0.55 | 0.581 | 0.867 | [-0.0029, 0.0052] |

Diagnosticos: BG_p = 0.013; BP_p = 0.618; JB_p = 0.819; RESET_p = 0.401; CUSUM_stat = 0.701; CUSUM_p = 0.709; VIF_max = 2.046; r2_adj = 0.345; phi_mitad1 = 0.035; phi_mitad2 = -0.060; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.003 | 0.001 | 0.000 | 0.007 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.037 | 0.034 | 0.007 | 0.007 | True |
| 2014T1-2019T4 | residuo no explicado | -0.033 | -0.029 | -0.001 | 0.007 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.004 | NA | NA | 0.007 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.003 | NA | NA | 0.007 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.002 | -0.001 | -0.000 | -0.005 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.005 | 0.005 | 0.001 | -0.005 | True |
| 2020T1-2022T2 | residuo no explicado | -0.008 | -0.009 | -0.006 | -0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.007 | NA | NA | -0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.002 | NA | NA | -0.005 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.004 | 0.001 | 0.000 | 0.013 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.021 | 0.020 | 0.004 | 0.013 | True |
| 2022T3-ultimo | residuo no explicado | -0.012 | -0.008 | 0.009 | 0.013 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.018 | NA | NA | 0.013 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.005 | NA | NA | 0.013 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 -0.016\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.042\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.460\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.016; semivida = 43.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.042.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0002 | 1.66 | 0.102 | 0.348 | [-0.0001, 0.0008] |
| d_y_L1 | 0.4601 | 0.1003 | 4.59 | 0.000 | 0.000 | [0.2602, 0.6601] |
| d_ln_hip_importe | 0.0017 | 0.0016 | 1.08 | 0.285 | 0.582 | [-0.0015, 0.0050] |

Diagnosticos: BG_p = 0.913; BP_p = 0.526; JB_p = 0.840; RESET_p = 0.388; CUSUM_stat = 0.485; CUSUM_p = 0.973; VIF_max = 1.000; r2_adj = 0.523; phi_mitad1 = 0.020; phi_mitad2 = -0.050; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.002 | 0.002 | 0.000 | 0.007 | True |
| 2014T1-2019T4 | residuo no explicado | 0.008 | 0.005 | 0.006 | 0.007 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.007 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.002 | NA | NA | 0.007 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.007 | 0.008 | 0.001 | -0.005 | True |
| 2020T1-2022T2 | residuo no explicado | 0.003 | -0.012 | -0.006 | -0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.002 | NA | NA | -0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | -0.005 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.002 | -0.003 | -0.000 | 0.016 | True |
| 2022T3-ultimo | residuo no explicado | 0.014 | 0.019 | 0.017 | 0.016 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.017 | NA | NA | 0.016 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | 0.016 | True |
