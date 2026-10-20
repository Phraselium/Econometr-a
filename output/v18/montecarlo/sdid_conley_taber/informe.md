# V18 · Monte Carlo · SDID y Conley-Taber con pocos tratados

**Veredicto: APTO.**

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real). E2-A1 (zonas tensionadas de 2024 en Cataluña, Incasòl 2022T1-2026T1): T = 17 trimestres, entrada en el índice 9 (2024T2): 9 previos y 8 posteriores;
tratados 2, 5, 10 y 25 municipios y 200 controles (42 comarcas). E2-A2 (País Vasco, EMAL 2016T1-2025T4): T = 40, 3 posteriores (índice 37), 8 tratados y 150 controles.
Resultado: el de _dgp_did.py con la frecuencia trimestral (factores comunes AR(1) ρ 0,8 sd 0,03 con cargas N(1; 0,4) y N(0; 0,5), choque de comarca AR(1) ρ 0,6 sd 0,02, ruido AR(1) ρ 0,5
sd 0,05·exp(0,3 z_i − 0,045), tendencias propias d_i ~ N(0; 0,001)); efecto τ_i = τ(1 + 0,5 z'_i) con rampa 1 − exp(−(e + 1)/2). Los tratados se concentran en las 12 primeras comarcas (los
controles se reparten por todas): la asignación no depende de las cargas, de las tendencias ni de la varianza (intercambiabilidad ex ante necesaria para los placebos).
Estimador: SDID (Arkhangelsky et al. 2021): ω de unidad con intercepto y regularización ζ = (N_tr T_post)^(1/4) σ̂, λ de tiempo con regularización mínima, FISTA (80 y 60 iteraciones).
Inferencia: (1) Conley-Taber: 199 placebos que toman n_tr controles al azar como tratados y reestiman ω con los donantes restantes; p-valor simétrico P(|ĉ| >= |τ̂ − θ0|) (principal);
(2) SE de placebos con normal (Arkhangelsky); (3) Conley-Taber sobre el DiD simple (pesos uniformes; referencia). Diagnóstico de intercambiabilidad: tratados con variabilidad temporal 0,5 y 2 veces la de los controles. Medidas: tamaño = rechazo de θ = 0 con τ = 0; cobertura = 1 − rechazo de
θ = verdad (media de τ_i de los tratados en los periodos posteriores) con τ = −0,05 (inversión del contraste) y bajo el nulo; potencia = rechazo de θ = 0 con τ = −0,05.
Aproximación declarada: los pesos de tiempo λ no se reestiman en los placebos.

## Qué falló en V16 y qué se hace distinto

