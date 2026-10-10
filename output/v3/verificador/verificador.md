# Verificador de afirmaciones sobre la vivienda en España (v3)

Generado por `make verificador` a partir de output/v3. Cada ficha evalúa la afirmación, no a quien la formula. Capas: C1 hechos (≥2 fuentes), C2 cotas, C3 efectos con identificación, C4 exploratorio.

| Id | Afirmación | Veredicto | Capa |
|---|---|---|---|
| V01 | Las viviendas turísticas son la causa principal de la subida del alquiler en España. | SIN EVIDENCIA SUFICIENTE | C2 |
| V02 | Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres. | SIN EVIDENCIA SUFICIENTE | C4 |
| V03 | La inmigración explica la subida de los precios y de los alquileres. | PARCIALMENTE | C2 |
| V04 | El problema de la vivienda se debe a la falta de oferta nueva y de suelo. | PARCIALMENTE | C1 |
| V05 | Faltan cientos de miles de viviendas en España. | RESPALDADA | C1 |
| V06 | Los topes al precio del alquiler bajan los alquileres. | SIN EVIDENCIA SUFICIENTE | C4 |
| V07 | Los topes al precio del alquiler reducen la oferta de vivienda en alquiler. | SIN EVIDENCIA SUFICIENTE | C4 |
| V08 | Hay millones de viviendas vacías que se podrían movilizar para resolver el problema. | PARCIALMENTE | C1 |
| V09 | La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler. | SIN EVIDENCIA SUFICIENTE | C4 |
| V10 | Bajar el ITP o el IVA de la vivienda la abarataría para los compradores. | SIN EVIDENCIA SUFICIENTE | C4 |
| V11 | Construir vivienda pública resolvería el problema de la vivienda. | PARCIALMENTE | C2 |
| V12 | Los tipos de interés explican la subida de los precios de la vivienda. | PARCIALMENTE | C2 |
| V13 | Hay una burbuja en el precio de la vivienda en España. | SIN EVIDENCIA SUFICIENTE | C4 |
| V14 | Los compradores extranjeros encarecen la vivienda en España. | SIN EVIDENCIA SUFICIENTE | C1 |

## V01 · Viviendas turísticas

**Afirmación:** Las viviendas turísticas son la causa principal de la subida del alquiler en España.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C2 |
| Magnitud | El aumento de VUT 2020M08-2024M08 equivale como máximo al 2,7 % del stock de alquiler (sustitución 1:1). El 25,0 % de la subida municipal del alquiler ocurre en municipios donde las VUT apenas crecieron. H3-1 no disponible. |
| Intervalo | desplazamiento de oferta [2,4; 2,7] % del stock |
| Cota | C2 (cantidad): ≤2,7 % del stock de alquiler. C4 (precio, condicionado a ε): ≤8,3 % con |ε_d|=0,33 y ≤2,7 % con |ε_d|=1 |
| Literatura | García-López et al. (2020) en Barcelona 2012-2016: réplica conceptual 2021-2024 NO REPLICADO (T = 0,0121 log-p por pp; propia -0,0042). MESVAL (2022): NO REPLICABLE (datos propietarios). |
| Regla del veredicto | La afirmación exige que las VUT expliquen más de la mitad de la subida nacional. Con C2 solo se acota la cantidad (desplazamiento pequeño frente al stock; una cuarta parte de la subida ocurre donde las VUT no crecieron), lo que no basta para descartarla. NO RESPALDADA solo si H3-1 alcanza C3 y su efecto implica menos de la mitad de la subida nacional; si no, SIN EVIDENCIA SUFICIENTE (las estimaciones C4 no deciden). |
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

