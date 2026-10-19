---
description: V17 · Fase 1 · Datos que faltan
---
1. Lee docs/v17/plan.md, docs/v17/decisiones.md, docs/v17/estado.md y docs/v18/plan.md. Respeta las reglas A y las paradas E de V17. Todo lo de V17 es a posteriori y se rotula así.
2. Fase 1 · Datos que faltan: Solo lo necesario para la auditoría y D3 (plan, fase 1): turismo local, migración y hogares, crédito y compras, titularidad, parque social, renta y oferta. Hasta 3 adquisidor-datos en paralelo; data/raw/v17/<familia>/ con manifiesto, licencia y sha256.
3. Ejecuta solo esta fase (`make v17_f1`). Registra cada subagente con `python3 src/v17/registro_subagentes.py` (tope 4 millones de tokens por fase).
4. Actualiza docs/v17/estado.md, docs/v17/decisiones.md y, si hay bloqueos, docs/v17/bloqueos.md.
5. `make check` en solitario, commit por tarea y push solo a la rama designada.
6. Resumen de 250 palabras como máximo.
