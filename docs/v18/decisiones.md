# V18 · Decisiones

## K0. Punto de partida: V17 dentro de V18 (2026-10-19, orden del autor)
- V17 no existía en el repositorio. El autor entregó su plan (docs/v17/plan.md) y ordenó ejecutar de V17 las fases 0-3 y 5 antes de la infraestructura y las fases de V18.
- La fase 4 de V17 no se ejecuta. El Documento de Trabajo de la fase 6 de V18 (publicacion/documento_v18/) integra su contenido e incluye además las secciones de V17 sobre demografía, problema general o local, factibilidad de construir, discurso público y medidas auditadas.
- CLAUDE.md: la línea de V16 se sustituyó por la de V18, porque no había línea de V17. Debajo se añadió la remisión a V17.

## K1. Infraestructura C (2026-10-20)
- **Puerta.** La etiqueta plan-replicacion-v18 es local; la puerta exige además que su commit esté en la rama remota (así vale aunque el proxy no deje subir etiquetas; plan, fase 3).
- **Fase 3.** El plan dice que el hook rechace la fase 3 y las siguientes sin la etiqueta. Por eso el plan de replicación se escribe, se revisa y se etiqueta sin make; el objetivo de la fase 3 solo comprueba el plan ya etiquetado.
- **Guarda (g).** Mira solo las órdenes, no el texto de un heredoc entrecomillado que escribe un fichero.
- **Lenguaje causal.** check_v18 aplica una lista de expresiones causales a las cifras V18 que no son IDENTIFICADO; el texto del Documento de Trabajo se revisará además con check_texto y con el árbitro.
- **Fuga v6.** La guarda de check_v17 (K5 de V17) ya cubre src/v18/.

## K2. Lenguaje causal y capas en V18 (decisión del autor, 2026-10-20)
- Choque señalado por el revisor del pre-registro (hallazgo 4) y por el abogado del diablo (T3): B3 del plan permite hablar de causa en IDENTIFICADO; CLAUDE.md y metodologia/capas.md reservan el lenguaje causal a C3/C3s, y C3 exige evaluación en muestra sellada.
- **Decisión: opción restrictiva con evaluación sellada diferida.**
  - Toda cifra V18 es C4 (nivel_evidencia EXPLORATORIO). La clasificación V18 (IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE, NO ESTIMABLE) va en el campo clasificacion_v18, al lado de la capa.
  - En IDENTIFICADO solo cabe la fórmula condicional «con los supuestos X, el diseño identifica…», y solo en las secciones técnicas del Documento de Trabajo (resultados por factor y anexos). Nunca en cifras_clave, la web, la consulta, el resumen ejecutivo ni el resumen no técnico. check_v18 rechaza el lenguaje causal en todas las cifras V18, también en IDENTIFICADO.
  - Vía a C3: una evaluación sellada diferida (evaluate_v18) con datos posteriores al pre-registro, que se fija en la adenda del plan. Los episodios históricos (Ley 11/2020, auge 2000-2008) no pueden llegar a C3 con la definición actual de capas.md, y se dice.
- **Diagnóstico de make check (2026-10-20).** El fallo sin test fallido del cuarto make check de V18 lo produjo el worktree del subagente del plan, creado dentro del repositorio mientras corría; pytest en solitario pasa (746). Los worktrees de subagentes se excluyen en .git/info/exclude y no se crean mientras corre make check.

## K3. Pre-registro interno de V18: plan + adenda y etiqueta (2026-10-20)
- El pre-registro interno lo forman docs/v18/plan_replicacion.md (d4e9869) y docs/v18/plan_replicacion_adenda.md, que responde a los 28 hallazgos del revisor (APTO CON CAMBIOS) y a todos los del abogado del diablo, sin haber mirado ningún resultado de V18. La etiqueta local plan-replicacion-v18 se pone en el commit de la adenda.
- **sellar_v18 y evaluate_v18.** El autor eligió en K2 la vía de la evaluación sellada diferida; la adenda (1.11) fija ahora qué se evalúa, con qué datos, cuándo y el criterio de superación. Las funciones de src/holdout.py se escriben en la versión que ejecute evaluate_v18 (no antes de 2027: los datos posteriores mínimos todavía no existen), con orden expresa del autor; dentro de V18 no se sella ni se evalúa nada.
- **docs/v18/sellado_v18.json** (topes de entrenamiento por variable, regla 1.4 de la adenda) lo genera de forma determinista, solo con metadatos, src/v18/f3_sellado.py después de la etiqueta y antes de la primera estimación.

