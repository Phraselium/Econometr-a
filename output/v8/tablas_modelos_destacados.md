# Tablas de modelos destacados V8 (F6)

Generado por `src/v8/f6_tablas.py` solo a partir de salidas versionadas (output/v8/M0-M9 y F5). No se estima nada nuevo. Capa: C4 (asociación) para todos los modelos de coeficientes; C3s solo en H8-1…H8-4 (condicionada a las restricciones de signo). Sin lenguaje causal fuera de esas capas.

## 1. Criterio y resultado

Criterio de §9 del pre-registro:

- **(a)** modelos que cumplen la regla de §8 (efecto por periodo, `cumple_regla_m0`) Y la del multiverso (signo estable ≥ 80 % y significativo tras BH ≥ 50 % en las especificaciones de la variable; M7 orientado).
- **(b)** además, el mejor de cada familia por mercado y periodo según el error fuera de muestra en bloques con embargo, nunca por su p, marcado «NO CUMPLE LA REGLA» si es el caso.

**Resultado (a): 0 modelos cumplen ambas reglas.** Pocos (es lo esperable): la regla de §8 la cumplen 2 variables de las 30 evaluables y ninguna cumple el multiverso orientado; las 18 variables que cumplen el multiverso no cumplen o no pueden evaluar §8. Se listan como parciales, sin ser destacados:

| regla | mercado | periodo | variable | cumple_regla_m0 | cumple_multiverso | pct_mismo_signo | pct_sig_bh |
|---|---|---|---|---|---|---|---|
| solo §8 | compra | P2 | pib_vol | si | no | 0.750 | 0.307 |
| solo §8 | compra | P4 | terminadas | si | no | 0.617 | 0.117 |
| solo multiverso | alquiler | P2 | hogares_epa | no_evaluable | sí | 1.000 | 0.750 |
| solo multiverso | alquiler | P2 | pob_extranj_ine | no_evaluable | sí | 1.000 | 0.771 |
| solo multiverso | alquiler | P2 | pob_total | no_evaluable | sí | 1.000 | 0.823 |
| solo multiverso | alquiler | P4 | tipo_hip_real | no_evaluable | sí | 0.833 | 0.542 |
| solo multiverso | alquiler | P4 | pob_extranj_ine | no_evaluable | sí | 0.800 | 0.525 |
| solo multiverso | alquiler | completo | credito_stock_real | no_evaluable | sí | 0.938 | 0.526 |
| solo multiverso | alquiler | completo | tipo_hip_real | no_evaluable | sí | 1.000 | 0.729 |
| solo multiverso | alquiler | completo | pob_extranj_ine | no_evaluable | sí | 0.990 | 0.625 |
| solo multiverso | alquiler | completo | pob_total | no_evaluable | sí | 1.000 | 0.693 |
| solo multiverso | compra | P1 | tipo_hip_real | no_evaluable | sí | 0.958 | 0.656 |
| solo multiverso | compra | P5 | credito_stock_real | no_evaluable | sí | 0.927 | 0.641 |
| solo multiverso | compra | P5 | tipo_hip_real | no_evaluable | sí | 0.875 | 0.500 |
| solo multiverso | compra | P5 | bis_hpi_xm_real | no_evaluable | sí | 0.948 | 0.589 |
| solo multiverso | compra | completo | credito_nuevo_real | no_evaluable | sí | 0.870 | 0.549 |
| solo multiverso | compra | completo | ocupados | no_evaluable | sí | 0.974 | 0.513 |
| solo multiverso | compra | completo | bis_hpi_xm_real | no_evaluable | sí | 0.990 | 0.643 |
| solo multiverso | compra | completo | terminadas | no_evaluable | sí | 0.953 | 0.526 |
| solo multiverso | compra | completo | visados | no_evaluable | sí | 0.979 | 0.747 |

**Resultado (b): 18 modelos destacados** (todos «NO CUMPLE LA REGLA» salvo indicación). Ámbito de la elección: el error fuera de muestra solo existe, por módulo, a nivel de mercado (M0, M4) o de mercado y muestra completa (M6); no hay OOS por periodo para esos modelos, de modo que la ecuación por periodo de M0 se destaca como bloque. Familias sin error fuera de muestra y por tanto no elegibles: M1 (factor común), M3 (regímenes), M5 (LP-IV), M8 (regional), M9-DML (el OOS de M9 es de los modelos predictivos LightGBM/GAM, que no tienen coeficientes) y M0 ampliada. Comparación con AR(4): 3 de 18 tienen RMSE menor o igual que AR(4) en su módulo (razón RMSE en la fila «fuera de muestra» de cada tabla; sin ajuste de multiplicidad aquí: los p DM-HLN ajustados están en la hoja Fuera_muestra).

## 2. Modelos destacados por mercado y periodo

### alquiler · P1

