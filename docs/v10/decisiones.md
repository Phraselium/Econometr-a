# Decisiones V10-DIFUSIÓN

Rama local `r10/difusion`, subida a la rama remota designada (`claude/housing-price-spain-econometric-95dhj3`), la única a la que se puede subir (CLAUDE.md). Solo análisis descriptivo, integración y difusión: no se estiman modelos ni se abren muestras selladas.

## D0 — Arranque (2026-10-14)
- **V9-DATOS-COMPLETO** se interrumpe tras su bloque 0 (regulación) por la orden de pasar a V10. El estado y los pasos aplazados están en docs/v9/estado_datos.md.
- **Herramientas.**
  - Se añade DuckDB 1.5.6 (requirements.lock), además de geopandas, shapely y pyogrio, que ya estaban instalados y faltaban en el lock.
  - Quarto no está instalado. La web se generará con Python y librerías JavaScript vendorizadas (D3), para que `make web` funcione sin red.
- **Subagentes:** ninguno por ahora.

## D1 — Base única (bloque 1)
- **Entradas.** data/processed (paneles v1, v7 y v8; València), data/raw/v9 (censo anual por sección, IPVA, registro VUT de la GVA, EMAL, Inside Airbnb, BCE, Eurostat de plataformas, Incasòl y zonas tensionadas) y publicacion/cifras_clave.csv.
- **Tabla larga `hechos`.** Columnas: las pedidas más `desagregacion` (nacionalidad, antigüedad del contrato, fijación…), `origen`, `posterior_prereg` y `muestra_sellada_v6`.
  - Clave única: territorio_codigo, nivel, periodo, frecuencia, variable y desagregacion.
- **Un solo panel por serie.** Cada serie (variable × territorio × desagregación) sale entera del panel más reciente que la tiene (v8 > v7 > v1). Nunca se empalman paneles.
  - Motivo: hay 203 claves en que los paneles discrepan:
    - `hogares_ecp` está en miles en v8 y en unidades en v1;
    - `pob_extranj` se define con Eurostat en v8 y con el INE en v1;
    - `pob_total` difiere por redondeos.
  - Empalmar habría mezclado unidades o definiciones.
- **Columnas excluidas** (no son variables de nivel del territorio): logaritmos y diferencias, dummies de modelo (q1-q4, covid, P1-P5…), exposiciones fijas, variables nacionales repetidas en los paneles de CCAA (`nac_*`, `hpi_ea*`, `bis_*`) y banderas de sellado.
- **Capa, unidad y fuente** salen de los diccionarios del proyecto (v8 > v7 > v6 > v1) y, para V9, de una tabla explícita en src/v10/base.py. Sin capa conocida: C4.
- **Licencias.**
  - No redistribuibles: las filas cuyas fuentes el inventario de V8.1 marca como no claramente permitidas o que están retiradas (Registradores, Notariado, shocks JK, Incasòl).
  - La capa pública (data/base/publica/, versionada) solo contiene filas redistribuibles.
  - La tabla completa (data/base/hechos.parquet) y vivienda.duckdb no se versionan: se regeneran con `make base`.
- **`posterior_prereg`.** Es True si el periodo incluye algún día desde el 2026-07-01 (2026T3, 2026-07…; también los anuales de 2026).
  - Esas filas se muestran como dato, pero no entran en ningún cálculo del atlas ni en ninguna comparación con predicciones.
- **`muestra_sellada_v6`** marca las 11 provincias del sellado transversal de v6. Es informativo: data/sealed no se lee nunca.
- **Territorios** (dimensión con jerarquía):
  - CCAA, provincias y municipios: relación del INE de 2026;
  - distritos y secciones: seccionado del INE de 2025;
  - barrios de València: Ajuntament, código de 9 dígitos = 46250 + distrito (2) + barrio (2).
  - Se añaden como «no vigentes en 2025» las 338 secciones del censo 2021-2024 que ya no existen en el seccionado de 2025.
