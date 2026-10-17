# Auditoría de datos V15 · Renta y microdatos (fase 1.2, capa C4, DESCRIPTIVO)

Script: `src/v15/auditoria/renta_microdatos.py` (SEED=20261010, sin red, solo lectura; base con `NOT coalesce(muestra_sellada_v6,false)`). Cruces por código INE (sección a municipio = 5 primeros dígitos). Sin efectos estimados. De AEAT solo salen agregados propios (razones, recuentos, correlaciones); del Censo, nada con n < 10; de la ECV, solo recuentos. Tablas CSV en esta carpeta.

## 1. AEAT 2013-2015: dictamen NO UTILIZABLE como renta en euros (reescalado no aplicable)

- La tabla cruda de 2013-2015 (55 conceptos) no es la de 2016-2024 (57-61): le faltan NÚMERO DE DECLARACIONES, RENTA BRUTA MEDIA y RENTA DISPONIBLE MEDIA, y solo un nombre de concepto coincide (cuota de autoliquidación). Mediana global de los valores: ~480 (2013-2015) frente a ~11.000 (2016).
- Razones por municipio (317 municipios) entre ejercicios consecutivos: dentro de 2013-2015 y dentro de 2016-2024 tienen mediana de 0,76 a 1,10 (74-100 % de municipios entre 0,5 y 2); en 2015/2016 caen a 5e-5 (trabajo), 1,3e-4 (actividades), 3e-4 (ganancias y cuota), 8e-4 (inmuebles) y 1,6e-3 (capital mobiliario), con 0 % entre 0,5 y 2. No son una sola potencia de 10 (un factor euros/miles de euros daría 1e-3 en todos): no se reescala.
- Los valores de 2015 son compatibles con recuentos de declarantes por concepto: dividen por el NÚMERO DE DECLARACIONES de 2016 entre 0,11 (ganancias) y 0,80 (trabajo), siempre ≤ 1,2 en el 100 % de los municipios. Es una inferencia; el HTML original no está en el repositorio. `src/v11/fetch_aeat_irpf_municipios.py` solo conserva la primera columna numérica de cada informe, de modo que importes y medias de 2013-2015 pudieron descartarse.
- Por qué la base empieza en 2016: `src/v11/base_v11.py` selecciona conceptos por nombre (RENTA BRUTA MEDIA, NÚMERO DE DECLARACIONES, etc.) y esos nombres no existen antes de 2016. La explicación de docs/v11/auditoria_exhaustividad.md («València figura desde 2016») no se sostiene en el crudo: 46250 está en 2013-2015. Quedan dos municipios solo en 2015 (03085, 12096).
- 2016-2024 está en euros: importe de RENTA BRUTA ÷ declaraciones ÷ RENTA BRUTA MEDIA = 1,000 en todos los ejercicios (p05 = p95 = 1). Disponible/bruta: 0,69-0,91, nunca mayor que 1. Mediana de la renta bruta media: 19.857 € (2016) a 26.465 € (2024).
- Utilizable: 2013-2015 solo como recuento de declarantes por concepto tras comprobarlo; nunca como importe. Pendiente: nueva descarga con todas las columnas (tareas_autor).

## 2. Atípicos (|z robusto| > 5)

- AEAT (324 municipios, 2016-2024): renta bruta media 14 en nivel y 69 en variación interanual (corte transversal), 45 en las series municipales; disponible 16 y 66. Los mayores son picos y reversión en municipios pequeños (+119 % y −93 % al año siguiente; ±70 % en 2023-2024): candidatos a error de un ejercicio o a pocas declaraciones, no a fallo de unidades. Rangos: bruta 13.396-69.313 €.
- ADRH (36.317 secciones, 2019-2023): 0 en nivel; en variación, 1.213 secciones en renta por persona (486 en 2019→2020, 332 en 2020→2022, 395 en 2022→2023), 1.236 por hogar y 362 en Gini. Rango persona 4.053-36.918 €; hogar/persona 1,3-7,6 (mediana 2,5; una sección fuera de 1-6). Gini 19,7-45,2.

## 3. Coherencia AEAT renta bruta media frente a ADRH (CV, municipio, media simple de secciones)

- Niveles (log, 318-324 municipios): correlación 0,57-0,83 con ADRH persona o hogar; la mejor, con hogar 2020 (0,83) y la peor en 2019 (0,59 con persona). AEAT bruta ≈ 2,0 × ADRH neta por persona y ≈ 0,8 × neta por hogar: definiciones distintas (declarante frente a persona, bruta frente a neta), no un problema de unidades.
- Tasas: la correlación entre variaciones es de −0,61 (2019→2020), −0,09 a −0,25 (2020→2022) y ≈ 0 (2022→2023). Con la AEAT un ejercicio antes, 2019→2020 pasa a +0,68, indicio de desfase de año de referencia no resuelto (en los demás pares baja a 0,12-0,23). ADRH 2022→2023 crece 7,4 % frente a 3,9 % de la AEAT. Conclusión: AEAT y ADRH sirven como niveles, no como tasas intercambiables.
- ECV (personas con dato, 2018-2025): esfuerzo del alquiler 4.382 → 8.856 (hogares 1.650 → 3.642); sobrecarga 33.692 → 71.161. Por origen en 2025 (esfuerzo): española 4.876, fuera de la UE 1.499, UE 464. Por edad 2025: 18-34 1.961; 35-49 2.595; 50-64 1.554; 65+ 714. Recuentos completos en `ecv_n_por_anio_grupo.csv`.

## 4. Rupturas

- ADRH: la base solo tiene 2019, 2020, 2022 y 2023 (falta 2021; en el crudo hay un servicio de 2021 con campos etiquetados por orden, supuesto). Secciones: 36.317 (2019 y 2020), 36.382 (2021), 36.462 (2022), 36.477 (2023): salen 74-127 y entran 89-207 códigos por año; 100-178 municipios cambian de número de secciones. Sin tabla de relaciones no se puede enlazar una sección escindida o fusionada. En los códigos que persisten, la variación mediana es parecida en municipios con y sin cambio de número de secciones (4,7 % frente a 4,5 % en 2020→2021; |Δ| > 20 %: 0,4-0,8 %): no hay ruptura detectable en los códigos estables, pero no se puede excluir una ruptura en códigos reutilizados.
- ECV: el tamaño de muestra salta en 2021 (hogares 15.043 → 21.007, ×1,40) y sigue creciendo hasta 29.779 (2024); los pesos suman 46,2-48,7 millones sin saltos (≤ 1,9 %). Hasta 2020 la nacionalidad solo existe para adultos (16-18 % de personas sin dato) y el país de nacimiento no existe (100 % ausente); desde 2021 ambos están completos. El cambio de marco a la base del Censo en 2021 no consta en docs/: se reportan solo estas señales de los datos.
- EPA: 34 trimestres (2018T1-2026T2), sin huecos, con diseño de registro 2021-(…). La EPA no recoge tenencia ni gasto en vivienda (como indica b6_condiciones.py): no sirve para P8.

## 5. P8: tamaños muestrales (umbral n ≥ 200 hogares por celda)

- ECV por año (2025), esfuerzo del alquiler: viable origen (3 celdas) y origen × tenencia; origen × edad 7 de 12, origen × quintil 7 de 15, tres cruces o más ≤ 12 de 60. Agrupando 2023-2025: origen × edad 10 de 12, origen × quintil 11 de 15, origen × edad × quintil 26 de 60; el cruce de cuatro dimensiones no es viable (26 de 60 en alquiler y 87 de 238 en sobrecarga, con celdas de n < 10). Sobrecarga (todas las tenencias) 2023-2025: origen × edad (12 de 12), origen × tenencia (12 de 12) y origen × quintil (15 de 15) son viables.
- Censo 2021 (muestra 10 %): nacionalidad × edad × tenencia, 24 de 24 celdas ≥ 200; llegada, 29 de 30; con tipo de hogar, 157 de 192. No trae renta ni gasto: no permite el cruce por renta. En la base, c21md tiene 759 municipios y 1.468.378 hogares frente a 909 y 1.853.662 del crudo (diferencia sin explicar aquí).
- ECEPOV 2021 (172.444 viviendas; 21.050 alquiladas, todas con pago e ingreso en intervalos): sí permite esfuerzo por intervalos de ingreso; alquiler × nacionalidad × edad × ingreso, 26 de 32 celdas ≥ 200. Un solo año y códigos NAC sin decodificar.

## Implicaciones y límites

Para P8: usar ECV agrupada 2023-2025 con origen × edad × tenencia (esfuerzo 10 de 12 celdas, sobrecarga 34 de 48) y, con renta, solo cruces de dos dimensiones (origen × quintil 11 de 15; origen × edad × quintil solo 26 de 60), avisando de las celdas bajo 200; ECEPOV y Censo solo como contraste de 2021; la AEAT 2013-2015 no entra. Límites: ADRH agregado por media simple de secciones; municipios AEAT = Comunitat Valenciana (> 1.000 hab.); umbrales (|z| > 5, n ≥ 200, n ≥ 10) fijados aquí por convención.
