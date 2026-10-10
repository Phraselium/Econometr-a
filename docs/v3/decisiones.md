# Decisiones v3

Formato: fecha · decisión · motivo. Las desviaciones del pre-registro (`prereg-v3`) se anotan aquí con motivo.

## Setup (2026-10-10)
- Rama r3/main desde r2/main (841c695). CLAUDE.md adaptado a v3 (19 líneas); los agentes apuntan a src/v3, output/v3, docs/v3. El reviewer v3 no reproduce el pipeline (lo hace el orquestador con `make check` y `make all` ×2). Revisa solo identificación, capas, neutralidad y conclusiones.
- `make check` no existía en v2: se crea (ruff + pytest + `src/v3/check_texto.py`). `check_texto.py` busca tres cosas:
  1. léxico valorativo o partidista y alusiones a partidos o personas en los textos v3;
  2. promoción de capa (lenguaje causal en fichas o párrafos C1, C2 o C4);
  3. fichas del verificador incompletas.
- Ventanas: se reutiliza el sellado v2 (2024Q3-2026Q2 y provincias 11, 16, 45) para lo provincial ya analizado. El sellado v3 propio es por sección censal: 20 % de los bloques espaciales de distritos más la última oleada. Se aplica solo a P-C.
- Bloques espaciales sin cartografía:
  - En municipios con ≥2 distritos, cada bloque es un par de distritos con numeración consecutiva. En las ciudades españolas la numeración de distritos suele ser contigua; esto es un supuesto, documentado.
  - En municipios de un solo distrito, el bloque es el municipio.
  - Si se obtiene la cartografía de secciones (INE), se sustituye por bloques de contigüidad antes del pre-registro.
- Magnitudes en €/mes, % y viviendas. Holm en confirmatorias v3; BH en exploratorias.
- Para P-A (C1) y P-B (C2) se usan los paneles COMPLETOS. Se leen con `holdout.load_full(nombre, uso)`, que solo funciona si ya existen las 4 evaluaciones selladas de v2 (H1, H2, H6 y H7) y registra cada lectura con el evento «v3_completo». El sellado v2 ya no protege ninguna hipótesis pendiente.
- La especificación de P-A y P-B (docs/v3/especificacion_PA_PB.md) se fija ANTES de calcular. También fija el efecto económicamente relevante de cada diseño P-C, que decide el go/no-go por potencia.
- Las solicitudes de transparencia están redactadas pero no presentadas: exigen la identificación electrónica de una persona física. La cota de grandes tenedores queda en espera, con la ingesta preparada.

## D2 descarga de datos nuevos (2026-10-10)
- SERPAVI por sección y distrito: se extrae de la hoja «Secciones censales» y «Distritos» del xlsx ya usado en v2 (no hace falta red). Es el STOCK de contratos declarados en el IRPF, no contratos nuevos; amortigua los cambios de precio. Cuadre sección→municipio con la hoja «Municipios» (recuento BI_ALVHEPCO VC+VU): coincidencia exacta en la mayoría de pares municipio-año (≥99,99 % redondeado), máximo desfase 103 viviendas, sin corregir. La versión valenciana de v2 (serpavi_valencia_secciones.csv) se mantiene y solapa con la nueva.
- Incasòl (fianzas): flujo de contratos depositados. Dataset Socrata qww9-bvhh (municipal, 2007-2026). Las bandas de precio cambian entre años: no se empalman. «renda» es la media de la banda, no del municipio; la serie TOTAL_bandas es suma de bandas (no es un dato publicado). Las filas sin renda (19.964) quedan NaN.
- Madrid: el único conjunto encontrado es alquiler medio por código postal (1934258, 2023-2024). No es municipio ni distrito; el origen de los datos no está verificado.
- Eurostat: ilc_lvps08 (18-34 con padres) y ilc_lvho02 (tenencia × tipo de hogar, rskpovth = TOTAL). Las celdas ':' de Eurostat no aparecen en el JSON y no se rellenan. Cuadre: OWN_L + OWN_NL = OWN, OWN + RENT = 100 % (España, 2007 y 2025).
- Eventos BOE: fechas de publicación y entrada en vigor comprobadas en boe.es/eli (Ley 12/2023; RD 1312/2024; LO 1/2025; Ley 11/2020 catalana). Sin confirmar: obligatoriedad del registro, número de la disposición final de la LPH, STC 37/2022 (fecha BOE), DL catalán 3/2023 y DL valenciano 9/2024.
- Zonas tensionadas: copia sin editar de la v2 (318 filas: Cataluña 271, Navarra 21, País Vasco 18, Asturias 6, Galicia 2). No se añadieron declaraciones nuevas porque no se pudieron verificar en esta pasada.

