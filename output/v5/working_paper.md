# Necesidad de vivienda, territorio y precios en España: hechos, cotas y exploración con datos públicos y una escala de evidencia

*Borja Romero, economista (independiente). Documento de trabajo, versión `5.0`, 10 de octubre de 2026. DOI: pendiente.*

*Proyecto reproducible: `make all` sin red; todas las cifras proceden de `output/v5/cifras_clave.csv`.*

## Resumen

Este trabajo mide la necesidad de vivienda en España y su distribución territorial con registros públicos y clasifica cada resultado en una escala de evidencia: hechos con dos fuentes independientes, cotas con supuestos explícitos y resultados exploratorios. Entre 2021 y 2024 los hogares crecieron entre 562.692-688.692 viviendas más que las viviendas terminadas [C1]. El precio de compra subió 47,2 % en 2015-2025 según tres registros, frente a 79,9 % del índice oficial; un puente contable reconcilia ambas medidas salvo un residuo de método. Una contabilidad stock-flujo provincial da una necesidad de 214.868 viviendas/año en 2026-2035 [C4]; al ritmo actual de terminadas, el déficit alcanzaría 1.296.670 viviendas a fin de 2030 [C4]. El déficit se concentra en pocas provincias, y una clasificación con un coste de construcción oficial separa dónde falta vivienda y es rentable construir de dónde la oferta no responde. Un análisis pre-registrado de las diferencias provinciales de precios resulta descriptivo por falta de potencia, y las contribuciones contables de los factores a la subida no son estables entre métodos ni periodos. Ningún resultado nuevo alcanza la capa de efectos identificados.

## Abstract

This paper measures housing need in Spain and its territorial distribution using public records, and classifies every result on an evidence scale: facts confirmed by two independent sources, bounds under explicit assumptions, and exploratory results. Between 2021 and 2024 households grew by 562.692-688.692 viviendas more than completed dwellings [C1]. Purchase prices rose by 47,2 % over 2015-2025 according to three administrative registers, against 79,9 % in the official index; an accounting bridge reconciles both measures up to a methodological residual. A provincial stock-flow accounting yields a need of 214.868 viviendas/año in 2026-2035 [C4]; at the current pace of completions, the shortfall would reach 1.296.670 viviendas by the end of 2030 [C4]. The shortfall is concentrated in a few provinces, and a classification based on an official construction cost separates places where housing is lacking and building is profitable from places where supply does not respond. A pre-registered analysis of provincial price differences turns out to be descriptive for lack of power, and the accounting contributions of the factors behind the price increase are not stable across methods or periods. No new result reaches the layer of identified effects.

**Palabras clave:** vivienda; déficit de vivienda; necesidad de vivienda; precios de la vivienda; alquiler; identificación parcial; pre-registro; España.

**Keywords:** housing; housing shortage; housing need; house prices; rents; partial identification; pre-registration; Spain.

**JEL:** R21, R31, R38, C21, C81.

---

## 1. Introducción

**Pregunta.** ¿Qué se puede afirmar, y con qué grado de seguridad, sobre cuántas viviendas faltan en España, dónde faltan, cuánto han subido los precios y alquileres, qué factores se asocian con la subida y qué instrumentos tienen evidencia a favor en cada territorio?

**Motivación.** El debate público sobre la vivienda en España mezcla cifras de déficit que difieren por definición, índices de precios que miden cosas distintas y afirmaciones causales sin diseño que las sostenga. Una misma pregunta («¿cuánto ha subido la vivienda?») tiene respuestas que van de la mitad a cuatro quintas partes según el índice, y una misma cifra de déficit cambia según la ventana y la fuente de hogares. Este trabajo no añade una estimación más: ordena lo que los datos públicos permiten afirmar y con qué capa de evidencia.

