# Atlas regional: Comunidad Foral de Navarra (15)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 60,95 | 2019Q4 | 68,60 | +12,6 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 69,84 | 2022Q2 | 76,37 | +9,4 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 77,30 | 2026Q2 | 109,17 | +41,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 89,33 | 2019Q4 | 91,49 | +2,4 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,11 | 2022Q2 | 94,43 | +2,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 94,90 | 2026Q2 | 101,48 | +6,9 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.015 -0.032\,(\text{ln\_ipc\_alquiler}_{t-1} - [-1.191\,\text{ln\_ocupados}_{t-1} + 0.748\,\text{ln\_pob\_total}_{t-1}]) -0.044\,\text{d\_ln\_ocupados\_L0} +1.579\,\text{d\_ln\_pob\_total\_L0} -0.005\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.032; semivida = 21.0 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.191, ln_pob_total = 0.748.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0436 | 0.0256 | -1.70 | 0.093 | 0.396 | [-0.0946, 0.0075] |
| d_ln_pob_total_L0 | 1.5791 | 0.8796 | 1.80 | 0.077 | 0.396 | [-0.1777, 3.3359] |
| d_ln_hip_importe | -0.0053 | 0.0023 | -2.26 | 0.027 | 0.274 | [-0.0100, -0.0006] |

Diagnosticos: BG_p = 0.308; BP_p = 0.125; JB_p = 0.000; RESET_p = 0.513; CUSUM_stat = 0.576; CUSUM_p = 0.895; VIF_max = 1.315; r2_adj = 0.285; phi_mitad1 = -0.116; phi_mitad2 = -0.125; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.039\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.285\,\text{d\_y\_L1} -0.004\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.039; semivida = 17.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0003 | 1.27 | 0.209 | 0.509 | [-0.0002, 0.0009] |
| d_y_L1 | 0.2846 | 0.0930 | 3.06 | 0.003 | 0.027 | [0.0991, 0.4700] |
| d_ln_hip_importe | -0.0045 | 0.0019 | -2.30 | 0.025 | 0.120 | [-0.0084, -0.0006] |

Diagnosticos: BG_p = 0.997; BP_p = 0.332; JB_p = 0.006; RESET_p = 0.764; CUSUM_stat = 0.748; CUSUM_p = 0.631; VIF_max = 1.000; r2_adj = 0.381; phi_mitad1 = -0.047; phi_mitad2 = 0.003; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,032 | 21,0 |
| B | -0,039 | 17,4 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -1.156 -0.271\,(\text{ln\_ipv}_{t-1} - [-0.372\,\text{ln\_ocupados}_{t-1} + -0.139\,\text{ln\_hip\_importe}_{t-1} + -3.632\,\text{ln\_pob\_total}_{t-1}]) -0.095\,\text{d\_ln\_ocupados\_L0} -0.026\,\text{d\_ln\_hip\_importe\_L0} -20.330\,\text{d\_ln\_pob\_total\_L0} +0.008\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.271; semivida = 2.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.372, ln_hip_importe = -0.139, ln_pob_total = -3.632.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0950 | 0.1116 | -0.85 | 0.398 | 0.752 | [-0.3181, 0.1281] |
| d_ln_hip_importe_L0 | -0.0257 | 0.0149 | -1.73 | 0.089 | 0.316 | [-0.0554, 0.0040] |
| d_ln_pob_total_L0 | -20.3300 | 5.9874 | -3.40 | 0.001 | 0.040 | [-32.2949, -8.3651] |
| d_ln_compraventas | 0.0083 | 0.0119 | 0.69 | 0.490 | 0.813 | [-0.0155, 0.0320] |

