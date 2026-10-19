Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · vacias (medida 4)

## 1. Texto auditado
4. Movilizar vivienda vacía: prometedora para reducir la vacancia. No hay evidencia de que baje precios.

En lo publicado: informe integral III.6. Signo estable [C2] en la rejilla de la 1.0; escenario V7.1 de −1,7 puntos % de alquiler por cada 10.000 viviendas [C4].

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **Vacancia.** Segú (2020) estudia el impuesto francés de 1999 con diferencias en diferencias y emparejamiento. La vacancia baja un 13 % en términos relativos entre 1997 y 2001, sobre todo la de larga duración. La mayoría de esas viviendas pasa a residencia principal.
- **Precios.** No hay estudio con diseño sobre el precio:
  - Caracciolo y Miglino (Vancouver; NO VERIFICADA, resumen de buscador) no hallan efecto significativo sobre la renta media.
  - Han, Stacey y Chen (2023, NO VERIFICADA) advierten en un modelo calibrado de que el impuesto puede reducir la oferta en venta.
- **España.** No hay evaluación:
  - del recargo del IBI de la Ley 12/2023;
  - del impuesto catalán sobre viviendas vacías (Ley 14/2015, que grava a personas jurídicas). La búsqueda del 2026-10-19 solo dio un trabajo de fin de grado, que no cuenta como estudio con diseño.

**En contra (lo que falta).** La frase no separa parque vacío nominal de útil, ni dice dónde está.
- **Nominal.** 3.828.307 viviendas vacías por consumo eléctrico, un 14,4 % de las viviendas familiares [C4] (Censo 2021, tabla 59531). Es una aproximación: incluye viviendas en ruina, en obra, en herencia, en venta o entre inquilinos.
- **Localización** (cálculo propio en 2.574 municipios de la tabla, sin provincias selladas v6). La vacancia es mayor donde hay menos demanda:
  - 23,4 % en municipios de menos de 2.000 viviendas;
  - 18,5 % en los de 2.000-10.000;
  - 14,4 % en los de 10.000-50.000;
  - 12,6 % en los de más de 50.000 (V17-AUD-OT-VAC-TASA-T1 a T4).
  - Los municipios de menos de 10.000 viviendas reúnen el 40 % de las vacías de la muestra.
- **Donde está el déficit.**
  - En las 6 provincias con más déficit 2021-2025 (Barcelona, València, Alicante, Tarragona, Málaga, Almería; 272.346 viviendas de déficit) hay 909.028 vacías por consumo. Solo 162.010 están en sus capitales, con tasas del 6,3 % (Málaga) al 12,4 % (Tarragona) (V17-AUD-OT-VAC-6PROV-VACIAS y -6CAP-VACIAS).
  - Ilustración (juicio experto): con la reducción relativa de Segú, pasarían a uso unas 21.000 viviendas en esas capitales (el 8 % del déficit de las 6 provincias) y unas 118.000 en las provincias (43 %). Pero la mayor parte de estas estarían en municipios con poca demanda (V17-AUD-OT-VAC-SEGU-ILUSTRACION-6PROV). Supone que las vacías por consumo son vacancia gravable y que el efecto francés se traslada.
- **Escenario de la 1.0 frente a la literatura.**
  - El escenario de vacías de la 1.0 (−1,7 puntos % por 10.000 viviendas) implica una elasticidad alquiler-parque de −1,9: mayor que la de construir (−0,75) y unas 10 veces la de Mense (2025) (V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71).
  - La 1.0 lo presenta como robusto en 17 de 17 comunidades. Esa robustez es de la rejilla simulada, no de la literatura.
  - Que la frase auditada diga «no hay evidencia de que baje precios» corrige bien a esos escenarios.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Útil frente a nominal.**
  - La tabla 59531 no permite separar la vacancia friccional ni el estado de la vivienda. La única separación posible es por localización (tamaño del municipio) y por presión (provincias con déficit).
  - Las «viviendas con bajo consumo» y las de «uso esporádico» son categorías distintas y no se suman.
  - La muestra del Censo no identifica la vacía.
- **Recargos.** Segú (2020) es el único estudio con diseño y DOI verificado. Solo mide la vacancia.

## 4. Literatura
- **Segú (2020).** «The impact of taxing vacancy on housing markets: Evidence from France», *Journal of Public Economics* 185, 104079. DOI 10.1016/j.jpubeco.2019.104079, **VERIFICADA** (Crossref, 2026-10-19; cuartil no verificado). Resumen.
  - Validez externa: el impuesto francés se aplicó en ciudades grandes con mercado tensionado, a viviendas vacías durante más de 2 años. Se parece al recargo del IBI español en la forma, no en la base, porque en España la vacancia se concentra en municipios pequeños.
- **Caracciolo y Miglino (2024)** (C.D. Howe), **Han, Stacey y Chen (2023)** y **BCREA (2020)**: NO VERIFICADA. Resumen de buscador; la última es de una asociación del sector (ficha L7).
- No se localizó evaluación española con diseño.

## 5. Veredicto
**Se sostiene con matices.** Las dos afirmaciones son correctas. Falta decir dos cosas:
- La mayor parte del parque vacío nominal está donde no hay presión: un 23 % de vacancia en los municipios más pequeños frente a un 12-13 % en los grandes.
- La parte útil en los mercados tensionados es pequeña frente al déficit: del orden del 8 % del déficit de las 6 provincias más tensionadas si se aplicase el efecto francés a sus capitales.

## 6. Texto corregido y confianza
4. Movilizar vivienda vacía: un impuesto puede reducir la vacancia. En Francia, un 13 % en cuatro años. No hay evidencia de que baje el alquiler ni el precio. La mayor parte de la vivienda vacía está en municipios pequeños con poca demanda. En las capitales con más déficit, la parte que se movilizaría es pequeña frente a lo que falta.

Confianza:
- Vacancia: «la evidencia sugiere» (un estudio con diseño, otro país).
- Precio: «no permite concluir».
- Localización: «la evidencia indica» (dato del Censo).

## 7. PARADA
No hay.
