# K1: lineas base exigentes. Notas y limitaciones (2026-10-11, capa C4)

## Lineas base nuevas (src/v6/m4_lineas_base.py, fuera de make; apertura unica `k1_<tarea>__<linea>` con evaluate_v6)
- Factor f_t = media, entre provincias NO selladas, de la media provincial de dy (cada provincia pesa igual; en municipio y distrito se promedia antes dentro de la provincia). Es el factor NACIONAL de entrenamiento: para provincias selladas no existe factor provincial propio; municipio y distrito usan el mismo factor nacional.
- (a) ult_crec_nac: y_(t-1) + f. Variante factible: f_(t-1). Variante oraculo: f_t. En el grupo espacial f_t existe en el entrenamiento (otras provincias, mismo periodo) pero no seria conocible al predecir; en los grupos temporal y conjunto f_t se obtiene de las filas de provincias no selladas del ultimo periodo (realizado): por eso es oraculo.
- (b) ar_factor: dy_it = a_i + b dy_i,t-1 + c f_(t-1) (+ d f_t en oraculo); EF de unidad intra, coeficientes solo con entrenamiento.
- (c) twfe: dy_it = a_i + lambda_t; prediccion y_(t-1) + a_i + lambda_(t-1) (factible) o lambda_t (oraculo). Para periodos sin lambda estimado (>= corte) lambda = f - media(a_i).
- Efecto de unidad inexistente (provincia sellada, unidad nueva): media de los efectos de unidad de entrenamiento; las CCAA selladas lo estan enteras, no hay efecto de CCAA. Sin prediccion posible -> persistencia (n_fallback_persistencia).
- Los valores del factor en periodos >= corte salen de filas de provincias no selladas dentro de la ventana sellada; entran solo como dato (f_(t-1) pasado en factible, f_t realizado en oraculo), nunca para estimar.

## Reanalisis (src/v6_1/k1_run.py, entra en make)
- Base exigente = menor RMSE espacial entre persistencia, AR por unidad, ECM v1, M1 econ y las tres nuevas factibles. Oraculos aparte, nunca definen la base exigente.
- DM-HLN (h=1, celdas provincia-periodo; version por periodo en tabla_largo_k1.csv) y permutacion por inversion de signo por provincia, EXACTA (los 2^11 = 2.048 patrones; p minimo 1/2.048 = 0,00049), una cola; Holm por tarea y grupo (revision R-03).
- Clase por grupo espacial; los demas grupos se reportan sin modificar la clase.

## Limitaciones
- Segunda mirada a la misma muestra sellada para NUEVOS comparadores (D3 de v6.1); las predicciones de los modelos de v6 no cambian. La base exigente se elige mirando el sellado (optimismo a favor de la base, no del modelo).
- 11 provincias selladas (10 con datos municipales): poca potencia; "no distinguible" no es equivalencia.
- El mejor modelo se elige por RMSE sellado (optimista). Prediccion no es causalidad: nada causal desde importancias.
- Temporal y conjunta: ultimo periodo solo (1 anio o 4 trimestres), validacion ya vista en parte en v2.
- (Revision R-01) El DM-HLN por celdas trata como independientes provincias del mismo periodo, que estan correlacionadas; es anticonservador. Por eso la tabla principal incluye el DM por periodo (p_dm_hln_per_holm) y la clase exige ademas la permutacion por provincia.
- (Revision R-02) Una tarea en «predice mejor» cuyo DM por periodo no es significativo se rotula «fragil» (PROV_PRECIO_ANUAL).
- (Revision R-04) Las clases «peor» de los grupos temporal, conjunta y total heredan el sesgo de elegir la base mirando el sellado; no se interpretan como inferioridad demostrada.
- (Revision R-05) En m4_lineas_base.py el factor se calcula antes de filtrar anio < corte. Hoy no tiene efecto (tr solo contiene entrenamiento). El script no se puede re-ejecutar (aperturas unicas), asi que solo se anota.
- (Revision R-06) Sensibilidad con Holm sobre las 9 tareas en tabla_modelos_k1.md.
