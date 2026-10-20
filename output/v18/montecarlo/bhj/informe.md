# BHJ a nivel de choque · Monte Carlo V18

**simulación; sin datos reales.** SEED 20261010, R = 2000 por escenario.

Proceso generador: ver el docstring de src/v18/montecarlo/bhj.py (39 provincias, K choques, HHI, cuotas incompletas, confusores sectoriales, dependencia entre provincias por 4 regiones).

## Resultados

| inferencia                |   K |   HHI |   pi |    R |   tamano_5pct |   cobertura_95 |   potencia |   F1_medio |   inv_hhi_realizado | veredicto   | banda_adenda_1_12           |
|:--------------------------|----:|------:|-----:|-----:|--------------:|---------------:|-----------:|-----------:|--------------------:|:------------|:----------------------------|
| iv_cluster (normal)       |  10 | 0.1   | 1    | 2000 |        0.1535 |         0.8465 |     0.3245 |    18.7464 |              9.6724 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  10 | 0.1   | 1    | 2000 |        0.1235 |         0.8765 |     0.2825 |    18.7464 |              9.6724 | NO APTO     | con valor crítico corregido |
| AR (ar_ic_nulo_impuesto)  |  10 | 0.1   | 1    | 2000 |        0.0065 |         0.9935 |     0.0235 |    18.7464 |              9.6724 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  10 | 0.2   | 1    | 2000 |        0.1995 |         0.8005 |     0.353  |    16.1495 |              4.9403 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  10 | 0.2   | 1    | 2000 |        0.157  |         0.843  |     0.308  |    16.1495 |              4.9403 | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  10 | 0.2   | 1    | 2000 |        0.0025 |         0.9975 |     0.01   |    16.1495 |              4.9403 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  10 | 0.3   | 1    | 2000 |        0.2375 |         0.7625 |     0.3645 |    17.0568 |              3.3171 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  10 | 0.3   | 1    | 2000 |        0.1945 |         0.8055 |     0.33   |    17.0568 |              3.3171 | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  10 | 0.3   | 1    | 2000 |        0.0015 |         0.9985 |     0.0025 |    17.0568 |              3.3171 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  20 | 0.1   | 1    | 2000 |        0.1525 |         0.8475 |     0.3545 |    15.7937 |              9.7277 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  20 | 0.1   | 1    | 2000 |        0.141  |         0.859  |     0.331  |    15.7937 |              9.7277 | NO APTO     | con valor crítico corregido |
| AR (ar_ic_nulo_impuesto)  |  20 | 0.1   | 1    | 2000 |        0.017  |         0.983  |     0.0465 |    15.7937 |              9.7277 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  20 | 0.2   | 1    | 2000 |        0.2045 |         0.7955 |     0.3425 |    17.4603 |              4.951  | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  20 | 0.2   | 1    | 2000 |        0.186  |         0.814  |     0.326  |    17.4603 |              4.951  | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  20 | 0.2   | 1    | 2000 |        0.0045 |         0.9955 |     0.0105 |    17.4603 |              4.951  | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  20 | 0.3   | 1    | 2000 |        0.2615 |         0.7385 |     0.385  |    16.9041 |              3.32   | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  20 | 0.3   | 1    | 2000 |        0.246  |         0.754  |     0.3625 |    16.9041 |              3.32   | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  20 | 0.3   | 1    | 2000 |        0.0015 |         0.9985 |     0.003  |    16.9041 |              3.32   | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  30 | 0.1   | 1    | 2000 |        0.17   |         0.83   |     0.368  |    16.0668 |              9.6904 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  30 | 0.1   | 1    | 2000 |        0.155  |         0.845  |     0.3515 |    16.0668 |              9.6904 | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  30 | 0.1   | 1    | 2000 |        0.019  |         0.981  |     0.0545 |    16.0668 |              9.6904 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  30 | 0.2   | 1    | 2000 |        0.1985 |         0.8015 |     0.3665 |    16.5198 |              4.9488 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  30 | 0.2   | 1    | 2000 |        0.1845 |         0.8155 |     0.356  |    16.5198 |              4.9488 | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  30 | 0.2   | 1    | 2000 |        0.0055 |         0.9945 |     0.0185 |    16.5198 |              4.9488 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  30 | 0.3   | 1    | 2000 |        0.235  |         0.765  |     0.3725 |    16.1619 |              3.3216 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  30 | 0.3   | 1    | 2000 |        0.222  |         0.778  |     0.358  |    16.1619 |              3.3216 | NO APTO     | no fiable                   |
| AR (ar_ic_nulo_impuesto)  |  30 | 0.3   | 1    | 2000 |        0.005  |         0.995  |     0.01   |    16.1619 |              3.3216 | NO APTO     | no fiable                   |
| iv_cluster (normal)       |  20 | 0.2   | 0.25 | 2000 |        0.1525 |         0.8475 |     0.228  |     4.3595 |              4.9372 | NO APTO     | no fiable                   |
| iv_cluster (t de Student) |  20 | 0.2   | 0.25 | 2000 |        0.1315 |         0.8685 |     0.214  |     4.3595 |              4.9372 | NO APTO     | con valor crítico corregido |
| AR (ar_ic_nulo_impuesto)  |  20 | 0.2   | 0.25 | 2000 |        0.002  |         0.998  |     0.005  |     4.3595 |              4.9372 | NO APTO     | no fiable                   |
| iv_cluster (normal)       | 200 | 0.006 | 1    | 2000 |        0.0855 |         0.9145 |     0.407  |    15.1589 |            103.431  | NO APTO     | con valor crítico corregido |
| iv_cluster (t de Student) | 200 | 0.006 | 1    | 2000 |        0.0835 |         0.9165 |     0.4055 |    15.1589 |            103.431  | NO APTO     | con valor crítico corregido |
| AR (ar_ic_nulo_impuesto)  | 200 | 0.006 | 1    | 2000 |        0.0525 |         0.9475 |     0.198  |    15.1589 |            103.431  | APTO        | apta                        |

