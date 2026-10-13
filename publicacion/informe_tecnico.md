<!-- Generado por `make publicacion` desde output/v5/informe_tecnico.md. No editar a mano: se regenera y un test lo comprueba. -->

# Vivienda en España: necesidad, territorio, precios e instrumentos con datos públicos

## Informe técnico (versión de referencia v7.2)

- **Autor:** Borja Romero, economista (independiente).
- **Fecha:** 10 de octubre de 2026.
- **Versión:** `5.0`.
- **DOI:** pendiente.
- **Reproducción:** `make all` sin red, semilla `SEED=20261010`; comprobaciones con `make check`.
- **Cifras:** todas proceden de `output/v5/cifras_clave.csv` (tabla legible en `output/v5/cifras_clave.md`); este texto se genera desde una plantilla y no contiene cifras tecleadas.

---

## Resumen ejecutivo

**Qué hace este informe.** Ordena lo que se puede afirmar sobre la vivienda en España con datos públicos y con qué seguridad. Cada afirmación lleva una capa de evidencia: [C1] hecho confirmado por al menos dos fuentes independientes; [C2] cota con supuestos explícitos; [C4] exploratorio o de fuente única. En esta versión no hay ninguna afirmación de tipo C3 (efecto identificado con todos los controles): ningún resultado nuevo de v5 los supera.

**Lo que se sostiene con dos fuentes [C1].**
- Entre 2021 y 2024 el número de hogares creció más que el de viviendas terminadas: la diferencia está en el rango 389.361-710.542 viviendas (sin las dos correcciones que conservan el salto de la EPA, 596.371-710.542 viviendas) [C2: cota; la cuantía depende de cómo se corrija el salto de la EPA en 2021]. Con las bajas del parque estimadas, llega como máximo a 765.994 viviendas [C4].
- Los hogares aumentaron en 997.586 hogares (981.823-1.013.350 hogares) entre 2021 y 2025 [C1].
- Se terminaron 72.264-94.426 viviendas/año en 2019-2024 (territorio común) [C1].
- El precio de compra subió 47,2 % (44,2-56,1 %) en 2015-2025 según el núcleo de tres fuentes (Ministerio, Notariado y Registradores) [C1]; el índice del INE marca 79,9 % [C4]. Los dos se dan siempre juntos.
- La renta del stock de contratos de alquiler subió 10,9-22,9 % en 2015-2024 [C1]; los contratos nuevos subieron más (sección de alquiler).
- Los hogares con vivienda principal en propiedad son 74,5 % de hogares (72,1-75,9 % de hogares) [C1].

**Lo que es una proyección o una contabilidad con supuestos [C4].**
- Necesidad de vivienda 2026-2035 (base): 210.424 viviendas/año (99.388-292.083 viviendas/año) de media, suma de 52 provincias [C4]. Si una parte de las viviendas liberadas no llega al mercado, la necesidad efectiva sube a 245.989 viviendas/año (123.936-338.663 viviendas/año) [C4]. Equivale a 1,4 veces, 2,7 veces y 3,8 veces la producción actual con la misma cobertura. El mayor componente es el crecimiento de hogares proyectado por el INE (1.720.537 hogares en diez años, [C2]). El supuesto que más pesa en el rango es la fracción de vacías movilizables. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
- Viviendas liberadas por envejecimiento en 2026-2035: 1.856.430 viviendas (936.056-3.168.590 viviendas); llegan al mercado 150.079 viviendas al año [C4].
- Bajas del parque: las identidades de stock no las miden; las demoliciones con licencia son 0,02-0,04 % del parque en 2024 [C4].
- [C2] De 2025 a 2030 el déficit nacional empeora en todos los escenarios de la rejilla, incluido uno de construcción optimista. La magnitud es [C4]: un aumento de 585.609 viviendas (87.246-946.852 viviendas), hasta 1.349.025 viviendas (788.180-1.773.555 viviendas) a fin de 2030. Por provincias, 15 provincias empeoran, 0 provincias mejoran y 37 provincias quedan indeterminadas. A 2035 la dirección es indeterminada [C4].
- El déficit está concentrado: 6 provincias suman la mitad del déficit positivo de 2021-2025 [C4].

**Lo que no se puede afirmar.**
- Ninguna descomposición de la subida de precios es estable: el orden de las familias de factores cambia con el método y el periodo (tau de Kendall mínima -0,71 tau (4 familias)) [C4]. Se habla de «contribuciones contables», no de atribuciones.
- Las diferencias de precios entre provincias se describen, no se atribuyen: el pre-registro de B3 tenía potencia insuficiente y el resultado es «descriptivo honesto» [C4].
- No se dispone de datos públicos sobre la distribución del parque por tipo de propietario (personas jurídicas, grandes tenedores); las afirmaciones del debate sobre ese punto quedan sin analizar por falta de datos.

**Instrumentos.** Con la misma rúbrica se evalúan 36 instrumentos; en 18 instrumentos el signo no es evaluable con la evidencia disponible [C4]. La parte de una ayuda general a la demanda que se trasladaría al precio depende de la clase territorial: clase `1`, 27,8-81,8 %; clase `2`, 88,1-100,0 %; clase `3`, 50,1-89,8 % [C4]. Lo que aparece con signo estable en la rejilla de v3 es más construcción donde falta y la movilización de vacías [C2 en el signo; C4 en la magnitud].

**Convergencia.** Frente a BdE, Ministerio, INE, OCDE y Eurostat, y solo cuando concepto, periodo y cobertura son comparables, las cifras del proyecto coinciden en 2 y difieren en 1; otras 6 son comparables solo en parte (otro periodo o concepto), 4 comparten fuente primaria con el proyecto y no cuentan, y 9 no son comparables [C4]. Las diferencias se describen por periodo, concepto o bajas del parque.

**Cómo está organizado.** El diagnóstico nacional abre el informe (déficit, hogares, terminadas, precios, alquiler y Europa). Siguen la necesidad futura por provincia y la proyección a 2030, el territorio (concentración, clases y diferencias provinciales), la pregunta de qué se asocia con la subida, el parque frente al mercado, los instrumentos, la política por territorio, el módulo València, la convergencia con organismos y las limitaciones. Cada sección termina con una «Lectura» que resume lo que se puede y lo que no se puede decir.

**Qué cambia respecto a v4.** El coste de construcción deja de ser un supuesto y pasa a ser un rango oficial; se añade una contabilidad de necesidades a diez años y una proyección a 2030; se reconcilian el índice de precios del INE y el núcleo de tres fuentes; se separan los contratos de alquiler nuevos de los existentes; las diferencias provinciales se estudian con un pre-registro; la matriz de instrumentos se amplía y se cruza con el territorio; y todas las cifras se contrastan con las de los organismos públicos.

---

## Guía de capas

| Capa | Qué exige | Cómo se lee en el texto |
|---|---|---|
| C1 · Hecho | al menos dos fuentes independientes, con todos los componentes en C1, dentro de una tolerancia declarada | «es», «fue», «creció» |
| C2 · Cota | identificación parcial (Manski) con supuestos explícitos y escritos | «como máximo», «como mínimo», «entre … y …» |
| C3 · Efecto | diseño con pretendencias, placebos, sensibilidad y muestra sellada | no hay ninguno nuevo en v5 |
| C4 · Exploratorio | fuente única, proyección, supuestos no contrastados o asociación | «se asocia», «coincide», «es compatible con» |

Reglas que se aplican en todo el informe:
- La capa de una cifra es la menor de las de sus componentes. Por eso cifras habituales en el debate (el déficit 2021-2025, el peso de los compradores no residentes, las vacías) quedan en C4.
- Nunca se promueve una cifra de capa: una cifra C4 no pasa a C1 por repetirse o por coincidir con un organismo que usa la misma fuente.
- Sin lenguaje causal por debajo de C3. Las descomposiciones son «contribuciones contables».
- Si dos métodos discrepan, se dan los dos. Los resultados negativos se reportan.
- Se evalúan afirmaciones e instrumentos; nunca a quien los propone.

---

## 1. Diagnóstico

### 1.1 Déficit: 2021-2024 (C1) y 2021-2025 (C4)

**Definición.** El déficit contable es el aumento del número de hogares menos las viviendas terminadas en el mismo periodo. No incluye la demanda latente (jóvenes que no se emancipan) ni la vivienda que sale del parque, salvo que se diga.

**2021-2024 [C2 desde v6.2; antes C1].** Con dos fuentes independientes en cada componente (hogares: ECP y EPA corregida por la ruptura de 2021; terminadas: Ministerio, validado con Catastro dentro de ±15 %) [la corrección de la EPA de v1 es una constante de 242.400 hogares fijada en v1 (informe v1, §5.1)], el rango C1 publicado hasta v6.1 está retirado (ERRATA.md; output/v5/cifras_superadas.csv). En v6.2 (L3) se recalcula con siete correcciones alternativas del salto de la EPA más la constante de v1 (ocho variantes: sin corrección, trimestres vecinos con dos y cuatro trimestres, variación nula, dos enlaces con la ECP, solo ECP y la constante): sin bajas, el rango es 389.361 viviendas-710.542 viviendas. Las fuentes coinciden, pero la amplitud supera la tolerancia de C1 (±15 %), de modo que la cifra pasa a cota C2 (549.952 viviendas (389.361-710.542 viviendas) (2021-2024; hogares: EPA (varias correcciones) y ECP; terminadas: MIVAU y Catastro; dato de 2024T4; C2)). Detalle en `output/v6_2/L3/deficit_alternativas.md`. <!-- check:cifra-libre (parámetros de método ±15 %, bajas 0-0,2 % y constante EPA 242.400 de v1, declarados en la nota K4b; etiquetas de versión) -->

**Con bajas del parque estimadas [C4]: una sola cifra.** Al combinar todas las variantes del déficit sin bajas (siete alternativas más la constante de v1, con tres fuentes de terminadas) con las tasas de bajas estimadas en `T1` (mínimo, central y máximo), el déficit 2021-2024 queda en 654.646 viviendas (389.361-765.994 viviendas) [C4]. Es la única cifra de déficit con bajas que se publica desde v7.2. Las otras dos que circularon se retiran (ERRATA.md): el máximo de v5.1 con las bajas de `T1` sobre las cuatro combinaciones antiguas de fuentes (una sola corrección de la EPA), y el de las bajas supuestas del 0,1-0,2 % anual, que nada observado respalda. Con 2025 y sin bajas, 523.606-887.950 viviendas [C4]. <!-- check:cifra-libre (parámetros de método) -->

**Bajas del parque (`T1`) [C4].** Las identidades de stock no miden bajas: Censos 2011-2021 y Catastro dan tasas negativas (-0,33 % del parque al año y -0,18 % del parque al año), que reflejan altas no certificadas o afloramientos. Las demoliciones con licencia son 0,02-0,04 % del parque en 2024 y no cubren ruina, cambios de uso ni agregaciones. La tasa usada es C4 (mínimo, central y máximo de las demoliciones con licencia: 0,00 % del parque al año, 0,03 % del parque al año y 0,05 % del parque al año), salvo la cota física cero, que es C2. Sustituye al supuesto de bajas de v4, que queda por encima de todo lo observado.

