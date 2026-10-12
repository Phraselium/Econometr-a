# Region 10, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.179 -0.188\,(\text{ln\_ipv}_{t-1} - [0.213\,\text{ln\_ocupados}_{t-1} + -0.104\,\text{ln\_hip\_importe}_{t-1} + -1.093\,\text{ln\_pob\_total}_{t-1}]) -0.032\,\text{d\_ln\_ocupados\_L0} -0.023\,\text{d\_ln\_hip\_importe\_L0} +2.330\,\text{d\_ln\_pob\_total\_L0} -0.034\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.188; semivida = 3.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.213, ln_hip_importe = -0.104, ln_pob_total = -1.093.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0324 | 0.0806 | -0.40 | 0.689 | 0.900 | [-0.1933, 0.1286] |
| d_ln_hip_importe_L0 | -0.0226 | 0.0132 | -1.71 | 0.092 | 0.316 | [-0.0490, 0.0038] |
| d_ln_pob_total_L0 | 2.3298 | 1.6094 | 1.45 | 0.153 | 0.443 | [-0.8864, 5.5459] |
| d_ln_compraventas | -0.0341 | 0.0147 | -2.32 | 0.024 | 0.146 | [-0.0635, -0.0047] |

Diagnosticos: BG_p = 0.275; BP_p = 0.009; JB_p = 0.001; RESET_p = 0.001; CUSUM_stat = 0.738; CUSUM_p = 0.648; VIF_max = 5.094; r2_adj = 0.164; phi_mitad1 = -0.249; phi_mitad2 = -0.415; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.012 | -0.006 | -0.002 | 0.000 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.073 | -0.008 | -0.002 | 0.000 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.012 | -0.008 | 0.022 | 0.000 | True |
| 2014T1-2019T4 | residuo no explicado | -0.049 | 0.022 | -0.018 | 0.000 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.030 | NA | NA | 0.000 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.030 | NA | NA | 0.000 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.011 | -0.006 | -0.001 | 0.001 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.053 | 0.005 | 0.001 | 0.001 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.027 | -0.018 | 0.051 | 0.001 | True |
| 2020T1-2022T2 | residuo no explicado | 0.092 | 0.020 | -0.049 | 0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.021 | NA | NA | 0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.020 | NA | NA | 0.001 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0.012 | -0.006 | -0.002 | 0.005 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.020 | -0.002 | -0.000 | 0.005 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.059 | -0.038 | 0.108 | 0.005 | True |
| 2022T3-ultimo | residuo no explicado | 0.055 | 0.051 | -0.102 | 0.005 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.000 | NA | NA | 0.005 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.005 | NA | NA | 0.005 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.013 -0.173\,(\text{ln\_ipv}_{t-1} - [-0.006\,\text{tasa\_paro\_epa}_{t-1} + -0.080\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.016\,\text{d\_ln\_hip\_importe\_L0} -0.032\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.173; semivida = 3.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.006, ln_hip_importe = -0.080.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0011 | 0.29 | 0.775 | 0.894 | [-0.0019, 0.0025] |
| d_ln_hip_importe_L0 | -0.0162 | 0.0123 | -1.32 | 0.193 | 0.596 | [-0.0408, 0.0084] |
| d_ln_compraventas | -0.0321 | 0.0136 | -2.36 | 0.021 | 0.178 | [-0.0592, -0.0050] |

Diagnosticos: BG_p = 0.244; BP_p = 0.001; JB_p = 0.000; RESET_p = 0.001; CUSUM_stat = 0.882; CUSUM_p = 0.418; VIF_max = 2.015; r2_adj = 0.150; phi_mitad1 = -0.205; phi_mitad2 = -0.248; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.032 | 0.038 | -0.013 | 0.000 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.108 | 0.149 | 0.018 | 0.000 | True |
| 2014T1-2019T4 | residuo no explicado | -0.140 | -0.186 | -0.005 | 0.000 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.026 | NA | NA | 0.000 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.027 | NA | NA | 0.000 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.009 | 0.011 | -0.004 | 0.001 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.076 | -0.104 | -0.013 | 0.001 | True |
| 2020T1-2022T2 | residuo no explicado | 0.068 | 0.094 | 0.018 | 0.001 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.021 | NA | NA | 0.001 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.020 | NA | NA | 0.001 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.007 | -0.008 | 0.003 | 0.012 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.068 | 0.093 | 0.011 | 0.012 | True |
| 2022T3-ultimo | residuo no explicado | -0.049 | -0.073 | -0.003 | 0.012 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.006 | NA | NA | 0.012 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.017 | NA | NA | 0.012 | True |