- 2026-10-10 · D3 · Inside Airbnb: se usa data/listings.csv.gz (no la versión visualisations/listings.csv) para leer room_type, neighbourhood_cleansed y last_review; el bruto se descarta tras agregar. Anuncios activos = filas de la captura; con reseña 12m = last_review ≥ fecha de captura − 365 días. Cuadre barrios = total ciudad en las 36 capturas.
- 2026-10-10 · D3 · Google Trends no se descarga: no hay API pública y el endpoint explore exige token de widget; pytrends sería scraping no autorizado. Alternativa: exportación CSV manual por el responsable.
- 2026-10-10 · D3 · HUT: el dataset t2h3-cgys es una foto actual sin fechas de alta/baja; se entrega como snapshot (no sirve para flujos de altas en 2025-2026).

## Oleada 1: datos de replicación (orquestador)
- **García-López et al. (2020), Barcelona:** no es replicable en su forma original. Faltan tres cosas:
  - el histórico de Inside Airbnb de 2012-2016 (solo hay capturas desde 2025-12);
  - los alquileres por barrio (opendata BCN bloquea con anti-bot);
  - el instrumento (Google Trends sin API, y sin atractivos turísticos).

  Clasificación provisional: NO REPLICABLE con los datos originales. La «replicación» se hace como **réplica conceptual**: la misma especificación (efectos fijos de unidad y de periodo; tratamiento = viviendas turísticas por cada 100 viviendas), con las viviendas turísticas del INE por sección (2020-2025) y el alquiler SERPAVI por sección en Barcelona. Su coeficiente se compara con el objetivo (alquiler +0,035 % por 100 anuncios, tabla 3, col. 2, cifra del WP 2019) en unidades homogéneas.
- **P-C2 (caída de anuncios 2025-2026):** Inside Airbnb solo cubre 2025-12 a 2026-09, posterior a la obligatoriedad del registro único (julio de 2025 según el texto del RD; está por verificar). No hay periodo previo, así que no hay diseño con pretendencias. Se decidirá en la puerta de potencia: probablemente es descriptivo (C4) o no se estima. Las oleadas INE de VUT (2024M08, 2024M11 y posteriores) pueden aportar un periodo previo a escala de sección.

## D1 INE (2026-10-10, src/v3/fetch_ine_v3.py)
- Fecha de referencia del Censo 2021 = 2021-11-01 (fecha censal). Los indicadores por sección son provisionales según el INE (secciones de algunas viviendas en reasignación).
- Edad por sección: solo grandes grupos (ID_GRAN_GRUPO_EDAD); los tramos 16-24 a 45-64 no están disponibles por sección en la API (ver fuentes_fallidas).
- Cuadre sección -> municipio (viviendas, tabla 59525): tolerancia 0,5. Cuadre edad -> t1_1: tolerancia 10 personas (diferencias de redondeo entre la API y el fichero de indicadores, máximo observado ±6).
- VUT municipal: filas sin código único se marcan en `nivel` (agregado_o_no_identificado / municipio_ambiguo). Son agregados (CCAA, provincias) o homónimos; no entran en cuadres.
- Originales de descarga en data/raw/v3_orig (gitignored; re-descargables con FORCE=1).
- **VUT por sección (orquestador):** las tablas JAXI del INE llegan solo a municipio, pero los servicios ArcGIS del INE (servergis/Hosted/Viviendas_turísticas_<oleada>) publican distrito y sección. Script: `src/v3/fetch_ine_vut_seccion_v3.py`.
  - Cobertura: 12 oleadas, 2021M02-2026M05; falta 2020M08, que no está en el GIS.
  - Para 2022M08 se usa el servicio «Porcentaje_…», porque el de «Viviendas_…» está vacío.
  - Validación: la suma de secciones equivale a un 89-90 % del total provincial JAXI en todas las oleadas (p. ej. 2024M02: 351.389 frente a 391.996). La ratio es estable, lo que indica viviendas sin sección asignada. En los análisis por sección se usa la sección; en las cotas nacionales, el total JAXI.
