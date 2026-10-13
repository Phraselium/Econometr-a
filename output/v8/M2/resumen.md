# M2: SVAR bayesiano con restricciones de signo y de cero (V8-F4)

Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas en docs/v8/hipotesis.md §5; el lenguaje causal queda condicionado a ellas. Referencias de metodo NO VERIFICADAS.

## Avisos

- Aviso (Y6): el BVAR en tasas atenua sistematicamente las IRF hacia cero (sesgo absoluto hasta 0,46; cobertura del 90 % de 0,86-0,90 en F3); las magnitudes de las IRF y de la descomposicion historica se leen como cota inferior aproximada. Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas.
- Las bandas de la descomposicion historica casi nunca excluyen el cero con T de unos 88 (Y6): una contribucion cuya banda incluye el cero se lee como «no distinguible de cero».
- Los dos shocks sin identificar quedan sin restricciones; sus resultados no se interpretan. Los elementos no restringidos solo se leen si su banda excluye el cero (Y4).
- Los pesos de importancia (ceros) son una derivacion propia NO VERIFICADA frente al articulo (Y4).
- Muestra efectiva (V3): 2004Q2-2026Q1 (N=88); la compraventas MIVAU (tx_total) acaba en 2026T1, por lo que P5 cubre 2022T3-2026T1 (15 trimestres) en el principal y 2022T3-2026T2 en la larga.
- `pob_total` es una interpolacion lineal entre fechas semestrales hasta 2020 (marcada en el panel): la dinamica de n es suave por construccion; las conclusiones sobre el shock demografico dependen de ello.
- Contribuciones en puntos log x100 de la variacion acumulada del periodo (precio y alquiler reales, deflactor IPC); %: contribucion / variacion observada del periodo (inestable si la variacion observada es cercana a cero). `determinista` = condiciones iniciales + constante + ficticias (COVID, EPA 2021T1).

## Estado de la identificacion pre-registrada (principal, h = 0-1)

- Sondeo con datos reales: 300 sorteos de theta x 30000 rotaciones = 9.000.000 rotaciones; aceptadas = 0. Estado: **INVIABLE**.
- Operativa: **V3** (solo impacto h = 0, sin la restriccion de q en demanda y oferta; pre-registrada como variante V3, Y6). Las hipotesis H8-1..H8-4, la atribucion y la congelacion usan esta identificacion; la forma reducida congelada es la misma del principal. La V1, V2 y la robustez se estiman tambien con restricciones solo de impacto (V1 h = 0-1 es inviable con datos reales).

## Muestreo y ESS

| variante | N_obs | muestra | p | D_theta | aceptadas | ESS | frac_theta | lam |
|---|---|---|---|---|---|---|---|---|
| V3 | 88 | 2004Q2-2026Q1 | 2 | 738 | 730 | 671 | 0.618 | 0.371 |
| V1 | 88 | 2004Q2-2026Q1 | 2 | 2647 | 736 | 643 | 0.238 | 0.378 |
| V2 | 83 | 2005Q3-2026Q1 | 2 | 817 | 924 | 838 | 0.676 | 0.359 |
| robust_p1 | 88 | 2004Q2-2026Q1 | 1 | 766 | 719 | 661 | 0.587 | 0.302 |
| robust_p4 | 88 | 2004Q2-2026Q1 | 4 | 760 | 676 | 613 | 0.576 | 0.342 |
| robust_prior_fijo | 88 | 2004Q2-2026Q1 | 2 | 771 | 731 | 678 | 0.584 | 0.2 |
| robust_sin_covid | 88 | 2004Q2-2026Q1 | 2 | 882 | 712 | 647 | 0.542 | 0.438 |
| robust_deflactor_pib | 88 | 2004Q2-2026Q1 | 2 | 468 | 646 | 598 | 0.72 | 0.386 |
| larga | 125 | 1995Q2-2026Q2 | 2 | 300 | 6732 | 6.64e+03 | 0.95 | 0.348 |

V3: ESS = 671 (objetivo >= 500); 730 rotaciones aceptadas de 738 sorteos de theta (61.8 % de los theta aportan); lambda GLP = 0.3712; error maximo de la identidad de la DH = 8.2e-13.

