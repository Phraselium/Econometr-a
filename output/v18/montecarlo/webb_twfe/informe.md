# Wild cluster bootstrap de Webb en TWFE · Monte Carlo V18

**simulación; sin datos reales.** SEED 20261010, R = 2000, B = 9999.

Proceso generador: ver el docstring de src/v18/montecarlo/webb_twfe.py.

## Resultados

| inferencia                    |   G |   T |   tratados |    R |    B |   tamano_5pct |   cobertura_95 |   potencia | veredicto   | banda_adenda_1_12           | principal   |
|:------------------------------|----:|----:|-----------:|-----:|-----:|--------------:|---------------:|-----------:|:------------|:----------------------------|:------------|
| CR1 (normal)                  |   8 |  14 |          4 | 2000 | 9999 |        0.0955 |         0.9045 |     0.332  | NO APTO     | con valor crítico corregido | True        |
| CR1 (t de Student, G-1)       |   8 |  14 |          4 | 2000 | 9999 |        0.0485 |         0.9515 |     0.231  | APTO        | apta                        | True        |
| wild cluster bootstrap (Webb) |   8 |  14 |          4 | 2000 | 9999 |        0.0595 |         0.9405 |     0.258  | APTO        | apta                        | True        |
| CR1 (normal)                  |  30 |  14 |         15 | 2000 | 9999 |        0.049  |         0.951  |     0.681  | APTO        | apta                        | True        |
| CR1 (t de Student, G-1)       |  30 |  14 |         15 | 2000 | 9999 |        0.0425 |         0.9575 |     0.658  | APTO        | apta                        | True        |
| wild cluster bootstrap (Webb) |  30 |  14 |         15 | 2000 | 9999 |        0.047  |         0.953  |     0.6585 | APTO        | apta                        | True        |
| CR1 (normal)                  |  39 |  14 |         20 | 2000 | 9999 |        0.0535 |         0.9465 |     0.766  | APTO        | apta                        | True        |
| CR1 (t de Student, G-1)       |  39 |  14 |         20 | 2000 | 9999 |        0.045  |         0.955  |     0.7475 | APTO        | apta                        | True        |
| wild cluster bootstrap (Webb) |  39 |  14 |         20 | 2000 | 9999 |        0.0465 |         0.9535 |     0.7495 | APTO        | apta                        | True        |
| CR1 (normal)                  |   8 |  14 |          1 | 2000 | 9999 |        0.4535 |         0.5465 |     0.61   | NO APTO     | no fiable                   | False       |
| CR1 (t de Student, G-1)       |   8 |  14 |          1 | 2000 | 9999 |        0.372  |         0.628  |     0.536  | NO APTO     | no fiable                   | False       |
| wild cluster bootstrap (Webb) |   8 |  14 |          1 | 2000 | 9999 |        0.004  |         0.996  |     0.004  | NO APTO     | no fiable                   | False       |
| CR1 (normal)                  |  30 |  14 |          3 | 2000 | 9999 |        0.148  |         0.852  |     0.495  | NO APTO     | con valor crítico corregido | False       |
| CR1 (t de Student, G-1)       |  30 |  14 |          3 | 2000 | 9999 |        0.136  |         0.864  |     0.4715 | NO APTO     | con valor crítico corregido | False       |
| wild cluster bootstrap (Webb) |  30 |  14 |          3 | 2000 | 9999 |        0.0075 |         0.9925 |     0.047  | NO APTO     | no fiable                   | False       |
| CR1 (normal)                  |  39 |  14 |          4 | 2000 | 9999 |        0.121  |         0.879  |     0.494  | NO APTO     | con valor crítico corregido | False       |
| CR1 (t de Student, G-1)       |  39 |  14 |          4 | 2000 | 9999 |        0.1115 |         0.8885 |     0.4785 | NO APTO     | con valor crítico corregido | False       |
| wild cluster bootstrap (Webb) |  39 |  14 |          4 | 2000 | 9999 |        0.049  |         0.951  |     0.343  | APTO        | apta                        | False       |
| CR1 (normal)                  |  39 |  30 |         20 | 2000 | 9999 |        0.0515 |         0.9485 |     0.907  | APTO        | apta                        | False       |
| CR1 (t de Student, G-1)       |  39 |  30 |         20 | 2000 | 9999 |        0.0415 |         0.9585 |     0.899  | APTO        | apta                        | False       |
| wild cluster bootstrap (Webb) |  39 |  30 |         20 | 2000 | 9999 |        0.0465 |         0.9535 |     0.902  | APTO        | apta                        | False       |

## Veredicto (escenarios principales: la mitad de los clusters tratados)

- **CR1 (normal): APTO CONDICIONADO.** Aptos: G=30, G=39. Fallan: G=8 (tamaño 0.0955, cobertura 0.9045).
- **CR1 (t de Student, G-1): APTO.** Aptos: G=8, G=30, G=39. Fallan: ninguno.
- **wild cluster bootstrap (Webb): APTO.** Aptos: G=8, G=30, G=39. Fallan: ninguno.
