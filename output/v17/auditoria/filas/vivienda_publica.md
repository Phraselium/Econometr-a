Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada. Revisada tras la ronda 1 del abogado del diablo.

# Fila D1 · vivienda_publica (medida 6, parte de vivienda pública)

## 1. Texto auditado
6. Vivienda pública e ITP: sin evidencia en España. (Esta ficha audita la vivienda pública; el ITP está en `itp_medida.md`.)

En lo publicado:
- Informe integral III.7: «sin evidencia en España; no evaluable con los datos disponibles».
- Signo estable no positivo [C2] en la rejilla de la 1.0.
- Escenario V7.1 de −3,2 puntos % de alquiler por 10.000 viviendas [C4].
- I.7: «Vivienda pública por habitante frente a la UE: sin dato».

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** No hay estudio español con diseño sobre el efecto de la vivienda pública o protegida en los precios de mercado (ficha L7). La evidencia internacional sobre el mercado es mixta:
- **Desplazamiento de la promoción privada.** Cercano al 100 % en Eriksen y Rosenthal (2010). Adición neta de un tercio a la mitad por unidad en Sinai y Waldfogel (2005). Solo en barrios en gentrificación en Baum-Snow y Marion (2009). Murray (1999) halla que la vivienda pública añade parque.
- **Precio del vecindario.** El signo depende de la renta del barrio: +6,5 % en los de renta baja y −2,5 % en los de renta alta (Diamond y McQuade, 2019). +3,5 % cerca de mejoras de vivienda social en los Países Bajos (Koster y van Ommeren, 2019).
- **Viena.** Asociación con trayectorias de renta privada más bajas (Banabak, 2023). No es un diseño.
- **Francia (ley SRU).** Más construcción pública en los municipios obligados, pero ocupada sobre todo por hogares que no son pobres (Chapelle, Gobillon y Vignolles, CEPR DP 17535 / IZA DP 17854; NO VERIFICADA, resumen vía buscador). No estudian el desplazamiento ni los precios.

**En contra, o matices que faltan.**
- **Efecto sobre los ocupantes.** No es una cuestión de evidencia: **es definicional**. El parque social se define por una renta inferior a la de mercado asignada por reglas (OCDE PH4.2). Lo que no está medido en España es la focalización (a quién llega) y el valor del beneficio. La evidencia francesa advierte de que la focalización puede fallar.
- **Escala.**
  - España tiene un 1,13 % de parque social (OCDE PH4.2, 2019, 290.000 viviendas, sobre el parque). El MIVAU da 318.000 viviendas públicas de alquiler (Boletín Especial 2024): un 1,72 % de los hogares, o un 1,24 % del mismo parque que usa la OCDE. Es esta última la que se compara con el 7,99 %, que también es sobre parque.
  - **El 7,99 % de la UE es una media simple de los 19 países UE con dato**, con años de referencia distintos. La media simple que calculo coincide con el agregado de la OCDE (V17-AUD-OT-PUB-UE-MEDIA-SIMPLE). No está ponderada por parque.
  - Igualarla con el parque actual exigiría entre 1,73 millones (desde el 1,24 %) y 1,76 millones (desde el 1,13 %) de viviendas sociales adicionales: unos 21 años de toda la producción actual (V17-AUD-OT-PUB-BRECHA-UE).
  - Al ritmo de calificaciones definitivas de vivienda protegida de 2021-2025 (11.265 al año, incluida la de venta), añadir un punto de parque social llevaría unos 23 años. Serían 3 si toda la producción actual fuera social. Sin contar las descalificaciones (V17-AUD-OT-PUB-ANIOS-1PP).
- **Parque protegido en propiedad.** La vivienda protegida española ha sido sobre todo de venta, con protección temporal de 10 a 30 años, tras la cual pasa al mercado libre (Funcas, NO VERIFICADA). Ese parque en propiedad no entra en el 1,13 % ni en el 1,24 %, y no se cuantifica aquí. Abarata el acceso a la propiedad de sus compradores, lo que tampoco se ha evaluado en España.
- **El escenario de la 1.0.** Implica una elasticidad alquiler-parque de −5,6 en la CCAA mediana de las 9 no selladas (−3,4 con las 17) (V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71). No se comprueba si recoge el desplazamiento: lo dice la propia 1.0 (III.7).
- **Validez externa** de Viena, los Países Bajos y Francia: son parques construidos durante décadas, con financiación estable y sin descalificación.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Ocupantes frente a mercado.** Separados arriba. Para los ocupantes, el beneficio es definicional y su focalización no está medida. Para el mercado, no hay evidencia española y la internacional es mixta.
- **Escala.** Brecha con la UE de 1,73-1,76 millones de viviendas; unos 23 años por punto de parque social al ritmo actual.
- **Evidencia internacional y validez externa.** Arriba.
- Para el autor: I.7 del informe integral («sin dato» frente a la UE) está desactualizado. El dato de la OCDE ya está en data/raw/v17/parque_social.

