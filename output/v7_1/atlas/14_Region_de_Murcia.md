# Atlas regional: Región de Murcia (14)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 58,68 | 2019Q4 | 68,45 | +16,7 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 68,35 | 2022Q2 | 79,26 | +16,0 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,71 | 2026Q2 | 113,19 | +42,0 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 93,47 | 2019Q4 | 93,75 | +0,3 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 94,17 | 2022Q2 | 95,82 | +1,8 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 96,04 | 2026Q2 | 103,01 | +7,3 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.011 -0.041\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.012\,\text{ln\_ocupados}_{t-1} + -1.146\,\text{ln\_pob\_total}_{t-1}]) -0.004\,\text{d\_ln\_ocupados\_L0} +0.373\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.041; semivida = 16.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.012, ln_pob_total = -1.146.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0036 | 0.0259 | -0.14 | 0.889 | 0.972 | [-0.0553, 0.0480] |
| d_ln_pob_total_L0 | 0.3727 | 0.9553 | 0.39 | 0.698 | 0.890 | [-1.5352, 2.2805] |
| d_ln_hip_importe | 0.0036 | 0.0036 | 1.01 | 0.318 | 0.706 | [-0.0036, 0.0109] |

Diagnosticos: BG_p = 0.046; BP_p = 0.011; JB_p = 0.000; RESET_p = 0.640; CUSUM_stat = 0.669; CUSUM_p = 0.762; VIF_max = 1.396; r2_adj = -0.021; phi_mitad1 = 0.134; phi_mitad2 = -0.458; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.006\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.073\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.294\,\text{d\_y\_L1} +0.006\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.006; semivida = 121.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.073.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0003 | -0.30 | 0.763 | 0.846 | [-0.0007, 0.0005] |
| d_y_L1 | 0.2942 | 0.1071 | 2.75 | 0.008 | 0.043 | [0.0806, 0.5079] |
| d_ln_hip_importe | 0.0065 | 0.0033 | 1.99 | 0.051 | 0.217 | [-0.0000, 0.0129] |

Diagnosticos: BG_p = 0.740; BP_p = 0.534; JB_p = 0.005; RESET_p = 0.520; CUSUM_stat = 0.603; CUSUM_p = 0.861; VIF_max = 1.000; r2_adj = 0.136; phi_mitad1 = -0.009; phi_mitad2 = -0.051; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,041 | 16,4 |
| B | -0,006 | 121,8 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.010 -0.068\,(\text{ln\_ipv}_{t-1} - [0.643\,\text{ln\_ocupados}_{t-1} + 0.126\,\text{ln\_hip\_importe}_{t-1} + -1.851\,\text{ln\_pob\_total}_{t-1}]) -0.086\,\text{d\_ln\_ocupados\_L0} +0.018\,\text{d\_ln\_hip\_importe\_L0} -2.960\,\text{d\_ln\_pob\_total\_L0} -0.008\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.068; semivida = 9.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.643, ln_hip_importe = 0.126, ln_pob_total = -1.851.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0859 | 0.0847 | -1.01 | 0.314 | 0.668 | [-0.2552, 0.0833] |
| d_ln_hip_importe_L0 | 0.0176 | 0.0123 | 1.43 | 0.156 | 0.443 | [-0.0069, 0.0421] |
| d_ln_pob_total_L0 | -2.9604 | 2.6060 | -1.14 | 0.260 | 0.600 | [-8.1681, 2.2472] |
| d_ln_compraventas | -0.0077 | 0.0128 | -0.60 | 0.549 | 0.860 | [-0.0333, 0.0179] |

Diagnosticos: BG_p = 0.485; BP_p = 0.092; JB_p = 0.820; RESET_p = 0.008; CUSUM_stat = 0.697; CUSUM_p = 0.716; VIF_max = 4.974; r2_adj = 0.184; phi_mitad1 = -0.185; phi_mitad2 = -0.410; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.006 -0.072\,(\text{ln\_ipv}_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1} + 0.227\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.072; semivida = 9.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.014, ln_hip_importe = 0.227.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0010 | 0.0010 | 0.98 | 0.328 | 0.672 | [-0.0010, 0.0029] |
| d_ln_hip_importe_L0 | 0.0216 | 0.0115 | 1.88 | 0.065 | 0.275 | [-0.0014, 0.0446] |
| d_ln_compraventas | -0.0057 | 0.0126 | -0.46 | 0.650 | 0.894 | [-0.0308, 0.0194] |

