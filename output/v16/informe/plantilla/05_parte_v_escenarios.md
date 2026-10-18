## Parte V · Escenarios y predicción

Esta parte reúne tres cosas distintas. Primero, cuántas viviendas hacen falta según la contabilidad de la 1.0. Segundo, qué resulta de simular medidas bajo supuestos. Tercero, qué se puede predecir y con qué límites. Ninguna de las tres se lee como un efecto identificado. Un escenario responde a «qué pasa si se cumplen estos supuestos». Una predicción responde a «qué valor es probable». Ninguna responde a «qué produce qué». <!-- check:cifra-libre (versión 1.0 del estudio) -->

### V.1 Necesidad de vivienda y déficit (cifras de la 1.0)

#### Qué se mide

La necesidad anual suma el crecimiento de hogares, la reposición y el atraso a absorber. Resta las viviendas en construcción. No resta las viviendas que deja el envejecimiento. La proyección de hogares del INE ya las descuenta. Restarlas de nuevo las contaría dos veces. `make check` comprueba esta regla.

Los rangos de abajo son rangos entre supuestos, no intervalos de confianza. Las cifras de necesidad son [C4]: dependen de hogares de fuente única y de supuestos que ningún dato contrasta.

#### Necesidad anual

- La necesidad anual 2026-2035, en la base sin la sensibilidad X, es {{T3-H5b}} [C4]. <!-- check:cifra-libre (periodo 2026-2035) -->
- El rango pone todos los componentes en su extremo bajo o alto a la vez: {{T3-H5b:rango}} [C4].
- Es una cifra de orden de magnitud. Una cifra puntual no es defendible con estos datos.

Afirmación evaluada: «Hacen falta X viviendas al año». Veredicto de la 1.0: ANALIZADA, NO CONCLUYENTE [C4]. El valor depende del atraso y de las viviendas vacías movilizables, que son los componentes más inciertos. <!-- check:cifra-libre (versión 1.0) -->

#### Cambio del déficit entre 2025 y 2030

La dirección y la magnitud se separan, porque tienen capas distintas.

- **Dirección [C2].** En el recuento de provincias, {{T4-H3:num}} provincias empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} quedan indeterminadas [C2]. A escala nacional el déficit empeora en todos los escenarios de la rejilla. <!-- check:cifra-libre (rejilla de 180 escenarios, número de diseño; periodo 2025-2030) -->
- **Magnitud [C4].** El cambio central es {{T4-H2:valor}} [C4]. El rango de la rejilla es {{T4-H2:rango}} [C4].
- **Terminadas.** Para no empeorar harían falta {{T4-H6}} [C4] en 2026-2030. El escenario optimista llega a {{T4-H7:rango}} [C4]. El extremo bajo es el ritmo reciente y el alto, el máximo plausible. <!-- check:cifra-libre (periodo 2026-2030) -->

#### Dos mínimos de T4-H2

El extremo inferior del rango depende de una convención de cálculo. Hay dos versiones y se dan las dos.

| Versión | Convención | Mínimo del cambio del déficit | Capa |
|---|---|---|---|
| Publicada | Tras 2025 la cartera toma el valor de relleno del escenario, sin interpolar | {{T4-H2:min}} | [C4] |
| Alternativa | Interpolación lineal entre 2025 y el valor de relleno | {{V16-T4-H2-min-interp:valor}} | [C4] |

<!-- check:cifra-libre (años de la tabla) -->

La convención publicada hace más favorable el escenario optimista. Adelanta las terminadas del relleno a los años de 2026 a 2030 y baja el extremo inferior del déficit. La interpolación lineal sube ese extremo y hace el escenario optimista menos favorable. El valor central y la dirección no dependen de la convención. Por eso la afirmación «el déficit empeora en toda la rejilla» no cambia. La ficha T4-H2 del anexo metodológico (output/v6_2/anexo_metodologico.md) describe las dos versiones. Una réplica ciega de V16 reprodujo el valor central y el máximo, y explicó el mínimo por esta convención. <!-- check:cifra-libre (años 2025 y 2026-2030; referencia a la ficha del anexo) -->

Afirmación evaluada: «Al ritmo actual el déficit se cerrará en pocos años». Veredicto de la 1.0: NO RESPALDADA [C2]. Lo que la sostiene es la dirección, no la magnitud. Una producción sostenida muy por encima del escenario optimista, o unos hogares claramente por debajo de la proyección baja del INE, podrían cambiar la dirección. <!-- check:cifra-libre (versión 1.0) -->

