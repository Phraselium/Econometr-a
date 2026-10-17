# Validación Monte Carlo V16 · cips_bootstrap (Q9, CIPS con bootstrap de bloques)

Código: `src/v16/montecarlo/cips_bootstrap.py` · semilla `default_rng([20261010, 1, k])` · salidas en `output/v16/montecarlo/cips_bootstrap/`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** N = 38 unidades (provincias de entrenamiento), T = 95 trimestres (2002T1-2026T2). Ningún valor real.
- **Dependencia transversal:** factor común f_t AR(1) con ρ = 0,5 y cargas γ_i ~ N(1; 0,5²); correlación espacial en anillo (peso 0,25 con los dos vecinos).
- **Autocorrelación y heterogeneidad:** errores AR(1) con ρ_i ~ U(0; 0,4) (valor declarado, no calibrado con datos), σ_i ~ U(0,5; 1,5).
- **Nulo:** y_it = y_i,t-1 + γ_i f_t + e_it (raíz unitaria en todas las unidades). **Alternativa:** φ_i ~ U(0,85; 0,95), constante μ_i, factor estacionario.
- **Estadístico:** CIPS = media de las t de CADF(1) con constante (medias transversales y rezago 1).
- **Inferencia:** bootstrap de bloques móviles (longitud 2·T^(1/3) ≈ 9) sobre las primeras diferencias de todas las unidades a la vez (conserva el factor común), sin deriva, B = 399 (por defecto) y valor crítico = cuantil 5 % del CIPS*. Se compara con el VC asintótico aproximado de Pesaran (2007), −2,11.
- **Réplicas:** 2.000 bajo el nulo, 500 bajo la alternativa. Cobertura: no definida para una prueba; el veredicto usa el tamaño.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, R=500 bajo la alternativa, B=399, bloque=9)

| escenario   |    R |   rech_boot |   rech_pvalor |   rech_asint |   media_cips |   cv_boot_media |
|:------------|-----:|------------:|--------------:|-------------:|-------------:|----------------:|
| nulo        | 2000 |       0.006 |        0.0055 |       0.0925 |     -1.7888  |        -2.35664 |
| alternativa |  500 |       0.868 |        0.856  |       1      |     -2.63409 |        -2.47712 |

Tamaño con bootstrap: 0.0060 (IC binomial [0.0026, 0.0094]); con CV asintótico -2,11: 0.0925. Potencia (φ_i en U(0,85; 0,95)): 0.8680.

**Veredicto: NO APTO** tamaño 0.0060 fuera de [0.04; 0.06]

Diagnóstico exploratorio (R=120, B=149, src/v16/montecarlo/cips_bootstrap_diagnostico.py; no es parte del veredicto): bloques de 9, 20 y 40 dan tamaño 0,0 en los tres casos (sobrecorrección: VC demasiado negativo); un bootstrap sieve AR(1) con remuestreo conjunto de residuos da 0,075 (ruido ±0,05); VC asintótico -2,11: 0,092.
