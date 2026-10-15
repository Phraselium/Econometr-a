# ¿Por qué ha subido el precio de la vivienda? Factores, periodos y factor común (V8)

Borja Romero, economista (firma individual, independiente). Documento generado por `make v8` desde `docs/v8/plantillas/por_que_ha_subido.md`. Cada cifra sale de `output/v5/cifras_clave.csv` (identificador `V8-…`) y se puede rastrear hasta su script en `src/v8/`.

## Resumen

Este documento responde a tres preguntas sobre la vivienda en España entre 1995 y 2026: cuánto pesa cada factor en la variación del precio real de compra y del alquiler real en cada periodo, qué ecuaciones son significativas y robustas, y qué parte de la subida es común a todas las comunidades autónomas y a la zona euro. Las reglas de decisión se fijaron antes de estimar (pre-registro V8, `docs/v8/hipotesis.md`) y las desviaciones están anotadas en `docs/v8/desviaciones.md`.

La respuesta principal es negativa y precisa. Con la regla pre-registrada, **ningún factor puede designarse como «el más relevante» en ninguno de los diez casos** (dos mercados por cinco periodos): el número máximo de métodos que coinciden es {{V8-VOTOS-c-P5:num}} de cuatro cuando se exigen tres (ese máximo se alcanza en la compra de P3, P4 y P5 y en el alquiler de P2 y P5). Los métodos discrepan entre sí, las bandas de incertidumbre de la descomposición estructural incluyen el cero en casi todos los casos y ninguno de los tres instrumentos externos tiene fuerza suficiente para una lectura causal.

Lo que sí se sostiene es más modesto:

- El precio real de compra subió {{V8-OBS-c-P1}} en la expansión de 1995-2007, varió {{V8-OBS-c-P2}} en la crisis de 2008-2013 y ha subido {{V8-OBS-c-P5}} desde mediados de 2022. El alquiler real (IPC de alquiler deflactado por el IPC general) ha variado mucho menos: {{V8-OBS-a-P5}} en el mismo periodo reciente. Esa cifra mide el parque de contratos vivos (IPC de alquiler), no los contratos nuevos; para estos hay cifras C1 con dos fuentes por comunidad en 2021-2024 (variación nominal de la renta de los contratos nuevos, medida y periodo distintos, no comparables cifra a cifra con el alquiler real de P5): Cataluña {{A23-A9:cita}}; Comunitat Valenciana {{A23-A10:cita}}.
- En 1995-2007, el shock de actividad y renta es el único componente con una banda que excluye el cero en la descomposición histórica del SVAR: {{V8-SVAR-c-P1-empleo_renta-media}} de la subida del precio de compra [C3s, condicionado a las restricciones de signo y de cero]. No se designa porque los otros tres métodos se abstienen.
- La subida reciente es **muy común a todas las comunidades autónomas**: el componente común explica {{V8-M1-cuota-c-P5}} de la varianza del crecimiento interanual del precio de compra en 2022-2026, frente a {{V8-M1-cuota-c-P2}} en 2008-2013 [C4].
- El factor común español **acompaña** al precio de la vivienda de la zona euro: correlación {{V8-H8-9-est}}, p ajustado por Holm {{V8-H8-9-pholm:num}} [C4, asociación].
- Ningún modelo predice mejor fuera de muestra que un AR(4) sencillo.
- En la compra de 2022-2026, {{V8-QNA-pp-c-P5:valor}} de los {{V8-OBS-c-P5:valor}} observados quedan sin atribuir a los shocks identificados (banda del 68 %: {{V8-QNA-pp-c-P5:rango}}; la banda incluye el cero y la parte no atribuida no es un factor más) [C3s, condicionado a las restricciones de signo y de cero].
- El multiverso se lee de dos maneras que no deben confundirse. Por familias de factores, {{V8-M7-cumplen:num}} de {{V8-M7-combinaciones:num}} combinaciones cumplen la regla (signo estable en al menos el 80 % y significativo tras BH en al menos el 50 %). Por variables, {{V8-M7-var-cumplen:num}} de {{V8-M7-var-total:num}} combinaciones de mercado, periodo y variable la cumplen (apartado «Lectura por variables del multiverso»); son asociaciones, sin identificación [C4].

## Abstract (English)

