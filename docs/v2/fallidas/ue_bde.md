# Fallos y limitaciones de descarga v2: UE (Eurostat, OCDE, BIS, BCE) y Banco de España

Última ejecución: 2026-10-10 (`src/fetch_ue_v2.py`, `src/fetch_bde_v2.py`). El archivo no existía antes de esta ejecución; se crea aquí con el registro completo.

## 1. Descargas sin fallo de endpoint

Ninguna petición de descarga falló. Cada endpoint se probó antes con una petición pequeña (`lastTimePeriod=1`, `lastNObservations=1/3`, o `Range` de 2 KB para el BdE) y se anotó la última fecha en la salida del script.

## 2. Microdatos de la Encuesta Financiera de las Familias (EFF 2022): NO descargados

- **Estado:** no descargado. No se pudo verificar que la descarga sea pública y sin registro, así que se trata como "requiere registro o solicitud (no verificado)".
- **Lo verificado:**
  - Anuncio del BdE de 05/02/2025: los ficheros de microdatos EFF 2022 "están ya disponibles para uso científico a través de su web" (https://www.bde.es/wbe/es/estadisticas/anuncios/los-ficheros-de-microdatos-de-la-eff2022-estan-ya-disponibles-para-uso-cientifico-a-traves-de-su-web.html). El anuncio no describe el trámite de acceso.
  - La web de la EFF (https://app.bde.es/efs_www/home?lang=ES) es una aplicación Dash cargada con JavaScript. Sin ejecutar JS no aparece ningún enlace de descarga ni texto sobre registro, usuario o solicitud.
- **Alternativa propuesta:** (a) tablas y resultados publicados de la EFF 2022 en el Documento Ocasional 2413 (PDF: https://repositorio.bde.es/bitstream/123456789/36572/1/do2413.pdf, DOI 10.53479/36572), extraídos por pdf-extractor a `data/raw/pdf/` con validación; (b) si el proyecto necesita microdatos, solicitarlos con una cuenta o formulario del BdE, decisión que debe tomar el usuario. Esta descarga no se hace sin confirmación del usuario.

## 3. Incidencias de endpoints corregidas durante la prueba (no son fallos de la fuente)

| Dataset | Intento | Resultado | Corrección aplicada |
|---|---|---|---|
| Eurostat `prc_hpi_a` | unit `I15`, `RCH_A` | vacío | El anual usa `I15_A_AVG` y `RCH_A_AVG` |
| Eurostat `sts_cobp_a` | `BPRM_DW` con `cpa2_1=CPA_F41001` | vacío para todos los países | `BPRM_DW` (miles) usa `CPA_F41001_X_410014` (residencial excepto residencias colectivas). El total de viviendas en número no está publicado en este dataset |
| Eurostat `sts_cobp_a` / `_q` | unit `SQM` | parámetro inválido | `BPRM_SQM` usa `MIO_M2` (anual) |
| Eurostat `nasa_10_nf_tr` | filtro `s_adj` | error 400 (dimensión no definida) | Sin filtro de ajuste (el dataset es anual sin ajuste) |
| Eurostat `prc_hicp_midx` / `parse_periodo` | periodos `YYYY-MM` | error de parseo | `parse_periodo` acepta `YYYY-MM` además de `YYYY-MMM` (cambio en `src/fetch_eurostat.py`, compatible con la versión anterior) |
| BIS `WS_SPP` | frecuencia `A` | sin resultados | Solo trimestral (`Q`); no hay anual en este dataflow |

## 4. Cobertura parcial (datos publicados, sin relleno)

- **Eurostat `sts_cobp_q` (permisos trimestrales, `BPRM_DW` índice 2021=100, SCA):** 29 territorios, pero las series tienen pocos periodos en varios países. Trátese como robustez.
- **Eurostat `migr_imm1ctz`:** sin PT ni UK. Celdas internas sin publicar: BE 2008-2009, BG 2008-2011, HR 2005, UK 2005 (8 NaN en `eu_migr_pop.csv`). Se conservan como NaN.
- **Eurostat HPI (`prc_hpi_a`, `prc_hpi_q`):** sin EL (Grecia) ni UK.
- **Eurostat `nasa_10_nf_tr` y `lfsi_emp_a`:** últimos datos 2025 (anual). Eurostat `tec00113` (renta disponible per cápita en PPS) tiene 12 países, no se usa.
- **BCE MIR (nuevas hipotecas para vivienda):** solo áreas euro (U2 y 21 países). Suecia, Polonia, Hungría, República Checa, Rumanía, Dinamarca, Noruega, Suiza, Islandia y Reino Unido no están en la serie. El valor de ES coincide exactamente con `ecb_tipo_hipotecario_es.csv` en los 284 meses solapados.
- **OCDE (`oecd_house_prices.csv`):** 27 áreas (no se pidió el agregado EU27_2020, que no es OCDE; BG, HR, CY, MT y RO no son OCDE). Publica trimestres hasta 2026-Q3; el último trimestre puede ser preliminar.
- **BIS (`bis_rpp.csv`):** 33 áreas (incluye XM, área euro, y GB, TR). Último trimestre 2026-Q2. Sin RU, UA, BY, RS, MK, BA ni AL (no incluidos en el alcance).
- **Código de país:** Eurostat usa EL y UK; OCDE y BIS usan GRC/GR y GBR/GB. La columna `territorio` conserva el código de cada fuente. La armonización se hace en data-cleaner.

## 5. Series BdE sin publicar en el origen

- `be0819` (saldos a hogares por finalidad, `DF_MESNAA25A1`, `DF_MESNAA26A1`, `D_MEE62100`, `D_MEE62200`, `D_MEE62600`): NaN en el tramo inicial y en periodos sin valor en el boletín (3-281 meses según la columna). No se rellenan.
- `be1911` / `be1916`: 2003 en adelante.
- Último dato: saldos hasta 2026-06 (`be0819`), nuevas operaciones y tipos hasta 2026-08 (`be1911`, `be1903`, `be1906`, `be1916`).
