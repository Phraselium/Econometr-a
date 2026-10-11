# Sellado v6 (M0) — rehecho tras la revisión (docs/v6/revision_M0.md)

Fecha: 2026-10-11. Función: `holdout.sellar_v6`. Lado sellado escrito por holdout en `data/sealed/v6_<panel>.csv`; M0 no lo lee. Solo se guarda entrenamiento en `output/v6/M0/paneles/*_train.csv.gz`. Recuentos del lado sellado calculados sobre el panel en memoria; cada fichero sellado lleva su sha256 en `sellado_info.json` (N2).

## Tabla de cortes (un único año sellado por medida, en todos los niveles)

| Medida | Corte (año sellado desde) | Niveles con ese corte |
|---|---|---|
| Compra (valor tasado MIVAU) | 2025 | provincia anual, provincia trimestral (2025T1 en adelante), municipio |
| Alquiler de stock (SERPAVI) | 2024 | provincia, municipio, distrito |
| Contratos nuevos (fianzas GVA/Incasòl) | 2024 | provincia, municipio |

Provincias selladas v6 (11): 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50. Distritos sellados en v3 excluidos de ambos lados (2.136).

## Cobertura del precio en la parte espacial sellada
Provincias selladas con alguna observación de valor tasado (tras B3): 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50. Sin valor tasado: ninguna.

## Unidades y años por panel

| Panel | Corte | Unidades total | Unidades entrenamiento | Unidades selladas | Años entrenamiento | Años sellados | Filas entrenamiento | Filas selladas |
|---|---|---|---|---|---|---|---|---|
| prov_compra_anual | 2025 | 52 | 41 | 11 | 2015-2024 | 2025-2025 | 410 | 162 |
| prov_alquiler_anual | 2024 | 52 | 41 | 11 | 2015-2023 | 2024-2025 | 369 | 203 |
| prov_contratos_nuevos_anual | 2024 | 52 | 41 | 11 | 2015-2023 | 2024-2025 | 369 | 203 |
| prov_trim_compra | 2025 | 52 | 41 | 11 | 2015-2024 | 2025-2026 | 1640 | 736 |
| mun_compra_anual | 2025 | 3063 | 2470 | 593 | 2015-2024 | 2025-2025 | 20530 | 6315 |
| mun_alquiler_anual | 2024 | 3063 | 2341 | 722 | 2015-2023 | 2024-2025 | 18181 | 8664 |
| mun_contratos_anual | 2024 | 3063 | 2341 | 722 | 2015-2023 | 2024-2025 | 18181 | 8664 |
| dis_alquiler_anual | 2024 | 10552 | 6766 | 3786 | 2011-2023 | 2024-2024 | 40673 | 34420 |

## Notas
- En paneles provinciales el lado sellado es (años >= corte, todas las provincias) U (las 11 provincias selladas, todos sus años).
- Límite declarado (B5): el corte temporal cae en la ventana sellada de v2 (`holdout._mascara_sellada`, años >= 2025) y ya se abrió en 8 contrastes de v2. La parte nueva es la espacial. M4 reportará por separado (i) provincias selladas en años de entrenamiento y (ii) último año; las conclusiones se apoyan en (i).
- Contratos nuevos: ninguna provincia de GVA (03, 12, 46) ni de Incasòl (08, 17, 25, 43) está sellada espacialmente (N5).
- Caché de reglas de sellado: ver `cache_sellado` en `src/v6/m0_run.py` (N6 verificado con distritos v3).
