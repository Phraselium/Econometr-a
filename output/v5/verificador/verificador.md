# Verificador de afirmaciones sobre la vivienda en España (v5)

Generado por `make verificador`. Cada ficha evalúa la afirmación, nunca a quien la formula, y se aplican las mismas reglas a todas. Capas: C1 hechos (≥2 fuentes independientes), C2 cotas con supuestos explícitos, C3 efectos identificados (ninguno) y C4 exploratorio. Con C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE». «NO ANALIZADA: FALTAN DATOS» quiere decir que no hay datos para analizar la afirmación, no que sea falsa.

Recuento de veredictos: ANALIZADA, NO CONCLUYENTE: 32; NO ANALIZADA: FALTAN DATOS: 3; PARCIALMENTE: 3; CONTRADICHA: 1; NO RESPALDADA: 1.

| Id | Afirmación | Veredicto | Capa |
|---|---|---|---|
| V02 | Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres. | NO ANALIZADA: FALTAN DATOS | C4 |
| V06 | Los topes al precio del alquiler bajan los alquileres. | ANALIZADA, NO CONCLUYENTE | C4 |
| V07 | Los topes al precio del alquiler reducen la oferta de vivienda en alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |
| V08 | Hay millones de viviendas vacías que se podrían movilizar para resolver el problema. | ANALIZADA, NO CONCLUYENTE | C4 |
| V10 | Bajar el ITP o el IVA de la vivienda la abarataría para los compradores. | NO ANALIZADA: FALTAN DATOS | C4 |
| V11 | Construir vivienda pública resolvería el problema de la vivienda. | PARCIALMENTE | C2 |
| M3-V1 | Hay suelo de sobra para construir. | ANALIZADA, NO CONCLUYENTE | C4 |
| M4-V3 | Hay muchas viviendas vacías o de uso esporádico frente a las turísticas. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V2 | Faltan viviendas en toda España. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V3 | Los hogares crecen por la inmigración. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V4 | Limitar las compras de no residentes bajaría los precios de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V5 | Bajar los impuestos a la construcción abarataría la vivienda. | NO ANALIZADA: FALTAN DATOS | C4 |
| A23-V1 | El alquiler se ha duplicado (variante stock: renta de los contratos vigentes). | CONTRADICHA | C1 |
| A23-V2 | El alquiler se ha duplicado (variante contratos nuevos: renta de quien firma ahora). | ANALIZADA, NO CONCLUYENTE | C4 |
| B1-V1 | Hacen falta X viviendas al año en España. | ANALIZADA, NO CONCLUYENTE | C4 |
| B1-V2 | La vivienda que dejan los mayores resolverá el problema de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| B4-V1 | La subida se debe sobre todo a la inmigración. | ANALIZADA, NO CONCLUYENTE | C4 |
| B4-V2 | La subida se debe a los pisos turísticos. | ANALIZADA, NO CONCLUYENTE | C4 |
| B4-V3 | La subida se debe a la falta de oferta. | ANALIZADA, NO CONCLUYENTE | C4 |
| B4-V4 | La subida se debe a los tipos de interés bajos. | ANALIZADA, NO CONCLUYENTE | C4 |
| CA-V1 | La vivienda en España es más cara que en Europa. | ANALIZADA, NO CONCLUYENTE | C4 |
| CA-V2 | La falta de crédito a promotores frena la oferta de vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| CA-V3 | La mayoría compra al contado. | ANALIZADA, NO CONCLUYENTE | C4 |
| CB-V1 | La ocupación ilegal reduce la oferta de alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |
| CB-V2 | La mayoría de los caseros son pequeños propietarios. | ANALIZADA, NO CONCLUYENTE | C4 |
| CB-V3 | Las empresas y fondos dominan el alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |
| CC-V1 | Sin ayuda familiar los jóvenes no pueden comprar vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| CC-V2 | Las viviendas protegidas se pierden por descalificación y el parque protegido se erosiona. | ANALIZADA, NO CONCLUYENTE | C4 |
| D1-V1 | Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda. | PARCIALMENTE | C2 |
| R1A-V1 | Los compradores extranjeros encarecen la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| R1B-V1 | Hay una burbuja en el precio de la vivienda en España. | ANALIZADA, NO CONCLUYENTE | C4 |
| T1-V1 | En España apenas se derriban viviendas / las bajas del parque son despreciables. | ANALIZADA, NO CONCLUYENTE | C4 |
| T2-V1 | El envejecimiento resolvera el problema de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| T2-V2 | Las herencias liberaran vivienda suficiente. | ANALIZADA, NO CONCLUYENTE | C4 |
| T4-V1 | Al ritmo actual el déficit se cerrará en pocos años. | NO RESPALDADA | C2 |
| M4-V3 | El alquiler y la compra se mueven por los mismos factores. | ANALIZADA, NO CONCLUYENTE | C4 |
| M4-V4 | La ratio precio/alquiler indica sobrevaloracion. | ANALIZADA, NO CONCLUYENTE | C4 |
| K1-V1 | Los modelos de inteligencia artificial predicen el precio y el alquiler mejor que los métodos sencillos. | ANALIZADA, NO CONCLUYENTE | C4 |
| K2-V1 | La llegada de inmigrantes sube el precio de la vivienda o el alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |
| L3-V1 | Faltan cientos de miles de viviendas en España. | PARCIALMENTE | C2 |

## Fichas sustituidas en v5

| Ficha anterior | Sustituida por | Motivo |
|---|---|---|
| M7-V1 | R1B-V1 | GSADF con tamaño corregido y frente a fundamentales |
| M4-V1 | R1A-V1 | residentes y no residentes por provincia |
| M4-V2 | CB-V3 | stock y flujos, con dos métodos |
| M5-V1 | D1-V1 | traslado a precios por clase territorial |
| V09 | CB-V1 | datos del CGPJ y de Interior: la afirmación ya está analizada |
| V01 | B4-V2 | triangulación de B3, v2 y las cotas de v3 (la cota C2 de v3 se conserva) |
| V03 | B4-V1 | triangulación de B3, v2 y las cotas de v3 |
| V04 | B4-V3 | triangulación de B3, v2 y A4 |
| V12 | B4-V4 | triangulación de B3, v2 y la cota de v3 |
| B2-V1 | T4-V1 | v5.1: dirección y magnitud separadas en una rejilla de 180 escenarios |
| V05 | L3-V1 | v6.2: déficit 2021-2024 con siete correcciones del salto de la EPA; pasa de C1 a cota C2 |

## V02 · Grandes tenedores

**Afirmación:** Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Parque total: sí hay dato; 4,2 % de las viviendas son de titulares con más de diez (Catastro 2026, España sin País Vasco ni Navarra; V12-B5-pct_mas10). Parque en alquiler: solo datos parciales; 2,4 % del alquiler de vivienda principal en personas físicas con once o más (Banco de España, 2024; V17-DOC-BDE-GT-ALQUILER-2024), 36,1 % del alquiler habitual de Barcelona ciudad (O-HB, 2021; V17-DOC-OHB-GT-ALQUILER-BCN-2021) y, para España, entre el 2 % y el 12 % con supuestos explícitos (V17-AUD-OT-COTA-GT-ALQUILER-NACIONAL). Efecto sobre los precios: no medido en España. |
| Intervalo | n/d |
| Cota | Sin cota de la contribución a la subida: el efecto en los precios no está medido |
| Literatura | Sin trabajo replicado para España; la literatura de EE. UU. sobre inversores institucionales tiene validez externa limitada. |
| Regla del veredicto | Hay datos de titularidad del parque total y datos parciales del alquiler, pero ninguna estimación del efecto de los grandes tenedores sobre los precios en España: no se puede acotar su contribución a la subida. v4: Faltan datos para medir el efecto sobre los precios. Hay titularidad del parque total y datos parciales del alquiler (corregido en V17; ERRATA.md, 2026-10-19). |
| Límites | Corregido en V17: antes decía «sin datos de titularidad». El dato del parque total ya estaba publicado (atlas de V12 e informe integral, VII.7). El alquiler a escala nacional sigue sin dato directo. |
| Evidencia | output/v12/b5, docs/v17/fuentes/titularidad.md, output/v17/auditoria/filas/grandes_tenedores.md |

