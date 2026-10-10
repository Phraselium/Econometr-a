# Decisiones v4

## Setup (2026-10-10)
- Rama r4/main desde r3/main (5eab0db). CLAUDE.md apunta a docs/v4 y añade la regla de evaluar instrumentos, no partidos.
- `check_texto` se amplía a output/v4. La procedencia literal de las medidas de los programas (con el nombre del partido) va en un anexo de datos (CSV) que no escanea el control de léxico partidista. Los textos evalúan instrumentos.
- Sin worktrees, como en v3: espacios de nombres por módulo (src/v4/mN_*, output/v4/MN/) y commits solo del orquestador. El disco libre es de 5,5 GB.
