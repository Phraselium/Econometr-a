# westerlund_csardl · E1: Westerlund con bootstrap, CIPS y CS-ARDL (N = 40, T = 98, factor común)

Herramienta de V15 (preregistro_v15.md E1 y sección 6). Código: `src/v15/montecarlo/westerlund_csardl.py`; semilla `SeedSequence([20261010, 6, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de E1):** N = 40 provincias de entrenamiento (41 con IPC de alquiler; 38 con valor tasado), T = 98 trimestres (alquiler desde 2002T1 hasta 2026T2); 50 trimestres de rodaje descartados.
- **Regresor (log IPC de alquiler simulado), I(1) con factor común:** Δx_it = 0,2 + 0,5 γx_i f1_t + u_it, con f1 AR(1) (ρ = 0,5), γx_i ~ N(1; 0,5²) y u_it = e_it + 0,25 (e_{i−1,t} + e_{i+1,t}) (correlación espacial en anillo; e ~ N(0; 0,8²)).
- **Resultado (log valor tasado simulado):** y_it = β_i x_it + z_it, con β_i ~ N(0,8; 0,2²) (elasticidad de largo plazo por unidad; la verdad es su media muestral) y z_it = ρ_i z_{i,t−1} + 0,5 c_i f2_t + 0,7 e'_it (f2 segundo factor común AR(1) con ρ = 0,5 en las innovaciones, c_i ~ N(1; 0,5²), e' con el mismo anillo espacial). El factor común entra en las innovaciones (incrementos persistentes, como el crecimiento del precio), no como componente estacionario de nivel.
- **Nota de revisión (declarada):** la primera versión del proceso añadía además un componente estacionario de nivel λ_i f2_t en y_it. Eso crea una raíz de media móvil negativa en Δy, que ningún contraste tipo ADF con un rezago maneja (distorsión de tamaño conocida) y no se parece al crecimiento observado del precio (autocorrelación positiva). Con esa versión el tamaño del bootstrap de Westerlund salió 0,56 (Gτ), 0,72 (Gα), 0,50 (Pτ) y 0,65 (Pα), el de CIPS 0,0125 y la cobertura de CS-ARDL 0,9925. Se sustituyó por el proceso anterior de este párrafo antes de interpretar nada más; ambos resultados se declaran aquí.
  - **Nulo (sin cointegración):** ρ_i = 1 (z es I(1): regresión espuria con dependencia transversal).
  - **Alternativa (cointegración):** ρ_i = 1 + α_i con α_i ~ U(−0,06; −0,02), media −0,04 (velocidad de ajuste trimestral de referencia del pre-registro; semivida ≈ 17 trimestres).
- **Westerlund (2007):** modelo de corrección de errores por unidad Δy_s = δ_i + α_i y_{s−1} + λ_i x_{s−1} + a_i Δy_{s−1} + b_i Δx_s + b'_i Δx_{s−1} + e (1 rezago, sin adelantos) y estadísticos Gτ, Gα, Pτ, Pα (agrupados con las variables auxiliares eliminadas por unidad). **Valores p por bootstrap de Westerlund:** VAR(1) de (Δy, Δx) por unidad bajo el nulo; remuestreo de los residuos con el MISMO índice temporal para todas las unidades (conserva la dependencia transversal), reconstrucción en niveles y recálculo; contraste de cola izquierda; B = 99 réplicas (con B = 99 el contraste al 5 % es exacto: rango ≥ 95 de 100). El estadístico principal declarado es **Gτ** (admite heterogeneidad); los otros tres se reportan.
- **CIPS (Pesaran 2007):** CADF con intercepto, 1 rezago y medias transversales, media de los t. **Tamaño:** sobre la serie x (I(1) con factor), en todas las réplicas. **Potencia:** panel estacionario con φ_i ~ U(0,94; 0,98) (velocidad de ajuste media −0,04) con factor común, 1.000 réplicas. Valor crítico por bootstrap de bloques móviles de las diferencias (conjunto entre unidades, longitud 9), B = 199, raíz unitaria impuesta.
- **CS-ARDL (Chudik-Pesaran 2015):** ARDL(1,1) por unidad aumentado con las medias transversales de y y x y sus 4 rezagos (⌊T^(1/3)⌋); elasticidad de largo plazo θ = media de (b0 + b1)/(1 − φ) y velocidad de ajuste media φ − 1, sobre la alternativa (cointegración). Inferencia: bootstrap de bloques móviles (longitud 9) de las filas de regresión conjuntas, B = 99, IC normal con EE bootstrap. Cobertura de la media muestral de β_i y de la velocidad media verdadera; tamaño = 1 − cobertura.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (Gτ, CIPS) y cobertura del IC95 de CS-ARDL en [0,92; 0,97]. Umbral de V15: potencia de Westerlund (Gτ) frente a −0,04 ≥ 0,5; si no, E1 solo descriptiva (independiente del veredicto de tamaño). El pre-registro no nombra inferencia alternativa para estas herramientas: si no pasan, «NO APTO → solo descriptivo».

<!-- RESULTADOS -->
## Resultados (R = 2000 nulo, 1000 alternativa; B Westerlund = 99, B CIPS = 199; semilla 20261010, k = 6)

| herramienta | R_nulo | tamano_5pct | R_alt | potencia_alpha_-0.04 | cobertura_95 | sesgo | rmse |
|---|---|---|---|---|---|---|---|
| Westerlund Gtau | 2000 | 0.1355 | 1000 | 0.3380 | nan | nan | nan |
| Westerlund Galpha | 2000 | 0.0930 | 1000 | 0.3350 | nan | nan | nan |
| Westerlund Ptau | 2000 | 0.1965 | 1000 | 0.4070 | nan | nan | nan |
| Westerlund Palpha | 2000 | 0.1810 | 1000 | 0.4590 | nan | nan | nan |
| CIPS (serie I(1)) | 2000 | 0.0105 | 1000 | 0.0780 | nan | nan | nan |
| CS-ARDL elasticidad de largo plazo | 2000 | 0.0075 | 2000 | 0.2045 | 0.9925 | -0.0187 | 1.1579 |
| CS-ARDL velocidad de ajuste media | 2000 | 0.9970 | 2000 | 1.0000 | 0.0030 | -0.1250 | 0.1262 |

**Umbral de V15:** potencia de Gτ frente a α = −0,04: 0.338 → E1 solo DESCRIPTIVA.

**Veredictos de tamaño/cobertura**

- Westerlund Gtau: **NO APTO → solo descriptivo** tamaño 0.1355 fuera de [0.04; 0.06]
- Westerlund Galpha: **NO APTO → solo descriptivo** tamaño 0.0930 fuera de [0.04; 0.06]
- Westerlund Ptau: **NO APTO → solo descriptivo** tamaño 0.1965 fuera de [0.04; 0.06]
- Westerlund Palpha: **NO APTO → solo descriptivo** tamaño 0.1810 fuera de [0.04; 0.06]
- CIPS (serie I(1)): **NO APTO → solo descriptivo** tamaño 0.0105 fuera de [0.04; 0.06]
- CS-ARDL elasticidad de largo plazo: **NO APTO → solo descriptivo** tamaño 0.0075 fuera de [0.04; 0.06]; cobertura 0.9925 fuera de [0.92; 0.97]
- CS-ARDL velocidad de ajuste media: **NO APTO → solo descriptivo** tamaño 0.9970 fuera de [0.04; 0.06]; cobertura 0.0030 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Umbral de V15:** la potencia de Westerlund (Gτ, bootstrap, B = 99) frente a una velocidad de ajuste de −0,04 trimestral es **0,338** (Gα 0,335, Pτ 0,407, Pα 0,459), menor que 0,5 en los cuatro estadísticos: **E1 se reporta solo como descriptiva**, con independencia del tamaño.
- **Tamaño:** Gτ 0,136, Gα 0,093, Pτ 0,197, Pα 0,181: el bootstrap (VAR(1) por unidad, remuestreo temporal conjunto) sobre-rechaza con N = 40, T = 98 y raíces cercanas a la unidad; la potencia queda inflada por ese sobre-rechazo. **CIPS** con bootstrap de bloques es conservador (0,0105) y con potencia 0,078 frente a φ ≈ 0,96.
- **CS-ARDL:** la elasticidad de largo plazo tiene RMSE 1,158 (frente a una elasticidad de 0,8: el cociente (b0+b1)/(1−φ) es inestable por unidad) y cobertura 0,993 (IC enormes); la **velocidad de ajuste** media sale sesgada en -0,125 (verdad −0,04) con cobertura 0,0030: el ARDL(1,1) con las medias transversales de y y x y sus 4 rezagos (14 regresores con 94 observaciones) probablemente absorbe la tendencia común (ȳ y x̄ están casi colineales) y estima la reversión de la desviación respecto a la media, no la del nivel; no se ha contrastado esta explicación.
- **Veredictos:** ver lista anterior: ninguna herramienta pasa. La adenda no nombra alternativa para estas herramientas.
