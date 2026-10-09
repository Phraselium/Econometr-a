# Revisión independiente — Puerta F3 (inmigración y precios, P2)

Revisor: reviewer (independiente; no participó en F3). Fecha: 2026-10-09.
Material: `docs/decisiones.md` (F3 prefijada + hallazgo `trans_extranjeros`), `src/f3_inmigracion.py`, `output/f3/*`, `output/registro_busqueda_f3.csv`, `docs/literatura.md`, `data/raw`, `data/processed/panel_ccaa_a.csv`.

## Veredicto: **REHACER (acotado)**

El núcleo econométrico es correcto y lo he replicado de forma independiente. La conclusión **«asociación, no causal»** para P2 es la adecuada. Lo que hay que rehacer es lo siguiente: (i) los artefactos que están en el commit no coinciden con lo que produce el código; (ii) el resumen contiene una frase falsa frente a la literatura y otra que exagera el resultado del alquiler; (iii) la prueba de pretendencias no es una prueba «pre» para dos de los cuatro resultados. No hace falta reestimar el modelo principal.

---

## 1. Reproducibilidad

| Comprobación | Resultado |
|---|---|
| `python3 src/f3_inmigracion.py` ×2 en una copia aislada (`git archive HEAD`, sin red: proxy anulado, FORCE sin definir) | **md5 idénticos** en los 43 ficheros de `output/f3/` y en `registro_busqueda_f3.csv`. 149 especificaciones. ~50 s por ejecución. El código es determinista. |
| Artefactos del commit HEAD (004ea86) frente a esa ejecución limpia | **NO coinciden.** `git show HEAD:output/f3/resumen_f3.md` dice «Especificaciones registradas en F3: **126**», y en la tabla de Holm faltan las filas `PAN_serpavi_FE_2SLS` y `PAN_ipc_alq_FE_2SLS`. El `registro_busqueda_f3.csv` de HEAD tiene 144 filas; el que genera el código tiene 149. |
| Ejecución en el repo compartido | Mi segunda ejecución coincidió con `make all`/`make models` lanzados por otros agentes (procesos 3754 y 3070). El resultado fue un `registro_busqueda_f3.csv` con 195 filas, ids duplicados y un `resumen_f3.md` distinto. En este momento el árbol de trabajo tiene `registro_busqueda_f2.csv` y `registro_busqueda_f3.csv` modificados por esas ejecuciones concurrentes. |
| `make all` completo | No lo ejecuté en el repo compartido, para no corromper más los registros mientras otros agentes lo están ejecutando. La reproducibilidad de F3 se comprobó en la copia aislada. |

Causa: `eu.Registry` hace `unlink` y después *append* fila a fila, y `resumen()` relee el CSV. Cualquier ejecución concurrente trunca o mezcla filas. El código está bien y el problema es de procedimiento, pero hoy el commit no es reproducible.

## 2. Datos

