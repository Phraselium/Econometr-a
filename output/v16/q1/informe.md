# V16 · Q1 · Zonas tensionadas (grupo A, entrenamiento)

**Capa C4, pendiente de evaluación sellada.** Todo es asociación o descriptivo; sin lenguaje causal. Datos: data/processed/v16/entrenamiento (base_alquiler SERPAVI, base_precio compraventas, base_regulacion BOE); sin muestra sellada. Fecha de corte 2026-10-17.

## Qué se ha hecho
- **Q1a (diagnóstico descriptivo).** Sin RD ni efecto: su resultado solo existe en la muestra sellada. Se cuenta la elegibilidad por el criterio de precio del art. 18.
- **Q1b (SDID).** Se comprueba si hay periodo posterior al tratamiento en el entrenamiento.
- **Q1c (Callaway-Sant'Anna).** Herramienta: NO APTO (tamaño 0,0655; cobertura 0,9015) → solo descriptivo. Estimación puntual, sin p-valor ni IC.
- **BLP/GATES.** No estimable para Q1.

## Resultados
<a id="v16-q1-1"></a>
**Q1b: no estimable en el entrenamiento; pendiente de la evaluación sellada.**
- Tratados fuera de Cataluña con panel SERPAVI: 8 (2 con panel completo 2019-2022 y 2024).
- Primer inicio de zona: 2025-05-01. Último año de SERPAVI en el entrenamiento: 2024. Ninguna otra ventana (no se inventa).
- La inferencia de Conley-Taber solo es APTA en el escenario A, con un tamaño de 0,0575 (límite superior de [0,04; 0,06]). Potencia: MDE 7,1 % frente a −0,75 %.

<a id="v16-q1-3"></a>
**Q1c.** Cohortes: 01 2025Q4, 08 2024Q1, 15 2025Q3, 17 2024Q1, 20 2025Q3, 25 2024Q1, 43 2024Q1, 48 2025Q2.
- Estimador CS global (Δlog de compraventas, tratadas frente a nunca tratadas, base g−1): **-0,048** (≈ -4,7 %); sin grandes ciudades: -0,064.
- Por cohorte: 2024Q1 -0,026, 2025Q2 -0,087, 2025Q3 -0,035, 2025Q4 -0,223. Las cohortes de 2025 tienen pocos trimestres posteriores.
- Estudio de eventos (e = −8…+6): -8: -0,039, -7: -0,035, -6: 0,000, -5: -0,018, -4: 0,006, -3: 0,009, -2: -0,033, 0: -0,051, 1: -0,046, 2: -0,038, 3: -0,066, 4: -0,022, 5: -0,071, 6: -0,041. Los coeficientes previos (e = −8, −7, −2) tienen el mismo orden de magnitud que los posteriores: no hay separación nítida entre la diferencia posterior y el ruido previo.
- Magnitud de referencia: ninguna comparable, así que la condición (b) no se cumple. Sin errores típicos no hay tipo S ni M.

<a id="v16-q1-4"></a>
**Placebo de fecha:** 0,0003 (cohortes adelantadas 8 trimestres; datos hasta el tratamiento real).

<a id="v16-q1-5"></a>
**Cataluña (2024T1):** -0,026. Solapa con H1/H2 de V15 (declarado); no se contrasta con ellas.

<a id="v16-q1-6"></a>
**Q1a:** IPC acumulado 2018-2023 15,7 %; umbral = ln(1+IPC+0,03) = 0,171.
- De 1188 municipios con SERPAVI VC en 2018 y 2023, 864 lo superan y 833 están a ±10 puntos logarítmicos.
- Tasa de declaración: 23,7 % entre elegibles y 5,6 % entre no elegibles (205 y 18 declarados).

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
| Q1b · periodo posterior al tratamiento en el entrenamiento | fallida | primera entrada en vigor fuera de Cataluña 2025-05-01; último año de SERPAVI 2024; zonas vigentes fuera de Cataluña antes de 2025: 0 |
| Q1b · potencia | fallida | MDE 7,1 % frente a −0,75 % de referencia (SERPAVI es stock): sin potencia |
| Q1b · balance tratados/donantes | informativa (sin umbral pre-registrado) | renta ADRH 36.639 frente a 25.974 €; población 160.845 frente a 12.133 (tratados 8, donantes 1.201); exposición al tipo variable no está en disco |
| Q1c · pretendencias (coeficientes previos del estudio de eventos) | informativa (sin umbral pre-registrado) | media de los coeficientes e∈[−8,−2] = -0,016; |media| de las ATT(g,t) previas = 0,101 |
| Q1c · Honest DiD | no evaluable | no validado en la fase 5 (no figura en veredictos.csv) |
| Q1c · placebo de fecha (cohortes 8 trimestres antes) | informativa (sin umbral pre-registrado) | estimación placebo 0,0003 frente a -0,048 del principal |
| Q1c · exclusión de grandes ciudades | informativa | sin Barcelona, València, Sevilla y Málaga: -0,064 (mismo signo) |
| Q1c · balance tratadas/no tratadas | informativa (sin umbral pre-registrado) | diferencias estandarizadas: ln_renta 1,96; ln_pob 0,81; cuota_extranj 0,71; pct_vut_2020_08 0,55; obra_pc 0,20 |
| Q1c · Oster (δ, β=0, Rmax = 1,3 R²) | fallida | δ = -0,158 (δ < 1 = frágil) |
| Q1c · Cinelli-Hazlett RV_q=1 | superada | RV = 0,170 (frágil si < 0,05) |
| Q1c · E-value (puntual) | informativa (sin umbral) | 2,97 |
| Q1c · Moran de los residuos (cruce provincial) | informativa | I = -0,018, p de permutación (diagnóstico) = 0,335 |
| Q1c · heterocedasticidad (Breusch-Pagan) | informativa | LM = 1,232, p = 0,745 |
| Q1c · ruptura (Bai-Perron) en la brecha tratadas − no tratadas | informativa | 2 rupturas, trimestres ['2021Q4', '2023Q2']: la brecha cambia de régimen antes del primer tratamiento (2024T1) |
| Controles negativos (población 65+, IPC general provincial) | no evaluable | no están en el entrenamiento |
| Raíces unitarias / cointegración con dependencia transversal | no aplica | diseños en diferencias sobre ventana corta |
| BLP/GATES de Q1 | no evaluable | Q1b sin periodo posterior; Q1c tiene 8 tratadas frente a 5 moderadores; herramienta NO APTA |

## Límites
Q1c incluye Cataluña (solapa con H1/H2 de V15, declarado). Cohortes 2024T1 (Cataluña) y 2025T2-T4 (Euskadi, Galicia): las de 2025 tienen entre 1 y 4 trimestres posteriores. La cohorte de Álava/Gipuzkoa/Bizkaia/A Coruña se fecha con base_regulacion (zt_vigente); intervenciones.csv recoge una fecha de 2025-01-31 para un municipio de Gipuzkoa que base_regulacion no lleva. Magnitud de referencia de Q1c: ninguna comparable → condición (b) no se cumple. Q1a no tiene resultado en entrenamiento. Multiverso de Q1c: solo la principal y la exclusión del punto 14 (D3).
Resumen para el control de falsos descubrimientos: lista de p-valores vacía (ninguna prueba con inferencia apta). Ficha reproducible: `python3 src/v16/q1_zonas.py` (SEED=20261010); entradas en data/processed/v16/entrenamiento (base_precio, base_alquiler, base_regulacion, base_macro, renta_parque, base_poblacion, alquiler_turismo); salidas en output/v16/q1/ (q1c_att_gt.csv, q1c_evento.csv, q1a_elegibilidad.csv, q1b_balance.csv, registro.csv).
