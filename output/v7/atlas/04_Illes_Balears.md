# Atlas regional: Illes Balears (04)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 47,58 | 2019Q4 | 68,23 | +43,4 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 69,05 | 2022Q2 | 80,51 | +16,6 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 82,06 | 2026Q2 | 112,05 | +36,5 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 84,62 | 2019Q4 | 90,03 | +6,4 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 90,33 | 2022Q2 | 92,05 | +1,9 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 92,35 | 2026Q2 | 103,04 | +11,6 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.033 -0.087\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.009\,\text{ln\_ocupados}_{t-1} + 0.812\,\text{ln\_pob\_total}_{t-1}]) +0.002\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.087; semivida = 7.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.009, ln_pob_total = 0.812.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0015 | 0.0033 | 0.46 | 0.646 | 0.867 | [-0.0050, 0.0081] |
| d_ln_pob_total_L0 | 0.2979 | 0.3344 | 0.89 | 0.376 | 0.768 | [-0.3700, 0.9657] |
| d_ln_hip_importe | 0.0002 | 0.0016 | 0.13 | 0.896 | 0.972 | [-0.0031, 0.0035] |

Diagnosticos: BG_p = 0.025; BP_p = 0.000; JB_p = 0.972; RESET_p = 0.182; CUSUM_stat = 0.505; CUSUM_p = 0.961; VIF_max = 1.688; r2_adj = 0.021; phi_mitad1 = -0.107; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.011\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.006\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.040\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.011; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.006.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0000 | 0.0001 | -0.57 | 0.567 | 0.731 | [-0.0002, 0.0001] |
| d_y_L1 | 0.0401 | 0.1220 | 0.33 | 0.743 | 0.842 | [-0.2033, 0.2835] |
| d_ln_hip_importe | 0.0006 | 0.0016 | 0.39 | 0.697 | 0.808 | [-0.0025, 0.0038] |

Diagnosticos: BG_p = 0.024; BP_p = 0.795; JB_p = 0.148; RESET_p = 0.409; CUSUM_stat = 0.513; CUSUM_p = 0.955; VIF_max = 1.000; r2_adj = -0.010; phi_mitad1 = 0.040; phi_mitad2 = -0.015; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,087 | 7,6 |
| B | 0,011 | NA |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.039 -0.012\,(\text{ln\_ipv}_{t-1} - [10.192\,\text{ln\_ocupados}_{t-1} + 0.801\,\text{ln\_hip\_importe}_{t-1} + -15.928\,\text{ln\_pob\_total}_{t-1}]) +0.087\,\text{d\_ln\_ocupados\_L0} +0.012\,\text{d\_ln\_hip\_importe\_L0} -4.358\,\text{d\_ln\_pob\_total\_L0} -0.025\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.012; semivida = 58.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 10.192, ln_hip_importe = 0.801, ln_pob_total = -15.928.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0872 | 0.0217 | 4.02 | 0.000 | 0.011 | [0.0439, 0.1305] |
| d_ln_hip_importe_L0 | 0.0115 | 0.0122 | 0.94 | 0.349 | 0.720 | [-0.0129, 0.0359] |
| d_ln_pob_total_L0 | -4.3579 | 2.5555 | -1.71 | 0.093 | 0.316 | [-9.4646, 0.7488] |
| d_ln_compraventas | -0.0254 | 0.0169 | -1.50 | 0.139 | 0.431 | [-0.0592, 0.0085] |

