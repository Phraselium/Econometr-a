## Parte III · Catálogo de medidas

Esta parte evalúa afirmaciones sobre ocho instrumentos de política de vivienda. No evalúa a quien los propone ni a quien los aplica. Cada ficha tiene siete apartados: mecanismo, evidencia internacional, evidencia española, nuestra estimación, coste, efectos secundarios y veredicto. <!-- check:cifra-libre (ocho instrumentos y siete apartados: estructura del catálogo) -->

### III.1 Cómo leer el catálogo

- **Qué se evalúa.** Una afirmación del tipo «el instrumento X baja el alquiler (o el precio)». Cada afirmación se juzga con la misma vara, sea cual sea el territorio o el momento en que se aplicó.
- **Escala de veredicto.**
  - **Eficacia probada.** Hay estudios con diseño creíble, de referencias VERIFICADAS, que coinciden en el resultado. Se dice siempre para qué resultado y en qué país.
  - **Prometedora.** Los estudios apuntan en un sentido, pero hay pocos, son de otro contexto, se leyeron en resumen o discrepan en parte.
  - **Sin evidencia.** No hay estudio con diseño que permita decir que funciona, o los estudios con diseño discrepan entre sí.
  - **Evidencia en contra.** Los estudios con diseño apuntan en sentido contrario al objetivo declarado del instrumento.
  - **No evaluable con los datos disponibles.** Ni la literatura ni nuestros datos permiten juzgar el instrumento en España.
- **Regla de capa.** Todas nuestras estimaciones (V15, V16 y los escenarios de la 1.0) son [C4]. Con todo en [C4], un veredicto de **eficacia probada** solo puede venir de la literatura verificada. Cuando aparece, la ficha lo dice: la prueba es de otros países o de otro periodo, y no una estimación nuestra sobre España. Ningún veredicto de este catálogo se apoya en una estimación propia de capa superior a [C4].
- **Literatura.** Solo entran las referencias de `docs/v16/literatura/` y `docs/v15/literatura/`, con la etiqueta de su ficha: VERIFICADA (existe en Crossref o DataCite; cuartil no verificado) o NO VERIFICADA (sin DOI localizado). Casi todo se leyó en resumen o en versión de trabajo. Las magnitudes de los autores no están en `cifras_clave`, así que aquí se da el signo y la ficha donde está la cifra.
- **Pre-registro.** Los resultados de V15 y V16 que se citan tienen un pre-registro interno, sin sello de tiempo externo. V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. No son pre-registros depositados. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro) -->
- **Evaluación sellada pendiente.** Las hipótesis de V15 (H1 a H5) tienen la evaluación sellada pendiente (calendario en `docs/v15/preregistro_v15_adenda.md`, sección C; fecha límite 31-12-2027). Las preguntas de V16 citadas también están pendientes de su evaluación sellada. <!-- check:cifra-libre (números de hipótesis, sección y fecha) -->
- **Qué se cita de V15 y V16.** Solo lo que superó la revisión adversarial. H1: solo el signo. H2, Q1c, Q6-v y Q2c no se citan con cifras. H3, Q2a y Q6-p son «no concluyentes». <!-- check:cifra-libre (identificadores de hipótesis) -->
- **Costes.** Cuando existe, el coste sale de los escenarios de la versión 7.1 (`V71-S1-*`): una simulación sobre un panel de 17 comunidades a diez años, con rangos entre comunidades. Es [C4]. No es un presupuesto. <!-- check:cifra-libre (17 comunidades y diez años: diseño de V71-S1) -->

### III.2 Zonas tensionadas y topes al alquiler

#### Mecanismo

- **Teoría.** Un precio máximo por debajo del de equilibrio crea exceso de demanda. La oferta de alquiler puede retirarse (venta, otros usos), bajar la calidad y reducir la movilidad. Con un segmento regulado y otro libre, la renta libre puede subir (desbordamiento). Fuente: ficha L1, apartado 1.
- **Generaciones.** La congelación de rentas es la primera generación. Los topes que limitan la subida entre contratos y dentro de ellos, con exenciones para obra nueva, son la segunda. La Ley 12/2023 combina un tope de actualización con zonas declaradas tensionadas y con exención de obra nueva durante un periodo.
- **Vías de salida.** La ficha L1 y el Banco de España (Documento Ocasional 2432, VERIFICADA) describen el paso a alquiler de temporada y de habitaciones, con marco regulatorio más laxo.

#### Evidencia internacional