- **Población anual 77019, a 1 de enero.** El panel coincide con `data/raw/ine_ecp_ccaa_paises.csv` en las cifras que contrasté: C. Valenciana, extranjeros, 2002: 243.338 (raw 243.338). C. Valenciana, extranjeros, 2024: 969.602 (raw 969.602). C. Valenciana, total, 2010: 4.989.631 (raw 4.989.631).
- **Grupos.** `pob_europa_sin_espana` suma la familia UE28 entre 2002 y 2020 y la UE27 entre 2021 y 2025 (comprobado: los recuentos por año de `pob_ue28_sin_espana` y `pob_ue27_sin_espana` son disjuntos). Los 8 grupos suman `pob_extranj` con una diferencia relativa máxima del 0,016 %. Es correcto y no mezcla UE28 con UE27.
- **x_ct.** `dext / pob_total.shift(1)` agrupado por CCAA. Usa la población del año anterior: correcto. **Ojo con el calendario:** como los stocks son a 1 de enero, x del año t es el cambio neto entre el 1-ene-(t−1) y el 1-ene-t, es decir, el flujo neto durante el año t−1 (comprobado: CV 2010 = 4.989.631 = 2010T1). El resumen dice «población que llega en el año» y «contemporáneas». Es inexacto: frente al Δln de la media anual de precios, x va adelantada aproximadamente medio año.
- **Instrumento.** Cuotas FIJAS de 2002, verificado en el código: `P0 = P[P.anio == 2002]` y `s_g = P0[P_g]/ΣP0[P_g]` se aplican con `map` a todos los años. *Leave-one-out*: `nat[dP_g] − dP_g` de la propia CCAA. Los z y x de 2002 se ponen a NaN. Es correcto (Card 2001).
- **`trans_extranjeros`.** Raw MIVAU 340101i0, nacional: 2007 = 35.111, 2008 = 18.213, 2009 = 26.832. Panel, suma de 17 CCAA: 35.090, 18.180 y 26.784. Coincide con la nota de `decisiones.md` (compradores extranjeros RESIDENTES y salto 2008→2009).
- **Valor tasado por CCAA desde 1995** (`mivau_valor_tasado_nacional_ccaa_prov.csv`): permite una prueba de pretendencias anterior al año base (ver §3).
- Defecto menor en documentación (F1): `docs/diccionario_variables.md` (líneas 204 y 234) muestra los marcadores sin sustituir `{last_pob_e}` y `{dif_eu.max():.0f}`. Falta el prefijo `f` en `src/build_dataset.py` (líneas 1521 y 1558).

## 3. Econometría e identificación

**Re-estimación independiente** (linearmodels `IV2SLS`, dummies de CCAA y de año, cluster CCAA):

| Resultado | n | 2SLS (yo) | 2SLS (F3) | OLS (yo) | F primera etapa (yo / F3) |
|---|---|---|---|---|---|
| Δln IPV 2008+ | 306 | −1,615 | −1,615 | −0,454 | 21,4 / 17,9 |
| Δln valor tasado 2003+ | 386 | −0,875 | −0,875 | 0,361 | 62,9 / 53,2 |
| Δln IPC alquiler 2003+ | 391 | 0,437 | 0,437 | 0,534 | 64,2 / 54,4 |
| Δln SERPAVI 2012+ | 198 | 0,554 | 0,554 | 1,217 | 13,2 / 10,6 |

Los coeficientes son idénticos. Los EE y la F de F3 son unos 6 % y 16 % más conservadores, porque la corrección de muestra pequeña cuenta en K los efectos fijos de CCAA, que están anidados en el cluster. No es un error: es una opción conservadora que conviene documentar. La comparación OLS/2SLS se hace en la misma muestra dentro de cada resultado (verificado).

- **Primera etapa.** F entre 10,6 (SERPAVI) y 54 (valor tasado e IPC). Con un solo instrumento y un solo regresor endógeno, la F efectiva de Montiel Olea-Pflueger coincide con la F de Wald robusta. Hay que quitar la frase «no se implementó» o explicar esa equivalencia. La forma reducida, equivalente a Anderson-Rubin y robusta a instrumentos débiles, no rechaza en ningún resultado (p de 0,19 a 0,51). Conviene decirlo expresamente.
- **Rotemberg.** Ningún grupo domina por sí solo, pero dos concentran alrededor del 80 % del peso:
  - IPV: América α = 0,50 y Europa α = 0,31. Europa, con β_g = −3,39 (p = 0,016), aporta ≈ −1,07 de los −1,615.
  - Valor tasado: Europa α = 0,43 y América α = 0,39. Europa β_g = −2,45 (p = 0,024).
  - IPC alquiler: lo mueve América (α = 0,39, β_g = 0,975), que es justo el grupo cuya cuota de 2002 tiene pretendencia significativa (Holm p = 0,014).

  El *jackknife* sin Baleares baja el 2SLS del valor tasado a −0,06. El signo negativo parece venir de la cuota europea de 2002, muy ligada a regiones de costa e islas con demanda de residentes y turística. Eso amenaza la exclusión y no es un error de código.