## V06 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler bajan los alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Principal (Callaway-Sant'Anna, fianzas Incasòl, renta de los contratos nuevos): -5,4 % [-7,1; -3,7] (p 0,000). Validación sellada por fuente (SERPAVI, stock): -0,77 % [-1,39; -0,14], p_Holm 0,048. Estimadores alternativos y réplica de JMS (objetivo −4,5 %): R1 JMS -3,5 % [-4,7; -2,3] (REPLICADO); R2 JMS -4,5 % [-6,5; -2,6] (REPLICADO). Multiverso: 100 % mismo signo, 89 % significativas. Capa C4 (falla: a, c). |
| Intervalo | [-7,1; -3,7] % (principal) |
| Cota | — |
| Literatura | Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE, VERIFICADA, Q1; Diamond, McQuade y Qian (2019), AER, VERIFICADA, Q1 (calibración, San Francisco). |
| Regla del veredicto | RESPALDADA solo con C3 robusto; con capa C4 el veredicto es SIN EVIDENCIA SUFICIENTE aunque las estimaciones C4 apunten en una dirección (no se promueve de capa). v4: H3-3a analizada: C4. No puede ser C3: la validación por fuente no es independiente y el cálculo de potencia vio municipios sellados (decisiones v3, O1). |
| Límites | Un solo episodio (Cataluña, 2020Q4-2022Q1). La validación por fuente mide un stock (SERPAVI) en los mismos municipios: no es independiente y su magnitud es menor que la principal. |
| Evidencia | output/v3/C3/resultado.json, output/v3/C3/tabla_replicacion_jms.csv, output/v3/holm_v3.csv |

## V07 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler reducen la oferta de vivienda en alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Principal (Callaway-Sant'Anna, fianzas Incasòl, número de contratos nuevos): -4,9 % [-9,9; 0,5] (p 0,073). Validación sellada por fuente (SERPAVI, stock): -4,36 % [-6,37; -2,30], p_Holm 0,000. Estimadores alternativos y réplica de JMS (objetivo −0,3 % en contratos): R1 JMS 3,0 % [-0,9; 7,0] (PARCIAL); R2 JMS -2,0 % [-8,3; 4,2] (PARCIAL). Multiverso: 81 % mismo signo, 0 % significativas. Capa C4 (falla: a, b, c). |
| Intervalo | [-9,9; 0,5] % (principal) |
| Cota | — |
| Literatura | Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE, VERIFICADA, Q1; Diamond, McQuade y Qian (2019), AER, VERIFICADA, Q1 (calibración, San Francisco). |
| Regla del veredicto | RESPALDADA solo con C3 robusto; con capa C4 el veredicto es SIN EVIDENCIA SUFICIENTE aunque las estimaciones C4 apunten en una dirección (no se promueve de capa). v4: H3-3b analizada: C4 (fallan pretendencias, placebo de fecha y sensibilidad); mismas salvedades de contaminación que V06. |
| Límites | Un solo episodio (Cataluña, 2020Q4-2022Q1). La validación por fuente mide un stock (SERPAVI) en los mismos municipios: no es independiente y su magnitud es menor que la principal. |
| Evidencia | output/v3/C3/resultado.json, output/v3/C3/tabla_replicacion_jms.csv, output/v3/holm_v3.csv |

## V08 · Viviendas vacías

**Afirmación:** Hay millones de viviendas vacías que se podrían movilizar para resolver el problema.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4). En las muestras municipales con dato (277 a 1.806 municipios según la definición), el 27,5-40,3 % de las vacías está en el tercil alto de presión de precios y el 20,7-28,3 % en el tercil bajo (C1, dos medidas). |
| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 a 1.806 municipios) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | La cifra de millones es de fuente única (C4); el reparto por presión (C1) sitúa en el tercil alto entre el 27,5 % y el 40,3 %; la fracción movilizable es un supuesto (P-D). PARCIALMENTE: hay muchas vacías, pero su movilización para «resolver» no está evaluada. v4: La cifra de vacías y su reparto proceden del Censo 2021 (consumo eléctrico); Catastro − hogares no es independiente del Censo, que se construye sobre el Catastro (revisión B, B10/B8). |
| Límites | Vacía por consumo eléctrico incluye viviendas en venta, en obras o en herencias; independencia parcial de las dos medidas. |
| Evidencia | output/v3/PA/hechos.json#A3, output/v3/PD/resultados.json |

## V10 · Fiscalidad

**Afirmación:** Bajar el ITP o el IVA de la vivienda la abarataría para los compradores.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Sin diseño propio; la incidencia depende de la elasticidad de la oferta (no estimada aquí). |
| Intervalo | n/d |
| Cota | — |
| Literatura | Sin trabajo de incidencia verificado incorporado. |
| Regla del veredicto | La incidencia depende de la elasticidad de la oferta: si fuera baja, parte de la rebaja podría trasladarse al precio; sin estimación no se puede cuantificar ni fijar su signo neto para el comprador. v4: Falta una serie armonizada de tipos de ITP/IVA por CCAA y fecha con precios a escala fina; el diseño de diferencias no se realizó. |
| Límites | Los cambios autonómicos del ITP permitirían un diseño de diferencias (no realizado). |
| Evidencia | — |

## V11 · Vivienda pública

**Afirmación:** Construir vivienda pública resolvería el problema de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | variación del esfuerzo medio nacional (10 mil/año; coste unitario = parámetro): [-5,4; 0,0] %; variación del esfuerzo medio nacional (25 mil/año; coste unitario = parámetro): [-13,1; 0,0] % |
| Intervalo | ver magnitud |
| Cota | — |
| Literatura | Calibración con la literatura de P-D. |
| Regla del veredicto | Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igual (≤ 0; nulo si desplaza por completo a la construcción privada, ρ = 1); con 10.000-25.000 viviendas/año queda lejos de la brecha de 104.000-413.000 viviendas/año, de modo que «resolver» depende del volumen y del desplazamiento. |
| Límites | Simulación con rangos de elasticidades; coste fiscal no cuantificado sin dato de coste. |
| Evidencia | output/v3/PD/resultados.json |
| Convención A (estricta: traducción a precio en C4) | PARCIALMENTE |
| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Regla común con M5-V1 (revisión C, C5): signo estable en la rejilla (≤ 0, nulo con desplazamiento total), C2; magnitud C4. «Resolvería» no se sostiene a las dosis simuladas: 10.000-25.000 viviendas/año frente a una brecha de 104.000-413.000/año (cantidades contables C2). |

## M3-V1 · Suelo disponible

