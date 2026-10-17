# V16 · Fase 2.1 · Fichas de las cifras

Una ficha por cifra: definición, fuentes, por qué es o no C1, tolerancia y cálculo reproducible (`python3 src/v16/f2_hechos.py`).

### V16-HEC-ALQ-BRECHA-2124-CAT
<a id="v16-hec-alq-brecha-2124-cat"></a>

- **Definición.** Brecha de crecimiento contratos nuevos menos vigentes 2021-2024, Cataluña (p.p.; 2021-2024; Cataluña).
- **Fuentes.** INE IPVA; Incasòl fianzas; INE IPC alquiler (grupos: aeat_irpf, encuesta_ine, fianzas_cat).
- **Capa C1.** Brecha A (IPVA nuevo - IPVA existente) = 9.7 p.p. y brecha B (Incasòl fianzas - IPC alquiler Cataluña) = 11.9 p.p. Coinciden dentro de ±3.0 p.p. con fuentes de tres grupos (aeat_irpf, fianzas, encuesta_ine); valor = punto medio.
- **Tolerancia.** ±3.0 p.p. entre las dos estimaciones de la brecha
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; IPVA provincial (59005) ponderado por contratos SERPAVI 2024; cambio acumulado de los contratos nuevos - vigentes. Controles con A23-A9: IPVA nuevo 17.2 %, Incasòl fianzas 16.6 %, IPC alquiler 4.8 %, IPVA existente 7.5 %.

### V16-HEC-ALQ-BRECHA-2124-CV
<a id="v16-hec-alq-brecha-2124-cv"></a>

- **Definición.** Brecha de crecimiento contratos nuevos menos vigentes 2021-2024, Comunitat Valenciana (p.p.; 2021-2024; Comunitat Valenciana).
- **Fuentes.** INE IPVA; GVA fianzas; INE IPC alquiler (grupos: aeat_irpf, encuesta_ine, fianzas_cv).
- **Capa C4.** Brecha A (IPVA nuevo - IPVA existente) = 16.0 p.p. y brecha B (GVA fianzas - IPC alquiler Comunitat Valenciana) = 23.6 p.p. No coinciden dentro de ±3.0 p.p.: se publican ambas (rango), capa C4.
- **Tolerancia.** ±3.0 p.p. entre las dos estimaciones de la brecha
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; IPVA provincial (59005) ponderado por contratos SERPAVI 2024; cambio acumulado de los contratos nuevos - vigentes. Controles con A23-A10: IPVA nuevo 26.1 %, GVA fianzas 30.8 %, IPC alquiler 7.2 %, IPVA existente 10.0 %.

### V16-HEC-ALQ-BRECHA-2125-CAT
<a id="v16-hec-alq-brecha-2125-cat"></a>

- **Definición.** Brecha de crecimiento fianzas nuevas menos IPC alquiler 2021-2025, Cataluña (p.p.; 2021-2025; Cataluña).
- **Fuentes.** Incasòl fianzas; INE IPC alquiler (grupos: encuesta_ine, fianzas_cat).
- **Capa C4.** Una sola medida de contratos nuevos en 2025 (IPVA acaba en 2024): C4.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; Incasòl fianzas 18.9 % menos IPC alquiler 6.3 %. IPVA acaba en 2024.

### V16-HEC-ALQ-BRECHA-2125-CV
<a id="v16-hec-alq-brecha-2125-cv"></a>

- **Definición.** Brecha de crecimiento fianzas nuevas menos IPC alquiler 2021-2025, Comunitat Valenciana (p.p.; 2021-2025; Comunitat Valenciana).
- **Fuentes.** GVA fianzas; INE IPC alquiler (grupos: encuesta_ine, fianzas_cv).
- **Capa C4.** Una sola medida de contratos nuevos en 2025 (IPVA acaba en 2024): C4.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; GVA fianzas 47.7 % menos IPC alquiler 11.5 %. IPVA acaba en 2024.

