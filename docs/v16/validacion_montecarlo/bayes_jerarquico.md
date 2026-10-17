# Validación Monte Carlo V16 · bayes_jerarquico (modelo normal-normal sección ⊂ municipio ⊂ provincia)

Código: `src/v16/montecarlo/bayes_jerarquico.py` · semilla `default_rng([20261010, 7, k])`.

## Proceso generador (declarado antes de simular)
- **Estructura real (solo códigos):** 8 provincias elegidas al azar entre las 41 con secciones SERPAVI de `base_alquiler` (entrenamiento), hasta 25 municipios por provincia y hasta 12 secciones por municipio, con los recuentos reales de secciones por municipio (≈ 181 municipios, ≈ 530 secciones). Los efectos y las estimaciones se simulan.
- **Modelo:** β̂_s ~ N(θ_s, se_s²), θ_s = μ + u_p + v_m + w_s; u ~ N(0, τu²), v ~ N(0, τv²), w ~ N(0, τw²); se_s = 0,06·exp(N(0; 0,5²)).
- **Priors (adenda punto 12, familia Q1):** μ ~ normal(0; 0,07); τu, τv, τw ~ semi-normal(0; 0,07). Sensibilidad con s×0,5 y s×2.
- **Verdades:** «prior» (μ y τ sorteados del propio prior, calibración bayesiana); «no nulo» (μ = −0,05; τ = 0,02/0,03/0,04); «nulo» (μ = 0); «homogéneo» (τ = 0,005, casi sin heterogeneidad).
- **Implementación (declarada):** PyMC no se usa. Muestreador Gibbs propio, con las varianzas de sección marginalizadas para (μ, u, v) y rejilla de 90 puntos (griddy Gibbs) para las tres desviaciones típicas; 1.200 iteraciones, 300 de calentamiento; μ se actualiza con u_p marginalizado (Gibbs parcialmente colapsado, orden μ → u → v → desviaciones → w), corrección hecha tras una primera pasada en que μ cubría 0,858 en el escenario «prior» por mala mezcla (documentada, no se usó).
- **Medidas:** cobertura del IC creíble al 95 % de μ, de los efectos de sección, de municipio y de provincia (criterio [0,92; 0,97]), sesgo y RMSE de μ, y P(0 fuera del IC) (tamaño/potencia informativos). R = 2.000 (nulo) y 1.000 (resto; 500 en sensibilidad: la cobertura, no el tamaño, es el criterio).

<!-- RESULTADOS -->
## Resultados

| escenario   |   escala_prior |    R |   cob_mu |   cob_seccion |   cob_municipio |   cob_provincia |   sesgo_mu |   rmse_mu |   P(0 fuera IC95 mu) |
|:------------|---------------:|-----:|---------:|--------------:|----------------:|----------------:|-----------:|----------:|---------------------:|
| prior       |            1   | 1000 |    0.94  |        0.9473 |          0.9434 |          0.9394 |    -0.0006 |    0.0238 |                0.529 |
| no_nulo     |            1   | 1000 |    0.972 |        0.9461 |          0.9386 |          0.9394 |     0.0013 |    0.008  |                0.998 |
| nulo        |            1   | 2000 |    0.952 |        0.9462 |          0.9374 |          0.9355 |    -0.0002 |    0.0081 |                0.048 |
| homogeneo   |            1   | 1000 |    0.976 |        0.9851 |          0.9661 |          0.9585 |     0.0002 |    0.0029 |                1     |
| no_nulo     |            0.5 |  500 |    0.92  |        0.9458 |          0.9388 |          0.924  |     0.0037 |    0.0086 |                1     |
| no_nulo     |            2   |  500 |    0.954 |        0.9464 |          0.9384 |          0.928  |    -0.0002 |    0.0083 |                0.998 |

**Veredicto: NO APTO** no_nulo cob_mu=0.972; homogeneo cob_mu=0.976; homogeneo cob_seccion=0.985
