# V16 · Fase 1 · Familia demanda_internacional

Fecha de la adquisición: 2026-10-17 (UTC, ver fecha_descarga en el manifiesto).
Manifiesto: data/raw/v16/demanda_internacional/_manifest.csv (registro de licencias).
Scripts reproducibles: data/raw/v16/demanda_internacional/_scripts/ (manifiesto.py, bce_sorpresas.py, bde_fijacion.py, ine_etdp_titular.py, comparacion_internacional.py).
Regla del coordinador aplicada: lo que tiene redistribuible «no» o «dudoso» va a data/raw/v16/demanda_internacional/_terceros/ (carpeta no versionada, con su propio .gitignore).

## 1. Sorpresas de política monetaria del BCE (instrumento externo)

### 1a. EA-MPD (Altavilla, Brugnolini, Gürkaynak, Motto y Ragusa, 2019)
- Endpoint: https://www.ecb.europa.eu/pub/pdf/annex/Dataset_EA-MPD.xlsx (verificado: HTTP 200, 377 KB).
- Edición: libro de Excel con 4 hojas; fecha de modificación interna 2025-11-13 (docProps/core.xml). Cobertura declarada en el README de JK: desde 1999.
- Ubicación: data/raw/v16/demanda_internacional/_terceros/bce_sorpresas/Dataset_EA-MPD.xlsx.
- sha256: f417fb861a305e3cbb871a7571c4899ba6bca003d9e087024d2f3f0744426cef.
- Licencia: copyright del BCE (https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html). La página declara copyright y restringe la publicación de documentos de trabajo en otra forma; no concede licencia expresa al anexo. Redistribuible: **dudoso**.
- Nota: el WP 2281 declara que los datos se actualizan periódicamente; no se ha encontrado una página de versiones distinta del propio libro.

### 1b. Choques de Jarociński-Karadi (2020), actualización del repositorio
- Endpoints (verificados HTTP 200): https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/master/shocks_ecb_mpd_me_d.csv y .../shocks_ecb_mpd_me_m.csv.
- Edición: actualización publicada en el repositorio jkshocks_update_ecb (los datos llegan a 2025-10-30; el README remite al EA-MPD del BCE).
- Ficheros: data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_d.csv (1999-01-07 a 2025-10-30; sha256 2327230c45a97c8733ccefba45de354d6e37965c553983ea5ac98badfce413e8) y jk_shocks_ecb_mpd_me_m.csv (sha256 89c5b2ec39509057b3c71f44218424fc8d15d4041b16f31c96613f8fe0965534).
- Variables: pc1 (factor de sorpresa), STOXX50, MP_pm/CBI_pm (sign restrictions simples), MP_median/CBI_median (rotación mediana). Identidades: MP + CBI = pc1.
- Licencia: datos CC BY 4.0; código BSD-3 (README, sección Licensing). Redistribuible: **sí**.
- Ruta de descarga alternativa del autor: https://marekjarocinski.github.io/jkshocks/jkshocks.html (página personal con enlaces a versiones antiguas y a la de Fed).

### 1c. Paquete zip de la web de los autores
- Endpoint: https://marekjarocinski.github.io/jkshocks/shocks_median.zip (HTTP 200, 46 KB). Contiene shocks_ecb_mpd_me_njt_median_{d,m,q}.csv, la versión mediana y los códigos Matlab.
- Ubicación: data/raw/v16/demanda_internacional/_terceros/bce_sorpresas/jk_shocks_median.zip (sha256 cc5e7ebd9e0799b4f7fddfda639134984f1547ad8962369431c1cda2564467ac).
- Licencia: la página personal no declara licencia. Redistribuible: **dudoso**. Se usa solo para contraste con 1b.
- Pendiente: comparar el zip con el csv del repositorio fila a fila antes de usarlos; no se ha hecho en esta fase.

## 2. Banco de España, nuevas operaciones de vivienda por periodo de fijación

