<!-- Generado por `make consulta` (src/consulta/generar.py). No editar a mano: se regenera y un test lo comprueba. -->

# Glosario

Términos del proyecto, en el orden en que suelen aparecer. Las definiciones son operativas y no sustituyen al [anexo metodológico](../metodologia/anexo_metodologico.md).

## Capas (C1, C2, C3, C3s, C4)

Niveles de evidencia. C1 hechos (dos fuentes o más); C2 cotas con supuestos; C3 efectos identificados (instrumento externo o diseño que supera las pruebas); C3s identificación por restricciones de signo y de cero, válida solo bajo ellas; C4 exploratorio. Nunca se promueve de capa. Véase [capas](../metodologia/capas.md).

## Escala de evidencia

CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Por debajo de CAUSAL no se usa lenguaje causal.

## SVAR

Vector autorregresivo estructural. En V8 es bayesiano, de 7 variables, con restricciones de signo y de cero. Separa shocks (actividad y renta, demográfico, crédito y tipos, demanda de vivienda, oferta) y atribuye la variación observada a cada uno.

## Restricciones de signo

Supuestos sobre el signo de la respuesta de las variables a cada shock (por ejemplo, un shock de oferta baja el precio). Identifican parcialmente el modelo; los resultados valen solo condicionados a ellas (C3s).

## Restricciones de cero

Supuestos de que ciertos shocks no afectan a ciertas variables en el impacto. Se combinan con las de signo.

## Descomposición histórica

Reparto de la variación observada de una serie en un periodo entre las contribuciones acumuladas de cada shock más una parte no atribuida (determinista). Se publica con bandas del 68 %.

## Banda del 68 %

Percentiles 16-84 de la distribución posterior. Si incluye el cero, la contribución no se distingue de cero. Los ids con sufijo -media y -mediana comparten la misma banda.

## Parte no atribuida

Componente determinista y no identificado del SVAR (condiciones iniciales y término de deriva). Se publica porque una atribución sin ella sería incompleta.

## LP-IV

Proyecciones locales con variables instrumentales. Estiman la respuesta a un shock a distintos horizontes usando un instrumento externo; solo valen si el instrumento es fuerte.

## Anderson-Rubin

Contraste y región de confianza para el coeficiente de una regresión con instrumentos que es válido aunque el instrumento sea débil; por eso se usa cuando el F efectivo es bajo.

## F efectivo

Estadístico de fuerza del instrumento robusto a heteroscedasticidad y autocorrelación (Montiel Olea y Pflueger). El umbral operativo de C3 es F efectivo mayor o igual que 10.

## Dominancia LMG

Reparto del R² entre regresores promediando sobre todos los órdenes de entrada (Lindeman, Merenda y Gold). Describe ajuste, no causa.

## Contabilidad hogares-viviendas

Identidad que descompone el cambio en hogares y viviendas; asociación, no causa. Demografía y oferta no se separan en ella.

## Multiverso

Conjunto de especificaciones razonables (variables, muestras, retardos, transformaciones) que se ajustan todas; se reporta la distribución de signos y significatividades. En V8 el tope es 50.000 especificaciones.

## BH (Benjamini-Hochberg)

Control de la tasa de falsos descubrimientos. Se aplica a familias grandes de contrastes (por ejemplo, el multiverso, con q = 0,10).

## Holm

Corrección de comparaciones múltiples que controla la tasa de error por familia; se usa en las hipótesis confirmatorias (H8-1 a H8-9).

## Hipótesis confirmatoria

Hipótesis pre-registrada con una sola evaluación. De las nueve de V8, solo H8-9 se sostiene tras Holm.

## Pre-registro

Documento con hipótesis, reglas y análisis fijados antes de ver los resultados. Las desviaciones se registran en docs/v8/desviaciones.md.

## Muestra sellada

Datos reservados que solo abre src/holdout.py, registrando cada acceso, una vez por hipótesis confirmatoria.

## SHAP

Reparto aditivo de la predicción de un modelo entre sus variables. Describe la predicción del modelo, no efectos causales.

## DML

Aprendizaje automático doble (double machine learning): estima un coeficiente tras limpiar controles con modelos flexibles. Sin identificación externa sigue siendo asociación (C4).

## AR(4) y ECM v1

Líneas base de predicción: autorregresivo de orden 4 y modelo de corrección del error de la v1. Un modelo solo «predice mejor» si supera a la más exigente en la misma muestra.

## RMSE

Raíz del error cuadrático medio de predicción. Menor es mejor; solo se compara en la misma muestra.

## Diebold-Mariano

Contraste de igualdad de precisión predictiva entre dos modelos.

## Cointegración, ARDL con cotas

Relación de largo plazo estable entre series no estacionarias. El ARDL con cotas contrasta su existencia sin saber si las series son I(0) o I(1).

## Factor común

Primer componente principal de las series de las 17 CCAA; su cuota mide cuánto de la variación se mueve a la vez en todo el país. Es comovimiento, no causa.

## GSADF

Contraste de exuberancia (raíz explosiva) en series de precios. Detecta aceleración, no sobrevaloración.

## Periodos P1-P5

P1 1995-2007 (versión larga); P2 2008T3-2013T4 (crisis); P3 2014T1-2019T4; P4 2020T2 en adelante (pandemia y tipos); P5 2022T3 hasta el último dato. Detalle en docs/v8/hipotesis.md.

## pp

Puntos porcentuales. En V8, log por 100 (aproximadamente un porcentaje en variaciones pequeñas).

## IPC de alquiler vs IPVA

El IPC de alquiler mide el alquiler del parque (contratos vigentes, con actualizaciones lentas); el IPVA, el de contratos nuevos. Se mueven distinto y no son intercambiables.

## Parque vs contratos nuevos

El parque es el conjunto de contratos vigentes (stock); los contratos nuevos reflejan el precio de mercado de entrada. Un resultado de uno no vale para el otro.

## Valor tasado

Precio medio por m² de las tasaciones hipotecarias (Ministerio de Vivienda). Es una medida de precio de compra distinta del IPV del INE y del precio de escritura.

## IPV

Índice de precios de vivienda del INE.

## SERPAVI

Sistema estatal de referencia del precio del alquiler de vivienda (Ministerio). Mide el alquiler del parque.

## Dosis y coste

Cada instrumento simulado declara cuánto se aplica (dosis) y cuánto cuesta. Las simulaciones son escenarios condicionales (C4).

## Déficit y necesidad

El déficit acumulado es hogares menos viviendas terminadas (con o sin bajas); la necesidad es el flujo anual 2026-2035 (A+R+V+F-M-K). Las viviendas liberadas por envejecimiento nunca se restan de la necesidad.

## Identificación parcial (Manski)

Cotas sobre un parámetro cuando los supuestos no bastan para un valor puntual. Fundamento de la capa C2.

## Superada / retirada

Una cifra superada fue sustituida por otra mejor (consta en cifras_superadas.csv); una hipótesis retirada se publicó con una especificación errónea y se conserva con su motivo.

## Verificador

Fichas que evalúan una afirmación (no a quien la formula) con magnitud, intervalo, límites y veredicto. Con capa C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE».

