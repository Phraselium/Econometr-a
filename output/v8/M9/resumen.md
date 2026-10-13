# M9 - ML interpretable como contraste (C4)

Contraste, no causal: ningun resultado de SHAP, importancias ni DML se lee como efecto. Capa C4 (EXPLORATORIO).

## Fuera de muestra (5 bloques de 8 trimestres, embargo 4; DM-HLN h=4)

- alquiler/ccaa_panel: RMSE bases ar4 0.93, ar4_fc 0.93 (mas exigente: ar4); mejores ML: gam_ar_alfa100 1.06 (p DM vs exigente 0.10), gam_ar_alfa10 1.11 (p DM vs exigente 0.09), lgbm_ar_Bm 1.50 (p DM vs exigente 0.14). Predicen mejor: ninguno.
- alquiler/nacional: RMSE bases ar4 0.95, ecm_v1 1.62 (mas exigente: ar4); mejores ML: gam_ar_alfa100 1.73 (p DM vs exigente 0.00), gam_ar_alfa10 1.84 (p DM vs exigente 0.00), lgbm_ar_Am 2.46 (p DM vs exigente 0.13). Predicen mejor: ninguno.
- compra/ccaa_panel: RMSE bases ar4 2.47, ar4_fc 2.14 (mas exigente: ar4_fc); mejores ML: gam_ar_alfa100 2.46 (p DM vs exigente 0.02), gam_ar_alfa10 2.56 (p DM vs exigente 0.00), lgbm_ar_Bm 3.01 (p DM vs exigente 0.03). Predicen mejor: ninguno.
- compra/nacional: RMSE bases ar4 1.09, ecm_v1 2.76 (mas exigente: ar4); mejores ML: gam_ar_alfa100 2.24 (p DM vs exigente 0.00), gam_ar_alfa10 2.33 (p DM vs exigente 0.00), lgbm_ar_Am 2.62 (p DM vs exigente 0.00). Predicen mejor: ninguno.

## Atribucion SHAP (modelo solo familias, panel; contribucion media pp; ver atribucion.csv con bandas)

- alquiler P5: factor_europeo -1.76 [-3.64, +0.23]; demografia +0.24 [+0.18, +0.32]; demanda_externa -0.22 [-0.21, +0.01]; empleo_renta +0.07 [-0.34, +0.33]; credito_tipos +0.05 [-0.07, +0.08]; oferta -0.05 [-0.07, +0.01]
- compra P5: empleo_renta +7.96 [+3.26, +8.47]; demografia +2.30 [+1.55, +3.35]; factor_europeo +2.14 [-0.36, +7.19]; credito_tipos +1.58 [+0.60, +2.80]; oferta +0.83 [+0.49, +1.21]; demanda_externa +0.51 [+0.10, +0.71]

## DML manual (C4, sin identificacion)

- compra, tipo_hip_real: theta +0.045 (EE 0.126), p BH 0.80
- compra, epa_pob: theta -0.172 (EE 0.240), p BH 0.73
- alquiler, tipo_hip_real: theta +0.452 (EE 0.097), p BH 0.00
- alquiler, epa_pob: theta +0.072 (EE 0.125), p BH 0.79

## Estabilidad del ranking y sustituto

- compra/ccaa_panel: fidelidad R2 del sustituto 0.78; correlacion maxima entre variables 0.96
- compra/nacional: fidelidad R2 del sustituto 0.92; correlacion maxima entre variables 0.93
- alquiler/ccaa_panel: fidelidad R2 del sustituto 0.88; correlacion maxima entre variables 0.96
- alquiler/nacional: fidelidad R2 del sustituto 0.78; correlacion maxima entre variables 0.93
- alquiler/ccaa_panel: ranking completo reproducido en 3 % de replicas bootstrap y 25 % de pliegues
- alquiler/nacional: ranking completo reproducido en 17 % de replicas bootstrap y 25 % de pliegues
- compra/ccaa_panel: ranking completo reproducido en 10 % de replicas bootstrap y 25 % de pliegues
- compra/nacional: ranking completo reproducido en 10 % de replicas bootstrap y 25 % de pliegues

## Limites

- Predictores con retardo de 1 trimestre; panel 2009T2-2026T2 (P1 solo en el nacional, desde 2003T2). Variables comunes en el tiempo aportan pocas observaciones independientes.
- ECM v1 solo aproximado y solo nacional. Turismo solo en sensibilidad. Presupuesto de hiperparametros declarado y sin seleccion por error fuera de muestra.
