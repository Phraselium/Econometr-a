# Revisión independiente v6.2 (tras L1-L3; L4-L5 ya aplicados)

Revisor independiente, 2026-10-12. Lectura dirigida (no se leyó data/sealed; no se ejecutó `make all`, porque el presupuesto lo impedía). Las cifras de las fichas muestreadas se recalcularon a mano.

## Veredicto: REHACER

El anexo, la doble implementación y la regla de capa del déficit están bien en lo esencial. Hay, sin embargo, una cifra publicada que L3 no ha actualizado (H1). También hay una etiqueta errónea en dh_2125 (H2) y una ventana desalineada que mueve el mínimo publicado (H3). Corregido esto, se puede aprobar sin otra revisión completa.

## Hallazgos (por prioridad)

**H1 · ALTA · El déficit con bajas estimadas no se ha recalculado tras L3.**
- Dónde: `output/v5/cifras_clave.csv` (T3-H2: 653.097, rango 562.692-744.144; T3-H3: «nuevo máximo» frente a 902.808). Se cita en `informe_tecnico.md:74`, `working_paper.md:100`, `lo_que_sabemos.md`, `policy_brief.md`, `articulo_colegio.md`, `ponencia/diapositivas.md` y `linkedin/01.md`.
- Problema: el mínimo 562.692 es el mínimo de las variantes de hogares de v1, ya sustituidas. Con las variantes de L3 y las bajas de v5.1 T1 (0 a 55.452), el rango es 344.803-765.994. Además, la comparación con «902.808» ya no sirve: el máximo C2 vigente es 924.658.
- `test_l5_cifras.py` no lo detecta, porque «562.692-744.144» no está en SUPERADOS.
- Corrección:
  1. Recalcular T3-H2 y T3-H3 en `l3_deficit.py` con las 24 combinaciones × bajas v5.1 (min/central/max). Se mantienen en C4.
  2. Regenerar los entregables y anotarlo en ERRATA, porque cambia una cifra publicada.
  3. Añadir «562.692-744.144» y «902.808» (sin marca de histórico) a SUPERADOS.

**H2 · MEDIA · E5 parte de una premisa falsa: dh_2125 no usa la constante 242.400.**
- En `src/v4/m2_run.py:totales` el ajuste solo se aplica si `a < 2021 <= b`. Para 2021-2025 (a = 2021) no se aplica, y las dos medias anuales de la EPA (2021 y 2025) son posteriores a la ruptura. El anexo A1 lo dice bien.
- Recomendación sobre E5: **mantener C1 y no aplicar el tratamiento de L3**, porque no hay salto dentro de la ventana.
- Hay que corregir:
  - el texto de E5 en `docs/v6_2/decisiones.md`;
  - la columna fuente de dh_2125 en `cifras_clave.csv` y en `cifras_publicables.md`: «EPA (corregida por la ruptura de 2021)» debe pasar a «EPA sin corrección (ambos extremos posteriores a la ruptura)»;
  - la frase del anexo «la EPA corregida del rótulo coincide…».
- Riesgo residual ya declarado: la ECP es un stock a 1 de enero y la EPA, una diferencia de medias anuales. Debe seguir declarándose.

**H3 · MEDIA · Ventana desalineada en las variantes e y d1 de L3.**
- Las dos terminan en ECP(2024T4), que es el stock a 1 de octubre de 2024. La variante e cubre 15 trimestres (el propio código lo dice: «ventana un trimestre más corta»). Las terminadas, en cambio, son de los años naturales 2021-2024.
- El mínimo publicado (344.803 = d1 − Catastro) sale de ese recorte.
- Con ECP(2025T1) = 19.521.046 el resultado cambia:
  - e = 981.823;
  - d1 = 774.811;
  - el mínimo pasa a 389.359;
  - la capa sigue siendo C2 (amplitud de alrededor del 29 %).
- Corrección: usar ECP(2025T1) como final de la ventana 2021-2024, o publicar las dos ventanas (si dos métodos discrepan, se reportan ambos). Actualizar A5/A6, L3-V1, D3 y ERRATA.

