# Necesidades de vivienda por provincia en España, 2026-2035: una contabilidad por componentes con rangos y con la vivienda que liberará el envejecimiento

**Borja Romero, economista.** Borrador de artículo (v5). Todas las cifras proceden de `output/v5/cifras_clave.csv`; cada afirmación lleva su capa de evidencia entre corchetes.

## Resumen

Este artículo estima cuántas viviendas harán falta al año en cada una de las provincias españolas entre 2026 y 2035 mediante una contabilidad stock-flujo por componentes: atraso acumulado, reposición del parque, vacancia friccional y crecimiento de hogares, menos las viviendas vacías movilizables y la cartera en construcción. Cada componente se presenta con un mínimo, un valor central y un máximo, y la capa del total es la menor de sus componentes. La necesidad central agregada es de {{E-B1-anual}} [C4], con un crecimiento de hogares proyectado por el INE de {{E-B1-F}} en diez años [C2]. El artículo cuantifica además las viviendas que quedarán disponibles por la disolución de hogares de personas mayores, {{E-B1-L}} en diez años [C4], y argumenta por qué esa cifra no debe restarse del crecimiento de hogares: la proyección del INE ya es neta de disoluciones, y restarla de nuevo daría una necesidad de {{E-B1-N10_formula_literal_menos_L}} en diez años [C4], una cifra que cuenta dos veces el mismo fenómeno. Una proyección complementaria a 2030 indica que, al ritmo de terminaciones de 2023-2025, el déficit empeora en {{E-B2-empeora}} y mejora en {{E-B2-mejora}}, mientras que en {{E-B2-indeterminado}} el signo depende de los supuestos [C4]. Los resultados son una contabilidad con supuestos explícitos, no un pronóstico ni una estimación de efectos.

**Palabras clave:** necesidad de vivienda, proyección de hogares, envejecimiento, provincias, identificación parcial.

## Abstract

This paper estimates annual housing needs for each Spanish province over 2026-2035 using a component-based stock-flow accounting framework: accumulated backlog, replacement of the stock, frictional vacancy and household growth, net of mobilisable vacant dwellings and the construction pipeline. Each component is reported as a minimum, central and maximum value, and the evidence layer of the total is the weakest of its components. The central aggregate need is {{E-B1-anual}} [C4], with official household growth of {{E-B1-F}} over ten years [C2]. We also quantify the dwellings that will be released by the dissolution of elderly households, {{E-B1-L}} over ten years [C4], and show why this figure must not be subtracted from household growth: the official projection is already net of household dissolutions, so subtracting it again would yield {{E-B1-N10_formula_literal_menos_L}} over ten years [C4], double counting the same flow. A complementary projection to 2030 shows that, at the 2023-2025 completion rate, the backlog worsens in {{E-B2-empeora}}, improves in {{E-B2-mejora}} and is undetermined in {{E-B2-indeterminado}} [C4]. Results are accounting under explicit assumptions, not forecasts or identified estimates.

**Keywords:** housing need, household projections, ageing, provinces, partial identification.

## Introducción

La pregunta «cuántas viviendas hacen falta» aparece en el debate público con cifras muy distintas. Parte de la dispersión procede de que se mezclan conceptos: el déficit acumulado (un stock), el crecimiento de hogares (un flujo), las viviendas vacías (un stock cuya movilización es incierta) y la reposición del parque (un flujo difícil de medir). Otra parte procede de que las cifras se presentan como puntos y no como rangos, y de que rara vez se dice qué componente descansa en una sola fuente.

Este artículo ofrece una contabilidad explícita, provincia a provincia, con tres propiedades. Primera, cada componente se calcula por separado y se publica con su rango, de modo que el lector puede sustituir cualquier supuesto. Segunda, la capa de evidencia del total es la menor de las capas de sus componentes, lo que impide que una cifra robusta (el crecimiento de hogares del INE, [C2]) preste su solidez a componentes de fuente única. Tercera, se incorpora de forma explícita la vivienda que liberará el envejecimiento, un flujo grande que suele invocarse como solución y cuya relación con la proyección de hogares rara vez se aclara.

