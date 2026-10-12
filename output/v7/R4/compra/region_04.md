# Region 04, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.039 -0.012\,(\text{ln\_ipv}_{t-1} - [10.192\,\text{ln\_ocupados}_{t-1} + 0.801\,\text{ln\_hip\_importe}_{t-1} + -15.928\,\text{ln\_pob\_total}_{t-1}]) +0.087\,\text{d\_ln\_ocupados\_L0} +0.012\,\text{d\_ln\_hip\_importe\_L0} -4.358\,\text{d\_ln\_pob\_total\_L0} -0.025\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.012; semivida = 58.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 10.192, ln_hip_importe = 0.801, ln_pob_total = -15.928.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0872 | 0.0217 | 4.02 | 0.000 | 0.011 | [0.0439, 0.1305] |
| d_ln_hip_importe_L0 | 0.0115 | 0.0122 | 0.94 | 0.349 | 0.720 | [-0.0129, 0.0359] |
| d_ln_pob_total_L0 | -4.3579 | 2.5555 | -1.71 | 0.093 | 0.316 | [-9.4646, 0.7488] |
| d_ln_compraventas | -0.0254 | 0.0169 | -1.50 | 0.139 | 0.431 | [-0.0592, 0.0085] |

Diagnosticos: BG_p = 0.428; BP_p = 0.436; JB_p = 0.997; RESET_p = 0.043; CUSUM_stat = 0.433; CUSUM_p = 0.992; VIF_max = 2.214; r2_adj = 0.285; phi_mitad1 = -0.195; phi_mitad2 = -0.027; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.042 | -0.022 | -0.006 | 0.147 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.013 | 0.001 | 0.000 | 0.147 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.100 | -0.065 | 0.184 | 0.147 | True |
| 2014T1-2019T4 | residuo no explicado | 0.302 | 0.234 | -0.031 | 0.147 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.186 | NA | NA | 0.147 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.038 | NA | NA | 0.147 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.014 | -0.007 | -0.002 | 0.051 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.045 | -0.005 | -0.001 | 0.051 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.022 | -0.014 | 0.041 | 0.051 | True |
| 2020T1-2022T2 | residuo no explicado | 0.041 | 0.077 | 0.013 | 0.051 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.011 | NA | NA | 0.051 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.062 | NA | NA | 0.051 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.052 | 0.028 | 0.007 | -0.022 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.004 | 0.000 | 0.000 | -0.022 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.043 | -0.028 | 0.079 | -0.022 | True |
| 2022T3-ultimo | residuo no explicado | -0.028 | -0.023 | -0.108 | -0.022 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.015 | NA | NA | -0.022 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.038 | NA | NA | -0.022 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.017\,(\text{ln\_ipv}_{t-1} - [-0.098\,\text{tasa\_paro\_epa}_{t-1} + 0.373\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.014\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.017; semivida = 41.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.098, ln_hip_importe = 0.373.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0015 | 0.0004 | -3.29 | 0.002 | 0.040 | [-0.0023, -0.0006] |
| d_ln_hip_importe_L0 | 0.0137 | 0.0121 | 1.13 | 0.261 | 0.633 | [-0.0104, 0.0378] |
| d_ln_compraventas | -0.0045 | 0.0155 | -0.29 | 0.774 | 0.894 | [-0.0353, 0.0264] |

Diagnosticos: BG_p = 0.454; BP_p = 0.579; JB_p = 0.609; RESET_p = 0.000; CUSUM_stat = 0.632; CUSUM_p = 0.819; VIF_max = 1.864; r2_adj = 0.191; phi_mitad1 = -0.193; phi_mitad2 = 0.007; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.029 | 0.034 | -0.012 | 0.147 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.019 | -0.026 | -0.003 | 0.147 | True |
| 2014T1-2019T4 | residuo no explicado | 0.138 | 0.140 | 0.162 | 0.147 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.179 | NA | NA | 0.147 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.032 | NA | NA | 0.147 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.023 | -0.028 | 0.010 | 0.050 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.063 | 0.087 | 0.011 | 0.050 | True |
| 2020T1-2022T2 | residuo no explicado | 0.010 | -0.009 | 0.030 | 0.050 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.028 | NA | NA | 0.050 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.079 | NA | NA | 0.050 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.006 | 0.007 | -0.002 | -0.016 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.079 | -0.108 | -0.013 | -0.016 | True |
| 2022T3-ultimo | residuo no explicado | 0.057 | 0.086 | 0.000 | -0.016 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.033 | NA | NA | -0.016 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.049 | NA | NA | -0.016 | True |
