# P9 · Predicción y nowcasting del precio de la vivienda en España: literatura

Pregunta: ¿puede algún modelo (factores dinámicos, combinación, BVAR, penalizados, MIDAS con compraventas, hipotecas, visados y afiliación) batir al AR(4) en la misma muestra para el precio trimestral de la vivienda en España? En el repositorio ninguno lo ha hecho; con 73 errores recursivos el DM solo detecta reducciones del ECM del 18 % al 30 % (output/v15/potencia/informe.md, fila P9).

Alcance y límites de lo leído. Todas las fichas se basan en el resumen o en el registro bibliográfico (IDEAS/RePEc, Crossref, arXiv, páginas del Banco de España), nunca en el texto completo. Donde el resumen no da cifras, la ficha lo dice y no se aporta ninguna. Las líneas «Validez externa» son valoración propia del lector, no afirmaciones de los autores. No he encontrado: (i) un trabajo de Ghysels y coautores que aplique MIDAS al precio de la vivienda (lo más cercano es Andreou, Ghysels y Kourtellos 2013, MIDAS con datos financieros diarios, que no es de vivienda y no ficho, y Trojanek et al. 2025, que sí lo es y está fichado); (ii) un trabajo del Banco de España de nowcasting o previsión puntual del precio con compraventas, hipotecas o visados (solo el modelo de riesgo a la baja); (iii) un trabajo de Gupta y coautores con ECM relativo frente al AR en el resumen leído (Plakandaras et al. lo da frente al paseo aleatorio). Leídos pero sin ficha por el tope de 16: Bork y Møller (2018, Real Estate Economics 46(3), DOI 10.1111/1540-6229.12185: PCA, PLS y PLS disperso con 128 series, resumen sin cifras); Das, Gupta y Kabundi (2010, Journal of Housing Research 19(1), DOI 10.1080/10835547.2010.12092016: FAVAR mejor en 8 de 9 divisiones censales); Gupta, Kabundi y Miller (2011, Journal of Housing Research 20(2), 161-191, sin DOI visible: 20 estados, los fundamentales mejoran la previsión en 13 y no en 7); Kohlscheen (2025, arXiv 2509.21460, 13 economías: bosque aleatorio con RMSE un 44 % menor que MCO con las mismas 10 variables).

## A. Contraste de capacidad predictiva

