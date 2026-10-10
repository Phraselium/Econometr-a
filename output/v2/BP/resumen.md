# Rama BP (política de vivienda): resumen

Todos los resultados son de entrenamiento (≤2024Q2). Semilla 20261010. `evaluar_H6` NO se ha ejecutado ni se ha tocado data/sealed.

## H5 (confirmatoria): tope de rentas catalán (Ley 11/2020), 4 tratadas vs 45 donantes, 2016Q1-2023Q4
Resultado principal: ln IPC alquiler; Synthetic DiD propio (Arkhangelsky et al. 2021); EE y p por permutación espacial (4 donantes aleatorios, B=1000).

| Efecto (ln) | SDiD | IC95 (placebo) | p perm. bilateral | SC | DiD |
|---|---|---|---|---|---|
| 2020Q4-2022Q1 (tope vigente) | +0,0037 | [-0,0002; +0,0076] | 0,065 (una cola "−": 0,97) | +0,0053 | +0,0191 |
| 2022Q2-2023Q4 (tras la anulación) | +0,0055 | [-0,0059; +0,0170] | 0,358 | +0,0073 | +0,0250 |

* Signo contrario al esperado (−); con Δ4 ln el SDiD da +0,0006 (p=0,77) y −0,0012 (p=0,70). No hay evidencia de que el tope redujera el IPC de alquiler provincial.
* **Diagnósticos de identificación: no se superan.** Placebo en el tiempo (fecha falsa 2018Q4): τ=+0,0078, p=0,009 (no nulo). Pendiente de pretendencia SDiD p=0,040 (RMS p=0,14); con pesos uniformes p=0,010: las tratadas ya crecían distinto antes del tope. El DiD y SC "significativos" (positivos) son compatibles con esa divergencia previa, no con un efecto del tope.
* Por provincia (SDiD, permutación exacta con 45 donantes): ninguna negativa y significativa en la ventana del tope (08: −0,0014, p=0,74).
* Nivel de evidencia: **EXPLORATORIO** (en el código, la etiqueta solo podría ser "candidata a CAUSAL, pendiente de Holm-7 y submuestras" si se superaran todos los tests) (no CAUSAL: fallan pretendencias y placebo de tiempo; ni siquiera p<0,05 con signo −). Holm-7 queda para BS (p sin ajustar 0,065 bilateral).
* Fuera de muestra: no aplica la comparación con AR(4)/ECM v1. Diagnóstico pseudo-OOS (pesos ≤2018Q3, objetivos 2018Q4-2020Q3, Δ4 medio de las 4 tratadas): RMSE sintético 0,0063 vs AR(4) de panel 0,0043 (DM-HLN p=0,50, n=8; el sintético usa donantes contemporáneos, no es un duelo de predicción). Ajuste en muestra de la brecha de nivel: RMSE 0,0011 (SDiD).

## H6 (confirmatoria, solo preparación)
`src/v2/bp_h6_sellado.py::evaluar_H6` fija el diseño: 40 donantes (49 − 4 catalanas − 01, 20, 48, 31, 15), pesos ajustados con ≤2023Q4, 2024Q1-Q2 y el periodo del tope excluidos del ajuste, efecto 2024Q3-2026Q2, regla "τ<0 y p de permutación bilateral<0,05". Ensayo en seco (tests/test_bp_h6_sellado.py, pseudo-sellado con entrenamiento): sin efecto τ=−0,0045, p=0,44 (no cumple); con efecto inyectado −0,03: τ=−0,0345, p=0,005 (cumple). Potencia aproximada: SD del efecto placebo 0,0062, efecto mínimo detectable ≈0,017 en ln (~1,7 %).

## Declaración ex ante (antes de abrir H6): potencia, lectura y riesgos
* Efecto mínimo detectable (80 %, bilateral): H6 ≈ 1,7 % en ln IPC de alquiler (2,8 × DE placebo 0,0062); H5 ≈ 0,56 % (2,8 × 0,0020).
* El IPC de alquiler del INE mide las rentas de todos los contratos vigentes (el parque); el tope y las zonas tensionadas actúan sobre todo en contratos nuevos y solo en los municipios declarados. Referencia de magnitud en contratos nuevos: Jofre-Monseny, Martínez-Mazza y Segú (2023, Regional Science and Urban Economics 101, 103916): rentas de contratos nuevos de orden 4-6 % menores en municipios regulados (según el resumen publicado; cuartil no verificado). Un no rechazo se leerá como "no detectable en el IPC provincial", no como "sin efecto".
* Riesgos: (a) anticipación (Resolución TER/2940/2023, agosto de 2023; λ probablemente concentrado en 2023Q4: sesgo hacia 0); (b) paquete catalán coetáneo (DL 3/2023 de viviendas de uso turístico, 2.ª ronda de zonas desde 2024-10-10): H6 mide "Cataluña 2024-2026", no la zona tensionada aislada; (c) contratos del tope aún en el parque en el pre 2022Q2-2023Q4; (d) choques nacionales (tope del 3 % en 2024, IRAV desde 2025); (e) la inferencia placebo supone unidades intercambiables (probablemente conservadora, pues Barcelona reduce el ruido del agregado) y el jackknife es poco fiable con 4 tratadas; (f) los pesos de zona_tensionada_share pueden venir de un año de stock sellado (solo secundario). Secundario informativo añadido: SDiD sin 2023Q3-Q4 en el pre.
* Orden de cálculo de evaluar_H6: PRINCIPAL y DECISION primero; secundarios en try/except. Debe lanzarse con OMP_NUM_THREADS=1 y timeout amplio (≈1 min con B=1000; ≈7 s con B=100); si se corta, H6 queda quemada.

## Exploratorio descriptivo (sin inferencia ni control)
* RDL 7/2019: Δ4 ln IPC alquiler nacional medio 0,83 % (2017-18) vs 1,48 % (2019Q2-2020Q1).
* Ley 12/2023: 1,06 % (2021Q3-2022Q4) vs 2,05 % (2023Q3-2024Q2); coincide con tipos/inflación y topes de actualización; no se atribuye a la ley. Zonas tensionadas municipales con SERPAVI: no aplica (SERPAVI termina en 2023).

## Qué NO se puede afirmar
Nada sobre la oferta de alquiler (no hay datos de oferta ni de contratos), sobre precios de compra, ni sobre el efecto en los municipios con tope (el IPC provincial diluye el tratamiento y mide el parque de contratos, no solo los nuevos). No se puede afirmar que el tope no tuviera efecto local; solo que no se detecta en el IPC provincial con este diseño y que las pretendencias no son paralelas. Nada sobre H6 hasta su evaluación sellada.
