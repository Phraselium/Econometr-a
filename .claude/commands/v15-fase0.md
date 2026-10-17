---
description: V15 · Fase 0 · Punto de partida
---
1. Lee docs/v15/plan.md completo y docs/v15/estado.md. Respeta las reglas A del plan y las condiciones de parada D.
2. Fase 0: comprueba V14.4 y escribe docs/v15/punto_partida.md (≤3 páginas).
3. Ejecuta solo esta fase (`make v15_f0` para sus scripts deterministas). Registra cada subagente con `python3 src/v15/registro_subagentes.py`.
4. Actualiza docs/v15/estado.md (hecho, siguiente, subagentes y tokens), docs/v15/decisiones.md y, si hay bloqueos, docs/v15/bloqueos.md.
5. Termina con `make check` en solitario (ningún otro proceso escribiendo en el repositorio), commit por tarea y push solo a la rama designada (`git push -u origin r12/analisis:claude/housing-price-spain-econometric-95dhj3`).
6. Resumen final de 250 palabras como máximo: qué se ha hecho, qué preguntas sobreviven y por qué, qué se ha descartado y por qué, tokens de subagentes y qué toca al autor.
