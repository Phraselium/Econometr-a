## Parte II · Mecanismos

Esta parte responde a una pregunta: qué se asocia con el precio de compra y con el alquiler, qué sabemos de ello y qué no. Usa un marco teórico (cuatro cuadrantes), la descomposición «por qué ha subido» de la versión 8, la triangulación de V16 y las pistas de V15 y V16 que superan la revisión adversarial. No hay en ella ninguna conclusión sobre una medida concreta: eso va en la Parte III. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

### II.1 Cómo leer esta parte

- **Capas.** Todo lo de V15 y V16 es [C4] (exploratorio o descriptivo). Lo de V8 es [C3s] cuando se dice, y está condicionado a las restricciones de signo que se declaran. Una coincidencia con la literatura no sube la capa. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
- **Lenguaje.** Se escribe «se asocia», «coincide con» y «en la simulación». Nada de lo que sigue identifica un efecto.
- **Pre-registro.** Los resultados de V15 y V16 citados aquí tienen un pre-registro interno, sin sello de tiempo externo. V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. No es un pre-registro depositado. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro) -->
- **Evaluación sellada de V15.** Las hipótesis H1 a H5 de V15 tienen la evaluación sellada pendiente. El calendario está en `docs/v15/preregistro_v15_adenda.md`, sección C, con fecha límite 31-12-2027. Aquí son pistas pendientes, nunca confirmaciones. <!-- check:cifra-libre (números de hipótesis, sección y fecha límite del calendario) -->
- **Literatura.** Cada referencia lleva la etiqueta de su ficha: «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o NO VERIFICADA (sin DOI localizado o de otra agencia). Casi todo se leyó en resumen o en versión de trabajo. Las magnitudes de la literatura no están en `cifras_clave`: por eso aquí se da el signo y se remite a la ficha. Las cifras que faltan se listan en III.11. <!-- check:cifra-libre (apartado III.11) -->

### II.2 El marco: cuatro cuadrantes (DiPasquale y Wheaton)

#### Qué es y qué no es

El modelo de stock y flujo de cuatro cuadrantes conecta cuatro relaciones:

1. el mercado del uso: la demanda de servicios de vivienda fija el alquiler para un stock dado; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
2. el mercado de activos: el alquiler y la rentabilidad exigida fijan el precio; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
3. la construcción: el precio frente al coste fija la obra nueva; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
4. el stock: la obra nueva, menos las bajas, cambia el parque. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

En V16 se calibra para España con rangos declarados y se simula cada shock con Monte Carlo sobre esos rangos (`output/v16/f3/cuatro_cuadrantes.md`, generado por `src/v16/f3_cuatro_cuadrantes.py`). Es un marco teórico calibrado, no una estimación. Dice qué respuesta cabe esperar si el mercado funcionara como el modelo. Capa [C4]. <!-- check:cifra-libre (cuatro cuadrantes: nombre del marco) -->

#### Parámetros: de dónde salen

| Parámetro | Origen | Estado |
|---|---|---|
| Elasticidad de la oferta nueva al precio | Literatura: una estimación por CCAA (Taltavull de la Paz, 2014, DOI verificado, leída en resumen) | Rango de la ficha L3 | <!-- check:cifra-libre (ficha L3) -->
| Elasticidad-precio de la demanda | Supuesto del autor; no hay estimación española leída | Rango amplio a propósito |
| Elasticidad-renta de la demanda | Supuesto del autor; hay una referencia española (Fernández-Kranz y Hon, 2006, DOI verificado) que no se usó para fijar el rango | Rango amplio a propósito |
| Rentabilidad inicial (inversa del cociente precio/alquiler) | `cifras_clave` | Ratio precio/alquiler 2023: {{K3-RATIO-2023:rango}} [C4] |
| Obra nueva sobre el parque cada año | Supuesto del autor; orden de magnitud de las terminadas | Terminadas por año 2019-2024, 52 provincias con País Vasco y Navarra, libres y protegidas (ámbito de E-T7-prod): {{E-T7-prod:rango}} [C4]. En territorio común, sin País Vasco ni Navarra: {{terminadas_1924:min_num}}-{{terminadas_1924:max_num}} [C1] | <!-- check:cifra-libre (52 provincias: ámbito de E-T7-prod) -->
| Retardo entre inicio y fin de obra | `cifras_clave` | {{B2-H5:rango}} [C4]. Solo informativo: el estado estacionario no depende de él |

