<!-- Generado por `make consulta` (src/consulta/generar.py). No editar a mano: se regenera y un test lo comprueba. -->

# Preguntas frecuentes

Respuestas breves a las preguntas más habituales. Cada cifra se lee de `output/v5/cifras_clave.csv` por su id, con su capa y su fecha; el enlace lleva a la fuente. Capas: [glosario](glosario.md). Reglas para responder: [LEEME_ASISTENTE.md](LEEME_ASISTENTE.md).

### 1. ¿Se puede señalar un único factor como el más relevante en la subida del precio?

No. La regla pre-registrada de V8 no designa ningún factor en ninguno de los diez casos (mercado por periodo). En la compra de 2022 en adelante, el máximo de métodos que coinciden es 2 votos de cuatro.

- `V8-REGLA-c-P5` = 0 designado; capa C4; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-VOTOS-c-P5` = 2 votos; capa C4; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md)

### 2. ¿Cuánto de la subida reciente de la compra es común a todas las comunidades?

En 2022T3-último dato el primer componente común explica 92,79 % (86,65 a 94,92) de la varianza del crecimiento interanual del precio real entre las 17 comunidades. Es la mayor cuota de los cinco periodos (C4, asociación).

- `V8-M1-cuota-c-P5` = 92,79 % (86,65 a 94,92); capa C4; periodo P5 (2022T3-último dato); dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M1/resumen.md](../output/v8/M1/resumen.md)

### 3. ¿Y en el alquiler, en el mismo periodo?

El componente común explica 97,49 % (86,1 a 98,69) de la varianza del crecimiento interanual del alquiler real entre comunidades en 2022T3-último dato. Describe comovimiento territorial, no causa.

- `V8-M1-cuota-a-P5` = 97,49 % (86,1 a 98,69); capa C4; periodo P5 (2022T3-último dato); dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M1/resumen.md](../output/v8/M1/resumen.md)

### 4. ¿Y durante la crisis de 2008-2013, en la compra?

La cuota del factor común fue 45,27 % (42,01 a 54,17) en P2 (2008T3-2013T4), la más baja junto con P4. La subida reciente es más común entre comunidades que la de la crisis.

- `V8-M1-cuota-c-P2` = 45,27 % (42,01 a 54,17); capa C4; periodo P2 (2008T3-2013T4); dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M1/resumen.md](../output/v8/M1/resumen.md)

### 5. ¿Es el factor común más de la mitad de la variación en cada periodo (H8-8)?

No se sostiene. La cuota mínima entre periodos es 45,27 % y el p ajustado por Holm es 0,669. H8-8 exigía más de la mitad en todos los periodos.

- `V8-H8-8-est` = 45,27 %; capa C4; periodo P1-P5; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-H8-8-pholm` = 0,669; capa C4; periodo P1-P5; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md)

### 6. ¿El precio de la vivienda en España acompaña al de la zona euro?

Hay asociación: la correlación del factor común español con el precio de la zona euro es 0,598  (0,135 a 0,858) (p de Holm 0,02). Es la única hipótesis confirmatoria de V8 que se sostiene; es C4, sin lectura causal.

- `V8-H8-9-est` = 0,598  (0,135 a 0,858); capa C4; periodo 2006T1-2026T2; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-H8-9-pholm` = 0,02; capa C4; periodo 2006T1-2026T2; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md)

### 7. ¿Qué parte del precio de compra en la crisis se asocia al precio europeo?

En P2 la parte asociada al precio de la vivienda de la zona euro es -15,33 pp (-21,72 a -7,55). La banda excluye el cero en la crisis; en P3-P5 la incluye. Es asociación (C4).

- `V8-M1-eur-c-P2` = -15,33 pp (-21,72 a -7,55); capa C4; periodo P2 (2008T3-2013T4); dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M1/resumen.md](../output/v8/M1/resumen.md)

### 8. ¿Cuánto varió el precio real de compra en 2022T3-último dato?

La variación observada en P5 es 18,42 pp (log por 100, unidad común del SVAR). Es un dato observado; las contribuciones por factor llevan siempre banda.

- `V8-OBS-c-P5` = 18,42 pp; capa C4; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/por_que_ha_subido.md](../output/v8/por_que_ha_subido.md)

### 9. ¿Y el alquiler real en el mismo periodo?

La variación observada del alquiler real en P5 es -1,85 pp. El alquiler y la compra no se mueven igual en este periodo, por eso se analizan por separado.

- `V8-OBS-a-P5` = -1,85 pp; capa C4; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/por_que_ha_subido.md](../output/v8/por_que_ha_subido.md)

### 10. ¿Qué aportan el crédito y los tipos a la subida reciente de la compra?

En P5 la contribución media del SVAR es -0,469 pp (-2,82 a 12,77). La banda del 68 % incluye el cero, así que no se distingue de cero. Vale solo condicionado a las restricciones de signo y de cero (C3s).

- `V8-SVAR-c-P5-credito_tipos-media` = -0,469 pp (-2,82 a 12,77); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M2/resumen.md](../output/v8/M2/resumen.md)

### 11. ¿Frenó la subida de tipos el precio de compra (H8-2)?

No está respaldado. La estimación de H8-2 es -0,469 pp (-15,43 a 27,44) y el p de Holm es 0,987. El intervalo incluye valores positivos y negativos (C3s, condicionado a las restricciones).

- `V8-H8-2-est` = -0,469 pp (-15,43 a 27,44); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-H8-2-pholm` = 0,987; capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/F5/fichas.md](../output/v8/F5/fichas.md)

