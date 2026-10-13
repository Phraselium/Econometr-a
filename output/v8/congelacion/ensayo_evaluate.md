# Ensayo de evaluate_v8 (--simular)

Objetivos evaluados: 2024Q1, 2024Q2, 2024Q3, 2024Q4; modelos: 3.

## RMSE (pp, crecimiento trimestral real log x100)

| mercado | modelo | RMSE | n |
|---|---|---|---|
| alquiler | ar4 | 0.693 | 4 |
| alquiler | ar_fc | 0.692 | 4 |
| alquiler | ecm_v1 | 1.432 | 4 |
| compra | ar4 | 1.166 | 4 |
| compra | ar_fc | 1.225 | 4 |
| compra | ecm_v1 | 1.994 | 4 |

## DM-HLN y Holm (vs AR(4) y vs AR + factor comun)

| mercado | modelo | ref | RMSE/RMSE_ref | DM-HLN | p | p Holm |
|---|---|---|---|---|---|---|
| alquiler | ar4 | ar_fc | 1.00 | 0.04 | 0.969 | 0.969 |
| alquiler | ecm_v1 | ar4 | 2.06 | 1.83 | 0.165 | 0.660 |
| alquiler | ecm_v1 | ar_fc | 2.07 | 1.76 | 0.177 | 0.660 |
| compra | ar4 | ar_fc | 0.95 | -1.50 | 0.230 | 0.660 |
| compra | ecm_v1 | ar4 | 1.71 | 3.30 | 0.046 | 0.261 |
| compra | ecm_v1 | ar_fc | 1.63 | 3.37 | 0.043 | 0.261 |

Aviso: con 4 objetivos de un solo origen los p son DESCRIPTIVOS (potencia muy baja). C4: prediccion, no causalidad.

Condiciones del ensayo: origen 2023Q4, objetivos 2024T1-T4 (YA VISTOS: dentro de la muestra de entrenamiento de la congelacion; no es evidencia); modelos ar4, ar_fc, ecm_v1 (el BVAR de M2 no se re-estima en el ensayo). Sin red; no se escribe docs/v8/evaluate_v8_accesos.md.