Tres de los cinco parámetros que mueven los multiplicadores son supuestos del autor. Los rangos son amplios a propósito. Un lector que cambie un supuesto cambia el multiplicador. Las dos series de terminadas tienen ámbitos distintos (con y sin País Vasco y Navarra, y con o sin protegidas): no se comparan entre sí ni se restan. <!-- check:cifra-libre (cinco parámetros y tres supuestos: diseño del marco) -->

#### Qué respuesta cabe esperar de cada shock

Los multiplicadores numéricos (mediana y banda entre los percentiles 5 y 95) están en `output/v16/f3/cuatro_cuadrantes.md` y no están en `cifras_clave`: se consultan allí; el informe no los cita porque no tienen id. Sin cifras, el patrón de signos es este: <!-- check:cifra-libre (percentiles 5 y 95: banda del Monte Carlo) -->

| Shock | A corto plazo (stock fijo) | A largo plazo (stock se ajusta) |
|---|---|---|
| Más demanda (renta u hogares) | Sube el alquiler y sube la obra nueva. El precio sube con el alquiler | Alquiler y precio suben menos; el stock crece |
| Más rentabilidad exigida al comprador (coste de uso: tipo, fiscalidad, revalorización esperada) | Baja el precio y baja la obra nueva. El alquiler no cambia | El precio baja menos; el stock es menor y el alquiler sube |
| Más coste de construcción | Sin efecto inmediato | Suben precio y alquiler; el stock es menor |
| Oferta menos elástica y más demanda | — | El precio sube más y el stock crece menos |

Tres lecturas, todas dentro del marco:

- **El stock tarda décadas en ajustarse.** La semivida del ajuste del stock sale de varias décadas con los rangos declarados, porque la obra nueva anual es una fracción pequeña del parque. A corto plazo el ajuste recae en el precio y el alquiler. El valor de la semivida está en output/v16/f3/cuatro_cuadrantes.md y no se cita aquí, porque no tiene id en cifras_clave. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
- **Los shocks de tipos y de demanda tienen firmas distintas.** Un shock solo de tipos baja precio y obra nueva y deja el alquiler. Un shock solo de demanda sube alquiler, obra nueva y precio.
- **El «tipo exigido» no es el tipo hipotecario.** Es la rentabilidad que pide el comprador. Una subida del hipotecario no se traslada uno a uno.

#### ¿Lo muestran los datos? Episodio de subida de tipos

Comparación descriptiva de las medias de 2024 frente a las de 2022. Es una lectura de signos, no un contraste.

| Serie | Signo observado | Signo si solo cambiaran los tipos |
|---|---|---|
| Tipo hipotecario | + | + |
| Precio de compra (IPV) | + | − |
| Alquiler (IPC) | + | 0 o + | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| Compraventas | − | − |
| Visados de obra nueva | + | − |
| Renta real de los hogares | + | 0 | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
| Hogares (EPA) | + | 0 | <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

Los valores de la variación de cada serie están en `output/v16/f3/cuatro_cuadrantes.md`: se consultan allí; no tienen id en cifras_clave. <!-- check:cifra-libre (años de la comparación) -->

El patrón de un shock solo de tipos no aparece: precio, alquiler y obra nueva suben. El marco es compatible con un shock de demanda simultáneo (hogares, renta) que compense la subida de tipos. Con estos datos no se pueden separar los dos shocks. El intento de separarlos (Q5, sorpresas de política monetaria) no dio señal estable: la primera etapa tiene el signo contrario al esperado y el placebo es comparable a la respuesta. Q5 queda «no concluyente» y no se cita con cifras. <!-- check:cifra-libre (identificador de pregunta) -->

#### Dónde falla el marco

- No hay elasticidad municipal de la oferta identificada para España. Q4 (restricción física, Red Natura) no produjo ningún hallazgo: la inferencia con agrupación provincial no es apta y el placebo de choque adelantado es del mismo signo y de mayor tamaño que la estimación. Queda «sin hallazgo». <!-- check:cifra-libre (identificador de pregunta) -->
- Los parámetros españoles de la demanda quedan como supuestos.
- El marco es de equilibrio y de un solo mercado. No modela la segmentación entre contratos nuevos y vigentes, ni el alquiler de temporada, ni los cambios de uso.
- No se calibró para las grandes áreas urbanas, aunque el plan lo preveía: no hay series de parque, terminadas y coste de uso por área urbana con la cobertura necesaria. Está declarado en la desviación D9 (anexo C), anotada después de ver los resultados. <!-- check:cifra-libre (desviación D9 y anexo C) -->

