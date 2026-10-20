# Factores de la subida del precio de la vivienda en España: reproducción, réplica y magnitudes (Documento de Trabajo V18)

Borja Romero, economista (firma individual, independiente). Documento de Trabajo de la versión V18 del proyecto (docs/v18/plan.md,
fase 6). Toda cifra procede de output/v5/cifras_clave.csv con su id. Toda cifra V18 es de capa C4 (nivel de evidencia EXPLORATORIO)
y lleva al lado su clasificación V18 (IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE; docs/v18/decisiones.md,
K2). Pre-registro interno sin sello de tiempo externo (etiqueta plan-replicacion-v18). Generado por src/v18/f6_documento.py; no se
edita a mano.


## Resumen ejecutivo

Este documento reproduce, replica y amplía con datos españoles los estudios publicados sobre nueve factores de la evolución del precio de la vivienda: vivienda turística, topes al alquiler, inmigración, ayudas a la demanda, oferta y suelo, obra nueva, tipos de interés, fiscalidad de la compra y compradores no residentes. Para cada factor busca una magnitud preferida que combine las estimaciones propias con las de la literatura, y con ellas ensaya una contabilidad de la subida por periodo y territorio.

Toda cifra V18 es de capa C4 (exploratoria) y lleva al lado su clasificación V18: IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE. El diseño es un pre-registro interno sin sello de tiempo externo (etiqueta git plan-replicacion-v18 sobre el commit ad4385c, 2026-10-20). Los análisis posteriores a ese commit se declaran a posteriori (anexo F).

| Factor | Magnitud preferida | Intervalo | Clasificación | Confianza | Limitación principal |
|---|---|---|---|---|---|
| Vivienda turística (E1) | 0,038 | [0,0145; 0,0615] (IC95) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Topes al alquiler (E2) | sin magnitud preferida | [−0,122; 0,0029] (rango) | SUGESTIVO | baja | la decisión cambia con la prior: rango sin magnitud preferida; estimación propia: SUGESTIVO |
| Inmigración (E3) | sin magnitud preferida | [−0,49; 3,51] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Ayudas a la demanda (E4) | 0,0408 | [−0,0138; 0,0953] (IC95) | NO ESTIMABLE | baja | pocos estudios con error típico; heterogeneidad declarada; estimación propia: no entra (NO ESTIMABLE) |
| Oferta y suelo (E5) | sin magnitud preferida | [−0,202; 1,48] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Obra nueva (E6) | −0,192 | [−0,319; −0,0646] (IC95) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Tipos de interés (E7) | sin magnitud preferida | [−5; −2] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |
| Fiscalidad de la compra (ITP) (E8) | sin magnitud preferida | [−3,5; −3] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (ASOCIACIÓN) |
| Compradores no residentes (E9) | sin magnitud preferida | [1,4; 2,1] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |

Unidades: E1: Δln del alquiler por +1 pp de viviendas turísticas sobre el parque; E2: ATT en ln de la renta de los contratos regulados; E3: % de precio por +1 % de población por entrada de inmigrantes; E4: θ: euros de alquiler por euro de ayuda; E5: elasticidad precio de la oferta de unidades; E6: elasticidad del alquiler respecto a la oferta nueva (% por 1 %); E7: % del precio por +100 pb del tipo hipotecario, a 8 trimestres; E8: % de precio por +1 pp del ITP, a 12 meses; E9: % de precio por +1 pp de cuota de compras de no residentes. Cifras: ids V18-B5-E1 a V18-B5-E9 de cifras_clave (capa C4). La clasificación es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura (sección 4). Confianza: media solo con magnitud preferida de tres o más estudios; muy baja sin error típico en la literatura; baja en el resto.

**Resultado.**

- Ninguna estimación propia alcanza la clase IDENTIFICADO. La única de clase SUGESTIVO es la de los topes al alquiler en Cataluña (E2-R1): una diferencia negativa de la renta de los contratos nuevos en los municipios regulados frente a los de control, que no es estable en el tiempo ni se separa de otros cambios de la época. Su cifra solo se difunde con la frase de limitación de la sección 4.2.
- El resto de las estimaciones propias son ASOCIACIÓN (por ejemplo, E1-R3 y E8-R1), NO CONCLUYENTE (E1-R4 y E3-R1) o NO ESTIMABLE por falta de variación o de datos.
- Solo E1, E4 y E6 tienen magnitud preferida, y en los tres casos procede de uno o dos estudios de la literatura, no de una estimación propia. En E2, E3 y E5 las estimaciones de la literatura son heterogéneas y no hay magnitud preferida. En E7, E8 y E9 la literatura da rangos sin error típico.
- Contabilidad de la subida. La regla fijada de antemano admite solo factores con una estimación propia válida dentro de la magnitud preferida. Ningún factor la cumple, de modo que toda la variación observada queda en «no explicado». Por ejemplo, la variación del precio real de compra en 1995T1-2007T4 que queda sin explicar es de 69,0 pp (100·Δln) (NO ESTIMABLE). Una ilustración aparte con magnitudes de la literatura, que no es una atribución, deja también sin explicar la mayor parte de la variación en casi todos los periodos y territorios (sección 5).
- El documento no permite decir qué factor explica la mayor parte de la subida en ningún periodo ni territorio. Tampoco modifica los veredictos de la auditoría de V17 (sección 6).

**Qué datos lo resolverían** (docs/v18/tareas_autor.md).

- Ayudas a la demanda (E4): microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas, con fecha de solicitud y concesión.
- Topes y turismo (E2, E1): registros de contratos de alquiler con renta anterior, superficie y tipo de contrato, y microdatos de portales de anuncios.
- Oferta, obra nueva y grandes tenedores (E5, E6, E10): descarga masiva del Catastro, Sistema de Información Urbana y restricciones físicas del suelo.
- Tipos y no residentes (E7, E9): compras por nacionalidad y al contado (Notariado, Registradores), más series de riesgo de los países de origen y la Encuesta Financiera de las Familias.
- Vacías y vivienda pública (E11, E12): calendario del recargo del IBI y del impuesto catalán, y promociones públicas por municipio y año.
- Para cualquier clase superior a las actuales: la evaluación sellada diferida (evaluate_v18), con datos posteriores a la etiqueta.


## Resumen no técnico

**Qué se ha hecho.** Se han revisado los estudios publicados sobre nueve factores que suelen citarse para explicar la subida del precio de la vivienda y del alquiler en España. Se han repetido con datos españoles los que se podían repetir. Cuando los estudios medían lo mismo en las mismas unidades, sus resultados se han combinado con los propios.

**Qué se ha encontrado.** Poco que se pueda afirmar con seguridad.

- En la mayoría de los casos no se puede estimar nada fiable. Faltan datos, o los datos disponibles apenas varían. Por ejemplo, no hay datos de quienes reciben las ayudas al alquiler ni registros de contratos con su renta anterior. Esto se declara como NO ESTIMABLE.
- Algunas estimaciones muestran una asociación, pero sin un diseño que permita interpretarla como el efecto de un factor (ASOCIACIÓN). Otras son demasiado imprecisas para decidir (NO CONCLUYENTE).
- Una sola estimación propia tiene un diseño suficiente para decir «la evidencia sugiere» (SUGESTIVO): la de los topes al alquiler en Cataluña entre 2019 y 2022. En los municipios regulados, la renta de los contratos nuevos fue menor que en los de control. La diferencia no fue estable y no se puede separar de otros cambios de la época, como la pandemia. Para los topes, el conjunto de estudios da un rango de -0,12 a 0,00 en logaritmos de la renta, sin una cifra única preferida.

**Qué no se puede afirmar.** No se puede decir cuánta parte de la subida corresponde a cada factor. La cuenta que se fijó antes de estimar solo admite factores con una estimación propia válida. Ninguno la cumple, de modo que toda la variación observada queda «sin explicar». Por ejemplo, entre 1995 y 2007 el precio real de compra varió 69,0 puntos porcentuales (cien veces la variación del logaritmo). Si se usaran magnitudes de la literatura, también quedaría sin explicar la mayor parte, y esa cuenta no sería una atribución.

**Qué significa para el debate público.** Las afirmaciones que achacan la subida a un solo factor no pueden confirmarse ni descartarse con estos resultados. Los veredictos de la auditoría anterior (V17) sobre medidas y afirmaciones no cambian.

**Qué haría falta.** Datos de beneficiarios de ayudas, registros de contratos de alquiler más completos, la descarga masiva del Catastro, compras por nacionalidad y al contado, y calendarios de impuestos locales sobre la vivienda vacía. Con datos posteriores se podrá, además, evaluar en muestra sellada las estimaciones que lo merezcan.

**Cautelas.** Toda cifra es exploratoria (capa C4). El diseño se fijó en un plan interno sin sello de tiempo externo. Ninguna cifra ha pasado una evaluación en muestra sellada. Se evalúan factores e instrumentos, nunca partidos ni personas.


## Abstract

For each of nine factors, the paper reproduces and replicates published estimates for Spain, extends them to more periods and territories where the data allow, and reports a preferred magnitude, an interval and a V18 classification. All V18 figures are exploratory (project layer C4). The design is an internal pre-registration without an external timestamp (git tag plan-replicacion-v18, commit ad4385c, 2026-10-20); the V17 audit, the robustness checks added after the first results and the deviations are declared as post hoc.

Results are mostly negative. No own estimate reaches the IDENTIFIED class. One is SUGGESTIVE (rent caps in Catalonia, E2-R1); the others are ASSOCIATION, INCONCLUSIVE or NOT ESTIMABLE for lack of variation or data. Only E1, E4 and E6 have a preferred magnitude, and it comes from one or two published studies. For E2, E3 and E5 the published estimates are too heterogeneous to combine; for E7, E8 and E9 the literature gives ranges without standard errors. For rent caps, the range across studies is -0,12 to 0,00 in log points of rent, with no preferred magnitude.

The accounting of the price rise follows a rule fixed beforehand that admits only factors with a valid own estimate. No factor qualifies, so the whole observed change is left unexplained: in 1995Q1-2007Q4 the unexplained change in the real purchase price is 69,0 percentage points (100 times the log change). An illustration with magnitudes from the literature is shown separately and is not an attribution.

Limitation sentence for the E2-R1 figure. Between 2020Q4 and 2022Q1, the average rent of new contracts registered at Incasòl in the municipalities subject to Law 11/2020 (excluding Barcelona city; sample: 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16) stood, relative to 2019, below that of unregulated Catalan municipalities with a tight market (log −0,0384; 95% CI -0,05 to -0,03, rounded to two decimals). The difference is not stable: it is largest in 2021Q1 ([FALTA CIFRA: coeficiente de 2021T1 del estudio de eventos de E2-R1]), narrows gradually until it is indistinguishable from zero in 2022Q1, before Constitutional Court ruling 37/2022, with no change afterwards, and falls to [FALTA CIFRA: coeficiente de E2-R1 con trayectorias trimestrales por tamaño del municipio e IC95] when quarterly trajectories are allowed to differ by municipality size. These data cannot separate the part associated with the law from a transitory COVID-19 shock in large municipalities or from a change in the composition of registered contracts, and sensitivity to differential trends (Honest DiD with M̄ of 0.5 or more) cannot be assessed with the available power. The magnitude is consistent with Jofre-Monseny et al. (2023), who use the same register and the same episode. V18 class: SUGGESTIVE; project layer C4.

Keywords: housing prices, rents, Spain, replication, meta-analysis, exploratory evidence.


## 1. Introducción

**Pregunta.** ¿Cuánto de la subida del precio de compra y del alquiler en España se asocia con cada uno de los factores que la literatura y el debate público señalan, y con qué grado de confianza? El documento responde con tres herramientas: la reproducción de estudios publicados con sus propios datos, su réplica con los datos del proyecto y su ampliación a más periodos, territorios y escalas. Después combina las estimaciones propias con las de la literatura y ensaya una contabilidad de la subida.

**Resultado en una frase.** Casi todas las preguntas quedan sin respuesta cuantitativa fiable. Entre 1995 y 2007, la contabilidad principal deja sin explicar 69,0 pp (100·Δln) de la variación del precio real de compra en el conjunto de España (toda la variación observada), porque ningún factor reúne una estimación propia válida. La sección 5 detalla los demás periodos y territorios.

**Aportación.**

1. *Reproducción.* Tres estudios con paquete de replicación abierto se reproducen con sus datos y coinciden con lo publicado (anexo B). Es un control de las herramientas, no de nuestros datos.
2. *Réplica y ampliación.* Cada estudio clave de la lista del plan se traslada a datos españoles con la especificación del original y se amplía. Casi todas las ampliaciones resultan NO ESTIMABLES: la comprobación de variación hecha antes de estimar muestra que el diseño no distinguiría una magnitud como la de la literatura.
3. *Magnitud preferida.* Un metaanálisis bayesiano de efectos aleatorios, con reglas fijadas de antemano, combina las estimaciones en una misma unidad. Cuando las unidades no son comparables, no se combinan y se dice.
4. *Contabilidad.* Con las magnitudes preferidas se calcula qué parte de la variación observada se asociaría con cada factor, con una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural.
5. *Clasificación y capa.* Cada estimación lleva una clase V18 (IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE) y la capa C4 del proyecto. La clase no promueve la capa: sin evaluación en muestra sellada, nada de V18 pasa de C4.

**Lo que ya se sabía.** El proyecto había estimado antes casi todos los factores con estos mismos datos (versiones V8 a V17). Las réplicas de V18 no son, por tanto, primeras miradas, y el plan lo declaró antes de estimar: las especificaciones que repiten una ya vista llevan la marca `repite_visto`. La descomposición histórica de V8 no designó ningún factor como el más relevante en ninguno de los casos analizados; V18 llega a una conclusión del mismo sentido por otro camino.

**Relación con V17.** V17 auditó afirmaciones de divulgación y medidas de política con la literatura y los datos disponibles. Sus secciones sobre demografía, problema general o local, factibilidad de construir, medidas auditadas y discurso público se integran aquí como 5.2, 5.3, 6.1, 6.2 y 6.3. Son análisis a posteriori de capa C4. La sección 6 dice qué cambia en ellas con los resultados de V18: ningún veredicto.

**Neutralidad.** Se evalúan afirmaciones, factores e instrumentos, nunca partidos ni personas. Si una conclusión resulta incómoda para cualquier posición, se dice igual. No se usa lenguaje valorativo.

**Pre-registro.** El diseño es un pre-registro interno sin sello de tiempo externo: el plan de replicación y su adenda, fijados con la etiqueta git local plan-replicacion-v18 sobre el commit ad4385c el 2026-10-20. No es un pre-registro depositado en un registro externo. El anexo F separa lo pre-registrado de lo hecho a posteriori.

**Estructura.** La sección 2 describe los datos y las unidades selladas que se excluyen. La sección 3 expone los métodos y las reglas de clasificación. La sección 4 presenta los resultados por factor: original, reproducción, réplica, ampliación y magnitud preferida. La sección 5 contiene la contabilidad de la subida y las dos secciones heredadas de V17 sobre población y componente común. La sección 6 trata las implicaciones para las políticas. La sección 7 recoge las limitaciones y los datos que las resolverían. Los anexos reúnen fichas, reproducciones, planes, pruebas, Monte Carlo y la declaración de pre-registro.