This document asks why Spanish house prices and rents have risen, by period (1995-2026), factor and market, and how much of the rise is common across regions and with the euro area. Decision rules were pre-registered. Under those rules, **no single factor can be designated as the most relevant in any of the ten market-period cells**: the four attribution methods (a Bayesian SVAR with sign restrictions, dominance analysis, LP-IV with external instruments and household-dwelling accounting) disagree, structural bands mostly include zero and all three external instruments are weak. The activity-and-income shock is the only component whose 68 % band excludes zero, for the purchase price in 1995-2007 (conditional on the sign restrictions). The recent rise (2022-2026) is highly common across the seventeen regions, and the Spanish common factor co-moves with euro-area house prices (an association, not a causal effect). No model beats a simple AR(4) out of sample.

## 1. Qué se ha medido y cómo leerlo

**Medidas.** Precio real de compra: valor tasado del Ministerio (desde 1995), deflactado por el IPC. Alquiler real: IPC de alquiler del INE (desde 2002), deflactado por el IPC. Las variaciones se expresan en puntos logarítmicos ×100 acumulados en cada periodo («pp»); para variaciones pequeñas equivalen a puntos porcentuales. El IPC de alquiler sigue el **parque** de contratos vivos, no los contratos nuevos, y por eso se mueve mucho más despacio que el precio de los anuncios o de los contratos firmados en el año.

**Periodos** (fijados antes de estimar):

| Código | Periodo | Precio real de compra | Alquiler real |
|---|---|---|---|
| P1 | 1995T1-2007T4, expansión y crédito | {{V8-OBS-c-P1}} | {{V8-OBS-a-P1}} |
| P2 | 2008T3-2013T4, crisis y ajuste | {{V8-OBS-c-P2}} | {{V8-OBS-a-P2}} |
| P3 | 2014T1-2019T4, recuperación | {{V8-OBS-c-P3}} | {{V8-OBS-a-P3}} |
| P4 | 2020T2-2022T2, pandemia y reapertura | {{V8-OBS-c-P4}} | {{V8-OBS-a-P4}} |
| P5 | 2022T3-2026T1, subida de tipos y presión demográfica | {{V8-OBS-c-P5}} | {{V8-OBS-a-P5}} |

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

Antes de calcular nada se fijó cómo vota cada método, cuándo se abstiene (una abstención cuenta como «no apoya») y que la parte no atribuida a ningún factor nunca compite (`docs/v8/desviaciones.md`, regla operativa de F5). En el alquiler, LP-IV se abstiene siempre (instrumento débil e intervalo de Anderson-Rubin al 68 % no acotado), de modo que allí solo la demografía podía reunir tres votos. En la compra, el intervalo de Anderson-Rubin al 68 % está acotado y LP-IV puede votar, pero solo por crédito y tipos; lo hace en P4, con una primera etapa débil (F efectivo {{V8-H8-5-F:num}}) y de signo contrario al esperado.

### 2.2 El resultado

| Mercado | Periodo | Máximo de métodos que coinciden | ¿Designado? (uno = sí; cero = no) |
|---|---|---|---|
| Compra | P1 | {{V8-VOTOS-c-P1:num}} | {{V8-REGLA-c-P1:num}} |
| Compra | P2 | {{V8-VOTOS-c-P2:num}} | {{V8-REGLA-c-P2:num}} |
| Compra | P3 | {{V8-VOTOS-c-P3:num}} | {{V8-REGLA-c-P3:num}} |
| Compra | P4 | {{V8-VOTOS-c-P4:num}} | {{V8-REGLA-c-P4:num}} |
| Compra | P5 | {{V8-VOTOS-c-P5:num}} | {{V8-REGLA-c-P5:num}} |
| Alquiler | P1 | {{V8-VOTOS-a-P1:num}} | {{V8-REGLA-a-P1:num}} |
| Alquiler | P2 | {{V8-VOTOS-a-P2:num}} | {{V8-REGLA-a-P2:num}} |
| Alquiler | P3 | {{V8-VOTOS-a-P3:num}} | {{V8-REGLA-a-P3:num}} |
| Alquiler | P4 | {{V8-VOTOS-a-P4:num}} | {{V8-REGLA-a-P4:num}} |
| Alquiler | P5 | {{V8-VOTOS-a-P5:num}} | {{V8-REGLA-a-P5:num}} |

**Por qué no se puede designar.** No es falta de cálculo; son tres razones concretas:

- **Los métodos no coinciden.** En la compra de P5, crédito y tipos es el factor con más probabilidad de ser el mayor en el SVAR ({{V8-PFSTAR-c-P5}}), aunque su media posterior es negativa y la mayor media es la de actividad y renta; la dominancia también vota crédito y tipos, y la contabilidad hogares-viviendas vota demografía. En el alquiler de P3, el SVAR señala demografía y la dominancia, demanda externa.
- **La incertidumbre es grande.** En el SVAR, la probabilidad de que el primer factor sea de verdad el mayor va, en la compra, de {{V8-PFSTAR-c-P4}} a {{V8-PFSTAR-c-P1}} según el periodo, y en el alquiler de {{V8-PFSTAR-a-P4}} a {{V8-PFSTAR-a-P2}}. Solo en la compra de P1 supera la mitad.
- **No hay identificación externa.** Los tres instrumentos (shocks monetarios de alta frecuencia del BCE, empuje migratorio desde el resto de la UE y composición sectorial del empleo) tienen una primera etapa débil: F efectivo de {{V8-H8-5-F:num}} para el primero y de {{V8-H8-7-F:num}} para el segundo, muy por debajo del umbral de diez. Ningún instrumento llega a C3 ({{V8-M5-c3:num}} de tres).

Lo que se publica en su lugar es un **ranking con incertidumbre** (`output/v8/F5/ranking.csv`) y una ficha por caso (`output/v8/F5/fichas.md`).

## 3. Periodo a periodo

Las contribuciones del SVAR son medias posteriores acumuladas en el periodo, con la banda del 68 % entre paréntesis, condicionadas a las restricciones de signo y de cero [C3s]. La media es la única medida que suma la variación observada; la mediana se publica al lado en las tablas porque la posterior tiene colas largas.

### P1 (1995-2007): expansión

El precio real de compra subió {{V8-OBS-c-P1}}. Para este periodo se usa la versión larga del SVAR (cuatro variables desde 1995: precio, tipo hipotecario, PIB en volumen y población), porque el crédito nuevo y las compraventas no existen antes de 2004.

- Actividad y renta: {{V8-SVAR-c-P1-empleo_renta-media}}. Es la única contribución del SVAR cuya banda del 68 % excluye el cero. En el multiverso, el crecimiento del PIB tiene un signo estable pero **negativo**, casi nunca significativo tras BH, y deja de ser estable si se cuentan las especificaciones fallidas: la asociación por regresión no acompaña al signo del SVAR [C4].
- Demografía: {{V8-SVAR-c-P1-demografia-media}}.
- Crédito y tipos: {{V8-SVAR-c-P1-credito_tipos-media}}.
- Parte no atribuida a los shocks identificados: {{V8-QNA-pp-c-P1}} (banda aproximada).

Lectura: bajo las restricciones del SVAR, la expansión del precio de compra en 1995-2007 se asocia sobre todo a shocks de actividad y renta [C3s, condicionado a las restricciones]. No se designa porque la dominancia, LP-IV y la contabilidad no lo votan y porque el multiverso no acompaña al signo. El alquiler de P1 no tiene SVAR (la serie empieza en 2002).

### P2 (2008-2013): crisis

El precio real de compra varió {{V8-OBS-c-P2}}.

- Actividad y renta: {{V8-SVAR-c-P2-empleo_renta-media}}.
- Crédito y tipos: {{V8-SVAR-c-P2-credito_tipos-media}}.
- Demanda de vivienda: {{V8-SVAR-c-P2-demanda_vivienda-media}}.
- Oferta: {{V8-SVAR-c-P2-oferta-media}}.

Las bandas de actividad y de crédito quedan muy cerca de excluir el cero, pero lo incluyen. La hipótesis pre-registrada de que crédito y actividad juntos empujaron a la baja (H8-4) inclina en ese sentido (intervalo al 95 %: {{V8-H8-4-est}}) pero no se sostiene tras corregir por comparaciones múltiples (p de Holm {{V8-H8-4-pholm:num}}).

La parte del crecimiento del precio que acompaña al de la zona euro es de {{V8-M1-eur-c-P2}} en P2 [C4]. Con la del tramo final de P1 (desde 2006, cuando empieza la serie de la zona euro: {{V8-M1-eur-c-P1}}), es uno de los dos casos en que esa parte tiene una banda que excluye el cero; en P3, P4 y P5 la incluye. La caída española coincidió con la de otros mercados europeos, sin que eso identifique un efecto.

### P3 (2014-2019): recuperación

El precio real de compra subió {{V8-OBS-c-P3}}. Actividad y renta es el primer factor en el SVAR ({{V8-SVAR-c-P3-empleo_renta-media}}) y en la dominancia, y su signo es estable en el multiverso, pero la banda del SVAR incluye el cero. La hipótesis H8-3 (actividad y renta positiva en P3) no se sostiene tras Holm (p {{V8-H8-3-pholm:num}}). La contabilidad hogares-viviendas vota por demografía porque se formaron más hogares que viviendas terminadas.

En el alquiler real ({{V8-OBS-a-P3}}), el SVAR señala demografía y la dominancia, demanda externa: no coinciden.

### P4 (2020-2022): pandemia

Nueve trimestres no bastan para separar factores. Todas las contribuciones son pequeñas, con bandas que incluyen el cero, y el pre-registro prohíbe designar factor en este periodo.

### P5 (2022-2026): subida de tipos y presión demográfica

El precio real de compra ha subido {{V8-OBS-c-P5}} y el alquiler real ha variado {{V8-OBS-a-P5}}.

- **Crédito y tipos.** En el SVAR, la media es {{V8-SVAR-c-P5-credito_tipos-media}} y la mediana {{V8-SVAR-c-P5-credito_tipos-mediana:valor}}: la posterior es muy asimétrica y el signo no está determinado. La hipótesis H8-2 (crédito y tipos restaron al precio en P5) no se sostiene (p de Holm {{V8-H8-2-pholm:num}}). En el multiverso, la familia de crédito y tipos (orientada para que «más crédito o menos tipo» cuente igual) no llega al 80 %. La variable principal, el tipo real hipotecario, sí tiene un signo estable, pero en sentido contrario al canal expansivo: un tipo real más alto va con más crecimiento del precio. Es una asociación sin identificación [C4], y su signo positivo con el precio no se interpreta como un efecto del tipo: la inflación entra en las dos medidas (resta al tipo real y es el deflactor del precio real), lo que induce por construcción un comovimiento positivo, y tampoco se descarta el sentido inverso (el ciclo del precio acompañando al del tipo), porque ambos pueden responder a un mismo ciclo.
- **Actividad y renta.** Media {{V8-SVAR-c-P5-empleo_renta-media}}, mediana {{V8-SVAR-c-P5-empleo_renta-mediana:valor}}.
- **Demografía.** En el precio de compra, {{V8-SVAR-c-P5-demografia-media}}. En el alquiler, {{V8-SVAR-a-P5-demografia-media}}. La hipótesis H8-1 (el shock demográfico empujó el alquiler en P5) no se sostiene (p de Holm {{V8-H8-1-pholm:num}}). La contabilidad hogares-viviendas sí vota por demografía en la compra: en P5 se formaron más hogares que viviendas libres terminadas (la serie no incluye las protegidas).
- **Oferta.** {{V8-SVAR-c-P5-oferta-media}} en la compra.
- **Parte no atribuida.** {{V8-QNA-pp-c-P5}} en la compra (banda aproximada).

El empuje migratorio, instrumentado con la emigración de cada país de origen hacia el resto de la UE, es demasiado débil para estimar su efecto sobre el alquiler (H8-7, F efectivo {{V8-H8-7-F:num}}).

**Turismo (solo contraste).** En una sensibilidad no principal, limitada a las {{V8-M9-turismo-ccaa:num}} comunidades con datos de turismo, el aprendizaje automático (gradient boosting con SHAP agrupado por familias) asigna al turismo {{V8-M9-shap-c-P5-turismo}} del crecimiento del precio de compra de esas comunidades en P5. No es comparable con la variación nacional. Es un **contraste predictivo**, no una atribución: SHAP mide cuánto usa el modelo cada variable para predecir, y el turismo solo existe desde 2016, lo que lo confunde con el ciclo reciente. El mismo modelo no predice mejor que un AR(4), y el punto queda fuera de su propia banda bootstrap, otra señal de inestabilidad. La cifra no implica ninguna relación de causa [C4].

## 3 bis. Factor a factor

Esta sección reúne, para cada familia, lo que dicen todos los métodos a la vez. Recuerda la capa de cada cifra: solo la descomposición del SVAR es C3s; todo lo demás es C4.

**Demografía.** En el alquiler es la única familia que podía reunir tres votos, y no los reúne en ningún periodo. En el SVAR, sus contribuciones son pequeñas y con bandas que incluyen el cero: {{V8-SVAR-c-P5-demografia-media}} en el precio de compra de P5 y {{V8-SVAR-a-P5-demografia-media}} en el alquiler. Por otro lado, es la única familia que cumple la regla del multiverso en la lectura por familias: positiva en el alquiler durante la crisis y en la muestra completa [C4]. **Aviso de colinealidad.** La población total y la población extranjera se mueven casi a la par: la correlación entre sus crecimientos interanuales es {{V8-M6-colpob-completo-corr}} en la muestra completa, {{V8-M6-colpob-P2-corr}} en P2 (VIF del par {{V8-M6-colpob-P2-vif:num}}) y {{V8-M6-colpob-P5-corr}} en P5. Que las dos cumplan la regla en la misma celda no son dos pruebas independientes, y este análisis no separa su contribución. En M6, que usa una variable por familia, el VIF máximo es {{V8-M6-vif-max:num}} y el de la población total llega a {{V8-M6-vif-pob_total-max:num}}. La contabilidad hogares-viviendas también apunta en esa dirección en la compra de P3 y P5, cuando la formación de hogares superó a las viviendas terminadas. La lectura prudente: la presión demográfica acompaña a los precios en varios métodos, pero ninguno la identifica como el factor dominante, y el instrumento migratorio es demasiado débil para estimar su efecto.

**Empleo y renta.** Es el primer factor del SVAR en la compra de P1, P2 y P3, y en P1 es la única contribución del SVAR con banda que excluye el cero, aunque en el multiverso el signo estable es el contrario ({{V8-SVAR-c-P1-empleo_renta-media}}) [C3s, condicionado a las restricciones de signo y de cero]. En P5 la media posterior es alta ({{V8-SVAR-c-P5-empleo_renta-media}}) pero la mediana es pequeña ({{V8-SVAR-c-P5-empleo_renta-mediana:valor}}): la evidencia reciente depende de unas pocas extracciones de la posterior. El instrumento sectorial del empleo es débil.

**Crédito y tipos.** Lo vota la dominancia en P4 y P5 (el primer factor cuya contribución parcial tiene el signo de la variación) y, en la compra de P5, el SVAR por probabilidad ({{V8-PFSTAR-c-P5}}), no por media: en P5 la media es {{V8-SVAR-c-P5-credito_tipos-media}} y la mediana {{V8-SVAR-c-P5-credito_tipos-mediana:valor}}. Los shocks monetarios del BCE no permiten estimar su efecto: la primera etapa es débil (F efectivo {{V8-H8-5-F:num}}) y tiene el signo contrario al esperado. Las hipótesis H8-5 y H8-6 no se sostienen (p de Holm {{V8-H8-5-pholm:num}} y {{V8-H8-6-pholm:num}}). En el multiverso, la familia orientada no tiene un signo estable; el tipo real hipotecario sí, pero contrario al canal expansivo. Un modelo de aprendizaje automático doble (DML) asocia un tipo más alto con más alquiler ({{V8-M9-dml-a-tipo:num}}), una asociación sin identificación [C4].

**Oferta.** En el SVAR, su contribución es pequeña en todos los periodos ({{V8-SVAR-c-P5-oferta-media}} en la compra de P5). Lo que la oferta sí muestra es su ausencia relativa: en P5 se formaron más hogares que viviendas libres terminadas (la serie no incluye las protegidas), y por eso la contabilidad vota por demografía. Oferta y demografía son las dos caras de la misma brecha.

**Demanda externa (compradores extranjeros).** No es primer factor en ningún método salvo en la dominancia del alquiler de P3. En el aprendizaje automático, su peso en la compra de P5 es pequeño: {{V8-M9-shap-c-P5-demanda_externa}} [C4].

**Turismo.** Solo hay datos desde 2016 y para {{V8-M9-turismo-ccaa:num}} comunidades. El contraste de aprendizaje automático le asigna un peso alto en la compra de P5, pero inestable y sin lectura causal (sección P5).

**Factor europeo.** El factor común español acompaña al de la zona euro ({{V8-H8-9-est}}) y la parte europea del crecimiento español tiene una banda que excluye el cero en la crisis ({{V8-M1-eur-c-P2}}) y en el tramo final de P1 ({{V8-M1-eur-c-P1}}). En P5 es {{V8-M1-eur-c-P5}}. La dominancia lo vota (primer factor con el signo de la variación) en la compra de P2 y en el alquiler de P1 [C4].

## 4. El componente común: España y la zona euro

**Entre comunidades autónomas.** La parte de la varianza del crecimiento interanual del precio de compra que comparten las diecisiete comunidades (primer componente principal) es:

| Periodo | Compra | Alquiler |
|---|---|---|
| P1 | {{V8-M1-cuota-c-P1}} | sin datos |
| P2 | {{V8-M1-cuota-c-P2}} | {{V8-M1-cuota-a-P2}} |
| P3 | {{V8-M1-cuota-c-P3}} | {{V8-M1-cuota-a-P3}} |
| P4 | {{V8-M1-cuota-c-P4}} | {{V8-M1-cuota-a-P4}} |
| P5 | {{V8-M1-cuota-c-P5}} | {{V8-M1-cuota-a-P5}} |

[C4.] La subida reciente es la más sincronizada de las cinco etapas: sus fluctuaciones son, sobre todo, comunes a todo el país. La hipótesis H8-8 (más de la mitad de la varianza es común en **cada** periodo) no se sostiene (p de Holm {{V8-H8-8-pholm:num}}), porque en la crisis y en la pandemia las comunidades se separaron más. El IPC de alquiler por comunidades es casi todo común, en parte porque mide el parque de contratos y se mueve despacio.

**Con la zona euro.** El factor común español y el crecimiento del precio de la vivienda de la zona euro se mueven juntos: correlación {{V8-H8-9-est}} (H8-9, p de Holm {{V8-H8-9-pholm:num}}). Se mantiene con una aproximación de la zona euro sin España (media simple de Alemania, Francia, Italia, Países Bajos y Portugal). Es una asociación [C4]: tipos comunes del BCE, ciclos financieros comunes y demanda transfronteriza son explicaciones compatibles, y este análisis no las separa.

## 5. Comunitat Valenciana y València ciudad

Precio real de compra en P5 (2022-2026) [C4, descriptivo y asociación]:

| Ámbito | Variación acumulada observada, valor tasado | Segunda fuente (Registradores) | Parte de la variación asociada al factor común nacional | Comovimiento con el factor común (R² del crecimiento interanual) |
|---|---|---|---|---|
| Alicante (03) | {{V8-M8-cv-p03-P5-acum-mivau}} | {{V8-M8-cv-p03-P5-acum-alt}} | {{V8-M8-cv-p03-P5-fcpp}} | {{V8-M8-cv-p03-P5-cuota}} |
| Castellón (12) | {{V8-M8-cv-p12-P5-acum-mivau}} | {{V8-M8-cv-p12-P5-acum-alt}} | {{V8-M8-cv-p12-P5-fcpp}} | {{V8-M8-cv-p12-P5-cuota}} |
| Valencia (46) | {{V8-M8-cv-p46-P5-acum-mivau}} | {{V8-M8-cv-p46-P5-acum-alt}} | {{V8-M8-cv-p46-P5-fcpp}} | {{V8-M8-cv-p46-P5-cuota}} |
| València ciudad | {{V8-M8-cv-vlc-P5-acum-mivau}} | sin dato | {{V8-M8-cv-vlc-P5-fcpp}} | {{V8-M8-cv-vlc-P5-cuota}} |

La parte asociada al factor común se estima sobre la media interanual del periodo (una aproximación de la variación acumulada), por eso no se resta directamente de la columna observada. En la provincia de Valencia las dos fuentes de precio discrepan: el valor tasado da {{V8-M8-cv-p46-P5-acum-mivau}} frente a {{V8-M8-cv-p46-P5-acum-alt}} de Registradores, y no se elige una. En València ciudad solo existe el valor tasado ({{V8-M8-cv-vlc-P5-acum-mivau}}), sin segunda fuente con la que contrastarlo; la cifra de la ciudad no se corrobora.

- En las tres provincias, las fluctuaciones del crecimiento reciente van casi enteras con las del conjunto de España (R² muy alto) [C4].
- La parte del aumento asociada al factor común es menor que el aumento observado en Alicante y en Valencia, y en Castellón es del orden de lo observado.
- En València ciudad la subida de P5 es la mayor de los cuatro ámbitos y la parte asociada al factor común es una fracción menor de ella: hay un componente propio de la ciudad que este análisis no atribuye a ningún factor.

Crisis (P2), variación aproximada (media interanual por la duración del periodo en años): Alicante {{V8-M8-cv-p03-P2-total}}, Castellón {{V8-M8-cv-p12-P2-total}}, Valencia {{V8-M8-cv-p46-P2-total}} y València ciudad {{V8-M8-cv-vlc-P2-total}}.

No hay SVAR regional, así que no se designa ningún factor por debajo del nivel nacional.

## 6. Ecuaciones significativas y robustas

El pre-registro pedía ecuaciones por periodo significativas y robustas, sin hallazgos por azar. El balance es escaso:

- **Efectos por periodo (M0).** {{V8-M0-cumplen:num}} de {{V8-M0-coef:num}} coeficientes cumplen la regla de periodo (signo coincidente en el análisis principal y en una confirmación, permutación de fechas y medida alternativa de precio), pero solo {{V8-M0-evaluables:num}} son evaluables: los otros {{V8-M0-no-evaluable:num}} quedan «no evaluable» (de ellos, {{V8-M0-no-evaluable-alquiler:num}} son del alquiler). En el alquiler la regla de periodo es «no evaluable» porque no hay medida alternativa trimestral nacional del alquiler; no es un incumplimiento. Ninguno de los coeficientes que la cumplen sobrevive a la corrección por comparaciones múltiples (BH). Se reportan como exploratorios.
- **Multiverso (M7).** De {{V8-M7-rejilla:num}} especificaciones, {{V8-M7-ajustadas:num}} se pudieron estimar. Solo {{V8-M7-cumplen:num}} de {{V8-M7-combinaciones:num}} combinaciones de mercado, periodo y factor tienen un signo estable en al menos el 80 % y significativo en al menos la mitad: las dos son la demografía en el alquiler (crisis y muestra completa), con signo positivo [C4]. Esa es la lectura por **familias**; la lectura por **variables** (siguiente apartado) es más amplia y no la sustituye.
- **Largo plazo (M4).** No se demuestra una relación de cointegración estable: el contraste de cotas ARDL, con su contraste t, la acepta en {{V8-M4-ardl-rechaza:num}} de {{V8-M4-ardl-total:num}} especificaciones (ambas del precio de compra, ninguna del alquiler), y los contrastes de Engle-Granger y Gregory-Hansen no la aceptan en ninguna.
- **Ningún modelo ha sido elegido por su p.** Los modelos destacados se eligen por su error fuera de muestra y, como ninguno cumple a la vez la regla de periodo y la del multiverso, todos van marcados «no cumple la regla» (`output/v8/tablas_modelos_destacados.md`).

### Lectura por variables del multiverso [C4]

Misma regla (signo orientado estable en al menos el 80 % de las especificaciones y significativo tras BH en al menos el 50 %), aplicada a cada variable por separado en lugar de a la familia entera: cumplen {{V8-M7-var-cumplen:num}} de {{V8-M7-var-total:num}} combinaciones de mercado, periodo y variable. Un mismo factor puede tener una variable que cumple y otra que no, de modo que la lectura por familias (dos combinaciones) y la lectura por variables no se contradicen: miden cosas distintas. Con las especificaciones fallidas contadas como «no cumple», {{V8-M7-var-cumplen-rejilla:num}} siguen cumpliéndola; las marcadas con † (alquiler en P4 y tipo real en la compra de P1) tienen el multiverso truncado y dejan de cumplir en ese recuento. Signo orientado: positivo = más presión al alza; para el tipo real, un tipo más bajo cuenta como presión al alza.

| Mercado | Periodo | Variable | Familia | Signo orientado y lectura | % con el mismo signo | % significativas tras BH |
|---|---|---|---|---|---|---|
| Alquiler | P2 | Hogares (EPA) | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-P2-hogares_epa-signo:num}} | {{V8-M7-var-a-P2-hogares_epa-bh:num}} |
| Alquiler | P2 | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-P2-pob_extranj_ine-signo:num}} | {{V8-M7-var-a-P2-pob_extranj_ine-bh:num}} |
| Alquiler | P2 | Población total | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-P2-pob_total-signo:num}} | {{V8-M7-var-a-P2-pob_total-bh:num}} |
| Alquiler | P4 † | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | {{V8-M7-var-a-P4-tipo_hip_real-signo:num}} | {{V8-M7-var-a-P4-tipo_hip_real-bh:num}} |
| Alquiler | P4 † | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-P4-pob_extranj_ine-signo:num}} | {{V8-M7-var-a-P4-pob_extranj_ine-bh:num}} |
| Alquiler | Muestra completa | Saldo de crédito real | Crédito y tipos | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-completo-credito_stock_real-signo:num}} | {{V8-M7-var-a-completo-credito_stock_real-bh:num}} |
| Alquiler | Muestra completa | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | {{V8-M7-var-a-completo-tipo_hip_real-signo:num}} | {{V8-M7-var-a-completo-tipo_hip_real-bh:num}} |
| Alquiler | Muestra completa | Población extranjera (INE) | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-completo-pob_extranj_ine-signo:num}} | {{V8-M7-var-a-completo-pob_extranj_ine-bh:num}} |
| Alquiler | Muestra completa | Población total | Demografía | positivo: más de la variable con más crecimiento | {{V8-M7-var-a-completo-pob_total-signo:num}} | {{V8-M7-var-a-completo-pob_total-bh:num}} |
| Compra | P1 † | Tipo hipotecario real | Crédito y tipos | positivo: tipo real más bajo con más crecimiento | {{V8-M7-var-c-P1-tipo_hip_real-signo:num}} | {{V8-M7-var-c-P1-tipo_hip_real-bh:num}} |
| Compra | P5 | Saldo de crédito real | Crédito y tipos | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-P5-credito_stock_real-signo:num}} | {{V8-M7-var-c-P5-credito_stock_real-bh:num}} |
| Compra | P5 | Tipo hipotecario real | Crédito y tipos | negativo: tipo real más alto con más crecimiento | {{V8-M7-var-c-P5-tipo_hip_real-signo:num}} | {{V8-M7-var-c-P5-tipo_hip_real-bh:num}} |
| Compra | P5 | Precio real de la vivienda de otros países (BIS) | Factor europeo | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-P5-bis_hpi_xm_real-signo:num}} | {{V8-M7-var-c-P5-bis_hpi_xm_real-bh:num}} |
| Compra | Muestra completa | Crédito nuevo real | Crédito y tipos | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-completo-credito_nuevo_real-signo:num}} | {{V8-M7-var-c-completo-credito_nuevo_real-bh:num}} |
| Compra | Muestra completa | Ocupados (EPA) | Empleo y renta | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-completo-ocupados-signo:num}} | {{V8-M7-var-c-completo-ocupados-bh:num}} |
| Compra | Muestra completa | Precio real de la vivienda de otros países (BIS) | Factor europeo | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-completo-bis_hpi_xm_real-signo:num}} | {{V8-M7-var-c-completo-bis_hpi_xm_real-bh:num}} |
| Compra | Muestra completa | Viviendas terminadas | Oferta | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-completo-terminadas-signo:num}} | {{V8-M7-var-c-completo-terminadas-bh:num}} |
| Compra | Muestra completa | Visados de obra nueva | Oferta | positivo: más de la variable con más crecimiento | {{V8-M7-var-c-completo-visados-signo:num}} | {{V8-M7-var-c-completo-visados-bh:num}} |

