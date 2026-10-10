# Regla de elección del modelo H7 (fijada ANTES de ejecutar la comparación; rama BM)

Fecha: 2026-10-10. Se escribe antes de ejecutar `bm_run.py` y se versiona en el mismo commit que `presupuesto.json`.

## Qué se elige
UN modelo por objetivo (A: nacional ln IPV real; B: panel provincial IPC alquiler; C: panel provincial p_tasado real), entre los **candidatos con variables** (las líneas base AR(4) y ECM v1 no son candidatas):
- A: ARDL, elastic net (10 configuraciones), post-lasso plug-in, ECM de umbral (2), BVAR Minnesota (5), TVP-VAR con olvido (2).
- B y C: elastic net (10), post-lasso plug-in, random forest (4), LightGBM (4) y, si se ejecuta el bloque 5, elastic net con factor común (2).
Las proyecciones locales por periodo y los contrastes PDS son inferencia, no candidatos.

## Métrica de elección (solo validación en bloques de ENTRENAMIENTO)
- Bloques: `v2_common.block_splits`, h=4, primer test 2012Q1, bloques de 4 orígenes, embargo 4, ventana expansiva (los mismos de las líneas base).
- Muestra común: orígenes (unidad, periodo) con predicción en AR(4), ECM v1 y el candidato. Un candidato que cubra < 90 % de la muestra AR(4)∩ECM v1 queda excluido de la elección (cobertura insuficiente) y se informa.
- Métrica: RMSE medio en bloques = media simple, sobre los bloques de test, del RMSE de cada bloque en la muestra común de los candidatos que cumplen la cobertura. Gana el de menor valor.
- Empate: si varios candidatos están a menos de un 1 % relativo del mínimo, gana el más simple según este orden de clase: ARDL = post-lasso (1) < elastic net (2) < ECM de umbral = BVAR (3) < TVP-VAR (4) < random forest (5) < LightGBM (6). Dentro de una clase, la primera configuración de la rejilla declarada (de menor a mayor flexibilidad).
- La elección NO depende de si el candidato supera a AR(4)/ECM v1 en entrenamiento. Sesgo de selección: el mínimo sobre las configuraciones es optimista; por eso la decisión se toma en la muestra sellada.

## Evaluación sellada (una sola vez, la ejecuta el orquestador con `holdout.evaluate`)
- Orígenes 2023Q3-2025Q2 (8; objetivos 2024Q3-2026Q2). Se aborta si hay < 8 periodos.
- Pendientes/parámetros: SOLO con unidades de entrenamiento y objetivos <= 2024Q2. Las 3 provincias selladas (11, 16, 45) reciben su efecto fijo propio, estimado con su historia <= 2024Q2 (idéntico en modelo, AR(4) y ECM v1).
- B y C: contraste principal con las 52 provincias; A: serie nacional (n = 8).
- Para cada objetivo: DM-HLN (h=4, pérdida cuadrática) del modelo frente a AR(4) y frente a ECM v1.
- Objetivo "cumple" si RMSE(modelo) < RMSE(AR4) y RMSE(modelo) < RMSE(ECM v1) y p_IUT = max(p_AR4, p_ECM) < alfa tras Holm sobre los 3 objetivos (alfa = 0,05).
- H7 se cumple si algún objetivo cumple. Este Holm (m=3) es intra-H7; el Holm de las 7 confirmatorias lo aplica el orquestador. Secundarios informativos: 52 vs 49 provincias, solo selladas, ventana de entrenamiento.
- Nivel de evidencia tras el sellado: ASOCIACIÓN ROBUSTA como máximo si H7 se cumple (predictivo, no causal); si no, EXPLORATORIO. Las importancias (permutación, SHAP, ALE) son siempre EXPLORATORIO.
