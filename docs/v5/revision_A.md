# Revisión independiente · Módulo A de v5 (cierre de v4)

Revisor independiente; no ha participado en el trabajo. Fecha: 2026-10-10. No se ha ejecutado `make all` ni se ha leído data/sealed.

## Reproducción
- Se ejecutaron `src/v5/a23_run.py`, `a4_run.py`, `a5_run.py` y `cifras_clave.py` sin red (`HTTPS_PROXY=http://127.0.0.1:9`). Los cuatro terminan con exit 0, y después `git status` queda limpio: las salidas son idénticas byte a byte a las versionadas.
- `python3 src/v5/check_v5.py`: 0 errores. `python3 src/v3/check_texto.py`: 0 errores.

## Respuestas a las preguntas del encargo
- **Puente IPV frente al núcleo.**
  - El residuo de −30,9 pp está en C4, y las notas dicen que «no se descompone con los datos del repositorio». Es correcto.
  - Falla otra cosa: el propio IPV (+79,9 %) figura como C1. Es de fuente única y queda fuera del núcleo que se usa como referencia: 1,799/1,561 = +15,2 %, por encima de la tolerancia del 15 %. Véase B1.
- **Alquiler de stock C1 (IPC frente a IPVA).**
  - Se aceptan como independientes. El IPC sale de la recogida de precios del INE y el IPVA de declaraciones IRPF cruzadas con el Catastro; que ambos los publique el INE no hace común el dato de origen.
  - El rango 10,9-22,9 % es C1 como banda.
  - El valor central 20,6 es una mediana dominada por el grupo AEAT, porque dos de las tres series son IPVA (N3).
  - La fila A23-A1 (solo IPC, 2015-2025, C1) no es aceptable (B1).
- **Contratos nuevos C1 en Cataluña y C. Valenciana.**
  - Se aceptan. El IPVA (IRPF) y los registros de fianzas (Incasòl, GVA) son fuentes administrativas independientes. Sus niveles quedan dentro del 15 %: 1,172/1,166 en Cataluña y 1,308/1,224 = 1,069 en la C. Valenciana.
  - Conviene acotar el periodo en el veredicto de la ficha (N6).
- **Clase territorial C2 con el MBC de 1993 más el índice.**
  - Exigir que la clase sea la misma en la unión 422-1.500 €/m² es una condición aceptable para el componente de coste: es una cota con un supuesto explícito, c ≤ 1.500 €/m².
  - Con esa condición la clase sigue sin poder ser C2. «Falta» depende de un déficit 2021-2025 que el propio módulo etiqueta como C4 (a4_run.py:407-409), y el código reconoce que `capa_estricta_B5 = C4` en todas las provincias (a4_run.py:21-23 y 223).
  - Debe quedar en C4 (B2).

## Hallazgos

