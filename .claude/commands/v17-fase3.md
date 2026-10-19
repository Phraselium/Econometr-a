---
description: V17 · Fase 3 · Auditoría crítica
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 3 · Auditoría crítica: Para cada fila de D1 y cada pregunta de D3, con abogado-del-diablo (dos rondas): argumentos a favor y en contra, pruebas mínimas, veredicto y texto corregido; output/v17/auditoria/ con la tabla «antes / después / por qué». Parada si una conclusión de la 1.0 o del informe integral resulta falsa.
3. Ejecuta solo esta fase (`make v17_f3`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
