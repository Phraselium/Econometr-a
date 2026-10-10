# Vivienda en España: necesidad, territorio, precios e instrumentos con datos públicos

## Informe técnico v5

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
- Entre 2021 y 2024 el número de hogares creció más que el de viviendas terminadas: la diferencia está en {{deficit_2124_c1:rango}} [C1]. Con bajas del parque supuestas, el rango se amplía a {{deficit_2124_c2:rango}} [C2].
- Los hogares aumentaron en {{dh_2125}} entre 2021 y 2025 [C1].
- Se terminaron {{terminadas_1924:rango}} en 2019-2024 (territorio común) [C1].
- El precio de compra subió {{A23-P2}} en 2015-2025 según el núcleo de tres fuentes (Ministerio, Notariado y Registradores) [C1]; el índice del INE marca {{A23-P1:valor}} [C4]. Los dos se dan siempre juntos.
- La renta del stock de contratos de alquiler subió {{A23-A2:rango}} en 2015-2024 [C1]; los contratos nuevos subieron más (sección de alquiler).
- Los hogares con vivienda principal en propiedad son {{R1C-001}} [C1].

**Lo que es una proyección o una contabilidad con supuestos [C4].**
- Necesidad de vivienda 2026-2035: {{B1-H1}} de media anual, suma de {{E-E1-nprov:valor}} [C4]. El mayor componente es el crecimiento de hogares proyectado por el INE ({{B1-H4:valor}} en diez años, [C2]).
- Déficit acumulado a fin de 2030 si se mantiene el ritmo actual de terminadas: {{B2-H1}} [C4], partiendo de {{B2-H2:valor}} en 2021-2025. En el rango completo de supuestos, {{E-E1-B2-empeora:valor}} empeoran, {{E-E1-B2-mejora:valor}} mejoran y {{E-E1-B2-indeterminado:valor}} quedan indeterminadas [C4].
- El déficit está concentrado: {{A4-conc50-2021-2025:valor}} suman la mitad del déficit positivo de 2021-2025 [C4].

**Lo que no se puede afirmar.**
- Ninguna descomposición de la subida de precios es estable: el orden de las familias de factores cambia con el método y el periodo (tau de Kendall mínima {{B4-estabilidad-tau-min:valor}}) [C4]. Se habla de «contribuciones contables», no de atribuciones.
- Las diferencias de precios entre provincias se describen, no se atribuyen: el pre-registro de B3 tenía potencia insuficiente y el resultado es «descriptivo honesto» [C4].
- No se dispone de datos públicos sobre la distribución del parque por tipo de propietario (personas jurídicas, grandes tenedores); las afirmaciones del debate sobre ese punto quedan sin analizar por falta de datos.

**Instrumentos.** Con la misma rúbrica se evalúan {{D1-H01:valor}}; en {{D1-H02:valor}} el signo no es evaluable con la evidencia disponible [C4]. Donde la oferta no responde (clase `2` de A4), una ayuda general a la demanda se trasladaría al precio en {{D1-H12:valor}} según la rejilla de elasticidades [C4]. Lo que aparece con signo estable en la rejilla de v3 es más construcción donde falta y la movilización de vacías [C2 en el signo; C4 en la magnitud].

**Convergencia.** Frente a BdE, Ministerio, INE, OCDE y Eurostat, y solo cuando concepto, periodo y cobertura son comparables, las cifras del proyecto coinciden en {{D3-coincide:num}} y difieren en {{D3-difiere:num}}; otras {{D3-comparable_en_parte:num}} son comparables solo en parte (otro periodo o concepto), {{D3-control_misma_fuente:num}} comparten fuente primaria con el proyecto y no cuentan, y {{D3-no_comparable:num}} no son comparables [C4]. Las diferencias se describen por periodo, concepto o bajas del parque.

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

**2021-2024 [C1].** Con dos fuentes independientes en cada componente (hogares: ECP y EPA corregida por la ruptura de 2021; terminadas: Ministerio y Catastro), el déficit está entre {{deficit_2124_c1:rango}}. Es la única ventana en la que todos los componentes pasan la regla de dos fuentes ({{deficit_2124_c1:cita}}).

**Con bajas del parque [C2].** Si se suponen bajas anuales del parque en el rango declarado en v4, el déficit 2021-2024 queda entre {{deficit_2124_c2:rango}} [C2]. La cota inferior es la cifra sin bajas; la superior, la de bajas máximas.

**2021-2025 [C4].** Al añadir 2025, uno de los componentes pasa a depender de una sola fuente y el resultado baja a C4: {{B2-H2}} con bajas nulas [C4]. Por provincias, la mediana entre combinaciones de fuentes reparte ese total con un rango por provincia (`output/v5/A4/clasificacion_provincias.csv`).

**Lectura.** La cifra que conviene citar con seguridad es la de 2021-2024 [C1]. La de 2021-2025 es la habitual en el debate y coincide en orden de magnitud con las del Banco de España (sección de convergencia), pero es C4.

**Por qué no coinciden las cifras del debate.** Las cifras de déficit que circulan difieren por cuatro motivos, que se pueden separar: el periodo (con o sin 2021, con o sin 2025), la fuente de hogares (con o sin la corrección de la ruptura de la EPA de 2021), la fuente de terminadas (certificados de fin de obra o altas en el Catastro) y el tratamiento de las bajas del parque. La conciliación de v4 cerraba exactamente con una cadena de pasos; en v5 se mantiene y se añade la comparación con los organismos (sección de convergencia). Ninguna de las cifras es «la verdadera»: cada una responde a una definición.

### 1.2 Hogares

- Entre 2021 y 2025 los hogares aumentaron en {{dh_2125}} [C1] (INE ECP y EPA corregida por la ruptura de 2021).
- La demanda latente de jóvenes que viven con sus padres, frente a la tasa de convivencia de 2008, está entre {{latente_convivencia:rango}} [C2]. Es una cota: supone que la tasa de 2008 es la de referencia.
- El INE proyecta {{B1-H4:valor}} más en 2026-2035 [C2] y {{B2-H3:valor}} en 2026-2030 [C2]. Es un escenario del INE: no reacciona a la oferta ni a los precios.
- La descomposición contable de v4 (población por nacionalidad, edad y jefatura) se mantiene sin cambios en v5 y es C4 en los componentes de fuente única (`output/v4/M2`).

### 1.3 Viviendas terminadas

- En 2019-2024 se terminaron {{terminadas_1924:rango}} en territorio común (sin País Vasco ni Navarra) [C1]: Ministerio (certificados de fin de obra) y Catastro (altas) coinciden dentro de la tolerancia declarada.
- El ritmo de 2023-2025 proyectado a cinco años da {{B2-H4}} en 2026-2030 [C4].
- El retardo medio entre iniciadas y terminadas es de {{B2-H5}} [C4].
- La cartera en construcción (iniciadas menos terminadas en dos o tres años) es de {{B1-H7}} [C4].
- Capacidad del sector: los ocupados en construcción por vivienda libre iniciada pasan de {{R1C-010:valor}} en 2008 a {{R1C-011:valor}} en 2013 y {{R1C-012:valor}} en 2025 [C4]. El coste de construcción (Eurostat) creció {{R1C-013:valor}} menos que el precio entre 2014 y 2025 [C4]. Con estos datos no se contrasta si hay un cuello de botella de mano de obra.

