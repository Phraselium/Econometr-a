# Region 02, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.291 -0.211\,(\text{ln\_ipv}_{t-1} - [0.116\,\text{ln\_ocupados}_{t-1} + -0.120\,\text{ln\_hip\_importe}_{t-1} + 4.096\,\text{ln\_pob\_total}_{t-1}]) +0.050\,\text{d\_ln\_ocupados\_L0} -0.015\,\text{d\_ln\_hip\_importe\_L0} +6.111\,\text{d\_ln\_pob\_total\_L0} +0.005\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.211; semivida = 2.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.116, ln_hip_importe = -0.120, ln_pob_total = 4.096.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0502 | 0.0887 | 0.57 | 0.573 | 0.860 | [-0.1270, 0.2274] |
| d_ln_hip_importe_L0 | -0.0148 | 0.0081 | -1.82 | 0.073 | 0.292 | [-0.0311, 0.0014] |
| d_ln_pob_total_L0 | 6.1105 | 2.3648 | 2.58 | 0.012 | 0.118 | [1.3849, 10.8361] |
| d_ln_compraventas | 0.0051 | 0.0121 | 0.42 | 0.673 | 0.900 | [-0.0190, 0.0293] |

Diagnosticos: BG_p = 0.010; BP_p = 0.144; JB_p = 0.120; RESET_p = 0.896; CUSUM_stat = 0.499; CUSUM_p = 0.964; VIF_max = 1.775; r2_adj = 0.259; phi_mitad1 = -0.362; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.001 | -0.000 | -0.000 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.038 | 0.004 | 0.001 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.020 | 0.013 | -0.037 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | 0.002 | -0.033 | 0.019 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.027 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.043 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.004 | 0.002 | 0.000 | -0.016 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.017 | -0.002 | -0.000 | -0.016 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.007 | 0.005 | -0.013 | -0.016 | True |
| 2020T1-2022T2 | residuo no explicado | -0.043 | -0.020 | -0.003 | -0.016 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.020 | NA | NA | -0.016 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.004 | NA | NA | -0.016 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.006 | 0.003 | 0.001 | 0.023 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.024 | 0.002 | 0.001 | 0.023 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.001 | 0.000 | -0.001 | 0.023 | True |
| 2022T3-ultimo | residuo no explicado | 0.040 | 0.017 | 0.023 | 0.023 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.023 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.019 | NA | NA | 0.023 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.002 -0.070\,(\text{ln\_ipv}_{t-1} - [0.018\,\text{tasa\_paro\_epa}_{t-1} + -0.219\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.009\,\text{d\_ln\_hip\_importe\_L0} +0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.070; semivida = 9.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.018, ln_hip_importe = -0.219.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0006 | 0.0013 | 0.43 | 0.669 | 0.894 | [-0.0020, 0.0031] |
| d_ln_hip_importe_L0 | -0.0093 | 0.0078 | -1.19 | 0.237 | 0.610 | [-0.0249, 0.0063] |
| d_ln_compraventas | 0.0056 | 0.0123 | 0.46 | 0.649 | 0.894 | [-0.0189, 0.0302] |

Diagnosticos: BG_p = 0.003; BP_p = 0.302; JB_p = 0.000; RESET_p = 0.481; CUSUM_stat = 0.527; CUSUM_p = 0.944; VIF_max = 1.618; r2_adj = 0.215; phi_mitad1 = -0.077; phi_mitad2 = -0.109; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.004 | -0.005 | 0.002 | -0.017 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.056 | -0.078 | -0.009 | -0.017 | True |
| 2014T1-2019T4 | residuo no explicado | 0.044 | 0.066 | -0.009 | -0.017 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.017 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.012 | NA | NA | -0.017 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.007 | -0.009 | 0.003 | -0.014 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.025 | 0.034 | 0.004 | -0.014 | True |
| 2020T1-2022T2 | residuo no explicado | -0.032 | -0.039 | -0.021 | -0.014 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.000 | NA | NA | -0.014 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.014 | NA | NA | -0.014 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.022 | -0.026 | 0.009 | 0.046 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.054 | -0.075 | -0.009 | 0.046 | True |
| 2022T3-ultimo | residuo no explicado | 0.122 | 0.146 | 0.047 | 0.046 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.049 | NA | NA | 0.046 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.002 | NA | NA | 0.046 | True |
