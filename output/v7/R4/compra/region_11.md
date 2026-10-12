# Region 11, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.160 -0.156\,(\text{ln\_ipv}_{t-1} - [-0.829\,\text{ln\_ocupados}_{t-1} + 0.170\,\text{ln\_hip\_importe}_{t-1} + 2.305\,\text{ln\_pob\_total}_{t-1}]) -0.080\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +5.770\,\text{d\_ln\_pob\_total\_L0} +0.012\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.156; semivida = 4.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.829, ln_hip_importe = 0.170, ln_pob_total = 2.305.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0797 | 0.0965 | -0.83 | 0.412 | 0.757 | [-0.2725, 0.1131] |
| d_ln_hip_importe_L0 | 0.0029 | 0.0136 | 0.22 | 0.830 | 0.956 | [-0.0242, 0.0300] |
| d_ln_pob_total_L0 | 5.7698 | 2.7406 | 2.11 | 0.039 | 0.222 | [0.2932, 11.2465] |
| d_ln_compraventas | 0.0122 | 0.0142 | 0.86 | 0.395 | 0.752 | [-0.0162, 0.0405] |

Diagnosticos: BG_p = 0.699; BP_p = 0.056; JB_p = 0.711; RESET_p = 0.113; CUSUM_stat = 0.702; CUSUM_p = 0.708; VIF_max = 6.103; r2_adj = 0.201; phi_mitad1 = -0.396; phi_mitad2 = -0.285; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.013 | 0.007 | 0.002 | -0.115 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.006 | -0.001 | -0.000 | -0.115 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.072 | 0.047 | -0.132 | -0.115 | True |
| 2014T1-2019T4 | residuo no explicado | -0.206 | -0.168 | 0.015 | -0.115 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.132 | NA | NA | -0.115 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.016 | NA | NA | -0.115 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.019 | -0.010 | -0.003 | -0.047 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.023 | -0.002 | -0.000 | -0.047 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.030 | 0.019 | -0.055 | -0.047 | True |
| 2020T1-2022T2 | residuo no explicado | -0.080 | -0.054 | 0.011 | -0.047 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.014 | NA | NA | -0.047 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.061 | NA | NA | -0.047 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.024 | 0.013 | 0.003 | -0.039 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.024 | 0.002 | 0.001 | -0.039 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.054 | 0.035 | -0.100 | -0.039 | True |
| 2022T3-ultimo | residuo no explicado | -0.093 | -0.090 | 0.057 | -0.039 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.069 | NA | NA | -0.039 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.030 | NA | NA | -0.039 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.045 -0.001\,(\text{ln\_ipv}_{t-1} - [-1.219\,\text{tasa\_paro\_epa}_{t-1} + 24.398\,\text{ln\_hip\_importe}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.007\,\text{d\_ln\_hip\_importe\_L0} +0.018\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.001; semivida = 527.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -1.219, ln_hip_importe = 24.398.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0004 | 0.0013 | -0.28 | 0.781 | 0.894 | [-0.0031, 0.0023] |
| d_ln_hip_importe_L0 | 0.0073 | 0.0133 | 0.55 | 0.585 | 0.894 | [-0.0193, 0.0339] |
| d_ln_compraventas | 0.0179 | 0.0138 | 1.30 | 0.199 | 0.596 | [-0.0096, 0.0455] |

Diagnosticos: BG_p = 0.456; BP_p = 0.001; JB_p = 0.761; RESET_p = 0.977; CUSUM_stat = 0.866; CUSUM_p = 0.441; VIF_max = 2.929; r2_adj = 0.129; phi_mitad1 = -0.085; phi_mitad2 = -0.086; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.031 | -0.037 | 0.013 | -0.115 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.009 | 0.013 | 0.002 | -0.115 | True |
| 2014T1-2019T4 | residuo no explicado | -0.094 | -0.092 | -0.130 | -0.115 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.119 | NA | NA | -0.115 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.004 | NA | NA | -0.115 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.055 | 0.065 | -0.023 | -0.047 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.036 | 0.049 | 0.006 | -0.047 | True |
| 2020T1-2022T2 | residuo no explicado | -0.137 | -0.161 | -0.030 | -0.047 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.025 | NA | NA | -0.047 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.022 | NA | NA | -0.047 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.016 | 0.020 | -0.007 | -0.034 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.027 | 0.037 | 0.004 | -0.034 | True |
| 2022T3-ultimo | residuo no explicado | -0.077 | -0.090 | -0.031 | -0.034 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.010 | NA | NA | -0.034 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.023 | NA | NA | -0.034 | True |