### Diebold y Mariano (1995). Comparing Predictive Accuracy
- DOI: sin DOI · Revista: Journal of Business & Economic Statistics 13(3), 253-263
- Leído: resumen (https://www.econbiz.de/Record/comparing-predictive-accuracy/10005170846 y https://econpapers.repec.org/RePEc:fip:fedmem:52, versión de trabajo de 1991; además el resumen de Diebold 2012 en https://www.nber.org/papers/w18391.pdf, citado por el resultado de búsqueda). Crossref devolvió solo el documento técnico NBER t0169 (DOI 10.3386/t0169, 1994) y no el artículo de la revista, por eso no se asigna DOI.
- Diseño e identificación: contraste de la hipótesis nula de igual precisión de dos pronósticos rivales; no exige pérdida cuadrática, admite errores no gaussianos, de media no nula y con correlación serial; versiones asintótica y exacta de muestra finita. Datos: ninguno propio en lo leído. Resultado: no hay magnitud; es un procedimiento. Diebold (2012), según el resumen leído, aclara que el contraste sirve para comparar pronósticos y no estaba pensado para comparar modelos.
- Validez externa para España: el contraste es aplicable, pero con 73 errores recursivos y horizonte múltiple la autocorrelación de la diferencia de pérdidas es fuerte; la potencia es la del informe de potencia del repositorio. Discrepancia: el matiz de Diebold (2012) (pronósticos, no modelos) separa el DM del de Giacomini-White y del de Clark-West, que tratan la estimación y el anidamiento.
- Estado: NO VERIFICADA (sin DOI)

### Harvey, Leybourne y Newbold (1997). Testing the equality of prediction mean squared errors
- DOI: sin DOI · Revista: International Journal of Forecasting 13(2), 281-291
- Leído: resumen (https://ideas.repec.org/a/eee/intfor/v13y1997i2p281-291.html, que solo da la referencia; https://iaorifors.com/paper/20644, resumen visto a través de la búsqueda web)
- Diseño e identificación: examinan dos contrastes de igualdad de precisión de pronósticos y modificaciones para corregir sus defectos, y recomiendan un enfoque para uso práctico. La corrección de muestra pequeña del estadístico DM (reescalado con la raíz de (T+1−2h+h(h−1)/T)/T y comparación con una t) se atribuye al artículo en fuentes secundarias de la búsqueda (documentación de software); no la he visto en el resumen del artículo. Datos y magnitud: no constan en lo leído.
- Validez externa para España: con T pequeño y horizontes de 4 u 8 trimestres, la corrección de muestra finita es la práctica mínima; no resuelve la baja potencia (valoración propia). Discrepancias: no consta ninguna en lo leído.
- Estado: NO VERIFICADA (sin DOI)

### Giacomini y White (2006). Tests of Conditional Predictive Ability
- DOI: 10.1111/j.1468-0262.2006.00718.x · Revista: Econometrica 74(6), 1545-1578
- Leído: resumen (https://ideas.repec.org/a/ecm/emetrp/v74y2006i6p1545-1578.html; DOI también en el registro de Crossref)
- Diseño e identificación: marco de contrastes fuera de muestra y de selección de pronósticos que permite modelos mal especificados; (i) conserva el efecto de la incertidumbre de estimación en el límite asintótico, (ii) evalúa de forma condicional, es decir, qué pronóstico será mejor en una fecha futura, lo que incluye el caso incondicional; vale para modelos anidados y no anidados; propone una regla de decisión en dos pasos. Ilustración: métodos de reducción de parámetros con muchos predictores macro. Magnitud: ninguna en el resumen.
- Validez externa para España: la evaluación condicional con 73 errores añade instrumentos y reduce la potencia (valoración propia). Discrepancia con Clark-West: GW se plantea sobre la precisión del pronóstico estimado, CW sobre el modelo poblacional anidado; pueden dar conclusiones distintas con el mismo par AR(4)/modelo ampliado.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Clark y West (2007). Approximately normal tests for equal predictive accuracy in nested models
- DOI: 10.1016/j.jeconom.2006.05.023 · Revista: Journal of Econometrics
- Leído: resumen (versión de trabajo SSRN 874146 vía Crossref, https://api.crossref.org/works; el DOI de la revista figura en el registro de Crossref)
- Diseño e identificación: cuando el modelo simple (nulo) es el proceso generador, el modelo mayor añade ruido al estimar parámetros que son cero y su ECM tiende a ser mayor. Proponen ajustar los ECM por ese ruido y aplicar contrastes estándar a la diferencia ajustada. Argumentan que los valores críticos normales dan tamaños cercanos, aunque algo inferiores, al nominal, y lo respaldan con simulaciones. Magnitud: ninguna.
- Validez externa para España: es la prueba natural para un AR(4) frente a un AR(4) ampliado con indicadores mensuales (anidados). Un CW significativo con ECM relativo mayor que 1 es posible y no equivale a «predice mejor» según la regla del plan (valoración propia). Discrepancia con DM/GW: con anidamiento, el DM es conservador según el resumen.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Hansen, Lunde y Nason (2011). The Model Confidence Set
- DOI: 10.3982/ECTA5771 · Revista: Econometrica 79(2), 453-497
- Leído: resumen (https://ideas.repec.org/a/ecm/emetrp/v79y2011i2p453-497.html y https://www.econometricsociety.org/publications/econometrica/2011/03/01/model-confidence-set)
- Diseño e identificación: procedimiento que devuelve un conjunto de modelos que, con un nivel de confianza dado, contiene al mejor, de forma análoga a un intervalo de confianza. Datos poco informativos dan un conjunto grande y datos informativos uno pequeño. No exige un modelo verdadero y sirve para comparar objetos más generales. Aplicaciones: pronósticos de inflación de Stock y Watson (1999) y regresiones de regla de Taylor con criterios de verosimilitud en muestra. Magnitud: ninguna en el resumen.
- Validez externa para España: con T corto el MCS probablemente no excluya casi nada, y que el AR(4) permanezca en el conjunto no demuestra que sea mejor (valoración propia, coherente con la propiedad que describe el resumen). Es la herramienta adecuada para declarar un nulo informativo: «el conjunto contiene a todos los modelos».
- Estado: VERIFICADA (Crossref; cuartil no verificado)

## B. Factores, combinación, BVAR y nowcasting

### Stock y Watson (2002). Forecasting Using Principal Components from a Large Number of Predictors
- DOI: sin DOI · Revista: Journal of the American Statistical Association 97(460), 1167-1179
- Leído: resumen (https://stock.scholars.harvard.edu/publications/forecasting-using-principal-components-large-number-predictors y https://collaborate.princeton.edu/en/publications/forecasting-using-principal-components-from-a-large-number-of-pre/)
- Diseño e identificación: predicción de una serie con muchos predictores N relativos a T bajo un modelo de factores aproximado; los índices se estiman por componentes principales. Teoría: la diferencia entre el pronóstico factible y el infactible con los factores verdaderos converge a cero en probabilidad cuando N y T crecen; los factores estimados son consistentes aun con variación temporal de las cargas. Magnitud empírica: no consta en lo leído.
- Validez externa para España: el resultado es asintótico en N y T; los indicadores mensuales útiles para España (compraventas, hipotecas, visados, afiliación) son pocas decenas y comparten tendencia, y el trimestral tiene T reducido (valoración propia). Discrepancia: Stock y Watson (2004) muestran que predictores individuales inestables empeoran frente al AR.
- Estado: NO VERIFICADA (sin DOI)

### Stock y Watson (2004). Combination forecasts of output growth in a seven-country data set
- DOI: 10.1002/for.928 · Revista: Journal of Forecasting 23(6), 405-430
- Leído: resumen (https://ideas.repec.org/a/jof/jforec/v23y2004i6p405-430.html)
- Diseño e identificación: combinación de pronósticos del crecimiento del producto; datos trimestrales de siete países, 1959-1999, hasta 73 predictores por país. Resultado: los pronósticos con predictores individuales son inestables en el tiempo y entre países, y en media son peores que la referencia autorregresiva; los combinados superan con frecuencia a los autorregresivos; las mejores combinaciones (por ejemplo la media simple) son las menos sensibles al rendimiento reciente de los componentes, lo que es difícil de explicar con la teoría de combinación en entorno estacionario. El resumen no da cifras de ECM.
- Validez externa para España: el objeto es el PIB, no el precio de la vivienda; la media simple de modelos ampliados es la candidata natural contra el AR(4) en P9 (valoración propia) y el resultado sugiere no ponderar por rendimiento reciente. Discrepancia: Rapach y Strauss (sección C) obtienen ganancias heterogéneas por estado con combinación.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Timmermann (2006). Forecast Combinations
- DOI: sin DOI · Revista: Handbook of Economic Forecasting, vol. 1, cap. 4, 135-196 (Elsevier)
- Leído: resumen (https://ideas.repec.org/h/eee/ecofch/1-04.html y, por contenido, la versión de trabajo de Aiolfi, Capistrán y Timmermann, CREATES 2010-21, https://ideas.repec.org/p/aah/create/2010-21.html)
- Diseño e identificación: revisión. Las combinaciones han mostrado con frecuencia mejores pronósticos en media que el mejor modelo individual ex ante; analiza qué determina la ganancia (correlación de errores, varianzas relativas) y por qué las combinaciones simples suelen batir a ponderaciones más refinadas (mala especificación, inestabilidad, error de estimación cuando hay muchos modelos en relación con T). Magnitud: no consta en lo leído.
- Validez externa para España: el argumento del error de estimación con T corto favorece la media simple frente a pesos estimados en P9 (valoración propia). Discrepancia: no consta ninguna en lo leído; la versión de 2010 es de otros autores y se cita solo por su resumen.
- Estado: NO VERIFICADA (sin DOI)

### Bańbura, Giannone y Reichlin (2010). Large Bayesian vector auto regressions
- DOI: 10.1002/jae.1137 · Revista: Journal of Applied Econometrics 25(1), 71-92
- Leído: resumen (https://ideas.repec.org/a/wly/japmet/v25y2010i1p71-92.html; el DOI procede de la respuesta de búsqueda web)
- Diseño e identificación: VAR con contracción bayesiana para sistemas dinámicos grandes; vinculando la intensidad de la contracción a la dimensión del sistema, los VAR monetarios pequeños mejoran su pronóstico al añadir variables macro e información sectorial; los VAR grandes con contracción dan respuestas a impulsos creíbles. Magnitud: no consta en el resumen.
- Validez externa para España: el resultado procede de macroeconomía de EE. UU. con series largas; con T trimestral reducido el prior domina y el BVAR tiende a un AR o a un paseo aleatorio (valoración propia). Discrepancia: en el precio de la vivienda de EE. UU., Plakandaras et al. (sección C) encuentran, según la búsqueda web, que BAR y BVAR son peores que el paseo aleatorio.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Giannone, Reichlin y Small (2008). Nowcasting: The real-time informational content of macroeconomic data
- DOI: sin DOI · Revista: Journal of Monetary Economics 55(4), 665-676
- Leído: resumen (https://ideas.repec.org/a/eee/moneco/v55y2008i4p665-676.html)
- Diseño e identificación: método formal para medir el efecto marginal de cada publicación intra-mensual sobre el pronóstico del trimestre en curso (nowcast) del PIB real; admite conjuntos grandes con calendarios de publicación escalonados («borde irregular»); el nowcast se actualiza con cada publicación. Magnitud: no consta en lo leído.
- Validez externa para España: la estructura (indicadores mensuales con retardos de publicación distintos) coincide con compraventas, hipotecas y visados, pero la ganancia depende de que el indicador se publique antes que el objetivo, y el precio de la vivienda se publica con retraso (valoración propia). Discrepancia: el trabajo trata el PIB, no un precio con fuerte persistencia.
- Estado: NO VERIFICADA (sin DOI)

## C. Predicción del precio de la vivienda

### Rapach y Strauss (2009). Differences in housing price forecastability across US states
- DOI: sin DOI · Revista: International Journal of Forecasting 25(2), 351-372
- Leído: resumen (https://ideas.repec.org/a/eee/intfor/v25y2009i2p351-372.html)
- Diseño e identificación: pronóstico del crecimiento real del precio de la vivienda por estado de EE. UU., 1995-2006; compara un modelo autorregresivo con modelos que usan variables estatales, regionales y nacionales (por la búsqueda web, con combinación de pronósticos). Resultado: la previsibilidad varía entre estados; los modelos autorregresivos, en especial con muchas variables económicas, suelen pronosticar bien en varios estados del interior; todos los modelos fallan en un grupo mayormente costero de fuerte crecimiento, que los autores atribuyen a una «desconexión» entre precios y fundamentales. El resumen leído no da ganancias numéricas.
- Validez externa para España: España tiene un mercado con tramos costeros y metropolitanos y un ciclo de burbuja 1997-2007 (valoración propia); el hallazgo de peor previsibilidad donde el precio se separa de los fundamentales anticipa más dificultad en la costa mediterránea y los archipiélagos. Discrepancia: la muestra termina en 2006, antes del desplome, como señalan trabajos posteriores citados en la búsqueda.
- Estado: NO VERIFICADA (sin DOI)

### Plakandaras, Gupta, Gogas y Papadimitriou (2015). Forecasting the U.S. real house price index
- DOI: 10.1016/j.econmod.2014.10.050 (DOI de la revista, localizado en Crossref por el orquestador; versión arXiv 10.48550/arXiv.1707.04868) · Revista: Economic Modelling 45, 259-267
- Leído: resumen (https://arxiv.org/abs/1707.04868 y https://repository.up.ac.za/items/f1447e8b-6f04-4a53-bbaa-111ea554b976)
- Diseño e identificación: método híbrido de descomposición empírica por modos (EEMD) y regresión de vectores soporte (SVR) frente a paseo aleatorio con y sin deriva, autorregresivo bayesiano (BAR) y VAR bayesiano (BVAR); pronóstico fuera de muestra del índice real de precios de la vivienda de EE. UU. (frecuencia y muestra no constan en lo leído). Resultado: el modelo híbrido supera a todos los rivales con «aproximadamente la mitad del error» de los paseos aleatorios, según el resumen. Según la búsqueda web (no confirmado en el resumen), BAR y BVAR dan peores pronósticos que el paseo aleatorio, dentro y fuera de muestra.
- Validez externa para España: la ganancia de ~50 % frente al paseo aleatorio no es comparable con el AR(4) del repositorio (el AR es un listón más exigente en series persistentes, cf. Kishor y Marfatia) y procede de un índice largo de EE. UU.; con 73 errores no se puede asumir que sea replicable (valoración propia). Discrepancia: el resultado negativo del BVAR contrasta con la lectura favorable de Bańbura et al. para sistemas grandes.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Bork y Møller (2015). Forecasting house prices in the 50 states using Dynamic Model Averaging and Dynamic Model Selection
- DOI: 10.1016/j.ijforecast.2014.05.005 · Revista: International Journal of Forecasting 31(1), 63-78
- Leído: resumen (https://ideas.repec.org/a/eee/intfor/v31y2015i1p63-78.html; versión de trabajo de 2014 vía la búsqueda web)
- Diseño e identificación: promediado y selección dinámicos de modelos (DMA/DMS) que permiten cambios en el modelo y en los parámetros en el tiempo y entre estados, para los 50 estados de EE. UU. Resultado: según el resumen, permitir que todo el modelo cambie «mejora sustancialmente» la precisión; el cambio de modelo y de parámetros es más necesario en los mercados más volátiles. El resumen no da la magnitud.
- Validez externa para España: la lógica de cambio de modelo es aplicable a una serie con rupturas (2008, 2013, 2020), pero muchos predictores candidatos con T reducido elevan el riesgo de sobreajuste (valoración propia). Discrepancia: Rapach y Strauss encuentran que los estados costeros son difíciles de prever con modelos fijos; DMA/DMS es una respuesta a ese hallazgo, no una refutación.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Kishor y Marfatia (2018). Forecasting house prices in OECD economies
- DOI: 10.1002/for.2483 · Revista: Journal of Forecasting 37(2), 170-190
- Leído: resumen (https://ideas.repec.org/a/wly/jforec/v37y2018i2p170-190.html)
- Diseño e identificación: crecimiento real del precio de la vivienda en 16 países de la OCDE con indicadores macro internos y medidas globales del mercado de vivienda. Resultado: como en EE. UU., un modelo autorregresivo supera al paseo aleatorio en la mayoría de los países; un modelo bivariante con variables macro internas clave y dos indicadores globales mejora significativamente al AR univariante; el tipo de interés interno da el menor ECM en la mayoría de los países; renta, producción industrial y bolsa también aportan; hay algo de evidencia de que el crecimiento global del precio ayuda fuera de muestra. El resumen no da cifras de ganancia ni confirma que España esté entre los 16 países (no verificado).
- Validez externa para España: es la referencia más cercana a un AR frente a ampliaciones macro en datos internacionales; su AR es un listón más exigente que el paseo aleatorio, como el de P9 (valoración propia). Discrepancia con Plakandaras et al.: ganancias modestas pero significativas frente al AR, frente a ~50 % frente a un paseo aleatorio.
- Estado: VERIFICADA (Crossref; cuartil no verificado)

### Ganics y Rodríguez-Moreno (2023). A house price-at-risk model to monitor the downside risk for the Spanish housing market
- DOI: sin DOI · Revista: Banco de España, Documentos de Trabajo n.º 2244 (23-01-2023)
- Leído: resumen (https://www.bde.es/wbe/es/publicaciones/analisis-economico-investigacion/documentos-trabajo/house-priceatrisk-model-to-monitor-downside-risk-for-spanish-housing-market.html)
- Diseño e identificación: modelo «at-risk» con regresiones cuantílicas; incluye la tasa trimestral de crecimiento del precio, una medida de sobrevaloración y el índice de confianza del consumidor. Según el resumen, predice con precisión la evolución del mercado español hasta dos años vista. Magnitud: no consta en la página leída (no se leyó el PDF).
- Validez externa para España: es el único trabajo del Banco de España leído que predice el precio español; evalúa la cola inferior de la distribución (riesgo a la baja), no el error de la media, así que no es comparable con el DM sobre el ECM del AR(4) (valoración propia). No he encontrado un nowcasting del Banco de España con compraventas, hipotecas o visados.
- Estado: NO VERIFICADA (sin DOI)

### Trojanek, Hartigan, Pfeifer y Steurer (2025). Nowcasting Transaction-Based House Price Indices Using Web-Scraped Listings and MIDAS Regression
- DOI: sin DOI · Revista: CAMA Working Paper 45/2025 (Crawford School, ANU)
- Leído: resumen (https://crawford.anu.edu.au/cama/content-centre/research/nowcasting-transaction-based-house-price-indices-using-web-scraped)
- Diseño e identificación: 16 años de microdatos de Varsovia y Poznań; índices mensuales de precios de oferta e índices trimestrales de precios de transacción; los de oferta preceden a los de transacción uno o dos meses (más en Varsovia); MIDAS para el nowcast del crecimiento trimestral con datos mensuales de oferta. Resultado: las especificaciones preferidas reducen el error a un trimestre frente a autorregresivos, con más ganancia cuando se usan el primer o segundo mes del trimestre. Cifras: la búsqueda web las da como reducción del RMSE de aproximadamente 16-23 % en Varsovia y 5-15 % en Poznań; no las he visto en la página leída (solo cualitativa) y deben comprobarse en el PDF.
- Validez externa para España: la ganancia viene de un indicador de precio de oferta mensual, no de cantidades (compraventas, visados); no hay en el repositorio una serie mensual de precios de oferta redistribuible (valoración propia). Es un documento de trabajo, no revisado. Ghysels no figura como autor.
- Estado: NO VERIFICADA (sin DOI)

## Qué sería sorprendente replicar o no replicar en España, y por qué

- Sorprendería replicar una reducción del ECM del orden del 50 % frente al AR(4): el resumen de Plakandaras et al. la da frente al paseo aleatorio en EE. UU., y Kishor y Marfatia indican que el AR ya supera al paseo aleatorio en la mayoría de países. El listón de P9 es el AR(4), no el paseo.
- Sorprendería, por el tamaño, que el DM, el GW o el CW detecten con 73 errores recursivos una mejora menor del 18 %-30 % del ECM: el informe de potencia dice que no hay potencia por debajo. Una significación aislada con un solo modelo y un solo horizonte debe leerse junto con las más de 43.510 especificaciones previas del repositorio y con corrección múltiple.
- No sería sorprendente un nulo: Stock y Watson (2004) hallan predictores individuales inestables y peores que el AR en media, y, según la búsqueda, el BVAR de Plakandaras et al. no bate al paseo aleatorio. Un MCS que conserve a casi todos los modelos sería coherente con T corto, no una prueba de que el AR(4) sea el mejor.
- Sorprendería, pero sería coherente con Stock y Watson (2004) y Timmermann (2006), que ganase una media simple de modelos ampliados. Si ocurre, comprobar con Clark-West que no es ruido de estimación y que persiste en el bloque sellado.
- Sorprendería que un indicador de cantidades (compraventas, hipotecas, visados) adelante al precio: Trojanek et al. obtienen su ganancia con precios de oferta, no con cantidades, y no he leído evidencia que equipare ambos tipos de indicador.
- No sería sorprendente que cualquier ganancia fuese menor en la costa y los archipiélagos (Rapach y Strauss: peor previsibilidad donde el precio se separa de los fundamentales) ni que cambie en las rupturas de 2008 y 2020.
- Con la muestra sellada nueva (pocos trimestres) la potencia será menor aún: el resultado esperado y correcto de declarar es «no distinguible del AR(4)», con el MCS y el ECM relativo con su intervalo.
