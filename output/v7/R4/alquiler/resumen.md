# Resumen R4a, alquiler (informativo, muestra ya vista en v1; capa C4; asociacion de largo plazo, sin lenguaje causal)

## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)

| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |
|---|---|---|---|---|---|---|---|
| H7-A1 | ln_ocupados (spec A) | 0.088 | 0.027 | 0.003 | [0.003, 0.088] | 0.5087 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A2 | ln_pob_total (spec A) | 0.894 | 0.844 | 0.177 | [0.177, 0.894] | 0.5086 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-A3 | tasa_paro_epa (spec B) | -0.004 | 0.004 | 0.000 | [-0.004, 0.004] | 0.5087 | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |

## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman

| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |
|---|---|---|---|---|---|---|---|
| A | -0.048 | -3.12 | False | 0.981 | 0.950 | 0.976 | 0.540 |
| B | -0.030 | -2.52 | False | 0.174 | 0.818 | 0.872 | 0.350 |

Heterogeneidad de phi_i, spec A: media -0.048, mediana -0.041, DE 0.064, min -0.147, max 0.053; phi_i<0 en 11/17; semivida mediana 6.6 trimestres. phi_i SIN INFERENCIA VALIDA (solo estimacion; sin IC, p ni BH; la comparacion valida de la media es el t de MG frente a -8,83).
Diagnosticos spec A: BG p<0,05 en 10, BP en 9, JB en 9, RESET en 2, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 5.

Heterogeneidad de phi_i, spec B: media -0.029, mediana -0.016, DE 0.048, min -0.134, max 0.031; phi_i<0 en 13/17; semivida mediana 24.8 trimestres. phi_i SIN INFERENCIA VALIDA (solo estimacion; sin IC, p ni BH; la comparacion valida de la media es el t de MG frente a -8,83).
Diagnosticos spec B: BG p<0,05 en 7, BP en 5, JB en 7, RESET en 0, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 8.

## Hausman
No rechaza en alquiler (potencia ~0,61): se reportan MG y PMG sin afirmar homogeneidad; la relacion de largo plazo no esta establecida.

## Cotas ARDL por region (diagnostico C4, no validado en R2, invalido si hay I(2))
- Spec A: 10/17 regiones rechazan la ausencia de cointegracion tras Holm (p simulado con cota I(1)); sin ajuste, 11/17 superan la cota superior. Discrepancia con Pedroni/Westerlund del panel: ver cointegracion.csv.
- Spec B: 15/17 regiones rechazan la ausencia de cointegracion tras Holm (p simulado con cota I(1)); sin ajuste, 15/17 superan la cota superior. Discrepancia con Pedroni/Westerlund del panel: ver cointegracion.csv.

## Sensibilidad del signo al orden de rezagos (signos_rezago.csv)
El signo de theta NO es estable al orden ARDL: signo estable entre SBC, (1,1) y (2,2) en 0/24 combinaciones spec-variable-estimador. Un PMG degenerado (EE enormes) es un fallo numerico, no un resultado.
- Bai-Perron spec A (relacion agregada, mmax = 5): m por BIC = 2, fechas ['2013Q2', '2020Q4']; en el limite de m: False.
- Bai-Perron spec B (relacion agregada, mmax = 5): m por BIC = 4, fechas ['2012Q1', '2016Q3', '2020Q1', '2023Q4']; en el limite de m: False.

## Orden de integracion por CCAA (ADF c + KPSS c; I(1) si ADF no rechaza en nivel, KPSS rechaza y ADF rechaza en diferencias)

- ln_ipc_alquiler: {'ambiguo': 15, 'I(1)': 2}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 9/17 CCAA (ver integracion.csv)
- ln_ocupados: {'I(1)': 10, 'ambiguo': 7}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 0/17 CCAA (ver integracion.csv)
- ln_pob_total: {'ambiguo': 16, 'I(1)': 1}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 15/17 CCAA (ver integracion.csv)
- tasa_paro_epa: {'ambiguo': 13, 'I(1)': 4}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 7/17 CCAA (ver integracion.csv)
Si I(2) no se descarta para y, ARDL/PMG y las cotas PSS no son validas con ese regresando: se anade la sensibilidad con la diferencia de ln y (specs A_g y B_g en largo_plazo.csv); no es confirmatoria.

Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.
Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %).