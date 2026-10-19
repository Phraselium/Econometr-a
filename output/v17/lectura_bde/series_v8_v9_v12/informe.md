Análisis a posteriori (V17). Grupo series_v8_v9_v12: inferencia convencional de resultados publicados sin inferencia apta, junto al tamaño real medido en el Monte Carlo.

Filas: 86; reproducidas: 37 (desviación relativa máxima 5.77e-14, tolerancia 1e-6); publicables: 24; con reserva (sin medir): 26; no fiables (> 15 %): 16; bloques sin recalcular: 20.

Todo se rotula a posteriori; nada cambia de capa ni de valor. Sin lenguaje causal. Holm y BH por pregunta, nunca entre preguntas.

## V16

- **Q5-p-h1** (Q5, C4): punto -0.4544; p = 0,0358; el contraste rechaza un 8,4 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=1]
- **Q5-p-h4-P** (Q5, C4): punto -0.5128; p = 0,316; el contraste rechaza un 10,1 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=4]
- **Q5-p-h8** (Q5, C4): punto 0.2325; p = 0,813; el contraste rechaza un 11,0 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=8]
- **Q5-p-h12** (Q5, C4): punto 2.303; p = 0,148; el contraste rechaza un 11,6 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=12]
- **Q5-a-h1** (Q5, C4): punto 0.0248; p = 0,387; el contraste rechaza un 8,4 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=1]
- **Q5-a-h4-P** (Q5, C4): punto -0.06205; p = 0,389; el contraste rechaza un 10,1 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=4]
- **Q5-a-h8** (Q5, C4): punto -0.2578; p = 0,111; el contraste rechaza un 11,0 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=8]
- **Q5-a-h12** (Q5, C4): punto -0.2971; p = 0,306; el contraste rechaza un 11,6 % de las veces bajo la nula [sí; herramienta: lp_newey_west_b, NW M=4 normal, rho 0,95, h=12]
- **Q9-g** (Q9, C4): punto 5.919; p = 0,004; el contraste rechaza un 4,5 % de las veces bajo la nula; por debajo del 5 % nominal: conservador; inferencia bootstrap ya publicada y APTA [sí; herramienta: gsadf_factor (bootstrap salvaje; salto y volatilidad estocástica)]
- **Q9-c-CS-ARDL-p2** (Q9, C4): punto 0.8384; p = 0,0167; el contraste rechaza un 10,2 % de las veces bajo la nula [sí; herramienta: csardl (N=38, T=95; escenario más parecido; el contraste simulado usa bootstrap de bloques, no el error de media de grupo)]
- **Q10-1-MIDAS-h1-HLN** (Q10-1, C4): punto -0.1828; p = 0,901; el contraste rechaza un 0,2 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, HLN unilateral, h=1)]
- **Q10-1-MIDAS-h1-CW** (Q10-1, C4): punto -0.1828; p = 0,36; el contraste rechaza un 3,3 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1)]
- **Q10-1-ECM_v1-h1-HLN** (Q10-1, C4): punto -1.349; p = 1; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, HLN unilateral, h=1) (sin escenario comparable)]
- **Q10-1-MIDAS-h4-HLN** (Q10-1, C4): punto -0.09142; p = 0,787; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, HLN unilateral, h=1) (sin escenario comparable)]
- **Q10-1-MIDAS-h4-CW** (Q10-1, C4): punto -0.09142; p = 0,162; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1) (sin escenario comparable)]
- **Q10-1-ECM_v1-h4-HLN** (Q10-1, C4): punto -1.535; p = 0,969; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, HLN unilateral, h=1) (sin escenario comparable)]
- **Q10-2-NOWCAST-h1-HLN** (Q10-2, C4): punto -0.3029; p = 0,985; el contraste rechaza un 0,2 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, HLN unilateral, h=1)]
- **Q10-2-NOWCAST-h1-CW** (Q10-2, C4): punto -0.3029; p = 0,712; el contraste rechaza un 3,3 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1)]
- **Q10-2-NOWCAST-h4-HLN** (Q10-2, C4): punto -0.05388; p = 0,655; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, HLN unilateral, h=1) (sin escenario comparable)]
- **Q10-2-NOWCAST-h4-CW** (Q10-2, C4): punto -0.05388; p = 0,0507; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1) (sin escenario comparable)]
- **Q10-3-MIDAS-h1-HLN** (Q10-3, C4): punto 0.4064; p = 0,0823; el contraste rechaza un 0,2 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, HLN unilateral, h=1)]
- **Q10-3-MIDAS-h1-CW** (Q10-3, C4): punto 0.4064; p = 0,0463; el contraste rechaza un 3,3 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1)]
- **Q10-3-MIDAS-h4-HLN** (Q10-3, C4): punto 0.0324; p = 0,281; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, HLN unilateral, h=1) (sin escenario comparable)]
- **Q10-3-MIDAS-h4-CW** (Q10-3, C4): punto 0.0324; p = 0,0706; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: dm_hln (nulo anidado, CW normal unilateral, h=1) (sin escenario comparable)]

## V15

- **H5-DM-HLN** (H5, C4): punto -0.5139; p = 0,866; el contraste rechaza un 5,5 % de las veces bajo la nula [sí; herramienta: dfm_bvar_mcs (DM-HLN, P = 73; aquí P = 53)]
- **H5-ClarkWest** (H5, C4): punto -0.5139; no fiable: el contraste convencional rechaza un 18.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: dfm_bvar_mcs (Clark-West, δ = 0)]
- **E1-P2-CS-ARDL-p1-theta** (P2, C4): punto 0.6399; p = 0,0445; el contraste rechaza un 0,8 % de las veces bajo la nula; por debajo del 5 % nominal: conservador [sí; herramienta: westerlund_csardl: CS-ARDL elasticidad de largo plazo (cobertura 0,9925)]
- **E1-P2-CS-ARDL-p1-velocidad** (P2, C4): punto -0.2809; no fiable: el contraste convencional rechaza un 99.7 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: westerlund_csardl: CS-ARDL velocidad de ajuste media (cobertura 0,003)]
- **E2-prov-obra_neta_catastro-hogares-SERPAVI** (P7, C4): punto 0.7698; p = 1,62e-08; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-obra_neta_catastro-hogares-IPC_alquiler** (P7, C4): punto 0.5148; p = 0,000944; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-terminadas_MIVAU-hogares-SERPAVI** (P7, C4): punto 0.7427; p = 3,25e-07; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-terminadas_MIVAU-hogares-IPC_alquiler** (P7, C4): punto 0.4973; p = 0,00149; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-iniciadas_MIVAU-hogares-SERPAVI** (P7, C4): punto 0.6985; p = 3,07e-06; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-iniciadas_MIVAU-hogares-IPC_alquiler** (P7, C4): punto 0.4651; p = 0,00326; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-obra_neta_catastro-poblacion-SERPAVI** (P7, C4): punto 0.7698; p = 1,62e-08; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-obra_neta_catastro-poblacion-IPC_alquiler** (P7, C4): punto 0.5148; p = 0,000944; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-terminadas_MIVAU-poblacion-SERPAVI** (P7, C4): punto 0.7427; p = 3,25e-07; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-terminadas_MIVAU-poblacion-IPC_alquiler** (P7, C4): punto 0.4973; p = 0,00149; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-iniciadas_MIVAU-poblacion-SERPAVI** (P7, C4): punto 0.6985; p = 3,07e-06; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E2-prov-iniciadas_MIVAU-poblacion-IPC_alquiler** (P7, C4): punto 0.4651; p = 0,00326; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para correlaciones provinciales]
- **E3-SAR-contigüidad-2015_2024** (P10, C4): punto 0.3928; p = 2,5e-47; el contraste rechaza un 5,5 % de las veces bajo la nula [sí; herramienta: sar_sdm: Wald de ρ (rango de celdas 0,0453-0,055)]

## V8

- **H8-5** (V8-M5, C4): punto -8.776; p = 0,724; el contraste rechaza un 8,7 % de las veces bajo la nula [sí; herramienta: lp_iv, intervalo AR (cobertura 0,913-1,000)]
- **H8-6** (V8-M5, C4): punto -2.912; p = 0,635; el contraste rechaza un 8,7 % de las veces bajo la nula [sí; herramienta: lp_iv, intervalo AR (cobertura 0,913-1,000)]
- **H8-7** (V8-M5, C4): punto -0.5112; p = 0,536; el contraste rechaza un 8,7 % de las veces bajo la nula [sí; herramienta: lp_iv, intervalo AR (cobertura 0,913-1,000)]
- **V8-M0** (V8-M0-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: lp_ols/NW (aprox.)]
- **V8-M1** (V8-M1-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: dfm_pca / dfm_ml]
- **V8-M2** (V8-M2-bloque, C3s): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: BVAR-GLP (cobertura 90 %: 0,86-0,97, con reservas)]
- **V8-M3** (V8-M3-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: lp_ols EWC (cobertura 0,838-0,948)]
- **V8-M4** (V8-M4-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: sin Monte Carlo propio]
- **V8-M6** (V8-M6-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: dominancia (V8 F3)]
- **V8-M7** (V8-M7-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: lp_ols/NW (aprox.)]
- **V8-M8** (V8-M8-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: sin Monte Carlo para Driscoll-Kraay]
- **V8-M9** (V8-M9-bloque, C4): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: shap_grupos (V8 F3)]
- **V8-F5** (V8-F5-bloque, C3s para svar_hd; C4 el resto): ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s [n/a; herramienta: BVAR-GLP]

## V9

