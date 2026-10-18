# V16 · Lo ya visto (V5-V15)

Generado por `python3 src/v16/f0_lo_ya_visto.py` desde output/v5/cifras_clave.csv y output/v15/auditoria/*/resultado.json. Ningún número está tecleado: cada fila lleva su id de cifras_clave.

**Uso.** Todo pre-registro de V16 declara qué de esto ya se ha visto para su pregunta. Lo ya visto es informativo: una pregunta de V16 solo es confirmatoria en datos o diseños que no se hayan usado antes (docs/v16/plan.md, regla A; adenda 2 de V15). Las conclusiones publicadas en la 1.0 no se reescriben: si V16 las contradice, es una parada (sección D).

## V5-V7 · Hechos de partida (hogares, déficit, necesidad, precios y alquiler)

**Lectura.** Hechos C1 o cotas C2 de la 1.0. V16 los actualiza con fuentes nuevas, pero no los reemplaza: un valor distinto en V16 es una cifra V16-* nueva y, si contradice uno publicado, es una parada.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| A23-A10 | Contratos nuevos Comunitat Valenciana 2021-2024: IPVA nuevo y fianzas GVA | 28,5 | 26,1 a 30,8 | 2021-2024 | C1 |
| A23-A2 | Alquiler stock 2015-2024: núcleo IPC de alquiler e IPVA (contratos existentes y total; tolerancia ±15 % en nivel) |  | 10,9 a 22,9 | 2015-2024 | C1 |
| A23-A9 | Contratos nuevos Cataluña 2021-2024: IPVA nuevo e Incasòl | 16,9 | 16,6 a 17,2 | 2021-2024 | C1 |
| A23-P2 | Precio de compra, núcleo MIVAU/Notariado/Registradores 2015-2025 | 47,2 | 44,2 a 56,1 | 2015-2025 (media anual) | C1 |
| L3-DEF-2124-SINBAJAS | Déficit acumulado 2021-2024 sin bajas (todas las variantes de corrección EPA y de terminadas) | 5,5e+05 | 3,894e+05 a 7,105e+05 | 2021-2024 | C2 |
| T3-H5b | Necesidad anual de vivienda 2026-2035, base sin la sensibilidad X (A+R+V+F-M-K; no resta liberadas) | 2,104e+05 | 9,939e+04 a 2,921e+05 | 2026-2035 | C4 |
| dh_2125 | Aumento del número de hogares | 9,976e+05 | 9,818e+05 a 1,013e+06 | 2021-2025 | C1 |
| terminadas_1924 | Viviendas terminadas al año (territorio común: sin País Vasco ni Navarra) |  | 7,226e+04 a 9,443e+04 | 2019-2024 | C1 |

## V7.2 · Exuberancia (GSADF)

**Lectura.** Hay niveles explosivos, pero no exuberancia de los cocientes tras el ajuste múltiple. La pregunta Q9 de V16 repite el contraste por territorio y debe declarar estas cifras.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V72-GSADF-ccaa-bh | Series de CCAA (precio/alquiler, IPV y valor tasado; 17 CCAA) con exuberancia tras BH | 0 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-ccaa-v6 | CCAA con exuberancia (p<0,05) en el ratio precio/alquiler, provincias de entrenamiento v6 | 0 |  | 2015T1-2024T4 | C4 |
| V72-GSADF-niveles-bh | Niveles de precio nacionales (IPV y valor tasado, sin fundamentales) con exuberancia tras BH | 0 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-ratios-bh | Cocientes precio/renta y precio/alquiler nacionales con exuberancia tras BH | 0 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-ratios-bh4-sens | SENSIBILIDAD: cocientes precio/renta y precio/alquiler nacionales con exuberancia tras BH en la familia de los 4 cocientes (la principal es la de 8) | 1 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-ratios-p05 | Cocientes precio/renta y precio/alquiler nacionales con exuberancia sin ajuste múltiple (p<0,05) | 1 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-rev | Series nacionales del GSADF de v5 que se reproducen exactamente con el mismo método y la misma semilla | 14 |  | 2007T1-2026T2 | C4 |
| V72-GSADF-tipos-p05 | Precio frente a valores de referencia con tipos de interés (descuento del alquiler y cuota sobre renta) con exuberancia sin ajuste | 0 |  | 2007T1-2026T2 | C4 |

## V6.1 (K1) · Predicción en la muestra sellada v6

**Lectura.** Ningún modelo predice mejor que la línea base más exigente en la validación sellada v6. H5 de V15 y Q10 de V16 parten de aquí.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| K1-N-MEJOR | Tareas en que el mejor modelo predice mejor que la base mas exigente (DM-HLN y permutacion, Holm, grupo espacial) | 6 |  | validacion sellada v6 | C4 |
| K1-N-TAREAS | Tareas comparadas en la validacion sellada v6 (K1) | 9 |  | validacion sellada v6 | C4 |

## V8 · Por qué ha subido (factores, periodos, factor común)

**Lectura.** Ningún factor destaca como principal. La parte no atribuida es C3s, válida solo bajo las restricciones del SVAR. El factor común domina en P5.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V8-H8-9-est | H8-9: correlación del factor común español con el crecimiento interanual del precio de la vivienda de la zona euro (EA19; intervalo al 95 %) | 0,5976 | 0,135 a 0,8578 | 2006T1-2026T2 | C4 |
| V8-M1-cuota-c-P5 | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P5 (banda del 68 %; resumen de comovimiento, sin lectura causal) | 92,79 | 86,65 a 94,92 | P5 (2022T3-último dato) | C4 |
| V8-OBS-a-P5 | Variación observada de alquiler real en P5 (pp, log×100; unidad común R0) | -1,846 |  | P5 (2022T3-último dato) | C4 |
| V8-OBS-c-P5 | Variación observada de precio real de compra en P5 (pp, log×100; unidad común R0) | 18,42 |  | P5 (2022T3-último dato) | C4 |
| V8-QNA-pp-c-P5 | Cuota no atribuida de precio real de compra en P5 en puntos: media posterior (mediana 3,4; cola derecha pesada, con el tipo hipotecario del Banco de España en lugar del BCE la media sería 20,7 y la mediana 3,5); banda del 68 % exacta (cuantiles de la suma); condicionado a las restricciones de signo y de cero de M2 | 9,516 | -7,762 a 16,44 | P5 (2022T3-último dato) | C3s |
| V8-VOTOS-c-P5 | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P5: crédito y tipos | 2 |  | P5 (2022T3-último dato) | C4 |

## V9-D1 · Topes y zonas tensionadas (Incasòl)

**Lectura.** D1a (zonas tensionadas, 2022T2-2026T1) no supera pretendencias, placebo de fecha ni Honest DiD. D1b (Ley 11/2020) supera pretendencias y placebo, pero no Honest DiD (M̄ de ruptura < 1). Todo es C4. H1 y H2 de V15 y Q1 de V16 usan otro diseño sobre una ventana ya vista: lo ya visto es informativo.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V9-D1a-contratos-att | zonas tensionadas (Ley 12/2023): diferencia (ATT, CS) en el número de contratos nuevos | -6,25 | -13,21 a 0,706 | 2022T2-2026T1 | C4 |
| V9-D1a-contratos-placebo-p | zonas tensionadas (Ley 12/2023), log contratos: p del placebo de fecha (4 trimestres antes) | 0,6126 |  | 2022T2-2026T1 | C4 |
| V9-D1a-contratos-pretend-p | zonas tensionadas (Ley 12/2023), log contratos: p del contraste conjunto de pretendencias | 0,03134 |  | 2022T2-2026T1 | C4 |
| V9-D1a-contratos-ruptura | zonas tensionadas (Ley 12/2023), log contratos: M̄ de ruptura de Honest DiD (magnitudes relativas, simplificado) | 0 |  | 2022T2-2026T1 | C4 |
| V9-D1a-renta-att | zonas tensionadas (Ley 12/2023): diferencia (ATT, CS) en la renta media de los contratos nuevos | -5,846 | -8,499 a -3,193 | 2022T2-2026T1 | C4 |
| V9-D1a-renta-pholm | zonas tensionadas (Ley 12/2023), log renta media: p ajustado por Holm (familia confirmatoria de V9) | 0 |  | 2022T2-2026T1 | C4 |
| V9-D1a-renta-placebo-p | zonas tensionadas (Ley 12/2023), log renta media: p del placebo de fecha (4 trimestres antes) | 0,00701 |  | 2022T2-2026T1 | C4 |
| V9-D1a-renta-pretend-p | zonas tensionadas (Ley 12/2023), log renta media: p del contraste conjunto de pretendencias | 0,0004 |  | 2022T2-2026T1 | C4 |
| V9-D1a-renta-ruptura | zonas tensionadas (Ley 12/2023), log renta media: M̄ de ruptura de Honest DiD (magnitudes relativas, simplificado) | 0,2 |  | 2022T2-2026T1 | C4 |
| V9-D1b-contratos-att | Ley catalana 11/2020: diferencia (ATT, CS) en el número de contratos nuevos | -1,317 | -7,02 a 4,385 | 2019T1-2022T1 | C4 |
| V9-D1b-contratos-placebo-p | Ley catalana 11/2020, log contratos: p del placebo de fecha (4 trimestres antes) | 0,1562 |  | 2019T1-2022T1 | C4 |
| V9-D1b-contratos-pretend-p | Ley catalana 11/2020, log contratos: p del contraste conjunto de pretendencias | 0,2802 |  | 2019T1-2022T1 | C4 |
| V9-D1b-contratos-ruptura | Ley catalana 11/2020, log contratos: M̄ de ruptura de Honest DiD (magnitudes relativas, simplificado) | 0 |  | 2019T1-2022T1 | C4 |
| V9-D1b-renta-att | Ley catalana 11/2020: diferencia (ATT, CS) en la renta media de los contratos nuevos | -5,851 | -7,346 a -4,356 | 2019T1-2022T1 | C4 |
| V9-D1b-renta-pholm | Ley catalana 11/2020, log renta media: p ajustado por Holm (familia confirmatoria de V9) | 0 |  | 2019T1-2022T1 | C4 |
| V9-D1b-renta-placebo-p | Ley catalana 11/2020, log renta media: p del placebo de fecha (4 trimestres antes) | 0,4084 |  | 2019T1-2022T1 | C4 |
| V9-D1b-renta-pretend-p | Ley catalana 11/2020, log renta media: p del contraste conjunto de pretendencias | 0,2816 |  | 2019T1-2022T1 | C4 |
| V9-D1b-renta-ruptura | Ley catalana 11/2020, log renta media: M̄ de ruptura de Honest DiD (magnitudes relativas, simplificado) | 0,5 |  | 2019T1-2022T1 | C4 |
| V9-D1c-renta-att | Zonas tensionadas de Euskadi: ATT exploratorio sobre la renta de fianzas nuevas (EMAL) | -2,484 | -3,519 a -1,449 | 2016T1-2025T4 | C4 |

## V9-D2/D3 · Vivienda turística

**Lectura.** Pretendencias rechazadas en D2; D3 sin potencia y con un placebo del mismo signo. C4. H3 de V15 y Q2 de V16 cambian de datos y de diseño.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V9-D2-renta-covid | Viviendas de uso turístico en 2019 × COVID 2020-2021: variación de la renta de contratos nuevos por 1 DE de dosis | 0,219 | -0,549 a 0,987 | 2014-2025 | C4 |
| V9-D2-renta-pretend-p | D2, renta: p del contraste conjunto de pretendencias (2014-2018) | 0,00023 |  | 2014-2018 | C4 |
| V9-D2-renta-reap | Viviendas de uso turístico en 2019 × reapertura 2022-2025: variación de la renta de contratos nuevos por 1 DE de dosis | 1,046 | 0,39 a 1,703 | 2014-2025 | C4 |
| V9-D3-cuota | Caída del registro VUT (por 1 VUT por 100 viviendas) y variación de la cuota provincial de fianzas 2024→2025 por CP (descriptivo) | 0,00205 | -0,00216 a 0,00625 | 2024-2025 | C4 |
| V9-D3-media | Caída del registro VUT (por 1 VUT por 100 viviendas) y variación de la fianza media 2024→2025 por CP (descriptivo) | -0,195 | -0,413 a 0,024 | 2024-2025 | C4 |

## V9-D4 · Inmigración (2SLS shift-share provincial)

**Lectura.** Instrumento débil en todas las variantes (F efectiva < 5). C4, no concluyente. H4 de V15 es municipal; Q3 de V16 separa alquiler de compra y la escala de barrio.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V9-D4-ipc-ampliacion | Inmigración (2SLS shift-share), IPC de alquiler: elasticidad por punto de población extranjera (2015-2022) | 1,525 | -1,364 a 4,414 | 2015-2022 | C4 |
| V9-D4-ipc-ampliacion-F | Inmigración, IPC de alquiler: F efectiva del instrumento | 2,794 |  | 2015-2022 | C4 |
| V9-D4-ipc-replica | Inmigración (2SLS shift-share), IPC de alquiler: elasticidad por punto de población extranjera (2003-2012) | 0,723 | -0,815 a 2,261 | 2003-2012 | C4 |
| V9-D4-ipc-replica-F | Inmigración, IPC de alquiler: F efectiva del instrumento | 4,551 |  | 2003-2012 | C4 |
| V9-D4-tasado-ampliacion | Inmigración (2SLS shift-share), valor tasado: elasticidad por punto de población extranjera (2015-2022) | 12,88 | -1,452 a 27,21 | 2015-2022 | C4 |
| V9-D4-tasado-ampliacion-F | Inmigración, valor tasado: F efectiva del instrumento | 3,438 |  | 2015-2022 | C4 |
| V9-D4-tasado-replica | Inmigración (2SLS shift-share), valor tasado: elasticidad por punto de población extranjera (2003-2012) | -0,286 | -2,716 a 2,145 | 2003-2012 | C4 |
| V9-D4-tasado-replica-F | Inmigración, valor tasado: F efectiva del instrumento | 3,656 |  | 2003-2012 | C4 |

## V9-D5 a D7 · Otros diseños

**Lectura.** Ver cada fila: capa y periodo. D6 (Bono Alquiler Joven) no es estimable sin microdatos de perceptores.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V9-D5-alq-h4 | Shock monetario del BCE × cuota de hipotecas a tipo variable (1 DE): Δ log alquiler (h = 4) | -11,68 | -17,4 a -5,962 | 2008T1-2025T3 | C4 |
| V9-D5-precio-h4 | Shock monetario del BCE × cuota de hipotecas a tipo variable (1 DE): Δ log precio (h = 4) | -5,251 | -15,63 a 5,13 | 2008T1-2025T3 | C4 |
| V9-D5-precio-h8 | Shock monetario del BCE × cuota de hipotecas a tipo variable (1 DE): Δ log precio (h = 8) | -4,389 | -17,54 a 8,759 | 2008T1-2025T3 | C4 |
| V9-D7-CV-1121-H0 | Hogares al inicio (2011-2021; descomposición D7) | 1,987e+06 |  | 2011-2021 | C4 |
| V9-D7-CV-1121-H1 | Hogares al final (2011-2021; descomposición D7) | 2,023e+06 |  | 2011-2021 | C4 |
| V9-D7-CV-1121-P0 | Población al inicio (2011-2021; descomposición D7) | 5,129e+06 |  | 2011-2021 | C4 |
| V9-D7-CV-1121-P1 | Población al final (2011-2021; descomposición D7) | 5,098e+06 |  | 2011-2021 | C4 |
| V9-D7-CV-1121-cuota-pob | Componente población del aumento de hogares (2011-2021), % del total | -33,98 |  | 2011-2021 | C4 |
| V9-D7-CV-1121-dH | Aumento de hogares (2011-2021) | 3,56e+04 |  | 2011-2021 | C4 |
| V9-D7-CV-2225-H0 | Hogares al inicio (2022-2025; descomposición D7) | 2,063e+06 |  | 2022-2025 | C4 |
| V9-D7-CV-2225-H1 | Hogares al final (2022-2025; descomposición D7) | 2,178e+06 |  | 2022-2025 | C4 |
| V9-D7-CV-2225-P0 | Población al inicio (2022-2025; descomposición D7) | 5,108e+06 |  | 2022-2025 | C4 |
| V9-D7-CV-2225-P1 | Población al final (2022-2025; descomposición D7) | 5,425e+06 |  | 2022-2025 | C4 |
| V9-D7-CV-2225-cuota-pob | Componente población del aumento de hogares (2022-2025), % del total | 111,6 |  | 2022-2025 | C4 |
| V9-D7-CV-2225-dH | Aumento de hogares (2022-2025) | 1,144e+05 |  | 2022-2025 | C4 |
| V9-D7-ES-1121-H0 | Hogares al inicio (2011-2021; descomposición D7) | 1,808e+07 |  | 2011-2021 | C4 |
| V9-D7-ES-1121-H1 | Hogares al final (2011-2021; descomposición D7) | 1,854e+07 |  | 2011-2021 | C4 |
| V9-D7-ES-1121-P0 | Población al inicio (2011-2021; descomposición D7) | 4,727e+07 |  | 2011-2021 | C4 |
| V9-D7-ES-1121-P1 | Población al final (2011-2021; descomposición D7) | 4,748e+07 |  | 2011-2021 | C4 |
| V9-D7-ES-1121-cuota-pob | Componente población del aumento de hogares (2011-2021), % del total | 13,65 |  | 2011-2021 | C4 |
| V9-D7-ES-1121-dH | Aumento de hogares (2011-2021) | 4,529e+05 |  | 2011-2021 | C4 |
| V9-D7-ES-2225-H0 | Hogares al inicio (2022-2025; descomposición D7) | 1,882e+07 |  | 2022-2025 | C4 |
| V9-D7-ES-2225-H1 | Hogares al final (2022-2025; descomposición D7) | 1,952e+07 |  | 2022-2025 | C4 |
| V9-D7-ES-2225-P0 | Población al inicio (2022-2025; descomposición D7) | 4,749e+07 |  | 2022-2025 | C4 |
| V9-D7-ES-2225-P1 | Población al final (2022-2025; descomposición D7) | 4,913e+07 |  | 2022-2025 | C4 |
| V9-D7-ES-2225-cuota-pob | Componente población del aumento de hogares (2022-2025), % del total | 91,96 |  | 2022-2025 | C4 |
| V9-D7-ES-2225-dH | Aumento de hogares (2022-2025) | 6,989e+05 |  | 2022-2025 | C4 |
| V9-D7-c1-dif | Hogares 2021: ECP (1-1-2022) frente a censo 2021 (viviendas principales), diferencia | 1,54 |  | 2021 | C4 |

## V12 · Población, hogares, oferta, titularidad, condiciones y turismo (descriptivo)

**Lectura.** Contabilidades y descriptivos C4. V16 los amplía (fase 2), sin lenguaje causal.

| id | Indicador | Valor | Rango | Periodo | Capa |
|---|---|---|---|---|---|
| V12-B1-2022-2024-crecimiento | Crecimiento de la población, España, 2022-2024 | 1,642e+06 |  | 2022-2024 | C4 |
| V12-B1-2022-2024-residuo | Residuo de la identidad demográfica, España, 2022-2024 | 8897 |  | 2022-2024 | C4 |
| V12-B1-2022-2024-saldo_exterior | Saldo migratorio con el extranjero, España, 2022-2024 | 1,996e+06 |  | 2022-2024 | C4 |
| V12-B1-2022-2024-vegetativo | Saldo vegetativo (nacimientos − defunciones), España, 2022-2024 | -3,629e+05 |  | 2022-2024 | C4 |
| V12-B2-alicante-saldo-corona | Saldo de la capital con su corona metropolitana (alicante), 2022-2024 | -3590 |  | 2022-2024 | C4 |
| V12-B2-barcelona-saldo-corona | Saldo de la capital con su corona metropolitana (barcelona), 2022-2024 | -2,254e+04 |  | 2022-2024 | C4 |
| V12-B2-castellon-saldo-corona | Saldo de la capital con su corona metropolitana (castellon), 2022-2024 | -650 |  | 2022-2024 | C4 |
| V12-B2-madrid-saldo-corona | Saldo de la capital con su corona metropolitana (madrid), 2022-2024 | -2,92e+04 |  | 2022-2024 | C4 |
| V12-B2-valencia-saldo-corona | Saldo de la capital con su corona metropolitana (valencia), 2022-2024 | -1,222e+04 |  | 2022-2024 | C4 |
| V12-B3-hogares-crec | Crecimiento del número de hogares, España, 2011-2021 | 4,555e+05 |  | 2011-2021 | C4 |
| V12-B3-hogares-estructura | Componente «estructura por edad» del crecimiento de hogares 2011-2021 (media de los dos órdenes; rango = órdenes) | 1,072e+06 | 9,668e+05 a 1,177e+06 | 2011-2021 | C4 |
| V12-B3-hogares-ext | Hogares cuya persona de referencia tiene nacionalidad extranjera, España | 9,73 | 9,69 a 9,77 | 2021 | C4 |
| V12-B3-hogares-jefatura | Componente «tasa de jefatura» del crecimiento de hogares 2011-2021 (media de los dos órdenes; rango = órdenes) | -8,127e+05 | -9,19e+05 a -7,064e+05 | 2011-2021 | C4 |
| V12-B3-hogares-poblacion | Componente «población» del crecimiento de hogares 2011-2021 (media de los dos órdenes; rango = órdenes) | 1,965e+05 | 1,951e+05 a 1,979e+05 | 2011-2021 | C4 |
| V12-B4-hogares-nuevos | Hogares nuevos (ECP), 1-1-2021 → 1-1-2025, 46 provincias con Catastro y MIVAU | 9,346e+05 |  | 2021-2024 | C4 |
| V12-B4-obra-catastro | Obra nueva neta (Catastro, unidades residenciales), 2021-2024 | 3,555e+05 |  | 2021-2024 | C4 |
| V12-B4-regularizacion | Exceso del Catastro sobre el MIVAU en 2013-2017 (regularización catastral) | 3,488e+05 |  | 2013-2017 | C4 |
| V12-B4-terminadas-mivau | Viviendas terminadas (MIVAU: libres + protegidas), 2021-2024 | 3,464e+05 |  | 2021-2024 | C4 |
| V12-B5-pct_PJ | Viviendas de personas jurídicas privadas, España sin País Vasco ni Navarra, 2026 | 4,583 |  | 2026 | C4 |
| V12-B5-pct_mas10 | Viviendas de titulares con más de 10 viviendas, España sin País Vasco ni Navarra, 2026 | 4,165 |  | 2026 | C4 |
| V12-B5-pct_mas100 | Viviendas de titulares con más de 100 viviendas, España sin País Vasco ni Navarra, 2026 | 2,059 |  | 2026 | C4 |
| V12-B6-brecha-sobrecarga_40 | Sobrecarga > 40 %: personas adultas de nacionalidad extranjera − española de igual edad y renta (puntos) | 14,66 | 13,27 a 16,31 | 2023-2025 | C4 |
| V12-B7-CV-vut-ine | Viviendas turísticas anunciadas (INE), Comunitat Valenciana | 5,127e+04 |  | 2026-05 | C4 |
| V12-B7-CV-vut-registro | Viviendas turísticas inscritas en el registro de la GVA, Comunitat Valenciana | 9,012e+04 |  | 2026-10-14 | C4 |

## V15 · Auditorías de calidad de los datos (fase 1; descriptivas)

No son cifras publicadas: son diagnósticos de los datos que V16 usa y que todo diseño debe tener en cuenta. Detalle en output/v15/auditoria/<grupo>/informe.md.

- **precios_compra** (output/v15/auditoria/precios_compra/): Auditoría C4: sin efectos ni regresiones. Sin series por periodo de Notariado, Registradores ni ERI en output.; Tasas de Registradores: suma móvil de 4 trimestres (suaviza y retrasa); se comparan en variante ventana4.; Notariado: precio m2 nacional semestral; sin serie territorial de precio por m2 en el repositorio.; Municipios MIVAU sin código INE en el raw: atípicos y cobertura se reportan por n
- **alquiler** (output/v15/auditoria/alquiler/): Auditoría descriptiva C4: sin efectos ni regresiones; el estadístico de cambio de media es solo orientativo, sin p-valor.; Incasòl e Inside Airbnb (licencia no abierta): en output solo estadísticos resumen y recuentos de municipios; sin series por periodo.; Cruces solo por código INE. Excluido del cruce: la tabla de alquiler por CP de la Comunidad de Madrid (origen no verificado, data/raw/v3/madri
- **oferta_parque** (output/v15/auditoria/oferta_parque/): Sin efectos ni regresiones. Cruces solo por código INE. Interpolados excluidos de los atípicos. La regularización catastral 2013-2017 y el origen del parque estimado del MIVAU se citan de la documentación del repositorio (docs/v12) y no se han verificado aquí.
- **demografia_hogares** (output/v15/auditoria/demografia_hogares/): SEED=20261010 (sin aleatoriedad); cruces por código INE; ningún efecto estimado; solo agregados propios de INE, Catastro y Ajuntament de València
- **turismo** (output/v15/auditoria/turismo/): Auditoría C4: sin efectos ni regresiones. Muestra reservada de V6 excluida con NOT coalesce(muestra_sellada_v6,false).; Inside Airbnb y registro de Catalunya (Socrata, «Ver términos de uso»): solo estadísticos resumen; sin series por unidad.; Además de data/base y data/raw, el script lee los zip originales de Barcelona en data/manual/v11/bcn_hut_trimestral solo para recontar filas por barrio (lect
- **financiacion_macro** (output/v15/auditoria/financiacion_macro/): Auditoría C4 sin efectos; hechos filtrado con NOT coalesce(muestra_sellada_v6,false) (41 de 52 provincias en series provinciales); no se lee la muestra sellada.; Sin series de Notariado, Registradores ni AEAT en la salida (variables aeat_ excluidas del grupo).; ipc_general, ss_afiliados provinciales totales, eu_*, bis_rpp y oecd_house_prices no están en hechos (solo en data/raw o como derivadas).
- **renta_microdatos** (output/v15/auditoria/renta_microdatos/): Auditoría C4: sin efectos. Solo agregados propios de AEAT (razones, recuentos de atípicos, correlaciones); sin series municipales de AEAT.; Celdas del Censo 2021 (clase b) y recuentos ECV con n<10 suprimidos; no se escribe ningún microdato.; ADRH 2021 solo en el crudo (data/raw/v3), con campos etiquetados por orden (supuesto); la base no tiene 2021.; ECEPOV: persona 01 del hogar como proxy de la p

## V15 · Pre-registro interno (sin sello de tiempo externo)

- H1-H5 están fijados en docs/v15/preregistro_v15.md y sus adendas 1 y 2 (pre-registro interno, fijado en el commit 542b4fd y publicado como etiqueta prereg-v15 el 2026-10-17, sin sello de tiempo externo; docs/preregistros.md). V16 no los modifica.
- Solo es confirmatorio lo publicado después del corte del 17-10-2026. Calendario: H1 y H2 hacia marzo de 2027; H5 hacia octubre de 2027; H4 en el último trimestre de 2027.
- Potencia (output/v15/potencia/informe.md) y sellado (docs/v15/sellado_v15.json): V16 los reutiliza y no toca su muestra sellada.