### 12. ¿Qué aportan la actividad y la renta a la compra en P5?

La media posterior de su contribución es 7,16 pp (-4,71 a 11,19), con banda del 68 % que incluye el cero. Es el factor con mayor media en la compra de P5, pero la regla no lo designa (C3s).

- `V8-SVAR-c-P5-empleo_renta-media` = 7,16 pp (-4,71 a 11,19); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M2/resumen.md](../output/v8/M2/resumen.md)

### 13. ¿Explica la demografía la evolución del alquiler reciente?

En P5 la contribución media del SVAR es 0,074 pp (-1,92 a 2,13), con banda que incluye el cero. H8-1 tiene p de Holm 0,987: no respaldada (C3s, condicionado a las restricciones).

- `V8-SVAR-a-P5-demografia-media` = 0,074 pp (-1,92 a 2,13); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-H8-1-pholm` = 0,987; capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M2/resumen.md](../output/v8/M2/resumen.md)

### 14. ¿Qué papel tiene la oferta en el alquiler de P5?

La contribución media de la oferta es 0,365 pp (-1,75 a 2,6), con banda que incluye el cero. No permite designar la oferta como factor del alquiler en ese periodo (C3s).

- `V8-SVAR-a-P5-oferta-media` = 0,365 pp (-1,75 a 2,6); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M2/resumen.md](../output/v8/M2/resumen.md)

### 15. ¿Cuánto de la variación de la compra queda sin atribuir a ningún factor?

La cuota no atribuida (parte determinista y no identificada) en P5 es 0,517  (-0,79 a 1,31) de la variación. Una atribución sin esta parte sería incompleta; por eso se publica con bandas.

- `V8-QNA-c-P5` = 0,517  (-0,79 a 1,31); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/por_que_ha_subido.md](../output/v8/por_que_ha_subido.md)

### 16. ¿Y la parte no atribuida del alquiler?

En P5 la cuota no atribuida del alquiler real es 1,06  (-1,94 a 4,29) de la variación observada: casi toda. Leer siempre con su banda.

- `V8-QNA-a-P5` = 1,06  (-1,94 a 4,29); capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/por_que_ha_subido.md](../output/v8/por_que_ha_subido.md)

### 17. ¿Qué probabilidad hay de que crédito y tipos sea el factor de mayor contribución en la compra de P5?

La probabilidad posterior de que sea el factor de mayor contribución es 29,66 %. Es una probabilidad dentro del modelo y de sus restricciones, no una prueba de causa (C4).

- `V8-PFSTAR-c-P5` = 29,66 %; capa C3s; periodo P5 (2022T3-último dato); dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/F5/fichas.md](../output/v8/F5/fichas.md)

### 18. ¿Algún instrumento externo permite una lectura causal?

No. Los instrumentos de M5 que cumplen las condiciones de C3 son 0 instrumentos. Los tres tienen primera etapa débil, por lo que no hay lectura causal externa.

- `V8-M5-c3` = 0 instrumentos; capa C4; periodo ver hipótesis; dato 2025T3. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M5/resumen.md](../output/v8/M5/resumen.md)

### 19. ¿Es fuerte el instrumento de los shocks monetarios del BCE sobre la compra?

No. El F efectivo de la primera etapa es 1,83, frente a un umbral de 10. H8-5 queda sin respaldo y sin lectura causal (C4).

- `V8-H8-5-F` = 1,83; capa C4; periodo ver hipótesis; dato 2025T3. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M5/resumen.md](../output/v8/M5/resumen.md)

### 20. ¿Y para el alquiler?

El F efectivo del instrumento monetario sobre el alquiler (H8-6) es 0,766, muy por debajo de 10. No supera las condiciones de C3.

- `V8-H8-6-F` = 0,766; capa C4; periodo ver hipótesis; dato 2025T3. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M5/resumen.md](../output/v8/M5/resumen.md)

### 21. ¿Es válido el instrumento de empuje migratorio?

No. El F efectivo de H8-7 es 0,048, con solo 20 observaciones anuales. No permite estimar el efecto de la inmigración sobre el alquiler.

- `V8-H8-7-F` = 0,048; capa C4; periodo ver hipótesis; dato 2025T3. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M5/resumen.md](../output/v8/M5/resumen.md)

### 22. ¿Hay una relación estable de largo plazo entre precio y fundamentales?

No se demuestra. De 9 especificaciones probadas, el ARDL con cotas rechaza la ausencia de cointegración solo en 2 especificaciones. Por eso la contabilidad de largo plazo no vota en la designación de factores.

- `V8-M4-ardl-total` = 9 especificaciones; capa C4; periodo 1998T1-último dato; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M4-ardl-rechaza` = 2 especificaciones; capa C4; periodo 1998T1-último dato; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M4/resumen.md](../output/v8/M4/resumen.md)

