# Publicación 2.0: preparada, sin publicar (2026-10-23)

Ensayo de la consolidación final. Nada se ha subido a GitHub público, Zenodo ni OSF: lo hace el autor (docs/tareas_autor.md).

## Versión
proyecto.json: `version_publica` 2.0, `fecha_version` 2026-10-23, `estado_publicacion` «preparada y sin publicar». La 1.0 (2026-10-16) no llegó a depositarse. Puertas de entrada, CITATION.cff, .zenodo.json, consulta/ y web regenerados con la 2.0 (`make metadatos publicacion consulta web`); check_v13 comprueba que todas declaran la misma.

## Paquete de Zenodo (`make paquete_zenodo`)
- `_deposito/vivienda-espana-evidencia-2.0/` (ignorado por git): 5.467 ficheros incluidos, 73 versionados excluidos, 7 variables AEAT quitadas de la capa pública, 1.510 MB.
- `sha256sum -c CHECKSUMS.sha256`: correcto en todos los ficheros. sha256 del propio CHECKSUMS.sha256: `0737d4265abdc593c1d9264f6ac6b1d004c765bdb0e048eb475f20b831acdf69` (de este ensayo; el autor regenera el paquete desde el commit final).
- Incluye publicacion/documento_final/ (documento y resumen ejecutivo).
- No se generó el zip (duplicaría el tamaño en un disco con 2,6 GB libres); lo hace el autor con `--zip`.

## Árbol público (`src/v14/arbol_publico.py`)
- 4.455 ficheros, 1.140 versionados excluidos, 31 tablas redactadas, origen c437a8d.
- **Desviación:** se generó con `--sin-git` en el directorio temporal de la sesión, no con `make arbol_publico DEST=…`, porque el árbol con su repositorio git no cabía junto al paquete en el disco de la sesión (y no se pudo borrar el paquete). El contenido es el mismo; el commit único «Versión 2.0» lo crea `make arbol_publico` en la máquina del autor.
- El primer intento se detuvo por dos rutas locales en ficheros versionados (docs/v16/preparacion_2_0.md y el valor por defecto del directorio temporal de src/v18/estimacion/e1_adquisicion.py); se corrigieron y el árbol se generó sin avisos.

## Escaneo de series de terceros (`src/v14/escaneo_terceros.py --valores`)
Resultados fichero a fichero en docs/documento_final/escaneo_2_0/ (el escaneo de la 1.0 en docs/v14/escaneo_terceros.* no se reescribe).

| Ámbito | Ficheros con hallazgos | Sin revisar (no estaban en la lista de la 1.0) | Coincidencias por valores |
|---|---|---|---|
| Repositorio | 99 | 16 | — |
| Árbol 2.0 | 73 | 16 | 3 |
| Paquete 2.0 | 75 | 16 | 3 |

- **Coincidencias por valores (3): falsos positivos.** Una ficha bibliográfica (docs/v18/bib/inmigracion/sa_2015_iza.md), una tabla de cobertura temporal por variable (output/v15/auditoria/alquiler/cobertura_temporal_variables.csv, años y recuentos) y un informe de estimación (output/v18/estimacion/e6/informe.md). Ninguno contiene una serie de Notariado ni de Registradores.
- **Hallazgos sin revisar (16), decisión del autor.** Ficheros posteriores a la revisión de la 1.0 que nombran una fuente: claves de metadatos o de sellado (docs/v14/escenarios_resultado.json, docs/v16/sellado_v16.json, docs/v18/sellado_v18.json, output/v16/f2_hechos/control.json, output/v16/potencia/resultado.json, output/v16/replica/v10_a/resultado.json, output/v16/auditoria/tension_social/resultado.json, output/v15/auditoria/precios_compra/resultado.json), la hoja de la revisión externa 2.0 (cabeceras con el nombre de la fuente) y **seis tablas derivadas de la AEAT** (output/v12/b5/aeat_cv_2013_2015.csv, aeat_cv_declarantes_inmuebles.csv y output/v15/auditoria/renta_microdatos/aeat_*.csv, con su resultado.json). Con `terceros_1_0.aeat = agregados` (V14.4) esas tablas entran en el árbol y en el paquete; el autor debe confirmar que son agregados propios y no la serie, o excluirlas, antes de publicar (docs/tareas_autor.md, punto 2).

## Revisión externa 2.0 (`make revision_externa_2_0`)
revision_externa/2_0/: muestra.csv y hoja_revision.xlsx (40 cifras del documento final, estratificadas por capa y clase V18, SEED=20261010: C1 4, C2 4, C3s 1, C4 sin clase V18 4, SUGESTIVO 3, ASOCIACIÓN 4, NO CONCLUYENTE 2, NO ESTIMABLE 4, sin clase propia 14), resumen_ejecutivo.pdf (dos páginas apaisadas en español y una en inglés) y guía de dos páginas (guia.md y guia.pdf).
