# V16 · Q8 · Compras de no residentes (grupo A, entrenamiento)

**Capa C4, descriptiva, pendiente de evaluación sellada.** Sin estimador de efecto, sin p-valor y sin lectura causal. Fecha de corte 2026-10-17. Fuente: data/raw/mivau_transacciones_residencia.csv (nivel CCAA y ciudad autónoma, 9 CCAA de entrenamiento + Ceuta y Melilla); sin muestra sellada.

<a id="v16-q8-1"></a>
## Cuota de no residentes
- Ventana 2024T2-2025T1: **8,69 %** (45884 de 528270 transacciones).
- Ventana 2025T2-2026T1: **7,35 %** (39453 de 536568).
- No residentes extranjeros: 8,13 % → 6,81 %.

<a id="v16-q8-2"></a>
## Variación
-1,33 pp entre ventanas. La misma comparación un año antes (2023T2-2024T1 frente a 2024T2-2025T1) dio -0,68 pp: la cuota ya bajaba antes de abril de 2025. La descripción no separa los visados de oro (no hay distinción UE/extra-UE ni autorizaciones del OPI).

<a id="v16-q8-3"></a>
## Serie anual (agregado de entrenamiento)
| Año | No residentes | Total | Cuota (%) |
|---|---|---|---|
| 2018 | 34374 | 399146 | 8,61 |
| 2019 | 32681 | 395443 | 8,26 |
| 2020 | 22946 | 340723 | 6,73 |
| 2021 | 33927 | 473675 | 7,16 |
| 2022 | 49157 | 505994 | 9,71 |
| 2023 | 43296 | 454333 | 9,53 |
| 2024 | 45087 | 509974 | 8,84 |
| 2025 | 41239 | 545383 | 7,56 |
| 2026 | 18307 | 255069 | 7,18 |

2026 recoge solo dos trimestres. Provincias con más cuota en 2025: Alicante/Alacant 33,2 %, Málaga 27,9 %, Girona 14,7 %, Almería 8,2 %, Castellón/Castelló 5,6 % (output/v16/q8/q8_provincias.csv).

## Diagnósticos
| Prueba | Estado | Detalle |
|---|---|---|
| Q8 · distinción UE / fuera de la UE | no disponible | la fuente MIVAU no la trae (adenda, R23); solo no residentes totales, extranjeros y españoles |
| Q8 · muestra | informativa | agregado de 9 CCAA de entrenamiento + Ceuta y Melilla; el total nacional se descarta porque incluye las 8 CCAA de v6 |
| Q8 · comparación con el año anterior | informativa | variación de la cuota un año antes: -0,68 pp frente a -1,33 pp |
| Q8 · pruebas de diseño (pretendencias, placebos, sensibilidad) | no aplica | descriptiva: sin estimador de efecto |

## Límites
Descriptiva. Sin distinción UE/extra-UE: la cuota total de no residentes no identifica los visados de oro. No hay autorizaciones del OPI. Ninguna lectura causal sobre el fin de la golden visa. Lista de p-valores: vacía. Ficha reproducible: `python3 src/v16/q8_no_residentes.py` sobre data/raw/mivau_transacciones_residencia.csv; salidas en output/v16/q8/.