- **Pretendencias.** Para valor tasado e IPC alquiler, la ventana 2003-07 está DENTRO de la muestra de estimación (2003+) y es posterior al año base: no es una prueba «pre». Solo lo es para el IPV (2008+). Además, la sección cruzada y el panel con FE de año dan el mismo coeficiente (−1,404), así que no son pruebas independientes. **Comprobación propia con raw MIVAU:** media de Δln del valor tasado 1996-2001 por CCAA sobre zbar 2008-25 da 9,46 (EE HC3 6,26; p = 0,13). Sobre las cuotas de 2002, una a una, p entre 0,43 y 0,996. No rechaza, pero es imprecisa. Hay que añadirla como pretendencia propiamente dicha.
- **J de Hansen.** Con 17 clusters y 5 instrumentos tiene muy poca potencia. Su advertencia es correcta y no rechazar no aporta información.
- **Wild cluster bootstrap.** WRE simplificado (residuos de la forma reducida sin restringir), Webb, 9.999 réplicas. Ningún 2SLS de la especificación principal sobrevive (p de 0,12 a 0,49). Sí sobrevive el OLS de IPC alquiler y SERPAVI (p = 0,004 y 0,007).
- **Sobreajuste.** 149 especificaciones. El mínimo de Holm es 0,051 (`NAC_ANUAL_A1`) y **nada sobrevive**. `PAN_ipc_alq_FE_OLS` tiene Holm 0,59. Holm se aplica a una familia que mezcla pruebas de diagnóstico (pretendencias, J) con efectos. Es conservador; basta con decirlo.
- **Pruebas propias de submuestra (no registradas, solo para la revisión):**
  - IPV 2014+: 2SLS −1,69 (EE 1,26).
  - IPV hasta 2013: −2,25.
  - Valor tasado 2003-07 (auge): **+5,39** (EE 3,83; F 8,3).
  - Valor tasado 2003-13: +0,62.

  Es decir, en el periodo comparable a González-Ortega el signo es positivo, aunque impreciso y con instrumento débil.
- **Proyecciones locales nacionales.** Correcto: HAC(h+4), muestra común fijada en h = 8 para todos los h, Δ4 por la MA de la interpolación semestral.
  - Lo que falta comentar: Chow 2014Q1 p < 0,002 en IPV (Bai-Perron detecta un quiebre en 2013Q2-Q3). Chow 2020Q1 p < 0,03 en alquiler. VIF de 17,9 en alquiler. Chow 2022Q3 sale NaN porque la muestra acaba en 2024Q2.
  - El regresor Δ4 ln pob. extranjera es muy persistente y la respuesta del alquiler crece de forma monótona. Es un patrón compatible con una tendencia común.
  - La variante `x_flow` (Δ4 extranjeros / población total, la misma unidad que la literatura) da 1,26 en alquiler a h = 8 (p = 0,028) y nada en IPV. Esa es la que hay que citar al comparar con Saiz.
- **Flujo anual nacional.** 10,65 con N = 17. Es un orden de magnitud mayor que el panel: es una covariación cíclica (auge-crisis), no un efecto. Hay que decirlo.
- **Canal comprador.** −42 en 2SLS (OLS −19). Sin 2008-09 (2010+) sigue en −24,7 (EE 6,4), y en compras totales es −16,5 (EE 5,2). Por tanto **no es solo un artefacto de la serie** de residentes ni del salto 2008→09. El instrumento predice el desplome local de transacciones, algo que la inmigración no puede explicar con esa magnitud. Es una señal en contra de la exclusión (z correlacionado con el ciclo inmobiliario local) y refuerza que todo P2 debe leerse como asociación.

## 4. Signos y magnitudes frente a la literatura

