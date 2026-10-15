<!-- Generado por `make publicacion` desde output/v8/por_que_ha_subido.md. No editar a mano: se regenera y un test lo comprueba. -->

# ¿Por qué ha subido el precio de la vivienda? Factores, periodos y factor común (V8)

Borja Romero, economista (firma individual, independiente). Documento generado por `make v8` desde `docs/v8/plantillas/por_que_ha_subido.md`. Cada cifra sale de `output/v5/cifras_clave.csv` (identificador `V8-…`) y se puede rastrear hasta su script en `src/v8/`.

## Resumen

Este documento responde a tres preguntas sobre la vivienda en España entre 1995 y 2026: cuánto pesa cada factor en la variación del precio real de compra y del alquiler real en cada periodo, qué ecuaciones son significativas y robustas, y qué parte de la subida es común a todas las comunidades autónomas y a la zona euro. Las reglas de decisión se fijaron antes de estimar (pre-registro V8, `docs/v8/hipotesis.md`) y las desviaciones están anotadas en `docs/v8/desviaciones.md`.

La respuesta principal es negativa y precisa. Con la regla pre-registrada, **ningún factor puede designarse como «el más relevante» en ninguno de los diez casos** (dos mercados por cinco periodos): el número máximo de métodos que coinciden es 2 de cuatro cuando se exigen tres (ese máximo se alcanza en la compra de P3, P4 y P5 y en el alquiler de P2 y P5). Los métodos discrepan entre sí, las bandas de incertidumbre de la descomposición estructural incluyen el cero en casi todos los casos y ninguno de los tres instrumentos externos tiene fuerza suficiente para una lectura causal.

Lo que sí se sostiene es más modesto:

- El precio real de compra subió 75,4 pp en la expansión de 1995-2007, varió -44,0 pp en la crisis de 2008-2013 y ha subido 18,4 pp desde mediados de 2022. El alquiler real (IPC de alquiler deflactado por el IPC general) ha variado mucho menos: -1,8 pp en el mismo periodo reciente. Esa cifra mide el parque de contratos vivos (IPC de alquiler), no los contratos nuevos; para estos hay cifras C1 con dos fuentes por comunidad en 2021-2024 (variación nominal de la renta de los contratos nuevos, medida y periodo distintos, no comparables cifra a cifra con el alquiler real de P5): Cataluña 16,9 % (16,6-17,2 %) (2021-2024; INE IPVA (AEAT); Incasòl; dato de 2024; C1); Comunitat Valenciana 28,5 % (26,1-30,8 %) (2021-2024; INE IPVA (AEAT); GVA fianzas; dato de 2024; C1).
- En 1995-2007, el shock de actividad y renta es el único componente con una banda que excluye el cero en la descomposición histórica del SVAR: 31,8 pp (9,0-54,6 pp) de la subida del precio de compra [C3s, condicionado a las restricciones de signo y de cero]. No se designa porque los otros tres métodos se abstienen.
- La subida reciente es **muy común a todas las comunidades autónomas**: el componente común explica 92,8 % (86,7-94,9 %) de la varianza del crecimiento interanual del precio de compra en 2022-2026, frente a 45,3 % (42,0-54,2 %) en 2008-2013 [C4].
- El factor común español **acompaña** al precio de la vivienda de la zona euro: correlación 0,60 (0,14-0,86), p ajustado por Holm 0,020 [C4, asociación].
- Ningún modelo predice mejor fuera de muestra que un AR(4) sencillo.
- En la compra de 2022-2026, 9,5 pp de los 18,4 pp observados quedan sin atribuir a los shocks identificados (banda del 68 %: -14,6 a 24,1 pp; la banda incluye el cero y la parte no atribuida no es un factor más) [C3s, condicionado a las restricciones de signo y de cero].
- El multiverso se lee de dos maneras que no deben confundirse. Por familias de factores, 2 de 74 combinaciones cumplen la regla (signo estable en al menos el 80 % y significativo tras BH en al menos el 50 %). Por variables, 18 de 200 combinaciones de mercado, periodo y variable la cumplen (apartado «Lectura por variables del multiverso»); son asociaciones, sin identificación [C4].

## Abstract (English)

