# Atlas regional: Aragón (02)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 57,00 | 2019Q4 | 68,59 | +20,3 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 68,86 | 2022Q2 | 76,63 | +11,3 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 77,47 | 2026Q2 | 113,47 | +46,5 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,85 | 2019Q4 | 90,85 | +2,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,21 | 2022Q2 | 93,30 | +2,3 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 93,65 | 2026Q2 | 102,44 | +9,4 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.004 -0.104\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.122\,\text{ln\_ocupados}_{t-1} + 0.220\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} +0.365\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.104; semivida = 6.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.122, ln_pob_total = 0.220.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0159 | 0.0175 | -0.91 | 0.366 | 0.768 | [-0.0509, 0.0190] |
| d_ln_pob_total_L0 | 0.3646 | 0.5037 | 0.72 | 0.472 | 0.829 | [-0.6412, 1.3705] |
| d_ln_hip_importe | 0.0013 | 0.0012 | 1.04 | 0.300 | 0.706 | [-0.0012, 0.0037] |

Diagnosticos: BG_p = 0.118; BP_p = 0.000; JB_p = 0.000; RESET_p = 0.349; CUSUM_stat = 0.581; CUSUM_p = 0.888; VIF_max = 1.027; r2_adj = 0.357; phi_mitad1 = -0.094; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.134\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.016\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.134; semivida = 4.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0002 | 1.21 | 0.232 | 0.534 | [-0.0002, 0.0007] |
| d_y_L1 | 0.0163 | 0.1011 | 0.16 | 0.872 | 0.927 | [-0.1853, 0.2178] |
| d_ln_hip_importe | 0.0007 | 0.0011 | 0.61 | 0.546 | 0.731 | [-0.0015, 0.0029] |

Diagnosticos: BG_p = 0.005; BP_p = 0.000; JB_p = 0.026; RESET_p = 0.849; CUSUM_stat = 0.694; CUSUM_p = 0.722; VIF_max = 1.000; r2_adj = 0.448; phi_mitad1 = -0.146; phi_mitad2 = -0.092; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,104 | 6,3 |
| B | -0,134 | 4,8 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.291 -0.211\,(\text{ln\_ipv}_{t-1} - [0.116\,\text{ln\_ocupados}_{t-1} + -0.120\,\text{ln\_hip\_importe}_{t-1} + 4.096\,\text{ln\_pob\_total}_{t-1}]) +0.050\,\text{d\_ln\_ocupados\_L0} -0.015\,\text{d\_ln\_hip\_importe\_L0} +6.111\,\text{d\_ln\_pob\_total\_L0} +0.005\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.211; semivida = 2.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.116, ln_hip_importe = -0.120, ln_pob_total = 4.096.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0502 | 0.0887 | 0.57 | 0.573 | 0.860 | [-0.1270, 0.2274] |
| d_ln_hip_importe_L0 | -0.0148 | 0.0081 | -1.82 | 0.073 | 0.292 | [-0.0311, 0.0014] |
| d_ln_pob_total_L0 | 6.1105 | 2.3648 | 2.58 | 0.012 | 0.118 | [1.3849, 10.8361] |
| d_ln_compraventas | 0.0051 | 0.0121 | 0.42 | 0.673 | 0.900 | [-0.0190, 0.0293] |