La contribución principal es doble. Por un lado, una tabla provincial de necesidades 2026-2035 con rangos y con control de que la suma provincial coincide con el total nacional (`output/v5/B1/control_sumas.json`). Por otro, la demostración contable de que la vivienda liberada por envejecimiento ya está descontada en la proyección oficial de hogares, con lo que restarla otra vez infravalora la necesidad.

El artículo se organiza así: la sección de datos describe las fuentes y sus fechas; la de método, la fórmula y la construcción de cada rango; la de resultados presenta el agregado, la distribución provincial y la proyección a 2030; la de robustez muestra las variantes; la discusión trata la vivienda liberada y los límites; la conclusión resume lo que se puede y lo que no se puede afirmar.

## Datos

Las fuentes son públicas y se descargan con fecha de consulta registrada (`output/v5/B1/registro.csv`):

- **Hogares.** INE, Proyección de Hogares (base 1 de enero de 2026), por provincia. Es el único componente con dos fuentes comparables en el periodo base y por eso alcanza la capa [C2].
- **Población y mortalidad.** INE, Proyecciones de Población 2024-2074 (corto plazo) y tablas de mortalidad provinciales de 2024, usadas para el componente de envejecimiento.
- **Parque y viviendas vacías.** Censo de Población y Viviendas 2021 (1 de noviembre de 2021): viviendas totales, principales, vacías y de uso esporádico, y viviendas en alquiler.
- **Construcción.** MIVAU, viviendas iniciadas y terminadas (libres y protegidas) hasta 2025.
- **Bajas del parque.** Censo 2011-2021 y Catastro (estadísticas urbanas, ejercicios 2012-2025), cada uno combinado con las terminadas del MIVAU.
- **Déficit de partida.** Módulo A4 del proyecto (déficit 2021-2025 por provincia, con bajas nulas) y clasificación de presión de las provincias.

El déficit agregado de partida se apoya en el aumento de hogares de 2021-2025, {{dh_2125:cita}}, y en la conciliación de v4 entre las cifras de distintos organismos. Los componentes de hogares compartidos, hacinamiento y habitaciones compartidas no tienen dato provincial accesible y quedan fuera; el rango es, por tanto, incompleto por arriba.

## Método

### La identidad contable

La necesidad acumulada en diez años de cada provincia se define como

N = A + R + V + F − M − K,

donde A es el atraso (déficit acumulado 2021-2025 más emancipación retrasada), R la reposición del parque, V el ajuste de vacancia friccional, F el crecimiento de hogares proyectado, M las viviendas vacías movilizables en zonas con presión y K la cartera en construcción. La vivienda liberada por envejecimiento, L, se calcula aparte y **no se resta** en la especificación principal (véase la discusión). El documento de método completo está en `output/v5/B1/metodo.md`.

### Construcción de cada componente

- **Atraso (A).** Suma del déficit 2021-2025 del módulo A4 (A1, {{E-B1-A1}} en el conjunto de provincias) y de la emancipación retrasada respecto a la tasa de jefatura de referencia (A2, {{E-B1-A2}}) [C4]. Se absorbe en los diez años del horizonte.
- **Reposición (R).** Dos métodos: bajas implícitas entre el Censo 2011 y el de 2021 más las terminadas, y bajas implícitas en Catastro más las terminadas. Las tasas negativas se acotan a cero. En {{E-B1-Rnopos}} ambos métodos dan tasas brutas de baja no positivas: el stock censal o catastral crece más que las terminadas. Por eso R es un límite inferior poco informativo, {{E-B1-R}} [C4], y no una medición.
- **Vacancia friccional (V).** Sobre el parque en alquiler del Censo 2021, entre el cero y el cuatro por ciento con valor central del dos por ciento, solo en zonas con presión: {{B1-H5}} [C4].
- **Crecimiento de hogares (F).** Proyección del INE, con un escenario alternativo de tasas de jefatura constantes que define el mínimo: {{E-B1-F}} [C2].
- **Vacías movilizables (M).** Entre el diez y el treinta por ciento de las viviendas vacías censales en provincias con presión: {{E-B1-M}} [C4].
- **Cartera (K).** Iniciadas menos terminadas en los dos o tres años previos: {{E-B1-K}} [C4].
- **Vivienda liberada (L).** Tasa de disolución de hogares encabezados por personas de setenta y cinco años o más, a partir de las tablas de mortalidad y de la tasa de jefatura disponible (la de sesenta y cinco y más, con un factor de ajuste entre ±quince por ciento): {{E-B1-L}} [C4].

### Rangos y capa

El mínimo del total combina los componentes que suman en su mínimo y los que restan en su máximo; el máximo, al revés. Son cotas, no intervalos de confianza: no hay un modelo de muestreo detrás, sino supuestos. La capa del total es la menor de sus componentes ([C4]), aunque F sea [C2]. No hay contrastes de hipótesis, por lo que el control de falsos descubrimientos no aplica; todas las especificaciones están registradas en `output/v5/B1/registro.csv`. Tampoco aplica la comparación fuera de muestra frente a AR(4) o el ECM de v1, porque no se trata de un modelo predictivo.

### Proyección a 2030 (módulo B2)

Para responder si el déficit se cierra al ritmo actual, se proyecta D(2030) = D(2025) + F − T + B por provincia, con F el crecimiento de hogares 2026-2030, T las terminadas y B las bajas. T tiene tres escenarios: (a) cinco veces la media 2023-2025, (b) la cartera de iniciadas con el retardo medio nacional entre iniciación y terminación, {{B2-H5}}, y (c) una tendencia, solo como sensibilidad. El signo de cada provincia se clasifica como «empeora», «mejora» o «indeterminado» según el rango completo.

## Resultados

### Agregado nacional

La necesidad acumulada en 2026-2035 es de {{E-B1-N10}} [C4], es decir, {{E-B1-anual}} [C4]. El componente de mayor tamaño es el crecimiento de hogares, {{E-B1-F}} [C2], seguido del atraso, {{B1-H2}} [C4]. Las vacías movilizables restan {{E-B1-M}} [C4] y la cartera en construcción {{E-B1-K}} [C4].

El rango es amplio: el máximo multiplica el mínimo por más de tres. La mayor parte de la amplitud procede de dos supuestos que no se pueden contrastar con los datos disponibles: la fracción de vacías que se movilizaría y la tasa de jefatura de referencia para la emancipación retrasada.

Como referencia del ritmo actual, las terminadas al año en el territorio común en 2019-2024 estuvieron entre {{terminadas_1924:rango}} ({{terminadas_1924:periodo}}; {{terminadas_1924:fuentes}}; dato de {{terminadas_1924:fecha_dato}}; {{terminadas_1924:capa}}). La comparación con la necesidad central indica una brecha anual del orden de varias decenas de miles de viviendas en el escenario central [C4].

### Distribución provincial

La necesidad se concentra en las provincias con presión. De las provincias españolas, {{E-B1-npresion}} se clasifican con presión en A4, y en ellas se acumula una necesidad de {{E-B1-N10_solo_presion_central}} en diez años [C4], prácticamente todo el total. Por clases de A4, las provincias donde falta vivienda y construir es rentable suman {{D2-H01}} [C4]; aquellas donde falta y hay freno regulatorio o de suelo, {{D2-H02}} [C4]; y aquellas donde falta y construir no es rentable, {{D2-H03}} [C4].

En la Comunitat Valenciana la necesidad central anual es de {{E-B1-anual-Valencia}} en la provincia de Valencia, {{E-B1-anual-Alicante}} en la de Alicante y {{E-B1-anual-Castellon}} en la de Castellón [C4]. Como comparación, Madrid registra {{E-B1-anual-Madrid}} y Barcelona {{E-B1-anual-Barcelona}} [C4].

![Necesidad anual de vivienda por provincia, 2026-2035 (C4)](B1/figuras/B1_mapa_necesidad.png)

La tabla provincial completa, con mínimo, central y máximo de cada componente, está en `output/v5/B1/tablas/B1_tabla_provincial.csv`.