**Contribución.**
1. **Una escala de evidencia aplicada de forma uniforme.** Cuatro capas: C1 hechos (al menos dos fuentes independientes, con todos los componentes en C1), C2 cotas de identificación parcial con supuestos explícitos (Manski, 2003), C3 efectos (pretendencias, placebos, sensibilidad y muestra sellada) y C4 exploratorio. La capa de una cifra es la menor de sus componentes. En esta versión ningún resultado nuevo alcanza C3.
2. **Una contabilidad de necesidad a diez años por provincia y una proyección del déficit a 2030**, con rango por componente y capa por componente, que hace explícito de qué supuesto depende cada cifra.
3. **Un puente contable entre el índice de precios oficial y el núcleo de tres registros**, y la separación del alquiler de stock y de contratos nuevos con dos fuentes por territorio.
4. **Una clasificación territorial con un coste de construcción oficial**, que sustituye al coste supuesto de versiones anteriores, y un análisis pre-registrado de las diferencias provinciales cuya potencia se declara antes de estimar.
5. **Una matriz de instrumentos con rúbrica común y una comparación sistemática con las cifras de los organismos públicos.**

**Frente a la literatura.**
- La literatura sobre la respuesta de la oferta y la regulación del suelo (Saiz, 2010; Glaeser y Gyourko, 2018; Hilber y Vermeulen, 2016) relaciona la elasticidad de la oferta con la transmisión de la demanda al precio. Este trabajo usa esa intuición para clasificar provincias, pero no estima elasticidades causales: la clasificación es exploratoria.
- Sobre la regulación del alquiler, Diamond, McQuade y Qian (2019) documentan una reducción de la oferta de alquiler en San Francisco, y Jofre-Monseny, Martínez-Mazza y Segú (2023) una reducción de rentas en Cataluña. Con los datos abiertos del proyecto no se replica García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020) sobre viviendas turísticas, y se documenta por qué (stock frente a flujo).
- Sobre la incidencia de las ayudas a la demanda, Gibbons y Manning (2006), Eriksen y Ross (2015), Hilber y Turner (2014) y Carozzi, Hilber y Yu (2024) muestran que el traslado al precio depende de la rigidez de la oferta. La matriz de instrumentos traduce esa condición a las clases territoriales.
- Sobre edificabilidad y licencias, Büchler y Lutz (2024) y Greenaway-McGrevy y Phillips (2023) evalúan cambios de zonificación con diseños de diferencias; Ball (2011) documenta retrasos de tramitación. No hay evaluación comparable en España.
- Metodológicamente, el trabajo combina identificación parcial (Manski, 2003), sensibilidad a variables omitidas (Oster, 2019; Cinelli y Hazlett, 2020), pretendencias robustas (Rambachan y Roth, 2023) y pre-registro con corrección por comparaciones múltiples.

**Estructura.** La sección de datos describe las fuentes y la regla de dos fuentes. La de métodos presenta las capas y los procedimientos de cada una. Los resultados se ordenan en necesidad, territorio, precios y contribuciones. Siguen la robustez, la discusión y las conclusiones.

---

## 2. Datos

**Fuentes.** Todas son públicas y se descargan con scripts separados de la reconstrucción (`make all` funciona sin red):
- **Hogares:** INE, Encuesta Continua de Población (ECP) y EPA corregida por la ruptura metodológica de 2021; proyecciones de hogares del INE para 2026-2035.
- **Producción de vivienda:** Ministerio de Vivienda (certificados de fin de obra, iniciadas, calificaciones de vivienda protegida) y Catastro (altas de inmuebles).
- **Precio de compra:** INE (IPV), Ministerio (valor tasado), Notariado (Consejo General) y Registradores (datos abiertos).
- **Alquiler:** INE (IPC de alquiler e IPVA de la AEAT), SERPAVI del Ministerio, Incasòl (Cataluña) y registro de fianzas de la GVA (Comunitat Valenciana).
- **Coste de construcción:** módulo básico de construcción (BOE) actualizado con el índice de costes de Eurostat.
- **Parque y propiedad:** Censo 2021, ECV, EFF del Banco de España y estadísticas del IRPF de la AEAT.
- **Europa:** Eurostat (índice de precios, IPCA, SILC, permisos, demografía).
- **Organismos (para la convergencia):** Banco de España, Ministerio, INE, OCDE y Eurostat.