This document asks why Spanish house prices and rents have risen, by period (1995-2026), factor and market, and how much of the rise is common across regions and with the euro area. Decision rules were pre-registered. Under those rules, **no single factor can be designated as the most relevant in any of the ten market-period cells**: the four attribution methods (a Bayesian SVAR with sign restrictions, dominance analysis, LP-IV with external instruments and household-dwelling accounting) disagree, structural bands mostly include zero and all three external instruments are weak. The activity-and-income shock is the only component whose 68 % band excludes zero, for the purchase price in 1995-2007 (conditional on the sign restrictions). The recent rise (2022-2026) is highly common across the seventeen regions, and the Spanish common factor co-moves with euro-area house prices (an association, not a causal effect). No model beats a simple AR(4) out of sample.

## 1. Qué se ha medido y cómo leerlo

**Medidas.** Precio real de compra: valor tasado del Ministerio (desde 1995), deflactado por el IPC. Alquiler real: IPC de alquiler del INE (desde 2002), deflactado por el IPC. Las variaciones se expresan en puntos logarítmicos ×100 acumulados en cada periodo («pp»); para variaciones pequeñas equivalen a puntos porcentuales. El IPC de alquiler sigue el **parque** de contratos vivos, no los contratos nuevos, y por eso se mueve mucho más despacio que el precio de los anuncios o de los contratos firmados en el año.

**Periodos** (fijados antes de estimar):

| Código | Periodo | Precio real de compra | Alquiler real |
|---|---|---|---|
| P1 | 1995T1-2007T4, expansión y crédito | 75,4 pp | 4,9 pp |
| P2 | 2008T3-2013T4, crisis y ajuste | -44,0 pp | -2,7 pp |
| P3 | 2014T1-2019T4, recuperación | 8,2 pp | -1,1 pp |
| P4 | 2020T2-2022T2, pandemia y reapertura | -5,5 pp | -9,3 pp |
| P5 | 2022T3-2026T1, subida de tipos y presión demográfica | 18,4 pp | -1,8 pp |

El alquiler de P1 empieza en 2002. P4 tiene nueve trimestres y todas sus estimaciones se declaran imprecisas.

**Capas de evidencia.** Cada resultado lleva su capa:

- **C3s**: efecto identificado por restricciones de signo y de cero explícitas en un SVAR. Vale solo bajo esos supuestos y se escribe siempre «condicionado a las restricciones».
- **C3**: efecto identificado por un instrumento externo que supera sus pruebas. En V8 **ningún** resultado llega a C3.
- **C4**: asociación o descripción. Sin lectura causal.

**Siete familias de factores**: demografía, empleo y renta, crédito y tipos, oferta, demanda externa (compradores extranjeros), turismo y factor europeo. El SVAR identifica además un shock de demanda específica de vivienda, que no es una de las siete familias.

## 2. La pregunta principal: ¿qué factor ha pesado más?

### 2.1 La regla

El pre-registro exige tres condiciones a la vez para designar un factor como el más relevante en un mercado y periodo:

1. que sea el de mayor contribución en al menos tres de cuatro métodos: la descomposición histórica del SVAR, el análisis de dominancia, las proyecciones locales con instrumentos externos (LP-IV) y la contabilidad hogares-viviendas;
2. que su signo sea estable en al menos el 80 % del multiverso de especificaciones;
3. que su banda del 68 % en la descomposición histórica no incluya el cero.

Antes de calcular nada se fijó cómo vota cada método, cuándo se abstiene (una abstención cuenta como «no apoya») y que la parte no atribuida a ningún factor nunca compite (`docs/v8/desviaciones.md`, regla operativa de F5). En el alquiler, LP-IV se abstiene siempre (instrumento débil e intervalo de Anderson-Rubin al 68 % no acotado), de modo que allí solo la demografía podía reunir tres votos. En la compra, el intervalo de Anderson-Rubin al 68 % está acotado y LP-IV puede votar, pero solo por crédito y tipos; lo hace en P4, con una primera etapa débil (F efectivo 1,83) y de signo contrario al esperado.

### 2.2 El resultado

| Mercado | Periodo | Máximo de métodos que coinciden | ¿Designado? (uno = sí; cero = no) |
|---|---|---|---|
| Compra | P1 | 1 | 0 |
| Compra | P2 | 1 | 0 |
| Compra | P3 | 2 | 0 |
| Compra | P4 | 2 | 0 |
| Compra | P5 | 2 | 0 |
| Alquiler | P1 | 1 | 0 |
| Alquiler | P2 | 2 | 0 |
| Alquiler | P3 | 1 | 0 |
| Alquiler | P4 | 1 | 0 |
| Alquiler | P5 | 2 | 0 |

