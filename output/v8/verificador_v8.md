# Verificador V8 (por qué ha subido la vivienda: factores, periodos y factor común)

Generado por `src/v8/f6_verificador.py`. Cada ficha evalúa una afirmación, nunca a quien la formula, y se aplican las mismas reglas a todas. Complementa el verificador principal (output/v5/verificador) y las fichas de V7 (output/v7_1/verificador_v7_1.md), cuyos recuentos no cambian. Capas: C3s = identificación por restricciones de signo y de cero explícitas, válida solo bajo ellas; C4 = exploratorio o asociación. Las cifras llevan el id de `cifras_clave` (campo «ids_cifras»).

## V8-V1 · Tipos de interés y crédito

**Afirmación evaluada:** Los tipos de interés bajos y el crédito abundante explican la subida del precio de la vivienda de compra.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C3s)

**Magnitud:** SVAR de 7 variables (C3s, condicionado a las restricciones de signo y de cero de M2): contribución de crédito y tipos a la variación del precio real de compra, media y banda del 68 %: P2 -8,6 pp (-18,9 a 0,54 pp); P4 -1,3 pp (-4,7 a 4,4 pp); P5 -0,47 pp (-2,8 a 12,8 pp) (versión larga en P1: 3,0 pp (-7,2 a 14,0 pp)). Las cinco bandas incluyen el 0. H8-2 (en P5, contribución negativa de crédito y tipos a la compra): p de Holm 0,987, no respaldada. Instrumento externo (shocks monetarios del BCE, H8-5): F efectivo 1,83 (umbral 10), instrumentos que cumplen las condiciones de C3: 0 de 3; sin lectura causal (C4).

**Intervalo:** Bandas del 68 % de la contribución (por periodo); intervalo al 95 % de H8-2: -15,4 a 27,4 pp

**Límites:** Las magnitudes del SVAR pueden estar atenuadas (solo restricciones de impacto en V3); el instrumento monetario es débil; el signo positivo del tipo real con el precio en el multiverso no se lee como efecto (la inflación entra en el tipo real y en el deflactor del precio, y no se descarta el sentido inverso); no se designa ningún factor como el más relevante en ningún periodo.

**Regla:** Con capa C3s los resultados valen solo condicionado a las restricciones de signo y de cero de M2; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se puede ni respaldar ni descartar con este diseño.

**Literatura:** Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).

**Evidencia:** output/v8/M2/resumen.md; output/v8/M5/resumen.md; output/v8/F5/fichas.md; docs/v8/hipotesis.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-H8-2-est, V8-H8-2-pholm, V8-H8-5-F, V8-M5-c3, V8-REGLA-a-P1, V8-REGLA-a-P2, V8-REGLA-a-P3, V8-REGLA-a-P4, V8-REGLA-a-P5, V8-REGLA-c-P1, V8-REGLA-c-P2, V8-REGLA-c-P3, V8-REGLA-c-P4, V8-REGLA-c-P5, V8-SVAR-c-P1-credito_tipos-media, V8-SVAR-c-P2-credito_tipos-media, V8-SVAR-c-P4-credito_tipos-media, V8-SVAR-c-P5-credito_tipos-media

## V8-V2 · Demografía e inmigración

**Afirmación evaluada:** El crecimiento de la población y la inmigración explican sobre todo la subida del alquiler.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C3s)

**Magnitud:** SVAR (C3s, condicionado a las restricciones de signo y de cero de M2): contribución de la demografía a la variación del alquiler real, media y banda del 68 %: P2 0,33 pp (-1,9 a 2,7 pp); P3 0,00 pp (-2,9 a 2,7 pp); P5 0,07 pp (-1,9 a 2,1 pp). H8-1 (en P5, contribución positiva de la demografía al alquiler): p de Holm 0,987, no respaldada. Multiverso (C4, asociación): 2 de 74 combinaciones cumplen la regla por familias, ambas de demografía en el alquiler (periodo P2 y periodo completo, signo positivo); por variables, 18 de 200. La población total y la extranjera son casi colineales (correlación 0,91 en la muestra completa), de modo que sus filas no son pruebas independientes. Instrumento de empuje migratorio (H8-7): F efectivo 0,05, no cumple C3. Contabilidad hogares-viviendas (asociación): vota a favor de la demografía en 2 celdas (compra P3 y P5).