- **Sellado v3 (fijado antes de cualquier estimación de P-C).** Implementación: `holdout.distritos_sellados_v3()` y `es_sellado_v3()`; lista en data/processed/v3/sellado_v3.json.
  - Tamaño: 20 % de los 10.460 distritos (2.136), en bloques espaciales completos (pares de distritos consecutivos), más la última oleada (2026M05) en todas las unidades.
  - Estratificación: por municipio en las ciudades con ≥4 bloques; por provincia en el resto.
  - Motivo de estratificar: sin estratos, el sorteo sellaba 6 de los 10 distritos de Barcelona y 9 de los 19 de València, y dejaba la réplica y P-C1 sin muestra en las ciudades clave.
  - Uso: P-C (diseños, réplicas y selección de modelos) excluye las observaciones selladas. C1 y C2 (hechos y cotas, agregados municipales o provinciales) usan todas las unidades: no seleccionan modelos de efecto.
- **Sin worktrees en la oleada 1.** Cada subagente escribe en su propio espacio de nombres (src/v3/<prefijo>_*, output/v3/<DISEÑO>/) y solo el orquestador hace commit. Así no se duplican 700 MB por worktree en un disco con ~7 GB libres.

## Puerta go/no-go de P-C (potencia; output/v3/POT/potencia.md)
| Diseño | EMD frente a EER | Decisión |
|---|---|---|
| P-C1 turísticos → alquiler, sección, efectos fijos (MCO) | 0,002 (nacional) y 0,006 (6 ciudades) frente a 0,01 | **GO** |
| P-C1 shift-share leave-one-out | 6 ciudades: 0,008-0,009 (F 24-29); nacional: no detectable (F 0,25-5,3) | **GO solo en las 6 ciudades** |
| P-C2 caída de anuncios 2025-2026 | EMD infinito: no hay alquiler a escala fina posterior a 2024 | **NO-GO**: «no detectable con los datos disponibles». Queda como descripción C4 de la caída de anuncios |
| P-C3 topes de Cataluña y zonas tensionadas (alquiler y contratos, fianzas municipales) | topes 0,018 frente a 0,03 y 0,054 frente a 0,10; zonas 0,023 frente a 0,03 y 0,079 frente a 0,10 | **GO**. Antes del pre-registro se sustituye el proxy de 58 municipios por la lista oficial de municipios sujetos a la Ley 11/2020 y se recalcula la potencia |
| P-C4 suelo como moderador | 0,154 y 0,67 frente a 0,1 | **NO-GO**: no detectable |

La decisión queda condicionada a la revisión de la oleada 1.

