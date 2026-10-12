# Region 01, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.050 +0.017\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.301\,\text{ln\_ocupados}_{t-1} + 1.631\,\text{ln\_pob\_total}_{t-1}]) +0.003\,\text{d\_ln\_ocupados\_L0} -0.448\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.017; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.301, ln_pob_total = 1.631.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0028 | 0.0100 | 0.28 | 0.784 | 0.952 | [-0.0172, 0.0228] |
| d_ln_pob_total_L0 | -0.4475 | 0.3593 | -1.25 | 0.217 | 0.652 | [-1.1652, 0.2701] |
| d_ln_hip_importe | 0.0004 | 0.0023 | 0.19 | 0.852 | 0.965 | [-0.0041, 0.0050] |

Diagnosticos: BG_p = 0.016; BP_p = 0.012; JB_p = 0.000; RESET_p = 0.636; CUSUM_stat = 0.650; CUSUM_p = 0.792; VIF_max = 1.133; r2_adj = -0.047; phi_mitad1 = -0.342; phi_mitad2 = -0.074; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.006 | 0.002 | 0.000 | 0.003 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.001 | 0.001 | 0.000 | 0.003 | True |
| 2014T1-2019T4 | residuo no explicado | -0.003 | 0.001 | 0.003 | 0.003 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.003 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | 0.003 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.001 | 0.000 | 0.000 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.003 | 0.003 | 0.001 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.007 | -0.006 | -0.003 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.001 | 0.000 | 0.000 | 0.011 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.007 | -0.007 | -0.001 | 0.011 | True |
| 2022T3-ultimo | residuo no explicado | 0.017 | 0.017 | 0.012 | 0.011 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.011 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.006 | NA | NA | 0.011 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.034\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.002\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.162\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.034; semivida = 20.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.002.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0000 | 0.0002 | -0.08 | 0.933 | 0.954 | [-0.0003, 0.0003] |
| d_y_L1 | 0.1621 | 0.1208 | 1.34 | 0.184 | 0.494 | [-0.0789, 0.4031] |
| d_ln_hip_importe | 0.0000 | 0.0022 | 0.00 | 1.000 | 1.000 | [-0.0045, 0.0045] |

Diagnosticos: BG_p = 0.038; BP_p = 0.023; JB_p = 0.000; RESET_p = 0.165; CUSUM_stat = 0.667; CUSUM_p = 0.765; VIF_max = 1.000; r2_adj = -0.019; phi_mitad1 = -0.309; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.018 | -0.019 | -0.002 | 0.003 | True |
| 2014T1-2019T4 | residuo no explicado | -0.015 | 0.022 | 0.005 | 0.003 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.003 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.002 | NA | NA | 0.003 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.003 | -0.003 | -0.000 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.005 | 0.001 | -0.002 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.003 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.005 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.007 | -0.007 | -0.001 | 0.013 | True |
| 2022T3-ultimo | residuo no explicado | 0.006 | 0.020 | 0.014 | 0.013 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.013 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.007 | NA | NA | 0.013 | True |
