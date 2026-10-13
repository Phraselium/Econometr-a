# Atlas regional: Comunitat Valenciana (10)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 57,02 | 2019Q4 | 69,04 | +21,1 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 69,33 | 2022Q2 | 78,11 | +12,7 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 78,89 | 2026Q2 | 111,70 | +41,6 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 85,95 | 2019Q4 | 88,13 | +2,5 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 88,68 | 2022Q2 | 91,08 | +2,7 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 91,48 | 2026Q2 | 103,28 | +12,9 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.138 -0.147\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.072\,\text{ln\_ocupados}_{t-1} + 0.979\,\text{ln\_pob\_total}_{t-1}]) -0.012\,\text{d\_ln\_ocupados\_L0} +0.601\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.147; semivida = 4.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.072, ln_pob_total = 0.979.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0120 | 0.0154 | -0.78 | 0.438 | 0.823 | [-0.0428, 0.0187] |
| d_ln_pob_total_L0 | 0.6007 | 0.3513 | 1.71 | 0.092 | 0.396 | [-0.1009, 1.3024] |
| d_ln_hip_importe | -0.0019 | 0.0025 | -0.76 | 0.452 | 0.823 | [-0.0070, 0.0031] |

Diagnosticos: BG_p = 0.000; BP_p = 0.019; JB_p = 0.721; RESET_p = 0.205; CUSUM_stat = 0.742; CUSUM_p = 0.640; VIF_max = 1.715; r2_adj = 0.239; phi_mitad1 = -0.334; phi_mitad2 = -0.116; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.019\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.407\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.019; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.014.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0002 | -0.52 | 0.602 | 0.731 | [-0.0006, 0.0003] |
| d_y_L1 | 0.4068 | 0.1162 | 3.50 | 0.001 | 0.009 | [0.1752, 0.6385] |
| d_ln_hip_importe | -0.0018 | 0.0024 | -0.74 | 0.460 | 0.711 | [-0.0066, 0.0030] |

Diagnosticos: BG_p = 0.009; BP_p = 0.325; JB_p = 0.510; RESET_p = 0.509; CUSUM_stat = 0.570; CUSUM_p = 0.902; VIF_max = 1.000; r2_adj = 0.345; phi_mitad1 = -0.060; phi_mitad2 = 0.022; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,147 | 4,4 |
| B | 0,019 | NA |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.179 -0.188\,(\text{ln\_ipv}_{t-1} - [0.213\,\text{ln\_ocupados}_{t-1} + -0.104\,\text{ln\_hip\_importe}_{t-1} + -1.093\,\text{ln\_pob\_total}_{t-1}]) -0.032\,\text{d\_ln\_ocupados\_L0} -0.023\,\text{d\_ln\_hip\_importe\_L0} +2.330\,\text{d\_ln\_pob\_total\_L0} -0.034\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.188; semivida = 3.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.213, ln_hip_importe = -0.104, ln_pob_total = -1.093.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0324 | 0.0806 | -0.40 | 0.689 | 0.900 | [-0.1933, 0.1286] |
| d_ln_hip_importe_L0 | -0.0226 | 0.0132 | -1.71 | 0.092 | 0.316 | [-0.0490, 0.0038] |
| d_ln_pob_total_L0 | 2.3298 | 1.6094 | 1.45 | 0.153 | 0.443 | [-0.8864, 5.5459] |
| d_ln_compraventas | -0.0341 | 0.0147 | -2.32 | 0.024 | 0.146 | [-0.0635, -0.0047] |

