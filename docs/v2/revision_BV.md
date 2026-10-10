# Revisión v2 — rama BV (compra), fase de entrenamiento

Revisor independiente (opus). Objeto: worktree `/home/user/wt-BV`, rama `r2/BV`, commit `9fb2830` (src/v2/bv_*.py, output/v2/BV/). Pre-registro: docs/v2/hipotesis.md en `910c42a` (sin cambios desde entonces en r2/main). Fecha: 2026-10-10.

## Veredicto: **REHACER**

El análisis de entrenamiento es sólido: reproducible, sin fuga en H2 y con lenguaje prudente. Pero la función de evaluación sellada (`evaluar_H2`), que solo se puede ejecutar UNA vez, (i) no da un resultado válido por construcción, (ii) no evalúa el modelo pre-registrado y (iii) no incluye las provincias selladas. Hay que corregirla antes de llamar a `holdout.evaluate("H2", ...)`. Los cambios son acotados: no hace falta rehacer el análisis de entrenamiento.

## 1. Reproducción (clon aislado, sin red)

- Clon local de /home/user/Econometr-a + `git fetch` de r2/BV, checkout `9fb2830`, sin data/sealed en el clon. `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`.
- `python3 src/v2/bv_main.py` y `python3 src/v2/bv_main.py --smoke`, dos veces cada uno: exit 0 en las cuatro ejecuciones.
- md5 de los 26 ficheros de output/v2/BV (incluido smoke/): **idénticos** entre las dos ejecuciones (diff vacío).
- Tras la 1.ª ejecución, `git status` estaba limpio: las salidas versionadas coinciden byte a byte con las regeneradas.
- `make models` ejecuta `src/v2/bv_*.py` en orden alfabético. `bv_h2_sellado.py` solo define funciones y no llama a `evaluate`: es seguro, pero conviene blindarlo (ver C7).
- `resumen.md` está escrito a mano (no lo genera ningún script). Sus cifras coinciden con los CSV/JSON (comprobadas: coeficientes, IC, p WCB, Holm, RMSE, DM y magnitudes de +0,09 pp y −0,44 pp).

## 2. Fuga de información

| Comprobación | Resultado |
|---|---|
| Lecturas de datos en src/v2/bv_*.py | Solo `vc.load("panel_prov_q")` y `vc.load("nacional_q_v2")` (→ `holdout.load_train`). No hay ninguna lectura de data/raw, de data/processed v1 ni de data/sealed, ni acceso a la red. OK |
| Periodos ≥ 2024Q3 en entrenamiento | `preparar_panel` recorta a `Q_TRAIN_FIN=2024Q2`. El train tiene 49 provincias (sin 11, 16 ni 45) y llega hasta 2024Q2. OK |
| Deflactor / precio real | `ln_deflactor` nacional, contemporáneo. `coste_uso_aprox` = tipo_hip − media móvil RETRASADA de 4 trimestres de la inflación del deflactor (build_dataset_v2.py:276-279): sin información futura. Es la serie SA del INE (añada actual, no en tiempo real): es una limitación, no una fuga. OK |
| Exposición 2005-2007 | Media 2005Q1-2007Q4 del importe hipotecario por habitante, fija por provincia y estandarizada (z) entre las 49 provincias de entrenamiento. Es anterior a cualquier origen de test (primer test en 2012Q1). OK. *Pero* (a) `pob_total` está interpolada log-linealmente en T2-T4 (74 % de las filas), lo que choca con la regla «interpolaciones solo en robustez», con efecto mínimo al promediar 12 trimestres; (b) la estandarización se recalcula con las provincias que reciba `preparar_panel`, y eso rompe la evaluación sellada si entran 11, 16 y 45 (ver C4) |
| Escalado/selección de los modelos C1-C6 | Reestimación por split con orígenes s+h ≤ L, embargo max(4,h)=4 y ventana expansiva (v2_common). Sin escalado aprendido. La selección de C1 usa solo la validación en bloques de entrenamiento. OK como procedimiento, pero el criterio no es el pre-registrado (ver C2) |
| Fuga transversal en la infraestructura común (no imputable a BV) | `pob_*` de 2024Q2 en el train está interpolada entre 2024-01-01 y **2025-01-01** (dato sellado). Afecta aquí solo al modelo B por periodos (exploratorio, `d4_ln_pob_*` en P4), pero **afecta a H1 (rama BA), cuyo regresor principal es Δ4 ln pob 20-34**. Hay que avisar al orquestador: en el train, las filas 2024Q2 de `pob_*` deberían ser NaN o extrapolarse solo con información ≤ 2024Q2 |
| Accesos a la muestra sellada | docs/v2/holdout_accesos.md no existe en ninguna rama ni en el historial git. `evaluate` lo crea en la primera evaluación, así que no ha habido ninguna. El revisor no tiene permiso para leer data/sealed/_accesos.log (denegado por la configuración), por lo que la comprobación es indirecta. No hay ninguna llamada a `evaluate` en el código de la rama. **H2 no ha sido evaluada.** OK |

