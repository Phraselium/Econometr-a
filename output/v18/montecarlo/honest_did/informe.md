# V18 · Monte Carlo · Honest DiD (Rambachan-Roth, magnitudes relativas)

**Veredicto: APTO CONDICIONADO (solo en: cat_S_M0_PTexacta, cat_L_M0_PTexacta).** Condición en que falla: cat_M_M0_PTexacta (tamaño 0.0820 fuera de [0,03; 0,08] (liberal) / cobertura 0.9180 fuera de [0,92; 0,97] (insuficiente)); cat_M_M05_frontera (tamaño 0.0000 fuera de [0,03; 0,08] (conservador) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora)); cat_M_M1_frontera (tamaño 0.0000 fuera de [0,03; 0,08] (conservador) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora)); cat_S_M1_frontera (tamaño 0.0000 fuera de [0,03; 0,08] (conservador) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora)); cat_L_M1_frontera (tamaño 0.0000 fuera de [0,03; 0,08] (conservador) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora) / cobertura 1.0000 fuera de [0,92; 0,97] (conservadora)).

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real). Cataluña municipio-trimestre, 2019T1-2022T1 (T = 13): ref = 2020T2 (índice 5), previos = índices 0-4 (5 coeficientes),
posteriores = índices 6-12 (7 coeficientes; el efecto empieza en el índice 7 = 2020T4 y el 6 = 2020T3 es el trimestre parcial); tratados 50/100/150 y controles 100/200/300
(S/M/L); 42 comarcas. ITP (E8): 36 provincias en 8 CCAA, una cohorte de 15 provincias (3 CCAA, índice 8), 21 controles, cluster = CCAA, ref = índice 7, 6 previos, 7 posteriores.
Resultado: el de _dgp_did.py (factores comunes con cargas heterogéneas AR(1), choque de comarca/CCAA, ruido AR(1) heterocedástico, tendencias propias d_i ~ N(0; 0,001);
efecto τ_i = τ(1 + 0,5 z_i) con rampa 1 − exp(−(e+1)/2)). Las tendencias paralelas se cumplen en esperanza.
Sesgo de tendencias diferencial (solo tratados): δ_t = s·(t − ref) para t <= ref y δ_t = m·s·(t − ref) para t > ref, con s = 0,004 por trimestre. El valor m es el de la
frontera de Δ^RM(M̄ = m): la pendiente posterior iguala m veces la previa (M̄ = 1: igual; M̄ = 0,5: la mitad; M̄ = 0: sin sesgo posterior).
Estimación dentro de cada réplica: estudio de eventos b_t = media tratados − media controles de (Y_t − Y_ref), covarianza AGRUPADA estimada (cluster = municipio, que es el nivel del
tratamiento en E2, o CCAA en E8) con factor G/(G − 1); contraste condicional ARP por piezas (src/v9) para θ = media de los 7 coeficientes posteriores.
Medidas: tamaño = rechazo de θ = 0 con τ = 0 (al borde de Δ^RM(M̄)); cobertura = 1 − rechazo de θ = θ verdadero (media de los efectos τ_i de los 7 posteriores) con τ = −0,05
(inversión del contraste) y bajo el nulo (θ = 0); potencia = rechazo de θ = 0 con τ = −0,05. Variantes de covarianza: (a) cluster del tratamiento (principal); (b) cluster = comarca
(solo en diseños municipales); (c) (a) con factor de Hotelling (G−1)/(G−k) sobre la covarianza (k coeficientes) cuando G > k + 1.
Verdad con covarianza conocida (diagnóstico): covarianza empírica de los coeficientes entre réplicas bajo el nulo.

## Qué falló en V16 y qué se hace distinto

