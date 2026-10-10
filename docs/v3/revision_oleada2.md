# Revisión independiente · v3 oleada 2 (H3-1, H3-2, H3-3a, H3-3b, P-D, verificador)

Revisor independiente. HEAD 40e7ea3 (r3/main). Alcance acordado: identificación, capas, neutralidad, conclusiones y cumplimiento del pre-registro. No se ha reproducido el pipeline. Sí se ha ejecutado `src/v3/check_texto.py` sin red, con resultado de 0 errores; los problemas de abajo son semánticos y ese chequeo no los detecta. No se ha leído `data/sealed`.

## Veredicto: **REHACER** (alcance limitado)

La parte econométrica confirmatoria es correcta:
- se respetan el orden y la apertura única;
- las cuatro hipótesis están bien asignadas a C4;
- Holm está bien aplicado.

No hace falta reestimar ni volver a abrir ningún sellado. Se rehace la capa de comunicación (verificador, P-D, `lo_que_sabemos.md`, `informe_politica.md`) y la documentación de desviaciones. Hay asimetrías de estándar entre afirmaciones de distinto signo, un error de cálculo en V11 y una P-D desactualizada respecto a C1.

---

## 1. Pre-registro

| Comprobación | Resultado |
|---|---|
| Integridad de `hipotesis.md` | `git diff 204c073 -- docs/v3/hipotesis.md` sale vacío: sin cambios desde el ancla. |
| Orden P2 → adelanto → estimación → sellado | **Se cumple.** En `c1_run.main` los pasos van [2] P2, [3] adelanto, [4]-[5] estimación y [6] sellado. En `c3_run.main` van potencia (§3), estimación (§5) y sellado (§6). P2 decide `estimable` antes de estimar. |
| fn sellada de H3-1 = especificación registrada | **Sí.** `fn_h31` llama a `ce.fit(..., fe="ym")` por defecto, es decir, efectos fijos de sección + año×municipio, con cluster por distrito. Usa VUT de agosto (`c1_data` l. 44), excluye 2026M05 y aplica a entrenamiento y sellado la misma `prep`. |
| fn sellada de H3-2 | 2SLS con z = cuota de 2021M08 × crecimiento LOO; 6 ciudades como principal; 5 ciudades y Palma aparte (P5). Correcta. Los efectos fijos de H3-2 no estaban fijados en el pre-registro; la desviación C1-5 está declarada. |
| Una apertura por hipótesis | **Sí.** En `docs/v2/holdout_accesos.md` hay una APERTURA y una evaluación para cada una: H3-3a y H3-3b a las 13:42:50Z, H3-1 a las 13:47:05Z y H3-2 a las 13:47:09Z. No hay filas DRY en el registro real. `evaluate_v3` rechaza una segunda apertura. |
| Parche en memoria (`shim_pandas3`) de C3 | **Sin efecto en los resultados.** Solo sustituye `DataFrame.apply(pd.to_numeric, errors="ignore")`. Además, `make_fn` convierte por su cuenta `cod_ine`, `anio` y la columna de resultado. La versión actual de `holdout.py` (c5e8aae) ya no contiene esa llamada, así que el shim es código muerto. Hay dos problemas documentales: (i) C3/desviaciones §11 afirma que «src/holdout.py no se modifica», pero c5e8aae lo modificó; (ii) el cambio de la infraestructura de sellado posterior al ancla no figura en `decisiones.md`. Además, `dry_run` de C3 redirige `holdout.LOG`/`LOG_MD` a un directorio temporal. Aquí fue inocuo porque usó datos sintéticos, pero es un patrón que permite eludir el registro (ver W9). |
| Desviaciones no declaradas | (a) **Validación por fuente de H3-3.** Es un DiD 2×2 con pre = 2018-2019 y post = 2021-2022; descarta 2020 y **2023**. El pre-registro dice «SERPAVI 2018-2023 con el mismo diseño (anual)». La elección es razonable, pero no figura en C3/desviaciones. (b) **H3-1.** El pre-registro pide «muestra nacional y 6 ciudades conjuntas»; el principal confirmatorio pasa a ser solo el nacional (C1/desviaciones §2). Ninguna conclusión cambia, porque el sellado de 6 ciudades da p = 0,20 con **signo opuesto**, −0,0013. Pero es una elección de familia: si ambas fueran confirmatorias, m sería 5. (c) **Criterios fijados después del pre-registro.** El umbral de placebo de tratamiento (≤10 % de permutaciones con \|t\|>1,96) y la regla «ADRH significativo cuenta como fallo de b» se fijaron después. Este segundo punto contradice P3, que dice que se informa sin invalidar automáticamente. (d) **Registro.** Ninguna de las 27 desviaciones de C1 y C3 está transcrita en `docs/v3/decisiones.md`, como exige el propio pre-registro. |