**2021-2025 [C4].** Al añadir 2025, uno de los componentes pasa a depender de una sola fuente y el resultado baja a C4: 700.934 viviendas (700.934-700.934 viviendas) con bajas nulas [C4]. Por provincias, la mediana entre combinaciones de fuentes reparte ese total con un rango por provincia (`output/v5/A4/clasificacion_provincias.csv`).

**Lectura.** La cifra que conviene citar con seguridad es la de 2021-2024 [C1]. La de 2021-2025 es la habitual en el debate y coincide en orden de magnitud con las del Banco de España (sección de convergencia), pero es C4.

**Por qué no coinciden las cifras del debate.** Las cifras de déficit que circulan difieren por cuatro motivos, que se pueden separar: el periodo (con o sin 2021, con o sin 2025), la fuente de hogares (con o sin la corrección de la ruptura de la EPA de 2021), la fuente de terminadas (certificados de fin de obra o altas en el Catastro) y el tratamiento de las bajas del parque. La conciliación de v4 cerraba exactamente con una cadena de pasos; en v5 se mantiene y se añade la comparación con los organismos (sección de convergencia). Ninguna de las cifras es «la verdadera»: cada una responde a una definición.

### 1.2 Hogares

- Entre 2021 y 2025 los hogares aumentaron en 997.586 hogares (981.823-1.013.350 hogares) [C1] (INE ECP y EPA; la EPA sin corrección, porque las medias de 2021 y 2025 son posteriores a la ruptura).
- La demanda latente de jóvenes que viven con sus padres, frente a la tasa de convivencia de 2008, está entre 188.000-506.000 hogares [C2]. Es una cota: supone que la tasa de 2008 es la de referencia.
- El INE proyecta 1.720.537 hogares más en 2026-2035 [C2] y 1.024.156 hogares en 2026-2030 [C2]. Es un escenario del INE: no reacciona a la oferta ni a los precios.
- La descomposición contable de v4 (población por nacionalidad, edad y jefatura) se mantiene sin cambios en v5 y es C4 en los componentes de fuente única (`output/v4/M2`).

### 1.3 Viviendas terminadas

- En 2019-2024 se terminaron 72.264-94.426 viviendas/año en territorio común (sin País Vasco ni Navarra) [C1]: Ministerio (certificados de fin de obra) y Catastro (altas) coinciden dentro de la tolerancia declarada.
- El ritmo de 2023-2025 proyectado a cinco años da 473.250 viviendas (402.475-648.361 viviendas) en 2026-2030 [C4].
- El retardo medio entre iniciadas y terminadas es de 3,2 años (3,0-3,2 años) [C4].
- La cartera en construcción (iniciadas menos terminadas en dos o tres años) es de 89.815 viviendas (75.674-103.956 viviendas) [C4].
- Capacidad del sector: los ocupados en construcción por vivienda libre iniciada pasan de 10,3 personas por vivienda en 2008 a 35,2 personas por vivienda en 2013 y 12,6 personas por vivienda en 2025 [C4]. El coste de construcción (Eurostat) creció -18,8 puntos porcentuales menos que el precio entre 2014 y 2025 [C4]. Con estos datos no se contrasta si hay un cuello de botella de mano de obra.

![Capacidad del sector de la construcción](../output/v5/R1C/figuras/construccion_capacidad.png)

**Lectura.** El ritmo de terminadas de los últimos años es muy inferior al aumento de hogares, y el ratio de ocupados por vivienda iniciada ha vuelto a niveles parecidos a los de antes de la crisis financiera. Eso es compatible con una capacidad del sector que no es el único freno, pero con datos agregados no se puede separar la capacidad del sector de la rentabilidad, el suelo o la tramitación.

### 1.4 Precios: el puente IPV frente al núcleo

**Dos medidas que no coinciden.**
- Núcleo de tres fuentes (Ministerio, valor tasado; Notariado; Registradores): 47,2 % (44,2-56,1 %) en 2015-2025, medias anuales [C1].
- Índice de precios de vivienda del INE: 79,9 % [C4]. Eurostat publica el mismo índice, de modo que la coincidencia con Eurostat no es una segunda fuente.

**El puente.** Se reconcilian las dos medidas paso a paso, en logaritmos y con pesos comunes:
- reponderar el IPV con pesos de comunidades autónomas comunes cambia 0,60 pp [C4];
- la composición entre vivienda nueva y usada en la media de precio por metro cuadrado aporta 0,00 pp [C4];
- con pesos provinciales de 2015, Registradores sube 66,8 % y con pesos de comunidades 63,8 % [C4]: la reponderación geográfica amplía la diferencia en lugar de reducirla;
- queda un residuo no identificado de -30,9 pp [C4], compatible con diferencias de método (hedónico frente a medias o medianas), calidad, tamaño y cobertura, que no se pueden separar con los datos del repositorio.

**Factor común.** Las cuatro fuentes se mueven juntas: el primer componente principal recoge 89,2 % de la varianza de las variaciones anuales [C4]. El desacuerdo está en el nivel acumulado, no en la dirección.

**Niveles.** Registradores 2.284 EUR/m2 y Notariado 1.949 EUR/m2 en 2025 [C4], fuentes únicas por concepto.

![Puente de precio entre el IPV y el núcleo](../output/v5/A23/fig1_puente_precio.png)

**Lectura.** «La vivienda ha subido un ochenta por ciento» y «ha subido la mitad» describen dos medidas distintas. Este informe da las dos y cita el núcleo como C1.

### 1.5 Alquiler: stock frente a contratos nuevos

- **Stock de contratos (todos los vigentes).** El núcleo IPC de alquiler e IPVA de contratos existentes da 10,9-22,9 % en 2015-2024 [C1]. SERPAVI, con composición constante, da 43,0 % [C4].
- **Contratos nuevos.** El IPVA de nuevo contrato sube 37,0 % en 2015-2024 [C4]; en Cataluña (Incasòl) 54,5 % en 2015-2025 [C4]; en la Comunitat Valenciana (fianzas de la GVA) 58,0 % en 2020-2025 [C4].
- **Dos fuentes por territorio [C1].** Cataluña 2021-2024: 16,9 % (16,6-17,2 %) (IPVA nuevo e Incasòl) [C1]; Comunitat Valenciana 2021-2024: 28,5 % (26,1-30,8 %) (IPVA nuevo y fianzas) [C1].
- **Brecha.** En 2024 los contratos nuevos están 13,6 % por encima de los existentes (IPVA) [C4]. La cuota implícita de contratos nuevos en el índice es 16,0 % (13,9-17,6 %) [C4].
- **Rotación.** Fianzas sobre contratos vigentes: 25,0 % en Cataluña y 13,5 % en la Comunitat Valenciana [C4].
- **Actualización.** Si todo contrato vigente se hubiese actualizado con el HICP, el stock habría subido 7,2 % más en 2022-2024 [C4]: es una contabilidad con supuestos, no un contrafactual de una norma.

![Alquiler de stock y de contratos nuevos](../output/v5/A23/fig2_alquiler.png)

**Lectura.** El IPC de alquiler mide lo que pagan todos los inquilinos; el que busca vivienda paga el precio de contrato nuevo. Las dos cifras son correctas y miden cosas distintas.

**Por qué importa la distinción.** Una política que se evalúe con el IPC de alquiler verá cambios lentos, porque la mayoría de los contratos vigentes no se renuevan cada año; una que se evalúe con los contratos nuevos verá cambios más rápidos y más volátiles. Las dos cifras deben citarse con su definición. La rotación medida con las fianzas es baja en las dos comunidades con datos: la mayoría de los hogares inquilinos no pasa por el mercado cada año, pero quien entra lo hace a precios de contrato nuevo.

### 1.6 Comparación europea

Posición de España en la Unión Europea de los veintisiete (Eurostat; Eurostat toma el dato de España del INE, así que es coherencia, no independencia) [C4]:

| Indicador | España, nivel | Cambio desde 2015 | Capa |
|---|---|---|---|
| Precio real de la vivienda | — | 42,6 % acumulado desde 2015 | C4 |
| Alquiler real (IPCA) | — | -10,3 % acumulado desde 2015 | C4 |
| Tenencia en propiedad | 73,6 nivel % población | -4,6 cambio desde 2015 (% población) | C4 |
| Alquiler a precio de mercado | 17,4 nivel % población | 4,7 cambio desde 2015 (% población) | C4 |
| Edad media de emancipación | 30,2 nivel años | 1,2 cambio desde 2015 (años) | C4 |
| Hacinamiento | 9,5 nivel % población | 4,0 cambio desde 2015 (% población) | C4 |
| Sobrecarga de coste | 7,2 nivel % población | -3,1 cambio desde 2015 (% población) | C4 |
| Viviendas con permiso por mil habitantes | 4,1 nivel viv./1.000 hab. | 3,3 cambio desde 2015 (viv./1.000 hab.) | C4 |
| Crecimiento de la población | 9,4 nivel por 1.000 hab. | — | C4 |
| Migración neta | 11,8 nivel por 1.000 hab. | — | C4 |

![España en la distribución europea](../output/v5/CA/figuras/europa_percentiles.png)

**Lectura.** Lo específico de España en 2025 es la combinación de crecimiento de la población y migración neta altos con un precio real que sube y un alquiler real (medido por el IPCA, que es un índice de stock) que baja [C4]. El rango del precio real (16,9-60,9 % acumulado desde 2015) refleja el desacuerdo entre fuentes de precio de la sección anterior.

---

## 2. Necesidades 2026-2035 por provincia (B1) y déficit a 2030 (B2)

### 2.1 Método de B1

La necesidad de vivienda es una contabilidad stock-flujo por provincia, con rango mínimo-central-máximo en cada componente:

**N = A + R + V + F − M − K**

| Componente | Qué es | Diez años, central (rango) | Capa |
|---|---|---|---|
| A | Atraso: déficit 2021-2025 más emancipación retrasada | 1.103.170 viviendas (stock) (830.963-1.473.641 viviendas (stock)) | C4 |
| R | Reposición del parque | 89.665 viviendas (1.070-178.259 viviendas) | C4 |
| V | Vacancia friccional en zonas con presión | 58.674 viviendas (0-117.348 viviendas) | C4 |
| F | Crecimiento de hogares (INE) | 1.720.537 hogares (1.308.531-1.772.410 hogares) | C2 |
| M | Vacías movilizables en zonas con presión | 733.553 viviendas (366.777-1.100.330 viviendas) | C4 |
| K | Cartera en construcción | 89.815 viviendas (75.674-103.956 viviendas) | C4 |
| L | Viviendas liberadas por envejecimiento (aparte; ya neta en F) | 1.415.263 viviendas (10 años) (801.982-2.170.070 viviendas (10 años)) | C4 |

Decisiones de método:
- F, del INE, ya es neta de disoluciones de hogares. Restar además L duplicaría: se da la fórmula literal solo como variante (733.415 viviendas en diez años) [C4].
- R se estima con dos métodos (Censo 2011-2021 más Ministerio; Catastro más Ministerio). En 38 provincias las tasas brutas de baja no son positivas en ninguno de los dos: se acotan a cero y R queda como límite inferior poco informativo [C4].
- Hogares compartidos, hacinamiento y habitaciones compartidas no tienen dato provincial accesible: el rango se da sin ellos.
- La capa del total es la menor de las de sus componentes: C4.
- No es un modelo predictivo: AR(4) y ECM v1 no aplican, y no hay contrastes que ajustar.

