# M3: coeficientes por periodo (C4, exploratorio)

**Principal (Y6):** LP-OLS dependiente del periodo (impulso x ficticia P1-P5), EWC fixed-b, resumen = media de h=4-8. **Contraste:** VAR(2) bayesiano por regímenes, «no apto» según F3 (cobertura 0,08 en 9 trimestres): solo descriptivo (`coef_periodo_var.csv`). C4: multiplicador condicional (impulso = variable observada, no shock identificado); asociacion, sin lectura causal. LP-OLS con T~90-110: cobertura F3 0,78-0,84 incluso con EWC, bandas aproximadas. P4 (9 trimestres) impreciso. Rezagos y ficticias comunes a todos los periodos.

- Especificaciones: compra_larga, compra_epa, alquiler_epa, alquiler_pib. Pares origen→destino: 12 por especificación; 10 contrastes de periodos por par.
- Diferencias entre periodos con BH q=0,10: **60 de 480** (24 sin implicar a P4). Un no rechazo no prueba igualdad (potencia baja).
- Ancho mediano de la banda del 90 % por periodo (coeficientes h=4-8):

| espec. | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| alquiler_epa | 0.41 | 0.35 | 0.36 | 0.60 | 0.49 |
| alquiler_pib | 0.82 | 0.45 | 0.72 | 0.97 | 0.73 |
| compra_epa | 0.65 | 0.29 | 0.26 | 0.61 | 0.33 |
| compra_larga | 1.26 | 0.98 | 0.81 | 0.41 | 1.08 |

P4 (9 trimestres) se declara impreciso por diseño. Aviso: la banda de P4 NO es siempre la más ancha (p. ej. compra_larga); con 9 observaciones, regresores comunes y EWC con pocos grados de libertad, las bandas de P4 pueden ser artificialmente estrechas (sobreajuste), no más informativas. Las diferencias que implican a P4 no deben leerse como evidencia sólida. Diferencias significativas tras BH (hasta 12):

| espec. | origen→destino | periodos | dif. | p BH |
|---|---|---|---|---|
| compra_larga | i→p | P1 vs P5 | 1.22 | 0.006 |
| compra_larga | n→i | P3 vs P4 | 4.20 | 0.014 |
| compra_larga | n→i | P1 vs P4 | 6.45 | 0.019 |
| alquiler_epa | e→n | P3 vs P4 | 0.03 | 0.024 |
| alquiler_epa | n→i | P2 vs P3 | -3.60 | 0.025 |
| compra_epa | e→n | P3 vs P4 | 0.03 | 0.026 |
| compra_epa | n→i | P2 vs P3 | -3.87 | 0.026 |
| compra_epa | p→i | P1 vs P5 | 0.18 | 0.026 |
| compra_epa | n→i | P3 vs P4 | 3.86 | 0.026 |
| alquiler_pib | n→i | P2 vs P3 | -3.88 | 0.026 |
| alquiler_epa | i→e | P1 vs P2 | 1.52 | 0.026 |
| alquiler_epa | n→i | P3 vs P4 | 3.80 | 0.028 |

Todas las filas (significativas o no) están en `diferencias_periodos.csv`, `coef_periodo.csv` y `coeficientes.csv`. Los coeficientes del VAR son del retardo 1 (unidades distintas del multiplicador LP). Sin lectura causal.
