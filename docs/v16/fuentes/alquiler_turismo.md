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
