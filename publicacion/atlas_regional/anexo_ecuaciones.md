<!-- Generado por `make publicacion` desde output/v7_1/atlas/anexo_ecuaciones.md. No editar a mano: se regenera y un test lo comprueba. -->

# Anexo de ecuaciones y contrastes (V7)

*Capa C4; informativo, muestra ya vista en v1; asociación, sin lectura causal. Generado desde output/v7/R4, R4b, R5 y R6.*

## A. Contrastes y su uso

| contraste | uso | familia de control |
|---|---|---|
| Raíces unitarias de panel (CIPS) y por región | orden de integración | informativo; I(2) no se descarta en 8 de 17 CCAA |
| Cointegración de panel y por región | existencia de largo plazo | Holm por familia |
| t de MG, PMG, DFE y CS-DL con bootstrap salvaje (Webb) y Driscoll-Kraay | hipótesis H7 | Holm |
| Breusch-Godfrey, Breusch-Pagan, Jarque-Bera, RESET, CUSUM, VIF | diagnósticos por región | descriptivo |
| Bai-Perron | cambios estructurales | descriptivo |
| Diebold-Mariano y permutación | backtest R5 | Holm |
| Coeficientes de corto plazo por región | exploratorio | BH, q = 0,10 |

## B. Ecuaciones R4, alquiler


#### Especificacion A: largo plazo comun (MG con demeaning transversal, ARDL(1,1), 2007Q1-2025Q1)

$$\text{ln\_ipc\_alquiler}_{it} - \bar{\text{ln\_ipc\_alquiler}}_t = \alpha_i + +0.088\,\text{ln\_ocupados}_{it} + +0.894\,\text{ln\_pob\_total}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec A

$$\Delta \text{ln\_ipc\_alquiler}_{it} = c_i + \varphi_i\Big(\text{ln\_ipc\_alquiler}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{0}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_hip\_importe}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = +0.050 +0.017\,(y_{t-1} - [0.301\,\text{ln\_ocupados}_{t-1} + 1.631\,\text{ln\_pob\_total}_{t-1}]) +0.003\,\text{d\_ln\_ocupados\_L0} -0.448\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.045)
- Region 02: $\Delta y_t = +0.004 -0.104\,(y_{t-1} - [-0.122\,\text{ln\_ocupados}_{t-1} + 0.220\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} +0.365\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.043)
- Region 03: $\Delta y_t = +0.020 +0.022\,(y_{t-1} - [0.610\,\text{ln\_ocupados}_{t-1} + -2.081\,\text{ln\_pob\_total}_{t-1}]) -0.007\,\text{d\_ln\_ocupados\_L0} +1.114\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.026)
- Region 04: $\Delta y_t = +0.033 -0.087\,(y_{t-1} - [0.009\,\text{ln\_ocupados}_{t-1} + 0.812\,\text{ln\_pob\_total}_{t-1}]) +0.002\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.045)
- Region 05: $\Delta y_t = -0.005 -0.140\,(y_{t-1} - [0.039\,\text{ln\_ocupados}_{t-1} + 0.157\,\text{ln\_pob\_total}_{t-1}]) +0.007\,\text{d\_ln\_ocupados\_L0} +0.298\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.040)
- Region 06: $\Delta y_t = -0.010 -0.099\,(y_{t-1} - [-0.032\,\text{ln\_ocupados}_{t-1} + -0.069\,\text{ln\_pob\_total}_{t-1}]) -0.026\,\text{d\_ln\_ocupados\_L0} +1.266\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.026)
- Region 07: $\Delta y_t = -0.002 -0.007\,(y_{t-1} - [8.376\,\text{ln\_ocupados}_{t-1} + -6.155\,\text{ln\_pob\_total}_{t-1}]) +0.039\,\text{d\_ln\_ocupados\_L0} +0.826\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.022)
- Region 08: $\Delta y_t = -0.011 -0.132\,(y_{t-1} - [0.071\,\text{ln\_ocupados}_{t-1} + 0.828\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.346\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.044)
- Region 09: $\Delta y_t = +0.105 +0.009\,(y_{t-1} - [3.603\,\text{ln\_ocupados}_{t-1} + 4.596\,\text{ln\_pob\_total}_{t-1}]) -0.016\,\text{d\_ln\_ocupados\_L0} -0.533\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.010)
- Region 10: $\Delta y_t = -0.138 -0.147\,(y_{t-1} - [-0.072\,\text{ln\_ocupados}_{t-1} + 0.979\,\text{ln\_pob\_total}_{t-1}]) -0.012\,\text{d\_ln\_ocupados\_L0} +0.601\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.054)
- Region 11: $\Delta y_t = +0.001 -0.044\,(y_{t-1} - [-0.239\,\text{ln\_ocupados}_{t-1} + 0.319\,\text{ln\_pob\_total}_{t-1}]) -0.023\,\text{d\_ln\_ocupados\_L0} +0.409\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.050)
- Region 12: $\Delta y_t = -0.006 +0.014\,(y_{t-1} - [-1.212\,\text{ln\_ocupados}_{t-1} + -0.232\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.534\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.032)
- Region 13: $\Delta y_t = +0.023 +0.053\,(y_{t-1} - [0.953\,\text{ln\_ocupados}_{t-1} + -0.696\,\text{ln\_pob\_total}_{t-1}]) -0.008\,\text{d\_ln\_ocupados\_L0} +0.780\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.020)
- Region 14: $\Delta y_t = -0.011 -0.041\,(y_{t-1} - [0.012\,\text{ln\_ocupados}_{t-1} + -1.146\,\text{ln\_pob\_total}_{t-1}]) -0.004\,\text{d\_ln\_ocupados\_L0} +0.373\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.035)
- Region 15: $\Delta y_t = -0.015 -0.032\,(y_{t-1} - [-1.191\,\text{ln\_ocupados}_{t-1} + 0.748\,\text{ln\_pob\_total}_{t-1}]) -0.044\,\text{d\_ln\_ocupados\_L0} +1.579\,\text{d\_ln\_pob\_total\_L0} -0.005\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.020)
- Region 16: $\Delta y_t = -0.000 +0.005\,(y_{t-1} - [-6.127\,\text{ln\_ocupados}_{t-1} + 7.205\,\text{ln\_pob\_total}_{t-1}]) +0.006\,\text{d\_ln\_ocupados\_L0} -0.193\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.040)
- Region 17: $\Delta y_t = +0.678 -0.099\,(y_{t-1} - [0.149\,\text{ln\_ocupados}_{t-1} + 3.708\,\text{ln\_pob\_total}_{t-1}]) +0.015\,\text{d\_ln\_ocupados\_L0} -0.697\,\text{d\_ln\_pob\_total\_L0} +0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.020)

