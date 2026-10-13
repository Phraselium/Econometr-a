# M2: SVAR bayesiano con restricciones de signo y de cero (V8-F4)

Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas en docs/v8/hipotesis.md §5; el lenguaje causal queda condicionado a ellas. Referencias de metodo NO VERIFICADAS.

## Avisos

- Aviso (Y6): el BVAR en tasas atenua sistematicamente las IRF hacia cero (sesgo absoluto hasta 0,46; cobertura del 90 % de 0,86-0,90 en F3); las magnitudes de las IRF y de la descomposicion historica se leen como cota inferior aproximada. Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas.
- Las bandas de la descomposicion historica casi nunca excluyen el cero con T de unos 88 (Y6): una contribucion cuya banda incluye el cero se lee como «no distinguible de cero».
- Los dos shocks sin identificar quedan sin restricciones; sus resultados no se interpretan. Los elementos no restringidos solo se leen si su banda excluye el cero (Y4).
- Los pesos de importancia (ceros) son una derivacion propia NO VERIFICADA frente al articulo (Y4).
- Muestra efectiva (V3): 2004Q2-2026Q1 (N=88); la compraventas MIVAU (tx_total) acaba en 2026T1, por lo que P5 cubre 2022T3-2026T1 (15 trimestres) en las variantes de 7 variables y 2022T3-2026T2 en la larga.
- `pob_total` es una interpolacion lineal entre fechas semestrales hasta 2020 (marcada en el panel): la dinamica de n es suave por construccion; las conclusiones sobre el shock demografico dependen de ello.
- Contribuciones en puntos log x100 de la variacion acumulada del periodo (precio y alquiler reales, deflactor IPC); %: contribucion / variacion observada del periodo (inestable si la variacion observada es cercana a cero). La contribucion puntual es la MEDIA posterior (aditiva: la suma de las medias de todos los componentes es la variacion observada; la mediana no lo es, J2); `determinista` (condiciones iniciales + constante + ficticias: COVID 2020T2-T4 e impulso EPA 2021T1) y `no_identificados` son factores aparte y no compiten en el ranking.
- J1 (revision F4): la ficticia EPA 2021 es un IMPULSO en 2021T1 (antes, un escalon desde 2021T1 en las 7 ecuaciones). opcion (b): impulso en 2021T1 en todas las ecuaciones (la opcion (a), solo en la ecuacion de e, exige tocar herramientas/bvar.py). En las predicciones, covid y epa2021 valen 0. La version anterior se conserva como retirada (hipotesis_m2_retirada.csv, hd_periodos_retirada.csv).

## Estado de la identificacion pre-registrada (principal, h = 0-1)

- Sondeo con datos reales: 300 sorteos de theta x 30000 rotaciones = 9.000.000 rotaciones; aceptadas = 1. Estado: **INVIABLE**.
- Operativa: **V3** (solo impacto h = 0, sin la restriccion de q en demanda y oferta; pre-registrada como variante V3, Y6). Las hipotesis H8-1..H8-4, la atribucion y la congelacion usan esta identificacion; la forma reducida congelada es la misma del principal. La V1, V2 y la robustez se estiman tambien con restricciones solo de impacto (V1 h = 0-1 es inviable con datos reales).

## Muestreo y ESS

| variante | N_obs | muestra | p | D_theta | aceptadas | ESS | frac_theta | lam |
|---|---|---|---|---|---|---|---|---|
| V3 | 88 | 2004Q2-2026Q1 | 2 | 720 | 708 | 657 | 0.611 | 0.374 |
| V1 | 88 | 2004Q2-2026Q1 | 2 | 2502 | 728 | 629 | 0.251 | 0.385 |
| V2 | 83 | 2005Q3-2026Q1 | 2 | 707 | 766 | 702 | 0.618 | 0.361 |
| robust_p1 | 88 | 2004Q2-2026Q1 | 1 | 809 | 750 | 692 | 0.577 | 0.296 |
| robust_p4 | 88 | 2004Q2-2026Q1 | 4 | 721 | 658 | 594 | 0.596 | 0.35 |
| robust_prior_fijo | 88 | 2004Q2-2026Q1 | 2 | 764 | 727 | 667 | 0.577 | 0.2 |
| robust_sin_covid | 88 | 2004Q2-2026Q1 | 2 | 897 | 714 | 650 | 0.554 | 0.433 |
| robust_deflactor_pib | 88 | 2004Q2-2026Q1 | 2 | 486 | 610 | 562 | 0.702 | 0.368 |
| larga | 125 | 1995Q2-2026Q2 | 2 | 300 | 6732 | 6.64e+03 | 0.95 | 0.348 |

