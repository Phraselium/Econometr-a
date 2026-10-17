# Familia alquiler_turismo (V16, fase 1)

Descarga: 2026-10-17. Manifiesto con sha256 de cada fichero: `data/raw/v16/alquiler_turismo/_manifest.csv` (82 filas). Scripts: `data/raw/v16/alquiler_turismo/_scripts/` (01 Inside Airbnb, 02 INE Tempus, 03 manifiesto). Ningún fichero supera 50 MB (`_grandes/` vacía); total 231 MB. Los ficheros con datos personales o redistribución dudosa están en `_terceros/`.

## 1. Inside Airbnb (CC BY 4.0)
- Endpoint: `https://data.insideairbnb.com/spain/<region>/<ciudad>/<fecha>/data/listings.csv.gz` (listings detallado). Listado de instantáneas: `https://insideairbnb.com/page-data/sq/d/3176684073.json` (country = Spain), consultado 2026-10-17. La página `get-the-data` solo muestra la última; el JSON de página incluye las instantáneas archivadas (trimestrales, últimos 12 meses). robots.txt solo veta `/get-the-data` a `ia_archiver`.
- Licencia: CC BY 4.0 declarada en https://insideairbnb.com/get-the-data/ (https://creativecommons.org/licenses/by/4.0/). Redistribuible: sí (datos no oficiales; contiene `host_name` y textos libres: excluir de la capa pública).
- Cobertura: 9 áreas (Barcelona, Girona, Euskadi, Madrid, Málaga, Sevilla, Mallorca, Menorca, València) × 4 instantáneas (2025-12, 2026-03, 2026-06, 2026-09) = 36. Se descargan 31 nuevas en `original/insideairbnb/`; las 5 de septiembre de 2026 (Barcelona, Madrid, Málaga, Mallorca, València) ya están en `data/raw/v9/insideairbnb/`. Nuevas áreas: Girona, Euskadi, Sevilla, Menorca (4 instantáneas cada una).
- Notas: `n_filas` del manifiesto es líneas-1 (puede exceder el número de anuncios por saltos de línea en textos). El archivo anterior a 2025-12 no está público (necesita «data request», ver Requiere al autor). El HEAD devolvía 403, pero GET con rango y descarga completa funcionan.

