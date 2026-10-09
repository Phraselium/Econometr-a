ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Modelo de interacciones en la muestra completa (N=82): Δ4 ln p_tasado València sobre Δ4 ln comparador con pendiente e intercepto propios por tramo; EE HAC(8) (Δ4 induce MA(3) y la persistencia es mayor). Cada tramo tiene N<40 (24-32 trimestres): su cifra es descriptiva dentro de un modelo con N total >= 40. 'const' es el intercepto del tramo (pp/año). Asociación, no causa. ADVERTENCIA parte-todo: València forma parte de provincia, CV y España, lo que induce un componente mecánico de co-movimiento (sobre todo frente a la provincia).

| modelo                    | tramo         |   N_tramo |   beta |   EE_HAC |   p_beta_igual_1 |   const |   EE_const |
|:--------------------------|:--------------|----------:|-------:|---------:|-----------------:|--------:|-----------:|
| València_vs_Provincia     | 2006Q1-2013Q4 |        32 |  1.327 |  0.08891 |        0.0002313 | -0.911  |     0.5966 |
| València_vs_Provincia     | 2014Q1-2019Q4 |        24 |  2.617 |  0.2943  |        3.896e-08 | -1.584  |     0.8525 |
| València_vs_Provincia     | 2020Q1-2026Q2 |        26 |  1.016 |  0.1301  |        0.9039    |  3.316  |     0.9009 |
| València_vs_C. Valenciana | 2006Q1-2013Q4 |        32 |  1.579 |  0.1154  |        5.394e-07 |  0.6628 |     0.7338 |
| València_vs_C. Valenciana | 2014Q1-2019Q4 |        24 |  3.376 |  0.7027  |        0.0007194 | -2.071  |     0.7425 |
| València_vs_C. Valenciana | 2020Q1-2026Q2 |        26 |  1.02  |  0.1119  |        0.8567    |  4.113  |     0.7961 |
| València_vs_España        | 2006Q1-2013Q4 |        32 |  1.671 |  0.1137  |        3.608e-09 | -0.3597 |     0.8201 |
| València_vs_España        | 2014Q1-2019Q4 |        24 |  2.8   |  0.6276  |        0.004125  | -2.48   |     1.218  |
| València_vs_España        | 2020Q1-2026Q2 |        26 |  1.204 |  0.1339  |        0.1281    |  4.566  |     0.7892 |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