**Afirmación:** La inmigración explica la subida de los precios y de los alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | Fracción máxima de la creación neta de hogares atribuible a hogares extranjeros: 45,2 % en 2014-2019 (rango [15,1; 45,2]); en 2014-2025 y 2020-2025 la cota con el extremo lógico (1 persona por hogar) llega al 100 % y no es informativa; en 2008-2013 el saldo extranjero neto fue negativo (cota 0,0 %). |
| Intervalo | [15,1; 45,2] % (2014-2019) |
| Cota | C2 de cantidad (hogares); las traducciones a precio son C4 condicionadas a ε. |
| Literatura | Saiz (2007), Sá (2015), González y Ortega (2013): magnitudes de calibración (no replicadas). |
| Regla del veredicto | La inmigración puede ser una parte relevante de la demanda nueva desde 2014 (cota no nula), pero la cota no es informativa en 2020-2025 con supuestos débiles y no hay diseño C3 propio; v2 (BI) la asocia al alquiler con evidencia EXPLORATORIA. No basta para «explica» ni para descartarla. |
| Límites | Medida por nacionalidad (las nacionalizaciones la sesgan a la baja); tamaño del hogar extranjero supuesto. |
| Evidencia | output/v3/PB/cotas.json#B2, output/v2/informe_v2.md |

## V04 · Oferta y suelo

**Afirmación:** El problema de la vivienda se debe a la falta de oferta nueva y de suelo.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Balance contable hogares − viviendas nuevas 2021-2025: 701.187 viviendas (rango entre fuentes [559.752; 969.059]); en 2012-2021 el signo no está determinado ([-1.015.321; 689.037]). El papel del suelo como moderador no es detectable con los datos (P-C4). |
| Intervalo | [559.752; 969.059] viviendas (2021-2025) |
| Cota | — |
| Literatura | Saiz (2010), Glaeser y Gyourko (2018): calibración; BdE (Informe Anual 2025, DOI no comprobado) ≈750 mil. |
| Regla del veredicto | El desfase entre hogares y viviendas nuevas desde 2021 es un hecho C1 compatible con la afirmación; antes de 2021 el signo no está determinado y el componente «suelo» no tiene evidencia propia. |
| Límites | Un balance contable no mide demanda insatisfecha a cualquier precio; bajas del parque supuestas. |
| Evidencia | output/v3/PA/tablas/A1_tabla_unica_periodos.csv, output/v3/POT/potencia.md#P-C4 |

## V05 · Déficit

**Afirmación:** Faltan cientos de miles de viviendas en España.

| Campo | Contenido |
|---|---|
| Veredicto | **RESPALDADA** |
| Capa de la evidencia | C1 |
| Magnitud | 2021-2025: 701.187 viviendas; rango entre fuentes [559.752; 969.059]. |
| Intervalo | [559.752; 969.059] viviendas |
| Cota | — |
| Literatura | BdE (Informe Anual 2025) ≈750 mil, dentro del rango. |
| Regla del veredicto | Todas las combinaciones de fuentes de 2021-2025 dan un balance positivo de cientos de miles (C1). |
| Límites | Depende del periodo de partida: con 2012 como base el signo no está determinado. «Faltan» se refiere al balance contable, no a una necesidad normativa. |
| Evidencia | output/v3/PA/hechos.json#A1_nacional_2021-2025 |

## V06 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler bajan los alquileres.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Topes de la Ley 11/2020 (contratos nuevos, fianzas Incasòl): -5,4 % [-7,1; -3,7], -37 €/mes [-48; -25]; validación sellada por fuente (SERPAVI, stock): -0,77 % [-1,39; -0,14]. Capa C4: falla: a, c. |
| Intervalo | ver magnitud |
| Cota | — |
| Literatura | Jofre-Monseny et al. (2023): −4,5 % renta (T2 c3); réplica propia en output/v3/C3/tabla_replicacion_jms.csv. |
| Regla del veredicto | RESPALDADA solo con C3 robusto. H3-3a queda en C4 (falla Rambachan-Roth con M̄=1 y la sensibilidad); las estimaciones C4 (fianzas, SERPAVI sellado y réplica de JMS 2023) tienen todas signo negativo, pero no se promueven de capa. |
| Límites | Un solo episodio (Cataluña 2020-2022, 16 meses); validación sellada por fuente (SERPAVI), no independiente. |
| Evidencia | output/v3/C3/resultado.json, output/v3/C3/tabla_replicacion_jms.csv |

