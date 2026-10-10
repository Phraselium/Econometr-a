# Revisión v2 — rama BP (política de vivienda): H5 (sin sellado) y puerta de H6 (sellada)

Revisor independiente (opus). Objeto: worktree `/home/user/wt-BP`, rama `r2/BP`, commit `7c9876f` (src/v2/bp_main.py, bp_lib.py, bp_h6_sellado.py, tests/test_bp_h6_sellado.py; output/v2/BP/). Pre-registro: docs/v2/hipotesis.md en `910c42a` (sin cambios hasta `7c9876f`). Fecha: 2026-10-10.

## Veredicto: **REHACER** (acotado; no hay que rehacer H5 ni tocar el diseño de H6)

H5 está bien hecha: reproducible, sin fuga que afecte al estimador principal, SDiD fiel a Arkhangelsky et al. (2021) y nivel EXPLORATORIO coherente con los diagnósticos. `evaluar_H6` es fiel al pre-registro (con desviaciones declaradas y razonables) y funciona con la configuración real en un sellado falso. Pero H6 solo se abre UNA vez y antes hay que cerrar cuatro cosas baratas: (C1) que un fallo o un corte por tiempo en los análisis secundarios no queme la apertura sin dejar resultado principal; (C2) declarar ANTES de abrir la potencia y cómo se leerá un nulo (IPC de parque frente a tope sobre contratos nuevos); (C3) la base 2025=100 del IPC lleva información sellada a los niveles: el SC (no el SDiD) depende de ella; (C4) `make models` falla en `bp_h6_sellado.py`. Tras C1-C4 basta una re-revisión breve de bp_h6_sellado.py, del test y del resumen.

## 1. Reproducción (clon aislado, sin red)

- Clon nuevo (`git clone --no-hardlinks -b r2/BP`, HEAD `7c9876f`) en un directorio de scratch. El clon no tiene data/sealed: `holdout` resuelve SEALED en el propio clon, que no existe. `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`. No hay objetivo de BP en el Makefile, así que ejecuté directamente `python3 src/v2/bp_main.py` y `python3 tests/test_bp_h6_sellado.py`, dos veces.
- **exit 0** en las 4 ejecuciones (main y test, ×2). Salida: `nivel: EXPLORATORIO | tau1=0.0037 p=0.065 | tau2=0.0055 p=0.358`; el ensayo en seco da lo mismo que el JSON versionado.
- **md5 de los 31 ficheros de output/v2/BP: idénticos entre las dos ejecuciones.**
- Frente a las salidas versionadas, cambian 8 ficheros. SDiD, DiD, λ, ω, jackknife y potencia difieren en ≤ 1e-15 (redondeo). Solo el **SC** cambia algo más: τ_post1 0,0052807 → 0,0052820 y p del placebo SC 0,0480 → 0,0470. La causa es que el QP del SC no tiene penalización y su solución no es única: depende del número de hilos de BLAS (yo usé `OMP_NUM_THREADS=1`, porque con hilos por defecto y la máquina cargada una ejecución pasó de 26 min sin terminar). No cambia ninguna conclusión. Declararlo y fijar los hilos en el Makefile/README (C9).
- Tiempo: con un hilo, `evaluar_H6` con la configuración real tarda ≈ 6-7 s con B=100, así que ≈ 1 min con B=1000. Con hilos por defecto en una máquina cargada puede tardar decenas de veces más (C1).
- `make models` **no** reproduciría la rama: `bp_h6_sellado.py` sale con código 1 y corta el bucle (C4).
- smoke/ no se regeneró (sin cambios de código desde el commit).

## 2. Fuga de información

