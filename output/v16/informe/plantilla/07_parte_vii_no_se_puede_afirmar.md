## Parte VII · Lo que no se puede afirmar y por qué

Esta parte evalúa afirmaciones frecuentes en el debate. No evalúa a quien las dice. Para cada una indica qué no se puede afirmar con los datos y los diseños disponibles, y por qué: datos, diseño, potencia o pruebas fallidas.

Tres reglas de lectura:
- La ausencia de hallazgo no demuestra la ausencia del fenómeno. Muchos diseños tienen poca potencia o no tienen inferencia válida.
- Todo lo de V15 y V16 es [C4]. Ningún resultado alcanza C3. Las estimaciones se leen como asociaciones. <!-- check:cifra-libre (nombres de versión y de capa) -->
- Los pre-registros de V15 y V16 son internos, sin sello de tiempo externo (anexo C). <!-- check:cifra-libre (nombres de versión) -->

### VII.1 «Hay una burbuja» y «no hay burbuja»

**Qué no se puede afirmar.** Ni que haya una burbuja ni que no la haya [C4].

**La pista de V16 (Q9-g), no confirmada [C4].**
- Q9-g mide la exuberancia estadística (GSADF) del factor común del cociente entre el valor tasado y el IPC de alquiler. El estadístico es {{V16-Q9-g}}. El rango que se muestra es el valor crítico bootstrap del 95 %. <!-- check:cifra-libre (id de pregunta) -->
- El p sin ajuste es {{V16-Q9-gp:num}}. <!-- check:cifra-libre (id de pregunta) -->
- Con el control de falsos descubrimientos de Benjamini-Yekutieli sobre la rama de diseños (m = 21), el q es {{V16-FDR-Q9-g-q:num}}. El umbral pre-registrado es q ≤ 0,10 y no se alcanza. Por eso es una pista y no un hallazgo. <!-- check:cifra-libre (m = 21 y umbral q ≤ 0,10 del diseño) -->
- Q9 no tiene magnitud de referencia pre-registrada, así que tampoco se cumple la condición de tamaño. <!-- check:cifra-libre (id de pregunta) -->

**Tres advertencias.**
1. **Corrección múltiple.** El p sin ajuste no es el que cuenta. Tras el ajuste, el q queda por encima del umbral. Las pruebas sin p válido, por herramienta no apta, cuentan en el denominador y no pueden rechazarse.
2. **Valor tasado suavizado y con retraso.** La tasación se suaviza y llega tarde. Eso puede generar un patrón explosivo aparente. La revisión adversarial lo lee como artefacto probable: la mayoría de las fechas marcadas caen en tramos en que el cociente baja o está plano. Además, la prueba de calibración no cubre este proceso generador, porque la variación del factor es persistente y heterocedástica.
3. **Una exuberancia estadística no identifica una burbuja.** Un resultado explosivo es compatible con cambios en los fundamentales, en los tipos de interés o en la composición de lo que se mide. Con tipos de interés, V7.2 no rechaza. La alternativa con SERPAVI anual no rechaza, pero tiene muy pocos periodos y no tiene potencia. <!-- check:cifra-libre (nombre de versión) -->

**El GSADF de V7.2, corregido (K20) [C4].**
- Cocientes nacionales (precio/renta y precio/alquiler) con exuberancia tras el ajuste múltiple, en la familia publicada de 8 contrastes: {{V72-GSADF-ratios-bh:num}}. <!-- check:cifra-libre (tamaño de la familia de contrastes y nombre de versión) -->
- Solo como sensibilidad, con el ajuste limitado a la familia de 4 cocientes: {{V72-GSADF-ratios-bh4-sens:num}}. <!-- check:cifra-libre (tamaño de la familia de contrastes) -->
- Sin ajuste múltiple: {{V72-GSADF-ratios-p05:num}}.
- Niveles de precio nacionales (IPV y valor tasado) con exuberancia tras el ajuste: {{V72-GSADF-niveles-bh:num}}.
- Series de comunidades autónomas (17 comunidades) con exuberancia tras el ajuste: {{V72-GSADF-ccaa-bh:num}}. <!-- check:cifra-libre (número de comunidades del diseño) -->
- Muestra de entrenamiento de v6 (11 comunidades): {{V72-GSADF-ccaa-v6:num}}. <!-- check:cifra-libre (número de comunidades del diseño y nombre de versión) -->

La familia principal es la de 8 contrastes. La de 4 es una sensibilidad: se muestra para que el lector vea que el recuento cambia con el tamaño de la familia. Nada de esto identifica una burbuja ni la descarta. <!-- check:cifra-libre (tamaño de las familias de contrastes) -->

**Explicación en lenguaje llano.** Es un cambio de cifras de la 1.0 y se cuenta aquí.
- **Qué decía la 1.0.** Que los niveles de precio nacionales y varias series autonómicas eran «explosivos» tras el ajuste. [FALTA CIFRA: recuento anterior de series de niveles y autonómicas calificadas de explosivas en la 1.0, en ERRATA.md] <!-- check:cifra-libre (versión) -->
- **Por qué era incorrecto.** Por dos errores de código.
  - **E1.** El contraste compara cada serie con miles de series simuladas sin burbuja. La regla que elige cuántos retardos simula el bootstrap comparaba modelos estimados con distinto número de datos. Eso la sesgaba. <!-- check:cifra-libre (id de error) -->
  - **E2.** La serie del IPV de Navarra se cortaba en 2014 porque faltaba otra serie de Navarra en 2015-2018. <!-- check:cifra-libre (id de error y años) -->
- **Cómo se vio.** La réplica ciega de V16 rehízo las cifras sin leer el código original. No coincidían, y la reconciliación encontró E1 y E2. <!-- check:cifra-libre (versión e ids de error) -->
- **Qué da el cálculo corregido.** {{V72-GSADF-niveles-bh:num}} series de niveles y {{V72-GSADF-ccaa-bh:num}} series autonómicas con exuberancia tras el ajuste. También se pasó de 499 a 4.999 simulaciones, porque con 499 los recuentos cambiaban con la semilla. <!-- check:cifra-libre (número de simulaciones del diseño) -->
- **Qué no cambia.** La conclusión de fondo: no se puede afirmar que haya una burbuja ni que no la haya. Que no salga exuberancia no demuestra alineación con los fundamentales, porque el contraste tiene poca potencia con 78 trimestres. Que saliera tampoco identificaría una burbuja. <!-- check:cifra-libre (número de trimestres de la muestra) -->

El detalle, con los valores de antes y de después, está en el anexo de erratas y en ERRATA.md.

**Otras pruebas.** El largo plazo entre valor tasado y alquiler no se contrasta: Westerlund, CIPS y CS-ARDL no pasaron el Monte Carlo (E1 de V15 y Q9-c de V16). Las elasticidades de largo plazo se dan solo como estimaciones puntuales, con un rango entre estimadores que incluye ambos signos ({{V16-Q9-c}}). En el panel regional de V7.1, las hipótesis de largo plazo confirmadas son {{V71-S3-largo-confirmadas}}. <!-- check:cifra-libre (ids de análisis y de versión) -->

### VII.2 «Un solo factor es el responsable de la subida»

**Qué no se puede afirmar.** Que turismo, inmigración, falta de oferta, tipos de interés, compradores extranjeros o empresas sean el factor principal.

**Por qué.**
- **Datos.** Los factores se mueven juntos. El componente común a las comunidades y a la zona euro es grande: la correlación del factor común español con el de la zona euro es {{V8-H8-9-est}} [C4]. Eso describe comovimiento, no atribución.
- **Diseño.** En V8, la regla de designación de un factor como el más relevante dio «no designado» en los diez casos (dos mercados por cinco periodos). Los métodos discrepan entre sí. <!-- check:cifra-libre (versión y diseño de V8: diez casos = dos mercados por cinco periodos) -->
- **Instrumentos.** Los instrumentos externos de V8 que cumplen las condiciones de C3: {{V8-M5-c3}}. El F efectivo de la primera etapa para el empuje migratorio es {{V8-H8-7-F}}. <!-- check:cifra-libre (versión y nombre de capa) -->
- **Pruebas fallidas.** Ninguna hipótesis de V8 pasa Holm con un instrumento que supere C3. V9, V15 y V16 no alcanzan C3 en ninguna pregunta. <!-- check:cifra-libre (versiones y nombre de capa) -->
- **Atribuciones.** Siempre se dan con bandas. Una atribución sin banda no es citable.

**Qué sí hay.** Hechos [C1] sobre cuánto han subido el precio y el alquiler, y sobre cuánto han crecido los hogares frente a las viviendas terminadas (resumen ejecutivo). Describen qué ha pasado, no qué lo ha movido.

### VII.3 «Los pisos turísticos suben (o no suben) el alquiler»

**Qué no se puede afirmar.** Ni la dirección ni la magnitud de la asociación entre vivienda turística y alquiler en España.

**Por qué.**
- **Datos.** El INE publica la vivienda turística como estadística experimental, con pocas ediciones. El SERPAVI mide el stock de contratos declarados, no los contratos nuevos. Las exposiciones de los registros autonómicos se reconstruyen con supuestos de fecha.
- **Potencia.** En H3 (V15), el coeficiente principal ({{V15-H3-beta}}) está por debajo del efecto mínimo detectable ({{V15-H3-mde}}). La mediana de su multiverso es {{V15-H3-rango}}. H3 es no concluyente, no nula. <!-- check:cifra-libre (ids de hipótesis y versión) -->
- **Diseño.** Q2a (provincias) es no concluyente. Q2c (IPVA municipal) cambia de signo según la especificación, falla la prueba de Oster y tiene heterocedasticidad. En E4 (Cataluña y Comunitat Valenciana), la regla puntual de pretendencias la cumplen {{V15-E4-compat}}. El BLP/GATES no pasó el Monte Carlo. <!-- check:cifra-libre (ids de pregunta) -->
- **Triangulación.** H3 y Q2a tienen el mismo signo; Q2c, el contrario. Las escalas «por desviación típica» no son comparables entre diseños, así que no se comparan magnitudes. <!-- check:cifra-libre (ids de pregunta) -->

**Qué sí hay.** Una cota [C2]: el aumento de viviendas turísticas entre 2020 y 2024 equivale como máximo a {{B4-v3-vut-cantidad}}. En viviendas, con sustitución uno a uno, {{VER-B4-V2-1}} [C2]. Es una cota de cantidad, no de precio. <!-- check:cifra-libre (años) -->

### VII.4 «La inmigración sube (o no sube) los precios y el alquiler»

**Qué no se puede afirmar.** Que la inmigración suba o baje el precio o el alquiler.

**Por qué.**
- **Instrumentos débiles.** En V9, el F efectivo del instrumento por cuotas de origen es {{V9-D4-ipc-ampliacion-F}} (alquiler) y {{V9-D4-tasado-ampliacion-F}} (valor tasado). Está muy por debajo del umbral de 10 que fija el diseño de V8 para C3. En V8, el del empuje migratorio es {{V8-H8-7-F}}. <!-- check:cifra-libre (versiones y umbral F ≥ 10 del diseño) -->
- **Pocos orígenes efectivos.** En H4, el número efectivo de choques es {{V15-H4-neff}}. En Q3-c, el origen de mayor peso aporta {{V16-Q3-rotemberg-1}} del estimador. <!-- check:cifra-libre (ids de hipótesis y pregunta) -->
- **Fragilidad de H4.** {{V15-H4-beta}} [C4]. Cambia de signo al quitar los cinco orígenes de mayor peso, y la AKM no pasó el Monte Carlo. [FALTA CIFRA: mediana del multiverso de H4] <!-- check:cifra-libre (id de hipótesis) -->
- **Pretendencia de Q3-b.** {{V16-Q3-b-beta}} [C4]. El placebo con el periodo anterior da {{V16-Q3-b-pretendencia}}, del mismo orden. La inferencia de Conley no pasó el Monte Carlo. [FALTA CIFRA: mediana del multiverso de Q3-b] <!-- check:cifra-libre (id de pregunta) -->
- **Signos que dependen de la medida.** En el valor tasado provincial, la asociación es {{V16-Q3-c1-beta}}; en las compraventas, {{V16-Q3-c2-beta}}. Ninguna tiene inferencia válida.
- **Controles.** El signo cambia con el control de población, la medida de precio, el método y la escala. Controlar por población es un mal control, porque la población crece por la propia inmigración.
- **Datos.** El padrón por nacionalidad no recoge las nacionalizaciones y termina en 2022. <!-- check:cifra-libre (año) -->

**Qué sí hay.** La contabilidad [C4]: de dónde viene el aumento de hogares y de población (Parte I). Es descriptiva.

### VII.5 «Los topes al alquiler y las zonas tensionadas bajan (o no bajan) el alquiler»

**Qué no se puede afirmar.** Que bajen el alquiler, que reduzcan la oferta o que no hagan ninguna de las dos cosas.

