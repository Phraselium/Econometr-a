# Atlas multiescala V16 (fase 2.3): capa C4, descriptivo

Generado por `src/v16/f2_atlas.py` (SEED 20261010); no editar a mano. Fecha del dato: cada fila lleva su periodo; construcción 2026-10-17. Ninguna frase atribuye causas: son coincidencias territoriales. Amplía el atlas de V10 (`output/v10/atlas_descriptivo.md`: coste por grupo social, València, Comunitat Valenciana y provincias) con renta ADRH 2015-2023 completa, turismo, parque, lanzamientos e intervenciones, a todas las escalas disponibles; no repite sus tablas.

<a id="cobertura"></a>
## Cobertura y unidades en blanco por validación sellada

Salida: `atlas.parquet` (formato largo: territorio_codigo, nivel, periodo, indicador, valor, ic_inf, ic_sup, calidad, suprimida, fuente; más unidad, n_base y cv). Escalas: España, CCAA, provincia, partido judicial, municipio, distrito y sección censal. **Área urbana funcional: sin correspondencia en `data/base/geo` ni en territorios; no se produce** (los mapas usan el municipio y la sección).

Las unidades de la muestra sellada (v6, V15 y V16, `holdout.unidad_sellada_v16`) **están en blanco por validación sellada, no por falta de dato**: no figuran en el fichero ni en los mapas con valor. Las ocho CCAA de la decisión K8 (Aragón, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra y La Rioja) aparecen solo a escala de CCAA y nación; nunca como provincia ni por debajo. Unidades selladas (recuento): provincia 11 de 52; municipio 3280 de 8205; distrito 4361 de 10552; seccion 19522 de 37663; partido_judicial 97 de 427.

<a id="supresion"></a>
## Incertidumbre y supresión

- **Supresión**: base < 10 unidades (contratos, anuncios, hogares, viviendas, personas o recuento) o CV > 30 % => valor en blanco y `suprimida = True`; el motivo queda en `calidad`. Filas suprimidas: 71,717 de 1,586,227. Motivos: suprimida: base < 10 (51385); valor sustituto de provincia/comarca: no se muestra como municipal (20196); suprimida: CV > 30 % (136).
- **Intervalos al 95 %** solo donde hay error de estimación: (i) alquiler SERPAVI municipal y provincial, aproximación normal a la mediana con SE = 1,2533·(P75−P25)/1,349/√n; (ii) esfuerzo municipal y provincial, que propaga solo el intervalo del alquiler (la renta ADRH es un registro); (iii) sobreesfuerzo ECV por CCAA, bootstrap de `f2_esfuerzo`. Sección y distrito: sin n ni intervalo por celda; el n de base se acota con el del municipio (si el municipio tiene n < 10, la celda se suprime).
- **Registros administrativos** (ADRH, padrón, Censo 2021, CGPJ, SERPAVI en niveles finos): sin intervalo, con marca de calidad (cota inferior/superior por secreto estadístico, estimación experimental INE-VTE, rastreo de plataforma no validado). Los **valores sustitutos de provincia o comarca del ADRH no se muestran como municipales** (suprimidos, con su marca). No hay interpolaciones. Inside Airbnb es un rastreo no validado y no exhaustivo: solo descriptivo.

<a id="esfuerzo"></a>
## Construcción de la ratio de esfuerzo

`esfuerzo = 100 · (mediana SERPAVI de €/m² y mes, tipología colectiva) · 12 · 80 m² / renta neta media del hogar (ADRH)`, mismo año (2015-2023), por provincia, municipio, distrito y sección. La superficie de 80 m² es un supuesto de vivienda tipo (como en V10), no la superficie observada. SERPAVI mide el stock de contratos declarados, no los contratos nuevos; la renta es la de todos los hogares de la unidad, no solo la de los inquilinos. **No es la tasa de sobreesfuerzo de la ECV** (que se muestra aparte por CCAA, `ecv_sobreesfuerzo_30/40_ccaa`, con otro universo y otra definición) y no debe compararse con ella.

## Límites de cobertura
- Valor tasado MIVAU: provincia, CCAA y nación; a escala municipal solo València (el MIVAU publica los municipios con nombre, no con código INE).
- Vacías y esporádicas (Censo 2021, tabla 59531): municipios que el INE publica; en la tabla del Censo el «vacío» por consumo eléctrico y las no principales son la misma fuente, no dos (C4).
- Viviendas turísticas: INE VTE (agosto de 2020, 2022 y 2024, mayo de 2026) e Inside Airbnb (última instantánea por unidad). Los registros autonómicos de Madrid, Canarias y Baleares no se usan (K8).
- Lanzamientos: CGPJ. Provincia: suma anual 2013-2025 de trimestres completos (Cádiz incluye Ceuta y Málaga incluye Melilla). Partido judicial: agregado propio 2013-2024 (suma de 12 años); tasa con las viviendas del Censo 2021 de sus municipios. CCAA: series por TSJ. Solo agregados; ningún fichero de microdatos del CGPJ sale de este módulo.
- Intervenciones: `output/v16/f1/intervenciones.csv`, vigentes a la fecha del dato; la ausencia de fila no equivale a ausencia de regulación.
- Distrito y sección: todos los años disponibles de cada fuente (ADRH 2015-2023, SERPAVI 2015-2024).

