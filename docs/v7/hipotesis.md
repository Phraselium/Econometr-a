# Pre-registro V7: modelos regionales (CCAA trimestral; provincia como complemento)

Fecha de redacción: 2026-10-12. Se escribe ANTES de cualquier estimación con datos reales de V7.
- La versión que vale es la del commit que lleva la etiqueta local `prereg-v7`.
- Su fecha **verificable** será la de la release o el DOI que cree el autor (docs/v7/notas_release.md).
- Cualquier desviación de este documento se anota en docs/v7/desviaciones.md, con su motivo.

## 1. Datos y muestra

- **Panel principal.** data/processed/v7/panel_ccaa_q_v7.csv: 17 CCAA, Ceuta y Melilla fuera; 2007T1-2026T2, con N = 17 y T de unas 78.
- **Contaminación.** El panel ya lo usó v1 entero. Toda estimación y todo backtest con 2007T1-2026T2 se rotula **«informativo, muestra ya vista en v1»**.
- **Validación limpia.** Solo la diferida de la sección 6.

## 2. Variables y especificaciones principales

Todas las variables van en logaritmos salvo las tasas. La dependencia transversal y el nivel general de precios nacional los absorben las medias transversales (CS-ARDL) o el demeaning transversal (PMG/MG/DFE). No se incluye un deflactor regional porque no existe.

| Mercado | Dependiente (y) | Largo plazo (x), especificación A | Especificación B (sin colinealidad) | Corto plazo y controles |
|---|---|---|---|---|
| Alquiler | ln IPC alquiler (CCAA) | ln ocupados, ln población total | tasa de paro (sustituye a ocupados), sin población | Δ ln hipotecas (importe); dummies de quiebre; zt_declarada, tope_rentas_ccaa (solo corto plazo, exploratorio) |
| Compra | ln IPV (CCAA) | ln ocupados, ln hipotecas (importe), ln población total | tasa de paro, ln hipotecas (importe) | Δ ln compraventas; dummies de quiebre |

- **Robustez** (no confirmatoria):
  - SERPAVI anual en alquiler y valor tasado en compra;
  - población extranjera en lugar de población total; nunca las dos a la vez, ni con ocupados en una misma especificación;
  - PIB regional interpolado, solo como control.
- **Dummies de quiebre, fijas:**
  - EPA 2021T1 (escalón en las variables EPA);
  - COVID 2020T2-2020T4;
  - cambio de base del IPV 2015/2007, si el enlace lo exige.
- **Ruptura.** Bai-Perron como diagnóstico de la relación agregada.
- **Retardos.** ARDL(p, q) con p, q ≤ 4, elegidos por SBC en la media de las CCAA y comunes a todas en PMG/MG/DFE. Se reporta también el ARDL(1,1).

## 3. Hipótesis confirmatorias (signo de largo plazo común)

| id | Mercado | Hipótesis (H1 unilateral) | Estimador principal | Familia |
|---|---|---|---|---|
| H7-A1 | Alquiler | θ(ln ocupados) > 0 | MG con demeaning transversal; PMG con IC bootstrap como contraste | F-A |
| H7-A2 | Alquiler | θ(ln población) > 0 | MG con demeaning transversal (spec. A); PMG como contraste | F-A |
| H7-A3 | Alquiler | θ(tasa de paro) < 0 | MG con demeaning transversal (spec. B); PMG como contraste | F-A |
| H7-C1 | Compra | θ(ln ocupados) > 0 | MG con demeaning transversal (spec. A); PMG como contraste | F-C |
| H7-C2 | Compra | θ(ln hipotecas) > 0 | MG con demeaning transversal (spec. A); PMG como contraste | F-C |
| H7-C3 | Compra | θ(ln población) > 0 | MG con demeaning transversal (spec. A); PMG como contraste | F-C |
| H7-C4 | Compra | θ(tasa de paro) < 0 | MG con demeaning transversal (spec. B); PMG como contraste | F-C |
| H7-E1 | Ambos | Existe cointegración de panel | «Tipo Westerlund» Gt/Pt con bootstrap, más Pedroni panel/group-ADF (contraste principal de cointegración) | F-E |
| H7-E2 | Ambos | Velocidad de ajuste media φ̄ < 0 | t de MG frente al valor crítico **simulado bajo no cointegración** (R2); si no está disponible, EXPLORATORIO. El sesgo de φ en muestra finita va a favor de H1 y se declara | F-E |