**Afirmación:** Hay suelo de sobra para construir.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Solares catastrales (uso «solar») 2026: 3.092.393 unidades urbanas. Con 5/10/20 viviendas por solar cubren el déficit 2021-2025 (mediana M1) en 100 %/100 %/100 % de las 48 provincias con déficit positivo y dato de solares (excluidas 4 provincias sin dato de solares). Esa prueba provincial no es informativa: da positivo por construcción cuando el total de solares supera con holgura al déficit. En municipios con déficit positivo y dato (454) la cobertura es 100 %/100 %/100 %. La brecha precio-coste no se usa: el coste en nivel es un supuesto. |
| Intervalo | cobertura provincial [100 %; 100 %]; municipal [100 %; 100 %] según viviendas por solar (5 a 20) |
| Cota | — |
| Literatura | Glaeser y Gyourko (2018, VERIFICADA): precio por encima del coste de construcción más suelo; sin cifra citable para España. |
| Regla del veredicto | Regla común con M4-V3: con capa C4 el veredicto máximo es «ANALIZADA, NO CONCLUYENTE»; PARCIALMENTE exige al menos C2. La fuente de suelo es única (Catastro) y el SIU no es accesible. |
| Límites | El uso «solar» catastral cuenta unidades urbanas sin edificar, sin superficie, uso urbanístico, edificabilidad, estado de urbanización ni disponibilidad en el mercado. Puede sobrestimar el suelo disponible (incluye solares industriales o terciarios, parcelas residuales, suelo sin urbanizar del todo) y subestimarlo (deja fuera el suelo urbanizable sin planeamiento de desarrollo, rústico a efectos catastrales). Sin dato en las provincias forales. SIU inaccesible (docs/v4/fuentes_fallidas.md). El coste de construcción en nivel no tiene fuente verificable. |
| Evidencia | output/v4/M3/clasificacion_provincias.csv, output/v4/M3/clasificacion_municipios.csv, output/v4/M3/tablas/M3_solares_nacional_catastro.csv, data/raw/v4/catastro_solares_municipios.csv.gz |

## M4-V3 · Viviendas vacías, de uso esporádico y turísticas

**Afirmación:** Hay muchas viviendas vacías o de uso esporádico frente a las turísticas.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | España: 3.828.307 vacías (14,4 % del parque) y 2.517.628 de uso esporádico (9,5 %) en el Censo 2021 (método de consumo eléctrico); 341.001 turísticas en mayo de 2026 (1,3 % del parque 2021). Ratio (vacías + esporádicas) / turísticas: 18,6. |
| Intervalo | — |
| Cota | — |
| Literatura | No revisada en esta ficha. |
| Regla del veredicto | Hecho descriptivo: las vacías y esporádicas suman un orden de magnitud más que las turísticas. «Muchas» no tiene umbral y la fuente de vacías es única (capa C4), por lo que no cabe veredicto de respaldo. |
| Límites | Vacía y esporádica se infieren del consumo eléctrico (INE, experimental); las turísticas son de otra fecha y pertenecen al parque principal o no principal (no suman). El registro de la Generalitat Valenciana (3 provincias) y el INE difieren 1,5-2,2 veces en turísticas (ver vut_ine_frente_registro_gva.csv): la cifra nacional es de fuente única (C4). No se estima ningún efecto. |
| Evidencia | output/v4/M4/tablas/stock_uso_nacional.csv, output/v4/M4/tablas/stock_uso_provincia.csv, output/v4/M4/tablas/stock_uso_ciudades.csv, output/v4/M4/tablas/vut_ine_frente_registro_gva.csv |

## M5-V2 · Geografía del déficit

**Afirmación:** Faltan viviendas en toda España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | 2021-2025: ninguna provincia con excedente; 7 provincias suman el 50 % del déficit y 19 el 80 %; 249 municipios con excedente (71 mil viviendas). Hechos de M1 en C4 (hogares provinciales de fuente única). |
| Intervalo | 7 provincias = 50 % del déficit |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Hay déficit en todas las provincias, pero muy concentrado y con municipios en excedente; capa C4 (fuente única de hogares provinciales). |
| Límites | Los municipios usan Catastro (sin territorios forales). Capa C4 por regla B5: hogares de fuente única (ECP) impiden C2; altas triangulables (componente C2) |
| Evidencia | output/v4/M1/hechos.json |

## M5-V3 · Demografía

**Afirmación:** Los hogares crecen por la inmigración.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | 2021-2025: hogares +1,01 millones (C1: ECP y EPA corregida). En la descomposición contable, el componente de población de nacionalidad extranjera supone el 56-58 % (rango 53-76 % según la corrección de la EPA), con jefatura de fuente única (C4). |
| Intervalo | 56-58 % de ΔH (componente contable) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | La descomposición es contable, no causal, y sus componentes son C4. Es compatible con la afirmación como descripción del crecimiento de hogares 2021-2025; no lo es para 2008-2013, cuando el componente extranjero fue ≈0. |
| Límites | Nacionalidad, no país de nacimiento; sin migración interior. |
| Evidencia | output/v4/M2/hechos.json |

## M5-V4 · Compras de no residentes

**Afirmación:** Limitar las compras de no residentes bajaría los precios de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Compradores extranjeros no residentes ≈7 % de las compraventas en 2025 (MIVAU), concentrados en costa e islas (C4). Sin diseño sobre el precio. |
| Intervalo | ≈7 % de las compraventas |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Hay un peso descriptivo (C4), pero ningún diseño ni cota sobre el precio. |
| Límites | Fuentes no independientes (MIVAU y Notariado). |
| Evidencia | output/v4/M4/hechos.json |

## M5-V5 · Fiscalidad de la construcción

**Afirmación:** Bajar los impuestos a la construcción abarataría la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Sin diseño ni datos de incidencia; con oferta rígida parte de la rebaja puede trasladarse al precio del suelo. |
| Intervalo | n/d |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Falta una serie de cargas tributarias de la promoción por municipio y una estimación de la elasticidad de oferta. |
| Límites | — |
| Evidencia | — |

## A23-V1 · Alquiler

**Afirmación:** El alquiler se ha duplicado (variante stock: renta de los contratos vigentes).

| Campo | Contenido |
|---|---|
| Veredicto | **CONTRADICHA** |
| Capa de la evidencia | C1 |
| Magnitud | Stock 2015-2025: IPC alquiler +13.6 %. 2015-2024: IPC alquiler +10.9 %, IPVA contratos existentes +20.6 %, IPVA total +22.9 %, SERPAVI (composición constante) +43.0 %. Ninguna fuente llega a +100 %. |
| Intervalo | [10.9; 43.0] % (núcleo IPC/IPVA: 10.9-22.9 %; SERPAVI discrepante) |
| Cota | Cuantía C1 en el núcleo (IPC alquiler, grupo INE; IPVA, grupo AEAT); SERPAVI comparte fuente (AEAT) con el IPVA y queda fuera del núcleo; se reportan ambos. |
| Literatura | No aplica. |
| Regla del veredicto | Duplicarse exige +100 %; el stock mide las mismas viviendas o contratos vigentes y todas las medidas quedan por debajo. |
| Límites | El stock sube menos que la renta de quien busca piso (ver variante contratos nuevos). Sin fianzas de Madrid, Euskadi ni Baleares (sin dato abierto localizado, docs/v5/fuentes_fallidas.md); IPVA nuevo contrato solo 2021-2024 (2015=100 supuesto, coherente con el total); portales (Idealista, Fotocasa) fuera de la ficha (C4, sin cifra verificada); medias no excluyen municipios concretos con subidas mayores. |
| Evidencia | output/v5/A23/tablas/alquiler_series_nacional_cataluna.csv, output/v5/A23/tablas/ipva_cuota_implicita.csv |

## A23-V2 · Alquiler

**Afirmación:** El alquiler se ha duplicado (variante contratos nuevos: renta de quien firma ahora).

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | IPVA contrato nuevo 2015-2024 +37.0 % (nacional). Incasòl renta media 2015-2025 +54.5 % (Cataluña). GVA mediana de fianza 2020-2025 +58.0 % (C. Valenciana). 2021-2024: Cataluña 16.6-17.2 %, C. Valenciana 26.1-30.8 %. Municipios con renta de fianzas x2 o más: 1 de 261 (Cataluña, 2015-2025) y 2 de 103 (C. Valenciana, 2020-2025). |
| Intervalo | [37.0; 54.5] % en 2015-2024/25 |
| Cota | Dirección C1 en Cataluña y C. Valenciana (IPVA, Incasòl y GVA, grupos independientes, mismo signo); cuantía nacional C4 (fuentes de cobertura distinta). |
| Literatura | No aplica. |
| Regla del veredicto | Regla B5: la cuantía nacional de contratos nuevos es de fuente única (IPVA, C4), así que el veredicto nacional es como máximo ANALIZADA, NO CONCLUYENTE. Limitado a Cataluña y C. Valenciana (C1 en dirección y banda 2021-2024), la afirmación queda CONTRADICHA en promedio en 2021-2024. Las medias de contratos nuevos suben más que el stock, pero ninguna fuente alcanza +100 % en el periodo; la afirmación puede cumplirse en municipios o segmentos concretos fuera de las fuentes oficiales con dato. |
| Límites | Sin fianzas de Madrid, Euskadi ni Baleares (sin dato abierto localizado, docs/v5/fuentes_fallidas.md); IPVA nuevo contrato solo 2021-2024 (2015=100 supuesto, coherente con el total); portales (Idealista, Fotocasa) fuera de la ficha (C4, sin cifra verificada); medias no excluyen municipios concretos con subidas mayores. |
| Evidencia | output/v5/A23/tablas/brecha_nuevo_stock_ccaa.csv, output/v5/A23/tablas/gva_fianzas_resumen.csv |

