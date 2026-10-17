# V15 · Tareas del autor

Pendiente de la fase 3: registro del pre-registro en OSF y `osf_prereg_v15` en proyecto.json. El texto exacto se añadirá aquí al cerrar la fase 3.

## Pendiente de decisión (de la fase 0)
- **Capa de siete cifras C1 de la 1.0** (docs/v15/punto_partida.md, §3.1): E-T7-prod, V8-M8-cv-p03/p12-P5-acum-alt y -acum-mivau, VER-A23-V2-1 y VER-A23-V2-2, V10-ATL-A1 a A3 y V9-D7-c1-dif.
  - Tienen una sola fuente, o dos que no son independientes, frente a la definición de C1 de metodologia/capas.md.
  - Los valores no cambian; cambiaría la capa.
  - Por la regla del plan («un error de versiones anteriores que cambie una cifra publicada: a ERRATA en una versión posterior, nunca se reescribe»), V15 no lo toca. Decida si se corrige en la 1.0.1 con entrada en ERRATA.md.
- **Metadatos de la base pública 1.0** (docs/v15/decisiones.md, G4). Ninguna cifra de cifras_clave cambia. Decida si se corrigen en la 1.0.1 con entrada en ERRATA.md:
  - el periodo de `obra_nueva_neta_catastro` está desplazado un año;
  - la base de `ipc_alquiler_indice` es 2025=100, no 2021=100;
  - la unidad y la fuente de `permisos` (índice de Eurostat) están mal declaradas.
- **Cuartiles Scimago** (descarga no automatizable: Cloudflare; docs/v6/fuentes_fallidas.md).
  1. Descargue el ranking de 2024 desde https://www.scimagojr.com/journalrank.php («Download data»).
  2. Deje en docs/v15/scimago_cuartiles.csv solo las revistas citadas en docs/v15/literatura/, con las columnas revista, issn, cuartil, categoria, anio_scimago y fecha_consulta.
  3. `python3 src/v15/verificar_referencias.py --sin-red` rellenará los cuartiles.

  Mientras tanto, todas las referencias con DOI quedan «VERIFICADA (Crossref; cuartil no verificado)».
- **AEAT 2013-2015** (auditoría de renta y microdatos). Los ficheros municipales de esos años no traen declaraciones, renta bruta media ni renta disponible media, y sus valores parecen recuentos. **No son utilizables como renta en euros.** La base usa 2016-2024, así que ninguna cifra publicada cambia. Si se quieren esos años, hay que volver a descargarlos con todas las columnas (descarga HTML por municipio, no automatizada en el repositorio).
