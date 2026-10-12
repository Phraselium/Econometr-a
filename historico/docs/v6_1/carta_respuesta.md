# Carta de respuesta a los revisores (revisión por pares simulada, v6.1, K5)

**Borja Romero, economista** (firma individual, independiente). 2026-10-11.

Agradezco a los dos revisores sus objeciones. Respondo una a una. «Aceptada — cambio aplicado» significa que el cambio está hecho en `docs/v5/plantillas/*.md` y renderizado en `output/v5/` (render, check_texto y check_v5 con 0 errores). Estos cambios son solo de texto, rótulos o avisos, sin nuevas estimaciones ni cifras tecleadas. «No viable en esta versión» significa que la objeción exige estimar o calcular de nuevo. Esas objeciones pasan a la sección «Limitaciones (revisión por pares simulada v6.1)» del working paper y a la §10.4 del informe técnico.

## Árbitro académico

| id | respuesta |
|---|---|
| A-01 | **Aceptada en parte — cambio aplicado:** la conclusión 1 del working paper indica ahora qué combinación da cada extremo. Dice también que la corrección de la EPA es un supuesto, que las terminadas son dos variantes del Ministerio y que el Catastro solo valida. **No viable en esta versión — pasa a limitaciones:** recalcular con las altas del Catastro o rebajar la capa en cifras_clave exige recalcular el módulo y regenerar las cifras. |
| A-02 | **Aceptada en parte — cambio aplicado:** §5.5 rotula la comparación con líneas base nuevas como segunda mirada no confirmatoria. **No viable — limitaciones:** una validación limpia necesita una muestra sellada nueva (el año siguiente), que todavía no existe. |
| A-03 | **Aceptada en parte — cambio aplicado:** §5.5 avisa de que los p del DM por provincia sobrestiman la precisión y de que, con el DM por periodo, la ventaja en el precio provincial anual no es significativa. **No viable — limitaciones:** dar como principal el DM por periodo o agrupado y el efecto mínimo detectable exige reejecutar las comparaciones. |
| A-04 | **No viable — limitaciones:** el recuento conjunto de especificaciones entre versiones exige reconstruir los registros de v1 a v6.1. Se declara que ningún p de una versión aislada es confirmatorio. |
| A-05 | **No viable — limitaciones:** generalizar el WCB y retirar los paneles municipales con regresor provincial exige reestimar. |
| A-06 | **No viable — limitaciones:** los intervalos de Anderson-Rubin y la inferencia shift-share exigen reestimar. Las cifras de 2SLS quedan como historial. |
| A-07 | **Aceptada — cambio aplicado:** en la Discusión del working paper, el traslado al precio pasa a ser un parámetro supuesto de la rejilla, no un efecto estimado. En el brief, la columna de signo se rotula como condicional a la rejilla y «se traslada» pasa a «se trasladaría según la rejilla». |
| A-08 | **Aceptada — cambio aplicado:** el aviso «Cómo citar estas cifras» (página única, brief y lo que sabemos) explica que [C4] incluye estadísticas oficiales de fuente única y no indica baja calidad. |
| A-09 | **No viable — limitaciones:** publicar las ecuaciones y parámetros del método de traslado y de la necesidad exige extraerlos del código y verificarlos (coste: una tarea de documentación con doble implementación). |
| A-10 | **Aceptada — cambio aplicado:** el aviso pide dar el rango antes que el valor central. El redondeo de los marcadores queda pendiente porque cambiaría el formato de cifras_clave. |
| A-11 | **Aceptada — cambio aplicado:** la conclusión 6 es ahora descriptiva («declaró la falta de potencia antes de ver los resultados…»). |
| A-12 | **Aceptada — cambio aplicado:** nuevo párrafo «Alcance de la aportación» en la Discusión: la aportación es de medición y de método, sin estimaciones identificadas, y la literatura de otros países solo fija los extremos de las rejillas. |
| A-13 | **No viable — limitaciones:** ya estaba declarada en §5.5. Resolverla requiere una muestra futura. |
| A-14 | **Ya resuelta fuera de K5:** K6 cerró K4a-07; se omiten 0 de 30 pliegues (docs/v6_1/estado.md). No requiere cambio. |
| A-15 | **Aceptada — cambio aplicado:** nota en inglés tras el abstract sobre la coma decimal y las unidades en español. |

## Revisor de política pública

