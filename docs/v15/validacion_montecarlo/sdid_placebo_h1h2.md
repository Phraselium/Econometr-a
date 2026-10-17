# sdid_placebo_h1h2 · SDID con placebo (H1/H2) y variante IPVA (adenda 2, B)

Herramienta de V15 (preregistro_v15.md sección 6; adenda 1 punto 13). Código: `src/v15/montecarlo/sdid_placebo_h1h2.py` y `_comun_panel_v15.py`; semilla `SeedSequence([20261010, 1, escenario*10+etapa]).spawn(R)` (una réplica = un generador).

## Proceso generador (declarado antes de simular)
**Estructura leída (códigos, calendario, geometría; ningún valor de resultado):** municipios catalanes de entrenamiento con renta de Incasòl (611), cohortes de `regulacion_zonas` (2024T1: 128; 2024T4: 113; nunca tratados: 370) y centroides de `data/base/geo`. Se toman 124 tratados de la cohorte 2024T1 (234 × 128/241, del recuento de la adenda 1) y 74 donantes nunca tratados al azar (el filtro de ≥ 5 contratos no se reproduce porque exigiría leer el número de contratos); la variante de 10 km usa los 14 donantes de esos 74 a ≥ 10 km de cualquier municipio tratado (la adenda cuenta 13).
Calendario (adenda 1, puntos 1 y 6): 7 trimestres previos (2022T2-2023T4; pesos de SDID con los 5 primeros) y 9 posteriores (2024T1-2026T1), ATT = media de los 9.
**Resultado simulado (log):** y_it = mu_i + d_i t + g1_i f1_t + g2_i f2_t + s_it + e_it + efecto.
- mu_i ~ N(0,1); d_i ~ N(0; 0,002²) por trimestre (heterogeneidad de tendencia no relacionada con el tratamiento).
- f1, f2 factores comunes AR(1) con ρ = 0,6 y sd 0,03 (dependencia transversal); g1_i ~ N(1; 0,5²); g2_i = campo espacial exponencial (alcance 60 km) N(0,1).
- s_it: campo espacial exp(-d/25 km), AR(1) ρ = 0,5, sd 0,02 (correlación espacial por distancia entre centroides reales).
- e_it: AR(1) ρ = 0,5 con sd marginal sd_e × exp(0,5 z_i − 0,125) (heterogeneidad entre municipios; sd_e = 0,05 en H1, 0,15 en H2). Valores declarados, no estimados con datos reales.
**Efecto (solo tratados, 9 trimestres posteriores):** nulo = 0. Alternativa de referencia = −0,05 (H1; literatura citada en el pre-registro) y −0,13 (H2), con heterogeneidad tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i). Potencia además frente al MDE80 del pre-registro (−0,022 en H1; −0,039 en H2).
**Escenarios:** S1 (H1, 124 tratados y 74 donantes), S2 (H1, 14 donantes a ≥ 10 km), S3 (H2, 74 donantes, más ruido) y S4 (variante R-IPVA, ver abajo).
**S4 (adenda 2, B):** panel anual 2015-2023 (9 previos) + 2024 (1 posterior), 124 municipios tratados con zona vigente en 2024 (cualquier CCAA, códigos de `regulacion_zonas` presentes en el entrenamiento) y 382 donantes de provincias sin zona (al azar entre los municipios de entrenamiento con SERPAVI); clusters = provincia. Mismo proceso con sd_e = 0,02, más un choque provincia-año AR(1) (ρ = 0,5, sd 0,015), efecto de referencia −0,02 (diluido: el IPVA mide el stock de contratos), MDE −0,04.

## Inferencias
- **Principal (preregistro H1):** error típico por bootstrap de placebo (Arkhangelsky et al., alg. 4), IC normal ± 1,96 SE. En el Monte Carlo B = 99 réplicas de placebo (el pre-registro usa 1.000: se reduce por coste, 45 min; con B = 99 el SE tiene un error relativo ≈ 7 %). El algoritmo literal reasigna N_tr = 124 donantes como tratados: **no es computable con 74 o 14 donantes**. Se reportan dos variantes de diagnóstico con m = N_co/2 placebo-tratados: sin reescalar y reescalada por sqrt(m/N_tr). No cuentan como la inferencia principal.
- **Alternativa nombrada en la adenda 1 (punto 5):** wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDID (pesos fijos; 999 réplicas; nulo impuesto). En S4 es la inferencia especificada (clusters = provincia; adenda 2, B).
- Para S1-S3 la inferencia principal es la del placebo; si no es computable o no pasa, se prueba solo Webb; si tampoco, «NO APTO → diseño solo descriptivo».
- Criterio: tamaño al 5 % en [0,04; 0,06] con R = 2.000 bajo el nulo y cobertura del IC 95 % en [0,92; 0,97] bajo la alternativa de referencia. Potencia, sesgo y RMSE informados.