V3: ESS = 657 (objetivo >= 500); 708 rotaciones aceptadas de 720 sorteos de theta (61.1 % de los theta aportan); lambda GLP = 0.3741; error maximo de la identidad de la DH = 3.7e-12.

## IRF acumuladas (operativa V3) (nivel de p y r, h = 4, 8, 12, 20; mediana [banda 68 %], por shock de 1 d.t.)

**Precio real de compra**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 1.13 [0.38; 2.00] | 1.62 [0.52; 2.73] | 1.87 [0.61; 3.25] | 2.00 [0.56; 3.87] |
| credito | 0.83 [0.13; 1.67] | 1.24 [0.25; 2.43] | 1.56 [0.33; 2.97] | 1.72 [0.34; 3.34] |
| demanda | 0.88 [0.19; 1.65] | 1.19 [0.18; 2.32] | 1.36 [0.16; 2.74] | 1.47 [0.10; 3.16] |
| demografico | 0.69 [-0.14; 1.48] | 0.93 [-0.21; 2.09] | 1.02 [-0.26; 2.48] | 1.02 [-0.42; 2.83] |
| nid1 | -0.10 [-0.99; 0.98] | -0.15 [-1.39; 1.37] | -0.14 [-1.63; 1.53] | -0.15 [-1.97; 1.82] |
| nid2 | 0.07 [-0.91; 0.98] | 0.08 [-1.28; 1.42] | 0.12 [-1.51; 1.61] | 0.08 [-1.73; 1.99] |
| oferta | -0.78 [-1.53; -0.04] | -1.03 [-2.06; -0.00] | -1.19 [-2.48; 0.05] | -1.26 [-2.88; 0.08] |

**Alquiler real**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.35 [0.10; 0.60] | 0.38 [0.07; 0.67] | 0.42 [0.09; 0.72] | 0.50 [0.17; 0.85] |
| credito | -0.00 [-0.35; 0.41] | -0.09 [-0.39; 0.33] | -0.06 [-0.35; 0.33] | 0.05 [-0.29; 0.44] |
| demanda | 0.12 [-0.27; 0.51] | 0.11 [-0.23; 0.51] | 0.14 [-0.21; 0.52] | 0.19 [-0.16; 0.62] |
| demografico | 0.31 [0.09; 0.59] | 0.38 [0.10; 0.64] | 0.45 [0.12; 0.74] | 0.55 [0.18; 0.89] |
| nid1 | 0.02 [-0.38; 0.38] | 0.03 [-0.40; 0.43] | 0.02 [-0.45; 0.47] | -0.01 [-0.56; 0.57] |
| nid2 | 0.00 [-0.36; 0.36] | -0.01 [-0.39; 0.39] | 0.02 [-0.46; 0.47] | 0.04 [-0.57; 0.57] |
| oferta | -0.27 [-0.61; 0.16] | -0.24 [-0.56; 0.14] | -0.22 [-0.56; 0.15] | -0.25 [-0.60; 0.10] |

## FEVD (V3 operativa) (mediana; h = 4, 8, 12, 20)

**Precio real de compra**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.145 | 0.148 | 0.146 | 0.145 |
| credito | 0.089 | 0.095 | 0.098 | 0.101 |
| demanda | 0.101 | 0.098 | 0.099 | 0.101 |
| demografico | 0.081 | 0.086 | 0.086 | 0.085 |
| nid1 | 0.076 | 0.080 | 0.083 | 0.090 |
| nid2 | 0.074 | 0.079 | 0.079 | 0.085 |
| oferta | 0.099 | 0.103 | 0.105 | 0.107 |