**Regla de dos fuentes.** Una cifra es C1 si dos fuentes independientes coinciden dentro de una tolerancia declarada. Eurostat toma el dato de España del INE y la ECV es la fuente de Eurostat-SILC: en esos casos no hay independencia y la cifra queda en C4.

**Unidad territorial.** 52 provincias (cincuenta provincias y dos ciudades autónomas) en la contabilidad de necesidad; 50 provincias en el análisis transversal de precios (sin Ceuta ni Melilla). La suma provincial coincide con el total nacional en todas las tablas (comprobación automática).

**Muestra sellada.** Una parte de las series de v2 y v3 está sellada para evaluación confirmatoria y solo se accede a ella mediante un registro de accesos (`src/holdout.py`); cada hipótesis confirmatoria se evalúa una vez.

---

## 3. Métodos por capas

### 3.1 C1: hechos

Para cada cifra C1 se calculan los dos valores y se publica el rango. El déficit 2021-2024 es el aumento de hogares (ECP y EPA corregida) menos las terminadas (Ministerio y Catastro). El núcleo de precio es la banda entre Ministerio, Notariado y Registradores con pesos comunes. El alquiler de stock es la banda entre el IPC y el IPVA de contratos existentes.

### 3.2 C2: cotas

Se usan cotas de identificación parcial cuando un supuesto no se puede contrastar: bajas del parque en un rango, demanda latente frente a una tasa de convivencia de referencia, crecimiento de hogares del INE como escenario, desplazamiento máximo del stock de alquiler por viviendas turísticas. La cota se escribe con su supuesto.

### 3.3 C4: contabilidades, proyecciones y asociaciones

- **Necesidad (B1).** `N = A + R + V + F − M − K` por provincia: atraso, reposición, vacancia friccional, crecimiento de hogares, vacías movilizables y cartera en construcción. Cada componente tiene un rango; el total toma la menor capa.
- **Proyección (B2).** `D2030 = D2025 + F − T + B`, con tres escenarios de terminadas. El signo provincial se asigna solo si todo el rango coincide.
- **Clasificación (A4).** Falta o no falta (déficit 2021-2025) y rentabilidad con el coste oficial; estabilidad en una rejilla de costes, márgenes, tipos y holguras.
- **Diferencias provinciales (B3).** Mínimos cuadrados con las ocho familias de factores a la vez, errores `HC3` y Conley, inferencia por aleatorización de Freedman-Lane y Holm sobre las familias. Pre-registro con análisis de potencia previo.
- **Contribuciones (B4).** Triangulación de salidas de v2 (series temporales nacionales), B3 (reparto de Shapley entre provincias) y v3 (cotas). Estabilidad con la tau de Kendall.
- **Puente de precios (A23).** Variación acumulada en logaritmos con pesos comunes, sensibilidad a pesos y desfases, factor común de las fuentes.

### 3.4 Control de falsos descubrimientos y validación

Toda especificación probada se registra (`registro.csv` de cada módulo). Las familias de contrastes se corrigen con Holm (confirmatorias) o Benjamini-Hochberg (exploratorias). Los modelos de series se comparan en la misma muestra con un AR(4) y con el ECM de v1, con validación temporal en bloques con embargo; en el corte transversal se usa validación dejando una provincia fuera frente al modelo de solo media.

---

## 4. Resultados

### 4.1 Necesidad

