---
description: Invoca al subagente reviewer (Opus) sobre el estado actual del proyecto y devuelve APROBAR / REHACER.
---
Invoca al subagente `reviewer` sobre el estado actual (fase indicada en argumentos o la última completada). Debe ejecutar `make all`, aplicar su checklist
y escribir docs/revision_<fase>.md. Muestra el veredicto y la lista de cambios; si es REHACER, planifica las correcciones antes de avanzar.
Fase: $ARGUMENTS
