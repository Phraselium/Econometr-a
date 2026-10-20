# V18 · Monte Carlo · BVAR recursivo con prior de Minnesota: cobertura de las bandas (E7-R3 y E7-A1)

**Veredicto: NO APTO.** Condición en que falla: T=60|rho=0.97|nulo|compraventas: cobertura 68 % 0.987 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|precio: cobertura 68 % 0.964 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|visados: cobertura 68 % 0.988 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|compraventas: cobertura 90 % 0.952 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|precio: cobertura 68 % 0.016 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.180 fuera de [0.87; 0.93] (insuficiente); T=60|rho=0.97|alternativa|visados: cobertura 68 % 0.420 fuera de [0.63; 0.73] (insuficiente); T=74|rho=0.97|nulo|compraventas: cobertura 68 % 0.981 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|nulo|precio: cobertura 68 % 0.940 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 0.999 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|nulo|visados: cobertura 68 % 0.977 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|alternativa|compraventas: cobertura 68 % 0.608 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.934 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|alternativa|precio: cobertura 68 % 0.005 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.117 fuera de [0.87; 0.93] (insuficiente); T=74|rho=0.97|alternativa|visados: cobertura 68 % 0.316 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.825 fuera de [0.87; 0.93] (insuficiente).

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real): VAR(2) de 7 variables en el orden de San Juan (2023), [compraventas, precio, visados, PIB, IPCA, euríbor, crédito] (variables en 100 log salvo el IPCA y el euríbor, en puntos
porcentuales), con 3 ficticias estacionales no nulas en la estimación (el proceso verdadero no tiene estacionalidad: la estimación se carga de parámetros inútiles, un caso conservador) y los huecos de visados de 2016T2 y 2017T2 de la base.
Proceso verdadero: matrices A_1 = diag(0,5) + N(0; 0,05²) y A_2 = diag(0,2) + N(0; 0,05²) con SEED 20261010; se pone a cero la columna del euríbor en las ecuaciones de las tres variables de interés y se
fijan los efectos hacia delante del euríbor (alternativa: compraventas −1,2, precio −0,5, visados −2,5 por pp en el primer rezago); en el nulo, la respuesta verdadera de las tres variables al choque del euríbor es EXACTAMENTE cero a todo
horizonte (se anula toda la columna del euríbor y la del crédito en las ecuaciones de las variables que anteceden al crédito). Se reescala todo para que la mayor raíz de la companion sea ρ = 0,97 o 0,90.
Perturbaciones u_t = B0 ε_t con B0 = diag(σ) (I + N(0; 0,3²) estrictamente por debajo de la diagonal), σ = (3; 0,8; 6; 0,5; 0,4; 0,15; 5): triangular inferior con diagonal positiva, de modo que el Cholesky de Σ es B0 y la
identificación recursiva es exacta (supuesto de San Juan cumplido por construcción). Choque: el del euríbor (posición 6), normalizado a +1 pp en su impacto (+100 pb).
Estimador: BVAR(2) con prior de Minnesota en observaciones ficticias (λ = 0,2, γ = 1 en niveles y 0,8 en el IPCA y el euríbor, decaimiento por rezago, suma de coeficientes con peso 1/(10 λ) = 0,5 sobre la media inicial en logaritmos (convención de Bańbura et al., 2010); escalas σ_i del AR(1) de cada serie; Σ ~ IW,
B | Σ normal): 500 extracciones del posterior por réplica; bandas por percentiles 16-84 y 5-95 de la respuesta normalizada a h = 4 y 8. La «prior más laxa» (variante v1 de E7-R3) usa λ = 0,5 y sin suma de coeficientes; la «difusa» (λ = 50, sin suma de coeficientes; solo información) comprueba que el código da una cobertura cercana a la nominal cuando el prior apenas informa.
Cobertura = proporción de réplicas con la respuesta verdadera dentro de la banda. T = 60 (2008T1-2022T4, E7-R3), 74 (2008T1-2026T2, E7-A1) y 48 (2008T1-2019T4, E7-R3-v2).

## Qué falló en V16 y qué se hace distinto