**Déficit pasado.** El déficit 2021-2024 está entre 562.692-688.692 viviendas [C1]; con bajas del parque, entre 562.692-902.808 viviendas [C2]. El de 2021-2025, con bajas nulas, es 700.934 viviendas [C4]. Los hogares crecieron 997.586 hogares en 2021-2025 [C1] y se terminaron 72.264-94.426 viviendas/año en 2019-2024 [C1]. La demanda latente por convivencia con los padres está entre 188.000-506.000 hogares [C2].

**Necesidad futura.** La necesidad media anual en 2026-2035 es 214.868 viviendas/año (93.628-309.921 viviendas/año) [C4]. Sus componentes a diez años:

| Componente | Central (rango) | Capa |
|---|---|---|
| Atraso | 1.103.170 viviendas (stock) (830.963-1.473.640 viviendas (stock)) | C4 |
| Reposición | 89.665 viviendas (1.070-178.259 viviendas) | C4 |
| Vacancia friccional | 58.674 viviendas (0-117.348 viviendas) | C4 |
| Hogares (INE) | 1.720.540 hogares (1.308.530-1.772.410 hogares) | C2 |
| Vacías movilizables (resta) | 733.553 viviendas (366.777-1.100.330 viviendas) | C4 |
| Cartera en construcción (resta) | 89.815 viviendas (75.674-103.956 viviendas) | C4 |

**Déficit a 2030.** Con terminadas al ritmo de 2023-2025, el déficit llegaría a 1.296.670 viviendas (872.529-1.447.950 viviendas) [C4]; con el escenario de cartera, a 1.136.180 viviendas [C4]. En el rango completo empeoran 20 provincias, mejoran 5 provincias y quedan indeterminadas 27 provincias [C4].

![Necesidad anual por provincia](B1/figuras/B1_mapa_necesidad.png)

### 4.2 Territorio

**Concentración.** 6 provincias suman la mitad del déficit positivo de 2021-2025 y 18 provincias cuatro quintas partes [C4].

**Clases.** Con el coste oficial (677,0 EUR/m2 construido (422,0-932,0 EUR/m2 construido)), en 2021-2025 hay 37 provincias en la clase `1` (falta y es rentable), 11 provincias en la clase `2` (falta y la oferta no responde pese a que el precio supera coste y suelo), 2 provincias en la clase `3` (falta y no es rentable) y 0 provincias en la clase `4` (no falta) [C4]. En 2012-2025 la clase `4` reúne 20 provincias [C4]. Todas las clases son C4.

**Diferencias provinciales (B3).** El modelo de ocho familias alcanza un R² de 0,91 proporción [C4]. La única asociación que sobrevive a Holm es la del precio inicial (`H-B3-6`): -16,0 puntos logarítmicos (≈ %) por DT (-23,8--8,2 puntos logarítmicos (≈ %) por DT), p ajustado 0,00 probabilidad; con el precio inicial de otra fuente, -9,0 puntos logarítmicos (≈ %) por DT y p 0,06 probabilidad [C4]. La demanda sectorial (`H-B3-1`, 2,4 puntos logarítmicos (≈ %) por DT, p ajustado 0,33 probabilidad) y el crecimiento de la población (`H-B3-2`, 3,5 puntos logarítmicos (≈ %) por DT, p ajustado 0,41 probabilidad) no se distinguen de cero [C4].

![Variación del precio por provincia](B3/figuras/mapa_P1.png)

### 4.3 Precios

**Compra.** Núcleo de tres registros: 47,2 % (44,2-56,1 %) en 2015-2025 [C1]. IPV del INE: 79,9 % [C4]. Las cuatro fuentes comparten un factor común que recoge 89,2 % de la varianza de las variaciones anuales [C4]. La reponderación geográfica no reduce la diferencia: con pesos provinciales, Registradores sube 66,8 % [C4]. Queda un residuo no identificado de -30,9 pp [C4].

**Alquiler.** Stock de contratos: 10,9-22,9 % en 2015-2024 [C1]. Contratos nuevos con dos fuentes: Cataluña 16,9 % (16,6-17,2 %) y Comunitat Valenciana 26,6 % (22,4-30,8 %) en 2021-2024 [C1]. En 2024 los contratos nuevos están 13,6 % por encima de los existentes [C4].

**Europa.** El precio real de la vivienda en España creció 42,6 % acumulado desde 2015 y el alquiler real del IPCA -10,3 % acumulado desde 2015 [C4]; la tasa de sobrecarga de coste varió -3,1 puntos desde 2015 [C4].

![Puente de precio](A23/fig1_puente_precio.png)

### 4.4 Contribuciones

Las contribuciones contables al precio de compra en 2015-2025 (v2) son: demografía -7,0 pp de Δln acumulado, renta y empleo 1,1 pp de Δln acumulado, financiación 1,1 pp de Δln acumulado, oferta 0,09 pp de Δln acumulado y residuo 3,6 pp de Δln acumulado [C4]. Entre provincias (B3), el reparto del R² da oferta y suelo 25,9 % del R2, demografía 23,6 % del R2, turismo y no residentes 18,4 % del R2, financiación 11,3 % del R2 y renta 9,8 % del R2 [C4]. La tau de Kendall mínima del orden de las familias es -0,71 tau (4 familias) [C4]: las contribuciones no son estables. Las viviendas turísticas desplazaron como máximo 2,7 % del stock de alquiler [C2].

---

## 5. Robustez

### 5.1 Multiverso

- **B3.** 32 especificaciones por hipótesis confirmatoria. El signo de la principal se mantiene en 100,0 % de las especificaciones para `H-B3-6`, en 100,0 % para `H-B3-2` y en 62,5 % para `H-B3-1` [C4]. La proporción de especificaciones con p nominal por debajo del umbral convencional es 46,9 %, 59,4 % y 3,1 %, respectivamente.
- **Diseños de v2 (`R1B`).** En la forma reducida del alquiler sobre el instrumento (BI), la proporción de especificaciones con el mismo signo que la base es 0,96 proporción (min = significativas tras Holm; max = significativas nominales) [C4]. En el diseño de control sintético (BP H5), 0,79 proporción (min = Holm; B=200 permutaciones, resolución limitada) [C4].
- **Efecto donut (`R1B`).** El cambio de pendiente del gradiente de crecimiento con la distancia al centro, antes y después de 2019, es 0,16 pp de crecimiento anual por cada 10 km en el alquiler y -0,04 pp de crecimiento anual por cada 10 km en el valor tasado; ninguna especificación es significativa tras Holm (0,00 proporción y 0,00 proporción) [C4].

### 5.2 Oster y Cinelli-Hazlett

| Diseño | Oster δ | RV de Cinelli-Hazlett | Capa |
|---|---|---|---|
| B3, `H-B3-1` (Bartik) | 3,8 | 0,28 (RV con α: 0,04 R² parcial) | C4 |
| B3, `H-B3-2` (población) | 1,6 | 0,26 (RV con α: 0,01 R² parcial) | C4 |
| v2, BI (alquiler e instrumento) | 8,8 | 0,35 | C4 |
| v2, BP H6 (muestra sellada) | — | 0,32 (aproximado) | C4 |

Un δ de Oster mayor que uno indica que las variables omitidas tendrían que estar más relacionadas con el resultado que las observadas para anular el coeficiente. En B3, el parámetro de Oster se acotó a uno porque la regla del pre-registro daba un valor mayor (desviación declarada). El RV con α, que exige que el intervalo deje de excluir el cero, es pequeño en las dos hipótesis de B3: una confusión modesta bastaría para que dejaran de ser significativas, en línea con su falta de significación tras Holm.

### 5.3 GSADF con tamaño corregido

La prueba GSADF de exuberancia con valores críticos para errores independientes tiene un tamaño empírico de 0,15 (fracción de rechazos con un nivel nominal convencional) cuando la variación sigue un AR(1) [C4]; con valores críticos por bootstrap de un AR(p) estimado, el tamaño baja a 0,04 [C4]. Con los valores corregidos:

