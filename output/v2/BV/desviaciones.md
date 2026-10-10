# Desviaciones y decisiones de BV (iteración 2)

1. **Precio real.** El pre-registro dice Δ4 ln p_tasado; se usa Δ4 ln p_tasado − Δ4 ln deflactor nacional (nacional_q_v2). Al ser nacional, lo absorbe el FE de trimestre: resultados idénticos al nominal (`H2_nominal_equivalente_por_FE_trim` no es una robustez).
2. **Exposición 2005-2007.** Suma anual del importe hipotecario / población observada (1 de enero, no interpolada), media de 2005-2007, estandarizada con media y DE de las 49 provincias de entrenamiento (parámetros fijos, también para 11, 16, 45). Operacionalización única, sin búsqueda.
3. **Holm.** Dentro de la rama: Holm/BH intra-H2 con m=2 (crédito, interacción) y contraste intersección-unión (p = máx.). El Holm de la familia de 7 confirmatorias lo aplica el orquestador en BS. Los p del bootstrap iguales a 0 son p <= 1/(B+1) = 1e-4.
4. **Nivel de evidencia.** Criterio uniforme: H2 tiene evaluación sellada, luego antes del sellado el máximo es EXPLORATORIO. El fuera de muestra de entrenamiento (C3 vs AR(4)) es solo informativo; no es un criterio fijado en hipotesis.md.
5. **Modelo sellado = C3** (variables de H2), no el de menor RMSE (C1). Presupuesto de configuraciones: panel 6, nacional 4 (separado).
6. **evaluar_H2:** orígenes 2023Q3-2025Q2 (8); contraste principal con 52 provincias (49 + 3 selladas con FE propio de su historia <= 2024Q2); secundarios (a), (b), (b'), ECM v1; aborta si n_periodos < 8. Ensayo en seco con pseudo-sellado de entrenamiento: tests/test_bv_h2_sellado.py -> dryrun_h2_sellado.json.
7. **Fusión de r2/main** (fuga de población 2024Q2): solo cambia el modelo B exploratorio por periodos (demografía en P4); H2 no cambia.
