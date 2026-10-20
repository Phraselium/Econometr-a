# V18 · Monte Carlo · Callaway-Sant'Anna con wild cluster bootstrap de Webb

**Veredicto: APTO CONDICIONADO (solo en: cat_trim_S, cat_trim_M, cat_trim_L, cat_anual, zt2024_2cohortes, pocos_tratados).** Condición en que falla: itp_8ccaa (tamaño 0.1780 fuera de [0,03; 0,08] (liberal) / cobertura 0.8220 fuera de [0,92; 0,97] (insuficiente) / cobertura 0.8290 fuera de [0,92; 0,97] (insuficiente)).

## Proceso generador (declarado antes de simular)

V18 · Procesos generadores de los diseños de diferencias en diferencias de V18 (solo estructura declarada; todo simulado).

Escenarios (dimensiones tomadas del plan de replicación; ningún dato real):
  cat_trim_S / _M / _L : Cataluña, municipio-trimestre 2019T1-2022T1 (T = 13); una cohorte que entra en 2020T4 (índice 7);
                         tratados 50 / 100 / 150 y controles 100 / 200 / 300; 42 comarcas.
  cat_anual            : Cataluña, municipio-año 2014-2021 (T = 8); cohorte 2020 (índice 6); 100 tratados, 200 controles.
  zt2024_2cohortes     : zonas tensionadas, trimestre 2022T1-2026T1 (T = 17); dos cohortes (2024T2, índice 9, 45 municipios; 2025T2,
                         índice 13, 25 municipios); 150 controles.
  pocos_tratados       : 10 tratados y 150 controles, T = 13, una cohorte en el índice 7.
  itp_8ccaa            : 36 provincias en 8 CCAA (tamaños 8, 1, 9, 5, 4, 3, 2, 4), trimestre 2010T1-2015T4 (T = 24); cohortes por CCAA
                         (3 CCAA / 15 provincias en 2012T1, índice 8; 3 CCAA / 11 provincias en 2013T1, índice 12; 2 CCAA / 10 provincias
                         sin cambio); cluster = CCAA.
Resultado simulado (log):  y_it = a_i + d_i t + Σ_k λ_ik f_kt + η_c(i),t + ε_it + efecto_it
  f_1, f_2 AR(1) (ρ_f, sd_f); λ_i1 ~ N(1; 0,4), λ_i2 ~ N(0; 0,5); η_ct AR(1) por comarca / CCAA (ρ_η, sd_η); ε_it AR(1) (ρ_ε, sd_ε
  · exp(0,3 z_i − 0,045)); d_i ~ N(0; sd_d). Las tendencias paralelas se cumplen en esperanza (la asignación no depende de λ, d ni z).
  Frecuencia trimestral: ρ_f 0,8, sd_f 0,03; ρ_η 0,6, sd_η 0,02; ρ_ε 0,5, sd_ε 0,05; sd_d 0,001.
  Frecuencia anual:      ρ_f 0,6, sd_f 0,04; ρ_η 0,4, sd_η 0,025; ρ_ε 0,4, sd_ε 0,06; sd_d 0,004.
Efecto: nulo = 0; alternativa τ (log) con heterogeneidad τ_i = τ (1 + 0,5 z'_i) y dinámica 1 − exp(−(e + 1)/2) tras la entrada.
Los valores son declarados, no estimados con datos reales.

Estimador: Callaway-Sant'Anna con nunca tratadas y periodo base g − 1; agregado «simple» (peso por tamaño de cohorte sobre las celdas t >= g). Verdad: el mismo agregado de los efectos verdaderos.
Inferencia (principal): wild cluster bootstrap-t de Webb (6 puntos, B = 999) con el NULO IMPUESTO sobre el agregado y EE de agrupación recalculado en cada réplica bootstrap (WCR-t); cluster = nivel del
tratamiento (municipio en los diseños municipales; CCAA en itp_8ccaa), como pide B2. Variantes: cluster = comarca (diseños municipales) y bootstrap sin nulo impuesto (diagnóstico de V16).
Diagnóstico (no decide el veredicto): el diseño de 8 CCAA con 4 y 5 CCAA de control y 3 y 2 tratadas. Medidas: tamaño = rechazo de θ = 0 con τ = 0; cobertura = 1 − rechazo de θ = verdad (inversión del contraste) con τ = 0,05 y bajo el nulo; potencia = rechazo de θ = 0 con τ = 0,05 (log).

## Qué falló en V16 y qué se hace distinto

V16 (cs_webb, NO APTO): tamaño 0,0655 y cobertura 0,9015 en la variante principal (41 provincias x 30 trimestres, cohortes de 1 provincia y 11 tratadas) y tamaño 0,3145 y cobertura 0,6905 en la variante
de multiplicador sobre la función de influencia SIN nulo impuesto. Causa de la variante «a»: con cohortes de una sola provincia la función de influencia centrada por cohorte es cero para la tratada, de modo
que el EE no incluía la variabilidad de las tratadas. Causa de la principal: la dependencia espacial y los factores comunes con cargas heterogéneas (los clusters provinciales no son independientes) y el
estadístico bootstrap estudentizado con el EE de la influencia no recalculado. Aquí: nulo impuesto sobre el agregado (sin imponer igualdad entre celdas), EE recalculado en cada réplica bootstrap, cobertura
por inversión del mismo contraste, y diseños con la estructura de V18 (unidad = municipio, 50-150 tratados, 100-300 controles, y el caso de 8 clusters de E8, donde se espera que falle por tener solo 2 clusters de control).

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | n_tratadas | n_controles | clusters | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | veredicto | banda_112 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cat_trim_S | webb_WCR_t_cluster_principal | 2000 | 50 | 100 | 150 | 0.0620 | 0.9380 | 0.9495 | 0.9360 | APTO | con valor crítico corregido |
| cat_trim_S | webb_WCR_t_cluster_comarca | 2000 | 50 | 100 | 150 | 0.0520 | 0.9480 | 0.9615 | 0.8770 | APTO | apta |
| cat_trim_M | webb_WCR_t_cluster_principal | 2000 | 100 | 200 | 300 | 0.0710 | 0.9290 | 0.9340 | 0.9965 | APTO | con valor crítico corregido |
| cat_trim_M | webb_WCR_t_cluster_comarca | 2000 | 100 | 200 | 300 | 0.0475 | 0.9525 | 0.9540 | 0.9910 | APTO | apta |
| cat_trim_M | webb_sin_nulo_impuesto (diagnóstico) | 2000 | 100 | 200 | 300 | 0.0720 | 0.9280 | 0.9310 | 0.9965 | APTO | con valor crítico corregido |
| cat_trim_L | webb_WCR_t_cluster_principal | 2000 | 150 | 300 | 450 | 0.0565 | 0.9435 | 0.9540 | 1.0000 | APTO | apta |
| cat_trim_L | webb_WCR_t_cluster_comarca | 2000 | 150 | 300 | 450 | 0.0545 | 0.9455 | 0.9535 | 1.0000 | APTO | apta |
| cat_anual | webb_WCR_t_cluster_principal | 2000 | 100 | 200 | 300 | 0.0600 | 0.9400 | 0.9435 | 0.7715 | APTO | apta |
| cat_anual | webb_WCR_t_cluster_comarca | 2000 | 100 | 200 | 300 | 0.0495 | 0.9505 | 0.9580 | 0.7015 | APTO | apta |
| zt2024_2cohortes | webb_WCR_t_cluster_principal | 2000 | 70 | 150 | 220 | 0.0600 | 0.9400 | 0.9565 | 0.9870 | APTO | apta |
| zt2024_2cohortes | webb_WCR_t_cluster_comarca | 2000 | 70 | 150 | 220 | 0.0535 | 0.9465 | 0.9620 | 0.9805 | APTO | apta |
| pocos_tratados | webb_WCR_t_cluster_principal | 2000 | 10 | 150 | 160 | 0.0575 | 0.9425 | 0.9465 | 0.4225 | APTO | apta |
| pocos_tratados | webb_sin_nulo_impuesto (diagnóstico) | 2000 | 10 | 150 | 160 | 0.0575 | 0.9425 | 0.9460 | 0.4300 | APTO | apta |
| itp_8ccaa | webb_WCR_t_cluster_principal | 2000 | 26 | 10 | 8 | 0.1780 | 0.8220 | 0.8290 | 0.5900 | NO APTO | no fiable |
| itp_8ccaa | webb_sin_nulo_impuesto (diagnóstico) | 2000 | 26 | 10 | 8 | 0.2000 | 0.8000 | 0.8115 | 0.5695 | NO APTO | no fiable |
| itp_8ccaa_4controles (diagnóstico) | webb_WCR_t_cluster_principal | 2000 | 20 | 16 | 8 | 0.0150 | 0.9850 | 0.9870 | 0.0905 | NO APTO | no fiable |
| itp_8ccaa_5controles (diagnóstico) | webb_WCR_t_cluster_principal | 2000 | 17 | 19 | 8 | 0.0005 | 0.9995 | 0.9995 | 0.0025 | NO APTO | no fiable |

## Notas

- Principal: cluster = nivel del tratamiento. Las variantes (comarca, sin nulo impuesto) y las filas «(diagnóstico)» no deciden el veredicto.
- B = 999 en el Monte Carlo (el plan fija 9.999 para el análisis real: el tamaño del p-valor bootstrap con 999 es el mismo salvo el error de discretización de 0,001).
- Diagnóstico puntual (R = 800, fuera de la tabla): una sola cohorte, 3 CCAA tratadas (15 provincias) y 2 de control (10), mismo proceso generador. Callaway-Sant'Anna y Sun-Abraham dan estimaciones y EE de agrupación idénticos (diferencia 1e-15), el EE medio es 0,016 frente a una desviación típica real de 0,033 (el t normal rechaza el 40,6 %), y el bootstrap de Webb con nulo impuesto rechaza el 0,5 % con la construcción de CS y el 7,9 % con la de SA: con 5 clusters el tamaño depende de cómo se construyan los residuos del bootstrap, no solo del estimador. La forma cerrada de CS está verificada contra un remuestreo ingenuo (tests/v18/test_herramientas_did_bootstrap_ingenuo.py). Con 8 clusters no hay veredicto fiable en ninguna de las dos: SA da 0,0685 con 2 CCAA de control pero 0,0805 y 0,0920 con 4 y 5; CS da 0,178, 0,015 y 0,0005.