**Por qué no se puede designar.** No es falta de cálculo; son tres razones concretas:

- **Los métodos no coinciden.** En la compra de P5, crédito y tipos es el factor con más probabilidad de ser el mayor en el SVAR (29,7 %), aunque su media posterior es negativa y la mayor media es la de actividad y renta; la dominancia también vota crédito y tipos, y la contabilidad hogares-viviendas vota demografía. En el alquiler de P3, el SVAR señala demografía y la dominancia, demanda externa.
- **La incertidumbre es grande.** En el SVAR, la probabilidad de que el primer factor sea de verdad el mayor va, en la compra, de 25,9 % a 71,7 % según el periodo, y en el alquiler de 24,5 % a 38,8 %. Solo en la compra de P1 supera la mitad.
- **No hay identificación externa.** Los tres instrumentos (shocks monetarios de alta frecuencia del BCE, empuje migratorio desde el resto de la UE y composición sectorial del empleo) tienen una primera etapa débil: F efectivo de 1,83 para el primero y de 0,05 para el segundo, muy por debajo del umbral de diez. Ningún instrumento llega a C3 (0 de tres).

Lo que se publica en su lugar es un **ranking con incertidumbre** (`output/v8/F5/ranking.csv`) y una ficha por caso (`output/v8/F5/fichas.md`).

## 3. Periodo a periodo

Las contribuciones del SVAR son medias posteriores acumuladas en el periodo, con la banda del 68 % entre paréntesis, condicionadas a las restricciones de signo y de cero [C3s]. La media es la única medida que suma la variación observada; la mediana se publica al lado en las tablas porque la posterior tiene colas largas.

### P1 (1995-2007): expansión

El precio real de compra subió 75,4 pp. Para este periodo se usa la versión larga del SVAR (cuatro variables desde 1995: precio, tipo hipotecario, PIB en volumen y población), porque el crédito nuevo y las compraventas no existen antes de 2004.

- Actividad y renta: 31,8 pp (9,0-54,6 pp). Es la única contribución del SVAR cuya banda del 68 % excluye el cero. En el multiverso, el crecimiento del PIB tiene un signo estable pero **negativo**, casi nunca significativo tras BH, y deja de ser estable si se cuentan las especificaciones fallidas: la asociación por regresión no acompaña al signo del SVAR [C4].
- Demografía: 8,9 pp (-5,0 a 24,8 pp).
- Crédito y tipos: 3,0 pp (-7,2 a 14,0 pp).
- Parte no atribuida a los shocks identificados: 31,6 pp (-6,0 a 74,1 pp) (banda aproximada).

Lectura: bajo las restricciones del SVAR, la expansión del precio de compra en 1995-2007 se asocia sobre todo a shocks de actividad y renta [C3s, condicionado a las restricciones]. No se designa porque la dominancia, LP-IV y la contabilidad no lo votan y porque el multiverso no acompaña al signo. El alquiler de P1 no tiene SVAR (la serie empieza en 2002).

### P2 (2008-2013): crisis

El precio real de compra varió -44,0 pp.

- Actividad y renta: -10,6 pp (-23,5 a 0,66 pp).
- Crédito y tipos: -8,6 pp (-18,9 a 0,54 pp).
- Demanda de vivienda: -7,4 pp (-17,9 a 2,0 pp).
- Oferta: -4,8 pp (-13,3 a 2,5 pp).

Las bandas de actividad y de crédito quedan muy cerca de excluir el cero, pero lo incluyen. La hipótesis pre-registrada de que crédito y actividad juntos empujaron a la baja (H8-4) inclina en ese sentido (intervalo al 95 %: -19,2 pp (-57,3 a 9,9 pp)) pero no se sostiene tras corregir por comparaciones múltiples (p de Holm 0,343).

La parte del crecimiento del precio que acompaña al de la zona euro es de -15,3 pp (-21,7 a -7,6 pp) en P2 [C4]. Con la del tramo final de P1 (desde 2006, cuando empieza la serie de la zona euro: 7,4 pp (4,7-8,7 pp)), es uno de los dos casos en que esa parte tiene una banda que excluye el cero; en P3, P4 y P5 la incluye. La caída española coincidió con la de otros mercados europeos, sin que eso identifique un efecto.

### P3 (2014-2019): recuperación