## 4. Literatura (ficha L7 salvo indicación)
Todas leídas en resumen; cuartil no verificado.
- **VERIFICADA:**
  - Sinai y Waldfogel (2005), 10.1016/j.jpubeco.2004.06.015.
  - Eriksen y Rosenthal (2010), 10.1016/j.jpubeco.2010.07.002.
  - Baum-Snow y Marion (2009), 10.1016/j.jpubeco.2009.01.001.
  - Murray (1999), 10.1023/A:1007741630145.
  - Diamond y McQuade (2019), 10.1086/701354.
  - Koster y van Ommeren (2019), 10.1162/rest_a_00779.
  - Banabak (2023), 10.1080/12265934.2022.2110144.
  - BdE DO 2432, 10.53479/37872.
- **NO VERIFICADA:** Chapelle, Gobillon y Vignolles; Rodríguez-Fernández (2026, Funcas).
- **Datos:**
  - OCDE AHD PH4.2 (https://webfs.oecd.org/Els-com/Affordable_Housing_Database/PH4-2-Social-rental-housing-stock.xlsx, actualizada el 24-11-2025, consultada el 2026-10-19).
  - MIVAU, Boletín Especial Vivienda Social 2024.

## 5. Veredicto
**Se sostiene con matices.** «Sin evidencia en España» es cierto para lo que puede faltar, que es el efecto sobre los precios de mercado y la focalización. El beneficio para el ocupante no es una cuestión de evidencia, sino de definición. Hay que decirlo para que el lector no entienda que la vivienda pública «no funciona».

Criterio común con `ayudas_demanda.md`: allí la frase es incorrecta porque la asequibilidad del beneficiario sí tiene estudios con diseño y la frase lo niega. Aquí el beneficio del ocupante no depende de la traslación (es renta regulada), y la frase no lo niega: solo lo omite. Por eso «con matices» y no «incorrecta».

Matiz decisivo: con un parque social de alquiler del 1,1-1,2 % del parque, frente a una media simple europea del 8 %, la escala es compatible con un efecto pequeño sobre los precios nacionales a diez años.

## 6. Texto corregido y confianza
6a. Vivienda pública o social: baja el coste de la vivienda para quien la ocupa; es su definición. A quién llega no está medido en España. Que baje los precios del mercado tampoco. Fuera, parte de la vivienda subvencionada sustituye a promoción privada, y el efecto en el barrio depende de su renta. España parte de un 1,1-1,2 % de parque social de alquiler sobre el parque, frente a una media simple del 8 % en la UE. Igualarla exigiría unos 1,7-1,8 millones de viviendas, unos 21 años de toda la producción actual. Eso es compatible con un efecto pequeño sobre el precio nacional a diez años, que puede ser mayor en mercados locales. Buena parte de la vivienda protegida española fue de venta y pierde la protección con el tiempo.

Confianza:
- Beneficio del ocupante: definicional; su focalización «no permite concluir».
- Efecto de mercado en España: «no permite concluir».
- Efecto nacional pequeño a diez años: «la evidencia es compatible con» (aritmética de escala, juicio experto).

## 7. PARADA
No hay.

## Respuesta a la ronda 1
- **Veredicto hacia «se sostiene con matices». Aceptado,** con el criterio común con ayudas_demanda explicado en el apartado 5.
- **El beneficio del ocupante es definicional. Aplicado:** retirado «la evidencia indica».
- **Brecha con el 1,13 % y con el 1,72 %. Aplicado:** 1,61-1,76 millones. El 7,99 % es una media simple: la calculo con el fichero de la OCDE y coincide.
- **«Ninguna ampliación verosímil» → «es compatible con». Aplicado.**
- **Parque protegido en propiedad. Añadido,** sin cuantificar: no hay dato en el repositorio.

## Respuesta a la ronda 2
- **Brecha con 318.000 sobre el parque (1,24 %), no con el 1,72 % sobre hogares. Aplicado:** 1,73-1,76 millones (V17-AUD-OT-PUB-BRECHA-UE, mínimo cambiado). El texto corregido dice 1,7-1,8 millones y un 1,1-1,2 % de partida.
- **«Explica en parte por qué…». Retirado:** no está demostrado.
- **Guarda v6.** La elasticidad implícita del escenario se calcula ahora sobre la CCAA mediana de las 9 CCAA no selladas: −5,6 en vivienda pública.
