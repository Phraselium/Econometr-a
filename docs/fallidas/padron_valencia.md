# Padrón de València: intentos fallidos o incompletos

Objetivo: población de València ciudad (INE 46250) por nacionalidad, anual, 1998/2002-2025.
Salida: `data/raw/ine_padron_valencia.csv` (script `src/fetch_padron_valencia.py`).

## Lo que sí se ha descargado

- València municipio, total, hombres y mujeres, anual 1996-2025: INE tabla 2903 (op. DPOP, provincia de Valencia por municipios). Series `DPOP21796/97/98`. Sin desglose por nacionalidad.
- Comunitat Valenciana por nacionalidad (grupos de países) y sexo, trimestral/anual, 2002-2026T3: INE tabla 56942 (op. ECP). 20 series `ECP18xxxx`. Es el nivel más bajo con nacionalidad que la API ofrece.

## Intentos fallidos o no disponibles

| Fuente / endpoint | Búsqueda o URL probada | Resultado | Alternativa |
|---|---|---|---|
| INE wstempus, población municipal por nacionalidad anual | `OPERACIONES_DISPONIBLES` (filtro "Padrón", "Explotación", "municipio"); `TABLAS_OPERACION/22` (DPOP, 65 tablas); `TABLAS_OPERACION/450` (ECP, 78 tablas) | No hay ninguna tabla municipal con nacionalidad anual. Las tablas DPOP por municipio solo dan total y sexo. Las de ECP son nacional, CCAA y provincia. No aparece en la lista de operaciones una explotación del padrón por municipio. | Ninguna en la API para anual. Ver las dos filas siguientes. |
| INE, censo 2021 por municipio y nacionalidad | `TABLAS_OPERACION/463` (CENSOP): tablas 68529 (MUN, sexo y edad x nacionalidad), 69270 y similares (SECC-MUN-PROV) | Existe, pero es una sola observación (2021), no serie anual. No descargado. | Usar como punto de referencia de 2021 si se necesita. |
| INE ECP, provincia de Valencia por nacionalidad | `DATOS_TABLA/56947?nult=1` (PROV_SDET, agrupación de países) | Respuesta: `"No puede mostrarse por restricciones de volumen"`. La tabla 56951 (PROV_SDET) no contiene la provincia de Valencia (solo Baleares y Canarias). | Usar la CCAA (tabla 56942), que sí está disponible. |
| Portal de datos abiertos del Ajuntament, API Explore | `https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets?where=search(...)` | Dominio no resuelve (página "This domain could not be found - Huwise"). | CKAN de abajo. |
| Portal de datos abiertos del Ajuntament, CKAN | `https://opendata.vlci.valencia.es/api/3/action/package_search?q=padron`; `q=poblacion`, `q=nacionalidad`, `q=habitantes`; `package_list` (279 conjuntos) | Ningún dataset de padrón, población por nacionalidad ni por distrito. Solo cartografía (manzanas con población total y por edad 0-14/15-65/66+, `illa-de-cases-cadastrals-amb-dades-de-poblacio`; secciones censales sin población), recursos sociales e indicadores de pobreza (`1_1`). | Ninguna para padrón. Los distritos se pueden tomar de `districtes-distritos` solo como geografía, sin cifras. |
| Estadística municipal del Ajuntament (Oficina d'Estadística) | `https://www.valencia.es/cas/estadistica/inicio` (200, sin enlaces útiles); `/cas/estadistica/poblacion` y `/cas/estadistica/padron` (403 "Request Rejected", firewall); `/ayuntamiento/estadistica.nsf` (403) | Bloqueado por el firewall del portal. Sin acceso a anuarios, series en Excel ni PDF de población. | Pendiente de revisar a mano en un navegador: el anuario estadístico y "Població de València a 1 de gener" por nacionalidad. |
| Distritos de València (padrón por distrito) | Ver fila del CKAN y del portal Ajuntament | Sin cifras de población por distrito en fuentes accesibles. | Pendiente, ver anterior. `data/raw/vlc_padron_distritos.csv` no creado. |

## Validación (resultados de la última ejecución)

- València total = hombres + mujeres: 0 personas de diferencia en todos los años (1996-2025).
- València total 2025: tabla 2903 = tabla 29005 (840.792). Nota: las dos tablas comparten la misma serie INE (`DPOP21796`), así que es una comprobación de consistencia entre endpoints, no una fuente independiente.
- CCAA: total = española + extranjera, máximo 1 persona de diferencia (redondeo de la ECP).
- CCAA: extranjera = suma de los grupos de países, máximo 2 personas. Solo se puede comprobar para 2002-2020, porque la serie UE28 sin España termina en 2020.
- Valores no publicados: 16 observaciones NaN en `ECP182053` y `ECP182062` (Europa menos UE27 y UE27 sin España, desde 2012). Marcados como secreto en la API, sin imputar.

## Pendientes

- Desglose por nacionalidad a nivel municipal anual: no disponible en la API. Requiere el Padrón municipal explotado (Ajuntament o petición al INE), o el uso del censo 2021 como única observación.
- Distritos de València: sin fuente accesible.

## Padrón de València por nacionalidad a nivel municipal (ficheros PC-Axis/CSV del INE), 1998-2025

Esta sección amplía la fila "Desglose por nacionalidad a nivel municipal" de arriba: el dato sí existe
en los ficheros CSV de la explotación del Padrón continuo por municipios (no en la API). Script:
`src/fetch_padron_valencia.py`, función `fetch_nacionalidad_pcaxis()`. Salida:
`data/raw/ine_padron_vlc_nacionalidad.csv` (València 46250 y fila Total provincial; Ambos sexos, Hombres, Mujeres).

**Cobertura**: 1998-2022 con datos. 2023-2025 sin datos (hueco, no interpolado).

**Mapa año → fichero** (provincia 46; ruta base `https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t20/e245/p05/`):

| Años | Fichero | Contenido |
|---|---|---|
| 1998-2001 | `aAAAA/l0/00046004.csv_bdsc` + `00046005.csv_bdsc` | Continentes; países de la UE. Sin principales nacionalidades |
| 2002 | `a2002/l0/00046004.csv_bdsc` + `00046002.csv_bdsc` | Principales nacionalidades (14 categorías) + total, españoles, extranjeros |
| 2003-2019 | `aAAAA/l0/00046003.csv_bdsc` + `00046002.csv_bdsc` | Principales nacionalidades (14 a 38 categorías) + total, españoles, extranjeros |
| 2020-2022 | `https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/33946.csv` (tabla 33946, serie 2003-2022) | Principales nacionalidades (40 categorías) |

**Fallos y huecos**

| Años | URL probada | Resultado | Alternativa propuesta |
|---|---|---|---|
| 2023-2025 | `https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t20/e245/p05/a2024/l0/00046001.csv_bdsc` (y `00046002`, `00046003`; también a2023 y a2025) | HTTP 204, cuerpo vacío | Pedir la tabla a InfoINE; no interpolar |
| 2023-2025 | `https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p05/a2024/l0/&file=00046003.px` | HTTP 404 | Idem |
| 2023-2025 | `https://www.ine.es/dynt3/inebase/index.htm?padre=6232&capsel=6233` (operación Padrón continuo, Municipios) | Solo "Serie 2003-2022"; `t=33946` termina en 2022 (fechaFin 2023-01-24) | Idem |
| 2023-2025 | `https://www.ine.es/ftp/microdatos/padron/2023/disreg_padron_2023.zip` (y 2024, 2025) | HTTP 404 (el último microdato publicado es 2022) | Agregar microdatos 2022 no sirve para 2023+; pedir al INE o al Ajuntament |
| 2020-2022 | `https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t20/e245/p05/a2020/l0/00046003.csv_bdsc` | HTTP 204 (y 404 en el `Tabla.htm` equivalente) | Usar la tabla 33946 (ver mapa) |
| 2002 | `.../a2002/l0/00046003.csv_bdsc` | HTTP 204 | Usar `00046004` (ver mapa) |
| 1998-2001 | principales nacionalidades | No publicadas a nivel municipal en los ficheros de esos años | Solo Total, Española, Extranjera y grupos de continente/UE; ver notas |

**Notas de clasificación y calidad**

- Las categorías cambian entre años: en 2003 hay 14 categorías; en 2008-2019, 38; en 2020-2022, 40 (la tabla 33946 usa "De África", "Europa (sin España)", "País de la UE28 sin España", etc.). Las equivalencias de grupo se han verificado con valores: en 2019 coinciden exactamente con el fichero anual y en 2003-2019 difieren como mucho en 32 personas (revisiones entre tablas). Las agrupaciones UE tienen composición distinta (UE15 / UE25 / UE28 / UE27_2020) y no se mezclan con la etiqueta anual "Total Unión Europea" (la diferencia llega a 3.905 personas en 2003).
- "Total Extranjeros" (2005-2019) y "Total nacionalidades" (2002-2003) se normalizan a `Extranjera`; "Españoles" y "españoles" a `Española`; "Varones" a `Hombres`; los nombres con mojibake ("Am‚rica") se corrigen.
- Crecimiento de extranjeros en València en 1998-2002 (8.035 a 39.818): se señala para revisar antes de usar la serie larga.
- Celdas vacías (secreto) en la fuente: 22 observaciones en total, sin imputar. 1998-2001: `Luxemburgo` (mujeres). 2020-2022: grupos UE27_2020/UE28 y Europa menos UE27_2020/UE28.

**Validación (resultado de la última ejecución)**

- (a) València: total = españoles + extranjeros, máximo 0 personas (75 filas año × sexo).
- (b) València total vs DPOP21796/97/98 en `data/raw/ine_padron_valencia.csv`: 0 personas de diferencia en 25 años y en los tres sexos.
- (c) Provincia 46: suma de municipios vs fila Total. Diferencias solo en 1998-2001, de 1 a 15 personas, en 8 combinaciones (año × sexo × nacionalidad) sin celdas vacías. Por ejemplo, 1999 Española: la suma de 260 municipios da 2.162.936 frente a 2.162.922 en el propio fichero. Es discrepancia de la fuente, no corregida. En 2002-2022 la suma cuadra exactamente en todas las combinaciones completas.
- (d) Cruce anual 2003-2019 vs tabla 33946: países y totales, 0 personas en 1.458 celdas.
- (e) Duplicados entre ficheros del mismo año: 0 personas.
- (f) Extranjera = Total Europa + África + América + Asia + Resto + Oceanía y Apátridas: máximo 1 persona (2001, redondeo).