## 2. Datos

**Regla general.** Toda cifra del documento procede de output/v5/cifras_clave.csv con su id (V18-*, V17-* y anteriores), su fuente, su capa y, en las cifras V18, su clasificación. El generador redondea los valores: dos decimales para los menores que la unidad en valor absoluto, un decimal para los intermedios y enteros para los recuentos y las cifras grandes. Los coeficientes pequeños se muestran con tres cifras significativas; los límites de sus intervalos, redondeados como se acaba de decir (los valores completos están en tablas_v18.xlsx, pestaña «estimaciones»).

### 2.1 Fuentes por factor

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

- E1-R3 (Barcelona): 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador.
- E2-R1 (Ley 11/2020): 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16.
- E3-R1 (inmigración): 39 provincias de entrenamiento; N = 234; sin las 11 provincias de v6.
- E8-R1 (ITP): 30 provincias con valor tasado trimestral de 7 comunidades de régimen común no selladas (sin Cantabria: no hay serie provincial completa), 2007T1-2026T2.
- E10-A1 (grandes tenedores): 1365 municipios.
- E7-R3 (BVAR de tipos): nacional.

### 2.2 Unidades selladas que se excluyen

- **v6.** Se excluyen de toda estimación las comunidades y provincias de la muestra sellada de v6 (Aragón, Asturias, Illes Balears, Canarias, Madrid, Región de Murcia, Navarra y La Rioja, con sus provincias y todos sus municipios, distritos y secciones). Quedan fuera, entre otras, las ciudades de Madrid, Palma, Zaragoza y Murcia.
- **V15 y V16.** Se excluyen los municipios, distritos y secciones de los bloques espaciales sellados de V15 y V16. En Barcelona, València, Sevilla y Málaga eso aparta una parte de los distritos: la muestra de Barcelona pierde Gràcia, Sant Andreu y Nou Barris. El total municipal de una ciudad con distritos sellados es una fuga declarada y no se usa en las principales (adenda 1.5).
- **Sellado temporal.** No se usa ningún periodo posterior al último visto de cada variable en V15 y V16, ni ninguna edición publicada después de la fecha de corte común de ambas (2026-10-17). Los topes por variable están en docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación. Donde dos reglas dan topes distintos se aplica el más restrictivo (por ejemplo, el total de transacciones de extranjeros).
- **Distritos sellados en v3.** No se excluyen: su muestra sellada ya se abrió en v3 con una evaluación por hipótesis (docs/v3/decisiones.md). Se dice por transparencia.
- **Sin acceso a muestras selladas.** No se lee data/sealed ni las filas marcadas como muestra sellada de v6, y no se ejecuta ninguna evaluación sellada. Las fuentes se leen con el filtro de sellado de V18 y con la exclusión de v6.

### 2.3 Datos posteriores a la etiqueta

Las fuentes abiertas que el inventario de la fase 0 marcaba como ausentes y que no requerían al autor se descargaron después de la etiqueta (Censo de 2001 por nacionalidad, OpenStreetMap, Google Trends, Open Data BCN, afiliación por sector, tipos de cambio, entre otras). Llevan la marca `posterior_prereg` y su manifiesto. Su adquisición se limitó a descargar, normalizar y auditar, sin cruzarlas con ningún resultado. Cuando una fuente no pudo descargarse, la especificación que la necesitaba pasó a NO ESTIMABLE y se anotó en docs/v6/fuentes_fallidas.md.

### 2.4 Licencias y terceros

- Incasòl: datos no redistribuibles; solo se publican agregados propios.
- Registradores: el aviso legal prohíbe reproducir; sus agregados se usan solo como contraste interno.
- Inside Airbnb: su política pide no republicar los datos; se publican solo agregados.
- Notariado: el portal no permite extracción automática; las compras por nacionalidad y al contado son tarea del autor.
- Paquetes de replicación de otros autores: se guardan fuera de git, con su licencia y suma de control. Ningún PDF se versiona; las fichas llevan enlace, DOI, licencia y notas, con citas de 15 palabras como máximo.
- Los PDF y paquetes figuran en data/bib (fuera de git, con sha256 en data/bib/CHECKSUMS.sha256).

### 2.5 Interpolaciones y fuentes no validadas

Las series interpoladas (por ejemplo, visados de 1995 a 2007) y las fuentes no validadas entran solo en robustez. Las fechas de entrada en vigor de los cambios del ITP proceden de memorias de Hacienda y no están contrastadas con el BOE: por ello E8 tiene tope SUGESTIVO y esa limitación se repite en la sección 4.8.


## 3. Métodos

### 3.1 Diseños por factor

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

### 3.2 Inferencia

Se publica siempre la inferencia convencional que corresponde a cada diseño. Los errores típicos se agrupan al nivel del tratamiento. Con pocos clusters se usa el wild cluster bootstrap con pesos de Webb. En shift-share se usan los intervalos de Anderson-Rubin y el F efectivo de Montiel Olea y Pflueger, con el número efectivo de choques (inverso del índice de Herfindahl de los pesos, de Borusyak, Hull y Jaravel) calculado antes de estimar. También se usan Conley en datos espaciales, Driscoll-Kraay en paneles con dependencia transversal y Newey-West en series. Cuando el número de clusters es muy pequeño (ocho comunidades), la inferencia por aleatorización del calendario sustituye a Webb.

Cada herramienta se valida antes por Monte Carlo con procesos generadores que reproducen la estructura de los diseños (anexo E). Un resultado «apto» tiene tamaño y cobertura dentro de las bandas de la adenda 1.12. «Con valor crítico corregido» obliga a publicar el p-valor con el valor crítico calibrado en la simulación. «No fiable» se publica con esa etiqueta y la clasificación no puede apoyarse en él. Las herramientas NO APTAS (por ejemplo, la proyección local con Newey-West, el SVAR con proxy, el BVAR y el metaanálisis bayesiano) se publican con esa etiqueta y su resultado se lee como informativo.

### 3.3 Clasificación V18

La clase se asigna con las reglas del plan (B3 y criterios I1 a I8, revisados en la adenda 1.2), sin elegirla por el p-valor:

- **IDENTIFICADO.** Diseño creíble, primera etapa fuerte o intervalo de Anderson-Rubin acotado, pretendencias y placebos superados, robustez, significación tras Holm, réplica ciega coincidente y ningún tope de la especificación. Ninguna estimación de V18 llega a esta clase.
- **SUGESTIVO.** Diseño creíble y réplica ciega coincidente, sin fallo decisivo, con alguna prueba débil o un tope fijado en la adenda. Se dice «la evidencia sugiere», con la limitación concreta.
- **NO CONCLUYENTE (sin potencia).** Diseño válido sin significación y sin equivalencia demostrada por la prueba TOST.
- **ASOCIACIÓN.** Diseño no creíble o fallo decisivo (por ejemplo, un cambio de signo en una prueba B4 o un placebo de fecha significativo del mismo signo).
- **NO ESTIMABLE.** Falta un dato imprescindible o la comprobación previa de variación no alcanza el mínimo.

Tres lecturas decididas antes de difundir resultados (docs/v18/decisiones.md). Un cambio de signo en una prueba de robustez del plan es un fallo decisivo y no se compensa con un tope (K7). Un coeficiente no significativo es NO CONCLUYENTE si supera los criterios de diseño y ASOCIACIÓN si no los supera (K7). Cuando la ficha admite dos lecturas con clases distintas se toma la más prudente (K8 bis). La etiqueta de coherencia con la literatura (I6) se publica, pero no interviene en la clase ni en la entrada en la magnitud preferida. Un resultado sin réplica ciega coincidente no se clasifica.

Capa y lenguaje (K2). Toda cifra V18 es de capa C4, con nivel de evidencia EXPLORATORIO. La clase V18 va en un campo propio al lado de la capa y no la promueve. Cada cifra se lee como asociación condicionada al diseño. La fórmula condicional prevista para la clase IDENTIFICADO solo cabría en la sección 4 y en los anexos, y no se ha necesitado.

### 3.4 Estimabilidad previa por magnitud mínima detectable

Antes de estimar cada especificación principal, y sin mirar su resultado, se calcula por Monte Carlo la magnitud mínima detectable (MDE) con la potencia convencional fijada en la adenda 1.3. El cálculo usa la variación real del tratamiento, de la exposición o del instrumento y la dispersión residual de V15 o V16 (declarada «ya vista») o la del periodo previo. La especificación es estimable si el MDE no supera la magnitud de referencia de la literatura convertida a nuestra unidad. Si no, es NO ESTIMABLE por variación y se publica el MDE, no el coeficiente. Además se exigen mínimos de datos (por ejemplo, un número mínimo de municipios tratados y de control) y, en shift-share, un número efectivo de choques suficiente. Esta comprobación explica la mayoría de los NO ESTIMABLE.

### 3.5 Magnitud preferida (B5, adenda 1.9)

- **Qué entra.** La estimación propia designada de cada factor, si su diseño es válido y es IDENTIFICADO, SUGESTIVO o NO CONCLUYENTE, con independencia de su p-valor. No entran las ASOCIACIÓN ni las NO ESTIMABLE. Los estudios de la literatura entran si están en la misma unidad y tienen error típico.
- **Episodios compartidos.** Si una estimación propia y un estudio miden el mismo episodio con la misma fuente, el episodio cuenta una vez, combinado con una correlación modelada fijada en la adenda.
- **Modelo.** Metaanálisis bayesiano de efectos aleatorios con tres priors sobre el efecto medio. La magnitud preferida se publica solo si la decisión (signo e inclusión del cero) coincide en las tres. Si no, se publica el rango de las tres sin magnitud preferida. Si la heterogeneidad es alta y el intervalo de predicción cambia de signo, tampoco hay magnitud preferida. Con un solo estudio se publica su magnitud; con dos, el efecto fijo ponderado por precisión. Si las unidades no son comparables, no se combinan.
- **Advertencia de la simulación.** El metaanálisis bayesiano resultó NO APTO por conservador: sus intervalos cubren de más y, con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera. Los intervalos con más de dos estudios son prudentes y los de dos estudios no deben leerse como IC95 fiables.
- **Referencias.** Toda referencia lleva el estado de su ficha: VERIFICADA (DOI comprobado con Crossref o DataCite; cuartil no verificado), NO VERIFICADA o DISCREPANTE (la ficha describe una versión de trabajo y el DOI corresponde a la versión publicada; se trata como NO VERIFICADA).
- **Confianza de la tabla de magnitudes.** Regla fija: «media» solo con magnitud preferida de tres o más estudios; «muy baja» si la literatura no tiene error típico en la unidad; «baja» en el resto. Nunca «alta», porque toda cifra es C4. La clasificación de cada fila es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura.

### 3.6 Contabilidad de la subida (adenda 1.10)

La contribución de un factor es su magnitud preferida por su variación observada en el periodo y el territorio, con la incertidumbre propagada por Monte Carlo sobre la magnitud y una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural: no hay interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Reglas:

- Un factor sin magnitud dice «sin magnitud», no cero.
- Cada contribución de un diseño de panel con efectos de periodo se rotula «relativa entre provincias (o unidades), sin el componente común». Solo los tipos (E7, series nacionales) incluyen el componente común.
- Cada fila dice si la variación observada del factor está dentro o fuera del soporte de la muestra de estimación. Fuera del soporte no lleva cifra.
- Inmigración (E3) y no residentes (E9) usan cuotas del padrón por nacionalidad y no se suman: E9 va como alternativa de E3.
- **Lectura restrictiva aplicada.** La adenda admite todo factor con magnitud preferida construida con las reglas de B5. El plan deja las magnitudes «solo literatura» en una tabla secundaria rotulada, y una magnitud sin estimación propia no tiene clase que limite la confianza. Se aplicó la lectura restrictiva (K10): la tabla principal solo admite factores con estimación propia dentro de B5. Ninguno la cumple. Las magnitudes de la literatura van en una tabla aparte, rotulada ilustración. La lectura inclusiva solo cambiaría de tabla a E1, E4 y E6, y no cambiaría ninguna conclusión.
- La variación observada usa el deflactor del PIB del INE, no el IPC general que usó V8. Las variaciones observadas difieren por eso de las de V8.
- Las viviendas liberadas por envejecimiento nunca se restan de la necesidad (la proyección de hogares del INE ya las descuenta).

### 3.7 Modelos de conjunto (F)

El modelo de precio de largo plazo con corrección del error, el de alquiler y el de oferta se contrastan primero para cointegración, con corrección por pruebas múltiples. Si el contraste no rechaza la ausencia de cointegración, no se publican elasticidades de largo plazo ni sobrevaloración (regla AD-F), y solo se publica la dinámica de corto plazo como ASOCIACIÓN.

### 3.8 Evaluación sellada diferida

La vía a la capa C3 es una evaluación sellada diferida (evaluate_v18) con datos posteriores al tope de entrenamiento, una sola evaluación por hipótesis y un criterio de superación fijado en la adenda 1.11. No se ejecuta dentro de V18, requiere orden expresa del autor y no puede abrirse antes de 2027. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015 a 2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.

### 3.9 Multiplicidad y registro

Toda especificación, incluidas las variantes y las fallidas, se registra antes de leer su resultado. Se controlan los falsos descubrimientos con Holm dentro de la familia de cada factor y con Benjamini-Yekutieli entre las variantes enumeradas de cada identificador. Ningún modelo se elige por su p-valor. SEED 20261010 en todo lo aleatorio.


## 4. Resultados por factor

Cada subsección sigue el mismo orden: estudio original, reproducción, réplica, ampliación y magnitud preferida. Las estimaciones propias se rotulan «estimación propia V18» y llevan su clase V18 y su capa. Las magnitudes de la literatura se rotulan «literatura» y llevan el estado de su ficha (VERIFICADA, NO VERIFICADA o DISCREPANTE; la verificación es la del DOI, y el cuartil de la revista no está verificado). Todas las cifras V18 son de capa C4 y se leen como asociaciones condicionadas al diseño.

Los valores publicados por estudio de la literatura no están en cifras_clave: [FALTA CIFRA: magnitud y error típico de cada estudio de la literatura (output/v18/f5/magnitudes_estudios.csv)]. Por eso esta sección describe cada estudio por su diseño, su signo y el estado de su ficha, y da las magnitudes agregadas con los ids de la magnitud preferida (V18-B5-E1 a V18-B5-E9). Los intervalos de la magnitud preferida están en la tabla del resumen ejecutivo. El estado de las fichas que no se citan con estado en el texto está en output/v18/f1/catalogo.csv y en el anexo A.

### 4.1 Vivienda turística (E1)

**Original (literatura).** Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), Journal of Urban Economics 119, 103278 (ficha VERIFICADA). Barcelona, 2007-2017, alquiler anunciado. Diseños: efectos fijos con tendencias heterogéneas por barrio; shift-share con atractivos turísticos (dónde) y búsquedas de Google (cuándo); estudio de eventos; caso de la Sagrada Família. Resultado publicado: [FALTA CIFRA: efecto de Garcia-López et al. (2020) sobre el alquiler en el barrio medio y en el decil de mayor exposición]. Su unidad es el logaritmo del alquiler por cada 100 anuncios en el área estadística básica, y no es convertible a puntos de densidad de viviendas porque la ficha no da las viviendas por área. Con sus coeficientes y la densidad turística observada, V17 calculó una ilustración, que no es una estimación: 1,6 por ciento del alquiler a escala nacional (rango 1,0 a 2,1).

**Reproducción.** El paquete de Garcia-López et al. no es público, y no se reproduce. Sí se reproduce, con el paquete de su autor, Chaves-Fonseca (2026) (VERIFICADA): un instrumento del mismo tipo (proximidad a atractivos por búsquedas de Google) sobre precios de compra en Madrid. Coincide con lo publicado (anexo B). Valida la herramienta, no el resultado de Barcelona.

**Réplica (estimaciones propias V18, Barcelona).**

- E1-R3, estudio de eventos de dosis (densidad HUT de 2018T2 por periodo posterior, sobre el logaritmo del alquiler mediano de SERPAVI por sección): coeficiente 0,00443 por punto de densidad, con IC95 que excluye el cero. Clase ASOCIACIÓN, capa C4. La estimación no cumple los criterios de diseño de una clase superior y se lee como asociación. Muestra: 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador.
- E1-R4, Sagrada Família (secciones del radio frente al anillo exterior): coeficiente 0,00166, con IC95 de Webb que incluye el cero. Clase NO CONCLUYENTE: el diseño es válido, la estimación no es significativa y la equivalencia con el nulo no queda acotada. La réplica ciega y el modelizador partieron de lecturas distintas de la ficha (con y sin los adelantos de 2011-2012 como regresores); se resolvió a favor de la más prudente (K8 bis). La variante con adelantos, que sí acota el nulo, se publica al lado como variante: [FALTA CIFRA: coeficiente e IC90 de E1-R4 con adelantos como regresores].
- E1-R1 (stock HUT por barrio) es NO ESTIMABLE: solo 18 barrios cumplen el cambio mínimo de stock exigido por el plan. E1-R2 (IV con atractivos y búsquedas) es NO ESTIMABLE: F efectivo de la primera etapa 0,0233.
- Coprincipal H3 de V15 en la muestra V18: −6,5e−05 (logaritmo del alquiler por desviación típica intra-sección). No se clasifica y, como en V15, no se distingue de cero. Q2a de V16 dio 0,0132 en el logaritmo del IPC de alquiler por desviación típica de la exposición, con una herramienta NO APTA, solo puntual.

**Ampliación.** E1-A1 (viviendas turísticas por sección, instrumentadas con proximidad a atractivos por noches de la NUTS 3, en València, Sevilla, Málaga y Alicante, 2021-2024) es NO ESTIMABLE: la magnitud mínima detectable es 0,166, frente a 0,038 de la referencia. La regulación local (PEUAT y moratorias) como diferencias en diferencias no se estima: faltan la geometría de las zonas y las fechas (tarea 13 del autor).

**Magnitud preferida (literatura).** 0,038 en Δln del alquiler por +1 pp de viviendas turísticas sobre el parque, clase de la estimación propia designada NO ESTIMABLE, capa C4. Procede de un solo estudio, Segú (2018), cuya ficha es NO VERIFICADA. estudios de España (1 estudios con error típico en la unidad (un solo estudio en la unidad); estado B5: magnitud de un solo estudio). Garcia-López et al. (VERIFICADA), Chaves-Fonseca (VERIFICADA) y Duso et al. (VERIFICADA) no entran por unidad no convertible. La estimación propia E1-R3 no es coherente con la referencia (etiqueta I6). Confianza baja.

**Lectura.** Los datos disponibles no permiten contrastar la magnitud local de la literatura ni en otras ciudades ni después de las regulaciones. No contradice lo publicado: v3, v6 y V8 calificaban de no concluyente el resultado nacional, y V17 limitó el efecto local a Barcelona 2012-2016.

### 4.2 Topes al alquiler (E2)

**Original (literatura).** Jofre-Monseny, Martínez-Mazza y Segú (2023), Regional Science and Urban Economics 101, 103916 (VERIFICADA): diferencias en diferencias y estudio de eventos con el registro de contratos; renta menor en los contratos regulados y sin caída detectable de la oferta. Monràs y García-Montalvo (2023), documento de trabajo de la Reserva Federal de San Francisco (VERIFICADA): contratos del Incasòl, no anuncios (así lo recoge la ficha de la fase 1, que corrige la lectura del plan); efectos distintos por tramo de precio. Con el mismo registro, la réplica de V17 sobre la renta de los contratos nuevos da una mediana de -5,8 por ciento (rango de especificaciones -6,8 a -5,1; no es un intervalo de confianza).

**Reproducción.** Ninguno de los dos estudios tiene paquete público (microdatos no públicos del Incasòl). No se reproducen.

**Réplica (estimación propia V18).**

- E2-R1, renta media de los contratos nuevos, 2019T1-2022T1. Coeficiente −0,0384 en logaritmos (IC95 de Webb -0,05 a -0,03). Clase SUGESTIVO, capa C4. Muestra: 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16. La réplica ciega coincide con el coeficiente del modelizador, y las dos rondas del abogado del diablo no activan ningún fallo decisivo. La clase queda en SUGESTIVO por la potencia insuficiente de la prueba de pretendencias, el placebo de fecha en el límite y la corrección de un fallo conocido de V9-D1b (grupo de control y ventana).

La cifra no se difunde sin la frase de limitación siguiente, que se reproduce tal cual (K9):

> Entre 2020T4 y 2022T1, la renta media de los contratos nuevos registrados en el Incasòl en los municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad; muestra: 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16) se situó, respecto a 2019, [FALTA CIFRA: diferencia porcentual equivalente al coeficiente logarítmico] por debajo (log −0,0384; IC95 -0,05 a -0,03, redondeado a dos decimales) de la de municipios catalanes no regulados con mercado tensionado. La diferencia no es estable: es máxima en 2021T1 ([FALTA CIFRA: coeficiente de 2021T1 del estudio de eventos de E2-R1]), se reduce de forma gradual hasta no distinguirse de cero en 2022T1, antes de la STC 37/2022, sin cambio posterior, y baja a [FALTA CIFRA: coeficiente de E2-R1 con trayectorias trimestrales por tamaño del municipio e IC95] cuando se permiten trayectorias trimestrales distintas según el tamaño del municipio. Con estos datos no se separa la parte asociada a la norma de un choque transitorio de la COVID-19 en los municipios grandes ni de un cambio en la composición de los contratos registrados, y la sensibilidad a tendencias diferenciales (Honest DiD con M̄ ≥ 0,5) no es evaluable con la potencia disponible. La magnitud coincide con la de Jofre-Monseny et al. (2023), que usan el mismo registro y el mismo episodio. Clase V18: SUGESTIVO; capa del proyecto C4.

- Pruebas. La prueba de pretendencias no rechaza, pero su potencia es insuficiente para descartar una pendiente previa relevante. El placebo de fecha (adopción falsa en 2017) tiene signo contrario al principal. Honest DiD solo es apto con M̄ igual a cero; con valores mayores es válido pero conservador y no decide (anexo E). El placebo de resultado no tiene dato en el repositorio. El signo es negativo en todas las variantes estimadas.
- Robustez a posteriori (B6; no decide la clase). El coeficiente medio no describe un nivel estable: la diferencia se reduce durante la vigencia. Con HUT y ln(población) por trimestre: −0,0242. Con controles emparejados por el crecimiento previo de la renta: −0,0546. Con diferencias en diferencias sintéticas: −0,044. Los intervalos de estas tres variantes excluyen el cero. Salto en 2022T2 sobre la extrapolación de la recta: −0,0217, con IC95 que incluye el cero.
- Reversión tras la STC 37/2022 (2022T2-2023T4): −0,00157, con IC95 que incluye el cero. El nivel vuelve al previo y no se detecta un rebote.
- E2-R1c, número de contratos nuevos por 1.000 habitantes: coeficiente 0,0173, con IC95 que incluye el cero. Clase ASOCIACIÓN: el placebo de fecha es significativo y la diferencia persiste tras la STC. Con el denominador de hogares inquilinos del Censo 2021, la variante a posteriori da −0,0314, también con IC95 que incluye el cero y que no excluye caídas relevantes. No se descarta el desvío a contratos de temporada ni la falta de depósito de fianza.

**Ampliación.** Las cuatro ampliaciones son NO ESTIMABLES. Zonas tensionadas de 2024 en Cataluña (E2-A1): MDE 0,0408, superior al umbral. Otras comunidades (E2-A2): 6 municipios tratados con datos y periodo posterior, frente a un mínimo mayor del plan. Desplazamiento a la venta (E2-A3): 2 municipios de control en la serie municipal del MIVAU. Desbordamiento a municipios vecinos (E2-A4): MDE 0,0444, superior al umbral. El análisis por tramo de renta y el desvío a temporada necesitan los microdatos de fianzas (tarea 4 del autor).

**Comparación con lo publicado.** El informe integral (III.2) calificaba los topes de «prometedora» y recogía una renta regulada menor. E2-R1 es compatible con esa lectura y añade que la diferencia se reduce durante la vigencia. Sobre el número de contratos, V17 concluía que la evidencia no permite concluir; E2-R1c no lo cambia. V17 recoge para los contratos una mediana de 3,6 por ciento (rango -1,3 a 7,6). E2-A1 repite H1 y H2 de V15 en entrenamiento y no sustituye su evaluación sellada.

**Magnitud preferida.** No hay. estudios de España, Francia, Alemania (5 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (la decisión no coincide en las tres priors)). La decisión no coincide en las tres priors (con una de ellas el intervalo incluye el cero), la heterogeneidad es alta y el intervalo de predicción cambia de signo. Se publica el rango de las tres priors: -0,12 a 0,00 en logaritmos de la renta de los contratos regulados (clase de la estimación propia designada: SUGESTIVO). Estudios que entran (literatura): Jofre-Monseny et al. 2023 (VERIFICADA), Monràs y García-Montalvo 2023 (VERIFICADA), Breuille et al. 2025 (NO VERIFICADA), Hahn et al. 2021 (VERIFICADA) y la estimación propia E2-R1, contando una vez el episodio catalán. Con la estrategia alternativa para extraer la magnitud de Hahn et al. sí habría magnitud preferida; se publica como sensibilidad y no cambia la tabla, porque la regla se fijó antes de combinar [FALTA CIFRA: magnitud preferida de la sensibilidad con la estrategia B de Hahn et al. (output/v18/f5/sensibilidad_b5.csv)]. La herramienta es NO APTA por conservadora.

### 4.3 Inmigración (E3)

**Original (literatura).** González y Ortega (2013), Journal of Regional Science 53(1), 37-59: instrumento por asentamientos históricos de cada nacionalidad en provincias españolas, años 2000-2010 según la ficha de la fase 1. Se leen además dos versiones previas del mismo trabajo, con ventanas distintas: IZA 2009 (NO VERIFICADA) y Chicago Fed 2011 (NO VERIFICADA). La fase 1 señala que la fracción de la subida que los autores atribuyen a la inmigración difiere entre versiones: [FALTA CIFRA: fracción de la subida de precios atribuida a la inmigración en cada versión de González y Ortega]. V17 dedujo del resumen de la versión de 2013 una elasticidad implícita de 1,3 por ciento de precio por 1 % de población (rango 1,0 a 1,5); es una derivación a partir del resumen, no un coeficiente publicado. Saiz (2007) y Borusyak, Hull y Jaravel (2022) son referencias metodológicas.

**Reproducción.** González y Ortega no tiene paquete público. Se reproduce, con el paquete de sus autores, Borusyak, Hull y Jaravel (2022), aplicación de Autor, Dorn y Hanson con datos: coincide con lo publicado en todos los coeficientes comparados, y la herramienta de shift-share queda validada (anexo B).

**Réplica (estimación propia V18).** E3-R1 (provincias no selladas, 2002-2008, sin 2003; instrumento por la distribución del grupo de origen en el Censo de 2001 y las entradas nacionales del grupo; ocho grupos de origen en lugar de dieciséis, desviación declarada): asociación entre la entrada de extranjeros y la variación anual del valor tasado de 3,55 €/m² por punto de población, con IC95 de Webb-Anderson-Rubin de -53,5 a 63,9. F efectivo de la primera etapa 81,1; magnitud mínima detectable 36,7 €/m² por punto; número efectivo de choques 7,9. Clase NO CONCLUYENTE, capa C4. El intervalo incluye el cero y también la magnitud de la versión IZA de 2009 [FALTA CIFRA: coeficiente de la versión IZA de 2009 en €/m² por punto de población]. Muestra: 39 provincias de entrenamiento; N = 234; sin las 11 provincias de v6.

**Ampliación.** Las demás especificaciones son NO ESTIMABLES por variación (la magnitud mínima detectable supera la de referencia): la elasticidad de 2002-2010 (E3-R2, MDE 2,33), su variante hasta 2008 (E3-R2b, 2,14), la ampliación de 2014 a 2022 en precio (E3-A1, 10,4 % por punto), en alquiler municipal (E3-A2, 13,4 % por punto) y la ventana de 2002 a 2019 (E3-A5, 3,8 % por punto). La separación entre demanda de compra y de alquiler por tenencia del Censo de 2011 no tiene datos (E3-A4). Coincide con V9-D4 (F efectivo bajo) y con H4 de V15 y Q3 de V16 (no concluyentes).

**Magnitud preferida.** No hay: estudios de España, EE. UU., Reino Unido, Alemania (5 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo)). Rango de las tres priors: -0,49 a 3,5 en % de precio por +1 % de población (literatura). Entran González y Ortega 2009 (NO VERIFICADA), Sanchis-Guarner 2017 (DISCREPANTE), Saiz 2007 (VERIFICADA), Sá 2015 (VERIFICADA) y Ünal 2022 (NO VERIFICADA). Quedan fuera por versión duplicada, unidad o falta de error típico: González y Ortega 2011 (NO VERIFICADA), Accetturo 2012 (DISCREPANTE) y Torres y Montero 2023 (VERIFICADA). La heterogeneidad es alta y el intervalo de predicción cambia de signo. La estimación propia designada es NO ESTIMABLE, y E3-R1 (NO CONCLUYENTE) está en otra unidad: se muestra al lado y no se combina. La elasticidad implícita de V17 cae dentro del rango.

### 4.4 Ayudas a la demanda (E4)

**Original (literatura).** Fack (2005, CEPREMAP; VERIFICADA) y Fack (2006): diferencias y triples diferencias con la extensión de las ayudas al alquiler de los años noventa en Francia. Gibbons y Manning (2006): recorte del Housing Benefit en el Reino Unido. Grislain-Letrémy y Trevien (2022, Banque de France, documento de trabajo 886): discontinuidad geográfica en aglomeraciones francesas. Eerola et al. (2026; VERIFICADA): Finlandia. Todos miden la parte de la ayuda que acaba en el alquiler (traslación θ) o su relación con el alquiler en otra unidad. Ningún estudio es español.

**Reproducción y réplica.** Ninguno tiene paquete público. E4 es NO ESTIMABLE (E4-X1): no hay microdatos de perceptores del Bono Alquiler Joven ni convocatorias autonómicas con fecha, solo el calendario estatal. La discontinuidad por edad de Q7a (V16) da −0,12 en el logaritmo del alquiler (IC95 -0,26 a 0,02); mide un cambio de generosidad, no la incidencia, y no se repite.

**Magnitud preferida (solo literatura, sin estimación propia).** θ = 0,0408 euros de alquiler por euro de ayuda, clase NO ESTIMABLE, capa C4. estudios de Francia, Finlandia (2 estudios con error típico en la unidad (media ponderada por la inversa de la varianza (efecto fijo)); estado B5: magnitud preferida). Entran Fack 2005 (VERIFICADA) y Eerola et al. 2026 (VERIFICADA), por efecto fijo ponderado por precisión; Kangasharju 2008 (VERIFICADA) y Hyslop y Rea 2018 (VERIFICADA) quedan fuera por falta de error típico en la ficha. Con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera en la simulación, de modo que el intervalo no es un IC95 fiable. Esta magnitud está dominada por el estudio más preciso y no sustituye a la lectura de V17, que usó la mediana de la traslación de siete u ocho estudios con una cifra por estudio: 46,0 % (rango 3,6 a 78,0) con siete estudios y 54,7 % con ocho. La composición de estudios es distinta y la discrepancia se declara.

### 4.5 Oferta y suelo (E5)

**Original (literatura).** Saiz (2010, Quarterly Journal of Economics): elasticidades de oferta por área metropolitana con restricciones geográficas (solo resumen en la ficha; sin paquete). Baum-Snow y Han (DISCREPANTE, versión de trabajo): elasticidades por choques de demanda laboral; solo código. Taltavull (2006; NO VERIFICADA): comunidades autónomas españolas, 1990-2004. Paciorek (2012; VERIFICADA).

**Reproducción.** Ninguna: el paquete de Baum-Snow y Han no cabe en el disco y el resto no tiene paquete.

**Réplica (estimación propia V18).** E5-R1, elasticidad de las viviendas libres iniciadas respecto al valor tasado real, con un Bartik de empleo de cuatro ramas en provincias, 2002-2023: NO ESTIMABLE, y no se publica ningún coeficiente. El F efectivo de la primera etapa es 0,032 en toda la ventana (6,6 en 2002-2007, 0,00179 en 2008-2013 y 0,182 en 2014-2023), y el número efectivo de choques es 3,3. La interacción del instrumento de inmigración con los solares por vivienda (E5-A1) da 0,00244, con IC95 que incluye el cero y una magnitud mínima detectable de 0,0134. Clase ASOCIACIÓN. No se usa la Red Natura como instrumento, porque ya falló en Q4.

**Ampliación.** Las restricciones físicas (pendiente, costa, agua) y de planeamiento (SIU) no están en el repositorio (tarea 5 del autor); la elasticidad tipo Saiz no se estima. La elasticidad de la oferta de F3 se resume en 4.11.

**Magnitud preferida.** No hay: estudios de España, EE. UU. (3 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo)). Rango de las tres priors: -0,20 a 1,5 (elasticidad precio de la oferta, literatura). Entran Taltavull 2006 (NO VERIFICADA), Baum-Snow y Han (DISCREPANTE) y Paciorek 2012 (VERIFICADA). La heterogeneidad es alta y el intervalo de predicción cambia de signo. El Informe Anual 2025 del Banco de España usa una elasticidad de oferta como cota superior, que es de otro orden de incertidumbre y no se usa en la contabilidad.

### 4.6 Obra nueva y alquileres cercanos (E6)

**Original (literatura).** Mense (2025), Journal of Political Economy Macroeconomics (VERIFICADA): elasticidad del alquiler respecto a la oferta nueva, con un instrumento de lluvia, en Alemania. Asquith, Mast y Reed (2020; DISCREPANTE, versión de trabajo): alquileres cerca de edificios nuevos, en Estados Unidos.

**Reproducción.** Con el paquete de Mense (CC0, con datos): coincide con lo publicado (anexo B). Asquith, Mast y Reed solo tiene código.

**Réplica (estimación propia V18).** E6-R1 (cohortes de edificios terminados en 2015-2018 en la provincia de València; secciones contiguas; antigüedad del Catastro INSPIRE y SERPAVI): NO ESTIMABLE por variación; la magnitud mínima detectable es 0,0623, un poco por encima del umbral de la adenda. Se aplica la regla y no el matiz. E6-A1 (edificios mayores, anillo menor): 0 secciones tratadas, frente al mínimo del plan, NO ESTIMABLE por datos. La réplica de Mense (E6-R2) necesita la lluvia de AEMET, que no está en el repositorio. Fuera de la provincia de València, la descarga masiva del Catastro no está disponible (tarea 1 del autor).

**Magnitud preferida (literatura, un solo estudio).** −0,192 en elasticidad del alquiler respecto a la oferta nueva (% por 1 %), clase de la estimación propia designada NO ESTIMABLE. estudios de Alemania (1 estudios con error típico en la unidad (un solo estudio en la unidad); estado B5: magnitud de un solo estudio). Procede de Mense 2025 (VERIFICADA). Asquith, Mast y Reed quedan fuera por otra unidad y no se combinan. La ilustración de V17 con esta elasticidad da -0,50 % del alquiler medio al cerrar el déficit (rango -0,63 a -0,37); es un orden de magnitud, no una estimación.

### 4.7 Tipos de interés (E7)

**Original (literatura).** San Juan (2023), Banco de España (VERIFICADA): BVAR con identificación recursiva; intervalos al 68 % solo en un gráfico, sin error típico numérico. BCE, Boletín Económico 6/2022 (NO VERIFICADA): proyecciones locales. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan las sorpresas monetarias, que se usan como dato.

**Reproducción.** No hay paquete con las series del Banco de España; las sorpresas se usan como dato y no se reproducen.

**Réplica (estimaciones propias V18, nacionales).**

- E7-R1, proyección local con instrumento, ocho trimestres, valor tasado, 1999T1-2024T2: 2SLS de 1,28 % del precio por +100 pb. El conjunto de Anderson-Rubin es toda la recta, la primera etapa tiene signo contrario al esperado y el F efectivo es bajo. Clase NO ESTIMABLE. Repite la debilidad ya vista en V8 y V16. La proyección local con Newey-West es NO APTA en el Monte Carlo y se publica con esa etiqueta.
- E7-R2, SVAR con proxy: −10,5. Clase NO ESTIMABLE (primera etapa débil; Anderson-Rubin no acotado; herramienta NO APTA).
- E7-R3, BVAR recursivo (réplica de San Juan, 2008T1-2022T4): a ocho trimestres de +100 pb del euríbor, el precio responde −1,55 %, con banda del 68 % de -2,3 a -0,87. Clase ASOCIACIÓN. Se publica solo como informativa, porque el Monte Carlo del BVAR es NO APTO (bandas conservadoras o con cobertura distinta de la nominal). La ampliación a 2026T2 (E7-A1) da −0,321 %, con banda del 68 % de -1,9 a 1,2, que incluye el cero.
- Panel provincial (E7-A2), respuesta relativa entre provincias a la sorpresa por la exposición hipotecaria: −19,7, sin el componente común. Clase NO ESTIMABLE.

**Comparación.** San Juan estima una caída del precio a ocho trimestres menor que la del BCE, en el extremo menos negativo del rango de la literatura, con otra unidad (el choque al tipo hipotecario, no al euríbor). E7-R3 coincide en el signo; la etiqueta I6 de E7-R1 es «no coherente». V17 calibró con las elasticidades de la zona euro un efecto de -11,4 % del precio (rango -22,6 a -11,4) para una subida de 2,5 puntos del tipo de las hipotecas nuevas entre 2021T4 y 2023T3. Es una calibración, no una estimación para España, y V18 no la sustituye.

**Magnitud preferida.** No hay: literatura sin estudios con error típico en la unidad (0 estudios con error típico en la unidad (sin estudios con error típico en la unidad); estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico)). Rango de la literatura sin error típico, de -5,0 a -2,0 % del precio por +100 pb del tipo hipotecario a ocho trimestres. San Juan 2023 (VERIFICADA) y el BCE (NO VERIFICADA) no entran en el metaanálisis por falta de error típico.

### 4.8 Fiscalidad de la compra (E8)

**Original (literatura).** Best y Kleven (2018) y Besley, Meads y Surico (2014): impuestos de transmisión en el Reino Unido, con datos fiscales administrativos; sin paquete. Dölls et al. (2020; VERIFICADA): precio de la vivienda frente al tipo del impuesto de transmisión. No se conoce una evaluación española del ITP con diseño; esta sería la primera, con las reservas de la clasificación.

**Reproducción.** Ninguna.

**Réplica (estimación propia V18).** E8-R1, diferencias en diferencias de dosis continua con el tipo general del ITP por comunidad sobre el logaritmo del valor tasado provincial, respuesta acumulada a cuatro trimestres: 0,0146 por punto del tipo general, con IC95 por inversión de la aleatorización de los calendarios que excluye el cero. Clase ASOCIACIÓN, capa C4. Muestra: 30 provincias con valor tasado trimestral de 7 comunidades de régimen común no selladas (sin Cantabria: no hay serie provincial completa), 2007T1-2026T2. La réplica ciega coincide. Tiene signo contrario al de la referencia (etiqueta I6: no coherente) y, sin los años 2012-2013, el signo cambia: el calendario de cambios se concentra en la crisis y el diseño no separa el tipo del ciclo. Un cambio de signo en una prueba del plan es un fallo decisivo (K7). Las fechas de entrada en vigor proceden de memorias de Hacienda y no están contrastadas con el BOE. La coprincipal Q6-p de V16, reproducida en la muestra V18, se mantiene sin clasificar. El volumen de compraventas (E8-R2, MDE 0,0894 por punto) y la ampliación municipal (E8-A2, MDE 0,216 por punto) son NO ESTIMABLES por variación. El análisis de recaudación y de agrupamiento en umbrales no tiene datos.

**Inferencia.** Con ocho comunidades solo la aleatorización del calendario es apta en el Monte Carlo; Webb y el t de Student con pocos clusters no lo son.

**Magnitud preferida.** No hay: literatura sin estudios con error típico en la unidad (0 estudios con error típico en la unidad (sin estudios con error típico en la unidad); estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico)). Rango de la literatura sin error típico, de -3,5 a -3,0 % de precio por +1 pp del ITP a doce meses (estudio de referencia: Dölls et al. 2020, VERIFICADA).

### 4.9 Compradores no residentes (E9)

**Original (literatura).** Badarinza y Ramadorai (2018): choques en los países de origen y precios por barrios de Londres. Cvijanović y Spaenjers (2021): París, magnitud pequeña y no significativa. Sá (2016; VERIFICADA): documento del Centre for Macroeconomics de la London School of Economics, con instrumento. Álvarez, Blanco y García-Posada (2020; NO VERIFICADA): regresión de corte transversal para España, sin instrumento. Ninguno tiene paquete.

**Réplica (estimación propia V18).** E9 es NO ESTIMABLE por choques efectivos. Con la exposición del padrón de 2003 y los ocho orígenes con serie de riesgo, el inverso del índice de Herfindahl es 6,3 sin pesos y 5,9 con pesos de población, por debajo del mínimo de la adenda. Si todos los países del padrón tuvieran serie de riesgo, sería 11,5: el límite son las series de riesgo de los países latinoamericanos, africanos y asiáticos, que no están en el repositorio. El índice de exposición de E9 y el instrumento de E3 se construyen con las mismas cuotas del padrón y están muy correlacionados: no se suman, y E9 va como alternativa de E3 en la contabilidad. El fin de la golden visa como diferencias en diferencias no se estima (sin datos que separen UE de fuera de la UE).

**Contexto descriptivo.** La cuota de compras de no residentes fue 7,4 % de las transacciones entre 2025T2 y 2026T1 (V16). Es un dato descriptivo.

**Magnitud preferida.** No hay: literatura sin estudios con error típico en la unidad (0 estudios con error típico en la unidad (sin estudios con error típico en la unidad); estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico)). Rango de la literatura sin error típico, de 1,4 a 2,1 % de precio por +1 pp de cuota de compras de no residentes (referencia: Sá 2016, VERIFICADA). Álvarez, Blanco y García-Posada no entra por ser una asociación transversal sin instrumento.

### 4.10 Grandes tenedores, viviendas vacías y vivienda pública (E10 a E12)

- **E10, grandes tenedores.** La fase 1 no encontró estudios con datos españoles. La replicación exigiría la entrada de grandes tenedores por zona y la renta de contratos; solo hay tres cortes de titularidad. E10-X1 es NO ESTIMABLE. E10-A1 es una asociación transversal entre el alquiler municipal por m² y el porcentaje de viviendas de grandes tenedores: 1,07 % del alquiler por punto, con IC95 que incluye el cero (muestra: 1365 municipios). En la variación de 2019 a 2024 (E10-A1-d), 0,105. La definición del regresor cambia el resultado: con personas jurídicas (E10-A1-v1), 2,71, con IC95 que excluye el cero. Clase ASOCIACIÓN: sin variación exógena y con el tramo contado dentro del municipio, que da una cota inferior. V17 midió que los titulares de más de diez viviendas tienen el 4,2 % del parque (Catastro, 2026) y entre el 2,2 y el 12,2 % del alquiler habitual con supuestos explícitos. V18 no duplica esas cifras.
- **E11, viviendas vacías.** NO ESTIMABLE (E11-X1): no hay calendario de adopción del recargo del IBI por municipio ni del impuesto catalán, y la vacancia solo tiene dos cortes con métodos distintos, de modo que una diferencia entre cortes confundiría el método con la diferencia buscada. Tarea 12 del autor.
- **E12, vivienda pública.** Solo hay calificaciones de vivienda protegida por provincia, no promociones públicas por municipio y año (tarea 11 del autor). E12-A1, respuesta de las viviendas libres iniciadas a la vivienda protegida calificada con un instrumento provincial: 6,5 viviendas libres por vivienda protegida (ambas por 100 del parque), con conjunto de Anderson-Rubin de -1,2 a 170,0, que incluye el cero. Clase NO ESTIMABLE (magnitud mínima detectable superior a la de referencia). E12-A2, valor tasado real: 22,1 % por cada 100 viviendas protegidas calificadas por 100 del parque, con un conjunto de Anderson-Rubin no acotado. Clase ASOCIACIÓN. Ninguna de las dos mide la vivienda pública.

### 4.11 Modelos de conjunto (F1 a F4)

En ninguno de los contrastes de cointegración de la familia F, con corrección de Holm, se rechaza la ausencia de cointegración. Por la regla AD-F no se publican elasticidades de largo plazo de precio, alquiler u oferta, ni la sobrevaloración (F1-A3), y no se hacen las comparaciones de F4. Solo se publica la dinámica de corto plazo, como ASOCIACIÓN. El resultado coincide con V7.2 y V8-M4 y no cambia ninguna cifra ni conclusión publicada.

- F1, precio frente a renta real de los hogares, trimestral nacional, 1999T1-2026T2: elasticidad de impacto en variaciones de 0,126, con IC95 que incluye el cero (clase ASOCIACIÓN). En el panel provincial con PMG, la elasticidad de corto plazo respecto a la renta per cápita (producto provincial como sustituto) es 0,348, con IC95 que excluye el cero.
- F2, alquiler real frente a renta per cápita, panel provincial con PMG: −0,102, con IC95 que excluye el cero y signo negativo.
- F3, viviendas iniciadas frente al valor tasado real, panel con PMG: 3,52, con IC95 que excluye el cero. Una señal cercana a la cointegración en F3-A2 se declara, sin publicarse como largo plazo.
- El nivel de precio frente a renta que usan los indicadores del Banco de España (V17) es de 8,4 años de renta bruta por hogar en el último dato; V18 no lo replica con elasticidades.

### 4.12 Lectura conjunta

- La única clase superior a la asociación es SUGESTIVO, y corresponde a E2-R1.
- Las etiquetas de coherencia con la literatura (I6) son informativas: E2-R1 es coherente con Jofre-Monseny et al.; E1-R3, E7-R1 y E8-R1 no lo son. No intervienen en la clase.
- Las estimaciones propias con cifra que no son la designada de su factor (por ejemplo, E1-R3, E1-R4 y E3-R1) no entran en la magnitud preferida: son ASOCIACIÓN o NO CONCLUYENTE, o están en otra unidad.
- La coherencia de F4 entre los modelos de conjunto y los factores no puede evaluarse: F no publica elasticidades de largo plazo.


## 5. Contabilidad de la subida por periodo y territorio

La contabilidad calcula, para cada factor con magnitud preferida, el producto de esa magnitud por la variación observada del factor, y deja una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural: no incluye interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Todas las cifras son de capa C4. Los periodos son los del plan: 1995-2007, 2008-2013, 2014-2019, 2020-2022 y 2022-2026.

Regla aplicada (K10). La contabilidad principal admite solo los factores con una estimación propia válida dentro de la magnitud preferida. Ningún factor la cumple, y cada uno dice «sin magnitud» (no cero). Toda la variación observada queda, por construcción, en «no explicado». Las magnitudes de la literatura se muestran en una tabla aparte, rotulada ilustración, que no es una atribución.

### 5.1 Contabilidad por periodo y territorio

**a) Contabilidad principal, nacional.** Variación observada, que es también la parte sin explicar (puntos porcentuales; cien veces la variación del logaritmo del precio real, deflactado con el deflactor del PIB del INE).

| Periodo | Precio real de compra | Alquiler real | Clasificación de la fila |
|---|---|---|---|
| 1995T1-2007T4 | 69,0 | 1,8 (desde 2002T1) | NO ESTIMABLE |
| 2008T1-2013T4 | -36,6 | 6,6 | NO ESTIMABLE |
| 2014T1-2019T4 | 6,3 | -2,9 | NO ESTIMABLE |
| 2020T1-2022T2 | -1,0 | -3,8 | NO ESTIMABLE |
| 2022T3-2026T2 | 14,9 | -6,4 | NO ESTIMABLE |

La variación observada usa el valor tasado del MIVAU y el IPC de alquiler menos el deflactor del PIB del INE, no el IPC general que usó V8: por eso las variaciones de los periodos 2008-2013 y 2022-2026 no coinciden con las de V8. Las provincias selladas de v6 y los municipios de V15 y V16 se excluyen de las series provinciales.

**b) Por comunidad autónoma, precio real de compra.** Variación observada y sin explicar (puntos porcentuales; media de las provincias no selladas de la comunidad, ponderada por población). No suman el total nacional, que incluye las provincias selladas. Cantabria no tiene serie provincial de valor tasado en la base y su comunidad queda fuera.

| Comunidad | 1995T1-2007T4 | 2008T1-2013T4 | 2014T1-2019T4 | 2020T1-2022T2 | 2022T3-2026T2 |
|---|---|---|---|---|---|
| Andalucía | 9,2 | -2,8 | 5,7 | 1,5 | 5,2 |
| Castilla y León | -13,2 | -0,30 | -3,9 | -1,9 | -0,99 |
| Castilla-La Mancha | 2,8 | -9,2 | -2,8 | -0,71 | 2,0 |
| Cataluña | -3,5 | -5,9 | 19,3 | 1,4 | -1,6 |
| Comunitat Valenciana | 37,9 | -6,4 | 8,5 | 3,5 | 12,6 |
| Extremadura | -7,0 | 13,6 | 1,0 | -1,2 | -13,1 |
| Galicia | -1,4 | 6,8 | 0,85 | 1,7 | 1,1 |
| País Vasco | -13,8 | 14,1 | -1,6 | -0,17 | -4,4 |

En todas las filas de esta tabla toda la variación queda sin explicar (clasificación de las filas: NO ESTIMABLE). El alquiler por comunidad está en las mismas condiciones (ids V18-C5-<periodo>-<comunidad>-NOEXPL-A) y en tablas_v18.xlsx, pestaña «contabilidad».

**c) Provincias y grandes ciudades.** El detalle provincial está en output/v18/f5/contabilidad.csv y no entra en cifras_clave: [FALTA CIFRA: variación observada y sin explicar por provincia, periodo y precio o alquiler (output/v18/f5/contabilidad.csv)]. Entre las grandes ciudades solo hay datos no sellados para València y Barcelona; Madrid, Palma, Zaragoza, Murcia y Las Palmas están selladas. Para Barcelona y València solo existen filas de la ilustración (más abajo).

**d) Ilustración con magnitudes de la literatura, nacional, precio real de compra (no es una atribución).** La magnitud es el rango entre los estudios (E3, E7, E8, E9, sin intervalo estadístico), el efecto fijo o el estudio único (E1) y, para Cataluña, la estimación propia E2-R1 sola. La variación observada del factor se toma sin error. Valores: mediana de la contribución en puntos porcentuales e intervalo del 68 % (percentiles 16 y 84 de la propagación por Monte Carlo sobre la magnitud). Los paneles (E3, E9) son «relativos entre provincias, sin el componente común»; solo E7 incluye el componente común. E9 es la alternativa de E3 y no se suman.

| Periodo | Fila | Mediana (pp) | Intervalo 68 % (pp) | Clasificación |
|---|---|---|---|---|
| 1995T1-2007T4 | E3 inmigración | 6,9 | -11,3 a 24,2 | NO ESTIMABLE |
| 1995T1-2007T4 | no explicado | 62,1 | 44,7 a 80,3 | NO ESTIMABLE |
| 2008T1-2013T4 | E3 inmigración | -0,75 | -2,7 a 1,2 | NO ESTIMABLE |
| 2008T1-2013T4 | E7 tipos de interés | 1,1 | 0,70 a 1,6 | NO ESTIMABLE |
| 2008T1-2013T4 | E9 no residentes (alternativa de E3) | 11,2 | 9,2 a 13,2 | NO ESTIMABLE |
| 2008T1-2013T4 | no explicado | -37,0 | -39,1 a -35,1 | NO ESTIMABLE |
| 2008T1-2013T4 | no explicado con E9 en lugar de E3 | -49,0 | -51,1 a -46,9 | NO ESTIMABLE |
| 2014T1-2019T4 | E3 inmigración | 1,0 | -1,7 a 3,6 | NO ESTIMABLE |
| 2014T1-2019T4 | E7 tipos de interés | 0,35 | 0,21 a 0,48 | NO ESTIMABLE |
| 2014T1-2019T4 | E9 no residentes (alternativa de E3) | -4,2 | -5,0 a -3,5 | NO ESTIMABLE |
| 2014T1-2019T4 | no explicado | 5,0 | 2,4 a 7,7 | NO ESTIMABLE |
| 2014T1-2019T4 | no explicado con E9 en lugar de E3 | 10,2 | 9,5 a 11,0 | NO ESTIMABLE |
| 2020T1-2022T2 | E3 inmigración | 0,48 | -0,79 a 1,7 | NO ESTIMABLE |
| 2020T1-2022T2 | E7 tipos de interés | 0,33 | 0,20 a 0,45 | NO ESTIMABLE |
| 2020T1-2022T2 | no explicado | -1,9 | -3,1 a -0,59 | NO ESTIMABLE |
| 2020T1-2022T2 | no explicado con E9 en lugar de E3 | -1,4 | -1,5 a -1,2 | NO ESTIMABLE |
| 2022T3-2026T2 | E3 inmigración | 1,8 | -2,9 a 6,2 | NO ESTIMABLE |
| 2022T3-2026T2 | E7 tipos de interés | 2,9 | 1,8 a 4,0 | NO ESTIMABLE |
| 2022T3-2026T2 | E9 no residentes (alternativa de E3) | -3,3 | -3,9 a -2,7 | NO ESTIMABLE |
| 2022T3-2026T2 | no explicado | 10,2 | 5,6 a 15,0 | NO ESTIMABLE |
| 2022T3-2026T2 | no explicado con E9 en lugar de E3 | 15,3 | 14,0 a 16,7 | NO ESTIMABLE |

Filas sin cifra: E7 en 1995T1-2007T4 (el aumento del tipo queda fuera del horizonte estimado de ocho trimestres, que solo cuenta el cambio de los últimos ocho trimestres de cada periodo) y E9 en 2020T1-2022T2 (fuera del soporte de la variación de la muestra de estimación). E1, E4, E5 y E6 no tienen fila nacional: sus unidades no son comparables con la variación disponible o no hay variación medida.

**e) Cataluña (E2-R1 propia sola) y Barcelona (E1).** En 2020T1-2022T2 el régimen de la Ley 11/2020 no estaba vigente al final del periodo (STC 37/2022; reversión estimada −0,00157): la variación entre extremos del factor es 0 y su contribución a la variación del periodo es nula. Durante la vigencia (2020T4-2022T1), la contribución del factor al nivel medio de la renta de los contratos nuevos en Cataluña (sin Barcelona ciudad), por la cuota de contratos regulados, es de -2,7 pp (mediana; un signo negativo indica una renta menor; intervalo del 68 % de -3,5 a -2,0; clasificación SUGESTIVO). Esta cifra requiere la frase de limitación de la sección 4.2. La variación observada de esos contratos en el periodo es -2,8 pp (la renta es la de contratos nuevos del Incasòl, no el IPC). En 2022T3-2026T2, la zona tensionada de 2024 es otro régimen y no hay magnitud. Barcelona ciudad no estaba en la muestra de E2-R1; su cifra de E1 mide viviendas HUT por 100 viviendas con una magnitud definida por anuncios de Airbnb: contribución de -0,08 pp en 2020T1-2022T2 y de 0,50 pp en 2022T3-2026T2, frente a una variación observada del alquiler de -6,0 y -2,6 pp (clasificación NO ESTIMABLE).

**f) Respuesta explícita: qué factores explican la mayor parte de la subida, con qué confianza, y qué queda sin explicar.**

- *Con respaldo propio:* ninguno, en ningún periodo ni territorio. La contabilidad principal deja toda la variación sin explicar. La confianza es la de la frase «la evidencia no permite concluir».
- *Con magnitudes de la literatura (ilustración):* en el agregado nacional, la contribución en valor absoluto mayor frente a la variación observada es la de E9 en 2014T1-2019T4, de -4,2 pp frente a una variación observada de 6,3 pp. Es de signo opuesto al de la variación observada, procede de un rango de otro país sin error típico y no se suma a E3. Ningún otro factor explica por sí solo la mayor parte de la variación en ningún periodo.
- *Sensibilidad de E2.* Con la estrategia alternativa de Hahn et al. el metaanálisis daría una magnitud preferida. Se publica como sensibilidad y no cambia la tabla principal, porque la regla se fijó antes de combinar. Si se adoptara, E2 entraría con la clase SUGESTIVO como techo, pero su variación entre extremos del periodo 2020-2022 sería nula, porque la norma no estaba vigente al final.
- *Qué queda sin explicar.* La parte común a todas las provincias (el componente común, que los diseños de panel con efectos de periodo no separan de los efectos de año) y la variación de los fundamentales que no se miden aquí (renta y crédito: F1 es ASOCIACIÓN y no entra).

**g) Comparación con V8 y con el Banco de España (sin sumar).**

- *V8* (descomposición histórica del SVAR, capa C3s, bandas del 68 %) no designó ningún factor como el más relevante en ninguno de los casos. Las correspondencias son: demografía con inmigración (E3, E9); crédito y tipos con tipos (E7); oferta con E5 y E6 (sin fila en V18); actividad y renta con F1 (ASOCIACIÓN, no entra). Con cifra en ambos lados (E3 y E7) el signo coincide en la mayoría de las comparaciones y las bandas se solapan en casi todas; las bandas de V8 incluyen el cero casi siempre, por lo que el solape es una prueba débil [FALTA CIFRA: recuento de comparaciones, de coincidencias de signo y de solapes de bandas (output/v18/f5/comparacion_v8.csv)].
- *Banco de España* (referencias de V17 y fichas de la fase 1). (i) Sobrevaloración del precio: es un indicador de nivel frente a fundamentales, con incertidumbre alta entre métodos, que la contabilidad con elasticidades no replica. (ii) Tipos: San Juan (2023) estima una caída del precio a ocho trimestres que cae dentro del rango de B5 para E7, de -5,0 a -2,0 % por +100 pb. (iii) El diferencial entre hogares y viviendas que estima el Banco de España y la parte de déficit asociada a no residentes son contabilidad de cantidades, no de precios. (iv) La elasticidad de oferta del Informe Anual 2025 se cita como cota superior; el rango de E5 de B5 (-0,20 a 1,5) es de otro orden de incertidumbre y no se usa.

**h) Compatibilidad con lo publicado.** No hay parada por contradicción: ninguna estimación propia es IDENTIFICADO. (i) V8 («ningún factor puede designarse»): coherente. (ii) Informe integral III.2 y V17, topes: E2-R1 es compatible con la lectura publicada y añade que la diferencia se reduce durante la vigencia. (iii) V17, inmigración: la elasticidad implícita de 1,3 % cae dentro del rango de B5 para E3 (-0,49 a 3,5). La ilustración asocia a la inmigración 6,9 pp de la variación de 1995T1-2007T4 (intervalo del 68 % de -11,3 a 24,2), con la mediana del rango de la literatura. Es una fracción menor que la que atribuye el estudio de González y Ortega para 2000-2010, que corresponde al extremo alto del rango. Se documenta; no contradice, porque la cifra de V17 es una ilustración. (iv) V17, tipos: el horizonte de ocho trimestres deja fuera del horizonte el aumento de 2022-2023, y en 2022T3-2026T2 solo cuenta la bajada posterior (2,9 pp, de signo contrario). La contabilidad no contradice la afirmación de V17 sobre los tipos; no la contrasta.

