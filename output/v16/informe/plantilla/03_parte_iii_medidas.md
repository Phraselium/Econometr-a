## Parte III · Catálogo de medidas

Esta parte evalúa afirmaciones sobre ocho instrumentos de política de vivienda. No evalúa a quien los propone ni a quien los aplica. Cada ficha tiene siete apartados: mecanismo, evidencia internacional, evidencia española, nuestra estimación, coste, efectos secundarios y veredicto. <!-- check:cifra-libre (ocho instrumentos y siete apartados: estructura del catálogo) -->

### III.1 Cómo leer el catálogo

- **Qué se evalúa.** Una afirmación del tipo «el instrumento X baja el alquiler (o el precio)». Cada afirmación se formula según el **objetivo declarado** del instrumento, que se nombra en cada ficha. Una ayuda a la demanda, por ejemplo, tiene como objetivo la asequibilidad del beneficiario; su traslación al precio o a la renta se evalúa por separado.
- **Regla de umbral (la misma para todas las fichas).** El veredicto depende de tres cosas: cuántos estudios con diseño hay para ese resultado y ese objetivo, si coinciden en el signo y si se leyeron completos. Los estudios con diseño son los que usan un grupo de control, una discontinuidad, un instrumento u otro diseño que se declare. Los descriptivos no cuentan.
- **Escala de veredicto.**
  - **Eficacia probada.** Al menos dos estudios con diseño, leídos completos, con referencia de DOI verificado, que coinciden en el signo para el mismo resultado. Se dice siempre para qué resultado y en qué país.
  - **Prometedora.** Hay al menos un estudio con diseño en el sentido del objetivo, pero se leyó en resumen, o son pocos, o son de otro contexto, o discrepan en parte. Si hay dos estudios con diseño que coinciden pero no se leyeron completos, es «prometedora», no «eficacia probada».
  - **Sin evidencia.** No hay estudio con diseño que permita decir que funciona, o los estudios con diseño discrepan en el signo.
  - **Evidencia en contra.** Al menos dos estudios con diseño, leídos completos, en sentido contrario al objetivo declarado.
  - **No evaluable con los datos disponibles.** Ni la literatura ni nuestros datos permiten juzgar el instrumento en España.
- **Resultado de aplicar la regla.** Casi toda la literatura de `docs/v16/literatura/` se leyó en resumen o en versión de trabajo. Por eso ninguna ficha llega a «eficacia probada». La única «evidencia en contra» es la de III.8 (ii), corregida en V17 por decisión del autor, y descansa en un estudio leído completo en su versión definitiva (Grislain-Letrémy y Trevien, 2022, sin DOI) y otro leído completo en su versión de trabajo (Susin, 1999, publicado en 2002). Con la lectura más estricta de esta regla, que no cuenta las versiones de trabajo, sería «prometedora» en sentido contrario al objetivo. Cuando los estudios con diseño coinciden, el veredicto es «prometedora» y la ficha lo dice.
- **Regla de capa.** Todas nuestras estimaciones de V15 y V16 son [C4]. De la 1.0 entran dos cosas. Las magnitudes de los escenarios simulados son [C4]. El signo de cuatro actuaciones es [C2], dentro de la rejilla simulada: movilización de vacías y más construcción donde hay presión (signo estable); vivienda pública (signo estable no positivo: nulo si desplaza por completo a la promoción privada); ayudas a la demanda (el beneficiario paga igual o menos como grupo). Ese signo [C2] es el publicado en la 1.0, no sube ni baja de capa, vale solo dentro de la rejilla de supuestos y no es una estimación sobre España. Ningún veredicto de este catálogo se apoya en una estimación propia de capa superior a [C4]. Los veredictos que no son «no evaluable» vienen de la literatura con DOI verificado, de otros países o periodos, y no de una estimación nuestra sobre España; el signo [C2] de la rejilla se cita junto a ellos, donde corresponde, sin sustituirlos. <!-- check:cifra-libre (versión 1.0; número de actuaciones: diseño) -->
- **Literatura.** Solo entran las referencias de `docs/v16/literatura/` y `docs/v15/literatura/`, con la etiqueta de su ficha: «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o NO VERIFICADA (sin DOI localizado). Las magnitudes de los autores no están en `cifras_clave`, así que aquí se da el signo y la ficha donde está la cifra.
- **Pre-registro.** Los resultados de V15 y V16 que se citan tienen un pre-registro interno, sin sello de tiempo externo. V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. No son pre-registros depositados. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro) -->
- **Evaluación sellada.** Las hipótesis de V15 (H1 a H5) tienen la evaluación sellada pendiente (calendario en `docs/v15/preregistro_v15_adenda.md`, sección C; fecha límite 31-12-2027). `evaluate_v16` no aplica: ninguna pregunta de V16 cumple las condiciones para una evaluación sellada confirmatoria, así que V16 no tiene evaluación sellada pendiente. <!-- check:cifra-libre (números de hipótesis, sección y fecha) -->
- **Qué se cita de V15 y V16.** Solo lo que superó la revisión adversarial. H1: solo el signo. H2, Q1c, Q1b, Q6-v y Q2c no se citan con cifras. H3, Q2a y Q6-p son «no concluyentes». <!-- check:cifra-libre (identificadores de hipótesis) -->
- **Costes.** Cuando existe, el coste sale de los escenarios de la versión 7.1 (`V71-S1-*`): una simulación sobre un panel de 17 comunidades a diez años, con rangos entre comunidades. Es [C4]. No es un presupuesto. <!-- check:cifra-libre (versión 7.1, 17 comunidades y diez años: diseño de V71-S1) -->

### III.2 Zonas tensionadas y topes al alquiler

**Objetivo declarado:** contener la subida de la renta de los inquilinos en zonas con tensión de precios.

#### Mecanismo

- **Teoría.** Un precio máximo por debajo del de equilibrio crea exceso de demanda. La oferta de alquiler puede retirarse (venta, otros usos), bajar la calidad y reducir la movilidad. Con un segmento regulado y otro libre, la renta libre puede subir (desbordamiento). Fuente: ficha L1, apartado 1. <!-- check:cifra-libre (ficha L1 y apartado 1) -->
- **Generaciones.** La congelación de rentas es la primera generación. Los topes que limitan la subida entre contratos y dentro de ellos, con exenciones para obra nueva, son la segunda. La Ley 12/2023 combina un tope de actualización con zonas declaradas tensionadas y con exención de obra nueva durante un periodo. <!-- check:cifra-libre (Ley 12/2023) -->
- **Vías de salida.** La ficha L1 y el Banco de España (Documento Ocasional 2432, DOI verificado) describen el paso a alquiler de temporada y de habitaciones, con marco regulatorio más laxo. <!-- check:cifra-libre (Documento Ocasional 2432) -->

#### Evidencia internacional

- **Renta del contrato regulado.** Los estudios de segunda generación con grupo de control hallan rentas más bajas en los contratos regulados. Entre ellos: Breidenbach, Eilers y Fries (2022, Alemania, DOI verificado), con un efecto que se atenúa al cabo de un tiempo; Breuillé et al. (2025, París, NO VERIFICADA), con un efecto creciente. En la congelación de Berlín, Hahn, Kholodilin, Waltl y Fongoni (2024, DOI verificado), la caída es mayor.
- **Desbordamiento a la renta libre.** Mense, Michelsen y Kholodilin (2023, DOI verificado) hallan rentas libres al alza en Alemania. Jofre-Monseny et al. (2023, DOI verificado) hallan en Cataluña, en cambio, una caída menor en municipios vecinos no regulados. Los estudios con diseño discrepan en el signo del desbordamiento: se estima, no se supone.
- **Tercera generación, San Francisco.** Diamond, McQuade y Qian (2019, DOI verificado): baja la oferta de alquiler de los propietarios afectados y sube la renta de la ciudad.
- **Valor del inmueble.** Autor, Palmer y Pathak (2014, DOI verificado): el fin de un control estricto sube el valor, también el de viviendas nunca controladas. Ahern y Giacoletti (2022, DOI verificado, documento NBER): el tope baja el valor de venta.
- **Construcción.** Kholodilin y Voigtländer (2026, NO VERIFICADA, documento de trabajo): menos terminaciones tras el freno alemán, con pretendencias significativas en uno de los estimadores. Mense et al. (2019, DOI verificado) hallan, en cambio, más valor del suelo edificable exento. Los resultados sobre obra nueva no coinciden.
- **Revisión.** Kholodilin (2024, DOI verificado) cuenta el signo de los estudios publicados. La mayoría halla rentas controladas más bajas. La mayoría halla también peor calidad, menos movilidad y rentas no controladas más altas. Es un recuento de signos, no de tamaños, y mezcla generaciones y calidad de diseño.

#### Evidencia española

- **Ley 11/2020 de Cataluña (2020-2022).** Monràs y García-Montalvo (2023, DOI verificado) y Jofre-Monseny et al. (2023, DOI verificado), ambos con microdatos de contratos, coinciden en una renta más baja en los contratos regulados. Discrepan en la cantidad de contratos. Kholodilin, López, Rey Blanco y González Arbués (2022, DOI verificado) estudian la norma anulada. Abel, Carrer y Luque (2024, NO VERIFICADA) la estudian con anuncios. <!-- check:cifra-libre (Ley 11/2020) -->
- **Zonas de la Ley 12/2023.** Hay trabajos sobre 2024 (Pérez García, 2026, DOI verificado en DataCite, preprint; Pinto, 2026, NO VERIFICADA). Sus resultados constan en la ficha P6 de V15 y no se resumen aquí. <!-- check:cifra-libre (Ley 12/2023, ficha P6) -->
- **Banco de España.** El Documento Ocasional 2432 (DOI verificado) es descriptivo, sin identificación: documenta el paso a temporada y a habitaciones y no estima el efecto de la regulación. <!-- check:cifra-libre (Documento Ocasional 2432) -->
- **Lagunas.** No hay evaluación con identificación de la Ley 12/2023 ni medida del desplazamiento a temporada con contratos. <!-- check:cifra-libre (Ley 12/2023) -->

#### Nuestra estimación