## 3. Fidelidad al pre-registro (H2)

Pre-registro: «Δ4 ln p_tasado sobre Δ4 ln hipotecas_importe (provincial), coste_uso_aprox (nacional, identificado por interacción con la exposición hipotecaria provincial 2005-2007), Δ4 ln ocupados, FE provincia y trimestre; EE cluster provincia (+ wild cluster bootstrap); Holm sobre la familia de 7».

| Elemento | Código | Valoración |
|---|---|---|
| Dependiente | Δ4 ln p_tasado **real** (− Δ4 ln deflactor nacional) | Desviación formal no declarada. Sin efecto numérico: el deflactor es nacional y lo absorbe el FE de trimestre (H2_nominal = H2_principal hasta el último decimal). Hay que declararla y explicar que «H2_nominal» no es una robustez |
| Regresores | Δ4 ln hipotecas_importe, cu×expo, Δ4 ln ocupados; FE prov + trimestre | Coincide. El nivel de cu queda absorbido por el FE de trimestre (declarado) |
| Exposición | importe hipotecario per cápita, media 2005-07, z-score | Operacionalización razonable y única (sin búsqueda), pero no declarada en decisiones.md |
| Inferencia | CR1 cluster provincia con t(G−1) + WCB restringido con pesos de Webb, B=9.999 | Implementación revisada: restricción, FWL, residuos bootstrap y CR1 correctos |
| Holm | m=2 dentro de H2 (crédito, interacción) + Bonferroni ×7 «conservador» | El pre-registro pide Holm sobre las 7 confirmatorias. La familia de 7 solo la puede aplicar el orquestador al final. Hay que etiquetar el m=2 como «Holm intra-H2» y dejar pendiente el Holm de la familia de 7 |
| Nivel de evidencia | EXPLORATORIO, con el criterio añadido `oos_ok` (mejora del AR(4) en validación de entrenamiento) | Es conservador y aceptable, pero el resumen dice que ese criterio estaba «fijado de antemano», y no figura en hipotesis.md. Además `oos_ok` se calcula sobre C1, que no es el modelo de H2. Hay que reformular |
| p WCB = 0 | resultado.json `p_wcb.cu_x_expo = 0.0` | Con B=9.999 la cota es p ≤ 1/(B+1) = 1e-4. Hay que informarlo como «≤ 0,0001», no como 0 |

## 4. Especificaciones, presupuesto y FDR

- registro.csv: 145 filas. H2: 9 especificaciones (principal + 8 robusteces, todas en el CSV). Periodos: 68. Arbitraje: 32 (2 desviaciones × 2 resultados × 8 horizontes). Nacional en muestra: 2. OOS de panel: presupuesto declarado n_max=6 y 6 usadas (C1-C6). OOS nacional: presupuesto aparte n_max=4 y 4 usadas.
- No he encontrado configuraciones en el código que falten en el registro. La rama tiene un solo commit, así que no se pueden auditar iteraciones previas.
- El presupuesto de panel (≤6) se respeta. El nacional (4) es un presupuesto separado: el orquestador debe decidir si cuenta contra el mismo límite. Si fuera un límite global de 6, se supera (10).
- Holm (econ_utils.holm) y BH (bv_lib.bh): implementaciones revisadas, correctas (step-down / step-up con mínimo acumulado).
- Arbitraje: el Holm m=16 se aplica a la versión con «media de toda la muestra», que usa información futura dentro del entrenamiento y tiene reversión mecánica. Es exploratorio, pero la versión de referencia debería ser la de media expansiva.

## 5. Fuera de muestra (entrenamiento)

- Misma muestra: `comun()` cruza AR(4), ECM v1 y C1-C6 (n=2.209 provincia-trimestre, 46 orígenes). La nacional (46 orígenes) se contrasta frente a ar4_nacional y ecm_v1_nacional. DM-HLN por periodo (media transversal) con t(n−1). OK.
- Resultado: ningún modelo mejora significativamente al AR(4). Los que contienen las variables de H2 (C3, C4) son claramente peores (RMSE 0,0606 / 0,0602 frente a 0,0418). Está bien informado.

## 6. Lenguaje causal, datos y referencias

