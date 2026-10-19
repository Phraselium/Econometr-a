Análisis a posteriori (V17). Ficha de auditoría de la fila «turisticos» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-TUR-* en output/v17/auditoria/demanda_precios_hechos.json.

# «La culpa es de los pisos turísticos»

## 1. Texto auditado

> «La culpa es de los pisos turísticos»: a escala nacional no puede ser la causa principal (≤ 2,7 % del parque de alquiler). En barrios concretos es posible, pero no está demostrado en España.

Son tres afirmaciones: (a) un dato, «≤ 2,7 % del parque de alquiler»; (b) una conclusión nacional, «no puede ser la causa principal»; (c) una conclusión local, «no está demostrado en España».

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- La media nacional es baja frente a la subida. Las viviendas turísticas (INE, estadística experimental) son el 1,5 % de todas las viviendas familiares en agosto de 2024: 403.267 de 26,6 millones. El Banco de España da la misma cifra para 2025 (IA2025, p. 150).
- Con los coeficientes de Garcia-López et al. (2020), esa densidad es compatible con un alquiler entre un 1,0 % y un 2,1 % más alto que con densidad cero (V17-AUD-DP-TUR-GL-ALQ-NAC; ilustración, no estimación). En 2015-2024 el alquiler de los contratos vigentes subió entre un 10,9 % y un 22,9 % (IPC e IPVA; informe integral, resumen).
- Los propios autores dicen que el efecto «cannot explain the bulk» de la subida de Barcelona en 2012-2016 (versión de trabajo, conclusiones).
- Nuestra H3 (V15) no ve asociación dentro de la sección: 0,003 % por DT, con p = 0,93 y un tamaño real del 9,6 % (lectura convencional publicable).

**En contra.**
- **El 2,7 % no es el peso de los pisos turísticos.** Es el AUMENTO de 2020M08 a 2024M08 (81.771 viviendas) sobre el parque de alquiler del Censo 2021 (B4-v3-vut-cantidad; output/v3/PB/cotas.json). El peso del stock es:
  - 13,5 % del parque de alquiler en agosto de 2024, o 11,9 % con el denominador de la ECV (V17-AUD-DP-TUR-NAC-STOCK-2024M08);
  - 11,8 % en febrero de 2024 (V17-AUD-DP-TUR-NAC-STOCK-2024M02);
  - 11,5 % en mayo de 2026.
- **Ventana y base de la cota.** La cota empieza en el mínimo de la pandemia, cubre solo cuatro años y deja fuera el auge de 2014-2019, que la estadística del INE no cubre. Entre 2024M08 y 2026M05 el stock cae en 62.266 viviendas.
- **La distribución local es muy desigual.** En las secciones censales sin muestra sellada, la mediana de viviendas turísticas sobre el alquiler es del 3,1 %, el P90 del 33,9 % y el P99 del 168,8 % (24.201 secciones; V17-AUD-DP-TUR-SEC-*). El 12,6 % del parque de alquiler está en secciones donde las turísticas superan la cuarta parte del alquiler.
- **Hay una estimación causal publicada en España.** Garcia-López et al. (2020, JUE) usan un instrumento de tipo shift-share y estudios de evento con 220 áreas de Barcelona. Estiman +7 % de alquiler y +17-19 % de precio de transacción en el decil alto de actividad de Airbnb.
- **Nuestra señal provincial.** Q2a (V16) da 0,013 Δlog del IPC de alquiler por DT del log de la exposición: p = 0,0004, Holm 0,0008, tamaño real 14,2 % (publicable por poco, por debajo del 15 %). Es una asociación, no un efecto, pero no es «sin señal».

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_demanda_precios.py.
- Determinista, sin red, SEED 20261010.
- Solo usa filas con muestra_sellada_v6 = False.
- Cruces por código INE de sección y de municipio.
- Test: tests/v17/test_f3_demanda_precios.py.

**3.1 Denominador y universo de las tres cifras.**

| Cifra | Numerador | Denominador | Universo | Qué mide |
|---|---|---|---|---|
| 2,7 % (2,4-2,7) de la 1.0 | aumento 2020M08-2024M08 (81.771) | alquiler, Censo 2021 (2.978.090) o ECV × ECP (3.374.940) | España | flujo: cota de sustitución uno a uno |
| 11,8 % (BdE DO 2432, cuadro A.3) | stock feb. 2024 (351.389) | viviendas principales en alquiler, Censo 2021 | «Total España» por sección | stock; el proyecto lo reproduce (11,80 %) |
| «cerca del 10 %» (BdE IA2025, p. 150) | unas 355.000 (media 2025) | mercado del alquiler (denominador no publicado) | España | stock |
| 10,8 % (BdE IA2025, diapositiva 40) | no localizado | no localizado | no localizado | **no se encontró en el original**: el capítulo da «cerca del 10 %». No se usa |