### 23. ¿Cuántos modelos del multiverso cumplen la regla de robustez?

De 74 combinaciones evaluadas, cumplen la regla 2 combinaciones, ambas de demografía en el alquiler (P2 y muestra completa). Es asociación (C4) y la regla de periodo no se cumple a la vez.

- `V8-M7-combinaciones` = 74 combinaciones; capa C4; periodo P1-P5 y completo; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M7-cumplen` = 2 combinaciones; capa C4; periodo P1-P5 y completo; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M7/resumen.md](../output/v8/M7/resumen.md)

### 24. ¿Cuántas especificaciones se exploraron en el multiverso?

La rejilla tiene 37.980 especificaciones y se ajustaron con éxito 32.424 especificaciones. El tope del pre-registro es 50.000. Las fallidas constan en el registro del módulo.

- `V8-M7-rejilla` = 37.980 especificaciones; capa C4; periodo P1-P5 y completo; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M7-ajustadas` = 32.424 especificaciones; capa C4; periodo P1-P5 y completo; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M7/resumen.md](../output/v8/M7/resumen.md)

### 25. ¿Sobreviven los efectos por periodo al control de falsos descubrimientos?

Tras BH (q = 0,10) hay 35 coeficientes, pero 2 efectos cumplen la regla de periodo y ninguno de ellos sobrevive a BH. Resultado exploratorio (C4).

- `V8-M0-bh` = 35 coeficientes; capa C4; periodo P1-P5; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M0-cumplen` = 2 efectos; capa C4; periodo P1-P5; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M0/resumen.md](../output/v8/M0/resumen.md)

### 26. ¿Mejora algún modelo la predicción de un AR(4) en el precio de compra?

No. El RMSE fuera de muestra del AR(4) es 1,18 pp; el del ECM v1 es 2,62 pp. Ningún modelo lo supera en la misma muestra.

- `V8-OOS-c-ar4-rmse` = 1,18 pp; capa C4; periodo 2016T2-2026T1; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-OOS-c-ecm_v1-rmse` = 2,62 pp; capa C4; periodo 2016T2-2026T1; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/F5/fichas.md](../output/v8/F5/fichas.md)

### 27. ¿Y en el alquiler?

El AR(4) tiene RMSE fuera de muestra de 0,803 pp; el BVAR de M2, 0,976 pp. Ninguno mejora al AR(4).

- `V8-OOS-a-ar4-rmse` = 0,803 pp; capa C4; periodo 2016T2-2026T1; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-OOS-a-bvar_m2-rmse` = 0,976 pp; capa C4; periodo 2016T2-2026T1; dato 2026T1. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/F5/fichas.md](../output/v8/F5/fichas.md)

### 28. ¿Supera el aprendizaje automático a la línea base en V8?

No. Los modelos de M9 que superan al AR(4) tras BH en la compra nacional son 0 modelos. Su mejor modelo tiene RMSE 2,24 pp, frente a 1,09 pp de la base.

- `V8-M9-oos-c-nacional-mejor` = 0 modelos; capa C4; periodo bloque de prueba de M9; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M9-oos-c-nacional-ml` = 2,24 pp; capa C4; periodo bloque de prueba de M9; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- `V8-M9-oos-c-nacional-base` = 1,09 pp; capa C4; periodo bloque de prueba de M9; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M9/resumen.md](../output/v8/M9/resumen.md)

### 29. ¿Qué coeficiente asocia el tipo hipotecario con el alquiler en el panel de CCAA?

El coeficiente DML es 0,452. Es una asociación sin identificación (C4) y no debe leerse como efecto. Las importancias y el SHAP tampoco son causas.

- `V8-M9-dml-a-tipo` = 0,452; capa C4; periodo panel de CCAA; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M9/resumen.md](../output/v8/M9/resumen.md)

### 30. ¿Qué mide el SHAP o la dominancia LMG: causa o predicción?

Miden contribución a la predicción o al ajuste, no causa. En V8 el coeficiente DML del tipo sobre la compra es 0,045 y se reporta como asociación (C4).

- `V8-M9-dml-c-tipo` = 0,045; capa C4; periodo panel de CCAA; dato 2026T2. Origen: [hechos.json](../output/v8/F6/hechos.json).
- Fuente: [output/v8/M9/resumen.md](../output/v8/M9/resumen.md)

### 31. ¿Cuál es el déficit de vivienda acumulado en 2021-2024?

Sin bajas del parque, la cifra de referencia y el rango entre variantes son 549.952 viviendas (389.361 a 710.542). Es una cota (C2): la dirección positiva se mantiene en todas las variantes, la amplitud no permite una cifra única.

- `L3-DEF-2124-SINBAJAS` = 549.952 viviendas (389.361 a 710.542); capa C2; periodo 2021-2024; dato 2024T4. Origen: [hechos.json](../output/v6_2/L3/hechos.json).
- Fuente: [output/v6_2/L3/deficit_alternativas.md](../output/v6_2/L3/deficit_alternativas.md)

### 32. ¿Y con las bajas estimadas del parque?