- **Geometrías.**
  - Se parte de las secciones del INE y se disuelven por código INE en municipios, provincias y CCAA (sin cruce por nombre).
  - GeoParquet simplificado (10 m en secciones y municipios; 200 m en provincias y CCAA).
  - GeoJSON muy simplificado para la web.
  - Correspondencia sección → barrio de València por área: 531 de las 588 secciones caen en un barrio en al menos el 95 % de su área; las demás se reparten con pesos.
- **Cifras clave.** publicacion/cifras_clave.csv se carga tal cual como tabla de la base. El test exige identidad exacta con el CSV, tanto en el parquet como en DuckDB.

## D2 — Base ampliada y montaje en DuckDB (bloques 1 y 2)
- **Montaje en DuckDB.** La base se monta en DuckDB en disco: pandas se quedaba sin memoria con unos 11 millones de filas con texto.
  - Resultado: 10,16 M filas, 238 variables y unos 56.500 territorios.
  - Se añaden los municipios, secciones y distritos históricos (fusiones de municipios, secciones de 2021-2024 que ya no existen en 2025), marcados con `vigente_2025 = False`.
- **Fuentes del proyecto que se añaden** (todas con código INE y licencia permitida en el inventario de V8.1):
  - SERPAVI por municipio, distrito y sección;
  - viviendas turísticas del INE por sección;
  - renta ADRH por sección;
  - indicadores del Censo 2021 por sección;
  - unidades urbanas del Catastro por municipio;
  - resultados ya publicados: déficit provincial V5-A4, factor común V8-M1 y atribución V8-F5 (esta, en una tabla propia, `v8_atribucion`).
- **Excluidas.** Valor tasado y transacciones por municipio del MIVAU: solo traen el nombre del municipio, y el cruce por nombre está prohibido. El atlas lo indica.

## D3 — Atlas descriptivo (bloque 2)
- **a) Microdatos ECV 2018-2025 y EPA 2018T1-2026T2.**
  - Unidad: personas ponderadas.
  - IC por linealización con el hogar como conglomerado. Los ficheros públicos no traen estratos, así que los IC son algo estrechos; se dice en cada tabla.
  - Celdas con n < 50: suprimidas.
  - Esfuerzo: mediana con IC de Woodruff. La media se descartó porque las rentas muy bajas la distorsionan (media 69 % frente a mediana 21 %).
  - Antes de 2021 la ECV no trae edad ni nacionalidad en el fichero de personas: la edad se calcula con el año de nacimiento y la nacionalidad sale del fichero de adultos.
- **Criterio de capa C1 en a).** La serie nacional coincide con la tabla oficial de Eurostat dentro de 0,5 puntos **todos** los años.
  - La sobrecarga del 40 % (total y por tenencia de propiedad y alquiler de mercado) replica Eurostat con menos de 0,05 puntos: C1.
  - El hacinamiento queda unos 0,8 puntos por debajo todos los años (diferencia de definición sin resolver): C4.
  - Todo lo demás de los microdatos (grupos, CCAA, edad, nacionalidad) es C4 de fuente única.
- **b) Entrar frente a quedarse.** Brecha entre índices encadenados del IPVA, en puntos de índice 2015 = 100; compara crecimientos, no niveles.
  - Fianzas de la GVA por código postal: el código postal no es código INE y no se cruza; celdas con menos de 20 fianzas, suprimidas; 2026 excluido.
- **c) València.**
  - Agregación sección → barrio por área: recuentos repartidos, tasas recalculadas y medianas promediadas ponderando.
  - Índice de presión: media simple de cuatro puntuaciones z, solo descriptivo.
  - No disponibles: antigüedad y usos por sección (Catastro INSPIRE no descargado) y accesibilidad (GTFS no descargado). Ambos quedaron en el bloque 2 aplazado de V9-DATOS-COMPLETO.
