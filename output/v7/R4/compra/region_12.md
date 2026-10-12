# Region 12, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.013 -0.219\,(\text{ln\_ipv}_{t-1} - [0.621\,\text{ln\_ocupados}_{t-1} + 0.052\,\text{ln\_hip\_importe}_{t-1} + -0.626\,\text{ln\_pob\_total}_{t-1}]) +0.044\,\text{d\_ln\_ocupados\_L0} -0.002\,\text{d\_ln\_hip\_importe\_L0} +2.006\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.219; semivida = 2.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.621, ln_hip_importe = 0.052, ln_pob_total = -0.626.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0445 | 0.1026 | 0.43 | 0.666 | 0.900 | [-0.1606, 0.2496] |
| d_ln_hip_importe_L0 | -0.0015 | 0.0098 | -0.15 | 0.878 | 0.962 | [-0.0211, 0.0180] |
| d_ln_pob_total_L0 | 2.0064 | 2.5480 | 0.79 | 0.434 | 0.768 | [-3.0853, 7.0981] |
| d_ln_compraventas | -0.0140 | 0.0105 | -1.33 | 0.188 | 0.480 | [-0.0350, 0.0070] |

Diagnosticos: BG_p = 0.114; BP_p = 0.007; JB_p = 0.688; RESET_p = 0.540; CUSUM_stat = 0.419; CUSUM_p = 0.995; VIF_max = 6.039; r2_adj = 0.273; phi_mitad1 = -0.515; phi_mitad2 = -0.263; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.021 | 0.011 | 0.003 | -0.038 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.181 | 0.019 | 0.004 | -0.038 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.048 | 0.031 | -0.088 | -0.038 | True |
| 2014T1-2019T4 | residuo no explicado | 0.074 | -0.099 | 0.043 | -0.038 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.046 | NA | NA | -0.038 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.008 | NA | NA | -0.038 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.013 | 0.007 | 0.002 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.037 | 0.004 | 0.001 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.018 | 0.011 | -0.032 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | 0.005 | -0.024 | 0.028 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.002 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.000 | 0.000 | 0.000 | -0.017 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.017 | -0.002 | -0.000 | -0.017 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.034 | 0.022 | -0.063 | -0.017 | True |
| 2022T3-ultimo | residuo no explicado | -0.068 | -0.037 | 0.047 | -0.017 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.022 | NA | NA | -0.017 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.005 | NA | NA | -0.017 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.002 -0.173\,(\text{ln\_ipv}_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.004\,\text{d\_ln\_hip\_importe\_L0} -0.013\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.173; semivida = 3.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.013, ln_hip_importe = 0.055.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0018 | 0.0015 | -1.19 | 0.239 | 0.610 | [-0.0047, 0.0012] |
| d_ln_hip_importe_L0 | -0.0044 | 0.0081 | -0.54 | 0.588 | 0.894 | [-0.0206, 0.0118] |
| d_ln_compraventas | -0.0133 | 0.0099 | -1.35 | 0.181 | 0.596 | [-0.0331, 0.0064] |

Diagnosticos: BG_p = 0.087; BP_p = 0.003; JB_p = 0.768; RESET_p = 0.413; CUSUM_stat = 0.470; CUSUM_p = 0.980; VIF_max = 1.615; r2_adj = 0.278; phi_mitad1 = -0.189; phi_mitad2 = -0.197; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.012 | -0.015 | 0.005 | -0.038 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.267 | -0.368 | -0.045 | -0.038 | True |
| 2014T1-2019T4 | residuo no explicado | 0.242 | 0.345 | 0.002 | -0.038 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.038 | NA | NA | -0.038 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | -0.038 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.030 | -0.036 | 0.012 | -0.001 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.055 | -0.076 | -0.009 | -0.001 | True |
| 2020T1-2022T2 | residuo no explicado | 0.084 | 0.111 | -0.004 | -0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | -0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.001 | NA | NA | -0.001 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.011 | 0.013 | -0.005 | -0.009 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.004 | 0.005 | 0.001 | -0.009 | True |
| 2022T3-ultimo | residuo no explicado | -0.023 | -0.027 | -0.005 | -0.009 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.017 | NA | NA | -0.009 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.009 | NA | NA | -0.009 | True |