**H4 · MEDIA · Inmigración (L4): advertencia asimétrica y lenguaje de canales.**
- Dónde: `lo_que_sabemos.md:73-78`, `policy_brief.md:55-60`, `working_paper.md:231-236`, `informe_tecnico.md:724` y K2-V1.
- El bloque «Por qué la directa puede engañar» advierte solo contra una de las dos especificaciones. La total también puede recoger cualquier factor provincial que mueva a la vez la población y el precio, como el empleo o la costa. Eso se ve en el propio texto: con demanda externa, la total en compra baja a 1,6 (-0,79 a 4,0).
- «Canal» y «elimina ese canal» son lenguaje de mediación (causal) en C4.
- Corrección:
  - Añadir la advertencia simétrica: «la total puede recoger otros factores asociados al crecimiento de población; ninguna de las dos identifica un efecto».
  - Cambiar «canal» por «componente contable del crecimiento de la población (INE, Estadística de Migraciones)».
  - Lo demás está bien: la separación total/directa es correcta, los números de K2-V1 cuadran con los entregables y el veredicto es neutral.

**H5 · MEDIA · Regla de L3: no se puede comprobar que se declarara antes, y el universo incluye variantes que el propio análisis considera erróneas.**
- La regla (`REGLA` en `l3_deficit.py`) entra en el mismo commit que los resultados (bd21a0f). El plan (8a50aaa) no la contiene.
- La capa C2 depende solo de la amplitud. Esa amplitud la generan las variantes a y d1, que conservan un quiebre conocido. Sin ellas, el rango es 551.813-710.542 y la amplitud del 12,6 % cumpliría C1, porque la independencia sí se cumple.
- No es una promoción de capa, y C2 es la opción conservadora. Pero el mínimo de la cota se apoya en un supuesto («no corregir la ruptura») que no es defendible como supuesto de Manski.
- Corrección:
  - Declarar en D/ERRATA que la anterioridad de la regla no consta en git.
  - En la ficha C2, nombrar el supuesto que fija cada extremo (mín = sin retirar el salto, escala ECP; máx = trimestres vecinos con MIVAU sin protegida).
  - Publicar la sensibilidad junto al rango en todos los entregables, no solo en el informe técnico.

**H6 · BAJA · Doble implementación: la tolerancia es laxa y la independencia, parcial.**
- `comparar.py:coincide` acepta un 0,5 % relativo. En cálculos deterministas sobre los mismos datos raw eso permite errores de unas 1.700-5.000 unidades en el déficit y en dh_2125.
- Corrección: usar como tolerancia medio paso del redondeo publicado, y el 0,5 % solo donde haya interpolación de percentiles.
- B1-H1/B1-H4 y D1-H11/H12 leen tablas intermedias de src (`B1_nacional.csv`, `clasificacion_provincias.csv`). Para esas cifras la doble implementación no es independiente. Hay que marcarlas así en `comparacion.csv` y en el resultado.json de L2.
- El test sí falla si cambia una cifra de cifras_clave por encima de la tolerancia.

**H7 · BAJA · El número de variantes no es el mismo en todos los textos.**
- El informe técnico y L3-V1 dicen «siete variantes». El anexo habla de 8 (siete alternativas más la constante de v1).
- Corrección: unificar como «siete alternativas más la constante de v1 (8 variantes)».

**H8 · BAJA · Anexo.**
- A1 no tabula los 8 trimestres de la EPA de 2021 y 2025 que usa; se puede reconstruir con raw y el filtro, pero conviene añadirlos.
- A16 depende de la clase A4 (tabla intermedia, declarado). La clasificación A4 en sí no se puede reconstruir desde la ficha.
- Las fichas breves sí incluyen fuente, filtro, fórmula y script, y el aviso de que no se han verificado es honesto.
- Muestreo recalculado (A1, A5 y A16-A17): coincide (b, c, d1, d2, e, la amplitud del 34,7 % y las εs y medianas de las clases 1 y 2).

**H9 · BAJA · Cobertura de L5.**
- SUPERADOS hace comparación literal de cadenas: no detecta otros formatos (por ejemplo «562 692» o «0,56 millones»), ni T3-H2/H3 (véase H1).
- `cifras_publicables.md` incluye deficit_2124_c1 y c2 en las líneas 34-35. Hay que confirmar que están en una sección de «históricos/no citar», o sacarlos de la tabla publicable.


## Respuesta del orquestador (ronda 1 de 2)
Los hallazgos H1-H9 están aplicados según la decisión E7 de docs/v6_2/decisiones.md. H8 pasa al backlog. Con esta ronda se cierra el REHACER: las correcciones son las que propone el revisor y están verificadas con `make check`.
