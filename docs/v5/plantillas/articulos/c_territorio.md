# Diferencias territoriales en precios de la vivienda en España, 2015-2025: un análisis pre-registrado y descriptivo por diseño

**Borja Romero, economista.** Borrador de artículo (v5). Todas las cifras proceden de `output/v5/cifras_clave.csv`; cada afirmación lleva su capa de evidencia entre corchetes.

## Resumen

Este artículo describe con qué características provinciales se asocian las diferencias de variación del precio de la vivienda entre {{E-B3-N}} españolas en 2015-2025. El análisis se pre-registró (`docs/v5/prereg_B3.md`) con ocho familias de características, un cálculo de potencia previo y reglas de ajuste por comparaciones múltiples. El cálculo de potencia concluyó antes de estimar que el tamaño mínimo detectable con Holm es de {{E-B3-EMD}} de la variable dependiente: con ese tamaño muestral el estudio es, por diseño, un «descriptivo honesto» y ningún resultado supera la capa [C4]. El modelo alcanza un R² de {{B3-R2}} [C4]. La única asociación que sobrevive al ajuste de Holm es la convergencia: las provincias con precio inicial más alto crecieron menos, {{E-B3-H-B3-6-ic}} [C4]. Al controlar el error de medida con el precio inicial de una segunda fuente (Registradores), la asociación se reduce a {{B3-H-B3-6-b-control}} y su p pasa a {{B3-H-B3-6-p-control:valor}} [C4]. La demanda (empleo sectorial, población) no se distingue de cero tras Holm. La descomposición de Shapley del R² no es estable entre fuentes de precio.

**Palabras clave:** precios de la vivienda, provincias, pre-registro, potencia estadística, convergencia, Shapley.

## Abstract

We describe which provincial characteristics are associated with differences in house price growth across {{E-B3-N}} Spanish provinces in 2015-2025. The analysis was pre-registered with eight families of characteristics, an ex-ante power calculation and multiple-testing rules. The power calculation concluded before estimation that the minimum detectable size under Holm is {{E-B3-EMD}} of the dependent variable: by design the study is an «honest descriptive» exercise and no result exceeds layer [C4]. The model reaches an R² of {{B3-R2}} [C4]. The only association surviving Holm is convergence: provinces with higher initial prices grew less, {{E-B3-H-B3-6-ic}} [C4]. Controlling for measurement error with the initial price from a second source (Land Registry), the association falls to {{B3-H-B3-6-b-control}} with p {{B3-H-B3-6-p-control:valor}} [C4]. Demand shifters are not distinguishable from zero after Holm. The Shapley decomposition of R² is not stable across price sources.

## Introducción

Las diferencias territoriales de precios en España son grandes y persistentes, y en el debate se atribuyen a la demanda (empleo, inmigración, turismo), a la oferta (suelo, construcción) o a la financiación. Con {{E-B3-N}} observaciones, ninguna de esas atribuciones se puede contrastar con potencia suficiente si se ajusta por el número de hipótesis. Este artículo toma esa limitación como punto de partida: pre-registra las hipótesis, calcula la potencia antes de estimar y presenta los resultados como descripción.

## Datos

Precio: valor tasado de la vivienda libre del MIVAU (principal) y precio de Registradores (control). Alquiler: SERPAVI agregado a provincia (robustez). Características: empleo sectorial (EPA, instrumento tipo Bartik), variación del Padrón, PIB per cápita (CRE), VUT del INE, viviendas del Censo 2021, hipotecas del INE y la clasificación de presión de A4. Ceuta y Melilla quedan fuera. Las desviaciones del pre-registro están en `output/v5/B3/desviaciones.md`; todas se tratan como exploratorias.

## Método

MCO con las ocho familias a la vez y regresores estandarizados; errores `HC3` y de Conley (umbrales de cien y doscientos kilómetros), usando el mayor p; inferencia por aleatorización de Freedman-Lane con semilla fija; Holm sobre las ocho familias y, como referencia, sobre las tres hipótesis confirmatorias; BH sobre las exploratorias; multiverso de especificaciones; sensibilidad de Oster y de Cinelli-Hazlett; descomposición de Shapley del R² con dos fuentes de precio. Al tratarse de un corte transversal, la comparación con AR(4) y la validación en bloques no aplican: se sustituyen por validación cruzada dejando una provincia fuera frente a un modelo de solo media.

