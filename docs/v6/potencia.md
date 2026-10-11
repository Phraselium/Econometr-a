# Potencia v6 (M0): efecto mínimo detectable — rehecha tras la revisión

Fecha del cálculo: 2026-10-11. Solo parte de entrenamiento (N = filas con desenlace no nulo).

Especificación: FE de unidad y de año; regresores preregistrados en docs/v6/hipotesis.md §2 (t−1); K = regresores preregistrados + desenlace. ρ mín. = tanh((z_{1−α/(2K)} + z_{1−β}) / √(N_eff − 3)), α = 0,05, β = 0,20 (Bonferroni sobre K, cota superior de Holm). Columna «iid»: N_eff = N. Columna «clúster»: N_eff = N / (1 + (m − 1)·ICC), m = N / nº de CCAA, ICC = 0,3 SUPUESTO. Con 8-11 CCAA la inferencia clúster no es fiable: la inferencia final usará wild cluster bootstrap (Webb), pre-registrado en hipotesis.md.

La sd es WITHIN (desviación típica de y tras quitar media de unidad y de año). Efecto en % = 100·(exp(ρ·sd_within) − 1) por cada desviación típica within de x.

| panel | desenlace (mercado) | nivel | K | N train | CCAA | sd within | ρ mín. iid | ρ mín. clúster (ICC 0,3) | efecto mín. % por 1 DE within (iid / clúster) |
|---|---|---|---|---|---|---|---|---|---|
| prov_compra_anual | ln_pm2_tasado (precio de compra) | provincia | 11 | 410 | 11 | 0.043 | 0.180 | 0.575 | 0.78 / 2.50 |
| prov_compra_anual | ln_cv_etdp (volumen de compra) | provincia | 11 | 410 | 11 | 0.085 | 0.180 | 0.575 | 1.55 / 5.02 |
| prov_alquiler_anual | ln_alq_m2_serpavi_vc (alquiler de stock) | provincia | 4 | 344 | 11 | 0.022 | 0.179 | 0.536 | 0.39 / 1.17 |
| mun_compra_anual | ln_pm2_tasado_mun (precio de compra) | municipio | 1 | 1909 | 10 | 0.063 | 0.064 | 0.472 | 0.41 / 3.04 |
| mun_alquiler_anual | ln_alq_m2_serpavi_mun (alquiler de stock) | municipio | 1 | 14656 | 11 | 0.062 | 0.023 | 0.449 | 0.14 / 2.80 |
| dis_alquiler_anual | ln_alq_m2_serpavi_dis (alquiler de stock) | distrito (punto medio p25-p75) | 2 | 27578 | 11 | 0.071 | 0.019 | 0.487 | 0.13 / 3.53 |

Lectura: con N de entrenamiento de 150-400 la potencia es baja: solo se detectan efectos grandes con seguridad tras Holm. El contraste trimestral no tiene potencia propia: repite las mismas unidades que el anual (1.672 filas sin independencia adicional). Contratos nuevos (N ≈ 15 filas en 3-4 provincias) no tiene potencia y queda como descriptivo.