### V16-HEC-ALQ-IPC-NOMINAL-2007-2025
<a id="v16-hec-alq-ipc-nominal-2007-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado nominal 2007-2025, España (%; 2007-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-IPC-NOMINAL-2013-2025
<a id="v16-hec-alq-ipc-nominal-2013-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado nominal 2013-2025, España (%; 2013-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-IPC-NOMINAL-2019-2025
<a id="v16-hec-alq-ipc-nominal-2019-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado nominal 2019-2025, España (%; 2019-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-IPC-REAL-2007-2025
<a id="v16-hec-alq-ipc-real-2007-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado real 2007-2025, España (%; 2007-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-IPC-REAL-2013-2025
<a id="v16-hec-alq-ipc-real-2013-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado real 2013-2025, España (%; 2013-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-IPC-REAL-2019-2025
<a id="v16-hec-alq-ipc-real-2019-2025"></a>

- **Definición.** IPC de alquiler (stock), cambio acumulado real 2019-2025, España (%; 2019-2025 (media anual); España).
- **Fuentes.** INE IPC alquiler (grupos: encuesta_ine).
- **Capa C4.** Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, así que 2025 no tiene segunda fuente.

### V16-HEC-ALQ-NIVEL-2024-CAT
<a id="v16-hec-alq-nivel-2024-cat"></a>

- **Definición.** Brecha de nivel contrato nuevo frente a existente en 2024 (IPVA), Cataluña (%; 2024; Cataluña).
- **Fuentes.** INE IPVA (grupos: aeat_irpf).
- **Capa C4.** Una sola fuente (IPVA, AEAT-IRPF): el nivel relativo no tiene segunda fuente independiente comparable en la misma unidad.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; cociente IPVA nuevo/existente 2024 por provincia, ponderado.

### V16-HEC-ALQ-NIVEL-2024-CV
<a id="v16-hec-alq-nivel-2024-cv"></a>

- **Definición.** Brecha de nivel contrato nuevo frente a existente en 2024 (IPVA), Comunitat Valenciana (%; 2024; Comunitat Valenciana).
- **Fuentes.** INE IPVA (grupos: aeat_irpf).
- **Capa C4.** Una sola fuente (IPVA, AEAT-IRPF): el nivel relativo no tiene segunda fuente independiente comparable en la misma unidad.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_alquiler.py:brechas; cociente IPVA nuevo/existente 2024 por provincia, ponderado.

### V16-HEC-ALQ-STOCK-NOMINAL-2013-2024
<a id="v16-hec-alq-stock-nominal-2013-2024"></a>

- **Definición.** Alquiler de contratos vigentes, cambio acumulado nominal 2013-2024, España (%; 2013-2024 (media anual); España).
- **Fuentes.** INE IPC alquiler; INE IPVA; SERPAVI (grupos: aeat_irpf, encuesta_ine).
- **Capa C4.** Sin dos grupos distintos dentro de ±3.0 p.p.: {'INE IPC alquiler': 9.6, 'INE IPVA': 22.3, 'SERPAVI': 40.7}. INE IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): un solo grupo. Se publican todas.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual; IPVA total (59005), SERPAVI composición constante, IPC alquiler; real con IPC general.

### V16-HEC-ALQ-STOCK-NOMINAL-2019-2024
<a id="v16-hec-alq-stock-nominal-2019-2024"></a>

- **Definición.** Alquiler de contratos vigentes, cambio acumulado nominal 2019-2024, España (%; 2019-2024 (media anual); España).
- **Fuentes.** INE IPC alquiler; INE IPVA; SERPAVI (grupos: aeat_irpf, encuesta_ine).
- **Capa C4.** Sin dos grupos distintos dentro de ±3.0 p.p.: {'INE IPC alquiler': 7.5, 'INE IPVA': 11.7, 'SERPAVI': 21.2}. INE IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): un solo grupo. Se publican todas.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual; IPVA total (59005), SERPAVI composición constante, IPC alquiler; real con IPC general.

### V16-HEC-ALQ-STOCK-REAL-2013-2024
<a id="v16-hec-alq-stock-real-2013-2024"></a>