**Intervalo:** Bandas del 68 % de la contribución (las tres citadas incluyen el 0)

**Límites:** Demografía y oferta no se separan en la contabilidad; población total y extranjera colineales; el instrumento migratorio tiene 20 observaciones anuales y F muy bajo; la asociación del multiverso no distingue causa de comovimiento.

**Regla:** Con capa C3s los resultados valen solo condicionado a las restricciones de signo y de cero de M2; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se puede ni respaldar ni descartar con este diseño.

**Literatura:** Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).

**Evidencia:** output/v8/M2/resumen.md; output/v8/M5/resumen.md; output/v8/M7/resumen.md; output/v8/M4/resumen.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-H8-1-pholm, V8-H8-7-F, V8-M4-voto-demografia, V8-M6-colpob-completo-corr, V8-M7-combinaciones, V8-M7-cumplen, V8-M7-var-cumplen, V8-M7-var-total, V8-SVAR-a-P2-demografia-media, V8-SVAR-a-P3-demografia-media, V8-SVAR-a-P5-demografia-media

## V8-V3 · Viviendas turísticas

**Afirmación evaluada:** El turismo y las viviendas de uso turístico explican la subida del alquiler.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** El factor de turismo no entra en el SVAR (M2). Solo hay datos utilizables en 6 de 17 CCAA y para P4 y P5. Sensibilidad no principal (valores ausentes nativos de LightGBM), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional. Contraste del modelo de aprendizaje automático (C4, no es un efecto): contribución SHAP media del turismo al alquiler, con banda del 68 %: P4 0,11 pp (-0,53 a 0,30 pp); P5 -0,44 pp (-0,67 a 0,23 pp); en la compra, P4 1,5 pp (0,13-2,2 pp) y P5 15,2 pp (8,1-14,8 pp). Ninguna de estas cifras es la variante principal.

**Intervalo:** Bandas del 68 % del bootstrap de bloques (el punto puede quedar fuera de la banda)

**Límites:** Sin identificación, cobertura parcial y periodos P1-P3 sin datos de turismo; SHAP describe cómo el modelo usa la variable y no identifica efectos. Véanse las fichas anteriores sobre viviendas turísticas (v3, v6) para el análisis municipal.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE.

**Literatura:** No aplica.

**Evidencia:** output/v8/M9/resumen.md; output/v8/F5/fichas.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-M9-shap-a-P4-turismo, V8-M9-shap-a-P5-turismo, V8-M9-shap-c-P4-turismo, V8-M9-shap-c-P5-turismo, V8-M9-turismo-ccaa

## V8-V4 · Compradores extranjeros

**Afirmación evaluada:** La demanda de compradores extranjeros es el principal motor de la subida del precio de la vivienda.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** En V8 la demanda externa solo se contrasta con aprendizaje automático (C4, no es un efecto), en el panel de 17 CCAA: contribución SHAP media a la variación del precio real de compra, con banda del 68 %: P3 -0,24 pp (-0,44 a 0,09 pp); P5 0,51 pp (0,10-0,71 pp); al alquiler en P5 -0,22 pp (-0,21 a 0,01 pp) (en el alquiler de P5 el punto queda fuera de su banda del 68 %: el punto SHAP no es el centro de la banda bootstrap). No es un shock identificado en el SVAR. El peso de las compraventas con comprador extranjero (cifra de v4, C4, id compradores_extranjeros en cifras_clave) no mide su efecto sobre el precio.

**Intervalo:** Bandas del 68 % del bootstrap de bloques

**Límites:** Sin identificación; fuentes de compradores extranjeros no independientes entre sí; la demanda externa es colineal con tipos y actividad.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE.

**Literatura:** No aplica.

**Evidencia:** output/v8/M9/resumen.md; output/v8/F5/fichas.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-M9-shap-a-P5-demanda_externa, V8-M9-shap-c-P3-demanda_externa, V8-M9-shap-c-P5-demanda_externa

