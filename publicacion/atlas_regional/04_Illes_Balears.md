<!-- Generado por `make publicacion` desde output/v7_1/atlas/04_Illes_Balears.md. No editar a mano: se regenera y un test lo comprueba. -->

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

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0437 | [-0,0098; 0,0345] | no |
| alquiler | 2020T1-2022T2 | 0,0126 | [-0,0002; 0,0105] | no |
| alquiler | 2022T3-ultimo | 0,0134 | [-0,0019; 0,0099] | no |
| compra | 2014T1-2019T4 | 0,1474 | [-0,0309; 0,3019] | sí |
| compra | 2020T1-2022T2 | 0,0508 | [0,0129; 0,0773] | sí |
| compra | 2022T3-ultimo | -0,0222 | [-0,1081; -0,0226] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_04.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | mixto | 0,684 | 0,679 | no | 0,679 | no |
| compra | ar4 | 3,047 | 4,281 | sí | 3,058 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | precio | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -4,1 % [-8,8 %, -2,0 %] | -4,1 % [-8,8 %, -2,0 %] | sí |
| movilización de vacías | precio | 10 | -1,4 % [-2,8 %, -0,8 %] | -1,4 % [-2,8 %, -0,8 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -3,8 % [-8,5 %, -1,7 %] | -3,8 % [-8,5 %, -1,7 %] | sí |
| vivienda pública o asequible | precio | 10 | -0,7 % [-1,6 %, -0,3 %] | -0,7 % [-1,6 %, -0,3 %] | sí |
| regulación local de turísticos | alquiler | 10 | -2,9 % [-6,8 %, -1,0 %] | -2,9 % [-6,8 %, -1,0 %] | sí |
| regulación local de turísticos | precio | 10 | -0,5 % [-1,2 %, -0,2 %] | -0,5 % [-1,2 %, -0,2 %] | sí |
| ayudas a la demanda | alquiler | 10 | +4,2 % [+1,8 %, +8,0 %] | -5,5 % [-9,5 %, -2,5 %] | no |
| ayudas a la demanda | precio | 10 | +4,2 % [+1,8 %, +8,0 %] | -5,5 % [-9,5 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | precio | 10 | +1,0 % [+0,4 %, +2,2 %] | -1,3 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción | precio | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); regulación local de turísticos (alquiler); regulación local de turísticos (precio); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 19.037 | -1,4 % | no estimable | -0,76 pp [-1,42, -0,52] | — | — |
| movilización de vacías | alquiler | 19.037 | -4,1 % | no estimable | -2,18 pp [-4,39, -1,18] | — | — |
| vivienda pública o asequible | compra | 9.629 | -0,7 % | no estimable | -0,76 pp [-1,42, -0,52] | — | — |
| vivienda pública o asequible | alquiler | 9.629 | -3,8 % | no estimable | -3,95 pp [-7,46, -2,59] | — | — |
| regulación local de turísticos | compra | 6.794 | -0,5 % | no estimable | -0,76 pp [-1,42, -0,52] | — | — |
| regulación local de turísticos | alquiler | 6.794 | -2,9 % | no estimable | -4,37 pp [-8,18, -2,90] | — | — |
| construcción adicional | compra | 0 | +0,0 % | no estimable | — | — | — |
| construcción adicional | alquiler | 0 | +0,0 % | no estimable | — | — | — |
| rebaja de impuestos y costes de construcción | compra | 4.215 | -1,1 % | 31 [16, 50] | — | -3,60 pp [-5,16, -1,95] | 28 [19, 51] |
| rebaja de impuestos y costes de construcción | alquiler | 4.215 | -1,1 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 14.667 | +4,2 % | 511 [278, 729] | — | +0,89 pp [+0,44, +1,36] | 89 [65, 145] |
| ayudas a la demanda | alquiler | 14.667 | +4,2 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 14.667 | +1,0 % | 127 [58, 194] | — | +0,89 pp [+0,44, +1,36] | 95 [67, 169] |

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
