# Revisión independiente FINAL de V8 (puerta F6)

- Fecha: 2026-10-13. Revisor independiente; no ha participado en el trabajo revisado.
- Commit revisado: f06358f (r8/main). El HEAD al revisar es 9f8baa9, que solo cambia docs/v8/estado.md.
- No se ha leído data/sealed. Solo se ha escrito este fichero; no se ha modificado código, salidas ni documentos del repositorio.
- Re-ejecución en un clon aislado (scratchpad/rev_final/repo, sin red: HTTPS_PROXY=http://127.0.0.1:9). No se ha tocado el clon donde corre `make v8`.

## 0. Veredicto

**APROBAR CON CORRECCIONES.** No hay hallazgos bloqueantes. Hay 10 hallazgos mayores, que hay que corregir antes de difundir y de crear la etiqueta v8.0, y 7 menores.

Lo que se sostiene:

- **La conclusión central, «ningún factor designado en los diez casos», es correcta** y no depende de las elecciones discutibles. He recalculado tres celdas a mano (§2). Aunque se cambien las elecciones de K2 y K4 (contar el voto de LP-IV o votar el SVAR por la media), ninguna celda llega a tres votos.
- **La reproducibilidad de F5 y F6 está comprobada.** La cadena f5_atribucion → f6_congelar → f6_tablas → f6_hechos → f6_verificador → cifras_clave → render_v8 se ha ejecutado dos veces: rc = 0 las dos veces, y el md5 coincide entre las dos ejecuciones y con el commit en los 25 ficheros comparados. `git status` solo muestra `output/v8/F5/tiempos.json`, de modo que tablas_v8.xlsx y ensayo_evaluate.md también son idénticos. `check_v8`: 0 errores. `make check` en el clon: rc = 0 (277 tests aprobados; check_texto, check_v5, check_v6 y check_v8 con 0 errores). El `make v8` completo (M0-M9) no lo he re-ejecutado; corre en el otro clon.
- **Las cifras de v1-v7.2 no cambian.** Las 716 filas no V8 de output/v5/cifras_clave.csv son idénticas, campo a campo, a las de la etiqueta `v7.2` y a las huellas de docs/v8/cifras_base_v72.csv: 0 cambios y 0 desapariciones.
- **La congelación cuadra.** El sha256 conjunto recalculado es 89c5feb6…c664863, igual al de docs/v8/notas_release.md y al de congelacion.json. El de output/v8/M2/predicciones_congeladas.csv (5009f044…) coincide con su manifiesto.
- **evaluate_v8 resiste las pruebas de apertura** (§5): con datos parciales no registra apertura y la segunda ejecución se niega (rc = 3).
- **Neutralidad.** No hay léxico valorativo ni partidista en los entregables ni en las fichas del verificador V8. Las fichas evalúan afirmaciones, no a quien las formula.

## 1. Cierre de J1-J23 (docs/v8/revision_F4.md)

| J | Estado | Evidencia |
|---|---|---|
| J1 | Corregido | Se aplica la opción (b) en lugar de la (a), declarada en desviaciones.md (línea 68 del fichero) por la restricción de bvar.py. `m2_svar.py:106`: impulso en 2021T1. Las hipótesis retiradas están publicadas (M2/hipotesis_m2_retirada.csv). Hay sha nuevo, con `sha256_anterior_retirado`, en M2/congelacion.json. M3 (`m3_periodos_var.py:72`) y M6/M7 (`m67_comun.py:83-84`: 4 trimestres en las interanuales) usan impulsos. |
| J2 | Corregido | El punto es la media posterior; se publican la mediana y las bandas; P(f*) se calcula sorteo a sorteo (M2/prob_mayor.csv). |
| J3 | Corregido | hipotesis_m5.csv: `signo_pi_apriori` = «+». p AR = 0,724, 0,635 y 0,536; Holm = 1 en las tres. Se añade la forma reducida y la regresión ya es una sola (la de F y AR). |
| J4 | **Parcial** | En el alquiler, LP-IV se abstiene. En la compra, `vota_s9 = si` en P1-P5, porque el AR del 68 % está acotado, y en compra P4 vota por credito_tipos. Los documentos dicen lo contrario (K2). |
| J5 | Corregido | La contribución es cuota × R² × ΔY, más una fila de `residuo` y `signo_parcial` (M6/atribucion.csv, voto_dominancia.csv). |
| J6 | Corregido | M7/resumen_multiverso.csv tiene las columnas `orientacion` y `beta_orient_mediana`; 2 de 74 celdas cumplen. Su uso en el texto es incompleto (K3, K8). |
| J7 | Corregido | F5/fuera_muestra_comun.csv: ECM v1 importado de v7, misma muestra 2016T2-2026T1 (n = 40) para los cuatro modelos. |
| J8 | Corregido | La tasa de paro EPA está en el umbral de M0 (`m0_periodos.py:68,577`) y la desviación está corregida (línea 65). |
| J9 | Corregido | M0/resultado.json: «EXPLORATORIO (C4) para todo». |
| J10 | Corregido | M4/cointegracion.csv: decisión con F y t; 2 de 9 especificaciones. |
| J11 | Corregido | M4/voto_contabilidad.csv: voto por el signo de la brecha con umbral del 0,5 %. |
| J12 | Parcial (declarado) | SHAP evaluado dentro de la bolsa (`m9_ml.py:304-347`). Siguen fuera de su banda 6 de 146 puntos, entre ellos turismo en compra P5 (15,16 frente a [8,13; 14,83]); los entregables lo declaran. |
| J13 | Corregido | Un panel por mercado (`m9_ml.py:509`); turismo solo en P4-P5. |
| J14 | Parcial | `ms_fit` está anotado en Y9. La desviación IV2b sigue diciendo «se añade antes de ver el resultado» (desviaciones.md, línea 59 del fichero), sin el rótulo pedido. Aparecen casos nuevos del mismo tipo (K4, K15). |
| J15 | Corregido | Columnas `pct_*_rejilla` y `multiverso_truncado`. |
| J16 | Parcial | H8-9 con L = 12 y rótulo «aproximación de 5 países» (M1/resumen.md, línea 5). En M6, 10 de 152 puntos principales siguen fuera de su banda del 68 %, y el informe dice «centradas» (K14). |
| J17 | Corregido | Los identificadores de M3 cruzan: 480 de 480. |
| J18 | Corregido | `perm_instrumento_ok`; no cuenta como prueba independiente. |
| J19 | Corregido | `ccaa:01`…`ccaa:17`; `pct_total` de M1 en %. |
| J20 | Corregido | Columnas `variante` y `principal` en todas las atribucion.csv. |
| J21 | Corregido | `check_v8.p_ajustados` pasa; M9/coeficientes.csv tiene las 47 columnas del contrato. |
| J22 | Corregido | Reproducido en F5-F6: solo cambia tiempos.json. |
| J23 | Corregido | `factor_comun` está en NO_COMPITEN (`f5_atribucion.py`). |

## 2. F5: aplicación de R0-R8 y recálculo a mano

**Recálculo desde las entradas.** Las tres celdas coinciden con output/v8/F5/regla_s9.csv.

- **Compra P5 (ΔY = +18,42).**
  - M2/prob_mayor.csv: el máximo de P(f*) es credito_tipos (0,2966) y el máximo de la media c·sign es empleo_renta (7,157), por lo que vota credito_tipos (Y10) con el aviso «ranking incierto».
  - M6/voto_dominancia.csv: factor_europeo, turismo y empleo_renta tienen signo «−»; vota credito_tipos (cuota 0,11; «+»).
  - M5: `vota_s9 = si`, pero c·sign = −11,3 < 7,157, así que LP-IV se abstiene.
  - M4: brecha +580,8 miles = 3,0 % ≥ 0,5 %, del mismo signo que ΔY, así que la contabilidad vota demografía.
  - Recuento: credito_tipos 2 y demografia 1, de modo que la condición 1 no se cumple.
  - M7: la familia credito_tipos tiene 0,632 (< 0,80) y tipo_hip_real 0,875, de modo que la condición 2 no se cumple.
  - Banda de M2: [−2,82; 12,77], que incluye el 0, de modo que la condición 3 no se cumple.
- **Compra P4.**
  - LP-IV: c·sign = −4,355 × −1 = 4,355, mayor que el máximo del SVAR (2,614, demanda_vivienda), así que vota credito_tipos.
  - Dominancia: credito_tipos (0,59; «−»).
  - SVAR: empleo_renta (P = 0,259).
  - Recuento: credito_tipos 2. Multiverso: 0,542 y 0,525. Además, R7 (P4 es impreciso).
- **Compra P1.**
  - SVAR: empleo_renta (P = 0,717); banda [9,0; 54,6], que excluye el 0.
  - Dominancia: los cuatro factores tienen signo «−», así que se abstiene.
  - LP-IV: 26,7 < 31,8, así que se abstiene.
  - Contabilidad: la brecha es −547,6 miles con ΔY > 0, así que se abstiene.
  - Recuento: 1 voto. Multiverso: pib_vol 0,875 (con signo **negativo**; K3).

**¿Se aplica R0-R8 sin ajustarla al resultado?** En lo esencial, sí. Hay dos salvedades:

- **Voto del SVAR (Y10).** R2 (revision_F4.md, línea 423) define f* como el argmax de la media posterior. Y10 lo cambia por el argmax de P(f*). Y10 se escribió en el commit 7b00215, el mismo que produjo M2/prob_mayor.csv. Las «precisiones de aplicación» (1)-(5) y la tabla común fuera de muestra (desviaciones.md, líneas 72-73 del fichero) entraron en f20ab0d, el mismo commit que los resultados de F5. Que sean anteriores a los resultados no es verificable con git. Ninguna de estas elecciones cambia la conclusión: con el voto por la media, compra P5 queda en 1-1-1 y compra P4 en 2.
- **Consecuencia declarada en desviaciones.md** (línea 66 del fichero: «con lpiv abstenido, solo demografia puede reunir 3 votos»). Es falsa en la compra (K2).

**«Ningún factor designado».** Es correcto: el máximo es 2 de 4 en compra P3, P4 y P5 y en alquiler P2 y P5. Contando el voto de LP-IV en la compra, ninguna celda llega a 3.

## 3. Hallazgos

### K1. Comunitat Valenciana: la «parte común» es un R² y se presenta como parte de la subida; el «crecimiento acumulado» es una aproximación que no coincide con el acumulado observado. — **mayor**

**Evidencia.**
- La columna «Parte común en P5» de por_que_ha_subido.md (líneas 172-177) vale 95,8 %, 94,5 %, 98,0 % y 77,2 %. Es `cuota_factor_nacional = r2` (`m8_regional.py:420`; M8/cuota_cv.csv), es decir, la cuota de la **varianza** del crecimiento interanual.
- La parte de la **subida** asociada al factor común está en M8/atribucion.csv (P5, `principal = si`): Alicante 11,2 de 16,8 pp (66,8 %), Castellón 14,6 de 7,8 pp (187 %), Valencia 12,2 de 21,1 pp (58,0 %) y València ciudad 13,0 de 36,3 pp (35,8 %, con un residuo propio de 23,3 pp, el 64 %).
- Por tanto, «En las tres provincias, la subida reciente se explica casi entera por lo común a toda España» (línea 179) no tiene respaldo, y en València ciudad la parte propia es mayoritaria, no «algo menor». El verbo «explica» en C4 es además lenguaje causal.
- Los «crecimientos acumulados» de la tabla (16,8 / 7,8 / 21,1 / 36,3 pp) son la media interanual × T/4. El acumulado observado del valor tasado (M8/descriptivo_cv.csv) es 25,1 / 18,6 / 29,4 / 43,5 pp. En la provincia de Valencia, P5, las dos fuentes discrepan (MIVAU 29,4 frente a Registradores 17,4; C4), y CLAUDE.md pide reportar ambas.

**Corrección.**
1. Plantilla, línea 170: sustituir «Crecimiento acumulado del precio de compra en cada periodo y parte que acompaña al factor común nacional» por «Variación del precio real de compra (media interanual × T/4; aproximación) y cuota de la varianza del crecimiento interanual que comparte con el factor común nacional (R²)».
2. Renombrar la columna a «Comovimiento con el factor común en P5 (R²)».
3. Añadir una columna «Parte de la variación asociada al factor común en P5 (pp, banda del 68 %)» desde M8/atribucion.csv, con ids nuevos en f6_hechos.py.
4. Sustituir la línea 179 por: «En las tres provincias, las fluctuaciones del crecimiento reciente van casi enteras con las del conjunto de España (R² de 0,94-0,98) [C4]. La parte del aumento acumulado asociada al factor común es menor: 58-67 % en Alicante y Valencia; en Castellón supera lo observado. En València ciudad es en torno a un tercio, y el resto es un componente propio que este análisis no atribuye a ningún factor.»
5. Añadir el acumulado de las dos fuentes de descriptivo_cv.csv (las dos cuando discrepan).
6. En f6_hechos.py:230, cambiar el indicador `V8-M8-cv-*-cuota` a «R² del crecimiento interanual … sobre el factor común nacional (cuota de varianza; no es parte de la variación acumulada)».

### K2. «LP-IV se abstiene casi siempre; por construcción solo la demografía podía reunir tres votos»: es falso en la compra. — **mayor**

**Evidencia.**
- M5/atribucion.csv: `vota_s9 = si` en compra P1-P5 (AR del 68 % acotado), aunque F = 1,83 y el AR del 95 % es (−∞, ∞).
- regla_s9.csv, compra P4: `voto_lpiv = credito_tipos`. En la compra, credito_tipos podía reunir tres votos (SVAR, dominancia y LP-IV).
- Las contribuciones de LP-IV salen de β = −8,78, la estimación con la primera etapa de signo contrario (J3).
- Afirmaciones afectadas:
  - por_que_ha_subido.md:57 y :138;
  - informe_econometrico.md:73 («Con F por debajo de diez y Anderson-Rubin no acotado, el método LP-IV se abstiene»);
  - cierre_proyecto.md §2 («Con LP-IV abstenido, solo la demografía podía reunir tres votos por construcción»);
  - desviaciones.md, línea 66 del fichero («Consecuencia declarada…»).

**Corrección.**
- Plantilla por_que, línea 57: sustituir «Con los instrumentos débiles, el método LP-IV se abstiene casi siempre, y eso deja a la demografía como la única familia que, por construcción, podía reunir tres votos.» por «En el alquiler, LP-IV se abstiene siempre (F < 10 y Anderson-Rubin al 68 % no acotado), de modo que allí solo la demografía podía reunir tres votos. En la compra, el intervalo de Anderson-Rubin al 68 % está acotado y LP-IV puede votar, pero solo por crédito y tipos; lo hace en P4, con una primera etapa débil (F = 1,83) y de signo contrario al esperado.»
- Línea 138: sustituir «Es la única familia que podía reunir tres votos con los instrumentos débiles» por «En el alquiler es la única familia que podía reunir tres votos».
- Informe, línea 73: sustituir por «En el alquiler, LP-IV se abstiene (F < 10 y Anderson-Rubin al 68 % no acotado). En la compra, el Anderson-Rubin al 68 % está acotado y LP-IV vota cuando supera a todos los factores del SVAR (solo en P4; primera etapa con el signo contrario)».
- Cierre §2: el mismo cambio.
- desviaciones.md: añadir una fila con fecha que diga que la «consecuencia declarada» era inexacta para la compra.

### K3. Compra P1: «su signo es estable en el multiverso» se presenta como apoyo, pero el signo estable es el contrario. — **mayor**

**Evidencia.**
- M7/resumen_multiverso.csv, compra P1, empleo_renta / pib_vol: `pct_mismo_signo` = 0,875, con `signo_mayoritario` = **negativo** (`beta_orient_mediana` = −0,149), `pct_sig_bh` = 0,031 y `multiverso_truncado` = True.
- Con las fallidas en el denominador queda en el 35 % (familia) y el 58 % (variable) (fichas.md, compra P1).
- El SVAR da +31,8 pp. La condición 2 se cumple solo porque R3 no exige que el signo coincida con la dirección de la contribución.
- Afirmaciones afectadas: por_que_ha_subido.md:90 («…y cuyo signo es estable en el multiverso») y cierre_proyecto.md §1 («y signo estable en el multiverso»).

**Corrección.**
- Plantilla, línea 90: sustituir por «Es la única contribución del SVAR cuya banda del 68 % excluye el cero. En el multiverso, el crecimiento del PIB tiene un signo estable, pero **negativo** (el 88 % de las especificaciones; ninguna significativa tras BH en más del 3 %; con las especificaciones fallidas, el 35 %): la asociación por regresión no acompaña al signo del SVAR.»
- Cierre §1: «tiene banda que excluye el cero, pero en el multiverso el signo estable es el contrario y un solo método vota por él».
- En fichas.md, añadir el signo mayoritario a la línea del multiverso.
- Declarar en desviaciones.md que R3 se aplicó sin exigir la coincidencia de signo, y que esto no altera ninguna designación.

### K4. Compra P5: «el SVAR señala crédito y tipos» y «es el primero en el SVAR de P5» sin decir que por la media es el último. — **mayor**

**Evidencia.**
- M2/prob_mayor.csv, compra P5: medias c·sign de empleo_renta 7,16, oferta 1,87, demografia 0,65, demanda_vivienda −0,30 y credito_tipos **−0,47**.
- El voto (Y10) va al máximo de P(f*): credito_tipos, con 0,297. Es decir, un factor cuya media empuja en contra de ΔY recibe el voto de «mayor empuje en la dirección de ΔY» (R0).
- Y10 se escribió en el mismo commit que prob_mayor.csv (§2).
- «Es el primero en la dominancia de P4 y P5» (por_que:142): en compra P5, credito_tipos es el cuarto por cuota (0,11). Es el voto de la dominancia (el primero con el signo de ΔY), no el primero.
- Lo mismo con «La dominancia lo pone primero en la compra de P2 y en el alquiler de P1» (por_que:150): factor_europeo es el segundo por cuota (0,25 y 0,14).

**Corrección.**
- Plantilla, línea 76: sustituir «En la compra de P5, el SVAR y la dominancia señalan crédito y tipos» por «En la compra de P5, crédito y tipos es el factor con más probabilidad de ser el mayor en el SVAR (30 %), aunque su media posterior es negativa y la mayor media es la de actividad y renta; la dominancia también lo vota».
- Línea 142: sustituir «Es el primero en la dominancia de P4 y P5 y en el SVAR de P5» por «Lo vota la dominancia en P4 y P5 (el primer factor cuya contribución parcial tiene el signo de la variación) y, en P5, el SVAR por probabilidad (30 %), no por media».
- Línea 150: sustituir «La dominancia lo pone primero» por «La dominancia lo vota (primer factor con el signo de la variación)».
- Anotar en desviaciones.md que Y10 y las precisiones (1)-(5) entraron en los commits 7b00215 y f20ab0d, junto con las salidas de M2 y F5.

### K5. Factor europeo: «solo es distinta de cero en la crisis» lo contradice el propio informe (P1). — **mayor**

**Evidencia.**
- M1/atribucion.csv, P1: factor_europeo 7,37 [4,72; 8,73]; la banda del 68 % excluye el 0 (informe_econometrico.md:98).
- Lo contradicen: por_que_ha_subido.md:108 («Es el único periodo en que esa parte tiene una banda que excluye el cero»), :150 («solo es distinta de cero en la crisis») y cierre_proyecto.md §1 («La parte europea solo es distinta de cero en la crisis»).
- La cifra de P1 se calcula con n = 10 trimestres (notas de M1: zona euro desde 2006), pero `V8-M1-eur-c-P1` lleva el rótulo «P1 (1995T1-2007T4)».

**Corrección.**
- Sustituir las tres frases por «La parte europea tiene una banda que excluye el cero en P2 (−15,3 pp) y en el tramo final de P1 (2005-2007, 7,4 pp); en P3-P5 incluye el cero».
- Cambiar el periodo de `V8-M1-eur-c-P1` en f6_hechos.py a la ventana efectiva (n = 10).

### K6. Turismo «15,2 pp»: es una sensibilidad no principal, promediada sobre 6 CCAA, que se presenta al lado de la variación nacional. — **mayor**

**Evidencia.**
- M9/atribucion.csv, fila 36: `metodo = shap_sens_turismo`, `principal = no`, «resumen solo en filas con dato de turismo» (6 CCAA), B = 64. R8 pide filtrar por la variante principal.
- La cobertura de `V8-M9-shap-c-P5-turismo` dice «17 CCAA (panel)», pero el texto dice 6.
- La cifra aparece en por_que_ha_subido.md:132, informe_econometrico.md:102 y verificador_v8.md (V8-V3), al lado de los 18,4 pp nacionales.

**Corrección.**
- Indicador y cobertura en f6_hechos.py: «sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional».
- Plantillas: «En una sensibilidad no principal, limitada a las 6 comunidades con datos de turismo, SHAP asigna al turismo … del crecimiento del precio de compra de esas comunidades».
- Retirarla del informe y dejarla solo en la sección «solo contraste».

### K7. Lectura causal desde DML y verbos causales en líneas C4. — **mayor**

**Evidencia.**
- por_que_ha_subido.md:142, tras el coeficiente de DML: «Una lectura compatible, no contrastada aquí, es que el encarecimiento del crédito desvíe demanda de la compra al alquiler.» Propone un mecanismo causal a partir de una asociación de DML (§11 del pre-registro; CLAUDE.md v6).
- por_que_ha_subido.md:164: «lo que la mueve es, sobre todo, común a todo el país» (C4, a partir de una cuota de varianza).
- por_que_ha_subido.md:179 (K1).
- `check_v8` no detecta ninguna de las tres (K9).

**Corrección.**
- Línea 142: borrar la frase.
- Línea 164: sustituir «lo que la mueve es, sobre todo, común a todo el país» por «sus fluctuaciones son, sobre todo, comunes a todo el país».

### K8. Multiverso de crédito y tipos en P5: el texto omite que la variable principal sí tiene un signo estable, pero contrario al canal expansivo. — **mayor**

**Evidencia.**
- M7, compra P5, tipo_hip_real: 0,875 estable, orientado **negativo** (un tipo real más alto va con más crecimiento del precio), con `pct_sig_bh` = 0,50: cumple la regla por variable (tablas_modelos_destacados.md, tabla (a)).
- En el alquiler también: P5 0,854 negativo, P4 0,833 y completo 1,000.
- por_que_ha_subido.md:124 («solo es estable en una parte de las especificaciones y no llega al 80 %») y :142 («el signo deja de ser estable») solo valen para la familia (0,632).

**Corrección.**
- Línea 124: «En el multiverso, la familia de crédito y tipos (orientada) no llega al 80 % (63 %). La variable principal, el tipo real hipotecario, sí tiene un signo estable (88 %), pero en sentido contrario al canal expansivo: un tipo real más alto va con más crecimiento del precio. Es una asociación sin identificación [C4].»
- Línea 142: lo mismo, en una frase.

### K9. check_v8.py deja pasar infracciones reales. — **mayor**

He probado regex y alcance con líneas fabricadas (scratchpad/rev_final/tests_eval/t_check.py). 5 de 6 infracciones pasan:

| Línea fabricada | Detectada |
|---|---|
| «Según SHAP, el turismo impulsa la subida … [C4]» | no |
| «…se explica casi entera por lo común … [C4]» | no |
| «El DML muestra que … desvía demanda …, aunque sin identificación [C4]» | no |
| «SHAP muestra que el turismo causa la subida, sin identificación externa [C4]» | no |
| «La dominancia indica que el crédito es el motor … [C4]» | no |
| «El turismo explica la subida (SHAP) [C4]» | sí |

Huecos:

| Comprobación | Hueco |
|---|---|
| a) Texto | `NEG` (línea 40) exime la línea entera si contiene «sin/no … identifica/causal». `CAUSAL` (líneas 38-39) no cubre impulsa, empuja, motor, mueve, desvía, frena ni «se explica». El alcance no incluye output/v8/F5/fichas.md, F5/resumen.md, M*/resumen.md ni docs/v8/cierre_proyecto.md. |
| b) Cruces | La regex de la línea 133 no detecta `left_on=`/`right_on=` (no hay límite de palabra en «_on»), `on=variable`, `.map()` ni `isin()` por nombre. |
| c) Bandas | Solo se exigen en las filas con `vota == "si"` (línea 104). V8 pide «atribuciones siempre con bandas»: lpiv del alquiler, `residuo` y la cuota no atribuida (banda aproximada) pasan sin control. |
| d) p ajustado | Solo mira M*/coeficientes.csv. No valida que `metodo_ajuste` ∈ {Holm, BH}. Si falta la columna `p_ajustado`, `c.get(...)` devuelve None y el check falla con una excepción en vez de un error controlado. No cubre hipotesis_m*.csv ni F5. |
| e) Cifras previas | `i not in errata` (líneas 63 y 66) es una búsqueda de subcadena: 9 ids de la base (A23-A10, B2-H3, D2-H01, D2-H13, T3-H5, T3-H5b, …) aparecen ya en ERRATA.md y quedan **exentos para siempre**. |
| f) Modelos destacados | Solo una regex sobre el motivo. No comprueba que el destacado sea el de menor RMSE de su familia. |
| g) Trazabilidad | Solo comprueba que `origen` empiece por «output/v8/». No comprueba que la clave exista en hechos.json ni que el valor coincida. |

