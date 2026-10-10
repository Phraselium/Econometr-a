# Verificador de afirmaciones sobre la vivienda en España (v4)

Generado por `make verificador`. Cada ficha evalúa la afirmación, no a quien la formula. Capas: C1 hechos (≥2 fuentes), C2 cotas, C3 efectos con identificación, C4 exploratorio. Veredictos: RESPALDADA, PARCIALMENTE, NO RESPALDADA, CONTRADICHA, ANALIZADA, NO CONCLUYENTE y NO ANALIZADA: FALTAN DATOS. Las fichas con cota de precio muestran su veredicto bajo las dos convenciones de traducción a precio.

| Id | Afirmación | Veredicto (convención A) | Capa |
|---|---|---|---|
| V01 | Las viviendas turísticas son la causa principal de la subida del alquiler en España. | ANALIZADA, NO CONCLUYENTE | C2 |
| V02 | Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres. | NO ANALIZADA: FALTAN DATOS | C4 |
| V03 | La inmigración es la causa principal de la subida de los precios y de los alquileres (≥50 % de la subida). | ANALIZADA, NO CONCLUYENTE | C2 |
| V04 | La falta de oferta nueva y de suelo es la causa principal del problema de la vivienda (≥50 % de la subida). | ANALIZADA, NO CONCLUYENTE | C1 |
| V05 | Faltan cientos de miles de viviendas en España. | PARCIALMENTE | C1 |
| V06 | Los topes al precio del alquiler bajan los alquileres. | ANALIZADA, NO CONCLUYENTE | C4 |
| V07 | Los topes al precio del alquiler reducen la oferta de vivienda en alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |
| V08 | Hay millones de viviendas vacías que se podrían movilizar para resolver el problema. | ANALIZADA, NO CONCLUYENTE | C4 |
| V09 | La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler. | NO ANALIZADA: FALTAN DATOS | C4 |
| V10 | Bajar el ITP o el IVA de la vivienda la abarataría para los compradores. | NO ANALIZADA: FALTAN DATOS | C4 |
| V11 | Construir vivienda pública resolvería el problema de la vivienda. | PARCIALMENTE | C2 |
| V12 | Los tipos de interés son la causa principal de la subida de los precios de la vivienda (≥50 % de la subida). | ANALIZADA, NO CONCLUYENTE | C4 |
| M3-V1 | Hay suelo de sobra para construir. | ANALIZADA, NO CONCLUYENTE | C4 |
| M4-V1 | Los compradores extranjeros encarecen la vivienda en España. | ANALIZADA, NO CONCLUYENTE | C4 |
| M4-V2 | Las empresas dominan el mercado del alquiler. | NO ANALIZADA: FALTAN DATOS | C4 |
| M4-V3 | Hay muchas viviendas vacías o de uso esporádico frente a las turísticas. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V1 | Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda. | PARCIALMENTE | C2 |
| M5-V2 | Faltan viviendas en toda España. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V3 | Los hogares crecen por la inmigración. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V4 | Limitar las compras de no residentes bajaría los precios de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |
| M5-V5 | Bajar los impuestos a la construcción abarataría la vivienda. | NO ANALIZADA: FALTAN DATOS | C4 |
| M7-V1 | Hay una burbuja en el precio de la vivienda en España. | ANALIZADA, NO CONCLUYENTE | C4 |

## V01 · Viviendas turísticas