V16 (sdid_conley_taber): Conley-Taber APTO solo en el escenario A (2 tratados, 1 provincia): tamaño 0,0575 y cobertura 0,943; la réplica B del mismo diseño dio 0,0650 y 0,9290, y agrupando
4.000 réplicas el tamaño fue 0,0612: «en el límite», no holgado. El Webb de la alternativa degeneraba (tamaño 0,78 con un cluster tratado). Aquí se mide el barrido de n_tr = 2, 5, 10, 25 (el
criterio no se aplica a un solo tamaño) y el diseño de País Vasco (T = 40, 3 posteriores), con R = 2.000 y 199 placebos por réplica. No se usa Webb (con pocos tratados no es una opción).

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | sesgo | rmse | veredicto | banda_112 |
|---|---|---|---|---|---|---|---|---|---|---|
| tratados_02 | conley_taber_sdid | 2000 | 0.0445 | 0.9555 | 0.9560 | 0.2595 | 0.0004 | 0.0311 | APTO | apta |
| tratados_02 | sdid_placebo_normal | 2000 | 0.0480 | 0.9520 | 0.9550 | 0.2690 | 0.0004 | 0.0311 | APTO | apta |
| tratados_02 | conley_taber_did_simple (referencia) | 2000 | 0.0520 | 0.9480 | 0.9575 | 0.2535 | 0.0004 | 0.0311 | APTO | apta |
| tratados_05 | conley_taber_sdid | 2000 | 0.0525 | 0.9475 | 0.9560 | 0.5305 | -0.0006 | 0.0200 | APTO | apta |
| tratados_05 | sdid_placebo_normal | 2000 | 0.0555 | 0.9445 | 0.9525 | 0.5365 | -0.0006 | 0.0200 | APTO | apta |
| tratados_05 | conley_taber_did_simple (referencia) | 2000 | 0.0600 | 0.9400 | 0.9415 | 0.5160 | -0.0006 | 0.0200 | APTO | apta |
| tratados_10 | conley_taber_sdid | 2000 | 0.0555 | 0.9445 | 0.9540 | 0.8070 | 0.0003 | 0.0147 | APTO | apta |
| tratados_10 | sdid_placebo_normal | 2000 | 0.0580 | 0.9420 | 0.9480 | 0.8100 | 0.0003 | 0.0147 | APTO | apta |
| tratados_10 | conley_taber_did_simple (referencia) | 2000 | 0.0605 | 0.9395 | 0.9485 | 0.7885 | 0.0003 | 0.0147 | APTO | con valor crítico corregido |
| tratados_25 | conley_taber_sdid | 2000 | 0.0535 | 0.9465 | 0.9430 | 0.9875 | 0.0001 | 0.0094 | APTO | apta |
| tratados_25 | sdid_placebo_normal | 2000 | 0.0530 | 0.9470 | 0.9430 | 0.9865 | 0.0001 | 0.0094 | APTO | apta |
| tratados_25 | conley_taber_did_simple (referencia) | 2000 | 0.0585 | 0.9415 | 0.9445 | 0.9800 | 0.0001 | 0.0094 | APTO | apta |
| pais_vasco_A2 | conley_taber_sdid | 2000 | 0.0560 | 0.9440 | 0.9370 | 0.4265 | 0.0003 | 0.0174 | APTO | apta |
| pais_vasco_A2 | sdid_placebo_normal | 2000 | 0.0570 | 0.9430 | 0.9355 | 0.4345 | 0.0003 | 0.0174 | APTO | apta |
| pais_vasco_A2 | conley_taber_did_simple (referencia) | 2000 | 0.0630 | 0.9370 | 0.9320 | 0.3885 | 0.0003 | 0.0174 | APTO | con valor crítico corregido |
| tratados_10_variabilidad_x0.5 (diagnóstico) | conley_taber_sdid | 2000 | 0.0330 | 0.9670 | 0.9715 | 0.8090 | 0.0001 | 0.0138 | NO APTO | con valor crítico corregido |
| tratados_10_variabilidad_x0.5 (diagnóstico) | sdid_placebo_normal | 2000 | 0.0320 | 0.9680 | 0.9675 | 0.8180 | 0.0001 | 0.0138 | APTO | con valor crítico corregido |
| tratados_10_variabilidad_x0.5 (diagnóstico) | conley_taber_did_simple (referencia) | 2000 | 0.0610 | 0.9390 | 0.9385 | 0.7925 | 0.0001 | 0.0138 | APTO | con valor crítico corregido |
| tratados_10_variabilidad_x2 (diagnóstico) | conley_taber_sdid | 2000 | 0.4435 | 0.5565 | 0.5430 | 0.6655 | 0.0000 | 0.0367 | NO APTO | no fiable |
| tratados_10_variabilidad_x2 (diagnóstico) | sdid_placebo_normal | 2000 | 0.4470 | 0.5530 | 0.5425 | 0.6660 | 0.0000 | 0.0367 | NO APTO | no fiable |
| tratados_10_variabilidad_x2 (diagnóstico) | conley_taber_did_simple (referencia) | 2000 | 0.4820 | 0.5180 | 0.5160 | 0.6580 | 0.0000 | 0.0367 | NO APTO | no fiable |

## Notas

- Principal: Conley-Taber sobre SDID. SDID con normal de placebos y Conley-Taber sobre DiD simple son referencia. Las filas «(diagnóstico)» rompen a propósito la intercambiabilidad entre tratados y controles (no deciden el veredicto): muestran la condición en que los placebos dejan de valer.
- R = 2000 réplicas por escenario y por bloque; 199 placebos por réplica (p-valor mínimo 0,005).
