ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Regresión Δ4 ln p_tasado València (100·) sobre Δ4 ln del comparador, N=82. EE HAC Newey-West con maxlags=4 (principal) y 6 (robustez; Δ4 induce MA(3)). p_beta_igual_1 contrasta H0: β=1. Asociación contemporánea, no efecto causal.

| modelo                         |   maxlags |   N |   beta |   EE_HAC |   IC95_inf |   IC95_sup |   p_beta0 |   p_beta_igual_1 |   R2_aj |    const |
|:-------------------------------|----------:|----:|-------:|---------:|-----------:|-----------:|----------:|-----------------:|--------:|---------:|
| beta_València_vs_Provincia     |         4 |  82 |  1.395 |  0.09436 |      1.21  |      1.58  | 1.911e-49 |        2.861e-05 |  0.8313 | -0.09051 |
| beta_València_vs_Provincia     |         6 |  82 |  1.395 |  0.09221 |      1.214 |      1.576 | 1.087e-51 |        1.855e-05 |  0.8313 | -0.09051 |
| beta_València_vs_C. Valenciana |         4 |  82 |  1.515 |  0.1019  |      1.315 |      1.715 | 5.644e-50 |        4.367e-07 |  0.8095 |  0.539   |
| beta_València_vs_C. Valenciana |         6 |  82 |  1.515 |  0.0996  |      1.32  |      1.71  | 3.037e-52 |        2.343e-07 |  0.8095 |  0.539   |
| beta_València_vs_España        |         4 |  82 |  1.729 |  0.1054  |      1.522 |      1.935 | 1.913e-60 |        4.712e-12 |  0.7868 |  0.292   |
| beta_València_vs_España        |         6 |  82 |  1.729 |  0.1027  |      1.528 |      1.93  | 1.353e-63 |        1.271e-12 |  0.7868 |  0.292   |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
