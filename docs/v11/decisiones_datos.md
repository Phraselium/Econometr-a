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
13. **Censo 2021**: las 37 tablas predefinidas (tpx) de viviendas, hogares y núcleos no cruzan con la nacionalidad.
    El cruce sale de los microdatos de personas (muestra del 10 % de hogares): recuentos MUESTRALES sin elevar por
    municipio × nacionalidad de la primera persona del hogar (NORDEN=01, aproximación a la persona de referencia;
    el censo no la identifica) × tenencia × superficie × tamaño y tipo de hogar × periodo de llegada a España. Los
    municipios < 10.000 hab. vienen agregados por tamaño en la provincia (PP991/PP992/PP993; no son códigos INE).
    Sección censal: no hay tablas de tenencia ni de hogares por sección más allá de los indicadores de v3.
14. **ECV y EPA** (punto 9): auditoría de variables en docs/v11/auditoria_microdatos_ecv_epa.md; no se calcula nada.
15. **ECEPOV 2021**: microdatos descargados (no versionados) e inventario de variables versionado; el municipio
    solo se identifica en capitales y municipios > 50.000 hab.
16. **Catastro INSPIRE**: el código de municipio del Catastro (DGC) NO es el del INE (DGC 46900 = València,
    INE 46250; DGC 46250 = Turís). Cada edificio se asigna por posición a la sección INE 2025, y la correspondencia
    DGC → INE se guarda y verifica (cuota de edificios en el municipio INE). Área metropolitana operativa: municipios
    de la provincia 46 con centroide a ≤ 20 km del centroide INE de València (49 municipios). El centroide de
    València queda al sur (incluye la Albufera); se acepta y se documenta. Capitales añadidas: Alicante y Castellón.
17. **Segunda pasada y descargas manuales**:
    - los bloqueos se clasifican en servidor y entorno (fuentes_fallidas.md);
    - no se eluden captchas ni retos anti-bots;
    - lo inalcanzable va a docs/v11/descargas_manuales.md;
    - `src/v11/incorporar_manual.py` incorpora lo que el autor suba a data/manual/v11/<fuente>/, con origen «descarga manual del autor».
18. **Área metropolitana**: la definición oficial (ámbito PATEVAL de la GVA, 90 municipios) se une a la operativa
    (20 km) en el Catastro INSPIRE (94 municipios).
19. **Catastro, titularidad**: los CSV de 2024-2026 (sujetos pasivos e inmuebles por tramo de nº de inmuebles y tipo de
    persona) y la serie JAXI de 2012-2023 (titulares por clase urbano o rústico, sin tramos) tienen definiciones distintas.
    Son variables separadas (`catastro_tit_*` y `catastro_titulares_jaxi`); no se encadenan.
20. **Obra nueva por municipio y año**, dos medidas complementarias que no se mezclan:
    - (a) `obra_nueva_viviendas_inspire`: viviendas de edificios residenciales vigentes por año exacto de construcción
      (stock superviviente; cota inferior de lo construido, 94 municipios);
    - (b) `obra_nueva_neta_catastro`: diferencia anual de unidades urbanas residenciales (neta de bajas y de cambios de
      uso; todos los municipios, 2013-2026).
21. **AEAT, IRPF por municipios**:
    - un informe HTML por municipio y ejercicio, sin ficheros descargables;
    - se limita a la Comunitat Valenciana por coste;
    - no hay número de declarantes con rentas inmobiliarias (solo importe y media).
22. **IPVA municipal y de distrito**: códigos INE tomados de los metadatos de la API (tip=AM); por tamaño de la vivienda.
    No existe por antigüedad del contrato a esa escala.
23. **Censo anual**: no publica país de nacimiento ni hogares por municipio. El padrón por país de nacimiento (v9) cubre
    2003-2022 y termina con el padrón continuo.
