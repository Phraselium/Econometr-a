# V16 · Fase 1 · Familia oferta_suelo (ficha de fuentes)

Verificación: 2026-10-17. Escribe solo en data/raw/v16/oferta_suelo/ y en esta ficha.
Manifiesto: data/raw/v16/oferta_suelo/_manifest.csv (licencias y sha256).
Objetivo: insumos para una elasticidad de oferta municipal tipo Saiz (suelo no edificable por pendiente, agua, protección y planeamiento).
Regla de licencias: redistribuible «no» o «dudoso» va a data/raw/v16/oferta_suelo/_terceros/ (no versionado; .gitignore línea 153).

## Descargadas en esta sesión

### 1. INE · índices de materiales y mano de obra en construcción (IMM)
- Endpoint: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<tabla> (API INE, verificado 2026-10-17).
- Tablas: 8381 (materiales generales, 16 series), 8382 (materiales específicos, 5 series), 8377 (mano de obra, 1 serie). Base 2011=100 y base julio 1980 respectivamente.
- Cobertura: nacional, mensual; 8381/8382 desde 2012-01, 8377 desde 1995-01; última fecha de cabecera 2026-03 (fecha 2026-03-01 hora de Madrid).
- Ficheros: data/raw/v16/oferta_suelo/ine_imm/imm_8381.json, imm_8382.json, imm_8377.json (JSON original, sin transformar).
- Script: data/raw/v16/oferta_suelo/_scripts/fetch_ine_imm.py (caché; FORCE=1 para rebajar de nuevo).
- Licencia: reutilización de información del INE con cita (Ley 37/2007). Redistribuible: sí.
- Hueco que cubre: el repositorio tiene coste de producción (Eurostat sts_copi_q, eurostat_costes.csv) pero no los precios de materiales y mano de obra del INE. No son municipales: solo sirven como deflactor o coste de construcción nacional.
- sha256: 11ee60e9…560e48 (8381), a27fd759…2dcf (8382), 9a86c5e0…3ce (8377). Completos en el manifiesto.

