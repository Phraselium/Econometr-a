# Pendientes de auditoría en V7.1 (S3)

Criterio del encargo:
- se resuelven los pendientes de severidad media que son de **redacción o coherencia**;
- el resto pasa al backlog con su coste (S = horas, M = días, L = semanas o datos nuevos).

Fuentes revisadas:
- historico/docs/v6_1/auditoria.md y docs/v6_1/backlog.md;
- docs/estado_proyecto/informe_estado.md (incidencias del inventario);
- historico/docs/v6_1/carta_respuesta.md (objeciones «no viable»).

## Resueltos en v7.1 (redacción o coherencia)

| id | Qué | Resolución |
|---|---|---|
| K4b-dh | dh_2125 mezcla el stock a 1 de enero (ECP) con la media anual (EPA) | Se declara en el campo de fuentes de la cifra (cifras_clave.py), así que aparece en cada cita. No cambia el número. |
| K4c-03 / K4c-26 | El mismo pendiente tiene dos nombres | Se unifica como K4c-26. La parte sustantiva (26 cifras del verificador fuera de cifras_clave) sigue en el backlog. |
| Inventario: v3 C3 H3-3b | El IC95 incluye el 0, pero el p ajustado es 0,0002 | No es una incoherencia. El IC95 [−9,9 %; +0,5 %] es la estimación CS de entrenamiento (p 0,073). El p ajustado de 0,0002 es el de la evaluación sellada (IC95 −6,4 % a −2,3 %). Son dos estimaciones distintas en el mismo JSON. Se aclara aquí; output/v3 es solo lectura. Sigue siendo C4, porque fallan los criterios de pretendencia. |
| Inventario: v2 BP, Holm-7 «pendiente» | El JSON de BP deja el Holm-7 como pendiente | Lo calcula BS: holm7_H5 = 1,0 (output/v2/BS/resultado.json). Conclusión sin cambio: no concluyente. |
| Inventario: v1 ECM, DM 0,290 frente a 0,509 | Dos p distintas para el mismo contraste | Resuelto en la adenda R0 de V7: son el modelo nominal y el real. Se cita en la sección única «Qué cambió». |
| K4a-04 | min/max con otro sentido | Resuelto en v6.3 con la columna sentido_min_max. Las cifras nuevas de V7 y V7.1 la rellenan. |
| K4a-03b / P-11 | Recalcular D2 con la necesidad T3 | Resuelto en v6.3, con su propagación en ERRATA. |
| A-09 | Publicar las ecuaciones del método de traslado | Resuelto en V7: output/v7/R6/metodo.md y anexo de ecuaciones del atlas. |
| P-10 | Costes y magnitudes por euro | Resuelto en parte en V7.1 (S1): coste estimado donde hay base y «coste no estimable», con su motivo, en el resto. |
| Duplicación de «Qué cambió» | Cinco entregables repetían el mismo bloque de v6.1 | Hay una sola sección (que_cambio.md); los entregables enlazan a ella. |

## Al backlog (con coste)

| id | Qué | Por qué no se hace en v7.1 | Coste |
|---|---|---|---|
| K4a-05 | Fianza media de la GVA: media bruta frente a truncada | Cambiaría paneles sellados de v6 y su hash | S |
| K4a-08 | El adaptador «188-506 mil» se extrae de un texto | Requiere leer un campo numérico de v4 M2: es código, no redacción | S |
| K4a-10 | Comprobaciones tautológicas en control_sumas | Requiere rediseñar comprobaciones | M |
| K4b-NR | 5 cifras no reconstruibles solo con el texto | Requiere ampliar el anexo metodológico con fórmulas | M |
| K4c-26 | 26 cifras del verificador fuera de cifras_clave | Requiere llevarlas a hechos.json del verificador y revisar los recuentos de v6.2 | S |
| K4d-ref y cuartiles de V7.1 | Referencias con «cuartil no verificado» | Scimago devuelve 403 desde la sesión; tarea del autor | S (autor) |
| A-04 | Recuento de especificaciones entre versiones | Cota inferior publicada en output/v7/cuenta_especificaciones.md; el recuento completo no es recuperable | — |
| A-13, P-12 | Muestra futura y fecha de publicación de las etiquetas | Dependen de la release y de make evaluate_v7 (tareas del autor) | autor |
| K2-49 | Reestimar la inmigración con 49 provincias | Exige mirar provincias selladas | L |
| BK-E3 | Ampliar los artículos | El autor amplía la prosa | M (autor) |
| BK-014, BK-017 | Temporada, habitaciones, MESVAL | Sin datos oficiales | L |
| H8 (v6.2) | Anexo: 8 trimestres de la EPA; clase A4 no reconstruible desde la ficha | Ampliación del anexo | S |
