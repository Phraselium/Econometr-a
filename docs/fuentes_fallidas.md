# Fuentes fallidas o incompletas

Registro de descargas que no funcionan, están truncadas o no se han podido verificar.
Los datos de la tabla "no descargado" no se han inventado.

## Banco de España

| Dato | Estado | URLs / búsquedas probadas | Alternativa propuesta |
|---|---|---|---|
| Esfuerzo teórico anual (accesibilidad a la vivienda) | No encontrado | Descarga de los 400 CSV enlazados desde `temas/estadisticas-economicas-generales`, `temas/instituciones-financieras`, `temas/tipos-interes`, `temas/sociedades-no-financieras` y `temas/mercados-financieros`; búsqueda de "esfuerzo" y "accesib" en cabeceras y páginas: sin resultados | Calcular el indicador a partir de la cuota (tipo ECB `ecb_tipo_hipotecario_es.csv` + precio `bde_precio_vivienda_libre.csv`) y de renta de INE/Eurostat (fuera de este script). Revisar la visualización "Indicadores del mercado de la vivienda" de BIEST manualmente. |
| Páginas de estadísticas con índice de indicadores de vivienda | 404 | `https://www.bde.es/webbe/es/estadisticas/indicadores/si1_1.html`, `https://www.bde.es/webbe/es/estadisticas/temas/si_1_5.html` | Usar los CSV de boletín (`compartido/datos/csv/beNNNN.csv`) que sí funcionan. |
| Índice de carpeta `compartido/datos/csv/` | 403 | `https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/` | Enlaces directos a cada CSV (funcionan). |

Series BdE descargadas (ver `src/fetch_bde.py`):
- `be2507.csv`: precio medio m2 de vivienda libre tasada (`DHIVTNOAPLPMMUVT_*`). Trimestral. Las series de vivienda nueva y usada solo tienen datos desde 2013. El origen "Ministerio de Vivienda" del enunciado no aparece en el CSV ni en la página del BdE; queda sin confirmar.
- `be1901.csv`: tipo medio de adquisición de vivienda libre (`D_1T9H0000`). Mensual.

## Banco Central Europeo (data-api)

| Serie | Problema | Alternativa propuesta |
|---|---|---|
| `ICP/M.ES.N.000000.4.ANR` (IAPC España, tasa anual) | La serie termina en 2025-12 (estado `E`, estimada). El BCE indica en la metainformación que deja de publicar el índice actual tras el cambio metodológico de 2026. | Eurostat `prc_hicp_manr` (geo=ES, coicop=CP00), fuera del alcance de este script. |
| `FM/B.U2.EUR.4F.KR.MRR_FR.LEV` (tipo BCE operaciones principales) | Serie de fechas de cambio: 48 observaciones (la última 2026-09-16), no mensual. | Expandir a mensual con el tipo vigente a cierre de mes en la capa de limpieza (data-cleaner). |

## INE (src/fetch_ine.py)

Descargas con fallo de endpoint: ninguna. Las siguientes búsquedas no encontraron la serie pedida (3 intentos o más por búsqueda, sobre `OPERACIONES_DISPONIBLES` y `TABLAS_OPERACION/{id}`):

| Dato pedido | Estado | Búsqueda probada | Alternativa propuesta |
|---|---|---|---|
| Encuesta Continua de Hogares (ECH, anual) | No encontrada | Ninguna operación de INE con nombre "Encuesta Continua de Hogares" en `OPERACIONES_DISPONIBLES`; búsqueda de "Hogares" y "ECH" en las 129 operaciones | 60131 (hogares ECP, trimestral desde 2021) es la fuente disponible. Para renta de hogares, ADRH (op. 353, atlas de renta) o Encuesta de Condiciones de Vida fuera de este script. |
| Renta disponible bruta de los hogares (trimestral) | No encontrada a nivel hogares | `CTNFSI` (op. 246), tablas 62265, 80330, 67203 y 80333: solo aparece renta disponible de la economía total | Se descarga 80333 (renta disponible bruta, total de la economía, CTNFSI, trimestral). No es renta de hogares: usar con cautela. |
| Inmigración total trimestral (suma de todas las nacionalidades) | No publicada como serie única en las tablas de ECP (59011, 59013, 59020, 59012) | Búsqueda de nombres con "Total. Flujo" o "Total Nacional. Total" en las tablas de flujo trimestral | Se descarga 69687 (total anual EMCR). Para el total trimestral hay que sumar las nacionalidades de 59011 en la capa de limpieza y declararlo. |
| Inmigración trimestral por CCAA con total (sin nacionalidad) | No localizada | Tablas de la operación ECP (op. 450) y EMCR (op. 455) | 59013 (CCAA × nacionalidad, trimestral desde 2023T2). Para CCAA anual sin nacionalidad: 69691 (EMCR). |

- **Tabla 69691 (EMCR, inmigración anual por CCAA, sin nacionalidad): NO descargada.** Sigue pendiente como alternativa para el flujo anual por CCAA; hoy no hay flujo anual por CCAA en `data/raw`. Mientras tanto F3 usa Δ de los stocks 77019 (`panel_ccaa_a`).
- **Calendario de la estadística VUT (INE, tabla 39366) cambió**: hasta 2024-08 se publicaba en febrero y agosto; desde 2024-11 se publica en **mayo y noviembre** (2024-11, 2025-05, 2025-11, 2026-05). `valencia.csv` asigna may→T2 y nov→T4 desde 2024-11.