- **Renta del contrato regulado.** Los estudios de segunda generación con grupo de control hallan rentas más bajas en los contratos regulados. Entre ellos: Breidenbach, Eilers y Fries (2022, Alemania, VERIFICADA), con un efecto que se atenúa al cabo de un tiempo; Breuillé et al. (2025, París, NO VERIFICADA), con un efecto creciente. En la congelación de Berlín, Hahn, Kholodilin, Waltl y Fongoni (2024, VERIFICADA), la caída es mayor.
- **Desbordamiento a la renta libre.** Mense, Michelsen y Kholodilin (2023, VERIFICADA) hallan rentas libres al alza en Alemania. Jofre-Monseny et al. (2023, VERIFICADA) hallan en Cataluña, en cambio, una caída menor en municipios vecinos no regulados. El signo del desbordamiento no está establecido: se estima, no se supone.
- **Tercera generación, San Francisco.** Diamond, McQuade y Qian (2019, VERIFICADA): baja la oferta de alquiler de los propietarios afectados y sube la renta de la ciudad.
- **Valor del inmueble.** Autor, Palmer y Pathak (2014, VERIFICADA): el fin de un control estricto sube el valor, también el de viviendas nunca controladas. Ahern y Giacoletti (2022, VERIFICADA, documento NBER): el tope baja el valor de venta.
- **Construcción.** Kholodilin y Voigtländer (2026, NO VERIFICADA, documento de trabajo): menos terminaciones tras el freno alemán, con pretendencias significativas en uno de los estimadores. Mense et al. (2019, VERIFICADA) hallan, en cambio, más valor del suelo edificable exento. Los resultados sobre obra nueva no coinciden.
- **Revisión.** Kholodilin (2024, VERIFICADA) cuenta el signo de los estudios publicados. La mayoría halla rentas controladas más bajas. La mayoría halla también peor calidad, menos movilidad y rentas no controladas más altas. Es un recuento de signos, no de tamaños, y mezcla generaciones y calidad de diseño.

#### Evidencia española

- **Ley 11/2020 de Cataluña (2020-2022).** Monràs y García-Montalvo (2023, VERIFICADA) y Jofre-Monseny et al. (2023, VERIFICADA), ambos con microdatos de contratos, coinciden en una renta más baja en los contratos regulados. Discrepan en la cantidad de contratos. Kholodilin, López, Rey Blanco y González Arbués (2022, VERIFICADA) estudian la norma anulada. Abel, Carrer y Luque (2024, NO VERIFICADA) la estudian con anuncios.
- **Zonas de la Ley 12/2023.** Hay trabajos sobre 2024 (Pérez García, 2026, VERIFICADA en DataCite, preprint; Pinto, 2026, NO VERIFICADA). Sus resultados constan en la ficha P6 de V15 y no se resumen aquí.
- **Banco de España.** El Documento Ocasional 2432 (VERIFICADA) es descriptivo, sin identificación: documenta el paso a temporada y a habitaciones y no estima el efecto de la regulación.
- **Lagunas.** No hay evaluación con identificación de la Ley 12/2023 ni medida del desplazamiento a temporada con contratos.

#### Nuestra estimación

- **H1 (V15): solo el signo.** La asociación de la zona tensionada con la renta media de los contratos nuevos, en municipios de Cataluña, es negativa con Callaway-Sant'Anna y con SDID [C4]. No se cita ninguna magnitud. Fallan el placebo temporal y las pretendencias. Hay anticipación por la Ley 12/2023, reversión tras la sentencia del Tribunal Constitucional sobre la norma catalana, selección de municipios y paso a contratos de temporada. La cota de Lee llega al cero. La evaluación sellada está pendiente.
- **H2 (V15) y Q1c (V16).** El número de contratos y las compraventas provinciales no tienen señal que se distinga del ruido previo. No se citan con cifras.
- **Q1a y Q1b (V16): descriptivo.** La declaración de zona no es determinista con el criterio de precio del artículo 18: entre los municipios que lo superan, la proporción declarada es {{V16-Q1-6:valor}} [C4]. Superan el criterio {{V16-Q1-7:valor}} de entrenamiento [C4]. Esto limita una discontinuidad nítida en el umbral; Q1a no tiene resultado en el entrenamiento. Fuera de Cataluña, el primer inicio de zona vigente es en {{V16-Q1-2:num}}, posterior al último año de datos de alquiler del entrenamiento [C4]. Q1b queda sin periodo posterior y pendiente de la evaluación sellada. <!-- check:cifra-libre (artículo 18, año 2024 de último dato del SERPAVI) -->
- **Triangulación.** El signo de H1 coincide con el de la literatura leída. Las unidades no son comparables. Ningún resultado sube de capa por eso.

#### Coste

No hay cifra de coste fiscal en `V71-S1-*` para este instrumento. Sin dato de coste en el repositorio.

#### Efectos secundarios