- **d) Provincias.**
  - Las CCAA uniprovinciales no tienen valor tasado provincial en el panel: se usa el de la CCAA (mismo territorio, media de cuatro trimestres) y se marca el origen.
  - El esfuerzo provincial es un indicador comparativo: vivienda tipo de 80 m² frente a la renta por persona.
- **e) Ciudades comparables.** SERPAVI no cubre los territorios forales hasta 2024, por lo que Bilbao solo tiene ese año.
- **Texto** (output/v10/atlas_descriptivo.md, copiado a publicacion/ por `make publicacion`):
  - todas las cifras se calculan a partir de las tablas;
  - un test prohíbe el vocabulario causal.

## D4 — Figuras (bloque 3)
- **Diseño.**
  - Paleta Okabe-Ito; mapas con «cividis» (secuencial) o «PuOr» (divergente).
  - Tamaños: paper (16 × 10 cm, 300 ppp, PNG y PDF), web (SVG) y redes (1.200 × 675).
- **Contenido.** 14 figuras:
  - atlas: sobrecarga, esfuerzo, IPVA, mapas provincial, de la Comunitat Valenciana y de València, ciudades y emancipación;
  - figuras clave regeneradas desde la base: contratos nuevos frente a existentes (V5), déficit provincial (V5), factor común (V8), descomposición por periodo con bandas (V8) y cotas C2 (verificador).
- **Ficha por figura** (figuras/fichas.json y README.md): título, fuente, fecha, capa, nota y texto alternativo.
  - Los textos alternativos describen la figura, no anticipan hallazgos.

## D5 — Licencias de la capa pública (corrección)
- **Fallo.** El filtro de no redistribuibles solo miraba el prefijo `registr_`. Por eso, en los commits bc0f83b y 4e0c4a8, la capa pública (data/base/publica/hechos.parquet) incluía dos variables agregadas del Colegio de Registradores: `registradores_extranj_pct` y `registradores_compraventas_anual`.
- **Corrección.** El filtro mira ahora el prefijo (`registr`, `notariado`, `jk_`, `incasol_`…) y también el texto de la fuente. Un test lo impide en la capa pública y en la web.
- **Historial.** No se reescribe: los dos commits siguen conteniendo esas filas en el historial de la rama. Se avisa al autor.

## D6 — Web (bloque 4)
- **Por qué no Quarto ni Observable Framework.** Quarto no está instalado en el entorno, y Observable Framework exige `npm install` al construir.
  - Se usa un generador en Python (Jinja2 y markdown) con Observable Plot 0.6.17, D3 7.9.0 y Leaflet 1.9.4 vendorizados en web/vendor, con sus licencias (ISC, BSD y BSD-2).
  - Así `make web` funciona sin red y el sitio no hace peticiones a terceros. Los mapas no usan teselas externas, por privacidad y licencia.
- **Despliegue.** .github/workflows/pages.yml, en cada push a `main` que toque datos, salidas o web.
  - Requiere que el autor active Pages con origen «GitHub Actions».
  - URL prevista: https://phraselium.github.io/vivienda-espana-evidencia/.
- **Contenido.**
  - 9 secciones y 311 fichas territoriales: 19 CCAA, 52 provincias, municipios de 50.000 habitantes o más y 87 barrios de València.
  - Navegación y textos clave en castellano y valenciano; metodología y resumen en inglés.
- **Accesibilidad.**
  - Enlace para saltar al contenido, foco visible y contraste AA.
  - Texto alternativo en las figuras; cada mapa con una tabla equivalente y un CSV descargable; cada gráfico con su tabla.
- **Datos.**
  - Solo redistribuibles: la web publica data/base/publica y los agregados del atlas.
  - El panel y los mapas excluyen los periodos desde 2026T3. Un test comprueba todo esto.

## D7 — Monitor (bloque 5)
- **Script** (src/v10/monitor.py): 12 series abiertas que cambian con frecuencia, con su último dato y la variación interanual (en puntos para los tipos).
  - INE: IPV, IPC de alquiler, compraventas, hipotecas, VUT y población.
  - Eurostat: HPI y plataformas.
  - BCE: tipos MIR.
  - GVA: fianzas.
