## Parte VI · Manual de verificación

Este manual enseña a reconocer un argumento engañoso sobre la vivienda. No sirve para decidir quién tiene razón. Sirve para comprobar si una afirmación concreta se sostiene con los datos. Las afirmaciones se formulan en abstracto: se evalúa lo que se dice, nunca quién lo dice. Las mismas reglas valen para todas.

Cada apartado tiene tres partes: cómo es el truco, cómo se comprueba y un ejemplo real evaluado por el estudio. Los ejemplos salen del verificador de la 1.0 y de los hechos de V16. Las capas son: C1 hechos con al menos dos fuentes, C2 cotas con supuestos explícitos, C3 efectos identificados y C4 exploratorio. <!-- check:cifra-libre (versión 1.0; nombres de capa) -->

### Cinco preguntas antes de creer una cifra

1. ¿Qué periodo cubre y por qué ese? <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
2. ¿Es un valor nominal o real? <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
3. ¿Mide contratos vigentes o contratos nuevos? <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
4. ¿Es una media, un índice o un caso concreto? <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
5. ¿Compara dos cosas que ocurren a la vez o muestra un efecto? <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

<!-- check:cifra-libre (numeración de la lista) -->

### VI.1 Periodos elegidos a conveniencia

**El truco.** Una misma serie da un crecimiento muy distinto según el año de inicio y el de fin. Quien elige el periodo elige el resultado.

**Cómo se comprueba.** Pide la serie entera y prueba otras ventanas. Si la conclusión cambia con el periodo, la cifra no resume la serie.

**Ejemplo.** Para los contratos nuevos de Cataluña hay dos cifras. En 2015-2025 la renta media de las fianzas sube {{A23-A4}} [C4]. En 2021-2024, con el índice del INE y esa misma fuente, sube {{A23-A9:valor}} [C1], con rango {{A23-A9:rango}}. Las dos son ciertas. Responden a preguntas distintas. Ninguna puede usarse sola para hablar de «lo que ha subido el alquiler». <!-- check:cifra-libre (periodos 2015-2025 y 2021-2024) -->

### VI.2 Nominal frente a real

**El truco.** Un valor nominal incluye la inflación. Un valor real la descuenta. Mezclarlos hace parecer que algo sube o baja más de lo que lo hace.

**Cómo se comprueba.** Mira si la cifra está deflactada y con qué índice. Compara siempre con la misma base y con la misma medida.

**Ejemplo.** Se usa una sola medida: el IPC de alquiler, que mide contratos vigentes. En 2019-2025 su cambio acumulado es {{V16-HEC-ALQ-IPC-NOMINAL-2019-2025:valor}} en términos nominales [C4] y {{V16-HEC-ALQ-IPC-REAL-2019-2025:valor}} en términos reales, con el deflactor del IPC general [C4]. Es la misma serie y el mismo periodo. Solo cambia el deflactor. Lo mismo vale para el precio de compra. Con las tres medidas por m² (MIVAU, Notariado y Registradores), el cambio 2019-2025 es {{V16-HEC-PRECIO-NOM-2019-2025}} nominal [C1] y {{V16-HEC-PRECIO-REAL-2019-2025}} real [C1]. Con otra medida, el IPV del INE ajustado por calidad, es {{V16-HEC-IPV-NOM-2019-2025:valor}} nominal y {{V16-HEC-IPV-REAL-2019-2025:valor}} real [C4]. Una cifra nominal de una medida no se compara con una cifra real de otra. <!-- check:cifra-libre (periodo 2019-2025) -->

### VI.3 Contratos vigentes frente a contratos nuevos

**El truco.** El alquiler de quien firma hoy no es el alquiler de quien firmó hace años. Los contratos vigentes se actualizan con topes y cambian poco. Los nuevos reflejan el mercado actual.

**Cómo se comprueba.** Pregunta si la cifra mide el stock de contratos o el flujo de los firmados ahora.

**Ejemplo.** La afirmación «el alquiler se ha duplicado» tiene dos versiones. Con el stock, el veredicto de la 1.0 es CONTRADICHA [C1]: ninguna fuente llega a +100 % y el rango es {{A23-A2:rango}}. Con los contratos nuevos, la subida del índice del INE es {{A23-A3:valor}} [C4]. Los contratos nuevos pesan {{A23-A7:valor}} [C4] en el índice de contratos vigentes, y por eso el stock sube más despacio. Tampoco los contratos nuevos alcanzan +100 % en el periodo, pero su cuantía nacional es de fuente única y el veredicto es ANALIZADA, NO CONCLUYENTE. <!-- check:cifra-libre (umbral de +100 %, periodo 2015-2024 y versión 1.0) -->

### VI.4 Medias frente a índices

**El truco.** Una media nacional oculta casos concretos, y una media de precios cambia cuando cambia la mezcla de viviendas, no solo el precio. Un índice de composición constante sigue las mismas viviendas.