![Capacidad del sector de la construcción](R1C/figuras/construccion_capacidad.png)

**Lectura.** El ritmo de terminadas de los últimos años es muy inferior al aumento de hogares, y el ratio de ocupados por vivienda iniciada ha vuelto a niveles parecidos a los de antes de la crisis financiera. Eso es compatible con una capacidad del sector que no es el único freno, pero con datos agregados no se puede separar la capacidad del sector de la rentabilidad, el suelo o la tramitación.

### 1.4 Precios: el puente IPV frente al núcleo

**Dos medidas que no coinciden.**
- Núcleo de tres fuentes (Ministerio, valor tasado; Notariado; Registradores): {{A23-P2}} en 2015-2025, medias anuales [C1].
- Índice de precios de vivienda del INE: {{A23-P1}} [C4]. Eurostat publica el mismo índice, de modo que la coincidencia con Eurostat no es una segunda fuente.

**El puente.** Se reconcilian las dos medidas paso a paso, en logaritmos y con pesos comunes:
- reponderar el IPV con pesos de comunidades autónomas comunes cambia {{A23-P4:valor}} [C4];
- la composición entre vivienda nueva y usada en la media de precio por metro cuadrado aporta {{A23-P5:valor}} [C4];
- con pesos provinciales de 2015, Registradores sube {{A23-P8:valor}} y con pesos de comunidades {{A23-P9:valor}} [C4]: la reponderación geográfica amplía la diferencia en lugar de reducirla;
- queda un residuo no identificado de {{A23-P3:valor}} [C4], compatible con diferencias de método (hedónico frente a medias o medianas), calidad, tamaño y cobertura, que no se pueden separar con los datos del repositorio.

**Factor común.** Las cuatro fuentes se mueven juntas: el primer componente principal recoge {{A23-P10:valor}} de la varianza de las variaciones anuales [C4]. El desacuerdo está en el nivel acumulado, no en la dirección.

**Niveles.** Registradores {{A23-P6:valor}} y Notariado {{A23-P7:valor}} en 2025 [C4], fuentes únicas por concepto.

![Puente de precio entre el IPV y el núcleo](A23/fig1_puente_precio.png)

**Lectura.** «La vivienda ha subido un ochenta por ciento» y «ha subido la mitad» describen dos medidas distintas. Este informe da las dos y cita el núcleo como C1.

### 1.5 Alquiler: stock frente a contratos nuevos

- **Stock de contratos (todos los vigentes).** El núcleo IPC de alquiler e IPVA de contratos existentes da {{A23-A2:rango}} en 2015-2024 [C1]. SERPAVI, con composición constante, da {{A23-A2b:valor}} [C4].
- **Contratos nuevos.** El IPVA de nuevo contrato sube {{A23-A3:valor}} en 2015-2024 [C4]; en Cataluña (Incasòl) {{A23-A4:valor}} en 2015-2025 [C4]; en la Comunitat Valenciana (fianzas de la GVA) {{A23-A5:valor}} en 2020-2025 [C4].
- **Dos fuentes por territorio [C1].** Cataluña 2021-2024: {{A23-A9}} (IPVA nuevo e Incasòl) [C1]; Comunitat Valenciana 2021-2024: {{A23-A10}} (IPVA nuevo y fianzas) [C1].
- **Brecha.** En 2024 los contratos nuevos están {{A23-A6:valor}} por encima de los existentes (IPVA) [C4]. La cuota implícita de contratos nuevos en el índice es {{A23-A7}} [C4].
- **Rotación.** Fianzas sobre contratos vigentes: {{A23-A11:valor}} en Cataluña y {{A23-A12:valor}} en la Comunitat Valenciana [C4].
- **Actualización.** Si todo contrato vigente se hubiese actualizado con el HICP, el stock habría subido {{A23-A8:valor}} más en 2022-2024 [C4]: es una contabilidad con supuestos, no un contrafactual de una norma.

![Alquiler de stock y de contratos nuevos](A23/fig2_alquiler.png)

**Lectura.** El IPC de alquiler mide lo que pagan todos los inquilinos; el que busca vivienda paga el precio de contrato nuevo. Las dos cifras son correctas y miden cosas distintas.

**Por qué importa la distinción.** Una política que se evalúe con el IPC de alquiler verá cambios lentos, porque la mayoría de los contratos vigentes no se renuevan cada año; una que se evalúe con los contratos nuevos verá cambios más rápidos y más volátiles. Las dos cifras deben citarse con su definición. La rotación medida con las fianzas es baja en las dos comunidades con datos: la mayoría de los hogares inquilinos no pasa por el mercado cada año, pero quien entra lo hace a precios de contrato nuevo.

### 1.6 Comparación europea

Posición de España en la Unión Europea de los veintisiete (Eurostat; Eurostat toma el dato de España del INE, así que es coherencia, no independencia) [C4]:

| Indicador | España, nivel | Cambio desde 2015 | Capa |
|---|---|---|---|
| Precio real de la vivienda | — | {{CA-EU-hpi_real-crecimiento:valor}} | C4 |
| Alquiler real (IPCA) | — | {{CA-EU-alq_real-crecimiento:valor}} | C4 |
| Tenencia en propiedad | {{CA-EU-propiedad-nivel:valor}} | {{CA-EU-propiedad-cambio_desde_2015:valor}} | C4 |
| Alquiler a precio de mercado | {{CA-EU-alquiler_mercado-nivel:valor}} | {{CA-EU-alquiler_mercado-cambio_desde_2015:valor}} | C4 |
| Edad media de emancipación | {{CA-EU-emancipacion-nivel:valor}} | {{CA-EU-emancipacion-cambio_desde_2015:valor}} | C4 |
| Hacinamiento | {{CA-EU-hacinamiento-nivel:valor}} | {{CA-EU-hacinamiento-cambio_desde_2015:valor}} | C4 |
| Sobrecarga de coste | {{CA-EU-sobrecarga-nivel:valor}} | {{CA-EU-sobrecarga-cambio_desde_2015:valor}} | C4 |
| Viviendas con permiso por mil habitantes | {{CA-EU-permisos_1000-nivel:valor}} | {{CA-EU-permisos_1000-cambio_desde_2015:valor}} | C4 |
| Crecimiento de la población | {{CA-EU-crec_pob-nivel:valor}} | — | C4 |
| Migración neta | {{CA-EU-migr_neta-nivel:valor}} | — | C4 |

![España en la distribución europea](CA/figuras/europa_percentiles.png)

