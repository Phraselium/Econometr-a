Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · mas_oferta (medida 1)

## 1. Texto auditado
1. Más oferta donde hay presión: prometedora. Es coherente con el déficit medido y con la literatura internacional. Es la más respaldada, pero tarda años, porque el parque se ajusta despacio.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **Déficit.** Los hogares crecen más que las viviendas terminadas: 997.586 hogares (981.823-1.013.350) [C1], frente a 72.264-94.426 viviendas/año [C1]. Hay un déficit 2021-2024 de 549.952 viviendas (389.361-710.542) [C2], y uno 2021-2025 de 705.778 viviendas (523.606-887.950; L3-DEF-2125). El Banco de España da unas 750.000 en 2021-2025 (Informe Anual 2025).
- **Concentración.** El déficit está concentrado: 5 provincias suman la mitad y 14 el 80 % (V17-D3-DEFICIT-CONCENTRACION-50 y -80).
- **Literatura con diseño, más sólida que en la 1.0:**
  - Asquith, Mast y Reed (2023): un 6 % menos de alquiler cerca de grandes edificios nuevos en barrios de renta baja.
  - Pennington (2021): −1,2 a −2,3 % a menos de 500 m, con incendios como variación exógena.
  - **Mense (2025)**, ausente en la 1.0: con retrasos de obra por el clima como variación exógena, +1 % de oferta da −0,19 % del alquiler medio y baja también en las viviendas de peor calidad (Alemania).
  - Cadenas de mudanzas que llegan a hogares de renta baja: Mast (2023), y Bratu, Harjunen y Saarimaa (2023) en Helsinki (31 viviendas liberadas en el quintil inferior por cada 100 nuevas).
  - Restricciones de oferta y precios más altos: Saiz (2010) y Hilber y Vermeulen (2016).
- **Plazo.** «Tarda años» es cierto. El retardo medio entre el inicio y el fin de obra es de 3,2 años [C4], sin contar planeamiento ni licencia. La única cifra de plazos de licencia es de una asociación sectorial (unos 12 meses; nota de prensa de ASPRIMA-EY de 2020, estudio no localizado). No se usa como hecho.

**En contra (o matices que faltan).**
- **Escala.** Lo que dice la literatura por unidad es modesto. Cerrar el déficit central de la 1.0 supone un 2,65 % del parque de viviendas familiares (1,97-3,34 %; V17-AUD-OT-OFERTA-DEFICIT-SOBRE-PARQUE). Con la elasticidad de corto plazo de Mense, eso sería del orden de −0,4 a −0,6 % del alquiler medio (V17-AUD-OT-OFERTA-MENSE-ILUSTRACION). Es una ilustración nacional, estática y con validez externa no comprobada, no un efecto. Para comparar: la mediana provincial del alquiler SERPAVI subió un 33 % en 2015-2024 (output/v17/d3). «Más oferta» es necesaria para que el desajuste no crezca, pero por sí sola y a corto plazo no deshace la subida pasada.
- **Los escenarios de la 1.0 son más optimistas que la literatura.** La simulación V7.1 da −0,70 puntos % de alquiler por cada 10.000 viviendas en la comunidad mediana (V71-S1-a, [C4]). Eso equivale a una elasticidad de −0,75 % de alquiler por 1 % de parque, unas 3,9 veces la de corto plazo de Mense (V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71). La de vivienda pública es −3,4 y la de vacías −1,9: mayores que la de construcción sin respaldo en la literatura.
- **«Donde hay presión» es justo donde construir es más difícil.**
  - Para el área de Barcelona, el Banco de España estima unas 120.000 viviendas potenciales no ejecutadas. Eso es el 0,39 de la necesidad provincial a 10 años (308.670, central; output/v17/d3/suelo_potencial_bde_vs_necesidad.csv). El área y la provincia no son el mismo ámbito.
  - En el área de Sevilla el potencial (163.000) supera la necesidad provincial (2,63).
- **Capacidad.**
  - La producción necesaria para cerrar el déficit central en 5 años es de 293.623 viviendas/año: 3,5 veces la actual (83.700) y el 52 % de la del boom (568.684) (V17-D3-PROD-*).
  - Con la relación ocupados/terminadas de 2007, esa producción pediría unos 1,40 millones de ocupados, frente a 1,50 millones hoy (V17-AUD-OT-OFERTA-EMPLEO-PROPORCIONAL-BOOM). El «empleo implícito a productividad 2025» de output/v17/d3 (5,4 millones) exagera, porque la rama F incluye obra civil y rehabilitación. El número de ocupados no parece el límite. Lo serían la composición del empleo, el suelo finalista y los plazos, que no están medidos.