**Limitaciones de la contabilidad.** Magnitudes de la literatura, muchas con ficha NO VERIFICADA o solo con resumen, aplicadas a España. E7, E8 y E9 sin error típico. E1 con un solo estudio y unidades que no coinciden con la variación disponible (anuncios de Airbnb frente a registro HUT). E4, E5 y E6 sin variación comparable medida. Turismo anterior a 2018 no medido (no cero). Variación observada sin error. Conversión de porcentajes a logaritmos aproximada y efectos de nivel permanentes para E3, E8 y E9, que en la literatura son a doce meses o promedios del periodo. Ventanas anuales recortadas a los topes de sellado. Desviaciones respecto al plan: deflactor del PIB en lugar del IPC; rangos de la literatura en lugar del posterior de B5 cuando B5 no da magnitud; Cantabria sin serie provincial; E1 y E2 solo en Barcelona y Cataluña.


### 5.2 ¿Problema general o local? (V17)

Análisis a posteriori de V17, capa C4, contable y descriptivo. La pregunta es qué parte de la varianza de la variación anual de los precios y los alquileres corresponde a un componente común a todos los territorios (el efecto año) y qué parte es local (provincia por año). Las cuotas llevan intervalo de confianza al 95 % por bootstrap de provincias y se comparan con una referencia de azar (permutación temporal dentro de cada provincia).

| Serie | Periodo | Cuota del componente común (%) | IC95 (%) |
|---|---|---|---|
| Índice de precios de vivienda (IPV) por comunidad, comunidades no selladas | 2015-2025 | 81,1 | 70,3 a 93,9 |
| Valor tasado del MIVAU por provincia | 2015-2025 | 60,7 | 55,2 a 67,5 |
| Índice de precios de vivienda del INE por provincia (IPVA) | 2015-2024 | 76,9 | 70,4 a 84,6 |
| IPC de alquiler del INE por provincia | 2015-2025 | 64,2 | 59,3 a 71,4 |
| Alquiler mediano en €/m² de SERPAVI por provincia | 2015-2024 | 70,8 | 64,8 a 79,1 |

**Lectura.**

- En compra, el componente común es mayoritario en el conjunto de 2015-2025 en las tres series. Por subperiodos, en el valor tasado y en el IPV por comunidad el componente local pesa más antes de 2020 y el común domina desde 2020; no ocurre así con el IPVA [FALTA CIFRA: cuotas del componente común por subperiodo, 2015-2019 y 2020-2025 (output/v17/d3/varianza_comun_local.csv)].
- En alquiler, el resultado es mixto y menos seguro: las cuotas del componente común son menores y los intervalos más anchos, y en SERPAVI el componente común baja desde 2020.
- En todas las series queda una parte local (provincia por año), de modo que la respuesta no es una u otra. Depende de la serie y del método.
- El déficit está concentrado: 5 provincias suman la mitad del déficit positivo de 2021-2025 y 14 suman el 80 % (41 provincias no selladas).
- Movimientos dentro de la provincia: el saldo acumulado de 2015 a 2024 de las capitales con el resto de su provincia es de -199.029 personas (8 capitales de provincias no selladas); negativo significa que la capital cede residentes a su corona. Solo cubre movimientos entre municipios de una misma provincia y no mide el padrón de la corona.

**Relación con V18.** Los diseños de panel con efectos de periodo (E1, E2, E3, E5, E8, E9, E12) solo recogen la parte local, la que varía entre territorios en el mismo periodo. Por eso las contribuciones por factor de la contabilidad se rotulan «relativas entre provincias, sin el componente común», y la variación común queda fuera de lo que esos diseños pueden asociar a un factor. Es una de las razones de que la fila «no explicado» sea grande.

**Límites.** No hay esfuerzo provincial propio en los datos locales. La cuota depende de la serie, del número de periodos y de los territorios no sellados. Nada de esta sección es una estimación de un efecto.


### 5.3 Demografía (V17)

Análisis a posteriori de V17, capa C4, contable y descriptivo. Los datos locales no contienen los motivos de llegada ni permiten construir un contrafactual, de modo que esta sección no estima efectos.

**Población.** Entre el 1 de enero de 2015 y el 1 de enero de 2026, la población residente creció en 3.170.654 personas. El saldo vegetativo acumulado fue de -896.778 personas (negativo desde 2017; el dato de 2025 es provisional). El resto, 4.067.432 personas, es saldo migratorio exterior neto más ajustes estadísticos, y equivale al 128,3 % del crecimiento. El residuo mezcla el saldo exterior oficial con ajustes (rebase censal de 2021, revisiones, bajas por caducidad). En 2015-2024, el saldo exterior oficial suma 3.757.591 personas, y el residuo menos ese saldo es de -284.056 personas.

**Por lugar de nacimiento.** La población nacida en el extranjero varió en 4.120.690 personas y la nacida en España, en -975.687. Los nacidos en el extranjero equivalen al 130,0 % del crecimiento, más que la totalidad porque la población nacida en España disminuye. El saldo vegetativo de nacionalidad española acumula -1.389.513 personas y el de nacionalidad extranjera, 604.316 (por nacionalidad de la madre y del fallecido, que aproxima el lugar de nacimiento).

**Hogares.** Entre 2021 y 2026 el número de hogares aumentó en 1.222.836. Descomposición contable del cambio (Shapley anual, V16): 858.274 hogares corresponden al tamaño de la población, 473.045 a la estructura por edad (envejecimiento) y -11.510 a la jefatura (residuo; tamaño medio del hogar). Si los nacidos en el extranjero forman hogares como el resto, entre 724.785 y 858.274 hogares del componente de población corresponden a su crecimiento (valor central 791.530). Es una cota de contabilidad, no un efecto.

**Tenencia (Censo 2021, muestra del hogar con persona de mayor edad de referencia).** Viven en alquiler el 36,8 % de los hogares cuya persona de mayor edad nació en el extranjero y el 11,5 % de los de persona nacida en España. En propiedad viven el 50,6 % y el 80,5 %, respectivamente.

**Relación con E3 y E9.** La contabilidad de población no es una estimación del efecto de la inmigración sobre los precios, que es la pregunta de E3. Un aumento de población se asocia con más hogares sea cual sea su origen, y no hay evidencia de que un hogar inmigrante presione más que otro equivalente. E3-R1 es NO CONCLUYENTE y la magnitud preferida de E3 no existe (sección 4.3). Por eso V17 mantuvo la calificación «engañosa» para la afirmación que atribuye la subida a la inmigración: ni la contabilidad ni la literatura permiten fijar una magnitud.

**Límites.** La población del Padrón continuo es provisional y se revisa cada trimestre; el dato de 2025 mezcla ediciones. El saldo vegetativo aproxima el lugar de nacimiento por la nacionalidad. No hay tasa de jefatura por edad posterior a 2021. Las cifras de V5 sobre el conjunto de provincias se citan solo como publicadas.


## 6. Implicaciones para las políticas

Esta sección dice qué cambia, con los resultados de V18, en la tabla de medidas y en la de discurso público auditadas en V17. Se evalúan instrumentos y afirmaciones, nunca a quien los propone. No contiene recomendaciones: dice qué se puede y qué no se puede afirmar de cada instrumento con la evidencia disponible, y qué dato permitiría afirmar más.

**Resultado: no cambia ningún veredicto de V17.** Las razones son cuatro.

1. Ninguna estimación propia de V18 es IDENTIFICADO. Ninguna cifra V18 pasa de la capa C4, y la auditoría de V17 ya se apoyaba en la literatura y en datos descriptivos con esa misma capa.
2. La única estimación de clase SUGESTIVO, la de los topes al alquiler en Cataluña (E2-R1), es compatible con lo que V17 ya decía sobre la renta de los contratos regulados. Añade un matiz: la diferencia se reduce durante la vigencia de la norma y no se separa de otros choques de la época.
3. Las demás estimaciones propias son ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE. No tienen potencia o diseño para sostener ni para refutar una afirmación. Donde V17 escribió «la evidencia no permite concluir» o «no está medido», V18 confirma que sigue sin estar medido con un diseño que supere las pruebas.
4. Las magnitudes preferidas de V18 son de la literatura (E1, E4, E6) o rangos sin error típico (E7, E8, E9), y V17 ya había usado esa misma literatura. La combinación formal no altera la lectura.

**Qué sí cambia: la precisión de algunas formulaciones.** Donde V17 dice «en España no se ha medido» (ITP, ayudas, vivienda pública), el enunciado exacto pasa a ser «no se ha medido con un diseño que supere las pruebas; hay una estimación exploratoria de clase ASOCIACIÓN o NO ESTIMABLE». No es un cambio de veredicto y no modifica ninguna cifra publicada, de modo que no genera entrada en ERRATA.md.

**Qué evidencia haría falta para cada instrumento.** Es la lista de datos de la sección 7. En resumen: las ayudas, los topes y la regulación turística se podrían evaluar con registros de contratos y de beneficiarios con fecha y renta anterior; la oferta, la obra nueva y las vacías, con el Catastro y los calendarios de impuestos locales; los tipos y los no residentes, con compras por nacionalidad y al contado.


### 6.1 Factibilidad de construir (V17)

Análisis a posteriori de V17, capa C4, contable y con supuestos explícitos; no es una predicción.

**Producción.** Se terminaron 83.700 viviendas al año de media en 2024-2025, frente a 568.684 en 2005-2007. Para cerrar el déficit inicial y absorber los hogares nuevos y la reposición hacen falta 293.623 viviendas al año en cinco años (rango por déficit inicial: 257.188 a 330.057) o 223.045 en diez años (204.828 a 241.262). Frente a la producción actual, la necesidad es de 2,8 a 4,4 veces a cinco años y de 2,2 a 3,5 veces a diez años. El déficit de 2021-2025 equivale al 2,7 % del parque de viviendas familiares. Supuestos: producción necesaria igual al déficit entre los años más los hogares nuevos de la proyección del INE y la reposición, sin restar las viviendas liberadas por envejecimiento.

**Capacidad.** Los ocupados en construcción eran 1.498 miles en 2025, frente a 2.703 miles en 2007. Las viviendas terminadas por ocupado fueron 0,05 en 2025 y 0,21 en 2007. El índice real del coste de la mano de obra en construcción en 2025 es de 1,0 respecto a 2007. Con supuestos de productividad (juicio experto), pasar a la producción necesaria a cinco años exigiría entre 208,0 y 1.615 miles de ocupados adicionales (central 648,6), y a diez años, entre 142,1 y 1.033 miles.

**Suelo.** No hay Sistema de Información Urbana por provincia en los datos locales. El potencial que cita el Banco de España para las seis grandes áreas urbanas es de 1.100.000 viviendas (cifra de documento). En el área de Barcelona, el potencial equivale a 0,39 de la necesidad provincial a diez años (rango 0,29 a 0,51): el suelo previsto no basta, y ahí es un freno. En el resto de las grandes ciudades no se puede saber con los datos disponibles. Los plazos de licencias y de transporte a coronas no tienen datos oficiales locales.

**Qué aporta V18.** Los factores de oferta no tienen estimación propia: E5 (elasticidad de la oferta con Bartik) y E6 (obra nueva y alquileres cercanos) son NO ESTIMABLES (sección 4). La única magnitud de V18 que enlaza con esta sección es la de E6, que procede de un estudio de la literatura (Mense 2025, VERIFICADA): −0,192 de elasticidad del alquiler respecto a la oferta nueva. Con ella, la ilustración de V17 al cerrar el déficit da -0,50 % del alquiler medio (rango -0,63 a -0,37), que es un orden de magnitud y no una estimación para España. El veredicto de V17 sobre más oferta no cambia.


### 6.2 Medidas auditadas en V17: qué cambia

Son las filas de los grupos «Regulación y ayudas» y «Oferta y titularidad» de la tabla final de V17 (output/v17/auditoria/tabla_final.md). El veredicto de V17 es sobre el enunciado original de cada fila. La última columna dice si V18 cambia ese veredicto.

| Medida | Veredicto de V17 | Aporte de V18 (clase, capa C4) | ¿Cambia? |
|---|---|---|---|
| Ayudas a la demanda (bono joven, avales) | incorrecta (el enunciado «sin evidencia») | E4 sin estimación propia (NO ESTIMABLE). Magnitud solo de la literatura, θ = 0,0408, con dos estudios | No |
| Regulación de la renta de los contratos nuevos (topes) | engañosa | E2-R1 (SUGESTIVO): diferencia de −0,0384 en logaritmos de la renta, que se reduce durante la vigencia. E2-R1c, contratos (ASOCIACIÓN): sin diferencia detectable | No |
| Regulación de la vivienda turística | se sostiene con matices | E1-R3 (ASOCIACIÓN) y E1-R4 (NO CONCLUYENTE); sin evaluación de ninguna norma local sobre el alquiler | No |
| Grandes tenedores | incorrecta (el enunciado «no hay datos») | E10-A1 (ASOCIACIÓN): asociación municipal sin variación exógena; el efecto en precios sigue sin medirse | No |
| Rebajar el ITP (medida y discurso) | se sostiene con matices | E8-R1 (ASOCIACIÓN): signo contrario a la literatura y dependiente de 2012-2013; E8-R2 (NO ESTIMABLE) | No |
| Más oferta donde hay presión | se sostiene con matices | E5-R1 (NO ESTIMABLE) y E6-R1 (NO ESTIMABLE); magnitud de E6 solo de la literatura (−0,192, un estudio) | No |
| Movilizar vivienda vacía | se sostiene con matices | E11-X1, NO ESTIMABLE: sin calendario de recargos no hay estimación | No |
| Vivienda pública o social | se sostiene con matices | E12-A1 (NO ESTIMABLE) y E12-A2 (ASOCIACIÓN) miden vivienda protegida, no pública | No |

**Notas por fila.**

- *Ayudas.* La traslación mediana de las ayudas al alquiler a la renta en los estudios con diseño es de 46,0 % de la ayuda (rango 3,6 a 78,0 entre estudios); con sensibilidad de composición, 54,7 % (de 41,0 a 65,0). La magnitud de B5 es distinta porque solo incluye dos estudios con error típico en la misma unidad; no sustituye a la cifra de V17 y la discrepancia se declara (sección 4.4). Ningún estudio es español, y el bono dura menos que el contrato: el umbral de traslación a partir del cual el perceptor pierde en el contrato es de 40,0 %.
- *Topes.* La renta de los contratos regulados es menor en E2-R1, del mismo orden que el rango de V17 (-5,8 %). Que la cantidad de contratos baje sigue en disputa en la literatura, y E2-R1c no la resuelve. La coprincipal con otro grupo de control da una diferencia mayor, de modo que la magnitud depende del control (anexo D).
- *ITP.* El enunciado exacto pasa a «no se ha medido con un diseño que supere las pruebas». La estimación de V18 es una asociación con signo contrario al de la literatura internacional y no sostiene ni refuta el veredicto. Las fechas de los cambios no están contrastadas con el BOE.
- *Grandes tenedores.* V17 situó a los titulares de más de diez viviendas en el 4,2 % del parque y, con supuestos, entre el 2,2 y el 12,2 % del alquiler habitual; en Barcelona ciudad, el 36,1 % del alquiler habitual en 2021. V18 no añade cifras de peso. Sobre el efecto en el alquiler, la asociación municipal de E10-A1 no es concluyente y depende de la definición del regresor.
- *Más oferta, vacías y vivienda pública.* V17 cifró el tamaño de la tarea (sección 6.1) y V18 no la modifica.

