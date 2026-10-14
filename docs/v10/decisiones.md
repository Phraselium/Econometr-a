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
