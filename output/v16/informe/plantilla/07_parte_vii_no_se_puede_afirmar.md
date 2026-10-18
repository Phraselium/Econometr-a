## Parte VII · Lo que no se puede afirmar y por qué

Esta parte evalúa afirmaciones frecuentes en el debate. No evalúa a quien las dice. Para cada una indica qué no se puede afirmar con los datos y los diseños disponibles, y por qué: datos, diseño, potencia o pruebas fallidas.

Tres reglas de lectura:
- La ausencia de hallazgo no demuestra la ausencia del fenómeno. Muchos diseños tienen poca potencia o no tienen inferencia válida.
- Todo lo de V15 y V16 es [C4]. Ningún resultado alcanza C3. Las estimaciones se leen como asociaciones.
- Los pre-registros de V15 y V16 son internos, sin sello de tiempo externo (anexo C). <!-- check:cifra-libre (identificadores de versión) -->

### VII.1 «Hay una burbuja» y «no hay burbuja»

**Qué no se puede afirmar.** Ni que haya una burbuja ni que no la haya [C4].

**La pista de V16 (Q9-g), no confirmada [C4].**
- Q9-g mide la exuberancia estadística (GSADF) del factor común del cociente entre el valor tasado y el IPC de alquiler. El estadístico es {{V16-Q9-g}}. El rango que se muestra es el valor crítico bootstrap del 95 %.
- El p sin ajuste es {{V16-Q9-gp:num}}.
- Con el control de falsos descubrimientos de Benjamini-Yekutieli sobre la rama de diseños (m = 21), el q es {{V16-FDR-Q9-g-q:num}}. El umbral pre-registrado es q ≤ 0,10 y no se alcanza. Por eso es una pista y no un hallazgo.
- Q9 no tiene magnitud de referencia pre-registrada, así que tampoco se cumple la condición de tamaño.
<!-- check:cifra-libre (m = 21 y umbral q ≤ 0,10 del diseño; identificadores de pregunta) -->

**Tres advertencias.**
1. **Corrección múltiple.** El p sin ajuste no es el que cuenta. Tras el ajuste, el q es mayor que el umbral. Las pruebas sin p válido por herramienta no apta cuentan en el denominador y no pueden rechazarse.
2. **Valor tasado suavizado y con retraso.** La tasación se suaviza y llega tarde. Eso puede generar un patrón explosivo aparente. La revisión adversarial lo lee como artefacto probable: la mayoría de las fechas marcadas caen en tramos en que el cociente baja o está plano. Además, la prueba de calibración no cubre este proceso generador (la variación del factor es persistente y heterocedástica).
3. **Una exuberancia estadística no identifica una burbuja.** Un resultado explosivo es compatible con cambios en los fundamentales, en los tipos de interés o en la composición de lo que se mide. Con tipos de interés, V7.2 no rechaza. La alternativa con SERPAVI anual no rechaza, pero tiene muy pocos periodos y no tiene potencia.

**El GSADF de V7.2, corregido (K20) [C4].**
- Cocientes nacionales (precio/renta y precio/alquiler) tras el ajuste múltiple, en la familia publicada de 8 contrastes: {{V72-GSADF-ratios-bh:num}} series con exuberancia.
- Solo como sensibilidad, con el ajuste limitado a la familia de 4 cocientes: {{V72-GSADF-ratios-bh4-sens:num}} serie.
- Sin ajuste múltiple: {{V72-GSADF-ratios-p05:num}} serie.
- Niveles de precio nacionales (IPV y valor tasado) tras el ajuste: {{V72-GSADF-niveles-bh:num}} series.
- Series de comunidades autónomas tras el ajuste (17 comunidades): {{V72-GSADF-ccaa-bh:num}} series.
- Muestra de entrenamiento de v6 (11 comunidades): {{V72-GSADF-ccaa-v6:num}} comunidades.
<!-- check:cifra-libre (tamaño de las familias de contrastes y de la muestra: 8, 4, 17 y 11) -->

La familia principal es la de 8 contrastes. La de 4 es una sensibilidad: se muestra para que el lector vea que el recuento cambia con el tamaño de la familia. Nada de esto identifica una burbuja ni la descarta.