#### Déficit acumulado hasta 2024

Aquí se cuenta el aumento de hogares menos las viviendas terminadas. La cuantía es una cota, porque la EPA cambió de método en 2021 y hay siete correcciones posibles del salto. <!-- check:cifra-libre (año 2021 y número de correcciones, diseño) -->

- Sin bajas del parque, 2021-2024: {{L3-DEF-2124-SINBAJAS:rango}} [C2]. <!-- check:cifra-libre (periodo 2021-2024) -->
- Sin las dos variantes que conservan el salto de la EPA: {{L3-DEF-2124-SENS:rango}} [C2].
- Con las bajas estimadas en v5.1: {{L3-DEF-2124-BAJAST1:rango}} [C4]. Es la única cifra con bajas desde v7.2. <!-- check:cifra-libre (versiones v5.1 y v7.2) -->
- Hasta 2025, sin bajas: {{L3-DEF-2125:rango}} [C4]. Las terminadas de 2025 son frágiles. <!-- check:cifra-libre (año 2025) -->

El signo lo confirman dos fuentes de hogares y dos de terminadas en todas las variantes. La cuantía es una cota. Afirmación evaluada: «Faltan cientos de miles de viviendas». Veredicto de la 1.0: PARCIALMENTE [C2]. «Cientos de miles» se cumple en todas las variantes. Una cifra puntual no es defendible. <!-- check:cifra-libre (versión 1.0; dos fuentes de hogares y dos de terminadas, diseño) -->

#### Hogares proyectados [C2]

La proyección de hogares del INE da un crecimiento 2026-2035 de {{B1-H4}} [C2] y 2026-2030 de {{B2-H3}} [C2]. Son proyecciones oficiales, no observaciones. <!-- check:cifra-libre (periodos) -->

#### Viviendas liberadas por el envejecimiento

Las viviendas que quedan libres por fallecimiento o traslado a residencia son una cifra de orden de magnitud [C4]. No se restan de la necesidad. No suman a la oferta adicional, porque la proyección de hogares ya las incluye. Se informa de ellas aparte. Su destino (venta, alquiler, herencia o uso esporádico) no tiene dato.

### V.2 Simulaciones condicionales

Una simulación aplica una medida a un modelo con supuestos y devuelve una variación. Todas las de esta sección son [C4]. En la simulación, cada medida se asocia con un cambio de precio o de esfuerzo. La simulación no mide lo que ocurriría en la realidad. Los resultados dependen de elasticidades de oferta que no se han estimado con datos de España.

Cada resultado declara su medida de precio: precio de compra o de alquiler de mercado, y esfuerzo del hogar. El horizonte es de 10 años. El ámbito son 17 comunidades autónomas. Las cifras son la mediana entre comunidades, con el rango entre comunidades. <!-- check:cifra-libre (horizonte de 10 años y 17 comunidades, números de diseño) -->

#### V71-S1 y V71-S3: rejilla de medidas

- **Vivienda pública o asequible, por cada 10.000 viviendas.** En la simulación, el alquiler de mercado varía {{V71-S1-c_vivienda_publica-alquiler-efecto_10k}} [C4]. La compra varía {{V71-S1-c_vivienda_publica-compra-efecto_10k}} [C4]. <!-- check:cifra-libre (dosis de 10.000 viviendas, diseño) -->
- **Variación acumulada a 10 años con esa medida.** En la simulación, alquiler: {{V71-S3-R6-c_vivienda_publica-alquiler-precio10a}} [C4]. Compra: {{V71-S3-R6-c_vivienda_publica-compra-precio10a}} [C4]. <!-- check:cifra-libre (horizonte de 10 años) -->
- **Robustez.** El esfuerzo baja en todas las extracciones y el precio de mercado no sube en {{V71-S3-R6-c_vivienda_publica-alquiler-robustas:num}} CCAA de 17 en alquiler y en {{V71-S3-R6-c_vivienda_publica-compra-robustas:num}} CCAA de 17 en compra. <!-- check:cifra-libre (17 CCAA, diseño) -->
- **Regulación local de turísticos.** En la simulación, alquiler a 10 años: {{V71-S3-R6-d_turisticos-alquiler-precio10a}} [C4]. Compra: {{V71-S3-R6-d_turisticos-compra-precio10a}} [C4]. Es robusta en {{V71-S3-R6-d_turisticos-alquiler-robustas:num}} CCAA de 17 en alquiler y en {{V71-S3-R6-d_turisticos-compra-robustas:num}} CCAA de 17 en compra. <!-- check:cifra-libre (horizonte de 10 años, 17 CCAA) -->
- **Ayudas a la demanda (compra).** Coste fiscal anual aproximado: {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur}} [C4]. En la simulación, cada 100 M€ anuales se asocian con una variación del precio de mercado de {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado}} [C4]. El signo es al alza. <!-- check:cifra-libre (unidad de 100 M€, diseño) -->