**Potencia previa.** El tamaño mínimo detectable con potencia del ochenta por ciento y Holm sobre ocho familias es {{E-B3-EMD:valor}} en el escenario de referencia, con un rango en la rejilla de supuestos de {{E-B3-EMD:rango}} (`output/v5/B3/potencia.md`). Al superar la mitad de una desviación típica, la regla pre-registrada fija la capa máxima en [C4] y la redacción de «descriptivo honesto»: un resultado no significativo no es evidencia de ausencia de asociación.

## Resultados

| Hipótesis | Coeficiente por DT (`IC95`) | p Holm, ocho familias | p Holm, tres confirmatorias | p por aleatorización |
|---|---|---|---|---|
| Demanda de empleo (Bartik), `H-B3-1` | {{E-B3-H-B3-1-ic}} | {{B3-H-B3-1-p:valor}} | {{E-B3-H-B3-1-p3}} | {{E-B3-H-B3-1-pri}} |
| Población, `H-B3-2` | {{E-B3-H-B3-2-ic}} | {{B3-H-B3-2-p:valor}} | {{E-B3-H-B3-2-p3}} | {{E-B3-H-B3-2-pri}} |
| Precio inicial (convergencia), `H-B3-6` | {{E-B3-H-B3-6-ic}} | {{E-B3-H-B3-6-p8}} | {{E-B3-H-B3-6-p3}} | {{E-B3-H-B3-6-pri}} |

Todas las filas son [C4]. El empleo y la población tienen el signo esperado, pero no se distinguen de cero tras Holm. En el multiverso, el signo del empleo se mantiene en {{B3-mv-H-B3-1}} de las especificaciones, el de la población en {{B3-mv-H-B3-2}} y el de la convergencia en {{B3-mv-H-B3-6}} [C4].

**Convergencia y error de medida.** Un coeficiente negativo del precio inicial puede ser mecánico: si el precio de 2015 se mide con error, el error aparece con signo contrario en la variación. Para controlarlo se usa el precio inicial de Registradores, que no comparte el error del valor tasado. La asociación se reduce de {{E-B3-H-B3-6-ic:valor}} a {{B3-H-B3-6-b-control}} y su p (mayor de `HC3` y Conley) es {{B3-H-B3-6-p-control:valor}} [C4]. La convergencia es, por tanto, compatible con una parte de error de medida; la parte restante no se distingue con claridad de cero en la especificación de control.

**Shapley no estable.** Las cuotas de R² por familia no conservan el orden entre las dos fuentes de precio: correlación de Spearman {{B3-shap-spearman}} y tau de Kendall {{E-B3-kendall}}, pero el orden no coincide [C4]. Con el valor tasado, las mayores cuotas corresponden a oferta y suelo ({{B4-b3-shapley-oferta_suelo}}) y demografía ({{B4-b3-shapley-demografica}}) [C4]; entre métodos y periodos, la tau mínima del orden de familias es {{B4-estabilidad-tau-min}} [C4]. Ninguna lectura del tipo «el factor más importante es...» es estable.

**Ajuste fuera de muestra.** El error cuadrático medio dejando una fuera es {{E-B3-rmse:valor}}, frente a {{E-B3-rmse:max}} del modelo de solo media [C4]. El modelo describe bien la geografía de precios, pero eso no identifica qué característica la produce.

![Variación del precio por provincia, 2015-2025](B3/figuras/mapa_P1.png)

![Cuotas de Shapley del R² con dos fuentes de precio](B3/figuras/shapley.png)

## Robustez

Con el precio de Registradores el R² es {{E-B3-R2reg}} [C4]. Las especificaciones con alquiler SERPAVI tienen menos provincias por cobertura. Las cotas de Oster y Cinelli-Hazlett se publican en `output/v5/B3/tablas/sensibilidad.json`.

## Discusión

El artículo muestra lo que un panel de {{E-B3-N}} puede y no puede decir. Puede describir: la geografía de los precios es muy predecible con características observables. No puede atribuir: con el tamaño mínimo detectable calculado de antemano, las asociaciones de magnitud plausible de la demanda no se distinguen del ruido tras ajustar por comparaciones múltiples. La convergencia es la única regularidad robusta al ajuste y es en parte compatible con error de medida. Las comparaciones con organismos se recogen en `output/v5/D3/convergencia.md` ({{D3-coincide:num}} coinciden y {{D3-difiere:num}} difieren) [C4].

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
