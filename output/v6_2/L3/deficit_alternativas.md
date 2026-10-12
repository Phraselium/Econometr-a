# L3 · Déficit 2021-2024 y 2021-2025 bajo correcciones alternativas del salto EPA 2021T1

Respuesta a la objeción A-01 del informe del árbitro. Datos: INE EPA (2020T4-2025T4) y ECP (2021T1-2025T4); MIVAU terminadas; Catastro (1-ene de cada ejercicio); bajas v5.1 T1.

## Regla de decisión (declarada ANTES de mirar los resultados finales)

1. Universo: todas las variantes de hogares (v1 constante, a, b, b4, c, d1, d2, e) cruzadas con todas las terminadas
   (MIVAU con y sin protegida; Catastro completado), SIN bajas.
2. Amplitud relativa = (máx - mín) / (máx + mín), es decir, semiamplitud sobre el punto medio. Estrecho: amplitud <= 15 % (tolerancia C1 del proyecto).
3. Independencia: hay >= 2 fuentes independientes si (i) hogares: EPA y ECP coinciden dentro de +-15 % en el cambio de hogares
   con la corrección que se elija, y (ii) terminadas: MIVAU y Catastro (territorio común) coinciden dentro de +-15 % en 2021-2024.
   Se declara que la EPA corregida con una constante o con un supuesto no es una medida independiente de la ECP en el salto.
4. Si 1-3 se cumplen: se mantiene C1 con el rango completo (nuevo mín-máx de todas las variantes sin bajas).
   Si no: C2 (cota con supuestos explícitos: la corrección del salto y la fuente de terminadas).
5. Con bajas supuestas (0,1 y 0,2 %) o estimadas (v5.1 T1): C2 como mucho (el supuesto de bajas no es un hecho). Capa final = la menor de sus componentes.
6. 2021-2025: misma regla, y capa = la menor de sus componentes (la terminadas 2025 es C4 frágil en M0).

## Variantes de hogares

### Cambio de hogares hasta 2024T4 (viviendas)

| variante | fuente | cambio de hogares | descripción |
|---|---|---|---|
| v1_constante | EPA | 1.019.800 | EPA + constante 242.400 (criterio v1) |
| a_sin_correccion | EPA | 777.400 | EPA 2020T4-fin sin retirar el salto |
| b_vecinos2 | EPA | 1.041.650 | variación 2021T1 = media de 2020T4 y 2021T2 |
| b4_vecinos4 | EPA | 1.037.775 | variación 2021T1 = media de 2020T3, T4, 2021T2, T3 |
| c_variacion_cero | EPA | 985.200 | variación 2021T1 = 0 |
| d1_enlace_cociente | EPA+ECP | 774.813 | EPA 2020T4 x (ECP/EPA en 2021T1); conserva el salto en escala ECP |
| d2_enlace_ecp_retropolada | ECP | 999.548 | ECP con nivel 2020T4 retropolado con la variación media de 2020 (ventana completa) |
| e_ecp | ECP | 981.823 | ECP 1-ene-2021 a 1-ene del año siguiente al final (2021T1 a (fin+1)T1) |

### Cambio de hogares hasta 2025T4 (viviendas)

| variante | fuente | cambio de hogares | descripción |
|---|---|---|---|
| v1_constante | EPA | 1.278.000 | EPA + constante 242.400 (criterio v1) |
| a_sin_correccion | EPA | 1.035.600 | EPA 2020T4-fin sin retirar el salto |
| b_vecinos2 | EPA | 1.299.850 | variación 2021T1 = media de 2020T4 y 2021T2 |
| b4_vecinos4 | EPA | 1.295.975 | variación 2021T1 = media de 2020T3, T4, 2021T2, T3 |
| c_variacion_cero | EPA | 1.243.400 | variación 2021T1 = 0 |
| d1_enlace_cociente | EPA+ECP | 1.015.826 | EPA 2020T4 x (ECP/EPA en 2021T1); conserva el salto en escala ECP |
| d2_enlace_ecp_retropolada | ECP | 1.240.561 | ECP con nivel 2020T4 retropolado con la variación media de 2020 (ventana completa) |
| e_ecp | ECP | 1.222.836 | ECP 1-ene-2021 a 1-ene del año siguiente al final (2021T1 a (fin+1)T1) |

Censo 2021 como ancla: no hay una cifra nacional de hogares del Censo versionada en data/raw; la ECP ya está rebasada sobre el Censo 2021, de modo que no añade una medida independiente del cambio de hogares.

