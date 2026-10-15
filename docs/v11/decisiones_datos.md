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
8. **MNP municipal**: solo existe en microdatos (INEbase llega a provincia). Se leen los cuatro diseños de registro de
   nacimientos (1980-95, 1996-2006, 2007-15, 2016-) y los tres de defunciones (1980-98, 1999-2008, 2009-); 1975-1979
   no se incorpora (otro diseño; fuera del periodo de análisis). Municipio = residencia de la madre (nacimientos) y del
   fallecido (defunciones). Nacionalidad disponible desde 1996 (nacimientos, de la madre) y 1999 (defunciones); antes,
   «NC». Validación: totales nacionales iguales a los publicados (1985: 456.298 nacimientos; 2023: 320.656 nacimientos y
   436.124 defunciones).
9. **EMCR**: validada contra la tabla publicada 69696 (València 2024: 37.891 inmigraciones del extranjero en ambos) y
   saldo interior nacional = 0 en cada año.
10. **OPI e Interior** (residentes con certificado o tarjeta, protección internacional y temporal por provincia):
    sus webs rechazan el acceso desde el entorno (403 o Cloudflare). Respaldo de nivel NACIONAL por nacionalidad con
    Eurostat (migr_asyappctzm, migr_asydcfstq, migr_asytpsm/fm/fa, migr_resvalid), solo con sexo y edad totales y sin
    celdas a 0 (tamaño). El desglose provincial queda en fuentes_fallidas.md y en las solicitudes (bloque 5).
11. **ECP**: se añade la serie TRIMESTRAL provincial por nacionalidad (56947, 2002T1-2025T1; 82104, 2025T2-) y la
    población en viviendas familiares por nacionalidad (60129). La ECP no publica hogares por nacionalidad; ese cruce
    sale del Censo 2021 y de los microdatos EPA y ECV.
12. **Eventos BOE**: legislación consolidada de ámbito estatal por título y las referencias posteriores (modificaciones,
    desarrollos, sentencias) de las normas núcleo. «alcance» es una etiqueta por palabras del título; la fecha de la
    norma modificadora se extrae del texto de la referencia (vacía si no se puede leer; el identificador BOE se
    conserva siempre).