**Qué no incluye.** La necesidad no es demanda solvente: no dice cuántas viviendas se venderían o alquilarían a los precios actuales, sino cuántas harían falta para alojar a los hogares proyectados, absorber el atraso y reponer el parque, una vez descontadas las vacías movilizables y la cartera en construcción. Tampoco distingue entre vivienda en propiedad, alquiler libre o protegido: esa elección corresponde a la política, no a la contabilidad.

**Por qué el rango es amplio.** El rango refleja tres incertidumbres que se suman: el atraso de partida (que depende de la ventana y de las fuentes), el crecimiento de hogares (el INE da un escenario y el proyecto añade una alternativa) y la parte de las vacías que se puede movilizar (entre un décimo y tres décimos de las vacías en zonas con presión, un supuesto de la rejilla de v3). Las vacías movilizables son el componente que más reduce la necesidad y el más incierto.

### 2.2 Resultado de B1

- Necesidad total (`v5.1`, base): 210.424 viviendas/año (99.388-292.083 viviendas/año) de media en 2026-2035, suma de 52 provincias [C4]; con la sensibilidad X, 245.989 viviendas/año (123.936-338.663 viviendas/año) [C4]. Las cifras provinciales de abajo son de B1 (`v5`).
- Las provincias con presión (clases `1` a `3` de A4) son 48 provincias; concentran 2.110.221 viviendas de la necesidad a diez años [C4].
- Las cuatro mayores necesidades anuales: Madrid 47.228 viviendas/año, Barcelona 30.963 viviendas/año, València 16.993 viviendas/año y Alicante 14.264 viviendas/año [C4].

![Necesidad anual de vivienda por provincia, 2026-2035](../output/v5/B1/figuras/B1_mapa_necesidad.png)

**Necesidad (`v5.1`) [C4].** Con la reposición basada en las bajas estimadas (`T1`) en lugar del supuesto de v4, la necesidad base (A + R + V + F − M − K) es de 210.424 viviendas/año (99.388-292.083 viviendas/año) de media en 2026-2035 [C4]. Si una parte de las viviendas liberadas no llega al mercado y queda vacía o como secundaria (componente X, que suma), la necesidad efectiva sube a 245.989 viviendas/año (123.936-338.663 viviendas/año) [C4]. X es un flujo bruto hacia la vacancia y sesga al alza; por eso la cifra de referencia es la base. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares. Frente a la producción con la misma cobertura (terminadas en España con País Vasco y Navarra, 78.810-100.980 viviendas/año en 2019-2024), la necesidad con X equivale a 1,4 veces, 2,7 veces y 3,8 veces la producción media (mínimo, central y máximo) [C4].

**Descomposición del rango [C4].** La amplitud de la necesidad anual (máximo menos mínimo) es de 214.727 viviendas/año. Se reparte así entre los supuestos: vacías movilizables 34,2 %, flujo futuro de hogares 21,6 %, atraso 20,7 %, liberadas que no llegan al mercado 10,3 %, reposición 6,5 %, vacancia friccional 5,5 % y cartera 1,3 %. El supuesto que más pesa es la fracción de vacías movilizables.

**Viviendas liberadas por envejecimiento (`T2`) [C4].** En 2026-2035 se liberarían 1.856.430 viviendas (936.056-3.168.590 viviendas) por fallecimiento del último miembro del hogar o por traslado a una residencia; llegan al mercado (venta o alquiler) 150.079 viviendas al año. Por tipo de municipio (central): 619.768 viviendas en las capitales de provincia, 137.395 viviendas en el entorno de las grandes ciudades y 1.099.268 viviendas en el resto de municipios. Hay desajuste territorial: 28,4 % de las liberadas está en municipios sin clase A4 (sin precio de referencia); entre los clasificados, 65,5 % cae en municipios de clase `1` o `2`. Los parámetros de traslado a residencias no tienen dato verificado. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.

**Lectura.** La necesidad está concentrada donde ya hay déficit: las provincias con más necesidad anual son las mismas que encabezan el déficit contable de 2021-2025. Fuera de las provincias con presión, la necesidad procede sobre todo de la reposición y del crecimiento de hogares, y es pequeña.

### 2.3 Método de B2

`D2030 = D2025 + F − T + B`, por provincia:
- `D2025`: déficit 2021-2025 con bajas nulas, 700.934 viviendas [C4];
- F: hogares INE 2026-2030, 1.024.156 hogares [C2];
- T: terminadas, con tres escenarios: (a) media de 2023-2025 (473.250 viviendas en cinco años); (b) cartera con el retardo nacional de 3,2 años; (c) tendencia, solo como sensibilidad;
- B: bajas, de R de B1, que es un límite inferior.

El rango de cada provincia combina el mínimo y el máximo de F, la envolvente de T entre los escenarios (a) y (b) y el rango de B. El signo (mejora o empeora) se asigna solo cuando todo el rango tiene el mismo signo.

### 2.4 Resultado de B2

**Proyección 2026-2030 (`T4`).** En una rejilla de escenarios que incluye los de B2, uno de construcción optimista (146.435 terminadas al año, por encima de cualquier año nacional desde 2008), bajas nulas, hogares bajos y las liberadas, el déficit nacional empeora de 2025 a 2030 en todos los escenarios: la dirección es [C2]. La magnitud es [C4]: el aumento está en el intervalo 87.246-946.852 viviendas y el déficit a fin de 2030 queda en 1.349.025 viviendas (788.180-1.773.555 viviendas). Por provincias, 15 provincias empeoran, 0 provincias mejoran y 37 provincias quedan indeterminadas (en `v5`: 20 provincias, 5 provincias y 27 provincias). A 2035 la dirección nacional es indeterminada [C4], con un déficit a fin de 2035 entre 482.095 viviendas y 2.400.412 viviendas: el envejecimiento libera 869.654 viviendas (5 años) en 2026-2030 y 986.777 viviendas (5 años) en 2031-2035, de modo que pesa más después de 2030. Mantener constante el déficit en 2026-2030 exigiría 211.772 terminadas al año [C4].

Los escenarios de B2 (`v5`), que la rejilla de `T4` incluye:

- En el escenario (b), 1.136.179 viviendas; en el (c), 1.276.238 viviendas [C4].
- En el escenario central (a) empeoran 45 provincias; en el (b), 40 provincias; en el (c), 41 provincias [C4].
- Con el rango completo: empeoran 20 provincias, mejoran 5 provincias y quedan indeterminadas 27 provincias [C4]. El signo central coincide en los tres escenarios en 46 provincias.

![Signo del cambio del déficit 2025-2030 por provincia](../output/v5/B2/figuras/B2_mapa_signo.png)

**Lectura.** Es una proyección bajo supuestos, no un pronóstico. Dice qué pasaría si las terminadas siguieran al ritmo reciente y los hogares crecieran como proyecta el INE. No incorpora la reacción de la oferta ni de la formación de hogares a los precios.

---

## 3. Territorio

### 3.1 Concentración

- En 2021-2025, 6 provincias suman la mitad del déficit positivo y 18 provincias suman cuatro quintas partes [C4].
- En 2021-2024 las cifras son 6 provincias y 17 provincias [C4].
- La concentración es estable entre ventanas: el déficit es un fenómeno de pocas provincias, con las grandes áreas urbanas y el litoral mediterráneo a la cabeza.

![Concentración del déficit 2021-2025](../output/v5/A4/figuras/A4_concentracion_2021_2025.png)

### 3.2 Clases de A4

**Cómo se clasifica.** Cada provincia se clasifica según dos preguntas: si falta vivienda (déficit 2021-2025 positivo) y si construir es rentable con un coste de construcción oficial. El coste procede del módulo básico de construcción de 1993 (BOE) actualizado con el índice de costes de Eurostat: 677,0 EUR/m2 construido (422,0-932,0 EUR/m2 construido) [C4]. En v4 el coste era supuesto; en v5 es un rango derivado de una norma.

| Clase | Definición | Provincias 2021-2025 (robustas) | Provincias 2012-2025 (robustas) |
|---|---|---|---|
| `1` | falta y es rentable | 37 (8) | 24 (13) |
| `2` | falta con freno regulatorio o de suelo: el precio supera coste y suelo con margen y la oferta no responde | 11 (3) | 6 (1) |
| `3` | falta y no es rentable con el coste oficial | 2 (0) | 0 (0) |
| `4` | no falta: déficit menor o igual que cero en la ventana | 0 (0) | 20 (8) |
| `9` | sin dato | 2 (1) | 2 (0) |

«Robustas»: la clase es la misma en todo el rango de costes, márgenes, tipos de descuento y holguras.

**Clase `4`.** Una provincia es de clase `4` cuando su déficit contable es nulo o negativo en la ventana: ha crecido más el parque que los hogares. En 2021-2025 no hay ninguna; en 2012-2025, que incluye los años de construcción de la década anterior, hay 20 provincias [C4]. Que una provincia sea de clase `4` no significa que no tenga problemas de acceso: significa que, en el agregado de la ventana, el parque creció más que los hogares.

**Nota de capa.** Todas las clases son C4. El déficit provincial de 2021-2025 es C4 (regla del componente más débil) y la rentabilidad depende de un coste derivado de una sola norma y un índice, que no es un coste de mercado observado. Por eso ningún resultado por clase (en D1 y D2) se promueve.

![Provincias por clase A4](../output/v5/A4/figuras/A4_provincias_por_clase.png)

![Rango oficial de coste de construcción](../output/v5/A4/figuras/A4_rango_coste_oficial.png)

**Lectura.** Las clases ordenan el territorio según dos preguntas sencillas y transparentes, con un coste oficial en lugar de uno supuesto. Su valor está en que hacen explícito el supuesto del que depende cada recomendación condicional: la clase `2` lleva a mirar el suelo y la tramitación; la clase `3`, el coste; la clase `1`, la capacidad de producir más. Pero son exploratorias: un cambio razonable del coste puede mover una provincia de clase, y eso es lo que mide la columna de robustez.

### 3.3 Diferencias provinciales (B3): descriptivo honesto

**Pre-registro.** Antes de estimar se registraron las hipótesis, las variables, las ocho familias de factores y la corrección por comparaciones múltiples (`docs/v5/prereg_B3.md`, etiqueta `prereg-v5`). El análisis de potencia previo dio un efecto mínimo detectable con Holm de 0,62 DT (0,34-1,1 DT) [C4], por encima del umbral que el pre-registro consideraba útil. Por eso B3 se declara de antemano **descriptivo honesto**: describe con qué se asocian las diferencias entre provincias, sin pretender identificar nada.

**Diseño.** Corte transversal de 50 provincias (sin Ceuta ni Melilla), variación del precio 2015-2025, ocho familias de factores a la vez, errores `HC3` y Conley, inferencia por aleatorización y Holm.

**Resultados [C4].**
- El modelo de ocho familias tiene un R² de 0,91 con el valor tasado.
- `H-B3-6` (precio inicial): -16,0 puntos logarítmicos (≈ %) por DT (-23,8 a -8,2 puntos logarítmicos (≈ %) por DT), p ajustado 0,00 probabilidad. Las provincias que partían de precios más bajos subieron más. Con el precio inicial de Registradores, para controlar el error de medida, el coeficiente baja a -9,0 puntos logarítmicos (≈ %) por DT y el p a 0,06 probabilidad: la asociación se mantiene en signo, pero parte de ella es mecánica (el error de medida del precio inicial empuja el coeficiente hacia valores negativos).
- `H-B3-1` (demanda sectorial tipo Bartik): 2,4 puntos logarítmicos (≈ %) por DT (-0,06 a 4,8 puntos logarítmicos (≈ %) por DT), p ajustado 0,33 probabilidad. No se distingue de cero.
- `H-B3-2` (crecimiento de la población): 3,5 puntos logarítmicos (≈ %) por DT (-0,74 a 7,8 puntos logarítmicos (≈ %) por DT), p ajustado 0,41 probabilidad. No se distingue de cero tras el ajuste.
- La validación cruzada dejando una provincia fuera da un RMSE de 0,07 log-puntos frente a 0,16 log-puntos del modelo de solo media [C4].

**Desviaciones del pre-registro.** Están todas en `output/v5/B3/desviaciones.md` y son exploratorias: renta medida con el PIB per cápita provincial en lugar de la renta por hogar; ventanas más cortas en alquiler y renta; validación por exclusión de una provincia en lugar de AR(4); acotación del parámetro de Oster.

![Variación del precio por provincia](../output/v5/B3/figuras/mapa_P1.png)

![Reparto de Shapley del R² por familias](../output/v5/B3/figuras/shapley.png)

**Lectura.** Las provincias con mayor subida 2015-2025 se asocian con precios de partida más bajos, un patrón de convergencia que en parte es mecánico. El resto de factores no se distingue de cero tras corregir por comparaciones múltiples. Con medio centenar de unidades y ocho familias de factores correlacionadas, no se puede pedir más a un corte transversal; el pre-registro sirvió precisamente para decirlo antes de ver los resultados.

---

## 4. Qué explica la subida y con qué seguridad (B4): contribuciones no estables

**Pregunta.** ¿Cuánto de la variación del precio de compra y del alquiler se asocia con cada familia de factores (demografía, renta y empleo, financiación, oferta y suelo, turismo y no residentes), y es estable ese orden?

**Método.** B4 no estima nada nuevo: triangula salidas existentes.
- v2 (series temporales nacionales): contribución contable = coeficiente por variación media de cada variable, en puntos de variación logarítmica acumulada.
- B3 (corte transversal): reparto de Shapley del R² entre provincias.
- v3: cotas de cantidad.
Las unidades no son sumables entre métodos. La estabilidad se mide con la tau de Kendall del orden de las cuatro familias comunes.

**Contribuciones contables al precio de compra (v2, valor tasado real) [C4].**

| Familia | 2015-2019 | 2019-2025 | 2015-2025 |
|---|---|---|---|
| Demografía | -5,0 pp de Δln acumulado | -2,0 pp de Δln acumulado | -7,0 pp de Δln acumulado |
| Renta y empleo | 0,48 pp de Δln acumulado | 0,61 pp de Δln acumulado | 1,1 pp de Δln acumulado |
| Financiación y tipos | 0,18 pp de Δln acumulado | 0,97 pp de Δln acumulado | 1,1 pp de Δln acumulado |
| Oferta y suelo | 0,11 pp de Δln acumulado | -0,02 pp de Δln acumulado | 0,09 pp de Δln acumulado |
| Residuo | 7,6 pp de Δln acumulado | -4,0 pp de Δln acumulado | 3,6 pp de Δln acumulado |

**Contribuciones contables al alquiler de stock (v2, IPC) [C4].**

| Familia | 2015-2019 | 2019-2025 | 2015-2025 |
|---|---|---|---|
| Demografía | -3,6 pp de Δln acumulado | 0,39 pp de Δln acumulado | -3,2 pp de Δln acumulado |
| Renta y empleo | 0,12 pp de Δln acumulado | 0,04 pp de Δln acumulado | 0,16 pp de Δln acumulado |
| Financiación y tipos | 0,01 pp de Δln acumulado | -0,07 pp de Δln acumulado | -0,06 pp de Δln acumulado |
| Oferta y suelo | 0,02 pp de Δln acumulado | 0,01 pp de Δln acumulado | 0,03 pp de Δln acumulado |
| Residuo | 5,0 pp de Δln acumulado | 5,3 pp de Δln acumulado | 10,4 pp de Δln acumulado |

**Reparto entre provincias (B3, cuota del R²) [C4].** Oferta y suelo 25,9 % del R2; demografía 23,6 % del R2; turismo y no residentes 18,4 % del R2; financiación y tipos 11,3 % del R2; renta y empleo 9,8 % del R2; residuo 18,8-29,9 % del R2. El orden de las familias no es el mismo con valor tasado y con Registradores (correlación de Spearman 0,91 coeficiente).

**Cota de cantidad [C2].** Las viviendas turísticas desplazaron como máximo 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) en 2020-2024 [C2].

**Estabilidad.** La tau de Kendall mínima del orden de las familias entre métodos y periodos es -0,71 tau (4 familias) [C4]: el orden se invierte según se mire. En las series nacionales el residuo es grande y cambia de signo entre periodos; entre provincias pesan más la oferta, la demografía y el turismo.

**Lectura.** No se puede afirmar qué familia de factores «explica» la subida. Lo que se sostiene es que las contribuciones contables no son estables: cambian con el método (series temporales frente a corte transversal), con el periodo y con la fuente de precio. Las tablas son contabilidad, no atribución.

---

## 5. Parque frente a mercado

El parque es el conjunto de viviendas existentes y sus ocupantes; el mercado son las transacciones y contratos de cada año. Una afirmación sobre uno no vale para el otro.

### 5.1 Quién posee las viviendas (R1C)

- Hogares con vivienda principal en propiedad: 74,5 % de hogares (72,1-75,9 % de hogares) [C1].
- Hogares con otras propiedades: 61,6 % de hogares del tramo en el tramo de sesenta y cinco a setenta y cuatro años frente a 15,3 % de hogares del tramo en el de menores de treinta y cinco [C4, EFF del BdE, fuente única].
- Personas jurídicas y sector público en el parque: **sin dato** público. Se ha pedido (solicitudes S1 y S3 de `docs/v5/solicitudes.md`).
- Vacías y de uso esporádico: el INE las publica para 3.185 entidades (3.185-3.185 entidades); la mediana municipal del porcentaje de vacías es 17,4 % de viviendas (6,8-35,2 % de viviendas) [C4].

![Propiedad por edad y personas jurídicas](../output/v5/R1C/figuras/propiedad_edad_y_pj.png)

**Lectura.** La propiedad de la vivienda principal está muy extendida y es una cifra C1. La concentración de otras propiedades en los tramos de edad mayores, frente a los menores, es compatible con una transferencia de riqueza inmobiliaria por edad, pero es fuente única. Sobre la propiedad empresarial del parque no hay dato: cualquier cifra que circule sobre ese punto no procede de una estadística pública que el proyecto haya podido localizar.

### 5.2 Empresas (CB)

- Compraventas con comprador persona jurídica: 11,3 % de compraventas en 2024 [C4]. Es un flujo; no dice qué parte del parque poseen las empresas.
- Declarantes del IRPF con rendimientos de capital inmobiliario: 3.262.026 declarantes; con reducción por arrendamiento de vivienda: 2.236.896 declarantes [C4].
- Viviendas equivalentes arrendadas por personas físicas: 2.650.952 viviendas, es decir, 0,81 viviendas/declarante por declarante [C4].
- Frente a las viviendas principales en alquiler del Censo (2.965.497 viviendas), el residual que incluye personas jurídicas, sector público y alquiler no declarado está entre 16,9-38,1 % del stock [C4].
- La AEAT no publica la distribución de arrendadores por número de inmuebles: no se puede contrastar cuánto alquiler está en manos de grandes tenedores.

### 5.3 No residentes (R1A)

- Peso de los compradores extranjeros no residentes: 6,8 % en 2025 frente a 9,9 % en 2015 [C4]. Con residentes, los compradores extranjeros son 16,9 % [C4].
- Entre provincias va de 0,07-32,5 % [C4].
- Asociación entre el peso inicial de no residentes y la subida del precio 2015-2025: bivariada 0,96 % de precio por punto de peso inicial (0,46-1,5 % de precio por punto de peso inicial); con renta, población, costa e islas, 0,02 % de precio por punto de peso inicial (-0,55 a 0,59 % de precio por punto de peso inicial) [C4]. Con controles el coeficiente no se distingue de cero, pero el intervalo no excluye una asociación de una parte apreciable de la bivariada. No se atribuye la subida a los no residentes ni se descarta.

**Lectura.** Los no residentes son una parte pequeña de las compraventas nacionales, pero muy desigual entre provincias: en algunas del litoral y los archipiélagos pesan mucho más que en el interior. La asociación con la subida de precios es frágil a los controles. No se puede afirmar que los no residentes sean un factor principal de la subida nacional ni que sean irrelevantes en las provincias donde su peso es alto.

### 5.4 Contado (CA)

- Hipotecas sobre vivienda por cada cien compraventas: 70,0 hipotecas por 100 compraventas en 2025 (INE) [C4]. Con Registradores, en 2022-2025, la razón coincide: 71,4-71,7 hipotecas por 100 compraventas en 2022, 65,3-65,8 hipotecas por 100 compraventas en 2023, 66,4-68,4 hipotecas por 100 compraventas en 2024 y 70,0-70,7 hipotecas por 100 compraventas en 2025 [C4].
- Si todas las hipotecas fuesen de compra, el contado sería como mínimo 30,0 % de compraventas de las compraventas [C4]. La cota solo es informativa si la fracción de hipotecas de compra supera 71,4 % de las hipotecas.
- Crédito a construcción y actividades inmobiliarias: de 471,8 miles de millones de euros en 2008 a 97,6 miles de millones de euros en 2025, una caída de -79,3 % [C4]. Es un saldo, no nuevas operaciones.

![Hipotecas por compraventa](../output/v5/CA/figuras/contado_ratio.png)

**Lectura.** Hay un volumen grande de compras sin hipoteca, cuya magnitud exacta depende de qué fracción de las hipotecas financia compras de vivienda. Es compatible con compras de inversores y de hogares con ahorro acumulado o con ayuda familiar, pero los datos no separan a unos de otros. El crédito a promotores es una fracción del de la década anterior, lo que es compatible con una financiación de la construcción más restringida, sin que se pueda separar la oferta de crédito de la demanda.

### 5.5 Seguridad jurídica (CB)

- Lanzamientos por la LAU (principalmente impago de alquiler): 18.317 lanzamientos/anio en 2025, frente a un máximo de 38.141 lanzamientos/anio en 2013-2025 [C4].
- Hechos conocidos de allanamiento o usurpación: 14.875 hechos/anio en 2025; procedimientos verbales posesorios por ocupación ingresados: 1.845 procedimientos/anio [C4].
- Frente a 2.965.497 viviendas principales en alquiler, los órdenes de magnitud son pequeños. Con los datos públicos no se puede contrastar si la percepción de inseguridad reduce la oferta de alquiler: la correlación entre comunidades no es un diseño que lo permita.

### 5.6 Fiscalidad (CB)

