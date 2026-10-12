# Resumen R4a, compra (informativo, muestra ya vista en v1; capa C4; asociacion de largo plazo, sin lenguaje causal)

## Hipotesis de largo plazo (triangulacion V12: p de Holm de MG_dm < 0,05 y mismo signo en PMG_dm y CS-DL)

| id | variable | MG_dm | PMG_dm | CS-DL | rango | p Holm (MG_dm) | veredicto |
|---|---|---|---|---|---|---|---|
| H7-C1 | ln_ocupados (spec A) | -0.460 | -0.246 | -0.062 | [-0.460, -0.062] | 1.0000 | NO CONFIRMADA (p de Holm de MG_dm >= 0,05) |
| H7-C2 | ln_hip_importe (spec A) | 0.304 | -0.032 | -0.007 | [-0.032, 0.304] | 0.3564 | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |
| H7-C3 | ln_pob_total (spec A) | -1.957 | -1.280 | 3.608 | [-1.957, 3.608] | 1.0000 | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |
| H7-C4 | tasa_paro_epa (spec B) | -0.015 | -0.018 | 0.006 | [-0.018, 0.006] | 0.8153 | NO CONFIRMADA; signos discrepantes entre estimadores (p de Holm de MG_dm >= 0,05) |

## Velocidad de ajuste (H7-E2: t de MG frente a -8,83) y Hausman

| spec | phi_MG | t_MG | rechaza | Hausman p | Pedroni panel p | Pedroni group p | WL Gt p |
|---|---|---|---|---|---|---|---|
| A | -0.168 | -6.56 | False | 0.001 | 0.521 | 0.707 | 0.300 |
| B | -0.088 | -6.24 | False | 0.841 | 0.301 | 0.048 | 0.025 |

Heterogeneidad de phi_i, spec A: media -0.166, mediana -0.179, DE 0.108, min -0.368, max -0.008; phi_i<0 en 17/17; semivida mediana 3.5 trimestres. phi_i SIN INFERENCIA VALIDA (solo estimacion; sin IC, p ni BH; la comparacion valida de la media es el t de MG frente a -8,83).
Diagnosticos spec A: BG p<0,05 en 4, BP en 5, JB en 3, RESET en 4, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 0.

Heterogeneidad de phi_i, spec B: media -0.086, mediana -0.072, DE 0.057, min -0.174, max 0.006; phi_i<0 en 16/17; semivida mediana 8.8 trimestres. phi_i SIN INFERENCIA VALIDA (solo estimacion; sin IC, p ni BH; la comparacion valida de la media es el t de MG frente a -8,83).
Diagnosticos spec B: BG p<0,05 en 5, BP en 6, JB en 4, RESET en 3, CUSUM rechaza en 0 de 17; cambio de signo de phi entre mitades en 1.

## Hausman
El Hausman de compra A rechaza (p = 0,001), pero NO indica heterogeneidad del largo plazo: sin cointegracion rechaza ~24 % de las veces (validacion R2, escenarios C y D), Pedroni no rechaza en A y la relacion de largo plazo no esta establecida. En alquiler no rechaza y no se afirma homogeneidad.

## Cotas ARDL por region (diagnostico C4, no validado en R2, invalido si hay I(2))
- Spec A: 16/17 regiones rechazan la ausencia de cointegracion tras Holm (p simulado con cota I(1)); sin ajuste, 16/17 superan la cota superior. Discrepancia con Pedroni/Westerlund del panel: ver cointegracion.csv.
- Spec B: 16/17 regiones rechazan la ausencia de cointegracion tras Holm (p simulado con cota I(1)); sin ajuste, 16/17 superan la cota superior. Discrepancia con Pedroni/Westerlund del panel: ver cointegracion.csv.

## Sensibilidad del signo al orden de rezagos (signos_rezago.csv)
El signo de theta NO es estable al orden ARDL: signo estable entre SBC, (1,1) y (2,2) en 8/40 combinaciones spec-variable-estimador. Un PMG degenerado (EE enormes) es un fallo numerico, no un resultado.
- Bai-Perron spec A (relacion agregada, mmax = 5): m por BIC = 2, fechas ['2011Q1', '2013Q4']; en el limite de m: False.
- Bai-Perron spec B (relacion agregada, mmax = 5): m por BIC = 4, fechas ['2010Q4', '2013Q4', '2018Q4', '2023Q3']; en el limite de m: False.

## Orden de integracion por CCAA (ADF c + KPSS c; I(1) si ADF no rechaza en nivel, KPSS rechaza y ADF rechaza en diferencias)

- ln_ipv: {'ambiguo': 17}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 8/17 CCAA (ver integracion.csv)
- ln_hip_importe: {'ambiguo': 16, 'I(1)': 1}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 1/17 CCAA (ver integracion.csv)
- ln_ocupados: {'I(1)': 10, 'ambiguo': 7}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 0/17 CCAA (ver integracion.csv)
- ln_pob_total: {'ambiguo': 16, 'I(1)': 1}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 15/17 CCAA (ver integracion.csv)
- tasa_paro_epa: {'ambiguo': 13, 'I(1)': 4}; I(2) no descartado (ADF en diferencias con constante y tendencia, AIC y BIC) en 7/17 CCAA (ver integracion.csv)
Si I(2) no se descarta para y, ARDL/PMG y las cotas PSS no son validas con ese regresando: se anade la sensibilidad con la diferencia de ln y (specs A_g y B_g en largo_plazo.csv); no es confirmatoria.

Ver largo_plazo.csv (todos los estimadores y rezagos), cointegracion.csv (Westerlund tipo, Pedroni, bounds por region), integracion.csv, corto_plazo_region.csv, diagnosticos_region.csv, dfe_inferencia.csv, bai_perron.csv, magnitudes.csv.
Aviso de potencia: el tipo Westerlund tiene potencia 0,06-0,29 con ajuste lento; un no rechazo no prueba ausencia de cointegracion. PMG: IC aproximados. Con factor I(1) de cargas heterogeneas ningun estimador es apto (sesgo MG_dm ~20 %).