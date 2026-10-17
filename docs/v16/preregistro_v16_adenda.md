# V16 · Adenda al pre-registro interno (respuesta a la revisión; vinculante)

**Estado:** escrita antes de estimar nada de V16 y fijada en el mismo commit que la etiqueta `prereg-v16`. **Prevalece** sobre docs/v16/preregistro_v16.md donde difiera.

**Origen.** Responde punto por punto a dos revisiones:
- revisor-preregistro: 25 hallazgos, veredicto «aprobar con cambios»;
- abogado-del-diablo: A1-A12 y B por pregunta, veredicto «no resiste en su redacción actual».

Las referencias «R n» son del revisor; «A n», «Q n-k» y similares, del abogado del diablo.

## 0. Cambios de código ya hechos (commit anterior a esta adenda)
- **R6 / A6.** En `holdout.sellar_v16`, el tope temporal es el mínimo entre los manifiestos de V15 y V16: V16 nunca sella más tarde que V15.
  - `evaluate_v16` se niega a abrir un panel que comparta variables con una hipótesis de V15 aún no evaluada (`hipotesis_v15_pendientes`).
  - Tests: tests/v16/test_holdout_v16.py.
- **R7 / A4.** `unidad_sellada_v16` sella a escala de CCAA las 8 comunidades enteras de v6 (02, 03, 04, 05, 13, 14, 15 y 17).
- **R21.** `f4_sellado.py` se niega a rehacer el sellado si la etiqueta prereg-v16 existe en local, y registra cada intento en docs/v16/sellado_intentos.log.
- **R1, R8 y A4-A5.** La rejilla queda fija en output/v16/potencia/rejilla_fija.csv, generada por src/v16/f4_rejilla.py (ver punto 4).

## 1. Capas: V16 no alcanza C3 (R10, A3, A10)
Se importan las reglas 3 y 4 de la adenda 2 de V15:
- un resultado estimado con datos ya vistos (entrenamiento) no pasa de C4;
- C3 exige una evaluación sellada temporal con IC 95 % que excluya el 0, más todas las pruebas de su diseño.

Además, V16 exige para C3 una triangulación entre dos diseños con fuentes de sesgo distintas, cada uno con C3 alcanzable. **La lista cerrada de parejas válidas está vacía:**
- Q5 tiene un solo instrumento.
- Q3 municipal en exclusión de orígenes es el mismo diseño.
- Q2b solo es robustez.
- Q1a no tiene resultado en entrenamiento.
- Q1b, Q2a y Q3 son C4 por las razones de los puntos 5-7.

En consecuencia, **todo V16 es C4 como máximo**: asociación, pista o nulo, sin lenguaje causal. Las pruebas de la sección 3 del pre-registro se ejecutan y se publican como diagnósticos.

Esta regla no se reabre después de ver resultados. Si llegan datos que permitan una pareja válida (Inside Airbnb histórico, pernoctaciones por país, MDT05), se añadirá con una adenda **antes** de mirar esos datos.

## 2. Control de falsos descubrimientos: dos ramas (R2, A1)
- **(i) Rama de diseños.** Una prueba principal por subdiseño, sin variantes; la lista está en el punto 3 (18 pruebas).
- **(ii) Rama de rejilla.** Una prueba por celda de rejilla_fija.csv con su especificación principal (83 pruebas). Las otras variantes de cada celda son robustez y no entran en el denominador.
- **Método:**
  - BH jerárquico en cada rama: primero se controla la familia de cada pregunta (p-valor de familia por Simes, q = 0,10) y después las pruebas dentro de cada familia rechazada (q = 0,10).
  - La tasa global declarada es ≤ 2q = 0,20 (cota de Yekutieli).
  - Si el Monte Carlo de la fase 5 no apoya la dependencia positiva (PRDS), se usa Benjamini-Yekutieli en lugar de BH.
- **Holgura.** No entra en ningún denominador y no puede producir hallazgos.
- **Resultados en varias familias.** Un mismo resultado puede aparecer en varias familias (Q1, Q2, Q3 y Q6 sobre compraventas). Cada familia se controla por separado y un resultado no cuenta como dos hallazgos.

## 3. Especificación principal por subdiseño (R9, A1)
Cada fila fija la muestra, la ventana, el estimador, la agrupación, la inferencia principal y la magnitud de referencia para (b).