**Por qué.**
- **Datos.** Solo hay trimestres posteriores a la declaración para Cataluña. Fuera de Cataluña, la primera zona vigente empieza en {{V16-Q1-2}}, después del último año de SERPAVI del entrenamiento: Q1b no es estimable. El SERPAVI es stock de contratos; un tope sobre contratos vigentes no se lee con los contratos nuevos. En Cataluña, la brecha de crecimiento entre nuevos y vigentes es {{V16-HEC-ALQ-BRECHA-2124-CAT}} [C1]. <!-- check:cifra-libre (ids de pregunta y periodo) -->
- **Diseño de H1.** En V15, la estimación de entrenamiento tiene signo negativo. Falla las pretendencias y el placebo temporal. La cota de Lee llega prácticamente a cero ({{V15-H1-lee}}). El control sintético de los grandes municipios da signo contrario. Solo se cita el signo, sin magnitud. H2 no tiene señal estable. <!-- check:cifra-libre (ids de hipótesis y versión) -->
- **Pretendencias de Q1c.** El estudio de eventos muestra rupturas en la brecha entre provincias tratadas y no tratadas antes del primer tratamiento. <!-- check:cifra-libre (id de pregunta) -->
- **V9.** La Ley 11/2020 se asocia con {{V9-D1b-renta-att}} en la renta de los contratos nuevos frente a municipios comparables [C4]. Es compatible con la literatura y no supera la robustez a desviaciones de tendencia. <!-- check:cifra-libre (versión y número de ley) -->
- **Selección.** Los municipios tratados no se eligen al azar: la declaración depende de criterios de precio (art. 18 de la Ley 12/2023). Entre los municipios que superan el criterio, la tasa de declaración es {{V16-Q1-6}} (el rango va de los no elegibles a los elegibles) [C4]. <!-- check:cifra-libre (artículo y número de ley) -->
- **Desplazamientos.** El paso a contratos de temporada y a venta no se puede medir con los datos de entrenamiento.
- **Potencia.** Las herramientas de inferencia (Honest DiD, Webb, control sintético) no pasaron el Monte Carlo.

**Pendiente.** H1 y H2 se evaluarán con la muestra sellada, a partir de marzo de 2027. <!-- check:cifra-libre (ids de hipótesis y fecha del calendario) -->

### VII.6 «Los compradores extranjeros o no residentes suben (o no suben) el precio»

**Qué no se puede afirmar.** Que limitar o liberar las compras de no residentes cambie el precio. Ni que el fin de la golden visa tenga algún efecto en la cuota de compradores.

**Por qué.**
- **Datos.** La fuente (MIVAU) da el total de no residentes, sin separar UE de extra-UE. La cuota total no identifica los visados de oro. No hay autorizaciones por programa.
- **Diseño de Q8.** Es descriptiva: sin estimador, sin placebo, sin diferencias en diferencias. La cuota de no residentes en el agregado de entrenamiento pasa de {{V16-Q8-2}} a {{V16-Q8-1}}, una variación de {{V16-Q8-3}} [C4]. El año anterior ya había bajado, y el rango de la variación incluye ese cambio. <!-- check:cifra-libre (id de pregunta) -->
- **Hecho de la 1.0.** Compraventas con comprador extranjero (residente o no): {{compradores_extranjeros}} [C4]. No residentes: {{compradores_no_residentes}} [C4]. Ministerio y Notariado no son independientes, así que no llega a C1. <!-- check:cifra-libre (nombres de capa y versión) -->
- **Asociación.** La asociación bivariada del precio con el peso inicial de no residentes ({{R1A-H4}}) es una correlación entre provincias, no una identificación.

### VII.7 «Los grandes tenedores controlan el alquiler»

**Qué no se puede afirmar.** Cuántas viviendas en alquiler, o con qué precio, están en manos de grandes tenedores.

**Por qué.**
- **Datos.** El Catastro da la titularidad por tramos de inmuebles (V12), pero cuenta viviendas, no contratos de alquiler. En España sin País Vasco ni Navarra, en 2026, las viviendas de titulares con más de diez viviendas son {{V12-B5-pct_mas10}} y las de titulares con más de cien son {{V12-B5-pct_mas100}} [C4]. No dicen cuántas están alquiladas, vacías o en venta. <!-- check:cifra-libre (versión, tramos de titularidad del Catastro y año) -->
- **Compraventas.** Las compraventas con comprador persona jurídica son {{R1C-004}} [C4]. La persona jurídica no equivale a gran tenedor.
- **Diseño.** Ningún diseño de V15-V16 contrasta conductas de precio por tipo de titular. Las solicitudes de datos de titularidad del alquiler figuran como pendientes en la 1.0 (S1, S3 y S4). <!-- check:cifra-libre (versiones e ids de solicitud) -->

### VII.8 «Bajar el ITP abarata (o no abarata) la compra»

**Qué no se puede afirmar.** Que bajar o subir el tipo general del ITP cambie el precio o las compraventas.

