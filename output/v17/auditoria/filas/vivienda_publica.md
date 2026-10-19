Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · vivienda_publica (medida 6, parte de vivienda pública)

## 1. Texto auditado
6. Vivienda pública e ITP: sin evidencia en España. (Esta ficha audita la vivienda pública; el ITP está en `itp_medida.md`.)

En lo publicado:
- Informe integral III.7: «sin evidencia en España; no evaluable con los datos disponibles».
- Signo estable no positivo [C2] en la rejilla de la 1.0.
- Escenario V7.1 de −3,2 puntos % de alquiler por cada 10.000 viviendas [C4].
- I.7: «Vivienda pública por habitante frente a la UE: sin dato».

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** No hay estudio español con diseño sobre el efecto de la vivienda pública o protegida en los precios de mercado (ficha L7). La evidencia internacional sobre el mercado es mixta:
- **Desplazamiento de la promoción privada.** Eriksen y Rosenthal (2010) hallan un desplazamiento cercano al 100 % para el LIHTC con instrumentos políticos. Sinai y Waldfogel (2005) hallan una adición neta de un tercio a la mitad por unidad. Baum-Snow y Marion (2009) solo lo hallan en barrios en gentrificación. Murray (1999) halla que la vivienda pública añade parque.
- **Precio del vecindario.** El signo cambia: +6,5 % en barrios de renta baja y −2,5 % en los de renta alta (Diamond y McQuade, 2019). Las mejoras de vivienda social en los Países Bajos suben los precios cercanos un 3,5 % (Koster y van Ommeren, 2019).
- **Viena.** Más vivienda de beneficio limitado se asocia con trayectorias de renta privada más bajas (Banabak, 2023). Es una asociación, no un diseño.
- **Francia (ley SRU).** Chapelle, Gobillon y Vignolles (CEPR DP 17535; IZA DP 17854; NO VERIFICADA, resumen vía buscador): la cuota obligatoria del 20 % aumentó la construcción de vivienda pública en los municipios tratados. Pero la mayoría de los nuevos ocupantes no son hogares pobres. No estudian el desplazamiento de la promoción privada ni los precios.

**En contra (la frase mezcla dos efectos y omite la escala).**
- **Efecto sobre los ocupantes.** Es el objetivo principal del instrumento, y no es «sin evidencia»: por construcción, el hogar paga una renta inferior a la de mercado. El parque social se define así: alquiler por debajo del precio de mercado, asignado por reglas (OCDE PH4.2). Lo que falta en España es medir cuánto, a quién llega y si está bien focalizado, no si existe el beneficio. La evidencia francesa sobre focalización matiza: los nuevos ocupantes no son mayoritariamente pobres.
- **La escala hace improbable un efecto de mercado nacional a medio plazo.**
  - España tiene un parque social del 1,13 % (OCDE PH4.2, 2019, 290.000 viviendas), frente al 7,99 % de la UE (2022 o último). El MIVAU da 318.000 viviendas públicas de alquiler, el 1,72 % de los hogares (Boletín Especial 2024).
  - Igualar la media de la UE con el parque actual exigiría unas 1,76 millones de viviendas sociales adicionales: 21 años de toda la producción actual (V17-AUD-OT-PUB-BRECHA-UE).
  - Al ritmo de calificaciones definitivas de vivienda protegida de 2021-2025 (11.265 al año, incluida la de venta; V17-AUD-OT-PUB-CALIF-MEDIA-2021-2025), añadir un solo punto de parque social llevaría unos 23 años. Serían 3 si toda la producción actual fuera social, y sin contar las descalificaciones (V17-AUD-OT-PUB-ANIOS-1PP).
- **El escenario de la 1.0 es optimista frente a la literatura.** −3,2 puntos % por cada 10.000 viviendas implica una elasticidad alquiler-parque de −3,4 en la CCAA mediana: unas 18 veces la de Mense (2025) para la oferta en general (V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71). Además, la 1.0 no comprueba si el escenario recoge el desplazamiento (lo dice III.7).
- **Validez externa de Viena, los Países Bajos y Francia.** Son parques sociales construidos durante décadas (Austria 23,6 %, Países Bajos 34,1 %, Francia 14,0 %; OCDE PH4.2), con financiación estable y sin descalificación. En España, la vivienda protegida pierde la protección tras 10-30 años (Funcas, NO VERIFICADA). No dicen qué pasaría con una ampliación pequeña y rápida en un mercado de propietarios.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Ocupantes frente a mercado.** Separados arriba. Para los ocupantes, la evidencia es definicional y descriptiva. Para el mercado, internacional y mixta.
- **Escala.** Brecha con la UE: 1,76 millones de viviendas. Un punto de parque social: unos 23 años al ritmo actual de calificaciones.
- **Evidencia internacional y validez externa.** Arriba, con referencias.
- Corrección para la 1.0 (I.7, «sin dato»): el dato de la OCDE ya está descargado (docs/v17/fuentes/parque_social.md). Es una omisión, no una falsedad, porque estaba pendiente en docs/v16/tareas_autor.md.

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
  - Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432, 10.53479/37872. Incluye el «reducido parque de alquiler social» entre los factores del tensionamiento del alquiler; descriptivo.
- **NO VERIFICADA:** Chapelle, Gobillon y Vignolles (CEPR DP 17535, 2022; IZA DP 17854, 2025), solo resumen vía buscador; Rodríguez-Fernández (2026, Funcas).
- **Datos:**
  - OCDE AHD PH4.2 (https://webfs.oecd.org/Els-com/Affordable_Housing_Database/PH4-2-Social-rental-housing-stock.xlsx, actualizada el 24-11-2025, consultada el 2026-10-19).
  - MIVAU, Boletín Especial Vivienda Social 2024.
- No se localizó un diseño creíble del desplazamiento fuera de EE. UU.

## 5. Veredicto
**Engañosa.** «Sin evidencia en España» es cierto solo para el efecto sobre los precios de mercado. Mezcla dos cosas:
- El beneficio para los ocupantes, que existe por definición, aunque su focalización está sin medir en España.
- El efecto de mercado: sin estudio español, con evidencia internacional mixta por el desplazamiento.

Y omite lo decisivo: con un parque del 1,1 % frente al 8 % de la UE, ninguna ampliación verosímil a diez años puede mover los precios nacionales de forma apreciable. Su papel es de protección de hogares concretos y de mercados locales.

## 6. Texto corregido y confianza
6a. Vivienda pública o social: baja el coste de la vivienda para quien la ocupa, que es su objetivo. Que baje los precios del mercado no está medido en España. Fuera, parte de la vivienda subvencionada sustituye a promoción privada, y el efecto en el barrio depende de su renta. España parte de un 1,1 % de parque social frente al 8 % de la UE: igualar la media europea exigiría unos 1,8 millones de viviendas, más de 20 años de toda la producción actual. A diez años, su efecto sobre el precio nacional sería pequeño; puede ser mayor en mercados locales.

Confianza:
- Beneficio para los ocupantes: «la evidencia indica».
- Efecto de mercado en España: «no permite concluir».
- Que a escala nacional sería pequeño a diez años: «la evidencia sugiere» (aritmética de escala, juicio experto).

## 7. PARADA
No hay: es engañosa por incompleta, no falsa. Para el autor: I.7 del informe integral dice «sin dato» de vivienda pública frente a la UE, y el dato ya está en data/raw/v17/parque_social. Es una actualización pendiente, no una parada.
