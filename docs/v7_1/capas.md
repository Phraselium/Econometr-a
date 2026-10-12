# Capas de evidencia y escala de lectura

Todas las cifras y conclusiones del proyecto llevan una capa. **Nunca se promueve de capa**: la capa de un resultado es la menor de las de sus componentes.

| Capa | Nombre | Qué exige | Cómo se redacta |
|---|---|---|---|
| C1 | HECHOS | Al menos dos fuentes independientes que coinciden dentro de una tolerancia declarada (±15 % en recuentos), con todos sus componentes en C1 | «es», «fue»; se da el rango entre fuentes, no un intervalo de confianza |
| C2 | COTAS | Intervalo con supuestos explícitos (identificación parcial, Manski) o dirección que se mantiene en toda una rejilla de escenarios definida por el autor | «como máximo», «en todos los escenarios de la rejilla»; se citan los supuestos |
| C3 | EFECTOS | Efecto identificado con pretendencias, placebos, sensibilidad y evaluación en muestra sellada | lenguaje causal permitido. **Ningún resultado del proyecto ha alcanzado C3** |
| C4 | EXPLORATORIO | Asociaciones, contabilidades, proyecciones, predicción, simulaciones con parámetros supuestos, estadísticas oficiales de fuente única | «se asocia», «en la simulación», «si se aplicase…»; sin lenguaje causal |

## Escala de evidencia de los resultados estimados

CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Por debajo de CAUSAL no se usa lenguaje causal. Con capa C4, el veredicto del verificador es como máximo «ANALIZADA, NO CONCLUYENTE».

## Reglas que acompañan a las capas

- **Una sola fuente de cifras.** Toda cifra difundible sale de output/v5/cifras_clave.csv, con fecha del dato, fuentes y capa. Los entregables se generan desde plantillas con marcadores.
- **Comparaciones múltiples.** Toda especificación probada se registra, y se controla la tasa de falsos descubrimientos (Holm o BH).
- **Predicción frente a causalidad.** Un modelo solo «predice mejor» si supera a la línea base más exigente en la misma muestra. Las importancias, el SHAP y las descomposiciones no se leen como causas.
- **Simulaciones de política (R6, S1).** Son escenarios condicionales en C4. El signo de los instrumentos de oferta y de demanda lo fija en gran parte la fórmula de incidencia; lo informativo son las magnitudes relativas, con la dosis y el coste declarados.
- **Neutralidad.** Se evalúan afirmaciones e instrumentos, nunca partidos ni personas, y sin lenguaje valorativo.
