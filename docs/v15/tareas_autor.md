# V15 · Tareas del autor

## Puerta de la fase 3 (sustituida en V16)
El pre-registro de V15 es **interno, sin sello de tiempo externo**: ya no se deposita en OSF ni se usan campos osf_prereg_* (docs/v16/plan.md, regla A). La puerta es la etiqueta `prereg-v15` publicada en el remoto y apuntando a 542b4fdf398970c817af7abfcd20c92dda299c69. Los comandos para publicarla están en docs/v16/tareas_autor.md (bloqueo B-1: el remoto rechaza las etiquetas desde la sesión).

## Pendiente de decisión (de la fase 0)
- ~~**Capa de las cifras C1 de la 1.0**~~ Resuelto antes del depósito: 11 cifras bajan a C4 sin cambiar su valor (ERRATA, adenda V15 del historial; decisiones G8).
- ~~**Metadatos de la base pública 1.0**~~ Resuelto antes del depósito: año de la obra neta del Catastro, base del IPC de alquiler y unidad y fuente de permisos (ERRATA; decisiones G8; docs/v15/cambios_publicacion_web.md).
- **Cuartiles Scimago** (descarga no automatizable: Cloudflare; docs/v6/fuentes_fallidas.md).
  1. Descargue el ranking de 2024 desde https://www.scimagojr.com/journalrank.php («Download data»).
  2. Deje en docs/v15/scimago_cuartiles.csv solo las revistas citadas en docs/v15/literatura/, con las columnas revista, issn, cuartil, categoria, anio_scimago y fecha_consulta.
  3. `python3 src/v15/verificar_referencias.py --sin-red` rellenará los cuartiles.

  Mientras tanto, todas las referencias con DOI quedan «VERIFICADA (Crossref; cuartil no verificado)».
- **AEAT 2013-2015** (auditoría de renta y microdatos). Los ficheros municipales de esos años no traen declaraciones, renta bruta media ni renta disponible media, y sus valores parecen recuentos. **No son utilizables como renta en euros.** La base usa 2016-2024, así que ninguna cifra publicada cambia. Si se quieren esos años, hay que volver a descargarlos con todas las columnas (descarga HTML por municipio, no automatizada en el repositorio).
- ~~**Filas sub-provinciales de las provincias selladas en v6**~~ Resuelto antes del depósito: docs/v15/contaminacion_v6.md, todos los casos sin efecto, marca en la base y control en make check (decisiones G7).
