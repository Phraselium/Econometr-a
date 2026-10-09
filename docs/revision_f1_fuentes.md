# Revisión independiente F1: fuentes recuperadas sin API (SERPAVI, Notariado, Registradores, GVA)

Fecha: 2026-10-09. Revisor independiente; no hice la extracción. Alcance: comprobar que la validación de los datos recuperados es real
y decidir qué series entran en `data/processed` y con qué papel. **No** he ejecutado `make all` (el dataset se reconstruye después),
**no** he tocado `data/raw` ni los scripts. Todas las comprobaciones se hicieron en memoria contra los originales de
`data/raw/pdf/originales/` y `data/raw/gva_orig/`.

## Veredicto: **REHACER** (parcial y acotado)

La mayor parte de la validación es real y se puede reproducir: las cifras que cotejé coinciden al céntimo con los originales, los
`error_max` declarados se reproducen y no hay valores rellenados ni corregidos a mano. Aun así, hay que rehacer esta parte por cuatro
defectos concretos:

1. **Bug silencioso, con validación falsamente positiva** (`notariado_cv_municipios_anual`). Faltan **València ciudad** y otros
   5 municipios en las ediciones 4T2022 y 4T2025.
2. **`make all` no corre sin red** (`extract_notariado.py`).
3. **Registradores open data**: la serie de 4 trimestres móviles no está marcada en el nombre de la serie ni en la fecha.
4. **SERPAVI España**: el agregado mezcla composiciones distintas de CCAA.

Ninguno de estos defectos invalida los datos de origen. Los cambios necesarios en los extractores son pequeños (ver la lista al final).

## 1. Tabla de decisiones por serie

Leyenda de origen: api = API/CKAN · xls = XLSX/CSV oficial · pdf = PDF con texto nativo (pdfplumber, **sin OCR**). Ninguna
serie procede de OCR.

