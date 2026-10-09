# Fuentes fallidas o incompletas

Registro de descargas que no funcionan, están truncadas o no se han podido verificar.
Los datos de la tabla "no descargado" no se han inventado.

## Banco de España

| Dato | Estado | URLs / búsquedas probadas | Alternativa propuesta |
|---|---|---|---|
| Esfuerzo teórico anual (accesibilidad a la vivienda) | No encontrado | Descarga de los 400 CSV enlazados desde `temas/estadisticas-economicas-generales`, `temas/instituciones-financieras`, `temas/tipos-interes`, `temas/sociedades-no-financieras` y `temas/mercados-financieros`; búsqueda de "esfuerzo" y "accesib" en cabeceras y páginas: sin resultados | Calcular el indicador a partir de la cuota (tipo ECB `ecb_tipo_hipotecario_es.csv` + precio `bde_precio_vivienda_libre.csv`) y de renta de INE/Eurostat (fuera de este script). Revisar la visualización "Indicadores del mercado de la vivienda" de BIEST manualmente. |
| Páginas de estadísticas con índice de indicadores de vivienda | 404 | `https://www.bde.es/webbe/es/estadisticas/indicadores/si1_1.html`, `https://www.bde.es/webbe/es/estadisticas/temas/si_1_5.html` | Usar los CSV de boletín (`compartido/datos/csv/beNNNN.csv`) que sí funcionan. |
| Índice de carpeta `compartido/datos/csv/` | 403 | `https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/` | Enlaces directos a cada CSV (funcionan). |

Series BdE descargadas (ver `src/fetch_bde.py`):
- `be2507.csv`: precio medio m2 de vivienda libre tasada (`DHIVTNOAPLPMMUVT_*`). Trimestral. Las series de vivienda nueva y usada solo tienen datos desde 2013. El origen "Ministerio de Vivienda" del enunciado no aparece en el CSV ni en la página del BdE; queda sin confirmar.
- `be1901.csv`: tipo medio de adquisición de vivienda libre (`D_1T9H0000`). Mensual.

## Banco Central Europeo (data-api)

| Serie | Problema | Alternativa propuesta |
|---|---|---|
| `ICP/M.ES.N.000000.4.ANR` (IAPC España, tasa anual) | La serie termina en 2025-12 (estado `E`, estimada). El BCE indica en la metainformación que deja de publicar el índice actual tras el cambio metodológico de 2026. | Eurostat `prc_hicp_manr` (geo=ES, coicop=CP00), fuera del alcance de este script. |
| `FM/B.U2.EUR.4F.KR.MRR_FR.LEV` (tipo BCE operaciones principales) | Serie de fechas de cambio: 48 observaciones (la última 2026-09-16), no mensual. | Expandir a mensual con el tipo vigente a cierre de mes en la capa de limpieza (data-cleaner). |