## B1-V1 · Necesidad de vivienda

**Afirmación:** Hacen falta X viviendas al año en España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Contabilidad stock-flujo 2026-2035 (suma de 52 provincias): 214868 viviendas/año central, rango 93628 a 309921 (cotas con todos los componentes en su extremo). De ellas, atraso a absorber en 10 años: 110317/año; crecimiento de hogares más reposición: 181020/año. D y S aparte. |
| Intervalo | 93628 a 309921 viviendas/año (C4) |
| Cota | — |
| Literatura | Gabriel y Nothaft (2001), J. Urban Econ., DOI 10.1006/juec.2000.2187: VERIFICADA (DOI en Crossref; JUE, Q1 según docs/literatura.md); sustenta la existencia de una vacancia friccional, no el rango 2-4 % (supuesto del encargo). |
| Regla del veredicto | Capa del total = menor de sus componentes: A, R, V, M, K y L en C4 (hogares provinciales de fuente única, supuestos no contrastados); solo F (INE, dos métodos) en C2. Con C4 el máximo es ANALIZADA, NO CONCLUYENTE. El valor depende del atraso y de las vacías movilizables, que son los componentes más inciertos. |
| Límites | Sin dato de hogares compartidos, hacinamiento ni residencias; vacancia disponible sin dato; K aproxima la cartera con iniciadas menos terminadas; los rangos no son IC. |
| Evidencia | output/v5/B1/tablas/B1_tabla_provincial.csv, output/v5/B1/resultado.json |

## B1-V2 · Envejecimiento

**Afirmación:** La vivienda que dejan los mayores resolverá el problema de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Viviendas liberadas por disolución de hogares de 75+ en 2026-2035: 141526/año central (rango 80198-217007); equivalen al 66% de la necesidad anual central; 97% de ellas en provincias con presión (A4 clase 1-2). Ya están descontadas en el crecimiento neto de hogares del INE, así que no suman a la oferta adicional. |
| Intervalo | 80198 a 217007 viviendas/año (C4) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | L es C4 (tasa de jefatura 75+ sin dato propio, traslados a residencias sin dato, destino de la vivienda liberada -venta, alquiler, herencia, uso esporádico- sin dato). Los hechos acotan el orden de magnitud, no el veredicto. |
| Límites | Sin Censo 2021 por edad del jefe; mortalidad de 2024 constante (sesgo al alza de la liberación). |
| Evidencia | output/v5/B1/tablas/B1_envejecimiento.csv |

## B4-V1 · Inmigración

**Afirmación:** La subida se debe sobre todo a la inmigración.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Cota C2 de cantidad: la población extranjera supone como máximo el 45,2 % de la creación de hogares en 2014-2019 (174.410 viviendas) y no informa en 2020-2025 (100 %). Precio: condicional a |ε_d|=0,33, ≤2,1 % (2014-2019) y ≤19,0 % (2020-2025) (C4). v2: la componente demográfica de la descomposición contable es de -3,0 a -4,1 pp al alquiler en 2014-2019 y signo opuesto según modelo en compra 2020-2024 (M1 +1,2; M2 -5,3 pp reales). B3: demografía segunda por cuota de R2 (21-26 %), con p de Holm 0,41 para F2. |
| Intervalo | Cuota de R2 entre provincias 21-26 %; contribución v2 sin signo estable |
| Cota | C2 solo la cantidad; magnitud sobre precio C4 |
| Literatura | No aplica. |
| Regla del veredicto | La traducción a precio solo es C4 (ε sin estimación verificada, fuente única de población); sin C3 no se puede afirmar ni negar el papel principal. |
| Límites | La asociación transversal y la contribución temporal discrepan en signo y orden; sin identificación causal. |
| Evidencia | output/v5/B4/tabla_contribuciones_larga.csv, output/v5/B4/estabilidad.csv |

## B4-V2 · Turismo

**Afirmación:** La subida se debe a los pisos turísticos.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Cota C2: como máximo el 2,4-2,7 % del stock de alquiler (hasta 81.771 viviendas), 2020M08-2024M08, suponiendo sustitución 1:1. En precio de alquiler, condicional a |ε_d| (1,0-0,33): ≤2,7-8,3 % frente a un alquiler de stock que sube 10,9-22,9 % en 2015-2024 (IPC, IPVA). v2 (2021T3-2024T1, solo M1): +0,02 pp [-0,06; 0,09] de 2,26 pp. B3: VUT sin coeficiente distinguible de 0 en precio. Concentración local: hasta 8,9 % del stock en Málaga capital (cota C2). |
| Intervalo | Cantidad 2,4-2,7 % del stock (C2); precio ≤2,7-8,3 % (C4, condicional) |
| Cota | C2 de cantidad; C4 de precio |
| Literatura | No aplica. |
| Regla del veredicto | La cota de cantidad (C2) limita el desplazamiento nacional, pero la traducción a precio depende de una elasticidad no verificada (C4): no se llega a un veredicto sobre «se debe». El alcance es nacional; en ciudades concretas la cota es mayor. |
| Límites | VUT del INE es estadística experimental; sin series de alquiler turístico/de temporada (BK-014 sin analizar); no residentes: con controles la asociación no se distingue de cero (R1A, C4). |
| Evidencia | output/v5/B4/tabla_contribuciones_larga.csv, output/v5/B4/estabilidad.csv |

## B4-V3 · Oferta

**Afirmación:** La subida se debe a la falta de oferta.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | B3: la brecha de oferta (F4) es la familia con mayor cuota de R2 entre provincias (23-29 %), pero se mide en 2021-2025 con precios y puede ser en parte mecánica. v2: la componente contable de la oferta contemporánea (terminadas) es de -0,02 a 0,10 pp, con IC que incluye 0. Las clases de A4 son C4 (regla B5). |
| Intervalo | B3 23-29 % del R2; v2 -0,02 a 0,10 pp |
| Cota | C4 (no hay cota de oferta con supuestos explícitos en esta tabla) |
| Literatura | No aplica. |
| Regla del veredicto | Los dos métodos discrepan (orden primero en B3, nulo en v2) y ninguno es C3; se reportan ambos. |
| Límites | Medición distinta en cada método (stock de déficit frente a flujo de terminadas); sin respuesta de la oferta identificada. |
| Evidencia | output/v5/B4/tabla_contribuciones_larga.csv, output/v5/B4/estabilidad.csv |

## B4-V4 · Financiación

**Afirmación:** La subida se debe a los tipos de interés bajos.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | v3 PB: la caída del coste de uso es compatible como máximo con +23,5 a +78,0 % (Δln 1/uc) en 2014-2021 frente a +12,7 % de precio tasado; en 2021-2025 los tipos suben y el precio también (+25,0 %): signo contrario. v2: financiación y tipos +1,9 a +2,3 pp en compra real (M1) y ≈0 (M2): discrepan. En alquiler, la componente de los tipos se fija en 0 por supuesto. B3: hipotecas por 1.000 habitantes sin asociación distinguible (8,9-13,6 % del R2). |
| Intervalo | v2 compra -0,00 a 2,27 pp según modelo; cota v3 23-78 % (C4) |
| Cota | C4 |
| Literatura | No aplica. |
| Regla del veredicto | Los métodos discrepan y la componente común de los tipos nacionales queda en el componente común de v2 (tiempo), no atribuible por provincia; sin C3 no se concluye. |
| Límites | Los tipos nacionales no varían entre provincias: v2 y B3 no los identifican; la cota v3 es condicional a supuestos de coste de uso. |
| Evidencia | output/v5/B4/tabla_contribuciones_larga.csv, output/v5/B4/estabilidad.csv |

## CA-V1 · Comparación europea

**Afirmación:** La vivienda en España es más cara que en Europa.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Crecimiento (real, 2015-2025): precio +42.6 % en España frente a una mediana UE-27 de +37.4 % (percentil 65, dentro del rango intercuartílico 16.9 a 60.9); alquiler real -10.3 % frente a -3.0 % (percentil 22, bajo). Nivel: Eurostat no publica un precio por m² comparable; como aproximación, la sobrecarga de coste de vivienda es 7.2 % de la población (2025) frente a una mediana de 6.1 % (percentil 74, dentro). Sostenidamente fuera del rango (5 años): emancipacion|nivel, propiedad|cambio_desde_2015, alquiler_mercado|cambio_desde_2015; (3 años): emancipacion|nivel, emancipacion|cambio_desde_2015, propiedad|cambio_desde_2015, alquiler_mercado|cambio_desde_2015, crec_pob|nivel, migr_neta|nivel. |
| Intervalo | percentil de España en el precio real: 65; en la sobrecarga: 74 |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Variante de nivel: no contrastable con un precio comparable (el HPI es un índice, no un nivel); las aproximaciones de asequibilidad no sitúan a España fuera del rango intercuartílico. Variante de crecimiento: el precio real acumulado desde 2015 queda dentro del rango; el alquiler real queda por debajo de la mediana. Capa C4: el dato del resto de países es de fuente única (Eurostat) y el de España procede del INE. |
| Límites | Comparación entre índices con base 2015; deflactor IPCA general; Eurostat toma los datos de España del INE (coherencia, no independencia). Países sin dato en el año omitidos. |
| Evidencia | output/v5/CA/tablas/europa_posicion_es.csv, output/v5/CA/tablas/europa_contraste_nacional.csv |

## CA-V2 · Crédito a promotores

**Afirmación:** La falta de crédito a promotores frena la oferta de vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | El saldo de crédito a construcción y actividades inmobiliarias pasó de 470 mil millones de euros (máximo, 2008) a 98 en 2025. De 36 pruebas (retardos de 0 a 8 trimestres, 4 regresores) con Holm, 1 resulta distinta de cero: g_inmobiliarias retardo 8 (rho -0.56); el signo es negativo (asociación descriptiva únicamente). Fuera de muestra, el modelo con crédito no mejora a AR(4) (DM-HLN p = 0.57). |
| Intervalo | — |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Relación descriptiva entre variaciones interanuales, sin interpretación de efecto. El saldo no es nuevas operaciones (no disponibles por finalidad en el Boletín). |
| Límites | Variaciones interanuales solapadas (HAC 8); iniciadas libres, no protegidas; la EPB de España trae criterios de empresas desde 2003 y de vivienda desde 2022. |
| Evidencia | output/v5/CA/tablas/credito_iniciadas_retardos.csv, output/v5/CA/tablas/credito_iniciadas_anual.csv |

## CA-V3 · Forma de pago

**Afirmación:** La mayoría compra al contado.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | En 2025, el INE registra 70.0 hipotecas sobre vivienda por cada 100 compraventas de vivienda; Registradores da 70.7 (diferencia máxima 1.9 pp en 2022-2025). Si todas las hipotecas financiaran compras, el contado sería al menos el 30 %; la mayoría al contado exige que menos del 71 % de las hipotecas sobre vivienda financie una compra, fracción no observada. |
| Intervalo | contado 30 % (phi = 1) a 58 % (phi = 0,6) |
| Cota | C2-like: contado = 100 - phi x razón; supuesto sobre phi declarado, no estimado |
| Literatura | — |
| Regla del veredicto | La razón hipotecas/compraventas es un hecho coherente en dos fuentes (ambas de origen registral); el porcentaje al contado depende de qué parte de las hipotecas no es de compra. La demanda inversora no equivale al contado: un inversor puede financiarse con hipoteca y un comprador residente puede pagar al contado. |
| Límites | Notariado (porcentaje de compras financiadas) sin dato accesible; Registradores solo 2022-2025 (texto de los Anuarios ERI). No distingue comprador residente de inversor. |
| Evidencia | output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv, output/v5/CA/tablas/contado_sensibilidad_phi.csv |

## CB-V1 · Seguridad jurídica y oferta

**Afirmación:** La ocupación ilegal reduce la oferta de alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | N=17 CCAA; Spearman usurpacion/100.000 viv. con cuota de alquiler: rho=0.66 (p Holm 0.0378); verbales posesorios con cuota: rho=0.61 (p Holm 0.0525). Las especificaciones sobre variaciones 2021-2025 y sobre lanzamientos por LAU no son significativas (registro.csv). El signo es positivo (mas usurpaciones donde hay mas alquiler), contrario al de la afirmacion; es compatible con que ambas magnitudes crecen con la urbanizacion. Sin diseno que identifique un efecto. |
| Intervalo | None |
| Cota | Sin cota (C4) |
| Literatura | No consultada en este modulo |
| Regla del veredicto | Con C4 y sin identificacion, como maximo ANALIZADA, NO CONCLUYENTE. |
| Límites | Una asociacion entre CCAA no distingue oferta, demanda ni composicion; el denominador (viviendas) y el numerador (denuncias) dependen del tamano del parque; el delito de usurpacion incluye inmuebles que no son vivienda; fianzas por CCAA no disponibles. |
| Evidencia | C, G, P, J,  , 1, T,  , 2, 0, 2, 6, ;,  , I, n, t, e, r, i, o, r,  , 2, 0, 2, 5, ;,  , I, N, E,  , C, e, n, s, o,  , 2, 0, 2, 1,  , y,  , E, C, V,  , 2, 0, 2, 5, ;,  , t, a, b, l, a, s,  , e, n,  , o, u, t, p, u, t, /, v, 5, /, C, B, /, t, a, b, l, a, s |
| Convención (nota) | Cifras con fecha del dato; sin lenguaje causal |

## CB-V2 · Arrendadores

**Afirmación:** La mayoría de los caseros son pequeños propietarios.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Personas fisicas declaran 2.333.816 viviendas equivalentes arrendadas como vivienda habitual (IRPF 2024); el residual PJ+publico+no declarado es 16.9-38.1 % del stock; 0.81 viviendas equivalentes por declarante con ingresos de capital inmobiliario. |
| Intervalo | None |
| Cota | Sin cota (C4) |
| Literatura | No consultada en este modulo |
| Regla del veredicto | Falta la distribucion por numero de inmuebles (1, 2-4, >=5): la AEAT no la publica; el promedio no la sustituye. Los datos acotan el peso de las personas juridicas, no el tamano de las carteras de las personas fisicas. |
| Límites | Fechas distintas entre fuentes; Navarra y Pais Vasco fuera de la AEAT; copropiedad cuenta como declarantes separados. |
| Evidencia | A, E, A, T,  , I, R, P, F,  , 2, 0, 2, 4, ;,  , I, N, E,  , C, e, n, s, o,  , 2, 0, 2, 1, ,,  , E, C, V,  , 2, 0, 2, 5, ,,  , E, C, H,  , 2, 0, 2, 5, T, 4 |
| Convención (nota) | Cifras con fecha del dato; sin lenguaje causal |