## IRF acumuladas (operativa V3) (nivel de p y r, h = 4, 8, 12, 20; mediana [banda 68 %], por shock de 1 d.t.)

**Precio real de compra**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 1.16 [0.48; 1.91] | 1.53 [0.61; 2.60] | 1.74 [0.66; 3.04] | 1.84 [0.61; 3.41] |
| credito | 0.77 [0.19; 1.47] | 1.14 [0.31; 2.10] | 1.37 [0.36; 2.50] | 1.54 [0.34; 2.95] |
| demanda | 0.71 [0.13; 1.54] | 0.96 [0.11; 2.12] | 1.09 [0.09; 2.45] | 1.14 [0.05; 2.74] |
| demografico | 0.86 [-0.02; 1.59] | 1.11 [-0.03; 2.17] | 1.22 [-0.08; 2.53] | 1.24 [-0.29; 2.81] |
| nid1 | 0.04 [-0.91; 1.00] | 0.08 [-1.22; 1.38] | 0.10 [-1.36; 1.60] | 0.12 [-1.61; 1.85] |
| nid2 | -0.00 [-0.99; 0.91] | 0.01 [-1.41; 1.27] | 0.03 [-1.76; 1.53] | -0.10 [-1.99; 1.73] |
| oferta | -0.78 [-1.56; -0.18] | -1.01 [-2.10; -0.15] | -1.16 [-2.47; -0.14] | -1.24 [-2.80; -0.13] |

**Alquiler real**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.32 [0.10; 0.54] | 0.37 [0.12; 0.61] | 0.41 [0.15; 0.66] | 0.49 [0.19; 0.80] |
| credito | 0.09 [-0.22; 0.40] | 0.07 [-0.21; 0.35] | 0.08 [-0.18; 0.38] | 0.16 [-0.12; 0.50] |
| demanda | 0.13 [-0.17; 0.43] | 0.15 [-0.14; 0.42] | 0.19 [-0.11; 0.45] | 0.21 [-0.09; 0.55] |
| demografico | 0.31 [0.08; 0.54] | 0.38 [0.11; 0.66] | 0.46 [0.15; 0.75] | 0.53 [0.22; 0.92] |
| nid1 | 0.00 [-0.30; 0.30] | 0.01 [-0.37; 0.36] | 0.01 [-0.43; 0.44] | 0.00 [-0.52; 0.53] |
| nid2 | 0.02 [-0.31; 0.32] | -0.00 [-0.37; 0.35] | -0.02 [-0.45; 0.41] | -0.02 [-0.56; 0.50] |
| oferta | -0.26 [-0.55; 0.08] | -0.25 [-0.54; 0.06] | -0.26 [-0.57; 0.05] | -0.28 [-0.65; 0.05] |

## FEVD (V3 operativa) (mediana; h = 4, 8, 12, 20)

**Precio real de compra**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.160 | 0.159 | 0.154 | 0.151 |
| credito | 0.076 | 0.087 | 0.088 | 0.089 |
| demanda | 0.083 | 0.082 | 0.084 | 0.085 |
| demografico | 0.103 | 0.104 | 0.105 | 0.106 |
| nid1 | 0.069 | 0.075 | 0.080 | 0.084 |
| nid2 | 0.070 | 0.078 | 0.080 | 0.085 |
| oferta | 0.093 | 0.095 | 0.096 | 0.097 |

**Alquiler real**

| shock | 4 | 8 | 12 | 20 |
|---|---|---|---|---|
| actividad | 0.082 | 0.082 | 0.081 | 0.082 |
| credito | 0.099 | 0.098 | 0.098 | 0.097 |
| demanda | 0.087 | 0.086 | 0.085 | 0.086 |
| demografico | 0.075 | 0.079 | 0.083 | 0.086 |
| nid1 | 0.088 | 0.099 | 0.104 | 0.104 |
| nid2 | 0.083 | 0.095 | 0.101 | 0.101 |
| oferta | 0.144 | 0.149 | 0.152 | 0.151 |

## Descomposicion historica (V3 operativa) por periodo y mercado

**compra** (pp log x100; mediana [68 %]; [90 %]; P(>0))