## K4. Sellado de entrenamiento de V18 (2026-10-20)
- docs/v18/sellado_v18.json (src/v18/f3_sellado.py, solo metadatos, después de la etiqueta): 100 combinaciones variable|nivel|frecuencia con su tope y regla (a)-(f) de la adenda 1.4, y 13 fuentes que se descargarán después de la etiqueta (sin tope: src/v18/sellado.filtrar da error con ellas hasta que se registren). Excluidas: 8 CCAA y 11 provincias de v6; 853 municipios de V15 y 777 de V16; 1.211 distritos de V15 y 1.118 de V16; 161 municipios con distritos sellados como fuga declarada (total municipal, adenda 1.5).
- **trans_total:** la regla (e) daría 2026T1 y el Anexo C fija 2024T4: se aplica el más restrictivo.
- **Distritos sellados en v3.** No se excluyen: su muestra sellada ya se abrió en v3 (una evaluación por hipótesis, docs/v3/decisiones.md) y la sección A del plan V18 enumera como selladas las de v6, V15 y V16. Se dice en el Documento de Trabajo.
- Un subagente usó una vez un heredoc entrecomillado para editar f3_sellado.py (permitido por CLAUDE.md, que solo prohíbe los heredocs sin comillas); sin efecto en el resultado.

## K5. Monte Carlo de las herramientas de la sección 1.13 (agente montecarlo, 2026-10-20)
- **Qué hay.** src/v18/herramientas/ (did, dcdh, aleatorizacion, honest_did, sdid, lp_iv, svar_proxy, meta_bayes), src/v18/montecarlo/ (un conductor por herramienta, procesos generadores _dgp_did y _dgp_itp, utilidades), tests/v18/test_herramientas_*.py y salidas en output/v18/montecarlo/<herramienta>/{resultado.json, tabla.csv, informe.md}. Todo simulado, SEED 20261010, `ALCANCE_TERRITORIAL = "sin lectura de datos"`; ningún dato real de resultado ni muestra sellada.
- **Criterio.** El del encargo (tamaño al 5 % en [0,03; 0,08] y cobertura al 95 % en [0,92; 0,97], bajo el nulo y bajo la alternativa) y, en la columna banda_112, las bandas de la adenda 1.12 (apta: tamaño [0,04; 0,06] y cobertura [0,93; 0,97]; con valor crítico corregido; no fiable). R = 2.000 en paneles y aleatorización, 5.000 en LP-IV, 3.000 en SVAR y metaanálisis; el bootstrap de bloques del SVAR (≈ 600 réplicas) es información y no decide. B = 999 permutaciones o réplicas bootstrap (499 en Sun-Abraham y aleatorización) frente a las 9.999 del plan para el análisis real.
- **Veredictos** (la condición completa está en cada informe.md):
  - **cs_webb: APTO CONDICIONADO.** APTO en los diseños municipales (50-150 tratados, T = 8, 13 y 17, dos cohortes, 10 tratados): tamaño 0,056-0,071, cobertura 0,93-0,96 con cluster = municipio. NO APTO con 8 clusters (E8): 0,178.
  - **sa_webb: APTO** en los siete diseños (0,058-0,071), con 8 CCAA en el límite (0,0685) y frágil: 0,0805 y 0,0920 si las CCAA de control son 4 y 5.
  - **dcdh_aleatorizacion: APTO** con la aleatorización del calendario entre 8 CCAA (0,0455-0,0535, cobertura 0,95-0,96, ℓ = 4 y ℓ = 0, tamaños de CCAA desiguales o no). El bootstrap de Webb con 8 clusters es NO APTO (0,12-0,15). El 0,0775 de V16 no se reproduce y su causa no queda identificada.
  - **honest_did: APTO CONDICIONADO.** Solo con M̄ = 0 (0,0655 con 50/100 y 0,0545 con 150/300; 0,082 con 100/200, en el borde). Con M̄ = 0,5 y 1 en la frontera el tamaño es 0 y la potencia ≈ 0: válido, no informativo (IC95 de ancho 0,20 con M̄ = 1). Con 8 clusters la covarianza tiene rango <= 7 y el tamaño con M̄ = 0 es 0,17.
  - **sdid_conley_taber: APTO** con 2, 5, 10 y 25 tratados y con País Vasco (T = 40, 3 posteriores): 0,0445-0,056, cobertura 0,937-0,956, si los tratados son intercambiables con los controles; con tratados 2 veces más variables el tamaño es 0,44.
  - **aleatorizacion: APTO** (E2 entre municipios 0,0635 con 100/200 y 0,053 con 10/150; E8 0,053-0,0575).
  - **lp_iv: NO APTO.** Newey-West h + 1: 0,07-0,115 con instrumento F >= 10. Bajo el nulo el AR aumentado con EHW es el único cercano al nominal en todas las fuerzas (0,049-0,069) y el 2SLS aumentado va de 0,041 a 0,079 con F >= 10; pero la cobertura bajo la alternativa es 0,77-0,96 (0,82-0,87 con instrumento fuerte): con T = 108 la LP queda atenuada un 10 %, 22 % y 38 % a h = 4, 8 y 12 (casi nada con T = 1.000).
  - **svar_proxy: NO APTO.** AR por método delta: APTO solo con F ≈ 10 (0,032-0,040); con F ≈ 27 tamaño 0,057-0,072 y cobertura 0,87-0,90 bajo la alternativa; con F ≈ 4 conservador (0,014-0,019).
  - **meta_bayes: NO APTO por conservador.** Calibración exacta (0,95); con verdades fijas la cobertura de μ es 0,96-0,99 (K <= 4 y τ = 0,25) y 0,99-1,00 con τ pequeño; el prior s/2 queda corto en calibración (0,85-0,92); con K = 2 el efecto fijo cubre μ solo 0,50-0,56 con heterogeneidad.