## CB-V3 · Empresas en el alquiler

**Afirmación:** Las empresas y fondos dominan el alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Flujo de compra con comprador PJ: 11.3 % de compraventas (ETDP 2024). Stock: el residual PJ+publico+no declarado del alquiler principal es 16.9 % (stock del Censo 2021) y 38.1 % (stock ECV 2025); los dos métodos discrepan y se dan ambos. Es una cota superior del peso de las empresas bajo esos supuestos. |
| Intervalo | None |
| Cota | Sin cota (C4) |
| Literatura | No consultada en este modulo |
| Regla del veredicto | Bajo los supuestos declarados, ninguna de las dos estimaciones del residual alcanza el 50 % del stock de vivienda principal en alquiler; ambas son C4 (fechas distintas, fuente unica del Censo, discrepancia entre ellas) y no miden el peso por zonas ni por tamano de cartera. |
| Límites | No se localizo Catastro por naturaleza del titular, Notariado ni Censo por tipo de arrendador; concentracion local (grandes ciudades) no medida. |
| Evidencia | I, N, E,  , E, T, D, P,  , 2, 0, 2, 4, ;,  , A, E, A, T,  , 2, 0, 2, 4, ;,  , I, N, E,  , C, e, n, s, o,  , 2, 0, 2, 1, ;,  , I, N, E,  , E, C, V,  , 2, 0, 2, 5 |
| Convención (nota) | Cifras con fecha del dato; sin lenguaje causal |

## CC-V1 · Desigualdad y ayuda familiar

**Afirmación:** Sin ayuda familiar los jóvenes no pueden comprar vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | No medible con los datos accesibles: la EFF publicada en el repositorio no recoge herencia, donación ni ayuda para la entrada. Contexto descriptivo: 30,6 % de los hogares de 16-29 años están en propiedad (34,2 % en 2015), de ellos 14,1 puntos sin hipoteca (la ECV no distingue su origen). |
| Intervalo | n/d |
| Cota | n/d |
| Literatura | NO VERIFICADA (no se consultó literatura en este módulo) |
| Regla del veredicto | Con capa C4 el máximo es «ANALIZADA, NO CONCLUYENTE»; la afirmación exige un contrafactual (compra sin ayuda) que ningún dato accesible identifica. |
| Límites | Propiedad sin hipoteca no equivale a herencia o donación. Sin cuadro EFF de ayuda familiar. ECV y Eurostat no son fuentes independientes. |
| Evidencia | output/v5/CC/tablas/ecv_tenencia_16_29.csv, output/v5/CC/tablas/sobrecarga_quintil_tenencia_2015_ultimo.csv |

## CC-V2 · Vivienda protegida

**Afirmación:** Las viviendas protegidas se pierden por descalificación y el parque protegido se erosiona.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Escenarios ilustrativos (plazo de 30 años salvo excepciones; no recorren el supuesto de 15-30 años): salidas 2026-2035 de 532040 (bajo) a 669394 (alto) viviendas, base 594890, frente a 11265 calificaciones nuevas al año de media en los últimos 5 años (2021-2025). |
| Intervalo | 0-669394 viviendas (cota inferior lógica 0 si el régimen fuese permanente) |
| Cota | Sin cota C2: los escenarios no recorren todo el supuesto de plazos (15-30 años) y las descalificaciones efectivas no se observan |
| Literatura | NO VERIFICADA (el texto introductorio del RD 326/2026 afirma la dinámica de descalificación; no hay contraste independiente) |
| Regla del veredicto | Regla B4: con capa C4 el máximo es ANALIZADA, NO CONCLUYENTE. Los escenarios ilustran la salida por fin de plazo con supuestos; la descalificación efectiva no se observa. |
| Límites | Los plazos autonómicos no se han recogido; las salidas son por fin de plazo, no descalificaciones observadas. |
| Evidencia | output/v5/CC/tablas/salidas_nacional_2026_2035.csv, output/v5/CC/tablas/plazos_planes.csv |

## D1-V1 · Ayudas a la demanda

**Afirmación:** Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Signo por grupo (C2, estable en la rejilla de P-D): el beneficiario paga igual o menos; el no beneficiario paga más. Traslado a precios de una ayuda general por unidad (C4, método A): clase 1 28 %-82 %; clase 2 88 %-100 %; clase 3 50 %-90 %; clase 9 No evaluable. Con el método B: clase 1 15 %-46 %, clase 2 100 %-100 %, clase 3 40 %-77 %. |
| Intervalo | clase 1: 28 %-82 %; clase 2: 88 %-100 %; clase 3: 50 %-90 % al precio (C4) |
| Cota | C2 de signo por grupo; magnitud y clase C4 |
| Literatura | Eriksen-Ross 2015 (VERIFICADA, Q1); Hilber-Turner 2014 (VERIFICADA, Q1); Gibbons-Manning 2006 (VERIFICADA, Q1; J. Public Economics); Carozzi-Hilber-Yu 2024 (VERIFICADA, Q1). |
| Regla del veredicto | Regla común con M5-V1: signo estable (C2) para el grupo al que se refiere la afirmación, PARCIALMENTE acotado a ese grupo. Por clase, cuanto más rígida la oferta (clase 2), mayor es la parte que se traslada al precio y menor la ventaja neta del beneficiario; en la clase 1 la parte es menor, pero no nula. La capa C2 es solo del signo por grupo; la magnitud del traslado y su desglose por clase son C4 (las clases de A4 son C4) y no se promueven. |
| Límites | Sin evaluación verificada de los avales ICO ni de las ayudas españolas; la respuesta de oferta de A4 es C4; una ayuda focalizada tiene una cota superior de traslado. |
| Evidencia | output/v5/D1/incidencia_ayudas_por_clase.csv, output/v5/D1/matriz_instrumentos.csv |

## R1A-V1 · Compradores extranjeros y precio por provincia

**Afirmación:** Los compradores extranjeros encarecen la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Peso de no residentes extranjeros en las compraventas: España 9.9 % (2015) y 6.8 % (2025); por unidad en 2025 entre 0.07 % y 32.5 % (Alicante, Málaga, Baleares y Tenerife en cabeza). Sin controles, cada punto de peso inicial se asocia con 0.96 % más de subida de precio 2015-2025 (IC95 0.46 a 1.47); con renta, población, costa e islas, 0.02 % (IC95 -0.55 a 0.59; p Holm = 1). |
| Intervalo | [-0.55; 0.59] % por punto de peso (con controles, C4) |
| Cota | — (sin cota C2 de precio) |
| Literatura | NO VERIFICADA (sin DOI Crossref en esta pasada; cuartil no verificado). El resultado es una asociación transversal, no un efecto. |
| Regla del veredicto | Capa C4 (menor de sus componentes): una sola fuente efectiva por provincia (MIVAU/Notariado no independientes; Registradores sin residencia por provincia) y sin diseño de identificación; el máximo con C4 es ANALIZADA, NO CONCLUYENTE. |
| Límites | ~50 unidades, 1 corte transversal; costa e islas concentran a la vez peso de no residentes y subida de precio; con controles el coeficiente no se distingue de cero (IC95 compatible con cero y con hasta un 60 % de la bivariada); no se identifica un efecto; valor tasado ≠ precio de transacción; MIVAU cubre todas las viviendas y el Notariado solo vivienda libre (cociente Notariado/MIVAU de extranjeros por CCAA 1,04-1,24, correlación de rangos 1.00); errores robustos HC3 con pocas unidades pueden subestimar la varianza; peso de residentes extranjeros (E4) tampoco se asocia con controles. |
| Evidencia | output/v5/R1A/tablas/no_residentes_regresiones.csv, output/v5/R1A/tablas/no_residentes_peso_2015_2025.csv, output/v5/R1A/tablas/extranjeros_notariado_vs_mivau_ccaa_2025.csv, output/v5/R1A/registro.csv |