## Contención de rentas Cataluña (Ley 11/2020) y zonas tensionadas Cataluña (Ley 12/2023) — 2026-10-10
- Anexo Ley 11/2020: 61 municipios en el texto consolidado BOE (versión 2020-10-01, tras DL 33/2020, que añadió Mollet del Vallès); el texto original (2020-09-21) cita 60. Se usa 61.
- fecha_vigencia_fin Ley 11/2020 = 2021-09-21: caducidad de la DT segunda (un año desde 22/09/2020). La STC 37/2022 (BOE 08/04/2022) anuló arts. 1, 6-13, 15, 16.2, DA 1-4 y DT 1 y 4.b, no la DT segunda.
- «Pineda» del anexo = Pineda de Mar (08163); «Castell d'Aro, Platja d'Aro i S'Agaró» = 17048.
- Errata en data/raw/v3/zonas_tensionadas_v3.csv (no editado): Rubí aparece con 08085 (Font-rubí) en lugar de 08184; Mont-roig del Camp con 17110 (Mont-ras) en lugar de 43092. La salida usa los códigos validados en Incasòl y en el texto BOE.
- Ley 12/2023: la relación trimestral la publica la Secretaría de Estado de Vivienda y Agenda Urbana (Resolución, no orden ministerial). Cataluña: 140 (BOE-A-2024-5214, TER/800/2024) y 131 (BOE-A-2024-20576, TER/2408/2024). Sin declaraciones catalanas en 2025 en el BOE consultado; la ampliación a 302 (julio 2026) solo figura en prensa.

## Revisión de la oleada 1: REHACER (iteración 1) — docs/v3/revision_oleada1.md
- **O1, incidencias de sellado, declaradas:**
  - (i) El subagente de potencia y GL ejecutó un `describe()` global sobre el fichero de VUT por sección (todas las unidades y oleadas, incluida la 2026M05) antes de recibir la orden de sellado. Fueron estadísticos marginales del tratamiento, sin el resultado. Contaminación baja.
  - (ii) `pot_run.pc3` estimó P-C3 (topes y zonas, fianzas municipales) con todos los municipios, incluidos los que el sellado v3 deja fuera, y publicó los coeficientes: topes −0,022 / +0,002; zonas −0,047 / −0,203.
  - (iii) Los coeficientes de P-C1 en la muestra no sellada (nacional +0,0011 y ciudades) también se conocen por la réplica GL.

  Consecuencias, fijadas ahora:
  - La potencia publicará solo el EE y el EMD.
  - `prereg-v3` declara (ii) y (iii), y en P-C1 solo la evaluación sellada es confirmatoria.
  - **P-C3 no tiene ya una muestra sellada espacial limpia.** Su validación sellada se hace **por fuente**: la misma especificación con el alquiler SERPAVI (IRPF) municipal de Cataluña, 2018-2023, que no se ha estimado nunca para P-C3, evaluada una vez vía `holdout.evaluate`. Es una desviación del sellado espacial y se declara como tal. Las zonas tensionadas de 2024 ya vistas quedan en C4.
  - Ventana de los topes: 2020Q4-2022Q1 (vigencia efectiva hasta la STC 37/2022, BOE 08/04/2022), con sensibilidad de fin en 2021Q3.

## Pre-registro v3 (2026-10-10)
- La oleada 1 se aprobó en la iteración 2 (docs/v3/revision_oleada1.md). Lo que persiste está en docs/v3/limitaciones.md.
- `prereg-v3`: tag local en el commit 204c073. El push del tag lo rechaza el proxy, igual que en v2. **El ancla del pre-registro es el SHA 204c073 en la rama remota.** Cualquier cambio posterior de docs/v3/hipotesis.md es una desviación y se anota aquí.
- Sellado v3 operativo:
  - `holdout.sellar_v3`: separa las unidades selladas al construir el panel, y la rama solo recibe el entrenamiento.
  - `holdout.sellar_fuente_v3`: validación por fuente de P-C3; la rama guarda el panel sin mirarlo.
  - `holdout.evaluate_v3`: una apertura por hipótesis, registrada antes de leer.