- Unidad: coeficiente = variación en % del precio por un flujo neto del 1 % de la población total del año anterior. Es la **misma unidad que Saiz (2007)** («inflow equal to 1% of the city population → ~1%»), con dos matices: x es el cambio neto del stock padronal (resta las nacionalizaciones) y es anual.
- **Discrepancia (marcar):** IPV 2SLS −1,615, EE 1,078. IC95 % con t(16): **[−3,90; 0,67], que excluye +1 (Saiz) y el ≈3 derivado de González-Ortega.** La frase del resumen «intervalos que incluyen tanto +1 como valores negativos en precio» es **falsa para el IPV**. Es cierta para el valor tasado ([−2,89; 1,14]) y para SERPAVI.
- González-Ortega: el cociente 52/17 ≈ 3 tiene como denominador la población en edad de trabajar. Por punto de población total el cociente sería mayor. Además es un efecto acumulado de 1998-2008, en pleno auge, a nivel provincial.
- ¿Error, diseño o resultado legítimo? **No es un error** (replicado). Es **diseño y periodo**: la muestra de 2008 en adelante es de crisis y recuperación, la estimación es anual y no de diferencias largas, la variación de x es neta, y el peso de Rotemberg recae en la cuota europea de 2002 (costa e islas). En el auge 2003-07 el signo es positivo. El signo negativo es compatible con Sá (2015, −1,6 % por 1 %, salida de nativos), pero no hay evidencia del mecanismo.
- Alquiler: IPC 0,44 (2SLS) y 0,53 (OLS). Mismo signo que Saiz y algo menor. Ninguno es robusto a búsqueda ni a pretendencias.

## 5. Referencias

- Verificadas por mí en la web: Saiz (2007) (resumen IZA DP 2189 / Penn: «1% → ~1%», JUE 61(2) 345-371). González y Ortega (2013) (IDEAS/IZA DP 4333: 17 % → 52 %, 37 % de la construcción, JRS 53(1) 37-59). Sá (2015) (EJ 125(587) 1393-1424, signo negativo). La cifra de −1,6 % sigue siendo del DP 5893 y ya figura como no comprobada en la versión publicada, lo cual es correcto.
- Card (2001), GPSS (2020), BHJ (2022), AKM (2019) y Accetturo et al. (2014): los datos bibliográficos de `literatura.md` son coherentes. No los he vuelto a verificar en la web en esta revisión.
- **El resumen cita referencias metodológicas que NO están en `docs/literatura.md`:** Webb, Davidson-MacKinnon (WRE), Driscoll-Kraay, Montiel Olea-Pflueger, Sanderson-Windmeijer, Kleibergen-Paap y Hansen. Hay que añadirlas verificadas o marcarlas **NO VERIFICADA**.

## 6. ¿«Asociación» es correcto para P2?

Sí. Ningún 2SLS principal sobrevive al wild bootstrap, nada sobrevive a Holm, la pretendencia del alquiler falla en el grupo que lo mueve, el canal comprador apunta a que se viola la exclusión y el J no tiene potencia. Precisión necesaria: en precios de compraventa (IPV y valor tasado) **no hay ni asociación significativa**. La formulación correcta es «sin evidencia de efecto positivo; el 2SLS del IPV es incompatible con +1 al 5 %». En alquiler: «asociación positiva en OLS (≈0,5), frágil».

## 7. Cambios necesarios, priorizados