**Corrección mínima.**

- **a)**
  - Ampliar `CAUSAL` con `impuls\w*|empuj\w*|motor|mueve[n]?|desv[ií]\w*|fren\w*|se explica\w*|determin\w*`.
  - Aplicar `NEG` solo a la proposición que contiene la palabra causal (dividir por «.» y «;» antes de evaluar), no a la línea.
  - Considerar C4 toda línea bajo una sección o tabla rotulada C4 (heredar la capa de la cabecera o del rótulo, como hace `revisar_texto` con `seccion`).
  - Añadir al alcance F5/fichas.md, F5/resumen.md y docs/v8/cierre_proyecto.md.
- **b)** Regex `(?:left_|right_)?on\s*=` y prohibir columnas `*nombre*|*name*` en `on`, `left_on`, `right_on`, `.map(` e `index=`.
- **c)** Exigir `b68_lo/b68_hi` en todas las filas de `atribucion_combinada.csv` con `compite == "si"` y `metodo ∈ {svar_hd, dominancia, lpiv, contabilidad}`, salvo `notas` con «sin banda (AR no acotado)».
- **d)** Exigir `metodo_ajuste ∈ {Holm, BH}`, tolerar la columna ausente como error y cubrir `M*/hipotesis_m*.csv`.
- **e)** Exigir en ERRATA.md una línea `id | sha256_nuevo` y comparar con la huella nueva, en vez de la subcadena.
- **f)** Recalcular, por (módulo, familia, mercado, periodo), el argmin del RMSE y compararlo con `destacado`.
- **g)** Abrir el hechos.json de `origen` y comprobar `id` y valor.

