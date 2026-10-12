# Atlas regional: Andalucía (01)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 53,32 | 2019Q4 | 66,17 | +24,1 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 66,67 | 2022Q2 | 76,20 | +14,3 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 77,43 | 2026Q2 | 110,90 | +43,2 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,39 | 2019Q4 | 90,44 | +2,3 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 90,66 | 2022Q2 | 92,45 | +2,0 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 92,86 | 2026Q2 | 102,28 | +10,1 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.050 +0.017\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.301\,\text{ln\_ocupados}_{t-1} + 1.631\,\text{ln\_pob\_total}_{t-1}]) +0.003\,\text{d\_ln\_ocupados\_L0} -0.448\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.017; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.301, ln_pob_total = 1.631.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0028 | 0.0100 | 0.28 | 0.784 | 0.952 | [-0.0172, 0.0228] |
| d_ln_pob_total_L0 | -0.4475 | 0.3593 | -1.25 | 0.217 | 0.652 | [-1.1652, 0.2701] |
| d_ln_hip_importe | 0.0004 | 0.0023 | 0.19 | 0.852 | 0.965 | [-0.0041, 0.0050] |

Diagnosticos: BG_p = 0.016; BP_p = 0.012; JB_p = 0.000; RESET_p = 0.636; CUSUM_stat = 0.650; CUSUM_p = 0.792; VIF_max = 1.133; r2_adj = -0.047; phi_mitad1 = -0.342; phi_mitad2 = -0.074; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.034\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.002\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.162\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.034; semivida = 20.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.002.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0000 | 0.0002 | -0.08 | 0.933 | 0.954 | [-0.0003, 0.0003] |
| d_y_L1 | 0.1621 | 0.1208 | 1.34 | 0.184 | 0.494 | [-0.0789, 0.4031] |
| d_ln_hip_importe | 0.0000 | 0.0022 | 0.00 | 1.000 | 1.000 | [-0.0045, 0.0045] |

Diagnosticos: BG_p = 0.038; BP_p = 0.023; JB_p = 0.000; RESET_p = 0.165; CUSUM_stat = 0.667; CUSUM_p = 0.765; VIF_max = 1.000; r2_adj = -0.019; phi_mitad1 = -0.309; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,017 | NA |
| B | -0,034 | 20,1 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.482 -0.008\,(\text{ln\_ipv}_{t-1} - [-9.625\,\text{ln\_ocupados}_{t-1} + 2.713\,\text{ln\_hip\_importe}_{t-1} + -32.573\,\text{ln\_pob\_total}_{t-1}]) -0.125\,\text{d\_ln\_ocupados\_L0} +0.035\,\text{d\_ln\_hip\_importe\_L0} -0.058\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.008; semivida = 83.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -9.625, ln_hip_importe = 2.713, ln_pob_total = -32.573.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.1253 | 0.0509 | -2.46 | 0.017 | 0.123 | [-0.2269, -0.0236] |
| d_ln_hip_importe_L0 | 0.0353 | 0.0128 | 2.76 | 0.008 | 0.102 | [0.0098, 0.0608] |
| d_ln_pob_total_L0 | -0.0580 | 1.7133 | -0.03 | 0.973 | 0.988 | [-3.4817, 3.3657] |
| d_ln_compraventas | -0.0144 | 0.0159 | -0.91 | 0.368 | 0.735 | [-0.0463, 0.0174] |

