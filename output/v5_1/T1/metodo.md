# T1 · método

Bajas del parque residencial (salidas netas), 2011-2025, en viviendas y % del parque. Cifras con fecha: INE Censo 2011 (tabla 3457), referencia 1-nov-2011; INE Censo 2021 (tabla 59525), referencia 1-ene-2021 (la fecha 2021-11-01 del manifiesto es la de publicación); MIVAU Boletín Online, tablas 3.2 (libres) y 1.6 (protegida), hasta dic-2025; Catastro estadísticas urbanas, ejercicios 2012-2025 (1-ene de cada ejercicio); MIVAU Boletín Online, licencias municipales de obra (tablas 6 y 10), serie anual 2000-2024; CCAA hasta 2022.

## (a) Identidad de stock con los Censos
Bajas = Parque_Censo2011 + Terminadas(1-nov-2011 a 31-dic-2020) - Parque_Censo2021. Tasa anual = Bajas / (ventana x Parque_2011), ventana = 9,17 años.

- Fecha de referencia: el Censo 2021 se refiere a 1-ene-2021 (el manifiesto del repositorio anota 2021-11-01, que es la fecha de publicación de la descarga). Lo corrobora que el parque MIVAU a 31-dic-2020 (26.623.708) coincide con V_TOTAL del Censo 2021. El Censo 2011 se refiere a 1-nov-2011. Ventana de terminadas: nov-dic 2011 (libres mensuales; protegida a prorrata 2/12 del año, supuesto) más 2012-2020.
- Corrección respecto a B1: B1 sumaba terminadas 2012-2021 (un año de más, 70.235 viviendas netas de la ventana correcta). Con la ventana de B1 las bajas implícitas son -687.579; con la correcta, -757.814. B1 no cambia de signo (siguen negativas).
- Definiciones: ambos Censos cuentan viviendas familiares (total = principales + no principales). Según el encargo, el Censo 2011 se obtuvo con encuesta y muestra y el 2021 con registros y Catastro (no verificado en el repositorio); esa diferencia de cobertura no se puede medir con datos del repositorio y es la causa principal admitida del residuo (se cuantifica por diferencia, no por medición). Descomposición del principal/no principal:

| concepto | Censo 2011 | Censo 2021 | variación |
|---|---|---|---|
| viviendas principales | 18.083.692 | 18.536.616 | 452.924 |
| no principales (secundarias + vacías + otras) | 7.134.844 | 8.087.092 | 952.248 |
| total | 25.218.536 | 26.623.708 | 1.405.172 |

- Terminadas: MIVAU libres (3.2) + protegidas (calificaciones definitivas, 1.6). Solo libres: bajas implícitas -895.368.

| concepto | viviendas |
|---|---|
| Δ parque Censo 2011 a Censo 2021 (viviendas familiares) | 1.405.173 |
| Terminadas MIVAU 1-nov-2011 a 31-dic-2020 (libres + protegidas, nov-dic 2011 y protegida 2011 a prorrata 2/12) | 647.359 |
| Diferencia = altas netas no explicadas por terminadas (= -bajas de la identidad) | 757.814 |
| de ellas, territorio común | 741.580 |
| de ellas, 4 provincias forales | 16.234 |
| territorio común: Δ unidades urbanas residenciales Catastro 1-ene-2012 a 1-ene-2021 menos terminadas 2012-2020 | 369.332 |
| territorio común: residuo no explicado por el Catastro (cobertura censal 2011/2021, vivienda aflorada, otras) | 372.248 |
| Sensibilidad ventana: sumar terminadas 2021 completo y quitar nov-dic 2011 (lectura B1: 2012-2021) | 70.235 |

Lectura: bajas negativas. El parque de los Censos creció 757.814 viviendas más de lo que explican las terminadas del Ministerio. Como mucho 369.332 (territorio común) se corresponden con altas catastrales sin terminadas (regularizaciones y viviendas aflorando); el resto (372.248 en territorio común y 16.234 en las cuatro provincias forales) es cobertura censal, vivienda no registrada que aflora, rehabilitaciones que recuperan viviendas, cambios de uso a vivienda o terminadas no certificadas, sin separar. Provincias con bajas implícitas negativas: 49 de 52.

## (b) Catastro
Bajas(y) = Terminadas MIVAU(y) - [UU(1-ene-y+1) - UU(1-ene-y)], UU = unidades urbanas residenciales de los municipios presentes en todos los ejercicios 2012-2025, territorio común. UU / viviendas del Censo 2021 = 0.944: no son la misma unidad, la comparación es de variaciones. Resultados anuales en tablas/bajas_nacional_B.csv y por provincia en tablas/catastro_bajas_provincia_anio.csv. Negativas en 2012-2017 (regularizaciones y actualización catastral, como en M0) y cercanas a 0 en 2018-2024, donde coincide con las terminadas por construcción de M0 (la coincidencia MIVAU-Catastro es el criterio de M0): no es una confirmación independiente de una baja pequeña. Provincias con bajas 2012-2020 negativas: 43 de 48.

