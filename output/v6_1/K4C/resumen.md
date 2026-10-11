# K4c · Coherencia de cifras (resumen)

Cifras significativas analizadas: 1916. Fuente de verdad: output/v5/cifras_clave.csv.

## Recuentos globales

| clase | n |
|---|---|
| EN_CIFRAS_CLAVE | 797 |
| HISTORICA_MARCADA | 503 |
| SIN_FECHA | 585 |
| HUERFANA | 26 |
| CONTRADICTORIA | 5 |

## Recuentos por fichero

| fichero | EN_CIFRAS_CLAVE | HISTORICA_MARCADA | SIN_FECHA | HUERFANA | CONTRADICTORIA | total |
|---|---|---|---|---|---|---|
| README.md | 1 | 0 | 0 | 0 | 0 | 1 |
| README_REPLICACION.md | 0 | 5 | 2 | 0 | 0 | 7 |
| archive/output/v3/articulo.md | 0 | 160 | 0 | 0 | 0 | 160 |
| archive/output/v3/informe_politica.md | 0 | 69 | 0 | 0 | 0 | 69 |
| archive/output/v3/lo_que_sabemos.md | 0 | 59 | 0 | 0 | 0 | 59 |
| archive/output/v4/policy_brief.md | 0 | 24 | 0 | 0 | 0 | 24 |
| archive/output/v4/working_paper.md | 0 | 63 | 0 | 0 | 0 | 63 |
| docs/v5/calendario_publicacion.md | 0 | 0 | 1 | 0 | 0 | 1 |
| docs/v5/licencias_datos.md | 2 | 2 | 0 | 0 | 0 | 4 |
| docs/v5/literatura_instrumentos.md | 11 | 1 | 1 | 0 | 0 | 13 |
| output/v5/articulo_colegio.md | 36 | 3 | 14 | 0 | 0 | 53 |
| output/v5/articulos/a_necesidades.md | 50 | 16 | 85 | 0 | 0 | 151 |
| output/v5/articulos/b_replicacion.md | 16 | 8 | 30 | 0 | 0 | 54 |
| output/v5/articulos/c_territorio.md | 6 | 0 | 50 | 0 | 0 | 56 |
| output/v5/correo_coev.md | 0 | 0 | 2 | 0 | 0 | 2 |
| output/v5/informe_tecnico.md | 227 | 39 | 210 | 0 | 1 | 477 |
| output/v5/linkedin/01.md | 1 | 0 | 2 | 0 | 0 | 3 |
| output/v5/linkedin/02.md | 3 | 0 | 0 | 0 | 0 | 3 |
| output/v5/linkedin/03.md | 2 | 0 | 4 | 0 | 0 | 6 |
| output/v5/linkedin/04.md | 5 | 0 | 0 | 0 | 0 | 5 |
| output/v5/linkedin/05.md | 2 | 0 | 2 | 0 | 0 | 4 |
| output/v5/linkedin/06.md | 4 | 0 | 0 | 0 | 0 | 4 |
| output/v5/linkedin/07.md | 3 | 0 | 0 | 0 | 0 | 3 |
| output/v5/linkedin/08.md | 1 | 0 | 0 | 0 | 0 | 1 |
| output/v5/linkedin/09.md | 0 | 0 | 3 | 0 | 0 | 3 |
| output/v5/linkedin/10.md | 2 | 0 | 0 | 0 | 0 | 2 |
| output/v5/lo_que_sabemos.md | 50 | 2 | 16 | 0 | 0 | 68 |
| output/v5/policy_brief.md | 25 | 2 | 19 | 0 | 0 | 46 |
| output/v5/ponencia/diapositivas.md | 16 | 0 | 13 | 0 | 0 | 29 |
| output/v5/ponencia/guion.md | 11 | 0 | 22 | 0 | 0 | 33 |
| output/v5/una_pagina.md | 19 | 0 | 0 | 0 | 0 | 19 |
| output/v5/verificador/verificador.md | 235 | 26 | 8 | 26 | 4 | 299 |
| output/v5/working_paper.md | 69 | 24 | 101 | 0 | 0 | 194 |

## Contradictorias (prioridad 1)