- Posible paso a alquiler de temporada o de habitaciones, y a venta. La literatura lo documenta con anuncios; ningún estudio leído lo mide con contratos.
- Posible reducción de la cantidad de contratos o de anuncios. Los estudios con microdatos del mismo territorio discrepan.
- Calidad, movilidad y construcción: signos en su mayoría negativos en la literatura, con las salvedades de arriba.
- Desbordamiento a la renta libre y a municipios vecinos, de signo incierto.

#### Veredicto

| Afirmación | Veredicto | Base |
|---|---|---|
| Un tope de segunda generación baja la renta del contrato regulado | **Eficacia probada** (solo literatura verificada; Cataluña 2020-2022, Alemania; no es una estimación nuestra) | Estudios con grupo de control y microdatos, de referencias VERIFICADAS |
| Un tope baja la renta del conjunto del mercado | **Evidencia en contra** | Recuento de signos de una revisión VERIFICADA y desbordamiento a la renta libre en varios estudios |
| Un tope mantiene la cantidad de contratos y la oferta | **Sin evidencia** | Los estudios con microdatos del mismo territorio discrepan |
| Las zonas de la Ley 12/2023 bajan el alquiler en España | **No evaluable con los datos disponibles** | Sin periodo posterior en el entrenamiento fuera de Cataluña; H1 solo en el signo, con pruebas fallidas, en [C4] |

### III.3 Bono Alquiler Joven

#### Mecanismo

Una ayuda directa al pago del alquiler reduce el coste neto del inquilino que la recibe. Si la oferta de alquiler es rígida, parte de la ayuda puede trasladarse a la renta. El tamaño depende de la elasticidad de la oferta y de que la ayuda alcance a una parte pequeña o grande del mercado.

#### Evidencia internacional

La traslación de las ayudas al alquiler en las fichas VERIFICADAS de L5 (Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015; Viren, 2013; Hyslop y Rea, 2019; Eerola et al., 2026) va de parcial a muy alta según el diseño y el mercado. La dispersión es grande. La ficha L5 da las cifras de los autores. No hay un resultado único que sirva para predecir España.

#### Evidencia española

No hay evaluación del Bono Alquiler Joven ni de sus convocatorias autonómicas (ficha L5). La base de intervenciones recoge solo la norma estatal; faltan las convocatorias autonómicas y la vigencia posterior a 2025 (`docs/v16/fuentes/intervenciones.md`).

#### Nuestra estimación

- **Q7a (V16): descriptivo, sin separación entre señal y ruido.** Se compara el alquiler de los inquilinos de mercado a uno y otro lado del corte de edad del bono, antes y después de su entrada en vigor, con la ECV. La diferencia en discontinuidades del logaritmo del alquiler es {{V16-Q7-1:valor}} [C4]. Los umbrales placebo de edad dan diferencias del mismo orden: {{V16-Q7-4:rango}} [C4]. No se muestra ningún intervalo.
- **Lo que mide.** El Plan Estatal 2018-2021 ya tenía un programa para menores de 35 años. La diferencia mide un cambio de generosidad entre ese plan y el bono, no un programa nuevo. El corte legal difiere en un año del de la ECV. La potencia está en el límite. <!-- check:cifra-libre (edad de corte, plan 2018-2021) -->
- **Conclusión.** No se cita ninguna magnitud como efecto del bono. Pendiente de la evaluación sellada.

#### Coste

Sin dato de coste en el repositorio. En `V71-S1-e` se simula el coste de una ayuda a la demanda en compra, no en alquiler (véase III.8).

#### Efectos secundarios

Traslación a la renta en mercados de oferta rígida (literatura). Efectos de umbral: una edad de corte puede crear incentivos a posponer o adelantar la solicitud. Ningún estudio español los mide.

#### Veredicto

**No evaluable con los datos disponibles.** La literatura internacional apunta a una traslación al alquiler de tamaño muy variable. En España no hay evaluación, y nuestro diseño descriptivo no distingue señal de ruido.

### III.4 Impuesto de transmisiones patrimoniales (ITP)

#### Mecanismo

Un impuesto sobre la transmisión es un coste de transacción. Si baja, se espera más compraventa y menos inmovilidad de los hogares. La incidencia entre comprador y vendedor depende de las elasticidades de oferta y demanda. En mercados con oferta rígida, parte de la bajada puede capitalizarse en el precio.

#### Evidencia internacional

Las fichas VERIFICADAS de L4 coinciden en que el volumen de transacciones responde al impuesto: baja tras las subidas permanentes, se adelanta antes de las subidas y sube con las rebajas temporales (Besley, Meads y Surico, 2014, Reino Unido; Best y Kleven, 2018; Dachis, Duranton y Turner, 2012, Toronto; Fritzsche y Vandrei, 2019, Alemania; Dolls et al., 2025). La incidencia en el precio recae sobre todo en el vendedor en varios de ellos. Hilber y Lyytikäinen (2017, VERIFICADA) estudian la movilidad de los hogares. Las cifras están en la ficha L4.

