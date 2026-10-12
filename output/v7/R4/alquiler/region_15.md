# Region 15, mercado alquiler (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.015 -0.032\,(\text{ln\_ipc\_alquiler}_{t-1} - [-1.191\,\text{ln\_ocupados}_{t-1} + 0.748\,\text{ln\_pob\_total}_{t-1}]) -0.044\,\text{d\_ln\_ocupados\_L0} +1.579\,\text{d\_ln\_pob\_total\_L0} -0.005\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.032; semivida = 21.0 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.191, ln_pob_total = 0.748.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0436 | 0.0256 | -1.70 | 0.093 | 0.396 | [-0.0946, 0.0075] |
| d_ln_pob_total_L0 | 1.5791 | 0.8796 | 1.80 | 0.077 | 0.396 | [-0.1777, 3.3359] |
| d_ln_hip_importe | -0.0053 | 0.0023 | -2.26 | 0.027 | 0.274 | [-0.0100, -0.0006] |

Diagnosticos: BG_p = 0.308; BP_p = 0.125; JB_p = 0.000; RESET_p = 0.513; CUSUM_stat = 0.576; CUSUM_p = 0.895; VIF_max = 1.315; r2_adj = 0.285; phi_mitad1 = -0.116; phi_mitad2 = -0.125; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.003 | -0.001 | -0.000 | 0.000 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.022 | 0.021 | 0.004 | 0.000 | True |
| 2014T1-2019T4 | residuo no explicado | -0.019 | -0.020 | -0.004 | 0.000 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.001 | NA | NA | 0.000 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.000 | NA | NA | 0.000 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.000 | -0.000 | -0.000 | -0.002 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.006 | 0.005 | 0.001 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.007 | -0.007 | -0.003 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.002 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.001 | 0.000 | 0.000 | -0.006 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.001 | 0.001 | 0.000 | -0.006 | True |
| 2022T3-ultimo | residuo no explicado | -0.008 | -0.007 | -0.006 | -0.006 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | -0.006 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.000 | NA | NA | -0.006 | True |

## Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.039\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.285\,\text{d\_y\_L1} -0.004\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.039; semivida = 17.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0003 | 1.27 | 0.209 | 0.509 | [-0.0002, 0.0009] |
| d_y_L1 | 0.2846 | 0.0930 | 3.06 | 0.003 | 0.027 | [0.0991, 0.4700] |
| d_ln_hip_importe | -0.0045 | 0.0019 | -2.30 | 0.025 | 0.120 | [-0.0084, -0.0006] |

Diagnosticos: BG_p = 0.997; BP_p = 0.332; JB_p = 0.006; RESET_p = 0.764; CUSUM_stat = 0.748; CUSUM_p = 0.631; VIF_max = 1.000; r2_adj = 0.381; phi_mitad1 = -0.047; phi_mitad2 = 0.003; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.014 | 0.014 | 0.002 | 0.000 | True |
| 2014T1-2019T4 | residuo no explicado | 0.015 | -0.014 | -0.001 | 0.000 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.007 | NA | NA | 0.000 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.007 | NA | NA | 0.000 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.000 | -0.000 | -0.000 | -0.002 | True |
| 2020T1-2022T2 | residuo no explicado | -0.002 | -0.002 | -0.002 | -0.002 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | -0.002 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.004 | NA | NA | -0.002 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.006 | 0.006 | 0.001 | -0.016 | True |
| 2022T3-ultimo | residuo no explicado | -0.010 | -0.022 | -0.017 | -0.016 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | -0.016 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.011 | NA | NA | -0.016 | True |
