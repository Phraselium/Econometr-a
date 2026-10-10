# Decisiones v4

## Setup (2026-10-10)
- Rama r4/main desde r3/main (5eab0db). CLAUDE.md apunta a docs/v4 y añade la regla de evaluar instrumentos, no partidos.
- `check_texto` se amplía a output/v4. La procedencia literal de las medidas de los programas (con el nombre del partido) va en un anexo de datos (CSV) que no escanea el control de léxico partidista. Los textos evalúan instrumentos.
- Sin worktrees, como en v3: espacios de nombres por módulo (src/v4/mN_*, output/v4/MN/) y commits solo del orquestador. El disco libre es de 5,5 GB.

## M0: cierre de v3 (orquestador)
- **Verificador v4** (`src/v4/verificador.py`, que se ejecuta después del v3 en `make verificador`). El veredicto «SIN EVIDENCIA SUFICIENTE» se divide en dos:
  - «ANALIZADA, NO CONCLUYENTE» (V01, V03, V04, V06, V07, V12, V14);
  - «NO ANALIZADA: FALTAN DATOS» (V02, V09, V10, V13), cada una con su motivo.

  Las fichas con cota de precio (V01, V03, V12) muestran su veredicto bajo las dos convenciones:
  - A, estricta: traducciones a precio en C4;
  - B, estructural: esas traducciones como C2.

  En V01 la convención B da NO RESPALDADA; en V03 y V12, PARCIALMENTE.
- **Topes (H3-3), contaminación declarada.** El cálculo de potencia de v3 estimó P-C3 con municipios que luego quedaron sellados (O1), y la validación por fuente (SERPAVI) mide el mismo mercado en los mismos municipios. Por eso H3-3 queda fuera de C3 de forma definitiva, aunque los criterios a-c se cumplieran en una reestimación. Se dice en las fichas V06 y V07 y en el texto v4.