#### Evidencia española

No hay estudio con identificación del ITP, de las rebajas autonómicas, del adelanto de 2012 ni del IVA superreducido (ficha L4). Mora-Sanguinetti y Rubio (2014, VERIFICADA) evalúan reformas con un modelo DSGE; Montalvo, Piolatto y Raya (2020, VERIFICADA) tratan la evasión en transacciones. Ninguno estima el efecto de un cambio autonómico del tipo.

#### Nuestra estimación

- **Q6 (V16).** El calendario de entrenamiento tiene {{V16-Q6-cambios:num}} cambios del tipo general del ITP, que se concentran en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo. <!-- check:cifra-libre (años 2012-2013) -->
- **Q6-v (compraventas): descriptivo.** El placebo con el resultado retardado un año es de signo contrario y mayor que la estimación. No se cita ninguna cifra.
- **Q6-p (valor tasado): no concluyente.** Fue pista hasta su réplica ciega, que corrigió un error de diferencias entre años no consecutivos.
- **Escenarios de la 1.0.** Véase «Coste»: en la simulación, la rebaja del ITP y del IVA de vivienda nueva da el mismo valor de efecto sobre el precio de mercado que las ayudas a la demanda (III.8).

#### Coste

Coste fiscal anual aproximado de una rebaja de ITP e IVA en vivienda nueva, en la simulación: {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:valor}}, con rango entre comunidades {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:rango}} [C4]. Coste anual por punto de reducción del precio neto pagado: {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur:valor}}, rango {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur:rango}} [C4]. En la misma simulación, el precio de mercado sube en {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-efecto_100meur_mercado:valor}} por cada 100 M€ anuales, rango {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-efecto_100meur_mercado:rango}} [C4]. Es una simulación, no una estimación del ITP. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave) -->

#### Efectos secundarios

Menos recaudación autonómica. Competencia fiscal entre comunidades. Mayor movilidad de los hogares si el impuesto baja. Transmisiones en fraude (ficha L4).

#### Veredicto

**No evaluable con los datos disponibles** para España. La literatura verificada establece que el volumen responde al impuesto; no establece para España que una rebaja mejore la asequibilidad, y la incidencia en el precio queda abierta. Nuestro diseño no separa el ITP del ciclo.

### III.5 Regulación de la vivienda turística

#### Mecanismo

Una vivienda dedicada a estancias cortas sale del mercado residencial o no entra en él. Con demanda residencial dada, menos oferta residencial tiende a subir el alquiler. Una norma que limite la vivienda turística puede devolver vivienda al mercado residencial, o no, si la vivienda pasa a otro uso (temporada, venta, vacía) o si el cumplimiento es bajo.

#### Evidencia internacional

Las fichas VERIFICADAS de L2 y P5 (entre ellas Barron, Kung y Proserpio, 2021; Robertson, Dejean y Suire, 2023, Burdeos; Chaves Fonseca, 2024, Santa Mónica; Wachsmuth y St-Hilaire, 2026) coinciden en el signo: el aumento de oferta de alquiler de corta duración se asocia con rentas residenciales más altas, y las normas reducen sobre todo los anuncios. El efecto sobre el alquiler residencial es pequeño según los autores, con algún caso nulo. En precios de compra, el signo es negativo en las normas estudiadas. Las cifras están en las fichas L2 y P5. La elasticidad del alquiler a la densidad turística, en las fichas, es de un orden de magnitud pequeño.

#### Evidencia española

- García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020, Barcelona, VERIFICADA): la actividad de Airbnb se asocia con rentas y precios de venta más altos en los barrios más expuestos.
- Benítez-Aurioles (2023) y Mozo Carollo et al. (2023) son VERIFICADAS. Casanova Ferrando (2019) y Pastor et al. (2022) son NO VERIFICADAS. Chaves Fonseca (2026, Madrid, SERIEs) es VERIFICADA.
- Reina (2026, VERIFICADA) estudia el PEUAT de Barcelona; su diseño y resultado constan en la ficha P5.
- No hay evaluación con identificación localizada del Plan Especial de Hospedaje de Madrid, de Palma, de Baleares, de Canarias ni de la moratoria de València (ficha L2).

#### Nuestra estimación

