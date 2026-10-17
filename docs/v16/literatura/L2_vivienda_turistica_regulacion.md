# L2 · Regulación de la vivienda turística (moratorias, licencias, zonificación) y diseños para Q2

V16, fase 3. Lector de literatura, una pregunta. Fecha de lectura: 2026-10-17. Todas las fichas quedan en «NO VERIFICADA». Este fichero AÑADE a docs/v15/literatura/P5_pisos_turisticos.md (17 fichas); no repite sus fichas: se citan como «ver docs/v15/literatura/P5_pisos_turisticos.md, ficha <autores>». No he podido releer docs/v15/literatura.md ni el resto de ficheros de docs/v15/literatura/ por presupuesto; solo he leído P5.

Reglas de lectura. Solo se resume lo leído al menos en su resumen. «Resumen del buscador» significa que solo he visto el extracto que devuelve el buscador, no la página de origen; en ese caso lo digo y no uso la cifra como estimación. Las magnitudes van tal como las da el autor. Donde WebFetch devolvió un PDF binario, lo leí con el lector de PDF (páginas indicadas). Los ficheros PDF descargados quedaron fuera del repositorio.

Medidas del resultado: la unidad de exposición cambia entre trabajos (anuncios por barrio, tasa de anuncios en %, anuncios por 100 viviendas, cuota en p.p.). Las comparaciones entre trabajos son de orden de magnitud. El CSV acompañante (L2_vivienda_turistica_regulacion_efectos.csv) separa dos bloques: (i) densidad de VUT → alquiler (cifras de V15 citadas con «ver P5» y leido = «ficha V15») y (ii) regulación → anuncios, alquiler, precio.

---

## 1. Mecanismo teórico

Koster, van Ommeren y Volkhausen (versión de 2019, pp. 1-2, leída) formulan tres mecanismos, que atribuyen a Turner et al. (2014): (1) efecto de uso eficiente: el alquiler de corta duración genera renta de espacio ocioso y sube la demanda y el precio de compra; (2) efecto de oferta de vivienda: reasignación de parque desde el alquiler residencial hacia el uso en propiedad, lo que sube los alquileres; (3) efecto de externalidad: molestias que bajan el valor vecino. De ahí se sigue una predicción de diseño que ellos mismos explicitan (p. 19): en una discontinuidad de frontera el alquiler residencial no debería saltar (inquilinos indiferentes entre ambos lados, subarriendo prohibido), mientras que el precio de compra sí, porque capitaliza la opción de alquilar a turistas. Por eso estiman el alquiler con diferencias en diferencias (DiD) y no con regresión discontinua.

Gonçalves, Peralta y Pereira dos Santos (IZA DP 15706, abstract y p. 1, leído) añaden un mecanismo de institución: en Portugal la licencia de alojamiento local no caduca hasta la venta, por lo que prohibir nuevos registros elimina la opción de uso turístico del inmueble (valor de opción). Bibler, Teltser y Tremblay (2021, resumen, p. 1) formulan que el efecto neto sobre la asequibilidad es teóricamente ambiguo, porque la renta turística puede compensar el mayor coste de la vivienda. Wachsmuth y St-Hilaire (versión de septiembre de 2024, resumen y pp. 2-4, leída) distinguen tres canales: oferta (reasignación de unidades), demanda (residentes que demandan más vivienda para ofrecerla) y rigidez de precios (propietarios que suben el alquiler con más agresividad cuando disponen del uso turístico como alternativa). Para el marco de equilibrio general y sorting, ver ficha Almagro y Domínguez-Iino en P5. Para el valor de opción, ver ficha Valentin en P5.

## 2. Evidencia internacional con diseño creíble

Efecto de la regulación sobre anuncios. Todos los trabajos con diseño leído encuentran descensos de anuncios o de actividad, de tamaño muy variable: −50 % de anuncios en Los Ángeles (ver P5, ficha Koster; en la versión de 2019, −9,7 p.p. en la probabilidad de estar anunciado, equivalente según los autores a −32 %, que sube a −20 p.p. a 2,5 años o más, ≈ −70 %); −40 % en oferta y reservas con el registro obligatorio en Chicago y San Francisco (Bibler et al. 2021); −9,0 % de anuncios en 12 meses (Bekkerman et al. 2023, resumen); −43 % de días de reserva en Burdeos (Robertson et al. 2023); ≈ −60 % en Santa Monica (Chaves Fonseca 2024, resumen). En cambio Viena (reforma de julio de 2024) muestra solo un descenso leve de anuncios no atribuible claramente a la reforma (Banabak y Sielker 2026, resumen). Ver también P5, fichas Duso et al. y Dong para Berlín y Nueva York (−90 % de oferta con la Local Law 18 según el resumen de Dong).

