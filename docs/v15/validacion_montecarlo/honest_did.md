# honest_did · Honest DiD (Rambachan-Roth, magnitudes relativas) en el estudio de eventos de H1

Herramienta de V15 (preregistro_v15.md sección 6: «implementación propia de V9, con tamaño del 7,3 % en 400 réplicas: se revalida o se sustituye»; adenda 1, punto 13). Código: `src/v15/montecarlo/honest_did.py`, que llama a la implementación de V9 (`honest_rr` y sus piezas, `src/v9/herramientas.py`) sin modificarla. Semilla `SeedSequence([20261010, 2, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Panel (estructura de H1, escenario S1 de sdid_placebo_h1h2):** 124 tratados y 74 donantes nunca tratados (códigos reales, centroides reales), 7 trimestres previos (2022T2-2023T4) y 9 posteriores (2024T1-2026T1), mismo proceso generador que `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). La referencia del estudio de eventos es e = −1 (2023T4).
- **Estudio de eventos estimado dentro de cada réplica:** b_e = (media de tratados − media de donantes) en e, menos la misma diferencia en e = −1; e = −7..−2 (6 previos) y 0..8 (9 posteriores). Covarianza estimada con varianzas robustas por unidad (varianza de las medias de cada grupo): el error de estimación de la covarianza entra en el tamaño.
- **Tendencias paralelas exactas (escenarios A-D):** para aislar el contraste de Honest DiD del sesgo de composición, el proceso de estos escenarios no lleva tendencias propias ni cargas heterogéneas de los factores (solo efectos de tiempo comunes, campo espacial de 25 km y AR(1) idiosincrásico heterocedástico). Los escenarios E y F usan el proceso completo de H1 (factores con cargas heterogéneas y tendencias propias d_i ~ N(0; 0,002²)), en el que las tendencias paralelas solo se cumplen en esperanza (información).
- **Sesgo de tendencias paralelas simulado:** a los tratados se les suma δ_e = s·(e + 1) en todos los trimestres (tendencia diferencial lineal; δ_{−1} = 0). Con s = 0,004 por trimestre las diferencias posteriores igualan a las previas, es decir, el caso frontera de Δ^RM(M̄ = 1).
- **Parámetro:** θ = ATT medio de los 9 trimestres posteriores (media muestral de tau_i, con tau_i = tau(1 + 0,5 z_i)).
- **Escenarios:** A (M̄ = 0, tendencias paralelas exactas), B (M̄ = 1, tendencia lineal frontera; es el umbral de C3 de H1), y de información: C (M̄ = 1, sin tendencia: el contraste es conservador por construcción), D (M̄ = 0 con tendencia: la hipótesis es falsa, mide el sobre-rechazo si se ignora el sesgo), E y F (proceso completo de H1 con M̄ = 0 y M̄ = 1).
- **Medidas:** tamaño = rechazo de θ = 0 con tau = 0; cobertura = 1 − rechazo de θ = θ_verdadero con tau = −0,05 (dualidad: θ ∈ IC si alguna pieza no rechaza θ; es el IC de V9 sin recorrer la rejilla); potencia = rechazo de θ = 0 con tau = −0,05 y con el MDE80 del pre-registro (−0,022). Sesgo y RMSE del estimador puntual (media de los 9 b_e posteriores) frente a θ.
- **Diagnóstico de la covarianza:** además del contraste con la covarianza estimada en cada réplica (la que usará H1), se repite con la covarianza verdadera (covarianza empírica de los coeficientes entre réplicas bajo el nulo, «Σ verdadera»). Si el tamaño solo falla con la estimada, el problema es la covarianza clusterizada por municipio (ignora la correlación espacial y los efectos comunes), no el contraste ARP.
- **Consistencia:** en 60 réplicas se comprueba que `honest_rr` (IC por inversión sobre rejilla, V9) contiene θ0 si y solo si el contraste por piezas no lo rechaza.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (escenarios A y B, que son los casos frontera) y cobertura en [0,92; 0,97]. El pre-registro no nombra una inferencia alternativa para Honest DiD; la adenda (punto 13) exige además una segunda implementación independiente para sostener C3 (doble implementación: fuera de este encargo).

