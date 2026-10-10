# M0 · Por qué la réplica de García-López no reproduce el coeficiente (C4, EXPLORATORIO)

Objetivo de GL: 0,035 (EE 0,009) log-puntos por 100 anuncios en un barrio, convertido a 0,01215 por punto de VUT/parque (T). Estimación propia (GL1, sección, FE, cluster distrito): -0.0042 (EE 0.0015, IC95 [-0.0078; -0.0005], p Holm 0.27), NO REPLICADO, con signo contrario. Esta nota separa tres fuentes de discrepancia; no añade estimaciones causales.

## Tres fuentes de discrepancia

| fuente | GL (2020) | réplica propia | cuantificable con lo que hay |
|---|---|---|---|
| datos: alquiler | precio de oferta (Idealista), flujo | SERPAVI: stock de contratos IRPF | sí, vía Incasòl e IPC (abajo) |
| datos: turismo | anuncios de Airbnb | VUT del INE (oleadas, cuenta unidades) | parcial: razón VUT/anuncios 0,11-0,42 en una sola fecha (2025) |
| periodo | 2012-2016 | 2021-2024 (3 diferencias anuales) | SERPAVI sí existe 2011-2024; VUT INE solo desde 2021: no hay solape |
| método | IV (instrumento de GL) | FE sin IV | no: sin instrumento no se puede aislar |
| unidad | barrio/AEB (233 AEB) | sección (815) y distrito (8 con datos) | sí, GL1 frente a GL2: mismo signo, misma magnitud |

## Atenuación de un stock frente a un flujo (Barcelona municipio)

Series: Incasòl renta media de contratos de fianza de Barcelona (flujo; ruptura de umbral >650 a >600 euros en 2021, el salto 2020-2021 se excluye), SERPAVI mediana de €/m² (media simple de los 10 distritos, stock IRPF) e IPC de alquiler nacional (INE). Diferencias de logaritmos anuales; n pequeño, descriptivo.

| tramo | n dif | Δlog Incasòl | Δlog SERPAVI | Δlog IPC | razón acum. SERPAVI/Incasòl | razón acum. SERPAVI/IPC | pendiente SERPAVI~Incasòl |
|---|---|---|---|---|---|---|---|
| 2012-2016 (periodo GL) | 5 | +0.062 | -0.043 | -0.009 | -0.68 | 4.74 | 0.44 |
| 2015-2020 | 6 | +0.338 | +0.253 | +0.038 | 0.75 | 6.73 | 0.16 |
| 2022-2024 (periodo propio, sin salto 2021) | 3 | +0.222 | +0.122 | +0.055 | 0.55 | 2.21 | nan |
| 2015-2024 sin 2021 | 9 | +0.560 | +0.375 | +0.093 | 0.67 | 4.04 | 0.07 |
| 2012-2024 sin 2021 | 12 | +0.470 | +0.292 | +0.090 | 0.62 | 3.25 | 0.46 |

Lectura: en 2022-2024 el stock SERPAVI recoge 55% de la variación acumulada de Incasòl; en 2015-2020, 75%. Si el efecto de GL sobre el flujo fuese T = 0.0121, un stock lo mostraría atenuado en torno a λT = 0.0067 (hasta 0.0645 con el T alto por la razón VUT/anuncios). Observado: -0.0042.
- La atenuación explica una magnitud menor que 0,01215, no un signo negativo: el IC95 propio ([−0,0078; −0,0005]) queda por debajo de cero y de cualquier λT positivo.
- El IC95 de GL2 (distrito) es igual de negativo: la unidad (sección o distrito) no cambia el resultado, con 8 clusters.

## Qué explicación tiene más apoyo
1. Datos (stock frente a flujo): CUANTIFICADA y real, pero solo reduce la magnitud esperada; por sí sola no produce un coeficiente negativo. Apoyo: moderado para la magnitud, nulo para el signo.
2. Método (FE sin IV, 3 diferencias anuales, 8 clusters): no se puede cuantificar sin instrumento. El diagnóstico de v3 ya lo indica: pretendencia sin señal (p=0,71, N=3), placebo de permutación p=0,026 con pocas permutaciones distintas. Un coeficiente negativo con FE es compatible con confusión (los distritos con más cambio de VUT diferían en tendencia de alquiler) y con error de medida del VUT; los datos no permiten distinguirlo.
3. Periodo (2021-2024 con regulación y alquiler de temporada posterior a la pandemia frente a 2012-2016): plausible, no contrastable aquí porque el VUT del INE no existe antes de 2021. València (PARCIAL, signo de GL) y Sevilla (signo contrario) muestran que el signo varía por ciudad, lo que apunta a heterogeneidad además de a un problema de datos.
Conclusión: la discrepancia no se atribuye a una sola fuente. El apoyo cuantificado es que la mezcla stock/IRPF atenúa la magnitud; el signo opuesto queda sin explicar con estos datos y es compatible con identificación débil (sin IV, ventana corta) y con medida distinta del VUT. No se afirma que GL esté refutado ni confirmado para España 2021-2024. Siguiente paso mínimo: serie histórica de VUT/anuncios 2012-2016 y un instrumento (no disponibles en el repo).

Capa: C4 (EXPLORATORIO).