### K10. La congelación se puede rehacer en silencio y evaluate_v8 no exige la fecha verificable. — **mayor**

**Evidencia.**
- `f6_congelar` está en `V8_ORDEN` (Makefile:92), de modo que cada `make v8` re-estima las predicciones y **reescribe** `sha256_predicciones_v8` en docs/v8/notas_release.md sin ninguna guarda (`f6_congelar.py`, funciones `main` y `NOTAS.write_text`).
- `evaluate_v8.verificar()` compara con ese mismo fichero. Si `make v8` se ejecuta después de actualizar data/raw (con revisiones históricas o con datos de 2026T3), se congela de nuevo y la evaluación lo acepta.
- `evaluate_v8` no comprueba `fecha_verificable` (sigue en PENDIENTE), aunque §10 exige datos «publicados después de la fecha verificable».
- `congelacion.json` guarda `fecha = dt.date.today()`, de modo que el md5 cambia de un día a otro.

Pruebas en el clon, con `descargar` neutralizado y `observados` simulado:

| Prueba | Resultado |
|---|---|
| 2 de 4 trimestres | rc 0, sin apertura |
| Compra completa y alquiler con 3 trimestres | rc 0, sin apertura |
| Completo | apertura registrada antes de evaluar |
| Segunda ejecución | rc 3, se niega |