- **Lo que esto significa para el plan (solo lectura; el plan no se toca).**
  - E8: la inferencia por aleatorización es la única válida con 8 CCAA; Webb y el t de Student con 8 clusters no lo son. E2: la aleatorización entre municipios vale (0,0635; dentro de la comarca 0,052).
  - E2 y E8, Honest DiD: con M̄ = 1 el IC95 solo excluiría el cero si el efecto supera ≈ 0,10 en log; el criterio «IC con M̄ = 1 excluye el cero» no se alcanzará con efectos de la magnitud de la literatura (−0,044).
  - E7-R1: el Newey-West de h + 1 se publica con la etiqueta de distorsión; el AR aumentado con EHW es el intervalo a mirar con F < 10, y las estimaciones de la LP a h = 8 están atenuadas en T = 108.
  - E2-A1, A2: SDID con Conley-Taber vale con 2 a 25 tratados si son intercambiables; si los tratados son más variables que los controles (grandes municipios), no.
  - B5: la regla de «decisión coincidente en las tres priors» parte de intervalos conservadores; con K = 2 el efecto fijo no cubre μ si hay heterogeneidad (se muestra con esa advertencia).
- **Aprendido de V16 y aplicado.** Nulo impuesto sobre el agregado y EE recalculado dentro de cada bootstrap (cs_webb); covarianza agrupada al nivel del tratamiento (honest); cobertura por inversión del mismo contraste; diseños con la estructura de V18 y diagnósticos que rompen a propósito el supuesto (variabilidad de los tratados, 4-5 CCAA de control, sorpresa gaussiana).