### II.3 La descomposición «por qué ha subido» de V8

#### Qué hizo V8

V8 descompuso la variación del precio real de compra y del alquiler real en cinco periodos, con un SVAR con restricciones de signo y de cero (M2), y contrastó cada factor con una regla fijada de antemano (la regla del apartado 9: coincidencia entre métodos, bandas y falsación). Los factores son demografía, empleo y renta, crédito y tipos, oferta, demanda externa y turismo. Todo se condiciona a esas restricciones. <!-- check:cifra-libre (cinco periodos P1 a P5 y apartado 9: diseño de V8) -->

#### Resultado: ningún factor designado

- **Ningún factor queda designado.** La regla del apartado 9 no designa a ningún factor en ninguno de los periodos, ni en compra ni en alquiler. En el último periodo (P5, desde 2022T3) la regla da {{V8-REGLA-c-P5:num}} en compra y {{V8-REGLA-a-P5:num}} en alquiler (1 = designado, 0 = no designado) [C4]. <!-- check:cifra-libre (P5 es el nombre del periodo; codificación 1 y 0) -->
- **La contribución de cada factor tiene una banda que contiene el cero.** Ejemplos del último periodo, con el intervalo del 95 %: <!-- check:cifra-libre (nivel del intervalo) -->
  - demografía y alquiler real: {{V8-H8-1-est:valor}}, intervalo {{V8-H8-1-est:rango}} [C3s]; p ajustado por Holm {{V8-H8-1-pholm:num}} [C3s]. No respaldada; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
  - crédito y tipos y precio real de compra: {{V8-H8-2-est:valor}}, intervalo {{V8-H8-2-est:rango}} [C3s]; p ajustado por Holm {{V8-H8-2-pholm:num}} [C3s]. No respaldada. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

#### La parte no atribuida

La «cuota no atribuida» es la parte de la variación observada que el SVAR no asigna a ningún factor identificado: su componente determinista y lo no identificado. Para el precio real de compra en el último periodo:

- media posterior: {{V8-QNA-pp-c-P5:valor}} [C3s]; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
- mediana posterior: {{V8-QNA-pp-c-P5-med:num}} pp [C3s]; <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
- banda del 68 % exacta, calculada con los cuantiles de la suma: {{V8-QNA-pp-c-P5:rango}} [C3s]; <!-- check:cifra-libre (nivel de la banda) -->
- sensibilidad, con el tipo hipotecario del Banco de España en lugar del BCE: media {{V8-QNA-pp-c-P5-bde:num}} pp [C3s]. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

La media está muy por encima de la mediana porque la cola derecha es pesada. Por eso se dan las dos y la banda. La sensibilidad al tipo hipotecario elegido es grande en la media y pequeña en la mediana: se reportan ambas. Esta cifra se corrigió en V16 (errata de la banda exacta, aplicada en ERRATA.md).

Como proporción de la variación observada, la parte no atribuida del precio de compra en el último periodo es {{V8-QNA-c-P5}} [C3s]. Para el alquiler real, en puntos, es {{V8-QNA-pp-a-P5:valor}} con banda {{V8-QNA-pp-a-P5:rango}} [C3s]. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->

**Lectura.** La descomposición no permite decir qué factor ha pesado más en la subida. Una parte grande y de signo incierto queda sin atribuir, y ninguna contribución se separa de cero tras el control de múltiples contrastes. Esto no dice que los factores no importen: dice que esta descomposición, con estos datos, no los separa.

#### Lo que V16 añade: comovimiento y contabilidad (descriptivo)

V16 no repite la descomposición. Añade tres descripciones que ayudan a leerla [C4]:

- **Una parte grande del crecimiento del valor tasado es común a las provincias.** La cuota del primer factor común en la varianza del crecimiento interanual de 33 provincias es {{V16-CON-PRECIO-CUOTA-PC1-2007-2013:valor}} en 2007-2013, {{V16-CON-PRECIO-CUOTA-PC1-2014-2019:valor}} en 2014-2019 y {{V16-CON-PRECIO-CUOTA-PC1-2020-2026:valor}} en 2020-2026 [C4]. La correlación media de los residuos locales entre provincias de la misma comunidad es baja: {{V16-CON-PRECIO-LOCAL-CCAA:valor}} [C4]. Con provincias en lugar de comunidades, la cuota común es menor que la de V8: diferencia media {{V16-CON-PRECIO-V8-DIF-PUNTOS:valor}} [C4]. Esto describe el comovimiento. No dice qué lo mueve. <!-- check:cifra-libre (33 provincias, periodos) -->
- **Contabilidad del número de hogares, 2021-2025.** El cambio observado, con las dos fuentes alineadas al 1 de enero, es {{V16-CON-HOG-CAMBIO:valor}} [C4], con rango entre ECP y EPA {{V16-CON-HOG-CAMBIO:rango}} [C4]. Según la descomposición de Shapley, el tamaño de la población aporta {{V16-CON-HOG-POBLACION:valor}} [C4], la estructura por edad {{V16-CON-HOG-ESTRUCTURA-EDAD:valor}} [C4], el residuo de jefatura {{V16-CON-HOG-JEFATURA:valor}} [C4] y la composición por nacionalidad {{V16-CON-HOG-COMPOSICION-NACIONALIDAD:valor}} [C4]. Es contabilidad, no una estimación de efectos. En esa ventana, la EPA da un cambio mayor que la ECP en {{V16-CON-HOG-ECP-EPA-DISCREPANCIA:valor}} [C4]: se dan las dos fuentes. <!-- check:cifra-libre (periodo, 1 de enero) -->
- **Obra frente a hogares.** Las viviendas libres terminadas en 2021-2025 por hogar nuevo son {{V16-HEC-OBRA-SOBRE-HOGARES-2125:valor}} [C4], con {{V16-HEC-OBRA-TERMINADAS-2125:valor}} terminadas en el periodo [C4]. Es un cociente de flujos. No dice cuánta vivienda falta: la necesidad de vivienda se trata en la Parte V. <!-- check:cifra-libre (periodo) -->

### II.4 Triangulación de V16

La fase 6 compara cada resultado con la literatura y con otros diseños del mismo proyecto (`output/v16/triangulacion/informe.md`). Reglas: se compara el signo y, solo si la unidad coincide, el orden de magnitud. No hay metaanálisis, porque ningún grupo de resultados reúne estudios suficientes con error estándar y la misma unidad (decisión K7). Los 88 grupos de la literatura se quedan en rangos sin agregar. Ningún resultado sube de capa por coincidir con la literatura. <!-- check:cifra-libre (88 grupos y decisión K7: diseño del metaanálisis) -->

#### Entre diseños del propio proyecto

| Pareja | Mismo signo |
|---|---|
| H1: Callaway-Sant'Anna y SDID (zonas tensionadas y renta de contratos nuevos, Cataluña) | Sí |
| H3 y Q2a (vivienda turística y alquiler, sección y provincia) | Sí |
| H3 y Q2c (vivienda turística y alquiler, sección y municipio) | No |
| H4 y Q3-c1 (inmigración y alquiler municipal; inmigración y valor tasado provincial) | Sí |
| H4 y Q3-b (inmigración y alquiler municipal; inmigración y alquiler por sección) | Sí |

Que dos diseños coincidan en el signo no los convierte en independientes: comparten datos, periodo y, a veces, el mismo shock de origen.

#### Frente a la literatura

| Resultado | Estado | Lectura frente a la literatura |
|---|---|---|
| H1 (zonas tensionadas, renta de contratos nuevos) | Pista, solo el signo [C4] | Mismo signo. Las unidades no son comparables: solo se compara el signo |
| H2 y Q1c (zonas tensionadas, contratos y compraventas) | Ruido previo; no se citan | Sin señal estable |
| H3 y Q2a (vivienda turística) | No concluyente [C4] | Mismo signo; unidades no comparables |
| Q2c (vivienda turística, IPVA municipal) | No se cita | Signo opuesto al de la literatura, sin inferencia válida; se lee como robustez nula de H3 |
| H4 y Q3-b (inmigración) | Correlaciones frágiles [C4] | Sin comparación numérica con la literatura leída |
| Q6-v (ITP y compraventas) | Descriptivo | Se aparta de la literatura: el placebo con el resultado retardado es de signo contrario y mayor que la estimación, y los cambios de tipo se concentran en la crisis. El diseño no separa el ITP del ciclo |
| Q6-p (ITP y valor tasado) | No concluyente [C4] | Mismo signo; unidades no comparables |
| Q5-p (sorpresas monetarias y valor tasado) | No se cita | Sin comparación |

#### Qué se cita y con qué límites

**H1 de V15: solo el signo.** La asociación de la zona tensionada con la renta media de los contratos nuevos en Cataluña es negativa en los dos diseños (Callaway-Sant'Anna y SDID). No se cita ninguna magnitud: el placebo temporal y las pretendencias fallan, y las cotas no la permiten. Además hay anticipación y reversión por la sentencia del Tribunal Constitucional, selección de municipios y paso de contratos a temporada. La evaluación sellada está pendiente. [C4]

**H5 de V15: la combinación no supera al AR(4).** La razón del error cuadrático medio de la combinación frente al AR(4), en el valor tasado a un trimestre, es {{V15-H5-razon-ecm:num}} en la implementación pre-registrada [C4]. En la réplica ciega es {{V15-H5-razon-replica:num}}. El rango entre implementaciones es {{V15-H5-razon-replica:min_num}} a {{V15-H5-razon-replica:max_num}} [C4]: en ambas la razón queda por encima de uno. El multiverso de 60 especificaciones, que mezcla medidas y horizontes, va de {{V15-H5-razon-ecm:min_num}} a {{V15-H5-razon-ecm:max_num}} [C4]; no es un rango entre implementaciones. Se dice «la combinación no supera al AR(4)». No se dice «el AR(4) es mejor». El contraste de Diebold-Mariano no se cita como prueba. La evaluación sellada está pendiente. <!-- check:cifra-libre (AR(4): nombre del modelo; 60 especificaciones: tamaño del multiverso) -->

**E3 de V15: correlación espacial descriptiva, no contagio.** El parámetro autorregresivo espacial ρ (contigüidad, variación de la renta de alquiler de 1.124 municipios en 2015-2024) es {{V15-E3-rho:num}}, con rango del multiverso de {{V15-E3-rho:min}} a {{V15-E3-rho:max}} [C4]. Puede reflejar una tendencia regional común. El intervalo no recoge la incertidumbre de especificación: se cita el rango del multiverso. <!-- check:cifra-libre (1.124 municipios y periodo: diseño de E3) -->

**H4 de V15 y Q3-b de V16: correlaciones frágiles.** Ambas son asociaciones entre la presencia de población extranjera y el alquiler. No se leen como el efecto de la inmigración.
- **H4.** La asociación (2SLS) entre población extranjera predicha y alquiler municipal es {{V15-H4-beta:valor}}, con rango del multiverso {{V15-H4-beta:rango}} [C4]. El rango contiene el cero y el signo cambia al quitar los orígenes principales. Hay pocos orígenes efectivos: {{V15-H4-neff:num}} choques efectivos [C4]. El 2SLS es varias veces el MCO. La mediana del multiverso es {{V15-H4-mediana:valor}} [C4]. <!-- check:cifra-libre (2SLS: nombre del estimador) -->
- **Q3-b.** La asociación transversal del alquiler por sección con la cuota de extranjeros es {{V16-Q3-b-beta:sig}} log por desviación típica [C4]; es la mayor de las seis variantes del multiverso. El coeficiente de pretendencia (variación previa) es {{V16-Q3-b-pretendencia:sig}} [C4], más de la mitad del coeficiente principal. Puede haber reversión a la media o convergencia, y la exposición de 2022 cae dentro de la ventana del resultado. La mediana del multiverso es {{V16-Q3-b-mediana:sig}} [C4], menor que el coeficiente principal. <!-- check:cifra-libre (seis variantes del diseño, «más de la mitad») -->
- **Literatura.** La literatura con DOI verificado sobre inmigración y vivienda no tiene un signo único. Mussa, Nwaogu y Pozo (2017) asocian más entradas con alquileres y precios más altos. El metaanálisis de Larkin et al. (2019) halla que la inmigración sube los precios en conjunto, más a escala provincial. Sá (2015) y Saiz y Wachter (2011) hallan, en cambio, precios más bajos o una apreciación más lenta. Para España, Torres-Téllez y Montero-Soler (2023) asocian la llegada de inmigrantes con alquileres más altos. Las cinco referencias tienen DOI verificado y cuartil no verificado (ficha P4 de V15). Miden en unidades distintas y con otras muestras: no se compara la magnitud. <!-- check:cifra-libre (ficha P4) -->

**H3, Q2a y Q6-p: no concluyentes.** No concluyente no es «nulo». H3 (vivienda turística y alquiler por sección) tiene un coeficiente principal que es el mínimo de su multiverso y no tiene error estándar válido. Q2a (provincial) depende de los controles. Q6-p (ITP y valor tasado) fue pista hasta su réplica ciega, que corrigió un error de diferencias entre años no consecutivos.

**Exuberancia de precios.** Se trata en la Parte VII, con sus advertencias.

### II.5 Qué se asocia con qué: síntesis por canal

Cada canal se juzga con lo que la evidencia permite. «Literatura» es la ficha con DOI verificado de V15 o V16; «nuestro dato» es lo de V15, V16 o la 1.0.

| Canal | Mecanismo | Literatura | Nuestro dato | Estado |
|---|---|---|---|---|
| Demanda: hogares y renta | Más hogares o más renta suben alquiler y precio a corto plazo | Marco de cuatro cuadrantes; Fernández-Kranz y Hon (2006, DOI verificado) sobre la elasticidad-renta | Contabilidad de hogares; V8 no designa ningún factor | Compatible, no separado |
| Demanda: inmigración | Más hogares en alquiler y compra | Signo no unívoco (Mussa et al., 2017; Larkin et al., 2019; Sá, 2015; Torres-Téllez y Montero-Soler, 2023, todas con DOI verificado) | H4 y Q3-b, correlaciones frágiles | Correlación frágil [C4] |
| Tipos de interés | Más tipo exigido, menos precio y menos obra | Marco de cuatro cuadrantes | V8 no designa crédito y tipos; Q5 no concluyente | No separado de la demanda |
| Oferta y suelo | Oferta rígida, más precio ante un shock de demanda | Saiz (2010); Hilber y Vermeulen (2016); Caldera Sánchez y Johansson (2013), todas con DOI verificado | Q4 sin hallazgo; elasticidad municipal sin identificar | No evaluable con los datos disponibles |
| Vivienda turística | Cambio de uso: menos oferta residencial, más alquiler | García-López et al. (2020, Barcelona); Barron et al. (2021), ambas con DOI verificado | H3 y Q2a no concluyentes; Q2c no se cita | No concluyente [C4] |
| Regulación del alquiler | Tope en el contrato regulado, posibles desbordamientos | Ver Parte III | H1: signo | Pista, solo el signo [C4] |
| Fiscalidad de la compra | Un impuesto sobre la transmisión cambia volumen y, en parte, precio | Best y Kleven (2018); Besley et al. (2014), ambas con DOI verificado | Q6-v descriptivo; Q6-p no concluyente | No evaluable |
| Compradores no residentes | Más demanda de compra | Badarinza y Ramadorai (2018); Cvijanović y Spaenjers (2021), ambas con DOI verificado | Q8 descriptivo | No evaluable |
| Fundamentales y burbuja | Precio frente a alquiler y renta | — | La exuberancia se trata en la Parte VII | Ver Parte VII |

### II.6 Qué no sabemos

- **Qué factor pesa más en la subida reciente.** V8 no designa ningún factor y deja una parte sin atribuir. V16 no mejora esa descomposición.
- **El tamaño de ningún efecto de una medida en España.** Todo lo de V15 y V16 es [C4]. Las pistas son signos.
- **Si el patrón de 2022-2024 viene de la demanda, de los tipos o de ambos.** Q5 no los separa.
- **La elasticidad de la oferta municipal.** No hay estimación identificada.
- **Cuánto del comovimiento de precios entre provincias es un factor común y cuánto es una tendencia compartida.** El análisis de factores describe, no identifica.
- **Qué parte del cambio de hogares es formación y qué parte es cambio de jefatura.** La contabilidad da un residuo con rango.

Todo esto se actualiza cuando llegue la evaluación sellada de V15 (calendario en `docs/v15/preregistro_v15_adenda.md`, sección C). Hasta entonces, las hipótesis de V15 están pendientes. <!-- check:cifra-libre (sección C del calendario) -->
