# Region 17, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.678 -0.099\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.149\,\text{ln\_ocupados}_{t-1} + 3.708\,\text{ln\_pob\_total}_{t-1}]) +0.015\,\text{d\_ln\_ocupados\_L0} -0.697\,\text{d\_ln\_pob\_total\_L0} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.099; semivida = 6.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.149, ln_pob_total = 3.708.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0155 | 0.0152 | 1.02 | 0.312 | 0.706 | [-0.0149, 0.0459] |
| d_ln_pob_total_L0 | -0.6975 | 0.3594 | -1.94 | 0.057 | 0.396 | [-1.4153, 0.0204] |
| d_ln_hip_importe | 0.0016 | 0.0011 | 1.44 | 0.154 | 0.523 | [-0.0006, 0.0038] |

Diagnosticos: BG_p = 0.049; BP_p = 0.109; JB_p = 0.000; RESET_p = 0.728; CUSUM_stat = 0.366; CUSUM_p = 0.999; VIF_max = 1.089; r2_adj = 0.260; phi_mitad1 = -0.079; phi_mitad2 = -0.055; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.002 | -0.001 | -0.000 | -0.042 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.002 | -0.002 | -0.000 | -0.042 | True |
| 2014T1-2019T4 | residuo no explicado | -0.038 | -0.040 | -0.042 | -0.042 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.043 | NA | NA | -0.042 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | -0.042 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.003 | -0.001 | -0.000 | 0.001 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.001 | 0.001 | 0.000 | 0.001 | True |
| 2020T1-2022T2 | residuo no explicado | 0.003 | 0.001 | 0.001 | 0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.003 | NA | NA | 0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | 0.001 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.009 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.004 | -0.004 | -0.001 | -0.009 | False |
| 2022T3-ultimo | residuo no explicado | -0.003 | -0.004 | -0.008 | -0.009 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.012 | NA | NA | -0.009 | False |
| 2022T3-ultimo | ECM propio: residuo | 0.003 | NA | NA | -0.009 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.014\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.015\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.105\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.014; semivida = 50.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.015.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0001 | 0.0002 | 0.62 | 0.537 | 0.731 | [-0.0003, 0.0006] |
| d_y_L1 | 0.1053 | 0.1182 | 0.89 | 0.376 | 0.685 | [-0.1304, 0.3410] |
| d_ln_hip_importe | 0.0018 | 0.0013 | 1.44 | 0.153 | 0.434 | [-0.0007, 0.0043] |

Diagnosticos: BG_p = 0.404; BP_p = 0.649; JB_p = 0.000; RESET_p = 0.653; CUSUM_stat = 0.558; CUSUM_p = 0.915; VIF_max = 1.000; r2_adj = 0.062; phi_mitad1 = 0.004; phi_mitad2 = -0.148; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.002 | 0.002 | 0.000 | -0.042 | True |
| 2014T1-2019T4 | residuo no explicado | -0.040 | -0.044 | -0.042 | -0.042 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.032 | NA | NA | -0.042 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.010 | NA | NA | -0.042 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.010 | 0.011 | 0.001 | 0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.012 | -0.009 | 0.001 | 0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.004 | NA | NA | 0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.006 | NA | NA | 0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.004 | 0.004 | 0.000 | -0.005 | True |
| 2022T3-ultimo | residuo no explicado | -0.002 | -0.009 | -0.005 | -0.005 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.004 | NA | NA | -0.005 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | -0.005 | True |
