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
