# Informe de política de vivienda (v3), con módulo València

Este documento presenta los resultados del proyecto v3 para quienes diseñan o evalúan políticas de vivienda. No recomienda opciones por preferencia: indica qué medidas mejoran el acceso en todo el rango de supuestos simulado y cuáles dependen de supuestos inciertos. Cada cifra lleva su capa de evidencia (C1 hecho, C2 cota, C3 efecto identificado, C4 exploratorio). Ningún efecto alcanzó C3.

## 1. Diagnóstico
- [C1] Balance hogares − viviendas nuevas en 2021-2025: +701.000 viviendas (rango 560.000-969.000). El signo depende del año de partida: con 2012 como base no está determinado.
- [C1] Emancipación: viven con sus padres el 40,3-50,2 % de las personas de 25-34 años. La propiedad entre los hogares de menos de 35 años es del 30,7-31,8 % (2022), entre 24,2 y 34,0 puntos menos que en 2008.
- [C1] Esfuerzo: el precio de 80 m² equivale a 3,0-4,1 años de renta media del hogar (2023).
- [C1] Vacías: en las muestras municipales con dato (277 a 1.806 municipios según la definición de presión), el 27,5-40,3 % está en el tercil alto de presión de precios y el 20,7-28,3 % en el tercil bajo.
- [C4, fuente única] El Censo 2021 estima 3,8 millones de viviendas vacías. Se terminaron 89.000-101.000 viviendas al año en 2021-2025 (certificados de fin de obra del MIVAU).

## 2. Qué dice la evidencia sobre cada palanca

| Palanca | Resultado | Capa | ¿Depende de supuestos? |
|---|---|---|---|
| Más oferta (construcción) | 104.000-413.000 viviendas/año para estabilizar el esfuerzo en 2026-2035; +25.000 a +100.000 viviendas/año reducen el esfuerzo en toda la rejilla | C2 | No en el signo; sí en la magnitud; costes no modelados |
| Movilizar vacías donde hay presión | El 10-30 % de las vacías del tercil alto aporta 50.000-248.000 viviendas, el 4,6-51 % de la brecha | C2 | El porcentaje movilizable es un supuesto; coste sin cuantificar |
| Vivienda pública | Reduce el esfuerzo si no desplaza construcción privada; efecto nulo con desplazamiento total | C2 (dominancia débil) | Sí: grado de desplazamiento y coste unitario |
| Regulación de viviendas turísticas | Retirarlas todas en las secciones de mayor peso de 6 ciudades devolvería como máximo unas 31.000 viviendas; variación asociada (C4) del alquiler local de −2,0 % a +0,5 % con H3-1 sellado (mayor con calibraciones no replicadas) | C2 en cantidad, C4 en precio | Sí: signo no estable |
| Topes de alquiler | Asociación de −5,4 % en la renta de los contratos nuevos (Cataluña, 2020-2022); contratos −4,9 % [−9,9; +0,5]; esfuerzo medio de los inquilinos de −2,9 % a +7,3 % según la respuesta de la oferta | C4 | Sí: el signo depende de la reducción de contratos |
| Tipos de interés | Con P/R = 1/coste de uso: compatible con la subida de 2014-2021; signo contrario en 2021-2025 | C4 (supuesto estructural) | Depende del suelo del coste de uso |

Lectura:
- Signo estable en toda la rejilla, en sentido estricto: construcción y movilización de vacías donde hay presión.
- Signo estable solo débilmente (≤ 0, nulo si desplaza a la construcción privada): vivienda pública.
- Signo no estable: retirada de viviendas turísticas y topes. Pueden mejorar o empeorar el acceso según parámetros que los datos actuales no fijan.

La simulación no incluye costes (fiscales, de suelo, de movilización ni pérdidas de los propietarios). La ordenación no es una evaluación coste-beneficio.

