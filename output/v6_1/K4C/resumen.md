# K4c · Coherencia de cifras (resumen)

Cifras significativas analizadas: 2071. Fuente de verdad: output/v5/cifras_clave.csv.

## Recuentos globales

| clase | n |
|---|---|
| EN_CIFRAS_CLAVE | 836 |
| HISTORICA_MARCADA | 516 |
| SIN_FECHA | 699 |
| HUERFANA | 16 |
| CONTRADICTORIA | 4 |

## Recuentos por fichero

| fichero | EN_CIFRAS_CLAVE | HISTORICA_MARCADA | SIN_FECHA | HUERFANA | CONTRADICTORIA | total |
|---|---|---|---|---|---|---|
| README.md | 1 | 0 | 0 | 0 | 0 | 1 |
| README_REPLICACION.md | 0 | 6 | 2 | 2 | 0 | 10 |
| archive/output/v3/articulo.md | 0 | 160 | 0 | 0 | 0 | 160 |
| archive/output/v3/informe_politica.md | 0 | 69 | 0 | 0 | 0 | 69 |
| archive/output/v3/lo_que_sabemos.md | 0 | 59 | 0 | 0 | 0 | 59 |
| archive/output/v4/policy_brief.md | 0 | 24 | 0 | 0 | 0 | 24 |
| archive/output/v4/working_paper.md | 0 | 63 | 0 | 0 | 0 | 63 |
| docs/v5/calendario_publicacion.md | 0 | 0 | 1 | 0 | 0 | 1 |
| docs/v5/licencias_datos.md | 2 | 2 | 0 | 0 | 0 | 4 |
| docs/v5/literatura_instrumentos.md | 11 | 1 | 1 | 0 | 0 | 13 |
| output/v5/articulo_colegio.md | 37 | 3 | 14 | 0 | 0 | 54 |
| output/v5/articulos/a_necesidades.md | 50 | 16 | 86 | 0 | 0 | 152 |
| output/v5/articulos/b_replicacion.md | 19 | 12 | 34 | 0 | 0 | 65 |
| output/v5/articulos/c_territorio.md | 6 | 0 | 56 | 0 | 0 | 62 |
| output/v5/correo_coev.md | 0 | 0 | 2 | 0 | 0 | 2 |
| output/v5/informe_tecnico.md | 225 | 50 | 260 | 0 | 0 | 535 |
| output/v5/linkedin/01.md | 2 | 0 | 2 | 0 | 0 | 4 |
| output/v5/linkedin/02.md | 3 | 0 | 0 | 0 | 0 | 3 |
| output/v5/linkedin/03.md | 2 | 0 | 4 | 0 | 0 | 6 |
| output/v5/linkedin/04.md | 5 | 0 | 0 | 0 | 0 | 5 |
| output/v5/linkedin/05.md | 2 | 0 | 2 | 0 | 0 | 4 |
| output/v5/linkedin/06.md | 4 | 0 | 0 | 0 | 0 | 4 |
| output/v5/linkedin/07.md | 3 | 0 | 0 | 0 | 0 | 3 |
| output/v5/linkedin/08.md | 1 | 0 | 0 | 0 | 0 | 1 |
| output/v5/linkedin/09.md | 0 | 0 | 3 | 0 | 0 | 3 |
| output/v5/linkedin/10.md | 2 | 0 | 0 | 0 | 0 | 2 |
| output/v5/lo_que_sabemos.md | 51 | 2 | 33 | 0 | 0 | 86 |
| output/v5/policy_brief.md | 26 | 2 | 36 | 0 | 0 | 64 |
| output/v5/ponencia/diapositivas.md | 17 | 0 | 13 | 0 | 0 | 30 |
| output/v5/ponencia/guion.md | 11 | 0 | 22 | 0 | 0 | 33 |
| output/v5/una_pagina.md | 20 | 0 | 0 | 0 | 0 | 20 |
| output/v5/verificador/verificador.md | 265 | 23 | 8 | 14 | 4 | 314 |
| output/v5/working_paper.md | 71 | 24 | 120 | 0 | 0 | 215 |

## Contradictorias (prioridad 1)

- output/v5/verificador/verificador.md:332 · 45,2% · A23-P2 · «| Magnitud | Cota C2 de cantidad: la población extranjera supone como máximo el 45,2 % de la creación de hogar» → REVISADA: falso positivo: cota de población extranjera, no el precio A23-P2
- output/v5/verificador/verificador.md:348 · 2,26 · B4-v3-vut-cantidad · «| Magnitud | Cota C2: como máximo el 2,4-2,7 % del stock de alquiler (hasta 81.771 viviendas), 2020M08-2024M08» → REVISADA: huérfana de ficha: pp de la v2 (B4), no es el máximo de VUT
- output/v5/verificador/verificador.md:412 · 470 · CA-CR-saldo-pico · «| Magnitud | El saldo de crédito a construcción y actividades inmobiliarias pasó de 470 mil millones de euros » → REVISADA: redondeo de 471,8 mil millones (CA-CR-saldo-pico); diferencia 0,4 %
- output/v5/verificador/verificador.md:461 · 2.333.816 · CB-C6-03 · «| Magnitud | Personas fisicas declaran 2.333.816 viviendas equivalentes arrendadas como vivienda habitual ; el» → REVISADA: falso positivo: solo vivienda habitual; CB-C6-03 es habitual y otras

## Huérfanas (prioridad 2; primeras 60)

- output/v5/verificador/verificador.md:122 · 277 ·  · «| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4»
- output/v5/verificador/verificador.md:122 · 1.806 ·  · «| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4»
- output/v5/verificador/verificador.md:123 · 277 ·  · «| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 a 1.806 municipios) |»
- output/v5/verificador/verificador.md:123 · 1.806 ·  · «| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 a 1.806 municipios) |»
- output/v5/verificador/verificador.md:158 · 10.000 ·  · «| Regla del veredicto | Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igu»
- output/v5/verificador/verificador.md:158 · 104.000 ·  · «| Regla del veredicto | Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igu»
- output/v5/verificador/verificador.md:162 · 10.000 ·  · «| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Regla común con M5-V1 (revisión C, C»
- output/v5/verificador/verificador.md:162 · 104.000 ·  · «| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Regla común con M5-V1 (revisión C, C»
- output/v5/verificador/verificador.md:172 · 454 ·  · «| Magnitud | Solares catastrales (uso «solar») 2026: 3.092.393 unidades urbanas. Con viviendas por solar cubre»
- output/v5/verificador/verificador.md:204 · 249 ·  · «| Magnitud | 2021-2025: ninguna provincia con excedente; 7 provincias suman el 50 % del déficit y 19 el 80 %; »
- output/v5/verificador/verificador.md:220 · 53 ·  · «| Magnitud | 2021-2025: hogares +1,01 millones (C1: ECP y EPA corregida). En la descomposición contable, el co»
- output/v5/verificador/verificador.md:564 · 200 ·  · «| Límites | Muestra 2007Q1-2026Q2 (T=78) corta para el ciclo; ADF con un rezago; el valor de descuento fija g=»
- output/v5/verificador/verificador.md:623 · 180 ·  · «| Magnitud | Dirección nacional 2025-2030 (C2): empeora en 180 escenarios (terminadas: ritmo actual, cartera, »
- output/v5/verificador/verificador.md:656 · 3,79 ·  · «| Intervalo | Brecha rentabilidad menos coste de uso (g=2 %): mediana 1,56 pp, rango -0,07 a 3,79 pp |»
- README_REPLICACION.md:12 · 7.498 ·  · «| Tiempo | ≈2 min por ejecución completa ( , v1-v6, un solo hilo); medido dos veces en un clon limpio: 7.564 s»
- README_REPLICACION.md:12 · 6.947 ·  · «| Tiempo | ≈2 min por ejecución completa ( , v1-v6, un solo hilo); medido dos veces en un clon limpio: 7.564 s»