## Oleada 2/3 (orquestador)
- **H3-3 (topes), resultado:** C4. Fallan el criterio a (el IC de Rambachan-Roth con M̄=1 incluye 0) y el c (sensibilidad). En H3-3b fallan además las pretendencias y el placebo de fecha. Cada hipótesis abrió la validación por fuente una sola vez (log 13:42:50Z).
- **P-D, topes:** se calibra con Jofre-Monseny et al. (2023), que es VERIFICADA (−4,5 % [IC]). La estimación propia de H3-3a (−5,4 % [−7,1; −3,7], C4) cae en un rango compatible. No sustituye a la calibración porque es C4. P-D lee los resultados de la oleada 2 en tiempo de ejecución y deja constancia de que existen.

## Desviaciones de la oleada 2 (W8 de la revisión), transcritas

### C1 (H3-1, H3-2), de output/v3/C1/desviaciones.md

1. **Lectura del sellado (holdout).** La primera versión de `evaluate_v3` fallaba con pandas 3 (`errors='ignore'`) tras registrar la apertura. El orquestador lo corrigió en `src/holdout.py` antes de la llamada; la rama no usó ningún parche propio. Cada hipótesis abrió el sellado una vez (H3-1 y H3-2) y el resultado se guardó en `sellado_H3-1.json` y `sellado_H3-2.json`; `c1_run.py` los lee y no vuelve a llamar.
2. **Resultado principal sellado.** El pre-registro dice «nacional y 6 ciudades conjuntas». La confirmación sellada de H3-1 se evalúa en la muestra nacional (más potencia, P2); las 6 ciudades se informan como secundaria. En H3-2 la confirmación sellada es la de las 6 ciudades (tabla de hipótesis); las 5 ciudades y Palma van aparte (P5).
3. **ADRH.** La renta por hogar ADRH no tiene 2021 en el GIS del INE (hay 2019, 2020, 2022, 2023). El placebo de resultado usa 2022-2023, con FE de sección y año×municipio.
4. **Resultado «media».** SERPAVI solo publica mediana y percentiles; no existe la media. En el multiverso se sustituye por la mediana en €/mes (`ALQTBID12_M`).
5. **FE de H3-2.** El pre-registro no fija los efectos fijos de H3-2; se usan los de H3-1 (sección + año×municipio). Fijado antes de ver la primera etapa de esa especificación. La variante sección + año queda fuera del principal (el EMD de potencia se calculó con ella).
6. **Instrumento.** z = cuota inicial (VUT por 100 viviendas en 2021M08) × crecimiento relativo de VUT del resto del municipio sin la propia sección. En la potencia se usó la variación por 100 viviendas; esa variante y las bases 2021M02, y el agregado provincial, están en el multiverso H3-2.
7. **BHJ.** No procede: hay 5 shocks de ciudad (3 años) y no un conjunto amplio de shocks idiosincráticos. Se informan los pesos de Rotemberg y la exclusión de cada ciudad.
8. **Sellado y LOO.** En la evaluación sellada, el «resto de la ciudad» se calcula con las secciones selladas del municipio (no se mezcla entrenamiento). Fuente de error de medida adicional.
9. **P2 sellado.** EMD de la validación sellada aproximado con el EE de entrenamiento reescalado por sqrt(G_ent/G_sellado), con G_sellado contado en el panel antes de separar (solo recuentos de distritos balanceados: 734 nacional, 21 en 6 ciudades, 17 en 5 ciudades). EMD calibrado por WCB con pesos de Webb (999) aproximado como (valor crítico bootstrap + t0,80)·EE.
10. **Criterio de placebo de tratamiento.** Se pasa si la fracción de permutaciones con |t|>1,96 es ≤ 10 %. El placebo de resultado ADRH se pasa con p ≥ 0,05. Un ADRH significativo se informa sin invalidar el diseño (P3), pero el criterio (b) de capas lo cuenta como fallo.
11. **Sensibilidad.** Controles = ocho covariables censales × dummies de año. δ de Oster con R_max = 1,3·R̃ sobre R² intra-FE. RV_q=1 con el t de clúster (sensemakr no instalado; fórmula propia) frente al máximo R² parcial de la mejor covariable (con el resultado y con el tratamiento).
12. **Conley.** Núcleo Bartlett de 1 km entre centroides (cartografía INE 2021, centroides calculados sin geopandas; temporales borrados; caché `centroides.csv`). Sin corrección de grados de libertad.
13. **Fuera de muestra.** No se compara con AR(4) ni con ECM v1: son coeficientes de asociación entre secciones, no pronósticos. La validación fuera de muestra es la sellada.
14. **Holm (m=4).** Lo aplica el orquestador con `p_sellado` de `resultado.json`.
15. **Familia confirmatoria de H3-1.** Se eligió la muestra nacional como único confirmatorio (punto 2). Si las 6 ciudades también lo fueran, m sería 5. El sellado de las 6 ciudades da β = −0,0013 [−0,0034; 0,0008], p = 0,20 (wcb 0,24), con signo opuesto al nacional (+0,0010); se informa con el mismo relieve y la hipótesis no se apoya en ninguna de las dos.
16. **Umbrales fijados después del pre-registro.** El umbral de placebo de tratamiento (≤ 10 % de permutaciones con |t| > 1,96) se fijó después. Criterio b revisado: depende solo de la permutación; el ADRH significativo (H3-1, p = 0,0003) se informa sin invalidar automáticamente (P3). Criterio c unificado con C3: RV_q=1 frente a max(R²_y, R²_d) de la covariable más fuerte y |δ| de Oster > 1. Las capas no cambian (a falla).
17. **p_ajustado** (Holm m = 4) tomado de `output/v3/holm_v3.csv`: H3-1 0,467; H3-2 0,501.

