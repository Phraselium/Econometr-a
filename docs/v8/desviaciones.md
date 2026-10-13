# Desviaciones y aclaraciones del pre-registro V8 (todas ANTES de cualquier estimación con datos reales)

| Fecha | § | Desviación o aclaración | Motivo |
|---|---|---|---|
| 2026-10-13 | §5 | **Ceros en la población: son 4, como en la tabla** (la población no responde en el impacto a los shocks de actividad, demanda, oferta ni crédito). Los dos shocks no identificados quedan sin restricción. El texto «a ningún shock salvo al demográfico» se refiere a los cinco identificados. | Revisión F3 (H16): con 6 ceros, el shock demográfico quedaría exactamente identificado por la fila de Σ y la identificación cambiaría materialmente. |
| 2026-10-13 | §8 | **Markov switching: el número de regímenes se elige por BIC.** El contraste bootstrap de la razón de verosimilitudes se reporta como informativo. | Monte Carlo de F3: el BIC acierta en el 80-97 % de las réplicas; el bootstrap 1 frente a 2 tiene una potencia de 0,40 y el de 2 frente a 3 no es concluyente con un B factible. |
| 2026-10-13 | §7 (H8-8) | **Número de factores comunes fijado en 1** (sensibilidad con 2), en lugar de elegirlo por el criterio de Bai-Ng. | Monte Carlo de F3: con N = 10-17, IC_p2 elige el máximo en el 100 % de las réplicas. |
| 2026-10-13 | §5 | **Prior del BVAR.** Media a priori del primer retardo propio δ = 0 para las tasas de variación y δ = 1 para el tipo en nivel. | Revisión F3 (H10): las variables de M2 son tasas trimestrales. |
| 2026-10-13 | §5 (M3) | **VAR por regímenes con los periodos pre-registrados** como fechas conocidas, en lugar de un TVP-VAR para los coeficientes. Con 4 variables (p o r, i, e, n) y p = 2, en lugar de 7, para que P4 (9 trimestres) no sea solo el prior. P4 se declara impreciso. | El TVP-VAR-SV no es apto (detección del 17 %); revisión F3 (H9). |