- **Definición.** Alquiler de contratos vigentes, cambio acumulado real 2013-2024, España (%; 2013-2024 (media anual); España).
- **Fuentes.** INE IPC alquiler; INE IPVA; SERPAVI (grupos: aeat_irpf, encuesta_ine).
- **Capa C4.** Sin dos grupos distintos dentro de ±3.0 p.p.: {'INE IPC alquiler': -10.6, 'INE IPVA': -0.3, 'SERPAVI': 14.7}. INE IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): un solo grupo. Se publican todas.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual; IPVA total (59005), SERPAVI composición constante, IPC alquiler; real con IPC general.

### V16-HEC-ALQ-STOCK-REAL-2019-2024
<a id="v16-hec-alq-stock-real-2019-2024"></a>

- **Definición.** Alquiler de contratos vigentes, cambio acumulado real 2019-2024, España (%; 2019-2024 (media anual); España).
- **Fuentes.** INE IPC alquiler; INE IPVA; SERPAVI (grupos: aeat_irpf, encuesta_ine).
- **Capa C4.** Sin dos grupos distintos dentro de ±3.0 p.p.: {'INE IPC alquiler': -9.3, 'INE IPVA': -5.7, 'SERPAVI': 2.3}. INE IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): un solo grupo. Se publican todas.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_alquiler.py:stock_nacional; media anual; IPVA total (59005), SERPAVI composición constante, IPC alquiler; real con IPC general.

### V16-HEC-ESPORADICO-2021
<a id="v16-hec-esporadico-2021"></a>

- **Definición.** Viviendas de uso esporádico por consumo eléctrico, Censo 2021 (viviendas; 2021; España).
- **Fuentes.** Censo 2021 consumo eléctrico; Censo 2021 (grupos: censo).
- **Capa C4.** Las «vacías del Censo» solo se publican en la tabla 59531 (consumo eléctrico), que es una tabla del propio Censo 2021 con el mismo universo (26.623.708 viviendas, comprobado). Las vacías del Censo y las vacías por consumo eléctrico son la misma cifra: no son independientes. Fuente única: C4. Las vacías por consumo y el uso esporádico son subconjuntos de las no principales (78% de ellas).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** tabla 59531, fila «Viviendas de uso esporádico».

### V16-HEC-HOGARES-ECP-2125
<a id="v16-hec-hogares-ecp-2125"></a>

- **Definición.** Aumento del número de hogares (ECP, 1-1-2021 a 1-1-2025) (hogares; 2021-2025; España).
- **Fuentes.** INE ECP (grupos: ine_hogares).
- **Capa C4.** Aquí solo ECP (un extremo): C4; la cifra C1 con ECP y EPA sigue siendo dh_2125.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** ECP 2025T1 - 2021T1 de la base. Reproduce el extremo inferior publicado de dh_2125 (981823); la cifra publicada dh_2125 (C1, con EPA) no se recalcula ni se sustituye.

### V16-HEC-INTL-HPI_RPI-ES-2007-2025
<a id="v16-hec-intl-hpi_rpi-es-2007-2025"></a>