**Por qué.**
- **Datos.** Las compraventas provinciales de entrenamiento son el total de vivienda, sin separar usada y nueva. Hay {{V16-Q6-cambios}} cambios de tipo en pocas comunidades, concentrados en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo. <!-- check:cifra-libre (años del calendario) -->
- **Q6-p (valor tasado).** {{V16-Q6-p-beta}} [C4]. No concluyente: sin inferencia válida y por debajo de la referencia de diseño. <!-- check:cifra-libre (id de pregunta) -->
- **Q6-v (compraventas).** El placebo es mayor que la estimación y de signo contrario. No se cita con cifra. <!-- check:cifra-libre (id de pregunta) -->
- **Herramientas.** dCDH, Honest DiD y la inferencia por aleatorización no pasaron el Monte Carlo.
- **Exclusiones.** País Vasco, Ceuta y Melilla quedan fuera por falta de tipo general comparable.

### VII.9 «Falta oferta» y «el suelo es el cuello de botella»

**Qué no se puede afirmar.** Que construir más baje (o suba) el alquiler o el precio, ni cuánto pesa el suelo.

**Por qué.**
- **Datos.** La pendiente, la costa, el agua y el planeamiento no están en disco y figuran como tareas del autor. El coste de construcción no tiene fuente verificable.
- **Diseño de Q4.** Usa el porcentaje de Red Natura como restricción física. La Red Natura no es exógena: se asocia con lo rural y la despoblación. Los residuos tienen dependencia espacial fuerte, y el placebo de choque adelantado tiene el mismo signo y mayor tamaño que el resultado. <!-- check:cifra-libre (id de pregunta) -->
- **Identificación.** No hay una elasticidad de oferta instrumentada con inferencia válida, así que no se separan oferta y demanda.
- **E2 (V15).** La presión demográfica no cubierta por la obra se asocia de forma positiva con el crecimiento del alquiler en las especificaciones con dato. No hay intervalo y las provincias son pocas. Que las viviendas iniciadas se asocien con el alquiler no indica que construir lo suba. <!-- check:cifra-libre (ids de análisis y versión) -->

**Qué sí hay.** Los hogares crecen más que las viviendas terminadas ({{dh_2125}} y {{terminadas_1924}}) [C1]. El balance 2021-2024 es positivo, con cota {{L3-DEF-2124-SINBAJAS}} [C2]. Las viviendas liberadas por envejecimiento no se restan de la necesidad. <!-- check:cifra-libre (periodo) -->

### VII.10 «Este modelo predice el precio» y «lo que predice es lo que lo mueve»

**Qué no se puede afirmar.** Que algún modelo del proyecto prediga el precio nacional mejor que un AR(4) sencillo, ni que las variables que ayudan a predecir sean las que lo mueven. <!-- check:cifra-libre (AR(4): nombre del modelo) -->

**Por qué.**
- **H5 (V15).** La combinación de DFM, BVAR, LASSO y ARDL no supera al AR(4). Razón del ECM: {{V15-H5-razon-ecm:valor}} [C4], la de la implementación pre-registrada. La réplica ciega da una razón menor [FALTA CIFRA: razón de H5 en la réplica ciega]. La conclusión es la misma en todas las implementaciones. El DM-HLN dio {{V15-H5-p-dm:valor}} y no se cita como prueba, porque no pasa el Monte Carlo de V16. <!-- check:cifra-libre (ids de hipótesis, versiones y AR(4)) -->
- **Q10 (V16).** MIDAS y el nowcasting no mejoran al AR(4) en el IPV ni en el IPC de alquiler. En las compraventas, la mejora aparente desaparece al excluir 2020. En el IPV, los intervalos conformes de MIDAS y del AR(4) cubren menos que su nivel nominal. <!-- check:cifra-libre (id de pregunta, versión, AR(4) y año) -->
- **Datos.** Las series son revisadas, no en tiempo real.
- **Coherencia con la 1.0.** En la validación sellada de v6 (provincias que los modelos no vieron), el mejor modelo supera a la línea base más exigente en {{K1-N-MEJOR}} de las 9 tareas. Es otro objetivo, otra escala y otra muestra que el agregado nacional trimestral de H5 y de V8. No contradice esa conclusión: en el agregado nacional ningún modelo gana al AR(4). <!-- check:cifra-libre (versiones, id de hipótesis y nueve tareas de la validación de v6) -->
- **Predicción no es identificación.** Las importancias de los modelos de predicción dicen qué variables ayudan a predecir, no qué pasaría si una variable cambiara.