Con las bajas estimadas en v5.1 el déficit 2021-2024 es 654.646 viviendas (389.361 a 765.994) (todas las variantes). Es C4: depende de una estimación de bajas.

- `L3-DEF-2124-BAJAST1` = 654.646 viviendas (389.361 a 765.994); capa C4; periodo 2021-2024; dato 2024T4. Origen: [hechos.json](../output/v6_2/L3/hechos.json).
- Fuente: [output/v6_2/L3/deficit_alternativas.md](../output/v6_2/L3/deficit_alternativas.md)

### 33. ¿Cuál es el déficit acumulado 2021-2025?

Sin bajas, el rango de todas las variantes es 705.778 viviendas (523.606 a 887.950). Es C4 (contabilidad con correcciones de la EPA). Debe citarse con rango, no con un valor único.

- `L3-DEF-2125` = 705.778 viviendas (523.606 a 887.950); capa C4; periodo 2021-2025; dato 2025T4. Origen: [hechos.json](../output/v6_2/L3/hechos.json).
- Fuente: [output/v6_2/L3/deficit_alternativas.md](../output/v6_2/L3/deficit_alternativas.md)

### 34. ¿Cuántas viviendas hacen falta cada año de 2026 a 2035?

La necesidad anual recalculada es 210.424 viviendas/año (99.388 a 292.083) sin la sensibilidad X y 245.989 viviendas/año (123.936 a 338.663) con ella (cifra de referencia y rango entre escenarios). Es C4, no una cifra puntual.

- `T3-H5b` = 210.424 viviendas/año (99.388 a 292.083); capa C4; periodo 2026-2035; dato 2025. Origen: [hechos.json](../output/v5_1/T3/hechos.json).
- `T3-H5` = 245.989 viviendas/año (123.936 a 338.663); capa C4; periodo 2026-2035; dato 2025. Origen: [hechos.json](../output/v5_1/T3/hechos.json).
- Fuente: [output/v5_1/T3](../output/v5_1/T3)

### 35. ¿Se restan de la necesidad las viviendas liberadas por envejecimiento?

No, nunca. La proyección de hogares del INE ya las descuenta. Se estiman 185.643 viviendas/año (93.606 a 316.859) liberadas; frente a la necesidad central equivalen a 86,4 % (30,2 a 338,4), pero no se restan.

- `T2-H2` = 185.643 viviendas/año (93.606 a 316.859); capa C4; periodo 2026-2035; dato 2026-06-17. Origen: [hechos.json](../output/v5_1/T2/hechos.json).
- `T2-H15` = 86,4 % (30,2 a 338,4); capa C4; periodo 2026-2035; dato 2026-06-17. Origen: [hechos.json](../output/v5_1/T2/hechos.json).
- Fuente: [output/v5_1/T2](../output/v5_1/T2)

### 36. ¿Cuál será el déficit acumulado a fin de 2030?

En la rejilla de v5.1 el déficit a fin de 2030 es 1.349.025 viviendas (788.180 a 1.773.555) (mínimo, central y máximo). Es una proyección condicional (C4); no una predicción.

- `T4-H1` = 1.349.025 viviendas (788.180 a 1.773.555); capa C4; periodo 2021-2030; dato 2025. Origen: [hechos.json](../output/v5_1/T4/hechos.json).
- Fuente: [output/v5_1/T4](../output/v5_1/T4)

### 37. ¿Empeora el déficit entre 2025 y 2030?

En toda la rejilla de v5.1 la dirección nacional es que empeora (C2), con un cambio de 585.609 viviendas (87.246 a 946.852). La magnitud es C4. Hay provincias con dirección indeterminada.

- `T4-H2` = 585.609 viviendas (87.246 a 946.852); capa C4; periodo 2026-2030; dato 2025. Origen: [hechos.json](../output/v5_1/T4/hechos.json).
- Fuente: [output/v5_1/T4](../output/v5_1/T4)

### 38. ¿Cuántas viviendas al año habría que terminar para no aumentar el déficit?

Para mantener constante el déficit 2026-2030 hacen falta 211.772 viviendas/año (163.884 a 245.193). Es un cálculo condicional a hogares INE central y bajas de T1 (C4).

- `T4-H6` = 211.772 viviendas/año (163.884 a 245.193); capa C4; periodo 2026-2030; dato 2025. Origen: [hechos.json](../output/v5_1/T4/hechos.json).
- Fuente: [output/v5_1/T4](../output/v5_1/T4)

### 39. ¿Cuántas veces cabe la producción actual en la necesidad?

La necesidad equivale a 2,7 veces (1,4 a 3,8) la producción reciente (terminadas 2019-2024), según el cálculo de v5.1. Depende de los escenarios de necesidad y es C4.

- `T3-H9` = 2,7 veces (1,4 a 3,8); capa C4; periodo 2019-2024 (producción); dato 2024. Origen: [hechos.json](../output/v5_1/T3/hechos.json).
- Fuente: [output/v5_1/T3](../output/v5_1/T3)

### 40. ¿Cuántos hogares se crearon en 2021-2025?

El aumento de hogares fue 997.586 hogares (981.823 a 1.013.350), hecho C1 (al menos dos fuentes coinciden dentro de la tolerancia declarada).

