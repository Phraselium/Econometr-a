# Atlas regional: Cataluña (09)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 49,99 | 2019Q4 | 71,98 | +44,0 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 72,46 | 2022Q2 | 80,61 | +11,2 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 82,34 | 2026Q2 | 109,05 | +32,4 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,67 | 2019Q4 | 92,49 | +4,3 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,78 | 2022Q2 | 95,09 | +2,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 95,44 | 2026Q2 | 101,70 | +6,6 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.105 +0.009\,(\text{ln\_ipc\_alquiler}_{t-1} - [3.603\,\text{ln\_ocupados}_{t-1} + 4.596\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} -0.533\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.009; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 3.603, ln_pob_total = 4.596.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0158 | 0.0234 | -0.67 | 0.503 | 0.856 | [-0.0626, 0.0310] |
| d_ln_pob_total_L0 | -0.5327 | 0.2709 | -1.97 | 0.054 | 0.396 | [-1.0738, 0.0084] |
| d_ln_hip_importe | -0.0005 | 0.0015 | -0.32 | 0.754 | 0.937 | [-0.0034, 0.0025] |

Diagnosticos: BG_p = 0.019; BP_p = 0.039; JB_p = 0.000; RESET_p = 0.890; CUSUM_stat = 0.700; CUSUM_p = 0.711; VIF_max = 1.680; r2_adj = 0.378; phi_mitad1 = 0.008; phi_mitad2 = 0.103; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 +0.012\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.052\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.529\,\text{d\_y\_L1} -0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.012; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.052.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0003 | 0.79 | 0.432 | 0.711 | [-0.0004, 0.0009] |
| d_y_L1 | 0.5294 | 0.0920 | 5.75 | 0.000 | 0.000 | [0.3458, 0.7129] |
| d_ln_hip_importe | -0.0004 | 0.0014 | -0.27 | 0.791 | 0.858 | [-0.0032, 0.0024] |

Diagnosticos: BG_p = 0.825; BP_p = 0.035; JB_p = 0.142; RESET_p = 0.541; CUSUM_stat = 0.867; CUSUM_p = 0.440; VIF_max = 1.000; r2_adj = 0.432; phi_mitad1 = 0.029; phi_mitad2 = 0.064; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,009 | NA |
| B | 0,012 | NA |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.548 -0.111\,(\text{ln\_ipv}_{t-1} - [-1.536\,\text{ln\_ocupados}_{t-1} + 0.279\,\text{ln\_hip\_importe}_{t-1} + -2.336\,\text{ln\_pob\_total}_{t-1}]) +0.084\,\text{d\_ln\_ocupados\_L0} +0.030\,\text{d\_ln\_hip\_importe\_L0} +6.163\,\text{d\_ln\_pob\_total\_L0} -0.006\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.111; semivida = 5.9 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.536, ln_hip_importe = 0.279, ln_pob_total = -2.336.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0844 | 0.1525 | 0.55 | 0.582 | 0.860 | [-0.2203, 0.3891] |
| d_ln_hip_importe_L0 | 0.0299 | 0.0123 | 2.43 | 0.018 | 0.123 | [0.0053, 0.0545] |
| d_ln_pob_total_L0 | 6.1626 | 1.9555 | 3.15 | 0.002 | 0.050 | [2.2549, 10.0704] |
| d_ln_compraventas | -0.0055 | 0.0179 | -0.31 | 0.759 | 0.900 | [-0.0412, 0.0302] |

Diagnosticos: BG_p = 0.005; BP_p = 0.012; JB_p = 0.776; RESET_p = 0.000; CUSUM_stat = 1.322; CUSUM_p = 0.061; VIF_max = 9.369; r2_adj = 0.289; phi_mitad1 = -0.154; phi_mitad2 = -0.106; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.010 -0.061\,(\text{ln\_ipv}_{t-1} - [-0.121\,\text{tasa\_paro\_epa}_{t-1} + -0.084\,\text{ln\_hip\_importe}_{t-1}]) -0.005\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.011\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.061; semivida = 11.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.121, ln_hip_importe = -0.084.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0055 | 0.0019 | -2.83 | 0.006 | 0.085 | [-0.0094, -0.0016] |
| d_ln_hip_importe_L0 | 0.0044 | 0.0119 | 0.37 | 0.712 | 0.894 | [-0.0194, 0.0282] |
| d_ln_compraventas | 0.0113 | 0.0172 | 0.66 | 0.514 | 0.894 | [-0.0231, 0.0456] |