## V8-V5 · Oferta de vivienda

**Afirmación evaluada:** La falta de construcción (oferta insuficiente) explica la subida del precio de la vivienda.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C3s)

**Magnitud:** SVAR (C3s, condicionado a las restricciones de signo y de cero de M2): contribución de la oferta a la variación del precio real de compra, media y banda del 68 %: P2 -4,8 pp (-13,3 a 2,5 pp); P4 -0,80 pp (-4,8 a 3,3 pp); P5 1,9 pp (-3,3 a 9,0 pp); al alquiler en P4 -1,6 pp (-3,6 a 0,10 pp). En el largo plazo (M4), el ARDL con cotas rechaza la no cointegración en 2 de 9 especificaciones (asociación, C4), y la que añade la oferta es inconcluyente.

**Intervalo:** Bandas del 68 % de la contribución

**Límites:** La oferta y la demanda específica de vivienda se identifican por signos opuestos en el precio y las compraventas; el signo estimado no distingue por sí mismo escasez de otros canales.

**Regla:** Con capa C3s los resultados valen solo condicionado a las restricciones de signo y de cero de M2; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se puede ni respaldar ni descartar con este diseño.

**Literatura:** Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).

**Evidencia:** output/v8/M2/resumen.md; output/v8/M4/resumen.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-M4-ardl-rechaza, V8-M4-ardl-total, V8-SVAR-a-P4-oferta-media, V8-SVAR-c-P2-oferta-media, V8-SVAR-c-P4-oferta-media, V8-SVAR-c-P5-oferta-media

## V8-V6 · Empleo y renta

**Afirmación evaluada:** La mejora del empleo y de la renta explica la subida del precio de la vivienda.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C3s)

**Magnitud:** SVAR (C3s, condicionado a las restricciones de signo y de cero de M2): empleo y renta es el factor con mayor contribución media en compra P1 (versión larga): 31,8 pp (9,0-54,6 pp), con P(f*) = 71,7 % y 1 de 4 votos; en P5 7,2 pp (-4,7 a 11,2 pp). H8-3 (en P3, contribución positiva de actividad y renta a la compra): estimación 7,7 pp (-22,8 a 40,0 pp) y p de Holm 0,838, no respaldada. M0 (exploratorio): 2 de 70 coeficientes cumplen la regla de §8 (30 evaluables; la del alquiler es «no evaluable», no incumplida) y ninguno sobrevive a BH.

**Intervalo:** Bandas del 68 % de la contribución; intervalo al 95 % de H8-3: -22,8 a 40,0 pp

**Límites:** Empleo y renta compite con demografía y crédito; P1 usa una versión de 4 variables desde 1995T2; no se designa factor en ningún periodo.

**Regla:** Con capa C3s los resultados valen solo condicionado a las restricciones de signo y de cero de M2; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se puede ni respaldar ni descartar con este diseño.

**Literatura:** Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).

**Evidencia:** output/v8/M2/resumen.md; output/v8/M0/resumen.md; output/v8/F5/fichas.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-H8-3-est, V8-H8-3-pholm, V8-M0-coef, V8-M0-cumplen, V8-M0-evaluables, V8-PFSTAR-c-P1, V8-SVAR-c-P1-empleo_renta-media, V8-SVAR-c-P5-empleo_renta-media, V8-VOTOS-c-P1

## V8-V7 · Factor europeo

**Afirmación evaluada:** La subida en España forma parte de un movimiento común europeo del precio de la vivienda.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** El factor común español covaría positivamente con el crecimiento del precio de la vivienda de la zona euro (EA19): correlación 0,60 (0,14-0,86) (H8-9; p de Holm 0,020, rechazada la ausencia de relación; la zona euro incluye a España). En compra P2, la parte asociada al precio europeo es -15,3 pp (-21,7 a -7,6 pp). En cambio, H8-8 (el componente común de las 17 CCAA explica más del 50 % de la varianza en cada periodo) no se rechaza: cuota mínima 45,3 %, p de Holm 0,669. Todo es asociación estadística (C4): un factor común resume comovimiento, no una causa.