**Qué puede decirse hoy de cada medida.** Para las ayudas, los topes, el ITP, la oferta, las vacías y la vivienda pública, la evidencia con diseño de España es escasa o nula y la de otros países es heterogénea. Esta es una afirmación sobre la evidencia y no sobre la conveniencia de la medida.


### 6.3 Discurso público auditado en V17: qué cambia

Son las afirmaciones del grupo «Demanda y precios» de la tabla final de V17. El veredicto se emite sobre la afirmación, nunca sobre quien la formula. La última columna dice si V18 lo cambia.

| Afirmación | Veredicto de V17 | Cifras de V17 y aporte de V18 (clase, capa C4) | ¿Cambia? |
|---|---|---|---|
| «Hay burbuja» o «no hay burbuja» | engañosa | Variación del precio sobre la renta bruta por hogar frente a 2007: -10,7 %; variación del saldo de crédito sobre el PIB frente a 2007: -28,8 puntos. V18: los modelos F1 a F3 no rechazan la ausencia de cointegración y no publican sobrevaloración; la dinámica de corto plazo es ASOCIACIÓN (F1-R1: ASOCIACIÓN) | No |
| La inmigración como explicación de la subida | engañosa | La población crece por el saldo migratorio (el residuo es el 128,3 % del crecimiento) y los hogares en alquiler cuya persona de mayor edad nació en el extranjero son el 33,2 % del total. V18: E3-R1 (NO CONCLUYENTE) y E3 sin magnitud preferida | No |
| Los pisos turísticos como explicación de la subida | engañosa | El aumento de 2020-2024 equivale al 2,7 % del parque de alquiler y el stock de mayo de 2026, al 11,5 %; en el percentil 90 de las secciones, el 33,9 %. V18: E1-R3 (ASOCIACIÓN) y E1-R4 (NO CONCLUYENTE) | No |
| «El alquiler ha subido un X %» | se sostiene con matices | La renta media de los contratos nuevos en Cataluña, ponderada por contratos (Incasòl, 2019-2025), varió 20,0 %; el IPC de alquiler deflactado por la renta por hogar, -13,9 %. V18 no añade estimaciones sobre esta pregunta | No |
| «El precio ha subido un X %» | se sostiene con matices | El IPV deflactado por la renta por hogar varió 12,9 % en 2019-2025. V18 no añade estimaciones | No |
| «Con los tipos altos bajarán los precios» | se sostiene con matices | El IPV subió 22,3 % entre 2021T4 y 2024T4. V18: E7-R1 (NO ESTIMABLE) y E7-R3 (ASOCIACIÓN); el rango de la literatura es de -5,0 a -2,0 % por +100 pb | No |

**Por qué no cambian.**

- *Burbuja.* V17 concluía que ninguna de las dos afirmaciones se puede sostener. V18 no aporta un indicador de nivel nuevo, y los modelos de largo plazo no se publican por falta de cointegración. La sobrevaloración que cita V17 es la del Banco de España.
- *Inmigración.* V17 separaba la contabilidad de la población (que V18 no toca) del efecto sobre el precio (que V18 tampoco logra medir: E3-R1 es NO CONCLUYENTE y las demás especificaciones, NO ESTIMABLES). La afirmación sigue sin base para atribuir la subida a un grupo concreto, y también sin base para negar que un aumento de población se asocie con más demanda.
- *Turísticos.* Los datos permiten una asociación débil en Barcelona y nada concluyente fuera de ella. V17 limitaba el efecto local a los barrios muy expuestos y V18 no lo desmiente ni lo confirma.
- *Alquiler y precio.* Son preguntas de definición y medida (contratos vigentes o nuevos, nominal o real, territorio). V18 no estima nada sobre ellas.
- *Tipos.* El hecho de que los precios subieran con los tipos (2022-2024) es descriptivo y V18 no puede contrastarlo: la proyección local con instrumento es NO ESTIMABLE por primera etapa débil, y el BVAR es informativo, con herramienta NO APTA.

**Lo que dicen las preguntas D3 de V17 con V18.** Población: crece por la migración neta (sección 5.3). ¿General o local?: común en compra, mixto en alquiler (sección 5.2). ¿Factible construir?: la necesidad supera varias veces la producción actual (sección 6.1). Qué no sabemos: el efecto en España de casi todas las medidas, que es también el resultado de V18.


## 7. Limitaciones y qué datos las resolverían

### 7.1 Limitaciones generales

- **Capa y evaluación.** Toda cifra V18 es de capa C4 y ninguna ha pasado una evaluación en muestra sellada. La vía a una capa superior es la evaluación sellada diferida (evaluate_v18), que se abriría con datos posteriores al tope de entrenamiento y no antes de 2027. Las hipótesis fijadas para esa evaluación (E1-A1, E2-A1, E3-A1, E3-A2, E3-A3, E5-R1 y E6-R2) solo se evalúan si en entrenamiento quedan IDENTIFICADO. Hoy ninguna lo es, de modo que ninguna se evaluaría. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015-2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.
- **Pre-registro interno.** El plan y la adenda no tienen sello de tiempo externo, y casi todos los factores se habían estimado antes con estos datos: las réplicas no son primeras miradas. Parte de la evidencia de V18 es a posteriori (anexo F).
- **Potencia.** La mayoría de las ampliaciones son NO ESTIMABLES porque la magnitud mínima detectable supera la magnitud de la literatura o el número efectivo de choques es insuficiente. Un resultado NO ESTIMABLE no es un resultado nulo.
- **Literatura.** Muchas fichas son «solo resumen», NO VERIFICADAS o DISCREPANTES (la ficha describe una versión de trabajo y el DOI corresponde a la publicada), y el cuartil de las revistas no está verificado. La búsqueda sistemática adicional con OpenAlex quedó incompleta por agotarse la cuota, y está pendiente. Las magnitudes de otros países se aplican a España con unidades que no siempre coinciden. Para los tipos de interés (E7) no hay estudios con error típico en la unidad: la literatura da un rango de -5,0 a -2,0 % del precio por +100 pb del tipo hipotecario, a 8 trimestres.
- **Herramientas.** El BVAR, la proyección local con Newey-West, el SVAR con proxy y el metaanálisis bayesiano son NO APTOS en el Monte Carlo, y la herramienta de Honest DiD es apta solo sin desviación de tendencias paralelas. Sus resultados se publican con esa etiqueta.
- **Sellado y muestra.** Las comunidades y provincias selladas de v6 (entre ellas Madrid, Baleares y Canarias) y los bloques de V15 y V16 quedan fuera. Las ciudades con más presión turística y de alquiler no están en la muestra, salvo Barcelona con tres distritos menos.
- **Medidas.** El precio se mide con el valor tasado, el IPV por comunidad o el IPVA; el alquiler, con SERPAVI, el IPC de alquiler o los contratos nuevos del Incasòl (solo Cataluña). No son equivalentes.
- **Contabilidad.** Es contabilidad con elasticidades estimadas, sin interacciones ni efectos de equilibrio general. La variación observada no tiene error. Las contribuciones de los paneles son relativas entre territorios.
- **Fechas del ITP.** Proceden de memorias de Hacienda y no están contrastadas con el BOE.

### 7.2 Qué falta por factor y qué dato lo resolvería

La tercera columna cita, cuando existe, la tarea correspondiente de docs/v18/tareas_autor.md.

| Factor | Qué falta | Dato que lo resolvería |
|---|---|---|
| E1 Turismo | Más barrios con cambio de stock; primera etapa del IV; zonas y fechas de la regulación local | Microdatos de portales; geometría del PEUAT y fechas de moratorias; Inside Airbnb anterior a 2025-12 |
| E2 Topes | Renta anterior, superficie y tipo de contrato; tramo de renta; más trimestres posteriores en las zonas de 2024; desvío a temporada | Microdatos de fianzas con renta anterior y registros de otras comunidades; Registro Único de Arrendamientos |
| E3 Inmigración | Variación suficiente para detectar la magnitud de la literatura; Censo de 1991 y más grupos de origen | Series de nacionalidad más finas por provincia; ventanas más largas con datos posteriores |
| E4 Ayudas | Cualquier estimación propia | Microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas |
| E5 Oferta y suelo | Restricciones físicas y de planeamiento; primera etapa del Bartik | Sistema de Información Urbana, modelo digital del terreno, costa y agua; descarga masiva del Catastro |
| E6 Obra nueva | Edificios nuevos fuera de la provincia de València; lluvia de AEMET | Descarga masiva del Catastro; lluvia de AEMET |
| E7 Tipos | Primera etapa fuerte; exposición hipotecaria; saldo de préstamos | Licencia de EA-MPD; Encuesta Financiera de las Familias; saldo de préstamos del Banco de España; compraventas anteriores a 2007 |
| E8 Fiscalidad | Fechas verificadas; recaudación; compraventas por tramo | BOE y diarios autonómicos; compras por tramo de precio (Notariado) |
| E9 No residentes | Series de riesgo de más países de origen; compras por nacionalidad y provincia | Notariado y Registradores por nacionalidad y provincia; autorizaciones de golden visa |
| E10 Grandes tenedores | Serie homogénea de titularidad y entrada por zona | Serie del Catastro por tramo de titular, municipio y año; Panel de Hogares AEAT-IEF |
| E11 Vacías | Calendario del recargo del IBI y del impuesto catalán | Ordenanzas fiscales por municipio; calendario de la Ley catalana de vacías; serie anual de vacancia |
| E12 Vivienda pública | Promociones públicas por municipio y año | MIVAU, CASA 47 y empresas públicas autonómicas, por transparencia |
| F1 a F3 | Cointegración detectable con series más largas | Más años de datos y la Encuesta Financiera de las Familias |

### 7.3 Tareas pendientes del autor que no bloquean el documento

- Subir la etiqueta plan-replicacion-v18 al remoto desde su ordenador (el commit ya está en la rama remota).
- Descargar la tabla de Scimago para verificar los cuartiles.
- Repetir la búsqueda sistemática con OpenAlex cuando se restablezca la cuota.
- Autorizar `sellar_v18` y `evaluate_v18` en una versión posterior, cuando existan los datos mínimos.

### 7.4 Qué no cambia

Ninguna cifra publicada cambia de valor ni de capa por V18. No hay parada por contradicción con una conclusión publicada, porque ninguna estimación propia es IDENTIFICADO.


## Anexo A. Fichas bibliográficas

La fase 1 fijó los criterios antes de buscar (docs/v18/bib/criterios.md): diseño cuasi experimental o estructural, datos de España o de mercados europeos comparables, y publicación en revista con revisión, documento de banco central o serie reconocida de documentos de trabajo. Se hizo una ficha por estudio, agrupadas por factor (docs/v18/bib/<factor>/), con una tabla de efectos y su unidad. El catálogo está en output/v18/f1/catalogo.csv. [FALTA CIFRA: recuentos del catálogo (fichas, texto completo, solo resumen, con paquete de replicación; VERIFICADA, NO VERIFICADA y DISCREPANTE) en output/v18/f1/informe.md]

Los PDF y los paquetes de replicación están solo en disco, con sha256 en data/bib/CHECKSUMS.sha256, y no se versionan. Al repositorio van la ficha, el enlace, el DOI, la licencia y las notas, con citas breves. Estado: VERIFICADA es DOI comprobado con Crossref o DataCite; el cuartil de Scimago no está verificado (tarea del autor). DISCREPANTE es una ficha de versión de trabajo cuyo DOI corresponde a la versión publicada (otro año o título), y se trata como NO VERIFICADA. No se cita ninguna cifra de la versión publicada sin leerla.

Estudios con error típico en la unidad para inmigración (E3): estudios de España, EE. UU., Reino Unido, Alemania (5 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo)).

**Referencias de la magnitud preferida y de la etiqueta I6.**

| Factor | Estudio | Estado de la ficha | ¿Entra en la magnitud preferida? Motivo |
|---|---|---|---|
| E1 | Segú (2018) | NO VERIFICADA | Sí (único estudio) |
| E1 | Garcia-López et al. (2020) | VERIFICADA | No: unidad no convertible (por 100 anuncios en el área estadística básica) |
| E1 | Chaves-Fonseca (2026) | VERIFICADA | No: unidad no convertible (por 100 anuncios, sobre el precio de compra) |
| E1 | Duso et al. (2024) | VERIFICADA | No: unidad no convertible (€/m² por anuncio en un radio) |
| E2 | Jofre-Monseny et al. (2023) | VERIFICADA | Sí |
| E2 | Monràs y García-Montalvo (2023) | VERIFICADA | Sí (peso nulo al contar una vez el episodio compartido) |
| E2 | Breuille et al. (2025) | NO VERIFICADA | Sí |
| E2 | Hahn et al. (2021) | VERIFICADA | Sí |
| E2 | Pérez García (2026) | VERIFICADA | No: otro régimen (zonas de 2024), otra unidad y sin pretendencias paralelas |
| E2 | Abel (2024) | NO VERIFICADA | No: mide la oferta |
| E3 | González y Ortega (IZA, 2009) | NO VERIFICADA | Sí (versión que da la unidad) |
| E3 | González y Ortega (Chicago Fed, 2011) | NO VERIFICADA | No: misma obra; entra en la sensibilidad |
| E3 | Sanchis-Guarner (2017) | DISCREPANTE | Sí |
| E3 | Saiz (2007) | VERIFICADA | Sí |
| E3 | Sá (2015) | VERIFICADA | Sí |
| E3 | Ünal (2022) | NO VERIFICADA | Sí |
| E3 | Accetturo (2012) | DISCREPANTE | No: elasticidad respecto a la población extranjera, no a la total |
| E3 | Torres y Montero (2023) | VERIFICADA | No: sin error típico |
| E4 | Fack (2005) | VERIFICADA | Sí |
| E4 | Eerola et al. (2026) | VERIFICADA | Sí |
| E4 | Kangasharju (2008) | VERIFICADA | No: sin error típico |
| E4 | Hyslop y Rea (2018) | VERIFICADA | No: sin error típico |
| E5 | Taltavull (2006) | NO VERIFICADA | Sí |
| E5 | Baum-Snow y Han (versión de trabajo) | DISCREPANTE | Sí |
| E5 | Paciorek (2012) | VERIFICADA | Sí |
| E6 | Mense (2025) | VERIFICADA | Sí (único estudio) |
| E6 | Asquith, Mast y Reed (2020) | DISCREPANTE | No: otra unidad |
| E7 | San Juan (2023) | VERIFICADA | No: intervalos solo en un gráfico |
| E7 | BCE, Boletín Económico 6/2022 | NO VERIFICADA | No: sin error típico |
| E8 | Dölls et al. (2020) | VERIFICADA | No: sin error típico recuperado |
| E9 | Sá (2016) | VERIFICADA | No: sin error típico extraído |
| E9 | Álvarez, Blanco y García-Posada (2020) | NO VERIFICADA | No: regresión transversal sin instrumento |

