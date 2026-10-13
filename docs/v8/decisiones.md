# Decisiones V8 (Y = decisión de V8)

- **Y0.** V8 parte de r7.2/main.
  - F0 estaba casi completo en v7.2 (retirada de cifras superadas, dosis de construcción, ficha de burbuja, test). Aquí solo se añade el rótulo del marcador de fecha de publicación.
  - La v7.1 sigue siendo la referencia y la v7.2 es su corrección, con ERRATA.
- **Y1. Capas de V8:**
  - C1: hechos;
  - C2: cotas;
  - C3: identificación por un instrumento externo o por un diseño que supera sus pruebas;
  - C3s: identificación por supuestos estructurales explícitos (restricciones de signo), solo con los supuestos declarados;
  - C4: exploratorio o asociación.
  
  El lenguaje causal solo se admite en C3 y C3s, y en C3s siempre condicionado a los supuestos.
- **Y2.** No está instalada la biblioteca de EBM (interpret). Se usa un GAM con splines de statsmodels (GLMGam) como modelo aditivo interpretable, y no se añade ninguna dependencia nueva.
- **Y3. Uso de las herramientas del grupo B de F3** (output/v8/F3/otros/validacion.md):
  - **Bai-Perron:** bootstrap POR BLOQUES obligatorio, porque con errores AR el wild bootstrap da un tamaño de 0,60.
  - **Número de factores:** con N = 17 CCAA no se elige por Bai-Ng (que con N pequeño elige kmax); se fija en 1 y se reporta la sensibilidad con 2.
  - **Markov switching:** el número de regímenes se elige por BIC (acierto del 80-97 %) y el bootstrap de la razón de verosimilitudes se reporta solo como informativo, por su baja potencia.
  - **Permutación de fechas:** con el estadístico studentizado (tamaño 0,052); su baja potencia se declara.
  - **LP-IV:** se usan siempre los intervalos de Anderson-Rubin, porque el intervalo normal no es fiable con instrumentos débiles.
  - **SHAP agrupado:** solo como contraste. Se reporta la estabilidad del ranking.
- **Y4. Uso de las herramientas del grupo A de F3** (output/v8/F3/var/validacion.md):
  - **BVAR-GLP, con reservas.** El sesgo de las IRF (14-25 %) aparece también con prior plano: es sesgo de muestra finita. La cobertura del 90 % está entre 0,91 y 0,97. Se usa, y se declara que las magnitudes de las IRF pueden estar sesgadas hacia cero; se interpretan con sus bandas.
  - **Restricciones de signo y ceros.** La mecánica es apta: identidad de la descomposición histórica y ceros exactos. Las bandas de los elementos no restringidos son anchas (sobrecobertura): un resultado no restringido solo se lee si su banda excluye el cero.
  - **Pesos ARW.** Son una derivación propia, NO VERIFICADA frente al artículo. Pasan la prueba de invarianza al orden de los shocks. En la principal (signos y ceros) se usan con esa declaración; la variante V3 (solo signos) no los necesita.
  - **TVP-VAR-SV, no apta** para detectar cambios de coeficientes con T de unos 90 (detección del 17 %). M3 usa el VAR por regímenes con los periodos pre-registrados como fechas conocidas (con reservas: cobertura de 0,90 y potencia de 0,64), que es la alternativa prevista en el encargo. La senda TVP-SV se muestra solo para la volatilidad.
- **Y5. Revisión F3: APROBAR CON CORRECCIONES** (docs/v8/revision_F3.md).
  - Las aclaraciones del pre-registro (H11, H16, H10, H9) están en docs/v8/desviaciones.md, antes de estimar.
  - Las correcciones de código (H1, H2, H4-H8, H12-H15, H17, H18) se encargan a dos subagentes. F4 no estima con datos reales hasta que estén hechas y validadas.
- **Y6. Tras las correcciones de la familia VAR** (output/v8/F3/var/validacion.md):
  - **SVAR principal (7 variables, 4 ceros, signos en h = 0-1).** Se mantiene la versión pre-registrada. La aceptación es baja (el 22 % de los θ aporta rotaciones; ESS de 147 con M = 3.000), así que en M2 se aumenta el número de sorteos de θ hasta un ESS ≥ 500 y se reporta el ESS. La variante V3 (solo impacto; aceptación del 100 % de los θ) se presenta al lado como robustez.
  - **Bandas.** Las de la descomposición histórica casi nunca excluyen el cero con T ≈ 88: se reporta tal cual (contribuciones con banda que incluye el cero = «no distinguible de cero»).
  - **BVAR en tasas: no apto por sesgo.** La atenuación de las IRF hacia cero es sistemática (sesgo absoluto hasta 0,46), y la cobertura del 90 % es de 0,86-0,90. Las magnitudes de las IRF y de la descomposición histórica se presentan como posiblemente atenuadas. La identificación sigue siendo C3s, pero las magnitudes se leen como cota inferior aproximada; se declara en cada tabla.
  - **M3: VAR por regímenes con 5 tramos, no apto** (el tramo de 9 trimestres tiene cobertura de 0,08). Se usa en su lugar la alternativa validada: proyecciones locales dependientes del periodo (LP con interacción de la variable de impulso por la ficticia de periodo; inferencia HAR y LP-IV con Anderson-Rubin), herramienta apta en F3. Su capa es C4 salvo con instrumento (C3). P4 (9 trimestres) se reporta, pero se declara impreciso.
- **Y7. Tras las correcciones del grupo B** (output/v8/F3/otros/validacion.md):
  - **Bai-Perron y umbral de Hansen:** siempre con bootstrap **sieve-AR** (tamaño de 0,03 a 0,08 con errores muy persistentes). Su potencia es baja con series persistentes (BP: 0,32-0,42), así que un no rechazo no prueba ausencia de ruptura o umbral.
  - **LP-OLS:** con T = 90-110 la cobertura queda en 0,78-0,84, incluso con EWC. Las LP sin instrumento (M3 y las de orden temporal de M6) usan EWC y son C4 con bandas aproximadas, declaradas como tales; nunca son evidencia de C3. Las LP-IV usan siempre el intervalo de Anderson-Rubin (cobertura de 0,91 a 1,00), y el placebo por permutación, por su baja potencia (0,21-0,35), se reporta como diagnóstico.
  - **Permutación de fechas con 5 tramos:** es conservadora y tiene poca potencia. Un p < 0,05 es exigente; un p ≥ 0,05 no descarta un efecto por periodo.
  - **Reglas de etiquetado** (H15): las bandas de «con reservas» (cobertura en [0,80; 0,99] y sesgo ≤ 30 %) se fijaron tras ver la primera pasada. Se declaran como tales: las etiquetas son descriptivas y no criterios pre-registrados.

## Y8 — M2: identificación operativa V3 y lectura de la parte determinista (2026-10-13)
- La principal pre-registrada (signos h = 0-1 y 4 ceros) da 0 rotaciones aceptadas en 9·10^6. Por la regla de viabilidad de Y6 se usa V3 (solo impacto) como identificación operativa para H8-1…H8-4 y la atribución. Desviación anotada antes de ver las descomposiciones completas.
- En P5 la parte determinista (constante, condiciones iniciales y ficticias) concentra gran parte de la variación del precio de compra (+17,8 pp [1,5; 34,1]). Se reporta como «crecimiento tendencial no atribuido a los shocks identificados», no como un factor. Se pide al revisor de F4 que lo examine. F5 lo trata como componente explícito («residuo») y no lo reparte entre factores.
- H8-1…H8-4: ninguna rechaza la nula tras Holm (p Holm 0,43-0,82). Se reporta igual.
