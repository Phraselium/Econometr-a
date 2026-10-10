# Alquileres turísticos y topes al alquiler en España: una replicación y extensión con los resultados negativos a la vista

**Borja Romero, economista.** Borrador de artículo de replicación (v5). Todas las cifras proceden de `output/v5/cifras_clave.csv`; cada afirmación lleva su capa de evidencia entre corchetes.

## Resumen

Este artículo documenta un intento de replicar y extender dos resultados de la literatura empírica sobre vivienda en España: la asociación entre la presencia de viviendas de uso turístico (VUT) y los alquileres, estimada para Barcelona por García-López et al. (2020), y la asociación entre los topes al alquiler de la `Ley 11/2020` de Cataluña y las rentas y los contratos. La replicación conceptual del primer resultado, con datos de stock de contratos (SERPAVI) y de VUT del INE para 2021-2024, da un coeficiente de -4,2 milésimas de log-punto por punto de VUT/parque (-7,8--0,54 milésimas de log-punto por punto de VUT/parque) [C4], de signo contrario al original y no distinguible de cero tras el ajuste de Holm (p ajustado 26,9 % (valor p)). El artículo separa las fuentes de la discrepancia: datos (stock frente a flujo, cuantificada), periodo y método (no contrastables). Sobre los topes, las estimaciones de entrenamiento apuntan a rentas más bajas, -5,4 % (-7,1--3,7 %) [C4], pero la validación quedó contaminada y la hipótesis se retira de forma definitiva de la capa causal. Se añaden una cota de identificación parcial para VUT (2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) del stock de alquiler como máximo [C2]) y una discrepancia de medición entre el registro autonómico y el INE (cociente 1,6 veces (1,4-1,8 veces) [C4]). El artículo es una replicación honesta: los negativos se reportan y ninguna conclusión se promueve de capa.

**Palabras clave:** replicación, viviendas de uso turístico, control de alquileres, SERPAVI, identificación parcial.

## Abstract

We document an attempt to replicate and extend two results in the empirical housing literature on Spain: the association between short-term rental (STR) units and rents in Barcelona (García-López et al., 2020), and the association between the 2020 Catalan rent caps and rents and contracts. Our conceptual replication of the first result, using a stock-of-contracts rent measure (SERPAVI) and official STR counts for 2021-2024, yields -4,2 milésimas de log-punto por punto de VUT/parque (-7,8--0,54 milésimas de log-punto por punto de VUT/parque) [C4], with the opposite sign and not distinguishable from zero after Holm adjustment (adjusted p 26,9 % (valor p)). We decompose the discrepancy into data (stock versus flow, quantified), period and method (not testable). For rent caps, training-sample estimates point to lower rents, -5,4 % (-7,1--3,7 %) [C4], but validation was contaminated and the hypothesis is permanently withdrawn from the effects layer. We add a partial-identification bound for STR (2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) of the rental stock at most [C2]) and a measurement discrepancy between the regional register and the INE count (ratio 1,6 veces (1,4-1,8 veces) [C4]). Negative results are reported and no conclusion is promoted across evidence layers.

**Keywords:** replication, short-term rentals, rent control, administrative rent data, partial identification.

## Introducción

Las replicaciones en economía urbana son escasas y, cuando existen, suelen reportar solo los éxitos. Este artículo hace lo contrario: describe qué se replica, qué no y por qué, con la misma atención a los resultados nulos que a los significativos.

El punto de partida son dos preguntas frecuentes en el debate español sobre la vivienda. La primera es si la expansión de los alquileres turísticos se asocia con alquileres residenciales más altos. García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020) encontraron, para Barcelona en 2012-2016 y con una estrategia de variable instrumental, una asociación positiva entre anuncios de Airbnb y precios de oferta del alquiler. Franco y Santos (2021) encontraron asociaciones del mismo signo en Portugal. La segunda pregunta es si los topes al alquiler reducen las rentas y la oferta. Jofre-Monseny, Martínez-Mazza y Segú (2023) estudiaron la regulación catalana de 2020, y Kholodilin (2024) revisa la literatura internacional, en la que conviven reducciones de renta en el segmento regulado con reducciones de oferta.

El proyecto del que procede este artículo diseñó en su versión v3 un protocolo con hipótesis registradas, una muestra sellada y un acceso único por hipótesis confirmatoria. El artículo reporta qué ocurrió al aplicar ese protocolo: la replicación de García-López no reproduce el coeficiente, y la evaluación de los topes quedó fuera de la capa causal por un fallo del propio protocolo que se detectó después.

La contribución es metodológica y sustantiva. Metodológica, porque separa las fuentes de una discrepancia de replicación en cuantificables y no cuantificables, y porque documenta cómo una validación contaminada invalida una conclusión aunque el resultado «salga». Sustantiva, porque aporta una cota superior de lo que las VUT pueden representar en el stock de alquiler y una discrepancia de medición entre registros que condiciona cualquier estudio futuro.

## Datos

- **Alquiler, stock.** SERPAVI (Sistema Estatal de Referencia del Precio del Alquiler de Vivienda), a partir de declaraciones del IRPF: renta mediana por metro cuadrado de los contratos vigentes, por sección censal, distrito y municipio, 2015-2024. Mide un stock: incluye contratos firmados en años anteriores.
- **Alquiler, flujo.** Incasòl: renta media de los contratos nuevos con fianza depositada en Cataluña, por municipio, 2012-2025 (con una ruptura de umbral en 2021).
- **Viviendas turísticas.** INE, medición experimental de VUT a partir de plataformas, por sección, disponible desde 2020-2021. Registro de VUT de la Generalitat Valenciana (GVA), solo para las tres provincias valencianas.
- **IPC de alquiler.** INE, índice nacional.
- **Topes.** Municipios sujetos a la `Ley 11/2020` de Cataluña frente a municipios de control.

La cobertura de la suma de secciones del INE frente al total provincial es de 90,4 % (90,2-90,7 %) [C4]: los totales nacionales de VUT se toman del total publicado y no de la suma por sección.

## Método

### Replicación conceptual de García-López et al. (2020)

El original estima, con variable instrumental y para barrios de Barcelona en 2012-2016, la elasticidad del precio de oferta del alquiler a los anuncios de Airbnb. La réplica propia estima, por MCO con efectos fijos de sección y año y errores agrupados por distrito, la asociación entre VUT por cada cien viviendas y el alquiler SERPAVI en 2021-2024. Es una réplica conceptual, no estricta: cambian los datos, el periodo y el método.

### Topes al alquiler (hipótesis `H3-3`)

Diferencias en diferencias de Callaway y Sant'Anna (2021) con un único momento de tratamiento (2020T4), contrastadas con TWFE y con el estimador de de Chaisemartin y D'Haultfœuille (2020); estudio de eventos, placebos, sensibilidad de Oster y de Cinelli-Hazlett (NO VERIFICADAS) y un multiverso de especificaciones. La evaluación confirmatoria se hizo una sola vez en la muestra sellada, con un diseño anual (media 2021-2022 menos media 2018-2019, excluido 2020).

### Cota de identificación parcial (v3)

Para la contribución máxima de las VUT al alquiler se usan cotas de Manski: sustitución completa de vivienda residencial por turística, traspaso completo al precio y una elasticidad de demanda en una rejilla tomada de la literatura. La cantidad se acota sin supuesto de elasticidad; el precio depende de ella.

### Control de falsos descubrimientos

Todas las especificaciones se registran. Los p de las hipótesis se ajustan por Holm dentro de su familia.

## Resultados

### Lo que no se replica: VUT y alquiler en Barcelona

La estimación propia es -4,2 milésimas de log-punto por punto de VUT/parque (-7,8--0,54 milésimas de log-punto por punto de VUT/parque) [C4], con p ajustado por Holm 26,9 % (valor p). El signo es contrario al del original y el coeficiente no es distinguible de cero tras el ajuste. No se replica el resultado.

La tabla siguiente separa las fuentes de discrepancia (`output/v4/M0/gl_no_replica.md`, `output/v5/A6/nota.md`):

| Fuente | Original | Réplica | ¿Cuantificable? |
|---|---|---|---|
| Datos de alquiler | precio de oferta (flujo) | SERPAVI (stock de contratos) | sí |
| Datos de turismo | anuncios de Airbnb | VUT del INE (unidades) | parcialmente |
| Periodo | 2012-2016 | 2021-2024 | no: el VUT del INE no existe antes |
| Método | variable instrumental | efectos fijos sin instrumento | no: falta el instrumento |

**Atenuación stock-flujo.** En Barcelona, el stock SERPAVI recoge entre el 55,1 % (2022-2024) y el 74,9 % (2015-2020) de la variación acumulada del flujo Incasòl [C4]. Si el coeficiente del original sobre el flujo se trasladara al stock con esa atenuación, el coeficiente esperado en la réplica sería 6,7 milésimas de log-punto por punto de VUT/parque [C4]. La atenuación justifica una magnitud menor, pero no un signo negativo.

**Periodo y método.** No se pueden contrastar con los datos disponibles: la serie de VUT oficial empieza en 2020-2021 y no se dispone del instrumento del original. La discrepancia restante puede proceder del periodo (2021-2024 incluye la salida de la pandemia y la regulación municipal de VUT), del método o de ambos.

**Capa y lectura.** El resultado se presenta como [C4]: no refuta ni confirma el resultado original para España en 2021-2024. Es compatible con que la asociación en el stock sea pequeña en ese periodo.

### Lo que tampoco se replica a escala nacional

En el conjunto de secciones censales con datos, la asociación entre VUT por cada cien viviendas y alquiler SERPAVI es 0,26 milésimas de log-punto por VUT/100 viv. (-0,74-1,3 milésimas de log-punto por VUT/100 viv.) [C4], con p ajustado por Holm 46,7 % (valor p). Es un nulo con intervalo estrecho: la asociación, si existe, es pequeña en la escala del stock.

### Topes: por qué la hipótesis queda fuera de la capa causal

Las estimaciones de entrenamiento de v3 apuntan a rentas más bajas en los municipios sujetos, -5,4 % (-7,1--3,7 %) [C4], y a menos contratos, -4,9 % (-9,9-0,47 %) [C4], este último con un intervalo que incluye el cero. En la muestra sellada, el diseño anual da -0,77 % (-1,4--0,14 %) para la renta y -4,4 % (-6,4--2,3 %) para los contratos [C4].

Estos resultados no se pueden presentar como evidencia causal. La revisión posterior detectó dos problemas en la validación (`docs/v4/decisiones.md`, M0):

1. El cálculo de potencia de v3 usó municipios que luego quedaron en la muestra sellada. La muestra sellada dejó de ser independiente del diseño.
2. La validación por una segunda fuente (SERPAVI) mide el mismo mercado en los mismos municipios; no es una prueba independiente.

En consecuencia, `H3-3` queda fuera de C3 de forma definitiva: sus estimaciones se reportan como [C4], las fichas `V06` y `V07` del verificador dan el veredicto ANALIZADA, NO CONCLUYENTE y el control `check_v5` impide asignar a los topes la capa de efectos. El artículo lo reporta porque una replicación honesta debe incluir los fallos del propio protocolo, no solo los del trabajo replicado.

La literatura publicada sobre la misma regulación (Jofre-Monseny et al., 2023) y la revisión de Kholodilin (2024) son referencias para quien quiera contrastar estas magnitudes; este artículo no pretende arbitrar entre ellas.

### La cota de identificación parcial

Bajo supuestos débiles, las VUT pueden haber desplazado como máximo 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) del stock de alquiler en 2020-2024 [C2]. La cota de precio depende de la elasticidad de la demanda, para la que no hay estimación verificada en España: con la elasticidad mínima de la rejilla sería 8,3 % [C4], y crece sin límite si la elasticidad tiende a cero. Por eso la cota de precio se presenta como función de la elasticidad y queda en [C4]; la cota de cantidad, que no depende de ella, alcanza [C2].

### Discrepancia de medición: registro autonómico frente al INE

En las tres provincias valencianas, el registro de VUT de la GVA cuenta más viviendas que el INE: el cociente es 1,6 veces (1,4-1,8 veces) [C4] en el periodo común y 1,8 veces (1,4-1,9 veces) [C4] con el registro vigente más reciente. Los dos instrumentos miden cosas distintas: el registro recoge viviendas inscritas (activas o no) y el INE viviendas anunciadas en plataformas con criterios de deduplicación. Cualquier estudio que use una u otra fuente debe declarar cuál y reportar la otra como robustez: con la GVA la intensidad turística es mayor y los coeficientes por unidad, menores.

## Robustez

- **Unidad geográfica.** La réplica por sección y por distrito da el mismo signo y una magnitud similar.
- **Multiverso de los topes.** Las especificaciones alternativas de v3 están registradas en los resultados de v3; ninguna cambia la capa, porque la contaminación afecta a la validación y no a la estimación puntual.
- **Fuente de VUT.** Con el registro de la GVA, la intensidad turística aumenta en el cociente indicado; no hay serie anterior a 2020 en ninguna de las dos fuentes.
- **Cobertura.** La suma de secciones del INE cubre 90,4 % (90,2-90,7 %) del total provincial [C4].

## Discusión