## Resultados sin bajas

| periodo | mín | máx | punto medio | amplitud rel. | EPA vs ECP (máx. dif.) | Catastro vs MIVAU común | >=2 fuentes | capa |
|---|---|---|---|---|---|---|---|---|
| 2021-2024 | 389.361 | 710.542 | 549.952 | 29.2 % | 5.9 % | 3.1 % | sí | C2 |
| 2021-2025 | 523.606 | 887.950 | 705.778 | 25.8 % | 6.1 % | 5.4 % | sí | C4 |

Rango sin bajas por variante de hogares (mín-máx entre las 3 fuentes de terminadas):

| variante | 2021-2024 | 2021-2025 |
|---|---|---|
| v1_constante | 634.348 - 688.692 | 785.780 - 866.100 |
| a_sin_correccion | 391.948 - 446.292 | 543.380 - 623.700 |
| b_vecinos2 | 656.198 - 710.542 | 807.630 - 887.950 |
| b4_vecinos4 | 652.323 - 706.667 | 803.755 - 884.075 |
| c_variacion_cero | 599.748 - 654.092 | 751.180 - 831.500 |
| d1_enlace_cociente | 389.361 - 443.705 | 523.606 - 603.926 |
| d2_enlace_ecp_retropolada | 614.096 - 668.440 | 748.341 - 828.661 |
| e_ecp | 596.371 - 650.715 | 730.616 - 810.936 |

Rango sin bajas por fuente de terminadas (mín-máx entre variantes de hogares):

| terminadas | 2021-2024 | 2021-2025 |
|---|---|---|
| MIVAU_con_protegida | 400.240 - 667.077 | 547.603 - 831.627 |
| MIVAU_sin_protegida | 443.705 - 710.542 | 603.926 - 887.950 |
| Catastro_completado | 389.361 - 656.198 | 523.606 - 807.630 |

Terminadas acumuladas (viviendas): 2021-2024: MIVAU_con_protegida 374.573, MIVAU_sin_protegida 331.108, Catastro_completado 385.452; 2021-2025: MIVAU_con_protegida 468.223, MIVAU_sin_protegida 411.900, Catastro_completado 492.220.

Catastro completado = unidades urbanas residenciales de territorio común + (MIVAU nacional - MIVAU común) para País Vasco y Navarra; no es una fuente totalmente independiente. Las unidades urbanas no son viviendas (ratio 0,944 respecto al Censo 2021).

## Con bajas

Bajas supuestas 0,1 y 0,2 % anual del parque del año anterior; bajas estimadas de v5.1 T1 (C4, fuente única de licencias y catastro): 2021-2024: v5.1_min 0, v5.1_central 27.405, v5.1_max 55.452; 2021-2025: v5.1_min 0, v5.1_central 34.320, v5.1_max 69.446.

| periodo | mín con bajas (cualquier escenario) | máx con supuestos 0,1-0,2 % | máx con cualquier escenario |
|---|---|---|---|
| 2021-2024 | 389.361 | 924.658 | 924.658 |
| 2021-2025 | 523.606 | 1.156.075 | 1.156.075 |

## Aplicación de la regla

- Amplitud relativa 2021-2024 sin bajas: 29.2 % (umbral 15 %): NO cumple.
- EPA corregida vs ECP: máxima diferencia 5.9 %; Catastro vs MIVAU (común, 2021-2024): 3.1 %.
- Capa final 2021-2024 sin bajas: **C2**, rango 389.361-710.542 viviendas. Con bajas supuestas: **C2**, 389.361-924.658.
- 2021-2025: 523.606-887.950 sin bajas, capa C4 (la terminadas 2025 es C4 frágil en M0; no se promueve).

Sensibilidad (posterior a la regla, no la sustituye): sin las variantes a y d1, que conservan el quiebre metodológico de la EPA, el rango 2021-2024 sin bajas es 596.371-710.542 (amplitud 8.7 %). La regla pre-declarada incluía todas las variantes; la capa C2 se mantiene. Lo que decide es qué variantes se aceptan, es decir, un supuesto sobre el salto.

Tabla completa: deficit_alternativas.csv (288 filas).

Nota: d1 conserva el salto (la razón ECP/EPA alinea el nivel posterior, no el anterior) y es el extremo bajo; se reporta junto con d2, que usa la ECP con ventana completa.