- **H3 (V15), Q2a (V16): no concluyentes.** La asociación entre la densidad de vivienda turística y el alquiler tiene signo positivo en los dos diseños (sección censal y provincia) [C4]. El coeficiente principal de H3 es el mínimo de su multiverso y no tiene error estándar válido. El efecto mínimo detectable de H3, {{V15-H3-mde:valor}} [C4], es mayor que el coeficiente principal, {{V15-H3-beta:valor}} [C4]. No concluyente no significa nulo: el diseño no distingue entre efecto pequeño y ausencia de efecto. Q2a depende de los controles y de la fecha de la exposición. Las escalas «por desviación típica» no son comparables entre diseños.
- **Q2c (V16).** No se cita: tiene signo inestable.
- **Atlas.** La vivienda turística (INE, medición experimental) se concentra: el cociente entre el percentil 90 y el 10 de su peso municipal es {{V16-ATL-DISP-VT-PCT:valor}} [C4], con dato en una parte de los municipios (el resto, suprimidos). La media nacional esconde la concentración.
- **Triangulación.** H3 y Q2a coinciden en el signo; H3 y Q2c no. Con la literatura: mismo signo, unidades no comparables. Pendiente de la evaluación sellada.

#### Coste

En los escenarios de la 1.0, una regulación local de pisos turísticos se simula como un cambio de oferta residencial. No hay coste fiscal. Sin dato de coste de inspección en el repositorio.

#### Efectos secundarios

Paso a otros usos (temporada, venta, vacía). Pérdida de ingresos de propietarios y de actividad turística local. Caída del valor de los inmuebles con licencia (la literatura internacional lo recoge). Cumplimiento: las normas necesitan registro y control.

#### Veredicto

**Prometedora** en la literatura internacional: las normas reducen los anuncios y el alquiler residencial baja algo. **No evaluable con los datos disponibles** en España: nuestros resultados son no concluyentes y sin identificación, y no hay evaluación con identificación de las normas españolas. Nada permite hoy decir cuánto alquiler se evita.

### III.6 Movilización de vivienda vacía

#### Mecanismo

Un impuesto o recargo sobre la vivienda vacía eleva el coste de mantenerla sin uso. Si la vivienda vacía pasa a alquiler o venta, la oferta efectiva aumenta. Hay vacancia friccional (cambio de inquilino, obra, herencia) que ningún impuesto elimina, y la vivienda vacía puede estar donde no hay demanda.

#### Evidencia internacional

Segú (2020, Francia, VERIFICADA): la vacancia baja con el impuesto, también en relativo. Caracciolo y Miglino (2024), Han, Stacey y Chen (2023) y el informe de BCREA (2020) estudian el impuesto de Columbia Británica; las tres fichas son NO VERIFICADAS, y la última procede de una asociación del sector. La cifra de Segú está en la ficha L7.

#### Evidencia española

No hay estudio con diseño sobre el recargo del IBI a la vivienda vacía (ficha L7). La base de intervenciones recoge solo el marco estatal (Ley 12/2023); no hay ordenanzas municipales verificadas (`docs/v16/fuentes/intervenciones.md`).

#### Nuestra estimación

- **Hecho de partida [C4].** El Censo 2021 cuenta {{V16-HEC-PARQUE-NOPRINCIPALES-2021:valor}} no principales (secundarias y vacías) [C4]. Por consumo eléctrico, hay {{V16-HEC-VACIAS-CONSUMO-2021:valor}} vacías, un {{V16-HEC-VACIAS-PCT-2021:valor}} de las viviendas familiares [C4]. Son medidas con definiciones distintas; no se suman ni se identifican con vivienda disponible.
- **Dispersión.** El cociente entre percentil 90 y percentil 10 del porcentaje municipal de viviendas vacías por consumo eléctrico es {{V16-ATL-DISP-VACIAS:valor}} [C4]. La media nacional esconde que la vacancia se concentra en unos municipios.
- **Escenario de la 1.0.** En la simulación de la versión 7.1, movilizar vivienda vacía se asocia con una variación del precio del alquiler de {{V71-S1-b_vacias-alquiler-efecto_10k:valor}} por cada 10.000 viviendas en 10 años (mediana entre comunidades), con rango {{V71-S1-b_vacias-alquiler-efecto_10k:rango}} [C4]. Es un escenario condicional sobre coeficientes de panel de la versión 7, no un resultado de V15 ni de V16. En compra, las cuatro actuaciones de oferta de la simulación (construcción, vacías, vivienda pública y turísticas) tienen el mismo valor: {{V71-S1-b_vacias-compra-efecto_10k:valor}}, rango {{V71-S1-b_vacias-compra-efecto_10k:rango}} [C4]. En la simulación, el precio de compra no distingue entre ellas. <!-- check:cifra-libre (10.000 viviendas y 10 años: unidad y horizonte de la cifra de cifras_clave; cuatro actuaciones: diseño) -->
- Ninguna estimación de V15 ni de V16 cubre este instrumento.

#### Coste

Sin dato de coste en el repositorio.

#### Efectos secundarios