**Intervalo:** Intervalo al 95 % de la correlación: 0,14-0,86; bandas del 68 % de la parte europea

**Límites:** La zona euro sin España no es construible con los pesos oficiales (se usa una aproximación de 5 países como sensibilidad); con 17 CCAA y pocos trimestres la cuota del primer componente está sesgada al alza.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE.

**Literatura:** No aplica.

**Evidencia:** output/v8/M1/resumen.md; output/v8/F5/fichas.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-H8-8-est, V8-H8-8-pholm, V8-H8-9-est, V8-H8-9-pholm, V8-M1-eur-c-P2

## V8-V8 · Un factor único

**Afirmación evaluada:** Hay un único factor que explica la subida de la vivienda en cada periodo y se puede identificar.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C3s)

**Magnitud:** Regla de §9 (tres de cuatro métodos, multiverso orientado ≥ 80 % y banda del 68 % del SVAR que excluya el 0), fijada antes de calcular: se designa un factor en 0 de 10 celdas (mercado, periodo). Cuota no atribuida (parte determinista y no identificada del SVAR), compra P1: 0,42 (-0,08 a 0,98) de la variación; compra P5: 0,52 (-0,79 a 1,3). Ejemplo de ranking incierto: en compra P3, P(f*) del primero = 40,8 %.

**Intervalo:** Bandas del 68 % de la cuota no atribuida (fracción de la variación observada)

**Límites:** No designar un factor no prueba que no exista uno dominante; indica que los métodos no coinciden con la incertidumbre actual. P4 (9 trimestres) y alquiler P1 (sin datos) no se designan por regla.

**Regla:** Con capa C3s los resultados valen solo condicionado a las restricciones de signo y de cero de M2; ninguna regla de V8 designa un factor (0 de 10 celdas), de modo que la afirmación no se puede ni respaldar ni descartar con este diseño.

**Literatura:** Método: SVAR bayesiano con restricciones de signo y de cero (Rubio-Ramírez, Waggoner y Zha, 2010; Arias, Rubio-Ramírez y Waggoner, 2018). Referencias NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes).

**Evidencia:** output/v8/F5/resumen.md; output/v8/F5/fichas.md; docs/v8/desviaciones.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-PFSTAR-c-P3, V8-QNA-c-P1, V8-QNA-c-P5

## V8-V9 · Capacidad predictiva

**Afirmación evaluada:** Los modelos econométricos y de aprendizaje automático predicen el precio y el alquiler mejor que un modelo sencillo.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** Tabla común fuera de muestra (2016T2-2026T1, misma muestra, embargo de 4 trimestres), RMSE del crecimiento trimestral real de compra: AR(4) 1,2 pp; ECM v1 2,6 pp; BVAR de M2 1,4 pp. Alquiler: AR(4) 0,80 pp; ECM v1 1,7 pp; BVAR 0,98 pp. Ningún modelo supera a la base más exigente (el AR(4)); el ECM v1 es peor con p de Holm 0,012 (compra). M9 (nacional, compra): mejor modelo de aprendizaje automático 2,2 pp frente a 1,1 pp del AR(4); modelos que superan a la base tras BH: 0.

**Intervalo:** Contraste Diebold-Mariano con corrección de Harvey-Leybourne-Newbold; p ajustados por Holm

**Límites:** El bloque de prueba es corto (40 trimestres); explicar y predecir son tareas distintas (un modelo puede ser útil para atribuir sin predecir mejor).

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE.

**Literatura:** No aplica.

**Evidencia:** output/v8/F5/fuera_muestra_comun.csv; output/v8/M9/resumen.md; output/v8/F6/hechos.json; docs/v8/plantillas/README.md

**Ids de cifras:** V8-M9-oos-c-nacional-base, V8-M9-oos-c-nacional-mejor, V8-M9-oos-c-nacional-ml, V8-OOS-a-ar4-rmse, V8-OOS-a-bvar_m2-rmse, V8-OOS-a-ecm_v1-rmse, V8-OOS-c-ar4-rmse, V8-OOS-c-bvar_m2-rmse, V8-OOS-c-ecm_v1-pholm, V8-OOS-c-ecm_v1-rmse