### Qué replica, qué no y por qué

| Resultado | ¿Se replica? | Motivo | Capa |
|---|---|---|---|
| VUT y alquiler, Barcelona (García-López et al., 2020) | no | datos (stock frente a flujo, cuantificado), periodo y método (no contrastables) | [C4] |
| VUT y alquiler, secciones de España | nulo | asociación pequeña en el stock | [C4] |
| Topes y renta, Cataluña | no evaluable con el protocolo | validación contaminada | [C4] |
| Topes y contratos, Cataluña | no evaluable con el protocolo | validación contaminada | [C4] |
| Cota de cantidad de VUT | sí, como cota | supuestos de Manski explícitos | [C2] |

### Lecciones para replicaciones con datos administrativos españoles

1. **Stock frente a flujo.** SERPAVI es una fuente valiosa, pero mide contratos vigentes. Un fenómeno que actúa sobre los contratos nuevos aparece atenuado. Toda comparación con estudios basados en precios de oferta debe ajustar por esa atenuación.
2. **Sellado.** Una muestra sellada solo es útil si ningún paso del diseño la toca. El cálculo de potencia es parte del diseño.
3. **Registros que discrepan.** Cuando dos registros públicos difieren en la magnitud del fenómeno, hay que reportar ambos.
4. **Negativos.** Un nulo con intervalo estrecho es informativo; uno con intervalo amplio no lo es. Ambos se publican.

### Qué falta

La serie de anuncios de 2012-2016 por barrio y el instrumento del original permitirían separar periodo y método. Un acceso a contratos nuevos con fianza por sección permitiría estimar con un flujo. Ambos quedan en el backlog del proyecto.

## Conclusión

La replicación conceptual no reproduce el resultado de García-López et al. (2020) en 2021-2024 con datos de stock: el coeficiente es -4,2 milésimas de log-punto por punto de VUT/parque (-7,8--0,54 milésimas de log-punto por punto de VUT/parque) [C4] y no se distingue de cero tras Holm. La diferencia entre stock y flujo justifica una magnitud menor, no un cambio de signo; periodo y método no se pueden contrastar. Los topes al alquiler no se pueden evaluar como efecto con el protocolo aplicado porque la validación quedó contaminada; sus estimaciones se reportan como [C4]. Lo que sí se puede afirmar con supuestos débiles es una cota: como máximo 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) del stock de alquiler desplazado por VUT [C2].

## Referencias

- García-López, M.-À., Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2020). Do short-term rental platforms affect housing markets? Evidence from Airbnb in Barcelona. *Journal of Urban Economics*. [DOI](https://doi.org/10.1016/j.jue.2020.103278). VERIFICADA · Q1.
- Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2023). Effectiveness and supply effects of high-coverage rent control policies. *Regional Science and Urban Economics*. [DOI](https://doi.org/10.1016/j.regsciurbeco.2023.103916). VERIFICADA (Crossref) · Q1.
- Franco, S. F. y Santos, C. D. (2021). The impact of Airbnb on residential property values and rents: Evidence from Portugal. *Regional Science and Urban Economics*. [DOI](https://doi.org/10.1016/j.regsciurbeco.2021.103667). VERIFICADA · Q1.
- Kholodilin, K. A. (2024). Rent control effects through the lens of empirical research. *Journal of Housing Economics*. [DOI](https://doi.org/10.1016/j.jhe.2024.101983). VERIFICADA · Q2.
- Callaway, B. y Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001). VERIFICADA · Q1.
- de Chaisemartin, C. y D'Haultfœuille, X. (2020). Two-way fixed effects estimators with heterogeneous treatment effects. *American Economic Review*. [DOI](https://doi.org/10.1257/aer.20181169). VERIFICADA · Q1.
- Roth, J., Sant'Anna, P. H. C., Bilinski, A. y Poe, J. (2023). What's trending in difference-in-differences? *Journal of Econometrics*. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008). VERIFICADA · Q1.
- Oster, E. (2019) y Cinelli, C. y Hazlett, C. (2020): métodos de sensibilidad usados. NO VERIFICADAS en el registro del proyecto.

## Revistas adecuadas

- *Journal of Comments and Replications in Economics* — cuartil no verificado.
- *Journal of Urban Economics* — Q1 (registrado en `docs/literatura.md`, Scimago).
- *Regional Science and Urban Economics* — Q1 (registrado en `docs/literatura.md`, Scimago).
- *Journal of Housing Economics* — Q2 (registrado en `docs/literatura.md`, Scimago).
