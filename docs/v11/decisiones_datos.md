# V11-DATOS · Decisiones

Tarea de solo datos: sin estimaciones, sin tocar salidas publicadas ni muestras selladas; sin subagentes.

1. **Inventario previo** (docs/v11/inventario.md): no se descarga de nuevo nada ya presente en data/raw, data/raw/v9 o la
   base V10 salvo edición nueva.
2. **Convenciones**: `src/v11/comun.py` reutiliza las utilidades de V9 (descarga con caché y reintentos, gzip
   determinista, manifiesto por fuente). Manifiesto consolidado en `data/raw/v11/_manifest.csv` (`make datos_v11`).
3. **Microdatos y originales** (`data/raw/v11/*/original/`) y matrices origen-destino municipales
   (`od_municipios_<año>.parquet`) no se versionan (tamaño): sha256 en el manifiesto y regeneración con `make datos_v11`.
   Se versionan los agregados (saldos y flujos exteriores por municipio).
4. **Municipios < 10.000 hab.**: el INE blanquea su código en EVR y EMCR; se codifican como `PP999` («resto de la
   provincia PP»). Cruces solo por código INE (PP + MMM).
5. **EVR (1988-2021) y EMCR (2021-)**: el nivel municipal anterior a 2021 solo existe en microdatos EVR; la EM
   (2008-2021) es provincial (ya en v9). 2021 aparece en ambas: se conservan las dos y no se mezclan (la EMCR usa
   otra metodología; si discrepan se reportan ambas).
6. **Nacionalidad**: ES si país de nacionalidad = 108 (España); EXT en otro caso. Edad en 4 grupos (0-15, 16-34,
   35-64, 65+).
7. **posterior_prereg**: toda serie con periodos ≥ 2026T3 usada en evaluate_v7/v8/v9 se marca con `marcar_posterior_prereg`
   y no se usa en cálculos.
