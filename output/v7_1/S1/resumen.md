# V7.1-S1 · Dosis, coste fiscal y normalización de los instrumentos de R6 (capa C4)

Escenarios condicionales («si se hiciera X, con estos supuestos…»), no efectos identificados. Se reproducen las extracciones de Monte Carlo de R6 (v7) con la misma semilla; la variación de precio coincide con output/v7/R6/impactos.csv (comprobado en el script). Se evalúan instrumentos, no actores.

**Nota de lectura (C4).** El signo lo fija en gran parte la fórmula de incidencia: los instrumentos de cantidad bajan el precio (Δp/p = −(ΔQ/Q)/(εs+|εd|)) y las ayudas a la demanda lo suben (Δp/p = s·|εd|/(εs+|εd|)). Lo informativo son las magnitudes relativas entre instrumentos y CCAA, condicionadas a la rejilla de elasticidades de v5 (la regional no es utilizable en ninguna CCAA).

## Definiciones

- **Dosis**: cantidad a la que se aplica el instrumento (ver tabla). Horizonte: 2, 5 y 10 años; los titulares son a 10 años.
- **Coste fiscal anual** (M€/año, sin efectos inducidos ni descuento): e y f1 = s × compraventas 2025 × 90 m² × valor tasado 2025T4 (como en R6); f2 = rebaja del coste × cuota del coste × visados 2025 × 90 m² × valor tasado. Coste a 10 años = 10 × anual.
- **Efecto por 10.000 viviendas** (instrumentos de cantidad): variación del precio (puntos %) por cada 10.000 viviendas de dosis acumulada.
- **Efecto por 100 M€ anuales** (instrumentos con coste): variación del precio de mercado y del precio neto pagado por el beneficiario por cada 100 M€/año.
- **Coste por punto**: M€ anuales por punto porcentual de reducción del precio neto pagado (en f2, del precio de mercado). En e y f1 el precio de mercado SUBE: el coste por punto se refiere solo al beneficiario.
- **Regla de lectura para los instrumentos de cantidad** (sin coste estimable): si el coste por vivienda fuera u euros, el efecto por 100 M€ sería «efecto por 10.000 viviendas × 10.000 / u». No se publica ningún u: no hay base verificada.

## Resumen nacional (mediana entre CCAA y rango entre CCAA, 10 años, rejilla)

| Instrumento | Mercado | Dosis (mediana CCAA) | Δ precio de mercado (%) | Coste anual (M€) | Efecto por 10.000 viv. (pp) | Efecto por 100 M€/año en precio de mercado (pp) | Coste por punto (M€/año) |
|---|---|---|---|---|---|---|---|
| construcción adicional | compra | 21.145 | -1,44 [-3,96; -0,33] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| construcción adicional | alquiler | 21.145 | -1,58 [-4,40; -0,37] | no estimable | -0,696 [-2,740; -0,124] | — | — |
| movilización de vacías | compra | 23.336 | -1,34 [-2,98; -0,57] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| movilización de vacías | alquiler | 23.336 | -3,78 [-8,37; -1,63] | no estimable | -1,748 [-6,804; -0,306] | — | — |
| vivienda pública o asequible | compra | 9.629 | -0,57 [-1,01; -0,13] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| vivienda pública o asequible | alquiler | 9.629 | -2,96 [-5,28; -0,64] | no estimable | -3,169 [-12,218; -0,560] | — | — |
| regulación local de turísticos | compra | 2.125 | -0,09 [-0,53; -0,03] | no estimable | -0,609 [-2,353; -0,108] | — | — |
| regulación local de turísticos | alquiler | 2.125 | -0,50 [-3,05; -0,18] | no estimable | -3,524 [-13,579; -0,620] | — | — |
| ayudas a la demanda | compra | 26.678 | 4,37 [4,14; 8,09] | 378 [68; 2915] | — | 1,364 [0,158; 7,603] | 76 [12; 516] |
| ayudas a la demanda | alquiler | 26.678 | 4,37 [4,14; 8,09] | no estimable | — | — | — |
| rebaja de ITP/IVA (vivienda nueva) | compra | 26.678 | 1,07 [1,01; 1,99] | 93 [17; 718] | — | 1,364 [0,158; 7,603] | 82 [13; 550] |
| rebaja de impuestos y costes de construcción (no difundible) | compra | 4.308 | -1,04 [-1,08; -0,29] | 15 [4; 135] | — | -6,542 [-29,859; -0,823] | 15 [3; 121] |
| rebaja de impuestos y costes de construcción (no difundible) | alquiler | 4.308 | -1,04 [-1,08; -0,29] | (el de compra) | — | — | — |