Conclusión: el denominador del 2,7 % es correcto y es el mismo que el del Banco de España. Lo que cambia es el numerador: flujo de cuatro años frente a stock. El 2,7 % publicado es correcto con su definición. La paráfrasis «≤ 2,7 % del parque de alquiler» es falsa si se lee como peso del parque, y así se lee.

**3.2 Distribución local (2024M08; viviendas turísticas del INE sobre el alquiler del Censo 2021).**

| Ámbito | P50 | P90 | P99 | N |
|---|---|---|---|---|
| Secciones (sin ponderar) | 3,1 % | 33,9 % | 168,8 % | 24.201 |
| Secciones (ponderadas por el alquiler) | 2,9 % | 33,3 % | 192,6 % | 24.201 |
| Secciones, mayo de 2026 | 2,3 % | 30,9 % | 155,2 % | — |
| Secciones, AUMENTO 2021M08-2024M08 sobre el alquiler | 0,0 % | 13,8 % | 67,2 % | — |
| Municipios (todos) | 6,2 % | 47,1 % | 180,6 % | 5.454 |
| Municipios con 5.000 viviendas en alquiler o más | 4,7 % | 22,5 % | 78,0 % | 61 |
| Inside Airbnb, viviendas completas (sep. 2026; solo áreas rastreadas) | 4,3 % | 25,9 % | 93,7 % | 1.849 |

- **Sobre el total de viviendas de la sección:** P50 0,29 %, P90 2,5 % y P99 10,2 % (V17-AUD-DP-TUR-SEC-VIV-P90).
- **Ciudades sin muestra sellada:** Barcelona 4,7 %, València 14,3 %, Sevilla 18,4 % y Málaga 29,4 % del alquiler.
- **Máximos entre los municipios grandes:** Mijas 78 %, Marbella 78 % y Torrevieja 71 %.
- **Lectura.** Donde la proporción supera el 100 %, las turísticas no pueden haber salido todas del alquiler residencial: vienen sobre todo de segundas residencias, en la costa y en municipios pequeños. El cociente sobre el alquiler sobreestima el desplazamiento ahí. Por eso la escala de Garcia-López et al. (anuncios sobre viviendas) es la que se usa para el precio.

**3.3 Traslación a precio (ilustración con parámetros ajenos; juicio experto).** Garcia-López et al., versión de trabajo, cuadro 4 y sección 3.4:
- en la especificación de densidad, 0,68 % de alquiler por punto de anuncios sobre viviendas (no significativo, e.e. 0,5);
- en el decil alto, con ≈ 5 % de las viviendas anunciadas, el +7 % implica ≈ 1,4 % por punto.

| Densidad (turísticas sobre viviendas) | Alquiler compatible |
|---|---|
| Media nacional, 1,5 % | +1,0 a +2,1 % |
| Sección P50, 0,29 % | +0,2 a +0,4 % |
| Sección P90, 2,5 % | +1,7 a +3,5 % |
| Sección P99, 10,2 % | +7,0 a +14,3 % |

- **Límites del P99.** Fuera del soporte del estudio (≈ 5 %): es extrapolación lineal.
- **Precio de transacción.** El coeficiente es unas 3-6 veces el del alquiler (3,9 % por punto en la especificación de densidad).
- **Límites generales.**
  - Barcelona en 2012-2016, con alquileres anunciados.
  - La validez externa no se ha comprobado.
  - Es el nivel acumulado frente a densidad cero, no la variación de un periodo.

**3.4 Comparación con H3 y Q2.**
- **H3 frente a Garcia-López et al.** Con la DT intra-sección de H3 (0,61 pp), los coeficientes de Garcia-López et al. implicarían 0,42-0,86 % por DT. H3 da 0,003 % (EMD del 80 % = 0,097 %). La diferencia es de dos órdenes de magnitud, y H3 tenía potencia para ver un efecto de ese tamaño.
- **Por qué pueden diferir.** H3 mide el alquiler de los contratos VIGENTES (SERPAVI, datos tributarios), que solo se ajusta al renovar. Garcia-López et al. miden anuncios nuevos. Además, H3 cubre 2021-2024, con una exposición ya regulada en las grandes ciudades. Son medidas y periodos distintos, no una refutación.
- **Q2a** (provincias) tiene el signo de Garcia-López et al. y p convencional válido.
- **Q2c** (IPVA municipal) cambia de signo y no es concluyente.

**3.5 Banco de España y otros estudios españoles.**
- IA2023 (p. 255) cita a Garcia-López et al. y da cerca del 10 % del mercado de alquiler.
- DO 2432 es descriptivo: atribuye la limitación de la oferta de alquiler, en parte, a usos alternativos (turístico, habitaciones, temporada).
- No hay estimación propia del Banco de España.
- Estudios españoles sin diseño causal comparable: MESVAL 2022 (València, corte transversal), Casanova 2019 (Madrid, sin significación con dependencia espacial) y Mozo Carollo et al. 2023 (San Sebastián). Fichas en docs/v15/literatura/P5_pisos_turisticos.md.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), JUE 119, 103278, DOI 10.1016/j.jue.2020.103278 | VERIFICADA (Crossref; cuartil no verificado) | texto parcial de la versión de trabajo (MPRA 96131): secciones 1, 3.4 y 5, cuadro 4 y conclusiones, leídos en V17; de la versión publicada, solo el resumen |
| Barron, Kung y Proserpio (2021), Marketing Science, DOI 10.1287/mksc.2020.1227 | VERIFICADA | resumen (elasticidad 0,018 en alquiler) |
| Franco y Santos (2021), RSUE 88, DOI 10.1016/j.regsciurbeco.2021.103667 | VERIFICADA | resumen (Portugal: +3,7 % de precio por punto de cuota) |
| Koster, van Ommeren y Volkhausen (2021), JUE 124, DOI 10.1016/j.jue.2021.103356 | VERIFICADA | resumen |
| Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432, DOI 10.53479/37872 | VERIFICADA (Crossref, consulta 2026-10-19) | parcial, incluido el cuadro A.3 (p. 57) |
| Banco de España, Informe Anual 2023 (cap. 4) y 2025 (cap. 2) | NO VERIFICADA (sin DOI) | páginas citadas (docs/v17/referencias/bde_informes.md) |

## 5. Veredicto

**Engañosa.**
- (a) El dato está mal descrito: el peso del stock es del 11,8-13,5 % del parque de alquiler, no ≤ 2,7 %. El 2,7 % es el aumento de un periodo corto que empieza en la pandemia.
- (b) La conclusión nacional se sostiene con matices, pero por otra razón. Con la densidad media nacional (1,5 % de las viviendas) y las elasticidades publicadas, el efecto compatible es pequeño frente a la subida. «No puede ser» es más fuerte que lo que la propia 1.0 permite: su verificador dice que no se puede afirmar ni negar el papel principal.
- (c) «No está demostrado en España» es demasiado prudente. Hay un diseño causal publicado en una revista con revisión por pares para Barcelona (2012-2016). Lo que no está medido es su validez en otras ciudades y después de 2017, con la exposición regulada.

## 6. Texto corregido y confianza

> «La culpa es de los pisos turísticos»: en la media nacional, no. Son en torno al 1,5 % de las viviendas y entre el 12 % y el 13,5 % del parque de alquiler. Su aumento entre 2020 y 2024 equivale como mucho al 2,7 % del alquiler. Con las estimaciones publicadas, eso deja un efecto nacional pequeño frente a la subida. En los barrios muy turísticos sí puede pesar. En una de cada diez secciones censales los pisos turísticos superan un tercio del alquiler. En Barcelona, un estudio con diseño causal estima alquileres un 7 % más altos en los barrios con más Airbnb (2012-2016). Fuera de esos barrios, y después de las regulaciones, no está medido.

Confianza:
- efecto nacional pequeño: **la evidencia sugiere** (escala local medida; elasticidad ajena);
- efecto en barrios muy turísticos de Barcelona en 2012-2016: **la evidencia indica**;
- en otras ciudades y en 2021-2026: **la evidencia es compatible con** un efecto local, sin medirlo.

## 7. Parada

**No hay parada sobre la 1.0.** El 2,7 % publicado (B4-v3-vut-cantidad, informe integral I.7 y VII.3) está rotulado como «el aumento 2020-2024 equivale como máximo a 2,7 %». Es correcto con esa definición, y su denominador es el mismo que el del Banco de España. La auditoría no muestra que esa cifra sea falsa.

**Aviso al autor, no es una parada.** La paráfrasis de D1, «≤ 2,7 % del parque de alquiler», no figura en publicacion/ ni en web/. Si se lee como peso de los pisos turísticos, es falsa: el peso es del 11,8-13,5 % (V17-AUD-DP-TUR-NAC-STOCK-*). Si esa frase se ha usado o se va a usar en divulgación, debe corregirse antes. Lo decide el autor.
