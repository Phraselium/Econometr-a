# Verificador de afirmaciones sobre la vivienda en España (v3)

Generado por `make verificador` a partir de output/v3. Cada ficha evalúa la afirmación, no a quien la formula. Capas: C1 hechos (≥2 fuentes), C2 cotas, C3 efectos con identificación, C4 exploratorio.

| Id | Afirmación | Veredicto | Capa |
|---|---|---|---|
| V01 | Las viviendas turísticas son la causa principal de la subida del alquiler en España. | SIN EVIDENCIA SUFICIENTE | C2 |
| V02 | Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres. | SIN EVIDENCIA SUFICIENTE | C4 |
| V03 | La inmigración es la causa principal de la subida de los precios y de los alquileres (≥50 % de la subida). | SIN EVIDENCIA SUFICIENTE | C2 |
| V04 | La falta de oferta nueva y de suelo es la causa principal del problema de la vivienda (≥50 % de la subida). | SIN EVIDENCIA SUFICIENTE | C1 |
| V05 | Faltan cientos de miles de viviendas en España. | PARCIALMENTE | C1 |
| V06 | Los topes al precio del alquiler bajan los alquileres. | SIN EVIDENCIA SUFICIENTE | C4 |
| V07 | Los topes al precio del alquiler reducen la oferta de vivienda en alquiler. | SIN EVIDENCIA SUFICIENTE | C4 |
| V08 | Hay millones de viviendas vacías que se podrían movilizar para resolver el problema. | PARCIALMENTE | C1 |
| V09 | La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler. | SIN EVIDENCIA SUFICIENTE | C4 |
| V10 | Bajar el ITP o el IVA de la vivienda la abarataría para los compradores. | SIN EVIDENCIA SUFICIENTE | C4 |
| V11 | Construir vivienda pública resolvería el problema de la vivienda. | PARCIALMENTE | C2 |
| V12 | Los tipos de interés son la causa principal de la subida de los precios de la vivienda (≥50 % de la subida). | SIN EVIDENCIA SUFICIENTE | C4 |
| V13 | Hay una burbuja en el precio de la vivienda en España. | SIN EVIDENCIA SUFICIENTE | C4 |
| V14 | Los compradores extranjeros encarecen la vivienda en España. | SIN EVIDENCIA SUFICIENTE | C1 |

## V01 · Viviendas turísticas

**Afirmación:** Las viviendas turísticas son la causa principal de la subida del alquiler en España.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C2 |
| Magnitud | El aumento de VUT 2020M08-2024M08 equivale como máximo al 2,7 % del stock de alquiler (sustitución 1:1). El 25,0 % de la subida municipal del alquiler ocurre en municipios donde las VUT apenas crecieron. H3-1 (sección, efectos fijos, nacional): capa C4; entrenamiento β = 0,00026 log-p por pp de VUT, IC95 [-0,0007; 0,0013]; distritos sellados β = 0,0010 [-0,0007; 0,0028] (p 0,23). Con un aumento típico de 1,37 pp de VUT equivale a menos de +0,5 % de alquiler (C4). |
| Intervalo | desplazamiento de oferta [2,4; 2,7] % del stock |
| Cota | C2 (cantidad): ≤2,7 % del stock de alquiler. C4 (precio, condicionado a ε): ≤8,3 % con |ε_d|=0,33 y ≤2,7 % con |ε_d|=1 |
| Literatura | García-López et al. (2020), JUE, VERIFICADA, Q1, Barcelona 2012-2016: réplica conceptual 2021-2024 NO REPLICADO (T = 0,0121 log-p por pp; propia -0,0042). MESVAL-UV (2022), NO VERIFICADA (sin DOI): NO REPLICABLE (datos propietarios). |
| Regla del veredicto | Regla común (i)-(iv): «causa principal» exige ≥50 % de la subida. Solo hay cota C2 de cantidad (desplazamiento ≤2,7 % del stock de alquiler; el 25 % de la subida municipal ocurre donde las VUT apenas crecieron), que no atribuye precio; sin cota C2/C3 de precio, SIN EVIDENCIA SUFICIENTE. H3-1 y H3-2 quedaron en C4 (fallan adelanto, sensibilidad y sellado; el placebo de tratamiento pasa): sus estimaciones, con IC95 que incluye 0, no se promueven de capa. |
| Límites | Las VUT del INE no son todos los alquileres de temporada; el efecto local en barrios concretos puede ser mayor que el nacional (ver cotas por ciudad en output/v3/PB); SERPAVI es un stock que amortigua. |
| Evidencia | output/v3/PB/cotas.json#B1, output/v3/C1/resultado.json, output/v3/GL/replicacion.md |

## V02 · Grandes tenedores

**Afirmación:** Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Sin datos de titularidad por tamaño de tenedor (solicitud de transparencia al Catastro pendiente). |
| Intervalo | n/d |
| Cota | B3 en espera de datos (src/v3/ingesta_grandes_tenedores.py) |
| Literatura | Sin trabajo replicado para España con estos datos. |
| Regla del veredicto | Sin datos de la cuota de grandes tenedores no se puede acotar su contribución. |
| Límites | La ingesta está preparada; la cota se calculará con el esquema de B1 cuando lleguen los datos. |
| Evidencia | docs/v3/solicitudes_transparencia.md, output/v3/PB/grandes_tenedores.json |

## V03 · Inmigración

**Afirmación:** La inmigración es la causa principal de la subida de los precios y de los alquileres (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Fracción máxima de la creación neta de hogares atribuible a hogares extranjeros: 45,2 % en 2014-2019 (rango [15,1; 45,2]); en 2014-2025 y 2020-2025 la cota con el extremo lógico (1 persona por hogar) llega al 100 % y no es informativa; en 2008-2013 el saldo extranjero neto fue negativo (cota 0,0 %). Dato análogo al de V01: en 2014-2019 el 30,2 % de la subida del alquiler provincial ocurrió en provincias con saldo extranjero no positivo; en 2020-2025 no hay provincias así (sin dato análogo). Las traducciones a precio son C4 condicionadas a ε. |
| Intervalo | [15,1; 45,2] % de Δhogares (2014-2019) |
| Cota | C2 de cantidad (hogares); las traducciones a precio son C4 condicionadas a ε. |
| Literatura | Saiz (2007), JUE, VERIFICADA, Q1 (año no comprobado); Sá (2015), EJ, VERIFICADA, Q1; González y Ortega (2013), JRS, VERIFICADA, cuartil no verificado: magnitudes de calibración (no replicadas). |
| Regla del veredicto | Regla común (i)-(iv), la misma que V01: solo hay cota C2 de cantidad (hogares), que no atribuye precio; sin cota C2/C3 de precio ni diseño C3 propio, SIN EVIDENCIA SUFICIENTE. v2 (BI) asocia la inmigración al alquiler con evidencia EXPLORATORIA, que no entra en el veredicto. |
| Límites | Medida por nacionalidad (las nacionalizaciones la sesgan a la baja); tamaño del hogar extranjero supuesto. |
| Evidencia | output/v3/PB/cotas.json#B2, output/v3/PB/tablas/b2_no_explica_provincias.csv, output/v2/informe_v2.md |

## V04 · Oferta y suelo

**Afirmación:** La falta de oferta nueva y de suelo es la causa principal del problema de la vivienda (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Balance contable hogares − viviendas nuevas 2021-2025: 701.187 viviendas (rango entre fuentes [559.752; 969.059]); en 2012-2021 el signo no está determinado ([-1.015.321; 689.037]). El papel del suelo como moderador no es detectable con los datos (P-C4). |
| Intervalo | [559.752; 969.059] viviendas (2021-2025) |
| Cota | — |
| Literatura | Saiz (2010), QJE, VERIFICADA; Glaeser y Gyourko (2018), JEP, VERIFICADA: calibración. Banco de España, Informe Anual 2025 (DOI no comprobado): ≈750 mil. |
| Regla del veredicto | Regla común (i)-(iv), la misma que V01 y V03: el desfase hogares − viviendas nuevas desde 2021 es un hecho C1 (ver V05), pero no atribuye la subida; no hay cota C2/C3 de precio para la oferta y el moderador «suelo» no es detectable (P-C4). |
| Límites | Un balance contable no mide demanda insatisfecha a cualquier precio; bajas del parque supuestas. |
| Evidencia | output/v3/PA/tablas/A1_tabla_unica_periodos.csv, output/v3/POT/potencia.md#P-C4 |

## V05 · Déficit

**Afirmación:** Faltan cientos de miles de viviendas en España.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C1 |
| Magnitud | 2021-2025: 701.187 viviendas; rango entre fuentes [559.752; 969.059]. 2012-2021: signo no determinado ([-1.015.321; 689.037]). |
| Intervalo | [559.752; 969.059] viviendas |
| Cota | — |
| Literatura | Banco de España, Informe Anual 2025 (DOI no comprobado): ≈750 mil, dentro del rango. |
| Regla del veredicto | Criterio de periodo común a todas las fichas: una afirmación sin periodo se juzga en todas las ventanas C1 disponibles. Respaldada en 2021-2025 (todas las combinaciones dan cientos de miles, C1) y no determinada con 2012 como base: PARCIALMENTE. Las ventanas C1 se eligieron tras ver la disponibilidad de fuentes (docs/v3/limitaciones.md, 7). |
| Límites | Depende del periodo de partida: con 2012 como base el signo no está determinado. «Faltan» se refiere al balance contable, no a una necesidad normativa. |
| Evidencia | output/v3/PA/hechos.json#A1_nacional_2021-2025 |

## V06 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler bajan los alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Principal (Callaway-Sant'Anna, fianzas Incasòl, renta de los contratos nuevos): -5,4 % [-7,1; -3,7] (p 0,000). Validación sellada por fuente (SERPAVI, stock): -0,77 % [-1,39; -0,14], p_Holm 0,048. Estimadores alternativos y réplica de JMS (objetivo −4,5 %): R1 JMS -3,5 % [-4,7; -2,3] (REPLICADO); R2 JMS -4,5 % [-6,5; -2,6] (REPLICADO). Multiverso: 100 % mismo signo, 89 % significativas. Capa C4 (falla: a, c). |
| Intervalo | [-7,1; -3,7] % (principal) |
| Cota | — |
| Literatura | Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE, VERIFICADA, Q1; Diamond, McQuade y Qian (2019), AER, VERIFICADA, Q1 (calibración, San Francisco). |
| Regla del veredicto | RESPALDADA solo con C3 robusto; con capa C4 el veredicto es SIN EVIDENCIA SUFICIENTE aunque las estimaciones C4 apunten en una dirección (no se promueve de capa). |
| Límites | Un solo episodio (Cataluña, 2020Q4-2022Q1). La validación por fuente mide un stock (SERPAVI) en los mismos municipios: no es independiente y su magnitud es menor que la principal. |
| Evidencia | output/v3/C3/resultado.json, output/v3/C3/tabla_replicacion_jms.csv, output/v3/holm_v3.csv |

## V07 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler reducen la oferta de vivienda en alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Principal (Callaway-Sant'Anna, fianzas Incasòl, número de contratos nuevos): -4,9 % [-9,9; 0,5] (p 0,073). Validación sellada por fuente (SERPAVI, stock): -4,36 % [-6,37; -2,30], p_Holm 0,000. Estimadores alternativos y réplica de JMS (objetivo −0,3 % en contratos): R1 JMS 3,0 % [-0,9; 7,0] (PARCIAL); R2 JMS -2,0 % [-8,3; 4,2] (PARCIAL). Multiverso: 81 % mismo signo, 0 % significativas. Capa C4 (falla: a, b, c). |
| Intervalo | [-9,9; 0,5] % (principal) |
| Cota | — |
| Literatura | Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE, VERIFICADA, Q1; Diamond, McQuade y Qian (2019), AER, VERIFICADA, Q1 (calibración, San Francisco). |
| Regla del veredicto | RESPALDADA solo con C3 robusto; con capa C4 el veredicto es SIN EVIDENCIA SUFICIENTE aunque las estimaciones C4 apunten en una dirección (no se promueve de capa). |
| Límites | Un solo episodio (Cataluña, 2020Q4-2022Q1). La validación por fuente mide un stock (SERPAVI) en los mismos municipios: no es independiente y su magnitud es menor que la principal. |
| Evidencia | output/v3/C3/resultado.json, output/v3/C3/tabla_replicacion_jms.csv, output/v3/holm_v3.csv |

## V08 · Viviendas vacías

**Afirmación:** Hay millones de viviendas vacías que se podrían movilizar para resolver el problema.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4). Sobre los 277 municipios con dato, el 27,5-40,3 % de las vacías está en el tercil alto de presión de precios y el 20,7-28,3 % en el tercil bajo (C1, dos medidas). |
| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 municipios) |
| Cota | — |
| Literatura | — |
| Regla del veredicto | La cifra de millones es de fuente única (C4); el reparto por presión (C1) sitúa en el tercil alto entre el 27,5 % y el 40,3 %; la fracción movilizable es un supuesto (P-D). PARCIALMENTE: hay muchas vacías, pero su movilización para «resolver» no está evaluada. |
| Límites | Vacía por consumo eléctrico incluye viviendas en venta, en obras o en herencias; independencia parcial de las dos medidas. |
| Evidencia | output/v3/PA/hechos.json#A3, output/v3/PD/resultados.json |

