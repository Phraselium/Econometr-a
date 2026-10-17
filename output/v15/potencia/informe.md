# V15 · Potencia por pregunta candidata (fase 1.3)

Generado con `python3 src/v15/f1_potencia.py`: 500 réplicas placebo, SEED=20261010. La tabla completa está en [potencia.csv](potencia.csv) y el método en docs/v15/decisiones.md (G5). **Recalculado el 2026-10-17 tras marcar las filas sub-provinciales de las provincias de v6** (docs/v15/contaminacion_v6.md): los paneles excluyen esas 11 provincias, como el entrenamiento de V15. No se estima ningún efecto: los tratamientos y exposiciones placebo son independientes del resultado. P6 usa solo trimestres anteriores a la primera zona tensionada.

MDE80 es el efecto mínimo detectable con potencia del 80 % y contraste bilateral al 5 %, igual a 2,8 × la desviación típica placebo. «Rechazo placebo» es la tasa de rechazo al 5 % con errores agrupados; debería rondar 0,05.

| Pregunta | Panel de resultado | Unidades · T | MDE80 | Rechazo placebo | Lectura provisional |
|---|---|---|---|---|---|
| P6 topes y ZT (Cataluña) | Incasòl, renta media de contratos nuevos, trimestral | 287 municipios (244 «tratados» placebo) · 20 trimestres previos | 2,2 log puntos | 0,20 con 4 provincias; 0,050 por municipio | **Con potencia** frente a la referencia de V9-D1b (−5,9 %). Agrupar por municipio; 4 provincias no bastan |
| P6b número de contratos (Cataluña) | Incasòl, log(1 + contratos nuevos), trimestral | 541 municipios (270 «tratados» placebo) · 20 trimestres previos | 3,9 log puntos | 0,038 por municipio | **Con potencia** frente a la referencia de −13 % (Pérez García 2026, preprint) |
| P6 (España) | SERPAVI €/m², colectiva | 1.498 municipios · 13 años, 1 posterior | 1,4 log puntos | 0,050 | Con potencia estadística, pero mide el stock de contratos y solo tiene 2024 como año posterior: robustez |
| P4 inmigración (municipal) | SERPAVI €/m² | 1.673 municipios · 4 años (2021-2024) | 0,82 log puntos por 1 DT | 0,072 | Precisión suficiente; T = 4. El límite es la identificación (shift-share con pocos orígenes), no la varianza |
| P4 (municipal, padrón 2003-2022) | SERPAVI €/m² | 1.452 municipios · 12 años (2011-2022) | 0,83 log puntos por 1 DT | 0,116 | Precisión suficiente; con las provincias de entrenamiento la inferencia sobrerrechaza algo con exposición espacialmente correlacionada: usar AKM o bootstrap salvaje |
| P4 (València) | SERPAVI por sección | 584 secciones · 14 años | 1,1 log puntos por 1 DT | 0,072 (19 distritos) | Con potencia si la exposición por barrio varía. Inferencia AKM por orígenes |
| P5 pisos turísticos (Barcelona) | SERPAVI por sección | 1.058 secciones · 14 años | 0,67 log puntos por 1 DT | 0,106 (10 distritos) | Precisión suficiente; con 10 distritos la inferencia sobrerrechaza: agrupar por barrio (73) o bootstrap salvaje |
| P5 (España, por sección) | SERPAVI por sección; exposición: % de viviendas turísticas INE (código INE) | 15.112 secciones · 4 años (2021-2024) | 0,53 log puntos por 1 DT | 0,052 (por municipio) | **Con potencia** e inferencia correcta agrupando por municipio; T corto |
| P5 (C. Valenciana) | SERPAVI €/m² | 255 municipios · 10 años | 0,71 log puntos por 1 DT | 0,048 | Con potencia; la exposición reconstruida del registro GVA es un supuesto de fechado y solo vale para robustez |
| P7 demografía y obra nueva | SERPAVI €/m² | 1.673 municipios · 4 años | 0,52 log puntos por 1 DT | 0,092 | Precisión suficiente, pero la auditoría de oferta limita P7 a lo descriptivo (provincial desde 2018, municipal 2021-2025) |
| P10 espacial | SERPAVI, Δlog 2015-2024 (corte) | 1.436 municipios | 2,8 log puntos por 1 DT | 0,128 | Corte transversal único; los efectos indirectos dependen de W. Exploratorio |
| P1 oferta | Valor tasado, Δlog 2013-2024 (corte) | 38 provincias | 6,5 log puntos por 1 DT | 0,084 | **Sin potencia y sin datos**: no hay restricciones físicas en el repositorio ni precio de compra municipal en la base |
| P3 tipos (valor tasado) | Proyección local nacional | 117 / 113 trimestres (h = 4 / 8) | 1,2 / 2,5 log puntos por 1 DT de sorpresa | — | Serie única sin exposición regional. La comparación con magnitudes de la literatura se hace en la fase 2 |
| P3 tipos (IPV) | Proyección local nacional | 69 / 65 trimestres | 2,2 / 4,5 log puntos por 1 DT | — | Peor que con valor tasado: menos T |
| P9 predicción | DM frente al AR(4), Δlog valor tasado | 73 errores recursivos desde 2008 | 18 % (ρ = 0,9) a 30 % (ρ = 0,7) de reducción del ECM | — | Solo detecta mejoras grandes. Con la muestra sellada nueva (pocos trimestres) la potencia será menor: el nulo es el resultado esperado |
| P8 distribución | ECV, cambio 2018-2025 de la brecha española / fuera de la UE | ~97.000 personas | 9 a 15 puntos porcentuales | — | **Sin potencia para cambios** en la brecha; solo descriptivo de niveles (ya publicado en V12-B6) o reponderación DFL como C4 |

P2 (fundamentales y cointegración en panel) no tiene un efecto mínimo detectable en este sentido: 38 provincias, 126 trimestres de valor tasado. La potencia de CIPS, Westerlund y CS-ARDL con ese N y ese T se valida por Monte Carlo después de la puerta, según el plan (montecarlo, fase 4).

## Consecuencias para la fase 3 (provisionales; se cierran con la literatura)
- **Descartadas por potencia o por datos:** P1, porque no hay restricciones físicas ni precio municipal (lo confirma la auditoría de oferta y parque), y P8 como contraste de cambios (queda como descriptiva).
- **Con potencia, sujetas a identificación:** P6 (contratos nuevos de Incasòl, por municipio), P5 (Barcelona y C. Valenciana), P4 (València por sección) y P2.
- **Con potencia baja anunciada:** P3 y P9. Se mantienen solo si la literatura sugiere magnitudes del orden de los MDE, o como nulo bien identificado.
- **Exploratorias:** P7 y P10.