| Serie (fichero) | Origen | ¿Validado? | error_max (declarado → reproducido) | Decisión | Motivo |
|---|---|---|---|---|---|
| SERPAVI CCAA / provincias / municipios 46 (`serpavi_ccaa`, `_provincias`, `_municipios_46`) | xls | sí (celdas cotejadas: 0 error) | 6,43 pp en la tasa frente al IPVA (Valencia, 2019) → 6,43 / 2019 / corr 0,977 ✓ | **PRINCIPAL** | Lectura directa de un XLSX oficial. Es anual (2011-2024) y mide el stock de contratos declarados en el IRPF, no contratos nuevos. Ojo: el contraste con el IPVA **no es independiente**, porque el IPVA del INE también sale de datos de la AEAT/IRPF. |
| SERPAVI distritos / secciones València (`serpavi_valencia_distritos`, `_secciones`) | xls | sí (mismo XLSX) | n/a | **ROBUSTEZ** (descriptivo) | Unidades pequeñas: mínimo de 10 viviendas y percentiles ruidosos. Útil para mapas o heterogeneidad, no para el modelo principal. |
| SERPAVI España (`serpavi_esp_agregado`) | xls → derivado propio | parcial | 4,39 pp frente al IPVA nacional ✓ | **ROBUSTEZ** (o PRINCIPAL si se rehace con composición constante) | La composición cambia: Navarra entra en 2021 y el País Vasco en 2024 (n_ccaa 17→18→19, contando Ceuta y Melilla). He medido que **la entrada del País Vasco infla el crecimiento de 2024 en +0,71 pp** (5,66 % frente a 4,95 % con composición constante). Además, una media ponderada de medianas no es una mediana nacional. |
| Notariado CGN semestral (`notariado_cgn_extranjeros_semestral`) | xls | sí | T1–T5: 0 ✓. Frente a MIVAU: 832 (6,2 %) en CV y 5.694 (9,4 %) en España ✓ | **PRINCIPAL** | Sumas internas exactas. Frente a la suma de las 3 provincias del PDF, la ratio PDF/CGN se mantiene en **1,055–1,075** en 16 semestres (el PDF incluye VPO y el CGN solo vivienda libre). Es un contraste externo sólido. La fila `SIN_ETIQUETA_EN_ORIGEN` (entre Cataluña y C. Valenciana, valores 14–52) es casi seguro Ceuta+Melilla por el orden alfabético: no consta en el original, así que no se debe renombrar sin fuente. |
| Notariado CV provincias trimestral: `viv_vendidas_esp/ext`, `cuantia_media_esp/ext` (`notariado_cv_prov_trimestral`) | pdf | sí | 0 frente a los totales anuales publicados ✓. Suma de las 3 provincias frente al CGN: 1.463 (7,5 %) ✓ | **PRINCIPAL** (2018T1-2025T4, n=32) | Texto nativo, sumas exactas frente a los totales del propio PDF y contraste externo estable con el CGN (xls). Una sola edición (4T2025), así que no hay mezcla de revisiones. **Limitación:** el 4T2025 lleva una remisión del IUI del 99,90 % y cuenta viviendas con al menos un comprador extranjero. **No mezclar niveles** con el MIVAU (ratio 1,06–1,20). |
| Notariado CV provincias, detalle por nacionalidad (`viv_vendidas_pais`, `cuantia_media_pais`) | pdf | sí (suma = Total, 0) | 0 ✓ | **ROBUSTEZ** | Celdas pequeñas y vacías en origen (no se imputan, correcto). Las etiquetas de varias líneas se reconstruyen con la heurística `fix_label`; las 25 etiquetas resultantes son canónicas. |
| Notariado actos mensuales (`notariado_cv_actos_mensual`) | pdf | parcial (suma = TOTAL: 0 ✓) | revisión entre ediciones de hasta el 6,1 % ✓. Frente al INE: 154 % (otro concepto) | **ROBUSTEZ** | Mide **actos sobre inmuebles**, no solo viviendas. Hay revisiones de hasta el 6 % entre ediciones, y la selección de la "edición más reciente" tiene un bug (ver cambio 4). |
| Notariado municipios anual (`notariado_cv_municipios_anual`) | pdf | **NO** (falso positivo) | "0" declarado, pero solo sobre los bloques que llegaron a extraerse | **EXCLUIR hasta corregir** | **Faltan València ciudad (2022: 2.171; 2025: 2.538), Llíria, Ontinyent, Barx, Sagunt y Canet en las ediciones 4T2022 y 4T2025** (13 municipios en lugar de 19). Causa: el recorte fijo `w/2` (297,6 pt) corta la columna derecha, que empieza en x=295. La línea de cabecera queda como `"Valencia - hasta 4T 2025 O"` y la regex falla en silencio. La comprobación "ciudad ≤ provincia" también se saltó 2022 y 2025 sin avisar. El PNG `..._4T2025_p2.png`, declarado como "revisado", muestra claramente el bloque de València (2.538). |
| Registradores open data (`registradores_opendata_compraventas`) | xls (CSV oficial) | sí | Frente al Anuario PDF: 0 en compraventas (con la conciliación de Ceuta y Melilla documentada) y 0,5 €/m² en precio ✓. Frente al INE ETDP: ≤1,4 % ✓ | **PRINCIPAL**, solo como **anual (T4)** o tratada explícitamente como suma móvil de 4 trimestres | He confirmado que es una suma móvil de 4 trimestres: nacional 2025T1–T4 = 667.058 / 691.863 / 699.638 / 705.357, todas cifras de orden anual. La validación usa solo T4 (correcto) y la columna `nota` lo dice. Pero el nombre de la serie y la `fecha` (inicio del último trimestre) **no** lo reflejan. Usada como trimestral, introduciría un MA(3) mecánico y solapamiento. No se puede reconstruir el flujo trimestral sin un valor semilla. |
| Registradores Anuario: compraventas y €/m² CCAA/provincias (`registradores_eri_anuario`) | pdf | sí | 0 ✓ (sumas exactas de CCAA y provincias frente a España) | **ROBUSTEZ** (redundante) | Repite el CSV open data; es preferible el CSV. |
| Registradores Anuario: capitales (València capital) | pdf | **no** (sin cuadre) | n/a | **ROBUSTEZ** | No hay ninguna restricción contable. Solo comprobé que capital ≤ provincia: 9.961/36.679, 9.844/38.770 y 9.603/40.839. Solo hay 3 años. |
| Registradores Anuario: % compras de extranjeros por CCAA y provincia (+ serie de 8 años) | pdf | sí | 0 entre tablas y ediciones ✓; nacionales + extranjeros = 100 ✓ | **ROBUSTEZ** | Validado, pero es anual y corto (unión 2016-2025 por CCAA, 2023-2025 por provincia). No da para el modelo principal. |
| Registradores Anuario: nacionalidad España y CCAA (`viv_pct_sobre_extranjeros*`) | pdf | **no** | 2,04 pp ✓ (defecto del origen) | **ROBUSTEZ** (descriptivo) | La tabla publicada suma el 97,96 % (lo he comprobado en el texto de la p78: también la columna % s/total suma 13,55 frente a 13,82). La parte de CCAA (`_ccaa`, 170 obs.) no tiene ninguna validación. |
| GVA VUT stock / altas por municipio 2010-2024 (`gva_vut_municipio`: `vut_stock_*`, `vut_altas_*`) | api (CKAN CSV) | sí (reconstrucción reproducida, 0 error) | No había fichero de validación. Lo recalculé: CV dic-2024 = 101.171; València 46250 = 6.090 (2024-12), 5.710 (2019-12), 1.249 (2015-12) ✓ | **PRINCIPAL condicionado** (CV/provincia) | Es un **registro administrativo**, no actividad de mercado. Tiene saltos regulatorios (2016-2019, 2021, purga de 2025-26). Hay 56 registros con baja < alta (no cuentan nunca). Frente al INE VUT experimental, la ratio INE/GVA en la CV es **inestable (0,57–0,71)**: no sirve para validar niveles. Condiciones de uso: etiquetarla como "VUT registradas", añadir dummies de quiebre y no compararla en niveles con el INE. |
| GVA VUT foto de la lista vigente (`vut_foto_*`) | api | n/a | n/a | **EXCLUIR** del panel (dejarla solo como nota) | No es comparable con el stock reconstruido (ver §3.4). |
| GVA padrón: población total por municipio 2005-2022 | api (ZIP IVE) | sí | Lo recalculé: **0 de diferencia en 18 años** frente al INE padrón de València ciudad (DPOP21796). CV = suma de municipios: 0 ✓ | **PRINCIPAL** | Coincidencia exacta con la cifra oficial del INE. |
| GVA padrón: población extranjera por municipio 2005-2022 | api | **parcial** | Grupos = total: 0, pero es **tautológico** (el total se calcula como suma de los grupos) | **PRINCIPAL condicionado** a 1 contraste externo | El mismo método de agregación da 0 error en el total, así que el riesgo es bajo. Pero no hay un contraste independiente del componente extranjero. El contraste frente a la ECP del INE no sirve (concepto distinto: diferencias de +22 % en 2013 y −9 % en 2022 por las bajas por caducidad del padrón). Hay 26 celdas NaN (municipio y año sin fichero ta6), que no deben convertirse en 0. El desglose por procedencia solo existe para **2022**. |

