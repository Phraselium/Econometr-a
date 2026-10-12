# Revisión independiente v6.1 tras K1, K4a, K4b y K2

Fecha: 2026-10-11. Revisor independiente; no hizo el trabajo revisado. Alcance: K1, K4a, K4b y K2 según el encargo. Tope de 60.000 tokens: la lectura fue dirigida (grep/head) y no se reejecutó `make all`. No se leyó data/sealed. No se hizo commit.

## Veredicto por módulo

| Módulo | Veredicto | Motivo principal |
|---|---|---|
| K1 | **APROBAR** (con R-03 y R-04 obligatorios antes de citar) | Sin fuga en las bases factibles. Una apertura por id. DM-HLN, permutación y Holm bien hechos. El criterio de clase se aplica tal como está escrito. |
| K4a | **APROBAR** (con R-07) | K4a-01 y K4a-02 son correctas y mínimas. K4a-03 está infravalorado. |
| K4b | **APROBAR** (con R-08, R-09 y R-10) | Las explicaciones son plausibles salvo A23-A10. Hay un posible origen no versionado en A23-P2. |
| K2 | **REHACER** (parcial y solo en texto: R-11 a R-14) | La descomposición es honesta y la capa C4 es correcta. Pero la conclusión se apoya en un control que puede ser mediador, y hay tres filas del historial mal clasificadas. |

## Comprobaciones hechas sin hallazgo
- **Accesos al sellado (K1).** `docs/v2/holdout_accesos.md` tiene 54 líneas `k1_`, que corresponden a 27 ids únicos. Cada id tiene una línea APERTURA y una línea de resultado: es decir, una apertura por (tarea, línea base), como fija D3. Ningún id se repite.
- **Bases factibles (src/v6/m4_lineas_base.py).**
  - El factor excluye las provincias selladas.
  - Los coeficientes se estiman solo con periodos < corte.
  - `fac` usa f_(t-1) y y_(t-1), que son información conocida un paso por delante, como la persistencia.
  - El efecto de unidad de una provincia sellada se imputa con la media de entrenamiento, no con el sellado.
  - En los trimestres de la ventana sellada, f_(t-1) usa filas de provincias no selladas del trimestre anterior. Eso es coherente con el diseño a un paso.
  - `ora` se etiqueta como oráculo y no entra en la base exigente.
- **DM-HLN (k1_run.py: dm_hln).** El factor sqrt((n−1)/n) es el de HLN con h=1. Usa t con n−1 grados de libertad y una sola cola en cada dirección.
- **Permutación y Holm.** La permutación invierte el signo por provincia, con 10.000 permutaciones y SEED 20261010, en una sola cola. Holm es monótono y está bien aplicado dentro de cada tarea × grupo × referencia.
- **Criterio de clase (línea 181).** Exige RMSE menor, p_Holm < 0,05 en DM-HLN y p_Holm < 0,05 en la permutación, contra la base exigente del grupo espacial. Los oráculos no definen la base. Se aplica bien.
- **K4a-02.** En el raw de Incasòl, todas las filas de 2007-2018 son «gener-desembre» y en 2019-2025 solo lo es ≈1/6. El filtro no pierde años anteriores a 2019. Que se exija unidad == contratos resuelve la mezcla con euros.
- **K4a-01.** `float_format="%.10g"` basta para recuentos < 10^10 y es un cambio mínimo.
- **K2.**
  - «anterior» se reestima en la misma muestra en cada paso (columna `coef_anterior_misma_muestra`, con N_anterior = N).
  - Hay 181 especificaciones en el registro, con Holm y BH por bloque.
  - Las salidas de K2 no nombran partidos ni personas ni usan lenguaje valorativo.
  - resultado.json declara C4 y «ANALIZADA, NO CONCLUYENTE».

## Hallazgos

