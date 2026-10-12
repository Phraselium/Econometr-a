# Region 09, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.548 -0.111\,(\text{ln\_ipv}_{t-1} - [-1.536\,\text{ln\_ocupados}_{t-1} + 0.279\,\text{ln\_hip\_importe}_{t-1} + -2.336\,\text{ln\_pob\_total}_{t-1}]) +0.084\,\text{d\_ln\_ocupados\_L0} +0.030\,\text{d\_ln\_hip\_importe\_L0} +6.163\,\text{d\_ln\_pob\_total\_L0} -0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.111; semivida = 5.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.536, ln_hip_importe = 0.279, ln_pob_total = -2.336.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0844 | 0.1525 | 0.55 | 0.582 | 0.860 | [-0.2203, 0.3891] |
| d_ln_hip_importe_L0 | 0.0299 | 0.0123 | 2.43 | 0.018 | 0.123 | [0.0053, 0.0545] |
| d_ln_pob_total_L0 | 6.1626 | 1.9555 | 3.15 | 0.002 | 0.050 | [2.2549, 10.0704] |
| d_ln_compraventas | -0.0055 | 0.0179 | -0.31 | 0.759 | 0.900 | [-0.0412, 0.0302] |

Diagnosticos: BG_p = 0.005; BP_p = 0.012; JB_p = 0.776; RESET_p = 0.000; CUSUM_stat = 1.322; CUSUM_p = 0.061; VIF_max = 9.369; r2_adj = 0.289; phi_mitad1 = -0.154; phi_mitad2 = -0.106; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.006 | -0.003 | -0.001 | 0.168 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.120 | -0.012 | -0.003 | 0.168 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.051 | -0.033 | 0.094 | 0.168 | True |
| 2014T1-2019T4 | residuo no explicado | 0.105 | 0.217 | 0.077 | 0.168 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.063 | NA | NA | 0.168 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.105 | NA | NA | 0.168 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.002 | 0.001 | 0.000 | -0.003 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.185 | -0.019 | -0.004 | -0.003 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.013 | -0.009 | 0.024 | -0.003 | True |
| 2020T1-2022T2 | residuo no explicado | -0.178 | 0.023 | -0.024 | -0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | -0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.003 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.011 | -0.006 | -0.001 | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.033 | 0.003 | 0.001 | -0.007 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.032 | -0.021 | 0.058 | -0.007 | True |
| 2022T3-ultimo | residuo no explicado | 0.069 | 0.016 | -0.065 | -0.007 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.027 | NA | NA | -0.007 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.034 | NA | NA | -0.007 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.010 -0.061\,(\text{ln\_ipv}_{t-1} - [-0.121\,\text{tasa\_paro\_epa}_{t-1} + -0.084\,\text{ln\_hip\_importe}_{t-1}]) -0.005\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.011\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.061; semivida = 11.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.121, ln_hip_importe = -0.084.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0055 | 0.0019 | -2.83 | 0.006 | 0.085 | [-0.0094, -0.0016] |
| d_ln_hip_importe_L0 | 0.0044 | 0.0119 | 0.37 | 0.712 | 0.894 | [-0.0194, 0.0282] |
| d_ln_compraventas | 0.0113 | 0.0172 | 0.66 | 0.514 | 0.894 | [-0.0231, 0.0456] |

Diagnosticos: BG_p = 0.008; BP_p = 0.001; JB_p = 0.605; RESET_p = 0.068; CUSUM_stat = 1.205; CUSUM_p = 0.110; VIF_max = 4.619; r2_adj = 0.295; phi_mitad1 = -0.115; phi_mitad2 = -0.144; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.007 | 0.009 | -0.003 | 0.168 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.177 | 0.244 | 0.030 | 0.168 | True |
| 2014T1-2019T4 | residuo no explicado | -0.017 | -0.085 | 0.141 | 0.168 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.071 | NA | NA | 0.168 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.097 | NA | NA | 0.168 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.009 | 0.011 | -0.004 | -0.005 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.274 | 0.377 | 0.046 | -0.005 | True |
| 2020T1-2022T2 | residuo no explicado | -0.288 | -0.393 | -0.047 | -0.005 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.030 | NA | NA | -0.005 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.035 | NA | NA | -0.005 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.013 | -0.016 | 0.006 | -0.044 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.041 | -0.057 | -0.007 | -0.044 | True |
| 2022T3-ultimo | residuo no explicado | 0.011 | 0.029 | -0.043 | -0.044 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.030 | NA | NA | -0.044 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.014 | NA | NA | -0.044 | True |