- `dh_2125` = 997.586 hogares (981.823 a 1.013.350); capa C1; periodo 2021-2025; dato 2025T1. Origen: [hechos.json](../output/v4/M2/hechos.json).
- Fuente: [output/v4/M2](../output/v4/M2)

### 41. ¿Cuántas viviendas se terminan al año?

En el territorio común (sin País Vasco ni Navarra), las terminadas de 2019-2024 van de 72.264 a 94.426 viviendas/año, hecho C1 (rango entre fuentes). Sirve de referencia para la oferta reciente.

- `terminadas_1924` = 72.264 a 94.426 viviendas/año; capa C1; periodo 2019-2024; dato 2024. Origen: [terminadas_triangulacion.csv](../output/v4/M0/terminadas_triangulacion.csv).
- Fuente: [output/v4/M0](../output/v4/M0)

### 42. ¿Cuántas viviendas vacías hay que se pudieran movilizar?

Se estiman 733.553 viviendas (366.777 a 1.100.330) movilizables en zonas con presión en 10 años (10-30 % de las vacías); es C4. El Censo 2021 da una mediana municipal de vacías de 17,4 % de viviendas (6,8 a 35,2).

- `B1-H6` = 733.553 viviendas (366.777 a 1.100.330); capa C4; periodo 2026-2035; dato 2026-10-10. Origen: [hechos.json](../output/v5/B1/hechos.json).
- `R1C-021` = 17,4 % de viviendas (6,8 a 35,2); capa C4; periodo 2021-11; dato 2021-11. Origen: [hechos.json](../output/v5/R1C/hechos.json).
- Fuente: [output/v5/B1](../output/v5/B1)

### 43. ¿Qué peso tienen los compradores extranjeros?

En 2025 el 16,89 % (16,89 a 18,82) de las compraventas tiene comprador extranjero (residente o no) y los no residentes son 6,83 %. Es dato descriptivo (C4, una fuente).

- `compradores_extranjeros` = 16,89 % (16,89 a 18,82); capa C4; periodo 2025; dato 2025. Origen: [hechos.json](../output/v4/M4/hechos.json).
- `compradores_no_residentes` = 6,83 %; capa C4; periodo 2025; dato 2025. Origen: [hechos.json](../output/v4/M4/hechos.json).
- Fuente: [output/v4/M4](../output/v4/M4)

### 44. ¿Compran las personas jurídicas muchas viviendas?

En 2024 las compraventas con comprador persona jurídica son 11,3 % de compraventas. Es descriptivo (C4) y no distingue el uso posterior de la vivienda.

- `R1C-004` = 11,3 % de compraventas; capa C4; periodo 2024; dato 2024-12. Origen: [hechos.json](../output/v5/R1C/hechos.json).
- Fuente: [output/v5/R1C](../output/v5/R1C)

### 45. ¿Cuántos hogares viven en propiedad?

Tienen la vivienda principal en propiedad 74,5 % de hogares (72,1 a 75,9); es C1 (dos fuentes, 2021-2022). La mayoría de las compras no pasa por el mercado de alquiler.

- `R1C-001` = 74,5 % de hogares (72,1 a 75,9); capa C1; periodo 2021-2022; dato 2021-11. Origen: [hechos.json](../output/v5/R1C/hechos.json).
- Fuente: [output/v5/R1C](../output/v5/R1C)

### 46. ¿Ha subido el coste de construcción más que el precio?

Entre 2014T1 y 2025T4, el coste de construcción menos el precio de tasación varió -18,8 puntos porcentuales (-65,7 a -18,8). Es una diferencia de variaciones (C4), no un margen de beneficio.

- `R1C-013` = -18,8 puntos porcentuales (-65,7 a -18,8); capa C4; periodo 2014T1-2025T4; dato 2025-12. Origen: [hechos.json](../output/v5/R1C/hechos.json).
- Fuente: [output/v5/R1C](../output/v5/R1C)

### 47. ¿Cuántos lanzamientos por impago de alquiler hay?

Los lanzamientos practicados por la LAU, principalmente por alquiler impagado, son 18.317 lanzamientos/anio. Es una estadística de fuente única (C4) y no dice cuántos hogares afectados siguen en la vivienda.

- `CB-C5-01` = 18.317 lanzamientos/anio; capa C4; periodo 2025; dato 2025-12. Origen: [hechos.json](../output/v5/CB/hechos.json).
- Fuente: [output/v5/CB](../output/v5/CB)

### 48. ¿Cuánta vivienda protegida se califica al año?

La media anual de calificaciones definitivas de vivienda protegida es 11.265 viviendas/año. Es fuente única (C4); la oferta protegida es pequeña frente a la necesidad anual.

- `CC-C2-nuevas5a` = 11.265 viviendas/año; capa C4; periodo 2021-2025; dato 2025. Origen: [hechos.json](../output/v5/CC/hechos.json).
- Fuente: [output/v5/CC](../output/v5/CC)

### 49. ¿Cuántos instrumentos de política se han evaluado y con qué resultado?

Se evaluaron 36 instrumentos con una rúbrica; en 18 instrumentos el signo no es evaluable. Se evalúan instrumentos, no partidos ni personas, y siempre como escenario condicional (C4).

- `D1-H01` = 36 instrumentos; capa C4; periodo 2026-10; dato 2026-10-10. Origen: [hechos.json](../output/v5/D1/hechos.json).
- `D1-H02` = 18 instrumentos; capa C4; periodo 2026-10; dato 2026-10-10. Origen: [hechos.json](../output/v5/D1/hechos.json).
- Fuente: [output/v5/D1](../output/v5/D1)

### 50. ¿Qué parte de una ayuda a la demanda se traslada al precio?

En provincias de clase A4 1, el método A da 58,4 % (27,8 a 81,8) en la rejilla de elasticidad 0,3-1,5. Es una simulación con parámetros supuestos (C4), no un efecto medido.

- `D1-H11` = 58,4 % (27,8 a 81,8); capa C4; periodo rejilla εd 0,3-1,5; dato 2026-10-10. Origen: [hechos.json](../output/v5/D1/hechos.json).
- Fuente: [output/v5/D1](../output/v5/D1)

### 51. ¿Cuánto bajaría el precio de compra con 10.000 viviendas más de construcción?

En la simulación condicional de V7.1, la variación del precio por cada 10.000 viviendas es -0,609 puntos % (-2,35 a -0,108) (mediana entre CCAA). Es C4 y el signo lo fija en parte la fórmula; lo informativo es la magnitud relativa.

- `V71-S1-a_construccion-compra-efecto_10k` = -0,609 puntos % (-2,35 a -0,108); capa C4; periodo 2026-2036 (escenario); dato 2026-10-12. Origen: [hechos.json](../output/v7_1/S1/hechos.json).
- Fuente: [metodologia/dosis_coste.md](../metodologia/dosis_coste.md)

### 52. ¿Y movilizando vacías, en el alquiler?

La simulación da -1,75 puntos % (-6,8 a -0,306) por cada 10.000 viviendas, con la dosis y el coste declarados. Es un escenario condicional (C4), no una previsión.

- `V71-S1-b_vacias-alquiler-efecto_10k` = -1,75 puntos % (-6,8 a -0,306); capa C4; periodo 2026-2036 (escenario); dato 2026-10-12. Origen: [hechos.json](../output/v7_1/S1/hechos.json).
- Fuente: [metodologia/dosis_coste.md](../metodologia/dosis_coste.md)

### 53. ¿Qué efecto tendría regular los alquileres turísticos?

En la simulación de V7.1 la regulación local de turísticos da -3,52 puntos % (-13,58 a -0,62) en el alquiler por cada 10.000 viviendas. Es un escenario con parámetros supuestos (C4); no se mide un efecto.

- `V71-S1-d_turisticos-alquiler-efecto_10k` = -3,52 puntos % (-13,58 a -0,62); capa C4; periodo 2026-2036 (escenario); dato 2026-10-12. Origen: [hechos.json](../output/v7_1/S1/hechos.json).
- Fuente: [metodologia/dosis_coste.md](../metodologia/dosis_coste.md)

### 54. ¿Cuánto cuestan las ayudas a la demanda?

El coste fiscal anual aproximado de la simulación es 378,2 M€/año (67,98 a 2.915) (mediana entre CCAA). Se compara por dosis y coste, no por ideología del instrumento.

- `V71-S1-e_ayuda_demanda-compra-coste_anual_meur` = 378,2 M€/año (67,98 a 2.915); capa C4; periodo 2026-2036 (escenario); dato 2026-10-12. Origen: [hechos.json](../output/v7_1/S1/hechos.json).
- Fuente: [metodologia/dosis_coste.md](../metodologia/dosis_coste.md)

### 55. ¿En cuántas comunidades es robusta la movilización de vacías en alquiler?

En la simulación, es robusta en 17 CCAA de 17. Robusta significa que el esfuerzo baja en todas las extracciones del escenario; es C4, condicionado a los supuestos.

- `V71-S3-R6-b_vacias-alquiler-robustas` = 17 CCAA de 17; capa C4; periodo 2026-2036 (escenario); dato 2026-10-12. Origen: [hechos.json](../output/v7_1/S3/hechos.json).
- Fuente: [metodologia/dosis_coste.md](../metodologia/dosis_coste.md)

### 56. ¿Hay burbuja en el precio nacional?

Cocientes precio/renta y precio/alquiler con exuberancia GSADF tras BH: 0 series. Niveles de precio, que no controlan fundamentales: 0 series. Una exuberancia estadística no identifica una burbuja, y su ausencia tampoco la descarta (C4).

- `V72-GSADF-ratios-bh` = 0 series; capa C4; periodo 2007T1-2026T2; dato 2026-10-13. Origen: [hechos.json](../output/v7_2/gsadf/hechos.json).
- `V72-GSADF-niveles-bh` = 0 series; capa C4; periodo 2007T1-2026T2; dato 2026-10-13. Origen: [hechos.json](../output/v7_2/gsadf/hechos.json).
- Fuente: [output/v7_2/gsadf/ficha_burbuja.md](../output/v7_2/gsadf/ficha_burbuja.md)

### 57. ¿Y en las comunidades autónomas?

Series regionales (17 CCAA) con exuberancia tras BH: 0 series; en las provincias de entrenamiento de v6: 0 CCAA. Es exploratorio (C4): el contraste detecta aceleración, no sobrevaloración.

- `V72-GSADF-ccaa-bh` = 0 series; capa C4; periodo 2007T1-2026T2; dato 2026-10-13. Origen: [hechos.json](../output/v7_2/gsadf/hechos.json).
- `V72-GSADF-ccaa-v6` = 0 CCAA; capa C4; periodo 2015T1-2024T4; dato 2026-10-13. Origen: [hechos.json](../output/v7_2/gsadf/hechos.json).
- Fuente: [output/v7_2/gsadf/ficha_burbuja.md](../output/v7_2/gsadf/ficha_burbuja.md)

### 58. ¿Se confirma que empleo y población determinan el alquiler a largo plazo en las CCAA?

No. Ninguna de las hipótesis de largo plazo del atlas regional se confirma tras Holm. La velocidad de ajuste media del alquiler es -0,048 por trimestre, sin intervalo válido (C4, diferido).

- `V7-R4-PHI-ALQUILER-A` = -0,048 por trimestre; capa C4; periodo 2007Q1-2025Q1; dato 2026-10-10. Origen: [hechos.json](../output/v7/R4/hechos.json).
- Fuente: [output/v7/R4](../output/v7/R4)

### 59. ¿Qué rentabilidad bruta da el alquiler?

La mediana provincial de la rentabilidad bruta (alquiler sobre valor tasado) es 5,84 % del valor tasado, y el ratio precio/alquiler, 17,12 años de alquiler (15,33 a 18,84). Descriptivo (C4).

- `m1b_rentabilidad_bruta_mediana` = 5,84 % del valor tasado; capa C4; periodo 2023; dato 2024T4. Origen: [hechos.json](../output/v6/M1B/hechos.json).
- `m1b_ratio_precio_alquiler_mediana` = 17,12 años de alquiler (15,33 a 18,84); capa C4; periodo 2023; dato 2024T4. Origen: [hechos.json](../output/v6/M1B/hechos.json).
- Fuente: [output/v6/M1B](../output/v6/M1B)

### 60. ¿Cuál es el coste de uso de comprar?

El coste de uso anual (tipo hipotecario más 2,0 % de depreciación y mantenimiento) es 4,28 % del valor. La brecha con la rentabilidad bruta es 1,56 pp. Descriptivo (C4).

- `m1b_coste_uso_g2` = 4,28 % del valor; capa C4; periodo 2023; dato 2024T4. Origen: [hechos.json](../output/v6/M1B/hechos.json).
- `m1b_brecha_rentabilidad_coste_uso` = 1,56 pp; capa C4; periodo 2023; dato 2024T4. Origen: [hechos.json](../output/v6/M1B/hechos.json).
- Fuente: [output/v6/M1B](../output/v6/M1B)

### 61. ¿Se asocia la población extranjera con el alquiler en las provincias?

En el modelo provincial S0, +1 punto de población extranjera se asocia con 5,45 EUR/mes (-4,27 a 15,39) en el alquiler de stock; en S1 es 0,05 EUR/mes (-6,46 a 6,66). El signo y la magnitud dependen de la especificación (C4).

- `m1a_provincia_S0_share_ext_pob` = 5,45 EUR/mes (-4,27 a 15,39); capa C4; periodo 2021.0-2023.0; dato 2023. Origen: [hechos.json](../output/v6/M1A/hechos.json).
- `m1a_provincia_S1_share_ext_pob` = 0,05 EUR/mes (-6,46 a 6,66); capa C4; periodo 2016.0-2023.0; dato 2023. Origen: [hechos.json](../output/v6/M1A/hechos.json).
- Fuente: [output/v6/M1A](../output/v6/M1A)

### 62. ¿Se asocian las viviendas turísticas con el alquiler?

En provincias, +1.000 viviendas turísticas se asocian con -1,58 EUR/mes (-6,6 a 3,5) en el alquiler de stock; ningún intervalo al 95 % excluye el cero. No concluyente (C4).

- `m1a_provincia_S0_ln_vut` = -1,58 EUR/mes (-6,6 a 3,5); capa C4; periodo 2021.0-2023.0; dato 2023. Origen: [hechos.json](../output/v6/M1A/hechos.json).
- Fuente: [output/v6/M1A](../output/v6/M1A)

### 63. ¿Bajaron el alquiler los topes de precios catalanes?

Los resultados cambian de signo según la especificación: 4,36 EUR/mes (-0,38 a 9,16) en S0 y -1,54 EUR/mes (-4,01 a 0,95) en S1. No concluyente (C4); las pretendencias fallan.

- `m1a_municipio_S0_tope_cat_mun` = 4,36 EUR/mes (-0,38 a 9,16); capa C4; periodo 2021.0-2023.0; dato 2023. Origen: [hechos.json](../output/v6/M1A/hechos.json).
- `m1a_municipio_S1_tope_cat_mun` = -1,54 EUR/mes (-4,01 a 0,95); capa C4; periodo 2016.0-2023.0; dato 2023. Origen: [hechos.json](../output/v6/M1A/hechos.json).
- Fuente: [output/v6/M1A](../output/v6/M1A)

