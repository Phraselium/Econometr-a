# Ecuaciones, mercado compra (informativo, muestra ya vista en v1; asociacion de largo plazo, no causal)

## Especificacion A: largo plazo comun (MG con demeaning transversal, ARDL(3,1), 2007Q1-2025Q1)

$$\text{ln\_ipv}_{it} - \bar{\text{ln\_ipv}}_t = \alpha_i + -1.323\,\text{ln\_ocupados}_{it} + -0.146\,\text{ln\_hip\_importe}_{it} + +0.578\,\text{ln\_pob\_total}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec A

$$\Delta \text{ln\_ipv}_{it} = c_i + \varphi_i\Big(\text{ln\_ipv}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{2}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_compraventas}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = +1.765 -0.028\,(y_{t-1} - [-2.871\,\text{ln\_ocupados}_{t-1} + 0.964\,\text{ln\_hip\_importe}_{t-1} + -36.065\,\text{ln\_pob\_total}_{t-1}]) -0.075\,\text{d\_ln\_ocupados\_L0} +0.028\,\text{d\_ln\_hip\_importe\_L0} -0.807\,\text{d\_ln\_pob\_total\_L0} -0.614\,\text{d\_y\_L1} -0.150\,\text{d\_y\_L2} -0.012\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.036)
- Region 02: $\Delta y_t = +0.354 -0.381\,(y_{t-1} - [0.475\,\text{ln\_ocupados}_{t-1} + -0.048\,\text{ln\_hip\_importe}_{t-1} + 4.697\,\text{ln\_pob\_total}_{t-1}]) +0.075\,\text{d\_ln\_ocupados\_L0} -0.001\,\text{d\_ln\_hip\_importe\_L0} +6.237\,\text{d\_ln\_pob\_total\_L0} -0.113\,\text{d\_y\_L1} -0.075\,\text{d\_y\_L2} -0.008\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.136)
- Region 03: $\Delta y_t = +0.165 -0.195\,(y_{t-1} - [0.104\,\text{ln\_ocupados}_{t-1} + 0.151\,\text{ln\_hip\_importe}_{t-1} + 1.393\,\text{ln\_pob\_total}_{t-1}]) -0.035\,\text{d\_ln\_ocupados\_L0} +0.017\,\text{d\_ln\_hip\_importe\_L0} +3.767\,\text{d\_ln\_pob\_total\_L0} -0.195\,\text{d\_y\_L1} +0.060\,\text{d\_y\_L2} -0.007\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.051)
- Region 04: $\Delta y_t = -0.068 +0.043\,(y_{t-1} - [-2.726\,\text{ln\_ocupados}_{t-1} + -0.443\,\text{ln\_hip\_importe}_{t-1} + 7.217\,\text{ln\_pob\_total}_{t-1}]) +0.063\,\text{d\_ln\_ocupados\_L0} +0.019\,\text{d\_ln\_hip\_importe\_L0} -5.462\,\text{d\_ln\_pob\_total\_L0} -0.271\,\text{d\_y\_L1} -0.196\,\text{d\_y\_L2} -0.010\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.062)
- Region 05: $\Delta y_t = +0.039 -0.170\,(y_{t-1} - [0.225\,\text{ln\_ocupados}_{t-1} + -0.127\,\text{ln\_hip\_importe}_{t-1} + -1.001\,\text{ln\_pob\_total}_{t-1}]) +0.021\,\text{d\_ln\_ocupados\_L0} -0.005\,\text{d\_ln\_hip\_importe\_L0} +1.483\,\text{d\_ln\_pob\_total\_L0} -0.225\,\text{d\_y\_L1} -0.537\,\text{d\_y\_L2} +0.005\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.103)
- Region 06: $\Delta y_t = +0.524 -0.006\,(y_{t-1} - [-14.870\,\text{ln\_ocupados}_{t-1} + -7.027\,\text{ln\_hip\_importe}_{t-1} + 112.265\,\text{ln\_pob\_total}_{t-1}]) -0.056\,\text{d\_ln\_ocupados\_L0} -0.024\,\text{d\_ln\_hip\_importe\_L0} +3.982\,\text{d\_ln\_pob\_total\_L0} -0.227\,\text{d\_y\_L1} -0.393\,\text{d\_y\_L2} -0.021\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.069)