## V07 · Topes de alquiler

**Afirmación:** Los topes al precio del alquiler reducen la oferta de vivienda en alquiler.

| Campo | Contenido |
|---|---|
| Veredicto | **SIN EVIDENCIA SUFICIENTE** |
| Capa de la evidencia | C4 |
| Magnitud | Número de contratos nuevos: -4,9 % [-9,9; 0,5] (p 0,073); validación por fuente (viviendas en alquiler declaradas, stock): -4,4 % [-6,4; -2,3]. Capa C4: falla: a, b, c. |
| Intervalo | ver magnitud |
| Cota | — |
| Literatura | Jofre-Monseny et al. (2023): −4,5 % renta (T2 c3); réplica propia en output/v3/C3/tabla_replicacion_jms.csv; −0,3 % contratos (no significativo). Diamond et al. (2019, San Francisco): calibración. |
| Regla del veredicto | RESPALDADA solo con C3 robusto. H3-3b queda en C4 (fallan pretendencias, placebo de fecha y sensibilidad); el contraste principal no es significativo (p≈0,07). |
| Límites | El número de contratos registrados no es el stock ofertado; posible desvío a temporada no observado. |
| Evidencia | output/v3/C3/resultado.json |

## V08 · Viviendas vacías

**Afirmación:** Hay millones de viviendas vacías que se podrían movilizar para resolver el problema.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C1 |
| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico). Solo [27,5; 36,0] % de ellas están en los municipios del tercil alto de presión de precios. |
| Intervalo | [27,5; 36,0] % en el tercil alto de presión |
| Cota | — |
| Literatura | — |
| Regla del veredicto | La cifra de millones es un hecho C1, pero la mayor parte no está donde sube el precio; la fracción movilizable es un supuesto (P-D). |
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
| Regla del veredicto | Con oferta poco elástica, parte de la rebaja se traslada al precio; sin estimación, no se puede cuantificar. |
| Límites | Los cambios autonómicos del ITP permitirían un diseño de diferencias (no realizado). |
| Evidencia | — |

## V11 · Vivienda pública

**Afirmación:** Construir vivienda pública resolvería el problema de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | viviendas aportadas (10 % de las vacías del tercil alto): [50.142,2; 82.698,5] viviendas; variación del esfuerzo medio nacional (10 %): [-4,5; -0,1] %; viviendas aportadas (30 % de las vacías del tercil alto): [150.426,6; 248.095,5] viviendas |
| Intervalo | ver magnitud |
| Cota | — |
| Literatura | Calibración con la literatura de P-D. |
| Regla del veredicto | Aumentar la oferta reduce la brecha en todo el rango simulado, pero «resolver» depende del volumen y del plazo; ver P-D. |
| Límites | Simulación con rangos de elasticidades; coste fiscal no cuantificado sin dato de coste. |
| Evidencia | output/v3/PD/resultados.json |

## V12 · Tipos de interés

**Afirmación:** Los tipos de interés explican la subida de los precios de la vivienda.

| Campo | Contenido |
|---|---|
| Veredicto | **PARCIALMENTE** |
| Capa de la evidencia | C2 |
| Magnitud | 2014-2021: la caída del coste de uso podría cubrir toda la subida (cota 78,0 % frente a la subida observada). 2021-2025: el coste de uso subió (cota -20,5 %), de signo contrario a la subida de precios: no puede explicarla. Sobre el alquiler no actúan directamente (supuesto). |
| Intervalo | 2014-2021 [23,5; 109,6] %; 2021-2025 [-99,8; -20,5] % |
| Cota | C2 en estado estacionario P/R = 1/uc. |
| Literatura | Poterba (1984) para el coste de uso. |
| Regla del veredicto | Compatible con 2014-2021; contradicha por el signo en 2021-2025. Respaldada solo para una parte del periodo. |
| Límites | Depende del suelo del coste de uso y de la ganancia esperada; estado estacionario. |
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
