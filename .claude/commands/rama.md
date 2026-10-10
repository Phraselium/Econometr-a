---
description: Lanza una rama v2 en su worktree con smoke test, resultado.json, revisión y actualización de estado.
---
Rama: $ARGUMENTS
1. Lee docs/v2/estado.md, docs/v2/plan.md, docs/v2/hipotesis.md y docs/v2/decisiones.md (sección de la rama).
2. Trabaja SOLO en ../wt-$ARGUMENTS (rama git r2/$ARGUMENTS); ficheros: src/v2/$ARGUMENTS_*.py y output/v2/$ARGUMENTS/. econ_utils y data/ solo lectura.
3. Smoke test con una submuestra antes del run completo; si tras el smoke test y una iteración no hay señal, documenta resultado negativo y cierra.
4. Escribe output/v2/$ARGUMENTS/resultado.json (esquema en CLAUDE.md) y registro de especificaciones.
5. Pasa la puerta del reviewer (opus). REHACER → solo cambios pedidos, máx. 2 iteraciones; lo que persista → docs/v2/limitaciones.md.
6. Si APROBAR, fusiona r2/$ARGUMENTS en r2/main. Actualiza docs/v2/estado.md (hecho / siguiente / tokens).
