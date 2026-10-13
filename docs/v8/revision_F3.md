# Revisión independiente de la PUERTA F3 de V8 (validación por Monte Carlo de herramientas)

- Fecha: 2026-10-13. Revisor independiente; no ha participado en el trabajo revisado.
- Commits revisados: 1545d79 (grupo B) y e740d76 (grupo A); HEAD al revisar: 947889a.
- Alcance: código de src/v8/herramientas/, src/v8/f3_montecarlo_{var,otros}.py, output/v8/F3/{var,otros}/validacion.md, docs/v8/hipotesis.md (pre-registro) y docs/v8/decisiones.md (Y3, Y4).
- No se ha leído data/sealed ni se ha modificado ningún fichero salvo este.

## 0. Comprobaciones reproducidas por el revisor

| Comprobación | Resultado |
|---|---|
| `python3 -m pytest -q tests/v8` | 25 pasan (10 s). |
| `f3_montecarlo_var.py --rapido`, dos veces, sin red (HTTPS_PROXY=http://127.0.0.1:9), salida a un directorio temporal (F3_OUT) | exit 0 y md5 idéntico de montecarlo.csv en las dos ejecuciones (7654cdb3d374c3019f5bd83275aeae12). No se ha ejecutado `f3_montecarlo_otros.py`, porque escribe en output/ sin opción de redirigir la salida. |
| Uso de datos reales | Ninguno. Ni las herramientas ni los scripts de Monte Carlo leen data/ (grep de read_/data/ /open/sealed/holdout). Los únicos accesos a ficheros son las salidas propias y el Registry de multiverso. Los commits de F3 no tocan data/. |
| Etiquetas del grupo A frente a las cifras | Coinciden con las reglas de `etiquetas()`: BVAR con reservas (cobertura del 90 % entre 0,907 y 0,966; sesgo entre 0,138 y 0,246); signos con reservas (no restringidas, 0,990-0,993 > 0,98); TVP no apta (detección 0,17); regímenes con reservas (0,90 / 0,64 / 0,04). |
| Etiquetas del grupo B frente a las cifras | Coinciden con montecarlo.csv, pero son cadenas fijas en el código, no se derivan de reglas (ver H15). |
| Cifras citadas en Y3 e Y4 | Coinciden con los csv: cobertura BVAR de 0,91 a 0,97; sesgo de 14 a 25 %; BIC del 80 al 97 %; tamaño de la permutación 0,052; TVP 17 %; regímenes 0,90 y 0,64. |

### Verificación analítica del código crítico (correcta)

- **BVAR (bvar.py:47-113).**
  - Varianza a priori Σ_jj·λ²/(l²·ψ_i) en la estructura de Kronecker Σ⊗Ω0: es la de GLP. La IW(diag ψ, n+2) da E[Σ] = diag ψ.
  - Dummies de suma de coeficientes y de observación inicial: correctas.
  - logml = π^(−nT/2)·Γn(ν1/2)/Γn(ν0/2)·|S0|^(ν0/2)|S1|^(−ν1/2)·(|Ω1|/|Ω0|)^(n/2): correcta (bvar.py:97-104). Lo confirman la cuadratura (2e-9) y la cadena predictiva t multivariante (6e-14).
  - Bartlett con χ²(ν−i) y B = B̄ + chol(Ω)·Z·chol(Σ)': correctos.
- **Signos (signos.py:100-178).**
  - Sin ceros, la proyección secuencial de gaussianas equivale a QR con diagonal positiva: es Haar (RRWZ).
  - Con ceros, el algoritmo secuencial de ARW y la condición z_j ≤ n−j están bien implementados; los ceros se cumplen con error de 1e-14.
- **Pesos de importancia (signos.py:62-97).** Contraste independiente del revisor: n = 3, ceros en dos shocks con filas distintas, 2·10⁵ sorteos secuenciales frente a una referencia de Haar condicionada por «concha fina» (|c| < 0,004·|ρ|, 2.236 aceptados).
  - Con pesos, la diferencia máxima en E[Q²] es 0,009 (orden 1) y 0,007 (orden 2), con un error de Monte Carlo de 0,007.
  - Sin pesos, la diferencia es de 0,21-0,22.
  - Conclusión: la derivación es correcta para el objetivo que declara, es decir, p(θ)·Haar(Q) condicionado a c(θ,Q) = 0. Que ese objetivo coincida con el de ARW es otra cuestión (H3).
- **Descomposición histórica (signos.py:211-242).** y_t = determinista + Σ G_{t−s}·ε_s, con ε = A0inv⁻¹u: identidad exacta (error < 1e-8).
- **LP-IV (lp.py:85-158).**
  - Anderson-Rubin: invierte n·ḡ'S(b0)⁻¹ḡ con S(b0) = Saa − b0(Sac+Sca) + b0²Scc HAC; correcto.
  - Con 1 instrumento, el F efectivo de Olea-Pflueger coincide con el F robusto.
- **Umbral (regimenes.py:130-194).** Bootstrap de regresores fijos de Hansen (1996). IC por inversión de la LR con c = −2·ln(1−√0,95) = 7,35 (Hansen 2000).
- **Bai-Perron (regimenes.py:198-293).**
  - La programación dinámica sobre la SSR por segmento es correcta.
  - El bootstrap de la nula sin rupturas corrige la búsqueda de fechas.
- **Dominancia (dominancia.py:22-94).** Shapley exacto del R² (los φ suman el R²) con pesos k!(p−k−1)!/p!.
- **Permutación (permutacion.py:236-243).** El muestreo de «estrellas y barras» es uniforme sobre los conjuntos de cortes válidos.

## 1. Tabla de hallazgos

Severidad. Alta: hay que corregirlo antes de usar la herramienta en F4. Media: corregirlo o declararlo antes de F4. Baja: documentación o mejora.

| id | fichero:línea | hallazgo | severidad | corrección propuesta |
|---|---|---|---|---|
| H1 | src/v8/f3_montecarlo_var.py:173-259; src/v8/herramientas/signos.py:100 | **La configuración validada de signos y ceros no es la pre-registrada.** El Monte Carlo usa n = 4 y restricciones solo de impacto. M2 usa n = 7, signos en h = 0-1, 4 ceros y T ≈ 88. Simulación del revisor con un DGP de 7 variables que cumple la tabla de §5: aceptación de 1,05e-4 por rotación; con `max_rot = 3000`, solo 53 de 200 sorteos de θ obtienen una rotación aceptada (el 73 % se descarta); ESS de los pesos 48,5/53. La cobertura, la recuperación del signo y el coste no están validados en la configuración en la que se contrastarán H8-1 a H8-4. | alta | Monte Carlo con el esquema exacto de §5: 7 variables, h = 0-1, 4 ceros (o 6, ver H16), T = 88, p = 2 y GLP. Medir cobertura, recuperación del signo, P(contribución ≤ 0) bajo la nula y fracción de θ sin aceptación. Fijar `max_rot` o el número de sorteos de θ en docs/v8/decisiones.md antes de F4. |
| H2 | src/v8/herramientas/signos.py:122-163 | **Se guarda la primera rotación aceptada de cada θ (`por_sorteo = 1`) y se reintenta hasta `max_rot`.** Así cada θ con al menos una aceptación pesa igual, en lugar de pesar en proporción a P(S\|θ), que es lo que exige la posterior uniforme-normal-Wishart inversa condicionada a los signos (RRWZ/ARW: un Q por θ, o todos los aceptados de un número fijo de rotaciones). En el DGP de 4 variables con T = 90, P(S\|θ) varía entre sorteos en un factor 4 (p10-p90: 0,00075-0,00155; ESS si se pondera por P(S\|θ): 55/60). La distorsión es pequeña en ese caso, pero existe. Con aceptación muy baja (H1) la selección se aproxima sola a la proporcionalidad. | media | Para cada θ, probar un número fijo M de rotaciones y conservar todas las aceptadas, o ponderar cada θ por su tasa de aceptación estimada. Repetir el Monte Carlo de signos con el cambio. |
| H3 | src/v8/herramientas/signos.py:8-12, 62-97; docs/v8/decisiones.md (Y4) | **Pesos de importancia.** Son correctos para su objetivo declarado (contraste de concha fina, sección 0). Pero ese objetivo, Haar condicionado en coordenadas (θ, Q), no está demostrado que coincida con el de ARW (prior NGN condicionado en el espacio estructural, con pesos = cociente de elementos de volumen v_{f_h\|Z}/v_{(g∘f_h)\|Z}). En general pueden diferir en un factor jacobiano que depende de θ y de Q. La prueba de invariancia al orden no los distingue, porque ambos objetivos son invariantes al orden. | media | (i) Renombrarlos en salidas y textos como «pesos propios (Haar condicionado a los ceros), no ARW», y no citar ARW como fuente del prior. (ii) En F4, reportar la descomposición histórica principal con y sin pesos; en la configuración de H1 el ESS es de 48,5/53, así que la sensibilidad es barata. (iii) Opcional: implementar los pesos de ARW por diferencias finitas en un caso pequeño (n = 3) y compararlos. |
| H4 | src/v8/herramientas/bvar.py:25-32, 116-159; src/v8/herramientas/signos.py:211-242 | **No hay regresores exógenos.** El pre-registro (§5) exige ficticias fijas de COVID y de EPA 2021T1 como exógenas en el BVAR. `retardos()` solo admite constante, y la parte determinista de la descomposición histórica solo propaga la constante y las condiciones iniciales. Sin ellas, la identidad de la descomposición histórica con exógenas no está validada. | alta | Añadir un argumento `exog` a `retardos`, `estimar` y `descomposicion_historica`, con varianza a priori laxa como la de la constante. Incluir las exógenas en la parte determinista y repetir el test de identidad (< 1e-8). |
| H5 | src/v8/herramientas/regimenes.py:247-283; docs/v8/decisiones.md (Y3) | **El bootstrap por bloques de Bai-Perron solo se ha validado con AR(0,5) y bajo la nula.** Contraste del revisor (R = 120, B = 99, n = 100, bloque = 8): tamaño de UDmax con AR(0,85) = **0,267**; potencia con AR(0,5) y salto de 1σ = **0,55** con bloques (0,975 con wild). Las series de detección de §8 (crédito, tipos y actividad) son persistentes. Y3 da los bloques por suficientes. | alta | Longitud de bloque dependiente de los datos (Politis-White) o bootstrap sieve-AR/preblanqueado. Validar tamaño con ρ ∈ {0,5; 0,8; 0,9} y potencia con n ≈ 90-126. Si el tamaño no baja de 0,10, BP queda como confirmación «con reservas» y no puede satisfacer por sí sola la regla de §8. |
| H6 | src/v8/herramientas/regimenes.py:130-194; output/v8/F3/otros/validacion.md | **Umbral de Hansen «apta» sin opción para errores autocorrelacionados.** Contraste del revisor (R = 120, n = 100): con errores AR(0,5) y una variable umbral persistente (AR 0,9, como el tipo real, el crédito interanual o el paro de §8), el tamaño es **0,175**; con errores iid es 0,050. Y3 no impone restricciones de uso. En crecimientos interanuales los errores son MA(3) por construcción. | alta | Añadir bootstrap por bloques (o sieve) y validarlo con errores AR y q persistente. Hasta entonces, cambiar la etiqueta a «apta solo con errores sin autocorrelación (comprobar con LM)» y añadirlo a Y3. |
| H7 | src/v8/herramientas/lp.py:54-158 | **LP y LP-IV no admiten horizontes negativos.** Las pretendencias son un requisito de C3 (§6). Tampoco hay p-valor de Anderson-Rubin unilateral, que H8-5/H8-6 usan («p del intervalo AR»), ni un contraste conjunto para h = 4-8. El placebo con instrumento permutado no está implementado. | media | Añadir horizontes h < 0 (y_{t+h} con h negativo, misma inferencia). Añadir una función `ar_p(b0 = 0, lado)` y la regla de agregación h = 4-8 del pre-registro. Añadir el placebo por permutación del instrumento y validarlo con 1-2 escenarios de Monte Carlo. |
| H8 | src/v8/f3_montecarlo_otros.py:172-221 | **LP-OLS y LP-IV se validan con n = 200 y solo h ≤ 8 (OLS) o h ∈ {0, 2} (IV).** IV1 tiene unos 107 trimestres y los horizontes confirmatorios son h = 4-8 (hasta 12 en el pre-registro). Contraste del revisor con n = 100: cobertura de LP-OLS NW en h = 8 de **0,863**; con ρ = 0,9, 0,863 en h = 4 y 0,853 en h = 8 (fuera de [0,90; 0,98]). La AR de LP-IV con instrumento débil y ρ = 0,8 da 0,963 (h = 0) y 0,983 (h = 4): se mantiene. | media | Repetir el Monte Carlo con n ∈ {90, 110} y h ∈ {0, 4, 8, 12}. Si LP-OLS sigue por debajo de 0,90, etiquetarla «con reservas» y usar ancho de banda mayor o EWC; no usarla como evidencia de C3. |
| H9 | src/v8/herramientas/tvp.py:205-236; docs/v8/decisiones.md (Y4) | **VAR por regímenes con los cinco periodos pre-registrados.** El Monte Carlo valida 2 regímenes de 59 observaciones con n = 3. En M3, P4 tiene 9 trimestres y P1 desde 2004 tiene 16; con n = 7 y p = 2 hay 15 coeficientes por ecuación, de modo que en P4 la posterior es esencialmente el prior. Además, `var_regimenes` supone tramos contiguos y no trata los huecos de transición (2008T1-T2, 2020T1). | media | Monte Carlo con 5 tramos de longitudes reales (incluido uno de 9 observaciones) y n del uso previsto. Declarar en Y4 qué variables entran en M3 y que en P4 el resultado queda como exploratorio si la posterior no se separa del prior. Admitir tramos no contiguos o excluir los huecos explícitamente. |
| H10 | src/v8/herramientas/bvar.py:47-58, 116; tvp.py:205 | **La media a priori del primer retardo propio es `delta = 1` (paseo aleatorio) por defecto.** Las variables de M2 son tasas trimestrales (log ×100), para las que GLP usan δ = 0 o un valor bajo. Los DGP del Monte Carlo son estacionarios con media cero, y no se ha validado δ = 0 ni la sensibilidad a δ. | media | Fijar δ por variable en docs/v8/decisiones.md antes de F4 (p. ej., 0 para crecimientos; para el tipo en nivel, 1 o el AR(1) de una pre-muestra). Añadir una celda de Monte Carlo con δ = 0. |
| H11 | docs/v8/decisiones.md (Y3); docs/v8/hipotesis.md:6, §8 | **Desviación no anotada.** El pre-registro dice que el número de regímenes de Markov switching se contrasta por bootstrap. Y3 pasa a elegirlo por BIC y deja el bootstrap como informativo. El pre-registro exige anotar las desviaciones en docs/v8/desviaciones.md (motivo y fecha, antes de ver el resultado), y ese fichero no existe. Lo mismo para el número de factores fijo (r = 1) si se interpreta como un cambio de método en H8-8. | media | Crear docs/v8/desviaciones.md con estas entradas (fecha, motivo y cifras de F3) antes de F4. |
| H12 | output/v8/F3/var/validacion.md (sección 1); docs/v8/decisiones.md (Y4) | **Y4 afirma que las IRF del BVAR están «sesgadas hacia cero», pero la validación solo da el sesgo absoluto agregado.** Contraste del revisor (60 réplicas por celda, GLP): está atenuado el 77-87 % de las celdas en el DGP denso y el 78-100 % en el casi_RW. La atenuación firmada relativa es de 0,074 (denso) y 0,045 (casi_RW) con T = 120, y de 0,229 y 0,198 con T = 60. La afirmación es coherente, pero no está documentada. Con T = 120 el sesgo firmado sería ≤ 10 %; el criterio absoluto mezcla error de Monte Carlo por celda. | baja | Añadir la métrica de sesgo firmado (atenuación) a `mc_bvar` y a validacion.md, y citarla en Y4. |
| H13 | src/v8/herramientas/permutacion.py:1-5, 203, 246-267, 270-308 | **El texto afirma un «p-valor exacto de permutación (válido en muestra finita)».** La exactitud exigiría intercambiabilidad de las fechas bajo H0, que no se cumple en general con dependencia serial (el propio código reconoce que el estadístico sin studentizar depende de la posición). Su validez es aproximada y está respaldada por el Monte Carlo (studentizado: 0,048-0,056). Además, el estadístico compara solo el primer y el último tramo, supone tramos contiguos (los periodos de §3 tienen huecos) y no se ha probado con 5 tramos, longitud mínima de 8 y T ≈ 126. | baja | Cambiar «exacto» por «de permutación de fechas (validez aproximada, ver Monte Carlo)». Documentar el estadístico multitramo que se usará en M0 y añadir una celda de Monte Carlo con 5 tramos, longitud mínima de 8 y n = 126, con AR(0,8). |
| H14 | src/v8/f3_montecarlo_otros.py:124-170, 222-257, 327-360 | **Los tamaños muestrales de varios Monte Carlo no son los del uso previsto.** Markov switching: n = 200-250 frente a T ≈ 100-126. Dominancia: iid con n = 300 frente a series de T ≈ 90 (no se valida el bootstrap por bloques). DFM: N ∈ {10, 40} y no N = 17; DFM-ML solo con N = 8 y r = 1. | baja | Añadir celdas con T ≈ 100-126 y N = 17 y dominancia con `bloque > 1` y regresores AR. La decisión r = 1 de Y3 es coherente con la validación (con N pequeño, Bai-Ng elige kmax). |
| H15 | src/v8/f3_montecarlo_otros.py:381-416; src/v8/f3_montecarlo_var.py:400-405, 472-520 | **Etiquetas y reglas.** En el grupo B las etiquetas son literales («apta», «con reservas») que no se calculan con las cifras; si un Monte Carlo cambiara, la etiqueta no cambiaría. Las reglas de «con reservas» (cobertura en [0,80; 0,99], sesgo ≤ 30 %) las define el ejecutor en el mismo commit que los resultados, y varios valores numéricos de los párrafos de «Lectura» de validacion.md son literales. | baja | Derivar las etiquetas del grupo B con reglas explícitas como en el grupo A. Fijar las reglas de «con reservas» en docs/v8/decisiones.md con la nota de que se definieron después de ver las cifras de F3. Generar las cifras de los párrafos desde el csv. |
| H16 | docs/v8/hipotesis.md §5 (ceros en población) | **Ambigüedad del pre-registro que afecta a la configuración que hay que validar (H1).** El texto dice que la población no responde a ningún shock salvo al demográfico, lo que supone 6 ceros si los dos shocks no identificados también tienen cero. La tabla solo marca 4 ceros. Con 6 ceros, el shock demográfico queda determinado por la fila de Σ (exactamente identificado), y la identificación cambia materialmente. | media | Aclararlo en docs/v8/desviaciones.md o en decisiones.md antes de F4 y validar la variante elegida en H1. |
| H17 | src/v8/herramientas/multiverso.py:27-69 | El tope por defecto es `max_specs = 2000` (el pre-registro dice como máximo 50.000). Las especificaciones que fallan o tienen n pequeño se descartan sin registrarse en el Registry. | baja | Usar el tope del pre-registro y registrar también las especificaciones fallidas, con su motivo. |
| H18 | src/v8/f3_montecarlo_otros.py:24 | La salida de `f3_montecarlo_otros.py` no se puede redirigir (OUT fijo), de modo que el revisor no puede reproducirlo sin escribir en output/. | baja | Admitir una variable de entorno `F3_OUT` como en el script del grupo A. |

## 2. Diseño de los Monte Carlo (pregunta 2)

- **Pertinencia.**
  - Se ajustan al uso:
    - BVAR, con T ∈ {60, 120} que encuadra T = 88;
    - umbral y BP, con n = 120;
    - TVP, con T efectivo de 88.
  - No se ajustan:
    - signos y ceros (n = 4, solo impacto, frente a n = 7 y h = 0-1: H1);
    - LP y LP-IV (n = 200: H8);
    - Markov switching (n = 200-250);
    - dominancia (iid, n = 300);
    - DFM (N = 17 ausente);
    - persistencia de los errores (solo AR 0,5: H5, H6).
- **Honestidad de los criterios.**
  - Los criterios declarados (sesgo ≤ 10 %, cobertura del 90 % en [0,85; 0,98], tamaño en [0,02; 0,10]) se aplican sin rebajarlos.
  - El BVAR no se declara «apta» por el sesgo.
  - Los signos quedan «con reservas» por sobrecobertura.
  - La TVP es «no apta» por potencia.
  - Markov switching queda «con reservas», con el carácter indicativo de R = 20 y R = 6 declarado.
  - Las categorías intermedias («con reservas») usan umbrales del ejecutor (H15), pero están escritas y son trazables.
- **Correspondencia entre etiquetas y cifras.** Correcta en todos los casos revisados, con dos excepciones:
  - «umbral_hansen: apta» y «lp_ols: apta» son ciertas solo en los DGP probados (errores iid, n = 200); para el uso previsto no se sostienen (H6, H8).

## 3. Coherencia de Y3 e Y4 con la validación (pregunta 4)

| Decisión | Coherencia |
|---|---|
| TVP no apta → VAR por regímenes con fechas conocidas; TVP solo para la volatilidad | Coherente con las cifras (detección del 17 %; regímenes 0,90 / 0,64 / 0,04), dentro de lo previsto en el plan («TVP-VAR-SV o regímenes»). Pendiente: validar los 5 tramos reales (H9). |
| BP con bootstrap por bloques | Coherente con lo medido (AR 0,5: 0,044), pero insuficiente con persistencia alta y sin potencia validada (H5). |
| Número de factores fijo (r = 1, sensibilidad con 2) con N = 17 | Coherente (Bai-Ng con N = 10: 0 % de acierto). |
| Markov switching: k por BIC; bootstrap informativo | Coherente con las cifras (potencia de 0,40), pero es una desviación del pre-registro sin anotar (H11). |
| Permutación studentizada | Coherente (tamaño 0,048-0,056); baja potencia declarada. |
| LP-IV siempre con Anderson-Rubin | Coherente (la AR cubre entre 0,925 y 0,975 incluso con instrumento débil; el IC normal llega a 0,998). |
| SHAP solo como contraste | Coherente con §9 del pre-registro. |
| BVAR-GLP con reservas; IRF atenuadas | Coherente; la atenuación la confirma el revisor, pero falta documentarla (H12). |
| Signos: un elemento no restringido solo se lee si su banda excluye el cero | Coherente con el dato (la banda del 90 % nunca excluye el cero en las celdas no restringidas). |
| Pesos «ARW» con declaración | Admisible si se renombran y se reporta la sensibilidad con y sin pesos (H3). |

## 4. Veredicto

**APROBAR CON CORRECCIONES.**

- La implementación de lo crítico es correcta en lo verificado: verosimilitud marginal, prior GLP, RRWZ y algoritmo secuencial de ceros, identidad de la descomposición histórica, Anderson-Rubin, Hansen, Bai-Perron y LMG.
- Los pesos de importancia son correctos para el objetivo que declaran.
- No se han usado datos reales, y la ejecución rápida es reproducible sin red.

Antes de que F4 use estas herramientas en contrastes confirmatorios o en la regla de §8, hay que resolver, por este orden de prioridad:

1. **H4.** Exógenas (COVID y EPA) en el BVAR y en la descomposición histórica, con su test de identidad.
2. **H1 + H16.** Aclarar si los ceros son 4 o 6 y hacer un Monte Carlo del esquema exacto de §5 (7 variables, h = 0-1, T = 88), con `max_rot` o el número de sorteos fijado.
3. **H5, H6.** Bootstrap de BP y del umbral robusto a la persistencia (validado con ρ de 0,8-0,9 y n ≈ 100), o rebajar su papel en la regla de §8.
4. **H2, H3.** Ponderación por P(S|θ); renombrar los pesos y reportar la sensibilidad con y sin ellos.
5. **H7, H8.** Pretendencias, p-valor AR unilateral y placebo en LP-IV; Monte Carlo de LP con n ≈ 100 y h hasta 12.
6. **H9, H10, H11.** Monte Carlo de regímenes con los 5 tramos reales; δ fijado antes de F4; crear docs/v8/desviaciones.md.
7. **Bajas: H12-H15, H17, H18.**
