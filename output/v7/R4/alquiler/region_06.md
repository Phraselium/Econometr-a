# Region 06, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.010 -0.099\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.032\,\text{ln\_ocupados}_{t-1} + -0.069\,\text{ln\_pob\_total}_{t-1}]) -0.026\,\text{d\_ln\_ocupados\_L0} +1.266\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.099; semivida = 6.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.032, ln_pob_total = -0.069.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0265 | 0.0251 | -1.06 | 0.295 | 0.706 | [-0.0766, 0.0236] |
| d_ln_pob_total_L0 | 1.2657 | 0.7282 | 1.74 | 0.087 | 0.396 | [-0.1887, 2.7201] |
| d_ln_hip_importe | 0.0014 | 0.0026 | 0.56 | 0.580 | 0.867 | [-0.0037, 0.0065] |

Diagnosticos: BG_p = 0.008; BP_p = 0.002; JB_p = 0.000; RESET_p = 0.000; CUSUM_stat = 0.619; CUSUM_p = 0.838; VIF_max = 1.028; r2_adj = 0.194; phi_mitad1 = -0.114; phi_mitad2 = -0.401; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.005 | -0.002 | -0.000 | -0.002 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.014 | -0.013 | -0.003 | -0.002 | True |
| 2014T1-2019T4 | residuo no explicado | 0.017 | 0.013 | 0.001 | -0.002 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.012 | NA | NA | -0.002 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.009 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.002 | -0.000 | -0.000 | 0.001 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.000 | -0.000 | -0.000 | 0.001 | True |
| 2020T1-2022T2 | residuo no explicado | 0.003 | 0.001 | 0.001 | 0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.008 | NA | NA | 0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.008 | NA | NA | 0.001 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.001 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.011 | -0.010 | -0.002 | -0.001 | True |
| 2022T3-ultimo | residuo no explicado | 0.011 | 0.009 | 0.001 | -0.001 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.003 | NA | NA | -0.001 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.002 | NA | NA | -0.001 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.124\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.000\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.073\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.124; semivida = 5.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.000.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0002 | 0.0003 | 0.67 | 0.507 | 0.731 | [-0.0004, 0.0009] |
| d_y_L1 | -0.0732 | 0.1089 | -0.67 | 0.503 | 0.731 | [-0.2904, 0.1440] |
| d_ln_hip_importe | 0.0014 | 0.0024 | 0.57 | 0.568 | 0.731 | [-0.0034, 0.0062] |

Diagnosticos: BG_p = 0.026; BP_p = 0.000; JB_p = 0.000; RESET_p = 0.238; CUSUM_stat = 0.672; CUSUM_p = 0.758; VIF_max = 1.000; r2_adj = 0.205; phi_mitad1 = -0.109; phi_mitad2 = -0.385; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.009 | 0.009 | 0.001 | -0.002 | True |
| 2014T1-2019T4 | residuo no explicado | 0.007 | -0.012 | -0.003 | -0.002 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.002 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.003 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.002 | -0.002 | -0.000 | 0.001 | True |
| 2020T1-2022T2 | residuo no explicado | -0.002 | 0.003 | 0.001 | 0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.002 | NA | NA | 0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.001 | NA | NA | 0.001 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.006 | 0.006 | 0.001 | 0.002 | True |
| 2022T3-ultimo | residuo no explicado | 0.008 | -0.004 | 0.002 | 0.002 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.002 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.004 | NA | NA | 0.002 | True |