Los valores por estudio están en output/v18/f5/magnitudes_estudios.csv y no en cifras_clave (véase la sección 4).

## Anexo B. Reproducciones

La fase 2 reproduce con el paquete de su autor, y sin datos del proyecto, los estudios que lo tienen abierto. El veredicto es «coincide» (la misma cifra al redondeo publicado, o una diferencia menor que la fijada en el plan y dentro del error), «difiere con explicación» o «difiere sin explicación» (parada). Ninguna reproducción difiere sin explicación. [FALTA CIFRA: coeficientes e intervalos reproducidos y publicados de las tres reproducciones (output/v18/reproduccion/*/informe.md y docs/v18/reproduccion.md)]

| Estudio | Método reproducido | Veredicto |
|---|---|---|
| Chaves-Fonseca (2026), tabla 2 | IV shift-share (proximidad a atractivos por búsquedas de Google), efectos fijos de barrio y año, errores agrupados por barrio; Madrid, precios | coincide |
| Mense (2025), tabla 3A | IV-2SLS en panel con efectos fijos de región y año, instrumento de lluvia; alquiler | coincide |
| Borusyak, Hull y Jaravel (2022), tabla 4 | IV shift-share a nivel de sector, aplicación de Autor, Dorn y Hanson | coincide; la herramienta (src/v18/reproduccion/bhj_lib.py) queda validada |

Sin reproducción por falta de paquete con datos: Garcia-López et al. (2020), Jofre-Monseny et al. (2023), Monràs y García-Montalvo (2023), González y Ortega (2013), Fack, Gibbons y Manning y Grislain-Letrémy y Trevien (E4), Saiz (2010), Best y Kleven (2018) y Besley et al. (2014), Badarinza y Ramadorai (2018) y Cvijanović y Spaenjers (2021), la literatura de grandes tenedores, Segú (2020) y Koster y van Ommeren (2019). Baum-Snow y Han (2024) solo tiene código y su paquete completo no cabe en el disco; Asquith, Mast y Reed (2023) solo tiene código, sin datos. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan series de choques, que se usan como dato.

## Anexo C. Planes de replicación

El pre-registro interno lo forman el plan de replicación (docs/v18/plan_replicacion.md, commit d4e9869) y su adenda (docs/v18/plan_replicacion_adenda.md), que prevalece donde difiera. La etiqueta git local plan-replicacion-v18 señala el commit de la adenda (ad4385c), que está en la rama remota claude/housing-price-spain-econometric-95dhj3. La puerta de la fase 4 exige la etiqueta y que su commit esté en la rama remota; la subida de la etiqueta al remoto queda como tarea del autor.

- **Contenido.** Para cada estudio y ampliación: la especificación del original, su traslado a los datos del proyecto, las ampliaciones previstas y las pruebas. Incluye las reglas de inferencia, la clasificación V18, el multiverso enumerado, la estimabilidad por MDE, el sellado temporal y espacial, la magnitud preferida y la contabilidad.
- **Revisión.** Revisor del pre-registro (apto con cambios) y abogado del diablo (resiste con limitaciones). La adenda responde a todos los hallazgos de ambos sin haber mirado ningún resultado de V18; el autor decidió la regla de capas y lenguaje (K2).
- **Sellado de entrenamiento.** docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación.
- **Desviaciones.** Toda desviación respecto al plan está en docs/v18/desviaciones*.md con fecha y motivo.

## Anexo D. Pruebas por estimación

Las pruebas son las de B4 de cada diseño (pretendencias y potencia de Roth, placebos de fecha y de resultado, Honest DiD, primera etapa y F efectivo, número efectivo de choques, robustez a la exclusión de unidades atípicas y a la medida de precio o alquiler). Madrid, Baleares y Canarias ya están fuera por el sellado de v6, de modo que «sin Madrid» y «sin islas» no cambian la muestra provincial. Los valores completos y los intervalos están en tablas_v18.xlsx (pestañas «estimaciones» y «magnitudes»).

**D.1 Estimaciones con cifra.** «IC incluye el cero» describe el intervalo de la ficha (IC95, salvo indicación). Todas son de capa C4.

| Id | Magnitud y unidad | Estimación | ¿IC incluye el cero? | Clase V18 |
|---|---|---|---|---|
| E1-R3 | Log del alquiler por punto de densidad HUT (estudio de eventos) | 0,00443 | No | ASOCIACIÓN |
| E1-R4 | Log, secciones del radio frente al anillo (Sagrada Família) | 0,00166 | Sí | NO CONCLUYENTE |
| E1-P-H3 | Log del alquiler por desviación típica intra-sección (coprincipal) | −6,5e−05 | Sí | SUGESTIVO |
| E2-R1 | Log de la renta media de contratos nuevos | −0,0384 | No | SUGESTIVO |
| E2-R1c | Log de contratos por 1.000 habitantes | 0,0173 | Sí | ASOCIACIÓN |
| E2-R1-REV | Reversión tras la STC 37/2022 (log de la renta) | −0,00157 | Sí | SUGESTIVO |
| E3-R1 | €/m² por punto de población (IV, Webb-AR) | 3,55 | Sí | NO CONCLUYENTE |
| E5-A1 | Interacción del instrumento de inmigración con solares (Δ ln P) | 0,00244 | Sí | ASOCIACIÓN |
| E7-R1 | % del precio por +100 pb a ocho trimestres (LP-IV); AR no acotado | 1,28 | No aplicable | NO ESTIMABLE |
| E7-R3 | % del precio por +100 pb del euríbor a ocho trimestres (BVAR; banda del 68 %) | −1,55 | No (banda del 68 %) | ASOCIACIÓN |
| E7-A2 | Respuesta relativa entre provincias (panel) | −19,7 | No | NO ESTIMABLE |
| E8-R1 | Log del valor tasado a cuatro trimestres por punto del tipo general del ITP | 0,0146 | No (aleatorización) | ASOCIACIÓN |
| E10-A1 | % del alquiler por m² por punto de viviendas de grandes tenedores | 1,07 | Sí | ASOCIACIÓN |
| E12-A1 | Viviendas libres iniciadas por vivienda protegida calificada (IV) | 6,5 | Sí (conjunto AR) | NO ESTIMABLE |
| E12-A2 | % del valor tasado real por vivienda protegida calificada (IV) | 22,1 | AR no acotado | ASOCIACIÓN |
| F1-R1 | Elasticidad de impacto, precio frente a renta de los hogares (nacional) | 0,126 | Sí | ASOCIACIÓN |
| F1-R2-pmg | Elasticidad de corto plazo, panel provincial (PMG) | 0,348 | No | ASOCIACIÓN |
| F2-R1 | Elasticidad de corto plazo del alquiler a la renta (PMG) | −0,102 | No | ASOCIACIÓN |
| F3-A2 | Elasticidad de corto plazo de las iniciadas al valor tasado (PMG) | 3,52 | No | ASOCIACIÓN |

**D.2 Estimaciones NO ESTIMABLES: la comprobación previa.** Se publica la magnitud mínima detectable (MDE), el F efectivo o el recuento de datos, no el coeficiente.

| Id | Comprobación | Cifra | Clase V18 |
|---|---|---|---|
| E1-R1 | Barrios con el cambio mínimo de stock | 18 | NO ESTIMABLE |
| E1-R2 | F efectivo de la primera etapa | 0,0233 | NO ESTIMABLE |
| E1-A1 | MDE | 0,166 | NO ESTIMABLE |
| E2-A1 | MDE | 0,0408 | NO ESTIMABLE |
| E2-A4 | MDE | 0,0444 | NO ESTIMABLE |
| E3-R2 | MDE (elasticidad) | 2,33 | NO ESTIMABLE |
| E3-A1 | MDE (% por punto) | 10,4 | NO ESTIMABLE |
| E5-R1 | F efectivo de la primera etapa | 0,032 | NO ESTIMABLE |
| E6-R1 | MDE (log) | 0,0623 | NO ESTIMABLE |
| E8-R2 | MDE (log por punto) | 0,0894 | NO ESTIMABLE |
| E9 | Número efectivo de choques (sin pesos) | 6,3 | NO ESTIMABLE |

**D.3 E2-R1: robustez a posteriori (B6).** Los resultados de esta tabla se añadieron después de ver los de E2-R1 y no deciden su clase.

| Id | Prueba | Estimación | ¿IC incluye el cero? |
|---|---|---|---|
| E2-B6-A | Salto en 2022T2 sobre la extrapolación de la recta de la vigencia | −0,0217 | Sí |
| E2-B6-B | HUT 2019 y ln(población) 2019 por trimestre | −0,0242 | No |
| E2-B6-C | Controles emparejados por el crecimiento previo de la renta | −0,0546 | No |
| E2-B6-D | Diferencias en diferencias sintéticas con controles ponderados | −0,044 | No |
| E2-R1c-v1 | Contratos por hogar inquilino del Censo 2021 | −0,0314 | Sí |

## Anexo E. Monte Carlo de las herramientas

Cada herramienta nueva se validó antes de usarse con procesos generadores que reproducen la estructura de los diseños de V18 (output/v18/montecarlo/<herramienta>/). Se simula bajo el nulo y bajo la alternativa, con semilla fija y sin ningún dato real de resultado ni muestra sellada. Un resultado es apto si el tamaño al 5 % y la cobertura al 95 % caen en las bandas de la adenda 1.12. [FALTA CIFRA: tamaños empíricos y coberturas por herramienta y condición (output/v18/montecarlo/*/resultado.json)]

| Herramienta | Veredicto | Condición |
|---|---|---|
| Callaway-Sant'Anna con Webb | APTO CONDICIONADO | Diseños municipales con muchos tratados y controles; NO APTO con ocho clusters |
| Sun-Abraham con Webb | APTO | Frágil si las comunidades de control son pocas |
| de Chaisemartin-D'Haultfœuille con aleatorización del calendario | APTO | Aleatorización entre ocho comunidades; el bootstrap de Webb con ocho clusters es NO APTO |
| Aleatorización | APTO | Entre municipios y entre comunidades |
| Honest DiD | APTO CONDICIONADO | Solo sin desviación de tendencias paralelas; con desviaciones mayores es válido pero conservador y sin potencia |
| DiD sintético con Conley-Taber | APTO | Si los tratados son intercambiables con los controles; no si son más variables |
| Webb en TWFE | APTO y APTO CONDICIONADO | Según el diseño |
| Conley | Mixto | Apto si el alcance de la dependencia no supera el corte; NO APTO si lo duplica |
| IV débil | Mixto | APTO con instrumento fuerte; APTO CONDICIONADO o NO APTO en los diseños más débiles |
| BHJ con pocos choques | NO APTO | Con pocos choques efectivos |
| Driscoll-Kraay con T corto | NO APTO | Con series temporales cortas |
| Proyección local con instrumento | NO APTO | Newey-West subestima la incertidumbre; el AR aumentado con EHW es el más cercano al nominal bajo el nulo; con T corto la respuesta a horizontes largos queda atenuada |
| SVAR con proxy | NO APTO | AR por método delta apto solo con F cercano a diez |
| BVAR recursivo | NO APTO | Bandas conservadoras o con cobertura distinta de la nominal |
| Metaanálisis bayesiano | NO APTO por conservador | Intervalos que cubren de más; con dos estudios y heterogeneidad el efecto fijo no cubre la media verdadera |

En la simulación, la inferencia por aleatorización del calendario es la única apta con ocho comunidades (E8). Las herramientas NO APTAS se publican con esa etiqueta y la clasificación no se apoya en ellas.

## Anexo F. Pre-registro interno y análisis a posteriori

**Qué es pre-registro interno sin sello de tiempo externo.**

- El plan de replicación (commit d4e9869) y su adenda, con la etiqueta git local plan-replicacion-v18 sobre el commit ad4385c, fechada el 2026-10-20. El commit está en la rama remota claude/housing-price-spain-econometric-95dhj3; la etiqueta aún no está en el remoto (tarea del autor).
- No es un pre-registro depositado en un registro externo y no debe describirse como tal. Lo fija solo el historial de git del proyecto.
- Las especificaciones, las variantes enumeradas, las reglas de estimabilidad por MDE, de clasificación y de magnitud preferida, la designación de la estimación propia de cada factor y las hipótesis de la evaluación diferida se fijaron en ese plan y su adenda, antes de la primera estimación de V18 y sin haber mirado ningún resultado.
- Los resultados de V18 se describen siempre como resultados de un pre-registro interno sin sello de tiempo externo, con su etiqueta, su commit y su fecha.

**Qué es a posteriori.**

- *Todo V17.* La auditoría de afirmaciones y medidas, la demografía, el análisis general o local, la factibilidad y las cifras V17-* se hicieron sin pre-registro y se integran aquí como análisis a posteriori de capa C4.
- *La robustez B6 de E2-R1 y E2-R1c.* Se añadió después de ver los resultados, por petición del abogado del diablo (anexo D.3). No cambia la especificación principal ni su clase por sí sola.
- *Las desviaciones.* Toda desviación respecto al plan (docs/v18/desviaciones*.md) se declaró con fecha y motivo. Entre ellas: el paro registrado de E2 (una versión anterior de la desviación era errónea y se corrigió); la geometría y la lectura de la ficha de E1-R4 (K8 bis); la lectura restrictiva de la contabilidad (K10); el deflactor del PIB en lugar del IPC; los ocho grupos de origen en E3.
- *Decisiones tomadas tras ver resultados de otras especificaciones.* K7 (clasificación de E8-R1 y E2-R1c tras la ronda 1 del abogado del diablo), K8 y K8 bis (E1-R4) y K9 (E2-R1 tras la ronda 2, con su frase de limitación).
- *Datos descargados después de la etiqueta.* Marcados `posterior_prereg`.
- *La ilustración de la contabilidad* con magnitudes de la literatura.
- *Réplicas del plan sobre preguntas ya vistas.* Las especificaciones que repiten una pregunta cuyo resultado ya se conocía llevan la marca `repite_visto` (plan, 0.2).

**Capa y lenguaje.** Toda cifra V18 es de capa C4 con nivel de evidencia EXPLORATORIO. Ninguna estimación es IDENTIFICADO, de modo que no se usa en ningún lugar la fórmula condicional prevista. El documento no formula ninguna cifra V18 como causa: cada una es una asociación condicionada al diseño. El generador del documento (src/v18/f6_documento.py) toma todas las cifras de output/v5/cifras_clave.csv y falla si un marcador no existe.
