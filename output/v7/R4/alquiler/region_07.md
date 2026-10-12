# Region 07, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.002 -0.007\,(\text{ln\_ipc\_alquiler}_{t-1} - [8.376\,\text{ln\_ocupados}_{t-1} + -6.155\,\text{ln\_pob\_total}_{t-1}]) +0.039\,\text{d\_ln\_ocupados\_L0} +0.826\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.007; semivida = 102.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 8.376, ln_pob_total = -6.155.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0387 | 0.0168 | 2.30 | 0.025 | 0.274 | [0.0051, 0.0723] |
| d_ln_pob_total_L0 | 0.8256 | 0.3630 | 2.27 | 0.026 | 0.274 | [0.1006, 1.5507] |
| d_ln_hip_importe | -0.0003 | 0.0014 | -0.21 | 0.833 | 0.965 | [-0.0030, 0.0024] |

Diagnosticos: BG_p = 0.001; BP_p = 0.273; JB_p = 0.434; RESET_p = 0.300; CUSUM_stat = 0.509; CUSUM_p = 0.958; VIF_max = 1.010; r2_adj = 0.372; phi_mitad1 = -0.025; phi_mitad2 = -0.117; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.003 | -0.001 | -0.000 | -0.008 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.042 | -0.040 | -0.008 | -0.008 | True |
| 2014T1-2019T4 | residuo no explicado | 0.037 | 0.032 | -0.000 | -0.008 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.007 | NA | NA | -0.008 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | -0.008 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.002 | -0.000 | -0.000 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.014 | -0.013 | -0.003 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.014 | 0.012 | 0.001 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.001 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.013 | -0.013 | -0.003 | -0.007 | True |
| 2022T3-ultimo | residuo no explicado | 0.008 | 0.006 | -0.004 | -0.007 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | -0.007 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | -0.007 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.001 -0.029\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.025\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.331\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.029; semivida = 23.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.025.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0002 | 0.0002 | -0.98 | 0.332 | 0.652 | [-0.0007, 0.0003] |
| d_y_L1 | 0.3312 | 0.1136 | 2.92 | 0.005 | 0.035 | [0.1047, 0.5577] |
| d_ln_hip_importe | 0.0001 | 0.0014 | 0.08 | 0.935 | 0.954 | [-0.0028, 0.0030] |

Diagnosticos: BG_p = 0.033; BP_p = 0.264; JB_p = 0.076; RESET_p = 0.509; CUSUM_stat = 0.733; CUSUM_p = 0.656; VIF_max = 1.000; r2_adj = 0.358; phi_mitad1 = -0.017; phi_mitad2 = -0.121; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.000 | 0.000 | 0.000 | -0.008 | True |
| 2014T1-2019T4 | residuo no explicado | -0.008 | -0.009 | -0.008 | -0.008 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.009 | NA | NA | -0.008 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | -0.008 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.003 | 0.003 | 0.000 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.001 | -0.005 | -0.002 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.001 | 0.001 | 0.000 | -0.006 | True |
| 2022T3-ultimo | residuo no explicado | -0.004 | -0.007 | -0.006 | -0.006 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.008 | NA | NA | -0.006 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.002 | NA | NA | -0.006 | True |
