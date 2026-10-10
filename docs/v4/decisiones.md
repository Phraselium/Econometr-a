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

## Revisión de la oleada A: REHACER (docs/v4/revision_oleadaA.md)
- A2, corregido por el orquestador. La convención B compara la cota de precio con la subida OBSERVADA del periodo: la afirmación queda NO RESPALDADA solo si la cota es inferior al 50 % de esa subida. El borrador anterior comparaba con el 50 % en niveles, y era un error. Resultado:
  - V01 con B: ANALIZADA, NO CONCLUYENTE. La cota es el 133 % de la subida con |ε|=0,33; con |ε|=1 sería el 44 %.
  - V03 con B: ANALIZADA, NO CONCLUYENTE (79 % de la subida de compra).
  - V11: sin cambio entre convenciones.
  - B no cambia la capa.
- A7. V13 pasa a ANALIZADA, NO CONCLUYENTE: se analizaron indicadores y no se hizo el test GSADF. La cifra del BdE va como NO VERIFICADA (DOI no comprobado).
- A1, A3-A6, A8-A10 y A11 están devueltos a M1, M2 y M0. M3 lee M1 en tiempo de ejecución.
- Gestión: tras la revisión hay 5 subagentes activos a la vez (M3, M4 y las correcciones de M0, M1 y M2). Supera el máximo orientativo de 3. Ninguno usa worktree ni comparte ficheros de salida.

## M3: ¿se puede construir? (umbrales declarados antes de clasificar)
- Clases: 4 déficit <= 0; 3 brecha <= 0; 2 precio > r(coste + suelo repercutido), r en {1,25; 1,5}; 1 brecha > 0 sin ser 2 y con solares suficientes; 5 (añadida) brecha moderada con solares insuficientes; 9 sin dato de solares.
- Multiverso (324 especificaciones x variantes de déficit M1): margen 15/20/25 %; edificabilidad 0,8/1,2/1,6; coste 900/1.200/1.500 EUR/m2 (supuesto externo no verificado); suelo todos o >50.000 hab.; viviendas por solar 5/10/20. C2 si la clase modal aparece en >= 80 %.
- Los umbrales no se fijaron con M1. m3_run lee M1 en ejecución; los recuentos son PROVISIONALES hasta corregir M1 (error de terminadas).
- Municipios sin valor tasado propio usan el precio provincial (proxy, siempre C4). La capa efectiva se limita a la del déficit de M1.
- M3, revisión: segundo intento de coste en nivel sin resultado. Licencias y visados del Boletín Online (BoletinOnline2 y BoletinOnline, orden 10000000) y el INE no traen presupuesto de ejecución material; el Catastro extraído no trae superficie construida, así que V_CONSTRUCCION/m2 no se puede calcular. Brecha y clasificación pasan a C4 («coste en nivel supuesto»); la ficha M3-V1 se apoya solo en solares y suelo.
