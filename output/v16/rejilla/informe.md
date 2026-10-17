# Rejilla fija multiescala (83 celdas) · C4, pendiente de evaluación sellada

**Capa.** C4. TWFE de municipio y provincia NO APTO (tamaño 0,203 y 0,1105): **estimación puntual, sin p-valor ni IC**; las 83 celdas pasan al control BY del orquestador con p null. Asociación, sin lenguaje causal.

<a id="resumen"></a>## Resumen

- Celdas estimadas: 83 de 83; no estimables: 0 (sin variación de la exposición en la ventana o < 10 unidades).
- Variantes de robustez declaradas: 415; estimadas: 355. Mediana de la proporción de variantes con el mismo signo que la principal: 1,00.

| Familia | Celdas | Estimadas | β > 0 | β < 0 | Mediana mismo signo en variantes |
|---|---|---|---|---|---|
| Q1 | 18 | 18 | 9 | 9 | 1,00 |
| Q2 | 24 | 24 | 12 | 12 | 1,00 |
| Q3 | 21 | 21 | 11 | 10 | 0,80 |
| Q4 | 7 | 7 | 3 | 4 | 1,00 |
| Q6 | 13 | 13 | 7 | 6 | 1,00 |

## Especificación y límites
log del resultado anual ~ exposición + EF de unidad y periodo (pre-registrada; adenda, punto 4). Exposiciones: Q1 fracción del año con zona vigente; Q2 log del % de vivienda turística INE estandarizado; Q3 shift-share del padrón de 2003; Q4 Red Natura × Q3; Q6 tipo general del ITP de su CCAA. Q3 y Q4 llegan a 2022. Las celdas por unidad (β por unidad de exposición y por DT, n, variantes y exclusión de grandes ciudades) están en rejilla_resultados.csv.
No se elige ninguna celda por su resultado; el listado completo, con las no estimables, es el de rejilla_fija.csv. Diagnósticos de diseño (pretendencias, placebos, Honest DiD, Oster): en los informes de Q1-Q6, no por celda.
