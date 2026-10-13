# Atlas regional: Extremadura (11)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 70,20 | 2019Q4 | 75,63 | +7,7 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 75,05 | 2022Q2 | 81,92 | +9,2 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 83,02 | 2026Q2 | 111,96 | +34,9 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 92,33 | 2019Q4 | 92,05 | -0,3 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,27 | 2022Q2 | 93,96 | +1,8 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 94,26 | 2026Q2 | 101,66 | +7,9 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.001 -0.044\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.239\,\text{ln\_ocupados}_{t-1} + 0.319\,\text{ln\_pob\_total}_{t-1}]) -0.023\,\text{d\_ln\_ocupados\_L0} +0.409\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.044; semivida = 15.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.239, ln_pob_total = 0.319.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0231 | 0.0154 | -1.50 | 0.138 | 0.510 | [-0.0539, 0.0077] |
| d_ln_pob_total_L0 | 0.4087 | 0.2737 | 1.49 | 0.140 | 0.510 | [-0.1378, 0.9553] |
| d_ln_hip_importe | -0.0004 | 0.0016 | -0.24 | 0.811 | 0.962 | [-0.0036, 0.0028] |

Diagnosticos: BG_p = 0.087; BP_p = 0.265; JB_p = 0.407; RESET_p = 0.268; CUSUM_stat = 0.828; CUSUM_p = 0.500; VIF_max = 1.662; r2_adj = 0.014; phi_mitad1 = -0.107; phi_mitad2 = -0.005; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.004\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.293\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.004; semivida = 156.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.016.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0002 | 1.83 | 0.071 | 0.278 | [-0.0000, 0.0008] |
| d_y_L1 | 0.2934 | 0.1051 | 2.79 | 0.007 | 0.043 | [0.0838, 0.5030] |
| d_ln_hip_importe | -0.0012 | 0.0015 | -0.81 | 0.419 | 0.711 | [-0.0041, 0.0017] |

Diagnosticos: BG_p = 0.970; BP_p = 0.851; JB_p = 0.228; RESET_p = 0.706; CUSUM_stat = 0.739; CUSUM_p = 0.646; VIF_max = 1.000; r2_adj = 0.102; phi_mitad1 = -0.085; phi_mitad2 = -0.079; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,044 | 15,4 |
| B | -0,004 | 156,8 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.160 -0.156\,(\text{ln\_ipv}_{t-1} - [-0.829\,\text{ln\_ocupados}_{t-1} + 0.170\,\text{ln\_hip\_importe}_{t-1} + 2.305\,\text{ln\_pob\_total}_{t-1}]) -0.080\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +5.770\,\text{d\_ln\_pob\_total\_L0} +0.012\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.156; semivida = 4.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.829, ln_hip_importe = 0.170, ln_pob_total = 2.305.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0797 | 0.0965 | -0.83 | 0.412 | 0.757 | [-0.2725, 0.1131] |
| d_ln_hip_importe_L0 | 0.0029 | 0.0136 | 0.22 | 0.830 | 0.956 | [-0.0242, 0.0300] |
| d_ln_pob_total_L0 | 5.7698 | 2.7406 | 2.11 | 0.039 | 0.222 | [0.2932, 11.2465] |
| d_ln_compraventas | 0.0122 | 0.0142 | 0.86 | 0.395 | 0.752 | [-0.0162, 0.0405] |

