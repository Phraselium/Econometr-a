# Region 01, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.482 -0.008\,(\text{ln\_ipv}_{t-1} - [-9.625\,\text{ln\_ocupados}_{t-1} + 2.713\,\text{ln\_hip\_importe}_{t-1} + -32.573\,\text{ln\_pob\_total}_{t-1}]) -0.125\,\text{d\_ln\_ocupados\_L0} +0.035\,\text{d\_ln\_hip\_importe\_L0} -0.058\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.008; semivida = 83.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -9.625, ln_hip_importe = 2.713, ln_pob_total = -32.573.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.1253 | 0.0509 | -2.46 | 0.017 | 0.123 | [-0.2269, -0.0236] |
| d_ln_hip_importe_L0 | 0.0353 | 0.0128 | 2.76 | 0.008 | 0.102 | [0.0098, 0.0608] |
| d_ln_pob_total_L0 | -0.0580 | 1.7133 | -0.03 | 0.973 | 0.988 | [-3.4817, 3.3657] |
| d_ln_compraventas | -0.0144 | 0.0159 | -0.91 | 0.368 | 0.735 | [-0.0463, 0.0174] |

Diagnosticos: BG_p = 0.003; BP_p = 0.060; JB_p = 0.232; RESET_p = 0.778; CUSUM_stat = 0.424; CUSUM_p = 0.994; VIF_max = 10.813; r2_adj = 0.089; phi_mitad1 = -0.455; phi_mitad2 = -0.153; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.029 | -0.016 | -0.004 | 0.016 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.077 | -0.008 | -0.002 | 0.016 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.002 | -0.001 | 0.003 | 0.016 | True |
| 2014T1-2019T4 | residuo no explicado | -0.031 | 0.040 | 0.018 | 0.016 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.035 | NA | NA | 0.016 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.020 | NA | NA | 0.016 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.008 | -0.004 | -0.001 | 0.029 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.003 | -0.000 | -0.000 | 0.029 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.006 | -0.004 | 0.012 | 0.029 | True |
| 2020T1-2022T2 | residuo no explicado | 0.040 | 0.038 | 0.018 | 0.029 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.024 | NA | NA | 0.029 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.005 | NA | NA | 0.029 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.006 | -0.003 | -0.001 | 0.038 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.016 | -0.002 | -0.000 | 0.038 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.015 | 0.010 | -0.028 | 0.038 | True |
| 2022T3-ultimo | residuo no explicado | 0.012 | 0.033 | 0.068 | 0.038 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.030 | NA | NA | 0.038 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.008 | NA | NA | 0.038 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.036 -0.053\,(\text{ln\_ipv}_{t-1} - [0.011\,\text{tasa\_paro\_epa}_{t-1} + 0.343\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.012\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.053; semivida = 12.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.011, ln_hip_importe = 0.343.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0015 | 0.0008 | 2.04 | 0.045 | 0.231 | [0.0000, 0.0031] |
| d_ln_hip_importe_L0 | 0.0277 | 0.0123 | 2.25 | 0.027 | 0.199 | [0.0032, 0.0523] |
| d_ln_compraventas | -0.0117 | 0.0158 | -0.74 | 0.461 | 0.871 | [-0.0432, 0.0198] |

Diagnosticos: BG_p = 0.033; BP_p = 0.215; JB_p = 0.240; RESET_p = 0.571; CUSUM_stat = 0.601; CUSUM_p = 0.863; VIF_max = 4.630; r2_adj = 0.094; phi_mitad1 = -0.148; phi_mitad2 = -0.070; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.069 | 0.082 | -0.028 | 0.016 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.114 | 0.157 | 0.019 | 0.016 | True |
| 2014T1-2019T4 | residuo no explicado | -0.168 | -0.224 | 0.025 | 0.016 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.058 | NA | NA | 0.016 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.042 | NA | NA | 0.016 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.011 | 0.014 | -0.005 | 0.028 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.006 | 0.008 | 0.001 | 0.028 | True |
| 2020T1-2022T2 | residuo no explicado | 0.011 | 0.007 | 0.032 | 0.028 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.027 | NA | NA | 0.028 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.001 | NA | NA | 0.028 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.026 | 0.031 | -0.011 | 0.029 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.046 | 0.063 | 0.008 | 0.029 | True |
| 2022T3-ultimo | residuo no explicado | -0.043 | -0.065 | 0.032 | 0.029 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.009 | NA | NA | 0.029 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.020 | NA | NA | 0.029 | True |
