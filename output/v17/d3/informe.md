Análisis a posteriori (V17). Apoyo cuantitativo a las preguntas D3 1-3. Capa C4, contable y descriptivo; sin lenguaje causal.

# V17 · D3 apoyo cuantitativo

Generado por `src/v17/d3_cuantitativo.py` (SEED 20261010). Sin red. Con la base, siempre `muestra_sellada_v6 == False`; no se lee `data/sealed`. Cada cifra tiene id `V17-D3-*` en `hechos.json`. Registro de especificaciones: `registro.csv` (Registry de `src/econ_utils.py`).

## 1. Población y hogares 2015-2025 <a id="demografia"></a>

Identidad: ΔPoblación = saldo vegetativo + residuo (saldo migratorio exterior neto + ajustes estadísticos). Población: ECP a 1 de enero, serie vigente (1-1-2026 = 49.596.376; la nota original daba 49.570.725). Saldo vegetativo: MNP microdatos hasta 2024; 2025 provisional de la nota EDeS/EMN (tabla -125.818; texto -122.167; se usa nacimientos menos defunciones). 2024: los microdatos con residencia en España dan −116.056, igual que la nota del INE (sin excluir los residentes en el extranjero, 318.005 − 436.118 = −118.113). No hay país de nacimiento de la madre en los microdatos: el saldo vegetativo «de nacidos en España» se aproxima por NACIONALIDAD (madre y fallecido). Nacidos en el extranjero: ECP t79278 (a 1-1-2025) y nota ECP 4T25 (1-1-2026, vintage distinto).

| Año (1-1 a 1-1) | ΔPoblación | Saldo vegetativo | Residuo migratorio y ajustes | Saldo exterior oficial | Δ nacidos en el extranjero | Δ nacidos en España | SV nac. española | SV nac. extranjera |
|---|---|---|---|---|---|---|---|---|
| 2015-2016 | -6.838 | -1.976 | -4.862 | 28.537 | 29.274 | -36.112 | -65.461 | 61.639 |
| 2016-2017 | 78.509 | 503 | 78.006 | 123.020 | 101.543 | -23.034 | -62.934 | 61.507 |
| 2017-2018 | 147.677 | -30.772 | 178.449 | 226.131 | 192.801 | -45.124 | -93.458 | 60.645 |
| 2018-2019 | 273.881 | -54.326 | 328.207 | 412.754 | 341.800 | -67.919 | -117.777 | 61.014 |
| 2019-2020 | 399.099 | -57.355 | 456.454 | 528.093 | 465.444 | -66.345 | -123.334 | 63.234 |
| 2020-2021 | 82.748 | -151.812 | 234.560 | 252.393 | 240.044 | -157.296 | -212.902 | 58.534 |
| 2021-2022 | 85.929 | -112.326 | 198.255 | 191.094 | 213.319 | -127.390 | -168.120 | 55.584 |
| 2022-2023 | 598.634 | -133.250 | 731.884 | 727.005 | 736.090 | -137.456 | -192.020 | 58.723 |
| 2023-2024 | 534.334 | -113.590 | 647.924 | 642.296 | 634.028 | -99.694 | -174.481 | 60.711 |
| 2024-2025 | 508.602 | -116.056 | 624.658 | 626.268 | 625.976 | -117.374 | -179.026 | 62.725 |
| 2025-2026 | 468.079 | -125.818 | 593.897 | — | 540.371 | -97.943 | — | — |

Acumulado 2015-2025: población 3.170.654; saldo vegetativo -896.778; residuo 4.067.432 (el residuo es 128 % del crecimiento). Lectura contable: el saldo vegetativo es negativo desde 2017 y el crecimiento procede del residuo migratorio. El residuo mezcla saldo exterior y ajustes (rebase censal 2021, revisiones); la columna «saldo exterior oficial» permite ver la diferencia. Qué NO se puede atribuir causalmente: por qué llegan (empleo, origen latinoamericano, reagrupación, regularizaciones), ni qué habría pasado sin ellos. Los datos locales no contienen esos motivos.

Por grandes grupos de nacionalidad (inmigración exterior anual 2015-2021 y stock 1-1) en `demografia_grupos_nacionalidad.csv`. Se descarta mostrar 2022-2025 por grupos: la serie semestral v2 acaba en 2022S1 y el EMCR 2023+ solo tiene recuentos de inmigración (140 valores no vacíos).

### Hogares: motores (reutiliza V16, `hogares_motores_2014_2026.csv`) <a id="hogares"></a>

| Periodo | Cambio de hogares | Población | Composición por nacionalidad | Estructura por edad | Jefatura (residuo; tamaño medio) |
|---|---|---|---|---|---|
| 2014-2021 (EPA) | 343.500 | 361.916 (105 %) | -41.918 | 701.278 (204 %) | -677.776 |
| 2021-2022 (ECP) | 282.880 | 31.884 (11 %) | -5.769 | 119.696 (42 %) | 137.069 |
| 2022-2023 (ECP) | 280.947 | 234.531 (83 %) | -30.736 | 72.052 (26 %) | 5.099 |
| 2023-2024 (ECP) | 211.580 | 209.923 (99 %) | -21.354 | 93.001 (44 %) | -69.990 |
| 2024-2025 (ECP) | 206.416 | 199.357 (97 %) | -21.494 | 85.426 (41 %) | -56.874 |
| 2025-2026 (ECP) | 241.013 | 182.579 (76 %) | -17.621 | 102.869 (43 %) | -26.814 |

