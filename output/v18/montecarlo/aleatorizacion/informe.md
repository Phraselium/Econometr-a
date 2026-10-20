# V18 · Monte Carlo · Inferencia por aleatorización (permutaciones)

**Veredicto: APTO.**

## Proceso generador (declarado antes de simular)

Dos familias, con la estructura de _dgp_did.py (E2) y _dgp_itp.py (E8); todo simulado.
E2 (topes en Cataluña, R1 / A1): municipio-trimestre, T = 13, entrada en el índice 7; cat_trim_M = 100 tratados y 200 controles; pocos_tratados = 10 y 150; 42 comarcas, tratados concentrados en las 12 primeras.
Resultado: factores comunes AR(1) con cargas heterogéneas, choque de comarca AR(1) (ρ 0,6, sd 0,02), ruido AR(1) heterocedástico, efecto τ_i = τ (1 + 0,5 z_i) con rampa (nulo 0; alternativa τ = −0,05). Estadístico:
ATT = media(Δ_i | tratados) − media(Δ_i | controles), Δ_i = media de los periodos posteriores − media de los previos; verdad = media de los efectos de los tratados en los periodos posteriores.
Contrastes (499 permutaciones + identidad): (1) permutación de la asignación ENTRE TODOS los municipios, estadístico estudentizado (Welch) [la del plan, principal]; (2) la misma con el coeficiente a secas;
(3) permutación DENTRO de cada comarca (conserva los tratados por comarca) estudentizada; (4) dentro de comarca con el coeficiente.
E8 (ITP, R1/R2): 36 provincias en 8 CCAA, T = 24, calendarios de dosis como en dcdh_aleatorizacion («desigual» y «equilibrado»), nulo β = 0 y alternativa β = −0,03 por punto con efecto CONSTANTE (nivel de la dosis).
Estadístico: coeficiente de MCO de dos vías sobre la dosis con EE agrupado por CCAA; permutación de los calendarios completos entre las 8 CCAA (499 + identidad), estudentizado (principal) o no.
Cobertura = 1 − rechazo del contraste en θ = verdad (inversión del contraste, efecto constante impuesto); tamaño = rechazo de θ = 0 con el efecto nulo; potencia = rechazo de θ = 0 con la alternativa.

## Qué falló en V16 y qué se hace distinto

V16 (dcdh_aleatorizacion, NO APTO): tamaño 0,0775 y cobertura 0,967 con 11 clusters y un estadístico sin estudentizar. La aleatorización de V18 se mide aquí en sus dos usos (asignación entre municipios en E2 y
calendarios entre CCAA en E8) y con dos estadísticos, para aislar qué cambia el tamaño: estudentizar (en estos procesos no lo cambia de forma apreciable) y permutar dentro de la comarca (lo acerca al nominal cuando
los tratados se concentran en pocas comarcas con choques propios, que es lo que el plan no controla cuando permuta entre todos los municipios). El 0,0775 de V16 no se reproduce con estas estructuras.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | veredicto | banda_112 |
|---|---|---|---|---|---|---|---|---|
| E2_cat_trim_M | permuta_entre_municipios_estudentizada (plan) | 2000 | 0.0635 | 0.9365 | 0.9425 | 0.9995 | APTO | con valor crítico corregido |
| E2_cat_trim_M | permuta_entre_municipios_coeficiente | 2000 | 0.0635 | 0.9365 | 0.9345 | 1.0000 | APTO | con valor crítico corregido |
| E2_cat_trim_M | permuta_dentro_de_comarca_estudentizada | 2000 | 0.0520 | 0.9480 | 0.9650 | 0.9990 | APTO | apta |
| E2_cat_trim_M | permuta_dentro_de_comarca_coeficiente | 2000 | 0.0520 | 0.9480 | 0.9605 | 0.9990 | APTO | apta |
| E2_pocos_tratados | permuta_entre_municipios_estudentizada (plan) | 2000 | 0.0530 | 0.9470 | 0.9680 | 0.5590 | APTO | apta |
| E2_pocos_tratados | permuta_entre_municipios_coeficiente | 2000 | 0.0525 | 0.9475 | 0.9535 | 0.6490 | APTO | apta |
| E2_pocos_tratados | permuta_dentro_de_comarca_estudentizada | 2000 | 0.0530 | 0.9470 | 0.9725 | 0.5445 | NO APTO | con valor crítico corregido |
| E2_pocos_tratados | permuta_dentro_de_comarca_coeficiente | 2000 | 0.0490 | 0.9510 | 0.9620 | 0.6360 | APTO | apta |
| E8_desigual | calendarios_entre_CCAA_estudentizada (plan) | 2000 | 0.0530 | 0.9470 | 0.9540 | 0.8630 | APTO | apta |
| E8_desigual | calendarios_entre_CCAA_coeficiente | 2000 | 0.0420 | 0.9580 | 0.9535 | 0.9470 | APTO | apta |
| E8_equilibrado | calendarios_entre_CCAA_estudentizada (plan) | 2000 | 0.0575 | 0.9425 | 0.9600 | 0.9280 | APTO | apta |
| E8_equilibrado | calendarios_entre_CCAA_coeficiente | 2000 | 0.0550 | 0.9450 | 0.9470 | 0.9725 | APTO | apta |

## Notas

- Las variantes marcadas (plan) deciden el veredicto; las demás aíslan la causa (estudentización, permutación dentro de comarca).
- E8: el efecto de la alternativa es constante (efecto de nivel de la dosis), porque el contraste de Fisher impone un efecto constante.
