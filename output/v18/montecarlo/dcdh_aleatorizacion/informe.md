# V18 · Monte Carlo · de Chaisemartin-D'Haultfœuille con aleatorización del calendario (8 CCAA)

**Veredicto: APTO.**

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real): panel provincial trimestral 2010T1-2015T4 (T = 24) con 36 provincias en 8 CCAA de régimen común
(tamaños 8, 1, 9, 5, 4, 3, 2, 4); dosis = tipo general del ITP por CCAA; 6 CCAA cambian 1 o 2 veces (85 % de los cambios en 2012T1-2013T4,
índices 8-15; tamaño +1, +2, −1, −2 puntos con prob. 0,4/0,3/0,2/0,1) y 2 CCAA (10 provincias) no cambian. El calendario se redibuja en cada réplica.
Resultado (log): y_it = a_i + d_i t + Σ_k λ_ik f_kt + η_c(i),t + ε_it + β_i D_it. Factores comunes AR(1) ρ 0,8 sd 0,03; choque CCAA-trimestre AR(1)
ρ 0,6 sd 0,02·exp(0,3 z_c − 0,045) (heterocedasticidad entre CCAA, escenario «desigual»); ε_it AR(1) ρ 0,5 sd 0,05·exp(0,3 z_i − 0,045); d_i ~ N(0; 0,001);
β_i = β (1 + 0,5 z'_i), efecto de nivel de la dosis. Nulo β = 0; alternativa β = −0,03 por punto (precio, referencia Dolls et al.).
Pocos clusters: 8 (cluster = CCAA). Escenarios: «desigual» (tamaños y varianzas desiguales) y «equilibrado» (4-5 provincias por CCAA, sin heterocedasticidad; diagnóstico).
Estimador: DID_ℓ de dCDH con ℓ = 4 (efecto a 4 trimestres, E8-R1; principal) y ℓ = 0 (contemporáneo, como V16; información). Cambiantes: ΔD ≠ 0 sin otro
cambio en (t, t+ℓ]; controles: sin cambio en [t, t+ℓ]; β̂ = Σ sign(ΔD)(ΔY − m_t) / Σ |ΔD|. Verdad: media de β_i ponderada por |ΔD| en las celdas cambiantes.
Inferencia: (1) aleatorización del calendario entre las 8 CCAA, estadístico ESTUDENTIZADO |β̂/EE| (nueva; principal), 499 permutaciones aleatorias + identidad;
(2) aleatorización con el coeficiente |β̂| (la de V16); (3) bootstrap-t de Webb por CCAA con nulo impuesto, 999; (4) t de Student (G−1 = 7 gl) con EE de agrupación.
Cobertura = 1 − tasa de rechazo del contraste de θ = verdad (inversión del contraste; efecto constante impuesto en el contraste de aleatorización).

## Qué falló en V16 y qué se hace distinto

V16 (src/v16/montecarlo/dcdh_aleatorizacion.py): tamaño 0,0775 y cobertura 0,967 con 11 clusters, estadístico sin estudentizar y 499 permutaciones. Hipótesis de V16: heterogeneidad de tamaño y de varianza entre
clusters (los calendarios permutados no serían intercambiables para el coeficiente). Este Monte Carlo NO la confirma con la estructura de V18 (8 CCAA, dosis de nivel, calendarios concentrados en 2012-2013): el
estadístico sin estudentizar da un tamaño de 0,04-0,06 y el estudentizado también, en el escenario desigual y en el equilibrado, de modo que el 0,0775 de V16 no se reproduce y su causa (11 clusters, 41 provincias,
DID_M contemporáneo, correlación espacial entre provincias) no queda identificada aquí. Se mantiene la estudentización como principal (es la razón de intercambiabilidad más robusta a priori) y se mide la
cobertura invirtiendo el contraste. Lo que sí falla, y de forma clara, es el bootstrap de Webb con 8 clusters (tamaño 0,12-0,15), como cabía esperar con menos de 10 clusters. No se repite el diseño de V16
con un criterio más laxo: el criterio es el del encargo y se reporta junto a las bandas de la adenda 1.12.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | sesgo | rmse | veredicto | banda_112 |
|---|---|---|---|---|---|---|---|---|---|---|
| itp_desigual_ell4 | aleatorizacion_estudentizada | 2000 | 0.0455 | 0.9545 | 0.9535 | 0.3745 | -0.0001 | 0.0159 | APTO | apta |
| itp_desigual_ell4 | aleatorizacion_coeficiente (V16) | 2000 | 0.0415 | 0.9585 | 0.9620 | 0.3295 | -0.0001 | 0.0159 | APTO | apta |
| itp_desigual_ell4 | webb_8_clusters | 2000 | 0.1485 | 0.8515 | 0.8545 | 0.6210 | -0.0001 | 0.0159 | NO APTO | con valor crítico corregido |
| itp_desigual_ell4 | t_cluster_7gl | 2000 | 0.0655 | 0.9345 | 0.9370 | 0.4505 | -0.0001 | 0.0159 | APTO | con valor crítico corregido |
| itp_equilibrado_ell4 | aleatorizacion_estudentizada | 2000 | 0.0535 | 0.9465 | 0.9495 | 0.4390 | 0.0006 | 0.0145 | APTO | apta |
| itp_equilibrado_ell4 | aleatorizacion_coeficiente (V16) | 2000 | 0.0520 | 0.9480 | 0.9480 | 0.4390 | 0.0006 | 0.0145 | APTO | apta |
| itp_equilibrado_ell4 | webb_8_clusters | 2000 | 0.1200 | 0.8800 | 0.8870 | 0.6405 | 0.0006 | 0.0145 | NO APTO | con valor crítico corregido |
| itp_equilibrado_ell4 | t_cluster_7gl | 2000 | 0.0610 | 0.9390 | 0.9405 | 0.4670 | 0.0006 | 0.0145 | APTO | con valor crítico corregido |
| itp_desigual_ell0 | aleatorizacion_estudentizada | 2000 | 0.0480 | 0.9520 | 0.9580 | 0.7045 | 0.0005 | 0.0092 | APTO | apta |
| itp_desigual_ell0 | aleatorizacion_coeficiente (V16) | 2000 | 0.0415 | 0.9585 | 0.9600 | 0.8235 | 0.0005 | 0.0092 | APTO | apta |
| itp_desigual_ell0 | webb_8_clusters | 2000 | 0.1430 | 0.8570 | 0.8680 | 0.8920 | 0.0005 | 0.0092 | NO APTO | con valor crítico corregido |
| itp_desigual_ell0 | t_cluster_7gl | 2000 | 0.0710 | 0.9290 | 0.9365 | 0.8015 | 0.0005 | 0.0092 | APTO | con valor crítico corregido |
| itp_equilibrado_ell0 | aleatorizacion_estudentizada | 2000 | 0.0535 | 0.9465 | 0.9570 | 0.7715 | -0.0001 | 0.0089 | APTO | apta |
| itp_equilibrado_ell0 | aleatorizacion_coeficiente (V16) | 2000 | 0.0565 | 0.9435 | 0.9455 | 0.8855 | -0.0001 | 0.0089 | APTO | apta |
| itp_equilibrado_ell0 | webb_8_clusters | 2000 | 0.1180 | 0.8820 | 0.8955 | 0.9180 | -0.0001 | 0.0089 | NO APTO | con valor crítico corregido |
| itp_equilibrado_ell0 | t_cluster_7gl | 2000 | 0.0610 | 0.9390 | 0.9475 | 0.8255 | -0.0001 | 0.0089 | APTO | con valor crítico corregido |

## Notas

- Principal: aleatorización estudentizada, escenario «desigual», ℓ = 4. Las demás filas son diagnóstico.
- R = 2000 réplicas por escenario y por bloque (nulo y alternativa); permutaciones por réplica: 499.