**Lectura.** Lo específico de España en 2025 es la combinación de crecimiento de la población y migración neta altos con un precio real que sube y un alquiler real (medido por el IPCA, que es un índice de stock) que baja [C4]. El rango del precio real ({{CA-EU-hpi_real-crecimiento:rango}}) refleja el desacuerdo entre fuentes de precio de la sección anterior.

---

## 2. Necesidades 2026-2035 por provincia (B1) y déficit a 2030 (B2)

### 2.1 Método de B1

La necesidad de vivienda es una contabilidad stock-flujo por provincia, con rango mínimo-central-máximo en cada componente:

**N = A + R + V + F − M − K**

| Componente | Qué es | Diez años, central (rango) | Capa |
|---|---|---|---|
| A | Atraso: déficit 2021-2025 más emancipación retrasada | {{B1-H2}} | C4 |
| R | Reposición del parque | {{B1-H3}} | C4 |
| V | Vacancia friccional en zonas con presión | {{B1-H5}} | C4 |
| F | Crecimiento de hogares (INE) | {{B1-H4}} | C2 |
| M | Vacías movilizables en zonas con presión | {{B1-H6}} | C4 |
| K | Cartera en construcción | {{B1-H7}} | C4 |
| L | Viviendas liberadas por envejecimiento (aparte; ya neta en F) | {{B1-H8}} | C4 |

Decisiones de método:
- F, del INE, ya es neta de disoluciones de hogares. Restar además L duplicaría: se da la fórmula literal solo como variante ({{E-B1-N10_formula_literal_menos_L:valor}} en diez años) [C4].
- R se estima con dos métodos (Censo 2011-2021 más Ministerio; Catastro más Ministerio). En {{E-B1-Rnopos:valor}} las tasas brutas de baja no son positivas en ninguno de los dos: se acotan a cero y R queda como límite inferior poco informativo [C4].
- Hogares compartidos, hacinamiento y habitaciones compartidas no tienen dato provincial accesible: el rango se da sin ellos.
- La capa del total es la menor de las de sus componentes: C4.
- No es un modelo predictivo: AR(4) y ECM v1 no aplican, y no hay contrastes que ajustar.

**Qué no incluye.** La necesidad no es demanda solvente: no dice cuántas viviendas se venderían o alquilarían a los precios actuales, sino cuántas harían falta para alojar a los hogares proyectados, absorber el atraso y reponer el parque, una vez descontadas las vacías movilizables y la cartera en construcción. Tampoco distingue entre vivienda en propiedad, alquiler libre o protegido: esa elección corresponde a la política, no a la contabilidad.

**Por qué el rango es amplio.** El rango refleja tres incertidumbres que se suman: el atraso de partida (que depende de la ventana y de las fuentes), el crecimiento de hogares (el INE da un escenario y el proyecto añade una alternativa) y la parte de las vacías que se puede movilizar (entre un décimo y tres décimos de las vacías en zonas con presión, un supuesto de la rejilla de v3). Las vacías movilizables son el componente que más reduce la necesidad y el más incierto.

### 2.2 Resultado de B1

- Necesidad total: {{B1-H1}} de media anual en 2026-2035, suma de {{E-E1-nprov:valor}} [C4].
- En diez años: {{E-B1-N10}} [C4].
- Las provincias con presión (clases `1` a `3` de A4) son {{E-B1-npresion:valor}}; concentran {{E-B1-N10_solo_presion_central:valor}} de la necesidad a diez años [C4].
- Las cuatro mayores necesidades anuales: Madrid {{E-B1-anual-Madrid:valor}}, Barcelona {{E-B1-anual-Barcelona:valor}}, València {{E-B1-anual-Valencia:valor}} y Alicante {{E-B1-anual-Alicante:valor}} [C4].

![Necesidad anual de vivienda por provincia, 2026-2035](B1/figuras/B1_mapa_necesidad.png)

**Lectura.** La necesidad está concentrada donde ya hay déficit: las provincias con más necesidad anual son las mismas que encabezan el déficit contable de 2021-2025. Fuera de las provincias con presión, la necesidad procede sobre todo de la reposición y del crecimiento de hogares, y es pequeña.

### 2.3 Método de B2

`D2030 = D2025 + F − T + B`, por provincia:
- `D2025`: déficit 2021-2025 con bajas nulas, {{B2-H2:valor}} [C4];
- F: hogares INE 2026-2030, {{B2-H3:valor}} [C2];
- T: terminadas, con tres escenarios: (a) media de 2023-2025 ({{B2-H4:valor}} en cinco años); (b) cartera con el retardo nacional de {{B2-H5:valor}}; (c) tendencia, solo como sensibilidad;
- B: bajas, de R de B1, que es un límite inferior.

El rango de cada provincia combina el mínimo y el máximo de F, la envolvente de T entre los escenarios (a) y (b) y el rango de B. El signo (mejora o empeora) se asigna solo cuando todo el rango tiene el mismo signo.

### 2.4 Resultado de B2

- Déficit nacional a fin de 2030 en el escenario (a): {{B2-H1}} [C4]. En el escenario (b), {{E-E1-B2-D2030-b:valor}}; en el (c), {{E-E1-B2-D2030-c:valor}} [C4].
- En el escenario central (a) empeoran {{E-E1-B2-empeora-a:valor}}; en el (b), {{E-E1-B2-empeora-b:valor}}; en el (c), {{E-E1-B2-empeora-c:valor}} [C4].
- Con el rango completo: empeoran {{E-E1-B2-empeora:valor}}, mejoran {{E-E1-B2-mejora:valor}} y quedan indeterminadas {{E-E1-B2-indeterminado:valor}} [C4]. El signo central coincide en los tres escenarios en {{E-E1-B2-estable3:valor}}.

![Signo del cambio del déficit 2025-2030 por provincia](B2/figuras/B2_mapa_signo.png)

**Lectura.** Es una proyección bajo supuestos, no un pronóstico. Dice qué pasaría si las terminadas siguieran al ritmo reciente y los hogares crecieran como proyecta el INE. No incorpora la reacción de la oferta ni de la formación de hogares a los precios.

---

## 3. Territorio

### 3.1 Concentración

- En 2021-2025, {{A4-conc50-2021-2025:valor}} suman la mitad del déficit positivo y {{A4-conc80-2021-2025:valor}} suman cuatro quintas partes [C4].
- En 2021-2024 las cifras son {{A4-conc50-2021-2024:valor}} y {{A4-conc80-2021-2024:valor}} [C4].
- La concentración es estable entre ventanas: el déficit es un fenómeno de pocas provincias, con las grandes áreas urbanas y el litoral mediterráneo a la cabeza.

![Concentración del déficit 2021-2025](A4/figuras/A4_concentracion_2021_2025.png)

### 3.2 Clases de A4

**Cómo se clasifica.** Cada provincia se clasifica según dos preguntas: si falta vivienda (déficit 2021-2025 positivo) y si construir es rentable con un coste de construcción oficial. El coste procede del módulo básico de construcción de 1993 (BOE) actualizado con el índice de costes de Eurostat: {{A4-001}} [C4]. En v4 el coste era supuesto; en v5 es un rango derivado de una norma.

