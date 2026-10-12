# Atlas regional: Comunidad de Madrid (13)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 46,90 | 2019Q4 | 70,42 | +50,2 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 72,18 | 2022Q2 | 78,44 | +8,7 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 80,23 | 2026Q2 | 111,85 | +39,4 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,16 | 2019Q4 | 90,65 | +2,8 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,02 | 2022Q2 | 92,38 | +1,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 92,74 | 2026Q2 | 102,55 | +10,6 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.023 +0.053\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.953\,\text{ln\_ocupados}_{t-1} + -0.696\,\text{ln\_pob\_total}_{t-1}]) -0.008\,\text{d\_ln\_ocupados\_L0} +0.780\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.053; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.953, ln_pob_total = -0.696.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0077 | 0.0153 | -0.51 | 0.614 | 0.867 | [-0.0382, 0.0228] |
| d_ln_pob_total_L0 | 0.7799 | 0.3192 | 2.44 | 0.017 | 0.274 | [0.1424, 1.4174] |
| d_ln_hip_importe | 0.0011 | 0.0020 | 0.55 | 0.581 | 0.867 | [-0.0029, 0.0052] |

Diagnosticos: BG_p = 0.013; BP_p = 0.618; JB_p = 0.819; RESET_p = 0.401; CUSUM_stat = 0.701; CUSUM_p = 0.709; VIF_max = 2.046; r2_adj = 0.345; phi_mitad1 = 0.035; phi_mitad2 = -0.060; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 -0.016\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.042\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.460\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.016; semivida = 43.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.042.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0002 | 1.66 | 0.102 | 0.348 | [-0.0001, 0.0008] |
| d_y_L1 | 0.4601 | 0.1003 | 4.59 | 0.000 | 0.000 | [0.2602, 0.6601] |
| d_ln_hip_importe | 0.0017 | 0.0016 | 1.08 | 0.285 | 0.582 | [-0.0015, 0.0050] |

