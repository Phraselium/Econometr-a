# wild_webb_v15 · wild cluster bootstrap de Webb

Herramienta de V15 (preregistro_v15.md H1/H2 «pocos clusters con wild cluster bootstrap de pesos Webb», sección 6; adenda 1 punto 5 y adenda 2 B). Código: `src/v15/montecarlo/wild_webb_v15.py` (usa `_comun_panel_v15`, `sdid_placebo_h1h2.estructura_s4` y `akm_municipal`); semilla `SeedSequence([20261010, 8, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **W1 (H1/H2):** 124 tratados de la cohorte 2024T1 y 74 nunca tratados (códigos y centroides reales de Incasòl/geo), 7 trimestres previos y 9 posteriores; clusters = municipio (G = 198). Resultado simulado con el proceso de `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial de 25 km, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). Efecto en los 9 trimestres posteriores de los tratados: nulo = 0; referencia = −0,05 con tau_i = tau(1 + 0,5 z_i); MDE80 = −0,022. Estimador: MCO con efectos de municipio y trimestre (TWFE) del indicador tratado × posterior (el estimador del pre-registro es SDID/CS; aquí se valida la inferencia de Webb, que es común a los tres).
- **W2 (H4):** estructura de `akm_municipal` (1.451 municipios, 28 orígenes, cuotas 2003 reales, T = 11, provincia × año absorbidos), clusters = provincia (G = 38, muy desiguales: la más grande concentra ≈ 10 % de los municipios). Forma reducida y_it = β_rf z_it + ε_it con el error con dependencia por cuota y factor común de `akm_municipal` (σ_y = 0,05). Nulo β_rf = 0; referencia β_rf = 0,004 (≈ 0,01 × primera etapa 0,39); MDE 0,003.
- **W3 (R-IPVA, adenda 2 B):** 124 municipios tratados y 382 donantes (estructura de S4 de `sdid_placebo_h1h2`: tratados en las pocas provincias con zona, donantes en provincias sin zona), 9 años previos y 1 posterior; clusters = provincia (G ≈ 36, de ellos ≈ 5 tratados: pocos clusters tratados). Mismo proceso de S4 (choque provincia-año AR(1)). Efecto de referencia −0,02, MDE −0,04. TWFE con efectos de municipio y año.
- **Inferencias comparadas:** (a) wild cluster bootstrap-t de Webb (6 puntos) con nulo impuesto (WCR) para el contraste y no impuesto (WCU) para el IC95 percentil-t; (b) error agrupado CR1 con t(G − 1) como referencia. B = 9.999 réplicas bootstrap (como en V15; el cierre algebraico por cluster hace barato usar más de 999) y, como sensibilidad, B = 999 con las primeras 999 columnas.
- **Cierre algebraico:** como el efecto fijo de unidad está anidado en el cluster, el estadístico bootstrap se calcula sobre sumas por cluster (sin rehacer la regresión por réplica); es exactamente la regresión bootstrap con los residuos reponderados (Roodman et al., 2019), con los efectos de tiempo recentrados.
- **Medidas:** tamaño (rechazo de β = 0 con tau = 0), cobertura del IC95 bajo la referencia (verdad = ATT muestral en W1 y W3, β_rf en W2), potencia (referencia y MDE), sesgo y RMSE. R = 2.000.
- **Criterio:** tamaño en [0,04; 0,06] y cobertura en [0,92; 0,97] para Webb. El pre-registro no nombra alternativa; si falla, «NO APTO → inferencia solo descriptiva».

<!-- RESULTADOS -->
## Resultados (R = 2000 por etapa; B = 9999; semilla 20261010, k = 8)