**Reglas que valen para toda la tabla:**
- Los resultados van en logaritmos.
- La muestra es siempre el entrenamiento de V16 (`unidad_sellada_v16` = False y sin filas v6).
- En el control de falsos descubrimientos entra solo la prueba principal.
- El resto del multiverso se resume con la mediana de la estimación y la proporción de especificaciones con el mismo signo e IC 95 % que excluya el 0. Ese resumen no entra en el control.

| Id | Resultado | Estimador y muestra | Ventana | Agrupación e inferencia principal | Magnitud de referencia para (b) |
|---|---|---|---|---|---|
| Q1b | Δlog SERPAVI €/m², municipal anual | SDID. Tratados: municipios con zona vigente fuera de Cataluña. Donantes: municipios de CCAA sin zonas. Anticipación: 2023 fuera de la ventana | 2019-2022 frente a 2024 | Inferencia por aleatorización de Conley-Taber (principal); wild bootstrap de Webb por provincia (alternativa nombrada) | −0,75 % (−5 % en contratos nuevos, de la literatura L1, × 0,15 de cuota anual de contratos nuevos en el stock) |
| Q1c | log compraventas, provincial trimestral | Callaway-Sant'Anna con tratamiento = provincia con alguna zona vigente | 2019T1-2026T2 (hasta el corte de V15) | Wild bootstrap de Webb por provincia | ninguna comparable → (b) no se cumple |
| Q2a | Δlog IPC de alquiler provincial | DiD de intensidad: % de vivienda turística INE de 2020-08 × periodo posterior a 2022. Sin 2020-2021. **Forma reducida** (sin 2SLS) | 2017-2019 frente a 2022-2025 | Wild bootstrap de Webb por provincia | 0,04 × DT del log de la exposición entre provincias (elasticidad central de L2/P5, fijada con la DT de la exposición, que no depende del resultado) |
| Q2c | Δlog IPVA municipal | Exposición INE-VUT municipal estandarizada, con efectos fijos de municipio y año | 2021-2024 | Agrupación por provincia | la misma regla que Q2a; se lee como robustez de H3 |
| Q3-c1 | log valor tasado, provincial anual | Shift-share en forma reducida: cuotas del padrón de 2003 × crecimiento nacional sin la provincia; efectos fijos de provincia y año | 2011-2024 | AKM | elasticidad 1,0 (Saiz) por punto de población extranjera predicha |
| Q3-c2 | log compraventas, provincial anual | Igual que Q3-c1 | 2011-2024 | AKM | ninguna comparable → (b) no se cumple |
| Q3-b | Δlog SERPAVI por sección, 2021-2024 | Correlación transversal con la cuota de extranjeros de 2022 por sección; efectos fijos de municipio | 2021-2024 | Conley a 2 km | ninguna → (b) no se cumple (C4, correlación) |
| Q4a | log obra nueva neta del Catastro, municipal | Asociación con el % de Red Natura; efectos fijos de provincia | **2018-2025** (sin la regularización de 2013-2017) | Agrupación por provincia | ninguna → (b) no se cumple |
| Q4b | Δlog SERPAVI municipal | Choque de Q3 × % de Red Natura; efectos fijos de municipio y año | 2018-2024 | Agrupación por provincia | ninguna → (b) no se cumple |
| Q5-p | Δlog valor tasado nacional | Proyección local a h = 4 sobre la sorpresa mediana de Jarociński-Karadi (mensual agregada), con 4 rezagos | 1999T1-2026T2 | Newey-West con b fija | −0,6 % por desviación típica de sorpresa (P3 de V15) |
| Q5-a | Δlog IPC de alquiler nacional | Igual que Q5-p | 2002T1-2026T2 | Newey-West con b fija | ninguna comparable → (b) no se cumple |
| Q6-v | log compraventas de vivienda usada, provincial anual | De Chaisemartin-D'Haultfœuille (tratamiento continuo y no absorbente): cambio del tipo general del ITP en puntos; panel **anual** (las fechas aproximadas no afectan al año) | 2011-2024 | Aleatorización del calendario entre CCAA | −7 % por punto (Fritzsche-Vandrei, L4) |
| Q6-p | log valor tasado provincial anual | Igual que Q6-v | 2011-2024 | Igual que Q6-v | −1 % por punto (el vendedor soporta el impuesto, L4) |
| Q9-g | ratio valor tasado / IPC de alquiler: factor común de las provincias de entrenamiento | GSADF sobre el factor común (agregado) | 2002T1-2026T2 | Valores críticos por bootstrap | no aplica (prueba de explosividad) |
| Q9-c | log valor tasado frente a log IPC de alquiler, provincial | CS-ARDL: elasticidad de largo plazo | 2002T1-2026T2 | Bootstrap por bloques | no aplica |
| Q10-1 | Δlog IPV nacional, h = 1 | MIDAS frente a AR(4) | Ventana expansiva desde 2007T1 | DM-HLN | reducción del ECM ≥ 10 % (relevancia mínima declarada) |
| Q10-2 | Δlog IPC de alquiler nacional, h = 1 | *Nowcasting* con indicadores mensuales frente a AR(4) | Ventana expansiva desde 2002T1 | DM-HLN | ≥ 10 % |
| Q10-3 | Δlog compraventas nacional, h = 1 | MIDAS frente a AR(4) | Ventana expansiva desde 2007T1 | DM-HLN | ≥ 10 % |

