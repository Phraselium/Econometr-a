Análisis a posteriori (V17). Inferencia convencional de las estimaciones de V15 y V16 (grupo v15_v16_micro) publicadas sin inferencia.

Misma muestra, misma especificación y mismo estimador puntual que lo publicado; solo cambia la inferencia. Regla del 15 %: si el tamaño real del contraste al 5 % nominal medido en el Monte Carlo del repositorio supera el 15 %, la fila es «no fiable» y solo lleva la estimación puntual. Holm y BH se calculan dentro de cada pregunta (nunca entre preguntas) como sensibilidad junto al ajuste original del proyecto; m es el número de contrastes primarios de la pregunta (incluidos los no fiables); las filas alternativas del mismo punto quedan fuera. Nada cambia de capa (todas siguen en C4, DESCRIPTIVO). Sin lenguaje causal.

| id | pregunta | estimación publicada | reproducida | método convencional | p | IC 95 % | tamaño real | publicable | Holm | BH |
|---|---|---|---|---|---|---|---|---|---|---|
| H1-CS | V15 zonas tensionadas (H1, H2) | -7.17883 | -7.17883 | errores robustos agrupados por municipio (función de influencia, t(G-1 |  |  | 0.2165 | no_fiable |  |  |
| H1-SDID | V15 zonas tensionadas (H1, H2) | -3.64207 | -3.64207 | wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDI |  |  | 0.208 | no_fiable |  |  |
| H2-CS | V15 zonas tensionadas (H1, H2) | -4.21589 | -4.21589 | errores robustos agrupados por municipio (función de influencia, t(G-1 |  |  | 0.2165 | no_fiable |  |  |
| H2-SDID | V15 zonas tensionadas (H1, H2) | -14.1605 | -14.1605 | wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDI | 0.0001 | [-19.28; -8.711] | 0.093 | si | 0.0004 | 0.00025 |
| H2-PPML | V15 zonas tensionadas (H1, H2) | -9.94808 | -9.94808 | PPML con efectos de municipio y trimestre; errores robustos agrupados  |  |  | 0.2165 | no_fiable |  |  |
| H3 | V15 turismo por sección (H3) | 0.00298867 | 0.00298867 | Conley 2 km (núcleo de Bartlett, normal), mismo radio que el diseño or | 0.9314 | [-0.06504; 0.07102] | 0.0963 | si | 0.9314 | 0.9314 |
| H4-AKM0 | V15 inmigración shift-share (H4) | 0.30524 | 0.30524 | Anderson-Rubin / AKM0 (inversión del contraste con residuos bajo la nu | 0.2589 | [-1.045; 0.6044] | 0.0047 | si | 0.2589 | 0.2589 |
| H4-AKM | V15 inmigración shift-share (H4) | 0.30524 | 0.30524 | AKM (varianza por origen, normal) |  |  | 0.3283 | no_fiable |  |  |
| H4-PROV | V15 inmigración shift-share (H4) | 0.30524 | 0.30524 | error agrupado por provincia, t(G-1) |  |  | 0.705 | no_fiable |  |  |
| Q1c-global | V16 Q1 zonas tensionadas (Q1c) | -0.0478017 | -0.0478017 | wild cluster bootstrap-t de Webb por provincia (nulo impuesto, B=9.999 | 0.0943 | [-0.1028; 0.007171] | 0.0655 | si | 0.0943 | 0.0943 |
| Q1c-sin-grandes | V16 Q1 zonas tensionadas (Q1c) | -0.0640498 | -0.0640498 | wild cluster bootstrap-t de Webb por provincia (nulo impuesto, B=9.999 | 0.0401 | [-0.1252; -0.002893] | 0.0655 | si | 0.0802 | 0.0802 |
| Q2a | V16 Q2 turismo (Q2a, Q2c) | 0.0131618 | 0.0131618 | wild cluster bootstrap-t de Webb por provincia (residuos restringidos, | 0.0004 | [0.005541; 0.02078] | 0.142 | si | 0.0008 | 0.0008 |
| Q2c | V16 Q2 turismo (Q2a, Q2c) | -0.0053761 | -0.0053761 | wild cluster bootstrap-t de Webb por provincia (residuos restringidos, | 0.3 | [-0.01552; 0.004764] | 0.0605 | si | 0.3 | 0.3 |
| Q3-b | V16 Q3 inmigración (Q3-b, Q3-c) | 0.00907727 | 0.00907727 | Conley 2 km (núcleo de Bartlett, normal), mismo radio y núcleo corregi | 2.607e-13 | [0.006645; 0.01151] | 0.0963 | si | 7.82e-13 | 7.82e-13 |
| Q3-c1-AKM0 | V16 Q3 inmigración (Q3-b, Q3-c) | 0.0118962 | 0.0118962 | AKM0 (inversión del contraste con residuos bajo la nula; varianza por  | 0.3273 |  | 0.0108 | si | 0.3273 | 0.3273 |
| Q3-c1-AKM | V16 Q3 inmigración (Q3-b, Q3-c) | 0.0118962 | 0.0118962 | AKM (varianza por origen, normal), forma reducida |  |  | 0.3762 | no_fiable |  |  |
| Q3-c2-AKM0 | V16 Q3 inmigración (Q3-b, Q3-c) | -0.0281765 | -0.0281765 | AKM0 (inversión del contraste con residuos bajo la nula; varianza por  | 0.07723 | [-0.3851; 0.005971] | 0.0108 | si | 0.1545 | 0.1158 |
| Q3-c2-AKM | V16 Q3 inmigración (Q3-b, Q3-c) | -0.0281765 | -0.0281765 | AKM (varianza por origen, normal), forma reducida |  |  | 0.3762 | no_fiable |  |  |
| Q4a | V16 Q4 oferta (Q4a, Q4b) | -0.129719 | -0.129719 | errores robustos agrupados por provincia, t(G-1); efectos fijos de pro |  |  | 0.203 | no_fiable |  |  |
| Q4b | V16 Q4 oferta (Q4a, Q4b) | -0.00138262 | -0.00138262 | errores robustos agrupados por provincia, t(G-1); efectos fijos de año |  |  | 0.203 | no_fiable |  |  |
| Q6-v | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | 0.0250825 | 0.0250825 | inferencia por aleatorización del calendario entre CCAA (B=9.999 permu | 0.2178 | [-0.01499; 0.06516] | 0.0775 | si | 0.4356 | 0.4356 |
| Q6-v-Webb | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | 0.0250825 | 0.0250825 | wild cluster bootstrap-t de Webb por CCAA (B=9.999; nulo impuesto) sob | 0.1758 | [-0.008495; 0.05866] |  | sin_medir |  |  |
| Q6-p | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | -0.00203721 | -0.00203721 | inferencia por aleatorización del calendario entre CCAA (B=9.999 permu | 0.886 | [-0.03234; 0.02826] | 0.0775 | si | 0.886 | 0.886 |
| Q6-p-Webb | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | -0.00203721 | -0.00203721 | wild cluster bootstrap-t de Webb por CCAA (B=9.999; nulo impuesto) sob | 0.8565 | [-0.02568; 0.02161] |  | sin_medir |  |  |
| Q7 | V16 Q7 bono alquiler joven | -0.119972 | -0.119972 | wild cluster bootstrap-t de Webb por edad del sustentador (variable de | 0.0743 | [-0.26; 0.02001] |  | sin_medir | 0.0743 | 0.0743 |
| Q8 | V16 Q8 no residentes | -1.33287 | -1.33287 | Newey-West (Bartlett, retardo 2 = regla de Newey-West 1994 con T=8) so | 0.006651 | [-2.157; -0.5347] |  | sin_medir | 0.006651 | 0.006651 |

## Frases publicables

- **H2-SDID** (sdid_placebo_h1h2 S3_H2_74donantes, webb_cluster): p = 0,000; el contraste rechaza un 9,3 % de las veces bajo la nula. A posteriori.
- **H3** (conley_seccion, escenario principal (radio 1,0 km), Conley 2 km): p = 0,931; el contraste rechaza un 9,6 % de las veces bajo la nula. A posteriori.
- **H4-AKM0** (akm_municipal M3_instr_sin_residenciales_F_alta, AKM0 (AR)): p = 0,259; el contraste rechaza un 0,5 % de las veces bajo la nula (contraste conservador: por debajo del 5 % nominal). A posteriori.
- **Q1c-global** (cs_webb variante b (WCR, nulo impuesto, Webb por provincia)): p = 0,094; el contraste rechaza un 6,6 % de las veces bajo la nula. A posteriori.
- **Q1c-sin-grandes** (cs_webb variante b (WCR, nulo impuesto, Webb por provincia)): p = 0,040; el contraste rechaza un 6,6 % de las veces bajo la nula. A posteriori.
- **Q2a** (did_intensidad_webb Q2a provincial, Webb (principal)): p = 0,000; el contraste rechaza un 14,2 % de las veces bajo la nula. A posteriori.
- **Q2c** (did_intensidad_webb Q2c municipal, Webb por provincia (referencia extra)): p = 0,300; el contraste rechaza un 6,0 % de las veces bajo la nula. A posteriori.
- **Q3-b** (conley_seccion, escenario principal (radio 1,0 km), Conley 2 km): p = 0,000; el contraste rechaza un 9,6 % de las veces bajo la nula. A posteriori.
- **Q3-c1-AKM0** (shiftshare_akm principal wA=0,5, AKM0): p = 0,327; el contraste rechaza un 1,1 % de las veces bajo la nula (contraste conservador: por debajo del 5 % nominal). A posteriori.
- **Q3-c2-AKM0** (shiftshare_akm principal wA=0,5, AKM0): p = 0,077; el contraste rechaza un 1,1 % de las veces bajo la nula (contraste conservador: por debajo del 5 % nominal). A posteriori.
- **Q6-v** (dcdh_aleatorizacion nulo (aleatorización del calendario entre CCAA)): p = 0,218; el contraste rechaza un 7,8 % de las veces bajo la nula. A posteriori.
- **Q6-v-Webb** (sin medir (no hay Monte Carlo de esta herramienta en el repositorio)): p = 0,176; distorsión del contraste sin medir (no hay Monte Carlo de esta herramienta). A posteriori.
- **Q6-p** (dcdh_aleatorizacion nulo (aleatorización del calendario entre CCAA)): p = 0,886; el contraste rechaza un 7,8 % de las veces bajo la nula. A posteriori.
- **Q6-p-Webb** (sin medir (no hay Monte Carlo de esta herramienta en el repositorio)): p = 0,857; distorsión del contraste sin medir (no hay Monte Carlo de esta herramienta). A posteriori.
- **Q7** (sin medir (no hay Monte Carlo de esta herramienta en el repositorio)): p = 0,074; distorsión del contraste sin medir (no hay Monte Carlo de esta herramienta). A posteriori.
- **Q8** (sin medir (no hay Monte Carlo de esta herramienta en el repositorio)): p = 0,007; distorsión del contraste sin medir (no hay Monte Carlo de esta herramienta). A posteriori.

## No fiables (solo estimación puntual)

- **H1-CS**: Inferencia convencional NO publicada: el contraste (errores robustos agrupados por municipio (función de influencia, t(G-1)); nivel del tratamiento = municipio (308 > 40 clusters: sin Webb)) rechaza un 21,6 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: wild_webb_v15 W1_H1H2_198municipios, CR1 por municipio.
- **H1-SDID**: Inferencia convencional NO publicada: el contraste (wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDID (pesos fijos, nulo impuesto, B=9.999); IC percentil-t simétrico) rechaza un 20,8 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: sdid_placebo_h1h2 S1_H1_74donantes, webb_cluster.
- **H2-CS**: Inferencia convencional NO publicada: el contraste (errores robustos agrupados por municipio (función de influencia, t(G-1)); nivel del tratamiento = municipio (308 > 40 clusters: sin Webb)) rechaza un 21,6 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: wild_webb_v15 W1_H1H2_198municipios, CR1 por municipio.
- **H2-PPML**: Inferencia convencional NO publicada: el contraste (PPML con efectos de municipio y trimestre; errores robustos agrupados por municipio (método delta para el agregado de las dos cohortes)) rechaza un 21,6 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: wild_webb_v15 W1 (CR1 por municipio; TWFE lineal, análogo del PPML: PPML sin medir).
- **H4-AKM**: Inferencia convencional NO publicada: el contraste (AKM (varianza por origen, normal)) rechaza un 32,8 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: akm_municipal M3_instr_sin_residenciales_F_alta, AKM.
- **H4-PROV**: Inferencia convencional NO publicada: el contraste (error agrupado por provincia, t(G-1)) rechaza un 70,5 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: akm_municipal M3_instr_sin_residenciales_F_alta, agrupado provincia t(40).
- **Q3-c1-AKM**: Inferencia convencional NO publicada: el contraste (AKM (varianza por origen, normal), forma reducida) rechaza un 37,6 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: shiftshare_akm principal wA=0,5, AKM.
- **Q3-c2-AKM**: Inferencia convencional NO publicada: el contraste (AKM (varianza por origen, normal), forma reducida) rechaza un 37,6 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: shiftshare_akm principal wA=0,5, AKM.
- **Q4a**: Inferencia convencional NO publicada: el contraste (errores robustos agrupados por provincia, t(G-1); efectos fijos de provincia y año) rechaza un 20,3 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: rejilla_twfe escala municipio (CR1 por provincia, 41 clusters), TWFE de exposición continua; análogo, no el diseño exacto.
- **Q4b**: Inferencia convencional NO publicada: el contraste (errores robustos agrupados por provincia, t(G-1); efectos fijos de año) rechaza un 20,3 % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori. Distorsión tomada de: rejilla_twfe escala municipio (CR1 por provincia, 41 clusters), TWFE de exposición continua; análogo, no el diseño exacto.

## Notas por fila

- **H1-CS**: Resultado en log(renta) (H1) o log(1+contratos) (H2). La dependencia espacial entre municipios no está recogida por el agrupamiento. Punto reproducido (rel. 0.0e+00).
- **H1-SDID**: Pesos SDID tratados como fijos (como en el Monte Carlo sdid_placebo_h1h2). Punto reproducido (rel. 4.9e-14).
- **H2-CS**: Resultado en log(renta) (H1) o log(1+contratos) (H2). La dependencia espacial entre municipios no está recogida por el agrupamiento. Punto reproducido (rel. 0.0e+00).
- **H2-SDID**: Pesos SDID tratados como fijos (como en el Monte Carlo sdid_placebo_h1h2). La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 1.8e-12).
- **H2-PPML**: Principal de H2. Monte Carlo del PPML no existe: se toma el TWFE lineal de wild_webb_v15 W1 como análogo. Punto reproducido (rel. 1.1e-14).
- **H3**: Panel T=4 (el Monte Carlo es de corte transversal con efectos fijos de municipio: escenario más parecido). EE agrupado por municipio: 0.0410 (p = 0.942); referencia, sin medir en panel. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 2.9e-14).
- **H4-AKM0**: F efectivo de Montiel Olea-Pflueger (varianza AKM de la primera etapa) = 12.8 (referencia 23,1 para tau=10 %, un instrumento; el F robusto HC1 publicado es 70,2); número efectivo de choques = 1.3; IC AKM0 acotado. Primaria de H4 (única inferencia con tamaño ≤ 15 %; muy conservadora: potencia 0,008 frente a la referencia de Saiz). La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 1.3e-14).
- **H4-AKM**: Alternativa de la misma estimación (excluida de Holm/BH). Punto reproducido (rel. 1.3e-14).
- **H4-PROV**: Alternativa (excluida de Holm/BH). Punto reproducido (rel. 1.3e-14).
- **Q1c-global**: Q1c incluye Cataluña (solapa con H1/H2). Q1a es un recuento y Q1b no es estimable en el entrenamiento: sin inferencia aplicable. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 1.5e-16).
- **Q1c-sin-grandes**: Q1c incluye Cataluña (solapa con H1/H2). Q1a es un recuento y Q1b no es estimable en el entrenamiento: sin inferencia aplicable. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 2.2e-16).
- **Q2a**: EE CR1 por provincia, t(G-1): p = 0.000 (referencia). Punto reproducido también con Q.twfe (0.013162). La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 7.4e-15).
- **Q2c**: El Monte Carlo del principal de Q2c (CR1 por provincia) da tamaño 0,0975; Webb por provincia (la herramienta usada aquí) 0,0605 (referencia extra del Monte Carlo). EE CR1: p = 0.209. Punto con Q.twfe: -0.005376. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 6.3e-15).
- **Q3-b**: Escenario exacto del Monte Carlo (corte transversal con efectos fijos de municipio). Pretendencia 2018-2021 no nula en la publicación (diagnóstico del original): la inferencia no corrige el sesgo de selección. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 0.0e+00).
- **Q3-c1-AKM0**: Forma reducida sin instrumento: Anderson-Rubin y F efectivo no aplican. Número efectivo de choques = 1.0; IC AKM0 no acotado. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 4.4e-16).
- **Q3-c1-AKM**: Alternativa (excluida de Holm/BH). Punto reproducido (rel. 4.4e-16).
- **Q3-c2-AKM0**: Forma reducida sin instrumento: Anderson-Rubin y F efectivo no aplican. Número efectivo de choques = 3.1; IC AKM0 acotado. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 4.9e-16).
- **Q3-c2-AKM**: Alternativa (excluida de Holm/BH). Punto reproducido (rel. 4.9e-16).
- **Q4a**: Agrupado por provincia (análogo al Monte Carlo) en lugar de por municipio (nivel del tratamiento: la correlación espacial de la Red Natura cruza municipios); EE agrupado por municipio (4374 clusters) = 0.0185. Punto reproducido (rel. 0.0e+00).
- **Q4b**: Agrupado por provincia (análogo al Monte Carlo); EE agrupado por municipio (1293 clusters) = 0.00135. El choque de demanda es el shift-share de Q3 (generado a partir de cuotas): ni AKM ni la corrección por regresor generado están aplicados. Punto reproducido (rel. 0.0e+00).
- **Q6-v**: Los calendarios se reasignan entre las 8 CCAA del panel (el Monte Carlo usó 11, con Ceuta y Melilla). Con 8 CCAA y pocos cambios de tipo la prueba tiene resolución limitada. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 0.0e+00).
- **Q6-v-Webb**: Webb sobre dCDH no está en el Monte Carlo: sin medir. Alternativa de la misma estimación (excluida de Holm/BH). Con 8 clusters el bootstrap tiene pocas combinaciones distintas. Punto reproducido (rel. 0.0e+00).
- **Q6-p**: Los calendarios se reasignan entre las 8 CCAA del panel (el Monte Carlo usó 11, con Ceuta y Melilla). Con 8 CCAA y pocos cambios de tipo la prueba tiene resolución limitada. La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %. Punto reproducido (rel. 0.0e+00).
- **Q6-p-Webb**: Webb sobre dCDH no está en el Monte Carlo: sin medir. Alternativa de la misma estimación (excluida de Holm/BH). Con 8 clusters el bootstrap tiene pocas combinaciones distintas. Punto reproducido (rel. 0.0e+00).
- **Q7**: Agrupar por edad es el estándar con variable de asignación discreta (Lee y Card 2008); la ECV es muestreo complejo (estratos y conglomerados no declarados en la publicación). Lectura: cambio de generosidad entre el Plan 2018-2021 y el Bono, no efecto del programa (ver q7). Punto reproducido (rel. 7.8e-14).
- **Q8**: La estimación publicada es la razón de sumas (-1.3329); la regresión sobre cuotas trimestrales da -1.3459 (diferencia de medias simples): se usa para la inferencia. Solo 8 trimestres: la corrección de HAC con T tan pequeño es poco fiable. La referencia del año anterior (-0,68 pp) no se contrasta: la comparación es entre ventanas, no un diseño con grupo de control. Punto reproducido (rel. 0.0e+00). (El punto reproducido es la razón de sumas publicada, no el de la regresión.)

## No cubierto

- Q1a (recuento de elegibilidad) y Q1b (SDID con Conley-Taber, no estimable en el entrenamiento por no haber periodo posterior): sin estimación sujeta a inferencia.
- Q3-b y Q3-c comparten familia (Q3); las alternativas AKM/AKM0 de la misma estimación y los Webb sin medir de Q6 no entran en Holm/BH.
- Honest DiD, TOST y BLP/GATES no son inferencia de estos resultados y no se tocan. Fuentes del tamaño real: docs/v15/validacion_montecarlo/*.md, docs/v16/validacion_montecarlo.md y output/v16/montecarlo/.
