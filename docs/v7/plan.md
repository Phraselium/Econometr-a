# Plan V7: atlas econométrico regional

Rama r7/main, creada desde r6.2/main (462ebf1). v6.2 es la versión de referencia congelada: sus cifras publicables no cambian salvo error demostrado, y entonces se publica como v6.3 y se anota en ERRATA. Lo nuevo va en src/v7, output/v7, docs/v7 y tests/v7.

## Presupuesto de subagentes: 1,3 M

- Corte al 80 % (1,04 M).
- Reserva del 10 % (0,13 M) para el cierre.
- Cada subagente recibe un tope explícito y debe parar al 80 % del suyo.
- Si un tipo de tarea supera su tope, el orquestador la hace él mismo a partir de ahí.

| Módulo | Tope | Quién |
|---|---|---|
| R0 Higiene y pendientes | 0,08 M | orquestador más 1 sonnet (D2 con T3, min/max de cifras_clave) |
| R1 Panel regional | 0,15 M | 1 sonnet |
| R2 Herramientas y Monte Carlo | 0,15 M | 1 sonnet |
| Revisor tras R2 | 0,04 M | opus |
| R3 Pre-registro y evaluación diferida | 0,07 M | orquestador más 1 sonnet pequeño (`make evaluate_v7`) |
| R4 Modelos explicativos | 0,40 M | 2 sonnet: (a) integración, cointegración, PMG/MG/DFE, CS-ARDL y ecuaciones; (b) jerárquico, proyecciones locales, descomposición y provincia |
| Revisor tras R4 | 0,05 M | opus |
| R5 Predicción | 0,12 M | 1 sonnet |
| R6 Propuestas | 0,20 M | 1 sonnet |
| R7 Entregables | 0,10 M | 1 sonnet |
| Revisor final | 0,04 M | opus |

## Orden

R0 → R1 → R2 → revisor → R3 → R4 → revisor → R5 → R6 → R7 → revisor → `make v7` ×2 y `make all` ×1 en un clon limpio → cierre.
