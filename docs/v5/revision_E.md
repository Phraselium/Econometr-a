# Revisión independiente del módulo E (publicación) de v5

Revisor independiente. Fecha: 2026-10-10. Objeto: los entregables renderizados en output/v5 y los documentos de publicación. No he reejecutado `make all` ni he leído data/sealed.

## Comprobaciones ejecutadas
- `python3 src/v5/render.py`: 0 marcadores sin resolver. `python3 src/v5/check_v5.py`: 0 errores. `python3 src/v3/check_texto.py`: 0 errores.
- Los controles automáticos pasan, pero no detectan los defectos de renderizado ni el de unidades que se describen abajo. Para buscarlos he usado expresiones regulares sobre las palabras duplicadas, «—», NaN y la representación de listas de Python.
- He comprobado al azar 3 de las 15 entradas de `docs/v5/revision_humana.md`. Las tres coinciden con el código: `src/v5/a23_run.py:567` (A23-A2), `src/v5/cifras_clave.py:28` (deficit_2124_c1) y `src/v5/b1_run.py:433` (B1-H1). He revisado además la n.º 8, que está desfasada (N4).
- Longitud de LinkedIn: entre 563 y 860 caracteres por publicación, todas por debajo de 1.300. Hay 10 publicaciones.
- Requisitos que se cumplen:
  - Informe técnico: unas 9.200 palabras y 13 figuras, con matriz, política por territorio, módulo València, convergencia y limitaciones.
  - Working paper: resumen, abstract y apéndices A (datos), B (replicación) y C (IA e independencia).
  - Tres artículos con 4 revistas cada uno, cada revista con su cuartil o la marca «cuartil no verificado».
  - Ponencia: 14 diapositivas y guion.
  - una_pagina: 8 afirmaciones, solo C1 y C2.
  - Titulares de E4, E6 y E8: solo C1 y C2.
  - No aparece ninguna C3. Ningún partido ni ninguna persona en los textos.
- Coherencia con docs/v5/decisiones.md:
  - D3: «2 coincidencias» en el informe y en el artículo del Colegio.
  - Déficit 2021-2025 en C4 (informe técnico:76 y tabla de D3).
  - Clases territoriales en C4.
  - CC-V2 en C4 en el verificador.

## Hallazgos