## MIVAU, Ajuntament de València, IVE/PEGV y Notariado/Registradores (src/fetch_mivau.py, src/fetch_valencia.py)

Última comprobación: 2026-10-09.

### 1. Estado tras la recuperación (escalera API → PDF texto → OCR → no recuperable), 2026-10-09

Detalle de cada intento en `docs/fallidas/<fuente>.md`. Decisión de uso: `docs/revision_f1_fuentes.md` (revisor).

| Fuente | Peldaño que funcionó | Resultado | Lo que sigue sin recuperarse | Detalle |
|---|---|---|---|---|
| SERPAVI (alquiler, AEAT) | 1 · XLSX oficial en `cdn.mivau.gob.es` | 2011-2024 anual: CCAA, provincias, municipios prov. 46, València ciudad, 19 distritos, 590 secciones (`data/raw/pdf/serpavi_*.csv`) | Visor con reCAPTCHA (no se elude); ArcGIS con token. Sin fila oficial «España»: agregados propios (composición variable / constante / encadenada) | `docs/fallidas/serpavi.md` |
| Padrón València por nacionalidad | 1 · INE PC-Axis anuales + tabla 33946 | 1998-2022, València ciudad × nacionalidad (`ine_padron_vlc_nacionalidad.csv`); total ciudad 1996-2025 (DPOP) | 2023-2025 por nacionalidad (no publicado a nivel municipal); distritos (solo PDF del Ajuntament, no extraído); `valencia.es` 403 | `docs/fallidas/padron_valencia.md` |
| IVE / PEGV | 1 · CKAN `dadesobertes.gva.es` (no el IVE) | VUT Registre de Turisme 2010-2024 por municipio; padrón por sección 2005-2022 agregado a municipio | `ive.es`, `pegv.gva.es`: corte de túnel en el proxy del entorno (no se elude). Compraventas/precios IVE no recuperados | `docs/fallidas/ive.md` |
| Notariado | 1 · anexo XLSX CGN; 2 · PDF Colegio Notarial de Valencia (pdfplumber) | CGN extranjeros semestral 2007-2025 (España/CCAA); CV provincias trimestral 2018-2025; municipios anual 2021-2025 (19 municipios, València incluida) | API `penotariado.com` privada (400 sin autorización); €/m² de todas las compraventas | `docs/fallidas/notariado.md` |
| Registradores | 1 · CSV open data (cabeceras de navegador); 2 · Anuarios ERI 2023-2025 (pdfplumber) | Compraventas, importe y €/m² 2007-2026 (suma móvil 4T + anual T4); % extranjeros CCAA/provincia/capital | Trimestres individuales (no recuperables de la suma móvil sin valor semilla); extranjeros anteriores a 2023 | `docs/fallidas/registradores.md` |
| Población y hogares por CCAA (INE) | 1 · API wstempus (tablas 77019, 65269, 65285) | Población por CCAA y nacionalidad/grupo de países 2002-2025 (anual); hogares EPA trimestrales 2002-2026 (nacional) | Hogares por CCAA; 56947 (restricción de volumen) | `docs/fallidas/ine_ccaa.md` |

No ha hecho falta OCR (peldaño 3) en ninguna fuente: todos los PDF usados tienen capa de texto.

### 2. Fuentes parciales o sustitutas (documentar en el análisis)

- **Visados de dirección de obra (CSCAE) y certificados de fin de obra (obj. 2).** No están en el MIVAU. Se usan las series mensuales "viviendas libres iniciadas" (tabla 32100500, `mivau_visados.csv`) y "viviendas libres terminadas" (tabla 32101000, `mivau_fin_obra.csv`), del Boletín de Fomento. Son proxies: no son visados ni certificados de fin de obra, y su definición exacta no consta en el fichero.
- **Transacciones por municipio (obj. 5).** `mivau_transacciones_municipios.csv` solo contiene los municipios que aparecen en la lista >25.000 hab. de la tabla 35103500 (305 de 306 emparejados por nombre; Vila-real/Villarreal no aparece en la tabla de transacciones). El Boletín publica todos los municipios (tabla 34010210, ~240 MB en CSV); el fichero completo se puede regenerar desde `data/raw/mivau_xls/34010210.XLS`.
- **Valor tasado, vivienda libre antigüedad (35101500, 35102000).** Disponibles en el Boletín, no incorporadas en esta descarga.
- **Precio de la vivienda libre del Ajuntament de València (`vlc_precio_vivienda_libre.csv`).** Cobertura solo 2021T2-2022T2 en el recurso CKAN. La fuente primaria no aparece en el recurso. Sirve solo como contraste.
- **Idealista / Fotocasa.** PRIVADA: no descargar. Solo para robustez (ver `CLAUDE.md`).

### 3. Notas de acceso

- Los XLS de `apps.fomento.gob.es/BoletinOnline2/sedal/` responden con User-Agent del proyecto. Algunas páginas HTML del MIVAU (`www.mivau.gob.es`) devuelven 403 a clientes sin navegador; el script no raspa HTML, solo descarga XLS e INE API.
- Algunos ficheros `.XLS` del Boletín son en realidad xlsx; `utils_fetch.read_excel_any` detecta el formato por cabecera.
