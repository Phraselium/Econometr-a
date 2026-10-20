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
