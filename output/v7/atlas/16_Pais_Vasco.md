# Atlas regional: País Vasco (16)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 59,81 | 2019Q4 | 71,28 | +19,2 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 73,23 | 2022Q2 | 79,16 | +8,1 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 80,89 | 2026Q2 | 109,33 | +35,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 91,98 | 2019Q4 | 92,65 | +0,7 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,83 | 2022Q2 | 95,17 | +2,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 95,50 | 2026Q2 | 101,27 | +6,0 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.000 +0.005\,(\text{ln\_ipc\_alquiler}_{t-1} - [-6.127\,\text{ln\_ocupados}_{t-1} + 7.205\,\text{ln\_pob\_total}_{t-1}]) +0.006\,\text{d\_ln\_ocupados\_L0} -0.193\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.005; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -6.127, ln_pob_total = 7.205.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0059 | 0.0120 | 0.49 | 0.625 | 0.867 | [-0.0181, 0.0298] |
| d_ln_pob_total_L0 | -0.1927 | 0.4091 | -0.47 | 0.639 | 0.867 | [-1.0097, 0.6242] |
| d_ln_hip_importe | 0.0007 | 0.0017 | 0.44 | 0.664 | 0.868 | [-0.0027, 0.0042] |

Diagnosticos: BG_p = 0.212; BP_p = 0.692; JB_p = 0.647; RESET_p = 0.403; CUSUM_stat = 0.764; CUSUM_p = 0.604; VIF_max = 1.119; r2_adj = 0.191; phi_mitad1 = 0.009; phi_mitad2 = -0.116; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.002 -0.028\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.387\,\text{d\_y\_L1} +0.003\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.028; semivida = 24.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.013.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0002 | 0.0002 | 0.76 | 0.448 | 0.711 | [-0.0003, 0.0007] |
| d_y_L1 | 0.3866 | 0.1117 | 3.46 | 0.001 | 0.009 | [0.1637, 0.6094] |
| d_ln_hip_importe | 0.0031 | 0.0018 | 1.76 | 0.082 | 0.299 | [-0.0004, 0.0067] |

Diagnosticos: BG_p = 0.213; BP_p = 0.546; JB_p = 0.345; RESET_p = 0.085; CUSUM_stat = 0.957; CUSUM_p = 0.319; VIF_max = 1.000; r2_adj = 0.282; phi_mitad1 = -0.054; phi_mitad2 = 0.038; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,005 | NA |
| B | -0,028 | 24,8 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.078 -0.272\,(\text{ln\_ipv}_{t-1} - [-0.086\,\text{ln\_ocupados}_{t-1} + -0.024\,\text{ln\_hip\_importe}_{t-1} + 2.117\,\text{ln\_pob\_total}_{t-1}]) +0.000\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +1.824\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.272; semivida = 2.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.086, ln_hip_importe = -0.024, ln_pob_total = 2.117.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0004 | 0.0701 | 0.01 | 0.996 | 0.996 | [-0.1398, 0.1405] |
| d_ln_hip_importe_L0 | -0.0011 | 0.0138 | -0.08 | 0.939 | 0.982 | [-0.0286, 0.0265] |
| d_ln_pob_total_L0 | 1.8235 | 3.0988 | 0.59 | 0.558 | 0.860 | [-4.3689, 8.0160] |
| d_ln_compraventas | 0.0041 | 0.0132 | 0.31 | 0.755 | 0.900 | [-0.0222, 0.0305] |

