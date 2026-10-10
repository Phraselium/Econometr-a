# Plan v5 (MODO AUTÓNOMO V5 MAESTRO)

Autor: Borja Romero, economista (firma individual, independiente). Ámbito: España por provincias + módulo València.
Fecha de corte: la última disponible en cada fuente; cada dato lleva su fecha en output/v5/cifras_clave.csv.

## Orden y presupuesto (tokens de subagentes)
| Módulo | Límite | Corte 80 % | Contenido |
|---|---|---|---|
| R recuperación | 0,9 M | 0,72 M | R0 backlog; R1 pendientes no cubiertos por A-E |
| A cierre v4 | 0,7 M | 0,56 M | cifras_clave; IPV vs resto; alquiler stock/nuevos; coste oficial y reclasificación; programas oficiales; topes y GL |
| B necesidades y territorio | 1,0 M | 0,80 M | necesidad 2026-2035; proyección del déficit 2026-2030; diferencias provinciales; contribuciones a la subida |
| C ángulos | 0,7 M | 0,56 M | C1-C8 (≤0,1 M cada uno), por impacto |
| D política | 0,6 M | 0,48 M | matriz completa; política por territorio; convergencia |
| E publicación | 0,6 M | 0,48 M | E1-E12 |
| Reserva cierre/revisor | 0,42 M (10 %) | — | correcciones y revisiones |
| **Total** | **4,2 M** | **3,36 M** | La suma de límites (4,5 M) supera lo disponible (3,78 M sin reserva): manda el corte global. |

- Revisor (opus) una vez por módulo; REHACER como máximo 2 veces.
- `make check` en cada puerta, con las comprobaciones nuevas de v5.
- Pre-registro: tag `prereg-v5` antes de lo confirmatorio (B3).
- Lo que no quepa vuelve a docs/v5/backlog.md con motivo y coste.