Diagnosticos: BG_p = 0.362; BP_p = 0.006; JB_p = 0.955; RESET_p = 0.053; CUSUM_stat = 0.843; CUSUM_p = 0.476; VIF_max = 1.742; r2_adj = 0.160; phi_mitad1 = -0.147; phi_mitad2 = -0.282; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,068 | 9,9 |
| B | -0,072 | 9,3 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,046 | 0,011 | 0,000 | 0,640 | 0,762 | 1,40 | -0,02 | 0,134 | -0,458 | True |
| alquiler | B | 0,740 | 0,534 | 0,005 | 0,520 | 0,861 | 1,00 | 0,14 | -0,009 | -0,051 | False |
| compra | A | 0,485 | 0,092 | 0,820 | 0,008 | 0,716 | 4,97 | 0,18 | -0,185 | -0,410 | False |
| compra | B | 0,362 | 0,006 | 0,955 | 0,053 | 0,476 | 1,74 | 0,16 | -0,147 | -0,282 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | -0,0174 | [-0,0393; -0,0213] | sí |
| alquiler | 2020T1-2022T2 | -0,0086 | [-0,0220; -0,0111] | sí |
| alquiler | 2022T3-ultimo | -0,0188 | [-0,0254; -0,0202] | sí |
| compra | 2014T1-2019T4 | -0,0325 | [-0,1070; 0,0065] | sí |
| compra | 2020T1-2022T2 | 0,0058 | [-0,0436; 0,0296] | sí |
| compra | 2022T3-ultimo | -0,0121 | [-0,0567; 0,0000] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_14.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,446 | 0,574 | sí | 0,433 | no |
| compra | pmg | 2,917 | 4,103 | sí | 2,633 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -4,4 % [-9,7 %, -2,0 %] | -4,4 % [-9,7 %, -2,0 %] | sí |
| construcción adicional (dosis v7.2) | compra | 10 | -4,0 % [-7,6 %, -2,3 %] | -4,0 % [-7,6 %, -2,3 %] | sí |
| movilización de vacías | alquiler | 10 | -3,1 % [-6,5 %, -1,5 %] | -3,1 % [-6,5 %, -1,5 %] | sí |
| movilización de vacías | compra | 10 | -1,1 % [-2,1 %, -0,6 %] | -1,1 % [-2,1 %, -0,6 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -5,1 % [-11,3 %, -2,3 %] | -5,1 % [-11,3 %, -2,3 %] | sí |
| vivienda pública o asequible | compra | 10 | -1,0 % [-2,1 %, -0,5 %] | -1,0 % [-2,1 %, -0,5 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,3 % [-0,8 %, -0,1 %] | -0,3 % [-0,8 %, -0,1 %] | no |
| regulación local de turísticos | compra | 10 | -0,1 % [-0,1 %, -0,0 %] | -0,1 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,2 % [+1,9 %, +8,4 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| ayudas a la demanda | compra | 10 | +4,2 % [+1,9 %, +8,4 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,3 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -1,0 % [-2,1 %, -0,5 %] | -1,0 % [-2,1 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -1,0 % [-2,1 %, -0,5 %] | -1,0 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler); vivienda pública o asequible (compra); rebaja de impuestos y costes de construcción (no difundible) (alquiler); rebaja de impuestos y costes de construcción (no difundible) (compra) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 18.507 | -1,1 % | no estimable | -0,59 pp [-1,09, -0,40] | — | — |
| movilización de vacías | alquiler | 18.507 | -3,1 % | no estimable | -1,70 pp [-3,38, -0,93] | — | — |
| vivienda pública o asequible | compra | 16.405 | -1,0 % | no estimable | -0,59 pp [-1,09, -0,40] | — | — |
| vivienda pública o asequible | alquiler | 16.405 | -5,1 % | no estimable | -3,08 pp [-5,81, -2,00] | — | — |
| regulación local de turísticos | compra | 976 | -0,1 % | no estimable | -0,59 pp [-1,09, -0,40] | — | — |
| regulación local de turísticos | alquiler | 976 | -0,3 % | no estimable | -3,42 pp [-6,41, -2,26] | — | — |
| construcción adicional | compra | 66.427 | -4,0 % | no estimable | -0,59 pp [-1,09, -0,40] | — | — |
| construcción adicional | alquiler | 66.427 | -4,4 % | no estimable | -0,67 pp [-1,41, -0,33] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 4.308 | -1,0 % | 10 [6, 17] | — | -10,54 pp [-15,26, -5,56] | 9 [7, 18] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 4.308 | -1,0 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 27.814 | +4,2 % | 320 [174, 459] | — | +1,42 pp [+0,69, +2,21] | 57 [41, 93] |
| ayudas a la demanda | alquiler | 27.814 | +4,2 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 27.814 | +1,1 % | 81 [37, 122] | — | +1,42 pp [+0,69, +2,21] | 60 [42, 110] |

«No estimable»: no hay coste unitario verificado ni versionado (motivos en output/v7_1/S1/resumen.md). En las ayudas a la demanda y en la rebaja de ITP/IVA el coste por punto se refiere al precio neto que paga el beneficiario; el precio de mercado sube. El efecto por 100 M€ de la rebaja de impuestos a la construcción está sobrestimado por construcción (la rebaja se traslada a todo el mercado y el coste solo cubre la obra nueva).

## 7. Qué no se puede afirmar

- Que haya una relación de largo plazo estable entre precios o alquileres y empleo, población, hipotecas o paro: ninguna hipótesis confirmatoria de R4 se confirmó (p de Holm ≥ 0,05).
- Que la velocidad de ajuste de la región sea distinta de cero o de la del resto: no hay inferencia válida individual.
- Que la descomposición atribuya la variación a un factor: el residuo domina y los coeficientes no están confirmados.
- Que el mejor modelo del backtest vaya a predecir mejor en el futuro: muestra ya vista en v1 y selección en muestra.
- Que un instrumento sea «más eficiente por euro» que otro: los costes de los instrumentos de cantidad no son estimables y los demás dependen de supuestos (C4).
- Que una propuesta produzca los impactos de la tabla: son escenarios condicionales con supuestos (C4), no estimaciones identificadas.
- Nada de lo anterior es causal: la evidencia queda por debajo del nivel CAUSAL.

---
*Capas: variaciones de índices C4 (fuente única regional); ECM, descomposición y backtest C4; propuestas C4 condicional. informativo, muestra ya vista en v1. Validación diferida pendiente: los modelos están congelados (R5) y se evaluarán con `make evaluate_v7` sobre datos posteriores.*