1. **Reproducibilidad del commit.** Regenerar `output/f3/` y `registro_busqueda_f3.csv` con una ejecución aislada; deben salir 149 especificaciones y md5 iguales a los de esta revisión (`resumen_f3.md` 8249895e…, registro 72116fd8…). Hacer commit solo de eso. Restaurar `registro_busqueda_f2.csv` y `registro_busqueda_f3.csv` en el árbol de trabajo. Serializar las ejecuciones: `flock` en el Makefile, o que `Registry` acumule en memoria y escriba al final.
2. **Corregir el párrafo de comparabilidad del resumen.** Sustituir «intervalos que incluyen tanto +1 como valores negativos en precio» por los IC de t(16) por resultado: IPV [−3,90; 0,67], que excluye +1 (Saiz) y ≈3 (González-Ortega); valor tasado [−2,89; 1,14]. Explicar la discrepancia como diseño/periodo, con el peso de Rotemberg de Europa y el *jackknife* de Baleares. Para la comparación nacional, citar `x_flow`, que está en la misma unidad.
3. **Reformular «el único resultado robusto es la asociación positiva con el IPC de alquiler (OLS y 2SLS similares)»** como: «asociación positiva en OLS (0,53; WCB p = 0,004), que no sobrevive a Holm (0,59); 2SLS 0,44, no significativo (WCB p = 0,12); el IPC alquiler no estaba en el diseño prefijado; lo mueve el grupo América, con pretendencia significativa». Anotar en `decisiones.md` que el IPC alquiler se añadió después del diseño prefijado.
4. **Pretendencias.** Renombrar la prueba 2003-07 como «correlación en los primeros años de la muestra» (solo es «pre» para el IPV). Añadir la pretendencia real 1996-2001 del valor tasado por CCAA (raw MIVAU) sobre zbar y sobre las cuotas, y registrarla.
5. **Canal comprador y calendario de x.** Llevar al resumen la nota de `decisiones.md` (residentes, salto 2008→09). Añadir que sin 2008-09 sigue en −24,7 y que en compras totales es −16,5, así que es una señal contra la exclusión del instrumento y no solo un artefacto de la serie. Cambiar «población que llega en el año»/«contemporáneas» por «flujo neto durante el año t−1 (stocks a 1 de enero)».
6. Menores:
   - Etiquetar las filas x_t / x_{t−1} en las tablas de rezago (ahora no se distinguen). El 2SLS del valor tasado da +3,5/−4,3 con p < 0,002; ninguno sobrevive a Holm.
   - Explicar que F efectiva = F robusta con un instrumento, y presentar la forma reducida como prueba Anderson-Rubin.
   - Documentar la corrección de muestra pequeña con FE anidados.
   - Comentar los quiebres de las LP (2013-14 en IPV, 2020 en alquiler) y que el flujo anual nacional (10,65) es cíclico.
   - Añadir las referencias metodológicas a `literatura.md` o marcarlas NO VERIFICADA.
   - Corregir los marcadores sin sustituir del diccionario (`build_dataset.py`, líneas 1521 y 1558).

---

## Re-revisión (iteración 2) — commit 3a6e3ef

**Veredicto final: APROBAR.**

- **Determinismo.** Copia aislada (`git archive HEAD`, sin red, FORCE sin definir), dos ejecuciones: md5 idénticos en todo `output/f3/` y en el registro. Los ficheros coinciden byte a byte con los de HEAD. Registro: 150 especificaciones, sin ids duplicados. Holm mínimo 0,051: nada sobrevive.
- **Cambios 1-5 aplicados y comprobados en `resumen_f3.md`:**
  - IC95 por resultado; el del IPV, [−3,90; 0,67], excluye +1 y ≈3, con la explicación de diseño y periodo (Rotemberg de Europa, Baleares).
  - 2SLS 2003-07 del valor tasado = 5,39, registrado. Su EE es 4,56 frente a mis 3,83 y su F 5,8 frente a 8,3, por la corrección conservadora con FE anidados. Es coherente.
  - Eliminado «único resultado robusto»; el IPC alquiler queda anotado como posterior al diseño en `decisiones.md`.
  - Pretendencias renombradas. La 1996-2001 se cita como cálculo externo de la revisión, lo cual es aceptable por la regla de leer solo de `processed`.
  - Canal comprador presentado como posible violación de la exclusión, y x_t descrito como flujo durante t−1. Las filas de rezago están etiquetadas y la F efectiva está explicada.
- **Pendientes no bloqueantes:**
  - El texto dice «Holm sobre las 149 especificaciones»; ahora son 150.
  - Llevar el valor tasado por CCAA de 1995-2001 a `data/processed` y calcular la pretendencia en el script.
  - Verificación de las referencias metodológicas (lit-researcher en curso).
  - Marcadores sin sustituir en el diccionario (`build_dataset.py`).
