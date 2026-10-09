# Proyecto: determinantes del precio de la vivienda en España (módulo C. Valenciana / València)

Idioma de salida: español. Reproducible con `make all` (data → clean → models → report).

## Estructura
- `data/raw/` descargas originales (formato largo: fecha, periodo, serie, valor, unidad, fuente, url) + `_manifest.csv`. **Nunca editar a mano.**
- `data/processed/` bases construidas por `src/build_dataset.py`.
- `src/fetch_*.py` descargas (caché; `FORCE=1` para rebajar) usando `src/utils_fetch.py`.
- `src/fN_*.py` modelos por fase; `src/report.py` informe.
- `output/` tablas, figuras, `registro_busqueda.csv`, `informe.md`.
- `docs/` literatura, diccionario de variables, fuentes fallidas, revisiones.

## Reglas
- No inventar cifras ni referencias; fuentes fallidas → `docs/fuentes_fallidas.md`.
- Comparar modelos en la misma muestra; HAC(4); registrar cada especificación probada.
- "Asociación" salvo identificación explícita.
- Subagentes: data-fetcher, data-cleaner (haiku); lit-researcher, econometrician (sonnet); reviewer (opus, solo en puertas).
- pdf-extractor (sonnet): fuentes en PDF/visor → data/raw/pdf/, con validación (cuadres, serie solapada, revisión visual).
- Datos de PDF/OCR no validados: solo robustez, nunca en el modelo principal.
- Dependencias de sistema para OCR: tesseract-ocr (+spa), ghostscript, qpdf, java (tabula).
