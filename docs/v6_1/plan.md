# Plan v6.1 — cierre, auditoría crítica y consolidación

Rama de trabajo: `r6.1/main`, creada desde `r6/main` en 08d7629 (cierre de v6). Push solo a `claude/housing-price-spain-econometric-95dhj3`.

V1-V6 están cerradas. Solo se corrige lo que esta auditoría encuentre como error. Todo lo nuevo va en:
- src/v6_1/;
- output/v6_1/<MÓDULO>/;
- docs/v6_1/.

## Presupuesto de subagentes: 1,4 M tokens

Corte al 80 % (1,12 M). Reserva del 10 % (0,14 M) para el cierre.

| Módulo | Contenido | Tope | Subagente |
|---|---|---|---|
| K1 | Líneas base exigentes en la misma validación sellada v6; DM con corrección de muestra pequeña y permutación por provincias | 0,15 M | ml-engineer |
| K2 | Historial de conclusiones v1-v6; inmigración, cambiando una dimensión cada vez | 0,25 M | econometrician |
| K3 | Iniciadas: adelantos y retardos; léxico de importancia; ratio P/A con varias medidas | 0,08 M | econometrician |
| K4a | Auditoría de código y estadística, con tests nuevos | ≈0,2 M | general-purpose (sonnet) |
| K4b | Doble implementación de las 15 cifras, sin ver el código | ≈0,15 M | general-purpose (sonnet) |
| K4c/K4d | Coherencia de cifras; documentación y publicación | ≈0,15 M | general-purpose |
| K5 | Revisión por pares simulada (académica y de política pública) y carta de respuesta | 0,15 M | reviewer (opus) |
| K6 | Backlog, tareas del autor, entregables y la sección «qué cambió» | 0,1 M | orquestador o general-purpose |
| Revisor | Tras K2 y al final; REHACER como máximo 2 veces | — | reviewer (opus) |

## Orden

K1 ∥ K4a ∥ K4b → K2 → revisor → K3 → K4c/K4d → K5 → K6 → revisor final → `make all` ×2 en un clon limpio → cierre.

`make check` se pasa en cada puerta.