| id | respuesta |
|---|---|
| P-01 | **Aceptada — cambio aplicado:** «Se construye poco» pasa a «Viviendas terminadas.» en la página única. |
| P-02 | **Aceptada — cambio aplicado:** recuadro «Cómo citar estas cifras» en la página única, el brief y lo que sabemos: rango antes que punto, las dos medidas de precio juntas y la rejilla citada con la conclusión. |
| P-03 | **Aceptada — cambio aplicado:** el mismo recuadro dice que solo la versión vigente es citable y remite al historial y a la fe de erratas para el motivo de cada cambio. |
| P-04 | **Aceptada — cambio aplicado:** véase A-07 (rótulo de la columna y condicional en la fila de ayudas). |
| P-05 | **Aceptada — cambio aplicado:** nuevo punto en «No se puede afirmar» (lo que sabemos) y en «Lo que este brief no afirma»: el signo de la asociación con la inmigración cambia con el control de población, la medida, el método y el nivel, y ninguna especificación aislada es la de referencia [C4]. |
| P-06 | **Aceptada — cambio aplicado:** el recuadro aclara que los rangos [C1] son el mínimo y el máximo entre combinaciones de fuentes, no intervalos de confianza. |
| P-07 | **Aceptada — cambio aplicado:** «rejilla de escenarios, definida por el autor» en la página única y en el brief. |
| P-08 | **Aceptada — cambio aplicado:** «no es un error de nadie» pasa a «no indica que ninguna de las dos fuentes esté mal medida». |
| P-09 | **Aceptada — cambio aplicado:** véase A-11. |
| P-10 | **No viable — limitaciones:** los costes y las magnitudes por euro requieren datos y estimaciones nuevos. |
| P-11 | **No viable — limitaciones:** recalcular D2 con T3 exige reejecutar el módulo. Se mantiene el rótulo de definición de K4a-03. |
| P-12 | **No viable — limitaciones:** la fecha depende de la publicación de las etiquetas en el repositorio remoto. |

## Recuento

- Objeciones: 27 (15 académicas y 12 de política).
- Con cambio de texto aplicado: 18, de las que 3 son aceptadas en parte (A-01, A-02, A-03).
- Pasadas a limitaciones: 11 (A-01, A-02, A-03 en su parte no viable; A-04, A-05, A-06, A-09, A-13; P-10, P-11, P-12).
- Ya resueltas antes de K5: 1 (A-14).
- Las limitaciones se agrupan en 9 puntos en el working paper y en el informe técnico §10.4.


## Adenda v6.2: respuesta completa a A-01

La parte que en v6.1 era «no viable» se ejecutó en v6.2 (tarea L3).

**A-01 (capa C1 del déficit 2021-2024).** Objeción: el extremo alto usa una corrección de la EPA fijada en el código (242.400 hogares), y las terminadas proceden de un solo organismo, de modo que no hay dos fuentes independientes en sentido fuerte.

Qué se hizo (v6.2, L3; src/v6_2/l3_deficit.py):
- Se recalculó el déficit con siete tratamientos alternativos del salto de la EPA en 2021T1, más la constante de v1: sin corrección; variación de ese trimestre igual a la media de los trimestres vecinos, con dos y con cuatro; igual a cero; enlace por cociente con la ECP; ECP retropolada; ECP publicada.
- Se cruzaron con tres fuentes de terminadas: Ministerio con y sin protegida, y Catastro completado con el Ministerio en País Vasco y Navarra.
- Se aplicaron bajas de 0 %, 0,1 % y 0,2 % anual, además de las estimadas en v5.1.
- Tras la revisión de v6.2, la ventana de la ECP va de 1-ene-2021 a 1-ene-2025.

Resultado:
- Sin bajas, el déficit 2021-2024 queda entre 389.361 y 710.542 viviendas. La amplitud es del 29,2 % del punto medio, frente a una tolerancia del 15 %, aunque la EPA corregida y la ECP coinciden dentro del 10,5 %, y el Catastro y el Ministerio dentro del 3,1 %.
- El mínimo lo fijan las variantes que conservan el quiebre de la EPA. Sin ellas, el rango sería 596.371-710.542, pero excluirlas es un supuesto sobre el salto.

Capa final: el déficit 2021-2024 sin bajas pasa de C1 a C2, una cota con supuestos explícitos sobre el tratamiento del salto y la fuente de terminadas.
- Con bajas estimadas: 389.361-765.994 (C4).
- Con bajas supuestas: hasta 924.658 (C2).
- La regla de capa se escribió en el mismo commit que los resultados, así que su anterioridad no consta en git.

Entregables y verificador actualizados: el déficit se cita como cota C2, con la sensibilidad al lado. La ficha V05 se sustituye por L3-V1.
