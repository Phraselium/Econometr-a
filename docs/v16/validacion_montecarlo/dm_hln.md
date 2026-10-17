# Validación Monte Carlo V16 · dm_hln (Q10, Diebold-Mariano con HLN; alternativa Clark-West)

Código: `src/v16/montecarlo/dm_hln.py` · semilla `default_rng([20261010, 4, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** h = 1; ventana expansiva con 30 observaciones iniciales y P = 75 errores fuera de muestra.
- **Verdad:** y_t = 0,1 + 0,5 y_t-1 + 0,1 y_t-2 + 0,05 y_t-3 − 0,05 y_t-4 + β x_t-1 + e_t, e ~ N(0,1), x AR(1) con 0,3 (valores declarados, no calibrados con datos reales).
- **Modelos (anidados):** AR(4) con constante frente a AR(4) + x_t-1, reestimados cada periodo por MCO.
- **Nulo:** β = 0 (el modelo grande añade un regresor irrelevante: caso anidado clásico en que DM sobrerrechaza o subrechaza). **Alternativa:** β = 1/3 (reducción poblacional del ECM ≈ 10 %, la relevancia mínima de la adenda).
- **Pruebas:** DM-HLN (t con P−1 g. de l.; unilateral, H1: el modelo grande reduce el ECM; también bilateral); DM con normal; Clark-West (normal y t) como alternativa nombrada para pares anidados.
- **Réplicas:** 2.000 bajo el nulo, 1.000 bajo la alternativa.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, 1.000 bajo la alternativa)

| escenario       |    R |   tam_HLN_unilateral |   tam_HLN_bilateral |   tam_DM_normal_unilateral |   CW_normal_unilateral |   CW_t_unilateral |   reduccion_ECM_media |
|:----------------|-----:|---------------------:|--------------------:|---------------------------:|-----------------------:|------------------:|----------------------:|
| nulo_anidado    | 2000 |                0.002 |               0.069 |                      0.002 |                  0.033 |             0.032 |            -0.0214849 |
| alt_reduccion10 | 1000 |                0.277 |               0.167 |                      0.287 |                  0.824 |             0.82  |             0.0838235 |

**Veredicto: NO APTO → diseño solo descriptivo** tamaño 0.0020 fuera de [0.04; 0.06]; Clark-West: tamaño 0.0330 fuera de [0.04; 0.06]