## K6. Escritores en paralelo sin worktrees (2026-10-20)
- Cada worktree ocupa unos 1,5 GB y el disco de la sesión tiene unos 4 GB libres: al crear dos a la vez se llenó (fallaron sin efecto en lo versionado). Los subagentes que escriben trabajan en el árbol principal, como máximo 3 a la vez, cada uno en ficheros y carpetas propios (src/v18/estimacion/<estudio>.py, output/v18/estimacion/<estudio>/); el orquestador revisa y hace commit, y no se lanza make check mientras escriben.

## K7. Clasificación tras la ronda 1 del abogado del diablo (B6; 2026-10-20)
- Se aplican las reglas del plan tal como están escritas, sin reinterpretarlas a la vista del resultado:
  - **E8-R1 → ASOCIACIÓN.** El cambio de signo sin 2012-2013 es una prueba B4 del plan y un cambio de signo en B4 es fallo decisivo (plan, línea 124); el «tope SUGESTIVO» de la adenda (R-18) es un techo y no anula esa regla. Además depende de fechas no verificadas con el BOE.
  - **E2-R1c → ASOCIACIÓN.** Falla el placebo de fecha (p = 0,0005) y persiste la diferencia tras la STC (tope de la adenda, línea 581). No existe la clase «SUGESTIVO sin significación»: un resultado no significativo es NO CONCLUYENTE si supera I1-I5 y ASOCIACIÓN si no.
  - **E2-R1 → SUGESTIVO provisional**, pendiente de la réplica ciega (I8), de las pruebas 1-2 de la ronda 1 (tendencia del efecto y salto en 2022T2; HUT 2019 × trimestre) y de la ronda 2. El M̄ de ruptura queda «no evaluable» (desviación C2, decidida antes de estimar, porque el Monte Carlo de Honest DiD con M̄ > 0 no tiene potencia); se dice en la ficha.

## K8. E1-R4 (Sagrada Família) tras la réplica ciega (B6; 2026-10-20)
- La réplica ciega, con la principal de la adenda (centroide a menos de 500 m frente al anillo de 500-1.000 m; 21 y 56 secciones no selladas; 5 barrios), da 0,0011 (IC95 de Webb [−0,047; 0,072]) frente a 0,0018 del modelizador, cuya muestra (77 frente a 693 secciones) corresponde a la lectura «radio de 1 km frente al resto de Barcelona», es decir, a la variante v1 de la adenda, no a la principal.
- Regla B6: con la réplica en desacuerdo no se clasifica hasta resolverlo. Se resuelve a favor de la ficha del pre-registro: la principal es la de la réplica y la del modelizador pasa a ser la variante v1.
- Con la principal, el contraste de equivalencia (TOST, δ = 0,05) no acota el nulo (IC90 [−0,038; 0,054]): **E1-R4 → NO CONCLUYENTE (sin potencia)**. El script de E1 se corrige para que la principal siga la adenda.

## K8 bis. Corrección de K8 (E1-R4; 2026-10-20)
- **La premisa de K8 era errónea.** 693 eran observaciones (77 secciones × 9 años), no secciones de control: la principal del modelizador ya comparaba el radio de 500 m con el anillo de 500-1.000 m. El modelizador corrigió la geometría (centroide en UTM 31N: 22 y 55 secciones; una sección queda a 499,7 m con la geometría del INE y a 507,3 m con la del Ajuntament) y el TOST (IC90 de Webb por inversión).
- **Lo que separa las dos estimaciones** es una lectura de la ficha: el modelizador incluye los adelantos de 2011-2012 como regresores (estudio de eventos; 0,0026, IC90 [−0,026; 0,039]: nulo acotado) y la réplica estima la diferencia en diferencias sin ellos (0,0017 con las mismas secciones, IC90 [−0,026; 0,053]: no acotado).
- **Decisión.** El plan (sección 1, E1-R4) define la principal como «diferencias en diferencias» de las secciones del radio frente al anillo; los adelantos son el diagnóstico de pretendencias, no parte de la estimación. Además, cuando la ficha admite dos lecturas y dan clases distintas, se toma la más prudente. **E1-R4 → NO CONCLUYENTE (sin potencia)**; la versión con adelantos se publica al lado como variante, con su IC90.