Lectura. Con dosis de 10.000 a 25.000 viviendas al año, la vivienda pública queda lejos de la brecha de la sección V.1. Que «resuelva» el problema depende del volumen y del desplazamiento de la construcción privada. En la simulación, la ayuda a la demanda baja el precio neto para quien la recibe y sube el de mercado. En la simulación, quien no la recibe paga más. Ese reparto por grupos es el único resultado de signo que la ficha del verificador de la 1.0 sitúa en [C2]. Las cifras de esta sección son [C4]; el C2 no se apoya en ellas. <!-- check:cifra-libre (dosis de 10.000 y 25.000 viviendas al año de la ficha V11 del verificador; versión 1.0) -->

#### Límites de la rejilla

- La ficha del anexo de V71-S3-R6 estaba incompleta: omitía supuestos de la rejilla. Tras completarlos, la réplica ciega de V16 reprodujo V71-S3-R6 al bit (decisión K19). Esa reproducción confirma el cálculo, no los supuestos. Las cifras de V71-S3-R6 son [C4] y no sostienen ningún veredicto [C2]. <!-- check:cifra-libre (identificadores V71-S3-R6 y K19) -->
- La variación de precio depende de elasticidades de oferta y de un coste unitario que son parámetros, no estimaciones.
- La rebaja de ITP o IVA de la vivienda nueva tiene su fila en la rejilla (V71-S1-f1). La afirmación sobre su incidencia en el precio que paga el comprador está NO ANALIZADA por falta de datos. <!-- check:cifra-libre (identificador V71-S1-f1) -->
- En el análisis regional de largo plazo de V7.1, las hipótesis confirmadas son {{V71-S3-largo-confirmadas:num}} de 7 pre-registradas [C4]. <!-- check:cifra-libre (versión V7.1; 7 hipótesis del diseño) -->

#### Q5 de V16

Q5 estimó la respuesta del alquiler y del valor tasado a sorpresas de política monetaria. No se cita ninguna cifra. Motivo: la primera etapa tiene el signo contrario al esperado, el placebo es comparable al resultado y la respuesta cambia de signo. Es un resultado sin señal utilizable. <!-- check:cifra-libre (identificador de hipótesis Q5) -->

### V.3 Predicción y sus límites

#### Qué se evalúa

Una predicción se compara siempre con el modelo sencillo más exigente (un autorregresivo de orden 4, AR(4)) y con el ECM v1, en la misma muestra de objetivos. Un modelo solo «predice mejor» si lo supera. Predecir bien no dice nada sobre qué mueve el precio. Ningún coeficiente, ninguna importancia ni ningún valor SHAP se lee como efecto. <!-- check:cifra-libre (nombres de modelos: AR(4), ECM v1) -->

**Estado del contraste DM-HLN.** El contraste de Diebold-Mariano con corrección de Harvey, Leybourne y Newbold (DM-HLN) es apto bajo el proceso generador de datos de V15 y no apto bajo el de V16. No se usa como prueba en este informe. <!-- check:cifra-libre (versiones V15 y V16; nombre del contraste) -->

#### Pre-registros de V15 y V16

Los resultados de V15 y V16 son un pre-registro interno sin sello de tiempo externo.

- V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (commit y fecha del pre-registro de V15) -->
- V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (commit y fecha del pre-registro de V16) -->

Las hipótesis de V15 tienen la evaluación sellada pendiente (`evaluate_v15`, fecha límite 31-12-2027). Se presentan como pendientes, nunca como confirmadas. Todo lo de esta sección es [C4]: nivel de evidencia descriptivo o exploratorio. <!-- check:cifra-libre (fecha límite de la evaluación sellada; V15) -->

#### H5 de V15: la combinación no supera al AR(4)