## V09 · Seguridad jurídica

**Afirmación:** La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Sin datos de ocupaciones por municipio y periodo en las fuentes reunidas. |
| Intervalo | n/d |
| Cota | — |
| Literatura | Sin trabajo verificado incorporado. |
| Regla del veredicto | Sin medida del fenómeno ni diseño, no se puede evaluar. |
| Límites | Requeriría datos judiciales o policiales a escala municipal. |
| Evidencia | docs/v3/fuentes_fallidas.md |

## V10 · Fiscalidad

**Afirmación:** Bajar el ITP o el IVA de la vivienda la abarataría para los compradores.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Sin diseño propio; la incidencia depende de la elasticidad de la oferta (no estimada aquí). |
| Intervalo | n/d |
| Cota | — |
| Literatura | Sin trabajo de incidencia verificado incorporado. |
| Regla del veredicto | La incidencia depende de la elasticidad de la oferta: si fuera baja, parte de la rebaja podría trasladarse al precio; sin estimación no se puede cuantificar ni fijar su signo neto para el comprador. |
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

## V12 · Tipos de interés

**Afirmación:** Los tipos de interés son la causa principal de la subida de los precios de la vivienda (≥50 % de la subida).

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Con el supuesto estructural P/R = 1/coste de uso (C4): 2014-2021, Δln(1/uc) = +78,0 % (rango [23,5; 109,6] %), por encima de la subida del precio de compra; 2021-2025, Δln(1/uc) = -20,5 %, de signo contrario a la subida de precios. Sobre el alquiler no se calcula cota. |
| Intervalo | 2014-2021 [23,5; 109,6] %; 2021-2025 [-99,8; -20,5] % |
| Cota | C4: traducción a precio con un supuesto estructural (mismo estándar que la vía ε de V01 y V03). |
| Literatura | Poterba (1984), QJE, VERIFICADA, Q1 para el coste de uso. |
| Regla del veredicto | Regla común (i)-(iv), con el mismo estándar que V01 y V03: toda traducción de una cota a precio que descansa en un supuesto estructural no estimado (ε en V01/V03; P/R = 1/uc aquí) es C4 y no decide. Con ese supuesto, la afirmación sería incompatible con 2021-2025 y no descartada en 2014-2021. |
| Límites | Estado estacionario; depende del suelo del coste de uso y de la ganancia esperada. |
| Evidencia | output/v3/PB/cotas.json#B4 |

## V13 · Burbuja

**Afirmación:** Hay una burbuja en el precio de la vivienda en España.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Precio/renta 2023: [3,0; 4,1] veces la renta anual; la dirección de la razón precio/alquiler 2015-2024 no está establecida (medidas de signo contrario: [-9,3; 43,9] %). |
| Intervalo | n/d |
| Cota | — |
| Literatura | Sin test de exuberancia (GSADF) realizado en v3. |
| Regla del veredicto | Sin test de exuberancia y con indicadores de valoración contradictorios, no se puede afirmar ni descartar. |
| Límites | El test GSADF por CCAA estaba previsto en P-E (exploratorio) y no se ejecutó. |
| Evidencia | output/v3/PA/hechos.json#A4, output/v3/PA/hechos.json#A6 |

## V14 · Compradores extranjeros

**Afirmación:** Los compradores extranjeros encarecen la vivienda en España.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Cuota de compraventas por personas de nacionalidad extranjera 2023-2025: [9,6; 15,0] % (MIVAU 9,6-11,0 %; Registradores 13,8-15,0 %). Su efecto sobre el precio no se ha estimado. |
| Intervalo | [9,6; 15,0] % de las compraventas |
| Cota | — |
| Literatura | v2 (BV): sin efecto identificado. |
| Regla del veredicto | Hay un hecho C1 sobre su peso, pero ningún diseño sobre su efecto en el precio. |
| Límites | La cuota incluye residentes extranjeros; la de no residentes es menor y se concentra en zonas costeras. |
| Evidencia | data/processed (nacional_q_v2 vía holdout.load_full) |