Diagnosticos: BG_p = 0.010; BP_p = 0.144; JB_p = 0.120; RESET_p = 0.896; CUSUM_stat = 0.499; CUSUM_p = 0.964; VIF_max = 1.775; r2_adj = 0.259; phi_mitad1 = -0.362; phi_mitad2 = -0.174; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.002 -0.070\,(\text{ln\_ipv}_{t-1} - [0.018\,\text{tasa\_paro\_epa}_{t-1} + -0.219\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.009\,\text{d\_ln\_hip\_importe\_L0} +0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.070; semivida = 9.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.018, ln_hip_importe = -0.219.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0006 | 0.0013 | 0.43 | 0.669 | 0.894 | [-0.0020, 0.0031] |
| d_ln_hip_importe_L0 | -0.0093 | 0.0078 | -1.19 | 0.237 | 0.610 | [-0.0249, 0.0063] |
| d_ln_compraventas | 0.0056 | 0.0123 | 0.46 | 0.649 | 0.894 | [-0.0189, 0.0302] |

Diagnosticos: BG_p = 0.003; BP_p = 0.302; JB_p = 0.000; RESET_p = 0.481; CUSUM_stat = 0.527; CUSUM_p = 0.944; VIF_max = 1.618; r2_adj = 0.215; phi_mitad1 = -0.077; phi_mitad2 = -0.109; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,211 | 2,9 |
| B | -0,070 | 9,5 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,118 | 0,000 | 0,000 | 0,349 | 0,888 | 1,03 | 0,36 | -0,094 | -0,174 | False |
| alquiler | B | 0,005 | 0,000 | 0,026 | 0,849 | 0,722 | 1,00 | 0,45 | -0,146 | -0,092 | False |
| compra | A | 0,010 | 0,144 | 0,120 | 0,896 | 0,964 | 1,77 | 0,26 | -0,362 | -0,174 | False |
| compra | B | 0,003 | 0,302 | 0,000 | 0,481 | 0,944 | 1,62 | 0,22 | -0,077 | -0,109 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0025 | [0,0043; 0,0115] | sí |
| alquiler | 2020T1-2022T2 | 0,0036 | [0,0043; 0,0076] | sí |
| alquiler | 2022T3-ultimo | 0,0035 | [0,0036; 0,0050] | sí |
| compra | 2014T1-2019T4 | -0,0166 | [-0,0332; 0,0193] | sí |
| compra | 2020T1-2022T2 | -0,0156 | [-0,0434; -0,0026] | sí |
| compra | 2022T3-ultimo | 0,0235 | [0,0171; 0,0401] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_02.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,390 | 0,358 | no | 0,358 | no |
| compra | ar4 | 2,795 | 5,761 | sí | 2,563 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | precio | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -4,0 % [-8,6 %, -2,0 %] | -4,0 % [-8,6 %, -2,0 %] | sí |
| movilización de vacías | precio | 10 | -1,4 % [-2,8 %, -0,8 %] | -1,4 % [-2,8 %, -0,8 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -2,3 % [-4,8 %, -1,0 %] | -2,3 % [-4,8 %, -1,0 %] | sí |
| vivienda pública o asequible | precio | 10 | -0,4 % [-0,9 %, -0,2 %] | -0,4 % [-0,9 %, -0,2 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| regulación local de turísticos | precio | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,4 % [+1,9 %, +8,3 %] | -5,3 % [-9,5 %, -2,4 %] | no |
| ayudas a la demanda | precio | 10 | +4,4 % [+1,9 %, +8,3 %] | -5,3 % [-9,5 %, -2,4 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,3 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |
| rebaja de impuestos y costes de construcción | precio | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 7. Qué no se puede afirmar

- Que haya una relación de largo plazo estable entre precios o alquileres y empleo, población, hipotecas o paro: ninguna hipótesis confirmatoria de R4 se confirmó (p de Holm ≥ 0,05).
- Que la velocidad de ajuste de la región sea distinta de cero o de la del resto: no hay inferencia válida individual.
- Que la descomposición atribuya la variación a un factor: el residuo domina y los coeficientes no están confirmados.
- Que el mejor modelo del backtest vaya a predecir mejor en el futuro: muestra ya vista en v1 y selección en muestra.
- Que una propuesta produzca los impactos de la tabla: son escenarios condicionales con supuestos (C4), no estimaciones identificadas.
- Nada de lo anterior es causal: la evidencia queda por debajo del nivel CAUSAL.

---
*Capas: variaciones de índices C4 (fuente única regional); ECM, descomposición y backtest C4; propuestas C4 condicional. informativo, muestra ya vista en v1. Validación diferida pendiente: los modelos están congelados (R5) y se evaluarán con `make evaluate_v7` sobre datos posteriores.*