## (c) Licencias de obra del Ministerio
Boletín Online, licencias municipales de obra: tabla 10 (viviendas a demoler en demolición total + viviendas suprimidas en demolición parcial) = definición estrecha; tabla 6 columna (3) (viviendas, obras de demolición total) = definición amplia. Coinciden hasta 2018; desde 2019 la amplia es mayor (9.706 frente a 5.898 en 2024) sin explicación en la fuente. Nivel provincial: no existe; hay CCAA hasta 2022, y se reparte por el parque provincial MIVAU (reparto, no medida). 2023-2024: cuota CCAA media 2019-2022; 2025: no publicado, se repite 2024 (marcado). Ceuta y Melilla: sin dato, tasa media del resto. La suma provincial es igual al total nacional (control_sumas.json). Una licencia no es un derribo ejecutado y no incluye ruina, cambios de uso ni agregaciones.

## Comparación (margen ±0,05 pp anuales, declarado antes de ver los resultados: equivale a unas 13.500 viviendas/año, el 15 % de 90.000 terminadas, la tolerancia de M0)

| método | tasa anual (%) | viviendas/año | signo |
|---|---|---|---|
| a) identidad Censo, nacional 2011-2020 | -0.328 | -82.671 | negativa |
| a) identidad Censo, territorio común | -0.339 | -80.900 | negativa |
| b) Catastro, territorio común 2012-2020 | -0.176 | -41.037 | negativa |
| c) licencias, demolición estrecha (tabla 10) 2012-2020 | 0.025 | 6.390 | positiva |
| c) licencias, demolición amplia (tabla 6) 2012-2020 | 0.025 | 6.525 | positiva |
| b) Catastro, territorio común 2019-2024 (núcleo C1 de terminadas, M0) | -0.008 | -1.969 | ≈0 (neta) |
| c) licencias demolición estrecha 2019-2024 | 0.021 | 5.713 | positiva |
| c) licencias demolición amplia 2019-2024 | 0.030 | 7.868 | positiva |

- a vs b: diferencia 0.163 pp (fuera del margen, ambas negativas). a vs c: 0.363 pp. b vs c 2012-2020: 0.200 pp. b vs c 2019-2024: 0.030 y 0.038 pp (dentro del margen, pero b es neta de altas catastrales y coincide con las terminadas por construcción de M0).
- Resultado: los métodos no coinciden en 2011-2020. Rango C4: 0 a 0.052 % del parque al año (0 es la cota física; el máximo es el máximo anual 2011-2024 de la definición amplia). Causa de la discrepancia: a y b miden altas netas no certificadas, no bajas; solo c es positiva y es fuente única.
- Capa: ningún método supera C4 como nivel de bajas. C1 requiere dos fuentes independientes con componentes C1 y aquí solo licencias miden bajas; C2 requeriría cota superior, que las identidades no dan (las altas no certificadas son un sumando desconocido, de modo que b es una cota inferior de las bajas si esas altas son >= 0).
- Contraste de tasas medias provinciales (H0: media = 0, t de una muestra, Holm): C_amplia: p_aj=4.2e-17, C_estrecha: p_aj=4.2e-17, A: p_aj=3.5e-12, B: p_aj=8.2e-08. Descriptivo; las bajas de a y b son significativamente negativas, lo que confirma que no miden bajas.

## Sustitución del supuesto de bajas en el déficit
Déficit contable = delta de hogares (ECP) - terminadas (libres + protegida) + bajas, con bajas = tasa provincial x parque MIVAU a 1 de enero de cada año (tablas/bajas_provincia.csv: tasa_min = 0, central = media de las dos definiciones de licencia 2015-2024, max = máximo anual de la definición amplia 2011-2024). Base sin bajas: A4 / M0.

| periodo | escenario | bajas acumuladas | déficit |
|---|---|---|---|
| 2021-2024 | estimada_tasa_min | 0 | 562.692 |
| 2021-2024 | estimada_tasa_central | 27.405 | 590.097 |
| 2021-2024 | supuesto_0,1% | 107.058 | 669.750 |
| 2021-2024 | supuesto_0,2% | 214.116 | 776.808 |
| 2021-2024 | estimada_tasa_max | 55.452 | 618.144 |
| 2021-2025 | estimada_tasa_min | 0 | 700.934 |
| 2021-2025 | estimada_tasa_central | 34.320 | 735.254 |
| 2021-2025 | supuesto_0,1% | 134.063 | 834.997 |
| 2021-2025 | supuesto_0,2% | 268.125 | 969.059 |
| 2021-2025 | estimada_tasa_max | 69.446 | 770.380 |

Con las bajas licenciadas el déficit 2021-2024 queda en 590.097 (rango 562.692-618.144) y el 2021-2025 en 735.254 (700.934-770.380), frente a 669.750-776.808 y 834.997-969.059 con el supuesto de 0,1-0,2 %. La capa pasa de C2 a C4 (la parte de bajas es de fuente única). El extremo del supuesto antiguo no queda respaldado por ningún método, pero tampoco refutado: ruina, cambios de uso y agregaciones no están medidos.

## Fuera de alcance / no probado
Censo 2011 de edificios en estado ruinoso, Estadística de Construcción de Edificios del INE y registros autonómicos de derribos: no probados en esta tarea.
