# M0 · Viviendas terminadas al año 2012-2025: triangulación

Umbral de coincidencia declarado: |diferencia| ≤ 15% en el año entre dos fuentes independientes. Alineación del Catastro fijada antes de mirar el resultado: variación del stock de unidades urbanas residenciales de 1 de enero del año y a 1 de enero de y+1, con los municipios presentes en todos los años (7.593 en 2012; 7.610 desde 2019).

## Independencia de las fuentes
- MIVAU fin de obra mensual y MIVAU v2 anual son la misma tabla 3.2 (diferencia máxima anual 0): una sola fuente, no dos.
- Calificaciones definitivas de protegida (tabla 1.6): es otro registro del Ministerio, pero mide la calificación y no la finalización; se suma a las libres para tener un bruto comparable. Misma fuente administrativa.
- Δ parque MIVAU: estimación del propio Ministerio, cuya metodología no consta en el repo. Mediana de |Δparque − bruto|/bruto = 1.4% en 2021-2025 (casi idéntica a las terminadas) y 163% en 2012-2020 (muy superior, a la par del Catastro). Se trata como NO independiente y como segundo método discrepante antes de 2021, que se reporta pero no se usa para promover.
- Banco de España: data/raw/bde_* contiene precios de tasación, crédito y tipos; NO hay serie de viviendas terminadas. La única cifra del BdE es 92.000 en 2025 (Informe Anual, vía output/f4). Frente a 80.792 libres + 12.858 protegida = 93.650 (−1,8 %) es consistente con la serie del Ministerio, pero el BdE no nombra la fuente: no se cuenta como independiente.
- Catastro: registro fiscal con otro proceso de alta (declaraciones y regularizaciones). Es independiente solo en parte: el alta catastral de obra nueva suele apoyarse en la escritura de obra nueva o la declaración de alteración, que exigen el certificado final de obra, documento de origen común con MIVAU aunque el proceso administrativo sea distinto. Cubre régimen común (sin País Vasco ni Navarra); la comparación usa las demás comunidades del MIVAU. Su variación de stock es neta por construcción (altas menos bajas, con regularizaciones); MIVAU es flujo bruto, y la coincidencia puede deberse a que las regularizaciones compensen las bajas.

## Resultado anual (territorio común, sin País Vasco ni Navarra)

| año | MIVAU libres+prot | Catastro ΔUU | dif Catastro | Δparque | capa | rango |
|---|---|---|---|---|---|---|
| 2012 | 121.958 | 147.465 | +20.9% | 207.386 | C4 | 121.958-147.465 |
| 2013 | 52.191 | 135.727 | +160.1% | 141.144 | C4 | 52.191-135.727 |
| 2014 | 43.904 | 131.158 | +198.7% | 134.668 | C4 | 43.904-131.158 |
| 2015 | 42.941 | 119.940 | +179.3% | 133.914 | C4 | 42.941-119.940 |
| 2016 | 39.905 | 102.035 | +155.7% | 121.784 | C4 | 39.905-102.035 |
| 2017 | 49.416 | 89.191 | +80.5% | 129.923 | C4 | 49.416-89.191 |
| 2018 | 58.032 | 51.016 | -12.1% | 135.904 | C4 (rango, C1 frágil) | 51.016-58.032 |
| 2019 | 72.264 | 72.009 | -0.4% | 140.187 | C1 | 72.009-72.264 |
| 2020 | 81.496 | 82.898 | +1.7% | 152.547 | C1 | 81.496-82.898 |
| 2021 | 87.741 | 87.241 | -0.6% | 89.009 | C1 | 87.241-87.741 |
| 2022 | 82.361 | 92.345 | +12.1% | 84.543 | C1 | 82.361-92.345 |
| 2023 | 82.847 | 87.337 | +5.4% | 83.969 | C1 | 82.847-87.337 |
| 2024 | 94.426 | 91.121 | -3.5% | 95.517 | C1 | 91.121-94.426 |
| 2025 | 87.390 | 100.453 | +14.9% | 88.343 | C4 (rango, C1 frágil) | 87.390-100.453 |

## Acumulados

| periodo | MIVAU bruto | Catastro | dif Catastro | Δparque | dif Δparque |
|---|---|---|---|---|---|
| 2012-2025 | 996.872 | 1.389.936 | +39.4% | 1.738.838 | +74.4% |
| 2021-2025 | 434.765 | 458.497 | +5.5% | 441.381 | +1.5% |
| 2012-2020 | 562.107 | 931.439 | +65.7% | 1.297.457 | +130.8% |

## Cifra nacional (MIVAU, libres + calificaciones definitivas)

| año | libres | protegida | bruto |
|---|---|---|---|
| 2012 | 80.083 | 53.332 | 133.415 |
| 2013 | 43.230 | 17.059 | 60.289 |
| 2014 | 35.382 | 15.046 | 50.428 |
| 2015 | 41.541 | 7.931 | 49.472 |
| 2016 | 37.512 | 7.118 | 44.630 |
| 2017 | 49.336 | 4.938 | 54.274 |
| 2018 | 58.853 | 5.191 | 64.044 |
| 2019 | 71.562 | 7.248 | 78.810 |
| 2020 | 77.531 | 9.973 | 87.504 |
| 2021 | 84.091 | 10.637 | 94.728 |
| 2022 | 79.935 | 9.610 | 89.545 |
| 2023 | 80.473 | 8.847 | 89.320 |
| 2024 | 86.609 | 14.371 | 100.980 |
| 2025 | 80.792 | 12.858 | 93.650 |

## Veredicto
- Años con MIVAU y Catastro (independientes solo en parte) dentro de ±15%: 8 de 14 (2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025). C1 solo el núcleo 2019-2024 (presente en las tres alineaciones), con el rango MIVAU-Catastro de la tabla; 2018 y 2025 quedan en C4 con rango y la salvedad de C1 frágil (cerca del umbral; salen con otras alineaciones); el resto en C4. Con ±10 % coinciden: 2019, 2020, 2021, 2023, 2024.
- Reglas aplicadas: un año es C1 solo si Catastro y MIVAU coinciden; no se promociona ningún año por la coincidencia de Δparque, que no es independiente. Sensibilidad a la alineación: con rezago de un año en el Catastro coinciden 7 años (2012, 2019, 2020, 2021, 2022, 2023, 2024); con todos los municipios (no constantes), 7 (2018, 2019, 2020, 2021, 2022, 2023, 2024).
- 2012-2017: MIVAU (libres + protegida) es entre 1,2 y 3 veces menor que el Catastro y el Δparque; el Catastro en esos años incorpora altas por regularización y actualización, y MIVAU puede infraregistrar certificados. Los dos métodos discrepan y no se resuelve: C4. 2018 (−12,1 %) y 2025 (+14,9 %) están cerca del umbral. Rango C1 2018-2025 en territorio común; no cubre País Vasco ni Navarra.
- Cifra nacional 2024: 86.609 libres + 14.371 protegida = 100.980, la cifra que v1 marcó como NO VERIFICADA (prensa); se reproduce con MIVAU, pero es la misma fuente, no una verificación independiente. 2025: 93.650 (BdE ≈ 92.000).
- La serie MIVAU de libres se usa sola en las cifras de v1 y v3 ; aquí solo se promociona lo que supera el contraste con el Catastro. Las diferencias no se resuelven: el Catastro mide variación neta con regularizaciones, MIVAU mide certificados de fin de obra.