**Alquiler real**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.086 | 0.085 | 0.084 | 0.086 |
| credito | 0.097 | 0.096 | 0.096 | 0.096 |
| demanda | 0.095 | 0.094 | 0.092 | 0.091 |
| demografico | 0.082 | 0.084 | 0.085 | 0.086 |
| nid1 | 0.093 | 0.102 | 0.105 | 0.107 |
| nid2 | 0.082 | 0.095 | 0.101 | 0.102 |
| oferta | 0.126 | 0.131 | 0.134 | 0.134 |

## Descomposicion historica (V3 operativa) por periodo y mercado

**compra** (pp log x100; media [68 %]; [90 %]; P(>0))

| factor | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| actividad | -10.6 [-23.5; 0.7] (-38.8; 7.3) p+=0.19 (med -7.6) | 7.7 [-3.5; 18.2] (-15.2; 31.2) p+=0.72 (med 5.2) | 0.3 [-7.1; 4.7] (-13.2; 10.2) p+=0.46 (med -0.5) | 7.2 [-4.7; 11.2] (-10.8; 22.7) p+=0.57 (med 1.1) |
| credito | -8.6 [-18.9; 0.5] (-32.9; 5.2) p+=0.22 (med -5.9) | -1.6 [-9.8; 7.1] (-17.7; 18.4) p+=0.45 (med -0.7) | -1.3 [-4.7; 4.4] (-10.0; 9.2) p+=0.51 (med 0.1) | -0.5 [-2.8; 12.8] (-9.9; 20.7) p+=0.71 (med 3.4) |
| demanda | -7.4 [-17.9; 2.0] (-34.0; 6.1) p+=0.29 (med -3.5) | -0.4 [-7.2; 9.0] (-18.4; 17.7) p+=0.55 (med 0.5) | -2.6 [-6.0; 2.4] (-12.3; 6.0) p+=0.41 (med -0.7) | -0.3 [-2.9; 11.0] (-10.8; 19.5) p+=0.70 (med 2.4) |
| demografico | -2.9 [-10.7; 4.0] (-20.6; 11.1) p+=0.38 (med -1.6) | 0.1 [-6.6; 6.8] (-14.0; 17.3) p+=0.48 (med -0.2) | -0.3 [-4.0; 3.4] (-8.2; 7.1) p+=0.51 (med 0.1) | 0.6 [-4.1; 5.8] (-9.0; 13.4) p+=0.56 (med 0.6) |
| determinista | -1.8 [-16.4; 13.2] (-26.8; 25.8) p+=0.40 (med -3.2) | 0.3 [-15.3; 14.2] (-29.5; 27.3) p+=0.45 (med -2.3) | -0.9 [-10.7; 6.6] (-17.5; 12.5) p+=0.41 (med -2.0) | 5.4 [-8.8; 11.8] (-18.6; 21.0) p+=0.53 (med 0.9) |
| no_identificados | -7.9 [-18.8; 2.3] (-29.6; 12.1) p+=0.23 (med -6.5) | 1.6 [-9.9; 13.4] (-22.4; 26.7) p+=0.53 (med 0.8) | 0.2 [-5.4; 5.4] (-10.2; 10.1) p+=0.50 (med 0.0) | 4.2 [-5.7; 12.3] (-15.1; 20.8) p+=0.65 (med 2.9) |
| oferta | -4.8 [-13.3; 2.5] (-25.0; 7.6) p+=0.34 (med -2.1) | 0.4 [-7.3; 8.0] (-16.8; 19.0) p+=0.52 (med 0.2) | -0.8 [-4.8; 3.3] (-10.0; 7.5) p+=0.46 (med -0.3) | 1.9 [-3.3; 9.0] (-10.1; 16.9) p+=0.68 (med 1.8) |

Variacion observada (pp): P2 = -44.0; P3 = 8.2; P4 = -5.5; P5 = 18.4

**alquiler** (pp log x100; media [68 %]; [90 %]; P(>0))

