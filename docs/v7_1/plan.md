# Plan V7.1: consolidación final y estructura para publicación

Rama r7.1/main, creada desde r7/main (3d1170c, v7.0).

Reglas:
- **Sin análisis nuevo.** No se estiman modelos nuevos ni se abre ninguna muestra sellada. S1 reutiliza las extracciones de Monte Carlo de R6, con la misma semilla y los mismos supuestos; solo hace contabilidad de dosis y coste.
- **Versiones.** V1-V7 están cerradas. La v7.1 pasa a ser la versión de referencia y la v6.2 queda como histórica.

## Presupuesto de subagentes: 0,65 M

- Corte al 80 % (0,52 M).
- Reserva del 10 % (0,065 M) para el cierre.
- Cada subagente recibe un tope y para al 80 % de él.
- Las síntesis y la revisión de coherencia las hace el orquestador.

En V7 se superaron los topes de: inventario, revisores, R0 y entregables (R7). Por la regla de disciplina, estos tipos de tarea los hace el orquestador. Solo se delega lo acotado y nuevo: la verificación de literatura de S2 (lit-researcher) y el revisor único de control.

| Módulo | Tope | Quién |
|---|---|---|
| S1 Dosis y coste | 0,15 M | orquestador (contabilidad sobre las extracciones de R6) |
| S2 Nota metodológica | 0,15 M | orquestador (texto) + 1 lit-researcher (DOI y cuartiles; tope 60k) |
| S3 Consolidación | 0,15 M | orquestador (plantillas → render) |
| S4 Ensayo de evaluate_v7 | 0,08 M | orquestador |
| S5 Estructura | 0,06 M | orquestador |
| S6 Paquete de publicación | 0,05 M | orquestador |
| Control (revisor único, opus) | 0,08 M | 1 reviewer (tope 80k; si lo supera, revisa el orquestador y lo declara) |

## Orden

S1 → S2 → S3 → S5 → control → S4 → S6 → cierre.

El cierre consiste en:
1. `make v7` ×2 en un clon limpio sin red;
2. `make publicacion`;
3. `make check`;
4. `make all` ×1.
