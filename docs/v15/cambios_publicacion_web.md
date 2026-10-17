# V15 · Páginas que cambian con las correcciones de la 1.0 (antes del depósito, 2026-10-17)

Generadas con `make publicacion` y `make web` tras las correcciones de ERRATA del 2026-10-17. Ningún valor de cifras_clave cambia; cambian la capa de 11 cifras (C1 → C4) y los metadatos de tres variables.

**Método de comparación.** La web (web/_site) no está versionada. Se construyó también desde el commit anterior a las correcciones (c35772b, en un worktree temporal ya borrado) y se compararon las dos con `diff -r`.

## publicacion/ y metodologia/ (versionadas)

| Página | Qué cambia | Por qué |
|---|---|---|
| publicacion/cifras_clave.csv | `capa` C1 → C4 en 11 filas (E-T7-prod, V8-M8-cv-p03/p12-P5-acum-alt/-mivau, VER-A23-V2-1/-2, V10-ATL-A1/A2/A3, V9-D7-c1-dif); valores iguales | Bajadas de capa |
| publicacion/atlas_descriptivo.md | «*Capa C1; … con contraste con Eurostat*» pasa a «*Capa C4; … el contraste con Eurostat es la misma encuesta, no una fuente independiente*». En la tabla de ficheros, a_contraste_eurostat.csv deja de citarse como «criterio de C1» | V10-ATL-A1 a A3 |
| publicacion/informe_v9.md | «Censo 2021 y ECP coinciden en … [C1]» pasa a «… difieren en … [C4: la ECP se apoya en el censo …]» | V9-D7-c1-dif |
| metodologia/historial_conclusiones.md | Nueva «Adenda V15» con las 11 bajadas y los metadatos corregidos | Historial |
| docs/v8/plantillas/README.md (índice de cifras de la plantilla V8) | Columna de capa C1 → C4 en las cuatro V8-M8-cv-*-P5-acum-* | Bajadas de capa |
| publicacion/MANIFIESTO.md, metodologia/MANIFIESTO.md | Huellas de los ficheros regenerados | — |

Sin cambios: el verificador (las fichas VER-A23-V2 ya figuraban en C4 a nivel de afirmación), la página de una hoja, el working paper, el informe técnico, el resumen ejecutivo y los artículos. Ninguno cita estas cifras con la etiqueta C1.

## Web (web/_site)

| Página o fichero | Qué cambia |
|---|---|
| index.html | Hallazgo del atlas sobre sobrecarga del gasto: «Capa C4 …; el contraste con Eurostat es la misma encuesta, no una fuente independiente» |
| metodologia.html | Diccionario: `ipc_alquiler_indice` con unidad «índice 2025=100»; `obra_nueva_neta_catastro` con periodo 2012–2025 y la nota del año de la obra |
| datos/indicadores/catalogo.json | Unidad de `provincia__ipc_alquiler_indice` |
| datos/indicadores/provincia__ipc_alquiler_indice.json | Unidad «índice 2025=100» (valores iguales) |
| descargas/variables.csv y variables.parquet | Unidad y fuente de `permisos`; unidad de `ipc_alquiler_indice`; periodo de `obra_nueva_neta_catastro` |
| descargas/hechos.parquet | Periodo de `obra_nueva_neta_catastro` (un año antes, mismos valores); unidad y fuente de `permisos` e `ipc_alquiler_indice`; marca `muestra_sellada_v6` en las filas sub-provinciales de las 11 provincias de v6 |

Las 311 fichas territoriales, los mapas y las demás páginas son idénticas.