Recaudación adicional si el recargo se aplica. Traslado del uso de la vivienda a segunda residencia declarada o a alquiler de temporada. Costes de verificar la vacancia (el consumo eléctrico es una aproximación). Efecto desigual: la vacancia se concentra en pocos municipios.

#### Veredicto

**Prometedora** para reducir la vacancia (Segú, 2020, VERIFICADA: un solo estudio con diseño, en un país). **Sin evidencia** de que reduzca el alquiler o el precio: no hay estudio con diseño sobre ese resultado, y el escenario de la 1.0 es una simulación de capa [C4]. En España, no evaluable con los datos disponibles.

### III.7 Oferta pública y suelo

La ficha agrupa dos instrumentos con mecanismos distintos: más oferta libre (suelo, urbanismo, obra nueva) y vivienda pública o asequible.

#### Mecanismo

- **Más oferta libre.** Con demanda dada, más vivienda reduce el precio y el alquiler relativos. El tamaño depende de la elasticidad de la oferta, que depende del suelo, el planeamiento y los costes. Las cadenas de mudanzas trasladan parte del efecto a hogares de renta baja.
- **Vivienda pública.** Añade viviendas a precio regulado. Una parte puede sustituir a vivienda privada que no se construye (desplazamiento), y el efecto en el vecindario puede cambiar de signo según su renta.

#### Evidencia internacional

- **Oferta libre.** Saiz (2010), Hilber y Vermeulen (2016) y Caldera Sánchez y Johansson (2013) son VERIFICADAS y asocian la restricción de oferta con precios más altos. Asquith, Mast y Reed (2023), Mast (2023) y Bratu, Harjunen y Saarimaa (2023) son VERIFICADAS y asocian la obra nueva con rentas cercanas más bajas y con cadenas de mudanzas que llegan a hogares de renta baja. Greenaway-McGrevy y Phillips (2023), Pennington (2021) y Li (2022) son NO VERIFICADAS. Las cifras de los autores están en la ficha L3.
- **Vivienda pública.** Sinai y Waldfogel (2005), Eriksen y Rosenthal (2010), Baum-Snow y Marion (2009), Diamond y McQuade (2019) y Koster y van Ommeren (2019) son VERIFICADAS. Los estudios de EE. UU. sobre desplazamiento hallan que parte de la vivienda subsidiada sustituye a vivienda privada. El efecto en el precio del vecindario cambia de signo según la renta del barrio (ficha L7).

#### Evidencia española

- La única elasticidad de la oferta nueva leída es por comunidad autónoma (Taltavull de la Paz, 2014, VERIFICADA, leída en resumen). No hay elasticidad municipal identificada ni evaluación de la Ley del Suelo (ficha L3). Taltavull de la Paz (2015, VERIFICADA) trata los factores institucionales; Arrazola et al. (2014) es NO VERIFICADA.
- No hay estudio con diseño sobre la vivienda protegida. El parque social español es una fracción pequeña del total y su tamaño depende de la fuente (ficha L7). Rodríguez-Fernández (2026, Funcas) es NO VERIFICADA.

#### Nuestra estimación

- **Q4 (V16): sin hallazgo.** La asociación de la obra nueva neta con el porcentaje de Red Natura municipal es {{V16-Q4a-beta:valor}} [C4], pero la inferencia con agrupación provincial no es apta, los residuos tienen dependencia espacial y la Red Natura no es exógena (restricción de uso correlacionada con el medio rural). La interacción con el choque de demanda, Q4b, es {{V16-Q4b-beta:valor}} [C4] y su placebo de choque adelantado tiene el mismo signo y mayor tamaño. No se concluye nada sobre la elasticidad municipal.
- **Producción de vivienda.** En 2025 se terminaron {{V16-HEC-OBRA-TERMINADAS-2025:valor}} libres [C4]. Entre 2021 y 2025 se terminaron {{V16-HEC-OBRA-SOBRE-HOGARES-2125:valor}} libres por hogar nuevo [C4]. Son flujos, no una medida de necesidad. <!-- check:cifra-libre (años) -->
- **Escenarios de la 1.0 (V7.1).** En la simulación, por cada 10.000 viviendas adicionales en 10 años:
  - construcción adicional: alquiler {{V71-S1-a_construccion-alquiler-efecto_10k:valor}}, rango {{V71-S1-a_construccion-alquiler-efecto_10k:rango}} [C4];
  - vivienda pública o asequible: alquiler {{V71-S1-c_vivienda_publica-alquiler-efecto_10k:valor}}, rango {{V71-S1-c_vivienda_publica-alquiler-efecto_10k:rango}} [C4];
  - en compra, el mismo valor para todas las actuaciones de oferta: {{V71-S1-c_vivienda_publica-compra-efecto_10k:valor}}, rango {{V71-S1-c_vivienda_publica-compra-efecto_10k:rango}} [C4].
  Los valores son variaciones del precio en puntos porcentuales, mediana entre comunidades. Es una simulación condicional sobre coeficientes de panel, no una estimación de V15 ni de V16. No se ha comprobado que la simulación recoja el desplazamiento de vivienda privada que documenta la literatura de EE. UU. <!-- check:cifra-libre (10.000 viviendas, 10 años: unidad y horizonte de las cifras de cifras_clave) -->