- **V9-D1a-00-H1a-renta** (V9-D1a, C4): punto -0.05846; no fiable: el contraste convencional rechaza un 21.6 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: wild_webb_v15 W1 (CS, wild bootstrap por municipio, 198 municipios)]
- **V9-D1a-01-H1a-contratos (explorato** (V9-D1a, C4): punto -0.0625; no fiable: el contraste convencional rechaza un 21.6 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: wild_webb_v15 W1 (CS, wild bootstrap por municipio, 198 municipios)]
- **V9-D1b-02-H1b-renta** (V9-D1b, C4): punto -0.05851; no fiable: el contraste convencional rechaza un 21.6 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: wild_webb_v15 W1 (escenario más parecido; Barcelona, 60 tratados)]
- **V9-D1b-03-H1b-contratos (explorato** (V9-D1b, C4): punto -0.01317; no fiable: el contraste convencional rechaza un 21.6 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: wild_webb_v15 W1 (escenario más parecido; Barcelona, 60 tratados)]
- **V9-D1c-04-exploratoria** (V9-D1c, C4): punto -0.02484; p = 0; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo (CS aún no tratados, N = 13-20)]
- **V9-D1c-05-exploratoria** (V9-D1c, C4): punto -0.06151; p = 0,03; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo (CS aún no tratados, N = 13-20)]
- **V9-D2-06-H2-renta-covid (explorat** (V9-D2, C4): punto 0.00219; no fiable: el contraste convencional rechaza un 20.3 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: rejilla_twfe, municipio (TWFE con dosis continua)]
- **V9-D2-07-H2-renta-reapertura (exp** (V9-D2, C4): punto 0.01046; no fiable: el contraste convencional rechaza un 20.3 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: rejilla_twfe, municipio (TWFE con dosis continua)]
- **V9-D2-08-H2-contratos-covid (expl** (V9-D2, C4): punto 0.01008; no fiable: el contraste convencional rechaza un 20.3 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: rejilla_twfe, municipio (TWFE con dosis continua)]
- **V9-D2-09-H2-contratos-reapertura ** (V9-D2, C4): punto 0.01263; no fiable: el contraste convencional rechaza un 20.3 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: rejilla_twfe, municipio (TWFE con dosis continua)]
- **V9-D3-10-descriptiva** (V9-D3, C4): punto 0.00205; p = 0,34; el contraste rechaza un 9,6 % de las veces bajo la nula [sí; herramienta: conley_seccion (Conley a 2 km; aquí 10 km)]
- **V9-D3-11-descriptiva** (V9-D3, C4): punto -0.00195; p = 0,0804; el contraste rechaza un 9,6 % de las veces bajo la nula [sí; herramienta: conley_seccion (Conley a 2 km; aquí 10 km)]
- **V9-D4-12-H4-réplica-alquiler (exp** (V9-D4, C4): punto 0.00723; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D4-13-H4-réplica-alquiler (exp** (V9-D4, C4): punto 0.00442; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D4-14-exploratoria** (V9-D4, C4): punto -0.00286; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D4-15-exploratoria (efecto tot** (V9-D4, C4): punto -0.00165; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D4-16-H4-réplica-alquiler (exp** (V9-D4, C4): punto 0.01525; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D4-17-exploratoria** (V9-D4, C4): punto 0.1288; no fiable: el contraste convencional rechaza un 21.9 % de las veces bajo la nula (> 15 %); solo estimación puntual [no (no fiable); herramienta: akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)]
- **V9-D5-18-exploratoria** (V9-D5, C4): punto -0.05251; p = 0,322; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para Driscoll-Kraay (N = 17-18 países)]
- **V9-D5-19-exploratoria** (V9-D5, C4): punto -0.04389; p = 0,513; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para Driscoll-Kraay (N = 17-18 países)]
- **V9-D5-20-exploratoria** (V9-D5, C4): punto -0.1168; p = 7e-05; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para Driscoll-Kraay (N = 17-18 países)]
- **V9-D5-21-exploratoria** (V9-D5, C4): punto -0.06561; p = 0,332; distorsión del contraste sin medir en el Monte Carlo del repositorio [con reserva (sin medir); herramienta: sin Monte Carlo para Driscoll-Kraay (N = 17-18 países)]
- **V9-D7** (V9-D7, C4 (contable)): contable: sin inferencia que recalcular [n/a; herramienta: ]
- **V9-D6** (V9-D6, no estimado): no estimado en V9 [n/a; herramienta: ]

## V12

- **V12-f0** (V12-f0, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b1** (V12-b1, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b2** (V12-b2, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b3** (V12-b3, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b4** (V12-b4, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b5** (V12-b5, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b6** (V12-b6, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]
- **V12-b7** (V12-b7, C1/C4 (contable o descriptivo)): contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque) [n/a; herramienta: ]

## Límites
- V8, V9 y V12: salvo M5, se anota que ya tienen bandas/IC publicados o son contables; V9 reutiliza el error publicado y solo añade la regla del 15 % (pipeline no reejecutado).
- Newey-West de Q5: retardo de Newey-West 1994 con normal; el escenario del Monte Carlo es «NW M=4 normal», rho = 0,95.
- El error de media de grupo (Q9-c, P2) no corrige dependencia transversal residual; el Monte Carlo disponible usa otro procedimiento (bootstrap de bloques).
- Correlaciones de P7: distorsión sin medir; el IC supone independencia entre provincias.
- No se calculó Driscoll-Kraay ni Webb: los paneles de V9 no se reestimaron.
- P10 ya tiene inferencia APTA (Wald de ρ); Q9-g tiene bootstrap salvaje APTO.