| Razón | Estadístico (valor crítico, p y p ajustado BH) | Capa |
|---|---|---|
| Precio/renta (IPV) | 3,4 estadístico (min = vc 95 %; p=0.012; BH familia=0.080) | C4 |
| Precio/alquiler (IPV) | 3,1 estadístico (min = vc 95 %; p=0.036; BH familia=0.096) | C4 |
| Precio frente al valor de descuento del alquiler (IPV) | 0,90 estadístico (min = vc 95 %; p=0.762; BH familia=0.948) | C4 |
| Precio frente a la cuota hipotecaria (IPV) | 0,91 estadístico (min = vc 95 %; p=0.604; BH familia=0.948) | C4 |
| Precio/renta (valor tasado) | 0,22 estadístico (min = vc 95 %; p=0.932; BH familia=0.948) | C4 |
| Precio/alquiler (valor tasado) | 4,3 estadístico (min = vc 95 %; p=0.020; BH familia=0.080) | C4 |
| Precio frente al valor de descuento del alquiler (valor tasado) | 0,16 estadístico (min = vc 95 %; p=0.948; BH familia=0.948) | C4 |
| Precio frente a la cuota hipotecaria (valor tasado) | 0,52 estadístico (min = vc 95 %; p=0.838; BH familia=0.948) | C4 |

Ninguna razón supera el ajuste por comparaciones múltiples en la familia nacional; por comunidades autónomas, 7 series (max = significativas sin ajuste) de las combinaciones muestran exuberancia tras BH [C4]. Las razones que comparan el precio con fundamentales (valor de descuento del alquiler, cuota hipotecaria) no muestran exuberancia. Una exuberancia estadística no es una burbuja.

### 5.4 Pre-registro `prereg-v5` y desviaciones

El pre-registro (`docs/v5/prereg_B3.md`, etiqueta git `prereg-v5`) fijó antes de estimar: hipótesis, variables, ventanas, familias, errores estándar, inferencia por aleatorización y corrección de Holm. El análisis de potencia dio un efecto mínimo detectable de 0,62 DT (0,34-1,1 DT) [C4], y B3 se declaró descriptivo de antemano. Desviaciones, todas exploratorias (`output/v5/B3/desviaciones.md`):
1. Renta: PIB per cápita provincial en lugar de la renta por hogar, por la falta de serie provincial de 2015.
2. Ventanas más cortas en alquiler (SERPAVI) y en renta.
3. Crecimiento de la población con el padrón; los flujos migratorios terminan antes.
4. Hipotecas por habitante en lugar de por hogar.
5. La respuesta de la oferta se mide en la ventana del resultado: su asociación puede ser en parte mecánica.
6. Holm aplicado como dice el texto del pre-registro y, además, sobre las tres confirmatorias.
7. Validación dejando una provincia fuera en lugar de AR(4) y ECM, que no aplican a un corte transversal.
8. Control añadido del error de medida del precio inicial con otra fuente.
9. Parámetro de Oster acotado a uno.

---

## 6. Discusión

**Necesidad.** La cifra de necesidad es grande y su rango es amplio. El rango no es un defecto: muestra que la necesidad depende sobre todo de dos supuestos (el crecimiento de hogares y la parte movilizable de las vacías). Una política que fije un objetivo de producción debería declarar qué supuesto adopta.

**Territorio.** El déficit está concentrado y la clasificación separa dos situaciones con implicaciones distintas: donde construir es rentable y la oferta responde, y donde el precio supera holgadamente coste y suelo pero la oferta no responde. En el segundo caso, la literatura verificada de otros países apunta al suelo y a la tramitación; en España no hay evaluación comparable. La clasificación es exploratoria y depende del coste oficial.

**Precios.** La discrepancia entre índices no es un error de nadie: el índice oficial y los registros miden cosas distintas (método hedónico frente a medias, calidad, tamaño, cobertura). Citar una sola cifra sin su definición produce desacuerdos aparentes. El alquiler de stock y el de contratos nuevos también miden cosas distintas.

**Contribuciones.** La falta de estabilidad de las contribuciones es un resultado, no una carencia del análisis. Con las series y los cortes disponibles, la pregunta «qué factor explica la subida» no tiene una respuesta robusta. Un diseño de identificación requeriría variación exógena que los datos públicos no ofrecen en el periodo estudiado.

**Instrumentos.** La condición que más pesa en la evaluación de instrumentos es la respuesta de la oferta: el traslado de las ayudas a la demanda al precio va de 30,9 % en la clase `1` (método B) a 100,0 % en la clase `2` [C4]. Los instrumentos con signo estable en la rejilla de v3 son la construcción adicional donde falta y la movilización de vacías [C2 en el signo]. Las evaluaciones son condicionales y no sustituyen a evaluaciones con diseño de identificación en España.

**Convergencia.** Las cifras del proyecto coinciden con las de los organismos cuando concepto y periodo son comparables, y las diferencias se explican por definiciones. Las coincidencias con fuentes que comparten insumos primarios no elevan la capa.

---

## 7. Conclusiones

1. Entre 2021 y 2024 el aumento de hogares superó al de viviendas terminadas en 562.692-688.692 viviendas [C1]: es la cifra de déficit que se sostiene con dos fuentes.
2. La necesidad 2026-2035 y el déficit a 2030 son contabilidades con supuestos [C4]; su rango es amplio y depende de hogares y vacías.
3. El déficit se concentra en pocas provincias, y la clase territorial condiciona qué instrumentos tienen signo estable [C4].
4. El precio de compra subió 47,2 % según los registros [C1] y 79,9 % según el índice oficial [C4]; las dos cifras deben darse juntas.
5. No se puede atribuir la subida a una familia de factores: las contribuciones contables no son estables.
6. El pre-registro funcionó como estaba previsto: declaró la falta de potencia antes de ver los resultados y limitó las conclusiones a lo descriptivo.

---

## Referencias

Solo se citan como base referencias verificadas por DOI en Crossref, con cuartil Scimago cuando consta; el resto se marca.

