# Region 14, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.010 -0.068\,(\text{ln\_ipv}_{t-1} - [0.643\,\text{ln\_ocupados}_{t-1} + 0.126\,\text{ln\_hip\_importe}_{t-1} + -1.851\,\text{ln\_pob\_total}_{t-1}]) -0.086\,\text{d\_ln\_ocupados\_L0} +0.018\,\text{d\_ln\_hip\_importe\_L0} -2.960\,\text{d\_ln\_pob\_total\_L0} -0.008\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.068; semivida = 9.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.643, ln_hip_importe = 0.126, ln_pob_total = -1.851.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0859 | 0.0847 | -1.01 | 0.314 | 0.668 | [-0.2552, 0.0833] |
| d_ln_hip_importe_L0 | 0.0176 | 0.0123 | 1.43 | 0.156 | 0.443 | [-0.0069, 0.0421] |
| d_ln_pob_total_L0 | -2.9604 | 2.6060 | -1.14 | 0.260 | 0.600 | [-8.1681, 2.2472] |
| d_ln_compraventas | -0.0077 | 0.0128 | -0.60 | 0.549 | 0.860 | [-0.0333, 0.0179] |

Diagnosticos: BG_p = 0.485; BP_p = 0.092; JB_p = 0.820; RESET_p = 0.008; CUSUM_stat = 0.697; CUSUM_p = 0.716; VIF_max = 4.974; r2_adj = 0.184; phi_mitad1 = -0.185; phi_mitad2 = -0.410; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.014 | -0.008 | -0.002 | -0.033 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.038 | -0.004 | -0.001 | -0.033 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0.042 | -0.027 | 0.077 | -0.033 | True |
| 2014T1-2019T4 | residuo no explicado | -0.015 | 0.006 | -0.107 | -0.033 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.020 | NA | NA | -0.033 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.013 | NA | NA | -0.033 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0.005 | -0.003 | -0.001 | 0.006 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.008 | -0.001 | -0.000 | 0.006 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.027 | -0.018 | 0.050 | 0.006 | True |
| 2020T1-2022T2 | residuo no explicado | 0.030 | 0.027 | -0.044 | 0.006 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.014 | NA | NA | 0.006 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.020 | NA | NA | 0.006 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.007 | 0.004 | 0.001 | -0.012 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.053 | -0.006 | -0.001 | -0.012 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.016 | -0.011 | 0.030 | -0.012 | True |
| 2022T3-ultimo | residuo no explicado | -0.057 | 0.000 | -0.042 | -0.012 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.004 | NA | NA | -0.012 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.008 | NA | NA | -0.012 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.006 -0.072\,(\text{ln\_ipv}_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1} + 0.227\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.072; semivida = 9.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.014, ln_hip_importe = 0.227.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0010 | 0.0010 | 0.98 | 0.328 | 0.672 | [-0.0010, 0.0029] |
| d_ln_hip_importe_L0 | 0.0216 | 0.0115 | 1.88 | 0.065 | 0.275 | [-0.0014, 0.0446] |
| d_ln_compraventas | -0.0057 | 0.0126 | -0.46 | 0.650 | 0.894 | [-0.0308, 0.0194] |

Diagnosticos: BG_p = 0.362; BP_p = 0.006; JB_p = 0.955; RESET_p = 0.053; CUSUM_stat = 0.843; CUSUM_p = 0.476; VIF_max = 1.742; r2_adj = 0.160; phi_mitad1 = -0.147; phi_mitad2 = -0.282; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.023 | 0.027 | -0.009 | -0.033 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.057 | 0.078 | 0.009 | -0.033 | True |
| 2014T1-2019T4 | residuo no explicado | -0.112 | -0.137 | -0.033 | -0.033 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.040 | NA | NA | -0.033 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.007 | NA | NA | -0.033 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.015 | 0.018 | -0.006 | 0.007 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | 0.011 | 0.015 | 0.002 | 0.007 | True |
| 2020T1-2022T2 | residuo no explicado | -0.020 | -0.027 | 0.011 | 0.007 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.001 | NA | NA | 0.007 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.007 | NA | NA | 0.007 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.013 | -0.015 | 0.005 | 0.010 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.041 | 0.057 | 0.007 | 0.010 | True |
| 2022T3-ultimo | residuo no explicado | -0.018 | -0.032 | -0.002 | 0.010 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.032 | NA | NA | 0.010 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.022 | NA | NA | 0.010 | True |
