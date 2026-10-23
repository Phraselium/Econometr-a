# Consolidación final · Paso 1: base restaurada (2026-10-23)

`make base` en solitario (src/v10/geo.py y src/v10/base.py; 6 min 34 s). Resultado de base.py: 14.523.489 filas en la tabla
completa, 14.467.304 en la capa pública, 340 variables, 56.579 territorios.

## Comparación con el manifiesto

El manifiesto de la capa pública son los ficheros versionados en git (data/base/publica/*.parquet, data/base/geo/**, los parquet
de dimensiones de data/base y docs/v10/diccionario_base.md; inventario en docs/v13/datos_inventario.csv) y, en el paquete de
Zenodo, el CHECKSUMS.sha256 que se genera a partir de ellos.

| Fichero | Comprobación | Resultado |
|---|---|---|
| data/base/publica/*.parquet (7) | `git status` tras `make base` | sin cambios: coinciden byte a byte con lo versionado |
| data/base/geo/** y parquet de dimensiones | `git status` | sin cambios |
| docs/v10/diccionario_base.md | `git status` | sin cambios |
| data/base/hechos.parquet (no versionado, > 50 MB) | sha256 antes y después | igual: `a8ae4998d40057fa2834a105528a283f947ec2e6405a74c50859e07c8ef31377` |
| data/base/vivienda.duckdb (no versionado) | identidad fila a fila de sus 8 tablas con los parquet (`EXCEPT ALL` en los dos sentidos) y tests/v10/test_base.py | 0 filas de diferencia en las 8 tablas; 9 tests aprobados |

sha256 de la capa pública tras la restauración:

| Fichero | sha256 |
|---|---|
| publica/cifras_clave.parquet | `e16a8f905ef81d12badca1711207db38f3853701f86b919a7acb54e0c6d105f9` |
| publica/hechos.parquet | `8c02b9890a45f5eb16917f0167a7853e9a3307a8048e0022bba72ae69a429c25` |
| publica/regulacion_zonas.parquet | `f9fd77777e9498cee2613af0f3d5fe1a3bf0858c4ed9dc28141c59227a774fa4` |
| publica/territorios.parquet | `6e7b5d5f315720a6127e03d4a04fcacf38bd16755c53bbfc88db12033eecf971` |
| publica/v8_atribucion.parquet | `8a8e39864771dca29f39db0e696bef07f585bec6ae57ebabd28ce0de5d5e70a8` |
| publica/v9_efectos.parquet | `7de61eca6c94bb94bc60cc86fe99f34a33bb340aa0fdbb0ad2bf938c40388f8f` |
| publica/variables.parquet | `26fe4fcc543c1b68bf8c3fbcc76dae8c0ce4224f976cdb950efca1bbdf3e7366` |

## vivienda.duckdb: no había huella con la que comparar

vivienda.duckdb no se versiona (docs/v10/decisiones.md) y ningún manifiesto anterior registra su sha256; K13 la había retirado del
disco. No es una discrepancia: su contenido se comprueba contra los parquet, que sí tienen manifiesto. El sha256 del fichero de esta
restauración es `0d97c7d08f7f557276873bf6bd0413e59abcde5031da006c2f3d8dd62bee2d13`; queda como referencia, sabiendo que DuckDB no
garantiza el mismo fichero byte a byte entre ejecuciones ni versiones, de modo que la comprobación válida es la de contenido.

## Después de la restauración

La consolidación añade 9 cifras a cifras_clave (V18-AUX-JE-*, K15 de docs/v18/decisiones.md; ERRATA del 2026-10-23). Las copias de
cifras_clave de la base (data/base/cifras_clave.parquet, publica/cifras_clave.parquet y la tabla cifras_clave de vivienda.duckdb) se
actualizan con la tabla nueva; el resto de la base no cambia.