| Comprobación | Resultado |
|---|---|
| Lecturas de datos | `bp_main.py` solo usa `vc.load` (→ `holdout.load_train`) para `panel_prov_q` y `nacional_q_v2`. Ni data/raw ni data/sealed ni red. `bp_h6_sellado.py` no importa `holdout`; el test AST lo comprueba en los tres módulos. OK |
| Periodo | `assert pan.trimestre.max() <= 2024Q2`; H5 usa 2016Q1-2023Q4; el exploratorio nacional, ≤ 2024Q2. El train tiene 49 provincias (sin 11, 16, 45) y `ipc_alquiler` está completo 2002Q1-2024Q2 (método `agregado_media`, sin interpolar). `ipc_alquiler` del train es idéntico en `910c42a` y `7c9876f` (solo cambiaron las `pob_*` por la anulación de interpolaciones). OK |
| Fechas del tope | eventos_politica E09: Ley 11/2020, vigor 2020-09-22; E10: STC 37/2022, publicada 2022-04-08. Codificación 2020Q4-2022Q1 = pre-registro; 2020Q3 (9 días) y 2022Q2 (8 días) quedan fuera, declarado (desviaciones 4). OK |
| Fechas de H6 | Zonas catalanas: declaración autonómica 2024-03-13 (140) y 2024-07-01 (131); efecto BOE 2024-03-16 y 2024-10-10. Excluir 2024Q1-Q2 del ajuste es correcto. Donantes: con zona declarada hasta 2026Q2 solo País Vasco (01, 20, 48), Navarra (31) y A Coruña (15; Santiago va en ZT09, 2026-07-30, igual que Asturias): Asturias (33) es donante legítimo (efecto 2026-07-30 > 2026Q2). OK |
| **Base del índice (nuevo, transversal)** | `ine_v2_ipc_alquiler_prov.csv` es **base 2025 = 100** (media 2025 de las series de índice = 100,000; la dispersión entre provincias cae de 3,4 en 2016Q1 a 0,9 en 2024Q2). Así, ln IPC_it del train = ln P_it − ln P̄_i,2025: una constante por provincia calculada con datos sellados. SDiD y DiD son invariantes a constantes por unidad (lo he comprobado: τ idéntico rebasando a 2016=100), pero el **SC sin intercepto no**: τ_post1 0,00528 → 0,00536 y placebo 2018Q4 0,00551 → 0,00490. Fuga formal y pequeña, solo en robustez (ver C3). Para el orquestador: cualquier uso en nivel sin efecto fijo de unidad de `ipc_alquiler` o de `ratio_precio_alquiler_idx` (= ln p_tasado − ln ipc_alquiler) en otras ramas tiene el mismo problema |
| `zona_tensionada_share` (secundario de H6) | Pesos catastrales del «año de stock más cercano» (diccionario_v2): puede ser un año ≥ 2025. Solo afecta al agregado ponderado (secundario). Declararlo |
| Accesos a la muestra sellada | docs/v2/holdout_accesos.md: solo H1 (BA) y H2 (BV), con apertura y resultado. **H6 no se ha evaluado.** Ni el código de BP ni el test llaman a `evaluate`. La configuración no me deja leer data/sealed/_accesos.log, así que la comprobación es indirecta (copia versionada). OK |

## 3. Fidelidad de SDiD a Arkhangelsky et al. (2021) y estimadores de robustez

