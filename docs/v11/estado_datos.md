# V11-DATOS · Estado (2026-10-15, cierre)

## Hecho
- Primera pasada, segunda pasada y continuación del histórico: ver auditoria_exhaustividad.md, cobertura.md,
  fuentes_fallidas.md (bloqueo del servidor frente a bloqueo del entorno) y decisiones_datos.md.
- `make datos_v11`: 405 ficheros verificados.
- `make base`: 14,09 millones de filas, 315 variables; capa pública de 45,9 MB, por debajo del límite de 50 MB.
  La afiliación municipal entra solo con el total de regímenes.
- `make check`: en verde.
  - test_base cuenta las filas del parquet desde sus metadatos, en lugar de cargar una segunda copia que agotaba la memoria;
  - base_v11 lee la versión versionada de catastro_urbana.
- Lista de descargas manuales: docs/v11/descargas_manuales.md.
- Incorporación de lo descargado a mano: src/v11/incorporar_manual.py, dentro de `make datos_v11`.

## Siguiente (para `claude --continue`)
1. Cuando el autor suba ficheros a data/manual/v11/<fuente>/: `make datos_v11`, `make base` y `make check`.
2. En una sesión con la red ampliada, reintentar los hosts de la sección A de fuentes_fallidas.md.
3. `make check` regenera output/v10/web_resumen.csv (tamaño de la web local): restaurarlo con
   `git checkout output/v10/web_resumen.csv` antes de hacer commit (salida publicada; no se modifica).

## Tokens de subagentes
Ninguno (la tarea prohíbe subagentes).