## R1B-V1 · Burbuja de precios (revisión con tamaño corregido y fundamentales)

**Afirmación:** Hay una burbuja en el precio de la vivienda en España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Con valores críticos por bootstrap de AR(p) estimado (tamaño comprobado: 4.0 % con phi=0,5 frente a 15.0 % con vc iid), el cociente precio/alquiler muestra exuberancia sin ajustar (p<0,05) en 0 de 2 medidas nacionales, pero ninguna sobrevive a BH en la familia de 8 cocientes (BH 0.211-0.937); episodios fechados sin ajuste múltiple (ninguno sobrevive a BH): . Precio frente a valor de descuento del alquiler con tipos (prima de 3 pp; sensibilidad 2 y 4 pp) y frente a la cuota hipotecaria constante sobre renta: sin exuberancia (p 0.52-0.84). CCAA con exuberancia tras BH: 0 de 34 series (M7 con vc iid: 29 de 34 con p<0,05 sin ajuste; con vc corregidos: 6). |
| Intervalo | — |
| Cota | — |
| Literatura | Phillips, Shi y Yu (2015), GSADF: NO VERIFICADA (DOI y cuartil no comprobados sin red). |
| Regla del veredicto | Una exuberancia estadística no es una burbuja: el test detecta crecimiento explosivo de una serie o de un cociente, no la causa (renta, tipos, oferta, expectativas) ni la sobrevaloración. Con capa C4 el veredicto no puede ser RESPALDADA ni CONTRADICHA. Los cocientes frente a fundamentales con tipos no muestran exuberancia, lo que no equivale a ausencia de sobrevaloración: el valor fundamental usado es una referencia simple con supuestos propios. |
| Límites | Muestra 2007Q1-2026Q2 (T=78) corta para el ciclo; ADF con un rezago; el valor de descuento fija g=2 % y una prima de 3 pp (sensibilidad 2 y 4 pp) y usa el tipo medio de nuevas hipotecas ; renta del hogar nacional; sin renta por CCAA; el tamaño con bootstrap queda en 2-4 % (por debajo del nominal) con R=200. |
| Evidencia | output/v5/R1B/tablas/gsadf_corregido.csv, output/v5/R1B/tablas/gsadf_tamano.json, output/v4/M7/tablas/gsadf_resultados.csv |

## T1-V1 · Bajas del parque

**Afirmación:** En España apenas se derriban viviendas / las bajas del parque son despreciables.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Licencias de demolición del Ministerio: 5.898-9.706 viviendas en 2024 y 6.200-7.195 de media en 2012-2024, es decir 0.026 % del parque al año (0,02-0,04 %), frente al 0,1-0,2 % supuesto antes. No incluye ruina, cambios de uso, agregaciones ni derribos sin licencia. Las identidades de Censos y Catastro dan bajas negativas (-0.3278 % y -0.1758 % al año en 2011-2020) y no acotan por arriba. |
| Intervalo | 0-0.052 % del parque al año (C4) |
| Cota | C2 solo la cota física inferior (bajas >= 0); sin cota superior medida |
| Literatura | — |
| Regla del veredicto | Una sola fuente para el nivel (licencias del Ministerio) y los métodos de stock no miden bajas: capa C4. Lo licenciado es pequeño frente al parque; el total de salidas no está medido. |
| Límites | Licencia no es derribo ejecutado; faltan ruina, cambio de uso, agregaciones y obras sin licencia; reparto provincial por parque. |
| Evidencia | output/v5_1/T1/tablas/comparacion_metodos.csv, output/v5_1/T1/tablas/licencias_demolicion_nacional.csv, output/v5_1/T1/tablas/identidad_descomposicion.csv |

## T2-V1 · Envejecimiento

**Afirmación:** El envejecimiento resolvera el problema de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Liberadas por fallecimiento y traslado a residencia: 185643 viviendas/año central (rango 93606-316859) en 2026-2035, frente a una necesidad central de 214868 viviendas/año (B1). Ya estan descontadas en la proyeccion de hogares del INE, asi que no restan necesidad. Llegan al mercado 150079/ano (70096-275008). 97 % en provincias A4 clase 1-2. |
| Intervalo | 93606 a 316859 viviendas/año (C4) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | Capa C4: parametros de residencias sin dato propio y destino de la vivienda liberada sin dato. Cifra de orden de magnitud; no se resta de la necesidad. |
| Límites | Solo 75+; reparto municipal por poblacion 65+; mortalidad 2024 constante; no contrasta la calidad ni la ubicacion de la vivienda. |
| Evidencia | output/v5_1/T2/tablas/liberadas_provincia.csv, output/v5_1/T2/resultado.json |

## T2-V2 · Herencias

**Afirmación:** Las herencias liberaran vivienda suficiente.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Herencias inscritas: 203393 viviendas/año (2023-2025, INE ETDP, fuente unica: C4). Liberadas por fallecimiento en propiedad: 118075/ano (modelo, C4). Fraccion que llega al mercado 75-87 % (supuesto C4: X entre vacias y vacias+secundarias del Censo 2021). No llegan 24548-46580 viviendas/año, un aumento posible de la necesidad efectiva de 11-22 % (prueba de estres X=50 %: 43 %). |
| Intervalo | 70096 a 275008 viviendas/año al mercado (C4) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | El dato registral de las herencias es de fuente unica (INE) y el destino posterior (venta, alquiler, uso familiar, vacia) no tiene dato: la cifra de mercado es C4 por la menor capa de sus componentes. La suficiencia depende de ese destino. |
| Límites | Una inscripcion de herencia puede incluir segundas viviendas o vacias; no hay seguimiento de la vivienda heredada. |
| Evidencia | output/v5_1/T2/tablas/liberadas_provincia.csv, data/raw/v5_1/ine_t2_t6154.csv |

## T4-V1 · Cierre del déficit

**Afirmación:** Al ritmo actual el déficit se cerrará en pocos años.

| Campo | Contenido |
|---|---|
| Veredicto | **NO RESPALDADA** |
| Capa de la evidencia | C2 |
| Magnitud | Dirección nacional 2025-2030 (C2): empeora en 180 escenarios (terminadas: ritmo actual, cartera, tendencia, mínimo y optimista; hogares bajos, central y altos; bajas 0, central y máxima de T1; liberadas que no llegan al mercado: ninguna, mín., central y máx.). Magnitud (C4): el déficit pasa de 763.416 (2025, central: media de las fuentes con y sin protegida más bajas centrales de T1; 700.934 sin bajas y con protegida) a 1.349.025 a fin de 2030 al ritmo 2023-2025 (rango de la rejilla 788.180 a 1.773.555); cambio 585.609 (rango 87.246 a 946.852). Para no empeorar harían falta unas 211.772 terminadas al año frente a 94.650 del ritmo actual y 146.435 del escenario optimista. Provincias: 15 empeoran, 0 mejoran y 37 indeterminadas (B2: 20 / 5 / 27). El déficit nacional 2025-2030 empeora en todos los escenarios de la rejilla (dirección C2); por tanto la afirmación «se cerrará en pocos años» no se sostiene en ninguno de ellos. La dirección C2 depende de que el rango plausible esté en la rejilla: unas terminadas sostenidas muy por encima del optimista o unos hogares claramente por debajo de la proyección baja del INE podrían cambiarla (umbrales en docs/v5_1/revision.md). La magnitud del aumento es C4. |
| Intervalo | cambio del déficit 2025-2030: 87.246 a 946.852 viviendas (C4); dirección nacional C2 |
| Cota | Dirección C2 solo si el signo es único en toda la rejilla; magnitud siempre C4 |
| Literatura | — |
| Regla del veredicto | Criterio T4: la dirección sube a C2 solo si el signo se mantiene en TODOS los escenarios que cubren el rango plausible de terminadas, hogares, bajas y liberadas; si no, C4. La magnitud es siempre C4 (con C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE»). Actualiza B2-V1: misma afirmación. |
| Límites | Terminadas aproximadas con libres terminadas más calificaciones definitivas de protegida; el retardo de la cartera es nacional; el escenario de 2006-2007 queda fuera del rango plausible y se informa aparte; las bajas y las liberadas son C4 de fuente única; los rangos no son intervalos de confianza. |
| Evidencia | output/v5_1/T4/tablas/recuento_por_etapas.csv, output/v5_1/T4/tablas/direccion_provincial_2030.csv, output/v5_1/T4/resultado.json |

