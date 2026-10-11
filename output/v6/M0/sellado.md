# Sellado v6 (M0)

Fecha: 2026-10-11. Función: `holdout.sellar_v6` (criterio temporal: año >= último año del desenlace del panel; espacial: provincias selladas v6). La parte sellada la escribe holdout en `data/sealed/v6_<panel>.csv`; M0 NO la ha leído. Sólo se guarda la parte de entrenamiento en `output/v6/M0/paneles/*_train.csv.gz`. Recuentos del lado sellado calculados sobre el panel en memoria antes del corte, sin abrir `data/sealed`.

Provincias selladas v6 (11): 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50. Distritos sellados en v3 excluidos de ambos lados (2.136 distritos, `holdout.distritos_sellados_v3`).

Nota técnica: `holdout.distrito_sellado_v6` y `municipio_sellado_v6` releen el VUT (1,6 M filas) en cada llamada. M0 las sustituye por una caché con las mismas reglas (`cache_sellado` en `src/v6/m0_run.py`), verificada en una muestra de códigos. No se modifica `src/holdout.py`.

| Panel | Desenlace (último año) | Unidades total | Unidades entrenamiento | Unidades selladas | Años total | Años entrenamiento | Años sellados | Filas entrenamiento | Filas selladas |
|---|---|---|---|---|---|---|---|---|---|
| prov_compra_anual | ultimo_anio=2025 | 52 | 41 | 11 | 2015-2025 | 2015-2024 | 2025-2025 | 410 | 162 |
| prov_alquiler_anual | ultimo_anio=2024 | 52 | 41 | 11 | 2015-2025 | 2015-2023 | 2024-2025 | 369 | 203 |
| prov_contratos_nuevos_anual | ultimo_anio=2025 | 52 | 41 | 11 | 2015-2025 | 2015-2024 | 2025-2025 | 410 | 162 |
| prov_trim_compra | ultimo_anio=2026 | 43 | 38 | 5 | 2015-2026 | 2015-2025 | 2026-2026 | 1672 | 306 |
| mun_anual | ultimo_anio=2025 | 3063 | 2470 | 593 | 2015-2025 | 2015-2024 | 2025-2025 | 20530 | 6315 |
| dis_alquiler_anual | ultimo_anio=2024 | 10552 | 6766 | 3786 | 2011-2024 | 2011-2023 | 2024-2024 | 40673 | 34420 |

Notas: en paneles provinciales, el lado sellado combina el corte temporal (años >= ultimo_anio, en todas las provincias) y las 11 provincias selladas (todos sus años). En `mun_anual` las unidades selladas son municipios de esas provincias. En `dis_alquiler_anual` son distritos de esas provincias (sin distritos v3). En `prov_trim_compra` el corte es 2026 (último año con valor tasado trimestral); sólo 43 provincias tienen dato en la fuente.

Límite declarado: las provincias y los distritos se usaron de forma descriptiva en v4-v5, así que la validación v6 no es una muestra que nadie haya visto nunca (decisiones.md).
