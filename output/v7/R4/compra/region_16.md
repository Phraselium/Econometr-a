# Region 16, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.078 -0.272\,(\text{ln\_ipv}_{t-1} - [-0.086\,\text{ln\_ocupados}_{t-1} + -0.024\,\text{ln\_hip\_importe}_{t-1} + 2.117\,\text{ln\_pob\_total}_{t-1}]) +0.000\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +1.824\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.272; semivida = 2.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.086, ln_hip_importe = -0.024, ln_pob_total = 2.117.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0004 | 0.0701 | 0.01 | 0.996 | 0.996 | [-0.1398, 0.1405] |
| d_ln_hip_importe_L0 | -0.0011 | 0.0138 | -0.08 | 0.939 | 0.982 | [-0.0286, 0.0265] |
| d_ln_pob_total_L0 | 1.8235 | 3.0988 | 0.59 | 0.558 | 0.860 | [-4.3689, 8.0160] |
| d_ln_compraventas | 0.0041 | 0.0132 | 0.31 | 0.755 | 0.900 | [-0.0222, 0.0305] |

Diagnosticos: BG_p = 0.508; BP_p = 0.293; JB_p = 0.888; RESET_p = 0.080; CUSUM_stat = 0.594; CUSUM_p = 0.872; VIF_max = 4.322; r2_adj = 0.093; phi_mitad1 = -0.197; phi_mitad2 = -0.530; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.031 | 0.016 | 0.004 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.062 | -0.006 | -0.001 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.017 | -0.011 | 0.032 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | -0.092 | -0.016 | -0.051 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.022 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.011 | 0.006 | 0.002 | -0.005 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.076 | 0.008 | 0.002 | -0.005 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.012 | 0.008 | -0.022 | -0.005 | True |
| 2020T1-2022T2 | residuo no explicado | 0.048 | -0.027 | 0.014 | -0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.002 | NA | NA | -0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | -0.005 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.000 | -0.000 | -0.000 | 0.008 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.031 | 0.003 | 0.001 | 0.008 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.019 | 0.012 | -0.035 | 0.008 | True |
| 2022T3-ultimo | residuo no explicado | 0.020 | -0.008 | 0.042 | 0.008 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.014 | NA | NA | 0.008 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.022 | NA | NA | 0.008 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.134\,(\text{ln\_ipv}_{t-1} - [0.003\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.000\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.134; semivida = 4.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.003, ln_hip_importe = 0.055.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0009 | 0.0015 | -0.62 | 0.540 | 0.894 | [-0.0040, 0.0021] |
| d_ln_hip_importe_L0 | 0.0041 | 0.0124 | 0.33 | 0.740 | 0.894 | [-0.0207, 0.0290] |
| d_ln_compraventas | 0.0005 | 0.0131 | 0.04 | 0.972 | 0.972 | [-0.0257, 0.0266] |

Diagnosticos: BG_p = 0.950; BP_p = 0.191; JB_p = 0.931; RESET_p = 0.102; CUSUM_stat = 0.523; CUSUM_p = 0.947; VIF_max = 1.884; r2_adj = 0.073; phi_mitad1 = -0.068; phi_mitad2 = -0.433; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.053 | -0.063 | 0.022 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.092 | 0.126 | 0.015 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | -0.056 | -0.080 | -0.054 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.009 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.008 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.006 | 0.007 | -0.002 | -0.006 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.115 | -0.158 | -0.019 | -0.006 | True |
| 2020T1-2022T2 | residuo no explicado | 0.103 | 0.145 | 0.015 | -0.006 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.022 | NA | NA | -0.006 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.016 | NA | NA | -0.006 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.010 | -0.012 | 0.004 | -0.023 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.081 | -0.112 | -0.014 | -0.023 | True |
| 2022T3-ultimo | residuo no explicado | 0.068 | 0.100 | -0.014 | -0.023 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.016 | NA | NA | -0.023 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.008 | NA | NA | -0.023 | True |
