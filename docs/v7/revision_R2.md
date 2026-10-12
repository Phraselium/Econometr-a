# Revisión independiente de V7 · R2 (herramientas de panel)

Revisor independiente. Fecha: 2026-10-12. Alcance: src/v7/panel_tools.py, src/v7/r2_montecarlo.py, docs/v7/validacion_herramientas.md, tests/v7/test_panel_tools.py, docs/v7/decisiones.md (V9 y V10) y docs/v7/hipotesis.md. Las conclusiones salen de leer el código, de ver el historial de git (15dc096 → 0495ce7) y de comparar con la literatura. No he vuelto a ejecutar el Monte Carlo, no he estimado nada con datos reales y no he leído data/sealed.

## Veredicto: **REHACER** (alcance acotado)

Las fórmulas centrales son correctas. Las fallas están en el diseño de la validación y en cómo se justifica el estimador principal. Mientras no se corrijan los hallazgos 1 a 5, no conviene estimar con datos reales.

## 1. Corrección de las implementaciones

Elementos que he comprobado y doy por correctos:

- **Forma ECM (`_build`, l. 26-40).** `d` = Δy_t; los niveles son (y_{t-1}, x_{t-1}); Δx entra contemporáneo y con q-1 retardos; Δy, con p-1 retardos. Los índices son coherentes con `_start`.
- **PMG, verosimilitud concentrada (l. 117-129).** Se parcializa W y se concentran φ_i y σ_i², lo que da RSS_i = d̃'d̃ − (ξ̃'d̃)²/ξ̃'ξ̃. `prof` es −2·logL de PSS (1999), eq. 13-15. Es correcta.
- **Medias transversales de CS-ARDL (`_cs_extra`, l. 47-55).** z_{t-1} junto con Δz_t…Δz_{t-pT+1} abarca el mismo espacio que z_t…z_{t-pT}. Es correcto según Chudik y Pesaran (2015).
- **CADF/CIPS (l. 241-257).** Incluye constante, y_{i,t-1}, ȳ_{t-1}, Δȳ_t y los retardos aumentados. Coincide con Pesaran (2007), eq. 6.
- **Webb, WCR restringido, DFE con EE agrupados y Driscoll-Kraay.** Son correctos. Al DFE le afecta el sesgo de Nickell, que está documentado.

## 2. Hallazgos

| # | Severidad | Hallazgo | Corrección |
|---|---|---|---|
| 1 | ALTA | **El DGP no pone a prueba el motivo por el que se elige MG_dm.** En `r2_montecarlo.py:53`, el factor entra en Δy como shock I(0) dentro de la ecuación ECM (`ky*f[t]`). Así, el residuo de cointegración es estacionario y la dependencia transversal no sesga θ: MG y PMG sin ajuste ya sesgan ≤6 % (validacion_herramientas.md:220). Falta el caso relevante para la vivienda: un **factor común I(1) en el residuo de cointegración** (ciclo nacional de precios) con cargas heterogéneas y correlacionadas con x. Con cargas heterogéneas (`gx`, `ky` ~ N(1; 0,5)), el demeaning transversal no elimina el factor. Solo CCE (CS-ARDL/CS-DL) lo hace. | Añadir los escenarios F (factor I(1) en u_it con cargas heterogéneas y correlacionadas con gx) y G (cargas homogéneas). Comparar MG_dm, CS-ARDL y CS-DL en ambos. |
| 2 | ALTA | **CS-ARDL y CS-DL se descartan en el DGP donde no aportan nada.** Además, no se prueban sus correcciones estándar. Con pT=4 hay unos 22 regresores para 74 observaciones. Chudik et al. (2016) proponen el jackknife de mitades y un pT menor. `jackknife_phi` existe, pero no se aplica a θ de CS-ARDL. | Repetir con pT ∈ {1, 2, 4} y con jackknife sobre θ en los escenarios A, B, F y G. Decidir «no apta» solo después. |
| 3 | ALTA | **El criterio de CIPS se cambió a posteriori.** En la ronda 1, CIPS «no apta» (rechaza 0,11-0,56 sobre la y I(1) del DGP). En la ronda 2 se añade un objetivo nuevo, `CIPS_RW_puro` (diff 15dc096→0495ce7), y pasa a «apta». La y del DGP, una I(1) con un gran componente estacionario (raíz MA casi cancelada), es precisamente el caso de los precios. Decir que «no es un problema de CIPS» (validacion_herramientas.md:218) es incorrecto. | Mantener «no apta / solo con reservas» para series con un componente I(0) grande. Probar CIPS* (truncación K1/K2), selección de retardos por SBC y tendencia. Registrar el cambio de criterio en decisiones.md. |
| 4 | ALTA | **El IC bootstrap de PMG con demeaning no está validado.** V10 y hipotesis.md:38-46 lo usan con la cobertura «≈0,88», pero en el MC `PMG_boot` se calcula solo sobre datos SIN demeaning (`r2_montecarlo.py:84-86`), con r<100 y B=49. El bootstrap por unidades (`panel_tools.py:157-168`) supone unidades independientes. Tras el demeaning dejan de serlo (suman cero) y, si hay factor, ese supuesto falla. | Validar `pmg_bootstrap` sobre datos con demeaning, volviendo a aplicar el demeaning dentro de cada remuestra, con B≥199 y ≥200 réplicas en A, B, F y E. |
| 5 | ALTA | **La inferencia de H7-E2 (φ̄<0) no es estándar.** Bajo H0 φ=0 no hay cointegración y el t de MG sigue una distribución tipo Dickey-Fuller, no normal. Además, el sesgo de φ es −19 % en la dirección de H1, de modo que el test es anticonservador. | Para E2, usar el p simulado bajo H0 (escenarios C y D) o subsumir E2 en Westerlund Gt (E1). Si no, declarar E2 como EXPLORATORIO. |
| 6 | MEDIA | **Westerlund no es el estadístico estándar.** En `panel_tools.py:297`, α_i(1) se obtiene como 1−Σλ en lugar de ω̂_u/ω̂_y (Newey-West). Pt y Pa (l. 312-314) son una versión agrupada ponderada por 1/σ_i² y no la de Westerlund (2007), eq. 12-13, y no hay leads de Δx. Con el p bootstrap el tamaño queda controlado, pero el tamaño es 0,000-0,010 (fuera de [0,02; 0,10]) y la potencia solo se mide con φ_i ∈ [−0,4; −0,1]. | Rotular «tipo Westerlund». Medir la potencia con φ_i ∈ [−0,1; −0,02] (ajuste lento, típico de la vivienda). Bootstrap por bloques: comprobar que el remuestreo de Δ bajo H1 no le quita potencia. |
| 7 | MEDIA | **Hausman: la no significación se usa como prueba de homogeneidad.** La potencia es 0,61 (hipotesis.md:51 frente a hipotesis.md:71). La variante `var_diff='mg'` se eligió porque era la única con un tamaño válido en el MC: es una selección guiada por el resultado. | Si no se rechaza, reportar MG y PMG sin declarar «homogeneidad». Documentar la elección de la variante como decisión a posteriori. |
| 8 | MEDIA | **Faltan escenarios.** No hay roturas estructurales (2008, 2020), ni retroalimentación del EC en Δx (x no débilmente exógena), ni errores con heterocedasticidad o autocorrelación, ni un ARDL mal especificado. La selección de retardos por SBC (hipotesis.md:32) tampoco se valida: el MC usa el orden verdadero ARDL(2,1). | Añadir al menos: rotura en c_i o θ en t≈T/3; feedback (Δx con −0,1·ec); SBC con p, q ≤ 4. |
| 9 | MEDIA | **La precisión del MC es baja.** Con 200 réplicas, el EE-MC de una cobertura de 0,90 es ≈0,021. PMG_boot usa 100 réplicas (EE ≈0,03) y B=49. Coberturas como 0,895 frente a 0,90 no son distinguibles. | Usar ≥500 réplicas en los escenarios decisivos y reportar el EE-MC junto a cada cifra. |
| 10 | MEDIA | **Los tests de `make check` son de humo, no de validez.** Hausman admite un rechazo ≤0,35 y CIPS ≤0,30 (test_panel_tools.py:43 y 60). Wild cluster solo comprueba 0≤p≤1 y potencia. No hay comparación con una implementación de referencia (xtpmg, xtcointtest, xtcips) ni comprobación de que los veredictos del MC se reproducen. | Añadir: (a) comparación numérica con resultados publicados o de Stata/R sobre un panel fijo versionado; (b) tamaño de WCR con 17 clusters en [0,02; 0,10]; (c) test de que `veredictos()` reproduce la tabla del documento con una semilla fija y pocas réplicas. |
| 11 | BAJA | `pmg` l. 141: los grados de libertad de se_phi_i son n−1−k y deberían ser n−dim(W)−1. La información de PSS no proyecta ξ (es asintóticamente equivalente). `cs_dl` l. 181: el filtro `(t-1-j).min()>=0` nunca se activa (es código muerto). | Corregir los grados de libertad y eliminar el filtro. |
| 12 | BAJA | MG_dm sobrecubre en E (1,000) y cubre 0,87 en A: el EE de MG con demeaning ignora la correlación negativa entre los θ_i (que suman cero). | Calcular el EE por jackknife de unidades re-demeaned. |

## 3. Respuestas a las preguntas

1. **¿Son correctas las implementaciones?** Sí en lo esencial: la verosimilitud concentrada de PSS, la forma ECM, CS-ARDL y CADF/CIPS. Westerlund es una variante y debe rotularse así (hallazgo 6).
2. **¿Es pertinente el DGP?** El tamaño N=17, T=78 es el adecuado, pero el DGP no incluye el factor I(1) en el residuo, el feedback ni las roturas (hallazgos 1 y 8). Los criterios ±10 % / [0,90; 0,98] / [0,02; 0,10] son razonables, pero se relajaron a posteriori (hallazgos 3 y 7) y el EE-MC es grande (hallazgo 9).
3. **¿Está justificada la elección del estimador principal?** Todavía no. MG_dm gana en un DGP donde la dependencia transversal es inocua (hallazgo 1). El IC bootstrap de PMG_dm no está validado (hallazgo 4). Hausman con V_MG es conservador y poco potente (hallazgo 7). El pre-registro es coherente con V10 en su forma, pero hereda estos problemas y añade el de E2 (hallazgo 5).
4. **¿Comprueba `make check` la validez?** No. Comprueba que las funciones se ejecutan y tienen un comportamiento grosero razonable (hallazgo 10).

## 4. Prioridad para la ronda 3

Orden propuesto: 1 → 2 → 4 → 3 → 5 → 10 → 6 → 8 → 7 → 9 → 11-12.

Hasta cerrar 1-5, el pre-registro (hipotesis.md) no debe publicarse ni usarse para estimar.
