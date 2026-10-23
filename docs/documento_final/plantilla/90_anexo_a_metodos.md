## Anexo A. Métodos

### A.1 Diseños por factor

| Factor | Diseños (identificadores del plan) | Estimación propia designada para la magnitud preferida |
|---|---|---|
| E1 Vivienda turística | Estudio de eventos de dosis con el registro HUT (R3); diferencias en diferencias radio-anillo en torno a la Sagrada Família (R4); IV de tipo shift-share con atractivos y búsquedas de Google (R2, A1) | E1-A1 (respaldo E1-R2) |
| E2 Topes al alquiler | Diferencias en diferencias con la Ley 11/2020 sobre renta y número de contratos de Incasòl (R1, R1c); zonas tensionadas de 2024 y otras comunidades (A1, A2); desbordamiento y desplazamiento (A3, A4) | E2-R1 (respaldo E2-A1) |
| E3 Inmigración | IV por asentamientos históricos de cada nacionalidad en provincias (R1, R2, A1 a A5) | E3-R2 (respaldo E3-A1) |
| E4 Ayudas a la demanda | Incidencia de las ayudas con microdatos de perceptores (X1) | ninguna (solo literatura) |
| E5 Oferta y suelo | Bartik de empleo por ramas para la elasticidad de la oferta (R1); interacción con el suelo (A1) | E5-R1 |
| E6 Obra nueva | Diferencias en diferencias por distancia a edificios nuevos (R1, A1); IV con lluvia como en Mense (R2) | E6-R2 |
| E7 Tipos de interés | Proyección local con instrumento (R1); SVAR con proxy (R2); BVAR recursivo, réplica de San Juan (R3, A1); panel provincial con exposición hipotecaria (A2) | E7-R1 (respaldo E7-R2) |
| E8 Fiscalidad de la compra | Diferencias en diferencias de dosis continua del tipo general del ITP (R1 precio, R2 volumen, A2 municipal) | E8-R1 (precio), E8-R2 (volumen) |
| E9 No residentes | Shift-share por riesgo en el país de origen (R1, R2, A1, A2) | E9-R2 |
| E10 a E12 | Asociación transversal (E10); calendario de recargos (E11); IV provincial con vivienda protegida (E12) | ninguna |
| F1 a F3 | Corrección del error, DOLS y PMG, CS-ARDL en panel; modelo de alquiler y de oferta | ninguna |

### A.2 Inferencia

Se publica siempre la inferencia convencional que corresponde a cada diseño. Los errores típicos se agrupan al nivel del tratamiento. Con pocos clusters se usa el wild cluster bootstrap con pesos de Webb. En shift-share se usan los intervalos de Anderson-Rubin y el F efectivo de Montiel Olea y Pflueger, con el número efectivo de choques (inverso del índice de Herfindahl de los pesos, de Borusyak, Hull y Jaravel) calculado antes de estimar. También se usan Conley en datos espaciales, Driscoll-Kraay en paneles con dependencia transversal y Newey-West en series. Cuando el número de clusters es muy pequeño (las comunidades autónomas de E8), la inferencia por aleatorización del calendario sustituye a Webb.

Cada herramienta se valida antes por Monte Carlo con procesos generadores que reproducen la estructura de los diseños (anexo A.15). Un resultado «apto» tiene tamaño y cobertura dentro de las bandas de la adenda 1.12; el anexo A.15 da también el criterio, más amplio, del encargo del Monte Carlo y dice cuál decide. «Con valor crítico corregido» obliga a publicar el p-valor con el valor crítico calibrado en la simulación. «No fiable» se publica con esa etiqueta y la clasificación no puede apoyarse en él. Las herramientas NO APTAS (por ejemplo, la proyección local con Newey-West, el SVAR con proxy, el BVAR y el metaanálisis bayesiano) se publican con esa etiqueta y su resultado se lee como informativo.

### A.3 Clasificación V18

La clase se asigna con las reglas del plan (B3 y criterios I1 a I8, revisados en la adenda 1.2), sin elegirla por el p-valor:

- **IDENTIFICADO.** Diseño creíble, primera etapa fuerte o intervalo de Anderson-Rubin acotado, pretendencias y placebos superados, robustez, significación tras Holm, réplica ciega coincidente y ningún tope de la especificación. Ninguna estimación de V18 llega a esta clase.
- **SUGESTIVO.** Diseño creíble y réplica ciega coincidente, sin fallo decisivo, con alguna prueba débil o un tope fijado en la adenda. Se dice «la evidencia sugiere», con la limitación concreta.
- **NO CONCLUYENTE (sin potencia).** Diseño válido sin significación y sin equivalencia demostrada por la prueba TOST.
- **ASOCIACIÓN.** Diseño no creíble o fallo decisivo de la lista del plan: F efectivo menor que 5 con Anderson-Rubin no informativo; pretendencias con p < 0,01 o M̄ de ruptura < 0,5; placebo de fecha significativo al 5 %, del mismo signo y de al menos la mitad del efecto; cambio de signo en una prueba B4; inferencia «no fiable» sin alternativa apta. Además (K7), un coeficiente no significativo que no supera los criterios de diseño (I1 a I5) es ASOCIACIÓN: por ejemplo, con un placebo de fecha significativo de cualquier signo, que indica que el diseño no es creíble para ese resultado (es el caso de E2-R1c).
- **NO ESTIMABLE.** Falta un dato imprescindible o la comprobación previa de variación no alcanza el mínimo. Esta comprobación se aplica antes que la clasificación.

Tres lecturas decididas antes de difundir resultados (docs/v18/decisiones.md). Un cambio de signo en una prueba de robustez del plan es un fallo decisivo y no se compensa con un tope (K7). Un coeficiente no significativo es NO CONCLUYENTE si supera los criterios de diseño y ASOCIACIÓN si no los supera (K7). Cuando la ficha admite dos lecturas con clases distintas se toma la más prudente (K8 bis). La etiqueta de coherencia con la literatura (I6) se publica, pero no interviene en la clase ni en la entrada en la magnitud preferida.

Réplica ciega (I8). El plan no clasifica un resultado sin réplica ciega coincidente. Se hizo para E2-R1, E8-R1 y E1-R4 (orden de la fase 4). Las clases de las demás estimaciones con cifra (entre ellas E1-R3, E3-R1, las de E7, E10, E12 y la familia F) son provisionales hasta I8, como dicen sus resultado.json; la réplica solo podría bajarlas o dejarlas sin clase.

Cifras sin clase propia (K12 y K14). Cada cifra lleva la clase de su propia especificación, no la del estudio. Cuatro valores marcan las cifras que no tienen clase propia: «sin clasificar (coprincipal informativa)» para la coprincipal que el plan no clasifica (E1-P-H3); «robustez a posteriori» para las pruebas añadidas tras ver el resultado (B6); «diagnóstico o variante (sin clase propia)» para los diagnósticos, las variantes enumeradas y las pruebas de una estimación, incluidas las cifras auxiliares que el documento cita de su salida de origen; y «literatura (sin clase propia)» para los valores publicados por la literatura y sus reproducciones (ids V18-AUX-LIT-* y V18-AUX-REP-*), porque la clase V18 es de un factor o de una estimación propia, no de un valor publicado. Las filas de magnitud preferida (V18-B5) llevan la clase de la estimación propia designada del factor, no la de la magnitud ni la del rango.

Capa y lenguaje (K2). Toda cifra V18 es de capa C4, con nivel de evidencia EXPLORATORIO. La clase V18 va en un campo propio al lado de la capa y no la promueve. Cada cifra se lee como asociación condicionada al diseño. La fórmula condicional prevista para la clase IDENTIFICADO solo cabría en los anexos técnicos, y no se ha necesitado.

### A.4 Estimabilidad previa por magnitud mínima detectable

Antes de estimar cada especificación principal, y sin mirar su resultado, se calcula por Monte Carlo la magnitud mínima detectable (MDE) con la potencia convencional fijada en la adenda 1.3. El cálculo usa la variación real del tratamiento, de la exposición o del instrumento y la dispersión residual de V15 o V16 (declarada «ya vista») o la del periodo previo. La especificación es estimable si el MDE no supera la magnitud de referencia de la literatura convertida a nuestra unidad. Si no, es NO ESTIMABLE por variación y se publica el MDE, no el coeficiente. Además se exigen mínimos de datos (por ejemplo, un número mínimo de municipios tratados y de control) y, en shift-share, un número efectivo de choques suficiente. Esta comprobación explica la mayoría de los NO ESTIMABLE.

### A.5 Magnitud preferida (B5, adenda 1.9)

- **Qué entra.** La estimación propia designada de cada factor, si su diseño es válido y es IDENTIFICADO, SUGESTIVO o NO CONCLUYENTE, con independencia de su p-valor. No entran las ASOCIACIÓN ni las NO ESTIMABLE. Los estudios de la literatura entran si están en la misma unidad y tienen error típico.
- **Episodios compartidos.** Si una estimación propia y un estudio miden el mismo episodio con la misma fuente, el episodio cuenta una vez, combinado con una correlación modelada fijada en la adenda.
- **Modelo.** Metaanálisis bayesiano de efectos aleatorios con tres priors sobre el efecto medio. La magnitud preferida se publica solo si la decisión (signo e inclusión del cero) coincide en las tres. Si no, se publica el rango de las tres sin magnitud preferida. Si la heterogeneidad es alta y el intervalo de predicción cambia de signo, tampoco hay magnitud preferida. Con un solo estudio se publica su magnitud; con dos, el efecto fijo ponderado por precisión. Si las unidades no son comparables, no se combinan.
- **Advertencia de la simulación.** El metaanálisis bayesiano resultó NO APTO por conservador: sus intervalos cubren de más y, con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera. Los intervalos con más de dos estudios son prudentes y los de dos estudios no deben leerse como IC95 fiables.
- **Referencias.** Toda referencia lleva el estado de su ficha: VERIFICADA (DOI comprobado con Crossref o DataCite; cuartil no verificado), NO VERIFICADA o DISCREPANTE (la ficha describe una versión de trabajo y el DOI corresponde a la versión publicada; se trata como NO VERIFICADA).
- **Confianza de la tabla de magnitudes.** Regla fija: «media» solo con magnitud preferida de tres o más estudios; «muy baja» si la literatura no tiene error típico en la unidad; «baja» en el resto. Nunca «alta», porque toda cifra es C4. La clasificación de cada fila es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura. Con un estudio, el intervalo es el IC95 de ese estudio; con dos, el del efecto fijo, que no es un IC95 fiable.

### A.6 Contabilidad de la subida (adenda 1.10)

La diferencia asociada a un factor en la contabilidad es su magnitud preferida por su variación observada en el periodo y el territorio, con la incertidumbre propagada por Monte Carlo sobre la magnitud y una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural ni una atribución: no hay interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Reglas:

- Un factor sin magnitud dice «sin magnitud», no cero.
- Cada diferencia asociada que procede de un diseño de panel con efectos de periodo se rotula «relativa entre provincias (o unidades), sin el componente común». Solo los tipos (E7, series nacionales) incluyen el componente común. Por eso, en la regla del Documento de Trabajo V18, las filas relativas no se restan de la variación nacional. El documento final solo lo hace en la versión 2 de la cuenta (parte V.4), como supuesto de juicio experto escrito, con la fila «no explicado» que K14 (N4) había retirado y K15 recupera rotulada.
- Cada fila dice si la variación observada del factor está dentro o fuera del soporte de la muestra de estimación. Fuera del soporte no lleva cifra.
- Inmigración (E3) y no residentes (E9) usan cuotas del padrón por nacionalidad y no se suman: E9 va como alternativa de E3.
- **Lectura restrictiva aplicada.** La adenda admite todo factor con magnitud preferida construida con las reglas de B5. El plan deja las magnitudes «solo literatura» en una tabla secundaria rotulada, y una magnitud sin estimación propia no tiene clase que limite la confianza. Se aplicó la lectura restrictiva (K10): la tabla principal solo admite factores con estimación propia dentro de B5. Ninguno la cumple. Las magnitudes de la literatura van en una tabla aparte, rotulada ilustración en V18 y «juicio experto con magnitudes de la literatura, no estimación propia» en el documento final (parte V.4, versión 2). La lectura inclusiva solo cambiaría de tabla a E1, E4 y E6, y no cambiaría ninguna conclusión.
- La variación observada usa el deflactor del PIB del INE, no el IPC general que usó V8. Las variaciones observadas difieren por eso de las de V8.
- Las viviendas liberadas por envejecimiento nunca se restan de la necesidad (la proyección de hogares del INE ya las descuenta).

### A.7 Modelos de conjunto (F)

El modelo de precio de largo plazo con corrección del error, el de alquiler y el de oferta se contrastan primero para cointegración, con corrección por pruebas múltiples. Si el contraste no rechaza la ausencia de cointegración, no se publican elasticidades de largo plazo ni sobrevaloración (regla AD-F), y solo se publica la dinámica de corto plazo como ASOCIACIÓN, cuando su estimador no supone la cointegración (por eso no se publican los coeficientes de corto plazo del PMG; anexo B.11). El modelo de precio se evalúa además fuera de muestra en la misma muestra que el AR(4) y el ECM v1, en bloques con embargo; solo «predice mejor» si supera a la línea base más exigente (K1 de v6.1).

### A.8 Evaluación sellada diferida

La vía a la capa C3 es una evaluación sellada diferida (evaluate_v18) con datos posteriores al tope de entrenamiento, una sola evaluación por hipótesis y un criterio de superación fijado en la adenda 1.11. No se ejecuta dentro de V18, requiere orden expresa del autor y no puede abrirse antes de 2027. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015 a 2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.

### A.9 Multiplicidad y registro

Toda especificación, incluidas las variantes y las fallidas, se registra antes de leer su resultado. Se controlan los falsos descubrimientos con Holm dentro de la familia de cada factor y con Benjamini-Yekutieli entre las variantes enumeradas de cada identificador. Ningún modelo se elige por su p-valor. SEED 20261010 en todo lo aleatorio.


**Regla general.** Toda cifra del documento procede de output/v5/cifras_clave.csv con su id (V18-*, V17-* y anteriores), su fuente, su capa y, en las cifras V18, su clasificación. El generador redondea los valores: dos decimales para los menores que la unidad en valor absoluto, un decimal para los intermedios y enteros para los recuentos y las cifras grandes. Los coeficientes pequeños se muestran con tres cifras significativas; los límites de sus intervalos, redondeados como se acaba de decir (los valores completos están en tablas_v18.xlsx, pestaña «estimaciones»).

### A.10 Fuentes por factor

| Factor | Fuentes principales | Periodo y nivel |
|---|---|---|
| E1 Vivienda turística | Registro de viviendas de uso turístico (HUT) del Ajuntament de Barcelona con coordenadas por licencia; SERPAVI (alquiler mediano por sección); Censo 2021; INE de viviendas turísticas por sección; OpenStreetMap (atractivos); Google Trends; Eurostat (noches por NUTS 3) | Barcelona por sección y barrio, 2011-2024; otras cuatro ciudades por sección, 2021-2024 |
| E2 Topes al alquiler | Incasòl, registro de fianzas (renta media y número de contratos por municipio); paro registrado mensual del SEPE por municipio; padrón; Censo 2021; BOE y DOGC | Municipios de Cataluña, trimestral desde 2019T1 y anual desde 2007 |
| E3 Inmigración | Padrón por nacionalidad (stock a 1 de enero); Censo de 2001 por nacionalidad (Eurostat); entradas por nacionalidad (INE y Eurostat); valor tasado del MIVAU; IPVA; SERPAVI | Provincias, 2002-2022 |
| E4 Ayudas a la demanda | Calendario estatal del Bono Alquiler Joven (RD 42/2022); Encuesta de Condiciones de Vida | Sin microdatos de perceptores |
| E5 Oferta y suelo | Viviendas iniciadas y terminadas (MIVAU); valor tasado; empleo por rama (Eurostat e INE, NUTS 3); deflactor | Provincias, 2002-2023 |
| E6 Obra nueva | Catastro INSPIRE de los municipios de la provincia de València que lo publican; SERPAVI por sección | Secciones de la provincia de València, 2011-2024 |
| E7 Tipos de interés | Tipos hipotecarios y euríbor (Banco de España); sorpresas monetarias de alta frecuencia (Jarociński y Karadi); valor tasado; IPV; IPC de alquiler; compraventas; visados | Nacional, 1999-2026; panel provincial |
| E8 Fiscalidad de la compra | Tipo general del ITP por comunidad (memorias de Hacienda, base de intervenciones de V16); valor tasado provincial; compraventas mensuales | Comunidades de régimen común no selladas, desde 2010 |
| E9 No residentes | Padrón por nacionalidad de 2003; series de riesgo en origen (PIB, precios de la vivienda: Eurostat y OCDE); cuota de compras de no residentes (MIVAU) | Provincias y países de origen |
| E10 Grandes tenedores | Estadística de titularidad del Catastro (tres cortes, 2024-2026); alquiler municipal por m² | Municipios |
| E11 Viviendas vacías | Censos de 2011 y 2021 (este último por consumo eléctrico) | Dos cortes con métodos distintos |
| E12 Vivienda pública | Calificaciones definitivas de vivienda protegida (MIVAU) | Provincias, 2002-2024 |
| F1-F3 Modelos de conjunto | PIB, renta disponible, población, hogares, tipos, parque, iniciadas y valor tasado | Nacional trimestral y panel provincial |

Muestras concretas de las estimaciones principales:

- E1-R3 (Barcelona): {{V18-E1-R3:cobertura}}.
- E2-R1 (Ley 11/2020): {{V18-E2-R1:cobertura}}.
- E3-R1 (inmigración): {{V18-E3-R1-beta:cobertura}}.
- E8-R1 (ITP): {{V18-E8-R1:cobertura}}.
- E10-A1 (grandes tenedores): {{V18-E10-A1:cobertura}}.
- E7-R3 (BVAR de tipos): {{V18-E7-R3:cobertura}}.

### A.11 Unidades selladas que se excluyen

- **v6.** Se excluyen de toda estimación las comunidades y provincias de la muestra sellada de v6 (Aragón, Asturias, Illes Balears, Canarias, Madrid, Región de Murcia, Navarra y La Rioja, con sus provincias y todos sus municipios, distritos y secciones). Quedan fuera, entre otras, las ciudades de Madrid, Palma, Zaragoza y Murcia.
- **V15 y V16.** Se excluyen los municipios, distritos y secciones de los bloques espaciales sellados de V15 y V16. En Barcelona, València, Sevilla y Málaga eso aparta una parte de los distritos: la muestra de Barcelona pierde Gràcia, Sant Andreu y Nou Barris. El total municipal de una ciudad con distritos sellados es una fuga declarada y no se usa en las principales (adenda 1.5).
- **Sellado temporal.** No se usa ningún periodo posterior al último visto de cada variable en V15 y V16, ni ninguna edición publicada después de la fecha de corte común de ambas (2026-10-17). Los topes por variable están en docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación. Donde dos reglas dan topes distintos se aplica el más restrictivo (por ejemplo, el total de transacciones de extranjeros).
- **Distritos sellados en v3.** No se excluyen: su muestra sellada ya se abrió en v3 con una evaluación por hipótesis (docs/v3/decisiones.md). Se dice por transparencia.
- **Sin acceso a muestras selladas.** No se lee data/sealed ni las filas marcadas como muestra sellada de v6, y no se ejecuta ninguna evaluación sellada. Las fuentes se leen con el filtro de sellado de V18 y con la exclusión de v6.

### A.12 Datos posteriores a la etiqueta

Las fuentes abiertas que el inventario de la fase 0 marcaba como ausentes y que no requerían al autor se descargaron después de la etiqueta (Censo de 2001 por nacionalidad, OpenStreetMap, Google Trends, Open Data BCN, afiliación por sector, tipos de cambio, entre otras). Llevan la marca `posterior_prereg` y su manifiesto. Su adquisición se limitó a descargar, normalizar y auditar, sin cruzarlas con ningún resultado. Cuando una fuente no pudo descargarse, la especificación que la necesitaba pasó a NO ESTIMABLE y se anotó en docs/v6/fuentes_fallidas.md.

### A.13 Licencias y terceros

- Incasòl: datos no redistribuibles; solo se publican agregados propios.
- Registradores: el aviso legal prohíbe reproducir; sus agregados se usan solo como contraste interno.
- Inside Airbnb: su política pide no republicar los datos; se publican solo agregados.
- Notariado: el portal no permite extracción automática; las compras por nacionalidad y al contado son tarea del autor.
- Paquetes de replicación de otros autores: se guardan fuera de git, con su licencia y suma de control. Ningún PDF se versiona; las fichas llevan enlace, DOI, licencia y notas, con citas de 15 palabras como máximo.
- Los PDF y paquetes figuran en data/bib (fuera de git, con sha256 en data/bib/CHECKSUMS.sha256).

### A.14 Interpolaciones y fuentes no validadas

Las series interpoladas (por ejemplo, visados de 1995 a 2007) y las fuentes no validadas entran solo en robustez. Las fechas de entrada en vigor de los cambios del ITP proceden de memorias de Hacienda y no están contrastadas con el BOE: por ello E8 tiene tope SUGESTIVO y esa limitación se repite en el anexo B.8.


### A.15 Monte Carlo de las herramientas

Cada herramienta nueva se validó antes de usarse con procesos generadores que reproducen la estructura de los diseños de V18 (output/v18/montecarlo/<herramienta>/). Se simula bajo el nulo y bajo la alternativa, con semilla fija y sin ningún dato real de resultado ni muestra sellada.

Hay dos criterios de «apto», y los dos se publican. El del encargo del Monte Carlo, más amplio, pide un tamaño al 5 % entre {{V18-AUX-CRIT-ENCARGO-TAM:min_num}} y {{V18-AUX-CRIT-ENCARGO-TAM:max_num}} y una cobertura al 95 % entre {{V18-AUX-CRIT-ENCARGO-COB:min_num}} y {{V18-AUX-CRIT-ENCARGO-COB:max_num}}, bajo el nulo y bajo la alternativa; con él se escribió el veredicto de cada herramienta (columna «Veredicto» de la segunda tabla). Las bandas de la adenda 1.12, más estrictas, piden un tamaño entre {{V18-AUX-CRIT-ADENDA-TAM:min_num}} y {{V18-AUX-CRIT-ADENDA-TAM:max_num}} y una cobertura entre {{V18-AUX-CRIT-ADENDA-COB:min_num}} y {{V18-AUX-CRIT-ADENDA-COB:max_num}}; son las que deciden en la inferencia de cada estimación (por ejemplo, el valor crítico corregido cuando el tamaño cae fuera de su banda) y están en la columna banda_112 de cada tabla.csv. Cuando los dos criterios difieren, la inferencia sigue el de la adenda, que es el del pre-registro (adenda 1.12 e I7); el criterio del encargo solo rotula la herramienta. La tabla da, por herramienta, el mínimo y el máximo entre las filas que deciden su veredicto (columna «principal», «entra_en_veredicto» o «decisivo» de su tabla.csv; si no la hay, la variante principal, con h = 8 en las proyecciones locales y el proxy-SVAR). Los escenarios de diagnóstico (rotulados así en su tabla.csv, como los de pocos controles o de variabilidad distinta) no deciden el veredicto y no entran en el mínimo ni en el máximo; en webb_twfe solo entran las filas del bootstrap de Webb, porque las de CR1 son otra inferencia (su veredicto está en la segunda tabla). El valor de cada condición está en output/v18/montecarlo/<herramienta>/tabla.csv y el veredicto en su resultado.json. En meta_bayes la cobertura es la de μ.

| Herramienta | Tamaño al 5 %: mínimo a máximo | Cobertura al 95 %: mínimo a máximo |
|---|---|---|
| aleatorizacion | {{V18-AUX-MC-ALEATORIZACION-TAM:min_sig}} a {{V18-AUX-MC-ALEATORIZACION-TAM:max_sig}} | {{V18-AUX-MC-ALEATORIZACION-COB:min_sig}} a {{V18-AUX-MC-ALEATORIZACION-COB:max_sig}} |
| bhj | {{V18-AUX-MC-BHJ-TAM:min_sig}} a {{V18-AUX-MC-BHJ-TAM:max_sig}} | {{V18-AUX-MC-BHJ-COB:min_sig}} a {{V18-AUX-MC-BHJ-COB:max_sig}} |
| conley | {{V18-AUX-MC-CONLEY-TAM:min_sig}} a {{V18-AUX-MC-CONLEY-TAM:max_sig}} | {{V18-AUX-MC-CONLEY-COB:min_sig}} a {{V18-AUX-MC-CONLEY-COB:max_sig}} |
| cs_webb | {{V18-AUX-MC-CS-WEBB-TAM:min_sig}} a {{V18-AUX-MC-CS-WEBB-TAM:max_sig}} | {{V18-AUX-MC-CS-WEBB-COB:min_sig}} a {{V18-AUX-MC-CS-WEBB-COB:max_sig}} |
| dcdh_aleatorizacion | {{V18-AUX-MC-DCDH-ALEATORIZACION-TAM:min_sig}} a {{V18-AUX-MC-DCDH-ALEATORIZACION-TAM:max_sig}} | {{V18-AUX-MC-DCDH-ALEATORIZACION-COB:min_sig}} a {{V18-AUX-MC-DCDH-ALEATORIZACION-COB:max_sig}} |
| driscoll_kraay | {{V18-AUX-MC-DRISCOLL-KRAAY-TAM:min_sig}} a {{V18-AUX-MC-DRISCOLL-KRAAY-TAM:max_sig}} | {{V18-AUX-MC-DRISCOLL-KRAAY-COB:min_sig}} a {{V18-AUX-MC-DRISCOLL-KRAAY-COB:max_sig}} |
| honest_did | {{V18-AUX-MC-HONEST-DID-TAM:min_sig}} a {{V18-AUX-MC-HONEST-DID-TAM:max_sig}} | {{V18-AUX-MC-HONEST-DID-COB:min_sig}} a {{V18-AUX-MC-HONEST-DID-COB:max_sig}} |
| iv_debil | {{V18-AUX-MC-IV-DEBIL-TAM:min_sig}} a {{V18-AUX-MC-IV-DEBIL-TAM:max_sig}} | {{V18-AUX-MC-IV-DEBIL-COB:min_sig}} a {{V18-AUX-MC-IV-DEBIL-COB:max_sig}} |
| lp_iv | {{V18-AUX-MC-LP-IV-TAM:min_sig}} a {{V18-AUX-MC-LP-IV-TAM:max_sig}} | {{V18-AUX-MC-LP-IV-COB:min_sig}} a {{V18-AUX-MC-LP-IV-COB:max_sig}} |
| meta_bayes | {{V18-AUX-MC-META-BAYES-TAM:min_sig}} a {{V18-AUX-MC-META-BAYES-TAM:max_sig}} | {{V18-AUX-MC-META-BAYES-COB:min_sig}} a {{V18-AUX-MC-META-BAYES-COB:max_sig}} |
| sa_webb | {{V18-AUX-MC-SA-WEBB-TAM:min_sig}} a {{V18-AUX-MC-SA-WEBB-TAM:max_sig}} | {{V18-AUX-MC-SA-WEBB-COB:min_sig}} a {{V18-AUX-MC-SA-WEBB-COB:max_sig}} |
| sdid_conley_taber | {{V18-AUX-MC-SDID-CONLEY-TABER-TAM:min_sig}} a {{V18-AUX-MC-SDID-CONLEY-TABER-TAM:max_sig}} | {{V18-AUX-MC-SDID-CONLEY-TABER-COB:min_sig}} a {{V18-AUX-MC-SDID-CONLEY-TABER-COB:max_sig}} |
| svar_proxy | {{V18-AUX-MC-SVAR-PROXY-TAM:min_sig}} a {{V18-AUX-MC-SVAR-PROXY-TAM:max_sig}} | {{V18-AUX-MC-SVAR-PROXY-COB:min_sig}} a {{V18-AUX-MC-SVAR-PROXY-COB:max_sig}} |
| webb_twfe | {{V18-AUX-MC-WEBB-TWFE-TAM:min_sig}} a {{V18-AUX-MC-WEBB-TWFE-TAM:max_sig}} | {{V18-AUX-MC-WEBB-TWFE-COB:min_sig}} a {{V18-AUX-MC-WEBB-TWFE-COB:max_sig}} |

El BVAR se valida con sus bandas del 68 % y del 90 %, que son aptas si cubren entre {{V18-AUX-CRIT-BVAR-COB68:min_num}} y {{V18-AUX-CRIT-BVAR-COB68:max_num}} y entre {{V18-AUX-CRIT-BVAR-COB90:min_num}} y {{V18-AUX-CRIT-BVAR-COB90:max_num}}, respectivamente; en sus filas decisivas la cobertura al 68 % va de {{V18-AUX-MC-BVAR-COB68:min_sig}} a {{V18-AUX-MC-BVAR-COB68:max_sig}} y la del 90 % de {{V18-AUX-MC-BVAR-COB90:min_sig}} a {{V18-AUX-MC-BVAR-COB90:max_sig}}.

| Herramienta | Veredicto | Condición |
|---|---|---|
| Callaway-Sant'Anna con Webb | APTO CONDICIONADO | Diseños municipales con muchos tratados y controles; NO APTO con ocho clusters |
| Sun-Abraham con Webb | APTO | Frágil si las comunidades de control son pocas |
| de Chaisemartin-D'Haultfœuille con aleatorización del calendario | APTO | Aleatorización entre ocho comunidades. El t de Student con siete grados de libertad es apto con valor crítico corregido (banda de la adenda 1.12); solo el bootstrap de Webb con ocho clusters es NO APTO |
| Aleatorización | APTO | Entre municipios y entre comunidades |
| Honest DiD | APTO CONDICIONADO | Solo sin desviación de tendencias paralelas; con desviaciones mayores es válido pero conservador y sin potencia |
| DiD sintético con Conley-Taber | APTO | Si los tratados son intercambiables con los controles; no si son más variables |
| Webb en TWFE | APTO | Con 8, 30 y 39 clusters (tamaños del diseño de la simulación: comunidades, provincias con valor tasado y provincias de entrenamiento). En la misma tabla, CR1 con la normal es APTO CONDICIONADO (NO APTO con ocho clusters) y CR1 con t de Student de G − 1 grados de libertad es APTO; los diseños con muy pocos tratados son NO APTOS |
| Conley | Mixto | Apto si el alcance de la dependencia no supera el corte; NO APTO si lo duplica |
| IV débil | Mixto | APTO con instrumento fuerte; APTO CONDICIONADO o NO APTO en los diseños más débiles |
| BHJ con pocos choques | NO APTO | Con pocos choques efectivos; por eso, con menos de {{V18-AUX-CRIT-HHI-INFERENCIA:sig}}, la inferencia principal de E3, E5, E9 y E12 es Webb por provincia con Anderson-Rubin y BHJ queda como alternativa (adenda 1.13) |
| Driscoll-Kraay con T corto | NO APTO | Con series temporales cortas |
| Proyección local con instrumento | NO APTO | Newey-West subestima la incertidumbre; el AR aumentado con EHW es el más cercano al nominal bajo el nulo; con T corto la respuesta a horizontes largos queda atenuada |
| SVAR con proxy | NO APTO | AR por método delta apto solo con F cercano a diez |
| BVAR recursivo | NO APTO | Bandas conservadoras o con cobertura distinta de la nominal |
| Metaanálisis bayesiano | NO APTO por conservador | Intervalos que cubren de más; con dos estudios y heterogeneidad el efecto fijo no cubre la media verdadera |

En la simulación, con ocho comunidades, la aleatorización del calendario es apta; el t de Student con siete grados de libertad lo es con valor crítico corregido, y el bootstrap de Webb es NO APTO. La muestra de E8-R1 tiene {{V18-AUX-E8-R1-NCCAA:sig}} comunidades. Las herramientas NO APTAS se publican con esa etiqueta y la clasificación no se apoya en ellas.