Son asociaciones [C4] entre el crecimiento de cada variable y el del precio o el alquiler: no identifican un efecto ni ordenan las variables por relevancia. Varias variables de una misma familia se mueven juntas (véase el aviso de colinealidad de la población), de modo que sus filas no son pruebas independientes. El signo positivo del tipo real hipotecario con el precio de compra en P5 y con el alquiler (en P4 y en la muestra completa) tiene el aviso de inflación y de sentido inverso del apartado de P5 (crédito y tipos).

## 7. Predicción

Raíz del error cuadrático medio fuera de muestra (crecimiento trimestral real, 2016T2-2026T1, misma muestra para todos) [C4]:

| Modelo | Compra | Alquiler |
|---|---|---|
| AR(4) | {{V8-OOS-c-ar4-rmse}} | {{V8-OOS-a-ar4-rmse}} |
| AR + factor común | {{V8-OOS-c-ar_fc-rmse}} | {{V8-OOS-a-ar_fc-rmse}} |
| BVAR del SVAR (forma reducida) | {{V8-OOS-c-bvar_m2-rmse}} | {{V8-OOS-a-bvar_m2-rmse}} |
| ECM v1 | {{V8-OOS-c-ecm_v1-rmse}} | {{V8-OOS-a-ecm_v1-rmse}} |

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

V9 añade diseños de identificación con datos locales, pre-registrados y revisados antes de estimar (`publicacion/informe_v9.md`). **Ninguno alcanza C3 o C3s** ({{V9-NC3}} en C3/C3s), así que la respuesta de V8 se mantiene: no se puede atribuir a ningún factor una parte cuantificada de la subida. Lo que añade, siempre como asociación o descripción [C4]: <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->

- **Topes de la Ley catalana 11/2020.** La renta de los contratos nuevos fue {{V9-D1b-renta-att}} en los municipios con topes frente a los comparables. Supera las pruebas de tendencias previas y de placebo, pero no la robustez a desviaciones de tendencia exigida en el pre-registro. <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->
- **Zonas tensionadas en Cataluña.** La diferencia es {{V9-D1a-renta-att}}, pero los municipios ya divergían antes. No se detecta una caída del número de contratos.
- **Pisos turísticos e inmigración.** No hay diseño concluyente: tendencias previas en los pisos turísticos e instrumento débil en la inmigración (F efectiva {{V9-D4-ipc-replica-F:num}}).
- **Hogares (contable).** El componente población explica {{V9-D7-ES-2225-cuota-pob}} del aumento de hogares de 2022-2025 en España y {{V9-D7-CV-2225-cuota-pob}} en la Comunitat Valenciana. <!-- check:cifra-libre (número de ley, nombres de capa y años del periodo) -->
