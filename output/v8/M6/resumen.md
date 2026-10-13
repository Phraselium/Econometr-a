# M6 - colinealidad y peso relativo (capa C4: asociacion)

Ecuacion del crecimiento nacional (log x 100) con una variable por familia; precio real de compra (valor tasado) y alquiler real (IPC alquiler). La dominancia (LMG/Shapley) reparte el R2 y NO es una atribucion causal.

## Mayor cuota de R2 por mercado y periodo (interanual, bandas b90 de la contribucion en pp)

| mercado | periodo | factor | cuota LMG x R2 % | b90 contribucion pp | segundo (cuota %) | bandas solapadas |
|---|---|---|---|---|---|---|
| alquiler | P1 | credito_tipos | 63.9 | 2.91 a 4.4 | factor_europeo (13.2) | no |
| alquiler | P2 | credito_tipos | 45.0 | -1.61 a -1.01 | demografia (26.0) | si |
| alquiler | P3 | credito_tipos | 55.3 | -0.83 a -0.54 | demografia (20.7) | no |
| alquiler | P4 | credito_tipos | 70.2 | -9.19 a -4.72 | empleo_renta (24.6) | no |
| alquiler | P5 | credito_tipos | 31.1 | -0.88 a -0.46 | turismo (30.3) | si |
| alquiler | completo | credito_tipos | 71.0 | -13.17 a -8.79 | empleo_renta (10.8) | no |
| compra | P1 | credito_tipos | 47.0 | 31.37 a 56.23 | demografia (20.5) | no |
| compra | P2 | credito_tipos | 36.1 | -26.94 a -12.49 | factor_europeo (24.2) | si |
| compra | P3 | empleo_renta | 26.0 | 1.45 a 3.63 | factor_europeo (25.4) | si |
| compra | P4 | credito_tipos | 34.8 | -3.6 a -1.72 | demografia (17.1) | no |
| compra | P5 | factor_europeo | 31.7 | 4.65 a 9.3 | turismo (28.9) | si |
| compra | completo | factor_europeo | 29.5 | 7.64 a 14.28 | demografia (22.7) | si |

VIF maximo observado: 18.4. P4 (9 trimestres) se declara impreciso (solo 3 familias por GL).
Colinealidad: ver colinealidad.csv y belsley.csv; ortogonalizacion en todos los ordenes (rango min-max) en ortogonalizacion.csv; PC1 en indice_compuesto.csv.
Granger (predictivo, no causal) en granger.csv; LP-OLS EWC h=4-8 (C4) en lp_agregado.csv; BMA en bma.csv; ridge/enet en penalizados.csv.
Fuera de muestra (compra, trimestral, completo; bloques con embargo): {"modelo": "enet (compra, trimestral, completo)", "rmse": 1.4671610609537629, "rmse_ar4": 1.0382000028478129, "dm_vs_ar4": {"DM_HLN": 3.054817670927112, "p": 0.004048279917663811, "p_holm": 0.02833795942364668}}.
Reglas: sin lenguaje causal; interpoladas fuera de la muestra principal; familias sin cobertura excluidas (muestras.csv).