#### Especificacion B: largo plazo comun (MG con demeaning transversal, ARDL(2,1), 2007Q1-2026Q2)

$$\text{ln\_ipc\_alquiler}_{it} - \bar{\text{ln\_ipc\_alquiler}}_t = \alpha_i + -0.004\,\text{tasa\_paro\_epa}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec B

$$\Delta \text{ln\_ipc\_alquiler}_{it} = c_i + \varphi_i\Big(\text{ln\_ipc\_alquiler}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{1}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_hip\_importe}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = +0.000 -0.034\,(y_{t-1} - [-0.002\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.162\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.027)
- Region 02: $\Delta y_t = +0.001 -0.134\,(y_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.016\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.021)
- Region 03: $\Delta y_t = +0.000 -0.013\,(y_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.172\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.018)
- Region 04: $\Delta y_t = +0.002 +0.011\,(y_{t-1} - [0.006\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.040\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.007)
- Region 05: $\Delta y_t = -0.000 -0.105\,(y_{t-1} - [-0.001\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.140\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.056)
- Region 06: $\Delta y_t = +0.001 -0.124\,(y_{t-1} - [0.000\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.073\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.026)
- Region 07: $\Delta y_t = -0.001 -0.029\,(y_{t-1} - [-0.025\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.331\,\text{d\_y\_L1} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.020)
- Region 08: $\Delta y_t = +0.000 -0.021\,(y_{t-1} - [-0.004\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.154\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.020)
- Region 09: $\Delta y_t = +0.002 +0.012\,(y_{t-1} - [-0.052\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.529\,\text{d\_y\_L1} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.015)
- Region 10: $\Delta y_t = +0.002 +0.019\,(y_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.407\,\text{d\_y\_L1} -0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.016)
- Region 11: $\Delta y_t = +0.000 -0.004\,(y_{t-1} - [-0.016\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.293\,\text{d\_y\_L1} -0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.012)
- Region 12: $\Delta y_t = -0.001 +0.031\,(y_{t-1} - [0.027\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.386\,\text{d\_y\_L1} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.013)
- Region 13: $\Delta y_t = +0.002 -0.016\,(y_{t-1} - [0.042\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.460\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.013)
- Region 14: $\Delta y_t = +0.001 -0.006\,(y_{t-1} - [-0.073\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.294\,\text{d\_y\_L1} +0.006\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.011)
- Region 15: $\Delta y_t = +0.000 -0.039\,(y_{t-1} - [0.004\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.285\,\text{d\_y\_L1} -0.004\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.009)
- Region 16: $\Delta y_t = -0.002 -0.028\,(y_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.387\,\text{d\_y\_L1} +0.003\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.022)
- Region 17: $\Delta y_t = +0.000 -0.014\,(y_{t-1} - [0.015\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.105\,\text{d\_y\_L1} +0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.009)

## B. Ecuaciones R4, compra


#### Especificacion A: largo plazo comun (MG con demeaning transversal, ARDL(1,1), 2007Q1-2025Q1)

$$\text{ln\_ipv}_{it} - \bar{\text{ln\_ipv}}_t = \alpha_i + -0.460\,\text{ln\_ocupados}_{it} + +0.304\,\text{ln\_hip\_importe}_{it} + -1.957\,\text{ln\_pob\_total}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec A

$$\Delta \text{ln\_ipv}_{it} = c_i + \varphi_i\Big(\text{ln\_ipv}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{0}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_compraventas}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = +0.482 -0.008\,(y_{t-1} - [-9.625\,\text{ln\_ocupados}_{t-1} + 2.713\,\text{ln\_hip\_importe}_{t-1} + -32.573\,\text{ln\_pob\_total}_{t-1}]) -0.125\,\text{d\_ln\_ocupados\_L0} +0.035\,\text{d\_ln\_hip\_importe\_L0} -0.058\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.030)
- Region 02: $\Delta y_t = +0.291 -0.211\,(y_{t-1} - [0.116\,\text{ln\_ocupados}_{t-1} + -0.120\,\text{ln\_hip\_importe}_{t-1} + 4.096\,\text{ln\_pob\_total}_{t-1}]) +0.050\,\text{d\_ln\_ocupados\_L0} -0.015\,\text{d\_ln\_hip\_importe\_L0} +6.111\,\text{d\_ln\_pob\_total\_L0} +0.005\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.055)
- Region 03: $\Delta y_t = +0.170 -0.235\,(y_{t-1} - [-0.135\,\text{ln\_ocupados}_{t-1} + 0.115\,\text{ln\_hip\_importe}_{t-1} + 1.135\,\text{ln\_pob\_total}_{t-1}]) -0.074\,\text{d\_ln\_ocupados\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} +5.166\,\text{d\_ln\_pob\_total\_L0} -0.001\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.063)
- Region 04: $\Delta y_t = -0.039 -0.012\,(y_{t-1} - [10.192\,\text{ln\_ocupados}_{t-1} + 0.801\,\text{ln\_hip\_importe}_{t-1} + -15.928\,\text{ln\_pob\_total}_{t-1}]) +0.087\,\text{d\_ln\_ocupados\_L0} +0.012\,\text{d\_ln\_hip\_importe\_L0} -4.358\,\text{d\_ln\_pob\_total\_L0} -0.025\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.059)
- Region 05: $\Delta y_t = -0.064 -0.318\,(y_{t-1} - [0.151\,\text{ln\_ocupados}_{t-1} + -0.004\,\text{ln\_hip\_importe}_{t-1} + 1.080\,\text{ln\_pob\_total}_{t-1}]) +0.098\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +2.245\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.093)
- Region 06: $\Delta y_t = -0.041 -0.090\,(y_{t-1} - [-0.529\,\text{ln\_ocupados}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1} + 0.344\,\text{ln\_pob\_total}_{t-1}]) -0.045\,\text{d\_ln\_ocupados\_L0} -0.005\,\text{d\_ln\_hip\_importe\_L0} +1.235\,\text{d\_ln\_pob\_total\_L0} -0.018\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.070)
- Region 07: $\Delta y_t = -0.036 -0.368\,(y_{t-1} - [0.371\,\text{ln\_ocupados}_{t-1} + 0.144\,\text{ln\_hip\_importe}_{t-1} + 0.196\,\text{ln\_pob\_total}_{t-1}]) +0.032\,\text{d\_ln\_ocupados\_L0} +0.033\,\text{d\_ln\_hip\_importe\_L0} +2.867\,\text{d\_ln\_pob\_total\_L0} -0.022\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.097)
- Region 08: $\Delta y_t = -0.042 -0.045\,(y_{t-1} - [3.379\,\text{ln\_ocupados}_{t-1} + 0.225\,\text{ln\_hip\_importe}_{t-1} + 9.014\,\text{ln\_pob\_total}_{t-1}]) -0.009\,\text{d\_ln\_ocupados\_L0} -0.011\,\text{d\_ln\_hip\_importe\_L0} +0.258\,\text{d\_ln\_pob\_total\_L0} -0.003\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.035)
- Region 09: $\Delta y_t = +0.548 -0.111\,(y_{t-1} - [-1.536\,\text{ln\_ocupados}_{t-1} + 0.279\,\text{ln\_hip\_importe}_{t-1} + -2.336\,\text{ln\_pob\_total}_{t-1}]) +0.084\,\text{d\_ln\_ocupados\_L0} +0.030\,\text{d\_ln\_hip\_importe\_L0} +6.163\,\text{d\_ln\_pob\_total\_L0} -0.006\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.029)
- Region 10: $\Delta y_t = +0.179 -0.188\,(y_{t-1} - [0.213\,\text{ln\_ocupados}_{t-1} + -0.104\,\text{ln\_hip\_importe}_{t-1} + -1.093\,\text{ln\_pob\_total}_{t-1}]) -0.032\,\text{d\_ln\_ocupados\_L0} -0.023\,\text{d\_ln\_hip\_importe\_L0} +2.330\,\text{d\_ln\_pob\_total\_L0} -0.034\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.063)
- Region 11: $\Delta y_t = +0.160 -0.156\,(y_{t-1} - [-0.829\,\text{ln\_ocupados}_{t-1} + 0.170\,\text{ln\_hip\_importe}_{t-1} + 2.305\,\text{ln\_pob\_total}_{t-1}]) -0.080\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +5.770\,\text{d\_ln\_pob\_total\_L0} +0.012\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.049)
- Region 12: $\Delta y_t = +0.013 -0.219\,(y_{t-1} - [0.621\,\text{ln\_ocupados}_{t-1} + 0.052\,\text{ln\_hip\_importe}_{t-1} + -0.626\,\text{ln\_pob\_total}_{t-1}]) +0.044\,\text{d\_ln\_ocupados\_L0} -0.002\,\text{d\_ln\_hip\_importe\_L0} +2.006\,\text{d\_ln\_pob\_total\_L0} -0.014\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.065)
- Region 13: $\Delta y_t = -0.131 -0.080\,(y_{t-1} - [-0.755\,\text{ln\_ocupados}_{t-1} + 0.469\,\text{ln\_hip\_importe}_{t-1} + 1.350\,\text{ln\_pob\_total}_{t-1}]) -0.078\,\text{d\_ln\_ocupados\_L0} +0.041\,\text{d\_ln\_hip\_importe\_L0} +1.261\,\text{d\_ln\_pob\_total\_L0} +0.035\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.031)
- Region 14: $\Delta y_t = -0.010 -0.068\,(y_{t-1} - [0.643\,\text{ln\_ocupados}_{t-1} + 0.126\,\text{ln\_hip\_importe}_{t-1} + -1.851\,\text{ln\_pob\_total}_{t-1}]) -0.086\,\text{d\_ln\_ocupados\_L0} +0.018\,\text{d\_ln\_hip\_importe\_L0} -2.960\,\text{d\_ln\_pob\_total\_L0} -0.008\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.063)
- Region 15: $\Delta y_t = -1.156 -0.271\,(y_{t-1} - [-0.372\,\text{ln\_ocupados}_{t-1} + -0.139\,\text{ln\_hip\_importe}_{t-1} + -3.632\,\text{ln\_pob\_total}_{t-1}]) -0.095\,\text{d\_ln\_ocupados\_L0} -0.026\,\text{d\_ln\_hip\_importe\_L0} -20.330\,\text{d\_ln\_pob\_total\_L0} +0.008\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.074)
- Region 16: $\Delta y_t = -0.078 -0.272\,(y_{t-1} - [-0.086\,\text{ln\_ocupados}_{t-1} + -0.024\,\text{ln\_hip\_importe}_{t-1} + 2.117\,\text{ln\_pob\_total}_{t-1}]) +0.000\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +1.824\,\text{d\_ln\_pob\_total\_L0} +0.004\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.092)
- Region 17: $\Delta y_t = +1.706 -0.179\,(y_{t-1} - [-0.361\,\text{ln\_ocupados}_{t-1} + 0.086\,\text{ln\_hip\_importe}_{t-1} + 5.646\,\text{ln\_pob\_total}_{t-1}]) +0.094\,\text{d\_ln\_ocupados\_L0} +0.003\,\text{d\_ln\_hip\_importe\_L0} +3.661\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.070)