| Elemento | Paper (Alg. 1) | bp_lib.sdid | Valoración |
|---|---|---|---|
| Pesos de unidad | min Σ_t (ω0 + Σ_i ω_i Y_it − ȳ_tr,t)² + ζ² T_pre ‖ω‖², ω en el símplex | intercepto eliminado al centrar cada unidad en el tiempo (A − media por columna), penalización `z_om**2 * Tpre`, QP en el símplex | Correcto |
| ζ | (N_tr T_post)^{1/4} σ̂, σ̂ = DE de las primeras diferencias de los controles en el pre | idéntico; `_noise` usa solo diferencias entre trimestres consecutivos (necesario en H6, cuyo pre tiene hueco) | Correcto. H5: σ̂ = 0,0026, ζ_ω = 0,0058 |
| Pesos de tiempo | intercepto λ0, ζ_λ = 10⁻⁶ σ̂, objetivo = media post de los controles | centrado entre unidades, `z_la**2 * N0`, objetivo `Yco[:, post].mean(1)` | Correcto. λ degenera en el último trimestre pre (H5: 2020Q3 = 1,0): esperable en niveles con tendencia; declarado |
| τ | DiD ponderado | `gap[post].mean() − λ·gap[pre]` con gap = ȳ_tr − ω'Y_co | Correcto |
| Solver | Frank-Wolfe | SLSQP en el símplex | Misma solución (problema convexo). `r.success` no se comprueba (C9) |
| SC | Abadie et al. (2010) | ω en el símplex, sin intercepto ni λ, τ = brecha media post | Correcto como SC «de niveles»; pero depende de la base del índice (C3) |
| DiD | pesos uniformes | igual; coincide con TWFE-cluster (assert 1e-9) | Correcto |

Inferencia:
- **Placebo/permutación (Alg. 4)**: se asigna el tratamiento a 4 donantes al azar (B=1000 de C(45,4)=148.995 subconjuntos, semilla fija), re-estimando ω y λ en cada placebo. Es el procedimiento que el paper recomienda con pocas tratadas. Su validez exige que las unidades sean intercambiables (homocedasticidad entre unidades, §5 del paper). La media de 4 provincias catalanas, con Barcelona dentro, puede ser menos ruidosa que la de 4 donantes al azar, y eso haría la prueba conservadora. Hay que declararlo (C7).
- **Jackknife (Alg. 3)**: con N_tr=4 está definido (solo es imposible con N_tr=1) pero tiene poca fiabilidad, porque cada réplica que quita una tratada cambia un 25 % del agregado. Da EE 0,0026 frente a 0,0020 del placebo. Que figure como secundario es correcto.
- Los p analíticos del DiD-FE cluster (49 clusters, 4 tratadas) son poco fiables, y la rama lo dice.
- Holm/BH internos (m=6 = 3 métodos × 2 resultados por ventana): implementaciones correctas (Holm step-down con máximo acumulado; BH step-up con mínimo acumulado). Es una familia de robustez, no de hipótesis, y solo informa. El Holm-7 se aplica en BS (criterio uniforme (d)). OK.

## 4. H5: resultados y escala de evidencia

| Resultado (ln IPC alquiler, SDiD) | τ | p perm. bilateral |
|---|---|---|
| Tope vigente 2020Q4-2022Q1 | +0,0037 (IC placebo −0,0002; +0,0076) | 0,065 (una cola «−»: 0,97) |
| Tras la anulación 2022Q2-2023Q4 | +0,0055 | 0,36 |
| Placebo en el tiempo (fecha falsa 2018Q4) | +0,0078 | 0,009 |
| Pretendencia SDiD: pendiente / RMS | +0,0003 por año | 0,040 / 0,14 |
| Pretendencia con pesos uniformes: pendiente / RMS | — | 0,010 / 0,010 |
| Barcelona sola (permutación exacta, 45 placebos) | −0,0014 | 0,74 |