#### Coste

El escenario de la 1.0 no estima el coste de construir o de adquirir suelo. Sin dato de coste por vivienda en el repositorio.

#### Efectos secundarios

Desplazamiento de vivienda privada por la pública. Plazos largos (el retardo medio entre inicio y fin de obra es de {{B2-H5:valor}} [C4]). Presión sobre el medio natural y los servicios. Cambios de valor en el vecindario de una promoción.

#### Veredicto

- **Oferta libre (más suelo, más obra nueva):** **prometedora**. Las referencias VERIFICADAS asocian más oferta con rentas cercanas más bajas, y las restricciones de oferta con precios más altos. En España no hay estimación identificada de la elasticidad municipal, y Q4 queda sin hallazgo.
- **Vivienda pública o asequible:** **sin evidencia** en España; **no evaluable con los datos disponibles**. La literatura de EE. UU. documenta desplazamiento parcial, y el efecto en el precio depende de la renta del barrio.

### III.8 Ayudas a la demanda (compra y alquiler en general)

Incluye las ayudas a la compra (avales ICO, deducciones, planes estatales) y las ayudas al alquiler distintas del Bono Alquiler Joven, que tiene su ficha.

#### Mecanismo

Una ayuda a la demanda aumenta la capacidad de pago. Si la oferta es rígida, el aumento de demanda sube el precio y la ayuda se capitaliza en parte en el precio o en la renta. Si la oferta responde, se construye más.

#### Evidencia internacional

Las fichas VERIFICADAS de L5 (Carozzi, Hilber y Yu, 2024, Help to Buy; Berger, Turner y Zwick, 2020; Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015) apuntan a que la ayuda se capitaliza en el precio donde la oferta es rígida y, en alquiler, se traslada en parte a la renta. Krolage (2020, NO VERIFICADA) estudia la ayuda a la compra en Baviera. Las cifras están en la ficha L5.

#### Evidencia española

No hay evaluación de los avales ICO ni de las ayudas del plan estatal (ficha L5). La base de intervenciones recoge solo el convenio de avales de 2024; las modificaciones posteriores no están comprobadas.

#### Nuestra estimación

Ninguna estimación de V15 ni de V16 cubre este instrumento. Escenario de la 1.0, en la simulación:
- coste fiscal anual aproximado de una ayuda a la demanda en compra: {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:valor}}, rango entre comunidades {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:rango}} [C4];
- coste anual por punto de reducción del precio neto pagado por el comprador: {{V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur:valor}}, rango {{V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur:rango}} [C4];
- variación del precio de mercado por cada 100 M€ anuales: {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado:valor}}, rango {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado:rango}} [C4].

Es una simulación condicional sobre coeficientes de panel de la versión 7. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave) -->

#### Coste

Los tres valores anteriores. Son el coste de la simulación, no un presupuesto.

#### Efectos secundarios

Capitalización en el precio, con beneficio parcial para el vendedor. Mayor endeudamiento de los hogares beneficiarios. En el alquiler, traslado parcial a la renta. Una parte del beneficio llega a quien ya habría comprado o alquilado.

#### Veredicto

**Evidencia en contra** de que la ayuda reduzca el precio o la renta en mercados con oferta rígida: las referencias VERIFICADAS la sitúan como capitalización parcial. Eso no afirma que el comprador no se beneficie: afirma que el precio de mercado sube. **No evaluable con los datos disponibles** en España: sin evaluación local, y nuestro escenario es una simulación [C4].

### III.9 Compradores no residentes

#### Mecanismo

Más demanda de compra de quien no vive en el mercado local sube el precio si la oferta es rígida. Un recargo o un límite a esa compra reduce la demanda de ese grupo. El efecto sobre el alquiler es indirecto: compra para alquilar, uso turístico o vivienda vacía.

#### Evidencia internacional

Badarinza y Ramadorai (2018, Londres), Cvijanović y Spaenjers (2021, París) y Gorback y Keys (2020, NBER) son VERIFICADAS y asocian más demanda extranjera con precios más altos. Pavlov, Somerville y Wetzel (2024) y Howell, Mughan y Singla (2024) son VERIFICADAS y estudian recargos a compradores extranjeros, con caídas de precio a corto plazo. Khan y Verstraete (2019, Banco de Canadá) es VERIFICADA en DataCite. Sá (2016) y Pereira dos Santos y Strohmaier (2024, visados de oro) son NO VERIFICADAS. Las cifras están en la ficha L6.

