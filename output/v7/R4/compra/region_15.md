# Region 15, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -1.156 -0.271\,(\text{ln\_ipv}_{t-1} - [-0.372\,\text{ln\_ocupados}_{t-1} + -0.139\,\text{ln\_hip\_importe}_{t-1} + -3.632\,\text{ln\_pob\_total}_{t-1}]) -0.095\,\text{d\_ln\_ocupados\_L0} -0.026\,\text{d\_ln\_hip\_importe\_L0} -20.330\,\text{d\_ln\_pob\_total\_L0} +0.008\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.271; semivida = 2.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.372, ln_hip_importe = -0.139, ln_pob_total = -3.632.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0950 | 0.1116 | -0.85 | 0.398 | 0.752 | [-0.3181, 0.1281] |
| d_ln_hip_importe_L0 | -0.0257 | 0.0149 | -1.73 | 0.089 | 0.316 | [-0.0554, 0.0040] |
| d_ln_pob_total_L0 | -20.3300 | 5.9874 | -3.40 | 0.001 | 0.040 | [-32.2949, -8.3651] |
| d_ln_compraventas | 0.0083 | 0.0119 | 0.69 | 0.490 | 0.813 | [-0.0155, 0.0320] |

Diagnosticos: BG_p = 0.156; BP_p = 0.376; JB_p = 0.214; RESET_p = 0.115; CUSUM_stat = 0.381; CUSUM_p = 0.999; VIF_max = 5.271; r2_adj = 0.182; phi_mitad1 = -0.445; phi_mitad2 = -0.307; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.014 | 0.008 | 0.002 | -0.105 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.140 | 0.015 | 0.003 | -0.105 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.049 | -0.032 | 0.089 | -0.105 | True |
| 2014T1-2019T4 | residuo no explicado | 0.070 | -0.095 | -0.199 | -0.105 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.075 | NA | NA | -0.105 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.030 | NA | NA | -0.105 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.017 | 0.002 | 0.000 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.012 | -0.008 | 0.023 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.024 | 0.003 | -0.026 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.000 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.003 | -0.002 | -0.000 | 0.039 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.010 | 0.001 | 0.000 | 0.039 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.002 | -0.001 | 0.003 | 0.039 | True |
| 2022T3-ultimo | residuo no explicado | 0.055 | 0.041 | 0.036 | 0.039 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.029 | NA | NA | 0.039 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.010 | NA | NA | 0.039 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.014 -0.065\,(\text{ln\_ipv}_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.008\,\text{d\_ln\_hip\_importe\_L0} -0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.065; semivida = 10.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.005, ln_hip_importe = -0.196.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0015 | 0.0014 | -1.02 | 0.311 | 0.672 | [-0.0044, 0.0014] |
| d_ln_hip_importe_L0 | -0.0082 | 0.0146 | -0.56 | 0.577 | 0.894 | [-0.0372, 0.0209] |
| d_ln_compraventas | -0.0011 | 0.0120 | -0.09 | 0.926 | 0.964 | [-0.0251, 0.0229] |

Diagnosticos: BG_p = 0.257; BP_p = 0.070; JB_p = 0.099; RESET_p = 0.090; CUSUM_stat = 0.590; CUSUM_p = 0.878; VIF_max = 2.286; r2_adj = 0.059; phi_mitad1 = -0.112; phi_mitad2 = -0.172; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.054 | -0.064 | 0.022 | -0.105 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.207 | -0.285 | -0.035 | -0.105 | True |
| 2014T1-2019T4 | residuo no explicado | 0.156 | 0.244 | -0.092 | -0.105 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.045 | NA | NA | -0.105 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.059 | NA | NA | -0.105 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.001 | 0.001 | -0.000 | -0.003 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.022 | -0.030 | -0.004 | -0.003 | True |
| 2020T1-2022T2 | residuo no explicado | 0.018 | 0.027 | 0.001 | -0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.007 | NA | NA | -0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.010 | NA | NA | -0.003 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.023 | -0.027 | 0.009 | 0.011 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.057 | 0.079 | 0.010 | 0.011 | True |
| 2022T3-ultimo | residuo no explicado | -0.023 | -0.040 | -0.008 | 0.011 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.017 | NA | NA | 0.011 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.028 | NA | NA | 0.011 | True |
