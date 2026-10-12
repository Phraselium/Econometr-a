# Resumen R4a, alquiler (informativo, muestra ya vista en v1; capa C4; asociacion de largo plazo, sin lenguaje causal)

## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)

| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |
|---|---|---|---|---|---|---|---|
| H7-A1 | ln_ocupados (spec A) | 0.048 | 0.081 | -0.008 | [-0.008, 0.081] | 0.5869 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A2 | ln_pob_total (spec A) | -0.154 | -0.357 | 0.161 | [-0.357, 0.161] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A3 | tasa_paro_epa (spec B) | 0.001 | -0.003 | 0.000 | [-0.003, 0.001] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |

## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman

| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |
|---|---|---|---|---|---|---|---|
| A | -0.109 | -3.55 | False | 0.715 | 0.078 | 0.059 | 0.200 |
| B | -0.061 | -2.13 | False | 0.057 | 0.843 | 0.314 | 0.150 |

Heterogeneidad de phi_i, spec A: media -0.109, mediana -0.130, DE 0.075, min -0.176, max 0.034; phi_i<0 en 5/6; semivida mediana 4.5 trimestres; BH q<0,10 en phi_i: 5/6 (t convencional, aproximado).
Diagnosticos spec A: BG p<0,05 en 4, BP en 5, JB en 5, RESET en 1, CUSUM rechaza en 0 de 6; cambio de signo de phi entre mitades en 0.

Heterogeneidad de phi_i, spec B: media -0.061, mediana -0.039, DE 0.070, min -0.193, max 0.006; phi_i<0 en 5/6; semivida mediana 16.9 trimestres; BH q<0,10 en phi_i: 2/6 (t convencional, aproximado).
Diagnosticos spec B: BG p<0,05 en 2, BP en 4, JB en 2, RESET en 1, CUSUM rechaza en 0 de 6; cambio de signo de phi entre mitades en 0.

Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.
Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %).