# Atlas regional: Galicia (12)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 60,86 | 2019Q4 | 70,74 | +16,2 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 70,67 | 2022Q2 | 79,81 | +12,9 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 80,34 | 2026Q2 | 111,83 | +39,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,70 | 2019Q4 | 91,50 | +3,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,73 | 2022Q2 | 93,88 | +2,3 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 94,37 | 2026Q2 | 102,48 | +8,6 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.006 +0.014\,(\text{ln\_ipc\_alquiler}_{t-1} - [-1.212\,\text{ln\_ocupados}_{t-1} + -0.232\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.534\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.014; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -1.212, ln_pob_total = -0.232.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0010 | 0.0275 | -0.04 | 0.970 | 0.980 | [-0.0559, 0.0538] |
| d_ln_pob_total_L0 | 0.5337 | 0.4681 | 1.14 | 0.258 | 0.706 | [-0.4013, 1.4687] |
| d_ln_hip_importe | 0.0013 | 0.0019 | 0.64 | 0.521 | 0.858 | [-0.0026, 0.0051] |

Diagnosticos: BG_p = 0.001; BP_p = 0.006; JB_p = 0.000; RESET_p = 0.000; CUSUM_stat = 0.541; CUSUM_p = 0.931; VIF_max = 1.000; r2_adj = 0.058; phi_mitad1 = 0.170; phi_mitad2 = -0.338; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = -0.001 +0.031\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.027\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.386\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.031; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.027.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0004 | 0.0003 | -1.12 | 0.264 | 0.562 | [-0.0010, 0.0003] |
| d_y_L1 | 0.3862 | 0.0939 | 4.11 | 0.000 | 0.002 | [0.1989, 0.5736] |
| d_ln_hip_importe | 0.0014 | 0.0015 | 0.94 | 0.351 | 0.664 | [-0.0016, 0.0044] |

Diagnosticos: BG_p = 0.233; BP_p = 0.937; JB_p = 0.121; RESET_p = 0.733; CUSUM_stat = 0.622; CUSUM_p = 0.833; VIF_max = 1.000; r2_adj = 0.334; phi_mitad1 = 0.055; phi_mitad2 = -0.173; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,014 | NA |
| B | 0,031 | NA |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.013 -0.219\,(\text{ln\_ipv}_{t-1} - [0.621\,\text{ln\_ocupados}_{t-1} + 0.052\,\text{ln\_hip\_importe}_{t-1} + -0.626\,\text{ln\_pob\_total}_{t-1}]) +0.044\,\text{d\_ln\_ocupados\_L0} -0.002\,\text{d\_ln\_hip\_importe\_L0} +2.006\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.219; semivida = 2.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.621, ln_hip_importe = 0.052, ln_pob_total = -0.626.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0445 | 0.1026 | 0.43 | 0.666 | 0.900 | [-0.1606, 0.2496] |
| d_ln_hip_importe_L0 | -0.0015 | 0.0098 | -0.15 | 0.878 | 0.962 | [-0.0211, 0.0180] |
| d_ln_pob_total_L0 | 2.0064 | 2.5480 | 0.79 | 0.434 | 0.768 | [-3.0853, 7.0981] |
| d_ln_compraventas | -0.0140 | 0.0105 | -1.33 | 0.188 | 0.480 | [-0.0350, 0.0070] |