**Explicación en lenguaje llano.** Es un cambio de cifras de la 1.0, y se explica.
- **Qué decía la 1.0.** Que los niveles de precio nacionales y varias series autonómicas eran «explosivos» tras el ajuste. [FALTA CIFRA: recuento anterior de series de niveles y autonómicas calificadas de explosivas en la 1.0, en ERRATA.md]
- **Por qué era incorrecto.** Por dos errores de código.
  - **E1.** El contraste compara cada serie con miles de series simuladas sin burbuja. La regla que elige cuántos trimestres pasados usa la simulación comparaba modelos estimados con distinto número de datos. Eso la sesgaba.
  - **E2.** La serie del IPV de Navarra se cortaba en 2014 porque faltaba otra serie de Navarra en 2015-2018.
- **Cómo se vio.** La réplica ciega de V16 rehízo las cifras sin leer el código original. No coincidían, y la reconciliación encontró E1 y E2.
- **Qué da el cálculo corregido.** {{V72-GSADF-niveles-bh:num}} series de niveles y {{V72-GSADF-ccaa-bh:num}} series autonómicas con exuberancia tras el ajuste. También se pasó de 499 a 4.999 simulaciones, porque con 499 los recuentos cambiaban con la semilla.
- **Qué no cambia.** La conclusión de fondo: no se puede afirmar que haya una burbuja ni que no la haya. Que no salga exuberancia no demuestra alineación con los fundamentales, porque el contraste tiene poca potencia con 78 trimestres. Que saliera tampoco identificaría una burbuja.

El detalle, con los valores de antes y de después, está en el anexo de erratas y en ERRATA.md. <!-- check:cifra-libre (E1, E2, 499 y 4.999 simulaciones, años y 78 trimestres: números del diseño) -->

**Otras pruebas.** El largo plazo entre valor tasado y alquiler no se contrasta: Westerlund, CIPS y CS-ARDL no pasaron el Monte Carlo (E1 de V15 y Q9-c de V16). Las elasticidades de largo plazo se dan solo como estimaciones puntuales, con un rango entre estimadores que incluye ambos signos ({{V16-Q9-c}}). En la regional de V7.2, {{V71-S3-largo-confirmadas}} hipótesis de largo plazo se confirman. <!-- check:cifra-libre (identificadores de resultado) -->

### VII.2 «Un solo factor es el responsable de la subida»

**Qué no se puede afirmar.** Que turismo, inmigración, falta de oferta, tipos de interés, compradores extranjeros o empresas sean el factor principal.

**Por qué.**
- **Datos.** Los factores se mueven juntos. El componente común a las comunidades y a la zona euro es grande: la correlación del factor común español con el de la zona euro es {{V8-H8-9-est}} [C4]. Eso describe comovimiento, no atribución.
- **Diseño.** En V8, la regla de designación de un factor como el más relevante dio «no designado» en los diez casos (dos mercados por cinco periodos). Los métodos discrepan entre sí.
- **Instrumentos.** Los instrumentos externos de V8 que cumplen las condiciones de C3: {{V8-M5-c3}}. El F efectivo de la primera etapa, por ejemplo para el empuje migratorio, es {{V8-H8-7-F}}.
- **Pruebas fallidas.** Ninguna hipótesis de V8 pasa Holm con un instrumento que supere C3. V9 y V15-V16 no alcanzan C3 en ninguna pregunta.
- **Atribuciones.** Siempre se dan con bandas. Una atribución sin banda no es citable.

**Qué sí hay.** Hechos [C1] sobre cuánto han subido el precio y el alquiler, y sobre cuánto han crecido los hogares frente a las viviendas terminadas (resumen ejecutivo). Describen qué ha pasado, no qué lo ha movido. <!-- check:cifra-libre (diez casos = dos mercados por cinco periodos, del diseño de V8) -->

### VII.3 «Los pisos turísticos suben (o no suben) el alquiler»

**Qué no se puede afirmar.** Ni la dirección ni la magnitud de la asociación entre vivienda turística y alquiler en España.

**Por qué.**
- **Datos.** El INE publica la vivienda turística como estadística experimental, con pocas ediciones. El SERPAVI mide el stock de contratos declarados, no los contratos nuevos. Las exposiciones de los registros autonómicos se reconstruyen con supuestos de fecha.
- **Potencia.** En H3 (V15), el coeficiente principal ({{V15-H3-beta}}) está por debajo del efecto mínimo detectable ({{V15-H3-mde}}). La mediana de su multiverso es {{V15-H3-rango}}. H3 es no concluyente, no nula.
- **Diseño.** Q2a (provincias) es no concluyente. Q2c (IPVA municipal) cambia de signo según la especificación y falla Oster y homocedasticidad. En E4 (Cataluña y Comunitat Valenciana) la regla puntual de pretendencias la cumplen {{V15-E4-compat}}. El BLP/GATES no pasó el Monte Carlo.
- **Triangulación.** H3 y Q2a tienen el mismo signo; Q2c, el contrario. Las escalas «por desviación típica» no son comparables entre diseños, así que no se comparan magnitudes.

**Qué sí hay.** Una cota [C2]: el aumento de viviendas turísticas entre 2020 y 2024 equivale como máximo a {{B4-v3-vut-cantidad}}. En viviendas, con sustitución uno a uno, {{VER-B4-V2-1}} [C2]. Es una cota de cantidad, no de precio. <!-- check:cifra-libre (identificadores de pregunta y años) -->

### VII.4 «La inmigración sube (o no sube) los precios y el alquiler»

**Qué no se puede afirmar.** Que la inmigración suba o baje el precio o el alquiler.

**Por qué.**
- **Instrumentos débiles o frágiles.** En V9, el F efectivo del instrumento por cuotas de origen es {{V9-D4-ipc-ampliacion-F}} (alquiler) y {{V9-D4-tasado-ampliacion-F}} (valor tasado), muy por debajo del umbral pre-registrado de 10. En V8, el del empuje migratorio es {{V8-H8-7-F}}.
- **Pocos orígenes efectivos.** En H4, el número efectivo de choques es {{V15-H4-neff}}. En Q3-c, el origen de mayor peso aporta {{V16-Q3-rotemberg-1}} del estimador.
- **Fragilidad.** H4: {{V15-H4-beta}} [C4]. Cambia de signo al quitar los cinco orígenes de mayor peso, y la AKM no pasó el Monte Carlo. [FALTA CIFRA: mediana del multiverso de H4]
- **Pretendencia.** Q3-b: {{V16-Q3-b-beta}} [C4]. El placebo con el periodo anterior da {{V16-Q3-b-pretendencia}}, del mismo orden. La inferencia de Conley no pasó el Monte Carlo. [FALTA CIFRA: mediana del multiverso de Q3-b]
- **Signos que dependen de la medida.** En el valor tasado provincial, la asociación es {{V16-Q3-c1-beta}}; en las compraventas, {{V16-Q3-c2-beta}}. Ninguna tiene inferencia válida.
- **Controles.** El signo cambia con el control de población, la medida de precio, el método y la escala. Controlar por población es un mal control, porque la población crece por la propia inmigración.
- **Datos.** El padrón por nacionalidad no recoge las nacionalizaciones y termina en 2022.

**Qué sí hay.** La contabilidad [C4]: de dónde viene el aumento de hogares y de población (atlas y contabilidad de la Parte I). Es descriptiva. <!-- check:cifra-libre (umbral F de 10 del diseño de V8/V9, años, cinco orígenes) -->

### VII.5 «Los topes al alquiler y las zonas tensionadas bajan (o no bajan) el alquiler»

**Qué no se puede afirmar.** Que bajen el alquiler, que reduzcan la oferta o que no hagan ninguna de las dos cosas.

**Por qué.**
- **Datos.** Solo hay trimestres posteriores a la declaración para Cataluña. Fuera de Cataluña, la primera zona vigente empieza en {{V16-Q1-2}}, y el último año del SERPAVI en el entrenamiento es anterior: Q1b no es estimable. El SERPAVI es stock de contratos; un tope sobre contratos vigentes no se lee con los contratos nuevos. En Cataluña, la brecha de crecimiento entre nuevos y vigentes es {{V16-HEC-ALQ-BRECHA-2124-CAT}} [C1].
- **Diseño.** En H1 (V15), la estimación de entrenamiento tiene signo negativo. Falla las pretendencias y el placebo temporal, la cota de Lee llega prácticamente a cero ({{V15-H1-lee}}), y el control sintético de los grandes municipios da signo contrario. Solo se cita el signo, sin magnitud. H2 no tiene señal estable.
- **Pretendencias.** En Q1c, el estudio de eventos muestra rupturas en la brecha entre provincias tratadas y no tratadas antes del primer tratamiento.
- **V9.** La Ley 11/2020 se asocia con {{V9-D1b-renta-att}} en la renta de los contratos nuevos frente a municipios comparables [C4]. Es compatible con la literatura y no supera la robustez a desviaciones de tendencia.
- **Selección.** Los municipios declarados son los de precio más alto. La definición legal depende del precio, así que declarar y tener un alquiler que sube van juntos: entre los municipios que superan el criterio de precio, la tasa de declaración es {{V16-Q1-6}} [C4].
- **Desplazamientos.** El paso a contratos de temporada y a venta no se puede medir con los datos de entrenamiento.
- **Potencia.** Las herramientas de inferencia (Honest DiD, Webb, control sintético) no pasaron el Monte Carlo.

**Pendiente.** H1 y H2 se evaluarán con la muestra sellada, a partir de marzo de 2027. <!-- check:cifra-libre (identificadores de pregunta y ley, fecha del calendario) -->

### VII.6 «Los compradores extranjeros o no residentes suben (o no suben) el precio»

**Qué no se puede afirmar.** Que limitar o liberar las compras de no residentes cambie el precio. Ni que el fin de la golden visa tenga algún efecto en la cuota de compradores.

**Por qué.**
- **Datos.** La fuente (MIVAU) da el total de no residentes, sin separar UE de extra-UE. La cuota total no identifica los visados de oro. No hay autorizaciones por programa.
- **Diseño.** Q8 es descriptiva: sin estimador, sin placebo, sin diferencias en diferencias. La cuota de no residentes en el agregado de entrenamiento pasa de {{V16-Q8-2}} a {{V16-Q8-1}}, una variación de {{V16-Q8-3}} [C4]. El año anterior ya había bajado; el rango de la variación incluye ese cambio.
- **Hecho de la 1.0.** Compraventas con comprador extranjero (residente o no): {{compradores_extranjeros}} [C4]. No residentes: {{compradores_no_residentes}} [C4]. Ministerio y Notariado no son independientes, así que no llega a C1.
- **Asociación.** La asociación bivariada del precio con el peso inicial de no residentes ({{R1A-H4}}) es una correlación entre provincias, no una identificación. <!-- check:cifra-libre (identificadores de pregunta) -->

### VII.7 «Los grandes tenedores controlan el alquiler»

**Qué no se puede afirmar.** Cuántas viviendas en alquiler, o con qué precio, están en manos de grandes tenedores.

**Por qué.**
- **Datos.** El Catastro da la titularidad por tramos de inmuebles (V12), pero cuenta viviendas, no contratos de alquiler. En España sin País Vasco ni Navarra, en 2026, las viviendas de titulares con más de diez viviendas son {{V12-B5-pct_mas10}} y las de titulares con más de cien son {{V12-B5-pct_mas100}} [C4]. No dicen cuántas están alquiladas, vacías o en venta.
- **Compraventas.** Las compraventas con comprador persona jurídica son {{R1C-004}} [C4]. La persona jurídica no equivale a gran tenedor.
- **Diseño.** No hay ningún diseño en V15-V16 que contraste conductas de precio por tipo de titular. Las solicitudes de datos de titularidad del alquiler siguen abiertas. <!-- check:cifra-libre (umbrales de tramo del Catastro: diez y cien, año 2026) -->

### VII.8 «Bajar el ITP abarata (o no abarata) la compra»

**Qué no se puede afirmar.** Que bajar o subir el tipo general del ITP cambie el precio o las compraventas.

