# R5 · Predicción regional y congelación (informativo, muestra ya vista en v1)

Capa C4 (predicción, no causalidad). Backtest de origen móvil 2016Q1..2026Q1, h=1-4, estimación solo con datos hasta cada origen. Datos hasta 2026Q2 (panel_ccaa_q_v7). RMSE en puntos log x100 (aprox. %).

## Mejor candidato por región frente a la base fuerte (AR con factor común), h=1-4 agrupados

- alquiler: el mejor candidato bate a la base fuerte en 12 de 17 CCAA; frente a la más exigente (mín. de persistencia, ult_crec_nac y ar_factor): 6 de 17 (selección en muestra: optimista).
- compra: el mejor candidato bate a la base fuerte en 17 de 17 CCAA; frente a la más exigente (mín. de persistencia, ult_crec_nac y ar_factor): 5 de 17 (selección en muestra: optimista).

## RMSE x100 a h=1 (17 CCAA, todos los orígenes)

| mercado   |   ar4 |   ar_factor |   ecm_v1 |   gbm |   mixto |   persistencia |   pmg |   ult_crec_nac |
|:----------|------:|------------:|---------:|------:|--------:|---------------:|------:|---------------:|
| alquiler  | 0.215 |       0.217 |    0.237 | 0.195 |   0.207 |          0.439 | 0.273 |          0.212 |
| compra    | 1.373 |       1.743 |    1.59  | 1.38  |   1.699 |          2.1   | 2.113 |          1.524 |

## H7-P1 (mejor regional vs base fuerte, agregado de 17 CCAA; en muestra, con Holm)

| mercado   |   h | comparador   |   dm_hln |   p_dm_mejor |   p_perm_mejor |   n_ccaa_mejor |   rmse_mejor_regional_x100 |   rmse_comparador_x100 |   p_dm_mejor_holm |   p_perm_mejor_holm | nota                                                                           |
|:----------|----:|:-------------|---------:|-------------:|---------------:|---------------:|---------------------------:|-----------------------:|------------------:|--------------------:|:-------------------------------------------------------------------------------|
| alquiler  |   1 | ar_factor    |  -2.5741 |       0.0102 |         0.0002 |             15 |                     0.1967 |                 0.2174 |            0.0408 |              0.0018 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   1 | ar4          |  -4.8557 |       0.0001 |         0.0003 |             16 |                     0.1967 |                 0.2154 |            0.0009 |              0.0021 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   2 | ar_factor    |  -3.3712 |       0.0019 |         0.0002 |             16 |                     0.3388 |                 0.3974 |            0.0156 |              0.0018 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   2 | ar4          |  -5.3147 |       0      |         0      |             16 |                     0.3388 |                 0.4008 |            0.0004 |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   3 | ar_factor    |  -2.7688 |       0.0068 |         0.0003 |             13 |                     0.479  |                 0.5742 |            0.0342 |              0.0021 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   3 | ar4          |  -5.3495 |       0      |         0      |             17 |                     0.479  |                 0.5879 |            0.0004 |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   4 | ar_factor    |  -1.8835 |       0.039  |         0.0245 |             11 |                     0.6485 |                 0.7534 |            0.0779 |              0.0544 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| alquiler  |   4 | ar4          |  -4.7503 |       0.0001 |         0      |             17 |                     0.6485 |                 0.7979 |            0.001  |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   1 | ar_factor    |  -5.8508 |       0      |         0      |             17 |                     1.3381 |                 1.7426 |            0.0002 |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   1 | ar4          |  -1.5746 |       0.0675 |         0.0666 |              6 |                     1.3381 |                 1.3726 |            0.0779 |              0.0666 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   2 | ar_factor    |  -9.5152 |       0      |         0      |             17 |                     2.1658 |                 3.3326 |            0      |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   2 | ar4          |  -2.3159 |       0.0171 |         0.0181 |              7 |                     2.1658 |                 2.2386 |            0.0512 |              0.0544 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   3 | ar_factor    | -10.4704 |       0      |         0      |             17 |                     2.9613 |                 4.9696 |            0      |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   3 | ar4          |  -3.0641 |       0.0037 |         0.0041 |              8 |                     2.9613 |                 3.1128 |            0.026  |              0.0207 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   4 | ar_factor    | -11.0442 |       0      |         0      |             17 |                     3.9343 |                 6.7817 |            0      |              0.0008 | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |
| compra    |   4 | ar4          |  -2.966  |       0.0046 |         0.0082 |              7 |                     3.9343 |                 4.1883 |            0.0273 |              0.033  | selección en muestra (optimista); la validación honesta es la diferida (H7-P1) |

## Notas
- ECM v1 no es replicable por CCAA: se usa un ECM nacional (spec A) con ajuste por nivel.
- PMG sin demeaning ni ajuste de rupturas (se predice en niveles); dX futuro = 0.
- GBM: 1 configuración fija (sin búsqueda). Mixto: pendiente aleatoria en el retardo 1, con alternativas si no converge.
- Un modelo solo «predice mejor» si supera a la base más exigente; los p son por CCAA (n=17), DM-HLN y permutación de signo, Holm por mercado, horizonte y comparador.
- Congelación: output/v7/R5/modelos_congelados.json (sha256 93795a9480eccf03f382bc20253561dd37e240287921453fd0d1add40a9a0646).