No puede abrir dos veces ni abrir con datos parciales, y no evalúa antes de registrar. El sha de notas_release coincide con congelacion.json (89c5feb6…).

**Corrección.**
- En `f6_congelar.main()`: si existe output/v8/congelacion/congelacion.json, recalcular y, si el sha conjunto difiere, salir con error salvo `--recongelar` (que exige una fila nueva en desviaciones.md). No tocar notas_release.md si ya contiene un sha distinto de PENDIENTE.
- Fijar `fecha` a una constante (la de la congelación).
- En `evaluate_v8.main()`: exigir `fecha_verificable` distinta de PENDIENTE.
- Comprobar con `git log -1 --format=%cI -- output/v8/congelacion/predicciones_congeladas.csv` que la congelación es anterior a esa fecha.
- La descarga escribe en data/raw/v8_eval, y data/raw es de solo lectura: usar data/eval_v8/ o declararlo (menor).

### K11. Etiquetas de banda. — **menor**

- por_que_ha_subido.md:106. La sección declara «banda del 68 % entre paréntesis» (línea 84), pero «(-57,3 a 9,9 pp)» de H8-4 es el **intervalo al 95 %**: escribir «(intervalo al 95 %: -57,3 a 9,9 pp)».
- por_que_ha_subido.md:93 y :128, informe_econometrico.md:48 y :60, y verificador V8-V8: la banda de la «parte no atribuida» es la suma de los límites. Añadir «banda aproximada».
- Verificador V8-V4: en el alquiler de P5, el punto −0,22 queda fuera de su banda (−0,21 a 0,01) y no se declara.