| Clase | Definición | Provincias 2021-2025 (robustas) | Provincias 2012-2025 (robustas) |
|---|---|---|---|
| `1` | falta y es rentable | {{A4-prov-2021-2025-c1:num}} ({{A4-prov-2021-2025-c1-robustas:num}}) | {{A4-prov-2012-2025-c1:num}} ({{A4-prov-2012-2025-c1-robustas:num}}) |
| `2` | falta con freno regulatorio o de suelo: el precio supera coste y suelo con margen y la oferta no responde | {{A4-prov-2021-2025-c2:num}} ({{A4-prov-2021-2025-c2-robustas:num}}) | {{A4-prov-2012-2025-c2:num}} ({{A4-prov-2012-2025-c2-robustas:num}}) |
| `3` | falta y no es rentable con el coste oficial | {{A4-prov-2021-2025-c3:num}} ({{A4-prov-2021-2025-c3-robustas:num}}) | {{A4-prov-2012-2025-c3:num}} ({{A4-prov-2012-2025-c3-robustas:num}}) |
| `4` | no falta: déficit menor o igual que cero en la ventana | {{A4-prov-2021-2025-c4:num}} ({{A4-prov-2021-2025-c4-robustas:num}}) | {{A4-prov-2012-2025-c4:num}} ({{A4-prov-2012-2025-c4-robustas:num}}) |
| `9` | sin dato | {{A4-prov-2021-2025-c9:num}} ({{A4-prov-2021-2025-c9-robustas:num}}) | {{A4-prov-2012-2025-c9:num}} ({{A4-prov-2012-2025-c9-robustas:num}}) |

«Robustas»: la clase es la misma en todo el rango de costes, márgenes, tipos de descuento y holguras.

**Clase `4`.** Una provincia es de clase `4` cuando su déficit contable es nulo o negativo en la ventana: ha crecido más el parque que los hogares. En 2021-2025 no hay ninguna; en 2012-2025, que incluye los años de construcción de la década anterior, hay {{A4-prov-2012-2025-c4:valor}} [C4]. Que una provincia sea de clase `4` no significa que no tenga problemas de acceso: significa que, en el agregado de la ventana, el parque creció más que los hogares.

**Nota de capa.** Todas las clases son C4. El déficit provincial de 2021-2025 es C4 (regla del componente más débil) y la rentabilidad depende de un coste derivado de una sola norma y un índice, que no es un coste de mercado observado. Por eso ningún resultado por clase (en D1 y D2) se promueve.

![Provincias por clase A4](A4/figuras/A4_provincias_por_clase.png)

![Rango oficial de coste de construcción](A4/figuras/A4_rango_coste_oficial.png)

**Lectura.** Las clases ordenan el territorio según dos preguntas sencillas y transparentes, con un coste oficial en lugar de uno supuesto. Su valor está en que hacen explícito el supuesto del que depende cada recomendación condicional: la clase `2` lleva a mirar el suelo y la tramitación; la clase `3`, el coste; la clase `1`, la capacidad de producir más. Pero son exploratorias: un cambio razonable del coste puede mover una provincia de clase, y eso es lo que mide la columna de robustez.

### 3.3 Diferencias provinciales (B3): descriptivo honesto

**Pre-registro.** Antes de estimar se registraron las hipótesis, las variables, las ocho familias de factores y la corrección por comparaciones múltiples (`docs/v5/prereg_B3.md`, etiqueta `prereg-v5`). El análisis de potencia previo dio un efecto mínimo detectable con Holm de {{E-B3-EMD}} [C4], por encima del umbral que el pre-registro consideraba útil. Por eso B3 se declara de antemano **descriptivo honesto**: describe con qué se asocian las diferencias entre provincias, sin pretender identificar nada.

**Diseño.** Corte transversal de {{E-E1-B3-N:valor}} (sin Ceuta ni Melilla), variación del precio 2015-2025, ocho familias de factores a la vez, errores `HC3` y Conley, inferencia por aleatorización y Holm.

**Resultados [C4].**
- El modelo de ocho familias tiene un R² de {{B3-R2:valor}} con el valor tasado.
- `H-B3-6` (precio inicial): {{B3-H-B3-6-b}}, p ajustado {{B3-H-B3-6-p:valor}}. Las provincias que partían de precios más bajos subieron más. Con el precio inicial de Registradores, para controlar el error de medida, el coeficiente baja a {{B3-H-B3-6-b-control:valor}} y el p a {{B3-H-B3-6-p-control:valor}}: la asociación se mantiene en signo, pero parte de ella es mecánica (el error de medida del precio inicial empuja el coeficiente hacia valores negativos).
- `H-B3-1` (demanda sectorial tipo Bartik): {{B3-H-B3-1-b}}, p ajustado {{B3-H-B3-1-p:valor}}. No se distingue de cero.
- `H-B3-2` (crecimiento de la población): {{B3-H-B3-2-b}}, p ajustado {{B3-H-B3-2-p:valor}}. No se distingue de cero tras el ajuste.
- La validación cruzada dejando una provincia fuera da un RMSE de {{E-B3-rmse:valor}} frente a {{E-B3-rmse:max}} del modelo de solo media [C4].

**Desviaciones del pre-registro.** Están todas en `output/v5/B3/desviaciones.md` y son exploratorias: renta medida con el PIB per cápita provincial en lugar de la renta por hogar; ventanas más cortas en alquiler y renta; validación por exclusión de una provincia en lugar de AR(4); acotación del parámetro de Oster.

![Variación del precio por provincia](B3/figuras/mapa_P1.png)

![Reparto de Shapley del R² por familias](B3/figuras/shapley.png)

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
| Demografía | {{B4-v2-compra-2015-2019-demografica:valor}} | {{B4-v2-compra-2019-2025-demografica:valor}} | {{B4-v2-compra-2015-2025-demografica:valor}} |
| Renta y empleo | {{B4-v2-compra-2015-2019-renta_empleo:valor}} | {{B4-v2-compra-2019-2025-renta_empleo:valor}} | {{B4-v2-compra-2015-2025-renta_empleo:valor}} |
| Financiación y tipos | {{B4-v2-compra-2015-2019-financiacion_tipos:valor}} | {{B4-v2-compra-2019-2025-financiacion_tipos:valor}} | {{B4-v2-compra-2015-2025-financiacion_tipos:valor}} |
| Oferta y suelo | {{B4-v2-compra-2015-2019-oferta_suelo:valor}} | {{B4-v2-compra-2019-2025-oferta_suelo:valor}} | {{B4-v2-compra-2015-2025-oferta_suelo:valor}} |
| Residuo | {{B4-v2-compra-2015-2019-residuo:valor}} | {{B4-v2-compra-2019-2025-residuo:valor}} | {{B4-v2-compra-2015-2025-residuo:valor}} |

