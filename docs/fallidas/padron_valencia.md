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