<!-- RESULTADOS -->
## Resultados (R = 2000 en A y B; 500 en C-F; potencia con 500; semilla 20261010, k = 2)

| escenario | Mbar | pendiente | PT_exacta | rol | R_nulo | tamano_5pct | cobertura_95 | potencia_tau_-0.05 | potencia_mde_-0.022 | tamano_Sigma_verdadera | cobertura_Sigma_verdadera | sesgo | rmse |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_PT_exacta_M0 | 0.0000 | 0.0000 | True | verdad | 2000 | 0.1440 | 0.8745 | 0.9980 | 0.6460 | 0.0520 | 0.9515 | -0.0001 | 0.0118 |
| B_frontera_lineal_M1 | 1.0000 | 0.0040 | True | verdad | 2000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0202 | 0.0234 |
| C_sin_tendencia_M1 | 1.0000 | 0.0000 | True | info | 500 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | -0.0003 | 0.0123 |
| D_tendencia_con_M0 | 0.0000 | 0.0040 | True | info | 500 | 0.5900 | 0.4480 | 0.8120 | 0.1660 | 0.3920 | 0.5880 | 0.0194 | 0.0227 |
| E_factores_M0 | 0.0000 | 0.0000 | False | info | 500 | 0.2420 | 0.7740 | 0.9260 | 0.6040 | 0.0520 | 0.9520 | 0.0005 | 0.0166 |
| F_factores_M1 | 1.0000 | 0.0000 | False | info | 500 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | -0.0007 | 0.0175 |

**Consistencia** (60 réplicas, escenario B): coincidencia de `honest_rr` con el contraste por piezas = 1.000.

**Veredicto: NO APTO → criterio M̄ solo descriptivo (no sostiene C3).**

- A_PT_exacta_M0: NO APTO — tamaño 0.1440 fuera de [0.04; 0.06]; cobertura 0.8745 fuera de [0.92; 0.97] (con Σ verdadera: APTO)
- B_frontera_lineal_M1: NO APTO — tamaño 0,0 (conservador extremo); cobertura 1.0000 fuera de [0.92; 0.97] (con Σ verdadera: NO APTO)

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto: NO APTO → criterio M̄ solo descriptivo (no sostiene C3).** La implementación de V9 se revalida con R = 2.000 y con tendencias paralelas exactas en el proceso:
  - **M̄ = 0 (escenario A):** con la covarianza que usará H1 (estimada por municipio) el tamaño es 0,144 y la cobertura 0,875: **no** pasa. Con la covarianza verdadera el mismo contraste da tamaño 0,052 y cobertura 0,952: el contraste ARP condicional de V9 es correcto (el 7,3 % de V9, con 400 réplicas y covarianza conocida, es compatible con este valor dentro del error de Monte Carlo de ±1,3 pp) y el sobre-rechazo viene de la covarianza clusterizada por municipio, que ignora la correlación espacial.
  - **M̄ = 1 (escenario B, tendencia lineal frontera):** tamaño 0,000 (conservador extremo, NO APTO) y **potencia 0,000** incluso frente a un efecto de −5 %: con el ruido declarado (SE de cada coeficiente ≈ 0,012) el IC con M̄ = 1 mide ≈ ±0,2 y nunca excluye el 0. Con la covarianza verdadera ocurre lo mismo.
- **Consecuencia:** el criterio «M̄ de ruptura ≥ 1» de H1 es inalcanzable con este nivel de ruido y no puede sostener C3, aunque haya una segunda implementación (la adenda la exige además y no está disponible aquí: sin red para instalar HonestDiD). Informativo: con tendencias propias y cargas factoriales heterogéneas (E y F) el comportamiento es el mismo (tamaño 0,242 con M̄ = 0; 0,000 con M̄ = 1).