El precio real de compra subió 8,2 pp. Actividad y renta es el primer factor en el SVAR (7,7 pp (-3,5 a 18,2 pp)) y en la dominancia, y su signo es estable en el multiverso, pero la banda del SVAR incluye el cero. La hipótesis H8-3 (actividad y renta positiva en P3) no se sostiene tras Holm (p 0,838). La contabilidad hogares-viviendas vota por demografía porque se formaron más hogares que viviendas terminadas.

En el alquiler real (-1,1 pp), el SVAR señala demografía y la dominancia, demanda externa: no coinciden.

### P4 (2020-2022): pandemia

Nueve trimestres no bastan para separar factores. Todas las contribuciones son pequeñas, con bandas que incluyen el cero, y el pre-registro prohíbe designar factor en este periodo.

### P5 (2022-2026): subida de tipos y presión demográfica

El precio real de compra ha subido 18,4 pp y el alquiler real ha variado -1,8 pp.

- **Crédito y tipos.** En el SVAR, la media es -0,47 pp (-2,8 a 12,8 pp) y la mediana 3,4 pp: la posterior es muy asimétrica y el signo no está determinado. La hipótesis H8-2 (crédito y tipos restaron al precio en P5) no se sostiene (p de Holm 0,987). En el multiverso, la familia de crédito y tipos (orientada para que «más crédito o menos tipo» cuente igual) no llega al 80 %. La variable principal, el tipo real hipotecario, sí tiene un signo estable, pero en sentido contrario al canal expansivo: un tipo real más alto va con más crecimiento del precio. Es una asociación sin identificación [C4], y su signo positivo con el precio no se interpreta como un efecto del tipo: la inflación entra en las dos medidas (resta al tipo real y es el deflactor del precio real), lo que induce por construcción un comovimiento positivo, y tampoco se descarta el sentido inverso (el ciclo del precio acompañando al del tipo), porque ambos pueden responder a un mismo ciclo.
- **Actividad y renta.** Media 7,2 pp (-4,7 a 11,2 pp), mediana 1,1 pp.
- **Demografía.** En el precio de compra, 0,65 pp (-4,1 a 5,8 pp). En el alquiler, 0,07 pp (-1,9 a 2,1 pp). La hipótesis H8-1 (el shock demográfico empujó el alquiler en P5) no se sostiene (p de Holm 0,987). La contabilidad hogares-viviendas sí vota por demografía en la compra: en P5 se formaron más hogares que viviendas libres terminadas (la serie no incluye las protegidas).
- **Oferta.** 1,9 pp (-3,3 a 9,0 pp) en la compra.
- **Parte no atribuida.** 9,5 pp (-14,6 a 24,1 pp) en la compra (banda aproximada).

El empuje migratorio, instrumentado con la emigración de cada país de origen hacia el resto de la UE, es demasiado débil para estimar su efecto sobre el alquiler (H8-7, F efectivo 0,05).

**Turismo (solo contraste).** En una sensibilidad no principal, limitada a las 6 comunidades con datos de turismo, el aprendizaje automático (gradient boosting con SHAP agrupado por familias) asigna al turismo 15,2 pp (8,1-14,8 pp) del crecimiento del precio de compra de esas comunidades en P5. No es comparable con la variación nacional. Es un **contraste predictivo**, no una atribución: SHAP mide cuánto usa el modelo cada variable para predecir, y el turismo solo existe desde 2016, lo que lo confunde con el ciclo reciente. El mismo modelo no predice mejor que un AR(4), y el punto queda fuera de su propia banda bootstrap, otra señal de inestabilidad. La cifra no implica ninguna relación de causa [C4].

## 3 bis. Factor a factor

Esta sección reúne, para cada familia, lo que dicen todos los métodos a la vez. Recuerda la capa de cada cifra: solo la descomposición del SVAR es C3s; todo lo demás es C4.

**Demografía.** En el alquiler es la única familia que podía reunir tres votos, y no los reúne en ningún periodo. En el SVAR, sus contribuciones son pequeñas y con bandas que incluyen el cero: 0,65 pp (-4,1 a 5,8 pp) en el precio de compra de P5 y 0,07 pp (-1,9 a 2,1 pp) en el alquiler. Por otro lado, es la única familia que cumple la regla del multiverso en la lectura por familias: positiva en el alquiler durante la crisis y en la muestra completa [C4]. **Aviso de colinealidad.** La población total y la población extranjera se mueven casi a la par: la correlación entre sus crecimientos interanuales es 0,91 en la muestra completa, 0,98 en P2 (VIF del par 24,89) y 0,78 en P5. Que las dos cumplan la regla en la misma celda no son dos pruebas independientes, y este análisis no separa su contribución. En M6, que usa una variable por familia, el VIF máximo es 18,38 y el de la población total llega a 7,44. La contabilidad hogares-viviendas también apunta en esa dirección en la compra de P3 y P5, cuando la formación de hogares superó a las viviendas terminadas. La lectura prudente: la presión demográfica acompaña a los precios en varios métodos, pero ninguno la identifica como el factor dominante, y el instrumento migratorio es demasiado débil para estimar su efecto.