<!-- RESULTADOS -->
## Resultados (R nulo = 2000, R ref = 2000, R mde = 400; B placebo = 99; Webb 999; semilla 20261010, k = 1)

| escenario | inferencia | efecto | R | R_validas | sesgo | rmse | cobertura | rechazo(tamaño|potencia) | ancho_medio_ic | segundos | provincias_tratadas | provincias_donantes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1_H1_74donantes | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.9515 | 0.0485 | 0.0521 | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.7290 | 0.2710 | 0.0285 | 317.3261 | nan | nan |
| S1_H1_74donantes | webb_cluster | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.7895 | 0.2080 | 0.0319 | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.9430 | 0.9555 | 0.0519 | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.7325 | 0.9910 | 0.0283 | 360.5893 | nan | nan |
| S1_H1_74donantes | webb_cluster | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.8010 | 0.9875 | 0.0331 | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 64.3920 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | mde | 400 | 400 | 0.0005 | 0.0134 | 0.9625 | 0.3875 | 0.0526 | 64.3920 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | mde | 400 | 400 | 0.0005 | 0.0134 | 0.7325 | 0.7125 | 0.0287 | 64.3920 | nan | nan |
| S1_H1_74donantes | webb_cluster | mde | 400 | 400 | 0.0005 | 0.0134 | 0.7800 | 0.6675 | 0.0323 | 64.3920 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.9845 | 0.0155 | 0.1196 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.4950 | 0.5050 | 0.0284 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.7715 | 0.2260 | 0.0524 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.9825 | 0.3610 | 0.1203 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.5210 | 0.9450 | 0.0286 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.8015 | 0.8635 | 0.0534 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | mde | 400 | 400 | 0.0003 | 0.0247 | 0.9725 | 0.0800 | 0.1180 | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | mde | 400 | 400 | 0.0003 | 0.0247 | 0.4425 | 0.6700 | 0.0280 | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | mde | 400 | 400 | 0.0003 | 0.0247 | 0.7600 | 0.4850 | 0.0517 | 84.6788 | nan | nan |
| S3_H2_74donantes | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.9920 | 0.0080 | 0.1337 | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.8640 | 0.1360 | 0.0730 | 508.0531 | nan | nan |
| S3_H2_74donantes | webb_cluster | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.9050 | 0.0930 | 0.0806 | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.9965 | 0.9870 | 0.1333 | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.8650 | 0.9995 | 0.0728 | 622.9112 | nan | nan |
| S3_H2_74donantes | webb_cluster | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.9185 | 0.9995 | 0.0837 | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 94.3444 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | mde | 400 | 400 | -0.0001 | 0.0239 | 0.9900 | 0.1425 | 0.1339 | 94.3444 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | mde | 400 | 400 | -0.0001 | 0.0239 | 0.8675 | 0.5350 | 0.0732 | 94.3444 | nan | nan |
| S3_H2_74donantes | webb_cluster | mde | 400 | 400 | -0.0001 | 0.0239 | 0.9025 | 0.4825 | 0.0812 | 94.3444 | nan | nan |
| S4_IPVA_provincias | webb_cluster | nulo | 2000 | 2000 | 0.0001 | 0.0127 | 0.7170 | 0.2825 | 0.0299 | 46.0487 | 5.0000 | 31.0000 |
| S4_IPVA_provincias | webb_cluster | ref | 2000 | 2000 | 0.0003 | 0.0129 | 0.7145 | 0.6645 | 0.0292 | 45.8063 | 5.0000 | 31.0000 |
| S4_IPVA_provincias | webb_cluster | mde | 400 | 400 | 0.0003 | 0.0128 | 0.7225 | 0.9400 | 0.0294 | 8.3846 | 5.0000 | 31.0000 |

**Veredictos**