Diagnosticos: BG_p = 0.508; BP_p = 0.293; JB_p = 0.888; RESET_p = 0.080; CUSUM_stat = 0.594; CUSUM_p = 0.872; VIF_max = 4.322; r2_adj = 0.093; phi_mitad1 = -0.197; phi_mitad2 = -0.530; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.134\,(\text{ln\_ipv}_{t-1} - [0.003\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.000\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.134; semivida = 4.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.003, ln_hip_importe = 0.055.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0009 | 0.0015 | -0.62 | 0.540 | 0.894 | [-0.0040, 0.0021] |
| d_ln_hip_importe_L0 | 0.0041 | 0.0124 | 0.33 | 0.740 | 0.894 | [-0.0207, 0.0290] |
| d_ln_compraventas | 0.0005 | 0.0131 | 0.04 | 0.972 | 0.972 | [-0.0257, 0.0266] |

Diagnosticos: BG_p = 0.950; BP_p = 0.191; JB_p = 0.931; RESET_p = 0.102; CUSUM_stat = 0.523; CUSUM_p = 0.947; VIF_max = 1.884; r2_adj = 0.073; phi_mitad1 = -0.068; phi_mitad2 = -0.433; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,272 | 2,2 |
| B | -0,134 | 4,8 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,212 | 0,692 | 0,647 | 0,403 | 0,604 | 1,12 | 0,19 | 0,009 | -0,116 | True |
| alquiler | B | 0,213 | 0,546 | 0,345 | 0,085 | 0,319 | 1,00 | 0,28 | -0,054 | 0,038 | True |
| compra | A | 0,508 | 0,293 | 0,888 | 0,080 | 0,872 | 4,32 | 0,09 | -0,197 | -0,530 | False |
| compra | B | 0,950 | 0,191 | 0,931 | 0,102 | 0,947 | 1,88 | 0,07 | -0,068 | -0,433 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0059 | -0,0002 | -0,0068 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0,0015 | 0,0078 | -0,0068 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0124 | -0,0082 | -0,0068 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0047 | -0,0047 | -0,0068 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0021 | -0,0021 | -0,0068 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0021 | -0,0001 | 0,0026 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0054 | -0,0011 | 0,0026 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0037 | 0,0102 | 0,0026 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0061 | -0,0061 | 0,0026 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0,0087 | 0,0087 | 0,0026 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0000 | 0,0000 | -0,0108 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0087 | -0,0017 | -0,0108 | False |
| 2022T3-ultimo | residuo no explicado | -0,0091 | -0,0022 | -0,0108 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0099 | -0,0099 | -0,0108 | False |
| 2022T3-ultimo | ECM propio: residuo | -0,0009 | -0,0009 | -0,0108 | False |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0041 | 0,0308 | -0,0168 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0064 | 0,0620 | -0,0168 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0171 | 0,0315 | -0,0168 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0925 | -0,0157 | -0,0168 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0052 | 0,0052 | -0,0168 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0220 | -0,0220 | -0,0168 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0015 | 0,0112 | -0,0050 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0764 | 0,0079 | -0,0050 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0220 | 0,0119 | -0,0050 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0267 | 0,0483 | -0,0050 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0018 | -0,0018 | -0,0050 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0032 | -0,0032 | -0,0050 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0001 | -0,0000 | 0,0080 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0306 | 0,0032 | 0,0080 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0351 | 0,0190 | 0,0080 | True |
| 2022T3-ultimo | residuo no explicado | -0,0075 | 0,0424 | 0,0080 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0140 | -0,0140 | 0,0080 | True |
| 2022T3-ultimo | ECM propio: residuo | 0,0220 | 0,0220 | 0,0080 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_16.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | mixto | 0,370 | 0,388 | sí | 0,388 | sí |
| compra | gbm | 3,018 | 4,969 | sí | 2,534 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 2, 5 y 10 años, con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| a_construccion | alquiler | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| a_construccion | alquiler | 5 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | sí |
| a_construccion | alquiler | 10 | -0,9 % [-2,2 %, -0,4 %] | -0,9 % [-2,2 %, -0,4 %] | sí |
| a_construccion | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| a_construccion | precio | 5 | -0,3 % [-0,7 %, -0,2 %] | -0,3 % [-0,7 %, -0,2 %] | sí |
| a_construccion | precio | 10 | -0,8 % [-1,8 %, -0,5 %] | -0,8 % [-1,8 %, -0,5 %] | sí |
| b_vacias | alquiler | 2 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | sí |
| b_vacias | alquiler | 5 | -1,1 % [-2,5 %, -0,5 %] | -1,1 % [-2,5 %, -0,5 %] | sí |
| b_vacias | alquiler | 10 | -2,8 % [-6,6 %, -1,4 %] | -2,8 % [-6,6 %, -1,4 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | sí |
| b_vacias | precio | 10 | -1,0 % [-2,1 %, -0,6 %] | -1,0 % [-2,1 %, -0,6 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 5 | -1,7 % [-4,0 %, -0,7 %] | -1,7 % [-4,0 %, -0,7 %] | sí |
| c_vivienda_publica | alquiler | 10 | -4,4 % [-10,7 %, -1,9 %] | -4,4 % [-10,7 %, -1,9 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | precio | 5 | -0,3 % [-0,8 %, -0,1 %] | -0,3 % [-0,8 %, -0,1 %] | sí |
| c_vivienda_publica | precio | 10 | -0,9 % [-2,0 %, -0,4 %] | -0,9 % [-2,0 %, -0,4 %] | sí |
| d_turisticos | alquiler | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| d_turisticos | alquiler | 5 | -0,3 % [-0,8 %, -0,1 %] | -0,3 % [-0,8 %, -0,1 %] | no |
| d_turisticos | alquiler | 10 | -0,4 % [-0,9 %, -0,1 %] | -0,4 % [-0,9 %, -0,1 %] | no |
| d_turisticos | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 5 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 10 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| e_ayuda_demanda | alquiler | 2 | +3,8 % [+2,0 %, +6,2 %] | -1,2 % [-2,7 %, -0,5 %] | no |
| e_ayuda_demanda | alquiler | 5 | +6,2 % [+3,3 %, +10,0 %] | -2,2 % [-4,6 %, -0,8 %] | no |
| e_ayuda_demanda | alquiler | 10 | +7,3 % [+3,9 %, +11,7 %] | -2,7 % [-5,5 %, -1,1 %] | no |
| e_ayuda_demanda | precio | 2 | +3,8 % [+2,0 %, +6,2 %] | -1,2 % [-2,7 %, -0,5 %] | no |
| e_ayuda_demanda | precio | 5 | +6,2 % [+3,3 %, +10,0 %] | -2,2 % [-4,6 %, -0,8 %] | no |
| e_ayuda_demanda | precio | 10 | +7,3 % [+3,9 %, +11,7 %] | -2,7 % [-5,5 %, -1,1 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,9 % [+0,4 %, +1,6 %] | -0,3 % [-0,7 %, -0,1 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +1,6 % [+0,7 %, +2,6 %] | -0,4 % [-1,1 %, -0,1 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,8 % [+0,9 %, +3,0 %] | -0,5 % [-1,3 %, -0,2 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| f2_impuestos_construccion | alquiler | 5 | -0,4 % [-0,9 %, -0,1 %] | -0,4 % [-0,9 %, -0,1 %] | no |
| f2_impuestos_construccion | alquiler | 10 | -0,4 % [-1,0 %, -0,1 %] | -0,4 % [-1,0 %, -0,1 %] | no |
| f2_impuestos_construccion | precio | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| f2_impuestos_construccion | precio | 5 | -0,4 % [-0,9 %, -0,1 %] | -0,4 % [-0,9 %, -0,1 %] | no |
| f2_impuestos_construccion | precio | 10 | -0,4 % [-1,0 %, -0,1 %] | -0,4 % [-1,0 %, -0,1 %] | no |

**Combinaciones robustas en esta región:** a_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); a_construccion (precio; robusto solo con rejilla (regional no utilizable)); b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (precio; robusto solo con rejilla (regional no utilizable)).

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
