<!-- Generado por `make consulta` (src/consulta/generar.py). No editar a mano: se regenera y un test lo comprueba. -->

# Registro de hallazgos

Un registro por hallazgo de las versiones vigentes (v5-V8, con v4 donde sigue en cifras_clave): cifras de `output/v5/cifras_clave.csv`, fichas del verificador, conclusiones del historial e hipótesis retiradas. Las superadas y retiradas están al final y **no se citan**. La versión legible por máquina es [hallazgos.json](hallazgos.json). Las capas se leen según [metodologia/capas.md](../metodologia/capas.md): causalidad solo en C3 y C3s.

Vigentes por versión: v4: 7; v5: 415; v5.1: 39; v6: 146; v6.1: 48; v6.2: 4; v6.3: 8; v7: 33; v7.1: 69; v7.2: 7; V8: 366; v10: 28; v1: 8; v2: 7; v3: 3. Total vigentes: 1188.

## Versión v4

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `compradores_extranjeros` | Compraventas de vivienda con comprador extranjero (residente o no) | 16,89 % (16,89 a 18,82) | C4 | 2025 | [hechos.json](../output/v4/M4/hechos.json) |
| `compradores_no_residentes` | Compraventas con comprador extranjero no residente | 6,83 % | C4 | 2025 | [hechos.json](../output/v4/M4/hechos.json) |
| `dh_2125` | Aumento del número de hogares | 997.586 hogares (981.823 a 1.013.350) | C1 | 2021-2025 | [hechos.json](../output/v4/M2/hechos.json) |
| `latente_convivencia` | Demanda latente de jóvenes por convivencia con los padres (frente a 2008) | 188.000 a 506.000 hogares | C2 | 2008-2025 | [hechos.json](../output/v4/M2/hechos.json) |
| `terminadas_1924` | Viviendas terminadas al año (territorio común: sin País Vasco ni Navarra) | 72.264 a 94.426 viviendas/año | C1 | 2019-2024 | [terminadas_triangulacion.csv](../output/v4/M0/terminadas_triangulacion.csv) |
| `HIST-007` | Nacionalidad extranjera · Hogares creados (ΔH) | 53-76 % de ΔH en 2020-2025 según corrección EPA | C4 | 2006-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-029` | Déficit · Viviendas | 632.861 sin protegida; 598.157 con; v4 mediana 744.100 (657.059-933.231) | C4 | 2021Q1-2024Q2; 2021-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Versión v5

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `A23-A10` | Contratos nuevos Comunitat Valenciana 2021-2024: IPVA nuevo y fianzas GVA | 28,5 % (26,1 a 30,8) | C1 | 2021-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A11` | Rotación Cataluña: fianzas Incasòl / contratos vigentes SERPAVI | 25 % (25 a 43,2) | C4 | 2015-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A12` | Rotación Comunitat Valenciana: fianzas GVA / contratos vigentes SERPAVI | 13,5 % (13,5 a 15,8) | C4 | 2020-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A13` | Municipios con renta media de fianzas x2 o más (Incasòl 2015-2025, >=30 fianzas) | 1 municipios | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A14` | Municipios con mediana de fianza x2 o más (GVA 2020-2025, >=30 fianzas) | 2 municipios | C4 | 2020-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A2` | Alquiler stock 2015-2024: núcleo IPC de alquiler e IPVA (contratos existentes y total; tolerancia ±15 % en nivel) | 10,9 a 22,9 % | C1 | 2015-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A2b` | Alquiler stock 2015-2024: SERPAVI (renta declarada, composición constante), discrepante del núcleo | 43 % | C4 | 2015-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A3` | Contratos nuevos, IPVA nuevo contrato 2015-2024 (base 2015=100) | 37 % | C4 | 2015-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A4` | Contratos nuevos, Incasòl renta media 2015-2025 | 54,5 % | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A5` | Contratos nuevos, GVA mediana fianza 2020-2025 | 58 % | C4 | 2020-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A6` | Brecha nuevo menos existente (IPVA) 2024 | 13,6 % | C4 | 2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A7` | Cuota implícita de contratos nuevos en el IPVA | 16 % (13,9 a 17,6) | C4 | 2021-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A8` | Subida adicional del stock si todo contrato se actualizase al HICP (sin tope) | 7,2 % | C4 | 2022-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-A9` | Contratos nuevos Cataluña 2021-2024: IPVA nuevo e Incasòl | 16,9 % (16,6 a 17,2) | C1 | 2021-2024 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P1` | Precio de compra, variación acumulada 2015-2025, INE IPV | 79,9 % | C4 | 2015-2025 (media anual) | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P10` | Factor común de las 4 fuentes de precio: varianza explicada por el 1.er componente | 89,2 % | C4 | 2016-2025 (dln anual) | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P2` | Precio de compra, núcleo MIVAU/Notariado/Registradores 2015-2025 | 47,2 % (44,2 a 56,1) | C1 | 2015-2025 (media anual) | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P3` | Residuo no identificado del puente INE IPV -> núcleo (sin descomponer; candidatos: método, calidad, tamaño, cobertura) | -30,9 pp | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P4` | Diferencia contable del IPV con pesos CCAA comunes | 0,6 pp | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P5` | Diferencia contable por composición nueva/usada en la media de pm2 | 0 pp | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P6` | Precio por m2 Registradores nacional 2025 | 2.284 EUR/m2 | C4 | 2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P7` | Precio por m2 Notariado 2025 | 1.949 EUR/m2 | C4 | 2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P8` | Registradores con pesos provinciales de importe 2015 (52 provincias) | 66,8 % | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A23-P9` | Registradores con pesos CCAA de importe 2015 | 63,8 % | C4 | 2015-2025 | [hechos.json](../output/v5/A23/hechos.json) |
| `A4-001` | Rango oficial derivado de coste de construcción (MBC 1993 actualizado) | 677 EUR/m2 construido (422 a 932) | C4 | 2025T3-2026T2 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-conc50-2021-2024` | Provincias que suman el 50 % del déficit positivo | 6 provincias | C4 | 2021-2024 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-conc50-2021-2025` | Provincias que suman el 50 % del déficit positivo | 6 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-conc80-2021-2024` | Provincias que suman el 80 % del déficit positivo | 17 provincias | C4 | 2021-2024 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-conc80-2021-2025` | Provincias que suman el 80 % del déficit positivo | 18 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c1` | Provincias en clase 1 (1 falta y es rentable) | 24 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c1-robustas` | Provincias en clase 1 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 13 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c2` | Provincias en clase 2 (2 falta con freno regulatorio o de suelo (precio > r(c+suelo) y oferta sin respuesta)) | 6 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c2-robustas` | Provincias en clase 2 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 1 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c3` | Provincias en clase 3 (3 falta y no es rentable) | 0 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c3-robustas` | Provincias en clase 3 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 0 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c4` | Provincias en clase 4 (4 no falta (deficit <= 0)) | 20 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c4-robustas` | Provincias en clase 4 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 8 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c9` | Provincias en clase 9 (9 sin dato) | 2 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2012-2025-c9-robustas` | Provincias en clase 9 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 0 provincias | C4 | 2012-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c1` | Provincias en clase 1 (1 falta y es rentable) | 37 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c1-robustas` | Provincias en clase 1 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 8 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c2` | Provincias en clase 2 (2 falta con freno regulatorio o de suelo (precio > r(c+suelo) y oferta sin respuesta)) | 11 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c2-robustas` | Provincias en clase 2 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 3 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c3` | Provincias en clase 3 (3 falta y no es rentable) | 2 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c3-robustas` | Provincias en clase 3 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 0 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c4` | Provincias en clase 4 (4 no falta (deficit <= 0)) | 0 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c4-robustas` | Provincias en clase 4 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 0 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c9` | Provincias en clase 9 (9 sin dato) | 2 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A4-prov-2021-2025-c9-robustas` | Provincias en clase 9 con clase estable en todo el rango de costes, márgenes y holguras (diagnóstico) | 1 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/A4/hechos.json) |
| `A5-H01` | Documentos oficiales con texto buscado por palabras clave | 22 documentos | C4 | 2023-2026 | [hechos.json](../output/v5/A5/hechos.json) |
| `A5-H02` | Medidas de v4 sin documento oficial (excluidas de los recuentos) | 41 medidas | C4 | 2023 | [hechos.json](../output/v5/A5/hechos.json) |
| `A5-H03` | Medidas de v4 detectadas por el diccionario en el texto oficial | 44 medidas | C4 | 2023 | [hechos.json](../output/v5/A5/hechos.json) |
| `A5-H04` | Precisión del diccionario: coincidencias que son una medida (estricta) | 50 % (50 a 77,5) | C4 | 2023-2026 | [hechos.json](../output/v5/A5/hechos.json) |
| `B1-H2` | Atraso a absorber en 10 años (déficit 2021-2025 + emancipación retrasada) | 1.103.170 viviendas (830.963 a 1.473.641) | C4 | 2021-2025 absorbido en 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H3` | Reposición del parque (10 años) | 89.665 viviendas (1.070 a 178.259) | C4 | 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H4` | Crecimiento de hogares proyectado (INE, 10 años) | 1.720.537 hogares (1.308.531 a 1.772.410) | C2 | 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H5` | Ajuste de vacancia friccional en zonas con presión | 58.674 viviendas (0 a 117.348) | C4 | 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H6` | Vacías movilizables en zonas con presión (10-30 %) | 733.553 viviendas (366.777 a 1.100.330) | C4 | 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H7` | Cartera en construcción (iniciadas menos terminadas, 2-3 años) | 89.815 viviendas (75.674 a 103.956) | C4 | 2023-2025 | [hechos.json](../output/v5/B1/hechos.json) |
| `B1-H8` | Viviendas liberadas por envejecimiento (tasa de disolución de hogares de 75+) | 1.415.263 viviendas (801.982 a 2.170.070) | C4 | 2026-2035 | [hechos.json](../output/v5/B1/hechos.json) |
| `B2-H1` | Déficit acumulado nacional a fin de 2030 (suma de 52 provincias, escenario a) | 1.296.672 viviendas (872.529 a 1.447.953) | C4 | 1-ene-2026 a 31-dic-2030 | [hechos.json](../output/v5/B2/hechos.json) |
| `B2-H2` | Déficit 2021-2025 de partida (bajas 0) | 700.934 viviendas | C4 | 2021-2025 | [hechos.json](../output/v5/B2/hechos.json) |
| `B2-H3` | Crecimiento de hogares proyectado INE 2026-2030 | 1.024.156 hogares (819.421 a 1.060.364) | C2 | 1-ene-2026 a 1-ene-2031 | [hechos.json](../output/v5/B2/hechos.json) |
| `B2-H4` | Terminadas 2026-2030, ritmo actual (5 x media 2023-25) | 473.250 viviendas (402.475 a 648.361) | C4 | 2026-2030 | [hechos.json](../output/v5/B2/hechos.json) |
| `B2-H5` | Retardo medio iniciadas-terminadas (nacional) | 3,2 años (2,97 a 3,21) | C4 | ventanas 2008-2025 a 2022-2025 | [hechos.json](../output/v5/B2/hechos.json) |
| `B2-H6` | Provincias que empeoran / mejoran / indeterminadas (rango completo) | 20 provincias (5 a 27) | C4 | 2025 a 2030 | [hechos.json](../output/v5/B2/hechos.json) |
| `B3-H-B3-1-b` | Asociación de F1_bartik con la variación log del precio (por DT del regresor) | 2,36 puntos logarítmicos (-0,06 a 4,79) | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-1-p` | p ajustado Holm (8 familias) de H-B3-1 | 0,335 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-2-b` | Asociación de F2_dlnpob con la variación log del precio (por DT del regresor) | 3,55 puntos logarítmicos (-0,74 a 7,84) | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-2-p` | p ajustado Holm (8 familias) de H-B3-2 | 0,407 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-6-b` | Asociación de F6_lnp0 con la variación log del precio (por DT del regresor); con riesgo de error de medida: ver -control | -16,01 puntos logarítmicos (-23,79 a -8,23) | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-6-b-control` | H-B3-6 con el precio inicial de Registradores (control de error de medida; por DT) | -9,02 puntos logarítmicos | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-6-p` | p ajustado Holm (8 familias) de H-B3-6 | 0,0013 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-H-B3-6-p-control` | p (mayor de HC3/Conley) de H-B3-6 con el precio inicial de Registradores; p de permutación 0.016 | 0,058 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-R2` | R² del modelo de 8 familias (Y1 tasado, P1) | 0,912 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-mv-H-B3-1` | Multiverso H-B3-1: % de especificaciones con el signo de la principal | 62,5 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-mv-H-B3-2` | Multiverso H-B3-2: % de especificaciones con el signo de la principal | 100 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-mv-H-B3-6` | Multiverso H-B3-6: % de especificaciones con el signo de la principal | 100 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-shap-orden` | Shapley: mismo orden de familias con Y1 tasado y Registradores (1 = sí) | 0 indicador | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B3-shap-spearman` | Correlación de Spearman de los Shapley entre fuentes | 0,905 | C4 | 2015-2025 | [hechos.json](../output/v5/B3/hechos.json) |
| `B4-b3-shapley-demografica` | Cuota de R2 entre provincias de demografica (precio) | 23,62 % del R2 (21,06 a 26,18) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-b3-shapley-financiacion_tipos` | Cuota de R2 entre provincias de financiacion_tipos (precio) | 11,29 % del R2 (8,94 a 13,64) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-b3-shapley-oferta_suelo` | Cuota de R2 entre provincias de oferta_suelo (precio) | 25,89 % del R2 (23,18 a 28,6) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-b3-shapley-renta_empleo` | Cuota de R2 entre provincias de renta_empleo (precio) | 9,83 % del R2 (8,92 a 10,75) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-b3-shapley-residuo` | Cuota de R2 entre provincias de residuo (precio) | 18,84 a 29,87 % del R2 | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-b3-shapley-turismo_no_residentes` | Cuota de R2 entre provincias de turismo_no_residentes (precio) | 18,39 % del R2 (9,3 a 18,7) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-estabilidad-tau-min` | Tau de Kendall mínima del orden de familias entre métodos/periodos | -0,707 tau (-0,707 a 1) | C4 | 2015-2025 | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2019-demografica` | Contribución contable de demografica a alquiler (IPC, stock) (v2, M1-M2) | -3,59 pp de Δln acumulado (-4,15 a -3,03) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2019-financiacion_tipos` | Contribución contable de financiacion_tipos a alquiler (IPC, stock) (v2, M1-M2) | 0,011 pp de Δln acumulado (-0,125 a 0,148) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2019-oferta_suelo` | Contribución contable de oferta_suelo a alquiler (IPC, stock) (v2, M1-M2) | 0,019 pp de Δln acumulado (0,018 a 0,02) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2019-renta_empleo` | Contribución contable de renta_empleo a alquiler (IPC, stock) (v2, M1-M2) | 0,123 pp de Δln acumulado (0,081 a 0,166) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2019-residuo` | Contribución contable de residuo a alquiler (IPC, stock) (v2, M1-M2) | 5,02 pp de Δln acumulado (4,28 a 5,75) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2025-demografica` | Contribución contable de demografica a alquiler (IPC, stock) (v2, M1-M2) | -3,2 pp de Δln acumulado (-3,32 a -3,09) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2025-financiacion_tipos` | Contribución contable de financiacion_tipos a alquiler (IPC, stock) (v2, M1-M2) | -0,059 pp de Δln acumulado (-0,238 a 0,121) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2025-oferta_suelo` | Contribución contable de oferta_suelo a alquiler (IPC, stock) (v2, M1-M2) | 0,028 pp de Δln acumulado (0,025 a 0,03) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2025-renta_empleo` | Contribución contable de renta_empleo a alquiler (IPC, stock) (v2, M1-M2) | 0,163 pp de Δln acumulado (0,077 a 0,248) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2015-2025-residuo` | Contribución contable de residuo a alquiler (IPC, stock) (v2, M1-M2) | 10,35 pp de Δln acumulado (9,95 a 10,76) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2019-2025-demografica` | Contribución contable de demografica a alquiler (IPC, stock) (v2, M1-M2) | 0,387 pp de Δln acumulado (-0,053 a 0,828) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2019-2025-financiacion_tipos` | Contribución contable de financiacion_tipos a alquiler (IPC, stock) (v2, M1-M2) | -0,07 pp de Δln acumulado (-0,113 a -0,027) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2019-2025-oferta_suelo` | Contribución contable de oferta_suelo a alquiler (IPC, stock) (v2, M1-M2) | 0,009 pp de Δln acumulado (0,007 a 0,01) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2019-2025-renta_empleo` | Contribución contable de renta_empleo a alquiler (IPC, stock) (v2, M1-M2) | 0,039 pp de Δln acumulado (-0,004 a 0,082) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-alquiler_stock-2019-2025-residuo` | Contribución contable de residuo a alquiler (IPC, stock) (v2, M1-M2) | 5,33 pp de Δln acumulado (5 a 5,67) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2019-demografica` | Contribución contable de demografica a compra (valor tasado real) (v2, M1-M2) | -4,98 pp de Δln acumulado (-7,69 a -2,27) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2019-financiacion_tipos` | Contribución contable de financiacion_tipos a compra (valor tasado real) (v2, M1-M2) | 0,182 pp de Δln acumulado (0,027 a 0,337) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2019-oferta_suelo` | Contribución contable de oferta_suelo a compra (valor tasado real) (v2, M1-M2) | 0,111 pp de Δln acumulado (0,108 a 0,114) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2019-renta_empleo` | Contribución contable de renta_empleo a compra (valor tasado real) (v2, M1-M2) | 0,477 pp de Δln acumulado (0,052 a 0,901) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2019-residuo` | Contribución contable de residuo a compra (valor tasado real) (v2, M1-M2) | 7,6 pp de Δln acumulado (4,62 a 10,58) | C4 | 2015-2019 (v2: 2014Q1-2019Q4) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2025-demografica` | Contribución contable de demografica a compra (valor tasado real) (v2, M1-M2) | -7,02 pp de Δln acumulado (-7,53 a -6,5) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2025-financiacion_tipos` | Contribución contable de financiacion_tipos a compra (valor tasado real) (v2, M1-M2) | 1,15 pp de Δln acumulado (0,026 a 2,27) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2025-oferta_suelo` | Contribución contable de oferta_suelo a compra (valor tasado real) (v2, M1-M2) | 0,093 pp de Δln acumulado (0,087 a 0,099) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2025-renta_empleo` | Contribución contable de renta_empleo a compra (valor tasado real) (v2, M1-M2) | 1,09 pp de Δln acumulado (0,504 a 1,67) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2015-2025-residuo` | Contribución contable de residuo a compra (valor tasado real) (v2, M1-M2) | 3,58 pp de Δln acumulado (2,53 a 4,63) | C4 | 2015-2025 (v2: 2014Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2019-2025-demografica` | Contribución contable de demografica a compra (valor tasado real) (v2, M1-M2) | -2,04 pp de Δln acumulado (-5,27 a 1,19) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2019-2025-financiacion_tipos` | Contribución contable de financiacion_tipos a compra (valor tasado real) (v2, M1-M2) | 0,966 pp de Δln acumulado (-0,001 a 1,93) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2019-2025-oferta_suelo` | Contribución contable de oferta_suelo a compra (valor tasado real) (v2, M1-M2) | -0,018 pp de Δln acumulado (-0,021 a -0,014) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2019-2025-renta_empleo` | Contribución contable de renta_empleo a compra (valor tasado real) (v2, M1-M2) | 0,609 pp de Δln acumulado (0,451 a 0,766) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v2-compra-2019-2025-residuo` | Contribución contable de residuo a compra (valor tasado real) (v2, M1-M2) | -4,02 pp de Δln acumulado (-8,05 a 0,017) | C4 | 2019-2025 (v2: 2020Q1-2024Q1) | [hechos.json](../output/v5/B4/hechos.json) |
| `B4-v3-vut-cantidad` | Máximo de stock de alquiler desplazado por viviendas turísticas | 2,75 % del stock de alquiler (2,42 a 2,75) | C2 | 2020M08-2024M08 | [hechos.json](../output/v5/B4/hechos.json) |
| `CA-CR-saldo-2025` | Saldo de crédito a construcción + actividades inmobiliarias | 97,57 miles de millones de euros | C4 | 2025Q4 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CR-saldo-caida` | Caída del saldo de crédito a constr.+inmob. desde su máximo hasta 2025Q4 | -79,32 % | C4 | 2008Q3-2025Q4 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CR-saldo-pico` | Saldo de crédito a construcción + actividades inmobiliarias: máximo 2005-2025 | 471,8 miles de millones de euros | C4 | 2008Q3 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-contado-cota` | Cota inferior del contado si todas las hipotecas fueran de compra (phi = 1) | 29,95 % de compraventas | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-phi-critico` | Fracción de hipotecas dedicadas a compra por debajo de la cual el contado supera el 50 % | 71,38 % de las hipotecas | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-ratio-ine` | Hipotecas sobre vivienda por 100 compraventas de vivienda (INE) | 70,05 hipotecas por 100 compraventas (63,89 a 159,8) | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-ratio-triang-2022` | Hipotecas por 100 compraventas: INE 71.4 frente a Registradores 71.7 | 71,37 hipotecas por 100 compraventas | C4 | 2022 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-ratio-triang-2023` | Hipotecas por 100 compraventas: INE 65.3 frente a Registradores 65.8 | 65,27 hipotecas por 100 compraventas | C4 | 2023 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-ratio-triang-2024` | Hipotecas por 100 compraventas: INE 66.4 frente a Registradores 68.4 | 66,45 hipotecas por 100 compraventas | C4 | 2024 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-CT-ratio-triang-2025` | Hipotecas por 100 compraventas: INE 70.0 frente a Registradores 70.7 | 70,05 hipotecas por 100 compraventas | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-alq_real-crecimiento` | Alquiler real (IPCA rúbrica CP041 deflactado, 2015=100) · crecimiento: España | -10,3 % acumulado desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-alquiler_mercado-cambio_desde_2015` | Alquiler a precio de mercado (ilc_lvho02) · cambio_desde_2015: España | 4,7 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-alquiler_mercado-nivel` | Alquiler a precio de mercado (ilc_lvho02) · nivel: España | 17,4 nivel % población | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-crec_pob-nivel` | Crecimiento de la población (demo_gind) · nivel: España | 9,4 nivel por 1.000 hab. | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-emancipacion-cambio_desde_2015` | Edad media de salida del hogar parental (yth_demo_030) · cambio_desde_2015: España | 1,2 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-emancipacion-nivel` | Edad media de salida del hogar parental (yth_demo_030) · nivel: España | 30,2 nivel años | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-hacinamiento-cambio_desde_2015` | Hacinamiento (ilc_lvho05a) · cambio_desde_2015: España | 4 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-hacinamiento-nivel` | Hacinamiento (ilc_lvho05a) · nivel: España | 9,5 nivel % población | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-hpi_real-crecimiento` | Precio de la vivienda real (HPI deflactado por IPCA, 2015=100) · crecimiento: España | 42,6 % acumulado desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-migr_neta-nivel` | Migración neta con ajuste (demo_gind) · nivel: España | 11,8 nivel por 1.000 hab. | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-permisos_1000-cambio_desde_2015` | Viviendas con permiso por 1.000 habitantes (sts_cobp_a / demo_pjan) · cambio_desde_2015: España | 3,29 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-permisos_1000-nivel` | Viviendas con permiso por 1.000 habitantes (sts_cobp_a / demo_pjan) · nivel: España | 4,07 nivel viv./1.000 hab. | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-propiedad-cambio_desde_2015` | Tenencia en propiedad (ilc_lvho02) · cambio_desde_2015: España | -4,6 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-propiedad-nivel` | Tenencia en propiedad (ilc_lvho02) · nivel: España | 73,6 nivel % población | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-sobrecarga-cambio_desde_2015` | Sobrecarga de coste de vivienda (ilc_lvho07a) · cambio_desde_2015: España | -3,1 cambio desde 2015 | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CA-EU-sobrecarga-nivel` | Sobrecarga de coste de vivienda (ilc_lvho07a) · nivel: España | 7,2 nivel % población | C4 | 2025 | [hechos.json](../output/v5/CA/hechos.json) |
| `CB-C5-01` | Lanzamientos practicados por LAU (principalmente alquiler impagado) | 18.317 lanzamientos/anio | C4 | 2025 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C5-02` | Lanzamientos practicados por LAU, maximo 2013-2025 | 38.141 lanzamientos/anio | C4 | 2013-2025 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C5-03` | Hechos conocidos por allanamiento/usurpacion de inmuebles | 14.875 hechos/anio | C4 | 2025 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C5-04` | Verbales posesorios por ocupacion ilegal de viviendas ingresados | 1.845 procedimientos/anio | C4 | 2025 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C5-05` | Viviendas principales en alquiler (Censo 2021) | 2.965.497 viviendas | C4 | 2021 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C6-01` | Declarantes IRPF con ingresos de capital inmobiliario | 3.262.026 declarantes | C4 | 2024 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C6-02` | Declarantes IRPF con reduccion por arrendamiento de vivienda (art. 23.2 LIRPF) | 2.236.896 declarantes | C4 | 2024 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C6-03` | Viviendas equivalentes arrendadas por personas fisicas (habitual y otras) | 2.650.952 viviendas | C4 | 2024 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C6-04` | Viviendas equivalentes arrendadas por personas fisicas por declarante con ingresos de capital inmobiliario | 0,81 viviendas/declarante | C4 | 2024 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C6-05` | Residual (PJ + sector publico + alquiler no declarado) sobre el stock en alquiler | 16,9 % del stock (16,9 a 38,1) | C4 | 2021-2025 | [hechos.json](../output/v5/CB/hechos.json) |
| `CB-C8-01` | Compraventas con comprador persona juridica | 11,3 % de compraventas | C4 | 2024 | [hechos.json](../output/v5/CB/hechos.json) |
| `CC-C2-nuevas5a` | Calificaciones definitivas de vivienda protegida, media anual | 11.265 viviendas/año | C4 | 2021-2025 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C2-ratio` | Salidas anuales medias 2026-2035 (base) / calificaciones nuevas anuales medias 5 años | 5,28 ratio (4,72 a 5,94) | C4 | 2026-2035 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C2-salidas-alto` | Viviendas protegidas que saldrían del régimen 2026-2035 (escenario ilustrativo alto; cota inferior lógica 0) | 669.394 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C2-salidas-bajo` | Viviendas protegidas que saldrían del régimen 2026-2035 (escenario ilustrativo bajo; cota inferior lógica 0) | 532.040 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C2-salidas-base` | Viviendas protegidas que saldrían del régimen 2026-2035 (escenario ilustrativo base; cota inferior lógica 0) | 594.890 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7a-qu-QU1` | Tasa de sobrecarga de coste de vivienda, primer quintil de renta, España | 27,7 % de personas (27,7 a 40,9) | C4 | 2025 (2015: 40.9 %) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7a-qu-QU5` | Tasa de sobrecarga de coste de vivienda, quinto quintil de renta, España | 0,2 % de personas (0,1 a 0,3) | C4 | 2025 (2015: 0.2 %) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7a-ten-OWN_L` | Tasa de sobrecarga de coste de vivienda, propietarios con hipoteca, España | 3,4 % de personas (3 a 8,7) | C4 | 2025 (2015: 8.7 %) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7a-ten-RENT_MKT` | Tasa de sobrecarga de coste de vivienda, inquilinos a precio de mercado, España | 26,8 % de personas (26,8 a 43,3) | C4 | 2025 (2015: 43.3 %) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7b-alq-d123` | Inquilinos a precio de mercado situados en los deciles 1-3 de renta por UC | 46,9 % de personas inquilinas | C4 | 2025 | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7b-jov-cesion` | Hogares de 16-29 años en vivienda cedida (gratis o precio inferior) | 14,7 % de hogares | C4 | 2025 (2015 en min) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7b-jov-prop` | Hogares con persona de referencia de 16-29 años en propiedad | 30,6 % de hogares | C4 | 2025 (2015 en min) | [hechos.json](../output/v5/CC/hechos.json) |
| `CC-C7b-jov-sinhip` | Hogares de 16-29 años en propiedad sin hipoteca (proxy NO medida de herencia/donación) | 14,1 % de hogares | C4 | 2025 | [hechos.json](../output/v5/CC/hechos.json) |
| `D1-H01` | Instrumentos evaluados con la rúbrica (I01-I29 sin I17 ni I23, N1-N9) | 36 instrumentos | C4 | 2026-10 | [hechos.json](../output/v5/D1/hechos.json) |
| `D1-H02` | Instrumentos con 'No evaluable' en el signo | 18 instrumentos | C4 | 2026-10 | [hechos.json](../output/v5/D1/hechos.json) |
| `D1-H11` | Parte de una ayuda general que se traslada al precio, clase A4 1 (método A) | 58,4 % (27,8 a 81,8) | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/D1/hechos.json) |
| `D1-H12` | Parte de una ayuda general que se traslada al precio, clase A4 2 (método A) | 100 % (88,1 a 100) | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/D1/hechos.json) |
| `D1-H13` | Parte de una ayuda general que se traslada al precio, clase A4 3 (método A) | 76,4 % (50,1 a 89,8) | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/D1/hechos.json) |
| `D2-H01` | Necesidad anual de vivienda, provincias de clase A4 1 (T3 sin X, v6.3) | 185.283 viviendas/año (96.224 a 251.870) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H02` | Necesidad anual de vivienda, provincias de clase A4 2 (T3 sin X, v6.3) | 21.155 viviendas/año (2.983 a 35.113) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H03` | Necesidad anual de vivienda, provincias de clase A4 3 (T3 sin X, v6.3) | 3.260 viviendas/año (-112 a 4.185) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H09` | Necesidad anual de vivienda, provincias de clase A4 9 (T3 sin X, v6.3) | 726 viviendas/año (293 a 919) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H11` | Cobertura de la necesidad por la construcción adicional de P-D (+25-100 mil/año repartidas por cuota), clase 1 | 29,7 % (11,9 a 47,5) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H12` | Cobertura de la necesidad por la construcción adicional de P-D (+25-100 mil/año repartidas por cuota), clase 2 | 29,7 % (11,9 a 47,5) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D2-H13` | Cobertura de la necesidad por la construcción adicional de P-D (+25-100 mil/año repartidas por cuota), clase 3 | 29,7 % (11,9 a 47,5) | C4 | 2026-2035 | [hechos.json](../output/v5/D2/hechos.json) |
| `D3-coincide` | Referencias de organismos: coincide | 2 referencias | C4 | 2026-10-10 | [hechos.json](../output/v5/D3/hechos.json) |
| `D3-comparable_en_parte` | Referencias de organismos: comparable en parte | 6 referencias | C4 | 2026-10-10 | [hechos.json](../output/v5/D3/hechos.json) |
| `D3-control_misma_fuente` | Referencias de organismos: control misma fuente | 4 referencias | C4 | 2026-10-10 | [hechos.json](../output/v5/D3/hechos.json) |
| `D3-difiere` | Referencias de organismos: difiere | 1 referencias | C4 | 2026-10-10 | [hechos.json](../output/v5/D3/hechos.json) |
| `D3-no_comparable` | Referencias de organismos: no comparable | 9 referencias | C4 | 2026-10-10 | [hechos.json](../output/v5/D3/hechos.json) |
| `E-B1-A1` | Atraso: déficit 2021-2025 (componente A1) | 788.154 viviendas (643.007 a 967.740) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-A2` | Atraso: emancipación retrasada (componente A2) | 315.017 viviendas (187.956 a 505.902) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-F` | Crecimiento de hogares proyectado (componente F, 10 años) | 1.720.537 hogares (1.308.531 a 1.772.410) | C2 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-K` | Cartera en construcción (componente K) | 89.815 viviendas (75.674 a 103.956) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-L` | Viviendas liberadas por envejecimiento (componente L, 10 años; no se resta) | 1.415.263 viviendas (801.982 a 2.170.070) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-L_en_presion_central` | Viviendas liberadas por envejecimiento en provincias con presión (10 años) | 1.373.851 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-M` | Vacías movilizables en zonas con presión (componente M, 10 años) | 733.553 viviendas (366.777 a 1.100.330) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-N10` | Necesidad de vivienda acumulada en 10 años (A+R+V+F-M-K), suma de 52 provincias | 2.148.678 viviendas (936.278 a 3.099.208) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-N10_formula_literal_menos_L` | Variante literal: necesidad 10 años restando además L (duplica disoluciones) | 733.415 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-N10_solo_presion_central` | Necesidad 10 años solo en provincias con presión | 2.110.221 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-R` | Reposición del parque (componente R, 10 años; límite inferior) | 89.665 viviendas (1.070 a 178.259) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-Rnopos` | Provincias con tasas brutas de baja no positivas en los dos métodos de reposición | 38 provincias | C4 | 2011-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual` | Necesidad de vivienda por año (N10/10), suma de 52 provincias | 214.868 viviendas/año (93.628 a 309.921) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual-Alicante` | Necesidad de vivienda por año, provincia de Alicante/Alacant | 14.264 viviendas/año (10.484 a 18.624) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual-Barcelona` | Necesidad de vivienda por año, provincia de Barcelona | 30.963 viviendas/año (21.166 a 45.466) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual-Castellon` | Necesidad de vivienda por año, provincia de Castellón/Castelló | 4.267 viviendas/año (2.788 a 5.685) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual-Madrid` | Necesidad de vivienda por año, provincia de Madrid | 47.228 viviendas/año (36.705 a 59.722) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-anual-Valencia` | Necesidad de vivienda por año, provincia de Valencia/València | 16.993 viviendas/año (13.241 a 22.407) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B1-npresion` | Provincias con presión (clase A4 1-3) | 48 provincias | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B2-D2030-b` | Déficit acumulado a fin de 2030, escenario b (cartera con retardo) | 1.136.179 viviendas | C4 | 2026-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B2-Tb` | Terminadas 2026-2030, escenario b (cartera con retardo) | 633.743 viviendas | C4 | 2026-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B2-empeora` | Provincias cuyo déficit 2025-2030 empeora en todo el rango (ritmo actual) | 20 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B2-indeterminado` | Provincias cuyo déficit 2025-2030 indeterminado en todo el rango (ritmo actual) | 27 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B2-mejora` | Provincias cuyo déficit 2025-2030 mejora en todo el rango (ritmo actual) | 5 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-EMD` | Efecto mínimo detectable con Holm m=8 (R² 0,5, VIF 2; rango de la rejilla) | 0,619 DT (0,339 a 1,1) | C4 | pre-registro 2026-10-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-1-ic` | H-B3-1: coeficiente por DT del regresor con IC95 (HC3/Conley, mayor EE) | 2,36 puntos log. por DT (-0,061 a 4,79) | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-1-p3` | H-B3-1: p Holm sobre las 3 confirmatorias | 11,15 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-1-pri` | H-B3-1: p por aleatorización Freedman-Lane | 4,92 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-2-ic` | H-B3-2: coeficiente por DT del regresor con IC95 (HC3/Conley, mayor EE) | 3,55 puntos log. por DT (-0,739 a 7,84) | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-2-p3` | H-B3-2: p Holm sobre las 3 confirmatorias | 11,15 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-2-pri` | H-B3-2: p por aleatorización Freedman-Lane | 7,32 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-6-ic` | H-B3-6: coeficiente por DT del regresor con IC95 (HC3/Conley, mayor EE) | -16,01 puntos log. por DT (-23,79 a -8,23) | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-6-p3` | H-B3-6: p Holm sobre las 3 confirmatorias | 0,054 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-6-p8` | H-B3-6: p Holm sobre 8 familias | 0,127 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-H-B3-6-pri` | H-B3-6: p por aleatorización Freedman-Lane | 0,02 % | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-N` | Provincias en la muestra principal de B3 | 50 provincias | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-R2reg` | R² del modelo de 8 familias con precio de Registradores | 0,821 | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-kendall` | Tau de Kendall de los Shapley entre fuentes de precio | 0,786 | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-B3-rmse` | RMSE dejando una fuera, modelo de 8 familias (máx = modelo de solo media) | 0,066 log-puntos | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-D2030-a` | Déficit nacional a fin de 2030, escenario (a) de terminadas (central) | 1.296.672 viviendas | C4 | 1-ene-2026 a 31-dic-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-D2030-b` | Déficit nacional a fin de 2030, escenario (b) de terminadas (central) | 1.136.179 viviendas | C4 | 1-ene-2026 a 31-dic-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-D2030-c` | Déficit nacional a fin de 2030, escenario (c) de terminadas (central) | 1.276.238 viviendas | C4 | 1-ene-2026 a 31-dic-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-empeora` | Provincias cuyo déficit empeora 2025-2030 en todo el rango | 20 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-empeora-a` | Provincias que empeoran, escenario (a) central | 45 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-empeora-b` | Provincias que empeoran, escenario (b) central | 40 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-empeora-c` | Provincias que empeoran, escenario (c) central | 41 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-estable3` | Provincias con el mismo signo central en los 3 escenarios de terminadas | 46 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-indeterminado` | Provincias cuyo déficit indeterminado 2025-2030 en todo el rango | 27 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B2-mejora` | Provincias cuyo déficit mejora 2025-2030 en todo el rango | 5 provincias | C4 | 2025 a 2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-N` | Provincias del corte transversal principal de B3 (sin Ceuta ni Melilla) | 50 provincias | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-RV-H-B3-1` | Cinelli-Hazlett RV (q=1) de H-B3-1 | 0,281 R² parcial (0,041 a 0,32) | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-RV-H-B3-2` | Cinelli-Hazlett RV (q=1) de H-B3-2 | 0,262 R² parcial (0,015 a 0,298) | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-mvp-H-B3-1` | Multiverso H-B3-1: % de especificaciones con p<0,05 | 3,12 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-mvp-H-B3-2` | Multiverso H-B3-2: % de especificaciones con p<0,05 | 59,38 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-mvp-H-B3-6` | Multiverso H-B3-6: % de especificaciones con p<0,05 | 46,88 % | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-nesp` | Especificaciones del multiverso por hipótesis confirmatoria (B3) | 32 especificaciones | C4 | 2015-2025 / 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-oster-H-B3-1` | Oster δ (Rmax acotado a 1) de H-B3-1 | 3,76 razón δ | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-B3-oster-H-B3-2` | Oster δ (Rmax acotado a 1) de H-B3-2 | 1,61 razón δ | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D1-incB-1` | Parte de una ayuda general que se traslada al precio, clase A4 1 (método B, rejilla P-D) | 30,95 % (14,63 a 46,15) | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D1-incB-2` | Parte de una ayuda general que se traslada al precio, clase A4 2 (método B, rejilla P-D) | 100 % | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D1-incB-3` | Parte de una ayuda general que se traslada al precio, clase A4 3 (método B, rejilla P-D) | 63,05 % (40 a 76,92) | C4 | rejilla εd 0,3-1,5 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-cobpd-1` | Cobertura de la necesidad por la construcción adicional de P-D, clase A4 1 | 29,7 % (11,88 a 47,52) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-cobpd-2` | Cobertura de la necesidad por la construcción adicional de P-D, clase A4 2 | 29,7 % (11,88 a 47,52) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-covvac-1` | Cobertura de la necesidad por vacías movilizables, clase A4 1 (central) | 30,89 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-covvac-2` | Cobertura de la necesidad por vacías movilizables, clase A4 2 (central) | 76,22 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-nprov-1` | Provincias de clase A4 1 (2021-2025) | 37 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-nprov-2` | Provincias de clase A4 2 (2021-2025) | 11 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-nrob-1` | Provincias de clase A4 1 con clase robusta (2021-2025) | 8 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-nrob-2` | Provincias de clase A4 2 con clase robusta (2021-2025) | 3 provincias | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-vac-1` | Vacías movilizables por año, clase A4 1 (central y rango) | 57.230 viviendas/año (28.615 a 85.845) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-D2-vac-2` | Vacías movilizables por año, clase A4 2 (central y rango) | 16.125 viviendas/año (8.063 a 24.188) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-B1` | Necesidad anual de vivienda, provincia de València | 16.993 viviendas/año (13.241 a 22.407) | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-B2` | Déficit acumulado a fin de 2030, provincia de València | 118.711 viviendas (112.120 a 128.910) | C4 | 1-ene-2026 a 31-dic-2030 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-claseciu-v4` | Clase M3 v4 de València ciudad (coste supuesto) | 2 clase | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-claseciu-v5` | Clase A4 v5 de València ciudad (rango oficial de coste) | 1 clase | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-claseprov` | Clase A4 de la provincia de València (2021-2025) | 1 clase | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-contratos` | Contratos SERPAVI con renta declarada en los distritos de València, 2024 | 65.742 contratos | C4 | 2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-crec-max` | Crecimiento de la renta mediana SERPAVI 2015-2024, distrito Ciutat Vella | 85,81 % | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-crec-med` | Crecimiento de la renta mediana SERPAVI 2015-2024, mediana entre distritos | 73,49 % (50,66 a 85,81) | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-crec-min` | Crecimiento de la renta mediana SERPAVI 2015-2024, distrito Poblats Del Nord | 50,66 % | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-def2125` | Déficit contable 2021-2025, provincia de València (mediana y rango) | 68.926 viviendas (59.206 a 80.093) | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-defciu` | Déficit contable 2021-2025, València ciudad (fuente única) | 13.048 viviendas | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-estab-v4` | Estabilidad de la clase M3 v4 de València ciudad en el multiverso | 97,22 % | C4 | 2021-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-fianza-2020` | Mediana de la fianza depositada en la GVA, 2020 | 500 € | C4 | 2020 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-fianza-2025` | Mediana de la fianza depositada en la GVA, 2025 | 790 € | C4 | 2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-fianza-n2025` | Fianzas depositadas en la GVA, 2025 | 35.079 contratos | C4 | 2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-ndist` | Distritos de València ciudad con SERPAVI y nombre | 19 distritos | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-precio` | Valor tasado de la vivienda libre, València ciudad | 2.849 €/m² | C4 | 2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-serpavi-max` | Renta mediana SERPAVI 2024, distrito Ciutat Vella | 10,9 €/m²/mes | C4 | 2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-serpavi-med` | Mediana entre distritos de la renta mediana SERPAVI 2024 | 8,03 €/m²/mes (5,87 a 10,9) | C4 | 2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-VLC-serpavi-min` | Renta mediana SERPAVI 2024, distrito Poblats Del Nord | 5,87 €/m²/mes | C4 | 2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-nprov` | Provincias (y ciudades autónomas) de la contabilidad provincial B1/B2 | 52 provincias | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-anc` | Afirmaciones con veredicto «ANALIZADA, NO CONCLUYENTE» | 32 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-contr` | Afirmaciones con veredicto «CONTRADICHA» | 1 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-n` | Afirmaciones del debate evaluadas en el verificador v5 | 40 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-nafd` | Afirmaciones con veredicto «NO ANALIZADA: FALTAN DATOS» | 3 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-nresp` | Afirmaciones con veredicto «NO RESPALDADA» | 1 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-E1-ver-parc` | Afirmaciones con veredicto «PARCIALMENTE» | 3 afirmaciones | C4 | 2026-10 | [hechos.json](../output/v5/E/hechos.json) |
| `E-GL-coef` | Réplica García-López: coeficiente propio (FE sección y año, sin IV), Barcelona | -4,17 milésimas de log-punto por pu… (-7,79 a -0,542) | C4 | 2021-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-GL-esperado` | Coeficiente esperado en un stock si el efecto de GL sobre el flujo se atenuase | 6,69 milésimas de log-punto por pu… | C4 | 2012-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-GL-lambda` | Parte de la variación del flujo (Incasòl) que recoge el stock (SERPAVI) | 55,05 % (55,05 a 74,91) | C4 | 2022-2024 (máx: 2015-2020) | [hechos.json](../output/v5/E/hechos.json) |
| `E-GL-pholm` | Réplica García-López: p ajustado Holm | 26,86 % | C4 | 2021-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-demol-2024` | Viviendas con licencia de demolición en 2024 en % del parque (definición estrecha y amplia) | 0,022 a 0,036 % del parque | C4 | 2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-lib-capital` | Viviendas liberadas por envejecimiento en capitales de provincia (central) | 619.768 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-lib-entorno` | Viviendas liberadas por envejecimiento en entorno de las grandes ciudades (central) | 137.395 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-lib-resto` | Viviendas liberadas por envejecimiento en resto de municipios (central) | 1.099.268 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-A` | Peso en la amplitud de la necesidad anual 2026-2035: atraso (A1+A2) | 20,65 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-F` | Peso en la amplitud de la necesidad anual 2026-2035: flujo futuro (F) | 21,6 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-K` | Peso en la amplitud de la necesidad anual 2026-2035: cartera (K) | 1,32 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-M` | Peso en la amplitud de la necesidad anual 2026-2035: movilizables (M) | 34,16 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-R` | Peso en la amplitud de la necesidad anual 2026-2035: reposición (R) | 6,54 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-V` | Peso en la amplitud de la necesidad anual 2026-2035: vacancia friccional (V) | 5,46 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-peso-X` | Peso en la amplitud de la necesidad anual 2026-2035: liberadas que no llegan al mercado (X) | 10,26 % | C4 | 2026-2035 | [hechos.json](../output/v5/E/hechos.json) |
| `E-T7-prod` | Viviendas terminadas al año, España con País Vasco y Navarra (mín. y máx. anual) | 78.810 a 100.980 viviendas/año | C1 | 2019-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M1A-HOLM` | Hipótesis confirmatorias de alquiler que pasan Holm (p<0,05) | 0 hipótesis | C4 | 2021-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M1A-NCONF` | Hipótesis confirmatorias de alquiler contrastadas con Holm | 16 hipótesis | C4 | 2021-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M1B-GSADF-SIG` | CCAA con exuberancia GSADF (p<0,05) en el ratio precio/alquiler | 0 CCAA | C4 | 2015T1-2024T4 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M1B-GSADF-TOT` | CCAA contrastadas con GSADF | 11 CCAA | C4 | 2015T1-2024T4 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M1B-HOLM` | Hipótesis confirmatorias de compra que pasan Holm (p<0,05) | 0 hipótesis | C4 | 2016-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-ALQ-ln_iniciadas_libres` | PIP BMA núcleo (sin VUT ni suelo) de viviendas libres iniciadas, alquiler de stock (SERPAVI), provincia | 0,97 | C4 | 2015-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-ALQ-ln_pib_pc` | PIP BMA núcleo (sin VUT ni suelo) de PIB por habitante, alquiler de stock (SERPAVI), provincia | 0,188 | C4 | 2015-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-ALQ-ln_pob` | PIP BMA núcleo (sin VUT ni suelo) de población, alquiler de stock (SERPAVI), provincia | 1 | C4 | 2015-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-ALQ-share_ext_pob` | PIP BMA núcleo (sin VUT ni suelo) de población extranjera, alquiler de stock (SERPAVI), provincia | 0,062 | C4 | 2015-2023 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-COMPRA-ln_iniciadas_libres` | PIP BMA núcleo (sin VUT ni suelo) de viviendas libres iniciadas, precio de compra (tasado MIVAU), provincia | 0,056 | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-COMPRA-ln_pib_pc` | PIP BMA núcleo (sin VUT ni suelo) de PIB por habitante, precio de compra (tasado MIVAU), provincia | 0,47 | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-COMPRA-ln_pob` | PIP BMA núcleo (sin VUT ni suelo) de población, precio de compra (tasado MIVAU), provincia | 1 | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M2-PIPN-COMPRA-share_ext_pob` | PIP BMA núcleo (sin VUT ni suelo) de población extranjera, precio de compra (tasado MIVAU), provincia | 0,772 | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3A-DL-gnn` | RMSE de validación interna, GraphSAGE, alquiler de stock (distrito) | 4,8 log-puntos x100 | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3A-DL-mlp` | RMSE de validación interna, MLP con embeddings, alquiler de stock (distrito) | 4,8 log-puntos x100 | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3A-DLp-gnn` | p DM-HLN de GraphSAGE frente a gradient boosting, alquiler de stock (distrito) | 0,606 p | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3A-DLp-mlp` | p DM-HLN de MLP con embeddings frente a gradient boosting, alquiler de stock (distrito) | 0,633 p | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3A-GB-dis` | RMSE de validación interna, gradient boosting, alquiler de stock (distrito) | 4,81 log-puntos x100 | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3B-DL_GCN_espacial` | RMSE % de GCN espacial, precio municipal anual, validación por bloques con embargo | 8,31 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3B-DL_MLP_tabular` | RMSE % de MLP tabular, precio municipal anual, validación por bloques con embargo | 5,19 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3B-PERS-PROV_PRECIO_TRIM` | RMSE % de la persistencia, precio provincial trimestral, validación por bloques con embargo | 1,91 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3B-PERS-PROV_VOL_TRIM` | RMSE % de la persistencia, volumen provincial trimestral, validación por bloques con embargo | 25,75 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3Bp-DL_GCN_espacial` | p DM-HLN de GCN espacial frente a gradient boosting, precio municipal anual | 0,063 p | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M3Bp-DL_MLP_tabular` | p DM-HLN de MLP tabular frente a gradient boosting, precio municipal anual | 0,454 p | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M4-TEMP-PROV_VOL_TRIM` | RMSE temporal sellado del mejor modelo (bosque), volumen provincial trimestral | 12 log-puntos x100 | C4 | último año (temporal ya visto en v2) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-M4-TEMPPERS-PROV_VOL_TRIM` | RMSE temporal sellado de la persistencia, volumen provincial trimestral | 11,29 log-puntos x100 | C4 | último año (temporal ya visto en v2) | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-NPROV-SELL` | Provincias selladas en la validación v6 (bloques de CCAA) | 11 provincias | C4 | 2015-2025 | [hechos.json](../output/v5/E/hechos.json) |
| `E-V6-NPROV-TRAIN` | Provincias de entrenamiento en v6 | 41 provincias | C4 | 2015-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-1` | VUT por 100 viviendas y alquiler SERPAVI (FE sección, nacional), coeficiente v3 | 0,26 milésimas de log-punto por VU… (-0,744 a 1,26) | C4 | 2021-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-1-p` | p Holm de H3-1 (v3) | 46,66 % | C4 | 2021-2024 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-3a-CS` | Topes v3 (renta), DiD Callaway-Sant'Anna en entrenamiento; reportado como C4 | -5,41 % (-7,09 a -3,7) | C4 | 2018-2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-3a-sell` | Topes v3 (renta), DiD anual en la muestra sellada; validación contaminada, C4 | -0,77 % (-1,39 a -0,145) | C4 | 2018-2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-3b-CS` | Topes v3 (contratos), DiD Callaway-Sant'Anna en entrenamiento; reportado como C4 | -4,87 % (-9,93 a 0,465) | C4 | 2018-2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-H3-3b-sell` | Topes v3 (contratos), DiD anual en la muestra sellada; validación contaminada, C4 | -4,36 % (-6,37 a -2,3) | C4 | 2018-2022 | [hechos.json](../output/v5/E/hechos.json) |
| `E-v3-vut-precio-cota` | Cota de precio atribuible a VUT con la elasticidad mínima de la rejilla (v3) | 8,32 % | C4 | 2020M08-2024M08 | [hechos.json](../output/v5/E/hechos.json) |
| `R1A-H1` | Peso de compradores extranjeros no residentes en las compraventas, España 2025 | 6,83 % | C4 | 2025 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H2` | Peso de compradores extranjeros no residentes, España 2015 | 9,86 % | C4 | 2015 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H3` | Peso de no residentes extranjeros por provincia 2025 (rango entre unidades) | 32,5 % (0,07 a 32,5) | C4 | 2025 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H4` | Asociación bivariada precio 2015-2025 y peso inicial de no residentes (coef.) | 0,96 % de precio por punto de peso… (0,46 a 1,47) | C4 | 2015-2025 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H5` | Misma asociación con renta, población, costa e islas (coef.) | 0,02 % de precio por punto de peso… (-0,55 a 0,59) | C4 | 2015-2025 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H6` | Cociente VUT registro GVA (stock) / INE, 3 provincias valencianas, 2024-11 | 1,56 veces (1,41 a 1,75) | C4 | 2020-08 a 2024-11 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H7` | Cociente VUT registro vigente GVA (2026-10-09) / INE (2026-05) | 1,76 veces (1,42 a 1,91) | C4 | 2026 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1A-H8` | Cobertura de la suma de secciones INE VUT frente al total provincial (52 provincias) | 90,4 % (90,2 a 90,7) | C4 | 2024-11 a 2026-05 | [hechos.json](../output/v5/R1A/hechos.json) |
| `R1B-D-serpavi_VC` | Cambio de pendiente del gradiente de crecimiento anual con la distancia al centro (2019-2024 menos 2015-2019), alquiler SERPAVI V… | 0,161 pp de crecimiento anual por c… (-0,141 a 0,464) | C4 | 2015-2019 frente a 2019-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-D-serpavi_VC-holm` | Proporción de especificaciones significativas tras Holm, alquiler SERPAVI VC | 0  (0 a 1) | C4 | 2015-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-D-serpavi_VC-mv` | Proporción de especificaciones con cambio de pendiente positivo (periferia gana frente al centro), alquiler SERPAVI VC | 0,771 | C4 | 2015-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-D-tasado` | Cambio de pendiente del gradiente de crecimiento anual con la distancia al centro (2019-2024 menos 2015-2019), valor tasado (>25.… | -0,044 pp de crecimiento anual por c… (-0,507 a 0,418) | C4 | 2015-2019 frente a 2019-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-D-tasado-holm` | Proporción de especificaciones significativas tras Holm, valor tasado (>25.000 hab.) | 0  (0 a 1) | C4 | 2015-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-D-tasado-mv` | Proporción de especificaciones con cambio de pendiente positivo (periferia gana frente al centro), valor tasado (>25.000 hab.) | 0,547 | C4 | 2015-2024 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-0` | GSADF (vc bootstrap AR): precio/renta: IPV / renta del hogar | 3,42 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-1` | GSADF (vc bootstrap AR): precio/alquiler: IPV / IPC alquiler | 3,1 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-2` | GSADF (vc bootstrap AR): precio frente a valor de descuento del alquiler (tipo, g=2 %, prima 3 pp): IPV | 0,895 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-3` | GSADF (vc bootstrap AR): precio frente a valor de cuota hipotecaria constante sobre renta: IPV | 0,909 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-5` | GSADF (vc bootstrap AR): precio/renta: valor tasado / renta del hogar | 0,224 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-6` | GSADF (vc bootstrap AR): precio/alquiler: valor tasado / IPC alquiler | 4,34 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-7` | GSADF (vc bootstrap AR): precio frente a valor de descuento del alquiler (tipo, g=2 %, prima 3 pp): valor tasado | 0,161 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-8` | GSADF (vc bootstrap AR): precio frente a valor de cuota hipotecaria constante sobre renta: valor tasado | 0,516 | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-ccaa` | CCAA-medida con exuberancia tras BH (vc corregidos) de 34 | 7 series | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-tam` | Tamaño empírico del GSADF con vc iid cuando Δy es AR(1) con phi=0,5 (nominal 5 %) | 0,15 % | C4 | simulación T=78, R=200 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-G-tam-corr` | Tamaño empírico con vc por bootstrap de AR(p) estimado, phi=0,5 | 0,04 % | C4 | simulación T=78, R=200 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-S-BI-RV` | Valor de robustez Cinelli-Hazlett RV (q=1) de la forma reducida BI, gl=G-1 | 0,347 R² parcial | C4 | 2009-2021 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-S-BI-delta` | Oster δ (β*=0, Rmax=1,3·R²) de la forma reducida alquiler~instrumento Bartik, BI | 8,76 razón δ | C4 | 2009-2021 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-S-BI-mv` | BI: proporción de especificaciones con el mismo signo que la base (alquiler) | 0,963 | C4 | 2009-2021 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-S-BP-H6-RV` | BP H6 (resultado publicado, muestra sellada): RV aproximado desde τ y EE de placebo | 0,323 R² parcial | C4 | 2024Q3-2026Q2 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1B-S-BP-mv` | BP H5 SDiD: proporción de especificaciones con el mismo signo que la base (positivo) | 0,792 | C4 | 2012Q1-2022Q1 | [hechos.json](../output/v5/R1B/hechos.json) |
| `R1C-001` | Hogares con vivienda principal en propiedad | 74,5 % de hogares (72,1 a 75,9) | C1 | 2021-2022 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-002` | Hogares con otras propiedades (cualquier inmueble), tramo 65-74 | 61,6 % de hogares del tramo | C4 | 2022 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-003` | Hogares con otras propiedades (cualquier inmueble), tramo <35 | 15,3 % de hogares del tramo | C4 | 2022 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-004` | Compraventas con comprador persona juridica | 11,3 % de compraventas | C4 | 2024 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-010` | Ocupados en construccion por vivienda libre iniciada, nacional 2008 | 10,34 personas por vivienda | C4 | 2008 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-011` | Ocupados en construccion por vivienda libre iniciada, nacional 2013 | 35,22 personas por vivienda | C4 | 2013 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-012` | Ocupados en construccion por vivienda libre iniciada, nacional 2025 | 12,56 personas por vivienda | C4 | 2025 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-013` | Variacion 2014T1-2025T4 del coste de construccion (Eurostat) menos precio (tasacion BdE) | -18,8 puntos porcentuales (-65,7 a -18,8) | C4 | 2014T1-2025T4 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-020` | Entidades municipales con vacias y uso esporadico publicadas por el INE (Censo 2021, consumo electrico) | 3.185 entidades | C4 | 2021-11 | [hechos.json](../output/v5/R1C/hechos.json) |
| `R1C-021` | Mediana municipal del % de viviendas vacias (p10-p90 en min-max) | 17,4 % de viviendas (6,8 a 35,2) | C4 | 2021-11 | [hechos.json](../output/v5/R1C/hechos.json) |
| `HIST-008` | Peso inicial de no residentes · Subida del precio provincial | bivariada 0,0096 por pp; con controles 0,0002 | C4 | 2015-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-034` | Precio de compra: IPV frente a núcleo · % acumulado | IPV +79,9 %; núcleo +44,2 a +56,1 % | C4 | 2015-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `FICHA-A23-V1` | El alquiler se ha duplicado (variante stock: renta de los contratos vigentes). | CONTRADICHA | C1 |  | [alquiler_series_nacional_cataluna.csv](../output/v5/A23/tablas/alquiler_series_nacional_cataluna.csv) |
| `FICHA-A23-V2` | El alquiler se ha duplicado (variante contratos nuevos: renta de quien firma ahora). | ANALIZADA, NO CONCLUYENTE | C4 |  | [brecha_nuevo_stock_ccaa.csv](../output/v5/A23/tablas/brecha_nuevo_stock_ccaa.csv) |
| `FICHA-B1-V1` | Hacen falta X viviendas al año en España. | ANALIZADA, NO CONCLUYENTE | C4 |  | [B1_tabla_provincial.csv](../output/v5/B1/tablas/B1_tabla_provincial.csv) |
| `FICHA-B1-V2` | La vivienda que dejan los mayores resolverá el problema de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [B1_envejecimiento.csv](../output/v5/B1/tablas/B1_envejecimiento.csv) |
| `FICHA-B4-V1` | La subida se debe sobre todo a la inmigración. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_contribuciones_larga.csv](../output/v5/B4/tabla_contribuciones_larga.csv) |
| `FICHA-B4-V2` | La subida se debe a los pisos turísticos. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_contribuciones_larga.csv](../output/v5/B4/tabla_contribuciones_larga.csv) |
| `FICHA-B4-V3` | La subida se debe a la falta de oferta. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_contribuciones_larga.csv](../output/v5/B4/tabla_contribuciones_larga.csv) |
| `FICHA-B4-V4` | La subida se debe a los tipos de interés bajos. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_contribuciones_larga.csv](../output/v5/B4/tabla_contribuciones_larga.csv) |
| `FICHA-CA-V1` | La vivienda en España es más cara que en Europa. | ANALIZADA, NO CONCLUYENTE | C4 |  | [europa_posicion_es.csv](../output/v5/CA/tablas/europa_posicion_es.csv) |
| `FICHA-CA-V2` | La falta de crédito a promotores frena la oferta de vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [credito_iniciadas_retardos.csv](../output/v5/CA/tablas/credito_iniciadas_retardos.csv) |
| `FICHA-CA-V3` | La mayoría compra al contado. | ANALIZADA, NO CONCLUYENTE | C4 |  | [contado_ratio_hipotecas_compraventas.csv](../output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv) |
| `FICHA-CB-V1` | La ocupación ilegal reduce la oferta de alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |  | [CB-V1.json](../output/v5/verificador/fichas/CB-V1.json) |
| `FICHA-CB-V2` | La mayoría de los caseros son pequeños propietarios. | ANALIZADA, NO CONCLUYENTE | C4 |  | [CB-V2.json](../output/v5/verificador/fichas/CB-V2.json) |
| `FICHA-CB-V3` | Las empresas y fondos dominan el alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |  | [CB-V3.json](../output/v5/verificador/fichas/CB-V3.json) |
| `FICHA-CC-V1` | Sin ayuda familiar los jóvenes no pueden comprar vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [ecv_tenencia_16_29.csv](../output/v5/CC/tablas/ecv_tenencia_16_29.csv) |
| `FICHA-CC-V2` | Las viviendas protegidas se pierden por descalificación y el parque protegido se erosiona. | ANALIZADA, NO CONCLUYENTE | C4 |  | [salidas_nacional_2026_2035.csv](../output/v5/CC/tablas/salidas_nacional_2026_2035.csv) |
| `FICHA-D1-V1` | Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda. | PARCIALMENTE | C2 |  | [incidencia_ayudas_por_clase.csv](../output/v5/D1/incidencia_ayudas_por_clase.csv) |
| `FICHA-K1-V1` | Los modelos de inteligencia artificial predicen el precio y el alquiler mejor que los métodos sencillos. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_modelos_k1.md](../output/v6_1/K1/tabla_modelos_k1.md) |
| `FICHA-K2-V1` | La llegada de inmigrantes sube el precio de la vivienda o el alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |  | [inmigracion.md](../output/v6_1/K2/inmigracion.md) |
| `FICHA-L3-V1` | Faltan cientos de miles de viviendas en España. | PARCIALMENTE | C2 |  | [deficit_alternativas.md](../output/v6_2/L3/deficit_alternativas.md) |
| `FICHA-M3-V1` | Hay suelo de sobra para construir. | ANALIZADA, NO CONCLUYENTE | C4 |  | [clasificacion_provincias.csv](../output/v4/M3/clasificacion_provincias.csv) |
| `FICHA-M4-V3` | El alquiler y la compra se mueven por los mismos factores. | ANALIZADA, NO CONCLUYENTE | C4 |  | [tabla_modelos.csv](../output/v6/M4/tabla_modelos.csv) |
| `FICHA-M4-V4` | La ratio precio/alquiler indica sobrevaloracion. | ANALIZADA, NO CONCLUYENTE | C4 |  | [ratio_ult.csv](../output/v6/M1B/tablas/ratio_ult.csv) |
| `FICHA-M5-V2` | Faltan viviendas en toda España. | ANALIZADA, NO CONCLUYENTE | C4 |  | [hechos.json](../output/v4/M1/hechos.json) |
| `FICHA-M5-V3` | Los hogares crecen por la inmigración. | ANALIZADA, NO CONCLUYENTE | C4 |  | [hechos.json](../output/v4/M2/hechos.json) |
| `FICHA-M5-V4` | Limitar las compras de no residentes bajaría los precios de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [hechos.json](../output/v4/M4/hechos.json) |
| `FICHA-M5-V5` | Bajar los impuestos a la construcción abarataría la vivienda. | NO ANALIZADA: FALTAN DATOS | C4 |  | [M5-V5.json](../output/v5/verificador/fichas/M5-V5.json) |
| `FICHA-R1A-V1` | Los compradores extranjeros encarecen la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [no_residentes_regresiones.csv](../output/v5/R1A/tablas/no_residentes_regresiones.csv) |
| `FICHA-R1B-V1` | Hay una burbuja en el precio de la vivienda en España. | ANALIZADA, NO CONCLUYENTE | C4 |  | [gsadf_corregido.csv](../output/v5/R1B/tablas/gsadf_corregido.csv) |
| `FICHA-T1-V1` | En España apenas se derriban viviendas / las bajas del parque son despreciables. | ANALIZADA, NO CONCLUYENTE | C4 |  | [comparacion_metodos.csv](../output/v5_1/T1/tablas/comparacion_metodos.csv) |
| `FICHA-T2-V1` | El envejecimiento resolvera el problema de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [liberadas_provincia.csv](../output/v5_1/T2/tablas/liberadas_provincia.csv) |
| `FICHA-T2-V2` | Las herencias liberaran vivienda suficiente. | ANALIZADA, NO CONCLUYENTE | C4 |  | [liberadas_provincia.csv](../output/v5_1/T2/tablas/liberadas_provincia.csv) |
| `FICHA-T4-V1` | Al ritmo actual el déficit se cerrará en pocos años. | NO RESPALDADA | C2 |  | [recuento_por_etapas.csv](../output/v5_1/T4/tablas/recuento_por_etapas.csv) |
| `FICHA-V02` | Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres. | NO ANALIZADA: FALTAN DATOS | C4 |  | [solicitudes_transparencia.md](../docs/v3/solicitudes_transparencia.md) |
| `FICHA-V06` | Los topes al precio del alquiler bajan los alquileres. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resultado.json](../output/v3/C3/resultado.json) |
| `FICHA-V07` | Los topes al precio del alquiler reducen la oferta de vivienda en alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resultado.json](../output/v3/C3/resultado.json) |
| `FICHA-V08` | Hay millones de viviendas vacías que se podrían movilizar para resolver el problema. | ANALIZADA, NO CONCLUYENTE | C4 |  | [V08.json](../output/v5/verificador/fichas/V08.json) |
| `FICHA-V10` | Bajar el ITP o el IVA de la vivienda la abarataría para los compradores. | NO ANALIZADA: FALTAN DATOS | C4 |  | [V10.json](../output/v5/verificador/fichas/V10.json) |
| `FICHA-V11` | Construir vivienda pública resolvería el problema de la vivienda. | PARCIALMENTE | C2 |  | [resultados.json](../output/v3/PD/resultados.json) |

## Versión v5.1

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `T1-H1` | Bajas netas implícitas en la identidad Censo 2011 + terminadas - Censo 2021 (negativas) | -82.671 viviendas/año | C4 | 1-nov-2011 a 1-ene-2021 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H10` | Déficit contable 2021-2025 con bajas estimadas (ECP, con protegida) | 735.254 viviendas | C4 | 2021-2025 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H2` | Tasa anual implícita de la identidad de Censos (negativa) | -0,328 % del parque al año | C4 | 1-nov-2011 a 1-ene-2021 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H3` | Altas netas no explicadas por las terminadas del Ministerio | 757.814 viviendas (369.332 a 757.814) | C4 | 1-nov-2011 a 1-ene-2021 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H4` | Tasa anual Catastro-terminadas, territorio común (negativa) | -0,176 % del parque al año | C4 | 2012-2020 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H5` | Tasa anual Catastro-terminadas, territorio común | -0,0083 % del parque al año | C4 | 2019-2024 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H6` | Viviendas con licencia de demolición (total y parcial) al año | 6.200 viviendas/año (6.200 a 7.195) | C4 | media 2012-2024 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H7` | Viviendas con licencia de demolición en 2024 | 5.898 viviendas (5.898 a 9.706) | C4 | 2024 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H8` | Tasa anual de bajas (licencias de demolición, media 2015-2024) | 0,026 % del parque al año (0 a 0,052) | C4 | 2015-2024 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T1-H9` | Déficit contable 2021-2024 con bajas estimadas (ECP, con protegida) | 590.097 viviendas (562.692 a 618.144) | C4 | 2021-2024 | [hechos.json](../output/v5_1/T1/hechos.json) |
| `T2-H1` | Viviendas liberadas por fallecimiento del ultimo miembro y traslado a residencia, acumuladas | 1.856.430 viviendas (936.056 a 3.168.590) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H10` | Cuota de las liberadas (central) en provincias A4 clase 1-2 | 97,2 % | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H11` | Cuota en municipios A4 clase 1-2 sobre las liberadas en municipios con clase (703 municipios con precio) | 65,5 % | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H12` | Cuota de las liberadas en municipios sin clase A4 (sin precio) | 28,4 % | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H13` | Herencias de vivienda inscritas al ano (media 2023-2025) | 203.393 viviendas/año | C4 | 2023-2025 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H14` | Liberadas por fallecimiento en vivienda en propiedad al ano (modelo) | 118.074 viviendas/año | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H15` | Liberadas al ano frente a la necesidad central B1 (no se resta de ella) | 86,4 % (30,2 a 338,4) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H2` | Viviendas liberadas al ano (media) | 185.643 viviendas/año (93.606 a 316.859) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H3` | Viviendas liberadas por fallecimiento (formula B1 con correccion por muertes en residencia), acumuladas | 1.343.164 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H4` | Viviendas liberadas por traslado a residencia de quien vivia solo, acumuladas | 513.266 viviendas | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H5` | Escenario: viviendas liberadas acumuladas | 1.140.312 viviendas (575.802 a 1.944.232) | C4 | 2036-2040 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H6` | Viviendas liberadas que llegan al mercado (venta o alquiler), al ano | 150.079 viviendas/año (70.096 a 275.008) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H7` | Viviendas liberadas que NO llegan al mercado al ano (X data-based: vacias y secundarias del Censo 2021) | 35.564 viviendas/año (24.548 a 46.580) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H8` | Aumento posible de la necesidad efectiva (no_llega / necesidad central B1) | 16,6 % (11,4 a 21,7) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T2-H9` | Prueba de estres X=50 % (sin dato): aumento posible de la necesidad | 43,2 % | C4 | 2026-2035 | [hechos.json](../output/v5_1/T2/hechos.json) |
| `T3-H5` | Necesidad anual de vivienda 2026-2035 recalculada (A+R+V+F-M-K+X; no resta liberadas) | 245.989 viviendas/año (123.936 a 338.663) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T3-H5b` | Necesidad anual de vivienda 2026-2035, base sin la sensibilidad X (A+R+V+F-M-K; no resta liberadas) | 210.424 viviendas/año (99.388 a 292.083) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T3-H6` | Liberadas por envejecimiento que no llegan al mercado (componente que suma), por año | 35.564 viviendas/año (24.548 a 46.580) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T3-H7` | Reposición con las bajas de T1 (10 años) | 69.407 viviendas (0 a 140.447) | C4 | 2026-2035 | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T3-H8` | Amplitud conjunta (máx. - mín.) de la necesidad; mayor aporte: movilizables (M) | 214.727 viviendas/año | C4 | 2026-2035 | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T3-H9` | Veces que cabe la producción actual (terminadas nacionales con País Vasco y Navarra, media 2019-2024) en la necesidad anual con s… | 2,7 veces (1,4 a 3,8) | C4 | 2019-2024 (producción) | [hechos.json](../output/v5_1/T3/hechos.json) |
| `T4-H1` | Déficit acumulado nacional a fin de 2030 (magnitud; mín., central ritmo actual y máx. de la rejilla) | 1.349.025 viviendas (788.180 a 1.773.555) | C4 | 2021-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H2` | Cambio del déficit 2025 a 2030 (nacional; mín. y máx. de la rejilla) | 585.609 viviendas (87.246 a 946.852) | C4 | 2026-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H3` | Dirección nacional del déficit 2025-2030 en toda la rejilla (empeora); provincias que empeoran / mejoran / indeterminadas | 15 provincias (0 a 37) | C2 | 2025-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H4` | Provincias que empeoran / mejoran / indeterminadas en B2 (rango sin las variantes nuevas) | 20 provincias (5 a 27) | C4 | 2025-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H5` | Déficit acumulado nacional a fin de 2035 (escenario; mín., central y máx.) | 1.606.859 viviendas (482.095 a 2.400.412) | C4 | 2021-2035 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H6` | Terminadas por año necesarias para mantener constante el déficit 2026-2030 (hogares INE central + bajas T1 central) | 211.772 viviendas/año (163.884 a 245.193) | C4 | 2026-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H7` | Terminadas por año del escenario optimista (máximo plausible; media de provincias sumadas) | 146.435 viviendas/año (94.650 a 146.435) | C4 | 2026-2030 | [hechos.json](../output/v5_1/T4/hechos.json) |
| `T4-H8` | Viviendas liberadas por envejecimiento, 2031-2035 frente a 2026-2030 (central, T2 repartido por defunciones de 75+) | 986.777 viviendas (869.654 a 986.777) | C4 | 2031-2035 (valor y max) / 2026-2030 (mi… | [hechos.json](../output/v5_1/T4/hechos.json) |

## Versión v6

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `M0-SELLADO` | Filas selladas (no abiertas) por panel | 59.367 filas | C4 | ver output/v6/M0/sellado.md | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-dis_alquiler_anual` | Panel de modelización dis_alquiler_anual: unidades y años de entrenamiento | 40.673 filas | C4 | 2011-2023 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-mun_alquiler_anual` | Panel de modelización mun_alquiler_anual: unidades y años de entrenamiento | 18.181 filas | C4 | 2015-2023 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-mun_compra_anual` | Panel de modelización mun_compra_anual: unidades y años de entrenamiento | 20.530 filas | C4 | 2015-2024 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-mun_contratos_anual` | Panel de modelización mun_contratos_anual: unidades y años de entrenamiento | 18.181 filas | C4 | 2015-2023 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-prov_alquiler_anual` | Panel de modelización prov_alquiler_anual: unidades y años de entrenamiento | 369 filas | C4 | 2015-2023 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-prov_compra_anual` | Panel de modelización prov_compra_anual: unidades y años de entrenamiento | 410 filas | C4 | 2015-2024 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-prov_contratos_nuevos_anual` | Panel de modelización prov_contratos_nuevos_anual: unidades y años de entrenamiento | 369 filas | C4 | 2015-2023 | [hechos.json](../output/v6/M0/hechos.json) |
| `M0-prov_trim_compra` | Panel de modelización prov_trim_compra: unidades y años de entrenamiento | 1.640 filas | C4 | 2015-2024 | [hechos.json](../output/v6/M0/hechos.json) |
| `V6-M4-N-REL` | Variables 'relevante con seguridad' (criterios A y B pre-registrados), alquiler y compra | 0 variables | C4 | entrenamiento 2015-2024 y sellado v6 | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-MUN_PRECIO_ANUAL` | RMSE espacial sellado de la persistencia, compra (precio), municipio (anual) | 6,33 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-PROV_PRECIO_ANUAL` | RMSE espacial sellado de la persistencia, compra (precio), provincia (anual) | 3,96 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-PROV_PRECIO_ANUAL_REGISTRADORES` | RMSE espacial sellado de la persistencia, compra (precio), provincia (anual) | 6,03 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-PROV_PRECIO_TRIM` | RMSE espacial sellado de la persistencia, compra (precio), provincia (trimestral) | 1,93 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-PROV_VOL_ANUAL` | RMSE espacial sellado de la persistencia, compra (volumen), provincia (anual) | 15,86 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-PROV_VOL_TRIM` | RMSE espacial sellado de la persistencia, compra (volumen), provincia (trimestral) | 18,46 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-alq_distrito` | RMSE espacial sellado de la persistencia, alquiler de stock (SERPAVI), distrito | 6,98 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-alq_municipio` | RMSE espacial sellado de la persistencia, alquiler de stock (SERPAVI), municipio | 6,51 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-PERS-alq_provincia` | RMSE espacial sellado de la persistencia, alquiler de stock (SERPAVI), provincia | 4,21 log-puntos x100 | C4 | validacion sellada v6 (11 provincias) | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-MUN_PRECIO_ANUAL` | RMSE espacial sellado del mejor modelo (MUN_PRECIO_ANUAL__ecm_v1), compra (precio), municipio (anual), medida ln_pm2_tasado_mun (… | 3,93 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-PROV_PRECIO_ANUAL` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_ANUAL__random_forest), compra (precio), provincia (anual), medida ln_pm2_tasa… | 2,48 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-PROV_PRECIO_ANUAL_REGISTRADORES` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_ANUAL_REGISTRADORES__ecm_v1), compra (precio), provincia (anual), medida ln_p… | 4,68 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-PROV_PRECIO_TRIM` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano), compra (precio), provincia (trimestral), m… | 1,61 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-PROV_VOL_ANUAL` | RMSE espacial sellado del mejor modelo (PROV_VOL_ANUAL__bosque_bootstrap_bayesiano), compra (volumen), provincia (anual), medida… | 13,04 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-PROV_VOL_TRIM` | RMSE espacial sellado del mejor modelo (PROV_VOL_TRIM__bosque_bootstrap_bayesiano), compra (volumen), provincia (trimestral), med… | 11,3 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-alq_distrito` | RMSE espacial sellado del mejor modelo (alquiler_distrito_gb), alquiler de stock (SERPAVI), distrito, medida ln_alq_m2_serpavi_di… | 5,6 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-alq_municipio` | RMSE espacial sellado del mejor modelo (alquiler_municipio_rf), alquiler de stock (SERPAVI), municipio, medida ln_alq_m2_serpavi_… | 5,07 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `V6-M4-RMSE-alq_provincia` | RMSE espacial sellado del mejor modelo (alquiler_provincia_gb), alquiler de stock (SERPAVI), provincia, medida ln_alq_m2_serpavi_… | 1,61 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, 2… | [hechos.json](../output/v6/M4/hechos.json) |
| `m1a_distrito_S0_ln_pib_pc` | Alquiler de stock (distrito): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,21 EUR/mes (-3,58 a 3,19) | C4 | 2022.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_distrito_S0_ln_vut_plazas_dis` | Alquiler de stock (distrito): +100 plazas turísticas en el distrito; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,01 EUR/mes (-1,11 a 1,14) | C4 | 2022.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_distrito_S1_ln_pib_pc` | Alquiler de stock (distrito): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,92 EUR/mes (-4,17 a 2,35) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_ln_iniciadas_libres` | Alquiler de stock (municipio): +1.000 viviendas libres iniciadas; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,67 EUR/mes (-1,92 a 0,57) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_ln_pib_pc` | Alquiler de stock (municipio): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,5 EUR/mes (-1,37 a 0,37) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_ln_pob` | Alquiler de stock (municipio): +10.000 habitantes; asociacion con el alquiler SERPAVI, regresor en t-1 | 2,25 EUR/mes (0,04 a 4,47) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_ln_terminadas_libres` | Alquiler de stock (municipio): +1.000 viviendas libres terminadas; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,06 EUR/mes (-0,96 a 1,08) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_ln_vut` | Alquiler de stock (municipio): +1.000 viviendas turísticas; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,16 EUR/mes (-0,98 a 0,65) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_share_ext_pob` | Alquiler de stock (municipio): +1 punto de población extranjera; asociacion con el alquiler SERPAVI, regresor en t-1 | 4,97 EUR/mes (-6,82 a 17,13) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S0_tope_cat_mun` | Alquiler de stock (municipio): municipio pasa a tope; asociacion con el alquiler SERPAVI, regresor en t-1 | 4,36 EUR/mes (-0,38 a 9,16) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_ln_iniciadas_libres` | Alquiler de stock (municipio): +1.000 viviendas libres iniciadas; asociacion con el alquiler SERPAVI, regresor en t-1 | 1,23 EUR/mes (0,26 a 2,21) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_ln_pib_pc` | Alquiler de stock (municipio): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | 1,37 EUR/mes (-0,3 a 3,05) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_ln_pob` | Alquiler de stock (municipio): +10.000 habitantes; asociacion con el alquiler SERPAVI, regresor en t-1 | 2,14 EUR/mes (0,62 a 3,66) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_ln_terminadas_libres` | Alquiler de stock (municipio): +1.000 viviendas libres terminadas; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,18 EUR/mes (-1,67 a 2,04) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_share_ext_pob` | Alquiler de stock (municipio): +1 punto de población extranjera; asociacion con el alquiler SERPAVI, regresor en t-1 | 1,39 EUR/mes (-3,21 a 6,06) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_municipio_S1_tope_cat_mun` | Alquiler de stock (municipio): municipio pasa a tope; asociacion con el alquiler SERPAVI, regresor en t-1 | -1,54 EUR/mes (-4,01 a 0,95) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_ln_iniciadas_libres` | Alquiler de stock (provincia): +1.000 viviendas libres iniciadas; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,17 EUR/mes (-1,97 a 1,64) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_ln_pib_pc` | Alquiler de stock (provincia): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,05 EUR/mes (-1,69 a 1,79) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_ln_pob` | Alquiler de stock (provincia): +10.000 habitantes; asociacion con el alquiler SERPAVI, regresor en t-1 | 4,63 EUR/mes (1,14 a 8,14) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_ln_terminadas_libres` | Alquiler de stock (provincia): +1.000 viviendas libres terminadas; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,85 EUR/mes (-1,97 a 0,27) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_ln_vut` | Alquiler de stock (provincia): +1.000 viviendas turísticas; asociacion con el alquiler SERPAVI, regresor en t-1 | -1,58 EUR/mes (-6,6 a 3,5) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_n_mun_topes_cat` | Alquiler de stock (provincia): +1 municipio con tope; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,18 EUR/mes (-0,11 a 0,47) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S0_share_ext_pob` | Alquiler de stock (provincia): +1 punto de población extranjera; asociacion con el alquiler SERPAVI, regresor en t-1 | 5,45 EUR/mes (-4,27 a 15,39) | C4 | 2021.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_ln_iniciadas_libres` | Alquiler de stock (provincia): +1.000 viviendas libres iniciadas; asociacion con el alquiler SERPAVI, regresor en t-1 | 2,21 EUR/mes (-2,31 a 6,78) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_ln_pib_pc` | Alquiler de stock (provincia): +1.000 EUR de PIB por habitante; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,75 EUR/mes (-0,99 a 2,5) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_ln_pob` | Alquiler de stock (provincia): +10.000 habitantes; asociacion con el alquiler SERPAVI, regresor en t-1 | 5,07 EUR/mes (3,1 a 7,04) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_ln_terminadas_libres` | Alquiler de stock (provincia): +1.000 viviendas libres terminadas; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,05 EUR/mes (-4 a 4,15) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_n_mun_topes_cat` | Alquiler de stock (provincia): +1 municipio con tope; asociacion con el alquiler SERPAVI, regresor en t-1 | -0,09 EUR/mes (-0,36 a 0,19) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1a_provincia_S1_share_ext_pob` | Alquiler de stock (provincia): +1 punto de población extranjera; asociacion con el alquiler SERPAVI, regresor en t-1 | 0,05 EUR/mes (-6,46 a 6,66) | C4 | 2016.0-2023.0 | [hechos.json](../output/v6/M1A/hechos.json) |
| `m1b_brecha_rentabilidad_coste_uso` | Rentabilidad bruta menos coste de uso (g=2 %), mediana provincial | 1,56 pp | C4 | 2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_coste_uso_g2` | Coste de uso anual (tipo hipotecario ECB + 2,0 % depreciación y mantenimiento + 0,5 % impuestos - 2 % ganancia esperada; SUPUESTO… | 4,28 % del valor | C4 | 2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_anual_FE_unidad_año` | Elasticidad precio tasado - alquiler (FE_unidad+año, asociación) | 1,33 elasticidad (0,811 a 1,85) | C4 | 2015-2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_anual_FE_unidad_año_v2` | Elasticidad precio tasado - alquiler (FE_unidad+año, asociación) | 1,31 elasticidad (0,93 a 1,7) | C4 | 2015-2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_anual_FE_unidad_tendencia` | Elasticidad precio tasado - alquiler (FE_unidad+tendencia, asociación) | 0,594 elasticidad (0,439 a 0,749) | C4 | 2015-2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_anual_FE_unidad_tendencia_v2` | Elasticidad precio tasado - alquiler (FE_unidad+tendencia, asociación) | 0,434 elasticidad (0,177 a 0,691) | C4 | 2015-2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_trimestral_DOLS_FE_unidad_tendencia` | Elasticidad precio tasado - alquiler (DOLS_FE_unidad+tendencia, asociación) | 2,12 elasticidad (1,85 a 2,4) | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_elasticidad_trimestral_DOLS_FE_unidad_trimestreentreprovincias` | Elasticidad precio tasado - alquiler (DOLS_FE_unidad+trimestre(entre provincias), asociación) | 1,62 elasticidad (1,17 a 2,07) | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_hip_viv_num` | Variación asociada en el valor tasado de ln_hip_viv_num (t-1): % por +10 % (logs) o +1 pp | -0,426 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_iniciadas_libres` | Variación asociada en el valor tasado de ln_iniciadas_libres (t-1): % por +10 % (logs) o +1 pp | 0,009 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_ocupados_miles` | Variación asociada en el valor tasado de ln_ocupados_miles (t-1): % por +10 % (logs) o +1 pp | -1,23 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_pib_pc` | Variación asociada en el valor tasado de ln_pib_pc (t-1): % por +10 % (logs) o +1 pp | 1,34 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_pob` | Variación asociada en el valor tasado de ln_pob (t-1): % por +10 % (logs) o +1 pp | 26,52 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_ln_terminadas_libres` | Variación asociada en el valor tasado de ln_terminadas_libres (t-1): % por +10 % (logs) o +1 pp | 0,119 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_paro_tasa` | Variación asociada en el valor tasado de paro_tasa (t-1): % por +10 % (logs) o +1 pp | -0,351 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_fe_precio_share_ext_pob` | Variación asociada en el valor tasado de share_ext_pob (t-1): % por +10 % (logs) o +1 pp | -1,3 % | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_01` | GSADF ratio precio/IPC alquiler, CCAA 01: p bootstrap (episodios: ) | 1,74 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_06` | GSADF ratio precio/IPC alquiler, CCAA 06: p bootstrap (episodios: ) | 0,285 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_07` | GSADF ratio precio/IPC alquiler, CCAA 07: p bootstrap (episodios: ) | 0,897 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_08` | GSADF ratio precio/IPC alquiler, CCAA 08: p bootstrap (episodios: ) | 0,983 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_09` | GSADF ratio precio/IPC alquiler, CCAA 09: p bootstrap (episodios: ) | 0,195 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_10` | GSADF ratio precio/IPC alquiler, CCAA 10: p bootstrap (episodios: ) | 0,779 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_11` | GSADF ratio precio/IPC alquiler, CCAA 11: p bootstrap (episodios: ) | 0,333 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_12` | GSADF ratio precio/IPC alquiler, CCAA 12: p bootstrap (episodios: ) | 1,09 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_16` | GSADF ratio precio/IPC alquiler, CCAA 16: p bootstrap (episodios: ) | -1,05 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_18` | GSADF ratio precio/IPC alquiler, CCAA 18: p bootstrap (episodios: ) | -0,422 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_gsadf_ccaa_19` | GSADF ratio precio/IPC alquiler, CCAA 19: p bootstrap (episodios: ) | 0,417 | C4 | 2015T1-2024T4 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_ratio_precio_alquiler_mediana` | Ratio precio/alquiler anual, mediana provincial (valor tasado / alquiler de stock anualizado) | 17,12 años de alquiler (15,33 a 18,84) | C4 | 2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_ratio_precio_alquiler_mediana_2015` | Ratio precio/alquiler anual, mediana provincial | 20,33 años de alquiler (18,85 a 21,98) | C4 | 2015 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_rentabilidad_bruta_mediana` | Rentabilidad bruta por alquiler, mediana provincial | 5,84 % del valor tasado | C4 | 2023 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_sdm_rho_ln_cv_etdp` | Autocorrelación espacial (Durbin espacial, W 4 vecinos) de ln_cv_etdp | 0,117  (-0,036 a 0,27) | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m1b_sdm_rho_ln_pm2_tasado` | Autocorrelación espacial (Durbin espacial, W 4 vecinos) de ln_pm2_tasado | 0,275  (0,142 a 0,409) | C4 | 2016-2024 | [hechos.json](../output/v6/M1B/hechos.json) |
| `m2_pip_alq_ln_iniciadas_libres` | PIP BMA de ln_iniciadas_libres, alquiler de stock (SERPAVI), provincia | 0,089 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_ln_pib_pc` | PIP BMA de ln_pib_pc, alquiler de stock (SERPAVI), provincia | 0,097 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_ln_pob` | PIP BMA de ln_pob, alquiler de stock (SERPAVI), provincia | 1 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_ln_terminadas_libres` | PIP BMA de ln_terminadas_libres, alquiler de stock (SERPAVI), provincia | 0,169 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_ln_vut` | PIP BMA de ln_vut, alquiler de stock (SERPAVI), provincia | 0,116 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_n_mun_topes_cat` | PIP BMA de n_mun_topes_cat, alquiler de stock (SERPAVI), provincia | 0,231 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_alq_share_ext_pob` | PIP BMA de share_ext_pob, alquiler de stock (SERPAVI), provincia | 0,297 | C4 | 2015-2023 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_hip_viv_num` | PIP BMA de ln_hip_viv_num, precio de compra (tasado MIVAU), provincia | 0,122 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_iniciadas_libres` | PIP BMA de ln_iniciadas_libres, precio de compra (tasado MIVAU), provincia | 0,124 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_ocupados_miles` | PIP BMA de ln_ocupados_miles, precio de compra (tasado MIVAU), provincia | 0,196 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_pib_pc` | PIP BMA de ln_pib_pc, precio de compra (tasado MIVAU), provincia | 0,844 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_pob` | PIP BMA de ln_pob, precio de compra (tasado MIVAU), provincia | 0,763 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_suelo_pm2_m50k` | PIP BMA de ln_suelo_pm2_m50k, precio de compra (tasado MIVAU), provincia | 0,145 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_terminadas_libres` | PIP BMA de ln_terminadas_libres, precio de compra (tasado MIVAU), provincia | 0,116 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_ln_vut` | PIP BMA de ln_vut, precio de compra (tasado MIVAU), provincia | 0,095 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_paro_tasa` | PIP BMA de paro_tasa, precio de compra (tasado MIVAU), provincia | 0,131 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cp_share_ext_pob` | PIP BMA de share_ext_pob, precio de compra (tasado MIVAU), provincia | 0,308 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_hip_viv_num` | PIP BMA de ln_hip_viv_num, volumen de compra (INE ETDP), provincia | 0,091 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_iniciadas_libres` | PIP BMA de ln_iniciadas_libres, volumen de compra (INE ETDP), provincia | 0,977 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_ocupados_miles` | PIP BMA de ln_ocupados_miles, volumen de compra (INE ETDP), provincia | 0,102 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_pib_pc` | PIP BMA de ln_pib_pc, volumen de compra (INE ETDP), provincia | 0,093 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_pob` | PIP BMA de ln_pob, volumen de compra (INE ETDP), provincia | 0,098 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_suelo_pm2_m50k` | PIP BMA de ln_suelo_pm2_m50k, volumen de compra (INE ETDP), provincia | 0,096 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_terminadas_libres` | PIP BMA de ln_terminadas_libres, volumen de compra (INE ETDP), provincia | 0,113 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_ln_vut` | PIP BMA de ln_vut, volumen de compra (INE ETDP), provincia | 0,138 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_paro_tasa` | PIP BMA de paro_tasa, volumen de compra (INE ETDP), provincia | 0,224 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m2_pip_cv_share_ext_pob` | PIP BMA de share_ext_pob, volumen de compra (INE ETDP), provincia | 0,112 | C4 | 2015-2024 | [hechos.json](../output/v6/M2/hechos.json) |
| `m3a_rmse_ar_distrito` | RMSE de AR por unidad, misma muestra, distrito | 0,105 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3a_rmse_ar_municipio` | RMSE de AR por unidad, misma muestra, municipio | 0,076 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3a_rmse_ar_provincia` | RMSE de AR por unidad, misma muestra, provincia | 0,03 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3a_rmse_distrito` | RMSE de validacion interna del mejor modelo de ML (gb), alquiler de stock, distrito (variacion anual de ln EUR/m2) | 0,048 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3a_rmse_municipio` | RMSE de validacion interna del mejor modelo de ML (gb), alquiler de stock, municipio (variacion anual de ln EUR/m2) | 0,046 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3a_rmse_provincia` | RMSE de validacion interna del mejor modelo de ML (rf), alquiler de stock, provincia (variacion anual de ln EUR/m2) | 0,01 log-puntos | C4 | 2018-2023 (pliegues) | [hechos.json](../output/v6/M3A/hechos.json) |
| `m3b_MUN_PRECIO_ANUAL_rmse_pct_ADL` | MUN_PRECIO_ANUAL: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 8,8 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_MUN_PRECIO_ANUAL_rmse_pct_AR` | MUN_PRECIO_ANUAL: RMSE % AR, validación por bloques con embargo | 8,95 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_MUN_PRECIO_ANUAL_rmse_pct_mejor_ML` | MUN_PRECIO_ANUAL: RMSE % del mejor ML (BBF), validación por bloques con embargo | 4,98 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_ADL` | PROV_PRECIO_ANUAL_REGISTRADORES: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 6,85 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_AR` | PROV_PRECIO_ANUAL_REGISTRADORES: RMSE % AR, validación por bloques con embargo | 7,18 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_REGISTRADORES_rmse_pct_mejor_ML` | PROV_PRECIO_ANUAL_REGISTRADORES: RMSE % del mejor ML (BBF), validación por bloques con embargo | 4,19 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_rmse_pct_ADL` | PROV_PRECIO_ANUAL: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 4,12 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_rmse_pct_AR` | PROV_PRECIO_ANUAL: RMSE % AR, validación por bloques con embargo | 4,12 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_ANUAL_rmse_pct_mejor_ML` | PROV_PRECIO_ANUAL: RMSE % del mejor ML (RF), validación por bloques con embargo | 2,67 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_TRIM_rmse_pct_ADL` | PROV_PRECIO_TRIM: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 3,51 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_TRIM_rmse_pct_AR` | PROV_PRECIO_TRIM: RMSE % AR, validación por bloques con embargo | 3,55 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_PRECIO_TRIM_rmse_pct_mejor_ML` | PROV_PRECIO_TRIM: RMSE % del mejor ML (BBF), validación por bloques con embargo | 1,93 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_ANUAL_rmse_pct_ADL` | PROV_VOL_ANUAL: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 28,17 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_ANUAL_rmse_pct_AR` | PROV_VOL_ANUAL: RMSE % AR, validación por bloques con embargo | 28,71 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_ANUAL_rmse_pct_mejor_ML` | PROV_VOL_ANUAL: RMSE % del mejor ML (BBF), validación por bloques con embargo | 19,9 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_TRIM_rmse_pct_ADL` | PROV_VOL_TRIM: RMSE % M1b_ADL (FE agrupado), validación por bloques con embargo | 67,79 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_TRIM_rmse_pct_AR` | PROV_VOL_TRIM: RMSE % AR, validación por bloques con embargo | 53,85 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `m3b_PROV_VOL_TRIM_rmse_pct_mejor_ML` | PROV_VOL_TRIM: RMSE % del mejor ML (BBF), validación por bloques con embargo | 25,66 % | C4 | orígenes 2018/2020/2022 | [hechos.json](../output/v6/M3B/hechos.json) |
| `HIST-009` | Cuota de extranjeros (t-1) · Alquiler SERPAVI (stock); valor tasado | alquiler +0,05 €/mes [−6,46; 6,66]; compra −1,3 % por pp (p WCB 0,43) | C4 | 2016-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-021` | Turísticos (VUT) · Alquiler SERPAVI; valor tasado | −1,58 €/mes por 1.000 [−6,6; 3,5]; municipio −0,16; PIP 0,12 / 0,10 | C4 | 2021-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-024` | Tipos / coste de uso · Cota del coste; rentabilidad | Δln(1/uc) hasta +78 % (2014-2021) y −20,5 % (2021-2025); coste de uso 4,28 % y rentabilid… | C4 | 2014-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-033` | Exuberancia (burbuja) · GSADF sobre ratio precio/alquiler | nacional: estadísticos GSADF 3,10-4,82 (veredicto en la fuente, no reverificado en K2); C… | C4 | 2015T1-2024T4 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-035` | Elasticidad precio-alquiler · Valor tasado frente a SERPAVI | 0,43-1,33 (FE); 1,6-2,1 (DOLS trimestral); ratio P/A 20,3 → 17,1 años | C4 | 2015-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-038` | Modelos de ML · RMSE sellado (11 provincias, último año) | mejor modelo: alquiler provincia 1,61 frente a 4,21 de la persistencia; ninguna variable… | C4 | 2024-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Versión v6.1

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `K1-BASE-MUN_PRECIO_ANUAL` | RMSE espacial sellado de la base mas exigente (ecm_v1), compra (precio), municipio (anual), medida de precio: valor tasado MIVAU… | 3,93 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-PROV_PRECIO_ANUAL` | RMSE espacial sellado de la base mas exigente (ecm_v1), compra (precio), provincia (anual), medida de precio: valor tasado MIVAU | 2,82 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-PROV_PRECIO_ANUAL_REGISTRADORES` | RMSE espacial sellado de la base mas exigente (ecm_v1), compra (precio), provincia (anual), medida de precio: Registradores (robu… | 4,68 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-PROV_PRECIO_TRIM` | RMSE espacial sellado de la base mas exigente (ar_factor_fac), compra (precio), provincia (trimestral), medida de precio: valor t… | 1,82 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-PROV_VOL_ANUAL` | RMSE espacial sellado de la base mas exigente (ecm_v1), compra (volumen), provincia (anual) | 13,7 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-PROV_VOL_TRIM` | RMSE espacial sellado de la base mas exigente (ar_factor_fac), compra (volumen), provincia (trimestral) | 16,74 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-alq_distrito` | RMSE espacial sellado de la base mas exigente (ecm_v1), alquiler de stock (SERPAVI), distrito | 6,12 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-alq_municipio` | RMSE espacial sellado de la base mas exigente (ar_factor_fac), alquiler de stock (SERPAVI), municipio | 5,43 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-BASE-alq_provincia` | RMSE espacial sellado de la base mas exigente (ar_factor_fac), alquiler de stock (SERPAVI), provincia | 2,2 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-N-MEJOR` | Tareas en que el mejor modelo predice mejor que la base mas exigente (DM-HLN y permutacion, Holm, grupo espacial) | 6 tareas | C4 | validacion sellada v6 | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-N-TAREAS` | Tareas comparadas en la validacion sellada v6 (K1) | 9 tareas | C4 | validacion sellada v6 | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-MUN_PRECIO_ANUAL` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (precio), municipio (anual), medida de precio: valor tasado M… | 1,05 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-PROV_PRECIO_ANUAL` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (precio), provincia (anual), medida de precio: valor tasado M… | 0,879 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-PROV_PRECIO_ANUAL_REGISTRADORES` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (precio), provincia (anual), medida de precio: Registradores… | 1 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-PROV_PRECIO_TRIM` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (precio), provincia (trimestral), medida de precio: valor tas… | 0,888 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-PROV_VOL_ANUAL` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (volumen), provincia (anual) | 0,952 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-PROV_VOL_TRIM` | Cociente de RMSE espacial, mejor modelo / base mas exigente, compra (volumen), provincia (trimestral) | 0,675 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-alq_distrito` | Cociente de RMSE espacial, mejor modelo / base mas exigente, alquiler de stock (SERPAVI), distrito | 0,915 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-alq_municipio` | Cociente de RMSE espacial, mejor modelo / base mas exigente, alquiler de stock (SERPAVI), municipio | 0,93 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RATIO-alq_provincia` | Cociente de RMSE espacial, mejor modelo / base mas exigente, alquiler de stock (SERPAVI), provincia | 0,729 cociente | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-MUN_PRECIO_ANUAL` | RMSE espacial sellado del mejor modelo (MUN_PRECIO_ANUAL__bosque_bootstrap_bayesiano), compra (precio), municipio (anual), medida… | 4,13 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-PROV_PRECIO_ANUAL` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_ANUAL__random_forest), compra (precio), provincia (anual), medida de precio:… | 2,48 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-PROV_PRECIO_ANUAL_REGISTRADORES` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_ANUAL_REGISTRADORES__bosque_bootstrap_bayesiano), compra (precio), provincia… | 4,7 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-PROV_PRECIO_TRIM` | RMSE espacial sellado del mejor modelo (PROV_PRECIO_TRIM__bosque_bootstrap_bayesiano), compra (precio), provincia (trimestral), m… | 1,61 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-PROV_VOL_ANUAL` | RMSE espacial sellado del mejor modelo (PROV_VOL_ANUAL__bosque_bootstrap_bayesiano), compra (volumen), provincia (anual) | 13,04 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-PROV_VOL_TRIM` | RMSE espacial sellado del mejor modelo (PROV_VOL_TRIM__bosque_bootstrap_bayesiano), compra (volumen), provincia (trimestral) | 11,3 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-alq_distrito` | RMSE espacial sellado del mejor modelo (alquiler_distrito_gb), alquiler de stock (SERPAVI), distrito | 5,6 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-alq_municipio` | RMSE espacial sellado del mejor modelo (alquiler_municipio_gb), alquiler de stock (SERPAVI), municipio | 5,05 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K1-RMSE-alq_provincia` | RMSE espacial sellado del mejor modelo (alquiler_provincia_gb), alquiler de stock (SERPAVI), provincia | 1,61 log-puntos x100 | C4 | validacion sellada v6 (11 provincias, g… | [hechos.json](../output/v6_1/K1/hechos.json) |
| `K2-CORR-POB-CONJUNTA` | Correlacion conjunta entre la cuota de extranjeros (t-1) y el ln de la poblacion (t-1) | 0,138 correlacion | C4 | 2016-2024 | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CORR-POB-DENTRO` | Correlacion dentro de provincia (EF dobles) entre la cuota de extranjeros (t-1) y el ln de la poblacion (t-1) | 0,664 correlacion | C4 | 2016-2024 | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-ALQ-NUCLEO-EXT` | Idem con controles de demanda externa | 0,301 % por pp (-1,3 a 1,9) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-ALQ-NUCLEO-SIN` | Cuota de extranjeros (t-1) y alquiler SERPAVI, EF dobles, con nucleo (poblacion incluida), sin demanda externa | 0,178 % por pp (-1,48 a 1,83) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-ALQ-SINPOB-EXT` | Idem con controles de demanda externa | 1,55 % por pp (0,052 a 3,05) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-ALQ-SINPOB-SIN` | Cuota de extranjeros (t-1) y alquiler de stock SERPAVI, EF dobles, sin controles y sin demanda externa | 2,67 % por pp (1,31 a 4,04) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-COMPRA-EXT` | Idem con controles de demanda externa (costa x anio, vivienda no principal x anio, compras de extranjeros residentes) | -1,42 % por pp (-4,37 a 1,52) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-COMPRA-SIN` | Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, con nucleo de controles (poblacion incluida), sin controles de demand… | -1,31 % por pp (-4,31 a 1,69) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-COMPRA-SINPOB-EXT` | Idem sin poblacion, con controles de demanda externa | 1,6 % por pp (-0,788 a 3,99) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K2-CUOTA-COMPRA-SINPOB-SIN` | Cuota de extranjeros (t-1) y valor tasado MIVAU, EF dobles, sin controles (sin poblacion) y sin demanda externa | 4,26 % por pp (2,12 a 6,41) | C4 | 2016-2024 (compra), 2016-2023 (alquiler) | [hechos.json](../output/v6_1/K2/hechos.json) |
| `K3-INI-A-ini_1000` | Iniciadas ini_1000 sobre Δln alquiler (EF) | 0,0027 coef. (0,0001 a 0,0052) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-A-ini_f1` | Iniciadas ini_f1 sobre Δln alquiler (EF) | -0,0002 coef. (-0,0017 a 0,0014) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-A-ini_f2` | Iniciadas ini_f2 sobre Δln alquiler (EF) | 0,0007 coef. (-0,0016 a 0,0031) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-A-ini_l1` | Iniciadas ini_l1 sobre Δln alquiler (EF) | -0,0007 coef. (-0,0035 a 0,0021) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-A-ini_l2` | Iniciadas ini_l2 sobre Δln alquiler (EF) | -0,0013 coef. (-0,004 a 0,0014) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-B-dlna_l1` | Iniciadas_t sobre dlna_l1 (EF) | 0,028 coef. (-14,43 a 14,48) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-INI-B-dlna_l2` | Iniciadas_t sobre dlna_l2 (EF) | 2,92 coef. (-8,93 a 14,78) | C4 | 2016-2023 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-RATIO-2015` | Ratio precio/alquiler, medida v6 (tasado/stock); min-max con las demás medidas de precio provinciales | 20,33 años de alquiler (18,93 a 20,33) | C4 | 2015 | [hechos.json](../output/v6_1/K3/hechos.json) |
| `K3-RATIO-2023` | Ratio precio/alquiler, medida v6 (tasado/stock); min-max con las demás medidas de precio provinciales | 17,12 años de alquiler (17,12 a 17,73) | C4 | 2023 | [hechos.json](../output/v6_1/K3/hechos.json) |

## Versión v6.2

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `L3-DEF-2124-BAJAST1` | Déficit acumulado 2021-2024 con las bajas del parque estimadas en v5.1 (T1), todas las variantes | 654.646 viviendas (389.361 a 765.994) | C4 | 2021-2024 | [hechos.json](../output/v6_2/L3/hechos.json) |
| `L3-DEF-2124-SENS` | Sensibilidad: déficit 2021-2024 sin bajas sin las dos variantes que conservan el salto de la EPA (a y d1) | 653.456 viviendas (596.371 a 710.542) | C2 | 2021-2024 | [hechos.json](../output/v6_2/L3/hechos.json) |
| `L3-DEF-2124-SINBAJAS` | Déficit acumulado 2021-2024 sin bajas (todas las variantes de corrección EPA y de terminadas) | 549.952 viviendas (389.361 a 710.542) | C2 | 2021-2024 | [hechos.json](../output/v6_2/L3/hechos.json) |
| `L3-DEF-2125` | Déficit acumulado 2021-2025 sin bajas (todas las variantes) | 705.778 viviendas (523.606 a 887.950) | C4 | 2021-2025 | [hechos.json](../output/v6_2/L3/hechos.json) |

## Versión v6.3

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `VER-A23-V2-1` | Municipios de Cataluña con renta de fianzas (Incasòl) en el análisis | 261 municipios | C1 | 2015-2025 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-A23-V2-2` | Municipios de la C. Valenciana con renta de fianzas (GVA) en el análisis | 103 municipios | C1 | 2020-2025 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-B4-V1-1` | Aumento de la población extranjera 2014-2019 (denominador de la cota de cantidad) | 174.410 personas | C2 | 2014-2019 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-B4-V2-1` | Cota C2 de viviendas de alquiler absorbidas por turismo, sustitución 1:1 | 81.771 viviendas | C2 | 2020M08-2024M08 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-M3-V1-1` | Solares catastrales (uso «solar») | 3.092.393 unidades urbanas | C4 | 2026 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-M4-V3-1` | Viviendas vacías, Censo 2021 (consumo eléctrico) | 3.828.307 viviendas | C4 | 2021 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-M4-V3-2` | Viviendas de uso esporádico, Censo 2021 (consumo eléctrico) | 2.517.628 viviendas | C4 | 2021 | [hechos.json](../output/v6_3/VER/hechos.json) |
| `VER-M4-V3-3` | Viviendas turísticas, INE VUT experimental | 341.001 viviendas | C4 | 2026M05 | [hechos.json](../output/v6_3/VER/hechos.json) |

## Versión v7

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `V7-R4-H7-A1` | Coef. largo plazo ln_ocupados (alquiler, spec A), MG_dm; veredicto: NO CONFIRMADA (p de Holm de MG_dm >= 0,05) | 0,00302 a 0,088 d ln y por d ln x | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-A2` | Coef. largo plazo ln_pob_total (alquiler, spec A), MG_dm; veredicto: NO CONFIRMADA (p de Holm de MG_dm >= 0,05) | 0,177 a 0,894 d ln y por d ln x | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-A3` | Coef. largo plazo tasa_paro_epa (alquiler, spec B), MG_dm; veredicto: NO CONFIRMADA; signos discrepantes entre estimadores (p de… | -0,00405 a 0,0041 d ln y por pp de paro | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-C1` | Coef. largo plazo ln_ocupados (compra, spec A), MG_dm; veredicto: NO CONFIRMADA (p de Holm de MG_dm >= 0,05) | -0,46 a -0,062 d ln y por d ln x | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-C2` | Coef. largo plazo ln_hip_importe (compra, spec A), MG_dm; veredicto: NO CONFIRMADA; signos discrepantes entre estimadores (p de H… | -0,032 a 0,304 d ln y por d ln x | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-C3` | Coef. largo plazo ln_pob_total (compra, spec A), MG_dm; veredicto: NO CONFIRMADA; signos discrepantes entre estimadores (p de Hol… | -1,96 a 3,61 d ln y por d ln x | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-H7-C4` | Coef. largo plazo tasa_paro_epa (compra, spec B), MG_dm; veredicto: NO CONFIRMADA; signos discrepantes entre estimadores (p de Ho… | -0,018 a 0,00631 d ln y por pp de paro | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-PHI-ALQUILER-A` | Velocidad de ajuste media phi (MG_dm), alquiler spec A | -0,048 por trimestre | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-PHI-ALQUILER-B` | Velocidad de ajuste media phi (MG_dm), alquiler spec B | -0,03 por trimestre | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-PHI-COMPRA-A` | Velocidad de ajuste media phi (MG_dm), compra spec A | -0,168 por trimestre | C4 | 2007Q1-2025Q1 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4-PHI-COMPRA-B` | Velocidad de ajuste media phi (MG_dm), compra spec B | -0,088 por trimestre | C4 | 2007Q1-2026Q2 | [hechos.json](../output/v7/R4/hechos.json) |
| `V7-R4b-H-alquiler-A-phibar` | Velocidad de ajuste media del ECM jerarquico, alquiler, spec A | -0,00137 coef. trimestral (-0,013 a 0,00447) | C4 | 2007Q3-2025Q1 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R4b-H-alquiler-B-phibar` | Velocidad de ajuste media del ECM jerarquico, alquiler, spec B | -0,00269 coef. trimestral (-0,014 a 0,00195) | C4 | 2007Q3-2025Q1 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R4b-H-compra-A-phibar` | Velocidad de ajuste media del ECM jerarquico, compra, spec A | -0,00988 coef. trimestral (-0,078 a 0,017) | C4 | 2007Q3-2025Q1 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R4b-H-compra-B-phibar` | Velocidad de ajuste media del ECM jerarquico, compra, spec B | -0,051 coef. trimestral (-0,118 a 0,021) | C4 | 2007Q3-2025Q1 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R4b-L-alquiler-tipo-pico` | Mayor efecto diferencial /coef/ de shock tipo hipotecario x exposicion, alquiler (h=8) | 0,015 puntos % por DT de exposicion (-0,027 a 0,058) | C4 | 2008-2026 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R4b-L-compra-tipo-pico` | Mayor efecto diferencial /coef/ de shock tipo hipotecario x exposicion, compra (h=7) | -0,145 puntos % por DT de exposicion (-0,428 a 0,138) | C4 | 2008-2026 | [hechos.json](../output/v7/R4b/hechos.json) |
| `V7-R5-001` | CCAA donde el mejor candidato bate a la base fuerte (alquiler), h=1-4 [comparador: base fuerte = AR con factor común; frente a la… | 12 CCAA de 17 (0 a 17) | C4 | origenes 2016Q1-2026Q1 | [hechos.json](../output/v7/R5/hechos.json) |
| `V7-R5-002` | CCAA donde el mejor candidato bate a la base fuerte (compra), h=1-4 [comparador: base fuerte = AR con factor común; frente a la b… | 17 CCAA de 17 (0 a 17) | C4 | origenes 2016Q1-2026Q1 | [hechos.json](../output/v7/R5/hechos.json) |
| `V7-R5-003` | RMSE x100 de la base fuerte a h=1 (alquiler) | 0,217 puntos log x100 (0,135 a 0,313) | C4 | origenes 2016Q1-2026Q1 | [hechos.json](../output/v7/R5/hechos.json) |
| `V7-R5-004` | RMSE x100 de la base fuerte a h=1 (compra) | 1,74 puntos log x100 (1,33 a 2,21) | C4 | origenes 2016Q1-2026Q1 | [hechos.json](../output/v7/R5/hechos.json) |
| `V7-R6-b_vacias-esfuerzo10a` | Variacion del esfuerzo de compra a 10 anos si se aplicase b_vacias (mediana entre CCAA, rejilla) | -1,34 % (-6,39 a -0,324) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7/R6/hechos.json) |
| `V7-R6-c_vivienda_publica-esfuerzo10a` | Variacion del esfuerzo de compra a 10 anos si se aplicase c_vivienda_publica (mediana entre CCAA, rejilla) | -0,574 % (-2,22 a -0,058) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7/R6/hechos.json) |
| `V7-R6-d_turisticos-esfuerzo10a` | Variacion del esfuerzo de compra a 10 anos si se aplicase d_turisticos (mediana entre CCAA, rejilla) | -0,087 % (-1,23 a -0,011) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7/R6/hechos.json) |
| `V7-R6-e_ayuda_demanda-esfuerzo10a` | Variacion del esfuerzo de compra a 10 anos si se aplicase e_ayuda_demanda (mediana entre CCAA, rejilla) | -5,33 % (-9,55 a -0,838) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7/R6/hechos.json) |
| `V7-R6-f1_rebaja_ITP_IVA_vivienda_nueva-esfuerzo10a` | Variacion del esfuerzo de compra a 10 anos si se aplicase f1_rebaja_ITP_IVA_vivienda_nueva (mediana entre CCAA, rejilla) | -1,21 % (-2,44 a -0,118) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7/R6/hechos.json) |
| `HIST-039` | Largo plazo precio y alquiler con empleo, población, hipotecas y paro · Ninguna de las 7 hipótesis pre-registradas se confirma (M… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-040` | Cointegración y velocidad de ajuste · No se establece cointegración: el tipo Westerlund tiene baja potencia y Pedroni rechaza sol… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-041` | Tipos de interés por exposición regional · Proyecciones locales sin respuesta diferencial robusta · **Confirma** v1 y v2 (sin efe… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-042` | Zonas tensionadas y topes · Asociación de corto plazo de las zonas tensionadas que pasa BH, pero con pretendencia no descartada;… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-043` | Predicción regional · El mejor modelo por región bate a la base más exigente en 6 de 17 CCAA en alquiler y en 5 de 17 en compra (… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-044` | Propuestas · Robustas (sin subida del precio de mercado): movilización de vacías, vivienda pública e impuestos a la construcción… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-045` | Muestra · Todo es «informativo, muestra ya vista en v1»; la validación limpia es diferida (`make evaluate_v7`) · Nuevo protocolo… | (sin cifra puntual) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Versión v7.1

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `V71-S1-a_construccion-alquiler-efecto_10k` | Variación del precio por cada 10.000 viviendas, construcción adicional, alquiler, 10 años (mediana entre CCAA; rango entre CCAA) | -0,696 puntos % (-2,74 a -0,124) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-a_construccion-compra-efecto_10k` | Variación del precio por cada 10.000 viviendas, construcción adicional, compra, 10 años (mediana entre CCAA; rango entre CCAA) | -0,609 puntos % (-2,35 a -0,108) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-b_vacias-alquiler-efecto_10k` | Variación del precio por cada 10.000 viviendas, movilización de vacías, alquiler, 10 años (mediana entre CCAA; rango entre CCAA) | -1,75 puntos % (-6,8 a -0,306) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-b_vacias-compra-efecto_10k` | Variación del precio por cada 10.000 viviendas, movilización de vacías, compra, 10 años (mediana entre CCAA; rango entre CCAA) | -0,609 puntos % (-2,35 a -0,108) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-c_vivienda_publica-alquiler-efecto_10k` | Variación del precio por cada 10.000 viviendas, vivienda pública o asequible, alquiler, 10 años (mediana entre CCAA; rango entre… | -3,17 puntos % (-12,22 a -0,56) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-c_vivienda_publica-compra-efecto_10k` | Variación del precio por cada 10.000 viviendas, vivienda pública o asequible, compra, 10 años (mediana entre CCAA; rango entre CC… | -0,609 puntos % (-2,35 a -0,108) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-d_turisticos-alquiler-efecto_10k` | Variación del precio por cada 10.000 viviendas, regulación local de turísticos, alquiler, 10 años (mediana entre CCAA; rango entr… | -3,52 puntos % (-13,58 a -0,62) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-d_turisticos-compra-efecto_10k` | Variación del precio por cada 10.000 viviendas, regulación local de turísticos, compra, 10 años (mediana entre CCAA; rango entre… | -0,609 puntos % (-2,35 a -0,108) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-e_ayuda_demanda-compra-coste_anual_meur` | Coste fiscal anual aproximado, ayudas a la demanda, compra, 10 años (mediana entre CCAA; rango entre CCAA) | 378,2 M€/año (67,98 a 2.915) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur` | Coste anual por punto de reducción del precio neto pagado, ayudas a la demanda, compra, 10 años (mediana entre CCAA; rango entre… | 76,35 M€/año por punto (12,15 a 515,9) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-e_ayuda_demanda-compra-efecto_100meur_mercado` | Variación del precio de mercado por cada 100 M€ anuales, ayudas a la demanda, compra, 10 años (mediana entre CCAA; rango entre CC… | 1,36 puntos % (0,158 a 7,6) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur` | Coste fiscal anual aproximado, rebaja de ITP/IVA (vivienda nueva), compra, 10 años (mediana entre CCAA; rango entre CCAA) | 93,34 M€/año (17,23 a 717,7) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur` | Coste anual por punto de reducción del precio neto pagado, rebaja de ITP/IVA (vivienda nueva), compra, 10 años (mediana entre CCA… | 82,43 M€/año por punto (12,91 a 549,5) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-efecto_100meur_mercado` | Variación del precio de mercado por cada 100 M€ anuales, rebaja de ITP/IVA (vivienda nueva), compra, 10 años (mediana entre CCAA;… | 1,36 puntos % (0,158 a 7,6) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S1/hechos.json) |
| `V71-S3-MC-DFE-A-cobertura` | Cobertura del IC95 de DFE en el escenario A (media; mín. y máx. entre θ1 y θ2) | 0,902  (0,89 a 0,915) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-DFE-A-sesgo` | Sesgo relativo máximo /θ/ de DFE en el escenario A (Monte Carlo R2, ronda 2, N=17, T=78) | 2,23 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-DFE-B-cobertura` | Cobertura del IC95 de DFE en el escenario B (media; mín. y máx. entre θ1 y θ2) | 0,873  (0,85 a 0,895) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-DFE-B-sesgo` | Sesgo relativo máximo /θ/ de DFE en el escenario B (Monte Carlo R2, ronda 2, N=17, T=78) | 3,11 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-DFE-E-cobertura` | Cobertura del IC95 de DFE en el escenario E (media; mín. y máx. entre θ1 y θ2) | 0,938  (0,915 a 0,96) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-DFE-E-sesgo` | Sesgo relativo máximo /θ/ de DFE en el escenario E (Monte Carlo R2, ronda 2, N=17, T=78) | 20,51 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-CS-ARDL_pT4` | Cobertura del IC95 de CS-ARDL (p_T=4) en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,862  (0,812 a 0,912) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-CS-DL_pT4` | Cobertura del IC95 de CS-DL (p_T=4) en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,879  (0,86 a 0,898) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-MG` | Cobertura del IC95 de MG sin ajuste en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,371  (0,344 a 0,398) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-MG_dm` | Cobertura del IC95 de MG con demeaning en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,889  (0,848 a 0,93) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-PMG` | Cobertura del IC95 de PMG sin ajuste en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,122  (0,106 a 0,138) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-cobertura-PMG_dm_boot` | Cobertura del IC95 de PMG con demeaning y bootstrap en el mismo escenario (mín. y máx. entre θ1 y θ2) | 0,92  (0,895 a 0,945) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-CS-ARDL_pT4` | Sesgo relativo máximo /θ/ de CS-ARDL (p_T=4) con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78) | 16,81 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-CS-DL_pT4` | Sesgo relativo máximo /θ/ de CS-DL (p_T=4) con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78) | 10,88 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-MG` | Sesgo relativo máximo /θ/ de MG sin ajuste con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78) | 53,92 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-MG_dm` | Sesgo relativo máximo /θ/ de MG con demeaning con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78) | 20,28 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-PMG` | Sesgo relativo máximo /θ/ de PMG sin ajuste con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=78) | 43,83 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-F-sesgo-PMG_dm_boot` | Sesgo relativo máximo /θ/ de PMG con demeaning y bootstrap con factor común I(1) de cargas heterogéneas (Monte Carlo R2, N=17, T=… | 15,8 % | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-WL-potencia-J` | Potencia del contraste tipo Westerlund con ajuste lento (φ entre −0,1 y −0,02; mín. y máx. de Ga, Gt, Pa y Pt) | 0,138  (0,06 a 0,285) | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-MC-phi-critico` | Valor crítico al 5 % del t de MG de la velocidad de ajuste media bajo no cointegración (simulado; menor de C y D) | -8,83 | C4 | simulación | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R5-exigente-alquiler` | CCAA en las que el mejor modelo regional bate a la base más exigente (alquiler; h=1-4; selección en muestra, informativo) | 6 CCAA de 17 | C4 | 2016T1-2026T1 (orígenes) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R5-exigente-compra` | CCAA en las que el mejor modelo regional bate a la base más exigente (compra; h=1-4; selección en muestra, informativo) | 5 CCAA de 17 | C4 | 2016T1-2026T1 (orígenes) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-a_construccion-alquiler-precio10a` | Variación del alquiler de mercado a 10 años si se aplicase «construcción adicional» (escenario condicional; mediana entre CCAA; m… | -1,58 % (-4,4 a -0,371) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-a_construccion-alquiler-robustas` | CCAA en las que «construcción adicional» es robusta en alquiler (esfuerzo baja en todas las extracciones y el precio de mercado n… | 16 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-a_construccion-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «construcción adicional» (escenario condicional; mediana entre… | -1,44 % (-3,96 a -0,331) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-a_construccion-compra-robustas` | CCAA en las que «construcción adicional» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de mercado no… | 17 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-b_vacias-alquiler-precio10a` | Variación del alquiler de mercado a 10 años si se aplicase «movilización de vacías» (escenario condicional; mediana entre CCAA; m… | -3,78 % (-8,37 a -1,63) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-b_vacias-alquiler-robustas` | CCAA en las que «movilización de vacías» es robusta en alquiler (esfuerzo baja en todas las extracciones y el precio de mercado n… | 17 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-b_vacias-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «movilización de vacías» (escenario condicional; mediana entre… | -1,34 % (-2,98 a -0,573) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-b_vacias-compra-robustas` | CCAA en las que «movilización de vacías» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de mercado no… | 17 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-c_vivienda_publica-alquiler-precio10a` | Variación del alquiler de mercado a 10 años si se aplicase «vivienda pública o asequible» (escenario condicional; mediana entre C… | -2,96 % (-5,28 a -0,645) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-c_vivienda_publica-alquiler-robustas` | CCAA en las que «vivienda pública o asequible» es robusta en alquiler (esfuerzo baja en todas las extracciones y el precio de mer… | 17 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-c_vivienda_publica-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «vivienda pública o asequible» (escenario condicional; mediana… | -0,574 % (-1,01 a -0,126) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-c_vivienda_publica-compra-robustas` | CCAA en las que «vivienda pública o asequible» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de merca… | 12 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-d_turisticos-alquiler-precio10a` | Variación del alquiler de mercado a 10 años si se aplicase «regulación local de turísticos» (escenario condicional; mediana entre… | -0,498 % (-3,05 a -0,178) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-d_turisticos-alquiler-robustas` | CCAA en las que «regulación local de turísticos» es robusta en alquiler (esfuerzo baja en todas las extracciones y el precio de m… | 8 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-d_turisticos-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «regulación local de turísticos» (escenario condicional; media… | -0,087 % (-0,531 a -0,031) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-d_turisticos-compra-robustas` | CCAA en las que «regulación local de turísticos» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de mer… | 1 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-e_ayuda_demanda-alquiler-precio10a` | Variación del alquiler de mercado a 10 años si se aplicase «ayudas a la demanda» (escenario condicional; mediana entre CCAA; mín.… | 4,37 % (4,14 a 8,09) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-e_ayuda_demanda-alquiler-robustas` | CCAA en las que «ayudas a la demanda» es robusta en alquiler (esfuerzo baja en todas las extracciones y el precio de mercado no s… | 0 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-e_ayuda_demanda-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «ayudas a la demanda» (escenario condicional; mediana entre CC… | 4,37 % (4,14 a 8,09) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-e_ayuda_demanda-compra-robustas` | CCAA en las que «ayudas a la demanda» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de mercado no sub… | 0 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-f1_rebaja_ITP_IVA_vivienda_nueva-compra-precio10a` | Variación del precio de compra de mercado a 10 años si se aplicase «rebaja de ITP/IVA (vivienda nueva)» (escenario condicional; m… | 1,07 % (1,01 a 1,99) | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-R6-f1_rebaja_ITP_IVA_vivienda_nueva-compra-robustas` | CCAA en las que «rebaja de ITP/IVA (vivienda nueva)» es robusta en compra (esfuerzo baja en todas las extracciones y el precio de… | 0 CCAA de 17 | C4 | 2026-2036 (escenario) | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-comun-corr-alquiler` | Correlación media entre pares de CCAA de la variación interanual (alquiler; mín. y máx. entre pares) | 0,857  (0,581 a 0,965) | C4 | 2008Q1-2026Q2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-comun-corr-compra` | Correlación media entre pares de CCAA de la variación interanual (compra; mín. y máx. entre pares) | 0,92  (0,738 a 0,99) | C4 | 2008Q1-2026Q2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-comun-r2-alquiler` | Parte de la varianza de la variación interanual de IPC del alquiler de cada CCAA que acompaña a la media de las 17 CCAA (R², medi… | 86,14 % (64,86 a 97,37) | C4 | 2008Q1-2026Q2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-comun-r2-compra` | Parte de la varianza de la variación interanual de IPV de cada CCAA que acompaña a la media de las 17 CCAA (R², mediana entre CCA… | 93,61 % (81,04 a 97,83) | C4 | 2008Q1-2026Q2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-i2-alquiler` | CCAA en las que no se descarta I(2) en ln_ipc_alquiler (ADF en diferencias con constante y tendencia) | 9 CCAA de 17 | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-i2-compra` | CCAA en las que no se descarta I(2) en ln_ipv (ADF en diferencias con constante y tendencia) | 8 CCAA de 17 | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `V71-S3-largo-confirmadas` | Hipótesis de largo plazo regional confirmadas (de 7 pre-registradas; Holm y triangulación MG_dm, PMG_dm y CS-DL) | 0 hipótesis | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_1/S3/hechos.json) |
| `FICHA-V7-V1` | En cada comunidad autónoma, el precio y el alquiler dependen a largo plazo sobre todo del empleo y de la población. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resumen.md](../output/v7/R4/alquiler/resumen.md) |
| `FICHA-V7-V2` | Las ayudas directas a la compra abaratan la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [impactos.csv](../output/v7/R6/impactos.csv) |
| `FICHA-V7-V3` | Las subidas de los tipos de interés abaratan la vivienda más en las regiones con más hipotecas. | ANALIZADA, NO CONCLUYENTE | C4 |  | [lp_compra.csv](../output/v7/R4b/lp_compra.csv) |
| `FICHA-V72-BURBUJA` | Hay una burbuja en el precio de la vivienda en España. | ANALIZADA, NO CONCLUYENTE | C4 |  | [reverificacion.csv](../output/v7_2/gsadf/reverificacion.csv) |

## Versión v7.2

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `V72-GSADF-ccaa-bh` | Series de CCAA (precio/alquiler, IPV y valor tasado; 17 CCAA) con exuberancia tras BH | 7 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-ccaa-v6` | CCAA con exuberancia (p<0,05) en el ratio precio/alquiler, provincias de entrenamiento v6 | 0 CCAA | C4 | 2015T1-2024T4 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-niveles-bh` | Niveles de precio nacionales (IPV y valor tasado, sin fundamentales) con exuberancia tras BH | 2 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-ratios-bh` | Cocientes precio/renta y precio/alquiler nacionales con exuberancia tras BH | 0 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-ratios-p05` | Cocientes precio/renta y precio/alquiler nacionales con exuberancia sin ajuste múltiple (p<0,05) | 3 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-rev` | Series nacionales del GSADF de v5 que se reproducen exactamente con el mismo método y la misma semilla | 14 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |
| `V72-GSADF-tipos-p05` | Precio frente a valores de referencia con tipos de interés (descuento del alquiler y cuota sobre renta) con exuberancia sin ajuste | 0 series | C4 | 2007T1-2026T2 | [hechos.json](../output/v7_2/gsadf/hechos.json) |

## Versión V8

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `V8-H8-1-est` | H8-1: En P5, la contribucion del shock demografico a la subida del alquiler real es positiva (contribución acumulada del periodo,… | 0,074 pp (-4,51 a 4,73) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-1-pholm` | H8-1: p ajustado por Holm (Prob. posterior unilateral; no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5)) | 0,987 | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-2-est` | H8-2: En P5, la contribucion de credito y tipos al precio real de compra es negativa (contribución acumulada del periodo, interva… | -0,469 pp (-15,43 a 27,44) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-2-pholm` | H8-2: p ajustado por Holm (Prob. posterior unilateral; no respaldada (la mediana apunta al signo contrario o no distingue)) | 0,987 | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-3-est` | H8-3: En P3, la contribucion de actividad y renta al precio real de compra es positiva (contribución acumulada del periodo, inter… | 7,72 pp (-22,81 a 40,01) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-3-pholm` | H8-3: p ajustado por Holm (Prob. posterior unilateral; no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5)) | 0,838 | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-4-est` | H8-4: En P2, la contribucion conjunta de credito y tipos y de actividad y renta al precio real de compra es negativa (contribució… | -19,23 pp (-57,26 a 9,88) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-4-pholm` | H8-4: p ajustado por Holm (Prob. posterior unilateral; no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5)) | 0,343 | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-5-F` | H8-5: F efectivo de la primera etapa (Un shock monetario contractivo del BCE reduce el precio real de compra a h = 4-8; umbral C3… | 1,83 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-5-pholm` | H8-5: p ajustado por Holm (no respaldada tras Holm (instrumento no supera C3)) | 1 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-5-tFR` | H8-5: t de la forma reducida (signo esperado -1) | 0,596 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-6-F` | H8-6: F efectivo de la primera etapa (Un shock monetario contractivo del BCE reduce el alquiler real a h = 4-8; umbral C3: F ≥ 10) | 0,766 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-6-pholm` | H8-6: p ajustado por Holm (no respaldada tras Holm (instrumento no supera C3)) | 1 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-6-tFR` | H8-6: t de la forma reducida (signo esperado -1) | 0,345 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-7-F` | H8-7: F efectivo de la primera etapa (El empuje migratorio aumenta el alquiler real; umbral C3: F ≥ 10) | 0,048 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-7-pholm` | H8-7: p ajustado por Holm (no respaldada tras Holm (instrumento no supera C3)) | 1 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-7-tFR` | H8-7: t de la forma reducida (signo esperado +1) | -0,091 | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-8-est` | H8-8: cuota mínima del componente común de las 17 CCAA en la varianza del crecimiento interanual del precio real de compra (mínim… | 45,27 % | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-8-pholm` | H8-8: p ajustado por Holm | 0,669 | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-9-est` | H8-9: correlación del factor común español con el crecimiento interanual del precio de la vivienda de la zona euro (EA19; interva… | 0,598  (0,135 a 0,858) | C4 | 1999-último dato | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-H8-9-pholm` | H8-9: p ajustado por Holm | 0,02 | C4 | 1999-último dato | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-bh` | Coeficientes de M0 significativos tras BH (q = 0,10) | 35 coeficientes | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-coef` | Coeficientes por periodo y variable estimados en M0 | 70 coeficientes | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-cumplen` | Efectos por periodo que cumplen la regla de §8 de M0 (ninguno sobrevive a BH; exploratorio) | 2 efectos | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-evaluables` | Coeficientes de M0 con la regla de periodo evaluable (cumple o no cumple) | 30 coeficientes | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-no-evaluable` | Coeficientes de M0 cuya regla de periodo es «no evaluable» (falta la medida alternativa de precio o de periodo; no es un incumpli… | 40 coeficientes | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M0-no-evaluable-alquiler` | De ellos, los del alquiler (no hay medida alternativa trimestral nacional del alquiler: la regla es «no evaluable», no «incumplid… | 35 coeficientes | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-a-P2` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de alquiler real en P2 (banda del 68 %… | 96,21 % (92,6 a 97,7) | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-a-P3` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de alquiler real en P3 (banda del 68 %… | 79,58 % (71,51 a 86) | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-a-P4` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de alquiler real en P4 (banda del 68 %… | 99,5 % (99,26 a 99,71) | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-a-P5` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de alquiler real en P5 (banda del 68 %… | 97,49 % (86,1 a 98,69) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-c-P1` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P1 (banda… | 64,74 % (56,38 a 71,24) | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-c-P2` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P2 (banda… | 45,27 % (42,01 a 54,17) | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-c-P3` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P3 (banda… | 59,58 % (47,81 a 66,82) | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-c-P4` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P4 (banda… | 45,5 % (42,73 a 53,12) | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-cuota-c-P5` | Cuota del primer componente común de las 17 CCAA en la varianza del crecimiento interanual de precio real de compra en P5 (banda… | 92,79 % (86,65 a 94,92) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-eur-c-P1` | Parte de la variación de precio real de compra en P1 asociada al precio de la vivienda de la zona euro (regresión con retardos 0-… | 7,37 pp (4,72 a 8,73) | C4 | P1 (ventana efectiva 2005T3-2007T4, n =… | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-eur-c-P2` | Parte de la variación de precio real de compra en P2 asociada al precio de la vivienda de la zona euro (regresión con retardos 0-… | -15,33 pp (-21,72 a -7,55) | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-eur-c-P3` | Parte de la variación de precio real de compra en P3 asociada al precio de la vivienda de la zona euro (regresión con retardos 0-… | 0,811 pp (-4,41 a 4,04) | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-eur-c-P4` | Parte de la variación de precio real de compra en P4 asociada al precio de la vivienda de la zona euro (regresión con retardos 0-… | 1,39 pp (-1,76 a 3,38) | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M1-eur-c-P5` | Parte de la variación de precio real de compra en P5 asociada al precio de la vivienda de la zona euro (regresión con retardos 0-… | -3,32 pp (-7,04 a 1,76) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M4-ardl-rechaza` | Especificaciones de largo plazo (compra y alquiler) en que el ARDL con cotas rechaza la no cointegración (sin rupturas) | 2 especificaciones | C4 | 1998T1-último dato | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M4-ardl-total` | Especificaciones de largo plazo probadas con el ARDL con cotas (compra y alquiler) | 9 especificaciones | C4 | 1998T1-último dato | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M4-voto-demografia` | Celdas (mercado, periodo) en que la contabilidad hogares-viviendas vota a favor de la demografía | 2 celdas | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M5-c3` | Instrumentos de M5 (hipótesis H8-5 a H8-7) que cumplen las condiciones de C3 | 0 instrumentos | C4 | ver hipótesis | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-P2-corr` | Correlación entre el crecimiento interanual de la población total y el de la población extranjera (INE), P2 (2008T3-2013T4) (n =… | 0,98 | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-P2-vif` | VIF del par población total y población extranjera, P2 (2008T3-2013T4) (1 / (1 - r²) con dos variables; diagnóstico descriptivo) | 24,89 cociente | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-P5-corr` | Correlación entre el crecimiento interanual de la población total y el de la población extranjera (INE), P5 (2022T3-último dato)… | 0,779 | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-P5-vif` | VIF del par población total y población extranjera, P5 (2022T3-último dato) (1 / (1 - r²) con dos variables; diagnóstico descript… | 2,54 cociente | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-completo-corr` | Correlación entre el crecimiento interanual de la población total y el de la población extranjera (INE), muestra completa (n = 94… | 0,914 | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-colpob-completo-vif` | VIF del par población total y población extranjera, muestra completa (1 / (1 - r²) con dos variables; diagnóstico descriptivo) | 6,07 cociente | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-vif-max` | VIF máximo de las ecuaciones de M6 (una variable por familia; ninguna ecuación incluye a la vez la población total y la extranjer… | 18,38 cociente | C4 | P1-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M6-vif-pob_total-max` | VIF máximo de la población total en las ecuaciones de M6 (P3, interanual) | 7,44 cociente | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-ajustadas` | Especificaciones del multiverso ajustadas con éxito (las fallidas están en registro.csv) | 32.424 especificaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-combinaciones` | Combinaciones (mercado, periodo, factor) evaluadas en el multiverso | 74 combinaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-cumplen` | Combinaciones que cumplen la regla del multiverso (signo orientado estable en ≥ 80 % y significativo tras BH en ≥ 50 %) | 2 combinaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-rejilla` | Especificaciones de la rejilla del multiverso (tope 50.000; sin truncar) | 37.980 especificaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-hogares_epa-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), hogares (EPA) (demografía), alquiler real, P2 (… | 75 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-hogares_epa-signo` | Multiverso por variable: % de especificaciones con el mismo signo, hogares (EPA) (demografía), alquiler real, P2 (2008T3-2013T4);… | 100 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-pob_extranj_ine-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), población extranjera (INE) (demografía), alquil… | 77,08 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-pob_extranj_ine-signo` | Multiverso por variable: % de especificaciones con el mismo signo, población extranjera (INE) (demografía), alquiler real, P2 (20… | 100 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-pob_total-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), población total (demografía), alquiler real, P2… | 82,29 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P2-pob_total-signo` | Multiverso por variable: % de especificaciones con el mismo signo, población total (demografía), alquiler real, P2 (2008T3-2013T4… | 100 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P4-pob_extranj_ine-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), población extranjera (INE) (demografía), alquil… | 52,5 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P4-pob_extranj_ine-signo` | Multiverso por variable: % de especificaciones con el mismo signo, población extranjera (INE) (demografía), alquiler real, P4 (20… | 80 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P4-tipo_hip_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), tipo hipotecario real (crédito y tipos), alquil… | 54,17 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-P4-tipo_hip_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, tipo hipotecario real (crédito y tipos), alquiler real, P4 (20… | 83,33 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-credito_stock_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), saldo de crédito real (crédito y tipos), alquil… | 52,6 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-credito_stock_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, saldo de crédito real (crédito y tipos), alquiler real, muestr… | 93,75 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-pob_extranj_ine-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), población extranjera (INE) (demografía), alquil… | 62,5 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-pob_extranj_ine-signo` | Multiverso por variable: % de especificaciones con el mismo signo, población extranjera (INE) (demografía), alquiler real, muestr… | 98,96 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-pob_total-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), población total (demografía), alquiler real, mu… | 69,27 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-pob_total-signo` | Multiverso por variable: % de especificaciones con el mismo signo, población total (demografía), alquiler real, muestra completa;… | 100 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-tipo_hip_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), tipo hipotecario real (crédito y tipos), alquil… | 72,92 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-a-completo-tipo_hip_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, tipo hipotecario real (crédito y tipos), alquiler real, muestr… | 100 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P1-tipo_hip_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), tipo hipotecario real (crédito y tipos), precio… | 65,62 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P1-tipo_hip_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, tipo hipotecario real (crédito y tipos), precio real de compra… | 95,83 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-bis_hpi_xm_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), precio real de la vivienda de otros países (BIS… | 58,85 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-bis_hpi_xm_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, precio real de la vivienda de otros países (BIS) (factor europ… | 94,79 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-credito_stock_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), saldo de crédito real (crédito y tipos), precio… | 64,06 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-credito_stock_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, saldo de crédito real (crédito y tipos), precio real de compra… | 92,71 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-tipo_hip_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), tipo hipotecario real (crédito y tipos), precio… | 50 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-P5-tipo_hip_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, tipo hipotecario real (crédito y tipos), precio real de compra… | 87,5 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-bis_hpi_xm_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), precio real de la vivienda de otros países (BIS… | 64,32 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-bis_hpi_xm_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, precio real de la vivienda de otros países (BIS) (factor europ… | 98,96 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-credito_nuevo_real-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), crédito nuevo real (crédito y tipos), precio re… | 54,95 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-credito_nuevo_real-signo` | Multiverso por variable: % de especificaciones con el mismo signo, crédito nuevo real (crédito y tipos), precio real de compra, m… | 86,98 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-ocupados-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), ocupados (EPA) (empleo y renta), precio real de… | 51,3 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-ocupados-signo` | Multiverso por variable: % de especificaciones con el mismo signo, ocupados (EPA) (empleo y renta), precio real de compra, muestr… | 97,4 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-terminadas-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), viviendas terminadas (oferta), precio real de c… | 52,6 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-terminadas-signo` | Multiverso por variable: % de especificaciones con el mismo signo, viviendas terminadas (oferta), precio real de compra, muestra… | 95,31 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-visados-bh` | Multiverso por variable: % de especificaciones significativas tras BH (q = 0,10), visados de obra nueva (oferta), precio real de… | 74,74 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-c-completo-visados-signo` | Multiverso por variable: % de especificaciones con el mismo signo, visados de obra nueva (oferta), precio real de compra, muestra… | 97,92 % | C4 | muestra completa | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-cumplen` | Combinaciones (mercado, periodo, variable) que cumplen la regla del multiverso a nivel de variable (signo orientado estable en >=… | 18 combinaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-cumplen-rejilla` | De ellas, las que siguen cumpliendo si las especificaciones fallidas u omitidas cuentan como «no cumple» (P4 y compra P1: multive… | 15 combinaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M7-var-total` | Combinaciones (mercado, periodo, variable) evaluadas a nivel de variable en el multiverso | 200 combinaciones | C4 | P1-P5 y completo | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-a-P2` | Cuota del componente común en la varianza de alquiler real (mediana entre las 17 CCAA) en P2 | 96,1 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-a-P3` | Cuota del componente común en la varianza de alquiler real (mediana entre las 17 CCAA) en P3 | 85,8 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-a-P4` | Cuota del componente común en la varianza de alquiler real (mediana entre las 17 CCAA) en P4 | 99,8 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-a-P5` | Cuota del componente común en la varianza de alquiler real (mediana entre las 17 CCAA) en P5 | 98,2 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-c-P1` | Cuota del componente común en la varianza de precio real de compra (mediana entre las 17 CCAA) en P1 | 68,5 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-c-P2` | Cuota del componente común en la varianza de precio real de compra (mediana entre las 17 CCAA) en P2 | 46,2 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-c-P3` | Cuota del componente común en la varianza de precio real de compra (mediana entre las 17 CCAA) en P3 | 61,9 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-c-P4` | Cuota del componente común en la varianza de precio real de compra (mediana entre las 17 CCAA) en P4 | 46,5 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-comun-c-P5` | Cuota del componente común en la varianza de precio real de compra (mediana entre las 17 CCAA) en P5 | 93,6 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P1-cuota` | R² del crecimiento interanual de provincia de Alicante (03) en P1 sobre el factor común nacional (cuota de varianza; no es parte… | 61,41 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P1-total` | Variación observada del precio real de compra en provincia de Alicante (03) en P1 (pp, log×100; media interanual × T/4: aproximac… | 94,91 pp | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P2-cuota` | R² del crecimiento interanual de provincia de Alicante (03) en P2 sobre el factor común nacional (cuota de varianza; no es parte… | 19,25 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P2-total` | Variación observada del precio real de compra en provincia de Alicante (03) en P2 (pp, log×100; media interanual × T/4: aproximac… | -46,56 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P3-cuota` | R² del crecimiento interanual de provincia de Alicante (03) en P3 sobre el factor común nacional (cuota de varianza; no es parte… | 39,59 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P3-total` | Variación observada del precio real de compra en provincia de Alicante (03) en P3 (pp, log×100; media interanual × T/4: aproximac… | 4,21 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P4-cuota` | R² del crecimiento interanual de provincia de Alicante (03) en P4 sobre el factor común nacional (cuota de varianza; no es parte… | 8,53 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P4-total` | Variación observada del precio real de compra en provincia de Alicante (03) en P4 (pp, log×100; media interanual × T/4: aproximac… | -1,11 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P5-acum-alt` | Variación acumulada observada del precio real de compra en provincia de Alicante (03) en P5 con la segunda fuente (Registradores… | 20,3 pp | C1 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P5-acum-mivau` | Variación acumulada observada del valor tasado real de compra en provincia de Alicante (03) en P5 (valor tasado MIVAU (p_tasado)… | 25,07 pp | C1 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P5-cuota` | R² del crecimiento interanual de provincia de Alicante (03) en P5 sobre el factor común nacional (cuota de varianza; no es parte… | 95,81 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P5-fcpp` | Parte de la variación del precio real de compra de provincia de Alicante (03) en P5 asociada al factor común nacional (pp; regres… | 11,24 pp (4,58 a 16,8) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p03-P5-total` | Variación observada del precio real de compra en provincia de Alicante (03) en P5 (pp, log×100; media interanual × T/4: aproximac… | 16,84 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P1-cuota` | R² del crecimiento interanual de provincia de Castellón (12) en P1 sobre el factor común nacional (cuota de varianza; no es parte… | 58,02 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P1-total` | Variación observada del precio real de compra en provincia de Castellón (12) en P1 (pp, log×100; media interanual × T/4: aproxima… | 98,2 pp | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P2-cuota` | R² del crecimiento interanual de provincia de Castellón (12) en P2 sobre el factor común nacional (cuota de varianza; no es parte… | 71,07 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P2-total` | Variación observada del precio real de compra en provincia de Castellón (12) en P2 (pp, log×100; media interanual × T/4: aproxima… | -54,37 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P3-cuota` | R² del crecimiento interanual de provincia de Castellón (12) en P3 sobre el factor común nacional (cuota de varianza; no es parte… | 80,41 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P3-total` | Variación observada del precio real de compra en provincia de Castellón (12) en P3 (pp, log×100; media interanual × T/4: aproxima… | -8,26 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P4-cuota` | R² del crecimiento interanual de provincia de Castellón (12) en P4 sobre el factor común nacional (cuota de varianza; no es parte… | 57,36 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P4-total` | Variación observada del precio real de compra en provincia de Castellón (12) en P4 (pp, log×100; media interanual × T/4: aproxima… | -3,64 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P5-acum-alt` | Variación acumulada observada del precio real de compra en provincia de Castellón (12) en P5 con la segunda fuente (Registradores… | 10,89 pp | C1 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P5-acum-mivau` | Variación acumulada observada del valor tasado real de compra en provincia de Castellón (12) en P5 (valor tasado MIVAU (p_tasado)… | 18,57 pp | C1 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P5-cuota` | R² del crecimiento interanual de provincia de Castellón (12) en P5 sobre el factor común nacional (cuota de varianza; no es parte… | 94,52 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P5-fcpp` | Parte de la variación del precio real de compra de provincia de Castellón (12) en P5 asociada al factor común nacional (pp; regre… | 14,61 pp (6,65 a 21,38) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p12-P5-total` | Variación observada del precio real de compra en provincia de Castellón (12) en P5 (pp, log×100; media interanual × T/4: aproxima… | 7,8 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P1-cuota` | R² del crecimiento interanual de provincia de València (46) en P1 sobre el factor común nacional (cuota de varianza; no es parte… | 74,29 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P1-total` | Variación observada del precio real de compra en provincia de València (46) en P1 (pp, log×100; media interanual × T/4: aproximac… | 85,89 pp | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P2-cuota` | R² del crecimiento interanual de provincia de València (46) en P2 sobre el factor común nacional (cuota de varianza; no es parte… | 59,32 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P2-total` | Variación observada del precio real de compra en provincia de València (46) en P2 (pp, log×100; media interanual × T/4: aproximac… | -48,41 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P3-cuota` | R² del crecimiento interanual de provincia de València (46) en P3 sobre el factor común nacional (cuota de varianza; no es parte… | 63,32 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P3-total` | Variación observada del precio real de compra en provincia de València (46) en P3 (pp, log×100; media interanual × T/4: aproximac… | 4,47 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P4-cuota` | R² del crecimiento interanual de provincia de València (46) en P4 sobre el factor común nacional (cuota de varianza; no es parte… | 36,92 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P4-total` | Variación observada del precio real de compra en provincia de València (46) en P4 (pp, log×100; media interanual × T/4: aproximac… | 0,575 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P5-acum-alt` | Variación acumulada observada del precio real de compra en provincia de València (46) en P5 con la segunda fuente (Registradores… | 17,37 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P5-acum-mivau` | Variación acumulada observada del valor tasado real de compra en provincia de València (46) en P5 (valor tasado MIVAU (p_tasado)… | 29,36 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P5-cuota` | R² del crecimiento interanual de provincia de València (46) en P5 sobre el factor común nacional (cuota de varianza; no es parte… | 97,96 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P5-fcpp` | Parte de la variación del precio real de compra de provincia de València (46) en P5 asociada al factor común nacional (pp; regres… | 12,24 pp (5,56 a 18,22) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-p46-P5-total` | Variación observada del precio real de compra en provincia de València (46) en P5 (pp, log×100; media interanual × T/4: aproximac… | 21,11 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P1-cuota` | R² del crecimiento interanual de València ciudad en P1 sobre el factor común nacional (cuota de varianza; no es parte de la varia… | 12,18 % | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P1-total` | Variación observada del precio real de compra en València ciudad en P1 (pp, log×100; media interanual × T/4: aproximación, no es… | 17,22 pp | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P2-cuota` | R² del crecimiento interanual de València ciudad en P2 sobre el factor común nacional (cuota de varianza; no es parte de la varia… | 39,17 % | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P2-total` | Variación observada del precio real de compra en València ciudad en P2 (pp, log×100; media interanual × T/4: aproximación, no es… | -68,56 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P3-cuota` | R² del crecimiento interanual de València ciudad en P3 sobre el factor común nacional (cuota de varianza; no es parte de la varia… | 32,82 % | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P3-total` | Variación observada del precio real de compra en València ciudad en P3 (pp, log×100; media interanual × T/4: aproximación, no es… | 7,76 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P4-cuota` | R² del crecimiento interanual de València ciudad en P4 sobre el factor común nacional (cuota de varianza; no es parte de la varia… | 17,23 % | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P4-total` | Variación observada del precio real de compra en València ciudad en P4 (pp, log×100; media interanual × T/4: aproximación, no es… | 6,27 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P5-acum-mivau` | Variación acumulada observada del valor tasado real de compra en València ciudad en P5 (valor tasado MIVAU (p_tasado) real; pp lo… | 43,48 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P5-cuota` | R² del crecimiento interanual de València ciudad en P5 sobre el factor común nacional (cuota de varianza; no es parte de la varia… | 77,25 % | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P5-fcpp` | Parte de la variación del precio real de compra de València ciudad en P5 asociada al factor común nacional (pp; regresión sobre e… | 13 pp (5,08 a 19,94) | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M8-cv-vlc-P5-total` | Variación observada del precio real de compra en València ciudad en P5 (pp, log×100; media interanual × T/4: aproximación, no es… | 36,32 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-dml-a-tipo` | Coeficiente DML (sin identificación; asociación) del tipo hipotecario real sobre el crecimiento de alquiler real (p ajustado BH 0… | 0,452 | C4 | panel de CCAA | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-dml-c-tipo` | Coeficiente DML (sin identificación; asociación) del tipo hipotecario real sobre el crecimiento de precio real de compra (p ajust… | 0,045 | C4 | panel de CCAA | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-nacional-base` | RMSE fuera de muestra de la base más exigente (ar4) para alquiler real (crecimiento trimestral real, pp) | 0,947 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-nacional-mejor` | Modelos de M9 que superan a la base más exigente tras BH en alquiler real | 0 modelos | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-nacional-ml` | RMSE fuera de muestra del mejor modelo de aprendizaje automático en esa tabla (gam_ar_alfa100) para alquiler real (pp; no se elig… | 1,73 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-panel-base` | RMSE fuera de muestra de la base más exigente (ar4) para alquiler real (crecimiento trimestral real, pp) | 0,931 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-panel-mejor` | Modelos de M9 que superan a la base más exigente tras BH en alquiler real | 0 modelos | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-a-panel-ml` | RMSE fuera de muestra del mejor modelo de aprendizaje automático en esa tabla (gam_ar_alfa100) para alquiler real (pp; no se elig… | 1,06 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-nacional-base` | RMSE fuera de muestra de la base más exigente (ar4) para precio real de compra (crecimiento trimestral real, pp) | 1,09 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-nacional-mejor` | Modelos de M9 que superan a la base más exigente tras BH en precio real de compra | 0 modelos | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-nacional-ml` | RMSE fuera de muestra del mejor modelo de aprendizaje automático en esa tabla (gam_ar_alfa100) para precio real de compra (pp; no… | 2,24 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-panel-base` | RMSE fuera de muestra de la base más exigente (ar4_fc) para precio real de compra (crecimiento trimestral real, pp) | 2,14 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-panel-mejor` | Modelos de M9 que superan a la base más exigente tras BH en precio real de compra | 0 modelos | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-oos-c-panel-ml` | RMSE fuera de muestra del mejor modelo de aprendizaje automático en esa tabla (gam_ar_alfa100) para precio real de compra (pp; no… | 2,46 pp | C4 | bloque de prueba de M9 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P2-demanda_externa` | Contribución SHAP media de demanda externa a la variación de alquiler real en P2 en el panel de CCAA (banda del 68 % por bootstra… | 0,241 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P2-factor_europeo` | Contribución SHAP media de factor europeo a la variación de alquiler real en P2 en el panel de CCAA (banda del 68 % por bootstrap… | 0,806 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P3-demanda_externa` | Contribución SHAP media de demanda externa a la variación de alquiler real en P3 en el panel de CCAA (banda del 68 % por bootstra… | -0,171 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P3-factor_europeo` | Contribución SHAP media de factor europeo a la variación de alquiler real en P3 en el panel de CCAA (banda del 68 % por bootstrap… | 3,23 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P4-demanda_externa` | Contribución SHAP media de demanda externa a la variación de alquiler real en P4 en el panel de CCAA (banda del 68 % por bootstra… | 0,067 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P4-factor_europeo` | Contribución SHAP media de factor europeo a la variación de alquiler real en P4 en el panel de CCAA (banda del 68 % por bootstrap… | -2,68 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P4-turismo` | Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional: Contr… | 0,109 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P5-demanda_externa` | Contribución SHAP media de demanda externa a la variación de alquiler real en P5 en el panel de CCAA (banda del 68 % por bootstra… | -0,218 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P5-factor_europeo` | Contribución SHAP media de factor europeo a la variación de alquiler real en P5 en el panel de CCAA (banda del 68 % por bootstrap… | -1,76 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-a-P5-turismo` | Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional: Contr… | -0,436 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P2-demanda_externa` | Contribución SHAP media de demanda externa a la variación de precio real de compra en P2 en el panel de CCAA (banda del 68 % por… | -0,373 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P2-factor_europeo` | Contribución SHAP media de factor europeo a la variación de precio real de compra en P2 en el panel de CCAA (banda del 68 % por b… | -12,69 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P3-demanda_externa` | Contribución SHAP media de demanda externa a la variación de precio real de compra en P3 en el panel de CCAA (banda del 68 % por… | -0,237 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P3-factor_europeo` | Contribución SHAP media de factor europeo a la variación de precio real de compra en P3 en el panel de CCAA (banda del 68 % por b… | 6,86 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P4-demanda_externa` | Contribución SHAP media de demanda externa a la variación de precio real de compra en P4 en el panel de CCAA (banda del 68 % por… | 0,091 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P4-factor_europeo` | Contribución SHAP media de factor europeo a la variación de precio real de compra en P4 en el panel de CCAA (banda del 68 % por b… | -0,22 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P4-turismo` | Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional: Contr… | 1,47 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P5-demanda_externa` | Contribución SHAP media de demanda externa a la variación de precio real de compra en P5 en el panel de CCAA (banda del 68 % por… | 0,51 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P5-factor_europeo` | Contribución SHAP media de factor europeo a la variación de precio real de compra en P5 en el panel de CCAA (banda del 68 % por b… | 2,14 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-shap-c-P5-turismo` | Sensibilidad no principal (NaN nativos), media de las 6 CCAA con datos de turismo; no comparable con la variación nacional: Contr… | 15,16 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-M9-turismo-ccaa` | CCAA con datos de turismo (viviendas de uso turístico y turistas) utilizables en M9 | 6 CCAA | C4 | P4-P5 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-a-P1` | Variación observada de alquiler real en P1 (pp, log×100; unidad común R0) | 4,93 pp | C4 | P1 (sin datos de alquiler) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-a-P2` | Variación observada de alquiler real en P2 (pp, log×100; unidad común R0) | -2,7 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-a-P3` | Variación observada de alquiler real en P3 (pp, log×100; unidad común R0) | -1,06 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-a-P4` | Variación observada de alquiler real en P4 (pp, log×100; unidad común R0) | -9,34 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-a-P5` | Variación observada de alquiler real en P5 (pp, log×100; unidad común R0) | -1,85 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-c-P1` | Variación observada de precio real de compra en P1 (pp, log×100; unidad común R0) | 75,35 pp | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-c-P2` | Variación observada de precio real de compra en P2 (pp, log×100; unidad común R0) | -44 pp | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-c-P3` | Variación observada de precio real de compra en P3 (pp, log×100; unidad común R0) | 8,22 pp | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-c-P4` | Variación observada de precio real de compra en P4 (pp, log×100; unidad común R0) | -5,46 pp | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OBS-c-P5` | Variación observada de precio real de compra en P5 (pp, log×100; unidad común R0) | 18,42 pp | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-ar4-rmse` | RMSE fuera de muestra de ar4 para el crecimiento trimestral real de alquiler real (pp; misma muestra para todos los modelos) | 0,803 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-ar_fc-pholm` | p ajustado por Holm del contraste Diebold-Mariano de ar_fc frente al AR(4) (alquiler real) | 0,596 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-ar_fc-rmse` | RMSE fuera de muestra de ar_fc para el crecimiento trimestral real de alquiler real (pp; misma muestra para todos los modelos) | 0,832 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-bvar_m2-pholm` | p ajustado por Holm del contraste Diebold-Mariano de bvar_m2 frente al AR(4) (alquiler real) | 0,127 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-bvar_m2-rmse` | RMSE fuera de muestra de bvar_m2 para el crecimiento trimestral real de alquiler real (pp; misma muestra para todos los modelos) | 0,976 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-ecm_v1-pholm` | p ajustado por Holm del contraste Diebold-Mariano de ecm_v1 frente al AR(4) (alquiler real) | 0,00045 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-a-ecm_v1-rmse` | RMSE fuera de muestra de ecm_v1 para el crecimiento trimestral real de alquiler real (pp; misma muestra para todos los modelos) | 1,69 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-ar4-rmse` | RMSE fuera de muestra de ar4 para el crecimiento trimestral real de precio real de compra (pp; misma muestra para todos los model… | 1,18 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-ar_fc-pholm` | p ajustado por Holm del contraste Diebold-Mariano de ar_fc frente al AR(4) (precio real de compra) | 0,132 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-ar_fc-rmse` | RMSE fuera de muestra de ar_fc para el crecimiento trimestral real de precio real de compra (pp; misma muestra para todos los mod… | 1,27 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-bvar_m2-pholm` | p ajustado por Holm del contraste Diebold-Mariano de bvar_m2 frente al AR(4) (precio real de compra) | 0,132 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-bvar_m2-rmse` | RMSE fuera de muestra de bvar_m2 para el crecimiento trimestral real de precio real de compra (pp; misma muestra para todos los m… | 1,37 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-ecm_v1-pholm` | p ajustado por Holm del contraste Diebold-Mariano de ecm_v1 frente al AR(4) (precio real de compra) | 0,012 | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-OOS-c-ecm_v1-rmse` | RMSE fuera de muestra de ecm_v1 para el crecimiento trimestral real de precio real de compra (pp; misma muestra para todos los mo… | 2,62 pp | C4 | 2016T2-2026T1 | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-a-P2` | Probabilidad posterior de que empleo y renta sea el factor de mayor contribución en alquiler real en P2 (P(f*); condicionado a la… | 38,81 % | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-a-P3` | Probabilidad posterior de que demografía sea el factor de mayor contribución en alquiler real en P3 (P(f*); condicionado a las re… | 32,58 % | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-a-P4` | Probabilidad posterior de que demanda específica de vivienda (shock de M2, no pre-registrado como factor) sea el factor de mayor… | 24,48 % | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-a-P5` | Probabilidad posterior de que crédito y tipos sea el factor de mayor contribución en alquiler real en P5 (P(f*); condicionado a l… | 25,72 % | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-c-P1` | Probabilidad posterior de que empleo y renta sea el factor de mayor contribución en precio real de compra en P1 (P(f*); condicion… | 71,66 % | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-c-P2` | Probabilidad posterior de que empleo y renta sea el factor de mayor contribución en precio real de compra en P2 (P(f*); condicion… | 31,77 % | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-c-P3` | Probabilidad posterior de que empleo y renta sea el factor de mayor contribución en precio real de compra en P3 (P(f*); condicion… | 40,77 % | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-c-P4` | Probabilidad posterior de que empleo y renta sea el factor de mayor contribución en precio real de compra en P4 (P(f*); condicion… | 25,93 % | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-PFSTAR-c-P5` | Probabilidad posterior de que crédito y tipos sea el factor de mayor contribución en precio real de compra en P5 (P(f*); condicio… | 29,66 % | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-a-P2` | Cuota no atribuida de la variación de alquiler real en P2 (parte determinista y no identificada del SVAR, banda del 68 %; condici… | 0,459  (-1,91 a 2,78) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-a-P3` | Cuota no atribuida de la variación de alquiler real en P3 (parte determinista y no identificada del SVAR, banda del 68 %; condici… | 4,31  (-2,69 a 10,92) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-a-P4` | Cuota no atribuida de la variación de alquiler real en P4 (parte determinista y no identificada del SVAR, banda del 68 %; condici… | 0,338  (-0,149 a 0,865) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-a-P5` | Cuota no atribuida de la variación de alquiler real en P5 (parte determinista y no identificada del SVAR, banda del 68 %; condici… | 1,06  (-1,94 a 4,29) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-c-P1` | Cuota no atribuida de la variación de precio real de compra en P1 (parte determinista y no identificada del SVAR, banda del 68 %;… | 0,419  (-0,08 a 0,984) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-c-P2` | Cuota no atribuida de la variación de precio real de compra en P2 (parte determinista y no identificada del SVAR, banda del 68 %;… | 0,219  (-0,353 a 0,8) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-c-P3` | Cuota no atribuida de la variación de precio real de compra en P3 (parte determinista y no identificada del SVAR, banda del 68 %;… | 0,235  (-3,07 a 3,36) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-c-P4` | Cuota no atribuida de la variación de precio real de compra en P4 (parte determinista y no identificada del SVAR, banda del 68 %;… | 0,138  (-2,2 a 2,95) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-c-P5` | Cuota no atribuida de la variación de precio real de compra en P5 (parte determinista y no identificada del SVAR, banda del 68 %;… | 0,517  (-0,79 a 1,31) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-a-P2` | Cuota no atribuida de alquiler real en P2 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero de M2) | -1,24 pp (-7,52 a 5,16) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-a-P3` | Cuota no atribuida de alquiler real en P3 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero de M2) | -4,56 pp (-11,56 a 2,85) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-a-P4` | Cuota no atribuida de alquiler real en P4 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero de M2) | -3,16 pp (-8,08 a 1,39) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-a-P5` | Cuota no atribuida de alquiler real en P5 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero de M2) | -1,96 pp (-7,92 a 3,58) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-c-P1` | Cuota no atribuida de precio real de compra en P1 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero… | 31,56 pp (-6,04 a 74,13) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-c-P2` | Cuota no atribuida de precio real de compra en P2 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero… | -9,62 pp (-35,21 a 15,54) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-c-P3` | Cuota no atribuida de precio real de compra en P3 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero… | 1,93 pp (-25,19 a 27,64) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-c-P4` | Cuota no atribuida de precio real de compra en P4 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero… | -0,753 pp (-16,08 a 12) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-QNA-pp-c-P5` | Cuota no atribuida de precio real de compra en P5 en puntos (banda del 68 %; condicionado a las restricciones de signo y de cero… | 9,52 pp (-14,56 a 24,14) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-a-P1` | Resultado de la regla del §9 en alquiler real en P1: no designado (factor evaluado: factor europeo); 1 = designado, 0 = no design… | 0 designado | C4 | P1 (sin datos de alquiler) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-a-P2` | Resultado de la regla del §9 en alquiler real en P2: no designado (factor evaluado: empleo y renta); 1 = designado, 0 = no design… | 0 designado | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-a-P3` | Resultado de la regla del §9 en alquiler real en P3: no designado (factor evaluado: demografía); 1 = designado, 0 = no designado | 0 designado | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-a-P4` | Resultado de la regla del §9 en alquiler real en P4: no designado (factor evaluado: demanda específica de vivienda (shock de M2,… | 0 designado | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-a-P5` | Resultado de la regla del §9 en alquiler real en P5: no designado (factor evaluado: crédito y tipos); 1 = designado, 0 = no desig… | 0 designado | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-c-P1` | Resultado de la regla del §9 en precio real de compra en P1: no designado (factor evaluado: empleo y renta); 1 = designado, 0 = n… | 0 designado | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-c-P2` | Resultado de la regla del §9 en precio real de compra en P2: no designado (factor evaluado: empleo y renta); 1 = designado, 0 = n… | 0 designado | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-c-P3` | Resultado de la regla del §9 en precio real de compra en P3: no designado (factor evaluado: empleo y renta); 1 = designado, 0 = n… | 0 designado | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-c-P4` | Resultado de la regla del §9 en precio real de compra en P4: no designado (factor evaluado: crédito y tipos); 1 = designado, 0 =… | 0 designado | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-REGLA-c-P5` | Resultado de la regla del §9 en precio real de compra en P5: no designado (factor evaluado: crédito y tipos); 1 = designado, 0 =… | 0 designado | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-credito_tipos-media` | Contribución de crédito y tipos a la variación de alquiler real en P2 (media posterior; banda del 68 %; pp log×100; condicionado… | 0,256 pp (-1,46 a 2,13) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de alquiler real en P2 (mediana posterior; banda del 68 %; pp log×100; condicionad… | 0,334 pp (-1,46 a 2,13) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P2… | -0,323 pp (-2,32 a 1,85) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P2… | -0,08 pp (-2,32 a 1,85) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-demografia-media` | Contribución de demografía a la variación de alquiler real en P2 (media posterior; banda del 68 %; pp log×100; condicionado a las… | 0,328 pp (-1,86 a 2,71) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-demografia-mediana` | Contribución de demografía a la variación de alquiler real en P2 (mediana posterior; banda del 68 %; pp log×100; condicionado a l… | 0,224 pp (-1,86 a 2,71) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-empleo_renta-media` | Contribución de empleo y renta a la variación de alquiler real en P2 (media posterior; banda del 68 %; pp log×100; condicionado a… | -1,66 pp (-4,3 a 0,829) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-empleo_renta-mediana` | Contribución de empleo y renta a la variación de alquiler real en P2 (mediana posterior; banda del 68 %; pp log×100; condicionado… | -1,18 pp (-4,3 a 0,829) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-oferta-media` | Contribución de oferta a la variación de alquiler real en P2 (media posterior; banda del 68 %; pp log×100; condicionado a las res… | -0,058 pp (-1,97 a 1,91) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P2-oferta-mediana` | Contribución de oferta a la variación de alquiler real en P2 (mediana posterior; banda del 68 %; pp log×100; condicionado a las r… | 0,094 pp (-1,97 a 1,91) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-credito_tipos-media` | Contribución de crédito y tipos a la variación de alquiler real en P3 (media posterior; banda del 68 %; pp log×100; condicionado… | 0,237 pp (-1,74 a 2,68) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de alquiler real en P3 (mediana posterior; banda del 68 %; pp log×100; condicionad… | 0,162 pp (-1,74 a 2,68) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P3… | 0,665 pp (-1,36 a 2,9) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P3… | 0,63 pp (-1,36 a 2,9) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-demografia-media` | Contribución de demografía a la variación de alquiler real en P3 (media posterior; banda del 68 %; pp log×100; condicionado a las… | -0,0037 pp (-2,95 a 2,74) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-demografia-mediana` | Contribución de demografía a la variación de alquiler real en P3 (mediana posterior; banda del 68 %; pp log×100; condicionado a l… | -0,091 pp (-2,95 a 2,74) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-empleo_renta-media` | Contribución de empleo y renta a la variación de alquiler real en P3 (media posterior; banda del 68 %; pp log×100; condicionado a… | 1,73 pp (-1,12 a 4,8) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-empleo_renta-mediana` | Contribución de empleo y renta a la variación de alquiler real en P3 (mediana posterior; banda del 68 %; pp log×100; condicionado… | 1,38 pp (-1,12 a 4,8) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-oferta-media` | Contribución de oferta a la variación de alquiler real en P3 (media posterior; banda del 68 %; pp log×100; condicionado a las res… | 0,871 pp (-1,08 a 3,22) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P3-oferta-mediana` | Contribución de oferta a la variación de alquiler real en P3 (mediana posterior; banda del 68 %; pp log×100; condicionado a las r… | 0,557 pp (-1,08 a 3,22) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-credito_tipos-media` | Contribución de crédito y tipos a la variación de alquiler real en P4 (media posterior; banda del 68 %; pp log×100; condicionado… | -1,45 pp (-3,18 a 0,305) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de alquiler real en P4 (mediana posterior; banda del 68 %; pp log×100; condicionad… | -0,926 pp (-3,18 a 0,305) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P4… | -1,57 pp (-3,24 a 0,124) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P4… | -1,25 pp (-3,24 a 0,124) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-demografia-media` | Contribución de demografía a la variación de alquiler real en P4 (media posterior; banda del 68 %; pp log×100; condicionado a las… | -0,737 pp (-2,32 a 0,654) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-demografia-mediana` | Contribución de demografía a la variación de alquiler real en P4 (mediana posterior; banda del 68 %; pp log×100; condicionado a l… | -0,456 pp (-2,32 a 0,654) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-empleo_renta-media` | Contribución de empleo y renta a la variación de alquiler real en P4 (media posterior; banda del 68 %; pp log×100; condicionado a… | -0,811 pp (-2,83 a 0,641) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-empleo_renta-mediana` | Contribución de empleo y renta a la variación de alquiler real en P4 (mediana posterior; banda del 68 %; pp log×100; condicionado… | -0,636 pp (-2,83 a 0,641) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-oferta-media` | Contribución de oferta a la variación de alquiler real en P4 (media posterior; banda del 68 %; pp log×100; condicionado a las res… | -1,61 pp (-3,57 a 0,104) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P4-oferta-mediana` | Contribución de oferta a la variación de alquiler real en P4 (mediana posterior; banda del 68 %; pp log×100; condicionado a las r… | -1,12 pp (-3,57 a 0,104) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-credito_tipos-media` | Contribución de crédito y tipos a la variación de alquiler real en P5 (media posterior; banda del 68 %; pp log×100; condicionado… | -0,502 pp (-2,57 a 2,34) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de alquiler real en P5 (mediana posterior; banda del 68 %; pp log×100; condicionad… | -0,046 pp (-2,57 a 2,34) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P5… | -0,299 pp (-2,01 a 1,99) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de alquiler real en P5… | 0,00896 pp (-2,01 a 1,99) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-demografia-media` | Contribución de demografía a la variación de alquiler real en P5 (media posterior; banda del 68 %; pp log×100; condicionado a las… | 0,074 pp (-1,92 a 2,13) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-demografia-mediana` | Contribución de demografía a la variación de alquiler real en P5 (mediana posterior; banda del 68 %; pp log×100; condicionado a l… | 0,038 pp (-1,92 a 2,13) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-empleo_renta-media` | Contribución de empleo y renta a la variación de alquiler real en P5 (media posterior; banda del 68 %; pp log×100; condicionado a… | 0,472 pp (-1,87 a 2,1) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-empleo_renta-mediana` | Contribución de empleo y renta a la variación de alquiler real en P5 (mediana posterior; banda del 68 %; pp log×100; condicionado… | -0,055 pp (-1,87 a 2,1) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-oferta-media` | Contribución de oferta a la variación de alquiler real en P5 (media posterior; banda del 68 %; pp log×100; condicionado a las res… | 0,365 pp (-1,75 a 2,6) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-a-P5-oferta-mediana` | Contribución de oferta a la variación de alquiler real en P5 (mediana posterior; banda del 68 %; pp log×100; condicionado a las r… | 0,283 pp (-1,75 a 2,6) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-credito_tipos-media` | Contribución de crédito y tipos a la variación de precio real de compra en P1 (media posterior; banda del 68 %; pp log×100; condi… | 3,03 pp (-7,19 a 14,01) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de precio real de compra en P1 (mediana posterior; banda del 68 %; pp log×100; con… | 0,098 pp (-7,19 a 14,01) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-demografia-media` | Contribución de demografía a la variación de precio real de compra en P1 (media posterior; banda del 68 %; pp log×100; condiciona… | 8,94 pp (-4,99 a 24,78) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-demografia-mediana` | Contribución de demografía a la variación de precio real de compra en P1 (mediana posterior; banda del 68 %; pp log×100; condicio… | 4,75 pp (-4,99 a 24,78) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-empleo_renta-media` | Contribución de empleo y renta a la variación de precio real de compra en P1 (media posterior; banda del 68 %; pp log×100; condic… | 31,82 pp (9 a 54,65) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P1-empleo_renta-mediana` | Contribución de empleo y renta a la variación de precio real de compra en P1 (mediana posterior; banda del 68 %; pp log×100; cond… | 29,5 pp (9 a 54,65) | C3s | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-credito_tipos-media` | Contribución de crédito y tipos a la variación de precio real de compra en P2 (media posterior; banda del 68 %; pp log×100; condi… | -8,6 pp (-18,87 a 0,542) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de precio real de compra en P2 (mediana posterior; banda del 68 %; pp log×100; con… | -5,88 pp (-18,87 a 0,542) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -7,41 pp (-17,88 a 2) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -3,54 pp (-17,88 a 2) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-demografia-media` | Contribución de demografía a la variación de precio real de compra en P2 (media posterior; banda del 68 %; pp log×100; condiciona… | -2,93 pp (-10,71 a 4,05) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-demografia-mediana` | Contribución de demografía a la variación de precio real de compra en P2 (mediana posterior; banda del 68 %; pp log×100; condicio… | -1,6 pp (-10,71 a 4,05) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-empleo_renta-media` | Contribución de empleo y renta a la variación de precio real de compra en P2 (media posterior; banda del 68 %; pp log×100; condic… | -10,64 pp (-23,52 a 0,66) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-empleo_renta-mediana` | Contribución de empleo y renta a la variación de precio real de compra en P2 (mediana posterior; banda del 68 %; pp log×100; cond… | -7,57 pp (-23,52 a 0,66) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-oferta-media` | Contribución de oferta a la variación de precio real de compra en P2 (media posterior; banda del 68 %; pp log×100; condicionado a… | -4,81 pp (-13,3 a 2,49) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P2-oferta-mediana` | Contribución de oferta a la variación de precio real de compra en P2 (mediana posterior; banda del 68 %; pp log×100; condicionado… | -2,05 pp (-13,3 a 2,49) | C3s | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-credito_tipos-media` | Contribución de crédito y tipos a la variación de precio real de compra en P3 (media posterior; banda del 68 %; pp log×100; condi… | -1,55 pp (-9,78 a 7,07) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de precio real de compra en P3 (mediana posterior; banda del 68 %; pp log×100; con… | -0,685 pp (-9,78 a 7,07) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -0,412 pp (-7,21 a 8,99) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | 0,532 pp (-7,21 a 8,99) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-demografia-media` | Contribución de demografía a la variación de precio real de compra en P3 (media posterior; banda del 68 %; pp log×100; condiciona… | 0,142 pp (-6,58 a 6,81) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-demografia-mediana` | Contribución de demografía a la variación de precio real de compra en P3 (mediana posterior; banda del 68 %; pp log×100; condicio… | -0,177 pp (-6,58 a 6,81) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-empleo_renta-media` | Contribución de empleo y renta a la variación de precio real de compra en P3 (media posterior; banda del 68 %; pp log×100; condic… | 7,72 pp (-3,47 a 18,23) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-empleo_renta-mediana` | Contribución de empleo y renta a la variación de precio real de compra en P3 (mediana posterior; banda del 68 %; pp log×100; cond… | 5,22 pp (-3,47 a 18,23) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-oferta-media` | Contribución de oferta a la variación de precio real de compra en P3 (media posterior; banda del 68 %; pp log×100; condicionado a… | 0,381 pp (-7,29 a 8,02) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P3-oferta-mediana` | Contribución de oferta a la variación de precio real de compra en P3 (mediana posterior; banda del 68 %; pp log×100; condicionado… | 0,184 pp (-7,29 a 8,02) | C3s | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-credito_tipos-media` | Contribución de crédito y tipos a la variación de precio real de compra en P4 (media posterior; banda del 68 %; pp log×100; condi… | -1,29 pp (-4,72 a 4,44) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de precio real de compra en P4 (mediana posterior; banda del 68 %; pp log×100; con… | 0,116 pp (-4,72 a 4,44) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -2,61 pp (-6 a 2,42) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -0,694 pp (-6 a 2,42) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-demografia-media` | Contribución de demografía a la variación de precio real de compra en P4 (media posterior; banda del 68 %; pp log×100; condiciona… | -0,273 pp (-3,99 a 3,39) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-demografia-mediana` | Contribución de demografía a la variación de precio real de compra en P4 (mediana posterior; banda del 68 %; pp log×100; condicio… | 0,071 pp (-3,99 a 3,39) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-empleo_renta-media` | Contribución de empleo y renta a la variación de precio real de compra en P4 (media posterior; banda del 68 %; pp log×100; condic… | 0,273 pp (-7,09 a 4,66) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-empleo_renta-mediana` | Contribución de empleo y renta a la variación de precio real de compra en P4 (mediana posterior; banda del 68 %; pp log×100; cond… | -0,477 pp (-7,09 a 4,66) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-oferta-media` | Contribución de oferta a la variación de precio real de compra en P4 (media posterior; banda del 68 %; pp log×100; condicionado a… | -0,797 pp (-4,75 a 3,32) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P4-oferta-mediana` | Contribución de oferta a la variación de precio real de compra en P4 (mediana posterior; banda del 68 %; pp log×100; condicionado… | -0,285 pp (-4,75 a 3,32) | C3s | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-credito_tipos-media` | Contribución de crédito y tipos a la variación de precio real de compra en P5 (media posterior; banda del 68 %; pp log×100; condi… | -0,469 pp (-2,82 a 12,77) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-credito_tipos-mediana` | Contribución de crédito y tipos a la variación de precio real de compra en P5 (mediana posterior; banda del 68 %; pp log×100; con… | 3,37 pp (-2,82 a 12,77) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-demanda_vivienda-media` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | -0,302 pp (-2,87 a 10,98) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-demanda_vivienda-mediana` | Contribución de demanda específica de vivienda (shock de M2, no pre-registrado como factor) a la variación de precio real de comp… | 2,44 pp (-2,87 a 10,98) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-demografia-media` | Contribución de demografía a la variación de precio real de compra en P5 (media posterior; banda del 68 %; pp log×100; condiciona… | 0,647 pp (-4,08 a 5,79) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-demografia-mediana` | Contribución de demografía a la variación de precio real de compra en P5 (mediana posterior; banda del 68 %; pp log×100; condicio… | 0,615 pp (-4,08 a 5,79) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-empleo_renta-media` | Contribución de empleo y renta a la variación de precio real de compra en P5 (media posterior; banda del 68 %; pp log×100; condic… | 7,16 pp (-4,71 a 11,19) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-empleo_renta-mediana` | Contribución de empleo y renta a la variación de precio real de compra en P5 (mediana posterior; banda del 68 %; pp log×100; cond… | 1,1 pp (-4,71 a 11,19) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-oferta-media` | Contribución de oferta a la variación de precio real de compra en P5 (media posterior; banda del 68 %; pp log×100; condicionado a… | 1,87 pp (-3,25 a 9,03) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-SVAR-c-P5-oferta-mediana` | Contribución de oferta a la variación de precio real de compra en P5 (mediana posterior; banda del 68 %; pp log×100; condicionado… | 1,78 pp (-3,25 a 9,03) | C3s | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-a-P1` | Votos máximos (de 4 métodos) a un mismo factor en alquiler real en P1: factor europeo | 1 votos | C4 | P1 (sin datos de alquiler) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-a-P2` | Votos máximos (de 4 métodos) a un mismo factor en alquiler real en P2: empleo y renta | 2 votos | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-a-P3` | Votos máximos (de 4 métodos) a un mismo factor en alquiler real en P3: demografía | 1 votos | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-a-P4` | Votos máximos (de 4 métodos) a un mismo factor en alquiler real en P4: demanda específica de vivienda (shock de M2, no pre-regist… | 1 votos | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-a-P5` | Votos máximos (de 4 métodos) a un mismo factor en alquiler real en P5: crédito y tipos | 2 votos | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-c-P1` | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P1: empleo y renta | 1 votos | C4 | P1 (1995T1-2007T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-c-P2` | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P2: empleo y renta | 1 votos | C4 | P2 (2008T3-2013T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-c-P3` | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P3: empleo y renta | 2 votos | C4 | P3 (2014T1-2019T4) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-c-P4` | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P4: crédito y tipos | 2 votos | C4 | P4 (2020T2-2022T2) | [hechos.json](../output/v8/F6/hechos.json) |
| `V8-VOTOS-c-P5` | Votos máximos (de 4 métodos) a un mismo factor en precio real de compra en P5: crédito y tipos | 2 votos | C4 | P5 (2022T3-último dato) | [hechos.json](../output/v8/F6/hechos.json) |
| `HIST-046` | Demografía e inmigración · Alquiler real | P5 (2022T3-2026T2): 0,07 pp (-1,9 a 2,1 pp); multiverso: 2 de 74 combinaciones por famili… | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-047` | Tipos de interés y crédito · Precio real de compra | P5: -0,47 pp (-2,8 a 12,8 pp); P2: -8,6 pp (-18,9 a 0,54 pp) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-048` | Empleo y renta · Precio real de compra | P1 (larga): 31,8 pp (9,0-54,6 pp); P5: 7,2 pp (-4,7 a 11,2 pp) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-049` | Oferta · Precio real de compra | P5: 1,9 pp (-3,3 a 9,0 pp); P2: -4,8 pp (-13,3 a 2,5 pp) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-050` | Turismo y viviendas turísticas · Alquiler real | SHAP P5: -0,44 pp (-0,67 a 0,23 pp); CCAA con datos: 6 de 17 | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-051` | Demanda externa y compradores extranjeros · Precio real de compra | SHAP P5: 0,51 pp (0,10-0,71 pp) | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-052` | Factor europeo (nuevo en V8) · Crecimiento del precio de compra | correlación con la zona euro 0,60 (0,14-0,86); parte europea en P2: -15,3 pp (-21,7 a -7,… | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-053` | Un factor único (regla del §9) · Precio real de compra y alquiler real | 0 de 10 celdas designadas | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-054` | Predicción fuera de muestra · Crecimiento trimestral real | RMSE compra: AR(4) 1,2 pp, ECM v1 2,6 pp, BVAR 1,4 pp | C4 |  | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `FICHA-V8-V1` | Los tipos de interés bajos y el crédito abundante explican la subida del precio de la vivienda de compra. | ANALIZADA, NO CONCLUYENTE | C3s |  | [resumen.md](../output/v8/M2/resumen.md) |
| `FICHA-V8-V2` | El crecimiento de la población y la inmigración explican sobre todo la subida del alquiler. | ANALIZADA, NO CONCLUYENTE | C3s |  | [resumen.md](../output/v8/M2/resumen.md) |
| `FICHA-V8-V3` | El turismo y las viviendas de uso turístico explican la subida del alquiler. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resumen.md](../output/v8/M9/resumen.md) |
| `FICHA-V8-V4` | La demanda de compradores extranjeros es el principal motor de la subida del precio de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resumen.md](../output/v8/M9/resumen.md) |
| `FICHA-V8-V5` | La falta de construcción (oferta insuficiente) explica la subida del precio de la vivienda. | ANALIZADA, NO CONCLUYENTE | C3s |  | [resumen.md](../output/v8/M2/resumen.md) |
| `FICHA-V8-V6` | La mejora del empleo y de la renta explica la subida del precio de la vivienda. | ANALIZADA, NO CONCLUYENTE | C3s |  | [resumen.md](../output/v8/M2/resumen.md) |
| `FICHA-V8-V7` | La subida en España forma parte de un movimiento común europeo del precio de la vivienda. | ANALIZADA, NO CONCLUYENTE | C4 |  | [resumen.md](../output/v8/M1/resumen.md) |
| `FICHA-V8-V8` | Hay un único factor que explica la subida de la vivienda en cada periodo y se puede identificar. | ANALIZADA, NO CONCLUYENTE | C3s |  | [resumen.md](../output/v8/F5/resumen.md) |
| `FICHA-V8-V9` | Los modelos econométricos y de aprendizaje automático predicen el precio y el alquiler mejor que un modelo sencillo. | ANALIZADA, NO CONCLUYENTE | C4 |  | [fuera_muestra_comun.csv](../output/v8/F5/fuera_muestra_comun.csv) |

## Versión v1

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `HIST-001` | Inmigración (flujo neto) · Alquiler IPC (stock) | 0,534 (EE 0,167; p WCB 0,004); 2SLS 0,437 (p 0,119) | C4 | 2003-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-002` | Inmigración (flujo neto) · Precio IPV INE / valor tasado | IPV −0,454 (0,503); 2SLS −1,615 (IC95 −3,90; 0,67); Holm mínimo 0,051 | C4 | 2009-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-003` | Cuota de extranjeros · Δ ln IPV / valor tasado | 0,001 (p 0,77); tasado 0,016 (p cluster 0,010); 0,1-1,9 % por pp según alineación; Holm m… | C4 | 2009-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-011` | Empleo (ocupados) · Precio real | LP 1,482 (0,330), N=72; ECM cambia de signo antes de 2020 | C4 | 2008-2026 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-014` | Renta (PIB/renta del hogar) · IV del precio | renta como único instrumento defendible | C4 | 2008-2026 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-017` | Oferta (iniciadas) · Elasticidad de la oferta | 1,44 (0,21); Δ4 1,39 (0,63), no rechaza 0,45 | C4 | 2008-2026 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-022` | Tipos hipotecarios · Precio (ECM) | tipo real ≈0 en el largo plazo real | C4 | 2008-2026 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-036` | Predicción · RMSE fuera de muestra | no mejora al AR(4) (DM p 0,509) | C4 | 2008-2026 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Versión v10

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `V10-ATL-A1` | Sobrecarga del gasto en vivienda (>40 % de la renta), personas en alquiler de mercado | 26,8 % (24,4 a 29,19) | C1 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A10` | Personas de 30 a 34 años que viven con al menos uno de sus padres, primer año | 27,14 % (26,54 a 27,75) | C4 | 2018 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A11` | Personas de 30 a 34 años que viven con al menos uno de sus padres, último año completo | 31,68 % (30,84 a 32,52) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A2` | Sobrecarga del gasto en vivienda (>40 % de la renta), total de la población | 7,17 % (6,67 a 7,67) | C1 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A3` | Sobrecarga del gasto en vivienda (>40 %), alquiler de mercado, primer año de la serie | 38,07 % (34,15 a 41,99) | C1 | 2018 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A4` | Sobrecarga del gasto en vivienda (>40 %), primer decil de renta equivalente | 43,85 % (40,27 a 47,42) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A5` | Sobrecarga del gasto en vivienda (>40 %), décimo decil de renta equivalente | 0,057 % (-0,009 a 0,122) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A6` | Sobrecarga del gasto en vivienda (>40 %), nacionalidad de fuera de la UE | 24,05 % (20,64 a 27,46) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A7` | Sobrecarga del gasto en vivienda (>40 %), nacionalidad española | 4,71 % (4,38 a 5,04) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A8` | Esfuerzo mediano de alquiler (alquiler anual / renta del hogar), 18-29 años, alquiler de mercado | 21,14 % (19,81 a 23,16) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-A9` | Esfuerzo mediano de alquiler, 45-64 años, alquiler de mercado | 21,5 % (20,53 a 22,87) | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-B1` | Brecha IPVA contratos nuevos menos existentes (índices 2015=100) | 16,4 puntos de índice | C4 | 2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C1` | València: porcentaje de población de nacionalidad extranjera | 19,41 % | C4 | 2025 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C2` | València: porcentaje de población de nacionalidad extranjera | 13,31 % | C4 | 2021 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C3` | València: viviendas turísticas (INE, medición experimental) | 5.393 viviendas | C4 | 2026-05 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C4-462500101` | Índice descriptivo de presión residencial, barrio La Seu | 1,45 puntuación z media | C4 | 2019-2026 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C4-462500104` | Índice descriptivo de presión residencial, barrio El Pilar | 1,73 puntuación z media | C4 | 2019-2026 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C4-462500105` | Índice descriptivo de presión residencial, barrio El Mercat | 2,25 puntuación z media | C4 | 2019-2026 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C4-462501006` | Índice descriptivo de presión residencial, barrio La Punta | 1,59 puntuación z media | C4 | 2019-2026 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-C4-462501102` | Índice descriptivo de presión residencial, barrio Cabanyal-Canyamelar | 1,21 puntuación z media | C4 | 2019-2026 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-D1` | Alquiler anual de 80 m² sobre la renta neta por persona, rango provincial | 42,26 % (28,59 a 66,87) | C4 | alquiler 2024; renta 2023 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-D2` | Variación del alquiler mediano 2019-2024, municipios de la Comunitat Valenciana con 20.000 hab. o más | 31,93 % (19,1 a 48,52) | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-03014` | Variación del alquiler mediano 2019-2024, Alicante/Alacant | 31,27 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-07040` | Variación del alquiler mediano 2019-2024, Palma | 24,6 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-29067` | Variación del alquiler mediano 2019-2024, Málaga | 31,36 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-41091` | Variación del alquiler mediano 2019-2024, Sevilla | 21,38 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-46250` | Variación del alquiler mediano 2019-2024, València | 39,77 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |
| `V10-ATL-E-50297` | Variación del alquiler mediano 2019-2024, Zaragoza | 21,31 % | C4 | 2019-2024 | [hechos.json](../output/v10/atlas/hechos.json) |

## Versión v2

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `HIST-005` | Población extranjera (Δ4 ln) · Alquiler IPC | −0,018 [−0,054; 0,017] | C4 | 2008T1-2024T2 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-012` | Empleo (Δ4 ln ocupados) · Precio real de compra | 0,044 | C4 | 2004-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-016` | Iniciadas libres (elasticidad a precio) · Iniciadas, respuesta al precio real | β 0,79; interacción con suelo −0,62; p IUT 0,046 | C4 | 2005-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-023` | Crédito nuevo y coste de uso · Precio real de compra | 0,0087; −0,0044; sin valor predictivo en sellado | C4 | 2004-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-025` | Topes de renta catalanes (Ley 11/2020) · Alquiler IPC (stock) | +0,0037 en ln (2020T4-2022T1); falla pretendencias | C4 | 2016-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-027` | Zonas tensionadas (H6) · Alquiler IPC (stock) | τ −0,0117 en ln; p 0,014; Holm-7 0,098 | C4 | 2016-2023 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-037` | Demografía (20-34) · Alquiler y su predicción | RMSE 0,0108 frente a 0,0122 del AR(4) (DM-HLN p 0,005) | C4 | 2008-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Versión v3

| id | enunciado | cifra | capa | periodo | origen |
|---|---|---|---|---|---|
| `HIST-006` | Inmigración · Cotas de cantidad (hogares extranjeros) | cuota máxima 100 % (no informativa) | C4 | 2014-2025 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-019` | Turísticos (VUT) · Alquiler SERPAVI | +0,0003 por 100 viviendas (p aj. 0,47); GL −0,0042 | C4 | 2016-2024; 2021-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |
| `HIST-020` | Turísticos · Cota de cantidad | como máximo 2,75 % del stock de alquiler (81.771 viviendas) | C2 | 2020-2024 | [historial_conclusiones.md](../metodologia/historial_conclusiones.md) |

## Superadas y retiradas (no citar)

Cada fila indica por qué ya no vale y, si existe, la cifra que la sustituye.

| id | estado | enunciado | sustituida por / motivo |
|---|---|---|---|
| `deficit_2124_c1` | superada | Déficit acumulado: aumento de hogares menos viviendas terminadas, sin bajas | L3-DEF-2124-SINBAJAS superada en v6.2: rango C1 con una sola corrección de la EPA; pasa a cota C2 con 8 variantes |
| `deficit_2124_c2` | superada | Déficit acumulado con bajas del parque supuestas del 0,1-0,2 % anual (cota) | L3-DEF-2124-BAJAST1 superada: bajas SUPUESTAS del 0,1-0,2 % anual (v4) sin respaldo observado; máximo 902.808 |
| `B1-H1` | superada | Necesidad total de vivienda por año (A+R+V+F-M-K), suma de 52 provincias | T3-H5b superada en v5.1: necesidad de v5 (B1); la vigente es la recalculada en T3 |
| `T3-H1` | superada | Déficit acumulado sin bajas (12 combinaciones de M0: 4 de fuentes; las bajas a 0) | L3-DEF-2124-SINBAJAS superada en v6.2: mismas 4 combinaciones de fuentes que deficit_2124_c1 (C1 retirado) |
| `T3-H2` | superada | Déficit acumulado con las bajas estimadas de T1 (4 fuentes x tasa 0 / central / máx.) | L3-DEF-2124-BAJAST1 superada en v6.2: bajas estimadas T1 sobre las 4 combinaciones antiguas de M0; máximo 744.144 |
| `T3-H3` | superada | Nuevo máximo del déficit 2021-2024 frente al máximo del supuesto antiguo de bajas 0,1-0,2 % (902.808) | L3-DEF-2124-BAJAST1 superada: compara con el supuesto antiguo de bajas (902.808), ya retirado |
| `T3-H4` | superada | Déficit 2021-2025 con las bajas estimadas de T1 (ECP, con y sin protegida) | L3-DEF-2125 retirada en v7.2: déficit 2021-2025 con bajas T1 sobre las combinaciones antiguas de M0 (solo ECP); se publica una sola cifra con bajas (2021-2024) |
| `HIST-031` | superada | Bajas y déficit con bajas · Viviendas |  |
| `HIST-032` | superada | Necesidad 2026-2035 · Viviendas/año |  |
| `HIST-010` | superada | Cuota de extranjeros · PIP del BMA |  |
| `HIST-013` | superada | Empleo · Valor tasado |  |
| `HIST-015` | superada | Renta (PIB por habitante) · Alquiler; valor tasado |  |
| `HIST-018` | superada | Iniciadas libres · Alquiler SERPAVI (stock); volumen |  |
| `L3-DEF-2124-CONBAJAS` | superada | Déficit acumulado 2021-2024 con bajas supuestas 0,1-0,2 % anual (cota) | L3-DEF-2124-BAJAST1 superada en v7.2: mismas variantes L3 con bajas SUPUESTAS del 0,1-0,2 % anual; máximo 924.658 |
| `HIST-030` | superada | Déficit 2021-2024 sin bajas · Viviendas (hogares − terminadas) |  |
| `V7-R6-a_construccion-esfuerzo10a` | superada | Variacion del esfuerzo de compra a 10 anos si se aplicase a_construccion (mediana entre CCAA, rejilla) | V71-S3-R6-a_construccion-compra-precio10a superada en v7.2: dosis de construcción adicional nula en 14 CCAA; reestimada con dosis no nula |
| `V7-R6-f2_impuestos_construccion-esfuerzo10a` | superada | Variacion del esfuerzo de compra a 10 anos si se aplicase f2_impuestos_construccion (mediana entre CCAA, reji… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V7-R6-n-robustas` | superada | Combinaciones CCAA x instrumento x mercado robustas | V71-S3-R6-*-robustas superada en v7.2: incluía la construcción adicional con dosis nula y la rebaja de impuestos a la construcción (no difundible) |
| `V71-S1-f2_impuestos_construccion-compra-coste_anual_meur` | superada | Coste fiscal anual aproximado, rebaja de impuestos y costes de construcción (no difundible), compra, 10 años… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S1-f2_impuestos_construccion-compra-coste_por_punto_meur` | superada | Coste anual por punto de reducción del precio neto pagado, rebaja de impuestos y costes de construcción (no d… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S1-f2_impuestos_construccion-compra-efecto_100meur_mercado` | superada | Variación del precio de mercado por cada 100 M€ anuales, rebaja de impuestos y costes de construcción (no dif… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S3-R6-f2_impuestos_construccion-alquiler-precio10a` | superada | Variación del alquiler de mercado a 10 años si se aplicase «rebaja de impuestos y costes de construcción» (es… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S3-R6-f2_impuestos_construccion-alquiler-robustas` | superada | CCAA en las que «rebaja de impuestos y costes de construcción» es robusta en alquiler (esfuerzo baja en todas… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S3-R6-f2_impuestos_construccion-compra-precio10a` | superada | Variación del precio de compra de mercado a 10 años si se aplicase «rebaja de impuestos y costes de construcc… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `V71-S3-R6-f2_impuestos_construccion-compra-robustas` | superada | CCAA en las que «rebaja de impuestos y costes de construcción» es robusta en compra (esfuerzo baja en todas l… | — no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción |
| `RET-H8-1` | retirada | En P5, la contribucion del shock demografico a la subida del alquiler real es positiva | especificación errónea (escalón EPA), retirada |
| `RET-H8-2` | retirada | En P5, la contribucion de credito y tipos al precio real de compra es negativa | especificación errónea (escalón EPA), retirada |
| `RET-H8-3` | retirada | En P3, la contribucion de actividad y renta al precio real de compra es positiva | especificación errónea (escalón EPA), retirada |
| `RET-H8-4` | retirada | En P2, la contribucion conjunta de credito y tipos y de actividad y renta al precio real de compra es negativa | especificación errónea (escalón EPA), retirada |
| `HIST-004` | superada | Inmigración (flujo/pob., shift-share 2002) · Alquiler IPC; valor tasado real |  |
| `HIST-026` | superada | Topes de renta · Renta y nº de contratos nuevos (fianzas) |  |
| `HIST-028` | superada | Déficit acumulado · Viviendas (hogares − terminadas) |  |
