# V15-A · H1 y H2: zonas tensionadas en Cataluña (renta y contratos nuevos de Incasòl)

Capa C4 (entrenamiento; asociación, sin lenguaje causal). Estimación **puntual descriptiva**: la inferencia de SDID (placebo literal no computable, Webb NO APTO), Honest DiD y control sintético es NO APTA (docs/v15/validacion_montecarlo.md, K13). Sin p-valor ni IC. `pendiente_sellada: true`: la evaluación sellada (hacia marzo de 2027) no se ha hecho. La ventana 2024T2-2026T1 ya la vio V9-D1 (ATT de CS −5,8 % en renta y −6,2 % en contratos, ambos C4): lo que sigue repite la ventana con otro diseño y es informativo, no confirmatorio.

## Datos y diseño
- Medida: renta de los contratos nuevos de Incasòl (media ponderada por contratos de los tramos con renta publicada; stock excluido) y recuento de contratos. 308 municipios catalanes del recuento de la adenda: 127 de la cohorte 2024T1, 107 de la 2024T4 y 74 nunca tratados. Preperiodo limpio 2022T2-2023T4 (pesos de SDID en 2022T2-2023T2).
- Limitación de los datos: Incasòl suprime la renta con menos de 6 contratos; el panel de renta equilibrado en 16 trimestres solo conserva 184 tratados y 20 donantes (SDID de H1). CS usa los municipios con renta en cada celda. Las cotas de Lee acotan la selección.
- Balance previo (diferencia tipificada tratados menos donantes): log renta 0,7; log contratos 1,3. Donantes en el soporte común de la renta previa: 68 (la regla de la adenda exige ≥ 30 para C3; aquí sería suficiente, pero C3 es inalcanzable en entrenamiento).

## H1 · renta media de los contratos nuevos (log)
- **CS (diseño a):** -7,2 % (cohorte 2024T1: -8,1 %; cohorte 2024T4: -5,4 %). Con solo la cohorte 2024T4 como control de 2024T2-2024T3: -4,5 %.
- **SDID (diseño b):** -3,6 % con 20 donantes (cohorte 2024T1: -2,8 %; 2024T4: -5,7 %).
- **Multiverso (36 especificaciones, BH no aplicable sin p):** CS entre -8,9 % y -3,4 % (9 estimables); SDID entre -4,9 % y -2,8 % (5 estimables). Las celdas con menos de 3 donantes no son estimables o son degeneradas (ver registro.csv).
- **Pretendencias** (CS, 2022T2-2023T3): máximo |coef| 4,7 puntos log·100 frente al umbral declarado 3,7: NO compatible. Contraste SDID 2023T3-2023T4: 4,6: NO compatible.
- **Placebo temporal (2023T2):** CS 7,4, SDID 2,7 (log·100). **Placebo espacial** (1.000 permutaciones, CS): DT 1,0, rango p2,5-p97,5 [-2,0; 2,0]; el ATT de CS queda fuera de ese rango (escala, no p-valor).
- **Exclusiones:** sin Barcelona ni el decil superior de renta: CS -7,2 %, SDID -4,0 %; provincia 08 sin la capital: CS -6,9 %, SDID -2,4 %.
- **Cotas de Lee** (renta observada en todos los trimestres posteriores: 78,6 % de tratados frente a 27,0 % de donantes): variación de la renta entre -9,8 y -0,0 puntos log·100.
- **Control sintético** (10 mayores tratados, puntual): mediana 1,6 %, media 6,5 %. **Ruptura en 2022T2** (preperiodo largo): salto de nivel de la brecha 0,6 puntos log·100; ruptura única estimada en 2023T2. Moran de residuos: I = -0,6/100.
- **Pruebas superadas (regla puntual):** exclusiones_signo_CS, exclusiones_signo_SDID. **Fallidas:** pretendencias_CS, contraste_SDID_2023T3_T4, placebo_temporal_CS, placebo_temporal_SDID. **No evaluadas (herramienta NO APTA):** inferencia de SDID, Webb, Honest DiD, potencia de Roth.