### Proyección a 2030

En el escenario (a), con terminadas iguales a cinco veces la media 2023-2025 ({{B2-H4}}), el déficit acumulado a fin de 2030 alcanza {{B2-H1}} [C4], frente a un déficit de partida de {{B2-H2}} [C4] y un crecimiento de hogares en el quinquenio de {{B2-H3}} [C2]. En el escenario (b), en que la cartera de iniciadas llega a terminarse con el retardo medio, las terminadas suben a {{E-B2-Tb}} y el déficit a fin de 2030 queda en {{E-B2-D2030-b}} [C4].

Con el rango completo, el déficit empeora en {{E-B2-empeora}}, mejora en {{E-B2-mejora}} y es indeterminado en {{E-B2-indeterminado}} [C4]. Ninguno de los escenarios centrales cierra el déficit agregado antes de 2030 [C4].

![Signo del cambio del déficit 2025-2030 por provincia (C4)](B2/figuras/B2_mapa_signo.png)

## Robustez

- **Fórmula literal.** Si se resta L además de F, la necesidad de diez años cae a {{E-B1-N10_formula_literal_menos_L}} [C4]. Se publica como variante para mostrar la magnitud del doble cómputo, no como estimación alternativa.
- **Solo provincias con presión.** Si se limita la contabilidad a las provincias con presión, el total apenas cambia: {{E-B1-N10_solo_presion_central}} [C4].
- **Reposición.** Con los dos métodos de bajas, el componente R se mueve entre {{E-B1-R:min}} y {{E-B1-R:max}} [C4]; el resultado agregado es poco sensible a R porque es pequeño frente a A y F.
- **Vacías.** La fracción movilizable es el supuesto más influyente. Con el diez por ciento, M resta {{E-B1-M:min}}; con el treinta por ciento, {{E-B1-M:max}} [C4]. La mediana municipal del porcentaje de vacías en el Censo 2021 es {{R1C-021}} [C4], con gran dispersión entre municipios.
- **Escenario de terminadas.** El escenario (c), de tendencia, no entra en el rango principal; su resultado nacional cae entre los de (a) y (b).
- **Contraste con organismos.** El módulo D3 compara las cifras clave con las de organismos públicos y privados: {{D3-coincide:num}} coinciden, {{D3-difiere:num}} difieren y {{D3-no_comparable:num}} no son comparables por concepto o periodo [C4].

## Discusión

### Por qué la vivienda liberada por envejecimiento no se resta del crecimiento de hogares

La vivienda que liberará la disolución de hogares de personas mayores es grande: {{E-B1-L}} en diez años [C4], de las que {{E-B1-L_en_presion_central}} en provincias con presión [C4]. En el debate se invoca a menudo como si esa vivienda fuese a cubrir la demanda nueva. La contabilidad muestra por qué ese razonamiento cuenta dos veces.

La proyección de hogares del INE es un saldo: hogares que se forman menos hogares que se disuelven. Cuando un hogar unipersonal de una persona de ochenta y cinco años se disuelve, el INE lo descuenta del número de hogares del año siguiente. El crecimiento proyectado F ya es, por tanto, neto de esas disoluciones. Si F es el aumento del número de hogares y cada hogar necesita una vivienda, la necesidad de vivienda nueva por crecimiento de hogares es F, no F − L: la vivienda liberada ya está «usada» por los hogares nuevos que compensan los que desaparecen. Restar L de nuevo supondría que cada vivienda liberada sirve dos veces: una para compensar la disolución dentro de F y otra para un hogar adicional.

Hay dos matices. Primero, la vivienda liberada no está necesariamente donde se forman los hogares nuevos: una parte se encuentra en municipios sin presión. La necesidad provincial no recoge esa desalineación dentro de la provincia, que puede ser relevante. Segundo, la vivienda liberada puede no salir al mercado (herencias indivisas, uso esporádico); en ese caso aumentaría el stock de vacías y entraría, si acaso, a través de M. Ninguno de los dos matices justifica restar L de F; ambos son razones para vigilar el componente M.

