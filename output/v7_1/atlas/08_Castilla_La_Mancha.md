# Atlas regional: Castilla-La Mancha (08)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 67,83 | 2019Q4 | 75,80 | +11,7 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 75,41 | 2022Q2 | 83,04 | +10,1 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 84,29 | 2026Q2 | 110,86 | +31,5 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 90,97 | 2019Q4 | 91,35 | +0,4 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,48 | 2022Q2 | 93,04 | +1,7 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 93,56 | 2026Q2 | 102,41 | +9,5 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.011 -0.132\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.071\,\text{ln\_ocupados}_{t-1} + 0.828\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.346\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.132; semivida = 4.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.071, ln_pob_total = 0.828.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0008 | 0.0159 | -0.05 | 0.959 | 0.980 | [-0.0326, 0.0310] |
| d_ln_pob_total_L0 | 0.3458 | 0.1846 | 1.87 | 0.066 | 0.396 | [-0.0228, 0.7145] |
| d_ln_hip_importe | 0.0001 | 0.0013 | 0.09 | 0.932 | 0.980 | [-0.0025, 0.0027] |

Diagnosticos: BG_p = 0.191; BP_p = 0.052; JB_p = 0.231; RESET_p = 0.715; CUSUM_stat = 0.564; CUSUM_p = 0.908; VIF_max = 1.009; r2_adj = 0.110; phi_mitad1 = -0.413; phi_mitad2 = -0.340; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.021\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.004\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.154\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.021; semivida = 33.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0002 | 0.0002 | -0.84 | 0.403 | 0.708 | [-0.0006, 0.0003] |
| d_y_L1 | 0.1538 | 0.1215 | 1.27 | 0.210 | 0.509 | [-0.0885, 0.3960] |
| d_ln_hip_importe | -0.0007 | 0.0014 | -0.53 | 0.600 | 0.731 | [-0.0036, 0.0021] |

Diagnosticos: BG_p = 0.339; BP_p = 0.008; JB_p = 0.259; RESET_p = 0.119; CUSUM_stat = 0.731; CUSUM_p = 0.660; VIF_max = 1.000; r2_adj = -0.018; phi_mitad1 = -0.117; phi_mitad2 = -0.070; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,132 | 4,9 |
| B | -0,021 | 33,1 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.042 -0.045\,(\text{ln\_ipv}_{t-1} - [3.379\,\text{ln\_ocupados}_{t-1} + 0.225\,\text{ln\_hip\_importe}_{t-1} + 9.014\,\text{ln\_pob\_total}_{t-1}]) -0.009\,\text{d\_ln\_ocupados\_L0} -0.011\,\text{d\_ln\_hip\_importe\_L0} +0.258\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.045; semivida = 15.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 3.379, ln_hip_importe = 0.225, ln_pob_total = 9.014.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0093 | 0.0928 | -0.10 | 0.920 | 0.982 | [-0.1948, 0.1762] |
| d_ln_hip_importe_L0 | -0.0114 | 0.0103 | -1.10 | 0.273 | 0.600 | [-0.0319, 0.0092] |
| d_ln_pob_total_L0 | 0.2576 | 1.5799 | 0.16 | 0.871 | 0.962 | [-2.8996, 3.4147] |
| d_ln_compraventas | -0.0027 | 0.0143 | -0.19 | 0.852 | 0.962 | [-0.0313, 0.0259] |

