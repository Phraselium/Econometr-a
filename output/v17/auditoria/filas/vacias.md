Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada. Revisada tras la ronda 1 del abogado del diablo.

# Fila D1 · vacias (medida 4)

## 1. Texto auditado
4. Movilizar vivienda vacía: prometedora para reducir la vacancia. No hay evidencia de que baje precios.

En lo publicado: informe integral III.6. Signo estable [C2] en la rejilla de la 1.0; escenario V7.1 de −1,7 puntos % de alquiler por cada 10.000 viviendas [C4].

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **Vacancia.** Segú (2020) estudia el impuesto francés de 1999 con diferencias en diferencias y emparejamiento. La vacancia baja un 13 % en términos relativos entre 1997 y 2001, sobre todo la de larga duración, y la mayoría de esas viviendas pasa a residencia principal.
- **Precios.** No hay estudio con diseño sobre el precio. Caracciolo y Miglino (Vancouver; NO VERIFICADA) no hallan efecto significativo sobre la renta media.
- **España.** No hay evaluación del recargo del IBI (Ley 12/2023) ni del impuesto catalán (Ley 14/2015).

**En contra (lo que falta).** Hay que distinguir cuatro magnitudes.

**(a) Parque vacío nominal.** 3.828.307 viviendas vacías por consumo eléctrico, un 14,4 % de las viviendas familiares [C4] (Censo 2021, tabla 59531). En las provincias sin muestra sellada v6 son 2.932.346 (V17-AUD-OT-VAC-COBERTURA). La tabla lista los municipios grandes y agrupa los pequeños en filas «Resto de provincia». Esa agrupación tiene una vacancia del 32,6 % y reúne el 15,1 % de las vacías.

**(b) Dónde está.** Sobre el total provincial, incluido el «resto»:
- En las provincias analizadas (sin las selladas v6), más de la mitad de las vacías (54,8 %) está en municipios de menos de 10.000 viviendas (no habitantes) o en los no listados por la tabla. Solo el 20,1 % está en municipios de más de 50.000 viviendas (V17-AUD-OT-VAC-CUOTA-MUN-PEQUENOS).
- Tasas por tamaño, en municipios listados: 23,4 %, 18,4 %, 12,7 % y 10,0 % (V17-AUD-OT-VAC-TASA-T1 a T4).

**(c) Vacancia frente a presión, en el mismo ámbito (provincia).** La presión se mide como déficit 2021-2025 por vivienda (V17-D3), en 41 provincias sin muestra sellada:
- Correlación de rangos entre vacancia y presión: −0,36 (V17-AUD-OT-VAC-PRESION-SPEARMAN). Hay menos vacancia donde hay más déficit.
- Tercil de más presión: vacancia del 13,5 %, frente al 22,3 % del de menos presión. Ese tercil reúne el 45 % de las vacías y el 73 % del déficit (V17-AUD-OT-VAC-TASA-TERCIL-PRESION-ALTA).
- Aun así, las vacías nominales superan al déficit en todos los terciles: 3,7 veces en el de más presión y 24,8 veces en el de menos.
- En las 6 provincias con más déficit hay 909.028 vacías y 272.346 de déficit, 3,3 veces más. En sus capitales (ninguna de provincias selladas; el script comprueba que son las de esas 6 provincias) hay 162.010, con tasas del 6,3 al 12,4 %.

**(d) Parque útil frente a lo movilizable.**
- **Parque útil: no se puede saber.** El consumo eléctrico no separa la vacancia friccional (entre inquilinos, en venta), la de obra o ruina, las herencias y la vivienda sin demanda. No hay fuente que lo mida.
- **Lo movilizable con un impuesto como el francés es un escenario, no el parque útil.** Con la reducción relativa del 13 % de Segú, pasarían a uso unas 21.000 viviendas en las capitales de las 6 provincias (el 8 % de su déficit) y unas 118.000 en las provincias enteras (el 43 %). La mayor parte estaría fuera de las capitales (V17-AUD-OT-VAC-SEGU-ILUSTRACION-6PROV). Supone que la vacancia por consumo es gravable y que el efecto francés se traslada.

**Absorción.**
- El déficit contable (hogares nuevos menos viviendas nuevas, bajas 0) no descuenta que parte de los hogares nuevos de 2021-2025 ocupó viviendas vacías o secundarias ya existentes. En ese sentido, el déficit es una cota superior.
- El parque vacío de 2021 probablemente es menor hoy. No hay censo posterior para medirlo.
- Las dos cosas van en la misma dirección: lo que la vivienda vacía ya ha absorbido no se puede volver a contar como reserva.