- Endpoints (CSV del BdE, HTTP 200; robots.txt sin restricción sobre /csv/): be1903, be1904, be1911, be1912 (https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/...).
- Originales: data/raw/v16/demanda_internacional/bde_fijacion/originales/ (4 ficheros, latin-1).
- Salida larga: data/raw/v16/demanda_internacional/bde_fijacion/bde_nuevas_fijacion_vivienda.csv. 4.544 filas, 568 NaN (celdas «_» del BdE, no rellenadas). sha256 9a27ac9e92ae438c9cc5d5b8137f8c76d832f347b21dc6133671f8c91d011095.
- Series retenidas (crédito a la vivienda, hogares): TEDR tipo medio ponderado, hasta 1 año, más de 1 año y hasta 5, más de 5 y hasta 10, más de 10 (be1904 y be1903: total, excluidas renegociaciones, renegociados); importes totales estimados por periodo (be1911 y be1912).
- Periodo: enero 2003 a la última fecha del BdE (ver manifiesto).
- Limitación: el BdE clasifica por periodo inicial de fijación, no por «fijo» frente a «variable». «Hasta 1 año» es la aproximación a variable. No se afirma una participación fijo/variable sin la tabla del BdE que lo declare.
- Licencia: reutilización con cita del BdE. Redistribuible: **sí**. El enlace del aviso legal del BdE devuelve 404 desde el proxy; no se ha verificado la URL exacta del aviso (pendiente).

## 3. INE, hipotecas sobre viviendas por provincia y mes (ya en el repositorio)

- Ya en el repositorio: data/raw/ine_v2_hipotecas_prov.csv (número e importe; HPT; 2003M01 a 2026M07; 53 territorios = 52 provincias + nacional; 0 celdas vacías). No se redescarga.
- Lo que añadió esta fase: nada.

## 4. Compras por extranjeros y por personas jurídicas

### 4a. Ya en el repositorio (oficial)
- data/raw/mivau_transacciones_residencia.csv: transacciones por residencia del comprador (residentes, no residentes, no consta), trimestral 2007T1 a 2026T2, provincia, CCAA y nacional (49.920 filas).
- data/raw/mivau_transacciones_extranjeros.csv: transacciones de viviendas adquiridas por extranjeros residentes (26.486 filas, 2007T1 a 2026T2).
- Limitación: no hay desglose por nacionalidad.

### 4b. Nuevo (oficial): INE, ETDP, transmitente y titular
- Endpoints: wstempus DATOS_TABLA/50256 y /50272 (HTTP 200).
- Salida: data/raw/v16/demanda_internacional/ine_etdp_titular/ine_etdp_titular_largo.csv (1.016 filas, 0 NaN, sha256 32c7f82f663577a0d0a20e2d5edc18ca4151b45256f97d998b8f1ec3c04d28c3). Originales JSON en ine_etdp_titular/originales/.
- Contenido: porcentajes de compraventa de vivienda según transmitente y titular (persona física o jurídica), nacional. Es la alternativa oficial a las cifras de personas jurídicas de Registradores y Notariado.
- Codificación: FK_Periodo 1 a 12 = mes; 28 = año (verificado con las fechas). Aviso del INE en https://www.ine.es/aviso_legal.htm devuelve 404 desde el proxy; la licencia de reutilización es la de la Ley 37/2007 (pendiente de verificación de URL).
- Nacionalidad: no existe tabla de nacionalidad del comprador en las 17 tablas de la operación ETDP (revisadas por nombre).

### 4c. No descargado
- Registradores, Anuario ERI (cuotas de compradores extranjeros): prohibido reproducir o tratar sin permiso escrito (docs/v14/licencias.md, sección 1). No se descarga.
- Registradores, datos abiertos (ODbL 1.0): licencia clara, pero no se ha verificado si el conjunto tiene desglose por nacionalidad; no se descarga en esta fase (pendiente de revisar).
- Notariado, Portal Estadístico: uso exclusivamente personal y prohibición de transformación. No se descarga.
- Informes del CIEN: licencia ambigua (docs/v14/licencias.md). No se descarga en esta fase.

## 5. Comparación internacional

### 5a. OCDE, Analytical house prices (todos los países disponibles)
- Endpoint: https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,/<38 áreas>.Q....?format=csvfilewithlabels (HTTP 200).
- Salida: data/raw/v16/demanda_internacional/comparacion_internacional/oecd_house_prices_todos.csv.gz (39.923 filas, 38 áreas REF_AREA devueltas, 1956-Q1 a 2026-Q3, 7 medidas: HPI, HPI_RPI, HPI_RPI_AVG, HPI_YDH, HPI_YDH_AVG, RHP, RPI; 0 vacíos). sha256 d0fb8daf70cf971fcbf228f10cf80500f7751b80f6d06490bd833a00b933dda7.
- Ya en el repositorio: data/raw/oecd_house_prices.csv (27 países, 20.581 filas). Se conserva sin cambios; la nueva versión amplía cobertura a áreas no europeas.
- Licencia: términos del OECD. La página de términos (oecd.org) devuelve 403 desde el proxy; no se ha verificado el texto. Redistribuible: **sí** (reutilización con cita; pendiente de verificar el texto).
- Nota: el número de áreas devuelto (38) excede la lista pedida (37): se registra tal cual, sin filtrar.

