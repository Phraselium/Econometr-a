# V18 · E1 · Vivienda turística (Barcelona con registro HUT y SERPAVI; otras ciudades no selladas)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa. Clasificación provisional: falta I8 (réplica ciega, B6).
Código: `src/v18/estimacion/e1_turismo.py` (+ `e1_adquisicion.py`, `e1_datos.py`, `e1_diseno.py`, `e1_estim.py`, `e1_mde.py`, `e1_nucleo.py`, `e1_resultados.py`, `e1_salidas.py`); SEED 20261010; sin red en la estimación; 181 s.

## 1. Resumen
- **Lo que supera la estimabilidad (adenda 1.3)**: E1-R3 (estudio de eventos de dosis, 2011-2019) y E1-R4 (Sagrada Família), más la coprincipal E1-P-H3 (H3 de V15 en la muestra V18).
- **E1-R3**: coeficiente por pp de densidad HUT de 2018T2 = **0.0044** (IC95 0.0020; 0.0069; p corregido tras Holm 0.0041). Clase V18: **ASOCIACIÓN**. Razón con la referencia (0,038): 0.12, etiqueta no coherente.
- **E1-R4**: 0.0018 (IC95 de Webb -0.0446; 0.0418; p de Webb 0.8182, tras Holm 1.0000). Clase V18: **SUGESTIVO (efecto nulo acotado)**.
- **E1-P-H3**: -0.0001 por DT intra-sección (IC95 -0.0009; 0.0008; p 0.8769). Cifra de V15: 0,0030, p = 0,931. No se clasifica.
- **NO ESTIMABLES por la regla previa** (se publica el MDE, no el coeficiente): **E1-R1** (solo 18 barrios con un cambio del stock HUT de al menos el 10 %, mínimo 20; MDE80 0.0018), **E1-R2** (primera etapa nula: F efectivo 0.023) y **E1-A1** (MDE80 0.166 frente a 0,038; F efectivo 4.62).
- Consecuencia para B5: la estimación propia designada de E1 es E1-A1 y su respaldo E1-R2; las dos son NO ESTIMABLES por variación, de modo que **E1 no tiene estimación propia estimable** (la adenda 1.9 solo prevé el respaldo cuando la propia es NO ESTIMABLE, y también lo es). Lo dice el informe; no se sustituye por E1-R3 ni E1-R4.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada).

## 2. Datos y sellado
- **Barcelona.** 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador. Las 299 secciones selladas no se usan (ni sus puntos del registro): de los puntos del registro en 2018T4 se asignan a secciones no selladas 8387 de 9581 (87.5 %). Quedan los distritos de Ciutat Vella y l'Eixample, que concentran las licencias.
- **HUT.** El registro del Ajuntament trae coordenadas por licencia; cada punto se asigna a la sección INE que lo contiene (data/manual/v11/bcn_hut_trimestral; cortes de 2018T2 y de 4T de 2018 a 2024). El valor anual es el corte más cercano al 31 de diciembre (regla 1.3): en esos años es el de 4T. La densidad es HUT por 100 viviendas del Censo 2021 por sección. La asignación por punto sustituye a la agregación por barrio de la base (la base solo tiene series por barrio desde 2023): desviación D2.
- **SERPAVI** (VC, €/m²): 764 secciones en 2011 y 766 en 2024; todas las lecturas con `sellado.filtrar` (tope 2024).
- **Otras ciudades.** València (422 de 588 secciones tras el sellado), Sevilla (416 de 522), Málaga (356 de 435) y Alicante (196 de 246). INE-VUT por sección (media anual 2021-2024).
- **Atractivos, ayuntamientos, hospitales y universidades** de OpenStreetMap (extractos regionales de 2026-10-19; atractivos: Barcelona 136, València 51, Sevilla 65, Málaga 58, Alicante 33); **Google Trends** «airbnb» (término) en ES-CT, una descarga; **noches** de Eurostat por NUTS3; correspondencia sección-barrio de Open Data BCN. Todas con la marca `posterior_prereg` y manifiesto en data/raw/v18/_manifest_e1e6.csv.

Auditoría del geocodificado del registro HUT (puntos del fichero, con coordenadas y asignados a secciones no selladas):

| corte | filas_fichero | con_coordenadas | en_secciones_no_selladas |
|---|---|---|---|
| 2018T2 | 9603 | 9603 | 8409 |
| 2018T4 | 9581 | 9581 | 8387 |
| 2019T4 | 9572 | 9572 | 8499 |
| 2020T4 | 9536 | 9536 | 8482 |
| 2021T4 | 9403 | 9403 | 8367 |
| 2022T4 | 9411 | 9411 | 8387 |
| 2023T4 | 14120 | 9923 | 8837 |
| 2024T4 | 10417 | 10417 | 9147 |

## 3. Estimabilidad (adenda 1.3), calculada antes de mirar ningún coeficiente
MDE80: R = 2.000 réplicas, SEED 20261010; el ruido se remuestrea por barrio de los residuos del periodo previo de cada diseño («ya visto»: V15 y V16 no publican la σ residual de ln SERPAVI por sección) con la variación real del tratamiento; el valor crítico es el mayor entre el nominal t(G−1) y el empírico del propio Monte Carlo (corrección por tamaño). En los diseños con IV, el MDE es el del contraste de Anderson-Rubin por cluster.

| id | unidades | obs | clusters | mínimo de datos | MDE80 | umbral | decisión |
|---|---|---|---|---|---|---|---|
| E1-R1 | 766 | 5360 | 47 | barrios con cambio >= 10 % del stock HUT 2018-2024: 18 (mínimo 20) | 0.0018 | 0.0380 | NO ESTIMABLE |
| E1-R2 | 766 | 5360 | 47 | primera etapa y instrumento reales; F efectivo publicado (no es un criterio de estimabilidad) | — | 0.0380 | NO ESTIMABLE |
| E1-A1 | 1316 | 5157 | 36 | primera etapa y instrumento reales; F efectivo publicado (no es un criterio de estimabilidad) | 0.1656 | 0.0380 | NO ESTIMABLE |
| E1-R3 | 766 | 6884 | 47 | dosis de 2018T2 con variación entre secciones y barrios | 0.0060 | 0.0760 | estimable |
| E1-R4 | 77 | 693 | 6 | radio 22/25 y anillo 55/70 secciones no selladas (mínimo 75 % en cada uno) | 0.0407 | 0.1000 | estimable |
| E1-R2-v5 | 766 | 2290 | 47 | primera etapa y instrumento reales; F efectivo publicado (no es un criterio de estimabilidad) | 0.0880 | 0.0380 | NO ESTIMABLE |

Primera etapa de las especificaciones con instrumento y de sus variantes, **sin el resultado** (ln SERPAVI sustituido por 0): F efectivo de Montiel Olea-Pflueger y coeficiente.

| id | n | G | F_efectivo | pi |
|---|---|---|---|---|
| E1-R2 | 5360 | 47 | 0.02 | -0.0003 |
| E1-R2-v1 | 5360 | 47 | 0.00 | -0.0002 |
| E1-R2-v2 | 3829 | 47 | 0.01 | -0.0015 |
| E1-R2-v3 | 5360 | 47 | 0.11 | -0.0006 |
| E1-R2-v4 | 5360 | 47 | 0.07 | -0.0005 |
| E1-R2-v5 | 2290 | 47 | 16.82 | -0.2279 |
| E1-R2-v6 | 5360 | 47 | 0.01 | 0.0002 |
| E1-R2-v8 | 5360 | 47 | 0.01 | -0.0001 |
| E1-R2 [subperiodo 2018-2019] | 1531 | 47 | 0.00 | -0.0011 |
| E1-R2 [subperiodo 2020-2021] | 1531 | 47 | 1.62 | -0.0023 |
| E1-R2 [subperiodo 2022-2024] | 2298 | 47 | 0.55 | -0.0180 |
| E1-A1 | 5157 | 36 | 4.62 | 0.0495 |
| E1-A1-v1 | 3898 | 36 | 4.50 | 0.0850 |
| E1-A1-v2 | 8204 | 43 | 0.15 | 0.0094 |
| E1-A1-v4 | 5157 | 36 | 4.38 | 0.0577 |
| E1-A1-v5 | 5161 | 36 | 4.84 | 0.2540 |
| E1-A1-v6 | 1664 | 14 | 4.73 | -0.0494 |
| E1-A1-v7 | 1486 | 8 | 4.17 | 0.4368 |
| E1-A1-v8 | 1275 | 8 | 3.06 | 0.0502 |
| E1-A1-v9 | 732 | 6 | 52.86 | 0.0242 |
| E1-A1-v10 | 5101 | 35 | 4.34 | 0.0330 |
| E1-A1-v11 | 5157 | 36 | 6.29 | 0.0510 |
| E1-R2 [placebo hospitales] | 5360 | 47 | 0.57 | 0.0010 |
| E1-A1 [placebo hospitales] | 5157 | 36 | 0.01 | 0.0015 |
| E1-R2 [placebo universidades] | 5360 | 47 | 0.01 | 0.0001 |
| E1-A1 [placebo universidades] | 5157 | 36 | 5.26 | -0.0369 |

- **E1-R1 no alcanza el mínimo de datos** (18 barrios frente a 20): el stock HUT de los barrios no sellados casi no cambia entre 2018 y 2024 (moratoria desde 2014 y PEUAT desde 2017). Es una regla de la adenda, no una decisión sobre el coeficiente; de haberse contado 20 barrios, el MDE80 (0.0018) sí habría estado por debajo del umbral. Sus 10 variantes no se estiman.
- **E1-R2-v5 (suplementaria, solo diseño)**: la variante con el % INE-VUT como endógena (2022-2024) tiene F efectivo 16.82, coeficiente de la primera etapa -0.228 y MDE80 0.0880 frente a 0,038. Una variante solo se estima si su principal es estimable (anexo A); el dato queda para la revisión.
- **Placebos del instrumento (solo primera etapa)**: con la proximidad a hospitales y a universidades × el mismo «cuándo», el F efectivo es 0.57 y 0.01 en E1-R2 (instrumento real: 0.02) y 0.01 y 5.26 en E1-A1 (real: 4.62). La forma reducida sobre el resultado no se calcula (no se estima el resultado).
- **E1-R2 y E1-A1**: la proximidad × Trends (o × noches), con efectos de sección y de año (o de municipio × año) y la distancia al centro × año, casi no predice la exposición; el AR no alcanza el 80 % de potencia con efectos de magnitud razonable. Sus variantes se documentan solo en la primera etapa.

## 4. Resultados de las especificaciones estimadas
| id | n_obs | n_unidades | G | coef | ic95_lo | ic95_hi | p_cr1 | p_webb | p_i7 | p_holm | clase |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1-R3 | 6884 | 766 | 47 | 0.0044 | 0.0020 | 0.0069 | 0.0007 | 0.0102 | 0.0010 | 0.0041 | ASOCIACIÓN |
| E1-R4 | 693 | 77 | 6 | 0.0018 | -0.0446 | 0.0418 | 0.8259 | 0.8182 | 0.8182 | 1.0000 | SUGESTIVO (efecto nulo acotado) |
| E1-P-H3 | 39951 | 10004 | 1208 | -0.0001 | -0.0009 | 0.0008 | 0.8769 | — | 0.8769 | 1.0000 | no se clasifica |

p_cr1 = CR1 con t(G−1) por barrio (E1-R3) o por municipio (E1-P-H3); en E1-R4 la inferencia principal es Webb. p_i7 = p con el valor crítico corregido por el tamaño del Monte Carlo de cada diseño (E1-R3: 0.079 con CR1; E1-R4: 0.060 con Webb). Holm sobre la familia E1 estimada (m = 4: E1-R3, E1-R4, E1-P-H3, E1-R3-v3); E1-R1, R2 y A1 salen antes de ajustar; P-D2 y P-Q2b no se han estimado (desviación D7). Las coprincipales P no se clasifican.

Coeficiente de E1-R3 por desviación típica de la dosis (1.999 pp): 0.0089 (EE 0.0024); por pp: 0.0044. Inferencias alternativas: Webb 9.999 p = 0.0102; EE de Conley a 1 km 0.00252 y a 2 km 0.00220 (CR1: 0.00242; el Monte Carlo de V18 mide para Conley en secciones a 1 km un tamaño de 0,070, «con valor crítico corregido», apto solo si el alcance de la dependencia no supera el corte); Driscoll-Kraay no se usa («no fiable» en su Monte Carlo).

## 5. Pruebas B4
**E1-R3 (estudio de eventos de dosis; base 2013; coeficientes por DT de la dosis):**

| año | coef por DT de la dosis | ee |
|---|---|---|
| 2011 | -0.0073 | 0.0024 |
| 2012 | -0.0053 | 0.0020 |
| 2014 | 0.0058 | 0.0018 |
| 2015 | 0.0057 | 0.0022 |
| 2016 | 0.0074 | 0.0024 |
| 2017 | 0.0106 | 0.0033 |
| 2018 | 0.0117 | 0.0030 |
| 2019 | 0.0120 | 0.0028 |

- Adelantos (2011 y 2012, contraste conjunto): p = 0.008. Pendiente lineal previa detectable al 80 % (Roth, 2022): 0.0037 por año; sesgo que implicaría en la ventana posterior: 0.0131, frente a la mitad de |referencia| por DT (0.0380): superado. El preperiodo es de solo dos años.
- Placebo de fecha (adopción falsa en 2012, ventana 2011-2013): 0.0047, p = 0.054.
- Tendencia por distancia al centro de 2011-2013 (diagnóstico de la adenda R-15): coeficiente -0.0078, p = 0.003; la variante con distancia × año (v3) pasa a coprincipal.
- Honest DiD (Rambachan-Roth, magnitudes relativas). Según el Monte Carlo de V18 solo M̄ = 0 es apto; con M̄ = 0,5 y 1 es válido pero conservador y no decide (desviación D5):

| M̄ | IC95 | excluye 0 | lectura |
|---|---|---|---|
| 0.0 | (0.0037; 0.0140) | True | apto (M̄ = 0) |
| 0.5 | (-0.0084; 0.0252) | False | válido pero conservador; informativo |
| 1.0 | (-0.0234; 0.0400) | False | válido pero conservador; informativo |

- I de Moran de los residuos medios por sección (5 vecinos): I = -0.036 (E[I] = -0.001), p unilateral 0.965.
- Medida alternativa del resultado (por pp): €/mes de vivienda colectiva 0.0042 (IC95 0.0009; 0.0074); vivienda unifamiliar 0.0366; sin atípicos (1 % superior de dosis y 1 % extremo de la variación del resultado; 16 secciones) 0.0049. Fianzas por barrio: no existen en abierto (desviación D6).
- Placebo de resultado (población de 65 años o más por sección): no aplicable a 2011-2019 (existe solo desde 2021; adenda R-15).

**E1-R4 (Sagrada Família; coeficientes del radio de 500 m frente al anillo; base 2013):**

| año | coef | ee |
|---|---|---|
| 2011 | 0.0087 | 0.0099 |
| 2012 | -0.0044 | 0.0092 |
| 2014 | 0.0058 | 0.0027 |
| 2015 | 0.0033 | 0.0076 |
| 2016 | 0.0035 | 0.0088 |
| 2017 | -0.0050 | 0.0091 |
| 2018 | 0.0013 | 0.0106 |
| 2019 | 0.0016 | 0.0108 |

- Equivalencia (TOST, δ = 0,05): el IC95 de Webb (-0.0446; 0.0418) queda dentro de ±0,05, de modo que el IC90 también; con solo 6 clusters (3 con tratadas) fuera del rango del Monte Carlo de V18, se rotula con esa advertencia.
- Adelantos (2011 y 2012): p = 0.121; pendiente detectable 0.0129; sesgo implicado 0.0452 (umbral δ = 0,05). Placebo de fecha (adopción falsa en 2012): -0.0109, p = 0.195.
- Honest DiD:

| M̄ | IC95 | excluye 0 | lectura |
|---|---|---|---|
| 0.0 | (-0.0132; 0.0167) | False | apto (M̄ = 0) |
| 0.5 | (-0.0416; 0.0436) | False | válido pero conservador; informativo |
| 1.0 | (-0.0766; 0.0790) | False | válido pero conservador; informativo |

- Geometría: radio 22 de 25 secciones no selladas (0.88) y anillo 55 de 70 (0.79): se cumple el 75 % de la adenda 1.5. 6 barrios, 3 con tratadas.
- Medida alternativa: €/mes 0.0203; vivienda unifamiliar —. Moran de los residuos: I = 0.102, p unilateral 0.049.

## 6. Variantes enumeradas (anexo A)
Benjamini-Yekutieli al 10 % dentro de cada identificador. E1-R3 y E1-R4 con CR1 (E1-R4-v2, con 1.999 réplicas de Webb). Las variantes de E1-R1, E1-R2 y E1-A1 no se estiman (principal NO ESTIMABLE). E1-R3-v3 figura además como coprincipal en la familia de Holm cuando la tendencia por distancia de 2011-2013 es significativa al 10 % (adenda R-15); el q de cada variante es el de Benjamini-Yekutieli con su p de CR1 (E1-R4-v2: con su p de Webb).