Diagnosticos: BG_p = 0.003; BP_p = 0.060; JB_p = 0.232; RESET_p = 0.778; CUSUM_stat = 0.424; CUSUM_p = 0.994; VIF_max = 10.813; r2_adj = 0.089; phi_mitad1 = -0.455; phi_mitad2 = -0.153; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.036 -0.053\,(\text{ln\_ipv}_{t-1} - [0.011\,\text{tasa\_paro\_epa}_{t-1} + 0.343\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.012\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.053; semivida = 12.8 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.011, ln_hip_importe = 0.343.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0015 | 0.0008 | 2.04 | 0.045 | 0.231 | [0.0000, 0.0031] |
| d_ln_hip_importe_L0 | 0.0277 | 0.0123 | 2.25 | 0.027 | 0.199 | [0.0032, 0.0523] |
| d_ln_compraventas | -0.0117 | 0.0158 | -0.74 | 0.461 | 0.871 | [-0.0432, 0.0198] |

Diagnosticos: BG_p = 0.033; BP_p = 0.215; JB_p = 0.240; RESET_p = 0.571; CUSUM_stat = 0.601; CUSUM_p = 0.863; VIF_max = 4.630; r2_adj = 0.094; phi_mitad1 = -0.148; phi_mitad2 = -0.070; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,008 | 83,1 |
| B | -0,053 | 12,8 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,016 | 0,012 | 0,000 | 0,636 | 0,792 | 1,13 | -0,05 | -0,342 | -0,074 | False |
| alquiler | B | 0,038 | 0,023 | 0,000 | 0,165 | 0,765 | 1,00 | -0,02 | -0,309 | -0,083 | False |
| compra | A | 0,003 | 0,060 | 0,232 | 0,778 | 0,994 | 10,81 | 0,09 | -0,455 | -0,153 | False |
| compra | B | 0,033 | 0,215 | 0,240 | 0,571 | 0,863 | 4,63 | 0,09 | -0,148 | -0,070 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0033 | [-0,0032; 0,0029] | sí |
| alquiler | 2020T1-2022T2 | -0,0023 | [-0,0067; -0,0029] | sí |
| alquiler | 2022T3-ultimo | 0,0109 | [0,0123; 0,0172] | sí |
| compra | 2014T1-2019T4 | 0,0156 | [-0,0306; 0,0405] | sí |
| compra | 2020T1-2022T2 | 0,0288 | [0,0180; 0,0399] | sí |
| compra | 2022T3-ultimo | 0,0383 | [0,0124; 0,0677] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_01.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,405 | 0,438 | sí | 0,400 | no |
| compra | ar4 | 2,863 | 4,127 | sí | 2,702 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | compra | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -3,2 % [-6,8 %, -1,5 %] | -3,2 % [-6,8 %, -1,5 %] | sí |
| movilización de vacías | compra | 10 | -1,1 % [-2,2 %, -0,6 %] | -1,1 % [-2,2 %, -0,6 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -3,0 % [-6,8 %, -1,3 %] | -3,0 % [-6,8 %, -1,3 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,6 % [-1,3 %, -0,3 %] | -0,6 % [-1,3 %, -0,3 %] | sí |
| regulación local de turísticos | alquiler | 10 | -1,0 % [-2,2 %, -0,3 %] | -1,0 % [-2,2 %, -0,3 %] | sí |
| regulación local de turísticos | compra | 10 | -0,2 % [-0,4 %, -0,1 %] | -0,2 % [-0,4 %, -0,1 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,4 % [+1,9 %, +8,3 %] | -5,4 % [-9,4 %, -2,5 %] | no |
| ayudas a la demanda | compra | 10 | +4,4 % [+1,9 %, +8,3 %] | -5,4 % [-9,4 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,1 % [+0,4 %, +2,1 %] | -1,2 % [-2,3 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |
| rebaja de impuestos y costes de construcción | compra | 10 | -1,0 % [-2,0 %, -0,4 %] | -1,0 % [-2,0 %, -0,4 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); vivienda pública o asequible (precio); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 104.105 | -1,1 % | no estimable | -0,11 pp [-0,20, -0,07] | — | — |
| movilización de vacías | alquiler | 104.105 | -3,2 % | no estimable | -0,31 pp [-0,61, -0,17] | — | — |
| vivienda pública o asequible | compra | 52.944 | -0,6 % | no estimable | -0,11 pp [-0,20, -0,07] | — | — |
| vivienda pública o asequible | alquiler | 52.944 | -3,0 % | no estimable | -0,56 pp [-1,03, -0,37] | — | — |
| regulación local de turísticos | compra | 15.773 | -0,2 % | no estimable | -0,11 pp [-0,20, -0,07] | — | — |
| regulación local de turísticos | alquiler | 15.773 | -1,0 % | no estimable | -0,62 pp [-1,15, -0,41] | — | — |
| construcción adicional | compra | 0 | +0,0 % | no estimable | — | — | — |
| construcción adicional | alquiler | 0 | +0,0 % | no estimable | — | — | — |
| rebaja de impuestos y costes de construcción | compra | 27.454 | -1,0 % | 98 [52, 161] | — | -1,11 pp [-1,62, -0,58] | 90 [62, 173] |
| rebaja de impuestos y costes de construcción | alquiler | 27.454 | -1,0 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 142.848 | +4,4 % | 2.405 [1.318, 3.441] | — | +0,19 pp [+0,10, +0,29] | 431 [312, 717] |
| ayudas a la demanda | alquiler | 142.848 | +4,4 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 142.848 | +1,1 % | 596 [272, 917] | — | +0,19 pp [+0,10, +0,29] | 460 [319, 845] |

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