**Fuera de la rama de diseños** (descriptivos, sin p-valor):
- **Q1a:** diagnóstico de elegibilidad (R4, Q1-1, Q1-2). La variable de asignación es SERPAVI 2018-2023, anterior a la declaración. Su resultado solo existe en la muestra sellada y no se evaluará antes de H1/H2.
- **Q2b:** solo robustez de Q2a (A-Q2-3).
- **Q7a:** descriptiva, con intervalos de Kolesár-Rothe si se muestra alguno (R16).
- **Q8:** descriptiva con las compras de no residentes del MIVAU (mivau_transacciones_residencia), sin distinción UE frente a fuera de la UE (R23).
- **Q9:** GSADF por provincia (R18).

## 4. Rejilla fija (R1, R7, R8, A4, A5)
- **Contenido.** output/v16/potencia/rejilla_fija.csv tiene 83 celdas, con una exposición, una ventana y una especificación principal por celda, construidas por src/v16/f4_rejilla.py:
  - Q1: 18 celdas;
  - Q2: 24;
  - Q3: 21;
  - Q4: 7;
  - Q6: 13.
- **Fuera de la rejilla:**
  - las escalas nacional y CCAA: tras quitar las 8 CCAA de v6 quedan 9 comunidades, menos de 10 unidades;
  - las celdas con menos de 10 unidades de entrenamiento;
  - Q5, Q7 y Q9, sin exposición territorial;
  - las celdas que repiten una hipótesis de V15: Q1 × Incasòl repite H1/H2, Q2 × SERPAVI por sección repite H3, y Q3 × SERPAVI municipal repite H4.
- **Recuento.** Se hace tras `unidad_sellada_v16`. En SERPAVI municipal quedan 2.014 unidades, frente a las 2.759 de la candidata sin filtrar.
- **Ventanas sin tratamiento.** Por ejemplo, Q1 antes de 2024. Son placebos y no entran en el denominador.

## 5. Q1 (R4, R5, Q1-1 a Q1-6)
- **Q1a:** diagnóstico descriptivo (punto 3). Sin RD ni capa causal.
- **Q1b, alcance:**
  - excluye Cataluña, para no reestimar H1/H2 antes de su evaluación;
  - el resultado principal es SERPAVI, porque los contratos nuevos de Cataluña son de H1;
  - en IPVA manda la especificación R-IPVA de la adenda de V15: Q1b no la repite.
- **Q1b, estimando:** el paquete autonómico (zona y normas concurrentes), no la declaración aislada. Anticipación: 2023 excluido.
- **Selección de CCAA:** las que declaran zonas no son aleatorias. Se publican el balance tratados/donantes en renta (ADRH), población, cuota de extranjeros, % de vivienda turística y exposición al tipo variable, y una especificación de robustez con esas variables como controles (A9).
- **Potencia:** SERPAVI es stock (dilución), así que Q1b se declara sin potencia para −0,75 % (MDE 7,1 %). Su lectura informativa es la de un nulo no concluyente.

## 6. Q2 (R3, Q2-1 a Q2-4)
- **Datos.** No hay pernoctaciones por país de origen en disco, así que el shift-share se retira. Q2a pasa a DiD de intensidad en forma reducida, C4, sin 2020-2021.
- **Solapes declarados:** V9-D2 (pretendencias rechazadas con la variación de la COVID) y H3.
- **Q2b:** fuera de la triangulación (dosis reconstruida, solo robustez).
- **Pernoctaciones por país de origen y municipio:** tarea del autor. Q2a solo se reabriría como shift-share con una adenda anterior a mirar esos datos.