## Veredicto

- **AR (ar_ic_nulo_impuesto): NO APTO.** Aptos: ninguno. Fallan: K=10, HHI=0.1 (tamaño 0.0065, cobertura 0.9935); K=10, HHI=0.2 (tamaño 0.0025, cobertura 0.9975); K=10, HHI=0.3 (tamaño 0.0015, cobertura 0.9985); K=20, HHI=0.1 (tamaño 0.0170, cobertura 0.9830); K=20, HHI=0.2 (tamaño 0.0045, cobertura 0.9955); K=20, HHI=0.3 (tamaño 0.0015, cobertura 0.9985); K=30, HHI=0.1 (tamaño 0.0190, cobertura 0.9810); K=30, HHI=0.2 (tamaño 0.0055, cobertura 0.9945); K=30, HHI=0.3 (tamaño 0.0050, cobertura 0.9950).
- **iv_cluster (normal): NO APTO.** Aptos: ninguno. Fallan: K=10, HHI=0.1 (tamaño 0.1535, cobertura 0.8465); K=10, HHI=0.2 (tamaño 0.1995, cobertura 0.8005); K=10, HHI=0.3 (tamaño 0.2375, cobertura 0.7625); K=20, HHI=0.1 (tamaño 0.1525, cobertura 0.8475); K=20, HHI=0.2 (tamaño 0.2045, cobertura 0.7955); K=20, HHI=0.3 (tamaño 0.2615, cobertura 0.7385); K=30, HHI=0.1 (tamaño 0.1700, cobertura 0.8300); K=30, HHI=0.2 (tamaño 0.1985, cobertura 0.8015); K=30, HHI=0.3 (tamaño 0.2350, cobertura 0.7650).
- **iv_cluster (t de Student): NO APTO.** Aptos: ninguno. Fallan: K=10, HHI=0.1 (tamaño 0.1235, cobertura 0.8765); K=10, HHI=0.2 (tamaño 0.1570, cobertura 0.8430); K=10, HHI=0.3 (tamaño 0.1945, cobertura 0.8055); K=20, HHI=0.1 (tamaño 0.1410, cobertura 0.8590); K=20, HHI=0.2 (tamaño 0.1860, cobertura 0.8140); K=20, HHI=0.3 (tamaño 0.2460, cobertura 0.7540); K=30, HHI=0.1 (tamaño 0.1550, cobertura 0.8450); K=30, HHI=0.2 (tamaño 0.1845, cobertura 0.8155); K=30, HHI=0.3 (tamaño 0.2220, cobertura 0.7780).