- La reducción por arrendamiento de vivienda se aplica a 2.236.896 declarantes [C4].
- No hay en el repositorio una evaluación de la incidencia de los cambios fiscales en la oferta de alquiler. La matriz D1 los deja como «no evaluable» (instrumento `I15`).

### 5.7 Desigualdad (CC)

| Grupo | Sobrecarga de coste de vivienda, 2025 | 2015 | Capa |
|---|---|---|---|
| Primer quintil de renta | 27,7 % de personas | 40,9 % de personas | C4 |
| Quinto quintil de renta | 0,20 % de personas | — | C4 |
| Inquilinos a precio de mercado | 26,8 % de personas | 43,3 % de personas | C4 |
| Propietarios con hipoteca | 3,4 % de personas | 8,7 % de personas | C4 |

- Los inquilinos a precio de mercado situados en los tres primeros deciles de renta son 46,9 % de personas inquilinas [C4].
- Hogares jóvenes (de dieciséis a veintinueve años) en propiedad: 30,6 % de hogares en 2025 frente a 34,2 % de hogares en 2015; en vivienda cedida, 14,7 % de hogares frente a 17,4 % de hogares [C4]. En propiedad sin hipoteca, 14,1 % de hogares, que se usa solo como aproximación a la ayuda familiar, no como medida [C4].
- La sobrecarga ha bajado desde 2015 en todos los grupos [C4]. Eurostat-SILC es la ECV del INE: no hay segunda fuente y la cifra es C4.

**Lectura.** La sobrecarga de coste es mucho mayor entre los hogares de renta baja y los inquilinos a precio de mercado que entre los propietarios. Su descenso desde 2015 coincide con el aumento del empleo y de la renta, y con una caída de la proporción de propietarios con hipoteca; no se atribuye a ninguna medida. Los hogares jóvenes en propiedad son menos que en 2015.

### 5.8 Vivienda protegida (CC)

- Calificaciones definitivas de vivienda protegida: 11.265 viviendas/año de media en 2021-2025 [C4].
- Viviendas protegidas que saldrían del régimen en 2026-2035: 594.890 viviendas en el escenario base, entre 532.040 viviendas y 669.394 viviendas [C4]. Los plazos de algunos planes no constan en los reales decretos y se suponen.
- Las salidas anuales serían 5,3 ratio (4,7-5,9 ratio) veces las calificaciones nuevas [C4]. Con un régimen permanente, la cota inferior lógica sería cero.

**Lectura.** Por cada vivienda protegida que se califica, en la próxima década saldrán del régimen varias, según los plazos de los planes antiguos. El parque protegido puede reducirse aunque se mantenga el ritmo de calificaciones, salvo que los plazos se prolonguen o se califiquen más viviendas. Es una contabilidad con supuestos de plazo, no una previsión.

---

## 6. Matriz de instrumentos (D1), resumida

La matriz completa está en [output/v5/D1/matriz_instrumentos.md](../output/v5/D1/matriz_instrumentos.md). Aquí se resume.

**Rúbrica.** La misma para cada instrumento: evidencia y capa, magnitud y rango, signo, plazo, coste fiscal, riesgos, distribución, clase de A4 donde funcionaría y documentos que lo proponen. Se evalúan 36 instrumentos; en 18 instrumentos el signo es «no evaluable» por falta de literatura verificada o de simulación propia [C4]. «No evaluable: motivo» sustituye a cualquier opinión.

**Traslado de las ayudas a la demanda al precio, por clase [C4].** Parte de una ayuda general que captan vendedores o arrendadores, con la rejilla de elasticidades de demanda de v3:

| Clase A4 | Método A (respuesta de oferta de A4) | Método B (rejilla de oferta de v3) |
|---|---|---|
| `1` | 58,4 % (27,8-81,8 %) | 30,9 % (14,6-46,2 %) |
| `2` | 100,0 % (88,1-100,0 %) | 100,0 % |
| `3` | 76,4 % (50,1-89,8 %) | 63,1 % (40,0-76,9 %) |

Los dos métodos discrepan en la clase `1` y se dan ambos.

**Resumen por grupos de instrumentos.**
- **Con signo estable en la rejilla de v3 [C2 en el signo, C4 en la magnitud].** Más construcción donde falta (`P1`) y movilización de vivienda vacía (`I10`, `I27`, `N7`).
- **Con literatura verificada de otros países.** Edificabilidad (`N2`: Büchler y Lutz, 2024; Greenaway-McGrevy y Phillips, 2023) y licencias (`N1`, `I13`: Ball, 2011, solo asociación). Sin evaluación en España.
- **Regulación de precios del alquiler (`I01`).** El resultado propio de v3 (`H3-3`) queda fuera de C3 por la contaminación de la validación; la réplica de García-López y otros no se reproduce con los datos de stock (sección de limitaciones). La literatura verificada da resultados de distinto signo según la oferta. Signo no estable.
- **Ayudas a la demanda (`I06`-`I09`, `N9`).** Su traslado al precio depende de la respuesta de la oferta, por clase territorial (A4, método A, rejilla de elasticidades de demanda): clase `1`, falta y es rentable, 27,8-81,8 %; clase `2`, la oferta no responde, 88,1-100,0 %; clase `3`, no rentable, 50,1-89,8 % [C4]. El extremo bajo se apoya en la literatura con oferta elástica (Eriksen y Ross, 2015) y el alto en la de oferta rígida (Gibbons y Manning, 2006; Hilber y Turner, 2014).
- **Parque público (`I02`).** Signo menor o igual que cero en la rejilla (posiblemente nulo) si desplaza construcción privada.
- **No evaluables.** Rehabilitación, industrialización, seguridad jurídica, fiscalidad de arrendadores, entre otros: sin literatura verificada con magnitud ni simulación propia.

**Cómo leer la matriz.** Cada fila indica qué se sabe del instrumento, con qué capa y de dónde procede la evidencia. Una celda «no evaluable» no es una valoración negativa del instrumento: significa que el proyecto no ha encontrado literatura verificada con magnitud ni ha podido simularlo. Los documentos programáticos que proponen cada instrumento se cuentan con un diccionario de palabras clave cuya precisión estricta es 50,0 % [C4]: son cotas de coincidencias, no recuentos de medidas validadas.

**Lectura.** Con la evidencia disponible, lo que tiene signo estable es aumentar la oferta donde falta y movilizar vacías. Lo que más depende del territorio es el traslado de las ayudas a la demanda: donde la oferta no responde, la mayor parte de una ayuda general acabaría en el precio. Esto no es una recomendación sobre un instrumento concreto: es una condición que cualquier diseño tendría que tener en cuenta.

---

## 7. Política por territorio (D2), en lenguaje condicional

D2 cruza la necesidad de T3, la clase de A4 y la matriz de D1. Desde v6.3, D2 usa la misma necesidad provincial que el titular (v5.1 T3, 210.424 viviendas/año sin la sensibilidad X; suma de 52 provincias), no la de B1 (v5). Todo es C4: no hay efectos estimados por clase en España. El texto completo está en [output/v5/D2/politica_territorio.md](../output/v5/D2/politica_territorio.md). <!-- check:cifra-libre (etiquetas de versión y módulo) -->

**Clase `1` (37 provincias, 8 robustas).**
- Necesidad: 185.283 viviendas/año (96.224-251.870 viviendas/año) [C4].
- Si el objetivo fuese cubrir esa necesidad, los instrumentos con signo estable serían más construcción y movilización de vacías.
- La construcción adicional de la rejilla de v3, repartida por cuota de necesidad, cubriría 11,9-47,5 % de la necesidad; las vacías movilizables, 57.230 viviendas/año (28.615-85.845 viviendas/año), el 30,9 % en el central [C4].
- Una ayuda general a la demanda sin más oferta se trasladaría al precio en 27,8-81,8 % (método A) [C4].

**Clase `2` (11 provincias, 3 robustas).**
- Necesidad: 21.155 viviendas/año (2.983-35.113 viviendas/año) [C4].
- La clase se define porque la oferta no responde: si el cuello de botella es de suelo o de tramitación, los instrumentos que actúan sobre él (edificabilidad, licencias) serían los aplicables según la literatura verificada de otros países.
- Construcción adicional: 11,9-47,5 % de la necesidad; vacías: 16.125 viviendas/año (8.063-24.188 viviendas/año), el 76,2 % en el central [C4].
- Una ayuda general a la demanda se trasladaría al precio en 88,1-100,0 % [C4].

**Clase `3`.** Necesidad: 3.260 viviendas/año (-112,0 a 4.185 viviendas/año) [C4]. Si construir no es rentable con el coste oficial, los instrumentos de oferta privada tendrían poco recorrido sin cambios en coste o suelo.

**Clase `9`.** Necesidad: 726,0 viviendas/año (293,0-919,0 viviendas/año) [C4]. Sin clase: no evaluable.

**Lectura.** Las combinaciones son condicionales: «si el objetivo es X y la provincia está en la clase Y, los instrumentos con signo estable son Z». No son recomendaciones con efecto estimado.

---

## 8. Módulo València

### 8.1 Necesidad y clase

- Déficit contable 2021-2025 de la provincia de València: 68.926 viviendas (59.206-80.093 viviendas) [C4]; de la ciudad, 13.048 viviendas (fuente única) [C4].
- Necesidad anual 2026-2035 de la provincia: 16.993 viviendas/año (13.241-22.407 viviendas/año) [C4].
- Déficit acumulado a fin de 2030 en la provincia: 118.711 viviendas (112.120-128.910 viviendas) [C4]; empeora en todo el rango.
- Clase A4 de la provincia: `1` (falta y es rentable) [C4]. La ciudad pasa de la clase `2` de v4 (coste supuesto, estabilidad 97,2 %) a la clase `1` en v5 con el rango oficial de coste [C4]: el cambio de clase procede del cambio de coste, no de un cambio en el mercado.
- Valor tasado de la vivienda libre en la ciudad: 2.849 €/m² [C4].

### 8.2 Alquiler por distritos (SERPAVI con nombres)

Los distritos censales de SERPAVI se cruzan con los 19 distritos municipales (supuesto declarado: coinciden uno a uno; `output/v5/R1T`). En 2024 hay 65.742 contratos (min-max por distrito) contratos con renta declarada [C4].

| Indicador | Valor | Distrito | Capa |
|---|---|---|---|
| Renta mediana más alta, 2024 | 10,9 €/m²/mes | distrito Ciutat Vella | C4 |
| Renta mediana más baja, 2024 | 5,9 €/m²/mes | distrito Poblats Del Nord | C4 |
| Mediana entre distritos, 2024 | 8,0 €/m²/mes | — | C4 |
| Mayor crecimiento 2015-2024 | 85,8 % | distrito Ciutat Vella | C4 |
| Menor crecimiento 2015-2024 | 50,7 % | distrito Poblats Del Nord | C4 |
| Mediana del crecimiento entre distritos | 73,5 % (50,7-85,8 %) | — | C4 |

La tabla completa por distrito, con nombre, renta mediana de 2015 y 2024, contratos y posición, está en `output/v5/R1T/serpavi_distritos_valencia_nombres.csv`. El centro histórico encabeza a la vez el nivel y el crecimiento; los poblados periféricos tienen pocas observaciones y su crecimiento es menos preciso.