- **No hay elasticidad española identificada.**
  - Q4 de V16 queda sin hallazgo, y su inferencia convencional no es fiable (tamaño real del 20,3 %; inferencia.csv).
  - Taltavull de la Paz (2014) da una elasticidad de 0,8-1,3 por CCAA, sin diseño causal.

## 3. Pruebas mínimas
- Literatura de obra nueva y filtrado: arriba y en el apartado 4.
- Plazos: 3,2 años de obra [C4]; licencias sin dato oficial (docs/v17/fuentes/oferta_capacidad.md).
- Restricciones de suelo y capacidad: suelo y empleo arriba (output/v17/d3; src/v17/f3_oferta_titularidad.py).
- **Dónde sí y dónde no.**
  - Sí parece factible donde el planeamiento ya tiene potencial no ejecutado comparable a la necesidad: área de Madrid (550.000; la provincia está en la muestra sellada v6 y no se compara) y área de Sevilla.
  - No con el suelo previsto en la ciudad central de Barcelona y su área, ni en las capitales en general: 320.000 viviendas potenciales en las seis capitales, el 4,5 % del total (BdE, nota 41).
  - Ahí la oferta tendría que venir de la densificación (0,5 millones adicionales, hasta 1-1,2 millones de máximo teórico, según el BdE) o de las coronas, con transporte (sin datos).

## 4. Literatura
- **Mense (2025).** «The Impact of New Housing Supply on the Distribution of Rents», *Journal of Political Economy Macroeconomics*. DOI 10.1086/733977, **VERIFICADA** (Crossref, 2026-10-19; cuartil no verificado). Solo resumen (repositorio de la LSE, vía buscador).
- **Asquith, Mast y Reed (2023).** 10.1162/rest_a_01055, VERIFICADA (comprobada de nuevo en Crossref). Resumen.
- **Bratu, Harjunen y Saarimaa (2023).** 10.1016/j.jue.2022.103528, VERIFICADA (comprobada de nuevo). Texto parcial, págs. 1-3 (ficha L3).
- **Mast (2023).** 10.1016/j.jue.2021.103383, VERIFICADA. Texto parcial, págs. 1-2.
- **Pennington (2021).** Documento de trabajo, NO VERIFICADA. Texto parcial, págs. 1-4.
- **Li (2022).** *J. Econ. Geography*, NO VERIFICADA. Resumen.
- **Saiz (2010)** 10.1162/qjec.2010.125.3.1253 y **Hilber y Vermeulen (2016)** 10.1111/ecoj.12213: VERIFICADA, resumen.
- **Taltavull de la Paz (2014).** 10.1108/JERER-10-2013-0023, VERIFICADA, resumen.
- **Banco de España, Informe Anual 2025**, cap. 2, págs. 157-158 y notas 40-46 (pasaje leído completo; https://www.bde.es/f/webbe/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/25/InfAnual_2025.pdf; consultado el 2026-10-19).

Validez externa:
- Los estudios de filtrado y de alquiler cercano son de EE. UU., Finlandia y Alemania, con más alquiler y más movilidad que España.
- En España el ajuste por cadenas de mudanzas pasa sobre todo por la compra. No se ha medido.

## 5. Veredicto
**Se sostiene con matices.** Es la medida mejor respaldada, y la literatura es hoy más sólida de lo que dice la 1.0 (Mense, 2025). Faltan tres matices:
- El efecto por vivienda es pequeño. Cerrar el déficit nacional equivaldría, con la elasticidad de corto plazo de Mense, a menos de un punto de alquiler, y los escenarios de la 1.0 son unas 4 veces más optimistas.
- La factibilidad es desigual: donde hay más presión hay menos suelo previsto.
- El plazo no es solo de obra; también es de planeamiento.

## 6. Texto corregido y confianza
1. Más oferta donde hay presión: es la medida mejor respaldada. Con diseños creíbles fuera de España, la obra nueva baja el alquiler cercano y libera viviendas para hogares de menor renta. El efecto por vivienda es pequeño, así que hacen falta volúmenes sostenidos: unas 3,5 veces la producción actual para cerrar el déficit en cinco años. Y donde la presión es mayor, como Barcelona o los centros urbanos, el suelo previsto no basta. Tarda años: más de tres de obra, más el planeamiento y la licencia.

Confianza:
- Signo: «la evidencia indica».
- Magnitud en España: «la evidencia sugiere que es pequeña por unidad».
- Factibilidad local: «es compatible con».

## 7. PARADA
No hay.
