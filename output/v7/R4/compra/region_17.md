# Region 17, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +1.706 -0.179\,(\text{ln\_ipv}_{t-1} - [-0.361\,\text{ln\_ocupados}_{t-1} + 0.086\,\text{ln\_hip\_importe}_{t-1} + 5.646\,\text{ln\_pob\_total}_{t-1}]) +0.094\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +3.661\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.179; semivida = 3.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.361, ln_hip_importe = 0.086, ln_pob_total = 5.646.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0942 | 0.0712 | 1.32 | 0.190 | 0.480 | [-0.0481, 0.2365] |
| d_ln_hip_importe_L0 | 0.0029 | 0.0078 | 0.38 | 0.709 | 0.900 | [-0.0126, 0.0185] |
| d_ln_pob_total_L0 | 3.6609 | 1.8590 | 1.97 | 0.053 | 0.265 | [-0.0541, 7.3759] |
| d_ln_compraventas | -0.0021 | 0.0070 | -0.30 | 0.761 | 0.900 | [-0.0161, 0.0118] |

Diagnosticos: BG_p = 0.565; BP_p = 0.001; JB_p = 0.987; RESET_p = 0.524; CUSUM_stat = 0.650; CUSUM_p = 0.792; VIF_max = 1.842; r2_adj = 0.107; phi_mitad1 = -0.379; phi_mitad2 = -0.453; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.010 | 0.005 | 0.001 | -0.036 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.063 | 0.007 | 0.001 | -0.036 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.004 | 0.003 | -0.008 | -0.036 | True |
| 2014T1-2019T4 | residuo no explicado | 0.013 | -0.051 | -0.031 | -0.036 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.061 | NA | NA | -0.036 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.025 | NA | NA | -0.036 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.013 | 0.007 | 0.002 | -0.011 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.120 | -0.012 | -0.003 | -0.011 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.002 | -0.001 | 0.003 | -0.011 | True |
| 2020T1-2022T2 | residuo no explicado | -0.142 | -0.004 | -0.013 | -0.011 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.017 | NA | NA | -0.011 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.028 | NA | NA | -0.011 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.007 | 0.004 | 0.001 | 0.013 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.067 | 0.007 | 0.001 | 0.013 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.009 | 0.006 | -0.017 | 0.013 | True |
| 2022T3-ultimo | residuo no explicado | 0.064 | -0.004 | 0.028 | 0.013 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.002 | NA | NA | 0.013 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.011 | NA | NA | 0.013 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.028 -0.066\,(\text{ln\_ipv}_{t-1} - [0.024\,\text{tasa\_paro\_epa}_{t-1} + 0.185\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.001\,\text{d\_ln\_hip\_importe\_L0} +0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.066; semivida = 10.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.024, ln_hip_importe = 0.185.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0010 | 0.39 | 0.696 | 0.894 | [-0.0016, 0.0024] |
| d_ln_hip_importe_L0 | 0.0015 | 0.0075 | 0.20 | 0.844 | 0.915 | [-0.0134, 0.0164] |
| d_ln_compraventas | 0.0013 | 0.0070 | 0.19 | 0.851 | 0.915 | [-0.0127, 0.0153] |

Diagnosticos: BG_p = 0.171; BP_p = 0.011; JB_p = 0.866; RESET_p = 0.909; CUSUM_stat = 0.868; CUSUM_p = 0.438; VIF_max = 1.352; r2_adj = 0.031; phi_mitad1 = -0.052; phi_mitad2 = -0.239; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.008 | -0.010 | 0.003 | -0.036 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.094 | -0.129 | -0.016 | -0.036 | True |
| 2014T1-2019T4 | residuo no explicado | 0.066 | 0.103 | -0.024 | -0.036 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.064 | NA | NA | -0.036 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.028 | NA | NA | -0.036 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.039 | -0.047 | 0.016 | -0.010 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.175 | 0.241 | 0.029 | -0.010 | True |
| 2020T1-2022T2 | residuo no explicado | -0.145 | -0.204 | -0.055 | -0.010 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.004 | NA | NA | -0.010 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.013 | NA | NA | -0.010 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.013 | -0.016 | 0.005 | 0.026 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.155 | -0.214 | -0.026 | 0.026 | True |
| 2022T3-ultimo | residuo no explicado | 0.194 | 0.255 | 0.046 | 0.026 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.033 | NA | NA | 0.026 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.008 | NA | NA | 0.026 | True |
