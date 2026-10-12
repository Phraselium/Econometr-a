# Atlas regional: La Rioja (17)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 59,45 | 2019Q4 | 69,86 | +17,5 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 70,21 | 2022Q2 | 78,13 | +11,3 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,86 | 2026Q2 | 113,31 | +41,9 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 93,74 | 2019Q4 | 91,69 | -2,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,15 | 2022Q2 | 94,57 | +2,6 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 95,15 | 2026Q2 | 102,76 | +8,0 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.678 -0.099\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.149\,\text{ln\_ocupados}_{t-1} + 3.708\,\text{ln\_pob\_total}_{t-1}]) +0.015\,\text{d\_ln\_ocupados\_L0} -0.697\,\text{d\_ln\_pob\_total\_L0} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.099; semivida = 6.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.149, ln_pob_total = 3.708.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0155 | 0.0152 | 1.02 | 0.312 | 0.706 | [-0.0149, 0.0459] |
| d_ln_pob_total_L0 | -0.6975 | 0.3594 | -1.94 | 0.057 | 0.396 | [-1.4153, 0.0204] |
| d_ln_hip_importe | 0.0016 | 0.0011 | 1.44 | 0.154 | 0.523 | [-0.0006, 0.0038] |

Diagnosticos: BG_p = 0.049; BP_p = 0.109; JB_p = 0.000; RESET_p = 0.728; CUSUM_stat = 0.366; CUSUM_p = 0.999; VIF_max = 1.089; r2_adj = 0.260; phi_mitad1 = -0.079; phi_mitad2 = -0.055; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.014\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.015\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.105\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.014; semivida = 50.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.015.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0001 | 0.0002 | 0.62 | 0.537 | 0.731 | [-0.0003, 0.0006] |
| d_y_L1 | 0.1053 | 0.1182 | 0.89 | 0.376 | 0.685 | [-0.1304, 0.3410] |
| d_ln_hip_importe | 0.0018 | 0.0013 | 1.44 | 0.153 | 0.434 | [-0.0007, 0.0043] |

Diagnosticos: BG_p = 0.404; BP_p = 0.649; JB_p = 0.000; RESET_p = 0.653; CUSUM_stat = 0.558; CUSUM_p = 0.915; VIF_max = 1.000; r2_adj = 0.062; phi_mitad1 = 0.004; phi_mitad2 = -0.148; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,099 | 6,6 |
| B | -0,014 | 50,3 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +1.706 -0.179\,(\text{ln\_ipv}_{t-1} - [-0.361\,\text{ln\_ocupados}_{t-1} + 0.086\,\text{ln\_hip\_importe}_{t-1} + 5.646\,\text{ln\_pob\_total}_{t-1}]) +0.094\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +3.661\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.179; semivida = 3.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.361, ln_hip_importe = 0.086, ln_pob_total = 5.646.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0942 | 0.0712 | 1.32 | 0.190 | 0.480 | [-0.0481, 0.2365] |
| d_ln_hip_importe_L0 | 0.0029 | 0.0078 | 0.38 | 0.709 | 0.900 | [-0.0126, 0.0185] |
| d_ln_pob_total_L0 | 3.6609 | 1.8590 | 1.97 | 0.053 | 0.265 | [-0.0541, 7.3759] |
| d_ln_compraventas | -0.0021 | 0.0070 | -0.30 | 0.761 | 0.900 | [-0.0161, 0.0118] |