### C3 (H3-3), de output/v3/C3/desviaciones.md

1. Las fianzas trimestrales de Incasòl solo existen desde 2019Q1 (2017-2018 solo anual). La ventana previa es 2019Q1-2020Q3 (7 trimestres), el periodo de análisis 2019Q1-2023Q4 y la ventana de tratamiento 2020Q4-2022Q1 (o 2021Q3).
2. Placebo de fecha falsa 2018Q4: no es trimestral (no hay trimestres de 2018). Se hacen dos versiones: fecha falsa 2019Q4 con post 2019Q4-2020Q2 (se excluye 2020Q3 por la anticipación que documentan JMS) y versión anual (2019 frente a 2018, panel anual 2016-2019).
3. Rambachan-Roth: no hay paquete instalado. Se usan la cota de magnitudes relativas con M̄=1 y la de tendencia lineal (suavidad con M=0) con IC por bootstrap de unidades (999). No es el IC condicional/híbrido de Rambachan-Roth.
4. Control del multiverso: hipotesis.md dice «no sujetos con más de 20.000 habitantes como en JMS 2023». La ficha de literatura (A3) describe sus controles como mercado tenso por debajo del umbral. Se corren los dos más «todos los no sujetos» (principal). «Mercado tenso» se aproxima con el crecimiento anual de la renta de fianzas 2014-2019 ≥ 4,15 %.
5. Población: Censo 2021 (suma de grandes grupos de edad por municipio), fija en el tiempo. No hay padrón anual en los datos.
6. Barcelona se excluye en la especificación principal (como JMS y la potencia); su inclusión es una decisión del multiverso.
7. dCDH: no hay paquete. Se usa DID_M (efecto en el momento del cambio, 2020Q4 frente a 2020Q3), que con un único momento de tratamiento coincide con ATT(g,g) de CS.
8. Contratos: ln del nº de fianzas (sin denominador de población; la población fija se absorbe en los efectos fijos de municipio). Sin controles (paro, ERTO) que sí usan JMS.
9. El resultado de renta es la media de las medias de banda ponderada por nº de contratos; las bandas cambian entre años.
10. Potencia de la validación SERPAVI: la estructura (municipios con los 4 años) viene de SERPAVI y la varianza es la de las fianzas anuales (aproximación; SERPAVI es un stock IRPF y su varianza real no se miró).
11. Parche de pandas 3 (retirado). La primera versión aplicó en memoria un parche a `DataFrame.apply(pd.to_numeric, errors='ignore')` y un test en seco con `holdout.LOG` redirigido. La versión actual de `holdout.py` (c5e8aae) ya no contiene esa llamada: el parche era código muerto y se eliminó. `holdout.py` sí fue modificado por c5e8aae, después del ancla 204c073. El test en seco ahora llama a `fn` con un panel sintético, sin tocar `holdout`. Ninguna estimación cambia.
12. Muestra: panel equilibrado 2019Q1-2023Q4 (misma muestra para event study, pretendencias, estimación principal y sensibilidad). Las réplicas JMS usan paneles equilibrados de su propio periodo.
14. Validación por fuente: DiD 2x2 con pre 2018-2019 y post 2021-2022; descarta 2020 y 2023 (el pre-registro dice SERPAVI 2018-2023).
15. Umbrales de placebo fijados después del pre-registro: cualquier placebo con p < 0,05 (t o aleatorización) cuenta como fallo de b.
16. Criterio c (revisión de la oleada 2): RV_q=1 frente al mayor R² parcial entre R²_y y R²_d, y |δ| de Oster > 1. H3-3a depende de tomar la pendiente previa como covariable observada: sin ella RV_q=1 supera al resto (la capa no cambia porque falla a). Criterio b de H3-3: parcial, sin placebo de resultado. Se informa el M̄ de ruptura de Rambachan-Roth.
13. fuera_muestra: no se compara con AR(4)/ECM v1 (es un efecto de política); la validación fuera de muestra es la sellada por fuente.

