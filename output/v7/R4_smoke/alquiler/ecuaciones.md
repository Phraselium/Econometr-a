# Ecuaciones, mercado alquiler (informativo, muestra ya vista en v1; asociacion de largo plazo, no causal)

## Especificacion A: largo plazo comun (MG con demeaning transversal, ARDL(1,1), 2007Q1-2025Q1)

$$\text{ln\_ipc\_alquiler}_{it} - \bar{\text{ln\_ipc\_alquiler}}_t = \alpha_i + +0.048\,\text{ln\_ocupados}_{it} + -0.154\,\text{ln\_pob\_total}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec A

$$\Delta \text{ln\_ipc\_alquiler}_{it} = c_i + \varphi_i\Big(\text{ln\_ipc\_alquiler}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{0}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_hip\_importe}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = +0.374 -0.176\,(y_{t-1} - [-0.091\,\text{ln\_ocupados}_{t-1} + -1.198\,\text{ln\_pob\_total}_{t-1}]) -0.003\,\text{d\_ln\_ocupados\_L0} -0.549\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.042)
- Region 02: $\Delta y_t = +0.019 -0.152\,(y_{t-1} - [-0.071\,\text{ln\_ocupados}_{t-1} + 0.717\,\text{ln\_pob\_total}_{t-1}]) -0.001\,\text{d\_ln\_ocupados\_L0} +0.209\,\text{d\_ln\_pob\_total\_L0} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.058)
- Region 03: $\Delta y_t = +0.010 +0.034\,(y_{t-1} - [0.226\,\text{ln\_ocupados}_{t-1} + -0.877\,\text{ln\_pob\_total}_{t-1}]) -0.009\,\text{d\_ln\_ocupados\_L0} +1.063\,\text{d\_ln\_pob\_total\_L0} -0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.038)
- Region 04: $\Delta y_t = +0.019 -0.098\,(y_{t-1} - [0.001\,\text{ln\_ocupados}_{t-1} + 0.649\,\text{ln\_pob\_total}_{t-1}]) +0.002\,\text{d\_ln\_ocupados\_L0} +0.449\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.040)
- Region 05: $\Delta y_t = +0.005 -0.118\,(y_{t-1} - [0.068\,\text{ln\_ocupados}_{t-1} + -0.248\,\text{ln\_pob\_total}_{t-1}]) +0.006\,\text{d\_ln\_ocupados\_L0} +0.875\,\text{d\_ln\_pob\_total\_L0} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.030)
- Region 06: $\Delta y_t = +0.029 -0.142\,(y_{t-1} - [0.148\,\text{ln\_ocupados}_{t-1} + 0.045\,\text{ln\_pob\_total}_{t-1}]) -0.021\,\text{d\_ln\_ocupados\_L0} +0.750\,\text{d\_ln\_pob\_total\_L0} +0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.042)

## Especificacion B: largo plazo comun (MG con demeaning transversal, ARDL(4,1), 2007Q1-2026Q2)

$$\text{ln\_ipc\_alquiler}_{it} - \bar{\text{ln\_ipc\_alquiler}}_t = \alpha_i + +0.001\,\text{tasa\_paro\_epa}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec B

$$\Delta \text{ln\_ipc\_alquiler}_{it} = c_i + \varphi_i\Big(\text{ln\_ipc\_alquiler}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{3}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_hip\_importe}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = -0.000 -0.040\,(y_{t-1} - [-0.000\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.420\,\text{d\_y\_L1} -0.470\,\text{d\_y\_L2} +0.416\,\text{d\_y\_L3} +0.002\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.022)
- Region 02: $\Delta y_t = +0.001 -0.022\,(y_{t-1} - [0.008\,\text{tasa\_paro\_epa}_{t-1}]) +0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.128\,\text{d\_y\_L1} -0.021\,\text{d\_y\_L2} +0.295\,\text{d\_y\_L3} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.032)
- Region 03: $\Delta y_t = +0.000 -0.038\,(y_{t-1} - [-0.004\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.464\,\text{d\_y\_L1} -0.034\,\text{d\_y\_L2} +0.013\,\text{d\_y\_L3} -0.003\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.026)
- Region 04: $\Delta y_t = +0.001 +0.006\,(y_{t-1} - [0.006\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.067\,\text{d\_y\_L1} +0.308\,\text{d\_y\_L2} +0.142\,\text{d\_y\_L3} +0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.011)
- Region 05: $\Delta y_t = -0.000 -0.082\,(y_{t-1} - [0.000\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.022\,\text{d\_y\_L1} +0.250\,\text{d\_y\_L2} +0.125\,\text{d\_y\_L3} -0.001\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.028)
- Region 06: $\Delta y_t = -0.000 -0.193\,(y_{t-1} - [-0.003\,\text{tasa\_paro\_epa}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} +0.102\,\text{d\_y\_L1} -0.222\,\text{d\_y\_L2} +0.357\,\text{d\_y\_L3} -0.000\,\text{d\_ln\_hip\_importe}$ (EE de $\varphi$: 0.047)