**Contribuciones contables al alquiler de stock (v2, IPC) [C4].**

| Familia | 2015-2019 | 2019-2025 | 2015-2025 |
|---|---|---|---|
| Demografía | {{B4-v2-alquiler_stock-2015-2019-demografica:valor}} | {{B4-v2-alquiler_stock-2019-2025-demografica:valor}} | {{B4-v2-alquiler_stock-2015-2025-demografica:valor}} |
| Renta y empleo | {{B4-v2-alquiler_stock-2015-2019-renta_empleo:valor}} | {{B4-v2-alquiler_stock-2019-2025-renta_empleo:valor}} | {{B4-v2-alquiler_stock-2015-2025-renta_empleo:valor}} |
| Financiación y tipos | {{B4-v2-alquiler_stock-2015-2019-financiacion_tipos:valor}} | {{B4-v2-alquiler_stock-2019-2025-financiacion_tipos:valor}} | {{B4-v2-alquiler_stock-2015-2025-financiacion_tipos:valor}} |
| Oferta y suelo | {{B4-v2-alquiler_stock-2015-2019-oferta_suelo:valor}} | {{B4-v2-alquiler_stock-2019-2025-oferta_suelo:valor}} | {{B4-v2-alquiler_stock-2015-2025-oferta_suelo:valor}} |
| Residuo | {{B4-v2-alquiler_stock-2015-2019-residuo:valor}} | {{B4-v2-alquiler_stock-2019-2025-residuo:valor}} | {{B4-v2-alquiler_stock-2015-2025-residuo:valor}} |

**Reparto entre provincias (B3, cuota del R²) [C4].** Oferta y suelo {{B4-b3-shapley-oferta_suelo:valor}}; demografía {{B4-b3-shapley-demografica:valor}}; turismo y no residentes {{B4-b3-shapley-turismo_no_residentes:valor}}; financiación y tipos {{B4-b3-shapley-financiacion_tipos:valor}}; renta y empleo {{B4-b3-shapley-renta_empleo:valor}}; residuo {{B4-b3-shapley-residuo:rango}}. El orden de las familias no es el mismo con valor tasado y con Registradores (correlación de Spearman {{B3-shap-spearman:valor}}).

**Cota de cantidad [C2].** Las viviendas turísticas desplazaron como máximo {{B4-v3-vut-cantidad}} en 2020-2024 [C2].

**Estabilidad.** La tau de Kendall mínima del orden de las familias entre métodos y periodos es {{B4-estabilidad-tau-min:valor}} [C4]: el orden se invierte según se mire. En las series nacionales el residuo es grande y cambia de signo entre periodos; entre provincias pesan más la oferta, la demografía y el turismo.

**Lectura.** No se puede afirmar qué familia de factores «explica» la subida. Lo que se sostiene es que las contribuciones contables no son estables: cambian con el método (series temporales frente a corte transversal), con el periodo y con la fuente de precio. Las tablas son contabilidad, no atribución.

---

## 5. Parque frente a mercado

El parque es el conjunto de viviendas existentes y sus ocupantes; el mercado son las transacciones y contratos de cada año. Una afirmación sobre uno no vale para el otro.

### 5.1 Quién posee las viviendas (R1C)

- Hogares con vivienda principal en propiedad: {{R1C-001}} [C1].
- Hogares con otras propiedades: {{R1C-002:valor}} en el tramo de sesenta y cinco a setenta y cuatro años frente a {{R1C-003:valor}} en el de menores de treinta y cinco [C4, EFF del BdE, fuente única].
- Personas jurídicas y sector público en el parque: **sin dato** público. Se ha pedido (solicitudes S1 y S3 de `docs/v5/solicitudes.md`).
- Vacías y de uso esporádico: el INE las publica para {{R1C-020}}; la mediana municipal del porcentaje de vacías es {{R1C-021}} [C4].

![Propiedad por edad y personas jurídicas](R1C/figuras/propiedad_edad_y_pj.png)

**Lectura.** La propiedad de la vivienda principal está muy extendida y es una cifra C1. La concentración de otras propiedades en los tramos de edad mayores, frente a los menores, es compatible con una transferencia de riqueza inmobiliaria por edad, pero es fuente única. Sobre la propiedad empresarial del parque no hay dato: cualquier cifra que circule sobre ese punto no procede de una estadística pública que el proyecto haya podido localizar.

### 5.2 Empresas (CB)

- Compraventas con comprador persona jurídica: {{CB-C8-01}} en 2024 [C4]. Es un flujo; no dice qué parte del parque poseen las empresas.
- Declarantes del IRPF con rendimientos de capital inmobiliario: {{CB-C6-01:valor}}; con reducción por arrendamiento de vivienda: {{CB-C6-02:valor}} [C4].
- Viviendas equivalentes arrendadas por personas físicas: {{CB-C6-03:valor}}, es decir, {{CB-C6-04:valor}} por declarante [C4].
- Frente a las viviendas principales en alquiler del Censo ({{CB-C5-05:valor}}), el residual que incluye personas jurídicas, sector público y alquiler no declarado está entre {{CB-C6-05:rango}} [C4].
- La AEAT no publica la distribución de arrendadores por número de inmuebles: no se puede contrastar cuánto alquiler está en manos de grandes tenedores.

### 5.3 No residentes (R1A)

- Peso de los compradores extranjeros no residentes: {{R1A-H1:valor}} en 2025 frente a {{R1A-H2:valor}} en 2015 [C4]. Con residentes, los compradores extranjeros son {{compradores_extranjeros:valor}} [C4].
- Entre provincias va de {{R1A-H3:rango}} [C4].
- Asociación entre el peso inicial de no residentes y la subida del precio 2015-2025: bivariada {{R1A-H4}}; con renta, población, costa e islas, {{R1A-H5}} [C4]. Con controles el coeficiente no se distingue de cero, pero el intervalo no excluye una asociación de una parte apreciable de la bivariada. No se atribuye la subida a los no residentes ni se descarta.

**Lectura.** Los no residentes son una parte pequeña de las compraventas nacionales, pero muy desigual entre provincias: en algunas del litoral y los archipiélagos pesan mucho más que en el interior. La asociación con la subida de precios es frágil a los controles. No se puede afirmar que los no residentes sean un factor principal de la subida nacional ni que sean irrelevantes en las provincias donde su peso es alto.

### 5.4 Contado (CA)

- Hipotecas sobre vivienda por cada cien compraventas: {{CA-CT-ratio-ine:valor}} en 2025 (INE) [C4]. Con Registradores, en 2022-2025, la razón coincide: {{CA-CT-ratio-triang-2022:rango}} en 2022, {{CA-CT-ratio-triang-2023:rango}} en 2023, {{CA-CT-ratio-triang-2024:rango}} en 2024 y {{CA-CT-ratio-triang-2025:rango}} en 2025 [C4].
- Si todas las hipotecas fuesen de compra, el contado sería como mínimo {{CA-CT-contado-cota:valor}} de las compraventas [C4]. La cota solo es informativa si la fracción de hipotecas de compra supera {{CA-CT-phi-critico:valor}}.
- Crédito a construcción y actividades inmobiliarias: de {{CA-CR-saldo-pico:valor}} en 2008 a {{CA-CR-saldo-2025:valor}} en 2025, una caída de {{CA-CR-saldo-caida:valor}} [C4]. Es un saldo, no nuevas operaciones.