**Cómo se comprueba.** Pregunta si es una media o un índice, y si se refiere a todos los casos o a una parte.

**Ejemplo.** Que la media no llegue a +100 % no excluye que algún municipio sí lo alcance. En Cataluña, {{A23-A13:num}} de 261 municipios con al menos 30 fianzas tiene una renta media de fianzas doble o más entre 2015 y 2025 [C4]. En la Comunitat Valenciana son {{A23-A14:num}} de 103 municipios, entre 2020 y 2025 [C4]. Un caso así no demuestra que la media sea otra. La media tampoco descarta el caso. <!-- check:cifra-libre (tamaños de muestra 261 y 103, número mínimo de fianzas y periodos) -->

### VI.5 Correlación presentada como si fuera un efecto

**El truco.** Dos cosas suben a la vez y se afirma que una produce la otra. Puede ser que ambas crezcan con la urbanización, con la costa o con el tiempo. Es una correlación presentada como si fuera un efecto.

**Cómo se comprueba.** Busca si la asociación ya existía antes de que ocurriera lo que se invoca (pretendencia). Mira si desaparece con controles. Mira si el rango de las especificaciones incluye el cero.

**Ejemplo, Q3-b de V16.** Entre las secciones censales, la subida del alquiler 2021-2024 se asocia con la cuota de extranjeros: {{V16-Q3-b-beta:sig}} (log por desviación típica) [C4]. Pero el mismo cálculo sobre 2018-2021, antes del periodo, da {{V16-Q3-b-pretendencia:sig}} [C4]. La asociación ya estaba. Es una pista descriptiva y frágil, no un efecto. Pre-registro interno sin sello de tiempo externo (etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17).

**Ejemplo, H4 de V15.** La asociación entre la población extranjera predicha y el alquiler municipal es {{V15-H4-beta:valor}} en la estimación principal [C4]. El rango del multiverso de especificaciones va de {{V15-H4-beta:min}} a {{V15-H4-beta:max}} e incluye el cero. No se puede leer como un efecto. Pre-registro interno sin sello de tiempo externo (etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17); evaluación sellada pendiente. <!-- check:cifra-libre (periodos 2018-2021 y 2021-2024; commits y fechas de los pre-registros) -->

Que un cálculo salga con el signo esperado no lo vuelve un efecto. Solo lo vuelve un diseño que supere pretendencias, placebos y sensibilidad. La 1.0 sitúa todas sus estimaciones de este tipo en C4. <!-- check:cifra-libre (versión 1.0) -->

### VI.6 Efecto base

**El truco.** Un porcentaje grande puede venir de partir de un valor muy bajo, o de comparar con un año atípico. Un rebote parece una tendencia.

**Cómo se comprueba.** Mira el nivel de partida y quita el año atípico. Si la conclusión desaparece, dependía de la base.

**Ejemplo 1, compraventas (Q10-3 de V16).** Un modelo de predicción parece mejorar al modelo sencillo en las compraventas. La mejora procede de los años 2020 y 2021, de caída y rebote. Al excluir 2020 desaparece. Por eso Q10-3 se describe como «sin mejora fuera de 2020» y no se cita como pista. <!-- check:cifra-libre (años 2020 y 2021; identificador Q10-3) -->

**Ejemplo 2, déficit acumulado.** El déficit 2021-2024 depende de cómo se trate el salto de la encuesta de hogares de 2021. Con todas las variantes, el rango sin bajas es {{L3-DEF-2124-SINBAJAS:rango}} [C2]. Sin las dos variantes que conservan el salto, es {{L3-DEF-2124-SENS:rango}} [C2]. La base de la comparación cambia el resultado, y por eso la 1.0 da una cota y no una cifra puntual. <!-- check:cifra-libre (periodo 2021-2024 y año 2021; versión 1.0) -->

### VI.7 Escala que esconde la heterogeneidad

**El truco.** Una cifra nacional puede ser cierta y no describir ningún sitio concreto. Lo que pasa en el conjunto no pasa en cada provincia o ciudad.

**Cómo se comprueba.** Pide el desglose por territorio. Mira cuántas unidades empeoran, cuántas mejoran y cuántas no se pueden decir.

**Ejemplo, déficit por provincias.** A escala nacional, el déficit 2025-2030 empeora en todos los escenarios de la rejilla [C2]. Por provincias, {{T4-H3:num}} empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} quedan indeterminadas [C2]. La dirección nacional es robusta. La provincial queda sin determinar en la mayoría de las provincias. <!-- check:cifra-libre (periodo 2025-2030 y rejilla de escenarios) -->

