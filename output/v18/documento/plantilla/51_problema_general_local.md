### 5.2 ¿Problema general o local? (V17)

Análisis a posteriori de V17, capa C4, contable y descriptivo. La pregunta es qué parte de la varianza de la variación anual de los precios y los alquileres corresponde a un componente común a todos los territorios (el efecto año) y qué parte es local (provincia por año). Las cuotas llevan intervalo de confianza al 95 % por bootstrap de provincias y se comparan con una referencia de azar (permutación temporal dentro de cada provincia).

| Serie | Periodo | Cuota del componente común (%) | IC95 (%) |
|---|---|---|---|
| Índice de precios de vivienda (IPV) por comunidad, comunidades no selladas | 2015-2025 | {{V17-D3-VARIANZA-COMUN-IPV-CCAA:num}} | {{V17-D3-VARIANZA-COMUN-IPV-CCAA:min_num}} a {{V17-D3-VARIANZA-COMUN-IPV-CCAA:max_num}} |
| Valor tasado del MIVAU por provincia | 2015-2025 | {{V17-D3-VARIANZA-COMUN-VALOR-TASADO:num}} | {{V17-D3-VARIANZA-COMUN-VALOR-TASADO:min_num}} a {{V17-D3-VARIANZA-COMUN-VALOR-TASADO:max_num}} |
| Índice de precios de vivienda del INE por provincia (IPVA) | 2015-2024 | {{V17-D3-VARIANZA-COMUN-IPVA:num}} | {{V17-D3-VARIANZA-COMUN-IPVA:min_num}} a {{V17-D3-VARIANZA-COMUN-IPVA:max_num}} |
| IPC de alquiler del INE por provincia | 2015-2025 | {{V17-D3-VARIANZA-COMUN-IPC-ALQUILER:num}} | {{V17-D3-VARIANZA-COMUN-IPC-ALQUILER:min_num}} a {{V17-D3-VARIANZA-COMUN-IPC-ALQUILER:max_num}} |
| Alquiler mediano en €/m² de SERPAVI por provincia | 2015-2024 | {{V17-D3-VARIANZA-COMUN-SERPAVI:num}} | {{V17-D3-VARIANZA-COMUN-SERPAVI:min_num}} a {{V17-D3-VARIANZA-COMUN-SERPAVI:max_num}} |

**Lectura.**

- En compra, el componente común es mayoritario en el conjunto de 2015-2025 en las tres series. Por subperiodos, en el valor tasado y en el IPV por comunidad el componente local pesa más antes de 2020 y el común domina desde 2020; no ocurre así con el IPVA [FALTA CIFRA: cuotas del componente común por subperiodo, 2015-2019 y 2020-2025 (output/v17/d3/varianza_comun_local.csv)].
- En alquiler, el resultado es mixto y menos seguro: las cuotas del componente común son menores y los intervalos más anchos, y en SERPAVI el componente común baja desde 2020.
- En todas las series queda una parte local (provincia por año), de modo que la respuesta no es una u otra. Depende de la serie y del método.
- El déficit está concentrado: {{V17-D3-DEFICIT-CONCENTRACION-50:num}} provincias suman la mitad del déficit positivo de 2021-2025 y {{V17-D3-DEFICIT-CONCENTRACION-80:num}} suman el 80 % ({{V17-D3-DEFICIT-CONCENTRACION-50:cobertura}}).
- Movimientos dentro de la provincia: el saldo acumulado de 2015 a 2024 de las capitales con el resto de su provincia es de {{V17-D3-CORONAS-SALDO-CAPITAL:num}} personas ({{V17-D3-CORONAS-SALDO-CAPITAL:cobertura}}); negativo significa que la capital cede residentes a su corona. Solo cubre movimientos entre municipios de una misma provincia y no mide el padrón de la corona.

**Relación con V18.** Los diseños de panel con efectos de periodo (E1, E2, E3, E5, E8, E9, E12) solo recogen la parte local, la que varía entre territorios en el mismo periodo. Por eso las contribuciones por factor de la contabilidad se rotulan «relativas entre provincias, sin el componente común», y la variación común queda fuera de lo que esos diseños pueden asociar a un factor. Es una de las razones de que la fila «no explicado» sea grande.

**Límites.** No hay esfuerzo provincial propio en los datos locales. La cuota depende de la serie, del número de periodos y de los territorios no sellados. Nada de esta sección es una estimación de un efecto.