## 2. Comprobaciones que repetí

**SERPAVI (XLSX con openpyxl, en modo lectura).**
- Comparé 5 celdas con el CSV y todas coinciden exactamente:
  - CV `ALQM2_LV_M_VC_19` = 4,787234 · `_15` = 4,021739 · `_24` = 6,321839
  - Municipio 46250: `_24` = 8,181818 · `_13` = 4,735294 · `BI_ALVHEPCO_TVC_24` = 65.742
  - Navarra y País Vasco: vacíos hasta 2021 y 2024, respectivamente
- Recalculé el agregado de España con y sin las CCAA 15 y 16: la diferencia aparece en 2021-2024 (+0,71 pp en 2024).
- Recalculé el contraste Valencia-IPVA8471: diferencia máxima 6,43 pp en 2019, corr 0,977. Coincide con `serpavi_validacion.csv`.

**Notariado.**
- XLSX CGN abierto con openpyxl: Extranjero 1S07 = 33.148; 2S25 = 66.629; CV 1S07 = 9.731; CV 2S25 = 18.722. Coinciden con el CSV.
  Suma de T2 frente a Nacional: 0.
- PDF provincia de Valencia (pdfplumber, p2 y p3):
  - 2018T1 = 7.064/1.602; 2021T3 = 8.069/1.786; 2025T4 = 9.740/2.252; cuantía de extranjeros 2018T1 = 88.778,61 €. Coinciden.
  - Sumas trimestrales frente a la fila Total: 2018 (españoles) 29.278 y 2025 (extranjeros) 9.180. Exactas.