Diagnosticos: BG_p = 0.565; BP_p = 0.001; JB_p = 0.987; RESET_p = 0.524; CUSUM_stat = 0.650; CUSUM_p = 0.792; VIF_max = 1.842; r2_adj = 0.107; phi_mitad1 = -0.379; phi_mitad2 = -0.453; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.028 -0.066\,(\text{ln\_ipv}_{t-1} - [0.024\,\text{tasa\_paro\_epa}_{t-1} + 0.185\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.001\,\text{d\_ln\_hip\_importe\_L0} +0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.066; semivida = 10.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.024, ln_hip_importe = 0.185.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0010 | 0.39 | 0.696 | 0.894 | [-0.0016, 0.0024] |
| d_ln_hip_importe_L0 | 0.0015 | 0.0075 | 0.20 | 0.844 | 0.915 | [-0.0134, 0.0164] |
| d_ln_compraventas | 0.0013 | 0.0070 | 0.19 | 0.851 | 0.915 | [-0.0127, 0.0153] |

Diagnosticos: BG_p = 0.171; BP_p = 0.011; JB_p = 0.866; RESET_p = 0.909; CUSUM_stat = 0.868; CUSUM_p = 0.438; VIF_max = 1.352; r2_adj = 0.031; phi_mitad1 = -0.052; phi_mitad2 = -0.239; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,179 | 3,5 |
| B | -0,066 | 10,1 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,049 | 0,109 | 0,000 | 0,728 | 0,999 | 1,09 | 0,26 | -0,079 | -0,055 | False |
| alquiler | B | 0,404 | 0,649 | 0,000 | 0,653 | 0,915 | 1,00 | 0,06 | 0,004 | -0,148 | True |
| compra | A | 0,565 | 0,001 | 0,987 | 0,524 | 0,792 | 1,84 | 0,11 | -0,379 | -0,453 | False |
| compra | B | 0,171 | 0,011 | 0,866 | 0,909 | 0,438 | 1,35 | 0,03 | -0,052 | -0,239 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0019 | -0,0001 | -0,0421 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0019 | -0,0004 | -0,0421 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0417 | -0,0383 | -0,0421 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0428 | -0,0428 | -0,0421 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0,0007 | 0,0007 | -0,0421 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0025 | -0,0001 | 0,0015 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0,0002 | 0,0008 | 0,0015 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0014 | 0,0032 | 0,0015 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0034 | 0,0034 | 0,0015 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0019 | -0,0019 | 0,0015 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0014 | -0,0000 | -0,0089 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0043 | -0,0008 | -0,0089 | False |
| 2022T3-ultimo | residuo no explicado | -0,0080 | -0,0032 | -0,0089 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0115 | -0,0115 | -0,0089 | False |
| 2022T3-ultimo | ECM propio: residuo | 0,0027 | 0,0027 | -0,0089 | False |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0013 | 0,0098 | -0,0360 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0633 | 0,0066 | -0,0360 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0077 | 0,0042 | -0,0360 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0505 | 0,0134 | -0,0360 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0605 | -0,0605 | -0,0360 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0,0246 | 0,0246 | -0,0360 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0018 | 0,0130 | -0,0107 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0125 | 0,1198 | -0,0107 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0018 | 0,0033 | -0,0107 | True |
| 2020T1-2022T2 | residuo no explicado | -0,1417 | -0,0040 | -0,0107 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0168 | 0,0168 | -0,0107 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0275 | -0,0275 | -0,0107 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0010 | 0,0073 | 0,0129 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0675 | 0,0070 | 0,0129 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0173 | 0,0094 | 0,0129 | True |
| 2022T3-ultimo | residuo no explicado | -0,0042 | 0,0637 | 0,0129 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0023 | 0,0023 | 0,0129 | True |
| 2022T3-ultimo | ECM propio: residuo | 0,0106 | 0,0106 | 0,0129 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_17.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,417 | 0,655 | sí | 0,399 | no |
| compra | ar4 | 3,200 | 5,128 | sí | 2,489 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 2, 5 y 10 años, con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| a_construccion | alquiler | 2 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| a_construccion | alquiler | 5 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| a_construccion | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| a_construccion | precio | 2 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| a_construccion | precio | 5 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| a_construccion | precio | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| b_vacias | alquiler | 2 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | sí |
| b_vacias | alquiler | 5 | -1,2 % [-2,5 %, -0,6 %] | -1,2 % [-2,5 %, -0,6 %] | sí |
| b_vacias | alquiler | 10 | -3,0 % [-6,6 %, -1,5 %] | -3,0 % [-6,6 %, -1,5 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | sí |
| b_vacias | precio | 10 | -1,1 % [-2,1 %, -0,6 %] | -1,1 % [-2,1 %, -0,6 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,2 % [-0,3 %, -0,1 %] | -0,2 % [-0,3 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 5 | -1,0 % [-2,2 %, -0,4 %] | -1,0 % [-2,2 %, -0,4 %] | sí |
| c_vivienda_publica | alquiler | 10 | -2,6 % [-5,8 %, -1,1 %] | -2,6 % [-5,8 %, -1,1 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | precio | 5 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | sí |
| c_vivienda_publica | precio | 10 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| d_turisticos | alquiler | 2 | -0,3 % [-0,7 %, -0,1 %] | -0,3 % [-0,7 %, -0,1 %] | sí |
| d_turisticos | alquiler | 5 | -0,5 % [-1,2 %, -0,2 %] | -0,5 % [-1,2 %, -0,2 %] | sí |
| d_turisticos | alquiler | 10 | -0,6 % [-1,4 %, -0,2 %] | -0,6 % [-1,4 %, -0,2 %] | sí |
| d_turisticos | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 5 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| d_turisticos | precio | 10 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| e_ayuda_demanda | alquiler | 2 | +2,2 % [+1,0 %, +4,3 %] | -2,7 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | alquiler | 5 | +3,6 % [+1,6 %, +7,0 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,2 % [+1,9 %, +8,1 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| e_ayuda_demanda | precio | 2 | +2,2 % [+1,0 %, +4,3 %] | -2,7 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | precio | 5 | +3,6 % [+1,6 %, +7,0 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | precio | 10 | +4,2 % [+1,9 %, +8,1 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,5 % [+0,2 %, +1,1 %] | -0,6 % [-1,3 %, -0,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +0,9 % [+0,4 %, +1,8 %] | -1,1 % [-2,0 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,6 % [-1,1 %, -0,2 %] | -0,6 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,6 % [-1,1 %, -0,2 %] | -0,6 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (precio; robusto solo con rejilla (regional no utilizable)); d_turisticos (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó diagnósticos en 0 de 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 7. Qué no se puede afirmar

- Que haya una relación de largo plazo estable entre precios o alquileres y empleo, población, hipotecas o paro: ninguna hipótesis confirmatoria de R4 se confirmó (p de Holm ≥ 0,05).
- Que la velocidad de ajuste de la región sea distinta de cero o de la del resto: no hay inferencia válida individual.
- Que la descomposición atribuya la variación a un factor: el residuo domina y los coeficientes no están confirmados.
- Que el mejor modelo del backtest vaya a predecir mejor en el futuro: muestra ya vista en v1 y selección en muestra.
- Que una propuesta produzca los impactos de la tabla: son escenarios condicionales con supuestos (C4), no estimaciones identificadas.
- Nada de lo anterior es causal: la evidencia queda por debajo del nivel CAUSAL.

---
*Capas: variaciones de índices C4 (fuente única regional); ECM, descomposición y backtest C4; propuestas C4 condicional. informativo, muestra ya vista en v1. Validación diferida pendiente: los modelos están congelados (R5) y se evaluarán con `make evaluate_v7` sobre datos posteriores.*