- **EXPLORATORIO es coherente.** El signo es contrario al pre-registrado, p > 0,05, el placebo de fecha falsa es significativo y la pendiente pre también. Con el criterio uniforme (c), sin superar la identificación no cabe CAUSAL, y sin Holm-7 ni submuestras no cabe ASOCIACIÓN ROBUSTA. Lectura correcta: **H5 no se confirma, y el diseño no identifica el efecto en el IPC provincial.** El DiD y el SC «significativos» (positivos) no se usan como evidencia, y bien hecho.
- En la regla del código (`nivel = "CAUSAL"` si τ<0, p<0,05, pretendencias y placebo) falta el escalón de ASOCIACIÓN ROBUSTA (Holm-7 y submuestras). Ahora no tiene efecto, pero hay que corregirlo (C6).
- **Potencia y medida (punto 4 del encargo).** El IPC de alquiler del INE mide las rentas que pagan los hogares inquilinos en TODOS los contratos vigentes (el parque), no solo en los nuevos. El tope de la Ley 11/2020 limitaba sobre todo la renta de los contratos nuevos, y solo en los municipios declarados. La rama lo declara de forma cualitativa (notas de resultado.json, desviaciones 11, «Qué NO se puede afirmar»), pero falta: (i) el MDE de H5, que es ≈ 2,8 × 0,0020 ≈ 0,56 % en ln con su propio EE placebo; (ii) una referencia de magnitud esperada. La referencia directa es **Jofre-Monseny, Martínez-Mazza y Segú (2023), «Effectiveness and supply effects of high-coverage rent control policies», Regional Science and Urban Economics 101, 103916, doi 10.1016/j.regsciurbeco.2023.103916**: VERIFICADA (Crossref); cuartil no verificado. Con microdatos de contratos (fianzas), estima una reducción de las rentas de los contratos nuevos de alrededor del 4-6 % en los municipios regulados, sin caída de la oferta (según el resumen publicado). Diluido en el parque y en la provincia, el efecto esperable en el IPC provincial es una fracción de esa cifra, que depende de la rotación de contratos y del peso de los municipios regulados. Con ese denominador, un nulo en el IPC es poco informativo. Debe constar así (C2), y no está en docs/literatura.md (C8).

## 5. evaluar_H6 (puerta)

| Requisito (pre-registro / encargo) | Implementación | Valoración |
|---|---|---|
| Misma estrategia que H5 (SDiD; SC y DiD de robustez) | `bl.run_design` con los mismos estimadores y la misma permutación (B=1000, semilla) | OK |
| Ajuste con entrenamiento «hasta 2024Q2» | ω y λ con pre = 2016Q1-2020Q3 + 2022Q2-2023Q4 (26 trimestres); se excluyen 2024Q1-Q2 (140 municipios ya tratados desde 2024-03-16) y el periodo del tope | Es una desviación del texto literal, declarada (desviaciones 8a-b) y conservadora. Se decidió antes de abrir. OK |
| Efecto 2024Q3-2026Q2 | `post = qrange("2024Q3","2026Q2")` (8); aborta si falta algún dato de las tratadas | OK |
| Donantes = 40 | 49 de entrenamiento − 4 catalanas − {01, 20, 48, 31, 15}. `units_train` sale del panel de entrenamiento, así que las selladas 11, 16 y 45 no pueden ser donantes aunque aparezcan en el panel sellado. Se descarta cualquier donante con NaN (se informa) y se aborta si quedan < 30 | OK (comprobado: 40 donantes, ninguna sellada) |
| Regla | `cumple_regla = tau < 0 and p_bilateral < 0.05` en ln IPC (principal). Δ4, ponderado por share y provincias solas: solo informativos | OK, fiel a hipotesis.md («−») y al criterio uniforme (b) |
| Ensayo en seco | tests/test_bp_h6_sellado.py: pseudo-sellado hecho solo con entrenamiento (≤ 2022Q2, 3 pseudo-selladas, 4 pseudo-tratadas no catalanas). Sin efecto: τ = −0,0045, p = 0,44 (no cumple). Con −0,03 inyectado: τ = −0,0345, p = 0,005 (cumple). Prueba de aborto y prueba AST sin `holdout` | OK, con una carencia: usa un pre contiguo y otro `cfg`, así que no ejercita la configuración real (pre con hueco, 40 donantes). Lo he ejercitado yo (ver abajo) |
| Potencia | `h6_preparacion.json`: DE placebo 0,0062, MDE ≈ 2,8 × DE = 0,0174 en ln (≈ 1,7 %). Ventana pseudo-post de 6 trimestres con un hueco de 2 años respecto al pre: aproximación, probablemente conservadora | **Declarado** en resumen.md. Falta la lectura de lo que implica (C2) |

**Ensayo propio con `CFG_REAL` exacto** (sellado falso: valores de entrenamiento 2022Q3-2024Q2 re-etiquetados como 2024Q3-2026Q2 y encadenados en nivel; 11, 16 y 45 falsas añadidas en todos los periodos; B=100; script en el scratch del revisor, sin tocar data/sealed). 40 donantes, ninguna sellada entre ellos; pre 2016Q1-2023Q4 con 26 trimestres (hueco del tope respetado); post 2024Q3-2026Q2 (8); pesos de share 0,877/0,478/0,468/0,509. Sin efecto: τ = −0,0012, p = 0,76 (no cumple). Con −0,03 inyectado: τ = −0,0312, p = 0,010 (cumple). El camino de código real funciona.

Riesgos que hay que declarar ANTES de abrir (C5): (a) **anticipación**: la resolución TER/2940/2023 (agosto de 2023) precede a la declaración de 2024, y λ se concentrará casi seguro en 2023Q4 (como en H5, donde todo el peso cae en 2020Q3), así que cualquier efecto anticipado en 2023Q3-Q4 sesga τ hacia 0; (b) **paquete catalán**: el DL 3/2023 de viviendas de uso turístico (en vigor 2023-11-09) y la 2.ª ronda (declarada 2024-07-01, efectiva 2024-10-10) entran en el mismo contraste: H6 medirá «Cataluña 2024-2026», no la zona tensionada aislada; (c) el pre 2022Q2-2023Q4 incluye contratos firmados con el tope que siguen en el parque: el intercepto de ω solo absorbe un desplazamiento constante; (d) los choques nacionales (tope del 3 % en 2024, IRAV desde 2025) son comunes y quedan absorbidos solo si su incidencia no difiere entre Cataluña y los donantes.

## 6. Especificaciones no contadas y lenguaje

- registro.csv: 46 filas = 12 (3 métodos × 2 resultados × 2 ventanas) + 4 DiD-FE + 4 pretendencias + 6 placebos de tiempo + 16 por provincia + 1 diagnóstico AR(4) + 2 descriptivos + 1 preparación de H6. Coincide con el código. No constan en el registro: el jackknife (EE secundario, mismo τ), el ajuste de prueba y la potencia de H6 (sí en h6_preparacion.json) y la comprobación de «dos inicios del SLSQP» (desviaciones 3), que no está en el código. No hay barrido de hiperparámetros: ζ es el del paper (`zeta_scale=1` fijo). El historial de la rama tiene un solo commit, así que no puedo comprobar iteraciones previas. Aceptable.
- Comparación con AR(4)/ECM v1: no aplica a un estimador de efecto de política (declarado). El diagnóstico pseudo-OOS (8 obs., DM-HLN p = 0,50) está bien etiquetado como «no es un duelo de predicción».
- Lenguaje: correcto y prudente («no hay evidencia de que el tope redujera...»). Una frase atribuye: «El DiD y SC "significativos" (positivos) **reflejan** esa divergencia previa, no un efecto» → «son compatibles con esa divergencia previa» (C7).
- Datos: solo series oficiales observadas (IPC INE). Sin interpolación ni PDF/OCR en el modelo. Referencias usadas: Arkhangelsky et al. 2021 (AER, Q1), Abadie et al. 2010 (JASA, Q1) y Abadie 2021 (JEL, Q1), todas VERIFICADAS en docs/literatura.md.

**Qué NO se puede afirmar (H5, y H6 antes de abrir):** que el tope no tuviera efecto (el IPC provincial de parque tiene poca potencia frente a un efecto sobre contratos nuevos en algunos municipios; MDE ≈ 0,56 %); nada sobre oferta, precios de compra o municipios concretos; ningún efecto causal (fallan las pretendencias y el placebo de fecha falsa); y de H6, nada hasta su única evaluación. Aun entonces, un nulo no indica ausencia de efecto si es menor que ≈ 1,7 %, y un efecto significativo sería del «paquete catalán 2024-2026», no exclusivamente de la zona tensionada.

## 7. Cambios pedidos (priorizados)

1. **C1 [alta, antes de abrir H6]** `_evaluar`: calcular y fijar `res["DECISION"]` y el bloque PRINCIPAL primero, y envolver cada secundario (Δ4, ponderado por share, provincias solas) en `try/except`, guardando el error como texto, para que un fallo secundario no deje la apertura sin resultado (`holdout.evaluate` solo registra el resultado si `fn` termina). Añadir al test un caso con `CFG_REAL` **exacto** sobre un sellado falso (como el de §5), que ejercite el pre con hueco y los 40 donantes, y medir el tiempo de ejecución. El orquestador debe lanzarlo con `OMP_NUM_THREADS=1`, en segundo plano y con un timeout amplio (≈ 1 min esperado): si se corta, H6 queda quemada.
2. **C2 [alta, antes de abrir H6]** En resumen.md y en el docstring de bp_h6_sellado.py, declarar ex ante: MDE ≈ 1,7 % (H6) y ≈ 0,56 % (H5); que el IPC mide el parque y el tratamiento afecta sobre todo a contratos nuevos en municipios concretos (cita de Jofre-Monseny et al. 2023 como referencia de magnitud en contratos nuevos); y que, por tanto, un no rechazo de H6 se leerá como «no detectable en el IPC provincial», no como «sin efecto».
3. **C3 [media]** Rebasar el índice dentro de la rama a un periodo de entrenamiento (p. ej., media de 2016 = 0 en ln por provincia) antes de SC en H5 y en los secundarios SC de H6; regenerar las tablas de H5 (SDiD y DiD no cambian) y declararlo. Avisar al orquestador de que el IPC viene en base 2025 = 100 (información sellada en los niveles) y revisar los usos en nivel sin FE de unidad en otras ramas (`ratio_precio_alquiler_idx`).
4. **C4 [media, transversal]** `make models` ejecuta `src/v2/[a-z]*_*.py` con `|| exit 1`. `python3 src/v2/bp_h6_sellado.py` sale con código 1 (`raise SystemExit("solo vía...")`), así que `make models` se detiene ahí y nunca llega a `bp_main.py`. `bv_h2_sellado.py` ya en r2/main tiene el mismo problema. Arreglo: excluir `*_sellado.py` de MODELS en el Makefile, o imprimir el aviso y salir con 0.
5. **C5 [media, antes de abrir H6]** Declarar en el docstring y el resumen los riesgos de §5 (anticipación desde 2023 con λ concentrado en 2023Q4, el paquete catalán, contratos del tope en el parque, choques nacionales). Opcional, como secundario informativo fijado ahora: SDiD excluyendo 2023Q3-Q4 del pre.
6. **C6 [baja]** Regla de nivel de bp_main.py: con τ<0, p<0,05 y diagnósticos superados, etiquetar «candidata a CAUSAL (pendiente de Holm-7 y submuestras en BS)», no «CAUSAL».
7. **C7 [baja]** Lenguaje («reflejan» → «son compatibles con»). Declarar el supuesto de intercambiabilidad/homocedasticidad de la inferencia placebo y la poca fiabilidad del jackknife con N_tr = 4.
8. **C8 [baja]** Pedir a lit-researcher que incorpore Jofre-Monseny, Martínez-Mazza y Segú (2023, RSUE 101, 103916) a docs/literatura.md, con el cuartil.
9. **C9 [baja]** `simplex_qp`: comprobar `r.success` y avisar si no converge. Fijar `OMP_NUM_THREADS=1` en la ejecución (el SC sin penalización depende de los hilos) y regenerar las salidas versionadas con esa configuración. Declarar que los pesos catastrales de `zona_tensionada_share` pueden ser de un año sellado (solo afectan al secundario ponderado).