- output/v5/informe_tecnico.md:72 · 242.400 · T4-H6 · «**2021-2024 [C1].** Con dos fuentes independientes en cada componente (hogares: ECP y EPA corregida por la rup»
- output/v5/verificador/verificador.md:345 · 45,2% · A23-P2 · «| Magnitud | Cota C2 de cantidad: la población extranjera supone como máximo el 45,2 % de la creación de hogar» → REVISADA: falso positivo: cota de población extranjera, no el precio A23-P2
- output/v5/verificador/verificador.md:361 · 2,26 · B4-v3-vut-cantidad · «| Magnitud | Cota C2: como máximo el 2,4-2,7 % del stock de alquiler (hasta 81.771 viviendas), 2020M08-2024M08» → REVISADA: huérfana de ficha: pp de la v2 (B4), no es el máximo de VUT
- output/v5/verificador/verificador.md:425 · 470 · CA-CR-saldo-pico · «| Magnitud | El saldo de crédito a construcción y actividades inmobiliarias pasó de 470 mil millones de euros » → REVISADA: redondeo de 471,8 mil millones (CA-CR-saldo-pico); diferencia 0,4 %
- output/v5/verificador/verificador.md:474 · 2.333.816 · CB-C6-03 · «| Magnitud | Personas fisicas declaran 2.333.816 viviendas equivalentes arrendadas como vivienda habitual ; el» → REVISADA: falso positivo: solo vivienda habitual; CB-C6-03 es habitual y otras

## Huérfanas (prioridad 2; primeras 60)

- output/v5/verificador/verificador.md:88 · 559.752 ·  · «| Intervalo | [559.752; 969.059] viviendas |»
- output/v5/verificador/verificador.md:88 · 969.059 ·  · «| Intervalo | [559.752; 969.059] viviendas |»
- output/v5/verificador/verificador.md:90 · 750 ·  · «| Literatura | Banco de España, Informe Anual 2025 (NO VERIFICADA: DOI no comprobado): ≈750 mil, dentro del ra»
- output/v5/verificador/verificador.md:135 · 3,83 ·  · «| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4»
- output/v5/verificador/verificador.md:135 · 277 ·  · «| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4»
- output/v5/verificador/verificador.md:135 · 1.806 ·  · «| Magnitud | Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4»
- output/v5/verificador/verificador.md:136 · 277 ·  · «| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 a 1.806 municipios) |»
- output/v5/verificador/verificador.md:136 · 1.806 ·  · «| Intervalo | 27,5-40,3 % en el tercil alto de presión (277 a 1.806 municipios) |»
- output/v5/verificador/verificador.md:171 · 10.000 ·  · «| Regla del veredicto | Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igu»
- output/v5/verificador/verificador.md:171 · 104.000 ·  · «| Regla del veredicto | Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igu»
- output/v5/verificador/verificador.md:175 · 10.000 ·  · «| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Regla común con M5-V1 (revisión C, C»
- output/v5/verificador/verificador.md:175 · 104.000 ·  · «| Convención B (estructural: traducción a precio como C2) | PARCIALMENTE. Regla común con M5-V1 (revisión C, C»
- output/v5/verificador/verificador.md:185 · 3.092.393 ·  · «| Magnitud | Solares catastrales (uso «solar») 2026: 3.092.393 unidades urbanas. Con viviendas por solar cubre»
- output/v5/verificador/verificador.md:185 · 454 ·  · «| Magnitud | Solares catastrales (uso «solar») 2026: 3.092.393 unidades urbanas. Con viviendas por solar cubre»
- output/v5/verificador/verificador.md:201 · 3.828.307 ·  · «| Magnitud | España: 3.828.307 vacías (14,4 % del parque) y 2.517.628 de uso esporádico (9,5 %) en el Censo 20»
- output/v5/verificador/verificador.md:201 · 2.517.628 ·  · «| Magnitud | España: 3.828.307 vacías (14,4 % del parque) y 2.517.628 de uso esporádico (9,5 %) en el Censo 20»
- output/v5/verificador/verificador.md:201 · 341.001 ·  · «| Magnitud | España: 3.828.307 vacías (14,4 % del parque) y 2.517.628 de uso esporádico (9,5 %) en el Censo 20»
- output/v5/verificador/verificador.md:217 · 249 ·  · «| Magnitud | 2021-2025: ninguna provincia con excedente; 7 provincias suman el 50 % del déficit y 19 el 80 %; »
- output/v5/verificador/verificador.md:233 · 53 ·  · «| Magnitud | 2021-2025: hogares +1,01 millones (C1: ECP y EPA corregida). En la descomposición contable, el co»
- output/v5/verificador/verificador.md:297 · 261 ·  · «| Magnitud | IPVA contrato nuevo 2015-2024 +37.0 % (nacional). Incasòl renta media 2015-2025 +54.5 % (Cataluña»
- output/v5/verificador/verificador.md:297 · 103 ·  · «| Magnitud | IPVA contrato nuevo 2015-2024 +37.0 % (nacional). Incasòl renta media 2015-2025 +54.5 % (Cataluña»
- output/v5/verificador/verificador.md:345 · 174.410 ·  · «| Magnitud | Cota C2 de cantidad: la población extranjera supone como máximo el 45,2 % de la creación de hogar»
- output/v5/verificador/verificador.md:361 · 81.771 ·  · «| Magnitud | Cota C2: como máximo el 2,4-2,7 % del stock de alquiler (hasta 81.771 viviendas), 2020M08-2024M08»
- output/v5/verificador/verificador.md:577 · 200 ·  · «| Límites | Muestra 2007Q1-2026Q2 (T=78) corta para el ciclo; ADF con un rezago; el valor de descuento fija g=»
- output/v5/verificador/verificador.md:636 · 180 ·  · «| Magnitud | Dirección nacional 2025-2030 (C2): empeora en 180 escenarios (terminadas: ritmo actual, cartera, »
- output/v5/verificador/verificador.md:669 · 3,79 ·  · «| Intervalo | Brecha rentabilidad menos coste de uso (g=2 %): mediana 1,56 pp, rango -0,07 a 3,79 pp |»