**Ejemplo, viviendas turísticas.** La cota nacional del alquiler que las viviendas turísticas podrían desplazar es de {{B4-v3-vut-cantidad:rango}} [C2], entre 2020 y 2024. El repositorio no tiene una cota por ciudad, así que el ejemplo se queda en la escala nacional. Una cifra nacional baja no excluye una concentración local alta. Una cifra local alta tampoco se extiende al país. <!-- check:cifra-libre (periodo 2020-2024 y supuesto de sustitución 1:1) -->

### VI.8 Anuncios frente a entregas

**El truco.** Un objetivo de viviendas anunciadas no equivale a viviendas terminadas y habitables. Entre el anuncio y la entrega hay iniciadas, retrasos, calificaciones y bajas.

**Cómo se comprueba.** Compara el objetivo con las terminadas y con la necesidad en el mismo periodo. Mira qué parte son viviendas nuevas netas y qué parte sustituye a las que salen del parque protegido.

**Ejemplo, ritmo de terminadas.** Para no empeorar el déficit 2026-2030 harían falta {{T4-H6}} [C4]. El escenario optimista llega a {{T4-H7:rango}} [C4]. El extremo bajo es el ritmo reciente y el alto, el máximo plausible. Un anuncio solo es comparable con estas cifras si está medido en viviendas terminadas por año. <!-- check:cifra-libre (periodo 2026-2030) -->

**Ejemplo, vivienda protegida.** En los escenarios ilustrativos, las viviendas que saldrían del régimen de protección en 2026-2035 son {{CC-C2-salidas-base}} [C4]. Las calificaciones definitivas nuevas son {{CC-C2-nuevas5a}} [C4] de media anual en 2021-2025. Un anuncio de viviendas protegidas tiene que restar las salidas por fin de plazo para dar el saldo. Las salidas son escenarios con supuestos, no descalificaciones observadas. <!-- check:cifra-libre (periodos 2026-2035 y 2021-2025) -->

### Verificador ampliado

Esta tabla recoge afirmaciones que el estudio permite evaluar. Usa la escala del verificador de la 1.0: RESPALDADA, PARCIALMENTE, NO RESPALDADA, CONTRADICHA, ANALIZADA, NO CONCLUYENTE y NO ANALIZADA: FALTAN DATOS. Con una capa C4, el veredicto máximo es ANALIZADA, NO CONCLUYENTE. Las afirmaciones se evalúan; las personas y los partidos no. «NO ANALIZADA: FALTAN DATOS» quiere decir que no hay datos para analizar la afirmación, no que sea falsa. Los resultados de V15 y V16 son un pre-registro interno sin sello de tiempo externo, con la evaluación sellada de V15 pendiente. <!-- check:cifra-libre (versión 1.0; identificadores V15 y V16) -->

