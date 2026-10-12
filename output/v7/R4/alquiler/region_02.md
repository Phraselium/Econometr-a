# Region 02, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.004 -0.104\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.122\,\text{ln\_ocupados}_{t-1} + 0.220\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} +0.365\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.104; semivida = 6.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.122, ln_pob_total = 0.220.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0159 | 0.0175 | -0.91 | 0.366 | 0.768 | [-0.0509, 0.0190] |
| d_ln_pob_total_L0 | 0.3646 | 0.5037 | 0.72 | 0.472 | 0.829 | [-0.6412, 1.3705] |
| d_ln_hip_importe | 0.0013 | 0.0012 | 1.04 | 0.300 | 0.706 | [-0.0012, 0.0037] |

Diagnosticos: BG_p = 0.118; BP_p = 0.000; JB_p = 0.000; RESET_p = 0.349; CUSUM_stat = 0.581; CUSUM_p = 0.888; VIF_max = 1.027; r2_adj = 0.357; phi_mitad1 = -0.094; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.000 | 0.000 | 0.000 | 0.003 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.009 | -0.009 | -0.002 | 0.003 | True |
| 2014T1-2019T4 | residuo no explicado | 0.011 | 0.011 | 0.004 | 0.003 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.003 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | 0.003 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | 0.004 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.003 | -0.003 | -0.001 | 0.004 | True |
| 2020T1-2022T2 | residuo no explicado | 0.008 | 0.007 | 0.004 | 0.004 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.001 | NA | NA | 0.004 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.003 | NA | NA | 0.004 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | 0.003 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.000 | -0.000 | -0.000 | 0.003 | True |
| 2022T3-ultimo | residuo no explicado | 0.005 | 0.004 | 0.004 | 0.003 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | 0.003 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.004 | NA | NA | 0.003 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.134\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.016\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.134; semivida = 4.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0002 | 1.21 | 0.232 | 0.534 | [-0.0002, 0.0007] |
| d_y_L1 | 0.0163 | 0.1011 | 0.16 | 0.872 | 0.927 | [-0.1853, 0.2178] |
| d_ln_hip_importe | 0.0007 | 0.0011 | 0.61 | 0.546 | 0.731 | [-0.0015, 0.0029] |

Diagnosticos: BG_p = 0.005; BP_p = 0.000; JB_p = 0.026; RESET_p = 0.849; CUSUM_stat = 0.694; CUSUM_p = 0.722; VIF_max = 1.000; r2_adj = 0.448; phi_mitad1 = -0.146; phi_mitad2 = -0.092; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.001 | 0.001 | 0.000 | 0.003 | True |
| 2014T1-2019T4 | residuo no explicado | 0.004 | 0.001 | 0.002 | 0.003 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.004 | NA | NA | 0.003 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | 0.003 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.002 | 0.002 | 0.000 | 0.004 | True |
| 2020T1-2022T2 | residuo no explicado | 0.006 | 0.002 | 0.003 | 0.004 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.002 | NA | NA | 0.004 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.002 | NA | NA | 0.004 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.006 | 0.006 | 0.001 | 0.005 | True |
| 2022T3-ultimo | residuo no explicado | 0.011 | -0.000 | 0.005 | 0.005 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | 0.005 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.006 | NA | NA | 0.005 | True |
