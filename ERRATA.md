# Fe de erratas

Cada entrada indica la versión, el fichero, el error, la corrección y la fecha. Lo publicado no se reescribe: se corrige en una versión posterior y se anota aquí.

| Fecha | Versión | Fichero | Error | Corrección |
|---|---|---|---|---|
| 2026-10-10 | v2 | output/v2/BA/resultado.json, BV/resultado.json, BM/resultado.json («notas») | Las notas dicen «evaluación sellada pendiente» o «NO ejecutada», pero H1, H2 y H7 se evaluaron en la muestra sellada (docs/v2/holdout_accesos.md). | Las notas están desactualizadas y los resultados no cambian. La fuente válida es docs/v2/holdout_accesos.md con los *_sellado*.json. (BK-044) |
| 2026-10-10 | v1 | src/extract_notariado.py | La «edición más reciente» de los actos mensuales se elegía por orden de texto, y '1T2026' quedaba antes que '2019-2020'. | Pasa a orden cronológico (v5, BK-045). Solo afecta a una validación ya rotulada «conceptos distintos: no cuadra». Las salidas en caché no cambian. |
| 2026-10-10 | v4 | `data/raw/gva_vut_municipio.csv` | Fichero de 67 MB versionado, contra la regla de 50 MB. | Pasa a `.csv.gz` versionado; el CSV queda ignorado y con checksum (v5, R1). |
