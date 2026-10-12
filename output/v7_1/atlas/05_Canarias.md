# Atlas regional: Canarias (05)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 54,54 | 2019Q4 | 67,81 | +24,3 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 68,19 | 2022Q2 | 78,53 | +15,2 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,32 | 2026Q2 | 110,44 | +39,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,59 | 2019Q4 | 91,06 | +2,8 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,51 | 2022Q2 | 93,12 | +1,8 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 93,63 | 2026Q2 | 101,87 | +8,8 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.005 -0.140\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.039\,\text{ln\_ocupados}_{t-1} + 0.157\,\text{ln\_pob\_total}_{t-1}]) +0.007\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.140; semivida = 4.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.039, ln_pob_total = 0.157.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0069 | 0.0064 | 1.08 | 0.282 | 0.706 | [-0.0058, 0.0196] |
| d_ln_pob_total_L0 | 0.2978 | 0.3545 | 0.84 | 0.404 | 0.792 | [-0.4101, 1.0058] |
| d_ln_hip_importe | -0.0000 | 0.0012 | -0.03 | 0.980 | 0.980 | [-0.0024, 0.0023] |

Diagnosticos: BG_p = 0.188; BP_p = 0.546; JB_p = 0.543; RESET_p = 0.118; CUSUM_stat = 0.591; CUSUM_p = 0.876; VIF_max = 2.083; r2_adj = 0.270; phi_mitad1 = -0.280; phi_mitad2 = -0.238; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.000 -0.105\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.001\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.140\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.105; semivida = 6.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.001.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0003 | 0.0001 | -2.28 | 0.026 | 0.120 | [-0.0005, -0.0000] |
| d_y_L1 | 0.1395 | 0.1180 | 1.18 | 0.241 | 0.534 | [-0.0958, 0.3748] |
| d_ln_hip_importe | -0.0007 | 0.0014 | -0.53 | 0.598 | 0.731 | [-0.0034, 0.0020] |

Diagnosticos: BG_p = 0.011; BP_p = 0.099; JB_p = 0.014; RESET_p = 0.655; CUSUM_stat = 1.217; CUSUM_p = 0.104; VIF_max = 1.000; r2_adj = 0.058; phi_mitad1 = -0.245; phi_mitad2 = -0.309; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,140 | 4,6 |
| B | -0,105 | 6,2 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.064 -0.318\,(\text{ln\_ipv}_{t-1} - [0.151\,\text{ln\_ocupados}_{t-1} + -0.004\,\text{ln\_hip\_importe}_{t-1} + 1.080\,\text{ln\_pob\_total}_{t-1}]) +0.098\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +2.245\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.318; semivida = 1.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.151, ln_hip_importe = -0.004, ln_pob_total = 1.080.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0982 | 0.0509 | 1.93 | 0.058 | 0.265 | [-0.0036, 0.1999] |
| d_ln_hip_importe_L0 | -0.0006 | 0.0120 | -0.05 | 0.959 | 0.988 | [-0.0246, 0.0234] |
| d_ln_pob_total_L0 | 2.2455 | 2.8921 | 0.78 | 0.440 | 0.768 | [-3.5339, 8.0249] |
| d_ln_compraventas | -0.0026 | 0.0088 | -0.30 | 0.768 | 0.900 | [-0.0201, 0.0149] |

