## Parte VI. Sobrevaloración: ¿está el precio por encima de sus fundamentales?

<!-- V17 (lectura convencional, indicadores del Banco de España con media histórica y máximo), v7.2 (GSADF) y V18 (F1 a F4). Sin lenguaje causal. -->

**Qué miden los indicadores convencionales** (Banco de España; último dato frente a su media histórica y a su máximo anual; capa C4, a posteriori de V17).

| Indicador | Último dato | Media histórica | Máximo anual |
|---|---|---|---|
| Precio de la vivienda sobre renta bruta por hogar (años) | {{V17-B5-PRECIO-RENTA:num}} | {{V17-B5-PRECIO-RENTA:min_num}} | {{V17-B5-PRECIO-RENTA:max_num}} |
| Esfuerzo teórico anual sin deducciones (% de la renta) | {{V17-B5-ESFUERZO-TEORICO:num}} | {{V17-B5-ESFUERZO-TEORICO:min_num}} | {{V17-B5-ESFUERZO-TEORICO:max_num}} |
| Rentabilidad bruta del alquiler (%) | {{V17-B5-RENTABILIDAD-ALQUILER:num}} | {{V17-B5-RENTABILIDAD-ALQUILER:min_num}} | {{V17-B5-RENTABILIDAD-ALQUILER:max_num}} |
| Crédito a hogares para vivienda (% del PIB) | {{V17-B5-CREDITO-PIB:num}} | {{V17-B5-CREDITO-PIB:min_num}} | {{V17-B5-CREDITO-PIB:max_num}} |
| Crédito para vivienda, tasa interanual (%) | {{V17-B5-CREDITO-TASA:num}} | {{V17-B5-CREDITO-TASA:min_num}} | {{V17-B5-CREDITO-TASA:max_num}} |
| Préstamos con relación préstamo-valor mayor que 80 % (% del total) | {{V17-B5-LTV80:num}} | {{V17-B5-LTV80:min_num}} | {{V17-B5-LTV80:max_num}} |
| Dudosidad del crédito para vivienda (%) | {{V17-B5-DUDOSIDAD:num}} | {{V17-B5-DUDOSIDAD:min_num}} | {{V17-B5-DUDOSIDAD:max_num}} |

**Lectura.** El nivel del precio frente a la renta está por encima de su media histórica y por debajo del máximo de 2007 ({{V17-AUD-DP-BUR-PRECIO-RENTA-FRENTE-2007:num}} % frente a 2007), y la rentabilidad del alquiler está por debajo de su media; el esfuerzo teórico, que incorpora los tipos, está algo por debajo de la suya. En cambio, el crédito no muestra un auge como el de 2005-2007: su saldo sobre el PIB está {{V17-AUD-DP-BUR-CREDITO-FRENTE-2007:num}} puntos por debajo del de 2007, su tasa de crecimiento y los préstamos con relación préstamo-valor alta están por debajo de su media, y la dudosidad es baja. Una parte grande de las compras no usa hipoteca (al menos un {{V17-B5-SIN-HIPOTECA-MIN:num}} % en 2025). El Banco de España presenta un rango de indicadores de desequilibrio del precio con métodos distintos y una incertidumbre alta entre ellos; el proyecto no replica esas medidas de nivel y no las sustituye.

**Qué añade el proyecto.**

- *Exuberancia estadística* (v7.2, contraste GSADF). Con ajuste por comparaciones múltiples, {{V72-GSADF-ratios-bh:num}} de cuatro cocientes nacionales son exuberantes (los denominadores son los del diseño de output/v7_2/gsadf/ficha_burbuja.md); los niveles de precio lo son en {{V72-GSADF-niveles-bh:num}} de dos series y las comunidades en {{V72-GSADF-ccaa-bh:num}} de 34. La potencia del contraste frente a una alternativa explosiva simulada es baja ({{V17-AUD-DP-BUR-GSADF-POTENCIA:num}} de rechazos), de modo que su ausencia no descarta una burbuja, igual que una exuberancia estadística no la demostraría.
- *Relación de largo plazo* (V7.2, V8-M4 y V18, familia F). Ningún contraste de cointegración entre precio, alquiler, renta, crédito y oferta rechaza su ausencia tras la corrección de Holm. Por la regla del proyecto no se publican elasticidades de largo plazo ni una sobrevaloración propia (F1-A3). F1 no predice mejor que el AR(4) fuera de muestra.

**Conclusión.** La afirmación «hay burbuja» y la afirmación «no hay burbuja» no se pueden sostener con estos datos (veredicto de V17 sobre las dos: engañosa). Los indicadores de nivel son altos frente a su media y los de crédito, contenidos; la evidencia indica que no hay un auge del crédito como el de 2005-2007 y no permite concluir sobre una sobrevaloración medida por el proyecto.
