# Region 13, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.131 -0.080\,(\text{ln\_ipv}_{t-1} - [-0.755\,\text{ln\_ocupados}_{t-1} + 0.469\,\text{ln\_hip\_importe}_{t-1} + 1.350\,\text{ln\_pob\_total}_{t-1}]) -0.078\,\text{d\_ln\_ocupados\_L0} +0.041\,\text{d\_ln\_hip\_importe\_L0} +1.261\,\text{d\_ln\_pob\_total\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.080; semivida = 8.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.755, ln_hip_importe = 0.469, ln_pob_total = 1.350.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0782 | 0.1051 | -0.74 | 0.460 | 0.782 | [-0.2882, 0.1319] |
| d_ln_hip_importe_L0 | 0.0405 | 0.0153 | 2.66 | 0.010 | 0.113 | [0.0101, 0.0710] |
| d_ln_pob_total_L0 | 1.2609 | 2.0098 | 0.63 | 0.533 | 0.860 | [-2.7554, 5.2772] |
| d_ln_compraventas | 0.0350 | 0.0179 | 1.95 | 0.055 | 0.265 | [-0.0008, 0.0708] |

Diagnosticos: BG_p = 0.912; BP_p = 0.085; JB_p = 0.748; RESET_p = 0.126; CUSUM_stat = 0.514; CUSUM_p = 0.954; VIF_max = 12.790; r2_adj = 0.345; phi_mitad1 = -0.071; phi_mitad2 = -0.212; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.018 | -0.010 | -0.002 | 0.227 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.110 | -0.011 | -0.002 | 0.227 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.080 | -0.052 | 0.148 | 0.227 | True |
| 2014T1-2019T4 | residuo no explicado | 0.215 | 0.301 | 0.084 | 0.227 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.228 | NA | NA | 0.227 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.001 | NA | NA | 0.227 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.010 | 0.005 | 0.001 | 0.010 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.067 | 0.007 | 0.001 | 0.010 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.011 | -0.007 | 0.021 | 0.010 | True |
| 2020T1-2022T2 | residuo no explicado | 0.079 | 0.006 | -0.013 | 0.010 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | 0.010 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.016 | NA | NA | 0.010 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.019 | -0.010 | -0.003 | -0.000 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.044 | 0.005 | 0.001 | -0.000 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.047 | -0.030 | 0.086 | -0.000 | True |
| 2022T3-ultimo | residuo no explicado | 0.110 | 0.036 | -0.084 | -0.000 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.003 | NA | NA | -0.000 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.003 | NA | NA | -0.000 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.084 -0.088\,(\text{ln\_ipv}_{t-1} - [0.039\,\text{tasa\_paro\_epa}_{t-1} + 0.538\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.048\,\text{d\_ln\_hip\_importe\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.088; semivida = 7.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.039, ln_hip_importe = 0.538.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0020 | 0.0018 | 1.10 | 0.276 | 0.641 | [-0.0016, 0.0056] |
| d_ln_hip_importe_L0 | 0.0482 | 0.0137 | 3.52 | 0.001 | 0.039 | [0.0209, 0.0756] |
| d_ln_compraventas | 0.0349 | 0.0166 | 2.10 | 0.039 | 0.221 | [0.0018, 0.0680] |

Diagnosticos: BG_p = 0.867; BP_p = 0.073; JB_p = 0.315; RESET_p = 0.020; CUSUM_stat = 0.492; CUSUM_p = 0.969; VIF_max = 5.679; r2_adj = 0.385; phi_mitad1 = -0.185; phi_mitad2 = -0.206; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.007 | -0.009 | 0.003 | 0.227 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.162 | 0.223 | 0.027 | 0.227 | True |
| 2014T1-2019T4 | residuo no explicado | 0.072 | 0.012 | 0.197 | 0.227 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.250 | NA | NA | 0.227 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.023 | NA | NA | 0.227 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.028 | -0.034 | 0.012 | 0.010 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.098 | -0.135 | -0.016 | 0.010 | True |
| 2020T1-2022T2 | residuo no explicado | 0.137 | 0.179 | 0.015 | 0.010 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.001 | NA | NA | 0.010 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.010 | NA | NA | 0.010 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.009 | 0.011 | -0.004 | 0.009 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0.034 | -0.046 | -0.006 | 0.009 | True |
| 2022T3-ultimo | residuo no explicado | 0.033 | 0.044 | 0.018 | 0.009 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.017 | NA | NA | 0.009 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.026 | NA | NA | 0.009 | True |
