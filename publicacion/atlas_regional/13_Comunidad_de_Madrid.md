<!-- Generado por `make publicacion` desde output/v7_1/atlas/13_Comunidad_de_Madrid.md. No editar a mano: se regenera y un test lo comprueba. -->

# Atlas regional: Comunidad de Madrid (13)

*Capa C4 (fuente única INE a nivel de CCAA; informativo, muestra ya vista en v1). Asociación, sin lectura causal. Datos hasta 2026Q2; panel_ccaa_q_v7.*

## 1. Qué subió y cuánto

| serie | periodo | inicio | valor inicio | fin | valor fin | variación |
|---|---|---|---|---|---|---|
| IPV (INE) | 2014T1-2019T4 | 2014Q1 | 46,90 | 2019Q4 | 70,42 | +50,2 % |
| IPV (INE) | 2020T1-2022T2 | 2020Q1 | 72,18 | 2022Q2 | 78,44 | +8,7 % |
| IPV (INE) | 2022T3-último | 2022Q3 | 80,23 | 2026Q2 | 111,85 | +39,4 % |
| IPC alquiler (INE) | 2014T1-2019T4 | 2014Q1 | 88,16 | 2019Q4 | 90,65 | +2,8 % |
| IPC alquiler (INE) | 2020T1-2022T2 | 2020Q1 | 91,02 | 2022Q2 | 92,38 | +1,5 % |
| IPC alquiler (INE) | 2022T3-último | 2022Q3 | 92,74 | 2026Q2 | 102,55 | +10,6 % |

Variación = valor fin / valor inicio − 1, sobre el índice trimestral de cada fecha. El IPC de alquiler mide el stock de contratos; no es el alquiler de contratos nuevos.

## 2. Ecuación y tabla de cada modelo (ECM regional)

Los coeficientes de corto plazo tienen inferencia con control BH (q = 0,10). La velocidad de ajuste (φ), la semivida y θ se muestran como estimaciones **sin inferencia válida**: R4 no confirmó ninguna de las 7 hipótesis de largo plazo.

### Mercado: alquiler

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.023 +0.053\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.953\,\text{ln\_ocupados}_{t-1} + -0.696\,\text{ln\_pob\_total}_{t-1}]) -0.008\,\text{d\_ln\_ocupados\_L0} +0.780\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = 0.053; semivida = NA trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = 0.953, ln_pob_total = -0.696.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0077 | 0.0153 | -0.51 | 0.614 | 0.867 | [-0.0382, 0.0228] |
| d_ln_pob_total_L0 | 0.7799 | 0.3192 | 2.44 | 0.017 | 0.274 | [0.1424, 1.4174] |
| d_ln_hip_importe | 0.0011 | 0.0020 | 0.55 | 0.581 | 0.867 | [-0.0029, 0.0052] |

Diagnosticos: BG_p = 0.013; BP_p = 0.618; JB_p = 0.819; RESET_p = 0.401; CUSUM_stat = 0.701; CUSUM_p = 0.709; VIF_max = 2.046; r2_adj = 0.345; phi_mitad1 = 0.035; phi_mitad2 = -0.060; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

#### Especificacion B (N de la region = 76 observaciones; periodo 2007Q1-2026Q2; ARDL(2,1))

