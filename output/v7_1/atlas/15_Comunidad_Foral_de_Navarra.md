# Atlas regional: Comunidad Foral de Navarra (15)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 60,95 | 2019Q4 | 68,60 | +12,6 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 69,84 | 2022Q2 | 76,37 | +9,4 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 77,30 | 2026Q2 | 109,17 | +41,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 89,33 | 2019Q4 | 91,49 | +2,4 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,11 | 2022Q2 | 94,43 | +2,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 94,90 | 2026Q2 | 101,48 | +6,9 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.015 -0.032\,(\text{ln\_ipc\_alquiler}_{t-1} - [-1.191\,\text{ln\_ocupados}_{t-1} + 0.748\,\text{ln\_pob\_total}_{t-1}]) -0.044\,\text{d\_ln\_ocupados\_L0} +1.579\,\text{d\_ln\_pob\_total\_L0} -0.005\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.032; semivida = 21.0 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.191, ln_pob_total = 0.748.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0436 | 0.0256 | -1.70 | 0.093 | 0.396 | [-0.0946, 0.0075] |
| d_ln_pob_total_L0 | 1.5791 | 0.8796 | 1.80 | 0.077 | 0.396 | [-0.1777, 3.3359] |
| d_ln_hip_importe | -0.0053 | 0.0023 | -2.26 | 0.027 | 0.274 | [-0.0100, -0.0006] |

Diagnosticos: BG_p = 0.308; BP_p = 0.125; JB_p = 0.000; RESET_p = 0.513; CUSUM_stat = 0.576; CUSUM_p = 0.895; VIF_max = 1.315; r2_adj = 0.285; phi_mitad1 = -0.116; phi_mitad2 = -0.125; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.039\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.285\,\text{d\_y\_L1} -0.004\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.039; semivida = 17.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.004.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0003 | 0.0003 | 1.27 | 0.209 | 0.509 | [-0.0002, 0.0009] |
| d_y_L1 | 0.2846 | 0.0930 | 3.06 | 0.003 | 0.027 | [0.0991, 0.4700] |
| d_ln_hip_importe | -0.0045 | 0.0019 | -2.30 | 0.025 | 0.120 | [-0.0084, -0.0006] |

Diagnosticos: BG_p = 0.997; BP_p = 0.332; JB_p = 0.006; RESET_p = 0.764; CUSUM_stat = 0.748; CUSUM_p = 0.631; VIF_max = 1.000; r2_adj = 0.381; phi_mitad1 = -0.047; phi_mitad2 = 0.003; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,032 | 21,0 |
| B | -0,039 | 17,4 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -1.156 -0.271\,(\text{ln\_ipv}_{t-1} - [-0.372\,\text{ln\_ocupados}_{t-1} + -0.139\,\text{ln\_hip\_importe}_{t-1} + -3.632\,\text{ln\_pob\_total}_{t-1}]) -0.095\,\text{d\_ln\_ocupados\_L0} -0.026\,\text{d\_ln\_hip\_importe\_L0} -20.330\,\text{d\_ln\_pob\_total\_L0} +0.008\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.271; semivida = 2.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.372, ln_hip_importe = -0.139, ln_pob_total = -3.632.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0950 | 0.1116 | -0.85 | 0.398 | 0.752 | [-0.3181, 0.1281] |
| d_ln_hip_importe_L0 | -0.0257 | 0.0149 | -1.73 | 0.089 | 0.316 | [-0.0554, 0.0040] |
| d_ln_pob_total_L0 | -20.3300 | 5.9874 | -3.40 | 0.001 | 0.040 | [-32.2949, -8.3651] |
| d_ln_compraventas | 0.0083 | 0.0119 | 0.69 | 0.490 | 0.813 | [-0.0155, 0.0320] |