Atribución contable ilustrativa del componente población (858.274 hogares) del cambio 2021-2026 (1.222.836): entre 724.785 y 858.274 hogares corresponden al crecimiento de la población nacida en el extranjero (o de nacionalidad extranjera), suponiendo que forman hogares como el resto (cuota del crecimiento de población: 125 % por país de nacimiento, mayor que 100 % porque la población nacida en España disminuye; 84 % por nacionalidad). Es una cota de contabilidad, no un efecto. Emancipación: no hay tasa de jefatura por edad posterior a 2021, de modo que queda dentro del residuo de jefatura (no se separa).

### Tenencia por origen (Censo 2021, muestra del 10 %, persona de mayor edad del hogar) <a id="tenencia"></a>

| Origen | Propiedad | Alquiler | Otra |
|---|---|---|---|
| Nacida en España | 80.5 % | 11.5 % | 8.1 % |
| Nacida en el extranjero | 50.6 % | 36.8 % | 12.6 % |

Por nacionalidad y año de llegada: `tenencia_por_origen_censo2021.csv`. ECEPOV 2021 no se ha usado (microdatos de 197 MB sin tabulación previa; pendiente).

## 2. ¿General o local? <a id="general-local"></a>

Cuota de la varianza de la variación anual explicada por el componente común (efecto año), con IC95 por bootstrap de provincias y referencia de azar (permutación temporal dentro de cada provincia):

| Serie | Periodo | N | T | Común (año) | IC95 | Azar | Provincia fija | Local (prov×año) |
|---|---|---|---|---|---|---|---|---|
| Valor tasado MIVAU (€/m², media anual) | 2015-2019 | 38 | 5 | 4 % | 2-12 | 2 % | 38 % | 58 % |
| Valor tasado MIVAU (€/m², media anual) | 2020-2025 | 38 | 6 | 66 % | 61-73 | 2 % | 20 % | 13 % |
| Valor tasado MIVAU (€/m², media anual) | 2015-2025 | 38 | 11 | 61 % | 55-67 | 2 % | 16 % | 24 % |
| IPV INE por CCAA (índice, media anual) | 2015-2019 | 9 | 5 | 19 % | 7-65 | 5 % | 58 % | 22 % |
| IPV INE por CCAA (índice, media anual) | 2020-2025 | 9 | 6 | 92 % | 89-96 | 10 % | 5 % | 3 % |
| IPV INE por CCAA (índice, media anual) | 2015-2025 | 9 | 11 | 81 % | 70-94 | 10 % | 8 % | 11 % |
| IPC alquiler INE provincial (índice, media anual) | 2015-2019 | 41 | 5 | 49 % | 43-59 | 2 % | 15 % | 35 % |
| IPC alquiler INE provincial (índice, media anual) | 2020-2025 | 41 | 6 | 45 % | 40-55 | 2 % | 23 % | 31 % |
| IPC alquiler INE provincial (índice, media anual) | 2015-2025 | 41 | 11 | 64 % | 59-71 | 2 % | 9 % | 26 % |
| IPVA INE provincial (índice anual) | 2015-2019 | 38 | 5 | 74 % | 68-82 | 2 % | 13 % | 13 % |
| IPVA INE provincial (índice anual) | 2020-2024 | 38 | 5 | 68 % | 58-80 | 2 % | 25 % | 7 % |
| IPVA INE provincial (índice anual) | 2015-2024 | 38 | 10 | 77 % | 70-85 | 2 % | 11 % | 12 % |
| SERPAVI alquiler €/m² mediana provincial | 2015-2019 | 38 | 5 | 76 % | 70-83 | 2 % | 7 % | 17 % |
| SERPAVI alquiler €/m² mediana provincial | 2020-2024 | 38 | 5 | 45 % | 34-60 | 2 % | 30 % | 25 % |
| SERPAVI alquiler €/m² mediana provincial | 2015-2024 | 38 | 10 | 71 % | 65-79 | 2 % | 8 % | 21 % |

Variación acumulada 2015-2024 por provincia (dispersión), `variacion_acumulada_provincial.csv`:

| Serie | N | Mediana % | P10 | P90 | Mín | Máx |
|---|---|---|---|---|---|---|
| Valor tasado MIVAU (€/m², media anual) | 38 | 11 | -2 | 31 | -10 | 61 |
| IPV INE por CCAA (índice, media anual) | 9 | 48 | 27 | 60 | 25 | 69 |
| IPC alquiler INE provincial (índice, media anual) | 41 | 9 | 5 | 13 | 2 | 20 |
| IPVA INE provincial (índice anual) | 38 | 21 | 16 | 28 | 10 | 37 |
| SERPAVI alquiler €/m² mediana provincial | 38 | 33 | 27 | 45 | 23 | 55 |

