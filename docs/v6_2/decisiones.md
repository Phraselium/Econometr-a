# Decisiones v6.2

- **E1 · Alcance del anexo.** El anexo cubre las 15 cifras de docs/v5/revision_humana.md con una ficha completa cada una.
  - Cubre también las 49 cifras con marcador en una_pagina, el policy brief y el artículo del Colegio (lista en output/v6_2/lista_cifras_anexo.txt).
  - Las cifras del mismo módulo y método se agrupan en una ficha común con una subficha por cifra, para no repetir la fuente y la fórmula.
- **E2 · Rutas.** Lo nuevo va en src/v6_2/, output/v6_2/ y docs/v6_2/. El código independiente de L2 va en tests/doble_impl/.
- **E3 · L3 en paralelo con L1.** El déficit no depende del anexo. La ficha del déficit del anexo se actualiza con el resultado de L3 antes de L2, si L2 aún no ha empezado, o en una ronda de corrección. Ahorra tiempo de reloj sin cambiar el orden lógico: L2 valida el anexo final.
- **E4 · Integración de L3.**
  - Los entregables citan L3-DEF-2124-SINBAJAS y L3-DEF-2124-CONBAJAS, ambos C2, en lugar de deficit_2124_c1 y c2. Estos se conservan en cifras_clave como históricos: el informe técnico §1 los cita expresamente como «histórico».
  - D3 sustituye el id al leer las referencias (data/raw/v5 es solo lectura).
  - El verificador sustituye V05 por L3-V1.
  - En ERRATA se anota como reclasificación de capa con cambio de rango.
  - La regla de decisión de L3 se pre-declaró antes de mirar los resultados finales. La sensibilidad sin las variantes que conservan el quiebre (551.813-710.542, 12,6 %) se reporta, pero no cambia la capa.