- Sin lenguaje CAUSAL. Se declaran explícitamente la simultaneidad (crédito en t−4: p=0,48) y la identificación solo por interacción. Retoques menores: «+1 pp de coste de uso **resta** 0,44 pp» → «se asocia con 0,44 pp menos». En las contribuciones por periodo, «explica» → «contabiliza / se asocia con», y hay que aclarar que es una descomposición estadística.
- Interpolaciones: el modelo principal solo usa `pob_total` interpolada dentro de la exposición (ver §2). Las `pob_*` interpoladas solo aparecen en el modelo B exploratorio. Los datos de PDF/OCR no se usan.
- Referencias: la rama no cita literatura (no aplica VERIFICADA/cuartil).

## 7. `evaluar_H2` (src/v2/bv_h2_sellado.py): NO es apta para ejecutarse

**(1) Degenerada por construcción (crítico).** Los orígenes de test son ≥ 2024Q3 con objetivo ≤ 2026Q2, así que hay 4 orígenes (2024Q3-2025Q2) y n=4 periodos con h=4. El factor HLN, (n+1−2h+h(h−1)/n)/n = (5−8+3)/4, vale **0**: DM = 0 y p = 1 siempre, sea cual sea el dato. Lo he comprobado con un ensayo en seco usando SOLO entrenamiento (pseudo-sellado: ajuste hasta 2022Q2 y test desde 2022Q3). Salió `dm_vs_AR4 = -0.0, p = 1.0` con 4 periodos tanto para C1 como para C3. Además, solo se evalúan objetivos 2025Q3-2026Q2: se pierde la mitad de la ventana pre-registrada.
→ Los orígenes deben ser 2023Q3-2025Q2 (objetivos 2024Q3-2026Q2, 8 periodos). Los orígenes 2023Q3-2024Q2 son de entrenamiento, pero sus objetivos están sellados y no entran en la estimación (s+h ≤ 2024Q2). En el mismo ensayo en seco con 8 periodos el contraste es informativo (C3: DM −2,68, p=0,03). Hay que añadir una comprobación: abortar *antes* de calcular el resultado si n_periodos < 8, para no gastar el único acceso.

**(2) Modelo no fiel al pre-registro (crítico).** El pre-registro dice «el modelo con estas variables» (crédito, coste de uso×exposición, ocupados) «reduce el RMSE frente al AR(4) de panel». `config_h2_sellado.json` fija **C1** (AR4 + Δ4 crédito), elegido por menor RMSE de validación: le faltan dos de las tres variables de H2, y elegir entre configuraciones es tarea de H7 (BM), no de H2.
→ Hay que fijar **C3** (AR(4) de panel + Δ4 ln hipotecas_importe + Δ4 ln ocupados + coste_uso_aprox + cu×expo: el AR(4) anidado más las variables de H2), sin selección por RMSE, y declararlo en decisiones.md. El resultado esperable es negativo (C3 es peor en entrenamiento), pero eso no es motivo para cambiar de modelo.

