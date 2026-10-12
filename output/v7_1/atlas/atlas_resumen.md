# Atlas regional: comparación entre regiones

*Capa C4; informativo, muestra ya vista en v1; asociación, sin lectura causal. Datos hasta 2026Q2 (panel v7).*

## 1. Largo plazo: ninguna hipótesis confirmada

| id | mercado | variable | MG | PMG | CS-DL | rango entre estimadores | veredicto |
|---|---|---|---|---|---|---|---|
| H7-A1 | alquiler | ln_ocupados | 0,088 | 0,027 | 0,003 | [0,003; 0,088] | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A2 | alquiler | ln_pob_total | 0,894 | 0,844 | 0,177 | [0,177; 0,894] | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A3 | alquiler | tasa_paro_epa | -0,004 | 0,004 | 0,000 | [-0,004; 0,004] | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |
| H7-C1 | compra | ln_ocupados | -0,460 | -0,246 | -0,062 | [-0,460; -0,062] | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C2 | compra | ln_hip_importe | 0,304 | -0,032 | -0,007 | [-0,032; 0,304] | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |
| H7-C3 | compra | ln_pob_total | -1,957 | -1,280 | 3,608 | [-1,957; 3,608] | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |
| H7-C4 | compra | tasa_paro_epa | -0,015 | -0,018 | 0,006 | [-0,018; 0,006] | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |

Las 7 hipótesis quedan sin confirmar (p de Holm ≥ 0,05) y en varias los estimadores discrepan en el signo; se dan ambos. No se identifica un largo plazo estable ni común (V15).

## 2. Velocidades de ajuste (sin inferencia válida)

| CCAA | φ alquiler A | semivida | φ compra A | semivida |
|---|---|---|---|---|
| Andalucía | 0,017 | NA | -0,008 | 83,1 |
| Aragón | -0,104 | 6,3 | -0,211 | 2,9 |
| Asturias | 0,022 | NA | -0,235 | 2,6 |
| Illes Balears | -0,087 | 7,6 | -0,012 | 58,5 |
| Canarias | -0,140 | 4,6 | -0,318 | 1,8 |
| Cantabria | -0,099 | 6,6 | -0,090 | 7,4 |
| Castilla y León | -0,007 | 102,6 | -0,368 | 1,5 |
| Castilla-La Mancha | -0,132 | 4,9 | -0,045 | 15,2 |
| Cataluña | 0,009 | NA | -0,111 | 5,9 |
| Comunitat Valenciana | -0,147 | 4,4 | -0,188 | 3,3 |
| Extremadura | -0,044 | 15,4 | -0,156 | 4,1 |
| Galicia | 0,014 | NA | -0,219 | 2,8 |
| Comunidad de Madrid | 0,053 | NA | -0,080 | 8,3 |
| Región de Murcia | -0,041 | 16,4 | -0,068 | 9,9 |
| Comunidad Foral de Navarra | -0,032 | 21,0 | -0,271 | 2,2 |
| País Vasco | 0,005 | NA | -0,272 | 2,2 |
| La Rioja | -0,099 | 6,6 | -0,179 | 3,5 |

Semivida en trimestres; NA si φ ≥ 0. Solo la comparación del promedio con el valor crítico simulado es válida, y no es significativa.

## 3. Corto plazo heterogéneo y residuo

- alquiler: 9 de 102 coeficientes de corto plazo región × spec × variable con q BH < 0,10 (el resto sin señal).
- compra: 8 de 119 coeficientes de corto plazo región × spec × variable con q BH < 0,10 (el resto sin señal).

Rango del residuo no explicado entre estimadores, 2022T3-último, especificación A:

Variación **relativa a la media de las 17 CCAA** (datos con demeaning transversal; log). No es la subida absoluta, que está en cada ficha (sección 1).

