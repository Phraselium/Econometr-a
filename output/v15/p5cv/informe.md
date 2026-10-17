# V15-A · E4: exposición turística con periodo previo (Cataluña y Comunitat Valenciana)

Capa C4 (exploratoria, entrenamiento; asociación, sin lenguaje causal). Estudio de eventos de dosis continua con coeficientes **puntuales**: no hay inferencia APTA para el diseño y Honest DiD es NO APTO (docs/v15/validacion_montecarlo.md). `pendiente_sellada`: no aplica a E4 (exploratoria, sin evaluación sellada pre-registrada), se deja `true` por la regla común. BY lo aplica el orquestador (p = null).

## Diseño (DV15-A, A6)
- Dosis: log(1 + viviendas de uso turístico) en 2017, estandarizada (IDESCAT n y plazas en Cataluña; registro GVA reconstruido en la Comunitat Valenciana, fechados base/−12/+12 meses). Resultado: log de la renta anual de Incasòl (media ponderada por contratos) en Cataluña; log de la mediana SERPAVI (stock de contratos) VC o VU en la Comunitat Valenciana. Efectos fijos de municipio y de año; referencia 2017; paneles equilibrados en la ventana. Ventanas 2015-2024 y 2015-2019.
- La exposición del registro GVA es reconstruida a partir de las altas y bajas fechadas del registro actual: no recoge las viviendas ya dadas de baja, y los municipios sin vivienda inscrita hoy se tratan como dosis 0. Se reporta como C4 y nunca como principal.
- 16 especificaciones registradas (≤ 24 declaradas). Pretendencias: coeficientes de 2015 y 2016; lectura puntual declarada «compatible» si max|coef previo| ≤ 0,5 × |media de los coeficientes posteriores| (no es un test).

## Resultados
- **Cataluña, IDESCAT n, 2015-2024** (380 municipios): coeficientes previos 0,00 % (2015) y 0,75 % (2016) por DT de dosis; media posterior (2018-2024) 0,71 %; 2024: 0,83 %. Lectura puntual: NO compatible.
- **Comunitat Valenciana, SERPAVI VC, fechado base, 2015-2024** (207 municipios): previos 0,30 % y -0,48 %; media posterior 0,17 %. Lectura: NO compatible.
- **Conjunto de 16:** media posterior entre -0,72 % y 1,01 % por DT; positiva en 10; compatibles puntualmente con la regla declarada: 6; no compatibles: 10.

| región | medida | fechado | ventana | N mun. | previos 2015 / 2016 (%) | media post (%) | compatible | sin 1 % sup. (media post) | sin grandes ciudades (media post) |
|---|---|---|---|---|---|---|---|---|---|
| Cataluña | hut_n | n/a | 2015-2024 | 380 | 0,00 / 0,75 | 0,71 | no | 0,75 | 0,73 |
| Cataluña | hut_n | n/a | 2015-2019 | 402 | 0,25 / 0,87 | 0,96 | no | 0,97 | 0,97 |
| Cataluña | hut_plazas | n/a | 2015-2024 | 380 | 0,04 / 0,88 | 0,69 | no | 0,73 | 0,71 |
| Cataluña | hut_plazas | n/a | 2015-2019 | 402 | 0,29 / 1,03 | 1,01 | no | 1,01 | 1,01 |
| Comunitat Valenciana | SERPAVI VC | base_dic2017 | 2015-2024 | 207 | 0,30 / -0,48 | 0,17 | no | 0,12 | 0,07 |
| Comunitat Valenciana | SERPAVI VC | base_dic2017 | 2015-2019 | 207 | 0,30 / -0,48 | 0,20 | no | 0,15 | 0,15 |
| Comunitat Valenciana | SERPAVI VC | alta_12m_antes_dic2018 | 2015-2024 | 207 | 0,21 / -0,53 | 0,32 | no | 0,29 | 0,22 |
| Comunitat Valenciana | SERPAVI VC | alta_12m_antes_dic2018 | 2015-2019 | 207 | 0,21 / -0,53 | 0,30 | no | 0,25 | 0,25 |
| Comunitat Valenciana | SERPAVI VC | alta_12m_despues_dic2016 | 2015-2024 | 207 | 0,34 / -0,30 | 0,12 | no | 0,19 | 0,02 |
| Comunitat Valenciana | SERPAVI VC | alta_12m_despues_dic2016 | 2015-2019 | 207 | 0,34 / -0,30 | 0,17 | no | 0,15 | 0,12 |
| Comunitat Valenciana | SERPAVI VU | base_dic2017 | 2015-2024 | 187 | 0,04 / -0,05 | -0,50 | sí | -0,52 | -0,61 |
| Comunitat Valenciana | SERPAVI VU | base_dic2017 | 2015-2019 | 187 | 0,04 / -0,05 | -0,66 | sí | -0,67 | -0,71 |
| Comunitat Valenciana | SERPAVI VU | alta_12m_antes_dic2018 | 2015-2024 | 187 | -0,07 / -0,15 | -0,44 | sí | -0,45 | -0,55 |
| Comunitat Valenciana | SERPAVI VU | alta_12m_antes_dic2018 | 2015-2019 | 187 | -0,07 / -0,15 | -0,72 | sí | -0,73 | -0,76 |
| Comunitat Valenciana | SERPAVI VU | alta_12m_despues_dic2016 | 2015-2024 | 187 | -0,16 / -0,06 | -0,46 | sí | -0,29 | -0,56 |
| Comunitat Valenciana | SERPAVI VU | alta_12m_despues_dic2016 | 2015-2019 | 187 | -0,16 / -0,06 | -0,63 | sí | -0,53 | -0,67 |

## Lectura frente a lo ya publicado
- V9 estimó una dosis-respuesta en Cataluña con pretendencias rechazadas (V9-D2, C4). Aquí se repite con IDESCAT y otra referencia temporal; ninguna cifra es confirmatoria y ninguna contradice con dirección una conclusión de la 1.0 («turísticos: no concluyente»).
- Pruebas no evaluadas por herramienta NO APTA: inferencia del estudio de eventos, Honest DiD, potencia de Roth. Oster, Cinelli-Hazlett y E-values no se calculan sin error típico válido. Raíces unitarias y cointegración no aplican (T ≤ 10 por municipio, estudio de eventos).

## Fichas reproducibles
Todas: `python3 src/v15/p5cv_exposicion.py` (SEED 20261010; no hay aleatoriedad); cifras en output/v15/p5cv/estimacion_bruta.json y registro.csv.
- <a id="ficha-e4-cat"></a>**ficha-e4-cat:** `cataluna[medida=hut_n, ventana=2015-2024].media_post` = media de los coeficientes dosis × año de 2018 a 2024 (×100) del modelo log(renta Incasòl) ~ z·1[año] + FE de municipio y de año.
- <a id="ficha-e4-pre"></a>**ficha-e4-pre:** `cataluna[...].coef_pct_por_DT[2015, 2016]`.
- <a id="ficha-e4-cv"></a>**ficha-e4-cv:** `valenciana[medida=SERPAVI VC, fechado=base_dic2017, ventana=2015-2024].media_post`.
- <a id="ficha-e4-resumen"></a>**ficha-e4-resumen:** `resumen`.
