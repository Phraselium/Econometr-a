# V15 · Decisiones

## G1. Guardas: el hook bloquea antes que permissions.deny (B1)
- El hook PreToolUse se ejecuta antes que las reglas de permiso. Por eso, en Bash, el rechazo que se ve es el del hook. permissions.deny queda como segunda barrera; en la herramienta Read es la única.
- **Prueba hecha.** `make clean` y listar la muestra sellada fallaron por el hook. Leer un fichero de la muestra sellada con Read falló por permissions.deny.
- **Qué deja pasar la regla (a).** Un heredoc entrecomillado es inerte para el shell, así que la regla no mira su cuerpo.
- **Qué deja pasar la regla (e).** No cuenta el texto de un heredoc que solo escribe un fichero con cat o tee, como una nota que dice «nunca make all». Sí cuenta el cuerpo de un heredoc que alimenta un intérprete (bash, python…).
- **Bloqueo de make check.** El Makefile escribe el PID de make en /tmp/econometra_make_check.lock y lo borra al terminar bien. Si el check falla, el fichero queda, pero con un PID muerto, y la guarda lo ignora. Además, la guarda busca procesos `make check` vivos en /proc.

## G2. Modelos de los subagentes (B2)
Se usan los alias del plan: haiku para el inventariador; sonnet para auditor-datos, lector-literatura, montecarlo y modelizador; opus para revisor-preregistro y arbitro-final. Si un alias no está disponible en la sesión, se usará el más cercano y se anotará aquí.

## G3. Verificación de referencias sin red (B3)
- Crossref se consulta una vez por DOI y la respuesta reducida se guarda en docs/v15/literatura/crossref_cache.json, versionada con la fecha de consulta. Así `make v15_f2` y los tests funcionan sin red.
- El cuartil sale solo de docs/v15/scimago_cuartiles.csv, versionado con la fecha de consulta. Una revista que no esté ahí queda «cuartil no verificado». Nunca se supone un cuartil.

## G4. Metadatos de la base 1.0 con fallos detectados en la fase 1 (no cambian ninguna cifra de cifras_clave)
Las auditorías de la fase 1 han encontrado tres fallos de metadatos en la base pública 1.0. Ninguno cambia una cifra de output/v5/cifras_clave.csv: lo he comprobado buscando cada variable en cifras_clave y en los scripts que las generan. Sí afectan a quien use la base descargable.
- **`obra_nueva_neta_catastro`: periodo desplazado un año.** El fichero de origen t es el stock a 31-12-(t−1); comprobado en data/raw/catastro_urbana_municipios.csv.gz, columna `fecha`. La diferencia etiquetada t es, por tanto, la obra neta del año t−1. V12-B4 ya usaba la convención correcta (`anio_obra`), así que sus cifras no cambian. **V15 usa periodo − 1** en todo cruce por año.
- **`ipc_alquiler_indice`: base mal rotulada.** Se rotula «2021=100», pero su base efectiva es 2025=100 (auditoría de alquiler). Las tasas y los logaritmos en diferencias no cambian. V15 no usa niveles de esta serie entre fuentes.
- **`permisos`: unidad y fuente mal declaradas.** Es un índice de Eurostat, no visados del MIVAU (auditoría de oferta y parque). V15 usa `visados`/`iniciadas` para el MIVAU.

Corregir la base es corregir la 1.0. Según la regla del plan, eso va a ERRATA en una versión posterior y queda **pendiente del autor** (tareas_autor.md). No es condición de parada, porque no cambia ninguna cifra publicada de cifras_clave. Lo dejo escrito por si el autor entiende que la base descargable cuenta como cifra publicada.

## G5. Potencia: método (fase 1.3)
- **Método.** El efecto mínimo detectable se mide por aleatorización placebo (src/v15/f1_potencia.py, 500 réplicas, SEED=20261010). El tratamiento o la exposición placebo se genera al azar e independiente del resultado, así que no se estima ningún efecto.
- **P6.** Usa solo trimestres anteriores a la primera zona tensionada (2024T1), con el mismo número de periodos posteriores que tendrá el diseño.
- **Errores agrupados.** La tasa de rechazo placebo con errores agrupados indica si los clusters bastan. Con 4 provincias (Cataluña) el rechazo es 0,18, frente al 0,05 nominal. Por eso en P6 se agrupa por municipio y, si hay pocos clusters, se usa bootstrap salvaje.
- **Medidas de alquiler.** SERPAVI es la medida de alquiler en los paneles de sección y municipio (stock de contratos declarados). Incasòl es la medida de contratos nuevos en Cataluña (renta media ponderada por contratos de todos los tramos, que no depende del cambio de tramos de 2021).

## G6. Sellado V15 ejecutado (fase 3.3) y filas sub-provinciales de las provincias de v6
- **Ejecución.** `python3 src/v15/f3_sellado.py` se ejecutó el 2026-10-17, antes de estimar nada.
  - Manifiesto: docs/v15/sellado_v15.json, con fecha de corte, último periodo visto, celdas selladas y sha256 de las fuentes.
  - Entrenamiento por pregunta en data/processed/v15/ (versionado).
  - Parte sellada fuera del control de versiones, regenerable de forma determinista desde la base y el manifiesto.
- **Proporción sellada por el bloque espacial V15** (sobre lo que no son provincias de v6): ≈ 15 % (13-15 % según la pregunta), como se diseñó.
- **Filas de provincias v6 sin la marca de sellado.** La base conserva filas de municipio, distrito y sección de las 11 provincias selladas en v6 sin la marca `muestra_sellada_v6`, que solo cubre parte de las filas. sellar_v15 las aparta como selladas. Son el 20-30 % de las filas en P4, P5 y P7, y el 0,2 % en P6.
  - **Consecuencia para V15:** quedan fuera de toda estimación.
  - **Pendiente para el autor:** que la base pública lleve esas filas no altera ninguna cifra publicada de cifras_clave. Pero el cálculo de potencia de la fase 1 las incluyó en los paneles de sección (solo con tratamientos placebo, sin resultados). Queda para el autor decidir si conviene revisar qué análisis de V10-V14 las usaron (tareas_autor.md). Las evaluaciones v6 ya se hicieron, así que son muestras vistas.
- **Control.** check_v15 comprueba que los módulos de estimación (src/v15/p*.py) no lean la base completa, los crudos ni la muestra sellada.
