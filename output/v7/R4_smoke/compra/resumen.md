# Resumen R4a, compra (informativo, muestra ya vista en v1; capa C4; asociacion de largo plazo, sin lenguaje causal)

## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)

| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |
|---|---|---|---|---|---|---|---|
| H7-C1 | ln_ocupados (spec A) | -1.323 | 1.302 | -0.016 | [-1.323, 1.302] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C2 | ln_hip_importe (spec A) | -0.146 | -0.135 | 0.036 | [-0.146, 0.036] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C3 | ln_pob_total (spec A) | 0.578 | 2.056 | 1.807 | [0.578, 2.056] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C4 | tasa_paro_epa (spec B) | -0.011 | 0.077 | 0.009 | [-0.011, 0.077] | 0.7329 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |

## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman

| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |
|---|---|---|---|---|---|---|---|
| A | -0.126 | -2.04 | False | 0.000 | 0.510 | 0.333 | 0.600 |
| B | -0.080 | -3.02 | False | 0.000 | 0.039 | 0.059 | 0.350 |

Heterogeneidad de phi_i, spec A: media -0.123, mediana -0.099, DE 0.158, min -0.381, max 0.043; phi_i<0 en 5/6; semivida mediana 3.7 trimestres; BH q<0,10 en phi_i: 2/6 (t convencional, aproximado).
Diagnosticos spec A: BG p<0,05 en 1, BP en 1, JB en 0, RESET en 1, CUSUM rechaza en 0 de 6; cambio de signo de phi entre mitades en 2.

Heterogeneidad de phi_i, spec B: media -0.078, mediana -0.049, DE 0.066, min -0.197, max -0.026; phi_i<0 en 6/6; semivida mediana 14.9 trimestres; BH q<0,10 en phi_i: 2/6 (t convencional, aproximado).
Diagnosticos spec B: BG p<0,05 en 2, BP en 0, JB en 0, RESET en 1, CUSUM rechaza en 0 de 6; cambio de signo de phi entre mitades en 2.

Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.
Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %).