# Atlas regional: Cantabria (06)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 55,08 | 2019Q4 | 66,94 | +21,5 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 67,06 | 2022Q2 | 77,80 | +16,0 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,00 | 2026Q2 | 111,31 | +40,9 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 90,62 | 2019Q4 | 92,12 | +1,7 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,33 | 2022Q2 | 93,68 | +1,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 93,98 | 2026Q2 | 102,54 | +9,1 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.010 -0.099\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.032\,\text{ln\_ocupados}_{t-1} + -0.069\,\text{ln\_pob\_total}_{t-1}]) -0.026\,\text{d\_ln\_ocupados\_L0} +1.266\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.099; semivida = 6.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.032, ln_pob_total = -0.069.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0265 | 0.0251 | -1.06 | 0.295 | 0.706 | [-0.0766, 0.0236] |
| d_ln_pob_total_L0 | 1.2657 | 0.7282 | 1.74 | 0.087 | 0.396 | [-0.1887, 2.7201] |
| d_ln_hip_importe | 0.0014 | 0.0026 | 0.56 | 0.580 | 0.867 | [-0.0037, 0.0065] |

Diagnosticos: BG_p = 0.008; BP_p = 0.002; JB_p = 0.000; RESET_p = 0.000; CUSUM_stat = 0.619; CUSUM_p = 0.838; VIF_max = 1.028; r2_adj = 0.194; phi_mitad1 = -0.114; phi_mitad2 = -0.401; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.124\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.000\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.073\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.124; semivida = 5.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.000.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0002 | 0.0003 | 0.67 | 0.507 | 0.731 | [-0.0004, 0.0009] |
| d_y_L1 | -0.0732 | 0.1089 | -0.67 | 0.503 | 0.731 | [-0.2904, 0.1440] |
| d_ln_hip_importe | 0.0014 | 0.0024 | 0.57 | 0.568 | 0.731 | [-0.0034, 0.0062] |

Diagnosticos: BG_p = 0.026; BP_p = 0.000; JB_p = 0.000; RESET_p = 0.238; CUSUM_stat = 0.672; CUSUM_p = 0.758; VIF_max = 1.000; r2_adj = 0.205; phi_mitad1 = -0.109; phi_mitad2 = -0.385; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,099 | 6,6 |
| B | -0,124 | 5,2 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.041 -0.090\,(\text{ln\_ipv}_{t-1} - [-0.529\,\text{ln\_ocupados}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1} + 0.344\,\text{ln\_pob\_total}_{t-1}]) -0.045\,\text{d\_ln\_ocupados\_L0} -0.005\,\text{d\_ln\_hip\_importe\_L0} +1.235\,\text{d\_ln\_pob\_total\_L0} -0.018\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.090; semivida = 7.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.529, ln_hip_importe = -0.196, ln_pob_total = 0.344.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0449 | 0.0920 | -0.49 | 0.627 | 0.900 | [-0.2287, 0.1388] |
| d_ln_hip_importe_L0 | -0.0050 | 0.0121 | -0.41 | 0.683 | 0.900 | [-0.0292, 0.0193] |
| d_ln_pob_total_L0 | 1.2347 | 2.9773 | 0.41 | 0.680 | 0.900 | [-4.7149, 7.1842] |
| d_ln_compraventas | -0.0181 | 0.0130 | -1.39 | 0.168 | 0.457 | [-0.0441, 0.0078] |

Diagnosticos: BG_p = 0.000; BP_p = 0.106; JB_p = 0.803; RESET_p = 0.507; CUSUM_stat = 0.574; CUSUM_p = 0.896; VIF_max = 2.516; r2_adj = 0.012; phi_mitad1 = -0.087; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.007 -0.149\,(\text{ln\_ipv}_{t-1} - [0.019\,\text{tasa\_paro\_epa}_{t-1} + -0.067\,\text{ln\_hip\_importe}_{t-1}]) +0.003\,\text{d\_tasa\_paro\_epa\_L0} +0.000\,\text{d\_ln\_hip\_importe\_L0} -0.015\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.149; semivida = 4.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.019, ln_hip_importe = -0.067.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0027 | 0.0012 | 2.15 | 0.035 | 0.221 | [0.0002, 0.0051] |
| d_ln_hip_importe_L0 | 0.0004 | 0.0102 | 0.04 | 0.971 | 0.972 | [-0.0199, 0.0207] |
| d_ln_compraventas | -0.0154 | 0.0118 | -1.30 | 0.197 | 0.596 | [-0.0390, 0.0082] |