Diagnosticos: BG_p = 0.913; BP_p = 0.526; JB_p = 0.840; RESET_p = 0.388; CUSUM_stat = 0.485; CUSUM_p = 0.973; VIF_max = 1.000; r2_adj = 0.523; phi_mitad1 = 0.020; phi_mitad2 = -0.050; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,053 | NA |
| B | -0,016 | 43,2 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.131 -0.080\,(\text{ln\_ipv}_{t-1} - [-0.755\,\text{ln\_ocupados}_{t-1} + 0.469\,\text{ln\_hip\_importe}_{t-1} + 1.350\,\text{ln\_pob\_total}_{t-1}]) -0.078\,\text{d\_ln\_ocupados\_L0} +0.041\,\text{d\_ln\_hip\_importe\_L0} +1.261\,\text{d\_ln\_pob\_total\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.080; semivida = 8.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.755, ln_hip_importe = 0.469, ln_pob_total = 1.350.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0782 | 0.1051 | -0.74 | 0.460 | 0.782 | [-0.2882, 0.1319] |
| d_ln_hip_importe_L0 | 0.0405 | 0.0153 | 2.66 | 0.010 | 0.113 | [0.0101, 0.0710] |
| d_ln_pob_total_L0 | 1.2609 | 2.0098 | 0.63 | 0.533 | 0.860 | [-2.7554, 5.2772] |
| d_ln_compraventas | 0.0350 | 0.0179 | 1.95 | 0.055 | 0.265 | [-0.0008, 0.0708] |

Diagnosticos: BG_p = 0.912; BP_p = 0.085; JB_p = 0.748; RESET_p = 0.126; CUSUM_stat = 0.514; CUSUM_p = 0.954; VIF_max = 12.790; r2_adj = 0.345; phi_mitad1 = -0.071; phi_mitad2 = -0.212; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.084 -0.088\,(\text{ln\_ipv}_{t-1} - [0.039\,\text{tasa\_paro\_epa}_{t-1} + 0.538\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.048\,\text{d\_ln\_hip\_importe\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.088; semivida = 7.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.039, ln_hip_importe = 0.538.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0020 | 0.0018 | 1.10 | 0.276 | 0.641 | [-0.0016, 0.0056] |
| d_ln_hip_importe_L0 | 0.0482 | 0.0137 | 3.52 | 0.001 | 0.039 | [0.0209, 0.0756] |
| d_ln_compraventas | 0.0349 | 0.0166 | 2.10 | 0.039 | 0.221 | [0.0018, 0.0680] |

Diagnosticos: BG_p = 0.867; BP_p = 0.073; JB_p = 0.315; RESET_p = 0.020; CUSUM_stat = 0.492; CUSUM_p = 0.969; VIF_max = 5.679; r2_adj = 0.385; phi_mitad1 = -0.185; phi_mitad2 = -0.206; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,080 | 8,3 |
| B | -0,088 | 7,6 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,013 | 0,618 | 0,819 | 0,401 | 0,709 | 2,05 | 0,34 | 0,035 | -0,060 | True |
| alquiler | B | 0,913 | 0,526 | 0,840 | 0,388 | 0,973 | 1,00 | 0,52 | 0,020 | -0,050 | True |
| compra | A | 0,912 | 0,085 | 0,748 | 0,126 | 0,954 | 12,79 | 0,34 | -0,071 | -0,212 | False |
| compra | B | 0,867 | 0,073 | 0,315 | 0,020 | 0,969 | 5,68 | 0,38 | -0,185 | -0,206 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**alquiler, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | 0,0001 | 0,0035 | 0,0066 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | 0,0072 | 0,0366 | 0,0066 | True |
| 2014T1-2019T4 | residuo no explicado | -0,0335 | -0,0008 | 0,0066 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0039 | 0,0039 | 0,0066 | True |
| 2014T1-2019T4 | ECM propio: residuo | 0,0026 | 0,0026 | 0,0066 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | -0,0019 | -0,0001 | -0,0048 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | 0,0010 | 0,0052 | -0,0048 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0091 | -0,0058 | -0,0048 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0066 | -0,0066 | -0,0048 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0,0018 | 0,0018 | -0,0048 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | 0,0001 | 0,0037 | 0,0132 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | 0,0042 | 0,0213 | 0,0132 | True |
| 2022T3-ultimo | residuo no explicado | -0,0118 | 0,0088 | 0,0132 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0185 | 0,0185 | 0,0132 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0053 | -0,0053 | 0,0132 | True |

**compra, especificación A**

| periodo | componente | rango mín. | rango máx. | variación observada | no atribuible |
|---|---|---|---|---|---|
| 2014T1-2019T4 | theta*d(ln_ocupados) | -0,0182 | -0,0024 | 0,2271 | True |
| 2014T1-2019T4 | theta*d(ln_hip_importe) | -0,0114 | 0,1098 | 0,2271 | True |
| 2014T1-2019T4 | theta*d(ln_pob_total) | -0,0800 | 0,1475 | 0,2271 | True |
| 2014T1-2019T4 | residuo no explicado | 0,0845 | 0,3006 | 0,2271 | True |
| 2014T1-2019T4 | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,2284 | 0,2284 | 0,2271 | True |
| 2014T1-2019T4 | ECM propio: residuo | -0,0013 | -0,0013 | 0,2271 | True |
| 2020T1-2022T2 | theta*d(ln_ocupados) | 0,0013 | 0,0098 | 0,0103 | True |
| 2020T1-2022T2 | theta*d(ln_hip_importe) | -0,0668 | 0,0069 | 0,0103 | True |
| 2020T1-2022T2 | theta*d(ln_pob_total) | -0,0113 | 0,0209 | 0,0103 | True |
| 2020T1-2022T2 | residuo no explicado | -0,0134 | 0,0786 | 0,0103 | True |
| 2020T1-2022T2 | ECM propio de la region: suma ajustada (corto plazo + correccion) | -0,0057 | -0,0057 | 0,0103 | True |
| 2020T1-2022T2 | ECM propio: residuo | 0,0160 | 0,0160 | 0,0103 | True |
| 2022T3-ultimo | theta*d(ln_ocupados) | -0,0191 | -0,0026 | -0,0001 | True |
| 2022T3-ultimo | theta*d(ln_hip_importe) | -0,0445 | 0,0046 | -0,0001 | True |
| 2022T3-ultimo | theta*d(ln_pob_total) | -0,0466 | 0,0860 | -0,0001 | True |
| 2022T3-ultimo | residuo no explicado | -0,0845 | 0,1101 | -0,0001 | True |
| 2022T3-ultimo | ECM propio de la region: suma ajustada (corto plazo + correccion) | 0,0028 | 0,0028 | -0,0001 | True |
| 2022T3-ultimo | ECM propio: residuo | -0,0029 | -0,0029 | -0,0001 | True |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_13.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,536 | 0,631 | sí | 0,612 | sí |
| compra | ar4 | 3,060 | 4,891 | sí | 3,281 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 2, 5 y 10 años, con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| a_construccion | alquiler | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | no |
| a_construccion | alquiler | 5 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | no |
| a_construccion | alquiler | 10 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | no |
| a_construccion | precio | 2 | -0,0 % [-0,0 %, -0,0 %] | -0,0 % [-0,0 %, -0,0 %] | sí |
| a_construccion | precio | 5 | -0,1 % [-0,2 %, -0,1 %] | -0,1 % [-0,2 %, -0,1 %] | sí |
| a_construccion | precio | 10 | -0,3 % [-0,6 %, -0,2 %] | -0,3 % [-0,6 %, -0,2 %] | sí |
| b_vacias | alquiler | 2 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | sí |
| b_vacias | alquiler | 5 | -0,6 % [-1,3 %, -0,3 %] | -0,6 % [-1,3 %, -0,3 %] | sí |
| b_vacias | alquiler | 10 | -1,6 % [-3,5 %, -0,8 %] | -1,6 % [-3,5 %, -0,8 %] | sí |
| b_vacias | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | sí |
| b_vacias | precio | 5 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | sí |
| b_vacias | precio | 10 | -0,6 % [-1,1 %, -0,3 %] | -0,6 % [-1,1 %, -0,3 %] | sí |
| c_vivienda_publica | alquiler | 2 | -0,3 % [-0,7 %, -0,1 %] | -0,3 % [-0,7 %, -0,1 %] | sí |
| c_vivienda_publica | alquiler | 5 | -2,0 % [-4,4 %, -0,9 %] | -2,0 % [-4,4 %, -0,9 %] | sí |
| c_vivienda_publica | alquiler | 10 | -5,3 % [-11,5 %, -2,4 %] | -5,3 % [-11,5 %, -2,4 %] | sí |
| c_vivienda_publica | precio | 2 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | sí |
| c_vivienda_publica | precio | 5 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | sí |
| c_vivienda_publica | precio | 10 | -1,0 % [-2,2 %, -0,5 %] | -1,0 % [-2,2 %, -0,5 %] | sí |
| d_turisticos | alquiler | 2 | -0,1 % [-0,3 %, -0,0 %] | -0,1 % [-0,3 %, -0,0 %] | no |
| d_turisticos | alquiler | 5 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| d_turisticos | alquiler | 10 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | no |
| d_turisticos | precio | 2 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 5 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| d_turisticos | precio | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| e_ayuda_demanda | alquiler | 2 | +2,2 % [+0,9 %, +4,4 %] | -2,6 % [-5,0 %, -1,2 %] | no |
| e_ayuda_demanda | alquiler | 5 | +3,7 % [+1,6 %, +7,0 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | alquiler | 10 | +4,4 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| e_ayuda_demanda | precio | 2 | +2,2 % [+0,9 %, +4,4 %] | -2,6 % [-5,0 %, -1,2 %] | no |
| e_ayuda_demanda | precio | 5 | +3,7 % [+1,6 %, +7,0 %] | -4,5 % [-8,1 %, -2,1 %] | no |
| e_ayuda_demanda | precio | 10 | +4,4 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 2 | +0,5 % [+0,2 %, +1,1 %] | -0,6 % [-1,3 %, -0,3 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 5 | +0,9 % [+0,4 %, +1,9 %] | -1,0 % [-2,1 %, -0,4 %] | no |
| f1_rebaja_ITP_IVA_vivienda_nueva | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| f2_impuestos_construccion | alquiler | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | alquiler | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | alquiler | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |
| f2_impuestos_construccion | precio | 2 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| f2_impuestos_construccion | precio | 5 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| f2_impuestos_construccion | precio | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** a_construccion (precio; robusto solo con rejilla (regional no utilizable)); b_vacias (alquiler; robusto solo con rejilla (regional no utilizable)); b_vacias (precio; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (alquiler; robusto solo con rejilla (regional no utilizable)); c_vivienda_publica (precio; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (alquiler; robusto solo con rejilla (regional no utilizable)); f2_impuestos_construccion (precio; robusto solo con rejilla (regional no utilizable)).

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