- Ball, M. (2011). Planning delay and the responsiveness of English housing supply. *Urban Studies*. DOI: https://doi.org/10.1177/0042098010363499. VERIFICADA, Q1 (solo asociación).
- Büchler, S. y Lutz, E. (2024). Making housing affordable? The local effects of relaxing land-use regulation. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2024.103689. VERIFICADA, Q1.
- Carozzi, F., Hilber, C. A. L. y Yu, X. (2024). On the economic impacts of mortgage credit expansion policies: evidence from Help to Buy. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2023.103611. VERIFICADA, Q1.
- Cinelli, C. y Hazlett, C. (2020). Making sense of sensitivity: extending omitted variable bias. *Journal of the Royal Statistical Society, Series B*. DOI: https://doi.org/10.1111/rssb.12348. VERIFICADA, Q1.
- Diamond, R., McQuade, T. y Qian, F. (2019). The effects of rent control expansion on tenants, landlords, and inequality: evidence from San Francisco. *American Economic Review*. DOI: https://doi.org/10.1257/aer.20181289. VERIFICADA, Q1.
- Eriksen, M. D. y Ross, A. (2015). Housing vouchers and the price of rental housing. *American Economic Journal: Economic Policy*. DOI: https://doi.org/10.1257/pol.20130064. VERIFICADA, Q1.
- García-López, M. À., Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2020). Do short-term rental platforms affect housing markets? Evidence from Airbnb in Barcelona. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2020.103278. VERIFICADA, Q1.
- Gibbons, S. y Manning, A. (2006). The incidence of UK housing benefit: evidence from the 1990s reforms. *Journal of Public Economics*. DOI: https://doi.org/10.1016/j.jpubeco.2005.01.002. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (título de la obra) -->
- Glaeser, E. y Gyourko, J. (2018). The economic implications of housing supply. *Journal of Economic Perspectives*. DOI: https://doi.org/10.1257/jep.32.1.3. DOI verificado; cuartil no verificado.
- Greenaway-McGrevy, R. y Phillips, P. C. B. (2023). The impact of upzoning on housing construction in Auckland. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2023.103555. VERIFICADA, Q1.
- Hilber, C. A. L. y Turner, T. M. (2014). The mortgage interest deduction and its impact on homeownership decisions. *Review of Economics and Statistics*. DOI: https://doi.org/10.1162/rest_a_00427. VERIFICADA, Q1.
- Hilber, C. A. L. y Vermeulen, W. (2016). The impact of supply constraints on house prices in England. *Economic Journal*. DOI: https://doi.org/10.1111/ecoj.12213. VERIFICADA, Q1.
- Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2023). Effectiveness and supply effects of high-coverage rent control policies. *Regional Science and Urban Economics*. DOI: https://doi.org/10.1016/j.regsciurbeco.2023.103916. VERIFICADA, Q1.
- Manski, C. F. (2003). *Partial Identification of Probability Distributions*. Springer. DOI: https://doi.org/10.1007/b97478. VERIFICADA (libro).
- Oster, E. (2019). Unobservable selection and coefficient stability: theory and evidence. *Journal of Business & Economic Statistics*. DOI: https://doi.org/10.1080/07350015.2016.1227711. VERIFICADA, Q1.
- Phillips, P. C. B., Shi, S. y Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*. NO VERIFICADA en este proyecto (DOI no comprobado).
- Rambachan, A. y Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*. DOI: https://doi.org/10.1093/restud/rdad018. VERIFICADA, Q1.
- Saiz, A. (2010). The geographic determinants of housing supply. *Quarterly Journal of Economics*. DOI: https://doi.org/10.1162/qjec.2010.125.3.1253. DOI verificado; cuartil no verificado.

Lista completa y estado de verificación: `docs/literatura.md` y `docs/v5/literatura_instrumentos.md`.

---

## Apéndices

### Apéndice A. Datos

- Fuentes, licencias y fechas de descarga: `README_REPLICACION.md`, `docs/v5/licencias_datos.md` y el manifiesto de `data/raw`.
- Fuentes que no se pudieron obtener: `docs/v5/fuentes_fallidas.md`.
- Cada cifra del texto, con indicador, periodo, cobertura, fuentes, capa y fecha del dato: `output/v5/cifras_clave.md`.
- Tablas por módulo: `output/v5/<módulo>/tablas` y `resultado.json`.

### Apéndice B. Replicación

- `make all` reconstruye todos los resultados sin red; `make check` ejecuta las comprobaciones de puerta (cifras fuera de marcador, sumas provinciales, capas, léxico y lenguaje causal).
- Semilla `SEED=20261010` en todo lo aleatorio.
- Registro de especificaciones: `output/v5/*/registro.csv`; muestra sellada solo vía `src/holdout.py`.
- Este documento se genera con `python3 src/v5/render.py` desde `docs/v5/plantillas/working_paper.md`.

### Apéndice C. Uso de IA y declaración de independencia

- **Uso de IA.** El proyecto se ha ejecutado con agentes de IA (Claude, de Anthropic) bajo la supervisión del autor: un orquestador y subagentes de datos, econometría, literatura, redacción y revisión independiente por oleadas. Todas las cifras proceden del código del repositorio y de fuentes públicas; ninguna se ha tecleado en el texto. Las referencias se verifican por DOI o se marcan como no verificadas.
- **Responsabilidad.** El autor es responsable del contenido, incluidos los errores.
- **Independencia.** El trabajo no ha recibido financiación y no tiene vínculo con ningún partido ni organización política. Si hubiera algo que declarar, el autor lo completará en esta sección antes de la publicación.