$$\Delta\text{ln\_ipc\_alquiler}_t = +0.002 -0.016\,(\text{ln\_ipc\_alquiler}_{t-1} - [0.042\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.460\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$$

Velocidad de ajuste estimada phi_i = -0.016; semivida = 43.2 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.042.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0004 | 0.0002 | 1.66 | 0.102 | 0.348 | [-0.0001, 0.0008] |
| d_y_L1 | 0.4601 | 0.1003 | 4.59 | 0.000 | 0.000 | [0.2602, 0.6601] |
| d_ln_hip_importe | 0.0017 | 0.0016 | 1.08 | 0.285 | 0.582 | [-0.0015, 0.0050] |

Diagnosticos: BG_p = 0.913; BP_p = 0.526; JB_p = 0.840; RESET_p = 0.388; CUSUM_stat = 0.485; CUSUM_p = 0.973; VIF_max = 1.000; r2_adj = 0.523; phi_mitad1 = 0.020; phi_mitad2 = -0.050; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: True.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | 0,053 | NA |
| B | -0,016 | 43,2 |

### Mercado: compra

#### Especificacion A (N de la region = 72 observaciones; periodo 2007Q1-2025Q1; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.131 -0.080\,(\text{ln\_ipv}_{t-1} - [-0.755\,\text{ln\_ocupados}_{t-1} + 0.469\,\text{ln\_hip\_importe}_{t-1} + 1.350\,\text{ln\_pob\_total}_{t-1}]) -0.078\,\text{d\_ln\_ocupados\_L0} +0.041\,\text{d\_ln\_hip\_importe\_L0} +1.261\,\text{d\_ln\_pob\_total\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.080; semivida = 8.3 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): ln_ocupados = -0.755, ln_hip_importe = 0.469, ln_pob_total = 1.350.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_ln_ocupados_L0 | -0.0782 | 0.1051 | -0.74 | 0.460 | 0.782 | [-0.2882, 0.1319] |
| d_ln_hip_importe_L0 | 0.0405 | 0.0153 | 2.66 | 0.010 | 0.113 | [0.0101, 0.0710] |
| d_ln_pob_total_L0 | 1.2609 | 2.0098 | 0.63 | 0.533 | 0.860 | [-2.7554, 5.2772] |
| d_ln_compraventas | 0.0350 | 0.0179 | 1.95 | 0.055 | 0.265 | [-0.0008, 0.0708] |

Diagnosticos: BG_p = 0.912; BP_p = 0.085; JB_p = 0.748; RESET_p = 0.126; CUSUM_stat = 0.514; CUSUM_p = 0.954; VIF_max = 12.790; r2_adj = 0.345; phi_mitad1 = -0.071; phi_mitad2 = -0.212; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

#### Especificacion B (N de la region = 77 observaciones; periodo 2007Q1-2026Q2; ARDL(1,1))

$$\Delta\text{ln\_ipv}_t = -0.084 -0.088\,(\text{ln\_ipv}_{t-1} - [0.039\,\text{tasa\_paro\_epa}_{t-1} + 0.538\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.048\,\text{d\_ln\_hip\_importe\_L0} +0.035\,\text{d\_ln\_compraventas}$$

Velocidad de ajuste estimada phi_i = -0.088; semivida = 7.6 trimestres. **Sin inferencia valida** (no hay IC ni p de phi_i; la comparacion valida es la del promedio con -8,83). theta_i estimado (sin inferencia valida): tasa_paro_epa = 0.039, ln_hip_importe = 0.538.

| coeficiente de corto plazo | estimacion | EE | t | p | q (BH, q=0,10) | IC95 |
|---|---|---|---|---|---|---|
| d_tasa_paro_epa_L0 | 0.0020 | 0.0018 | 1.10 | 0.276 | 0.641 | [-0.0016, 0.0056] |
| d_ln_hip_importe_L0 | 0.0482 | 0.0137 | 3.52 | 0.001 | 0.039 | [0.0209, 0.0756] |
| d_ln_compraventas | 0.0349 | 0.0166 | 2.10 | 0.039 | 0.221 | [0.0018, 0.0680] |

Diagnosticos: BG_p = 0.867; BP_p = 0.073; JB_p = 0.315; RESET_p = 0.020; CUSUM_stat = 0.492; CUSUM_p = 0.969; VIF_max = 5.679; r2_adj = 0.385; phi_mitad1 = -0.185; phi_mitad2 = -0.206; CUSUM rechaza al 5 %: False; cambio de signo de phi entre mitades: False.

| spec | φ (sin inferencia válida) | semivida (trim.) |
|---|---|---|
| A | -0,080 | 8,3 |
| B | -0,088 | 7,6 |

## 3. Diagnósticos

| mercado | spec | Breusch-Godfrey p | Breusch-Pagan p | Jarque-Bera p | RESET p | CUSUM p | VIF máx | R² aj. | φ mitad 1 | φ mitad 2 | cambio de signo de φ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| alquiler | A | 0,013 | 0,618 | 0,819 | 0,401 | 0,709 | 2,05 | 0,34 | 0,035 | -0,060 | True |
| alquiler | B | 0,913 | 0,526 | 0,840 | 0,388 | 0,973 | 1,00 | 0,52 | 0,020 | -0,050 | True |
| compra | A | 0,912 | 0,085 | 0,748 | 0,126 | 0,954 | 12,79 | 0,34 | -0,071 | -0,212 | False |
| compra | B | 0,867 | 0,073 | 0,315 | 0,020 | 0,969 | 5,68 | 0,38 | -0,185 | -0,206 | False |

Un p bajo en Breusch-Godfrey indica autocorrelación residual; en ese caso los errores estándar de la tabla de corto plazo son menos fiables.

## 4. Descomposición por periodo (contabilidad descriptiva, con residuo)

Coeficientes no confirmados: la magnitud se da como rango entre estimadores (MG, PMG, CS-DL) y es asociación. Variación en log. «no atribuible = True»: el residuo domina o el rango abarca la variación.

**Ojo:** la descomposición se hace sobre datos con demeaning transversal, así que la variación es **relativa a la media de las 17 CCAA** (log; positiva si la región subió más que la media). Las subidas absolutas están en la sección 1.

| mercado | periodo | variación relativa a la media de las CCAA (log) | residuo no explicado [rango] | ¿no atribuible? |
|---|---|---|---|---|
| alquiler | 2014T1-2019T4 | 0,0066 | [-0,0335; -0,0008] | sí |
| alquiler | 2020T1-2022T2 | -0,0048 | [-0,0091; -0,0058] | sí |
| alquiler | 2022T3-ultimo | 0,0132 | [-0,0118; 0,0088] | sí |
| compra | 2014T1-2019T4 | 0,2271 | [0,0845; 0,3006] | sí |
| compra | 2020T1-2022T2 | 0,0103 | [-0,0134; 0,0786] | sí |
| compra | 2022T3-ultimo | -0,0001 | [-0,0845; 0,1101] | sí |

Las tablas completas (incluida la descomposición del ECM propio de la región) están en output/v7/R4/<mercado>/region_13.md.

## 5. Backtest (R5)

| mercado | mejor modelo | RMSE ×100 | base fuerte | ¿bate a la base fuerte? | base más exigente | ¿bate a la más exigente? |
|---|---|---|---|---|---|---|
| alquiler | gbm | 0,536 | 0,631 | sí | 0,612 | sí |
| compra | ar4 | 3,060 | 4,891 | sí | 3,281 | sí |

Origen móvil 2016Q1-2026Q1, h = 1-4 agrupados. informativo, muestra ya vista en v1; la selección del mejor modelo es en muestra (optimista). Solo "predice mejor" quien bate a la base más exigente.

## 6. Propuestas (R6; condicional, C4)

«Si se hiciera X, con estos supuestos…». Mediana e intervalo al 90 % (p5-p95) de la variación %, a 10 años (2 y 5 años en output/v7/R6/impactos.csv), con la elasticidad de oferta de la rejilla (v5). Esfuerzo = variación % del esfuerzo neto del beneficiario. Robusto = esfuerzo baja en todo el Monte Carlo y el precio de mercado no sube en ninguna extracción.

| instrumento | mercado | h | precio o alquiler de mercado: mediana [p5, p95] | esfuerzo: mediana [p5, p95] | robusto |
|---|---|---|---|---|---|
| construcción adicional (dosis v7.2) | alquiler | 10 | -0,4 % [-0,8 %, -0,2 %] | -0,4 % [-0,8 %, -0,2 %] | no |
| construcción adicional (dosis v7.2) | compra | 10 | -0,3 % [-0,6 %, -0,2 %] | -0,3 % [-0,6 %, -0,2 %] | sí |
| movilización de vacías | alquiler | 10 | -1,6 % [-3,5 %, -0,8 %] | -1,6 % [-3,5 %, -0,8 %] | sí |
| movilización de vacías | compra | 10 | -0,6 % [-1,1 %, -0,3 %] | -0,6 % [-1,1 %, -0,3 %] | sí |
| vivienda pública o asequible | alquiler | 10 | -5,3 % [-11,5 %, -2,4 %] | -5,3 % [-11,5 %, -2,4 %] | sí |
| vivienda pública o asequible | compra | 10 | -1,0 % [-2,2 %, -0,5 %] | -1,0 % [-2,2 %, -0,5 %] | sí |
| regulación local de turísticos | alquiler | 10 | -0,3 % [-0,6 %, -0,1 %] | -0,3 % [-0,6 %, -0,1 %] | no |
| regulación local de turísticos | compra | 10 | -0,0 % [-0,1 %, -0,0 %] | -0,0 % [-0,1 %, -0,0 %] | no |
| ayudas a la demanda | alquiler | 10 | +4,4 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| ayudas a la demanda | compra | 10 | +4,4 % [+1,8 %, +8,3 %] | -5,4 % [-9,5 %, -2,5 %] | no |
| rebaja de ITP/IVA (vivienda nueva) | compra | 10 | +1,1 % [+0,4 %, +2,2 %] | -1,2 % [-2,4 %, -0,5 %] | no |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 10 | -1,1 % [-2,1 %, -0,5 %] | -1,1 % [-2,1 %, -0,5 %] | sí |

**Combinaciones robustas en esta región:** construcción adicional (compra); movilización de vacías (alquiler); movilización de vacías (compra); vivienda pública o asequible (alquiler); vivienda pública o asequible (compra); rebaja de impuestos y costes de construcción (no difundible) (alquiler); rebaja de impuestos y costes de construcción (no difundible) (compra) (con la rejilla de elasticidades; la elasticidad regional no fue utilizable).

Con la elasticidad regional (DOLS) el resultado puede diferir; esa elasticidad no pasó los diagnósticos en ninguna de las 17 CCAA, de modo que se mantiene la rejilla y se reportan ambas en impactos.csv.

## 6 bis. Dosis y coste de las propuestas (v7.1; condicional, C4)

Misma simulación que la sección 6 (output/v7_1/S1/dosis_coste.csv, que reproduce R6). Dosis acumulada a 10 años (en e, f1 y f2, por año); coste fiscal anual aproximado, sin efectos inducidos; mediana [p5, p95]. El signo lo fija en gran parte la fórmula de incidencia: lo informativo son las magnitudes relativas.

| instrumento | mercado | dosis | precio de mercado | coste anual (M€) | por 10.000 viviendas | por 100 M€ anuales (mercado) | coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| movilización de vacías | compra | 33.823 | -0,6 % | no estimable | -0,17 pp [-0,31, -0,12] | — | — |
| movilización de vacías | alquiler | 33.823 | -1,6 % | no estimable | -0,49 pp [-0,98, -0,27] | — | — |
| vivienda pública o asequible | compra | 59.433 | -1,0 % | no estimable | -0,17 pp [-0,31, -0,12] | — | — |
| vivienda pública o asequible | alquiler | 59.433 | -5,3 % | no estimable | -0,88 pp [-1,59, -0,57] | — | — |
| regulación local de turísticos | compra | 2.707 | -0,0 % | no estimable | -0,17 pp [-0,31, -0,12] | — | — |
| regulación local de turísticos | alquiler | 2.707 | -0,3 % | no estimable | -0,98 pp [-1,77, -0,65] | — | — |
| construcción adicional | compra | 19.427 | -0,3 % | no estimable | -0,17 pp [-0,31, -0,12] | — | — |
| construcción adicional | alquiler | 19.427 | -0,4 % | no estimable | -0,19 pp [-0,39, -0,09] | — | — |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 17.718 | -1,1 % | 135 [69, 221] | — | -0,82 pp [-1,20, -0,43] | 121 [83, 230] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 17.718 | -1,1 % | el de compra | — | — | — |
| ayudas a la demanda | compra | 81.822 | +4,4 % | 2.915 [1.600, 4.159] | — | +0,16 pp [+0,08, +0,24] | 516 [374, 845] |
| ayudas a la demanda | alquiler | 81.822 | +4,4 % | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 81.822 | +1,1 % | 718 [328, 1.109] | — | +0,16 pp [+0,08, +0,24] | 550 [382, 1.004] |

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
