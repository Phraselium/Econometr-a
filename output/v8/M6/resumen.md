# M6 - colinealidad y peso relativo (capa C4: asociacion)

Ecuacion del crecimiento nacional (log x 100) con una variable por familia; precio real de compra (valor tasado) y alquiler real (IPC alquiler). La dominancia (LMG/Shapley) reparte el R2 y NO es una atribucion causal.

## Mayor cuota de R2 por mercado y periodo (interanual, bandas b90 de la contribucion en pp)

| mercado | periodo | factor | cuota R2 % | b90 contribucion pp | segundo (cuota %) | bandas solapadas |
|---|---|---|---|---|---|---|
| alquiler | P1 | credito_tipos | 67.7 | 2.03 a 3.53 | factor_europeo (14.0) | no |
| alquiler | P2 | credito_tipos | 47.4 | -1.5 a -0.84 | demografia (27.4) | si |
| alquiler | P3 | credito_tipos | 58.0 | -0.65 a -0.35 | demografia (21.7) | si |
| alquiler | P4 | credito_tipos | 70.2 | -8.41 a -3.93 | empleo_renta (24.6) | no |
| alquiler | P5 | credito_tipos | 31.2 | -0.69 a -0.28 | turismo (30.4) | si |
| alquiler | completo | credito_tipos | 74.3 | -10.78 a -6.75 | empleo_renta (11.3) | no |
| compra | P1 | credito_tipos | 64.1 | 17.65 a 52.6 | demografia (27.9) | si |
| compra | P2 | credito_tipos | 37.7 | -19.81 a -4.89 | factor_europeo (25.3) | si |
| compra | P3 | empleo_renta | 28.5 | 0.76 a 2.93 | factor_europeo (27.8) | si |
| compra | P4 | credito_tipos | 58.9 | -3.12 a -0.26 | demografia (29.0) | si |
| compra | P5 | factor_europeo | 32.1 | 2.42 a 7.12 | turismo (29.3) | si |
| compra | completo | factor_europeo | 38.7 | 10.23 a 18.6 | demografia (29.8) | si |

VIF maximo observado: 18.4. P4 (9 trimestres) se declara impreciso (solo 3 familias por GL).
Colinealidad: ver colinealidad.csv y belsley.csv; ortogonalizacion en todos los ordenes (rango min-max) en ortogonalizacion.csv; PC1 en indice_compuesto.csv.
Granger (predictivo, no causal) en granger.csv; LP-OLS EWC h=4-8 (C4) en lp_agregado.csv; BMA en bma.csv; ridge/enet en penalizados.csv.
Fuera de muestra (compra, trimestral, completo; bloques con embargo): {"modelo": "enet (compra, trimestral, completo)", "rmse": 1.4671610609537629, "rmse_ar4": 1.0382000028478129, "dm_vs_ar4": {"DM_HLN": 3.054817670927112, "p": 0.004048279917663811, "p_holm": 0.02833795942364668}}.
Reglas: sin lenguaje causal; interpoladas fuera de la muestra principal; familias sin cobertura excluidas (muestras.csv).