La implicación para el verificador es directa: la afirmación «la vivienda que dejan los mayores resolverá el problema de la vivienda» recibe el veredicto ANALIZADA, NO CONCLUYENTE [C4] (ficha `B1-V2`), porque la contabilidad no permite afirmar que ese flujo cubra la necesidad; en la proyección oficial ya está compensado por la formación de hogares.

### Límites

1. **Fuente única.** Casi todos los componentes salvo F proceden de una sola fuente o de supuestos no contrastados; de ahí la capa [C4] del total.
2. **Componentes omitidos.** Hogares compartidos, hacinamiento y habitaciones compartidas no tienen dato provincial; la necesidad máxima está infravalorada.
3. **Hogares sin reacción a la oferta.** La proyección del INE no responde a los precios ni a la construcción: si se construyese más, se formarían más hogares, y viceversa. La necesidad es, en ese sentido, una cota inferior de la demanda potencial.
4. **Reposición.** R es un límite inferior no informativo: los dos métodos no detectan bajas netas en la mayoría de provincias.
5. **Interpretación.** Nada de lo anterior es un efecto: describe magnitudes bajo supuestos.

### Relación con la literatura

La literatura sobre la respuesta de la oferta (Caldera y Johansson, 2013) muestra que la elasticidad de la oferta de vivienda en España es baja en comparación internacional; si la oferta responde poco, la brecha entre necesidad y terminadas se traduce en precios más que en cantidades. Este artículo no estima esa elasticidad: se limita a la contabilidad. La relación entre población y precios (Saiz, 2007; Sá, 2015) sugiere que el componente F se asocia con presión de precios en el corto plazo, pero esa asociación no se estima aquí.

## Conclusión

La necesidad de vivienda en España en 2026-2035 se sitúa, en el escenario central, en {{E-B1-anual}} [C4]. El crecimiento de hogares proyectado por el INE es la pieza más sólida, {{E-B1-F}} [C2]; el resto descansa en supuestos explícitos que el lector puede cambiar. La vivienda liberada por envejecimiento es grande pero ya está descontada en esa proyección y no debe restarse otra vez. Al ritmo de terminación de 2023-2025, el déficit no se cierra en el agregado antes de 2030 en ninguno de los escenarios centrales [C4], y la necesidad se concentra en las provincias con presión.

**Lo que no se puede afirmar con estos datos:** que una política concreta cerraría la brecha; que la vivienda vacía o la liberada cubrirán la necesidad; ni ninguna cifra puntual sin su rango.

## Referencias

- Caldera, A. y Johansson, Å. (2013). The price responsiveness of housing supply in OECD countries. *Journal of Housing Economics*. [DOI](https://doi.org/10.1016/j.jhe.2013.05.002). VERIFICADA (Crossref) · Q2.
- Saiz, A. (2007). Immigration and housing rents in American cities. *Journal of Urban Economics*. [DOI](https://doi.org/10.1016/j.jue.2006.07.004). VERIFICADA · Q1.
- Sá, F. (2015). Immigration and house prices in the UK. *The Economic Journal*. [DOI](https://doi.org/10.1111/ecoj.12158). VERIFICADA · Q1.
- Garriga, C., Manuelli, R. y Peralta-Alva, A. (2019). A macroeconomic model of price swings in the housing market. *American Economic Review*. [DOI](https://doi.org/10.1257/aer.20140193). VERIFICADA · Q1.
- INE (2026). Proyección de Hogares; Proyecciones de Población 2024-2074; Censo de Población y Viviendas 2021. Fuente estadística oficial (sin DOI).
- MIVAU (2026). Boletín estadístico en línea: viviendas iniciadas y terminadas. Fuente estadística oficial (sin DOI).

## Revistas adecuadas

- *Journal of Housing Economics* — Q2 (registrado en `docs/literatura.md`, Scimago).
- *Regional Science and Urban Economics* — Q1 (registrado en `docs/literatura.md`, Scimago).
- *Housing Studies* — cuartil no verificado (no se pudo comprobar en Scimago en esta sesión).
- *Investigaciones Regionales – Journal of Regional Research* — cuartil no verificado.