| # | Tipo | Fichero:línea | Hallazgo | Corrección |
|---|---|---|---|---|
| B1 | **Bloqueante** | src/v5/a23_run.py:550, 561, 563, 565; 557, 586, 589, 591 | Hay filas de fuente única promovidas de capa, contra la regla B5. **A23-P1** (INE IPV, C1): queda fuera del núcleo, a +15,2 % en nivel. **A23-P6** (Registradores, 2.284 €/m², C1) y **A23-P7** (Notariado, 1.949 €/m², C1): cada una es de fuente única, y juntas difieren un 17 %, por encima de la tolerancia. **A23-A1** (IPC 2015-2025, C1): una sola fuente, y además en un periodo distinto del núcleo 2015-2024, así que el mismo indicador aparece con dos periodos (13,6 frente a 10,9). **A23-P4, P8 y P9** (C2): son reponderaciones puntuales de una sola fuente, no cotas. **A23-A8** (C2): su componente IPVA es C4. | P1, P6, P7, A1, P4, P8 y P9 pasan a C4. A8 pasa a C4, o queda en C2 solo si se reformula como cota superior y se declara que el componente IPVA la limita a C4; por la regla del mínimo debe ser C4. Para A1, eliminar la fila o dejar un único periodo para el IPC. Regenerar cifras_clave y comprobar la capa mixta de resultado.json (línea 656). |
| B2 | **Bloqueante** | src/v5/a4_run.py:221 y 404; output/v5/A4/resultado.json («capa», «nivel_evidencia»); output/v5/cifras_clave.md:111; docs/v5/decisiones.md:55 | La clase provincial de 2021-2025 se etiqueta C2 aunque «falta» depende de un déficit C4 (2021-2025) y de P y suelo de fuente única (MIVAU). El código lo reconoce (`capa_estricta_B5 = C4`). Es una promoción de capa. | `capa = C4` en todas las clases. Se puede conservar «estable en la unión 422-1.500 €/m², márgenes y r» como diagnóstico de robustez, no como capa. Si se quiere una C2, solo cabe para 2021-2024 (déficit C1) y si P y suelo son al menos C2; si no, nada. Corregir decisiones.md:55, el .md y las figuras A4 (barras C2/C4). |
| B3 | **Bloqueante** | output/v5/A5/hechos.json (no lo genera ningún script); docs/v5/decisiones.md:65 | Las cifras de A5-H01 a H04 están **tecleadas a mano**, contra la regla A1 de no teclear cifras. Además, A5-H01 = 25 es erróneo: el inventario tiene 22 documentos oficiales (6 programas + 1 resumen + 2 normas + 13 proposiciones = 22), y `resultado.json` da `documentos_oficiales_con_texto: 22`. | Generar hechos.json en a5_run.py a partir de inventario.csv, conciliacion_v4.csv y validacion_precision.json. Corregir «25» en decisiones.md:65 y en la cobertura de H01. |
| B4 | **Bloqueante** | src/v5/check_v5.py (`sumas`); output/v5/A4/ | La comprobación «suma provincial = nacional» es vacía: no existe ningún `output/v5/*/control_sumas.json`, así que siempre pasa. La igualdad se cumple en los datos (resultado.json A4, `reconciliacion_prov_nacional`), pero no se controla. | Hacer que a4_run.py escriba `output/v5/A4/control_sumas.json` con déficit, ΔH, libres y protegidas en 2021-2024 y 2021-2025. Que check_v5 falle si falta el control de una tabla declarada (como mínimo A4). |
| N1 | No bloqueante | output/v5/cifras_clave.csv: A23-P3, P4, P10; A4-001; A4-prov-*; A5-H01 a H04 | `fecha_dato` = 2026-10-10, que es la fecha de cálculo, no la del dato. | Poner la última fecha de los datos de entrada (p. ej. 2025T4 o 2026T2) y dejar la fecha de cálculo en notas. |
| N2 | No bloqueante | output/v5/cifras_clave.md:37-46; a4_run.py:404 | Las filas de clases ponen en `min` el número de provincias C2 sin rotularlo, y se lee como un intervalo de incertidumbre. | Separar en una columna o id `n_estables`, o explicarlo en el indicador. Con B2 resuelto, rotularlo como «estables (diagnóstico)». |
| N3 | No bloqueante | a23_run.py:569-571 | El valor central 20,6 de A23-A2 es la mediana de tres series, dos de ellas del grupo AEAT. | Dar solo el rango, o la mediana por grupos. |
| N4 | No bloqueante | a23_run.py:555 | El rótulo de A23-P3 enumera componentes entre paréntesis, y se puede leer como atribución. | «Residuo no identificado del puente (sin descomponer; candidatos: método, calidad, tamaño, cobertura)». |
| N5 | No bloqueante | a23_run.py:557, 559 y 684 (resultado.json:148-149); output/v5/A6/nota.md:23 | Hay verbos de atribución en un análisis contable: «Efecto de pesos», «empuja a la baja», «NO explica» y «la atenuación … explica». | Sustituirlos por «diferencia contable por pesos», «con pesos provinciales la variación es mayor», «no reduce la diferencia» y «es compatible con». |
| N6 | No bloqueante | output/v5/A23/fichas_verificador.json (A23-V2) | El veredicto CONTRADICHA en Cataluña y la C. Valenciana se apoya en la banda 2021-2024, pero la ficha no lo dice. La «Dirección C1» no indica su ámbito. | «CONTRADICHA en 2021-2024 en Cataluña y C. Valenciana»; «dirección C1 en Cataluña y C. Valenciana». |
| N7 | No bloqueante | docs/v5/fuentes_fallidas.md:63; src/v5/a5_run.py:158-159 | Aparecen nombres de formaciones fuera del inventario y del CSV de medidas. | Usar doc_id y leer la correspondencia de inventario.csv. |
| N8 | No bloqueante | output/v5/A5/recuentos.csv; output/v5/A5/resultado.json («notas») | Donde se usan los recuentos no se da la precisión medida (50 % para medidas, 78 % para medidas o menciones, n = 40). Solo figura en cifras_clave (A5-H04). | Añadir una columna o cabecera de nota en recuentos.csv y la cifra en las notas de resultado.json: «cota de coincidencias, no de medidas». |
| N9 | No bloqueante | check_v5.py (`recuentos`, `topes_c3`) | Los recuentos solo se comprueban en «a favor». `topes_c3` solo busca el literal «[C3]» en .md y no mira fichas JSON ni «C3» sin corchetes. El léxico de E4, E5 y E8 lo cubre check_texto (plantillas y output/v5 *.md), no check_v5 como dice decisiones. | Comprobar también «en contra», ampliar `topes_c3` a JSON y a «C3», y alinear el texto de decisiones con lo que de verdad se comprueba. |
| N10 | No bloqueante | src/v5/cifras_clave.py:49-52 | Las cifras de `latente_convivencia` (188.000 y 506.000) están tecleadas; solo se valida con un `assert` sobre el texto. | Extraerlas del campo de origen. |
| N11 | No bloqueante | output/v5/A6/nota.md:14 | La cita de García-López et al. (2020) no lleva la marca VERIFICADA / NO VERIFICADA ni el cuartil. | Añadir DOI y cuartil de Scimago, o «NO VERIFICADA». |
| N12 | No bloqueante | a23_run.py:82; ficha A23-V1 | La tolerancia del ±15 % en nivel admite 12 pp de diferencia de crecimiento dentro de un C1 (10,9 frente a 22,9). | Dar la tolerancia junto a cada C1 del núcleo. |

## Lo que se cumple
- **A1.** La tabla única de cifras tiene periodo, cobertura, fuentes y fecha en todas las filas. Las clases 1-4 y 9 están definidas, la 4 con «no implica exceso de oferta». Los adaptadores de v4 leen de JSON y CSV (salvo N10). La comprobación de lecturas no versionadas está activa.
- **A5.** El diccionario está declarado y es reproducible. Los 3 programas en copias de medios se excluyen de los recuentos. Las normas van aparte. Los recuentos se rotulan como cota C4 y no se evalúan medidas.
- **A6.** Los topes no aparecen en C3 en ningún fichero de output/v5 ni de las plantillas. La explicación de García-López es prudente: C4, «ni refutado ni confirmado», y separa lo que se puede cuantificar de lo que no.
- No hay lenguaje causal ni partidista en las conclusiones, salvo los matices de N5.

## Veredicto: **REHACER**
Prioridad: B1 → B2 → B3 → B4. Son correcciones de etiqueta y de generación; no requieren nuevas estimaciones. Tras ellas hay que regenerar cifras_clave y pasar `make check`.