| factor | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| actividad | -1.7 [-4.3; 0.8] (-6.9; 2.7) p+=0.29 (med -1.2) | 1.7 [-1.1; 4.8] (-3.6; 8.0) p+=0.68 (med 1.4) | -0.8 [-2.8; 0.6] (-4.2; 1.6) p+=0.32 (med -0.6) | 0.5 [-1.9; 2.1] (-3.4; 3.9) p+=0.49 (med -0.1) |
| credito | 0.3 [-1.5; 2.1] (-3.3; 3.6) p+=0.59 (med 0.3) | 0.2 [-1.7; 2.7] (-3.6; 4.8) p+=0.53 (med 0.2) | -1.5 [-3.2; 0.3] (-5.2; 1.1) p+=0.24 (med -0.9) | -0.5 [-2.6; 2.3] (-4.3; 4.3) p+=0.49 (med -0.0) |
| demanda | -0.3 [-2.3; 1.8] (-5.0; 3.3) p+=0.48 (med -0.1) | 0.7 [-1.4; 2.9] (-3.3; 5.4) p+=0.64 (med 0.6) | -1.6 [-3.2; 0.1] (-5.1; 0.9) p+=0.18 (med -1.3) | -0.3 [-2.0; 2.0] (-4.3; 4.1) p+=0.50 (med 0.0) |
| demografico | 0.3 [-1.9; 2.7] (-4.6; 4.9) p+=0.56 (med 0.2) | -0.0 [-2.9; 2.7] (-5.5; 5.5) p+=0.47 (med -0.1) | -0.7 [-2.3; 0.7] (-4.1; 1.9) p+=0.35 (med -0.5) | 0.1 [-1.9; 2.1] (-3.7; 4.1) p+=0.51 (med 0.0) |
| determinista | -2.3 [-5.5; 1.0] (-7.9; 4.5) p+=0.21 (med -2.6) | -3.5 [-6.9; -0.1] (-10.9; 4.4) p+=0.16 (med -3.8) | -1.1 [-3.8; 1.2] (-5.3; 3.6) p+=0.33 (med -1.1) | -3.6 [-6.6; -0.9] (-9.4; 0.8) p+=0.09 (med -3.8) |
| no_identificados | 1.1 [-2.0; 4.2] (-4.5; 6.8) p+=0.65 (med 1.1) | -1.0 [-4.7; 2.9] (-7.4; 6.2) p+=0.38 (med -1.3) | -2.1 [-4.3; 0.2] (-6.4; 1.2) p+=0.18 (med -1.9) | 1.6 [-1.3; 4.5] (-4.0; 7.2) p+=0.69 (med 1.4) |
| oferta | -0.1 [-2.0; 1.9] (-3.9; 3.7) p+=0.52 (med 0.1) | 0.9 [-1.1; 3.2] (-2.8; 6.0) p+=0.63 (med 0.6) | -1.6 [-3.6; 0.1] (-5.3; 0.8) p+=0.19 (med -1.1) | 0.4 [-1.8; 2.6] (-3.4; 4.6) p+=0.57 (med 0.3) |

Variacion observada (pp): P2 = -2.7; P3 = -1.1; P4 = -9.3; P5 = -1.8

## Hipotesis confirmatorias H8-1 a H8-4 (Holm en la familia)

| id | mercado | periodo | factor | signo_esperado | contribucion_pp | b68_lo | b68_hi | b90_lo | b90_hi | prob_posterior | p_unilateral | p_holm | estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H8-1 | alquiler | P5 | demografico | 1 | 0.074 | -1.919 | 2.132 | -3.738 | 4.100 | 0.506 | 0.494 | 0.987 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |
| H8-2 | compra | P5 | credito | -1 | -0.469 | -2.819 | 12.773 | -9.852 | 20.669 | 0.293 | 0.707 | 0.987 | no respaldada (la mediana apunta al signo contrario o no distingue) |
| H8-3 | compra | P3 | actividad | 1 | 7.722 | -3.466 | 18.232 | -15.239 | 31.205 | 0.721 | 0.279 | 0.838 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |
| H8-4 | compra | P2 | credito+actividad | -1 | -19.232 | -34.586 | -4.146 | -50.193 | 4.594 | 0.914 | 0.086 | 0.343 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |

Lectura: cada p es 1 - P(posterior del signo esperado); resolucion minima de p = 1/ESS. Resultados bajo los supuestos de identificacion (C3s); magnitudes atenuadas (Y6).

## Variantes y robustez: contribucion media de cada hipotesis (pp) y P(signo esperado)

| variante | ESS | H8-1 | H8-2 | H8-3 | H8-4 |
|---|---|---|---|---|---|
| V3 | 657 | 0.1 (P=0.51) | -0.5 (P=0.29) | 7.7 (P=0.72) | -19.2 (P=0.91) |
| V1 | 629 | -2.5 (P=0.47) | -7.5 (P=0.44) | -1.2 (P=0.63) | -17.1 (P=0.85) |
| V2 | 702 | 737.5 (P=0.47) | -1419.1 (P=0.40) | 13.5 (P=0.57) | -24.7 (P=0.82) |
| robust_p1 | 692 | 0.0 (P=0.53) | 2.3 (P=0.40) | 5.8 (P=0.76) | -15.9 (P=0.90) |
| robust_p4 | 594 | 0.3 (P=0.56) | 5.4 (P=0.29) | 3.5 (P=0.67) | -18.3 (P=0.84) |
| robust_prior_fijo | 667 | 0.2 (P=0.53) | 3.3 (P=0.34) | 5.8 (P=0.73) | -18.4 (P=0.93) |
| robust_sin_covid | 650 | 0.0 (P=0.56) | 5.1 (P=0.27) | 7.1 (P=0.76) | -20.1 (P=0.91) |
| robust_deflactor_pib | 562 | -0.4 (P=0.42) | 1.8 (P=0.43) | 1.9 (P=0.59) | -12.6 (P=0.84) |

Celdas: media de la contribucion conjunta en pp (P = probabilidad posterior del signo esperado). En V1 el shock «credito» no incluye el monetario (H8-2/H8-4 con V1 usan solo `credito`; `monetario` esta en hd_periodos.csv). V1, V2 y la robustez usan la identificacion operativa solo de impacto. n.c. = periodo no cubierto o factor no definido en esa variante.

## Version larga (4 variables, 1995T2-2026T2): contribucion a la variacion del precio real de compra (pp)

| factor | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| actividad | 31.8 [9.0; 54.6] | -31.3 [-48.7; -12.2] | -1.0 [-11.8; 10.1] | -6.2 [-12.6; 0.0] | 4.2 [-1.9; 10.8] |
| credito_tipos | 3.0 [-7.2; 14.0] | -9.5 [-22.6; 2.1] | 6.5 [-0.7; 14.6] | 0.1 [-4.4; 4.9] | 1.0 [-3.2; 5.6] |
| demografico | 8.9 [-5.0; 24.8] | -7.8 [-20.8; 3.6] | -6.0 [-18.3; 5.0] | -0.5 [-5.3; 4.1] | 4.3 [-2.1; 11.0] |
| determinista | 23.1 [-1.0; 50.3] | 12.0 [-0.4; 22.5] | 13.6 [-0.6; 26.0] | 1.5 [-7.7; 10.0] | 4.8 [-5.5; 14.4] |
| no_identificados | 8.5 [-5.0; 23.8] | -7.5 [-20.5; 3.4] | -4.9 [-16.8; 5.7] | -0.4 [-5.1; 4.2] | 4.2 [-2.0; 10.9] |

ESS larga = 6640. Es un contraste (C3s) con 4 variables; el shock `residual` no esta identificado.

## H8-1 a H8-4: version corregida (principal) frente a la retirada (especificacion erronea, escalon EPA)