Diagnosticos: BG_p = 0.158; BP_p = 0.281; JB_p = 0.006; RESET_p = 0.682; CUSUM_stat = 0.369; CUSUM_p = 0.999; VIF_max = 2.281; r2_adj = 0.192; phi_mitad1 = -0.397; phi_mitad2 = -0.008; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.003 +0.006\,(\text{ln\_ipv}_{t-1} - [0.205\,\text{tasa\_paro\_epa}_{t-1} + -0.994\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.013\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = 0.006; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.205, ln_hip_importe = -0.994.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0009 | 0.0013 | 0.71 | 0.480 | 0.874 | [-0.0017, 0.0035] |
| d_ln_hip_importe_L0 | -0.0127 | 0.0104 | -1.22 | 0.225 | 0.610 | [-0.0335, 0.0080] |
| d_ln_compraventas | -0.0038 | 0.0140 | -0.27 | 0.789 | 0.894 | [-0.0317, 0.0242] |

Diagnosticos: BG_p = 0.193; BP_p = 0.330; JB_p = 0.004; RESET_p = 0.503; CUSUM_stat = 0.741; CUSUM_p = 0.642; VIF_max = 3.132; r2_adj = 0.132; phi_mitad1 = -0.048; phi_mitad2 = -0.036; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,045 | 15,2 |
| B | 0,006 | NA |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,191 | 0,052 | 0,231 | 0,715 | 0,908 | 1,01 | 0,11 | -0,413 | -0,340 | False |
| alquiler | B | 0,339 | 0,008 | 0,259 | 0,119 | 0,660 | 1,00 | -0,02 | -0,117 | -0,070 | False |
| compra | A | 0,158 | 0,281 | 0,006 | 0,682 | 0,999 | 2,28 | 0,19 | -0,397 | -0,008 | False |
| compra | B | 0,193 | 0,330 | 0,004 | 0,503 | 0,642 | 3,13 | 0,13 | -0,048 | -0,036 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | -0,0160 | [-0,0118; 0,0046] | no |
| alquiler | 2020T1-2022T2 | -0,0072 | [-0,0097; -0,0077] | sí |
| alquiler | 2022T3-ultimo | 0,0064 | [0,0029; 0,0056] | no |
| compra | 2014T1-2019T4 | -0,0919 | [-0,2156; -0,0050] | sí |
| compra | 2020T1-2022T2 | -0,0441 | [-0,0582; 0,0245] | sí |
| compra | 2022T3-ultimo | -0,0478 | [-0,0644; -0,0437] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_08.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,410 | 0,430 | sí | 0,351 | no |
| compra | pmg | 2,215 | 3,778 | sí | 2,341 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | compra | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -4,3 % [-8,9 %, -2,0 %] | -4,3 % [-8,9 %, -2,0 %] | sí |
| movilización de vacías | compra | 10 | -1,5 % [-3,0 %, -0,8 %] | -1,5 % [-3,0 %, -0,8 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -2,8 % [-6,4 %, -1,2 %] | -2,8 % [-6,4 %, -1,2 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,5 % [-1,2 %, -0,3 %] | -0,5 % [-1,2 %, -0,3 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | no |
| regulación local de turísticos | compra | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,5 % [+2,0 %, +8,5 %] | -5,2 % [-9,3 %, -2,4 %] | no |
| ayudas a la demanda | compra | 10 | +4,5 % [+2,0 %, +8,5 %] | -5,2 % [-9,3 %, -2,4 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,3 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |
| rebaja de impuestos y costes de construcción | compra | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 38.290 | -1,5 % | no estimable | -0,39 pp [-0,74, -0,27] | — | — |
| movilización de vacías | alquiler | 38.290 | -4,3 % | no estimable | -1,13 pp [-2,23, -0,60] | — | — |
| vivienda pública o asequible | compra | 13.523 | -0,5 % | no estimable | -0,39 pp [-0,74, -0,27] | — | — |
| vivienda pública o asequible | alquiler | 13.523 | -2,8 % | no estimable | -2,02 pp [-3,86, -1,32] | — | — |
| regulación local de turísticos | compra | 795 | -0,0 % | no estimable | -0,39 pp [-0,74, -0,27] | — | — |
| regulación local de turísticos | alquiler | 795 | -0,2 % | no estimable | -2,26 pp [-4,25, -1,49] | — | — |
| construcción adicional | compra | 0 | +0,0 % | no estimable | — | — | — |
| construcción adicional | alquiler | 0 | +0,0 % | no estimable | — | — | — |
| rebaja de impuestos y costes de construcción | compra | 6.473 | -1,0 % | 14 [7, 23] | — | -7,51 pp [-11,09, -3,87] | 13 [9, 26] |
| rebaja de impuestos y costes de construcción | alquiler | 6.473 | -1,0 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 34.495 | +4,5 % | 350 [192, 505] | — | +1,37 pp [+0,70, +2,05] | 65 [46, 108] |
| ayudas a la demanda | alquiler | 34.495 | +4,5 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 34.495 | +1,1 % | 85 [39, 134] | — | +1,37 pp [+0,70, +2,05] | 69 [48, 129] |

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