### K12. Redacción del resultado principal. — **menor**

- por_que_ha_subido.md:9: «es 2 de los cuatro exigidos en el periodo más reciente» → «es 2 de 4 (se exigen 3); también en compra P3 y P4 y en alquiler P2».
- Líneas 90 y 140: «la única contribución de todo el estudio cuya banda … excluye el cero» → «la única contribución **del SVAR**…». M1 en P1 y P2 y varias cifras SHAP también excluyen el cero.

### K13. Cierre del proyecto (punto 6 del encargo). — **menor**

Cumple los seis puntos: qué responde y con qué capa (§1); qué no pudo hacerse (§2); datos nuevos y quién los tiene (§3); qué revisar antes de difundir (§4); qué necesita la fase de propuestas (§5); declaración de última versión (§6).

Correcciones de contenido:
- K2, K3 y K5 en §1 y §2.
- §1: «cinco shocks … en P1-P5». En P1 (versión larga) hay tres.
- §4: añadir «comprobar K1-K10 de docs/v8/revision_final.md».
- notas_release.md, punto 4: «F4 congela» → «F6 congela».

### K14. M6: «bandas bootstrap por bloques centradas» (informe_econometrico.md:83). — **menor**

10 de los 152 puntos principales (24 en total) quedan fuera de su banda del 68 % aunque las bandas sean «básicas». Escribir «bandas bootstrap básicas; 10 puntos principales fuera de su banda del 68 % (sesgo del R² remuestreado)».