Rango entre corchetes: mínimo y máximo de las medianas de las 17 CCAA. El rango p5-p95 de cada CCAA está en dosis_coste.csv.

## Dosis por instrumento

| Instrumento | Dosis | Coste |
|---|---|---|
| construcción adicional | viviendas adicionales acumuladas (llegan tras 1 año); 50-100 % del mínimo entre la necesidad anual T3 y la capacidad observada (máximo anual de visados 2007-2025 menos visados 2025; v7.2) | coste no estimable: no hay coste unitario por vivienda (suelo, obra, financiación pública) verificado ni versionado; el escenario no fija quién paga |
| movilización de vacías | viviendas vacías movilizadas acumuladas; triangular(M_min, M_central, M_max) de T3 / 10 por año | coste no estimable: no hay coste unitario verificado de movilización (incentivo, rehabilitación, recargo del IBI) ni reparto entre recaudación y gasto |
| vivienda pública o asequible | viviendas públicas o asequibles netas de desplazamiento, acumuladas; 20 % × U(0,5; 1,5) de la necesidad anual, desplazamiento 0-50 % | coste no estimable: no hay coste unitario verificado por vivienda pública (v5 D1: «coste unitario sin dato verificado») |
| regulación local de turísticos | viviendas turísticas que vuelven al uso residencial (una vez); 5-30 % del stock VUT 2025T4 | coste no estimable: regulación sin coste fiscal directo verificable (inspección y compensaciones sin base) |
| ayudas a la demanda | compraventas beneficiarias por año (todas las de 2025) con ayuda del 5-15 % del precio | estimado (C4); en alquiler, coste no estimable: el panel v7 no tiene renta media del alquiler en euros por CCAA ni número de hogares beneficiarios |
| rebaja de ITP/IVA (vivienda nueva) | compraventas beneficiarias por año (todas las de 2025; cota superior: el escenario es de vivienda nueva) con rebaja de 1-4 puntos | estimado (C4) |
| rebaja de impuestos y costes de construcción (no difundible) | viviendas nuevas por año (visados 2025) con rebaja del coste del 2-6 % y cuota del coste en el precio del 40-70 % | estimado (C4) |

## Lectura

- Los instrumentos de cantidad no tienen coste fiscal estimable con base versionada: se comparan por su dosis y su efecto por 10.000 viviendas, no por euro.
- En compra, el efecto por 10.000 viviendas es el MISMO para vacías, vivienda pública y turísticos en cada CCAA (la fórmula solo depende del parque y de las elasticidades). Lo que los distingue es la dosis y, en alquiler, la fracción que llega al alquiler. Del mismo modo, el efecto por 100 M€ en el precio de mercado es idéntico para las ayudas a la demanda y la rebaja de ITP/IVA: ambos son una intensidad s sobre el mismo valor de compras. Son propiedades de la fórmula, no hallazgos.
- Las ayudas a la demanda y la rebaja de ITP/IVA reducen el precio neto del beneficiario, pero suben el precio de mercado para el resto. Su coste por punto es de reducción del precio neto, no del precio de mercado.
- La rebaja de impuestos y costes de construcción es NO DIFUNDIBLE (v7.2): su escenario sobrestima el efecto por diseño (R6 traslada la rebaja al precio de todo el mercado, mientras que el coste fiscal solo cubre la obra nueva). Sus filas se conservan para trazabilidad.
- Construcción adicional (v7.2): la dosis de R6 era 0 en la mayoría de las CCAA porque medía la capacidad con el máximo de visados de 2016-2025. Desde v7.2 la dosis es el mínimo entre la necesidad anual de T3 y la capacidad observada con el máximo de 2007-2025 (output/v7_2/construccion/resumen.md); es una capacidad generosa, que incluye el auge de 2007-2008.
- Todo es C4: los parámetros son supuestos de la rejilla. No se recomienda ningún instrumento; se comparan magnitudes condicionales.