### 5b. Eurostat HPI (prc_hpi_q), sobrecarga de vivienda (ilc_lvho07a) y tenencia (ilc_lvho02)
- Ya en el repositorio:
  - data/raw/eu_hpi.csv (31 geos, hasta 2026-Q2, 122 series) y data/raw/eurostat_hpi.csv (ES; prc_hpi_q).
  - data/raw/v5/ca_eurostat_ilc_lvho02.csv (tenencia, 6 categorías, 32 geos, 2003 a 2025).
  - data/raw/v5/ca_eurostat_ilc_lvho05a.csv (hacinamiento).
- Nuevo: data/raw/v16/demanda_internacional/eurostat_ilc/ilc_lvho07a_todos_desgloses.csv.gz (endpoint SDMX-CSV, 126.270 filas, 46 geos, 2003 a 2025, desgloses por edad, sexo y situación de pobreza; 175 vacíos marcados por Eurostat). sha256 47cd0adf75ea93c417b0db54cfa846feca441cecfd67a733b241fb8785d9a3d8.
- Limitación: ilc_lvho07a no tiene desglose por tenencia. El desglose por tenencia está en ilc_lvho02 (ya en v5).
- Licencia: reutilización con cita (política de Eurostat; la página de copyright responde 200). Redistribuible: **sí**.

## 6. Autorizaciones de residencia por inversión (golden visa, Q8)

- Intento: https://inclusion.gob.es/web/opi/estadisticas/productos_servicios/infografias (Observatorio Permanente de la Inmigración). Respuesta HTTP 403 en todas las variantes (sin y con cabecera de navegador). robots.txt de inclusion.gob.es: 403. No se ha sorteado el bloqueo.
- Sin serie oficial descargada.
- Cifras de prensa y de despachos (14.576 concesiones 2013-2023, por ejemplo) se consideran no oficiales y no entran en ningún recuento.

## Ya en el repositorio (resumen)
- Hipotecas por provincia: data/raw/ine_v2_hipotecas_prov.csv.
- TAE y TEDR de vivienda (total): data/raw/bde_tipos_hipotecas_nuevas.csv (sin desglose por periodo de fijación).
- Euribor y tipos BCE: data/raw/ecb_*.csv.
- BIS precios reales: data/raw/bis_rpp.csv (no se amplió).
- Residencia del comprador y extranjeros: data/raw/mivau_transacciones_residencia.csv, mivau_transacciones_extranjeros.csv.

## Requiere al autor
1. Decisión de licencia de Dataset_EA-MPD.xlsx (dudoso): si el autor acepta el uso bajo cita del BCE, se puede mover a data/raw/v16/demanda_internacional/bce_sorpresas/ y cambiar redistribuible a «sí» en el manifiesto. Hasta entonces se usa solo a través de los csv de JK (CC BY 4.0), que ya son la versión derivada redistribuible.
2. Golden visa, serie oficial por nacionalidad y año: descarga manual desde el OPI (inclusion.gob.es, estadísticas, flujos de autorizaciones concedidas, vía de inversión). Depositar en data/raw/v16/demanda_internacional/_terceros/golden_visa/ y anotar sha256 y la URL exacta de la tabla.
3. Registradores (ERI) y Notariado: decisión de si se consiguen permisos escritos. Si el autor pide cifras de compras por nacionalidad, la alternativa oficial disponible hoy es el MIVAU por residencia (sin nacionalidad).