### K15. Anotaciones «antes de calcular» que git no puede verificar. — **menor**

- desviaciones.md, líneas 72-73 del fichero: commit f20ab0d, el mismo que los resultados de F5.
- Y10: commit 7b00215, el mismo que M2/prob_mayor.csv.
- IV2b: J14 sin re-rotular.

Añadir a cada una «anotada en el mismo commit que los resultados (no verificable)». No cambian ninguna designación.

### K16. Otros. — **menor**

- por_que_ha_subido.md:144: «se formaron más hogares que viviendas terminadas» → «… que viviendas **libres** terminadas (faltan las protegidas; M4)».
- evaluate_v8: `bvar_m2` se evalúa con la mediana y el resto con la media (`punto`). Declararlo en el resultado.
- por_que_ha_subido.md:201: «la propia inercia del precio contiene casi toda la información útil» → «… contiene más información útil que los modelos con factores probados aquí».

### K17. Lo que no hace falta tocar. — información

- Holm por familias:
  - {H8-1..4}: 0,987 / 0,987 / 0,838 / 0,343;
  - {H8-5..7}: 1 / 1 / 1 (p = 0,724 / 0,635 / 0,536);
  - {H8-8, H8-9}: 0,669 / 0,020.
  Son coherentes con hipotesis_m*.csv y cifras_clave.