### 2. MITECO · Red Natura 2000 (cartografía 2025) — dudoso, en _terceros
- Página: https://www.miteco.gob.es/es/biodiversidad/servicios/banco-datos-naturaleza/informacion-disponible/rednatura_2000_desc.html (verificada 2026-10-17).
- Fichero: https://www.miteco.gob.es/content/dam/miteco/es/biodiversidad/servicios/banco-datos-naturaleza/3-rn2000/n2000_2025_shp.zip
- Tamaño: 132.446.342 bytes (>50 MB). Ubicación: data/raw/v16/oferta_suelo/_terceros/_grandes/n2000_2025_shp.zip. Checksum sha256 0b35e4f6…bbb2cbd. Pendiente: añadir a data/CHECKSUMS.sha256 (lo hace el coordinador; esta familia no escribe fuera de sus rutas).
- Contenido (listado del zip, sin extraer): dos capas shapefile, terrestre (n2000_spatial_es_pibal_proy_end25.shp, 193 MB) y canaria (n2000_spatial_es_can_proy_end25.shp, 24 MB). Ni marina ni archivos de otras ediciones.
- Licencia: la página solo enlaza el aviso legal general del MITECO (https://www.miteco.gob.es/es/atencion-al-ciudadano/aviso-legal.html). No consta licencia explícita; texto no verificado. Por eso: redistribuible = dudoso.
- Uso previsto: agregado municipal propio (porcentaje de superficie municipal en Red Natura) solo en robustez, según reglas de terceros.
- Script: data/raw/v16/oferta_suelo/_scripts/fetch_miteco_natura2000.py.

## Ya en el repositorio (no descargado de nuevo)

| Fuente | Ruta | Cobertura verificada | Uso para oferta |
|---|---|---|---|
| MIVAU precio del suelo urbano, CCAA, provincias y municipios >50.000 hab. (tablas 36400500 y 36403000) | data/raw/mivau_v2_suelo.csv | 2004T1-2026T2; 42 series | Precio del suelo por provincia; municipios >50.000 hab. |
| MIVAU vivienda protegida, calificaciones provisionales (31202000; 31303000) y definitivas (31205000; 31306000) | data/raw/mivau_v2_protegida.csv | Provisionales y definitivas, CCAA/provincia; 1991-2026 según tabla | Vivienda protegida calificada (oferta pública) |
| Visados de dirección de obra, proxy: viviendas libres iniciadas (32100500) | data/raw/mivau_visados.csv | 2008-01 a 2026-06, mensual | Proxy de obra iniciada (no es el visado CSCAE; ver docs/fuentes_fallidas.md) |
| Certificados de fin de obra, proxy: viviendas libres terminadas (32101000) | data/raw/mivau_fin_obra.csv | 2008-01 a 2026-06, mensual | Proxy de terminadas |
| MIVAU valor tasado municipios >25.000 hab. (35103500) | data/raw/mivau_valor_tasado_municipios.csv | 2005T1 en adelante | Precio municipal de vivienda libre |
| Eurostat costes, permisos, producción de construcción | data/raw/eurostat_costes.csv, eurostat_permisos.csv, eurostat_produccion_construccion.csv | Trimestral; 1995-2026 según fichero | Coste de construcción (índice) y permisos |
| Catastro: estadísticas urbanas por municipio | data/raw/catastro_urbana_municipios.csv(.gz) | 2011-2025; 15.220 series | Parque y suelo urbano por municipio (catastral) |
| Catastro: solares y suelo por municipio (derivado en v4) | data/raw/v4/catastro_solares_municipios.csv.gz | cod_mun, anio desde 2012; uu_solar, superf_urb, v_suelo | Oferta de solar disponible (ya usado en V4) |
| Límites de secciones censales (base para agregar a municipio) | data/raw/v10/geo/seccionado_2025.zip; data/raw/v3/cartografia/Cartografia_secc.zip | Secciones 2025 | Agregación municipal de cualquier capa |
| Incasòl, habitatges y renda por municipio (Cataluña) | data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz | 2007-2026T1 | Alquiler protegido o precio de referencia; no son calificaciones |

Hueco: el visado de dirección de obra del CSCAE y el certificado de fin de obra no se encuentran en el repositorio. Los dos ficheros MIVAU de arriba son proxies documentados como tales.

## Fuentes fallidas (endpoint, edición y fecha verificados)

1. **SIU del MIVAU (suelo urbano y urbanizable por municipio)**. Endpoints: https://www.mivau.gob.es/urbanismo-y-suelo/suelo/sistema-de-informacion-urbana (HTTP 403, 2026-10-17). La ficha de datos.gob.es https://datos.gob.es/es/catalogo/e05233601-siu-datos-graficos devuelve 403; datos.gob.es/robots.txt devuelve una página de desafío de WAF (Incapsula); no se intentó eludirlo. Cobertura antigua (edición 2017, según prensa): 3.937 municipios, 48,5 %. Alternativa: descarga manual del autor (ver «Requiere al autor»).
2. **MDT05 del IGN (pendientes)**. Endpoint: https://centrodedescargas.cnig.es/CentroDescargas/mdt-5m devuelve una página «no disponible»; la raíz (https://centrodedescargas.cnig.es/) da 301. Metadatos INSPIRE, sí accesibles: https://inspire-geoportal.ec.europa.eu/srv/api/records/spaignwcs_mdt (200, solo metadatos). No descargado: el MDT nacional es muy grande. Alternativa propuesta: cálculo de pendiente por hoja, a partir de una descarga manual de hojas del MDT05 para las provincias de estudio, o servicio WCS del IGN (no probado).
3. **Dominio público marítimo-terrestre (MITECO, deslinde DPMT y núcleos excluidos)**. Página verificada (200): https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/costas-medio-marino/deslinde-dpmt.html. Condiciones: uso libre y gratuito con cita «Fuente: «© Ministerio para la Transición Ecológica y el Reto Demográfico»». Enlaces de descarga: https://gis.miteco.gob.es/descargas/app/DescargaFichero?f=dpmt.zip (SHP 12,2 MB, actualización 31/03/2026) y ?f=nucleos-excluidos-dpmt.zip (11 KB). Ambos responden con HTML (página de la aplicación de descargas, no ZIP), verificado 2026-10-17. El script los valida y no los guarda. Pendiente: descarga manual.
4. **CORINE Land Cover 2018 (Copernicus)**. Página https://land.copernicus.eu/en/products/corine-land-cover/clc2018 (200). Las rutas de descarga por área y la API de CLMS (https://eea.github.io/clms-api-docs/download.html, 200) exigen token Bearer; no se consiguió el endpoint público de ficheros prepackaged. Endpoint https://land.copernicus.eu/api/datasets: 404. Tamaño y licencia no verificados en la fuente de descarga. No intentado por exigir autenticación.
5. **SIOSE (IGN, 2014 y 2020)**. Página del producto: https://centrodedescargas.cnig.es/CentroDescargas/siose-2020 devuelve la página «no disponible» (200 con error). Licencia de SIOSE 2014 según datos.gob.es: CC BY 4.0 (dato de búsqueda, no verificado en la fuente). No se encontró descarga municipal.
6. **Comunidad de Madrid (vivienda protegida y parque público)**. https://datos.comunidad.madrid/ devuelve 404; https://www.comunidad.madrid/servicios/ devuelve 404. No se localizó ningún conjunto de calificaciones ni de parque público por búsqueda.
7. **GVA (vivienda pública y calificaciones)**. https://opendata.gva.es/ sin respuesta (timeout, 000); https://dadesobertes.gva.es/ devuelve 77 bytes (redirección); no se localizó conjunto de calificaciones.
8. **Incasòl (parque público, calificaciones)**. https://www.incasol.gencat.cat/ sin respuesta (000). El fichero ya presente (v9) no es un registro de calificaciones.
9. **INE Estadística de Construcción de Edificios (licencias municipales de obra mayor)**. Ficha: https://www.ine.es/uc/B1aHHxCri1 (operación coyuntural; fuente: licencias municipales; PEN 2025-2028). La API de operaciones (https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES) no la lista y no se encontró su id de tabla. Municipal: no confirmado.
10. **MIVAU, aviso de SIU y datos de costes**. Otras URL de mivau.gob.es y fomento.gob.es devuelven 403 o 000 (no reintentadas).

## Requiere al autor

- **SIU (MIVAU).** Paso: en un navegador, abrir la página del SIU de mivau.gob.es, descargar la capa de suelo urbano y urbanizable por municipio y dejarla en data/raw/v16/oferta_suelo/_terceros/ (si el texto de licencia no es claro) con su fecha. Alternativa: pedir por escrito al MIVAU el fichero completo.
- **MDT05 (IGN/CNIG) para pendientes.** Paso: decidir si se descargan las hojas de las provincias de estudio (formato GeoTIFF). La página del CNIG no respondió a esta petición; hay que abrirla en navegador. Confirmar la licencia (CC BY 4.0 según datos.gob.es, no verificado en el CNIG).
- **DPMT (MITECO).** Paso: descargar a mano dpmt.zip (12,2 MB) desde la página indicada en la fuente 3 y guardarlo en data/raw/v16/oferta_suelo/dpmt_miteco/ con su fecha. La condición de uso es libre con cita.
- **CORINE/CLMS (Copernicus).** Paso: crear cuenta en CLMS si el autor la acepta (requiere registro): no se hace desde este agente.
- **Madrid y GVA (vivienda protegida).** Paso: indicar los URL exactos del catálogo (datos.comunidad.madrid, dadesobertes.gva.es) o pedir a la comunidad el registro de calificaciones y parque público.
- **Natura 2000, licencia.** Paso: confirmar la licencia en el aviso legal del MITECO. Si resulta abierta con cita, pasa de «dudoso» a «sí» y sale de _terceros.
- **Clasificación de licencias municipales de obra.** Paso: el autor busca en INEbase la tabla de «Estadística de Construcción de Edificios» por municipio o provincia (la operación figura en la ficha del INE) y dice el id de tabla.

## Pendiente de cálculo (no descargado)

- Pendiente media o porcentaje >15 % por municipio: se calcula desde el MDT05 (hojas) con proyección ETRS89 y agregación por código INE de municipio. Esta familia no lo calcula.
- Porcentaje de suelo protegido por municipio: combinar Natura 2000 (ya descargada) con DPMT (manual) y el seccionado 2025 para agregar a municipio.
- Usos del suelo (SIOSE/CORINE): tras el paso manual, agregación por municipio.

## Notas
- Los tamaños citados de fuentes no descargadas (SIU, CLC, MDT) no están verificados.
- Ninguna cifra de este fichero entra en cifras_clave ni en publicación: son insumos.
- No se leyó data/sealed ni filas marcadas muestra_sellada_v6.

## Normalización (V16 fase 1)

Script: `src/v16/datos/oferta_suelo.py` (determinista, SEED=20261010, sin red; ~5 min por la geometría). Tests: `tests/v16/test_datos_oferta_suelo.py`. Diccionario: `docs/v16/fuentes/oferta_suelo_variables.csv`. Resultado: `data/processed/v16/oferta_suelo_resultado.json`. capa = C4 y posterior_prereg = False (el corte de V16 no está fijado).

### Salidas
- `data/processed/v16/oferta_suelo.parquet` (versionado; 3 938 filas, 45 KB; redistribuible = sí): INE IMM, nacional (código «00»), mensual (periodo AAAA-MM; fecha_dato = fin de mes). 22 variables `ine_imm_*_indice`: mano de obra (IMM1, 1995-01 a 2026-03), 16 materiales generales y 5 específicos (2012-01 a 2026-03). La desagregación lleva el código de serie INE (IMM*). Unidades: «índice base 2011=100» o «índice base julio 1980».
- `data/processed/v16/oferta_suelo_terceros.parquet` (NO versionado; redistribuible = False; 24 396 filas): Red Natura 2000 (MITECO, edición 2025) por municipio, anual 2025: `miteco_rn2000_superficie_municipio_ha`, `miteco_rn2000_porcentaje_superficie_municipal` y `ine_geo_superficie_municipio_ha` (denominador). 8 132 municipios; 5 656 con alguna superficie en Red Natura.

### Cálculo de Red Natura 2000 (insumo de la restricción física, Q4)
- Geopandas, shapely 2 y pyogrio disponibles; geometría municipal: `data/base/geo/municipios.parquet` (polígonos INE derivados del seccionado, WGS84).
- Ambas capas (península/Baleares EPSG:25830 y Canarias EPSG:32628) y los municipios se reproyectan a LAEA EPSG:3035 (equivalente en área); geometrías reparadas con make_valid; las 1 865 geometrías de sitios se disuelven en una unión única (solapes LIC/ZEC-ZEPA y entre capas), y se intersecta cada municipio con las partes disueltas. Porcentaje = área en Red Natura / área municipal x 100, acotado a [0, 100].
- Comprobaciones: suma de áreas municipales 50,4 Mha (España, ~50,6 Mha); Madrid capital 60 492 ha.
- Marca muestra_sellada_v6 aplicada a los municipios de las provincias de holdout (solo por código).

### Rupturas
1. IMM1 usa base julio 1980; las demás series, base 2011=100: no comparables en nivel sin reescalado. Sin cambio de definición ni de seccionado (todas nacionales).
2. Las series de materiales específicos tienen huecos (161-167 observaciones frente a 171): no se interpolan.
3. Red Natura es una única edición (2025): sin serie temporal. Áreas sobre el polígono municipal 2025; la parte marina de los sitios queda fuera.

### Descartes
- 8 205 municipios en territorios.parquet frente a 8 132 con geometría. Sin geometría (73): 52 códigos «PP000» (pseudo-códigos provinciales, no municipios) y 21 municipios reales de creación o cambio posterior a la cartografía (03141, 04039, 11043, 11044, 13099, 15026, 15063, 17122, 22091, 22132, 22210, 22231, 28409, 36011, 36012, 36062, 41103, 46264, 46265, 46266, 46328). Quedan sin cálculo; lista completa en `oferta_suelo_resultado.json`. Ningún cruce por nombre.
- Sin geometría sin código: ninguna (geometria_sin_territorio vacío).

### Insumos de Q4 que siguen faltando y cómo obtenerlos
| Insumo | Estado | Cómo obtenerlo |
|---|---|---|
| Pendiente (% >15 %) | falta | MDT05 del CNIG, hojas por provincia (descarga manual en navegador); pendiente por celda en EPSG:25830 y agregación por código INE de municipio. Alternativa: WCS del IGN (no probado). Licencia por confirmar. |
| Agua (masas de agua, embalses, lagos) | falta | BDLJE/BCN del IGN o capas de masas de agua de MITECO/Confederaciones; la intersección es igual que la de Red Natura. Alternativa: clase «superficies de agua» de CORINE/SIOSE. |
| DPMT (deslinde y núcleos excluidos) | falta (descarga devuelve HTML) | Descarga manual de dpmt.zip (12,2 MB) en la página de MITECO de deslinde DPMT; uso libre con cita. Dejar en `data/raw/v16/oferta_suelo/dpmt_miteco/` y repetir el cálculo de intersección. |
| Planeamiento (suelo urbano/urbanizable) | falta | SIU del MIVAU (descarga manual; 403 en el agente); mientras tanto, proxy catastral `data/raw/v4/catastro_solares_municipios.csv.gz`. Licencias de obra mayor del INE ECE: falta el id de tabla. |
| Usos del suelo (CORINE/SIOSE) | falta | CLMS exige cuenta; SIOSE del CNIG sin endpoint. Alternativa: descarga manual del autor. |
| Red Natura: licencia | dudosa | Confirmar el aviso legal del MITECO; si es abierta con cita, pasa a «sí» y sale de _terceros. |