**Por qué.**
- **Datos.** Las compraventas provinciales de entrenamiento son el total de vivienda, sin separar usada y nueva. Hay {{V16-Q6-cambios}} cambios de tipo en pocas comunidades, concentrados en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo.
- **Q6-p** (valor tasado): {{V16-Q6-p-beta}} [C4]. No concluyente: sin inferencia válida y por debajo de la referencia de diseño.
- **Q6-v** (compraventas): el placebo es mayor que la estimación y de signo contrario. No se cita con cifra.
- **Herramientas.** dCDH, Honest DiD y la inferencia por aleatorización no pasaron el Monte Carlo.
- **Exclusiones.** País Vasco, Ceuta y Melilla quedan fuera por falta de tipo general comparable. <!-- check:cifra-libre (años del calendario) -->

### VII.9 «Falta oferta» y «el suelo es el cuello de botella»

**Qué no se puede afirmar.** Que construir más baje (o suba) el alquiler o el precio, ni cuánto pesa el suelo.

**Por qué.**
- **Datos.** No están en disco la pendiente, la costa, el agua ni el planeamiento. El coste de construcción no tiene fuente verificable. El suelo urbano y urbanizable del MIVAU y los certificados de fin de obra están como tareas del autor.
- **Diseño.** Q4 usa el porcentaje de Red Natura como restricción física. La Red Natura no es exógena: se asocia con lo rural y la despoblación. Los residuos tienen dependencia espacial fuerte y el placebo de choque adelantado tiene igual signo y mayor tamaño que el resultado.
- **Pruebas fallidas.** Sin elasticidad de oferta instrumentada no hay forma de separar oferta de demanda.
- **Correlaciones.** En E2 (V15), la presión demográfica no cubierta por la obra se asocia de forma positiva con el crecimiento del alquiler en las especificaciones con dato. Sin intervalo, con pocas provincias y con una asociación de las iniciadas con el alquiler que no indica que construir suba el alquiler.

**Qué sí hay.** Hechos y cotas: los hogares crecen más que las viviendas terminadas ({{dh_2125}} y {{terminadas_1924}}) [C1]; el balance 2021-2024 es positivo, con cota {{L3-DEF-2124-SINBAJAS}} [C2]. Las viviendas liberadas por envejecimiento no se restan de la necesidad. <!-- check:cifra-libre (identificadores de pregunta y periodo) -->

### VII.10 «Este modelo predice el precio» y «lo que predice es lo que lo mueve»

**Qué no se puede afirmar.** Que algún modelo del proyecto prediga el precio nacional mejor que un AR(4) sencillo, ni que las variables que ayudan a predecir sean las que lo mueven.

**Por qué.**
- **H5 (V15).** La combinación de DFM, BVAR, LASSO y ARDL no supera al AR(4). Razón del ECM: {{V15-H5-razon-ecm:valor}} [C4], la de la implementación pre-registrada; la réplica ciega da una razón menor [FALTA CIFRA: razón de H5 en la réplica ciega]. La conclusión es la misma en todas las implementaciones. El DM-HLN dio {{V15-H5-p-dm:valor}} y no se cita como prueba, porque no pasa el Monte Carlo de V16.
- **Q10 (V16).** MIDAS y el nowcasting no mejoran al AR(4) en el IPV ni en el IPC de alquiler. En las compraventas, la mejora aparente sale de 2020-2021 y desaparece fuera de ese año. Los intervalos conformes cubren menos que su nivel nominal en MIDAS.
- **Datos.** Las series son revisadas, no en tiempo real.
- **Coherencia con la 1.0.** En la validación sellada de v6 (provincias que los modelos no vieron), el mejor modelo supera a la línea base más exigente en {{K1-N-MEJOR}} de las 9 tareas. Es otro objetivo, otra escala y otra muestra que el agregado nacional trimestral de H5 y de V8, y no contradice esa conclusión: en el agregado nacional no hay modelo que gane al AR(4).
- **Predicción no es identificación.** Las importancias de los modelos de predicción dicen qué variables ayudan a predecir, no qué pasaría si una variable cambiara. <!-- check:cifra-libre (identificadores de pregunta; nueve tareas de v6) -->
