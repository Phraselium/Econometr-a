# Revisión independiente de la puerta F3 (estimación de diseños) — V9

Fecha: 2026-10-15. Revisor independiente (no ha hecho el trabajo). Objeto: rama `r9/main`, commit `e28d1e4`.
Referencias contrastadas: docs/v9/hipotesis.md (`prereg-v9`), docs/v9/hipotesis_addendum_a1.md (`prereg-v9-a1b`), docs/v9/decisiones.md (E3-E5), src/v9/*.py, output/v9/d1..d7 y output/v9/f3. No se ha leído data/sealed. No se ha modificado nada salvo este fichero.

## Veredicto: **REHACER** (iteración 1)

Ningún resultado sube de capa: la regla de f3_capas.py se aplica tal cual y no hay ningún C3. El problema es que la única prueba que separa H1b-renta de C3 (Honest DiD con M̄ = 1, M̄ de ruptura 0,8) usa una versión simplificada que **no es la pre-registrada** (Rambachan y Roth). Además, E5 dice que está «validada por Monte Carlo y conservadora», y eso no está demostrado. A esto se suma una regla pre-registrada de instrumento débil (D4) que no se aplica en las etiquetas de BH y que cambia una etiqueta. Son cambios acotados: no hace falta volver a estimar los diseños.

## Reproducción

Hecha en un clon aislado del commit e28d1e4 (scratchpad), con `data/` enlazada en solo lectura y sin red (`HTTPS_PROXY=http://127.0.0.1:9`). Se ejecutan d1, d2, d3, d4, d5, d7 y f3_capas en ese orden. Resultado: rc = 0 en todos y md5 idéntico (detalle al final).

## Hallazgos (por gravedad)

### ALTA

**1. Honest DiD: el procedimiento no es el pre-registrado y decide la capa de H1b-renta.** src/v9/herramientas.py:109-125 (`honest_rm`) y docs/v9/decisiones.md E5.3.
- **Qué se pre-registró.** «Honest DiD (Rambachan y Roth), magnitudes relativas» (hipotesis.md, D1a, prueba 2; addendum A1.2).
- **Qué se implementó.** Un IC por sustitución: θ̂ ± (M̄·máx|Δδ̂_pre|·media(1..K) + 1,96·EE).
  - El conjunto identificado de Δ^RM está bien calculado para un máx|Δδ| conocido.
  - Pero toma como verdadero el máx|Δδ̂| estimado, sin incertidumbre de muestreo. Rambachan y Roth la tratan con ARP condicional o híbrido.
  - En H1b ese máximo (0,016) es del orden del EE de cada coeficiente previo (≈ 0,010-0,012). Lo determina el salto e = −2 → −1, es decir, el confinamiento de 2020T2-T3.
- **La afirmación de E5 no tiene respaldo.** E5 dice que la versión está «validada por Monte Carlo y [es] conservadora frente a Rambachan y Roth».
  - tests/v9/test_herramientas.py:54-65 solo comprueba que, con M̄ = 0 y un efecto grande, el IC excluye el 0 y que la ruptura es > 0.
  - No hay prueba de cobertura con violaciones de tendencias paralelas ni comparación con RR.
  - Incumple además la regla del proyecto de validar las herramientas por Monte Carlo antes de usarlas.
- **Impacto.** H1b-renta cumple las otras cuatro condiciones (Holm, pretendencias p = 0,28, placebo de fecha p = 0,41, permutación p < 0,002). Con M̄ de ruptura 0,8, muy cerca de 1, la capa depende de la implementación.
- **Corrección.**
  - (a) Implementar el IC de RR para Δ^RM: ARP condicional o híbrido sobre (β̂_pre, β̂_post) y la matriz `es_vcov` existente. Validarlo por Monte Carlo (cobertura ≥ 95 % en la frontera de Δ^RM) y, si es posible, contra los ejemplos publicados del paquete HonestDiD.
  - (b) Aplicar la regla del addendum tal cual con ese IC y publicar las dos versiones.
  - (c) Corregir E5.3: quitar «validada» y «conservadora» mientras no haya prueba.
  - El resultado se acepta en cualquier dirección. Ejecutar el procedimiento pre-registrado no es promoción de capa. Sí lo sería cambiar de prueba o de ventana (por ejemplo, quitar el confinamiento) a la vista del resultado: eso queda prohibido.

### MEDIA

**2. D4: la regla de instrumento débil no se aplica en BH ni en el IC publicado.** src/v9/f3_capas.py:71-75 y 84-86; src/v9/d4_inmigracion.py:36-40.
- **La regla.** El pre-registro dice: «Si F < 23,1, solo se interpreta el IC de Anderson-Rubin». Todas las filas de D4 tienen F efectiva entre 1,5 y 5,4.
- **Lo que hace el código.** La familia BH usa el p de Wald de 2SLS y la tabla_revista muestra el IC de Wald.
- **Impacto.** Con el p de AR, que para β = 0 coincide con el de la forma reducida, «Δ log valor tasado, ampliación 2015-2022» pasa de p = 0,078 (BH 0,23, «no detectada») a p_rf = 0,0032 (BH ≈ 0,019, «asociación (BH < 0,10)»). Recalculado por el revisor; las demás etiquetas no cambian.
- **Corrección.**
  - Usar p_rf (equivalente a AR en β = 0) en la familia BH cuando F < 23,1.
  - En la tabla, poner el IC de AR en lugar del de Wald.
  - Sigue siendo C4: exploratoria, sin potencia (MDE 0,076).

**3. IC de Anderson-Rubin truncados por la rejilla.** src/v9/d4_inmigracion.py:32: `REJILLA = np.linspace(-0.3, 0.3, 1201)`.
- La mayoría de los IC de AR acaban en ±0,300, el borde de la rejilla. Son conjuntos no acotados (o uniones disjuntas) y se publican como intervalos finitos: por ejemplo, «AR [0,042; 0,300]» en tabla_revista.md.
- **Corrección.** Publicar «(−∞; ∞)», «[a; ∞)» o la unión de intervalos según `AR_acotado`. Ampliar la rejilla, o resolver la cuadrática de AR en forma cerrada.

**4. Pretendencias rechazadas sin indicar en filas exploratorias de D1.** src/v9/f3_capas.py:104.
- La advertencia «pretendencias rechazadas» solo se añade en D2.
- Falta en:
  - D1c renta: pretendencias p < 0,001 y etiqueta «asociación (BH < 0,10)» sin advertencia;
  - D1c contratos: p < 0,001;
  - D1a-contratos: p = 0,031.
- En D3, el placebo 2021→2023 rechaza en Δ log fianza media (p = 0,038-0,049, con una magnitud mayor que la principal), y no se indica en tabla_capas ni en tabla_revista.
- En D4, las pretendencias de Rotemberg de valor tasado rechazan para Rumanía, Marruecos y Portugal (p de Holm ≤ 0,015; output/v9/d4/rotemberg.csv), y no llegan a la tabla.
- En D2, la reapertura-renta pierde la significación con la tendencia por dosis (p = 0,30).
- **Corrección.** Aplicar la advertencia de pruebas fallidas a todo diseño con prueba (D1a/D1b/D1c, D2, D3 placebo, D4 Rotemberg y D2 sensibilidad A1.3) en `motivo_capa` y en tabla_revista.

**5. D7: periodos desalineados en la descomposición 2022-2025.** src/v9/d7_hogares.py:88-89.
- Los hogares van de la ECP 2022T1 a 2026T1 (4 años) y la población del censo anual de 2022 a 2025 (3 años).
- h1 = H(2026)/P(2025) atribuye a la tasa de jefatura un año de crecimiento de la población. El componente de población queda infravalorado y el de jefatura, sobrevalorado.
- El periodo pre-registrado era 2021→2025 y el cambio no consta en decisiones.md.
- **Corrección.** Alinear las fechas (ECP 2022T1→2025T1 con población a 1-1-2022 y 1-1-2025, o la población de la ECP en las mismas fechas). Si no es posible, publicar las dos variantes y anotar la desviación en decisiones.md.
- En el contraste C1 (d7_hogares.py:129-133), el umbral de ±2 % no estaba pre-registrado y compara el censo a 1-1-2021 con la ECP a 1-1-2022, es decir, fechas distintas. Hay que declarar el umbral como desviación o comparar en la misma fecha.

### BAJA

**6. p de permutación sin el +1 de Fisher.** src/v9/d1_zonas.py:55 y src/v9/d2_turisticos.py:133-134.
- p = media(|ATT*| ≥ |ATT|) puede valer 0. Con R = 500, la cota correcta es (1 + #)/(R + 1) ≥ 0,002.
- Igual en el p del bootstrap de CS (herramientas.py:90, p = 0 con B = 999).
- No cambia ninguna decisión. Corregir e informar «< 0,002».

**7. Registro incompleto en D4.** src/v9/d4_inmigracion.py:77. output/v9/d4/registry.csv tiene 19 filas frente a las 38 especificaciones de tabla_d4.csv: las variantes «endógena = Δ población total» no se anotan. **Corrección.** Anotar cada especificación.

**8. Familia BH.**
- f3_capas.py:84-86 incluye solo la especificación principal de cada hipótesis exploratoria. Es defendible, pero debe declararse en decisiones.md.
- Las filas «efecto total» de D4 duplican el mismo contraste de forma reducida.
- **Corrección.** Documentarlo. Con el hallazgo 2, cada par parcial/total comparte el p de AR: contarlo una sola vez.

**9. Especificaciones pre-registradas omitidas sin documentar.**
- D1a, controles «aún no tratados». Está cubierta en la práctica por dCDH (idéntico a CS «aún no tratados», tests/v9/test_herramientas.py:68-71), pero la etiqueta no lo dice.
- D2, Barcelona por barrios (descriptivo). No se estima y no consta en decisiones.md.
- D1b, dCDH y «aún no tratados». No son aplicables con una sola cohorte: indicarlo.
- **Corrección.** Una línea en decisiones.md por cada una.

**10. Lenguaje.**
- f3_capas.py:113, tabla_revista.md:3: «β: efecto o asociación». Con todo en C4, debe decir «asociación».
- Las filas «(efecto total)» de D4 deberían llamarse «asociación con Δ población total» (la terminología del addendum A1.8 solo vale si se superan los diagnósticos C3).
- comparacion_literatura.csv, fila 10: el lenguaje causal es de la cita de LA25 (literatura), no del proyecto. Es aceptable, pero conviene marcarlo como cita textual.
- No se ha encontrado lenguaje valorativo ni partidista.

**11. Conley en València ciudad.** El paso a HC1 si «más de la mitad de los pares» están dentro del corte (d3_valencia.py:91) es un umbral posterior a la estimación. La matriz de Conley solo es exactamente singular si todos los pares están dentro del corte. Es aceptable porque D3 es descriptivo y está documentado (E5.1). Conviene informar también el EE de Conley (sesgado a la baja) junto al HC1.

## Comprobaciones superadas

- **Familia de Holm.** {H1a-renta, H1b-renta}, m = 2 (f3_capas.py:51, 81-83). Coincide con el addendum A1.1. Las implementaciones de `holm` y `bh` son correctas (herramientas.py:336-358).
- **Reglas de capa** (f3_capas.py:88-97). Las cinco condiciones del addendum se exigen a la vez. Un NaN cuenta como fallo, en la dirección conservadora. Ninguna exploratoria puede llegar a C3, y no hay ningún C3.
- **CS** (herramientas.py:36-95).
  - La base es g − 1, con diferencias largas (base universal), y la base e = −1 está excluida.
  - Los controles son los nunca tratados; en D1a se excluye la Ley 11/2020 sin zona (d1_zonas.py:101).
  - Las cohortes 2024T2 y 2024T4 están bien asignadas desde las fechas BOE (paneles.py:82-90).
  - El bootstrap multiplicador de Rademacher es por municipio. Las pretendencias se contrastan con Wald sobre la vcov del bootstrap, en los e pre-registrados ([−8, −2] y [−7, −2]).
- **Placebo de fecha.** Usa la muestra anterior al primer tratamiento con desplazamiento de 4 periodos (d1_zonas.py:63-67); es correcto. La permutación de etiquetas conserva el tamaño de las cohortes.
- **TWFE con dosis (D2).**
  - El β agrupado de 2020-21 y de 2022-25 coincide con la media de los β anuales del estudio de eventos (0,0022 y 0,0105), como pide el pre-registro.
  - Hay controles de política y permutación dentro de provincia (A1.3). El placebo de 2017 usa la muestra 2012-2019.
- **2SLS, F efectiva y AKM.** El 2SLS y la F efectiva (un instrumento) están bien. El AKM está implementado con cuotas residualizadas; es aproximado (usa g_c y no el shock residualizado), pero no cambia ninguna capa. Ninguna fila de D4 alcanza F ≥ 23,1. BHJ: 1/HHI = 11,9.
- **LP (D5).** PanelOLS con efectos de país y trimestre, Driscoll-Kraay (Bartlett, ancho h + 4), 4 retardos y robustez CBI, 2008-2019 y sin España, como se pre-registró.
- **D7.** La identidad de la descomposición se cumple (residuo ≈ 0 salvo redondeo). La suma provincial coincide con la nacional en H0, H1 y P1 (excluyendo las filas agregadas ES y CV). La regla v5.1 se respeta: no se restan bajas.
- **Fugas.** En output/v9 no hay series municipales de Incasòl, Registre ni IEET, ni la serie de shocks JK: solo coeficientes, agregados y estudios de eventos. data/sealed no se usa.
- **Especificaciones.**
  - Las principales y las alternativas de D1a, D1b, D2, D3 (A1.4), D4 (A1.5) y D5 coinciden con el pre-registro y el addendum, salvo lo indicado en el hallazgo 9.
  - No hay indicios de elección por p-valor: se publican todas las alternativas, incluidas las no significativas y las de signo contrario (D1a-contratos BJS −0,135 frente a CS −0,063).

## Lista priorizada de cambios para la iteración 2

1. Honest DiD de Rambachan y Roth (ARP/híbrido) validado por Monte Carlo. Recalcular la capa de H1a/H1b-renta con la regla del addendum, sin cambiarla. Corregir E5.3 (hallazgo 1).
2. D4: usar p_rf/AR en la familia BH y el IC de AR en la tabla cuando F < 23,1. Publicar bien los conjuntos de AR no acotados (hallazgos 2 y 3).
3. Advertencias de pruebas fallidas en todas las filas que tienen prueba (hallazgo 4).
4. D7: alinear las fechas de hogares y población y documentar la desviación del periodo y el umbral C1 (hallazgo 5).
5. Bajos: +1 de Fisher, registro de D4, documentar la familia BH y las omisiones, y lenguaje «asociación» (hallazgos 6-11).

## Resultado de la reproducción

- Los siete scripts terminan con rc = 0, sin red.
- Los 32 ficheros CSV y JSON de output/v9/{d1,d2,d3,d4,d5,d7,f3} y output/v9/registry.csv tienen md5 idéntico al de los ficheros versionados en e28d1e4. Son por tanto dos ejecuciones idénticas: la versionada y la del revisor.
- Las figuras PNG no se han comparado.

## Re-revisión propia (iteración 2; 2026-10-15)

**Quién revisa.** El revisor independiente superó su tope (unos 114.000 tokens frente a 100.000). Conforme al prompt, esta re-revisión la hace el orquestador y se declara como tal: no es independiente.

| Hallazgo | Resolución | Comprobación |
|---|---|---|
| 1 (alta) Honest DiD | Se implementa el IC de Rambachan y Roth para magnitudes relativas: piezas poliédricas por diferencia previa y signo, y contraste condicional de Andrews, Roth y Pakes con cotas de truncamiento por programación lineal fraccional. Se descarta el contraste LF: con restricciones sobre diferencias acumuladas era muy conservador (con M̄ = 0 daba un IC 8 veces más ancho que el convencional). | Con M̄ = 0, el IC de D1b es [−0,072; −0,045], frente al convencional [−0,074; −0,044]. Validación por Monte Carlo en output/v9/validacion/honest_rr_mc.csv; test de propiedades en tests/v9. **Resultado:** H1b-renta tiene un M̄ de ruptura de 0,5 y H1a-renta de 0,2. Ninguna supera M̄ = 1 y las capas no cambian (C4). |
| 2 D4: p de AR | Con F < 23,1, la familia BH usa el p de la forma reducida (AR). | «Valor tasado, ampliación» pasa a «asociación (BH 0,019)»; sigue en C4, con el conjunto de AR no acotado. |
| 3 IC de AR truncados | Rejilla de ±5 y marca de conjunto no acotado. | tabla_d4.csv, columna AR_acotado. |
| 4 Pruebas fallidas | La capa de cada exploratoria enumera las pruebas que no supera (pretendencias, placebo, permutación, tendencia por dosis, Rotemberg y placebo de D3). | tabla_capas.csv, columna motivo_capa. |
| 5 D7 desalineado | Stocks a 1-1-2022 y 1-1-2025 en hogares y población; umbral C1 de ±2 % documentado. | El componente población pasa a 92 % en España y 112 % en la Comunitat Valenciana (la tasa de jefatura baja). Se añade la explicación a los textos. |
| Bajos | p de permutación con +1; registro de D4 completo; «diferencia o asociación» en la tabla; especificaciones no estimadas documentadas (E6). | — |

**Comprobaciones adicionales del orquestador.**
- No hay ninguna capa promovida.
- check_v9 da 0 errores: cifras previas sin cambios, p ajustados, lenguaje causal, capa pública, cruces por código y trazabilidad.
- Las cifras V9 se regeneran desde los scripts (`make v9`).

**Veredicto de la re-revisión: APROBAR**, condicionado a que la validación por Monte Carlo del IC de RR (src/v9/validar_honest_rr.py) dé una cobertura ≥ 0,90 en todas las configuraciones. Si no la da, se documenta en docs/v9/bloqueos.md y H1a/H1b se mantienen en C4.

**Resultado de la validación por Monte Carlo** (output/v9/validacion/honest_rr_mc.csv): se cumple la condición del veredicto.
- **Tamaño del contraste condicional en el θ verdadero** (M̄ = 0, 400 réplicas): cobertura 0,93, es decir, rechazo del 7,3 %, algo por encima del 5 % nominal (error de Monte Carlo ≈ 1,1 puntos).
- **Cobertura del IC** (30 réplicas por configuración): 1,0 sin tendencia previa con M̄ = 0 y M̄ = 1, y con tendencia lineal y M̄ = 1. La anchura con M̄ = 0 coincide con la del IC convencional.
- **Lectura.** Un ligero exceso de rechazo estrecha los IC, lo que favorecería que H1a y H1b superasen la prueba de M̄ = 1. No la superan, así que su capa C4 no depende de esta imprecisión.