**Empleo y renta.** Es el primer factor del SVAR en la compra de P1, P2 y P3, y en P1 es la única contribución del SVAR con banda que excluye el cero, aunque en el multiverso el signo estable es el contrario (31,8 pp (9,0-54,6 pp)) [C3s, condicionado a las restricciones de signo y de cero]. En P5 la media posterior es alta (7,2 pp (-4,7 a 11,2 pp)) pero la mediana es pequeña (1,1 pp): la evidencia reciente depende de unas pocas extracciones de la posterior. El instrumento sectorial del empleo es débil.

**Crédito y tipos.** Lo vota la dominancia en P4 y P5 (el primer factor cuya contribución parcial tiene el signo de la variación) y, en la compra de P5, el SVAR por probabilidad (29,7 %), no por media: en P5 la media es -0,47 pp (-2,8 a 12,8 pp) y la mediana 3,4 pp. Los shocks monetarios del BCE no permiten estimar su efecto: la primera etapa es débil (F efectivo 1,83) y tiene el signo contrario al esperado. Las hipótesis H8-5 y H8-6 no se sostienen (p de Holm 1,000 y 1,000). En el multiverso, la familia orientada no tiene un signo estable; el tipo real hipotecario sí, pero contrario al canal expansivo. Un modelo de aprendizaje automático doble (DML) asocia un tipo más alto con más alquiler (0,45), una asociación sin identificación [C4].

**Oferta.** En el SVAR, su contribución es pequeña en todos los periodos (1,9 pp (-3,3 a 9,0 pp) en la compra de P5). Lo que la oferta sí muestra es su ausencia relativa: en P5 se formaron más hogares que viviendas libres terminadas (la serie no incluye las protegidas), y por eso la contabilidad vota por demografía. Oferta y demografía son las dos caras de la misma brecha.

**Demanda externa (compradores extranjeros).** No es primer factor en ningún método salvo en la dominancia del alquiler de P3. En el aprendizaje automático, su peso en la compra de P5 es pequeño: 0,51 pp (0,10-0,71 pp) [C4].

**Turismo.** Solo hay datos desde 2016 y para 6 comunidades. El contraste de aprendizaje automático le asigna un peso alto en la compra de P5, pero inestable y sin lectura causal (sección P5).

**Factor europeo.** El factor común español acompaña al de la zona euro (0,60 (0,14-0,86)) y la parte europea del crecimiento español tiene una banda que excluye el cero en la crisis (-15,3 pp (-21,7 a -7,6 pp)) y en el tramo final de P1 (7,4 pp (4,7-8,7 pp)). En P5 es -3,3 pp (-7,0 a 1,8 pp). La dominancia lo vota (primer factor con el signo de la variación) en la compra de P2 y en el alquiler de P1 [C4].

## 4. El componente común: España y la zona euro

**Entre comunidades autónomas.** La parte de la varianza del crecimiento interanual del precio de compra que comparten las diecisiete comunidades (primer componente principal) es:

| Periodo | Compra | Alquiler |
|---|---|---|
| P1 | 64,7 % (56,4-71,2 %) | sin datos |
| P2 | 45,3 % (42,0-54,2 %) | 96,2 % (92,6-97,7 %) |
| P3 | 59,6 % (47,8-66,8 %) | 79,6 % (71,5-86,0 %) |
| P4 | 45,5 % (42,7-53,1 %) | 99,5 % (99,3-99,7 %) |
| P5 | 92,8 % (86,7-94,9 %) | 97,5 % (86,1-98,7 %) |

[C4.] La subida reciente es la más sincronizada de las cinco etapas: sus fluctuaciones son, sobre todo, comunes a todo el país. La hipótesis H8-8 (más de la mitad de la varianza es común en **cada** periodo) no se sostiene (p de Holm 0,669), porque en la crisis y en la pandemia las comunidades se separaron más. El IPC de alquiler por comunidades es casi todo común, en parte porque mide el parque de contratos y se mueve despacio.