Diagnosticos: BG_p = 0.156; BP_p = 0.376; JB_p = 0.214; RESET_p = 0.115; CUSUM_stat = 0.381; CUSUM_p = 0.999; VIF_max = 5.271; r2_adj = 0.182; phi_mitad1 = -0.445; phi_mitad2 = -0.307; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.014 -0.065\,(\text{ln\_ipv}_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.008\,\text{d\_ln\_hip\_importe\_L0} -0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.065; semivida = 10.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.005, ln_hip_importe = -0.196.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0015 | 0.0014 | -1.02 | 0.311 | 0.672 | [-0.0044, 0.0014] |
| d_ln_hip_importe_L0 | -0.0082 | 0.0146 | -0.56 | 0.577 | 0.894 | [-0.0372, 0.0209] |
| d_ln_compraventas | -0.0011 | 0.0120 | -0.09 | 0.926 | 0.964 | [-0.0251, 0.0229] |

Diagnosticos: BG_p = 0.257; BP_p = 0.070; JB_p = 0.099; RESET_p = 0.090; CUSUM_stat = 0.590; CUSUM_p = 0.878; VIF_max = 2.286; r2_adj = 0.059; phi_mitad1 = -0.112; phi_mitad2 = -0.172; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,271 | 2,2 |
| B | -0,065 | 10,3 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,308 | 0,125 | 0,000 | 0,513 | 0,895 | 1,32 | 0,29 | -0,116 | -0,125 | False |
| alquiler | B | 0,997 | 0,332 | 0,006 | 0,764 | 0,631 | 1,00 | 0,38 | -0,047 | 0,003 | True |
| compra | A | 0,156 | 0,376 | 0,214 | 0,115 | 0,999 | 5,27 | 0,18 | -0,445 | -0,307 | False |
| compra | B | 0,257 | 0,070 | 0,099 | 0,090 | 0,878 | 2,29 | 0,06 | -0,112 | -0,172 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0003 | [-0,0197; -0,0039] | sí |
| alquiler | 2020T1-2022T2 | -0,0020 | [-0,0072; -0,0031] | sí |
| alquiler | 2022T3-ultimo | -0,0063 | [-0,0078; -0,0065] | sí |
| compra | 2014T1-2019T4 | -0,1048 | [-0,1993; 0,0695] | sí |
| compra | 2020T1-2022T2 | -0,0024 | [-0,0260; 0,0244] | sí |
| compra | 2022T3-ultimo | 0,0394 | [0,0364; 0,0549] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_15.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,368 | 0,787 | sí | 0,421 | sí |
| compra | ar4 | 2,639 | 5,527 | sí | 2,548 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | -1,5 % [-3,5 %, -0,7 %] | -1,5 % [-3,5 %, -0,7 %] | sí |
| construcción adicional | precio | 10 | -1,4 % [-2,7 %, -0,8 %] | -1,4 % [-2,7 %, -0,8 %] | sí |
| movilización de vacías | alquiler | 10 | -2,5 % [-5,5 %, -1,3 %] | -2,5 % [-5,5 %, -1,3 %] | sí |
| movilización de vacías | precio | 10 | -0,9 % [-1,8 %, -0,5 %] | -0,9 % [-1,8 %, -0,5 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -3,6 % [-8,2 %, -1,6 %] | -3,6 % [-8,2 %, -1,6 %] | sí |
| vivienda pública o asequible | precio | 10 | -0,7 % [-1,6 %, -0,3 %] | -0,7 % [-1,6 %, -0,3 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,2 % [-0,5 %, -0,1 %] | -0,2 % [-0,5 %, -0,1 %] | no |
| regulación local de turísticos | precio | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,2 % [+1,8 %, +8,3 %] | -5,4 % [-9,6 %, -2,5 %] | no |
| ayudas a la demanda | precio | 10 | +4,2 % [+1,8 %, +8,3 %] | -5,4 % [-9,6 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | precio | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,0 % [-2,0 %, -0,5 %] | -1,0 % [-2,0 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción | precio | 10 | -1,0 % [-2,0 %, -0,5 %] | -1,0 % [-2,0 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (precio); movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 5.922 | -0,9 % | no estimable | -1,51 pp [-2,81, -1,03] | — | — |
| movilización de vacías | alquiler | 5.922 | -2,5 % | no estimable | -4,29 pp [-8,72, -2,34] | — | — |
| vivienda pública o asequible | compra | 4.585 | -0,7 % | no estimable | -1,51 pp [-2,81, -1,03] | — | — |
| vivienda pública o asequible | alquiler | 4.585 | -3,6 % | no estimable | -7,78 pp [-14,64, -5,12] | — | — |
| regulación local de turísticos | compra | 259 | -0,0 % | no estimable | -1,51 pp [-2,81, -1,03] | — | — |
| regulación local de turísticos | alquiler | 259 | -0,2 % | no estimable | -8,64 pp [-16,09, -5,80] | — | — |
| construcción adicional | compra | 9.093 | -1,4 % | no estimable | -1,51 pp [-2,81, -1,03] | — | — |
| construcción adicional | alquiler | 9.093 | -1,5 % | no estimable | -1,70 pp [-3,61, -0,83] | — | — |
| rebaja de impuestos y costes de construcción | compra | 1.765 | -1,0 % | 6 [3, 10] | — | -17,53 pp [-25,19, -9,36] | 6 [4, 11] |
| rebaja de impuestos y costes de construcción | alquiler | 1.765 | -1,0 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 7.480 | +4,2 % | 125 [69, 181] | — | +3,62 pp [+1,81, +5,56] | 22 [16, 37] |
| ayudas a la demanda | alquiler | 7.480 | +4,2 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 7.480 | +1,1 % | 31 [14, 48] | — | +3,62 pp [+1,81, +5,56] | 24 [17, 43] |

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
