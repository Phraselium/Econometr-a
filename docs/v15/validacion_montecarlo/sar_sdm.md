# sar_sdm · E3: SAR, SEM y SDM con W de contigüidad y de distancia inversa (corte 25 km)

Herramienta de V15 (preregistro_v15.md E3 y sección 6; adenda 1 punto 18: periodos 2011-2019 y 2015-2024). Código: `src/v15/montecarlo/sar_sdm.py`; semilla `SeedSequence([20261010, 7, celda*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Estructura leída (códigos y geometría; ningún valor de resultado):** municipios de entrenamiento con SERPAVI en 2015 y en 2024 (corte transversal de Δlog 2015-2024; N ≈ 1.900 tras quitar los que no tienen vecinos), polígonos de `data/base/geo`.
  - **W de contigüidad (reina):** polígonos que comparten frontera o vértice, estandarizada por filas.
  - **W de distancia inversa con corte de 25 km:** w_ij = 1/d_ij si d_ij < 25 km (distancia entre centroides), estandarizada por filas.
  - Se descartan las islas (sin vecino en alguna de las dos matrices) para que ambas matrices usen la misma muestra.
- **Covariables fijas:** x1 y x2 = (I − 0,5 W)^(-1) N(0,1) estandarizadas (autocorrelación espacial moderada, como cualquier covariable municipal), constante; β = (0; 0,5; −0,3). X se fija en todas las réplicas (inferencia condicional en X).
- **Procesos:**
  - SAR: y = ρ W y + X β + ε.
  - SEM: y = X β + u, u = λ W u + ε.
  - SDM: y = ρ W y + X β + W X θ + ε, con θ = (0,3; −0,2).
  - Nulo: ρ = λ = 0 (en el SDM, ρ = 0 y θ = 0, de modo que el efecto indirecto es 0). Alternativa: ρ = λ = 0,4.
- **Errores:** ε_i ~ N(0, σ_i²). Escenario «heterocedástico» (principal): σ_i = exp(0,4 z_i − 0,08) con z_i ~ N(0,1) (heterogeneidad entre municipios); escenario «homocedástico» (diagnóstico): σ_i = 1.
- **Estimación:** máxima verosimilitud concentrada con log-determinante exacto por autovalores de W. Contrastes sobre ρ (λ): Wald con la curvatura numérica de la verosimilitud perfilada y razón de verosimilitudes (referencia). Moran de los residuos MCO con la media y la varianza exactas de Cliff-Ord para residuos de regresión.
- **Efectos (LeSage-Pace) en SAR y SDM para x1:** efecto directo = media de la diagonal de S(W), total = suma/N, indirecto = total − directo; trazas hasta el orden 60 de W; 1.000 simulaciones de (ρ, β[, θ]) de la normal con la covarianza del método delta (β(ρ) = b0 − ρ bL) y IC percentil. La verdad es el valor analítico en los parámetros del proceso. Tamaño del efecto indirecto bajo el nulo = rechazo de que el IC95 contiene 0.
- **R = 3.000 por celda.** Criterio: tamaño de las pruebas sobre ρ en [0,04; 0,06] y cobertura del IC95 de los efectos indirectos y de ρ en [0,92; 0,97] (escenario heterocedástico; el homocedástico es diagnóstico). El pre-registro no nombra alternativa para estas pruebas distinta de los errores de Conley sobre los coeficientes (fuera de este encargo).

<!-- RESULTADOS -->
## Resultados (R = 3000 por celda; N = 1483; semilla 20261010, k = 7)

| W | modelo | errores | R | tamano_wald_rho | tamano_lr_rho | tamano_moran | cobertura_rho | potencia_wald_rho | sesgo_rho | rmse_rho | tamano_indirecto | cobertura_indirecto | cobertura_directo | potencia_indirecto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contigüidad | SAR | hetero | 3000 | 0.0550 | 0.0543 | 0.0530 | 0.9413 | 1.0000 | -0.0024 | 0.0244 | 0.0547 | 0.9447 | 0.9570 | 1.0000 |
| contigüidad | SAR | homo | 3000 | 0.0497 | 0.0497 | 0.0513 | 0.9493 | 1.0000 | -0.0019 | 0.0232 | 0.0533 | 0.9487 | 0.9500 | 1.0000 |
| contigüidad | SDM | hetero | 3000 | 0.0453 | 0.0453 | 0.0443 | 0.9527 | 1.0000 | -0.0023 | 0.0251 | 0.0517 | 0.9437 | 0.9507 | 1.0000 |
| contigüidad | SDM | homo | 3000 | 0.0537 | 0.0533 | 0.0517 | 0.9513 | 1.0000 | -0.0028 | 0.0253 | 0.0563 | 0.9443 | 0.9373 | 1.0000 |
| contigüidad | SEM | hetero | 3000 | 0.0487 | 0.0483 | 0.0473 | 0.9450 | 1.0000 | -0.0013 | 0.0264 | nan | nan | nan | nan |
| contigüidad | SEM | homo | 3000 | 0.0553 | 0.0553 | 0.0560 | 0.9527 | 1.0000 | -0.0032 | 0.0261 | nan | nan | nan | nan |
| dist_inversa_25km | SAR | hetero | 3000 | 0.0483 | 0.0477 | 0.0507 | 0.9483 | 1.0000 | -0.0043 | 0.0349 | 0.0470 | 0.9400 | 0.9447 | 1.0000 |
| dist_inversa_25km | SAR | homo | 3000 | 0.0503 | 0.0497 | 0.0457 | 0.9453 | 1.0000 | -0.0042 | 0.0341 | 0.0503 | 0.9433 | 0.9380 | 1.0000 |
| dist_inversa_25km | SDM | hetero | 3000 | 0.0550 | 0.0547 | 0.0497 | 0.9333 | 1.0000 | -0.0083 | 0.0394 | 0.0493 | 0.9460 | 0.9510 | 1.0000 |
| dist_inversa_25km | SDM | homo | 3000 | 0.0547 | 0.0557 | 0.0507 | 0.9507 | 1.0000 | -0.0058 | 0.0375 | 0.0543 | 0.9457 | 0.9460 | 1.0000 |
| dist_inversa_25km | SEM | hetero | 3000 | 0.0547 | 0.0540 | 0.0523 | 0.9457 | 1.0000 | -0.0053 | 0.0396 | nan | nan | nan | nan |
| dist_inversa_25km | SEM | homo | 3000 | 0.0547 | 0.0547 | 0.0520 | 0.9500 | 1.0000 | -0.0056 | 0.0385 | nan | nan | nan | nan |

**Veredicto: APTO.**

- SAR|contigüidad: ρ APTO  | indirecto APTO 
- SDM|contigüidad: ρ APTO  | indirecto APTO 
- SEM|contigüidad: ρ APTO  | indirecto n/a 
- SAR|dist_inversa_25km: ρ APTO  | indirecto APTO 
- SDM|dist_inversa_25km: ρ APTO  | indirecto APTO 
- SEM|dist_inversa_25km: ρ APTO  | indirecto n/a

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto: APTO** en las seis combinaciones modelo × W del escenario heterocedástico (R = 3.000 por celda, N = 1483).
- Tamaño del Wald sobre ρ (λ) entre 0,045 y 0,055; razón de verosimilitudes entre 0,045 y 0,055; Moran de los residuos entre 0,044 y 0,053. Cobertura del IC de ρ entre 0,933 y 0,953; del efecto indirecto entre 0,940 y 0,946; del directo entre 0,945 y 0,957; tamaño del efecto indirecto bajo el nulo entre 0,047 y 0,055. Sesgo de ρ ≤ 0,008 en valor absoluto.
- **Límites de la validación:** el proceso generador es el modelo bien especificado con la W verdadera, errores normales con heterocedasticidad moderada y X fija; no cubre una W equivocada ni una dependencia no espacial (factor común, tendencia regional), que es la amenaza más probable en datos reales. El resultado habilita las herramientas bajo esos supuestos; la sensibilidad a la elección de W queda para la fase de estimación (los dos W del pre-registro).