![Hipotecas por compraventa](CA/figuras/contado_ratio.png)

**Lectura.** Hay un volumen grande de compras sin hipoteca, cuya magnitud exacta depende de qué fracción de las hipotecas financia compras de vivienda. Es compatible con compras de inversores y de hogares con ahorro acumulado o con ayuda familiar, pero los datos no separan a unos de otros. El crédito a promotores es una fracción del de la década anterior, lo que es compatible con una financiación de la construcción más restringida, sin que se pueda separar la oferta de crédito de la demanda.

### 5.5 Seguridad jurídica (CB)

- Lanzamientos por la LAU (principalmente impago de alquiler): {{CB-C5-01:valor}} en 2025, frente a un máximo de {{CB-C5-02:valor}} en 2013-2025 [C4].
- Hechos conocidos de allanamiento o usurpación: {{CB-C5-03:valor}} en 2025; procedimientos verbales posesorios por ocupación ingresados: {{CB-C5-04:valor}} [C4].
- Frente a {{CB-C5-05:num}} viviendas principales en alquiler, los órdenes de magnitud son pequeños. Con los datos públicos no se puede contrastar si la percepción de inseguridad reduce la oferta de alquiler: la correlación entre comunidades no es un diseño que lo permita.

### 5.6 Fiscalidad (CB)

- La reducción por arrendamiento de vivienda se aplica a {{CB-C6-02:valor}} [C4].
- No hay en el repositorio una evaluación de la incidencia de los cambios fiscales en la oferta de alquiler. La matriz D1 los deja como «no evaluable» (instrumento `I15`).

### 5.7 Desigualdad (CC)

| Grupo | Sobrecarga de coste de vivienda, 2025 | 2015 | Capa |
|---|---|---|---|
| Primer quintil de renta | {{CC-C7a-qu-QU1:valor}} | {{CC-C7a-qu-QU1:max}} | C4 |
| Quinto quintil de renta | {{CC-C7a-qu-QU5:valor}} | — | C4 |
| Inquilinos a precio de mercado | {{CC-C7a-ten-RENT_MKT:valor}} | {{CC-C7a-ten-RENT_MKT:max}} | C4 |
| Propietarios con hipoteca | {{CC-C7a-ten-OWN_L:valor}} | {{CC-C7a-ten-OWN_L:max}} | C4 |

- Los inquilinos a precio de mercado situados en los tres primeros deciles de renta son {{CC-C7b-alq-d123:valor}} [C4].
- Hogares jóvenes (de dieciséis a veintinueve años) en propiedad: {{CC-C7b-jov-prop:valor}} en 2025 frente a {{CC-C7b-jov-prop:min}} en 2015; en vivienda cedida, {{CC-C7b-jov-cesion:valor}} frente a {{CC-C7b-jov-cesion:min}} [C4]. En propiedad sin hipoteca, {{CC-C7b-jov-sinhip:valor}}, que se usa solo como aproximación a la ayuda familiar, no como medida [C4].
- La sobrecarga ha bajado desde 2015 en todos los grupos [C4]. Eurostat-SILC es la ECV del INE: no hay segunda fuente y la cifra es C4.

**Lectura.** La sobrecarga de coste es mucho mayor entre los hogares de renta baja y los inquilinos a precio de mercado que entre los propietarios. Su descenso desde 2015 coincide con el aumento del empleo y de la renta, y con una caída de la proporción de propietarios con hipoteca; no se atribuye a ninguna medida. Los hogares jóvenes en propiedad son menos que en 2015.

### 5.8 Vivienda protegida (CC)

- Calificaciones definitivas de vivienda protegida: {{CC-C2-nuevas5a}} de media en 2021-2025 [C4].
- Viviendas protegidas que saldrían del régimen en 2026-2035: {{CC-C2-salidas-base:valor}} en el escenario base, entre {{CC-C2-salidas-bajo:valor}} y {{CC-C2-salidas-alto:valor}} [C4]. Los plazos de algunos planes no constan en los reales decretos y se suponen.
- Las salidas anuales serían {{CC-C2-ratio}} veces las calificaciones nuevas [C4]. Con un régimen permanente, la cota inferior lógica sería cero.

**Lectura.** Por cada vivienda protegida que se califica, en la próxima década saldrán del régimen varias, según los plazos de los planes antiguos. El parque protegido puede reducirse aunque se mantenga el ritmo de calificaciones, salvo que los plazos se prolonguen o se califiquen más viviendas. Es una contabilidad con supuestos de plazo, no una previsión.

---

## 6. Matriz de instrumentos (D1), resumida

La matriz completa está en [output/v5/D1/matriz_instrumentos.md](D1/matriz_instrumentos.md). Aquí se resume.

**Rúbrica.** La misma para cada instrumento: evidencia y capa, magnitud y rango, signo, plazo, coste fiscal, riesgos, distribución, clase de A4 donde funcionaría y documentos que lo proponen. Se evalúan {{D1-H01:valor}}; en {{D1-H02:valor}} el signo es «no evaluable» por falta de literatura verificada o de simulación propia [C4]. «No evaluable: motivo» sustituye a cualquier opinión.

**Traslado de las ayudas a la demanda al precio, por clase [C4].** Parte de una ayuda general que captan vendedores o arrendadores, con la rejilla de elasticidades de demanda de v3:

| Clase A4 | Método A (respuesta de oferta de A4) | Método B (rejilla de oferta de v3) |
|---|---|---|
| `1` | {{D1-H11}} | {{E-E1-D1-incB-1}} |
| `2` | {{D1-H12}} | {{E-E1-D1-incB-2:valor}} |
| `3` | {{D1-H13}} | {{E-E1-D1-incB-3}} |

Los dos métodos discrepan en la clase `1` y se dan ambos.

**Resumen por grupos de instrumentos.**
- **Con signo estable en la rejilla de v3 [C2 en el signo, C4 en la magnitud].** Más construcción donde falta (`P1`) y movilización de vivienda vacía (`I10`, `I27`, `N7`).
- **Con literatura verificada de otros países.** Edificabilidad (`N2`: Büchler y Lutz, 2024; Greenaway-McGrevy y Phillips, 2023) y licencias (`N1`, `I13`: Ball, 2011, solo asociación). Sin evaluación en España.
- **Regulación de precios del alquiler (`I01`).** El resultado propio de v3 (`H3-3`) queda fuera de C3 por la contaminación de la validación; la réplica de García-López y otros no se reproduce con los datos de stock (sección de limitaciones). La literatura verificada da resultados de distinto signo según la oferta. Signo no estable.
- **Ayudas a la demanda (`I06`-`I09`, `N9`).** Su traslado al precio depende de la respuesta de la oferta: alto donde la oferta no responde.
- **Parque público (`I02`).** Signo menor o igual que cero en la rejilla (posiblemente nulo) si desplaza construcción privada.
- **No evaluables.** Rehabilitación, industrialización, seguridad jurídica, fiscalidad de arrendadores, entre otros: sin literatura verificada con magnitud ni simulación propia.