**Afirmación:** Las viviendas turísticas son la causa principal de la subida del alquiler en España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C2 |
| Magnitud | El aumento de VUT 2020M08-2024M08 equivale como máximo al 2,7 % del stock de alquiler (sustitución 1:1). El 25,0 % de la subida municipal del alquiler ocurre en municipios donde las VUT apenas crecieron. H3-1 (sección, efectos fijos, nacional): capa C4; entrenamiento β = 0,00026 log-p por pp de VUT, IC95 [-0,0007; 0,0013]; distritos sellados β = 0,0010 [-0,0007; 0,0028] (p 0,23). Con un aumento típico de 1,37 pp de VUT equivale a menos de +0,5 % de alquiler (C4). |
| Intervalo | desplazamiento de oferta [2,4; 2,7] % del stock |
| Cota | C2 (cantidad): ≤2,7 % del stock de alquiler. C4 (precio, condicionado a ε): ≤8,3 % con |ε_d|=0,33 y ≤2,7 % con |ε_d|=1 |
| Literatura | García-López et al. (2020), JUE, VERIFICADA, Q1, Barcelona 2012-2016: réplica conceptual 2021-2024 NO REPLICADO (T = 0,0121 log-p por pp; propia -0,0042). MESVAL-UV (2022), NO VERIFICADA (sin DOI): NO REPLICABLE (datos propietarios). |
| Regla del veredicto | Regla común (i)-(iv): «causa principal» exige ≥50 % de la subida. Solo hay cota C2 de cantidad (desplazamiento ≤2,7 % del stock de alquiler; el 25 % de la subida municipal ocurre donde las VUT apenas crecieron), que no atribuye precio; sin cota C2/C3 de precio, SIN EVIDENCIA SUFICIENTE. H3-1 y H3-2 quedaron en C4 (fallan adelanto, sensibilidad y sellado; el placebo de tratamiento pasa): sus estimaciones, con IC95 que incluye 0, no se promueven de capa. v4: Hay cotas C2 de cantidad, cotas de precio C4 y un diseño (H3-1, C4); ninguno decide. |
| Límites | Las VUT del INE no son todos los alquileres de temporada; el efecto local en barrios concretos puede ser mayor que el nacional (ver cotas por ciudad en output/v3/PB); SERPAVI es un stock que amortigua. |
| Evidencia | output/v3/PB/cotas.json#B1, output/v3/C1/resultado.json, output/v3/GL/replicacion.md |
| Convención A (estricta: traducción a precio en C4) | ANALIZADA, NO CONCLUYENTE |
| Convención B (estructural: traducción a precio como C2) | ANALIZADA, NO CONCLUYENTE. Con |ε_d| = 0,33 la cota de precio es ≤8,3 % de alquiler frente a una subida observada del 6,3 % (IPC de alquiler 2020-2024): la cota supera el 100 % de la subida (133 %) y no excluye la afirmación; con |ε_d| = 1 la cota es 2,7 % (44 % de la subida), y quedaría NO RESPALDADA. |

## V02 · Grandes tenedores

**Afirmación:** Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Sin datos de titularidad por tamaño de tenedor (solicitud de transparencia al Catastro pendiente). |
| Intervalo | n/d |
| Cota | B3 en espera de datos (src/v3/ingesta_grandes_tenedores.py) |
| Literatura | Sin trabajo replicado para España con estos datos. |
| Regla del veredicto | Sin datos de la cuota de grandes tenedores no se puede acotar su contribución. v4: Faltan datos de titularidad por tamaño de tenedor (solicitud al Catastro pendiente). |
| Límites | La ingesta está preparada; la cota se calculará con el esquema de B1 cuando lleguen los datos. |
| Evidencia | docs/v3/solicitudes_transparencia.md, output/v3/PB/grandes_tenedores.json |

## V03 · Inmigración

**Afirmación:** La inmigración es la causa principal de la subida de los precios y de los alquileres (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Fracción máxima de la creación neta de hogares atribuible a hogares extranjeros: 45,2 % en 2014-2019 (rango [15,1; 45,2]); en 2014-2025 y 2020-2025 la cota con el extremo lógico (1 persona por hogar) llega al 100 % y no es informativa; en 2008-2013 el saldo extranjero neto fue negativo (cota 0,0 %). Dato análogo al de V01: en 2014-2019 el 30,2 % de la subida del alquiler provincial ocurrió en provincias con saldo extranjero no positivo; en 2020-2025 no hay provincias así (sin dato análogo). Las traducciones a precio son C4 condicionadas a ε. |
| Intervalo | [15,1; 45,2] % de Δhogares (2014-2019) |
| Cota | C2 de cantidad (hogares); las traducciones a precio son C4 condicionadas a ε. |
| Literatura | Saiz (2007), JUE, VERIFICADA, Q1 (año no comprobado); Sá (2015), EJ, VERIFICADA, Q1; González y Ortega (2013), JRS, VERIFICADA, cuartil no verificado: magnitudes de calibración (no replicadas). |
| Regla del veredicto | Regla común (i)-(iv), la misma que V01: solo hay cota C2 de cantidad (hogares), que no atribuye precio; sin cota C2/C3 de precio ni diseño C3 propio, SIN EVIDENCIA SUFICIENTE. v2 (BI) asocia la inmigración al alquiler con evidencia EXPLORATORIA, que no entra en el veredicto. v4: Hay cotas C2 de hogares (M2 la amplía) y traducciones a precio C4; ninguna decide. |
| Límites | Medida por nacionalidad (las nacionalizaciones la sesgan a la baja); tamaño del hogar extranjero supuesto. |
| Evidencia | output/v3/PB/cotas.json#B2, output/v3/PB/tablas/b2_no_explica_provincias.csv, output/v2/informe_v2.md |
| Convención A (estricta: traducción a precio en C4) | ANALIZADA, NO CONCLUYENTE |
| Convención B (estructural: traducción a precio como C2) | ANALIZADA, NO CONCLUYENTE. Compra 2014-2025: cota de precio ≤26,3 % frente a una subida observada de ≈33-34 % según la ponderación (≈78-79 % de la subida): no excluye la afirmación; alquiler: cota no informativa (227 %). |

## V04 · Oferta y suelo

**Afirmación:** La falta de oferta nueva y de suelo es la causa principal del problema de la vivienda (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Balance contable hogares − viviendas nuevas 2021-2025: 701.187 viviendas (rango entre fuentes [559.752; 969.059]); en 2012-2021 el signo no está determinado ([-1.015.321; 689.037]). El papel del suelo como moderador no es detectable con los datos (P-C4). v4 (M0): déficit 2021-2024 sin bajas = [562.692; 688.692] viviendas (C1: todos los componentes medidos con dos fuentes); con bajas supuestas del 0,1-0,2 % anual, hasta 902.808 (C2). La cifra 2021-2025 de v3 queda en C4 porque las terminadas de 2025 son frágiles. |
| Intervalo | [559.752; 969.059] viviendas (2021-2025) |
| Cota | — |
| Literatura | Saiz (2010), QJE, VERIFICADA; Glaeser y Gyourko (2018), JEP, VERIFICADA: calibración. Banco de España, Informe Anual 2025 (NO VERIFICADA: DOI no comprobado): ≈750 mil. |
| Regla del veredicto | Regla común (i)-(iv), la misma que V01 y V03: el desfase hogares − viviendas nuevas desde 2021 es un hecho C1 (ver V05), pero no atribuye la subida; no hay cota C2/C3 de precio para la oferta y el moderador «suelo» no es detectable (P-C4). v4: Hay hechos C1 de balance hogares-viviendas (M1) sin atribución de precio; el suelo no es detectable (P-C4). |
| Límites | Un balance contable no mide demanda insatisfecha a cualquier precio; bajas del parque supuestas. |
| Evidencia | output/v3/PA/tablas/A1_tabla_unica_periodos.csv, output/v3/POT/potencia.md#P-C4 |

## V05 · Déficit

**Afirmación:** Faltan cientos de miles de viviendas en España.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C1 |
| Magnitud | 2021-2025: 701.187 viviendas; rango entre fuentes [559.752; 969.059]. 2012-2021: signo no determinado ([-1.015.321; 689.037]). v4 (M0): déficit 2021-2024 sin bajas = [562.692; 688.692] viviendas (C1: todos los componentes medidos con dos fuentes); con bajas supuestas del 0,1-0,2 % anual, hasta 902.808 (C2). La cifra 2021-2025 de v3 queda en C4 porque las terminadas de 2025 son frágiles. |
| Intervalo | [559.752; 969.059] viviendas |
| Cota | — |
| Literatura | Banco de España, Informe Anual 2025 (NO VERIFICADA: DOI no comprobado): ≈750 mil, dentro del rango. |
| Regla del veredicto | Criterio de periodo común a todas las fichas: una afirmación sin periodo se juzga en todas las ventanas C1 disponibles. Respaldada en 2021-2025 (todas las combinaciones dan cientos de miles, C1) y no determinada con 2012 como base: PARCIALMENTE. Las ventanas C1 se eligieron tras ver la disponibilidad de fuentes (docs/v3/limitaciones.md, 7). |
| Límites | Depende del periodo de partida: con 2012 como base el signo no está determinado. «Faltan» se refiere al balance contable, no a una necesidad normativa. |
| Evidencia | output/v3/PA/hechos.json#A1_nacional_2021-2025 |

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

## V09 · Seguridad jurídica

**Afirmación:** La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Sin datos de ocupaciones por municipio y periodo en las fuentes reunidas. |
| Intervalo | n/d |
| Cota | — |
| Literatura | Sin trabajo verificado incorporado. |
| Regla del veredicto | Sin medida del fenómeno ni diseño, no se puede evaluar. v4: Faltan datos de ocupaciones ilegales por municipio y periodo (judiciales o policiales). |
| Límites | Requeriría datos judiciales o policiales a escala municipal. |
| Evidencia | docs/v3/fuentes_fallidas.md |

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

## V12 · Tipos de interés

**Afirmación:** Los tipos de interés son la causa principal de la subida de los precios de la vivienda (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Con el supuesto estructural P/R = 1/coste de uso (C4): 2014-2021, Δln(1/uc) = +78,0 % (rango [23,5; 109,6] %), por encima de la subida del precio de compra; 2021-2025, Δln(1/uc) = -20,5 %, de signo contrario a la subida de precios. Sobre el alquiler no se calcula cota. |
| Intervalo | 2014-2021 [23,5; 109,6] %; 2021-2025 [-99,8; -20,5] % |
| Cota | C4: traducción a precio con un supuesto estructural (mismo estándar que la vía ε de V01 y V03). |
| Literatura | Poterba (1984), QJE, VERIFICADA, Q1 para el coste de uso. |
| Regla del veredicto | Regla común (i)-(iv), con el mismo estándar que V01 y V03: toda traducción de una cota a precio que descansa en un supuesto estructural no estimado (ε en V01/V03; P/R = 1/uc aquí) es C4 y no decide. Con ese supuesto, la afirmación sería incompatible con 2021-2025 y no descartada en 2014-2021. v4: Cota B4 analizada; con la convención A la traducción a precio es C4. |
| Límites | Estado estacionario; depende del suelo del coste de uso y de la ganancia esperada. |
| Evidencia | output/v3/PB/cotas.json#B4 |
| Convención A (estricta: traducción a precio en C4) | ANALIZADA, NO CONCLUYENTE |
| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Con P/R = 1/uc: incompatible con 2021-2025 (signo contrario) y no descartada en 2014-2021 (la cota supera la subida observada). |

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

## M4-V1 · Compradores extranjeros (sustituye a V14)

**Afirmación:** Los compradores extranjeros encarecen la vivienda en España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Definición única: comprador extranjero según MIVAU (residentes + no residentes). Peso en las compraventas: MIVAU 16,9 % en 2025 (residentes 10,1 %, no residentes 6,8 %); Notariado, vivienda libre, 18,8 % en 2025 (residentes 11,6 %, no residentes 7,2 %); Registradores 13,8-15,0 % en 2023-2025. El 9,6-11,0 % de V14 (v3) contaba solo residentes extranjeros (en 2025, 10,1 % con MIVAU); V14 queda sustituida por esta ficha. El efecto sobre el precio no se ha estimado. |
| Intervalo | [13,8; 18,8] % de las compraventas (rango entre fuentes, por definiciones distintas) |
| Cota | — (sin cota C2 de precio) |
| Literatura | v2 (BV): sin efecto identificado. Referencia NO VERIFICADA (sin DOI Crossref; cuartil no verificado). El peso es un hecho descriptivo, no un efecto. |
| Regla del veredicto | Capa C4 (la menor de sus componentes): MIVAU y Notariado no se tratan como independientes y Registradores difiere más de 15 %; no hay diseño ni cota C2 sobre el efecto en el precio. Con C4 el veredicto máximo es ANALIZADA, NO CONCLUYENTE. |
| Límites | Independencia: MIVAU elabora su estadística, según la revisión, con datos del Notariado (no verificado en la web en esta pasada; se trata como no independiente). Registradores mide la inscripción (desfase respecto a la escritura) y su 13,8-15,0 % queda 3,6 puntos de media por debajo de MIVAU (correlación provincial 0,99). Definiciones: nacionalidad frente a residencia y trato del NIE no coinciden entre fuentes; Notariado cubre vivienda libre, MIVAU todas las viviendas, Registradores compraventas de vivienda registradas. Registradores no separa residentes de no residentes. Costa e islas: lista del analista, que incluye Barcelona, Valencia y Málaga (sensibilidad en extranjeros_concentracion_sensibilidad.csv). La concentración en costa e islas es un hecho descriptivo; no implica efecto. |
| Evidencia | output/v4/M4/tablas/extranjeros_evolucion_nacional.csv, output/v4/M4/tablas/extranjeros_provincias_2023_2025.csv, output/v4/M4/tablas/extranjeros_concentracion_zonas.csv |

## M4-V2 · Empresas en el mercado del alquiler

**Afirmación:** Las empresas dominan el mercado del alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **NO ANALIZADA: FALTAN DATOS** |
| Capa de la evidencia | C4 |
| Magnitud | Flujo: las personas jurídicas son el 11,3 % de los compradores y el 24,7 % de los vendedores en las compraventas de vivienda (2024, INE ETDP; fuente única). Stock de viviendas en alquiler por tipo de titular y contratos nuevos por tipo de arrendador: sin dato. |
| Intervalo | — |
| Cota | — |
| Literatura | No revisada en esta ficha. |
| Regla del veredicto | Faltan titularidad (Catastro no publica titulares por tipo), arrendador en las fianzas de Incasòl y tipo de arrendador en el Censo. La cuota de compra no mide el alquiler. |
| Límites | El único dato por tipo de persona es de compraventas (ETDP, del Registro de la Propiedad), no de alquiler ni de stock; capa C4. Las ventas de personas jurídicas incluyen promotores (obra nueva) y entidades financieras: el porcentaje de vendedores no mide empresas propietarias de stock ni desinversión de tenedores. |
| Evidencia | output/v4/M4/tablas/flujo_compraventas_comprador_pj_etdp.csv, output/v4/M4/tablas/tenencia_censo2021.csv, output/v4/M4/tablas/flujo_alquiler_incasol_contratos.csv |

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

## M5-V1 · Ayudas a la demanda

**Afirmación:** Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Signo (C2, estable en la rejilla de P-D: oferta η ∈ {0; 0,45; 1,75}, demanda 0,3-1,5): el beneficiario paga lo mismo o menos en neto (nada menos con oferta totalmente rígida) y los no beneficiarios pagan más. Magnitud (C4): entre el 15 % y el 100 % de una ayuda general por unidad se traslada al precio; para una ayuda focalizada en jóvenes es una cota superior, escalada por su peso en la demanda. Los avales relajan la restricción de entrada y no son una ayuda por unidad: su traducción es más incierta. |
| Intervalo | 15-100 % de una ayuda general al precio (C4) |
| Cota | C2 de signo por grupo; magnitud C4 |
| Literatura | Gibbons y Manning (2006), JPubE, VERIFICADA, cuartil no verificado: 60-67 % de incidencia en arrendadores; Carozzi, Hilber y Yu (2024), JUE, VERIFICADA, Q1 (referencia cualitativa para avales: precio al alza sin más construcción con oferta rígida). |
| Regla del veredicto | Regla común con V11 (revisión C, C5): si el signo es estable en la rejilla (C2) para el grupo al que se refiere la afirmación, PARCIALMENTE acotado a ese grupo; la magnitud es C4. Abarata (o no encarece) para el beneficiario y encarece para los no beneficiarios; «abaratar el acceso de los jóvenes» en conjunto depende de la magnitud, no establecida. |
| Límites | Sin evaluación verificada de los avales ICO ni de las ayudas españolas. |
| Evidencia | output/v4/M5/tablas/incidencia_ayudas_demanda.csv |
| Convención A (estricta: traducción a precio en C4) | PARCIALMENTE (signo por grupo, C2) |
| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE: misma conclusión con la magnitud también como cota. |

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

## M7-V1 · Burbuja de precios

**Afirmación:** Hay una burbuja en el precio de la vivienda en España.

| Campo | Contenido |
|---|---|
| Veredicto | **ANALIZADA, NO CONCLUYENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Precio de compra 2015-2025: dirección C1 (positiva); cuantía: núcleo MIVAU_tasado, Notariado, Registradores +44 % a +56 % (cuantía C1), discrepante: INE_IPV (rango total +44 % a +80 %). 2021-2025: núcleo +24 % a +36 %, rango total +24 % a +36 %. GSADF nacional precio/alquiler: exuberancia (BH 5 %, ambos métodos) en 2 de 2 medidas; CCAA con exuberancia en ambas medidas: 5 de 17; episodios nacionales: 2011Q4-2013Q3;2017Q2-2019Q3;2024Q2-2026Q2; 2017Q4-2019Q2;2024Q4-2026Q2. |
| Intervalo | [44; 56] % de variación 2015-2025 (núcleo de cuantía) |
| Cota | — |
| Literatura | Phillips, Shi y Yu (2015), GSADF: NO VERIFICADA (DOI y cuartil no comprobados sin red). |
| Regla del veredicto | Hay exuberancia estadística en el ratio precio/alquiler (episodios fechados con BSADF), pero un test de exuberancia no separa una burbuja de cambios en los fundamentos (renta, tipos de interés, oferta) ni mide la sobrevaloración. Con capa C4 el veredicto no puede ser RESPALDADA ni CONTRADICHA. |
| Límites | Sobre-rechazo moderado con Δy autocorrelacionada (tamaño 12,7 % con phi=0,5, vc al 5 %). El test detecta comportamiento explosivo de la serie, no una burbuja: no identifica si el precio se separa de los fundamentos. Ratios con índices rebasados (nivel de la ratio arbitrario); ADF con un rezago; valores críticos por simulación de paseo aleatorio (principal) y wild bootstrap (499 réplicas; más exigente si la muestra ya contiene tramos explosivos); muestra 2007-2026 corta para el ciclo. Precio/renta solo nacional; sin renta trimestral por CCAA. Verificación con series simuladas: superada. |
| Evidencia | output/v4/M7/tablas/gsadf_resultados.csv, output/v4/M7/tablas/variacion_precio.csv, data/processed (nacional_q_v2 vía holdout.load_full) |