## H2 · número de contratos nuevos
- **CS (diseño a):** -4,2 % (cohorte 2024T1: -8,7 %; cohorte 2024T4: 3,4 %). Con solo la cohorte 2024T4 como control de 2024T2-2024T3: -3,7 %.
- **SDID (diseño b):** -14,2 % con 74 donantes (cohorte 2024T1: -17,8 %; 2024T4: -8,1 %).
- **PPML (principal de H2):** -9,9 % (2024T1: -16,1 %; 2024T4: -0,3 %); TWFE simple de referencia -12,7 %. Sin error típico válido.
- **Multiverso (36 especificaciones, BH no aplicable sin p):** CS entre -32,7 % y 3,1 % (9 estimables); SDID entre -34,8 % y -10,4 % (6 estimables). Las celdas con menos de 3 donantes no son estimables o son degeneradas (ver registro.csv).
- **Pretendencias** (CS, 2022T2-2023T3): máximo |coef| 15,2 puntos log·100 frente al umbral declarado 2,2: NO compatible. Contraste SDID 2023T3-2023T4: -5,1: compatible.
- **Placebo temporal (2023T2):** CS -5,7, SDID -4,0 (log·100). **Placebo espacial** (1.000 permutaciones, CS): DT 3,3, rango p2,5-p97,5 [-6,5; 6,3]; el ATT de CS queda dentro de ese rango (escala, no p-valor).
- **Exclusiones:** sin Barcelona ni el decil superior de renta: CS -3,7 %, SDID -12,0 %; provincia 08 sin la capital: CS 1,0 %, SDID -14,2 %.
- **Pruebas superadas (regla puntual):** contraste_SDID_2023T3_T4, placebo_temporal_SDID, exclusiones_signo_SDID. **Fallidas:** pretendencias_CS, placebo_temporal_CS, exclusiones_signo_CS. **No evaluadas (herramienta NO APTA):** inferencia de SDID, Webb, Honest DiD, potencia de Roth.

## Lectura frente a lo ya publicado
- H1: el signo coincide con V9-D1a (−5,8 %), que no superó pretendencias ni placebo; aquí tampoco las supera la regla puntual declarada (ver arriba), así que el valor no se interpreta como magnitud de la intervención. No contradice con dirección ninguna conclusión de la 1.0.
- H2: V9-D1a concluyó «sin diferencia detectable» con una estimación de −6,2 % (−13,2 a 0,7). Las estimaciones puntuales de aquí son negativas pero sin inferencia válida: no pueden contradecir ni confirmar un contraste de significación. No es una parada.
- Cada estimación se lee junto a V9-D1 (multiplicidad entre versiones, preregistro_v15 §0).

## Fichas reproducibles
Todas: `python3 src/v15/p6_zonas.py && python3 src/v15/p6_informe.py` (SEED 20261010); cifras en output/v15/p6/estimacion_bruta.json.
- <a id="ficha-h1-cs"></a>**ficha-h1-cs / ficha-h2-cs:** clave `principal.<H>.CS_att` (log-diferencia media de las celdas ATT(g,t), g ∈ {2024T1, 2024T4}, t desde 2024T2 / 2024T4 hasta 2026T1, base g−1, ponderada por tratados), convertida a % con 100·(exp(x) − 1). Rango: `multiverso.<H>` con estimador CS y fin 2026T1.
- <a id="ficha-h1-sdid"></a>**ficha-h1-sdid / ficha-h2-sdid:** clave `principal.<H>.SDID_att`; SDID por cohorte con donantes nunca tratados, pesos en 2022T2-2023T2 (src/v15/pa_did.py:sdid).
- <a id="ficha-h1-placebo"></a>**ficha-h1-placebo / ficha-h2-placebo:** `principal.<H>.placebo_temporal_2023T2.CS` (adopción falsa en 2023T2, base 2023T1, controles nunca tratados).
- <a id="ficha-h2-ppml"></a>**ficha-h2-ppml:** `ppml.2026T1.att_pct` (Poisson pseudo-máxima verosimilitud, efectos de municipio y trimestre, cohorte × posterior).
- <a id="ficha-h1-lee"></a>**ficha-h1-lee:** `lee_H1` (selección = renta observada en todos los trimestres posteriores y previos).
- <a id="ficha-h2-cs"></a><a id="ficha-h2-sdid"></a><a id="ficha-h2-placebo"></a>