- **H1 (V15): solo el signo.** La asociación de la zona tensionada con la renta media de los contratos nuevos, en municipios de Cataluña, es negativa con Callaway-Sant'Anna y con SDID [C4]. No se cita ninguna magnitud: el placebo temporal y las pretendencias fallan, y las cotas no la permiten. Hay anticipación por la Ley 12/2023, reversión tras la sentencia del Tribunal Constitucional sobre la norma catalana, selección de municipios y paso a contratos de temporada. La evaluación sellada está pendiente. <!-- check:cifra-libre (Ley 12/2023) -->
- **H2 (V15) y Q1c (V16).** El número de contratos y las compraventas provinciales no tienen señal que se distinga del ruido previo. No se citan con cifras.
- **Q1a y Q1b (V16): descriptivo, sin cifras.** La declaración de zona no es determinista con el criterio de precio del artículo 18, lo que limita una discontinuidad nítida en el umbral. Q1a no tiene resultado en el entrenamiento. Fuera de Cataluña, el primer inicio de zona vigente es posterior al último año de datos de alquiler del entrenamiento, y Q1b queda sin periodo posterior. Por eso Q1a y Q1b no se citan con cifras. V16 no tiene evaluación sellada para Q1b (véase III.1). <!-- check:cifra-libre (artículo 18, apartado III.1) -->
- **Ley 11/2020 en V9 (C4).** La diferencia (ATT, Callaway-Sant'Anna) en la renta media de los contratos nuevos en Cataluña es {{V9-D1b-renta-att:valor}}, con intervalo {{V9-D1b-renta-att:rango}} [C4]. No supera la robustez, así que no sostiene ningún veredicto de este catálogo. <!-- check:cifra-libre (Ley 11/2020) -->
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
| Un tope de segunda generación baja la renta del contrato regulado | **Prometedora** (solo literatura con DOI verificado; Cataluña 2020-2022, Alemania; no es una estimación nuestra) | Varios estudios con grupo de control y microdatos coinciden en el signo, pero se leyeron en resumen |
| Un tope baja la renta del conjunto del mercado | **Sin evidencia** | Los estudios con diseño discrepan en el signo del desbordamiento a la renta libre |
| Un tope mantiene la cantidad de contratos y la oferta | **Sin evidencia** | Los estudios con microdatos del mismo territorio discrepan |
| Las zonas de la Ley 12/2023 bajan el alquiler en España | **No evaluable con los datos disponibles** | Sin periodo posterior en el entrenamiento fuera de Cataluña; H1 solo en el signo, con pruebas fallidas, en [C4] | <!-- check:cifra-libre (Ley 12/2023) -->

### III.3 Bono Alquiler Joven

**Objetivo declarado:** reducir el coste del alquiler del joven que recibe la ayuda.

#### Mecanismo

Una ayuda directa al pago del alquiler reduce el coste neto del inquilino que la recibe. Si la oferta de alquiler es rígida, parte de la ayuda puede trasladarse a la renta. El tamaño depende de la elasticidad de la oferta y de que la ayuda alcance a una parte pequeña o grande del mercado.

#### Evidencia internacional

La traslación de las ayudas al alquiler en las fichas con DOI verificado de L5 (Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015; Viren, 2013; Hyslop y Rea, 2019; Eerola et al., 2026) va de parcial a muy alta según el diseño y el mercado. La dispersión es grande. La ficha L5 da las cifras de los autores. No hay un resultado único que sirva para predecir España.

#### Evidencia española

No hay evaluación del Bono Alquiler Joven ni de sus convocatorias autonómicas (ficha L5). La base de intervenciones recoge solo la norma estatal; faltan las convocatorias autonómicas y la vigencia posterior a 2025 (`docs/v16/fuentes/intervenciones.md`).

#### Nuestra estimación

- **Q7a (V16): descriptivo, sin separación entre señal y ruido.** Se compara el alquiler de los inquilinos de mercado a uno y otro lado del corte de edad del bono, antes y después de su entrada en vigor, con la ECV. La diferencia en discontinuidades del logaritmo del alquiler es {{V16-Q7-1:valor}} [C4]. Los umbrales placebo de edad dan diferencias del mismo orden: {{V16-Q7-4:rango}} [C4]. No se muestra ningún intervalo.
- **Lo que mide.** El Plan Estatal 2018-2021 ya tenía un programa para menores de 35 años. La diferencia mide un cambio de generosidad entre ese plan y el bono, no un programa nuevo. El corte legal difiere en un año del de la ECV. La potencia está en el límite. <!-- check:cifra-libre (edad de corte, plan 2018-2021) -->
- **Signo de la 1.0 [C2].** Para las ayudas a la demanda en general, la 1.0 da un signo [C2] en la rejilla simulada (véase III.8). No es una evaluación del bono.
- **Literatura sobre las ayudas al alquiler en general.** Prometedora para la asequibilidad del beneficiario, con ganancia parcial, y evidencia en contra para la del resto de inquilinos (III.8, corregido en V17). No hay evaluación del bono en concreto. <!-- check:cifra-libre (apartado III.8, versión 1.0) -->
- **Conclusión.** No se cita ninguna magnitud como efecto del bono. V16 no tiene evaluación sellada para Q7a (véase III.1). <!-- check:cifra-libre (apartado III.1) -->

#### Coste

Sin dato de coste en el repositorio. En `V71-S1-e` se simula el coste de una ayuda a la demanda en compra, no en alquiler (véase III.8). <!-- check:cifra-libre (apartado III.8) -->

#### Efectos secundarios

Traslación a la renta en mercados de oferta rígida (literatura). Efectos de umbral: una edad de corte puede crear incentivos a posponer o adelantar la solicitud. Ningún estudio español los mide.

#### Veredicto

**No evaluable con los datos disponibles.** La literatura internacional apunta a una traslación al alquiler de tamaño muy variable. En España no hay evaluación del bono, y nuestro diseño descriptivo no distingue señal de ruido. Para las ayudas a la demanda en general, véase el veredicto de III.8.

### III.4 Impuesto de transmisiones patrimoniales (ITP)

**Objetivo declarado:** abaratar el acceso a la compra (menor coste de transacción).

#### Mecanismo

Un impuesto sobre la transmisión es un coste de transacción. Si baja, se espera más compraventa y menos inmovilidad de los hogares. La incidencia entre comprador y vendedor depende de las elasticidades de oferta y demanda. En mercados con oferta rígida, parte de la bajada puede capitalizarse en el precio.

#### Evidencia internacional

Las fichas con DOI verificado de L4 coinciden en que el volumen de transacciones responde al impuesto: baja tras las subidas permanentes, se adelanta antes de las subidas y sube con las rebajas temporales (Besley, Meads y Surico, 2014, Reino Unido; Best y Kleven, 2018; Dachis, Duranton y Turner, 2012, Toronto; Fritzsche y Vandrei, 2019, Alemania; Dolls et al., 2025). La incidencia en el precio recae sobre todo en el vendedor en varios de ellos. Hilber y Lyytikäinen (2017, DOI verificado) estudian la movilidad de los hogares. Las cifras están en la ficha L4.

#### Evidencia española

No hay estudio con identificación del ITP, de las rebajas autonómicas, del adelanto de 2012 ni del IVA superreducido (ficha L4). Mora-Sanguinetti y Rubio (2014, DOI verificado) evalúan reformas con un modelo DSGE; Montalvo, Piolatto y Raya (2020, DOI verificado) tratan la evasión en transacciones. Ninguno estima el efecto de un cambio autonómico del tipo.

#### Nuestra estimación

- **Q6 (V16).** El calendario de entrenamiento tiene {{V16-Q6-cambios:num}} cambios del tipo general del ITP, que se concentran en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo. <!-- check:cifra-libre (años 2012-2013) -->
- **Q6-v (compraventas): descriptivo.** El placebo con el resultado retardado un año es de signo contrario y mayor que la estimación. No se cita ninguna cifra.
- **Q6-p (valor tasado): no concluyente.** Fue pista hasta su réplica ciega, que corrigió un error de diferencias entre años no consecutivos.
- **Escenarios de la 1.0.** Véase «Coste»: en la simulación, la rebaja del ITP y del IVA de vivienda nueva da el mismo valor de efecto sobre el precio de mercado que las ayudas a la demanda (III.8). <!-- check:cifra-libre (apartado III.8) -->

#### Coste

Coste fiscal anual aproximado de una rebaja de ITP e IVA en vivienda nueva, en la simulación: {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:valor}}, con rango entre comunidades {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:rango}} [C4]. Coste anual por punto de reducción del precio neto pagado: {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur:valor}}, rango {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur:rango}} [C4]. En la misma simulación, el precio de mercado sube en {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-efecto_100meur_mercado:valor}} por cada 100 M€ anuales, rango {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-efecto_100meur_mercado:rango}} [C4]. Es una simulación, no una estimación del ITP. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave) -->

#### Efectos secundarios

