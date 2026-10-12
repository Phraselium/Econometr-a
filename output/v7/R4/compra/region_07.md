# Region 07, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.036 -0.368\,(\text{ln\_ipv}_{t-1} - [0.371\,\text{ln\_ocupados}_{t-1} + 0.144\,\text{ln\_hip\_importe}_{t-1} + 0.196\,\text{ln\_pob\_total}_{t-1}]) +0.032\,\text{d\_ln\_ocupados\_L0} +0.033\,\text{d\_ln\_hip\_importe\_L0} +2.867\,\text{d\_ln\_pob\_total\_L0} -0.022\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.368; semivida = 1.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.371, ln_hip_importe = 0.144, ln_pob_total = 0.196.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0324 | 0.1073 | 0.30 | 0.764 | 0.900 | [-0.1820, 0.2468] |
| d_ln_hip_importe_L0 | 0.0332 | 0.0107 | 3.10 | 0.003 | 0.050 | [0.0118, 0.0546] |
| d_ln_pob_total_L0 | 2.8670 | 2.2754 | 1.26 | 0.212 | 0.516 | [-1.6799, 7.4140] |
| d_ln_compraventas | -0.0216 | 0.0129 | -1.67 | 0.100 | 0.324 | [-0.0474, 0.0042] |

Diagnosticos: BG_p = 0.936; BP_p = 0.047; JB_p = 0.879; RESET_p = 0.413; CUSUM_stat = 0.597; CUSUM_p = 0.868; VIF_max = 6.526; r2_adj = 0.238; phi_mitad1 = -0.435; phi_mitad2 = -0.365; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.016 | 0.009 | 0.002 | -0.049 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.064 | 0.007 | 0.001 | -0.049 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.092 | 0.060 | -0.170 | -0.049 | True |
| 2014T1-2019T4 | residuo no explicado | -0.093 | -0.124 | 0.118 | -0.049 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.049 | NA | NA | -0.049 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.000 | NA | NA | -0.049 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.008 | 0.005 | 0.001 | -0.030 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.001 | 0.000 | 0.000 | -0.030 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.031 | 0.020 | -0.057 | -0.030 | True |
| 2020T1-2022T2 | residuo no explicado | -0.068 | -0.055 | 0.026 | -0.030 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.035 | NA | NA | -0.030 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.005 | NA | NA | -0.030 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.008 | 0.004 | 0.001 | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.018 | -0.002 | -0.000 | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.029 | 0.019 | -0.054 | -0.007 | True |
| 2022T3-ultimo | residuo no explicado | -0.063 | -0.029 | 0.046 | -0.007 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.004 | NA | NA | -0.007 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.003 | NA | NA | -0.007 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.010 -0.174\,(\text{ln\_ipv}_{t-1} - [0.008\,\text{tasa\_paro\_epa}_{t-1} + 0.237\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.019\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.174; semivida = 3.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.008, ln_hip_importe = 0.237.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0014 | 0.27 | 0.788 | 0.894 | [-0.0025, 0.0032] |
| d_ln_hip_importe_L0 | 0.0282 | 0.0101 | 2.80 | 0.007 | 0.085 | [0.0081, 0.0484] |
| d_ln_compraventas | -0.0192 | 0.0129 | -1.49 | 0.140 | 0.548 | [-0.0449, 0.0064] |

Diagnosticos: BG_p = 0.627; BP_p = 0.091; JB_p = 0.853; RESET_p = 0.572; CUSUM_stat = 0.656; CUSUM_p = 0.782; VIF_max = 1.360; r2_adj = 0.174; phi_mitad1 = -0.310; phi_mitad2 = -0.128; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.002 | -0.002 | 0.001 | -0.049 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.095 | -0.130 | -0.016 | -0.049 | True |
| 2014T1-2019T4 | residuo no explicado | 0.048 | 0.084 | -0.033 | -0.049 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.036 | NA | NA | -0.049 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.012 | NA | NA | -0.049 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.012 | -0.014 | 0.005 | -0.029 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.003 | -0.004 | -0.001 | -0.029 | True |
| 2020T1-2022T2 | residuo no explicado | -0.014 | -0.011 | -0.033 | -0.029 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.027 | NA | NA | -0.029 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.029 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.006 | -0.007 | 0.002 | 0.014 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.011 | -0.015 | -0.002 | 0.014 | True |
| 2022T3-ultimo | residuo no explicado | 0.030 | 0.036 | 0.014 | 0.014 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.014 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.008 | NA | NA | 0.014 | True |
