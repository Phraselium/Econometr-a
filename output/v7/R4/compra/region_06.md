# Region 06, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.041 -0.090\,(\text{ln\_ipv}_{t-1} - [-0.529\,\text{ln\_ocupados}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1} + 0.344\,\text{ln\_pob\_total}_{t-1}]) -0.045\,\text{d\_ln\_ocupados\_L0} -0.005\,\text{d\_ln\_hip\_importe\_L0} +1.235\,\text{d\_ln\_pob\_total\_L0} -0.018\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.090; semivida = 7.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.529, ln_hip_importe = -0.196, ln_pob_total = 0.344.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0449 | 0.0920 | -0.49 | 0.627 | 0.900 | [-0.2287, 0.1388] |
| d_ln_hip_importe_L0 | -0.0050 | 0.0121 | -0.41 | 0.683 | 0.900 | [-0.0292, 0.0193] |
| d_ln_pob_total_L0 | 1.2347 | 2.9773 | 0.41 | 0.680 | 0.900 | [-4.7149, 7.1842] |
| d_ln_compraventas | -0.0181 | 0.0130 | -1.39 | 0.168 | 0.457 | [-0.0441, 0.0078] |

Diagnosticos: BG_p = 0.000; BP_p = 0.106; JB_p = 0.803; RESET_p = 0.507; CUSUM_stat = 0.574; CUSUM_p = 0.896; VIF_max = 2.516; r2_adj = 0.012; phi_mitad1 = -0.087; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0.026 | 0.014 | 0.003 | -0.006 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.014 | 0.001 | 0.000 | -0.006 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.031 | 0.020 | -0.058 | -0.006 | True |
| 2014T1-2019T4 | residuo no explicado | -0.050 | -0.042 | 0.048 | -0.006 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.013 | NA | NA | -0.006 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.019 | NA | NA | -0.006 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.008 | 0.005 | 0.001 | 0.029 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.044 | 0.005 | 0.001 | 0.029 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0.001 | 0.000 | -0.001 | 0.029 | True |
| 2020T1-2022T2 | residuo no explicado | 0.064 | 0.019 | 0.028 | 0.029 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.032 | NA | NA | 0.029 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.003 | NA | NA | 0.029 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.003 | 0.002 | 0.000 | 0.007 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.031 | -0.003 | -0.001 | 0.007 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0.024 | 0.016 | -0.045 | 0.007 | True |
| 2022T3-ultimo | residuo no explicado | -0.051 | -0.007 | 0.052 | 0.007 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.005 | NA | NA | 0.007 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.013 | NA | NA | 0.007 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.007 -0.149\,(\text{ln\_ipv}_{t-1} - [0.019\,\text{tasa\_paro\_epa}_{t-1} + -0.067\,\text{ln\_hip\_importe}_{t-1}]) +0.003\,\text{d\_tasa\_paro\_epa\_L0} +0.000\,\text{d\_ln\_hip\_importe\_L0} -0.015\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.149; semivida = 4.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.019, ln_hip_importe = -0.067.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0027 | 0.0012 | 2.15 | 0.035 | 0.221 | [0.0002, 0.0051] |
| d_ln_hip_importe_L0 | 0.0004 | 0.0102 | 0.04 | 0.971 | 0.972 | [-0.0199, 0.0207] |
| d_ln_compraventas | -0.0154 | 0.0118 | -1.30 | 0.197 | 0.596 | [-0.0390, 0.0082] |

Diagnosticos: BG_p = 0.001; BP_p = 0.264; JB_p = 0.849; RESET_p = 0.363; CUSUM_stat = 0.455; CUSUM_p = 0.986; VIF_max = 1.950; r2_adj = 0.092; phi_mitad1 = -0.133; phi_mitad2 = -0.138; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | -0.035 | -0.042 | 0.015 | -0.006 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0.020 | -0.028 | -0.003 | -0.006 | True |
| 2014T1-2019T4 | residuo no explicado | 0.049 | 0.064 | -0.017 | -0.006 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.021 | NA | NA | -0.006 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.027 | NA | NA | -0.006 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | 0.009 | 0.010 | -0.004 | 0.029 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.066 | -0.091 | -0.011 | 0.029 | True |
| 2020T1-2022T2 | residuo no explicado | 0.086 | 0.109 | 0.043 | 0.029 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0.036 | NA | NA | 0.029 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.007 | NA | NA | 0.029 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | -0.023 | -0.028 | 0.010 | 0.012 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.020 | 0.028 | 0.003 | 0.012 | True |
| 2022T3-ultimo | residuo no explicado | 0.015 | 0.012 | -0.001 | 0.012 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.014 | NA | NA | 0.012 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.027 | NA | NA | 0.012 | True |