Menos recaudación autonómica. Competencia fiscal entre comunidades. Mayor movilidad de los hogares si el impuesto baja. Transmisiones en fraude (ficha L4).

#### Veredicto

**No evaluable con los datos disponibles** para España. La literatura con DOI verificado, leída en resumen, indica que el volumen responde al impuesto; no establece para España que una rebaja mejore la asequibilidad, y la incidencia en el precio queda abierta. Nuestro diseño no separa el ITP del ciclo.

### III.5 Regulación de la vivienda turística

**Objetivo declarado:** devolver vivienda al mercado residencial y contener el alquiler residencial.

#### Mecanismo

Una vivienda dedicada a estancias cortas sale del mercado residencial o no entra en él. Con demanda residencial dada, menos oferta residencial tiende a subir el alquiler. Una norma que limite la vivienda turística puede devolver vivienda al mercado residencial, o no, si la vivienda pasa a otro uso (temporada, venta, vacía) o si el cumplimiento es bajo.

#### Evidencia internacional

Las fichas con DOI verificado de L2 y P5 (entre ellas Barron, Kung y Proserpio, 2021; Robertson, Dejean y Suire, 2023, Burdeos; Chaves Fonseca, 2024, Santa Mónica; Wachsmuth y St-Hilaire, 2026) coinciden en el signo: el aumento de oferta de alquiler de corta duración se asocia con rentas residenciales más altas, y las normas reducen sobre todo los anuncios. El efecto sobre el alquiler residencial es pequeño según los autores, con algún caso nulo. En precios de compra, el signo es negativo en las normas estudiadas. Las cifras están en las fichas L2 y P5. La elasticidad del alquiler a la densidad turística, en las fichas, es de un orden de magnitud pequeño. <!-- check:cifra-libre (fichas L2 y P5) -->

#### Evidencia española

- García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020, Barcelona, DOI verificado): la actividad de Airbnb se asocia con rentas y precios de venta más altos en los barrios más expuestos.
- Benítez-Aurioles (2023) y Mozo Carollo et al. (2023) tienen DOI verificado. Casanova Ferrando (2019) y Pastor et al. (2022) son NO VERIFICADAS. Chaves Fonseca (2026, Madrid, SERIEs) tiene DOI verificado.
- Reina (2026, DOI verificado) estudia el PEUAT de Barcelona; su diseño y resultado constan en la ficha P5. <!-- check:cifra-libre (ficha P5) -->
- No hay evaluación con identificación localizada del Plan Especial de Hospedaje de Madrid, de Palma, de Baleares, de Canarias ni de la moratoria de València (ficha L2). <!-- check:cifra-libre (ficha L2) -->

#### Nuestra estimación

- **H3 (V15), Q2a (V16): no concluyentes.** La asociación entre la densidad de vivienda turística y el alquiler tiene signo positivo en los dos diseños (sección censal y provincia) [C4]. El coeficiente principal de H3 es el mínimo de su multiverso y no tiene error estándar válido. El efecto mínimo detectable de H3, {{V15-H3-mde:sig}} % por desviación típica [C4], es mayor que el coeficiente principal, {{V15-H3-beta:sig}} % por desviación típica [C4]. No concluyente no significa nulo: el diseño no distingue entre efecto pequeño y ausencia de efecto. Q2a depende de los controles y de la fecha de la exposición. Las escalas «por desviación típica» no son comparables entre diseños.
- **Q2c (V16).** No se cita: tiene signo inestable.
- **Atlas.** La vivienda turística (INE, medición experimental) se concentra: el cociente entre el percentil 90 y el 10 de su peso municipal es {{V16-ATL-DISP-VT-PCT:num}} [C4], con dato en una parte de los municipios (el resto, suprimidos). La media nacional esconde la concentración. <!-- check:cifra-libre (percentiles 90 y 10: definición del cociente) -->
- **Triangulación.** H3 y Q2a coinciden en el signo; H3 y Q2c no. Con la literatura: mismo signo, unidades no comparables. H3 (V15) está pendiente de su evaluación sellada; Q2a (V16) no tiene evaluación sellada.

#### Coste

En los escenarios de la 1.0, una regulación local de pisos turísticos se simula como un cambio de oferta residencial. No hay coste fiscal. Sin dato de coste de inspección en el repositorio.

#### Efectos secundarios

Paso a otros usos (temporada, venta, vacía). Pérdida de ingresos de propietarios y de actividad turística local. Caída del valor de los inmuebles con licencia (la literatura internacional lo recoge). Cumplimiento: las normas necesitan registro y control.

#### Veredicto

**Prometedora** en la literatura internacional: las normas reducen los anuncios y el alquiler residencial baja algo (estudios con diseño leídos en resumen). **No evaluable con los datos disponibles** en España: nuestros resultados son no concluyentes y sin identificación, y no hay evaluación con identificación de las normas españolas. Nada permite hoy decir cuánto alquiler se evita.

### III.6 Movilización de vivienda vacía

**Objetivo declarado:** que la vivienda vacía pase a alquiler o venta y aumente la oferta efectiva.

#### Mecanismo

Un impuesto o recargo sobre la vivienda vacía eleva el coste de mantenerla sin uso. Si la vivienda vacía pasa a alquiler o venta, la oferta efectiva aumenta. Hay vacancia friccional (cambio de inquilino, obra, herencia) que ningún impuesto elimina, y la vivienda vacía puede estar donde no hay demanda.

#### Evidencia internacional

Segú (2020, Francia, DOI verificado): la vacancia baja con el impuesto, también en relativo. Caracciolo y Miglino (2024), Han, Stacey y Chen (2023) y el informe de BCREA (2020) estudian el impuesto de Columbia Británica; las tres fichas son NO VERIFICADAS, y la última procede de una asociación del sector. La cifra de Segú está en la ficha L7. <!-- check:cifra-libre (ficha L7) -->

#### Evidencia española

No hay estudio con diseño sobre el recargo del IBI a la vivienda vacía (ficha L7). La base de intervenciones recoge solo el marco estatal (Ley 12/2023); no hay ordenanzas municipales verificadas (`docs/v16/fuentes/intervenciones.md`). <!-- check:cifra-libre (ficha L7, Ley 12/2023) -->

#### Nuestra estimación

