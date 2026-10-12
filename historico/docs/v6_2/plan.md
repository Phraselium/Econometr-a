# Plan v6.2 — cierre final para revisión externa

Rama `r6.2/main`, creada desde `r6.1/main` en 7a63f9f (cierre de v6.1). Push solo a `claude/housing-price-spain-econometric-95dhj3`.

Presupuesto de subagentes: 0,6 M tokens. Corte al 80 % (0,48 M) y reserva del 10 % (0,06 M) para el cierre.

| Tarea | Contenido | Tope | Quién |
|---|---|---|---|
| L1 | Anexo metodológico: 15 cifras de revision_humana y 49 cifras más de una_pagina, el policy brief y el artículo del Colegio | 0,20 M | general-purpose |
| L2 | Segunda doble implementación, solo con el anexo y data/raw; test en tests/doble_impl | 0,15 M | general-purpose (sonnet) |
| L3 | Déficit con correcciones alternativas de la EPA; capa C1 o C2; respuesta al árbitro | 0,10 M | econometrician |
| Revisor | Tras L3: anexo, doble implementación y capa del déficit | ≤0,05 M | reviewer (opus) |
| L4 | Inmigración: efecto total frente a directo | 0,05 M | orquestador o subagente pequeño |
| L5 | Coherencia final de cifras, test y cifras_publicables.md | 0,04 M | orquestador |
| L6 | Guía del revisor y tareas_autor | 0,03 M | orquestador |

Orden: L1 → L2 → L3 → revisor → L4 → L5 → L6 → `make all` ×2 en un clon limpio → cierre.