## Especificacion B: largo plazo comun (MG con demeaning transversal, ARDL(3,1), 2007Q1-2026Q2)

$$\text{ln\_ipv}_{it} - \bar{\text{ln\_ipv}}_t = \alpha_i + -0.011\,\text{tasa\_paro\_epa}_{it} + +0.012\,\text{ln\_hip\_importe}_{it} + u_{it}$$
(variables en desviacion de su media transversal de cada trimestre; las x entre parentesis son logaritmos salvo tasa_paro_epa en pp)

### ECM por region, spec B

$$\Delta \text{ln\_ipv}_{it} = c_i + \varphi_i\Big(\text{ln\_ipv}_{i,t-1} - \sum_k \theta_{ik}\,x_{k,i,t-1}\Big) + \sum_{j=0}^{0}\gamma_{ij}'\,\Delta x_{i,t-j} + \sum_{j=1}^{2}\lambda_{ij}\Delta y_{i,t-j} + \delta_i\,\Delta \text{ln\_compraventas}_{it} + \varepsilon_{it}$$

- Region 01: $\Delta y_t = -0.035 -0.110\,(y_{t-1} - [0.005\,\text{tasa\_paro\_epa}_{t-1} + 0.153\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.022\,\text{d\_ln\_hip\_importe\_L0} -0.349\,\text{d\_y\_L1} +0.080\,\text{d\_y\_L2} -0.006\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.029)
- Region 02: $\Delta y_t = -0.009 -0.036\,(y_{t-1} - [-0.003\,\text{tasa\_paro\_epa}_{t-1} + -0.685\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.003\,\text{d\_ln\_hip\_importe\_L0} -0.320\,\text{d\_y\_L1} -0.177\,\text{d\_y\_L2} +0.000\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.020)
- Region 03: $\Delta y_t = +0.017 -0.061\,(y_{t-1} - [-0.021\,\text{tasa\_paro\_epa}_{t-1} + 0.370\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.018\,\text{d\_ln\_hip\_importe\_L0} -0.118\,\text{d\_y\_L1} +0.194\,\text{d\_y\_L2} -0.011\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.033)
- Region 04: $\Delta y_t = -0.004 -0.026\,(y_{t-1} - [-0.065\,\text{tasa\_paro\_epa}_{t-1} + 0.491\,\text{ln\_hip\_importe}_{t-1}]) -0.001\,\text{d\_tasa\_paro\_epa\_L0} +0.017\,\text{d\_ln\_hip\_importe\_L0} -0.134\,\text{d\_y\_L1} -0.148\,\text{d\_y\_L2} +0.002\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.036)
- Region 05: $\Delta y_t = +0.002 -0.197\,(y_{t-1} - [0.000\,\text{tasa\_paro\_epa}_{t-1} + -0.081\,\text{ln\_hip\_importe}_{t-1}]) -0.000\,\text{d\_tasa\_paro\_epa\_L0} -0.003\,\text{d\_ln\_hip\_importe\_L0} -0.118\,\text{d\_y\_L1} -0.455\,\text{d\_y\_L2} +0.005\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.057)
- Region 06: $\Delta y_t = -0.010 -0.035\,(y_{t-1} - [0.018\,\text{tasa\_paro\_epa}_{t-1} + -0.332\,\text{ln\_hip\_importe}_{t-1}]) +0.001\,\text{d\_tasa\_paro\_epa\_L0} -0.008\,\text{d\_ln\_hip\_importe\_L0} -0.158\,\text{d\_y\_L1} -0.397\,\text{d\_y\_L2} -0.015\,\text{d\_ln\_compraventas}$ (EE de $\varphi$: 0.067)