**Con la zona euro.** El factor común español y el crecimiento del precio de la vivienda de la zona euro se mueven juntos: correlación 0,60 (0,14-0,86) (H8-9, p de Holm 0,020). Se mantiene con una aproximación de la zona euro sin España (media simple de Alemania, Francia, Italia, Países Bajos y Portugal). Es una asociación [C4]: tipos comunes del BCE, ciclos financieros comunes y demanda transfronteriza son explicaciones compatibles, y este análisis no las separa.

## 5. Comunitat Valenciana y València ciudad

Precio real de compra en P5 (2022-2026) [C4, descriptivo y asociación]:

| Ámbito | Variación acumulada observada, valor tasado | Segunda fuente (Registradores) | Parte de la variación asociada al factor común nacional | Comovimiento con el factor común (R² del crecimiento interanual) |
|---|---|---|---|---|
| Alicante (03) | 25,1 pp | 20,3 pp | 11,2 pp (4,6-16,8 pp) | 95,8 % |
| Castellón (12) | 18,6 pp | 10,9 pp | 14,6 pp (6,6-21,4 pp) | 94,5 % |
| Valencia (46) | 29,4 pp | 17,4 pp | 12,2 pp (5,6-18,2 pp) | 98,0 % |
| València ciudad | 43,5 pp | sin dato | 13,0 pp (5,1-19,9 pp) | 77,2 % |

La parte asociada al factor común se estima sobre la media interanual del periodo (una aproximación de la variación acumulada), por eso no se resta directamente de la columna observada. En la provincia de Valencia las dos fuentes de precio discrepan: el valor tasado da 29,4 pp frente a 17,4 pp de Registradores, y no se elige una. En València ciudad solo existe el valor tasado (43,5 pp), sin segunda fuente con la que contrastarlo; la cifra de la ciudad no se corrobora.

- En las tres provincias, las fluctuaciones del crecimiento reciente van casi enteras con las del conjunto de España (R² muy alto) [C4].
- La parte del aumento asociada al factor común es menor que el aumento observado en Alicante y en Valencia, y en Castellón es del orden de lo observado.
- En València ciudad la subida de P5 es la mayor de los cuatro ámbitos y la parte asociada al factor común es una fracción menor de ella: hay un componente propio de la ciudad que este análisis no atribuye a ningún factor.

Crisis (P2), variación aproximada (media interanual por la duración del periodo en años): Alicante -46,6 pp, Castellón -54,4 pp, Valencia -48,4 pp y València ciudad -68,6 pp.

No hay SVAR regional, así que no se designa ningún factor por debajo del nivel nacional.

## 6. Ecuaciones significativas y robustas

El pre-registro pedía ecuaciones por periodo significativas y robustas, sin hallazgos por azar. El balance es escaso:

- **Efectos por periodo (M0).** 2 de 70 coeficientes cumplen la regla de periodo (signo coincidente en el análisis principal y en una confirmación, permutación de fechas y medida alternativa de precio), pero solo 30 son evaluables: los otros 40 quedan «no evaluable» (de ellos, 35 son del alquiler). En el alquiler la regla de periodo es «no evaluable» porque no hay medida alternativa trimestral nacional del alquiler; no es un incumplimiento. Ninguno de los coeficientes que la cumplen sobrevive a la corrección por comparaciones múltiples (BH). Se reportan como exploratorios.
- **Multiverso (M7).** De 37.980 especificaciones, 32.424 se pudieron estimar. Solo 2 de 74 combinaciones de mercado, periodo y factor tienen un signo estable en al menos el 80 % y significativo en al menos la mitad: las dos son la demografía en el alquiler (crisis y muestra completa), con signo positivo [C4]. Esa es la lectura por **familias**; la lectura por **variables** (siguiente apartado) es más amplia y no la sustituye.
- **Largo plazo (M4).** No se demuestra una relación de cointegración estable: el contraste de cotas ARDL, con su contraste t, la acepta en 2 de 9 especificaciones (ambas del precio de compra, ninguna del alquiler), y los contrastes de Engle-Granger y Gregory-Hansen no la aceptan en ninguna.
- **Ningún modelo ha sido elegido por su p.** Los modelos destacados se eligen por su error fuera de muestra y, como ninguno cumple a la vez la regla de periodo y la del multiverso, todos van marcados «no cumple la regla» (`output/v8/tablas_modelos_destacados.md`).

