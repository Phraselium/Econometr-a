# Region 12, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.006 +0.014\,(\text{ln\_ipc\_alquiler}_{t-1} - [-1.212\,\text{ln\_ocupados}_{t-1} + -0.232\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.534\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.014; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.212, ln_pob_total = -0.232.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0010 | 0.0275 | -0.04 | 0.970 | 0.980 | [-0.0559, 0.0538] |
| d_ln_pob_total_L0 | 0.5337 | 0.4681 | 1.14 | 0.258 | 0.706 | [-0.4013, 1.4687] |
| d_ln_hip_importe | 0.0013 | 0.0019 | 0.64 | 0.521 | 0.858 | [-0.0026, 0.0051] |

Diagnosticos: BG_p = 0.001; BP_p = 0.006; JB_p = 0.000; RESET_p = 0.000; CUSUM_stat = 0.541; CUSUM_p = 0.931; VIF_max = 1.000; r2_adj = 0.058; phi_mitad1 = 0.170; phi_mitad2 = -0.338; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.004 | -0.001 | -0.000 | 0.014 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.022 | -0.021 | -0.004 | 0.014 | True |
| 2014T1-2019T4 | residuo no explicado | 0.040 | 0.036 | 0.018 | 0.014 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.018 | NA | NA | 0.014 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.004 | NA | NA | 0.014 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.003 | -0.001 | -0.000 | 0.005 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.008 | -0.008 | -0.002 | 0.005 | True |
| 2020T1-2022T2 | residuo no explicado | 0.015 | 0.013 | 0.007 | 0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.000 | NA | NA | 0.005 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.000 | -0.000 | -0.000 | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.016 | -0.015 | -0.003 | -0.002 | True |
| 2022T3-ultimo | residuo no explicado | 0.014 | 0.013 | 0.001 | -0.002 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.003 | NA | NA | -0.002 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.001 | NA | NA | -0.002 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.001 +0.031\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.027\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.386\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.031; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.027.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0004 | 0.0003 | -1.12 | 0.264 | 0.562 | [-0.0010, 0.0003] |
| d_y_L1 | 0.3862 | 0.0939 | 4.11 | 0.000 | 0.002 | [0.1989, 0.5736] |
| d_ln_hip_importe | 0.0014 | 0.0015 | 0.94 | 0.351 | 0.664 | [-0.0016, 0.0044] |

Diagnosticos: BG_p = 0.233; BP_p = 0.937; JB_p = 0.121; RESET_p = 0.733; CUSUM_stat = 0.622; CUSUM_p = 0.833; VIF_max = 1.000; r2_adj = 0.334; phi_mitad1 = 0.055; phi_mitad2 = -0.173; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.003 | 0.003 | 0.000 | 0.014 | True |
| 2014T1-2019T4 | residuo no explicado | 0.017 | 0.011 | 0.014 | 0.014 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.013 | NA | NA | 0.014 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | 0.014 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.008 | 0.008 | 0.001 | 0.005 | True |
| 2020T1-2022T2 | residuo no explicado | 0.013 | -0.003 | 0.004 | 0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.001 | NA | NA | 0.005 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.003 | -0.003 | -0.000 | -0.001 | True |
| 2022T3-ultimo | residuo no explicado | -0.003 | 0.002 | -0.000 | -0.001 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | -0.001 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.000 | NA | NA | -0.001 | True |
