# Estado V7

## Hecho
- Preparación: rama r7/main.
- Instalados pymc, arviz, arch, libpysal y spreg; versiones añadidas a requirements.lock.

- R0 (v6.3), R1 (paneles) y R2 (herramientas con validación Monte Carlo, REHACER atendido) hechos. Pre-registro cerrado con etiqueta prereg-v7.
- Acumulado de subagentes: unos 366.000 tokens (28 %).

## Siguiente
- R4a (núcleo: MG_dm, PMG_dm, CS-DL, DFE, ecuaciones y diagnósticos) y R4b (jerárquico, LP, regulación, provincia) en curso.
- R0 (subagente D2 + verificador), R1 (panel) y R2 (herramientas + Monte Carlo) en curso; R0 del orquestador hecho (V2).

## Tokens de subagentes (presupuesto 1,3 M; corte 1,04 M)
| Módulo | Tope | Usado |
|---|---|---|
| R0 (subagente D2 + verificador) | 60.000 | 96.591 (excedido; V5) |
| R1 panel | 120.000 | 96.994 |
| R2 herramientas (ronda 1) | 130.000 | 60.561 |
| R2 herramientas (ronda 2) | +55.000 | ~30.000 (declarado; ver aviso) |
| Revisor R2 | 40.000 | 48.945 (excedido) |
| R2 (total de las 3 rondas, según el sistema) | 150.000 (módulo) | 123.485 |
| R4a núcleo | 220.000 | 105.239 |