Diagnosticos: BG_p = 0.114; BP_p = 0.007; JB_p = 0.688; RESET_p = 0.540; CUSUM_stat = 0.419; CUSUM_p = 0.995; VIF_max = 6.039; r2_adj = 0.273; phi_mitad1 = -0.515; phi_mitad2 = -0.263; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.002 -0.173\,(\text{ln\_ipv}_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.004\,\text{d\_ln\_hip\_importe\_L0} -0.013\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.173; semivida = 3.7 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.013, ln_hip_importe = 0.055.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0018 | 0.0015 | -1.19 | 0.239 | 0.610 | [-0.0047, 0.0012] |
| d_ln_hip_importe_L0 | -0.0044 | 0.0081 | -0.54 | 0.588 | 0.894 | [-0.0206, 0.0118] |
| d_ln_compraventas | -0.0133 | 0.0099 | -1.35 | 0.181 | 0.596 | [-0.0331, 0.0064] |

Diagnosticos: BG_p = 0.087; BP_p = 0.003; JB_p = 0.768; RESET_p = 0.413; CUSUM_stat = 0.470; CUSUM_p = 0.980; VIF_max = 1.615; r2_adj = 0.278; phi_mitad1 = -0.189; phi_mitad2 = -0.197; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,219 | 2,8 |
| B | -0,173 | 3,7 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,001 | 0,006 | 0,000 | 0,000 | 0,931 | 1,00 | 0,06 | 0,170 | -0,338 | True |
| alquiler | B | 0,233 | 0,937 | 0,121 | 0,733 | 0,833 | 1,00 | 0,33 | 0,055 | -0,173 | True |
| compra | A | 0,114 | 0,007 | 0,688 | 0,540 | 0,995 | 6,04 | 0,27 | -0,515 | -0,263 | False |
| compra | B | 0,087 | 0,003 | 0,768 | 0,413 | 0,980 | 1,62 | 0,28 | -0,189 | -0,197 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0140 | [0,0184; 0,0398] | sí |
| alquiler | 2020T1-2022T2 | 0,0049 | [0,0066; 0,0155] | sí |
| alquiler | 2022T3-ultimo | -0,0020 | [0,0011; 0,0137] | sí |
| compra | 2014T1-2019T4 | -0,0377 | [-0,0988; 0,0744] | sí |
| compra | 2020T1-2022T2 | -0,0015 | [-0,0240; 0,0282] | sí |
| compra | 2022T3-ultimo | -0,0166 | [-0,0683; 0,0468] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_12.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,434 | 0,421 | no | 0,421 | no |
| compra | gbm | 2,490 | 3,885 | sí | 2,272 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -0,9 % [-2,1 %, -0,4 %] | -0,9 % [-2,1 %, -0,4 %] | sí |
| construcción adicional (dosis v7.2) | compra | 10 | -0,8 % [-1,6 %, -0,5 %] | -0,8 % [-1,6 %, -0,5 %] | sí |
| movilización de vacías | alquiler | 10 | -8,4 % [-18,1 %, -4,2 %] | -8,4 % [-18,1 %, -4,2 %] | sí |
| movilización de vacías | compra | 10 | -3,0 % [-5,8 %, -1,7 %] | -3,0 % [-5,8 %, -1,7 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -0,8 % [-1,8 %, -0,4 %] | -0,8 % [-1,8 %, -0,4 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,2 % [-0,3 %, -0,1 %] | -0,2 % [-0,3 %, -0,1 %] | no |
| regulación local de turísticos | alquiler | 10 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | no |
| regulación local de turísticos | compra | 10 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,9 % [+2,2 %, +9,1 %] | -4,8 % [-8,8 %, -2,2 %] | no |
| ayudas a la demanda | compra | 10 | +4,9 % [+2,2 %, +9,1 %] | -4,8 % [-8,8 %, -2,2 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,2 % [+0,5 %, +2,4 %] | -1,1 % [-2,2 %, -0,4 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -0,9 % [-1,8 %, -0,4 %] | -0,9 % [-1,8 %, -0,4 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler); rebaja de impuestos y costes de construcción (no difundible) (alquiler); rebaja de impuestos y costes de construcción (no difundible) (compra) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 91.002 | -3,0 % | no estimable | -0,33 pp [-0,61, -0,22] | — | — |
| movilización de vacías | alquiler | 91.002 | -8,4 % | no estimable | -0,94 pp [-1,91, -0,51] | — | — |
| vivienda pública o asequible | compra | 4.724 | -0,2 % | no estimable | -0,33 pp [-0,61, -0,22] | — | — |
| vivienda pública o asequible | alquiler | 4.724 | -0,8 % | no estimable | -1,70 pp [-3,21, -1,12] | — | — |
| regulación local de turísticos | compra | 2.658 | -0,1 % | no estimable | -0,33 pp [-0,61, -0,22] | — | — |
| regulación local de turísticos | alquiler | 2.658 | -0,5 % | no estimable | -1,89 pp [-3,54, -1,26] | — | — |
| construcción adicional | compra | 24.863 | -0,8 % | no estimable | -0,33 pp [-0,61, -0,22] | — | — |
| construcción adicional | alquiler | 24.863 | -0,9 % | no estimable | -0,38 pp [-0,78, -0,18] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 4.894 | -0,9 % | 15 [8, 24] | — | -6,54 pp [-9,96, -3,22] | 15 [10, 31] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 4.894 | -0,9 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 27.080 | +4,9 % | 378 [209, 550] | — | +1,36 pp [+0,75, +1,98] | 76 [53, 130] |
| ayudas a la demanda | alquiler | 27.080 | +4,9 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 27.080 | +1,2 % | 93 [44, 146] | — | +1,36 pp [+0,75, +1,98] | 82 [55, 159] |

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