## Fuentes fallidas
| Fuente | Endpoint | Error | Fecha verificada | Alternativa |
|---|---|---|---|---|
| OPI, autorizaciones de residencia por inversión | https://inclusion.gob.es/web/opi/estadisticas/productos_servicios/infografias | HTTP 403 (y robots.txt 403) | 2026-10-17 | Descarga manual del autor (requiere al autor, punto 2) |
| Aviso legal del BdE | https://www.bde.es/wbe/es/aviso-legal/ (y variantes) | HTTP 404 vía app.bde.es | 2026-10-17 | Reutilización con cita de las tablas del BdE; URL pendiente |
| Aviso legal del INE | https://www.ine.es/aviso_legal.htm | HTTP 404 | 2026-10-17 | Ley 37/2007; URL pendiente |
| Términos del OECD | https://www.oecd.org/en/about/legal/terms-and-conditions.html | HTTP 403 | 2026-10-17 | Texto pendiente; el dataset se redistribuye bajo cita |
| GitHub API de jkshocks | api.github.com/repos/marekjarocinski/... | HTTP 403 (acceso no habilitado) | 2026-10-17 | Descarga directa con raw.githubusercontent.com (verificada) |
| Eurostat, página de copyright (URL antigua) | ec.europa.eu/eurostat/about-us/policies/copyright | HTTP 404 | 2026-10-17 | ec.europa.eu/eurostat/web/main/help/copyright-notice (HTTP 200) |

## Notas de verificación
- Todos los ficheros nuevos se han descargado con el registro de la cabecera de agente y el checksum por fichero.
- Ninguna fila de data/sealed se ha leído ni escrito. No se ha tocado ningún fichero fuera de data/raw/v16/demanda_internacional/ y docs/v16/fuentes/.
- Tamaños: el mayor fichero versionable es oecd_house_prices_todos.csv.gz (~0,5 MB) y el mayor no versionable (_terceros) es el xlsx del BCE (~0,4 MB). No hay ficheros >50 MB.

## Normalización

Script: src/v16/datos/demanda_internacional.py (determinista, sin red). Salida versionable: data/processed/v16/demanda_internacional.parquet (174.814 filas, capa C4, redistribuible = True). Terceros: data/processed/v16/demanda_internacional_terceros.parquet (33.719 filas de EA-MPD, redistribuible = False, NO se versiona; el script no falla si el libro no existe). Diccionario: docs/v16/fuentes/demanda_internacional_variables.csv. Test: tests/v16/test_datos_demanda_internacional.py.

Decisiones
- posterior_prereg = False en todas las filas: el corte de V16 aún no está fijado. muestra_sellada_v6 = False en todas: no hay niveles provincia o inferior.
- Niveles no INE: «pais» (ISO-2), «zona_euro» (EA) y «agregado_ue» (EA18-EA21, EU, EU27_2007, EU27_2020, EU28 de Eurostat). España en BdE e INE: nacional, código 00.
- Periodos: M «AAAA-MM», T «AAAAT#», A «AAAA», D fecha ISO (reunión del Consejo de Gobierno); fecha_dato = fin del periodo.
- Cruces por código: OCDE ISO-3 a ISO-2 con tabla explícita del script (38 de 38 áreas, todas únicas). Eurostat: EL a GR y UK a GB; XK (Kosovo) se conserva tal cual.

Rupturas
- BdE: la clasificación es por periodo inicial de fijación, no fijo/variable; «hasta 1 año» solo aproxima variable. Hay dos totales (be1903/be1904 e importes be1911/be1912) con sufijo de tabla; no se fusionan.
- INE ETDP: mensual (50256, desde 2007-01) y anual (50272, 2007-2025) comparten variable y se distinguen por frecuencia. Supuesto: el orden del título de la serie es «transmitente. titular».
- Eurostat ilc_lvho07a: las marcas de calidad (b ruptura de serie, u poco fiable, e estimado, p provisional) se conservan en metodo_dato; los agregados de zona euro cambian de composición (EA18 a EA21).
- OCDE: serie desestacionalizada (ajuste S) base 2015 = 100; las ratios vs media de largo plazo tienen unidad propia. Sin interpolaciones.
- JK: el CSV no declara unidad; muestra hasta 2025-10-30. EA-MPD: ventanas horarias distintas desde julio 2022 (nota del libro); fechas del libro en dos formatos (datetime y dd/mm/aaaa).

Descartes
- Celdas vacías: BdE 568, Eurostat 175, EA-MPD NaN de ventanas sin cotización; no se rellenan.
- jk_shocks_median.zip (terceros, dudoso) no se procesa; sigue pendiente su contraste con el CSV del repositorio.
- Sin series de golden visa ni de Registradores/Notariado (sin fichero en disco).
