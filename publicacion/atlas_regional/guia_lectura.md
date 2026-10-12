<!-- Generado por `make publicacion` desde output/v7_1/atlas/guia_lectura.md. No editar a mano: se regenera y un test lo comprueba. -->

# Guía de lectura para no especialistas

*Capa C4; informativo, muestra ya vista en v1. Todo lo que sigue es asociación y escenarios condicionales, no causalidad.*

## Qué es un ECM
Un modelo de corrección del error (ECM) separa dos movimientos de un precio o un alquiler. El primero es el
**corto plazo**: cuánto cambia el índice cuando cambian este trimestre el empleo, la población o las hipotecas.
El segundo es la **corrección**: si el precio se ha alejado de lo que «le correspondería» según esas variables,
qué fracción de esa distancia se recupera cada trimestre. Esa fracción es la velocidad de ajuste (φ). La
**semivida** es el tiempo que tarda la distancia en reducirse a la mitad.

Para que la corrección tenga sentido hace falta que exista una relación de **largo plazo** estable entre el
precio y esas variables. Con los datos regionales de 2007 a 2026, no se encontró esa relación estable ni común a
las regiones.

## Qué significa «no confirmada»
Antes de mirar los datos se fijaron siete hipótesis de largo plazo (por ejemplo, «más población se asocia a
precios más altos»). «No confirmada» significa que, tras corregir por hacer varios contrastes a la vez (Holm), la
evidencia no alcanza el umbral del 5 %. No significa que la hipótesis sea falsa: significa que estos datos no
permiten sostenerla. Cuando los tres estimadores usados dan signos distintos, se muestran todos y el rango.

Por eso las velocidades de ajuste de cada región se publican con el rótulo **«sin inferencia válida»**: son
estimaciones de lo que ocurrió en la muestra, sin intervalo de confianza que permita compararlas.

## Por qué las propuestas van en condicional
Las tablas de propuestas responden a «si se hiciera X, con estos supuestos, el precio o el esfuerzo variarían en
este rango». Los supuestos (elasticidades de oferta y demanda, reparto entre alquiler y compra) no están
identificados con los datos; por eso la capa es C4 y el intervalo al 90 % refleja la incertidumbre de esos
supuestos, no un error de medida. Una propuesta se marca robusta solo si el esfuerzo baja en todas las
simulaciones y el precio de mercado no sube en ninguna. Se evalúan instrumentos, no actores.

## Cómo leer una ficha
1. **Qué subió y cuánto**: variación de índices del INE entre fechas concretas.
2. **Ecuación y tabla**: los coeficientes de corto plazo tienen intervalo; φ y θ no.
3. **Diagnósticos**: avisan de cuándo una tabla es menos fiable.
4. **Descomposición**: reparte la variación entre componentes y un **residuo**; si el residuo domina, la
   variación queda sin explicar.
5. **Backtest**: un modelo «predice mejor» solo si supera a la línea base más exigente. La muestra ya se usó en
   v1 y el mejor modelo se eligió dentro de ella, así que el resultado es optimista.
6. **Qué no se puede afirmar**: los límites de lectura de esa región.

## Pendiente
La validación fuera de muestra con datos posteriores sigue pendiente; los modelos están congelados para
evaluarla (`make evaluate_v7`).