**(3) Provincias selladas (11, 16, 45): deben incluirse.** La regla común del pre-registro define la muestra sellada como la ventana 2024Q3-2026Q2 *y* las tres provincias. decisiones.md añade que las confirmatorias se evalúan «preferentemente en las provincias selladas», porque la ventana nacional ya se vio en v1. Dejarlas fuera haría inaccesible para siempre esa parte, ya que el acceso es único. Procedimiento recomendado, que hay que fijar en el código ANTES de la llamada:
  - Coeficientes de pendiente: los de entrenamiento (49 provincias, objetivos ≤ 2024Q2), idénticos a los de la parte (a).
  - Efecto fijo de cada provincia sellada: media del residuo (y − x'β sin FE) en su propia historia con objetivos ≤ 2024Q2, aplicado por igual al modelo y al AR(4). Es preferible al «FE medio» que menciona el docstring, porque trata a 11, 16 y 45 como a las provincias de entrenamiento y no penaliza a ningún modelo por el nivel. Usar su historia anterior a 2024Q3 es legítimo: forma parte de la misma y única llamada a `evaluate`, y no se usa ningún objetivo de la ventana.
  - Exposición de 11, 16 y 45: su media 2005-07 estandarizada con la **media y DE de las 49 de entrenamiento** (hay que corregir `preparar_panel`, que hoy re-estandariza con todas las provincias que recibe y cambiaría también la exposición de las de entrenamiento).
  - Contraste **principal** (único, fijado ahora): 52 provincias (49 + 3) y objetivos 2024Q3-2026Q2, con DM-HLN sobre la diferencia de pérdidas cuadráticas promediada por periodo (`vc.evaluar`, h=4), bilateral y t(n−1). Regla: H2-fuera de muestra se cumple si RMSE_C3 < RMSE_AR4(panel) y p < 0,05; después entra en el Holm de las 7 confirmatorias.
  - **Secundarios**, informados en la misma llamada y sin poder decidir: (a) solo las 49 provincias de entrenamiento; (b) solo 11, 16 y 45 en la ventana; (b') 11, 16 y 45 en toda su historia (orígenes 2012Q1-2023Q2, coeficientes de cada split de la validación en bloques, con el FE estimado igual pero solo con objetivos ≤ L del split), que es el único tramo «virgen» con potencia razonable. Además, el ECM v1 de panel como referencia.
  - Devolver n, n_periodos, RMSE, DM, p y el booleano de la regla, para que el log de accesos registre la decisión.

**(4) Fragilidad.** El parcheo de `vc.Q_TRAIN_FIN` y de `vc._prep.__defaults__` funciona (lo he comprobado en el ensayo en seco) y se restaura en `finally`, pero hay que añadir un test con datos de entrenamiento (pseudo-sellado 2022Q3-2024Q2, 49+3 «provincias pseudo-selladas» tomadas del train) que ejecute `evaluar_H2` de principio a fin. No toca data/sealed y demuestra que la llamada real no fallará, ya que un fallo después de abrir data/sealed no registra el acceso pero sí expone los datos.

## Cambios requeridos (prioridad)

1. **C1 [bloqueante]** `evaluar_H2`: orígenes 2023Q3-2025Q2 (objetivos 2024Q3-2026Q2, 8 periodos) y comprobación n_periodos ≥ 8 antes de devolver el resultado.
2. **C2 [bloqueante]** Fijar el modelo sellado de H2 en **C3** (no C1) y declararlo en decisiones.md. `config_h2_sellado.json` no debe depender del ranking de RMSE. Recalcular `oos_ok` sobre C3 (el nivel sigue siendo EXPLORATORIO).
3. **C3 [bloqueante]** Implementar la parte de las provincias selladas tal como se describe en §7(3), con el contraste principal (52 provincias, ventana) y los secundarios (a), (b) y (b') fijados en el código y en el docstring antes de la llamada.
4. **C4 [bloqueante]** `preparar_panel`: estandarizar la exposición con la media y DE de las 49 provincias de entrenamiento (parámetros fijos), y calcular el per cápita con la población **observada** (T1 de 2005, 2006 y 2007) en lugar de la interpolada.
5. **C5 [alta]** Test de ensayo en seco de `evaluar_H2` solo con entrenamiento (pseudo-sellado), versionado en tests/ o src/v2/bv_test_*.py, fuera de `make models` si es lento.
6. **C6 [media]** Declarar en decisiones.md: dependiente real frente a nominal (equivalentes por el FE de trimestre: quitar «H2_nominal» como robustez o explicarlo), operacionalización de la exposición, Holm intra-H2 m=2 frente a la familia de 7 (pendiente del orquestador), criterio `oos_ok` como añadido propio (no «fijado de antemano») y presupuesto nacional separado (4).
7. **C7 [media]** `bv_h2_sellado.py`: guarda explícita (`if __name__ == "__main__": raise SystemExit("solo vía holdout.evaluate")`) y que no se ejecute nada en la importación (`make models` lo ejecuta).
8. **C8 [baja]** p WCB = 0 → «≤ 1/(B+1)». Lenguaje: «resta» → «se asocia con»; «explica» en las contribuciones → «contabiliza». Arbitraje: usar la media expansiva como versión de referencia del Holm.
9. **C9 [para el orquestador, fuera de BV]** Fuga en el train común: `pob_*` 2024Q2 está interpolada con el dato del 1-1-2025 (sellado). Hay que corregirlo en holdout/build (NaN o arrastre del último observado) antes de la puerta de BA (H1 usa Δ4 ln pob 20-34).

Tras C1-C5 basta una re-revisión breve de bv_h2_sellado.py, bv_lib.preparar_panel y del test. No hace falta repetir el análisis de entrenamiento salvo `oos_ok` y el texto.

---

# Re-revisión (iteración 2 de 2) — commit `e05f42c` (r2/BV, con r2/main fusionado)

## Veredicto final: **APROBAR**

Con este veredicto el orquestador puede llamar UNA vez a `holdout.evaluate("H2", bv_h2_sellado.evaluar_H2, "BV", ["panel_prov_q", "nacional_q_v2"])`.

## Comprobaciones

- **Reproducción.** Clon aislado nuevo (clon local de r2/main + fetch de r2/BV en `e05f42c`), sin red (`HTTPS_PROXY=http://127.0.0.1:9`). Se ejecutaron dos veces `bv_main.py`, `bv_main.py --smoke` y `tests/test_bv_h2_sellado.py`: exit 0 en las seis ejecuciones. Los md5 de los 28 ficheros de output/v2/BV son idénticos entre ejecuciones, y `git status` queda limpio (las salidas coinciden con las versionadas).
- **H2 no evaluada.** docs/v2/holdout_accesos.md (r2/main `58e460b`) solo contiene dos filas de H1 (APERTURA + resultado) y ninguna de H2. El código de la rama no llama a `evaluate`, y `bv_h2_sellado.py` aborta si se ejecuta como script.
- **C1 (orígenes).** Los orígenes son 2023Q3-2025Q2 (objetivos 2024Q3-2026Q2, 8 periodos). La función aborta con RuntimeError si n_periodos < 8 (lo comprueba `test_aborta_con_pocos_periodos`). El ensayo en seco da contrastes finitos y no degenerados (principal: n=392, 8 periodos, DM −2,71).
- **C2 (modelo).** `CFG="C3"` está fijo en el código y `config_h2_sellado.json` no depende del ranking. C3 = AR(4) de panel + Δ4 crédito + Δ4 ocupados + coste de uso + coste de uso × exposición. Es fiel a «el modelo con estas variables… frente al AR(4) de panel». La regla de decisión (RMSE_C3 < RMSE_AR4 y p_DM-HLN bilateral < 0,05, con el Holm de las 7 en BS) queda escrita antes de la llamada.
- **C3 (provincias selladas).** Las pendientes se estiman solo con las 49 de entrenamiento y objetivos ≤ 2024Q2. El efecto fijo propio de 11, 16 y 45 es la media del residuo en su historia con objetivos ≤ 2024Q2, aplicada por igual al modelo y al AR(4). El principal usa 52 provincias; los secundarios son (a), (b), (b′) y el ECM v1. He comprobado que la maquinaria propia `_predecir` reproduce exactamente `vc.panel_ar4` y `run_panel_model` en el mismo split (diferencia máxima de predicción ≈ 5e-10).
- **C4 (exposición).** Usa la población observada del 1 de enero (sin interpolar) y se estandariza con la media y la DE de las 49 de entrenamiento (`exposicion_ref(pt)`), también para las selladas. Los coeficientes de H2 apenas cambian (crédito +0,00873, interacción −0,00441) y el resumen es coherente.
- **C5-C8.** Hay ensayo en seco versionado. Las desviaciones están declaradas en output/v2/BV/desviaciones.md (pendiente de trasladar a decisiones.md). EXPLORATORIO aplica el criterio uniforme; se han hecho los cambios de redacción y la cota de p del WCB; el arbitraje se refiere a la media expansiva.
- **C9 (holdout).** `_sin_interpolacion_hacia_sellado` pone a NaN los valores interpolados posteriores a la última observación de entrenamiento. `evaluate` registra la apertura antes de leer y bloquea un segundo intento.

## Observaciones no bloqueantes → docs/v2/limitaciones.md

1. **(b′) desborda la ventana.** El docstring dice «orígenes 2012Q1-2023Q2», pero `block_splits` sobre ≤ 2024Q2 llega a orígenes 2023Q4, con objetivos hasta 2024Q4 que se solapan dos trimestres con la ventana. Es solo secundario e informativo: al informar del resultado hay que leerlo así.
2. **Riesgo de pérdida del único acceso.** Si el valor tasado de 2026Q2 no figura en la muestra sellada, la función aborta con n_periodos < 8 y la apertura ya queda registrada: H2 no podría evaluarse nunca. En ese caso se documenta como «no evaluable», sin reintento.
3. **Potencia baja.** Son 8 periodos con h=4 (DM-HLN con t(7)). Además, C3 es claramente peor que el AR(4) en la validación de entrenamiento (RMSE 0,0605 frente a 0,0418) y en el ensayo en seco. Lo esperable es un resultado negativo para la parte predictiva de H2.
4. **Inferencia.** Crédito: simultaneidad (sin poder predictivo a t−4). Coste de uso: aproximación nacional sin impuestos ni prima de riesgo, identificada solo por la interacción con una exposición no aleatoria. Datos de añada actual (deflactor SA), no en tiempo real.
5. **Presupuestos y Holm.** Presupuesto OOS nacional separado (4) del de panel (6). Holm intra-H2 m=2; el Holm de las 7 queda pendiente en BS.