| id | contribucion_pp | contribucion_pp_retirada | prob_posterior | prob_posterior_retirada | p_holm | p_holm_retirada |
|---|---|---|---|---|---|---|
| H8-1 | 0.074 | 0.667 | 0.506 | 0.684 | 0.987 | 0.817 |
| H8-2 | -0.469 | -0.412 | 0.293 | 0.543 | 0.987 | 0.817 |
| H8-3 | 7.722 | 4.078 | 0.721 | 0.728 | 0.838 | 0.817 |
| H8-4 | -19.232 | -14.327 | 0.914 | 0.893 | 0.343 | 0.428 |

La retirada usa la MEDIANA como contribucion; la corregida usa la MEDIA posterior (mediana en hipotesis_m2.csv, columna `mediana`).

Parte determinista de P5: compra: 17.8 (mediana, retirada) -> 5.4 (media) / 0.9 (mediana); alquiler: -8.4 (mediana, retirada) -> -3.6 (media) / -3.8 (mediana).

## Congelacion para evaluate_v8 (§10)

- Fichero: output/v8/M2/predicciones_congeladas.csv; sha256 = `5009f0448646d1d8d8461aa09df5a41c9dfa1b4d2d66ff9ba2e4194e181aa99c` (congelacion.json); sha256 anterior retirado = `bd23db78e3342c6865bb1285108d0943a70f0c0d4e1b5b07085491295f509a9e`.
- tx_total (compraventas MIVAU) acaba en 2026T1, por lo que la muestra comun del BVAR principal acaba en 2026T1 y el origen es 2026T1 (no 2026T2): h=1 (2026T2) ya es un dato y NO se evalua; las filas evaluables son h=2..5 desde 2026T1 = h=1..4 desde 2026T2 (docs/v8/desviaciones.md).

## Desviaciones y decisiones de ejecucion

- J1: ficticia EPA 2021 = impulso en 2021T1 (no escalon). opcion (b): impulso en 2021T1 en todas las ecuaciones (la opcion (a), solo en la ecuacion de e, exige tocar herramientas/bvar.py). COVID como pre-registrado (2020T2-T4, escalon de episodio); en predicciones futuras ambas valen 0. Se aplica a V3, V1, V2 y robustez; en 'sin 2020-2021' el impulso coincide con la ficticia d2021Q1 (se conserva una). La version larga no lleva EPA.
- La identificacion principal pre-registrada (7 variables, signos en h=0-1, 4 ceros) es INVIABLE con datos reales (sondeo: 0 aceptadas en 9.000.000 rotaciones); se usa V3 (solo impacto, sin q en demanda ni oferta; Y6) como identificacion operativa para H8-1..H8-4, atribucion y robustez. V1 se estima solo en el impacto (con h=0-1: 0 aceptadas).
- Muestra efectiva (7 variables) 2004T2-2026T1 (N=88, HD desde 2004T4): tx_total acaba en 2026T1 y las tasas empiezan en 2004T2; la muestra «2004T1-2026T2» del pre-registro se reduce por disponibilidad conjunta.
- Origen de la congelacion: 2026T1 (ultimo trimestre de la muestra comun); h=2..5 desde 2026T1 equivale a h=1..4 desde 2026T2 (2026T2 de p y r ya esta publicado y no se evalua).
- Factor 'demanda_vivienda' en atribucion.csv: demanda especifica de vivienda, no incluida en la lista de factores del contrato (declarado en notas).
- V2: el HPI de la zona euro (EA20) incluye a Espana (peso no verificado); entra como exogena contemporanea y con un retardo; 'factor_europeo' = su efecto estimado (directo y propagado).
- Robustez 'prior fijo': lambda = 0,2 sin optimizar; 'sin 2020-2021': ficticias de impulso 2020T1-2021T4 en lugar de la ficticia COVID; 'deflactor PIB' en p, r y c.
- Version larga: ficticia COVID como unica exogena (la EPA no entra); el shock 'residual' queda sin identificar y sin ceros.
- J2: contribucion_pp = media posterior; determinista y no_identificados por separado; suma de medias = variacion observada (diagnosticos.cierre_medias_max).
- IRF para un shock de 1 desviacion tipica (columnas de A0inv = chol(Sigma) Q); irf_acumulada.csv acumula las IRF de las variables en tasa (nivel de p, r, q, c, e, n).
