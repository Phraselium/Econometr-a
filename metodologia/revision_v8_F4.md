<!-- Generado por `make publicacion` desde docs/v8/revision_F4.md. No editar a mano: se regenera y un test lo comprueba. -->

# Revisión independiente de la PUERTA F4 de V8 (módulos M0-M9)

- Fecha: 2026-10-13. Revisor independiente; no ha participado en el trabajo revisado.
- Commit revisado: 213ac84 (r8/main). HEAD al revisar: 2be68ea, que solo cambia docs/v8/estado.md.
- Alcance:
  - documentos: CLAUDE.md, docs/v8/{hipotesis, desviaciones, decisiones, contrato_salidas, revision_F3}.md y output/v8/F3/*/validacion.md;
  - código: src/v8/m*_*.py y src/v8/herramientas/{lp, regimenes}.py;
  - salidas: output/v8/M0-M9.
- No se ha leído data/sealed. Solo se ha escrito este fichero; ni el código ni las salidas del repositorio se han modificado.
- Las re-ejecuciones se han hecho en clones aislados en el scratchpad, sin red (HTTPS_PROXY=http://127.0.0.1:9).

## 0. Veredicto

**Global: APROBAR CON CORRECCIONES. F5 queda bloqueada hasta cerrar J1, que obliga a rehacer M2.**

| Módulo | Veredicto | Hallazgos principales |
|---|---|---|
| M0 periodos | APROBAR CON CORRECCIONES | J8 (mayor), J9 (mayor), J22 |
| M1 factor común | APROBAR CON CORRECCIONES | J19, J21 |
| M2 SVAR | **REHACER** | **J1 (bloqueante)**, J2 (mayor), J20, J22 |
| M3 LP por periodo | APROBAR CON CORRECCIONES | J17, J22 |
| M4 largo plazo y contabilidad | APROBAR CON CORRECCIONES | J10 (mayor), J11 (mayor), J7 (mayor) |
| M5 instrumentos | APROBAR CON CORRECCIONES | J3 (mayor), J4 (mayor), J18 |
| M6 colinealidad y dominancia | APROBAR CON CORRECCIONES | J5 (mayor), J7 (mayor), J16 |
| M7 multiverso | APROBAR CON CORRECCIONES | J6 (mayor), J15 |
| M8 regional | APROBAR CON CORRECCIONES | J19, J20, J23 |
| M9 ML (contraste) | APROBAR CON CORRECCIONES | J12 (mayor), J13 (mayor), J7, J21 |

Lo que está bien, y no hace falta tocar:
- data/sealed no se usa en V8: ningún `sealed` ni `holdout` en src/v8 ni en tests/v8, y src/holdout.py y src/econ_utils.py no han cambiado desde `prereg-v8`.
- Las familias confirmatorias de Holm están bien calculadas, comprobado a mano:
  - {H8-1..4}: 0,428 / 0,816 / 0,816 / 0,816;
  - {H8-5..7}: 0,827 en las tres;
  - {H8-8, H8-9}: 0,669 / 0,020.
- No hay lenguaje causal fuera de M2 (C3s): se buscaron «causa», «provoca», «impulsa», «efecto de», «explica la subida» y «motor» en todos los resumen.md. SHAP, dominancia, Granger y DML se rotulan siempre como C4 o contraste.
- La validación temporal es por bloques con embargo de 4 (TimeSeriesSplit con gap = 4), y el escalado se ajusta dentro de cada pliegue (M6 y M9).
- Hiperparámetros de M9 dentro del presupuesto declarado: LightGBM A y B, con y sin monotonía, y GAM con α = 10 y α = 100 (m9_ml.py:61).
- M7 está dentro del tope: 37.980 especificaciones (≤ 50.000), y las fallidas quedan registradas.

## 1. Comprobaciones reproducidas por el revisor

| Comprobación | Resultado |
|---|---|
| Determinismo de M0, M1, M3, M4, M5, M6, M7 y M8 (clon de 213ac84 con data/processed/v8 y data/raw/v8 copiados; sin red; un hilo) | rc = 0 en todos. `git diff` contra las salidas versionadas: **solo cambian los campos de tiempo**: `segundos` / `tiempo_s` en M0, M3, M4, M5, M6 y M7 resultado.json, M1 y M8 tiempos.json y la última línea de M5 resumen.md. Los CSV, el PNG de M7 y los registros son idénticos byte a byte. Ver J22. |
| Determinismo de M9 (81 s) y M2 (448 s), en el mismo clon | rc = 0. Solo cambian `tiempo_s` (M9 resultado.json) y M2 tiempos.json. En M2, las mismas ESS (V3: 730 aceptadas y ESS 671; V1: 736 y 643) y predicciones_congeladas.csv con el mismo md5 que el versionado (8b17baa9…). |
| Replicación de la «parte determinista» de M2 con MCO (VAR(2), las mismas 7 variables, la misma muestra 2004T2-2026T1, constante + covid + epa2021) | Determinista acumulado de p en P5 = **+17,8 pp**, idéntico a la mediana bayesiana (+17,8). Sin `epa2021`: +2,3. Con `epa2021` como impulso en 2021T1: +1,6. Ver J1. |
| M2 V3 completo (ESS 657) con `epa2021` como impulso en 2021T1 (copia aislada con dos líneas cambiadas; ver J1) | Determinista de P5 en compra: +0,9 [−8,8; 11,8] (antes +17,8 [1,5; 34,1]). Holm: H8-1 0,99, H8-2 0,99, H8-3 0,84, H8-4 0,34; ninguna se rechaza, igual que antes. |
| Cálculo independiente del p unilateral de AR en H8-5 y H8-6 (con las funciones de src/v8/herramientas/lp.py) | Se reproduce el p publicado (0,276 y 0,365) con el signo ESTIMADO de π (π̂ = −0,93 y −0,49). Con el signo a priori (π > 0) el p es 0,724 y 0,635. Ver J3. |
| Script ad hoc de conformidad con contrato_salidas.md (columnas, factores, periodos, capas, claves duplicadas, punto dentro de su banda) | Ver J19-J21 y la tabla de §3. |

## 2. Hallazgos

Severidad:
- **bloqueante:** hay que corregirlo antes de F5;
- **mayor:** hay que corregirlo o declararlo antes de F5, porque cambia la lectura o la regla de §9;
- **menor:** documentación o trazabilidad.

### J1. M2: la ficticia EPA 2021 es un escalón en las 7 ecuaciones de un VAR en tasas. La «parte determinista» de +17,8 pp en P5 es un artefacto. — **BLOQUEANTE**

**Evidencia.**
- Código y datos:
  - `src/v8/f1_paneles.py:476` define `epa2021 = 1` desde 2021T1 (escalón).
  - `src/v8/m2_svar.py:104,169` la mete como exógena en todas las ecuaciones del BVAR, cuyas variables son tasas trimestrales.
  - `m2_svar.py:466` la mantiene igual a 1 en las predicciones congeladas.
- Efecto del escalón: equivale a un cambio permanente de la tasa media de crecimiento de las 7 variables desde 2021T1. Absorbe la media de 2021-2026 (p: −0,25 pp/trimestre en 2004T2-2020T4 frente a +0,69 en 2021T1-2026T1). Coeficiente MCO de epa2021 en la ecuación de p: +0,36 pp por trimestre.
- P5 (15 trimestres) cae entero bajo el escalón. La propagación dinámica da +17,8 pp, que coincide con la mediana bayesiana.
- El mismo mecanismo empuja la constante a la baja en los periodos anteriores: determinista −9,6 en P2 y −8,5 en P3, frente a −3,9 y −1,2 sin el escalón (MCO).
- La versión larga, que no lleva la ficticia EPA, da un determinista de +5,8 en P5.
- Lo que dice el pre-registro: §3 pide una «variable ficticia de nivel en las variables EPA». En un VAR en tasas, un salto de nivel de la EPA es un IMPULSO en Δe en 2021T1, no un escalón en todas las ecuaciones.
- Con el impulso (re-ejecución del revisor, V3 completo):

| | P5 compra | P5 alquiler |
|---|---|---|
| determinista, antes → ahora | +17,8 [1,5; 34,1] → +0,9 [−8,8; 11,8] | −8,4 → −3,8 [−6,6; −0,9] |
| crédito | −0,4 → +3,4 | |
| demanda | 0,3 → 2,4 | |
| oferta | 0,1 → 1,8 | |
| actividad | 1,1 → 1,1 | |

  En H8-2 cambia el signo de la mediana (de −0,41 a +3,37). Las decisiones de Holm no cambian.
- Las predicciones congeladas (§10) llevan dentro el desplazamiento de la media posterior a 2021.
- El Monte Carlo de F3 (validacion.md, línea 148) también modeló la ficticia como efecto sobre la tasa: valida la mecánica, no la especificación.

**Respuesta a 5a.**
- Sí, es un artefacto. No es «crecimiento tendencial».
- La identidad de la descomposición histórica se cumple en cada sorteo (error 8,2e-13).
- Pero las medianas no suman la variación observada (J2).

**Corrección.**
1. Re-especificar `epa2021` en M2 como impulso en 2021T1. Hay dos opciones; la (a) es la más fiel a §3:
   - (a) solo en la ecuación de e;
   - (b) en todas las ecuaciones, como impulso.
   
   Revisar también `robust_sin_covid`, V1 y V2.
2. Rehacer M2 completo: V3, variantes, robustez, H8-1…H8-4, atribucion.csv y hd_periodos.csv.
3. **Re-congelar** las predicciones (nuevo sha256) antes de la release; todavía no hay datos 2026T3+ vistos.
4. Anotar en desviaciones.md que es una corrección de implementación respecto al texto de §3, detectada tras ver resultados.
5. Publicar ambas versiones de H8-1…H8-4: la corregida como principal y la anterior como «especificación errónea, retirada». Que Holm no cambie de decisión no exime de declararlo.
6. Revisar el mismo uso del escalón como control en M3 (`m3_periodos_var.py:102`) y en M6/M7 (`m67_comun.py:183`), donde las regresiones son en tasas interanuales; ahí debería ser un impulso de 4 trimestres. Severidad menor en esos módulos.

### J2. M2: las medianas por factor no son aditivas y no se debe repartir sobre ellas. — **mayor**

**Evidencia.**
- La suma de las medianas de V3 frente a lo observado:
  - compra P2: −32,1 frente a −44,0 (faltan 12 pp);
  - compra P5: 19,7 frente a 18,4;
  - alquiler P4: −7,9 frente a −9,3.
- `pct_total` = mediana / observado (hd_periodos.csv), así que los porcentajes tampoco suman 100.

**Corrección.**
- Para F5, la contribución puntual será la **media posterior** (es aditiva sorteo a sorteo). La mediana y las bandas se dan aparte.
- El ranking «mayor contribución» se calcula **sorteo a sorteo**, como P(f es la mayor | datos) (véase §5).

### J3. M5: el p unilateral de Anderson-Rubin usa el signo ESTIMADO de la primera etapa, que es el contrario al esperado. La β negativa de H8-5 y H8-6 se lee al revés. — **mayor**

**Evidencia.**
- `herramientas/lp.py:181-197` y `:224-227`: `ar_p_menor` usa `signo_pi = sign(π̂)`. El docstring declara que eso solo vale «si ese signo se da por conocido».
- En la regresión agregada h = 4-8: π̂ = −0,93 (compra) y −0,49 (alquiler), con F = 1,83 y 0,77.
- La forma reducida es positiva: t_AR(0) = +0,60 en compra y +0,34 en alquiler. Es decir, tras un shock contractivo el precio sube en la muestra, lo contrario de H8-5 y H8-6.
- Con el signo a priori (π > 0, el que §6 da por conocido), p = 0,724 (H8-5) y 0,635 (H8-6), frente a los 0,276 y 0,365 publicados.
- La β = −8,78 publicada es el cociente de dos estimaciones con signo «equivocado». No es evidencia, ni siquiera débil, a favor de H8-5.
- En H8-7 (`m5_lpiv.py:248-250`, `ar_p_mayor`) pasa lo mismo, con F = 0,05.
- Además, el resumen da π y t de una regresión distinta (`signo_primera_etapa`, sin retardos y con HAC(2)) a la del F (agregada, con retardos y con HAC(9)), y los mezcla en la misma frase.

**Corrección.**
- Calcular los p unilaterales de H8-5, H8-6 y H8-7 con el signo a priori de π (+), y declararlo.
- Rehacer Holm. La decisión no cambia: no se rechaza ninguna.
- En hipotesis_m5.csv y en el resumen, añadir el signo de la forma reducida y quitar la lectura de la β.
- Unificar la regresión de la que salen π, t y F.

**Respuesta a 5d.**
- El F efectivo de Montiel Olea-Pflueger con un instrumento es el F de Wald robusto, y está bien calculado (`_iv_primera_etapa`; reproducido).
- Mal: el AR unilateral.

### J4. M5: la atribución `lpiv` no es utilizable para §9. — **mayor**

**Evidencia** (atribucion.csv de M5):

| Fila | Contribución | Observado | Por qué no sirve |
|---|---|---|---|
| compra P2, credito_tipos | +42,4 pp | −44,0 | sale de β = −8,78, la de J3 |
| compra P1 | +26,7 [−34; 132] | | banda inútil |
| ccaa_panel P3 | `pct_total` = 10.443 % | | |
| IV3 | | | efecto relativo entre CCAA (las ficticias de año absorben lo nacional; lo dice la propia nota), no comparable con una contribución nacional |
| 18 de 23 filas | | | sin bandas, por AR no acotado |

**Corrección.** Con F < 10 y AR95 no acotado, el método `lpiv` **se abstiene** en la regla de §9 (véase §5). Las filas se mantienen como C4 informativas.

### J5. M6: `contribucion_pp` de la dominancia no tiene signo propio y reparte el 100 % de la variación. No es comparable con `svar_hd`. — **mayor**

**Evidencia.**
- `m6_colinealidad.py:284-293`: `contribucion_pp = cuota × variación`, con la cuota LMG ≥ 0 normalizada a 100 %.
  - El signo de cada contribución es el de la variación del periodo, no el del factor: en alquiler P2-P5 todas son negativas porque el alquiler real bajó.
  - Las contribuciones suman exactamente la variación observada (comprobado en todas las celdas), aunque R² < 1. En compra P1, R² = 0,733 y aun así se reparte el 100 % de los 74,8 pp.
- Hay sobreajuste con muestras cortas: compra P5 tiene n = 15, k = 7 y R² = 0,988 en una regresión interanual con solapamiento.
- 22 de 128 puntos caen fuera de su banda del 68 %. Por ejemplo, compra P1 credito_tipos 47,96 frente a [27,3; 46,9]: el bootstrap de cuotas de R² está sesgado (J16).

**Respuesta a 5c.**
- No es comparable en unidades ni en signo con la descomposición histórica.
- Solo vale como **ranking de cuota de R²** (asociación).

**Corrección.**
- Que `contribucion_pp` sea `cuota_LMG × R² × variación`, con una fila `residuo` = (1 − R²) × variación.
- Añadir una columna con el signo de la contribución parcial (β·Δx̄ del periodo).
- En §9, la dominancia vota por ranking de cuota, condicionado al signo (véase §5).

### J6. M7: el signo por familia mezcla variables con signos económicos opuestos. La única celda de compra que «cumple» deja de cumplir al orientar los signos. — **mayor**

**Evidencia.**
- resumen_multiverso.csv, compra P5 credito_tipos «TODAS»: 88 % positivo y 51 % significativo tras BH, «cumple». Junta tres variables:
  - `tipo_hip_real`: 87,5 % positivo; a más tipo, más precio;
  - `credito_nuevo_real`: 84 % positivo;
  - `credito_stock_real`: 93 % positivo.
- Un coeficiente positivo del tipo y uno positivo del crédito tienen lecturas opuestas.
- Orientando el tipo (×−1), el porcentaje con el signo mayoritario orientado es (0,125 + 0,844 + 0,927)/3 ≈ 0,63 < 0,80: **no cumple**.
- El mismo problema afecta a la condición 2 de §9 en todas las celdas de credito_tipos.

**Corrección.**
- Definir antes de F5 una orientación por variable (tipos ×−1; el resto, «más es más presión») y recalcular `pct_mismo_signo` por familia con los signos orientados.
- Añadir la regla por variable, que es como la formula §9 («de esa variable»).

### J7. Comparación con AR(4) y ECM v1 en la misma muestra: no hay un ECM v1 canónico; cada módulo usa uno distinto o ninguno. — **mayor**

**Evidencia.**

| Módulo | ECM v1 |
|---|---|
| M4 (`m4_largo_plazo.py:703`) | «no evaluable en la misma muestra» |
| M6 (`m6_colinealidad.py:163-173`) | uno «aproximado» con ocupados, costes y renta |
| M9 (`m9_ml.py:191-210`) | otro distinto, solo nacional |
| M0 | no lo incluye |

- En el repo existe `src/v7/r5_prediccion.py:m_ecm_v1` (ECM nacional, especificación A), que V7 ya usó como «ECM v1».
- El RMSE del AR(4) en compra nacional varía entre módulos: 1,04 (M6), 1,09 (M9), 1,22 (M0) y 1,28 (M4), porque las muestras de prueba son distintas.
- Dentro de cada módulo sí es la misma muestra frente al AR(4).

**¿Es aceptable?** Solo en parte.
- Ningún modelo supera al AR(4) (M0, M4, M6, M9), así que no cambia ninguna conclusión de «predice mejor».
- Pero CLAUDE.md exige el ECM v1. Que haya tres aproximaciones distintas impide decir «frente a ECM v1».

**Corrección.**
- Un único comparador `ecm_v1` (la especificación A de v7, importada, no copiada), evaluado en los mismos pliegues de cada módulo donde haya regresores.
- Donde no los haya, `no evaluable` con el motivo.
- Una tabla común en F5 con los RMSE de AR(4) en una muestra de prueba fija (5 bloques de 8 trimestres con embargo 4, que terminan en 2026T1).

### J8. M0: la tasa de paro sí está en data/raw. La sustitución por ocupados se basa en una premisa falsa. — **mayor**

**Evidencia.**
- desviaciones.md (M0) dice: «Tasa de paro no disponible en data/processed/v8 ni en data/raw como serie nacional trimestral».
- Pero `data/raw/ine_v2_epa_prov.csv` trae, a nivel nacional (código 00), `EPA_parados` y `EPA_ocupados` de 2002T1 a 2026T2 (98 trimestres), de las que sale la tasa de paro.
- Además, panel_ccaa_q_v8 tiene `parados_epa` y `tasa_paro_epa` (2007T1-2026T2, 17 CCAA, sin interpolar).
- El umbral de Hansen ya se estima con unos 93 trimestres (bajo n = 71, alto n = 22), es decir, desde 2003. El paro desde 2002 (interanual desde 2003) cubre prácticamente la misma ventana.

**Corrección.**
- Construir la tasa de paro nacional = parados / (parados + ocupados) desde data/raw. Hay que hacerlo en F1, porque data/processed no es editable por las ramas.
- Estimar el umbral con la observable pre-registrada y mantener ocupados como sensibilidad.
- Corregir la desviación (la fecha y el motivo reales).

### J9. M0: el nivel de evidencia «ASOCIACIÓN ROBUSTA» contradice §7 (BH en todo lo exploratorio). — **mayor**

**Evidencia.**
- `resultado.json` de M0 da «ASOCIACION ROBUSTA solo para los efectos que cumplen la regla».
- Los 2 que la cumplen (compra P2 PIB, p_perm = 0,040; compra P4 terminadas, p_perm = 0,049975 = 100/2001, en el límite) tienen p BH = 0,889.
- §7: «Todo lo demás es exploratorio, con BH (q = 0,10)». M0 trata BH como «informativo, no forma parte de la regla».
- La regla de §8 no menciona BH, pero §7 lo impone a todo lo no confirmatorio.
- P4 tiene 9 trimestres (3 gl).

**Corrección.**
- Nivel EXPLORATORIO (C4) para los dos.
- La etiqueta «cumple la regla de §8» se mantiene, pero con «no sobrevive a BH».
- No usar «efecto por periodo» sin el calificativo C4.

### J10. M4: la decisión ARDL-bounds ignora el contraste t. La «discrepancia ARDL frente a Engle-Granger» es sobre todo un artefacto. — **mayor**

**Evidencia.**
- cointegracion.csv:
  - alquiler A1-A4: F = 10-25 («rechaza no cointegración»), pero t(y_L1) = −1,62, −1,80, −0,67, +0,41 y +0,21;
  - la velocidad de ajuste ARDL del alquiler es +0,012 (positiva).
- Sin un t negativo y significativo (cota I(1) de PSS, caso III, k = 5, en torno a −4,2 al 5 %), no hay cointegración. La propia nota del código lo advierte (`m4_largo_plazo.py:582`), pero `decision` no lo aplica.
- Compra C4: t = −3,13 (zona no concluyente). C2 y C3: t = −4,27 y −4,78. EG y GH no rechazan en ninguna especificación.
- La semivida de 45-47 trimestres (velocidad −0,015) en compra DOLS/FMOLS equivale a que no hay corrección de error, lo que es coherente con la ausencia de cointegración.

**Respuesta a 5g.**
- La «relación de largo plazo» no está respaldada salvo, como mucho, en compra C2 y C3 por ARDL.
- Las contribuciones `contabilidad_lp` (DOLS/FMOLS) son regresiones en niveles sin cointegración demostrada.

**Corrección.**
- `decision` = rechaza solo si F > cota I(1) **y** t < cota I(1).
- Etiquetar `contabilidad_lp` como «sin cointegración demostrada» y excluirla de §9.
- Para P1, §5 combina la larga, M4 y la contabilidad: con M4 sin cointegración, P1 queda con la versión larga del SVAR como única fuente identificada.

### J11. M4: la «contabilidad hogares-viviendas» es una regresión por periodo con pendiente que cambia de signo. No es una contabilidad. — **mayor**

**Evidencia.**
- contabilidad_hogares_asociacion.csv: b por periodo = −2,21 (P1), −0,47, +0,69, −0,99 y +0,86 (P5); en la muestra completa, −0,34 (p = 0,50).
- En P1 la brecha es negativa (se terminaron 548.000 viviendas libres más que hogares nuevos) y, con b < 0, la «contribución demográfica» sale de +26,6 pp. Se lee «el exceso de oferta subió el precio», lo que es causalidad inversa.
- P4: n = 9 y p = 0,0006 con HAC (la propia nota dice «no fiable»).
- Solo produce un factor (`demografia`, que en realidad es demografía menos oferta).

**Corrección.**
- Para §9, la contabilidad vota solo por el signo de la brecha en unidades físicas (véase §5), sin pendiente estimada por periodo.
- Si se quiere una magnitud, usar una única elasticidad fijada antes de F5 (de la muestra completa o de la literatura, marcada).

### J12. M9: el punto de la atribución SHAP cae fuera de su banda. No es un error de percentiles: el bootstrap está descentrado por diseño. — **mayor**

**Evidencia.**
- `m9_ml.py:281-320`: el punto se calcula con el modelo ajustado en toda la muestra. Cada réplica se reajusta con bloques remuestreados (en torno al 63 % de trimestres únicos), pero el SHAP se evalúa en la muestra ORIGINAL, con en torno al 37 % de filas fuera de la bolsa.
- Las contribuciones de las réplicas se encogen hacia la base (atenuación fuera de la bolsa) y su residuo crece.
- Pasa en 14 de 152 filas. Por ejemplo:
  - compra P5 empleo_renta: +2,11 frente a [0,89; 1,91];
  - compra P5 residuo: 0,49 frente a [0,52; 2,86].
  
  Siempre en la dirección esperada: |punto| > |banda| en los factores y residuo del punto < banda.
- Con B = 60, el percentil del 90 % es inestable.

**Respuesta a 5b.**
- Es un descentrado del bootstrap, no un error de cálculo de cuantiles.
- La nota lo admite («pueden no contener el punto»), pero así las bandas no sirven.

**Corrección.** Hay dos opciones:
- (a) evaluar el SHAP de cada réplica solo en sus filas dentro de la bolsa;
- (b) usar bandas «básicas» centradas (2·θ̂ − q), con B ≥ 200.

Además, convertir `contribucion_pp` a la unidad del contrato (J21).

### J13. M9: la sensibilidad con turismo de compra se calcula con el panel de ALQUILER. — **mayor** (error de código)

**Evidencia.**
- atribucion.csv de M9: las filas `shap_sens_turismo` de compra y de alquiler (P2-P5 y completo) son idénticas en los 5 periodos (por ejemplo, P5: −0,209276 [−0,3096; −0,0004] en ambos mercados).
- Causa: en `m9_ml.py:541` se usa `dt = dfp.dropna(...)`, pero `dfp` (`m9_ml.py:456`) es la variable del primer bucle, que al terminar contiene el panel de alquiler.
- Además, hay filas de turismo en P2 y P3, cuando el turismo solo existe desde 2016T4: el SHAP de NaN nativos describe la rama de valores ausentes, no el turismo.

**Corrección.**
- Guardar el panel en `contexts` y usarlo.
- Reportar el turismo solo en los periodos con cobertura (P5, y P4 parcial).

### J14. Desviaciones declaradas en el mismo commit que los resultados o con un motivo inexacto. — **menor** (salvo J1 y J8)

| Desviación | Commit | Resultados afectados | Valoración |
|---|---|---|---|
| Identificación V3 en M2 | 437d1cb (09:31) | 7c8f803 (09:39) | Anterior. El criterio de viabilidad ya estaba en estado.md (98295da) y el sondeo dio 0 aceptadas en 9·10⁶ rotaciones. **Aceptable.** Conviene añadir que los datos rechazan la tabla h = 0-1 (el Monte Carlo de F3 daba 9,9e-5 por rotación con un DGP compatible), lo que es en sí un resultado. |
| M3 principal = LP por periodo | 344457d, el mismo commit que los resultados de M3 | | No verificable «antes». Coherente con Y6 (437d1cb, anterior). Aceptable. |
| M0 (paro, representantes, permutación, confirmación) y M5 IV1-IV3 | 140f0e3 (09:38) | M0 (7cb5c51) y M5 (9cc8829), posteriores | Anterior. Correcto, salvo el motivo de J8. |
| IV2b, factor de M8 en pp, diseño de M9 y convención de M6 | 337ef5e, el mismo commit que los resultados de M1 y M8 | | IV2b: la motivación («la normalización amplifica EC y CO») sugiere haber visto el instrumento, aunque no necesariamente el resultado. Es exploratorio y no entra en Holm: aceptable, pero hay que marcarlo como «añadida tras construir el instrumento». El factor de M8 en pp no es verificable «antes». |
| Y8 (lectura de la parte determinista) | Después de ver M2 | | Declarado como tal. Queda superado por J1. |
| Motor propio de M7 | Declarado antes de M7 (337ef5e < 44abf3f) | | Contrastado en tests/v8/test_m7.py. Aceptable. |
| Convención de atribución de M6 | Antes de M6 | | La convención misma es inadecuada (J5). |
| `ms_fit` (herramienta validada en F3) cambiado en 213ac84 después de M0 | | | Las salidas de M0 son idénticas tras el cambio (lo he comprobado). Falta anotarlo en decisiones.md como cambio de herramienta posterior a F3. |

### J15. M7: 5.556 especificaciones fallidas, todas en P4 y en compra P1. — **menor**

- Las proporciones se calculan sobre las supervivientes, que sobrerrepresentan los modelos pequeños: fallan del 37 al 75 % por celda en P4 y en compra P1.
- No afecta a las 3 celdas que «cumplen» (alquiler P2 y completo demografía; compra P5 crédito), que no tienen fallidas.

**Respuesta a 5f.** Sesgan las celdas de P4 y de compra P1, no las que cumplen. La regla se aplica bien salvo por J6.

**Corrección.** Reportar además `pct_*` sobre la rejilla completa (las fallidas cuentan como «no cumple») y marcar P4 y compra P1 como «multiverso truncado».

### J16. Bootstrap de las cuotas de dominancia (M6) y de M1. — **menor**

- Los puntos fuera de su banda del 68 % (22 de 128 en M6) reflejan el sesgo del R² remuestreado.

**Respuesta a 5e.** La cuota del primer componente con T = 9-24 y N = 17 está sesgada al alza: la cuota media al azar es 0,28-0,49 (`cuota_azar_media`). Eso favorece rechazar la H0 «≤ 50 %»; como H8-8 no se rechaza (p IUT = 0,669; P2 = 0,45 y P4 = 0,46), la conclusión es conservadora y se mantiene.

**H8-9.**
- r = 0,60, y es robusto a la aproximación sin España (r = 0,58, p = 0,013).
- El rótulo «zona euro sin España» debe decir siempre «aproximación de 5 países, media simple».
- El bloque L = 8 con interanuales muy persistentes (T = 82) puede quedarse corto. Se propone, como sensibilidad, L = 12.

### J17. M3: el escalón EPA como control en LP en tasas (igual que J1). — **menor**

Además, los identificadores del registro (`compra_larga|p>i|P1|h0`) no coinciden con los de coeficientes.csv (`M3_lp_compra_larga_p>i_P1_h4-8`): 480 de 480 sin cruce. Hay que unificarlos.

### J18. M5: el «placebo» exige p_perm < 0,05, es decir, que el estadístico observado sea extremo. — **menor**

- Así funciona como un contraste de significación de la forma reducida, no como un placebo. Con instrumentos débiles, las pretendencias pasan por falta de potencia.
- Está declarado antes de estimar, de modo que se mantiene, pero se pide renombrarlo («permutación del instrumento») y no contarlo como prueba independiente.

### J19. Contrato: códigos de CCAA y unidades. — **menor**

- M8 usa `ccaa:1` … `ccaa:17` sin cero a la izquierda, mientras que `cv_prov:03` sí lo lleva. Los cruces son por código INE de 2 dígitos.
- M1 da `pct_total` en tanto por uno (0,79), y el resto en %.

### J20. Contrato: claves duplicadas en atribucion.csv sin columna de variante. — **menor**, pero F5 lo necesita

| Módulo | Duplicados (metodo, mercado, ambito, periodo, factor) | Variante solo en `notas` |
|---|---|---|
| M2 | 16 | V3 y larga |
| M4 | 150 | DOLS/FMOLS × con/sin escalones |
| M8 | 90 | cov / turismo_sens |

**Corrección.** Añadir una columna `variante` (o métodos distintos, por ejemplo `svar_hd_larga`) y una columna `principal` (sí/no).

### J21. Contrato: unidades de `contribucion_pp` distintas. — **menor**

| Módulo | Unidad |
|---|---|
| M9 | media de la tasa interanual del periodo, no la variación acumulada |
| M8 | media interanual × T/4 |
| M6 | cuota × variación (J5) |

Otras diferencias con el contrato:
- coeficientes.csv de M9 tiene 24 columnas de menos.
- M4, M5 y M6 añaden columnas al final (admisible).
- Hay p sin `p_ajustado` en M1 (15), M3 (240), M4 (144), M5 (114) y M6 (30), cuando todo p exploratorio debería llevar BH.

### J22. Reproducibilidad: md5. — **menor**

Los campos de tiempo (`segundos` / `tiempo_s` en resultado.json y en el resumen de M5) impiden que dos ejecuciones den md5 idénticos. Hay que moverlos a tiempos.json, fuera de la comparación.

### J23. M8: la pendiente del factor común (≈ 1) y «145 de 153 significativos tras BH» son mecánicos. — **menor**

- El factor en pp es la media transversal reescalada e incluye a la propia CCAA (1/17).
- En F5, `factor_comun` no compite con los 7 factores pre-registrados: es un resumen de comovimiento.

## 3. Coherencia de nombres y columnas con contrato_salidas.md (script ad hoc)

| Fichero | Columnas | Factores fuera de la lista | Duplicados | Punto fuera de b68 |
|---|---|---|---|---|
| M1 atribucion | OK | — | 0 | 0 / 10 |
| M2 atribucion | OK | `demanda_vivienda` (declarado) | 16 | 0 / 68 |
| M4 atribucion | OK | — | 150 | 0 / 210 |
| M5 atribucion | OK | — | 0 | 0 / 5 (18 sin bandas) |
| M6 atribucion | OK | — | 0 | **22 / 128** |
| M8 atribucion | OK | `factor_comun` (declarado) | 90 | 0 / 1.125 |
| M9 atribucion | OK | — | 0 | **14 / 152** |
| coeficientes M0, M1, M3, M8 | OK | | | |
| coeficientes M4, M5, M6 | + columnas al final | | | |
| coeficientes M9 | faltan 24 columnas | | | |
| M2 irf, fevd, hd_periodos; M3 coef_periodo | OK (con columnas adicionales al final) | | | |

## 4. Corrección prioritaria (orden)

1. **J1** (bloqueante): impulso EPA en M2. Rehacer M2, H8-1…4, atribución y hd_periodos; re-congelar §10 con un sha256 nuevo; anotar la desviación; publicar ambas versiones de H8-1…4.
2. **J3 + J4**: p unilateral de AR con el signo a priori en H8-5…7, y rehacer Holm; `lpiv` se abstiene en §9.
3. **J6**: orientación de signos en M7 y recálculo de `cumple_multiverso`.
4. **J5, J10, J11**: unidades de la dominancia; decisión ARDL con el t-bound; contabilidad por el signo de la brecha. Todo antes de F5.
5. **J8, J9**: paro desde data/raw (vía F1) y umbral rehecho; nivel de M0 a EXPLORATORIO.
6. **J12, J13**: bandas de M9 y error del panel de turismo.
7. **J7**: ECM v1 canónico (v7 especificación A) y muestra de prueba común.
8. Menores: J14-J23.

## 5. Regla operativa para F5 (propuesta; anotarla en desviaciones.md ANTES de calcular F5)

**R0. Unidad común.**
- Para cada (mercado, periodo, ámbito), ΔY_P = suma de las tasas trimestrales reales (log ×100) en una ventana común W_P:
  - P5 = 2022T3-2026T1 en todos los métodos, para coincidir con M2;
  - P1 empieza en el primer trimestre disponible del método, declarado.
- Toda contribución c_f se expresa en esos pp y como cuota con signo, s_f = c_f / ΔY_P.
- «Mayor contribución» = mayor **c_f · sign(ΔY_P)**, es decir, la que más empuja en la dirección de la variación observada.
- Convenio de signos: positivo = el factor empuja el precio al alza. Crédito y tipos: expansivo = positivo (tipos ×−1).

**R1. Residuo y parte determinista.**
- `determinista` y `no_identificados` (M2), `residuo` (resto de métodos) y `factor_comun` (M8) se reportan siempre, con banda, y **nunca entran en el ranking** ni se reparten entre los factores.
- En cada celda se publica la cuota «no atribuida» = (determinista + no identificados) / ΔY_P.
- Si su banda del 68 % excluye el 0 y su media supera la del primer factor, el texto debe decir «la mayor parte de la variación no se atribuye a los shocks identificados».
- Esto se aplica tras corregir J1.

**R2. Voto de cada método** (condición 1 de §9: mayor contribución en ≥ 3 de 4).

| Método | Cómo vota | Cuándo se abstiene |
|---|---|---|
| `svar_hd` (M2 V3 corregido; P1 con la versión larga) | Con los sorteos: f* = argmax de la media posterior de c_f·sign(ΔY) entre los shocks identificados. Se publica además P(f* es el mayor) sorteo a sorteo. | Nunca. Si P(f*) < 0,5, se rotula «ranking incierto», pero el voto cuenta (§9 no pide más). |
| `dominancia` (M6, interanual) | Vota por el factor con mayor cuota LMG **cuya contribución parcial β_f·Δx̄_f tenga el signo de ΔY**. Si el de mayor cuota tiene el signo contrario, vota por el siguiente que cumpla. Se usa `cuota × R² × ΔY` en pp para mostrarlo (J5). | Si ningún factor tiene el signo de ΔY. |
| `lpiv` (M5) | Solo si el instrumento tiene F ≥ 10 o un AR del 68 % acotado, y su contribución supera la de todos los factores de `svar_hd`. | En los demás casos. Con los resultados actuales, se abstiene en todas las celdas. |
| `contabilidad` (M4) | Solo puede votar por `demografia`: vota si la brecha hogares − viviendas terminadas del periodo tiene el signo de ΔY y \|brecha\| ≥ 0,5 % del stock de hogares (umbral fijado ahora, antes de F5). | Si no se cumple lo anterior. No usa la pendiente por periodo (J11). |

- Una abstención cuenta como «no apoya». No se reescala el denominador: se mantiene «3 de 4», tal como está pre-registrado.
- Consecuencia que hay que declarar en F5: con `lpiv` abstenido, solo `demografia` puede reunir 3 votos (svar_hd + dominancia + contabilidad). Para cualquier otro factor, la designación es imposible por construcción y se publica un ranking.

**R3. Condición 2 (multiverso).**
- pct_mismo_signo **orientado** (J6) ≥ 80 % en la familia y en la variable principal de esa familia.
- Las fallidas cuentan en el denominador como sensibilidad; se publican las dos cifras.

**R4. Condición 3.** La banda del 68 % de c_f en `svar_hd` (corregido) excluye el 0. En P1 se usa la versión larga.

**R5. Métodos sin bandas.**
- No votan con su punto si su banda no está definida, salvo la dominancia, cuyo voto es un ranking.
- Para mostrarlos sin banda se rotulan «sin banda (AR no acotado)» y no se usan en la condición 3.

**R6. Contrastes que no votan.**
- SHAP (M9), M1 (parte europea), M8 (factor común) y la dominancia trimestral se muestran en tablas aparte, convertidos a la unidad de R0.
- M9: media interanual × T/4 como aproximación declarada.

**R7. Periodos imprecisos.** En P4 (9 trimestres) y en el alquiler de P1 (sin datos), no se designa ningún factor aunque se cumplan R2-R4. Se publica el ranking con la etiqueta «impreciso».

**R8. Trazabilidad.**
- F5 lee las atribucion.csv filtrando por `variante = principal` (J20). Cada factor designado o no designado lleva una ficha con los cuatro votos, P(f*), pct orientado y la banda del 68 %.

## 6. Determinismo: resumen

- Los 10 módulos (M0-M9) se han re-ejecutado en un clon aislado de 213ac84, sin red. Todos terminan con rc = 0.
- Todos los CSV, PNG y registros coinciden byte a byte con los versionados. Las únicas diferencias son los tiempos de ejecución (J22).
- M2 reproduce exactamente el sha256 de la congelación: el md5 de predicciones_congeladas.csv es idéntico.
- El determinismo está confirmado. La validez de la especificación de M2 no lo está (J1).