## 2. Capas (criterios a-e)

| Hip. | a | b | c | d | e (Holm) | Capa | Juicio |
|---|---|---|---|---|---|---|---|
| H3-1 | falla: adelanto p ≈ 1e-4, \|b_adelanto\| = 0,0017 frente a b = 0,00026 | falla: ADRH p = 0,0003 (ver nota) | falla: RV 0,0016 < 0,0034 | falla: IC sellado [−0,0007; 0,0028] | p_Holm 0,47 | **C4** | Correcta. La falla en a basta. |
| H3-2 | falla: adelanto | falla: ADRH p = 0,003 | falla: δ = −3,7 con regla de signo | falla | 0,50 | **C4** | Correcta. F de primera etapa 21,9 en entrenamiento y 60,5 en sellado (>10). |
| H3-3a | falla: Wald p = 0,40 pasa; RR con M̄=1, IC [−0,23; 0,12] | pasa\* | falla: RV 0,206 < 0,279 (pendiente previa) | pasa: −0,77 % [−1,39; −0,14] | p_Holm 0,048, pasa | **C4** | Correcta. Ningún criterio está mal evaluado en un sentido que la promueva o la hunda. Comprobación propia: el máximo salto previo es ≈0,020, la cota RM media para j = 1..6 es 3,5×0,020 = 0,070 > \|θ\| = 0,056, y el conjunto identificado puntual [−0,126; +0,014] ya incluye 0. Falla con cualquier implementación de RR con promedio post. |
| H3-3b | falla: Wald p = 0,013 | falla: fecha falsa 2019Q4 p = 0,011 | falla | pasa: −4,4 % | p_Holm 0,0002 | **C4** | Correcta. El principal de fianzas es −4,9 % [−9,9; 0,5]; 0/36 especificaciones del multiverso son significativas. |

Holm (m = 4) usa los p de las evaluaciones confirmatorias, como fija P4: sellados H3-1 nacional y H3-2 6 ciudades, y validación por fuente H3-3a/b. La aritmética es correcta: 0,000055×4, 0,0162×3, 0,233×2 y 0,501×1. `p_ajustado` sigue en `null` en C1 y C3 `resultado.json` (W10).

Notas de criterio, sin efecto sobre la capa, que conviene homogeneizar:
- **Criterio b asimétrico.** En H3-1/H3-2 un placebo de resultado significativo cuenta como fallo, aunque P3 dice que no invalida automáticamente. En H3-3a se marca `b = true` aunque **no existe** placebo de resultado (P3 lo declara). Lo coherente es: H3-1, b «pasa tratamiento; resultado significativo informado»; H3-3, b «parcial: sin placebo de resultado».
- **Criterio c implementado distinto en cada rama.** C1 compara RV con max(R²_y, R²_d) y exige δ > 1 con signo. C3 compara solo con R²_y y usa \|δ\|. Además, en H3-3a el criterio c depende por completo de tomar la pendiente previa del resultado como «covariable observada». Sin ella, el máximo es 0,0076 y c pasa. Hay que declararlo. En H3-3a la capa no cambia, porque a falla.
- Conviene informar el **M̄ de ruptura** de H3-3a (≈0,79), sin promoción.
- El sellado de H3-3a es 7 veces menor que el principal (−0,77 % frente a −5,4 %). «Mismo signo» se cumple, pero la discrepancia de magnitud debe figurar en la misma frase.