Tras C1-C5 (C3 solo cambia el SC de robustez) basta una re-revisión breve de bp_h6_sellado.py, del test, del resumen y del Makefile. El análisis de H5 y su nivel EXPLORATORIO no cambian.

---

## Re-revisión (iteración 2; commit `300ca59`, con r2/main `d590094` fusionado)

**Reproducción.** Clon nuevo aislado, sin red, `OMP_NUM_THREADS=1`: `bp_main.py` y `tests/test_bp_h6_sellado.py` dos veces, con exit 0 en las cuatro ejecuciones. Los md5 de los 31 ficheros son idénticos entre ejecuciones e idénticos a los versionados (`git status` limpio). Tests nuevos: `test_cfg_real_exacta` (τ −0,0312, p 0,010 con −0,03 inyectado; 6,3 s con B=100) y `test_secundario_falla_no_aborta`, ambos OK. **H6 sigue sin evaluar**: docs/v2/holdout_accesos.md solo contiene H1 y H2.

**Cambios C1-C9: resueltos.** El PRINCIPAL y la DECISION se fijan antes que los secundarios, y cada secundario va en try/except. Se añade el secundario sin 2023Q3-Q4. La DECLARACIÓN EX ANTE (MDE de H6 ≈ 1,7 % y de H5 ≈ 0,56 %, IPC de parque frente a contratos nuevos, Jofre-Monseny et al. 2023, lectura de un nulo) y los riesgos (a)-(f) están en el docstring, en resumen.md y en resultado.json. La etiqueta pasa a «candidata a CAUSAL», se corrige el lenguaje, se añade el contador de QP no convergidos (0) y el Makefile ejecuta solo puntos de entrada con un hilo. El SDiD y el DiD de H5 no cambian con el rebase; H5 sigue EXPLORATORIO.

**Defecto nuevo y bloqueante, introducido por C3 (infraestructura).** `holdout.build` rebasa `ipc_alquiler` a 2015=100 **solo en el entrenamiento** (`_rebase_indices_2015(tr, ...)`). El panel sellado se sigue escribiendo en **base 2025=100** (`df[sell].to_csv(...)`, holdout.py:154). `evaluar_H6` concatena los dos paneles en niveles (`pd.concat([pt, ps])` → `_wide` → `np.log`), de modo que cada provincia salta de nivel entre 2024Q2 y 2024Q3 en ln(P̄_2025/P̄_2015). Como la base 2025 normaliza cada provincia por su propia media de 2025, que ya incluye el efecto, **el estimador anula por construcción el efecto que quiere medir.** Lo he comprobado con el CFG_REAL sobre un sellado falso hecho solo con entrenamiento, dividiendo los niveles «sellados» por su media de 2025:

| Sellado falso | τ SDiD (principal) | p | ¿cumple? | τ Δ4 (secundario) |
|---|---|---|---|---|
| misma base, efecto −0,03 | −0,0312 | 0,010 | sí | −0,0134 |
| base 2025 en el sellado, efecto −0,03 | **−0,0004** | 0,88 | **no** | −0,0205 |
| base 2025 en el sellado, efecto 0 | −0,0004 | 0,88 | no | −0,0205 (espurio) |

Los tests no lo detectan porque construyen el pseudo-sellado a partir del entrenamiento, que ya está en la base 2015. Si se abre H6 así, la única evaluación queda inservible.

### Veredicto final: **REHACER** (no abrir H6 todavía)

Cambios pedidos, todos necesarios antes de `holdout.evaluate("H6", ...)`:
1. **[bloqueante, orquestador]** En `holdout.build`, aplicar al panel sellado el mismo factor por unidad (100 / media de 2015 del índice), que se calcula con datos de 2015 (no sellados), y regenerar data/sealed. Alternativa local en `_evaluar`: reconstruir los niveles post encadenando el `d_ln_ipc_alquiler` sellado (invariante a la base) desde el nivel de entrenamiento de 2024Q2.
2. **[bloqueante, BP]** Guarda en `_evaluar`: abortar ANTES de estimar si |(ln niv[2024Q3] − ln niv[2024Q2]) − d_ln_ipc_alquiler sellado[2024Q3]| > 1e-6 en alguna unidad usada.
3. **[bloqueante, BP]** Test: un pseudo-sellado en otra base (como la tabla) debe abortar por la guarda, o, con la corrección, dar el mismo τ que en la misma base.
4. **[orquestador, transversal]** Revisar cualquier otro evaluador sellado que concatene niveles de `ipc_alquiler`, `ipv*` o `ratio_precio_alquiler_idx` de entrenamiento y sellado (p. ej., H7/BM).

Tras 1-3, basta comprobar la guarda y el test; el resto de la rama está aprobado.

### Para docs/v2/limitaciones.md
- H5: el diseño no identifica (placebo de fecha falsa p=0,009; pendiente pre p=0,04); EXPLORATORIO; signo contrario al pre-registrado.
- IPC de alquiler = parque de contratos vigentes; los topes actúan sobre contratos nuevos en municipios concretos: MDE ≈ 0,56 % (H5) y ≈ 1,7 % (H6); un nulo no prueba ausencia de efecto (Jofre-Monseny et al. 2023: −4/−6 % en contratos nuevos).
- H6 mide el «paquete catalán 2024-2026» (DL 3/2023 VUT, 2.ª ronda); posible anticipación desde 2023 (sesgo hacia 0); los choques nacionales solo se absorben si su incidencia es común.
- Inferencia placebo con 4 tratadas: supone unidades intercambiables; jackknife poco fiable.
- Índices INE en base 2025=100: los niveles sin rebasar llevan información sellada; el SC sin penalización depende de los hilos BLAS (se fija 1 hilo).
- `zona_tensionada_share`: pesos catastrales de un año posiblemente sellado (solo en el secundario).

---

## Verificación final (commit `3d57411`, con r2/main `26d2e83` fusionado)

- **Reproducción.** Clon nuevo aislado, sin red, 1 hilo: `bp_main.py` y los tests dos veces, con exit 0 en las cuatro ejecuciones. Los md5 de los 31 ficheros son idénticos entre ejecuciones y con lo versionado. Entre `300ca59` y `3d57411` el train y output/v2/BP no cambian.
- **holdout.build** (código): `_rebase_indices_2015` se aplica ahora a `df` COMPLETO antes de `_mascara_sellada`. Entrenamiento y sellado quedan en la misma base, y el factor usa solo valores de 2015. Correcto.
- **Guarda** (`UMBRAL_SALTO = 0,05`, fijada antes de abrir): `test_guarda_de_base` pasa. Además, mi sellado falso realista (base 2025 = media propia de 2025) ahora **aborta** (salto máx. 0,215) y ya no anula el efecto. Con la misma base se recupera −0,03 (τ −0,0312, p 0,0099).
- **H6 sigue sin evaluar**: holdout_accesos.md solo contiene H1 y H2.
- **Acceso indebido declarado** (decisiones.md): el orquestador vio dos estadísticos del panel completo, la media de 2015 (= 100) y el máx. |Δln| 2024Q2→Q3 = 0,0129 en el conjunto de provincias, sin separar tratadas y donantes. No informa sobre τ, y el diseño, la regla y el umbral ya estaban fijados. **No afecta a H6.** Que conste en limitaciones.

### Veredicto: **APROBAR**. Se puede ejecutar UNA vez `holdout.evaluate("H6", bp_h6_sellado.evaluar_H6, "BP", ["panel_prov_q"])` con `OMP_NUM_THREADS=1`, en segundo plano. Antes, regenerar data/sealed con el holdout corregido (si no se hace, la guarda abortaría y quemaría la apertura).
