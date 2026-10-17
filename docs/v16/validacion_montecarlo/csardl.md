# Validación Monte Carlo V16 · csardl (Q9-c, CS-ARDL)

Código: `src/v16/montecarlo/csardl.py` · semilla `default_rng([20261010, 2, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** N = 38, T = 95. Resultado y_it (log valor tasado simulado) y regresor x_it (log IPC de alquiler simulado).
- **Modelo:** ARDL(1,1): y_it = φ_i y_i,t-1 + β0_i x_it + β1_i x_i,t-1 + γ^y_i f_t + 0,7 e_it, con φ_i ~ U(0,5; 0,8) y elasticidad de largo plazo θ_i = (β0+β1)/(1−φ) ~ N(0,8; 0,2²) (heterogeneidad). x_it = ρ^x_i x_i,t-1 + γ^x_i f_t + u_it, ρ^x_i ~ U(0,3; 0,7).
- **Dependencia transversal:** un factor común f_t AR(1) ρ = 0,6, cargas N(1; 0,5²) en x e y; correlación espacial en anillo (0,25) en u y e. Pocos clusters: no aplica (inferencia por bloques de tiempo, no por cluster).
- **Estimador:** CS-ARDL por unidad con medias transversales de y y x y sus ⌊T^(1/3)⌋ = 4 rezagos; θ̂_MG = media de (b0+b1)/(1−φ̂).
- **Objetivo:** media muestral de los θ_i verdaderos. Inferencia: bootstrap de bloques móviles (longitud ≈ 9) de las filas de regresión conjuntas para las N unidades, B = 99, IC normal con EE bootstrap (y percentil centrado como diagnóstico).
- **Tamaño** = 1 − cobertura del mismo IC; **potencia** frente a θ = 0 y frente a un desplazamiento declarado de 0,2 (Q9-c no tiene magnitud de referencia). R = 2.000.

<!-- RESULTADOS -->
## Resultados (R=2000, B=99, bloque=9)

| medida                       |      valor |
|:-----------------------------|-----------:|
| sesgo                        | -0.0390991 |
| rmse                         |  0.0656413 |
| cobertura_normal_boot        |  0.8985    |
| cobertura_percentil_centrado |  0.8955    |
| tamano_5pct                  |  0.1015    |
| potencia_theta0              |  0.974     |
| potencia_desplazamiento_0.2  |  0.8705    |
| se_boot_medio                |  0.106951  |
| sd_estimador                 |  0.0597647 |

IC normal con EE bootstrap: cobertura 0.8985 (tamaño 0.1015). IC percentil centrado: 0.8955.

**Veredicto: NO APTO** tamaño 0.1015 fuera de [0.04; 0.06]; cobertura 0.8985 fuera de [0.92; 0.97]