## 3. Lo que falta para decidir mejor
- Datos de titularidad por tamaño de tenedor: solicitud al Catastro redactada y pendiente de presentar (docs/v3/solicitudes_transparencia.md).
- Series anuales del suelo urbanizable (SIU 2016-2024): solicitud redactada y pendiente de presentar.
- Un indicador de alquiler de contratos nuevos posterior a 2024 a escala fina, para evaluar el registro único de arrendamientos y la caída de anuncios de 2025-2026 (sin datos: P-C2 no detectable).
- Fianzas de la Generalitat Valenciana con acceso abierto (descarga fallida en v3).

## 4. Módulo València

Nota de periodos y medidas: no son comparables entre filas.
- Las filas de la ciudad usan 2020-2024 y el alquiler SERPAVI municipal.
- La fila de secciones usa 2021M08-2024M08.
- La provincia usa el IPC de alquiler provincial.

| Indicador | València ciudad | Provincia de València | Capa y fuente |
|---|---|---|---|
| Viviendas turísticas, oleadas de agosto (INE, municipio) | 6.899 (2020) → 5.616 (2021) → 7.976 (2024) | — | C4 (INE, estadística experimental; data/raw/ine_v2_vut.csv) |
| Viviendas turísticas, oleadas de mayo | 6.553 (2025) → 5.393 (2026) | — | C4 (ídem; solo se comparan oleadas del mismo mes) |
| Aumento de VUT 2020-2024 frente al stock de alquiler | como máximo el 1,9 % del stock (sustitución 1:1) | — | C2 (output/v3/PB) |
| Parte de la subida del alquiler 2021M08-2024M08 en secciones donde las VUT crecieron menos de 0,1 pp | 28,3 % (173 de 575 secciones) | — | C2 (output/v3/PB/tablas/b1_no_explica_secciones.csv) |
| Cota de precio de VUT con \|ε\|=0,33, 2020-2024 | ≤5,8 % (≈29 €/mes en 80 m²) | ≤9,6 % | C4 (condicionada a ε) |
| Parte de la subida del alquiler 2020-2024 que esa cota no cubre | 79,7 % (subida SERPAVI +28,7 %) | 0 %: con el IPC provincial, la cota cubre toda la subida | C4 (condicionada a ε; medidas de alquiler distintas) |
| Balance hogares − viviendas nuevas 2022-2025 | — | +52.000 a +69.000 | C4 (una sola fuente de hogares provincial) |
| Precio/renta (80 m², 2023) | 3,8 años de renta | 3,0 | C4 (una fuente de renta en ese nivel) |
| Alquiler/renta (SERPAVI, 2023) | 18,1 % | 16,3 % | C4 (fuente única de alquiler en ese nivel) |
| Cuota hipotecaria/renta (2023) | 18,8 % | 15,0 % | C4 |
| Réplica de García-López et al. (2020) | PARCIAL: mismo signo, magnitud menor (+0,005 log-p por pp; IC95 0,0001-0,010; p_Holm 0,37; G = 15) | — | C4 (output/v3/GL) |

Lectura del módulo:
- Viviendas turísticas en València ciudad (oleadas de agosto): 6.899 en 2020, 5.616 en 2021 y 7.976 en 2024. Entre mayo de 2025 y mayo de 2026 pasaron de 6.553 a 5.393.
- Su aumento acotado frente al stock de alquiler de la ciudad es como máximo del 1,9 %.
- La cota de precio depende de ε (C4):
  - En la ciudad, con el alquiler SERPAVI y la elasticidad más baja del rango, cubre como máximo el 20,3 % de la subida de 2020-2024.
  - En la provincia, con el IPC de alquiler, cubre toda la subida.
  - Las dos lecturas usan medidas de alquiler distintas y no se pueden comparar directamente.
- El esfuerzo de acceso de la ciudad es mayor que el de la provincia en las tres medidas.

## 5. Límites
Ver docs/v3/limitaciones.md. Los más relevantes para la política:
- (i) Ningún efecto alcanzó C3; las cifras C4 orientan, pero no deciden.
- (ii) Las simulaciones dependen de rangos de elasticidades sin estimación española verificada; se informa el rango completo.
- (iii) SERPAVI mide un stock de contratos declarados y amortigua los cambios de precio.