| factor | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| actividad | -7.7 [-22.2; -0.2] (-32.0; 3.1) p+=0.14 | 4.1 [-2.3; 16.7] (-9.3; 29.6) p+=0.73 | -1.0 [-7.0; 3.0] (-16.1; 7.7) p+=0.38 | 1.1 [-4.7; 9.0] (-12.9; 17.3) p+=0.59 |
| credito | -3.2 [-13.6; 1.5] (-24.3; 6.4) p+=0.28 | 1.1 [-4.3; 9.9] (-13.1; 19.4) p+=0.60 | 0.0 [-3.8; 3.5] (-7.9; 7.0) p+=0.51 | -0.4 [-6.4; 4.6] (-11.7; 9.7) p+=0.46 |
| demanda | -2.3 [-13.8; 1.4] (-25.2; 4.9) p+=0.28 | 1.2 [-4.4; 9.1] (-11.9; 21.8) p+=0.59 | -0.5 [-5.1; 2.7] (-10.5; 6.0) p+=0.43 | 0.3 [-4.8; 5.3] (-13.6; 10.7) p+=0.53 |
| demografico | -1.8 [-11.4; 3.9] (-21.8; 9.6) p+=0.37 | -0.1 [-7.5; 7.6] (-18.0; 17.4) p+=0.49 | -0.4 [-4.8; 2.7] (-10.3; 6.3) p+=0.43 | 0.5 [-5.2; 5.5] (-13.4; 12.0) p+=0.53 |
| determinista | -9.6 [-21.7; 5.4] (-34.2; 20.2) p+=0.26 | -8.5 [-22.5; 6.0] (-34.7; 21.8) p+=0.29 | 1.8 [-7.0; 9.5] (-12.2; 14.4) p+=0.58 | 17.8 [1.5; 34.1] (-7.4; 52.1) p+=0.87 |
| no_identificados | -5.4 [-19.3; 3.3] (-30.0; 10.7) p+=0.27 | 1.8 [-8.4; 14.2] (-17.5; 25.7) p+=0.57 | -1.2 [-6.7; 3.8] (-13.1; 8.8) p+=0.40 | 0.3 [-9.2; 7.1] (-19.3; 13.9) p+=0.52 |
| oferta | -2.0 [-11.8; 2.6] (-22.6; 7.7) p+=0.33 | 1.0 [-4.1; 9.7] (-10.5; 19.8) p+=0.58 | -0.8 [-4.9; 1.8] (-9.8; 6.8) p+=0.37 | 0.1 [-6.1; 4.6] (-11.6; 9.1) p+=0.52 |

Variacion observada (pp): P2 = -44.0; P3 = 8.2; P4 = -5.5; P5 = 18.4

**alquiler** (pp log x100; mediana [68 %]; [90 %]; P(>0))

| factor | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| actividad | -1.5 [-4.5; 0.3] (-7.0; 1.6) p+=0.21 | 1.0 [-1.0; 3.5] (-2.7; 6.7) p+=0.68 | -0.5 [-2.4; 0.6] (-3.8; 1.6) p+=0.35 | 0.4 [-1.0; 2.4] (-2.7; 4.9) p+=0.62 |
| credito | 0.1 [-1.4; 1.6] (-3.1; 3.1) p+=0.55 | 0.1 [-1.2; 1.7] (-2.5; 3.7) p+=0.53 | -0.6 [-2.2; 0.4] (-3.6; 1.1) p+=0.30 | 0.8 [-0.5; 2.5] (-1.5; 4.3) p+=0.71 |
| demanda | -0.0 [-1.9; 1.4] (-4.2; 3.0) p+=0.49 | 0.4 [-1.1; 2.2] (-2.8; 4.9) p+=0.61 | -0.7 [-2.4; 0.3] (-3.8; 1.0) p+=0.25 | 0.5 [-0.8; 2.6] (-2.1; 4.5) p+=0.66 |
| demografico | -0.0 [-2.6; 2.0] (-5.9; 4.1) p+=0.49 | -0.6 [-3.5; 1.8] (-6.2; 4.7) p+=0.39 | -0.4 [-2.2; 0.8] (-3.8; 1.9) p+=0.36 | 0.7 [-1.1; 2.6] (-2.9; 4.8) p+=0.68 |
| determinista | -0.7 [-4.2; 3.3] (-7.3; 7.0) p+=0.42 | -1.4 [-5.9; 3.1] (-9.3; 7.4) p+=0.36 | -3.3 [-5.6; -0.8] (-7.8; 0.8) p+=0.08 | -8.4 [-12.3; -4.1] (-16.1; -0.8) p+=0.03 |
| no_identificados | 0.6 [-2.6; 3.3] (-5.3; 5.0) p+=0.59 | -1.3 [-5.1; 1.9] (-8.8; 4.7) p+=0.36 | -1.5 [-3.8; 0.3] (-5.6; 1.4) p+=0.21 | 2.1 [-0.3; 5.2] (-2.6; 7.1) p+=0.80 |
| oferta | -0.2 [-2.3; 1.6] (-4.3; 3.1) p+=0.46 | 0.4 [-1.2; 2.2] (-2.5; 4.5) p+=0.62 | -1.0 [-2.9; 0.1] (-4.4; 0.7) p+=0.21 | 0.8 [-0.6; 3.1] (-2.1; 5.3) p+=0.71 |

