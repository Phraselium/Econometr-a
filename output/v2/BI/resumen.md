# BI · inmigración y vivienda (H3) · resumen

Muestra: 621 observaciones provincia-año (49 provincias, 2009-2021), idéntica para alquiler, compra y contraste. SEED 20261010. Todas las especificaciones están en `registro.csv` (la ejecución de humo 2009-2015 en `smoke_*`).

## H3 (confirmatoria, especificación pre-registrada)

| | beta (2SLS) | EE cluster | IC95 t(48) | p WCB 2 colas | p WCB 1 cola | MCO |
|---|---|---|---|---|---|---|
| Δln IPC alquiler | 3.06 | 0.95 | [1.14; 4.98] | 0.001 | 0.001 | 0.96 (0.23) |
| Δln valor tasado real | -1.04 | 2.51 | [-6.08; 4.00] | 0.671 | 0.662 | 5.07 (0.71) |
| alquiler − compra | 4.10 | 2.20 | [-0.33; 8.52] | 0.051 | 0.029 | -4.11 (0.75) |

Unidades: % de variación anual por cada 1 p.p. de población (flujo/pob t-1). Conjunto de AR de beta_alq: [1.4; 6.0]. Correlación entre ecuaciones (cluster) 0.49; el SE del contraste del sistema apilado (2.202) coincide con el de la regresión de la diferencia.

Contraste conjunto (unión-intersección, p WCB una cola): beta_alq>0 p=0.0010; beta_alq−beta_compra>0 p=0.0294; p_IUT=0.0294. Holm sobre 7 confirmatorias: el p ajustado nunca es menor que (8−rango)·p; cota pesimista Bonferroni-7: beta_alq 0.007 (sobrevive), contraste 0.206 (no sobrevive salvo que las otras seis hipótesis rechacen todas). La corrección final de la familia la aplica el orquestador.

**Nivel de evidencia de H3 tal como se registró (conjunción): EXPLORATORIO.** Por componentes: beta_alq>0 → CAUSAL (regla mecánica); contraste alquiler>compra → EXPLORATORIO.

## Diagnósticos de shift-share

- Primera etapa: F cluster = 14.4 (≥10; con un instrumento y un regresor el F efectivo de Montiel Olea-Pflueger coincide con el F robusto; no se contrasta con valores críticos). Es un F moderado: con tendencias provinciales baja a 5.4.
- Pesos de Rotemberg (8 grupos): sin pesos negativos; Sudamérica pesa 0.68 (F del grupo 52), los dos mayores suman 0.80. La identificación descansa sobre pocas cuotas (sobre todo Sudamérica); África y Europa tienen F por grupo < 2.
- Cuotas 2002 vs. características 2002 (instrumento medio): extranjeros 2002 r=0.56 (p=0.000), paro 2002 r=-0.34 (p=0.018), ln población r=-0.40 (p=0.004), ln precio r=0.07 (p=0.63). **Las cuotas no son independientes de las condiciones iniciales** (amenaza a la exogeneidad de cuotas de GPSS 2020).
- Pretendencias (Δ resultados 2003-2007 sobre el instrumento medio posterior, FE año): alquiler p=0.93, precio p=0.53 (no significativas; con 5 años y 49 clusters la potencia es limitada).
- Sobreidentificación (5 grupos de origen): J de Hansen cluster alquiler p=0.29, precio p=0.12 (no rechaza), pero Sargan homocedástico: alquiler p=0.065, precio p=5.8e-06 (rechaza en precio). Con 5 instrumentos y 49 clusters el J robusto tiene poca potencia. beta_alq con 5 instrumentos: 2.30 (EE 0.60).
- BHJ a nivel de shock (8 grupos × 13 años, EE cluster por grupo, t(7)): alquiler 3.99 (p=0.000); precio 2.90 (p=0.55). **Con 8 grupos la potencia y la inferencia son pobres**; es una comprobación de coherencia, no una prueba.
- EE tipo AKM0 (agrupando por grupo-shock, sin región de similitud de cuotas; aproximación a AKM 2019): alquiler EE 0.74 (p t(7) = 0.004) frente a 0.95 cluster-provincia; precio p=0.81. No es AKM completo.

## Stock vs flujo y timing (EXPLORATORIO)

| spec | resultado | regresor | b | EE | p cluster | F |
|---|---|---|---|---|---|---|
| tendencias_prov | y_alq | x | 3.90 | 1.66 | 0.023 | 5.4 |
| sin_covid | y_alq | x | 2.38 | 0.77 | 0.003 | 14.3 |
| stock_dcuota_extranj | y_alq | x_stock | 1.19 | 0.39 | 0.004 | 13.6 |
| flujo_t-1 | y_alq | x_l1 | 0.80 | 0.57 | 0.164 | 9.7 |
| x_t_y_x_t-1 | y_alq | x | 2.12 | 1.10 | 0.061 | 7.1 |
| x_t_y_x_t-1 | y_alq | x_l1 | 0.52 | 0.66 | 0.434 | 7.1 |
| z_alineado_stock_t+1 | y_alq | x | 2.37 | 0.59 | 0.000 | 29.9 |
| tendencias_prov | y_pre | x | -9.54 | 5.48 | 0.088 | 5.4 |
| sin_covid | y_pre | x | -0.92 | 2.59 | 0.724 | 14.3 |
| stock_dcuota_extranj | y_pre | x_stock | -0.40 | 0.98 | 0.683 | 13.6 |
| flujo_t-1 | y_pre | x_l1 | -6.05 | 3.29 | 0.072 | 9.7 |
| x_t_y_x_t-1 | y_pre | x | 13.29 | 3.07 | 0.000 | 7.1 |
| x_t_y_x_t-1 | y_pre | x_l1 | -7.85 | 2.49 | 0.003 | 7.1 |
| z_alineado_stock_t+1 | y_pre | x | 4.46 | 1.64 | 0.009 | 29.9 |