| escenario | inferencia | G | R | tamano_5pct | cobertura_95 | potencia_ref | potencia_mde | sesgo | rmse | ancho_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| W1_H1H2_198municipios | Webb WCR/WCU B=9999 | 198 | 2000 | 0.2155 | 0.7740 | 0.9860 | 0.7100 | -0.0004 | 0.0141 | 0.0319 |
| W1_H1H2_198municipios | Webb B=999 | 198 | 2000 | 0.2135 | 0.7735 | 0.9860 | 0.7110 | -0.0004 | 0.0141 | 0.0319 |
| W1_H1H2_198municipios | CR1 t(G-1) | 198 | 2000 | 0.2165 | 0.7735 | 0.9865 | 0.7140 | -0.0004 | 0.0141 | 0.0318 |
| W2_H4_38provincias | Webb WCR/WCU B=9999 | 38 | 2000 | 0.4240 | 0.6350 | 0.5165 | 0.4980 | 0.0001 | 0.0062 | 0.0136 |
| W2_H4_38provincias | Webb B=999 | 38 | 2000 | 0.4225 | 0.6330 | 0.5155 | 0.4950 | 0.0001 | 0.0062 | 0.0136 |
| W2_H4_38provincias | CR1 t(G-1) | 38 | 2000 | 0.5495 | 0.4570 | 0.6215 | 0.6030 | 0.0001 | 0.0062 | 0.0083 |
| W3_RIPVA_36provincias_pocos_tratados | Webb WCR/WCU B=9999 | 36 | 2000 | 0.1230 | 0.7760 | 0.3600 | 0.7350 | 0.0005 | 0.0214 | 0.0579 |
| W3_RIPVA_36provincias_pocos_tratados | Webb B=999 | 36 | 2000 | 0.1230 | 0.7780 | 0.3655 | 0.7420 | 0.0005 | 0.0214 | 0.0578 |
| W3_RIPVA_36provincias_pocos_tratados | CR1 t(G-1) | 36 | 2000 | 0.3150 | 0.7120 | 0.5355 | 0.8450 | 0.0005 | 0.0214 | 0.0425 |

**Veredictos (Webb B = 9.999)**

- W1_H1H2_198municipios: **NO APTO → inferencia solo descriptiva**
- W2_H4_38provincias: **NO APTO → inferencia solo descriptiva**
- W3_RIPVA_36provincias_pocos_tratados: **NO APTO → inferencia solo descriptiva**

- W1_H1H2_198municipios / Webb WCR/WCU B=9999: NO APTO — tamaño 0.2155 fuera de [0.04; 0.06]; cobertura 0.7740 fuera de [0.92; 0.97]
- W1_H1H2_198municipios / Webb B=999: NO APTO — tamaño 0.2135 fuera de [0.04; 0.06]; cobertura 0.7735 fuera de [0.92; 0.97]
- W1_H1H2_198municipios / CR1 t(G-1): NO APTO — tamaño 0.2165 fuera de [0.04; 0.06]; cobertura 0.7735 fuera de [0.92; 0.97]
- W2_H4_38provincias / Webb WCR/WCU B=9999: NO APTO — tamaño 0.4240 fuera de [0.04; 0.06]; cobertura 0.6350 fuera de [0.92; 0.97]
- W2_H4_38provincias / Webb B=999: NO APTO — tamaño 0.4225 fuera de [0.04; 0.06]; cobertura 0.6330 fuera de [0.92; 0.97]
- W2_H4_38provincias / CR1 t(G-1): NO APTO — tamaño 0.5495 fuera de [0.04; 0.06]; cobertura 0.4570 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / Webb WCR/WCU B=9999: NO APTO — tamaño 0.1230 fuera de [0.04; 0.06]; cobertura 0.7760 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / Webb B=999: NO APTO — tamaño 0.1230 fuera de [0.04; 0.06]; cobertura 0.7780 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / CR1 t(G-1): NO APTO — tamaño 0.3150 fuera de [0.04; 0.06]; cobertura 0.7120 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto:** W1_H1H2_198municipios: NO APTO → inferencia solo descriptiva; W2_H4_38provincias: NO APTO → inferencia solo descriptiva; W3_RIPVA_36provincias_pocos_tratados: NO APTO → inferencia solo descriptiva.
- El bootstrap de Webb es algebraicamente correcto (comprobado contra la regresión bootstrap explícita en tests/v15/test_mc_v15.py) y B = 9.999 no cambia nada frente a B = 999 (tamaño 0,2155 frente a 0,2135 en W1). Lo que falla es el supuesto de cluster: con 198 municipios (W1) el tamaño es 0,215 (el error agrupado CR1 da 0,216); con 38 provincias y dependencia por cuotas (W2) 0,424 (CR1: 0,549); con ≈ 5 provincias tratadas de 36 (W3) 0,123 (CR1: 0,315).
- **Interpretación:** Webb mejora a CR1 cuando hay pocos clusters (W3: de 0,315 a 0,123) pero no corrige la dependencia entre clusters (correlación espacial y por cuotas del proceso generador). Para H1/H2 y H4 no puede ser la inferencia que sostenga C3 si la dependencia entre clusters es del orden del proceso declarado.
