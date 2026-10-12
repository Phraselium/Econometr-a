# Cifras publicables (v6.2, L5)

Generado por src/v6_2/l5_publicables.py desde output/v5/cifras_clave.csv; no editar a mano. Toda cifra se cita con su rango, periodo, fuente, fecha del dato y capa.

## Aptas para difusión (C1 o cota C2)

| id | Indicador | Valor (rango) | Capa | Periodo | Fecha del dato | Fuentes | Cómo citarla |
|---|---|---|---|---|---|---|---|
| dh_2125 | Aumento del número de hogares | 997.586 hogares (981.823-1.013.350 hogares) | C1 | 2021-2025 | 2025T1 | INE ECP y EPA (sin corrección: los dos extremos son posteriores a la ruptura de 2021; ventanas distintas: stock a 1 de enero en la ECP y media anual en la EPA, v7.1 K4b-dh) | Citar con periodo y las dos fuentes (ECP y EPA). |
| terminadas_1924 | Viviendas terminadas al año (territorio común: sin País Vasco ni Navarra) | 72.264-94.426 viviendas/año | C1 | 2019-2024 | 2024 | Ministerio (fin de obra) y Catastro (altas), dentro de ±15 % | Rango anual del territorio común; no extrapolar a País Vasco y Navarra. |
| L3-DEF-2124-SINBAJAS | Déficit acumulado 2021-2024 sin bajas (todas las variantes de corrección EPA y de terminadas) | 389.361-710.542 viviendas | C2 | 2021-2024 | 2024T4 | hogares: EPA (varias correcciones) y ECP; terminadas: MIVAU y Catastro | Es una cota: citar siempre el rango completo, nunca un punto ni el extremo alto solo. |
| A23-P2 | Precio de compra, núcleo MIVAU/Notariado/Registradores 2015-2025 | 47,2 % (44,2-56,1 %) | C1 | 2015-2025 (media anual) | 2025 (anual) | MIVAU valor tasado; Notariado CGN; Registradores opendata | Variación del precio de compra con tres fuentes; no confundir con el IPV del INE. |
| A23-A2 | Alquiler stock 2015-2024: núcleo IPC de alquiler e IPVA (contratos existentes y total; tolerancia ±15 % en nivel) | 10,9-22,9 % | C1 | 2015-2024 | 2024 | INE IPC (encuesta); INE IPVA (datos tributarios AEAT) | Alquiler de contratos vigentes; no es el alquiler de los contratos nuevos. |
| A23-A10 | Contratos nuevos Comunitat Valenciana 2021-2024: IPVA nuevo y fianzas GVA | 28,5 % (26,1-30,8 %) | C1 | 2021-2024 | 2024 | INE IPVA (AEAT); GVA fianzas | Contratos nuevos, solo Comunitat Valenciana; no generalizar a España. |
| A23-A9 | Contratos nuevos Cataluña 2021-2024: IPVA nuevo e Incasòl | 16,9 % (16,6-17,2 %) | C1 | 2021-2024 | 2024 | INE IPVA (AEAT); Incasòl | Contratos nuevos, solo Cataluña. |
| E-B1-F | Crecimiento de hogares proyectado (componente F, 10 años) | 1.308.531-1.772.410 hogares | C2 | 2026-2035 | 2026 | INE Proyección de Hogares (tabla 54562) | Proyección del INE (C2), no previsión del autor. |
| R1C-001 | Hogares con vivienda principal en propiedad | 74,5 % de hogares (72,1-75,9 % de hogares) | C1 | 2021-2022 | 2021-11 (Censo) / 2022 (EFF, ECV) | BdE EFF; INE ECV; INE Censo 2021 | Hogares propietarios de su vivienda principal. |

## No citar fuera de contexto (C4 o dependientes de supuestos)