### Lectura por variables del multiverso [C4]

Misma regla (signo orientado estable en al menos el 80 % de las especificaciones y significativo tras BH en al menos el 50 %), aplicada a cada variable por separado en lugar de a la familia entera: cumplen 18 de 200 combinaciones de mercado, periodo y variable. Un mismo factor puede tener una variable que cumple y otra que no, de modo que la lectura por familias (dos combinaciones) y la lectura por variables no se contradicen: miden cosas distintas. Con las especificaciones fallidas contadas como «no cumple», 15 siguen cumpliéndola; las marcadas con † (alquiler en P4 y tipo real en la compra de P1) tienen el multiverso truncado y dejan de cumplir en ese recuento. Signo orientado: positivo = más presión al alza; para el tipo real, un tipo más bajo cuenta como presión al alza.

| Mercado | Periodo | Variable | Familia | Signo orientado y lectura | % con el mismo signo | % significativas tras BH |
|---|---|---|---|---|---|---|
| Alquiler | P2 | Hogares (EPA) | Demografía | positivo: más de la variable con más crecimiento | 100,0 | 75,0 |
| Alquiler | P2 | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | 100,0 | 77,1 |
| Alquiler | P2 | Población total | Demografía | positivo: más de la variable con más crecimiento | 100,0 | 82,3 |
| Alquiler | P4 † | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | 83,3 | 54,2 |
| Alquiler | P4 † | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | 80,0 | 52,5 |
| Alquiler | Muestra completa | Saldo de crédito real | Crédito y tipos | positivo: más de la variable con más crecimiento | 93,8 | 52,6 |
| Alquiler | Muestra completa | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | 100,0 | 72,9 |
| Alquiler | Muestra completa | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | 99,0 | 62,5 |
| Alquiler | Muestra completa | Población total | Demografía | positivo: más de la variable con más crecimiento | 100,0 | 69,3 |
| Compra | P1 † | Tipo hipotecario real | Crédito y tipos | positivo: tipo real más bajo con más crecimiento | 95,8 | 65,6 |
| Compra | P5 | Saldo de crédito real | Crédito y tipos | positivo: más de la variable con más crecimiento | 92,7 | 64,1 |
| Compra | P5 | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | 87,5 | 50,0 |
| Compra | P5 | Precio real de la vivienda de otros países (BIS) | Factor europeo | positivo: más de la variable con más crecimiento | 94,8 | 58,9 |
| Compra | Muestra completa | Crédito nuevo real | Crédito y tipos | positivo: más de la variable con más crecimiento | 87,0 | 54,9 |
| Compra | Muestra completa | Ocupados (EPA) | Empleo y renta | positivo: más de la variable con más crecimiento | 97,4 | 51,3 |
| Compra | Muestra completa | Precio real de la vivienda de otros países (BIS) | Factor europeo | positivo: más de la variable con más crecimiento | 99,0 | 64,3 |
| Compra | Muestra completa | Viviendas terminadas | Oferta | positivo: más de la variable con más crecimiento | 95,3 | 52,6 |
| Compra | Muestra completa | Visados de obra nueva | Oferta | positivo: más de la variable con más crecimiento | 97,9 | 74,7 |

Son asociaciones [C4] entre el crecimiento de cada variable y el del precio o el alquiler: no identifican un efecto ni ordenan las variables por relevancia. Varias variables de una misma familia se mueven juntas (véase el aviso de colinealidad de la población), de modo que sus filas no son pruebas independientes. El signo positivo del tipo real hipotecario con el precio de compra en P5 y con el alquiler (en P4 y en la muestra completa) tiene el aviso de inflación y de sentido inverso del apartado de P5 (crédito y tipos).

## 7. Predicción

Raíz del error cuadrático medio fuera de muestra (crecimiento trimestral real, 2016T2-2026T1, misma muestra para todos) [C4]:

| Modelo | Compra | Alquiler |
|---|---|---|
| AR(4) | 1,2 pp | 0,80 pp |
| AR + factor común | 1,3 pp | 0,83 pp |
| BVAR del SVAR (forma reducida) | 1,4 pp | 0,98 pp |
| ECM v1 | 2,6 pp | 1,7 pp |

El modelo más sencillo es el que menos se equivoca. Que un modelo con factores no prediga mejor no dice que los factores no importen: dice que, con un trimestre de antelación, la propia inercia del precio contiene más información útil que los modelos con factores probados aquí. Las predicciones de 2026T3-2027T2 están congeladas con su huella sha256 y se evaluarán una sola vez con `make evaluate_v8` cuando se publiquen esos datos.