Variacion observada (pp): P2 = -2.7; P3 = -1.1; P4 = -9.3; P5 = -1.8

## Hipotesis confirmatorias H8-1 a H8-4 (Holm en la familia)

| id | mercado | periodo | factor | signo_esperado | contribucion_pp | b68_lo | b68_hi | b90_lo | b90_hi | prob_posterior | p_unilateral | p_holm | estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H8-1 | alquiler | P5 | demografico | 1 | 0.667 | -1.062 | 2.649 | -2.891 | 4.792 | 0.684 | 0.316 | 0.817 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |
| H8-2 | compra | P5 | credito | -1 | -0.412 | -6.378 | 4.568 | -11.689 | 9.680 | 0.543 | 0.457 | 0.817 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |
| H8-3 | compra | P3 | actividad | 1 | 4.078 | -2.263 | 16.690 | -9.340 | 29.628 | 0.728 | 0.272 | 0.817 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |
| H8-4 | compra | P2 | credito+actividad | -1 | -14.327 | -29.344 | -2.540 | -42.223 | 3.268 | 0.893 | 0.107 | 0.428 | no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5) |

Lectura: cada p es 1 - P(posterior del signo esperado); resolucion minima de p = 1/ESS. Resultados bajo los supuestos de identificacion (C3s); magnitudes atenuadas (Y6).

## Variantes y robustez: contribucion mediana de cada hipotesis (pp) y P(signo esperado)

| variante | ESS | H8-1 | H8-2 | H8-3 | H8-4 |
|---|---|---|---|---|---|
| V3 | 671 | 0.7 (P=0.68) | -0.4 (P=0.54) | 4.1 (P=0.73) | -14.3 (P=0.89) |
| V1 | 643 | 0.7 (P=0.67) | 0.2 (P=0.47) | 3.4 (P=0.70) | -12.4 (P=0.87) |
| V2 | 838 | 0.5 (P=0.58) | -0.0 (P=0.50) | 3.8 (P=0.63) | -14.3 (P=0.80) |
| robust_p1 | 661 | 0.7 (P=0.65) | -0.1 (P=0.51) | 4.4 (P=0.74) | -13.3 (P=0.91) |
| robust_p4 | 613 | 0.5 (P=0.67) | -0.3 (P=0.53) | 4.2 (P=0.72) | -10.1 (P=0.83) |
| robust_prior_fijo | 678 | 0.7 (P=0.67) | -0.2 (P=0.53) | 4.0 (P=0.77) | -14.6 (P=0.91) |
| robust_sin_covid | 647 | 0.5 (P=0.65) | -0.3 (P=0.53) | 5.8 (P=0.74) | -16.7 (P=0.91) |
| robust_deflactor_pib | 598 | 0.1 (P=0.55) | -0.3 (P=0.55) | 0.7 (P=0.60) | -9.0 (P=0.88) |