- PNG `notariado_cv_val_extranjeros_4T2025_p10_zoomA.png`: Alemania 2018T1 = 77; Rumanía 2019T2 = 202; RU 2018T2 = 158;
  Otras 2021T4 = 589; Total 2021T4 = 2.126. Las celdas vacías (Noruega 2018T4, Estonia 2021T2) faltan también en el CSV.
  Todo coincide.
- Actos 2024-2025, p3: València ENE-2024 = 4.555, JUN-2025 = 6.063, DIC-2025 = 6.132. Coinciden.
- Suma de las 3 provincias frente al CGN: error máximo 1.463 (2022S2), relativo máximo 7,54 % (2021S1). Reproduce el
  `error_max` declarado.
- Volví a ejecutar `parse_prov_pdf` en memoria sobre los originales: 4.910 filas, 0 diferencias con el CSV guardado.
- Municipios, PDF 4T2025 y 4T2022, p2: el texto contiene "Valencia - hasta 4T 2025 … Total general 2.538" y
  "… 4T 2022 … Total general 2.171", pero ninguno de los dos está en el CSV. Diagnóstico: `extract_words` sitúa "Oliva" en
  x0 = 295 < w/2 = 297,6.
- PNG `notariado_cv_val_municipios_extranjeros_4T2025_p2.png` revisado: muestra València (2.538), Llíria (111) y Ontinyent (96).
  Ninguno está en el CSV de 4T2025.

**Registradores.**
- CSV original: comprobé la suma móvil de 4 trimestres (2025T1–T4 y 2026T1–T2 son cifras de orden anual; la provincia de
  València ronda las 40.000 en todos los trimestres).
- Anuario 2025 (pdfplumber):
  - p35: CV = 108.608 y España = 705.357.
  - p73: CV = 27,65 % y España = 13,82 % (también comprobado sobre el PNG `registradores_eri_anuario_2025_p73.png`).
  - p76: provincia de València = 12,23 %.
  - p78: texto completo revisado; la suma de nacionalidades da 97,96 %, así que el defecto está en el origen.
- Suma de CCAA = suma de provincias = España en 2023, 2024 y 2025: 0.
- Volví a ejecutar `parse_anuario` 2023-2025 en memoria: 5.251 filas, 0 diferencias con el CSV guardado.

**GVA.**
- VUT: reconstruí el stock con otro método (altas acumuladas − bajas acumuladas). Sale idéntico al del script
  (CV y 46250 en 2015, 2019 y 2024).
- Padrón: total de València frente a INE DPOP21796, 2005-2022: diferencia 0 en los 18 años. CV = suma de municipios.
  Población extranjera ≤ población total en todas las celdas.

