# dfm_bvar_mcs · H5: combinación DFM + BVAR + LASSO + ARDL frente al AR(4); DM-HLN, GW, CW y MCS

Herramienta de V15 (preregistro_v15.md H5 y sección 6; adenda 1 puntos 8 y 16). Código: `src/v15/montecarlo/dfm_bvar_mcs.py`; semilla `SeedSequence([20261010, 5, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de H5):** 94 trimestres (2003T1-2026T2), ventana expansiva desde el trimestre 22, de modo que hay **73 errores fuera de muestra** a horizonte 1; 20 indicadores «mensuales agregados al trimestre».
- **Factores y dependencia:** 2 factores comunes F_t = 0,7 F_{t−1} + u_t (u ~ N(0, I)). Indicadores x_jt = λ_j'F_t + 0,7 η_jt con cargas λ ~ N(0,1) sorteadas por réplica.
- **Variables del BVAR (6):** objetivo g_t (Δlog valor tasado), compraventas c_t = 0,6 F1_t + 0,8 ε, hipotecas h_t = 0,5 F2_t + 0,8 ε, ocupados o_t AR(1) ρ = 0,5, tipo AR(1) ρ = 0,9 e inflación AR(1) ρ = 0,8.
- **Objetivo:** g_t = 0,1 + Σ_{l=1..4} φ_l g_{t−l} + δ (0,7 F1_{t−1} + 0,7 F2_{t−1}) + ε_t, ε ~ N(0,1), φ = (0,3; 0,25; 0,2; 0,1) (AR(4) con memoria larga: los cuatro rezagos importan, de modo que los modelos más parsimoniosos de la combinación pierden precisión si no hay señal; con φ de memoria corta la combinación ya mejora al AR(4) sin señal, porque el AR(4) con 21 observaciones iniciales está mal estimado, y no existe un δ ≥ 0 de igual precisión); δ controla la señal de los indicadores.
- **Modelos (re-estimados en cada origen con la ventana expansiva):**
  - AR(4) (línea base).
  - DFM: 2 componentes principales de los 20 indicadores estandarizados + g_t, regresión directa a h = 1.
  - BVAR de Minnesota de 6 variables con 2 rezagos, media a priori 0, tightness λ = 0,2, decaimiento 1/l², escala de varianzas por AR(1) univariantes; media posterior de la ecuación de g (la verosimilitud marginal de Giannone-Lenza-Primiceri de la adenda se sustituye por λ fijo: coste; se declara).
  - LASSO: g_t y 20 indicadores, λ por BIC (LassoLarsIC; la validación temporal con embargo de la adenda se sustituye por BIC por coste).
  - ARDL: rezagos de g (1-4) y de c y h (1-4), orden por BIC.
  - Combinación = media simple de los 4 pronósticos.
- **Escenarios de señal:** δ = 0 (AR(4) es el proceso verdadero: nulo de Clark-West); δ* = el valor que iguala en media el ECM de la combinación y del AR(4) con n = 94 (nulo de igual precisión finita de Diebold-Mariano; calibrado con 300 réplicas por punto de una rejilla, semillas comunes; δ* hace cero la media de la diferencia de pérdidas); δ_20 = el que reduce un 20 % la razón entre los ECM medios (potencia; el pre-registro cita MDE del 18-30 %).
- **Pruebas** (combinación frente a AR(4), pérdida cuadrática, h = 1): DM-HLN unilateral (varianza de largo plazo = γ0 porque h = 1; t de Student con P − 1 gl); Giacomini-White condicional con instrumentos (1, d_{t−1}), χ²(2) (su hipótesis nula es condicional: bajo δ* solo es la igualdad incondicional, se reporta como diagnóstico); Clark-West unilateral normal.
- **MCS (Hansen-Lunde-Nason), tamaño:** proceso de pérdidas con 6 modelos (los 5 del pre-registro + AR(4)) con igualdad de precisión por construcción: errores e_mt = s_t √ρ-correlación 0,8 con t de 8 grados de libertad y volatilidad común log-AR(1) (ρ = 0,7, sd 0,3); pérdida cuadrática; P = 73. Estadístico T_max, bootstrap de bloques móviles (longitud 4, 999 réplicas), regla de eliminación e_max; tamaño = prob. de que el MCS excluya algún modelo.
- **R = 2.000** réplicas bajo cada nulo. **Criterio:** tamaño del DM-HLN, de CW (bajo δ = 0) en [0,04; 0,06]; para el MCS al 10 % la banda es [0,08; 0,12] (análoga, declarada aquí) y al 5 % [0,04; 0,06]. No hay IC: no hay cobertura. El pre-registro no nombra alternativa distinta de GW y CW; si DM-HLN no pasa y CW pasa, «alternativa APTA (CW)»; si ninguna pasa, «NO APTO → contraste solo descriptivo».

<!-- RESULTADOS -->
## Resultados (R = 2000 bajo cada nulo; semilla 20261010, k = 5)

Calibración: δ* = 0.338; δ_20 = 0.769. Rejilla (diferencia media de pérdidas y razón de ECM medios con 300 réplicas): {'dbar_media': {0.0: -0.10027667713390669, 0.15: -0.08492132091600865, 0.3: -0.027048007604417848, 0.45: 0.08012845717508785, 0.6: 0.2235962810316844, 0.8: 0.46353984510640667, 1.0: 0.7515143966991809, 1.3: 1.2647284232139502}, 'razon_ECM_medios': {0.0: 1.086261552781152, 0.15: 1.070505219034923, 0.3: 1.0202388797576682, 0.45: 0.9476290142617368, 0.6: 0.8740179100579435, 0.8: 0.786556318341988, 1.0: 0.7159999290816585, 1.3: 0.6394765255901291}}

| escenario | delta | R | ratio_ECM_medio | dif_perdida_media | rechazo_DM_HLN | rechazo_GW_cond | rechazo_CW | rechazo_DM_HLN_10pct |
|---|---|---|---|---|---|---|---|---|
| nulo_AR4_verdadero (delta=0) | 0.0000 | 2000 | 1.0860 | -0.0968 | 0.0035 | 0.0630 | 0.1895 | 0.0085 |
| nulo_igual_ECM (delta*) | 0.3379 | 2000 | 0.9975 | 0.0090 | 0.0545 | 0.0310 | 0.6950 | 0.1060 |
| alt_ECM_-20% (delta_20) | 0.7693 | 1000 | 0.7938 | 0.4496 | 0.5800 | 0.3050 | 0.9950 | 0.7600 |

**MCS (pérdidas con igualdad de precisión, 6 modelos, P = 73):** {'tamano_mcs_10pct': 0.123, 'tamano_mcs_5pct': 0.0575, 'R': 2000, 'tam_medio_conjunto_10': 5.8335}

**Veredicto DM/CW: APTO (DM-HLN).** **Veredicto MCS: NO APTO → MCS solo descriptivo.**

- DM-HLN: APTO 
- CW (δ = 0): NO APTO tamaño 0.1895 fuera de [0.04; 0.06]
- GW: NO APTO tamaño 0.0310 fuera de [0.04; 0.06]
- MCS 10 %: NO APTO tamaño 0.1230 fuera de [0.08; 0.12]
- MCS 5 %: APTO

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto DM/CW:** APTO (DM-HLN). Con el nulo de igual ECM esperado (δ* = 0,338), el DM-HLN unilateral con 73 errores tiene tamaño 0,0545 (dentro de [0,04; 0,06]) y potencia 0,580 frente a una reducción del 20 % del ECM (el MDE del pre-registro es del 18-30 %: la potencia es moderada, no alta). Con el AR(4) como proceso verdadero (δ = 0) la combinación es peor en media y el DM unilateral casi nunca rechaza (tamaño 0,0035), como corresponde.
- **Clark-West no es utilizable** para la combinación frente al AR(4): rechaza el 0,190 de las veces cuando el AR(4) es el proceso verdadero (la combinación de modelos no anidados con parámetros estimados no cumple la teoría de modelos anidados). **GW** condicional: tamaño 0,031 bajo igualdad incondicional; solo diagnóstico (su nulo es condicional).
- **MCS** (6 modelos, P = 73, igualdad de precisión por construcción): tamaño 0,1230 al 10 % (banda declarada [0,08; 0,12]; supera el límite por 0,003, dentro de un error de Monte Carlo de ≈ 0,007: **NO APTO en el límite**) y 0,0575 al 5 % (dentro de [0,04; 0,06]). El veredicto del MCS es NO APTO → MCS solo descriptivo; la decisión depende de la banda declarada para el 10 %, y por eso H5 debe leerse con el MCS al 5 % como comprobación.
- **Alcance:** esta validación cubre el tamaño de las pruebas con los modelos sustituidos por proxies declarados (λ de Minnesota fijo en lugar de GLP; BIC en lugar de validación temporal con embargo) y ventana expansiva; no valida la elección de la línea base de K1.