Diagnosticos: BG_p = 0.008; BP_p = 0.001; JB_p = 0.605; RESET_p = 0.068; CUSUM_stat = 1.205; CUSUM_p = 0.110; VIF_max = 4.619; r2_adj = 0.295; phi_mitad1 = -0.115; phi_mitad2 = -0.144; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,111 | 5,9 |
| B | -0,061 | 11,1 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,019 | 0,039 | 0,000 | 0,890 | 0,711 | 1,68 | 0,38 | 0,008 | 0,103 | False |
| alquiler | B | 0,825 | 0,035 | 0,142 | 0,541 | 0,440 | 1,00 | 0,43 | 0,029 | 0,064 | False |
| compra | A | 0,005 | 0,012 | 0,776 | 0,000 | 0,061 | 9,37 | 0,29 | -0,154 | -0,106 | False |
| compra | B | 0,008 | 0,001 | 0,605 | 0,068 | 0,110 | 4,62 | 0,29 | -0,115 | -0,144 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0239 | [-0,0006; 0,0193] | no |
| alquiler | 2020T1-2022T2 | -0,0002 | [-0,0058; -0,0014] | sí |
| alquiler | 2022T3-ultimo | -0,0119 | [-0,0285; -0,0149] | sí |
| compra | 2014T1-2019T4 | 0,1680 | [0,0774; 0,2171] | sí |
| compra | 2020T1-2022T2 | -0,0034 | [-0,1779; 0,0233] | sí |
| compra | 2022T3-ultimo | -0,0071 | [-0,0648; 0,0692] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_09.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | pmg | 0,292 | 0,276 | no | 0,276 | no |
| compra | ar4 | 2,542 | 4,888 | sí | 2,841 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | -0,1 % [-0,3 %, -0,1 %] | -0,1 % [-0,3 %, -0,1 %] | no |
| construcción adicional | precio | 10 | -0,1 % [-0,2 %, -0,1 %] | -0,1 % [-0,2 %, -0,1 %] | no |
| movilización de vacías | alquiler | 10 | -2,7 % [-5,8 %, -1,3 %] | -2,7 % [-5,8 %, -1,3 %] | sí |
| movilización de vacías | precio | 10 | -1,0 % [-1,9 %, -0,6 %] | -1,0 % [-1,9 %, -0,6 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -4,1 % [-9,1 %, -1,8 %] | -4,1 % [-9,1 %, -1,8 %] | sí |
| vivienda pública o asequible | precio | 10 | -0,8 % [-1,7 %, -0,4 %] | -0,8 % [-1,7 %, -0,4 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,6 % [-1,4 %, -0,2 %] | -0,6 % [-1,4 %, -0,2 %] | sí |
| regulación local de turísticos | precio | 10 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,2 % [+1,9 %, +8,2 %] | -5,3 % [-9,4 %, -2,5 %] | no |
| ayudas a la demanda | precio | 10 | +4,2 % [+1,9 %, +8,2 %] | -5,3 % [-9,4 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | precio | 10 | +1,1 % [+0,4 %, +2,1 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción | precio | 10 | -1,1 % [-2,0 %, -0,5 %] | -1,1 % [-2,0 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 75.393 | -1,0 % | no estimable | -0,13 pp [-0,24, -0,09] | — | — |
| movilización de vacías | alquiler | 75.393 | -2,7 % | no estimable | -0,37 pp [-0,74, -0,20] | — | — |
| vivienda pública o asequible | compra | 61.443 | -0,8 % | no estimable | -0,13 pp [-0,24, -0,09] | — | — |
| vivienda pública o asequible | alquiler | 61.443 | -4,1 % | no estimable | -0,66 pp [-1,25, -0,43] | — | — |
| regulación local de turísticos | compra | 8.070 | -0,1 % | no estimable | -0,13 pp [-0,24, -0,09] | — | — |
| regulación local de turísticos | alquiler | 8.070 | -0,6 % | no estimable | -0,73 pp [-1,39, -0,48] | — | — |
| construcción adicional | compra | 9.201 | -0,1 % | no estimable | -0,13 pp [-0,24, -0,09] | — | — |
| construcción adicional | alquiler | 9.201 | -0,1 % | no estimable | -0,15 pp [-0,30, -0,07] | — | — |
| rebaja de impuestos y costes de construcción | compra | 13.882 | -1,1 % | 71 [37, 116] | — | -1,57 pp [-2,24, -0,83] | 64 [45, 121] |
| rebaja de impuestos y costes de construcción | alquiler | 13.882 | -1,1 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 112.690 | +4,2 % | 2.674 [1.466, 3.896] | — | +0,17 pp [+0,08, +0,26] | 478 [352, 793] |
| ayudas a la demanda | alquiler | 112.690 | +4,2 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 112.690 | +1,1 % | 671 [305, 1.032] | — | +0,17 pp [+0,08, +0,26] | 507 [359, 927] |

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