El efecto sobre el alquiler es positivo en todas las variantes (stock: +1,2 por p.p. de variación de la cuota extranjera; sin COVID y con instrumento alineado ΔS_{t+1}: 2,4), pero con flujo t−1 solo y con x_t y x_{t−1} conjuntos pierde precisión (F 7-10). El efecto sobre el precio de compra cambia de signo entre variantes: no es estable.

## Heterogeneidad (EXPLORATORIO)

- DML (cross-fitting 5 bloques de provincias × 3 repeticiones, EE cluster): PLR lasso 0.30 (p=0.055), PLR RF 0.48 (p=0.0001); PLIV lasso 2.05 (p=0.18), PLIV RF 1.44 (p=0.027). PLR sin FE de provincia, con características 2002 y dummies de año.
- Causal forest (sin instrumento): efecto medio 0.43 [0.08; 0.79]; mayor efecto estimado donde la cuota extranjera 2002 y el precio inicial son altos y el paro 2002 bajo (importancia mayor: cuota extranjera 2002 0.32). La IC del bosque no agrupa por provincia y subestima la incertidumbre.
- Interacciones IV paramétricas (5 características): ninguna significativa (p mínimo 0.35, Holm 1,00). La heterogeneidad del bosque no se confirma con instrumento.
- Presupuesto declarado: 14 configuraciones, 10 usadas (4 DML + 1 bosque + 5 interacciones); hiperparámetros fijos, sin búsqueda.

## Comparación de magnitudes

- Saiz (2007, EE. UU.): entrada del 1 % de la población ≈ +1 % en alquileres. Aquí: 1 p.p. de población ⇒ +3.06 % de alquiler [IC 1.1; 5.0], unas 3 veces mayor; solo el extremo inferior del IC se acerca al valor de Saiz; MCO da 0.96. Unidades y mercado no son estrictamente comparables.
- v1 (F3, 17 CCAA): 2SLS IPC alquiler 0,44 (p cluster 0,16, WCB 0,12); valor tasado −0,88 (p 0,37). Con 49 provincias (más variación y cuotas más finas) el efecto sobre el alquiler es más grande y significativo; la compra sigue sin efecto detectable.

## Fuera de muestra

Anual, 2013-2020 (8 orígenes × 49 provincias, bloques expansivos con embargo 1 año). RMSE AR(4) panel 0.0107; AR(4)+flujo observado en t 0.0094 (DM-HLN 1.43, p=0.20: mejora no significativa); con flujo contemporáneo t+1 (NO es pronóstico) 0.0080 (DM 2.28, p=0.06). ECM v1 solo existe en trimestres: panel_ecm_v1 vs panel_ar4 (h=4, orígenes T4, mismo número de observaciones) RMSE 0.0156 vs 0.0125, DM -1.12 (p=0.30). No es posible añadir la tasa de inmigración (observada o instrumentada) al panel_ar4 trimestral: los flujos terminan en 2021-22 y sin muestra posterior. El instrumento no sirve para predecir (usa información posterior).

## Lo que NO se puede afirmar

- Que el contraste alquiler > compra sea robusto: p WCB una cola 0,03, bilateral 0,05, IC95 del contraste incluye 0 y no sobrevive a Holm sobre 7 (cota 0,21). Es EXPLORATORIO.
- Que la inmigración no afecte al precio de compra: el IC de beta_compra es muy ancho; solo se puede decir que no hay evidencia de efecto con este diseño, y que la estimación cambia de signo entre variantes de timing.
- Que beta_alq sea un efecto causal nítido: pasa la regla mecánica, pero F=14 moderado, identificación concentrada en Sudamérica, cuotas 2002 correlacionadas con extranjeros/paro/población iniciales, Sargan rechaza en precio, 8 grupos limitan BHJ/AKM, y el timing (stock a 1 enero vs flujo anual) no coincide exactamente. Debe leerse como efecto local (LATE) de la variación inducida por enclaves 2002.
- Que el efecto se mantenga tras 2021, en las provincias selladas (11, 16, 45) o en el periodo posterior (sin muestra sellada para H3).
- Que haya heterogeneidad por costa, turismo, tamaño o precio inicial: solo se observa con métodos sin instrumento y no se confirma con interacciones IV.
- Efectos de equilibrio general (salida de nativos, oferta, composición de la demanda) ni efectos sobre cantidades: el diseño estima el efecto reducido-forma sobre precios en la provincia.
- Capacidad predictiva fuera de muestra con inmigración (no hay mejora significativa frente a AR(4); ECM v1 no mejora a AR(4) en alquiler).