**Escenario de la 1.0.** La simulación de vacías de la 1.0 (−1,7 puntos % por 10.000 viviendas) implica, en la CCAA mediana de las 9 no selladas, una elasticidad alquiler-parque de −3,1, mayor que la de construir (−1,2) (V17-AUD-OT-OFERTA-ELASTICIDAD-IMPLICITA-V71). No hay referencia de la literatura que respalde que una vivienda movilizada pese más que una construida. Que la frase diga «no hay evidencia de que baje precios» corrige bien a ese escenario.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Útil frente a nominal.** El útil no se puede medir. El nominal se localiza y se cruza con la presión: arriba.
- **Recargos.** Segú (2020) es el único estudio con diseño y DOI verificado. Solo mide la vacancia.
- **Corrección propia.** La primera versión de esta ficha trataba las filas «Resto de provincia» como municipios y daba un 40 % de vacías en municipios de menos de 10.000 viviendas. Con el total provincial y el resto separado, es el 54,8 %. Las tasas por tamaño también cambian (12,6 % → 10,0 % en los de más de 50.000 viviendas).

## 4. Literatura
- **Segú (2020).** *Journal of Public Economics* 185, 104079. DOI 10.1016/j.jpubeco.2019.104079, **VERIFICADA** (Crossref, 2026-10-19; cuartil no verificado). Resumen.
  - Validez externa: el impuesto francés se aplicó en grandes ciudades tensionadas, a viviendas vacías durante más de 2 años. En España, la vacancia se concentra fuera de esos mercados.
- **Caracciolo y Miglino (2024), Han, Stacey y Chen (2023) y BCREA (2020):** NO VERIFICADA (ficha L7).
- No hay evaluación española con diseño.

## 5. Veredicto
**Se sostiene con matices.** Las dos afirmaciones son correctas. Falta decir:
- En las provincias analizadas, más de la mitad de la vivienda vacía nominal está en municipios de menos de 10.000 viviendas, y la vacancia es menor donde hay más presión.
- Las vacías nominales superan al déficit incluso en las provincias más tensionadas, pero no se sabe qué parte es útil.
- Un impuesto como el francés movilizaría, en escenario, una fracción pequeña frente al déficit en las capitales.

## 6. Texto corregido y confianza
4. Movilizar vivienda vacía: un impuesto puede reducir la vacancia; en Francia, un 13 % en cuatro años. No hay evidencia de que baje el alquiler ni el precio. Hay 3,8 millones de viviendas sin apenas consumo eléctrico. En las provincias analizadas, más de la mitad están en municipios de menos de 10.000 viviendas, y donde falta más vivienda hay menos vacancia. Cuántas son utilizables no se sabe. En las capitales con más déficit, lo que movilizaría un impuesto como el francés sería poco frente a lo que falta.

Confianza:
- Vacancia: «la evidencia sugiere» (un estudio, otro país).
- Precio: «no permite concluir».
- Localización y relación con la presión: «la evidencia indica» (Censo).
- Parque útil: «no se puede saber».

## 7. PARADA
No hay.

## Respuesta a la ronda 1
- **El texto corregido contradecía los datos (40 % frente a 60 %). Comprobado con el total y corregido el cálculo.** El error era mío: las filas «Resto de provincia» entraban como municipios grandes. Con el total provincial no sellado (2.932.346; total nacional 3.828.307), el 54,8 % está en municipios de menos de 10.000 viviendas o no listados. «Más de la mitad» se sostiene; «la mayor parte» se cambia por «más de la mitad».
- **Vacías y déficit en el mismo ámbito. Aplicado:** provincias y terciles de presión.
- **Parque útil frente a lo movilizable. Separados:** el útil no se puede saber; lo movilizable es un escenario.
- **Cruce con la presión en lugar del tamaño. Aplicado:** Spearman −0,36 y terciles. Se mantiene el tamaño como información complementaria.
- **Absorción de vacías y secundarias en el déficit. Añadida,** cualitativa, sin dato para cuantificarla.

## Respuesta a la ronda 2
- **«Menos de 10.000 viviendas» explícito. Aplicado:** el umbral es de viviendas, no de habitantes.
- **«En las provincias analizadas». Aplicado:** todo el cálculo municipal y provincial excluye las provincias selladas v6 con holdout.excluir_sellados_v6.
- **«Sin las provincias selladas» al hablar de capitales. Aplicado.**
- **Assert de que las capitales coinciden con el top-6. Añadido** en src/v17/f3_oferta_titularidad.py.
- **Guarda v6.** Ninguna cifra de vacías cambia, porque ya se excluían las mismas provincias. Cambia la elasticidad implícita del escenario de la 1.0 (ahora sobre la CCAA mediana de las 9 no selladas): −3,1 en vacías y −1,2 en construcción.
