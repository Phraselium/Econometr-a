# Atlas regional: Castilla y León (07)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 61,37 | 2019Q4 | 71,39 | +16,3 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 70,95 | 2022Q2 | 79,21 | +11,6 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 80,39 | 2026Q2 | 113,55 | +41,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 90,98 | 2019Q4 | 92,10 | +1,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,25 | 2022Q2 | 94,11 | +2,0 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 94,52 | 2026Q2 | 102,18 | +8,1 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.002 -0.007\,(\text{ln\_ipc\_alquiler}_{t-1} - [8.376\,\text{ln\_ocupados}_{t-1} + -6.155\,\text{ln\_pob\_total}_{t-1}]) +0.039\,\text{d\_ln\_ocupados\_L0} +0.826\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.007; semivida = 102.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 8.376, ln_pob_total = -6.155.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0387 | 0.0168 | 2.30 | 0.025 | 0.274 | [0.0051, 0.0723] |
| d_ln_pob_total_L0 | 0.8256 | 0.3630 | 2.27 | 0.026 | 0.274 | [0.1006, 1.5507] |
| d_ln_hip_importe | -0.0003 | 0.0014 | -0.21 | 0.833 | 0.965 | [-0.0030, 0.0024] |

Diagnosticos: BG_p = 0.001; BP_p = 0.273; JB_p = 0.434; RESET_p = 0.300; CUSUM_stat = 0.509; CUSUM_p = 0.958; VIF_max = 1.010; r2_adj = 0.372; phi_mitad1 = -0.025; phi_mitad2 = -0.117; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.001 -0.029\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.025\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.331\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.029; semivida = 23.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.025.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0002 | 0.0002 | -0.98 | 0.332 | 0.652 | [-0.0007, 0.0003] |
| d_y_L1 | 0.3312 | 0.1136 | 2.92 | 0.005 | 0.035 | [0.1047, 0.5577] |
| d_ln_hip_importe | 0.0001 | 0.0014 | 0.08 | 0.935 | 0.954 | [-0.0028, 0.0030] |

Diagnosticos: BG_p = 0.033; BP_p = 0.264; JB_p = 0.076; RESET_p = 0.509; CUSUM_stat = 0.733; CUSUM_p = 0.656; VIF_max = 1.000; r2_adj = 0.358; phi_mitad1 = -0.017; phi_mitad2 = -0.121; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,007 | 102,6 |
| B | -0,029 | 23,7 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.036 -0.368\,(\text{ln\_ipv}_{t-1} - [0.371\,\text{ln\_ocupados}_{t-1} + 0.144\,\text{ln\_hip\_importe}_{t-1} + 0.196\,\text{ln\_pob\_total}_{t-1}]) +0.032\,\text{d\_ln\_ocupados\_L0} +0.033\,\text{d\_ln\_hip\_importe\_L0} +2.867\,\text{d\_ln\_pob\_total\_L0} -0.022\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.368; semivida = 1.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.371, ln_hip_importe = 0.144, ln_pob_total = 0.196.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0324 | 0.1073 | 0.30 | 0.764 | 0.900 | [-0.1820, 0.2468] |
| d_ln_hip_importe_L0 | 0.0332 | 0.0107 | 3.10 | 0.003 | 0.050 | [0.0118, 0.0546] |
| d_ln_pob_total_L0 | 2.8670 | 2.2754 | 1.26 | 0.212 | 0.516 | [-1.6799, 7.4140] |
| d_ln_compraventas | -0.0216 | 0.0129 | -1.67 | 0.100 | 0.324 | [-0.0474, 0.0042] |