Cómo se juzga cada hipótesis:
- **Ajuste.** Holm dentro de cada familia F-A, F-C y F-E.
- **Para decir «se confirma»:** p de Holm < 0,05 con el MG con demeaning transversal y el mismo signo con PMG (IC bootstrap aproximado) y DFE. CS-ARDL no se usa: la validación de R2 lo declaró no apto.
- **Hausman** (varianza no paramétrica del MG; variante elegida a posteriori en R2, con potencia de unos 0,61).
  - Si rechaza, se declara la heterogeneidad del largo plazo.
  - Si no rechaza, se reportan MG y PMG **sin** afirmar homogeneidad.
- **Capa máxima: C4.** Son asociaciones de largo plazo, no efectos causales: no hay variación exógena.

## 4. Familias exploratorias (BH, q = 0,10)

- **F-H · Heterogeneidad regional.** Velocidades de ajuste φ_i y coeficientes de corto plazo por CCAA, en los dos mercados. Comparación con el encogimiento del modelo jerárquico (pymc; MixedLM como contraste).
- **F-L · Proyecciones locales de panel.** Respuesta de y a un shock del tipo hipotecario nacional (y del crédito nuevo), interactuado con la exposición regional (peso hipotecario de 2015-2019, predeterminado), en los horizontes 0 a 8. Una familia por mercado.
- **F-R · Regulación.**
  - Asociación de zt_declarada y tope_rentas_ccaa con Δ ln IPC alquiler a corto plazo.
  - Solo exploratorio. No hay un diseño causal nuevo; v3 ya halló pretendencias fallidas.
- **F-P · Provincia anual.** FE y CCE con flujos de padrón, EPA, ETDP, hipotecas e iniciadas, solo como complemento.

## 5. Potencia (Monte Carlo de R2, docs/v7/validacion_herramientas.md)

Escenario N = 17, T = 78:
- MG_dm: sesgo de θ pequeño, cobertura 0,87-0,94.
- PMG: cobertura de 0,86 a 0,92, según el EE.
- Westerlund: potencia de 0,99-1 con cointegración y tamaño conservador.
- Hausman: potencia de 0,61 frente a θ_i heterogéneo.

Si la potencia para el θ del ejercicio es menor de 0,8, un resultado nulo no es evidencia de ausencia. Los IC de PMG se rotulan «aproximados».

## 6. Validación limpia diferida

- **Muestra.** Datos publicados después de la fecha verificable del pre-registro:
  - trimestrales de 2026T3 a 2027T2 (IPV, IPC alquiler, EPA, hipotecas y compraventas por CCAA);
  - anuales de 2026, cuando se publiquen.
- **Procedimiento.** `make evaluate_v7` descarga, congela los modelos de R5 (sus coeficientes y especificaciones quedan versionados antes) y evalúa una sola vez. La apertura queda registrada en docs/v7/evaluate_v7_accesos.md.
- **Métrica.** RMSE de predicción a 1-4 trimestres frente a la base fuerte de K1 (AR con factor común) y frente al AR(4), con DM-HLN y permutación por CCAA.
- **Hipótesis de predicción H7-P1.** El mejor modelo regional de R5 bate a la base fuerte en el agregado de las 17 CCAA.

## 7. Qué NO se afirmará en ningún caso

- Efectos causales de la inmigración, de los topes, de las zonas tensionadas o de los turísticos.
- Recomendaciones de política más allá de la regla de R6: un instrumento solo es «robusto» si mantiene el signo en todo el rango, en PMG y en el modelo jerárquico.
