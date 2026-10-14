# Figuras de publicación (V10)

Generadas por `make figuras` (src/v10/figuras.py); no editar a mano.
Paleta Okabe-Ito (apta para daltonismo); mapas con «cividis» (secuencial) o «PuOr» (divergente).

| id | título | fuente | dato | capa | nota |
|---|---|---|---|---|---|
| F01_sobrecarga_tenencia | Sobrecarga del gasto en vivienda (>40 %) por tenencia, 2018-2025 | INE, ECV (microdatos), cálculo propio; contraste con Eurostat ilc_lvho07c | ECV 2018-2025 (renta del año anterior) | C1 en propiedad y alquiler de mercado (coinciden con Eurostat ≤0,5 p. todos los años); C4 en alquiler inferior al de mercado y cesión | Bandas: IC 95 % por linealización (sin estratos públicos). |
| F02_esfuerzo_alquiler_grupos | Esfuerzo mediano de alquiler por edad, nacionalidad y decil, 2025 | INE, ECV (microdatos), cálculo propio | ECV 2025 | C4 | Mediana ponderada; IC 95 % de Woodruff. Personas que viven en hogares de alquiler a precio de mercado. Línea: 30 %. |
| F03_ipva_brecha_ccaa | Brecha entre contratos nuevos y existentes (IPVA) por CCAA | INE, Índice de Precios de Vivienda en Alquiler (59004) | 2024 | C4 | Índices encadenados: comparan crecimientos desde 2015, no niveles. |
| F04_contratos_nuevos_existentes | IPVA: contratos nuevos frente a existentes, España 2015-2024 | INE, IPVA (59004) | 2015-2024 | C4 | Figura clave de V5 (contratos nuevos frente a vigentes), regenerada desde la base. |
| F05_mapa_provincias_alquiler_renta | Alquiler de 80 m² sobre la renta neta por persona, 2024 | MIVAU SERPAVI; INE ADRH y censo anual | alquiler 2024; renta 2023 | C4 | Indicador comparativo (vivienda tipo de 80 m²; renta por persona). Canarias recolocada. |
| F06_mapa_deficit_provincias | Déficit de vivienda 2021-2025 por 1.000 habitantes (mediana) | Resultado publicado V5 (A4) desde la base; INE censo anual | 2021-2025 | C4 | Mediana de las variantes de A4; rango en la base (estadístico min/max). Figura clave de V5. |
| F07_mapa_cv_alquiler | Comunitat Valenciana: variación del alquiler 2019-2024 | MIVAU SERPAVI (stock de contratos) | 2019-2024 | C4 | Mediana €/m² de vivienda colectiva; municipios sin dato en gris. |
| F08_mapa_valencia_indice | València: índice descriptivo de presión residencial por barrio | INE (censo anual, viviendas turísticas, Censo 2021), MIVAU SERPAVI, Ajuntament de València | 2019-2026 | C4 | Media de puntuaciones z de 4 componentes (alquiler 2024, su variación 2019-2024, viviendas turísticas por 100 viviendas y cambio del % de extranjeros). Solo descriptivo. |
| F09_mapa_valencia_vut | València: viviendas turísticas por 100 viviendas, mayo de 2026 | INE, medición experimental de viviendas turísticas; Censo 2021 | 2026-05 | C4 | Denominador: viviendas del Censo 2021. Escala truncada al percentil 98. |
| F10_ciudades_alquiler | Alquiler mediano 2015-2024: València y ciudades comparables | MIVAU SERPAVI | 2015-2024 | C4 | Bilbao solo 2024 (territorios forales). Sin inferencia causal. |
| F11_factor_comun | Factor común de precios (V8 M1) | Resultado publicado V8 (M1) desde la base | 1996T1-2026T2 | C4 | Figura clave de V8 regenerada desde la base. |
| F12_descomposicion_periodos | Descomposición por periodo (V8, atribución con bandas del 68 %) | Resultado publicado V8 (F5, atribución combinada) desde la base | periodos P1-P5 de V8 | C3s | C3s: condicionada a las restricciones de signo explícitas. Figura clave de V8. |
| F13_cotas_c2 | Cotas C2 publicadas (verificador) | publicacion/cifras_clave.csv desde la base | según cada cifra | C2 | Cotas de Manski con supuestos explícitos (ver la ficha de cada cifra). |
| F14_emancipacion_epa | Jóvenes que viven con sus padres (EPA), 2018-2026 | INE, EPA (microdatos), cálculo propio | 2018T1-2026T2 (2026: media de T1-T2) | C4 | Media anual de trimestres; IC en la tabla del atlas. |