- **Definición.** Ratio precio/alquiler, cambio acumulado del índice 2007-2025: España (%; 2007-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_RPI-ES-2019-2025
<a id="v16-hec-intl-hpi_rpi-es-2019-2025"></a>

- **Definición.** Ratio precio/alquiler, cambio acumulado del índice 2019-2025: España (%; 2019-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_RPI-MED-2007-2025
<a id="v16-hec-intl-hpi_rpi-med-2007-2025"></a>

- **Definición.** Ratio precio/alquiler, cambio acumulado del índice 2007-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2007-2025; UE (21 países) y OCDE (32 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_RPI-MED-2019-2025
<a id="v16-hec-intl-hpi_rpi-med-2019-2025"></a>

- **Definición.** Ratio precio/alquiler, cambio acumulado del índice 2019-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2019-2025; UE (22 países) y OCDE (34 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_YDH-ES-2007-2025
<a id="v16-hec-intl-hpi_ydh-es-2007-2025"></a>

- **Definición.** Ratio precio/renta disponible, cambio acumulado del índice 2007-2025: España (%; 2007-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_YDH-ES-2019-2025
<a id="v16-hec-intl-hpi_ydh-es-2019-2025"></a>

- **Definición.** Ratio precio/renta disponible, cambio acumulado del índice 2019-2025: España (%; 2019-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_YDH-MED-2007-2025
<a id="v16-hec-intl-hpi_ydh-med-2007-2025"></a>

- **Definición.** Ratio precio/renta disponible, cambio acumulado del índice 2007-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2007-2025; UE (21 países) y OCDE (31 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-HPI_YDH-MED-2019-2025
<a id="v16-hec-intl-hpi_ydh-med-2019-2025"></a>

- **Definición.** Ratio precio/renta disponible, cambio acumulado del índice 2019-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2019-2025; UE (22 países) y OCDE (32 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-RHP-ES-2007-2025
<a id="v16-hec-intl-rhp-es-2007-2025"></a>

- **Definición.** Precio real de la vivienda, cambio acumulado 2007-2025: España (%; 2007-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-RHP-ES-2019-2025
<a id="v16-hec-intl-rhp-es-2019-2025"></a>

- **Definición.** Precio real de la vivienda, cambio acumulado 2019-2025: España (%; 2019-2025; España).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-RHP-MED-2007-2025
<a id="v16-hec-intl-rhp-med-2007-2025"></a>

- **Definición.** Precio real de la vivienda, cambio acumulado 2007-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2007-2025; UE (21 países) y OCDE (35 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 21 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-RHP-MED-2019-2025
<a id="v16-hec-intl-rhp-med-2019-2025"></a>

- **Definición.** Precio real de la vivienda, cambio acumulado 2019-2025: mediana UE (mínimo/máximo: mediana UE y OCDE) (%; 2019-2025; UE (22 países) y OCDE (37 países)).
- **Fuentes.** OCDE (grupos: ine_ipv_derivado).
- **Capa C4.** Comparación internacional: C4. El índice de precios español de la OCDE, el de Eurostat y el de la BIS salen del IPV del INE (correlación 0,9999; K6), y el de ratios usa la renta y el alquiler de las cuentas nacionales; no hay segunda fuente independiente para España.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:internacional; OCDE (Analytical house price indicators): media anual de cuatro trimestres (índice 2015=100); mediana de la variación entre los países con dato completo en las dos fechas. UE = 22 países de la lista UE presentes; OCDE = todos los de la serie.

### V16-HEC-INTL-SOBRECARGA-ES-2025
<a id="v16-hec-intl-sobrecarga-es-2025"></a>

- **Definición.** Tasa de sobrecarga del coste de la vivienda, España frente a la UE (2025); mínimo y máximo: España y UE (% de la población; 2025; España y UE-27).
- **Fuentes.** Eurostat ECV (grupos: ecv).
- **Capa C4.** Eurostat y el INE publican la misma ECV: no hay segunda fuente (V10-ATL-A1 bajó a C4 por esta razón).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** Eurostat ilc_lvho07a, total; España 7.2 % y UE-27 7.7 %. Valor = España.

### V16-HEC-LANZ-2013
<a id="v16-hec-lanz-2013"></a>

- **Definición.** Lanzamientos practicados en 2013, España (total) (lanzamientos; 2013; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA».

### V16-HEC-LANZ-2025
<a id="v16-hec-lanz-2025"></a>

- **Definición.** Lanzamientos practicados en 2025, España (total) (lanzamientos; 2025; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA».

### V16-HEC-LANZ-PICO
<a id="v16-hec-lanz-pico"></a>

- **Definición.** Año con más lanzamientos practicados 2013-2025 (2014), España (lanzamientos; 2014; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA».

### V16-HEC-LANZ-TIPO-HIPOTECARIA-2025
<a id="v16-hec-lanz-tipo-hipotecaria-2025"></a>

- **Definición.** Cuota de los lanzamientos por tipo «hipotecaria» en 2025, España (%; 2025; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA». Tipo: hoja «Lanzamientos E.hipotecaria TSJ». Los tres tipos suman 24,540 frente al total 24,540.

### V16-HEC-LANZ-TIPO-LAU-2025
<a id="v16-hec-lanz-tipo-lau-2025"></a>

- **Definición.** Cuota de los lanzamientos por tipo «lau» en 2025, España (%; 2025; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA». Tipo: hoja «Lanzamientos L.A.U  TSJ». Los tres tipos suman 24,540 frente al total 24,540.

### V16-HEC-LANZ-TIPO-OTROS-2025
<a id="v16-hec-lanz-tipo-otros-2025"></a>

- **Definición.** Cuota de los lanzamientos por tipo «otros» en 2025, España (%; 2025; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA». Tipo: hoja «Lanzamientos. Otros TSJ». Los tres tipos suman 24,540 frente al total 24,540.

### V16-HEC-LANZ-UM4T
<a id="v16-hec-lanz-um4t"></a>

- **Definición.** Lanzamientos practicados en los últimos cuatro trimestres (2025T3-2026T2), España (lanzamientos; 2025T3-2026T2; España).
- **Fuentes.** CGPJ (grupos: cgpj).
- **Capa C4.** Una sola fuente (CGPJ, estadística de los órganos judiciales): C4. Redistribuible «no»; se publica como agregado propio (terceros_1_0: agregados). Es el total de los 17 TSJ (nacional); los partidos judiciales de 2025 están excluidos (K6).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:lanzamientos; hoja «Lanzamientos practic. total TSJ» de cgpj_series_tsj_2T2026.xlsx, fila TOTAL; columnas «Total AAAA».

### V16-HEC-OBRA-SOBRE-HOGARES-2125
<a id="v16-hec-obra-sobre-hogares-2125"></a>

- **Definición.** Libres terminadas 2021-2025 por hogar nuevo (ECP 2021-2025) (viviendas por hogar; 2021-2025; España).
- **Fuentes.** MIVAU fin de obra; INE ECP (grupos: ine_hogares, mivau_obra).
- **Capa C4.** Cociente de dos cifras de capa C4: la capa es la menor de las componentes.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** terminadas 2021-2025 / aumento de hogares ECP. Cociente de dos fuentes distintas con ventanas distintas (año natural frente a 1 de enero): descriptivo, sin lectura causal ni déficit (el déficit con bajas es L3-DEF-2125).

### V16-HEC-OBRA-TERMINADAS-2025
<a id="v16-hec-obra-terminadas-2025"></a>

- **Definición.** Viviendas libres terminadas (MIVAU) en 2025 (viviendas; 2025; España).
- **Fuentes.** MIVAU fin de obra (grupos: mivau_obra).
- **Capa C4.** Fuente única (MIVAU).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** suma de los cuatro trimestres de 2025.

### V16-HEC-OBRA-TERMINADAS-2125
<a id="v16-hec-obra-terminadas-2125"></a>

- **Definición.** Viviendas libres terminadas (MIVAU, certificados de fin de obra; sin protegidas), acumulado 2021-2025 (viviendas; 2021-2025; España).
- **Fuentes.** MIVAU fin de obra (grupos: mivau_obra).
- **Capa C4.** Una sola fuente (MIVAU, fin de obra): la misma razón que E-T7-prod en bajadas_capa.csv. Amplía a 2025 la cifra de la 1.0 (terminadas_1924, otro periodo y otro id).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:obra_hogares; suma de trimestres de la variable terminadas (nacional) de la base, años completos.

### V16-HEC-PARQUE-CATASTRO-CENSO-2021
<a id="v16-hec-parque-catastro-censo-2021"></a>

- **Definición.** Unidades urbanas residenciales del Catastro (1-1-2022) frente a viviendas del Censo 2021, territorio común (% de diferencia; 2021-2022; Territorio común (sin País Vasco ni Navarra)).
- **Fuentes.** Catastro; Censo 2021 (grupos: catastro, censo).
- **Capa C4.** Las dos cifras coinciden dentro de la tolerancia, pero NO se declara C1: la independencia no está demostrada en el repositorio (el directorio de viviendas del Censo puede apoyarse en el Catastro; no verificado en la metodología oficial) y la misma vara bajó a C4 las parejas que comparten origen (V9-D7-c1-dif, V10-ATL-A1). C4.
- **Tolerancia.** ±15% en recuentos (capas.md)
- **Cálculo reproducible.** f2_hechos_resto.py:parque; Catastro 23,898,695 frente a Censo 25,217,528.

### V16-HEC-PARQUE-NOPRINCIPALES-2021
<a id="v16-hec-parque-noprincipales-2021"></a>

- **Definición.** Viviendas no principales (secundarias y vacías), Censo 2021 (viviendas; 1-11-2021; España).
- **Fuentes.** Censo 2021 (grupos: censo).
- **Capa C4.** Una sola fuente (Censo 2021, INE): estadística oficial de fuente única.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:parque; INE Censo 2021 tabla 59525 (tipo de vivienda, total nacional)

### V16-HEC-PARQUE-PRINCIPALES-2021
<a id="v16-hec-parque-principales-2021"></a>

- **Definición.** Viviendas principales, Censo 2021 (viviendas; 1-11-2021; España).
- **Fuentes.** Censo 2021 (grupos: censo).
- **Capa C4.** Una sola fuente (Censo 2021, INE): estadística oficial de fuente única.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:parque; INE Censo 2021 tabla 59525 (tipo de vivienda, total nacional)

### V16-HEC-PARQUE-TOTAL-2021
<a id="v16-hec-parque-total-2021"></a>

- **Definición.** Viviendas familiares, Censo 2021 (viviendas; 1-11-2021; España).
- **Fuentes.** Censo 2021 (grupos: censo).
- **Capa C4.** Una sola fuente (Censo 2021, INE): estadística oficial de fuente única.
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:parque; INE Censo 2021 tabla 59525 (tipo de vivienda, total nacional)

### V16-HEC-PRECIO-CCAA-NCOINC-2007-2025
<a id="v16-hec-precio-ccaa-ncoinc-2007-2025"></a>

- **Definición.** CCAA (de 17) con al menos dos medidas de grupos distintos (IPV, tasado, Registradores) dentro de ±3.0 p.p. en el cambio real 2007-2025 (CCAA; 2007-2025; 17 CCAA).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores (grupos: notarial, registral, tasacion).
- **Capa C4.** Recuento interno del análisis (contabilidad del proyecto), no un hecho contrastado con dos fuentes (misma razón que VER-A23-V2-1 en bajadas_capa.csv). El cambio por CCAA de cada medida está en precios_ccaa.csv.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_precios.py: tabla precios_ccaa.csv (cambios por CCAA y medida; columna capa_real). Deflactor nacional para todas.

### V16-HEC-PRECIO-CCAA-NCOINC-2013-2025
<a id="v16-hec-precio-ccaa-ncoinc-2013-2025"></a>

- **Definición.** CCAA (de 17) con al menos dos medidas de grupos distintos (IPV, tasado, Registradores) dentro de ±3.0 p.p. en el cambio real 2013-2025 (CCAA; 2013-2025; 17 CCAA).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores (grupos: notarial, registral, tasacion).
- **Capa C4.** Recuento interno del análisis (contabilidad del proyecto), no un hecho contrastado con dos fuentes (misma razón que VER-A23-V2-1 en bajadas_capa.csv). El cambio por CCAA de cada medida está en precios_ccaa.csv.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_precios.py: tabla precios_ccaa.csv (cambios por CCAA y medida; columna capa_real). Deflactor nacional para todas.

### V16-HEC-PRECIO-CCAA-NCOINC-2019-2025
<a id="v16-hec-precio-ccaa-ncoinc-2019-2025"></a>

- **Definición.** CCAA (de 17) con al menos dos medidas de grupos distintos (IPV, tasado, Registradores) dentro de ±3.0 p.p. en el cambio real 2019-2025 (CCAA; 2019-2025; 17 CCAA).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores (grupos: notarial, registral, tasacion).
- **Capa C4.** Recuento interno del análisis (contabilidad del proyecto), no un hecho contrastado con dos fuentes (misma razón que VER-A23-V2-1 en bajadas_capa.csv). El cambio por CCAA de cada medida está en precios_ccaa.csv.
- **Tolerancia.** ±3.0 p.p.
- **Cálculo reproducible.** f2_hechos_precios.py: tabla precios_ccaa.csv (cambios por CCAA y medida; columna capa_real). Deflactor nacional para todas.

### V16-HEC-PRECIO-NOM-2007-2025
<a id="v16-hec-precio-nom-2007-2025"></a>

- **Definición.** Precio de compra, cambio acumulado nominales 2007-2025 (media anual), España; medidas: IPV del INE (ajustado por calidad) y precios medios por m² (%; 2007-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C4.** Las medidas no coinciden dentro de ±3.0 p.p. entre al menos dos grupos independientes: {'INE IPV': 20.3, 'MIVAU valor tasado': 3.5, 'Registradores': 13.3, 'Notariado': -1.9}. Se publican todas (rango) y no se escoge una; la discrepancia de método entre el IPV y las tasaciones ya era conocida (A23-P3).
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2007-1; real = (1+nominal)/(1+IPC general)-1 con IPC 42.6 %.

### V16-HEC-PRECIO-NOM-2013-2025
<a id="v16-hec-precio-nom-2013-2025"></a>

- **Definición.** Precio de compra, cambio acumulado nominales 2013-2025 (media anual), España; medidas: IPV del INE (ajustado por calidad) y precios medios por m² (%; 2013-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C4.** Las medidas no coinciden dentro de ±3.0 p.p. entre al menos dos grupos independientes: {'INE IPV': 86.9, 'MIVAU valor tasado': 42.3, 'Registradores': 59.6, 'Notariado': 49.5}. Se publican todas (rango) y no se escoge una; la discrepancia de método entre el IPV y las tasaciones ya era conocida (A23-P3).
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2013-1; real = (1+nominal)/(1+IPC general)-1 con IPC 25.9 %.

### V16-HEC-PRECIO-NOM-2019-2025
<a id="v16-hec-precio-nom-2019-2025"></a>

- **Definición.** Precio de compra, cambio acumulado nominales 2019-2025 (media anual), España; medida: precio medio por m² sin ajuste de calidad (MIVAU valor tasado, Notariado, Registradores); el IPV del INE, ajustado por calidad, da 44.4 % (%; 2019-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C1.** Coinciden MIVAU valor tasado, Notariado, Registradores (grupos distintos) dentro de ±3.0 p.p.; valor = punto medio de esas fuentes, rango = entre fuentes. Todas las medidas: {'INE IPV': 44.4, 'MIVAU valor tasado': 29.6, 'Registradores': 31.7, 'Notariado': 29.7}.
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2019-1; real = (1+nominal)/(1+IPC general)-1 con IPC 21.7 %.

### V16-HEC-PRECIO-REAL-2007-2025
<a id="v16-hec-precio-real-2007-2025"></a>

- **Definición.** Precio de compra, cambio acumulado reales (deflactor IPC general) 2007-2025 (media anual), España; medidas: IPV del INE (ajustado por calidad) y precios medios por m² (%; 2007-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C4.** Las medidas no coinciden dentro de ±3.0 p.p. entre al menos dos grupos independientes: {'INE IPV': -15.7, 'MIVAU valor tasado': -27.5, 'Registradores': -20.5, 'Notariado': -31.3}. Se publican todas (rango) y no se escoge una; la discrepancia de método entre el IPV y las tasaciones ya era conocida (A23-P3).
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2007-1; real = (1+nominal)/(1+IPC general)-1 con IPC 42.6 %.

### V16-HEC-PRECIO-REAL-2013-2025
<a id="v16-hec-precio-real-2013-2025"></a>

- **Definición.** Precio de compra, cambio acumulado reales (deflactor IPC general) 2013-2025 (media anual), España; medidas: IPV del INE (ajustado por calidad) y precios medios por m² (%; 2013-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C4.** Las medidas no coinciden dentro de ±3.0 p.p. entre al menos dos grupos independientes: {'INE IPV': 48.4, 'MIVAU valor tasado': 13.0, 'Registradores': 26.7, 'Notariado': 18.7}. Se publican todas (rango) y no se escoge una; la discrepancia de método entre el IPV y las tasaciones ya era conocida (A23-P3).
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2013-1; real = (1+nominal)/(1+IPC general)-1 con IPC 25.9 %.

### V16-HEC-PRECIO-REAL-2019-2025
<a id="v16-hec-precio-real-2019-2025"></a>

- **Definición.** Precio de compra, cambio acumulado reales (deflactor IPC general) 2019-2025 (media anual), España; medida: precio medio por m² sin ajuste de calidad (MIVAU valor tasado, Notariado, Registradores); el IPV del INE, ajustado por calidad, da 18.7 % (%; 2019-2025 (media anual); España).
- **Fuentes.** INE IPV; MIVAU valor tasado; Registradores; Notariado (grupos: notarial, registral, tasacion).
- **Capa C1.** Coinciden MIVAU valor tasado, Notariado, Registradores (grupos distintos) dentro de ±3.0 p.p.; valor = punto medio de esas fuentes, rango = entre fuentes. Todas las medidas: {'INE IPV': 18.7, 'MIVAU valor tasado': 6.5, 'Registradores': 8.2, 'Notariado': 6.6}.
- **Tolerancia.** ±3.0 p.p. entre cambios acumulados
- **Cálculo reproducible.** f2_hechos_precios.py: media anual de 4 trimestres (IPV, tasado), anual (Registradores pm2) y de 2 semestres (Notariado); cambio = X_2025/X_2019-1; real = (1+nominal)/(1+IPC general)-1 con IPC 21.7 %.

### V16-HEC-VACIAS-CONSUMO-2021
<a id="v16-hec-vacias-consumo-2021"></a>

- **Definición.** Viviendas vacías por consumo eléctrico (Censo 2021, tabla 59531) (viviendas; 2021; España).
- **Fuentes.** Censo 2021 consumo eléctrico; Censo 2021 (grupos: censo).
- **Capa C4.** Las «vacías del Censo» solo se publican en la tabla 59531 (consumo eléctrico), que es una tabla del propio Censo 2021 con el mismo universo (26.623.708 viviendas, comprobado). Las vacías del Censo y las vacías por consumo eléctrico son la misma cifra: no son independientes. Fuente única: C4. Las vacías por consumo y el uso esporádico son subconjuntos de las no principales (78% de ellas).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** f2_hechos_resto.py:parque; tabla 59531, fila «Viviendas vacías», total nacional. Definición INE: sin contrato o consumo inferior al de una vivienda media ocupada 15 días al año (docs/v16/fuentes/renta_parque.md, ficha 3).

### V16-HEC-VACIAS-PCT-2021
<a id="v16-hec-vacias-pct-2021"></a>

- **Definición.** Vacías por consumo eléctrico sobre viviendas familiares, Censo 2021 (%; 2021; España).
- **Fuentes.** Censo 2021 consumo eléctrico; Censo 2021 (grupos: censo).
- **Capa C4.** Las «vacías del Censo» solo se publican en la tabla 59531 (consumo eléctrico), que es una tabla del propio Censo 2021 con el mismo universo (26.623.708 viviendas, comprobado). Las vacías del Censo y las vacías por consumo eléctrico son la misma cifra: no son independientes. Fuente única: C4. Las vacías por consumo y el uso esporádico son subconjuntos de las no principales (78% de ellas).
- **Tolerancia.** no aplica (fuente única o descriptivo)
- **Cálculo reproducible.** vacías / total de viviendas, ambas del Censo 2021.