### 8.3 Viviendas turísticas: INE frente a GVA (R1A)

- El registro de la GVA (stock) cuenta 1,6 veces (1,4-1,8 veces) veces las viviendas turísticas que estima el INE en las tres provincias valencianas, 2020-2024 [C4].
- Con el registro vigente de la GVA de octubre de 2026 frente al INE de mayo de 2026, la razón es 1,8 veces (1,4-1,9 veces) [C4].
- La suma de secciones del INE cubre 90,4 % del total provincial [C4].
- La diferencia se descompone en cotas por factor (fechas de baja, definiciones, cobertura); el residual no tiene cota inferior (`BK-052`).

### 8.4 Fianzas de la GVA (A23)

- Mediana de la fianza depositada: 500 € en 2020 y 790 € en 2025 [C4], con 35.079 contratos fianzas en 2025.
- La renta de contratos nuevos (mediana de la fianza) sube 58,0 % en 2020-2025 [C4]; con el IPVA de nuevo contrato, el rango 2021-2024 de la Comunitat Valenciana es 28,5 % (26,1-30,8 %) [C1].
- Rotación (fianzas sobre contratos vigentes): 13,5 % (13,5-15,8 %) [C4].
- Municipios con mediana de fianza que se duplica: 2 municipios [C4].
- Las fianzas no traen la duración del contrato: el alquiler de temporada y por habitaciones sigue sin fuente (`BK-014`).

### 8.5 Heredado de v4

Se mantiene la lectura del módulo València de v4 (`output/v4/informe_tecnico.md`):
- [C4] la provincia de València está entre las tres primeras en déficit contable 2021-2025;
- el componente de nacionalidad extranjera pesa más en la variación de hogares de la provincia que en el conjunto nacional [C4];
- las viviendas turísticas de la ciudad están en 2026 por debajo del nivel de 2021 en la comparación del mismo mes (INE, oleadas experimentales) [C4].

---

## 9. Convergencia con BdE, Ministerio, INE, OCDE y Eurostat (D3)

**Regla.** Una cifra «coincide» o «difiere» solo si concepto, periodo y cobertura son comparables; coincide si los rangos se solapan o si la diferencia entre puntos medios no supera la tolerancia declarada. «Comparable en parte» (otro periodo, concepto o cobertura) no cuenta como coincidencia ni como diferencia. «Control de la misma fuente» es una cifra del organismo con la misma fuente primaria que el proyecto: confirma la transcripción y no cuenta. «No comparable» si el concepto lo impide o la cifra no se localizó. Las diferencias se describen por concepto, periodo, cobertura, método o bajas. No se valora a ningún organismo.

**Resultado [C4].** Coinciden 2; difieren 1; son comparables en parte 6; son controles de la misma fuente 4; no son comparables 9.

| Cifra del proyecto | Organismo | Veredicto | Por qué |
|---|---|---|---|
| Déficit 2021-2024 [C1] | Banco de España (intervenciones públicas) | comparable en parte | periodo distinto (empieza en 2022) y concepto (creación neta de hogares menos producción) |
| Déficit 2021-2025 [C4] | Banco de España (Informe Anual; Informe de Estabilidad Financiera) | coincide | mismo periodo y concepto; comparten insumos primarios |
| Déficit 2021-2025 [C4] | Banco de España (otras ventanas); OCDE | comparable en parte | ventana 2022-2025; la OCDE reproduce la estimación del BdE |
| Terminadas 2019-2024 [C1] | Banco de España | comparable en parte | un solo año, 2025, del organismo |
| Necesidad 2026-2035 [C4] | Ministerio; OCDE | no comparable | cifra del Ministerio no localizada; la de la OCDE es otro concepto (vivienda social) |
| Déficit a 2030 [C4] | Banco de España | no comparable | cifra no localizada |
| Precio 2015-2025, núcleo [C1] | Eurostat (IPV del INE) | difiere | son medidas distintas (puente de precio, sección de diagnóstico) |
| Precio 2015-2025, IPV; alquiler de stock; sobrecarga; emancipación | Eurostat | control de la misma fuente | misma fuente primaria: confirma la transcripción, no la cifra |
| Propiedad de la vivienda principal [C1] | Eurostat | comparable en parte | otro concepto (población frente a hogares) |

La tabla completa, con documento y página de cada organismo, está en [output/v5/D3/convergencia.md](../output/v5/D3/convergencia.md).

**Lectura.** La única diferencia en sentido estricto es la del precio, y se explica por el puente entre el índice del INE y el núcleo de tres fuentes. Las coincidencias en el déficit 2021-2025 comparten insumos con el proyecto; las de Eurostat en sobrecarga, emancipación, precio y alquiler comparten fuente primaria: confirman la transcripción, no la cifra.

**Por qué difieren las cifras de déficit.** La diferencia con las intervenciones del Banco de España sobre el déficit no es de método sino de definición: el organismo mide la creación neta de hogares menos la producción en ventanas que empiezan en 2022, mientras que el proyecto empieza en 2021, el primer año con la corrección de la ruptura de la EPA. Con la ventana 2021-2025 y bajas nulas, el proyecto coincide con las cifras del Informe Anual y del Informe de Estabilidad Financiera. Que coincidan no eleva la capa: el componente de 2025 sigue siendo de fuente única.

**Lo que no se ha podido comparar.** La necesidad a diez años y el déficit a 2030 no tienen una cifra publicada localizable con el mismo concepto. Cuando aparezca, la comparación se añadirá con la misma regla.

---

## 10. Limitaciones y lo que no se puede afirmar

### 10.1 Lo que no se puede afirmar

- **Que una familia de factores «explique» la subida de precios.** Las contribuciones contables no son estables entre métodos ni periodos [C4].
- **Que los grandes tenedores o los fondos determinen los precios.** No hay datos públicos del parque por tipo de propietario. El verificador lo deja en «no analizada: faltan datos».
- **Que los topes al alquiler bajen o suban las rentas en España.** El resultado de v3 está fuera de C3 por contaminación de la validación; la réplica de García-López y otros no se reproduce (coeficiente propio -4,2 milésimas de log-punto por punto de VUT/parque (-7,8 a -0,54 milésimas de log-punto por punto de VUT/parque), p ajustado 26,9 % (valor p)) porque el stock de SERPAVI recoge solo 55,1 % de la variación del flujo [C4].
- **Que las viviendas turísticas suban el alquiler nacional.** La asociación de v3 no se distingue de cero (0,26 milésimas de log-punto por VUT/100 viv. (-0,74 a 1,3 milésimas de log-punto por VUT/100 viv.), p ajustado 46,7 % (valor p)); la cota de cantidad es 2,7 % del stock de alquiler [C2].
- **Que haya una burbuja.** Las pruebas de exuberancia (GSADF) con tamaño corregido detectan episodios en algunas razones de precio y no en otras; una exuberancia estadística no es una burbuja (sección de robustez del working paper).
- **Que el pre-registro de B3 confirme una hipótesis.** Su potencia era insuficiente; el resultado es descriptivo.
- **Que alguna variable sea «relevante con seguridad» para el alquiler o la compra (v6).** Ninguna cumple los criterios pre-registrados (0 variables) y ninguna hipótesis confirmatoria pasa Holm; las importancias de los modelos de predicción son descriptivas (véase la sección sobre alquiler y compraventa) [C4].

### 10.2 Verificador de afirmaciones

Se evalúan 40 afirmaciones del debate público: 32 afirmaciones quedan «analizada, no concluyente», 3 afirmaciones «parcialmente», 3 afirmaciones «no analizada: faltan datos» y 1 afirmaciones «contradicha» [C4]. Detalle en [output/v5/verificador/verificador.md](verificador/verificador.md).

### 10.3 Limitaciones de datos y método

- El déficit provincial y la necesidad son C4: dependen de fuentes únicas en algún componente.
- El coste de construcción es un rango oficial derivado de una norma de 1993 y un índice; no es un coste de mercado observado.
- No hay datos públicos de personas jurídicas ni del sector público en el parque, ni de la distribución de arrendadores por número de inmuebles.
- No hay fuente oficial con la duración de los contratos de alquiler (temporada, habitaciones).
- La proyección a 2030 no incorpora la reacción de la oferta ni de la formación de hogares a los precios.
- Las clases de A4 son C4 y todo lo que se apoya en ellas (D1 por clase, D2) también.

### 10.4 Backlog pendiente

Del backlog (`docs/v5/backlog.md`) quedan abiertos o parciales:
- `BK-040`: sensibilidad de los diseños de v2, parcial (sin sensibilidad en un modelo; uno solo con RV aproximado por estar en muestra sellada).
- `BK-014`: alquiler de temporada y por habitaciones, no analizado por falta de datos.
- `BK-017`: réplica con datos privados, no ejecutable.
- `BK-050`, `BK-051`, `BK-042`, `BK-038`: series sin incorporar, tabla de relaciones del seccionado, un bloque de modelos de v2 y un análisis de v3 no especificado ni pre-registrado.
- Abiertos por fuentes: Atlas de Áreas Urbanas (`BK-041`), afiliación de la construcción por provincia (`BK-009`), Notariado y Registradores por residencia del comprador (`BK-002`).
- Solicitudes de datos a organismos: `docs/v5/solicitudes.md`.

### 10.5 Qué datos cambiarían las conclusiones

- **Parque por tipo de propietario** (Catastro por titular, con personas jurídicas y sector público): permitiría pasar de «no analizada» a una cifra en las afirmaciones sobre grandes tenedores.
- **Distribución de arrendadores por número de inmuebles** (AEAT): separaría pequeños y grandes arrendadores.
- **Duración de los contratos de alquiler** (registros de fianzas de todas las comunidades): permitiría medir el alquiler de temporada y por habitaciones.
- **Una segunda fuente de hogares en 2025**: subiría el déficit 2021-2025 de C4 a C1 si los componentes coincidieran.
- **Coste de construcción observado** (no derivado de una norma): reduciría la incertidumbre de las clases de A4 y, con ella, la de todo lo que se apoya en las clases.
- **Microdatos de transacciones con residencia del comprador por provincia** (Notariado y Registradores): elevarían la capa de las cifras sobre no residentes.

Las solicitudes a organismos están en `docs/v5/solicitudes.md`. Ninguna conclusión de este informe depende de datos privados.

---

### 10.4 Limitaciones (revisión por pares simulada v6.1) <!-- check:cifra-libre (etiqueta de versión pedida en el título) -->

Objeciones de la revisión por pares simulada (informes del árbitro académico y del revisor de política pública) que no se pueden resolver sin nuevas estimaciones. Cada punto indica el motivo y el coste.

- **Capa del déficit acumulado.** El extremo superior depende de una corrección constante de la EPA, y las terminadas son dos variantes del Ministerio. Para mantener la etiqueta [C1] con fuentes independientes en sentido fuerte habría que recalcular el rango con las altas del Catastro como segunda fuente de terminadas, o rebajar la capa en cifras_clave. Exige recalcular el módulo y regenerar las cifras.
- **Validación sellada.** La comparación con líneas base nuevas fue una segunda mirada a la muestra sellada, y la parte temporal ya se había visto. Una validación confirmatoria limpia exige una muestra nueva (el año siguiente), que todavía no existe.
- **Inferencia con once provincias selladas.** Dar como criterio principal el DM por periodo o agrupado por comunidad, y el efecto mínimo detectable, exige reejecutar las comparaciones.
- **Multiplicidad entre versiones.** La relación entre inmigración y precios se ha reestimado en varias versiones con correcciones dentro de cada módulo, no conjuntas. Un recuento conjunto con su p ajustado exige reconstruir los registros de todas las versiones. Hasta entonces, ningún p de una versión aislada debe leerse como confirmatorio.
- **Pocos conglomerados.** Generalizar el wild cluster bootstrap a todas las tablas con pocos grupos, y retirar los paneles municipales con regresor provincial, exige reestimar los módulos afectados.
- **Instrumento débil.** Los intervalos de Anderson-Rubin y la inferencia específica de diseños shift-share exigen reestimar. Las cifras de dos etapas quedan solo como historial.
- **Reproducibilidad del método de traslado y de la necesidad.** Varias cifras de modelo no se reconstruyen solo con el texto. Publicar las ecuaciones y parámetros de la rejilla exige extraerlos del código y verificarlos.
- **Utilidad para la decisión.** La tabla de instrumentos no da costes ni magnitudes por euro, y el reparto territorial usa una definición de necesidad distinta de la del titular. Las dos cosas exigen nuevos datos o recalcular el módulo de política por territorio.
- **Fecha de publicación** de las etiquetas del pre-registro: queda pendiente hasta su publicación en el repositorio remoto.

---

## 11. Alquiler y compraventa: qué se asocia y qué predice (v6)

**Pregunta.** ¿Qué variables se asocian con el alquiler y con la compraventa por provincia, municipio y distrito, qué modelo los predice mejor fuera de muestra y en qué se parecen y se diferencian los dos mercados? Todo el apartado es C4: predicción y asociación, sin lenguaje causal.

### 11.1 Medidas

- **Alquiler de stock.** SERPAVI (MIVAU), mediana del valor central en €/m²/mes por provincia, municipio y distrito; el IPC de alquiler entra solo como robustez. Es el alquiler de todos los contratos vigentes declarados, no el de los nuevos.
- **Contratos nuevos.** Se tratan por separado y solo de forma descriptiva: las fianzas con desglose por provincia cubren muy pocas provincias (Cataluña y la Comunitat Valenciana) y no admiten un modelo.
- **Compraventa, precio.** Medida declarada: valor tasado del MIVAU en €/m² (provincia anual y trimestral, municipio anual). Registradores entra como robustez.
- **Compraventa, volumen.** Compraventas de vivienda de la estadística de transmisiones del INE (ETDP), anual y trimestral por provincia.
- **Paneles.** 41 provincias de entrenamiento (2015-2024 en compra y 2015-2023 en alquiler); regresores en `t-1` con efectos fijos de unidad y año (pre-registro `prereg-v6`).

### 11.2 Validación sellada nueva y su limitación

- **Qué es nuevo.** Se sellaron 11 provincias por bloques completos de CCAA (Baleares, Aragón, La Rioja, Madrid, Murcia, Navarra, Asturias y Canarias), con sus municipios y distritos, más el último año de cada panel. Esas provincias no se habían usado nunca como validación. Cada modelo se evaluó una sola vez en la muestra sellada, sin reajustarlo.
- **Qué no es nuevo.** El último año (2025 en compra, 2024 en alquiler) cae dentro de la ventana sellada de v2, abierta para otras provincias, y todas las provincias se usaron de forma descriptiva en v4-v5. La validación es **espacial nueva; temporal ya vista**. Las conclusiones se apoyan en la parte espacial.
- **Limitación de la comparación.** En provincias nuevas, el AR por unidad, el ECM v1 y la econometría de M1 no tienen efecto fijo y quedan reducidos a la persistencia.

### 11.3 Mejor modelo por mercado, medida y nivel

Error en la parte espacial sellada (RMSE en log-puntos multiplicados por cien, aproximadamente en %), frente a la persistencia (el último valor observado) en la misma muestra [C4]:

| Mercado | Medida | Nivel | Mejor modelo | Error sellado (aprox. %) | Persistencia (aprox. %) | Mejora a la persistencia |
|---|---|---|---|---|---|---|
| Alquiler de stock | SERPAVI | provincia | gradient boosting | 1,6 | 4,2 | sí (DM-HLN, Holm) |
| Alquiler de stock | SERPAVI | municipio | random forest | 5,1 | 6,5 | sí (DM-HLN, Holm) |
| Alquiler de stock | SERPAVI | distrito | gradient boosting | 5,6 | 7,0 | sí (DM-HLN, Holm) |
| Compra, precio | valor tasado MIVAU | provincia anual | random forest | 2,5 | 4,0 | sí (DM-HLN, Holm) |
| Compra, precio | valor tasado MIVAU | provincia trimestral | bosque con bootstrap bayesiano | 1,6 | 1,9 | sí (DM-HLN, Holm) |
| Compra, precio | valor tasado MIVAU | municipio anual | ECM v1 (línea base) | 3,9 | 6,3 | sí, pero el ML no mejora la línea base |
| Compra, precio | Registradores (robustez) | provincia anual | ECM v1 (línea base) | 4,7 | 6,0 | sí, pero el ML no mejora la línea base |
| Compra, volumen | ETDP (INE) | provincia anual | bosque con bootstrap bayesiano | 13,0 | 15,9 | sí (DM-HLN, Holm) |
| Compra, volumen | ETDP (INE) | provincia trimestral | bosque con bootstrap bayesiano | 11,3 | 18,5 | en la parte espacial sí; en la temporal no |

Fuente: `output/v6/M4/mejor_modelo.csv` y `output/v6/M4/tabla_modelos.md`. El mejor modelo se elige por el error espacial sellado y la estabilidad entre periodos, nunca por el R². En el precio municipal y en Registradores el bosque no mejora al ECM v1 en más de un 5 % del error, y se queda la línea base.<!-- check:cifra-libre -->

**Lectura.** Los árboles predicen mejor el alquiler de stock y el precio provincial que la inercia, en provincias que no vieron. En el precio municipal y con Registradores, la econometría heredada (ECM v1) basta. Predecir mejor no identifica por qué sube el precio. Frente a la línea base más exigente (§11.3 bis), la ventaja se mantiene en el alquiler de stock y en el precio trimestral de tasación. En el precio provincial anual es frágil, y en el precio trimestral el modelo queda por detrás de la base en la parte temporal. <!-- check:cifra-libre (referencia a sección) -->

### 11.3 bis Frente a la línea base más exigente (v6.1) [C4]

En v6.1 la comparación se repite en la misma validación sellada, con tres líneas base más exigentes que la persistencia: <!-- check:cifra-libre (etiqueta de versión o referencia a sección) -->
- el último valor provincial multiplicado por el crecimiento nacional;
- un AR provincial con factor común;
- efectos fijos de provincia y año.

Solo cuentan como «predice mejor» los modelos que superan a la línea base con menor error en DM-HLN y en una permutación exacta sobre las provincias selladas, ambas con Holm. El modelo predice mejor que la base más exigente en 6 de las 9 tareas.

| Mercado | Nivel | Error del mejor modelo (aprox. %) | Base más exigente (aprox. %) | Cociente | Clase |
|---|---|---|---|---|---|
| Alquiler de stock (SERPAVI) | provincia | 1,6 | 2,2 (AR con factor común) | 0,73 | predice mejor |
| Alquiler de stock (SERPAVI) | municipio | 5,1 | 5,4 (AR con factor común) | 0,93 | predice mejor |
| Alquiler de stock (SERPAVI) | distrito | 5,6 | 6,1 (ECM v1) | 0,92 | predice mejor |
| Compra, valor tasado | provincia anual | 2,5 | 2,8 (ECM v1) | 0,88 | predice mejor, frágil (el DM por periodo no es significativo) |
| Compra, valor tasado | provincia trimestral | 1,6 | 1,8 (AR con factor común) | 0,89 | predice mejor |
| Compra, valor tasado | municipio anual | 4,1 | 3,9 (ECM v1) | 1,05 | no distinguible |
| Compra, Registradores | provincia anual | 4,7 | 4,7 (ECM v1) | 1,00 | no distinguible |
| Compra, volumen (ETDP) | provincia anual | 13,0 | 13,7 (ECM v1) | 0,95 | no distinguible |
| Compra, volumen (ETDP) | provincia trimestral | 11,3 | 16,7 (AR con factor común) | 0,68 | predice mejor en la parte espacial; peor en la temporal |

Fuente: `output/v6_1/K1/tabla_modelos_k1.md`. Error del grupo espacial sellado. Es una segunda mirada a la misma muestra sellada, pero solo para comparadores nuevos: las predicciones de los modelos de v6 no cambian. Con pocas provincias selladas, «no distinguible» no significa equivalencia.

**Lectura v6.1.** Frente a la línea base más exigente, la ventaja de los árboles se mantiene en el alquiler de stock y en el precio trimestral de tasación. En el precio provincial anual es frágil. Desaparece en el precio municipal, con Registradores y en el volumen anual. Lo que en v6 se leía como «predice mejor que la inercia» queda acotado a estas tareas. <!-- check:cifra-libre (etiqueta de versión o referencia a sección) -->

### 11.4 Peso predictivo de cada variable en alquiler y en compra [C4]

Dos lecturas complementarias, ambas asociativas:
- **M2 (incertidumbre de modelo).** Probabilidad de inclusión posterior (PIP) del promedio bayesiano de modelos (BMA), con el multiverso y la doble selección (PDS) como contraste. El BMA completo solo usa las observaciones con viviendas turísticas y suelo; el «núcleo» prescinde de esas dos variables y tiene más observaciones.
- **M4 (síntesis).** Una variable sería «relevante con seguridad» solo si pasara los criterios pre-registrados en las tres familias (econometría, incertidumbre de modelo y predicción). Ninguna lo hace (0).

| Variable | PIP alquiler (completo / núcleo) | PIP compra, precio (completo / núcleo) | Síntesis M4 |
|---|---|---|---|
| Población | 1,0 / 1,0 | 0,76 / 1,0 | apoyo en una familia en los dos mercados |
| Población extranjera | 0,30 / 0,06 | 0,31 / 0,77 | apoyo en una familia en alquiler; sin apoyo en compra |
| PIB por habitante | 0,10 / 0,19 | 0,84 / 0,47 | apoyo en una familia en compra; sin apoyo en alquiler |
| Viviendas libres iniciadas | 0,09 / 0,97 | 0,12 / 0,06 | sin apoyo suficiente |
| Viviendas libres terminadas | 0,17 | 0,12 | sin apoyo suficiente |
| Viviendas turísticas | 0,12 | 0,10 | sin apoyo suficiente |
| Municipios con tope de alquiler | 0,23 | — | sin apoyo suficiente |

