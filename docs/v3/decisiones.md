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