## 7. Q3 (R13, Q3-1 a Q3-4)
- **Municipal de alquiler:** retirado. Es H4 con otra muestra y no se estima antes de H4.
- **Compra provincial:** declara como ya visto V9-D4-tasado, con F de 3,4 a 3,7 (C4).
- **Barrio:** correlación transversal C4, sin AKM ni Rotemberg, porque solo hay unos 5 choques por continente.
- **Balance:** BHJ con tendencias de 1998-2003 y una indicadora de ruptura EVR/EMCR en 2021.

## 8. Q4, Q5, Q6, Q7, Q9 y Q10 (R14-R18, Q4-1 a Q10-1)
- **Q4:**
  - ventana desde 2018, para evitar la regularización catastral;
  - una sola restricción (Red Natura): la costa no está en disco y se retira del multiverso;
  - descriptiva C4; la Red Natura no se presenta como exógena.
- **Q5:**
  - corrección del texto del pre-registro: el único MDE por debajo de la magnitud de la literatura es el del IPC de alquiler (0,25-0,59), donde esa magnitud, que es de precio, no aplica; el valor tasado a h = 4 tiene un MDE de 1,47 %, por encima de 0,6-1,0;
  - solapes declarados: V9-D5 (interacción con la hipoteca variable) y V8 (SVAR C3s del periodo P5);
  - controles negativos: población de 65 años o más e IPC de servicios no ligados a la vivienda;
  - la fase 5 calcula los horizontes 1 y 12, y el tamaño por Monte Carlo antes de usarlo.
- **Q6:**
  - de Chaisemartin-D'Haultfœuille (punto 3);
  - panel anual con el año de la ley; el año anterior a cada cambio queda fuera como anticipación;
  - magnitudes de referencia separadas para volumen (−7 % por punto) y precio (−1 % por punto);
  - la contradicción con la sección 0 desaparece porque el panel anual no usa la fecha exacta.
- **Q7a:**
  - comprobar en el BOE si el Plan Estatal 2018-2021 (RD 106/2018) tenía un programa para menores de 35 años. Si lo tenía, la diferencia en discontinuidades mide un cambio de generosidad y se dice;
  - contrastar en el umbral la proporción de inquilinos antes y después;
  - descriptiva.
- **Q9:**
  - principal: el GSADF agregado del factor común;
  - la ratio usa un índice de stock de contratos sobre tasaciones, y se declara;
  - alternativa con SERPAVI provincial en nivel;
  - lectura simétrica: «no explosivo» se publica como «no detectado con esta potencia», nunca como «no hay burbuja»; «explosivo» exige BH y réplica sellada;
  - ya visto: el GSADF por CCAA de la versión 7.2.
- **Q10:** los indicadores mensuales se usan en su última edición, no en tiempo real. Es un límite declarado: el *nowcasting* puede parecer mejor de lo que sería en directo. No se abre el bloque sellado antes de H5.

## 9. Regla de hallazgo local (R11, A3)
Las tres condiciones se endurecen:
- **(a)** q ≤ 0,10 en su rama.
- **(b)** Error de tipo S < 0,01 y de tipo M < 1,5, calculados con la magnitud de referencia **numérica** del punto 3, en su unidad. Sin magnitud no hay hallazgo, aunque haya q bajo: a lo sumo una pista.
- **(c)** Mismo signo y z ≥ 1,28 unilateral en la muestra sellada de V16:
  - en las preguntas municipales, el bloque espacial;
  - en las provinciales y nacionales, el bloque temporal, con al menos 4 trimestres o 1 año nuevos y nunca antes de que V15 evalúe la hipótesis con variables compartidas;
  - se retira la vía de «unidades independientes comparables».

## 10. Lectura simétrica y paradas (R12, A12)
- **Mismo tratamiento en ambos sentidos.** Las mismas pruebas, el mismo informe y el mismo paso por el abogado del diablo, sea cual sea el signo.
- **Nulo informativo.** TOST de equivalencia frente a la magnitud de referencia del punto 3. Sin magnitud, «no concluyente».
- **Parada D.** Solo si un resultado contradice **con dirección** una conclusión de la 1.0. Precisar un «no concluyente» no es contradecirlo. Todo resultado retenido por una parada se registra con su fecha en docs/v16/bloqueos.md.