| id | resultado | n_obs | coef | ic95_lo | ic95_hi | p_cr1 | p_webb | q_by |
|---|---|---|---|---|---|---|---|---|
| E1-R3-v1 | [V] base 2012 | 6884 | 0.0071 | 0.0041 | 0.0100 | 0.0000 | — | 0.0002 |
| E1-R3-v2 | [E] dosis binaria del decil superior | 6884 | 0.0055 | 0.0003 | 0.0107 | 0.0388 | — | 0.1107 |
| E1-R3-v3 | [C] distancia × año | 6884 | 0.0023 | -0.0003 | 0.0049 | 0.0834 | — | 0.1905 |
| E1-R3-v4 | [U] barrio como unidad | 416 | 0.0071 | 0.0019 | 0.0122 | 0.0079 | — | 0.0302 |
| E1-R3-v5 | [U] sin el 1 % superior | 6812 | 0.0047 | 0.0017 | 0.0076 | 0.0025 | — | 0.0143 |
| E1-R4-v1 | [C] resto de Barcelona como control | 6884 | -0.0020 | -0.0138 | 0.0098 | 0.7302 | — | 1.0000 |
| E1-R4-v2 | [E] radios de 300 m y 300-800 m | 432 | 0.0241 | 0.0122 | 0.0361 | 0.0077 | 0.8000 | 1.0000 |

## 7. Clasificación (I1-I8 revisados)
- **E1-R3: ASOCIACIÓN.** Fallos decisivos: pretendencias p = 0.008 < 0,01. Pruebas débiles: inferencia con valor crítico corregido por tamaño (tamaño del Monte Carlo de este diseño: 0.079); placebo de fecha p = 0.054. Topes: tope de la especificación: SUGESTIVO (sin instrumento; la exogeneidad estricta no se contrasta).
- **E1-R4: SUGESTIVO (efecto nulo acotado).** Fallos decisivos: —. Pruebas débiles: solo 6 clusters (barrios), 3 con tratadas: fuera del rango del Monte Carlo de V18 (G = 8, 4 tratados); mismo signo en 50% de las variantes enumeradas (< 80 %). Topes: tope de la especificación: SUGESTIVO (un solo grupo tratado: la Sagrada Família).
- E1-P-H3, coprincipal: no se clasifica; su cifra publicada (V15) se muestra al lado.
- I6 como etiqueta: Segú (2018), IV lineal, por pp de densidad: 0,038 (0,012), ficha NO VERIFICADA (adenda, anexo B). E1-R3: razón 0.12, no coherente. La magnitud difiere de la referencia por la medida (licencias HUT, no anuncios activos), por SERPAVI (contratos vigentes declarados: stock, que diluye el cambio) y por el periodo (2014-2019, con la dosis medida en 2018T2). No interviene en la clase ni en B5.
- I8 pendiente en todas (replicador-ciego). En las dos especificaciones estimadas la clase describe el diseño; el lenguaje es el de una asociación estimada.

## 8. Comparación con lo ya visto en el proyecto
- H3 (V15): 0,0030 por DT intra-sección, p = 0,931 (2021-2024, toda España en entrenamiento). E1-P-H3 lo repite en la muestra V18: -0.0001 (p 0.877).
- Q2a/Q2c (V16), V9-D2 (Cataluña) y V9-D3 (València): asociaciones no concluyentes o con pretendencias rechazadas; E1-R3 y E1-R4 no sustituyen a ninguna de esas lecturas (periodos y unidades distintos) y no promueven de capa.
- V17 B4 y el informe integral (III.4): «turísticos: no concluyente». Una estimación NO CONCLUYENTE o SUGESTIVO no contradice esa conclusión; ninguna es IDENTIFICADO ni NO CONCLUYENTE con equivalencia (parada G3 no activada).

## 9. Desviaciones (detalle y fechas en docs/v18/desviaciones_e1_e6.md)
D1 Overpass no accesible: OSM por extractos regionales. D2 HUT por punto en lugar de por barrio. D3 Censo 2021 sin clave en sellado_v18.json. D4 INE-VUT porcentaje y plazas heredan el tope de viviendas turísticas. D5 Honest DiD solo informativo. D6 fianzas por barrio inexistentes. D7 coprincipales P-D2 y P-Q2b no estimadas. D8 E1-A2 no estimada. D9 definición operativa del instrumento y del «primer/último valor anual».

## 10. Limitaciones y datos que lo resolverían
- El stock de licencias HUT casi no varía tras 2018: el diseño de E1 con licencias no tiene primera etapa. La exposición con variación es el anuncio activo (InsideAirbnb, histórico por la Archived Data Request; tareas_autor, punto 14), no la licencia.
- SERPAVI mide contratos vigentes declarados (stock), no anuncios; no se contrasta la composición a escala de sección (el recuento de contratos por sección tiene el tope sellado entero).
- El preperiodo de E1-R3 y E1-R4 es de dos años (2011-2012): la potencia para detectar tendencias previas es baja.
- Precio de compra por barrio (X1): serie de compraventa de Open Data BCN o microdatos de portales (tareas_autor, punto 2).
