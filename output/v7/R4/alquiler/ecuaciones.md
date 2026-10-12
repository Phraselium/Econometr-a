# Ecuaciones, mercado alquiler (informativo, muestra ya vista en v1; asociacion de largo plazo, no causal)

## Especificacion A: largo plazo comun (MG con demeaning transversal, ARDL(1,1), 2007Q1-2025Q1)

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

## Especificacion B: largo plazo comun (MG con demeaning transversal, ARDL(2,1), 2007Q1-2026Q2)

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