**Cómo leer la matriz.** Cada fila indica qué se sabe del instrumento, con qué capa y de dónde procede la evidencia. Una celda «no evaluable» no es una valoración negativa del instrumento: significa que el proyecto no ha encontrado literatura verificada con magnitud ni ha podido simularlo. Los documentos programáticos que proponen cada instrumento se cuentan con un diccionario de palabras clave cuya precisión estricta es {{A5-H04:valor}} [C4]: son cotas de coincidencias, no recuentos de medidas validadas.

**Lectura.** Con la evidencia disponible, lo que tiene signo estable es aumentar la oferta donde falta y movilizar vacías. Lo que más depende del territorio es el traslado de las ayudas a la demanda: donde la oferta no responde, la mayor parte de una ayuda general acabaría en el precio. Esto no es una recomendación sobre un instrumento concreto: es una condición que cualquier diseño tendría que tener en cuenta.

---

## 7. Política por territorio (D2), en lenguaje condicional

D2 cruza la necesidad de B1, la clase de A4 y la matriz de D1. Todo es C4: no hay efectos estimados por clase en España. El texto completo está en [output/v5/D2/politica_territorio.md](D2/politica_territorio.md).

**Clase `1` ({{E-E1-D2-nprov-1:valor}}, {{E-E1-D2-nrob-1:num}} robustas).**
- Necesidad: {{D2-H01}} [C4].
- Si el objetivo fuese cubrir esa necesidad, los instrumentos con signo estable serían más construcción y movilización de vacías.
- La construcción adicional de la rejilla de v3, repartida por cuota de necesidad, cubriría {{E-E1-D2-cobpd-1:rango}} de la necesidad; las vacías movilizables, {{E-E1-D2-vac-1}}, el {{E-E1-D2-covvac-1:valor}} en el central [C4].
- Una ayuda general a la demanda sin más oferta se trasladaría al precio en {{D1-H11:rango}} (método A) [C4].

**Clase `2` ({{E-E1-D2-nprov-2:valor}}, {{E-E1-D2-nrob-2:num}} robustas).**
- Necesidad: {{D2-H02}} [C4].
- La clase se define porque la oferta no responde: si el cuello de botella es de suelo o de tramitación, los instrumentos que actúan sobre él (edificabilidad, licencias) serían los aplicables según la literatura verificada de otros países.
- Construcción adicional: {{E-E1-D2-cobpd-2:rango}} de la necesidad; vacías: {{E-E1-D2-vac-2}}, el {{E-E1-D2-covvac-2:valor}} en el central [C4].
- Una ayuda general a la demanda se trasladaría al precio en {{D1-H12:rango}} [C4].

**Clase `3`.** Necesidad: {{D2-H03}} [C4]. Si construir no es rentable con el coste oficial, los instrumentos de oferta privada tendrían poco recorrido sin cambios en coste o suelo.

**Clase `9`.** Necesidad: {{D2-H09}} [C4]. Sin clase: no evaluable.

**Lectura.** Las combinaciones son condicionales: «si el objetivo es X y la provincia está en la clase Y, los instrumentos con signo estable son Z». No son recomendaciones con efecto estimado.

---

## 8. Módulo València

### 8.1 Necesidad y clase

- Déficit contable 2021-2025 de la provincia de València: {{E-E1-VLC-def2125}} [C4]; de la ciudad, {{E-E1-VLC-defciu:valor}} (fuente única) [C4].
- Necesidad anual 2026-2035 de la provincia: {{E-E1-VLC-B1}} [C4].
- Déficit acumulado a fin de 2030 en la provincia: {{E-E1-VLC-B2}} [C4]; empeora en todo el rango.
- Clase A4 de la provincia: `1` (falta y es rentable) [C4]. La ciudad pasa de la clase `2` de v4 (coste supuesto, estabilidad {{E-E1-VLC-estab-v4:valor}}) a la clase `1` en v5 con el rango oficial de coste [C4]: el cambio de clase procede del cambio de coste, no de un cambio en el mercado.
- Valor tasado de la vivienda libre en la ciudad: {{E-E1-VLC-precio:valor}} [C4].

### 8.2 Alquiler por distritos (SERPAVI con nombres)

Los distritos censales de SERPAVI se cruzan con los {{E-E1-VLC-ndist:valor}} municipales (supuesto declarado: coinciden uno a uno; `output/v5/R1T`). En 2024 hay {{E-E1-VLC-contratos:valor}} contratos con renta declarada [C4].

| Indicador | Valor | Distrito | Capa |
|---|---|---|---|
| Renta mediana más alta, 2024 | {{E-E1-VLC-serpavi-max:valor}} | {{E-E1-VLC-serpavi-max:cobertura}} | C4 |
| Renta mediana más baja, 2024 | {{E-E1-VLC-serpavi-min:valor}} | {{E-E1-VLC-serpavi-min:cobertura}} | C4 |
| Mediana entre distritos, 2024 | {{E-E1-VLC-serpavi-med:valor}} | — | C4 |
| Mayor crecimiento 2015-2024 | {{E-E1-VLC-crec-max:valor}} | {{E-E1-VLC-crec-max:cobertura}} | C4 |
| Menor crecimiento 2015-2024 | {{E-E1-VLC-crec-min:valor}} | {{E-E1-VLC-crec-min:cobertura}} | C4 |
| Mediana del crecimiento entre distritos | {{E-E1-VLC-crec-med}} | — | C4 |

La tabla completa por distrito, con nombre, renta mediana de 2015 y 2024, contratos y posición, está en `output/v5/R1T/serpavi_distritos_valencia_nombres.csv`. El centro histórico encabeza a la vez el nivel y el crecimiento; los poblados periféricos tienen pocas observaciones y su crecimiento es menos preciso.

### 8.3 Viviendas turísticas: INE frente a GVA (R1A)

- El registro de la GVA (stock) cuenta {{R1A-H6}} veces las viviendas turísticas que estima el INE en las tres provincias valencianas, 2020-2024 [C4].
- Con el registro vigente de la GVA de octubre de 2026 frente al INE de mayo de 2026, la razón es {{R1A-H7}} [C4].
- La suma de secciones del INE cubre {{R1A-H8:valor}} del total provincial [C4].
- La diferencia se descompone en cotas por factor (fechas de baja, definiciones, cobertura); el residual no tiene cota inferior (`BK-052`).

### 8.4 Fianzas de la GVA (A23)