| CCAA | mercado | variación relativa a la media | residuo mín. | residuo máx. |
|---|---|---|---|---|
| Andalucía | alquiler | 0,011 | 0,012 | 0,017 |
| Andalucía | compra | 0,038 | 0,012 | 0,068 |
| Aragón | alquiler | 0,003 | 0,004 | 0,005 |
| Aragón | compra | 0,023 | 0,017 | 0,040 |
| Asturias | alquiler | -0,010 | -0,008 | 0,001 |
| Asturias | compra | -0,002 | -0,024 | 0,057 |
| Illes Balears | alquiler | 0,013 | -0,002 | 0,010 |
| Illes Balears | compra | -0,022 | -0,108 | -0,023 |
| Canarias | alquiler | 0,006 | -0,004 | 0,005 |
| Canarias | compra | 0,021 | 0,006 | 0,049 |
| Cantabria | alquiler | -0,001 | 0,001 | 0,011 |
| Cantabria | compra | 0,007 | -0,051 | 0,052 |
| Castilla y León | alquiler | -0,007 | -0,004 | 0,008 |
| Castilla y León | compra | -0,007 | -0,063 | 0,046 |
| Castilla-La Mancha | alquiler | 0,006 | 0,003 | 0,006 |
| Castilla-La Mancha | compra | -0,048 | -0,064 | -0,044 |
| Cataluña | alquiler | -0,012 | -0,029 | -0,015 |
| Cataluña | compra | -0,007 | -0,065 | 0,069 |
| Comunitat Valenciana | alquiler | 0,021 | -0,008 | 0,016 |
| Comunitat Valenciana | compra | 0,005 | -0,102 | 0,055 |
| Extremadura | alquiler | 0,003 | 0,008 | 0,032 |
| Extremadura | compra | -0,039 | -0,093 | 0,057 |
| Galicia | alquiler | -0,002 | 0,001 | 0,014 |
| Galicia | compra | -0,017 | -0,068 | 0,047 |
| Comunidad de Madrid | alquiler | 0,013 | -0,012 | 0,009 |
| Comunidad de Madrid | compra | -0,000 | -0,084 | 0,110 |
| Región de Murcia | alquiler | -0,019 | -0,025 | -0,020 |
| Región de Murcia | compra | -0,012 | -0,057 | 0,000 |
| Comunidad Foral de Navarra | alquiler | -0,006 | -0,008 | -0,006 |
| Comunidad Foral de Navarra | compra | 0,039 | 0,036 | 0,055 |
| País Vasco | alquiler | -0,011 | -0,009 | -0,002 |
| País Vasco | compra | 0,008 | -0,008 | 0,042 |
| La Rioja | alquiler | -0,009 | -0,008 | -0,003 |
| La Rioja | compra | 0,013 | -0,004 | 0,064 |

## 4. Backtest (R5; selección en muestra, optimista)

- alquiler: el mejor modelo bate a la base fuerte en 12 de 17 CCAA y a la base más exigente en 6 de 17 (Canarias, Castilla y León, Comunitat Valenciana, Comunidad de Madrid, Comunidad Foral de Navarra, País Vasco). PMG no la bate en ningún mercado.
- compra: el mejor modelo bate a la base fuerte en 17 de 17 CCAA y a la base más exigente en 5 de 17 (Illes Balears, Castilla-La Mancha, Cataluña, Comunitat Valenciana, Comunidad de Madrid). PMG no la bate en ningún mercado.

## 5. Recomendaciones robustas por región (condicional, C4)

Robusto: esfuerzo a la baja en todo el Monte Carlo y precio de mercado sin subida en ninguna extracción (V18). Se evalúan instrumentos, no actores. «Rejilla» indica que la elasticidad regional no fue utilizable.

| CCAA | alquiler | compra |
|---|---|---|
| Andalucía | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Aragón | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Asturias | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción |
| Illes Balears | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible |
| Canarias | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Cantabria | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción |
| Castilla y León | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción |
| Castilla-La Mancha | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Cataluña | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Comunitat Valenciana | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Extremadura | movilización de vacías, vivienda pública o asequible | movilización de vacías |
| Galicia | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción |
| Comunidad de Madrid | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | construcción adicional, movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Región de Murcia | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| Comunidad Foral de Navarra | construcción adicional, movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible | construcción adicional, movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |
| País Vasco | construcción adicional, movilización de vacías, vivienda pública o asequible | construcción adicional, movilización de vacías, vivienda pública o asequible |
| La Rioja | movilización de vacías, rebaja de impuestos y costes de construcción, regulación local de turísticos, vivienda pública o asequible | movilización de vacías, rebaja de impuestos y costes de construcción, vivienda pública o asequible |

## English summary (about 150 words)

This atlas compares 17 Spanish regions using quarterly panel data to 2026Q2. It is informative only: the sample was already seen in v1, and every result sits in layer C4 (exploratory, association, no causal reading). None of the seven long-run hypotheses on prices and rents was confirmed (Holm-adjusted p above 0.05), and the three estimators often disagree, so ranges are reported. Speeds of adjustment differ across regions but carry no valid individual inference. Short-run movements are heterogeneous and the unexplained residual dominates the historical accounting. In the backtest, the best model beats the most demanding baseline in 6 of 17 regions for rents and 5 of 17 for purchases; selection is in-sample, so this is optimistic. Policy scenarios are conditional (if X were done, under stated assumptions) and evaluate instruments, not actors. Deferred validation on new data remains pending.