## 3. P-D

1. **Desactualizada respecto a C1.** `PD/resultado.json` marca `"C1_resultado_json": "ausente"`, y las filas 8, 11 y 14 dicen «H3-1 ausente, solo literatura». Por eso el rango del efecto local de retirar VUT se apoya solo en GL (cuya réplica propia es NO REPLICADO) y en Barron. No incluye la estimación propia sellada: β ∈ [−0,0007; 0,0028] por pp, cuyo IC incluye 0 y que haría que `rango_max` alcance ≥ 0. Para los topes, en cambio, P-D calibra con JMS, que es VERIFICADA **y replicada**. Es un estándar distinto para dos políticas.
2. **Valores fuera de validez.** −84 % (fila 14) y −110,7 % (fila 15) están fuera del rango log-lineal. Solo la fila 9 lo advierte. Hay que truncar o marcar todas.
3. **«Robusto».** `robusta_en_todo_el_rango = sí` y la sección «Problema y soluciones robustas» usan «robusto» para referirse a un signo estable en la rejilla de un único modelo. El pre-registro reserva «robusto» para la triangulación con ≥2 diseños de supuestos distintos. Ninguna fila de P-D lo cumple.
4. **C2 con robustez «no».** Las filas 16 (retirar VUT, esfuerzo nacional), 28 y 29 (vivienda pública) tienen `robusta = no` y `capa = C2`. C2 solo es defendible para el enunciado débil «≤ 0, posiblemente nulo». Debe constar así en `metrica`.
5. **Canales adversos y costes asimétricos.** Los topes son la única opción con un canal adverso explícito: L de +3,8 % a −15 % (Diamond, San Francisco) y pérdida ℓ. Además, se resumen en un «saldo neto por inquilino» de −4.600 a +1.600 €/año. Construcción, movilización y retirada de VUT no tienen coste ni canal adverso modelado: s ≥ 0, ρ solo en la vivienda pública. El criterio de dominancia y el de mínimo arrepentimiento favorecen mecánicamente a las opciones sin coste modelado y a la dosis mayor (gana «construcción 100k/año»). No hay lenguaje de recomendación explícito (no aparecen «recomend», «debería», «conviene», «mejor opción»). Aun así, presentar un ranking de arrepentimiento sin costes, junto a un saldo neto solo para los topes, es una asimetría.

## 4. Verificador (14 fichas)

