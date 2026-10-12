# Region 03, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.170 -0.235\,(\text{ln\_ipv}_{t-1} - [-0.135\,\text{ln\_ocupados}_{t-1} + 0.115\,\text{ln\_hip\_importe}_{t-1} + 1.135\,\text{ln\_pob\_total}_{t-1}]) -0.074\,\text{d\_ln\_ocupados\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} +5.166\,\text{d\_ln\_pob\_total\_L0} -0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.235; semivida = 2.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.135, ln_hip_importe = 0.115, ln_pob_total = 1.135.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0738 | 0.0662 | -1.12 | 0.269 | 0.600 | [-0.2060, 0.0584] |
| d_ln_hip_importe_L0 | 0.0225 | 0.0092 | 2.45 | 0.017 | 0.123 | [0.0042, 0.0408] |
| d_ln_pob_total_L0 | 5.1657 | 2.7942 | 1.85 | 0.069 | 0.292 | [-0.4181, 10.7495] |
| d_ln_compraventas | -0.0009 | 0.0109 | -0.08 | 0.934 | 0.982 | [-0.0227, 0.0209] |

Diagnosticos: BG_p = 0.120; BP_p = 0.426; JB_p = 0.541; RESET_p = 0.260; CUSUM_stat = 0.345; CUSUM_p = 1.000; VIF_max = 3.697; r2_adj = 0.201; phi_mitad1 = -0.217; phi_mitad2 = -0.284; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.043 | 0.023 | 0.006 | -0.064 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.107 | 0.011 | 0.002 | -0.064 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.092 | 0.060 | -0.170 | -0.064 | True |
| 2014T1-2019T4 | residuo no explicado | -0.092 | -0.158 | 0.098 | -0.064 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.056 | NA | NA | -0.064 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.008 | NA | NA | -0.064 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.037 | 0.020 | 0.005 | -0.004 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.055 | -0.006 | -0.001 | -0.004 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.039 | 0.025 | -0.071 | -0.004 | True |
| 2020T1-2022T2 | residuo no explicado | -0.135 | -0.044 | 0.063 | -0.004 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.016 | NA | NA | -0.004 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.012 | NA | NA | -0.004 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.032 | -0.017 | -0.004 | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.024 | -0.002 | -0.001 | -0.002 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.030 | 0.019 | -0.055 | -0.002 | True |
| 2022T3-ultimo | residuo no explicado | -0.024 | -0.002 | 0.057 | -0.002 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.008 | NA | NA | -0.002 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.011 | NA | NA | -0.002 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.017 -0.079\,(\text{ln\_ipv}_{t-1} - [-0.015\,\text{tasa\_paro\_epa}_{t-1} + 0.251\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.002\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.079; semivida = 8.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.015, ln_hip_importe = 0.251.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0009 | 0.0010 | -0.98 | 0.330 | 0.672 | [-0.0029, 0.0010] |
| d_ln_hip_importe_L0 | 0.0224 | 0.0090 | 2.49 | 0.015 | 0.156 | [0.0044, 0.0403] |
| d_ln_compraventas | -0.0021 | 0.0117 | -0.18 | 0.861 | 0.915 | [-0.0253, 0.0212] |

Diagnosticos: BG_p = 0.631; BP_p = 0.139; JB_p = 0.903; RESET_p = 0.411; CUSUM_stat = 1.193; CUSUM_p = 0.116; VIF_max = 2.725; r2_adj = 0.059; phi_mitad1 = -0.205; phi_mitad2 = -0.412; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion relativa a la media de las CCAA (log, demeaning) | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.027 | -0.033 | 0.011 | -0.064 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.158 | -0.218 | -0.027 | -0.064 | True |
| 2014T1-2019T4 | residuo no explicado | 0.122 | 0.187 | -0.048 | -0.064 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.004 | NA | NA | -0.064 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.060 | NA | NA | -0.064 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.030 | -0.035 | 0.012 | -0.003 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.081 | 0.111 | 0.014 | -0.003 | True |
| 2020T1-2022T2 | residuo no explicado | -0.055 | -0.080 | -0.029 | -0.003 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.018 | NA | NA | -0.003 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.022 | NA | NA | -0.003 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.000 | -0.000 | 0.000 | 0.019 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.042 | 0.058 | 0.007 | 0.019 | True |
| 2022T3-ultimo | residuo no explicado | -0.023 | -0.038 | 0.012 | 0.019 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.022 | NA | NA | 0.019 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.002 | NA | NA | 0.019 | True |