- **Fianzas de la GVA.** El año en curso es un acumulado parcial (el fichero no trae mes): se muestra sin variación.
- **Posterior al pre-registro.** Se marca todo periodo que incluya algún mes desde 2026-07. Se muestra como dato, sin comparar con ninguna predicción.
- **En la base.** Las series entran como variables `monitor_*`.
- **Flujo mensual** (.github/workflows/actualizar.yml), los días 3 de cada mes:
  1. descarga el monitor y refresca las fuentes abiertas de V9;
  2. reconstruye base, atlas, figuras y web;
  3. pasa `make check`;
  4. abre un pull request con el resumen.
- **Límites del flujo.** No publica ni fusiona sin revisión. No toca evaluate_v7 ni evaluate_v8.

## D8 — Paquete académico (bloque 6)
- **Manuscrito** (paper/manuscrito.qmd), en Quarto con estructura de revista:
  - resumen y abstract;
  - datos, método y resultados descriptivos;
  - evidencia de V5-V8 regenerada desde la base;
  - diseños de v9 marcados como [PENDIENTE];
  - discusión;
  - referencias desde docs/v9_prep/referencias.bib;
  - apéndice de replicación.
- **Cifras del manuscrito.** Ninguna se escribe a mano: se calculan con código en línea desde las tablas.
- **Render.** Quarto no está instalado en el entorno, así que el manuscrito no se ha renderizado. Un test ejecuta sus bloques de código y su código en línea, y comprueba las figuras y las citas.
- **Excel** (publicacion/tablas_atlas.xlsx; src/v10/tablas_excel.py):
  - colores: datos de entrada en azul con fuente y fecha (cabecera y comentario); cálculos de la hoja en negro, como fórmulas recalculables; vínculos a otras pestañas en verde (índice con hipervínculos y fórmulas entre hojas);
  - sin paneles inmovilizados;
  - zip con fechas fijas (determinista);
  - fórmulas comprobadas con LibreOffice: sin errores; la brecha nacional del IPVA coincide con el atlas (16,404).

## D9 — Orden del repositorio (bloque 7) y cifras del atlas
- **Traslados a historico/.** Se trasladan con `git mv` 9 documentos de proceso de V7, V7.1 y V7.2 (planes, estados, bloqueos e instrucciones) que no lee ningún script, test ni el Makefile ni enlaza ningún entregable vigente; el detalle está en historico/INDICE.md.
- **Lo que no se mueve.** Las salidas output/v2-v8 se quedan donde están: sus scripts las regeneran en su ruta y los entregables vigentes las leen (cifras_clave, anexo, verificador). Moverlas exigiría reescribir decenas de scripts y arriesgaría `make all`. El índice del histórico dice qué está vigente.
- **Regla de V7.1** («toda cifra difundible sale de cifras_clave»):
  - el atlas escribe output/v10/atlas/hechos.json y src/v5/cifras_clave.py lo incorpora, con 28 cifras `V10-ATL-*`;
  - el texto cita cada id entre corchetes;
  - se ha comprobado que ninguna de las 1.064 cifras previas cambia.
- **Documentos actualizados.**
  - README y LEEME_PRIMERO, a mano.
  - consulta/ y llms.txt, con `make consulta`: entradas V10 en la guía para asistentes, el índice de ficheros y version.json (`difusion` y `web_prevista`). La versión sigue siendo 8.1 porque no se ha publicado ninguna release nueva.
  - CHANGELOG.
- **Orden de construcción:** `make base` → `make atlas` (actualiza hechos.json) → `src/v5/cifras_clave.py` → `make publicacion` → `make base` (vuelve a copiar cifras_clave) → `make consulta` → `make figuras` → `make web`. El flujo mensual sigue este mismo orden.