| Id | Veredicto / capa | ¿Sigue de la evidencia y de la regla? |
|---|---|---|
| V01 VUT | SIN EVID. / C2 | Coherente con su regla, pero ver la asimetría con V03. La regla general dice «SIN EVIDENCIA: solo C4 o sin datos», y aquí hay C2: hay que aclarar que la C2 es de cantidad y no decide sobre una afirmación de precio. |
| V02 tenedores | SIN EVID. / C4 | Sí. Simétrica con V09. |
| V03 inmigración | **PARCIALMENTE** / C2 | **No con el mismo estándar que V01.** Se apoya en (i) una **cota superior** de cantidad (≤45 % de la creación de hogares en 2014-2019, no informativa en 2020-2025) y (ii) «v2 (BI) la asocia… EXPLORATORIA», que es evidencia C4 dentro de la regla. V01 dice explícitamente que «las estimaciones C4 no deciden» y que una cota de cantidad «no basta». Una cota superior no nula no es respaldo parcial ni en V01 ni en V03. Además, V01 incluye un dato en contra (25 % de la subida donde las VUT no crecieron) y V03 no tiene análogo. |
| V04 oferta | PARCIALMENTE / C1 | Sí. |
| V05 déficit | RESPALDADA / C1 | Sí, con la salvedad de que es un balance contable. |
| V06 topes → alquiler | SIN EVID. / C4 | La regla es la misma que en V07 (correcto), pero la redacción es asimétrica. V06 subraya «todas signo negativo» y omite que el sellado es 7 veces menor. V07 subraya «no significativo (p≈0,07)» y omite que su validación por fuente sí excluye 0 (−4,4 %, p_Holm 0,0002) y que TWFE (−0,2 %) y dos réplicas JMS (+3,0 %, +2,2 %) tienen otro signo. Hace falta la misma plantilla en ambas: principal, sellado, estimadores alternativos y multiverso (% del mismo signo, % significativo: alquiler 100 % / 89 %; contratos 81 % / 0 %). |
| V07 topes → oferta | SIN EVID. / C4 | Ídem. |
| V08 vacías | PARCIALMENTE / C1 | Sí. |
| V09 seguridad jurídica | SIN EVID. / C4 | Sí. |
| V10 fiscalidad | SIN EVID. / C4 | La regla introduce una afirmación direccional sin evidencia («parte de la rebaja se traslada al precio»). Debe quedar en forma condicional y simétrica: la incidencia depende de la elasticidad de oferta, no estimada. |
| V11 vivienda pública | PARCIALMENTE / C2 | **Error.** El filtro de `verificador.py` (l. 284) incluye «vacías», y `pub[:3]` muestra tres filas de **movilización de vacías**, no de vivienda pública. La capa C2 sale de ellas. En P-D la vivienda pública da [−5,4; 0] % y [−13,1; 0] % con robustez «no» (nula si ρ = 1). La regla «reduce la brecha en todo el rango simulado» es falsa para esta política. |
| V12 tipos | PARCIALMENTE / C2 | Hay una incoherencia interna: «podría cubrir toda la subida (cota 78,0 %)» con un rango de [23,5; 109,6]. Solo el extremo cubre el 100 %. Además, la traducción a precio de V12 (coste de uso en estado estacionario) es C2, mientras que la de V01 (vía ε) es C4. Hay que justificar por qué un supuesto estructural es «débil» y el otro no, o tratar ambos igual. |
| V13 burbuja | SIN EVID. / C4 | Sí. |
| V14 compradores extranjeros | SIN EVID. / C1 | Sí. |

No hay veredicto RESPALDADA ni NO RESPALDADA apoyado en C4. Sí hay un veredicto PARCIALMENTE (V03) cuya regla cita evidencia EXPLORATORIA. Las fichas no llevan la etiqueta VERIFICADA/NO VERIFICADA con cuartil, aunque `literatura_v3.md` la tiene (JMS, GL, Diamond y Saiz 2007 son VERIFICADA Q1).

## 5. Neutralidad global

- **`lo_que_sabemos.md`.**
  - La sección «Probable pero no demostrado» contiene ítems C4, y «probable» no existe en la escala.
  - Hay una asimetría de ubicación. «Los topes bajan la renta» (V06, SIN EVID.) aparece como «probable». «Los topes reducen la oferta» (V07, SIN EVID.) y «las VUT son la causa principal» (V01, SIN EVID.) aparecen en «No se puede afirmar». Las tres fichas tienen el mismo veredicto.
  - Hay lenguaje causal en C4: «el alquiler sube menos de un 0,5 %» (VUT) y «la renta … fue un 5,4 % menor en los municipios sujetos».
- **`informe_politica.md`, «Lectura», y `lo_que_sabemos.md`, «Problema y soluciones robustas».** Afirman que añadir oferta es «la única familia de medidas cuyo signo no depende de supuestos» y que «las demás pueden mejorar o empeorar el acceso». Esto contradice P-D: la retirada de VUT (25/50/100 %) también domina débilmente (≤ 0 en toda la rejilla). Además, «vivienda pública sin desplazamiento» no es incondicional. La fila de construcción no lleva la advertencia «coste sin cuantificar», que sí aparece en movilización.
- No se encontraron alusiones partidistas ni léxico valorativo explícito; `check_texto` da 0 errores.

---

## Cambios obligatorios (por prioridad)

- **W1 (neutralidad, V01/V03).** Aplicar a V01, V03 y V12 una regla común:
  - (i) fijar en el enunciado de cada una la fracción que la afirmación necesita («explica» o «causa principal»);
  - (ii) una cota superior no nula de cantidad no es respaldo parcial;
  - (iii) la evidencia C4 no entra en la regla.

  Con la evidencia actual, V03 debe quedar como SIN EVIDENCIA SUFICIENTE, salvo que esa regla común justifique otra cosa también para V01. Hay que añadir a V03 el análogo del dato en contra de V01, si existe, o declarar que falta.
