---
description: V16 · Fase 4 · Preguntas nuevas, diseños y pre-registro interno V16
---
1. Lee docs/v16/plan.md completo y docs/v16/estado.md. Respeta las reglas A del plan y las paradas D.
2. Fase 4 · Preguntas nuevas, diseños y pre-registro interno V16: Q1-Q10 con potencia recalculada; rejilla multiescala fija; sellar_v16; docs/v16/preregistro_v16.md; revisor-preregistro y abogado-del-diablo (solo lectura, pueden ir en paralelo); adenda; etiqueta prereg-v16 publicada en el remoto. Sin parada si la etiqueta se publica.
3. Ejecuta solo esta fase (`make v16_f4` para sus scripts deterministas). Registra cada subagente con `python3 src/v15/registro_subagentes.py` y anota los tokens de la fase en docs/v16/estado.md (si una fase supera 6 millones de tokens de subagentes, para y explícalo).
4. Actualiza docs/v16/estado.md (hecho, siguiente, subagentes y tokens), docs/v16/decisiones.md y, si hay bloqueos, docs/v16/bloqueos.md.
5. Termina con `make check` en solitario, commit por tarea y push solo a la rama designada (`git push origin HEAD:claude/housing-price-spain-econometric-95dhj3`).
6. Resumen de 250 palabras como máximo: qué se ha hecho, qué preguntas sobreviven y por qué, qué se descarta y por qué, tokens y qué toca al autor.