## M4-V3 · Factores comunes a alquiler y compra

**Afirmación:** El alquiler y la compra se mueven por los mismos factores.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Variables comunes (6): pesan en ambos mercados ln_pob; solo en alquiler share_ext_pob; solo en compra ln_pib_pc (criterio: apoyo en al menos una familia o PIP>=0,5). Alquiler (stock SERPAVI) y compra (valor tasado) se comparan por separado; no hay contratos nuevos en el contraste. |
| Intervalo | Ver sintesis_variables.csv (PIP, IC de M1 y rango del multiverso por mercado) |
| Cota | — |
| Literatura | No aplica. |
| Regla del veredicto | Una coincidencia parcial de variables con apoyo debil (C4) no permite afirmar ni negar que ambos mercados compartan factores. |
| Límites | Validacion espacial nueva (11 provincias nunca usadas como validacion); temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5; el ultimo anio cae en la ventana sellada de v2. Las conclusiones se apoyan en la parte espacial. Las dos medidas tienen distinta cobertura temporal y frecuencia. |
| Evidencia | output/v6/M4/tabla_modelos.csv, output/v6/M4/mejor_modelo.csv, output/v6/M4/sintesis_variables.csv, output/v6/M4/comparacion_mercados.csv |

## M4-V4 · Ratio precio/alquiler y sobrevaloracion

**Afirmación:** La ratio precio/alquiler indica sobrevaloracion.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Ratio precio/alquiler anual (valor tasado / SERPAVI), 39 provincias de entrenamiento, 2023: mediana 17,1 anos de alquiler (rango 12,4-23,8); rentabilidad bruta mediana 5,84 %. Contraste de burbuja GSADF por CCAA: 0 de 11 con episodio explosivo (p BH<0,05). No existe un nivel de referencia identificado con el que la ratio senale sobrevaloracion. |
| Intervalo | Brecha rentabilidad menos coste de uso (g=2 %): mediana 1,56 pp, rango -0,07 a 3,79 pp |
| Cota | — |
| Literatura | No aplica. |
| Regla del veredicto | La ratio es una descripcion (C4) sin umbral de equilibrio validado; el contraste GSADF tiene pocas provincias por CCAA. |
| Límites | Validacion espacial nueva (11 provincias nunca usadas como validacion); temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5; el ultimo anio cae en la ventana sellada de v2. Las conclusiones se apoyan en la parte espacial. Las provincias selladas no entran en la ratio; precio tasado frente a alquiler de stock (no contratos nuevos). |
| Evidencia | output/v6/M1B/tablas/ratio_ult.csv, output/v6/M1B/tablas/gsadf.csv |

## K1-V1 · Predicción del precio y del alquiler

**Afirmación:** Los modelos de inteligencia artificial predicen el precio y el alquiler mejor que los métodos sencillos.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | En la validación sellada v6, el mejor modelo supera a la línea base más exigente en 6 de 9 tareas (alquiler de stock en provincia, municipio y distrito; precio de tasación trimestral y, frágil, anual; volumen trimestral espacial). Alquiler provincial: 1,61 % frente a 2,20 % (AR con factor común). |
| Intervalo | DM-HLN y permutación exacta por provincias, Holm (output/v6_1/K1/tabla_modelos_k1.md) |
| Cota | — |
| Literatura | Harvey, Leybourne y Newbold (1997) para el contraste. |
| Regla del veredicto | Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. La ventaja solo aparece en las tareas en que se supera a la base más exigente; no distinguible en precio municipal, Registradores y volumen anual. Predicción, no causalidad. |
| Límites | Segunda mirada a la muestra sellada para comparadores nuevos; 11 provincias selladas; poca potencia. |
| Evidencia | output/v6_1/K1/tabla_modelos_k1.md, output/v6_1/K1/notas.md |

## K2-V1 · Inmigración

**Afirmación:** La llegada de inmigrantes sube el precio de la vivienda o el alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Cuota de extranjeros (t-1), EF dobles, provincias de entrenamiento. Asociación TOTAL (sin controlar por población; la inmigración es un componente contable de su crecimiento): valor tasado 4,26 % por pp [2,12; 6,41], con demanda externa 1,60 [-0,79; 3,99]; alquiler de stock 2,67 [1,31; 4,04]. Asociación DIRECTA (a igual población): valor tasado -1,31 [-4,31; 1,69]. Correlación cuota-población dentro de provincia 0,66. |
| Intervalo | IC95 agrupados por provincia (output/v6_1/K2/inmigracion.md) |
| Cota | — |
| Literatura | Saiz (2007); Sá (2015): orientan el signo; ver docs/literatura.md (cuartil según marca). |
| Regla del veredicto | Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. El signo y el mercado cambian con el método (2SLS/MCO), la medida de alquiler y los controles. Controlar por población es un mal control (la población crece por la propia inmigración): el signo negativo de la asociación directa en compra no significa que la inmigración abarate la vivienda. A su vez, la total puede recoger otros factores ligados al crecimiento de la población; ninguna de las dos identifica un efecto. |
| Límites | 41 provincias de entrenamiento (sin las 11 selladas, incluidas las islas); no reproduce la muestra de 49 provincias de v2; primera etapa débil del instrumento en esta muestra. |
| Evidencia | output/v6_1/K2/inmigracion.md, output/v6_1/K2/pasos_inmigracion.csv, docs/v6_1/historial_conclusiones.md |

## L3-V1 · Déficit

**Afirmación:** Faltan cientos de miles de viviendas en España.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Déficit acumulado 2021-2024 (aumento de hogares menos viviendas terminadas), sin bajas del parque: 389.361-710.542 viviendas según la corrección del salto de la EPA en 2021 (siete alternativas más la constante de v1) y la fuente de terminadas (Ministerio o Catastro); sin las dos correcciones que conservan el salto, 596.371-710.542. Con las bajas estimadas en v5.1, 389.361-765.994 (C4; única cifra con bajas desde v7.2: el supuesto de bajas del 0,1-0,2 % se retira). 2021-2025: 523.606-887.950 (C4: terminadas de 2025 frágiles). |
| Intervalo | cota 389.361-710.542 viviendas (sin bajas) |
| Cota | C2: supuestos explícitos sobre la corrección de la EPA |
| Literatura | Banco de España (2024, 2025): estimaciones de 375.000-600.000 viviendas en periodos parecidos (output/v5/D3/convergencia.md). |
| Regla del veredicto | El signo (más hogares que viviendas terminadas) lo confirman dos fuentes de hogares y dos de terminadas en todas las variantes; la cuantía es una cota porque la amplitud entre correcciones de la EPA supera la tolerancia de C1 (±15 %). «Cientos de miles» se cumple en todas las variantes; una cifra puntual no es defendible. |
| Límites | Sin bajas del parque observadas; la EPA cambió de metodología en 2021T1; las terminadas de 2025 son frágiles. El mínimo lo fija no retirar el salto (d1) con Catastro; el máximo, trimestres vecinos (b) con Ministerio sin protegida. La regla de capa se escribió en el mismo commit que los resultados: su anterioridad no consta en git. |
| Evidencia | output/v6_2/L3/deficit_alternativas.md, output/v6_2/L3/resultado.json, output/v6_2/anexo_metodologico.md |
