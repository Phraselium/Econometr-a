# Region 05, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.064 -0.318\,(\text{ln\_ipv}_{t-1} - [0.151\,\text{ln\_ocupados}_{t-1} + -0.004\,\text{ln\_hip\_importe}_{t-1} + 1.080\,\text{ln\_pob\_total}_{t-1}]) +0.098\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +2.245\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.318; semivida = 1.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.151, ln_hip_importe = -0.004, ln_pob_total = 1.080.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0982 | 0.0509 | 1.93 | 0.058 | 0.265 | [-0.0036, 0.1999] |
| d_ln_hip_importe_L0 | -0.0006 | 0.0120 | -0.05 | 0.959 | 0.988 | [-0.0246, 0.0234] |
| d_ln_pob_total_L0 | 2.2455 | 2.8921 | 0.78 | 0.440 | 0.768 | [-3.5339, 8.0249] |
| d_ln_compraventas | -0.0026 | 0.0088 | -0.30 | 0.768 | 0.900 | [-0.0201, 0.0149] |

Diagnosticos: BG_p = 0.055; BP_p = 0.163; JB_p = 0.010; RESET_p = 0.489; CUSUM_stat = 0.638; CUSUM_p = 0.810; VIF_max = 15.545; r2_adj = 0.137; phi_mitad1 = -0.676; phi_mitad2 = -0.785; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.049 | -0.026 | -0.007 | 0.012 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.053 | -0.006 | -0.001 | 0.012 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.053 | -0.035 | 0.098 | 0.012 | True |
| 2014T1-2019T4 | residuo no explicado | 0.061 | 0.078 | -0.079 | 0.012 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.002 | NA | NA | 0.012 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.009 | NA | NA | 0.012 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.058 | -0.031 | -0.008 | 0.039 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.095 | 0.010 | 0.002 | 0.039 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.008 | -0.005 | 0.014 | 0.039 | True |
| 2020T1-2022T2 | residuo no explicado | 0.199 | 0.065 | 0.030 | 0.039 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.056 | NA | NA | 0.039 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.017 | NA | NA | 0.039 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.029 | -0.016 | -0.004 | 0.021 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.054 | -0.006 | -0.001 | 0.021 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.010 | -0.006 | 0.018 | 0.021 | True |
| 2022T3-ultimo | residuo no explicado | 0.006 | 0.049 | 0.009 | 0.021 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.011 | NA | NA | 0.021 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.011 | NA | NA | 0.021 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.102\,(\text{ln\_ipv}_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.107\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.003\,\text{d\_ln\_hip\_importe\_L0} -0.007\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.102; semivida = 6.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.005, ln_hip_importe = -0.107.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0016 | 0.0008 | -1.99 | 0.051 | 0.236 | [-0.0033, 0.0000] |
| d_ln_hip_importe_L0 | -0.0034 | 0.0122 | -0.28 | 0.781 | 0.894 | [-0.0278, 0.0210] |
| d_ln_compraventas | -0.0068 | 0.0090 | -0.76 | 0.453 | 0.871 | [-0.0248, 0.0112] |

Diagnosticos: BG_p = 0.013; BP_p = 0.649; JB_p = 0.007; RESET_p = 0.678; CUSUM_stat = 0.770; CUSUM_p = 0.594; VIF_max = 1.683; r2_adj = 0.055; phi_mitad1 = -0.084; phi_mitad2 = -0.416; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.052 | 0.061 | -0.021 | 0.012 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.078 | 0.108 | 0.013 | 0.012 | True |
| 2014T1-2019T4 | residuo no explicado | -0.119 | -0.158 | 0.020 | 0.012 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.014 | NA | NA | 0.012 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.026 | NA | NA | 0.012 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.079 | 0.094 | -0.032 | 0.037 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.140 | -0.192 | -0.023 | 0.037 | True |
| 2020T1-2022T2 | residuo no explicado | 0.098 | 0.136 | 0.093 | 0.037 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.021 | NA | NA | 0.037 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.017 | NA | NA | 0.037 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.058 | 0.069 | -0.024 | -0.005 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.095 | 0.130 | 0.016 | -0.005 | True |
| 2022T3-ultimo | residuo no explicado | -0.158 | -0.205 | 0.003 | -0.005 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.009 | NA | NA | -0.005 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.014 | NA | NA | -0.005 | True |