Diagnosticos: BG_p = 0.055; BP_p = 0.163; JB_p = 0.010; RESET_p = 0.489; CUSUM_stat = 0.638; CUSUM_p = 0.810; VIF_max = 15.545; r2_adj = 0.137; phi_mitad1 = -0.676; phi_mitad2 = -0.785; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.000 -0.102\,(\text{ln\_ipv}_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.107\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.003\,\text{d\_ln\_hip\_importe\_L0} -0.007\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.102; semivida = 6.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.005, ln_hip_importe = -0.107.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0016 | 0.0008 | -1.99 | 0.051 | 0.236 | [-0.0033, 0.0000] |
| d_ln_hip_importe_L0 | -0.0034 | 0.0122 | -0.28 | 0.781 | 0.894 | [-0.0278, 0.0210] |
| d_ln_compraventas | -0.0068 | 0.0090 | -0.76 | 0.453 | 0.871 | [-0.0248, 0.0112] |

Diagnosticos: BG_p = 0.013; BP_p = 0.649; JB_p = 0.007; RESET_p = 0.678; CUSUM_stat = 0.770; CUSUM_p = 0.594; VIF_max = 1.683; r2_adj = 0.055; phi_mitad1 = -0.084; phi_mitad2 = -0.416; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,318 | 1,8 |
| B | -0,102 | 6,5 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,188 | 0,546 | 0,543 | 0,118 | 0,876 | 2,08 | 0,27 | -0,280 | -0,238 | False |
| alquiler | B | 0,011 | 0,099 | 0,014 | 0,655 | 0,104 | 1,00 | 0,06 | -0,245 | -0,309 | False |
| compra | A | 0,055 | 0,163 | 0,010 | 0,489 | 0,810 | 15,54 | 0,14 | -0,676 | -0,785 | False |
| compra | B | 0,013 | 0,649 | 0,007 | 0,678 | 0,594 | 1,68 | 0,06 | -0,084 | -0,416 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0078 | [-0,0260; 0,0026] | sí |
| alquiler | 2020T1-2022T2 | 0,0022 | [-0,0125; 0,0011] | sí |
| alquiler | 2022T3-ultimo | 0,0061 | [-0,0039; 0,0050] | sí |
| compra | 2014T1-2019T4 | 0,0116 | [-0,0789; 0,0781] | sí |
| compra | 2020T1-2022T2 | 0,0386 | [0,0303; 0,1994] | sí |
| compra | 2022T3-ultimo | 0,0211 | [0,0061; 0,0485] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_05.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,411 | 0,450 | sí | 0,418 | sí |
| compra | ar4 | 2,646 | 4,045 | sí | 2,561 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | compra | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -6,7 % [-14,3 %, -3,1 %] | -6,7 % [-14,3 %, -3,1 %] | sí |
| movilización de vacías | compra | 10 | -2,3 % [-4,6 %, -1,3 %] | -2,3 % [-4,6 %, -1,3 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -4,5 % [-10,1 %, -2,0 %] | -4,5 % [-10,1 %, -2,0 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,9 % [-1,9 %, -0,4 %] | -0,9 % [-1,9 %, -0,4 %] | sí |
| regulación local de turísticos | alquiler | 10 | -3,0 % [-7,2 %, -1,0 %] | -3,0 % [-7,2 %, -1,0 %] | sí |
| regulación local de turísticos | compra | 10 | -0,5 % [-1,2 %, -0,2 %] | -0,5 % [-1,2 %, -0,2 %] | no |
| ayudas a la demanda | alquiler | 10 | +5,7 % [+2,7 %, +10,0 %] | -4,2 % [-7,9 %, -1,8 %] | no |
| ayudas a la demanda | compra | 10 | +5,7 % [+2,7 %, +10,0 %] | -4,2 % [-7,9 %, -1,8 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,4 % [+0,6 %, +2,6 %] | -0,9 % [-2,0 %, -0,3 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -0,8 % [-1,7 %, -0,3 %] | -0,8 % [-1,7 %, -0,3 %] | sí |
| rebaja de impuestos y costes de construcción | compra | 10 | -0,8 % [-1,7 %, -0,3 %] | -0,8 % [-1,7 %, -0,3 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 38.060 | -2,3 % | no estimable | -0,61 pp [-1,16, -0,42] | — | — |
| movilización de vacías | alquiler | 38.060 | -6,7 % | no estimable | -1,75 pp [-3,56, -0,94] | — | — |
| vivienda pública o asequible | compra | 14.037 | -0,9 % | no estimable | -0,61 pp [-1,16, -0,42] | — | — |
| vivienda pública o asequible | alquiler | 14.037 | -4,5 % | no estimable | -3,17 pp [-6,10, -2,07] | — | — |
| regulación local de turísticos | compra | 8.695 | -0,5 % | no estimable | -0,61 pp [-1,16, -0,42] | — | — |
| regulación local de turísticos | alquiler | 8.695 | -3,0 % | no estimable | -3,52 pp [-6,63, -2,33] | — | — |
| construcción adicional | compra | 0 | +0,0 % | no estimable | — | — | — |
| construcción adicional | alquiler | 0 | +0,0 % | no estimable | — | — | — |
| rebaja de impuestos y costes de construcción | compra | 4.666 | -0,8 % | 19 [10, 32] | — | -4,11 pp [-6,89, -1,94] | 24 [15, 51] |
| rebaja de impuestos y costes de construcción | alquiler | 4.666 | -0,8 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 25.368 | +5,7 % | 498 [269, 713] | — | +1,22 pp [+0,70, +1,62] | 115 [75, 198] |
| ayudas a la demanda | alquiler | 25.368 | +5,7 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 25.368 | +1,4 % | 124 [56, 189] | — | +1,22 pp [+0,70, +1,62] | 128 [78, 254] |

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