**Variables que aparecen en más modelos (PIP) en un mercado y no en el otro (C4, con discrepancias declaradas).**
- **Población:** se asocia con los dos mercados (aparece en más modelos, PIP alta) con los dos métodos.
- **PIB por habitante:** se asocia con la compra y no con el alquiler (aparece en más modelos) con el BMA completo y con la síntesis de M4; en el núcleo la diferencia se reduce.
- **Población extranjera: los métodos discrepan.** En el núcleo de M2 se asocia con la compra (PIP 0,77) y no en el alquiler (PIP 0,06); en la síntesis de M4 tiene apoyo en el alquiler (familia de predicción) y no en la compra. Se dan las dos lecturas y ninguna se elige.
- **Viviendas iniciadas: los métodos discrepan.** En el núcleo de M2 aparecen en más modelos (PIP) del alquiler que de la compra; en el BMA completo y en la síntesis de M4 no ayudan a predecir ninguno de los dos. Esa asociación con el alquiler no indica que construir suba el alquiler: en el análisis de orden temporal de K3 (`output/v6_1/K3/iniciadas.md`, provincias de entrenamiento, C4) ni los retardos ni los adelantos de las iniciadas se distinguen de cero respecto al crecimiento del alquiler, y el crecimiento previo del alquiler tampoco predice las iniciadas tras ajustar por comparaciones múltiples. Solo el contemporáneo es positivo y no sobrevive a Holm; es compatible con que la construcción se dirija a mercados con alquileres ya tensionados, sin que la muestra permita ordenar los hechos en el tiempo. En el volumen de compraventas el BMA les da una PIP de 0,98, con signo negativo. <!-- check:cifra-libre (etiquetas de módulo) -->
- **Viviendas turísticas y topes:** no tienen apoyo suficiente en ningún mercado.

En la econometría de M1, la población es la variable con la asociación más clara con el alquiler de stock provincial (4,6 EUR/mes (1,1-8,1 EUR/mes) por cada diez mil habitantes, en 2021-2023), pero no sobrevive a Holm y los métodos de contraste discrepan [C4].

Las importancias, los SHAP y los ALE de los modelos de predicción (`output/v6/M3A`, `output/v6/M3B`) son descriptivos: dicen qué variables ayudan al modelo a predecir, no qué ocurriría si una variable cambiara.

### 11.5 Relación entre el mercado de compra y el de alquiler [C4]

- **Elasticidad precio-alquiler.** Un uno por ciento más de alquiler de stock se asocia con entre un 0,59 % (anual, 2015-2023, efectos fijos de provincia y tendencia) y un 2,1 % (trimestral, 2015T1-2024T4, DOLS) más de valor tasado. La magnitud depende de la especificación y se dan los dos extremos. Es una asociación entre dos precios que se mueven juntos, no una transmisión de uno a otro.
- **Ratio precio/alquiler.** La mediana provincial pasa de 20,3 años de alquiler en 2015 a 17,1 en 2023: el alquiler de stock ha subido más que el valor tasado. La rentabilidad bruta mediana es 5,8 % del valor tasado, frente a un coste de uso de 4,3 % del valor, este último con supuestos explícitos.
- **Exuberancia.** El GSADF con tamaño corregido sobre el ratio precio/IPC de alquiler no detecta exuberancia en ninguna CCAA: 0 de 11 CCAA contrastadas (2015T1-2024T4). No detectar exuberancia no prueba que no la haya; las series son cortas.

### 11.6 Qué separa a unas provincias de otras según los modelos [C4, descriptivo]

- **Alquiler.** Las provincias con más población y, según la familia de predicción, con más población extranjera son las que los modelos asocian con alquileres más altos y subidas mayores.
- **Compra.** En el precio, la población y el PIB por habitante concentran el apoyo.
- **Vecindad.** El precio de una provincia se parece al de sus vecinas (autocorrelación espacial de 0,28); el volumen apenas (0,12).
Es una descripción de lo que comparten las provincias caras o con subidas mayores, no una atribución de la subida a esos factores. El verificador recoge estas dos preguntas (fichas `M4-V1` y `M4-V2`) con el veredicto «analizada, no concluyente».

### 11.7 Resultados negativos

- **Ninguna variable «relevante con seguridad».** 0 variables cumplen los criterios pre-registrados. En la especificación pre-registrada pasan Holm 0 de 16 hipótesis confirmatorias de alquiler y 0 de las de compra: con solo 41 provincias de entrenamiento y regresores en `t-1`, la potencia es baja.
- **El deep learning no bate al gradient boosting.** En el alquiler por distrito (validación interna), el MLP (4,8 %) y GraphSAGE (4,8 %) quedan a la par del gradient boosting (4,8 %), sin diferencia significativa (p de 0,63 y 0,61 en el contraste DM-HLN). En el precio municipal, el MLP (5,2 %) y la red espacial (8,3 %) tienen más error que el mejor bosque (5,0 %).
- **La persistencia no se bate en el volumen trimestral.** En la parte temporal sellada (2025), el bosque da 12,0 % de error frente a 11,3 % de la persistencia. En la validación interna, la persistencia iguala al ML en el volumen trimestral (25,7 % frente a 25,7 %) y en el precio trimestral (1,9 % frente a 1,9 %), aunque los dos baten con claridad al AR(4) (3,5 % en el precio). La inercia es la referencia difícil de batir en la compra trimestral.
- **Ninguna hipótesis confirmatoria pasa Holm**, ni en alquiler ni en compra. La identificación disponible (un solo choque de exposición y topes con pretendencias rechazadas) no alcanza C3.

Fuentes: `output/v6/M1A`, `output/v6/M1B`, `output/v6/M2/peso_variables.md`, `output/v6/M3A`, `output/v6/M3B` y `output/v6/M4`; decisiones en `docs/v6/decisiones.md`.

---

## 11 bis. Qué añade la versión de referencia v7.2 (atlas regional) [C4]

- **Domina el componente común.** La variación interanual del precio de cada comunidad acompaña en gran medida a la media de las 17: el R² mediano es 93,6 % en compra y 86,1 % en alquiler. Es una descripción, no un modelo.
- **No hay un largo plazo regional confirmado.** Se confirman 0 de las siete hipótesis pre-registradas (empleo, población, hipotecas y paro). En compra no se descarta que la serie sea I(2) en 8 de 17 comunidades. En la simulación, con un componente común así, ningún estimador de panel es fiable (nota metodológica).
- **Traslado al precio de las ayudas a la demanda y de la rebaja de ITP/IVA** (escenario condicional). Reducen el precio neto que paga el beneficiario: su esfuerzo varía un -5,3 % con la ayuda. Pero el precio de mercado sube un 4,4 % con la ayuda y un 1,1 % con la rebaja, a diez años (mediana entre comunidades). *Nota:* el signo lo fija en gran parte la fórmula de incidencia; lo informativo son las magnitudes relativas.
- **Dosis y coste.**
  - Coste fiscal anual mediano por comunidad: ayudas a la demanda, 378,2 M€/año; rebaja de ITP/IVA, 93,3 M€/año. La rebaja de impuestos y costes de construcción no se difunde: su escenario sobrestima el efecto por diseño (traslada la rebaja a todo el mercado y el coste solo cubre la obra nueva).
  - Coste anual por punto de reducción del precio neto: 76,4 M€/año por punto y 82,4 M€/año por punto.
  - Construcción, vacías, vivienda pública y turísticos no tienen coste estimable, porque no hay coste unitario verificado. Se comparan por su efecto por cada diez mil viviendas: en alquiler, -1,7 puntos % con vacías y -3,2 puntos % con vivienda pública (mediana). <!-- check:cifra-libre (unidad de normalización «diez mil viviendas», no son cifras de resultado) -->
  - Robustez en la rejilla simulada (C4; no es robustez estadística): la movilización de vacías es robusta en 17 de 17 comunidades en alquiler; las ayudas a la demanda, en 0.
- Detalle por comunidad: atlas regional (atlas_regional/). Método: [nota metodológica](nota_metodologica.md). Afirmaciones evaluadas: verificador V7.

## 12. Qué cambió entre versiones y por qué

Sección única del proyecto: [Qué cambió entre versiones y por qué](que_cambio.md) (versión de referencia v7.2).

## Anexo A. Datos y fuentes

| Bloque | Fuentes | Ruta |
|---|---|---|
| Hogares | INE ECP, EPA (ruptura de 2021 tratada según la ventana; anexo metodológico), proyecciones de hogares | `output/v5/B1`, `output/v5/B2` |
| Terminadas e iniciadas | Ministerio (certificados de fin de obra, visados), Catastro (altas) | `output/v5/B2`, `output/v5/R1C` |
| Precio de compra | INE IPV; Ministerio (valor tasado); Notariado; Registradores | `output/v5/A23` |
| Alquiler | INE IPC e IPVA; SERPAVI; Incasòl; fianzas de la GVA | `output/v5/A23`, `output/v5/R1T` |
| Coste de construcción | BOE (módulo básico); Eurostat (índice de costes) | `output/v5/A4` |
| Europa | Eurostat (HPI, IPCA, SILC, permisos, demografía) | `output/v5/CA` |
| Crédito y contado | BdE (Boletín Estadístico); INE (hipotecas, transmisiones); Registradores | `output/v5/CA` |
| Parque y propiedad | INE Censo 2021, ECV; BdE EFF; AEAT | `output/v5/R1C`, `output/v5/CB`, `output/v5/CC` |
| Seguridad jurídica | CGPJ; Ministerio del Interior | `output/v5/CB` |
| Vivienda protegida | Ministerio (Boletín), BOE | `output/v5/CC` |
| Viviendas turísticas | INE (estadística experimental); GVA (registro de turismo) | `output/v5/R1A` |
| Convergencia | BdE, Ministerio, INE, OCDE, Eurostat | `output/v5/D3` |

Licencias: `docs/v5/licencias_datos.md`. Fuentes fallidas: `docs/v5/fuentes_fallidas.md`. Fichas de cada cifra: `output/v5/cifras_clave.md`.

## Anexo B. Replicación

- **Anexo metodológico** ([output/v6_2/anexo_metodologico.md](../metodologia/anexo_metodologico.md)): una ficha por cifra publicable, con definición, fuente y fichero de data/raw, filtros, fórmula paso a paso, supuestos, capa y script. Permite reconstruir cada cifra sin leer el código; una segunda implementación independiente, escrita solo con el anexo, se comprueba en `make check` (tests/doble_impl). <!-- check:cifra-libre (ruta de versión) -->
- `make all` reconstruye todo sin red; las descargas están en los scripts `*_fetch.py`, fuera de `make all`.
- `make check` ejecuta `src/v5/check_v5.py` (cifras fuera de marcador, sumas provinciales iguales al total nacional, capas válidas) y `src/v3/check_texto.py` (léxico valorativo o partidista y lenguaje causal por debajo de C3).
- Este informe se genera con `python3 src/v5/render.py` desde `docs/v5/plantillas/informe_tecnico.md`.
- Toda especificación probada está en los `registro.csv` de cada módulo; la muestra sellada solo se usa vía `src/holdout.py`.
- Semilla: `SEED=20261010` en todo lo aleatorio.

## Declaración de independencia y uso de inteligencia artificial

Este informe es un trabajo individual e independiente de Borja Romero, economista, sin financiación externa ni vínculo con partidos políticos. Evalúa afirmaciones e instrumentos, nunca partidos ni personas. El análisis, el código y los borradores se elaboraron con agentes de inteligencia artificial (Claude), bajo la supervisión del autor, que revisa y asume la responsabilidad del contenido. El detalle está en el apéndice C del working paper y en README_REPLICACION.md. Las correcciones se publican en ERRATA.md.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