V15 (honest_did, NO APTO): tamaño 0,144 con M̄ = 0 y covarianza estimada por unidad (0,052 con la covarianza verdadera: el fallo no era el contraste ARP sino la covarianza),
cobertura 0,8745 en el caso frontera y tamaño 0,0 (conservador extremo) en el caso M̄ = 1 sin tendencia. V9 tuvo 7,3 % en 400 réplicas. Aquí: (1) la covarianza se agrupa por cluster del tratamiento
y se compara con la comarcal y con una versión con corrección de grados de libertad; (2) el criterio se aplica a los casos frontera de Δ^RM (M̄ = 0 con paralelismo exacto, M̄ = 0,5 y M̄ = 1 con la
pendiente posterior igual a m veces la previa); el caso M̄ = 1 sin tendencia es información (conservador por construcción: el contraste admite un sesgo que no existe); (3) se mide en tres tamaños
(50/100/150 tratados) y en el diseño de 8 CCAA, donde la covarianza agrupada tiene rango <= 7 y se espera que el método no sea válido.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | variante | R | tamano_5pct | cobertura_nulo | cobertura_alt | potencia | veredicto | banda_112 | Mbar | rango_V_medio |
|---|---|---|---|---|---|---|---|---|---|---|
| cat_M_M0_PTexacta | cluster_tratamiento | 2000 | 0.0820 | 0.9180 | 0.9370 | 0.9885 | NO APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_M_M0_PTexacta | cluster_comarca | 2000 | 0.0740 | 0.9260 | 0.9425 | 0.9765 | APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_M_M0_PTexacta | cluster_tratamiento + Hotelling | 2000 | 0.0770 | 0.9230 | 0.9410 | 0.9875 | APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_M_M05_frontera | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0010 | NO APTO | no fiable | 0.5000 | 12.0000 |
| cat_M_M05_frontera | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0005 | NO APTO | no fiable | 0.5000 | 12.0000 |
| cat_M_M05_frontera | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0010 | NO APTO | no fiable | 0.5000 | 12.0000 |
| cat_M_M1_frontera | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_M_M1_frontera | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_M_M1_frontera | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_S_M0_PTexacta | cluster_tratamiento | 2000 | 0.0655 | 0.9345 | 0.9440 | 0.8465 | APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_S_M0_PTexacta | cluster_comarca | 2000 | 0.0845 | 0.9155 | 0.9245 | 0.8390 | NO APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_S_M0_PTexacta | cluster_tratamiento + Hotelling | 2000 | 0.0595 | 0.9405 | 0.9530 | 0.8300 | APTO | apta | 0.0000 | 12.0000 |
| cat_S_M1_frontera | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_S_M1_frontera | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_S_M1_frontera | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_L_M0_PTexacta | cluster_tratamiento | 2000 | 0.0545 | 0.9455 | 0.9575 | 0.9995 | APTO | apta | 0.0000 | 12.0000 |
| cat_L_M0_PTexacta | cluster_comarca | 2000 | 0.0640 | 0.9360 | 0.9460 | 0.9990 | APTO | con valor crítico corregido | 0.0000 | 12.0000 |
| cat_L_M0_PTexacta | cluster_tratamiento + Hotelling | 2000 | 0.0525 | 0.9475 | 0.9610 | 0.9995 | APTO | apta | 0.0000 | 12.0000 |
| cat_L_M1_frontera | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_L_M1_frontera | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_L_M1_frontera | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_M_M1_sin_tendencia (info) | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_M_M1_sin_tendencia (info) | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| cat_M_M1_sin_tendencia (info) | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 12.0000 |
| itp_8ccaa_M0 (info) | cluster_tratamiento | 2000 | 0.1745 | 0.8255 | 0.8275 | 0.5060 | NO APTO | no fiable | 0.0000 | 6.0000 |
| itp_8ccaa_M0 (info) | cluster_comarca | 2000 | 0.1745 | 0.8255 | 0.8275 | 0.5060 | NO APTO | no fiable | 0.0000 | 6.0000 |
| itp_8ccaa_M0 (info) | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 0.0000 | 6.0000 |
| itp_8ccaa_M1_frontera (info) | cluster_tratamiento | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 6.0000 |
| itp_8ccaa_M1_frontera (info) | cluster_comarca | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 6.0000 |
| itp_8ccaa_M1_frontera (info) | cluster_tratamiento + Hotelling | 2000 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | NO APTO | no fiable | 1.0000 | 6.0000 |

## Notas

- El veredicto lo deciden los escenarios en frontera de Δ^RM con la covarianza agrupada del tratamiento; las variantes de covarianza y los escenarios marcados (info) son diagnóstico.
- Con M̄ = 1 y sin tendencia el contraste es conservador por construcción (admite un sesgo que no existe).
- En los casos frontera con M̄ > 0 el tamaño es 0 y la potencia contra τ = −0,05 es ≈ 0 en los tres tamaños: el IC es válido (no sobre-rechaza) pero no es nominal ni informativo con este ruido. Ancho medio del IC95 (log, 8 réplicas, 100 tratados/200 controles): 0,027 con M̄ = 0, 0,105 con M̄ = 0,5 y 0,201 con M̄ = 1 (0,168 con 150/300); es decir, con M̄ = 1 el IC solo excluye el cero si el efecto supera ≈ 0,10 en log, el doble de la magnitud de la literatura de E2 (−0,044). Por qué: la restricción relativa acota el sesgo posterior por M̄ veces el mayor salto previo, y el mayor salto previo se estima con un error del orden de 0,01 (frente a una pendiente verdadera de 0,004). Con M̄ = 0 el método es un contraste de tendencias paralelas posteriores y sí tiene potencia (0,85-1,00).
