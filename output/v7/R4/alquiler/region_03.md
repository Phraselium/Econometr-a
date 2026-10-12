# Region 03, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.020 +0.022\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.610\,\text{ln\_ocupados}_{t-1} + -2.081\,\text{ln\_pob\_total}_{t-1}]) -0.007\,\text{d\_ln\_ocupados\_L0} +1.114\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.022; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.610, ln_pob_total = -2.081.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0067 | 0.0142 | -0.47 | 0.638 | 0.867 | [-0.0352, 0.0217] |
| d_ln_pob_total_L0 | 1.1137 | 0.4216 | 2.64 | 0.010 | 0.274 | [0.2717, 1.9557] |
| d_ln_hip_importe | -0.0019 | 0.0014 | -1.35 | 0.183 | 0.583 | [-0.0048, 0.0009] |

Diagnosticos: BG_p = 0.633; BP_p = 0.017; JB_p = 0.000; RESET_p = 0.908; CUSUM_stat = 0.515; CUSUM_p = 0.953; VIF_max = 1.109; r2_adj = 0.164; phi_mitad1 = 0.067; phi_mitad2 = -0.132; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.008 | -0.003 | -0.000 | 0.006 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.042 | -0.040 | -0.008 | 0.006 | True |
| 2014T1-2019T4 | residuo no explicado | 0.057 | 0.049 | 0.015 | 0.006 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.005 | NA | NA | 0.006 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.001 | NA | NA | 0.006 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.007 | -0.002 | -0.000 | -0.003 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.018 | -0.017 | -0.003 | -0.003 | True |
| 2020T1-2022T2 | residuo no explicado | 0.021 | 0.015 | 0.000 | -0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.008 | NA | NA | -0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.004 | NA | NA | -0.003 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.006 | 0.002 | 0.000 | -0.010 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.014 | -0.013 | -0.003 | -0.010 | False |
| 2022T3-ultimo | residuo no explicado | -0.003 | 0.001 | -0.008 | -0.010 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.010 | False |
| 2022T3-ultimo | ECM propio: residuo | -0.005 | NA | NA | -0.010 | False |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.013\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.172\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.013; semivida = 51.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.016.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0002 | -0.48 | 0.633 | 0.751 | [-0.0005, 0.0003] |
| d_y_L1 | 0.1717 | 0.1114 | 1.54 | 0.128 | 0.384 | [-0.0505, 0.3939] |
| d_ln_hip_importe | -0.0022 | 0.0014 | -1.55 | 0.125 | 0.384 | [-0.0050, 0.0006] |

Diagnosticos: BG_p = 0.149; BP_p = 0.068; JB_p = 0.281; RESET_p = 0.866; CUSUM_stat = 0.822; CUSUM_p = 0.508; VIF_max = 1.000; r2_adj = 0.080; phi_mitad1 = 0.021; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.007 | 0.007 | 0.001 | 0.006 | True |
| 2014T1-2019T4 | residuo no explicado | 0.014 | -0.001 | 0.005 | 0.006 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.006 | NA | NA | 0.006 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.000 | NA | NA | 0.006 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.008 | 0.008 | 0.001 | -0.003 | True |
| 2020T1-2022T2 | residuo no explicado | 0.004 | -0.011 | -0.004 | -0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.002 | NA | NA | -0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.003 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.000 | 0.000 | 0.000 | -0.009 | True |
| 2022T3-ultimo | residuo no explicado | -0.008 | -0.009 | -0.009 | -0.009 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.008 | NA | NA | -0.009 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.001 | NA | NA | -0.009 | True |