## Dosis y coste de las propuestas (v7.1; condicional, C4)

Mediana entre CCAA y rango entre CCAA
| Instrumento | Mercado | Dosis (mediana CCAA) | Δ precio de mercado (%) | Coste anual (M€) | Efecto por 10.000 viv. (pp) | Efecto por 100 M€/año en precio de mercado (pp) | Coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| construcción adicional | compra | 0 | 0,00 [-1,38; 0,00] | no estimable | -0,785 [-1,507; -0,127] | — | — |
| construcción adicional | alquiler | 0 | 0,00 [-1,52; 0,00] | no estimable | -0,907 [-1,704; -0,146] | — | — |
| movilización de vacías | compra | 23.336 | -1,34 [-2,98; -0,57] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| movilización de vacías | alquiler | 23.336 | -3,78 [-8,37; -1,63] | no estimable | -1,748 [-6,804; -0,306] | — | — |
| vivienda pública o asequible | compra | 9.629 | -0,57 [-1,01; -0,13] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| vivienda pública o asequible | alquiler | 9.629 | -2,96 [-5,28; -0,64] | no estimable | -3,169 [-12,218; -0,560] | — | — |
| regulación local de turísticos | compra | 2.125 | -0,09 [-0,53; -0,03] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| regulación local de turísticos | alquiler | 2.125 | -0,50 [-3,05; -0,18] | no estimable | -3,524 [-13,579; -0,620] | — | — |
| ayudas a la demanda | compra | 26.678 | 4,37 [4,14; 8,09] | 378 [68; 2915] | — | 1,364 [0,158; 7,603] | 76 [12; 516] |
| ayudas a la demanda | alquiler | 26.678 | 4,37 [4,14; 8,09] | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 26.678 | 1,07 [1,01; 1,99] | 93 [17; 718] | — | 1,364 [0,158; 7,603] | 82 [13; 550] |
| rebaja de impuestos y costes de construcción | compra | 4.308 | -1,04 [-1,08; -0,29] | 15 [4; 135] | — | -6,542 [-29,859; -0,823] | 15 [3; 121] |
| rebaja de impuestos y costes de construcción | alquiler | 4.308 | -1,04 [-1,08; -0,29] | (el de compra) | — | — | — |

Rango entre corchetes: mínimo y máximo de las medianas de las 17 CCAA. El rango p5-p95 de cada CCAA está en dosis_coste.csv.

Definiciones y motivos de «no estimable»: output/v7_1/S1/resumen.md. Ficha por CCAA: sección 6 bis.

### Lectura

- Los instrumentos de cantidad no tienen coste fiscal estimable con base versionada: se comparan por su dosis y su efecto por 10.000 viviendas, no por euro.
- En compra, el efecto por 10.000 viviendas es el MISMO para vacías, vivienda pública y turísticos en cada CCAA (la fórmula solo depende del parque y de las elasticidades). Lo que los distingue es la dosis y, en alquiler, la fracción que llega al alquiler. Del mismo modo, el efecto por 100 M€ en el precio de mercado es idéntico para las ayudas a la demanda y la rebaja de ITP/IVA: ambos son una intensidad s sobre el mismo valor de compras. Son propiedades de la fórmula, no hallazgos.
- Las ayudas a la demanda y la rebaja de ITP/IVA reducen el precio neto del beneficiario, pero suben el precio de mercado para el resto. Su coste por punto es de reducción del precio neto, no del precio de mercado.
- La rebaja de impuestos y costes de construcción es el único instrumento con coste estimado que baja el precio de mercado. Pero su efecto por 100 M€ está sobrestimado por construcción: R6 traslada la rebaja al precio de todo el mercado, mientras que el coste fiscal solo cubre la obra nueva (visados 2025). No debe leerse como «el instrumento más eficiente por euro».
- La construcción adicional tiene dosis mediana 0: en la mayoría de las CCAA los visados de 2025 ya igualan o superan el máximo de 2016-2025 (el escenario de R6 solo añade el hueco).
- Todo es C4: los parámetros son supuestos de la rejilla. No se recomienda ningún instrumento; se comparan magnitudes condicionales.
