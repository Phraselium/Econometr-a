# gva_vut: registro de viviendas de uso turístico (Generalitat Valenciana)

Fuente: dadesobertes.gva.es (CKAN), conjuntos `dades-turisme-habitatges-comunitat-valenciana-2025` (histórico y último periodo) y `tur-gestur-vt` (diario). Licencia CC BY 4.0 (`license_id` cc-by). Script: `src/v9/fetch_gva_vut.py`.

## Cortes
| Fichero (cortes/) | Corte | Formato | Filas | Estado |
|---|---|---|---|---|
| vut_historico_2025-01-26.csv.gz | 2025-01-26 (fecha del conjunto; el nombre del recurso lleva 1960-01-01) | rico (Estado, Fecha alta, Fecha baja) | 182.893 | ALTA 101.222 / BAJA 81.671 |
| vut_ultimo_periodo_2025-01-26.csv.gz | 2025-01-26 | rico | 101.408 | ALTA 101.401 / BAJA 7 |
| vut_actual_2026-10-14.csv.gz | 2026-10-14 (metadata del conjunto diario) | reducido (sin estado ni baja) | 90.124 | todas vigentes |

Codificación: latin-1, separador `;`. Códigos: municipio INE 5 dígitos = `Cod. Provincia` (2) + `Cod. Municipio` (3); CP con 5 dígitos.

## Cómo se fechan altas y bajas
- **Alta**: campo `Fecha alta` (dd/mm/aaaa), presente en los tres cortes.
- **Baja**: campo `Fecha baja`, solo en el histórico rico (81.662 filas con fecha). Supuesto: una baja es efectiva desde esa fecha.
- **Estado**: `Estado` = ALTA/BAJA en el histórico. En el último periodo sigue como ALTA casi todo.
- El corte reducido de 2026 no trae baja: las bajas entre 2025-01-26 y 2026-10-14 solo se pueden inferir por diferencia de `signatura` (no hecho en esta tarea; pendiente).
- Discrepancia: el histórico cuenta 101.222 ALTA y el último periodo 101.401 en la misma fecha de referencia (diferencia de 179 registros; no resuelta).
- Fechas de alta anteriores a 2015 pueden ser retroactivas (migración del registro); el stock mensual 2015-2025 las trata como altas en su fecha.

## Paneles
- `gva_vut_panel_municipio.csv` (ine5, tipo, fecha, stock): `corte` en 2025-01-26 y 2026-10-14; `mensual_reconstruido` 2015-01 a 2025-01 desde el histórico (stock a fin de mes = alta <= fin de mes y (sin baja o baja > fin de mes)).
- `gva_vut_panel_cp.csv`: misma estructura por código postal.
- Stock mensual reconstruido solo hasta 2025-01 porque el histórico termina en esa fecha.

## Limitaciones
- La retirada de viviendas sin referencia catastral en 2025 (prensa, no verificada) explica parte de la caída entre cortes; no se corrige.
- Los conteos son de registro, no de ocupación ni de plazas; no equivalen a las viviendas del INE (`ine_v2_vut`).
- Suma de control frente a cifra publicada: PENDIENTE (no se ha localizado una cifra oficial verificada del total de registros en esta tarea).
