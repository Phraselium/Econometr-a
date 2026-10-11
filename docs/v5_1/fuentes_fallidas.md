# Fuentes fallidas v5.1

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba y error.


## T2 (viviendas liberadas por envejecimiento) — prueba 2026-10-11
| Fuente | Endpoint / prueba | Resultado | Uso alternativo |
|---|---|---|---|
| Censo 2021: hogares unipersonales y de pareja por edad del sustentador | WS-Tempus `TABLAS_OPERACION/8` y `/463`, `/70` (Censo, Proyeccion de Hogares): sin tabla de hogares por edad de la persona de referencia | SIN DATO | Tasa de jefatura 65+ de v4/M2 (como B1) |
| Censo 2021 / IMSERSO: poblacion en establecimientos colectivos por edad | Mismo listado: sin tabla; IMSERSO no consultado (sin enlace verificado) | SIN DATO | Supuestos C4 (4-8 % de 75+ en residencia), NO VERIFICADOS |
| Seguimiento de la vivienda heredada (venta/alquiler posterior) | INE ETDP 6154 solo cuenta transmisiones por titulo | NO EXISTE | Rango con X de vacias y secundarias del Censo 2021 |

## T1 · bajas del parque (probado 2026-10-11)
| Fuente | Endpoint | Edición | Fecha | Resultado |
|---|---|---|---|---|
| Licencias de obra, nivel provincial | https://apps.fomento.gob.es/BoletinOnline/?nivel=2&orden=10000000 (bloque 1: tablas 1-10 nacionales y 1002NN10/20/30 por CCAA) | Boletín Online, modificaciones dic-2025 | 2026-10-11 | No hay desglose provincial; solo nacional y CCAA. Reparto provincial por parque (no es medida) |
| Licencias de obra, CCAA | .../sedal/1002NN30.XLS (NN=01..19) | modificadas 2023 | 2026-10-11 | Serie hasta 2022 (Ceuta y Melilla hasta 2019, sin demolición). 2023-2024 con cuota media 2019-2022 y 2025 sin dato |
| Licencias de obra, 2025 | .../sedal/10010600.XLS y 10011000.XLS | dic-2025 | 2026-10-11 | Último año anual: 2024 |
| Ruina, cambios de uso, agregaciones | no localizado endpoint | — | 2026-10-11 | SIN DATO; INE ECE, censo de edificios ruinosos y registros autonómicos no probados |