Diagnosticos: BG_p = 0.699; BP_p = 0.056; JB_p = 0.711; RESET_p = 0.113; CUSUM_stat = 0.702; CUSUM_p = 0.708; VIF_max = 6.103; r2_adj = 0.201; phi_mitad1 = -0.396; phi_mitad2 = -0.285; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.045 -0.001\,(\text{ln\_ipv}_{t-1} - [-1.219\,\text{tasa\_paro\_epa}_{t-1} + 24.398\,\text{ln\_hip\_importe}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.007\,\text{d\_ln\_hip\_importe\_L0} +0.018\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.001; semivida = 527.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -1.219, ln_hip_importe = 24.398.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0004 | 0.0013 | -0.28 | 0.781 | 0.894 | [-0.0031, 0.0023] |
| d_ln_hip_importe_L0 | 0.0073 | 0.0133 | 0.55 | 0.585 | 0.894 | [-0.0193, 0.0339] |
| d_ln_compraventas | 0.0179 | 0.0138 | 1.30 | 0.199 | 0.596 | [-0.0096, 0.0455] |

Diagnosticos: BG_p = 0.456; BP_p = 0.001; JB_p = 0.761; RESET_p = 0.977; CUSUM_stat = 0.866; CUSUM_p = 0.441; VIF_max = 2.929; r2_adj = 0.129; phi_mitad1 = -0.085; phi_mitad2 = -0.086; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,156 | 4,1 |
| B | -0,001 | 527,2 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,087 | 0,265 | 0,407 | 0,268 | 0,500 | 1,66 | 0,01 | -0,107 | -0,005 | False |
| alquiler | B | 0,970 | 0,851 | 0,228 | 0,706 | 0,646 | 1,00 | 0,10 | -0,085 | -0,079 | False |
| compra | A | 0,699 | 0,056 | 0,711 | 0,113 | 0,708 | 6,10 | 0,20 | -0,396 | -0,285 | False |
| compra | B | 0,456 | 0,001 | 0,761 | 0,977 | 0,441 | 2,93 | 0,13 | -0,085 | -0,086 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | -0,0215 | [-0,0149; 0,0137] | sí |
| alquiler | 2020T1-2022T2 | -0,0074 | [-0,0049; 0,0043] | no |
| alquiler | 2022T3-ultimo | 0,0025 | [0,0075; 0,0318] | sí |
| compra | 2014T1-2019T4 | -0,1153 | [-0,2063; 0,0149] | sí |
| compra | 2020T1-2022T2 | -0,0470 | [-0,0804; 0,0107] | sí |
| compra | 2022T3-ultimo | -0,0392 | [-0,0931; 0,0568] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_11.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | ecm_v1 | 0,497 | 0,521 | sí | 0,496 | no |
| compra | gbm | 2,692 | 3,904 | sí | 2,652 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -1,2 % [-3,0 %, -0,5 %] | -1,2 % [-3,0 %, -0,5 %] | sí |
| construcción adicional (dosis v7.2) | compra | 10 | -1,1 % [-2,4 %, -0,6 %] | -1,1 % [-2,4 %, -0,6 %] | sí |
| movilización de vacías | alquiler | 10 | -8,3 % [-20,1 %, -3,9 %] | -8,3 % [-20,1 %, -3,9 %] | sí |
| movilización de vacías | compra | 10 | -2,9 % [-6,4 %, -1,6 %] | -2,9 % [-6,4 %, -1,6 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -1,1 % [-2,7 %, -0,5 %] | -1,1 % [-2,7 %, -0,5 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| regulación local de turísticos | alquiler | 10 | -0,3 % [-0,7 %, -0,1 %] | -0,3 % [-0,7 %, -0,1 %] | no |
| regulación local de turísticos | compra | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +8,1 % [+4,4 %, +12,3 %] | -2,2 % [-4,5 %, -0,8 %] | no |
| ayudas a la demanda | compra | 10 | +8,1 % [+4,4 %, +12,3 %] | -2,2 % [-4,5 %, -0,8 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +2,0 % [+0,9 %, +3,2 %] | -0,4 % [-1,0 %, -0,1 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -0,3 % [-0,8 %, -0,1 %] | -0,3 % [-0,8 %, -0,1 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -0,3 % [-0,8 %, -0,1 %] | -0,3 % [-0,8 %, -0,1 %] | no |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 22.114 | -2,9 % | no estimable | -1,32 pp [-2,71, -0,87] | — | — |
| movilización de vacías | alquiler | 22.114 | -8,3 % | no estimable | -3,82 pp [-8,72, -1,96] | — | — |
| vivienda pública o asequible | compra | 1.566 | -0,2 % | no estimable | -1,32 pp [-2,71, -0,87] | — | — |
| vivienda pública o asequible | alquiler | 1.566 | -1,1 % | no estimable | -6,83 pp [-14,39, -4,28] | — | — |
| regulación local de turísticos | compra | 371 | -0,0 % | no estimable | -1,32 pp [-2,71, -0,87] | — | — |
| regulación local de turísticos | alquiler | 371 | -0,3 % | no estimable | -7,57 pp [-15,85, -4,82] | — | — |
| construcción adicional | compra | 8.088 | -1,1 % | no estimable | -1,32 pp [-2,71, -0,87] | — | — |
| construcción adicional | alquiler | 8.088 | -1,2 % | no estimable | -1,52 pp [-3,51, -0,70] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 2.362 | -0,3 % | 4 [2, 7] | — | -7,02 pp [-16,04, -2,42] | 14 [6, 41] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 2.362 | -0,3 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 12.968 | +8,1 % | 110 [60, 158] | — | +7,60 pp [+5,96, +8,45] | 49 [28, 86] |
| ayudas a la demanda | alquiler | 12.968 | +8,1 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 12.968 | +2,0 % | 27 [13, 42] | — | +7,60 pp [+5,96, +8,45] | 68 [33, 157] |

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