- **W2 (error, V11).** Corregir el filtro de `verificador.py` (solo «públic»). Recalcular la capa y la magnitud con las filas 28-29 de P-D y reescribir la regla: el efecto es ≤ 0 y nulo si ρ = 1. El veredicto PARCIALMENTE es válido solo «según supuestos».
- **W3 (`lo_que_sabemos.md` / `informe_politica.md`).**
  - Suprimir «Probable pero no demostrado» y usar «Exploratorio (C4)».
  - Ubicar V06, V07 y V01 con el mismo criterio.
  - Cambiar los verbos causales de las frases C4 por lenguaje de asociación.
  - Corregir «la única familia de medidas…» para que refleje los conjuntos de dominancia estricta y débil de P-D. Incluir la retirada de VUT en la dominancia débil, indicando qué canales no se modelan.
- **W4 (P-D frente a C1).** Volver a ejecutar P-D con `C1/resultado.json` presente. Incluir H3-1 sellado (C4) como método en las filas del efecto local de la retirada de VUT; el rango debe alcanzar ≥ 0. Etiquetar GL como NO REPLICADO en la propia fila. Truncar o marcar los valores fuera de la validez log-lineal (filas 14 y 15).
- **W5 (P-D, simetría de costes).** Hacer una de dos cosas:
  - incluir un canal adverso o de coste parametrizado en todas las opciones (coste fiscal y de suelo de la construcción, coste de movilización, pérdida para propietarios y desplazamiento de la demanda turística en la retirada de VUT);
  - o retirar el «saldo neto» de los topes de los titulares y dejarlo en la tabla con la misma advertencia que las demás.

  Además, declarar en la fila de mínimo arrepentimiento que el resultado es mecánico en ausencia de costes.
- **W6 («robusto»).** Sustituir `robusta_en_todo_el_rango` y «soluciones robustas» por «signo estable en toda la rejilla», reservando «robusto» para la triangulación. Etiquetar las filas C2 con robustez «no» (16, 28 y 29) como «≤ 0 (posiblemente nulo)».
- **W7 (V06/V07, misma plantilla).** Ambas fichas deben incluir: principal, validación por fuente con p_Holm, estimadores alternativos, réplica JMS y multiverso (% del mismo signo y % significativo). Hay que mencionar en V06 la diferencia de magnitud entre el sellado y el principal, y en V07 que la validación por fuente excluye 0 y que hay estimadores de signo opuesto.
- **W8 (registro de desviaciones).**
  - Transcribir a `docs/v3/decisiones.md` las desviaciones de C1 (1-14) y C3 (1-13).
  - Añadir las no declaradas: ventana 2018-19/2021-22 de la validación por fuente de H3-3, sin 2023; elección del nacional como único confirmatorio de H3-1 e informe destacado del sellado de 6 ciudades con signo opuesto; umbrales de placebo fijados después.
  - Registrar el cambio de `holdout.py` en c5e8aae.
  - Corregir C3/desviaciones §11.
- **W9 (criterios homogéneos, sin cambiar capas).**
  - Unificar el criterio c entre ramas (R²_y y R²_d; \|δ\| o δ con signo, la misma regla en ambas) y declarar la dependencia de H3-3a respecto a la pendiente previa.
  - Criterio b de H3-3: «parcial (sin placebo de resultado)». Criterio b de H3-1: aplicar P3 tal como está escrito.
  - Informar el M̄ de ruptura de H3-3a.
  - Eliminar `shim_pandas3` (código muerto) y prohibir la redirección de `holdout.LOG` fuera de `holdout.py`.
- **W10 (menores).**
  - Rellenar `p_ajustado` en C1 y C3 `resultado.json` desde `holm_v3.csv`.
  - Añadir la etiqueta VERIFICADA/NO VERIFICADA con cuartil a la literatura de las fichas.
  - V10: regla condicional sin afirmación direccional.
  - V12: corregir «podría cubrir toda la subida» frente al 78 %.
