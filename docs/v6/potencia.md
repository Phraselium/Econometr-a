# Potencia v6 (M0): efecto mínimo detectable

Fecha del cálculo: 2026-10-11. Parte de entrenamiento únicamente (N = filas con desenlace no nulo en *_train).

Método: ρ mín. = tanh((z_{1-α/(2K)} + z_{1-β}) / √(N_eff − 3)), con α = 0,05, β = 0,20 y K = número de variables candidatas del panel (cota Bonferroni, que es el peor caso de Holm sobre K contrastes). La columna «iid» usa N; la columna «clúster» usa N_eff = N / (1 + (m − 1)·ICC), con m = N / nº de CCAA y ICC = 0,3 SUPUESTO (no estimado). Con 17 CCAA como clústeres, la inferencia clúster robusta es poco fiable: la columna clúster es orientativa.

El efecto mínimo en % se obtiene como 100·(exp(ρ·sd(ln y)) − 1): cambio de y por cada desviación típica de x.

| panel | desenlace (mercado) | nivel | K | N train | CCAA (clusters) | sd(y) | ρ mín. iid | ρ mín. clúster (ICC 0,3) | efecto mín. % por 1 DE de x (iid / clúster) |
|---|---|---|---|---|---|---|---|---|---|
| prov_compra_anual | ln_pm2_tasado (precio de compra) | provincia | 22 | 380 | 8 | 0.320 | 0.198 | 0.676 | 6.54 / 24.18 |
| prov_compra_anual | ln_cv_etdp (volumen de compra) | provincia | 22 | 410 | 11 | 1.104 | 0.191 | 0.600 | 23.43 / 94.03 |
| prov_trim_compra | ln_pm2_tasado (precio de compra) | provincia (trimestral) | 4 | 1672 | 8 | 0.329 | 0.082 | 0.599 | 2.72 / 21.72 |
| prov_trim_compra | ln_cv_etdp (volumen de compra) | provincia (trimestral) | 4 | 1672 | 8 | 1.018 | 0.082 | 0.599 | 8.66 / 83.90 |
| prov_alquiler_anual | ln_alq_m2_serpavi_vc (alquiler de stock) | provincia | 10 | 344 | 11 | 0.235 | 0.195 | 0.574 | 4.70 / 14.48 |
| prov_contratos_nuevos_anual | ln_fianza_media_gva_eur (alquiler de contratos nuevos) | provincia (solo CV) | 5 | 15 | 1 | 0.181 | 0.756 | nan | 14.64 / nan |
| mun_anual | ln_pm2_tasado_mun (precio de compra) | municipio (>25.000 hab., por nombre único) | 9 | 1909 | 10 | 0.392 | 0.083 | 0.579 | 3.29 / 25.47 |
| mun_anual | ln_alq_m2_serpavi_mun (alquiler de stock) | municipio | 9 | 16633 | 11 | 0.355 | 0.028 | 0.553 | 1.00 / 21.69 |
| dis_alquiler_anual | ln_alq_m2_serpavi_dis (alquiler de stock) | distrito (aprox. mediana p25-p75) | 2 | 27578 | 11 | 0.355 | 0.019 | 0.487 | 0.66 / 18.86 |

Lectura: ninguna especificación con N de entrenamiento inferior a ~400 puede detectar efectos pequeños con seguridad tras Holm; el panel municipal y distrital tienen más N pero menos cobertura por unidad y sesgo de muestra (solo municipios con valor tasado por nombre único y distritos con SERPAVI).