**Valores rellenados o corregidos a mano.**
- `grep` de fillna, interpolate, ffill, bfill y asignaciones sobre `valor` en los 4 scripts: el único ajuste es
  `od_.loc[...] += add` en `extract_registradores.py:399`. Es la conciliación de Ceuta y Melilla, se aplica **solo en la
  validación** (no se escribe en la salida) y está documentada.
- Las celdas vacías en origen se dejan vacías.

**Errores máximos declarados.** Reproduje los de: SERPAVI (Valencia), CGN T1–T5 y T2, provincias frente al total anual, suma de
3 provincias frente al CGN, sumas del Anuario, nacionalidades del Anuario (2,04) e INE frente a ERI 2025 (6.186). Todos coinciden.

## 3. Hallazgos que afectan al uso

### 3.1. El texto "páginas revisadas" no garantiza una revisión visual real
`PAGINAS_REVISADAS` es una cadena fija en el código. Declara revisada la p2 del PDF de municipios 4T2025, y esa página muestra el
bloque de València que falta en el CSV. Además, las comprobaciones de los municipios son **condicionales a lo que se extrajo**:
cuadran los bloques extraídos, pero nadie comprueba que estén todos.

### 3.2. Etiqueta "validado" de Registradores frente a notarios
En `registradores_validacion.csv`, las filas `*_extranjeros_implicitos_vs_notarios_CGN` dicen "si" con errores relativos del
27 % y del 30 %, y "no" con el 32 %. El umbral del 30 % es arbitrario. Es un contraste de plausibilidad (fuentes y fechas
distintas): debería etiquetarse `plausibilidad`, no `validado=si`.

### 3.3. Reproducibilidad sin red
`extract_notariado.py` llama a `find_doc()`, que hace `requests.get` a valencia.notariado.org en **cada** ejecución, antes de
mirar la caché de PDFs, y no tiene caché a nivel de salida. Sin red, `make data` (y por tanto `make all`) falla en este script.
SERPAVI y GVA sí tienen caché a nivel de salida. Registradores re-parsea desde los originales cacheados y funciona sin red.

### 3.4. VUT GVA: 101.171 (dic-2024) frente a 90.122 (lista de 2026). No es un cambio de qué se cuenta, sino de fecha, de numeración y una purga
- **Fechas distintas.** El histórico es una foto cortada el 2025-01-10 (máximo de alta y baja). La lista es del 2026-10-08/09.
  Hay 21 meses de diferencia.
- **Renumeración.** El histórico usa signaturas `VT-…`/`BL…` y la lista `CV-VUT…-A`. Hay **0 coincidencias literales**. Por la
  parte numérica, unos 78.500 de los 101.222 ALTA del histórico aparecen en la lista. El enlace es aproximado: la fecha de alta
  coincide en el 75 % de los pares.
- **Entradas nuevas.** Unos 12.000 registros de la lista no tienen equivalente en el histórico. Casi todos tienen alta en 2025-26
  (7.993 y 3.994).
- **Purga.** Unas 22.700 VUT del stock de enero de 2025 no están en la lista de 2026, coherente con las bajas de 2025-26.

Conclusión: la foto **no debe encadenarse** con la serie de stock.
- Tipos en el histórico: 100.975 "Unidad de Alojamiento Turístico", 224 "Bloque" y 23 "Conjunto" entre los ALTA.
- La lista no distingue tipo; tiene `rural` S/N (228 S).

### 3.5. Error de etiqueta fuera de alcance, pero importante
`data/raw/ine_vut_valencia_municipio.csv` (tabla INE 39363, código VTE15) **es la provincia de València, no el municipio**:
- 2024-08: 17.853, idéntico a la provincia en `ine_vut_nacional_ccaa_prov.csv`.
- 17.853 + 44.589 (Alicante) + 8.704 (Castellón) = 71.146 = CV, exacto.

`docs/diccionario_variables.md`, líneas 116-119, la describe como "València (municipio)". Hay que corregirlo antes de que entre en
`valencia.csv`.

