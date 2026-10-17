---
description: V16 · Fase 0 · Punto de partida
---
1. Lee docs/v16/plan.md completo y docs/v16/estado.md. Respeta las reglas A del plan y las paradas D.
2. Fase 0 · Punto de partida: Etiquetas prereg-* en el remoto (si el proxy lo rechaza: docs/v16/bloqueos.md y tareas_autor), preregistro_tipo en proyecto.json, comprobación de las correcciones previas, plantilla de una_pagina.md por tipo de cifra y docs/v16/lo_ya_visto.md. Sin subagentes que escriban.
3. Ejecuta solo esta fase (`make v16_f0` para sus scripts deterministas). Registra cada subagente con `python3 src/v15/registro_subagentes.py` y anota los tokens de la fase en docs/v16/estado.md (si una fase supera 6 millones de tokens de subagentes, para y explícalo).
4. Actualiza docs/v16/estado.md (hecho, siguiente, subagentes y tokens), docs/v16/decisiones.md y, si hay bloqueos, docs/v16/bloqueos.md.
5. Termina con `make check` en solitario, commit por tarea y push solo a la rama designada (`git push origin HEAD:claude/housing-price-spain-econometric-95dhj3`).
6. Resumen de 250 palabras como máximo: qué se ha hecho, qué preguntas sobreviven y por qué, qué se descarta y por qué, tokens y qué toca al autor.