## 8. Qué no se puede afirmar con esta evidencia

- Que un único factor (inmigración, turismo, tipos, compradores extranjeros, falta de oferta…) «explique» la subida reciente. La regla pre-registrada no lo permite en ningún periodo.
- Que la subida de tipos de 2022-2023 frenara el precio de compra: la contribución estimada no tiene signo determinado.
- Que el turismo sea el motor de la subida reciente: la cifra alta sale de un modelo predictivo y no es una atribución.
- Que la correlación con la zona euro sea un efecto de Europa sobre España.
- Cualquier efecto causal con los instrumentos de V8: los tres son débiles.

## 9. Límites

- **Identificación.** La identificación principal pre-registrada del SVAR (signos en el impacto y el trimestre siguiente, con ceros) no aceptó ninguna rotación con los datos: se usó la variante pre-registrada que solo restringe el impacto. Las magnitudes del SVAR bayesiano pueden estar atenuadas.
- **Corrección tras la revisión.** La revisión independiente de los modelos detectó que la ficticia del cambio de la EPA en 2021 se había introducido como un escalón y no como un impulso. Se corrigió, se rehízo el SVAR y la congelación de predicciones, y se publican ambas versiones de las hipótesis (`output/v8/M2/hipotesis_m2_retirada.csv`).
- **Medidas.** El alquiler es el IPC de alquiler (parque de contratos), no el precio de los contratos nuevos. No hay medida trimestral alternativa nacional para el alquiler.
- **Periodos cortos.** P4 tiene nueve trimestres; P5, quince.
- **Regional.** Sin SVAR regional; las cifras por provincia y para València ciudad son descriptivas.

Todo el material es reproducible sin red con `make v8`. Pre-registro, desviaciones, revisiones y decisiones: `docs/v8/`.

## Actualización V9 (2026-10-15): qué causa qué <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->

V9 añade diseños de identificación con datos locales, pre-registrados y revisados antes de estimar (`publicacion/informe_v9.md`). **Ninguno alcanza C3 o C3s** (0 efectos en C3/C3s), así que la respuesta de V8 se mantiene: no se puede atribuir a ningún factor una parte cuantificada de la subida. Lo que añade, siempre como asociación o descripción [C4]: <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->

- **Topes de la Ley catalana 11/2020.** La renta de los contratos nuevos fue -5,9 % (-7,3 a -4,4 %) en los municipios con topes frente a los comparables. Supera las pruebas de tendencias previas y de placebo, pero no la robustez a desviaciones de tendencia exigida en el pre-registro. <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->
- **Zonas tensionadas en Cataluña.** La diferencia es -5,8 % (-8,5 a -3,2 %), pero los municipios ya divergían antes. No se detecta una caída del número de contratos.
- **Pisos turísticos e inmigración.** No hay diseño concluyente: tendencias previas en los pisos turísticos e instrumento débil en la inmigración (F efectiva 4,55).
- **Hogares (contable).** El componente población explica 92,0 % del aumento de hogares de 2022-2025 en España y 111,6 % en la Comunitat Valenciana. <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->

## Actualización V12 (2026-10-15): población, propiedad y oferta <!-- check:cifra-libre (años de los periodos) -->

V12 no estima modelos: describe de dónde viene la población, quién es propietario y dónde se construye (`publicacion/atlas_v12.md`). No cambia la respuesta de V8 y V9 (ningún factor identificado), pero precisa magnitudes [C4]:

- **Población.** En 2022-2024 el crecimiento (1.641.570 personas) procede del saldo con el extranjero (1.995.569 personas); el saldo vegetativo es negativo (-362.896 personas). <!-- check:cifra-libre (años de los periodos) -->
- **Hogares frente a oferta (2021-2024; provincias con Catastro estatal y MIVAU, sin País Vasco, Navarra, Ceuta ni Melilla).** Hogares nuevos: 934.562 hogares; obra nueva neta en el Catastro: 355.508 viviendas; terminadas según el MIVAU: 346.403 viviendas. Es una relación contable, no una medida de necesidad.
- **Grandes titulares.** 4,2 % de las viviendas son de titulares con más de diez; la afirmación de que «son los responsables de la subida» sigue sin poder contrastarse (verificador, V12-V02). <!-- check:cifra-libre (identificador de la ficha) -->