Diagnosticos: BG_p = 0.428; BP_p = 0.436; JB_p = 0.997; RESET_p = 0.043; CUSUM_stat = 0.433; CUSUM_p = 0.992; VIF_max = 2.214; r2_adj = 0.285; phi_mitad1 = -0.195; phi_mitad2 = -0.027; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.017\,(\text{ln\_ipv}_{t-1} - [-0.098\,\text{tasa\_paro\_epa}_{t-1} + 0.373\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.014\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.017; semivida = 41.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.098, ln_hip_importe = 0.373.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0015 | 0.0004 | -3.29 | 0.002 | 0.040 | [-0.0023, -0.0006] |
| d_ln_hip_importe_L0 | 0.0137 | 0.0121 | 1.13 | 0.261 | 0.633 | [-0.0104, 0.0378] |
| d_ln_compraventas | -0.0045 | 0.0155 | -0.29 | 0.774 | 0.894 | [-0.0353, 0.0264] |

Diagnosticos: BG_p = 0.454; BP_p = 0.579; JB_p = 0.609; RESET_p = 0.000; CUSUM_stat = 0.632; CUSUM_p = 0.819; VIF_max = 1.864; r2_adj = 0.191; phi_mitad1 = -0.193; phi_mitad2 = 0.007; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,012 | 58,5 |
| B | -0,017 | 41,1 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,025 | 0,000 | 0,972 | 0,182 | 0,961 | 1,69 | 0,02 | -0,107 | -0,174 | False |
| alquiler | B | 0,024 | 0,795 | 0,148 | 0,409 | 0,955 | 1,00 | -0,01 | 0,040 | -0,015 | True |
| compra | A | 0,428 | 0,436 | 0,997 | 0,043 | 0,992 | 2,21 | 0,29 | -0,195 | -0,027 | False |
| compra | B | 0,454 | 0,579 | 0,609 | 0,000 | 0,819 | 1,86 | 0,19 | -0,193 | 0,007 | True |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0003 | 0,0080 | 0,0437 | False |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0,0090 | 0,0455 | 0,0437 | False |
| 2014T1-2019T4 | residuo no explicado | -0,0098 | 0,0345 | 0,0437 | False |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0360 | 0,0360 | 0,0437 | False |
| 2014T1-2019T4 | ECM propio: residuo | 0,0077 | 0,0077 | 0,0437 | False |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0001 | 0,0026 | 0,0126 | False |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0,0020 | 0,0101 | 0,0126 | False |
| 2020T1-2022T2 | residuo no explicado | -0,0002 | 0,0105 | 0,0126 | False |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0108 | 0,0108 | 0,0126 | False |
| 2020T1-2022T2 | ECM propio: residuo | 0,0018 | 0,0018 | 0,0126 | False |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0100 | -0,0003 | 0,0134 | False |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0,0039 | 0,0195 | 0,0134 | False |
| 2022T3-ultimo | residuo no explicado | -0,0019 | 0,0099 | 0,0134 | False |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0172 | 0,0172 | 0,0134 | False |
| 2022T3-ultimo | ECM propio: residuo | -0,0038 | -0,0038 | 0,0134 | False |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0419 | -0,0056 | 0,1474 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0130 | 0,0014 | 0,1474 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0996 | 0,1837 | 0,1474 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0309 | 0,3019 | 0,1474 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,1859 | 0,1859 | 0,1474 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0385 | -0,0385 | 0,1474 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0137 | -0,0018 | 0,0508 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0047 | 0,0452 | 0,0508 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0221 | 0,0408 | 0,0508 | True |
| 2020T1-2022T2 | residuo no explicado | 0,0129 | 0,0773 | 0,0508 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0108 | -0,0108 | 0,0508 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0,0616 | 0,0616 | 0,0508 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0070 | 0,0523 | -0,0222 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0035 | 0,0004 | -0,0222 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0427 | 0,0788 | -0,0222 | True |
| 2022T3-ultimo | residuo no explicado | -0,1081 | -0,0226 | -0,0222 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0154 | 0,0154 | -0,0222 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0376 | -0,0376 | -0,0222 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_04.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | mixto | 0,684 | 0,679 | no | 0,679 | no |
| compra | ar4 | 3,047 | 4,281 | sí | 3,058 | sí |

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
| b_vacias | alquiler | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | sí |
| b_vacias | alquiler | 5 | -1,6 % [-3,3 %, -0,7 %] | -1,6 % [-3,3 %, -0,7 %] | sí |
| b_vacias | alquiler | 10 | -4,1 % [-8,8 %, -2,0 %] | -4,1 % [-8,8 %, -2,0 %] | sí |
| b_vacias | precio | 2 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,5 % [-1,1 %, -0,3 %] | -0,5 % [-1,1 %, -0,3 %] | sí |
| b_vacias | precio | 10 | -1,4 % [-2,8 %, -0,8 %] | -1,4 % [-2,8 %, -0,8 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 5 | -1,5 % [-3,2 %, -0,6 %] | -1,5 % [-3,2 %, -0,6 %] | sí |
| c_vivienda_publica | alquiler | 10 | -3,8 % [-8,5 %, -1,7 %] | -3,8 % [-8,5 %, -1,7 %] | sí |
| c_vivienda_publica | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | precio | 5 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | sí |
| c_vivienda_publica | precio | 10 | -0,7 % [-1,6 %, -0,3 %] | -0,7 % [-1,6 %, -0,3 %] | sí |
| d_turisticos | alquiler | 2 | -1,5 % [-3,5 %, -0,5 %] | -1,5 % [-3,5 %, -0,5 %] | sí |
| d_turisticos | alquiler | 5 | -2,5 % [-5,8 %, -0,8 %] | -2,5 % [-5,8 %, -0,8 %] | sí |
| d_turisticos | alquiler | 10 | -2,9 % [-6,8 %, -1,0 %] | -2,9 % [-6,8 %, -1,0 %] | sí |
| d_turisticos | precio | 2 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | sí |
| d_turisticos | precio | 5 | -0,4 % [-1,0 %, -0,2 %] | -0,4 % [-1,0 %, -0,2 %] | sí |
| d_turisticos | precio | 10 | -0,5 % [-1,2 %, -0,2 %] | -0,5 % [-1,2 %, -0,2 %] | sí |
| e_ayuda_demanda | alquiler | 2 | +2,2 % [+0,9 %, +4,2 %] | -2,7 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | alquiler | 5 | +3,6 % [+1,6 %, +6,8 %] | -4,6 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,2 % [+1,8 %, +8,0 %] | -5,5 % [-9,5 %, -2,5 %] | no |
| e_ayuda_demanda | precio | 2 | +2,2 % [+0,9 %, +4,2 %] | -2,7 % [-4,9 %, -1,2 %] | no |
| e_ayuda_demanda | precio | 5 | +3,6 % [+1,6 %, +6,8 %] | -4,6 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | precio | 10 | +4,2 % [+1,8 %, +8,0 %] | -5,5 % [-9,5 %, -2,5 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,5 % [+0,2 %, +1,1 %] | -0,6 % [-1,3 %, -0,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +0,9 % [+0,3 %, +1,8 %] | -1,1 % [-2,1 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,0 % [+0,4 %, +2,2 %] | -1,3 % [-2,4 %, -0,5 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,9 % [-1,7 %, -0,4 %] | -0,9 % [-1,7 %, -0,4 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,9 % [-1,7 %, -0,4 %] | -0,9 % [-1,7 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (precio; robusto solo con rejilla (regional no utilizable)); d_turisticos (alquiler; robusto solo con rejilla (regional no utilizable)); d_turisticos (precio; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

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