- S1_H1_74donantes: **NO APTO → diseño solo descriptivo**
- S2_H1_14donantes_10km: **NO APTO → diseño solo descriptivo**
- S3_H2_74donantes: **NO APTO → diseño solo descriptivo**
- S4_IPVA_provincias: **NO APTO → diseño solo descriptivo**
- S1_H1_74donantes / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S1_H1_74donantes / placebo_m_sin_escalar: APTO 
- S1_H1_74donantes / placebo_m_escalado: NO APTO — tamaño 0.2710 fuera de [0.04; 0.06]; cobertura 0.7325 fuera de [0.92; 0.97]
- S1_H1_74donantes / webb_cluster: NO APTO — tamaño 0.2080 fuera de [0.04; 0.06]; cobertura 0.8010 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S2_H1_14donantes_10km / placebo_m_sin_escalar: NO APTO — tamaño 0.0155 fuera de [0.04; 0.06]; cobertura 0.9825 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / placebo_m_escalado: NO APTO — tamaño 0.5050 fuera de [0.04; 0.06]; cobertura 0.5210 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / webb_cluster: NO APTO — tamaño 0.2260 fuera de [0.04; 0.06]; cobertura 0.8015 fuera de [0.92; 0.97]
- S3_H2_74donantes / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S3_H2_74donantes / placebo_m_sin_escalar: NO APTO — tamaño 0.0080 fuera de [0.04; 0.06]; cobertura 0.9965 fuera de [0.92; 0.97]
- S3_H2_74donantes / placebo_m_escalado: NO APTO — tamaño 0.1360 fuera de [0.04; 0.06]; cobertura 0.8650 fuera de [0.92; 0.97]
- S3_H2_74donantes / webb_cluster: NO APTO — tamaño 0.0930 fuera de [0.04; 0.06]; cobertura 0.9185 fuera de [0.92; 0.97]
- S4_IPVA_provincias / webb_cluster: NO APTO — tamaño 0.2825 fuera de [0.04; 0.06]; cobertura 0.7145 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto por escenario:** S1_H1_74donantes: NO APTO → diseño solo descriptivo; S2_H1_14donantes_10km: NO APTO → diseño solo descriptivo; S3_H2_74donantes: NO APTO → diseño solo descriptivo; S4_IPVA_provincias: NO APTO → diseño solo descriptivo. Condición que falla: el error típico por placebo, tal como lo fija el pre-registro (N_tr = 124 placebo-tratados), **no es computable**: exige más donantes (74 o 14) que tratados (124). Con la inferencia alternativa de la adenda (wild cluster bootstrap de Webb por municipio) el tamaño es 0,208 (S1), 0,226 (S2) y 0,093 (S3), y la cobertura 0,801, 0,801 y 0,918. En la variante R-IPVA (clusters = provincia, ≈ 5 provincias tratadas) el tamaño es 0,282 y la cobertura 0,715.
- **Por qué:** el SDID puntual es insesgado en el proceso (sesgo ≈ 0; RMSE 0,0138 en S1), pero el error típico por municipio subestima la dispersión real (en S1 la anchura media del IC95 de Webb es 0,0331, es decir, un SE de ≈ 0,0085 frente a un RMSE de 0,0138) porque ignora la correlación espacial entre municipios próximos y las cargas factoriales espaciales (campos de 25 y 60 km del proceso generador). Ningún remuestreo por municipio recupera esa dependencia: haría falta agrupar por zona o por distancia.
- **Variantes de diagnóstico del placebo (no cumplen el pre-registro):** con m = N_co/2 placebo-tratados sin reescalar el tamaño es 0,0485 en S1 (dentro del criterio solo por coincidencia: sobrestima el SE en S2 y S3, con 0,0155 y 0,0080); reescalado por √(m/N_tr) el tamaño sube a 0,271. Ninguna variante es robusta a los tres escenarios.
- **Consecuencia para H1/H2 (adenda 1, puntos 2 y 13):** con esta inferencia el SDID no puede sostener C3; el estimador puntual sigue siendo válido como descriptivo. Condicionado a los niveles de ruido declarados (supuestos del proceso, no medidos), el MDE80 que implica el RMSE del estimador es ≈ 3,9 % en renta con 74 donantes (S1), ≈ 6,1 % con los 14 donantes a ≥ 10 km (S2; supera el 5 % de la regla de paso a exploratoria de la adenda) y ≈ 6,7 % en log(1 + contratos) (S3; por debajo del 13 %).
