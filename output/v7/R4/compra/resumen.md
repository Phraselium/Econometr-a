# Resumen R4a, compra (informativo, muestra ya vista en v1; capa C4; asociacion de largo plazo, sin lenguaje causal)

## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)

| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |
|---|---|---|---|---|---|---|---|
| H7-C1 | ln_ocupados (spec A) | -0.460 | -0.246 | -0.062 | [-0.460, -0.062] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C2 | ln_hip_importe (spec A) | 0.304 | -0.032 | -0.007 | [-0.032, 0.304] | 0.3564 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C3 | ln_pob_total (spec A) | -1.957 | -1.280 | 3.608 | [-1.957, 3.608] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C4 | tasa_paro_epa (spec B) | -0.015 | -0.018 | 0.006 | [-0.018, 0.006] | 0.8153 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |

## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman

| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |
|---|---|---|---|---|---|---|---|
| A | -0.168 | -6.56 | False | 0.001 | 0.521 | 0.707 | 0.300 |
| B | -0.088 | -6.24 | False | 0.841 | 0.301 | 0.048 | 0.025 |

Heterogeneidad de phi_i, spec A: media -0.166, mediana -0.179, DE 0.108, min -0.368, max -0.008; phi_i<0 en 17/17; semivida mediana 3.5 trimestres; BH q<0,10 en phi_i: 12/17 (t convencional, aproximado).
Diagnosticos spec A: BG p<0,05 en 4, BP en 5, JB en 3, RESET en 4, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 0.

Heterogeneidad de phi_i, spec B: media -0.086, mediana -0.072, DE 0.057, min -0.174, max 0.006; phi_i<0 en 16/17; semivida mediana 8.8 trimestres; BH q<0,10 en phi_i: 10/17 (t convencional, aproximado).
Diagnosticos spec B: BG p<0,05 en 5, BP en 6, JB en 4, RESET en 3, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 1.

## Orden de integracion por CCAA (ADF c + KPSS c; I(1) si ADF no rechaza en nivel, KPSS rechaza y ADF rechaza en diferencias)

- ln_ipv: {'ambiguo': 17} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)
- ln_hip_importe: {'ambiguo': 16, 'I(1)': 1} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)
- ln_ocupados: {'I(1)': 10, 'ambiguo': 7} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)
- ln_pob_total: {'ambiguo': 16, 'I(1)': 1} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)
- tasa_paro_epa: {'ambiguo': 13, 'I(1)': 4} (ver integracion.csv: ADF, KPSS, Zivot-Andrews)

Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.
Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %).