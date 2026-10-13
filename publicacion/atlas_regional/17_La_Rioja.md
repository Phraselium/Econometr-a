<!-- Generado por `make publicacion` desde output/v7_1/atlas/17_La_Rioja.md. No editar a mano: se regenera y un test lo comprueba. -->

# Atlas regional: La Rioja (17)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 59,45 | 2019Q4 | 69,86 | +17,5 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 70,21 | 2022Q2 | 78,13 | +11,3 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,86 | 2026Q2 | 113,31 | +41,9 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 93,74 | 2019Q4 | 91,69 | -2,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 92,15 | 2022Q2 | 94,57 | +2,6 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 95,15 | 2026Q2 | 102,76 | +8,0 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.678 -0.099\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.149\,\text{ln\_ocupados}_{t-1} + 3.708\,\text{ln\_pob\_total}_{t-1}]) +0.015\,\text{d\_ln\_ocupados\_L0} -0.697\,\text{d\_ln\_pob\_total\_L0} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.099; semivida = 6.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.149, ln_pob_total = 3.708.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0155 | 0.0152 | 1.02 | 0.312 | 0.706 | [-0.0149, 0.0459] |
| d_ln_pob_total_L0 | -0.6975 | 0.3594 | -1.94 | 0.057 | 0.396 | [-1.4153, 0.0204] |
| d_ln_hip_importe | 0.0016 | 0.0011 | 1.44 | 0.154 | 0.523 | [-0.0006, 0.0038] |

Diagnosticos: BG_p = 0.049; BP_p = 0.109; JB_p = 0.000; RESET_p = 0.728; CUSUM_stat = 0.366; CUSUM_p = 0.999; VIF_max = 1.089; r2_adj = 0.260; phi_mitad1 = -0.079; phi_mitad2 = -0.055; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.014\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.015\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.105\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.014; semivida = 50.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.015.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0001 | 0.0002 | 0.62 | 0.537 | 0.731 | [-0.0003, 0.0006] |
| d_y_L1 | 0.1053 | 0.1182 | 0.89 | 0.376 | 0.685 | [-0.1304, 0.3410] |
| d_ln_hip_importe | 0.0018 | 0.0013 | 1.44 | 0.153 | 0.434 | [-0.0007, 0.0043] |

Diagnosticos: BG_p = 0.404; BP_p = 0.649; JB_p = 0.000; RESET_p = 0.653; CUSUM_stat = 0.558; CUSUM_p = 0.915; VIF_max = 1.000; r2_adj = 0.062; phi_mitad1 = 0.004; phi_mitad2 = -0.148; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,099 | 6,6 |
| B | -0,014 | 50,3 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +1.706 -0.179\,(\text{ln\_ipv}_{t-1} - [-0.361\,\text{ln\_ocupados}_{t-1} + 0.086\,\text{ln\_hip\_importe}_{t-1} + 5.646\,\text{ln\_pob\_total}_{t-1}]) +0.094\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +3.661\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.179; semivida = 3.5 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.361, ln_hip_importe = 0.086, ln_pob_total = 5.646.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | 0.0942 | 0.0712 | 1.32 | 0.190 | 0.480 | [-0.0481, 0.2365] |
| d_ln_hip_importe_L0 | 0.0029 | 0.0078 | 0.38 | 0.709 | 0.900 | [-0.0126, 0.0185] |
| d_ln_pob_total_L0 | 3.6609 | 1.8590 | 1.97 | 0.053 | 0.265 | [-0.0541, 7.3759] |
| d_ln_compraventas | -0.0021 | 0.0070 | -0.30 | 0.761 | 0.900 | [-0.0161, 0.0118] |