Diagnosticos: BG_p = 0.156; BP_p = 0.376; JB_p = 0.214; RESET_p = 0.115; CUSUM_stat = 0.381; CUSUM_p = 0.999; VIF_max = 5.271; r2_adj = 0.182; phi_mitad1 = -0.445; phi_mitad2 = -0.307; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.014 -0.065\,(\text{ln\_ipv}_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.008\,\text{d\_ln\_hip\_importe\_L0} -0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.065; semivida = 10.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.005, ln_hip_importe = -0.196.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0015 | 0.0014 | -1.02 | 0.311 | 0.672 | [-0.0044, 0.0014] |
| d_ln_hip_importe_L0 | -0.0082 | 0.0146 | -0.56 | 0.577 | 0.894 | [-0.0372, 0.0209] |
| d_ln_compraventas | -0.0011 | 0.0120 | -0.09 | 0.926 | 0.964 | [-0.0251, 0.0229] |

Diagnosticos: BG_p = 0.257; BP_p = 0.070; JB_p = 0.099; RESET_p = 0.090; CUSUM_stat = 0.590; CUSUM_p = 0.878; VIF_max = 2.286; r2_adj = 0.059; phi_mitad1 = -0.112; phi_mitad2 = -0.172; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,271 | 2,2 |
| B | -0,065 | 10,3 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,308 | 0,125 | 0,000 | 0,513 | 0,895 | 1,32 | 0,29 | -0,116 | -0,125 | False |
| alquiler | B | 0,997 | 0,332 | 0,006 | 0,764 | 0,631 | 1,00 | 0,38 | -0,047 | 0,003 | True |
| compra | A | 0,156 | 0,376 | 0,214 | 0,115 | 0,999 | 5,27 | 0,18 | -0,445 | -0,307 | False |
| compra | B | 0,257 | 0,070 | 0,099 | 0,090 | 0,878 | 2,29 | 0,06 | -0,112 | -0,172 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0027 | -0,0001 | 0,0003 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0,0044 | 0,0222 | 0,0003 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0197 | -0,0039 | 0,0003 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0006 | 0,0006 | 0,0003 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0003 | -0,0003 | 0,0003 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0005 | -0,0000 | -0,0020 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0,0011 | 0,0057 | -0,0020 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0072 | -0,0031 | -0,0020 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0002 | -0,0002 | -0,0020 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0018 | -0,0018 | -0,0020 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0000 | 0,0007 | -0,0063 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0,0002 | 0,0008 | -0,0063 | True |
| 2022T3-ultimo | residuo no explicado | -0,0078 | -0,0065 | -0,0063 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0061 | -0,0061 | -0,0063 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0003 | -0,0003 | -0,0063 | True |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0019 | 0,0142 | -0,1048 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,1401 | 0,0146 | -0,1048 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0485 | 0,0895 | -0,1048 | True |
| 2014T1-2019T4 | residuo no explicado | -0,1993 | 0,0695 | -0,1048 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0750 | -0,0750 | -0,1048 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0298 | -0,0298 | -0,1048 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0003 | 0,0024 | -0,0024 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0168 | 0,0017 | -0,0024 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0124 | 0,0229 | -0,0024 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0260 | 0,0244 | -0,0024 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0002 | 0,0002 | -0,0024 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0026 | -0,0026 | -0,0024 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0035 | -0,0005 | 0,0394 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0104 | 0,0011 | 0,0394 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0017 | 0,0032 | 0,0394 | True |
| 2022T3-ultimo | residuo no explicado | 0,0364 | 0,0549 | 0,0394 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0290 | 0,0290 | 0,0394 | True |
| 2022T3-ultimo | ECM propio: residuo | 0,0103 | 0,0103 | 0,0394 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_15.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,368 | 0,787 | sí | 0,421 | sí |
| compra | ar4 | 2,639 | 5,527 | sí | 2,548 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 2, 5 y 10 años, con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| a_construccion | alquiler | 2 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | sí |
| a_construccion | alquiler | 5 | -0,6 % [-1,3 %, -0,3 %] | -0,6 % [-1,3 %, -0,3 %] | sí |
| a_construccion | alquiler | 10 | -1,5 % [-3,5 %, -0,7 %] | -1,5 % [-3,5 %, -0,7 %] | sí |
| a_construccion | precio | 2 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | sí |
| a_construccion | precio | 5 | -0,5 % [-1,0 %, -0,3 %] | -0,5 % [-1,0 %, -0,3 %] | sí |
| a_construccion | precio | 10 | -1,4 % [-2,7 %, -0,8 %] | -1,4 % [-2,7 %, -0,8 %] | sí |
| b_vacias | alquiler | 2 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | sí |
| b_vacias | alquiler | 5 | -0,9 % [-2,1 %, -0,5 %] | -0,9 % [-2,1 %, -0,5 %] | sí |
| b_vacias | alquiler | 10 | -2,5 % [-5,5 %, -1,3 %] | -2,5 % [-5,5 %, -1,3 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,3 % [-0,7 %, -0,2 %] | -0,3 % [-0,7 %, -0,2 %] | sí |
| b_vacias | precio | 10 | -0,9 % [-1,8 %, -0,5 %] | -0,9 % [-1,8 %, -0,5 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 5 | -1,4 % [-3,2 %, -0,6 %] | -1,4 % [-3,2 %, -0,6 %] | sí |
| c_vivienda_publica | alquiler | 10 | -3,6 % [-8,2 %, -1,6 %] | -3,6 % [-8,2 %, -1,6 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | precio | 5 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | sí |
| c_vivienda_publica | precio | 10 | -0,7 % [-1,6 %, -0,3 %] | -0,7 % [-1,6 %, -0,3 %] | sí |
| d_turisticos | alquiler | 2 | -0,1 % [-0,3 %, -0,0 %] | -0,1 % [-0,3 %, -0,0 %] | no |
| d_turisticos | alquiler | 5 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | no |
| d_turisticos | alquiler | 10 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| d_turisticos | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| d_turisticos | precio | 5 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| e_ayuda_demanda | alquiler | 2 | +2,2 % [+0,9 %, +4,4 %] | -2,6 % [-5,0 %, -1,2 %] | no |
| e_ayuda_demanda | alquiler | 5 | +3,6 % [+1,5 %, +7,1 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,2 % [+1,8 %, +8,3 %] | -5,4 % [-9,6 %, -2,5 %] | no |
| e_ayuda_demanda | precio | 2 | +2,2 % [+0,9 %, +4,4 %] | -2,6 % [-5,0 %, -1,2 %] | no |
| e_ayuda_demanda | precio | 5 | +3,6 % [+1,5 %, +7,1 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | precio | 10 | +4,2 % [+1,8 %, +8,3 %] | -5,4 % [-9,6 %, -2,5 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,6 % [+0,2 %, +1,1 %] | -0,6 % [-1,2 %, -0,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +0,9 % [+0,3 %, +1,8 %] | -1,0 % [-2,0 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,9 % [-1,7 %, -0,4 %] | -0,9 % [-1,7 %, -0,4 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,0 % [-2,0 %, -0,5 %] | -1,0 % [-2,0 %, -0,5 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,9 % [-1,7 %, -0,4 %] | -0,9 % [-1,7 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,0 % [-2,0 %, -0,5 %] | -1,0 % [-2,0 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** a_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); a_construccion (precio; robusto solo con rejilla (regional no utilizable)); b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (precio; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

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
