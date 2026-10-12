# Region 08, mercado compra (informativo, muestra ya vista en v1; capa C4; asociacion, sin lectura causal)

## Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.042 -0.045\,(\text{ln\_ipv}_{t-1} - [3.379\,\text{ln\_ocupados}_{t-1} + 0.225\,\text{ln\_hip\_importe}_{t-1} + 9.014\,\text{ln\_pob\_total}_{t-1}]) -0.009\,\text{d\_ln\_ocupados\_L0} -0.011\,\text{d\_ln\_hip\_importe\_L0} +0.258\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.045; semivida = 15.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 3.379, ln_hip_importe = 0.225, ln_pob_total = 9.014.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0093 | 0.0928 | -0.10 | 0.920 | 0.982 | [-0.1948, 0.1762] |
| d_ln_hip_importe_L0 | -0.0114 | 0.0103 | -1.10 | 0.273 | 0.600 | [-0.0319, 0.0092] |
| d_ln_pob_total_L0 | 0.2576 | 1.5799 | 0.16 | 0.871 | 0.962 | [-2.8996, 3.4147] |
| d_ln_compraventas | -0.0027 | 0.0143 | -0.19 | 0.852 | 0.962 | [-0.0313, 0.0259] |

Diagnosticos: BG_p = 0.158; BP_p = 0.281; JB_p = 0.006; RESET_p = 0.682; CUSUM_stat = 0.369; CUSUM_p = 0.999; VIF_max = 2.281; r2_adj = 0.192; phi_mitad1 = -0.397; phi_mitad2 = -0.008; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0.002 | -0.001 | -0.000 | -0.092 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.080 | -0.008 | -0.002 | -0.092 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0.046 | 0.030 | -0.085 | -0.092 | True |
| 2014T1-2019T4 | residuo no explicado | -0.216 | -0.112 | -0.005 | -0.092 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.133 | NA | NA | -0.092 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0.041 | NA | NA | -0.092 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0.005 | 0.002 | 0.001 | -0.044 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.067 | 0.007 | 0.001 | -0.044 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0.007 | -0.004 | 0.012 | -0.044 | True |
| 2020T1-2022T2 | residuo no explicado | 0.024 | -0.049 | -0.058 | -0.044 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.044 | NA | NA | -0.044 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0.000 | NA | NA | -0.044 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0.004 | 0.002 | 0.001 | -0.048 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.004 | -0.000 | -0.000 | -0.048 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0.009 | -0.006 | 0.016 | -0.048 | True |
| 2022T3-ultimo | residuo no explicado | -0.047 | -0.044 | -0.064 | -0.048 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.029 | NA | NA | -0.048 | True |
| 2022T3-ultimo | ECM propio: residuo | -0.019 | NA | NA | -0.048 | True |

## Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.003 +0.006\,(\text{ln\_ipv}_{t-1} - [0.205\,\text{tasa\_paro\_epa}_{t-1} + -0.994\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.013\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = 0.006; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.205, ln_hip_importe = -0.994.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0009 | 0.0013 | 0.71 | 0.480 | 0.874 | [-0.0017, 0.0035] |
| d_ln_hip_importe_L0 | -0.0127 | 0.0104 | -1.22 | 0.225 | 0.610 | [-0.0335, 0.0080] |
| d_ln_compraventas | -0.0038 | 0.0140 | -0.27 | 0.789 | 0.894 | [-0.0317, 0.0242] |

Diagnosticos: BG_p = 0.193; BP_p = 0.330; JB_p = 0.004; RESET_p = 0.503; CUSUM_stat = 0.741; CUSUM_p = 0.642; VIF_max = 3.132; r2_adj = 0.132; phi_mitad1 = -0.048; phi_mitad2 = -0.036; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

Descomposicion historica (contabilidad descriptiva; coeficientes no confirmados; rango entre MG_dm, PMG_dm y CS-DL):

| periodo | componente | MG_dm | PMG_dm | CS-DL | variacion observada | no atribuible |
|---|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(tasa_paro_epa) | 0.023 | 0.027 | -0.009 | -0.092 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | 0.118 | 0.163 | 0.020 | -0.092 | True |
| 2014T1-2019T4 | residuo no explicado | -0.233 | -0.282 | -0.102 | -0.092 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.091 | NA | NA | -0.092 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0.001 | NA | NA | -0.092 | True |
| 2020T1-2022T2 | theta*d(tasa_paro_epa) | -0.024 | -0.028 | 0.010 | -0.044 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0.096 | -0.132 | -0.016 | -0.044 | True |
| 2020T1-2022T2 | residuo no explicado | 0.075 | 0.116 | -0.038 | -0.044 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.022 | NA | NA | -0.044 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0.022 | NA | NA | -0.044 | True |
| 2022T3-ultimo | theta*d(tasa_paro_epa) | 0.002 | 0.002 | -0.001 | -0.057 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | 0.056 | 0.077 | 0.009 | -0.057 | True |
| 2022T3-ultimo | residuo no explicado | -0.115 | -0.137 | -0.066 | -0.057 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0.069 | NA | NA | -0.057 | True |
| 2022T3-ultimo | ECM propio: residuo | 0.012 | NA | NA | -0.057 | True |
