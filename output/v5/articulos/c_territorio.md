# Diferencias territoriales en precios de la vivienda en España, 2015-2025: un análisis pre-registrado y descriptivo por diseño

**Borja Romero, economista.** Borrador de artículo (v5). Todas las cifras proceden de `output/v5/cifras_clave.csv`; cada afirmación lleva su capa de evidencia entre corchetes.

## Resumen

Este artículo describe con qué características provinciales se asocian las diferencias de variación del precio de la vivienda entre 50 provincias españolas en 2015-2025. El análisis se pre-registró (`docs/v5/prereg_B3.md`) con ocho familias de características, un cálculo de potencia previo y reglas de ajuste por comparaciones múltiples. El cálculo de potencia concluyó antes de estimar que el tamaño mínimo detectable con Holm es de 0,62 DT (0,34-1,1 DT) de la variable dependiente: con ese tamaño muestral el estudio es, por diseño, un «descriptivo honesto» y ningún resultado supera la capa [C4]. El modelo alcanza un R² de 0,91 proporción [C4]. La única asociación que sobrevive al ajuste de Holm es la convergencia: las provincias con precio inicial más alto crecieron menos, -16,0 puntos log. por DT (-23,8--8,2 puntos log. por DT) [C4]. Al controlar el error de medida con el precio inicial de una segunda fuente (Registradores), la asociación se reduce a -9,0 puntos logarítmicos (≈ %) por DT y su p pasa a 0,06 probabilidad [C4]. La demanda (empleo sectorial, población) no se distingue de cero tras Holm. La descomposición de Shapley del R² no es estable entre fuentes de precio.

**Palabras clave:** precios de la vivienda, provincias, pre-registro, potencia estadística, convergencia, Shapley.

## Abstract

We describe which provincial characteristics are associated with differences in house price growth across 50 provincias Spanish provinces in 2015-2025. The analysis was pre-registered with eight families of characteristics, an ex-ante power calculation and multiple-testing rules. The power calculation concluded before estimation that the minimum detectable size under Holm is 0,62 DT (0,34-1,1 DT) of the dependent variable: by design the study is an «honest descriptive» exercise and no result exceeds layer [C4]. The model reaches an R² of 0,91 proporción [C4]. The only association surviving Holm is convergence: provinces with higher initial prices grew less, -16,0 puntos log. por DT (-23,8--8,2 puntos log. por DT) [C4]. Controlling for measurement error with the initial price from a second source (Land Registry), the association falls to -9,0 puntos logarítmicos (≈ %) por DT with p 0,06 probabilidad [C4]. Demand shifters are not distinguishable from zero after Holm. The Shapley decomposition of R² is not stable across price sources.

## Introducción

Las diferencias territoriales de precios en España son grandes y persistentes, y en el debate se atribuyen a la demanda (empleo, inmigración, turismo), a la oferta (suelo, construcción) o a la financiación. Con 50 provincias observaciones, ninguna de esas atribuciones se puede contrastar con potencia suficiente si se ajusta por el número de hipótesis. Este artículo toma esa limitación como punto de partida: pre-registra las hipótesis, calcula la potencia antes de estimar y presenta los resultados como descripción.

## Datos

Precio: valor tasado de la vivienda libre del MIVAU (principal) y precio de Registradores (control). Alquiler: SERPAVI agregado a provincia (robustez). Características: empleo sectorial (EPA, instrumento tipo Bartik), variación del Padrón, PIB per cápita (CRE), VUT del INE, viviendas del Censo 2021, hipotecas del INE y la clasificación de presión de A4. Ceuta y Melilla quedan fuera. Las desviaciones del pre-registro están en `output/v5/B3/desviaciones.md`; todas se tratan como exploratorias.

## Método

MCO con las ocho familias a la vez y regresores estandarizados; errores `HC3` y de Conley (umbrales de cien y doscientos kilómetros), usando el mayor p; inferencia por aleatorización de Freedman-Lane con semilla fija; Holm sobre las ocho familias y, como referencia, sobre las tres hipótesis confirmatorias; BH sobre las exploratorias; multiverso de especificaciones; sensibilidad de Oster y de Cinelli-Hazlett; descomposición de Shapley del R² con dos fuentes de precio. Al tratarse de un corte transversal, la comparación con AR(4) y la validación en bloques no aplican: se sustituyen por validación cruzada dejando una provincia fuera frente a un modelo de solo media.

**Potencia previa.** El tamaño mínimo detectable con potencia del ochenta por ciento y Holm sobre ocho familias es 0,62 DT en el escenario de referencia, con un rango en la rejilla de supuestos de 0,34-1,1 DT (`output/v5/B3/potencia.md`). Al superar la mitad de una desviación típica, la regla pre-registrada fija la capa máxima en [C4] y la redacción de «descriptivo honesto»: un resultado no significativo no es evidencia de ausencia de asociación.

## Resultados

| Hipótesis | Coeficiente por DT (`IC95`) | p Holm, ocho familias | p Holm, tres confirmatorias | p por aleatorización |
|---|---|---|---|---|
| Demanda de empleo (Bartik), `H-B3-1` | 2,4 puntos log. por DT (-0,06-4,8 puntos log. por DT) | 0,33 probabilidad | 11,2 % (valor p) | 4,9 % (valor p) |
| Población, `H-B3-2` | 3,6 puntos log. por DT (-0,74-7,8 puntos log. por DT) | 0,41 probabilidad | 11,2 % (valor p) | 7,3 % (valor p) |
| Precio inicial (convergencia), `H-B3-6` | -16,0 puntos log. por DT (-23,8--8,2 puntos log. por DT) | 0,13 % (valor p) | 0,05 % (valor p) | 0,02 % (valor p) |

Todas las filas son [C4]. El empleo y la población tienen el signo esperado, pero no se distinguen de cero tras Holm. En el multiverso, el signo del empleo se mantiene en 62,5 % de las especificaciones, el de la población en 100,0 % y el de la convergencia en 100,0 % [C4].

**Convergencia y error de medida.** Un coeficiente negativo del precio inicial puede ser mecánico: si el precio de 2015 se mide con error, el error aparece con signo contrario en la variación. Para controlarlo se usa el precio inicial de Registradores, que no comparte el error del valor tasado. La asociación se reduce de -16,0 puntos log. por DT a -9,0 puntos logarítmicos (≈ %) por DT y su p (mayor de `HC3` y Conley) es 0,06 probabilidad [C4]. La convergencia es, por tanto, compatible con una parte de error de medida; la parte restante no se distingue con claridad de cero en la especificación de control.

**Shapley no estable.** Las cuotas de R² por familia no conservan el orden entre las dos fuentes de precio: correlación de Spearman 0,91 coeficiente y tau de Kendall 0,79 coeficiente, pero el orden no coincide [C4]. Con el valor tasado, las mayores cuotas corresponden a oferta y suelo (25,9 % del R2 (23,2-28,6 % del R2)) y demografía (23,6 % del R2 (21,1-26,2 % del R2)) [C4]; entre métodos y periodos, la tau mínima del orden de familias es -0,71 tau (4 familias) (-0,71-1,0 tau (4 familias)) [C4]. Ninguna lectura del tipo «el factor más importante es...» es estable.

**Ajuste fuera de muestra.** El error cuadrático medio dejando una fuera es 0,07 log-puntos, frente a 0,16 log-puntos del modelo de solo media [C4]. El modelo describe bien la geografía de precios, pero eso no identifica qué característica la produce.

![Variación del precio por provincia, 2015-2025](B3/figuras/mapa_P1.png)

![Cuotas de Shapley del R² con dos fuentes de precio](B3/figuras/shapley.png)

## Robustez

Con el precio de Registradores el R² es 0,82 proporción [C4]. Las especificaciones con alquiler SERPAVI tienen menos provincias por cobertura. Las cotas de Oster y Cinelli-Hazlett se publican en `output/v5/B3/tablas/sensibilidad.json`.

## Discusión

El artículo muestra lo que un panel de 50 provincias puede y no puede decir. Puede describir: la geografía de los precios es muy predecible con características observables. No puede atribuir: con el tamaño mínimo detectable calculado de antemano, las asociaciones de magnitud plausible de la demanda no se distinguen del ruido tras ajustar por comparaciones múltiples. La convergencia es la única regularidad robusta al ajuste y es en parte compatible con error de medida. Las comparaciones con organismos se recogen en `output/v5/D3/convergencia.md` (2 coinciden y 1 difieren) [C4].

## Conclusión

Las diferencias territoriales de precios en 2015-2025 se asocian sobre todo con el nivel de partida [C4], en parte por error de medida. Ni el empleo ni la población se distinguen de cero tras Holm [C4], y la importancia relativa de las familias no es estable [C4]. El valor del ejercicio está en el diseño: pre-registro, potencia previa y negativos reportados.

## Referencias

- Goldsmith-Pinkham, P., Sorkin, I. y Swift, H. (2020). Bartik instruments: What, when, why, and how. *American Economic Review*. [DOI](https://doi.org/10.1257/aer.20181047). VERIFICADA · Q1.
- Borusyak, K., Hull, P. y Jaravel, X. (2022). Quasi-experimental shift-share research designs. *Review of Economic Studies*. [DOI](https://doi.org/10.1093/restud/rdab030). VERIFICADA · Q1.
- Saiz, A. (2007). Immigration and housing rents in American cities. *Journal of Urban Economics*. [DOI](https://doi.org/10.1016/j.jue.2006.07.004). VERIFICADA · Q1.
- Harvey, D., Leybourne, S. y Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*. DOI `10.1016/S0169-2070(96)00719-4`. VERIFICADA · Q1.
- Conley (1999), Oster (2019), Cinelli y Hazlett (2020), Freedman y Lane (1983): métodos usados. NO VERIFICADAS en el registro del proyecto.

## Revistas adecuadas

- *Regional Science and Urban Economics* — Q1 (registrado en `docs/literatura.md`, Scimago).
- *Papers in Regional Science* — cuartil no verificado (fuentes secundarias indican Q1; no comprobado en Scimago).
- *Investigaciones Regionales – Journal of Regional Research* — cuartil no verificado.
- *SERIEs – Journal of the Spanish Economic Association* — cuartil no verificado.