H5 combinaba varios modelos para predecir el valor tasado un trimestre adelante. El diseño contrastaba si la combinación supera al AR(4). No lo supera. <!-- check:cifra-libre (identificadores H5, AR(4); horizonte de un trimestre) -->

- La razón del error cuadrático medio de la combinación frente al AR(4), pre-registrada, es {{V15-H5-razon-ecm:valor}} [C4]. Una razón mayor que uno quiere decir que la combinación se equivoca más.
- Según la implementación, la razón va de {{V15-H5-razon-replica:rango}} (de la réplica ciega a la producción pre-registrada). Se cita el rango entre implementaciones, no solo la cifra pre-registrada. En las dos la razón es mayor que uno.
- No se cita un valor p: el DM-HLN no se usa como prueba (véase arriba su estado). La conclusión descansa en la razón de error.
- La STL por origen se eligió por la regla «sin datos posteriores al origen», no por su valor. Se decidió después de ver la reconciliación entre implementaciones, y así consta. <!-- check:cifra-libre (identificador STL; «mayor que uno» como umbral de la razón) -->

La evaluación sellada de V15 sigue pendiente.

#### Q10 de V16: tres series nacionales, horizonte de un trimestre

Q10 prueba un modelo más elaborado contra el AR(4) en tres series nacionales: el índice de precios, el IPC de alquiler y las compraventas. Los resultados son descriptivos. El DM-HLN no se usa como prueba (véase arriba) y el contraste de Clark-West no superó la calibración. No hay valor p. Solo se informa de la reducción puntual del error. Se usan los datos en su última edición, no en tiempo real. <!-- check:cifra-libre (identificadores Q10 y AR(4); horizonte de un trimestre) -->

| Serie | Modelo | Frente al AR(4) | Frente al ECM v1 reducido |
|---|---|---|---|
| Q10-1, precio (IPV) | MIDAS | empeora | el ECM v1 reducido también empeora frente al AR(4); MIDAS comete menos error que el ECM v1 reducido |
| Q10-2, IPC de alquiler | Nowcast | empeora | no existe ECM v1 para esta serie |
| Q10-3, compraventas | MIDAS | sin mejora fuera de 2020 | no existe ECM v1 para esta serie |

<!-- check:cifra-libre (identificadores Q10-1 a Q10-3, AR(4), ECM v1 y año 2020) -->

- **Q10-1 y Q10-2 empeoran frente al AR(4).** El modelo elaborado comete más error que el AR(4) en las dos series. Esto se mantiene al excluir 2020.
- **Q10-3 sin mejora fuera de 2020.** La mejora aparente en compraventas procede de 2020 y 2021, el periodo de caída y rebote. Al excluir 2020 desaparece. No se cita como pista.
- **ECM v1 reducido.** El ECM v1 de Q10 es una versión reducida, reproducida en el conjunto de entrenamiento sin la variable de costes. No equivale al modelo completo de la 1.0. Solo existe para el precio.
- **Cobertura.** Los intervalos conformes del 90 % quedan en torno o por debajo del nivel nominal en las tres series, tanto con el modelo elaborado como con el AR(4).

<!-- check:cifra-libre (años 2020 y 2021; ECM v1; versión 1.0; nivel nominal del 90 %) -->

Las cifras de Q10 no se citan. El motivo es que la comparación se apoya en un único criterio (el error puntual), sin contraste válido y con datos revisados. La evaluación sellada de Q10 no aplica: ninguna pregunta de V16 cumple las condiciones de `evaluate_v16`. <!-- check:cifra-libre (identificador Q10; evaluate_v16) -->

#### Qué se puede decir de la predicción

1. Un modelo más complejo no supera al AR(4) en las series nacionales probadas, salvo en una comparación que depende de un año atípico. El alcance es el agregado nacional trimestral.
2. La capacidad de predecir un trimestre adelante es limitada en precio y en alquiler.
3. Estos resultados no dicen nada sobre qué medidas bajan o suben los precios. Esa pregunta es de la sección V.2, con sus supuestos.
4. Cuando la 1.0 afirma que un modelo «predice mejor», la afirmación se limita a las tareas en que supera a la línea base más exigente. Está en el verificador (K1-V1) y tiene otro alcance: la validación sellada de v6, sobre provincias y municipios. <!-- check:cifra-libre (numeración de la lista, AR(4), versiones 1.0 y v6, ficha K1-V1) -->