- Mediana de la fianza depositada: {{E-E1-VLC-fianza-2020:valor}} en 2020 y {{E-E1-VLC-fianza-2025:valor}} en 2025 [C4], con {{E-E1-VLC-fianza-n2025:valor}} fianzas en 2025.
- La renta de contratos nuevos (mediana de la fianza) sube {{A23-A5:valor}} en 2020-2025 [C4]; con el IPVA de nuevo contrato, el rango 2021-2024 de la Comunitat Valenciana es {{A23-A10}} [C1].
- Rotación (fianzas sobre contratos vigentes): {{A23-A12}} [C4].
- Municipios con mediana de fianza que se duplica: {{A23-A14:valor}} [C4].
- Las fianzas no traen la duración del contrato: el alquiler de temporada y por habitaciones sigue sin fuente (`BK-014`).

### 8.5 Heredado de v4

Se mantiene la lectura del módulo València de v4 (`output/v4/informe_tecnico.md`):
- [C4] la provincia de València está entre las tres primeras en déficit contable 2021-2025;
- el componente de nacionalidad extranjera pesa más en la variación de hogares de la provincia que en el conjunto nacional [C4];
- las viviendas turísticas de la ciudad están en 2026 por debajo del nivel de 2021 en la comparación del mismo mes (INE, oleadas experimentales) [C4].

---

## 9. Convergencia con BdE, Ministerio, INE, OCDE y Eurostat (D3)

**Regla.** Una cifra «coincide» o «difiere» solo si concepto, periodo y cobertura son comparables; coincide si los rangos se solapan o si la diferencia entre puntos medios no supera la tolerancia declarada. «Comparable en parte» (otro periodo, concepto o cobertura) no cuenta como coincidencia ni como diferencia. «Control de la misma fuente» es una cifra del organismo con la misma fuente primaria que el proyecto: confirma la transcripción y no cuenta. «No comparable» si el concepto lo impide o la cifra no se localizó. Las diferencias se describen por concepto, periodo, cobertura, método o bajas. No se valora a ningún organismo.

**Resultado [C4].** Coinciden {{D3-coincide:num}}; difieren {{D3-difiere:num}}; son comparables en parte {{D3-comparable_en_parte:num}}; son controles de la misma fuente {{D3-control_misma_fuente:num}}; no son comparables {{D3-no_comparable:num}}.

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

La tabla completa, con documento y página de cada organismo, está en [output/v5/D3/convergencia.md](D3/convergencia.md).

**Lectura.** La única diferencia en sentido estricto es la del precio, y se explica por el puente entre el índice del INE y el núcleo de tres fuentes. Las coincidencias en el déficit 2021-2025 comparten insumos con el proyecto; las de Eurostat en sobrecarga, emancipación, precio y alquiler comparten fuente primaria: confirman la transcripción, no la cifra.

**Por qué difieren las cifras de déficit.** La diferencia con las intervenciones del Banco de España sobre el déficit no es de método sino de definición: el organismo mide la creación neta de hogares menos la producción en ventanas que empiezan en 2022, mientras que el proyecto empieza en 2021, el primer año con la corrección de la ruptura de la EPA. Con la ventana 2021-2025 y bajas nulas, el proyecto coincide con las cifras del Informe Anual y del Informe de Estabilidad Financiera. Que coincidan no eleva la capa: el componente de 2025 sigue siendo de fuente única.

**Lo que no se ha podido comparar.** La necesidad a diez años y el déficit a 2030 no tienen una cifra publicada localizable con el mismo concepto. Cuando aparezca, la comparación se añadirá con la misma regla.

---

## 10. Limitaciones y lo que no se puede afirmar

### 10.1 Lo que no se puede afirmar

- **Que una familia de factores «explique» la subida de precios.** Las contribuciones contables no son estables entre métodos ni periodos [C4].
- **Que los grandes tenedores o los fondos determinen los precios.** No hay datos públicos del parque por tipo de propietario. El verificador lo deja en «no analizada: faltan datos».
- **Que los topes al alquiler bajen o suban las rentas en España.** El resultado de v3 está fuera de C3 por contaminación de la validación; la réplica de García-López y otros no se reproduce (coeficiente propio {{E-GL-coef}}, p ajustado {{E-GL-pholm:valor}}) porque el stock de SERPAVI recoge solo {{E-GL-lambda:valor}} de la variación del flujo [C4].
- **Que las viviendas turísticas suban el alquiler nacional.** La asociación de v3 no se distingue de cero ({{E-v3-H3-1}}, p ajustado {{E-v3-H3-1-p:valor}}); la cota de cantidad es {{B4-v3-vut-cantidad:valor}} [C2].
- **Que haya una burbuja.** Las pruebas de exuberancia (GSADF) con tamaño corregido detectan episodios en algunas razones de precio y no en otras; una exuberancia estadística no es una burbuja (sección de robustez del working paper).
- **Que el pre-registro de B3 confirme una hipótesis.** Su potencia era insuficiente; el resultado es descriptivo.

### 10.2 Verificador de afirmaciones

Se evalúan {{E-E1-ver-n:valor}} del debate público: {{E-E1-ver-anc:valor}} quedan «analizada, no concluyente», {{E-E1-ver-parc:valor}} «parcialmente», {{E-E1-ver-nafd:valor}} «no analizada: faltan datos» y {{E-E1-ver-contr:valor}} «contradicha» [C4]. Detalle en [output/v5/verificador/verificador.md](verificador/verificador.md).

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

## Anexo A. Datos y fuentes

| Bloque | Fuentes | Ruta |
|---|---|---|
| Hogares | INE ECP, EPA (corregida por la ruptura de 2021), proyecciones de hogares | `output/v5/B1`, `output/v5/B2` |
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

- `make all` reconstruye todo sin red; las descargas están en los scripts `*_fetch.py`, fuera de `make all`.
- `make check` ejecuta `src/v5/check_v5.py` (cifras fuera de marcador, sumas provinciales iguales al total nacional, capas válidas) y `src/v3/check_texto.py` (léxico valorativo o partidista y lenguaje causal por debajo de C3).
- Este informe se genera con `python3 src/v5/render.py` desde `docs/v5/plantillas/informe_tecnico.md`.
- Toda especificación probada está en los `registro.csv` de cada módulo; la muestra sellada solo se usa vía `src/holdout.py`.
- Semilla: `SEED=20261010` en todo lo aleatorio.

## Declaración de independencia y uso de inteligencia artificial

Este informe es un trabajo individual e independiente de Borja Romero, economista, sin financiación externa ni vínculo con partidos políticos. Evalúa afirmaciones e instrumentos, nunca partidos ni personas. El análisis, el código y los borradores se elaboraron con agentes de inteligencia artificial (Claude), bajo la supervisión del autor, que revisa y asume la responsabilidad del contenido. El detalle está en el apéndice C del working paper y en README_REPLICACION.md. Las correcciones se publican en ERRATA.md.