#### Evidencia española

Álvarez, Blanco y García-Posada (2020, Banco de España) es NO VERIFICADA. Lajer Baron et al. (2024, Documento Ocasional 2433) es VERIFICADA. La ficha L6 recoge un estudio provincial sin resultado significativo y no localiza evaluación de la Ley 14/2013 ni de su supresión.

#### Nuestra estimación

- **Q8 (V16): descriptivo, sin estimador de efecto.** En el agregado de entrenamiento, la cuota de compras de no residentes sobre el total de transacciones es {{V16-Q8-1:valor}} en 2025T2-2026T1 y {{V16-Q8-2:valor}} en 2024T2-2025T1 [C4]. La variación entre ventanas es {{V16-Q8-3:valor}}; la misma comparación un año antes dio una variación del mismo signo (rango {{V16-Q8-3:rango}}) [C4]. La cuota ya bajaba antes de abril de 2025. En 2025 hubo {{V16-Q8-4:valor}} de no residentes, una cuota anual de {{V16-Q8-5:valor}} [C4]. <!-- check:cifra-libre (periodos) -->
- **Qué no permite.** La fuente no distingue comunitarios de extracomunitarios y no trae las autorizaciones de residencia por inversión. La cuota total de no residentes no identifica los visados de oro. No hay lectura sobre el fin de ese régimen. Pendiente de la evaluación sellada.

#### Coste

El instrumento no tiene coste fiscal directo; sí una posible variación de recaudación por transmisiones. Sin dato de recaudación en el repositorio.

#### Efectos secundarios

Menor entrada de capital. Efectos sobre el mercado turístico y de segunda residencia. Dificultad de aplicación por la libre circulación de capitales dentro de la Unión Europea.

#### Veredicto

**No evaluable con los datos disponibles.** En la literatura internacional, los recargos a compradores extranjeros se asocian con caídas de precio a corto plazo; para España no hay evaluación, y nuestros datos no distinguen el grupo afectado.

### III.10 Resumen del catálogo

| Instrumento | Veredicto | Nota |
|---|---|---|
| Zonas tensionadas y topes | Eficacia probada para la renta del contrato regulado (solo literatura); evidencia en contra para la renta del conjunto del mercado; sin evidencia para la cantidad de contratos; no evaluable para la Ley 12/2023 | H1: solo el signo en [C4] |
| Bono Alquiler Joven | No evaluable con los datos disponibles | Q7a descriptivo |
| ITP | No evaluable con los datos disponibles | Q6-v descriptivo; Q6-p no concluyente |
| Vivienda turística | Prometedora (literatura internacional); no evaluable en España | H3 y Q2a no concluyentes |
| Movilización de vacías | Prometedora para la vacancia; sin evidencia para alquiler y precio | Un solo estudio verificado |
| Oferta libre y suelo | Prometedora | Q4 sin hallazgo |
| Vivienda pública | Sin evidencia; no evaluable con los datos disponibles | Desplazamiento parcial en la literatura de EE. UU. |
| Ayudas a la demanda | Evidencia en contra de que reduzcan el precio con oferta rígida; no evaluable en España | Escenario de la 1.0 |
| Compradores no residentes | No evaluable con los datos disponibles | Q8 descriptivo |

#### Qué dice la regla de capa sobre esta tabla

- Con todas nuestras estimaciones en [C4], ninguna fila se apoya en un resultado propio de capa superior. Cada **eficacia probada** y cada **evidencia en contra** vienen de la literatura verificada, de otros países o periodos, y solo para el resultado que se indica.
- Para ningún instrumento hay una evaluación española con identificación y diseño creíble, salvo los topes de la Ley 11/2020 de Cataluña. La validez externa de la literatura depende de la elasticidad de la oferta y de la tenencia, que en España son distintas: mucha propiedad, poco parque social y una hipoteca mayoritariamente variable hasta 2022.
- Las evaluaciones selladas de V15 y de V16 pueden cambiar las filas de la tabla. Hasta entonces, las hipótesis están pendientes.

### III.11 Cifras pendientes

- Magnitudes de la literatura (rangos de renta, oferta, precio y traslación): no están en `cifras_clave`. Se remite a las fichas `docs/v16/literatura/L1` a `L7` y a `docs/v15/literatura/`. Las magnitudes se dan en esas fichas, no en este informe.
- Costes de zonas tensionadas, Bono Alquiler Joven, vivienda vacía, oferta pública y no residentes: marcados en cada ficha.