#### Especificacion B: largo plazo comun (MG con demeaning transversal, ARDL(1,1), 2007Q1-2026Q2)

$$\text{ln\_ipv}_{it} - \bar{\text{ln\_ipv}}_t = \alpha_i + -0.015\,\text{tasa\_paro\_epa}_{it} + +0.449\,\text{ln\_hip\_importe}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec B

$$\Delta \text{ln\_ipv}_{it} = c_i + \varphi_i\Big(\text{ln\_ipv}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{0}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_compraventas}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = -0.036 -0.053\,(y_{t-1} - [0.011\,\text{tasa\_paro\_epa}_{t-1} + 0.343\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.012\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.020)
- Region 02: $\Delta y_t = -0.002 -0.070\,(y_{t-1} - [0.018\,\text{tasa\_paro\_epa}_{t-1} + -0.219\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.009\,\text{d\_ln\_hip\_importe\_L0} +0.006\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.020)
- Region 03: $\Delta y_t = +0.017 -0.079\,(y_{t-1} - [-0.015\,\text{tasa\_paro\_epa}_{t-1} + 0.251\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.002\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.041)
- Region 04: $\Delta y_t = -0.000 -0.017\,(y_{t-1} - [-0.098\,\text{tasa\_paro\_epa}_{t-1} + 0.373\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.014\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.034)
- Region 05: $\Delta y_t = -0.000 -0.102\,(y_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.107\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.003\,\text{d\_ln\_hip\_importe\_L0} -0.007\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.038)
- Region 06: $\Delta y_t = -0.007 -0.149\,(y_{t-1} - [0.019\,\text{tasa\_paro\_epa}_{t-1} + -0.067\,\text{ln\_hip\_importe}_{t-1}]) +0.003\,\text{d\_tasa\_paro\_epa\_L0} +0.000\,\text{d\_ln\_hip\_importe\_L0} -0.015\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.062)
- Region 07: $\Delta y_t = +0.010 -0.174\,(y_{t-1} - [0.008\,\text{tasa\_paro\_epa}_{t-1} + 0.237\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.019\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.066)
- Region 08: $\Delta y_t = +0.003 +0.006\,(y_{t-1} - [0.205\,\text{tasa\_paro\_epa}_{t-1} + -0.994\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.013\,\text{d\_ln\_hip\_importe\_L0} -0.004\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.013)
- Region 09: $\Delta y_t = -0.010 -0.061\,(y_{t-1} - [-0.121\,\text{tasa\_paro\_epa}_{t-1} + -0.084\,\text{ln\_hip\_importe}_{t-1}]) -0.005\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.011\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.022)
- Region 10: $\Delta y_t = +0.013 -0.173\,(y_{t-1} - [-0.006\,\text{tasa\_paro\_epa}_{t-1} + -0.080\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.016\,\text{d\_ln\_hip\_importe\_L0} -0.032\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.059)
- Region 11: $\Delta y_t = +0.045 -0.001\,(y_{t-1} - [-1.219\,\text{tasa\_paro\_epa}_{t-1} + 24.398\,\text{ln\_hip\_importe}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.007\,\text{d\_ln\_hip\_importe\_L0} +0.018\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.019)
- Region 12: $\Delta y_t = +0.002 -0.173\,(y_{t-1} - [-0.013\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.002\,\text{d\_tasa\_paro\_epa\_L0} -0.004\,\text{d\_ln\_hip\_importe\_L0} -0.013\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.035)
- Region 13: $\Delta y_t = -0.084 -0.088\,(y_{t-1} - [0.039\,\text{tasa\_paro\_epa}_{t-1} + 0.538\,\text{ln\_hip\_importe}_{t-1}]) +0.002\,\text{d\_tasa\_paro\_epa\_L0} +0.048\,\text{d\_ln\_hip\_importe\_L0} +0.035\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.022)
- Region 14: $\Delta y_t = +0.006 -0.072\,(y_{t-1} - [0.014\,\text{tasa\_paro\_epa}_{t-1} + 0.227\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.006\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.044)
- Region 15: $\Delta y_t = -0.014 -0.065\,(y_{t-1} - [-0.005\,\text{tasa\_paro\_epa}_{t-1} + -0.196\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.008\,\text{d\_ln\_hip\_importe\_L0} -0.001\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.022)
- Region 16: $\Delta y_t = -0.000 -0.134\,(y_{t-1} - [0.003\,\text{tasa\_paro\_epa}_{t-1} + 0.055\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.004\,\text{d\_ln\_hip\_importe\_L0} +0.000\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.061)
- Region 17: $\Delta y_t = +0.028 -0.066\,(y_{t-1} - [0.024\,\text{tasa\_paro\_epa}_{t-1} + 0.185\,\text{ln\_hip\_importe}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.001\,\text{d\_ln\_hip\_importe\_L0} +0.001\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.038)

## C. Ecuaciones R6 (traslado e incidencia, condicional)


Todo el texto es condicional: «si se hiciera X, con estos supuestos…». No se afirma causalidad (C4). Se evalúan instrumentos, no actores.

## Ecuaciones (equilibrio parcial, mercado local)

Demanda con elasticidad $\varepsilon_d<0$ y oferta con elasticidad $\varepsilon_s\ge 0$ (respecto del precio).

1. Incidencia de una ayuda a la demanda sobre el precio (parte que capta el vendedor):
$$\iota=\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}\in(0,1]$$
2. Variación del precio ante una ayuda de demanda de intensidad $s$ (fracción del precio pagado), con ajuste completo:
$$\frac{\Delta p}{p}=s\,\iota=s\,\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}$$
   Precio neto pagado por el comprador: $\frac{\Delta p^{n}}{p}\approx -s\,(1-\iota)=-s\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$. Con $\varepsilon_s=0$ el precio absorbe toda la ayuda y el esfuerzo no varía.
3. Variación del precio ante un aumento de oferta $\Delta Q/Q$:
$$\frac{\Delta p}{p}=-\frac{\Delta Q/Q}{\varepsilon_s+|\varepsilon_d|}$$
4. Rebaja de un impuesto al coste de construcción $c$ (cuota $\kappa$ del coste en el precio), desplazamiento de la oferta:
$$\frac{\Delta p}{p}=-c\,\kappa\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$$
5. Senda de ajuste a horizonte $h$ años, con semivida $\tau$ (trimestres): $A(h)=1-2^{-4h/\tau}$, de modo que el efecto es el de las ecuaciones 2-4 multiplicado por $A(h)$.
6. Esfuerzo (compra) = precio neto pagado / renta, con la renta constante: su variación porcentual es la del precio neto. Para el alquiler, la variación de la renta.
7. Coste por euro: $\text{coste}/(\text{reducción del precio neto}\times\text{valor anual de compras})$, que en demanda es $1/(1-\iota)$ en el límite.

## Supuestos y capa

| Supuesto | Valor | Capa |
|---|---|---|
| Equilibrio parcial, un solo mercado local por CCAA, sin cambios de composición | — | C4 |
| $\lvert\varepsilon_d\rvert$ | rejilla uniforme 0,3-1,5 (P-D v3 / v5). Literatura sin valor verificado en docs/literatura.md: NO VERIFICADA | C4 |
| $\varepsilon_s$ rejilla | por clase A4 (método A de v5: percentiles 25-75 de la respuesta de oferta; método B: 1,75 / 0 / 0,45), media ponderada por déficit de las provincias de cada CCAA, cruce por código INE. Referencias: Saiz (2010, DOI verificado, cuartil no verificado); BdE IA 2025 (≈0,45) | C4 |
| $\varepsilon_s$ regional | DOLS ±2 de ln(visados) sobre ln(IPV/IPCA), 2008-2025, por CCAA; MG solo como insumo. Se usa si IC95 en [0; 5] y diagnósticos (cointegración Engle-Granger p<0,10; Ljung-Box(4) p>0,05) | C4 |
| Senda de ajuste | semivida entre las medianas regionales de R4 (spec A y B). Supuesto de senda: la inferencia de R4 no es válida (sin largo plazo identificado) | C4 |
| Ofertas: llegada | 1 año de trámite y obra antes de completarse; el acumulado es lineal | C4 |
| (a) construcción adicional | min(necesidad anual central T3, máximo anual de visados 2016-2025 menos visados 2025) × U(0,5; 1) | C4 |
| (b) vacías | triangular(M_min, M_central, M_max) de T3 / 10 años (v5 B1/T3) | C4 |
| (c) vivienda pública | 20 % de la necesidad anual central × U(0,5; 1,5), con desplazamiento de la promoción privada U(0; 0,5) | C4 |
| (d) turísticos | 5-30 % del stock de VUT regional vuelve al uso residencial; la cota nacional B4-v3-vut-cantidad (2,746 % del stock de alquiler, C2) no se reparte por CCAA | C4 |
| (e) ayuda a la demanda | 5-15 % del precio o la renta | C4 |
| (f1) rebaja ITP / IVA vivienda nueva | 1-4 puntos del precio; sin tipos vigentes por CCAA en data/raw: escenario genérico | C4 |
| (f2) impuestos a la construcción | rebaja del coste 2-6 %, cuota del coste en el precio 40-70 % | C4 |
| Reparto a alquiler | parque en alquiler 15-20 %; fracción de ΔQ al alquiler: (a) 10-30 %, (b) 30-70 %, (c) 80-100 %, (d) 100 % | C4 |
| Coste fiscal | s × compraventas 2025 × 90 m² × precio tasado (€/m²), sin efectos inducidos. Alquiler y oferta: sin base | C4 |

## Regla de «recomendación robusta» (adaptación declarada)

El encargo de V7 pedía robustez por PMG y jerárquico. R4 no identificó un largo plazo estable, así que se adapta: una combinación CCAA × instrumento es robusta solo si (i) la variación del esfuerzo es negativa en TODAS las extracciones de Monte Carlo y en los tres horizontes, y menor que -0,1 % a 10 años (materialidad), con la rejilla de $\varepsilon_s$, y (ii) lo mismo con la elasticidad regional cuando es utilizable. Si la regional no es utilizable, la robustez es «solo con rejilla» y se declara.

## D. Referencias

- Pesaran, M. H., Shin, Y. y Smith, R. P. (1999). Pooled mean group estimation of dynamic heterogeneous panels. JASA. NO VERIFICADA (cuartil no verificado).
- Pesaran, M. H. (2006). Estimation and inference in large heterogeneous panels with a multifactor error structure. Econometrica. NO VERIFICADA (cuartil no verificado).
- Pesaran, M. H. (2007). A simple panel unit root test in the presence of cross-section dependence. J. Applied Econometrics. NO VERIFICADA (cuartil no verificado).
- Chudik, A., Mohaddes, K., Pesaran, M. H. y Raissi, M. (2016). Long-run effects in large heterogeneous panel data models with cross-sectionally correlated errors. Advances in Econometrics. NO VERIFICADA (cuartil no verificado).
- Webb, M. D. (2014). Reworking wild bootstrap based inference for clustered errors. Queen's Economics Department WP 1315. NO VERIFICADA.
- Driscoll, J. C. y Kraay, A. C. (1998). Consistent covariance matrix estimation with spatially dependent panel data. Review of Economics and Statistics. NO VERIFICADA (cuartil no verificado).
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian J. Statistics. NO VERIFICADA (cuartil no verificado).
- Benjamini, Y. y Hochberg, Y. (1995). Controlling the false discovery rate. JRSS B. NO VERIFICADA (cuartil no verificado).
- Diebold, F. X. y Mariano, R. S. (1995). Comparing predictive accuracy. J. Business & Economic Statistics. NO VERIFICADA (cuartil no verificado).
- Bai, J. y Perron, P. (2003). Computation and analysis of multiple structural change models. J. Applied Econometrics. NO VERIFICADA (cuartil no verificado).
- Breusch-Godfrey (autocorrelación), Breusch-Pagan (heterocedasticidad), Jarque-Bera (normalidad), RESET de Ramsey (forma funcional), CUSUM de Brown-Durbin-Evans (estabilidad), VIF (colinealidad): contrastes estándar. NO VERIFICADA (referencias no consultadas en Crossref en este encargo).
