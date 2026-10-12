<!-- Generado por `make publicacion` desde output/v7_1/atlas/03_Asturias.md. No editar a mano: se regenera y un test lo comprueba. -->

# Atlas regional: Asturias (03)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 60,69 | 2019Q4 | 70,07 | +15,5 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 70,43 | 2022Q2 | 79,10 | +12,3 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 79,58 | 2026Q2 | 114,01 | +43,3 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 91,29 | 2019Q4 | 93,31 | +2,2 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 93,36 | 2022Q2 | 94,87 | +1,6 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 95,30 | 2026Q2 | 102,74 | +7,8 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.020 +0.022\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.610\,\text{ln\_ocupados}_{t-1} + -2.081\,\text{ln\_pob\_total}_{t-1}]) -0.007\,\text{d\_ln\_ocupados\_L0} +1.114\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.022; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.610, ln_pob_total = -2.081.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0067 | 0.0142 | -0.47 | 0.638 | 0.867 | [-0.0352, 0.0217] |
| d_ln_pob_total_L0 | 1.1137 | 0.4216 | 2.64 | 0.010 | 0.274 | [0.2717, 1.9557] |
| d_ln_hip_importe | -0.0019 | 0.0014 | -1.35 | 0.183 | 0.583 | [-0.0048, 0.0009] |

Diagnosticos: BG_p = 0.633; BP_p = 0.017; JB_p = 0.000; RESET_p = 0.908; CUSUM_stat = 0.515; CUSUM_p = 0.953; VIF_max = 1.109; r2_adj = 0.164; phi_mitad1 = 0.067; phi_mitad2 = -0.132; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.000 -0.013\,(\text{ln\_ipc\_alquiler}_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.172\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.013; semivida = 51.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.016.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0001 | 0.0002 | -0.48 | 0.633 | 0.751 | [-0.0005, 0.0003] |
| d_y_L1 | 0.1717 | 0.1114 | 1.54 | 0.128 | 0.384 | [-0.0505, 0.3939] |
| d_ln_hip_importe | -0.0022 | 0.0014 | -1.55 | 0.125 | 0.384 | [-0.0050, 0.0006] |

Diagnosticos: BG_p = 0.149; BP_p = 0.068; JB_p = 0.281; RESET_p = 0.866; CUSUM_stat = 0.822; CUSUM_p = 0.508; VIF_max = 1.000; r2_adj = 0.080; phi_mitad1 = 0.021; phi_mitad2 = -0.083; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,022 | NA |
| B | -0,013 | 51,4 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.170 -0.235\,(\text{ln\_ipv}_{t-1} - [-0.135\,\text{ln\_ocupados}_{t-1} + 0.115\,\text{ln\_hip\_importe}_{t-1} + 1.135\,\text{ln\_pob\_total}_{t-1}]) -0.074\,\text{d\_ln\_ocupados\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} +5.166\,\text{d\_ln\_pob\_total\_L0} -0.001\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.235; semivida = 2.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.135, ln_hip_importe = 0.115, ln_pob_total = 1.135.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0738 | 0.0662 | -1.12 | 0.269 | 0.600 | [-0.2060, 0.0584] |
| d_ln_hip_importe_L0 | 0.0225 | 0.0092 | 2.45 | 0.017 | 0.123 | [0.0042, 0.0408] |
| d_ln_pob_total_L0 | 5.1657 | 2.7942 | 1.85 | 0.069 | 0.292 | [-0.4181, 10.7495] |
| d_ln_compraventas | -0.0009 | 0.0109 | -0.08 | 0.934 | 0.982 | [-0.0227, 0.0209] |

Diagnosticos: BG_p = 0.120; BP_p = 0.426; JB_p = 0.541; RESET_p = 0.260; CUSUM_stat = 0.345; CUSUM_p = 1.000; VIF_max = 3.697; r2_adj = 0.201; phi_mitad1 = -0.217; phi_mitad2 = -0.284; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = +0.017 -0.079\,(\text{ln\_ipv}_{t-1} - [-0.015\,\text{tasa\_paro\_epa}_{t-1} + 0.251\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.002\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.079; semivida = 8.4 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = -0.015, ln_hip_importe = 0.251.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | -0.0009 | 0.0010 | -0.98 | 0.330 | 0.672 | [-0.0029, 0.0010] |
| d_ln_hip_importe_L0 | 0.0224 | 0.0090 | 2.49 | 0.015 | 0.156 | [0.0044, 0.0403] |
| d_ln_compraventas | -0.0021 | 0.0117 | -0.18 | 0.861 | 0.915 | [-0.0253, 0.0212] |

Diagnosticos: BG_p = 0.631; BP_p = 0.139; JB_p = 0.903; RESET_p = 0.411; CUSUM_stat = 1.193; CUSUM_p = 0.116; VIF_max = 2.725; r2_adj = 0.059; phi_mitad1 = -0.205; phi_mitad2 = -0.412; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,235 | 2,6 |
| B | -0,079 | 8,4 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,633 | 0,017 | 0,000 | 0,908 | 0,953 | 1,11 | 0,16 | 0,067 | -0,132 | True |
| alquiler | B | 0,149 | 0,068 | 0,281 | 0,866 | 0,508 | 1,00 | 0,08 | 0,021 | -0,083 | True |
| compra | A | 0,120 | 0,426 | 0,541 | 0,260 | 1,000 | 3,70 | 0,20 | -0,217 | -0,284 | False |
| compra | B | 0,631 | 0,139 | 0,903 | 0,411 | 0,116 | 2,73 | 0,06 | -0,205 | -0,412 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0063 | [0,0149; 0,0567] | sí |
| alquiler | 2020T1-2022T2 | -0,0033 | [0,0004; 0,0214] | sí |
| alquiler | 2022T3-ultimo | -0,0103 | [-0,0078; 0,0007] | no |
| compra | 2014T1-2019T4 | -0,0636 | [-0,1581; 0,0984] | sí |
| compra | 2020T1-2022T2 | -0,0043 | [-0,1347; 0,0629] | sí |
| compra | 2022T3-ultimo | -0,0025 | [-0,0244; 0,0570] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_03.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,368 | 0,341 | no | 0,341 | no |
| compra | gbm | 2,594 | 4,299 | sí | 2,319 | no |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional | alquiler | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| construcción adicional | precio | 10 | +0,0 % [-0,0 %, +0,0 %] | +0,0 % [-0,0 %, +0,0 %] | no |
| movilización de vacías | alquiler | 10 | -3,8 % [-8,2 %, -1,9 %] | -3,8 % [-8,2 %, -1,9 %] | sí |
| movilización de vacías | precio | 10 | -1,3 % [-2,6 %, -0,8 %] | -1,3 % [-2,6 %, -0,8 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -0,8 % [-1,8 %, -0,4 %] | -0,8 % [-1,8 %, -0,4 %] | sí |
| vivienda pública o asequible | precio | 10 | -0,2 % [-0,3 %, -0,1 %] | -0,2 % [-0,3 %, -0,1 %] | no |
| regulación local de turísticos | alquiler | 10 | -0,9 % [-2,0 %, -0,3 %] | -0,9 % [-2,0 %, -0,3 %] | sí |
| regulación local de turísticos | precio | 10 | -0,2 % [-0,3 %, -0,1 %] | -0,2 % [-0,3 %, -0,1 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,1 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| ayudas a la demanda | precio | 10 | +4,1 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | precio | 10 | +1,0 % [+0,4 %, +2,1 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción | alquiler | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción | precio | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** movilización de vacías (alquiler); movilización de vacías (precio); vivienda pública o asequible (alquiler); regulación local de turísticos (alquiler); rebaja de impuestos y costes de construcción (alquiler); rebaja de impuestos y costes de construcción (precio) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 18.269 | -1,3 % | no estimable | -0,74 pp [-1,37, -0,51] | — | — |
| movilización de vacías | alquiler | 18.269 | -3,8 % | no estimable | -2,11 pp [-4,16, -1,15] | — | — |
| vivienda pública o asequible | compra | 2.090 | -0,2 % | no estimable | -0,74 pp [-1,37, -0,51] | — | — |
| vivienda pública o asequible | alquiler | 2.090 | -0,8 % | no estimable | -3,81 pp [-7,25, -2,52] | — | — |
| regulación local de turísticos | compra | 2.125 | -0,2 % | no estimable | -0,74 pp [-1,37, -0,51] | — | — |
| regulación local de turísticos | alquiler | 2.125 | -0,9 % | no estimable | -4,25 pp [-7,99, -2,82] | — | — |
| construcción adicional | compra | 0 | +0,0 % | no estimable | — | — | — |
| construcción adicional | alquiler | 0 | +0,0 % | no estimable | — | — | — |
| rebaja de impuestos y costes de construcción | compra | 3.096 | -1,1 % | 10 [5, 16] | — | -11,25 pp [-16,00, -5,87] | 9 [6, 17] |
| rebaja de impuestos y costes de construcción | alquiler | 3.096 | -1,1 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 15.638 | +4,1 % | 233 [129, 341] | — | +1,89 pp [+0,96, +2,97] | 41 [31, 69] |
| ayudas a la demanda | alquiler | 15.638 | +4,1 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 15.638 | +1,0 % | 58 [27, 90] | — | +1,89 pp [+0,96, +2,97] | 44 [31, 82] |

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