V1 y V3 y robustez comparten la misma lectura; en V1 el shock «credito» no incluye el monetario (H8-2/H8-4 con V1 usan solo `credito`; ver hd_periodos.csv para `monetario`). n.c. = periodo no cubierto o factor no definido en esa variante.

## Version larga (4 variables, 1995T2-2026T2): contribucion a la variacion del precio real de compra (pp)

| factor | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| actividad | 29.5 [9.0; 54.6] | -32.3 [-48.7; -12.2] | -1.6 [-11.8; 10.1] | -5.7 [-12.6; 0.0] | 4.3 [-1.9; 10.8] |
| credito_tipos | 0.1 [-7.2; 14.0] | -5.5 [-22.6; 2.1] | 5.0 [-0.7; 14.6] | 0.2 [-4.4; 4.9] | 0.8 [-3.2; 5.6] |
| demografico | 4.8 [-5.0; 24.8] | -4.5 [-20.8; 3.6] | -4.1 [-18.3; 5.0] | -0.5 [-5.3; 4.1] | 3.0 [-2.1; 11.0] |
| determinista | 22.5 [-1.0; 50.3] | 12.9 [-0.4; 22.5] | 14.1 [-0.6; 26.0] | 1.6 [-7.7; 10.0] | 5.8 [-5.5; 14.4] |
| no_identificados | 4.5 [-5.0; 23.8] | -3.9 [-20.5; 3.4] | -2.7 [-16.8; 5.7] | -0.4 [-5.1; 4.2] | 2.9 [-2.0; 10.9] |

ESS larga = 6640. Es un contraste (C3s) con 4 variables; el shock `residual` no esta identificado.

## Congelacion para evaluate_v8 (§10)

- Fichero: output/v8/M2/predicciones_congeladas.csv; sha256 = `bd23db78e3342c6865bb1285108d0943a70f0c0d4e1b5b07085491295f509a9e` (congelacion.json).
- tx_total (compraventas MIVAU) acaba en 2026T1, por lo que la muestra comun del BVAR principal acaba en 2026T1 y el origen es 2026T1 (no 2026T2): h=1 (2026T2) ya es un dato y NO se evalua; las filas evaluables son h=2..5 desde 2026T1 = h=1..4 desde 2026T2 (docs/v8/desviaciones.md).

## Desviaciones y decisiones de ejecucion

- La identificacion principal pre-registrada (7 variables, signos en h=0-1, 4 ceros) es INVIABLE con datos reales (sondeo: 0 aceptadas en 9.000.000 rotaciones); se usa V3 (solo impacto, sin q en demanda ni oferta; Y6) como identificacion operativa para H8-1..H8-4, atribucion y robustez. V1 se estima solo en el impacto (con h=0-1: 0 aceptadas).
- Muestra efectiva (7 variables) 2004T2-2026T1 (N=88, HD desde 2004T4): tx_total acaba en 2026T1 y las tasas empiezan en 2004T2; la muestra «2004T1-2026T2» del pre-registro se reduce por disponibilidad conjunta.
- Origen de la congelacion: 2026T1 (ultimo trimestre de la muestra comun); h=2..5 desde 2026T1 equivale a h=1..4 desde 2026T2 (2026T2 de p y r ya esta publicado y no se evalua).
- Factor 'demanda_vivienda' en atribucion.csv: demanda especifica de vivienda, no incluida en la lista de factores del contrato (declarado en notas).
- V2: el HPI de la zona euro (EA20) incluye a Espana (peso no verificado); entra como exogena contemporanea y con un retardo; 'factor_europeo' = su efecto estimado (directo y propagado).
- Robustez 'prior fijo': lambda = 0,2 sin optimizar; 'sin 2020-2021': ficticias de impulso 2020T1-2021T4 en lugar de la ficticia COVID; 'deflactor PIB' en p, r y c.
- Version larga: ficticia COVID como unica exogena (la EPA no entra); el shock 'residual' queda sin identificar y sin ceros.
- IRF para un shock de 1 desviacion tipica (columnas de A0inv = chol(Sigma) Q); irf_acumulada.csv acumula las IRF de las variables en tasa (nivel de p, r, q, c, e, n).