Diagnosticos: BG_p = 0.936; BP_p = 0.047; JB_p = 0.879; RESET_p = 0.413; CUSUM_stat = 0.597; CUSUM_p = 0.868; VIF_max = 6.526; r2_adj = 0.238; phi_mitad1 = -0.435; phi_mitad2 = -0.365; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.010 -0.174\,(\text{ln\_ipv}_{t-1} - [0.008\,\text{tasa\_paro\_epa}_{t-1} + 0.237\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.019\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.174; semivida = 3.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.008, ln_hip_importe = 0.237.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0014 | 0.27 | 0.788 | 0.894 | [-0.0025, 0.0032] |
| d_ln_hip_importe_L0 | 0.0282 | 0.0101 | 2.80 | 0.007 | 0.085 | [0.0081, 0.0484] |
| d_ln_compraventas | -0.0192 | 0.0129 | -1.49 | 0.140 | 0.548 | [-0.0449, 0.0064] |

Diagnosticos: BG_p = 0.627; BP_p = 0.091; JB_p = 0.853; RESET_p = 0.572; CUSUM_stat = 0.656; CUSUM_p = 0.782; VIF_max = 1.360; r2_adj = 0.174; phi_mitad1 = -0.310; phi_mitad2 = -0.128; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,368 | 1,5 |
| B | -0,174 | 3,6 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,001 | 0,273 | 0,434 | 0,300 | 0,958 | 1,01 | 0,37 | -0,025 | -0,117 | False |
| alquiler | B | 0,033 | 0,264 | 0,076 | 0,509 | 0,656 | 1,00 | 0,36 | -0,017 | -0,121 | False |
| compra | A | 0,936 | 0,047 | 0,879 | 0,413 | 0,868 | 6,53 | 0,24 | -0,435 | -0,365 | False |
| compra | B | 0,627 | 0,091 | 0,853 | 0,572 | 0,782 | 1,36 | 0,17 | -0,310 | -0,128 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0031 | -0,0001 | -0,0084 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0422 | -0,0083 | -0,0084 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0000 | 0,0369 | -0,0084 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0068 | -0,0068 | -0,0084 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0016 | -0,0016 | -0,0084 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0016 | -0,0001 | -0,0019 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0141 | -0,0028 | -0,0019 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0009 | 0,0138 | -0,0019 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0005 | -0,0005 | -0,0019 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0015 | -0,0015 | -0,0019 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0015 | -0,0001 | -0,0070 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0135 | -0,0027 | -0,0070 | True |
| 2022T3-ultimo | residuo no explicado | -0,0043 | 0,0080 | -0,0070 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0064 | -0,0064 | -0,0070 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0006 | -0,0006 | -0,0070 | True |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0022 | 0,0163 | -0,0486 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0640 | 0,0067 | -0,0486 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,1704 | 0,0924 | -0,0486 | True |
| 2014T1-2019T4 | residuo no explicado | -0,1244 | 0,1182 | -0,0486 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0486 | -0,0486 | -0,0486 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0,0000 | 0,0000 | -0,0486 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0011 | 0,0085 | -0,0301 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0012 | 0,0001 | -0,0301 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0570 | 0,0309 | -0,0301 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0683 | 0,0257 | -0,0301 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0355 | -0,0355 | -0,0301 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0,0053 | 0,0053 | -0,0301 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0010 | 0,0078 | -0,0073 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0019 | 0,0183 | -0,0073 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0544 | 0,0295 | -0,0073 | True |
| 2022T3-ultimo | residuo no explicado | -0,0629 | 0,0464 | -0,0073 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0044 | -0,0044 | -0,0073 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0029 | -0,0029 | -0,0073 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_07.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,337 | 0,389 | sí | 0,346 | sí |
| compra | gbm | 2,654 | 4,515 | sí | 2,321 | no |

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
| b_vacias | alquiler | 2 | -0,3 % [-0,7 %, -0,2 %] | -0,3 % [-0,7 %, -0,2 %] | sí |
| b_vacias | alquiler | 5 | -2,1 % [-4,6 %, -1,0 %] | -2,1 % [-4,6 %, -1,0 %] | sí |
| b_vacias | alquiler | 10 | -5,6 % [-12,1 %, -2,7 %] | -5,6 % [-12,1 %, -2,7 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,2 %, -0,1 %] | -0,1 % [-0,2 %, -0,1 %] | sí |
| b_vacias | precio | 5 | -0,7 % [-1,4 %, -0,4 %] | -0,7 % [-1,4 %, -0,4 %] | sí |
| b_vacias | precio | 10 | -2,0 % [-3,8 %, -1,1 %] | -2,0 % [-3,8 %, -1,1 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | alquiler | 5 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 10 | -0,6 % [-1,4 %, -0,3 %] | -0,6 % [-1,4 %, -0,3 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| c_vivienda_publica | precio | 5 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| c_vivienda_publica | precio | 10 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | no |
| d_turisticos | alquiler | 2 | -0,1 % [-0,3 %, -0,0 %] | -0,1 % [-0,3 %, -0,0 %] | no |
| d_turisticos | alquiler | 5 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | no |
| d_turisticos | alquiler | 10 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| d_turisticos | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| d_turisticos | precio | 5 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| e_ayuda_demanda | alquiler | 2 | +2,4 % [+1,1 %, +4,7 %] | -2,4 % [-4,7 %, -1,1 %] | no |
| e_ayuda_demanda | alquiler | 5 | +4,0 % [+1,8 %, +7,5 %] | -4,1 % [-7,7 %, -1,9 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,6 % [+2,1 %, +8,7 %] | -4,9 % [-9,1 %, -2,3 %] | no |
| e_ayuda_demanda | precio | 2 | +2,4 % [+1,1 %, +4,7 %] | -2,4 % [-4,7 %, -1,1 %] | no |
| e_ayuda_demanda | precio | 5 | +4,0 % [+1,8 %, +7,5 %] | -4,1 % [-7,7 %, -1,9 %] | no |
| e_ayuda_demanda | precio | 10 | +4,6 % [+2,1 %, +8,7 %] | -4,9 % [-9,1 %, -2,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,6 % [+0,2 %, +1,2 %] | -0,6 % [-1,2 %, -0,2 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +1,0 % [+0,4 %, +2,0 %] | -0,9 % [-1,9 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,2 % [+0,5 %, +2,3 %] | -1,1 % [-2,2 %, -0,4 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,5 % [-1,0 %, -0,2 %] | -0,5 % [-1,0 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,8 % [-1,6 %, -0,3 %] | -0,8 % [-1,6 %, -0,3 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,0 % [-1,9 %, -0,4 %] | -1,0 % [-1,9 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,5 % [-1,0 %, -0,2 %] | -0,5 % [-1,0 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,8 % [-1,6 %, -0,3 %] | -0,8 % [-1,6 %, -0,3 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,0 % [-1,9 %, -0,4 %] | -1,0 % [-1,9 %, -0,4 %] | sí |

**Combinaciones robustas en esta región:** b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

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