### Orquestador
- `src/holdout.py` (commit c5e8aae): evaluate_v3 se corrigió para pandas 3, porque pd.to_numeric(errors='ignore') ya no existe. La corrección se aplicó DESPUÉS de las evaluaciones selladas de H3-3a y H3-3b, que se hicieron con un parche en memoria equivalente, y ANTES de las de H3-1 y H3-2. Una apertura por hipótesis (log 13:42:50Z y 13:47:05-09Z).
- C3 redirigió holdout.LOG en el test en seco de fn; se eliminó (W9). El log real tiene solo las aperturas declaradas.
- El pre-registro fijaba la sección «Probable pero no demostrado» de lo_que_sabemos.md por mandato del usuario. Se mantiene con el calificativo «(exploratorio, C4)» y redacción de asociación (W3).

## Revisión de la oleada 2: APROBAR (iteración 2)
- Residuos corregidos en edición:
  - R1: regla de V01.
  - R2: lenguaje de asociación y título de lo_que_sabemos.
  - R3: fila P-D de retirada de VUT en C4.
- R4, estándar único: toda traducción de cotas a precio con supuesto estructural no estimado es C4, sea ε o P/R = 1/uc. Consecuencias:
  - B4 pasa de C2 a C4. Es una bajada de capa, no una promoción.
  - V12 pasa a SIN EVIDENCIA SUFICIENTE.
  - La convención y su alternativa constan en docs/v3/limitaciones.md (L-v3-W3).

## Cierre v3
- Reproducción: `make all` sin red (proxy apuntado a 127.0.0.1:9, un solo hilo), dos veces, en un clon limpio de 7607040. Las dos ejecuciones terminan con rc=0 (unos 1.220 s cada una). Comparación de los md5 de output/ y data/processed: idénticos salvo `output/v2/BM/tiempos.json`, que guarda tiempos de reloj. Frente a lo versionado solo cambian ese fichero y la marca de tiempo de `docs/v2/fallidas/ine.md`.
- Corrección previa al cierre: `pa_data` leía el CSV del Catastro sin comprimir, que no está versionado. Ahora lee el `.csv.gz` versionado.
- Revisiones: oleada 1 APROBAR (it. 2), oleada 2 APROBAR (it. 2), oleada 3 APROBAR (it. 2). Lo pendiente está en docs/v3/limitaciones.md.
