# Plan v2

Objetivo: explicar la subida de precios (compra) y alquileres en España, sobre todo desde 2014 y 2020, separando alquiler y compra, y medir el impacto de cada familia de variables por periodos. Punto de partida v1 (output/informe.md): N=74 trimestres nacionales, sin poder predictivo frente al AR(4), identificación débil, quiebre en 2014; empleo asociado al precio real; inmigración asociada al alquiler y no a la compra; València sube en valor tasado más que con el IPV.

Estrategia: subir el N con paneles (52 provincias trimestral, municipios anual, ~27 países UE anual), más variables, parámetros cambiantes y no linealidades.

## Etapas
1. Paso 0 · setup (orquestador).
2. Paso A (paralelo) · literatura v2 (lit-researcher) + B0 datos (data-fetcher por fuente + data-cleaner): panel provincial trimestral, panel municipal anual, panel UE anual, base de eventos de política, coste de uso (Poterba), precio/alquiler, esfuerzo de acceso.
3. Puerta G0 (orquestador) · viabilidad por rama, docs/v2/hipotesis.md (pre-registro, tag `prereg-v2`), sellado del holdout (últimos 8 trimestres 2024T3-2026T2 + 3 provincias con semilla fija) vía src/holdout.py, worktrees.
4. Ramas (máx. 3 en paralelo; ≈0,6 M tokens de subagentes cada una): BA alquiler · BV compra · BI inmigración · BO oferta y suelo · BT turismo/no residentes/inversores · BP política · BM modelos. Cada una con smoke test, resultado.json y puerta del reviewer.
5. BD · descomposición por periodos con contrafactuales e intervalos.
6. BS · síntesis → output/v2/informe_v2.md.
7. Cierre · make all sin red ×2 idéntico, commit y push.

## Reglas de rama
Ver CLAUDE.md y .claude/commands/rama.md. Ramas fusionadas en r2/main solo si el reviewer aprueba.
