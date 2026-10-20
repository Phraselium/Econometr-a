# Driscoll-Kraay en paneles provinciales · Monte Carlo V18

**simulación; sin datos reales.** SEED 20261010.

Proceso generador: ver el docstring de src/v18/montecarlo/driscoll_kraay.py.

## Resultados

| inferencia                               |   T |   rho_f | efectos_ano   |    R |   tamano_5pct |   cobertura_95 |   potencia | veredicto   | banda_adenda_1_12           | principal   |
|:-----------------------------------------|----:|--------:|:--------------|-----:|--------------:|---------------:|-----------:|:------------|:----------------------------|:------------|
| Driscoll-Kraay (m = 2, t de T-1 gl)      |  14 |     0.5 | False         | 2000 |        0.202  |         0.798  |     0.7095 | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  14 |     0.5 | False         | 2000 |        0.2275 |         0.7725 |     0.7285 | NO APTO     | no fiable                   | True        |
| cluster por provincia (CR1, t de N-1 gl) |  14 |     0.5 | False         | 2000 |        0.48   |         0.52   |     0.8795 | NO APTO     | no fiable                   | True        |
| HC1 (normal, referencia)                 |  14 |     0.5 | False         | 2000 |        0.5325 |         0.4675 |     0.905  | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 2, t de T-1 gl)      |  20 |     0.5 | False         | 2000 |        0.1725 |         0.8275 |     0.785  | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  20 |     0.5 | False         | 2000 |        0.1845 |         0.8155 |     0.7895 | NO APTO     | no fiable                   | True        |
| cluster por provincia (CR1, t de N-1 gl) |  20 |     0.5 | False         | 2000 |        0.4965 |         0.5035 |     0.9305 | NO APTO     | no fiable                   | True        |
| HC1 (normal, referencia)                 |  20 |     0.5 | False         | 2000 |        0.553  |         0.447  |     0.95   | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  30 |     0.5 | False         | 2000 |        0.16   |         0.84   |     0.8765 | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 4, t de T-1 gl)      |  30 |     0.5 | False         | 2000 |        0.167  |         0.833  |     0.8825 | NO APTO     | no fiable                   | True        |
| cluster por provincia (CR1, t de N-1 gl) |  30 |     0.5 | False         | 2000 |        0.512  |         0.488  |     0.973  | NO APTO     | no fiable                   | True        |
| HC1 (normal, referencia)                 |  30 |     0.5 | False         | 2000 |        0.5655 |         0.4345 |     0.983  | NO APTO     | no fiable                   | True        |
| Driscoll-Kraay (m = 2, t de T-1 gl)      |  14 |     0.8 | False         | 2000 |        0.2715 |         0.7285 |     0.744  | NO APTO     | no fiable                   | False       |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  14 |     0.8 | False         | 2000 |        0.2955 |         0.7045 |     0.7595 | NO APTO     | no fiable                   | False       |
| cluster por provincia (CR1, t de N-1 gl) |  14 |     0.8 | False         | 2000 |        0.4595 |         0.5405 |     0.8615 | NO APTO     | no fiable                   | False       |
| HC1 (normal, referencia)                 |  14 |     0.8 | False         | 2000 |        0.576  |         0.424  |     0.9065 | NO APTO     | no fiable                   | False       |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  30 |     0.8 | False         | 2000 |        0.2335 |         0.7665 |     0.8225 | NO APTO     | no fiable                   | False       |
| Driscoll-Kraay (m = 4, t de T-1 gl)      |  30 |     0.8 | False         | 2000 |        0.2365 |         0.7635 |     0.8235 | NO APTO     | no fiable                   | False       |
| cluster por provincia (CR1, t de N-1 gl) |  30 |     0.8 | False         | 2000 |        0.5315 |         0.4685 |     0.9305 | NO APTO     | no fiable                   | False       |
| HC1 (normal, referencia)                 |  30 |     0.8 | False         | 2000 |        0.628  |         0.372  |     0.9595 | NO APTO     | no fiable                   | False       |
| Driscoll-Kraay (m = 2, t de T-1 gl)      |  14 |     0.5 | True          | 2000 |        0.175  |         0.825  |     0.9925 | NO APTO     | no fiable                   | False       |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  14 |     0.5 | True          | 2000 |        0.199  |         0.801  |     0.992  | NO APTO     | no fiable                   | False       |
| cluster por provincia (CR1, t de N-1 gl) |  14 |     0.5 | True          | 2000 |        0.055  |         0.945  |     0.9775 | APTO        | apta                        | False       |
| HC1 (normal, referencia)                 |  14 |     0.5 | True          | 2000 |        0.147  |         0.853  |     0.9945 | NO APTO     | con valor crítico corregido | False       |
| Driscoll-Kraay (m = 3, t de T-1 gl)      |  30 |     0.5 | True          | 2000 |        0.1255 |         0.8745 |     0.9995 | NO APTO     | con valor crítico corregido | False       |
| Driscoll-Kraay (m = 4, t de T-1 gl)      |  30 |     0.5 | True          | 2000 |        0.135  |         0.865  |     0.9995 | NO APTO     | con valor crítico corregido | False       |
| cluster por provincia (CR1, t de N-1 gl) |  30 |     0.5 | True          | 2000 |        0.053  |         0.947  |     0.999  | APTO        | apta                        | False       |
| HC1 (normal, referencia)                 |  30 |     0.5 | True          | 2000 |        0.126  |         0.874  |     1      | NO APTO     | con valor crítico corregido | False       |
| Driscoll-Kraay (m = 4, t de T-1 gl)      | 200 |     0.5 | False         | 2000 |        0.077  |         0.923  |     1      | APTO        | con valor crítico corregido | False       |
| Driscoll-Kraay (m = 6, t de T-1 gl)      | 200 |     0.5 | False         | 2000 |        0.0765 |         0.9235 |     1      | APTO        | con valor crítico corregido | False       |
| cluster por provincia (CR1, t de N-1 gl) | 200 |     0.5 | False         | 2000 |        0.5    |         0.5    |     1      | NO APTO     | no fiable                   | False       |
| HC1 (normal, referencia)                 | 200 |     0.5 | False         | 2000 |        0.5485 |         0.4515 |     1      | NO APTO     | no fiable                   | False       |

## Veredicto (escenarios principales)

- **Driscoll-Kraay (m = ancho, t de T-1 gl): NO APTO.** Aptos: ninguno. Fallan: T=14 (tamaño 0.2020, cobertura 0.7980); T=14 (tamaño 0.2275, cobertura 0.7725); T=20 (tamaño 0.1725, cobertura 0.8275); T=20 (tamaño 0.1845, cobertura 0.8155); T=30 (tamaño 0.1600, cobertura 0.8400); T=30 (tamaño 0.1670, cobertura 0.8330).
- **HC1 (normal, referencia): NO APTO.** Aptos: ninguno. Fallan: T=14 (tamaño 0.5325, cobertura 0.4675); T=20 (tamaño 0.5530, cobertura 0.4470); T=30 (tamaño 0.5655, cobertura 0.4345).
- **cluster por provincia (CR1, t de N-1 gl): NO APTO.** Aptos: ninguno. Fallan: T=14 (tamaño 0.4800, cobertura 0.5200); T=20 (tamaño 0.4965, cobertura 0.5035); T=30 (tamaño 0.5120, cobertura 0.4880).