**M0_alquiler_base_P1** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | -2.958** (1.157) | HAC-NW(4), t(14) | 0.0228 | 0.0483 (BH) | [-5.439; -0.478] | -0.633 | — | no_evaluable | 96; 0.60; 0.04; no |
| d4_pib_vol | -0.961*** (0.142) | HAC-NW(4), t(14) | 9.0e-06 | 7.0e-05 (BH) | [-1.265; -0.656] | -0.716 | — | no_evaluable | 96; 0.50; 0.05; no |
| tipo_hip_real | 0.625*** (0.070) | HAC-NW(4), t(14) | 3.9e-07 | 3.9e-06 (BH) | [0.474; 0.775] | 1.128 | — | no_evaluable | 96; 0.60; 0.26; no |
| d4_credito_vivienda_real | 0.065*** (0.018) | HAC-NW(4), t(14) | 0.0028 | 0.0081 (BH) | [0.027; 0.104] | 0.628 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | -0.037 (0.020) | HAC-NW(4), t(14) | 0.0844 | 0.1441 (BH) | [-0.079; 0.006] | -0.421 | — | no_evaluable | 96; 0.71; 0.08; no |

| concepto | valor |
|---|---|
| N | 20 |
| periodo / ámbito | P1 / nacional |
| R² / R² ajustado | 0.844 / 0.788 |
| AIC / BIC | 8.62 / 14.60 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.815 vs 0.800 (ratio 2.27; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.815 vs AR(4) 0.800 (peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_ipc_alquiler_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### alquiler · P2

**M0_alquiler_base_P2** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | -1.453 (0.695) | HAC-NW(4), t(16) | 0.0530 | 0.1030 (BH) | [-2.926; 0.021] | -0.383 | — | no_evaluable | 96; 1.00; 0.82; sí |
| d4_pib_vol | -0.413*** (0.069) | HAC-NW(4), t(16) | 2.1e-05 | 0.0001 (BH) | [-0.560; -0.266] | -0.313 | — | no_evaluable | 96; 0.56; 0.19; no |
| tipo_hip_real | 0.522*** (0.087) | HAC-NW(4), t(16) | 1.7e-05 | 0.0001 (BH) | [0.338; 0.705] | 0.349 | — | no_evaluable | 96; 0.75; 0.31; no |
| d4_credito_vivienda_real | 0.678*** (0.132) | HAC-NW(4), t(16) | 0.0001 | 0.0005 (BH) | [0.397; 0.959] | 0.958 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | -0.004 (0.007) | HAC-NW(4), t(16) | 0.5948 | 0.6609 (BH) | [-0.019; 0.011] | -0.032 | — | no_evaluable | 96; 0.58; 0.12; no |

| concepto | valor |
|---|---|
| N | 22 |
| periodo / ámbito | P2 / nacional |
| R² / R² ajustado | 0.975 / 0.968 |
| AIC / BIC | 25.03 / 31.58 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.815 vs 0.800 (ratio 2.27; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.815 vs AR(4) 0.800 (peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_ipc_alquiler_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### alquiler · P3

**M0_alquiler_base_P3** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | 1.834*** (0.193) | HAC-NW(4), t(18) | 1.9e-08 | 2.9e-07 (BH) | [1.429; 2.240] | 0.758 | — | no_evaluable | 96; 0.90; 0.21; no |
| d4_pib_vol | 0.117 (0.060) | HAC-NW(4), t(18) | 0.0667 | 0.1229 (BH) | [-0.009; 0.242] | 0.124 | — | no_evaluable | 96; 0.54; 0.02; no |
| tipo_hip_real | 0.690*** (0.042) | HAC-NW(4), t(18) | 2.8e-12 | 9.9e-11 (BH) | [0.602; 0.779] | 1.030 | — | no_evaluable | 96; 0.56; 0.12; no |
| d4_credito_vivienda_real | 0.261*** (0.057) | HAC-NW(4), t(18) | 0.0002 | 0.0009 (BH) | [0.142; 0.380] | 0.322 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | 0.003 (0.003) | HAC-NW(4), t(18) | 0.3276 | 0.4327 (BH) | [-0.003; 0.008] | 0.074 | — | no_evaluable | 96; 0.52; 0.08; no |

| concepto | valor |
|---|---|
| N | 24 |
| periodo / ámbito | P3 / nacional |
| R² / R² ajustado | 0.967 / 0.958 |
| AIC / BIC | -9.09 / -2.02 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.815 vs 0.800 (ratio 2.27; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.815 vs AR(4) 0.800 (peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_ipc_alquiler_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### alquiler · P4

**M0_alquiler_base_P4** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | 0.105 (0.655) | HAC-NW(4), t(3) | 0.8829 | 0.8957 (BH) | [-1.979; 2.189] | 0.007 | — | no_evaluable | 120; 0.63; 0.46; no |
| d4_pib_vol | 0.016** (0.002) | HAC-NW(4), t(3) | 0.0049 | 0.0132 (BH) | [0.009; 0.023] | 0.055 | — | no_evaluable | 120; 0.75; 0.47; no |
| tipo_hip_real | 1.293** (0.185) | HAC-NW(4), t(3) | 0.0061 | 0.0157 (BH) | [0.703; 1.884] | 1.297 | — | no_evaluable | 120; 0.83; 0.54; sí |
| d4_credito_vivienda_real | -0.403 (0.276) | HAC-NW(4), t(3) | 0.2406 | 0.3239 (BH) | [-1.281; 0.476] | -0.267 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | -0.003 (0.001) | HAC-NW(4), t(3) | 0.0778 | 0.1361 (BH) | [-0.007; 6.2e-04] | -0.014 | — | no_evaluable | 120; 0.63; 0.09; no |

| concepto | valor |
|---|---|
| N | 9 |
| periodo / ámbito | P4 / nacional |
| R² / R² ajustado | 1.000 / 1.000 |
| AIC / BIC | -25.09 / -23.91 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.815 vs 0.800 (ratio 2.27; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.815 vs AR(4) 0.800 (peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_ipc_alquiler_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### alquiler · P5

**M0_alquiler_base_P5** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | 1.178 (0.590) | HAC-NW(4), t(10) | 0.0739 | 0.1326 (BH) | [-0.137; 2.493] | 0.052 | — | no_evaluable | 96; 0.58; 0.12; no |
| d4_pib_vol | 0.087 (0.057) | HAC-NW(4), t(10) | 0.1593 | 0.2424 (BH) | [-0.041; 0.215] | 0.045 | — | no_evaluable | 96; 0.69; 0.18; no |
| tipo_hip_real | 0.772*** (0.017) | HAC-NW(4), t(10) | 6.6e-13 | 4.6e-11 (BH) | [0.734; 0.810] | 0.810 | — | no_evaluable | 96; 0.85; 0.46; no |
| d4_credito_vivienda_real | 0.248*** (0.014) | HAC-NW(4), t(10) | 5.3e-09 | 1.2e-07 (BH) | [0.218; 0.278] | 0.376 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | 0.002 (0.003) | HAC-NW(4), t(10) | 0.5419 | 0.6322 (BH) | [-0.005; 0.008] | 0.007 | — | no_evaluable | 96; 0.50; 0.05; no |

| concepto | valor |
|---|---|
| N | 16 |
| periodo / ámbito | P5 / nacional |
| R² / R² ajustado | 0.998 / 0.997 |
| AIC / BIC | -19.52 / -14.89 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.815 vs 0.800 (ratio 2.27; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.815 vs AR(4) 0.800 (peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_ipc_alquiler_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### alquiler · completo

**M4_alquiler_A2_sin_rupturas_ardl** (ardl_bounds_uecm; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | 1.428 (0.981) | delta (OLS clasico) | 0.1453 | 0.2889 (BH) | [-0.494; 3.351] | 2.433 | 1.428 | no_evaluable | —; —; —; no_evaluable |
| tipo | 0.071 (0.040) | delta (OLS clasico) | 0.0771 | 0.1755 (BH) | [-0.008; 0.151] | 2.888 | — | no_evaluable | —; —; —; no_evaluable |
| hogares | -2.327 (1.462) | delta (OLS clasico) | 0.1113 | 0.2313 (BH) | [-5.192; 0.538] | -3.798 | -2.327 | no_evaluable | —; —; —; no_evaluable |
| ruptura:epa2021 | -0.102 (0.058) | delta (OLS clasico) | 0.0814 | 0.1828 (BH) | [-0.216; 0.013] | -0.855 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 95 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.711 / 0.681 |
| AIC / BIC | -690.24 / -664.70 |
| velocidad de ajuste / semivida (trim.) | -0.043 / 15.6 |
| diagnósticos (p): BG / BP / JB / RESET | 0.0002 / 0.5114 / 1.6e-09 / 0.0773 |
| CUSUM estable / VIF máx. | sí / 2.66 |
| cointegración (p) | 0.0010 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 0.705 vs 0.726 (ratio 0.97; M4:A2_sin_rupturas_SR) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion A2 de menor RMSE (SR); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 0.705 vs AR(4) 0.726 (no peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_ipc_alquiler_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M4_alquiler_A2_sin_rupturas_dols** (dols; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | -0.307** (0.117) | HAC-NW(4) | 0.0088 | 0.0281 (BH) | [-0.537; -0.077] | -0.523 | -0.307 | no_evaluable | —; —; —; no_evaluable |
| tipo | 0.003 (0.003) | HAC-NW(4) | 0.3154 | 0.5230 (BH) | [-0.003; 0.009] | 0.118 | — | no_evaluable | —; —; —; no_evaluable |
| hogares | 0.513** (0.204) | HAC-NW(4) | 0.0118 | 0.0370 (BH) | [0.114; 0.912] | 0.837 | 0.513 | no_evaluable | —; —; —; no_evaluable |
| ruptura:epa2021 | -0.103*** (0.018) | HAC-NW(4) | 5.8e-09 | 6.9e-08 (BH) | [-0.137; -0.068] | -0.863 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 95 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.802 / 0.770 |
| AIC / BIC | -427.62 / -391.86 |
| velocidad de ajuste / semivida (trim.) | -0.055 / 12.2 |
| diagnósticos (p): BG / BP / JB / RESET | 3.4e-27 / 0.0085 / 0.0225 / 0.3898 |
| CUSUM estable / VIF máx. | no / 2.66 |
| cointegración (p) | 0.6352 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 0.705 vs 0.726 (ratio 0.97; M4:A2_sin_rupturas_SR) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion A2 de menor RMSE (SR); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 0.705 vs AR(4) 0.726 (no peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_ipc_alquiler_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M4_alquiler_A2_sin_rupturas_fmols** (fmols; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | -0.148 (0.101) | FMOLS Omega_u.e (Bartlett) | 0.1413 | 0.2844 (BH) | [-0.346; 0.049] | -0.253 | -0.148 | no_evaluable | —; —; —; no_evaluable |
| tipo | 0.004 (0.003) | FMOLS Omega_u.e (Bartlett) | 0.1545 | 0.2982 (BH) | [-0.001; 0.009] | 0.158 | — | no_evaluable | —; —; —; no_evaluable |
| hogares | 0.079 (0.090) | FMOLS Omega_u.e (Bartlett) | 0.3823 | 0.5867 (BH) | [-0.098; 0.256] | 0.129 | 0.079 | no_evaluable | —; —; —; no_evaluable |
| ruptura:epa2021 | -0.073*** (0.018) | FMOLS Omega_u.e (Bartlett) | 5.7e-05 | 0.0003 (BH) | [-0.108; -0.037] | -0.611 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 94 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.703 / 0.690 |
| AIC / BIC | -668.64 / -655.93 |
| velocidad de ajuste / semivida (trim.) | -0.077 / 8.6 |
| diagnósticos (p): BG / BP / JB / RESET | 1.1e-32 / 0.0010 / 0.0034 / 2.9e-12 |
| CUSUM estable / VIF máx. | no / 2.66 |
| cointegración (p) | 0.6352 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 0.705 vs 0.726 (ratio 0.97; M4:A2_sin_rupturas_SR) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion A2 de menor RMSE (SR); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 0.705 vs AR(4) 0.726 (no peor que AR(4)) |
| medida de precio | IPC alquiler, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_ipc_alquiler_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M6_ols_alquiler_trimestral_completo** (ols_familias; módulo M6)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| const | -0.278 (0.162) | EWC | 0.1305 | 0.2400 (BH) | [-0.662; 0.106] | — | — | no_evaluable | —; —; —; no_evaluable |
| hogares_epa | -0.441 (0.497) | EWC | 0.4038 | 0.5378 (BH) | [-1.616; 0.733] | -0.097 | -0.441 | no_evaluable | 576; 0.98; 0.60; sí |
| pib_vol | 0.055 (0.041) | EWC | 0.2238 | 0.3573 (BH) | [-0.043; 0.153] | 0.152 | 0.055 | no_evaluable | 576; 0.67; 0.26; no |
| tipo_hip_real | 0.185** (0.042) | EWC | 0.0032 | 0.0260 (BH) | [0.085; 0.284] | 0.373 | — | no_evaluable | 576; 0.58; 0.31; no |
| terminadas | -0.010 (0.005) | EWC | 0.1033 | 0.1967 (BH) | [-0.023; 0.003] | -0.181 | -0.010 | no_evaluable | 576; 0.63; 0.18; no |
| tx_extranj | -0.018 (0.008) | EWC | 0.0477 | 0.1103 (BH) | [-0.036; -2.4e-04] | -0.386 | -0.018 | no_evaluable | 384; 0.57; 0.24; no |
| bis_hpi_xm_real | 0.130 (0.197) | EWC | 0.5302 | 0.6539 (BH) | [-0.335; 0.595] | 0.134 | 0.130 | no_evaluable | 576; 0.51; 0.04; no |
| covid | -0.049 (0.256) | EWC | 0.8548 | 0.9004 (BH) | [-0.654; 0.557] | -0.009 | — | no_evaluable | —; —; —; no_evaluable |
| epa2021_q | -0.860 (0.699) | EWC | 0.2581 | 0.3847 (BH) | [-2.512; 0.792] | -0.090 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 76 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.438 / 0.371 |
| AIC / BIC | 202.42 / 223.39 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | 0.0052 / 0.5476 / 0.0004 / 0.6932 |
| CUSUM estable / VIF máx. | sí / 1.96 |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 3.839 vs 0.804 (ratio 4.77; M6:ols_factores) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_familias: ols_factores trimestral, periodo completo; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 3.839 vs AR(4) 0.804 (peor que AR(4)) |
| medida de precio | ipc_alquiler |
| transformación | trimestral |
| dependiente | d_ln_ipc_alquiler_real |
| script | src/v8/m6_colinealidad.py |
| fuente | output/v8/M6/coeficientes.csv |

### compra · P1

**M0_compra_base_P1** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | -3.670** (1.511) | HAC-NW(4), t(32) | 0.0210 | 0.0459 (BH) | [-6.748; -0.591] | -0.622 | — | no_evaluable | 96; 0.50; 0.14; no |
| d4_pib_vol | -3.520*** (0.888) | HAC-NW(4), t(32) | 0.0004 | 0.0015 (BH) | [-5.329; -1.710] | -0.689 | — | no_evaluable | 96; 0.88; 0.03; no |
| tipo_hip_real | -2.204*** (0.436) | HAC-NW(4), t(32) | 1.7e-05 | 0.0001 (BH) | [-3.091; -1.317] | -0.734 | — | no_evaluable | 96; 0.96; 0.66; sí |
| d4_credito_vivienda_real | -0.087 (0.110) | HAC-NW(4), t(32) | 0.4381 | 0.5380 (BH) | [-0.312; 0.138] | -0.102 | — | no_evaluable | —; —; —; no_evaluable |
| d4_terminadas | -0.043 (0.047) | HAC-NW(4), t(32) | 0.3688 | 0.4780 (BH) | [-0.139; 0.053] | -0.119 | — | no_evaluable | 84; 0.52; 0.14; no |

| concepto | valor |
|---|---|
| N | 38 |
| periodo / ámbito | P1 / nacional |
| R² / R² ajustado | 0.696 / 0.649 |
| AIC / BIC | 173.70 / 183.53 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.802 vs 1.216 (ratio 1.48; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.802 vs AR(4) 1.216 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_p_tasado_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### compra · P2

**M0_compra_base_P2** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | -1.897*** (0.544) | HAC-NW(4), t(16) | 0.0030 | 0.0085 (BH) | [-3.050; -0.745] | -0.418 | — | no | 192; 0.73; 0.12; no |
| d4_pib_vol | 1.379*** (0.135) | HAC-NW(4), t(16) | 2.0e-08 | 2.9e-07 (BH) | [1.093; 1.665] | 0.875 | — | sí | 192; 0.75; 0.31; no |
| tipo_hip_real | 1.170*** (0.200) | HAC-NW(4), t(16) | 2.5e-05 | 0.0001 (BH) | [0.746; 1.593] | 0.654 | — | no | 192; 0.64; 0.27; no |
| d4_credito_vivienda_real | 0.528*** (0.149) | HAC-NW(4), t(16) | 0.0028 | 0.0081 (BH) | [0.211; 0.844] | 0.622 | — | no | —; —; —; no_evaluable |
| d4_terminadas | 0.004 (0.008) | HAC-NW(4), t(16) | 0.5859 | 0.6609 (BH) | [-0.012; 0.020] | 0.029 | — | no | 192; 0.59; 0.10; no |

| concepto | valor |
|---|---|
| N | 22 |
| periodo / ámbito | P2 / nacional |
| R² / R² ajustado | 0.937 / 0.918 |
| AIC / BIC | 53.43 / 59.97 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.802 vs 1.216 (ratio 1.48; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.802 vs AR(4) 1.216 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_p_tasado_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### compra · P3

**M0_compra_base_P3** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | 4.079*** (0.849) | HAC-NW(4), t(18) | 0.0001 | 0.0007 (BH) | [2.295; 5.863] | 0.791 | — | no | 192; 0.72; 0.14; no |
| d4_pib_vol | 1.454*** (0.194) | HAC-NW(4), t(18) | 6.0e-07 | 5.2e-06 (BH) | [1.047; 1.861] | 0.723 | — | no | 192; 0.95; 0.43; no |
| tipo_hip_real | 0.219 (0.170) | HAC-NW(4), t(18) | 0.2134 | 0.3048 (BH) | [-0.138; 0.576] | 0.154 | — | no | 192; 0.78; 0.19; no |
| d4_credito_vivienda_real | 0.282 (0.208) | HAC-NW(4), t(18) | 0.1917 | 0.2855 (BH) | [-0.155; 0.719] | 0.163 | — | no | —; —; —; no_evaluable |
| d4_terminadas | -0.014 (0.009) | HAC-NW(4), t(18) | 0.1299 | 0.2115 (BH) | [-0.032; 0.004] | -0.176 | — | no | 192; 0.57; 0.19; no |

| concepto | valor |
|---|---|
| N | 24 |
| periodo / ámbito | P3 / nacional |
| R² / R² ajustado | 0.890 / 0.860 |
| AIC / BIC | 55.98 / 63.05 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.802 vs 1.216 (ratio 1.48; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.802 vs AR(4) 1.216 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_p_tasado_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### compra · P4

**M0_compra_base_P4** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | 0.196 (3.094) | HAC-NW(4), t(3) | 0.9536 | 0.9536 (BH) | [-9.652; 10.043] | 0.055 | — | no | 240; 0.67; 0.24; no |
| d4_pib_vol | -0.147** (0.029) | HAC-NW(4), t(3) | 0.0146 | 0.0351 (BH) | [-0.239; -0.055] | -2.096 | — | no | 240; 0.53; 0.26; no |
| tipo_hip_real | -1.442 (0.883) | HAC-NW(4), t(3) | 0.2009 | 0.2930 (BH) | [-4.253; 1.368] | -6.042 | — | no | 240; 0.53; 0.23; no |
| d4_credito_vivienda_real | 1.786 (1.211) | HAC-NW(4), t(3) | 0.2367 | 0.3239 (BH) | [-2.067; 5.639] | 4.951 | — | no | —; —; —; no_evaluable |
| d4_terminadas | 0.065* (0.018) | HAC-NW(4), t(3) | 0.0387 | 0.0796 (BH) | [0.006; 0.124] | 1.302 | — | sí | 240; 0.62; 0.12; no |

| concepto | valor |
|---|---|
| N | 9 |
| periodo / ámbito | P4 / nacional |
| R² / R² ajustado | 0.893 / 0.714 |
| AIC / BIC | 14.15 / 15.34 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.802 vs 1.216 (ratio 1.48; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.802 vs AR(4) 1.216 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_p_tasado_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### compra · P5

**M0_compra_base_P5** (ols_tramos_hac; módulo M0)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| d4_pob_total | -10.182*** (2.025) | HAC-NW(4), t(10) | 0.0005 | 0.0019 (BH) | [-14.694; -5.671] | -0.206 | — | no | 192; 0.59; 0.20; no |
| d4_pib_vol | -1.155*** (0.269) | HAC-NW(4), t(10) | 0.0016 | 0.0050 (BH) | [-1.755; -0.556] | -0.272 | — | no | 192; 0.85; 0.29; no |
| tipo_hip_real | 0.196 (0.127) | HAC-NW(4), t(10) | 0.1517 | 0.2361 (BH) | [-0.086; 0.478] | 0.094 | — | no | 192; 0.88; 0.50; sí |
| d4_credito_vivienda_real | 1.047*** (0.080) | HAC-NW(4), t(10) | 1.3e-07 | 1.5e-06 (BH) | [0.868; 1.226] | 0.727 | — | no | —; —; —; no_evaluable |
| d4_terminadas | -0.006 (0.017) | HAC-NW(4), t(10) | 0.7327 | 0.7771 (BH) | [-0.044; 0.032] | -0.010 | — | no | 192; 0.52; 0.10; no |

| concepto | valor |
|---|---|
| N | 16 |
| periodo / ámbito | P5 / nacional |
| R² / R² ajustado | 0.983 / 0.975 |
| AIC / BIC | 40.20 / 44.83 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | — / — / — / — |
| CUSUM estable / VIF máx. | — / — |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.802 vs 1.216 (ratio 1.48; M0:AR1+X_por_periodo) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_tramos_hac: ecuacion AR1+X por periodo; unico candidato con OOS en la familia; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.802 vs AR(4) 1.216 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | d4_ln*100 |
| dependiente | d4_ln_p_tasado_real |
| script | src/v8/m0_periodos.py |
| fuente | output/v8/M0/coeficientes.csv |

### compra · completo

**M4_compra_C1_sin_rupturas_ardl** (ardl_bounds_uecm; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | -0.691 (1.234) | delta (OLS clasico) | 0.5757 | 0.7406 (BH) | [-3.109; 1.728] | -0.448 | -0.691 | no_evaluable | —; —; —; no_evaluable |
| tipo | 6.6e-04 (0.057) | delta (OLS clasico) | 0.9908 | 0.9919 (BH) | [-0.111; 0.112] | 0.007 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 113 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.316 / 0.277 |
| AIC / BIC | -582.91 / -563.82 |
| velocidad de ajuste / semivida (trim.) | -0.017 / 39.8 |
| diagnósticos (p): BG / BP / JB / RESET | 1.7e-18 / 0.0346 / 0.3208 / 0.2154 |
| CUSUM estable / VIF máx. | sí / 1.27 |
| cointegración (p) | 0.1000 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.407 vs 1.283 (ratio 1.10; M4:C1_sin_rupturas_ECM) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion C1 de menor RMSE (ECM); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.407 vs AR(4) 1.283 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_p_tasado_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M4_compra_C1_sin_rupturas_dols** (dols; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | 0.688* (0.301) | HAC-NW(4) | 0.0223 | 0.0640 (BH) | [0.098; 1.278] | 0.446 | 0.688 | no_evaluable | —; —; —; no_evaluable |
| tipo | 0.006 (0.020) | HAC-NW(4) | 0.7594 | 0.8553 (BH) | [-0.032; 0.044] | 0.064 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 113 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.200 / 0.139 |
| AIC / BIC | -65.14 / -40.59 |
| velocidad de ajuste / semivida (trim.) | -0.016 / 42.0 |
| diagnósticos (p): BG / BP / JB / RESET | 1.1e-72 / 0.8097 / 0.0003 / 3.4e-08 |
| CUSUM estable / VIF máx. | no / 1.27 |
| cointegración (p) | 0.6252 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.407 vs 1.283 (ratio 1.10; M4:C1_sin_rupturas_ECM) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion C1 de menor RMSE (ECM); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.407 vs AR(4) 1.283 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_p_tasado_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M4_compra_C1_sin_rupturas_fmols** (fmols; módulo M4)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| renta | 0.618 (0.326) | FMOLS Omega_u.e (Bartlett) | 0.0577 | 0.1378 (BH) | [-0.020; 1.257] | 0.401 | 0.618 | no_evaluable | —; —; —; no_evaluable |
| tipo | 0.004 (0.020) | FMOLS Omega_u.e (Bartlett) | 0.8376 | 0.9048 (BH) | [-0.034; 0.042] | 0.043 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 112 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.157 / 0.142 |
| AIC / BIC | -392.50 / -384.35 |
| velocidad de ajuste / semivida (trim.) | -0.017 / 41.1 |
| diagnósticos (p): BG / BP / JB / RESET | 6.7e-81 / 0.3744 / 0.0005 / 0.0193 |
| CUSUM estable / VIF máx. | no / 1.27 |
| cointegración (p) | 0.6252 |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 1.407 vs 1.283 (ratio 1.10; M4:C1_sin_rupturas_ECM) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia dols/fmols/ardl: especificacion C1 de menor RMSE (ECM); el OOS se hace con beta OLS estatico y es comun a los tres estimadores; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 1.407 vs AR(4) 1.283 (peor que AR(4)) |
| medida de precio | valor tasado MIVAU, real (IPC general) |
| transformación | ln niveles; tipo en pp |
| dependiente | ln_p_tasado_real |
| script | src/v8/m4_largo_plazo.py |
| fuente | output/v8/M4/coeficientes.csv |

**M6_ols_compra_trimestral_completo** (ols_familias; módulo M6)

| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | multiverso (n; % signo; % sig. BH; cumple) |
|---|---|---|---|---|---|---|---|---|---|
| const | -0.703 (0.472) | EWC | 0.1747 | 0.2936 (BH) | [-1.792; 0.386] | — | — | no_evaluable | —; —; —; no_evaluable |
| hogares_epa | 1.980 (1.099) | EWC | 0.1093 | 0.2056 (BH) | [-0.554; 4.513] | 0.278 | 1.980 | no_evaluable | 1152; 0.72; 0.21; no |
| pib_vol | 0.080* (0.030) | EWC | 0.0281 | 0.0763 (BH) | [0.011; 0.149] | 0.107 | 0.080 | no_evaluable | 1152; 0.89; 0.22; no |
| tipo_hip_real | -0.033 (0.094) | EWC | 0.7356 | 0.7960 (BH) | [-0.248; 0.183] | -0.033 | — | no_evaluable | 1152; 0.76; 0.36; no |
| terminadas | 0.005 (0.009) | EWC | 0.5914 | 0.6974 (BH) | [-0.015; 0.025] | 0.042 | 0.005 | no_evaluable | 1152; 0.77; 0.43; no |
| bis_hpi_xm_real | 1.085* (0.352) | EWC | 0.0151 | 0.0502 (BH) | [0.273; 1.897] | 0.598 | 1.085 | no_evaluable | 960; 0.71; 0.35; no |
| covid | -1.375** (0.377) | EWC | 0.0065 | 0.0354 (BH) | [-2.244; -0.507] | -0.120 | — | no_evaluable | —; —; —; no_evaluable |
| epa2021_q | 2.248 (1.555) | EWC | 0.1863 | 0.3087 (BH) | [-1.338; 5.834] | 0.114 | — | no_evaluable | —; —; —; no_evaluable |

| concepto | valor |
|---|---|
| N | 96 |
| periodo / ámbito | completo / nacional |
| R² / R² ajustado | 0.466 / 0.423 |
| AIC / BIC | 361.17 / 381.68 |
| velocidad de ajuste / semivida (trim.) | — / — |
| diagnósticos (p): BG / BP / JB / RESET | 1.2e-09 / 0.0271 / 0.0064 / 0.1723 |
| CUSUM estable / VIF máx. | no / 1.11 |
| cointegración (p) | — |
| IV: F de primera etapa / intervalo AR95 | — / [—; —] |
| capa | C4 |
| fuera de muestra: RMSE (modelo) vs AR(4) | 2.830 vs 1.038 (ratio 2.73; M6:ols_factores) |
| cumple regla M0 (§8) / cumple multiverso | por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: no |
| motivo destacado | (b) mejor de la familia ols_familias: ols_factores trimestral, periodo completo; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE 2.830 vs AR(4) 1.038 (peor que AR(4)) |
| medida de precio | tasado |
| transformación | trimestral |
| dependiente | d_ln_tasado_real |
| script | src/v8/m6_colinealidad.py |
| fuente | output/v8/M6/coeficientes.csv |

Notas. Estrellas basadas en el p AJUSTADO (BH o Holm, segun la columna «método»): * < 0,10; ** < 0,05; *** < 0,01; sin estrella si no se alcanza o no hay p ajustado. El tipo de error estandar (EE) se indica en cada fila (HAC-NW, EWC, delta, etc.). β std. = coeficiente estandarizado; elasticidad solo cuando el modulo la define. La capa de todos los modelos de esta tabla es C4 (asociacion): sin lenguaje causal. Los modelos destacados por el criterio (b) se eligen por su error fuera de muestra, nunca por su p, y se marcan «NO CUMPLE LA REGLA» si no cumplen la regla de §8 y la del multiverso. Un RMSE mayor que el de AR(4) indica que el modelo no predice mejor que esa linea base. Valores «—» = no aplica.

## 3. Hipótesis H8-1…H8-9 (§7)

| id | hipotesis | estimacion | p | p_holm | capa | decision |
|---|---|---|---|---|---|---|
| H8-1 | En P5, la contribucion del shock demografico a la subida del alquiler real es positiva | contribucion acumulada 0.07 pp (mediana 0.04; banda 68 % [-1.92; 2.13]); P(signo esperado) = 0.506 | 0.4937 | 0.9875 | C3s | no respaldada tras Holm (C3s: condicionada a las restricciones de signo) |
| H8-2 | En P5, la contribucion de credito y tipos al precio real de compra es negativa | contribucion acumulada -0.47 pp (mediana 3.37; banda 68 % [-2.82; 12.77]); P(signo esperado) = 0.293 | 0.7066 | 0.9875 | C3s | no respaldada tras Holm (C3s: condicionada a las restricciones de signo) |
| H8-3 | En P3, la contribucion de actividad y renta al precio real de compra es positiva | contribucion acumulada 7.72 pp (mediana 5.22; banda 68 % [-3.47; 18.23]); P(signo esperado) = 0.721 | 0.2793 | 0.8378 | C3s | no respaldada tras Holm (C3s: condicionada a las restricciones de signo) |
| H8-4 | En P2, la contribucion conjunta de credito y tipos y de actividad y renta al precio real de compra es negativa | contribucion acumulada -19.23 pp (mediana -16.71; banda 68 % [-34.59; -4.15]); P(signo esperado) = 0.914 | 0.0857 | 0.3426 | C3s | no respaldada tras Holm (C3s: condicionada a las restricciones de signo) |
| H8-5 | Un shock monetario contractivo del BCE reduce el precio real de compra a h = 4-8 | beta descriptivo (cociente) -8.78 (no es evidencia); F efectivo 1.83; IC AR95 [-inf; inf]; signo forma reducida 1 (esperado -1) | 0.7244 | 1.0000 | C4 | no respaldada tras Holm; no respaldada tras Holm (instrumento no supera C3) |
| H8-6 | Un shock monetario contractivo del BCE reduce el alquiler real a h = 4-8 | beta descriptivo (cociente) -2.91 (no es evidencia); F efectivo 0.77; IC AR95 [-inf; inf]; signo forma reducida 1 (esperado -1) | 0.6349 | 1.0000 | C4 | no respaldada tras Holm; no respaldada tras Holm (instrumento no supera C3) |
| H8-7 | El empuje migratorio aumenta el alquiler real | beta descriptivo (cociente) -0.51 (no es evidencia); F efectivo 0.05; IC AR95 [-inf; inf]; signo forma reducida -1 (esperado 1) | 0.5364 | 1.0000 | C4 | no respaldada tras Holm; no respaldada tras Holm (instrumento no supera C3) |
| H8-8 | El componente comun de las 17 CCAA explica mas del 50 % de la varianza del crecimiento interanual del precio real de compra en cada periodo | {"P1": 0.6474, "P2": 0.4527, "P3": 0.5958, "P4": 0.455, "P5": 0.9279} | 0.6690 | 0.6690 | C4 | no respaldada tras Holm (C4: asociacion, sin lectura causal) |
| H8-9 | El factor comun espanol covaria positivamente con el crecimiento del HPI de la zona euro | 0.5976 | 0.0100 | 0.0200 | C4 | respaldada tras Holm (C4: asociacion, sin lectura causal) |

p: unilateral (H8-1…H8-4, posterior), Anderson-Rubin con signo a priori (H8-5…H8-7) y bootstrap (H8-8, H8-9). Holm dentro de cada familia ({H8-1…H8-4}, {H8-5…H8-7}, {H8-8, H8-9}). Ninguna hipótesis de SVAR ni de instrumentos se respalda; H8-9 (C4) es una asociación sin lectura causal.

## 4. Votos de la regla de §9 (F5)

| mercado | periodo | voto_svar_hd | voto_dominancia | voto_lpiv | voto_contabilidad | factor_evaluado | n_votos | cond1 | cond2 | cond3 | resultado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| compra | P1 | empleo_renta | abstiene | abstiene | abstiene | empleo_renta | 1 | no | sí | sí | no designado |
| compra | P2 | empleo_renta | factor_europeo | abstiene | abstiene | empleo_renta | 1 | no | no | no | no designado |
| compra | P3 | empleo_renta | empleo_renta | abstiene | demografia | empleo_renta | 2 | no | sí | no | no designado |
| compra | P4 | empleo_renta | credito_tipos | credito_tipos | abstiene | credito_tipos | 2 | no | no | no | no designado |
| compra | P5 | credito_tipos | credito_tipos | abstiene | demografia | credito_tipos | 2 | no | no | no | no designado |
| alquiler | P1 | abstiene | factor_europeo | abstiene | abstiene | factor_europeo | 1 | no | no | no | no designado |
| alquiler | P2 | empleo_renta | empleo_renta | abstiene | abstiene | empleo_renta | 2 | no | no | no | no designado |
| alquiler | P3 | demografia | demanda_externa | abstiene | abstiene | demografia | 1 | no | no | no | no designado |
| alquiler | P4 | demanda_vivienda | credito_tipos | abstiene | abstiene | demanda_vivienda | 1 | no | no | no | no designado |
| alquiler | P5 | credito_tipos | credito_tipos | abstiene | abstiene | credito_tipos | 2 | no | no | no | no designado |

Celdas designadas: 0 de 10. svar_hd es C3s (condicionada a los supuestos de signo); dominancia, LP-IV y contabilidad son C4.

## 5. Tabla común fuera de muestra (F5; RMSE en pp de crecimiento trimestral real)

| mercado | modelo | rmse_pp | evaluable | p_holm_vs_ar4 | p_holm_vs_exigente | mejor_que_exigente |
|---|---|---|---|---|---|---|
| compra | ar4 | 1.1757 | si | — | — | no |
| compra | ecm_v1 | 2.6170 | si | 0.0123 | 0.0123 | no |
| compra | ar_fc | 1.2735 | si | 0.1315 | 0.1315 | no |
| compra | bvar_m2 | 1.3736 | si | 0.1315 | 0.1315 | no |
| alquiler | ar4 | 0.8034 | si | — | — | no |
| alquiler | ecm_v1 | 1.6916 | si | 0.0005 | 0.0005 | no |
| alquiler | ar_fc | 0.8318 | si | 0.5955 | 0.5955 | no |
| alquiler | bvar_m2 | 0.9759 | si | 0.1266 | 0.1266 | no |

Prueba 2016T2-2026T1, 5 bloques con embargo de 4 trimestres; DM con corrección HLN y Holm. Ningún modelo supera a la base más exigente.