### 64. ¿Hay modelos de predicción que mejoren a la línea base más exigente en datos sellados?

En la validación sellada de v6 (K1), el mejor modelo predice mejor que la base más exigente en 6 tareas (de 9 tareas comparadas). Solo cuenta como «predice mejor» si supera a la base más exigente.

- `K1-N-MEJOR` = 6 tareas; capa C4; periodo validacion sellada v6; dato 2026-10-11. Origen: [hechos.json](../output/v6_1/K1/hechos.json).
- `K1-N-TAREAS` = 9 tareas; capa C4; periodo validacion sellada v6; dato 2026-10-11. Origen: [hechos.json](../output/v6_1/K1/hechos.json).
- Fuente: [output/v6_1/K1](../output/v6_1/K1)

### 65. ¿Hay variables relevantes con seguridad en la predicción provincial de v6?

No: son 0 variables según los criterios pre-registrados A y B, en alquiler y compra. Es predicción y asociación, no causa (C4).

- `V6-M4-N-REL` = 0 variables; capa C4; periodo entrenamiento 2015-2024 y sellado v6; dato 2026-10-11. Origen: [hechos.json](../output/v6/M4/hechos.json).
- Fuente: [output/v6/M4](../output/v6/M4)

### 66. ¿Cuál es la probabilidad de inclusión de la población en el precio de compra provincial?

El BMA da una probabilidad de inclusión posterior de 0,763 para la población. Una probabilidad alta no implica signo positivo ni causa (C4).

- `m2_pip_cp_ln_pob` = 0,763; capa C4; periodo 2015-2024; dato 2026-10-11. Origen: [hechos.json](../output/v6/M2/hechos.json).
- Fuente: [output/v6/M2](../output/v6/M2)

### 67. ¿Cuántas viviendas turísticas hay según el registro valenciano frente al INE?

El cociente entre el registro vigente de la Generalitat Valenciana y el INE es 1,76 veces (1,42 a 1,91). La discrepancia indica que las fuentes miden cosas distintas (C4).

- `R1A-H7` = 1,76 veces (1,42 a 1,91); capa C4; periodo 2026; dato 2026-08. Origen: [hechos.json](../output/v5/R1A/hechos.json).
- Fuente: [output/v5/R1A](../output/v5/R1A)

### 68. ¿Cuántas referencias de organismos coinciden con las cifras del proyecto?

Referencias que coinciden: 2 referencias; que difieren: 1 referencias. El resto no es comparable o lo es en parte. La comparación es descriptiva (C4).

- `D3-coincide` = 2 referencias; capa C4; periodo 2026-10-10; dato 2026-10-10. Origen: [hechos.json](../output/v5/D3/hechos.json).
- `D3-difiere` = 1 referencias; capa C4; periodo 2026-10-10; dato 2026-10-10. Origen: [hechos.json](../output/v5/D3/hechos.json).
- Fuente: [output/v5/D3](../output/v5/D3)

### 69. ¿Cuánto rotan los contratos en Cataluña?

La rotación (fianzas Incasòl sobre contratos vigentes SERPAVI) es 25 % (25 a 43,2). Es C4: combina dos fuentes con medidas distintas (contratos nuevos y stock).

- `A23-A11` = 25 % (25 a 43,2); capa C4; periodo 2015-2024; dato 2024. Origen: [hechos.json](../output/v5/A23/hechos.json).
- Fuente: [output/v5/A23](../output/v5/A23)

### 70. ¿Cuánto crédito hay en construcción e inmobiliarias?

El saldo de crédito a construcción y actividades inmobiliarias es 97,57 miles de millones de euros. Es una estadística oficial de fuente única (C4).

- `CA-CR-saldo-2025` = 97,57 miles de millones de euros; capa C4; periodo 2025Q4; dato 2026-06-01. Origen: [hechos.json](../output/v5/CA/hechos.json).
- Fuente: [output/v5/CA](../output/v5/CA)

### 71. ¿Cuál fue el atraso a absorber en diez años?

El atraso (déficit 2021-2025 más emancipación retrasada) es 1.103.170 viviendas (830.963 a 1.473.641). Es C4 y no se suma a la necesidad anual sin declarar el escenario.

- `B1-H2` = 1.103.170 viviendas (830.963 a 1.473.641); capa C4; periodo 2021-2025 absorbido en 2026-2035; dato 2026-10-10. Origen: [hechos.json](../output/v5/B1/hechos.json).
- Fuente: [output/v5/B1](../output/v5/B1)

### 72. ¿Cuántas viviendas libres de baja se han estimado por demolición?

Con licencias de demolición, la tasa anual de bajas es 0,026 % del parque al año (0 a 0,052) (media 2015-2024). Es una estimación (C4) y la identidad de censos da una tasa distinta.

- `T1-H8` = 0,026 % del parque al año (0 a 0,052); capa C4; periodo 2015-2024; dato 2024-12-31. Origen: [hechos.json](../output/v5_1/T1/hechos.json).
- Fuente: [output/v5_1/T1](../output/v5_1/T1)

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.
