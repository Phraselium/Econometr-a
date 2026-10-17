# V15 · Inventario único de variables (fase 1.1)

Generado por `python3 src/v15/f1_inventario.py` desde data/base/hechos.parquet (base V10-V14), data/base/variables.parquet y docs/v15/inventario_anotaciones.csv. La tabla completa está en [inventario_variables.csv](inventario_variables.csv): una fila por variable × nivel × frecuencia. Los ficheros de datos versionados de data/raw y data/manual (con su clase de licencia), en [inventario_ficheros_fuera_base.csv](inventario_ficheros_fuera_base.csv).

- Variables distintas: 340; combinaciones variable × nivel × frecuencia: 467; filas: 14.523.489.
- Con alguna imputación (interpolación, reconstrucción o estimación): 20 combinaciones; con más del 20 % imputado: 20.
- Sin anotación de definición o rupturas: 467 combinaciones (se completan en la auditoría).
- No redistribuibles: 18 variables.
- Ficheros de datos versionados (data/raw y data/manual; docs/v13/datos_inventario.csv): 668 (clase a: 667, b: 1, c: 0).

## Por concepto

| Concepto | Variables | Filas |
|---|---|---|
| no consta | 340 | 14.523.489 |

## Variables con más del 20 % de filas imputadas (solo en robustez, regla A del plan)

| Variable | Nivel | Frecuencia | % imputado | Métodos |
|---|---|---|---|---|
| inmig_anual | nacional | T | 100.0 | interpolado |
| vut_registro_gva_reconstruido | municipio | M | 100.0 | reconstruido |
| v12_obra_neta | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| v12_hogares_nuevos_estimados | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| v12_ratio_obra_hogares | municipio | A | 100.0 | contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021 |
| pib_ccaa_q | ccaa | T | 74.66 | interpolacion_loglineal_entre_anclas_T3 / observado_anual_ancla_T3 |
| pob_extranj | nacional | T | 74.19 | observado / interpolado |
| pob_extranj_ccaa_sum | nacional | T | 74.19 | interpolado_loglineal / observado |
| pob_extranj | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| pob_espanola | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| pob_total | ccaa | T | 73.97 | anual_asignado / interpolado_loglineal |
| vut_plazas | provincia | T | 45.83 | interpolado / observado |
| vut_viviendas | nacional | T | 45.83 | interpolado / observado |
| vut_viviendas | ccaa | T | 45.83 | interpolacion_lineal_entre_observaciones / observado |
| vut_viviendas | provincia | T | 45.83 | interpolado / observado |
| vut_plazas | nacional | T | 45.83 | interpolado / observado |
| visados | nacional | T | 41.94 | observado / interpolado |
| terminadas | nacional | T | 41.27 | interpolado / observado |
| pob_total | nacional | T | 41.27 | observado / interpolado |
| pob_extranj_ine | nacional | T | 38.78 | observado / interpolado |

## Rupturas anotadas

| Familia | Rupturas | Documento |
|---|---|---|
