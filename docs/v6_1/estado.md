# Estado v6.1

## Hecho
- Preparación: rama `r6.1/main` desde 08d7629; creado docs/v6_1/; CLAUDE.md apunta a v6.1.

## Siguiente
- K1, K4a y K4b en paralelo.

## Tokens de subagentes (presupuesto 1,4 M; corte al 80 %: 1,12 M)
| Módulo | Tokens |
|---|---|

## En curso
- K1 (ml-engineer), K4a (sonnet) y K4b (sonnet), lanzados en paralelo.
- Para K4b se preparó docs/v6_1/k4b_especificacion.md: las 15 cifras sin referencias al código original.
- K1 terminado: unos 90.000 tokens; integrado en make (V6_1_ORDEN). cifras_clave ahora también lee output/v6_1/*/hechos.json.
- K4a está en curso. Este commit es intermedio e incluye correcciones parciales de K4a (fianzas Incasòl): ver docs/v6_1/auditoria_K4a.md cuando termine.
- K4b terminado (unos 175.000 tokens). De las 15 cifras: 5 coinciden, 5 coinciden en parte y 5 no se pueden reconstruir con lo publicado.
  - Los fallos de descripción del déficit van a la auditoría consolidada:
    - la corrección EPA es una constante fija;
    - la segunda fuente de terminadas es MIVAU con y sin protegida, no Catastro;
    - las ventanas de hogares difieren.
  - Ver docs/v6_1/doble_implementacion.md.
- K4a terminado (unos 235.000 tokens): 11 hallazgos (0 críticos, 2 altos, 3 medios, 6 bajos).
  - Los dos altos están corregidos: K4a-01, redondeo de recuentos, y K4a-02, fianzas de Incasòl. Ambos van en ERRATA.
  - 31 tests nuevos.
- K2 lanzado (econometrician).
- K2 terminado (unos 240.000 tokens). El cambio de inmigración lo mueven tres dimensiones: método (2SLS frente a MCO), control de población (correlación 0,66 dentro de provincia) y medida de alquiler. Conclusión única: C4, «ANALIZADA, NO CONCLUYENTE». k2_inmigracion entra en make y es determinista.

## Consumo acumulado de subagentes
- K1: 90.376
- K4b: 170.138
- K4a: 234.566
- K2: 240.357
- Total: 735.437 de 1.400.000 (53 %).
- Margen hasta el corte del 80 %: 384.563 tokens.

Plan de ahorro (D7): revisor post-K2 ≤60.000, K3 ≤70.000, K4c/K4d ≤90.000, K5 ≤120.000, revisor final ≤60.000. K6 y la consolidación de la auditoría las hace el orquestador.
- K3 terminado (unos 50.000 tokens).
  - Iniciadas: ni los retardos ni los adelantos se distinguen de cero, y no se detecta orden temporal.
  - Léxico: 18 frases corregidas en las plantillas; también en m2_tablas.py y m4_run.py, para que make no las revierta.
  - Ratio precio/alquiler: 2015 entre 18,9 y 20,3 años; 2023 entre 17,1 y 17,7 años (provincial). Con contratos nuevos el ratio sale 3-6 años menor.
- Revisor tras K2 (unos 74.000 tokens) y K2 rehecho una vez, solo el texto (unos 10.000 tokens): ver D9.
- K4c y K4d en curso.
- Acumulado: unos 920.000 tokens (K1 90k, K4b 170k, K4a 235k, K2 250k, revisor 74k, K3 50k, más K4c/K4d en curso).

## K4c y K4d (terminados, unos 85.000 tokens)
- Hecho: coherencia de cifras (0 huérfanas ni contradictorias reales en output/v5/*.md; 26 huérfanas de ficha en el verificador), enlaces (0 rotos), versión 6.1, DECLARACION_IA.md, marcas de cuartil en docs/literatura.md. Detalle: docs/v6_1/auditoria_K4cd.md.
- Siguiente: commit de estos cambios (hacen pasar `make check` en check_v5); en el cierre, `make all` y verificar con red los cuartiles pendientes.
- K4c/K4d terminado (139.884 tokens, por encima de su tope de 90.000).
  - Entregables principales: 0 cifras huérfanas y 0 contradicciones reales.
  - 32 enlaces rotos corregidos.
  - Versión 6.1 en CITATION, .zenodo.json y README.
  - DECLARACION_IA.md creada.
  - 50 referencias marcadas «cuartil no verificado».
  - k4c y k4d entran en make.
- **Consumo acumulado de subagentes: 1.008.814 de 1.400.000 (72 %).**
  - Hasta el corte del 80 % quedan unos 111.000 tokens, para K5 (≤100.000).
  - El revisor final (≤60.000) sale de la reserva de cierre del 10 %.
  - K6 lo hace el orquestador.
- K6 (parcial, orquestador): docs/v6_1/backlog.md y docs/v6_1/tareas_autor.md (definitivo) escritos; K4a-07 cerrado (0 de 30 pliegues omitidos).