| id | módulo | sev. | hallazgo | corrección concreta |
|---|---|---|---|---|
| R-01 | K1 | media | El DM-HLN por celdas (provincia-periodo) trata como independientes celdas del mismo periodo, que están correlacionadas entre provincias. El p resultante es demasiado optimista: por ejemplo, PROV_PRECIO_TRIM da p_Holm 1e-9 con 380 celdas. La clase depende también de la permutación por provincia, que es más defendible, así que el riesgo queda acotado. | En notas.md, declarar que el DM por celdas es anticonservador por la dependencia transversal. Añadir a la tabla principal la columna `p_dm_hln_per_holm` (DM por periodo), que ya existe en tabla_modelos_k1.csv. |
| R-02 | K1 | media | **PROV_PRECIO_ANUAL** queda en «predice mejor» con DM por celdas (0,0025) y permutación (0,0004). Pero el DM por periodo da p_Holm 0,13, y la mejora no se repite de forma estable en otros grupos de otras tareas. | Marcarla «predice mejor (frágil: DM por periodo no significativo)» en tabla_modelos_k1.md y en resultado.json, sin cambiar la regla. |
| R-03 | K1 | baja | Con 11 provincias solo hay 2^11 = 2.048 patrones de signo, y el p exacto mínimo de una cola es 1/2.048 ≈ 0,00049. La tabla publica 0,0004, que es un artefacto de Monte Carlo (4/10.001) por debajo del mínimo exacto. notas.md dice «~0,0005». | En perm_prov, enumerar los 2^k patrones cuando k ≤ 16 (p exacto) y reportar ese p. Ninguna clase cambia: 0,00049 × 3 < 0,05. |
| R-04 | K1 | baja | La base exigente se elige por el RMSE espacial del propio sellado. notas.md lo declara como optimista a favor de la base, lo cual es correcto para «mejor». Pero para la clase «peor» de otros grupos el sesgo va en contra del modelo: MUN_PRECIO_ANUAL total, y PROV_PRECIO_TRIM y PROV_VOL_TRIM temporal. | En notas.md, añadir que las clases «peor» heredan ese sesgo de selección y no se interpretan como inferioridad demostrada. |
| R-05 | K1 | baja | `factor(tr, sel)` se calcula antes de filtrar `tr.anio < corte`. Si `tr` contuviera periodos ≥ corte, f_tr los incluiría. Hoy `tr` es solo entrenamiento, así que no hay efecto. | Calcular f_tr después del filtro (es una línea), o añadir un assert de que tr.anio < corte. |
| R-06 | K1 | baja | Las tareas de compra tienen un solo modelo de v6 por tarea, así que Holm con m=1 no corrige nada. El mejor modelo se eligió por RMSE sellado en v6. La familia real de comparaciones son las 9 tareas. | Añadir en notas.md un Holm sobre las 9 tareas (grupo espacial, base exigente) como sensibilidad. Con los p actuales, las 6 clases «mejor» se mantienen (máximo 0,0025 × 9 = 0,023 en DM; la permutación exacta da 0,00049 × 9 = 0,0044). |
| R-07 | K4a | media (infravalorado) | K4a-03 tiene severidad media y está pendiente. Consiste en dos cifras para la misma magnitud de necesidad en el mismo informe: B1 214.868 y T3-H5b 210.424, con D2 rotulado «(B1)». Es una incoherencia visible en un entregable, y K4b (cifra 13) la confirma. | Subir K4a-03 a alta y resolverla antes del próximo entregable: o se recalcula D2 sobre T3, o se rotulan explícitamente las dos cifras con su definición. Registrarlo en ERRATA.md si cambia una cifra publicada. |
| R-08 | K4b | media | En A23-A10, la explicación «diferencia de ponderación» no es plausible tal como está escrita. Las tres provincias suben +22,2 %, +23,0 % y +28,9 %. Un mínimo publicado de 22,4 exige ponderar casi todo en Alicante, y una ponderación por población o por contratos (Valencia es la mayor) daría más de 24,7, no 22,4. Puede ser un error de agregación del original, por ejemplo índices con bases distintas o un cociente de sumas mal construido. | Abrir a23_run.py, reproducir la agregación de la Comunitat Valenciana y reclasificar el caso como «coincide» o «error del original» (en este segundo caso, a ERRATA). Mientras tanto, quitar «no error de dato» de la conclusión de K4b. |
| R-09 | K4b | media | En A23-P2, el valor central publicado (47,2) usa una tercera fuente (Notariado nacional 2015-2025) que según K4b no está en data/raw. Si el original la leyó de un fichero no versionado o la escribió fija en el código, incumple la regla v5 «ningún script lee ficheros no versionados». | Localizar el origen de la serie de Notariado en el código de precio de v5 y documentarlo. Si no está versionada, pasa a ser hallazgo de K4a con severidad alta. |
| R-10 | K4b | baja-media | En la cifra 3, el original aplica una constante de corrección de la EPA fijada en el código (242.400) que no se ha verificado frente a la fuente del INE. Además, el texto publicado dice «Ministerio y Catastro», pero el código calcula Ministerio con y sin protegida. Lo segundo es un error de descripción en un entregable. | Verificar la constante frente a la nota del INE sobre la ruptura de la EPA y citarla. Corregir la descripción de fuentes en el entregable y en ERRATA.md. En la cifra 5 (stock a 1 de enero mezclado con media anual dentro del mismo rango), pedir al menos que se declare la definición en la ficha. |
| R-11 | K2 | alta | La conclusión única y la sección F dicen que el resultado cambia «sobre todo con el control por población», con un cambio de signo en compra de 3,15 a −2,23. Ni inmigracion.md ni que_cambio.md advierten de dos cosas: que la población es en parte consecuencia mecánica de la inmigración (es componente del flujo y denominador de la cuota), y que condicionar en ella cambia el estimando. Ese cambio de signo puede reflejar un control mediador y no una inestabilidad. La conclusión C4 «no concluyente» se mantiene, pero el argumento principal está mal ponderado. | En §F, §G y que_cambio.md, añadir que la población puede actuar como mediador o término mecánico, y que P8 estima otra magnitud. Presentar P8 como sensibilidad, no como «la dimensión principal». Reordenar §F para que el método (2SLS frente a MCO) y la medida de alquiler sean las dimensiones que se pueden afirmar sin esa salvedad. |
| R-12 | K2 / historial | media | La fila «v1 Inmigración → Alquiler IPC (CCAA)» está marcada **Cambia**. Pero K2 obtiene el mismo signo (+) con MCO 0,76 y 2SLS 2,66, y solo deja de distinguirse de 0 al controlar por población, un control que v1 no usaba (ver R-11). Además, el nivel es distinto (provincia y no CCAA). | Reclasificar como **Se mantiene** (signo +, C4), con la nota «no robusto al control por población (posible mediador)». |
| R-13 | K2 / historial | media | La fila «v1 Empleo (nacional, DOLS/ECM)» está marcada **Cambia** con la evidencia «−2,37 con núcleo en compra, p 0,07». Es un resultado no significativo, a otro nivel (provincial) y con otra medida. No basta para cambiar la conclusión de v1. | Reclasificar como **Se mantiene (no concluyente)** y añadir la sensibilidad de K2 como nota. |
| R-14 | K2 / historial | media | La fila «v4/M7 Exuberancia nacional» está marcada **Cambia** porque en v6 ninguna de las 11 CCAA supera el valor crítico. Un resultado por CCAA no refuta uno nacional, y el veredicto nacional no se reverificó. | Reclasificar como **Se mantiene (nacional, no reverificado)** y anotar «v6: sin exuberancia en las 11 CCAA (otro nivel)». |
| R-15 | K2 / historial | baja | La fila «v2/BI» está marcada **Cambia**, pero K2 no reproduce la muestra (38 provincias frente a 49, F = 3,5 frente a 14,4). La columna MCO de v2 ya mostraba el orden compra > alquiler, así que lo que cambia es la lectura, no el resultado. | Escribir «**Cambia la lectura**; no es una réplica (otra muestra, primera etapa débil)», igual que en la fila v6/M2. |
| R-16 | K2 | baja | En P8, N sube de 282 a 306 (alquiler) y de 304 a 328 (compra) al añadir un control. El «anterior» se reestima bien en la misma muestra, pero la cadena no explica por qué la muestra de P7 era más pequeña. | Añadir una nota en §A con la causa (qué variable de P7 faltaba). Ninguna cifra cambia. |
| R-17 | K2 / historial | baja | La fila «v2/BA Demografía (predicción)» está marcada **Se mantiene** frente al AR(4). Con K1, el criterio pasa a ser la base más exigente, y v2/BA no se ha comparado con ella. | Añadir «pendiente frente a la base exigente de K1». |

## Lista priorizada de cambios
1. **R-11.** Salvedad sobre la población como posible mediador en K2 §F, §G y que_cambio.md, y reordenar las dimensiones.
2. **R-12, R-13 y R-14** (y R-15). Reclasificar esas filas del historial.
3. **R-08 y R-09.** Verificar A23-A10 y el origen de Notariado en A23-P2; enviar a ERRATA o a K4a si procede.
4. **R-07.** Subir K4a-03 a alta y resolverlo antes de entregar.
5. **R-02 y R-01.** Marcar PROV_PRECIO_ANUAL como frágil y añadir la columna de DM por periodo.
6. **R-10.** Verificar la constante EPA de 242.400 y la descripción de fuentes de la cifra 3.
7. **R-03, R-04, R-05, R-06, R-16 y R-17.** Ajustes menores de cálculo y documentación.

## Límites de esta revisión
- No se reejecutó `make all` dos veces ni se compararon md5: el encargo y el tope lo excluyen.
- No se abrió src/v6_1/k4b_run.py ni a23_run.py (R-08 y R-09 quedan como sospecha razonada).
- Del script de K2 solo se leyó la cadena de pasos.
