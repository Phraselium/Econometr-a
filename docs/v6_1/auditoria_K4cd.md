# Auditoría K4c y K4d (coherencia de cifras; documentación y publicación)

Scripts: `src/v6_1/k4c_cifras.py` (salida en `output/v6_1/K4C/`), `src/v6_1/k4d_docs.py` (salida en `output/v6_1/K4D/`). Test: `tests/test_k4c_cifras.py`. Capa C4 (auditoría).

Cifras significativas analizadas: 1.916 en 33 ficheros. EN_CIFRAS_CLAVE 797, SIN_FECHA 585 (están en cifras_clave pero su frase no lleva año; el año del dato consta en cifras_clave), HISTORICA_MARCADA 503, HUERFANA 26 (todas en el verificador), CONTRADICTORIA 5 (heurística; revisadas una a una: ninguna real). Los entregables principales output/v5/*.md tienen 0 huérfanas y 0 contradictorias.

| id | ubicación | severidad | efecto en conclusiones | corrección | estado |
|---|---|---|---|---|---|
| K4c-01 | docs/v5/plantillas/informe_tecnico.md:72 (242.400 hogares, constante de corrección de la EPA) | media | ninguno: es un parámetro de v1, declarado como tal en la nota K4b | excepción documentada en el test; marcador `check:cifra-libre` | cerrado |
| K4c-02 | check_v5: 5 líneas de plantillas con etiquetas de versión o módulo (v6.1, K3, M2) y parámetros (±15 %) sin marcador | media | ninguno; `check_v5` fallaba (también en HEAD) | marcador `check:cifra-libre` con motivo en las 5 líneas; `src/v5/check_v5.py` no se toca | cerrado |
| K4c-03 | output/v5/verificador/verificador.md: 26 cifras de ficha sin fila en cifras_clave (intervalos, recuentos de municipios, saldos del Censo) | media | ninguno: proceden de las fichas del verificador (hechos de módulo) y no de los entregables | se listan en output/v6_1/K4C/resumen.md; promover a cifras_clave queda para el cierre | abierto |
| K4c-04 | verificador.md:425 «470 mil millones» frente a CA-CR-saldo-pico (471,8) | baja | redondeo del 0,4 % | sin cambio (redondeo declarado) | aceptado |
| K4c-05 | verificador.md:345, 361, 474 (45,2 %; 2,26; 2.333.816) marcadas CONTRADICTORIA por la heurística | baja | ninguno: otro indicador con redacción parecida | revisión manual registrada en el CSV (`revision_manual`) | cerrado |
| K4c-06 | archive/output/v3 y v4 (5 ficheros) sin aviso «histórico» | baja | evita que se lean cifras superadas como vigentes | aviso añadido en la primera línea | cerrado |
| K4c-07 | 585 cifras con valor en cifras_clave y sin año en su frase | baja | el año consta en cifras_clave (columna fecha_dato) | lista en cifras_entregables.csv (clase SIN_FECHA); sin cambio masivo de redacción | abierto |
| K4d-01 | enlaces de figuras en plantillas y salidas de articulos/ (a_necesidades, c_territorio): faltaba `../` | media | figuras no visibles | corregido en plantillas y re-render | cerrado |
| K4d-02 | output/v2/BS/smoke/informe_v2.md: enlace a BS/contribuciones_periodo.png | baja | figura no visible | ruta relativa corregida | cerrado |
| K4d-03 | CITATION.cff, .zenodo.json, README.md, README_REPLICACION.md en 5.1; CHANGELOG sin v6.1 | media | cita con versión equivocada | todos en 6.1; CHANGELOG con sección v6.1 «borrador, pendiente de cierre» | cerrado |
| K4d-04 | falta DECLARACION_IA.md (README la remitía al apéndice C) | media | transparencia sobre el uso de IA | creada; README enlaza | cerrado |
| K4d-05 | docs/MAPA.md sin docs/v6_1, output/v6_1 ni src/v6_1 | baja | mapa incompleto | filas añadidas | cerrado |
| K4d-06 | docs/literatura.md: 60 referencias con DOI sin marca de cuartil | alta | incumple la regla de referencias | 10 heredan el cuartil de su fila de tabla (VERIFICADA); 50 marcadas «DOI verificado; cuartil no verificado» | cerrado |
| K4d-07 | referencias con «cuartil no verificado» o NO VERIFICADA (11 + 76 con DOI en literatura.md, literatura_instrumentos.md y entregables) | media | evidencia secundaria sin cuartil | listadas en output/v6_1/K4D/referencias.csv; verificar con red en el cierre | abierto |
| K4d-08 | reproducción en clon limpio (HEAD): `make check` pasa ruff, 68 tests (307 s) y check_texto; falló check_v5 por K4c-02 | media | `make check` no pasaba en HEAD | corregido en el árbol de trabajo (pendiente de commit); k4c_cifras corre en el clon | corregido, pendiente de commit |

Notas. El enlace de CHANGELOG, ERRATA y LICENSE se revisó: sin enlaces rotos (0 de 382 .md). No cambia ninguna cifra publicada, por lo que no se anota en ERRATA.md. Clon borrado. `make all` queda para el cierre.
