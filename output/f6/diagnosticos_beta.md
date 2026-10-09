ESTIMACIÓN: N >= 40 trimestres; EE HAC Newey-West (maxlags=4) salvo indicación. Diagnósticos de los modelos beta (MCO clásico): DW, BG(4), BP, JB, RESET, CUSUM, VIF.

| modelo                         |   n |   k |    DW |     BG4_p |   BP_p |   JB_p |   RESET_p |   CUSUM_p |   VIF_max |
|:-------------------------------|----:|----:|------:|----------:|-------:|-------:|----------:|----------:|----------:|
| beta_València_vs_Provincia     |  82 |   2 | 1.179 | 2.029e-06 | 0.9086 | 0.4351 | 0.0002821 |  0.01549  |       nan |
| beta_València_vs_C. Valenciana |  82 |   2 | 1.133 | 4.848e-07 | 0.5563 | 0.5515 | 0.001377  |  0.04255  |       nan |
| beta_València_vs_España        |  82 |   2 | 1.23  | 1.896e-06 | 0.6809 | 0.4711 | 0.02196   |  0.001333 |       nan |

Fuente: elaboración propia con data/processed/valencia.csv (INE, MIVAU, GVA, SERPAVI, Notariado).