| id | Indicador | Valor (rango) | Capa | Periodo | Fecha del dato | Fuentes | Cómo citarla |
|---|---|---|---|---|---|---|---|
| L3-DEF-2124-CONBAJAS | Déficit acumulado 2021-2024 con bajas supuestas 0,1-0,2 % anual (cota) | 389.361-924.658 viviendas | C2 | 2021-2024 | 2024T4 | ídem, con bajas supuestas | Depende de bajas supuestas del parque. |
| T3-H5b | Necesidad anual de vivienda 2026-2035, base sin la sensibilidad X (A+R+V+F-M-K; no resta liberadas) | 210.424 viviendas/año (99.388-292.083 viviendas/año) | C4 | 2026-2035 | 2025 (ECP y MIVAU); proyección INE 54562 de 2026-06-17 | B1; T1 | Necesidad anual: contabilidad con supuestos (C4); citar el rango y la definición A+R+V+F−M−K. |
| T3-H5 | Necesidad anual de vivienda 2026-2035 recalculada (A+R+V+F-M-K+X; no resta liberadas) | 245.989 viviendas/año (123.936-338.663 viviendas/año) | C4 | 2026-2035 | 2025 (ECP y MIVAU); proyección INE 54562 de 2026-06-17 | B1; T1; T2; A4 | Necesidad con sensibilidad X (C4). |
| B1-H1 | Necesidad total de vivienda por año (A+R+V+F-M-K), suma de 52 provincias | 214.868 viviendas/año (93.628-309.921 viviendas/año) | C4 | 2026-2035 | 2026-10-10 (descarga); INE proyecciones 2026-06; Censo 2021-11; MIVAU/Catastro hasta 2025 | A4/M1; INE 54562; Censo 2021; MIVAU; Catastro | Versión v5 de la necesidad; sustituida por T3 en el titular. |
| D1-H11 | Parte de una ayuda general que se traslada al precio, clase A4 1 (método A) | 58,4 % (27,8-81,8 %) | C4 | rejilla εd 0,3-1,5 | 2026-10-10 | output/v5/A4; output/v3/PD; literatura verificada | Traslado a precio en una rejilla de elasticidades supuestas: no es una estimación. |
| D1-H12 | Parte de una ayuda general que se traslada al precio, clase A4 2 (método A) | 100,0 % (88,1-100,0 %) | C4 | rejilla εd 0,3-1,5 | 2026-10-10 | output/v5/A4; output/v3/PD; literatura verificada | Ídem. |
| K2-CUOTA-COMPRA-SINPOB-SIN | Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, sin controles (sin poblacion) y sin demanda externa | 4,3 % por pp (2,1-6,4 % por pp) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | 2026-10-11 | output/v6_1/K2/registro_holm.csv; output/v6/M0/paneles/prov_compra_anual_train.csv.gz | Inmigración, asociación total (C4): no es un efecto. |
| K2-CUOTA-COMPRA-SIN | Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, con nucleo de controles (poblacion incluida), sin controles de demanda externa | -1,3 % por pp (-4,3 a 1,7 % por pp) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | 2026-10-11 | output/v6_1/K2/registro_holm.csv; output/v6/M0/paneles/prov_compra_anual_train.csv.gz | Inmigración, asociación directa a igual población (mal control): el signo negativo no implica que abarate. |
| K1-N-MEJOR | Tareas en que el mejor modelo predice mejor que la base mas exigente (DM-HLN y permutacion, Holm, grupo espacial) | 6 tareas | C4 | validacion sellada v6 | 2026-10-11 | output/v6_1/K1/tabla_modelos_k1.csv | Predicción, no causalidad; solo frente a la base más exigente. |
| latente_convivencia | Demanda latente de jóvenes por convivencia con los padres (frente a 2008) | 188.000-506.000 hogares | C2 | 2008-2025 | 2025 | INE EPA y ECV (tasa de convivencia con los padres) | Demanda latente: cota con supuestos sobre preferencias. |
| B4-v3-vut-cantidad | Máximo de stock de alquiler desplazado por viviendas turísticas | 2,4-2,7 % del stock de alquiler | C2 | 2020M08-2024M08 | 2024-08 | v3 PB (INE VUT, Censo 2021) | Cota máxima del stock desplazado por viviendas turísticas; no es el efecto en el precio. |
| L3-DEF-2124-BAJAST1 | Déficit acumulado 2021-2024 con las bajas del parque estimadas en v5.1 (T1), todas las variantes | 654.646 viviendas (389.361-765.994 viviendas) | C4 | 2021-2024 | 2024T4 | ídem, con bajas estimadas en v5.1 (T1) | Con bajas estimadas en v5.1 (C4). |
| L3-DEF-2124-SENS | Sensibilidad: déficit 2021-2024 sin bajas sin las dos variantes que conservan el salto de la EPA (a y d1) | 596.371-710.542 viviendas | C2 | 2021-2024 | 2024T4 | ídem, sin variantes a y d1 | Sensibilidad del déficit: citarla junto al rango completo, nunca sola. |

## Históricas: no citar (sustituidas; ver ERRATA.md)

| id | Indicador | Valor (rango) | Capa | Periodo | Fecha del dato | Fuentes | Cómo citarla |
|---|---|---|---|---|---|---|---|
| deficit_2124_c1 | Déficit acumulado: aumento de hogares menos viviendas terminadas, sin bajas | 562.692-688.692 viviendas | C1 | 2021-2024 | 2024 | hogares: ECP y EPA corregida; terminadas: Ministerio y Catastro | Sustituida en v6.2 por L3-DEF-2124-SINBAJAS. No citar. |
| deficit_2124_c2 | Déficit acumulado con bajas del parque supuestas del 0,1-0,2 % anual (cota) | 562.692-902.808 viviendas | C2 | 2021-2024 | 2024 | ídem, con bajas supuestas | Sustituida en v6.2 por L3-DEF-2124-CONBAJAS. No citar. |
| T3-H2 | Déficit acumulado con las bajas estimadas de T1 (4 fuentes x tasa 0 / central / máx.) | 653.097 viviendas (562.692-744.144 viviendas) | C4 | 2021-2024 | 2024 | T1; M0; Licencias de demolición MIVAU | Sustituida en v6.2 por L3-DEF-2124-BAJAST1. No citar. |