Diagnosticos: BG_p = 0.001; BP_p = 0.264; JB_p = 0.849; RESET_p = 0.363; CUSUM_stat = 0.455; CUSUM_p = 0.986; VIF_max = 1.950; r2_adj = 0.092; phi_mitad1 = -0.133; phi_mitad2 = -0.138; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,090 | 7,4 |
| B | -0,149 | 4,3 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,008 | 0,002 | 0,000 | 0,000 | 0,838 | 1,03 | 0,19 | -0,114 | -0,401 | False |
| alquiler | B | 0,026 | 0,000 | 0,000 | 0,238 | 0,758 | 1,00 | 0,21 | -0,109 | -0,385 | False |
| compra | A | 0,000 | 0,106 | 0,803 | 0,507 | 0,896 | 2,52 | 0,01 | -0,087 | -0,083 | False |
| compra | B | 0,001 | 0,264 | 0,849 | 0,363 | 0,986 | 1,95 | 0,09 | -0,133 | -0,138 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0050 | -0,0002 | -0,0024 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0143 | -0,0028 | -0,0024 | True |
| 2014T1-2019T4 | residuo no explicado | 0,0006 | 0,0168 | -0,0024 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0116 | -0,0116 | -0,0024 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0,0092 | 0,0092 | -0,0024 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0016 | -0,0001 | 0,0007 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0003 | -0,0001 | 0,0007 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0008 | 0,0026 | 0,0007 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0084 | 0,0084 | 0,0007 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0077 | -0,0077 | 0,0007 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0006 | -0,0000 | -0,0011 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0110 | -0,0022 | -0,0011 | True |
| 2022T3-ultimo | residuo no explicado | 0,0011 | 0,0105 | -0,0011 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0030 | -0,0030 | -0,0011 | True |
| 2022T3-ultimo | ECM propio: residuo | 0,0019 | 0,0019 | -0,0011 | True |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0035 | 0,0258 | -0,0061 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0137 | 0,0014 | -0,0061 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0576 | 0,0312 | -0,0061 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0496 | 0,0477 | -0,0061 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0131 | 0,0131 | -0,0061 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0192 | -0,0192 | -0,0061 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0011 | 0,0085 | 0,0287 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0440 | 0,0046 | 0,0287 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0011 | 0,0006 | 0,0287 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0192 | 0,0636 | 0,0287 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0317 | 0,0317 | 0,0287 | True |
| 2020T1-2022T2 | ECM propio: residuo | -0,0030 | -0,0030 | 0,0287 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0004 | 0,0032 | 0,0073 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0032 | 0,0307 | 0,0073 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0445 | 0,0242 | 0,0073 | True |
| 2022T3-ultimo | residuo no explicado | -0,0508 | 0,0520 | 0,0073 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0055 | -0,0055 | 0,0073 | True |
| 2022T3-ultimo | ECM propio: residuo | 0,0127 | 0,0127 | 0,0073 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_06.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,451 | 0,520 | sí | 0,428 | no |
| compra | ar4 | 2,878 | 4,642 | sí | 2,640 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 2, 5 y 10 años, con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| a_construccion | alquiler | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| a_construccion | alquiler | 5 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| a_construccion | alquiler | 10 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | no |
| a_construccion | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| a_construccion | precio | 5 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| a_construccion | precio | 10 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | no |
| b_vacias | alquiler | 2 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | sí |
| b_vacias | alquiler | 5 | -1,2 % [-2,6 %, -0,6 %] | -1,2 % [-2,6 %, -0,6 %] | sí |
| b_vacias | alquiler | 10 | -3,2 % [-6,9 %, -1,6 %] | -3,2 % [-6,9 %, -1,6 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,4 % [-0,9 %, -0,2 %] | -0,4 % [-0,9 %, -0,2 %] | sí |
| b_vacias | precio | 10 | -1,1 % [-2,3 %, -0,7 %] | -1,1 % [-2,3 %, -0,7 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | sí |
| c_vivienda_publica | alquiler | 5 | -0,7 % [-1,6 %, -0,3 %] | -0,7 % [-1,6 %, -0,3 %] | sí |
| c_vivienda_publica | alquiler | 10 | -1,8 % [-4,1 %, -0,8 %] | -1,8 % [-4,1 %, -0,8 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| c_vivienda_publica | precio | 5 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | no |
| c_vivienda_publica | precio | 10 | -0,3 % [-0,8 %, -0,2 %] | -0,3 % [-0,8 %, -0,2 %] | no |
| d_turisticos | alquiler | 2 | -0,8 % [-1,9 %, -0,3 %] | -0,8 % [-1,9 %, -0,3 %] | sí |
| d_turisticos | alquiler | 5 | -1,3 % [-3,1 %, -0,5 %] | -1,3 % [-3,1 %, -0,5 %] | sí |
| d_turisticos | alquiler | 10 | -1,6 % [-3,6 %, -0,6 %] | -1,6 % [-3,6 %, -0,6 %] | sí |
| d_turisticos | precio | 2 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | no |
| d_turisticos | precio | 5 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| d_turisticos | precio | 10 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | no |
| e_ayuda_demanda | alquiler | 2 | +2,2 % [+1,0 %, +4,4 %] | -2,6 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | alquiler | 5 | +3,6 % [+1,6 %, +7,0 %] | -4,5 % [-8,0 %, -2,1 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,3 % [+1,9 %, +8,2 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| e_ayuda_demanda | precio | 2 | +2,2 % [+1,0 %, +4,4 %] | -2,6 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | precio | 5 | +3,6 % [+1,6 %, +7,0 %] | -4,5 % [-8,0 %, -2,1 %] | no |
| e_ayuda_demanda | precio | 10 | +4,3 % [+1,9 %, +8,2 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,6 % [+0,2 %, +1,1 %] | -0,6 % [-1,3 %, -0,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +0,9 % [+0,3 %, +1,8 %] | -1,1 % [-2,0 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,0 % [-2,1 %, -0,5 %] | -1,0 % [-2,1 %, -0,5 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,0 % [-2,1 %, -0,5 %] | -1,0 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); d_turisticos (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

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