| # | Tipo | Dónde (renderizado → plantilla) | Problema | Corrección |
|---|---|---|---|---|
| B1 | **Bloqueante** | una_pagina.md:11, linkedin/03.md:3, articulos/a_necesidades.md:131 → plantillas `una_pagina.md:11`, `linkedin/03.md:3`, `articulos/a_necesidades.md:131` (y :7, :55, :72), `lo_que_sabemos.md:18`; origen: id `E-B1-F` en `src/v5/e_hechos_*.py` | La misma proyección del INE aparece con dos unidades y dos juegos de fuentes. Con `B1-H4` sale como «1.720.540 **hogares**» (fuentes INE 54562 y 36726). Con `E-B1-F` sale como «1.720.540 **viviendas**» (fuentes «INE mortalidad; Censo; MIVAU; Catastro»). En el texto divulgativo esto confunde crecimiento de hogares con necesidad de viviendas, en la pieza más leída (una página) y en un titular C2 de LinkedIn. Incumple el criterio 3 (coherencia). | En `E-B1-F`: unidad = «hogares» y fuentes = las de `B1-H4`. Mejor aún, sustituir `E-B1-F` por `B1-H4` en las plantillas. Volver a ejecutar `cifras_clave.py` y `render.py`. |
| B2 | **Bloqueante** | Defectos de renderizado visibles en textos publicables (criterio 4) | (a) Unidad duplicada «hogares hogares»: articulo_colegio:33, informe_tecnico:84, ponencia/guion:11 → plantillas `articulo_colegio.md:33` (`{{latente_convivencia:rango}} hogares más`), `informe_tecnico.md:84` (`{{B1-H4:valor}} hogares más`), `ponencia/guion.md:11` (`{{dh_2125:valor}} hogares más`). (b) «viviendas viviendas»: plantilla `informe_tecnico.md:361`; «del stock del stock»: plantilla `informe_tecnico.md:336`. (c) «desde 2015 desde 2015»: plantillas `linkedin/06.md:5`, `lo_que_sabemos.md:40`, `working_paper.md:129` (la unidad de `CA-EU-hpi_real-crecimiento` ya incluye «acumulado desde 2015»). (d) «— viviendas» como valor: plantilla `informe_tecnico.md:70` usa `{{deficit_2124_c1:cita}}`, cuyo valor central está vacío. (e) Lista de Python «['INE Proyección…', …]» en las fuentes: articulo_colegio:15, ponencia/diapositivas:62 y :68 (ids `B1-H1` y `B1-H4`; origen en la llamada `H(...)` de `src/v5/b1_run.py:433`, que pasa las fuentes como lista). | (a-c) Quitar de las plantillas la palabra que duplica la unidad del marcador. (d) Sustituir por `:rango` más `:periodo/:fuentes/:fecha_dato/:capa`, o hacer que render.py omita «—» cuando el valor está vacío. (e) Unir las listas con «; » en cifras_clave.py o en render.py. Añadir a check_v5 una regla que rechace `(\b\w+ )\1`, `\['` y `— <unidad>` en output/v5. |
| B3 | **Bloqueante** | articulo_colegio:11 → plantilla `articulo_colegio.md:11` | Bajo un titular [C1], la frase «el déficit está concentrado, y un número pequeño de provincias suma la mitad» presenta como hecho una cifra C4 (`A4-conc50-2021-2025`, déficit provincial 2021-2025, C4 según decisiones B5). Incumple el criterio «ninguna C4 como hecho». Además, la cita sale como «6 provincias (6-6 provincias)». | Reformular de forma condicional, por ejemplo «En la contabilidad provincial 2021-2025 [C4], 6 provincias suman la mitad del déficit positivo», o moverla a «Lo probable pero no demostrado». Usar `:valor` en lugar de `:cita` cuando el rango es degenerado. |
| N1 | No bloqueante | articulo_colegio:71, informe_tecnico:38 y :500, a_necesidades:103, c_territorio:55 → plantillas `articulo_colegio.md:71`, `informe_tecnico.md:500` | Concordancia rota: «2 referencias coincidencias», «1 referencias diferencia», «difieren 1 referencias». | Usar `{{D3-…:num}}` sin la unidad «referencias» y escribir el sustantivo en la plantilla. |
| N2 | No bloqueante | working_paper:129 → plantilla `working_paper.md:129`; articulo_colegio:48 → plantilla `articulo_colegio.md:48` | «la sobrecarga de coste bajó -3,1 cambio desde 2015 (% población)» (doble negativo y unidad que rompe la frase); «26,8 % de personas de los inquilinos». | Usar `:num` con la unidad en la plantilla, por ejemplo «varió {{…:num}} puntos». |
| N3 | No bloqueante | linkedin/09:7 → plantilla `linkedin/09.md:7`; articulo_colegio:53; ponencia/diapositivas:90 | La traslación de la ayuda al precio se presenta de dos maneras: «entre 27,8 % y 81,8 %… hasta 100,0 %» (rango de la clase 1 y valor de la clase 2) frente a «entre 58,4 % y 100,0 %» (centrales). Además, en LinkedIn la cifra va sin periodo/rejilla, sin fuente y sin fecha. | Unificar el formato en los tres entregables (central y rango por clase) y usar `:cita` en LinkedIn. |
| N4 | No bloqueante | docs/v5/revision_humana.md:5 y :93 | Dicen que B4-v3-vut-cantidad está «fijado en el script… revisar». Desde la corrección registrada en decisiones, `src/v5/b4_run.py:310` lo lee de `output/v3/PB/cotas.json`. | Actualizar la nota y la entrada n.º 8. |
| N5 | No bloqueante | ponencia/diapositivas:81 y :88 → plantilla `ponencia/diapositivas.md` (títulos de las diapositivas 13-14) | «Qué podría funcionar» y «Qué no funcionaría por sí solo» son títulos valorativos sobre resultados C4. El cuerpo está en condicional. | Retitular, por ejemplo «Instrumentos con signo estable según el territorio [C2]» e «Instrumentos con signo no estable [C4]». |
| N6 | No bloqueante | informe_tecnico:487-489 (8.5) | «la provincia de València está entre las tres primeras en déficit contable 2021-2025» va sin capa (es C4). | Añadir [C4]. |
| N7 | No bloqueante | articulo_colegio.md | Unas 2.040 palabras en total, pero unas 1.740 sin las citas entre paréntesis. Cumple el mínimo solo si se cuentan las citas. | Valorar unas 300 palabras más de prosa, o aceptarlo y dejarlo anotado. |
| N8 | No bloqueante | articulo_colegio:9 | «En el mismo periodo» enlaza los hogares de 2021-2025 con las terminadas de 2019-2024. | Escribir los dos periodos. |
| N9 | No bloqueante | linkedin/06:1 | El titular «España en Europa… [C1]» enmarca una comparación europea que es C4. La cifra C1 es solo nacional. | Titular «La propiedad como forma de tenencia en España [C1]» y la comparación europea en el cuerpo con [C4]. |
| N10 | No bloqueante | Declaración de IA e independencia | Está completa en el apéndice C del WP y en el README. No aparece en el informe técnico, el policy brief ni el artículo del Colegio. | Añadir una nota breve al final del informe técnico y del artículo del Colegio. |
| N11 | No bloqueante | CITATION.cff, .zenodo.json; no hay fichero LICENSE | Declaran CC-BY-4.0 para un depósito de tipo software, pero no existe el fichero LICENSE. CC no se recomienda para código. | Añadir LICENSE y valorar una licencia doble: MIT (o similar) para el código y CC BY 4.0 para los textos. |
| N12 | No bloqueante | output/v5/verificador/verificador.md:34-35 | Faltan tildes: «ocupacion», «mayoria», «pequenos». | Corregir en el origen de las fichas CB. |
| N13 | No bloqueante | output/v5/correo_coev.md; docs/v5/calendario_publicacion.md | Fórmula «Estimados señores». El calendario fija la publicación según las campañas electorales: es neutral («cualquier campaña»), pero conviene justificarlo solo por la datación del contenido. | Usar «Estimados/as miembros de la comisión:». Mantener la redacción neutral del calendario. |

## Veredicto: **REHACER** (bloqueantes B1-B3)

Las correcciones son de plantilla, de metadatos de cifras_clave y de render/check, y no cambian ninguna estimación. Orden de prioridad:
1. B1: unidad y fuentes de `E-B1-F`.
2. B2: renderizado; añadir también la regla en check_v5.
3. B3: cifra C4 presentada como hecho en el artículo del Colegio.

Después hay que volver a ejecutar render, check_v5 y check_texto. Los no bloqueantes N1-N3 conviene corregirlos en la misma pasada porque tocan los mismos ficheros.