## 2. Registros autonómicos de viviendas de uso turístico
| Región | Fichero | Licencia | Redistribuible | Fechas de alta |
|---|---|---|---|---|
| Madrid | `original/madrid_vut/declaraciones_actividad_vut_2026-10-17.csv` + histórico zip (13 cortes mensuales 2025-04 a 2026-08) y `alojamientos_turisticos_2026-10-17.csv` (https://datos.comunidad.madrid) | CC BY | sí | no; altas/bajas por diferencia entre cortes |
| Andalucía (OpenRTA) | `_terceros/openrta_all_2026-10-17.csv.gz` (178.558 registros; VFT «Completa» y «Por habitaciones») | CC BY 4.0 (datos.juntadeandalucia.es) | dudoso (email, teléfono, titular) | sí: `registration_date`, `activity_start_date` |
| Mallorca | `_terceros/habitatges_turistics_mallorca_2026-10-17.csv` (HUT y ETV, 16.924) | CC BY | dudoso (explotadores) | sí: «Inici d'activitat» |
| Mallorca alojamientos | `original/baleares/allotjaments_turistics_mallorca_2026-10-17.csv` | CC BY | sí | no |
| Menorca | `_terceros/estades_habitatges_turistics_menorca_2026-10-17.csv` (5.430) y `original/baleares/allotjaments_turistics_menorca_2026-10-17.csv` | CC BY | dudoso (teléfono) / sí | no |
| Canarias | `original/canarias/vivienda_vacacional_registro_2026-10-17.csv` (72.183) + diccionario | Aviso Legal GobCan | sí (con cita) | no |
| Canarias ISTAC | `original/canarias/istac_C00065A_000061_v1.29_2026-10-17.csv` (viviendas vacacionales, plazas, ocupación, estancia media, ingresos por isla/municipio, mensual desde 2019-01) | Aviso Legal ISTAC | sí (con cita) | serie mensual |

Endpoints en el manifiesto. Ya en el repositorio, sin redescargar: Comunitat Valenciana (`data/raw/v9/gva_vut`, `data/raw/v11/gva_vut`; el CKAN sigue ofreciendo solo histórico y último periodo, última modificación 2025-11-12, ya descargados), Catalunya (`data/raw/v9/cat_turisme`: el Socrata `t2h3-cgys` sigue sin fecha de alta; licencia «See Terms of Use», no redistribuible), Euskadi (`data/raw/v11/euskadi_vut`, REATE).
- Illes Balears: Ibiza y Formentera no aparecen en el catálogo (solo Mallorca y Menorca); el registro autonómico no es abierto.

## 3. Registro Único de Arrendamientos (RD 1312/2024)
No se ha encontrado publicación abierta de datos agregados (web del Ministerio de Vivienda devuelve 403 al proxy; registradores.org no ofrece datos abiertos localizables; las cifras solo aparecen en prensa citando al Ministerio). No se ha descargado nada.

## 4. Fianzas de alquiler
- GVA e Incasòl: ya en el repositorio (v9). Euskadi EMAL (CC BY 4.0, fianzas, 2016-2025T4): ya en `data/raw/v9/emal`. Ninguna distingue contrato de temporada o habitación en las tablas abiertas halladas.
- Madrid (Agencia de Vivienda Social), Andalucía y Illes Balears: no hay conjunto de fianzas en sus portales abiertos (búsqueda en CKAN de Madrid, Andalucía y Baleares sin resultados). Marcado como inexistente en abierto.

## 5. INE
- Endpoint: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<id>?nult=1000` (JSON Tempus, serie completa, gzip). Licencia: reutilización con cita (https://www.ine.es/aviso_legal). Redistribuible: sí.
- Operaciones: EOAP apartamentos turísticos (239; tablas por CCAA, provincia, zona, punto turístico), EOH hoteles (238; provincia, zona, punto turístico), OAT ocupación en alojamientos turísticos y otros de corta estancia (429, base reciente con residencia del viajero), IPAP (61), VTE viviendas turísticas, medición experimental (410; provincias y municipios, 2020-08 a último dato). 40 ficheros. Duplicados exactos (mismo sha256, marcadores `.dup`): 67191=1993, 3151=2025, 67190=2074.
- Ya existía `data/raw/ine_v2_vut.csv` (VTE hasta 2026-05) y `data/raw/v11/ine_turismo_moviles` (telefonía móvil); esta descarga amplía EOAP/EOH/OAT y renueva VTE.
- Notas: las tablas de «puntos turísticos» (2083/2076, 75193/75198) corresponden a bases distintas; no mezclar sin empalme.

## Fuentes fallidas
- `https://datos.gob.es/apidata/...` devolvió 403 (2026-10-17); `https://www.mivau.gob.es/...` 403; HEAD a data.insideairbnb.com 403 (GET sí funciona).

## Requiere al autor
1. Inside Airbnb anterior a 2025-12 (años previos): solicitud en https://insideairbnb.com/data-requests/ (formulario; indicar ciudades españolas y periodo).
2. Registro Único de Arrendamientos: solicitud de estadísticas agregadas (por provincia/municipio y mes) al Ministerio de Vivienda y Agenda Urbana y al Colegio de Registradores (vía Portal de Transparencia, https://transparencia.gob.es, Ley 19/2013).
3. Catalunya HUT con fechas de alta, Ibiza/Formentera y fianzas de Madrid/Andalucía/Baleares por tipo de contrato: solicitud a la Direcció General de Turisme, Consell d'Eivissa/Formentera y a las agencias de vivienda correspondientes.

## Normalización

Script `src/v16/datos/alquiler_turismo.py` (determinista, sin red, SEED=20261010); salidas `data/processed/v16/alquiler_turismo.parquet` (1.769.895 filas, 5 MB, solo redistribuible = sí), `data/processed/v16/alquiler_turismo_terceros.parquet` (45.196 filas, redistribuible = False, no versionado), diccionario `docs/v16/fuentes/alquiler_turismo_variables.csv` (150 variables) y tabla de correspondencia nombre -> código INE con todos los descartes `docs/v16/fuentes/alquiler_turismo_correspondencia.csv`. Test: `tests/v16/test_datos_alquiler_turismo.py`. capa = C4; `posterior_prereg` = False en todas las filas porque el corte de V16 aún no está fijado; `muestra_sellada_v6` = True en provincia, municipio y sección de las provincias de `holdout.provincias_selladas_v6()` (472.545 filas).

### Decisiones
- **Inside Airbnb** (36 instantáneas: 31 de `original/insideairbnb/` y 5 de septiembre de 2026 de `data/raw/v9/insideairbnb/`, 9 áreas). Agregado propio por municipio y sección censal (sin anuncios individuales): punto en polígono con `data/base/geo/secciones.parquet` (secciones INE 2025, WGS84); anuncios fuera de polígono se asignan a la sección más cercana a ≤0,002° (<1 % de los anuncios; 12 sin asignar en total, descartados). Activo = `has_availability = t`. Variables: anuncios totales, activos, de vivienda entera, con licencia, anfitriones con >1 anuncio activo en el territorio y anuncios de esos anfitriones, n de anuncios con precio, mediana del precio por noche y mediana de `availability_365` y `availability_30`. Las medianas no se publican con <5 anuncios (evita exponer un anuncio individual); los recuentos sí. Periodo = fecha del fichero (frecuencia D). Si faltan los `listings_*.csv.gz` (ignorados por git), el script conserva las filas Inside Airbnb del parquet versionado y avisa; probado.
- **Registros**: recuento de filas por municipio y corte. Madrid VUT (14 cortes: 13 del zip + 2026-10), alojamientos de Madrid (tipo en `desagregacion`), Canarias VV (viviendas y plazas), ISTAC (mensual desde 2019-01; ya trae código INE), alojamientos de Mallorca y Menorca (grupo y estado en `desagregacion`). Terceros (solo recuentos, sin dato personal): OpenRTA Andalucía, HUT/ETV Mallorca y Menorca; incluyen el acumulado de altas a 31-dic de los registros vigentes (reconstrucción con sesgo de supervivencia: sin bajas históricas; solo robustez, declarado en `metodo_dato`).
- **Nombres a código INE**: tabla `territorios.parquet` (solo municipios vigentes) más alias ortográficos explícitos en el script; solo coincidencias únicas (dentro de la provincia cuando la fuente la da); ambiguas y sin coincidencia se listan en la tabla de correspondencia y se descartan.
- **INE (Tempus)**: formato largo directo a partir del JSON. El territorio y la variable se obtienen del nombre de la serie; cada tabla tiene un tipo territorial declarado en el script (nacional, CCAA, provincia, mixto, municipio, punto turístico, zona). Para cada serie el tipo lo fija la tabla de menor alcance en la que figura (evita confundir la provincia «Albacete» con el municipio). Los «puntos turísticos» se aceptan solo si el nombre es un municipio único (o trae el código INE de 5 dígitos como prefijo): supuesto declarado, punto = municipio. Las CCAA uniprovinciales cuyo nombre coincide con su provincia (Cantabria, La Rioja, Illes Balears, Ceuta, Melilla, en tablas mixtas) se publican con el mismo valor en nivel ccaa y provincia (`metodo_dato` lo declara). Los valores secretos o vacíos se omiten. FK_TipoDato = 2 (72.952 observaciones) se marca en `metodo_dato`; el JSON no documenta su significado.
- **Duplicados**: los 3 duplicados exactos de la ficha (tablas 67191, 3151 y 67190, marcadores `.dup`) no se leen. Además, las series presentes en varias tablas (p. ej. 2076 y 75198, 2074/49371/61766) se deduplican por (COD, fecha): 161.476 solapes, sin ninguna discrepancia de valor.

### Rupturas
- INE EOT/EOAP/EOH: series «Total categorías. Dato.» (base de 2014-2015) con COD distinto de las de 1999/2005; no se empalman. Tablas de puntos turísticos con serie nueva desde 2025-01 solapan sin discrepancias. Las tablas 2025, 61766 y 61768 mezclan establecimientos, apartamentos y hoteles con el mismo nombre y COD distintos: 41.506 filas llevan el COD en `desagregacion` (`serie=EOT...`); la asignación de operación se resuelve en la fase 2.
- INE VTE: medición experimental, cortes 2020-08, semestrales (feb/ago) y, desde 2024-11, cada seis meses desplazados; frecuencia M con meses irregulares. Últimos datos: VTE 2026-05, OAT mensual 2026-06 (anual hasta 2025), EOT/EOAP/EOH 2026-08.
- Inside Airbnb: cobertura = área de captura, no el municipio completo; sin precio en 2025-12 ni en Valencia 2026-03; desde 2026-03 el precio es la cotización de una estancia futura (`price_quote`), no el precio de lista; el símbolo es «$» y la moneda no se ha verificado; en 2026-09 la proporción `has_availability = f` sube (p. ej. Madrid 3.711 de 23.109) y reduce los «activos» respecto a marzo-junio; coordenadas desplazadas por la fuente (precisión práctica: sección).
- Madrid VUT: formato distinto en los cortes 2025-04 a 2025-09 (columna MUNICIPIO, ISO-8859-1) frente a Localidad; faltan los cortes 2025-08, 2025-10, 2025-11 y 2026-02; sin fecha de alta.
- ISTAC: unidad de ingresos no declarada (se asume euros); la serie incluye islas y «Desconocido», descartados.
- OpenRTA: el CSV mezcla dos esquemas (72 columnas con cabecera y 92 sin ella); las posiciones del bloque de 92 se fijan por anclas (código de registro, fecha, municipio, grupo) y se comprueban contra el esquema de 72.

### Descartes
- INE: 870 series de zonas turísticas (tablas 2013, 2022, 2039, 48432: sin código INE); 136 series de municipio con nombre repetido (VTE) y 16 + 24 sin coincidencia (p. ej. «San José», OAT); Illes Balears y similares ya no se descartan por ambigüedad (ver arriba).
- Registros: Madrid 36 alojamientos sin localidad; Canarias 4 + 2 registros sin municipio/provincia válida; Mallorca 2 «SENSE DEFINIR»; Menorca 2 vacíos; Andalucía 7 registros de pueblos con provincia errónea o pedanías (Olivares, Alameda, Badolatosa, Campanillas, San Pedro Alcántara, Nerja); 8 islas ISTAC (sin nivel INE). Listado completo en la tabla de correspondencia.
- Registro de Arrendamientos, fianzas por contrato y años previos a 2025-12 de Inside Airbnb: no hay dato en disco (ver «Requiere al autor»).