## Índice por escala e indicador

| indicador | escalas (unidades con valor en el último periodo) | periodos | filas | suprimidas | fuente |
|---|---|---|---|---|---|
| alquiler_m2_mediana | provincia 41; municipio 1390; distrito 2236; seccion 11440 | 2015..2024 | 136381 | 42 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler de |
| anuncios_activos_ia | municipio 165; seccion 1014 | 2025-12-14..2026-09-28 | 2976 | 1797 | Inside Airbnb (rastreo de anuncios de plataforma; no exhaust |
| anuncios_activos_ia_por_100_viviendas | municipio 165; seccion 1011 | 2025-12-14..2026-09-28 | 2963 | 1787 | Inside Airbnb (rastreo de anuncios de plataforma; no exhaust |
| anuncios_vivienda_entera_ia | municipio 138; seccion 826 | 2025-12-14..2026-09-28 | 2976 | 2012 | Inside Airbnb (rastreo de anuncios de plataforma; no exhaust |
| ecv_sobreesfuerzo_30_ccaa | ccaa 19 | 2004..2025 | 418 | 20 | INE, ECV (microdatos; f2_esfuerzo) |
| ecv_sobreesfuerzo_40_ccaa | ccaa 19 | 2004..2025 | 418 | 40 | INE, ECV (microdatos; f2_esfuerzo) |
| esfuerzo_alquiler_renta_hogar | provincia 39; municipio 1338; distrito 2146; seccion 10773 | 2015..2023 | 120530 | 38 | MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler de |
| gini | nacional 1; ccaa 19; provincia 41; municipio 3989; distrito 5224; seccion 16599 | 2015..2023 | 231489 | 0 | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 20 |
| intervencion_vut_municipal_vigente | municipio 2 | 2026-10-17 | 2 | 0 | output/v16/f1/intervenciones.csv (normativa verificada en F1 |
| intervencion_zona_tensionada_vigente | municipio 234 | 2026-10-17 | 234 | 0 | output/v16/f1/intervenciones.csv (normativa verificada en F1 |
| lanzamientos_hipotecaria | provincia 34 | 2013..2025 | 507 | 25 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_hipotecaria_acum_2013_2024 | partido_judicial 315 | 2013-2024 | 330 | 15 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_lau | provincia 39 | 2013..2025 | 507 | 0 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_lau_acum_2013_2024 | partido_judicial 326 | 2013-2024 | 330 | 4 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_total | ccaa 17; provincia 39 | 2013..2025 | 541 | 0 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_total_acum_2013_2024 | partido_judicial 330 | 2013-2024 | 330 | 0 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_total_por_10000_viviendas | provincia 39 | 2013..2025 | 507 | 0 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| lanzamientos_total_por_10000_viviendas_acum_2013_2024 | partido_judicial 330 | 2013-2024 | 330 | 0 | CGPJ, estadística judicial (agregado propio; tercero no redi |
| p80_p20 | nacional 1; ccaa 19; provincia 41; municipio 3989; distrito 5224; seccion 16599 | 2015..2023 | 231398 | 0 | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 20 |
| plazas_turisticas_ine | nacional 1; ccaa 19; provincia 41; municipio 1104 | 2020-08..2026-05 | 19614 | 15244 | INE, Viviendas turísticas en España (VTE), medición experime |
| poblacion_extranjera_pct | provincia 41; municipio 4857; seccion 17465 | 2021..2025 | 32202 | 45 | INE, Censo anual de población |
| precio_noche_mediana_ia | municipio 153; seccion 934 | 2026-03-21..2026-09-28 | 1848 | 761 | Inside Airbnb (rastreo de anuncios de plataforma; no exhaust |
| renta_media_hogar | nacional 1; ccaa 19; provincia 41; municipio 3986; distrito 5221; seccion 16593 | 2015..2023 | 241965 | 10098 | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 20 |
| renta_media_persona | nacional 1; ccaa 19; provincia 41; municipio 3986; distrito 5221; seccion 16593 | 2015..2023 | 241965 | 10098 | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 20 |
| renta_mediana_uc | nacional 1; ccaa 19; provincia 41; municipio 3986; distrito 5221; seccion 16593 | 2015..2023 | 231599 | 0 | INE, Atlas de Distribución de Renta de los Hogares (ADRH) 20 |
| saldo_migratorio_exterior_por_mil | municipio 4858 | 2021..2024 | 19472 | 41 | INE, Estadística de Migraciones y Cambios de Residencia (EMC |
| valor_tasado_m2 | nacional 1; ccaa 17; provincia 38; municipio 1 | 2015..2026T2 | 684 | 0 | MIVAU, valor tasado de vivienda libre (€/m², media anual de  |
| viviendas_no_principales_pct | nacional 1; ccaa 19; provincia 41; municipio 4867; seccion 16616 | 2021 | 21545 | 1 | INE, Censo de Población y Viviendas 2021 |
| viviendas_turisticas_ine | nacional 1; ccaa 19; provincia 41; municipio 1104 | 2020-08..2026-05 | 19614 | 15244 | INE, Viviendas turísticas en España (VTE), medición experime |
| viviendas_turisticas_pct_ine | nacional 1; ccaa 19; provincia 41; municipio 1104 | 2020-08..2026-05 | 18770 | 14405 | INE, Viviendas turísticas en España (VTE), medición experime |
| viviendas_uso_esporadico_pct | nacional 1; ccaa 19; provincia 41; municipio 1830 | 2021 | 1891 | 0 | INE, Censo de Población y Viviendas 2021, tabla 59531 (consu |
| viviendas_vacias_pct | nacional 1; ccaa 19; provincia 41; municipio 1830 | 2021 | 1891 | 0 | INE, Censo de Población y Viviendas 2021, tabla 59531 (consu |

<a id="dispersion"></a>
## Dispersión territorial (resumen)

| id | magnitud | P90/P10 | mínimo | máximo | periodo |
|---|---|---|---|---|---|
| V16-ATL-DISP-RENTA-HOGAR | «Renta neta media del hogar (ADRH)» entre municipios no sellados | 1.756 | 17450.0 | 85692.0 | 2023 |
| V16-ATL-DISP-RENTA-UC-SECCION | «Renta mediana por unidad de consumo (ADRH), entre secciones» entre seccions no sellados | 1.78 | 7350.0 | 44450.0 | 2023 |
| V16-ATL-DISP-ALQUILER-M2 | «Alquiler mediano €/m² y mes (SERPAVI)» entre municipios no sellados | 2.493 | 1.837 | 13.99 | 2024 |
| V16-ATL-DISP-ESFUERZO | «Ratio alquiler anual de 80 m² / renta neta media del hogar» entre municipios no sellados | 1.912 | 5.146 | 32.853 | 2023 |
| V16-ATL-DISP-ESFUERZO-SECCION | «Ratio alquiler anual de 80 m² / renta neta media del hogar, entre secciones» entre seccions no | 2.495 | 3.851 | 70.779 | 2023 |
| V16-ATL-DISP-VT-PCT | «Viviendas turísticas, % de las viviendas (INE VTE)» entre municipios no sellados | 23.608 | 0.05 | 18.24 | 2026-05 |
| V16-ATL-DISP-VACIAS | «Viviendas vacías por consumo eléctrico, % (Censo 2021)» entre municipios no sellados | 4.817 | 2.28 | 76.789 | 2021 |
| V16-ATL-DISP-NO-PRINCIPALES | «Viviendas no principales, % (Censo 2021)» entre municipios no sellados | 2.961 | 4.822 | 96.117 | 2021 |
| V16-ATL-DISP-EXTRANJERA | «Población de nacionalidad extranjera, % (censo anual)» entre municipios no sellados | 17.804 | 0.0 | 88.403 | 2025 |
| V16-ATL-DISP-PRECIO-PROV | «Valor tasado €/m², entre provincias» entre provincias no sellados | 2.709 | 854.2 | 3514.6 | 2026T2 |
| V16-ATL-DISP-LANZ-PJ | «Lanzamientos por 10.000 viviendas, suma 2013-2024, entre partidos judiciales» entre partido ju | 8.491 | 7.098 | 594.342 | 2013-2024 |
| V16-ATL-DISP-ECV40-CCAA | «Sobreesfuerzo del 40 % (ECV), entre CCAA» entre ccaas no sellados | 2.012 | 3.478 | 13.813 | 2025 |

## Mapas

`mapas/<área>_municipio.png` (municipios de la provincia) y `mapas/<área>_seccion.png` (secciones del municipio) para Barcelona, València y Sevilla (ninguna está sellada a escala de municipio; algunos distritos y secciones sí lo están y salen en gris hachurado). Seis paneles: renta mediana por unidad de consumo 2023, alquiler €/m² 2024, esfuerzo 2023, viviendas turísticas (INE VTE % por municipio; anuncios de Inside Airbnb por 100 viviendas por sección), población extranjera (censo anual 2025 por municipio; padrón 2022 por sección) y viviendas no principales (Censo 2021). Gris claro: sin dato o suprimida; gris hachurado: validación sellada.

## Summary (English)

Descriptive multiscale atlas (layer C4) of income (ADRH), rents (SERPAVI), appraised prices, rent-to-income ratio, tourist dwellings, foreign population, housing stock and vacancies, evictions and tenancy-related interventions, with 95 % intervals where there is estimation error and suppression of cells with fewer than 10 base units or CV above 30 %. Sealed-validation units are blank by design, not for lack of data. No causal claims.
