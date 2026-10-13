# Estado V8

## Hecho
- Rama r8/main desde r7.2/main (e7bf435).
- F0: la mayor parte ya está en v7.2:
  - cifras superadas retiradas;
  - una sola cifra de déficit con bajas;
  - construcción adicional con dosis no nula;
  - ficha de burbuja nacional y regional;
  - test de cifras superadas sobre cifras_clave.
- F0, en esta versión: el marcador «[fecha de publicación: pendiente]» se rotula como pendiente del autor (las etiquetas no se pueden publicar desde el entorno).

## En curso
- F0: clones limpios de v7.2 (`make v7_2` + `make v7` y `make all`) en marcha.
- F1: descarga de las series nuevas (subagente data-fetcher) hacia data/raw/v8.

## Siguiente paso exacto
- Al terminar los clones de v7.2: comparar con lo versionado, cerrar F0 (ERRATA y CHANGELOG si procede) y hacer commit.
- Al terminar la descarga: construir los paneles de F1 (src/v8/f1_paneles.py) y el diccionario.

## Tokens por módulo

| Módulo | Subagentes | Orquestador (estimación) |
|---|---|---|
| F0 | 0 | ~40k |