Diagnosticos: BG_p = 0.565; BP_p = 0.001; JB_p = 0.987; RESET_p = 0.524; CUSUM_stat = 0.650; CUSUM_p = 0.792; VIF_max = 1.842; r2_adj = 0.107; phi_mitad1 = -0.379; phi_mitad2 = -0.453; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.028 -0.066\,(\text{ln\_ipv}_{t-1} - [0.024\,\text{tasa\_paro\_epa}_{t-1} + 0.185\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.001\,\text{d\_ln\_hip\_importe\_L0} +0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.066; semivida = 10.1 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.024, ln_hip_importe = 0.185.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0010 | 0.39 | 0.696 | 0.894 | [-0.0016, 0.0024] |
| d_ln_hip_importe_L0 | 0.0015 | 0.0075 | 0.20 | 0.844 | 0.915 | [-0.0134, 0.0164] |
| d_ln_compraventas | 0.0013 | 0.0070 | 0.19 | 0.851 | 0.915 | [-0.0127, 0.0153] |

Diagnosticos: BG_p = 0.171; BP_p = 0.011; JB_p = 0.866; RESET_p = 0.909; CUSUM_stat = 0.868; CUSUM_p = 0.438; VIF_max = 1.352; r2_adj = 0.031; phi_mitad1 = -0.052; phi_mitad2 = -0.239; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,179 | 3,5 |
| B | -0,066 | 10,1 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,049 | 0,109 | 0,000 | 0,728 | 0,999 | 1,09 | 0,26 | -0,079 | -0,055 | False |
| alquiler | B | 0,404 | 0,649 | 0,000 | 0,653 | 0,915 | 1,00 | 0,06 | 0,004 | -0,148 | True |
| compra | A | 0,565 | 0,001 | 0,987 | 0,524 | 0,792 | 1,84 | 0,11 | -0,379 | -0,453 | False |
| compra | B | 0,171 | 0,011 | 0,866 | 0,909 | 0,438 | 1,35 | 0,03 | -0,052 | -0,239 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | -0,0421 | [-0,0417; -0,0383] | sí |
| alquiler | 2020T1-2022T2 | 0,0015 | [0,0014; 0,0032] | sí |
| alquiler | 2022T3-ultimo | -0,0089 | [-0,0080; -0,0032] | no |
| compra | 2014T1-2019T4 | -0,0360 | [-0,0505; 0,0134] | sí |
| compra | 2020T1-2022T2 | -0,0107 | [-0,1417; -0,0040] | sí |
| compra | 2022T3-ultimo | 0,0129 | [-0,0042; 0,0637] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_17.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,417 | 0,655 | sí | 0,399 | no |
| compra | ar4 | 3,200 | 5,128 | sí | 2,489 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -1,9 % [-4,1 %, -0,8 %] | -1,9 % [-4,1 %, -0,8 %] | sí |
| construcción adicional (dosis v7.2) | compra | 10 | -1,7 % [-3,3 %, -1,0 %] | -1,7 % [-3,3 %, -1,0 %] | sí |
| movilización de vacías | alquiler | 10 | -3,0 % [-6,6 %, -1,5 %] | -3,0 % [-6,6 %, -1,5 %] | sí |
| movilización de vacías | compra | 10 | -1,1 % [-2,1 %, -0,6 %] | -1,1 % [-2,1 %, -0,6 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -2,6 % [-5,8 %, -1,1 %] | -2,6 % [-5,8 %, -1,1 %] | sí |
| vivienda pública o asequible | compra | 10 | -0,5 % [-1,1 %, -0,2 %] | -0,5 % [-1,1 %, -0,2 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,6 % [-1,4 %, -0,2 %] | -0,6 % [-1,4 %, -0,2 %] | sí |
| regulación local de turísticos | compra | 10 | -0,1 % [-0,2 %, -0,0 %] | -0,1 % [-0,2 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,2 % [+1,9 %, +8,1 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| ayudas a la demanda | compra | 10 | +4,2 % [+1,9 %, +8,1 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (alquiler); construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler); vivienda pública o asequible (compra); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (no difundible) (alquiler); rebaja de impuestos y costes de construcción (no difundible) (compra) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 4.538 | -1,1 % | no estimable | -2,35 pp [-4,52, -1,62] | — | — |
| movilización de vacías | alquiler | 4.538 | -3,0 % | no estimable | -6,80 pp [-13,96, -3,71] | — | — |
| vivienda pública o asequible | compra | 2.106 | -0,5 % | no estimable | -2,35 pp [-4,52, -1,62] | — | — |
| vivienda pública o asequible | alquiler | 2.106 | -2,6 % | no estimable | -12,22 pp [-23,37, -7,99] | — | — |
| regulación local de turísticos | compra | 459 | -0,1 % | no estimable | -2,35 pp [-4,52, -1,62] | — | — |
| regulación local de turísticos | alquiler | 459 | -0,6 % | no estimable | -13,58 pp [-25,83, -9,08] | — | — |
| construcción adicional | compra | 7.040 | -1,7 % | no estimable | -2,35 pp [-4,52, -1,62] | — | — |
| construcción adicional | alquiler | 7.040 | -1,9 % | no estimable | -2,74 pp [-5,75, -1,31] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 1.405 | -1,1 % | 4 [2, 6] | — | -29,86 pp [-42,68, -16,07] | 3 [2, 6] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 1.405 | -1,1 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 5.527 | +4,2 % | 68 [38, 99] | — | +6,62 pp [+3,38, +10,19] | 12 [9, 20] |
| ayudas a la demanda | alquiler | 5.527 | +4,2 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 5.527 | +1,1 % | 17 [8, 26] | — | +6,62 pp [+3,38, +10,19] | 13 [9, 23] |

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