## 11. Calibración (R24, A8)
- **Requisito.** Ninguna herramienta se usa si su tamaño al 5 % sale de [0,04; 0,06] con al menos 2.000 réplicas (criterio de V15). Prevalece sobre el intervalo [0,03; 0,08] de la sección 6.
- **Inferencia alternativa.** Hay una sola por diseño, la nombrada en el punto 3. Si ninguna pasa, el diseño es descriptivo.
- **Rechazos placebo nulos.** Un rechazo placebo de 0,0 cuenta como fallo de calibración, no como aprobado.

## 12. Priors y modelo jerárquico (R19)
- **Escala fijada.** Distribución normal(0, s) para el efecto medio, con s en la unidad del resultado:

| Familia | s |
|---|---|
| Q1 (log del alquiler) | 0,07 |
| Q2 (log del alquiler por desviación típica de exposición) | 0,06 |
| Q3 (elasticidad) | 1,0 |
| Q4 (log por desviación típica) | 0,05 |
| Q6 (log del volumen por punto) | 0,07 |
| Q6 (log del precio por punto) | 0,02 |

- **Varianza entre unidades.** Semi-normal(0, s).
- **Sensibilidad.** Con s × 0,5 y s × 2.
- **Anidación.** Solo dentro del mismo resultado: por ejemplo, SERPAVI por sección ⊂ municipio ⊂ provincia, nunca SERPAVI con IPV.

## 13. Bosques causales y DML (R20)
- **Qué entra en el control.** Solo la prueba conjunta de heterogeneidad BLP/GATES (Chernozhukov et al.), una por pregunta con diseño, en la rama de diseños como prueba adicional; el recuento pasa a 18 + 3 = 21.
- **Moderadores, fijados ahora:** renta media ADRH, población, cuota de extranjeros, % de vivienda turística y obra nueva per cápita.
- **Subgrupos.** Son descriptivos C4.

## 14. Sensibilidad y otras precisiones (A11, R22, R25)
- **Oster.** Se publica δ para β = 0 con R²max = 1,3 × R²; δ < 1 se declara frágil.
- **Cinelli-Hazlett.** Se publica el valor de robustez RV_q=1; RV < 0,05 se declara frágil.
- **E-values.** Se publican sin umbral.
- **Exclusión de grandes ciudades.** Barcelona, València, Sevilla y Málaga, más las islas no selladas. Zaragoza se quita de la lista porque está sellada en v6.
- **Comparación MDE-literatura.** Las magnitudes no comparables se declaran como tales (punto 3). Las decisiones del punto 1 usan solo magnitudes de diseño creíble en su unidad.
- **Desviación del plan.** La fase 4.1 pedía preguntas confirmatorias nuevas y V16 no tiene ninguna. Queda en docs/v16/desviaciones.md (publicado en metodologia/desviaciones_v16.md con make publicacion) y en decisiones K9.

## 15. Holgura y recuento (A2)
- **Recuento declarado:**
  - rama de diseños: 21 pruebas principales;
  - multiversos de los subdiseños: 202 especificaciones;
  - rejilla: 83 principales y 415 variantes de robustez.
  - Total: 721.
- **Holgura:** ≤ 20 % del declarado, es decir, 144 especificaciones, con las tres cláusulas de V15:
  - ninguna desviación puede ser principal ni sostener una capa;
  - cada una se anota en docs/v16/desviaciones.md **antes** de ver su resultado;
  - toda especificación probada entra en el Registry y en su rama del control.
- **Total máximo V16:** 865 (con V15, 4.969; ≤ 50.000).

## 16. Sello y fecha (A7, R21, R25)
- **Mientras dure el bloqueo B-1.** La línea 3 del pre-registro se lee en condicional: la etiqueta está creada en local. Mientras el autor no la publique en el remoto (tareas_autor §1):
  - las fases 5-7 siguen bloqueadas por la guarda (f);
  - evaluate_v16 no se abre.
- **Fecha de corte.** Es la del commit etiquetado. El intervalo hasta la publicación en el remoto se declarará al publicarla.
- **Congelación de descargas.** No se descarga ningún dato nuevo de las fuentes de V16 hasta que la etiqueta esté en el remoto, salvo lo que el autor aporte con una adenda previa.
- **Contenido del commit etiquetado.** Esta adenda, sellado_v16.json y el resultado del sellado.