Diagnosticos: BG_p = 0.275; BP_p = 0.009; JB_p = 0.001; RESET_p = 0.001; CUSUM_stat = 0.738; CUSUM_p = 0.648; VIF_max = 5.094; r2_adj = 0.164; phi_mitad1 = -0.249; phi_mitad2 = -0.415; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.013 -0.173\,(\text{ln\_ipv}_{t-1} - [-0.006\,\text{tasa\_paro\_epa}_{t-1} + -0.080\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.016\,\text{d\_ln\_hip\_importe\_L0} -0.032\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.173; semivida = 3.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.006, ln_hip_importe = -0.080.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0011 | 0.29 | 0.775 | 0.894 | [-0.0019, 0.0025] |
| d_ln_hip_importe_L0 | -0.0162 | 0.0123 | -1.32 | 0.193 | 0.596 | [-0.0408, 0.0084] |
| d_ln_compraventas | -0.0321 | 0.0136 | -2.36 | 0.021 | 0.178 | [-0.0592, -0.0050] |

Diagnosticos: BG_p = 0.244; BP_p = 0.001; JB_p = 0.000; RESET_p = 0.001; CUSUM_stat = 0.882; CUSUM_p = 0.418; VIF_max = 2.015; r2_adj = 0.150; phi_mitad1 = -0.205; phi_mitad2 = -0.248; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,188 | 3,3 |
| B | -0,173 | 3,7 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,000 | 0,019 | 0,721 | 0,205 | 0,640 | 1,71 | 0,24 | -0,334 | -0,116 | False |
| alquiler | B | 0,009 | 0,325 | 0,510 | 0,509 | 0,902 | 1,00 | 0,35 | -0,060 | 0,022 | True |
| compra | A | 0,275 | 0,009 | 0,001 | 0,001 | 0,648 | 5,09 | 0,16 | -0,249 | -0,415 | False |
| compra | B | 0,244 | 0,001 | 0,000 | 0,001 | 0,418 | 2,01 | 0,15 | -0,205 | -0,248 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0062 | [-0,0015; 0,0051] | no |
| alquiler | 2020T1-2022T2 | 0,0097 | [-0,0049; 0,0072] | sí |
| alquiler | 2022T3-ultimo | 0,0211 | [-0,0080; 0,0158] | no |
| compra | 2014T1-2019T4 | 0,0004 | [-0,0489; 0,0222] | sí |
| compra | 2020T1-2022T2 | 0,0011 | [-0,0492; 0,0922] | sí |
| compra | 2022T3-ultimo | 0,0046 | [-0,1017; 0,0554] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_10.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,565 | 0,658 | sí | 0,658 | sí |
| compra | pmg | 2,197 | 4,095 | sí | 2,370 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -2,1 % [-4,7 %, -0,9 %] | -2,1 % [-4,7 %, -0,9 %] | sí |
| construcción adicional (dosis v7.2) | compra | 10 | -1,9 % [-3,6 %, -1,1 %] | -1,9 % [-3,6 %, -1,1 %] | sí |
| movilización de vacías | alquiler | 10 | -4,4 % [-9,4 %, -2,1 %] | -4,4 % [-9,4 %, -2,1 %] | sí |
| movilización de vacías | compra | 10 | -1,6 % [-3,1 %, -0,9 %] | -1,6 % [-3,1 %, -0,9 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -5,2 % [-11,1 %, -2,3 %] | -5,2 % [-11,1 %, -2,3 %] | sí |
| vivienda pública o asequible | compra | 10 | -1,0 % [-2,2 %, -0,5 %] | -1,0 % [-2,2 %, -0,5 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,9 % [-2,1 %, -0,3 %] | -0,9 % [-2,1 %, -0,3 %] | sí |
| regulación local de turísticos | compra | 10 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | no |
| ayudas a la demanda | alquiler | 10 | +5,4 % [+2,6 %, +9,6 %] | -4,4 % [-8,2 %, -1,9 %] | no |
| ayudas a la demanda | compra | 10 | +5,4 % [+2,6 %, +9,6 %] | -4,4 % [-8,2 %, -1,9 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,3 % [+0,6 %, +2,5 %] | -1,0 % [-2,0 %, -0,4 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -0,8 % [-1,7 %, -0,3 %] | -0,8 % [-1,7 %, -0,3 %] | sí |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -0,8 % [-1,7 %, -0,3 %] | -0,8 % [-1,7 %, -0,3 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler); vivienda pública o asequible (compra); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (no difundible) (alquiler); rebaja de impuestos y costes de construcción (no difundible) (compra) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

### Apartado provincial: provincias de Alicante (03), Castellón (12) y Valencia (46), y València ciudad

Coeficientes de R4b (provincia_valencia.csv; 21 observaciones, especificación core; asociación, C4):

| provincia | dependiente | Δln población | Δln ocupados EPA | Δln importe hipotecario | n |
|---|---|---|---|---|---|
| 03 | valor_tasado | 4,245 | -0,231 | 0,035 | 21 |
| 12 | valor_tasado | -0,357 | -0,047 | 0,010 | 21 |
| 46 | valor_tasado | 4,931 | -0,574 | 0,047 | 21 |
| 03 | ipc_alquiler | 0,137 | -0,108 | 0,008 | 21 |
| 12 | ipc_alquiler | 1,628 | -0,052 | 0,007 | 21 |
| 46 | ipc_alquiler | 0,641 | -0,013 | -0,008 | 21 |

N pequeño y sin inferencia validada: se leen como descriptivos. Variación del valor tasado (€/m², Ministerio):

| territorio | periodo | inicio | fin | variación |
|---|---|---|---|---|
| Alicante (03) | 2014T1-2019T4 | 2014Q1 1206 | 2019Q4 1315 | +9,0 % |
| Alicante (03) | 2020T1-2022T2 | 2020Q1 1295 | 2022Q2 1401 | +8,2 % |
| Alicante (03) | 2022T3-último | 2022Q3 1412 | 2026Q2 2021 | +43,1 % |
| Castellón (12) | 2014T1-2019T4 | 2014Q1 1053 | 2019Q4 1067 | +1,3 % |
| Castellón (12) | 2020T1-2022T2 | 2020Q1 1040 | 2022Q2 1085 | +4,3 % |
| Castellón (12) | 2022T3-último | 2022Q3 1064 | 2026Q2 1464 | +37,6 % |
| Valencia (provincia) (46) | 2014T1-2019T4 | 2014Q1 1053 | 2019Q4 1196 | +13,7 % |
| Valencia (provincia) (46) | 2020T1-2022T2 | 2020Q1 1184 | 2022Q2 1301 | +9,8 % |
| Valencia (provincia) (46) | 2022T3-último | 2022Q3 1289 | 2026Q2 1980 | +53,6 % |
| València ciudad (municipio) | 2014T1-2019T4 | 2014Q1 1179 | 2019Q4 1486 | +26,0 % |
| València ciudad (municipio) | 2020T1-2022T2 | 2020Q1 1507 | 2022Q2 1701 | +12,9 % |
| València ciudad (municipio) | 2022T3-último | 2022Q3 1685 | 2026Q2 2973 | +76,4 % |

Datos de València ciudad (data/processed/valencia.csv): valor tasado trimestral, transacciones, viviendas turísticas desde 2020T3 y 19 distritos con SERPAVI anual. No hay IPV ni IPC de alquiler municipal en el INE a esta escala; no se estima un ECM municipal (N insuficiente).

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 82.219 | -1,6 % | no estimable | -0,19 pp [-0,35, -0,13] | — | — |
| movilización de vacías | alquiler | 82.219 | -4,4 % | no estimable | -0,55 pp [-1,08, -0,29] | — | — |
| vivienda pública o asequible | compra | 51.218 | -1,0 % | no estimable | -0,19 pp [-0,35, -0,13] | — | — |
| vivienda pública o asequible | alquiler | 51.218 | -5,2 % | no estimable | -0,98 pp [-1,87, -0,65] | — | — |
| regulación local de turísticos | compra | 8.348 | -0,2 % | no estimable | -0,19 pp [-0,35, -0,13] | — | — |
| regulación local de turísticos | alquiler | 8.348 | -0,9 % | no estimable | -1,09 pp [-2,03, -0,73] | — | — |
| construcción adicional | compra | 98.685 | -1,9 % | no estimable | -0,19 pp [-0,35, -0,13] | — | — |
| construcción adicional | alquiler | 98.685 | -2,1 % | no estimable | -0,22 pp [-0,46, -0,11] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 14.256 | -0,8 % | 50 [26, 81] | — | -1,72 pp [-2,78, -0,82] | 58 [36, 121] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 14.256 | -0,8 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 109.301 | +5,4 % | 1.777 [984, 2.572] | — | +0,32 pp [+0,18, +0,44] | 392 [263, 665] |
| ayudas a la demanda | alquiler | 109.301 | +5,4 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 109.301 | +1,3 % | 435 [205, 684] | — | +0,32 pp [+0,18, +0,44] | 431 [272, 854] |

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