No hay Monte Carlo previo de un BVAR en V15 ni en V16 (el plan lo marca «Sin validar», sección 1.13). Se aplica lo aprendido en las demás herramientas de V18: el proceso generador reproduce la estructura de la muestra (T, huecos, orden de las
variables), el nulo se impone exactamente sobre las respuestas medidas y la cobertura se mide por inversión sobre la verdad del propio proceso; se separan la persistencia (0,90 y 0,97) y el tamaño muestral.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | variable | h | efecto_verdadero | R | cobertura_68 | cobertura_90 | ancho_banda_68 | sesgo_mediana | raices_estables | decisivo | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T=60|rho=0.97 | principal | compraventas | 4 | nulo | 2000 | 0.9560 | 0.9995 | 1.1750 | 0.1218 | 0.6509 | False | NO APTO |
| T=60|rho=0.97 | principal | precio | 4 | nulo | 2000 | 0.9080 | 0.9985 | 0.3757 | -0.0694 | 0.6509 | False | NO APTO |
| T=60|rho=0.97 | principal | visados | 4 | nulo | 2000 | 0.9705 | 0.9995 | 2.6722 | 0.0477 | 0.6509 | False | NO APTO |
| T=60|rho=0.97 | principal | compraventas | 8 | nulo | 2000 | 0.9870 | 1.0000 | 0.9524 | 0.0885 | 0.6509 | True | NO APTO |
| T=60|rho=0.97 | principal | precio | 8 | nulo | 2000 | 0.9635 | 1.0000 | 0.3512 | -0.0502 | 0.6509 | True | NO APTO |
| T=60|rho=0.97 | principal | visados | 8 | nulo | 2000 | 0.9880 | 1.0000 | 2.5852 | 0.0513 | 0.6509 | True | NO APTO |
| T=60|rho=0.97 | laxa | compraventas | 4 | nulo | 2000 | 0.8895 | 0.9910 | 1.2900 | 0.0869 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | laxa | precio | 4 | nulo | 2000 | 0.8500 | 0.9810 | 0.4074 | -0.0397 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | laxa | visados | 4 | nulo | 2000 | 0.8580 | 0.9890 | 3.1684 | -0.0530 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | laxa | compraventas | 8 | nulo | 2000 | 0.9435 | 1.0000 | 1.0218 | 0.0421 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | laxa | precio | 8 | nulo | 2000 | 0.9390 | 0.9985 | 0.3336 | -0.0195 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | laxa | visados | 8 | nulo | 2000 | 0.9305 | 0.9985 | 2.8225 | 0.0448 | 0.6617 | False | NO APTO |
| T=60|rho=0.97 | difusa | compraventas | 4 | nulo | 2000 | 0.8195 | 0.9690 | 1.6981 | 0.0901 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | difusa | precio | 4 | nulo | 2000 | 0.7865 | 0.9555 | 0.5493 | -0.0311 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | difusa | visados | 4 | nulo | 2000 | 0.7410 | 0.9400 | 3.9986 | -0.0839 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | difusa | compraventas | 8 | nulo | 2000 | 0.8750 | 0.9900 | 1.4018 | 0.0267 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | difusa | precio | 8 | nulo | 2000 | 0.8870 | 0.9850 | 0.4536 | -0.0019 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | difusa | visados | 8 | nulo | 2000 | 0.8540 | 0.9875 | 3.6181 | 0.1452 | 0.5980 | False | NO APTO |
| T=60|rho=0.97 | principal | compraventas | 4 | alternativa | 2000 | 0.5675 | 0.9530 | 1.0392 | 0.4374 | 0.7741 | False | NO APTO |
| T=60|rho=0.97 | principal | precio | 4 | alternativa | 2000 | 0.0030 | 0.0480 | 0.3739 | -0.5155 | 0.7741 | False | NO APTO |
| T=60|rho=0.97 | principal | visados | 4 | alternativa | 2000 | 0.5735 | 0.9560 | 2.1310 | 0.9364 | 0.7741 | False | NO APTO |
| T=60|rho=0.97 | principal | compraventas | 8 | alternativa | 2000 | 0.6665 | 0.9520 | 1.0954 | -0.4491 | 0.7741 | True | NO APTO |
| T=60|rho=0.97 | principal | precio | 8 | alternativa | 2000 | 0.0160 | 0.1800 | 0.4599 | -0.5408 | 0.7741 | True | NO APTO |
| T=60|rho=0.97 | principal | visados | 8 | alternativa | 2000 | 0.4200 | 0.8760 | 1.7496 | -1.0034 | 0.7741 | True | NO APTO |
| T=60|rho=0.97 | laxa | compraventas | 4 | alternativa | 2000 | 0.8280 | 0.9780 | 1.1145 | 0.2153 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | laxa | precio | 4 | alternativa | 2000 | 0.0510 | 0.2535 | 0.4468 | -0.4923 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | laxa | visados | 4 | alternativa | 2000 | 0.7915 | 0.9735 | 2.3177 | 0.5483 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | laxa | compraventas | 8 | alternativa | 2000 | 0.7700 | 0.9660 | 1.3991 | -0.3288 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | laxa | precio | 8 | alternativa | 2000 | 0.2415 | 0.6045 | 0.5554 | -0.4168 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | laxa | visados | 8 | alternativa | 2000 | 0.6780 | 0.9330 | 2.2599 | -0.7509 | 0.7214 | False | NO APTO |
| T=60|rho=0.97 | difusa | compraventas | 4 | alternativa | 2000 | 0.7845 | 0.9540 | 1.7755 | -0.0585 | 0.6110 | False | NO APTO |
| T=60|rho=0.97 | difusa | precio | 4 | alternativa | 2000 | 0.3990 | 0.6770 | 0.7228 | -0.4226 | 0.6110 | False | NO APTO |
| T=60|rho=0.97 | difusa | visados | 4 | alternativa | 2000 | 0.7780 | 0.9560 | 3.7782 | 0.2892 | 0.6110 | False | NO APTO |
| T=60|rho=0.97 | difusa | compraventas | 8 | alternativa | 2000 | 0.7140 | 0.9205 | 2.3154 | -0.1177 | 0.6110 | False | APTO |
| T=60|rho=0.97 | difusa | precio | 8 | alternativa | 2000 | 0.5530 | 0.8320 | 0.9334 | -0.3093 | 0.6110 | False | NO APTO |
| T=60|rho=0.97 | difusa | visados | 8 | alternativa | 2000 | 0.7385 | 0.9330 | 3.8864 | -0.2852 | 0.6110 | False | NO APTO |
| T=74|rho=0.97 | principal | compraventas | 4 | nulo | 2000 | 0.9390 | 0.9975 | 1.0559 | 0.1154 | 0.7493 | False | NO APTO |
| T=74|rho=0.97 | principal | precio | 4 | nulo | 2000 | 0.8715 | 0.9915 | 0.3408 | -0.0745 | 0.7493 | False | NO APTO |
| T=74|rho=0.97 | principal | visados | 4 | nulo | 2000 | 0.9500 | 0.9990 | 2.4843 | 0.0159 | 0.7493 | False | NO APTO |
| T=74|rho=0.97 | principal | compraventas | 8 | nulo | 2000 | 0.9810 | 0.9995 | 0.7878 | 0.0776 | 0.7493 | True | NO APTO |
| T=74|rho=0.97 | principal | precio | 8 | nulo | 2000 | 0.9400 | 0.9985 | 0.2958 | -0.0487 | 0.7493 | True | NO APTO |
| T=74|rho=0.97 | principal | visados | 8 | nulo | 2000 | 0.9770 | 1.0000 | 2.3272 | 0.0282 | 0.7493 | True | NO APTO |
| T=74|rho=0.97 | laxa | compraventas | 4 | nulo | 2000 | 0.8590 | 0.9850 | 1.1214 | 0.0779 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | laxa | precio | 4 | nulo | 2000 | 0.8320 | 0.9745 | 0.3620 | -0.0393 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | laxa | visados | 4 | nulo | 2000 | 0.8325 | 0.9790 | 2.8495 | -0.0852 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | laxa | compraventas | 8 | nulo | 2000 | 0.9170 | 0.9925 | 0.8345 | 0.0400 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | laxa | precio | 8 | nulo | 2000 | 0.9130 | 0.9950 | 0.2804 | -0.0171 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | laxa | visados | 8 | nulo | 2000 | 0.9055 | 0.9950 | 2.4804 | 0.0249 | 0.7432 | False | NO APTO |
| T=74|rho=0.97 | difusa | compraventas | 4 | nulo | 2000 | 0.7890 | 0.9640 | 1.3658 | 0.0753 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | difusa | precio | 4 | nulo | 2000 | 0.7580 | 0.9430 | 0.4487 | -0.0279 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | difusa | visados | 4 | nulo | 2000 | 0.7285 | 0.9345 | 3.3683 | -0.1150 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | difusa | compraventas | 8 | nulo | 2000 | 0.8580 | 0.9750 | 1.0564 | 0.0301 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | difusa | precio | 8 | nulo | 2000 | 0.8555 | 0.9840 | 0.3535 | 0.0000 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | difusa | visados | 8 | nulo | 2000 | 0.8360 | 0.9780 | 2.9700 | 0.0904 | 0.7021 | False | NO APTO |
| T=74|rho=0.97 | principal | compraventas | 4 | alternativa | 2000 | 0.5325 | 0.9345 | 0.9114 | 0.4119 | 0.8515 | False | NO APTO |
| T=74|rho=0.97 | principal | precio | 4 | alternativa | 2000 | 0.0000 | 0.0220 | 0.3390 | -0.5210 | 0.8515 | False | NO APTO |
| T=74|rho=0.97 | principal | visados | 4 | alternativa | 2000 | 0.5725 | 0.9415 | 1.8877 | 0.8434 | 0.8515 | False | NO APTO |
| T=74|rho=0.97 | principal | compraventas | 8 | alternativa | 2000 | 0.6080 | 0.9345 | 0.9579 | -0.4194 | 0.8515 | True | NO APTO |
| T=74|rho=0.97 | principal | precio | 8 | alternativa | 2000 | 0.0055 | 0.1175 | 0.4113 | -0.5194 | 0.8515 | True | NO APTO |
| T=74|rho=0.97 | principal | visados | 8 | alternativa | 2000 | 0.3155 | 0.8245 | 1.4702 | -0.9527 | 0.8515 | True | NO APTO |
| T=74|rho=0.97 | laxa | compraventas | 4 | alternativa | 2000 | 0.8050 | 0.9735 | 0.9641 | 0.2031 | 0.7966 | False | NO APTO |
| T=74|rho=0.97 | laxa | precio | 4 | alternativa | 2000 | 0.0465 | 0.2320 | 0.4117 | -0.4676 | 0.7966 | False | NO APTO |
| T=74|rho=0.97 | laxa | visados | 4 | alternativa | 2000 | 0.7880 | 0.9655 | 2.0224 | 0.4715 | 0.7966 | False | NO APTO |
| T=74|rho=0.97 | laxa | compraventas | 8 | alternativa | 2000 | 0.7790 | 0.9575 | 1.2471 | -0.2747 | 0.7966 | False | NO APTO |
| T=74|rho=0.97 | laxa | precio | 8 | alternativa | 2000 | 0.2375 | 0.6010 | 0.5036 | -0.3877 | 0.7966 | False | NO APTO |
| T=74|rho=0.97 | laxa | visados | 8 | alternativa | 2000 | 0.7065 | 0.9290 | 2.0302 | -0.6385 | 0.7966 | False | APTO |
| T=74|rho=0.97 | difusa | compraventas | 4 | alternativa | 2000 | 0.7755 | 0.9530 | 1.4142 | -0.0398 | 0.7307 | False | NO APTO |
| T=74|rho=0.97 | difusa | precio | 4 | alternativa | 2000 | 0.3785 | 0.6480 | 0.6252 | -0.3921 | 0.7307 | False | NO APTO |
| T=74|rho=0.97 | difusa | visados | 4 | alternativa | 2000 | 0.7455 | 0.9460 | 3.0767 | 0.2789 | 0.7307 | False | NO APTO |
| T=74|rho=0.97 | difusa | compraventas | 8 | alternativa | 2000 | 0.7105 | 0.9085 | 1.9166 | -0.1085 | 0.7307 | False | APTO |
| T=74|rho=0.97 | difusa | precio | 8 | alternativa | 2000 | 0.5485 | 0.8115 | 0.7936 | -0.2937 | 0.7307 | False | NO APTO |
| T=74|rho=0.97 | difusa | visados | 8 | alternativa | 2000 | 0.7135 | 0.9210 | 3.1465 | -0.2383 | 0.7307 | False | APTO |
| T=60|rho=0.9 | principal | compraventas | 4 | nulo | 2000 | 0.9520 | 0.9990 | 1.2305 | 0.1395 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | principal | precio | 4 | nulo | 2000 | 0.8960 | 0.9970 | 0.3908 | -0.0781 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | principal | visados | 4 | nulo | 2000 | 0.9630 | 1.0000 | 2.7645 | 0.0719 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | principal | compraventas | 8 | nulo | 2000 | 0.9915 | 1.0000 | 0.9749 | 0.0892 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | principal | precio | 8 | nulo | 2000 | 0.9650 | 1.0000 | 0.3506 | -0.0546 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | principal | visados | 8 | nulo | 2000 | 0.9940 | 1.0000 | 2.4733 | 0.0831 | 0.7367 | False | NO APTO |
| T=60|rho=0.9 | laxa | compraventas | 4 | nulo | 2000 | 0.8985 | 0.9930 | 1.3474 | 0.0723 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | laxa | precio | 4 | nulo | 2000 | 0.8755 | 0.9890 | 0.4127 | -0.0370 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | laxa | visados | 4 | nulo | 2000 | 0.8835 | 0.9910 | 3.2557 | 0.0050 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | laxa | compraventas | 8 | nulo | 2000 | 0.9665 | 0.9995 | 1.0189 | 0.0221 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | laxa | precio | 8 | nulo | 2000 | 0.9540 | 0.9970 | 0.3237 | -0.0168 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | laxa | visados | 8 | nulo | 2000 | 0.9675 | 0.9995 | 2.6604 | 0.0479 | 0.7610 | False | NO APTO |
| T=60|rho=0.9 | difusa | compraventas | 4 | nulo | 2000 | 0.8265 | 0.9690 | 1.8205 | 0.0524 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | difusa | precio | 4 | nulo | 2000 | 0.7935 | 0.9605 | 0.5697 | -0.0205 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | difusa | visados | 4 | nulo | 2000 | 0.7815 | 0.9570 | 4.1985 | 0.0748 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | difusa | compraventas | 8 | nulo | 2000 | 0.9225 | 0.9955 | 1.4416 | -0.0116 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | difusa | precio | 8 | nulo | 2000 | 0.9025 | 0.9915 | 0.4564 | 0.0006 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | difusa | visados | 8 | nulo | 2000 | 0.8950 | 0.9930 | 3.5744 | 0.1552 | 0.6955 | False | NO APTO |
| T=60|rho=0.9 | principal | compraventas | 4 | alternativa | 2000 | 0.8070 | 0.9835 | 1.1793 | 0.3075 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | principal | precio | 4 | alternativa | 2000 | 0.0165 | 0.2100 | 0.4218 | -0.4765 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | principal | visados | 4 | alternativa | 2000 | 0.7845 | 0.9715 | 2.4527 | 0.6732 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | principal | compraventas | 8 | alternativa | 2000 | 0.8140 | 0.9815 | 1.1064 | -0.2461 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | principal | precio | 8 | alternativa | 2000 | 0.1660 | 0.6060 | 0.4609 | -0.3656 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | principal | visados | 8 | alternativa | 2000 | 0.7675 | 0.9795 | 1.8881 | -0.5419 | 0.8718 | False | NO APTO |
| T=60|rho=0.9 | laxa | compraventas | 4 | alternativa | 2000 | 0.8425 | 0.9810 | 1.2135 | 0.1674 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | laxa | precio | 4 | alternativa | 2000 | 0.1760 | 0.4955 | 0.4697 | -0.3949 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | laxa | visados | 4 | alternativa | 2000 | 0.8165 | 0.9720 | 2.5697 | 0.4293 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | laxa | compraventas | 8 | alternativa | 2000 | 0.7990 | 0.9715 | 1.3128 | -0.1870 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | laxa | precio | 8 | alternativa | 2000 | 0.4710 | 0.8115 | 0.5086 | -0.2575 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | laxa | visados | 8 | alternativa | 2000 | 0.7835 | 0.9730 | 2.2873 | -0.3966 | 0.8473 | False | NO APTO |
| T=60|rho=0.9 | difusa | compraventas | 4 | alternativa | 2000 | 0.7850 | 0.9640 | 1.8876 | -0.0343 | 0.7509 | False | NO APTO |
| T=60|rho=0.9 | difusa | precio | 4 | alternativa | 2000 | 0.5250 | 0.7955 | 0.7349 | -0.3038 | 0.7509 | False | NO APTO |
| T=60|rho=0.9 | difusa | visados | 4 | alternativa | 2000 | 0.7775 | 0.9525 | 4.0542 | 0.2892 | 0.7509 | False | NO APTO |
| T=60|rho=0.9 | difusa | compraventas | 8 | alternativa | 2000 | 0.7495 | 0.9450 | 2.1193 | -0.0831 | 0.7509 | False | NO APTO |
| T=60|rho=0.9 | difusa | precio | 8 | alternativa | 2000 | 0.6300 | 0.8845 | 0.8223 | -0.1892 | 0.7509 | False | APTO |
| T=60|rho=0.9 | difusa | visados | 8 | alternativa | 2000 | 0.7965 | 0.9670 | 3.7657 | -0.1028 | 0.7509 | False | NO APTO |
| T=74|rho=0.9 | principal | compraventas | 4 | nulo | 2000 | 0.9350 | 0.9980 | 1.0788 | 0.1228 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | principal | precio | 4 | nulo | 2000 | 0.8550 | 0.9940 | 0.3469 | -0.0829 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | principal | visados | 4 | nulo | 2000 | 0.9550 | 0.9990 | 2.5138 | 0.0573 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | principal | compraventas | 8 | nulo | 2000 | 0.9840 | 1.0000 | 0.7827 | 0.0725 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | principal | precio | 8 | nulo | 2000 | 0.9445 | 0.9990 | 0.2859 | -0.0503 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | principal | visados | 8 | nulo | 2000 | 0.9830 | 1.0000 | 2.1306 | 0.0747 | 0.8248 | False | NO APTO |
| T=74|rho=0.9 | laxa | compraventas | 4 | nulo | 2000 | 0.8655 | 0.9905 | 1.1472 | 0.0549 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | laxa | precio | 4 | nulo | 2000 | 0.8505 | 0.9800 | 0.3628 | -0.0364 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | laxa | visados | 4 | nulo | 2000 | 0.8410 | 0.9820 | 2.8647 | -0.0113 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | laxa | compraventas | 8 | nulo | 2000 | 0.9380 | 0.9970 | 0.8138 | 0.0180 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | laxa | precio | 8 | nulo | 2000 | 0.9515 | 0.9975 | 0.2641 | -0.0129 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | laxa | visados | 8 | nulo | 2000 | 0.9265 | 0.9980 | 2.2533 | 0.0616 | 0.8314 | False | NO APTO |
| T=74|rho=0.9 | difusa | compraventas | 4 | nulo | 2000 | 0.7880 | 0.9605 | 1.4316 | 0.0472 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | difusa | precio | 4 | nulo | 2000 | 0.7810 | 0.9505 | 0.4610 | -0.0201 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | difusa | visados | 4 | nulo | 2000 | 0.7310 | 0.9430 | 3.4632 | -0.0024 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | difusa | compraventas | 8 | nulo | 2000 | 0.8840 | 0.9890 | 1.0614 | -0.0007 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | difusa | precio | 8 | nulo | 2000 | 0.8920 | 0.9900 | 0.3456 | 0.0051 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | difusa | visados | 8 | nulo | 2000 | 0.8615 | 0.9860 | 2.8316 | 0.1436 | 0.7954 | False | NO APTO |
| T=74|rho=0.9 | principal | compraventas | 4 | alternativa | 2000 | 0.7495 | 0.9665 | 1.0085 | 0.2874 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | principal | precio | 4 | alternativa | 2000 | 0.0105 | 0.1230 | 0.3715 | -0.4640 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | principal | visados | 4 | alternativa | 2000 | 0.7975 | 0.9720 | 2.1246 | 0.5461 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | principal | compraventas | 8 | alternativa | 2000 | 0.7970 | 0.9675 | 0.9389 | -0.2145 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | principal | precio | 8 | alternativa | 2000 | 0.1400 | 0.5600 | 0.3937 | -0.3307 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | principal | visados | 8 | alternativa | 2000 | 0.7250 | 0.9505 | 1.5672 | -0.4964 | 0.9368 | False | NO APTO |
| T=74|rho=0.9 | laxa | compraventas | 4 | alternativa | 2000 | 0.7990 | 0.9685 | 1.0450 | 0.1622 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | laxa | precio | 4 | alternativa | 2000 | 0.1810 | 0.5065 | 0.4273 | -0.3619 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | laxa | visados | 4 | alternativa | 2000 | 0.7960 | 0.9690 | 2.2474 | 0.3371 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | laxa | compraventas | 8 | alternativa | 2000 | 0.7920 | 0.9655 | 1.1494 | -0.1309 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | laxa | precio | 8 | alternativa | 2000 | 0.4855 | 0.7965 | 0.4511 | -0.2288 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | laxa | visados | 8 | alternativa | 2000 | 0.7735 | 0.9565 | 2.0106 | -0.2917 | 0.9134 | False | NO APTO |
| T=74|rho=0.9 | difusa | compraventas | 4 | alternativa | 2000 | 0.7475 | 0.9490 | 1.5410 | -0.0063 | 0.8638 | False | NO APTO |
| T=74|rho=0.9 | difusa | precio | 4 | alternativa | 2000 | 0.5510 | 0.8000 | 0.6401 | -0.2561 | 0.8638 | False | NO APTO |
| T=74|rho=0.9 | difusa | visados | 4 | alternativa | 2000 | 0.7340 | 0.9350 | 3.3852 | 0.1885 | 0.8638 | False | NO APTO |
| T=74|rho=0.9 | difusa | compraventas | 8 | alternativa | 2000 | 0.7200 | 0.9425 | 1.7323 | -0.0342 | 0.8638 | False | NO APTO |
| T=74|rho=0.9 | difusa | precio | 8 | alternativa | 2000 | 0.6215 | 0.8650 | 0.6986 | -0.1607 | 0.8638 | False | NO APTO |
| T=74|rho=0.9 | difusa | visados | 8 | alternativa | 2000 | 0.7590 | 0.9560 | 3.0110 | -0.0539 | 0.8638 | False | NO APTO |
| T=48|rho=0.97 | principal | compraventas | 4 | nulo | 2000 | 0.9675 | 0.9995 | 1.3128 | 0.1207 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | principal | precio | 4 | nulo | 2000 | 0.9450 | 0.9990 | 0.4183 | -0.0665 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | principal | visados | 4 | nulo | 2000 | 0.9845 | 0.9990 | 2.8725 | 0.0618 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | principal | compraventas | 8 | nulo | 2000 | 0.9940 | 1.0000 | 1.1750 | 0.0962 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | principal | precio | 8 | nulo | 2000 | 0.9850 | 1.0000 | 0.4250 | -0.0514 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | principal | visados | 8 | nulo | 2000 | 0.9955 | 1.0000 | 2.9268 | 0.0751 | 0.5409 | False | NO APTO |
| T=48|rho=0.97 | laxa | compraventas | 4 | nulo | 2000 | 0.9210 | 0.9955 | 1.5153 | 0.0945 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | laxa | precio | 4 | nulo | 2000 | 0.8985 | 0.9925 | 0.4621 | -0.0443 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | laxa | visados | 4 | nulo | 2000 | 0.9060 | 0.9935 | 3.5875 | -0.0414 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | laxa | compraventas | 8 | nulo | 2000 | 0.9710 | 1.0000 | 1.2922 | 0.0424 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | laxa | precio | 8 | nulo | 2000 | 0.9775 | 0.9995 | 0.4088 | -0.0191 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | laxa | visados | 8 | nulo | 2000 | 0.9640 | 0.9995 | 3.3832 | 0.0457 | 0.5723 | False | NO APTO |
| T=48|rho=0.97 | difusa | compraventas | 4 | nulo | 2000 | 0.8275 | 0.9725 | 2.3241 | 0.1086 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | difusa | precio | 4 | nulo | 2000 | 0.7940 | 0.9635 | 0.7287 | -0.0391 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | difusa | visados | 4 | nulo | 2000 | 0.7710 | 0.9585 | 5.1619 | -0.0600 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | difusa | compraventas | 8 | nulo | 2000 | 0.9160 | 0.9930 | 2.1112 | 0.0290 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | difusa | precio | 8 | nulo | 2000 | 0.9230 | 0.9940 | 0.6681 | 0.0063 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | difusa | visados | 8 | nulo | 2000 | 0.8940 | 0.9865 | 5.0917 | 0.1747 | 0.4508 | False | NO APTO |
| T=48|rho=0.97 | principal | compraventas | 4 | alternativa | 2000 | 0.6220 | 0.9680 | 1.1743 | 0.4757 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | principal | precio | 4 | alternativa | 2000 | 0.0070 | 0.1245 | 0.4175 | -0.5117 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | principal | visados | 4 | alternativa | 2000 | 0.6155 | 0.9650 | 2.4145 | 1.0251 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | principal | compraventas | 8 | alternativa | 2000 | 0.7385 | 0.9705 | 1.2896 | -0.4767 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | principal | precio | 8 | alternativa | 2000 | 0.0200 | 0.2750 | 0.5270 | -0.5671 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | principal | visados | 8 | alternativa | 2000 | 0.5695 | 0.9595 | 2.1867 | -1.0466 | 0.6607 | False | NO APTO |
| T=48|rho=0.97 | laxa | compraventas | 4 | alternativa | 2000 | 0.8720 | 0.9900 | 1.3099 | 0.2435 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | laxa | precio | 4 | alternativa | 2000 | 0.0610 | 0.3060 | 0.5020 | -0.5210 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | laxa | visados | 4 | alternativa | 2000 | 0.8150 | 0.9765 | 2.7394 | 0.6495 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | laxa | compraventas | 8 | alternativa | 2000 | 0.7875 | 0.9705 | 1.6156 | -0.3980 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | laxa | precio | 8 | alternativa | 2000 | 0.2385 | 0.6610 | 0.6400 | -0.4593 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | laxa | visados | 8 | alternativa | 2000 | 0.7230 | 0.9545 | 2.6746 | -0.8511 | 0.6163 | False | NO APTO |
| T=48|rho=0.97 | difusa | compraventas | 4 | alternativa | 2000 | 0.8015 | 0.9690 | 2.4024 | -0.0477 | 0.4231 | False | NO APTO |
| T=48|rho=0.97 | difusa | precio | 4 | alternativa | 2000 | 0.4215 | 0.7080 | 0.9045 | -0.4908 | 0.4231 | False | NO APTO |
| T=48|rho=0.97 | difusa | visados | 4 | alternativa | 2000 | 0.7915 | 0.9660 | 5.1182 | 0.4056 | 0.4231 | False | NO APTO |
| T=48|rho=0.97 | difusa | compraventas | 8 | alternativa | 2000 | 0.7355 | 0.9460 | 3.1292 | -0.2003 | 0.4231 | False | NO APTO |
| T=48|rho=0.97 | difusa | precio | 8 | alternativa | 2000 | 0.5975 | 0.8475 | 1.2287 | -0.3890 | 0.4231 | False | NO APTO |
| T=48|rho=0.97 | difusa | visados | 8 | alternativa | 2000 | 0.7795 | 0.9650 | 5.6178 | -0.2859 | 0.4231 | False | NO APTO |

## Notas

- Filas decisivas: prior principal, persistencia 0,97, T = 60 y 74, h = 8, con y sin efecto verdadero, precio, compraventas y visados (la columna `decisivo`).
- La cobertura es la de un intervalo de credibilidad en repetición frecuentista: un prior de Minnesota encoge hacia el paseo aleatorio y puede sesgar la mediana.
- El proceso generador cumple por construcción la identificación recursiva: la cobertura mide solo la incertidumbre de estimación, no el error de especificación.
- R = 2000 réplicas (error típico binomial del 68 % ≈ 0.010); R >= 1.000, como pide el encargo.
