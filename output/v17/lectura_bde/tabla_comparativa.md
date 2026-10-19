# V17 · Fase 2 · Lectura convencional frente a las capas del proyecto

Análisis a posteriori (V17). Generado por src/v17/f2_lectura_bde.py a partir de output/v17/lectura_bde/<grupo>/inferencia.csv. La lectura convencional es la inferencia que usaría un trabajo publicado. Se muestra junto a la distorsión medida en el Monte Carlo del repositorio y no cambia la capa del proyecto. Regla: si el tamaño real supera el 15 %, no se publica (solo estimación puntual).

Recuento: publicable: 36; con reserva (distorsión sin medir): 30; no fiable: 26; no recalculado (ya tenía inferencia o es contable): 20.

| Versión | Resultado | Pregunta | Estimación | Capa del proyecto | Lectura convencional | Distorsión | Regla | p Holm (pregunta) | Mejor estimación (B4) | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|
| V15 | H1-CS | V15 zonas tensionadas (H1, H2) | -7.179 % (100·(exp(ATT)-1)) | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V15 | H1-SDID | V15 zonas tensionadas (H1, H2) | -3.642 % (100·(exp(ATT)-1)) | C4 | solo estimación puntual | tamaño real 20.8 % al 5 % nominal | no fiable |  |  |  |
| V15 | H2-CS | V15 zonas tensionadas (H1, H2) | -4.216 % (100·(exp(ATT)-1)) | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V15 | H2-SDID | V15 zonas tensionadas (H1, H2) | -14.16 % (100·(exp(ATT)-1)) | C4 | p = 0.0001; IC 95 % [-19.28; -8.711] | tamaño real 9.3 % al 5 % nominal | publicable | 0.0004 |  |  |
| V15 | H2-PPML | V15 zonas tensionadas (H1, H2) | -9.948 % (cambio porcentual) | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V15 | H3 | V15 turismo por sección (H3) | 0.002989 % de alquiler por DT intra-sección del % de viviendas turísticas | C4 | p = 0.931; IC 95 % [-0.06504; 0.07102] | tamaño real 9.6 % al 5 % nominal | publicable | 0.931 |  |  |
| V15 | H4-AKM0 | V15 inmigración shift-share (H4) | 0.3052 % de alquiler por punto porcentual de población extranjera | C4 | p = 0.259; IC 95 % [-1.045; 0.6044] | tamaño real 0.5 % al 5 % nominal | publicable | 0.259 |  |  |
| V15 | H4-AKM | V15 inmigración shift-share (H4) | 0.3052 % de alquiler por punto porcentual de población extranjera | C4 | solo estimación puntual | tamaño real 32.8 % al 5 % nominal | no fiable |  |  |  |
| V15 | H4-PROV | V15 inmigración shift-share (H4) | 0.3052 % de alquiler por punto porcentual de población extranjera | C4 | solo estimación puntual | tamaño real 70.5 % al 5 % nominal | no fiable |  |  |  |
| V16 | Q1c-global | V16 Q1 zonas tensionadas (Q1c) | -0.0478 Δlog (ATT global) | C4 | p = 0.0943; IC 95 % [-0.1028; 0.007171] | tamaño real 6.6 % al 5 % nominal | publicable | 0.0943 |  |  |
| V16 | Q1c-sin-grandes | V16 Q1 zonas tensionadas (Q1c) | -0.06405 Δlog (ATT global) | C4 | p = 0.0401; IC 95 % [-0.1252; -0.002893] | tamaño real 6.6 % al 5 % nominal | publicable | 0.0802 |  |  |
| V16 | Q2a | V16 Q2 turismo (Q2a, Q2c) | 0.01316 Δlog IPC alquiler por DT del log de la exposición | C4 | p = 0.0004; IC 95 % [0.005541; 0.02078] | tamaño real 14.2 % al 5 % nominal | publicable | 0.0008 |  |  |
| V16 | Q2c | V16 Q2 turismo (Q2a, Q2c) | -0.005376 Δlog IPVA-TAM por DT de la exposición (nivel) | C4 | p = 0.3; IC 95 % [-0.01552; 0.004764] | tamaño real 6.0 % al 5 % nominal | publicable | 0.3 |  |  |
| V16 | Q3-b | V16 Q3 inmigración (Q3-b, Q3-c) | 0.009077 Δlog SERPAVI VC 2021-2024 por DT de la cuota de extranjeros | C4 | p = 2.61e-13; IC 95 % [0.006645; 0.01151] | tamaño real 9.6 % al 5 % nominal | publicable | 7.82e-13 |  |  |
| V16 | Q3-c1-AKM0 | V16 Q3 inmigración (Q3-b, Q3-c) | 0.0119 log del valor tasado por punto de población extranjera predicha | C4 | p = 0.327 | tamaño real 1.1 % al 5 % nominal | publicable | 0.327 |  |  |
| V16 | Q3-c1-AKM | V16 Q3 inmigración (Q3-b, Q3-c) | 0.0119 log del valor tasado por punto de población extranjera predicha | C4 | solo estimación puntual | tamaño real 37.6 % al 5 % nominal | no fiable |  |  |  |
| V16 | Q3-c2-AKM0 | V16 Q3 inmigración (Q3-b, Q3-c) | -0.02818 log de las compraventas por punto de población extranjera predicha | C4 | p = 0.0772; IC 95 % [-0.3851; 0.005971] | tamaño real 1.1 % al 5 % nominal | publicable | 0.154 |  |  |
| V16 | Q3-c2-AKM | V16 Q3 inmigración (Q3-b, Q3-c) | -0.02818 log de las compraventas por punto de población extranjera predicha | C4 | solo estimación puntual | tamaño real 37.6 % al 5 % nominal | no fiable |  |  |  |
| V16 | Q4a | V16 Q4 oferta (Q4a, Q4b) | -0.1297 Δlog obra nueva neta por DT del % Red Natura | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V16 | Q4b | V16 Q4 oferta (Q4a, Q4b) | -0.001383 Δlog SERPAVI por DT de Red Natura y punto de choque | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V16 | Q6-v | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | 0.02508 Δlog por punto de tipo general del ITP | C4 | p = 0.218; IC 95 % [-0.01499; 0.06516] | tamaño real 7.8 % al 5 % nominal | publicable | 0.436 |  |  |
| V16 | Q6-v-Webb | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | 0.02508 Δlog por punto de tipo general del ITP | C4 | p = 0.176; IC 95 % [-0.008495; 0.05866] | sin medir | con reserva (distorsión sin medir) |  |  |  |
| V16 | Q6-p | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | -0.002037 Δlog por punto de tipo general del ITP | C4 | p = 0.886; IC 95 % [-0.03234; 0.02826] | tamaño real 7.8 % al 5 % nominal | publicable | 0.886 |  |  |
| V16 | Q6-p-Webb | V16 Q6 fiscalidad ITP (Q6-v, Q6-p) | -0.002037 Δlog por punto de tipo general del ITP | C4 | p = 0.857; IC 95 % [-0.02568; 0.02161] | sin medir | con reserva (distorsión sin medir) |  |  |  |
| V16 | Q7 | V16 Q7 bono alquiler joven | -0.12 Δlog alquiler (diferencia en discontinuidades, ancho ±5) | C4 | p = 0.0743; IC 95 % [-0.26; 0.02001] | sin medir | con reserva (distorsión sin medir) | 0.0743 |  |  |
| V16 | Q8 | V16 Q8 no residentes | -1.333 puntos porcentuales de cuota (ventana de 4 trimestres posterior a 2025Q2 menos la anterior) | C4 | p = 0.00665; IC 95 % [-2.157; -0.5347] | sin medir | con reserva (distorsión sin medir) | 0.00665 |  |  |
| V16 | Q5-p-h1 | Q5 | -0.4544 % acumulado por DT de sorpresa | C4 | p = 0.0358; IC 95 % [-0.8786; -0.03017] | tamaño real 8.4 % al 5 % nominal | publicable | 0.286 |  |  |
| V16 | Q5-p-h4-P | Q5 | -0.5128 % acumulado por DT de sorpresa | C4 | p = 0.316; IC 95 % [-1.514; 0.4889] | tamaño real 10.1 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q5-p-h8 | Q5 | 0.2325 % acumulado por DT de sorpresa | C4 | p = 0.813; IC 95 % [-1.692; 2.157] | tamaño real 11.0 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q5-p-h12 | Q5 | 2.303 % acumulado por DT de sorpresa | C4 | p = 0.148; IC 95 % [-0.8209; 5.428] | tamaño real 11.6 % al 5 % nominal | publicable | 0.891 |  |  |
| V16 | Q5-a-h1 | Q5 | 0.0248 % acumulado por DT de sorpresa | C4 | p = 0.387; IC 95 % [-0.03138; 0.08098] | tamaño real 8.4 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q5-a-h4-P | Q5 | -0.06205 % acumulado por DT de sorpresa | C4 | p = 0.389; IC 95 % [-0.2031; 0.07899] | tamaño real 10.1 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q5-a-h8 | Q5 | -0.2578 % acumulado por DT de sorpresa | C4 | p = 0.111; IC 95 % [-0.5753; 0.05969] | tamaño real 11.0 % al 5 % nominal | publicable | 0.78 |  |  |
| V16 | Q5-a-h12 | Q5 | -0.2971 % acumulado por DT de sorpresa | C4 | p = 0.306; IC 95 % [-0.8662; 0.272] | tamaño real 11.6 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q9-g | Q9 | 5.919 estadístico GSADF del factor común | C4 | p = 0.004 | tamaño real 4.5 % al 5 % nominal | publicable | 0.008 |  |  |
| V16 | Q9-c-CS-ARDL-p2 | Q9 | 0.8384 elasticidad de largo plazo (θ medio) | C4 | p = 0.0167; IC 95 % [0.1621; 1.515] | tamaño real 10.2 % al 5 % nominal | publicable | 0.0167 |  |  |
| V16 | Q10-1-MIDAS-h1-HLN | Q10-1 | -0.1828 reducción relativa del ECM frente al AR(4) | C4 | p = 0.901 | tamaño real 0.2 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q10-1-MIDAS-h1-CW | Q10-1 | -0.1828 reducción relativa del ECM frente al AR(4) | C4 | p = 0.36 | tamaño real 3.3 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q10-1-ECM_v1-h1-HLN | Q10-1 | -1.349 reducción relativa del ECM frente al AR(4) | C4 | p = 1 | sin medir | con reserva (distorsión sin medir) | 1 |  |  |
| V16 | Q10-1-MIDAS-h4-HLN | Q10-1 | -0.09142 reducción relativa del ECM frente al AR(4) | C4 | p = 0.787 | sin medir | con reserva (distorsión sin medir) | 1 |  |  |
| V16 | Q10-1-MIDAS-h4-CW | Q10-1 | -0.09142 reducción relativa del ECM frente al AR(4) | C4 | p = 0.162 | sin medir | con reserva (distorsión sin medir) | 0.973 |  |  |
| V16 | Q10-1-ECM_v1-h4-HLN | Q10-1 | -1.535 reducción relativa del ECM frente al AR(4) | C4 | p = 0.969 | sin medir | con reserva (distorsión sin medir) | 1 |  |  |
| V16 | Q10-2-NOWCAST-h1-HLN | Q10-2 | -0.3029 reducción relativa del ECM frente al AR(4) | C4 | p = 0.985 | tamaño real 0.2 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q10-2-NOWCAST-h1-CW | Q10-2 | -0.3029 reducción relativa del ECM frente al AR(4) | C4 | p = 0.712 | tamaño real 3.3 % al 5 % nominal | publicable | 1 |  |  |
| V16 | Q10-2-NOWCAST-h4-HLN | Q10-2 | -0.05388 reducción relativa del ECM frente al AR(4) | C4 | p = 0.655 | sin medir | con reserva (distorsión sin medir) | 1 |  |  |
| V16 | Q10-2-NOWCAST-h4-CW | Q10-2 | -0.05388 reducción relativa del ECM frente al AR(4) | C4 | p = 0.0507 | sin medir | con reserva (distorsión sin medir) | 0.203 |  |  |
| V16 | Q10-3-MIDAS-h1-HLN | Q10-3 | 0.4064 reducción relativa del ECM frente al AR(4) | C4 | p = 0.0823 | tamaño real 0.2 % al 5 % nominal | publicable | 0.212 |  |  |
| V16 | Q10-3-MIDAS-h1-CW | Q10-3 | 0.4064 reducción relativa del ECM frente al AR(4) | C4 | p = 0.0463 | tamaño real 3.3 % al 5 % nominal | publicable | 0.185 |  |  |
| V16 | Q10-3-MIDAS-h4-HLN | Q10-3 | 0.0324 reducción relativa del ECM frente al AR(4) | C4 | p = 0.281 | sin medir | con reserva (distorsión sin medir) | 0.281 |  |  |
| V16 | Q10-3-MIDAS-h4-CW | Q10-3 | 0.0324 reducción relativa del ECM frente al AR(4) | C4 | p = 0.0706 | sin medir | con reserva (distorsión sin medir) | 0.212 |  |  |
| V15 | H5-DM-HLN | H5 | -0.5139 reducción relativa del ECM frente al AR(4) | C4 | p = 0.866 | tamaño real 5.5 % al 5 % nominal | publicable | 0.866 |  |  |
| V15 | H5-ClarkWest | H5 | -0.5139 reducción relativa del ECM frente al AR(4) | C4 | solo estimación puntual | tamaño real 18.9 % al 5 % nominal | no fiable |  |  |  |
| V15 | E1-P2-CS-ARDL-p1-theta | P2 | 0.6399 elasticidad de largo plazo (θ medio) | C4 | p = 0.0445; IC 95 % [0.01663; 1.263] | tamaño real 0.8 % al 5 % nominal | publicable | 0.0445 |  |  |
| V15 | E1-P2-CS-ARDL-p1-velocidad | P2 | -0.2809 velocidad de ajuste media (φ) | C4 | solo estimación puntual | tamaño real 99.7 % al 5 % nominal | no fiable |  |  |  |
| V15 | E2-prov-obra_neta_catastro-hogares-SERPAVI | P7 | 0.7698 correlación de Pearson | C4 | p = 1.62e-08; IC 95 % [0.597; 0.8743] | sin medir | con reserva (distorsión sin medir) | 1.94e-07 |  |  |
| V15 | E2-prov-obra_neta_catastro-hogares-IPC_alquiler | P7 | 0.5148 correlación de Pearson | C4 | p = 0.000944; IC 95 % [0.2335; 0.7165] | sin medir | con reserva (distorsión sin medir) | 0.00566 |  |  |
| V15 | E2-prov-terminadas_MIVAU-hogares-SERPAVI | P7 | 0.7427 correlación de Pearson | C4 | p = 3.25e-07; IC 95 % [0.5441; 0.8625] | sin medir | con reserva (distorsión sin medir) | 3.25e-06 |  |  |
| V15 | E2-prov-terminadas_MIVAU-hogares-IPC_alquiler | P7 | 0.4973 correlación de Pearson | C4 | p = 0.00149; IC 95 % [0.2111; 0.7049] | sin medir | con reserva (distorsión sin medir) | 0.00597 |  |  |
| V15 | E2-prov-iniciadas_MIVAU-hogares-SERPAVI | P7 | 0.6985 correlación de Pearson | C4 | p = 3.07e-06; IC 95 % [0.4761; 0.8369] | sin medir | con reserva (distorsión sin medir) | 2.46e-05 |  |  |
| V15 | E2-prov-iniciadas_MIVAU-hogares-IPC_alquiler | P7 | 0.4651 correlación de Pearson | C4 | p = 0.00326; IC 95 % [0.1709; 0.6832] | sin medir | con reserva (distorsión sin medir) | 0.00651 |  |  |
| V15 | E2-prov-obra_neta_catastro-poblacion-SERPAVI | P7 | 0.7698 correlación de Pearson | C4 | p = 1.62e-08; IC 95 % [0.597; 0.8743] | sin medir | con reserva (distorsión sin medir) | 1.94e-07 |  |  |
| V15 | E2-prov-obra_neta_catastro-poblacion-IPC_alquiler | P7 | 0.5148 correlación de Pearson | C4 | p = 0.000944; IC 95 % [0.2335; 0.7165] | sin medir | con reserva (distorsión sin medir) | 0.00566 |  |  |
| V15 | E2-prov-terminadas_MIVAU-poblacion-SERPAVI | P7 | 0.7427 correlación de Pearson | C4 | p = 3.25e-07; IC 95 % [0.5441; 0.8625] | sin medir | con reserva (distorsión sin medir) | 3.25e-06 |  |  |
| V15 | E2-prov-terminadas_MIVAU-poblacion-IPC_alquiler | P7 | 0.4973 correlación de Pearson | C4 | p = 0.00149; IC 95 % [0.2111; 0.7049] | sin medir | con reserva (distorsión sin medir) | 0.00597 |  |  |
| V15 | E2-prov-iniciadas_MIVAU-poblacion-SERPAVI | P7 | 0.6985 correlación de Pearson | C4 | p = 3.07e-06; IC 95 % [0.4761; 0.8369] | sin medir | con reserva (distorsión sin medir) | 2.46e-05 |  |  |
| V15 | E2-prov-iniciadas_MIVAU-poblacion-IPC_alquiler | P7 | 0.4651 correlación de Pearson | C4 | p = 0.00326; IC 95 % [0.1709; 0.6832] | sin medir | con reserva (distorsión sin medir) | 0.00651 |  |  |
| V15 | E3-SAR-contigüidad-2015_2024 | P10 | 0.3928 ρ espacial (SAR, contigüidad) | C4 | p = 2.5e-47; IC 95 % [0.3395; 0.4461] | tamaño real 5.5 % al 5 % nominal | publicable | 2.5e-47 |  |  |
| V8 | H8-5 | V8-M5 | -8.776 LP-IV acumulado (descriptivo) | C4 | p = 0.724 | tamaño real 8.7 % al 5 % nominal | publicable | 1 |  |  |
| V8 | H8-6 | V8-M5 | -2.912 LP-IV acumulado (descriptivo) | C4 | p = 0.635 | tamaño real 8.7 % al 5 % nominal | publicable | 1 |  |  |
| V8 | H8-7 | V8-M5 | -0.5112 LP-IV acumulado (descriptivo) | C4 | p = 0.536 | tamaño real 8.7 % al 5 % nominal | publicable | 1 |  |  |
| V8 | V8-M0 | V8-M0-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M1 | V8-M1-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M2 | V8-M2-bloque |  | C3s | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M3 | V8-M3-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M4 | V8-M4-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M6 | V8-M6-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M7 | V8-M7-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M8 | V8-M8-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-M9 | V8-M9-bloque |  | C4 | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V8 | V8-F5 | V8-F5-bloque |  | C3s para svar_hd; C4 el resto | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V9 | V9-D1a-00-H1a-renta | V9-D1a | -0.05846 log renta media de contratos nuevos | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D1a-01-H1a-contratos (explorato | V9-D1a | -0.0625 log contratos nuevos | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D1b-02-H1b-renta | V9-D1b | -0.05851 log renta media de contratos nuevos | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D1b-03-H1b-contratos (explorato | V9-D1b | -0.01317 log contratos nuevos | C4 | solo estimación puntual | tamaño real 21.6 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D1c-04-exploratoria | V9-D1c | -0.02484 log renta media de contratos nuevos | C4 | p = 0; IC 95 % [-0.03519; -0.01449] | sin medir | con reserva (distorsión sin medir) | 0 |  |  |
| V9 | V9-D1c-05-exploratoria | V9-D1c | -0.06151 log contratos nuevos | C4 | p = 0.03; IC 95 % [-0.1194; -0.00361] | sin medir | con reserva (distorsión sin medir) | 0.03 |  |  |
| V9 | V9-D2-06-H2-renta-covid (explorat | V9-D2 | 0.00219 log renta media de contratos nuevos (covid; por 1 DE de dosi | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D2-07-H2-renta-reapertura (exp | V9-D2 | 0.01046 log renta media de contratos nuevos (reapertura; por 1 DE de | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D2-08-H2-contratos-covid (expl | V9-D2 | 0.01008 log contratos nuevos (covid; por 1 DE de dosis) | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D2-09-H2-contratos-reapertura  | V9-D2 | 0.01263 log contratos nuevos (reapertura; por 1 DE de dosis) | C4 | solo estimación puntual | tamaño real 20.3 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D3-10-descriptiva | V9-D3 | 0.00205 d_cuota ~ ΔVUT por 100 viviendas | C4 | p = 0.34; IC 95 % [-0.00216; 0.00625] | tamaño real 9.6 % al 5 % nominal | publicable | 0.34 |  |  |
| V9 | V9-D3-11-descriptiva | V9-D3 | -0.00195 d_lmedia ~ ΔVUT por 100 viviendas | C4 | p = 0.0804; IC 95 % [-0.00413; 0.00024] | tamaño real 9.6 % al 5 % nominal | publicable | 0.161 |  |  |
| V9 | V9-D4-12-H4-réplica-alquiler (exp | V9-D4 | 0.00723 Δ log IPC de alquiler (principal (réplica 2003-2012)) | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D4-13-H4-réplica-alquiler (exp | V9-D4 | 0.00442 Δ log IPC de alquiler (principal (réplica 2003-2012) · endóg | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D4-14-exploratoria | V9-D4 | -0.00286 Δ log valor tasado (principal (réplica 2003-2012)) | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D4-15-exploratoria (efecto tot | V9-D4 | -0.00165 Δ log valor tasado (principal (réplica 2003-2012) · endógena | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D4-16-H4-réplica-alquiler (exp | V9-D4 | 0.01525 Δ log IPC de alquiler (ampliación 2015-2022) | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D4-17-exploratoria | V9-D4 | 0.1288 Δ log valor tasado (ampliación 2015-2022) | C4 | solo estimación puntual | tamaño real 21.9 % al 5 % nominal | no fiable |  |  |  |
| V9 | V9-D5-18-exploratoria | V9-D5 | -0.05251 Δ log precio (h = 4) por shock × 1 DE de exposición | C4 | p = 0.322; IC 95 % [-0.1563; 0.0513] | sin medir | con reserva (distorsión sin medir) | 0.965 |  |  |
| V9 | V9-D5-19-exploratoria | V9-D5 | -0.04389 Δ log precio (h = 8) por shock × 1 DE de exposición | C4 | p = 0.513; IC 95 % [-0.1754; 0.08759] | sin medir | con reserva (distorsión sin medir) | 0.965 |  |  |
| V9 | V9-D5-20-exploratoria | V9-D5 | -0.1168 Δ log alquiler (h = 4) por shock × 1 DE de exposición | C4 | p = 7e-05; IC 95 % [-0.174; -0.05962] | sin medir | con reserva (distorsión sin medir) | 0.00028 |  |  |
| V9 | V9-D5-21-exploratoria | V9-D5 | -0.06561 Δ log alquiler (h = 8) por shock × 1 DE de exposición | C4 | p = 0.332; IC 95 % [-0.1981; 0.0669] | sin medir | con reserva (distorsión sin medir) | 0.965 |  |  |
| V9 | V9-D7 | V9-D7 |  | C4 (contable) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V9 | V9-D6 | V9-D6 |  | no estimado | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-f0 | V12-f0 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b1 | V12-b1 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b2 | V12-b2 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b3 | V12-b3 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b4 | V12-b4 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b5 | V12-b5 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b6 | V12-b6 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
| V12 | V12-b7 | V12-b7 |  | C1/C4 (contable o descriptivo) | solo estimación puntual | sin medir | no recalculado (ya tenía inferencia o es contable) |  |  |  |
