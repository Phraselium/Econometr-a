# Revisión final de V7 (la hace el orquestador; V14)

Fecha: 2026-10-12. Los revisores de R2 y R4 superaron su tope de tokens. Por la regla de disciplina del encargo, esta revisión la hace el orquestador con la lista de comprobación del revisor: interpretación, propuestas y neutralidad. Se declara como desviación del control «revisor opus al final».

## Comprobaciones y hallazgos

| # | Ámbito | Hallazgo | Severidad | Corrección | Estado |
|---|---|---|---|---|---|
| F1 | Propuestas (R6) | Las «ayudas a la demanda» y la «rebaja de ITP/IVA» salían como robustas por reducir el esfuerzo neto del beneficiario, aunque **suben el precio de mercado** (+4,4 % y +1,1 % de mediana a 10 años). | alta | Criterio nuevo: robusto solo si además el precio de mercado no sube en ninguna extracción (V18). | corregido |
| F2 | Atlas, descomposición | La «variación observada» se calcula sobre datos con demeaning transversal, así que es **relativa a la media de las 17 CCAA**. Rotulada como subida, se leía mal: Cataluña, alquiler 2022T3-2026T2, aparecía con −1,2 % cuando subió unos +6,7 log-puntos. | alta | Rótulo «variación relativa a la media de las CCAA» en las fichas, el resumen y las tablas de región, con un aviso de que la subida absoluta está en la sección 1. | corregido |
| F3 | Atlas, nombres | El identificador `f2_impuestos_construccion` podía leerse como una subida de impuestos; el escenario es una **rebaja** de impuestos y costes. | media | Nombres legibles para los 7 instrumentos. | corregido |
| F4 | Atlas, texto | «no pasó diagnósticos en 0 de 17 CCAA» decía lo contrario de lo que quería decir. | baja | «no pasó los diagnósticos en ninguna de las 17 CCAA». | corregido |
| F5 | Atlas, extensión | Fichas de unas 3.200 palabras frente a las 2-4 páginas pedidas. | baja | La descomposición se resume (observado relativo y residuo), las propuestas van solo a 10 años y el detalle queda en region_<cod>.md e impactos.csv. Ahora tienen unas 2.100 palabras. | corregido |
| F6 | Verificador | Añadir las fichas de V7 al verificador de v5 cambiaba los recuentos publicados en v6.2 (40 → 43). | media | Verificador V7 aparte (output/v7/verificador_v7.md); v6.2 sin tocar. | corregido |
| F7 | Interpretación (R4) | Ninguna hipótesis se confirma; no hay largo plazo estable; φ sin inferencia válida; I(2) no descartado en 8 de 17; signos inestables según los retardos. | — | Se comunica tal cual en el resumen, las fichas y el historial («qué no se puede afirmar»). | correcto |
| F8 | Lenguaje causal | check_texto da 0 errores. Las descomposiciones, el SHAP y las importancias se rotulan como asociación o contabilidad; las propuestas van en condicional. | — | — | correcto |
| F9 | Neutralidad | No hay menciones a partidos ni personas en output/v7. Se evalúan instrumentos («se evalúan instrumentos, no actores»). | — | — | correcto |
| F10 | Contaminación | Todo lleva el rótulo «informativo, muestra ya vista en v1». La validación limpia es diferida, con los modelos congelados (sha256 en notas_release.md). | — | — | correcto |
| F11 | Elasticidades | La elasticidad de oferta regional no es utilizable en ninguna CCAA. Las propuestas descansan en la rejilla de v5 (C4) y se declara en cada ficha. | — | — | declarado |
| F12 | Referencias | El anexo de ecuaciones marca las referencias como NO VERIFICADA o «cuartil no verificado» (sin red). | baja | Tarea del autor (cuartiles). | pendiente del autor |

## Veredicto

**APROBAR con las correcciones F1-F6 aplicadas.** Los resultados centrales de V7 son negativos y se comunican como tales:
- no hay largo plazo identificado;
- no hay respuesta robusta a los tipos;
- la ventaja predictiva frente a la base más exigente se limita a 5-6 de 17 CCAA, con selección en muestra.

Las propuestas «robustas» son escenarios condicionales en C4, basados en la rejilla de elasticidades.