- Tabla común fuera de muestra: AR(4) es la base más exigente en ambos mercados. El BVAR (1,37 frente a 1,18; 0,98 frente a 0,80) y el ECM v1 son peores. En M4, la especificación A2 del alquiler (0,705 frente a 0,726) no mejora con DM-HLN (p = 0,995).
- Ningún modelo destacado se elige por su p: los 85 llevan motivo «(b) … fuera de muestra» y «NO CUMPLE LA REGLA».
- Referencias del verificador: marcadas «NO VERIFICADAS (DOI Crossref y cuartil Scimago pendientes)». Correcto.

## 4. Orden de corrección propuesto

1. K1, K2, K3, K4, K5, K6, K7 y K8: plantillas (docs/v8/plantillas/por_que_ha_subido.md e informe_econometrico.md), f6_hechos.py (indicadores de CV, turismo y periodo de M1-P1) y cierre_proyecto.md; después, `make v8` (o la cadena F5-F6), `make check` y `make publicacion`.
2. K10: guardas de f6_congelar y evaluate_v8 (antes de la release y de anotar `fecha_verificable`).
3. K9: ampliar check_v8 y re-ejecutar `make check`. Debe detectar las líneas de K1 y K7 antes de corregirlas.
4. K11-K16: menores, en la misma pasada.
