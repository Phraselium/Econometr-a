# Validación Monte Carlo V16 · tost (equivalencia, nulo informativo, adenda punto 10)

Código: `src/v16/montecarlo/tost.py` · semilla `default_rng([20261010, 8, k])`.

## Proceso generador (declarado antes de simular)
- **Estimación:** θ̂ ~ N(θ, EE²) con EE estimado con df grados de libertad (12 ≈ 13 provincias agrupadas, 37 ≈ N−1 con N = 38, e infinito = EE conocido).
- **Prueba:** TOST al 5 % (dos pruebas t unilaterales frente a ±Δ; equivale a que el IC al 90 % quede dentro de (−Δ, Δ)).
- **Tamaño:** en el borde θ = ±Δ, para Δ/EE ∈ {0,5; 1; 1,5; 2; 2,5; 3; 3,5; 4; 5; 6; 8}. Potencia en θ = 0 y θ = Δ/2.
- **Proceso del repositorio:** Δ = magnitud de referencia (`ref_pct`) y EE = MDE80/2,8 de `output/v16/potencia/potencia.csv` (15 filas con ambos); se evalúa en qué razones Δ/EE cae el repositorio.
- **R = 20.000** por celda (cálculo barato). Cobertura: no aplica.

<!-- RESULTADOS -->
## Resultados (R=20000 por celda)

|   df |   delta_sobre_EE |   tamano_borde |   tamano_borde_neg |   potencia_theta0 |   potencia_theta_mitad | apto   |
|-----:|-----------------:|---------------:|-------------------:|------------------:|-----------------------:|:-------|
|   12 |              0.5 |         0      |             0      |            0      |                 0      | False  |
|   12 |              1   |         0.0006 |             0.0008 |            0.0008 |                 0.0009 | False  |
|   12 |              1.5 |         0.0126 |             0.013  |            0.0391 |                 0.0296 | False  |
|   12 |              2   |         0.0402 |             0.0404 |            0.2314 |                 0.1522 | True   |
|   12 |              2.5 |         0.0482 |             0.0508 |            0.5282 |                 0.2861 | True   |
|   12 |              3   |         0.0464 |             0.0499 |            0.7614 |                 0.408  | True   |
|   12 |              3.5 |         0.049  |             0.0502 |            0.9031 |                 0.5002 | True   |
|   12 |              4   |         0.0516 |             0.0491 |            0.9656 |                 0.5917 | True   |
|   12 |              5   |         0.0494 |             0.0486 |            0.9976 |                 0.7582 | True   |
|   12 |              6   |         0.0463 |             0.0507 |            1      |                 0.8784 | True   |
|   12 |              8   |         0.0509 |             0.0518 |            1      |                 0.9824 | True   |
|   37 |              0.5 |         0      |             0      |            0      |                 0      | False  |
|   37 |              1   |         0      |             0      |            0      |                 0      | False  |
|   37 |              1.5 |         0.0052 |             0.0046 |            0.0154 |                 0.0116 | False  |
|   37 |              2   |         0.0406 |             0.0382 |            0.2579 |                 0.1594 | True   |
|   37 |              2.5 |         0.052  |             0.0464 |            0.581  |                 0.3166 | True   |
|   37 |              3   |         0.0505 |             0.0486 |            0.8056 |                 0.4247 | True   |
|   37 |              3.5 |         0.049  |             0.0506 |            0.9258 |                 0.5269 | True   |
|   37 |              4   |         0.047  |             0.0513 |            0.9778 |                 0.6206 | True   |
|   37 |              5   |         0.0503 |             0.0488 |            0.9984 |                 0.789  | True   |
|   37 |              6   |         0.0523 |             0.0506 |            1      |                 0.9048 | True   |
|   37 |              8   |         0.0486 |             0.0518 |            1      |                 0.9886 | True   |
|  inf |              0.5 |         0      |             0      |            0      |                 0      | False  |
|  inf |              1   |         0      |             0      |            0      |                 0      | False  |
|  inf |              1.5 |         0      |             0      |            0      |                 0      | False  |
|  inf |              2   |         0.0409 |             0.0405 |            0.2767 |                 0.1725 | True   |
|  inf |              2.5 |         0.0488 |             0.0502 |            0.6052 |                 0.3338 | True   |
|  inf |              3   |         0.0509 |             0.051  |            0.8234 |                 0.444  | True   |
|  inf |              3.5 |         0.0478 |             0.0486 |            0.9359 |                 0.5357 | True   |
|  inf |              4   |         0.0517 |             0.0505 |            0.9804 |                 0.6337 | True   |
|  inf |              5   |         0.0516 |             0.0491 |            0.9991 |                 0.8016 | True   |
|  inf |              6   |         0.051  |             0.0487 |            1      |                 0.91   | True   |
|  inf |              8   |         0.05   |             0.0478 |            1      |                 0.9898 | True   |

Razones Δ/EE del repositorio: mediana 1.04, rango [0.24; 7.30].

**Veredicto: NO APTO como regla general; APTO condicionado a Δ/EE >= umbral (en otro caso «no concluyente»)**. tamaño en el borde < 0,04 (hasta 0,0) para Δ/EE pequeña: 10 de 15 diseños del repositorio con tamaño < 0,04 (df=12); APTO solo si Δ/EE >= 2.0 (df=12), 2.0 (df=37)