Efecto sobre el alquiler residencial. Es el resultado con menos estimaciones puntuales independientes: Koster et al. dan −2 % (publicada) o −3,4 % a −4,9 % en el DiD de la versión de 2019 (tabla 9); Santa Monica da un efecto no significativo con síntesis de control (resumen); Wachsmuth y St-Hilaire encuentran que las regulaciones que reducen el volumen de alquiler turístico bajan los alquileres, y que el efecto se extiende a jurisdicciones vecinas (ver P5, ficha Wachsmuth y St-Hilaire; yo he leído en el PDF de septiembre de 2024 solo el resumen y la introducción, sin tablas; las cifras en dólares que aparecen en prensa no las he podido contrastar con el texto y no las uso); Viena no observa mayor oferta de alquiler de largo plazo; el ESRI para Irlanda no halla relación entre actividad de alquiler turístico y caída de nuevos registros de inquilinos en 2019-2023. Ver P5, ficha Dong, para el nulo de asequibilidad tras la Local Law 18 de Nueva York.

Efecto sobre el precio de compra. Los signos son negativos con regulación: −2,9 % a −4,2 % en Los Ángeles (tabla 5, versión de 2019), −8 % en Lisboa (−20 % en pisos de dos dormitorios; IZA DP 15706), −10 % en los tramos censales más densos (Bibler et al. 2021), −30 % en Nueva Orleans (ver P5, ficha Valentin). La interpretación de los autores es la capitalización de la opción de alquilar a turistas, no una reducción de oferta.

Efectos laterales documentados: inversión residencial. Bekkerman et al. (2023, resumen) hallan que la regulación reduce los permisos residenciales un 11,0 % en 12 meses (−16,5 % en unidades accesorias), con regresión discontinua en fronteras jurisdiccionales y con el calendario de las normas.

Diseño de regresión discontinua espacial en fronteras de zona. Koster et al. (2019, pp. 17-24, leído): panel RDD con efectos fijos de propiedad (o de bloque censal) y de área HSO × mes, núcleo uniforme, ancho de banda de Imbens-Kalyanaraman (1,67 km para anuncios) con robustez a ×2 y ÷2; segmentos de frontera × mes; comprobaciones de continuidad de covariables en la frontera (densidad, vivienda en propiedad, renta, edad, resultados escolares: continuas, fig. 5), tests tipo McCrary, y tres placebos (fronteras desplazadas 1 km, zonas con normativa urbanística no aplicada, ciudad de Los Ángeles) más placebos temporales a 5 y 10 años: todos indistinguibles de cero (tabla 8). Los efectos sobre anuncios crecen con el tiempo (fig. 7) y los del precio se estabilizan hacia los 1,5 años (≈ −4,5 %, fig. 8), de ahí que excluyan las transacciones del primer año tras la norma. Evidencia de desplazamiento a barrios vecinos en ese diseño: no hallan aumento de anuncios justo fuera de la zona (nota 25) ni de precios en 0-200 m y 200-500 m fuera de la zona (tabla 6, col. 5: 0,0219 con ee 0,0498 y −0,0409 con ee 0,0342). En cambio Nueva Orleans (ver P5, ficha Valentin) halla más uso en barrios contiguos, y Wachsmuth y St-Hilaire (resumen) efectos que se extienden a vecinos: la ausencia de desbordamiento no es general.

## 3. Evidencia española

Barcelona. El único trabajo con identificación creíble y alquiler y precio por barrio sigue siendo García-López, Jofre-Monseny, Martínez-Mazza y Segú (ver P5, ficha 1): termina en 2016-2017, antes de que el PEUAT (enero de 2017, según Ardura et al. 2019) pudiera desplegar efectos. No he localizado una evaluación causal publicada del PEUAT sobre alquiler o precio (confirma P5, ficha Reina 2026, que es cualitativa). Una tesis de Princeton, localizada solo por el buscador, estima un DiD sobre 134.960 anuncios de Barcelona y Sevilla (2015-2023) con efecto sobre precio por noche, reseñas y oferta de anuncios, no sobre alquiler residencial (ver ficha 12).

Madrid. Chaves Fonseca (SERIEs, 2026) estima con shift-share que por cada 100 anuncios de vivienda entera más en un barrio, el precio de la vivienda sube un 2 % y las entradas anuales de residentes bajan unas 50 (≈ 2 % de la media), 2010-2018 (resumen). No evalúa el Plan Especial de Hospedaje de 2019. Ardura et al. (2019) comparan descriptivamente el PEH y el PEUAT y concluyen que ambos contienen la turistificación en distritos centrales, con riesgos a su efectividad por criterios de zonificación y reactivación de aprobaciones. No encontré ninguna evaluación del efecto del PEH sobre el alquiler.

València, Palma, Baleares, Canarias. València: ver P5, ficha MESVAL (corte transversal de 2021, no una evaluación de la moratoria). Palma (prohibición en plurifamiliares de 2018): mi búsqueda solo devolvió prensa y sentencias; no hallé estudio que mida el efecto en alquiler. Baleares y Canarias: sin evaluación causal localizada (ver «Lo que no he podido leer»). IVIE: no lo busqué específicamente. AIReF y Banco de España: la búsqueda de un estudio propio sobre VUT no devolvió nada nuevo respecto de P5 (fichas López-Rodríguez y Matea; Khametshin et al.).

## 4. Efectos secundarios documentados y sus magnitudes

- Desplazamiento a alquiler de temporada (España): según un resumen del buscador, un análisis de EsadeEcPol con datos de Idealista sitúa el peso del alquiler de temporada en los anuncios de Barcelona en el 2,1 % en 2019 y el 14,4 % en 2023 y lo relaciona con la regulación del alquiler turístico desde 2017 (ficha 14; no he leído el documento). Una cifra de prensa sobre el 49 % de la oferta de alquiler en 2025 mide otra cosa (cuota de la oferta frente al total de anuncios) y no la uso. No hay estimación causal localizada del desplazamiento a temporada.
- Desplazamiento entre tipos de anfitrión: en Los Ángeles los anuncios de vivienda entera caen más que los de habitaciones compartidas donde se permite compartir (tabla 4, panel B, versión de 2019); en Burdeos la regulación también cambia el comportamiento de los anuncios no objetivo (Robertson et al. 2023, resumen); ver P5, ficha Duso et al., sobre comerciales y no comerciales.
- Hoteles y alojamiento formal: Koster et al. (2019, apéndice A.4.3, citado en p. 28) dan un aumento puntual de alrededor del 10 % de alojamientos formales tras las ordenanzas, imprecisa («suggestive evidence»). No he leído ningún estudio sobre precios hoteleros en Barcelona. Santa Monica y Los Ángeles no dan efecto sobre el precio por noche de Airbnb (Koster 2019, apéndice A.4.2, descrito en p. 28).
- Demanda anticipada: Gonçalves et al. documentan un pico de nuevos registros entre el anuncio y la entrada en vigor de la prohibición en Lisboa, impulsado por propietarios nacionales ya establecidos (IZA, abstract). Es un riesgo para un DiD con fecha de tratamiento = fecha de entrada en vigor.
- Inversión: ver sección 2 (Bekkerman et al.).
- Movilidad residencial: ver Madrid (Chaves Fonseca 2026).

---

## 5. Fichas

### Koster, van Ommeren y Volkhausen (2019). Short-term rentals and the housing market: Quasi-experimental evidence from Airbnb in Los Angeles (versión de trabajo, 8 de marzo de 2019)
- DOI: sin DOI (versión de trabajo; la versión publicada tiene 10.1016/j.jue.2021.103356 y ya consta en P5) · Revista: versión de seminario (SMU, 3 de abril de 2019); la serie CEPR DP13094 devolvió 403
- Leído: texto completo parcial, pp. 1-2 y 17-38 del PDF (https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2019/20190403.pdf); no leí los apéndices ni la sección de bienestar
- Diseño e identificación: 18 de 88 ciudades del condado de Los Ángeles adoptan ordenanzas que restringen severamente el alquiler de corta duración. Anuncios y precios de venta 2014-2018 (microdatos; precios de transacciones; alquiler mediano por m² de Zillow a nivel de código postal). Panel RDD con efectos fijos de propiedad o de bloque censal, área HSO × mes y segmento de frontera × mes; núcleo uniforme, ancho de banda óptimo de Imbens-Kalyanaraman con robustez ×2 y ÷2. Alquiler: DiD por código postal (efectos fijos de código postal y mes, tendencias por distancia al centro y a la playa), porque el diseño predice que el alquiler no salta en la frontera. Precio sobre tasa de anuncios: 2SLS con ficticias HSO específicas por ciudad como instrumentos (F de Kleibergen-Paap de 15 a 18 en la mayoría de columnas; la 4 es 16,94 y la 6 es 64,24). Diagnósticos leídos: tendencias paralelas previas en alquiler y precio (fig. 6), continuidad de covariables en la frontera (fig. 5), tres placebos de frontera y dos temporales (tabla 8).
- Resultado principal, con su magnitud: resumen de esta versión: «Ordinances reduced listings by 50% and housing prices by 3%... ordinances reduced rents also by 3%» y un aumento de precio de «10% within 2.5km of Downtown LA». Tabla 4, panel A, col. 1: efecto de la ordenanza sobre la probabilidad de estar anunciado (vivienda entera) −0,0969 (ee 0,0086), N = 270.906; col. 2 (con segmentos de frontera): −0,0985 (0,0088). Los autores lo traducen en −32 % de anuncios dada una probabilidad de 0,3 antes de la norma. Tabla 5, log precio: col. 1 −0,0421 (0,0067), N = 58.316; col. 2 −0,0297 (0,0080), N = 58.285 (los autores: −4,1 % y −2,9 %). Tabla 7, 2SLS log precio por 1 p.p. de tasa de anuncios (<200 m): col. 1 0,0351 (0,0100); col. 2 0,0226 (0,0088), N = 80.905; los autores calculan una elasticidad de 0,0386 (= 0,0226/1,1523) y un efecto de 4,2 % por desviación típica de la tasa (1,845 p.p.). Tabla 9, panel A, log alquiler mediano por m²: col. 1 −0,0347 (0,0118), N = 3.313; col. 2 −0,0372 (0,0120); col. 3 −0,0496 (0,0134); col. 4 (solo observaciones a <2,5 km fuera de las zonas) −0,0192 (0,0128); col. 5 −0,0376 (0,0124); col. 6 −0,0440 (0,0132). Panel B (2SLS), log alquiler por 1 p.p. de tasa de anuncios: col. 1 0,0365 (0,0199); col. 2 0,0321 (0,0148); col. 3 0,0575 (0,0274); col. 4 0,0112 (0,0099). Placebos de tabla 8: coeficientes no distintos de cero (por ejemplo, frontera desplazada 1 km: −0,0036 (0,0064) en anuncios y 0,0093 (0,0173) en precio). Sin heterogeneidad por demanda turística en el efecto de la norma sobre el precio (tabla 6, cols. 1-2). Las cifras de la versión publicada (−2 % en precio y en alquiler) son distintas de las de esta versión: ver P5, ficha Koster.
- Validez externa para España: transferible el diseño (frontera administrativa con tratamiento distinto, DiD de alquiler, placebos), no la magnitud: Los Ángeles prohíbe el subarriendo en casi todos los contratos, circunstancia que los autores usan como supuesto (p. 19), y la regulación es municipal con fronteras entre ciudades. En España la regulación autonómica cubre toda la unidad; las fronteras utilizables serían entre zonas de un mismo plan (PEUAT), entre municipios con moratoria y vecinos sin ella, o entre CCAA. Discrepancias: el efecto de precio y alquiler cambia de signo en magnitud entre versiones (3 % frente a 2 %); dentro de esta versión, el alquiler a menos de 2,5 km de las zonas no es significativo (tabla 9, col. 4), lo que los autores leen como continuidad de alquiler en la frontera.
- Estado: NO VERIFICADA (sin DOI)

### Bibler, Teltser y Tremblay (2021). Is Sharing Really Caring? The Effect of Airbnb on Housing Prices and Foreclosures
- DOI: 10.2139/ssrn.3846919 (visto en OpenAlex) · Revista: SSRN Electronic Journal (versión de 5 de noviembre de 2021; sin revisión por pares localizada)
- Leído: resumen y primera página de introducción (https://webarchive.ucr.edu/economics.ucr.edu/wp-content/uploads/2021/11/11-21-2021-Bibler.pdf; https://api.openalex.org/works?search=Airbnb+registration+enforcement+Chicago+San+Francisco). No he leído las tablas.
- Diseño e identificación: aplicación obligatoria del registro de anfitriones en las ciudades de Chicago y San Francisco, frente a áreas no tratadas dentro de las dos áreas metropolitanas; datos de anuncios y de transacciones y ejecuciones hipotecarias (Zillow ZTRAX) a nivel de tramo censal.
- Resultado principal, con su magnitud: «enforcing registration requirements... reduced Airbnb supply and bookings by 40%»; los mayores shocks en los barrios con más anuncios por habitante; «home prices decline by roughly 10% in the most Airbnb-dense census tracts while foreclosures in these same tracts increase by roughly 0.07 per tract-month (or 117%)». No mide alquiler.
- Validez externa para España: es un DiD sobre una norma de registro (coste de anunciar), no sobre una prohibición; la comparación es la más cercana a un registro de VUT, y avisa de que el efecto sobre el precio se concentra en los barrios más densos. Las ejecuciones hipotecarias son un resultado sin análogo directo en España. Discrepa en magnitud con Koster et al. (−10 % en los tramos más densos frente a −3 % de media); coincide en signo.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Bekkerman, Cohen, Kung, Maiden y Proserpio (2023). The Effect of Short-Term Rentals on Residential Investment
- DOI: 10.1287/mksc.2022.1409 (visto en IDEAS) · Revista: Marketing Science, vol. 42(4), pp. 819-834
- Leído: resumen (https://ideas.repec.org/a/inm/ormksc/v42y2023i4p819-834.html)
- Diseño e identificación: dos estrategias, según el resumen: (1) calendario de entrada en vigor de las normas locales sobre alquiler de corta duración; (2) fronteras jurisdiccionales con y sin norma. Resultado sobre anuncios y permisos de construcción residencial. No he leído datos, periodo ni país; el buscador indica EE. UU.
- Resultado principal, con su magnitud: en los primeros 12 meses tras la norma, los anuncios de Airbnb caen un 9,0 % y los permisos residenciales un 11,0 %; en la frontera, caída de permisos en el lado con norma, la mayor en unidades accesorias, un 16,5 %.
- Validez externa para España: es un efecto lateral sobre la oferta futura (construcción), no sobre alquiler o precio actuales. Importa para el diseño porque una regulación puede reducir la oferta residencial futura, lo que sesga a la baja cualquier efecto en alquiler a 2-3 años. No hay equivalente español localizado. Discrepancia: no hay trabajo comparable leído.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Chaves Fonseca (2024). Short-term rentals and residential rents: evidence from a regulation in Santa Monica
- DOI: 10.1108/ijhma-01-2024-0001 (visto en OpenAlex) · Revista: International Journal of Housing Markets and Analysis, vol. 18(5), pp. 1169-1203
- Leído: resumen reconstruido por el lector desde OpenAlex (https://api.openalex.org/works/doi:10.1108/ijhma-01-2024-0001); la versión SSRN de 2019 (10.2139/ssrn.3328485) no tiene resumen en OpenAlex
- Diseño e identificación: control sintético sobre un panel de anuncios de Airbnb y alquileres de varias ciudades del condado de Los Ángeles; la ordenanza de alquiler compartido de Santa Monica de 2015. El autor lo presenta como la primera aplicación de control sintético a una norma de este tipo.
- Resultado principal, con su magnitud: descenso de anuncios de «aproximadamente un 60 %» en dos años (parafraseo del resumen); efecto sobre el alquiler residencial no estadísticamente significativo. Sin ee ni IC en el resumen.
- Validez externa para España: un único tratamiento (una ciudad) con control sintético es un diseño aplicable a un único municipio español con moratoria (por ejemplo, València) si hay un conjunto de donantes con la misma medida de alquiler; pero el nulo se refiere a una ciudad y no excluye efectos del orden de 2-3 %. Discrepa de Koster et al., que incluye Santa Monica entre las 18 ciudades y halla −2 % a −3 % en alquiler agregado.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Robertson, Dejean y Suire (2023). «Airbnb in the City»: assessing short-term rental regulation in Bordeaux
- DOI: 10.1007/s00168-023-01215-4 (visto en OpenAlex) · Revista: The Annals of Regional Science, vol. 72(2), pp. 647-682
- Leído: resumen y primeras páginas de la versión de HAL (hal-04123595; https://nudd.univ-larochelle.fr/app/uploads/sites/10/2024/07/Airbnb20in20the20City20published.pdf), pp. 1-3. No leí datos ni tablas.
- Diseño e identificación: diferencias en diferencias y triple diferencia sobre la actividad de alquiler de corta duración en Burdeos tras la regulación de la ciudad (anuncios dirigidos o comerciales frente a no dirigidos o home-sharing). Sobre actividad, no sobre alquiler residencial.
- Resultado principal, con su magnitud: «reductive effect of over 322 rented days per month per district on average. This equates to 43% of mean reservation days and over 28 thousand less nights spent per month in STRs across the city»; en la periferia, 35 % de los días reservados mensuales. Los anuncios no objetivo «also seem to have modified their behavior». El resumen no da ee.
- Validez externa para España: indica que la efectividad de la norma varía entre centro y periferia (relevante para una zonificación como la del PEUAT) y que los anfitriones no objetivo reaccionan (posible contaminación del control). No mide alquiler. Un buscador devolvió «316 días» en otra versión: la cifra depende de la versión; uso la del PDF leído.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Gonçalves, Peralta y Pereira dos Santos (2022). Short-Term Rental Bans and Housing Prices: Quasi-Experimental Evidence from Lisbon
- DOI: sin DOI (no visto) · Revista: IZA Discussion Paper n.º 15706 (noviembre de 2022); versión previa en GEE Papers 155 (503 al consultar; no leída)
- Leído: resumen y página de introducción (pp. 1-4 del PDF; https://docs.iza.org/dp15706.pdf)
- Diseño e identificación: reforma urbanística de noviembre de 2018 que prohíbe nuevos registros de alquiler de corta duración en algunas zonas de Lisboa («containment areas»); DiD que aprovecha la discontinuidad espacial; registros administrativos de alojamiento local y de transacciones inmobiliarias, más datos de Airbnb. No he leído tablas ni el diseño detallado del radio.
- Resultado principal, con su magnitud: «The reform decreases real estate prices by 8%, mostly in two-bedroom dwellings, for which the price drops 20%»; pico de nuevos registros entre el anuncio y la entrada en vigor de la prohibición. No mide alquiler.
- Validez externa para España: es el caso más cercano a una moratoria de licencias por zonas con registro previo (como las de València o el PEUAT); la lectura del autor (valor de opción de la licencia) es aplicable donde la licencia se transmite o caduca con la venta; en España depende de la norma autonómica. Discrepa en magnitud de Franco y Santos (P5; efecto por cuota de Airbnb) y de Koster (−3 %).
- Estado: NO VERIFICADA (sin DOI)

### Nobre, Jardim Gonçalves y Cruz (2026). Short-term rentals and the housing market: evidence from Portuguese metropolitan areas
- DOI: 10.1007/s10258-026-00295-2 (visto en OpenAlex) · Revista: Portuguese Economic Journal
- Leído: resumen reconstruido desde OpenAlex (https://api.openalex.org/works/doi:10.1007/s10258-026-00295-2)
- Diseño e identificación: reforma de 2014 que facilita el registro; transacciones 2010-2017 en las áreas metropolitanas de Lisboa y Oporto; efectos fijos bidireccionales y DiD escalonado por código postal; controles de características, ubicación y tiempo.
- Resultado principal, con su magnitud: cada alquiler de corta duración adicional por trimestre y código postal eleva el valor de la transacción un 2,3 %-6,0 % (€104-€329 por transacción); mayor en segmentos altos y parroquias con menos paro y densidad; el efecto aparece hacia el décimo trimestre; efectos positivos sobre locales comerciales. No da ee en el resumen.
- Validez externa para España: mide precio de compra con exposición por unidad de código postal; el efecto tarda unos diez trimestres, de modo que un DiD español con ventana corta tras 2018-2024 puede no detectarlo. El resumen no menciona alquiler. Coincide en signo con Franco y Santos (P5).
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Chaves Fonseca (2026). The effect of short-term rentals on house prices and residential mobility: evidence from Madrid
- DOI: 10.1007/s13209-026-00335-2 (visto en OpenAlex) · Revista: SERIEs (Journal of the Spanish Economic Association)
- Leído: resumen reconstruido desde OpenAlex (https://api.openalex.org/works/doi:10.1007/s13209-026-00335-2)
- Diseño e identificación: panel barrio-año de Madrid, 2010-2018; variable instrumental tipo shift-share (atractivo turístico espacial por expansión de la plataforma); análisis de mediación.
- Resultado principal, con su magnitud: cada 100 anuncios adicionales de vivienda entera en un barrio se asocian con unas 50 entradas anuales menos de residentes (≈ 2 % de la media), sin efecto significativo en salidas, y con un aumento del precio de la vivienda del 2 %; el efecto sobre la movilidad opera sobre todo a través del precio; concentrado en residentes sin estudios universitarios. No da ee en el resumen; no hay resultado sobre alquiler.
- Validez externa para España: es el único estimador de identificación creíble para Madrid localizado, pero termina en 2018, antes del Plan Especial de Hospedaje (2019), y mide precio de compra, no alquiler. Sirve como contrapunto madrileño de García-López et al. (Barcelona).
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Banabak y Sielker (2026). Short term rental regulations in Vienna – enforcement versus deterrence?
- DOI: 10.1080/00343404.2026.2693559 (visto en OpenAlex) · Revista: Regional Studies, vol. 60(1)
- Leído: resumen reconstruido desde OpenAlex (https://api.openalex.org/works/doi:10.1080/00343404.2026.2693559)
- Diseño e identificación: métodos mixtos: DiD y entrevistas con oferentes y reguladores; reforma de julio de 2024 que restringe operaciones profesionales y permite el alquiler compartido.
- Resultado principal, con su magnitud: «slight decline in STR listings» no atribuible claramente a la reforma, y no se observa mayor oferta de alquiler de larga duración; efectos limitados atribuidos a problemas de cumplimiento y recursos administrativos. Sin cifras en el resumen.
- Validez externa para España: indica el riesgo de que una norma sin aplicación efectiva no genere variación de tratamiento: en el registro de VUT conviene separar la fecha de la norma de la fecha de aplicación (bajas de anuncios). Un resumen no permite comparar magnitudes. Sin explicación de la ventana temporal tras julio de 2024, muy corta.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Slaymaker (2025). New research highlights challenge of understanding short-term let activity and interaction with the rental sector (ESRI, Irlanda)
- DOI: sin DOI · Revista: ESRI (Economic and Social Research Institute), nota de prensa de 25-04-2025; el informe completo no lo he leído
- Leído: resumen en la página de la institución (https://www.esri.ie/node/10386)
- Diseño e identificación: análisis de anuncios de Airbnb en Irlanda, comparación con segundas residencias y evaluación del registro voluntario y de los requisitos de cambio de uso en las Zonas de Presión de Alquiler (RPZ). Sin identificación causal descrita en la nota.
- Resultado principal, con su magnitud: sin pruebas de que el aumento de la actividad de alquiler turístico se relacione con descensos de nuevos registros de inquilinos entre 2019 y 2023; al menos un anuncio por cada 10 viviendas del alquiler privado en 38 de 166 áreas electorales locales; 91 solicitudes de registro de cambio de uso en 2023 frente a 9.142 anuncios de vivienda entera en RPZ en septiembre de 2023 (dato de la nota).
- Validez externa para España: la norma irlandesa de 2019 sí diferencia RPZ y resto, pero la nota sugiere un incumplimiento extendido. Es una fuente institucional, no un estudio revisado por pares en lo que he leído. Discrepa de los efectos positivos del alquiler turístico sobre el alquiler residencial de P5 (García-López et al.), aunque mide otro resultado (nuevos registros).
- Estado: NO VERIFICADA (sin DOI)

### Ardura Urquiaga, Lorente Riverola, Mohíno Sanz y Ruiz Sánchez (2019). «No estamos tan mal como Barcelona»: análisis de la proliferación y regulación de las viviendas de uso turístico en Madrid y Barcelona
- DOI: 10.21138/bage.2828 (visto en OpenAlex) · Revista: Boletín de la Asociación de Geógrafos Españoles, n.º 83
- Leído: resumen (https://api.openalex.org/works/doi:10.21138/bage.2828)
- Diseño e identificación: comparación descriptiva del PEUAT de Barcelona (enero de 2017) y del Plan Especial de Hospedaje de Madrid (dos años después) con la oferta publicada en Airbnb: características y distribución temporal, para valorar el grado de turistificación y la adecuación de la zonificación. Sin diseño causal ni resultado de precios.
- Resultado principal, con su magnitud: ambos planes tratan de contener la turistificación residencial de los distritos centrales; las diferencias en criterios de zonificación y una reactivación de aprobaciones tras una posible consolidación de oferta profesionalizada podrían socavar su efectividad. Sin cifras en el resumen.
- Validez externa para España: da la fecha del PEUAT (enero de 2017) y confirma que las zonas de ambos planes son la variación disponible; no estima efecto sobre alquiler. Una fuente en español dató el PEUAT en 2022 (modificación) y el resumen de la tesis de Princeton en marzo de 2017: la fecha de tratamiento debe fijarse sobre el texto de la norma, no sobre estas fuentes.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Autoría no verificada (Princeton DataSpace). DiD de las normas del PEUAT sobre anuncios de Barcelona y Sevilla, 2015-2023
- DOI: sin DOI · Revista: repositorio Princeton DataSpace (handle 88435/dsp01f7623g92j); probable trabajo de fin de grado; no he podido abrir la página (401)
- Leído: resumen del buscador (https://dataspace.princeton.edu/handle/88435/dsp01f7623g92j?mode=full), no la fuente
- Diseño e identificación: según el buscador, DiD sobre 134.960 anuncios de Barcelona y Sevilla, 2015-2023, antes y después de las normas de marzo de 2017; resultados mensuales de precio, oferta y reseñas.
- Resultado principal, con su magnitud: precio −21,03 € (anuncios afectados por el PEUAT), reseñas −8,08 y oferta total −5.582 anuncios, según el buscador. El autor concluye (según el buscador) que las normas no restringieron la oferta pero redujeron demanda y precios. No lo uso en el CSV: sin leer la fuente.
- Validez externa para España: si se confirma, sugiere que el PEUAT no redujo anuncios, lo que choca con la expectativa de tratamiento fuerte; no mide alquiler residencial. Sin revisión por pares ni autoría confirmadas.
- Estado: NO VERIFICADA (sin DOI)

### Calder-Wang (2021). The Distributional Impact of the Sharing Economy on the Housing Market
- DOI: sin DOI · Revista: documento de trabajo (job-market paper, 2021; versión posterior en Harvard JCHS y NBER)
- Leído: resumen del buscador (https://www.jchs.harvard.edu/research-areas/working-papers/distributional-impact-sharing-economy-housing-market devolvió 403; no abrí ningún texto)
- Diseño e identificación: modelo estructural de equilibrio para Nueva York con elección de uso corto o largo por el propietario; contrafactual de restricción de Airbnb.
- Resultado principal, con su magnitud: el buscador da una pérdida de bienestar de los inquilinos de 178 millones de dólares al año en la versión de 2021 y 2.400 millones en una versión posterior, y un efecto «leve y positivo» de unos 125 dólares anuales por inquilino con la restricción (diapositivas de NBER). Las cifras difieren por versión y no las he leído en origen.
- Validez externa para España: contrafactual de regulación con modelo estructural; no es una estimación de diseño y no entra en el CSV. Sirve de aviso de que los efectos en bienestar dependen de la elasticidad de la oferta de vivienda.
- Estado: NO VERIFICADA (sin DOI)

### EsadeEcPol (2024). Insight 53: El mercado de alquiler en España
- DOI: sin DOI · Revista: EsadeEcPol, Insight n.º 53 (noviembre de 2024)
- Leído: resumen del buscador, no el documento (la descarga del PDF devolvió 502; https://esade.edu/ecpol/wp-content/uploads/2024/11/EsadeEcPol_Insight_53_El-mercado-de-alquiler-en-Espana.pdf)
- Diseño e identificación: según el buscador, análisis descriptivo con datos de Idealista del peso del alquiler de temporada en los anuncios de Barcelona; no identificación causal.
- Resultado principal, con su magnitud: cuota del alquiler de temporada en los anuncios del 2,1 % en 2019 y del 14,4 % en 2023, relacionada por el documento con la regulación del alquiler turístico desde 2017 (según el buscador).
- Validez externa para España: es el único dato sobre desplazamiento a temporada localizado; mide cuota de anuncios y no contratos (el propio resumen señala que los portales no siempre distinguen temporada de larga duración). No entra en el CSV.
- Estado: NO VERIFICADA (sin DOI)

---

## Lo que no he podido leer o no he encontrado

- Valero y Van Doorslaer, y Chen et al.: no localicé ningún trabajo con esos autores sobre vivienda turística. No hay ficha; no afirmo su existencia ni sus resultados.
- Ámsterdam (límite de 30 noches): sin trabajo revisado por pares; solo tesis y material de Airbnb, que no uso.
- París (límite de 120 noches): sin estudio independiente de alquiler o precio localizado; solo cifras de la plataforma.
- Berlín: Duso et al. consta en P5 (ficha 4); el borrador DIW DP 1890 (2020) y CEPR DP16150 devolvieron 503 y 403. El buscador atribuye al borrador de 2020 «al menos 7 céntimos por m² y mes» por anuncio cercano: sin leer.
- Nueva York, Local Law 18: solo P5, ficha Dong (cifra de datos internos). Sin otra evaluación leída.
- Wachsmuth y St-Hilaire: PDF de septiembre de 2024 leído solo en resumen e introducción (sin tablas). Cifras en dólares de prensa no verificadas con el texto.
- Madrid (PEH 2019): sin evaluación causal; Plan RESIDE (BOCM, 22-09-2025) lo sustituye, según un resumen del buscador.
- Palma 2018, Baleares, Canarias: sin evaluación causal; solo prensa y descripciones (P5: Yrigoy 2018).
- València (moratoria): ver P5, ficha MESVAL; sin evaluación de impacto.
- Estudio de la Universidad de Málaga (Málaga, Sevilla, Jaén, Teruel): solo conocido por prensa (Xataka, 6-01-2025); no localicé el documento; no lo uso. Las cifras no se citan.
- Regresión discontinua espacial en España: ninguna aplicación localizada.
- AIReF, IVIE: sin estudio propio localizado (IVIE no buscado específicamente).

## 6. Qué sería sorprendente replicar o no replicar en España, y por qué

1. Sería sorprendente un efecto grande de la regulación sobre el alquiler residencial. Los diseños creíbles leídos dan −2 % a −5 % con caídas de anuncios del 30 % al 70 % (Koster et al., 2019, tablas 4 y 9) y un nulo en Santa Monica; con las normas españolas, que topan el parque sin eliminarlo, lo esperable es un efecto menor o no distinguible de cero con la potencia de V15.
2. Sería sorprendente no encontrar efecto negativo sobre el precio de compra en zonas con prohibición o moratoria de nuevas licencias (−3 % a −4 % en Los Ángeles, −8 % en Lisboa, −10 % en tramos más densos de Chicago/San Francisco), pero la magnitud depende de que la licencia se pierda con la venta, lo que no he comprobado para las normas españolas.
3. Sería sorprendente que la regulación española reduzca los anuncios en proporciones como las de Los Ángeles (−50 %) o Nueva York (−90 %): Viena y la tesis sobre el PEUAT apuntan a efectos débiles cuando la aplicación es limitada. Sin variación de tratamiento real, el DiD no tiene primera etapa.
4. Sería sorprendente que en España no haya desplazamiento a alquiler de temporada: el único dato (cuota del 2,1 % al 14,4 % en Barcelona) apunta a ello, pero es descriptivo y mide anuncios. Si el repositorio mide alquiler con contratos de larga duración, el desplazamiento sesga a la baja el efecto de la regulación.
5. Sería sorprendente no hallar desbordamiento a barrios vecinos: en Nueva Orleans y en Canadá aparece; en Los Ángeles no. Un control en el mismo mercado puede estar contaminado; una frontera entre CCAA o entre municipios metropolitanos es más limpia que una frontera entre barrios.
6. Sería sorprendente una elasticidad de densidad sobre alquiler muy fuera de 0,02-0,06 (ver P5). El valor de Koster et al. 2019 de 0,0321 a 0,0575 por p.p. de tasa de anuncios es del mismo orden; no son comparables en unidades.
7. Sería sorprendente que un diseño con RDD espacial sea aplicable sin más: España tiene regulación autonómica uniforme y un solo municipio con zonas (PEUAT) en Barcelona; el RDD exigiría fronteras de zona con alquiler observado a nivel fino, que no he localizado.
8. Un resultado que cambie de signo con la medida (alquiler de oferta, contratos vigentes, precio de compra) no debe leerse como efecto: los trabajos leídos usan alquiler de oferta de portales o Zillow, y el efecto en precio de compra y en alquiler difiere por mecanismo (opción de alquilar frente a oferta).