| Afirmación | Veredicto | Capa | Cifra | Por qué |
|---|---|---|---|---|
| El alquiler se ha duplicado (contratos vigentes) | CONTRADICHA | C1 | {{A23-A2:rango}} [C1] | Ninguna fuente llega a +100 %. Las dos fuentes del núcleo coinciden. | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| El alquiler se ha duplicado (contratos nuevos) | ANALIZADA, NO CONCLUYENTE | C4 | {{A23-A3:valor}} [C4] | La cuantía nacional de contratos nuevos es de fuente única. |
| Al ritmo actual el déficit se cerrará en pocos años | NO RESPALDADA | C2 | {{T4-H3:num}} provincias empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} indeterminadas [C2] | La dirección empeora en toda la rejilla. La magnitud, {{T4-H2:rango}} [C4], es solo C4. |
| Faltan cientos de miles de viviendas | PARCIALMENTE | C2 | {{L3-DEF-2124-SINBAJAS:rango}} [C2] | Dos fuentes confirman el signo. La cuantía es una cota por la corrección de la encuesta de hogares. |
| Hacen falta X viviendas al año | ANALIZADA, NO CONCLUYENTE | C4 | {{T3-H5b}} [C4] | Rango entre supuestos, no intervalo. Las liberadas por envejecimiento no se restan. |
| La vivienda que dejan los mayores resolverá el problema | ANALIZADA, NO CONCLUYENTE | C4 | Sin cifra citable aquí | Ya están descontadas en la proyección de hogares. Su destino no tiene dato. |
| Hay una burbuja en el precio de la vivienda | ANALIZADA, NO CONCLUYENTE | C4 | {{V72-GSADF-ratios-bh:num}} series con exuberancia tras ajuste múltiple; {{V72-GSADF-ratios-p05:num}} sin ajuste [C4] | Una exuberancia estadística no identifica una burbuja. El contraste no distingue renta, tipos ni oferta. |
| La subida de alquileres es atribuible a las viviendas turísticas | ANALIZADA, NO CONCLUYENTE | C4 | {{B4-v3-vut-cantidad:rango}} [C2] (cota de cantidad) | La cota de cantidad limita el desplazamiento nacional. El paso a precio depende de una elasticidad no verificada. |
| Los compradores no residentes encarecen la vivienda | ANALIZADA, NO CONCLUYENTE | C4 | Peso de no residentes en las compraventas de 2025 (R1A-H1): {{R1A-H1:valor}} [C4] | Hay un peso descriptivo. Asociación bivariada con el precio 2015-2025 (R1A-H4): {{R1A-H4:valor}}, rango {{R1A-H4:rango}} [C4]. Con controles (R1A-H5): {{R1A-H5:valor}}, rango {{R1A-H5:rango}}, que incluye cero [C4]. |
| La población extranjera se asocia con subidas del alquiler municipal | ANALIZADA, NO CONCLUYENTE | C4 | {{V15-H4-beta:valor}} en la estimación principal [C4] | Correlación frágil: el rango del multiverso, de {{V15-H4-beta:min}} a {{V15-H4-beta:max}}, incluye cero. Evaluación sellada de V15 pendiente. |
| La vivienda pública resolvería el problema | ANALIZADA, NO CONCLUYENTE | C4 | En la simulación, precio de compra a 10 años: {{V71-S3-R6-c_vivienda_publica-compra-precio10a}} [C4] | Las cifras de la simulación son C4. «Resolver» depende del volumen y del desplazamiento. En la rejilla simulada de la 1.0, el signo para el esfuerzo es débil [C2] (no positivo o nulo si desplaza a la promoción privada), y la ficha V11 del verificador la sitúa en PARCIALMENTE [C2] para el esfuerzo de acceso. El precio de compra no tiene signo [C2]. | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| Las ayudas a la demanda abaratan el acceso | PARCIALMENTE | C2 | En la simulación, {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado}} por 100 M€ en el precio de mercado [C4] | El beneficiario paga igual o menos (C2, ficha del verificador de la 1.0). En la simulación, parte de la ayuda llega al precio. | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| La rebaja del ITP o del IVA abarata la compra | NO ANALIZADA: FALTAN DATOS | C4 | — | Falta una serie armonizada de tipos. La incidencia depende de la elasticidad de oferta. |
| Las empresas y fondos dominan el alquiler | ANALIZADA, NO CONCLUYENTE | C4 | {{CB-C6-05:rango}} [C4] (residuo de personas jurídicas, sector público y no declarado) | Los dos métodos discrepan. Ninguno llega al 50 %, pero no miden el peso por zonas. | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| Los modelos más complejos predicen mejor que uno sencillo | ANALIZADA, NO CONCLUYENTE | C4 | {{V15-H5-razon-ecm:valor}} [C4] pre-registrada, razón de error frente al AR(4); entre implementaciones, {{V15-H5-razon-replica:rango}} | Alcance: agregado nacional trimestral. Una razón mayor que uno es peor. La combinación no supera al AR(4). Q10-1 y Q10-2 empeoran y Q10-3 no mejora fuera de 2020. La validación sellada de v6 ({{K1-N-MEJOR:num}} de {{K1-N-MEJOR:cobertura}}) tenía otro alcance (provincias y municipios) y no se traslada aquí. El DM-HLN es apto bajo el proceso generador de V15 y no apto bajo el de V16: no se usa como prueba. | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

<!-- check:cifra-libre (identificadores de hipótesis R1A, V11 y Q10; umbrales de +100 % y 50 %; 2020; 2025; AR(4); 9 tareas del diseño; v6; DM-HLN) -->

#### Cómo se lee la tabla

- Un veredicto ANALIZADA, NO CONCLUYENTE no quiere decir que la afirmación sea falsa. Quiere decir que los datos disponibles no bastan para sostenerla ni para negarla.
- En la 1.0, los veredictos CONTRADICHA y NO RESPALDADA descansan en capas C1 y C2. Con una capa C4 no se llega a ninguno de los dos.
- Una cifra en C4 informa del orden de magnitud. No es una medición de un efecto.
- Las simulaciones muestran qué se asocia con qué bajo los supuestos del modelo. No dicen qué ocurriría.
- Compradores: «no residentes» no equivale a «extranjeros» (nacionalidad). La cifra de R1A-H1 es de no residentes, de la tabla 1.6 del Boletín del MIVAU, para España en el año 2025. La cuota anual de no residentes de Q8, {{V16-Q8-5:valor}} [C4], viene de otra tabla del mismo Boletín, de un agregado de entrenamiento (9 CCAA más Ceuta y Melilla). Las dos fuentes, el ámbito y la ventana difieren, y por eso las cuantías difieren. Se dan ambas. <!-- check:cifra-libre (tabla 1.6; 9 CCAA del agregado de entrenamiento; identificadores R1A-H1 y Q8) -->
- Cuando el estudio no tiene datos, lo declara. No rellena el hueco.

<!-- check:cifra-libre (referencias a capas y veredictos; versión 1.0) -->