Concentración del déficit 2021-2025 (ECP y MIVAU, bajas 0; 41 provincias sin muestra sellada): 5 provincias suman la mitad del déficit positivo y 14 el 80 % (Barcelona, Valencia/València, Alicante/Alacant, Tarragona, Málaga, Almería suman 56 %); 2 provincias con déficit ≤ 0. V5 publicó para las 52 provincias: 6 para el 50 % y 18 para el 80 %. Detalle: `deficit_provincial_concentracion.csv`.

Esfuerzo: la tabla territorial de V16 (`esfuerzo_cambios`) se copia si contiene niveles territoriales (`esfuerzo_territorial_v16.csv`); no hay esfuerzo provincial propio en los datos locales. Factor europeo: no se descompone aquí (V16 ya estimó la cuota común del valor tasado: `output/v16/f2_contabilidad/precio_cuota_comun_periodo.csv`).

Corona: saldo acumulado 2015-2024 de 8 capitales con el resto de su provincia: -199.029 personas (7 capitales negativas); mayores cesiones: 08 (-103.142), 46 (-43.131), 41 (-20.105). Solo cubre movimientos entre municipios de una misma provincia; no mide el padrón de la corona. Padrón por municipio no se ha usado (no hay serie municipal anual completa en los datos locales).

Lectura (descriptiva): el cociente común/local depende de la serie; véase la tabla. Lo que sí se observa en los datos es que una parte de la varianza es local (prov×año) en todas las series y que el déficit está concentrado.

## 3. Factibilidad <a id="factibilidad"></a>

**Suelo (SIU).** No hay SIU por provincia en los datos locales (descarga 403 en V16). Se usan cifras de documento del Banco de España (Informe Anual 2025, pp. 157-158): potencial de 7 millones de viviendas en España, 1,1 millones en las seis áreas urbanas y 320.000 en sus capitales. Comparación parcial con la necesidad de V5.1 (áreas ≠ provincias): `suelo_potencial_bde_vs_necesidad.csv`.

**Producción.** Terminadas 2005-2007: media 568.684; 2024-2025: 83.700.

| Déficit inicial | Años | Producción necesaria (viv./año) | Frente a actual | Frente al boom | Empleo implícito a productividad 2007 (miles) | Ídem a productividad 2025 (miles) |
|---|---|---|---|---|---|---|
| C2/C4 1.0 (L3-DEF-2125, min) (523.606) | 5 | 257.188 | x3.07 | x0.45 | 1.199 | 4.769 |
| C2/C4 1.0 (L3-DEF-2125, min) (523.606) | 10 | 204.828 | x2.45 | x0.36 | 955 | 3.798 |
| 1.0 central (L3-DEF-2125) (705.778) | 5 | 293.623 | x3.51 | x0.52 | 1.369 | 5.445 |
| 1.0 central (L3-DEF-2125) (705.778) | 10 | 223.045 | x2.66 | x0.39 | 1.040 | 4.136 |
| BdE (Informe Anual 2025) (750.000) | 5 | 302.467 | x3.61 | x0.53 | 1.411 | 5.609 |
| BdE (Informe Anual 2025) (750.000) | 10 | 227.467 | x2.72 | x0.40 | 1.061 | 4.218 |
| 1.0 (L3-DEF-2125, max) (887.950) | 5 | 330.057 | x3.94 | x0.58 | 1.539 | 6.120 |
| 1.0 (L3-DEF-2125, max) (887.950) | 10 | 241.262 | x2.88 | x0.42 | 1.125 | 4.474 |

Supuestos: producción necesaria = D0/N + hogares nuevos anuales (INE, proyección 2026-2041: +2.184.048 hogares en 15 años = 145.603/año, lineal) + reposición 6.864/año (V5.1 T1, central; las viviendas liberadas por envejecimiento no se restan). Déficit inicial: rango de la 1.0 (L3-DEF-2125: 523.606 a 887.950; central 705.778) y la cifra del Banco de España (750.000). Escenario contable, no predicción.

Capacidad (`capacidad_construccion_boom_actual.csv`): ocupados en construcción, terminadas por ocupado y coste de la mano de obra (IMM) deflactado, frente a 2007. El enlace de CNAE-93 a CNAE-2009 usa 2008 (ver `hechos.json`). Plazos de licencias y transporte a coronas: sin datos oficiales locales (ver `docs/v17/fuentes/oferta_capacidad.md`).

## Límites
- Contabilidad y descripción: nada aquí es un efecto causal. - ECP provisional (se revisa cada trimestre); 2025 vintage mixto. - MNP: nacionalidad, no país de nacimiento de la madre. - Provincias selladas v6 excluidas de todo cálculo con la base; las cifras de V5 sobre 52 provincias se citan solo como publicadas. - SIU provincial, plazos de licencias y ECEPOV: pendientes. - Las cifras del Banco de España son de documento; la de 92.000 terminadas en 2025 solo figura en prensa (correcciones.md).