### 3.6. Diccionario
`docs/diccionario_variables.md` todavía no recoge ninguna de estas series (SERPAVI, Notariado, Registradores, GVA). Hay que
añadirlas con unidad, frecuencia, cobertura y las limitaciones de este informe cuando se reconstruya el dataset.

## 4. Cambios necesarios en los extractores (por prioridad)

1. **`extract_notariado.py::parse_muni`**
   - Sustituir el recorte fijo `w/2` por columnas detectadas con `extract_words`: usar el x0 de la segunda cabecera
     "… - hasta …" o cortar por el hueco vertical entre tablas.
   - Añadir una comprobación de **completitud**: nº de cabeceras "- hasta" en el texto completo de cada página = nº de bloques
     extraídos.
   - Hacer que "ciudad ≤ provincia" **falle** si falta algún año en lugar de omitirlo.
   - Volver a validar las 5 ediciones (deben quedar 19 municipios en cada una).
2. **`extract_notariado.py`: reproducibilidad sin red.** Elegir una de dos:
   - una caché a nivel de salida, como en SERPAVI (si existen los 4 CSV y `notariado_validacion.csv` y no hay FORCE, no
     tocar la red); o
   - guardar las URLs resueltas en un fichero de manifiesto y llamar a `find_doc` solo si falta el PDF.

   Después, probar `make data` sin red.
3. **`extract_registradores.py::parse_opendata`**
   - Renombrar las series a `compraventas_viv_num_4tm`, etc., y poner la unidad "suma móvil de 4 trimestres".
   - Poner como `fecha` el **final** de la ventana (o añadir `fecha_ini_ventana`/`fecha_fin_ventana`).
   - Exportar aparte la serie anual (solo T4) para el modelo.
4. **`extract_notariado.py`: edición más reciente.** `sort_values("edicion")` ordena '1T2026' antes que '2019-2020'. Hay que
   ordenar por una fecha de publicación explícita (añadir una columna `fecha_publicacion` o `orden_edicion`) y aplicar el mismo
   criterio en `build_dataset`.
5. **`extract_serpavi.py`: agregado de España.** Añadir una variante de **composición constante** (15 CCAA de régimen común +
   Ceuta y Melilla, 2011-2024) y usar esa como serie principal. La actual (variable) se queda solo para robustez. Además:
   - documentar en `docs/fallidas/serpavi.md` que a nivel CCAA el País Vasco entra en 2024 (Gipuzkoa en 2022 es solo a nivel
     provincial);
   - anotar en la validación que el IPVA no es una fuente independiente (también sale de la AEAT).
6. **`extract_registradores.py`: validación.** Las filas `*_implicitos_vs_notarios_CGN` deben llevar `validado="plausibilidad"`,
   con el umbral documentado o eliminado. Hay que añadir alguna validación a `viv_pct_sobre_extranjeros_ccaa`, por ejemplo que la
   suma por CCAA sea ≤ 100 y que cuadre con el total de extranjeros de la CCAA; si no, se queda marcada como no validada.
7. **`fetch_gva.py`**
   - Generar `gva_validacion.csv` con: población total frente a INE DPOP (0 de error), CV = suma de municipios, el stock VUT
     recalculado por el método alternativo, la ratio frente al INE VUT (solo de plausibilidad) y el conteo de baja < alta (56).
   - Añadir un contraste de la **población extranjera** de al menos un municipio y año frente al padrón del INE por nacionalidad.
   - Marcar `vut_foto_*` como no encadenable (columna `nota`).
8. **Fuera de los extractores revisados**: corregir la etiqueta "municipio" de `ine_vut_valencia_municipio.csv` y del diccionario
   (es la provincia), o descargar la serie municipal real.
9. **Al reconstruir `data/processed`**: series de PDF solo con `origen` y `validado` propagados; nada del bloque
   ROBUSTEZ/EXCLUIR en el modelo principal; la serie de municipios del Notariado no entra hasta pasar el punto 1.