- **Hecho de partida [C4].** El Censo 2021 cuenta {{V16-HEC-PARQUE-NOPRINCIPALES-2021:valor}} no principales (secundarias y vacías) [C4]. Por consumo eléctrico, hay {{V16-HEC-VACIAS-CONSUMO-2021:valor}} vacías, un {{V16-HEC-VACIAS-PCT-2021:valor}} de las viviendas familiares [C4]. Son medidas con definiciones distintas; no se suman ni se identifican con vivienda disponible.
- **Dispersión.** El cociente entre percentil 90 y percentil 10 del porcentaje municipal de viviendas vacías por consumo eléctrico es {{V16-ATL-DISP-VACIAS:num}} [C4]. La media nacional esconde que la vacancia se concentra en unos municipios. <!-- check:cifra-libre (percentiles 90 y 10: definición del cociente) -->
- **Signo de la 1.0 [C2].** En la rejilla simulada de la 1.0, la movilización de vacías donde hay presión tiene signo estable [C2]. Es el signo, no la magnitud. No es un estudio con diseño sobre España. <!-- check:cifra-libre (versión 1.0) -->
- **Escenario de la 1.0.** En la simulación de la versión 7.1, movilizar vivienda vacía se asocia con una variación del precio del alquiler de {{V71-S1-b_vacias-alquiler-efecto_10k:valor}} por cada 10.000 viviendas en 10 años (mediana entre comunidades), con rango {{V71-S1-b_vacias-alquiler-efecto_10k:rango}} [C4]. Es un escenario condicional sobre coeficientes de panel de la versión 7, no un resultado de V15 ni de V16. En compra, las cuatro actuaciones de oferta de la simulación (construcción, vacías, vivienda pública y turísticas) tienen el mismo valor: {{V71-S1-b_vacias-compra-efecto_10k:valor}}, rango {{V71-S1-b_vacias-compra-efecto_10k:rango}} [C4]. En la simulación, el precio de compra no distingue entre ellas. <!-- check:cifra-libre (versiones 7 y 7.1, 10.000 viviendas y 10 años: unidad y horizonte de la cifra de cifras_clave; cuatro actuaciones: diseño) -->
- Ninguna estimación de V15 ni de V16 cubre este instrumento.

#### Coste

Sin dato de coste en el repositorio.

#### Efectos secundarios

Recaudación adicional si el recargo se aplica. Traslado del uso de la vivienda a segunda residencia declarada o a alquiler de temporada. Costes de verificar la vacancia (el consumo eléctrico es una aproximación). Efecto desigual: la vacancia se concentra en pocos municipios.

#### Veredicto

**Prometedora** para reducir la vacancia (Segú, 2020, DOI verificado: un solo estudio con diseño, en un país). **Sin evidencia** de que reduzca el alquiler o el precio: no hay estudio con diseño sobre ese resultado. El escenario de la 1.0 da un signo estable [C2] en la rejilla y magnitudes [C4], pero una simulación no es un estudio con diseño y no cambia este veredicto. En España, no evaluable con los datos disponibles.

### III.7 Oferta pública y suelo

La ficha agrupa dos instrumentos con mecanismos distintos: más oferta libre (suelo, urbanismo, obra nueva) y vivienda pública o asequible.

**Objetivo declarado:** aumentar la oferta para contener precios y rentas.

#### Mecanismo

- **Más oferta libre.** Con demanda dada, más vivienda reduce el precio y el alquiler relativos. El tamaño depende de la elasticidad de la oferta, que depende del suelo, el planeamiento y los costes. Las cadenas de mudanzas trasladan parte del efecto a hogares de renta baja.
- **Vivienda pública.** Añade viviendas a precio regulado. Una parte puede sustituir a vivienda privada que no se construye (desplazamiento), y el efecto en el vecindario puede cambiar de signo según su renta.

#### Evidencia internacional

- **Oferta libre.** Saiz (2010), Hilber y Vermeulen (2016) y Caldera Sánchez y Johansson (2013) tienen DOI verificado y asocian la restricción de oferta con precios más altos. Asquith, Mast y Reed (2023), Mast (2023) y Bratu, Harjunen y Saarimaa (2023) tienen DOI verificado y asocian la obra nueva con rentas cercanas más bajas y con cadenas de mudanzas que llegan a hogares de renta baja. Greenaway-McGrevy y Phillips (2023), Pennington (2021) y Li (2022) son NO VERIFICADAS. Las cifras de los autores están en la ficha L3. <!-- check:cifra-libre (ficha L3) -->
- **Vivienda pública.** Sinai y Waldfogel (2005), Eriksen y Rosenthal (2010), Baum-Snow y Marion (2009), Diamond y McQuade (2019) y Koster y van Ommeren (2019) tienen DOI verificado. Los estudios de EE. UU. sobre desplazamiento hallan que parte de la vivienda subsidiada sustituye a vivienda privada. El efecto en el precio del vecindario cambia de signo según la renta del barrio (ficha L7). <!-- check:cifra-libre (ficha L7) -->

#### Evidencia española

- La única elasticidad de la oferta nueva leída es por comunidad autónoma (Taltavull de la Paz, 2014, DOI verificado, leída en resumen). No hay elasticidad municipal identificada ni evaluación de la Ley del Suelo (ficha L3). Taltavull de la Paz (2015, DOI verificado) trata los factores institucionales; Arrazola et al. (2014) es NO VERIFICADA. <!-- check:cifra-libre (ficha L3) -->
- No hay estudio con diseño sobre la vivienda protegida. El parque social español es una fracción pequeña del total y su tamaño depende de la fuente (ficha L7). Rodríguez-Fernández (2026, Funcas) es NO VERIFICADA. <!-- check:cifra-libre (ficha L7) -->

#### Nuestra estimación

