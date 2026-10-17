# Validación Monte Carlo V16 · gsadf_factor (Q9-g, GSADF sobre el factor común)

Código: `src/v16/montecarlo/gsadf_factor.py` · semilla `default_rng([20261010, 3, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensión:** serie agregada de T = 98 trimestres; ventana mínima r0 = ⌊T(0,01 + 1,8/√T)⌋ = 18.
- **Nulo (raíz unitaria):** y_t = y_t-1 + σ_t ε_t, ε ~ N(0,1). Tres escenarios de volatilidad: homocedástico; **salto** (σ = 3 entre el 40 % y el 75 % de la muestra, 1 fuera); **estocástica** (log σ AR(1) con 0,9 y desviación 0,35).
- **Alternativa:** episodio explosivo ρ = 1,05 durante 15 trimestres (desde el 45 %) con colapso posterior, en volatilidad homocedástica y con salto.
- **Estadístico:** supremo de las t de ADF (sin rezagos, con constante) sobre todas las ventanas (inicio, fin) con longitud ≥ r0.
- **Inferencia:** bootstrap wild (Harvey et al. 2016): Δy* = Δy·w, w ~ N(0,1), raíz unitaria impuesta, B = 499; VC = cuantil 95 %. Se informa también el VC iid simulado (1.000 réplicas) para ver qué pasaría sin bootstrap.
- **Réplicas:** 2.000 bajo cada nulo, 500 bajo cada alternativa. Cobertura: no aplica.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, 500 bajo la alternativa, B=499)

| escenario   |    R |   rech_boot_wild |   rech_cv_iid_simulado |
|:------------|-----:|-----------------:|-----------------------:|
| nulo_homo   | 2000 |           0.017  |                 0.052  |
| nulo_salto  | 2000 |           0.0455 |                 0.288  |
| nulo_estoc  | 2000 |           0.0455 |                 0.3715 |
| alt_homo    |  500 |           0.064  |                 0.202  |
| alt_salto   |  500 |           0.132  |                 0.454  |

VC al 95 % iid simulado: 1.915. **Veredicto: APTO** nulo_homo: tamaño 0.0170 fuera de [0.04; 0.06]
