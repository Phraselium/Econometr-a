# Decisiones v6.2

- **E1 · Alcance del anexo.** El anexo cubre las 15 cifras de docs/v5/revision_humana.md con una ficha completa cada una.
  - Cubre también las 49 cifras con marcador en una_pagina, el policy brief y el artículo del Colegio (lista en output/v6_2/lista_cifras_anexo.txt).
  - Las cifras del mismo módulo y método se agrupan en una ficha común con una subficha por cifra, para no repetir la fuente y la fórmula.
- **E2 · Rutas.** Lo nuevo va en src/v6_2/, output/v6_2/ y docs/v6_2/. El código independiente de L2 va en tests/doble_impl/.
- **E3 · L3 en paralelo con L1.** El déficit no depende del anexo. La ficha del déficit del anexo se actualiza con el resultado de L3 antes de L2, si L2 aún no ha empezado, o en una ronda de corrección. Ahorra tiempo de reloj sin cambiar el orden lógico: L2 valida el anexo final.
- **E4 · Integración de L3.**
  - Los entregables citan L3-DEF-2124-SINBAJAS y L3-DEF-2124-CONBAJAS, ambos C2, en lugar de deficit_2124_c1 y c2. Estos se conservan en cifras_clave como históricos: el informe técnico §1 los cita expresamente como «histórico».
  - D3 sustituye el id al leer las referencias (data/raw/v5 es solo lectura).
  - El verificador sustituye V05 por L3-V1.
  - En ERRATA se anota como reclasificación de capa con cambio de rango.
  - La regla de decisión de L3 se pre-declaró antes de mirar los resultados finales. La sensibilidad sin las variantes que conservan el quiebre (551.813-710.542, 12,6 %) se reporta, pero no cambia la capa.
- **E5 · dh_2125 y la EPA** (corregida tras la revisión H2). La premisa era falsa: dh_2125 no usa la constante, porque las medias anuales de la EPA de 2021 y 2025 son posteriores a la ruptura. Se mantiene C1 sin el tratamiento de L3, y el rótulo de la fuente pasa a «EPA (sin corrección…)» en cifras_clave, D3 y las plantillas.
- **E6 · L5.**
  - docs/v6_2/cifras_publicables.md se genera desde cifras_clave (src/v6_2/l5_publicables.py, en make). Las cotas C2 se dan solo como rango.
  - El test tests/test_l5_cifras.py comprueba tres cosas:
    - que el fichero coincide con lo generado;
    - que ningún entregable, post, ficha del verificador ni el anexo cita una cifra sustituida que figure en ERRATA (lista cerrada de valores superados), salvo en líneas marcadas «histórico» o «v6.1»;
    - que las plantillas no usan ids históricos fuera de frases rotuladas como históricas.
- **E7 · Revisión tras L3: REHACER, ronda 1 de 2** (docs/v6_2/revision.md). Lo corrige el orquestador sin subagentes, para no pasar del 80 % del presupuesto.
  - **H1.** Nueva cifra L3-DEF-2124-BAJAST1 (C4), que sustituye a T3-H2 en todos los entregables. Va a ERRATA y a SUPERADOS.
  - **H2.** Véase E5.
  - **H3.** La ventana de la ECP va de 2021T1 a 2025T1, a 1 de enero. El mínimo pasa de 344.803 a 389.361; la capa sigue en C2. Actualizados el anexo, l1_verifica, tests/doble_impl, la ficha, la carta, ERRATA y CHANGELOG.
  - **H4.** La advertencia de inmigración es ahora simétrica y se retira la palabra «canal».
  - **H5.** Sensibilidad L3-DEF-2124-SENS (596.371-710.542) junto al rango en todos los entregables. Se declara en ERRATA, la ficha y la carta que la anterioridad de la regla no consta en git, y qué fija cada extremo.
  - **H6.** Tolerancia de medio paso del redondeo publicado (0,5 % solo con percentiles); la independencia parcial de B1 y D1 queda marcada. Siguen siendo 15/15.
  - **H7.** «Siete alternativas más la constante de v1».
  - **H8.** Los trimestres de la EPA de A1 no se tabulan: se reconstruyen desde raw con el filtro de la ficha. Pasa al backlog.
  - **H9.** Las cifras históricas van en una sección aparte de cifras_publicables. SUPERADOS se amplía; la comparación literal de cadenas es una limitación declarada.
- **E8 · Diferencias del clon limpio** (`make all` ×2 sin red sobre d585b1e: 7.928 s y 8.054 s, rc=0; md5 idénticos entre ejecuciones salvo output/v2/BM/tiempos.json). Frente a lo versionado:
  1. **output/v6/M3B/resultado.json.** Una nota con la «fecha de ejecución» tomada de `date.today()`; la salida cambiaba según el día. Se fija la fecha de la ejecución de v6 (2026-10-11) en src/v6/m3b_run.py, de modo que la salida vuelve a ser la versionada. No es una cifra.
  2. **output/v6_1/K4B/comparacion.csv y resultado.json.** La comparación de la doble implementación de v6.1 no se había vuelto a ejecutar tras corregir A23-A10 en v6.2. Ahora A23-A10 publicado (28,5; 26,1-30,8) difiere de la réplica K4b de v6.1 (24,7 de mínimo) y pasa a «parcial»: 5 coinciden y 5 son parciales. Es un artefacto de auditoría histórico; la doble implementación vigente es L2, con 15/15. Se copia la versión del clon.
  3. **output/v6_1/K4D/resumen.json.** md_revisados era 404 en el repositorio de trabajo y 403 en el clon: contaba .pytest_cache/README.md, que no está versionado. k4d_docs.py excluye ahora las cachés y da 403.
  4. **docs/v2/fallidas/ine.md y tiempos.json.** Dependen del entorno, como en v6 y v6.1; no se copian.
  - Ninguna diferencia afecta a una cifra publicada, así que no hay entrada en ERRATA.
  - Los dos cambios de código (fecha fija y exclusión de cachés) solo hacen que la salida coincida con la del clon. No se repite `make all` por ellos.