- **Q4 (V16): sin hallazgo.** La asociación de la obra nueva neta con el porcentaje de Red Natura municipal es {{V16-Q4a-beta:valor}} [C4], pero la inferencia con agrupación provincial no es apta, los residuos tienen dependencia espacial y la Red Natura no es exógena (restricción de uso correlacionada con el medio rural). La interacción con el choque de demanda, Q4b, es {{V16-Q4b-beta:valor}} [C4] y su placebo de choque adelantado tiene el mismo signo y mayor tamaño. No se concluye nada sobre la elasticidad municipal.
- **Producción de vivienda.** En 2025 se terminaron {{V16-HEC-OBRA-TERMINADAS-2025:valor}} libres [C4]. Entre 2021 y 2025, las viviendas libres terminadas por hogar nuevo (ECP) son {{V16-HEC-OBRA-SOBRE-HOGARES-2125:valor}} [C4]. Son flujos, no una medida de necesidad. <!-- check:cifra-libre (años) -->
- **Signo de la 1.0 [C2], en la rejilla simulada.** Más construcción donde hay presión tiene signo estable. La vivienda pública tiene un signo estable no positivo: nulo si desplaza por completo a la promoción privada. El verificador de la 1.0 (ficha V11) da PARCIALMENTE [C2] para el esfuerzo de acceso. Para el precio de compra no hay signo [C2]: las magnitudes de la simulación son [C4]. Es el signo de una simulación, no un estudio con diseño sobre España. <!-- check:cifra-libre (versión 1.0, ficha V11) -->
- **Escenarios de la 1.0 (V7.1).** En la simulación, por cada 10.000 viviendas adicionales en 10 años: <!-- check:cifra-libre (versión 7.1, 10.000 viviendas y 10 años: unidad y horizonte de las cifras de cifras_clave) -->
  - construcción adicional: alquiler {{V71-S1-a_construccion-alquiler-efecto_10k:valor}}, rango {{V71-S1-a_construccion-alquiler-efecto_10k:rango}} [C4];
  - vivienda pública o asequible: alquiler {{V71-S1-c_vivienda_publica-alquiler-efecto_10k:valor}}, rango {{V71-S1-c_vivienda_publica-alquiler-efecto_10k:rango}} [C4];
  - en compra, el mismo valor para todas las actuaciones de oferta: {{V71-S1-c_vivienda_publica-compra-efecto_10k:valor}}, rango {{V71-S1-c_vivienda_publica-compra-efecto_10k:rango}} [C4].

  Los valores son variaciones del precio en puntos porcentuales, mediana entre comunidades. Es una simulación condicional sobre coeficientes de panel, no una estimación de V15 ni de V16. No se ha comprobado que la simulación recoja el desplazamiento de vivienda privada que documenta la literatura de EE. UU.

#### Coste

El escenario de la 1.0 no estima el coste de construir o de adquirir suelo. Sin dato de coste por vivienda en el repositorio.

#### Efectos secundarios

Desplazamiento de vivienda privada por la pública. Plazos largos (el retardo medio entre inicio y fin de obra es de {{B2-H5:valor}} [C4]). Presión sobre el medio natural y los servicios. Cambios de valor en el vecindario de una promoción.

#### Veredicto

- **Oferta libre (más suelo, más obra nueva):** **prometedora**. Las referencias con DOI verificado, leídas en resumen, asocian más oferta con rentas cercanas más bajas, y las restricciones de oferta con precios más altos. La 1.0 añade un signo estable [C2] en la rejilla simulada para más construcción donde hay presión. En España no hay estimación identificada de la elasticidad municipal, y Q4 queda sin hallazgo.
- **Vivienda pública o asequible:** **sin evidencia** en España; **no evaluable con los datos disponibles**. La literatura de EE. UU. documenta desplazamiento parcial, y el efecto en el precio depende de la renta del barrio. En la rejilla simulada de la 1.0, el signo es estable y no positivo [C2] (nulo si desplaza por completo a la promoción privada) y el veredicto de la ficha V11 es PARCIALMENTE [C2] para el esfuerzo de acceso. El precio de compra no tiene signo [C2].

### III.8 Ayudas a la demanda (compra y alquiler en general)

Incluye las ayudas a la compra (avales ICO, deducciones, planes estatales) y las ayudas al alquiler distintas del Bono Alquiler Joven, que tiene su ficha.

**Objetivos que se evalúan:** (i) la asequibilidad del beneficiario (poder pagar la compra o el alquiler), que es el objetivo declarado; y (ii) la asequibilidad general del alquiler, que depende de cuánto de la ayuda se traslada a la renta de mercado. Corregido en V17 (ERRATA.md, 2026-10-19). <!-- check:cifra-libre (versión V17, fecha de la errata) -->

#### Mecanismo

Una ayuda a la demanda aumenta la capacidad de pago. Si la oferta es rígida, el aumento de demanda sube el precio y la ayuda se capitaliza en parte en el precio o en la renta. Si la oferta responde, se construye más.

#### Evidencia internacional

Las fichas con DOI verificado de L5 (Carozzi, Hilber y Yu, 2024, Help to Buy; Berger, Turner y Zwick, 2020; Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015) apuntan a que la ayuda se capitaliza en el precio donde la oferta es rígida y, en alquiler, se traslada en parte a la renta. Krolage (2020, NO VERIFICADA) estudia la ayuda a la compra en Baviera. Las cifras están en la ficha L5. <!-- check:cifra-libre (ficha L5) -->

#### Evidencia española

No hay evaluación de los avales ICO ni de las ayudas del plan estatal (ficha L5). La base de intervenciones recoge solo el convenio de avales de 2024; las modificaciones posteriores no están comprobadas. <!-- check:cifra-libre (ficha L5) -->

#### Nuestra estimación

Ninguna estimación de V15 ni de V16 cubre este instrumento. Escenario de la 1.0, en la simulación:
- **Signo [C2].** En la rejilla simulada, el beneficiario paga igual o menos como grupo y el no beneficiario paga más (ficha D1-V1 del verificador de la 1.0, PARCIALMENTE [C2]). El signo es C2; la magnitud del traslado al precio es [C4];
- coste fiscal anual aproximado de una ayuda a la demanda en compra: {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:valor}}, rango entre comunidades {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:rango}} [C4];
- coste anual por punto de reducción del precio neto pagado por el comprador: {{V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur:valor}}, rango {{V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur:rango}} [C4];
- variación del precio de mercado por cada 100 M€ anuales: {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado:valor}}, rango {{V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado:rango}} [C4]. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

Es una simulación condicional sobre coeficientes de panel de la versión 7. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave; versión 7; versión 1.0) -->

#### Coste

Los tres valores de coste y de variación del precio anteriores. Son el coste de la simulación, no un presupuesto.

#### Efectos secundarios

Capitalización en el precio, con beneficio parcial para el vendedor. Mayor endeudamiento de los hogares beneficiarios. En el alquiler, traslado parcial a la renta. Una parte del beneficio llega a quien ya habría comprado o alquilado.

#### Veredicto

Corregido en V17 por decisión del autor (ERRATA.md, 2026-10-19; auditoría en output/v17/auditoria/filas/ayudas_demanda.md). Ningún estudio es español. <!-- check:cifra-libre (versión V17, fecha de la errata) -->

- **(i) Asequibilidad del beneficiario de las ayudas al alquiler: prometedora, con ganancia parcial.**
  - El coste neto del beneficiario es la renta menos la ayuda. Si una parte θ de la ayuda se traslada a la renta, al beneficiario le queda 1 − θ, con dos condiciones: que la calidad de la vivienda no cambie y que la ayuda dure tanto como la subida de la renta.
  - La traslación mediana ronda la mitad: {{V17-AUD-RA-AYU-TRASLACION-MEDIANA:num}} % en siete estudios con diseño de otros países, y entre {{V17-AUD-RA-AYU-TRASLACION-SENS:min_num}} % y {{V17-AUD-RA-AYU-TRASLACION-SENS:max_num}} % según qué estudios se incluyan. Los estudios van de casi nada ({{V17-AUD-RA-AYU-TRASLACION-MEDIANA:min_num}} %) a cerca del 100 % [C4, juicio experto]. Tabla completa en output/v17/auditoria/filas/ayudas_demanda.md.
  - La ganancia del beneficiario es menor donde la oferta es más rígida (Fack, 2006; Grislain-Letrémy y Trevien, 2022; Eriksen y Ross, 2015).
  - Duración: el Bono Alquiler Joven dura dos años y los contratos de la LAU, cinco. Si la subida de renta se mantiene durante el contrato, el perceptor pierde en el conjunto del contrato cuando la traslación supera el 40 % [C4, juicio experto].
  - Es «prometedora» y no «eficacia probada» por la regla de III.1: los estudios se leyeron casi todos en resumen y ninguno es español. <!-- check:cifra-libre (siete estudios; años de las referencias; LAU; duraciones de dos y cinco años; umbral del 40 % de V17-AUD-RA-AYU-BONO-DURACION; apartado III.1) -->
- **(ii) Asequibilidad general del alquiler: evidencia en contra.**
  - No es el objetivo declarado de la ayuda. Es otro resultado: el alquiler de quienes no la reciben y del conjunto de inquilinos de renta baja.
  - La ayuda se asocia con alquileres más altos también para los no beneficiarios (EE. UU. +16 %, Francia +5,5 %). Lo encuentran dos estudios con diseño leídos completos: Susin (2002, EE. UU.; versión de trabajo de 1999): +16 % para el tercil bajo en 1974-1993; y Grislain-Letrémy y Trevien (2022, Banque de France, documento de trabajo 886, Francia): +5,5 % en 2000-2016. En los dos, la subida para el conjunto de inquilinos de renta baja es del orden de la ayuda o mayor. Véase docs/v17/referencias/no_beneficiarios.md.
  - En el Reino Unido no se detecta efecto en los no perceptores (Gibbons y Manning, 2006), con poca potencia y en un recorte de la ayuda.
  - La regla de «evidencia en contra» no exige DOI; Susin lo tiene para la versión publicada, no leída, y Grislain-Letrémy y Trevien no lo tiene (véase la salvedad de III.1). <!-- check:cifra-libre (cifras de los estudios citados, tomadas de su texto completo; años y número de documento de trabajo) -->
- **Avales ICO y ayudas a la compra: sin evidencia, como estaba.** No hay evaluación española. Donde la oferta es rígida, la literatura (Carozzi, Hilber y Yu, 2024) encuentra capitalización en el precio, y la ayuda puede no mejorar el acceso. <!-- check:cifra-libre (año) -->
- **Escenario de la 1.0.** El signo [C2] de la rejilla simulada (el beneficiario paga igual o menos como grupo y el no beneficiario paga más; ficha D1-V1) coincide en signo con (i) y con (ii). La magnitud del traslado en la simulación es [C4].

### III.9 Compradores no residentes

**Objetivo declarado:** reducir la presión de la demanda de compra de no residentes sobre el precio local.

#### Mecanismo

Más demanda de compra de quien no vive en el mercado local sube el precio si la oferta es rígida. Un recargo o un límite a esa compra reduce la demanda de ese grupo. El efecto sobre el alquiler es indirecto: compra para alquilar, uso turístico o vivienda vacía.

#### Evidencia internacional

Badarinza y Ramadorai (2018, Londres), Cvijanović y Spaenjers (2021, París) y Gorback y Keys (2020, NBER) tienen DOI verificado y asocian más demanda extranjera con precios más altos. Pavlov, Somerville y Wetzel (2024) y Howell, Mughan y Singla (2024) tienen DOI verificado y estudian recargos a compradores extranjeros, con caídas de precio a corto plazo. Khan y Verstraete (2019, Banco de Canadá) tiene DOI verificado en DataCite. Sá (2016) y Pereira dos Santos y Strohmaier (2024, visados de oro) son NO VERIFICADAS. Las cifras están en la ficha L6. <!-- check:cifra-libre (ficha L6) -->

#### Evidencia española

Álvarez, Blanco y García-Posada (2020, Banco de España) es NO VERIFICADA. Lajer Baron et al. (2024, Documento Ocasional 2433) tiene DOI verificado. La ficha L6 recoge un estudio provincial sin resultado significativo y no localiza evaluación de la Ley 14/2013 ni de su supresión. <!-- check:cifra-libre (Documento Ocasional 2433, ficha L6, Ley 14/2013) -->

#### Nuestra estimación

- **Q8 (V16): descriptivo, sin estimador de efecto.** En el agregado de entrenamiento, la cuota de compras de no residentes sobre el total de transacciones es {{V16-Q8-1:valor}} en 2025T2-2026T1 y {{V16-Q8-2:valor}} en 2024T2-2025T1 [C4]. La variación entre ventanas es {{V16-Q8-3:valor}} (este año {{V16-Q8-3:min}}; la misma comparación un año antes, {{V16-Q8-3:max}}, del mismo signo) [C4]. La cuota ya bajaba antes de abril de 2025. En 2025 hubo {{V16-Q8-4:valor}} de no residentes, una cuota anual de {{V16-Q8-5:valor}} [C4]. <!-- check:cifra-libre (periodos) -->
- **Qué no permite.** La fuente no distingue comunitarios de extracomunitarios y no trae las autorizaciones de residencia por inversión. La cuota total de no residentes no identifica los visados de oro. No hay lectura sobre el fin de ese régimen. V16 no tiene evaluación sellada para Q8 (véase III.1). <!-- check:cifra-libre (apartado III.1) -->

#### Coste

El instrumento no tiene coste fiscal directo; sí una posible variación de recaudación por transmisiones. Sin dato de recaudación en el repositorio.

#### Efectos secundarios

Menor entrada de capital. Efectos sobre el mercado turístico y de segunda residencia. Dificultad de aplicación por la libre circulación de capitales dentro de la Unión Europea.

#### Veredicto

**No evaluable con los datos disponibles.** En la literatura internacional, los recargos a compradores extranjeros se asocian con caídas de precio a corto plazo; para España no hay evaluación, y nuestros datos no distinguen el grupo afectado.

### III.10 Resumen del catálogo

| Instrumento | Veredicto | Nota |
|---|---|---|
| Zonas tensionadas y topes | Prometedora para la renta del contrato regulado (solo literatura); sin evidencia para la renta del conjunto del mercado y para la cantidad de contratos; no evaluable para la Ley 12/2023 | H1: solo el signo en [C4]; ATT de V9 sobre la Ley 11/2020 en [C4], no supera la robustez | <!-- check:cifra-libre (Ley 12/2023 y Ley 11/2020) -->
| Bono Alquiler Joven | No evaluable con los datos disponibles | Q7a descriptivo |
| ITP | No evaluable con los datos disponibles | Q6-v descriptivo; Q6-p no concluyente |
| Vivienda turística | Prometedora (literatura internacional); no evaluable en España | H3 y Q2a no concluyentes |
| Movilización de vacías | Prometedora para la vacancia; sin evidencia para alquiler y precio | Un solo estudio verificado; signo estable [C2] solo en la rejilla simulada de la 1.0 |
| Oferta libre y suelo | Prometedora | Q4 sin hallazgo; signo estable [C2] en la rejilla simulada de la 1.0 para más construcción donde hay presión |
| Vivienda pública | Sin evidencia; no evaluable con los datos disponibles | Desplazamiento parcial en la literatura de EE. UU.; signo estable no positivo [C2] en la rejilla de la 1.0; PARCIALMENTE [C2] para el esfuerzo en la ficha V11; el precio de compra no tiene signo [C2] |
| Ayudas a la demanda | Ayudas al alquiler: prometedora para la asequibilidad del beneficiario, con ganancia parcial (traslación en torno a la mitad, {{V17-AUD-RA-AYU-TRASLACION-SENS:min_num}}-{{V17-AUD-RA-AYU-TRASLACION-SENS:max_num}} % según los estudios incluidos); evidencia en contra para la asequibilidad general del alquiler. Avales ICO y ayudas a la compra: sin evidencia | Ningún estudio español; corregido en V17 (ERRATA.md) | <!-- check:cifra-libre (versión V17) -->
| Compradores no residentes | No evaluable con los datos disponibles | Q8 descriptivo |

#### Qué dice la regla de capa sobre esta tabla

- Con todas nuestras estimaciones de V15 y V16 en [C4], ninguna fila se apoya en un resultado propio de capa superior. La única capa superior es el signo [C2] de la rejilla simulada de la 1.0 (vacías, construcción, vivienda pública y ayudas a la demanda): es un signo de simulación, no un estudio con diseño sobre España. Con la regla de umbral de III.1, ninguna fila alcanza «eficacia probada» ni «evidencia en contra». Las filas «prometedora» vienen de la literatura con DOI verificado, de otros países o periodos, y solo para el resultado que se indica. <!-- check:cifra-libre (apartado III.1, versión 1.0) -->
- Para ningún instrumento hay una evaluación española con identificación y diseño creíble, salvo los topes de la Ley 11/2020 de Cataluña. La validez externa de la literatura depende de la elasticidad de la oferta y de la tenencia, que en España son distintas: mucha propiedad, poco parque social y una hipoteca mayoritariamente variable hasta 2022. <!-- check:cifra-libre (Ley 11/2020) -->
- La evaluación sellada de V15 puede cambiar las filas de la tabla. V16 no tiene evaluación sellada pendiente. Hasta entonces, las hipótesis de V15 están pendientes.

### III.11 Cifras pendientes

- Magnitudes de la literatura (rangos de renta, oferta, precio y traslación): no están en `cifras_clave`. Se remite a las fichas `docs/v16/literatura/L1` a `L7` y a `docs/v15/literatura/`. Las magnitudes se dan en esas fichas, no en este informe. <!-- check:cifra-libre (fichas L1 a L7) -->
- Costes de zonas tensionadas, Bono Alquiler Joven, vivienda vacía, oferta pública y no residentes: marcados en cada ficha.

### III.12 Instrumentos del plan no cubiertos y por qué

Estos instrumentos figuran en el plan de V16 (`docs/v16/plan.md`) y no tienen ficha propia. No se evalúan: el motivo se da en cada fila.

| Instrumento | Dónde queda | Por qué no tiene ficha |
|---|---|---|
| Tope del 2 % y del 3 % a la actualización de rentas vigentes | Se trata dentro de III.2 como parte de los topes | Ninguna pregunta de V15 o V16 lo toma como tratamiento; la ficha L1 recoge topes de actualización de otros países y no localiza una evaluación española del tope aplicado a contratos vigentes | <!-- check:cifra-libre (2 % y 3 %: topes del plan; apartado III.2; ficha L1) -->
| Suspensión de desahucios y lanzamientos | Sin ficha | La ficha L7 recoge moratorias de desahucios de otro país, con amenazas a la identificación declaradas por los autores; ninguna pregunta de V16 las toma como tratamiento | <!-- check:cifra-libre (ficha L7) -->
| Incentivos fiscales al alquiler | Sin ficha | No hay ficha de literatura ni pregunta de V15 o V16 sobre ellos |
| Planes estatales como tales | Sus programas entran en III.3 (Bono Alquiler Joven) y III.8 (ayudas a la demanda) | No hay evaluación del plan en conjunto; se evalúa cada programa por separado | <!-- check:cifra-libre (apartados III.3 y III.8) -->
| Avales ICO | III.8 (ayudas a la demanda) | Sin evaluación española localizada | <!-- check:cifra-libre (apartado III.8) -->
| Fin de la golden visa | III.9 (compradores no residentes) | La fuente de Q8 no trae las autorizaciones por inversión; no hay lectura sobre el fin del régimen | <!-- check:cifra-libre (apartado III.9) -->
